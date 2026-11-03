# Guides (topics). Runs after all category and comparison files, so prices below are read from the
# same verified category data and stay in sync when a category is refreshed.

def _ptable(rows, cols=("Tool", "Entry price", "Plan and billing", "Free plan / trial")):
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


# ---------- What is CRM software?
_crm_ranked = [t["id"] for t in TOOLS]
_crm_rows = [(f'<a href="/tools/best-crm-software/#{k}">{SHORT[k]}</a>', PRICING[k]["price"], PRICING[k]["note"], PRICING[k]["trial"]) for k in _crm_ranked]
_crm_low = min((_money(PRICING[k]["price"]), SHORT[k]) for k in _crm_ranked if _money(PRICING[k]["price"]))
_crm_high = max((_money(PRICING[k]["price"]), SHORT[k]) for k in _crm_ranked if _money(PRICING[k]["price"]))
_crm_free = [f"{SHORT[k]} ({PRICING[k]['trial'][0].lower() + PRICING[k]['trial'][1:]})" for k in _crm_ranked if PRICING[k]["trial"].lower().startswith("free")]

guide_page({
    "slug": "what-is-crm-software", "crumb": "What is CRM software?", "dept": "Sales", "cats": ["best-crm-software"],
    "date": "2026-11-01", "kicker": "Explainer",
    "title": "What Is CRM Software? Features, Types and Cost",
    "seo_title": f"What Is CRM Software? Features, Types and Cost ({YEAR}) | Vettlo",
    "desc": "CRM software explained: what a CRM does, the main types, who needs one and what it costs, with entry prices from the CRMs we rank.",
    "card": "What a CRM does, the three main types, and what teams pay for one.",
    "answer": ("CRM (customer relationship management) software is a shared database of the people and companies you sell to and the deals you're working on. "
               "It records every email, call and meeting, shows each deal's stage in a pipeline, reminds reps what to do next and reports on what will close. "
               f"Entry plans for the CRMs we rank run from {_fmt(_crm_low[0])} ({_crm_low[1]}) to {_fmt(_crm_high[0])} ({_crm_high[1]}) per user per month, and several have free plans."),
    "sections": [
        ("does", "What a CRM does", """<p>Every CRM is built around the same core records, then adds automation and reporting on top:</p>
<ul><li><b>Contacts and companies.</b> One record per person and account, with their details and full history.</li>
<li><b>Deals and pipeline.</b> Each opportunity moves through stages you define, from first conversation to closed won or lost.</li>
<li><b>Activities.</b> Calls, emails, meetings and tasks are logged against the right record, often automatically through email and calendar sync.</li>
<li><b>Automation.</b> Rules that assign leads, create follow-up tasks, move deals or send emails, so nothing depends on memory.</li>
<li><b>Reporting and forecasting.</b> Pipeline value by stage, win rates, activity by rep and a forecast of what will close this quarter.</li></ul>"""),
        ("who", "Who needs a CRM", """<p>A spreadsheet works until it doesn't. These are the usual signs a team has outgrown it:</p>
<ul><li>More than one person talks to the same customers, and nobody can see the full history.</li>
<li>Deals stall because follow-ups live in someone's inbox or head.</li>
<li>You can't say with confidence what will close this month or quarter.</li>
<li>Marketing hands over leads and can't tell what happened to them.</li></ul>
<p>Founders and very small teams can start on a free plan; growing sales teams usually need the automation and reporting on the second or third tier.</p>"""),
        ("types", "The main types of CRM", """<ul><li><b>Pipeline-first CRMs</b> focus on moving deals forward with a visual pipeline and activity reminders. They're quick to set up and easy for reps. Pipedrive is the best-known example.</li>
<li><b>All-in-one platforms</b> share one database across sales, marketing and service, with deep reporting and customization. HubSpot, Salesforce and Zoho CRM sit here; they suit teams that want one system across departments, and the biggest need an admin.</li>
<li><b>Communication-first CRMs</b> build calling, SMS and email sequences into the CRM for inside sales teams that live on the phone, such as Close.</li>
<li><b>Flexible-data CRMs</b> let you model your own objects, such as investors or partners, without an admin. Attio is one; they're popular with startups.</li></ul>"""),
        ("cost", "How much a CRM costs", f"""<p>Most CRMs charge per user per month, and the entry plan is rarely the one a sales team ends up on: automation, forecasting and custom reports usually sit one or two tiers up. Entry prices for the CRMs we rank, from each vendor's pricing page:</p>
{_ptable(_crm_rows)}
<p>Free plans: {", ".join(_crm_free) if _crm_free else "none of the ranked CRMs list one"}. Watch for one-time onboarding fees on higher tiers and for add-ons such as AI, calling or extra storage. For a full breakdown, including what a 10-person team pays a year, see <a href="/guides/crm-software-cost/">how much CRM software costs</a> and our <a href="/compare/hubspot-vs-pipedrive/">HubSpot vs Pipedrive</a> and <a href="/compare/salesforce-vs-hubspot/">Salesforce vs HubSpot</a> comparisons.</p>"""),
        ("choose", "How to choose a CRM", """<ol><li><b>Map your sales process first:</b> stages, who owns which step and what has to be logged.</li>
<li><b>Price the plan you'll need in a year,</b> not the entry plan, including onboarding fees and add-ons.</li>
<li><b>Check integrations</b> with your email, calendar, phone and marketing tools.</li>
<li><b>Run a real trial:</b> import 20 live deals and work them for a week with the people who'll use it daily.</li></ol>
<p>Our <a href="/tools/best-crm-software/">CRM shortlist</a> scores each option on six weighted criteria, and our <a href="/tools/best-crm-for-small-business/">small business guide</a> reweights them for teams of 1 to 20.</p>"""),
    ],
    "faqs": [
        ("What does CRM stand for?", "Customer relationship management: the practice, and the software, for managing a company's interactions with current and potential customers."),
        ("Is there a free CRM?", ("Yes. Among the CRMs we rank, free options include " + "; ".join(_crm_free) + ".") if _crm_free else "Several CRMs offer free trials; see our shortlist for current terms."),
        ("What is the difference between a CRM and a spreadsheet?", "A spreadsheet stores data; a CRM also logs activity automatically, reminds people what to do next, lets several people work the same accounts without overwriting each other, and reports on the pipeline."),
        ("How long does it take to set up a CRM?", "A small team can be running on a pipeline-first CRM in a day. Mid-market rollouts with custom fields, integrations and historical data commonly take several weeks."),
    ],
})


# ---------- How much does help desk software cost?
_hd = HD["tools"]
_hd_ranked = HD["_ranked"]
_hd_rows = [(f'<a href="/tools/best-help-desk-software/#{k}">{_hd[k]["name"]}</a>', _hd[k]["price"], _hd[k]["price_note"], _hd[k]["trial"]) for k in _hd_ranked]
_hd_usd = [(_money(_hd[k]["price"]), _hd[k]["name"]) for k in _hd_ranked if _money(_hd[k]["price"])]
_hd_lo, _hd_hi = min(_hd_usd), max(_hd_usd)
_hd_ex = "".join(f"<tr><td>{n}</td><td>{_fmt(v)}</td><td>{_fmt(v * 10 * 12)}</td></tr>" for v, n in sorted(_hd_usd))
_hd_ai = dict(HD["faqs"]).get("How do AI agents change help desk pricing?", "")
_hd_free = dict(HD["faqs"]).get("What is the best free help desk software?", "")

guide_page({
    "slug": "help-desk-software-cost", "crumb": "Help desk software cost", "dept": "Customer support", "cats": ["best-help-desk-software"],
    "date": "2026-11-01", "kicker": "Pricing guide",
    "title": f"How Much Does Help Desk Software Cost in {YEAR}?",
    "seo_title": f"How Much Does Help Desk Software Cost? ({YEAR} Prices) | Vettlo",
    "desc": "Help desk software prices per agent, what a 10-agent team pays a year, and how AI resolution fees and plan tiers change the bill.",
    "card": "Per-agent prices, a 10-agent yearly example and how AI fees add up.",
    "answer": (f"Entry plans for the help desks we rank start between {_fmt(_hd_lo[0])} and {_fmt(_hd_hi[0])} per agent per month in US dollars, "
               "and Zoho Desk lists euro prices. The entry plan is rarely the full bill: live chat, knowledge bases and SLAs often sit on higher tiers, "
               "and most vendors now charge for AI resolutions on top of seats."),
    "sections": [
        ("prices", "Entry prices by tool", f"""<p>The cheapest paid plan for each help desk in our ranking, from each vendor's pricing page:</p>
{_ptable(_hd_rows)}
<p class="small muted">{HD['price_footnote']}</p>"""),
        ("example", "What a 10-agent team pays per year", f"""<p>Ten agents on each vendor's entry plan, at the per-agent prices above (taxes, AI usage and add-ons excluded):</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Per agent per month</th><th>10 agents per year</th></tr></thead><tbody>{_hd_ex}</tbody></table></div>
<p>Check what each entry plan includes before comparing these totals. For example, our <a href="/compare/zendesk-vs-freshdesk/">Zendesk vs Freshdesk</a> comparison shows the plan each needs for a knowledge base and AI agent.</p>"""),
        ("drivers", "What drives the cost", f"""<ul><li><b>Agents.</b> Almost every help desk charges per agent (or seat) per month, so cost scales with team size. Some offer free light or viewer seats.</li>
<li><b>Plan tier.</b> Channels such as live chat and phone, a knowledge base, SLAs and custom reporting often start one or two tiers above the entry plan.</li>
<li><b>AI resolutions.</b> {_hd_ai}</li>
<li><b>Billing period.</b> Annual billing is usually cheaper than paying month to month.</li>
<li><b>One-time fees.</b> Some vendors charge onboarding fees on higher tiers, such as HubSpot Service Hub Professional.</li></ul>"""),
        ("save", "How to keep the bill down", """<ol><li>Price the plan that covers the channels you use today, not every channel you might add.</li>
<li>Estimate monthly AI resolutions before turning on an AI agent, and set a cap if the vendor offers one.</li>
<li>Give occasional users free light or collaborator seats where available.</li>
<li>Start on a free plan if your team is small; see the free options below.</li></ol>"""),
    ],
    "faqs": [
        ("How much does help desk software cost per agent?", f"Entry plans for the help desks we rank start between {_fmt(_hd_lo[0])} and {_fmt(_hd_hi[0])} per agent per month in US dollars, with higher tiers for more channels, SLAs and AI."),
        ("Is there free help desk software?", _hd_free or "Several help desks offer free plans for small teams; see our shortlist."),
        ("Do AI agents cost extra?", _hd_ai or "Most vendors charge for AI resolutions on top of seat prices."),
        ("Which help desk is best value?", dict(HD["faqs"]).get("What is the best help desk software?", "See our shortlist.")),
    ],
})


# ---------- How much does email marketing software cost?
_em = EM["tools"]
_em_ranked = EM["_ranked"]
_em_rows = [(f'<a href="/tools/best-email-marketing-software/#{k}">{_em[k]["name"]}</a>', _em[k]["price"], _em[k]["price_note"], _em[k]["trial"]) for k in _em_ranked]
_em_1k = dict(EM["faqs"]).get("How much does email marketing software cost for 1,000 contacts?", "")
_em_free = dict(EM["faqs"]).get("What is the best free email marketing software?", "")
_em_lo = min((_money(_em[k]["price"]), _em[k]["name"]) for k in _em_ranked if _money(_em[k]["price"]))

guide_page({
    "slug": "email-marketing-software-cost", "crumb": "Email marketing software cost", "dept": "Marketing", "cats": ["best-email-marketing-software"],
    "date": "2026-11-01", "kicker": "Pricing guide",
    "title": f"How Much Does Email Marketing Software Cost in {YEAR}?",
    "seo_title": f"How Much Does Email Marketing Software Cost? ({YEAR} Prices) | Vettlo",
    "desc": "Email marketing software prices by list size, the three ways vendors charge (contacts, sends, profiles), free plan limits and how to compare.",
    "card": "Prices by list size, the three pricing models and free plan limits.",
    "answer": (f"Paid email marketing plans start from {_fmt(_em_lo[0])} a month ({_em_lo[1]}) among the tools we rank, and the price rises with your list size. "
               + (_em_1k + " " if _em_1k else "") + "Most tools also have a free plan for small lists."),
    "sections": [
        ("prices", "Entry prices by tool", f"""<p>The cheapest paid plan for each tool in our ranking, at the smallest list size the vendor shows:</p>
{_ptable(_em_rows)}
<p class="small muted">{EM['price_footnote']}</p>"""),
        ("models", "Three ways vendors charge", """<ul><li><b>By contacts or subscribers.</b> The most common model: the price steps up as your list grows, usually with a monthly send limit tied to list size. Mailchimp, MailerLite, ActiveCampaign and Kit work this way.</li>
<li><b>By active profiles.</b> Similar, but counted on profiles you can message. Klaviyo prices email this way.</li>
<li><b>By emails sent.</b> You pay for monthly volume rather than list size, which suits big lists that send a few campaigns a month. Brevo prices this way.</li></ul>
<p>Because the models differ, compare tools at your own list size and sending frequency, not at the headline price.</p>"""),
        ("tiers", "What the higher tiers add", """<p>Entry plans usually cover campaigns and basic forms. The next tier is where multi-step automation, A/B testing, landing pages and removal of the vendor's logo tend to appear, and the top tier adds things like phone support, more seats and advanced segmentation. Our <a href="/tools/best-email-marketing-software/">shortlist</a> notes which plan first includes each of these for every tool.</p>"""),
        ("free", "Free plans", f"<p>{_em_free}</p><p>Free plans cap contacts or sends and often lock automation, so they suit a new list or a simple newsletter.</p>" if _em_free else "<p>Most tools offer a free plan for small lists.</p>"),
    ],
    "faqs": [
        ("How much does email marketing cost for 1,000 contacts?", _em_1k or "See our shortlist for prices at 1,000 contacts."),
        ("What is the cheapest email marketing software?", f"Among the tools we rank, the lowest entry price is {_fmt(_em_lo[0])} a month ({_em_lo[1]}). Compare at your own list size, since prices step up as the list grows."),
        ("Is there free email marketing software?", _em_free or "Yes, most tools offer a free plan for small lists."),
        ("Why do prices go up when my list grows?", "Most vendors price by the number of contacts, subscribers or active profiles, so each step in list size moves you to a higher price band. Vendors that price by emails sent are the exception."),
    ],
})


# ---------- How much does CRM software cost?
_cc_ranked = [t["id"] for t in TOOLS]
_cc_usd = sorted((_money(PRICING[k]["price"]), SHORT[k]) for k in _cc_ranked if _money(PRICING[k]["price"]))
_cc_lo, _cc_hi = _cc_usd[0][0], _cc_usd[-1][0]
_cc_lo_n = " and ".join(n for v, n in _cc_usd if v == _cc_lo)
_cc_hi_n = " and ".join(n for v, n in _cc_usd if v == _cc_hi)
_cc_rows = [(f'<a href="/tools/best-crm-software/#{k}">{SHORT[k]}</a>', PRICING[k]["price"], PRICING[k]["note"], PRICING[k]["trial"]) for k in _cc_ranked]
_cc_ex = "".join(f"<tr><td>{n}</td><td>{_fmt(v)}</td><td>{_fmt(v * 10 * 12)}</td></tr>" for v, n in _cc_usd)
_cc_mo = []  # (tool, annual-billing price, month-to-month price) where the vendor lists both
for k in _cc_ranked:
    _m = re.search(r"\(\$([\d.]+) monthly\)", PRICING[k]["note"])
    if _m and _money(PRICING[k]["price"]):
        _cc_mo.append((SHORT[k], _money(PRICING[k]["price"]), float(_m.group(1))))
_cc_mo_li = "".join(f"<li><b>{n}:</b> {_fmt(a)} billed annually vs {_fmt(m)} month to month, {_fmt((m - a) * 10 * 12)} more a year for 10 users</li>" for n, a, m in _cc_mo)
_cc_free = [f"{SHORT[k]}: {PRICING[k]['trial'][0].lower() + PRICING[k]['trial'][1:]}" for k in _cc_ranked if PRICING[k]["trial"].lower().startswith("free")]
_cc_faq = dict(FAQS)

guide_page({
    "slug": "crm-software-cost", "crumb": "CRM software cost", "dept": "Sales", "cats": ["best-crm-software"],
    "date": "2026-11-01", "kicker": "Pricing guide",
    "title": f"How Much Does CRM Software Cost in {YEAR}?",
    "seo_title": f"How Much Does CRM Software Cost? ({YEAR} Prices) | Vettlo",
    "desc": "CRM prices per user from the CRMs we rank, what a 10-person sales team pays a year, the cost of monthly billing and the fees beyond the license.",
    "card": "Per-user prices, a 10-person yearly example and the costs beyond the license.",
    "answer": (f"Entry plans for the CRMs we rank cost {_fmt(_cc_lo)} ({_cc_lo_n}) to {_fmt(_cc_hi)} ({_cc_hi_n}) per user per month on annual billing, "
               f"so a 10-person sales team pays {_fmt(_cc_lo * 120)} to {_fmt(_cc_hi * 120)} a year on entry plans. "
               "Most sales teams end up a tier or two higher, because sequences, automation and forecasting rarely sit on the entry plan, "
               "and implementation and data migration can add more than the license at larger companies."),
    "sections": [
        ("prices", "Entry prices by CRM", f"""<p>The cheapest paid plan for each CRM in our ranking, from each vendor's pricing page:</p>
{_ptable(_cc_rows)}
<p class="small muted">Starting prices from each vendor's pricing page, checked {PRICES_CHECKED}. Vendors change plans often; confirm before you buy.</p>"""),
        ("example", "What a 10-person sales team pays per year", f"""<p>Ten users on each vendor's entry plan, at the annual-billing prices above (taxes, add-ons and onboarding fees excluded):</p>
<div class="table-wrap"><table><thead><tr><th>CRM</th><th>Per user per month</th><th>10 users per year</th></tr></thead><tbody>{_cc_ex}</tbody></table></div>
<p>These totals compare entry plans only, and entry plans differ a lot in what they include. Check the plan that covers the workflows your team needs: our <a href="/compare/hubspot-vs-pipedrive/">HubSpot vs Pipedrive</a> comparison prices a 10-rep team on the plans that include sequences, automation and forecasting, and <a href="/compare/salesforce-vs-hubspot/">Salesforce vs HubSpot</a> does the same with Salesforce's suites.</p>"""),
        ("billing", "Annual vs monthly billing", (f"""<p>The prices above assume annual billing. Where a vendor also lists a month-to-month price for the same plan, paying monthly costs noticeably more:</p>
<ul>{_cc_mo_li}</ul>
<p>Monthly billing is worth the premium while you're still trialing a CRM with real deals. Once the team has settled on it, annual billing is the cheaper way to pay.</p>""" if _cc_mo else "<p>Most CRMs list their lowest per-user prices for annual billing; month-to-month billing usually costs more.</p>")),
        ("drivers", "What drives the cost beyond the entry price", f"""<ul><li><b>Users.</b> Nearly every CRM charges per user (or seat) per month, so cost scales with headcount. Count everyone who needs to log in, not just quota-carrying reps.</li>
<li><b>Plan tier.</b> Email sequences, workflow automation, forecasting and custom reports usually start one or two tiers above the entry plan, and per-user prices often rise steeply from one tier to the next.</li>
<li><b>One-time fees.</b> Some vendors charge onboarding fees on higher tiers; HubSpot does on Sales Hub Professional and Enterprise, as our <a href="/compare/hubspot-vs-pipedrive/">HubSpot vs Pipedrive</a> comparison shows.</li>
<li><b>Add-ons.</b> AI features, calling minutes, extra storage, data enrichment and sandboxes are often sold separately.</li>
<li><b>Implementation.</b> {_cc_faq.get("How much does CRM software cost?", "Budget for implementation, data migration and integrations as well as licenses.").split(". ", 1)[-1]}</li></ul>"""),
        ("budget", "How to budget for a CRM", f"""<ol><li><b>List the three workflows you can't live without,</b> such as a follow-up sequence after a demo or a weekly forecast call, and find the cheapest plan on each CRM that includes all three. That's your real price.</li>
<li><b>Multiply by every user for 12 months,</b> then add any onboarding fee and the add-ons you'll switch on.</li>
<li><b>Price year two as well.</b> First-year discounts and seat growth both change the renewal.</li>
<li><b>Start free if you're small.</b> {("Free options among the CRMs we rank: " + "; ".join(_cc_free) + ". ") if _cc_free else ""}See our <a href="/tools/best-free-crm-software/">best free CRM software</a> list for the limits of each.</li></ol>
<p>Our <a href="/tools/best-crm-software/">CRM shortlist</a> scores each option on six weighted criteria, including price and value, and our <a href="/tools/best-crm-for-small-business/">small business guide</a> reweights them for teams of 1 to 20. New to CRMs? Start with <a href="/guides/what-is-crm-software/">what CRM software is and what it does</a>.</p>"""),
    ],
    "faqs": [
        ("How much does a CRM cost per user?", f"Entry plans for the CRMs we rank cost {_fmt(_cc_lo)} to {_fmt(_cc_hi)} per user per month on annual billing. Plans with sequences, automation and forecasting cost more per user."),
        ("How much does a CRM cost for a team of 10?", f"On entry plans with annual billing, 10 users cost {_fmt(_cc_lo * 120)} ({_cc_lo_n}) to {_fmt(_cc_hi * 120)} ({_cc_hi_n}) a year, before taxes, add-ons and onboarding fees."),
        ("What is the cheapest CRM?", f"Among the CRMs we rank, {_cc_lo_n} has the lowest entry price at {_fmt(_cc_lo)} per user per month on annual billing. " + (("Free plans are also available from " + "; ".join(_cc_free) + ".") if _cc_free else "")),
        ("Why does CRM cost so much more than the entry price?", _cc_faq.get("How much does CRM software cost?", "Automation, forecasting and custom reporting usually sit on higher tiers, and implementation adds to the license cost.")),
    ],
})


# ---------- How much does project management software cost?
_pm = PM["tools"]
_pm_ranked = PM["_ranked"]
_pm_cat = "/tools/best-project-management-software/"
_pm_rows = [(f'<a href="{_pm_cat}#{k}">{_pm[k]["name"]}</a>', _pm[k]["price"], _pm[k]["price_note"], _pm[k]["trial"]) for k in _pm_ranked]
_pm_usd = sorted((_money(_pm[k]["price"]), _pm[k]["name"], k) for k in _pm_ranked if _money(_pm[k]["price"]))
_pm_lo, _pm_hi = _pm_usd[0][0], _pm_usd[-1][0]
_pm_lo_n = " and ".join(n for v, n, _k in _pm_usd if v == _pm_lo)
_pm_hi_n = " and ".join(n for v, n, _k in _pm_usd if v == _pm_hi)
_pm_ex = "".join(f'<tr><td>{n}</td><td>{_fmt(v)}</td><td>{_fmt(v * 10 * 12)}</td><td class="small">{_pm[k]["price_note"]}</td></tr>' for v, n, k in _pm_usd)
_pm_mo = []  # (tool, annual-billing price, month-to-month price) where the vendor lists both
for k in _pm_ranked:
    _m = re.search(r"\(\$([\d.]+) monthly\)", _pm[k]["price_note"])
    if _m and _money(_pm[k]["price"]):
        _pm_mo.append((_pm[k]["name"], _money(_pm[k]["price"]), float(_m.group(1))))
_pm_mo_li = "".join(f"<li><b>{n}:</b> {_fmt(a)} billed annually vs {_fmt(m)} month to month, {_fmt((m - a) * 10 * 12)} more a year for 10 users</li>" for n, a, m in _pm_mo)
_pm_free = [f"{_pm[k]['name']}: {_pm[k]['trial']}" for k in _pm_ranked if re.match(r"free (plan|forever)", _pm[k]["trial"], re.I)]
_pm_faq = dict(PM["faqs"])
_pm_choose = dict(PM["choose"])
# Flat-fee comparison: Basecamp (scored below our threshold, but the main flat-priced alternative)
_bc = _pm.get("basecamp", {})
_bc_top = re.search(r"Pro Unlimited \$([\d,]+)/mo", _bc.get("price_note", ""))
_bc_top = float(_bc_top.group(1).replace(",", "")) if _bc_top else None
_bc_lo = _money(_bc.get("price", "")) if _bc else None
_pm_top_seat = max(_pm_usd)  # highest entry seat price among ranked tools
_bc_break = int(_bc_top // _pm_top_seat[0]) + 1 if _bc_top else None
_pm_flat = (f"""<p>Basecamp is the main exception to per-seat pricing. {_bc['what']} At {_fmt(_bc_top)} a month, its unlimited plan costs less than putting every user on {_pm_top_seat[1]}'s {_fmt(_pm_top_seat[0])} entry plan once a team reaches {_bc_break} people. It scored below our threshold for the ranking because it lacks Gantt and timeline planning, but for large, simple teams the flat fee is worth pricing.</p>"""
            if _bc_top and _bc_lo else "")

guide_page({
    "slug": "project-management-software-cost", "crumb": "Project management software cost", "dept": "Projects & operations", "cats": ["best-project-management-software"],
    "date": "2026-11-02", "kicker": "Pricing guide",
    "title": f"How Much Does Project Management Software Cost in {YEAR}?",
    "seo_title": f"Project Management Software Cost ({YEAR} Prices) | Vettlo",
    "desc": "Project management software prices per user, what a 10-person team pays a year, the plan that unlocks Gantt charts, and per-seat vs flat pricing.",
    "card": "Per-user prices, a 10-person yearly example and which plan unlocks Gantt charts.",
    "answer": (f"Entry plans for the project management tools we rank cost {_fmt(_pm_lo)} ({_pm_lo_n}) to {_fmt(_pm_hi)} ({_pm_hi_n}) per user per month on annual billing, "
               f"so a 10-person team pays {_fmt(_pm_lo * 120)} to {_fmt(_pm_hi * 120)} a year on entry plans. "
               "Timeline views, higher automation limits, time tracking and portfolios often sit one or two tiers higher, so price the plan that has the features you need, not the entry plan."),
    "sections": [
        ("prices", "Entry prices by tool", f"""<p>The cheapest paid plan for each tool in our ranking, from each vendor's pricing page:</p>
{_ptable(_pm_rows)}
<p class="small muted">{PM['price_footnote']}</p>"""),
        ("example", "What a 10-person team pays per year", f"""<p>Ten users on each vendor's entry plan, at the annual-billing prices above (taxes, add-ons and extra AI usage excluded):</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Per user per month</th><th>10 users per year</th><th>Plan terms</th></tr></thead><tbody>{_pm_ex}</tbody></table></div>
<p>Read the plan terms before comparing totals: some entry plans cap the number of members or sell seats in minimum bundles, and entry plans differ in what they include. Our <a href="/compare/clickup-vs-asana/">ClickUp vs Asana</a> and <a href="/compare/asana-vs-monday/">Asana vs monday.com</a> comparisons price a 10-person team on the plan each tool needs for timelines, automations, time tracking and portfolios.</p>"""),
        ("tiers", "Which plan you'll actually need", f"""<p>The entry plan is often not the one a team keeps. These features decide which tier you land on:</p>
<ul><li><b>Timeline and Gantt views.</b> {_pm_choose.get("Find the plan with the views you need.", "Check which plan first includes timeline or Gantt views.")}</li>
<li><b>Automation limits.</b> {_pm_choose.get("Check automation limits.", "Some tools cap automation actions per month by plan.")}</li>
<li><b>Time tracking, portfolios and resource planning.</b> {_pm_faq.get("How much does project management software cost?", "").split(". ", 1)[-1]} Some vendors put resource planning on plans priced by quote.</li></ul>
<p>Our <a href="{_pm_cat}">project management shortlist</a> notes the plan each feature sits on for every tool.</p>"""),
        ("drivers", "Per-seat vs flat pricing and other cost drivers", f"""<ul><li><b>Paid seats.</b> Most tools charge per user per month. {_pm_choose.get("Count who needs a paid seat.", "Free viewer or guest seats change the cost for wide teams.")}</li>
<li><b>Billing period.</b> The prices above assume annual billing. Where a vendor also lists a month-to-month price for the same plan, paying monthly costs more:{f"<ul>{_pm_mo_li}</ul>" if _pm_mo else " check each vendor's pricing page."}</li>
<li><b>AI add-ons.</b> Some vendors include a monthly allowance of AI credits or requests and charge for more.</li>
<li><b>Discounted list prices.</b> Some vendors show plans as discounts from a higher regular price; confirm the renewal price at checkout.</li></ul>
{_pm_flat}"""),
        ("budget", "How to budget for project management software", f"""<ol><li><b>List the views and limits you need on day one,</b> such as a Gantt chart, 500 automations a month or time tracking, and find the cheapest plan on each tool that includes all of them.</li>
<li><b>Count paid seats separately from viewers and guests,</b> then multiply by 12 months.</li>
<li><b>Check seat minimums and caps</b> so a plan still fits when the team grows.</li>
<li><b>Start free if you're small.</b> {(_pm_faq.get("What is the best free project management software?", "") + " ") if _pm_free else ""}See our <a href="/tools/best-free-project-management-software/">best free project management software</a> list for the limits of each.</li></ol>
<p>Our <a href="{_pm_cat}">shortlist</a> scores each tool on six weighted criteria, including price and value, and our <a href="/tools/best-project-management-software-for-small-business/">small business list</a> reweights them for smaller teams. Moving off Asana? See <a href="/tools/best-asana-alternatives/">Asana alternatives</a>.</p>"""),
    ],
    "faqs": [
        ("How much does project management software cost per user?", f"Entry plans for the tools we rank cost {_fmt(_pm_lo)} to {_fmt(_pm_hi)} per user per month on annual billing. Plans with portfolios, resource planning and higher automation limits cost more per user."),
        ("How much does project management software cost for a team of 10?", f"On entry plans with annual billing, 10 users cost {_fmt(_pm_lo * 120)} ({_pm_lo_n}) to {_fmt(_pm_hi * 120)} ({_pm_hi_n}) a year, before taxes and add-ons."),
        ("What is the cheapest project management software?", f"Among the tools we rank, {_pm_lo_n} has the lowest entry price at {_fmt(_pm_lo)} per user per month on annual billing. " + (f"{len(_pm_free)} of the {len(_pm_ranked)} also have free plans for small teams." if _pm_free else "")),
        ("Which project management tools include Gantt charts on the cheapest plan?", _pm_faq.get("Which project management tools include Gantt charts?", "See our shortlist for which plan first includes Gantt charts.")),
    ],
})


# ---------- What is sales engagement software?
_se = SE["tools"]
_se_ranked = SE["_ranked"]
_se_cat = "/tools/best-sales-engagement-software/"
_se_faq = dict(SE["faqs"])
_se_choose = SE["choose"]
_se_rv = lambda k: (f'<a href="{REVIEW_URL[_se[k]["name"]]}">{_se[k]["name"]}</a>' if _se[k]["name"] in REVIEW_URL else _se[k]["name"])
_se_rows = [(f'<a href="{_se_cat}#{k}">{_se[k]["name"]}</a>', _se[k]["price"], _se[k]["price_note"], _se[k]["trial"]) for k in _se_ranked]
_se_seat = sorted((_money(_se[k]["price"]), _se[k]["name"], k) for k in _se_ranked
                  if _money(_se[k]["price"]) and re.search(r"/(user|seat)/", _se[k]["price"]))
_se_other = [k for k in _se_ranked if _money(_se[k]["price"]) and not re.search(r"/(user|seat)/", _se[k]["price"])]
_se_quote = [_se[k]["name"] for k in _se_ranked if not _money(_se[k]["price"])]
_se_free = [_se[k]["name"] for k in _se_ranked if re.match(r"free plan", _se[k]["trial"], re.I)]
_se_lo, _se_hi = _se_seat[0][0], _se_seat[-1][0]
_se_lo_n = " and ".join(n for v, n, _k in _se_seat if v == _se_lo)
_se_hi_n = " and ".join(n for v, n, _k in _se_seat if v == _se_hi)
_se_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_se_other_li = "".join(f'<li><b>{_se[k]["name"]}:</b> {_se[k]["price"]}. {_se[k]["price_note"]}.</li>' for k in _se_other)
_se_seat_range = (f"{_fmt(_se_lo)} ({_se_lo_n}) to {_fmt(_se_hi)} ({_se_hi_n}) per user per month" if _se_lo != _se_hi else f"{_fmt(_se_lo)} per user per month ({_se_lo_n})")
_se_seat_verb = "run from" if _se_lo != _se_hi else "start at"
_se_q_txt = (f"{_se_and(_se_quote)} don't publish prices. " + _se_faq.get("How much do Outreach and Salesloft cost?", "").split(". ")[-1].rstrip(".") + ".") if _se_quote else ""
_se_seat_year = (f"{_fmt(_se_lo * 120)} to {_fmt(_se_hi * 120)}" if _se_lo != _se_hi else _fmt(_se_lo * 120))
_se_feats = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in EXPLAIN["best-sales-engagement-software"]["features"])
_se_by = lambda *ks: _se_and([_se_rv(k) for k in ks if k in _se_ranked]) if any(k in _se_ranked for k in ks) else ""

guide_page({
    "slug": "what-is-sales-engagement-software", "crumb": "What is sales engagement software?", "dept": "Sales", "cats": ["best-sales-engagement-software"],
    "date": "2026-11-03", "kicker": "Explainer",
    "title": "What Is Sales Engagement Software? Features, Types and Cost",
    "seo_title": "What Is Sales Engagement Software? Features and Cost | Vettlo",
    "desc": "Sales engagement software explained: what it does, how it differs from a CRM and cold email tools, the main types and what the platforms we rank cost.",
    "card": "What sequences do, how it differs from a CRM, the main types and what it costs.",
    "answer": ("Sales engagement software runs multi-step outreach sequences across email, phone and LinkedIn, so reps contact prospects on schedule and stop when someone replies. "
               "It sits next to the CRM: the CRM is the record of contacts and deals, while the engagement platform does the outreach and logs the activity back. "
               f"Published entry prices among the platforms we rank start at {_se_seat_range}"
               + (f", while {_se_and(_se_quote)} sell by quote." if _se_quote else ".")),
    "sections": [
        ("does", "What sales engagement software does", f"""<p>A sequence is the core of every sales engagement platform: a timed series of steps, such as an email on day one, a call task on day three and a LinkedIn message on day five, that a prospect moves through until they reply, book a meeting or reach the end. Around that, platforms add:</p>
<ul>{_se_feats}</ul>
<p>The result is that follow-up no longer depends on each rep's memory or inbox. Managers can see which sequences, steps and templates get replies and copy what works across the team.</p>"""),
        ("vs", "Sales engagement vs CRM vs cold email tools", f"""<p>The three overlap, so it helps to separate what each is for:</p>
<ul><li><b>A CRM</b> is the system of record: contacts, companies, deals and pipeline stages. {_se_faq.get("Do I need a sales engagement platform if my CRM has sequences?", "").split(". ", 1)[-1]}</li>
<li><b>A sales engagement platform</b> runs the outreach itself: multichannel sequences across email, calls and LinkedIn, sending controls, and reply and meeting analytics for managers, with the activity synced back to the CRM.</li>
<li><b>Cold email tools</b> are narrower. {_se_faq.get("What is the difference between sales engagement and cold email software?", "").split(". ", 1)[-1]}</li></ul>
<p>Most outbound teams run a CRM plus one outreach tool. If your CRM's built-in sequences cover email-only follow-up for a handful of reps, you may not need a second tool yet; see our <a href="/tools/best-crm-software/">CRM shortlist</a> for which plans include them.</p>"""),
        ("types", "The main types of sales engagement platform", f"""<ul><li><b>Enterprise sales execution platforms</b> add governed sequences, call recording, deal management and forecasting for large teams with a RevOps owner. {_se_by("outreach", "salesloft")} sit here; our <a href="/compare/outreach-vs-salesloft/">Outreach vs Salesloft</a> comparison covers which package to ask each for.</li>
<li><b>Data plus engagement in one tool</b> bundles a B2B contact database with sequencing, so you don't buy prospect data separately. {_se_by("apollo")} is the best-known example; credits limit how many contacts you can reveal.</li>
<li><b>Multichannel outreach tools</b> run email, LinkedIn and call steps at a published, self-serve price for SMB and mid-market teams, such as {_se_by("reply", "lemlist")}.</li>
<li><b>Cold email platforms</b> focus on sending volume and deliverability across many connected inboxes, such as {_se_by("instantly")}. They're email-first rather than full multichannel suites.</li></ul>
<p>Inbox add-ons that put sequences inside Gmail, such as Mixmax, are a lighter fifth option. Our <a href="{_se_cat}">shortlist</a> scores each platform on sequencing, deliverability, data, CRM sync, analytics and price.</p>"""),
        ("cost", "How much sales engagement software costs", f"""<p>Pricing units vary more in this category than in most. Some platforms charge per user or seat, some charge a flat price per workspace plan, and enterprise vendors quote. Entry plans for the platforms we rank, from each vendor's pricing page:</p>
{_ptable(_se_rows)}
<p class="small muted">{SE['price_footnote']}</p>
<p>Per-user entry plans {_se_seat_verb} {_se_seat_range}, which is {_se_seat_year} a year for a 10-rep team before add-ons.{(" Priced differently:</p><ul>" + _se_other_li + "</ul><p>") if _se_other else " "}{(_se_q_txt + " ") if _se_quote else ""}{"Free plan" if len(_se_free) == 1 else "Free plans"}: {_se_and(_se_free) if _se_free else "none of the ranked platforms list one"}.</p>
<p>Beyond the license, budget for contact data (credits or a separate provider), extra sending inboxes and domains for cold email, and dialer minutes. Comparing Apollo.io with a data-only provider? See <a href="/compare/apollo-vs-zoominfo/">Apollo.io vs ZoomInfo</a>.</p>"""),
        ("choose", "How to choose a sales engagement platform", "<ol>" + "".join(f"<li><b>{a}</b> {b}</li>" for a, b in _se_choose) + f"""</ol>
<p>Our <a href="{_se_cat}">sales engagement shortlist</a> ranks {len(_se_ranked)} platforms, our <a href="/tools/best-sales-engagement-software-for-small-business/">small business list</a> reweights them for smaller teams, and <a href="/tools/best-apollo-alternatives/">Apollo.io alternatives</a> covers what to switch to when credits or sending limits run short.</p>"""),
    ],
    "faqs": [
        ("What is a sales sequence?", "A sequence is a timed series of outreach steps, such as emails, call tasks and LinkedIn messages, that a prospect moves through automatically. It stops when the prospect replies or books a meeting, so reps don't follow up with someone who already answered."),
        ("Is sales engagement software the same as a CRM?", "No. A CRM stores contacts, companies and deals and tracks the pipeline; a sales engagement platform runs the outreach and syncs the resulting activity back to the CRM. Some CRMs include basic sequences, and some engagement platforms include light deal tracking."),
        ("How much does sales engagement software cost?", f"Per-user entry plans for the platforms we rank {"cost" if _se_lo != _se_hi else "start at"} {_se_seat_range}." + (f" {_se_and(_se_quote)} don't publish prices." if _se_quote else "") + (f" {_se_and([_se[k]['name'] for k in _se_other])} {'lists' if len(_se_other) == 1 else 'list'} plan prices without a per-user unit; see our shortlist for each plan's terms." if _se_other else "")),
        ("Is there free sales engagement software?", _se_faq.get("Is there a free sales engagement platform?", "Some platforms have free plans; most offer 14-day trials.")),
    ],
})
