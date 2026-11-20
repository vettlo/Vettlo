# Vendor portal end-to-end test

Runs the whole vendor flow against a local Worker and a mock iyzico (no real payments):
pages and prices, product submission, reservation, card payment, editorial hold and approval,
monthly subscription, renewal webhook (incl. duplicate and forged), stopping renewal, waitlist,
access control and /go/ links.

1. `node scripts/portal-test/mock-iyzico.js &`
2. `.dev.vars` (never commit): `ADMIN_EMAILS=admin@ex.com`, `IYZICO_API_KEY=test-api`, `IYZICO_SECRET_KEY=test-secret`,
   `IYZICO_BASE_URL=http://localhost:9999`, `IYZICO_SUBSCRIPTIONS=1`
3. `npx wrangler dev --local --port 8787 --persist-to /tmp/vettlo-test` and open `/api/categories` once (creates tables)
4. Seed vendors 1–4 (admin@ex.com, c@, d@, e@) and sessions whose tokens are `adm`, `vc`, `vd`, `ve` (sha256 of the token in `sessions.hash`)
5. `node scripts/portal-test/e2e.js` → expect "0 failed"

## Paddle (current payment provider)

`e2e-paddle.js` runs the Paddle subscription flow against `mock-paddle.js` (port 9997): catalog sync, checkout page,
signed webhooks (duplicate, forged, stale), editorial hold + billing-date shift, renewal, failed renewal, cancellation,
refund and admin End.

1. `node scripts/portal-test/mock-paddle.js &`
2. `.dev.vars` (never commit): `ADMIN_EMAILS=admin@ex.com`, `PADDLE_API_KEY=test-api-key`, `PADDLE_CLIENT_TOKEN=test_client_token`,
   `PADDLE_WEBHOOK_SECRET=test-webhook-secret`, `PADDLE_BASE_URL=http://localhost:9997`
3. Start wrangler as above with `--persist-to <dir>`, open `/api/categories` once, seed vendors 1–3 and sessions `adm`, `vc`, `vd`
4. `WRANGLER=<path to wrangler> STATE=<dir> node scripts/portal-test/e2e-paddle.js` → expect "0 failed"
