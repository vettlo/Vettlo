#!/usr/bin/env python3
"""Near-duplicate check for vettlo.com's built pages.

Compares the main content of indexable pages (no noindex, in the sitemap) using 8-word shingles.
overlap(A, B) = share of A's shingles that also appear in B.

  python3 scripts/similarity.py                 # site report: pairs above the threshold
  python3 scripts/similarity.py /guides/x/      # check one page against every other page (exit 1 if too similar)
  python3 scripts/similarity.py --max 0.25 /guides/x/

Single-page checks default to a 30% limit (site report: 40%). Every new article must pass before it's published.
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
K = 8


def url_of(path):
    rel = os.path.relpath(os.path.dirname(path), ROOT)
    return "/" if rel == "." else f"/{rel}/"


def words(doc):
    m = re.search(r"<main.*?</main>", doc, re.S)
    doc = m.group(0) if m else doc
    # drop parts that repeat on purpose: scripts, styles, nav, disclosure, newsletter box, related-link lists
    doc = re.sub(r"<(script|style|nav)\b.*?</\1>", " ", doc, flags=re.S)
    doc = doc.split('class="newsletter"')[0]  # the newsletter box closes every page
    doc = re.sub(r'<section class="author-box".*?</section>', " ", doc, flags=re.S)
    doc = re.sub(r"<p class=\"disclose.*?</p>", " ", doc, flags=re.S)
    doc = re.sub(r"<h2>(?:Related|More on this topic|Guides|More [^<]*)</h2>\s*<ul>.*?</ul>", " ", doc, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", doc)).lower().split()


def shingles(w):
    return {" ".join(w[i:i + K]) for i in range(max(0, len(w) - K + 1))}


def load():
    pages = {}
    sitemap = open(os.path.join(ROOT, "sitemap.xml")).read()
    for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
        doc = open(f).read()
        u = url_of(f)
        if "noindex" in doc[:4000] or f"vettlo.com{u}<" not in sitemap:
            continue
        s = shingles(words(doc))
        if len(s) > 50:
            pages[u] = s
    return pages


def main():
    args = sys.argv[1:]
    limit = 0.30 if any(not a.startswith("--") and a.startswith("/") for a in args) else 0.40  # new pages: 30%; site report: 40%
    if "--max" in args:
        i = args.index("--max")
        limit = float(args[i + 1])
        del args[i:i + 2]
    pages = load()
    if args:
        target = args[0] if args[0].endswith("/") else args[0] + "/"
        if target not in pages:
            sys.exit(f"{target} isn't an indexable built page (run build.py first; is it noindex or missing from the sitemap?)")
        a = pages[target]
        rows = sorted(((len(a & b) / len(a), u) for u, b in pages.items() if u != target), reverse=True)[:5]
        for r, u in rows:
            print(f"{r:6.1%}  {u}")
        worst = rows[0][0] if rows else 0
        print(("OK" if worst <= limit else "TOO SIMILAR") + f": highest overlap {worst:.1%} (limit {limit:.0%})")
        sys.exit(0 if worst <= limit else 1)
    hits = []
    urls = list(pages)
    for i, u in enumerate(urls):
        for v in urls[i + 1:]:
            inter = len(pages[u] & pages[v])
            r = max(inter / len(pages[u]), inter / len(pages[v]))
            if r > limit:
                hits.append((r, u, v))
    for r, u, v in sorted(hits, reverse=True):
        print(f"{r:6.1%}  {u}  <->  {v}")
    print(f"{len(hits)} pairs above {limit:.0%} among {len(pages)} indexable pages")


if __name__ == "__main__":
    main()
