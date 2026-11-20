// PayTR flow end to end against a local Worker and mock-paytr.js (see README.md): card form, notification,
// stored card, editorial hold, automatic renewal by cron, declined renewal, stopping renewal.
const { execSync } = require('child_process');
const B = 'http://localhost:8787', M = 'http://localhost:9998';
const WR = process.env.WRANGLER || 'npx wrangler', STATE = process.env.STATE || '/tmp/vettlo-paytr';
let pass = 0, fail = 0;
const ok = (c, msg, extra) => { if (c) { pass++; console.log('  ✓ ' + msg); } else { fail++; console.log('  ✗ ' + msg, extra !== undefined ? JSON.stringify(extra).slice(0, 300) : ''); } };
const call = async (who, path, body, method) => { const r = await fetch(B + path, { method: method || (body ? 'POST' : 'GET'), redirect: 'manual',
  headers: { cookie: 'vs=' + who, 'content-type': 'application/json', 'x-requested-with': 'vettlo' }, body: body ? JSON.stringify(body) : undefined });
  const t = await r.text(); try { return { status: r.status, ...JSON.parse(t) }; } catch { return { status: r.status, text: t, location: r.headers.get('location') }; } };
const sql = (q) => JSON.parse(execSync(`${WR} d1 execute vettlo --local --persist-to ${STATE} --json --command "${q.replace(/"/g, '\\"')}"`, { cwd: __dirname + '/../..', stdio: ['ignore', 'pipe', 'ignore'] }).toString())[0].results;
const cron = async () => { for (const u of ['/cdn-cgi/handler/scheduled?cron=17+6+*+*+*', '/__scheduled?cron=17+6+*+*+*']) { const r = await fetch(B + u); if (r.ok) return; } };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const mock = async () => (await fetch(M + '/__state')).json();
const sub = (id) => sql(`SELECT * FROM subs WHERE id = ${Number(id)}`)[0];
const CRM = '/tools/best-crm-software/';

(async () => {
  console.log('1) Reserve and open the card form');
  let r = await call('vc', '/api/me');
  ok(r.vendor && r.payments === 'paytr' && r.subscriptions === true, 'portal reports PayTR with automatic renewals', r);
  r = await call('vc', '/api/listings', { product_name: 'Folk', category: 'best-crm-software', website: 'folk.app' });
  const folk = r.id;
  r = await call('vc', '/api/subscribe', { listing_id: folk, page: CRM, plan: 'p2', period: 'month', accept_terms: true });
  ok(r.ok && r.method === 'paytr', 'reserved #2 monthly', r);
  const subId = r.sub_id;
  const inv = (await call('vc', '/api/invoices')).rows.find((x) => x.status === 'requested');
  ok(inv && inv.amount_cents === 9900, 'invoice $99', inv);
  await call('vc', '/api/billing', { name: 'Cem', surname: 'Test', phone: '+905550000000', tax_id: '', address: 'Test cad. 1', city: 'Istanbul', country: 'Turkey', zip: '34000' }, 'PUT');
  r = await call('vc', '/api/pay', { invoice_id: inv.id });
  ok(r.ok && /\/api\/pay\/paytr\/V\d+R[0-9a-f]{16}$/.test(r.url), 'card form link created (no tax id needed)', r);
  const formUrl = r.url.replace(/^https?:\/\/[^/]+/, B);
  const page = await fetch(formUrl, { headers: { cookie: 'vs=vc', 'cf-connecting-ip': '85.1.2.3' } });
  const html = await page.text();
  const csp = page.headers.get('content-security-policy') || '';
  ok(page.status === 200 && csp.includes('form-action http://localhost:9998') && csp.includes("script-src 'none'"), 'form served; it can only post to PayTR and runs no scripts', csp);
  ok(html.includes(`action="${M}/odeme"`) && html.includes('name="paytr_token"') && html.includes('name="store_card"') && html.includes('Test mode'), 'form posts to PayTR, signed, with the save-card option');
  ok((await fetch(formUrl, { headers: { cookie: 'vs=vd' }, redirect: 'manual' })).status === 302, "another vendor can't open this form");

  console.log('2) Buyer pays on PayTR');
  const fields = Object.fromEntries([...html.matchAll(/<input type="hidden" name="([^"]+)" value="([^"]*)">/g)].map((m) => [m[1], m[2].replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>')]));
  const pay = await fetch(M + '/odeme', { method: 'POST', redirect: 'manual', body: new URLSearchParams({ ...fields, cc_owner: 'Cem Test', card_number: '4355084355084358', expiry_month: '12', expiry_year: '30', cvv: '000', store_card: '1' }) });
  let m = await mock();
  ok(m.notices.length === 1 && m.notices[0].reply === 'OK', 'PayTR notification accepted with plain OK', m.notices);
  const back = await fetch(pay.headers.get('location').replace('https://vettlo.com', B), { redirect: 'manual' });
  ok(/pay=ok/.test(back.headers.get('location') || ''), 'buyer returns to the portal with "paid"', back.headers.get('location'));
  let s = sub(subId);
  ok(s.status === 'active' && s.auto_renew === 1 && /^paytr:u\d+$/.test(s.provider_sub) && s.held_since, 'plan active, card stored for renewal, held for review', s);
  ok(sql(`SELECT COUNT(*) AS n FROM invoices WHERE id = ${inv.id} AND status = 'paid' AND provider_ref LIKE 'paytr:%'`)[0].n === 1, 'invoice paid with the PayTR order reference');
  ok(!JSON.stringify(sql('SELECT * FROM paytr_orders')).includes('4355'), 'no card number stored anywhere in our database');
  const pt0 = s.paid_through;
  r = await fetch(B + '/api/paytr/notify', { method: 'POST', body: new URLSearchParams(Object.fromEntries(Object.entries(m.notices[0]).filter(([k]) => k !== 'reply'))) });
  ok((await r.text()) === 'OK' && sub(subId).paid_through === pt0, 'repeated notification answered OK and ignored');
  r = await fetch(B + '/api/paytr/notify', { method: 'POST', body: new URLSearchParams({ ...m.notices[0], reply: '', hash: 'forged' }) });
  ok(r.status === 400, 'notification with a wrong hash refused', r.status);

  console.log('3) Approval releases the hold');
  await call('adm', '/api/admin/listings/' + folk, { status: 'approved', tool_id: 'folk' });
  s = sub(subId);
  ok(!s.held_since && Date.parse(s.paid_through) > Date.now() + 27 * 864e5, 'live, paid a month from approval', s.paid_through);

  console.log('4) Automatic renewal by the daily job');
  const soon = new Date(Date.now() + 12 * 36e5).toISOString();
  sql(`UPDATE subs SET paid_through = '${soon}' WHERE id = ${subId}`);
  await cron(); await wait(1500);
  s = sub(subId); m = await mock();
  const ren = m.payments.filter((p) => p.recurring);
  ok(ren.length === 1 && ren[0].non_3d === '1' && !ren[0].has_card_number && ren[0].amount === '99.00', 'stored card charged $99 without card details (Non3D, recurring)', ren);
  ok(Date.parse(s.paid_through) - Date.parse(soon) > 27 * 864e5, 'plan extended by a month', [soon, s.paid_through]);
  ok(sql(`SELECT COUNT(*) AS n FROM invoices WHERE slot_id = ${subId} AND status = 'paid'`)[0].n === 2, 'renewal invoice recorded as paid');
  await cron(); await wait(800);
  ok((await mock()).payments.filter((p) => p.recurring).length === 1, 'running the job again charges nothing (not due)');

  console.log('5) Declined renewal');
  const soon2 = new Date(Date.now() + 6 * 36e5).toISOString();
  sql(`UPDATE subs SET paid_through = '${soon2}' WHERE id = ${subId}`);
  await fetch(M + '/__decline');
  await cron(); await wait(1500);
  s = sub(subId);
  ok(s.paid_through === soon2 && s.auto_renew === 1, 'declined: not extended, renewal stays on for a retry', s);
  ok(sql(`SELECT COUNT(*) AS n FROM invoices WHERE slot_id = ${subId} AND status = 'requested'`)[0].n === 1, 'open invoice left for the vendor to pay in the portal');
  await cron(); await wait(800);
  ok((await mock()).payments.filter((p) => p.recurring).length === 2, 'no second try within the same day');
  sql(`UPDATE paytr_orders SET created_at = '2000-01-01T00:00:00.000Z' WHERE kind = 'renewal'`);
  await cron(); await wait(1500);
  s = sub(subId);
  ok(Date.parse(s.paid_through) > Date.parse(soon2) + 27 * 864e5, 'next day: retry succeeds and extends the plan', s.paid_through);

  console.log('6) Stop renewal');
  const ut = s.provider_sub.slice(6);
  r = await call('vc', `/api/subs/${subId}/stop`, {});
  m = await mock();
  ok(r.ok && sub(subId).auto_renew === 0 && (m.cards[ut] || []).length === 0, 'renewal off and the card deleted at PayTR', r);
  ok(sub(subId).status === 'active', 'position stays live until the paid month ends');

  console.log('7) Paying without saving the card');
  r = await call('vc', '/api/subscribe', { listing_id: folk, page: '/tools/best-hubspot-alternatives/', plan: 'p4', period: 'year', accept_terms: true });
  const sub2 = r.sub_id;
  const inv2 = (await call('vc', '/api/invoices')).rows.find((x) => x.status === 'requested' && x.slot_id === sub2) || (await call('vc', '/api/invoices')).rows.find((x) => x.status === 'requested');
  r = await call('vc', '/api/pay', { invoice_id: inv2.id });
  const h2 = await (await fetch(r.url.replace(/^https?:\/\/[^/]+/, B), { headers: { cookie: 'vs=vc', 'cf-connecting-ip': '85.1.2.3' } })).text();
  const f2 = Object.fromEntries([...h2.matchAll(/<input type="hidden" name="([^"]+)" value="([^"]*)">/g)].map((x) => [x[1], x[2].replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#39;/g, "'")]));
  ok(f2.payment_amount === '637.20', 'yearly #4 priced $637.20', f2.payment_amount);
  await fetch(M + '/odeme', { method: 'POST', redirect: 'manual', body: new URLSearchParams({ ...f2, cc_owner: 'Cem Test', card_number: '4355084355084358', expiry_month: '12', expiry_year: '30', cvv: '000' }) });
  s = sub(sub2);
  ok(s.status === 'active' && s.auto_renew === 0 && !s.provider_sub, 'paid once, no stored card, no automatic renewal', s);

  console.log('8) A declined first payment');
  r = await call('vd', '/api/listings', { product_name: 'Nimble', category: 'best-crm-software', website: 'nimble.com' });
  r = await call('vd', '/api/subscribe', { listing_id: r.id, page: CRM, plan: 'p6', period: 'month', accept_terms: true });
  const sub3 = r.sub_id;
  await call('vd', '/api/billing', { name: 'Deniz', surname: 'Test', phone: '+905550000001', address: 'Test sk. 2', city: 'Izmir', country: 'Turkey' }, 'PUT');
  const inv3 = (await call('vd', '/api/invoices')).rows.find((x) => x.status === 'requested');
  r = await call('vd', '/api/pay', { invoice_id: inv3.id });
  const h3 = await (await fetch(r.url.replace(/^https?:\/\/[^/]+/, B), { headers: { cookie: 'vs=vd', 'cf-connecting-ip': '85.1.2.4' } })).text();
  const f3 = Object.fromEntries([...h3.matchAll(/<input type="hidden" name="([^"]+)" value="([^"]*)">/g)].map((x) => [x[1], x[2].replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#39;/g, "'")]));
  const p3 = await fetch(M + '/odeme', { method: 'POST', redirect: 'manual', body: new URLSearchParams({ ...f3, cc_owner: 'Deniz Test', card_number: '4000000000000002', expiry_month: '12', expiry_year: '30', cvv: '000', store_card: '1' }) });
  const b3 = await fetch(p3.headers.get('location').replace('https://vettlo.com', B), { redirect: 'manual' });
  ok(/pay=failed/.test(b3.headers.get('location') || '') && sub(sub3).status === 'reserved', 'declined card: plan stays reserved, buyer sees "failed"', b3.headers.get('location'));

  m = await mock();
  ok(m.badHash === 0, 'every request to PayTR was correctly signed', m.badHash);
  console.log(`\n${pass} passed, ${fail} failed`);
})().catch((e) => console.log('CRASH', e));
