// Vettlo vendor portal client: login, dashboard and admin screens. No framework; talks to /api/*.
(function () {
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const money = (c) => "$" + (Number(c || 0) / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const api = async (path, opts = {}) => {
    const r = await fetch(path, { method: opts.method || "GET", credentials: "same-origin",
      headers: { "content-type": "application/json", "x-requested-with": "vettlo" }, body: opts.body ? JSON.stringify(opts.body) : undefined });
    const data = await r.json().catch(() => ({ ok: false, error: "Unexpected response." }));
    if (data.auth) { location.href = "/vendors/login/"; throw new Error("auth"); }
    return data;
  };
  const toast = (msg, bad) => { const t = $("#pt-toast"); if (!t) return; t.textContent = msg; t.className = "pt-toast show" + (bad ? " bad" : ""); setTimeout(() => (t.className = "pt-toast"), 3500); };
  let CATS = [];
  const catName = (slug) => (CATS.find((c) => c.slug === slug) || {}).name || slug;

  // ---------- login / signup
  async function initLogin() {
    const f = $("#pt-login"), msg = $("#pt-login-msg"), extra = $("#pt-signup");
    if (new URLSearchParams(location.search).get("expired")) msg.textContent = "That link has expired or was already used. Request a new one.";
    $("#pt-new").addEventListener("click", (e) => { e.preventDefault(); extra.hidden = false; f.dataset.signup = "1"; $("#pt-submit").textContent = "Create account and send link"; });
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      msg.textContent = "Sending…";
      const body = { email: f.email.value, website_hp: f.website_hp.value };
      if (f.dataset.signup) Object.assign(body, { signup: true, company: f.company.value, website: f.website.value, accept_terms: f.accept.checked });
      const r = await api("/api/auth/request", { method: "POST", body }).catch(() => ({ ok: false, error: "Network error." }));
      if (r.ok) { f.hidden = true; msg.innerHTML = `<b>Check your inbox.</b> We sent a sign-in link to ${esc(body.email)}. It expires in 20 minutes.`; }
      else { msg.textContent = r.error || "Something went wrong."; if (r.needs_signup) { extra.hidden = false; f.dataset.signup = "1"; $("#pt-submit").textContent = "Create account and send link"; } }
    });
  }

  // ---------- vendor dashboard
  let ME = null;
  const date = (iso) => iso ? new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : "";
  const ord = (n) => ["1st", "2nd", "3rd"][n - 1] || n + "th";
  async function initApp() {
    const me = await api("/api/me");
    if (!me.ok) return;
    ME = me;
    CATS = (await api("/api/categories")).categories || [];
    $("#pt-company").textContent = me.vendor.company || me.vendor.email;
    if (me.vendor.is_admin) $("#pt-admin-link").hidden = false;
    $("#pt-logout").addEventListener("click", async () => { await api("/api/logout", { method: "POST" }); location.href = "/vendors/"; });
    document.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => showTab(b.dataset.tab)));
    showTab(location.hash.slice(1) || "overview");
  }
  function showTab(name, arg) {
    document.querySelectorAll("[data-tab]").forEach((b) => b.classList.toggle("on", b.dataset.tab === name));
    history.replaceState(null, "", "#" + name);
    ({ overview, listings, placements, newListing, invoices, reports, account }[name] || overview)(arg);
  }
  const view = (html) => { $("#pt-view").innerHTML = html; };
  function bindGo() { document.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); showTab(a.dataset.go, a.dataset.arg); })); }
  const statusPill = (l) => `<span class="pt-pill ${l.status === "approved" ? (l.active ? "ok" : "off") : l.status}">${l.status === "approved" ? (l.active ? "Approved" : "Paused") : l.status === "pending" ? "In review" : "Not approved"}</span>`;
  const slotText = (s) => !s ? `<span class="muted">No position</span>` : s.status === "active" ? `<b>${ord(s.position)} place</b> until ${date(s.paid_through)}` : `${ord(s.position)} place reserved, awaiting payment (until ${date(s.reserved_until)})`;

  async function overview() {
    const [ls, inv] = await Promise.all([api("/api/listings"), api("/api/invoices")]);
    const L = ls.listings || [], I = (inv.rows || []).filter((x) => x.status === "requested");
    const live = L.filter((l) => l.slot && l.slot.status === "active");
    view(`<div class="pt-stats">
      <div><span>Live positions</span><b>${live.length}</b><small>${L.filter((l) => l.slot && l.slot.status === "reserved").length} awaiting payment</small></div>
      <div><span>Impressions, 30 days</span><b>${L.reduce((a, l) => a + l.impressions_30d, 0).toLocaleString()}</b><small>Views of shortlists showing your product</small></div>
      <div><span>Visits, 30 days</span><b>${L.reduce((a, l) => a + l.clicks_30d, 0).toLocaleString()}</b><small>Unique clicks to your site</small></div>
      <div><span>Open invoices</span><b>${I.length}</b><small>${I.length ? money(I.reduce((a, x) => a + x.amount_cents, 0)) + " due" : "Nothing due"}</small></div></div>
      ${L.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Product</th><th>Category</th><th>Status</th><th>Position</th><th>Impressions (30d)</th><th>Visits (30d)</th><th></th></tr></thead><tbody>
        ${L.map((l) => `<tr><td><b>${esc(l.product_name)}</b></td><td><a href="/tools/${esc(l.category)}/" target="_blank">${esc(catName(l.category))}</a></td><td>${statusPill(l)}</td><td>${slotText(l.slot)}</td><td>${l.impressions_30d}</td><td>${l.clicks_30d}</td>
        <td><a href="#placements" data-go="placements" data-arg="${l.id}">${l.slot ? "Manage" : "Get a position"}</a></td></tr>`).join("")}</tbody></table></div>`
      : `<div class="pt-empty"><h3>Get your product in front of buyers</h3><p>Create a listing for your product, then reserve one of the top three positions on its category shortlist for a flat monthly price.</p><button class="btn" data-go="newListing">Create a listing</button></div>`}`);
    bindGo();
  }

  async function listings() {
    const L = (await api("/api/listings")).listings || [];
    view(`<div class="pt-head"><h2>Listings</h2><button class="btn small" data-go="newListing">New listing</button></div>
      ${L.length ? L.map((l) => `<form class="pt-card" data-id="${l.id}">
        <div class="pt-card-head"><div><h3>${esc(l.product_name)}</h3><p class="muted small">${esc(catName(l.category))} · ${statusPill(l)} · ${slotText(l.slot)}${l.review_note ? " · " + esc(l.review_note) : ""}</p></div>
        <label class="pt-switch"><input type="checkbox" name="active" ${l.active ? "checked" : ""}> Show on site</label></div>
        <div class="pt-grid">
          <label>Landing page<input name="landing_url" type="url" value="${esc(l.landing_url)}"><small>Add UTM parameters to track Vettlo traffic.</small></label>
          <label>Starting price<input name="starting_price" maxlength="80" value="${esc(l.starting_price || "")}"></label>
          <label class="wide">Best for (one line)<input name="best_for" maxlength="90" value="${esc(l.best_for || "")}"></label>
          <label class="wide">Description<textarea name="description" rows="3" maxlength="600">${esc(l.description || "")}</textarea><small>Changing the description, best-for line or price sends the listing back to editorial review.</small></label>
        </div><div class="pt-actions"><button class="btn small" type="submit">Save</button><a class="small" href="#placements" data-go="placements" data-arg="${l.id}">${l.slot ? "Manage position" : "Get a position"} →</a></div></form>`).join("")
      : `<div class="pt-empty"><p>No listings yet.</p><button class="btn" data-go="newListing">Create a listing</button></div>`}`);
    bindGo();
    document.querySelectorAll("form.pt-card").forEach((f) => f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const r = await api(`/api/listings/${f.dataset.id}`, { method: "PUT", body: { active: f.active.checked, landing_url: f.landing_url.value,
        best_for: f.best_for.value, starting_price: f.starting_price.value, description: f.description.value } });
      toast(r.ok ? (r.resubmitted ? "Saved. Copy changes are back in editorial review." : "Saved.") : r.error, !r.ok);
      if (r.ok) listings();
    }));
  }

  async function placements(listingId) {
    const L = ((await api("/api/listings")).listings || []).filter((l) => l.status !== "rejected");
    if (!L.length) { view(`<div class="pt-empty"><p>Create a listing first, then choose a position.</p><button class="btn" data-go="newListing">Create a listing</button></div>`); return bindGo(); }
    const cur = L.find((l) => String(l.id) === String(listingId)) || L[0];
    const P = (await api("/api/positions?category=" + encodeURIComponent(cur.category))).positions || [];
    const card = (p) => {
      let action = "", note = "";
      if (p.state === "available") action = cur.slot ? `<span class="muted small">This listing already holds a position.</span>` : `<button class="btn small" data-reserve="${p.position}">Reserve for ${money(p.price_cents)}/mo</button>`;
      else if (p.state === "yours") { note = `Yours until ${date(p.until)}`; action = `<button class="btn small" data-renew="${p.slot_id}">Renew 1 month</button>`; }
      else if (p.state === "reserved_by_you") { note = `Reserved for you until ${date(p.until)}. Pay the invoice to go live.`; action = `<button class="btn ghost small" data-cancel="${p.slot_id}">Cancel reservation</button>`; }
      else if (p.state === "taken" || p.state === "priority_other") { note = p.state === "taken" ? `Taken until ${date(p.until)}` : `Offered to the next vendor on the waitlist until ${date(p.until)}`;
        action = p.on_waitlist ? `<button class="btn ghost small" data-leave="${p.position}">Leave waitlist</button>` : `<button class="btn ghost small" data-wait="${p.position}">Join waitlist</button>`; }
      return `<div class="pt-slot ${p.state}"><span class="pt-slot-n">${ord(p.position)}</span><div><b>${ord(p.position)} place on the shortlist</b><span class="muted small">${money(p.price_cents)} per month${p.waitlist ? " · " + p.waitlist + " on waitlist" : ""}</span>${note ? `<span class="small">${note}</span>` : ""}</div>${action}</div>`;
    };
    view(`<div class="pt-head"><h2>Positions</h2>${L.length > 1 ? `<select id="pt-pick">${L.map((l) => `<option value="${l.id}" ${l.id === cur.id ? "selected" : ""}>${esc(l.product_name)} · ${esc(catName(l.category))}</option>`).join("")}</select>` : ""}</div>
      <p class="muted">Positions on the <a href="/tools/${esc(cur.category)}/" target="_blank">${esc(catName(cur.category))}</a> shortlist for <b>${esc(cur.product_name)}</b>. Each position is a flat monthly price. Your product appears there while the month is paid and the listing is approved.${cur.status === "pending" ? " <b>This listing is still in editorial review</b>; you can reserve now and it goes live once approved." : ""}</p>
      <div class="pt-slots">${P.map(card).join("")}</div>
      <p class="muted small">A reservation holds the position for 7 days while you pay the invoice. When a position frees up, the first vendor on its waitlist gets 72 hours to claim it. Scores and review text are never part of what you buy.</p>`);
    bindGo();
    const pick = $("#pt-pick"); if (pick) pick.addEventListener("change", () => placements(pick.value));
    const act = async (url, body, okMsg) => { const r = await api(url, { method: "POST", body }); toast(r.ok ? okMsg(r) : r.error, !r.ok); placements(cur.id); };
    document.querySelectorAll("[data-reserve]").forEach((b) => b.addEventListener("click", () => act("/api/slots", { listing_id: cur.id, position: Number(b.dataset.reserve) }, () => "Reserved. We'll email your invoice; the position goes live when it's paid.")));
    document.querySelectorAll("[data-renew]").forEach((b) => b.addEventListener("click", () => act(`/api/slots/${b.dataset.renew}/renew`, {}, () => "Renewal invoice requested.")));
    document.querySelectorAll("[data-cancel]").forEach((b) => b.addEventListener("click", () => act(`/api/slots/${b.dataset.cancel}/cancel`, {}, () => "Reservation cancelled.")));
    document.querySelectorAll("[data-wait]").forEach((b) => b.addEventListener("click", () => act("/api/waitlist", { listing_id: cur.id, position: Number(b.dataset.wait) }, () => "You're on the waitlist.")));
    document.querySelectorAll("[data-leave]").forEach((b) => b.addEventListener("click", () => act("/api/waitlist/leave", { category: cur.category, position: Number(b.dataset.leave) }, () => "Removed from the waitlist.")));
  }

  function newListing() {
    const opts = CATS.map((c) => `<option value="${esc(c.slug)}">${esc(c.dept)} · ${esc(c.name)}</option>`).join("");
    view(`<div class="pt-head"><h2>New listing</h2></div><form class="pt-card" id="pt-new-form"><div class="pt-grid">
      <label>Product name<input name="product_name" required maxlength="80"></label>
      <label>Category<select name="category" required><option value="">Choose…</option>${opts}</select></label>
      <label>Product website<input name="website" type="url" required placeholder="https://"></label>
      <label>Landing page<input name="landing_url" type="url" placeholder="https:// (optional, defaults to website)"></label>
      <label>Best for (one line)<input name="best_for" maxlength="90" placeholder="e.g. Small teams that want simple pipelines"></label>
      <label>Starting price<input name="starting_price" maxlength="80" placeholder="e.g. $12/user/mo billed annually"></label>
      <label class="wide">Description<textarea name="description" rows="3" maxlength="600" placeholder="What the product does and who it's for. Plain and factual; our editors may edit it."></textarea></label>
      </div><div class="pt-actions"><button class="btn" type="submit">Submit and choose a position</button><span class="muted small">Editorial review usually takes 1–2 business days.</span></div></form>`);
    $("#pt-new-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target;
      const r = await api("/api/listings", { method: "POST", body: { product_name: f.product_name.value, category: f.category.value, website: f.website.value,
        landing_url: f.landing_url.value || f.website.value, best_for: f.best_for.value, starting_price: f.starting_price.value, description: f.description.value } });
      toast(r.ok ? "Submitted for review." : r.error, !r.ok);
      if (r.ok) showTab("placements", r.id);
    });
  }

  async function invoices() {
    const rows = (await api("/api/invoices")).rows || [];
    view(`<div class="pt-head"><h2>Invoices</h2></div>
      <p class="muted">${ME.payments === "iyzico" ? "Pay open invoices by card through iyzico." : "We email an invoice for each reservation and renewal. Your position goes live, or is extended by a month, as soon as payment arrives."}</p>
      ${rows.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Date</th><th>For</th><th>Amount</th><th>Status</th></tr></thead><tbody>
      ${rows.map((x) => `<tr><td>${date(x.created_at)}</td><td>${x.position ? `${esc(x.product_name)}, ${ord(x.position)} place in ${esc(catName(x.category))}, 1 month` : "Adjustment"}</td><td>${money(x.amount_cents)}</td><td><span class="pt-pill ${x.status === "paid" ? "ok" : x.status === "requested" ? "pending" : "off"}">${x.status === "requested" ? "Due" : x.status === "paid" ? "Paid" : "Cancelled"}</span></td></tr>`).join("")}</tbody></table></div>`
      : `<p class="muted">No invoices yet.</p>`}`);
  }

  async function reports() {
    const rows = (await api("/api/reports?days=30")).rows || [];
    view(`<div class="pt-head"><h2>Reports</h2><span class="muted small">Last 30 days. Impressions are views of a shortlist showing your product; visits are unique clicks to your site (repeat clicks within 24 hours and bots aren't counted).</span></div>
      ${rows.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Day</th><th>Product</th><th>Category</th><th>Impressions</th><th>Visits</th><th>Click rate</th></tr></thead><tbody>
      ${rows.map((x) => `<tr><td>${x.day}</td><td>${esc(x.product_name)}</td><td>${esc(catName(x.category))}</td><td>${x.impressions}</td><td>${x.clicks}</td><td>${x.impressions ? ((x.clicks / x.impressions) * 100).toFixed(1) + "%" : "—"}</td></tr>`).join("")}</tbody></table></div>
      <p><a class="btn ghost small" id="pt-csv" href="#">Download CSV</a></p>` : `<div class="pt-empty"><p>No data yet. Numbers appear here once your product is live on a shortlist.</p></div>`}`);
    const c = $("#pt-csv");
    if (c) c.addEventListener("click", (e) => { e.preventDefault(); const csv = "day,product,category,impressions,visits\n" + rows.map((x) => [x.day, `"${x.product_name.replace(/"/g, '""')}"`, x.category, x.impressions, x.clicks].join(",")).join("\n");
      const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" })); a.download = "vettlo-report.csv"; a.click(); });
  }

  async function account() {
    const me = await api("/api/me"); const v = me.vendor;
    view(`<div class="pt-head"><h2>Account</h2></div><form class="pt-card" id="pt-acct"><div class="pt-grid">
      <label>Company<input name="company" value="${esc(v.company || "")}"></label>
      <label>Website<input name="website" type="url" value="${esc(v.website || "")}"></label>
      <label>Sign-in email<input value="${esc(v.email)}" disabled></label></div>
      <div class="pt-actions"><button class="btn small" type="submit">Save</button><a class="small" href="/advertiser-terms/" target="_blank">Advertiser terms</a></div></form>`);
    $("#pt-acct").addEventListener("submit", async (e) => {
      e.preventDefault(); const f = e.target;
      const r = await api("/api/me", { method: "PUT", body: { company: f.company.value, website: f.website.value } });
      toast(r.ok ? "Saved." : r.error, !r.ok);
    });
  }

  // ---------- admin
  async function initAdmin() {
    const me = await api("/api/me");
    if (!me.ok || !me.vendor.is_admin) { $("#pt-view").innerHTML = "<p>Admins only.</p>"; return; }
    CATS = (await api("/api/categories")).categories || [];
    renderAdmin();
  }
  async function renderAdmin() {
    const d = await api("/api/admin/overview");
    const D = (iso) => iso ? iso.slice(0, 10) : "";
    const toolOpts = (slug, cur) => `<option value="">Not on our list</option>` + ((CATS.find((c) => c.slug === slug) || {}).tools || []).map((t) => `<option value="${esc(t.id)}" ${t.id === cur ? "selected" : ""}>${esc(t.name)}</option>`).join("");
    $("#pt-view").innerHTML = `
      <h2>Invoices</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Date</th><th>Vendor</th><th>For</th><th>Amount</th><th>Status</th><th></th></tr></thead><tbody>
      ${d.invoices.map((i) => `<tr data-iid="${i.id}"><td>${D(i.created_at)}</td><td>${esc(i.company)}<br><small>${esc(i.email)}</small></td><td>${i.position ? `${esc(i.product_name)} · #${i.position} · ${esc(catName(i.category))}` : ""}</td><td>${money(i.amount_cents)}</td><td>${esc(i.status)}</td>
        <td>${i.status === "requested" ? `<input name="ref" placeholder="Payment ref"><button class="btn small" data-iact="paid">Mark paid</button> <button class="btn ghost small" data-iact="cancelled">Cancel</button>` : esc(i.provider_ref || "")}</td></tr>`).join("") || `<tr><td colspan="6" class="muted">No invoices.</td></tr>`}</tbody></table></div>
      <h2>Listings</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Vendor</th><th>Product</th><th>Category</th><th>Copy</th><th>Matches tool</th><th>Status</th><th></th></tr></thead><tbody>
      ${d.listings.map((l) => `<tr data-id="${l.id}"><td>${esc(l.company)}<br><small>${esc(l.email)}</small></td><td><a href="${esc(l.website)}" target="_blank" rel="noopener">${esc(l.product_name)}</a></td><td>${esc(catName(l.category))}</td>
        <td class="small">${esc(l.best_for || "")}<br>${esc(l.description || "")}<br>${esc(l.starting_price || "")}</td><td><select name="tool">${toolOpts(l.category, l.tool_id)}</select></td><td>${esc(l.status)}</td>
        <td><input name="note" placeholder="Note to vendor" value="${esc(l.review_note || "")}"><button class="btn small" data-act="approved">Approve</button> <button class="btn ghost small" data-act="rejected">Reject</button></td></tr>`).join("") || `<tr><td colspan="7" class="muted">No listings.</td></tr>`}</tbody></table></div>
      <h2>Positions</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Category</th><th>#</th><th>Product</th><th>Vendor</th><th>Status</th><th>Until</th><th></th></tr></thead><tbody>
      ${d.slots.map((s) => `<tr data-sid="${s.id}"><td>${esc(catName(s.category))}</td><td>${s.position}</td><td>${esc(s.product_name)}${s.listing_status !== "approved" ? ` <small>(listing ${esc(s.listing_status)})</small>` : ""}</td><td>${esc(s.company)}</td><td>${s.status === "active" ? "Live" : "Reserved, unpaid"}</td><td>${D(s.status === "active" ? s.paid_through : s.reserved_until)}</td><td><button class="btn ghost small" data-sact="end">End now</button></td></tr>`).join("") || `<tr><td colspan="7" class="muted">No positions sold yet.</td></tr>`}</tbody></table></div>
      <h2>Waitlist</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Category</th><th>#</th><th>Product</th><th>Vendor</th><th>Joined</th></tr></thead><tbody>
      ${d.waitlist.map((w) => `<tr><td>${esc(catName(w.category))}</td><td>${w.position}</td><td>${esc(w.product_name)}</td><td>${esc(w.company)}</td><td>${D(w.created_at)}</td></tr>`).join("") || `<tr><td colspan="5" class="muted">Empty.</td></tr>`}</tbody></table></div>
      <h2>Vendors</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Company</th><th>Email</th><th>Website</th><th>Joined</th></tr></thead><tbody>
      ${d.vendors.map((v) => `<tr><td>${esc(v.company || "")}</td><td>${esc(v.email)}</td><td>${esc(v.website || "")}</td><td>${D(v.created_at)}</td></tr>`).join("")}</tbody></table></div>
      <h2>Sponsor traffic, last 30 days</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Day</th><th>Impressions</th><th>Visits</th></tr></thead><tbody>
      ${d.stats.map((c) => `<tr><td>${c.day}</td><td>${c.impressions}</td><td>${c.clicks}</td></tr>`).join("") || `<tr><td colspan="3" class="muted">No data yet.</td></tr>`}</tbody></table></div>`;
    const post = async (url, body) => { const r = await api(url, { method: "POST", body }); toast(r.ok ? "Saved." : r.error, !r.ok); renderAdmin(); };
    document.querySelectorAll("[data-act]").forEach((b) => b.addEventListener("click", () => { const tr = b.closest("tr"); post(`/api/admin/listings/${tr.dataset.id}`, { status: b.dataset.act, tool_id: tr.querySelector("[name=tool]").value, review_note: tr.querySelector("[name=note]").value }); }));
    document.querySelectorAll("[data-iact]").forEach((b) => b.addEventListener("click", () => { const tr = b.closest("tr"); post(`/api/admin/invoices/${tr.dataset.iid}`, { status: b.dataset.iact, ref: tr.querySelector("[name=ref]").value }); }));
    document.querySelectorAll("[data-sact]").forEach((b) => b.addEventListener("click", () => { if (confirm("End this position now? The vendor won't be refunded automatically.")) post(`/api/admin/slots/${b.closest("tr").dataset.sid}/end`, {}); }));
  }

  const mode = document.body.dataset.portal || ($("#pt-root") || {}).dataset?.portal;
  if (mode === "login") initLogin();
  if (mode === "app") initApp();
  if (mode === "admin") initAdmin();
})();
