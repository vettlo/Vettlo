// Vettlo Worker: serves the static site and turns form posts into emails.
// Mail goes through Cloudflare Email Routing's send_email binding to the verified
// address stored in the FORM_TO variable (set in the Cloudflare dashboard, not in this repo).
import { EmailMessage } from "cloudflare:email";
import { handlePortalApi, handleGo, handleCheckoutPage, placeOnShortlist, rateLimited, billingDaily } from "./portal.js";

// Same security headers as public/_headers, added to everything the Worker returns (API, redirects, shortlist pages).
const SECURITY = {
  "x-content-type-options": "nosniff",
  "referrer-policy": "strict-origin-when-cross-origin",
  "x-frame-options": "DENY",
  "strict-transport-security": "max-age=31536000",
  "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()",
  "cross-origin-opener-policy": "same-origin",
};
function secure(res) {
  const r = new Response(res.body, res);
  for (const [k, v] of Object.entries(SECURITY)) if (!r.headers.has(k)) r.headers.set(k, v);
  return r;
}

const FROM = "forms@vettlo.com";
const FIELDS = {
  contact: ["name", "email", "topic", "message"],
  advertise: ["name", "email", "company", "interest", "message"],
};

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

const clean = (v, max) => String(v ?? "").replace(/\r/g, "").trim().slice(0, max);
const oneLine = (v, max) => clean(v, max).replace(/\n/g, " ");
const b64 = (s) => {
  const bytes = new TextEncoder().encode(s);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
};
const wrap = (s) => s.replace(/.{1,76}/g, "$&\r\n");

async function handleForm(request, env) {
  if (!env.FORM_TO || !env.SEND) return json({ ok: false, error: "Form delivery isn't configured yet." }, 503);
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: "Invalid request." }, 400);
  }
  const kind = data.form in FIELDS ? data.form : null;
  if (!kind) return json({ ok: false, error: "Unknown form." }, 400);

  // Spam checks: hidden honeypot field and a minimum time on the page. Bots get a quiet "ok".
  if (clean(data.website, 200) || Number(data.elapsed) < 3000) return json({ ok: true });
  if (await rateLimited(env, request, "form", 10, 600)) return json({ ok: false, error: "Too many messages from your network. Please try again in a few minutes." }, 429);

  const name = oneLine(data.name, 120);
  const email = oneLine(data.email, 200);
  const message = clean(data.message, 5000);
  if (!name || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email)) return json({ ok: false, error: "Please enter your name and a valid email." }, 400);
  if (kind === "contact" && !message) return json({ ok: false, error: "Please write a message." }, 400);

  const lines = FIELDS[kind].map((f) => `${f[0].toUpperCase() + f.slice(1)}: ${f === "message" ? "\n" + (message || "-") : oneLine(data[f], 300) || "-"}`);
  const page = oneLine(request.headers.get("referer"), 300);
  const body = `New ${kind} form submission on vettlo.com\n\n${lines.join("\n")}\n\nPage: ${page || "-"}\nReply to this email to answer ${name}.\n`;
  const subject = `[Vettlo] ${kind === "contact" ? "Contact: " + (oneLine(data.topic, 60) || "Message") : "Advertising inquiry"} from ${name}`;

  const raw = [
    `From: Vettlo Forms <${FROM}>`,
    `To: <${env.FORM_TO}>`,
    `Reply-To: <${email}>`,
    `Subject: =?UTF-8?B?${b64(subject)}?=`,
    `Message-ID: <${crypto.randomUUID()}@vettlo.com>`,
    `Date: ${new Date().toUTCString()}`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "",
    wrap(b64(body)),
  ].join("\r\n");

  try {
    await env.SEND.send(new EmailMessage(FROM, env.FORM_TO, raw));
  } catch (e) {
    return json({ ok: false, error: "We couldn't send your message. Please try again later." }, 502);
  }
  return json({ ok: true });
}

// Retired URLs (merged or removed pages) -> the page that now holds their content. Built into /data/redirects.json.
let REDIRECTS = null, REDIRECTS_AT = 0;
async function redirects(env, request) {
  if (REDIRECTS && Date.now() - REDIRECTS_AT < 300e3) return REDIRECTS;
  try {
    const r = await env.ASSETS.fetch(new Request(new URL("/data/redirects.json", request.url)));
    REDIRECTS = r.ok ? await r.json() : {};
  } catch (e) { REDIRECTS = REDIRECTS || {}; }
  REDIRECTS_AT = Date.now();
  return REDIRECTS;
}

export default {
  async fetch(request, env, ctx) {
    return secure(await route(request, env, ctx));
  },
  // Daily: renewal invoices, vendor reminders and the admin's Payoneer to-do list.
  async scheduled(event, env, ctx) {
    ctx.waitUntil(billingDaily(env));
  },
};

async function route(request, env, ctx) {
  {
    const url = new URL(request.url);
    if (url.pathname === "/api/form") {
      if (request.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);
      return handleForm(request, env);
    }
    if (url.pathname.startsWith("/api/")) return handlePortalApi(request, env, url.pathname);
    if (url.pathname.startsWith("/go/")) return handleGo(request, env, ctx);
    if (url.pathname === "/vendors/checkout/" || url.pathname === "/vendors/checkout") return handleCheckoutPage(request, env); // Paddle default payment link
    if (!/\.[a-z0-9]+$/i.test(url.pathname)) {  // pages only, not assets
      const to = (await redirects(env, request))[url.pathname.endsWith("/") ? url.pathname : url.pathname + "/"];
      if (to) return new Response(null, { status: 301, headers: { location: new URL(to, url).toString() + url.search, "cache-control": "public, max-age=86400" } });
    }
    const res = await env.ASSETS.fetch(request);
    if (url.pathname.startsWith("/tools/")) {
      try { return await placeOnShortlist(request, env, res, ctx); } catch (e) { return res; }
    }
    return res;
  }
}
