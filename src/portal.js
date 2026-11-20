// Vettlo vendor portal: magic-link login, listings, paid positions #1-#10 on a category shortlist (one vendor per
// position, billed monthly or yearly) plus the Basic listing, with invoices, renewals, subscriptions through Paddle
// (Merchant of Record; iyzico kept as an alternative), waitlists, and click and impression reporting. Data lives in the D1 database bound as DB.

const SESSION_DAYS = 30;
const TOKEN_MINUTES = 20;
const BOT_UA = /bot|crawl|spider|slurp|preview|headless|python|curl|wget|httpclient|monitor|scan|facebookexternalhit|embedly/i;

export const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store", ...headers } });

const now = () => new Date().toISOString();
const clean = (v, max) => String(v ?? "").replace(/[\r\u0000]/g, "").trim().slice(0, max);
const oneLine = (v, max) => clean(v, max).replace(/\s*\n\s*/g, " ");
const isEmail = (e) => /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(e);
const isUrl = (u) => { try { const x = new URL(u); return x.protocol === "https:" || x.protocol === "http:"; } catch { return false; } };
const isHttps = (u) => { try { return new URL(u).protocol === "https:"; } catch { return false; } };
// Vendors may type just "example.com": add https://, upgrade http:// and require a real domain. Returns the URL or null.
function toUrl(raw, max = 500) {
  let v = oneLine(raw, max).trim();
  if (!v) return null;
  if (!/^[a-z][a-z0-9+.-]*:\/\//i.test(v)) v = "https://" + v.replace(/^\/+/, "");
  v = v.replace(/^http:\/\//i, "https://");
  try {
    const u = new URL(v);
    if (u.protocol !== "https:" || !/^[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$/i.test(u.hostname) || u.username || u.password) return null;
    return u.href.length <= max ? u.href : null;
  } catch { return null; }
}
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function sha256(s) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
const randomToken = () => [...crypto.getRandomValues(new Uint8Array(32))].map((b) => b.toString(16).padStart(2, "0")).join("");

// ---------- schema (self-migrating, once per isolate)
let migrated = false;
const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS vendors (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, company TEXT, website TEXT,
     balance_cents INTEGER NOT NULL DEFAULT 0, monthly_budget_cents INTEGER, terms_accepted_at TEXT, created_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active')`,
  `CREATE TABLE IF NOT EXISTS login_tokens (hash TEXT PRIMARY KEY, email TEXT NOT NULL, expires_at TEXT NOT NULL, created_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS sessions (hash TEXT PRIMARY KEY, vendor_id INTEGER NOT NULL, expires_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS listings (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, product_name TEXT NOT NULL, website TEXT NOT NULL,
     landing_url TEXT NOT NULL, category TEXT NOT NULL, tool_id TEXT, best_for TEXT, description TEXT, starting_price TEXT,
     bid_cents INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1, status TEXT NOT NULL DEFAULT 'pending', review_note TEXT,
     created_at TEXT NOT NULL, updated_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS clicks (id INTEGER PRIMARY KEY AUTOINCREMENT, listing_id INTEGER NOT NULL, vendor_id INTEGER NOT NULL, category TEXT,
     page TEXT, ts TEXT NOT NULL, ip_hash TEXT, billable INTEGER NOT NULL DEFAULT 0, cost_cents INTEGER NOT NULL DEFAULT 0, reason TEXT)`,
  `CREATE INDEX IF NOT EXISTS clicks_vendor_ts ON clicks(vendor_id, ts)`,
  `CREATE INDEX IF NOT EXISTS clicks_listing_ip ON clicks(listing_id, ip_hash, ts)`,
  `CREATE TABLE IF NOT EXISTS slots (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, listing_id INTEGER NOT NULL, category TEXT NOT NULL,
     position INTEGER NOT NULL, status TEXT NOT NULL, price_cents INTEGER NOT NULL, paid_through TEXT, reserved_until TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS slots_cat_pos ON slots(category, position, status)`,
  `CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, slot_id INTEGER, amount_cents INTEGER NOT NULL,
     status TEXT NOT NULL, provider_ref TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS waitlist (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, listing_id INTEGER NOT NULL, category TEXT NOT NULL,
     position INTEGER NOT NULL, created_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS subs (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, listing_id INTEGER NOT NULL, category TEXT NOT NULL,
     plan TEXT NOT NULL, status TEXT NOT NULL, price_cents INTEGER NOT NULL, started_at TEXT, paid_through TEXT, reserved_until TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS subs_cat_plan ON subs(category, plan, status)`,
  `CREATE TABLE IF NOT EXISTS plan_waitlist (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, listing_id INTEGER NOT NULL, category TEXT NOT NULL,
     plan TEXT NOT NULL, created_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS billing (vendor_id INTEGER PRIMARY KEY, name TEXT, surname TEXT, phone TEXT, tax_id TEXT, address TEXT, city TEXT, country TEXT, zip TEXT, updated_at TEXT)`,
  `CREATE TABLE IF NOT EXISTS pay_sessions (token TEXT PRIMARY KEY, invoice_id INTEGER NOT NULL, vendor_id INTEGER NOT NULL, created_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS impressions (listing_id INTEGER NOT NULL, day TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (listing_id, day))`,
  `CREATE TABLE IF NOT EXISTS iyzico_refs (key TEXT PRIMARY KEY, ref TEXT NOT NULL, created_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS pay_forms (token TEXT PRIMARY KEY, invoice_id INTEGER NOT NULL, vendor_id INTEGER NOT NULL, html TEXT NOT NULL, created_at TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS hits (key TEXT NOT NULL, ts TEXT NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS notices (sub_id INTEGER NOT NULL, kind TEXT NOT NULL, period_end TEXT NOT NULL, created_at TEXT NOT NULL, PRIMARY KEY (sub_id, kind, period_end))`,
  `CREATE INDEX IF NOT EXISTS hits_key_ts ON hits(key, ts)`,
  `CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, kind TEXT NOT NULL,
     status TEXT NOT NULL, note TEXT, provider_ref TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)`,
];
// Columns added after launch (ALTER fails harmlessly once the column exists).
const ALTERS = [
  "ALTER TABLE subs ADD COLUMN period TEXT NOT NULL DEFAULT 'year'",   // 'month' | 'year'
  "ALTER TABLE subs ADD COLUMN provider_sub TEXT",                     // iyzico subscription reference (monthly card plans)
  "ALTER TABLE subs ADD COLUMN auto_renew INTEGER NOT NULL DEFAULT 0", // 1 while an iyzico subscription renews it
  "ALTER TABLE subs ADD COLUMN page TEXT",                             // the page the position is on, e.g. /tools/best-crm-software/
  "ALTER TABLE plan_waitlist ADD COLUMN page TEXT",
  "ALTER TABLE subs ADD COLUMN held_since TEXT",                       // paid, waiting for our review; paid time is added back on approval
  "ALTER TABLE subs ADD COLUMN consent_at TEXT",                       // when the buyer accepted the terms (and Turkish pre-information form / contract) at checkout
];
async function migrate(env) {
  if (migrated) return;
  await env.DB.batch(SCHEMA.map((s) => env.DB.prepare(s)));
  for (const a of ALTERS) { try { await env.DB.prepare(a).run(); } catch {} }
  await migrateLegacyPlans(env);
  migrated = true;
}
// The old Premium plan was 1st place and Pro was 2nd/3rd place (earlier subscriber first). Map them onto positions.
async function migrateLegacyPlans(env) {
  const rows = (await env.DB.prepare("SELECT id, category, plan FROM subs WHERE plan IN ('premium', 'pro') ORDER BY id").all()).results;
  if (rows.length) {
    const live = new Set((await env.DB.prepare(`SELECT id FROM subs WHERE plan IN ('premium', 'pro') AND ${LIVE}`).bind(now()).all()).results.map((r) => r.id));
    const proCount = {}, stmts = [];
    for (const r of [...rows.filter((r) => live.has(r.id)), ...rows.filter((r) => !live.has(r.id))]) {
      let plan = "p1";
      if (r.plan === "pro") { proCount[r.category] = (proCount[r.category] || 0) + 1; plan = proCount[r.category] === 1 ? "p2" : "p3"; }
      stmts.push(env.DB.prepare("UPDATE subs SET plan = ? WHERE id = ?").bind(plan, r.id));
    }
    await env.DB.batch(stmts);
  }
  await env.DB.batch([env.DB.prepare("UPDATE plan_waitlist SET plan = 'p1' WHERE plan = 'premium'"), env.DB.prepare("UPDATE plan_waitlist SET plan = 'p2' WHERE plan = 'pro'"),
    // plans bought before pages could be chosen are on their category's shortlist
    env.DB.prepare("UPDATE subs SET page = '/tools/' || category || '/' WHERE page IS NULL"), env.DB.prepare("UPDATE plan_waitlist SET page = '/tools/' || category || '/' WHERE page IS NULL")]);
}

// ---------- rate limiting (per client IP, stored in D1; old rows are pruned as we go)
export async function rateLimited(env, request, bucket, max, windowSec) {
  if (!env.DB) return false;
  await migrate(env);
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const key = bucket + ":" + (await sha256(ip + "|" + (env.CLICK_SALT || "vettlo"))).slice(0, 32);
  const since = new Date(Date.now() - windowSec * 1000).toISOString();
  const r = await env.DB.prepare("SELECT COUNT(*) AS n FROM hits WHERE key = ? AND ts > ?").bind(key, since).first();
  if (r.n >= max) return true;
  await env.DB.batch([env.DB.prepare("INSERT INTO hits (key, ts) VALUES (?, ?)").bind(key, now()),
    env.DB.prepare("DELETE FROM hits WHERE ts < ?").bind(new Date(Date.now() - 86400e3).toISOString())]);
  return false;
}

// ---------- email (Brevo for vendors; Email Routing fallback for the admin address)
async function sendLoginEmail(env, email, link) {
  const subject = "Your Vettlo vendor portal sign-in link";
  const text = `Sign in to the Vettlo vendor portal:\n\n${link}\n\nThis link expires in ${TOKEN_MINUTES} minutes and can be used once. If you didn't ask for it, ignore this email.`;
  if (env.BREVO_API_KEY) {
    const r = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "api-key": env.BREVO_API_KEY, "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({
        sender: { name: "Vettlo", email: env.MAIL_FROM || "editor@vettlo.com" }, to: [{ email }], subject, textContent: text,
        htmlContent: `<p>Sign in to the Vettlo vendor portal:</p><p><a href="${esc(link)}">Sign in to Vettlo</a></p><p style="color:#666">This link expires in ${TOKEN_MINUTES} minutes and can be used once. If you didn't ask for it, ignore this email.</p>`,
      }),
    });
    if (!r.ok) throw new Error("brevo " + r.status);
    return;
  }
  if (env.SEND && env.FORM_TO && email.toLowerCase() === env.FORM_TO.toLowerCase()) {
    const { EmailMessage } = await import("cloudflare:email");
    const b64 = (s) => { let b = ""; for (const x of new TextEncoder().encode(s)) b += String.fromCharCode(x); return btoa(b); };
    const raw = [`From: Vettlo <forms@vettlo.com>`, `To: <${env.FORM_TO}>`, `Subject: =?UTF-8?B?${b64(subject)}?=`, `Message-ID: <${crypto.randomUUID()}@vettlo.com>`,
      `Date: ${new Date().toUTCString()}`, "MIME-Version: 1.0", "Content-Type: text/plain; charset=UTF-8", "Content-Transfer-Encoding: base64", "",
      b64(text).replace(/.{1,76}/g, "$&\r\n")].join("\r\n");
    await env.SEND.send(new EmailMessage("forms@vettlo.com", env.FORM_TO, raw));
    return;
  }
  throw new Error("no-mailer");
}

// Short notices to the site owner (the FORM_TO address) about vendor activity. Never blocks the request.
async function notifyAdmin(env, subject, lines) {
  try {
    if (!env.SEND || !env.FORM_TO) return;
    const { EmailMessage } = await import("cloudflare:email");
    const text = lines.filter(Boolean).join("\n") + "\n\nAdmin: https://vettlo.com/vendors/admin/";
    const b64 = (x) => { let b = ""; for (const c of new TextEncoder().encode(x)) b += String.fromCharCode(c); return btoa(b); };
    const raw = [`From: Vettlo <forms@vettlo.com>`, `To: <${env.FORM_TO}>`, `Subject: =?UTF-8?B?${b64("[Vettlo portal] " + subject)}?=`, `Message-ID: <${crypto.randomUUID()}@vettlo.com>`,
      `Date: ${new Date().toUTCString()}`, "MIME-Version: 1.0", "Content-Type: text/plain; charset=UTF-8", "Content-Transfer-Encoding: base64", "",
      b64(text).replace(/.{1,76}/g, "$&\r\n")].join("\r\n");
    await env.SEND.send(new EmailMessage("forms@vettlo.com", env.FORM_TO, raw));
  } catch (e) { /* notices are best effort */ }
}

// ---------- auth
function getCookie(request, name) {
  const m = (request.headers.get("cookie") || "").match(new RegExp("(?:^|; )" + name + "=([^;]+)"));
  return m ? m[1] : null;
}
async function currentVendor(request, env) {
  const tok = getCookie(request, "vs");
  if (!tok) return null;
  const row = await env.DB.prepare("SELECT v.* FROM sessions s JOIN vendors v ON v.id = s.vendor_id WHERE s.hash = ? AND s.expires_at > ?")
    .bind(await sha256(tok), now()).first();
  if (!row) return null;
  row.is_admin = isAdminEmail(env, row.email);
  return row;
}
function isAdminEmail(env, email) {
  const e = String(email || "").toLowerCase();
  return !!(env.FORM_TO && e === env.FORM_TO.toLowerCase()) || (env.ADMIN_EMAILS || "").toLowerCase().split(",").map((x) => x.trim()).filter(Boolean).includes(e);
}

async function requestLogin(request, env, data) {
  if (await rateLimited(env, request, "login", 20, 3600)) return json({ ok: false, error: "Too many sign-in requests from your network. Try again in an hour." }, 429);
  const email = oneLine(data.email, 200).toLowerCase();
  if (!isEmail(email)) return json({ ok: false, error: "Enter a valid work email." }, 400);
  if (clean(data.website_hp, 100)) return json({ ok: true }); // honeypot
  let vendor = await env.DB.prepare("SELECT * FROM vendors WHERE email = ?").bind(email).first();
  if (!vendor && isAdminEmail(env, email)) {  // the site owner signs in without the vendor sign-up step
    await env.DB.prepare("INSERT INTO vendors (email, company, website, terms_accepted_at, created_at) VALUES (?, 'Vettlo', 'https://vettlo.com', ?, ?)").bind(email, now(), now()).run();
    vendor = await env.DB.prepare("SELECT * FROM vendors WHERE email = ?").bind(email).first();
  }
  if (!vendor) {
    const company = oneLine(data.company, 120), website = toUrl(data.website, 300);
    if (!data.signup) return json({ ok: false, error: "No account for this email yet. Create one below.", needs_signup: true }, 404);
    if (!company || !website) return json({ ok: false, error: "Add your company name and website, e.g. example.com." }, 400);
    if (!data.accept_terms) return json({ ok: false, error: "Please accept the advertiser terms." }, 400);
    await env.DB.prepare("INSERT INTO vendors (email, company, website, terms_accepted_at, created_at) VALUES (?, ?, ?, ?, ?)")
      .bind(email, company, website, now(), now()).run();
    await notifyAdmin(env, `New vendor account: ${company}`, [`Company: ${company}`, `Website: ${website}`, `Email: ${email}`]);
  }
  const recent = await env.DB.prepare("SELECT COUNT(*) AS n FROM login_tokens WHERE email = ? AND created_at > ?")
    .bind(email, new Date(Date.now() - 3600e3).toISOString()).first();
  if (recent.n >= 5) return json({ ok: false, error: "Too many sign-in requests. Try again in an hour." }, 429);
  const token = randomToken();
  await env.DB.prepare("INSERT INTO login_tokens (hash, email, expires_at, created_at) VALUES (?, ?, ?, ?)")
    .bind(await sha256(token), email, new Date(Date.now() + TOKEN_MINUTES * 60e3).toISOString(), now()).run();
  const link = `${new URL(request.url).origin}/api/auth/verify?token=${token}`;
  try {
    await sendLoginEmail(env, email, link);
  } catch (e) {
    return json({ ok: false, error: "We couldn't send the sign-in email right now. Please contact us." }, 503);
  }
  return json({ ok: true });
}

async function verifyLogin(request, env) {
  const token = new URL(request.url).searchParams.get("token") || "";
  const h = await sha256(token);
  const row = await env.DB.prepare("SELECT * FROM login_tokens WHERE hash = ? AND expires_at > ?").bind(h, now()).first();
  if (!row) return Response.redirect(new URL("/vendors/login/?expired=1", request.url).toString(), 302);
  await env.DB.prepare("DELETE FROM login_tokens WHERE hash = ?").bind(h).run();
  const vendor = await env.DB.prepare("SELECT id, email FROM vendors WHERE email = ?").bind(row.email).first();
  const sess = randomToken();
  await env.DB.prepare("INSERT INTO sessions (hash, vendor_id, expires_at) VALUES (?, ?, ?)")
    .bind(await sha256(sess), vendor.id, new Date(Date.now() + SESSION_DAYS * 864e5).toISOString()).run();
  return new Response(null, { status: 302, headers: {
    location: isAdminEmail(env, vendor.email) ? "/vendors/admin/" : "/vendors/app/",
    "set-cookie": `vs=${sess}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}`,
  } });
}

// ---------- plans: paid positions per category
// p1..p10: that exact place on the category shortlist, review cards and comparison table; one vendor per position.
//          Billed monthly (auto-renewing through iyzico subscriptions when enabled) or yearly (10% off, renewed by invoice).
// basic:   listed first under "Other tools to consider", unlimited seats, yearly.
const POSITIONS = 10;
const POS_PLANS = Array.from({ length: POSITIONS }, (_, i) => "p" + (i + 1));
const PLANS = [...POS_PLANS, "basic"];
const CAPACITY = Object.fromEntries([...POS_PLANS.map((p) => [p, 1]), ["basic", Infinity]]);
const PLAN_NAME = { ...Object.fromEntries(POS_PLANS.map((p, i) => [p, `#${i + 1} position`])), basic: "Basic", premium: "Premium", pro: "Pro" };
const posOf = (plan) => (/^p\d+$/.test(plan) ? Number(plan.slice(1)) : 0);
const RESERVE_DAYS = 7;       // an unpaid reservation holds a seat this long
const WAITLIST_HOURS = 72;    // when a seat frees up, the first vendor on its waitlist gets it first for this long
const DEFAULT_MONTHLY = [15000, 9900, 7900, 5900, 4900, 3900, 2900, 1900, 1200, 1000]; // cents per month, positions 1..10
const YEAR_DISCOUNT = 0.10;   // yearly = 12 months minus 10%
const BASIC_YEAR = 5000;      // cents per year
function priceTable(env) {
  const m = (env.POSITION_PRICES || "").split(",").map((x) => Number(x.trim()));
  const monthly = m.length === POSITIONS && m.every((x) => x > 0) ? m : DEFAULT_MONTHLY;
  const t = { basic: { year: Number(env.BASIC_PRICE) > 0 ? Number(env.BASIC_PRICE) : BASIC_YEAR } };
  POS_PLANS.forEach((p, i) => { t[p] = { month: monthly[i], year: Math.round(monthly[i] * 12 * (1 - YEAR_DISCOUNT)) }; });
  return t;
}
const priceOf = (env, plan, period) => (priceTable(env)[plan] || {})[period] || null;
const PERIODS = ["month", "year"];
const addMonth = (iso) => { const d = new Date(iso); const day = d.getUTCDate(); d.setUTCMonth(d.getUTCMonth() + 1); if (d.getUTCDate() < day) d.setUTCDate(0); return d.toISOString(); };
const addYear = (iso) => { const d = new Date(iso); const day = d.getUTCDate(); d.setUTCFullYear(d.getUTCFullYear() + 1); if (d.getUTCDate() < day) d.setUTCDate(0); return d.toISOString(); };
const later = (a, b) => (!a ? b : !b ? a : a > b ? a : b);
const LIVE = "((status = 'active' AND paid_through > ?1) OR (status = 'reserved' AND reserved_until > ?1))";

async function occupants(env, page, plan) {
  return (await env.DB.prepare(`SELECT * FROM subs WHERE page = ?2 AND plan = ?3 AND ${LIVE} ORDER BY id ASC`).bind(now(), page, plan).all()).results;
}
async function freedAt(env, page, plan) {
  const r = await env.DB.prepare(`SELECT MAX(t) AS t FROM (SELECT CASE WHEN status = 'cancelled' THEN updated_at WHEN paid_through IS NOT NULL THEN paid_through ELSE reserved_until END AS t
    FROM subs WHERE page = ? AND plan = ?) WHERE t <= ?`).bind(page, plan, now()).first();
  return r && r.t;
}
// Pages vendors can buy positions on (category shortlists and their alternatives pages), from /data/categories.json.
async function pageIndex(env, request) {
  const m = new Map();
  for (const c of await categories(env, request))
    for (const p of c.pages || [{ url: `/tools/${c.slug}/`, title: c.name, kind: "shortlist" }])
      m.set(p.url, { ...p, category: c.slug, category_name: c.name, dept: c.dept });
  return m;
}
async function planState(env, pg, vendorId) {
  const P = priceTable(env), out = [];
  for (const plan of PLANS) {
    if (plan === "basic" && pg.kind !== "shortlist") continue;  // "Other tools to consider" exists only on shortlists
    const occ = await occupants(env, pg.url, plan);
    const wl = plan === "basic" ? [] : (await env.DB.prepare("SELECT vendor_id FROM plan_waitlist WHERE page = ? AND plan = ? ORDER BY created_at ASC, id ASC").bind(pg.url, plan).all()).results;
    const st = { plan, name: PLAN_NAME[plan], position: posOf(plan), month_cents: P[plan].month || null, year_cents: P[plan].year, capacity: CAPACITY[plan] === Infinity ? null : CAPACITY[plan], used: occ.length, waitlist: wl.length, on_waitlist: wl.some((w) => w.vendor_id === vendorId) };
    const mine = occ.find((o) => o.vendor_id === vendorId);
    if (mine) { st.state = mine.status === "active" ? "yours" : "reserved_by_you"; st.until = mine.status === "active" ? mine.paid_through : mine.reserved_until; st.sub_id = mine.id; st.period = mine.period; st.auto_renew = !!mine.auto_renew; }
    else if (occ.length >= CAPACITY[plan]) { st.state = "full"; st.until = occ.map((o) => (o.status === "active" ? o.paid_through : o.reserved_until)).sort()[0]; }
    else {
      const f = wl.length ? await freedAt(env, pg.url, plan) : null;
      const ends = f ? new Date(Date.parse(f) + WAITLIST_HOURS * 3600e3).toISOString() : null;
      if (ends && ends > now() && wl[0].vendor_id !== vendorId) { st.state = "priority_other"; st.until = ends; } else st.state = "available";
    }
    out.push(st);
  }
  return out;
}

async function categories(env, request) {
  const r = await env.ASSETS.fetch(new Request(new URL("/data/categories.json", request.url)));
  return r.ok ? r.json() : [];
}

// ---------- vendor API
async function vendorApi(request, env, vendor, path) {
  const method = request.method;
  const body = method === "GET" ? {} : await request.json().catch(() => ({}));
  const since30 = new Date(Date.now() - 30 * 864e5).toISOString();

  if (path === "/api/me" && method === "GET") {
    return json({ ok: true, vendor: { id: vendor.id, email: vendor.email, company: vendor.company, website: vendor.website, is_admin: vendor.is_admin },
      payments: payMode(env), subscriptions: subsEnabled(env) || payMode(env) === "paddle" });
  }
  if (path === "/api/me" && method === "PUT") {
    const company = oneLine(body.company, 120) || vendor.company;
    const website = toUrl(body.website, 300) || vendor.website;
    await env.DB.prepare("UPDATE vendors SET company = ?, website = ? WHERE id = ?").bind(company, website, vendor.id).run();
    return json({ ok: true });
  }
  if (path === "/api/logout" && method === "POST") {
    const tok = getCookie(request, "vs");
    if (tok) await env.DB.prepare("DELETE FROM sessions WHERE hash = ?").bind(await sha256(tok)).run();
    return json({ ok: true }, 200, { "set-cookie": "vs=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0" });
  }
  if (path === "/api/listings" && method === "GET") {
    const rows = (await env.DB.prepare("SELECT * FROM listings WHERE vendor_id = ? ORDER BY created_at DESC").bind(vendor.id).all()).results;
    for (const l of rows) {
      const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM clicks WHERE listing_id = ? AND ts >= ? AND billable = 1").bind(l.id, since30).first();
      const im = await env.DB.prepare("SELECT COALESCE(SUM(n),0) AS n FROM impressions WHERE listing_id = ? AND day >= ?").bind(l.id, since30.slice(0, 10)).first();
      const subs = (await env.DB.prepare(`SELECT * FROM subs WHERE listing_id = ?2 AND ${LIVE} ORDER BY id DESC`).bind(now(), l.id).all()).results;
      Object.assign(l, { clicks_30d: c.n, impressions_30d: im.n, subs, sub: subs[0] || null });
    }
    return json({ ok: true, listings: rows });
  }
  if (path === "/api/listings" && method === "POST") {
    const cats = await categories(env, request);
    const cat = cats.find((c) => c.slug === body.category);
    const f = { product_name: oneLine(body.product_name, 80), website: toUrl(body.website, 300), landing_url: toUrl(body.landing_url || body.website, 500),
      best_for: oneLine(body.best_for, 90), description: clean(body.description, 600), starting_price: oneLine(body.starting_price, 80) };
    if (!f.product_name || !f.website || !f.landing_url) return json({ ok: false, error: "Add the product name and its website, e.g. example.com." }, 400);
    if (await rateLimited(env, request, "listing:" + vendor.id, 20, 86400)) return json({ ok: false, error: "Too many new products today. Contact us if you need more." }, 429);
    if (!cat) return json({ ok: false, error: "Choose a category." }, 400);
    const tool = (cat.tools || []).find((t) => t.name.toLowerCase() === f.product_name.toLowerCase());
    const r = await env.DB.prepare(`INSERT INTO listings (vendor_id, product_name, website, landing_url, category, tool_id, best_for, description, starting_price, created_at, updated_at)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)`).bind(vendor.id, f.product_name, f.website, f.landing_url, cat.slug, tool ? tool.id : null, f.best_for, f.description, f.starting_price, now(), now()).run();
    await notifyAdmin(env, `New product to review: ${f.product_name}`, [`${vendor.company} added ${f.product_name} (${f.website}) for ${cat.name}.`, "Review it in the admin portal. It stays pending for the vendor until you approve it."]);
    return json({ ok: true, id: r.meta.last_row_id });
  }
  let m = path.match(/^\/api\/listings\/(\d+)$/);
  if (m && method === "PUT") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(m[1]), vendor.id).first();
    if (!l) return json({ ok: false, error: "Not found." }, 404);
    const active = body.active !== undefined ? (body.active ? 1 : 0) : l.active;
    const landing = body.landing_url !== undefined ? toUrl(body.landing_url, 500) : l.landing_url;
    if (!landing) return json({ ok: false, error: "Enter a valid landing page, e.g. example.com/pricing." }, 400);
    // Copy edits go back to editorial review; pausing and landing page changes don't.
    const copy = ["best_for", "description", "starting_price"].some((k) => body[k] !== undefined && oneLine(body[k], 600) !== (l[k] || ""));
    const status = copy && l.status === "approved" ? "pending" : l.status;
    await env.DB.prepare(`UPDATE listings SET active = ?, landing_url = ?, best_for = COALESCE(?, best_for), description = COALESCE(?, description),
      starting_price = COALESCE(?, starting_price), status = ?, updated_at = ? WHERE id = ?`)
      .bind(active, landing, body.best_for !== undefined ? oneLine(body.best_for, 90) : null, body.description !== undefined ? clean(body.description, 600) : null,
        body.starting_price !== undefined ? oneLine(body.starting_price, 80) : null, status, now(), l.id).run();
    if (status !== l.status) await notifyAdmin(env, `Listing edited, review again: ${l.product_name}`, [`${vendor.company} changed the copy of ${l.product_name}. It's hidden until you approve it again.`]);
    return json({ ok: true, resubmitted: status !== l.status });
  }
  if (path === "/api/pages" && method === "GET") {
    const pages = [...(await pageIndex(env, request)).values()];
    const taken = (await env.DB.prepare(`SELECT page, COUNT(DISTINCT plan) AS n FROM subs WHERE plan != 'basic' AND ${LIVE} GROUP BY page`).bind(now()).all()).results;
    const t = Object.fromEntries(taken.map((r) => [r.page, r.n]));
    return json({ ok: true, prices: priceTable(env), positions: POSITIONS, pages: pages.map((p) => ({ ...p, free: POSITIONS - (t[p.url] || 0) })) });
  }
  if (path === "/api/plans" && method === "GET") {
    const pg = (await pageIndex(env, request)).get(new URL(request.url).searchParams.get("page") || "");
    if (!pg) return json({ ok: false, error: "Choose a page." }, 400);
    return json({ ok: true, page: pg, plans: await planState(env, pg, vendor.id) });
  }
  if (path === "/api/subscribe" && method === "POST") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(body.listing_id), vendor.id).first();
    const plan = PLANS.includes(body.plan) ? body.plan : null;
    const period = plan === "basic" ? "year" : PERIODS.includes(body.period) ? body.period : "month";
    if (!l) return json({ ok: false, error: "Choose one of your listings." }, 400);
    if (!plan) return json({ ok: false, error: "Choose a plan." }, 400);
    if (body.accept_terms !== true) return json({ ok: false, error: "Please accept the terms to place your order." }, 400);
    const pg = (await pageIndex(env, request)).get(String(body.page || `/tools/${l.category}/`));
    if (!pg) return json({ ok: false, error: "Choose a page." }, 400);
    if (pg.category !== l.category) return json({ ok: false, error: "This product is listed in another category. Add it for this category first." }, 400);
    if (pg.exclude && l.tool_id === pg.exclude) return json({ ok: false, error: "A product can't take a position on its own alternatives page." }, 400);
    if (plan === "basic" && pg.kind !== "shortlist") return json({ ok: false, error: "Basic listings are only on category shortlists." }, 400);
    const amount = priceOf(env, plan, period);
    if (!amount) return json({ ok: false, error: "This billing period isn't available for this plan." }, 400);
    if (l.status === "rejected") return json({ ok: false, error: "This listing wasn't approved. Edit it and resubmit first." }, 400);
    const own = await env.DB.prepare(`SELECT 1 FROM subs WHERE listing_id = ?2 AND page = ?3 AND ${LIVE}`).bind(now(), l.id, pg.url).first();
    if (own) return json({ ok: false, error: "This product already has a position on this page. To change it, contact us." }, 400);
    const st = (await planState(env, pg, vendor.id)).find((x) => x.plan === plan);
    if (st.state !== "available") return json({ ok: false, error: st.state === "priority_other" ? "A vendor on the waitlist has first claim on this plan until " + st.until.slice(0, 10) + "." : "This plan is full in this category. Join the waitlist to get the next seat." }, 409);
    const r = await env.DB.prepare("INSERT INTO subs (vendor_id, listing_id, category, page, plan, period, status, price_cents, reserved_until, consent_at, created_at, updated_at) VALUES (?,?,?,?,?,?, 'reserved', ?,?,?,?,?)")
      .bind(vendor.id, l.id, l.category, pg.url, plan, period, amount, new Date(Date.now() + RESERVE_DAYS * 864e5).toISOString(), now(), now(), now()).run();
    const subId = r.meta.last_row_id;
    // Race check: the earliest rows win the seats.
    const occ = await occupants(env, pg.url, plan);
    if (occ.findIndex((o) => o.id === subId) >= CAPACITY[plan]) { await env.DB.prepare("UPDATE subs SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), subId).run(); return json({ ok: false, error: "Someone took the last seat a moment ago." }, 409); }
    await env.DB.batch([
      env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(vendor.id, subId, amount, now(), now()),
      env.DB.prepare("DELETE FROM plan_waitlist WHERE vendor_id = ? AND page = ? AND plan = ?").bind(vendor.id, pg.url, plan),
    ]);
    await notifyAdmin(env, `Plan reserved: ${PLAN_NAME[plan]} for ${l.product_name}`, [`${vendor.company} reserved ${PLAN_NAME[plan]} (${period === "month" ? "monthly" : "yearly"}) on ${pg.url} for ${l.product_name}.`,
      `Invoice: ${money(amount)} per ${period}, open for ${RESERVE_DAYS} days.`, payMode(env) === "iyzico" ? "They can pay by card in the portal." : "Send them an invoice, then mark it paid in the admin page.", l.status !== "approved" ? "The listing still needs your approval." : ""]);
    return json({ ok: true, sub_id: subId, method: payMode(env) });
  }
  m = path.match(/^\/api\/subs\/(\d+)\/(renew|cancel|stop)$/);
  if (m && method === "POST") {
    const s = await env.DB.prepare("SELECT * FROM subs WHERE id = ? AND vendor_id = ?").bind(Number(m[1]), vendor.id).first();
    if (!s) return json({ ok: false, error: "Not found." }, 404);
    if (m[2] === "cancel") {
      if (s.status !== "reserved") return json({ ok: false, error: "Only unpaid reservations can be cancelled. A paid plan simply ends if you don't renew it." }, 400);
      await env.DB.batch([
        env.DB.prepare("UPDATE subs SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), s.id),
        env.DB.prepare("UPDATE invoices SET status = 'cancelled', updated_at = ? WHERE slot_id = ? AND status = 'requested'").bind(now(), s.id),
      ]);
      return json({ ok: true });
    }
    if (m[2] === "stop") {
      if (!s.auto_renew || !s.provider_sub) return json({ ok: false, error: "This plan doesn't renew automatically." }, 400);
      if (s.provider_sub.startsWith("paddle:")) {
        const c = await paddleCancel(env, s, "next_billing_period");
        if (!c.ok) return json({ ok: false, error: "We couldn't stop the renewal right now (" + c.error + "). Please contact us." }, 502);
        await notifyAdmin(env, "Automatic renewal stopped", [`${vendor.company} stopped the automatic renewal of subscription ${s.id} (${PLAN_NAME[s.plan]} on ${s.page}). It stays live until ${String(s.paid_through).slice(0, 10)}.`]);
        return json({ ok: true });
      }
      const r = await iyzico(env, `/v2/subscription/subscriptions/${encodeURIComponent(s.provider_sub)}/cancel`, {});
      if (r.status !== "success") return json({ ok: false, error: "We couldn't stop the renewal right now" + (r.errorMessage ? ": " + r.errorMessage : ".") + " Please contact us." }, 502);
      await env.DB.prepare("UPDATE subs SET auto_renew = 0, updated_at = ? WHERE id = ?").bind(now(), s.id).run();
      await notifyAdmin(env, "Monthly renewal stopped", [`${vendor.company} stopped the monthly renewal of subscription ${s.id} (${PLAN_NAME[s.plan]} on ${s.page}). It stays live until ${String(s.paid_through).slice(0, 10)}.`]);
      return json({ ok: true });
    }
    if (s.status !== "active" || s.paid_through <= now()) return json({ ok: false, error: "This plan has ended. Subscribe again if a seat is available." }, 400);
    if (s.auto_renew) return json({ ok: false, error: "This plan renews automatically." }, 400);
    const open = await env.DB.prepare("SELECT 1 FROM invoices WHERE slot_id = ? AND status = 'requested'").bind(s.id).first();
    if (open) return json({ ok: false, error: "A renewal invoice is already open for this plan." }, 400);
    const price = priceOf(env, s.plan, s.period || "year");
    await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(vendor.id, s.id, price, now(), now()).run();
    return json({ ok: true, method: payMode(env) });
  }
  if (path === "/api/waitlist" && method === "POST") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(body.listing_id), vendor.id).first();
    const pg = (await pageIndex(env, request)).get(String(body.page || ""));
    if (!l || !pg || pg.category !== l.category || !POS_PLANS.includes(body.plan)) return json({ ok: false, error: "Choose a product, page and position." }, 400);
    const dup = await env.DB.prepare("SELECT 1 FROM plan_waitlist WHERE vendor_id = ? AND page = ? AND plan = ?").bind(vendor.id, pg.url, body.plan).first();
    if (!dup) await env.DB.prepare("INSERT INTO plan_waitlist (vendor_id, listing_id, category, page, plan, created_at) VALUES (?,?,?,?,?,?)").bind(vendor.id, l.id, l.category, pg.url, body.plan, now()).run();
    return json({ ok: true });
  }
  if (path === "/api/waitlist/leave" && method === "POST") {
    await env.DB.prepare("DELETE FROM plan_waitlist WHERE vendor_id = ? AND page = ? AND plan = ?").bind(vendor.id, oneLine(body.page, 200), oneLine(body.plan, 20)).run();
    return json({ ok: true });
  }
  if (path === "/api/billing" && method === "GET") {
    return json({ ok: true, billing: (await env.DB.prepare("SELECT * FROM billing WHERE vendor_id = ?").bind(vendor.id).first()) || {} });
  }
  if (path === "/api/billing" && method === "PUT") {
    const f = {}; for (const k of ["name", "surname", "phone", "tax_id", "address", "city", "country", "zip"]) f[k] = oneLine(body[k], k === "address" ? 300 : 80);
    await env.DB.prepare(`INSERT INTO billing (vendor_id, name, surname, phone, tax_id, address, city, country, zip, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(vendor_id) DO UPDATE SET name=excluded.name, surname=excluded.surname, phone=excluded.phone, tax_id=excluded.tax_id, address=excluded.address,
      city=excluded.city, country=excluded.country, zip=excluded.zip, updated_at=excluded.updated_at`).bind(vendor.id, f.name, f.surname, f.phone, f.tax_id, f.address, f.city, f.country, f.zip, now()).run();
    return json({ ok: true });
  }
  if (path === "/api/pay" && method === "POST") return startCardPayment(request, env, vendor, body);
  if (path === "/api/invoices" && method === "GET") {
    const rows = (await env.DB.prepare(`SELECT i.*, s.category, s.page, s.plan, s.period, l.product_name FROM invoices i LEFT JOIN subs s ON s.id = i.slot_id LEFT JOIN listings l ON l.id = s.listing_id
      WHERE i.vendor_id = ? ORDER BY i.created_at DESC LIMIT 100`).bind(vendor.id).all()).results;
    return json({ ok: true, rows });
  }
  if (path === "/api/reports" && method === "GET") {
    const days = Math.min(90, Math.max(1, Number(new URL(request.url).searchParams.get("days")) || 30));
    const since = new Date(Date.now() - days * 864e5).toISOString().slice(0, 10);
    const imp = (await env.DB.prepare(`SELECT i.day, i.listing_id, l.product_name, l.category, i.n FROM impressions i JOIN listings l ON l.id = i.listing_id WHERE l.vendor_id = ? AND i.day >= ?`).bind(vendor.id, since).all()).results;
    const clk = (await env.DB.prepare(`SELECT substr(c.ts,1,10) AS day, c.listing_id, l.product_name, l.category, SUM(c.billable) AS n FROM clicks c JOIN listings l ON l.id = c.listing_id
      WHERE c.vendor_id = ? AND c.ts >= ? GROUP BY day, c.listing_id`).bind(vendor.id, since).all()).results;
    const map = new Map();
    for (const r of imp) map.set(r.day + "|" + r.listing_id, { day: r.day, product_name: r.product_name, category: r.category, impressions: r.n, clicks: 0 });
    for (const r of clk) { const k = r.day + "|" + r.listing_id; const e = map.get(k) || { day: r.day, product_name: r.product_name, category: r.category, impressions: 0, clicks: 0 }; e.clicks = r.n; map.set(k, e); }
    return json({ ok: true, rows: [...map.values()].sort((a, b) => (a.day < b.day ? 1 : -1)) });
  }
  return null;
}

// ---------- admin API
async function adminApi(request, env, vendor, path) {
  if (!vendor.is_admin) return json({ ok: false, error: "Forbidden." }, 403);
  const method = request.method;
  const body = method === "GET" ? {} : await request.json().catch(() => ({}));
  if (path === "/api/admin/overview") {
    const q = async (sql, ...b) => (await env.DB.prepare(sql).bind(...b).all()).results;
    return json({ ok: true, now: now(),
      vendors: await q("SELECT id, email, company, website, status, created_at FROM vendors ORDER BY created_at DESC"),
      listings: await q("SELECT l.*, v.company, v.email FROM listings l JOIN vendors v ON v.id = l.vendor_id ORDER BY CASE l.status WHEN 'pending' THEN 0 ELSE 1 END, l.updated_at DESC"),
      subs: await q(`SELECT s.*, l.product_name, l.status AS listing_status, v.company, v.email FROM subs s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
        WHERE (s.status = 'active' AND s.paid_through > ?) OR (s.status = 'reserved' AND s.reserved_until > ?) ORDER BY s.page, CASE WHEN s.plan = 'basic' THEN 99 ELSE CAST(substr(s.plan, 2) AS INTEGER) END, s.started_at`, now(), now()),
      invoices: await q(`SELECT i.*, s.category, s.page, s.plan, s.period, s.status AS sub_status, l.product_name, v.company, v.email FROM invoices i JOIN vendors v ON v.id = i.vendor_id
        LEFT JOIN subs s ON s.id = i.slot_id LEFT JOIN listings l ON l.id = s.listing_id ORDER BY CASE i.status WHEN 'requested' THEN 0 ELSE 1 END, i.created_at DESC LIMIT 200`),
      customers: await q(`SELECT s.*, l.product_name, l.website, l.status AS listing_status, l.tool_id, v.company, v.email,
        (SELECT MAX(i.updated_at) FROM invoices i WHERE i.slot_id = s.id AND i.status = 'paid') AS last_paid_at,
        (SELECT i.provider_ref FROM invoices i WHERE i.slot_id = s.id AND i.status = 'paid' ORDER BY i.updated_at DESC LIMIT 1) AS last_ref,
        (SELECT COALESCE(SUM(i.amount_cents), 0) FROM invoices i WHERE i.slot_id = s.id AND i.status = 'paid') AS paid_total,
        (SELECT i.id FROM invoices i WHERE i.slot_id = s.id AND i.status = 'requested' ORDER BY i.id LIMIT 1) AS open_invoice,
        (SELECT i.amount_cents FROM invoices i WHERE i.slot_id = s.id AND i.status = 'requested' ORDER BY i.id LIMIT 1) AS open_amount
        FROM subs s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
        WHERE s.status = 'active' OR (s.status = 'reserved' AND s.reserved_until > ?) OR s.updated_at > ?
        ORDER BY CASE WHEN s.status = 'active' AND s.paid_through > ? THEN 0 WHEN s.status = 'reserved' THEN 1 ELSE 2 END, s.paid_through`, now(), new Date(Date.now() - 90 * 864e5).toISOString(), now()),
      waitlist: await q("SELECT w.*, l.product_name, v.company FROM plan_waitlist w JOIN listings l ON l.id = w.listing_id JOIN vendors v ON v.id = w.vendor_id ORDER BY w.page, CAST(substr(w.plan, 2) AS INTEGER), w.created_at"),
      stats: await q(`SELECT d.day, COALESCE((SELECT SUM(n) FROM impressions i WHERE i.day = d.day),0) AS impressions, COALESCE((SELECT SUM(billable) FROM clicks c WHERE substr(c.ts,1,10) = d.day),0) AS clicks
        FROM (SELECT DISTINCT day FROM impressions WHERE day >= ? UNION SELECT DISTINCT substr(ts,1,10) FROM clicks WHERE ts >= ?) d ORDER BY d.day DESC`, new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10), new Date(Date.now() - 30 * 864e5).toISOString()) });
  }
  let m = path.match(/^\/api\/admin\/listings\/(\d+)$/);
  if (m && method === "POST") {
    const status = ["approved", "rejected", "pending"].includes(body.status) ? body.status : null;
    if (!status) return json({ ok: false, error: "Bad status." }, 400);
    await env.DB.prepare("UPDATE listings SET status = ?, tool_id = ?, review_note = ?, updated_at = ? WHERE id = ?")
      .bind(status, oneLine(body.tool_id, 60) || null, oneLine(body.review_note, 300) || null, now(), Number(m[1])).run();
    if (status === "approved") await releaseHolds(env, Number(m[1]));
    await clearPlacements();
    return json({ ok: true });
  }
  m = path.match(/^\/api\/admin\/invoices\/(\d+)$/);
  if (m && method === "POST") {
    const inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ?").bind(Number(m[1])).first();
    if (!inv || inv.status !== "requested") return json({ ok: false, error: "Not found or already closed." }, 400);
    if (body.status === "cancelled") {
      await env.DB.prepare("UPDATE invoices SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), inv.id).run();
      return json({ ok: true });
    }
    if (body.status !== "paid") return json({ ok: false, error: "Bad status." }, 400);
    const r = await activateInvoice(env, inv, oneLine(body.ref, 120) || "manual");
    return json(r, r.ok ? 200 : 409);
  }
  if (path === "/api/admin/orders" && method === "POST") return adminCreateOrder(request, env, body);
  if (path === "/api/admin/paddle/sync" && method === "POST") {
    if (!paddleOn(env)) return json({ ok: false, error: "Paddle isn't connected yet (add the PADDLE_* settings in Cloudflare)." }, 400);
    try { const prices = await paddleSyncCatalog(env); return json({ ok: true, count: prices.length, sandbox: paddleSandbox(env), prices }); }
    catch (e) { return json({ ok: false, error: e.message }, 502); }
  }
  m = path.match(/^\/api\/admin\/subs\/(\d+)\/end$/);
  if (m && method === "POST") {
    const s = await env.DB.prepare("SELECT * FROM subs WHERE id = ?").bind(Number(m[1])).first();
    if (s && s.provider_sub && s.provider_sub.startsWith("paddle:")) {
      const c = await paddleCancel(env, s, "immediately");
      if (!c.ok) return json({ ok: false, error: "Paddle didn't cancel the subscription: " + c.error + ". Cancel it in the Paddle dashboard first." }, 502);
    }
    else if (s && s.auto_renew && s.provider_sub) {
      const r = await iyzico(env, `/v2/subscription/subscriptions/${encodeURIComponent(s.provider_sub)}/cancel`, {});
      if (r.status !== "success") return json({ ok: false, error: "iyzico didn't cancel the subscription" + (r.errorMessage ? ": " + r.errorMessage : "") + ". Cancel it in the iyzico panel first." }, 502);
    }
    await env.DB.prepare("UPDATE subs SET status = 'cancelled', auto_renew = 0, updated_at = ? WHERE id = ?").bind(now(), Number(m[1])).run();
    await clearPlacements();
    return json({ ok: true });
  }
  return json({ ok: false, error: "Not found." }, 404);
}

// A paid position shows on the site once the listing is approved and (for ranked positions) matched to a tool we've reviewed.
const liveReady = (l, plan) => !!l && l.status === "approved" && (plan === "basic" || !!l.tool_id);
// Called when a listing is approved: paid time spent waiting for our review is added back to each held plan.
async function releaseHolds(env, listingId) {
  const l = await env.DB.prepare("SELECT status, tool_id FROM listings WHERE id = ?").bind(listingId).first();
  const held = (await env.DB.prepare("SELECT * FROM subs WHERE listing_id = ? AND status = 'active' AND held_since IS NOT NULL").bind(listingId).all()).results;
  for (const s of held) {
    if (!liveReady(l, s.plan)) continue;
    const wait = Math.max(0, Date.now() - Date.parse(s.held_since));
    const until = new Date(Math.max(Date.parse(s.paid_through), Date.now()) + wait).toISOString();
    await env.DB.prepare("UPDATE subs SET paid_through = ?, held_since = NULL, updated_at = ? WHERE id = ?").bind(until, now(), s.id).run();
    await paddleAlignBilling(env, { ...s, paid_through: until });
  }
}
// Marks an invoice paid and starts or extends its plan by its billing period. Shared by the admin page, card payments and subscription renewals.
async function activateInvoice(env, inv, ref) {
  const s = await env.DB.prepare("SELECT * FROM subs WHERE id = ?").bind(inv.slot_id).first();
  if (!s) return { ok: false, error: "The plan for this invoice no longer exists." };
  if (s.status === "cancelled") return { ok: false, error: "This reservation was cancelled." };
  const live = s.status === "active" ? s.paid_through > now() : s.reserved_until > now();
  if (!live) {
    const others = (await occupants(env, s.page, s.plan)).filter((o) => o.id !== s.id);
    if (others.length >= CAPACITY[s.plan]) return { ok: false, error: "This plan lapsed and its seat has been taken. Refund or offer another plan." };
  }
  const extend = s.period === "month" ? addMonth : addYear;
  const paidThrough = extend(s.status === "active" ? later(s.paid_through, now()) : now());
  const r = await env.DB.prepare("UPDATE invoices SET status = 'paid', provider_ref = ?, updated_at = ? WHERE id = ? AND status = 'requested'").bind(ref, now(), inv.id).run();
  if (!r.meta.changes) return { ok: false, error: "This invoice was already closed." };
  await env.DB.prepare("UPDATE subs SET status = 'active', paid_through = ?, started_at = COALESCE(started_at, ?), updated_at = ? WHERE id = ?").bind(paidThrough, now(), now(), s.id).run();
  // Not live yet (our review isn't published): note when the wait started, so approval adds those days back.
  const l = await env.DB.prepare("SELECT status, tool_id FROM listings WHERE id = ?").bind(s.listing_id).first();
  if (!liveReady(l, s.plan)) await env.DB.prepare("UPDATE subs SET held_since = COALESCE(held_since, ?) WHERE id = ?").bind(now(), s.id).run();
  await clearPlacements();
  return { ok: true, paid_through: paidThrough, sub: s };
}

// ---------- card payments through iyzico (Checkout Form)
const money = (c) => "$" + (c / 100).toFixed(2);
function payMode(env) { return paddleOn(env) && env.PADDLE_CHECKOUT === "1" ? "paddle" : env.IYZICO_API_KEY && env.IYZICO_SECRET_KEY ? "iyzico" : "invoice"; }
// Monthly card plans renew through iyzico's Subscription add-on once it's enabled on the merchant account (IYZICO_SUBSCRIPTIONS=1).
const subsEnabled = (env) => payMode(env) === "iyzico" && env.IYZICO_SUBSCRIPTIONS === "1";
const iyzicoBase = (env) => env.IYZICO_BASE_URL || (env.IYZICO_LIVE === "1" ? "https://api.iyzipay.com" : "https://sandbox-api.iyzipay.com");
async function hmacHex(key, msg) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function iyzico(env, path, payload, method = "POST") {
  const body = method === "GET" ? "" : JSON.stringify(payload || {});
  const rnd = Date.now() + "" + Math.floor(Math.random() * 1e9);
  const sig = await hmacHex(env.IYZICO_SECRET_KEY, rnd + path.split("?")[0] + body);
  const auth = btoa(`apiKey:${env.IYZICO_API_KEY}&randomKey:${rnd}&signature:${sig}`);
  const r = await fetch(iyzicoBase(env) + path, { method, body: method === "GET" ? undefined : body,
    headers: { "content-type": "application/json", accept: "application/json", authorization: "IYZWSv2 " + auth, "x-iyzi-rnd": rnd } });
  return r.json().catch(() => ({ status: "failure", errorMessage: "HTTP " + r.status }));
}
const num = (v) => String(Number(v)); // iyzico signs prices without trailing zeros ("50.00" -> "50")

async function startCardPayment(request, env, vendor, body) {
  if (payMode(env) === "paddle") return startPaddle(request, env, vendor, body);
  if (payMode(env) !== "iyzico") return json({ ok: false, error: "Card payments aren't available yet. We'll email you an invoice." }, 400);
  const inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ? AND vendor_id = ? AND status = 'requested'").bind(Number(body.invoice_id), vendor.id).first();
  if (!inv) return json({ ok: false, error: "This invoice isn't open." }, 400);
  const s = await env.DB.prepare("SELECT s.*, l.product_name FROM subs s JOIN listings l ON l.id = s.listing_id WHERE s.id = ?").bind(inv.slot_id).first();
  if (!s || s.status === "cancelled" || (s.status === "reserved" && s.reserved_until <= now())) return json({ ok: false, error: "This reservation has lapsed. Reserve the plan again." }, 400);
  const b = await env.DB.prepare("SELECT * FROM billing WHERE vendor_id = ?").bind(vendor.id).first();
  if (!b || !b.name || !b.surname || !b.phone || !b.tax_id || !b.address || !b.city || !b.country) return json({ ok: false, error: "Add your billing details first (Account tab).", needs_billing: true }, 400);
  const price = (inv.amount_cents / 100).toFixed(2);
  const origin = new URL(request.url).origin;
  const contact = `${b.name} ${b.surname}`;
  const addr = { contactName: contact, city: b.city, country: b.country, address: b.address, zipCode: b.zip || undefined };
  if (s.period === "month" && subsEnabled(env) && s.status === "reserved") return startSubscriptionCheckout(env, vendor, inv, s, b, addr, origin);
  const res = await iyzico(env, "/payment/iyzipos/checkoutform/initialize/auth/ecom", {
    locale: "en", conversationId: String(inv.id), price, paidPrice: price, currency: env.IYZICO_CURRENCY || "USD", basketId: "inv-" + inv.id,
    paymentGroup: "LISTING", callbackUrl: origin + "/api/pay/callback", enabledInstallments: [1],
    buyer: { id: "v" + vendor.id, name: b.name, surname: b.surname, gsmNumber: b.phone, email: vendor.email, identityNumber: b.tax_id,
      registrationAddress: b.address, city: b.city, country: b.country, zipCode: b.zip || undefined, ip: request.headers.get("cf-connecting-ip") || "" },
    billingAddress: addr,
    basketItems: [{ id: "sub-" + s.id, name: `Vettlo ${PLAN_NAME[s.plan]}, 1 ${s.period === "month" ? "month" : "year"}: ${s.product_name}`.slice(0, 120), category1: "Advertising", itemType: "VIRTUAL", price }],
  });
  if (res.status !== "success" || !res.token || !res.paymentPageUrl) return json({ ok: false, error: "The payment page couldn't be opened" + (res.errorMessage ? ": " + res.errorMessage : ".") }, 502);
  await env.DB.prepare("INSERT INTO pay_sessions (token, invoice_id, vendor_id, created_at) VALUES (?,?,?,?)").bind(res.token, inv.id, vendor.id, now()).run();
  return json({ ok: true, url: res.paymentPageUrl });
}

// iyzico posts the token here after the card form; we confirm the result with iyzico before activating anything.
async function cardCallback(request, env) {
  const back = (q) => Response.redirect(new URL("/vendors/app/?" + q + "#invoices", request.url).toString(), 303);
  const form = await request.formData().catch(() => null);
  const token = form ? String(form.get("token") || "") : "";
  const ps = token && (await env.DB.prepare("SELECT * FROM pay_sessions WHERE token = ?").bind(token).first());
  if (!ps) return back("pay=error");
  const res = await iyzico(env, "/payment/iyzipos/checkoutform/auth/ecom/detail", { locale: "en", conversationId: String(ps.invoice_id), token });
  const expected = await hmacHex(env.IYZICO_SECRET_KEY, [res.paymentStatus, res.paymentId, res.currency, res.basketId, res.conversationId, num(res.paidPrice), num(res.price), res.token].join(":"));
  const inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ?").bind(ps.invoice_id).first();
  const ok = res.status === "success" && res.paymentStatus === "SUCCESS" && Number(res.fraudStatus) === 1 && res.signature === expected
    && res.basketId === "inv-" + ps.invoice_id && inv && Math.round(Number(res.paidPrice) * 100) === inv.amount_cents;
  if (!ok) {
    if (res.paymentStatus === "SUCCESS") await notifyAdmin(env, "Card payment needs a manual check", [`Invoice ${ps.invoice_id}: iyzico reported a payment that didn't pass our checks (fraud status ${res.fraudStatus}, payment ${res.paymentId}). Check it in the iyzico panel before marking the invoice paid.`]);
    return back("pay=failed");
  }
  if (inv.status === "paid") return back("pay=ok");
  const r = await activateInvoice(env, inv, "iyzico:" + res.paymentId);
  const v = await env.DB.prepare("SELECT company FROM vendors WHERE id = ?").bind(inv.vendor_id).first();
  if (!r.ok) {
    await notifyAdmin(env, "Paid, but the plan couldn't start", [`${v && v.company} paid invoice ${inv.id} by card (iyzico ${res.paymentId}), but: ${r.error}`, "Refund it in the iyzico panel or contact the vendor."]);
    return back("pay=held");
  }
  const l = await env.DB.prepare("SELECT product_name, status, tool_id FROM listings WHERE id = ?").bind(r.sub.listing_id).first();
  await notifyAdmin(env, `Payment received: ${money(inv.amount_cents)} from ${v && v.company}`, [`${PLAN_NAME[r.sub.plan]} plan for ${l.product_name} on ${r.sub.page}, paid by card (iyzico ${res.paymentId}).`, `Active until ${r.paid_through.slice(0, 10)}.`,
    r.sub.plan !== "basic" && !l.tool_id ? "We haven't scored this product yet, so it won't show in the top places until it's reviewed and matched to a tool on our list. Ask Claude to review and score it." :
    l.status === "approved" ? "The listing is approved, so it's live now." : "The listing is waiting for your approval. Approve it in the admin page to put it live."]);
  return back("pay=ok");
}

// ---------- monthly subscriptions through iyzico (Subscription add-on)
// One iyzico product for all placements; one monthly pricing plan per position and price, created on first use.
async function iyzicoRef(env, key, create) {
  const hit = await env.DB.prepare("SELECT ref FROM iyzico_refs WHERE key = ?").bind(key).first();
  if (hit) return hit.ref;
  const r = await create();
  const ref = r && r.status === "success" && r.data && r.data.referenceCode;
  if (!ref) throw new Error((r && r.errorMessage) || "iyzico setup failed");
  await env.DB.prepare("INSERT OR IGNORE INTO iyzico_refs (key, ref, created_at) VALUES (?,?,?)").bind(key, ref, now()).run();
  return ref;
}
async function monthlyPlanRef(env, plan, cents) {
  const cur = env.IYZICO_CURRENCY || "USD";
  const product = await iyzicoRef(env, "product", () => iyzico(env, "/v2/subscription/products", { locale: "en", name: "Vettlo category placement",
    description: "Monthly position on a Vettlo category shortlist" }));
  return iyzicoRef(env, `plan:${plan}:month:${cur}:${cents}`, () => iyzico(env, `/v2/subscription/products/${encodeURIComponent(product)}/pricing-plans`, {
    locale: "en", name: `Vettlo ${PLAN_NAME[plan]}, monthly (${money(cents)})`, price: cents / 100, currencyCode: cur,
    paymentInterval: "MONTHLY", paymentIntervalCount: 1, planPaymentType: "RECURRING" }));
}
async function startSubscriptionCheckout(env, vendor, inv, s, b, addr, origin) {
  let planRef;
  try { planRef = await monthlyPlanRef(env, s.plan, inv.amount_cents); }
  catch (e) { return json({ ok: false, error: "Monthly card payments aren't set up yet (" + e.message + "). We'll email you an invoice." }, 502); }
  const res = await iyzico(env, "/v2/subscription/checkoutform/initialize", {
    locale: "en", conversationId: String(inv.id), callbackUrl: origin + "/api/pay/sub-callback", pricingPlanReferenceCode: planRef, subscriptionInitialStatus: "ACTIVE",
    customer: { name: b.name, surname: b.surname, email: vendor.email, gsmNumber: b.phone, identityNumber: b.tax_id, billingAddress: addr, shippingAddress: addr } });
  if (res.status !== "success" || !res.token || !res.checkoutFormContent) return json({ ok: false, error: "The payment page couldn't be opened" + (res.errorMessage ? ": " + res.errorMessage : ".") }, 502);
  await env.DB.batch([
    env.DB.prepare("INSERT INTO pay_sessions (token, invoice_id, vendor_id, created_at) VALUES (?,?,?,?)").bind(res.token, inv.id, vendor.id, now()),
    env.DB.prepare("INSERT INTO pay_forms (token, invoice_id, vendor_id, html, created_at) VALUES (?,?,?,?,?)").bind(res.token, inv.id, vendor.id, res.checkoutFormContent, now()),
  ]);
  return json({ ok: true, url: origin + "/api/pay/form/" + encodeURIComponent(res.token) });
}
// The subscription checkout comes back as an embeddable script, so we serve it on a small page of our own.
async function subscriptionForm(request, env, token) {
  const vendor = await currentVendor(request, env);
  const f = vendor && (await env.DB.prepare("SELECT * FROM pay_forms WHERE token = ? AND vendor_id = ?").bind(token, vendor.id).first());
  if (!f) return Response.redirect(new URL("/vendors/app/#invoices", request.url).toString(), 302);
  const inv = await env.DB.prepare("SELECT amount_cents FROM invoices WHERE id = ?").bind(f.invoice_id).first();
  const page = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Pay monthly plan | Vettlo</title><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap" style="max-width:40rem;padding:2rem 1rem">
<p><a href="/vendors/app/#invoices">← Back to invoices</a></p><h1>Monthly plan: ${money(inv ? inv.amount_cents : 0)} per month</h1>
<p class="muted">Your card is charged now and then every month until you stop the renewal in the portal. Payments are processed by iyzico.</p>
<div id="iyzipay-checkout-form" class="responsive"></div>${f.html}</main></body></html>`;
  return new Response(page, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex",
    // iyzico's checkout form loads its own scripts, frames and styles
    "content-security-policy": "default-src 'self' https://*.iyzipay.com https://*.iyzico.com; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.iyzipay.com https://*.iyzico.com; style-src 'self' 'unsafe-inline' https://*.iyzipay.com https://*.iyzico.com https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' data: https:; frame-src https://*.iyzipay.com https://*.iyzico.com; frame-ancestors 'none'; base-uri 'self'; object-src 'none'" } });
}
// Records one successful subscription charge (first or renewal) after confirming it with iyzico. Idempotent per order.
async function recordSubscriptionOrder(env, s, orderRef) {
  const ref = "iyzico-order:" + orderRef;
  if (await env.DB.prepare("SELECT 1 FROM invoices WHERE provider_ref = ?").bind(ref).first()) return { ok: true, dup: true };
  const d = await iyzico(env, `/v2/subscription/subscriptions/${encodeURIComponent(s.provider_sub)}`, null, "GET");
  const item = d && d.status === "success" && d.data && (d.data.items || [])[0];
  const order = item && (item.orders || []).find((o) => o.referenceCode === orderRef);
  if (!order || order.orderStatus !== "SUCCESS") return { ok: false, error: "iyzico doesn't show this order as paid." };
  const cents = Math.round(Number(order.price) * 100);
  if (cents !== s.price_cents) return { ok: false, error: `Charged ${money(cents)} but the plan costs ${money(s.price_cents)}.` };
  let inv = await env.DB.prepare("SELECT * FROM invoices WHERE slot_id = ? AND status = 'requested' ORDER BY id LIMIT 1").bind(s.id).first();
  if (!inv) {
    const r = await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(s.vendor_id, s.id, cents, now(), now()).run();
    inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ?").bind(r.meta.last_row_id).first();
  }
  return activateInvoice(env, inv, ref);
}
async function subscriptionOrders(env, subRef) {
  const d = await iyzico(env, `/v2/subscription/subscriptions/${encodeURIComponent(subRef)}`, null, "GET");
  const item = d && d.status === "success" && d.data && (d.data.items || [])[0];
  return item ? item.orders || [] : [];
}
async function subscriptionCallback(request, env) {
  const back = (q) => Response.redirect(new URL("/vendors/app/?" + q + "#invoices", request.url).toString(), 303);
  const form = await request.formData().catch(() => null);
  const token = form ? String(form.get("token") || "") : "";
  const ps = token && (await env.DB.prepare("SELECT * FROM pay_sessions WHERE token = ?").bind(token).first());
  if (!ps) return back("pay=error");
  await env.DB.prepare("DELETE FROM pay_forms WHERE token = ?").bind(token).run();
  const res = await iyzico(env, `/v2/subscription/checkoutform/${encodeURIComponent(token)}`, null, "GET");
  const data = res && res.status === "success" && res.data;
  const inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ?").bind(ps.invoice_id).first();
  const s = inv && (await env.DB.prepare("SELECT * FROM subs WHERE id = ?").bind(inv.slot_id).first());
  if (!data || !data.referenceCode || !s) return back("pay=failed");
  await env.DB.prepare("UPDATE subs SET provider_sub = ?, auto_renew = 1, updated_at = ? WHERE id = ?").bind(data.referenceCode, now(), s.id).run();
  s.provider_sub = data.referenceCode;
  const paid = (await subscriptionOrders(env, data.referenceCode)).filter((o) => o.orderStatus === "SUCCESS");
  if (!paid.length) return back("pay=pending"); // the first charge is confirmed by the webhook
  const v = await env.DB.prepare("SELECT company FROM vendors WHERE id = ?").bind(s.vendor_id).first();
  for (const o of paid) {
    const r = await recordSubscriptionOrder(env, s, o.referenceCode);
    if (!r.ok) {
      await notifyAdmin(env, "Monthly plan paid, but it couldn't start", [`${v && v.company}: subscription ${data.referenceCode}, order ${o.referenceCode}: ${r.error}`, "Check it in the iyzico panel; cancel and refund if needed."]);
      return back("pay=held");
    }
  }
  await notifyAdmin(env, `Monthly plan started: ${money(s.price_cents)}/month from ${v && v.company}`, [`${PLAN_NAME[s.plan]} on ${s.page}, iyzico subscription ${data.referenceCode}. It renews every month until the vendor stops it.`]);
  return back("pay=ok");
}
// iyzico subscription notifications (set the URL https://vettlo.com/api/iyzico/webhook in the iyzico panel).
// Every event is re-checked against iyzico's API before anything changes, so a forged call can't start or extend a plan.
async function iyzicoWebhook(request, env) {
  const e = await request.json().catch(() => ({}));
  const ok = new Response("ok");
  if (!e.subscriptionReferenceCode || !e.orderReferenceCode) return ok;
  if (env.IYZICO_MERCHANT_ID && request.headers.get("x-iyz-signature-v3")) {
    const expect = await hmacHex(env.IYZICO_SECRET_KEY, [env.IYZICO_MERCHANT_ID, env.IYZICO_SECRET_KEY, e.iyziEventType, e.subscriptionReferenceCode, e.orderReferenceCode, e.customerReferenceCode].join(""));
    if (expect !== request.headers.get("x-iyz-signature-v3")) return new Response("bad signature", { status: 401 });
  }
  const s = await env.DB.prepare("SELECT * FROM subs WHERE provider_sub = ?").bind(e.subscriptionReferenceCode).first();
  if (!s) return ok;
  const v = await env.DB.prepare("SELECT company FROM vendors WHERE id = ?").bind(s.vendor_id).first();
  if (e.iyziEventType === "subscription.order.success") {
    const r = await recordSubscriptionOrder(env, s, e.orderReferenceCode);
    if (!r.ok) await notifyAdmin(env, "Monthly charge needs a manual check", [`${v && v.company}: subscription ${e.subscriptionReferenceCode}, order ${e.orderReferenceCode}: ${r.error}`]);
    else if (!r.dup) await notifyAdmin(env, `Monthly renewal paid: ${money(s.price_cents)} from ${v && v.company}`, [`${PLAN_NAME[s.plan]} on ${s.page}, live until ${String(r.paid_through).slice(0, 10)}.`]);
  } else if (e.iyziEventType === "subscription.order.failure") {
    await notifyAdmin(env, `Monthly charge failed: ${v && v.company}`, [`${PLAN_NAME[s.plan]} on ${s.page} (subscription ${e.subscriptionReferenceCode}). iyzico retries the card; the position stays live until ${String(s.paid_through).slice(0, 10)} and then lapses if nothing is paid.`]);
  }
  return ok;
}

// ---------- subscriptions through Paddle (Merchant of Record; Paddle Billing API)
// Settings (Cloudflare → Worker → Settings → Variables; API key and webhook secret as secrets):
//   PADDLE_API_KEY         Paddle → Developer tools → Authentication → API keys (permissions: products, prices, customers,
//                          transactions, subscriptions: read + write)
//   PADDLE_CLIENT_TOKEN    same page, client-side token (starts with test_ in sandbox, live_ in production)
//   PADDLE_WEBHOOK_SECRET  Paddle → Developer tools → Notifications → destination https://vettlo.com/api/paddle/webhook
//                          (events: transaction.completed, subscription.*, adjustment.*), its secret key
//   PADDLE_CHECKOUT=1      switches vendor payments to Paddle (after Paddle approves the account and vettlo.com);
//                          without it the keys only power the admin catalog sync
//   PADDLE_BASE_URL        only for the local test mock
// Paddle → Checkout → Checkout settings → Default payment link: https://vettlo.com/vendors/checkout/
// Paddle sells to the vendor; we keep only Paddle's subscription id in subs.provider_sub as "paddle:<sub_...>".
const paddleOn = (env) => !!(env.PADDLE_API_KEY && env.PADDLE_CLIENT_TOKEN && env.PADDLE_WEBHOOK_SECRET);
const paddleSandbox = (env) => !String(env.PADDLE_CLIENT_TOKEN || "").startsWith("live_");
const paddleBase = (env) => (env.PADDLE_BASE_URL || (paddleSandbox(env) ? "https://sandbox-api.paddle.com" : "https://api.paddle.com")).replace(/\/$/, "");
async function paddle(env, path, payload, method) {
  const r = await fetch(paddleBase(env) + path, { method: method || (payload ? "POST" : "GET"), body: payload ? JSON.stringify(payload) : undefined,
    headers: { authorization: "Bearer " + env.PADDLE_API_KEY, "content-type": "application/json", "paddle-version": "1" } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) return { error: (j.error && (j.error.detail || j.error.code)) || "HTTP " + r.status, status: r.status };
  return j;
}
const PERIOD_NAME = { month: "monthly", year: "yearly" };
// One Paddle product per plan, one price per plan + period + amount; created on first use and remembered.
async function paddleRef(env, key, create) {
  const hit = await env.DB.prepare("SELECT ref FROM iyzico_refs WHERE key = ?").bind(key).first();
  if (hit) return hit.ref;
  const r = await create();
  if (!r || !r.data || !r.data.id) throw new Error((r && r.error) || "Paddle setup failed");
  await env.DB.prepare("INSERT OR IGNORE INTO iyzico_refs (key, ref, created_at) VALUES (?,?,?)").bind(key, r.data.id, now()).run();
  return (await env.DB.prepare("SELECT ref FROM iyzico_refs WHERE key = ?").bind(key).first()).ref;
}
async function paddlePrice(env, plan, period, cents) {
  const tag = paddleSandbox(env) ? "sbx" : "live";
  const product = await paddleRef(env, `paddle:${tag}:product:${plan}`, () => paddle(env, "/products", {
    name: plan === "basic" ? "Vettlo Basic listing" : `Vettlo sponsored position ${PLAN_NAME[plan]}`, tax_category: "standard",
    description: plan === "basic" ? "Listed first under “Other tools to consider” on a Vettlo category shortlist." : `${PLAN_NAME[plan]} on a Vettlo category shortlist or alternatives page.` }));
  return paddleRef(env, `paddle:${tag}:price:${plan}:${period}:${cents}`, () => paddle(env, "/prices", {
    product_id: product, description: `${PLAN_NAME[plan]}, ${PERIOD_NAME[period]} (${money(cents)})`, name: PERIOD_NAME[period] === "monthly" ? "Monthly" : "Yearly",
    unit_price: { amount: String(cents), currency_code: "USD" }, billing_cycle: { interval: period, frequency: 1 }, tax_mode: "external",
    quantity: { minimum: 1, maximum: 1 } }));
}
// Admin: create every product and price in Paddle now, so the catalog matches the pricing page before review.
async function paddleSyncCatalog(env) {
  const t = priceTable(env), out = [];
  for (const plan of PLANS) for (const period of PERIODS) if (t[plan] && t[plan][period]) out.push({ plan, period, cents: t[plan][period], price_id: await paddlePrice(env, plan, period, t[plan][period]) });
  return out;
}
async function startPaddle(request, env, vendor, body) {
  const inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ? AND vendor_id = ? AND status = 'requested'").bind(Number(body.invoice_id), vendor.id).first();
  if (!inv) return json({ ok: false, error: "This invoice isn't open." }, 400);
  const s = await env.DB.prepare("SELECT s.*, l.product_name FROM subs s JOIN listings l ON l.id = s.listing_id WHERE s.id = ?").bind(inv.slot_id).first();
  if (!s || s.status === "cancelled" || (s.status === "reserved" && s.reserved_until <= now())) return json({ ok: false, error: "This reservation has lapsed. Reserve the plan again." }, 400);
  if (s.status === "active" && s.provider_sub && s.provider_sub.startsWith("paddle:") && s.auto_renew) return json({ ok: false, error: "This plan already renews automatically through Paddle." }, 400);
  let price;
  try { price = await paddlePrice(env, s.plan, s.period, inv.amount_cents); }
  catch (e) { return json({ ok: false, error: "Checkout isn't set up yet (" + e.message + "). Please contact us." }, 502); }
  const origin = new URL(request.url).origin;
  const t = await paddle(env, "/transactions", { items: [{ price_id: price, quantity: 1 }], collection_mode: "automatic",
    custom_data: { sub_id: String(s.id), invoice_id: String(inv.id), vendor_id: String(vendor.id) }, checkout: { url: origin + "/vendors/checkout/" } });
  if (!t.data || !t.data.id) return json({ ok: false, error: "The checkout couldn't be opened" + (t.error ? ": " + t.error : ".") }, 502);
  await env.DB.prepare("INSERT INTO pay_sessions (token, invoice_id, vendor_id, created_at) VALUES (?,?,?,?)").bind(t.data.id, inv.id, vendor.id, now()).run();
  return json({ ok: true, url: origin + "/vendors/checkout/?_ptxn=" + encodeURIComponent(t.data.id) });
}
// The checkout page: Paddle.js opens Paddle's checkout for the transaction in ?_ptxn=. No card data touches us.
async function paddleCheckoutPage(request, env) {
  const vendor = await currentVendor(request, env);
  const txn = new URL(request.url).searchParams.get("_ptxn") || "";
  const own = vendor && /^txn_[a-z0-9]+$/i.test(txn) && (await env.DB.prepare("SELECT 1 FROM pay_sessions WHERE token = ? AND vendor_id = ?").bind(txn, vendor.id).first());
  if (payMode(env) !== "paddle" || !own) return Response.redirect(new URL("/vendors/app/#invoices", request.url).toString(), 302);
  const nonce = randomToken().slice(0, 24);
  const cfg = JSON.stringify({ token: env.PADDLE_CLIENT_TOKEN, sandbox: paddleSandbox(env), txn, email: vendor.email }).replace(/</g, "\\u003c");
  const page = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Checkout | Vettlo</title><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap pay-card">
<p><a href="/vendors/app/#invoices">← Back to invoices</a></p><h1>Checkout</h1>
<p class="muted" id="pd-msg">Opening Paddle's secure checkout… Paddle.com is our online reseller and Merchant of Record and handles payment, tax and invoices.</p>
<noscript><p>Checkout needs JavaScript. Please enable it and reload this page.</p></noscript></main>
<script src="https://cdn.paddle.com/paddle/v2/paddle.js"></script>
<script nonce="${nonce}">(function(){var c=${cfg};if(!window.Paddle){document.getElementById("pd-msg").textContent="Paddle's checkout couldn't load. Check your connection or ad blocker and reload.";return;}
if(c.sandbox)Paddle.Environment.set("sandbox");
Paddle.Initialize({token:c.token,checkout:{settings:{displayMode:"overlay",theme:"light",locale:"en",allowLogout:false}},eventCallback:function(e){
if(e.name==="checkout.completed"){setTimeout(function(){location.href="/vendors/app/?pay=pending#invoices";},1500);}
if(e.name==="checkout.closed"){location.href="/vendors/app/#invoices";}}});
Paddle.Checkout.open({transactionId:c.txn,customer:{email:c.email}});})();</script></body></html>`;
  return new Response(page, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex",
    "content-security-policy": `default-src 'self'; script-src 'self' https://cdn.paddle.com 'nonce-${nonce}'; style-src 'self' 'unsafe-inline' https://cdn.paddle.com https://fonts.googleapis.com; font-src 'self' data: https://fonts.gstatic.com https://cdn.paddle.com; img-src 'self' data: https:; frame-src https://*.paddle.com; connect-src 'self' https://*.paddle.com; form-action 'self' https://*.paddle.com; frame-ancestors 'none'; base-uri 'none'; object-src 'none'` } });
}
const safeEq = (a, b) => { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };
// Paddle webhooks: signed with the destination's secret; replays are harmless (everything is keyed by Paddle ids).
async function paddleWebhook(request, env) {
  const raw = await request.text();
  const sig = Object.fromEntries((request.headers.get("paddle-signature") || "").split(";").map((p) => p.split("=")));
  const ts = Number(sig.ts);
  if (!paddleOn(env) || !ts || !sig.h1 || Math.abs(Date.now() / 1000 - ts) > 300) return new Response("bad signature", { status: 401 });
  const expect = await hmacHex(env.PADDLE_WEBHOOK_SECRET, ts + ":" + raw);
  const h1s = (request.headers.get("paddle-signature") || "").split(";").filter((p) => p.startsWith("h1=")).map((p) => p.slice(3));
  if (!h1s.some((h) => safeEq(h, expect))) return new Response("bad signature", { status: 401 });
  const e = JSON.parse(raw || "{}"), d = e.data || {};
  try {
    if (e.event_type === "transaction.completed") await paddleTransaction(env, d);
    else if (/^subscription\./.test(e.event_type)) await paddleSubscription(env, e.event_type, d);
    else if (/^adjustment\./.test(e.event_type)) await paddleAdjustment(env, d);
  } catch (err) {
    await notifyAdmin(env, "Paddle event needs a manual check", [`${e.event_type} ${d.id}: ${err.message}`]);
    return new Response("error", { status: 500 }); // Paddle retries
  }
  return new Response("ok");
}
async function subForPaddle(env, d) {
  if (d.subscription_id) {
    const s = await env.DB.prepare("SELECT * FROM subs WHERE provider_sub = ?").bind("paddle:" + d.subscription_id).first();
    if (s) return s;
  }
  const id = Number((d.custom_data || {}).sub_id);
  return id ? env.DB.prepare("SELECT * FROM subs WHERE id = ?").bind(id).first() : null;
}
async function paddleTransaction(env, d) {
  const ref = "paddle:" + d.id;
  if (await env.DB.prepare("SELECT 1 FROM invoices WHERE provider_ref = ?").bind(ref).first()) return; // already recorded
  const s = await subForPaddle(env, d);
  if (!s) throw new Error("no matching plan for this transaction");
  const v = await env.DB.prepare("SELECT company FROM vendors WHERE id = ?").bind(s.vendor_id).first();
  const cents = Number(((d.details || {}).totals || {}).subtotal);
  const first = !s.provider_sub;
  let inv = await env.DB.prepare("SELECT * FROM invoices WHERE slot_id = ? AND status = 'requested' ORDER BY id LIMIT 1").bind(s.id).first();
  if (!inv) {
    const r = await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(s.vendor_id, s.id, cents, now(), now()).run();
    inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ?").bind(r.meta.last_row_id).first();
  }
  if (cents !== inv.amount_cents) {
    await notifyAdmin(env, "Payment amount needs a check", [`Paddle ${d.id} (${v && v.company}): paid ${money(cents)} before tax, invoice is ${money(inv.amount_cents)}. Not applied; check it in Paddle.`]);
    return;
  }
  if (d.subscription_id) await env.DB.prepare("UPDATE subs SET provider_sub = ?, auto_renew = 1, updated_at = ? WHERE id = ?").bind("paddle:" + d.subscription_id, now(), s.id).run();
  const r = await activateInvoice(env, inv, ref);
  if (!r.ok) {
    await notifyAdmin(env, "Paid, but the plan couldn't start", [`${v && v.company} paid ${money(cents)} (Paddle ${d.id}), but: ${r.error}`, "Refund it in Paddle and cancel the subscription, or contact the vendor."]);
    return;
  }
  const l = await env.DB.prepare("SELECT product_name, status, tool_id FROM listings WHERE id = ?").bind(s.listing_id).first();
  await notifyAdmin(env, `${first ? "New subscription" : "Renewal paid"}: ${money(cents)} from ${v && v.company}`, [
    `${PLAN_NAME[s.plan]} (${PERIOD_NAME[s.period]}) for ${l.product_name} on ${s.page}, Paddle ${d.id}. Active until ${r.paid_through.slice(0, 10)}.`,
    first ? (s.plan !== "basic" && !l.tool_id ? "We haven't scored this product yet, so it won't show in the top places until it's reviewed and matched to a tool on our list. Ask Claude to review and score it."
      : l.status === "approved" ? "The listing is approved, so it's live now." : "The listing is waiting for your approval. Approve it in the admin page to put it live; the days it waits are added to the Paddle billing date.") : ""]);
}
async function paddleSubscription(env, type, d) {
  const s = await env.DB.prepare("SELECT * FROM subs WHERE provider_sub = ?").bind("paddle:" + d.id).first() || (await subForPaddle(env, { custom_data: d.custom_data }));
  if (!s) return;
  const v = await env.DB.prepare("SELECT company FROM vendors WHERE id = ?").bind(s.vendor_id).first();
  const cancelling = d.status === "canceled" || (d.scheduled_change && d.scheduled_change.action === "cancel");
  if (!s.provider_sub) await env.DB.prepare("UPDATE subs SET provider_sub = ?, updated_at = ? WHERE id = ?").bind("paddle:" + d.id, now(), s.id).run();
  if (cancelling && s.auto_renew) {
    await env.DB.prepare("UPDATE subs SET auto_renew = 0, updated_at = ? WHERE id = ?").bind(now(), s.id).run();
    await notifyAdmin(env, `Subscription cancelled: ${v && v.company}`, [`${PLAN_NAME[s.plan]} on ${s.page} won't renew. It stays live until ${String(s.paid_through).slice(0, 10)}.`]);
  } else if (!cancelling && d.status === "active" && !s.auto_renew && s.status === "active") {
    await env.DB.prepare("UPDATE subs SET auto_renew = 1, updated_at = ? WHERE id = ?").bind(now(), s.id).run();
  }
  if (d.status === "past_due") await notifyAdmin(env, `Renewal payment failed: ${v && v.company}`, [`${PLAN_NAME[s.plan]} on ${s.page}. Paddle retries the card and emails the vendor. The position stays live until ${String(s.paid_through).slice(0, 10)}.`]);
}
async function paddleAdjustment(env, d) {
  if (d.action !== "refund" || d.status !== "approved") return;
  const inv = await env.DB.prepare("SELECT * FROM invoices WHERE provider_ref = ?").bind("paddle:" + d.transaction_id).first();
  const s = inv && (await env.DB.prepare("SELECT * FROM subs WHERE id = ?").bind(inv.slot_id).first());
  const v = s && (await env.DB.prepare("SELECT company FROM vendors WHERE id = ?").bind(s.vendor_id).first());
  const full = d.type === "full" || (inv && Number(((d.totals || {}).subtotal)) >= inv.amount_cents);
  if (inv && full) await env.DB.prepare("UPDATE invoices SET status = 'refunded', updated_at = ? WHERE id = ? AND status = 'paid'").bind(now(), inv.id).run();
  await notifyAdmin(env, `Refund ${full ? "issued" : "(partial) issued"}: ${v ? v.company : "unknown vendor"}`, [
    `Paddle transaction ${d.transaction_id}${s ? `, ${PLAN_NAME[s.plan]} on ${s.page}` : ""}.`,
    full && s ? "End the plan in the admin page (End) so the position frees up; that also cancels the Paddle subscription." : ""]);
}
// Stop renewal at the end of the paid period (vendor), or end it now (admin).
async function paddleCancel(env, s, when) {
  const id = String(s.provider_sub || "").replace(/^paddle:/, "");
  const r = await paddle(env, `/subscriptions/${encodeURIComponent(id)}/cancel`, { effective_from: when });
  if (r.error && !/canceled|cancelled|not_active|already/i.test(r.error)) return { ok: false, error: r.error };
  await env.DB.prepare("UPDATE subs SET auto_renew = 0, updated_at = ? WHERE id = ?").bind(now(), s.id).run();
  return { ok: true };
}
// After our review: move the Paddle billing date to the new paid_through, so review days aren't billed.
async function paddleAlignBilling(env, s) {
  if (!paddleOn(env) || !s.provider_sub || !s.provider_sub.startsWith("paddle:") || !s.auto_renew) return;
  const id = s.provider_sub.slice(7);
  const r = await paddle(env, `/subscriptions/${encodeURIComponent(id)}`, { next_billed_at: s.paid_through, proration_billing_mode: "do_not_bill" }, "PATCH");
  if (r.error) await notifyAdmin(env, "Paddle billing date not moved", [`Subscription ${id} (${PLAN_NAME[s.plan]} on ${s.page}): set its next billing date to ${s.paid_through.slice(0, 10)} in Paddle by hand. Error: ${r.error}`]);
}

// ---------- admin-led sales: orders entered by the admin, invoices paid outside the site (Payoneer payment requests)
const PERIOD_WORD = { month: "monthly", year: "yearly" };
// Service emails to vendors (Brevo). Sent from vendors@vettlo.com when Brevo accepts it, otherwise from MAIL_FROM.
async function mailVendor(env, to, subject, text) {
  if (!env.BREVO_API_KEY || !to) return false;
  for (const from of [env.VENDOR_MAIL_FROM || "vendors@vettlo.com", env.MAIL_FROM || "editor@vettlo.com"]) {
    try {
      const r = await fetch("https://api.brevo.com/v3/smtp/email", { method: "POST",
        headers: { "api-key": env.BREVO_API_KEY, "content-type": "application/json", accept: "application/json" },
        body: JSON.stringify({ sender: { name: "Vettlo", email: from }, replyTo: { email: "vendors@vettlo.com", name: "Vettlo" }, to: [{ email: to }], subject, textContent: text }) });
      if (r.ok) return true;
    } catch (e) { /* try the next sender */ }
  }
  return false;
}
const pageLabel = (pg) => (pg && (pg.title || pg.url)) || "";
async function adminCreateOrder(request, env, b) {
  const email = oneLine(b.email, 200).toLowerCase();
  const company = oneLine(b.company, 120);
  const product = oneLine(b.product_name, 120);
  const site = toUrl(b.product_website);
  if (!isEmail(email)) return json({ ok: false, error: "Enter the vendor's email address." }, 400);
  if (!company || !product) return json({ ok: false, error: "Enter the company and product name." }, 400);
  if (!site) return json({ ok: false, error: "Enter the product's website, e.g. example.com." }, 400);
  const pg = (await pageIndex(env, request)).get(String(b.page || ""));
  if (!pg) return json({ ok: false, error: "Choose a page." }, 400);
  const plan = PLANS.includes(b.plan) ? b.plan : null;
  const period = plan === "basic" ? "year" : PERIODS.includes(b.period) ? b.period : null;
  if (!plan || !period) return json({ ok: false, error: "Choose a position and billing period." }, 400);
  if (plan === "basic" && pg.kind !== "shortlist") return json({ ok: false, error: "Basic listings are only on category shortlists." }, 400);
  const tool = oneLine(b.tool_id, 60) || null;
  if (tool && pg.exclude && tool === pg.exclude) return json({ ok: false, error: "A product can't take a position on its own alternatives page." }, 400);
  const custom = Math.round(Number(b.price) * 100);
  const amount = custom > 0 ? custom : priceOf(env, plan, period);
  if (!amount) return json({ ok: false, error: "No price for this plan." }, 400);
  // vendor and listing (reused when they already exist)
  let v = await env.DB.prepare("SELECT * FROM vendors WHERE email = ?").bind(email).first();
  if (!v) {
    await env.DB.prepare("INSERT INTO vendors (email, company, website, created_at, status) VALUES (?,?,?,?, 'active')").bind(email, company, site, now()).run();
    v = await env.DB.prepare("SELECT * FROM vendors WHERE email = ?").bind(email).first();
  } else if (!v.company) await env.DB.prepare("UPDATE vendors SET company = ? WHERE id = ?").bind(company, v.id).run();
  let l = await env.DB.prepare("SELECT * FROM listings WHERE vendor_id = ? AND category = ? AND lower(product_name) = lower(?)").bind(v.id, pg.category, product).first();
  if (!l) {
    const st = tool || plan === "basic" ? "approved" : "pending";
    await env.DB.prepare(`INSERT INTO listings (vendor_id, product_name, website, landing_url, category, tool_id, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?)`)
      .bind(v.id, product, site, site, pg.category, tool, st, now(), now()).run();
    l = await env.DB.prepare("SELECT * FROM listings WHERE vendor_id = ? AND category = ? AND lower(product_name) = lower(?)").bind(v.id, pg.category, product).first();
  } else if (tool && (l.tool_id !== tool || l.status !== "approved")) {
    await env.DB.prepare("UPDATE listings SET tool_id = ?, status = 'approved', updated_at = ? WHERE id = ?").bind(tool, now(), l.id).run();
    l = { ...l, tool_id: tool, status: "approved" };
  }
  if (await env.DB.prepare(`SELECT 1 FROM subs WHERE listing_id = ?2 AND page = ?3 AND ${LIVE}`).bind(now(), l.id, pg.url).first())
    return json({ ok: false, error: "This product already has a position on this page." }, 400);
  const stt = (await planState(env, pg, v.id)).find((x) => x.plan === plan);
  if (!stt || !["available", "priority_other"].includes(stt.state)) return json({ ok: false, error: `${PLAN_NAME[plan]} on this page is taken.` }, 409);
  const hold = Math.min(30, Math.max(1, Number(b.hold_days) || 14));
  const r = await env.DB.prepare("INSERT INTO subs (vendor_id, listing_id, category, page, plan, period, status, price_cents, reserved_until, created_at, updated_at) VALUES (?,?,?,?,?,?, 'reserved', ?,?,?,?)")
    .bind(v.id, l.id, l.category, pg.url, plan, period, amount, new Date(Date.now() + hold * 864e5).toISOString(), now(), now()).run();
  const subId = r.meta.last_row_id;
  const occ = await occupants(env, pg.url, plan);
  if (occ.findIndex((o) => o.id === subId) >= CAPACITY[plan]) { await env.DB.prepare("UPDATE subs SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), subId).run(); return json({ ok: false, error: "That position was just taken." }, 409); }
  const ir = await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(v.id, subId, amount, now(), now()).run();
  const inv = await env.DB.prepare("SELECT * FROM invoices WHERE id = ?").bind(ir.meta.last_row_id).first();
  let activated = null;
  if (b.paid) {
    activated = await activateInvoice(env, inv, oneLine(b.ref, 120) || "payoneer");
    if (!activated.ok) return json({ ok: false, error: activated.error }, 409);
  }
  let mailed = false;
  if (b.notify) {
    const live = liveReady(l, plan);
    mailed = await mailVendor(env, email, `Your Vettlo order: ${PLAN_NAME[plan]} on ${pageLabel(pg)}`,
      `Hi,\n\nThank you for your order. Here are the details:\n\nProduct: ${product}\nPage: ${pageLabel(pg)} (https://vettlo.com${pg.url})\nPosition: ${PLAN_NAME[plan]}\nBilling: ${PERIOD_WORD[period]}, ${money(amount)}\n\n`
      + (b.paid ? "We've received your payment. " : `You'll receive a payment request from Payoneer for ${money(amount)} shortly. You can pay it by card or bank transfer. `)
      + (live ? "Your product goes live at this position as soon as the payment is confirmed.\n\n" : "We're researching your product and writing its review. Your paid time starts the day it goes live, so the review days don't count against your plan.\n\n")
      + `You can sign in at https://vettlo.com/vendors/login/ with this email address to see your listing and its traffic.\n\nTerms: https://vettlo.com/advertiser-terms/\n\nLet me know if you have any questions.\n\nVettlo Vendor Relations`);
  }
  await clearPlacements();
  return json({ ok: true, sub_id: subId, invoice_id: inv.id, amount_cents: amount, paid: !!b.paid, paid_through: activated && activated.paid_through, mailed, listing_status: l.status });
}

// Daily billing job (Worker cron): opens renewal invoices 7 days before a plan ends, reminds the vendor the day before,
// and tells the admin what to send through Payoneer. Plans that renew through a card provider are skipped.
export async function billingDaily(env) {
  if (!env.DB) return { renewals: 0 };
  await migrate(env);
  const t = now(), week = new Date(Date.now() + 7 * 864e5).toISOString(), day = new Date(Date.now() + 1.5 * 864e5).toISOString();
  const lines = { renew: [], remind: [], lapsed: [] };
  const mark = async (s, kind) => (await env.DB.prepare("INSERT OR IGNORE INTO notices (sub_id, kind, period_end, created_at) VALUES (?,?,?,?)").bind(s.id, kind, s.paid_through, t).run()).meta.changes > 0;
  const base = `SELECT s.*, l.product_name, v.email, v.company FROM subs s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
    WHERE s.status = 'active' AND s.auto_renew = 0 AND s.held_since IS NULL AND v.status = 'active'`;
  for (const s of (await env.DB.prepare(base + " AND s.paid_through > ? AND s.paid_through <= ?").bind(t, week).all()).results) {
    if (!(await mark(s, "renewal"))) continue;
    let inv = await env.DB.prepare("SELECT * FROM invoices WHERE slot_id = ? AND status = 'requested' ORDER BY id LIMIT 1").bind(s.id).first();
    if (!inv) {
      await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(s.vendor_id, s.id, s.price_cents, t, t).run();
      inv = { amount_cents: s.price_cents };
    }
    lines.renew.push(`• ${s.company} <${s.email}>: ${money(inv.amount_cents)} for ${PLAN_NAME[s.plan]} (${PERIOD_WORD[s.period]}) on ${s.page}, ${s.product_name}. Ends ${s.paid_through.slice(0, 10)}.`);
    await mailVendor(env, s.email, `Your Vettlo plan renews on ${s.paid_through.slice(0, 10)}`,
      `Hi,\n\nYour ${PLAN_NAME[s.plan]} for ${s.product_name} on https://vettlo.com${s.page} ends on ${s.paid_through.slice(0, 10)}.\n\nTo keep it, pay the ${PERIOD_WORD[s.period]} renewal of ${money(inv.amount_cents)}. You'll receive a payment request from Payoneer in the next day or two; you can pay it by card or bank transfer.\n\nIf you'd rather not renew, just reply and let us know. The position then ends on that date and opens up for other vendors.\n\nLet me know if you have any questions.\n\nVettlo Vendor Relations`);
  }
  for (const s of (await env.DB.prepare(base + " AND s.paid_through > ? AND s.paid_through <= ? AND EXISTS (SELECT 1 FROM invoices i WHERE i.slot_id = s.id AND i.status = 'requested')").bind(t, day).all()).results) {
    if (!(await mark(s, "reminder"))) continue;
    lines.remind.push(`• ${s.company} <${s.email}>: ${PLAN_NAME[s.plan]} on ${s.page} ends ${s.paid_through.slice(0, 10)}, renewal still unpaid.`);
    await mailVendor(env, s.email, `Reminder: your Vettlo position ends ${s.paid_through.slice(0, 10)}`,
      `Hi,\n\nA quick reminder: your ${PLAN_NAME[s.plan]} for ${s.product_name} on https://vettlo.com${s.page} ends on ${s.paid_through.slice(0, 10)} and the renewal hasn't been paid yet. You can pay it through the Payoneer payment request we sent.\n\nLet me know if you have any questions.\n\nVettlo Vendor Relations`);
  }
  for (const s of (await env.DB.prepare(base + " AND s.paid_through <= ? AND s.paid_through > ?").bind(t, new Date(Date.now() - 3 * 864e5).toISOString()).all()).results) {
    if (!(await mark(s, "lapsed"))) continue;
    lines.lapsed.push(`• ${s.company}: ${PLAN_NAME[s.plan]} on ${s.page} ended ${s.paid_through.slice(0, 10)} unpaid and was taken off the page. A late payment still restarts it if the position is free.`);
  }
  if (lines.renew.length || lines.remind.length || lines.lapsed.length) {
    await clearPlacements();
    await notifyAdmin(env, `Billing: ${lines.renew.length} renewal${lines.renew.length === 1 ? "" : "s"} to send`, [
      lines.renew.length ? "Send a Payoneer payment request (Get Paid → Request a payment) to each, then mark the invoice paid in the admin page when it arrives:\n" + lines.renew.join("\n") : "",
      lines.remind.length ? "\nUnpaid, ending tomorrow (the vendor got a reminder):\n" + lines.remind.join("\n") : "",
      lines.lapsed.length ? "\nEnded unpaid:\n" + lines.lapsed.join("\n") : ""]);
  }
  return { renewals: lines.renew.length, reminders: lines.remind.length, lapsed: lines.lapsed.length };
}

// ---------- click tracking (reporting only; positions are billed monthly, not per click)
export async function handleCheckoutPage(request, env) {
  if (!env.DB) return Response.redirect(new URL("/vendors/app/", request.url).toString(), 302);
  await migrate(env);
  return paddleCheckoutPage(request, env);
}

export async function handleGo(request, env, ctx) {
  if (!env.DB) return Response.redirect(new URL("/", request.url).toString(), 302);
  await migrate(env);
  const url = new URL(request.url);
  const id = Number(url.pathname.split("/")[2]);
  // Only approved, active listings of active vendors redirect, so /go/ links can't be used to bounce visitors to unreviewed URLs.
  const l = await env.DB.prepare("SELECT l.* FROM listings l JOIN vendors v ON v.id = l.vendor_id WHERE l.id = ? AND l.status = 'approved' AND l.active = 1 AND v.status = 'active'").bind(id).first();
  if (!l || !isUrl(l.landing_url) || new URL(l.landing_url).protocol !== "https:") return Response.redirect(new URL("/", request.url).toString(), 302);
  const ua = request.headers.get("user-agent") || "";
  const ip = request.headers.get("cf-connecting-ip") || "";
  const day = new Date().toISOString().slice(0, 10);
  const ipHash = await sha256(`${ip}|${day}|${env.CLICK_SALT || "vettlo"}`);
  const category = oneLine(url.searchParams.get("c"), 120) || l.category;
  const page = oneLine(url.searchParams.get("p"), 300);
  ctx.waitUntil((async () => {
    let unique = 0, reason = "";
    if (!ua || BOT_UA.test(ua)) reason = "bot";
    else {
      const dup = await env.DB.prepare("SELECT 1 FROM clicks WHERE listing_id = ? AND ip_hash = ? AND ts >= ? LIMIT 1").bind(l.id, ipHash, new Date(Date.now() - 864e5).toISOString()).first();
      if (dup) reason = "duplicate"; else unique = 1;
    }
    // "billable" now means "counted": a unique human visit within 24 hours.
    await env.DB.prepare("INSERT INTO clicks (listing_id, vendor_id, category, page, ts, ip_hash, billable, cost_cents, reason) VALUES (?,?,?,?,?,?,?,0,?)")
      .bind(l.id, l.vendor_id, category, page, now(), ipHash, unique, reason || null).run();
  })());
  return new Response(null, { status: 302, headers: { location: new URL(l.landing_url).toString(), "cache-control": "no-store", "referrer-policy": "origin", "x-robots-tag": "noindex" } });
}

// ---------- API router
export async function handlePortalApi(request, env, path) {
  if (!env.DB) return json({ ok: false, error: "The vendor portal isn't connected to its database yet." }, 503);
  await migrate(env);
  if (path === "/api/pay/callback" && request.method === "POST") return cardCallback(request, env); // posted by the iyzico form
  if (path === "/api/pay/sub-callback" && request.method === "POST") return subscriptionCallback(request, env); // posted by the iyzico subscription form
  if (path === "/api/iyzico/webhook" && request.method === "POST") return iyzicoWebhook(request, env);
  if (path === "/api/paddle/webhook" && request.method === "POST") return paddleWebhook(request, env); // Paddle notifications
  const pf = path.match(/^\/api\/pay\/form\/([^/]+)$/);
  if (pf && request.method === "GET") return subscriptionForm(request, env, decodeURIComponent(pf[1]));
  if (request.method !== "GET" && request.headers.get("x-requested-with") !== "vettlo") return json({ ok: false, error: "Bad request." }, 400);
  if (path === "/api/auth/request" && request.method === "POST") return requestLogin(request, env, await request.json().catch(() => ({})));
  if (path === "/api/auth/verify" && request.method === "GET") return verifyLogin(request, env);
  if (path === "/api/categories") return json({ ok: true, categories: await categories(env, request) });
  const vendor = await currentVendor(request, env);
  if (!vendor) return json({ ok: false, error: "Please sign in.", auth: true }, 401);
  if (path.startsWith("/api/admin/")) return adminApi(request, env, vendor, path);
  return (await vendorApi(request, env, vendor, path)) || json({ ok: false, error: "Not found." }, 404);
}

// ---------- placement on category shortlists
const placementCache = new Map();
// Sponsor placements for every category, cached in memory (per isolate) and in the colo's edge cache (shared),
// so public shortlist pages don't wait on the database. Admin and billing changes call clearPlacements().
const SPONSOR_KEY = "https://vettlo.com/__cache/sponsors-v2";
async function allSponsors(env) {
  const hit = placementCache.get("*");
  if (hit && hit.t > Date.now() - 60e3) return hit.v;
  let v = null;
  try { const c = await caches.default.match(SPONSOR_KEY); if (c) v = await c.json(); } catch {}
  if (!v) {
    const rows = (await env.DB.prepare(`SELECT l.*, s.plan, COALESCE(s.page, '/tools/' || s.category || '/') AS sub_page FROM subs s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
      WHERE s.status = 'active' AND s.paid_through > ? AND l.status = 'approved' AND l.active = 1 AND v.status = 'active'
      ORDER BY s.started_at ASC, s.id ASC`).bind(now()).all()).results;
    v = {};
    for (const r of rows) (v[r.sub_page] ||= []).push(r);
    try { await caches.default.put(SPONSOR_KEY, new Response(JSON.stringify(v), { headers: { "content-type": "application/json", "cache-control": "public, max-age=300" } })); } catch {}
  }
  placementCache.set("*", { t: Date.now(), v });
  return v;
}
async function clearPlacements() {
  placementCache.clear();
  try { await caches.default.delete(SPONSOR_KEY); } catch {}
}
async function sponsors(env, pagePath) {
  const rows = (await allSponsors(env))[pagePath] || [];
  // p1..p10 take that place on the shortlist (one vendor each); basic goes to the top of "Other tools to consider".
  // Positions show only once we've scored the product (it maps to a tool on our list), so every ranked card looks and reads the same.
  const out = [], taken = new Set();
  for (const r of rows) {
    const pos = posOf(r.plan);
    if (pos && r.tool_id && !taken.has(pos)) { taken.add(pos); out.push({ ...r, position: pos }); }
  }
  return [...out.sort((a, b) => a.position - b.position), ...rows.filter((r) => r.plan === "basic").map((r) => ({ ...r, position: 0 }))];
}

const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return ""; } };
function partnerLi(l, catSlug, path) {
  return `<li><span class="rank">0</span><span><a class="nm" href="#partner-${l.id}"><img class="tlogo tlogo-24" src="https://www.google.com/s2/favicons?domain=${esc(hostOf(l.website))}&amp;sz=64" alt="" width="24" height="24" loading="lazy">${esc(l.product_name)}</a><br><span class="bf">${esc(l.best_for || "")}</span></span><span class="sc muted small">Not scored</span><a class="btn ghost small" href="/go/${l.id}?c=${esc(catSlug)}&amp;p=${encodeURIComponent(path)}" rel="sponsored nofollow noopener" target="_blank">Visit</a></li>`;
}
function partnerCard(l, catSlug, path) {
  return `<article class="tool" id="partner-${l.id}"><div class="tool-head"><span class="num">0</span><div><h3><img class="tlogo tlogo-40" src="https://www.google.com/s2/favicons?domain=${esc(hostOf(l.website))}&amp;sz=128" alt="" width="40" height="40" loading="lazy">${esc(l.product_name)}</h3><div class="bestfor">${esc(l.best_for || "")}</div></div>
<a class="btn small" href="/go/${l.id}?c=${esc(catSlug)}&amp;p=${encodeURIComponent(path)}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
<div class="tool-body">${l.description ? `<p>${esc(l.description)}</p>` : ""}${l.starting_price ? `<p><b>Starting price:</b> ${esc(l.starting_price)} (as provided by the vendor)</p>` : ""}<p class="small muted">We haven't scored this product yet.</p></div></article>`;
}
// Put each sponsor at its bought position (1-based); editorial items keep their order and fill the gaps.
function arrange(items, partners, find, make) {
  const placed = [];
  for (const p of partners) {
    const idx = p.tool_id ? items.findIndex((x) => find(x, p)) : -1;
    const el = idx >= 0 ? items.splice(idx, 1)[0] : make ? make(p) : null;
    if (el) placed.push({ pos: p.position, el });
  }
  const out = [...items];
  for (const { pos, el } of placed.sort((a, b) => a.pos - b.pos)) out.splice(Math.min(pos - 1, out.length), 0, el);
  return out;
}

export async function placeOnShortlist(request, env, response, ctx) {
  const url = new URL(request.url);
  const m = url.pathname.match(/^\/tools\/(best-[a-z0-9-]+)\/$/);
  if (!m || !env.DB || response.status !== 200 || !(response.headers.get("content-type") || "").includes("text/html")) return response;
  const slug = m[1];
  let partners;
  try { partners = await sponsors(env, url.pathname); } catch { return response; }  // no schema setup on the public path: tables exist once the portal has run
  if (!partners.length) return response;
  let html = await response.text();
  const path = url.pathname;
  const basic = partners.filter((p) => p.position === 0);
  partners = partners.filter((p) => p.position > 0);
  if (basic.length) {
    const lis = basic.map((p) => `<li><b><a href="/go/${p.id}?c=${esc(slug)}&amp;p=${encodeURIComponent(path)}" rel="sponsored nofollow noopener" target="_blank">${esc(p.product_name)}</a></b>: ${esc(p.best_for || p.description || "")}</li>`).join("");
    if (/<section id="others"[^>]*>[\s\S]*?<ol[^>]*>/.test(html)) {
      html = html.replace(/(<section id="others"[^>]*>[\s\S]*?<ol)( start="\d+")?([^>]*>)/, (all, a, st, z) => a + (st || "") + z + lis);
    } else {
      html = html.replace(/<section id="criteria"/, `<section id="others" class="prose"><h2>Other tools to consider</h2><p>These tools aren't on our ranked shortlist and we haven't scored them.</p><ol>${lis}</ol></section>\n<section id="criteria"`);
    }
  }

  html = html.replace(/(<ol class="shortlist">)([\s\S]*?)(<\/ol>)/, (all, a, inner, z) => {
    const items = inner.match(/<li>[\s\S]*?<\/li>/g) || [];
    const out = arrange(items, partners, (li, p) => li.includes(`href="#${p.tool_id}"`), (p) => partnerLi(p, slug, path));
    return a + out.map((li, i) => li.replace(/<span class="rank">\d+<\/span>/, `<span class="rank">${i + 1}</span>`)).join("") + z;
  });
  html = html.replace(/(<section id="reviews"><h2>[^<]*<\/h2>)([\s\S]*?)(<\/section>)/, (all, a, inner, z) => {
    const cards = inner.match(/<article class="tool"[\s\S]*?<\/article>/g) || [];
    const out = arrange(cards, partners, (c, p) => c.startsWith(`<article class="tool" id="${p.tool_id}"`), (p) => partnerCard(p, slug, path));
    return a + out.map((c, i) => c.replace(/<span class="num">\d+<\/span>/, `<span class="num">${i + 1}</span>`)).join("\n") + z;
  });
  html = html.replace(/(<section id="compare">[\s\S]*?<tbody>)([\s\S]*?)(<\/tbody>)/, (all, a, inner, z) => {
    const rows = inner.match(/<tr>[\s\S]*?<\/tr>/g) || [];
    const out = arrange(rows, partners, (r, p) => r.includes(`href="#${p.tool_id}"`), null);
    return a + out.map((r, i) => r.replace(/<td class="num">\d+<\/td>/, `<td class="num">${i + 1}</td>`)).join("") + z;
  });
  for (const p of partners) {
    if (!p.tool_id) continue;
    html = html.replace(new RegExp(`(<article class="tool" id="${p.tool_id}">[\\s\\S]*?<a class="btn small" href=")[^"]+(")`), `$1/go/${p.id}?c=${slug}&amp;p=${encodeURIComponent(path)}$2`);
  }
  // Count a daily impression per sponsor for vendor reports (humans only).
  const ua = request.headers.get("user-agent") || "";
  if (ctx && ua && !BOT_UA.test(ua) && request.method === "GET") {
    const day = new Date().toISOString().slice(0, 10);
    ctx.waitUntil(env.DB.batch(partners.map((p) => env.DB.prepare("INSERT INTO impressions (listing_id, day, n) VALUES (?, ?, 1) ON CONFLICT(listing_id, day) DO UPDATE SET n = n + 1").bind(p.id, day))).catch(() => {}));
  }
  const headers = new Headers(response.headers);
  headers.delete("content-length");
  headers.set("cache-control", "public, max-age=0, must-revalidate");
  return new Response(html, { status: 200, headers });
}
