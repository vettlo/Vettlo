#!/usr/bin/env python3
"""Keyword cannibalization check: one search keyword belongs to one URL.

Builds a keyword -> URL map from every indexable page (public/sitemap.xml) and every planned article in
data/clusters.json, then fails if two pages target the same keyword or near-identical keywords.

  python3 scripts/keyword_check.py                    # check the whole site + plan (exit 1 on conflicts)
  python3 scripts/keyword_check.py "zendesk pricing"  # who owns this keyword? (exit 1 if taken)
  python3 scripts/keyword_check.py --map              # print the full keyword map

Ownership rules (who a keyword belongs to):
- /tools/best-<x>/ shortlist (pillar): its head term ("<x>", "best <x>") and the pillar's extra heads below.
- /tools/best-<tool>-alternatives/: "<tool> alternatives".
- /compare/<a>-vs-<b>/: "<a> vs <b>" (either order).
- /tools/<tool>-review/: "<tool> review" and "<tool> pricing" — a tool's own pricing intent belongs to its review page.
- /guides/<slug>/: its target_keyword in data/clusters.json (or the slug as a phrase).
Planned (todo) articles count too, so two planned articles can't share a keyword either.
"""
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Extra head terms a pillar owns (beyond what its slug gives).
PILLAR_HEADS = {
    "/tools/best-crm-software/": ["crm", "crm software", "best crm", "crm system"],
    "/tools/best-password-managers-for-business/": ["password manager", "business password manager", "password manager for business", "best password manager for business"],
    "/tools/best-b2b-data-providers/": ["b2b data providers", "b2b data", "b2b contact data"],
    "/tools/best-sales-engagement-software/": ["sales engagement platform", "sales engagement software"],
    "/tools/best-hris-software/": ["hris", "hris software", "hr software"],
    "/tools/best-e-signature-software/": ["e signature software", "electronic signature software", "e signature"],
    "/tools/best-project-management-software/": ["project management software", "project management tools"],
    "/tools/best-accounting-software/": ["accounting software", "small business accounting software"],
    "/tools/best-help-desk-software/": ["help desk software", "ticketing system"],
    "/tools/best-email-marketing-software/": ["email marketing software", "email marketing", "newsletter software"],
    "/tools/best-time-tracking-software/": ["time tracking software", "time tracking app"],
    "/tools/best-expense-management-software/": ["expense management software"],
    "/tools/best-payroll-software/": ["payroll software", "payroll services", "full service payroll"],
}
STOP = {"the", "a", "an", "for", "of", "to", "and", "is", "are", "do", "does", "your", "in", "on", "with", "2026", "best", "software", "tool", "tools", "app"}


def norm(k):
    k = k.lower().replace("-", " ").replace(".", " ").replace("’", "'")
    k = re.sub(r"[^a-z0-9' ]", " ", k)
    k = re.sub(r"\s+", " ", k).strip()
    return " ".join(w[:-1] if w.endswith("s") and len(w) > 4 and not w.endswith("ss") else w for w in k.split())


def core(k):
    return frozenset(w for w in norm(k).split() if w not in STOP)


def build_map():
    owners = {}  # norm keyword -> set(urls)

    def own(k, url):
        owners.setdefault(norm(k), set()).add(url)

    sm = open(os.path.join(ROOT, "public", "sitemap.xml")).read()
    urls = re.findall(r"<loc>https://vettlo\.com(/[^<]*)</loc>", sm)
    for u in urls:
        m = re.fullmatch(r"/tools/best-(.+)-alternatives/", u)
        if m:
            own(f"{m.group(1)} alternatives", u); continue
        m = re.fullmatch(r"/tools/best-(.+)/", u)
        if m:
            x = m.group(1).replace("-", " ")
            own(x, u); own("best " + x, u)
            for h in PILLAR_HEADS.get(u, []):
                own(h, u)
            continue
        m = re.fullmatch(r"/compare/(.+)-vs-(.+)/", u)
        if m:
            a, b = m.group(1).replace("-", " "), m.group(2).replace("-", " ")
            own(f"{a} vs {b}", u); own(f"{b} vs {a}", u); continue
        m = re.fullmatch(r"/tools/(.+)-review/", u)
        if m:
            t = m.group(1).replace("-", " ")
            own(f"{t} review", u); own(f"{t} pricing", u)
            first = t.split()[0]  # "hubspot sales hub" also owns "hubspot sales hub pricing"; brand-only pricing too
            if first != t:
                own(f"{first} pricing", u)
            continue
    plan = json.load(open(os.path.join(ROOT, "data", "clusters.json")))
    for p in plan["pillars"]:
        for a in p["articles"]:
            u = a.get("url") or f"/guides/{a['slug']}/"
            if a.get("target_keyword"):
                own(a["target_keyword"], u)
    for u in urls:  # guides not in the plan: slug as phrase
        m = re.fullmatch(r"/guides/(.+)/", u)
        if m and not any(u in s for s in owners.values()):
            own(m.group(1).replace("-", " "), u)
    return owners


def main():
    args = sys.argv[1:]
    owners = build_map()
    if args and args[0] == "--map":
        for k, us in sorted(owners.items()):
            print(f"{k:45} {', '.join(sorted(us))}")
        return
    if args:
        q = norm(" ".join(args))
        hits = sorted(owners.get(q, set()))
        near = sorted({(k, u) for k, us in owners.items() for u in us if k != q and core(k) and core(k) == core(q)})
        print(f"'{q}': " + (", ".join(hits) if hits else "free"))
        for k, u in near:
            print(f"  near-identical: '{k}' -> {u}")
        sys.exit(1 if hits or near else 0)
    problems = []
    for k, us in owners.items():
        if len(us) > 1:
            problems.append(f"same keyword '{k}': {', '.join(sorted(us))}")
    seen = {}
    for k, us in owners.items():
        c = core(k)
        if not c:
            continue
        for u in us:
            for u2, k2 in seen.get(c, []):
                if u2 != u:
                    problems.append(f"near-identical '{k}' ({u}) ~ '{k2}' ({u2})")
            seen.setdefault(c, []).append((u, k))
    for p in sorted(set(problems)):
        print(p)
    print(("OK: " if not problems else f"{len(set(problems))} conflicts. ") + f"{len(owners)} keywords mapped")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
