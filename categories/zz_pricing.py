# Public vendor pricing page and refund policy. Paddle's seller review needs both: prices on the site must match the
# Paddle catalog, and the refund policy must be public. Not indexed.
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
<p>Basic lists your product first under "Other tools to consider" on the page you choose. Applicable sales tax or VAT is added at checkout. Payments are processed by Paddle.com, our online reseller and Merchant of Record, which also issues your invoices.</p></div></section>
<section class="split"><div><span class="kicker">How it works</span><h2>From order to live</h2></div>
<div class="prose"><ol>
<li><strong>Pick a page and a position.</strong> In the vendor portal, choose a category shortlist or alternatives page, then a free position on it.</li>
<li><strong>Choose monthly or yearly and subscribe.</strong> Add your product (name and website), accept the <a href="/advertiser-terms/">advertiser terms</a> and pay through Paddle's secure checkout.</li>
<li><strong>We review your product.</strong> It shows as "In editorial review" until we've written its review. Your paid time starts the day it goes live.</li>
</ol></div></section>
<section class="split"><div><span class="kicker">Cancelling</span><h2>Refunds and renewals</h2></div>
<div class="prose"><p>Plans renew automatically every month or year until you cancel in the portal; a cancelled plan stays live until the end of the period you paid for. Every payment can be refunded in full within 14 days, no questions asked. See the <a href="/refunds/">refund policy</a> and <a href="/advertiser-terms/">advertiser terms</a>.</p>
<p>A position changes where your product appears on a page. It doesn't change its score or our review. Questions: <a href="mailto:vendors@vettlo.com">vendors@vettlo.com</a>.</p></div></section>
</div>""")
NOINDEX.add("/vendors/pricing/")

FOOTER = FOOTER.replace('<li><a href="/vendors/">For vendors</a></li>',
                        '<li><a href="/vendors/">For vendors</a></li><li><a href="/vendors/pricing/">Vendor pricing</a></li>')

page("/refunds/", "Refund Policy: 14-Day Refunds on Vendor Plans | Vettlo",
     "Vettlo's refund policy for vendor plans: a full refund of any payment within 14 days, no questions asked, processed by Paddle, plus how cancelling works.",
     """<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Refund policy</h1>
<p>How refunds and cancellations work for positions and listings bought on Vettlo.</p>
<p class="small mono">Last updated Nov 20, 2026</p></div>
<div class="page-body prose">
<h2>14-day refunds</h2>
<p>You can get a full refund of any payment, whether it's your first payment or a renewal, if you ask within 14 days of that payment. No questions asked.</p>
<h2>How to ask for a refund</h2>
<p>Email <a href="mailto:vendors@vettlo.com">vendors@vettlo.com</a> or use our <a href="/contact/">contact page</a> with the email address you used to pay. You can also reply to your Paddle receipt. Our order process is conducted by our online reseller Paddle.com, the Merchant of Record for all our orders, so refunds are paid by Paddle to the payment method you used. Banks usually take 5 to 10 business days to show it.</p>
<h2>Products we don't accept</h2>
<p>If we decline your product after you've paid, or you cancel before your product goes live, we refund the full payment, whenever that happens.</p>
<h2>Cancelling a plan</h2>
<p>Plans renew automatically every month or year until you cancel in the vendor portal. A cancelled plan doesn't renew and stays live until the end of the period you paid for. After the 14-day window, the current period isn't refunded.</p>
<p>If we end your plan early for a reason other than a breach of our <a href="/advertiser-terms/">advertiser terms</a>, we refund the unused part of the period.</p>
</div></div>""")
