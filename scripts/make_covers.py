#!/usr/bin/env python3
"""Render each guide's SVG cover (public/assets/covers/<slug>.svg, written by build.py) to a 1200x630 PNG in
src/covers/<slug>.png, used for og:image and the Article schema image. Only renders covers that are new or changed.

  python3 build.py && python3 scripts/make_covers.py && python3 build.py   # second build picks up the new PNGs
"""
import hashlib, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SVG_DIR = os.path.join(ROOT, "public", "assets", "covers")
OUT = os.path.join(ROOT, "src", "covers")
MAN = os.path.join(OUT, "manifest.json")
os.makedirs(OUT, exist_ok=True)
man = json.load(open(MAN)) if os.path.exists(MAN) else {}
todo = []
for f in sorted(os.listdir(SVG_DIR)):
    if not f.endswith(".svg"):
        continue
    slug = f[:-4]
    svg = open(os.path.join(SVG_DIR, f)).read()
    h = hashlib.md5(svg.encode()).hexdigest()
    if man.get(slug) != h or not os.path.exists(os.path.join(OUT, slug + ".png")):
        todo.append((slug, svg, h))
if todo:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for slug, svg, h in todo:
            pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
            path = os.path.join(OUT, slug + ".png")
            pg.screenshot(path=path, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
            from PIL import Image  # flat colors: a 128-color palette keeps covers sharp at a fraction of the size
            Image.open(path).convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
            man[slug] = h
        b.close()
json.dump(man, open(MAN, "w"), indent=1, sort_keys=True)
print(f"{len(todo)} cover(s) rendered, {len(man)} total")
