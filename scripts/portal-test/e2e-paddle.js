// Paddle flow end to end against a local Worker and mock-paddle.js (see README.md): catalog sync, checkout page,
// webhooks (signed, duplicate, forged), editorial hold and billing-date shift, renewal, cancellation, refund.
const { execSync } = require('child_process');
const B = 'http://localhost:8787', M = 'http://localhost:9997';
const WR = process.env.WRANGLER || 'npx wrangler', STATE = process.env.STATE || '/tmp/vettlo-paddle';
let pass = 0, fail = 0;
const ok = (c, msg, extra) => { if (c) { pass++; console.log('  ✓ ' + msg); } else { fail++; console.log('  ✗ ' + msg, extra !== undefined ? JSON.stringify(extra).slice(0, 400) : ''); } };
const call = async (who, path, body, method) => { const r = await fetch(B + path, { method: method || (body ? 'POST' : 'GET'), redirect: 'manual',
  headers: { cookie: 'vs=' + who, 'content-type': 'application/json', 'x-requested-with': 'vettlo' }, body: body ? JSON.stringify(body) : undefined });
  const t = await r.text(); try { return { status: r.status, ...JSON.parse(t) }; } catch { return { status: r.status, text: t, location: r.headers.get('location') }; } };
const sql = (q) => JSON.parse(execSync(`${WR} d1 execute vettlo --local --persist-to ${STATE} --json --command "${q.replace(/"/g, '\\"')}"`, { cwd: __dirname + '/../..', stdio: ['ignore', 'pipe', 'ignore'] }).toString())[0].results;
const mk = (path, body) => fetch(M + path, { method: 'POST', body: JSON.stringify(body || {}) }).then((r) => r.json());
const mock = () => fetch(M + '/__state').then((r) => r.json());
const sub = (id) => sql(`SELECT * FROM subs WHERE id = ${Number(id)}`)[0];
const CRM = '/tools/best-crm-software/', HALT = '/tools/best-hubspot-alternatives/';

(async () => {
  console.log('1) Settings and catalog');
  let r = await call('vc', '/api/me');
  ok(r.payments === 'paddle' && r.subscriptions === true, 'portal reports Paddle subscriptions', r);
  ok((await call('vc', '/api/admin/paddle/sync', {})).status === 403, 'vendors cannot sync the catalog');
  r = await call('adm', '/api/admin/paddle/sync', {});
  ok(r.ok && r.count === 21 && r.sandbox === true, '21 prices created (10 positions × 2 periods + Basic yearly), sandbox', r);
  let m = await mock();
  const pr = Object.values(m.prices);
  ok(Object.keys(m.products).length === 11 && pr.length === 21, '11 products, 21 prices in Paddle');
  const p1m = pr.find((p) => p.unit_price.amount === '15000' && p.billing_cycle.interval === 'month');
  const p4y = pr.find((p) => p.unit_price.amount === '63720' && p.billing_cycle.interval === 'year');
  const bas = pr.find((p) => p.unit_price.amount === '5000' && p.billing_cycle.interval === 'year');
  ok(p1m && p4y && bas && pr.every((p) => p.tax_mode === 'external' && p.unit_price.currency_code === 'USD'), 'prices match the pricing page ($150/mo, $637.20/yr, Basic $50/yr), tax added on top');
  r = await call('adm', '/api/admin/paddle/sync', {});
  ok(r.ok && Object.keys((await mock()).prices).length === 21, 'running sync again creates nothing new');

  console.log('2) Vendor orders and opens checkout');
  r = await call('vc', '/api/listings', { product_name: 'Folk', category: 'best-crm-software', website: 'folk.app' });
  const folk = r.id;
  r = await call('vc', '/api/subscribe', { listing_id: folk, page: CRM, plan: 'p2', period: 'month', accept_terms: true });
  ok(r.ok && r.method === 'paddle', 'reserved #2 monthly', r);
  const s1 = r.sub_id;
  const inv = (await call('vc', '/api/invoices')).rows.find((x) => x.status === 'requested');
  r = await call('vc', '/api/pay', { invoice_id: inv.id });
  ok(r.ok && /\/vendors\/checkout\/\?_ptxn=txn_\d+$/.test(r.url), 'checkout link created without asking for billing details', r);
  const txn = r.url.split('_ptxn=')[1];
  m = await mock();
  ok(m.txns[txn].custom_data.sub_id === String(s1) && m.txns[txn].items[0].price_id === pr.find((p) => p.unit_price.amount === '9900' && p.billing_cycle.interval === 'month').id, 'transaction carries our plan id and the $99 monthly price');
  let page = await fetch(B + '/vendors/checkout/?_ptxn=' + txn, { headers: { cookie: 'vs=vc' }, redirect: 'manual' });
  const html = await page.text(), csp = page.headers.get('content-security-policy') || '';
  ok(page.status === 200 && html.includes('cdn.paddle.com/paddle/v2/paddle.js') && html.includes(txn) && html.includes('test_client') && html.includes('Merchant of Record'), 'checkout page loads Paddle.js for this transaction');
  ok(/script-src 'self' https:\/\/cdn\.paddle\.com 'nonce-[0-9a-f]+'/.test(csp) && csp.includes('frame-src https://*.paddle.com') && !csp.includes("'unsafe-eval'"), 'page CSP allows only Paddle and its own nonce script', csp);
  ok((await fetch(B + '/vendors/checkout/?_ptxn=' + txn, { headers: { cookie: 'vs=vd' }, redirect: 'manual' })).status === 302, "another vendor can't open this checkout");
  ok((await fetch(B + '/vendors/checkout/?_ptxn=txn_999', { headers: { cookie: 'vs=vc' }, redirect: 'manual' })).status === 302, 'unknown transaction redirects back');

  console.log('3) Payment completes (webhooks)');
  r = await mk('/__complete', { txn, again: true });
  ok(r.hooks.every((h) => h.status === 200), 'subscription.created and transaction.completed accepted', r);
  let s = sub(s1);
  ok(s.status === 'active' && s.auto_renew === 1 && s.provider_sub === 'paddle:' + r.sub && s.held_since, 'plan active, linked to the Paddle subscription, held for review', s);
  ok(sql(`SELECT COUNT(*) AS n FROM invoices WHERE slot_id = ${s1} AND status = 'paid' AND provider_ref = 'paddle:${txn}'`)[0].n === 1, 'invoice paid once even though the webhook came twice');
  const psub = r.sub;
  const pt0 = s.paid_through;
  const bad = await fetch(B + '/api/paddle/webhook', { method: 'POST', headers: { 'content-type': 'application/json', 'paddle-signature': 'ts=' + Math.floor(Date.now() / 1000) + ';h1=00' }, body: '{"event_type":"transaction.completed","data":{"id":"txn_x","custom_data":{"sub_id":"' + s1 + '"}}}' });
  ok(bad.status === 401 && sub(s1).paid_through === pt0, 'forged webhook refused');
  r = await mk('/__renew', { sub: psub, ts: Math.floor(Date.now() / 1000) - 3600 });
  ok(r.status === 401 && sub(s1).paid_through === pt0, 'stale (replayed) webhook refused');

  console.log('4) Approval moves the Paddle billing date');
  await call('adm', '/api/admin/listings/' + folk, { status: 'approved', tool_id: 'folk' });
  s = sub(s1); m = await mock();
  ok(!s.held_since && Date.parse(s.paid_through) > Date.now() + 27 * 864e5, 'live, paid a month from approval');
  ok(m.subs[psub].next_billed_at === s.paid_through && m.subs[psub].proration_billing_mode === 'do_not_bill', "Paddle's next billing date moved to match, without an extra charge", m.subs[psub]);

  console.log('5) Renewal');
  r = await mk('/__renew', { sub: psub });
  const s2 = sub(s1);
  ok(r.status === 200 && Date.parse(s2.paid_through) - Date.parse(s.paid_through) > 27 * 864e5, 'renewal extends by a month', [s.paid_through, s2.paid_through]);
  ok(sql(`SELECT COUNT(*) AS n FROM invoices WHERE slot_id = ${s1} AND status = 'paid'`)[0].n === 2, 'renewal invoice recorded');
  ok((await mk('/__past_due', { sub: psub })).status === 200 && sub(s1).paid_through === s2.paid_through, 'failed renewal noted, position unchanged');

  console.log('6) Vendor stops renewal');
  r = await call('vc', `/api/subs/${s1}/stop`, {});
  m = await mock();
  ok(r.ok && m.subs[psub].cancel_mode === 'next_billing_period' && sub(s1).auto_renew === 0 && sub(s1).status === 'active', 'cancelled at period end in Paddle; stays live until then', r);

  console.log('7) Yearly plan, cancelled from Paddle, then refunded and ended by admin');
  r = await call('vc', '/api/subscribe', { listing_id: folk, page: HALT, plan: 'p4', period: 'year', accept_terms: true });
  const s3 = r.sub_id;
  const inv3 = (await call('vc', '/api/invoices')).rows.find((x) => x.status === 'requested');
  ok(inv3.amount_cents === 63720, 'yearly #4 invoice $637.20');
  r = await call('vc', '/api/pay', { invoice_id: inv3.id });
  const txn3 = r.url.split('_ptxn=')[1];
  r = await mk('/__complete', { txn: txn3 });
  const psub3 = r.sub;
  ok(sub(s3).status === 'active' && sub(s3).auto_renew === 1 && !sub(s3).held_since, 'approved product goes live at once');
  await mk('/__schedule_cancel', { sub: psub3 });
  ok(sub(s3).auto_renew === 0 && sub(s3).status === 'active', 'cancellation scheduled in Paddle turns renewal off here');
  await mk('/__refund', { txn: txn3 });
  ok(sql(`SELECT status FROM invoices WHERE provider_ref = 'paddle:${txn3}'`)[0].status === 'refunded', 'refund marks the invoice refunded');
  r = await call('adm', `/api/admin/subs/${s3}/end`, {});
  m = await mock();
  ok(r.ok && sub(s3).status === 'cancelled' && m.subs[psub3].cancel_mode === 'immediately', 'admin End cancels the Paddle subscription immediately');

  console.log('8) Guards');
  r = await call('vd', '/api/listings', { product_name: 'Nimble', category: 'best-crm-software', website: 'nimble.com' });
  r = await call('vd', '/api/subscribe', { listing_id: r.id, page: CRM, plan: 'basic', period: 'year', accept_terms: true });
  const inv4 = (await call('vd', '/api/invoices')).rows.find((x) => x.status === 'requested');
  ok((await call('vc', '/api/pay', { invoice_id: inv4.id })).status === 400, "can't open checkout for another vendor's invoice");
  r = await call('vd', '/api/pay', { invoice_id: inv4.id });
  ok(r.ok, 'Basic yearly checkout opens', r);
  m = await mock();
  ok(m.badAuth === 0 && m.hooks.filter((h) => h.status !== 200).length === 1, 'every API call authenticated; only the stale webhook was refused', m.hooks);
  console.log(`\n${pass} passed, ${fail} failed`);
})().catch((e) => console.log('CRASH', e));
