# Tool review pages and category variants (free plans, small business), generated from the verified
# category data. Runs last so every category, comparison and alternatives page is registered.

CRM_FULL = {"slug": "best-crm-software", "crumb": "CRM Software", "plural": "CRM Software", "plural_lc": "CRM software",
            "date": UPDATED, "criteria": CRITERIA, "_score": score, "related": [("/sales-software/", "All sales software")],
            "price_footnote": f"Starting prices from each vendor's pricing page, checked {PRICES_CHECKED}.",
            "tools": {t["id"]: {"name": t["name"], "short": SHORT[t["id"]], "url": URLS[t["id"]], "bf": t["bf"],
                                "price": PRICING[t["id"]]["price"], "price_note": PRICING[t["id"]]["note"],
                                "trial": PRICING[t["id"]]["trial"], "trial_short": PRICING[t["id"]]["short"],
                                "g2": G2[t["id"]], "scores": SCORES[t["id"]], "what": t["what"], "who": t["who"], "why": t["why"],
                                "pros": t["pros"], "cons": t["cons"], "skip": t["notavoid"],
                                "links": CRM_CARD_LINKS.get(t["id"], [])} for t in CONSIDERED}}
CRM_FULL["_ranked"] = [t["id"] for t in TOOLS]

for _c in [CRM_FULL] + ALLCATS:
    variant_pages(_c)
review_pages([CRM_FULL] + ALLCATS)
