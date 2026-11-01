// Vettlo vendor portal: magic-link login, listings, bids, budgets, funds, click tracking and
// bid-based placement on category shortlists. Data lives in the D1 database bound as DB.

const MIN_BID_DEFAULT = 200; // cents
const BID_STEP = 50; // cents
const SESSION_DAYS = 30;
const TOKEN_MINUTES = 20;
const BOT_UA = /bot|crawl|spider|slurp|preview|headless|python|curl|wget|httpclient|monitor|scan|facebookexternalhit|embedly/i;

export const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store", ...headers } });

const now = () => new Date().toISOString();
const monthStart = () => { const d = new Date(); return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 1)).toISOString(); };
const clean = (v, max) => String(v ?? "").replace(/[\r\u0000]/g, "").trim().slice(0, max);
const oneLine = (v, max) => clean(v, max).replace(/\s*\n\s*/g, " ");
const isEmail = (e) => /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(e);
const isUrl = (u) => { try { const x = new URL(u); return x.protocol === "https:" || x.protocol === "http:"; } catch { return false; } };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const minBid = (env) => Number(env.MIN_BID_CENTS || MIN_BID_DEFAULT);

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

// ---------- vendor data helpers
async function monthSpend(env, vendorId) {
  const r = await env.DB.prepare("SELECT COALESCE(SUM(cost_cents),0) AS c FROM clicks WHERE vendor_id = ? AND ts >= ?").bind(vendorId, monthStart()).first();
  return r.c;
}

async function eligibleListings(env, category) {
  const ms = monthStart();
  const rows = await env.DB.prepare(
    `SELECT l.*, v.balance_cents, v.monthly_budget_cents,
       (SELECT COALESCE(SUM(cost_cents),0) FROM clicks c WHERE c.vendor_id = v.id AND c.ts >= ?) AS spent
     FROM listings l JOIN vendors v ON v.id = l.vendor_id
     WHERE l.category = ? AND l.status = 'approved' AND l.active = 1 AND v.status = 'active' AND l.bid_cents >= ?
     ORDER BY l.bid_cents DESC, l.created_at ASC`).bind(ms, category, minBid(env)).all();
  return rows.results.filter((r) => r.balance_cents >= r.bid_cents && (!r.monthly_budget_cents || r.spent + r.bid_cents <= r.monthly_budget_cents));
}

async function categories(env, request) {
  const r = await env.ASSETS.fetch(new Request(new URL("/data/categories.json", request.url)));
  return r.ok ? r.json() : [];
}

// ---------- vendor API
async function vendorApi(request, env, vendor, path) {
  const method = request.method;
  const body = method === "GET" ? {} : await request.json().catch(() => ({}));

  if (path === "/api/me" && method === "GET") {
    return json({ ok: true, vendor: { id: vendor.id, email: vendor.email, company: vendor.company, website: vendor.website,
      balance_cents: vendor.balance_cents, monthly_budget_cents: vendor.monthly_budget_cents, is_admin: vendor.is_admin,
      month_spend_cents: await monthSpend(env, vendor.id) }, min_bid_cents: minBid(env), bid_step_cents: BID_STEP,
      payments: env.IYZICO_API_KEY ? "iyzico" : "invoice" });
  }
  if (path === "/api/me" && method === "PUT") {
    const company = oneLine(body.company, 120) || vendor.company;
    const website = isUrl(body.website) ? oneLine(body.website, 300) : vendor.website;
    const budget = body.monthly_budget_cents === null || body.monthly_budget_cents === "" ? null : Math.max(0, Math.round(Number(body.monthly_budget_cents) || 0));
    await env.DB.prepare("UPDATE vendors SET company = ?, website = ?, monthly_budget_cents = ? WHERE id = ?").bind(company, website, budget, vendor.id).run();
    return json({ ok: true });
  }
  if (path === "/api/logout" && method === "POST") {
    const tok = getCookie(request, "vs");
    if (tok) await env.DB.prepare("DELETE FROM sessions WHERE hash = ?").bind(await sha256(tok)).run();
    return json({ ok: true }, 200, { "set-cookie": "vs=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0" });
  }
  if (path === "/api/listings" && method === "GET") {
    const rows = (await env.DB.prepare("SELECT * FROM listings WHERE vendor_id = ? ORDER BY created_at DESC").bind(vendor.id).all()).results;
    const since = new Date(Date.now() - 30 * 864e5).toISOString();
    for (const l of rows) {
      const comp = (await env.DB.prepare("SELECT id, bid_cents FROM listings WHERE category = ? AND status = 'approved' AND active = 1 ORDER BY bid_cents DESC, created_at ASC").bind(l.category).all()).results;
      l.top_bid_cents = comp.length ? comp[0].bid_cents : 0;
      const pos = comp.findIndex((c) => c.id === l.id);
      l.position = pos >= 0 ? pos + 1 : comp.filter((c) => c.bid_cents >= l.bid_cents).length + 1;
      const st = await env.DB.prepare("SELECT COUNT(*) AS clicks, COALESCE(SUM(billable),0) AS billable, COALESCE(SUM(cost_cents),0) AS cost FROM clicks WHERE listing_id = ? AND ts >= ?").bind(l.id, since).first();
      Object.assign(l, { clicks_30d: st.clicks, billable_30d: st.billable, cost_30d_cents: st.cost });
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
    const bid = Math.max(minBid(env), Math.round(Number(body.bid_cents) || minBid(env)));
    const tool = (cat.tools || []).find((t) => t.name.toLowerCase() === f.product_name.toLowerCase());
    await env.DB.prepare(`INSERT INTO listings (vendor_id, product_name, website, landing_url, category, tool_id, best_for, description, starting_price, bid_cents, created_at, updated_at)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?)`).bind(vendor.id, f.product_name, f.website, f.landing_url, cat.slug, tool ? tool.id : null, f.best_for, f.description, f.starting_price, bid, now(), now()).run();
    return json({ ok: true });
  }
  let m = path.match(/^\/api\/listings\/(\d+)$/);
  if (m && method === "PUT") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(m[1]), vendor.id).first();
    if (!l) return json({ ok: false, error: "Not found." }, 404);
    const bid = body.bid_cents !== undefined ? Math.max(minBid(env), Math.round(Number(body.bid_cents) || 0)) : l.bid_cents;
    if (bid % BID_STEP !== 0) return json({ ok: false, error: `Bids move in steps of $${(BID_STEP / 100).toFixed(2)}.` }, 400);
    const active = body.active !== undefined ? (body.active ? 1 : 0) : l.active;
    const landing = body.landing_url !== undefined && isUrl(body.landing_url) ? oneLine(body.landing_url, 500) : l.landing_url;
    // Copy edits go back to editorial review; bid, pause and landing page changes don't.
    const copy = ["best_for", "description", "starting_price"].some((k) => body[k] !== undefined && oneLine(body[k], 600) !== (l[k] || ""));
    const status = copy && l.status === "approved" ? "pending" : l.status;
    await env.DB.prepare(`UPDATE listings SET bid_cents = ?, active = ?, landing_url = ?, best_for = COALESCE(?, best_for), description = COALESCE(?, description),
      starting_price = COALESCE(?, starting_price), status = ?, updated_at = ? WHERE id = ?`)
      .bind(bid, active, landing, body.best_for !== undefined ? oneLine(body.best_for, 90) : null, body.description !== undefined ? clean(body.description, 600) : null,
        body.starting_price !== undefined ? oneLine(body.starting_price, 80) : null, status, now(), l.id).run();
    return json({ ok: true, resubmitted: status !== l.status });
  }
  if (path === "/api/reports" && method === "GET") {
    const days = Math.min(90, Math.max(1, Number(new URL(request.url).searchParams.get("days")) || 30));
    const since = new Date(Date.now() - days * 864e5).toISOString();
    const rows = (await env.DB.prepare(`SELECT substr(c.ts,1,10) AS day, l.product_name, c.category, COUNT(*) AS clicks, SUM(c.billable) AS billable, SUM(c.cost_cents) AS cost_cents
      FROM clicks c JOIN listings l ON l.id = c.listing_id WHERE c.vendor_id = ? AND c.ts >= ? GROUP BY day, l.id, c.category ORDER BY day DESC`).bind(vendor.id, since).all()).results;
    return json({ ok: true, rows });
  }
  if (path === "/api/funds" && method === "GET") {
    const rows = (await env.DB.prepare("SELECT * FROM ledger WHERE vendor_id = ? ORDER BY created_at DESC LIMIT 100").bind(vendor.id).all()).results;
    return json({ ok: true, rows });
  }
  if (path === "/api/funds" && method === "POST") {
    const amount = Math.round(Number(body.amount_cents) || 0);
    if (amount < 5000 || amount > 5000000) return json({ ok: false, error: "Choose an amount between $50 and $50,000." }, 400);
    await env.DB.prepare("INSERT INTO ledger (vendor_id, amount_cents, kind, status, note, created_at, updated_at) VALUES (?, ?, 'topup', 'requested', ?, ?, ?)")
      .bind(vendor.id, amount, oneLine(body.note, 200) || null, now(), now()).run();
    return json({ ok: true, method: env.IYZICO_API_KEY ? "iyzico" : "invoice" });
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
    return json({ ok: true,
      vendors: await q("SELECT id, email, company, website, balance_cents, monthly_budget_cents, status, created_at FROM vendors ORDER BY created_at DESC"),
      listings: await q("SELECT l.*, v.company, v.email FROM listings l JOIN vendors v ON v.id = l.vendor_id ORDER BY CASE l.status WHEN 'pending' THEN 0 ELSE 1 END, l.updated_at DESC"),
      funds: await q("SELECT f.*, v.company, v.email FROM ledger f JOIN vendors v ON v.id = f.vendor_id ORDER BY f.created_at DESC LIMIT 200"),
      clicks: await q("SELECT substr(ts,1,10) AS day, COUNT(*) AS clicks, SUM(billable) AS billable, SUM(cost_cents) AS cost_cents FROM clicks WHERE ts >= ? GROUP BY day ORDER BY day DESC", new Date(Date.now() - 30 * 864e5).toISOString()) });
  }
  let m = path.match(/^\/api\/admin\/listings\/(\d+)$/);
  if (m && method === "POST") {
    const status = ["approved", "rejected", "pending"].includes(body.status) ? body.status : null;
    if (!status) return json({ ok: false, error: "Bad status." }, 400);
    await env.DB.prepare("UPDATE listings SET status = ?, tool_id = ?, review_note = ?, updated_at = ? WHERE id = ?")
      .bind(status, oneLine(body.tool_id, 60) || null, oneLine(body.review_note, 300) || null, now(), Number(m[1])).run();
    return json({ ok: true });
  }
  m = path.match(/^\/api\/admin\/funds\/(\d+)$/);
  if (m && method === "POST") {
    const f = await env.DB.prepare("SELECT * FROM ledger WHERE id = ?").bind(Number(m[1])).first();
    if (!f || f.status === "paid") return json({ ok: false, error: "Not found or already paid." }, 400);
    if (body.status === "paid") {
      await env.DB.batch([
        env.DB.prepare("UPDATE ledger SET status = 'paid', provider_ref = ?, updated_at = ? WHERE id = ?").bind(oneLine(body.ref, 120) || null, now(), f.id),
        env.DB.prepare("UPDATE vendors SET balance_cents = balance_cents + ? WHERE id = ?").bind(f.amount_cents, f.vendor_id),
      ]);
    } else if (body.status === "cancelled") {
      await env.DB.prepare("UPDATE ledger SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), f.id).run();
    }
    return json({ ok: true });
  }
  if (path === "/api/admin/credit" && method === "POST") {
    const amount = Math.round(Number(body.amount_cents) || 0);
    if (!amount) return json({ ok: false, error: "Amount required." }, 400);
    await env.DB.batch([
      env.DB.prepare("INSERT INTO ledger (vendor_id, amount_cents, kind, status, note, created_at, updated_at) VALUES (?, ?, 'adjustment', 'paid', ?, ?, ?)")
        .bind(Number(body.vendor_id), amount, oneLine(body.note, 200) || null, now(), now()),
      env.DB.prepare("UPDATE vendors SET balance_cents = balance_cents + ? WHERE id = ?").bind(amount, Number(body.vendor_id)),
    ]);
    return json({ ok: true });
  }
  return json({ ok: false, error: "Not found." }, 404);
}

// ---------- click tracking
export async function handleGo(request, env, ctx) {
  if (!env.DB) return Response.redirect(new URL("/", request.url).toString(), 302);
  await migrate(env);
  const url = new URL(request.url);
  const id = Number(url.pathname.split("/")[2]);
  const l = await env.DB.prepare("SELECT l.*, v.balance_cents, v.monthly_budget_cents FROM listings l JOIN vendors v ON v.id = l.vendor_id WHERE l.id = ?").bind(id).first();
  if (!l || !isUrl(l.landing_url)) return Response.redirect(new URL("/", request.url).toString(), 302);
  const ua = request.headers.get("user-agent") || "";
  const ip = request.headers.get("cf-connecting-ip") || "";
  const day = new Date().toISOString().slice(0, 10);
  const ipHash = await sha256(`${ip}|${day}|${env.CLICK_SALT || "vettlo"}`);
  const category = oneLine(url.searchParams.get("c"), 120) || l.category;
  const page = oneLine(url.searchParams.get("p"), 300);
  ctx.waitUntil((async () => {
    let billable = 0, cost = 0, reason = "";
    if (!ua || BOT_UA.test(ua)) reason = "bot";
    else if (l.status !== "approved" || !l.active) reason = "inactive";
    else {
      const dup = await env.DB.prepare("SELECT 1 FROM clicks WHERE listing_id = ? AND ip_hash = ? AND ts >= ? LIMIT 1")
        .bind(l.id, ipHash, new Date(Date.now() - 864e5).toISOString()).first();
      if (dup) reason = "duplicate";
      else {
        const spent = await monthSpend(env, l.vendor_id);
        if (l.monthly_budget_cents && spent + l.bid_cents > l.monthly_budget_cents) reason = "budget";
        else {
          const r = await env.DB.prepare("UPDATE vendors SET balance_cents = balance_cents - ? WHERE id = ? AND balance_cents >= ?").bind(l.bid_cents, l.vendor_id, l.bid_cents).run();
          if (r.meta.changes) { billable = 1; cost = l.bid_cents; } else reason = "no-funds";
        }
      }
    }
    await env.DB.prepare("INSERT INTO clicks (listing_id, vendor_id, category, page, ts, ip_hash, billable, cost_cents, reason) VALUES (?,?,?,?,?,?,?,?,?)")
      .bind(l.id, l.vendor_id, category, page, now(), ipHash, billable, cost, reason || null).run();
  })());
  const dest = new URL(l.landing_url);
  return new Response(null, { status: 302, headers: { location: dest.toString(), "cache-control": "no-store", "referrer-policy": "origin", "x-robots-tag": "noindex" } });
}

// ---------- API router
export async function handlePortalApi(request, env, path) {
  if (!env.DB) return json({ ok: false, error: "The vendor portal isn't connected to its database yet." }, 503);
  await migrate(env);
  if (request.method !== "GET" && request.headers.get("x-requested-with") !== "vettlo") return json({ ok: false, error: "Bad request." }, 400);
  if (path === "/api/auth/request" && request.method === "POST") return requestLogin(request, env, await request.json().catch(() => ({})));
  if (path === "/api/auth/verify" && request.method === "GET") return verifyLogin(request, env);
  if (path === "/api/categories") return json({ ok: true, categories: await categories(env, request) });
  const vendor = await currentVendor(request, env);
  if (!vendor) return json({ ok: false, error: "Please sign in.", auth: true }, 401);
  if (path.startsWith("/api/admin/")) return adminApi(request, env, vendor, path);
  return (await vendorApi(request, env, vendor, path)) || json({ ok: false, error: "Not found." }, 404);
}

// ---------- bid-based placement on category shortlists
const placementCache = new Map();
async function cachedPlacements(env, category) {
  const hit = placementCache.get(category);
  if (hit && hit.t > Date.now() - 60e3) return hit.v;
  const v = await eligibleListings(env, category);
  placementCache.set(category, { t: Date.now(), v });
  return v;
}

function partnerLi(l, i, catSlug, path) {
  const host = (() => { try { return new URL(l.website).hostname.replace(/^www\./, ""); } catch { return ""; } })();
  return `<li><span class="rank">${i}</span><span><a class="nm" href="#partner-${l.id}"><img class="tlogo tlogo-24" src="https://www.google.com/s2/favicons?domain=${esc(host)}&amp;sz=64" alt="" width="24" height="24" loading="lazy">${esc(l.product_name)}</a><br><span class="bf">${esc(l.best_for || "")}</span></span><span class="sc muted small">Not scored</span><a class="btn ghost small" href="/go/${l.id}?c=${esc(catSlug)}&amp;p=${encodeURIComponent(path)}" rel="sponsored nofollow noopener" target="_blank">Visit</a></li>`;
}
function partnerCard(l, i, catSlug, path) {
  const host = (() => { try { return new URL(l.website).hostname.replace(/^www\./, ""); } catch { return ""; } })();
  return `<article class="tool" id="partner-${l.id}"><div class="tool-head"><span class="num">${i}</span><div><h3><img class="tlogo tlogo-40" src="https://www.google.com/s2/favicons?domain=${esc(host)}&amp;sz=128" alt="" width="40" height="40" loading="lazy">${esc(l.product_name)}</h3><div class="bestfor">${esc(l.best_for || "")}</div></div>
<a class="btn small" href="/go/${l.id}?c=${esc(catSlug)}&amp;p=${encodeURIComponent(path)}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
<div class="tool-body">${l.description ? `<p>${esc(l.description)}</p>` : ""}${l.starting_price ? `<p><b>Starting price:</b> ${esc(l.starting_price)} (as provided by the vendor)</p>` : ""}<p class="small muted">We haven't scored this product yet.</p></div></article>`;
}

export async function placeOnShortlist(request, env, response) {
  const url = new URL(request.url);
  const m = url.pathname.match(/^\/tools\/(best-[a-z0-9-]+)\/$/);
  if (!m || !env.DB || response.status !== 200 || !(response.headers.get("content-type") || "").includes("text/html")) return response;
  const slug = m[1];
  let partners;
  try { await migrate(env); partners = await cachedPlacements(env, slug); } catch { return response; }
  if (!partners.length) return response;
  let html = await response.text();
  const path = url.pathname;

  // shortlist
  html = html.replace(/(<ol class="shortlist">)([\s\S]*?)(<\/ol>)/, (all, a, inner, z) => {
    let items = inner.match(/<li>[\s\S]*?<\/li>/g) || [];
    const top = [];
    for (const p of partners) {
      const idx = p.tool_id ? items.findIndex((li) => li.includes(`href="#${p.tool_id}"`)) : -1;
      top.push(idx >= 0 ? items.splice(idx, 1)[0] : partnerLi(p, 0, slug, path));
    }
    const all2 = [...top, ...items].map((li, i) => li.replace(/<span class="rank">\d+<\/span>/, `<span class="rank">${i + 1}</span>`));
    return a + all2.join("") + z;
  });
  // review cards
  html = html.replace(/(<section id="reviews"><h2>[^<]*<\/h2>)([\s\S]*?)(<\/section>)/, (all, a, inner, z) => {
    let cards = inner.match(/<article class="tool"[\s\S]*?<\/article>/g) || [];
    const top = [];
    for (const p of partners) {
      const idx = p.tool_id ? cards.findIndex((c) => c.startsWith(`<article class="tool" id="${p.tool_id}"`)) : -1;
      top.push(idx >= 0 ? cards.splice(idx, 1)[0] : partnerCard(p, 0, slug, path));
    }
    const out = [...top, ...cards].map((c, i) => c.replace(/<span class="num">\d+<\/span>/, `<span class="num">${i + 1}</span>`));
    return a + out.join("\n") + z;
  });
  // comparison table rows
  html = html.replace(/(<section id="compare">[\s\S]*?<tbody>)([\s\S]*?)(<\/tbody>)/, (all, a, inner, z) => {
    let rows = inner.match(/<tr>[\s\S]*?<\/tr>/g) || [];
    const top = [];
    for (const p of partners) {
      const idx = p.tool_id ? rows.findIndex((r) => r.includes(`href="#${p.tool_id}"`)) : -1;
      if (idx >= 0) top.push(rows.splice(idx, 1)[0]);
    }
    const out = [...top, ...rows].map((r, i) => r.replace(/<td class="num">\d+<\/td>/, `<td class="num">${i + 1}</td>`));
    return a + out.join("") + z;
  });
  // send partners' existing "Visit website" buttons through click tracking
  for (const p of partners) {
    if (!p.tool_id) continue;
    html = html.replace(new RegExp(`(<article class="tool" id="${p.tool_id}">[\\s\\S]*?<a class="btn small" href=")[^"]+(")`), `$1/go/${p.id}?c=${slug}&amp;p=${encodeURIComponent(path)}$2`);
  }
  const headers = new Headers(response.headers);
  headers.delete("content-length");
  headers.set("cache-control", "public, max-age=0, must-revalidate");
  return new Response(html, { status: 200, headers });
}
