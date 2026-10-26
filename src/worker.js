// Vettlo Worker: serves the static site and turns form posts into emails.
// Mail goes through Cloudflare Email Routing's send_email binding to the verified
// address stored in the FORM_TO variable (set in the Cloudflare dashboard, not in this repo).
import { EmailMessage } from "cloudflare:email";

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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/form") {
      if (request.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);
      return handleForm(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};
