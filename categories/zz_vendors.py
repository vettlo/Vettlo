# Vendor portal pages: public landing, sign-in, dashboard and admin shells (the app itself is
# src/portal-client.js talking to the Worker API in src/portal.js), plus the advertiser terms draft.

_PSCRIPT = '<script src="/assets/portal.js?v=' + PORTAL_V + '" defer></script>'

page("/vendors/", "Advertise Your Software on Vettlo: Vendor Portal | Vettlo",
     "Put your software in front of buyers comparing tools on Vettlo. Self-serve listings, fixed monthly positions on category shortlists and live reports. No contract, cancel any month.",
     """<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Reach buyers while they compare software.</h1>
<p class="lede">Vettlo readers arrive with a buying question, on shortlists, comparisons and reviews for the category you sell in. List your product and reserve one of the top three positions on your category's shortlist for a flat monthly price.</p>
<div class="ctas"><a class="btn" href="/vendors/login/">Create a vendor account</a><a class="btn ghost" href="/vendors/login/">Sign in</a></div></div>
<aside class="scorecard" aria-label="How placement works"><div class="sc-head"><span>How placement works</span><span class="sc-ex">Per category</span></div>
<ol class="pt-how"><li><b>Three positions per category</b><span>1st, 2nd and 3rd place on the category shortlist, each sold to one vendor at a time.</span></li>
<li><b>Flat monthly price</b><span>One price per position per month, however many readers see or click it.</span></li>
<li><b>No contract</b><span>Renew month by month. When a position is taken, join its waitlist to get it next.</span></li></ol></aside>
</div></section>
<div class="wrap about">
<section><div class="section-head"><div><span class="kicker">How it works</span><h2>Live in four steps</h2></div></div>
<ol class="steps"><li><b>Create an account</b><span>Sign in with your work email; no password needed.</span></li>
<li><b>Add your listing</b><span>Choose a category, add your product details and landing page with UTM parameters.</span></li>
<li><b>Reserve a position</b><span>See which positions are free in your category and reserve one. We hold it for 7 days while you pay.</span></li>
<li><b>Pay and go live</b><span>Once the invoice is paid and our editors approve the listing, your product appears in that position for a month.</span></li></ol></section>
<section><div class="section-head"><div><span class="kicker">Pricing</span><h2>One flat price per position</h2></div></div>
<div class="cards3 aud">
<div class="card"><span class="label">1st place</span><h3 class="card-title">$299 per month</h3><p class="muted small">The first product on the category shortlist, review cards and comparison table.</p></div>
<div class="card"><span class="label">2nd place</span><h3 class="card-title">$199 per month</h3><p class="muted small">Second on the shortlist, review cards and comparison table.</p></div>
<div class="card"><span class="label">3rd place</span><h3 class="card-title">$149 per month</h3><p class="muted small">Third on the shortlist, review cards and comparison table.</p></div></div>
<p class="muted small">Prices are per category, per month, in USD. No setup fee and no contract.</p></section>
<section class="split"><div><span class="kicker">What stays editorial</span><h2>Scores and reviews aren't for sale</h2></div>
<div class="prose"><p>Partner placement changes where your product appears in a category list. It doesn't change your score, our review or what we write about competitors. Every review carries a disclosure that partner compensation may affect which products we include and where they appear.</p>
<p>Listings are reviewed by our editors before they go live. We may edit descriptions for accuracy and decline products that don't fit a category. See the <a href="/advertiser-terms/">advertiser terms</a>.</p></div></section>
<section id="faq"><h2>FAQ</h2><div>""" + "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
        ("Where will my product appear?", "In the position you reserve (1st, 2nd or 3rd) on the shortlist for your category, in the review cards and in the comparison table, with a link to your landing page."),
        ("What if the position I want is taken?", "Join its waitlist. When the current holder doesn't renew, the first vendor on the waitlist gets 72 hours to claim it before it opens to everyone."),
        ("How do I pay?", "Each reservation and renewal creates an invoice for one month. Your position goes live, or is extended by a month, when the invoice is paid. If you don't renew, the position ends at the end of the paid month."),
        ("Can I see results?", "Yes. Your dashboard shows impressions and visits to your site per day and per listing, with a CSV export. Add UTM parameters to your landing page to see conversions in your own analytics."),
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
<nav class="pt-tabs"><button data-tab="overview">Overview</button><button data-tab="listings">Listings</button><button data-tab="placements">Positions</button><button data-tab="newListing">New listing</button><button data-tab="invoices">Invoices</button><button data-tab="reports">Reports</button><button data-tab="account">Account</button></nav>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/vendors/admin/", "Admin: Vettlo Vendor Portal", "Vettlo vendor portal admin.",
     """<div class="wrap pt-app" id="pt-root" data-portal="admin"><div class="pt-top"><div><span class="kicker">Vendor portal</span><h1>Admin</h1></div><div class="pt-topnav"><a href="/vendors/app/">Vendor view</a></div></div>
<div id="pt-view" class="pt-view"><p class="muted">Loading…</p></div><div id="pt-toast" class="pt-toast"></div></div>""" + _PSCRIPT)

page("/advertiser-terms/", "Advertiser Terms | Vettlo",
     "The terms for listing and promoting software on Vettlo through the vendor portal: listings, monthly positions, billing and editorial review.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Advertiser terms</h1>
<p class="small mono">Draft · last updated Nov 2, 2026</p></div><div class="page-body prose">
<p>These terms apply to software vendors ("you") who create listings on Vettlo through the vendor portal. By creating an account you agree to them.</p>
<h2>1. Listings and editorial review</h2><ul><li>Listings go live only after editorial approval. We may edit listing copy for accuracy and clarity, request changes, or decline or remove a listing at our discretion.</li>
<li>You must provide accurate information about your product, pricing and landing page, and keep it up to date. Changes to listing copy are reviewed again before they go live.</li>
<li>Your listing doesn't change your product's Vettlo score, our reviews or what we write about other products.</li></ul>
<h2>2. Positions</h2><ul><li>Each category shortlist has a limited number of paid positions (currently 1st, 2nd and 3rd), each held by one vendor at a time for a paid month.</li>
<li>A reservation holds a position for 7 days while the invoice is paid. Unpaid reservations lapse automatically.</li>
<li>When a position becomes free, the first vendor on its waitlist may claim it within 72 hours before it opens to others.</li>
<li>Your product appears in its position only while the month is paid and the listing is approved and active.</li>
<li>Prices are shown in the portal and may change for future months with notice there; a paid month keeps the price you paid.</li>
<li>Every page that may contain partner placements discloses that partner compensation may affect which products we include and where they appear.</li></ul>
<h2>3. Billing</h2><ul><li>Positions are billed in advance, one month at a time. A position goes live, or is extended by one month, when its invoice is paid.</li>
<li>There's no contract. If you don't renew, the position ends at the end of the paid month.</li>
<li>If we remove your listing or end your position early for reasons other than a breach of these terms, we refund the unused part of the month.</li>
<li>Impression and visit figures in the portal are for your information and don't affect the price.</li></ul>
<h2>4. Your responsibilities</h2><ul><li>Your product, listing and landing page must be lawful, must not be misleading, and must not infringe anyone's rights.</li>
<li>You're responsible for your own landing pages, tracking and compliance with privacy laws for visitors you receive.</li></ul>
<h2>5. No guarantees</h2><p>We don't guarantee any number of impressions, clicks or conversions. The portal and reports are provided as is.</p>
<h2>6. Changes and termination</h2><p>You can pause listings, let positions lapse or close your account at any time. We may suspend accounts that breach these terms. We may update these terms; material changes will be announced in the portal.</p>
<h2>7. Contact</h2><p>Questions about these terms: <a href="/contact/">contact us</a>.</p>
</div></div>""")
