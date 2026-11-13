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
