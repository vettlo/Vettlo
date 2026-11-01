# Vendor portal pages: public landing, sign-in, dashboard and admin shells (the app itself is
# src/portal-client.js talking to the Worker API in src/portal.js), plus the advertiser terms draft.

_PSCRIPT = '<script src="/assets/portal.js?v=' + PORTAL_V + '" defer></script>'

page("/vendors/", "Advertise Your Software on Vettlo: Vendor Portal | Vettlo",
     "Put your software in front of buyers comparing tools on Vettlo. Self-serve listings, cost-per-click bids, live reports and prepaid funds with no minimum spend.",
     """<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Reach buyers while they compare software.</h1>
<p class="lede">Vettlo readers arrive with a buying question, on shortlists, comparisons and reviews for the category you sell in. List your product, set a cost-per-click bid and pay only for visits to your site.</p>
<div class="ctas"><a class="btn" href="/vendors/login/">Create a vendor account</a><a class="btn ghost" href="/vendors/login/">Sign in</a></div></div>
<aside class="scorecard" aria-label="How placement works"><div class="sc-head"><span>How placement works</span><span class="sc-ex">Per category</span></div>
<ol class="pt-how"><li><b>Highest bid first</b><span>Approved partner listings appear at the top of the category shortlist, ordered by bid.</span></li>
<li><b>Pay per visit</b><span>You pay your bid only when a reader clicks through to your site. Repeat clicks within 24 hours and bots are free.</span></li>
<li><b>You stay in control</b><span>Change bids, pause listings and cap your monthly spend at any time.</span></li></ol></aside>
</div></section>
<div class="wrap about">
<section><div class="section-head"><div><span class="kicker">How it works</span><h2>Live in four steps</h2></div></div>
<ol class="steps"><li><b>Create an account</b><span>Sign in with your work email; no password needed.</span></li>
<li><b>Add your listing</b><span>Choose a category, add your product details and landing page with UTM parameters.</span></li>
<li><b>Set your bid</b><span>See the top bid and your estimated position in the category before you commit.</span></li>
<li><b>Add funds and go live</b><span>Once our editors approve the listing and your balance covers your bid, it appears on the shortlist.</span></li></ol></section>
<section><div class="section-head"><div><span class="kicker">Pricing</span><h2>Simple, prepaid and capped by you</h2></div></div>
<div class="cards3 aud">
<div class="card"><span class="label">Cost per click</span><h3 class="card-title">From $2.00 per visit</h3><p class="muted small">Bids move in $0.50 steps. You're charged your own bid for each valid click.</p></div>
<div class="card"><span class="label">No minimums</span><h3 class="card-title">Start with $250</h3><p class="muted small">No contract and no minimum monthly spend. Add funds when you need them.</p></div>
<div class="card"><span class="label">Control</span><h3 class="card-title">Monthly caps and pauses</h3><p class="muted small">Set a monthly budget; listings pause automatically when you reach it.</p></div></div></section>
<section class="split"><div><span class="kicker">What stays editorial</span><h2>Scores and reviews aren't for sale</h2></div>
<div class="prose"><p>Partner placement changes where your product appears in a category list. It doesn't change your score, our review or what we write about competitors. Every review carries a disclosure that partner compensation may affect which products we include and where they appear.</p>
<p>Listings are reviewed by our editors before they go live. We may edit descriptions for accuracy and decline products that don't fit a category. See the <a href="/advertiser-terms/">advertiser terms</a>.</p></div></section>
<section id="faq"><h2>FAQ</h2><div>""" + "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
        ("Where will my product appear?", "At the top of the shortlist for the category you choose, ordered by bid among approved partners, with a link to your landing page."),
        ("What counts as a billable click?", "A visit from a reader to your landing page through your listing. Clicks from known bots, repeat clicks from the same visitor within 24 hours, and clicks when your balance or monthly cap is reached are not charged."),
        ("How do I pay?", "Add funds from your dashboard. Funds are prepaid and deducted per valid click."),
        ("Can I see results?", "Yes. Your dashboard shows clicks, paid clicks and cost per day and per listing, with a CSV export. Add UTM parameters to your landing page to see conversions in your own analytics."),
        ("Do I need to be on Vettlo's shortlist already?", "No. If we've scored your product, your existing review card moves up. If we haven't, your listing appears with the details you provide, marked as not yet scored."),
    ]) + """</div></section>
<section class="about-cta"><div><h2>Ready to reach software buyers?</h2><p>Create your account in a minute.</p></div><a class="btn" href="/vendors/login/">Get started</a></section>
</div>""", cur="/advertise/")

page("/vendors/login/", "Sign In: Vettlo Vendor Portal",
     "Sign in to the Vettlo vendor portal.",
     """<div class="wrap pt-narrow" id="pt-root" data-portal="login"><div class="page-head"><h1>Vendor portal</h1><p>We'll email you a one-time sign-in link.</p></div>
<form class="form pt-card" id="pt-login"><div aria-hidden="true" style="position:absolute;left:-9999px"><label>Website<input name="website_hp" tabindex="-1" autocomplete="off"></label></div>
<label>Work email<input name="email" type="email" required autocomplete="email"></label>
<div id="pt-signup" hidden><label>Company<input name="company" autocomplete="organization"></label><label>Company website<input name="website" type="url" placeholder="https://"></label>
<label class="pt-check"><input type="checkbox" name="accept"> I agree to the <a href="/advertiser-terms/" target="_blank">advertiser terms</a>.</label></div>
<button class="btn" id="pt-submit" type="submit">Send sign-in link</button>
<p class="small muted">New here? <a href="#" id="pt-new">Create a vendor account</a></p></form>
<p class="form-msg" id="pt-login-msg" aria-live="polite"></p></div>""" + _PSCRIPT)

page("/vendors/app/", "Dashboard: Vettlo Vendor Portal", "Vettlo vendor dashboard.",
     """<div class="wrap pt-app" id="pt-root" data-portal="app"><div class="pt-top"><div><span class="kicker">Vendor portal</span><h1 id="pt-company">Loading…</h1></div>
<div class="pt-topnav"><a id="pt-admin-link" href="/vendors/admin/" hidden>Admin</a><button class="btn ghost small" id="pt-logout">Sign out</button></div></div>
<nav class="pt-tabs"><button data-tab="overview">Overview</button><button data-tab="listings">Listings</button><button data-tab="newListing">New listing</button><button data-tab="reports">Reports</button><button data-tab="funds">Funds</button><button data-tab="account">Account</button></nav>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/vendors/admin/", "Admin: Vettlo Vendor Portal", "Vettlo vendor portal admin.",
     """<div class="wrap pt-app" id="pt-root" data-portal="admin"><div class="pt-top"><div><span class="kicker">Vendor portal</span><h1>Admin</h1></div><div class="pt-topnav"><a href="/vendors/app/">Vendor view</a></div></div>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/advertiser-terms/", "Advertiser Terms | Vettlo",
     "The terms for listing and promoting software on Vettlo through the vendor portal: listings, bids, billing, valid clicks and editorial review.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Advertiser terms</h1>
<p class="small mono">Draft · last updated Nov 1, 2026</p></div><div class="page-body prose">
<p>These terms apply to software vendors ("you") who create listings on Vettlo through the vendor portal. By creating an account you agree to them.</p>
<h2>1. Listings and editorial review</h2><ul><li>Listings go live only after editorial approval. We may edit listing copy for accuracy and clarity, request changes, or decline or remove a listing at our discretion.</li>
<li>You must provide accurate information about your product, pricing and landing page, and keep it up to date. Changes to listing copy are reviewed again before they go live.</li>
<li>Your listing doesn't change your product's Vettlo score, our reviews or what we write about other products.</li></ul>
<h2>2. Placement and bids</h2><ul><li>Approved listings with an active bid and enough balance appear at the top of the chosen category's shortlist, ordered by bid (highest first; earlier listings first on equal bids).</li>
<li>The minimum bid and bid increments are shown in the portal and may change with notice there.</li>
<li>Every page that may contain partner placements discloses that partner compensation may affect which products we include and where they appear.</li></ul>
<h2>3. Billing</h2><ul><li>The service is prepaid. Funds are added to your balance and your bid is deducted for each valid click.</li>
<li>A valid click is a visit to your landing page through your listing. We don't charge for clicks we identify as automated, repeat clicks from the same visitor within 24 hours, or clicks after your balance or monthly cap is reached.</li>
<li>If you believe clicks were invalid, tell us within 30 days; confirmed invalid clicks are credited back to your balance.</li>
<li>Unused balance is refunded on request when you close your account, less any payment processing fees.</li></ul>
<h2>4. Your responsibilities</h2><ul><li>Your product, listing and landing page must be lawful, must not be misleading, and must not infringe anyone's rights.</li>
<li>You're responsible for your own landing pages, tracking and compliance with privacy laws for visitors you receive.</li></ul>
<h2>5. No guarantees</h2><p>We don't guarantee any number of impressions, clicks or conversions. The portal and reports are provided as is.</p>
<h2>6. Changes and termination</h2><p>You can pause listings or close your account at any time. We may suspend accounts that breach these terms. We may update these terms; material changes will be announced in the portal.</p>
<h2>7. Contact</h2><p>Questions about these terms: <a href="/contact/">contact us</a>.</p>
</div></div>""")
