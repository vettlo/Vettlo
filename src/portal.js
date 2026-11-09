// Vettlo vendor portal: magic-link login, listings, annual plans (Basic / Pro / Premium) that place a product
// on its category shortlist, with invoices, renewals and waitlists, plus click and impression reporting. Data lives in the D1 database bound as DB.

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
  `CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, kind TEXT NOT NULL,
     status TEXT NOT NULL, note TEXT, provider_ref TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)`,
];
async function migrate(env) {
  if (migrated) return;
  await env.DB.batch(SCHEMA.map((s) => env.DB.prepare(s)));
  migrated = true;
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
  row.is_admin = !!(env.FORM_TO && row.email.toLowerCase() === env.FORM_TO.toLowerCase()) || (env.ADMIN_EMAILS || "").toLowerCase().split(",").map((s) => s.trim()).includes(row.email.toLowerCase());
  return row;
}

async function requestLogin(request, env, data) {
  const email = oneLine(data.email, 200).toLowerCase();
  if (!isEmail(email)) return json({ ok: false, error: "Enter a valid work email." }, 400);
  if (clean(data.website_hp, 100)) return json({ ok: true }); // honeypot
  let vendor = await env.DB.prepare("SELECT * FROM vendors WHERE email = ?").bind(email).first();
  if (!vendor) {
    const company = oneLine(data.company, 120), website = oneLine(data.website, 300);
    if (!data.signup) return json({ ok: false, error: "No account for this email yet. Create one below.", needs_signup: true }, 404);
    if (!company || !isUrl(website)) return json({ ok: false, error: "Add your company name and website (https://…)." }, 400);
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
  const vendor = await env.DB.prepare("SELECT id FROM vendors WHERE email = ?").bind(row.email).first();
  const sess = randomToken();
  await env.DB.prepare("INSERT INTO sessions (hash, vendor_id, expires_at) VALUES (?, ?, ?)")
    .bind(await sha256(sess), vendor.id, new Date(Date.now() + SESSION_DAYS * 864e5).toISOString()).run();
  return new Response(null, { status: 302, headers: {
    location: "/vendors/app/",
    "set-cookie": `vs=${sess}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}`,
  } });
}

// ---------- plans: annual packages per category
// basic: listed first under "Other tools to consider", unlimited seats
// pro: 2nd or 3rd place on the shortlist, 2 seats per category (earlier subscribers rank higher)
// premium: 1st place on the shortlist, 1 seat per category
const PLANS = ["basic", "pro", "premium"];
const CAPACITY = { basic: Infinity, pro: 2, premium: 1 };
const PLAN_NAME = { basic: "Basic", pro: "Pro", premium: "Premium" };
const RESERVE_DAYS = 7;       // an unpaid reservation holds a seat this long
const WAITLIST_HOURS = 72;    // when a seat frees up, the first vendor on its waitlist gets it first for this long
const DEFAULT_PRICES = { basic: 5000, pro: 9900, premium: 14900 }; // cents per year
function prices(env) {
  const p = (env.PLAN_PRICES || "").split(",").map((x) => Number(x.trim()));
  return p.length === 3 && p.every((x) => x > 0) ? { basic: p[0], pro: p[1], premium: p[2] } : DEFAULT_PRICES;
}
const addYear = (iso) => { const d = new Date(iso); const day = d.getUTCDate(); d.setUTCFullYear(d.getUTCFullYear() + 1); if (d.getUTCDate() < day) d.setUTCDate(0); return d.toISOString(); };
const later = (a, b) => (!a ? b : !b ? a : a > b ? a : b);
const LIVE = "((status = 'active' AND paid_through > ?1) OR (status = 'reserved' AND reserved_until > ?1))";

async function occupants(env, category, plan) {
  return (await env.DB.prepare(`SELECT * FROM subs WHERE category = ?2 AND plan = ?3 AND ${LIVE} ORDER BY id ASC`).bind(now(), category, plan).all()).results;
}
async function freedAt(env, category, plan) {
  const r = await env.DB.prepare(`SELECT MAX(t) AS t FROM (SELECT CASE WHEN status = 'cancelled' THEN updated_at WHEN paid_through IS NOT NULL THEN paid_through ELSE reserved_until END AS t
    FROM subs WHERE category = ? AND plan = ?) WHERE t <= ?`).bind(category, plan, now()).first();
  return r && r.t;
}
async function planState(env, category, vendorId) {
  const P = prices(env), out = [];
  for (const plan of PLANS) {
    const occ = await occupants(env, category, plan);
    const wl = plan === "basic" ? [] : (await env.DB.prepare("SELECT vendor_id FROM plan_waitlist WHERE category = ? AND plan = ? ORDER BY created_at ASC, id ASC").bind(category, plan).all()).results;
    const st = { plan, name: PLAN_NAME[plan], price_cents: P[plan], capacity: CAPACITY[plan] === Infinity ? null : CAPACITY[plan], used: occ.length, waitlist: wl.length, on_waitlist: wl.some((w) => w.vendor_id === vendorId) };
    const mine = occ.find((o) => o.vendor_id === vendorId);
    if (mine) { st.state = mine.status === "active" ? "yours" : "reserved_by_you"; st.until = mine.status === "active" ? mine.paid_through : mine.reserved_until; st.sub_id = mine.id; }
    else if (occ.length >= CAPACITY[plan]) { st.state = "full"; st.until = occ.map((o) => (o.status === "active" ? o.paid_through : o.reserved_until)).sort()[0]; }
    else {
      const f = wl.length ? await freedAt(env, category, plan) : null;
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
      payments: payMode(env) });
  }
  if (path === "/api/me" && method === "PUT") {
    const company = oneLine(body.company, 120) || vendor.company;
    const website = isUrl(body.website) ? oneLine(body.website, 300) : vendor.website;
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
      const s = await env.DB.prepare(`SELECT * FROM subs WHERE listing_id = ?2 AND ${LIVE} ORDER BY id DESC LIMIT 1`).bind(now(), l.id).first();
      Object.assign(l, { clicks_30d: c.n, impressions_30d: im.n, sub: s || null });
    }
    return json({ ok: true, listings: rows });
  }
  if (path === "/api/listings" && method === "POST") {
    const cats = await categories(env, request);
    const cat = cats.find((c) => c.slug === body.category);
    const f = { product_name: oneLine(body.product_name, 80), website: oneLine(body.website, 300), landing_url: oneLine(body.landing_url || body.website, 500),
      best_for: oneLine(body.best_for, 90), description: clean(body.description, 600), starting_price: oneLine(body.starting_price, 80) };
    if (!f.product_name || !isUrl(f.website) || !isUrl(f.landing_url)) return json({ ok: false, error: "Add the product name, website and landing page (https://…)." }, 400);
    if (!cat) return json({ ok: false, error: "Choose a category." }, 400);
    const tool = (cat.tools || []).find((t) => t.name.toLowerCase() === f.product_name.toLowerCase());
    const r = await env.DB.prepare(`INSERT INTO listings (vendor_id, product_name, website, landing_url, category, tool_id, best_for, description, starting_price, created_at, updated_at)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)`).bind(vendor.id, f.product_name, f.website, f.landing_url, cat.slug, tool ? tool.id : null, f.best_for, f.description, f.starting_price, now(), now()).run();
    await notifyAdmin(env, `Listing to review: ${f.product_name}`, [`${vendor.company} submitted ${f.product_name} for ${cat.name}.`, `Website: ${f.website}`, `Best for: ${f.best_for}`, `Description: ${f.description}`]);
    return json({ ok: true, id: r.meta.last_row_id });
  }
  let m = path.match(/^\/api\/listings\/(\d+)$/);
  if (m && method === "PUT") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(m[1]), vendor.id).first();
    if (!l) return json({ ok: false, error: "Not found." }, 404);
    const active = body.active !== undefined ? (body.active ? 1 : 0) : l.active;
    const landing = body.landing_url !== undefined && isUrl(body.landing_url) ? oneLine(body.landing_url, 500) : l.landing_url;
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
  if (path === "/api/plans" && method === "GET") {
    const cat = new URL(request.url).searchParams.get("category") || "";
    return json({ ok: true, category: cat, plans: await planState(env, cat, vendor.id) });
  }
  if (path === "/api/subscribe" && method === "POST") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(body.listing_id), vendor.id).first();
    const plan = PLANS.includes(body.plan) ? body.plan : null;
    if (!l) return json({ ok: false, error: "Choose one of your listings." }, 400);
    if (!plan) return json({ ok: false, error: "Choose a plan." }, 400);
    if (l.status === "rejected") return json({ ok: false, error: "This listing wasn't approved. Edit it and resubmit first." }, 400);
    const own = await env.DB.prepare(`SELECT 1 FROM subs WHERE listing_id = ?2 AND ${LIVE}`).bind(now(), l.id).first();
    if (own) return json({ ok: false, error: "This listing already has a plan. To change plans, contact us." }, 400);
    const st = (await planState(env, l.category, vendor.id)).find((x) => x.plan === plan);
    if (st.state !== "available") return json({ ok: false, error: st.state === "priority_other" ? "A vendor on the waitlist has first claim on this plan until " + st.until.slice(0, 10) + "." : "This plan is full in this category. Join the waitlist to get the next seat." }, 409);
    const r = await env.DB.prepare("INSERT INTO subs (vendor_id, listing_id, category, plan, status, price_cents, reserved_until, created_at, updated_at) VALUES (?,?,?,?, 'reserved', ?,?,?,?)")
      .bind(vendor.id, l.id, l.category, plan, st.price_cents, new Date(Date.now() + RESERVE_DAYS * 864e5).toISOString(), now(), now()).run();
    const subId = r.meta.last_row_id;
    // Race check: the earliest rows win the seats.
    const occ = await occupants(env, l.category, plan);
    if (occ.findIndex((o) => o.id === subId) >= CAPACITY[plan]) { await env.DB.prepare("UPDATE subs SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), subId).run(); return json({ ok: false, error: "Someone took the last seat a moment ago." }, 409); }
    await env.DB.batch([
      env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(vendor.id, subId, st.price_cents, now(), now()),
      env.DB.prepare("DELETE FROM plan_waitlist WHERE vendor_id = ? AND category = ? AND plan = ?").bind(vendor.id, l.category, plan),
    ]);
    await notifyAdmin(env, `Plan reserved: ${PLAN_NAME[plan]} for ${l.product_name}`, [`${vendor.company} reserved ${PLAN_NAME[plan]} on ${l.category} for ${l.product_name}.`,
      `Invoice: ${money(st.price_cents)}, open for ${RESERVE_DAYS} days.`, payMode(env) === "iyzico" ? "They can pay by card in the portal." : "Send them an invoice, then mark it paid in the admin page.", l.status !== "approved" ? "The listing still needs your approval." : ""]);
    return json({ ok: true, sub_id: subId, method: payMode(env) });
  }
  m = path.match(/^\/api\/subs\/(\d+)\/(renew|cancel)$/);
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
    if (s.status !== "active" || s.paid_through <= now()) return json({ ok: false, error: "This plan has ended. Subscribe again if a seat is available." }, 400);
    const open = await env.DB.prepare("SELECT 1 FROM invoices WHERE slot_id = ? AND status = 'requested'").bind(s.id).first();
    if (open) return json({ ok: false, error: "A renewal invoice is already open for this plan." }, 400);
    const price = prices(env)[s.plan];
    await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(vendor.id, s.id, price, now(), now()).run();
    return json({ ok: true, method: payMode(env) });
  }
  if (path === "/api/waitlist" && method === "POST") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(body.listing_id), vendor.id).first();
    if (!l || !["pro", "premium"].includes(body.plan)) return json({ ok: false, error: "Choose a listing and plan." }, 400);
    const dup = await env.DB.prepare("SELECT 1 FROM plan_waitlist WHERE vendor_id = ? AND category = ? AND plan = ?").bind(vendor.id, l.category, body.plan).first();
    if (!dup) await env.DB.prepare("INSERT INTO plan_waitlist (vendor_id, listing_id, category, plan, created_at) VALUES (?,?,?,?,?)").bind(vendor.id, l.id, l.category, body.plan, now()).run();
    return json({ ok: true });
  }
  if (path === "/api/waitlist/leave" && method === "POST") {
    await env.DB.prepare("DELETE FROM plan_waitlist WHERE vendor_id = ? AND category = ? AND plan = ?").bind(vendor.id, oneLine(body.category, 120), oneLine(body.plan, 20)).run();
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
    const rows = (await env.DB.prepare(`SELECT i.*, s.category, s.plan, l.product_name FROM invoices i LEFT JOIN subs s ON s.id = i.slot_id LEFT JOIN listings l ON l.id = s.listing_id
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
        WHERE (s.status = 'active' AND s.paid_through > ?) OR (s.status = 'reserved' AND s.reserved_until > ?) ORDER BY s.category, CASE s.plan WHEN 'premium' THEN 0 WHEN 'pro' THEN 1 ELSE 2 END, s.started_at`, now(), now()),
      invoices: await q(`SELECT i.*, s.category, s.plan, s.status AS sub_status, l.product_name, v.company, v.email FROM invoices i JOIN vendors v ON v.id = i.vendor_id
        LEFT JOIN subs s ON s.id = i.slot_id LEFT JOIN listings l ON l.id = s.listing_id ORDER BY CASE i.status WHEN 'requested' THEN 0 ELSE 1 END, i.created_at DESC LIMIT 200`),
      waitlist: await q("SELECT w.*, l.product_name, v.company FROM plan_waitlist w JOIN listings l ON l.id = w.listing_id JOIN vendors v ON v.id = w.vendor_id ORDER BY w.category, w.plan, w.created_at"),
      stats: await q(`SELECT d.day, COALESCE((SELECT SUM(n) FROM impressions i WHERE i.day = d.day),0) AS impressions, COALESCE((SELECT SUM(billable) FROM clicks c WHERE substr(c.ts,1,10) = d.day),0) AS clicks
        FROM (SELECT DISTINCT day FROM impressions WHERE day >= ? UNION SELECT DISTINCT substr(ts,1,10) FROM clicks WHERE ts >= ?) d ORDER BY d.day DESC`, new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10), new Date(Date.now() - 30 * 864e5).toISOString()) });
  }
  let m = path.match(/^\/api\/admin\/listings\/(\d+)$/);
  if (m && method === "POST") {
    const status = ["approved", "rejected", "pending"].includes(body.status) ? body.status : null;
    if (!status) return json({ ok: false, error: "Bad status." }, 400);
    await env.DB.prepare("UPDATE listings SET status = ?, tool_id = ?, review_note = ?, updated_at = ? WHERE id = ?")
      .bind(status, oneLine(body.tool_id, 60) || null, oneLine(body.review_note, 300) || null, now(), Number(m[1])).run();
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
  m = path.match(/^\/api\/admin\/subs\/(\d+)\/end$/);
  if (m && method === "POST") {
    await env.DB.prepare("UPDATE subs SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), Number(m[1])).run();
    await clearPlacements();
    return json({ ok: true });
  }
  return json({ ok: false, error: "Not found." }, 404);
}

// Marks an invoice paid and starts or extends its plan by a year. Shared by the admin page and card payments.
async function activateInvoice(env, inv, ref) {
  const s = await env.DB.prepare("SELECT * FROM subs WHERE id = ?").bind(inv.slot_id).first();
  if (!s) return { ok: false, error: "The plan for this invoice no longer exists." };
  if (s.status === "cancelled") return { ok: false, error: "This reservation was cancelled." };
  const live = s.status === "active" ? s.paid_through > now() : s.reserved_until > now();
  if (!live) {
    const others = (await occupants(env, s.category, s.plan)).filter((o) => o.id !== s.id);
    if (others.length >= CAPACITY[s.plan]) return { ok: false, error: "This plan lapsed and its seat has been taken. Refund or offer another plan." };
  }
  const paidThrough = addYear(s.status === "active" ? later(s.paid_through, now()) : now());
  const r = await env.DB.prepare("UPDATE invoices SET status = 'paid', provider_ref = ?, updated_at = ? WHERE id = ? AND status = 'requested'").bind(ref, now(), inv.id).run();
  if (!r.meta.changes) return { ok: false, error: "This invoice was already closed." };
  await env.DB.prepare("UPDATE subs SET status = 'active', paid_through = ?, started_at = COALESCE(started_at, ?), updated_at = ? WHERE id = ?").bind(paidThrough, now(), now(), s.id).run();
  await clearPlacements();
  return { ok: true, paid_through: paidThrough, sub: s };
}

// ---------- card payments through iyzico (Checkout Form)
const money = (c) => "$" + (c / 100).toFixed(2);
function payMode(env) { return env.IYZICO_API_KEY && env.IYZICO_SECRET_KEY ? "iyzico" : "invoice"; }
const iyzicoBase = (env) => env.IYZICO_BASE_URL || (env.IYZICO_LIVE === "1" ? "https://api.iyzipay.com" : "https://sandbox-api.iyzipay.com");
async function hmacHex(key, msg) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function iyzico(env, path, payload) {
  const body = JSON.stringify(payload);
  const rnd = Date.now() + "" + Math.floor(Math.random() * 1e9);
  const sig = await hmacHex(env.IYZICO_SECRET_KEY, rnd + path + body);
  const auth = btoa(`apiKey:${env.IYZICO_API_KEY}&randomKey:${rnd}&signature:${sig}`);
  const r = await fetch(iyzicoBase(env) + path, { method: "POST", body,
    headers: { "content-type": "application/json", accept: "application/json", authorization: "IYZWSv2 " + auth, "x-iyzi-rnd": rnd } });
  return r.json();
}
const num = (v) => String(Number(v)); // iyzico signs prices without trailing zeros ("50.00" -> "50")

async function startCardPayment(request, env, vendor, body) {
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
  const res = await iyzico(env, "/payment/iyzipos/checkoutform/initialize/auth/ecom", {
    locale: "en", conversationId: String(inv.id), price, paidPrice: price, currency: env.IYZICO_CURRENCY || "USD", basketId: "inv-" + inv.id,
    paymentGroup: "LISTING", callbackUrl: origin + "/api/pay/callback", enabledInstallments: [1],
    buyer: { id: "v" + vendor.id, name: b.name, surname: b.surname, gsmNumber: b.phone, email: vendor.email, identityNumber: b.tax_id,
      registrationAddress: b.address, city: b.city, country: b.country, zipCode: b.zip || undefined, ip: request.headers.get("cf-connecting-ip") || "" },
    billingAddress: addr,
    basketItems: [{ id: "sub-" + s.id, name: `Vettlo ${PLAN_NAME[s.plan]} plan, 1 year: ${s.product_name}`.slice(0, 120), category1: "Advertising", itemType: "VIRTUAL", price }],
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
  await notifyAdmin(env, `Payment received: ${money(inv.amount_cents)} from ${v && v.company}`, [`${PLAN_NAME[r.sub.plan]} plan for ${l.product_name} on ${r.sub.category}, paid by card (iyzico ${res.paymentId}).`, `Active until ${r.paid_through.slice(0, 10)}.`,
    r.sub.plan !== "basic" && !l.tool_id ? "We haven't scored this product yet, so it won't show in the top places until it's reviewed and matched to a tool on our list. Ask Claude to review and score it." :
    l.status === "approved" ? "The listing is approved, so it's live now." : "The listing is waiting for your approval. Approve it in the admin page to put it live."]);
  return back("pay=ok");
}

// ---------- click tracking (reporting only; positions are billed monthly, not per click)
export async function handleGo(request, env, ctx) {
  if (!env.DB) return Response.redirect(new URL("/", request.url).toString(), 302);
  await migrate(env);
  const url = new URL(request.url);
  const id = Number(url.pathname.split("/")[2]);
  const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ?").bind(id).first();
  if (!l || !isUrl(l.landing_url)) return Response.redirect(new URL("/", request.url).toString(), 302);
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
const SPONSOR_KEY = "https://vettlo.com/__cache/sponsors-v1";
async function allSponsors(env) {
  const hit = placementCache.get("*");
  if (hit && hit.t > Date.now() - 60e3) return hit.v;
  let v = null;
  try { const c = await caches.default.match(SPONSOR_KEY); if (c) v = await c.json(); } catch {}
  if (!v) {
    const rows = (await env.DB.prepare(`SELECT l.*, s.plan, s.category AS sub_category FROM subs s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
      WHERE s.status = 'active' AND s.paid_through > ? AND l.status = 'approved' AND l.active = 1 AND v.status = 'active'
      ORDER BY s.started_at ASC, s.id ASC`).bind(now()).all()).results;
    v = {};
    for (const r of rows) (v[r.sub_category] ||= []).push(r);
    try { await caches.default.put(SPONSOR_KEY, new Response(JSON.stringify(v), { headers: { "content-type": "application/json", "cache-control": "public, max-age=300" } })); } catch {}
  }
  placementCache.set("*", { t: Date.now(), v });
  return v;
}
async function clearPlacements() {
  placementCache.clear();
  try { await caches.default.delete(SPONSOR_KEY); } catch {}
}
async function sponsors(env, category) {
  const rows = (await allSponsors(env))[category] || [];
  // premium takes 1st place, pro takes 2nd and 3rd in order of subscription, basic goes to the top of "Other tools to consider"
  // Pro and Premium show only once we've scored the product (it maps to a tool on our list), so every ranked card looks and reads the same.
  return [...rows.filter((r) => r.plan === "premium" && r.tool_id).slice(0, 1).map((r) => ({ ...r, position: 1 })),
    ...rows.filter((r) => r.plan === "pro" && r.tool_id).slice(0, 2).map((r, i) => ({ ...r, position: 2 + i })),
    ...rows.filter((r) => r.plan === "basic").map((r) => ({ ...r, position: 0 }))];
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
  if (!m || m[1].endsWith("-alternatives") || !env.DB || response.status !== 200 || !(response.headers.get("content-type") || "").includes("text/html")) return response;
  const slug = m[1];
  let partners;
  try { partners = await sponsors(env, slug); } catch { return response; }  // no schema setup on the public path: tables exist once the portal has run
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
