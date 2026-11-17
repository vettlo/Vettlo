# Vendor portal pages: public landing, sign-in, dashboard and admin shells (the app itself is
# src/portal-client.js talking to the Worker API in src/portal.js), plus the advertiser terms draft.

_PSCRIPT = '<script src="/assets/portal.js?v=' + PORTAL_V + '" defer></script>'

page("/vendors/", "Advertise Your Software on Vettlo: Vendor Portal | Vettlo",
     "Put your software in front of buyers comparing tools on Vettlo. Pick a category shortlist or alternatives page, then buy position #1 to #10 on it, billed monthly or yearly, with a self-serve portal and live reports.",
     """<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Reach buyers while they compare software.</h1>
<p class="lede">Vettlo readers arrive with a buying question, on shortlists, comparisons and reviews for the category you sell in. Pick the page you want, a category shortlist or an alternatives page, then choose a position from #1 to #10 on it, billed monthly or yearly.</p>
<div class="ctas"><a class="btn" href="/advertise/#adv-form">Request pricing</a><a class="btn ghost" href="/vendors/login/">Vendor sign in</a></div></div>
<aside class="scorecard" aria-label="How placement works"><div class="sc-head"><span>How placement works</span><span class="sc-ex">Per category</span></div>
<ol class="pt-how"><li><b>Pick a page, then a position</b><span>Category shortlists and alternatives pages each have positions #1 to #10, each sold to one vendor at a time.</span></li>
<li><b>Monthly or yearly</b><span>A flat price per position, however many readers see or click it. Yearly saves 10%.</span></li>
<li><b>Waitlist</b><span>When the position you want is taken, join its waitlist and get first claim when it frees up.</span></li></ol></aside>
</div></section>
<div class="wrap about">
<section><div class="section-head"><div><span class="kicker">How it works</span><h2>Live in four steps</h2></div></div>
<ol class="steps"><li><b>Ask for pricing</b><span>Tell us your product and category. We'll reply with prices and your link to the vendor portal.</span></li>
<li><b>Add your listing</b><span>Choose a category, add your product details and landing page with UTM parameters.</span></li>
<li><b>Choose a page and position</b><span>Pick a shortlist or alternatives page, see which positions are free and reserve one. We hold it for 7 days while you pay.</span></li>
<li><b>Pay and go live</b><span>Once payment is confirmed and our editors approve the listing, your product appears at its position for the paid month or year.</span></li></ol></section>
<section><div class="section-head"><div><span class="kicker">Plans</span><h2>Positions and listings</h2></div></div>
<div class="cards3 aud">
<div class="card"><span class="label">1 vendor per position</span><h3 class="card-title">Positions #1 to #10</h3><p class="muted small">Your product at the position you buy on a category shortlist or alternatives page: its ranked list, review cards and comparison table. Higher positions cost more.</p></div>
<div class="card"><span class="label">Monthly or yearly</span><h3 class="card-title">Billing</h3><p class="muted small">Monthly plans renew automatically by card until you stop them. Yearly plans are paid once for 12 months at 10% off.</p></div>
<div class="card"><span class="label">Unlimited seats</span><h3 class="card-title">Basic listing</h3><p class="muted small">Listed first under “Other tools to consider” on your category page, with your description and a link to your site. Billed yearly.</p></div></div>
<p class="muted small">Every plan is per category and includes the vendor portal with impression and visit reports. <a href="/advertise/#adv-form">Ask us for pricing</a>.</p></section>
<section class="split"><div><span class="kicker">What stays editorial</span><h2>Scores and reviews aren't for sale</h2></div>
<div class="prose"><p>Partner placement changes where your product appears in a category list. It doesn't change your score, our review or what we write about competitors. Every review carries a disclosure that partner compensation may affect which products we include and where they appear.</p>
<p>Listings are reviewed by our editors before they go live. We may edit descriptions for accuracy and decline products that don't fit a category. See the <a href="/advertiser-terms/">advertiser terms</a>.</p></div></section>
<section id="faq"><h2>FAQ</h2><div>""" + "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
        ("Where will my product appear?", "On the page for the category you choose. A position plan puts your product at that position, from #1 to #10, on the shortlist, in the review cards and in the comparison table. If the list is shorter than your position, your product appears at the end of it. Basic lists you first under Other tools to consider."),
        ("What if the position I want is taken?", "Join its waitlist. When it frees up, the first vendor on the waitlist gets 72 hours to claim it before it opens to everyone."),
        ("How much does it cost, and how do I pay?", "Ask us for pricing and we'll send prices and your portal link. Choose monthly or yearly billing. Monthly plans are charged to your card each month until you stop the renewal in the portal. Yearly plans cost 10% less than 12 months and don't renew automatically."),
        ("Can I see results?", "Yes. Your dashboard shows impressions and visits to your site per day and per listing, with a CSV export. Add UTM parameters to your landing page to see conversions in your own analytics."),
        ("Do I need to be on Vettlo's shortlist already?", "No. For a position plan, our editors review and score your product with the same criteria as every other tool before it appears, usually within 2 to 3 business days of payment. The score is ours, and your plan doesn't change it. Basic listings appear under Other tools to consider, which we don't score."),
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
     """<div class="wrap pt-app" id="pt-root" data-portal="app"><div class="pt-top"><div><h1>Vendor portal</h1><p class="muted small" id="pt-company"></p></div>
<div class="pt-topnav"><a id="pt-admin-link" href="/vendors/admin/" hidden>Admin</a><button class="btn ghost small" id="pt-logout">Sign out</button></div></div>
<nav class="pt-tabs"><button data-tab="overview">Overview</button><button data-tab="listings">Products</button><button data-tab="plans">Buy a position</button><button data-tab="newListing">Add a product</button><button data-tab="invoices">Invoices</button><button data-tab="reports">Reports</button><button data-tab="account">Account</button></nav>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/vendors/admin/", "Admin: Vettlo Vendor Portal", "Vettlo vendor portal admin.",
     """<div class="wrap pt-app" id="pt-root" data-portal="admin"><div class="pt-top"><div><h1>Vettlo admin</h1><p class="muted small">Vendor requests, positions and payments</p></div><div class="pt-topnav"><a href="/vendors/app/">Vendor view</a></div></div>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/advertiser-terms/", "Advertiser Terms: Listings, Plans and Billing | Vettlo",
     "The terms for listing and promoting software on Vettlo through the vendor portal: listings, position plans, monthly and yearly billing, editorial review.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Advertiser terms</h1>
<p class="small mono">Draft · last updated Nov 17, 2026</p></div><div class="page-body prose">
<p>These terms apply to software vendors ("you") who create listings on Vettlo through the vendor portal. By creating an account you agree to them.</p>
<h2>1. Listings and editorial review</h2><ul><li>Listings go live only after editorial approval. We may edit listing copy for accuracy and clarity, request changes, or decline or remove a listing at our discretion.</li>
<li>You must provide accurate information about your product, pricing and landing page, and keep it up to date. Changes to listing copy are reviewed again before they go live.</li>
<li>Your listing doesn't change your product's Vettlo score, our reviews or what we write about other products.</li></ul>
<h2>2. Plans</h2><ul><li>Plans are sold per category. A position plan places your product at the position you buy, from #1 to #10, on the page you choose (a category shortlist or an alternatives page): its ranked list, review cards and comparison table. Each position on each page is sold to one vendor at a time, and a product can't buy a position on its own alternatives page. If a list has fewer entries than your position, your product appears at its end. Basic lists your product under Other tools to consider.</li>
<li>A reservation holds a seat for 7 days while the invoice is paid. Unpaid reservations lapse automatically.</li>
<li>When a position becomes free, the first vendor on its waitlist may claim it within 72 hours before it opens to others.</li>
<li>Your product appears only while the plan is paid and the listing is approved and active.</li>
<li>Prices are shown in the portal and may change for future billing periods; a paid period keeps the price you paid. A running monthly subscription keeps its price until you stop it.</li>
<li>Every page that may contain partner placements discloses that partner compensation may affect which products we include and where they appear.</li></ul>
<h2>3. Billing</h2><ul><li>Plans are billed in advance, monthly or yearly. A plan goes live, or is extended by its billing period, when payment is confirmed.</li>
<li>Monthly plans paid by card renew automatically each month until you stop the renewal in the portal; the plan then ends at the end of the paid month. Yearly plans cost 12 months minus 10% and don't renew automatically.</li>
<li>If we remove your listing or end your plan early for reasons other than a breach of these terms, we refund the unused part of the paid period.</li>
<li>Impression and visit figures in the portal are for your information and don't affect the price.</li></ul>
<h2>4. Your responsibilities</h2><ul><li>Your product, listing and landing page must be lawful, must not be misleading, and must not infringe anyone's rights.</li>
<li>You're responsible for your own landing pages, tracking and compliance with privacy laws for visitors you receive.</li></ul>
<h2>5. No guarantees</h2><p>We don't guarantee any number of impressions, clicks or conversions. The portal and reports are provided as is.</p>
<h2>6. Changes and termination</h2><p>You can pause listings, let plans lapse or close your account at any time. We may suspend accounts that breach these terms. We may update these terms; material changes will be announced in the portal.</p>
<h2>7. Contact</h2><p>Questions about these terms: <a href="/contact/">contact us</a>.</p>
</div></div>""")
