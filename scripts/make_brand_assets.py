#!/usr/bin/env python3
"""Render the brand images from the current brand colour: favicon.ico, icon-192.png, apple-touch-icon.png and og.png (src/).
Run after changing --brand in src/site.css:  python3 scripts/make_brand_assets.py && python3 build.py"""
import os, re, subprocess, tempfile, json
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
css = open(os.path.join(ROOT, "src", "site.css")).read()
var = lambda n: re.search(r"--%s:\s*(#[0-9a-fA-F]{6})" % n, css).group(1)
BRAND, BRAND2, TINT, INK, BG, DARK = var("brand"), var("brand-2"), var("brand-tint"), var("ink"), var("bg"), var("dark")
MARK = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="{s}" height="{s}"><rect width="32" height="32" rx="8" fill="%s"/>'
        '<path d="M8.5 10.5l6.2 12.2c.5 1 1.9 1 2.4 0L24.5 8" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>') % BRAND
bars = [("Fit for the job", 92), ("Features on the plan you'd buy", 84), ("Ease of use", 78), ("Price and value", 70)]
OG = f"""<html><head><style>body{{margin:0;width:1200px;height:630px;background:{BG};font-family:Geist,Inter,'Segoe UI',Arial,sans-serif;color:{INK};display:flex;align-items:center;}}
.l{{padding-left:80px;width:560px}} .brand{{display:flex;align-items:center;gap:16px;font-size:38px;font-weight:700;letter-spacing:-1px;margin-bottom:46px}}
h1{{font-size:84px;line-height:1.02;letter-spacing:-3px;margin:0 0 34px}} p{{font-size:26px;color:#43534f;margin:0}}
.card{{margin-left:auto;margin-right:80px;width:440px;background:#fff;border:1px solid #dde6e5;border-radius:28px;padding:34px;box-shadow:0 30px 70px rgba(12,26,26,.10)}}
.k{{font-size:17px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:{BRAND}}} .t{{display:flex;justify-content:space-between;align-items:baseline;margin:14px 0 22px}}
.t b{{font-size:26px}} .t span{{font-size:58px;font-weight:700;color:{BRAND};letter-spacing:-2px}} .t small{{font-size:20px;color:#6a7977}}
.r{{margin-top:16px;font-size:18px;color:#43534f}} .bar{{height:10px;border-radius:9px;background:{TINT};margin-top:8px}} .bar i{{display:block;height:10px;border-radius:9px;background:{BRAND}}}</style></head>
<body><div class="l"><div class="brand">{MARK.format(s=64)}vettlo</div><h1>Business software, scored in the open.</h1><p>Independent reviews for every team · vettlo.com</p></div>
<div class="card"><div class="k">How a score is built</div><div class="t"><b>Example tool</b><span>88<small>/100</small></span></div>
{''.join(f'<div class="r">{n}<div class="bar"><i style="width:{w}%"></i></div></div>' for n, w in bars)}</div></body></html>"""

js = """const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [mark, og, out] = process.argv.slice(2); const b = await chromium.launch();
  for (const s of [16, 32, 48, 180, 192]) { const p = await b.newPage({ viewport: { width: s, height: s } });
    await p.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(mark, 'utf8').replace(/\\{s\\}/g, s)}</body></html>`);
    await p.screenshot({ path: `${out}/mark-${s}.png`, omitBackground: true }); await p.close(); }
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } }); await p.setContent(fs.readFileSync(og, 'utf8')); await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}/og.png` }); await b.close(); })();"""
with tempfile.TemporaryDirectory() as t:
    open(f"{t}/mark.svg", "w").write(MARK); open(f"{t}/og.html", "w").write(OG); open(f"{t}/r.js", "w").write(js)
    subprocess.run(["node", f"{t}/r.js", f"{t}/mark.svg", f"{t}/og.html", t], check=True)
    src = os.path.join(ROOT, "src")
    Image.open(f"{t}/mark-192.png").save(f"{src}/icon-192.png")
    # apple touch icon: opaque background
    a = Image.new("RGBA", (180, 180), BRAND); a.alpha_composite(Image.open(f"{t}/mark-180.png").convert("RGBA")); a.convert("RGB").save(f"{src}/apple-touch-icon.png")
    Image.open(f"{t}/mark-48.png").save(f"{src}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    Image.open(f"{t}/og.png").convert("RGB").save(f"{src}/og.png", optimize=True)
print("brand assets written with", BRAND)
