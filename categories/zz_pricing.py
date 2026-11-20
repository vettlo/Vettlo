# Public vendor pricing / product page. Each position is a product card with its monthly and yearly price and a buy
# button that opens the vendor portal with that position preselected. Payment providers' site reviews need a page like
# this (products, prices, a way to buy). Not indexed.
# Prices must match DEFAULT_MONTHLY / YEAR_DISCOUNT / BASIC_YEAR in src/portal.js.

_MONTHLY = [150, 99, 79, 59, 49, 39, 29, 19, 12, 10]
_YEAR_OFF = 0.10
_BASIC_YEAR = 50


def _usd(x):
    return f"${x:,.2f}".replace(".00", "")


def _year(m):
    return round(m * 12 * (1 - _YEAR_OFF), 2)


_WHERE = {1: "The first product on the list", 2: "Second on the list", 3: "Third on the list"}


def _card(n, m):
    y = _year(m)
    note = _WHERE.get(n, f"Position #{n} on the list")
    return f"""<article class="pcard{' pcard-top' if n == 1 else ''}" id="p{n}">
<div class="pcard-head"><span class="pcard-n">#{n}</span><div><h3>Position #{n}</h3><p class="small muted">{note}</p></div></div>
<ul class="pcard-feat"><li>Your product at #{n} on one shortlist or alternatives page</li><li>Same spot in the review cards and comparison table</li><li>Impressions and visits in your vendor portal</li></ul>
<div class="pcard-prices"><div><b>{_usd(m)}</b><small>per month</small></div><div><b>{_usd(y)}</b><small>per year, 10% off</small></div></div>
<div class="pcard-buy"><a class="btn small" href="/vendors/login/?new=1&amp;plan=p{n}&amp;period=month">Buy monthly</a><a class="btn ghost small" href="/vendors/login/?new=1&amp;plan=p{n}&amp;period=year">Buy yearly</a></div>
</article>"""


_cards = "".join(_card(i + 1, m) for i, m in enumerate(_MONTHLY))
_cards += f"""<article class="pcard" id="basic">
<div class="pcard-head"><span class="pcard-n">B</span><div><h3>Basic listing</h3><p class="small muted">First under “Other tools to consider”</p></div></div>
<ul class="pcard-feat"><li>Your product listed first under “Other tools to consider” on one category shortlist</li><li>Link to your site</li><li>Impressions and visits in your vendor portal</li></ul>
<div class="pcard-prices"><div><b>{_usd(_BASIC_YEAR)}</b><small>per year</small></div></div>
<div class="pcard-buy"><a class="btn small" href="/vendors/login/?new=1&amp;plan=basic&amp;period=year">Buy yearly</a></div>
</article>"""

page("/vendors/pricing/", "Vendor Pricing: Positions #1 to #10 | Vettlo",
     "Buy a position on a Vettlo software list: #1 to #10 on a category shortlist or alternatives page, monthly or yearly with 10% off, plus a $50 Basic listing.",
     f"""<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Positions and prices</h1>
<p class="lede">Buy a position, from #1 to #10, on a Vettlo category shortlist or alternatives page. Each position on a page goes to one vendor. Pay monthly, or yearly and save 10%. All prices in US dollars, per page.</p>
<div class="ctas"><a class="btn" href="#positions">See positions</a><a class="btn ghost" href="/vendors/login/">Sign in</a></div></div>
</div></section>
<div class="wrap about">
<section id="positions"><div class="pcards">{_cards}</div></section>
<section class="split"><div><span class="kicker">How buying works</span><h2>From order to live</h2></div>
<div class="prose"><ol>
<li><strong>Choose a position above.</strong> Create a free vendor account with your work email; we send you a sign-in link.</li>
<li><strong>Pick the page.</strong> In the portal, choose the category shortlist or alternatives page you want; the position you chose is highlighted if it's free there.</li>
<li><strong>Add your product and confirm.</strong> Enter your product's name and website and accept the <a href="/advertiser-terms/">advertiser terms</a>. You can pay by card or bank transfer.</li>
<li><strong>We review your product.</strong> It shows as "In editorial review" until we've written its review. Your paid time starts the day it goes live.</li>
</ol></div></section>
<section class="split"><div><span class="kicker">Cancelling</span><h2>Refunds and renewals</h2></div>
<div class="prose"><p>Plans renew every month or year until you cancel; a cancelled plan stays live until the end of the period you paid for. Every payment can be refunded in full within 14 days, no questions asked. See the <a href="/refunds/">refund policy</a> and <a href="/advertiser-terms/">advertiser terms</a>.</p>
<p>A position changes where your product appears on a page. It doesn't change its score or our review. Questions: <a href="mailto:vendors@vettlo.com">vendors@vettlo.com</a>.</p></div></section>
</div>""")
NOINDEX.add("/vendors/pricing/")

FOOTER = FOOTER.replace('<li><a href="/vendors/">For vendors</a></li>',
                        '<li><a href="/vendors/">For vendors</a></li><li><a href="/vendors/pricing/">Vendor pricing</a></li>')

page("/refunds/", "Refund Policy: 14-Day Refunds on Vendor Plans | Vettlo",
     "Vettlo's refund policy for vendor plans: a full refund of any payment within 14 days, no questions asked, plus how to ask for one and how cancelling works.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Refund policy</h1>
<p>How refunds and cancellations work for positions and listings bought on Vettlo.</p>
<p class="small mono">Last updated Nov 20, 2026</p></div>
<div class="page-body prose">
<h2>14-day refunds</h2>
<p>You can get a full refund of any payment, whether it's your first payment or a renewal, if you ask within 14 days of that payment. No questions asked.</p>
<h2>How to ask for a refund</h2>
<p>Email <a href="mailto:vendors@vettlo.com">vendors@vettlo.com</a> or use our <a href="/contact/">contact page</a> with the email address you used to pay. We refund to the payment method you used. Banks usually take 5 to 10 business days to show it.</p>
<h2>Products we don't accept</h2>
<p>If we decline your product after you've paid, or you cancel before your product goes live, we refund the full payment, whenever that happens.</p>
<h2>Cancelling a plan</h2>
<p>Plans renew automatically every month or year until you cancel in the vendor portal. A cancelled plan doesn't renew and stays live until the end of the period you paid for. After the 14-day window, the current period isn't refunded.</p>
<p>If we end your plan early for a reason other than a breach of our <a href="/advertiser-terms/">advertiser terms</a>, we refund the unused part of the period.</p>
</div></div>""")
