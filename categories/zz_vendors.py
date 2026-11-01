# Vendor portal pages: public landing, sign-in, dashboard and admin shells (the app itself is
# src/portal-client.js talking to the Worker API in src/portal.js), plus the advertiser terms draft.

_PSCRIPT = '<script src="/assets/portal.js?v=' + PORTAL_V + '" defer></script>'

page("/vendors/", "Advertise Your Software on Vettlo: Vendor Portal | Vettlo",
     "Put your software in front of buyers comparing tools on Vettlo. Annual Basic, Pro and Premium plans that put your product on its category page, with a self-serve portal and live reports.",
     """<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Reach buyers while they compare software.</h1>
<p class="lede">Vettlo readers arrive with a buying question, on shortlists, comparisons and reviews for the category you sell in. Choose an annual plan for your category: a listing on the category page, or one of the top three places on its shortlist.</p>
<div class="ctas"><a class="btn" href="/advertise/#adv-form">Request pricing</a><a class="btn ghost" href="/vendors/login/">Vendor sign in</a></div></div>
<aside class="scorecard" aria-label="How placement works"><div class="sc-head"><span>How placement works</span><span class="sc-ex">Per category</span></div>
<ol class="pt-how"><li><b>Three plans</b><span>Basic, Pro and Premium, from a listing on the category page to 1st place on its shortlist.</span></li>
<li><b>One price a year</b><span>Billed once a year, however many readers see or click your listing.</span></li>
<li><b>Limited top places</b><span>Pro and Premium seats are limited in each category. When they're full, join the waitlist.</span></li></ol></aside>
</div></section>
<div class="wrap about">
<section><div class="section-head"><div><span class="kicker">How it works</span><h2>Live in four steps</h2></div></div>
<ol class="steps"><li><b>Ask for pricing</b><span>Tell us your product and category. We'll reply with prices and your link to the vendor portal.</span></li>
<li><b>Add your listing</b><span>Choose a category, add your product details and landing page with UTM parameters.</span></li>
<li><b>Choose a plan</b><span>See which plans have free seats in your category and reserve one. We hold it for 7 days while you pay.</span></li>
<li><b>Pay and go live</b><span>Once the invoice is paid and our editors approve the listing, your product appears for a year.</span></li></ol></section>
<section><div class="section-head"><div><span class="kicker">Plans</span><h2>Three annual plans</h2></div></div>
<div class="cards3 aud">
<div class="card"><span class="label">Unlimited seats</span><h3 class="card-title">Basic</h3><p class="muted small">Listed first under “Other tools to consider” on your category page, with your description and a link to your site.</p></div>
<div class="card"><span class="label">2 seats per category</span><h3 class="card-title">Pro</h3><p class="muted small">2nd or 3rd place on the category shortlist, review cards and comparison table. Earlier subscribers rank higher.</p></div>
<div class="card"><span class="label">1 seat per category</span><h3 class="card-title">Premium</h3><p class="muted small">1st place on the category shortlist, review cards and comparison table.</p></div></div>
<p class="muted small">All plans are billed yearly, per category, and include the vendor portal with impression and visit reports. <a href="/advertise/#adv-form">Ask us for pricing</a>.</p></section>
<section class="split"><div><span class="kicker">What stays editorial</span><h2>Scores and reviews aren't for sale</h2></div>
<div class="prose"><p>Partner placement changes where your product appears in a category list. It doesn't change your score, our review or what we write about competitors. Every review carries a disclosure that partner compensation may affect which products we include and where they appear.</p>
<p>Listings are reviewed by our editors before they go live. We may edit descriptions for accuracy and decline products that don't fit a category. See the <a href="/advertiser-terms/">advertiser terms</a>.</p></div></section>
<section id="faq"><h2>FAQ</h2><div>""" + "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
        ("Where will my product appear?", "On the page for the category you choose. Basic lists you first under Other tools to consider; Pro puts you 2nd or 3rd on the shortlist; Premium puts you 1st. Pro and Premium also place you in the review cards and comparison table."),
        ("What if the plan I want is full?", "Join its waitlist. When a seat frees up, the first vendor on the waitlist gets 72 hours to claim it before it opens to everyone."),
        ("How much does it cost, and how do I pay?", "Ask us for pricing and we'll send prices and your portal link. Plans are billed once a year: each new plan or renewal creates an invoice, and your plan goes live, or is extended by a year, when it's paid. Plans don't renew automatically."),
        ("Can I see results?", "Yes. Your dashboard shows impressions and visits to your site per day and per listing, with a CSV export. Add UTM parameters to your landing page to see conversions in your own analytics."),
        ("Do I need to be on Vettlo's shortlist already?", "No. If we've scored your product, your existing review card moves up. If we haven't, your listing appears with the details you provide, marked as not yet scored."),
    ]) + """</div></section>
<section class="about-cta"><div><h2>Ready to reach software buyers?</h2><p>Tell us your product and category, and we'll send pricing.</p></div><a class="btn" href="/advertise/#adv-form">Request pricing</a></section>
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
<nav class="pt-tabs"><button data-tab="overview">Overview</button><button data-tab="listings">Listings</button><button data-tab="plans">Plans</button><button data-tab="newListing">New listing</button><button data-tab="invoices">Invoices</button><button data-tab="reports">Reports</button><button data-tab="account">Account</button></nav>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/vendors/admin/", "Admin: Vettlo Vendor Portal", "Vettlo vendor portal admin.",
     """<div class="wrap pt-app" id="pt-root" data-portal="admin"><div class="pt-top"><div><span class="kicker">Vendor portal</span><h1>Admin</h1></div><div class="pt-topnav"><a href="/vendors/app/">Vendor view</a></div></div>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/advertiser-terms/", "Advertiser Terms | Vettlo",
     "The terms for listing and promoting software on Vettlo through the vendor portal: listings, annual plans, billing and editorial review.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Advertiser terms</h1>
<p class="small mono">Draft · last updated Nov 2, 2026</p></div><div class="page-body prose">
<p>These terms apply to software vendors ("you") who create listings on Vettlo through the vendor portal. By creating an account you agree to them.</p>
<h2>1. Listings and editorial review</h2><ul><li>Listings go live only after editorial approval. We may edit listing copy for accuracy and clarity, request changes, or decline or remove a listing at our discretion.</li>
<li>You must provide accurate information about your product, pricing and landing page, and keep it up to date. Changes to listing copy are reviewed again before they go live.</li>
<li>Your listing doesn't change your product's Vettlo score, our reviews or what we write about other products.</li></ul>
<h2>2. Plans</h2><ul><li>Plans are sold per category for one year. Basic lists your product under Other tools to consider. Pro places it 2nd or 3rd on the category shortlist (2 seats; earlier subscribers rank higher). Premium places it 1st (1 seat).</li>
<li>A reservation holds a seat for 7 days while the invoice is paid. Unpaid reservations lapse automatically.</li>
<li>When a Pro or Premium seat becomes free, the first vendor on its waitlist may claim it within 72 hours before it opens to others.</li>
<li>Your product appears only while the year is paid and the listing is approved and active.</li>
<li>Prices are shown in the portal and may change for future years; a paid year keeps the price you paid.</li>
<li>Every page that may contain partner placements discloses that partner compensation may affect which products we include and where they appear.</li></ul>
<h2>3. Billing</h2><ul><li>Plans are billed in advance, one year at a time. A plan goes live, or is extended by one year, when its invoice is paid.</li>
<li>Plans don't renew automatically. If you don't renew, the plan ends at the end of the paid year.</li>
<li>If we remove your listing or end your plan early for reasons other than a breach of these terms, we refund the unused part of the year.</li>
<li>Impression and visit figures in the portal are for your information and don't affect the price.</li></ul>
<h2>4. Your responsibilities</h2><ul><li>Your product, listing and landing page must be lawful, must not be misleading, and must not infringe anyone's rights.</li>
<li>You're responsible for your own landing pages, tracking and compliance with privacy laws for visitors you receive.</li></ul>
<h2>5. No guarantees</h2><p>We don't guarantee any number of impressions, clicks or conversions. The portal and reports are provided as is.</p>
<h2>6. Changes and termination</h2><p>You can pause listings, let plans lapse or close your account at any time. We may suspend accounts that breach these terms. We may update these terms; material changes will be announced in the portal.</p>
<h2>7. Contact</h2><p>Questions about these terms: <a href="/contact/">contact us</a>.</p>
</div></div>""")
