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
    if (new URLSearchParams(location.search).get("new")) { extra.hidden = false; f.dataset.signup = "1"; $("#pt-submit").textContent = "Create account and send link"; }
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
  const PLAN = { basic: "Basic", pro: "Pro", premium: "Premium" };
  for (let i = 1; i <= 10; i++) PLAN["p" + i] = "#" + i + " position";
  const planWhat = (plan) => plan === "basic" ? "Listed first under \u201cOther tools to consider\u201d on the category page, with a link to your site. Billed yearly."
    : `Your product at #${plan.slice(1)} on the category shortlist, review cards and comparison table. One vendor per position.`;
  const per = (p) => p === "month" ? "month" : "year";
  let PERIOD = "month";
  async function initApp() {
    const me = await api("/api/me");
    if (!me.ok) return;
    ME = me;
    CATS = (await api("/api/categories")).categories || [];
    $("#pt-company").textContent = "Signed in as " + (me.vendor.company || me.vendor.email);
    if (me.vendor.is_admin) $("#pt-admin-link").hidden = false;
    $("#pt-logout").addEventListener("click", async () => { await api("/api/logout", { method: "POST" }); location.href = "/vendors/"; });
    document.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => { if (b.dataset.tab === "plans") SEL = { page: null, plan: null }; showTab(b.dataset.tab); }));
    showTab(location.hash.slice(1) || "overview");
  }
  function showTab(name, arg) {
    document.querySelectorAll("[data-tab]").forEach((b) => b.classList.toggle("on", b.dataset.tab === name));
    history.replaceState(null, "", "#" + name);
    ({ overview, listings, plans, newListing, invoices, reports, account }[name] || overview)(arg);
  }
  // On phones, tables become stacked cards; each cell gets its column name as a label.
  const labelTables = (root) => root.querySelectorAll("table.pt-table").forEach((t) => {
    const heads = [...t.querySelectorAll("thead th")].map((th) => th.textContent.trim());
    t.querySelectorAll("tbody tr").forEach((tr) => [...tr.children].forEach((td, i) => { if (heads[i]) td.setAttribute("data-label", heads[i]); }));
  });
  const view = (html) => { const v = $("#pt-view"); v.innerHTML = html; labelTables(v); };
  function bindGo() { document.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); showTab(a.dataset.go, a.dataset.arg); })); }
  const statusPill = (l) => `<span class="pt-pill ${l.status === "approved" ? (l.active ? "ok" : "off") : l.status}">${l.status === "approved" ? (l.active ? "Published" : "Paused") : l.status === "pending" ? "In editorial review" : "Not approved"}</span>`;
  const subState = (s) => s.status !== "active" ? `<span class="pt-pill pending">Awaiting payment</span> <small class="muted">held until ${date(s.reserved_until)}</small>`
    : s.held_since ? `<span class="pt-pill pending">In editorial review</span> <small class="muted">Paid. Goes live when we publish your review; your paid time starts then.</small>`
    : `<span class="pt-pill ok">Live</span> <small class="muted">${s.auto_renew ? "renews" : "until"} ${date(s.paid_through)}</small>`;
  const subText = (s) => !s ? `<span class="muted">No position</span>` : `<b>${PLAN[s.plan]}</b> ${subState(s)}`;

  async function overview() {
    const [ls, inv] = await Promise.all([api("/api/listings"), api("/api/invoices")]);
    const L = ls.listings || [], I = (inv.rows || []).filter((x) => x.status === "requested");
    const live = L.filter((l) => l.sub && l.sub.status === "active");
    view(`<div class="pt-stats">
      <div><span>Positions</span><b>${L.reduce((a, l) => a + (l.subs || []).length, 0)}</b><small>${L.reduce((a, l) => a + (l.subs || []).filter((x) => x.held_since).length, 0)} in review · ${L.reduce((a, l) => a + (l.subs || []).filter((x) => x.status === "reserved").length, 0)} awaiting payment</small></div>
      <div><span>Impressions, 30 days</span><b>${L.reduce((a, l) => a + l.impressions_30d, 0).toLocaleString()}</b><small>Views of shortlists showing your product</small></div>
      <div><span>Visits, 30 days</span><b>${L.reduce((a, l) => a + l.clicks_30d, 0).toLocaleString()}</b><small>Unique clicks to your site</small></div>
      <div><span>Open invoices</span><b>${I.length}</b><small>${I.length ? money(I.reduce((a, x) => a + x.amount_cents, 0)) + " due" : "Nothing due"}</small></div></div>
      ${L.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Product</th><th>Category</th><th>Review</th><th>Position</th><th>Impressions (30d)</th><th>Visits (30d)</th><th></th></tr></thead><tbody>
        ${L.map((l) => `<tr><td><b>${esc(l.product_name)}</b></td><td><a href="/tools/${esc(l.category)}/" target="_blank">${esc(catName(l.category))}</a></td><td>${statusPill(l)}</td><td>${subText(l.sub)}</td><td>${l.impressions_30d}</td><td>${l.clicks_30d}</td>
        <td><a href="#plans" data-go="plans" data-arg="${l.id}">${l.sub ? "Manage" : "Buy a position"}</a></td></tr>`).join("")}</tbody></table></div>`
      : `<div class="pt-empty"><h3>Get your product in front of buyers</h3><p>Create a listing for your product, then choose a position on its category page, billed monthly or yearly.</p><button class="btn" data-go="newListing">Create a listing</button></div>`}`);
    bindGo();
  }

  async function listings() {
    const L = (await api("/api/listings")).listings || [];
    view(`<div class="pt-head"><h2>Your products</h2><button class="btn small" data-go="newListing">Add a product</button></div>
      <p class="muted">Our editors research each product and write its review before it goes live. Until then it shows as in editorial review.</p>
      ${L.length ? L.map((l) => `<form class="pt-card" data-id="${l.id}">
        <div class="pt-card-head"><div><h3>${esc(l.product_name)}</h3><p class="muted small"><a href="${esc(l.website)}" target="_blank" rel="noopener">${esc(l.website)}</a> · ${esc(catName(l.category))}</p><p>${statusPill(l)}${l.review_note ? ` <small class="muted">${esc(l.review_note)}</small>` : ""}</p></div>
        <label class="pt-switch"><input type="checkbox" name="active" ${l.active ? "checked" : ""}> Show on site</label></div>
        <label>Landing page<input name="landing_url" type="text" inputmode="url" autocapitalize="off" spellcheck="false" value="${esc(l.landing_url)}"><small>Where our Visit button sends readers. Add UTM parameters to track Vettlo traffic.</small></label>
        <div class="pt-actions"><button class="btn small" type="submit">Save</button><a class="small" href="#plans" data-go="plans" data-arg="${l.id}">${l.sub ? "Manage positions" : "Buy a position"} →</a></div></form>`).join("")
      : `<div class="pt-empty"><p>No products yet.</p><button class="btn" data-go="newListing">Add a product</button></div>`}`);
    bindGo();
    document.querySelectorAll("form.pt-card").forEach((f) => f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const r = await api(`/api/listings/${f.dataset.id}`, { method: "PUT", body: { active: f.active.checked, landing_url: f.landing_url.value } });
      toast(r.ok ? "Saved." : r.error, !r.ok);
      if (r.ok) listings();
    }));
  }

  // ---------- buy a position: 1) page, 2) position, 3) product and billing
  let PAGES = null, PRICES = null, SEL = { page: null, plan: null };
  const pageOf = (url) => (PAGES || []).find((p) => p.url === url);
  const kindLabel = (k) => k === "alternatives" ? "Alternatives page" : "Category shortlist";
  const steps = (n) => `<ol class="pt-steps">${["Choose a page", "Choose a position", "Product and billing"].map((t, i) => `<li class="${i + 1 < n ? "done" : i + 1 === n ? "on" : ""}"><span>${i + 1}</span>${t}</li>`).join("")}</ol>`;
  const pmo = (plan) => PRICES && PRICES[plan] ? PRICES[plan] : {};

  async function plans(arg) {
    const d = await api("/api/pages");
    PAGES = d.pages || []; PRICES = d.prices || {};
    if (arg && pageOf(arg)) SEL = { page: arg, plan: null };
    else if (arg && /^\d+$/.test(String(arg))) { const L = (await api("/api/listings")).listings || []; const l = L.find((x) => String(x.id) === String(arg)); SEL = { page: l ? `/tools/${l.category}/` : null, plan: null }; }
    if (SEL.page && SEL.plan) return stepProduct();
    if (SEL.page) return stepPosition();
    return stepPage();
  }

  async function stepPage() {
    const L = (await api("/api/listings")).listings || [];
    const mine = L.flatMap((l) => (l.subs || []).map((s) => ({ ...s, product_name: l.product_name })));
    const lo = money(pmo("p10").month), hi = money(pmo("p1").month);
    const groups = {};
    for (const p of PAGES) (groups[p.category] ||= { name: p.category_name, dept: p.dept, pages: [] }).pages.push(p);
    view(`<div class="pt-head"><h2>Buy a position</h2></div>${steps(1)}
      ${mine.length ? `<div class="pt-card"><h3>Your positions</h3><div class="table-wrap"><table class="pt-table"><thead><tr><th>Page</th><th>Position</th><th>Product</th><th>Billing</th><th>Status</th><th></th></tr></thead><tbody>
        ${mine.map((s) => { const pg = pageOf(s.page) || { title: s.page };
          const st = subState(s);
          const act = s.status !== "active" ? `<button class="btn ghost small" data-cancel="${s.id}">Cancel</button>` : s.held_since ? "" : s.auto_renew ? `<button class="btn ghost small" data-stop="${s.id}">Stop renewal</button>` : `<button class="btn ghost small" data-renew="${s.id}">Renew</button>`;
          return `<tr><td><a href="${esc(s.page)}" target="_blank">${esc(pg.title)}</a></td><td><b>${PLAN[s.plan]}</b></td><td>${esc(s.product_name)}</td><td>${s.period === "month" ? "Monthly" : "Yearly"}</td><td>${st}</td><td>${act}</td></tr>`; }).join("")}</tbody></table></div></div>` : ""}
      <p class="muted">Pick the page where you want your product to appear. Every page has 10 positions, each sold to one vendor: from ${lo} to ${hi} a month, or 10% less paid yearly.</p>
      <div class="pt-find"><input id="pt-q" type="search" placeholder="Search pages, e.g. CRM, HubSpot alternatives, payroll" autocomplete="off"></div>
      <div id="pt-pages">${Object.values(groups).map((g) => `<section class="pt-pgroup"><h3><span>${esc(g.dept)}</span> ${esc(g.name)}</h3>
        ${g.pages.map((p) => `<button class="pt-prow" data-page="${esc(p.url)}" data-q="${esc((p.title + " " + g.name + " " + g.dept).toLowerCase())}">
          <span class="pt-prow-t"><b>${esc(p.title)}</b><small>${kindLabel(p.kind)}</small></span>
          <span class="pt-prow-f ${p.free ? "" : "none"}">${p.free ? `${p.free} of 10 free` : "All taken"}</span><span class="pt-prow-go">Choose →</span></button>`).join("")}</section>`).join("")}</div>
      <p class="pt-none muted" hidden>No page matches. <a href="/contact/">Ask us</a> about other pages.</p>`);
    const q = $("#pt-q");
    q.addEventListener("input", () => { const v = q.value.trim().toLowerCase(); let any = 0;
      document.querySelectorAll(".pt-pgroup").forEach((g) => { let n = 0; g.querySelectorAll(".pt-prow").forEach((r) => { const ok = !v || r.dataset.q.includes(v); r.hidden = !ok; n += ok; }); g.hidden = !n; any += n; });
      $(".pt-none").hidden = !!any; });
    document.querySelectorAll("[data-page]").forEach((b) => b.addEventListener("click", () => { SEL = { page: b.dataset.page, plan: null }; stepPosition(); }));
    bindSubActions(stepPage);
  }

  function bindSubActions(again) {
    const act = async (url, okMsg) => { const r = await api(url, { method: "POST", body: {} }); toast(r.ok ? okMsg : r.error, !r.ok); again(); };
    document.querySelectorAll("[data-renew]").forEach((b) => b.addEventListener("click", () => act(`/api/subs/${b.dataset.renew}/renew`, "Renewal invoice created. Pay it in Invoices.")));
    document.querySelectorAll("[data-cancel]").forEach((b) => b.addEventListener("click", () => act(`/api/subs/${b.dataset.cancel}/cancel`, "Reservation cancelled.")));
    document.querySelectorAll("[data-stop]").forEach((b) => b.addEventListener("click", () => { if (confirm("Stop the monthly renewal? The position stays live until the end of the paid month.")) act(`/api/subs/${b.dataset.stop}/stop`, "Renewal stopped."); }));
  }

  async function stepPosition() {
    const r = await api("/api/plans?page=" + encodeURIComponent(SEL.page));
    if (!r.ok) { SEL = { page: null, plan: null }; return stepPage(); }
    const pg = r.page, P = r.plans || [];
    const row = (p) => {
      const period = p.plan === "basic" ? "year" : PERIOD;
      const cents = period === "month" ? p.month_cents : p.year_cents;
      let status = "", action = "";
      if (p.state === "available") { status = "Available"; action = `<button class="btn small" data-pick="${p.plan}">Select</button>`; }
      else if (p.state === "yours") status = `<b>Yours</b>, ${p.auto_renew ? "renews" : "paid until"} ${date(p.until)}`;
      else if (p.state === "reserved_by_you") status = `<b>Reserved for you</b> until ${date(p.until)}`;
      else { status = p.state === "full" ? `Taken until ${date(p.until)}` : `Held for the waitlist until ${date(p.until)}`;
        action = p.on_waitlist ? `<button class="btn ghost small" data-leave="${p.plan}">Leave waitlist</button>` : `<button class="btn ghost small" data-wait="${p.plan}">Join waitlist</button>`; }
      const n = p.plan === "basic" ? "B" : p.plan.slice(1);
      const label = p.plan === "basic" ? "Basic listing <small>under “Other tools to consider”, yearly only</small>" : `Position #${n}`;
      return `<div class="pt-slot ${p.state === "full" ? "taken" : p.state}"><span class="pt-slot-n">${n}</span><div><b>${label}</b><span class="small muted">${status}${p.waitlist ? " · " + p.waitlist + " waiting" : ""}</span></div>
        <div class="pt-slot-r"><span class="pt-plan-price">${money(cents)}<small> / ${period}</small></span>${action}</div></div>`;
    };
    view(`<div class="pt-head"><h2>Buy a position</h2></div>${steps(2)}
      <div class="pt-pagecard"><div><small>${kindLabel(pg.kind)} · ${esc(pg.category_name)}</small><b>${esc(pg.title)}</b></div>
        <div class="pt-actions"><a class="small" href="${esc(pg.url)}" target="_blank">View page ↗</a><button class="btn ghost small" id="pt-back">Change page</button></div></div>
      <div class="pt-seg" role="group" aria-label="Billing"><button class="${PERIOD === "month" ? "on" : ""}" data-period-pick="month">Monthly</button><button class="${PERIOD === "year" ? "on" : ""}" data-period-pick="year">Yearly <em>10% off</em></button></div>
      <div class="pt-slots">${P.map(row).join("")}</div>
      <p class="muted small">Your product appears at the position you buy on this page's ranked list, review cards and comparison table${pg.kind === "alternatives" ? "" : ""}. If the list is shorter than your position, it appears at the end. Our editors review and score your product before it goes live; the score is ours and isn't affected by your plan.</p>`);
    $("#pt-back").addEventListener("click", () => { SEL = { page: null, plan: null }; stepPage(); });
    document.querySelectorAll("[data-period-pick]").forEach((b) => b.addEventListener("click", () => { PERIOD = b.dataset.periodPick; stepPosition(); }));
    document.querySelectorAll("[data-pick]").forEach((b) => b.addEventListener("click", () => { SEL.plan = b.dataset.pick; stepProduct(); }));
    const L = ((await api("/api/listings")).listings || []).filter((l) => l.category === pg.category && l.status !== "rejected");
    const wl = async (url, plan, msg) => { if (!L.length) { toast("Add your product first: select a free position or create a listing for this category.", true); return; }
      const x = await api(url, { method: "POST", body: { listing_id: L[0].id, page: pg.url, plan } }); toast(x.ok ? msg : x.error, !x.ok); stepPosition(); };
    document.querySelectorAll("[data-wait]").forEach((b) => b.addEventListener("click", () => wl("/api/waitlist", b.dataset.wait, "You're on the waitlist.")));
    document.querySelectorAll("[data-leave]").forEach((b) => b.addEventListener("click", async () => { await api("/api/waitlist/leave", { method: "POST", body: { page: pg.url, plan: b.dataset.leave } }); toast("Removed from the waitlist."); stepPosition(); }));
  }

  async function stepProduct() {
    const pg = pageOf(SEL.page), plan = SEL.plan;
    const period = plan === "basic" ? "year" : PERIOD;
    const cents = pmo(plan)[period];
    const L = ((await api("/api/listings")).listings || []).filter((l) => l.category === pg.category && l.status !== "rejected" && !(pg.exclude && l.tool_id === pg.exclude)
      && !(l.subs || []).some((x) => x.page === pg.url));
    view(`<div class="pt-head"><h2>Buy a position</h2></div>${steps(3)}
      <div class="pt-summary"><div><small>Your order</small><b>${PLAN[plan]} on ${esc(pg.title)}</b><span class="muted small">${period === "month" ? "Billed monthly" + (ME.subscriptions ? ", renews automatically until you stop it" : "") : "Billed once for 12 months, 10% off"}</span></div>
        <span class="pt-plan-price">${money(cents)}<small> / ${period}</small></span></div>
      <form class="pt-card" id="pt-order"><h3>Which product?</h3>
        ${L.length ? `<div class="pt-choices">${L.map((l, i) => `<label class="pt-choice"><input type="radio" name="listing" value="${l.id}" ${i === 0 ? "checked" : ""}><span><b>${esc(l.product_name)}</b><small>${esc(l.best_for || l.website)}${l.status === "pending" ? " · in editorial review" : ""}</small></span></label>`).join("")}
          <label class="pt-choice"><input type="radio" name="listing" value="new"><span><b>Another product</b><small>Add a new product for ${esc(pg.category_name)}</small></span></label></div>` : `<input type="hidden" name="listing" value="new">`}
        <div id="pt-newprod" class="pt-grid" ${L.length ? "hidden" : ""}>
          <label>Product name<input name="product_name" maxlength="80"></label>
          <label>Product website<input name="website" type="text" inputmode="url" autocapitalize="off" spellcheck="false" placeholder="example.com"></label>
          <p class="wide muted small">That's all we need. Our editors research the product and write its review; you'll see it as in editorial review until we publish it.</p></div>
        <label class="pt-consent"><input type="checkbox" name="accept_terms" required> <span>I have read and agree to the <a href="/advertiser-terms/" target="_blank">advertiser terms</a><span class="pt-tr-docs" hidden>, the <a href="/yasal/on-bilgilendirme-formu/" target="_blank" lang="tr">Ön Bilgilendirme Formu</a> and the <a href="/yasal/mesafeli-hizmet-sozlesmesi/" target="_blank" lang="tr">Mesafeli Hizmet Sözleşmesi</a></span>.</span></label>
        <div class="pt-actions"><button class="btn" type="submit">Reserve ${PLAN[plan]} for ${money(cents)} / ${period}</button><button class="btn ghost small" type="button" id="pt-back">Back</button>
          <span class="muted small">We hold the position for 7 days while you pay. It goes live once our review is published, and your paid time starts then.</span></div></form>`);
    $("#pt-back").addEventListener("click", () => { SEL.plan = null; stepPosition(); });
    fetch("/yasal/on-bilgilendirme-formu/", { method: "HEAD" }).then((r) => { if (r.ok) document.querySelectorAll(".pt-tr-docs").forEach((x) => (x.hidden = false)); }).catch(() => {});
    const f = $("#pt-order"), np = $("#pt-newprod");
    f.querySelectorAll('input[name="listing"]').forEach((r) => r.addEventListener("change", () => { np.hidden = f.listing.value !== "new"; }));
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      let id = f.listing.value;
      if (id === "new") {
        if (!f.product_name.value || !f.website.value) return toast("Add the product name and website.", true);
        const c = await api("/api/listings", { method: "POST", body: { product_name: f.product_name.value, category: pg.category, website: f.website.value, landing_url: f.website.value } });
        if (!c.ok) return toast(c.error, true);
        id = c.id;
      }
      if (!f.accept_terms.checked) return toast("Please accept the terms to place your order.", true);
      const r = await api("/api/subscribe", { method: "POST", body: { listing_id: Number(id), page: pg.url, plan, period, accept_terms: true } });
      if (!r.ok) return toast(r.error, true);
      SEL = { page: null, plan: null };
      toast(ME.payments !== "invoice" ? "Reserved. Pay the invoice to go live." : "Reserved. We'll email your invoice.");
      showTab("invoices");
    });
  }

  function newListing() {
    const opts = CATS.map((c) => `<option value="${esc(c.slug)}">${esc(c.dept)} · ${esc(c.name)}</option>`).join("");
    view(`<div class="pt-head"><h2>Add a product</h2></div><form class="pt-card" id="pt-new-form"><div class="pt-grid">
      <label>Product name<input name="product_name" required maxlength="80"></label>
      <label>Product website<input name="website" type="text" inputmode="url" autocapitalize="off" spellcheck="false" required placeholder="example.com"></label>
      <label class="wide">Category<select name="category" required><option value="">Choose…</option>${opts}</select></label>
      </div><p class="muted small">Our editors research the product and write its review. It shows as in editorial review until we publish it.</p>
      <div class="pt-actions"><button class="btn" type="submit">Add product</button></div></form>`);
    $("#pt-new-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target;
      const r = await api("/api/listings", { method: "POST", body: { product_name: f.product_name.value, category: f.category.value, website: f.website.value, landing_url: f.website.value } });
      toast(r.ok ? "Added. It's now in editorial review." : r.error, !r.ok);
      if (r.ok) { SEL = { page: `/tools/${f.category.value}/`, plan: null }; showTab("plans"); }
    });
  }

  async function invoices() {
    const rows = (await api("/api/invoices")).rows || [];
    if (!PAGES) { const d = await api("/api/pages"); PAGES = d.pages || []; PRICES = d.prices || {}; }
    const card = ME.payments !== "invoice";
    const res = new URLSearchParams(location.search).get("pay");
    const msg = { ok: "Payment received. Your plan is active; it goes live on the site as soon as your listing is approved.", failed: "The payment didn't go through. You haven't been charged; please try again.",
      error: "We couldn't confirm that payment. If you were charged, contact us and we'll sort it out.", pending: "We're waiting for the payment provider to confirm your payment. Your plan starts as soon as it does; refresh in a minute.", held: "Payment received, but the plan couldn't start automatically. We'll contact you shortly." }[res];
    if (res) history.replaceState(null, "", location.pathname + "#invoices");
    view(`<div class="pt-head"><h2>Invoices</h2></div>
      ${msg ? `<div class="pt-note">${msg}</div>` : ""}
      <p class="muted">${card ? "Pay open invoices by card. Card details go straight to our payment provider and are never stored by Vettlo; your plan starts, or is extended by its billing period, as soon as the payment is confirmed." : "We email an invoice for each new plan and renewal. Your plan goes live, or is extended by its billing period, as soon as payment arrives."}</p>
      ${rows.length ? `<div class="table-wrap"><table class="pt-table"><thead><tr><th>Date</th><th>For</th><th>Amount</th><th>Status</th><th></th></tr></thead><tbody>
      ${rows.map((x) => `<tr><td>${date(x.created_at)}</td><td>${x.plan ? `${esc(x.product_name)}, ${PLAN[x.plan]} on ${esc((pageOf(x.page) || {}).title || catName(x.category))}, 1 ${per(x.period)}` : "Adjustment"}</td><td>${money(x.amount_cents)}</td><td><span class="pt-pill ${x.status === "paid" ? "ok" : x.status === "requested" ? "pending" : "off"}">${x.status === "requested" ? "Due" : x.status === "paid" ? "Paid" : "Cancelled"}</span></td>
        <td>${x.status === "requested" && card ? `<button class="btn small" data-pay="${x.id}">Pay by card</button>` : ""}</td></tr>`).join("")}</tbody></table></div>`
      : `<p class="muted">No invoices yet.</p>`}`);
    document.querySelectorAll("[data-pay]").forEach((b) => b.addEventListener("click", async () => {
      b.disabled = true; b.textContent = "Opening…";
      const r = await api("/api/pay", { method: "POST", body: { invoice_id: Number(b.dataset.pay) } });
      if (r.ok && r.url) { location.href = r.url; return; }
      toast(r.error || "Something went wrong.", true); b.disabled = false; b.textContent = "Pay by card";
      if (r.needs_billing) showTab("account");
    }));
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
    const [me, bl] = await Promise.all([api("/api/me"), api("/api/billing")]); const v = me.vendor, b = bl.billing || {};
    const f = (k, label, extra = "") => `<label>${label}<input name="${k}" value="${esc(b[k] || "")}" ${extra}></label>`;
    view(`<div class="pt-head"><h2>Account</h2></div><form class="pt-card" id="pt-acct"><h3>Company</h3><div class="pt-grid">
      <label>Company<input name="company" value="${esc(v.company || "")}"></label>
      <label>Website<input name="website" type="text" inputmode="url" autocapitalize="off" spellcheck="false" value="${esc(v.website || "")}"></label>
      <label>Sign-in email<input value="${esc(v.email)}" disabled></label></div>
      <div class="pt-actions"><button class="btn small" type="submit">Save</button><a class="small" href="/advertiser-terms/" target="_blank">Advertiser terms</a></div></form>
      <form class="pt-card" id="pt-bill"><h3>Billing details</h3><p class="muted small">Used on your invoices and required by our payment provider for card payments.</p><div class="pt-grid">
      ${f("name", "First name", "required")}${f("surname", "Last name", "required")}
      ${f("phone", "Phone", 'required type="tel" placeholder="+1 555 000 0000"')}${f("tax_id", "Tax ID or identity number", 'required placeholder="VAT, EIN, company number or national ID"')}
      <label class="wide">Billing address<input name="address" value="${esc(b.address || "")}" required></label>
      ${f("city", "City", "required")}${f("country", "Country", "required")}${f("zip", "Postal code")}</div>
      <div class="pt-actions"><button class="btn small" type="submit">Save billing details</button></div></form>`);
    $("#pt-acct").addEventListener("submit", async (e) => {
      e.preventDefault(); const t = e.target;
      const r = await api("/api/me", { method: "PUT", body: { company: t.company.value, website: t.website.value } });
      toast(r.ok ? "Saved." : r.error, !r.ok);
    });
    $("#pt-bill").addEventListener("submit", async (e) => {
      e.preventDefault(); const t = e.target; const body = {};
      for (const k of ["name", "surname", "phone", "tax_id", "address", "city", "country", "zip"]) body[k] = t[k].value;
      const r = await api("/api/billing", { method: "PUT", body });
      toast(r.ok ? "Billing details saved." : r.error, !r.ok);
    });
  }

  // ---------- admin
  async function initAdmin() {
    const me = await api("/api/me");
    if (!me.ok || !me.vendor.is_admin) { $("#pt-view").innerHTML = "<p>Admins only.</p>"; return; }
    CATS = (await api("/api/categories")).categories || [];
    const pd = await api("/api/pages"); PAGES = pd.pages || []; PRICES = pd.prices || {};
    renderAdmin();
  }
  async function renderAdmin() {
    const d = await api("/api/admin/overview");
    const D = (iso) => iso ? iso.slice(0, 10) : "";
    const toolOpts = (slug, cur) => `<option value="">Not on our list</option>` + ((CATS.find((c) => c.slug === slug) || {}).tools || []).map((t) => `<option value="${esc(t.id)}" ${t.id === cur ? "selected" : ""}>${esc(t.name)}</option>`).join("");
    const ptitle = (u) => esc((pageOf(u) || {}).title || u || "");
    const subsOf = (id) => d.subs.filter((x) => x.listing_id === id);
    const needs = d.listings.filter((l) => l.status === "pending" || (l.status === "approved" && !l.tool_id && subsOf(l.id).some((x) => x.plan !== "basic")));
    const reqCard = (l) => `<div class="pt-card pt-req" data-id="${l.id}"><div class="pt-card-head"><div>
        <h3>${esc(l.product_name)} <a class="small" href="${esc(l.website)}" target="_blank" rel="noopener">${esc(l.website)} ↗</a></h3>
        <p class="muted small">${esc(l.company)} · ${esc(l.email)} · ${esc(catName(l.category))} · added ${D(l.created_at)}</p></div><span class="pt-pill pending">${l.status === "pending" ? "Waiting for review" : "Approved, not matched"}</span></div>
      ${subsOf(l.id).length ? `<ul class="pt-reqsubs">${subsOf(l.id).map((x) => `<li><b>${PLAN[x.plan]}</b> on ${ptitle(x.page)} · ${x.period === "month" ? "monthly" : "yearly"} · ${x.status === "active" ? `<span class="pt-pill ok">Paid</span>` : `<span class="pt-pill">Not paid yet</span>`}</li>`).join("")}</ul>` : `<p class="muted small">No position reserved yet.</p>`}
      <ol class="pt-todo"><li>Ask Claude to research ${esc(l.product_name)} and add its review to ${esc(catName(l.category))}.</li><li>Once it's published, match it below and approve. The vendor's paid time starts then.</li></ol>
      <div class="pt-grid"><label>Matches tool on our list<select name="tool">${toolOpts(l.category, l.tool_id)}</select></label><label>Note to vendor (optional)<input name="note" value="${esc(l.review_note || "")}"></label></div>
      <div class="pt-actions"><button class="btn small" data-act="approved">Approve and publish</button><button class="btn ghost small" data-act="rejected">Reject</button></div></div>`;
    $("#pt-view").innerHTML = `
      <h2>Requests to review <span class="pt-count">${needs.length}</span></h2>
      ${needs.length ? needs.map(reqCard).join("") : `<div class="pt-empty"><p>No requests waiting. New products and position requests appear here.</p></div>`}
      <h2>Invoices</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Date</th><th>Vendor</th><th>For</th><th>Amount</th><th>Status</th><th></th></tr></thead><tbody>
      ${d.invoices.map((i) => `<tr data-iid="${i.id}"><td>${D(i.created_at)}</td><td>${esc(i.company)}<br><small>${esc(i.email)}</small></td><td>${i.plan ? `${esc(i.product_name)} · ${PLAN[i.plan]} · ${ptitle(i.page)}` : ""}</td><td>${money(i.amount_cents)}</td><td>${esc(i.status)}</td>
        <td>${i.status === "requested" ? `<input name="ref" placeholder="Payment ref"><button class="btn small" data-iact="paid">Mark paid</button> <button class="btn ghost small" data-iact="cancelled">Cancel</button>` : esc(i.provider_ref || "")}</td></tr>`).join("") || `<tr><td colspan="6" class="muted">No invoices.</td></tr>`}</tbody></table></div>
      <h2>All products</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Vendor</th><th>Product</th><th>Category</th><th>Copy</th><th>Matches tool</th><th>Status</th><th></th></tr></thead><tbody>
      ${d.listings.map((l) => `<tr data-id="${l.id}"><td>${esc(l.company)}<br><small>${esc(l.email)}</small></td><td><a href="${esc(l.website)}" target="_blank" rel="noopener">${esc(l.product_name)}</a></td><td>${esc(catName(l.category))}</td>
        <td class="small">${esc(l.best_for || "")}<br>${esc(l.description || "")}<br>${esc(l.starting_price || "")}</td><td><select name="tool">${toolOpts(l.category, l.tool_id)}</select></td><td>${esc(l.status)}</td>
        <td><input name="note" placeholder="Note to vendor" value="${esc(l.review_note || "")}"><button class="btn small" data-act="approved">Approve</button> <button class="btn ghost small" data-act="rejected">Reject</button></td></tr>`).join("") || `<tr><td colspan="7" class="muted">No listings.</td></tr>`}</tbody></table></div>
      <h2>Positions</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Page</th><th>Position</th><th>Product</th><th>Vendor</th><th>Status</th><th>Until</th><th></th></tr></thead><tbody>
      ${d.subs.map((s) => `<tr data-sid="${s.id}"><td>${ptitle(s.page)}</td><td>${PLAN[s.plan]}${s.period === "month" ? " · monthly" : " · yearly"}</td><td>${esc(s.product_name)}${s.listing_status !== "approved" ? ` <small>(listing ${esc(s.listing_status)})</small>` : ""}</td><td>${esc(s.company)}</td><td>${s.status !== "active" ? "Reserved, unpaid" : s.held_since ? "Paid, in review" : "Live"}</td><td>${D(s.status === "active" ? s.paid_through : s.reserved_until)}</td><td><button class="btn ghost small" data-sact="end">End now</button></td></tr>`).join("") || `<tr><td colspan="7" class="muted">No plans sold yet.</td></tr>`}</tbody></table></div>
      <h2>Waitlist</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Page</th><th>Position</th><th>Product</th><th>Vendor</th><th>Joined</th></tr></thead><tbody>
      ${d.waitlist.map((w) => `<tr><td>${ptitle(w.page)}</td><td>${PLAN[w.plan]}</td><td>${esc(w.product_name)}</td><td>${esc(w.company)}</td><td>${D(w.created_at)}</td></tr>`).join("") || `<tr><td colspan="5" class="muted">Empty.</td></tr>`}</tbody></table></div>
      <h2>Vendors</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Company</th><th>Email</th><th>Website</th><th>Joined</th></tr></thead><tbody>
      ${d.vendors.map((v) => `<tr><td>${esc(v.company || "")}</td><td>${esc(v.email)}</td><td>${esc(v.website || "")}</td><td>${D(v.created_at)}</td></tr>`).join("")}</tbody></table></div>
      <h2>Sponsor traffic, last 30 days</h2><div class="table-wrap"><table class="pt-table"><thead><tr><th>Day</th><th>Impressions</th><th>Visits</th></tr></thead><tbody>
      ${d.stats.map((c) => `<tr><td>${c.day}</td><td>${c.impressions}</td><td>${c.clicks}</td></tr>`).join("") || `<tr><td colspan="3" class="muted">No data yet.</td></tr>`}</tbody></table></div>`;
    labelTables($("#pt-view"));
    const post = async (url, body) => { const r = await api(url, { method: "POST", body }); toast(r.ok ? "Saved." : r.error, !r.ok); renderAdmin(); };
    document.querySelectorAll("[data-act]").forEach((b) => b.addEventListener("click", () => { const tr = b.closest("tr, .pt-req");
      if (b.dataset.act === "approved" && !tr.querySelector("[name=tool]").value && !confirm("This product isn't matched to a tool on our list, so ranked positions won't show yet. Approve anyway?")) return;
      post(`/api/admin/listings/${tr.dataset.id}`, { status: b.dataset.act, tool_id: tr.querySelector("[name=tool]").value, review_note: tr.querySelector("[name=note]").value }); }));
    document.querySelectorAll("[data-iact]").forEach((b) => b.addEventListener("click", () => { const tr = b.closest("tr"); post(`/api/admin/invoices/${tr.dataset.iid}`, { status: b.dataset.iact, ref: tr.querySelector("[name=ref]").value }); }));
    document.querySelectorAll("[data-sact]").forEach((b) => b.addEventListener("click", () => { if (confirm("End this plan now? The vendor won't be refunded automatically.")) post(`/api/admin/subs/${b.closest("tr").dataset.sid}/end`, {}); }));
  }

  const mode = document.body.dataset.portal || ($("#pt-root") || {}).dataset?.portal;
  if (mode === "login") initLogin();
  if (mode === "app") initApp();
  if (mode === "admin") initAdmin();
})();
