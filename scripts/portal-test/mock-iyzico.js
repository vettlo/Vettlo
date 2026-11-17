// Minimal iyzico mock: checks the IYZWSv2 signature on every call and answers like the real API.
const http = require('http'), crypto = require('crypto');
const KEY = 'test-api', SECRET = 'test-secret';
const hmac = (m) => crypto.createHmac('sha256', SECRET).update(m).digest('hex');
const num = (v) => String(Number(v));
const st = { n: 0, forms: {}, plans: {}, subs: {}, calls: [], badAuth: 0 };
const send = (res, o) => { res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
http.createServer((req, res) => {
  let body = ''; req.on('data', (c) => (body += c)); req.on('end', () => {
    const path = req.url.split('?')[0];
    if (path === '/__state') return send(res, st);
    if (path === '/__renew') { const s = st.subs[JSON.parse(body).ref]; s.orders.push({ referenceCode: 'ord-' + (++st.n), price: s.price, currencyCode: 'USD', orderStatus: 'SUCCESS' }); return send(res, s.orders.at(-1)); }
    const auth = req.headers.authorization || '', rnd = req.headers['x-iyzi-rnd'];
    const dec = Buffer.from(auth.replace('IYZWSv2 ', ''), 'base64').toString();
    const sig = (dec.match(/signature:([0-9a-f]+)/) || [])[1];
    if (!dec.startsWith('apiKey:' + KEY) || sig !== hmac(rnd + path + body)) { st.badAuth++; return send(res, { status: 'failure', errorMessage: 'bad auth' }); }
    const b = body ? JSON.parse(body) : {}; st.calls.push(req.method + ' ' + path);
    if (path === '/payment/iyzipos/checkoutform/initialize/auth/ecom') { const t = 'tok' + (++st.n); st.forms[t] = b; return send(res, { status: 'success', token: t, paymentPageUrl: 'http://localhost:9999/page/' + t }); }
    if (path === '/payment/iyzipos/checkoutform/auth/ecom/detail') { const f = st.forms[b.token]; const r = { status: 'success', paymentStatus: 'SUCCESS', fraudStatus: 1, paymentId: 'pay' + (++st.n), currency: f.currency, basketId: f.basketId, conversationId: f.conversationId, paidPrice: f.paidPrice, price: f.price, token: b.token };
      r.signature = hmac([r.paymentStatus, r.paymentId, r.currency, r.basketId, r.conversationId, num(r.paidPrice), num(r.price), r.token].join(':')); return send(res, r); }
    if (path === '/v2/subscription/products') return send(res, { status: 'success', data: { referenceCode: 'prod-1' } });
    let m;
    if ((m = path.match(/^\/v2\/subscription\/products\/([^/]+)\/pricing-plans$/))) { const ref = 'plan-' + (++st.n); st.plans[ref] = b; return send(res, { status: 'success', data: { referenceCode: ref } }); }
    if (path === '/v2/subscription/checkoutform/initialize') { const t = 'stok' + (++st.n); st.forms[t] = b; return send(res, { status: 'success', token: t, checkoutFormContent: '<script>window.MOCK_IYZICO=1</script>' }); }
    if ((m = path.match(/^\/v2\/subscription\/checkoutform\/([^/]+)$/))) { const f = st.forms[m[1]]; const ref = 'sub-' + (++st.n);
      st.subs[ref] = { plan: f.pricingPlanReferenceCode, price: st.plans[f.pricingPlanReferenceCode].price, orders: [{ referenceCode: 'ord-' + (++st.n), price: st.plans[f.pricingPlanReferenceCode].price, currencyCode: 'USD', orderStatus: 'SUCCESS' }] };
      return send(res, { status: 'success', data: { referenceCode: ref, subscriptionStatus: 'ACTIVE' } }); }
    if ((m = path.match(/^\/v2\/subscription\/subscriptions\/([^/]+)\/cancel$/))) { st.subs[m[1]].cancelled = true; return send(res, { status: 'success' }); }
    if ((m = path.match(/^\/v2\/subscription\/subscriptions\/([^/]+)$/))) { const s = st.subs[m[1]]; return send(res, { status: 'success', data: { items: [{ referenceCode: m[1], orders: s.orders }] } }); }
    send(res, { status: 'failure', errorMessage: 'unknown ' + path });
  });
}).listen(9999, () => console.log('mock iyzico on 9999'));
