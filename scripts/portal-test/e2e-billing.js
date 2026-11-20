// Admin-led sales with invoices paid outside the site (Payoneer): admin order form, customers list, mark paid,
// approval, and the daily billing job (renewal invoice, reminder, lapse). Run against a local Worker in invoice mode
// (no PADDLE_* / IYZICO_* settings) started with --test-scheduled; seed admin@ex.com with session token "adm".
const { execSync } = require('child_process');
const B = 'http://localhost:8787';
const WR = process.env.WRANGLER || 'npx wrangler', STATE = process.env.STATE || '/tmp/vettlo-billing';
let pass = 0, fail = 0;
const ok = (c, msg, extra) => { if (c) { pass++; console.log('  ✓ ' + msg); } else { fail++; console.log('  ✗ ' + msg, extra !== undefined ? JSON.stringify(extra).slice(0, 400) : ''); } };
const call = async (who, path, body, method) => { const r = await fetch(B + path, { method: method || (body ? 'POST' : 'GET'), redirect: 'manual',
  headers: { cookie: 'vs=' + who, 'content-type': 'application/json', 'x-requested-with': 'vettlo' }, body: body ? JSON.stringify(body) : undefined });
  const t = await r.text(); try { return { status: r.status, ...JSON.parse(t) }; } catch { return { status: r.status, text: t }; } };
const sql = (q) => JSON.parse(execSync(`${WR} d1 execute vettlo --local --persist-to ${STATE} --json --command "${q.replace(/"/g, '\\"')}"`, { cwd: __dirname + '/../..', stdio: ['ignore', 'pipe', 'ignore'] }).toString())[0].results;
const cron = async () => { for (const u of ['/cdn-cgi/handler/scheduled?cron=47+5+*+*+*', '/__scheduled?cron=47+5+*+*+*']) { const r = await fetch(B + u); if (r.ok) return true; } return false; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const order = async (page) => { const h = await (await fetch(B + page)).text(); const ol = (h.match(/<ol class="shortlist">([\s\S]*?)<\/ol>/) || [])[1] || '';
  return [...ol.matchAll(/<li>[\s\S]*?<\/li>/g)].map((m) => (m[0].match(/href="#([a-z0-9-]+)"/) || [])[1]); };
const cust = async (id) => (await call('adm', '/api/admin/overview')).customers.find((c) => c.id === id);
const CRM = '/tools/best-crm-software/', HALT = '/tools/best-hubspot-alternatives/';

(async () => {
  console.log('1) Admin creates orders');
  let r = await call('adm', '/api/admin/orders', { company: 'Attio Ltd', email: 'billing@attio.example', product_name: 'Attio', product_website: 'attio.com', page: CRM, plan: 'p2', period: 'year', tool_id: 'attio', notify: true });
  ok(r.ok && r.amount_cents === 106920 && !r.paid, 'yearly #2 on CRM: invoice $1,069.20 opened, awaiting payment', r);
  const s1 = r.sub_id, inv1 = r.invoice_id;
  ok((await call('vc', '/api/admin/orders', { company: 'X', email: 'x@x.example', product_name: 'X', product_website: 'x.com', page: CRM, plan: 'p3', period: 'year' })).status === 403, 'vendors cannot create orders');
  ok((await call('adm', '/api/admin/orders', { company: 'Close', email: 'ops@close.example', product_name: 'Close', product_website: 'close.com', page: CRM, plan: 'p2', period: 'month' })).status === 409, 'taken position refused');
  ok((await call('adm', '/api/admin/orders', { company: 'Close', email: 'not-an-email', product_name: 'Close', product_website: 'close.com', page: CRM, plan: 'p4', period: 'month' })).status === 400, 'bad email refused');
  r = await call('adm', '/api/admin/orders', { company: 'Close', email: 'ops@close.example', product_name: 'Close', product_website: 'close.com', page: HALT, plan: 'p1', period: 'month', price: '120', tool_id: 'close', paid: true, ref: 'PYN-123' });
  ok(r.ok && r.paid && r.amount_cents === 12000 && r.paid_through, 'monthly #1 on HubSpot alternatives at a custom $120, already paid', r);
  const s2 = r.sub_id;
  r = await call('adm', '/api/admin/orders', { company: 'Nimble', email: 'hi@nimble.example', product_name: 'Nimble', product_website: 'nimble.com', page: CRM, plan: 'p5', period: 'month' });
  ok(r.ok && r.listing_status === 'pending', 'product we have not reviewed yet is created as pending', r);
  const s3 = r.sub_id;

  console.log('2) Customers list and mark paid');
  let c1 = await cust(s1);
  ok(c1 && c1.company === 'Attio Ltd' && c1.status === 'reserved' && c1.open_amount === 106920 && c1.period === 'year', 'customer row shows company, awaiting payment, open invoice', c1);
  ok((await order(CRM))[1] !== 'attio', 'not on the page before payment', await order(CRM));
  r = await call('adm', '/api/admin/invoices/' + inv1, { status: 'paid', ref: 'PYN-456' });
  c1 = await cust(s1);
  ok(r.ok && c1.status === 'active' && c1.started_at && c1.last_ref === 'PYN-456' && c1.paid_total === 106920 && Date.parse(c1.paid_through) > Date.now() + 364 * 864e5, 'marked paid: started, paid a year, Payoneer ref kept', c1);
  ok((await order(CRM))[1] === 'attio', 'Attio now at #2 on the CRM shortlist', await order(CRM));
  ok((await order(HALT))[0] === 'close', 'Close at #1 on HubSpot alternatives', await order(HALT));
  await call('adm', '/api/admin/invoices/' + (await cust(s3)).open_invoice, { status: 'paid', ref: 'PYN-789' });
  const c3 = await cust(s3);
  ok(c3.status === 'active' && c3.held_since, 'unreviewed product: paid but held in review', c3);
  const v = (await call('adm', '/api/admin/overview')).vendors;
  ok(v.some((x) => x.email === 'billing@attio.example' && x.company === 'Attio Ltd'), 'vendor account created, so they can sign in to see stats');

  console.log('3) Daily billing job');
  const soon = new Date(Date.now() + 5 * 864e5).toISOString();
  sql(`UPDATE subs SET paid_through = '${soon}' WHERE id = ${s2}`);
  ok(await cron(), 'scheduled handler runs');
  await wait(800);
  let c2 = await cust(s2);
  ok(c2.open_invoice && c2.open_amount === 12000, 'renewal invoice opened 5 days before the end, at the customer price', c2);
  await cron(); await wait(500);
  ok(sql(`SELECT COUNT(*) AS n FROM invoices WHERE slot_id = ${s2} AND status = 'requested'`)[0].n === 1, 'running again opens no second invoice');
  const tomorrow = new Date(Date.now() + 20 * 3600e3).toISOString();
  sql(`UPDATE subs SET paid_through = '${tomorrow}' WHERE id = ${s2}`);
  await cron(); await wait(500);
  ok(sql(`SELECT COUNT(*) AS n FROM notices WHERE sub_id = ${s2} AND kind = 'reminder'`)[0].n === 1, 'reminder recorded the day before it ends');
  r = await call('adm', '/api/admin/invoices/' + c2.open_invoice, { status: 'paid', ref: 'PYN-REN' });
  c2 = await cust(s2);
  ok(r.ok && Date.parse(c2.paid_through) - Date.parse(tomorrow) > 27 * 864e5 && c2.paid_total === 24000, 'renewal paid: extended by a month, $240 paid so far', c2);
  sql(`UPDATE subs SET paid_through = '${new Date(Date.now() - 3600e3).toISOString()}' WHERE id = ${s3}`);
  sql(`UPDATE subs SET held_since = NULL WHERE id = ${s3}`);
  await cron(); await wait(500);
  ok(sql(`SELECT COUNT(*) AS n FROM notices WHERE sub_id = ${s3} AND kind = 'lapsed'`)[0].n === 1 && (await cust(s3)).paid_through < new Date().toISOString(), 'ended unpaid plan reported as lapsed');

  console.log('4) End now');
  r = await call('adm', `/api/admin/subs/${s2}/end`, {});
  ok(r.ok && (await cust(s2)).status === 'cancelled' && (await order(HALT))[0] !== 'close', 'End now takes it off #1 (Close stays only where our editorial list has it)', await order(HALT));
  console.log(`\n${pass} passed, ${fail} failed`);
})().catch((e) => console.log('CRASH', e));
