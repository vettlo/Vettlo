// Minimal Paddle Billing mock: checks the API key, stores catalog/transactions/subscriptions, and sends signed
// webhooks to the local Worker when the test "completes" a checkout, renews, cancels or refunds.
const http = require('http'), crypto = require('crypto');
const KEY = 'test-api-key', SECRET = 'test-webhook-secret', HOOK = process.env.HOOK || 'http://localhost:8787/api/paddle/webhook';
const st = { n: 0, products: {}, prices: {}, txns: {}, subs: {}, hooks: [], badAuth: 0 };
const id = (p) => p + '_' + String(++st.n).padStart(6, '0');
const send = (res, o, code = 200) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
async function hook(event_type, data, opts = {}) {
  const body = JSON.stringify({ event_id: id('evt'), event_type, occurred_at: new Date().toISOString(), data });
  const ts = opts.ts || Math.floor(Date.now() / 1000);
  const h1 = opts.badSig ? 'deadbeef' : crypto.createHmac('sha256', SECRET).update(ts + ':' + body).digest('hex');
  const r = await fetch(HOOK, { method: 'POST', headers: { 'content-type': 'application/json', 'paddle-signature': `ts=${ts};h1=${h1}` }, body });
  const out = { event_type, status: r.status }; st.hooks.push(out); return out;
}
function txnData(t) { const p = st.prices[t.items[0].price_id]; const sub = Number(p.unit_price.amount);
  return { id: t.id, status: 'completed', subscription_id: t.subscription_id || null, custom_data: t.custom_data, origin: t.origin,
    details: { totals: { subtotal: String(sub), tax: String(Math.round(sub * 0.2)), total: String(Math.round(sub * 1.2)), currency_code: 'USD' } }, items: t.items }; }
const srv = http.createServer((req, res) => {
  let body = ''; req.on('data', (c) => (body += c)); req.on('end', async () => { try {
    const path = req.url.split('?')[0], b = body ? JSON.parse(body) : {};
    if (path === '/__state') return send(res, st);
    if (path === '/__complete') { const t = st.txns[b.txn]; const sid = id('sub'); t.subscription_id = sid; t.origin = 'web';
      const p = st.prices[t.items[0].price_id];
      st.subs[sid] = { id: sid, status: 'active', custom_data: t.custom_data, price_id: p.id, billing_cycle: p.billing_cycle, scheduled_change: null };
      const a = await hook('subscription.created', st.subs[sid]); const c = await hook('transaction.completed', txnData(t));
      if (b.again) await hook('transaction.completed', txnData(t));
      return send(res, { sub: sid, hooks: [a, c] }); }
    if (path === '/__renew') { const s = st.subs[b.sub]; const t = { id: id('txn'), items: [{ price_id: s.price_id, quantity: 1 }], custom_data: s.custom_data, subscription_id: s.id, origin: 'subscription_recurring' };
      st.txns[t.id] = t; return send(res, await hook('transaction.completed', txnData(t), b)); }
    if (path === '/__schedule_cancel') { const s = st.subs[b.sub]; s.scheduled_change = { action: 'cancel', effective_at: new Date(Date.now() + 864e5).toISOString() };
      return send(res, await hook('subscription.updated', s)); }
    if (path === '/__past_due') { const s = st.subs[b.sub]; s.status = 'past_due'; const r = await hook('subscription.past_due', s); s.status = 'active'; return send(res, r); }
    if (path === '/__refund') return send(res, await hook('adjustment.created', { id: id('adj'), action: 'refund', type: 'full', status: 'approved', transaction_id: b.txn,
      subscription_id: st.txns[b.txn].subscription_id, totals: { subtotal: txnData(st.txns[b.txn]).details.totals.subtotal } }));
    if (req.headers.authorization !== 'Bearer ' + KEY) { st.badAuth++; return send(res, { error: { code: 'authentication_malformed' } }, 403); }
    let m;
    if (path === '/products' && req.method === 'POST') { const p = { id: id('pro'), ...b }; st.products[p.id] = p; return send(res, { data: p }, 201); }
    if (path === '/prices' && req.method === 'POST') { if (!st.products[b.product_id]) return send(res, { error: { detail: 'no product' } }, 400); const p = { id: id('pri'), ...b }; st.prices[p.id] = p; return send(res, { data: p }, 201); }
    if (path === '/transactions' && req.method === 'POST') { if (!st.prices[b.items?.[0]?.price_id]) return send(res, { error: { detail: 'bad price' } }, 400);
      const t = { id: id('txn'), status: 'draft', ...b }; st.txns[t.id] = t; return send(res, { data: { ...t, checkout: { url: b.checkout.url + '?_ptxn=' + t.id } } }, 201); }
    if ((m = path.match(/^\/subscriptions\/([^/]+)\/cancel$/)) && req.method === 'POST') { const s = st.subs[m[1]]; if (!s) return send(res, { error: { detail: 'not found' } }, 404);
      if (b.effective_from === 'immediately') s.status = 'canceled'; else s.scheduled_change = { action: 'cancel' }; s.cancel_mode = b.effective_from; return send(res, { data: s }); }
    if ((m = path.match(/^\/subscriptions\/([^/]+)$/)) && req.method === 'PATCH') { const s = st.subs[m[1]]; if (!s) return send(res, { error: { detail: 'not found' } }, 404);
      if (b.next_billed_at && !b.proration_billing_mode) return send(res, { error: { detail: 'proration_billing_mode required' } }, 400); Object.assign(s, b); return send(res, { data: s }); }
    send(res, { error: { detail: 'unknown ' + req.method + ' ' + path } }, 404);
  } catch (e) { console.error(e); send(res, { error: { detail: String(e) } }, 500); } });
});
srv.keepAliveTimeout = 120000; // the test runs slow wrangler commands between calls; don't drop idle sockets
srv.listen(9997, () => console.log('mock paddle on 9997'));
