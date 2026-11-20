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
<p>Our <a href="/tools/best-crm-software/">CRM shortlist</a> scores each option on six weighted criteria.</p>"""),
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
    "desc": "Help desk software prices per agent, what a 10-agent team pays a year, and how AI resolution fees and plan tiers change the bill, from vendor pages.",
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
<p class="small muted">Starting prices from each vendor's pricing page, checked {PRICES_CHECKED}.</p>"""),
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
<li><b>Start free if you're small.</b> {("Free options among the CRMs we rank: " + "; ".join(_cc_free) + ". ") if _cc_free else ""}Our <a href="/tools/best-crm-software/">CRM shortlist</a> shows what each free plan includes.</li></ol>
<p>Our <a href="/tools/best-crm-software/">CRM shortlist</a> scores each option on six weighted criteria, including price and value. New to CRMs? Start with <a href="/guides/what-is-crm-software/">what CRM software is and what it does</a>.</p>"""),
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
<li><b>Start free if you're small.</b> {(_pm_faq.get("What is the best free project management software?", "") + " ") if _pm_free else ""}Our <a href="/tools/best-project-management-software/">project management shortlist</a> shows what each free plan includes.</li></ol>
<p>Our <a href="{_pm_cat}">shortlist</a> scores each tool on six weighted criteria, including price and value. Moving off Asana? See <a href="/tools/best-asana-alternatives/">Asana alternatives</a>.</p>"""),
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
<p>Our <a href="{_se_cat}">sales engagement shortlist</a> ranks {len(_se_ranked)} platforms, and <a href="/tools/best-apollo-alternatives/">Apollo.io alternatives</a> covers what to switch to when credits or sending limits run short.</p>"""),
    ],
    "faqs": [
        ("What is a sales sequence?", "A sequence is a timed series of outreach steps, such as emails, call tasks and LinkedIn messages, that a prospect moves through automatically. It stops when the prospect replies or books a meeting, so reps don't follow up with someone who already answered."),
        ("Is sales engagement software the same as a CRM?", "No. A CRM stores contacts, companies and deals and tracks the pipeline; a sales engagement platform runs the outreach and syncs the resulting activity back to the CRM. Some CRMs include basic sequences, and some engagement platforms include light deal tracking."),
        ("How much does sales engagement software cost?", f"Per-user entry plans for the platforms we rank {"cost" if _se_lo != _se_hi else "start at"} {_se_seat_range}." + (f" {_se_and(_se_quote)} don't publish prices." if _se_quote else "") + (f" {_se_and([_se[k]['name'] for k in _se_other])} {'lists' if len(_se_other) == 1 else 'list'} plan prices without a per-user unit; see our shortlist for each plan's terms." if _se_other else "")),
        ("Is there free sales engagement software?", _se_faq.get("Is there a free sales engagement platform?", "Some platforms have free plans; most offer 14-day trials.")),
    ],
})


# ---------- How much does payroll software cost?
_py = PAY["tools"]
_py_ranked = PAY["_ranked"]
_py_cat = "/tools/best-payroll-software/"
_py_faq = dict(PAY["faqs"])
_py_choose = dict(PAY["choose"])
_py_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _py_bp(s):
    """(base, per-person) from strings like "$49/mo + $6/person"; None when not base-plus-per-person."""
    m = re.search(r"\$([\d,.]+)(?:/mo)?\s*\+\s*\$([\d,.]+)", s)
    return (float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))) if m else None


_py_pub = [(k, _py_bp(_py[k]["price"])) for k in _py_ranked if _py_bp(_py[k]["price"])]  # published base + per-person entry plans
_py_unpub = [k for k in _py_ranked if not _py_bp(_py[k]["price"])]
_py_cost = lambda bp, n: bp[0] + bp[1] * n
_py_10 = sorted((_py_cost(bp, 10), _py[k]["name"], k) for k, bp in _py_pub)
_py_lo, _py_hi = _py_10[0], _py_10[-1]
_py_bases = sorted(bp[0] for _k, bp in _py_pub)
_py_pers = sorted(bp[1] for _k, bp in _py_pub)
_py_rows = [(f'<a href="{_py_cat}#{k}">{_py[k]["name"]}</a>', _py[k]["price"], _py[k]["price_note"], _py[k]["trial"]) for k in _py_ranked]
_py_ex = "".join(f'<tr><td>{n}</td>' + "".join(f"<td>{_fmt(_py_cost(dict(_py_pub)[k], h))}</td>" for h in (5, 10, 25))
                 + f'<td>{_fmt(_py_cost(dict(_py_pub)[k], 10) * 12)}</td></tr>' for _v, n, k in _py_10)
# Higher tiers listed in price notes, e.g. "Plus $80 + $12/person" or "Premium $88 + $13"
_py_tiers = []
for k in ("gusto", "quickbooks_payroll"):
    if k in _py and _py_bp(_py[k]["price"]):
        _t = [(f'{_py[k]["short"].split()[0]} {_py[k]["price_note"].split(";")[0].split(",")[0]}', _py_bp(_py[k]["price"]))]
        _t += [(f'{_py[k]["short"].split()[0]} {nm}', (float(b), float(p))) for nm, b, p in re.findall(r"([A-Z][a-z]+) \$([\d.]+) \+ \$([\d.]+)", _py[k]["price_note"])]
        _py_tiers.append(_t)
_py_tier_rows = "".join(f"<tr><td>{nm}</td><td>{_fmt(bp[0])} + {_fmt(bp[1])}</td><td>{_fmt(_py_cost(bp, 10))}</td><td>{_fmt(_py_cost(bp, 10) * 12)}</td></tr>" for t in _py_tiers for nm, bp in t)
# OnPay add-ons and Patriot's per-state fee, read from the category text
_op = _py.get("onpay", {})
_op_bp = _py_bp(_op.get("price", "")) if _op else None
_op_hr = re.search(r"HR add-on \$([\d.]+) \+ \$([\d.]+)/worker", _op.get("price_note", ""))
_op_tt = re.search(r"time tracking \$([\d.]+) \+ \$([\d.]+)/worker", _op.get("price_note", ""))
_op_txt = ""
if _op_bp and _op_hr and _op_tt:
    _op_hr10 = float(_op_hr.group(1)) + float(_op_hr.group(2)) * 10
    _op_tt10 = float(_op_tt.group(1)) + float(_op_tt.group(2)) * 10
    _op_txt = (f"<li><b>OnPay add-ons.</b> OnPay's single plan is {_fmt(_py_cost(_op_bp, 10))} a month for 10 people. Its HR tools ({_fmt(float(_op_hr.group(1)))} + {_fmt(float(_op_hr.group(2)))} per worker) add {_fmt(_op_hr10)} "
               f"and time tracking ({_fmt(float(_op_tt.group(1)))} + {_fmt(float(_op_tt.group(2)))} per worker) adds {_fmt(_op_tt10)}, so the bundle comes to {_fmt(_py_cost(_op_bp, 10) + _op_hr10 + _op_tt10)} a month.</li>")
_pa = _py.get("patriot", {})
_pa_st = re.search(r"additional state costs \$([\d.]+) a month", _pa.get("what", ""))
_pa_bp = _py_bp(_pa.get("price", "")) if _pa else None
_pa_basic = re.search(r"Basic \(you file taxes\) \$([\d.]+) \+ \$([\d.]+)", _pa.get("price_note", ""))
_pa_txt = (f"<li><b>Extra states.</b> {_py_choose.get('Check multi-state before you sign.', '')} At 10 employees in two states, Patriot Full Service comes to {_fmt(_py_cost(_pa_bp, 10) + float(_pa_st.group(1)))} a month.</li>"
           if _pa_st and _pa_bp else "")
_sq = _py.get("square_payroll", {})
_sq_c = re.search(r"Contractor-only payroll costs \$([\d.]+) per person", _sq.get("what", ""))
_gu_c = re.search(r"Contractor plan costs \$([\d.]+) a month plus \$([\d.]+) per contractor", _py.get("gusto", {}).get("what", ""))
_py_contr = []
if _sq_c:
    _py_contr.append(f"Square Payroll's contractor-only payroll costs {_fmt(float(_sq_c.group(1)))} per person with no base fee")
if _gu_c:
    _py_contr.append(f"Gusto's Contractor plan costs {_fmt(float(_gu_c.group(1)))} a month plus {_fmt(float(_gu_c.group(2)))} per contractor")
_py_unpub_li = "".join(f'<li><b>{_py[k]["name"]}:</b> {_py[k]["price"]}. {_py[k]["price_note"]}.</li>' for k in _py_unpub)
_py_rev = lambda k, slug: f'<a href="/tools/{slug}-review/">{_py[k]["short"]}</a>' if k in _py else ""

guide_page({
    "slug": "payroll-software-cost", "crumb": "Payroll software cost", "dept": "HR & people", "cats": ["best-payroll-software"],
    "date": "2026-11-04", "kicker": "Pricing guide",
    "title": f"How Much Does Payroll Software Cost in {YEAR}?",
    "seo_title": f"How Much Does Payroll Software Cost? ({YEAR} Prices) | Vettlo",
    "desc": "Payroll software prices: base fee plus per-employee fees, what 5, 10 and 25 employees pay, higher plans, add-ons and the cost of extra states.",
    "card": "Base and per-employee fees, costs at 5, 10 and 25 employees, and the add-ons.",
    "answer": (f"Full-service payroll software, which files your payroll taxes, costs a monthly base fee of {_fmt(_py_bases[0])} to {_fmt(_py_bases[-1])} plus {_fmt(_py_pers[0])} to {_fmt(_py_pers[-1])} per employee among the providers we rank that publish prices. "
               f"For 10 employees that's {_fmt(_py_lo[0])} a month ({_py_lo[1]}) to {_fmt(_py_hi[0])} ({_py_hi[1]}), or {_fmt(_py_lo[0] * 12)} to {_fmt(_py_hi[0] * 12)} a year. "
               + (f"{_py_and([_py[k]['name'] for k in _py_unpub])} price by quote." if _py_unpub else "")),
    "sections": [
        ("model", "How payroll software is priced", f"""<p>Almost every small-business payroll service charges the same way: a <b>monthly base fee</b> for the account plus a <b>fee for each person you pay</b> that month. The base fee matters most for very small teams; past a handful of employees, the per-person fee decides the bill.</p>
<ul><li><b>Full-service vs do-it-yourself.</b> Full-service plans calculate, file and pay federal, state and local payroll taxes for you. {f"Patriot also sells a Basic plan for {_fmt(float(_pa_basic.group(1)))} a month plus {_fmt(float(_pa_basic.group(2)))} per worker, but you file the taxes yourself." if _pa_basic else "A few vendors sell cheaper plans where you file the taxes yourself."}</li>
<li><b>Who counts as a person.</b> The per-person fee can cover contractors as well as employees; OnPay, for example, counts both. If you pay many contractors, check how each vendor counts them, or look at a contractor-only plan.</li>
<li><b>Plan tiers.</b> Higher tiers raise both the base and the per-person fee, and add things like multi-state payroll, faster direct deposit, time tracking and HR support.</li>
<li><b>Quotes.</b> Platforms that bundle payroll with HR, benefits or IT often publish only a starting price or none at all.</li></ul>"""),
        ("prices", "Entry prices by provider", f"""<p>The entry plan that files payroll taxes for each provider in our ranking, from each vendor's pricing page:</p>
{_ptable(_py_rows, ("Provider", "Entry price", "Plans and add-ons", "Trial"))}
<p class="small muted">{PAY['price_footnote']}</p>"""),
        ("example", "What 5, 10 and 25 employees cost", f"""<p>Monthly cost on each entry plan at the published base and per-person fees, with the yearly total for 10 employees. Introductory discounts, add-ons and taxes are excluded:</p>
<div class="table-wrap"><table><thead><tr><th>Provider</th><th>5 employees</th><th>10 employees</th><th>25 employees</th><th>10 employees per year</th></tr></thead><tbody>{_py_ex}</tbody></table></div>
<p>Entry plans differ in what they include, so the cheapest line isn't always the cheapest fit. Multi-state payroll, next-day direct deposit and time tracking sit on different plans at each vendor; our <a href="{_py_cat}">payroll shortlist</a> shows where each one starts.</p>
{(f"<p>Not in the table because they don't publish a full price:</p><ul>{_py_unpub_li}</ul>") if _py_unpub else ""}"""),
        ("tiers", "Higher plans and add-ons", f"""<p>The entry plan is often not where a growing team stays. Monthly prices for the higher tiers that Gusto and QuickBooks publish:</p>
<div class="table-wrap"><table><thead><tr><th>Plan</th><th>Base + per person</th><th>10 employees per month</th><th>10 employees per year</th></tr></thead><tbody>{_py_tier_rows}</tbody></table></div>
<p>Our <a href="/compare/gusto-vs-quickbooks-payroll/">Gusto vs QuickBooks Payroll</a> comparison matches these tiers feature by feature. Other costs to price in:</p>
<ul>{_pa_txt}{_op_txt}
<li><b>Faster direct deposit.</b> {_py_choose.get("Decide how fast you need to pay people.", "Next-day and same-day direct deposit often sit on higher plans.")}</li>
{f"<li><b>Contractors.</b> {"; ".join(_py_contr)}.</li>" if _py_contr else ""}
<li><b>Benefits and insurance.</b> Health insurance, retirement plans and workers' compensation are usually separate products or add-ons, priced on top of payroll.</li></ul>"""),
        ("budget", "How to budget for payroll software", f"""<ol><li><b>Count everyone you pay</b>, employees and contractors, and the states they work in.</li>
<li><b>Find the cheapest plan on each provider that covers your must-haves,</b> such as multi-state payroll, next-day deposit or time tracking, then multiply its per-person fee by your headcount and add the base fee.</li>
<li><b>Add the add-ons you'll switch on</b>, such as HR tools, time tracking or extra states, and multiply by 12.</li>
<li><b>{"Look past introductory offers." if "Look past introductory offers." in _py_choose else "Price the regular rate."}</b> {_py_choose.get("Look past introductory offers.", "Compare regular prices, not introductory discounts.")}</li>
<li><b>Run a test payroll</b> before your next pay date, and check how it posts to your accounting software.</li></ol>
<p>Our <a href="{_py_cat}">payroll shortlist</a> scores each provider on six weighted criteria. Read the reviews of {_py_and([x for x in (_py_rev("gusto", "gusto"), _py_rev("rippling", "rippling"), _py_rev("square_payroll", "square-payroll"), _py_rev("patriot", "patriot-payroll"), _py_rev("quickbooks_payroll", "quickbooks-payroll")) if x])}, or see <a href="/tools/best-gusto-alternatives/">Gusto alternatives</a> if multi-state pay or per-person fees are pushing you off Gusto. Need employee records and time off too? See our <a href="/tools/best-hris-software/">HRIS shortlist</a>.</p>"""),
    ],
    "faqs": [
        ("How much does payroll software cost per employee?", f"Among the providers we rank that publish prices, full-service payroll costs {_fmt(_py_pers[0])} to {_fmt(_py_pers[-1])} per employee per month on the entry plan, plus a monthly base fee of {_fmt(_py_bases[0])} to {_fmt(_py_bases[-1])}."),
        ("How much does payroll software cost for 10 employees?", _py_faq.get("How much does payroll software cost?", f"{_fmt(_py_lo[0])} to {_fmt(_py_hi[0])} a month on entry plans.")),
        ("What is the cheapest payroll software?", _py_faq.get("What is the cheapest payroll software?", f"{_py_lo[1]} has the lowest entry cost for 10 employees.")),
        ("Does ADP publish payroll prices?", _py_faq.get("Does ADP publish RUN prices?", "No; ADP prices by quote.")),
    ],
})


# ---------- What is conversation intelligence software?
_ci = CI["tools"]
_ci_ranked = CI["_ranked"]
_ci_cat = "/tools/best-conversation-intelligence-software/"
_ci_faq = dict(CI["faqs"])
_ci_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_ci_rv = lambda k: (f'<a href="{REVIEW_URL[_ci[k]["name"]]}">{_ci[k]["name"]}</a>' if _ci[k]["name"] in REVIEW_URL else _ci[k]["name"])
_ci_by = lambda *ks: _ci_and([_ci_rv(k) for k in ks if k in _ci_ranked]) if any(k in _ci_ranked for k in ks) else ""
_ci_rows = [(f'<a href="{_ci_cat}#{k}">{_ci[k]["name"]}</a>', _ci[k]["price"], _ci[k]["price_note"], _ci[k]["trial"]) for k in _ci_ranked]
_ci_quote = [_ci[k]["name"] for k in _ci_ranked if not _money(_ci[k]["price"])]
_ci_free = [_ci[k]["name"] for k in _ci_ranked if re.search(r"free plan", _ci[k]["trial"], re.I)]
_ci_feats = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in EXPLAIN["best-conversation-intelligence-software"]["features"])
_ci_others = [n for n, _d in CI.get("others", [])]
# Per-seat price of the plan that includes conversation intelligence, read from the category text
_av = _ci.get("avoma", {})
_av_base = _money(_av.get("price", "")) if _av else None
_av_ci = re.search(r"Conversation Intelligence add-on \$([\d.]+)", _av.get("price_note", ""))
_av_ri = re.search(r"Revenue Intelligence add-ons \(\$([\d.]+) per seat per month each", _av.get("what", ""))
_ff = _ci.get("fireflies", {})
_ff_pro = re.search(r"Pro from \$([\d.]+)", _ff.get("price_note", ""))
_ci_plans = []  # (tool, plan label, per-seat monthly price)
for k in _ci_ranked:
    v = _money(_ci[k]["price"])
    if not v:
        continue
    if k == "avoma" and _av_ci:
        _ci_plans.append((_ci[k]["name"], "Startup, notes and CRM sync only", v))
        _ci_plans.append((_ci[k]["name"], "Startup + Conversation Intelligence add-on", v + float(_av_ci.group(1))))
        if _av_ri:
            _ci_plans.append((_ci[k]["name"], "Startup + Conversation and Revenue Intelligence add-ons", v + float(_av_ci.group(1)) + float(_av_ri.group(1))))
    else:
        _ci_plans.append((_ci[k]["name"], _ci[k]["price_note"].split(";")[0].split(",")[0], v))
_ci_ex = "".join(f"<tr><td>{n}</td><td>{p}</td><td>{_fmt(v)}</td><td>{_fmt(v * 10 * 12)}</td></tr>" for n, p, v in _ci_plans)
_ci_full = sorted((v, n) for n, p, v in _ci_plans if "notes and CRM sync only" not in p)  # plans that include CI-type features
_ci_lo, _ci_hi = _ci_full[0], _ci_full[-1]
_ci_av_txt = (f"Avoma's Startup plan is {_fmt(_av_base)} per recording seat, but AI call scoring and coaching come with its Conversation Intelligence add-on at {_fmt(float(_av_ci.group(1)))} more, so a seat with coaching costs {_fmt(_av_base + float(_av_ci.group(1)))}"
              + (f", or {_fmt(_av_base + float(_av_ci.group(1)) + float(_av_ri.group(1)))} with Revenue Intelligence for deal risk and forecasting" if _av_ri else "") + ".") if _av_base and _av_ci else ""
_ci_ff_txt = (f"Fireflies.ai's Pro plan starts at {_fmt(float(_ff_pro.group(1)))}, but conversation intelligence starts on Business at {_fmt(_money(_ff['price']))} per seat per month." if _ff_pro and _ff else "")

guide_page({
    "slug": "what-is-conversation-intelligence", "crumb": "What is conversation intelligence?", "dept": "Sales", "cats": ["best-conversation-intelligence-software"],
    "date": "2026-11-05", "kicker": "Explainer",
    "title": "What Is Conversation Intelligence Software? Features and Cost",
    "seo_title": "What Is Conversation Intelligence? Features and Cost | Vettlo",
    "desc": "Conversation intelligence explained: what it does with sales calls, how it differs from AI notetakers, the main types and what the tools we rank cost.",
    "card": "What it does with sales calls, how it differs from notetakers, and what it costs.",
    "answer": ("Conversation intelligence software records and transcribes sales calls and video meetings, then analyzes them to coach reps, flag deal risks and write notes back to the CRM. "
               "Unlike a plain AI notetaker, it adds call scoring, coaching workflows and reporting across the whole team. "
               f"Among the tools we rank, plans that include these features start at {_fmt(_ci_lo[0])} per seat per month ({_ci_lo[1]})"
               + (f", while {_ci_and(_ci_quote)} {'sells' if len(_ci_quote) == 1 else 'sell'} by quote." if _ci_quote else ".")),
    "sections": [
        ("does", "What conversation intelligence software does", f"""<p>The tool joins your calls and video meetings as a recorder, or connects to your phone system, and works in three steps: it captures the conversation, transcribes it with speaker labels, then analyzes what was said. Around that, platforms add:</p>
<ul>{_ci_feats}</ul>
<p>Reps use it to skip note-taking and follow-up admin. Sales managers use it to coach without sitting in on calls: they review scored calls, jump to key moments such as pricing or objections, and see patterns across the team, such as which reps talk too much or which competitors come up most.</p>"""),
        ("vs", "Conversation intelligence vs AI notetakers", f"""<p>The line between the two has blurred, because many notetakers now sell a sales plan. The useful difference is who the output is for:</p>
<ul><li><b>An AI notetaker</b> records, transcribes and summarizes meetings for the people in them. It's a personal productivity tool, and it works the same for a sales call, a stand-up or an interview.</li>
<li><b>Conversation intelligence</b> treats calls as team data. It adds call scoring and scorecards, coaching workflows for managers, analytics across reps, deal risk signals and structured CRM updates.</li></ul>
<p>The practical effect is on price: the sales features usually sit on a higher plan or a paid add-on. {_ci_ff_txt} {_ci_av_txt}{(" " + _ci["otter"]["what"].split(". ", 1)[-1].replace("Its ", "Otter.ai's ", 1)) if "otter" in _ci else ""} Sales dialers also record and transcribe calls; if your team mostly calls by phone, compare with our <a href="/tools/best-sales-dialers/">sales dialer shortlist</a>.</p>"""),
        ("types", "The main types of conversation intelligence tool", f"""<ul>{f"<li><b>Enterprise revenue platforms</b> put coaching, deal inspection and forecasting on the same conversation data, sold by annual contract to sales orgs with a RevOps team. {_ci_by('gong')} is the best-known example.</li>" if _ci_by('gong') else ""}
{f"<li><b>Meeting assistants with conversation intelligence add-ons</b> publish prices and let you buy only the modules you need, such as call scoring or deal risk. {_ci_by('avoma')} works this way.</li>" if _ci_by('avoma') else ""}
{f"<li><b>AI sales assistants</b> focus on the admin after a call: summaries, follow-up emails and CRM field updates for individual reps, with lighter team coaching. {_ci_by('sybill')} sits here.</li>" if _ci_by('sybill') else ""}
{f"<li><b>Notetakers with a sales tier</b> start as general meeting recorders and add conversation intelligence and team analytics on a business plan, at the lowest prices in the category. {_ci_by('fireflies')} is one.</li>" if _ci_by('fireflies') else ""}</ul>
{f"<p>Other tools in the category include {_ci_and(_ci_others)}. " if _ci_others else "<p>"}Our <a href="{_ci_cat}">shortlist</a> scores the ranked tools on recording, coaching, deal insights, CRM integration, ease of use and price.</p>"""),
        ("cost", "How much conversation intelligence software costs", f"""<p>Most tools charge per recording seat per month, and enterprise vendors quote. Entry plans for the tools we rank, from each vendor's pricing page:</p>
{_ptable(_ci_rows)}
<p class="small muted">{CI['price_footnote']}</p>
<p>Ten recording seats for a year at the published per-seat prices, before taxes and other add-ons:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Plan</th><th>Per seat per month</th><th>10 seats per year</th></tr></thead><tbody>{_ci_ex}</tbody></table></div>
<p>{(_ci_faq.get("How much does Gong cost?", "") + " ") if "gong" in _ci_ranked else ""}Compare what each plan includes, not only the total: our <a href="/compare/gong-vs-avoma/">Gong vs Avoma</a> comparison prices 10 seats at each feature level, and seat rules differ, since Avoma charges only for people who record while viewers are free.</p>"""),
        ("choose", "How to choose a conversation intelligence tool", "<ol>" + "".join(f"<li><b>{a}</b> {b}</li>" for a, b in CI["choose"]) + f"""</ol>
<p>Our <a href="{_ci_cat}">conversation intelligence shortlist</a> ranks {len(_ci_ranked)} tools, and <a href="/tools/best-gong-alternatives/">Gong alternatives</a> covers options with published pricing. New to outbound tooling? See <a href="/guides/what-is-sales-engagement-software/">what sales engagement software is</a>.</p>"""),
    ],
    "faqs": [
        ("What is conversation intelligence software?", _ci_faq.get("What is conversation intelligence software?", "It records, transcribes and analyzes sales calls for coaching, deal insights and CRM updates.")),
        ("What is the difference between conversation intelligence and an AI notetaker?", "A notetaker records and summarizes meetings for the people in them. Conversation intelligence treats calls as team data: it scores calls, supports manager coaching, reports across reps and flags deal risks. Many notetakers sell these features on a higher plan."),
        ("How much does conversation intelligence software cost?", f"Among the tools we rank, plans that include conversation intelligence features cost {_fmt(_ci_lo[0])} ({_ci_lo[1]}) to {_fmt(_ci_hi[0])} ({_ci_hi[1]}) per seat per month at published prices, or {_fmt(_ci_lo[0] * 120)} to {_fmt(_ci_hi[0] * 120)} a year for 10 seats." + (f" {_ci_and(_ci_quote)} {'doesn' if len(_ci_quote) == 1 else 'don'}'t publish prices." if _ci_quote else "")),
        ("Is there a free conversation intelligence tool?", _ci_faq.get("Is there a free conversation intelligence tool?", "Some tools have free plans with limits; coaching usually needs a paid plan.")),
    ],
})


# ---------- How much does a business password manager cost?
_pw = PWM["tools"]
_pw_ranked = PWM["_ranked"]
_pw_cat = "/tools/best-password-managers-for-business/"
_pw_faq = dict(PWM["faqs"])
_pw_choose = dict(PWM["choose"])
_pw_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_pw_rv = lambda k: f'<a href="/tools/{_tslug(_pw[k]["name"])}-review/">{_pw[k]["name"]}</a>'
_pw_rows = [(f'<a href="{_pw_cat}#{k}">{_pw[k]["name"]}</a>', _pw[k]["price"], _pw[k]["price_note"], _pw[k]["trial"]) for k in _pw_ranked]


def _pw_limits(note):
    """(min users, max users) for the entry plan, read from its price note; None where no limit is stated."""
    first = note.split(";")[0]
    m = re.search(r"(\d+)[–-](\d+) users", first)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"under (\d+) users", first)
    return (None, int(m.group(1)) - 1) if m else (None, None)


_pw_entry = []  # (per-user price, name, key, (min, max))
for k in _pw_ranked:
    v = _money(_pw[k]["price"])
    if v:
        _pw_entry.append((v, _pw[k]["name"], k, _pw_limits(_pw[k]["price_note"])))
_pw_entry.sort()
_pw_sizes = (10, 25, 50)


def _pw_cell(v, lim, n):
    lo, hi = lim
    if (lo and n < lo) or (hi and n > hi):
        return '<span class="muted">Not offered at this size</span>'
    return _fmt(v * n * 12)


_pw_ex = "".join(f"<tr><td>{n}</td><td>{_fmt(v)}</td>" + "".join(f"<td>{_pw_cell(v, lim, s)}</td>" for s in _pw_sizes) + "</tr>" for v, n, k, lim in _pw_entry)
_pw_pn = lambda n, plan: n + " " + " ".join(w for i, w in enumerate(plan.split()) if not (i == 0 and w in n.split()))
_pw_lim_txt = [f"{_pw_pn(n, re.match(r'([^,;]+?)(?:,| billed|;|$)', _pw[k]['price_note']).group(1).strip())} is for {re.search(r'[0-9]+[–-][0-9]+ users|under [0-9]+ users', _pw[k]['price_note'].split(';')[0]).group(0)}" for v, n, k, lim in _pw_entry if lim != (None, None)]
_pw_lo, _pw_hi = _pw_entry[0], _pw_entry[-1]
_pw_quote = [_pw[k]["name"] for k in _pw_ranked if not _money(_pw[k]["price"])]

# Other published plans, read from each tool's price note: (tool, plan, per-user/month, flat monthly fee, (min, max) users)
_pw_tiers = []
for k in _pw_ranked:
    for seg in _pw[k]["price_note"].split("; ")[1:]:
        m = re.match(r"(.+?) \$([\d.]+)(/user|/mo)?", seg)
        if not m:
            continue
        cap = re.search(r"up to (\d+) users", seg)
        lim = (None, int(cap.group(1))) if cap else _pw_limits(seg)
        flat = m.group(3) == "/mo"
        _pw_tiers.append((_pw[k]["name"], m.group(1), None if flat else float(m.group(2)), float(m.group(2)) if flat else None, lim))
_pw_plan = lambda k: re.match(r"([^,;]+?)(?:,| billed|;|$)", _pw[k]["price_note"]).group(1).strip()
_pw_limtxt = lambda seg: (lambda m: m.group(0) if m else "")(re.search(r"\d+[–-]\d+ users|under \d+ users|up to \d+ users", seg))
_pw_tier_rows = ""
for n, plan, per, flat, lim in _pw_tiers:
    if per:
        _pw_tier_rows += f"<tr><td>{n}</td><td>{plan}</td><td>{_fmt(per)} per user</td><td>{_pw_cell(per, lim, 10)}</td><td>{_pw_cell(per, lim, 50)}</td></tr>"
    else:
        _pw_tier_rows += f'<tr><td>{n}</td><td>{plan}</td><td>{_fmt(flat)} a month{f" for up to {lim[1]} users" if lim[1] else ""}</td><td>{_fmt(flat * 12)}</td><td>{_pw_cell(flat / 50, lim, 50) if lim[1] else _fmt(flat * 12)}</td></tr>'
_pw_flat = next(((n, plan, flat, lim[1]) for n, plan, per, flat, lim in _pw_tiers if flat), None)
_pw_num = lambda c: {2: "two", 3: "three", 4: "four", 5: "five"}.get(c, str(c))
_pw_free_org = [(_pw[k]["name"], int(m.group(1))) for k in _pw_ranked if (m := re.search(r"free (\d+)-(?:person|user) org", _pw[k]["trial"] + " " + _pw[k]["trial_short"], re.I))]
_pw_ent_quote = [_pw[k]["name"] for k in _pw_ranked if re.search(r"Enterprise (custom|quoted|pricing is by quote|, now quoted)", _pw[k]["price_note"] + " " + _pw[k]["what"] + " " + " ".join(_pw[k]["cons"]))]

guide_page({
    "slug": "password-manager-cost-for-business", "crumb": "Password manager cost", "dept": "IT & security", "cats": ["best-password-managers-for-business"],
    "date": "2026-11-06", "kicker": "Pricing guide",
    "title": f"How Much Does a Business Password Manager Cost in {YEAR}?",
    "seo_title": "How Much Does a Business Password Manager Cost? | Vettlo",
    "desc": "Business password manager prices per user, what 10, 25 and 50 users pay a year, what SSO plans cost, small-team packs and the limits to check.",
    "card": "Per-user prices, yearly cost for 10, 25 and 50 users, and what SSO adds.",
    "answer": (f"Business password managers charge per user per month, billed annually. Among the tools we rank, entry plans cost {_fmt(_pw_lo[0])} ({_pw_lo[1]}) to {_fmt(_pw_hi[0])} ({_pw_hi[1]}) per user, "
               f"or {_fmt(_pw_lo[0] * 120)} to {_fmt(_pw_hi[0] * 120)} a year for 10 users. "
               f"Single sign-on usually needs a higher plan: {_pw_choose.get('Price the plan with SSO, not the entry plan.', '').split('. ')[0]}."),
    "sections": [
        ("model", "How business password managers are priced", f"""<p>Every password manager we rank uses the same basic model: a <b>price per user per month</b>, with the headline price assuming you pay for a year up front. What changes between vendors is which plan unlocks the features IT asks for.</p>
<ul><li><b>Plan ladders.</b> Most vendors sell two or three business plans. The entry plan covers vaults, sharing and an admin console; higher plans add single sign-on (SSO), automatic provisioning from your identity provider (SCIM), advanced policies and reporting.</li>
<li><b>User limits.</b> Some plans only apply to a certain team size. {_pw_and(_pw_lim_txt) + "; outside those limits you move to another plan." if _pw_lim_txt else "Check each plan's minimum and maximum seats."}</li>
{f"<li><b>Flat small-team packs.</b> {_pw_flat[0]} also sells {_pw_flat[1]} for {_fmt(_pw_flat[2])} a month for up to {_pw_flat[3]} users, a fixed fee rather than a per-user price.</li>" if _pw_flat and _pw_flat[3] else ""}
<li><b>Quotes at the top.</b> {f"{_pw_and(_pw_ent_quote)} price their enterprise plans by quote." if _pw_ent_quote else "Enterprise plans are often priced by quote."} {f"{_pw_and(_pw_quote)} {'has' if len(_pw_quote) == 1 else 'have'} no published entry price." if _pw_quote else ""}</li>
<li><b>Free tiers.</b> {" ".join(f"{n}'s free organization lets {_pw_num(c)} people share passwords without paying." for n, c in _pw_free_org) + " Beyond that, business features need a paid plan." if _pw_free_org else "Business features need a paid plan; vendors offer free trials instead."}</li></ul>"""),
        ("prices", "Entry prices by password manager", f"""<p>The cheapest business plan for each password manager in our ranking, from each vendor's pricing pages:</p>
{_ptable(_pw_rows, ("Password manager", "Entry price", "Plans and billing", "Free plan / trial"))}
<p class="small muted">{PWM['price_footnote']}</p>"""),
        ("example", "What 10, 25 and 50 users cost per year", f"""<p>Yearly cost on each entry plan at the published per-user price, billed annually, before taxes and add-ons. Where a plan has a user limit, sizes outside it are marked:</p>
<div class="table-wrap"><table><thead><tr><th>Password manager</th><th>Per user per month</th>{''.join(f'<th>{s} users per year</th>' for s in _pw_sizes)}</tr></thead><tbody>{_pw_ex}</tbody></table></div>
<p>Entry plans don't include the same things, so the cheapest line isn't always the cheapest fit. {_pw_choose.get("Check where provisioning starts.", "")}</p>"""),
        ("tiers", "What SSO plans and small-team packs cost", f"""<p>The plan your security team needs is often a step up from the entry plan, and very small teams can sometimes pay less. Other plans each vendor publishes, from the same pricing pages:</p>
<div class="table-wrap"><table><thead><tr><th>Password manager</th><th>Plan</th><th>Price</th><th>10 users per year</th><th>50 users per year</th></tr></thead><tbody>{_pw_tier_rows}</tbody></table></div>
<p><b>Where SSO starts.</b> {_pw_choose.get("Price the plan with SSO, not the entry plan.", "")}</p>
<p><b>Small teams.</b> {_pw_choose.get("Price small-team plans separately.", "")}</p>
<p>Our <a href="/compare/1password-vs-bitwarden/">1Password vs Bitwarden</a> comparison matches two of these ladders plan by plan.</p>"""),
        ("budget", "How to budget for a business password manager", f"""<ol><li><b>Count seats, not just employees.</b> Include contractors and anyone who needs shared logins, and check the plan's user minimum or maximum.</li>
<li><b>Decide whether you need SSO and SCIM now.</b> If your company already uses an identity provider such as Okta or Microsoft Entra ID, price the plan that connects to it, since that is usually the one you end up on.</li>
<li><b>{"Ask about add-ons before you sign." if "Ask about add-ons before you sign." in _pw_choose else "Price the add-ons."}</b> {_pw_choose.get("Ask about add-ons before you sign.", "Some reporting and developer features are sold separately.")}</li>
<li><b>Count the family accounts.</b> {_pw_choose.get("Look at what staff get at home.", "")}</li>
<li><b>Multiply by 12.</b> Headline prices assume annual billing, so the first invoice is a full year.</li></ol>
<p>Our <a href="{_pw_cat}">password manager shortlist</a> scores {len(_pw_ranked)} tools on six weighted criteria. Read the reviews of {_pw_and([_pw_rv(k) for k in _pw_ranked])}, or see <a href="/tools/best-lastpass-alternatives/">LastPass alternatives</a> if you're moving off LastPass.</p>"""),
    ],
    "faqs": [
        ("How much does a business password manager cost?", _pw_faq.get("How much does a business password manager cost?", f"{_fmt(_pw_lo[0])} to {_fmt(_pw_hi[0])} per user per month on entry plans.")),
        ("Which business password manager includes SSO for the lowest price?", _pw_faq.get("Which business password manager includes SSO for the lowest price?", "")),
        ("What is the cheapest business password manager?", f"{_pw_lo[1]} has the lowest entry price we found, {_fmt(_pw_lo[0])} per user per month billed annually on {_pw_plan(_pw_lo[2])}{f" ({_pw_limtxt(_pw[_pw_lo[2]]['price_note'].split(';')[0])})" if _pw_limtxt(_pw[_pw_lo[2]]['price_note'].split(';')[0]) else ""}, or {_fmt(_pw_lo[0] * 120)} a year for 10 users. It doesn't include SSO on that plan."),
        ("Is there a free password manager for business?", (" ".join(f"{n} has a free organization for {_pw_num(c)} people that can share passwords." for n, c in _pw_free_org) + f" {'It is the only free business option' if len(_pw_free_org) == 1 else 'These are the only free business options'} among the tools we rank; for more people or admin features you need a paid plan, and the others offer free trials." if _pw_free_org else "Not among the tools we rank; they offer free trials instead.")),
    ],
})


# ---------- How much does accounting software cost?
_ac = ACC["tools"]
_ac_ranked = ACC["_ranked"]
_ac_cat = "/tools/best-accounting-software/"
_ac_faq = dict(ACC["faqs"])
_ac_choose = dict(ACC["choose"])
_ac_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_ac_rv = lambda k: f'<a href="/tools/{_tslug(_ac[k]["name"])}-review/">{_ac[k]["short"]}</a>'
_ac_rows = [(f'<a href="{_ac_cat}#{k}">{_ac[k]["name"]}</a>', _ac[k]["price"], _ac[k]["price_note"], _ac[k]["trial"]) for k in _ac_ranked]
_ac_usd = sorted((_money(_ac[k]["price"]), _ac[k]["name"], k) for k in _ac_ranked if _money(_ac[k]["price"]))
_ac_lo, _ac_hi = _ac_usd[0], _ac_usd[-1]
_ac_quote = [_ac[k]["name"] for k in _ac_ranked if not _money(_ac[k]["price"])]
_ac_free = [_ac[k]["name"] for k in _ac_ranked if re.search(r"free (plan|starter)", _ac[k]["trial"], re.I)]
_ac_annual = [_ac[k]["name"] for k in _ac_ranked if "billed annually" in _ac[k]["price_note"]]

# Full plan ladders from the vendor pricing detail kept for review pages (data/review_depth.json),
# used only where its entry price matches the category data, so the two never disagree.
_ac_depth = json.load(open(ROOT / "data" / "review_depth.json"))
_ac_num = lambda s: float(s.replace(",", ""))


def _ac_ladder(k):
    """[(plan, regular $/mo, month-to-month $/mo or None, (promo $/mo, months) or None, users)] or []."""
    d = _ac_depth.get(_ac[k]["name"]) if k in _ac else None
    if not d:
        return []
    users = {}
    lim = d.get("limits", {})
    for r in lim.get("rows", []):
        if r[0] == "Users":
            users = dict(zip(lim["cols"], r[1:]))
    out = []
    for plan, price, _inc in d["plans"]:
        m = re.match(r"\$([\d,.]+)/(?:org/)?mo", price)
        if not m:
            continue
        mo = re.search(r"or \$([\d,.]+) monthly", price)
        pr = re.search(r"\(\$([\d,.]+)/mo for (?:the first )?(\d+) months", price)
        out.append((plan, _ac_num(m.group(1)), _ac_num(mo.group(1)) if mo else None,
                    (_ac_num(pr.group(1)), int(pr.group(2))) if pr else None, users.get(plan, "")))
    if not out or out[0][1] != _money(_ac[k]["price"]):
        return []
    return out


_ac_lad = {k: _ac_ladder(k) for k in _ac_ranked}
_ac_lad = {k: v for k, v in _ac_lad.items() if v}
_ac_tier_rows = ""
for k, lad in _ac_lad.items():
    for plan, reg, mo, pr, us in lad:
        u = ("No per-user fees" if "per-user" in us else f"{us} user{'s' if us != '1' else ''}") if us else "Not stated"
        bill = f"{_fmt(reg)}" + (f" billed annually ({_fmt(mo)} monthly)" if mo else "")
        _ac_tier_rows += f"<tr><td>{_ac[k]['short']}</td><td>{plan}</td><td>{bill}</td><td>{u}</td><td>{_fmt(reg * 12)}</td></tr>"
# FreshBooks and Wave ladders, read from the category text
_fb = _ac.get("freshbooks", {})
_fb_tiers = re.findall(r"(Plus|Premium) \(\$([\d.]+)\) (\d+|unlimited) clients", _fb.get("what", ""))
_fb_lite = re.search(r"Lite covers (\d+) billable clients", _fb.get("what", ""))
_fb_tm = re.search(r"team members \$([\d.]+) each", _fb.get("price_note", ""))
if _fb and _money(_fb["price"]) and _fb_lite:
    _ac_tier_rows += f"<tr><td>{_fb['short']}</td><td>Lite</td><td>{_fmt(_money(_fb['price']))}</td><td>{_fb_lite.group(1)} billable clients</td><td>{_fmt(_money(_fb['price']) * 12)}</td></tr>"
    for plan, p, c in _fb_tiers:
        _ac_tier_rows += f"<tr><td>{_fb['short']}</td><td>{plan}</td><td>{_fmt(float(p))}</td><td>{'Unlimited' if c == 'unlimited' else c} billable clients</td><td>{_fmt(float(p) * 12)}</td></tr>"
_wv = _ac.get("wave", {})
_wv_yr = re.search(r"\(\$([\d,]+) a year\)", _wv.get("price_note", ""))
if _wv and _money(_wv["price"]):
    _ac_tier_rows += f"<tr><td>{_wv['short']}</td><td>Starter</td><td>Free</td><td>Not stated</td><td>$0</td></tr>"
    _ac_tier_rows += f"<tr><td>{_wv['short']}</td><td>Pro</td><td>{_fmt(_money(_wv['price']))} monthly" + (f" or {_fmt(_ac_num(_wv_yr.group(1)))} a year" if _wv_yr else "") + f"</td><td>Not stated</td><td>{_fmt(_ac_num(_wv_yr.group(1))) if _wv_yr else _fmt(_money(_wv['price']) * 12)}</td></tr>"

# Cheapest plan that includes 1, 3, 5 and 10 users, for vendors that publish user counts per plan
_ac_sizes = (1, 3, 5, 10)


def _ac_fit(lad, n):
    for plan, reg, mo, pr, us in lad:
        if "per-user" in us or (us.isdigit() and int(us) >= n):
            return plan, reg
    return None


_ac_size_rows = ""
for k, lad in _ac_lad.items():
    cells = []
    for n in _ac_sizes:
        f = _ac_fit(lad, n)
        cells.append(f'<td>{_fmt(f[1] * 12)}<br><span class="small muted">{f[0]}</span></td>' if f else '<td><span class="muted">Not listed</span></td>')
    _ac_size_rows += f"<tr><td>{_ac[k]['short']}</td>{''.join(cells)}</tr>"

# Introductory offers: first-year cost vs a full year at the regular price
_ac_promo = [(k, plan, reg, pr) for k, lad in _ac_lad.items() for plan, reg, mo, pr, us in lad if pr]
_ac_promo_rows = "".join(f"<tr><td>{_ac[k]['short']} {plan}</td><td>{_fmt(pr[0])} for {pr[1]} months, then {_fmt(reg)}</td>"
                         f"<td>{_fmt(pr[0] * pr[1] + reg * (12 - pr[1]))}</td><td>{_fmt(reg * 12)}</td></tr>" for k, plan, reg, pr in _ac_promo)
_ac_promo_pct = {}
for k, plan, reg, pr in _ac_promo:
    _ac_promo_pct.setdefault(k, (round((1 - pr[0] / reg) * 100), pr[1]))
_ac_promo_txt = _ac_and([f"{_ac[k]['short']} takes {p}% off for the first {m} months" for k, (p, m) in _ac_promo_pct.items()]) if _ac_promo_pct else ""
_ac_promo_simple = [(k, plan, reg, pr) for k, plan, reg, pr in _ac_promo if plan == _ac_lad[k][0][0]]
# Add-on and usage costs stated in the vendor notes
_ac_notes = {k: " ".join(_ac_depth[_ac[k]["name"]].get("notes", [])) for k in _ac_lad}
_xp = re.search(r"Xero Payroll, powered by Gusto: \$([\d.]+) a month \+ \$([\d.]+) per employee or contractor", _ac_notes.get("xero", ""))
_xr = next((p for f, p in _ac_depth.get("Xero", {}).get("first_plan", []) if f == "Auto-reconcile"), "") if "xero" in _ac_lad else ""
_xr = re.search(r"optional on Early for \$([\d.]+)/mo", _xr)
_qa = re.search(r"free up to a monthly allotment, then \$([\d.]+) per transaction", _ac_notes.get("quickbooks", ""))
_qp = "pricing page does not list its price" in _ac_notes.get("quickbooks", "")
_zu = re.search(r"Extra users cost \$([\d.]+) a month billed annually \(\$([\d.]+) monthly\)", _ac_notes.get("zohobooks", ""))
_ac_mo = [(_ac[k]["short"], plan, reg, mo) for k, lad in _ac_lad.items() for plan, reg, mo, pr, us in lad if mo]
_qau = {}
for _r in _ac_depth.get("QuickBooks Online", {}).get("limits", {}).get("rows", []) if "quickbooks" in _ac_lad else []:
    if _r[0] == "Accountant users":
        _qau = dict(zip(_ac_depth["QuickBooks Online"]["limits"]["cols"], _r[1:]))
_ac_extra = []
if _xp:
    _ac_extra.append(f"<li><b>Payroll.</b> Payroll is usually a separate subscription. Xero Payroll, powered by Gusto, costs {_fmt(float(_xp.group(1)))} a month plus {_fmt(float(_xp.group(2)))} per employee or contractor, or {_fmt(float(_xp.group(1)) + float(_xp.group(2)) * 10)} a month for 10 people, on top of any Xero plan."
                     + (" QuickBooks offers payroll as an add-on at checkout but doesn't list its price on the accounting pricing page." if _qp else "")
                     + ' Our <a href="/guides/payroll-software-cost/">payroll cost guide</a> compares the providers.</li>')
if _fb_tm or _zu:
    _ac_extra.append("<li><b>Extra people.</b> " + " ".join(x for x in (
        f"FreshBooks charges {_fmt(float(_fb_tm.group(1)))} a month for each team member you add." if _fb_tm else "",
        f"Zoho Books sells extra users for {_fmt(float(_zu.group(1)))} a month billed annually ({_fmt(float(_zu.group(2)))} monthly)." if _zu else "",
        "Xero has no per-user fees on any plan." if "xero" in _ac_lad else "") if x) + "</li>")
if _xr:
    _ac_extra.append(f"<li><b>Feature add-ons.</b> Xero Early can add auto-reconcile for {_fmt(float(_xr.group(1)))} a month, which brings it to {_fmt(_ac_lad['xero'][0][1] + float(_xr.group(1)))}; Growing includes it.</li>")
_ac_extra.append("<li><b>Payment and bill-pay fees.</b> "
                 + (f"Wave's free plan charges card processing fees when customers pay invoices online. " if _wv else "")
                 + (f"QuickBooks includes free standard ACH bill payments up to a monthly allotment, then charges {_fmt(float(_qa.group(1)))} per transaction. " if _qa else "")
                 + "Online card and bank payments from customers carry processing fees with most tools, so check the rates if you get paid through your invoices.</li>")
_ac_extra.append("<li><b>Your accountant or bookkeeper.</b> Most plans include free access for your accountant"
                 + (f" (QuickBooks includes {" or ".join(sorted(set(_qau.values())))} accountant users depending on the plan)" if _qau else "")
                 + ", but their fees for bookkeeping, month-end close and tax returns are a separate cost, and often a larger one than the software.</li>")
if "intacct" in _ac:
    _ac_extra.append(f'<li><b>Mid-market software.</b> {_ac["intacct"]["name"]} is {_ac["intacct"]["price_note"][0].lower() + _ac["intacct"]["price_note"][1:]}, and it needs implementation, so expect a quote that covers both. See our <a href="/tools/{_tslug(_ac["intacct"]["name"])}-review/">Sage Intacct review</a>.</li>')

guide_page({
    "slug": "accounting-software-cost", "crumb": "Accounting software cost", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-07", "kicker": "Pricing guide",
    "title": f"How Much Does Accounting Software Cost in {YEAR}?",
    "seo_title": f"How Much Does Accounting Software Cost? ({YEAR} Prices) | Vettlo",
    "desc": "Accounting software prices at regular rates: entry plans, every tier, cost for 1 to 10 users, what intro discounts save and the add-ons to budget for.",
    "card": "Regular prices, cost by team size, intro discounts and the add-ons.",
    "answer": (f"Small business accounting software costs {_fmt(_ac_lo[0])} ({_ac_lo[1]}) to {_fmt(_ac_hi[0])} ({_ac_hi[1]}) a month at regular prices for the entry plan among the tools we rank, "
               f"or {_fmt(_ac_lo[0] * 12)} to {_fmt(_ac_hi[0] * 12)} a year. It's priced per business, not per user, but plans cap users, invoices or clients, "
               "so growing teams often pay for a mid-tier plan"
               + (f", and {_ac_and(_ac_free)} {'has' if len(_ac_free) == 1 else 'have'} free plans" if _ac_free else "")
               + ". Introductory discounts cut the first few months, not the price you'll pay after that."),
    "sections": [
        ("model", "How accounting software is priced", f"""<p>Small business accounting tools charge a <b>flat monthly fee for your business</b> (the company file or organization), not a fee per employee. What decides your price is which plan you need, and plans are gated in a few ways:</p>
<ul><li><b>Users.</b> Some plans include a fixed number of people who can log in. QuickBooks Online steps up by users, while Xero has no per-user fees on any plan.</li>
<li><b>Volume.</b> Entry plans may cap invoices and bills (Xero Early) or billable clients (FreshBooks Lite), and Zoho Books caps invoices, bills and records per year on every plan.</li>
<li><b>Features.</b> {_ac_choose.get("Plan for inventory, projects and currencies.", "Inventory, projects and multi-currency usually start on mid-tier plans.")}</li>
<li><b>Introductory offers.</b> {_ac_choose.get("Compare regular prices, not promotions.", "")}</li>
<li><b>Billing period.</b> {f"{_ac_and(_ac_annual)} quotes {'its' if len(_ac_annual) == 1 else 'their'} headline price billed annually and charges more month to month; " if _ac_annual else ""}QuickBooks and Xero list monthly prices.</li></ul>
<p>Mid-market financial software such as {_ac_and(_ac_quote) if _ac_quote else "Sage Intacct"} works differently: it's sold by module and priced by quote, usually with an implementation project.</p>"""),
        ("prices", "Entry prices by tool", f"""<p>The cheapest paid plan for each accounting tool in our ranking, at the regular price:</p>
{_ptable(_ac_rows)}
<p class="small muted">{ACC['price_footnote']}</p>"""),
        ("tiers", "Every plan and what it costs per year", f"""<p>The entry plan rarely fits for long once a second person needs access or you start tracking inventory. Every published plan, at the regular price from each vendor's pricing page:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Plan</th><th>Regular price per month</th><th>Users or limit</th><th>Per year</th></tr></thead><tbody>{_ac_tier_rows}</tbody></table></div>
<p>Where the plan you need starts depends on the feature: inventory starts on QuickBooks Plus and Zoho Books Professional, multi-currency and projects on Xero Established, and project profitability on FreshBooks Premium. Our <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> comparison matches the two ladders plan by plan.</p>
<h3>Cost by number of users</h3>
<p>The cheapest plan that includes 1, 3, 5 and 10 users, per year at the regular price{f" (Zoho Books billed annually)" if "zohobooks" in _ac_lad else ""}:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th>{''.join(f'<th>{n} user{"s" if n > 1 else ""}</th>' for n in _ac_sizes)}</tr></thead><tbody>{_ac_size_rows}</tbody></table></div>
<p>{"Xero's price doesn't change with users, but Early's caps of 20 invoices and 5 bills a month can push a busier business to Growing. " if "xero" in _ac_lad else ""}{f"Zoho Books can also add users to a plan for {_fmt(float(_zu.group(1)))} each a month instead of moving up a tier. " if _zu else ""}{f"FreshBooks adds {_fmt(float(_fb_tm.group(1)))} a month per team member, and Wave doesn't list user limits." if _fb_tm else ""}</p>"""),
        ("promos", "Introductory discounts and other costs", f"""<p>{_ac_promo_txt + " for new customers. " if _ac_promo_txt else ""}That makes the first year cheaper, but the regular price applies once the offer ends. First year on the promotion compared with a full year at the regular price:</p>
<div class="table-wrap"><table><thead><tr><th>Plan</th><th>Offer</th><th>First year with offer</th><th>Each year after</th></tr></thead><tbody>{_ac_promo_rows}</tbody></table></div>
<p class="small muted">{"QuickBooks offers new customers either its 30-day free trial or the discount, not both. " if "alternative offer" in _ac_notes.get("quickbooks", "") else ""}Offers change often; check the vendor's page on the day you sign up.</p>
<p>Beyond the plan itself, budget for:</p>
<ul>{''.join(_ac_extra)}</ul>"""),
        ("budget", "How to budget for accounting software", f"""<ol><li><b>Count the people who need access</b>, including a bookkeeper, and the invoices and bills you handle each month. Those set your plan.</li>
<li><b>List the features you'll need within a year,</b> such as inventory, projects, multi-currency or bill approvals, and find the first plan on each tool that includes them.</li>
<li><b>Multiply the regular price by 12,</b> then add payroll, extra users and any add-ons.</li>
<li><b>{"Ask your accountant." if "Ask your accountant." in _ac_choose else "Talk to your accountant."}</b> {_ac_choose.get("Ask your accountant.", "Use the tool your accountant already knows.")}</li>
<li><b>{"Make sure your bank connects." if "Make sure your bank connects." in _ac_choose else "Check bank feeds."}</b> {_ac_choose.get("Make sure your bank connects.", "Check that your bank is supported before you migrate.")}</li></ol>
<p>Our <a href="{_ac_cat}">accounting software shortlist</a> scores {len(_ac_ranked)} tools on six weighted criteria. Read the reviews of {_ac_and([_ac_rv(k) for k in _ac_ranked])}, or see <a href="/tools/best-quickbooks-alternatives/">QuickBooks alternatives</a> if its regular price or user limits are the problem. Tracking receipts and company cards too? See our <a href="/tools/best-expense-management-software/">expense management shortlist</a>.</p>"""),
    ],
    "faqs": [
        ("How much does accounting software cost per month?", f"Entry plans for the accounting tools we rank cost {_fmt(_ac_lo[0])} to {_fmt(_ac_hi[0])} a month at regular prices. Plans with more users, inventory or projects cost more; for example, "
         + _ac_and([f"{_ac[k]['short']} {lad[-1][0]} is {_fmt(lad[-1][1])}" for k, lad in _ac_lad.items()]) + " a month." if _ac_lad else f"Entry plans cost {_fmt(_ac_lo[0])} to {_fmt(_ac_hi[0])} a month at regular prices."),
        ("How much does QuickBooks Online cost?", _ac_faq.get("How much does QuickBooks Online cost?", "See our shortlist for current QuickBooks prices.")),
        ("Is Xero cheaper than QuickBooks?", _ac_faq.get("Is Xero cheaper than QuickBooks?", "See our QuickBooks vs Xero comparison.")),
        ("Is there free accounting software?", _ac_faq.get("What is the best free accounting software?", "Some tools have free plans; see our shortlist.")),
    ],
})


# ---------- What is an HRIS?
_hr = HRIS["tools"]
_hr_ranked = HRIS["_ranked"]
_hr_cat = "/tools/best-hris-software/"
_hr_faq = dict(HRIS["faqs"])
_hr_choose = dict(HRIS["choose"])
_hr_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_hr_rv = lambda k: (f'<a href="{REVIEW_URL[_hr[k]["name"]]}">{_hr[k]["name"]}</a>' if _hr[k]["name"] in REVIEW_URL else _hr[k]["name"])
_hr_by = lambda *ks: _hr_and([_hr_rv(k) for k in ks if k in _hr_ranked]) if any(k in _hr_ranked for k in ks) else ""
_hr_rows = [(f'<a href="{_hr_cat}#{k}">{_hr[k]["name"]}</a>', _hr[k]["price"], _hr[k]["price_note"], _hr[k]["trial"]) for k in _hr_ranked]
_hr_quote = [_hr[k]["name"] for k in _hr_ranked if not _money(_hr[k]["price"])]
_hr_free = [_hr[k]["name"] for k in _hr_ranked if re.search(r"free plan", _hr[k]["trial"], re.I)]
_hr_feats = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in EXPLAIN["best-hris-software"]["features"])


def _hr_cost(k, n):
    """Monthly cost of a tool's published entry plan for n employees, read from its price strings; None if not published or n is outside the plan."""
    p, note = _hr[k]["price"], _hr[k]["price_note"]
    v = _money(p)
    if not v:
        return None
    if re.search(r"/(employee|user)/", p):
        cap = re.search(r"up to (\d+) employees", note)
        if cap and n > int(cap.group(1)):
            return None
        mn = re.search(r"from (\d+) users", note)
        return v * max(n, int(mn.group(1)) if mn else n)
    flat = re.search(r"for (\d+) users", p) or re.search(r"up to (\d+) employees", note)
    return v if flat and n <= int(flat.group(1)) else None


_hr_sizes = (10, 20)
_hr_unit = lambda k: ("Per employee" if "/employee/" in _hr[k]["price"] else "Per user" if "/user/" in _hr[k]["price"]
                      else "Flat fee for a headcount band" if _money(_hr[k]["price"]) else "Quote")
_hr_plan = lambda k: (lambda l: "Entry paid plan" if l.startswith("Paid plans") else l)(_hr[k]["price_note"].split(";")[0].split(",")[0])
_hr_cost_rows = "".join(f'<tr><td>{_hr[k]["name"]}</td><td>{_hr_plan(k)}</td><td>{_hr_unit(k)}</td>'
                        + "".join(f"<td>{_fmt(_hr_cost(k, n)) if _hr_cost(k, n) is not None else 'Quote'}</td>" for n in _hr_sizes) + "</tr>"
                        for k in _hr_ranked if _money(_hr[k]["price"]))
_hr_20 = sorted((_hr_cost(k, 20), _hr[k]["name"], k) for k in _hr_ranked if _hr_cost(k, 20) is not None)
_hr_lo, _hr_hi = _hr_20[0], _hr_20[-1]
_hr_yr = lambda k: ", billed yearly" if "billed yearly" in _hr[k]["price_note"] else ""
_hr_lo_n, _hr_hi_n = _hr_lo[1] + _hr_yr(_hr_lo[2]), _hr_hi[1] + _hr_yr(_hr_hi[2])
_hr_mod = [_hr[k]["name"] for k in _hr_ranked if "module" in _hr[k]["price_note"].lower() and _money(_hr[k]["price"])]
_ats_faq = dict(ATS["faqs"]) if "ATS" in globals() else {}

guide_page({
    "slug": "what-is-an-hris", "crumb": "What is an HRIS?", "dept": "HR & people", "cats": ["best-hris-software"],
    "date": "2026-11-08", "kicker": "Explainer",
    "title": "What Is an HRIS? Features, Types and Cost",
    "seo_title": "What Is an HRIS? Features, Types and Cost | Vettlo",
    "desc": "HRIS software explained: what an HRIS does, how it differs from HRMS, HCM, payroll and an ATS, the main types and what 10 or 20 employees cost.",
    "card": "What an HRIS does, how it differs from payroll and HCM, and what it costs.",
    "answer": ("An HRIS (human resources information system) is the system of record for your employees: profiles, job and pay history, documents, time off and onboarding, with self-service for staff and reports for HR. "
               "It doesn't calculate pay or file taxes on its own; that's payroll software, which many HRIS vendors sell as a module or connect to. "
               f"At published prices, the HRIS platforms we rank cost {_fmt(_hr_lo[0])} ({_hr_lo_n}) to {_fmt(_hr_hi[0])} ({_hr_hi_n}) a month for 20 employees"
               + (f", while {_hr_and(_hr_quote)} {'quotes' if len(_hr_quote) == 1 else 'quote'} every customer." if _hr_quote else ".")),
    "sections": [
        ("does", "What an HRIS does", f"""<p>An HRIS replaces the spreadsheets, shared folders and email threads where employee information usually starts out. Every person gets one record, and the rest of the system works off it:</p>
<ul>{_hr_feats}</ul>
<p>Three groups use it. <b>HR</b> keeps records accurate, runs onboarding and pulls headcount and turnover reports. <b>Managers</b> approve time off and see their team's details. <b>Employees</b> use self-service to update their address or bank details, request leave, sign documents and find policies, which removes a lot of routine requests from HR's inbox.</p>
<p>Higher plans and add-on modules extend the same record into performance reviews, compensation planning, time tracking, applicant tracking and payroll. Which of those you get, and on which plan, is where HRIS products differ most.</p>"""),
        ("vs", "HRIS vs HRMS, HCM, payroll and ATS", f"""<p>HR software terms overlap, and vendors use them loosely. In common usage:</p>
<ul><li><b>HRIS</b> means the core: employee records, documents, time off, onboarding and reporting.</li>
<li><b>HRMS</b> (human resource management system) usually means an HRIS plus operational tools such as time tracking, attendance and payroll.</li>
<li><b>HCM</b> (human capital management) is the broadest term, used mostly by enterprise suites. It adds talent management, such as recruiting, performance, learning, compensation and workforce planning, on top of core HR{f", as in {_hr_and([n for n, _d in HRIS.get('others', []) if 'HCM' in n])}" if any('HCM' in n for n, _d in HRIS.get('others', [])) else ""}.</li></ul>
<p>Two neighboring categories are separate products, even when one vendor sells both:</p>
<ul><li><b>Payroll software.</b> {_hr_faq.get("What's the difference between an HRIS and payroll software?", "An HRIS stores employee records; payroll software calculates pay and files taxes.")}</li>
<li><b>Applicant tracking systems.</b> {_ats_faq.get("What's the difference between an ATS and an HRIS?", "An ATS manages hiring; an HRIS manages people after they're hired.").replace('<a href="/tools/best-hris-software/">HRIS software ranking</a> for the employee side', '<a href="/tools/best-applicant-tracking-systems/">applicant tracking ranking</a> for the hiring side')}</li></ul>
<p>What matters in practice is that payroll, hiring and the HRIS share one employee record, either inside one platform or through an integration, so nobody types the same new hire in three places.</p>"""),
        ("types", "The main types of HRIS", f"""<ul>{f"<li><b>Core HRIS for small and midsize companies</b> covers records, time off, onboarding and reporting in an easy package, with reviews and hiring on higher plans. {_hr_by('bamboohr', 'factorial')} sit here.</li>" if _hr_by('bamboohr', 'factorial') else ""}
{f"<li><b>All-in-one HR, payroll and IT platforms</b> sell modules on one employee database, so onboarding can set up pay, apps and devices together. {_hr_by('rippling')} is the best-known example; our <a href='/compare/bamboohr-vs-rippling/'>BambooHR vs Rippling</a> comparison covers the trade-off.</li>" if _hr_by('rippling') else ""}
{f"<li><b>Mid-market and international HR platforms</b> focus on culture, engagement and multi-country teams, with talent, compensation and payroll as add-on modules. {_hr_by('hibob')} works this way.</li>" if _hr_by('hibob') else ""}
{f"<li><b>Low-cost HR suites</b> publish low per-user prices, often with a free tier, and fit best alongside the same vendor's other apps. {_hr_by('zoho_people')} is one.</li>" if _hr_by('zoho_people') else ""}
{f"<li><b>Mobile-first apps for frontline teams</b> put documents, time off and onboarding on employees' phones for staff who don't sit at a computer, at flat prices per user band. {_hr_by('connecteam')} sits here.</li>" if _hr_by('connecteam') else ""}</ul>
{f"<p>Other HR platforms in the category include {_hr_and([n for n, _d in HRIS.get('others', [])])}. " if HRIS.get('others') else "<p>"}Our <a href="{_hr_cat}">HRIS shortlist</a> scores the ranked platforms on core HR, time off and onboarding, performance, payroll and integrations, ease of use and price.</p>"""),
        ("cost", "How much an HRIS costs", f"""<p>Most HRIS vendors charge per employee per month. Some charge a flat fee for a headcount band instead, and larger vendors quote by headcount and modules. Entry plans for the platforms we rank, from each vendor's pricing page:</p>
{_ptable(_hr_rows)}
<p class="small muted">{HRIS['price_footnote']}</p>
<p>What the published entry plans come to each month for 10 and 20 employees:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Plan</th><th>Pricing unit</th>{''.join(f'<th>{n} employees</th>' for n in _hr_sizes)}</tr></thead><tbody>{_hr_cost_rows}</tbody></table></div>
<p>{(_hr_and(_hr_quote) + " isn't in the table because it publishes no prices. ") if _hr_quote else ""}The cheapest line isn't always the cheapest system: {(_hr_and(_hr_mod) + "'s price covers only the base HRIS module, so payroll and other modules add to the quote, and ") if _hr_mod else ""}performance reviews and time tracking often sit on a higher plan or cost extra, so price the plan that includes the features you'll use.</p>
<p>{"Free plans" if len(_hr_free) > 1 else "Free plan"}: {_hr_faq.get("Is there a free HRIS?", "").replace("Yes. ", "") if _hr_free else "none of the ranked platforms list one."} Budget too for payroll, which is usually a separate fee, and for any implementation or data migration charge in a quote. Pricing payroll as well? See <a href="/guides/payroll-software-cost/">how much payroll software costs</a>.</p>"""),
        ("choose", "How to choose an HRIS", "<ol>" + "".join(f"<li><b>{a}</b> {b}</li>" for a, b in HRIS["choose"]) + f"""</ol>
<p>Our <a href="{_hr_cat}">HRIS shortlist</a> ranks {len(_hr_ranked)} platforms, and <a href="/tools/best-bamboohr-alternatives/">BambooHR alternatives</a> covers cheaper options and ones with payroll on the same record. Read the reviews of {_hr_and([_hr_rv(k) for k in _hr_ranked])}.</p>"""),
    ],
    "faqs": [
        ("What does HRIS stand for?", "Human resources information system: software that stores and manages employee data, such as personal details, job and pay history, documents and time off, and the HR processes built on it, such as onboarding."),
        ("What's the difference between an HRIS and payroll software?", _hr_faq.get("What's the difference between an HRIS and payroll software?", "An HRIS stores employee records; payroll software calculates pay and files taxes.")),
        ("How much does an HRIS cost?", f"At published prices, the HRIS platforms we rank cost {_fmt(_hr_lo[0])} ({_hr_lo_n}) to {_fmt(_hr_hi[0])} ({_hr_hi_n}) a month for 20 employees on their entry plans."
         + (f" {_hr_and(_hr_quote)} {'doesn' if len(_hr_quote) == 1 else 'don'}'t publish prices." if _hr_quote else "")
         + (f" {_hr_and(_hr_mod)}'s price covers only the base HRIS module." if _hr_mod else "")),
        ("Is there a free HRIS?", _hr_faq.get("Is there a free HRIS?", "Some HRIS tools have free plans for very small teams; see our shortlist.")),
    ],
})


# ---------- Marketing automation vs email marketing software
_mv_em, _mv_ma = EM["tools"], MA["tools"]
_mv_emr, _mv_mar = EM["_ranked"], MA["_ranked"]
_mv_emc, _mv_mac = "/tools/best-email-marketing-software/", "/tools/best-marketing-automation-software/"
_mv_and = lambda xs: xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
_mv_rv = lambda n: f'<a href="{REVIEW_URL[n]}">{n}</a>' if n in REVIEW_URL else n
_mv_emfaq, _mv_mafaq = dict(EM["faqs"]), dict(MA["faqs"])
_mv_emch, _mv_mach = dict(EM["choose"]), dict(MA["choose"])
_mv_unit = lambda p: " per seat" if "/seat/" in p else ""
_mv_em_usd = sorted((_money(_mv_em[k]["price"]), _mv_em[k]["name"], k) for k in _mv_emr if _money(_mv_em[k]["price"]))
_mv_ma_usd = sorted((_money(_mv_ma[k]["price"]), _mv_ma[k]["name"], k) for k in _mv_mar if _money(_mv_ma[k]["price"]))
_mv_lo = lambda xs, t: f"{_fmt(xs[0][0])}{_mv_unit(t[xs[0][2]]['price'])} ({xs[0][1]})"
_mv_hi = lambda xs, t: f"{_fmt(xs[-1][0])}{_mv_unit(t[xs[-1][2]]['price'])} ({xs[-1][1]})"
_mv_em_rng = f"{_mv_lo(_mv_em_usd, _mv_em)} to {_mv_hi(_mv_em_usd, _mv_em)}"
_mv_ma_rng = f"{_mv_lo(_mv_ma_usd, _mv_ma)} to {_mv_hi(_mv_ma_usd, _mv_ma)}"
_mv_both = [k for k in _mv_mar if k in _mv_emr]
_mv_both_n = [_mv_ma[k]["short"] for k in _mv_both]
_mv_both_rows = "".join(
    f'<tr><td>{_mv_rv(_mv_ma[k]["name"])}</td><td>{cat_score(EM, k)}/100, #{_mv_emr.index(k) + 1} of {len(_mv_emr)}</td>'
    f'<td>{cat_score(MA, k)}/100, #{_mv_mar.index(k) + 1} of {len(_mv_mar)}</td><td>{_mv_ma[k]["price"]}: {_mv_ma[k]["price_note"]}</td></tr>'
    for k in _mv_both)
_mv_crit = "".join(f"<tr><td>{a[0]}</td><td>{a[1]}%</td><td>{b[0]}</td><td>{b[1]}%</td></tr>" for a, b in zip(EM["criteria"], MA["criteria"]))
_mv_feat = lambda sl: "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in EXPLAIN[sl]["features"])
_mv_row = lambda t, k, cat: (f'<a href="{cat}#{k}">{t[k]["name"]}</a>', t[k]["price"], t[k]["price_note"], t[k]["trial"])
_mv_free_em = [_mv_em[k]["name"] for k in _mv_emr if "free plan" in _mv_em[k]["trial"].lower()]
_mv_free_ma = [_mv_ma[k]["name"] for k in _mv_mar if "free plan" in _mv_ma[k]["trial"].lower()]
_mv_score = _mv_mafaq.get("Which marketing automation tool includes lead scoring for the lowest price?", "")
_mv_diff = _mv_mafaq.get("What is the difference between email marketing and marketing automation software?", "")
_mv_top = lambda cat, t: t[cat["_ranked"][0]]["name"]

guide_page({
    "slug": "marketing-automation-vs-email-marketing", "crumb": "Marketing automation vs email marketing", "dept": "Marketing",
    "cats": ["best-marketing-automation-software", "best-email-marketing-software"],
    "date": "2026-11-09", "kicker": "Explainer",
    "title": "Marketing Automation vs Email Marketing: What's the Difference?",
    "seo_title": "Marketing Automation vs Email Marketing Software | Vettlo",
    "desc": "Email marketing vs marketing automation: what each does, where they overlap, what each costs at published prices and which one your team needs.",
    "card": "What each category does, where they overlap and what each costs.",
    "answer": ("Email marketing software sends newsletters and campaigns to a list and runs simple triggered emails, such as a welcome series. "
               "Marketing automation software runs multi-step journeys across email and other channels based on what each contact does, scores leads and syncs with a CRM so sales knows who is ready to buy. "
               f"Among the tools we rank, email marketing entry plans cost {_mv_em_rng} a month at the smallest list size, while marketing automation entry plans run from {_mv_ma_rng} a month, and lead scoring usually sits several tiers above the entry plan."),
    "sections": [
        ("what", "What each one does", f"""<h3>Email marketing software</h3>
<p>{EXPLAIN["best-email-marketing-software"]["what"]} The core features:</p>
<ul>{_mv_feat("best-email-marketing-software")}</ul>
<h3>Marketing automation software</h3>
<p>{EXPLAIN["best-marketing-automation-software"]["what"]} The core features:</p>
<ul>{_mv_feat("best-marketing-automation-software")}</ul>
<p>The short version: an email tool is organized around the <b>list and the campaign</b>, and asks "what do we send this week?" A marketing automation platform is organized around the <b>contact and the journey</b>, and asks "what should happen next for this person, and are they ready for sales?"</p>"""),
        ("differences", "The key differences", f"""<p>Both categories send email and both offer automation, so the line is about depth, not presence:</p>
<div class="table-wrap"><table><thead><tr><th></th><th>Email marketing</th><th>Marketing automation</th></tr></thead><tbody>
<tr><td>Main job</td><td>Campaigns and newsletters to a list or segment</td><td>Behavior-based journeys for each contact, through to a sales handoff</td></tr>
<tr><td>Automation</td><td>Welcome series, abandoned-cart and date-based emails; cheaper plans often cap steps or actions</td><td>Branching workflows with multiple triggers, goals and waits, often across several channels</td></tr>
<tr><td>Lead scoring</td><td>Uncommon, or a paid add-on</td><td>A defining feature, though often on a higher tier or an add-on</td></tr>
<tr><td>CRM</td><td>Integrations, sometimes a light contact database</td><td>Two-way CRM sync or a CRM built in, so sales sees engagement</td></tr>
<tr><td>Reporting</td><td>Opens, clicks, conversions and A/B tests</td><td>Attribution of campaigns to pipeline and revenue</td></tr>
<tr><td>Typical buyer</td><td>Small businesses, creators and online stores</td><td>B2B marketing teams working with sales, and product-led companies messaging on behavior</td></tr>
</tbody></table></div>
<p>Our two rankings weight their criteria differently for the same reason. Email marketing tools are judged more on the builder, segmentation and ease of use; marketing automation platforms on journeys, lead management and attribution:</p>
<div class="table-wrap"><table><thead><tr><th>Email marketing criterion</th><th>Weight</th><th>Marketing automation criterion</th><th>Weight</th></tr></thead><tbody>{_mv_crit}</tbody></table></div>
<p class="small muted">Weights from our <a href="{_mv_emc}">email marketing</a> and <a href="{_mv_mac}">marketing automation</a> rankings. See our <a href="/methodology/">methodology</a> for how scores are calculated.</p>"""),
        ("overlap", "Where the two overlap", f"""<p>The categories blur in the middle. {_mv_and([_mv_rv(_mv_ma[k]["name"]) for k in _mv_both])} {"appears" if len(_mv_both) == 1 else "appear"} in both of our rankings, scored against each category's own criteria:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Email marketing ranking</th><th>Marketing automation ranking</th><th>Pricing</th></tr></thead><tbody>{_mv_both_rows}</tbody></table></div>
<p>Tools like these are a sensible middle step: you get campaigns and newsletters on the entry plan and can move up to deeper journeys without migrating your list. The catch is that the automation features usually start one or two plans up. {_mv_emch.get("Check automation limits on the cheaper plans.", "")}</p>
<p>At the other end, {_mv_rv(_mv_ma["hubspot"]["name"]) if "hubspot" in _mv_mar else "HubSpot Marketing Hub"} sells a Starter plan with limited automation and puts full workflows and lead scoring on Professional, which is why its <a href="/tools/best-hubspot-marketing-hub-alternatives/">alternatives</a> page and our <a href="/compare/hubspot-vs-activecampaign/">HubSpot vs ActiveCampaign</a> comparison focus on that jump.</p>"""),
        ("cost", "What each one costs", f"""<p>Email marketing tools mostly price by contacts or subscribers, with Brevo pricing by emails sent. Marketing automation platforms price by contacts too, but some add per-seat charges, annual contracts or one-time onboarding fees. Entry prices from each vendor's pricing page:</p>
<h3>Email marketing software</h3>
{_ptable([_mv_row(_mv_em, k, _mv_emc) for k in _mv_emr])}
<p class="small muted">{EM["price_footnote"]}</p>
<h3>Marketing automation software</h3>
{_ptable([_mv_row(_mv_ma, k, _mv_mac) for k in _mv_mar])}
<p class="small muted">{MA["price_footnote"]}</p>
<p>The entry prices overlap, but the plans that make a platform "marketing automation" don't. {_mv_score} {_mv_mach.get("Add onboarding and seats to year one.", "")} For prices at your list size, see <a href="/guides/email-marketing-software-cost/">how much email marketing software costs</a>.</p>"""),
        ("choose", "Which one do you need?", f"""<p><b>Email marketing software is enough if</b> you mostly send newsletters, promotions and a handful of automated emails; you sell online and want abandoned-cart and post-purchase flows; or there's no sales team waiting for qualified leads. Start with our <a href="{_mv_emc}">email marketing shortlist</a> ({_mv_top(EM, _mv_em)} ranks first).</p>
<p><b>You need marketing automation if</b> sales needs to know which leads are ready, you want journeys that branch on behavior across several channels, or you have to show which campaigns create pipeline. Start with our <a href="{_mv_mac}">marketing automation shortlist</a> ({_mv_top(MA, _mv_ma)} ranks first).</p>
<p>Whichever you pick, two checks from our rankings apply:</p>
<ol><li><b>Price the plan that includes your must-have feature.</b> {_mv_mach.get("Find the plan where your must-have feature starts.", "")}</li>
<li><b>Test one real workflow in the trial.</b> {_mv_mach.get("Build one real journey in the trial.", "")}</li></ol>
<p>Comparing specific tools? See <a href="/compare/mailerlite-vs-mailchimp/">MailerLite vs Mailchimp</a>, <a href="/compare/mailchimp-vs-brevo/">Mailchimp vs Brevo</a>, <a href="/compare/klaviyo-vs-mailchimp/">Klaviyo vs Mailchimp</a> and <a href="/tools/best-mailchimp-alternatives/">Mailchimp alternatives</a>.</p>"""),
    ],
    "faqs": [
        ("What is the difference between email marketing and marketing automation?", _mv_diff or "Email marketing tools focus on campaigns and simple automations; marketing automation platforms add multi-step journeys across channels, lead scoring and attribution."),
        ("Is marketing automation just automated email?", "No. Automated emails are part of it, but marketing automation also scores leads, branches journeys on behavior, can use channels such as SMS, and syncs with a CRM so marketing and sales share the same view of each contact."),
        ("Which tools do both email marketing and marketing automation?", f"{_mv_and(_mv_both_n)} {'is' if len(_mv_both) == 1 else 'are'} in both of our rankings: campaigns and newsletters on the entry plans, with deeper automation on higher plans." if _mv_both else "Several email tools offer automation on higher plans; see our shortlists."),
        ("Which marketing automation tool has lead scoring for the lowest price?", _mv_score or "See our marketing automation shortlist for which plan first includes lead scoring."),
    ],
})


# ---------- What is accounts payable? (AP process)
# AP features by plan, read from the vendor pricing detail in data/review_depth.json (same data as the review pages).
def _ap_plan_price(tool, plan):
    """Regular monthly price of a plan as text, e.g. "$38/mo" or "$40/mo billed annually"; None if not listed."""
    for p, s, _d in _ac_depth.get(tool, {}).get("plans", []):
        if p == plan:
            v = _money(s)
            if v is None:
                return None
            return f"{_fmt(v)}/mo" + (" billed annually" if "billed annually" in s else "")
    return None


def _ap_first(tool, feature):
    return next((p for f, p in _ac_depth.get(tool, {}).get("first_plan", []) if f == feature), None)


def _ap_limit(tool, row, plan):
    lim = _ac_depth.get(tool, {}).get("limits", {})
    for r in lim.get("rows", []):
        if r[0] == row and plan in lim.get("cols", []):
            return r[1:][lim["cols"].index(plan)]
    return None


_ap_name = {k: _ac[k]["name"] for k in _ac_ranked}
_ap_rows = []  # (tool link, AP feature, first plan, plan price)


def _ap_add(k, feature, label=None, plan=None, extra=""):
    tool = _ap_name.get(k)
    if not tool or tool not in _ac_depth:
        return
    pl = plan or _ap_first(tool, feature)
    if not pl:
        return
    pl = pl.split(" (")[0]
    pr = _ap_plan_price(tool, pl)
    if pr is None:
        return
    _ap_rows.append((_ac_rv(k), (label or feature) + extra, pl, pr))


_ap_add("quickbooks", "Bill pay with free ACH")
_ap_add("quickbooks", "1099 e-filing and bill approval workflows")
_xb_early = _ap_limit("Xero", "Bills", "Early")
_xb_grow = next((c for c in _ac_depth.get("Xero", {}).get("limits", {}).get("cols", []) if _ap_limit("Xero", "Bills", c) == "Unlimited"), None)
_ap_add("xero", "Free ACH bill payments", extra=f" (Early caps bills at {_xb_early} a month)" if _xb_early else "")
_ap_add("xero", "W-9 and 1099 management")
if _xb_grow:
    _ap_add("xero", "", label="Unlimited bills", plan=_xb_grow)
_zb_std = _ap_limit("Zoho Books", "Bills and expenses per year", "Standard")
_zb_free = _ap_limit("Zoho Books", "Bills and expenses per year", "Free")
if _zb_std:
    _ap_add("zohobooks", "", label=f"Bills and expenses: {_zb_std} a year" + (f" (Free plan: {_zb_free})" if _zb_free else ""), plan="Standard")
_ap_add("zohobooks", "Sales and purchase approvals")
_ap_add("zohobooks", "Vendor portal")
_ap_table = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in _ap_rows)
_ap_qa = re.search(r"free up to a monthly allotment, then \$([\d.]+) per transaction", " ".join(_ac_depth.get("QuickBooks Online", {}).get("notes", [])))
_ap_appr = [f"{_ac[k]['short']} {p.split(' (')[0]}" for k, f in (("quickbooks", "1099 e-filing and bill approval workflows"), ("zohobooks", "Sales and purchase approvals"))
            if k in _ap_name and _ap_name[k] in _ac_depth and (p := _ap_first(_ap_name[k], f))]
_ap_chk = lambda tool: _ac_depth.get(tool, {}).get("checked", "")
_ap_checked = max((_ap_chk(_ap_name[k]) for k in ("quickbooks", "xero", "zohobooks") if k in _ap_name), default="")
_ap_checked_h = (lambda d: f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(d[5:7]) - 1]} {int(d[8:])}, {d[:4]}")(_ap_checked) if _ap_checked else ""

# Early-payment discount maths (2/10 net 30): annualized cost of skipping the discount
_ap_d, _ap_dd, _ap_net = 2, 10, 30
_ap_apr = _ap_d / (100 - _ap_d) * 365 / (_ap_net - _ap_dd) * 100
_ap_bill = 1200
_ap_disc = _ap_bill * _ap_d / 100

guide_page({
    "slug": "accounts-payable-process", "crumb": "Accounts payable", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-10", "kicker": "Explainer",
    "title": "What Is Accounts Payable? The AP Process, Step by Step",
    "seo_title": "Accounts Payable: What It Is and the AP Process | Vettlo",
    "desc": "Accounts payable explained: what AP is, the six-step process from vendor invoice to payment, three-way matching, net 30 terms and the controls that matter.",
    "card": "What AP is, the six steps from invoice to payment, matching, terms and controls.",
    "answer": ("Accounts payable (AP) is the money a business owes its suppliers for goods and services it has received but not yet paid for, recorded as a current liability on the balance sheet. "
               "The AP process turns each vendor invoice into a payment in six steps: set up the vendor, capture the invoice, match it to the order and delivery, approve it, pay it by the due date, and record and reconcile the payment."),
    "sections": [
        ("what", "What is accounts payable?", f"""<p>Accounts payable is the total of unpaid bills from vendors: the office lease invoice, the supplier who shipped inventory on net 30 terms, the contractor who sent an invoice last week. Each bill is a short-term debt, so AP sits under <b>current liabilities</b> on the balance sheet, and it shrinks as you pay. In most small businesses AP lives in the bills or purchases module of the accounting software; our <a href="{_ac_cat}">comparison of the best accounting software</a> ranks {len(_ac_ranked)} tools, and this guide covers the process itself.</p>
<p>Three terms get mixed up with AP:</p>
<div class="table-wrap"><table><thead><tr><th>Term</th><th>What it is</th><th>Where it shows up</th></tr></thead><tbody>
<tr><td>Accounts payable</td><td>Money you owe vendors for things already received</td><td>Current liability</td></tr>
<tr><td>Accounts receivable</td><td>Money customers owe you for invoices you sent</td><td>Current asset</td></tr>
<tr><td>Accrued expenses</td><td>Costs incurred but not yet billed, such as wages earned since the last payday</td><td>Current liability, usually separate from AP</td></tr>
<tr><td>Expense reimbursements</td><td>Money owed to employees for out-of-pocket business spend</td><td>Often run through an expense tool, not vendor AP</td></tr>
</tbody></table></div>
<p>Employee receipts and company cards are their own workflow; our <a href="/tools/best-expense-management-software/">expense management software shortlist</a> covers the tools built for that.</p><h3>How is accounts payable recorded?</h3>
<p>Under accrual accounting, a bill hits AP when you receive it, not when you pay it. That's two journal entries per bill. Using a {_fmt(_ap_bill)} supplier invoice as an example:</p>
<div class="table-wrap"><table><thead><tr><th>Event</th><th>Debit</th><th>Credit</th><th>Effect on AP</th></tr></thead><tbody>
<tr><td>Bill received and entered</td><td>Expense or inventory {_fmt(_ap_bill)}</td><td>Accounts payable {_fmt(_ap_bill)}</td><td>Up {_fmt(_ap_bill)}</td></tr>
<tr><td>Bill paid</td><td>Accounts payable {_fmt(_ap_bill)}</td><td>Cash {_fmt(_ap_bill)}</td><td>Down {_fmt(_ap_bill)}</td></tr>
</tbody></table></div>
<p>So accounts payable is a credit balance: entering a bill credits it, paying a bill debits it. Accounting software makes both entries for you when you enter a bill and later mark it paid.</p>
<p>A business keeping its books on the cash method records the expense only when it pays, so there is no AP balance in the ledger. It still needs a list of unpaid bills to know what's due, which is why most tools keep a bills list either way.</p>"""),
        ("steps", "What are the steps in the accounts payable process?", f"""<p>The AP process has six steps, from adding a vendor to closing out the payment. Small teams often do all six with one or two people; larger ones split them so no single person can both add a vendor and pay it.</p>
<ol>
<li><b>Set up the vendor.</b> Record the legal name, address, payment details and terms, and collect a Form W-9 from contractors and other vendors you may need to report, so you have their taxpayer ID. Under the IRS instructions for tax years beginning after 2025, you report nonemployee compensation of $2,000 or more on Form 1099-NEC (up from $600), and payments to corporations generally aren't reported, with exceptions such as attorneys' fees. Forms are due January 31.</li>
<li><b>Capture the invoice.</b> Get every bill into one place: a dedicated AP email inbox, uploads, or receipt scanning in the accounting tool. Enter the vendor, invoice number, date, due date, amount and the account or item it belongs to.</li>
<li><b>Match and verify.</b> Check the invoice against what you ordered and what arrived (see three-way matching below), and check the invoice number against bills already entered to catch duplicates.</li>
<li><b>Approve.</b> The person who ordered or owns the budget confirms the bill is valid. Set a rule for who approves what, for example any bill above a set amount needs a second approver.</li>
<li><b>Schedule and pay.</b> Pay by the due date, or by the discount date if the vendor offers one, by ACH, check or card. Batching payments once or twice a week keeps it manageable.</li>
<li><b>Record and reconcile.</b> Mark the bill paid so AP drops, match the payment to the bank statement, and keep the invoice with proof of payment. At month end, the unpaid bills report should agree with the AP balance on the balance sheet.</li>
</ol>
<p class="small muted">This summarizes IRS reporting rules and isn't tax advice; check the current IRS instructions or ask your accountant about your vendors.</p>"""),
        ("matching", "What is three-way matching?", f"""<p>Three-way matching means paying an invoice only when it agrees with two other documents: the purchase order (what you agreed to buy) and the receiving record (what actually arrived). It stops you paying for goods that were never delivered, or at a price you never agreed.</p>
<div class="table-wrap"><table><thead><tr><th>Document</th><th>Who creates it</th><th>What you compare</th></tr></thead><tbody>
<tr><td>Purchase order</td><td>Your business, when ordering</td><td>Item, quantity, agreed unit price, terms</td></tr>
<tr><td>Receiving record (packing slip or goods received note)</td><td>Whoever accepts the delivery</td><td>Quantity actually received, condition</td></tr>
<tr><td>Vendor invoice</td><td>The supplier</td><td>Quantity billed, price, total, due date</td></tr>
</tbody></table></div>
<p><b>Two-way matching</b> compares only the purchase order and the invoice. It suits services and subscriptions, where there's no delivery to count. Many small businesses don't issue purchase orders at all; for them the practical version is checking each bill against the contract or quote and confirming with whoever ordered it that the work was done.</p>
<p>When the documents don't agree, don't pay the difference: hold the bill, ask the vendor for a corrected invoice or a credit note, and pay the amount you can match.</p>"""),
        ("terms", "How do net 30 and 2/10 net 30 payment terms work?", f"""<p>Payment terms say how many days you have to pay after the invoice date. <b>Net 30</b> means the full amount is due in 30 days. <b>2/10 net 30</b> means you can take {_ap_d}% off if you pay within {_ap_dd} days; otherwise the full amount is due in {_ap_net}.</p>
<div class="table-wrap"><table><thead><tr><th>Term</th><th>Meaning</th></tr></thead><tbody>
<tr><td>Due on receipt</td><td>Pay as soon as you get the invoice</td></tr>
<tr><td>Net 15 / net 30 / net 60</td><td>Full amount due 15, 30 or 60 days after the invoice date</td></tr>
<tr><td>{_ap_d}/{_ap_dd} net {_ap_net}</td><td>{_ap_d}% discount if paid within {_ap_dd} days, full amount due in {_ap_net}</td></tr>
<tr><td>EOM</td><td>Counted from the end of the month the invoice was issued</td></tr>
</tbody></table></div>
<p>Early-payment discounts are worth more than they look. On a {_fmt(_ap_bill)} bill, {_ap_d}/{_ap_dd} net {_ap_net} saves {_fmt(_ap_disc)} for paying {_ap_net - _ap_dd} days early. Skipping it is like borrowing {_fmt(_ap_bill - _ap_disc)} for {_ap_net - _ap_dd} days at {_ap_d}/{100 - _ap_d}, which works out to about {_ap_apr:.0f}% a year ({_ap_d}/{100 - _ap_d} × 365/{_ap_net - _ap_dd}). If you have the cash, taking the discount usually beats holding it.</p>
<p>Without a discount, paying on the due date rather than early keeps cash in the business longer. Finance teams track this as <b>days payable outstanding</b> (DPO): average accounts payable ÷ cost of goods sold × the days in the period. A higher DPO means you take longer to pay; a sudden rise can also mean bills are getting stuck in approval.</p>"""),
        ("controls", "How do you prevent duplicate payments and invoice fraud?", f"""<p>Two things go wrong in AP: paying the same bill twice, and paying a fake or altered one. These controls address both:</p>
<ul>
<li><b>Separate duties.</b> The person who adds or edits a vendor shouldn't also approve and release its payments. In a two-person business, have the owner approve payments the bookkeeper prepares.</li>
<li><b>Verify bank detail changes.</b> When a vendor asks to change where you send money, confirm by calling a phone number you already have on file, not one in the request.</li>
<li><b>Block duplicates.</b> Enter invoice numbers exactly and let the software warn on a repeat vendor and number.</li>
<li><b>Pay only real vendors.</b> The FTC's May 2026 alert to small businesses advises checking all invoices closely, having clear procedures for approving purchases and invoices from vendors you actually work with, and knowing who you're dealing with.</li>
<li><b>Keep the paper trail.</b> The IRS says supporting documents should identify the payee, the amount paid, proof of payment, the date incurred and a description showing it was a business expense; invoices and canceled checks or bank transfer records together do that. Keep them at least until the period of limitations for the return runs out, generally 3 years from the date you filed.</li>
</ul>"""),
        ("software", "Which accounting plans include bill pay and approvals?", f"""<p>Entry plans usually let you enter and pay bills; approval workflows and higher bill volumes start further up the plan ladder. Where AP features first appear on the three tools whose plan details we track, at regular prices:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>AP feature</th><th>First plan</th><th>Plan price</th></tr></thead><tbody>{_ap_table}</tbody></table></div>
<p class="small muted">From each vendor's US pricing page, checked {_ap_checked_h}.{f" QuickBooks' free standard ACH bill payments cover a monthly allotment, then cost {_fmt(float(_ap_qa.group(1)))} each." if _ap_qa else ""}</p>
<p>If more than one person needs to sign off on bills, price the first plan with approvals ({_ac_and(_ap_appr)}), not the entry plan. Our <a href="/guides/accounting-software-cost/">accounting software cost guide</a> prices every plan and team size, and <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> compares the two most common choices plan by plan. For tool-level detail, read the reviews of {_ac_and([_ac_rv(k) for k in ("quickbooks", "xero", "zohobooks") if k in _ap_name])}.</p>"""),
    ],
    "faqs": [
        ("Is accounts payable an asset or a liability?", "Accounts payable is a liability. It's money the business owes vendors, usually within weeks, so it's listed under current liabilities on the balance sheet."),
        ("Is accounts payable a debit or a credit?", "Accounts payable normally carries a credit balance. Entering a vendor bill credits AP and debits an expense or inventory account; paying the bill debits AP and credits cash."),
        ("What is the difference between accounts payable and accounts receivable?", "Accounts payable is what you owe suppliers for goods and services you received. Accounts receivable is what customers owe you for invoices you sent. AP is a liability; AR is an asset."),
        ("Do I need to send a 1099 to every vendor?", "No. For tax years beginning after 2025, the IRS instructions require Form 1099-NEC for nonemployee compensation of $2,000 or more, and payments to corporations generally aren't reported, with exceptions such as attorneys' fees. Collect a W-9 when you set up the vendor so you can tell. This isn't tax advice."),
    ],
    "sources": [
        ("IRS: Instructions for Forms 1099-MISC and 1099-NEC", "https://www.irs.gov/instructions/i1099mec"),
        ("IRS: What kind of records should I keep", "https://www.irs.gov/businesses/small-businesses-self-employed/what-kind-of-records-should-i-keep"),
        ("IRS: Topic no. 305, Recordkeeping", "https://www.irs.gov/taxtopics/tc305"),
        ("FTC: Run a small business? Pay your bills, not scammers (May 2026)", "https://consumer.ftc.gov/consumer-alerts/2026/05/run-small-business-pay-your-bills-not-scammers"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
        ("Xero US pricing plans", "https://www.xero.com/us/pricing-plans/"),
        ("Zoho Books pricing (US)", "https://www.zoho.com/us/books/pricing/"),
    ],
})


# ---------- Cash vs accrual accounting
# Hypothetical one-month example (December), computed here so the two totals always agree with the rows.
_ca_tx = [  # (date, what happened, cash-basis income, cash-basis expense, accrual income, accrual expense)
    ("Dec 1", "Pay December rent", 0, 1000, 0, 1000),
    ("Dec 5", "Cash sale, paid on the spot", 2000, 0, 2000, 0),
    ("Dec 10", "Invoice a client for December work, due in 30 days", 0, 0, 8000, 0),
    ("Dec 18", "Receive a supplier bill for December materials, due in 21 days", 0, 0, 0, 1500),
    ("Dec 22", "Client pays an invoice for work done in November", 3000, 0, 0, 0),
]
_ca_ci = sum(r[2] for r in _ca_tx)
_ca_ce = sum(r[3] for r in _ca_tx)
_ca_ai = sum(r[4] for r in _ca_tx)
_ca_ae = sum(r[5] for r in _ca_tx)
_ca_cp, _ca_ap = _ca_ci - _ca_ce, _ca_ai - _ca_ae
_ca_cell = lambda v: _fmt(v) if v else "—"
_ca_rows = "".join(f"<tr><td>{d}</td><td>{w}</td><td>{_ca_cell(ci)}</td><td>{_ca_cell(ce)}</td><td>{_ca_cell(ai)}</td><td>{_ca_cell(ae)}</td></tr>" for d, w, ci, ce, ai, ae in _ca_tx)
_ca_rows += f"<tr><td></td><td><b>December totals</b></td><td><b>{_fmt(_ca_ci)}</b></td><td><b>{_fmt(_ca_ce)}</b></td><td><b>{_fmt(_ca_ai)}</b></td><td><b>{_fmt(_ca_ae)}</b></td></tr>"
_ca_rows += f"<tr><td></td><td><b>December profit</b></td><td colspan=\"2\"><b>{_fmt(_ca_cp)}</b></td><td colspan=\"2\"><b>{_fmt(_ca_ap)}</b></td></tr>"
_ca_inv = next(r[4] for r in _ca_tx if r[0] == "Dec 10")
_ca_bill = next(r[5] for r in _ca_tx if r[0] == "Dec 18")
# IRS gross receipts test (section 448(c)), from IRS sources fetched 2026-11-11
_ca_gr = {2025: 31, 2026: 32}  # $ millions: Form 8990 instructions (2025), Rev. Proc. 2025-32 sec. 4.30 (2026)

# How each ranked tool handles report basis, from each vendor's help docs (checked 2026-11-11).
_ca_tool = {
    "quickbooks": ("Set a company default in Settings > Account and settings > Advanced > Accounting", "Yes: choose Cash or Accrual on any standard report, or under Customize"),
    "xero": ("Xero says it supports both cash and accrual reporting", "Yes: Xero says you can run reports on a cash or accrual basis and switch views any time"),
    "zohobooks": ("Report Basis field under Reports > Configure Report Layout (used for printing and PDFs)", "Yes, through Customize Report > Report Basis, on plans that include report customization"),
    "freshbooks": ("No single setting: the updated Profit and Loss report is accrual only (Billed)", "Partly: the legacy Profit and Loss report offers Billed (accrual) or Collected (cash)"),
    "wave": ("Every report starts on accrual by default", "Yes on the profit and loss, balance sheet, sales tax, trial balance and account transactions reports; the cash flow report has no accrual option"),
}
_ca_trs = "".join(f"<tr><td>{_ac_rv(k)}</td><td>{a}</td><td>{b}</td></tr>" for k, (a, b) in _ca_tool.items() if k in _ac_ranked)
_ca_names = _ac_and([_ac[k]["short"] for k in _ca_tool if k in _ac_ranked])

guide_page({
    "slug": "cash-vs-accrual-accounting", "crumb": "Cash vs accrual accounting", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-11", "kicker": "Explainer",
    "title": "Cash vs Accrual Accounting: Which Method Should Your Business Use?",
    "seo_title": "Cash vs Accrual Accounting: Differences and IRS Rules | Vettlo",
    "desc": f"Cash vs accrual accounting explained with a worked example, the IRS rules on who may use the cash method (${_ca_gr[2026]}M test for 2026) and how to switch.",
    "card": "Both methods side by side, a worked example, IRS limits and how to switch.",
    "answer": ("In cash vs accrual accounting, the difference is timing: cash accounting records income when money arrives and expenses when you pay them; accrual accounting records income when you earn it and expenses when you incur them, whether or not cash has moved. "
               "Most small businesses may choose either for taxes: the IRS bars only C corporations, partnerships with a C corporation partner and tax shelters from the cash method, "
               f"and the first two keep it if their average annual gross receipts for the prior 3 years are ${_ca_gr[2026]} million or less (tax years beginning in 2026). "
               "Cash is simpler and tracks your bank balance; accrual shows what you're owed and what you owe, so it gives the truer picture of profit."),
    "sections": [
        ("difference", "What is the difference between cash and accrual accounting?", f"""<p>The difference between cash vs accrual accounting is timing: the same sale or bill lands in a different month, and sometimes a different tax year, depending on the method. Under the <b>cash method</b> you generally report income in the year you receive it and deduct expenses in the year you pay them. Under the <b>accrual method</b> you report income in the year you earn it and deduct expenses in the year you incur them, as IRS Publication 538 puts it.</p>
<p>The small-business tools in our <a href="{_ac_cat}">ranking of the best accounting software</a> can show reports on either basis (details below), so the software rarely decides this for you; the tax rules and how your business gets paid do. How the two compare:</p>
<div class="table-wrap"><table><thead><tr><th></th><th>Cash method</th><th>Accrual method</th></tr></thead><tbody>
<tr><td>Income is recorded</td><td>When the customer's payment arrives</td><td>When you deliver the work or goods and bill for it</td></tr>
<tr><td>Expenses are recorded</td><td>When you pay the bill</td><td>When you receive the goods or service, even if unpaid</td></tr>
<tr><td>Unpaid customer invoices</td><td>Not in income until paid</td><td>In income and in accounts receivable</td></tr>
<tr><td>Unpaid supplier bills</td><td>Not an expense until paid</td><td>An expense and a liability in accounts payable</td></tr>
<tr><td>Profit follows</td><td>Money in and out of the bank</td><td>The work done in the period</td></tr>
<tr><td>Effort to keep</td><td>Lower: the bank statement drives most entries</td><td>Higher: invoices, bills and adjustments must be tracked</td></tr>
</tbody></table></div>
<p>Under the cash method, money can count as received before you withdraw it: the IRS treats income as <b>constructively received</b> when it's credited to your account or made available to you without restriction. And under either method, unpaid bills still have to be tracked so you pay them on time; our <a href="/guides/accounts-payable-process/">guide to the accounts payable process</a> covers that workflow.</p>"""),
        ("example", "Cash vs accrual: a worked example", f"""<p>The same five December transactions give two different profits. This is a hypothetical service business, used only to show the mechanics:</p>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Transaction</th><th>Cash income</th><th>Cash expense</th><th>Accrual income</th><th>Accrual expense</th></tr></thead><tbody>{_ca_rows}</tbody></table></div>
<p>Cash basis shows {_fmt(_ca_cp)} of December profit; accrual shows {_fmt(_ca_ap)}. The gap comes from three items:</p>
<ul><li>The {_fmt(_ca_inv)} December invoice is income in December under accrual, but under cash it waits until the client pays in January, which is also the next tax year.</li>
<li>The {_fmt(_ca_bill)} supplier bill is a December expense under accrual and a January expense under cash.</li>
<li>The {_fmt(3000)} payment for November's work is December income under cash, but under accrual it was already counted in November, so in December it only clears accounts receivable.</li></ul>
<p>That's why cash basis can make a month look weak right after a busy one, and strong right after a slow one: it reports when money moved, not when the work happened. Accrual lines up revenue with the costs of earning it.</p>"""),
        ("irs", "Who can use the cash method under IRS rules?", f"""<p>Most small businesses can use the cash method for federal taxes. IRS Publication 538 lists three kinds of taxpayers that generally can't:</p>
<ul><li>A corporation other than an S corporation (a C corporation).</li>
<li>A partnership with a C corporation as a partner.</li>
<li>A tax shelter, as defined in section 448(d)(3) of the tax code.</li></ul>
<p>The first two can still use cash if they pass the <b>gross receipts test</b>: add the gross receipts for the 3 prior tax years and divide by 3. The limit is adjusted for inflation each year:</p>
<div class="table-wrap"><table><thead><tr><th>Tax years beginning in</th><th>Average annual gross receipts limit</th><th>IRS source</th></tr></thead><tbody>
{''.join(f"<tr><td>{y}</td><td>${m} million</td><td>{s}</td></tr>" for (y, m), s in zip(_ca_gr.items(), ("Instructions for Form 8990", "Rev. Proc. 2025-32, section 4.30")))}
</tbody></table></div>
<p>A tax shelter can't use the test, and a qualified personal service corporation can use cash if it meets the function and ownership tests. Gross receipts for a short tax year are annualized.</p>
<h3>What about inventory?</h3>
<p>Businesses that sell products often assume they must use accrual. Under Publication 538, a <b>small business taxpayer</b> (one that passes the same gross receipts test and isn't a tax shelter) can choose not to keep an inventory, so stock alone doesn't force accrual for tax purposes.</p>
<h3>Can you mix the two methods?</h3>
<p>Yes, within limits. The IRS lets you use a combination of cash, accrual and special methods if it clearly reflects income and you use it consistently, but if you use the cash method for income you must also use it for expenses.</p>
<p class="small muted">This summarizes federal IRS guidance and isn't tax advice. State rules and your own facts can differ; check with your accountant or tax preparer.</p>"""),
        ("choose", "Which method should your business use?", f"""<p>Choose cash if you're small, mostly paid on the spot and want books that match your bank balance; choose accrual if you invoice on terms, carry stock, or need to show lenders or investors what you're owed and owe. The table is a starting point for that conversation with your accountant:</p>
<div class="table-wrap"><table><thead><tr><th>If your business…</th><th>Usually fits</th><th>Why</th></tr></thead><tbody>
<tr><td>Is a sole proprietor or freelancer paid at the time of sale</td><td>Cash</td><td>Little gap between earning and getting paid, and simpler records</td></tr>
<tr><td>Sends invoices on net 30 or longer terms</td><td>Accrual</td><td>Cash basis hides sales you've made but not collected</td></tr>
<tr><td>Is a C corporation over the gross receipts limit</td><td>Accrual (required)</td><td>The IRS bars the cash method above the limit</td></tr>
<tr><td>Wants a bank loan, investors or to sell the company</td><td>Accrual</td><td>Statements show receivables, payables and profit by period</td></tr>
<tr><td>Has big swings between when it bills and when it's paid</td><td>Accrual for management reports</td><td>Profit by month reflects the work, not the payment dates</td></tr>
<tr><td>Wants to time income at year end</td><td>Cash</td><td>Income counts when received, though constructive receipt still applies</td></tr>
</tbody></table></div>
<p>Because accounting software can show both bases from the same transactions, you can look at accrual reports to run the business even if you file taxes on the cash method. If you're also comparing tools, our <a href="/guides/accounting-software-cost/">accounting software cost guide</a> shows what each plan costs at regular prices.</p>"""),
        ("switch", "How do you change from cash to accrual accounting?", f"""<p>For taxes, you pick a method on your first return without IRS approval; after that, switching between cash and accrual generally needs IRS approval, requested on Form 3115. In your software, flipping a report's basis is a separate thing: it changes how reports display, not your tax method.</p>
<ol>
<li><b>Confirm you need or want to change.</b> Growing past the gross receipts limit as a C corporation is the common forced switch; a lender asking for accrual statements is a common voluntary one.</li>
<li><b>Talk to your tax preparer about timing.</b> The IRS says you must file a current Form 3115 to request a change in an overall accounting method, and some changes qualify for automatic consent while others use the non-automatic procedure.</li>
<li><b>Bring receivables and payables up to date.</b> Accrual needs every open customer invoice and unpaid supplier bill entered with the right dates, plus any prepaid or accrued items your accountant adjusts.</li>
<li><b>Change the reporting basis in your accounting software,</b> or run both side by side for a few months to see the difference (see the next section).</li>
<li><b>Stay consistent.</b> QuickBooks' own help notes that the IRS requires the same method from year to year and approval before you change it.</li>
</ol>
<p class="small muted">Not tax advice: the steps above describe the general IRS process from Publication 538.</p>"""),
        ("software", "How do accounting tools handle cash and accrual reports?", f"""<p>{_ca_names} all keep one set of transactions and let you view reports on a cash or accrual basis, but where you switch, and which reports support it, differs. From each vendor's help pages, checked {hdate("2026-11-11")}:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Default or company setting</th><th>Switch basis per report?</th></tr></thead><tbody>{_ca_trs}</tbody></table></div>
<p>If you need cash-basis reports every month, check that the reports you send your accountant support it on the plan you'd buy. For the full scoring of each tool, see the reviews of {_ac_and([_ac_rv(k) for k in _ca_tool if k in _ac_ranked])}, or the plan-by-plan <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero comparison</a>.</p>"""),
    ],
    "faqs": [
        ("Is cash or accrual accounting better for a small business?", "Neither is better for everyone. Cash is simpler and matches your bank account, which suits freelancers and businesses paid at the time of sale. Accrual shows what customers owe and what you owe, which suits businesses that invoice on terms, carry inventory or need statements for lenders."),
        ("What is the gross receipts limit for the cash method in 2026?", f"For tax years beginning in 2026, a C corporation or a partnership with a C corporation partner can use the cash method if its average annual gross receipts for the 3 prior tax years are ${_ca_gr[2026]} million or less (Rev. Proc. 2025-32). For 2025 the limit was ${_ca_gr[2025]} million. Tax shelters can't use the cash method at any size."),
        ("Can an LLC use cash basis accounting?", "Usually, yes. The IRS limits apply to C corporations, partnerships with a C corporation partner and tax shelters. An LLC taxed as a sole proprietorship, an S corporation or a partnership without C corporation partners isn't on that list. This isn't tax advice; confirm with your tax preparer."),
        ("Does QuickBooks use cash or accrual accounting?", "Both. In QuickBooks Online you set the company's default method under Settings > Account and settings > Advanced > Accounting, and you can run any standard report on a cash or accrual basis without changing your transactions."),
    ],
    "sources": [
        ("IRS: Publication 538, Accounting Periods and Methods", "https://www.irs.gov/publications/p538"),
        ("IRS: Rev. Proc. 2025-32 (2026 inflation adjustments, section 4.30)", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"),
        ("IRS: Instructions for Form 8990 (gross receipts test for 2025)", "https://www.irs.gov/instructions/i8990"),
        ("QuickBooks: Choose between cash and accrual accounting methods in QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-us/help-article/product-preferences/choose-cash-accrual-accounting-methods-reports/L64yocn6B_US_en_US"),
        ("Xero: Cash vs accrual accounting", "https://www.xero.com/us/guides/cash-vs-accrual-accounting/"),
        ("Zoho Books help: Manage reports", "https://www.zoho.com/us/books/help/reports/manage-reports.html"),
        ("FreshBooks support: What is a Profit and Loss report?", "https://support.freshbooks.com/hc/en-us/articles/219089507-What-is-a-Profit-and-Loss-report"),
        ("Wave support: Accrual vs. cash-basis reporting", "https://support.waveapps.com/hc/en-us/articles/360041245892-Accrual-vs-cash-basis-reporting"),
    ],
})


# ---------- Bank reconciliation (how-to)
# Worked example: a hypothetical business, computed here so the arithmetic always balances.
_br_stmt = 8450.00                       # bank statement ending balance, Mar 31
_br_dit = [("Mar 31", "Customer deposit made after the bank's cutoff", 1200.00)]
_br_oc = [("Check #1043", "Office rent", 650.00), ("Check #1045", "Supplier payment", 310.00)]
_br_fee, _br_int, _br_nsf = 25.00, 3.40, 480.00
_br_right, _br_wrong = 92.00, 29.00     # a $92 payment keyed into the books as $29 (transposed digits)
_br_err = _br_right - _br_wrong
_br_adj_bank = _br_stmt + sum(a for *_x, a in _br_dit) - sum(a for *_x, a in _br_oc)
_br_book = round(_br_adj_bank + _br_fee - _br_int + _br_nsf + _br_err, 2)  # book balance before adjustments
_br_adj_book = round(_br_book - _br_fee + _br_int - _br_nsf - _br_err, 2)
assert abs(_br_adj_bank - _br_adj_book) < 0.005
_br_f = lambda x: f"${x:,.2f}"
_br_rows = (f"<tr><td>Ending balance per bank statement</td><td>{_br_f(_br_stmt)}</td><td>Balance per books (general ledger)</td><td>{_br_f(_br_book)}</td></tr>"
            f"<tr><td>+ Deposit in transit</td><td>{_br_f(_br_dit[0][2])}</td><td>+ Interest earned, not yet recorded</td><td>{_br_f(_br_int)}</td></tr>"
            f"<tr><td>− Outstanding check #1043</td><td>{_br_f(_br_oc[0][2])}</td><td>− Bank service fee, not yet recorded</td><td>{_br_f(_br_fee)}</td></tr>"
            f"<tr><td>− Outstanding check #1045</td><td>{_br_f(_br_oc[1][2])}</td><td>− Customer check returned NSF</td><td>{_br_f(_br_nsf)}</td></tr>"
            f"<tr><td></td><td></td><td>− Payment recorded as {_br_f(_br_wrong)} instead of {_br_f(_br_right)}</td><td>{_br_f(_br_err)}</td></tr>"
            f"<tr><td><b>Adjusted bank balance</b></td><td><b>{_br_f(_br_adj_bank)}</b></td><td><b>Adjusted book balance</b></td><td><b>{_br_f(_br_adj_book)}</b></td></tr>")

# How each ranked tool reconciles, from vendor help and pricing pages (checked 2026-11-12); plan prices from data.
_br_plan = lambda tool, plan: (f"{plan.split(' (')[0]} ({p})" if (p := _ap_plan_price(tool, plan.split(' (')[0])) else plan.split(' (')[0])
_br_xauto = _ap_first("Xero", "Auto-reconcile") or ""
_br_xadd = re.search(r"\$([\d.]+)/mo", _br_xauto)
_br_zfeed = _ap_first("Zoho Books", "Bank feeds")
_br_fbplus = re.search(r"Plus \(\$(\d+)\)", _ac.get("freshbooks", {}).get("what", ""))
_br_tool = {
    "quickbooks": ("Reconcile tool: enter the statement's ending balance and date, tick cleared items until the difference is $0.00; transactions already matched in the bank feed arrive pre-ticked",
                   f"Bank connection included from {_br_plan('QuickBooks Online', 'Simple Start')}; the pricing page lists “Reconciles your books” from Plus"),
    "xero": ("Reconcile statement lines from the bank feed as they arrive, using suggested matches, bank rules and cash coding",
             f"Bank reconciliation on {_br_plan('Xero', 'Early')}; auto-reconcile on {_br_plan('Xero', _br_xauto)}"
             + (f", or as a {_fmt(float(_br_xadd.group(1)))}/mo add-on on Early" if _br_xadd else "")),
    "zohobooks": ("Reconcile Account: enter start date, end date and closing balance, select cleared transactions until the difference is zero; reconciliations can be undone",
                  f"Bank feeds from {_br_plan('Zoho Books', _br_zfeed)}" if _br_zfeed else "See the review for plan details"),
    "freshbooks": ("Match each bank transaction to a FreshBooks entry (with suggested Likely Matches), or Mark As transfer, owner's equity or refund; needs a connected bank and an opening balance",
                   "Bank Reconciliation on Plus" + (f" (${_br_fbplus.group(1)}/mo)" if _br_fbplus else "") + ", Premium and Select, not Lite"),
    "wave": ("Reconciliation page (web only): create a period with the statement's end date and closing balance, mark each matching transaction until the difference is zero",
             f"Automatic bank imports are part of Pro ({_ac['wave']['price']}), not the free Starter plan" if "wave" in _ac else ""),
}
_br_trs = "".join(f"<tr><td>{_ac_rv(k)}</td><td>{a}</td><td>{b}</td></tr>" for k, (a, b) in _br_tool.items() if k in _ac_ranked)

guide_page({
    "slug": "bank-reconciliation", "crumb": "Bank reconciliation", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-12", "kicker": "How-to",
    "title": "Bank Reconciliation: How to Reconcile a Bank Statement, Step by Step",
    "seo_title": "Bank Reconciliation: Steps, Example and Fixes | Vettlo",
    "desc": "Bank reconciliation explained: the 7 steps, a worked example with deposits in transit and outstanding checks, why balances don't match, and how to fix it.",
    "card": "The 7 steps, a worked example, common mismatches and how software automates it.",
    "answer": ("A bank reconciliation compares your bank statement with your own books for the same period and explains every difference until the two adjusted balances agree. "
               "You adjust the bank side for timing items the bank hasn't processed yet (deposits in transit, outstanding checks) and the book side for items only the bank knows about (fees, interest, returned checks) or your own errors. "
               "Do it at least monthly, as soon as each statement arrives."),
    "sections": [
        ("what", "What is a bank reconciliation?", f"""<p>Bank reconciliation is the monthly check that the cash balance in your accounting records matches what the bank says you have, once you account for items that one side has recorded and the other hasn't. The result is a short schedule, the <b>bank reconciliation statement</b>, that starts from both balances and ends at the same adjusted number.</p>
<p>Most tools in our <a href="{_ac_cat}">comparison of the best accounting software</a> include a reconciliation screen, and bank feeds do much of the matching. But the software can only match what's there: you still decide what each unmatched line is, which is what this guide covers.</p>
<p>The two balances rarely agree on their own, for three kinds of reasons:</p>
<ul><li><b>Timing:</b> you've recorded a deposit or written a check that hasn't reached the bank yet.</li>
<li><b>Bank-only items:</b> the bank charged a fee, paid interest or returned a customer's check, and you haven't entered it.</li>
<li><b>Errors:</b> a transaction was entered twice, skipped or keyed with the wrong amount, usually in the books, occasionally at the bank.</li></ul>
<p>Reconciling catches all three before they reach your financial statements or tax return, and it's one of the simplest ways to spot unauthorized withdrawals early.</p>"""),
        ("steps", "How do you do a bank reconciliation? 7 steps", f"""<p>Work from the bank statement and the cash account in your general ledger for the same dates. The steps are the same on paper, in a spreadsheet or in software:</p>
<ol>
<li><b>Get the statement and the ledger for the same period.</b> Note the statement's ending balance and date, and check that this period's opening balance equals last month's reconciled closing balance.</li>
<li><b>Tick off matching deposits.</b> Compare each deposit on the statement with deposits in your books. Anything in the books but not on the statement is a <b>deposit in transit</b>.</li>
<li><b>Tick off matching withdrawals.</b> Do the same for checks, card payments and transfers. Checks you've written that haven't cleared are <b>outstanding checks</b>.</li>
<li><b>Adjust the bank balance.</b> Statement ending balance + deposits in transit − outstanding checks ± bank errors = adjusted bank balance.</li>
<li><b>Find items only the bank has recorded.</b> Service fees, interest, returned (NSF) checks and automatic debits you didn't enter.</li>
<li><b>Adjust the book balance.</b> Book balance + interest and other credits − fees, returned checks and other charges ± your own errors = adjusted book balance. Record each of these as a journal entry or transaction in your books.</li>
<li><b>Compare, then document.</b> The two adjusted balances should be equal. Save the reconciliation report with the statement, and note any item you couldn't explain so you can follow it up.</li>
</ol>
<p>Only the book-side adjustments go into your ledger. Bank-side items are timing differences that clear on their own when the bank catches up, so you just carry them to next month's reconciliation.</p>"""),
        ("example", "Bank reconciliation example", f"""<p>Here's a full reconciliation for March. The business and figures are hypothetical, chosen to show each kind of reconciling item once:</p>
<div class="table-wrap"><table><thead><tr><th>Bank side</th><th>Amount</th><th>Book side</th><th>Amount</th></tr></thead><tbody>{_br_rows}</tbody></table></div>
<p>Both sides end at {_br_f(_br_adj_bank)}, so the account is reconciled. What each line means:</p>
<ul><li>The {_br_f(_br_dit[0][2])} deposit went to the bank after its cutoff on March 31; it will appear on April's statement.</li>
<li>Checks #1043 and #1045 ({_br_f(sum(a for *_x, a in _br_oc))} together) were mailed but not yet cashed.</li>
<li>The {_br_f(_br_fee)} fee and {_br_f(_br_int)} of interest appear only on the statement, so they're entered in the books now.</li>
<li>The {_br_f(_br_nsf)} customer check bounced; the deposit is reversed in the books and the customer owes you again.</li>
<li>A {_br_f(_br_right)} payment was recorded as {_br_f(_br_wrong)}, overstating the book balance by {_br_f(_br_err)}.</li></ul>
<p>That last difference, {_br_f(_br_err)}, divides evenly by 9 ({_br_f(_br_err)} ÷ 9 = {_br_f(_br_err / 9)}). When an unexplained difference is a multiple of 9, look for two swapped digits first.</p>"""),
        ("mismatch", "Why doesn't my bank reconciliation balance?", f"""<p>If the adjusted balances still differ, the cause is almost always one of a handful of problems. Check them in this order:</p>
<div class="table-wrap"><table><thead><tr><th>Symptom</th><th>Likely cause</th><th>Fix</th></tr></thead><tbody>
<tr><td>Off from the first line</td><td>Opening balance doesn't match last month's reconciled ending balance</td><td>Find the edited, deleted or back-dated transaction in a reconciled period and correct it</td></tr>
<tr><td>Difference equals one transaction</td><td>An item was left unticked or entered in the books twice</td><td>Search the ledger for that exact amount</td></tr>
<tr><td>Difference is twice one transaction</td><td>A deposit recorded as a withdrawal, or the reverse</td><td>Reverse the sign on that transaction</td></tr>
<tr><td>Difference divisible by 9</td><td>Transposed digits (92 entered as 29)</td><td>Compare amounts digit by digit</td></tr>
<tr><td>Bank feed shows a line twice</td><td>Duplicate import, often after reconnecting the bank</td><td>Delete the duplicate rather than matching it</td></tr>
<tr><td>Wrong ending date or balance</td><td>Statement figures keyed incorrectly</td><td>Re-enter both from the statement</td></tr>
<tr><td>Old outstanding check never clears</td><td>Lost, voided or stale check</td><td>Confirm with the payee, then void and reissue or record per your accountant's advice</td></tr>
</tbody></table></div>
<p>Avoid forcing a reconciliation with a plug entry. QuickBooks lets you finish with a difference and posts an adjusting entry for it, but Intuit's own help says it's usually best to resolve differences instead and to talk to your accountant first. Unpaid supplier bills don't belong here at all until they're paid; our <a href="/guides/accounts-payable-process/">accounts payable process guide</a> covers how those are tracked.</p>"""),
        ("software", "How does accounting software automate bank reconciliation?", f"""<p>Accounting software automates the matching, not the judgment. A <b>bank feed</b> imports transactions from your connected bank account; the software suggests a match against invoices, bills and payments you've already entered, and <b>bank rules</b> categorize repeat items such as a monthly subscription. You confirm or correct each suggestion, then run the reconciliation against the statement balance. Here's how the tools we rank do it, from each vendor's help and pricing pages, checked {hdate("2026-11-12")}:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>How reconciliation works</th><th>Plan notes</th></tr></thead><tbody>{_br_trs}</tbody></table></div>
<p>Two things to check before you buy. First, whether the entry plan includes the bank feed at all: Wave Starter and FreshBooks Lite don't include the automated workflow above. Second, whether your bank connects, which our shortlist's buying checklist also flags. For what each plan costs over a year, see the <a href="/guides/accounting-software-cost/">accounting software cost guide</a>; for two tools head to head, the <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> and <a href="/compare/xero-vs-zohobooks/">Xero vs Zoho Books</a> comparisons.</p>
<p>A practical habit: match the feed weekly so the month-end reconciliation is a final check against the statement rather than a month of catch-up.</p>"""),
        ("controls", "How often should you reconcile, and who should do it?", f"""<p>Reconcile every bank and credit card account at least monthly, soon after the statement closes, and have someone other than the person who handles cash review it. The Washington State Auditor's Office publishes best practices for the public entities it audits that apply just as well to a small business:</p>
<ul><li><b>Monthly at minimum,</b> with transactions recorded as they happen from source records, not keyed in from the bank statement at month end.</li>
<li><b>Separate duties:</b> the person reconciling shouldn't handle deposits, pay bills, run payroll, authorize transfers or sign on the account.</li>
<li><b>Documented review:</b> a supervisor reviews against the original statement or view-only online access, and signs and dates the review.</li>
<li><b>Deadlines for open items:</b> set a short window, such as two weeks, to research discrepancies. The auditor notes that many banks limit error corrections to 60 days after the transaction date, so old unexplained items can become unrecoverable.</li>
<li><b>Keep the evidence:</b> the statement, the reconciliation schedule and support for each reconciling item.</li></ul>
<p>In a very small business where one person does everything, the owner reviewing the statement and the reconciliation report each month is the practical version of that control. If you report on the cash basis, the reconciled bank balance also anchors your income figures; see <a href="/guides/cash-vs-accrual-accounting/">cash vs accrual accounting</a> for how the method changes what you record.</p>
<p class="small muted">This is general bookkeeping guidance, not accounting or legal advice. Your accountant may set different review steps for your business.</p>"""),
    ],
    "faqs": [
        ("What are the two sides of a bank reconciliation?", "The bank side starts from the statement's ending balance and adjusts for deposits in transit, outstanding checks and bank errors. The book side starts from your ledger balance and adjusts for fees, interest, returned checks and your own errors. The reconciliation is done when both adjusted balances are equal."),
        ("Do outstanding checks go on the bank side or the book side?", "The bank side. You've already recorded the check in your books; the bank just hasn't paid it yet, so you subtract it from the statement balance. No journal entry is needed, and it should clear on a later statement."),
        ("Do I need to reconcile if my accounting software has a bank feed?", "Yes. A bank feed imports and matches transactions, but it doesn't confirm that your ledger balance equals the statement balance. Duplicate imports, deleted transactions and entries made outside the feed only show up when you reconcile against the statement's ending balance."),
        ("How long does a bank reconciliation take?", "It depends on volume and how current your books are. An account with a bank feed that's matched weekly is usually a short final check at month end; an account several months behind can take hours because each month has to be reconciled in order, starting from the last reconciled balance."),
    ],
    "sources": [
        ("QuickBooks: Reconcile an account in QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-us/banking-topics/reconcile-accounts-in-quickbooks-online/00/186470"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
        ("Xero: Bank reconciliation (US)", "https://www.xero.com/us/features-and-tools/accounting-software/bank-reconciliation/"),
        ("Zoho Books help: Reconciliation", "https://www.zoho.com/en-sg/books/help/banking/reconciliation.md"),
        ("FreshBooks support: How do I reconcile simple transactions in bank reconciliation?", "https://support.freshbooks.com/hc/en-us/articles/360039682172"),
        ("Wave support: Reconcile your books", "https://support.waveapps.com/hc/en-us/articles/38599574877332"),
        ("Wave support: Import transactions automatically by connecting a bank account", "https://support.waveapps.com/hc/en-us/articles/208624076"),
        ("Washington State Auditor's Office: Best Practices for Bank Reconciliations (PDF)", "https://sao.wa.gov/sites/default/files/2023-05/Best-Practices-for-Bank-Reconciliations.pdf"),
    ],
})


# ---------- QuickBooks Desktop discontinued (explainer + migration)
# Desktop facts from Intuit help pages fetched 2026-11-13; QuickBooks Online plans, prices and user limits from data.
_qd_lad = _ac_lad.get("quickbooks", [])
_qd_first = dict((f, p) for f, p in _ac_depth.get(_ac["quickbooks"]["name"], {}).get("first_plan", []))
_qd_inv = _qd_first.get("Inventory tracking")
_qd_rows = "".join(f"<tr><td>{plan}</td><td>{_fmt(reg)}/mo</td><td>{us or 'Not stated'}</td><td>{_fmt(reg * 12)}</td></tr>" for plan, reg, mo, pr, us in _qd_lad)
_qd_lo = _qd_lad[0] if _qd_lad else None
_qd_hi = _qd_lad[-1] if _qd_lad else None

guide_page({
    "slug": "quickbooks-desktop-discontinued", "crumb": "QuickBooks Desktop discontinued", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-13", "kicker": "Migration guide",
    "title": "Is QuickBooks Desktop Being Discontinued? What Changed and What to Do",
    "seo_title": "QuickBooks Desktop Discontinued? Dates and Your Options | Vettlo",
    "desc": "QuickBooks Desktop discontinued? Not fully. What Intuit stopped selling in the US in 2024, what ends when a version sunsets, and how to move your data.",
    "card": "What Intuit actually stopped, what ends when a version sunsets, and how to move off Desktop.",
    "answer": ("QuickBooks Desktop isn't fully discontinued, but Intuit stopped selling new US subscriptions to Desktop Pro Plus, Premier Plus, Mac Plus and Enhanced Payroll after September 30, 2024. "
               "Existing subscribers can still renew and keep getting updates and support, and QuickBooks Desktop Enterprise is still sold. "
               "Separately, each Desktop version year is retired on its own date: QuickBooks Desktop 2023 lost payroll, online banking, live support and security updates after May 31, 2026."),
    "sections": [
        ("status", "Is QuickBooks Desktop discontinued?", f"""<p>No, not as a whole. "QuickBooks Desktop discontinued" usually refers to Intuit's 2024 decision to stop selling most Desktop editions to <b>new</b> customers in the United States. Intuit says the change applies to the US only and doesn't affect existing subscribers, who keep security updates, product updates and support.</p>
<p>If you're weighing a move to the cloud, our <a href="{_ac_cat}">ranking of the best accounting software</a> compares the alternatives on regular price and plan limits. This guide covers what changed, what it means for a Desktop file you already have, and how the move works. Here's the status of each edition, from Intuit's help pages checked {hdate("2026-11-13")}:</p>
<div class="table-wrap"><table><thead><tr><th>Edition</th><th>New US subscribers</th><th>Existing subscribers</th></tr></thead><tbody>
<tr><td>QuickBooks Desktop Pro Plus</td><td>Not sold after Sept. 30, 2024</td><td>Can keep renewing</td></tr>
<tr><td>QuickBooks Desktop Premier Plus</td><td>Not sold after Sept. 30, 2024</td><td>Can keep renewing</td></tr>
<tr><td>QuickBooks Desktop Mac Plus</td><td>Not sold after Sept. 30, 2024</td><td>Can keep renewing</td></tr>
<tr><td>QuickBooks Desktop Enhanced Payroll</td><td>Not sold after Sept. 30, 2024</td><td>Can keep renewing</td></tr>
<tr><td>QuickBooks Desktop Enterprise</td><td>Still sold (Silver, Gold, Platinum and Diamond)</td><td>Can keep renewing</td></tr>
<tr><td>Lifetime or perpetual Pro, Premier and Mac licenses</td><td>No longer offered</td><td>Subject to the version sunset below</td></tr>
</tbody></table></div>
<p>Intuit marks renewal availability as subject to change without notice. It also warns that sellers offering new Desktop Plus subscriptions or non-subscription Pro, Premier or Mac licenses may be selling fake software, and asks customers to report them on 1-800-4-INTUIT.</p>"""),
        ("sunset", "What happens when a QuickBooks Desktop version is discontinued?", f"""<p>When a version year reaches its discontinuation date, the software loses every connected service Intuit runs for it. This is a separate, recurring event from the 2024 stop-sell: it applies to each version year, whether you bought a license or a subscription.</p>
<p>The most recent example is QuickBooks Desktop 2023 (Pro Plus, Premier Plus, Enterprise Solutions 23.0 and the Accountant editions). Intuit's service discontinuation notice says that after May 31, 2026 these stop working with the 2023 software:</p>
<ul><li><b>Payroll:</b> Desktop Assisted, Basic, Standard and Enhanced Payroll, and QuickBooks Workforce.</li>
<li><b>Payments:</b> credit card and check processing, Merchant Service Deposit reconciliation and e-invoicing.</li>
<li><b>Online banking and backup:</b> transaction downloads, online payments and transfers, and Online Backup.</li>
<li><b>Live technical support.</b></li>
<li><b>Connected features:</b> Accountant Copy Transfer, Contributed Reports, multi-currency, email from the product and Shipping Manager.</li>
<li><b>Critical security updates,</b> which stopped June 1, 2026.</li></ul>
<p>Intuit says it notifies customers in advance before an older version is discontinued, but its notice doesn't give a fixed support period or a date for later versions. If you subscribe to Desktop Plus or Enterprise, moving to the newest version year is included at no extra cost, so the practical fix for a sunset is usually to upgrade inside the subscription. A one-time license holder has no upgrade path now that perpetual licenses aren't sold.</p>"""),
        ("data", "What happens to your data if you cancel QuickBooks Desktop Plus?", f"""<p>You keep read-only access for 12 months after the subscription ends, which is your window to export what you need. According to Intuit's Desktop FAQ:</p>
<ol>
<li><b>The cancellation takes effect at your next renewal date,</b> and you can use the product normally until then.</li>
<li><b>After it expires, you get 12 months of view-only access.</b> You can open the file and export data, but you can't edit it.</li>
<li><b>View-only access needs a recent version:</b> Desktop Plus for Windows 2023 R3 or newer, or Mac Plus 2024 or newer. Update before you cancel.</li>
<li><b>Support, Data Recovery, Intuit Data Protect and editing end</b> with the subscription.</li>
<li><b>Desktop Payroll and Desktop Payments aren't canceled automatically.</b> Cancel or move them separately so you aren't billed for services you no longer use.</li>
</ol>
<p>Before cancelling, keep a local backup (.QBB) of the company file and export the reports your accountant will want for past tax years, such as the general ledger, trial balance and payroll summaries. If you upgrade from Plus to Enterprise instead, Intuit says you can request a prorated refund for the Plus subscription.</p>"""),
        ("options", "What are your options if you're on QuickBooks Desktop?", f"""<p>You have four realistic paths: renew Desktop Plus, move up to Desktop Enterprise, convert to QuickBooks Online, or switch to a different cloud accounting tool. Which one fits depends mostly on whether you rely on Desktop-only workflows and how much history you need to keep editable.</p>
<div class="table-wrap"><table><thead><tr><th>Option</th><th>When it fits</th><th>What to check</th></tr></thead><tbody>
<tr><td>Keep renewing Desktop Plus</td><td>The software works for you and you already subscribe</td><td>Upgrade to each new version year before the old one sunsets; renewal terms can change</td></tr>
<tr><td>Upgrade to Desktop Enterprise</td><td>You need to stay on Desktop and want a product Intuit still sells to new customers</td><td>Price is higher; Intuit says data stays on the same platform with the same interface</td></tr>
<tr><td>Convert to QuickBooks Online</td><td>You want the cloud and want Intuit's own migration tool</td><td>Not everything migrates; plan size depends on users and features such as inventory</td></tr>
<tr><td>Switch to another cloud tool</td><td>QuickBooks Online's regular price or user limits don't suit you</td><td>How the vendor imports a Desktop file, and how much history you can bring</td></tr>
</tbody></table></div>
<p>If you convert to QuickBooks Online, the plan is chosen mainly by user count. Regular US prices from Intuit's pricing page, as in our {_ac_rv("quickbooks")} review:</p>
<div class="table-wrap"><table><thead><tr><th>QuickBooks Online plan</th><th>Regular price</th><th>Users</th><th>Per year</th></tr></thead><tbody>{_qd_rows}</tbody></table></div>
<p class="small muted">Regular prices, not the introductory discount for new customers. Accountant users are extra to the user counts shown.{f" Inventory tracking starts on {_qd_inv}." if _qd_inv else ""}</p>
<p>If QuickBooks Online doesn't fit, our <a href="/tools/best-quickbooks-alternatives/">QuickBooks alternatives shortlist</a> covers what each competitor gains and gives up, and the <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero comparison</a> goes deeper on the most common switch. For a full-year budget across vendors, see <a href="/guides/accounting-software-cost/">how much accounting software costs</a>.</p>"""),
        ("migrate", "How do you move from QuickBooks Desktop to QuickBooks Online?", f"""<p>Intuit's migration takes three stages: prepare the Desktop file, run the migration tool, then compare reports in both systems. You have 90 days from signing up for QuickBooks Online to import your Desktop data (180 days if your accountant does it), so convert early in the subscription. The steps, from Intuit's US help article updated {hdate("2026-11-05")}:</p>
<ol>
<li><b>Update QuickBooks Desktop</b> to the latest release, and make sure you're an admin on both the Desktop file and the QuickBooks Online account, set up in the same country.</li>
<li><b>Check the file's size.</b> Press F2 or Ctrl+1 to open Product Information and find Total Targets. If the file is over Intuit's limit, condense it, or choose the option that brings over lists and current balances without full transaction history.</li>
<li><b>Verify and rebuild the data,</b> and keep a local copy of the company file.</li>
<li><b>Close out banking.</b> Reconcile bank and credit card accounts and clear the bank feed queue, because bank feeds don't move. Our <a href="/guides/bank-reconciliation/">bank reconciliation guide</a> walks through the steps.</li>
<li><b>Save a Sales Tax Liability report</b> so you can confirm sales tax balances after the move.</li>
<li><b>Plan payroll.</b> Payroll data moves to QuickBooks Workforce; finish the migration at least 7 business days before your next payroll date.</li>
<li><b>Run the migration</b> with the tool inside QuickBooks Desktop for Windows, the browser-based tool (upload a .QBW, .QBM or .QBB file), or the export from QuickBooks Desktop for Mac 2020 or newer.</li>
<li><b>Choose carefully if the Online company already has data.</b> Replacing it can't be undone; use a new QuickBooks Online company if you want to keep what's there.</li>
<li><b>Compare the results.</b> After the "Your company is now online" email, run the profit and loss and balance sheet for the same dates in both systems and investigate any difference.</li>
</ol>
<p>Intuit says some data won't migrate and keeps a separate list of what doesn't carry over, so check it against the features you use most before you commit. Keep the Desktop file (and, if you cancel, its 12 months of view-only access) as the record of your pre-migration history.</p>
<p class="small muted">This is general guidance, not accounting or tax advice. Ask your accountant which historical reports to keep for your tax filings.</p>"""),
    ],
    "faqs": [
        ("Can I still buy QuickBooks Desktop?", "New US customers can buy QuickBooks Desktop Enterprise, which Intuit sells in Silver, Gold, Platinum and Diamond tiers. Desktop Pro Plus, Premier Plus, Mac Plus and Enhanced Payroll haven't been sold to new US subscribers since September 30, 2024, and Intuit no longer offers lifetime or perpetual Pro, Premier or Mac licenses."),
        ("Is QuickBooks Desktop Enterprise being discontinued?", "No. Intuit's help pages say Enterprise wasn't affected by the 2024 stop-sell and can still be bought or renewed by phone or online. Like every Desktop product, each Enterprise version year still has its own service discontinuation date, as Enterprise Solutions 23.0 did on May 31, 2026."),
        ("Will QuickBooks Desktop 2023 still open after support ended?", "Intuit's notice lists what stopped after May 31, 2026, including payroll, payments, online banking, live support and critical security updates from June 1, 2026. It doesn't say the software stops opening, but running accounting software without security updates or bank downloads is a risk; subscribers can upgrade to a newer version at no extra cost."),
        ("How long do I have to move Desktop data into QuickBooks Online?", "Intuit gives you 90 days from when you sign up for QuickBooks Online to import a Desktop company file, or 180 days if an accountant does the import. If the QuickBooks Online company already has data, importing replaces it and can't be undone."),
    ],
    "sources": [
        ("QuickBooks: Can't buy QuickBooks Desktop as a new US subscriber", "https://quickbooks.intuit.com/learn-support/en-us/help-article/new-subscriptions/us-quickbooks-desktop-sold-july-2024/L5lkQNq7L_US_en_US"),
        ("QuickBooks: Common QuickBooks Desktop questions", "https://quickbooks.intuit.com/learn-support/en-us/help-article/new-subscriptions/common-quickbooks-desktop-questions/L6qndvmPy_US_en_US"),
        ("QuickBooks blog: QuickBooks Desktop stop-sell", "https://quickbooks.intuit.com/r/whats-new/quickbooks-desktop-stop-sell/"),
        ("QuickBooks: QuickBooks Desktop 2023 service discontinuation policy", "https://quickbooks.intuit.com/learn-support/en-us/help-articles/quickbooks-desktop-service-discontinuation-disco-policy-and/00/262471"),
        ("QuickBooks: Move your QuickBooks Desktop company file to QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-us/help-article/import-export-data-files/move-quickbooks-desktop-file-quickbooks-online/L6af3Z0Fb_US_en_US"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
    ],
})


# ---------- What is accounts receivable? (AR, aging, DSO, collections)
# Hypothetical AR book for one small service business, as of Nov 30, 2026. Days past due, buckets and DSO are computed here.
import datetime as _ar_dt
_ar_asof = _ar_dt.date(2026, 11, 30)
_ar_inv = [  # (invoice, customer, amount, due date)
    ("INV-1048", "Customer A", 2400, _ar_dt.date(2026, 12, 10)),
    ("INV-1041", "Customer B", 1800, _ar_dt.date(2026, 11, 15)),
    ("INV-1033", "Customer C", 3200, _ar_dt.date(2026, 10, 20)),
    ("INV-1027", "Customer D", 950, _ar_dt.date(2026, 9, 25)),
    ("INV-1009", "Customer E", 600, _ar_dt.date(2026, 7, 31)),
]
_ar_buckets = ["Current", "1-30 days", "31-60 days", "61-90 days", "Over 90 days"]


def _ar_bucket(days):
    return 0 if days <= 0 else 1 if days <= 30 else 2 if days <= 60 else 3 if days <= 90 else 4


_ar_tot = sum(a for _i, _c, a, _d in _ar_inv)
_ar_by = [0] * 5
_ar_rows = ""
for _i, _c, _a, _d in _ar_inv:
    _late = (_ar_asof - _d).days
    _b = _ar_bucket(_late)
    _ar_by[_b] += _a
    _ar_rows += f"<tr><td>{_c}</td><td>{_d.strftime('%b')} {_d.day}</td><td>{max(_late, 0) or '—'}</td>" + "".join(f"<td>{_fmt(_a) if j == _b else ''}</td>" for j in range(5)) + "</tr>"
_ar_rows += "<tr><td><b>Total</b></td><td></td><td></td>" + "".join(f"<td><b>{_fmt(v) if v else '—'}</b></td>" for v in _ar_by) + "</tr>"
_ar_rows += "<tr><td><b>Share of AR</b></td><td></td><td></td>" + "".join(f"<td>{v / _ar_tot * 100:.0f}%</td>" for v in _ar_by) + "</tr>"
_ar_over60 = _ar_by[3] + _ar_by[4]
_ar_over60_pct = _ar_over60 / _ar_tot * 100
_ar_pastdue = _ar_tot - _ar_by[0]

# DSO and AR turnover for the quarter ending on the aging date (hypothetical figures)
_ar_begin, _ar_end, _ar_sales, _ar_terms = 7450, _ar_tot, 18000, 30
_ar_days = (_ar_asof - _ar_dt.date(2026, 9, 1)).days + 1
_ar_avg = (_ar_begin + _ar_end) / 2
_ar_dso = _ar_avg / _ar_sales * _ar_days
_ar_turn = _ar_sales / _ar_avg

# Invoicing on each ranked tool's entry plans, from the category data and data/review_depth.json
_ar_src_date = (re.search(r"on (\w+ \d+, \d{4})", ACC["price_footnote"]) or [None, ""])[1]
_xe = None
_ar_soft = []  # (tool link, plan, regular price, invoicing notes)
if "quickbooks" in _ap_name and _ap_name["quickbooks"] in _ac_depth:
    _q = _ac_depth[_ap_name["quickbooks"]]["plans"][0]
    if "invoicing and payments" in _q[2] and (_qp := _ap_plan_price(_ap_name["quickbooks"], _q[0])):
        _ar_soft.append((_ac_rv("quickbooks"), _q[0], _qp, f"Invoicing and online payments; {_q[2].split(';')[0]}"))
if "xero" in _ap_name and _ap_name["xero"] in _ac_depth:
    _xe = _ap_limit("Xero", "Invoices (approve and send)", "Early")
    _xpay = _ap_first("Xero", "Online invoice payments")
    _xg = next((c for c in _ac_depth["Xero"]["limits"]["cols"] if _ap_limit("Xero", "Invoices (approve and send)", c) == "Unlimited"), None)
    if _xe and (_xp := _ap_plan_price("Xero", "Early")):
        _ar_soft.append((_ac_rv("xero"), "Early", _xp, f"{_xe} invoices a month" + ("; online invoice payments included" if _xpay and _xpay.startswith("Early") else "")))
    if _xg and (_xgp := _ap_plan_price("Xero", _xg)):
        _ar_soft.append((_ac_rv("xero"), _xg, _xgp, "Unlimited invoices"))
if "zohobooks" in _ap_name and _ap_name["zohobooks"] in _ac_depth:
    for _zp in ("Free", "Standard"):
        _zl = _ap_limit("Zoho Books", "Invoices per year", _zp)
        _zd = next((d for p, _s, d in _ac_depth["Zoho Books"]["plans"] if p == _zp), "")
        _zprice = "Free" if _zp == "Free" else _ap_plan_price("Zoho Books", _zp)
        if _zl and _zprice:
            _zcap = re.search(r"revenue under \$[\d,.]+K?", _zd)
            _ar_soft.append((_ac_rv("zohobooks"), _zp, _zprice, f"{_zl} invoices a year" + (f"; only for {_zcap.group(0)}" if _zcap else "")))
if "freshbooks" in _ac:
    _fb = _ac["freshbooks"]
    _fbc = re.search(r"(\d+) billable clients", _fb["price_note"])
    if _fbc and _money(_fb["price"]):
        _ar_soft.append((_ac_rv("freshbooks"), "Lite", _fb["price"], f"Invoices up to {_fbc.group(1)} billable clients"))
if "wave" in _ac:
    _wv = _ac["wave"]
    if re.search(r"free invoicing", _wv["what"], re.I):
        _ar_soft.append((_ac_rv("wave"), "Starter", "Free", "Invoicing; card processing fees when customers pay online"))
    if "payment reminders" in _wv["what"] and _money(_wv["price"]):
        _ar_soft.append((_ac_rv("wave"), "Pro", _wv["price"], "Adds payment reminders"))
_ar_soft_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in _ar_soft)

guide_page({
    "slug": "accounts-receivable", "crumb": "Accounts receivable", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-14", "kicker": "How-to",
    "title": "What Is Accounts Receivable? How to Manage AR and Get Paid Faster",
    "seo_title": "Accounts Receivable: What It Is and How to Manage It | Vettlo",
    "desc": "Accounts receivable explained: how AR is recorded, how to read an aging report, how to calculate DSO, and a follow-up schedule to collect late invoices.",
    "card": "What AR is, an aging report and DSO worked out, and how to collect late invoices.",
    "answer": ("Accounts receivable (AR) is the money customers owe a business for goods or services it has already delivered and invoiced, recorded as a current asset on the balance sheet. "
               "Managing AR means invoicing promptly with clear terms, applying each payment to its invoice, reviewing an aging report every month, and following up on a fixed schedule so overdue invoices don't drift past 90 days."),
    "sections": [
        ("what", "What is accounts receivable?", f"""<p>Accounts receivable is the running total of invoices your customers haven't paid yet. When you finish a job or ship an order and send an invoice with net 30 terms, that amount sits in accounts receivable until the customer pays. In most small businesses AR is the invoicing or sales module of the accounting software; our <a href="{_ac_cat}">ranking of the best accounting software</a> compares {len(_ac_ranked)} tools, while this guide covers how to run receivables day to day.</p>
<p>AR is a <b>current asset</b> because you expect to turn it into cash within a year, usually within weeks. Its mirror image is the bills you owe suppliers, covered in our <a href="/guides/accounts-payable-process/">accounts payable process guide</a>.</p>
<h3>How is accounts receivable recorded?</h3>
<p>Under accrual accounting each invoice creates two journal entries: one when you bill and one when the customer pays. With a {_fmt(_ar_inv[2][2])} invoice as the example:</p>
<div class="table-wrap"><table><thead><tr><th>Event</th><th>Debit</th><th>Credit</th><th>Effect on AR</th></tr></thead><tbody>
<tr><td>Invoice sent</td><td>Accounts receivable {_fmt(_ar_inv[2][2])}</td><td>Sales revenue {_fmt(_ar_inv[2][2])}</td><td>Up {_fmt(_ar_inv[2][2])}</td></tr>
<tr><td>Customer pays</td><td>Cash {_fmt(_ar_inv[2][2])}</td><td>Accounts receivable {_fmt(_ar_inv[2][2])}</td><td>Down {_fmt(_ar_inv[2][2])}</td></tr>
</tbody></table></div>
<p>So AR carries a debit balance. Revenue is earned when you invoice; the payment only swaps one asset (AR) for another (cash). A business on the cash method doesn't book revenue until the money arrives, so it has no AR balance in its ledger, though it still needs an open-invoices list to chase payments. Our <a href="/guides/cash-vs-accrual-accounting/">cash vs accrual accounting guide</a> explains which method fits your business.</p>"""),
        ("process", "What are the steps in the accounts receivable process?", f"""<p>The AR process runs from agreeing terms with a customer to closing out the payment. Seven steps cover it:</p>
<ol>
<li><b>Agree credit terms before the work starts.</b> Put the payment term (due on receipt, net 15, net 30), any late fee and accepted payment methods in the quote or contract. For a new customer with a large order, consider a deposit.</li>
<li><b>Invoice as soon as the work is delivered.</b> Every day you wait to send the invoice is a day added to when you get paid. Include the invoice number, date, due date, a line-by-line description, the purchase order number if the customer uses one, and where to pay.</li>
<li><b>Make paying easy.</b> An online payment link on the invoice (card or ACH) removes the check-in-the-mail step. Card payments carry processing fees, so decide whether you absorb them.</li>
<li><b>Apply each payment to its invoice.</b> Record who paid, the amount and the invoice it settles. Partial payments and lump sums covering several invoices are where AR records drift out of date.</li>
<li><b>Match deposits to the bank.</b> Check that recorded payments actually landed in the bank account; our <a href="/guides/bank-reconciliation/">bank reconciliation guide</a> walks through that monthly check.</li>
<li><b>Follow up on a fixed schedule.</b> Send reminders before and after the due date, then escalate (see the collection schedule below).</li>
<li><b>Review the aging report monthly.</b> Look at what's past due, who owes it and how long it's been outstanding, and decide what to chase, renegotiate or write off.</li>
</ol>"""),
        ("aging", "What is an accounts receivable aging report?", f"""<p>An AR aging report lists every unpaid invoice and sorts it into buckets by how many days it is past its due date. It shows at a glance how much of your receivables is current and how much is getting old, and older invoices are less likely to be collected.</p>
<p>Here's a hypothetical aging report for a small service business on {_ar_asof.strftime('%B')} {_ar_asof.day}, {_ar_asof.year}, with five open invoices:</p>
<div class="table-wrap"><table><thead><tr><th>Customer</th><th>Due</th><th>Days late</th>{"".join(f"<th>{b}</th>" for b in _ar_buckets)}</tr></thead><tbody>{_ar_rows}</tbody></table></div>
<p>Total receivables are {_fmt(_ar_tot)}, of which {_fmt(_ar_pastdue)} is past due. The number to act on is the {_fmt(_ar_over60)} ({_ar_over60_pct:.0f}%) more than 60 days late. How to read it:</p>
<ul>
<li><b>Current and 1-30 days:</b> routine. A reminder usually settles these.</li>
<li><b>31-60 days:</b> call the customer. Ask whether the invoice was received, whether anything is disputed, and when it will be paid.</li>
<li><b>61-90 days and over:</b> pause new work on credit for that customer, agree a payment plan in writing, and decide whether to send it to a collection agency.</li>
</ul>
<p>Accounting software builds this report from your open invoices; it's usually called "A/R aging summary" or "aged receivables." Run it on the same day each month so the buckets compare.</p>"""),
        ("dso", "How do you calculate days sales outstanding (DSO)?", f"""<p>Days sales outstanding (DSO) is the average number of days it takes to collect payment after a credit sale. The formula is average accounts receivable ÷ credit sales for the period × the number of days in the period.</p>
<p>Continuing the example for the quarter from September 1 to {_ar_asof.strftime('%B')} {_ar_asof.day} ({_ar_days} days):</p>
<div class="table-wrap"><table><thead><tr><th>Figure</th><th>Value</th></tr></thead><tbody>
<tr><td>AR at the start of the quarter</td><td>{_fmt(_ar_begin)}</td></tr>
<tr><td>AR at the end of the quarter (aging report total)</td><td>{_fmt(_ar_end)}</td></tr>
<tr><td>Average AR</td><td>{_fmt(_ar_avg)}</td></tr>
<tr><td>Credit sales in the quarter</td><td>{_fmt(_ar_sales)}</td></tr>
<tr><td><b>DSO</b> ({_fmt(_ar_avg)} ÷ {_fmt(_ar_sales)} × {_ar_days})</td><td><b>{_ar_dso:.0f} days</b></td></tr>
<tr><td>AR turnover ({_fmt(_ar_sales)} ÷ {_fmt(_ar_avg)})</td><td>{_ar_turn:.1f} times in the quarter</td></tr>
</tbody></table></div>
<p>The business invoices on net {_ar_terms} terms, so a DSO of {_ar_dso:.0f} days means customers pay about {_ar_dso - _ar_terms:.0f} days late on average. Use only credit sales, not cash sales, or DSO looks better than it is. Track DSO every month: a rising number warns you about cash flow before the bank balance does.</p>
<p>AR turnover is the same information the other way round: how many times average receivables were collected in the period. Higher turnover means faster collection.</p>"""),
        ("collect", "How do you collect overdue invoices?", f"""<p>Collect overdue invoices with a written schedule that starts before the due date and escalates in steps, so every customer is treated the same and nothing waits for someone to remember. A schedule for net {_ar_terms} terms:</p>
<div class="table-wrap"><table><thead><tr><th>When</th><th>Action</th></tr></thead><tbody>
<tr><td>3-5 days before due</td><td>Friendly reminder with the invoice attached and the payment link</td></tr>
<tr><td>Due date</td><td>Reminder that payment is due today</td></tr>
<tr><td>7 days late</td><td>Second reminder; ask whether anything is holding the invoice up</td></tr>
<tr><td>15-30 days late</td><td>Phone call to the person who approves payment; agree a pay date and confirm it by email</td></tr>
<tr><td>45-60 days late</td><td>Formal letter; apply the late fee if your terms include one; stop new work on credit</td></tr>
<tr><td>90+ days late</td><td>Final notice, then a collection agency, small claims court or write-off</td></tr>
</tbody></table></div>
<p>Accounting software with scheduled payment reminders can send the first three automatically; check which plan includes them before you rely on it.</p>
<h3>What happens when an invoice can't be collected?</h3>
<p>An invoice you won't collect becomes a <b>bad debt</b>. Many businesses that report on the accrual basis estimate likely losses ahead of time with an <b>allowance for doubtful accounts</b>, a contra-asset that reduces AR on the balance sheet; others use the direct write-off method and remove the invoice when it's clearly uncollectible. Your accountant will say which your books need.</p>
<p>For taxes, the IRS treats credit sales to customers as a business bad debt that you can deduct when it becomes partly or totally worthless, but only if the amount was included in your income in the current or a prior year. That's why cash-method businesses generally can't deduct unpaid invoices: the income was never reported. Sole proprietors claim it on Schedule C (Form 1040).</p>
<p class="small muted">This summarizes IRS Topic 453 and isn't tax advice; ask your accountant before writing off a receivable.</p>"""),
        ("software", "Which accounting plans include invoicing and payment reminders?", f"""<p>For the {len({r[0] for r in _ar_soft})} tools in our ranking with published prices, the entry plans differ in how many invoices or clients they allow and whether customers can pay online. What each entry plan includes for receivables, at regular prices:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Plan</th><th>Regular price</th><th>Invoicing on this plan</th></tr></thead><tbody>{_ar_soft_rows}</tbody></table></div>
<p class="small muted">Regular US prices from each vendor's pricing page{f", checked {_ar_src_date}" if _ar_src_date else ""}; QuickBooks, Xero and Zoho Books plan details checked {_ap_checked_h}. Introductory discounts aren't shown.</p>
<p>The invoice cap matters most: {f"Xero Early's {_xe}-invoice monthly limit" if _xe else "a monthly invoice limit"} is easy to hit for a business that bills many small jobs. Our <a href="/guides/accounting-software-cost/">accounting software cost guide</a> prices every plan by team size, and <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> and <a href="/compare/xero-vs-zohobooks/">Xero vs Zoho Books</a> compare the most common choices plan by plan.</p>"""),
    ],
    "faqs": [
        ("Is accounts receivable an asset?", "Yes. Accounts receivable is a current asset on the balance sheet because the business expects to collect it in cash within a year. Uncollectible amounts are reduced through an allowance for doubtful accounts or written off."),
        ("Is accounts receivable a debit or a credit?", "Accounts receivable normally carries a debit balance. Sending an invoice debits AR and credits revenue; when the customer pays, cash is debited and AR is credited."),
        ("What is a good days sales outstanding (DSO)?", f"Compare DSO with your own payment terms. On net {_ar_terms} terms, a DSO close to {_ar_terms} days means customers pay roughly on time; a DSO well above it means invoices are paid late on average, and a rising trend is an early warning for cash flow."),
        ("Can I write off unpaid invoices on my taxes?", "Only if the income was reported. The IRS lets businesses deduct a business bad debt, including credit sales to customers, when it becomes partly or totally worthless and the amount was included in income in the current or a prior year. Cash-method businesses generally can't deduct unpaid invoices. This isn't tax advice."),
    ],
    "sources": [
        ("IRS: Topic no. 453, Bad debt deduction", "https://www.irs.gov/taxtopics/tc453"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
        ("Xero US pricing plans", "https://www.xero.com/us/pricing-plans/"),
        ("Zoho Books pricing (US)", "https://www.zoho.com/us/books/pricing/"),
        ("FreshBooks", _ac["freshbooks"]["url"] if "freshbooks" in _ac else "https://www.freshbooks.com/"),
        ("Wave", _ac["wave"]["url"] if "wave" in _ac else "https://www.waveapps.com/"),
    ],
})


# ---------- Chart of accounts (what it is, numbering, sample chart, software defaults)
# Sample chart is a hypothetical service business. Schedule C line labels from the 2025 Schedule C (Form 1040) PDF,
# QuickBooks/Xero/Zoho Books behavior from vendor help pages, all fetched 2026-11-15. Plan prices and class limits from data.
_ca_types = [  # (type, range, statement, normal balance, what it holds)
    ("Assets", "1000-1999", "Balance sheet", "Debit", "What the business owns or is owed: bank accounts, receivables, equipment"),
    ("Liabilities", "2000-2999", "Balance sheet", "Credit", "What it owes: bills, credit cards, sales tax collected, loans"),
    ("Equity", "3000-3999", "Balance sheet", "Credit", "The owner's stake: money put in, draws taken out, profit kept"),
    ("Revenue", "4000-4999", "Profit and loss", "Credit", "Income from selling goods or services"),
    ("Expenses", "5000-6999", "Profit and loss", "Debit", "Costs of running the business, from contractors to rent"),
]
_ca_chart = [  # (number, account, type, 2025 Schedule C line or "")
    (1000, "Business checking", "Assets", ""), (1010, "Business savings", "Assets", ""),
    (1100, "Accounts receivable", "Assets", ""), (1200, "Prepaid expenses", "Assets", ""),
    (1500, "Computer equipment", "Assets", ""), (1510, "Accumulated depreciation (contra-asset)", "Assets", ""),
    (2000, "Accounts payable", "Liabilities", ""), (2100, "Business credit card", "Liabilities", ""),
    (2200, "Sales tax payable", "Liabilities", ""), (2300, "Payroll liabilities", "Liabilities", ""),
    (2700, "Equipment loan", "Liabilities", ""),
    (3000, "Owner's contributions", "Equity", ""), (3100, "Owner's draws (contra-equity)", "Equity", ""),
    (3900, "Retained earnings", "Equity", ""),
    (4000, "Consulting revenue", "Revenue", "1 Gross receipts or sales"), (4100, "Project fees", "Revenue", "1 Gross receipts or sales"),
    (4900, "Refunds and allowances given", "Revenue", "2 Returns and allowances"),
    (5000, "Subcontractors", "Expenses", "11 Contract labor"),
    (6000, "Advertising and marketing", "Expenses", "8 Advertising"),
    (6050, "Vehicle expenses", "Expenses", "9 Car and truck expenses"),
    (6100, "Business insurance", "Expenses", "15 Insurance (other than health)"),
    (6150, "Accounting and legal fees", "Expenses", "17 Legal and professional services"),
    (6200, "Office supplies and software", "Expenses", "18 Office expense"),
    (6250, "Office rent", "Expenses", "20b Rent or lease: other business property"),
    (6300, "Repairs and maintenance", "Expenses", "21 Repairs and maintenance"),
    (6350, "Business licenses and taxes", "Expenses", "23 Taxes and licenses"),
    (6400, "Travel", "Expenses", "24a Travel"),
    (6450, "Business meals", "Expenses", "24b Deductible meals"),
    (6500, "Utilities and phone", "Expenses", "25 Utilities"),
    (6600, "Wages", "Expenses", "26 Wages (less employment credits)"),
    (6650, "Depreciation expense", "Expenses", "13 Depreciation and section 179"),
    (6900, "Bank fees and other expenses", "Expenses", "27b Other expenses"),
]
_ca_rows = "".join(f"<tr><td>{n}</td><td>{a}</td><td>{t}</td><td>{s or '—'}</td></tr>" for n, a, t, s in _ca_chart)
_ca_n = len(_ca_chart)
_ca_cnt = {t: sum(1 for _n, _a, tt, _s in _ca_chart if tt == t) for t, *_r in _ca_types}
_ca_sched = len({s.split(" ")[0] for _n, _a, t, s in _ca_chart if s and t == "Expenses"})
_ca_type_rows = "".join(f"<tr><td><b>{t}</b></td><td>{r}</td><td>{st}</td><td>{nb}</td><td>{w}</td></tr>" for t, r, st, nb, w in _ca_types)
_ca_qb = _ap_name.get("quickbooks", "QuickBooks Online")
_ca_qb_adv = _ap_plan_price(_ca_qb, "Advanced")
_ca_qb_plus = _ap_plan_price(_ca_qb, "Plus")
_ca_qb_cls = _ap_limit(_ca_qb, "Classes and locations", "Plus")
_ca_has = lambda k: k in _ac_ranked
_ca_soft_rows = ""
if _ca_has("quickbooks"):
    _ca_soft_rows += (f"<tr><td>{_ac_rv('quickbooks')}</td><td>Built for your business entity when you create the company</td>"
                      f"<td>Account type plus a detail type; account numbers optional</td>"
                      f"<td>250 active accounts on Simple Start, Essentials and Plus; unlimited on Advanced{f' ({_ca_qb_adv})' if _ca_qb_adv else ''}</td>"
                      "<td>Make unused accounts inactive; inactive accounts don't count toward the limit</td>"
                      "<td>Spreadsheet import (opening balances added afterward)</td></tr>")
if _ca_has("xero"):
    _ca_soft_rows += (f"<tr><td>{_ac_rv('xero')}</td><td>Default chart for your industry or business type</td>"
                      "<td>Xero's guide suggests 1000-5999 number ranges by type; tracking categories for departments and projects</td><td>No account cap listed</td>"
                      "<td>Archive accounts that have transactions instead of deleting them</td><td>Not stated in the Xero guide we checked</td></tr>")
if _ca_has("zohobooks"):
    _ca_soft_rows += (f"<tr><td>{_ac_rv('zohobooks')}</td><td>Set of default accounts grouped under assets, liability, equity, income and expense</td>"
                      "<td>Unique account code of up to 50 characters</td><td>No account cap listed</td>"
                      "<td>System default accounts can't be deleted or made inactive; accounts with transactions can't be deleted</td>"
                      "<td>CSV, TSV or XLS file up to 10 MB</td></tr>")

guide_page({
    "slug": "chart-of-accounts", "crumb": "Chart of accounts", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-15", "kicker": "Reference",
    "title": "Chart of Accounts: What It Is, How to Set One Up, and an Example",
    "seo_title": "Chart of Accounts: Example, Numbering and Setup | Vettlo",
    "desc": f"A chart of accounts explained: the five account types, a numbering scheme, a {_ca_n}-account small business example mapped to Schedule C, and setup steps.",
    "card": f"The five account types, a numbering scheme and a {_ca_n}-account sample chart for a small business.",
    "answer": ("A chart of accounts is the numbered list of every account a business records transactions in, grouped into five types: assets, liabilities, equity, revenue and expenses. "
               "The first three feed the balance sheet and the last two feed the profit and loss statement, so the way you set up the chart decides what your financial reports and tax totals can show."),
    "sections": [
        ("what", "What is a chart of accounts?", f"""<p>A chart of accounts is the index of your books. Every invoice, bill, bank deposit and card charge is posted to one or more accounts on it, and the general ledger keeps the running balance of each. If the chart has a "Software subscriptions" account, your reports can tell you what you spent on software; if it doesn't, that spending disappears into a broader line.</p>
<p>Accounting software creates a starter chart for you when you open a company file, and most of what you do afterward is trimming and extending it. Our <a href="{_ac_cat}">comparison of the best accounting software</a> ranks {len(_ac_ranked)} tools on price and features; this guide covers the chart itself, which works the same way in any of them.</p>
<p>Two everyday accounts show how it connects to the rest of your books: accounts receivable (money customers owe you, see our <a href="/guides/accounts-receivable/">accounts receivable guide</a>) and accounts payable (bills you owe, see the <a href="/guides/accounts-payable-process/">accounts payable process</a>). Both are single lines on the chart that summarize many open invoices.</p>"""),
        ("types", "What are the five types of accounts?", f"""<p>Every account belongs to one of five types, and the type decides which financial statement it appears on and whether a debit increases or decreases it. Contra accounts, such as accumulated depreciation or owner's draws, sit inside a type but run the opposite way.</p>
<div class="table-wrap"><table><thead><tr><th>Type</th><th>Common number range</th><th>Statement</th><th>Normal balance</th><th>What it holds</th></tr></thead><tbody>{_ca_type_rows}</tbody></table></div>
<p>Balance sheet accounts carry their balances from year to year. Revenue and expense accounts start over each fiscal year: at year-end their net result (profit or loss) moves into equity, usually into retained earnings. That's why the chart is always listed in the same order: balance sheet accounts first, then the profit and loss accounts.</p>
<p>Some businesses add a cost of goods sold group (often 5000-5999) between revenue and operating expenses, so gross profit shows separately. It's still an expense type.</p>"""),
        ("numbering", "How should you number a chart of accounts?", f"""<p>Give each type its own block of numbers, leave wide gaps between accounts, and number in the order accounts appear on the statements. A four-digit scheme is enough for most small businesses.</p>
<ol>
<li><b>Use the first digit for the type.</b> 1 for assets, 2 for liabilities, 3 for equity, 4 for revenue, 5 and 6 for expenses. Xero's own guide suggests the same 1000-5999 pattern.</li>
<li><b>Leave gaps of 10, 50 or 100.</b> If checking is 1000 and savings is 1010, a second bank account can be 1020 without renumbering anything.</li>
<li><b>Order within each block by liquidity or size.</b> Cash before receivables before equipment; short-term debts (2000s) before long-term loans (2700s).</li>
<li><b>Use subaccounts for detail you only sometimes need.</b> "Vehicle expenses" with fuel and insurance subaccounts keeps the profit and loss short while the detail stays one click away.</li>
<li><b>Don't create accounts for departments, projects or locations.</b> Use the software's tags for that: classes and locations in QuickBooks{f' (from the Plus plan, {_ca_qb_cls} combined)' if _ca_qb_cls else ''}, tracking categories in Xero. Otherwise every expense account gets copied once per department.</li>
</ol>
<p>Account numbers are optional in most cloud software, but they make the chart easier to scan, keep reports in a stable order and make it obvious when someone has created an account in the wrong group.</p>"""),
        ("example", "What does a small business chart of accounts look like?", f"""<p>Here's a sample chart of accounts for a hypothetical consulting business with one employee, some subcontractors and an office lease: {_ca_n} accounts in total ({", ".join(f"{v} {k.lower()}" for k, v in _ca_cnt.items())}). For a sole proprietor, the last column shows which line of the 2025 Schedule C (Form 1040) each income and expense account rolls up to.</p>
<div class="table-wrap"><table><thead><tr><th>No.</th><th>Account</th><th>Type</th><th>2025 Schedule C line</th></tr></thead><tbody>{_ca_rows}</tbody></table></div>
<p>The expense accounts cover {_ca_sched} different Schedule C lines, so the year-end tax totals come straight off the profit and loss report instead of being re-sorted from receipts. Partnerships and corporations file different returns with their own line items, and your preparer may place a few accounts differently (bank fees, for example, often go under other expenses). Balance sheet accounts don't map to Schedule C.</p>
<p>A business that sells products would add inventory (an asset, around 1300) and cost of goods sold accounts (5000s), which feed line 4 and Part III of Schedule C.</p>
<p class="small muted">Hypothetical example for illustration. Schedule C line labels from the IRS 2025 form. This isn't tax advice.</p>"""),
        ("setup", "How do you set up a chart of accounts?", f"""<p>Start from the default chart your accounting software creates, then cut it down and add only the accounts your reports and tax return need. Seven steps:</p>
<ol>
<li><b>Pick your entity and industry during setup.</b> QuickBooks Online builds the starting chart from your business entity, and Xero from your industry or business type, so a wrong answer here means more cleanup later.</li>
<li><b>List the reports you need.</b> Your tax return's expense lines, what your lender or investors ask for, and the two or three costs you want to watch every month.</li>
<li><b>Make inactive or archive the defaults you won't use.</b> An empty account list is easier to post to correctly. In QuickBooks, inactive accounts don't count toward the plan's account limit; Zoho Books keeps its system default accounts active.</li>
<li><b>Add your own accounts and numbers.</b> Choose the type carefully: in QuickBooks the account type and detail type decide where the account shows up on the statements.</li>
<li><b>Enter opening balances</b> for bank, credit card, loan and equity accounts as of your start date. Bank and card accounts connected to bank feeds bring in their own transactions.</li>
<li><b>Map bank rules and products to accounts</b> so routine transactions land in the right place without manual sorting.</li>
<li><b>Limit who can create accounts.</b> Xero recommends keeping it to one or two people; a chart that anyone can extend fills up with near-duplicates such as "Software" and "Subscriptions."</li>
</ol>
<p>Review the chart once a year, before the year-end close. Merging or renaming accounts is easiest before a new fiscal year starts.</p>"""),
        ("software", "How do QuickBooks, Xero and Zoho Books handle the chart of accounts?", f"""<p>All three create a default chart for you and let you add, rename and number accounts; they differ in limits, in what you can remove and in how you bring in a chart you already have.</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Default chart</th><th>Structure</th><th>Account limit</th><th>Removing accounts</th><th>Import</th></tr></thead><tbody>{_ca_soft_rows}</tbody></table></div>
<p class="small muted">From each vendor's help pages, checked Nov 15, 2026. QuickBooks limits from Intuit's usage limits page (updated Aug 5, 2026); plan prices are regular US monthly prices from our pricing data.</p>
<p>The 250-account cap rarely binds a small business, but a company that keeps a separate account per property, store or client can hit it on QuickBooks Plus{f' ({_ca_qb_plus})' if _ca_qb_plus else ''}; classes, locations or subaccounts are the cheaper fix than upgrading. For a plan-by-plan look at the most common pairings, see <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> and <a href="/compare/xero-vs-zohobooks/">Xero vs Zoho Books</a>, and for what each plan costs over a year, our <a href="/guides/accounting-software-cost/">accounting software cost guide</a>.</p>"""),
    ],
    "faqs": [
        ("How many accounts should a small business chart of accounts have?", f"There's no required number. Use enough accounts to read your profit and loss and fill in your tax return, and no more; the sample chart above has {_ca_n}. QuickBooks Online caps active accounts at 250 on its Simple Start, Essentials and Plus plans, with no cap on Advanced."),
        ("What is the difference between a chart of accounts and a general ledger?", "The chart of accounts is the list of accounts and their numbers and types. The general ledger is the record of every transaction posted to those accounts and each account's balance. The chart is the structure; the ledger is the data."),
        ("Can you change a chart of accounts after you start using it?", "Yes. You can add, rename and renumber accounts at any time. For accounts that already have transactions, make them inactive or archive them instead of deleting them so past reports stay intact; Zoho Books doesn't let you delete an account linked to transactions or any system default account."),
        ("What order does a chart of accounts follow?", "Balance sheet accounts come first (assets, liabilities, equity), then profit and loss accounts (revenue, then expenses). It's the same order the accounts appear on the financial statements, and the numbering usually follows it: 1000s for assets through 5000s and 6000s for expenses."),
    ],
    "sources": [
        ("IRS: 2025 Schedule C (Form 1040), Profit or Loss From Business", "https://www.irs.gov/pub/irs-prior/f1040sc--2025.pdf"),
        ("QuickBooks: Create a new account in your chart of accounts", "https://quickbooks.intuit.com/learn-support/en-us/help-articles/create-a-new-account-in-your-chart-of-accounts/00/348702"),
        ("QuickBooks: Learn about usage limits in QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-us/help-article/intuit-subscriptions/learn-usage-limits-quickbooks-online/L6THMltE4_US_en_US"),
        ("Xero: What is a chart of accounts?", "https://www.xero.com/glossary/chart-of-accounts/"),
        ("Zoho Books help: Chart of accounts", "https://www.zoho.com/books/help/accountant/chart-of-accounts.html"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
    ],
})


# ---------- What is a general ledger? (posting flow, computed example, trial balance, GL reports)
# Example business is hypothetical; account numbers follow the sample chart in the chart-of-accounts guide.
# IRS Pub 583 wording and record-retention periods fetched 2026-11-16; QuickBooks, Zoho Books and Xero report details
# from vendor pages fetched the same day. Plan prices from data/review_depth.json.
_gl_acct = {  # number: (name, type, normal balance)
    1000: ("Business checking", "Asset", "Dr"), 1100: ("Accounts receivable", "Asset", "Dr"),
    2100: ("Business credit card", "Liability", "Cr"), 3000: ("Owner's contributions", "Equity", "Cr"),
    4000: ("Consulting revenue", "Revenue", "Cr"), 5000: ("Subcontractors", "Expense", "Dr"),
    6200: ("Office supplies and software", "Expense", "Dr"), 6250: ("Office rent", "Expense", "Dr"),
}
_gl_tx = [  # (date, description, debit account, credit account, amount)
    ("Oct&nbsp;1", "Owner deposits starting capital", 1000, 3000, 10000),
    ("Oct&nbsp;3", "Pay October office rent", 6250, 1000, 1500),
    ("Oct&nbsp;8", "Design software charged to card", 6200, 2100, 300),
    ("Oct&nbsp;15", "Invoice client for brand project", 1100, 4000, 4800),
    ("Oct&nbsp;22", "Client pays part of the invoice", 1000, 1100, 3000),
    ("Oct&nbsp;29", "Pay freelance illustrator", 5000, 1000, 1200),
]
_gl_an = lambda n: f"{n} {_gl_acct[n][0]}"
_gl_j_rows = "".join(f"<tr><td>{d}</td><td>{desc}</td><td>{_gl_an(dr)}</td><td>{_gl_an(cr)}</td><td>{_fmt(a)}</td></tr>" for d, desc, dr, cr, a in _gl_tx)
_gl_dr = {n: sum(a for _d, _s, dr, _c, a in _gl_tx if dr == n) for n in _gl_acct}
_gl_cr = {n: sum(a for _d, _s, _r, cr, a in _gl_tx if cr == n) for n in _gl_acct}
_gl_bal = {n: (_gl_dr[n] - _gl_cr[n]) if _gl_acct[n][2] == "Dr" else (_gl_cr[n] - _gl_dr[n]) for n in _gl_acct}
# Cash account as it appears in the ledger, with a running balance
_gl_cash_rows, _gl_run = "", 0
for d, desc, dr, cr, a in _gl_tx:
    if 1000 not in (dr, cr):
        continue
    _gl_run += a if dr == 1000 else -a
    _gl_cash_rows += (f"<tr><td>{d}</td><td>{desc}</td><td>{_gl_an(cr if dr == 1000 else dr)}</td>"
                      f"<td>{_fmt(a) if dr == 1000 else ''}</td><td>{_fmt(a) if cr == 1000 else ''}</td><td>{_fmt(_gl_run)}</td></tr>")
assert _gl_run == _gl_bal[1000]
_gl_cash_n = sum(1 for t in _gl_tx if 1000 in (t[2], t[3]))
_gl_tb_dr = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][2] == "Dr")
_gl_tb_cr = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][2] == "Cr")
assert _gl_tb_dr == _gl_tb_cr
_gl_tb_rows = "".join(f"<tr><td>{_gl_an(n)}</td><td>{_gl_acct[n][1]}</td><td>{_fmt(_gl_bal[n]) if _gl_acct[n][2] == 'Dr' else ''}</td>"
                      f"<td>{_fmt(_gl_bal[n]) if _gl_acct[n][2] == 'Cr' else ''}</td></tr>" for n in sorted(_gl_acct))
_gl_rev = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][1] == "Revenue")
_gl_exp = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][1] == "Expense")
_gl_ni = _gl_rev - _gl_exp
_gl_assets = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][1] == "Asset")
_gl_liab = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][1] == "Liability")
_gl_eq = sum(_gl_bal[n] for n in _gl_acct if _gl_acct[n][1] == "Equity")
assert _gl_assets == _gl_liab + _gl_eq + _gl_ni
_gl_qb = _ap_name.get("quickbooks", "QuickBooks Online")
_gl_qb_adv = _ap_plan_price(_gl_qb, "Advanced")
_gl_qb_ss = _ap_plan_price(_gl_qb, "Simple Start")
_gl_soft_rows = ""
if "quickbooks" in _ac_ranked:
    _gl_soft_rows += (f"<tr><td>{_ac_rv('quickbooks')}</td><td>General Ledger</td><td>Reports &gt; Standard reports, search by name</td>"
                      "<td>Add Debit and Credit columns and a Cleared column for reconciliation status; filter by account</td>"
                      f"<td>Custom Report Builder only on Advanced{f' ({_gl_qb_adv})' if _gl_qb_adv else ''}</td></tr>")
if "zohobooks" in _ac_ranked:
    _gl_soft_rows += (f"<tr><td>{_ac_rv('zohobooks')}</td><td>General Ledger and Detailed General Ledger</td><td>Reports &gt; Accountant</td>"
                      "<td>Detailed version: opening and closing balance for every account and a row for every transaction</td>"
                      "<td>Large exports run in the background, with download links under Check Status</td></tr>")
if "xero" in _ac_ranked:
    _gl_soft_rows += (f"<tr><td>{_ac_rv('xero')}</td><td>General journal report, detailed or overview</td><td>Reports section</td>"
                      "<td>Xero's US guide describes a detailed report and an overview of journal activity</td>"
                      "<td>Report names differ from QuickBooks; ask your accountant which one they want</td></tr>")

guide_page({
    "slug": "general-ledger", "crumb": "General ledger", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-16", "kicker": "Explainer",
    "title": "What Is a General Ledger? How It Works, With an Example",
    "seo_title": "General Ledger: What It Is and How It Works | Vettlo",
    "desc": f"What a general ledger is, how journal entries post to it, a {len(_gl_tx)}-transaction example with a trial balance, and where to find GL reports in your software.",
    "card": f"How entries post to the general ledger, a worked {len(_gl_tx)}-transaction example and the trial balance it produces.",
    "answer": ("A general ledger (GL) is the complete record of a business's transactions, sorted by account, showing every debit, credit and running balance for each account on the chart of accounts. "
               "Transactions are first recorded as journal entries, then posted to the ledger; the ledger's account balances produce the trial balance, which in turn becomes the balance sheet and the profit and loss statement."),
    "sections": [
        ("what", "What is a general ledger?", f"""<p>The general ledger is where your books actually live. Each account, from the business checking account to office rent, gets its own page in the ledger listing every transaction that touched it, in date order, with a running balance. Add up the ledger and you have the numbers behind every financial report.</p>
<p>In practice, the general ledger is the core of any accounting software: invoices, bills, bank-feed matches and manual entries all end up posted there. Our <a href="{_ac_cat}">ranking of the best accounting software</a> compares {len(_ac_ranked)} tools on price and features; this guide explains what the ledger does, which works the same way in every one of them.</p>
<p>Three terms get mixed up:</p>
<ul>
<li><b>Chart of accounts:</b> the list of accounts and their numbers. It's the ledger's table of contents; see our <a href="/guides/chart-of-accounts/">chart of accounts guide</a> for how to set one up.</li>
<li><b>Journal:</b> the chronological record of each transaction as it happens. IRS Publication 583 describes it as the book where "you record each business transaction shown on your supporting documents."</li>
<li><b>Ledger:</b> the same transactions regrouped by account. Publication 583 calls it the book "that contains the totals from all of your journals."</li>
</ul>"""),
        ("posting", "How do transactions get into the general ledger?", f"""<p>Every transaction moves through the same path: a source document becomes a journal entry, the entry is posted to two or more ledger accounts, and the ledger's balances roll up into reports.</p>
<ol>
<li><b>Source document.</b> An invoice you send, a bill you receive, a receipt or a bank transaction.</li>
<li><b>Journal entry.</b> The transaction is recorded with a date, a description, and at least one debit and one credit of equal total. That rule is double-entry bookkeeping, which Publication 583 calls "self-balancing."</li>
<li><b>Posting.</b> Each line of the entry is copied to its account in the general ledger, and that account's balance is updated.</li>
<li><b>Trial balance.</b> At the end of the period, every account's balance is listed; total debits must equal total credits.</li>
<li><b>Adjusting entries and close.</b> Accruals, depreciation and corrections are posted, then the period is closed.</li>
<li><b>Financial statements.</b> Asset, liability and equity balances form the balance sheet; revenue and expense balances form the profit and loss statement.</li>
</ol>
<p>In accounting software, steps 2 and 3 happen together: saving an invoice writes the journal entry and posts it in one go. You rarely type journal entries yourself except for adjustments.</p>
<h3>What are subledgers?</h3>
<p>Busy accounts keep their detail in a subledger and post only totals to the general ledger. Accounts receivable is the usual example: the subledger tracks what each customer owes, invoice by invoice, while the GL holds one AR balance. Accounts payable works the same way for suppliers. Our guides to <a href="/guides/accounts-receivable/">accounts receivable</a> and the <a href="/guides/accounts-payable-process/">accounts payable process</a> cover running those day to day. The subledger total and the GL control account should always match.</p>"""),
        ("example", "What does a general ledger look like? A worked example", f"""<p>Here are {len(_gl_tx)} October transactions for a hypothetical one-person design studio, first as journal entries and then as they appear in one ledger account. Account numbers follow the sample chart in our chart of accounts guide.</p>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Transaction</th><th>Debit</th><th>Credit</th><th>Amount</th></tr></thead><tbody>{_gl_j_rows}</tbody></table></div>
<p>Each row touches two accounts. The ledger regroups them: the checking account's ledger page picks up the {_gl_cash_n} rows that moved cash, with the other account shown for reference.</p>
<p><b>General ledger: {_gl_an(1000)}, October</b></p>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Description</th><th>Offsetting account</th><th>Debit</th><th>Credit</th><th>Balance</th></tr></thead><tbody>{_gl_cash_rows}</tbody></table></div>
<p>The ending balance of {_fmt(_gl_bal[1000])} is what the books say is in the bank. Comparing it with the bank statement is the monthly check our <a href="/guides/bank-reconciliation/">bank reconciliation guide</a> walks through. The credit card charge and the invoice don't appear here at all: they live on the ledger pages for the card, accounts receivable and revenue.</p>
<p class="small muted">Hypothetical example for illustration; amounts are not from a real business.</p>"""),
        ("trial", "How does the general ledger produce a trial balance?", f"""<p>A trial balance lists every general ledger account's ending balance in a debit or credit column, and the two columns must total the same. In the example, both come to {_fmt(_gl_tb_dr)}:</p>
<div class="table-wrap"><table><thead><tr><th>Account</th><th>Type</th><th>Debit</th><th>Credit</th></tr></thead><tbody>{_gl_tb_rows}
<tr><td><b>Total</b></td><td></td><td><b>{_fmt(_gl_tb_dr)}</b></td><td><b>{_fmt(_gl_tb_cr)}</b></td></tr></tbody></table></div>
<p>From the same balances, October's profit and loss shows revenue of {_fmt(_gl_rev)} less expenses of {_fmt(_gl_exp)}, a profit of {_fmt(_gl_ni)}. The balance sheet shows assets of {_fmt(_gl_assets)} against liabilities of {_fmt(_gl_liab)} and equity of {_fmt(_gl_eq + _gl_ni)} (the owner's {_fmt(_gl_eq)} plus the month's profit), so assets equal liabilities plus equity.</p>
<h3>What a balanced trial balance doesn't prove</h3>
<p>Matching totals only show that every entry had equal debits and credits. These errors still balance:</p>
<ul>
<li>A transaction never entered at all.</li>
<li>A posting to the wrong account of the right side, such as software booked to rent.</li>
<li>The same wrong amount on both sides, such as {_fmt(_gl_tx[1][4])} typed as {_fmt(_gl_tx[1][4] * 10)}.</li>
<li>A transaction entered twice.</li>
</ul>
<p>That's why bank reconciliations and a review of the ledger detail for odd items are part of every month-end close, not just the trial balance.</p>"""),
        ("software", "How do you run a general ledger report in accounting software?", f"""<p>Every accounting tool has a general ledger report that lists transactions by account for a date range; the names and options differ. What the three most common tools in our ranking offer:</p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Report</th><th>Where</th><th>What it shows</th><th>Notes</th></tr></thead><tbody>{_gl_soft_rows}</tbody></table></div>
<p class="small muted">From vendor help pages and guides checked Nov 16, 2026 (QuickBooks article updated Aug 3, 2026). Prices are regular US monthly prices from our pricing data.</p>
<p>The general ledger report is available on entry plans{f", including QuickBooks Simple Start at {_gl_qb_ss}" if _gl_qb_ss else ""}; what you pay more for is customization and the transaction volume around it. For plan-by-plan differences see <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> and <a href="/compare/xero-vs-zohobooks/">Xero vs Zoho Books</a>, and for annual totals our <a href="/guides/accounting-software-cost/">accounting software cost guide</a>.</p>
<p>Your accountant will usually ask for the general ledger and the trial balance at year-end. Export both for the full fiscal year, and run them on the same accounting basis (cash or accrual) you file on; our <a href="/guides/cash-vs-accrual-accounting/">cash vs accrual accounting guide</a> explains the difference.</p>"""),
        ("retention", "How long should you keep general ledger records?", """<p>The IRS doesn't set a separate rule for the ledger; it falls under the general recordkeeping periods, which run from when you file the return the records support. From the IRS's "How long should I keep records?" page:</p>
<div class="table-wrap"><table><thead><tr><th>Situation</th><th>Keep records for</th></tr></thead><tbody>
<tr><td>Most returns</td><td>3 years</td></tr>
<tr><td>You file a claim for credit or refund after filing</td><td>3 years from filing or 2 years from paying the tax, whichever is later</td></tr>
<tr><td>You don't report income that is more than 25% of the gross income shown on the return</td><td>6 years</td></tr>
<tr><td>You claim a loss from worthless securities or a bad debt deduction</td><td>7 years</td></tr>
<tr><td>Employment tax records</td><td>At least 4 years after the tax is due or paid, whichever is later</td></tr>
<tr><td>You don't file a return, or file a fraudulent one</td><td>Indefinitely</td></tr>
</tbody></table></div>
<p>If you keep books in software, Publication 583 says a computerized system must be able to produce legible records that reconcile with your books and return. Before you cancel a subscription or switch tools, export the general ledger and trial balance for every open year, since access to old data can end with the plan. Lenders, insurers and buyers of a business may ask for records longer than the IRS does.</p>
<p class="small muted">Summarizes IRS guidance and isn't tax or legal advice.</p>"""),
    ],
    "faqs": [
        ("What is the difference between a general ledger and a general journal?", "The general journal records transactions in date order as they happen, each with its debits and credits. The general ledger takes the same entries and groups them by account, with a running balance for each. The journal shows what happened when; the ledger shows where each account stands."),
        ("Is a general ledger the same as a trial balance?", "No. The general ledger holds every transaction for every account. The trial balance is a one-page summary that lists only each account's ending balance in debit and credit columns, to check that the two totals match before preparing financial statements."),
        ("Does a small business need a general ledger?", "A business using double-entry bookkeeping has one by definition, and every mainstream accounting app keeps one automatically. IRS Publication 583 also allows a single-entry system based on the income statement, which can work for a very small, simple business, but it doesn't produce a balance sheet."),
        ("What are the five types of general ledger accounts?", "Assets, liabilities, equity, revenue and expenses. Asset and expense accounts normally carry debit balances; liability, equity and revenue accounts normally carry credit balances. The first three feed the balance sheet and the last two the profit and loss statement."),
    ],
    "sources": [
        ("IRS: Publication 583, Starting a Business and Keeping Records", "https://www.irs.gov/publications/p583"),
        ("IRS: How long should I keep records?", "https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records"),
        ("QuickBooks: Run a report that shows debits and credits for each transaction", "https://quickbooks.intuit.com/learn-support/en-us/help-article/profit-loss-reports/create-report-shows-debits-credits-transaction/L1zvqNX0e_US_en_US"),
        ("Zoho Books: Detailed General Ledger", "https://www.zoho.com/books/kb/reports/detailed-general-ledger.html"),
        ("Xero: General ledger accounting guide (US)", "https://www.xero.com/us/guides/general-ledger-accounting/"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
    ],
})


# ---------- Double-entry bookkeeping (supporting article for the accounting pillar)
# Hypothetical catering business; every total below is computed, so the tables always balance.
_de_acct = {  # number: (name, type)
    1000: ("Business checking", "Asset"), 1200: ("Accounts receivable", "Asset"), 1500: ("Kitchen equipment", "Asset"),
    2000: ("Accounts payable", "Liability"), 2500: ("Equipment loan", "Liability"),
    3000: ("Owner's capital", "Equity"), 4000: ("Catering revenue", "Revenue"),
    5000: ("Food and supplies", "Expense"), 6000: ("Kitchen rent", "Expense"),
}
_de_normal = {"Asset": "Debit", "Expense": "Debit", "Liability": "Credit", "Equity": "Credit", "Revenue": "Credit"}
_de_tx = [  # (date, description, [(account, debit, credit)])
    ("Mar&nbsp;1", "Owner deposits savings to start the business", [(1000, 12000, 0), (3000, 0, 12000)]),
    ("Mar&nbsp;3", "Buy a commercial oven: part cash, part loan", [(1500, 6000, 0), (1000, 0, 1500), (2500, 0, 4500)]),
    ("Mar&nbsp;6", "Buy ingredients on 30-day supplier terms", [(5000, 800, 0), (2000, 0, 800)]),
    ("Mar&nbsp;14", "Cater a corporate lunch and send the invoice", [(1200, 3200, 0), (4000, 0, 3200)]),
    ("Mar&nbsp;20", "Pay the kitchen rent", [(6000, 1100, 0), (1000, 0, 1100)]),
    ("Mar&nbsp;28", "Client pays the lunch invoice in full", [(1000, 3200, 0), (1200, 0, 3200)]),
    ("Mar&nbsp;31", "Pay the ingredient supplier", [(2000, 800, 0), (1000, 0, 800)]),
]
for _d, _s, _ls in _de_tx:
    assert sum(l[1] for l in _ls) == sum(l[2] for l in _ls), _s
_de_an = lambda n: f"{n} {_de_acct[n][0]}"
_de_signed = lambda n, dr, cr: (dr - cr) if _de_normal[_de_acct[n][1]] == "Debit" else (cr - dr)  # change in the account's balance
_de_j_rows = ""
for i, (d, desc, ls) in enumerate(_de_tx, 1):
    for j, (n, dr, cr) in enumerate(ls):
        acct = _de_an(n) if dr else f'<span style="padding-left:1.5em">{_de_an(n)}</span>'
        _de_j_rows += (f"<tr><td>{f'{i}. {d}' if j == 0 else ''}</td><td>{desc if j == 0 else ''}</td><td>{acct}</td>"
                       f"<td>{_fmt(dr) if dr else ''}</td><td>{_fmt(cr) if cr else ''}</td></tr>")
_de_compound = [i for i, t in enumerate(_de_tx, 1) if len(t[2]) > 2]
# The accounting equation after each entry: assets = liabilities + equity (equity includes revenue less expenses)
_de_bal = {n: 0 for n in _de_acct}
_de_eq_rows = ""
for i, (d, desc, ls) in enumerate(_de_tx, 1):
    chg = {"A": 0, "L": 0, "E": 0}
    for n, dr, cr in ls:
        t = _de_acct[n][1]
        delta = _de_signed(n, dr, cr)
        _de_bal[n] += delta
        k = {"Asset": "A", "Liability": "L"}.get(t, "E")
        chg[k] += -delta if t == "Expense" else delta
    A = sum(v for n, v in _de_bal.items() if _de_acct[n][1] == "Asset")
    L = sum(v for n, v in _de_bal.items() if _de_acct[n][1] == "Liability")
    E = sum(v for n, v in _de_bal.items() if _de_acct[n][1] in ("Equity", "Revenue")) - sum(v for n, v in _de_bal.items() if _de_acct[n][1] == "Expense")
    assert A == L + E
    sg = lambda x: ("+" if x > 0 else "&minus;") + _fmt(abs(x)) if x else "0"
    _de_eq_rows += f"<tr><td>{i}</td><td>{sg(chg['A'])}</td><td>{sg(chg['L'])}</td><td>{sg(chg['E'])}</td><td>{_fmt(A)}</td><td>{_fmt(L + E)}</td></tr>"
_de_A, _de_L, _de_E = A, L, E
_de_rev = sum(v for n, v in _de_bal.items() if _de_acct[n][1] == "Revenue")
_de_exp = sum(v for n, v in _de_bal.items() if _de_acct[n][1] == "Expense")
_de_cap = _de_bal[3000]
_de_cash = _de_bal[1000]
_de_n = len(_de_tx)
_de_lines = sum(len(t[2]) for t in _de_tx)
_de_tot = sum(l[1] for t in _de_tx for l in t[2])
_de_oven = _de_tx[1][2]
_de_rule_rows = "".join(
    f"<tr><td>{t}</td><td>{'Increases' if nb == 'Debit' else 'Decreases'}</td><td>{'Decreases' if nb == 'Debit' else 'Increases'}</td><td>{nb}</td><td>{ex}</td></tr>"
    for t, nb, ex in [("Asset", "Debit", "Cash, receivables, equipment"), ("Expense", "Debit", "Rent, supplies, wages"),
                      ("Liability", "Credit", "Supplier bills, loans, sales tax owed"), ("Equity", "Credit", "Owner's capital, retained earnings"),
                      ("Revenue", "Credit", "Sales, service fees")])
_de_qb = _ap_name.get("quickbooks", "QuickBooks Online")
_de_qb_ss = _ap_plan_price(_de_qb, "Simple Start")
_de_free = _ac_and(_ac_free) if _ac_free else ""

guide_page({
    "slug": "double-entry-bookkeeping", "crumb": "Double-entry bookkeeping", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-17", "kicker": "Explainer",
    "title": "Double-Entry Bookkeeping: How Debits and Credits Work",
    "seo_title": "Double-Entry Bookkeeping: Debits, Credits, Examples | Vettlo",
    "desc": f"Double-entry bookkeeping explained: the debit and credit rules for each account type, {_de_n} worked journal entries, and how it differs from single entry.",
    "card": f"The debit and credit rules by account type, with {_de_n} journal entries that keep the accounting equation balanced.",
    "answer": ("Double-entry bookkeeping records every transaction in at least two accounts: one or more debits and one or more credits of equal total, so the books stay in balance. "
               "Debits increase asset and expense accounts, credits increase liability, equity and revenue accounts, and after every entry assets still equal liabilities plus equity."),
    "sections": [
        ("what", "What is double-entry bookkeeping?", f"""<p>Double-entry bookkeeping is the method behind almost every set of business books: each transaction is written as an entry that debits at least one account and credits at least one other for the same total. Buy a $50 printer with cash and two things change at once: you have $50 more equipment and $50 less cash. Double entry records both sides.</p>
<p>It's also the method accounting software runs on, whichever product you choose. Our <a href="{_ac_cat}">comparison of the best accounting software</a> ranks {len(_ac_ranked)} tools on price and features; this guide covers the rules those tools apply when they write entries for you.</p>
<p>The idea rests on the accounting equation:</p>
<p><b>Assets = Liabilities + Equity</b></p>
<p>Everything the business owns (assets) was paid for either with borrowed money (liabilities) or with the owner's money and retained profit (equity). Because every entry changes two sides by the same amount, the equation can't drift out of balance. IRS Publication 583 calls the system "self-balancing because you record every transaction as a debit entry in one account and as a credit entry in another."</p>
<p>Revenue and expenses sit inside equity: revenue raises it, expenses lower it. Written out, the expanded equation is <b>Assets = Liabilities + Owner's capital + Revenue &minus; Expenses</b>, which is why sales and costs follow the same debit and credit logic as the balance sheet.</p>"""),
        ("rules", "How do debits and credits work?", f"""<p>A debit is an entry on the left side of an account and a credit is an entry on the right; whether each one increases or decreases the balance depends on the account type. Assets and expenses go up with debits. Liabilities, equity and revenue go up with credits.</p>
<div class="table-wrap"><table><thead><tr><th>Account type</th><th>A debit</th><th>A credit</th><th>Normal balance</th><th>Examples</th></tr></thead><tbody>{_de_rule_rows}</tbody></table></div>
<p>"Debit" and "credit" here have nothing to do with good or bad, or with your bank card. They only mean left and right. That's why your bank statement calls a deposit a credit: to the bank, your money is a liability it owes you. On your own books, the same deposit is a debit to cash.</p>
<p>A common memory aid is <b>DEAL</b> versus <b>ER</b>: Dividends (or owner's draws), Expenses and Assets increase with a debit; Liabilities, Equity and Revenue increase with a credit. Owner's draws are a contra-equity account, so they run the opposite way from capital.</p>
<p>To write any entry, ask three questions:</p>
<ol>
<li><b>Which accounts changed?</b> Every transaction touches at least two.</li>
<li><b>What type is each account?</b> Look it up on your <a href="/guides/chart-of-accounts/">chart of accounts</a>, which lists every account by type.</li>
<li><b>Did each one go up or down?</b> Use the table: an asset going up is a debit, a liability going up is a credit, and so on. Then check that total debits equal total credits.</li>
</ol>"""),
        ("examples", "What does double-entry bookkeeping look like? Worked journal entries", f"""<p>Here is a hypothetical catering business's first month as {_de_n} journal entries. Debits are listed first in each entry and credits are indented, the usual journal layout. Together they post {_de_lines} lines totaling {_fmt(_de_tot)} on each side.</p>
<div class="table-wrap"><table><thead><tr><th>Entry</th><th>Transaction</th><th>Account</th><th>Debit</th><th>Credit</th></tr></thead><tbody>{_de_j_rows}</tbody></table></div>
<p>Entry {_de_compound[0] if _de_compound else 2} is a <b>compound entry</b>: one debit of {_fmt(_de_oven[0][1])} balanced by two credits, {_fmt(_de_oven[1][2])} from checking and {_fmt(_de_oven[2][2])} borrowed. An entry can have any number of lines as long as the two columns match.</p>
<p>Entries 3 and 4 show why double entry separates earning from collecting. The ingredients are an expense on the day they arrive, before the supplier is paid, and the lunch is revenue when it's invoiced, before the client pays. That's accrual timing; our <a href="/guides/cash-vs-accrual-accounting/">cash vs accrual accounting guide</a> explains the alternative. Receivables and payables are covered in the <a href="/guides/accounts-receivable/">accounts receivable</a> and <a href="/guides/accounts-payable-process/">accounts payable</a> guides.</p>
<h3>How each entry keeps the equation balanced</h3>
<p>Track the three sides of the equation after each entry and they always match. Revenue and expenses are counted in equity.</p>
<div class="table-wrap"><table><thead><tr><th>Entry</th><th>Assets</th><th>Liabilities</th><th>Equity</th><th>Total assets</th><th>Liabilities + equity</th></tr></thead><tbody>{_de_eq_rows}</tbody></table></div>
<p>At month-end the business has {_fmt(_de_A)} of assets ({_fmt(_de_cash)} of it in checking), {_fmt(_de_L)} of liabilities and {_fmt(_de_E)} of equity: the owner's {_fmt(_de_cap)} plus a profit of {_fmt(_de_rev - _de_exp)} ({_fmt(_de_rev)} revenue less {_fmt(_de_exp)} expenses). Posting these entries to their accounts is what builds the <a href="/guides/general-ledger/">general ledger</a> and its trial balance.</p>
<p class="small muted">Hypothetical example for illustration; amounts are not from a real business.</p>"""),
        ("single", "Single-entry vs double-entry bookkeeping: what's the difference?", f"""<p>Single-entry bookkeeping records each transaction once, as income or an expense in a running list; double entry records it in two or more accounts and tracks assets and debts as well. Single entry is simpler, but it can't produce a balance sheet and has no built-in check for errors.</p>
<div class="table-wrap"><table><thead><tr><th></th><th>Single entry</th><th>Double entry</th></tr></thead><tbody>
<tr><td>Records per transaction</td><td>One line: income or expense</td><td>Two or more lines: debits and credits of equal total</td></tr>
<tr><td>Based on</td><td>The income statement (profit or loss)</td><td>Journals and ledgers for every account</td></tr>
<tr><td>Tracks assets and liabilities</td><td>Not in the main record; kept in separate lists if at all</td><td>Yes, each has its own account</td></tr>
<tr><td>Reports</td><td>Income, expenses and profit</td><td>Profit and loss, balance sheet, trial balance</td></tr>
<tr><td>Error check</td><td>None built in</td><td>Debits must equal credits</td></tr>
<tr><td>Typical fit</td><td>A new, very small business with few transactions</td><td>Any business with receivables, payables, loans, inventory or employees</td></tr>
</tbody></table></div>
<p>The IRS lets you choose. Publication 583 says single entry "can be a simple and practical system if you are starting a small business," recording income and expenses through a daily summary of cash receipts and monthly summaries of receipts and disbursements. It adds that double entry "uses journals and ledgers," and that total debits must equal total credits after posting; if they don't, there's an error to find.</p>
<p>A spreadsheet of income and expenses is single entry. You move to double entry, in practice, the day you start using accounting software, because it records both sides automatically.</p>
<p class="small muted">Summarizes IRS guidance and isn't tax or legal advice.</p>"""),
        ("software", "How does accounting software handle double entry?", f"""<p>Accounting software writes the journal entry for you every time you save a standard form, so you rarely choose debits and credits yourself. What each everyday action records behind the scenes:</p>
<div class="table-wrap"><table><thead><tr><th>You do this</th><th>Software debits</th><th>Software credits</th></tr></thead><tbody>
<tr><td>Send an invoice</td><td>Accounts receivable</td><td>Revenue (and sales tax payable, if charged)</td></tr>
<tr><td>Record a customer payment</td><td>Bank or undeposited funds</td><td>Accounts receivable</td></tr>
<tr><td>Enter a supplier bill</td><td>The expense or asset account on the bill</td><td>Accounts payable</td></tr>
<tr><td>Pay a bill</td><td>Accounts payable</td><td>Bank</td></tr>
<tr><td>Categorize a card or bank charge</td><td>The expense account you pick</td><td>Bank or credit card account</td></tr>
<tr><td>Transfer between your own accounts</td><td>Receiving account</td><td>Sending account</td></tr>
</tbody></table></div>
<p>The one place you write debits and credits directly is a manual journal entry, used for items with no standard form: depreciation, accrued expenses, loan interest splits and year-end corrections from your accountant.</p>
<ul>
<li><b>{_ac_rv('quickbooks') if 'quickbooks' in _ac_ranked else 'QuickBooks Online'}:</b> + New &gt; Journal entry. QuickBooks' help page says to enter each account on its own line, with the same amount in the opposite column, keeping total debits and credits equal.</li>
<li><b>{_ac_rv('zohobooks') if 'zohobooks' in _ac_ranked else 'Zoho Books'}:</b> Accountant &gt; Manual Journals &gt; + New Journal. Zoho's help page tells users to "ensure that the amount debited is always equal to the amount credited."</li>
</ul>
<p>Both help pages make balanced debits and credits a requirement of the entry, so the arithmetic is the easy part. Picking the right account is the part software can't do for you, which is why the categories you choose matter more than the mechanics. Prices start low{f": QuickBooks Simple Start is {_de_qb_ss} at the regular price" if _de_qb_ss else ""}{f", and {_de_free} offer free plans" if _de_free else ""}. For plan-by-plan differences, see <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> and <a href="/compare/xero-vs-zohobooks/">Xero vs Zoho Books</a>.</p>
<p class="small muted">Menu paths from QuickBooks and Zoho Books help pages checked Nov 17, 2026; prices are regular US prices from our pricing data.</p>"""),
        ("mistakes", "What are the most common double-entry mistakes?", """<p>Most double-entry errors still balance, because the debit and credit match but one of them lands in the wrong place. These are the ones bookkeepers most often fix at month-end:</p>
<div class="table-wrap"><table><thead><tr><th>Mistake</th><th>What happens</th><th>Fix</th></tr></thead><tbody>
<tr><td>Debit and credit swapped</td><td>Cash goes down when it should go up, so the error shows up as twice the amount</td><td>Reverse the entry and record it again the right way round</td></tr>
<tr><td>Equipment recorded as an expense</td><td>Profit is understated and the asset is missing from the balance sheet</td><td>Move it to a fixed-asset account and depreciate it</td></tr>
<tr><td>Owner's draws recorded as wages or expenses</td><td>Profit is understated; draws aren't a business expense</td><td>Use an owner's draw (contra-equity) account</td></tr>
<tr><td>Loan payments booked fully to expense</td><td>The loan balance never goes down</td><td>Split each payment: principal debits the loan, interest debits interest expense</td></tr>
<tr><td>Customer payment recorded as new revenue</td><td>Revenue counted twice and receivables never clear</td><td>Apply the payment to the open invoice so it credits receivables</td></tr>
</tbody></table></div>
<p>A monthly bank reconciliation catches many of these, since the books' cash balance won't match the statement; our <a href="/guides/bank-reconciliation/">bank reconciliation guide</a> walks through it.</p>"""),
    ],
    "faqs": [
        ("What is an example of double-entry bookkeeping?", "Paying $1,100 of rent from the business checking account is recorded as a $1,100 debit to rent expense and a $1,100 credit to cash. The expense goes up, cash goes down, and the debit and credit totals match."),
        ("Does a debit always mean an increase?", "No. A debit increases asset, expense and owner's draw accounts, and decreases liability, equity and revenue accounts. A credit does the opposite. Whether an entry raises or lowers a balance depends on the account's type."),
        ("Is double-entry bookkeeping required for a small business?", "Not by the IRS. Publication 583 lets a business choose single-entry or double-entry bookkeeping, as long as the records support the return. Lenders, investors and accountants usually expect double-entry books with a balance sheet, and accounting software keeps them by default."),
        ("Can you do double-entry bookkeeping in Excel?", "Yes. Use one sheet as a journal with date, account, debit and credit columns, check that each entry's debits and credits match, and summarize balances by account with a pivot table or SUMIF formulas. It works for a few dozen transactions a month; beyond that, bank feeds in accounting software save most of the typing."),
    ],
    "sources": [
        ("IRS: Publication 583 (12/2024), Starting a Business and Keeping Records", "https://www.irs.gov/publications/p583"),
        ("QuickBooks: Create journal entries in QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-us/reports-and-accounting/create-a-journal-entry/00/262076"),
        ("Zoho Books: Manual Journals", "https://www.zoho.com/books/help/accountant/manual-journal.html"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
    ],
})


# ---------- QuickBooks Online bank feed not updating (tool task guide, Fix it)
# Steps, menu names, error meanings and wait times from Intuit's QuickBooks Online help articles fetched Nov 20, 2026.
# Plan names come from data/review_depth.json so they follow the daily pricing refresh.
_bf_qb = _ac_depth.get("QuickBooks Online", {})
_bf_plans = [p for p, _s, _d in _bf_qb.get("plans", [])]
_bf_plan_txt = f"{_bf_plans[0]} through {_bf_plans[-1]}" if len(_bf_plans) > 1 else "every plan"
_bf_qbrv = _ac_rv("quickbooks") if "quickbooks" in _ac_ranked else '<a href="/tools/quickbooks-online-review/">QuickBooks Online</a>'
_bf_alt = _ac_and([_ac_rv(k) for k in ("xero", "zohobooks") if k in _ac_ranked])
_bf_path = "<b>All apps</b> &gt; <b>Accounting</b> &gt; <b>Bank transactions</b>"
_bf_err = [
    ("101", "The connection has been inactive for about 12 months or more", "Select <b>Update</b> to wake the connection"),
    ("102, 105", "QuickBooks can't reach your bank, usually maintenance or a server problem on the bank's side", "Wait (Intuit says 24 hours or more), then select <b>Update</b>; check the bank's site for outage notices"),
    ("103", "The user ID or password QuickBooks has stored is wrong", "Edit icon &gt; <b>Edit account sign in</b>, type the credentials by hand, <b>Save and connect</b>"),
    ("106", "The account is closed at the bank", "Disconnect it, then add the new account with <b>Link account</b>"),
    ("108", "The bank needs you to complete an action on its website first", "Sign in to the bank, finish the prompt, then select <b>Update</b>"),
    ("109", "The bank requires a new password", "Change it at the bank, then update it in <b>Edit account sign in</b>"),
    ("179", "You're signed in to the bank somewhere else", "Sign out everywhere, wait 15 minutes, clear cache and cookies, retry"),
    ("185, 187", "The bank needs extra verification (security question or one-time code); 187 means it was entered wrong", "Answer the prompt exactly as on the bank's site; allow pop-ups"),
    ("192", "The bank needs sign-in information QuickBooks can't supply", "Upload transactions manually from a CSV file"),
    ("324", "QuickBooks can no longer find the account at the bank", "<b>Fix now</b> &gt; <b>Manage connections</b> &gt; <b>Disconnect</b>, then link the new account"),
    ("9999", "Transactions aren't updating for an unspecified reason", "Wait 48 hours, then contact QuickBooks support"),
]
_bf_err_rows = "".join(f"<tr><td>{c}</td><td>{m}</td><td>{f}</td></tr>" for c, m, f in _bf_err)

guide_page({
    "slug": "quickbooks-bank-feed-not-updating", "crumb": "QuickBooks bank feed not updating", "dept": "Finance", "cats": ["best-accounting-software"],
    "date": "2026-11-20", "kicker": "How-to",
    "title": "QuickBooks Online Bank Feed Not Updating? How to Fix It",
    "seo_title": "QuickBooks Online Bank Feed Not Updating? Fix It | Vettlo",
    "desc": "QuickBooks Online bank feed not updating? Fix it in order: select Update, re-enter your bank sign-in, clear errors 102, 103, 185 or 324, or upload a CSV.",
    "card": "Eight fixes in the order Intuit recommends, plus what the common bank error codes mean and how long to wait.",
    "answer": ("When a QuickBooks Online bank feed stops updating, go to All apps &gt; Accounting &gt; Bank transactions, select the account and select Update; if an error code appears, fix what it points to, usually your bank sign-in or an extra security check. "
               "Errors 102 and 105 are on the bank's side and often clear within 24 to 48 hours, and while you wait you can download a CSV or QBO file from your bank and upload it so your books stay current."),
    "sections": [
        ("why", "Why is my QuickBooks Online bank feed not updating?", f"""<p>A QuickBooks Online bank feed not updating almost always has one of three causes: the bank changed something (a password, a security check, the account itself), the bank's systems are down, or the saved connection is stale. QuickBooks usually tells you which one with an error code on the account's tile.</p>
<p>Bank feeds are what make reconciliation quick in any of the tools on our <a href="{_ac_cat}">best accounting software shortlist</a>, so a broken feed shows up fast: no new transactions in the account's <b>Pending</b> tab, an old "last updated" date on the tile, or a red error banner. The fix steps below are the same on {_bf_plan_txt}; Intuit's help articles don't tie bank connections to a plan.</p>
<p>Start by sorting the problem into one of these groups, because the fix depends on it:</p>
<ul>
<li><b>Bank-side outage.</b> Errors 102, 105, 355 and similar. Nothing is wrong with your setup; waiting is the fix.</li>
<li><b>Sign-in or verification.</b> Errors 103, 109, 185 and 187. The bank rejected the stored credentials or wants an extra step.</li>
<li><b>Account changed.</b> Errors 106 and 324. The account was closed, renumbered or moved, so the feed can't be repaired and has to be replaced.</li>
<li><b>No error, just no new transactions.</b> The connection may simply need a manual refresh, or the bank hasn't posted the transactions yet.</li>
</ul>"""),
        ("fix", "How do I fix a QuickBooks bank feed that won't update?", f"""<p>Work through these steps in order and stop when transactions start flowing again. They follow Intuit's own troubleshooting sequence for QuickBooks Online, with the menu names from its current help articles.</p>
<ol>
<li><b>Check Intuit's bank feed status page.</b> Intuit's troubleshooting article lists this as an early step. If your bank shows a known issue, skip to step 7 and upload manually until it's resolved.</li>
<li><b>Refresh the feed.</b> Go to {_bf_path}, select the account and select <b>Update</b>. Follow any prompts; some banks ask you to sign in on their own site.</li>
<li><b>Sign in to your bank directly.</b> Open the bank's website in a private or incognito window and log in with the same credentials. If that fails, the problem is the credentials, not QuickBooks. While you're there, check for messages or prompts the bank wants you to accept.</li>
<li><b>Check third-party access.</b> Intuit notes that some banks require you to turn on access for third-party apps in your online banking settings before QuickBooks can connect.</li>
<li><b>Re-enter the bank sign-in.</b> In {_bf_path}, select the account, select the edit (pencil) icon, then <b>Edit account sign in</b>. Clear anything your browser autofilled, type the user ID and password by hand and select <b>Save and connect</b>.</li>
<li><b>Correct the account details.</b> If the account or routing number changed, use the same edit icon to update the details and save.</li>
<li><b>Upload transactions manually.</b> Download the missing period from your bank's website as a .csv or .qbo file and upload it to the same account in QuickBooks. This keeps your books current while the connection is fixed.</li>
<li><b>Contact support.</b> In QuickBooks Online go to <b>Help</b> and select <b>Contact Us</b>.</li>
</ol>
<p>If an error code is showing, jump to the table below first: it often tells you which of these steps will work.</p>"""),
        ("errors", "What do QuickBooks Online bank error codes mean?", f"""<p>Each QuickBooks bank error code points to a specific cause, and some of them, such as 102 and 105, are on the bank's side, where the fix is to wait. This table summarizes Intuit's help articles for the codes that most often stop a feed. "Edit icon" means the pencil icon on the account in {_bf_path}.</p>
<div class="table-wrap"><table><thead><tr><th>Error</th><th>What it means</th><th>What to do</th></tr></thead><tbody>{_bf_err_rows}</tbody></table></div>
<p>For errors 102 and 105, Intuit gives slightly different waits in different help articles: one says errors "may resolve within 24 hours or more," another says to wait 24 to 48 hours, and a third says to try again after 2 to 3 hours if the error persists. A sensible approach is to retry <b>Update</b> once after a few hours and upload manually if it's still failing after two days.</p>
<p>For error 185, Intuit says it's a bank security measure rather than a QuickBooks fault. If your bank sends a one-time code, expect to enter it each time the error appears; if it uses security questions, QuickBooks Online remembers the answers.</p>
<p class="small muted">Error descriptions summarize Intuit's QuickBooks Online help articles checked Nov 20, 2026. Codes and wording can differ by country.</p>"""),
        ("reconnect", "How do I disconnect and reconnect a bank account in QuickBooks Online?", f"""<p>Disconnecting and reconnecting is the fix when the account has changed at the bank (errors 106 and 324) or when Intuit's support asks you to rebuild the connection; review pending transactions first, or you risk duplicates when the feed downloads again.</p>
<ol>
<li><b>Review what's waiting.</b> In {_bf_path}, select the account and work through the transactions in the <b>Pending</b> tab: add, match or exclude each one.</li>
<li><b>Disconnect.</b> Select the edit icon, then <b>Edit account details</b>. Tick <b>Disconnect this account on save</b>, select <b>Disconnect</b>, then <b>Save</b>. For error 324, Intuit's path is <b>Fix now</b>, which opens <b>Manage connections</b>, then <b>Disconnect</b>.</li>
<li><b>Reconnect.</b> In {_bf_path}, select <b>Link account</b> (or <b>Connect account</b> if it's your first one), search for your bank, sign in with your current credentials and choose the account.</li>
</ol>
<p>Per Intuit, disconnecting removes the bank feed and no further transactions sync for that account until you link it again. After reconnecting, compare the first downloaded batch with what you already entered and exclude any duplicates before you <a href="/guides/bank-reconciliation/">reconcile the account</a>.</p>
<p>A closed account (error 324 or 106) has to be disconnected before you add its replacement; Intuit notes that otherwise QuickBooks reports the account as already connected.</p>"""),
        ("prevent", "How do I keep the bank feed from breaking again?", f"""<p>Most repeat failures come from the bank side changing without QuickBooks knowing, so the prevention is about telling QuickBooks when you change something.</p>
<ul>
<li><b>Update QuickBooks the same day you change your bank password</b> or security questions, using <b>Edit account sign in</b>. Record the answers exactly as the bank stores them; Intuit says they must match character for character.</li>
<li><b>Don't use copied or autofilled passwords</b> when connecting. Intuit's troubleshooting steps say to type credentials by hand instead.</li>
<li><b>Review the feed weekly.</b> A connection that stays unused for about 12 months triggers error 101, and a weekly look catches any other stall within days instead of at month-end.</li>
<li><b>Watch for "Fix now" on the tile.</b> Some banks require you to re-authorize the connection periodically; QuickBooks shows this as an error you clear by confirming your credentials.</li>
<li><b>Reconcile monthly.</b> A missed feed day shows up as a statement difference. The <a href="/guides/bank-reconciliation/">bank reconciliation guide</a> covers that monthly check.</li>
</ul>"""),
        ("alternatives", "What if your bank won't connect to QuickBooks at all?", f"""<p>If your bank has stopped supporting the connection (Intuit's error 155) or keeps failing, you can run QuickBooks on manual CSV or QBO uploads indefinitely, or move to software whose bank connection works with your bank.</p>
<p>Manual uploads add a monthly chore: download the statement period, upload it and categorize the transactions. For an error 155, Intuit suggests asking your bank to escalate the connection to Intuit's financial institution services team.</p>
<p>Before switching tools, check that your bank is supported by the alternative; bank coverage differs by provider. Our {_bf_qbrv} review covers QuickBooks' plans, the <a href="/tools/best-quickbooks-alternatives/">QuickBooks alternatives</a> page lists other options, and {_bf_alt} reviews describe their bank feed setups. <a href="/compare/quickbooks-vs-xero/">QuickBooks vs Xero</a> compares the two most common choices plan by plan.</p>"""),
    ],
    "faqs": [
        ("How do I manually refresh bank transactions in QuickBooks Online?", "Go to All apps > Accounting > Bank transactions, select the bank or card account and select Update, then follow any prompts; some banks ask you to sign in on their own website. In QuickBooks Self-Employed the equivalent is Settings > Manage accounts > Refresh all."),
        ("What does QuickBooks error 103 mean?", "Error 103 means the user ID or password QuickBooks has stored for your bank is wrong. Check the credentials by signing in to the bank in a private browser window, then in QuickBooks select the account's edit icon, choose Edit account sign in, type the credentials by hand and select Save and connect."),
        ("How long does QuickBooks error 102 or 105 take to fix?", "Errors 102 and 105 mean QuickBooks can't reach your bank, usually because of maintenance on the bank's side. Intuit's help articles say they often clear within 24 to 48 hours; retry Update after a few hours and upload transactions manually if it's still failing after two days."),
        ("Should I review transactions before disconnecting a bank account in QuickBooks?", "Yes. Intuit recommends reviewing or matching everything in the account's Pending tab before you disconnect, because the feed can download them again after you reconnect and create duplicates. Disconnecting removes the bank feed, and nothing new syncs for that account until you link it again."),
    ],
    "sources": [
        ("QuickBooks: What to do if you get a bank error or can't download transactions in QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-ca/help-article/manage-workflows/get-bank-error-download-transactions-quickbooks/L0xmVo0w1_CA_en_CA"),
        ("QuickBooks: Fix bank connection errors in QuickBooks", "https://quickbooks.intuit.com/learn-support/en-uk/help-article/bank-feeds/fix-bank-connection-errors-quickbooks/L39sZN1lJ_GB_en_GB"),
        ("QuickBooks: Fix bank error 103 in QuickBooks Online", "https://quickbooks.intuit.com/learn-support/en-ca/help-article/banking/fix-bank-error-103/L5VJSg75w_CA_en_CA"),
        ("QuickBooks: Fix your bank error 102 and 105", "https://quickbooks.intuit.com/learn-support/en-ca/help-article/banking/fix-bank-error-102-105/L5MRNfzfs_CA_en_CA"),
        ("QuickBooks Online pricing", "https://quickbooks.intuit.com/pricing/"),
    ],
})
