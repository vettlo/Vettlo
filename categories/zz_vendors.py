# Vendor portal pages: public landing, sign-in, dashboard and admin shells (the app itself is
# src/portal-client.js talking to the Worker API in src/portal.js), plus the advertiser terms draft.

_PSCRIPT = '<script src="/assets/portal.js?v=' + PORTAL_V + '" defer></script>'

page("/vendors/", "Vendor Portal: Put Your Software on Vettlo | Vettlo",
     "Pick a category shortlist or alternatives page, choose a position from #1 to #10 and manage it in the Vettlo vendor portal. Our editors review every product.",
     """<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Put your product in front of buyers.</h1>
<p class="lede">Choose a Vettlo page, a category shortlist or an alternatives page, and buy a position from #1 to #10 on it. Monthly or yearly, managed in one portal.</p>
<div class="ctas"><a class="btn" href="/vendors/login/?new=1">Create a vendor account</a><a class="btn ghost" href="/vendors/login/">Sign in</a></div></div>
<aside class="scorecard" aria-label="How it works"><div class="sc-head"><span>How it works</span><span class="sc-ex">3 steps</span></div>
<ol class="pt-how"><li><b>Pick a page</b><span>Any category shortlist or alternatives page in your category.</span></li>
<li><b>Choose a position</b><span>#1 to #10, one vendor per position. Add your product's name and website.</span></li>
<li><b>Go live after review</b><span>Our editors review your product, then it appears at its position. Your paid time starts then.</span></li></ol></aside>
</div></section>
<div class="wrap about">
<section class="split"><div><span class="kicker">What stays editorial</span><h2>Scores and reviews aren't for sale</h2></div>
<div class="prose"><p>A position changes where your product appears on a page. It doesn't change its score, our review or what we write about competitors. Every review discloses that partner compensation may affect which products we include and where they appear. See the <a href="/advertiser-terms/">advertiser terms</a>.</p></div></section>
<section class="about-cta"><div><h2>Ready to get listed?</h2><p>Create your account, pick a page and choose your position.</p></div><a class="btn" href="/vendors/login/?new=1">Go to the vendor portal</a></section>
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

page("/advertiser-terms/", "Advertiser Terms: Positions, Review and Billing | Vettlo",
     "The terms for buying a position on Vettlo: pages and positions #1 to #10, editorial review before going live, reservations, monthly and yearly billing, refunds.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Advertiser terms</h1>
<p>The terms for software vendors who buy a position on Vettlo through the vendor portal. By creating a vendor account you agree to them.</p>
<p class="small mono">Draft · last updated Nov 17, 2026</p></div>
<div class="legal-glance"><h2>At a glance</h2><ul>
<li><b>You pick a page and a position.</b> #1 to #10 on a category shortlist or alternatives page, one vendor per position.</li>
<li><b>We review first.</b> Your product goes live after we publish its review. Paid time starts then.</li>
<li><b>Scores aren't for sale.</b> A position changes where you appear, not what we write.</li>
<li><b>Monthly or yearly.</b> Monthly renews until you stop it; yearly is 10% off and doesn't auto-renew.</li></ul></div>
<div class="legal-grid"><nav class="toc" aria-label="Sections"><span class="label">Sections</span><a href="#pages">1. Pages and positions</a><a href="#review">2. Editorial review</a><a href="#independence">3. What a position doesn't buy</a><a href="#reservations">4. Reservations and waitlists</a><a href="#billing">5. Prices and billing</a><a href="#ending">6. Ending a plan</a><a href="#responsibilities">7. Your responsibilities</a><a href="#guarantees">8. No guarantees</a><a href="#changes">9. Changes to these terms</a><a href="#contact">10. Contact</a></nav>
<div class="page-body prose legal-body">
<section id="pages"><h2>1. Pages and positions</h2><ul><li>You buy a position on a specific page: a category shortlist or an alternatives page in your product's category. Each page has positions #1 to #10, and each position is sold to one vendor at a time.</li>
<li>A position places your product at that place in the page's ranked list, review cards and comparison table. If the list has fewer entries than your position, your product appears at the end of it.</li>
<li>A product can't buy a position on its own alternatives page.</li>
<li>A Basic listing places your product first under “Other tools to consider” on a category shortlist. It's sold yearly and isn't available on alternatives pages.</li></ul></section>
<section id="review"><h2>2. Editorial review</h2><ul><li>You give us your product's name and website. Our editors research the product and write its review and score with the same criteria we use for every tool in the category.</li>
<li>Your product goes live at its position only after its review is published and we approve it. Until then the portal shows it as in editorial review.</li>
<li>If you've already paid, your paid time starts when the product goes live: the days spent in review are added to your plan.</li>
<li>We may decline a product that doesn't fit the category or our standards. If we decline it after you've paid, we refund the full payment.</li></ul></section>
<section id="independence"><h2>3. What a position doesn't buy</h2><ul><li>A position changes where your product appears. It doesn't change its score, our review, or what we write about any other product, and you can't review or edit our text before it's published.</li>
<li>Every page that may contain paid positions discloses that partner compensation may affect which products we include and where they appear.</li></ul></section>
<section id="reservations"><h2>4. Reservations and waitlists</h2><ul><li>Choosing a free position reserves it for you for 7 days while you pay. Unpaid reservations lapse automatically and the position becomes free.</li>
<li>When a position is taken, you can join its waitlist. When it frees up, the first vendor on the waitlist may claim it within 72 hours before it opens to everyone.</li></ul></section>
<section id="billing"><h2>5. Prices and billing</h2><ul><li>Prices are shown in the portal in US dollars and are charged in advance. Yearly plans cost 12 monthly payments minus 10%.</li>
<li>Monthly plans paid by card renew automatically each month until you stop the renewal in the portal. The position then stays live until the end of the paid month. If a renewal payment fails, the position ends when the paid month ends.</li>
<li>Yearly plans don't renew automatically. You can renew from the portal before the year ends.</li>
<li>Prices may change for future billing periods. A paid period keeps the price you paid, and a running monthly subscription keeps its price until you stop it.</li>
<li>Impression and visit figures in the portal are for your information and don't affect the price.</li></ul></section>
<section id="ending"><h2>6. Ending a plan</h2><ul><li>You can stop a monthly renewal, let a yearly plan lapse, pause your listing or close your account at any time.</li>
<li>If we remove your product or end your plan early for a reason other than a breach of these terms, we refund the unused part of the paid period.</li>
<li>We may suspend or end the plans of accounts that breach these terms.</li></ul></section>
<section id="responsibilities"><h2>7. Your responsibilities</h2><ul><li>The information you give us about your product and your landing page must be accurate and lawful, must not be misleading, and must not infringe anyone's rights.</li>
<li>You're responsible for your landing pages, your tracking and your compliance with privacy laws for the visitors we send you.</li></ul></section>
<section id="guarantees"><h2>8. No guarantees</h2><p>We don't guarantee any number of impressions, clicks or sales. The portal and its reports are provided as is.</p></section>
<section id="changes"><h2>9. Changes to these terms</h2><p>We may update these terms. We'll announce material changes in the portal before they apply to your next billing period.</p></section>
<section id="contact"><h2>10. Contact</h2><p>Questions about these terms or a payment: <a href="/contact/">contact us</a>.</p></section>
</div></div></div>""")
