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
<p>Free plans: {", ".join(_crm_free) if _crm_free else "none of the ranked CRMs list one"}. Watch for one-time onboarding fees on higher tiers and for add-ons such as AI, calling or extra storage. For a full cost breakdown by team, see our <a href="/compare/hubspot-vs-pipedrive/">HubSpot vs Pipedrive</a> and <a href="/compare/salesforce-vs-hubspot/">Salesforce vs HubSpot</a> comparisons.</p>"""),
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
