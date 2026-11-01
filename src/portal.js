// Vettlo vendor portal: magic-link login, listings, fixed monthly positions on category shortlists
// (with invoices, renewals and waitlists), click and impression reporting. Data lives in the D1 database bound as DB.

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

// ---------- placements: fixed monthly positions per category
const POSITIONS = 3;
const RESERVE_DAYS = 7;       // an unpaid reservation holds the position this long
const WAITLIST_HOURS = 72;    // when a position frees up, the first vendor on its waitlist gets it first for this long
const DEFAULT_PRICES = [29900, 19900, 14900];
function prices(env, category) {
  try { const o = env.SLOT_PRICES_JSON ? JSON.parse(env.SLOT_PRICES_JSON) : null; if (o && Array.isArray(o[category])) return o[category].map(Number); } catch {}
  const p = (env.SLOT_PRICES || "").split(",").map((x) => Number(x.trim())).filter((x) => x > 0);
  return p.length === POSITIONS ? p : DEFAULT_PRICES;
}
const addMonth = (iso) => { const d = new Date(iso); const day = d.getUTCDate(); d.setUTCMonth(d.getUTCMonth() + 1); if (d.getUTCDate() < day) d.setUTCDate(0); return d.toISOString(); };
const later = (a, b) => (!a ? b : !b ? a : a > b ? a : b);

// The row currently holding (category, position): an active slot paid through the future, or an unexpired reservation.
async function holder(env, category, position) {
  return env.DB.prepare(`SELECT s.*, l.product_name FROM slots s JOIN listings l ON l.id = s.listing_id WHERE s.category = ? AND s.position = ?
    AND ((s.status = 'active' AND s.paid_through > ?) OR (s.status = 'reserved' AND s.reserved_until > ?)) ORDER BY s.id DESC LIMIT 1`)
    .bind(category, position, now(), now()).first();
}
// When the position last became free (end of the latest paid period or reservation).
async function freedAt(env, category, position) {
  const r = await env.DB.prepare(`SELECT MAX(t) AS t FROM (SELECT CASE WHEN status = 'cancelled' THEN updated_at WHEN paid_through IS NOT NULL THEN paid_through ELSE reserved_until END AS t
    FROM slots WHERE category = ? AND position = ?) WHERE t <= ?`).bind(category, position, now()).first();
  return r && r.t;
}
async function waitHead(env, category, position) {
  return env.DB.prepare("SELECT * FROM waitlist WHERE category = ? AND position = ? ORDER BY created_at ASC, id ASC LIMIT 1").bind(category, position).first();
}
async function positionState(env, category, vendorId) {
  const P = prices(env, category), out = [];
  for (let pos = 1; pos <= POSITIONS; pos++) {
    const h = await holder(env, category, pos);
    const wl = (await env.DB.prepare("SELECT vendor_id FROM waitlist WHERE category = ? AND position = ? ORDER BY created_at ASC, id ASC").bind(category, pos).all()).results;
    const st = { position: pos, price_cents: P[pos - 1], waitlist: wl.length, on_waitlist: wl.some((w) => w.vendor_id === vendorId) };
    if (h) {
      st.state = h.vendor_id === vendorId ? (h.status === "active" ? "yours" : "reserved_by_you") : "taken";
      st.until = h.status === "active" ? h.paid_through : h.reserved_until;
      st.slot_id = h.vendor_id === vendorId ? h.id : undefined;
    } else {
      const f = await freedAt(env, category, pos);
      const priorityEnds = f && wl.length ? new Date(Date.parse(f) + WAITLIST_HOURS * 3600e3).toISOString() : null;
      if (priorityEnds && priorityEnds > now() && wl[0].vendor_id !== vendorId) { st.state = "priority_other"; st.until = priorityEnds; }
      else st.state = "available";
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
      prices_cents: prices(env, ""), positions: POSITIONS, payments: env.IYZICO_API_KEY ? "iyzico" : "invoice" });
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
      const s = await env.DB.prepare(`SELECT * FROM slots WHERE listing_id = ? AND ((status = 'active' AND paid_through > ?) OR (status = 'reserved' AND reserved_until > ?)) ORDER BY id DESC LIMIT 1`).bind(l.id, now(), now()).first();
      Object.assign(l, { clicks_30d: c.n, impressions_30d: im.n, slot: s || null });
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
    return json({ ok: true, resubmitted: status !== l.status });
  }
  if (path === "/api/positions" && method === "GET") {
    const cat = new URL(request.url).searchParams.get("category") || "";
    return json({ ok: true, category: cat, positions: await positionState(env, cat, vendor.id) });
  }
  if (path === "/api/slots" && method === "POST") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(body.listing_id), vendor.id).first();
    const pos = Number(body.position);
    if (!l) return json({ ok: false, error: "Choose one of your listings." }, 400);
    if (!(pos >= 1 && pos <= POSITIONS)) return json({ ok: false, error: "Choose a position." }, 400);
    if (l.status === "rejected") return json({ ok: false, error: "This listing wasn't approved. Edit it and resubmit first." }, 400);
    const own = await env.DB.prepare(`SELECT 1 FROM slots WHERE listing_id = ? AND ((status = 'active' AND paid_through > ?) OR (status = 'reserved' AND reserved_until > ?))`).bind(l.id, now(), now()).first();
    if (own) return json({ ok: false, error: "This listing already holds a position. Renew it or let it expire first." }, 400);
    const st = (await positionState(env, l.category, vendor.id))[pos - 1];
    if (st.state !== "available") return json({ ok: false, error: st.state === "priority_other" ? "Another vendor on the waitlist has first claim on this position until " + st.until.slice(0, 10) + "." : "This position is taken. Join the waitlist to get it next." }, 409);
    const price = st.price_cents;
    const r = await env.DB.prepare("INSERT INTO slots (vendor_id, listing_id, category, position, status, price_cents, reserved_until, created_at, updated_at) VALUES (?,?,?,?, 'reserved', ?,?,?,?)")
      .bind(vendor.id, l.id, l.category, pos, price, new Date(Date.now() + RESERVE_DAYS * 864e5).toISOString(), now(), now()).run();
    const slotId = r.meta.last_row_id;
    // Re-check for a race: if someone else reserved the same position at the same moment, the earlier row wins.
    const first = await env.DB.prepare("SELECT id FROM slots WHERE category = ? AND position = ? AND status = 'reserved' AND reserved_until > ? ORDER BY id ASC LIMIT 1").bind(l.category, pos, now()).first();
    if (first && first.id !== slotId) { await env.DB.prepare("UPDATE slots SET status = 'cancelled' WHERE id = ?").bind(slotId).run(); return json({ ok: false, error: "Someone reserved this position a moment ago." }, 409); }
    await env.DB.batch([
      env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(vendor.id, slotId, price, now(), now()),
      env.DB.prepare("DELETE FROM waitlist WHERE vendor_id = ? AND category = ? AND position = ?").bind(vendor.id, l.category, pos),
    ]);
    return json({ ok: true, slot_id: slotId, method: env.IYZICO_API_KEY ? "iyzico" : "invoice" });
  }
  m = path.match(/^\/api\/slots\/(\d+)\/(renew|cancel)$/);
  if (m && method === "POST") {
    const s = await env.DB.prepare("SELECT * FROM slots WHERE id = ? AND vendor_id = ?").bind(Number(m[1]), vendor.id).first();
    if (!s) return json({ ok: false, error: "Not found." }, 404);
    if (m[2] === "cancel") {
      if (s.status !== "reserved") return json({ ok: false, error: "Only unpaid reservations can be cancelled. A paid position simply ends if you don't renew it." }, 400);
      await env.DB.batch([
        env.DB.prepare("UPDATE slots SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), s.id),
        env.DB.prepare("UPDATE invoices SET status = 'cancelled', updated_at = ? WHERE slot_id = ? AND status = 'requested'").bind(now(), s.id),
      ]);
      return json({ ok: true });
    }
    if (s.status !== "active" || s.paid_through <= now()) return json({ ok: false, error: "This position has ended. Reserve it again if it's available." }, 400);
    const open = await env.DB.prepare("SELECT 1 FROM invoices WHERE slot_id = ? AND status = 'requested'").bind(s.id).first();
    if (open) return json({ ok: false, error: "A renewal invoice is already open for this position." }, 400);
    const price = prices(env, s.category)[s.position - 1];
    await env.DB.prepare("INSERT INTO invoices (vendor_id, slot_id, amount_cents, status, created_at, updated_at) VALUES (?,?,?, 'requested', ?, ?)").bind(vendor.id, s.id, price, now(), now()).run();
    return json({ ok: true, method: env.IYZICO_API_KEY ? "iyzico" : "invoice" });
  }
  if (path === "/api/waitlist" && method === "POST") {
    const l = await env.DB.prepare("SELECT * FROM listings WHERE id = ? AND vendor_id = ?").bind(Number(body.listing_id), vendor.id).first();
    const pos = Number(body.position);
    if (!l || !(pos >= 1 && pos <= POSITIONS)) return json({ ok: false, error: "Choose a listing and position." }, 400);
    const dup = await env.DB.prepare("SELECT 1 FROM waitlist WHERE vendor_id = ? AND category = ? AND position = ?").bind(vendor.id, l.category, pos).first();
    if (!dup) await env.DB.prepare("INSERT INTO waitlist (vendor_id, listing_id, category, position, created_at) VALUES (?,?,?,?,?)").bind(vendor.id, l.id, l.category, pos, now()).run();
    return json({ ok: true });
  }
  if (path === "/api/waitlist/leave" && method === "POST") {
    await env.DB.prepare("DELETE FROM waitlist WHERE vendor_id = ? AND category = ? AND position = ?").bind(vendor.id, oneLine(body.category, 120), Number(body.position)).run();
    return json({ ok: true });
  }
  if (path === "/api/invoices" && method === "GET") {
    const rows = (await env.DB.prepare(`SELECT i.*, s.category, s.position, l.product_name FROM invoices i LEFT JOIN slots s ON s.id = i.slot_id LEFT JOIN listings l ON l.id = s.listing_id
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
      slots: await q(`SELECT s.*, l.product_name, l.status AS listing_status, v.company, v.email FROM slots s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
        WHERE (s.status = 'active' AND s.paid_through > ?) OR (s.status = 'reserved' AND s.reserved_until > ?) ORDER BY s.category, s.position`, now(), now()),
      invoices: await q(`SELECT i.*, s.category, s.position, s.status AS slot_status, l.product_name, v.company, v.email FROM invoices i JOIN vendors v ON v.id = i.vendor_id
        LEFT JOIN slots s ON s.id = i.slot_id LEFT JOIN listings l ON l.id = s.listing_id ORDER BY CASE i.status WHEN 'requested' THEN 0 ELSE 1 END, i.created_at DESC LIMIT 200`),
      waitlist: await q("SELECT w.*, l.product_name, v.company FROM waitlist w JOIN listings l ON l.id = w.listing_id JOIN vendors v ON v.id = w.vendor_id ORDER BY w.category, w.position, w.created_at"),
      stats: await q(`SELECT d.day, COALESCE((SELECT SUM(n) FROM impressions i WHERE i.day = d.day),0) AS impressions, COALESCE((SELECT SUM(billable) FROM clicks c WHERE substr(c.ts,1,10) = d.day),0) AS clicks
        FROM (SELECT DISTINCT day FROM impressions WHERE day >= ? UNION SELECT DISTINCT substr(ts,1,10) FROM clicks WHERE ts >= ?) d ORDER BY d.day DESC`, new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10), new Date(Date.now() - 30 * 864e5).toISOString()) });
  }
  let m = path.match(/^\/api\/admin\/listings\/(\d+)$/);
  if (m && method === "POST") {
    const status = ["approved", "rejected", "pending"].includes(body.status) ? body.status : null;
    if (!status) return json({ ok: false, error: "Bad status." }, 400);
    await env.DB.prepare("UPDATE listings SET status = ?, tool_id = ?, review_note = ?, updated_at = ? WHERE id = ?")
      .bind(status, oneLine(body.tool_id, 60) || null, oneLine(body.review_note, 300) || null, now(), Number(m[1])).run();
    placementCache.clear();
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
    const s = await env.DB.prepare("SELECT * FROM slots WHERE id = ?").bind(inv.slot_id).first();
    if (!s) return json({ ok: false, error: "The position for this invoice no longer exists." }, 400);
    let paidThrough;
    if (s.status === "reserved") {
      const h = await holder(env, s.category, s.position);
      if (h && h.id !== s.id) return json({ ok: false, error: "This reservation lapsed and another vendor now holds the position. Refund or offer another position." }, 409);
      paidThrough = addMonth(now());
    } else if (s.status === "active" || s.status === "expired") {
      const h = await holder(env, s.category, s.position);
      if (h && h.id !== s.id) return json({ ok: false, error: "This position ended and another vendor now holds it. Refund or offer another position." }, 409);
      paidThrough = addMonth(later(s.paid_through, now()));
    } else return json({ ok: false, error: "This reservation was cancelled." }, 400);
    await env.DB.batch([
      env.DB.prepare("UPDATE invoices SET status = 'paid', provider_ref = ?, updated_at = ? WHERE id = ?").bind(oneLine(body.ref, 120) || null, now(), inv.id),
      env.DB.prepare("UPDATE slots SET status = 'active', paid_through = ?, updated_at = ? WHERE id = ?").bind(paidThrough, now(), s.id),
    ]);
    placementCache.clear();
    return json({ ok: true, paid_through: paidThrough });
  }
  m = path.match(/^\/api\/admin\/slots\/(\d+)\/end$/);
  if (m && method === "POST") {
    await env.DB.prepare("UPDATE slots SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(now(), Number(m[1])).run();
    placementCache.clear();
    return json({ ok: true });
  }
  return json({ ok: false, error: "Not found." }, 404);
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
async function sponsors(env, category) {
  const hit = placementCache.get(category);
  if (hit && hit.t > Date.now() - 60e3) return hit.v;
  const v = (await env.DB.prepare(`SELECT l.*, s.position FROM slots s JOIN listings l ON l.id = s.listing_id JOIN vendors v ON v.id = s.vendor_id
    WHERE s.category = ? AND s.status = 'active' AND s.paid_through > ? AND l.status = 'approved' AND l.active = 1 AND v.status = 'active'
    ORDER BY s.position ASC`).bind(category, now()).all()).results;
  placementCache.set(category, { t: Date.now(), v });
  return v;
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
  try { await migrate(env); partners = await sponsors(env, slug); } catch { return response; }
  if (!partners.length) return response;
  let html = await response.text();
  const path = url.pathname;

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
