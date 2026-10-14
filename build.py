#!/usr/bin/env python3
"""Vettlo static site generator.

Builds two outputs from the same page definitions:
  dist/site/     -> deploy-ready (Cloudflare Pages / Netlify), clean URLs, full <head> SEO
  dist/preview/  -> artifact preview: relative links to .../index.html, root page without skeleton
"""
import json, os, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
DOMAIN = "https://vettlo.com"
UPDATED = "2026-10-02"
# Pre-launch: keep the whole site out of search results until placeholders are filled.
PRELAUNCH_NOINDEX = False
INDEXNOW_KEY = "c3fbbb23bcc5213c7fb866222a0f102b"
UPDATED_H = "Oct 2, 2026"
YEAR = 2026

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">')

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="var(--brand)"/>'
        '<path d="M8.5 10.5l6.2 12.2c.5 1 1.9 1 2.4 0L24.5 8" fill="none" stroke="var(--brand-ink)" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

STAMP = ('<svg class="stamp stamp-anim" viewBox="0 0 120 120" aria-hidden="true">'
         '<defs><path id="sc" d="M60 60 m-44 0 a44 44 0 1 1 88 0 a44 44 0 1 1 -88 0"/></defs>'
         '<circle cx="60" cy="60" r="56" fill="var(--stamp-soft)" stroke="var(--stamp)" stroke-width="3"/>'
         '<circle cx="60" cy="60" r="34" fill="none" stroke="var(--stamp)" stroke-width="1.5"/>'
         '<text font-family="JetBrains Mono, monospace" font-size="10.5" letter-spacing="3" fill="var(--stamp)" font-weight="700">'
         '<textPath href="#sc">VETTED · NOT FOR SALE · VETTED · NOT FOR SALE ·</textPath></text>'
         '<path d="M45 61l10 10 21-23" fill="none" stroke="var(--stamp)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

DRAFT = ('<div class="draftbar"><div class="wrap"><strong>Draft preview.</strong> Dashed fields '
         '<span class="fill">like this</span> must be filled with verified information before launch.</div></div>')

NAV = [("/best-tools/", "Tools"), ("/topics/", "Guides"), ("/methodology/", "How we vet"), ("/about/", "About")]


def header(cur):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if cur == h else ""}>{t}</a>' for h, t in NAV)
    return f"""<a href="#main" class="eyebrow" style="position:absolute;left:-999px">Skip to content</a>
<div class="topbar"><div class="wrap"><a href="/write-for-us/">Write for us</a><a href="/advertise/">Advertise</a><a href="/contact/">Contact</a></div></div>
<header class="site-head"><div class="wrap">
<a class="brand" href="/">{LOGO}<b>vettlo</b></a>
<nav class="nav" aria-label="Main">{links}<a class="btn small" href="/#newsletter">Get the briefing</a></nav>
</div></header>"""


FOOTER = f"""<footer class="site-foot"><div class="wrap">
<div class="cols">
<div><a class="brand" href="/">{LOGO}<b>vettlo</b></a>
<p>Independent reviews of the software revenue teams run on. Rankings are never for sale.</p></div>
<div><h4>Tools</h4><ul><li><a href="/tools/best-crm-software/">CRM software</a></li><li><a href="/best-tools/">All categories</a></li><li><a href="/contact/">Suggest a tool</a></li></ul></div>
<div><h4>Trust</h4><ul><li><a href="/methodology/">Review methodology</a></li><li><a href="/how-we-make-money/">How we make money</a></li><li><a href="/editorial-standards/">Editorial standards</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About Vettlo</a></li><li><a href="/advertise/">Advertise</a></li><li><a href="/write-for-us/">Write for us</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div>
<div class="legal"><span>© {YEAR} Vettlo. All rights reserved.</span><span><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a></span></div>
</div></footer>"""

NL_SCRIPT = """<script>
document.querySelectorAll('form[data-nl]').forEach(function(f){
  f.addEventListener('submit', function(e){ e.preventDefault();
    var m = f.parentElement.querySelector('.nl-note');
    if (m) m.textContent = 'Thanks. Sign-ups open when the briefing launches; connect your email tool before going live.';
  });
});
</script>"""


def newsletter():
    return """<section class="section" id="newsletter"><div class="wrap"><div class="newsletter">
<div><span class="eyebrow">The Vettlo Briefing</span><h2>One email a week for people who own the revenue stack.</h2>
<p>New reviews, pricing changes we spotted, and what other sales leaders are switching to.</p></div>
<div><form class="nl-form" data-nl><label for="nl-email" style="position:absolute;left:-999px">Work email</label>
<input id="nl-email" type="email" required placeholder="you@company.com" autocomplete="email"><button class="btn" type="submit">Subscribe</button></form>
<p class="nl-note">Free. Unsubscribe anytime.</p></div>
</div></div></section>"""


# ------------------------------------------------------------------ pages
PAGES = {}


def page(path, title, desc, body, cur=None, jsonld=None, ptype="website"):
    PAGES[path] = dict(title=title, desc=desc, body=body, cur=cur, jsonld=jsonld or [], ptype=ptype)


ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Vettlo", "url": DOMAIN,
       "logo": DOMAIN + "/assets/logo.svg", "description": "Independent reviews of B2B software for sales and revenue operations leaders."}

CATS = [
    ("best-crm-software", "CRM Software", "Pipelines, contacts and deal tracking", True),
    ("best-sales-engagement-software", "Sales Engagement Platforms", "Sequenced outreach across email, calls and LinkedIn", True),
    ("best-conversation-intelligence-software", "Conversation Intelligence", "Call recording, transcripts and deal risk signals", True),
    ("best-sales-forecasting-software", "Sales Forecasting Software", "Roll-ups, pipeline inspection and forecast calls", False),
    ("best-revenue-intelligence-platforms", "Revenue Intelligence", "Activity capture and deal health across the funnel", False),
    ("best-b2b-data-providers", "B2B Contact Data Providers", "Enrichment, intent data and list building", True),
    ("best-sales-dialers", "Sales Dialers", "Power, parallel and predictive dialing for outbound", True),
    ("best-cpq-software", "CPQ Software", "Configure, price and quote for complex deals", False),
    ("best-sales-commission-software", "Sales Commission Software", "Comp plans, payouts and rep-facing statements", False),
    ("best-sales-enablement-platforms", "Sales Enablement Platforms", "Content, playbooks and rep onboarding", False),
    ("best-lead-routing-software", "Lead Routing Software", "Speed-to-lead, round robin and territory rules", False),
    ("best-contract-management-software", "Contract Management", "Redlines, e-signature and renewal dates", False),
    ("best-sales-dialers", "Sales Dialers", "Power and parallel dialing for outbound teams", False),
]


def stack_grid(limit=None):
    out = []
    for slug, name, sub, live in CATS[:limit] if limit else CATS:
        if live:
            out.append(f'<a href="/tools/{slug}/"><span class="status is-live">Live review</span><span class="t">{name}</span><span class="s">{sub}</span></a>')
        else:
            out.append(f'<div class="tile"><span class="status is-bench">On the bench</span><span class="t">{name}</span><span class="s">{sub}</span></div>')
    return '<div class="stack-grid">' + "".join(out) + "</div>"


# ---------- HOME
page("/", "Vettlo: Software Reviews for Revenue Teams",
     "Independent reviews of CRM, sales engagement and revenue software for sales and RevOps leaders, scored on published criteria. Rankings are never for sale.",
     f"""
<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">For sales &amp; RevOps leaders</span>
<h1 style="margin-top:.8rem">Software for revenue teams, <em>vetted</em> before you sign the contract.</h1>
<p class="lede">We dig into the CRMs, dialers and forecasting tools your team will live in, score them against published criteria built for each category, and tell you who each one is actually for.</p>
<div class="ctas"><a class="btn" href="/tools/best-crm-software/">Read the CRM review</a><a class="btn ghost" href="/methodology/">How we vet tools</a></div>
</div>
<aside class="seal-card" aria-label="Our review commitments">
<h3 class="card-title">Every Vettlo review</h3>
<div class="check-row">{CHECK}<span>Built on category-specific criteria with published weights</span></div>
<div class="check-row">{CHECK}<span>Names who should <em>not</em> buy the tool</span></div>
<div class="check-row">{CHECK}<span>Labels every sponsored slot, and keeps it outside the ranking</span></div>
<div class="check-row">{CHECK}<span>Re-checked for pricing and features every 90 days</span></div>
</aside>
</div></section>

<section class="section band"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">The revenue tech stack</span><h2 style="margin-top:.4rem">Categories we cover</h2>
<p>One shortlist per category. Live reviews are open; the rest are in research.</p></div>
<a class="btn ghost small" href="/best-tools/">All categories</a></div>
{stack_grid(8)}
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Latest</span><h2 style="margin-top:.4rem">Recently published</h2>
<p>New shortlists and comparisons, with prices checked on the date shown on each page.</p></div></div>
<div class="bench">
<article><div class="meta"><span>Shortlist</span><span>Oct 14, 2026</span></div><h3><a href="/tools/best-sales-dialers/">Best sales dialers</a></h3><p class="muted small">Power dialers vs AI parallel dialers, and which plan the dialer actually sits on.</p></article>
<article><div class="meta"><span>Shortlist</span><span>Oct 14, 2026</span></div><h3><a href="/tools/best-conversation-intelligence-software/">Best conversation intelligence tools</a></h3><p class="muted small">Coaching, deal insights and CRM sync, and which features sit behind add-ons.</p></article>
<article><div class="meta"><span>Shortlist</span><span>Oct 14, 2026</span></div><h3><a href="/tools/best-b2b-data-providers/">Best B2B contact data providers</a></h3><p class="muted small">Coverage, phone data and how each vendor's credits actually work.</p></article>
<article><div class="meta"><span>Shortlist</span><span>Oct 14, 2026</span></div><h3><a href="/tools/best-sales-engagement-software/">Best sales engagement platforms</a></h3><p class="muted small">Sequencing, deliverability and data, plus which vendors hide their prices.</p></article>
</div>
</div></section>

<section class="section band"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Our rules</span><h2 style="margin-top:.4rem">Why buyers trust the shortlist</h2></div><a class="btn ghost small" href="/how-we-make-money/">How we make money</a></div>
<div class="pledges">
<div class="pledge"><span class="n">0</span><h4>Paid rankings</h4><p class="muted small">Vendors cannot buy a position in an editorial list. Featured slots are labeled and sit outside the ranking.</p></div>
<div class="pledge"><span class="n">6</span><h4>Weighted criteria per category</h4><p class="muted small">Published on every review, so you can see why a tool placed where it did.</p></div>
<div class="pledge"><span class="n">90</span><h4>Days between re-checks</h4><p class="muted small">Pricing and plan limits change fast. Every review shows its last verified date.</p></div>
</div>
</div></section>

{newsletter()}
""", cur="/", jsonld=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "Vettlo", "url": DOMAIN}])

# ---------- TOOLS HUB
page("/best-tools/", "Best Sales & Revenue Software by Category | Vettlo",
     "Every software category Vettlo reviews for sales and revenue operations teams, from CRM to commission software.",
     f"""<div class="wrap"><div class="page-head"><span class="eyebrow">Tools</span><h1>The revenue stack, one category at a time</h1>
<p>Each category gets one shortlist, scored on criteria built for that job. Live reviews link through; the rest are being tested.</p></div>
<div class="page-body">{stack_grid()}
<p class="muted small" style="margin-top:1.25rem">Missing a category your team buys? <a href="/contact/">Tell us</a> and we'll add it to the bench.</p>
<h2 style="margin:2.5rem 0 1rem">CRM guides</h2>
<div class="cards3">
<a class="card" href="/tools/best-crm-software/"><span class="label">Shortlist</span><h3>Best CRM Software for Sales Teams</h3><p class="muted small">Our CRM shortlist, scored on six weighted criteria.</p></a>
<a class="card" href="/compare/hubspot-vs-pipedrive/"><span class="label">Comparison</span><h3>HubSpot vs Pipedrive</h3><p class="muted small">What a 10-rep team pays for automation on each.</p></a>
<a class="card" href="/tools/best-pipedrive-alternatives/"><span class="label">Alternatives</span><h3>Best Pipedrive Alternatives</h3><p class="muted small">Six CRMs for teams outgrowing Pipedrive.</p></a>
<a class="card" href="/tools/best-hubspot-alternatives/"><span class="label">Alternatives</span><h3>Best HubSpot Alternatives</h3><p class="muted small">Six CRMs for teams leaving HubSpot Sales Hub.</p></a>
<a class="card" href="/tools/best-crm-for-small-business/"><span class="label">Shortlist</span><h3>Best CRM for Small Businesses</h3><p class="muted small">Weighted toward ease of use and price, with free plans.</p></a>
</div>
<!--CATGUIDES-->
</div></div>
{newsletter()}""", cur="/best-tools/")

# ---------- TOPICS
page("/topics/", "Guides for Sales & RevOps Leaders | Vettlo",
     "Guides on choosing, rolling out and getting value from revenue software.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Guides</span><h1>Guides for people who own the revenue stack</h1>
<p>Buying, rolling out and getting adoption on the tools your reps use every day.</p></div>
<div class="page-body"><div class="cards3">
<div class="card"><span class="label">RevOps</span><h3>Tech stack audits</h3><p class="muted small">Finding overlap, shelfware and missing data flows.</p><span class="status is-bench">First guide drafting</span></div>
<div class="card"><span class="label">Buying</span><h3>Running a software evaluation</h3><p class="muted small">Requirements, trials, reference calls and negotiation.</p><span class="status is-bench">First guide drafting</span></div>
<div class="card"><span class="label">Rollout</span><h3>Adoption and change management</h3><p class="muted small">Getting reps to actually log activity in the new tool.</p><span class="status is-bench">First guide drafting</span></div>
<div class="card"><span class="label">Leadership</span><h3>Interviews with revenue leaders</h3><p class="muted small">CROs and RevOps heads on the tools they kept and the ones they cut.</p><span class="status is-bench">Interviews scheduling</span></div>
</div></div></div>""", cur="/topics/")

# ---------- CRM REVIEW (flagship template)
TOOLS = [
    dict(id="hubspot", name="HubSpot Sales Hub", bf="Best for teams that want marketing and sales on one database",
         what="HubSpot's CRM pairs a free contact and deal database with paid Sales Hub tiers that add sequences, forecasting and custom reporting.",
         who="Inbound-led teams of roughly 5 to 100 reps who already use, or plan to use, HubSpot for marketing.",
         why="It removes the hand-off gap between marketing and sales: lifecycle stages, attribution and deal records live in the same objects, so RevOps does not maintain a sync.",
         pros=["Shared database with marketing removes most sync work", "Free CRM tier makes a low-risk start", "Large integration marketplace"],
         cons=["Costs rise steeply between tiers and with seat count", "Advanced reporting and custom objects sit in upper tiers"],
         notavoid="Teams with complex territory rules or heavy CPQ needs may outgrow the mid tiers."),
    dict(id="pipedrive", name="Pipedrive", bf="Best for small, pipeline-first sales teams",
         what="Pipedrive is a deal-centric CRM built around a visual pipeline, activity reminders and simple automation.",
         who="Founder-led and SMB sales teams that want reps working the pipeline within a day, without an admin.",
         why="The pipeline view and activity prompts push reps toward the next step on every deal, which is where small teams lose the most revenue.",
         pros=["Fast to set up and easy for reps to adopt", "Clear visual pipeline with activity prompts", "Marketplace covers common add-ons"],
         cons=["Reporting is lighter than enterprise CRMs", "Marketing features are add-ons rather than core"],
         notavoid="Not a fit if you need deep account hierarchies or complex permissions."),
    dict(id="salesforce", name="Salesforce Sales Cloud", bf="Best for enterprises with complex sales processes",
         what="Sales Cloud is the most customizable CRM on this list, with a deep ecosystem of apps, consultants and admins.",
         who="Mid-market and enterprise organizations with multiple sales motions, territories and a dedicated admin team.",
         why="When the process is complex, configurability matters more than out-of-the-box simplicity, and nothing on this list matches its depth.",
         pros=["Highly configurable objects, rules and permissions", "Largest app and partner ecosystem", "Scales to very large orgs"],
         cons=["Needs admin resources to configure and maintain", "Total cost goes well beyond the license"],
         notavoid="Overkill for teams under about 20 reps without an admin."),
    dict(id="zoho", name="Zoho CRM", bf="Best for budget-conscious teams that want depth",
         what="Zoho CRM offers workflow automation, territory management and analytics at lower price points, inside the wider Zoho suite.",
         who="SMB and mid-market teams that need more customization than entry-level CRMs but have a tight budget.",
         why="It covers features usually reserved for upper tiers elsewhere, which makes it a strong value pick if your team can handle a denser interface.",
         pros=["Broad feature set for the price", "Fits well with other Zoho apps", "Customizable modules and workflows"],
         cons=["Interface feels dense to new users", "Third-party integrations are thinner than HubSpot or Salesforce"],
         notavoid="Teams that prize a minimal interface may struggle with adoption."),
    dict(id="close", name="Close", bf="Best for high-volume inside sales and calling",
         what="Close is a CRM with built-in calling, SMS and email sequences, built for inside sales teams that live on the phone.",
         who="Inside sales and SDR-heavy teams that make a high volume of calls and want communication inside the CRM.",
         why="Calling, recording and sequencing sit inside the CRM itself, so reps do not toggle between a dialer and a database.",
         pros=["Native calling and SMS inside the CRM", "Built-in email sequences", "Quick for reps to work through call lists"],
         cons=["Less suited to field sales or complex account management", "Smaller app ecosystem"],
         notavoid="Enterprise teams with long, multi-threaded deals may find it limiting."),
    dict(id="attio", name="Attio", bf="Best for startups that want a flexible data model",
         what="Attio is a newer CRM with a flexible, spreadsheet-like data model that syncs email and calendar data to build records automatically.",
         who="Startups and product-led teams that want to model their own objects without hiring an admin.",
         why="Its flexible objects let a small team shape the CRM around a non-standard motion, such as partnerships or product-led sales.",
         pros=["Flexible objects and views without an admin", "Automatic enrichment from email and calendar", "Modern, fast interface"],
         cons=["Younger product with a smaller ecosystem", "Fewer mature sales-specific features than incumbents"],
         notavoid="Teams that need established forecasting and CPQ should look at incumbents first."),
    dict(id="freshsales", name="Freshsales", bf="Best for teams that want built-in AI scoring on a budget",
         what="Freshsales, from Freshworks, combines contact management, deal pipelines, built-in phone and AI-assisted lead scoring.",
         who="SMB teams that want calling, email and lead scoring in one product without stitching tools together.",
         why="It bundles phone, email and lead scoring that competitors often sell separately, which keeps the stack small.",
         pros=["Built-in phone and email", "AI-assisted lead and deal scoring", "Pairs with Freshdesk for support teams"],
         cons=["Customization is narrower than Salesforce or Zoho", "Reporting depth varies by tier"],
         notavoid="Not ideal if your process needs heavy custom objects."),
    dict(id="folk", name="folk", bf="Best for relationship-led teams and founders",
         what="folk is a lightweight CRM for managing relationships and outreach, with contact enrichment and simple pipelines.",
         who="Founders, agencies and partnership teams that manage relationships more than high-volume pipelines.",
         why="It keeps the overhead near zero, which matters for teams where nobody's full-time job is CRM hygiene.",
         pros=["Very low setup and maintenance overhead", "Easy contact import and enrichment", "Simple outreach from the CRM"],
         cons=["Not built for large sales teams", "Limited forecasting and reporting"],
         notavoid="Teams above about 10 quota-carrying reps will likely outgrow it."),
]

PRICING = {
    "hubspot":    dict(price="$7/seat/mo", note="Starter, billed annually ($20 monthly)", trial="Free plan (up to 2 users)", short="Free plan for 2 users"),
    "pipedrive":  dict(price="$14/seat/mo", note="Lite, billed annually", trial="14-day free trial", short="14-day trial"),
    "salesforce": dict(price="$25/user/mo", note="Starter Suite, monthly or annual", trial="Free Suite + free trial", short="Free Suite + trial"),
    "zoho":       dict(price="$14/user/mo", note="Standard, billed annually ($20 monthly)", trial="Free for 3 users; 15-day trial", short="Free for 3 users"),
    "close":      dict(price="$35/user/mo", note="Essentials, billed annually ($9 Solo plan for 1 user)", trial="14-day free trial", short="14-day trial"),
    "attio":      dict(price="$35/user/mo", note="Plus, billed annually ($44 monthly)", trial="Free plan (3 seats); 14-day Pro trial", short="Free plan for 3 seats"),
    "freshsales": dict(price="$9/user/mo", note="Growth, billed annually", trial="21-day free trial", short="21-day trial"),
    "folk":       dict(price="$24/user/mo", note="Standard, billed annually ($30 monthly)", trial="14-day free trial", short="14-day trial"),
}
PRICES_CHECKED = "Oct 2, 2026"

G2 = {
    "hubspot":    ("4.4", "14,347", "https://www.g2.com/products/hubspot-sales-hub/reviews"),
    "pipedrive":  ("4.3", "5,040",  "https://www.g2.com/products/pipedrive/reviews"),
    "salesforce": ("4.4", "27,564", "https://www.g2.com/products/salesforce-salesforce-sales-cloud/reviews"),
    "zoho":       ("4.1", "2,951",  "https://www.g2.com/products/zoho-crm/reviews"),
    "close":      ("4.7", "2,104",  "https://www.g2.com/products/close/reviews"),
    "attio":      ("4.3", "594",    "https://www.g2.com/products/attio/reviews"),
    "freshsales": ("4.5", "1,236",  "https://www.g2.com/products/freshsales/reviews"),
    "folk":       ("4.5", "343",    "https://www.g2.com/products/folk-folk/reviews"),
}


URLS = {'hubspot': 'https://www.hubspot.com/products/sales', 'pipedrive': 'https://www.pipedrive.com/', 'salesforce': 'https://www.salesforce.com/sales/', 'zoho': 'https://www.zoho.com/crm/', 'close': 'https://www.close.com/', 'attio': 'https://attio.com/', 'freshsales': 'https://www.freshworks.com/crm/sales/', 'folk': 'https://www.folk.app/'}

CRITERIA = [("Pipeline & deal management", 25), ("Automation & workflows", 20), ("Reporting & forecasting", 20),
            ("Integrations & data quality", 15), ("Usability & rep adoption", 10), ("Price & value", 10)]

SCORES = {  # 0-5 per criterion, same order as CRITERIA. Desk research, Oct 2, 2026.
    "salesforce": [5, 5, 5, 5, 3, 2.5],
    "hubspot":    [4.5, 4.5, 4.5, 5, 4.5, 3],
    "pipedrive":  [4.5, 3.5, 3.5, 4, 5, 4.5],
    "zoho":       [4, 4, 4, 3.5, 3, 5],
    "freshsales": [4, 3.5, 3.5, 3.5, 4, 4.5],
    "close":      [4, 4, 3.5, 3, 4.5, 3.5],
    "attio":      [4, 3.5, 3, 3.5, 4.5, 4],
    "folk":       [3, 2.5, 2, 3, 5, 4],
}
THRESHOLD = 70


def score(tid):
    return round(sum(w * r for (_, w), r in zip(CRITERIA, SCORES[tid])) / 5)


CONSIDERED = list(TOOLS)
EXCLUDED = [t for t in TOOLS if score(t["id"]) < THRESHOLD]
TOOLS = sorted([t for t in TOOLS if score(t["id"]) >= THRESHOLD], key=lambda t: -score(t["id"]))

FAQS = [
    ("What is the best CRM for a small sales team?", "For teams under about 10 reps, ease of adoption usually matters more than feature depth. Pipedrive and HubSpot's entry tiers are the most common starting points; Attio suits founder-led teams that want a flexible setup, and folk is a lighter option for relationship-led work. See our guide to the best CRM for small businesses. Start a trial with your real pipeline before deciding."),
    ("How much does CRM software cost?", "Most CRMs price per seat per month, with free or entry tiers for small teams and steep jumps for automation, forecasting and custom objects. Budget for implementation, data migration and integrations too, which can exceed license cost at enterprise scale."),
    ("Should sales and marketing share one CRM?", "Sharing one database removes sync work and makes attribution easier. It matters most for inbound-led motions. Outbound-heavy teams with separate marketing tools can run well with a sales-first CRM and a clean integration."),
    ("How long does a CRM migration take?", "Small teams can move in days. Mid-market migrations with custom fields, historical activity and integrations commonly take several weeks. Plan field mapping and deduplication before the cutover."),
    ("How does Vettlo choose which CRMs to include?", "We start from a long list of CRMs used by sales teams, score each against the six weighted criteria on this page, and include tools that clear our threshold. Vendors cannot pay for inclusion or position."),
]


def breakdown(tid):
    return "".join(f'<div class="crit"><span class="nm">{n} <span class="muted small">({w}%)</span></span><span class="w">{r:g}/5</span><span class="bar"><i style="width:{r*20}%"></i></span></div>'
                   for (n, w), r in zip(CRITERIA, SCORES[tid]))


def also_considered():
    if not EXCLUDED:
        return ""
    items = "".join(f'<li><b>{t["name"]}</b> scored {score(t["id"])}/100. {t["what"]} It\'s a good fit for {t["who"][0].lower() + t["who"][1:]} It fell short of our {THRESHOLD}-point bar mainly on reporting and forecasting, which matter for most sales teams. It does make our <a href="/tools/best-crm-for-small-business/">CRM shortlist for small businesses</a>, where ease of use and price carry more weight.</li>' for t in EXCLUDED)
    return f'<section id="also"><h2>Also considered</h2><ul class="prose">{items}</ul></section>'


def crm_page():
    short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{t["id"]}">{t["name"]}</a><br><span class="bf">{t["bf"]}</span></span><a class="btn ghost small" href="#{t["id"]}">Review</a></li>'
                    for i, t in enumerate(TOOLS, 1))
    rows = "".join(f'<tr><td class="num">{i}</td><td><a href="#{t["id"]}"><b>{t["name"]}</b></a></td><td>{t["bf"].replace("Best for ", "")[:1].upper() + t["bf"].replace("Best for ", "")[1:]}</td>'
                   f'<td>{PRICING[t["id"]]["short"]}</td><td class="num">From {PRICING[t["id"]]["price"]}</td><td class="num">{G2[t["id"]][0]}/5</td><td class="num"><b>{score(t["id"])}</b>/100</td></tr>'
                   for i, t in enumerate(TOOLS, 1))
    cards = []
    for i, t in enumerate(TOOLS, 1):
        pros = "".join(f"<li>{p}</li>" for p in t["pros"])
        cons = "".join(f"<li>{c}</li>" for c in t["cons"])
        cards.append(f"""<article class="tool" id="{t['id']}">
<div class="tool-head"><span class="num">{i}</span><div><h3>{t['name']}</h3><div class="bestfor">{t['bf']}</div></div>
<a class="btn small" href="{URLS[t['id']]}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
<div class="spec"><div><span class="label">Starting price</span><b>From {PRICING[t['id']]['price']}</b><span class="small muted">{PRICING[t['id']]['note']}</span></div><div><span class="label">Free trial / plan</span><b>{PRICING[t['id']]['trial']}</b></div><div><span class="label">Vettlo score</span><b>{score(t['id'])}/100</b><span class="small muted">Desk research</span></div><div><span class="label">G2 user rating</span><b>{G2[t['id']][0]}/5</b><a class="small" href="{G2[t['id']][2]}" target="_blank" rel="noopener">{G2[t['id']][1]} reviews</a></div></div>
<div class="tool-body">
<p>{t['what']}</p>
<div><h4>Who it's best for</h4><p>{t['who']}</p></div>
<div><h4>Why it made the shortlist</h4><p>{t['why']}</p></div>
<div class="pc"><div class="pros"><h4>Strengths</h4><ul>{pros}</ul></div><div class="cons"><h4>Watch-outs</h4><ul>{cons}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {t['notavoid']}</p>{('<p class="small"><a href="/compare/hubspot-vs-pipedrive/">Compare HubSpot vs Pipedrive →</a> · <a href="/tools/best-' + t['id'] + '-alternatives/">' + ('HubSpot' if t['id']=='hubspot' else 'Pipedrive') + ' alternatives →</a></p>') if t['id'] in ('hubspot','pipedrive') else ''}
<details class="breakdown"><summary>Score breakdown</summary><div class="criteria">{breakdown(t['id'])}</div></details>
</div>
</article>""")
    crit = "".join(f'<div class="crit"><span class="nm">{n}</span><span class="w">{w}%</span><span class="bar"><i style="width:{w*4}%"></i></span></div>' for n, w in CRITERIA)
    faq = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)
    toc = "".join(f'<a href="#{a}">{b}</a>' for a, b in [("shortlist", "Shortlist"), ("compare", "Comparison table"), ("reviews", "Reviews"), ("criteria", "How we scored"), ("choose", "How to choose"), ("pricing", "Pricing"), ("faq", "FAQ")])

    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/best-tools/">Tools</a> / CRM Software</nav>
<header class="article-head">
<span class="eyebrow">Shortlist · CRM software</span>
<h1>{len(TOOLS)} Best CRM Software for Sales Teams in {YEAR}</h1>
<div class="byline"><div class="avatar team-mark">{LOGO}</div><div class="who"><b>By <a href="/team/">Vettlo Editorial Team</a></b><span>Last verified <time datetime="{UPDATED}">{UPDATED_H}</time></span></div></div>
<p class="disclose">We may earn a commission when you click some links on this page. It never changes which tools we include or how we rank them. See <a href="/how-we-make-money/">how we make money</a> and our <a href="/methodology/">review methodology</a>.</p>
</header>
<div class="layout">
<div class="main-col">

<section class="prose"><p>A CRM is the system your reps will open more than any other tool, so a bad pick shows up as missing activity data, unreliable forecasts and reps keeping deals in spreadsheets. We built this shortlist for sales and RevOps leaders choosing a CRM for a team of 5 to 500 reps.</p>
<p>Each tool below was scored against six weighted criteria, listed in <a href="#criteria">How we scored</a>. For each one we say who it's for and, just as important, who should skip it.</p></section>

<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>

<aside class="trust" aria-label="Why trust this review">
<span class="label">Why trust this review</span>
<div class="facts"><div><b>{len(CONSIDERED)} CRMs</b><span class="small muted">scored</span></div><div><b>6</b><span class="small muted">weighted criteria</span></div><div><b>0</b><span class="small muted">paid positions</span></div><div><b>90 days</b><span class="small muted">re-check cycle</span></div></div>
<p class="small muted">Scores on this page come from desk research: each vendor's documentation and pricing pages plus patterns in G2 user reviews, checked on {UPDATED_H}. Hands-on trials are under way and we'll add test notes and screenshots as they finish. Vendors cannot pay for a position.</p>
</aside>

<section id="compare"><h2>CRM comparison at a glance</h2>
<div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Best for</th><th>Free plan / trial</th><th>Starting price</th><th>G2 rating</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div></section>

<aside class="sponsored" aria-label="Sponsored placement">
<span class="tag">Sponsored · Not part of our ranking</span>
<h3 style="font-size:1.05rem">Featured partner slot</h3>
<p class="small">A paying vendor can appear here, clearly labeled and kept separate from the editorial shortlist above. <a href="/advertise/">How featured slots work</a>.</p>
</aside>

<section id="reviews"><h2>The reviews</h2>{"".join(cards)}</section>

{also_considered()}

<section id="criteria"><h2>How we scored CRM software</h2>
<p class="prose">Each tool gets a 0 to 5 rating on every criterion. We weight the ratings below, convert the total to a percentage, and only include tools that score 70 or higher out of 100. For this edition, ratings come from desk research (documentation, pricing pages and G2 reviews); open any tool's <b>Score breakdown</b> to see its six ratings. Full process on our <a href="/methodology/">methodology page</a>.</p>
<div class="criteria">{crit}</div></section>

<section id="choose" class="prose"><h2>How to choose a CRM</h2>
<ul>
<li><b>Map your motion first.</b> Inbound, outbound, partner-led and product-led sales need different objects and automation. Write down the stages a deal passes through before you open a trial.</li>
<li><b>Count every seat that will touch it.</b> Managers, SDRs, CS and finance often need access. Per-seat pricing changes fast when you include them.</li>
<li><b>Test your three hardest workflows.</b> Lead routing, multi-contact deals and forecast roll-ups expose limits quickly. Run them with your own data during the trial.</li>
<li><b>Check the data exit.</b> Confirm you can export activity history and custom fields, not only contacts.</li>
<li><b>Price the whole first year.</b> Add implementation, migration, integrations and admin time to the license.</li>
</ul></section>

<section id="pricing"><h2>What CRM software costs</h2>
<div class="table-wrap"><table><thead><tr><th>Plan type</th><th>Typical price</th><th>What you usually get</th><th>Best for</th></tr></thead><tbody>
<tr><td>Free</td><td class="num">$0</td><td>Contacts, deals, basic pipeline, limited users or features</td><td>Founders and very small teams</td></tr>
<tr><td>Entry</td><td class="num">$7–25 /seat/mo</td><td>Pipelines, email sync, basic automation</td><td>SMB teams under 10 reps</td></tr>
<tr><td>Growth</td><td class="num">$35–100 /seat/mo</td><td>Sequences, forecasting, custom reports</td><td>Scaling teams with RevOps</td></tr>
<tr><td>Enterprise</td><td class="num">$59–195+ /seat/mo</td><td>Custom objects, territories, advanced permissions</td><td>Complex, multi-team orgs</td></tr>
</tbody></table></div>
<p class="small muted">Ratings in the table and cards are G2 averages as of {PRICES_CHECKED}. Ranges are list prices for the CRMs on this page, billed annually, in USD, as published on each vendor's pricing page on {PRICES_CHECKED}. Monthly billing usually costs 20–40% more. Some vendors add one-time onboarding fees on upper tiers; HubSpot, for example, charges $1,500 for Sales Hub Professional onboarding.</p></section>

<section id="faq"><h2>CRM software FAQ</h2><div>{faq}</div></section>

<section class="author-box"><div class="avatar team-mark">{LOGO}</div><div><b>Vettlo Editorial Team</b><p class="small muted">This review was researched and written by the Vettlo editorial team using the process on our <a href="/methodology/">methodology page</a>. Hands-on testing is in progress; individual reviewer profiles will be added to each review as testers sign off.</p><p class="small"><a href="/team/">About the editorial team</a></p></div></section>
</div>
<nav class="toc" aria-label="On this page"><span class="label">On this page</span>{toc}</nav>
</div></div>
{newsletter()}"""

    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": f"{len(TOOLS)} Best CRM Software for Sales Teams in {YEAR}",
         "datePublished": "2026-10-02", "dateModified": UPDATED, "author": {"@type": "Organization", "name": "Vettlo Editorial Team", "url": DOMAIN + "/team/"},
         "publisher": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN},
         "mainEntityOfPage": DOMAIN + "/tools/best-crm-software/"},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "Best CRM software",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": t["name"], "url": f"{DOMAIN}/tools/best-crm-software/#{t['id']}"} for i, t in enumerate(TOOLS, 1)]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": DOMAIN + "/best-tools/"},
            {"@type": "ListItem", "position": 3, "name": "CRM Software", "item": DOMAIN + "/tools/best-crm-software/"}]},
    ]
    page("/tools/best-crm-software/", f"{len(TOOLS)} Best CRM Software for Sales Teams ({YEAR}) | Vettlo",
         "We compared CRMs for sales teams of 5 to 500 reps on six weighted criteria. See who each CRM is for, who should skip it, and what it costs.",
         body, cur="/best-tools/", jsonld=ld, ptype="article")


crm_page()

# ---------- ALTERNATIVES PAGES
TOOL_BY_ID = {t["id"]: t for t in CONSIDERED}
SHORT = {"hubspot": "HubSpot", "pipedrive": "Pipedrive", "salesforce": "Salesforce", "zoho": "Zoho CRM",
         "close": "Close", "attio": "Attio", "freshsales": "Freshsales", "folk": "folk"}
ENTRY_PRICE = {"hubspot": 7, "pipedrive": 14, "salesforce": 25, "zoho": 14, "close": 35, "attio": 35, "freshsales": 9}


def alt_page(target, slug, lede, reasons, picks, faqs, related):
    tname = SHORT[target]
    tfull = TOOL_BY_ID[target]["name"]
    url = f"/tools/{slug}/"
    n = len(picks)
    short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{tid}">{TOOL_BY_ID[tid]["name"]}</a><br><span class="bf">{fit}</span></span><a class="btn ghost small" href="#{tid}">Details</a></li>'
                    for i, (tid, fit, _, _) in enumerate(picks, 1))
    rows = "".join(f'<tr><td><a href="#{tid}"><b>{TOOL_BY_ID[tid]["name"]}</b></a></td><td>{fit}</td><td class="num">From {PRICING[tid]["price"]}</td><td>{PRICING[tid]["short"]}</td><td class="num">${ENTRY_PRICE[tid]*120:,}</td><td class="num"><b>{score(tid)}</b>/100</td></tr>'
                   for tid, fit, _, _ in picks)
    rows = (f'<tr class="ref"><td><b>{tfull}</b> <span class="small muted">(for reference)</span></td><td>{TOOL_BY_ID[target]["bf"].replace("Best for ", "").capitalize()}</td><td class="num">From {PRICING[target]["price"]}</td><td>{PRICING[target]["short"]}</td><td class="num">${ENTRY_PRICE[target]*120:,}</td><td class="num"><b>{score(target)}</b>/100</td></tr>' + rows)
    cards = []
    for i, (tid, fit, gain, lose) in enumerate(picks, 1):
        t = TOOL_BY_ID[tid]
        cards.append(f"""<article class="tool" id="{tid}">
<div class="tool-head"><span class="num">{i}</span><div><h3>{t['name']}</h3><div class="bestfor">{fit}</div></div>
<a class="btn small" href="{URLS[tid]}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
<div class="spec"><div><span class="label">Starting price</span><b>From {PRICING[tid]['price']}</b><span class="small muted">{PRICING[tid]['note']}</span></div><div><span class="label">Free trial / plan</span><b>{PRICING[tid]['trial']}</b></div><div><span class="label">Vettlo score</span><b>{score(tid)}/100</b><span class="small muted">Desk research</span></div><div><span class="label">G2 user rating</span><b>{G2[tid][0]}/5</b><a class="small" href="{G2[tid][2]}" target="_blank" rel="noopener">{G2[tid][1]} reviews</a></div></div>
<div class="tool-body">
<p>{t['what']}</p>
<div class="pc"><div class="pros"><h4>What you gain over {tname}</h4><ul>{''.join(f'<li>{g}</li>' for g in gain)}</ul></div><div class="cons"><h4>What you give up</h4><ul>{''.join(f'<li>{l}</li>' for l in lose)}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {t['notavoid']}</p>
</div></article>""")
    reason_html = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in reasons)
    faq_html = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    rel_html = "".join(f'<li><a href="{h}">{x}</a></li>' for h, x in related)
    title = f"{n} Best {tname} Alternatives for Sales Teams ({YEAR}) | Vettlo"
    h1 = f"{n} Best {tname} Alternatives for Sales Teams in {YEAR}"
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/tools/best-crm-software/">CRM Software</a> / {tname} alternatives</nav>
<header class="article-head">
<span class="eyebrow">Alternatives · CRM software</span>
<h1>{h1}</h1>
<div class="byline"><div class="avatar team-mark">{LOGO}</div><div class="who"><b>By <a href="/team/">Vettlo Editorial Team</a></b><span>Published <time datetime="{ALT_DATE}">{ALT_DATE_H}</time> · Prices verified {PRICES_CHECKED}</span></div></div>
<p class="disclose">We may earn a commission when you click some links on this page. It never changes which tools we include or how we rank them. See <a href="/how-we-make-money/">how we make money</a>.</p>
</header>
<div class="layout"><div class="main-col">
<section class="prose"><p>{lede}</p></section>
<section class="prose" id="why"><h2>Why teams look for {tname} alternatives</h2><ul>{reason_html}</ul></section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<section id="compare"><h2>{tname} alternatives compared</h2>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Why pick it</th><th>Starting price</th><th>Free plan / trial</th><th>10 seats, year one*</th><th>Vettlo score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">*Entry plan list price × 10 seats × 12 months, billed annually, from each vendor's pricing page on {PRICES_CHECKED}. Entry plans differ in features; see each tool below. Scores use the same six weighted criteria as our <a href="/tools/best-crm-software/">CRM rankings</a>.</p></section>
<section id="reviews"><h2>The alternatives</h2>{''.join(cards)}</section>
<section class="prose" id="how"><h2>How we picked these alternatives</h2><p>Every tool here is from our <a href="/tools/best-crm-software/">CRM shortlist</a> and cleared our 70-point bar. We ordered them by how well each one solves the most common reasons teams leave {tname}, not only by overall score. Scores come from desk research (vendor documentation, current pricing pages and G2 reviews); see our <a href="/methodology/">methodology</a>.</p></section>
<section id="faq"><h2>{tname} alternatives FAQ</h2><div>{faq_html}</div></section>
<section class="prose"><h2>Related</h2><ul>{rel_html}</ul></section>
<section class="author-box"><div class="avatar team-mark">{LOGO}</div><div><b>Vettlo Editorial Team</b><p class="small muted">Researched and written by the Vettlo editorial team using our <a href="/methodology/">methodology</a>.</p></div></section>
</div>
<nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#why">Why switch</a><a href="#shortlist">Shortlist</a><a href="#compare">Comparison table</a><a href="#reviews">The alternatives</a><a href="#faq">FAQ</a></nav>
</div></div>
{newsletter()}"""
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": h1, "datePublished": ALT_DATE, "dateModified": ALT_DATE,
         "author": {"@type": "Organization", "name": "Vettlo Editorial Team", "url": DOMAIN + "/team/"},
         "publisher": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN}, "mainEntityOfPage": DOMAIN + url},
        {"@context": "https://schema.org", "@type": "ItemList", "name": f"Best {tname} alternatives",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": TOOL_BY_ID[tid]["name"], "url": f"{DOMAIN}{url}#{tid}"} for i, (tid, _, _, _) in enumerate(picks, 1)]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "CRM Software", "item": DOMAIN + "/tools/best-crm-software/"},
            {"@type": "ListItem", "position": 3, "name": f"{tname} alternatives", "item": DOMAIN + url}]},
    ]
    desc = f"The best {tname} alternatives for sales teams, compared on price, free plans, features and fit. What you gain and give up with each, plus year-one cost for 10 seats."
    page(url, title, desc, body, cur="/best-tools/", jsonld=ld, ptype="article")


ALT_DATE = "2026-10-14"
ALT_DATE_H = "Oct 14, 2026"

alt_page("pipedrive", "best-pipedrive-alternatives",
         "Pipedrive is one of the easiest CRMs for a small, pipeline-first sales team to adopt. Teams usually start looking elsewhere when they need marketing and sales on one database, deeper reporting across several teams, or calling built into the CRM. These are the alternatives we'd shortlist for each of those reasons.",
         [("You need marketing and sales on one database.", "Pipedrive's marketing features are add-ons rather than core, so inbound-led teams often end up syncing two systems."),
          ("Reporting needs outgrow the pipeline view.", "Pipedrive lists custom-data reports from its Premium plan, and multi-team forecasting is lighter than enterprise CRMs."),
          ("Your process gets complex.", "Deep account hierarchies, territories and granular permissions are where Pipedrive is weakest."),
          ("You want calling inside the CRM.", "Pipedrive's pricing page doesn't list built-in calling, so phone-heavy teams often add a separate dialer.")],
         [("hubspot", "Best if you want marketing and sales on one database",
           ["Marketing, lifecycle stages and attribution in the same records", "Free plan for up to 2 users", "Deeper custom reporting on Professional"],
           ["Sequences and forecasting are listed from Professional ($90/seat/mo + $1,500 onboarding), against Pipedrive Growth at $39", "More setup than Pipedrive"]),
          ("zoho", "Best for more depth on a similar budget",
           ["Territory management, workflow automation and analytics at entry-level prices", "Free edition for up to 3 users", "Fits the wider Zoho suite"],
           ["A denser interface that takes reps longer to learn", "Thinner third-party integrations than HubSpot or Salesforce"]),
          ("freshsales", "Best for built-in phone and lead scoring on a budget",
           ["Built-in phone and email", "AI-assisted lead and deal scoring", "Lowest entry price on this list at $9/user/mo"],
           ["Narrower customization than Salesforce or Zoho", "Reporting depth varies by tier"]),
          ("close", "Best for phone-heavy inside sales teams",
           ["Calling, SMS and email sequences inside the CRM", "Fast to work through call lists"],
           ["Workflows and the power dialer are listed from Close's Growth plan ($99/user/mo)", "Less suited to field sales or complex account management"]),
          ("salesforce", "Best when your process outgrows Pipedrive",
           ["The deepest customization of objects, rules and permissions", "The largest app and partner ecosystem", "Scales to very large organizations"],
           ["Needs admin resources to configure and maintain", "Total cost goes well beyond the license"]),
          ("attio", "Best for startups that want a flexible data model",
           ["Model your own objects, such as partners or investors, without an admin", "Records built automatically from email and calendar", "Free plan for up to 3 seats"],
           ["Younger product with a smaller ecosystem", "Fewer mature forecasting features than incumbents"])],
         [("What is the best free alternative to Pipedrive?", "Pipedrive has no free plan. HubSpot's free plan covers up to 2 users, Zoho CRM's free edition covers up to 3 users, and Attio's free plan covers up to 3 seats."),
          ("What is cheaper than Pipedrive?", "On entry list prices billed annually, Freshsales Growth ($9/user/mo) and HubSpot Sales Hub Starter ($7/seat/mo) start below Pipedrive Lite ($14). Zoho CRM Standard matches it at $14. Compare plan features too: entry plans differ in what they include."),
          ("Is HubSpot better than Pipedrive?", "HubSpot is better if your marketing runs on HubSpot or you need deep custom reporting. Pipedrive is better value if you need sequences, automation and forecast reports without HubSpot Professional pricing. See our full HubSpot vs Pipedrive comparison."),
          ("Which Pipedrive alternative is best for enterprise teams?", "Salesforce Sales Cloud, which scores highest in our CRM rankings for pipeline management, automation and reporting, though it needs admin resources and costs more in total.")],
         [("/compare/hubspot-vs-pipedrive/", "HubSpot vs Pipedrive"), ("/tools/best-hubspot-alternatives/", "Best HubSpot alternatives"), ("/tools/best-crm-software/", "Best CRM software for sales teams")])

alt_page("hubspot", "best-hubspot-alternatives",
         "HubSpot Sales Hub is a strong CRM, especially when marketing already runs on HubSpot. Teams usually look elsewhere when they need sales automation without the jump to Professional pricing, want something simpler for reps, or need a phone-first or enterprise-grade tool. These are the alternatives we'd shortlist.",
         [("The jump to Professional.", "HubSpot lists email sequences and forecasting on Sales Hub Professional at $90 per seat per month plus a $1,500 one-time onboarding fee, against $7 for Starter."),
          ("Costs that grow with seats.", "Per-seat pricing across tiers adds up quickly as a sales team grows."),
          ("More CRM than the team needs.", "Small pipeline-first teams sometimes find HubSpot's breadth slows reps down."),
          ("Very complex processes.", "Large organizations with territories and multi-team rules may need deeper customization.")],
         [("pipedrive", "Best for sales automation without Professional pricing",
           ["Sequences, workflow automation and forecast reports listed on the $39 Growth plan", "Fast for reps to adopt, no admin needed", "No onboarding fee listed"],
           ["No free plan (14-day trial instead)", "Marketing is an add-on, not a shared database"]),
          ("zoho", "Best for depth on a tight budget",
           ["Workflow automation, territories and analytics at lower prices", "Free edition for up to 3 users"],
           ["A denser interface", "Thinner third-party integrations"]),
          ("freshsales", "Best for an all-in-one sales CRM at a low price",
           ["Built-in phone, email and AI-assisted lead scoring", "Entry price of $9/user/mo billed annually", "21-day free trial"],
           ["Narrower customization", "Reporting depth varies by tier"]),
          ("salesforce", "Best for enterprises with complex processes",
           ["Deepest customization and largest ecosystem", "Scales to very large organizations"],
           ["Needs admin resources", "Total cost goes well beyond the license"]),
          ("close", "Best for phone-heavy inside sales teams",
           ["Calling, SMS and sequences built in", "Quick to work through call lists"],
           ["Workflows and the power dialer are listed from the $99 Growth plan", "Less suited to field sales"]),
          ("attio", "Best for startups that want a flexible data model",
           ["Flexible objects and views without an admin", "Free plan for up to 3 seats"],
           ["Younger product with a smaller ecosystem", "Fewer mature forecasting features"])],
         [("What is the best alternative to HubSpot Sales Hub?", "For most small and mid-sized sales teams, Pipedrive: it lists sequences, automation and forecast reports on its $39 Growth plan, while HubSpot lists sequences and forecasting from Professional at $90 per seat plus onboarding. Enterprises with complex processes should look at Salesforce."),
          ("Is there a free alternative to HubSpot?", "HubSpot itself has a free plan for up to 2 users. Zoho CRM's free edition covers up to 3 users and Attio's free plan covers up to 3 seats."),
          ("What is cheaper than HubSpot Sales Hub Professional?", "Pipedrive Growth ($39/seat/mo), Freshsales Pro ($39/user/mo) and Zoho CRM Professional are all listed well below HubSpot Professional's $90 per seat, and none lists an onboarding fee. Check that each plan covers the workflows you need."),
          ("Should I leave HubSpot if my marketing runs on it?", "Usually not. The shared database between marketing and sales is HubSpot's biggest advantage. Leaving means maintaining a sync between two systems.")],
         [("/compare/hubspot-vs-pipedrive/", "HubSpot vs Pipedrive"), ("/tools/best-pipedrive-alternatives/", "Best Pipedrive alternatives"), ("/tools/best-crm-software/", "Best CRM software for sales teams")])

# ---------- BEST CRM FOR SMALL BUSINESS
SB_WEIGHTS = [20, 15, 10, 5, 25, 25]  # same order as CRITERIA
SB_DATE = "2026-10-14"
SB_DATE_H = "Oct 14, 2026"
ENTRY_PRICE["folk"] = 24


def sb_score(tid):
    return int(sum(w * r for w, r in zip(SB_WEIGHTS, SCORES[tid])) / 5 + 0.5)


SB_FIT = {
    "pipedrive": ("Best overall for small sales teams", "Reps can work the pipeline within a day, and sequences, automation and forecast reports arrive on the $39 Growth plan."),
    "hubspot": ("Best free CRM to start with", "The free plan covers up to 2 users, and you can grow into marketing and sales on one database later."),
    "zoho": ("Best for depth on a small budget", "Workflow automation, territories and analytics at entry-level prices, plus a free edition for up to 3 users."),
    "freshsales": ("Best low-cost all-in-one", "Phone, email and AI-assisted lead scoring in one product from $9 per user per month on annual billing."),
    "attio": ("Best for startups with a non-standard process", "Model partners, investors or a product-led funnel without an admin, with a free plan for up to 3 seats."),
    "close": ("Best for small phone-based sales teams", "Calling, SMS and email sequences inside the CRM; a $9 Solo plan covers a single user."),
    "salesforce": ("Best if you expect to scale fast", "Starter Suite from $25 per user per month gives you a path into the deepest CRM platform without migrating later."),
    "folk": ("Best for founders and relationship-led work", "Very little setup or upkeep, easy contact enrichment and simple outreach for teams where nobody owns the CRM full time."),
}
SB_ORDER = sorted([t for t in SB_FIT if sb_score(t) >= THRESHOLD], key=lambda t: (-sb_score(t), ENTRY_PRICE[t]))

SB_FAQS = [
    ("What is the best CRM for a small business?", f"For most small sales teams, Pipedrive: it scores highest in our small-business ranking ({sb_score('pipedrive')}/100) because reps adopt it quickly and it lists sequences, automation and forecast reports on its $39 Growth plan. If you need a free start, HubSpot's free plan covers up to 2 users."),
    ("What is the best free CRM for a small business?", "HubSpot's free plan covers up to 2 users, Zoho CRM's free edition covers up to 3 users, and Attio's free plan covers up to 3 seats. Pipedrive, Freshsales, Close and folk offer free trials instead of free plans."),
    ("How much should a small business spend on a CRM?", "Entry plans on our list run from $7 to $35 per user per month on annual billing, so a 5-person team pays roughly $420 to $2,100 in year one. Plans with sales automation usually cost $35 to $100 per user per month."),
    ("Does a small business need a CRM?", "Once more than one person is following up with leads or customers, a shared CRM stops deals from slipping through spreadsheets and inboxes. Many teams start on a free plan and move to paid when they need automation."),
    ("Is Salesforce good for small businesses?", "Salesforce Starter Suite is priced for small teams, and it suits companies that expect to grow quickly. Most small teams without an admin will find Pipedrive, HubSpot or Zoho faster to set up."),
]


def sb_page():
    order = SB_ORDER
    short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{t}">{TOOL_BY_ID[t]["name"]}</a><br><span class="bf">{SB_FIT[t][0]}</span></span><a class="btn ghost small" href="#{t}">Details</a></li>' for i, t in enumerate(order, 1))
    rows = "".join(f'<tr><td class="num">{i}</td><td><a href="#{t}"><b>{TOOL_BY_ID[t]["name"]}</b></a></td><td>{SB_FIT[t][0].replace("Best ", "").capitalize()}</td><td class="num">From {PRICING[t]["price"]}</td><td>{PRICING[t]["short"]}</td><td class="num">${ENTRY_PRICE[t]*60:,}</td><td class="num"><b>{sb_score(t)}</b>/100</td></tr>' for i, t in enumerate(order, 1))
    cards = []
    for i, t in enumerate(order, 1):
        tool = TOOL_BY_ID[t]
        pros = "".join(f"<li>{p}</li>" for p in tool["pros"])
        cons = "".join(f"<li>{c}</li>" for c in tool["cons"])
        cards.append(f"""<article class="tool" id="{t}">
<div class="tool-head"><span class="num">{i}</span><div><h3>{tool['name']}</h3><div class="bestfor">{SB_FIT[t][0]}</div></div>
<a class="btn small" href="{URLS[t]}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
<div class="spec"><div><span class="label">Starting price</span><b>From {PRICING[t]['price']}</b><span class="small muted">{PRICING[t]['note']}</span></div><div><span class="label">Free trial / plan</span><b>{PRICING[t]['trial']}</b></div><div><span class="label">Small-business score</span><b>{sb_score(t)}/100</b><span class="small muted">Desk research</span></div><div><span class="label">G2 user rating</span><b>{G2[t][0]}/5</b><a class="small" href="{G2[t][2]}" target="_blank" rel="noopener">{G2[t][1]} reviews</a></div></div>
<div class="tool-body">
<p><b>Why it suits small businesses:</b> {SB_FIT[t][1]}</p>
<p>{tool['what']}</p>
<div class="pc"><div class="pros"><h4>Strengths</h4><ul>{pros}</ul></div><div class="cons"><h4>Watch-outs</h4><ul>{cons}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {tool['notavoid']}</p>
</div></article>""")
    wrows = "".join(f'<tr><td>{n}</td><td class="num">{w}%</td><td class="num">{sw}%</td></tr>' for (n, w), sw in zip(CRITERIA, SB_WEIGHTS))
    faq = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in SB_FAQS)
    n = len(order)
    h1 = f"{n} Best CRM Software for Small Businesses in {YEAR}"
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/tools/best-crm-software/">CRM Software</a> / Small business</nav>
<header class="article-head">
<span class="eyebrow">Shortlist · CRM for small business</span>
<h1>{h1}</h1>
<div class="byline"><div class="avatar team-mark">{LOGO}</div><div class="who"><b>By <a href="/team/">Vettlo Editorial Team</a></b><span>Published <time datetime="{SB_DATE}">{SB_DATE_H}</time> · Prices verified {PRICES_CHECKED}</span></div></div>
<p class="disclose">We may earn a commission when you click some links on this page. It never changes which tools we include or how we rank them. See <a href="/how-we-make-money/">how we make money</a>.</p>
</header>
<div class="layout"><div class="main-col">
<section class="prose"><p>A small business needs a CRM its team will actually use, at a price that makes sense for a handful of seats. This guide covers teams of roughly 1 to 20 people. We used the same ratings as our <a href="/tools/best-crm-software/">main CRM ranking</a>, but weighted ease of use and price more heavily, because those matter most when nobody on the team is a full-time CRM admin.</p></section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<section id="compare"><h2>Small-business CRMs compared</h2>
<div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Best for</th><th>Starting price</th><th>Free plan / trial</th><th>5 users, year one*</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">*Entry plan list price × 5 users × 12 months, billed annually, from each vendor's pricing page on {PRICES_CHECKED}. Entry plans differ in features; check each tool below.</p></section>
<section class="prose" id="free"><h2>Best free CRMs for small businesses</h2>
<ul><li><b>HubSpot:</b> free plan for up to 2 users, no credit card required.</li><li><b>Zoho CRM:</b> free edition for up to 3 users.</li><li><b>Attio:</b> free plan for up to 3 seats.</li></ul>
<p>Pipedrive, Freshsales, Close and folk offer free trials of 14 to 21 days instead. Salesforce offers a Free Suite and a free trial.</p></section>
<section id="reviews"><h2>The reviews</h2>{''.join(cards)}</section>
<section id="weights"><h2>How we scored CRMs for small businesses</h2>
<p class="prose">Each tool keeps the same 0 to 5 ratings it has in our <a href="/tools/best-crm-software/">main CRM ranking</a>. For this guide we changed only the weights, then included every tool that scores 70 or higher. Ratings come from desk research: vendor documentation, current pricing pages and G2 reviews. See our <a href="/methodology/">methodology</a>.</p>
<div class="table-wrap"><table><thead><tr><th>Criterion</th><th>Main ranking</th><th>Small business</th></tr></thead><tbody>{wrows}</tbody></table></div></section>
<section class="prose" id="choose"><h2>How to choose a CRM for a small business</h2>
<ol><li><b>Start with who will use it daily.</b> If it's two founders, a free plan may be enough. If it's a sales team, pick the plan that includes the follow-up automation you need.</li>
<li><b>Price the plan you'll need in six months,</b> not the entry plan. Automation, forecasting and custom reports are usually one or two tiers up.</li>
<li><b>Test with real deals.</b> Import 20 live deals during the trial and run your normal week in the tool.</li>
<li><b>Check the exit.</b> Make sure you can export contacts, deals and activity history before you commit.</li></ol></section>
<section id="faq"><h2>Small business CRM FAQ</h2><div>{faq}</div></section>
<section class="prose"><h2>Related</h2><ul><li><a href="/tools/best-crm-software/">Best CRM software for sales teams</a></li><li><a href="/compare/hubspot-vs-pipedrive/">HubSpot vs Pipedrive</a></li><li><a href="/tools/best-pipedrive-alternatives/">Best Pipedrive alternatives</a></li><li><a href="/tools/best-hubspot-alternatives/">Best HubSpot alternatives</a></li></ul></section>
<section class="author-box"><div class="avatar team-mark">{LOGO}</div><div><b>Vettlo Editorial Team</b><p class="small muted">Researched and written by the Vettlo editorial team using our <a href="/methodology/">methodology</a>.</p></div></section>
</div>
<nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#shortlist">Shortlist</a><a href="#compare">Comparison table</a><a href="#free">Free CRMs</a><a href="#reviews">Reviews</a><a href="#weights">How we scored</a><a href="#faq">FAQ</a></nav>
</div></div>
{newsletter()}"""
    url = "/tools/best-crm-for-small-business/"
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": h1, "datePublished": SB_DATE, "dateModified": SB_DATE,
         "author": {"@type": "Organization", "name": "Vettlo Editorial Team", "url": DOMAIN + "/team/"},
         "publisher": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN}, "mainEntityOfPage": DOMAIN + url},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "Best CRM software for small businesses",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": TOOL_BY_ID[t]["name"], "url": f"{DOMAIN}{url}#{t}"} for i, t in enumerate(order, 1)]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in SB_FAQS]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "CRM Software", "item": DOMAIN + "/tools/best-crm-software/"},
            {"@type": "ListItem", "position": 3, "name": "Small business", "item": DOMAIN + url}]},
    ]
    page(url, f"{n} Best CRM Software for Small Businesses ({YEAR}) | Vettlo",
         "The best CRMs for small businesses and small sales teams, scored with extra weight on ease of use and price. Free plans, year-one cost for 5 users and who each CRM suits.",
         body, cur="/best-tools/", jsonld=ld, ptype="article")


sb_page()

# ---------- COMPARE: HUBSPOT VS PIPEDRIVE
CMP_UPDATED = "2026-10-14"
CMP_UPDATED_H = "Oct 14, 2026"
CMP_FAQS = [
    ("Is HubSpot or Pipedrive cheaper?", "At the entry level HubSpot is cheaper: Sales Hub Starter lists at $7 per seat per month billed annually, against $14 for Pipedrive Lite. Once you need email sequences, workflow automation and forecasting, Pipedrive is cheaper: those features are listed on Pipedrive Growth at $39 per seat per month, while HubSpot lists sequences and forecasting on Sales Hub Professional at $90 per seat per month plus a $1,500 one-time onboarding fee."),
    ("Does HubSpot have a free CRM?", "Yes. HubSpot's free plan covers up to 2 users with no credit card required. Pipedrive has no free plan but offers a 14-day free trial on every paid plan."),
    ("Which is easier for sales reps to use?", "Pipedrive is built around a visual deal pipeline and activity reminders, and small teams can usually work in it within a day. HubSpot is also approachable, but its wider feature set and shared marketing data take longer to configure well."),
    ("Should a team that uses HubSpot Marketing Hub pick HubSpot Sales Hub?", "Usually yes. Sales and marketing then share one contact database, lifecycle stages and attribution, so RevOps doesn't have to maintain a sync between two systems."),
    ("Can I switch from Pipedrive to HubSpot later?", "Yes, both tools support CSV import and export and have migration integrations. Plan field mapping, deduplication and activity history before the cutover, because history is the part teams most often lose."),
]

page("/compare/hubspot-vs-pipedrive/", f"HubSpot vs Pipedrive ({YEAR}): Pricing, Features and Which to Choose | Vettlo",
     "HubSpot Sales Hub vs Pipedrive compared on real list prices, plan features and team fit. See what a 10-rep team pays on each, and which CRM to pick.",
     f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/tools/best-crm-software/">CRM Software</a> / HubSpot vs Pipedrive</nav>
<header class="article-head">
<span class="eyebrow">Comparison · CRM software</span>
<h1>HubSpot vs Pipedrive: Which CRM Should Your Sales Team Pick in {YEAR}?</h1>
<div class="byline"><div class="avatar team-mark">{LOGO}</div><div class="who"><b>By <a href="/team/">Vettlo Editorial Team</a></b><span>Prices verified <time datetime="{CMP_UPDATED}">{CMP_UPDATED_H}</time></span></div></div>
<p class="disclose">We may earn a commission when you click some links on this page. It never changes our verdict. See <a href="/how-we-make-money/">how we make money</a>.</p>
</header>
<div class="layout"><div class="main-col">

<section class="verdict" aria-label="Quick verdict">
<span class="label">Quick verdict</span>
<div class="vs">
<div><h3>Pick Pipedrive if…</h3><ul><li>You run a pipeline-first sales team of roughly 3 to 25 reps</li><li>You need email sequences, automation and forecast reports without enterprise pricing</li><li>Nobody on the team has time to be a CRM admin</li></ul></div>
<div><h3>Pick HubSpot if…</h3><ul><li>Your marketing already runs on HubSpot, or will</li><li>You want a free or very cheap CRM for 1 or 2 users</li><li>You need deep custom reporting and can budget for Sales Hub Professional</li></ul></div>
</div>
<p class="small">In our <a href="/tools/best-crm-software/">CRM rankings</a>, HubSpot Sales Hub scores <b>{score("hubspot")}/100</b> and Pipedrive <b>{score("pipedrive")}/100</b>. HubSpot wins on reporting and integrations; Pipedrive wins on rep adoption and value.</p>
</section>

<section class="prose"><h2>The short answer</h2>
<p>The two CRMs split at the point where a team needs sales automation. HubSpot is cheaper to start: its free plan covers 2 users and Sales Hub Starter lists at $7 per seat per month on annual billing. But HubSpot lists email sequences and forecasting on Sales Hub Professional, at $90 per seat per month plus a $1,500 one-time onboarding fee. Pipedrive lists sequences, workflow automation and forecast reports on its Growth plan at $39 per seat per month. For a team that needs those features, Pipedrive costs well under half as much.</p></section>

<section id="cost"><h2>What a 10-rep team pays in year one</h2>
<p class="prose">List prices, billed annually, for 10 seats. Taxes, add-ons and discounts excluded.</p>
<div class="table-wrap"><table><thead><tr><th>Need</th><th>HubSpot plan</th><th>HubSpot year one</th><th>Pipedrive plan</th><th>Pipedrive year one</th></tr></thead><tbody>
<tr><td>Basic pipeline and contacts</td><td>Starter ($7)</td><td class="num">$840</td><td>Lite ($14)</td><td class="num">$1,680</td></tr>
<tr><td>Plus sequences, automation and forecasting</td><td>Professional ($90 + $1,500 onboarding)</td><td class="num">$12,300</td><td>Growth ($39)</td><td class="num">$4,680</td></tr>
<tr><td>Plus custom reports</td><td>Professional ($90 + $1,500 onboarding)</td><td class="num">$12,300</td><td>Premium ($59)</td><td class="num">$7,080</td></tr>
</tbody></table></div>
<p class="small muted">Prices from <a href="https://www.hubspot.com/pricing/sales" target="_blank" rel="noopener">HubSpot</a> and <a href="https://www.pipedrive.com/en/pricing" target="_blank" rel="noopener">Pipedrive</a> pricing pages, checked {CMP_UPDATED_H}. Vendors change plans often; confirm before you buy.</p></section>

<section id="features"><h2>Plan features side by side</h2>
<div class="table-wrap"><table><thead><tr><th>Feature</th><th>HubSpot Sales Hub</th><th>Pipedrive</th></tr></thead><tbody>
<tr><td>Free option</td><td>Free plan for up to 2 users</td><td>No free plan; 14-day free trial</td></tr>
<tr><td>Entry paid plan</td><td>Starter, $7/seat/mo (annual), $20 monthly</td><td>Lite, $14/seat/mo (annual)</td></tr>
<tr><td>Email sequences</td><td>Listed from Professional</td><td>Listed from Growth</td></tr>
<tr><td>Workflow automation</td><td>Starter: up to 50 workflows with restricted triggers; Professional: up to 300</td><td>Listed from Growth</td></tr>
<tr><td>Forecasting</td><td>Listed from Professional</td><td>Forecast reports from Growth</td></tr>
<tr><td>Custom reports</td><td>Professional: up to 100 custom reports</td><td>Listed from Premium</td></tr>
<tr><td>Lead routing</td><td>Not compared here</td><td>Listed from Premium</td></tr>
<tr><td>Calling minutes</td><td>Starter 500, Professional 3,000</td><td>Not listed on pricing page</td></tr>
<tr><td>Onboarding fee</td><td>$1,500 (Professional), $3,500 (Enterprise)</td><td>None listed</td></tr>
<tr><td>G2 user rating</td><td class="num">{G2["hubspot"][0]}/5 ({G2["hubspot"][1]} reviews)</td><td class="num">{G2["pipedrive"][0]}/5 ({G2["pipedrive"][1]} reviews)</td></tr>
<tr><td>Vettlo score</td><td class="num">{score("hubspot")}/100</td><td class="num">{score("pipedrive")}/100</td></tr>
</tbody></table></div>
<p class="small muted">"Listed from" means the feature first appears on that plan on the vendor's public pricing page. Feature availability by plan from vendor pricing pages, {CMP_UPDATED_H}.</p></section>

<section class="prose"><h2>Where HubSpot is stronger</h2>
<ul>
<li><b>One database with marketing.</b> If marketing uses HubSpot, leads, lifecycle stages and attribution flow into sales records without a sync to maintain.</li>
<li><b>A real free tier.</b> Two users can run a pipeline at no cost, which is useful for founders before the first sales hire.</li>
<li><b>Reporting depth at Professional.</b> Custom reports and forecasting at Professional go further than Pipedrive's equivalents.</li>
<li><b>Ecosystem.</b> A large integration marketplace and partner network.</li>
</ul>
<h2>Where Pipedrive is stronger</h2>
<ul>
<li><b>Price of automation.</b> Sequences, automation and forecast reports arrive on a $39 plan instead of a $90 plan with an onboarding fee.</li>
<li><b>Rep adoption.</b> The visual pipeline and activity prompts keep reps focused on the next step on every deal, with little setup.</li>
<li><b>No admin required.</b> Small teams can run it without a dedicated RevOps person.</li>
</ul>
<h2>How to decide in one afternoon</h2>
<ol>
<li>List the three workflows your team can't live without, for example "follow-up sequence after a demo" or "weekly forecast call".</li>
<li>Check which plan on each side includes all three. That's your real price, not the entry price.</li>
<li>Multiply by your seat count for 12 months, and add HubSpot's onboarding fee if you land on Professional.</li>
<li>Start both trials with a slice of your real pipeline and have two reps use each for a week.</li>
</ol></section>

<section id="faq"><h2>HubSpot vs Pipedrive FAQ</h2><div>{"".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in CMP_FAQS)}</div></section>

<section class="prose"><h2>Other options</h2><p>If neither fits, see our full <a href="/tools/best-crm-software/">ranking of {len(TOOLS)} CRMs for sales teams</a>, including Salesforce for complex enterprise processes and Zoho CRM for budget-conscious teams that want depth. Or see our guides to the <a href="/tools/best-pipedrive-alternatives/">best Pipedrive alternatives</a> and <a href="/tools/best-hubspot-alternatives/">best HubSpot alternatives</a>.</p></section>

<section class="author-box"><div class="avatar team-mark">{LOGO}</div><div><b>Vettlo Editorial Team</b><p class="small muted">Researched and written by the Vettlo editorial team using our <a href="/methodology/">methodology</a>. Prices and plan features come from each vendor's public pricing page.</p></div></section>
</div>
<nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#cost">Year-one cost</a><a href="#features">Features</a><a href="#faq">FAQ</a></nav>
</div></div>
{newsletter()}""", cur="/best-tools/", ptype="article", jsonld=[
        {"@context": "https://schema.org", "@type": "Article", "headline": f"HubSpot vs Pipedrive: Which CRM Should Your Sales Team Pick in {YEAR}?",
         "datePublished": CMP_UPDATED, "dateModified": CMP_UPDATED,
         "author": {"@type": "Organization", "name": "Vettlo Editorial Team", "url": DOMAIN + "/team/"},
         "publisher": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN},
         "mainEntityOfPage": DOMAIN + "/compare/hubspot-vs-pipedrive/"},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in CMP_FAQS]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "CRM Software", "item": DOMAIN + "/tools/best-crm-software/"},
            {"@type": "ListItem", "position": 3, "name": "HubSpot vs Pipedrive", "item": DOMAIN + "/compare/hubspot-vs-pipedrive/"}]},
    ])

# ---------- CATEGORY MODULES
exec(open(ROOT / "catlib.py").read())
for _f in sorted((ROOT / "categories").glob("*.py")):
    exec(open(_f).read())

# ---------- METHODOLOGY
page("/methodology/", "Our Software Review Methodology | Vettlo",
     "How Vettlo selects, tests and scores sales and revenue software, and how we keep rankings independent of advertising.",
     f"""<div class="wrap"><div class="page-head"><span class="eyebrow">How we vet</span><h1>Our review methodology</h1>
<p>Choosing revenue software is expensive to get wrong. Here is exactly how we build a shortlist, so you can judge it yourself.</p>
<p class="small mono">Last updated {UPDATED_H}</p></div>
<div class="page-body prose">
<h2>1. Build the long list</h2>
<p>For each category we start from every product a sales or RevOps team could reasonably buy: vendor directories, review platforms (G2, Capterra, TrustRadius), practitioner communities and reader suggestions. A tool does not need any relationship with us to be considered.</p>
<h2>2. Set criteria for the category</h2>
<p>We write criteria specific to the job the software does. A dialer is judged on connect rates and compliance controls; a CRM on pipeline management and forecasting. Each criterion gets a published weight, shown on the review.</p>
<h2>3. Test hands-on</h2>
<p>Reviewers sign up for trials or demo accounts and run the workflows a real team would: importing a pipeline, building a sequence, routing a lead, producing a forecast. We take our own screenshots and note setup time, limits and anything that surprised us.</p>
<div class="callout">Where hands-on testing for a category is still in progress, the review says so and its scores are labeled <b>Desk research</b>: they're based on vendor documentation, current pricing pages and verified user reviews. We replace them with hands-on scores once testing is complete.</div>
<h2>4. Check against real users</h2>
<p>We compare our findings with patterns in verified user reviews and with practitioners in our network, looking for consistent strengths and complaints across company sizes.</p>
<h2>5. Score and rank</h2>
<p>Each tool gets a 0 to 5 rating per criterion. Weighted totals become a score out of 100. Tools below 70 are not included in the ranked list; we list them under <b>Also considered</b> with their score. Position follows score, adjusted only by editorial judgment we explain in the review.</p>
<h2>6. Re-check every 90 days</h2>
<p>We re-verify pricing, plans and major features at least every 90 days and show the date on each review. Corrections are logged at the bottom of the page.</p>
<h2>What vendors can and cannot do</h2>
<ul><li>Vendors <b>can</b> correct factual errors, provide demo access and suggest their product for review.</li>
<li>Vendors <b>cannot</b> pay for inclusion, position, score or wording in an editorial review.</li>
<li>Paid placements appear only in labeled <b>Sponsored</b> slots, outside the ranked list. See <a href="/how-we-make-money/">how we make money</a>.</li></ul>
<h2>Who reviews</h2>
<p>Reviews are published under the <a href="/team/">Vettlo Editorial Team</a> byline. When a named reviewer completes hands-on testing for a category, their name and a profile describing their experience are added to that review.</p>
<h2>Change log</h2>
<p class="small mono">{UPDATED_H}: First version published.</p>
</div></div>""", cur="/methodology/")

# ---------- MONEY
page("/how-we-make-money/", "How We Make Money (Affiliate Disclosure) | Vettlo",
     "Vettlo's affiliate and advertising disclosure: where commissions and sponsorships appear, and why they never affect rankings.",
     f"""<div class="wrap"><div class="page-head"><span class="eyebrow">Disclosure</span><h1>How we make money</h1>
<p>Vettlo is free to read. Here is every way we earn revenue, and the walls we keep between that revenue and our rankings.</p>
<p class="small mono">Last updated {UPDATED_H}</p></div>
<div class="page-body prose">
<h2>Affiliate links</h2>
<p>Some links to software vendors are affiliate links. If you click one and later buy, we may earn a commission. The disclosure line at the top of each review tells you when a page contains them. Links are marked <code>rel="sponsored"</code>.</p>
<h2>Featured (sponsored) slots</h2>
<p>Vendors can pay for a <b>Featured</b> slot on a category page or in our newsletter. Every featured slot is labeled <b>Sponsored · Not part of our ranking</b>, styled differently from editorial content, and sits outside the ranked list.</p>
<h2>Pay-per-click listings</h2>
<p>On some pages vendors may pay per click on a "Visit website" button. Paying for clicks does not change inclusion, order, score or what we write. Tools without any commercial relationship appear in our lists, and paying vendors are left out when they don't score high enough.</p>
<h2>Sponsored content</h2>
<p>Occasionally we publish content paid for by a vendor, such as a webinar recap or a partner guide. It is labeled <b>Sponsored</b> at the top and is never presented as a review.</p>
<h2>What money never buys</h2>
<div class="callout">Inclusion in a shortlist, a ranking position, a score, the wording of a review, or the removal of criticism.</div>
<h2>How reviewers are paid</h2>
<p>Writers and reviewers are paid for their time and expertise. Their pay is never tied to clicks, conversions or which tools they recommend.</p>
<p>Questions about a specific relationship? <a href="/contact/">Contact us</a> and we'll answer.</p>
</div></div>""")

# ---------- EDITORIAL STANDARDS
page("/editorial-standards/", "Editorial Standards | Vettlo",
     "The standards Vettlo writers and editors follow: independence, accuracy, corrections and use of AI.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Standards</span><h1>Editorial standards</h1>
<p>The rules every Vettlo writer and editor follows.</p></div>
<div class="page-body prose">
<h2>Independence</h2><p>Editorial decisions are made by the editorial team. People who sell advertising do not assign, edit or approve reviews.</p>
<h2>Accuracy</h2><p>Prices, plan limits and feature claims are checked against the vendor's current public pages or our own test account. Every review shows its last verified date.</p>
<h2>Experience</h2><p>We assign reviews to people who have used tools in the category in a real job. Author pages list that experience.</p>
<h2>Use of AI</h2><p>We may use AI tools to help with research summaries, transcription and copy editing. Testing, scoring, conclusions and final wording are done and approved by a named human editor.</p>
<h2>Corrections</h2><p>When we get something wrong, we fix it and note the change in the review's change log. Report an error through our <a href="/contact/">contact page</a>.</p>
<h2>Editorial team</h2><p>Reviews are published by the <a href="/team/">Vettlo Editorial Team</a>. Questions about a review go through our <a href="/contact/">contact page</a>.</p>
</div></div>""")

# ---------- ABOUT (facts)
page("/about/", "About Vettlo",
     "Vettlo is an independent publication that reviews sales and revenue operations software for the leaders who buy it.",
     f"""<div class="wrap"><div class="page-head"><span class="eyebrow">About</span><h1>About Vettlo</h1>
<p>Vettlo reviews the software revenue teams run on, for the sales and RevOps leaders who choose it.</p></div>
<div class="page-body prose">
<p>Sales leaders make five- and six-figure software decisions based on vendor demos and listicles that rank whoever pays most. We started Vettlo to give them a shortlist built the way they'd build one themselves: trial the tool, test the hard workflows, and write down who it's actually for.</p>
<h2>Vettlo at a glance</h2>
<dl class="dl">
<dt>What</dt><dd>Independent reviews and comparisons of sales and revenue operations software</dd>
<dt>Audience</dt><dd>CROs, VPs of Sales, sales managers and RevOps leaders</dd>
<dt>Founded</dt><dd>{YEAR}</dd>
<dt>Coverage</dt><dd>CRM, sales engagement, conversation intelligence, forecasting, CPQ, commissions, data providers and more</dd>
<dt>Revenue</dt><dd>Affiliate commissions, labeled sponsored slots and newsletter sponsorships. <a href="/how-we-make-money/">Details</a></dd>
<dt>Rankings</dt><dd>Editorial only, based on published weighted criteria. Never sold.</dd>
<dt>Contact</dt><dd><a href="/contact/">Contact form</a></dd>
</dl>
<h2>Our team</h2><p>Reviews are researched and written by the <a href="/team/">Vettlo Editorial Team</a>.</p>
</div></div>""", cur="/about/", jsonld=[ORG])

# ---------- ADVERTISE
page("/advertise/", "Advertise with Vettlo",
     "Reach sales and RevOps leaders while they evaluate software. Featured slots, pay-per-click listings and newsletter sponsorships, always clearly labeled.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">For vendors</span><h1>Reach revenue leaders while they're choosing software</h1>
<p>Our readers arrive with a buying question. Put your product in front of them, with placements that are labeled and that buyers still trust.</p></div>
<div class="page-body" style="display:grid;gap:2.5rem">
<div class="cards3">
<div class="card"><span class="label">Demand capture</span><h3>Pay-per-click listings</h3><p class="muted small">Pay only when a reader clicks through to your site from a category page. Bids never change editorial order.</p><span class="price">CPC · pricing on request</span></div>
<div class="card"><span class="label">Visibility</span><h3>Featured category slot</h3><p class="muted small">A labeled Sponsored placement on a category shortlist page, outside the ranked list.</p><span class="price">Monthly · pricing on request</span></div>
<div class="card"><span class="label">Awareness</span><h3>Newsletter sponsorship</h3><p class="muted small">One sponsor per issue of The Vettlo Briefing, sent weekly to revenue leaders.</p><span class="price">Per issue · pricing on request</span></div>
<div class="card"><span class="label">Thought leadership</span><h3>Sponsored guides &amp; events</h3><p class="muted small">Co-produced webinars and guides, labeled Sponsored and kept separate from reviews.</p><span class="price">Custom</span></div>
</div>
<div class="prose"><h2>The one thing we don't sell</h2><p>Ranking positions, scores and review wording are editorial only. That's what makes a placement next to them worth paying for. Read the full <a href="/how-we-make-money/">disclosure</a>.</p></div>
<div class="prose"><h2>Audience</h2><p>Vettlo is written for CROs, VPs of Sales, sales managers and RevOps leaders. We'll publish audited traffic and newsletter numbers after our first full quarter. Until then, <a href="/contact/">ask us</a> for current figures.</p></div>
<div><h2 style="margin-bottom:1rem">Talk to us</h2>
<form class="form" id="adv-form"><label for="a-name">Name<input id="a-name" required autocomplete="name"></label>
<label for="a-email">Work email<input id="a-email" type="email" required autocomplete="email"></label>
<label for="a-company">Company website<input id="a-company" required placeholder="https://"></label>
<label for="a-int">Interested in<select id="a-int"><option>Pay-per-click listings</option><option>Featured category slot</option><option>Newsletter sponsorship</option><option>Sponsored guides &amp; events</option></select></label>
<button class="btn" type="submit">Send inquiry</button><p class="form-msg" id="adv-msg" aria-live="polite"></p></form>
<script>document.getElementById('adv-form').addEventListener('submit',function(e){e.preventDefault();document.getElementById('adv-msg').textContent='Form is a preview. Connect it to your inbox or a form service before launch.';});</script>
</div></div></div>""")

# ---------- TEAM
page("/team/", "Vettlo Editorial Team",
     "Who writes Vettlo's software reviews and how the editorial team works.",
     f"""<div class="wrap"><div class="page-head" style="grid-template-columns:auto minmax(0,1fr);align-items:center;gap:1.25rem"><div class="avatar team-mark" style="width:88px;height:88px">{LOGO}</div>
<div style="display:grid;gap:.4rem"><span class="eyebrow">Editorial team</span><h1>Vettlo Editorial Team</h1><p class="small muted">Software reviews for sales and RevOps leaders</p></div></div>
<div class="page-body prose">
<p>The Vettlo Editorial Team researches, scores and writes every review on this site. We cover the software revenue teams depend on: CRM, sales engagement, conversation intelligence, forecasting, CPQ, commissions and B2B data.</p>
<h2>How we work</h2>
<ul><li>Every review follows our published <a href="/methodology/">methodology</a>, with category-specific criteria and weights shown on the page.</li>
<li>Prices, plans and ratings are re-checked at least every 90 days, and each review shows its last verified date.</li>
<li>Scores labeled <b>Desk research</b> are based on vendor documentation, pricing pages and verified user reviews. They're replaced with hands-on scores once testing is complete.</li>
<li>Advertising and affiliate relationships never affect inclusion, order or scores. See <a href="/how-we-make-money/">how we make money</a>.</li></ul>
<h2>Published reviews</h2>
<ul><li><a href="/tools/best-crm-software/">Best CRM Software for Sales Teams</a></li><li><a href="/compare/hubspot-vs-pipedrive/">HubSpot vs Pipedrive</a></li><li><a href="/tools/best-pipedrive-alternatives/">Best Pipedrive Alternatives</a></li><li><a href="/tools/best-hubspot-alternatives/">Best HubSpot Alternatives</a></li><li><a href="/tools/best-crm-for-small-business/">Best CRM for Small Businesses</a></li></ul>
<h2>Join us</h2>
<p>We're looking for practitioners who have run sales teams or owned a CRM to test tools and write reviews. See <a href="/write-for-us/">write for us</a>.</p>
</div></div>""", jsonld=[{"@context": "https://schema.org", "@type": "Organization", "name": "Vettlo Editorial Team", "parentOrganization": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN}}])

# ---------- WRITE FOR US
page("/write-for-us/", "Write for Vettlo",
     "Pitch Vettlo if you've run sales teams or revenue operations and want to write about the tools and practices that work.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Contributors</span><h1>Write for Vettlo</h1>
<p>We publish practitioners: people who have carried a number, run a sales floor or owned a CRM.</p></div>
<div class="page-body prose">
<h2>What we're looking for</h2><ul><li>Hands-on tool reviews in a category you've worked in</li><li>Playbooks from real rollouts, migrations and stack consolidations</li><li>Opinionated takes on how revenue teams should work</li></ul>
<h2>What we don't accept</h2><ul><li>Pieces written on behalf of a vendor, or with links a vendor paid for</li><li>Generic or AI-generated drafts without first-hand experience</li></ul>
<h2>How to pitch</h2><p>Send a short pitch, your LinkedIn profile and two writing samples through our <a href="/contact/">contact page</a>.</p>
</div></div>""")

# ---------- CONTACT
page("/contact/", "Contact Vettlo",
     "Contact Vettlo to suggest a tool, report an error, pitch a story or ask about advertising.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Contact</span><h1>Get in touch</h1>
<p>Suggest a tool for review, report an error, pitch a story or ask about advertising.</p></div>
<div class="page-body"><form class="form" id="c-form">
<label for="c-name">Name<input id="c-name" required autocomplete="name"></label>
<label for="c-email">Email<input id="c-email" type="email" required autocomplete="email"></label>
<label for="c-topic">Topic<select id="c-topic"><option>Suggest a tool</option><option>Report an error</option><option>Pitch a story</option><option>Advertising</option><option>Something else</option></select></label>
<label for="c-msg">Message<textarea id="c-msg" rows="5" required></textarea></label>
<button class="btn" type="submit">Send message</button><p class="form-msg" id="c-out" aria-live="polite"></p></form>
<script>document.getElementById('c-form').addEventListener('submit',function(e){e.preventDefault();document.getElementById('c-out').textContent='Form is a preview. Connect it to your inbox or a form service before launch.';});</script>
</div></div>""")

# ---------- PRIVACY / TERMS
page("/privacy/", "Privacy Policy | Vettlo", "How Vettlo handles information when you visit the site.",
     f"""<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Privacy Policy</h1><p class="small mono">Last updated {UPDATED_H}</p></div>
<div class="page-body prose">
<p>This policy explains what information Vettlo handles when you visit vettlo.com.</p>
<h2>What we collect</h2>
<p>Vettlo does not use advertising trackers or analytics cookies. Our hosting provider, Cloudflare, processes standard technical data such as IP addresses and browser details to deliver and protect the site. See <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">Cloudflare's privacy policy</a>.</p>
<h2>Forms and newsletter</h2>
<p>Our newsletter and contact forms do not yet send or store any information. When they go live, we'll update this policy to say which provider handles your details and how to unsubscribe or request deletion.</p>
<h2>Links to other sites</h2>
<p>Reviews link to software vendors and review platforms. Some links are affiliate links. Those sites have their own privacy policies.</p>
<h2>Your rights</h2>
<p>You can ask what information we hold about you, or ask us to delete it, through our <a href="/contact/">contact page</a>.</p>
<h2>Changes</h2>
<p>We'll post any changes on this page and update the date above.</p>
</div></div>""")

page("/terms/", "Terms of Use | Vettlo", "Terms for using vettlo.com.",
     f"""<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Terms of Use</h1><p class="small mono">Last updated {UPDATED_H}</p></div>
<div class="page-body prose">
<p>By using vettlo.com you agree to these terms.</p>
<h2>Information, not advice</h2>
<p>Our reviews, scores and prices are provided for general information. Vendors change prices and features often, so confirm details with the vendor before you buy. Nothing on this site is professional, legal or financial advice.</p>
<h2>Accuracy</h2>
<p>We work to keep content accurate and show the date each review was last verified. If you spot an error, please <a href="/contact/">tell us</a> and we'll correct it.</p>
<h2>Affiliate links and sponsorships</h2>
<p>Some links earn us a commission, and some placements are sponsored and labeled as such. See <a href="/how-we-make-money/">how we make money</a>.</p>
<h2>Content</h2>
<p>Text and design on this site belong to Vettlo. You may quote short passages with a link back to the source page. Product names and trademarks belong to their owners.</p>
<h2>Liability</h2>
<p>The site is provided as is. Vettlo is not liable for decisions made based on its content or for content on third-party sites we link to.</p>
<h2>Changes</h2>
<p>We may update these terms and will post changes on this page.</p>
</div></div>""")

# ---------- 404
page("/404/", "Page Not Found | Vettlo", "This page doesn't exist.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">404</span><h1>This page didn't pass inspection</h1>
<p>It may have moved. Try the <a href="/best-tools/">tools index</a> or the <a href="/">home page</a>.</p></div></div>""")


# ------------------------------------------------------------------ render
def head_block(path, p, css_href):
    canon = DOMAIN + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in p["jsonld"])
    robots = '<meta name="robots" content="noindex, nofollow">' if (path == "/404/" or PRELAUNCH_NOINDEX) else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return (f'<title>{p["title"]}</title><meta name="description" content="{p["desc"]}">{robots}'
            f'<link rel="canonical" href="{canon}"><meta property="og:type" content="{p["ptype"]}"><meta property="og:site_name" content="Vettlo">'
            f'<meta property="og:title" content="{p["title"]}"><meta property="og:description" content="{p["desc"]}"><meta property="og:url" content="{canon}">'
            f'<meta property="og:image" content="{DOMAIN}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{DOMAIN}/assets/og.png"><link rel="icon" href="/assets/logo.svg" type="image/svg+xml">'
            f'{FONTS}<link rel="stylesheet" href="{css_href}">{ld}')


def body_block(p, path):
    return f'{header(p["cur"])}<main id="main">{p["body"]}</main>{FOOTER}{NL_SCRIPT}'


def out_file(path):
    return "index.html" if path == "/" else (path.strip("/") + "/index.html" if path != "/404/" else "404.html")


def relativize(html, path, out_rel):
    depth = out_rel.count("/")
    up = "../" * depth

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith("//") or not url.startswith("/"):
            return m.group(0)
        u, frag = (url.split("#", 1) + [""])[:2]
        frag = ("#" + frag) if frag else ""
        if u == "/":
            target = "index.html"
        elif u.endswith("/"):
            target = u.strip("/") + "/index.html"
        else:
            target = u.lstrip("/")
        if u == "/404/":
            target = "404.html"
        return f'{attr}="{up}{target}{frag}"'
    return re.sub(r'(href|src)="(/[^"]*)"', fix, html)


def build():
    if CATEGORY_PAGES:
        cards = "".join(f'<a class="card" href="{u}"><span class="label">{k}</span><h3>{t}</h3><p class="muted small">{b}</p></a>' for u, t, b, k in CATEGORY_PAGES)
        PAGES["/best-tools/"]["body"] = PAGES["/best-tools/"]["body"].replace("<!--CATGUIDES-->", f'<h2 style="margin:2.5rem 0 1rem">Prospecting and outreach guides</h2><div class="cards3">{cards}</div>')
    if DIST.exists():
        shutil.rmtree(DIST)
    site, prev = DIST / "site", DIST / "preview"
    for d in (site, prev):
        (d / "assets").mkdir(parents=True)
        shutil.copy(ROOT / "src" / "site.css", d / "assets" / "site.css")
        shutil.copy(ROOT / "src" / "og.png", d / "assets" / "og.png")
        (d / "assets" / "logo.svg").write_text(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"').replace("var(--brand-ink)", "#ffffff").replace("var(--brand)", "#2347d6"))
    for path, p in PAGES.items():
        rel = out_file(path)
        # deploy version
        doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
               f'{head_block(path, p, "/assets/site.css")}</head><body>{body_block(p, path)}</body></html>')
        f = site / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc)
        # preview version
        if path == "/":
            pdoc = f'<title>Vettlo Site Preview</title>{FONTS}<link rel="stylesheet" href="assets/site.css">{body_block(p, path)}'
        else:
            pdoc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
                    f'<title>{p["title"]}</title>{FONTS}<link rel="stylesheet" href="/assets/site.css"></head><body>{body_block(p, path)}</body></html>')
        pdoc = relativize(pdoc, path, rel)
        g = prev / rel
        g.parent.mkdir(parents=True, exist_ok=True)
        g.write_text(pdoc)

    lastmod = {"/compare/hubspot-vs-pipedrive/": "2026-10-14", "/tools/best-pipedrive-alternatives/": "2026-10-14", "/tools/best-hubspot-alternatives/": "2026-10-14", "/tools/best-crm-for-small-business/": "2026-10-14", "/team/": "2026-10-14", "/privacy/": "2026-10-14", "/terms/": "2026-10-14", "/": "2026-10-14"}
    for u, *_ in CATEGORY_PAGES:
        lastmod.setdefault(u, "2026-10-14")
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{lastmod.get(p, UPDATED)}</lastmod></url>" for p in PAGES if p != "/404/")
    (site / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (site / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    (site / "llms.txt").write_text(f"""# Vettlo

> Vettlo is an independent publication that reviews sales and revenue operations software (CRM, sales engagement, conversation intelligence, forecasting, CPQ, commissions, B2B data) for CROs, sales leaders and RevOps teams.

Rankings are editorial only and based on published, weighted criteria per category. Vendors cannot pay for inclusion, position or scores. Sponsored placements are labeled and kept outside ranked lists. Reviews are re-verified every 90 days.

## Reviews
- [Best CRM Software for Sales Teams]({DOMAIN}/tools/best-crm-software/): shortlist of {len(TOOLS)} CRMs scored on pipeline management, automation, reporting, integrations, usability and value
- [HubSpot vs Pipedrive]({DOMAIN}/compare/hubspot-vs-pipedrive/): list prices, plan features and year-one cost for a 10-rep team
- [Best Pipedrive alternatives]({DOMAIN}/tools/best-pipedrive-alternatives/): 6 CRMs for teams leaving Pipedrive, with what you gain and give up
- [Best HubSpot alternatives]({DOMAIN}/tools/best-hubspot-alternatives/): 6 CRMs for teams leaving HubSpot Sales Hub
- [Best CRM for small businesses]({DOMAIN}/tools/best-crm-for-small-business/): CRMs for teams of 1 to 20, weighted toward ease of use and price, with free-plan details
{"".join(f"- [{t}]({DOMAIN}{u}): {b}" + chr(10) for u, t, b, k in CATEGORY_PAGES)}- [All categories]({DOMAIN}/best-tools/)

## Trust
- [Review methodology]({DOMAIN}/methodology/)
- [How we make money]({DOMAIN}/how-we-make-money/)
- [Editorial standards]({DOMAIN}/editorial-standards/)
- [About Vettlo]({DOMAIN}/about/)
- [Editorial team]({DOMAIN}/team/)
""")
    (site / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY)
    (site / "_redirects").write_text("/author/editor/ /team/ 301\n/author/editor /team/ 301\n")
    (site / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n" + ("  X-Robots-Tag: noindex, nofollow\n" if PRELAUNCH_NOINDEX else ""))
    pub = ROOT / "public"
    if pub.exists():
        shutil.rmtree(pub)
    shutil.copytree(site, pub)
    print("pages:", len(PAGES))


if __name__ == "__main__":
    build()
