# Public vendor pricing page (temporary: shown to payment providers during their review).
# Not indexed. To remove: delete this file and add "/vendors/pricing/ /vendors/ 301" to _redirects in build.py.
# Prices must match DEFAULT_MONTHLY / YEAR_DISCOUNT / BASIC_YEAR in src/portal.js.

_MONTHLY = [150, 99, 79, 59, 49, 39, 29, 19, 12, 10]
_YEAR_OFF = 0.10
_BASIC_YEAR = 50


def _usd(x):
    return f"${x:,.2f}".replace(".00", "")


_rows = "".join(
    f"<tr><th>#{i + 1} position</th><td>{_usd(m)}</td><td>{_usd(round(m * 12 * (1 - _YEAR_OFF), 2))}</td></tr>"
    for i, m in enumerate(_MONTHLY))
_rows += f"<tr><th>Basic listing</th><td>–</td><td>{_usd(_BASIC_YEAR)}</td></tr>"

page("/vendors/pricing/", "Vendor Pricing: Positions #1 to #10 | Vettlo",
     "Prices for Vettlo vendor positions: #1 to #10 on a category shortlist or alternatives page, billed monthly or yearly with 10% off, plus a $50 Basic listing.",
     f"""<section class="about-hero"><div class="wrap">
<div><span class="kicker">For software vendors</span><h1>Vendor pricing</h1>
<p class="lede">Buy one position, from #1 to #10, on a Vettlo category shortlist or alternatives page. Each position on a page goes to one vendor. Pay monthly, or yearly and save 10%.</p>
<div class="ctas"><a class="btn" href="/vendors/login/?new=1">Create a vendor account</a><a class="btn ghost" href="/vendors/login/">Sign in</a></div></div>
</div></section>
<div class="wrap about">
<section class="split"><div><span class="kicker">Prices</span><h2>Per page, in US dollars</h2></div>
<div class="prose"><table class="legal-table"><thead><tr><th>Plan</th><th>Monthly</th><th>Yearly (10% off)</th></tr></thead><tbody>{_rows}</tbody></table>
<p>Basic lists your product first under "Other tools to consider" on the page you choose. Card payments are processed by our payment provider; we never see or store card numbers.</p></div></section>
<section class="split"><div><span class="kicker">How it works</span><h2>From order to live</h2></div>
<div class="prose"><ol>
<li><strong>Pick a page and a position.</strong> In the vendor portal, choose a category shortlist or alternatives page, then a free position on it.</li>
<li><strong>Choose monthly or yearly and pay.</strong> Add your product (name and website), accept the <a href="/advertiser-terms/">advertiser terms</a> and pay by card.</li>
<li><strong>We review your product.</strong> It shows as "In editorial review" until we've written its review. Your paid time starts the day it goes live.</li>
</ol></div></section>
<section class="split"><div><span class="kicker">Cancelling</span><h2>Refunds and renewals</h2></div>
<div class="prose"><p>Cancel before your product goes live, or if we don't accept it, and you get a full refund. After it goes live, a monthly plan you stop runs to the end of the month you paid for. Details are in the <a href="/advertiser-terms/">advertiser terms</a>.</p>
<p>A position changes where your product appears on a page. It doesn't change its score or our review. Questions: <a href="mailto:vendors@vettlo.com">vendors@vettlo.com</a>.</p></div></section>
</div>""")
NOINDEX.add("/vendors/pricing/")

FOOTER = FOOTER.replace('<li><a href="/vendors/">For vendors</a></li>',
                        '<li><a href="/vendors/">For vendors</a></li><li><a href="/vendors/pricing/">Vendor pricing</a></li>')
