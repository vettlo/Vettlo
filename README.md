# Vettlo site source

Static site for vettlo.com, hosted on Cloudflare (Worker `vettlo-site`).

## How it's built
- `build.py` holds every page's content and the shared header/footer. Edit content there.
- `src/site.css` is the shared stylesheet.
- Run `python3 build.py` to generate:
  - `dist/site/` — deploy this folder (zip it and upload as a new Production deployment in Cloudflare Pages).
  - `dist/preview/` — version used for the Claude artifact preview.

## Current state (Oct 2, 2026)
- Niche: software reviews for sales & RevOps leaders. First live review: `/tools/best-crm-software/` (8 CRMs).
- Pricing and G2 ratings on the CRM page were verified on Oct 2, 2026.
- `PRELAUNCH_NOINDEX = True` in build.py keeps the whole site out of search engines. Set to False when placeholders are filled, rebuild, redeploy, then submit sitemap.xml in Google Search Console.
- Yellow highlighted fields (`class="fill"`) still need real input: Vettlo scores, hands-on test notes, screenshots, editor name/bio, reviewer names.
- Domains: vettlo.com and www.vettlo.com point to vettlo.pages.dev (CNAME, proxied).

## Deploy
The site runs as the Cloudflare Worker `vettlo-site` (static assets from `public/`, see `wrangler.jsonc`), connected to this repo.
vettlo.com and www.vettlo.com are attached to that Worker as custom domains.
After editing `build.py` or `src/site.css`, run `python3 build.py` and commit both the source and `public/`. Pushing to `main` deploys the site automatically.
The old Pages project `vettlo` is no longer used.

## Search engines
- Google Search Console: domain property `sc-domain:vettlo.com`, sitemap submitted Oct 14, 2026.
- Bing / IndexNow: key file `public/<INDEXNOW_KEY>.txt` (key in build.py). After publishing new or changed pages, POST the URLs to https://www.bing.com/indexnow with host, key and keyLocation.
- Cloudflare AI Crawl Control: no AI crawlers blocked (checked Oct 14, 2026).
