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
  function showTab(name) {
    document.querySelectorAll("[data-tab]").forEach((b) => b.classList.toggle("on", b.dataset.tab === name));
    history.replaceState(null, "", "#" + name);
    ({ overview, listings, newListing, reports, funds, account }[name] || overview)();
  }
  const view = (html) => { $("#pt-view").innerHTML = html; };

  async function overview() {
    const [me, ls] = await Promise.all([api("/api/me"), api("/api/listings")]);
    const v = me.vendor, L = ls.listings || [];
    const clicks = L.reduce((a, l) => a + l.billable_30d, 0), cost = L.reduce((a, l) => a + l.cost_30d_cents, 0);
    view(`<div class="pt-stats">
      <div><span>Balance</span><b>${money(v.balance_cents)}</b><a href="#funds" data-go="funds">Add funds →</a></div>
      <div><span>Spent this month</span><b>${money(v.month_spend_cents)}</b><small>${v.monthly_budget_cents ? "of " + money(v.monthly_budget_cents) + " budget" : "No monthly cap"}</small></div>
      <div><span>Paid clicks, 30 days</span><b>${clicks}</b><small>${money(cost)} spent</small></div>
      <div><span>Live listings</span><b>${L.filter((l) => l.status === "approved" && l.active).length}</b><small>${L.filter((l) => l.status === "pending").length} in review</small></div></div>
      ${v.balance_cents <= 0 ? `<div class="pt-note">Your listings show only while your balance covers your bid. <a href="#funds" data-go="funds">Add funds</a> to go live.</div>` : ""}
      ${L.length ? listingTable(L) : `<div class="pt-empty"><h3>Get your product in front of buyers</h3><p>Create a listing, choose a category and set your bid. Our editors review new listings within 1–2 business days.</p><button class="btn" data-go="newListing">Create a listing</button></div>`}`);
    bindGo();
  }
  const statusPill = (l) => `<span class="pt-pill ${l.status === "approved" ? (l.active ? "ok" : "off") : l.status}">${l.status === "approved" ? (l.active ? "Live" : "Paused") : l.status === "pending" ? "In review" : "Not approved"}</span>`;
  const listingTable = (L) => `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Product</th><th>Category</th><th>Status</th><th>Your bid</th><th>Top bid</th><th>Est. position</th><th>Clicks (30d)</th><th>Cost (30d)</th></tr></thead><tbody>
    ${L.map((l) => `<tr><td><b>${esc(l.product_name)}</b></td><td><a href="/tools/${esc(l.category)}/" target="_blank">${esc(catName(l.category))}</a></td><td>${statusPill(l)}</td><td>${money(l.bid_cents)}</td><td>${money(l.top_bid_cents)}</td><td>#${l.position}</td><td>${l.billable_30d}</td><td>${money(l.cost_30d_cents)}</td></tr>`).join("")}</tbody></table></div>`;
  function bindGo() { document.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); showTab(a.dataset.go); })); }

  async function listings() {
    const ls = await api("/api/listings");
    const L = ls.listings || [];
    view(`<div class="pt-head"><h2>Listings</h2><button class="btn small" data-go="newListing">New listing</button></div>
      ${L.length ? L.map((l) => `<form class="pt-card" data-id="${l.id}">
        <div class="pt-card-head"><div><h3>${esc(l.product_name)}</h3><p class="muted small">${esc(catName(l.category))} · ${statusPill(l)}${l.review_note ? " · " + esc(l.review_note) : ""}</p></div>
        <label class="pt-switch"><input type="checkbox" name="active" ${l.active ? "checked" : ""}> Active</label></div>
        <div class="pt-grid">
          <label>Bid per click (USD)<input name="bid" type="number" min="${ME.min_bid_cents / 100}" step="${ME.bid_step_cents / 100}" value="${(l.bid_cents / 100).toFixed(2)}"><small>Top bid in this category: ${money(l.top_bid_cents)} · estimated position #${l.position}. Minimum ${money(ME.min_bid_cents)}, steps of ${money(ME.bid_step_cents)}.</small></label>
          <label>Landing page<input name="landing_url" type="url" value="${esc(l.landing_url)}"><small>Add UTM parameters to track Vettlo traffic.</small></label>
          <label>Best for (one line)<input name="best_for" maxlength="90" value="${esc(l.best_for || "")}"></label>
          <label>Starting price<input name="starting_price" maxlength="80" value="${esc(l.starting_price || "")}"></label>
          <label class="wide">Description<textarea name="description" rows="3" maxlength="600">${esc(l.description || "")}</textarea><small>Changing the description, best-for line or price sends the listing back to editorial review.</small></label>
        </div><div class="pt-actions"><button class="btn small" type="submit">Save</button><span class="muted small">${l.billable_30d} paid clicks and ${money(l.cost_30d_cents)} in the last 30 days</span></div></form>`).join("")
      : `<div class="pt-empty"><p>No listings yet.</p><button class="btn" data-go="newListing">Create a listing</button></div>`}`);
    bindGo();
    document.querySelectorAll("form.pt-card").forEach((f) => f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const r = await api(`/api/listings/${f.dataset.id}`, { method: "PUT", body: { bid_cents: Math.round(Number(f.bid.value) * 100), active: f.active.checked,
        landing_url: f.landing_url.value, best_for: f.best_for.value, starting_price: f.starting_price.value, description: f.description.value } });
      toast(r.ok ? (r.resubmitted ? "Saved. Copy changes are back in editorial review." : "Saved.") : r.error, !r.ok);
      if (r.ok) listings();
    }));
  }

  function newListing() {
    const opts = CATS.map((c) => `<option value="${esc(c.slug)}">${esc(c.dept)} · ${esc(c.name)}</option>`).join("");
    view(`<div class="pt-head"><h2>New listing</h2></div><form class="pt-card" id="pt-new-form"><div class="pt-grid">
      <label>Product name<input name="product_name" required maxlength="80"></label>
      <label>Category<select name="category" required><option value="">Choose…</option>${opts}</select></label>
      <label>Product website<input name="website" type="url" required placeholder="https://"></label>
      <label>Landing page<input name="landing_url" type="url" placeholder="https:// (optional, defaults to website)"></label>
      <label>Best for (one line)<input name="best_for" maxlength="90" placeholder="e.g. Best for small teams that want simple pipelines"></label>
      <label>Starting price<input name="starting_price" maxlength="80" placeholder="e.g. $12/user/mo billed annually"></label>
      <label class="wide">Description<textarea name="description" rows="3" maxlength="600" placeholder="What the product does and who it's for. Plain and factual; our editors may edit it."></textarea></label>
      <label>Bid per click (USD)<input name="bid" type="number" min="${ME.min_bid_cents / 100}" step="${ME.bid_step_cents / 100}" value="${(ME.min_bid_cents / 100).toFixed(2)}"><small>Minimum ${money(ME.min_bid_cents)}. The highest bids appear first in the category.</small></label>
      </div><div class="pt-actions"><button class="btn" type="submit">Submit for review</button><span class="muted small">Editorial review usually takes 1–2 business days.</span></div></form>`);
    $("#pt-new-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target;
      const r = await api("/api/listings", { method: "POST", body: { product_name: f.product_name.value, category: f.category.value, website: f.website.value,
        landing_url: f.landing_url.value || f.website.value, best_for: f.best_for.value, starting_price: f.starting_price.value, description: f.description.value,
        bid_cents: Math.round(Number(f.bid.value) * 100) } });
      toast(r.ok ? "Submitted for review." : r.error, !r.ok);
      if (r.ok) showTab("listings");
    });
  }

  async function reports() {
    const r = await api("/api/reports?days=30");
    const rows = r.rows || [];
    view(`<div class="pt-head"><h2>Reports</h2><span class="muted small">Last 30 days. Only paid clicks are billed: repeat clicks from the same visitor within 24 hours, bots and clicks over budget are free.</span></div>
      ${rows.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Day</th><th>Product</th><th>Category</th><th>Clicks</th><th>Paid clicks</th><th>Cost</th></tr></thead><tbody>
      ${rows.map((x) => `<tr><td>${x.day}</td><td>${esc(x.product_name)}</td><td>${esc(catName(x.category))}</td><td>${x.clicks}</td><td>${x.billable}</td><td>${money(x.cost_cents)}</td></tr>`).join("")}</tbody></table></div>
      <p><a class="btn ghost small" id="pt-csv" href="#">Download CSV</a></p>` : `<div class="pt-empty"><p>No clicks yet. Clicks appear here within a minute.</p></div>`}`);
    const c = $("#pt-csv");
    if (c) c.addEventListener("click", (e) => { e.preventDefault(); const csv = "day,product,category,clicks,paid_clicks,cost_usd\n" + rows.map((x) => [x.day, `"${x.product_name.replace(/"/g, '""')}"`, x.category, x.clicks, x.billable, (x.cost_cents / 100).toFixed(2)].join(",")).join("\n");
      const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" })); a.download = "vettlo-clicks.csv"; a.click(); });
  }

  async function funds() {
    const [me, r] = await Promise.all([api("/api/me"), api("/api/funds")]);
    const rows = r.rows || [];
    view(`<div class="pt-head"><h2>Funds</h2><span class="pt-balance">Balance <b>${money(me.vendor.balance_cents)}</b></span></div>
      <form class="pt-card" id="pt-fund"><h3>Add funds</h3><div class="pt-amounts">${[250, 500, 1000, 2500].map((a, i) => `<label><input type="radio" name="amt" value="${a}" ${i === 1 ? "checked" : ""}> $${a.toLocaleString()}</label>`).join("")}
      <label>Other <input name="other" type="number" min="50" step="10" placeholder="USD"></label></div>
      <div class="pt-actions"><button class="btn" type="submit">${me.payments === "iyzico" ? "Continue to payment" : "Request invoice"}</button>
      <span class="muted small">${me.payments === "iyzico" ? "Card payments are processed by iyzico." : "We'll email an invoice. Your balance is credited when payment arrives."} Funds don't expire.</span></div></form>
      <h3 style="margin-top:2rem">History</h3>${rows.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Date</th><th>Type</th><th>Amount</th><th>Status</th></tr></thead><tbody>
      ${rows.map((x) => `<tr><td>${x.created_at.slice(0, 10)}</td><td>${x.kind === "topup" ? "Top-up" : "Adjustment"}</td><td>${money(x.amount_cents)}</td><td>${esc(x.status)}</td></tr>`).join("")}</tbody></table></div>` : `<p class="muted">No transactions yet.</p>`}`);
    $("#pt-fund").addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target; const amt = Number(f.other.value) || Number(f.querySelector("input[name=amt]:checked").value);
      const res = await api("/api/funds", { method: "POST", body: { amount_cents: Math.round(amt * 100) } });
      toast(res.ok ? (res.method === "iyzico" ? "Redirecting to payment…" : "Invoice requested. We'll email it shortly.") : res.error, !res.ok);
      if (res.ok) funds();
    });
  }

  async function account() {
    const me = await api("/api/me"); const v = me.vendor;
    view(`<div class="pt-head"><h2>Account</h2></div><form class="pt-card" id="pt-acct"><div class="pt-grid">
      <label>Company<input name="company" value="${esc(v.company || "")}"></label>
      <label>Website<input name="website" type="url" value="${esc(v.website || "")}"></label>
      <label>Monthly budget cap (USD)<input name="budget" type="number" min="0" step="10" value="${v.monthly_budget_cents ? v.monthly_budget_cents / 100 : ""}" placeholder="No cap"><small>When you reach the cap, your listings pause until the next month.</small></label>
      <label>Sign-in email<input value="${esc(v.email)}" disabled></label></div>
      <div class="pt-actions"><button class="btn small" type="submit">Save</button><a class="small" href="/advertiser-terms/" target="_blank">Advertiser terms</a></div></form>`);
    $("#pt-acct").addEventListener("submit", async (e) => {
      e.preventDefault(); const f = e.target;
      const r = await api("/api/me", { method: "PUT", body: { company: f.company.value, website: f.website.value, monthly_budget_cents: f.budget.value === "" ? null : Math.round(Number(f.budget.value) * 100) } });
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
    const toolOpts = (slug, cur) => `<option value="">Not on our list</option>` + ((CATS.find((c) => c.slug === slug) || {}).tools || []).map((t) => `<option value="${esc(t.id)}" ${t.id === cur ? "selected" : ""}>${esc(t.name)}</option>`).join("");
    $("#pt-view").innerHTML = `
      <h2>Listings</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Vendor</th><th>Product</th><th>Category</th><th>Bid</th><th>Copy</th><th>Matches tool</th><th>Status</th><th></th></tr></thead><tbody>
      ${d.listings.map((l) => `<tr data-id="${l.id}"><td>${esc(l.company)}<br><small>${esc(l.email)}</small></td><td><a href="${esc(l.website)}" target="_blank" rel="noopener">${esc(l.product_name)}</a></td><td>${esc(catName(l.category))}</td><td>${money(l.bid_cents)}</td>
        <td class="small">${esc(l.best_for || "")}<br>${esc(l.description || "")}<br>${esc(l.starting_price || "")}</td><td><select name="tool">${toolOpts(l.category, l.tool_id)}</select></td><td>${esc(l.status)}</td>
        <td><input name="note" placeholder="Note to vendor" value="${esc(l.review_note || "")}"><button class="btn small" data-act="approved">Approve</button> <button class="btn ghost small" data-act="rejected">Reject</button></td></tr>`).join("")}</tbody></table></div>
      <h2>Funds</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Date</th><th>Vendor</th><th>Amount</th><th>Status</th><th></th></tr></thead><tbody>
      ${d.funds.map((f) => `<tr data-fid="${f.id}"><td>${f.created_at.slice(0, 10)}</td><td>${esc(f.company)} · ${esc(f.email)}</td><td>${money(f.amount_cents)}</td><td>${esc(f.status)}</td><td>${f.status === "requested" ? `<input name="ref" placeholder="Payment ref"><button class="btn small" data-fact="paid">Mark paid</button> <button class="btn ghost small" data-fact="cancelled">Cancel</button>` : ""}</td></tr>`).join("")}</tbody></table></div>
      <h2>Vendors</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Company</th><th>Email</th><th>Balance</th><th>Budget</th><th>Adjust balance</th></tr></thead><tbody>
      ${d.vendors.map((v) => `<tr data-vid="${v.id}"><td>${esc(v.company || "")}</td><td>${esc(v.email)}</td><td>${money(v.balance_cents)}</td><td>${v.monthly_budget_cents ? money(v.monthly_budget_cents) : "—"}</td><td><input name="amt" type="number" step="1" placeholder="USD (+/-)"><input name="note" placeholder="Note"><button class="btn small" data-vact="credit">Apply</button></td></tr>`).join("")}</tbody></table></div>
      <h2>Clicks, last 30 days</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Day</th><th>Clicks</th><th>Paid</th><th>Revenue</th></tr></thead><tbody>
      ${d.clicks.map((c) => `<tr><td>${c.day}</td><td>${c.clicks}</td><td>${c.billable}</td><td>${money(c.cost_cents)}</td></tr>`).join("")}</tbody></table></div>`;
    document.querySelectorAll("[data-act]").forEach((b) => b.addEventListener("click", async () => {
      const tr = b.closest("tr"); const r = await api(`/api/admin/listings/${tr.dataset.id}`, { method: "POST", body: { status: b.dataset.act, tool_id: tr.querySelector("[name=tool]").value, review_note: tr.querySelector("[name=note]").value } });
      toast(r.ok ? "Saved." : r.error, !r.ok); renderAdmin();
    }));
    document.querySelectorAll("[data-fact]").forEach((b) => b.addEventListener("click", async () => {
      const tr = b.closest("tr"); const r = await api(`/api/admin/funds/${tr.dataset.fid}`, { method: "POST", body: { status: b.dataset.fact, ref: tr.querySelector("[name=ref]").value } });
      toast(r.ok ? "Saved." : r.error, !r.ok); renderAdmin();
    }));
    document.querySelectorAll("[data-vact]").forEach((b) => b.addEventListener("click", async () => {
      const tr = b.closest("tr"); const r = await api("/api/admin/credit", { method: "POST", body: { vendor_id: tr.dataset.vid, amount_cents: Math.round(Number(tr.querySelector("[name=amt]").value) * 100), note: tr.querySelector("[name=note]").value } });
      toast(r.ok ? "Balance updated." : r.error, !r.ok); renderAdmin();
    }));
  }

  const mode = document.body.dataset.portal || ($("#pt-root") || {}).dataset?.portal;
  if (mode === "login") initLogin();
  if (mode === "app") initApp();
  if (mode === "admin") initAdmin();
})();
