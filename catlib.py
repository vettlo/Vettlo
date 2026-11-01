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
            '<p class="disclose">We may earn money when you click links on this page. Partner compensation may affect which products we include and where they appear. '
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


def _cap(s):
    return s[:1].upper() + s[1:]


def _pl(cat):
    return cat.get("plural_lc") or cat["plural"].lower().replace("b2b", "B2B").replace("crm", "CRM")


def _noun(cat):
    pl = _pl(cat)
    return pl.replace(" software", " tools") if pl.endswith(" software") else pl


def category_page(cat):
    tools = cat["tools"]
    ranked = sorted([k for k in tools if cat_score(cat, k) >= THRESHOLD], key=lambda k: (-cat_score(cat, k), -float(tools[k]["g2"][0])))
    excluded = [k for k in tools if cat_score(cat, k) < THRESHOLD]
    cat["_ranked"] = ranked
    if cat not in ALLCATS:
        ALLCATS.append(cat)
    for _t in tools.values():
        LOGOS[_t["name"]] = _t["url"]; LOGOS[_t["short"]] = _t["url"]
    PRICEROWS[cat["slug"]] = dict(noun=_noun(cat), plural=cat["plural"], others=cat.get("others", []), rows=[(tools[k]["name"], tools[k]["price"], tools[k]["price_note"], tools[k]["trial"], f"#{k}") for k in ranked])
    BADGES.extend((cat["crumb"], cat["slug"], k, tools[k]["name"], i) for i, k in enumerate(ranked, 1))
    SCOREBOARD.append((cat["crumb"], tools[ranked[0]]["name"], cat_score(cat, ranked[0]), f"/tools/{cat['slug']}/", len(tools)))
    url = f"/tools/{cat['slug']}/"
    n = len(ranked)
    h1 = f"{n} Best {cat['plural']} in {YEAR}"
    short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{k}">{tools[k]["name"]}</a><br><span class="bf">{tools[k]["bf"]}</span></span><span class="sc">{cat_score(cat, k)}<small>/100</small></span><a class="btn ghost small" href="#{k}">Review</a></li>' for i, k in enumerate(ranked, 1))
    rows = "".join(f'<tr><td class="num">{i}</td><td><a href="#{k}"><b>{tools[k]["name"]}</b></a></td><td>{_cap(tools[k]["bf"].replace("Best for ", ""))}</td><td>{tools[k]["trial_short"]}</td><td class="num">{tools[k]["price"]}</td><td class="num">{tools[k]["g2"][0]}/5</td><td class="num"><b>{cat_score(cat, k)}</b>/100</td></tr>' for i, k in enumerate(ranked, 1))
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
    toc = "".join(f'<a href="#{a}">{b}</a>' for a, b in [("answer", "Short answer"), ("shortlist", "Shortlist"), ("compare", "Comparison table"), ("reviews", "Reviews"), ("what-is", "What it is"), ("pricing", "Pricing"), ("criteria", "How we scored"), ("choose", "How to choose"), ("faq", "FAQ")])
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(cat['slug'])} / {cat['crumb']}</nav>
<header class="article-head"><span class="eyebrow">Shortlist · {cat['crumb']}</span><h1>{h1}</h1>{_byline(url, cat)}</header>
<div class="layout"><div class="main-col">
{answer_box(f"<b>{tools[ranked[0]]['name']}</b> is our top pick among the {n} {_noun(cat)} we ranked, scoring {cat_score(cat, ranked[0])}/100." + (f" Paid plans start at {tools[ranked[0]]['price'].replace('From ', '')}." if tools[ranked[0]]['price'][:1] in '$€F' else ""), [(tools[k]["name"], cat_score(cat, k), tools[k]["bf"]) for k in ranked[:5]])}
<section class="prose">{''.join(f'<p>{p}</p>' for p in cat['intro'])}</section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<aside class="trust" aria-label="Why trust this review"><span class="label">Why trust this review</span>
<div class="facts"><div><b>{len(tools)} tools</b><span class="small muted">scored</span></div><div><b>{len(cat['criteria'])}</b><span class="small muted">weighted criteria</span></div><div><b>{n}</b><span class="small muted">ranked</span></div><div><b>90 days</b><span class="small muted">re-check cycle</span></div></div>
<p class="small muted">Prices and plans checked against each vendor's pricing page on {hdate(page_dates(url, cat['date'], cat['date'])[1])}. Vendors cannot pay for a score.</p></aside>
<section id="compare"><h2>{cat['plural']} compared</h2>
<div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Best for</th><th>Free plan / trial</th><th>Starting price</th><th>G2 rating</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">{cat['price_footnote']}</p></section>
<section id="reviews"><h2>The reviews</h2>{''.join(cards)}</section>
{also}
<!--EXPLAIN:{cat['slug']}-->
<section id="criteria"><h2>How we scored {cat.get('plural_lc', cat['plural'].lower())}</h2>
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
    rows = (f'<tr class="ref"><td><b>{ref["name"]}</b> <span class="small muted">(for reference)</span></td><td>{_cap(ref["bf"].replace("Best for ", ""))}</td><td class="num">{ref["price"]}</td><td>{ref["trial_short"]}</td><td class="num"><b>{cat_score(cat, target)}</b>/100</td></tr>'
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
<p class="small muted">{cat['price_footnote']} Scores use the same weighted criteria as our <a href="/tools/{cat['slug']}/">{cat.get('plural_lc', cat['plural'].lower())} ranking</a>.</p></section>
<section id="reviews"><h2>The alternatives</h2>{''.join(cards)}</section>
<section class="prose"><h2>How we picked these alternatives</h2><p>Every tool here comes from our <a href="/tools/{cat['slug']}/">{cat.get('plural_lc', cat['plural'].lower())} shortlist</a>. We ordered them by how well each one solves the most common reasons teams leave {tname}, not only by overall score. See our <a href="/methodology/">methodology</a>.</p></section>
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
ALLCATS = []  # every category dict passed to category_page, in build order
REVIEW_URL = {}  # tool name -> review page URL


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


# ---------- LOGOS: vendor icons next to tool names (decorative; the name is always shown as text)
LOGOS = {}


def _logo_img(url, size):
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    return (f'<img class="tlogo tlogo-{size}" src="https://www.google.com/s2/favicons?domain={host}&amp;sz={128 if size > 24 else 64}" '
            f'alt="" width="{size}" height="{size}" loading="lazy" decoding="async">')


def add_logos():
    names = sorted(LOGOS, key=len, reverse=True)
    if not names:
        return
    alt = "|".join(re.escape(n) for n in names)
    pats = [
        (re.compile(r'(<div class="tool-head"><span class="num">\d+</span><div><h3>)(' + alt + r')(</h3>)'), 40),
        (re.compile(r'(<a class="nm" href="#[^"]+">)(' + alt + r')(</a>)'), 24),
        (re.compile(r'(<td><a href="#[^"]+"><b>)(' + alt + r')(</b></a></td>)'), 20),
        (re.compile(r'(<h3>Pick )(' + alt + r')( if…</h3>)'), 24),
    ]
    for path, pg in PAGES.items():
        b = pg["body"]
        for rx, size in pats:
            b = rx.sub(lambda m: m.group(1) + _logo_img(LOGOS[m.group(2)], size) + m.group(2) + m.group(3), b)
        pg["body"] = b


# ---------- EXPLAINERS on shortlists: what it is, key features, pricing overview, other tools
PRICEROWS = {}
_FREE = re.compile(r"free (plan|forever|tools|starter plan|for up to|for \d|2-person)|free plan", re.I)


def explainer_sections(slug, only_what=False):
    ex = EXPLAIN.get(slug) if "EXPLAIN" in globals() else None
    pr = PRICEROWS.get(slug)
    out = ""
    if ex:
        name = next((c[1] for c in CATS if c[0] == slug), "this software")
        nm = _catname(name)
        feats = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in ex.get("features", []))
        more = f' Read our full guide: <a href="{ex["guide"]}">{next((t for u, t, *_r in GUIDES if u == ex["guide"]), "guide")}</a>.' if ex.get("guide") else ""
        out += (f'<section id="what-is" class="prose"><h2>What is {nm[:-1] if nm.endswith("tools") and False else nm}?</h2><p>{ex["what"]}{more}</p>'
                + (f'<h3>Key features to look for</h3><ul>{feats}</ul>' if feats else "") + "</section>")
    if pr and pr["rows"] and not only_what:
        rows = pr["rows"]
        priced = sorted([(_money(p), n, p, a) for n, p, nt, t, a in rows if _money(p)], key=lambda x: x[0])
        onreq = [n for n, p, nt, t, a in rows if not _money(p) and not p[:1] in "€£"]
        other_cur = [(n, p) for n, p, nt, t, a in rows if p[:1] in "€£"]
        free = [n for n, p, nt, t, a in rows if _FREE.search(t)]
        lis = "".join(f'<li><a href="{a}">{n}</a>: {p}</li>' for v, n, p, a in priced) + "".join(f"<li>{n}: {p}</li>" for n, p in other_cur)
        summary = []
        if priced:
            summary.append(f"Among the {len(rows)} {pr['noun']} we ranked, published entry prices start at {priced[0][2].replace("From ", "")} ({priced[0][1]})" + (f" and go up to {priced[-1][2].replace("From ", "")} ({priced[-1][1]})" if len(priced) > 1 else "") + ". Units differ by vendor (per user, per agent, per contact tier or flat), so compare at your own team size.")
        if free:
            summary.append(f"Free plans: {', '.join(free)}.")
        if onreq:
            summary.append(f"No published price: {', '.join(onreq)}.")
        out += (f'<section id="pricing" class="prose"><h2>How much {pr["plural"].lower().replace("crm", "CRM").replace("b2b", "B2B").replace("hris", "HRIS")} cost{"" if pr["plural"].endswith("s") and not pr["plural"].endswith("Software") else "s"}</h2><p>{" ".join(summary)}</p>'
                f'<ul>{lis}</ul><p class="small muted">Entry prices from each vendor\'s pricing page, as shown in the comparison table above. Higher tiers usually add automation, reporting and admin controls.</p></section>')
    if pr and pr.get("others"):
        ol = "".join(f'<li><b>{n}</b>: {d}</li>' for n, d in pr["others"])
        out += (f'<section id="others" class="prose"><h2>Other {pr["noun"]} to consider</h2>'
                f'<p>These tools didn\'t make our ranked shortlist but are worth a look for specific needs. We haven\'t scored them.</p><ol start="{len(pr["rows"]) + 1}">{ol}</ol></section>')
    return out


def fill_explainers():
    for path, pg in PAGES.items():
        for m in re.findall(r"<!--EXPLAIN:([^>]*)-->", pg["body"]):
            sl, _, mode = m.partition(":")
            pg["body"] = pg["body"].replace(f"<!--EXPLAIN:{m}-->", explainer_sections(sl, mode == "what"))


# ---------- GUIDES (topics): explainers, pricing breakdowns and buying advice
GUIDES = []


def _money(price):
    """Numeric monthly price from strings like "$19/agent/mo"; None for non-dollar or unpriced."""
    m = re.match(r"\$([\d,]+(?:\.\d+)?)", price.replace("From ", ""))
    return float(m.group(1).replace(",", "")) if m else None


def _fmt(x):
    return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"


def guide_page(g):
    """g: slug, title, seo_title, desc, dept, cats, date, kicker, answer, sections [(id, h2, html)], faqs, sources [(title, url)]."""
    url = f"/guides/{g['slug']}/"
    dname = g["dept"]
    dslug = DEPT_SLUG[dname]
    secs = "".join(f'<section id="{sid}" class="prose"><h2>{h}</h2>{html_}</section>' for sid, h, html_ in g["sections"])
    rel_html = f"<!--GUIDEREL:{','.join(g.get('cats', []))}-->" if g.get("cats") else ""
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in g.get("sources", []))
    toc = '<a href="#answer">Short answer</a>' + "".join(f'<a href="#{sid}">{h}</a>' for sid, h, _ in g["sections"]) + '<a href="#faq">FAQ</a>'
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / <a href="/guides/#{dslug}">{dname}</a> / {g['crumb']}</nav>
<header class="article-head"><span class="eyebrow">{g.get('kicker', 'Guide')} · {dname}</span><h1>{g['title']}</h1>{byline(url, g['date'], g['date'])}</header>
<div class="layout"><div class="main-col">
<section class="answer" id="answer" aria-label="Short answer"><h2>Short answer</h2><p>{g['answer']}</p></section>
{secs}
<section id="faq"><h2>FAQ</h2><div>{_faq(g['faqs'])}</div></section>
{f'<section class="prose"><h2>Related reviews</h2><ul>{rel_html}</ul></section>' if rel_html else ''}
{f'<section class="prose"><h2>Sources</h2><ul class="small">{src}</ul></section>' if src else ''}
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span>{toc}</nav></div></div>
{newsletter()}"""
    crumbs = [("/", "Home"), ("/guides/", "Guides"), (url, g["crumb"])]
    page(url, g["seo_title"], g["desc"], body, cur="/guides/", ptype="article", jsonld=_ld(g["title"], url, g["date"], crumbs, [], g["faqs"]))
    GUIDES.append((url, g["title"], g["card"], dname, g.get("cats", []), g.get("kicker", "Guide")))


def guides_index():
    if GUIDES:
        cards = "".join(f'<a href="{u}"><span class="label">{k} · {d}</span><b>{t}</b><span class="muted small">{c}</span></a>' for u, t, c, d, _c, k in GUIDES[-3:][::-1])
        PAGES["/"]["body"] = PAGES["/"]["body"].replace("<!--HOMEGUIDES-->", f'''<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Guides</span><h2 style="margin-top:.4rem">Guides and pricing breakdowns</h2>
<p>What each category does, what it really costs and how to choose, from the same research behind our shortlists.</p></div>
<a class="btn ghost small" href="/guides/">All guides</a></div>
<div class="guide-grid">{cards}</div></div></section>''')
    PAGES["/"]["body"] = PAGES["/"]["body"].replace("<!--HOMEGUIDES-->", "")
    for url, *_r in GUIDES:
        b = PAGES[url]["body"]
        m = re.search(r"<!--GUIDEREL:([^>]*)-->", b)
        if not m:
            continue
        rel = []
        for cs in m.group(1).split(","):
            name = next((c[1] for c in CATS if c[0] == cs), cs)
            rel.append((f"/tools/{cs}/", f"Best {_catname(name)}"))
            rel += [(u, t) for u, t, _ in CLUSTER.get(cs, [])][:3]
        PAGES[url]["body"] = b.replace(m.group(0), "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in rel))
    by = {}
    for url, t, card, d, cats, k in GUIDES:
        by.setdefault(d, []).append((url, t, card, k))
    body = f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Guides</span><h1>Software guides for every team</h1>
<p>Explainers, pricing breakdowns and buying advice, written from the same research behind our shortlists. Every price comes from the vendor's own pricing page.</p></div>
<div class="page-body">'''
    chips = "".join(f'<a href="#{DEPT_SLUG[d]}">{d}</a>' for d, _, _ in DEPTS if d in by)
    body += f'<nav class="chips" aria-label="Guides by team">{chips}</nav>'
    for d, _, _ in DEPTS:
        if d not in by:
            continue
        cards = "".join(f'<a href="{u}"><span class="label">{k}</span><b>{t}</b><span class="muted small">{c}</span></a>' for u, t, c, k in by[d])
        body += f'<h2 class="dept-h" id="{DEPT_SLUG[d]}">{d}</h2><div class="guide-grid">{cards}</div>'
    body += '<p class="muted small" style="margin-top:2rem">Looking for a ranked list instead? See <a href="/best-tools/">all categories</a>.</p></div></div>' + newsletter()
    items = [{"@type": "ListItem", "position": i, "url": DOMAIN + u, "name": t} for i, (u, t, *_r) in enumerate(GUIDES, 1)]
    page("/guides/", "Business Software Guides: Explainers and Pricing | Vettlo",
         "Plain-English guides to business software: what each category does, what it really costs and how to choose, for sales, marketing, support, HR, finance and IT.",
         body, cur="/guides/", jsonld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Software guides", "url": DOMAIN + "/guides/",
                                       "mainEntity": {"@type": "ItemList", "itemListElement": items}}])


def link_guides():
    """Add a Guides block to each related category page and department hub."""
    for url, t, card, d, cats, k in GUIDES:
        for cs in cats:
            cu = f"/tools/{cs}/"
            if cu in PAGES:
                PAGES[cu].setdefault("_guides", []).append((url, t))
        hub = f"/{DEPT_SLUG[d]}/"
        if hub in PAGES:
            PAGES[hub].setdefault("_guides", []).append((url, t))
    for path, pg in PAGES.items():
        gs = pg.pop("_guides", None)
        if not gs:
            continue
        lis = "".join('<li><a href="%s">%s</a></li>' % (u, t) for u, t in gs)
        block = '<section class="prose"><h2>Guides</h2><ul>' + lis + '</ul></section>\n'
        b = pg["body"]
        for marker in ('<section class="author-box">', '<section id="faq">'):
            i = b.find(marker)
            if i > 0:
                pg["body"] = b[:i] + block + b[i:]
                break



# ---------- TOOL REVIEWS and CATEGORY VARIANTS (generated from the same verified category data)
def _tslug(name):
    n = name.strip().lower()
    n = n if n in ("customer.io",) else re.sub(r"\.(io|com|ai)$", "", n)
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def _price_sentence(t):
    p = t["price"]
    if p[:1] in "$€£" or p.startswith("From"):
        return f"Paid plans start at {p.replace('From ', '')} ({t['price_note']})."
    return f"{p}: {t['price_note']}."


def _cat_link(cat):
    return f'<a href="/tools/{cat["slug"]}/">{_noun(cat)} ranking</a>'


def review_pages(cats):
    by = {}
    for cat in cats:
        for i, k in enumerate(cat.get("_ranked", []), 1):
            t = cat["tools"][k]
            by.setdefault(t["name"], []).append((cat, k, i))
    for name, entries in by.items():
        REVIEW_URL[name] = f"/tools/{_tslug(name)}-review/"
    for name, entries in by.items():
        entries.sort(key=lambda e: -cat_score(e[0], e[1]))
        cat, k, rank = entries[0]
        t = cat["tools"][k]
        url = REVIEW_URL[name]
        date = max(page_dates(f"/tools/{c['slug']}/", c["date"], c["date"])[1] for c, _, _ in entries)
        s0 = cat_score(cat, k)
        ranks = " and ".join(f"#{r} of {len(c['_ranked'])} in our {_cat_link(c)} ({cat_score(c, kk)}/100)" for c, kk, r in entries)
        answer = f"{name} ranks {ranks}. {_cap(_bf(t['bf']))}. {_price_sentence(t)}"
        bd = "".join(f'<h3>{c["crumb"]} score: {cat_score(c, kk)}/100</h3><div class="criteria">{_breakdown(c, kk)}</div>' for c, kk, r in entries)
        comp_rows = ""
        for c, kk, r in entries[:1]:
            for j, o in enumerate(c["_ranked"][:6], 1):
                ot = c["tools"][o]
                nm = f'<a href="{REVIEW_URL[ot["name"]]}">{ot["name"]}</a>' if ot["name"] != name else f'<b>{ot["name"]}</b>'
                comp_rows += f'<tr><td class="num">{j}</td><td>{nm}</td><td>{_cap(ot["bf"].replace("Best for ", ""))}</td><td class="num">{ot["price"]}</td><td class="num"><b>{cat_score(c, o)}</b>/100</td></tr>'
        links = []
        for c, kk, r in entries:
            links += COMPARES.get(f"{c['slug']}:{kk}", [])
            links += [(h, x) for h, x in c["tools"][kk].get("links", [])]
            links.append((f"/tools/{c['slug']}/", f"Best {_noun(c)}"))
        seen, lis = set(), ""
        for h, x in links:
            if h not in seen:
                seen.add(h); lis += f'<li><a href="{h}">{x}</a></li>'
        others = [c["tools"][o]["name"] for o in cat["_ranked"] if c["tools"][o]["name"] != name][:3] if (c := cat) else []
        faqs = [
            (f"How much does {name} cost?", _price_sentence(t) + f" {('Free plan or trial: ' + t['trial'] + '.') if t.get('trial') else ''}".rstrip()),
            (f"Is {name} worth it?", f"{name} scores {s0}/100 in our {_noun(cat)} ranking, where it is {_bf(t['bf'])}. It's a weaker fit if: {t['skip'][:1].lower() + t['skip'][1:]}"),
            (f"Does {name} have a free plan or trial?", f"{t['trial']}."),
            (f"What are the best {name} alternatives?", f"In our {_noun(cat)} ranking, the closest alternatives are {', '.join(others[:-1]) + ' and ' + others[-1] if len(others) > 1 else ''.join(others)}." if others else f"See our {_noun(cat)} ranking."),
        ]
        crumbs = [("/", "Home"), dept_crumb_ld(cat["slug"]), (f"/tools/{cat['slug']}/", cat["crumb"]), (url, f"{name} review")]
        h1 = f"{name} Review ({YEAR}): Pricing, Pros and Cons"
        body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(cat['slug'])} / <a href="/tools/{cat['slug']}/">{cat['crumb']}</a> / {name} review</nav>
<header class="article-head"><span class="eyebrow">Review · {cat['crumb']}</span><h1>{h1}</h1>{_byline(url, dict(cat, date=date))}</header>
<div class="layout"><div class="main-col">
<section class="answer" id="answer" aria-label="Short answer"><h2>Short answer</h2><p>{answer}</p></section>
<article class="tool" id="{k}"><div class="tool-head"><span class="num">{rank}</span><div><h3>{name}</h3><div class="bestfor">{t['bf']}</div></div>
<a class="btn small" href="{t['url']}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>{_spec(cat, k)}</article>
<section id="overview" class="prose"><h2>What is {name}?</h2><p>{t['what']}</p>
<h3>Who it's best for</h3><p>{t['who']}</p><h3>Why we rank it</h3><p>{t['why']}</p></section>
<section id="pros-cons"><h2>Pros and cons</h2><div class="pc"><div class="pros"><h4>Strengths</h4><ul>{''.join(f'<li>{x}</li>' for x in t['pros'])}</ul></div><div class="cons"><h4>Watch-outs</h4><ul>{''.join(f'<li>{x}</li>' for x in t['cons'])}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {t['skip']}</p></section>
<section id="pricing" class="prose"><h2>{name} pricing</h2><p>{_price_sentence(t)} Free plan or trial: {t['trial']}.</p><p class="small muted">From {name}'s pricing page, checked on the date at the top of this review. See how it compares on price in our <a href="/tools/{cat['slug']}/#pricing">{_noun(cat)} pricing overview</a>.</p></section>
<section id="score"><h2>How we scored {name}</h2>{bd}<p class="small muted">Each criterion is rated 0 to 5 and weighted for the category. See our <a href="/methodology/">methodology</a>.</p></section>
<section id="compare"><h2>How {name} compares</h2><div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Best for</th><th>Starting price</th><th>Score</th></tr></thead><tbody>{comp_rows}</tbody></table></div></section>
<section class="prose"><h2>Alternatives and comparisons</h2><ul>{lis}</ul></section>
<section id="faq"><h2>{name} FAQ</h2><div>{_faq(faqs)}</div></section>
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#answer">Short answer</a><a href="#overview">Overview</a><a href="#pros-cons">Pros and cons</a><a href="#pricing">Pricing</a><a href="#score">Score</a><a href="#compare">Compared</a><a href="#faq">FAQ</a></nav></div></div>
{newsletter()}"""
        ld = _ld(h1, url, date, crumbs, [], faqs)
        ld.append({"@context": "https://schema.org", "@type": "Review", "name": h1, "url": DOMAIN + url,
                   "author": {"@type": "Organization", "name": "Vettlo Editorial Team", "url": DOMAIN + "/team/"},
                   "publisher": {"@type": "Organization", "name": "Vettlo", "url": DOMAIN},
                   "reviewRating": {"@type": "Rating", "ratingValue": s0, "bestRating": 100, "worstRating": 0},
                   "itemReviewed": {"@type": "SoftwareApplication", "name": name, "applicationCategory": "BusinessApplication", "url": t["url"]}})
        page(url, f"{name} Review ({YEAR}): Pricing, Pros & Cons | Vettlo",
             f"{name} review: {s0}/100 in our {_noun(cat)} ranking. {_price_sentence(t)} Pros, cons, who it's for and the best alternatives."[:300],
             body, cur="/reviews/", ptype="article", jsonld=ld)
        CATEGORY_PAGES.append((url, f"{name} Review", f"{name}'s pricing, pros, cons and score, from our {_noun(cat)} ranking.", "Review"))


def insert_review_links():
    """Add 'Read our full X review' under each tool card on shortlist, alternatives and variant pages."""
    rx = re.compile(r'(<article class="tool" id="[^"]+">.*?<h3>(?:<img[^>]*>)?([^<]+)</h3>.*?)(<details class="breakdown">|</article>)', re.S)
    for path, pg in PAGES.items():
        if path.endswith("-review/"):
            continue
        def sub(m):
            u = REVIEW_URL.get(m.group(2).strip())
            if not u or u in m.group(1):
                return m.group(0)
            return m.group(1) + f'<p class="small"><a href="{u}">Read our full {m.group(2).strip()} review →</a></p>' + m.group(3)
        pg["body"] = rx.sub(sub, pg["body"])


def _smb_weights(cat):
    ws = [w for _, w in cat["criteria"]]
    boost = [i for i, (n, _) in enumerate(cat["criteria"]) if re.search(r"price|ease|usability|setup", n, re.I)]
    if not boost:
        return ws
    new = {i: max(20, round(ws[i] * 1.7)) for i in boost}
    rest = [i for i in range(len(ws)) if i not in new]
    left = 100 - sum(new.values())
    tot = sum(ws[i] for i in rest)
    out = [new.get(i, round(ws[i] * left / tot)) for i in range(len(ws))]
    out[rest[0]] += 100 - sum(out)
    return out


def _wscore(cat, k, weights):
    return int(sum(w * r for w, r in zip(weights, cat["tools"][k]["scores"])) / 5 + 0.5)


def variant_pages(cat):
    tools, slug = cat["tools"], cat["slug"]
    base = slug[len("best-"):]
    noun = _noun(cat)
    out = []
    cat = dict(cat, date=page_dates(f"/tools/{slug}/", cat["date"], cat["date"])[1])
    # --- free plans
    free = [k for k in cat.get("_ranked", []) if _FREE.search(tools[k]["trial"])]
    if len(free) >= 3:
        url = f"/tools/best-free-{base}/"
        n = len(free)
        h1 = f"{n} Best Free {cat['plural']} in {YEAR}"
        short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{k}">{tools[k]["name"]}</a><br><span class="bf">{tools[k]["trial"]}</span></span><span class="sc">{cat_score(cat, k)}<small>/100</small></span><a class="btn ghost small" href="#{k}">Details</a></li>' for i, k in enumerate(free, 1))
        rows = "".join(f'<tr><td class="num">{i}</td><td><a href="#{k}"><b>{tools[k]["name"]}</b></a></td><td>{tools[k]["trial"]}</td><td>{tools[k]["price"]}<br><span class="small muted">{tools[k]["price_note"]}</span></td><td class="num"><b>{cat_score(cat, k)}</b>/100</td></tr>' for i, k in enumerate(free, 1))
        cards = "".join(f"""<article class="tool" id="{k}"><div class="tool-head"><span class="num">{i}</span><div><h3>{tools[k]['name']}</h3><div class="bestfor">{tools[k]['bf']}</div></div>
<a class="btn small" href="{tools[k]['url']}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div><div class="tool-body">
<p><b>Free plan:</b> {tools[k]['trial']}.</p><p><b>When you outgrow it:</b> paid plans start at {tools[k]['price'].replace('From ', '')} ({tools[k]['price_note']}).</p>
<p>{tools[k]['what']}</p><div class="pc"><div class="pros"><h4>Strengths</h4><ul>{''.join(f'<li>{x}</li>' for x in tools[k]['pros'])}</ul></div><div class="cons"><h4>Watch-outs</h4><ul>{''.join(f'<li>{x}</li>' for x in tools[k]['cons'])}</ul></div></div></div></article>""" for i, k in enumerate(free, 1))
        top = tools[free[0]]
        others = [tools[k]["name"] for k in free[1:4]]
        faqs = [(f"What is the best free {noun[:-1] if noun.endswith('s') and not noun.endswith('ss') else noun}?" if False else f"What are the best free {noun}?",
                 f"{top['name']} ({top['trial']}) ranks highest among the {noun} we rank that offer a free plan. {', '.join(others)} also have free plans."),
                (f"Is there a completely free option?", "Yes, each tool on this page lists a free plan on its pricing page. Free plans have limits, shown in the table above, and paid plans add more users, usage and features."),
                ("What do free plans usually leave out?", "Free plans typically cap users, records or monthly usage and leave out advanced automation, reporting and admin controls. Check each tool's limits against your team size before you commit."),
                ("When should I move to a paid plan?", f"When you hit a limit in the free plan or need a feature it leaves out. The table shows where each tool's paid plans start; our full {noun} ranking compares the paid tiers.")]
        body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(slug)} / <a href="/tools/{slug}/">{cat['crumb']}</a> / Free</nav>
<header class="article-head"><span class="eyebrow">Shortlist · Free plans</span><h1>{h1}</h1>{_byline(url, cat)}</header>
<div class="layout"><div class="main-col">
<section class="answer" id="answer" aria-label="Short answer"><h2>Short answer</h2><p><b>{top['name']}</b> has the highest-ranked free plan among the {noun} we rank ({cat_score(cat, free[0])}/100): {top['trial']}. {n} of the {len(cat['_ranked'])} tools in our {_cat_link(cat)} list a free plan.</p></section>
<section class="prose"><p>Every tool here comes from our main {_cat_link(cat)}, which scores {noun} on {len(cat['criteria'])} weighted criteria. This page keeps only the tools whose pricing page lists a free plan (not just a time-limited trial), in the same order, and shows what each free plan includes and where paid plans start.</p></section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<section id="compare"><h2>Free plans compared</h2><div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Free plan</th><th>Paid plans from</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">{cat['price_footnote']}</p></section>
<section id="reviews"><h2>The free plans</h2>{cards}</section>
<section id="faq"><h2>FAQ</h2><div>{_faq(faqs)}</div></section>
<section class="prose"><h2>Related</h2><ul><li><a href="/tools/{slug}/">Best {noun} (all plans)</a></li>{''.join(f'<li><a href="{h}">{x}</a></li>' for h, x in cat.get('related', []))}</ul></section>
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#answer">Short answer</a><a href="#shortlist">Shortlist</a><a href="#compare">Free plans compared</a><a href="#reviews">Details</a><a href="#faq">FAQ</a></nav></div></div>
{newsletter()}"""
        crumbs = [("/", "Home"), dept_crumb_ld(slug), (f"/tools/{slug}/", cat["crumb"]), (url, "Free")]
        page(url, f"{n} Best Free {cat['plural']} ({YEAR}) | Vettlo",
             f"The best free {noun}, from our ranked shortlist: what each free plan includes, its limits and where paid plans start. {top['name']} ranks first.",
             body, cur="/best-tools/", ptype="article", jsonld=_ld(h1, url, cat["date"], crumbs, [(k, tools[k]["name"]) for k in free], faqs))
        out.append((url, f"Best free {noun}"))
    # --- small business (skip CRM, which has its own hand-built page)
    if slug != "best-crm-software":
        ws = _smb_weights(cat)
        ranked = sorted([k for k in tools if _wscore(cat, k, ws) >= THRESHOLD], key=lambda k: (-_wscore(cat, k, ws), -float(tools[k]["g2"][0])))
        if len(ranked) >= 3:
            url = f"/tools/{slug.replace('-for-business', '')}-for-small-business/"
            n = len(ranked)
            plural_sb = cat["plural"].replace(" for Business", "")
            h1 = f"{n} Best {plural_sb} for Small Business in {YEAR}"
            short = "".join(f'<li><span class="rank">{i}</span><span><a class="nm" href="#{k}">{tools[k]["name"]}</a><br><span class="bf">{tools[k]["bf"]}</span></span><span class="sc">{_wscore(cat, k, ws)}<small>/100</small></span><a class="btn ghost small" href="#{k}">Details</a></li>' for i, k in enumerate(ranked, 1))
            rows = "".join(f'<tr><td class="num">{i}</td><td><a href="#{k}"><b>{tools[k]["name"]}</b></a></td><td>{tools[k]["trial_short"]}</td><td class="num">{tools[k]["price"]}</td><td class="num"><b>{_wscore(cat, k, ws)}</b>/100</td><td class="num">{cat_score(cat, k)}/100</td></tr>' for i, k in enumerate(ranked, 1))
            wrows = "".join(f'<tr><td>{nm}</td><td class="num">{w}%</td><td class="num">{sw}%</td></tr>' for (nm, w), sw in zip(cat["criteria"], ws))
            cards = "".join(f"""<article class="tool" id="{k}"><div class="tool-head"><span class="num">{i}</span><div><h3>{tools[k]['name']}</h3><div class="bestfor">{tools[k]['bf']}</div></div>
<a class="btn small" href="{tools[k]['url']}" target="_blank" rel="sponsored nofollow noopener">Visit website ↗</a></div>{_spec(cat, k, "Main score")}<div class="tool-body">
<p>{tools[k]['what']}</p><div><h4>Who it's best for</h4><p>{tools[k]['who']}</p></div>
<div class="pc"><div class="pros"><h4>Strengths</h4><ul>{''.join(f'<li>{x}</li>' for x in tools[k]['pros'])}</ul></div><div class="cons"><h4>Watch-outs</h4><ul>{''.join(f'<li>{x}</li>' for x in tools[k]['cons'])}</ul></div></div>
<p class="small muted"><b>Skip it if:</b> {tools[k]['skip']}</p></div></article>""" for i, k in enumerate(ranked, 1))
            top = tools[ranked[0]]
            moved = [tools[k]["name"] for k in ranked[:3] if k not in cat["_ranked"][:3]]
            faqs = [(f"What are the best {noun} for small businesses?", f"{top['name']} scores highest ({_wscore(cat, ranked[0], ws)}/100) once price and ease of use carry more weight, followed by {', '.join(tools[k]['name'] for k in ranked[1:3])}."),
                    ("How is this different from your main ranking?", f"Same tools and the same 0 to 5 ratings, but price and ease of use count for more, because small teams rarely have an admin or a big budget. The weights are in the table on this page." + (f" {', '.join(moved)} move into the top three as a result." if moved else "")),
                    (f"Which {noun} are cheapest for a small team?", "See the starting prices in the comparison table; free plans and trials are listed next to them. Price the plan that covers your team size, not only the entry plan."),
                    ("What should a small business look for?", "A free plan or low entry price, quick setup without an admin, and the two or three features you need on day one. Avoid paying for enterprise controls you won't use yet.")]
            body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {dept_crumb(slug)} / <a href="/tools/{slug}/">{cat['crumb']}</a> / Small business</nav>
<header class="article-head"><span class="eyebrow">Shortlist · Small business</span><h1>{h1}</h1>{_byline(url, cat)}</header>
<div class="layout"><div class="main-col">
<section class="answer" id="answer" aria-label="Short answer"><h2>Short answer</h2><p><b>{top['name']}</b> is our top pick for small businesses, scoring {_wscore(cat, ranked[0], ws)}/100 when price and ease of use carry more weight. {_price_sentence(top)}</p></section>
<section class="prose"><p>This list uses the same tools and ratings as our main {_cat_link(cat)}, reweighted for teams of roughly 1 to 50 people: price and ease of use count for more, and enterprise depth counts for less. Tools that score {THRESHOLD} or higher on the small-business weights are included.</p></section>
<section id="shortlist"><h2>The shortlist</h2><ol class="shortlist">{short}</ol></section>
<section id="compare"><h2>Compared for small teams</h2><div class="table-wrap"><table><thead><tr><th>#</th><th>Tool</th><th>Free plan / trial</th><th>Starting price</th><th>Small-business score</th><th>Main score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">{cat['price_footnote']}</p></section>
<section id="reviews"><h2>The reviews</h2>{cards}</section>
<section id="weights"><h2>How we weighted this list</h2><div class="table-wrap"><table><thead><tr><th>Criterion</th><th>Main ranking</th><th>Small business</th></tr></thead><tbody>{wrows}</tbody></table></div></section>
<section id="faq"><h2>FAQ</h2><div>{_faq(faqs)}</div></section>
<section class="prose"><h2>Related</h2><ul><li><a href="/tools/{slug}/">Best {noun} (main ranking)</a></li>{''.join(f'<li><a href="{h}">{x}</a></li>' for h, x in cat.get('related', []))}</ul></section>
{_author_box()}
</div><nav class="toc" aria-label="On this page"><span class="label">On this page</span><a href="#answer">Short answer</a><a href="#shortlist">Shortlist</a><a href="#compare">Comparison</a><a href="#reviews">Reviews</a><a href="#weights">Weights</a><a href="#faq">FAQ</a></nav></div></div>
{newsletter()}"""
            crumbs = [("/", "Home"), dept_crumb_ld(slug), (f"/tools/{slug}/", cat["crumb"]), (url, "Small business")]
            page(url, f"{n} Best {plural_sb} for Small Business ({YEAR}) | Vettlo",
                 f"The best {noun} for small businesses, reweighted for price and ease of use. {top['name']} ranks first; compare free plans, prices and scores.",
                 body, cur="/best-tools/", ptype="article", jsonld=_ld(h1, url, cat["date"], crumbs, [(k, tools[k]["name"]) for k in ranked], faqs))
            out.append((url, f"Best {noun.replace(' for business', '')} for small business"))
    for u, title in out:
        COMPARES.setdefault(slug, []).append((u, title))
        CLUSTER.setdefault(slug, []).append((u, title, "Shortlist"))
        CATEGORY_PAGES.append((u, title[:1].upper() + title[1:], f"{title[:1].upper() + title[1:]}, from our scored shortlist.", "Shortlist"))
