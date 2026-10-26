# Generic category pages. Exec'd inside build.py's namespace (uses page, LOGO, DOMAIN, YEAR, newsletter, THRESHOLD).
# Each category is a dict; see categories/*.py.

def cat_score(cat, tid):
    if "_score" in cat:
        return cat["_score"](tid)
    return int(sum(w * r for (_, w), r in zip(cat["criteria"], cat["tools"][tid]["scores"])) / 5 + 0.5)


def _spec(cat, tid, score_label="Vettlo score"):
    t = cat["tools"][tid]
    g = t["g2"]
    return (f'<div class="spec"><div><span class="label">Starting price</span><b>{t["price"]}</b><span class="small muted">{t["price_note"]}</span></div>'
            f'<div><span class="label">Free trial / plan</span><b>{t["trial"]}</b></div>'
            f'<div><span class="label">{score_label}</span><b>{cat_score(cat, tid)}/100</b></div>'
            f'<div><span class="label">G2 user rating</span><b>{g[0]}/5</b><a class="small" href="{g[2]}" target="_blank" rel="noopener">{g[1]} reviews</a></div></div>')


def _breakdown(cat, tid):
    return "".join(f'<div class="crit"><span class="nm">{n} <span class="muted small">({w}%)</span></span><span class="w">{r:g}/5</span><span class="bar"><i style="width:{r*20}%"></i></span></div>'
                   for (n, w), r in zip(cat["criteria"], cat["tools"][tid]["scores"]))


def _byline(url, cat):
    return (byline(url, cat["date"], cat["date"]) +
            '<p class="disclose">We may earn a commission when you click some links on this page. It never changes which tools we include or how we rank them. '
            'See <a href="/how-we-make-money/">how we make money</a>.</p>')


def _author_box():
    return (f'<section class="author-box"><div class="avatar team-mark">{LOGO}</div><div><b>Vettlo Editorial Team</b>'
            '<p class="small muted">Researched and written by the Vettlo editorial team using our <a href="/methodology/">methodology</a>. '
            'Prices and plan details come from each vendor\'s public pricing page.</p></div></section>')


def _faq(faqs):
    return "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)


def _ld(h1, url, date, crumbs, items, faqs):
    return [
        {"@context": "https://schema.org", "@type": "Article", "headline": h1, "datePublished": date, "dateModified": page_dates(url, date, date)[0],
         "author": {"@type": "Organization", "name": "Vettlo Editorial Team", "url": DOMAIN + "/team/"},
         "publisher": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN}, "mainEntityOfPage": DOMAIN + url},
        *([] if not items else [{"@context": "https://schema.org", "@type": "ItemList", "name": h1,
         "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "url": f"{DOMAIN}{url}#{tid}"} for i, (tid, n) in enumerate(items, 1)]}]),
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": DOMAIN + h} for i, (h, n) in enumerate(crumbs, 1)]},
    ]


def _lc(t):
    """Lowercase the first letter unless it starts a proper name (e.g. "Free Forever plan")."""
    w = t.split()
    return t if len(w) > 1 and w[1][:1].isupper() else t[:1].lower() + t[1:]


def _noun(cat):
    pl = cat["plural"].lower().replace("b2b", "B2B").replace("crm", "CRM")
    return pl.replace(" software", " tools") if pl.endswith(" software") else pl


def category_page(cat):
    tools = cat["tools"]
    ranked = sorted([k for k in tools if cat_score(cat, k) >= THRESHOLD], key=lambda k: (-cat_score(cat, k), -float(tools[k]["g2"][0])))
    excluded = [k for k in tools if cat_score(cat, k) < THRESHOLD]
    cat["_ranked"] = ranked
    BADGES.extend((cat["crumb"], cat["slug"], k, tools[k]["name"], i) for i, k in enumerate(ranked, 1))
    SCOREBOARD.append((cat["crumb"], tools[ranked[0]]["name"], cat_score(cat, ranked[0]), f"/tools/{cat['slug']}/", len(tools)))
    url = f"/tools/{cat['slug']}/"
    n = len(ranked)
    h1 = f"{n} Best {cat['plural']} in {YEAR}"
    short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{k}">{tools[k]["name"]}</a><br><span class="bf">{tools[k]["bf"]}</span></span><span class="sc">{cat_score(cat, k)}<small>/100</small></span><a class="btn ghost small" href="#{k}">Review</a></li>' for i, k in enumerate(ranked, 1))
    rows = "".join(f'<tr><td class="num">{i}</td><td><a href="#{k}"><b>{tools[k]["name"]}</b></a></td><td>{tools[k]["bf"].replace("Best for ", "").capitalize()}</td><td>{tools[k]["trial_short"]}</td><td class="num">{tools[k]["price"]}</td><td class="num">{tools[k]["g2"][0]}/5</td><td class="num"><b>{cat_score(cat, k)}</b>/100</td></tr>' for i, k in enumerate(ranked, 1))
    cards = []
    for i, k in enumerate(ranked, 1):
        t = tools[k]
        links = "".join(f'<a href="{h}">{x} →</a> ' for h, x in t.get("links", []))
        cards.append(f"""<article class="tool" id="{k}">
<div class="tool-head"><span class="num">{i}</span><div><h3>{t['name']}</h3><div class="bestfor">{t['bf']}</div></div>
<a class="btn small" href="{t['url']}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
{_spec(cat, k)}
<div class="tool-body">
<p>{t['what']}</p>
<div><h4>Who it's best for</h4><p>{t['who']}</p></div>
<div><h4>Why it made the shortlist</h4><p>{t['why']}</p></div>
<div class="pc"><div class="pros"><h4>Strengths</h4><ul>{''.join(f'<li>{p}</li>' for p in t['pros'])}</ul></div><div class="cons"><h4>Watch-outs</h4><ul>{''.join(f'<li>{c}</li>' for c in t['cons'])}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {t['skip']}</p>
<p class="small"><!--CMPLINKS:{cat['slug']}:{k}-->{links}</p>
<details class="breakdown"><summary>Score breakdown</summary><div class="criteria">{_breakdown(cat, k)}</div></details>
</div></article>""")
    also = ""
    if excluded:
        items = "".join(f'<li><b>{tools[k]["name"]}</b> scored {cat_score(cat, k)}/100. {tools[k]["what"]} {tools[k].get("excluded_note", "")}</li>' for k in excluded)
        also = f'<section id="also"><h2>Also considered</h2><ul class="prose">{items}</ul></section>'
    crit = "".join(f'<div class="crit"><span class="nm">{nm}</span><span class="w">{w}%</span><span class="bar"><i style="width:{w*4}%"></i></span></div>' for nm, w in cat["criteria"])
    choose = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in cat["choose"])
    rel = "".join(f'<li><a href="{h}">{x}</a></li>' for h, x in cat.get("related", []))
    toc = "".join(f'<a href="#{a}">{b}</a>' for a, b in [("answer", "Short answer"), ("shortlist", "Shortlist"), ("compare", "Comparison table"), ("reviews", "Reviews"), ("criteria", "How we scored"), ("choose", "How to choose"), ("faq", "FAQ")])
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(cat['slug'])} / {cat['crumb']}</nav>
<header class="article-head"><span class="eyebrow">Shortlist · {cat['crumb']}</span><h1>{h1}</h1>{_byline(url, cat)}</header>
<div class="layout"><div class="main-col">
{answer_box(f"<b>{tools[ranked[0]]['name']}</b> is our top pick among the {n} {_noun(cat)} we ranked, scoring {cat_score(cat, ranked[0])}/100." + (f" Paid plans start at {tools[ranked[0]]['price'].replace('From ', '')}." if tools[ranked[0]]['price'][:1] in '$€F' else ""), [(tools[k]["name"], cat_score(cat, k), tools[k]["bf"]) for k in ranked[:5]])}
<section class="prose">{''.join(f'<p>{p}</p>' for p in cat['intro'])}</section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<aside class="trust" aria-label="Why trust this review"><span class="label">Why trust this review</span>
<div class="facts"><div><b>{len(tools)} tools</b><span class="small muted">scored</span></div><div><b>{len(cat['criteria'])}</b><span class="small muted">weighted criteria</span></div><div><b>0</b><span class="small muted">paid positions</span></div><div><b>90 days</b><span class="small muted">re-check cycle</span></div></div>
<p class="small muted">Prices and plans checked against each vendor's pricing page on {hdate(page_dates(url, cat['date'], cat['date'])[1])}. Vendors cannot pay for a position.</p></aside>
<section id="compare"><h2>{cat['plural']} compared</h2>
<div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Best for</th><th>Free plan / trial</th><th>Starting price</th><th>G2 rating</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">{cat['price_footnote']}</p></section>
<section id="reviews"><h2>The reviews</h2>{''.join(cards)}</section>
{also}
<section id="criteria"><h2>How we scored {cat['plural'].lower()}</h2>
<p class="prose">Each tool gets a 0 to 5 rating on every criterion. We weight the ratings below, convert the total to a score out of 100, and only rank tools that score {THRESHOLD} or higher. Open any tool's <b>Score breakdown</b> to see its ratings. Full process on our <a href="/methodology/">methodology page</a>.</p>
<div class="criteria">{crit}</div></section>
<section id="choose" class="prose"><h2>How to choose {cat['choose_title']}</h2><ul>{choose}</ul></section>
<section id="faq"><h2>{cat['crumb']} FAQ</h2><div>{_faq(cat['faqs'])}</div></section>
<section class="prose"><h2>Related</h2><ul><!--COMPARES:{cat['slug']}-->{rel}</ul></section>
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span>{toc}</nav></div></div>
{newsletter()}"""
    crumbs = [("/", "Home"), dept_crumb_ld(cat["slug"]), (url, cat["crumb"])]
    page(url, f"{n} Best {cat['plural']} ({YEAR}) | Vettlo", cat["desc"], body, cur="/best-tools/", ptype="article",
         jsonld=_ld(h1, url, cat["date"], crumbs, [(k, tools[k]["name"]) for k in ranked], cat["faqs"]))


def alternatives_page(cat, target, slug, lede, reasons, picks, faqs, related):
    tools = cat["tools"]
    tname = tools[target]["short"]
    url = f"/tools/{slug}/"
    n = len(picks)
    h1 = f"{n} Best {tname} Alternatives in {YEAR}"
    short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{k}">{tools[k]["name"]}</a><br><span class="bf">{fit}</span></span><span class="sc">{cat_score(cat, k)}<small>/100</small></span><a class="btn ghost small" href="#{k}">Details</a></li>' for i, (k, fit, _, _) in enumerate(picks, 1))
    ref = tools[target]
    rows = (f'<tr class="ref"><td><b>{ref["name"]}</b> <span class="small muted">(for reference)</span></td><td>{ref["bf"].replace("Best for ", "").capitalize()}</td><td class="num">{ref["price"]}</td><td>{ref["trial_short"]}</td><td class="num"><b>{cat_score(cat, target)}</b>/100</td></tr>'
            + "".join(f'<tr><td><a href="#{k}"><b>{tools[k]["name"]}</b></a></td><td>{fit}</td><td class="num">{tools[k]["price"]}</td><td>{tools[k]["trial_short"]}</td><td class="num"><b>{cat_score(cat, k)}</b>/100</td></tr>' for k, fit, _, _ in picks))
    cards = []
    for i, (k, fit, gain, lose) in enumerate(picks, 1):
        t = tools[k]
        cards.append(f"""<article class="tool" id="{k}">
<div class="tool-head"><span class="num">{i}</span><div><h3>{t['name']}</h3><div class="bestfor">{fit}</div></div>
<a class="btn small" href="{t['url']}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>
{_spec(cat, k)}
<div class="tool-body"><p>{t['what']}</p>
<div class="pc"><div class="pros"><h4>What you gain over {tname}</h4><ul>{''.join(f'<li>{g}</li>' for g in gain)}</ul></div><div class="cons"><h4>What you give up</h4><ul>{''.join(f'<li>{l}</li>' for l in lose)}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {t['skip']}</p></div></article>""")
    reason_html = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in reasons)
    rel = f"<!--COMPARES:{cat['slug']}-->" + "".join(f'<li><a href="{h}">{x}</a></li>' for h, x in related)
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(cat['slug'])} / <a href="/tools/{cat['slug']}/">{cat['crumb']}</a> / {tname} alternatives</nav>
<header class="article-head"><span class="eyebrow">Alternatives · {cat['crumb']}</span><h1>{h1}</h1>{_byline(url, cat)}</header>
<div class="layout"><div class="main-col">
{answer_box(f"The best {tname} alternative for most teams is <b>{tools[picks[0][0]]['name']}</b> ({cat_score(cat, picks[0][0])}/100). {picks[0][2][0]}; {_lc(picks[0][2][1])}.", [(tools[k]["name"], cat_score(cat, k), f) for k, f, _, _ in picks[:5]])}
<section class="prose"><p>{lede}</p></section>
<section class="prose" id="why"><h2>Why teams look for {tname} alternatives</h2><ul>{reason_html}</ul></section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<section id="compare"><h2>{tname} alternatives compared</h2>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Why pick it</th><th>Starting price</th><th>Free plan / trial</th><th>Vettlo score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">{cat['price_footnote']} Scores use the same weighted criteria as our <a href="/tools/{cat['slug']}/">{cat['plural'].lower()} ranking</a>.</p></section>
<section id="reviews"><h2>The alternatives</h2>{''.join(cards)}</section>
<section class="prose"><h2>How we picked these alternatives</h2><p>Every tool here comes from our <a href="/tools/{cat['slug']}/">{cat['plural'].lower()} shortlist</a>. We ordered them by how well each one solves the most common reasons teams leave {tname}, not only by overall score. See our <a href="/methodology/">methodology</a>.</p></section>
<section id="faq"><h2>{tname} alternatives FAQ</h2><div>{_faq(faqs)}</div></section>
<section class="prose"><h2>Related</h2><ul>{rel}</ul></section>
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#why">Why switch</a><a href="#shortlist">Shortlist</a><a href="#compare">Comparison table</a><a href="#reviews">The alternatives</a><a href="#faq">FAQ</a></nav></div></div>
{newsletter()}"""
    crumbs = [("/", "Home"), dept_crumb_ld(cat["slug"]), (f"/tools/{cat['slug']}/", cat["crumb"]), (url, f"{tname} alternatives")]
    CLUSTER.setdefault(cat["slug"], []).append((url, f"Best {tname} alternatives", "Alternatives"))
    page(url, f"{n} Best {tname} Alternatives ({YEAR}) | Vettlo",
         f"The best {tname} alternatives compared on price, free plans, features and fit, with what you gain and give up with each.",
         body, cur="/best-tools/", ptype="article", jsonld=_ld(h1, url, cat["date"], crumbs, [(k, tools[k]["name"]) for k, _, _, _ in picks], faqs))


CATEGORY_PAGES = []  # (url, title, blurb, kind) collected for hubs and llms.txt
BADGES = []  # (category, slug, tool id, tool name, rank) for /badges/
CLUSTER = {}  # category slug -> [(url, title, kind)] supporting pages (alternatives, comparisons)
SCOREBOARD = []  # (category, top tool, score, url, tools scored) for the home scoreboard


COMPARES = {}  # category slug -> [(url, title)] for links from the category page


def compare_page(cat, a, b, date, pick_a, pick_b, summary, cost_intro, cost_rows, cost_note, feature_rows,
                 a_strengths, b_strengths, decide, faqs, desc=None):
    """Head-to-head comparison of two tools from one category's data."""
    tools = cat["tools"]
    A, B = tools[a], tools[b]
    an, bn = A["short"], B["short"]
    slug = f"{a.replace('_', '-')}-vs-{b.replace('_', '-')}"
    url = f"/compare/{slug}/"
    sa, sb = cat_score(cat, a), cat_score(cat, b)
    h1 = f"{an} vs {bn}: Which Should You Choose in {YEAR}?"
    lead = (f"In our <a href=\"/tools/{cat['slug']}/\">{' '.join(w if w.isupper() else w.lower() for w in cat['crumb'].split())} ranking</a>, <b>{A['name']}</b> scores <b>{sa}/100</b> "
            f"and <b>{B['name']}</b> scores <b>{sb}/100</b>. {summary}")
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    cost = "".join(f'<tr><td>{n}</td><td>{ap}</td><td class="num">{ac}</td><td>{bp}</td><td class="num">{bc}</td></tr>' for n, ap, ac, bp, bc in cost_rows)
    feats = feature_rows + [("G2 user rating", f"{A['g2'][0]}/5 ({A['g2'][1]} reviews)", f"{B['g2'][0]}/5 ({B['g2'][1]} reviews)"),
                            ("Vettlo score", f"{sa}/100", f"{sb}/100")]
    frows = "".join(f'<tr><td>{f}</td><td>{x}</td><td>{y}</td></tr>' for f, x, y in feats)
    strengths = lambda xs: "".join(f"<li><b>{h}</b> {t}</li>" for h, t in xs)
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(cat['slug'])} / <a href="/tools/{cat['slug']}/">{cat['crumb']}</a> / {an} vs {bn}</nav>
<header class="article-head"><span class="eyebrow">Comparison · {cat['crumb']}</span><h1>{h1}</h1>{_byline(url, cat if date == cat['date'] else dict(cat, date=date))}</header>
<div class="layout"><div class="main-col">
<section class="verdict" id="answer" aria-label="Short answer"><h2>Short answer</h2>
<p>{lead}</p>
<div class="vs"><div><h3>Pick {an} if…</h3><ul>{li(pick_a)}</ul></div><div><h3>Pick {bn} if…</h3><ul>{li(pick_b)}</ul></div></div></section>
<section id="cost"><h2>What it costs</h2><p class="prose">{cost_intro}</p>
<div class="table-wrap"><table><thead><tr><th>Need</th><th>{an} plan</th><th>{an} per year</th><th>{bn} plan</th><th>{bn} per year</th></tr></thead><tbody>{cost}</tbody></table></div>
<p class="small muted">{cost_note} Prices from <a href="{A['url']}" target="_blank" rel="noopener">{an}</a> and <a href="{B['url']}" target="_blank" rel="noopener">{bn}</a> pricing pages, checked {hdate(page_dates(url, date, date)[1])}. Vendors change plans often; confirm before you buy.</p></section>
<section id="features"><h2>Plans and features side by side</h2>
<div class="table-wrap"><table><thead><tr><th>Feature</th><th>{an}</th><th>{bn}</th></tr></thead><tbody>{frows}</tbody></table></div>
<p class="small muted">"Listed from" means the feature first appears on that plan on the vendor's public pricing page.</p></section>
<section class="prose"><h2>Where {an} is stronger</h2><ul>{strengths(a_strengths)}</ul>
<h2>Where {bn} is stronger</h2><ul>{strengths(b_strengths)}</ul>
<h2>How to decide</h2><ol>{li(decide)}</ol></section>
<section id="faq"><h2>{an} vs {bn} FAQ</h2><div>{_faq(faqs)}</div></section>
<section class="prose"><h2>Other options</h2><p>If neither fits, see our full <a href="/tools/{cat['slug']}/">ranking of {len(cat.get('_ranked', tools))} {_noun(cat)}</a>, with who each one is for and what it costs.{"".join(f' Or see our guide to the <a href="{h}">{x.lower().replace(an.lower(), an).replace(bn.lower(), bn)}</a>.' for h, x in A.get("links", []) + B.get("links", []))}</p></section>
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#answer">Short answer</a><a href="#cost">Cost</a><a href="#features">Features</a><a href="#faq">FAQ</a></nav></div></div>
{newsletter()}"""
    crumbs = [("/", "Home"), dept_crumb_ld(cat["slug"]), (f"/tools/{cat['slug']}/", cat["crumb"]), (url, f"{an} vs {bn}")]
    page(url, f"{an} vs {bn} ({YEAR}): Pricing Compared | Vettlo",
         desc or f"{A['name']} vs {B['name']} compared on real prices, plan features and team fit, with a clear pick for each type of team.",
         body, cur="/best-tools/", ptype="article",
         jsonld=_ld(h1, url, date, crumbs, [], faqs))
    COMPARES.setdefault(cat["slug"], []).append((url, f"{an} vs {bn}"))
    CLUSTER.setdefault(cat["slug"], []).append((url, f"{an} vs {bn}", "Comparison"))
    COMPARES.setdefault(f"{cat['slug']}:{a}", []).append((url, f"{an} vs {bn}"))
    COMPARES.setdefault(f"{cat['slug']}:{b}", []).append((url, f"{an} vs {bn}"))
    CATEGORY_PAGES.append((url, f"{an} vs {bn}", f"{A['name']} and {B['name']} compared on price, features and fit.", "Comparison"))
