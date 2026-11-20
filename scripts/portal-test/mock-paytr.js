// Minimal PayTR mock (Direct API + card storage). Checks every hash like the real service and sends the
// server-to-server notification to the local Worker, so the full flow runs without real cards or money.
const http = require('http'), crypto = require('crypto');
const ID = '123456', KEY = 'test-key', SALT = 'test-salt', NOTIFY = process.env.NOTIFY || 'http://localhost:8787/api/paytr/notify';
const b64 = (m) => crypto.createHmac('sha256', KEY).update(m).digest('base64');
const st = { n: 0, cards: {}, payments: [], notices: [], badHash: 0, declineNext: false };
const send = (res, o, code = 200) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
async function notify(f, status) {
  const cents = String(Math.round(Number(f.payment_amount) * 100));
  const n = { merchant_oid: f.merchant_oid, status, total_amount: status === 'success' ? cents : '0', payment_amount: cents, currency: f.currency, test_mode: f.test_mode,
    payment_type: 'card', installment_count: '0', ...(f.utoken ? { utoken: f.utoken } : {}), ...(status !== 'success' ? { failed_reason_code: '0', failed_reason_msg: 'Kart limiti yetersiz' } : {}) };
  n.hash = b64(n.merchant_oid + SALT + n.status + n.total_amount);
  st.notices.push(n);
  const r = await fetch(NOTIFY, { method: 'POST', body: new URLSearchParams(n) }); n.reply = await r.text();
}
http.createServer((req, res) => {
  let body = ''; req.on('data', (c) => (body += c)); req.on('end', async () => {
    const path = req.url.split('?')[0];
    if (path === '/__state') return send(res, st);
    if (path === '/__decline') { st.declineNext = true; return send(res, { ok: true }); }
    const f = Object.fromEntries(new URLSearchParams(body));
    if (f.merchant_id !== ID) { st.badHash++; return send(res, { status: 'error', err_msg: 'merchant' }); }
    if (path === '/odeme/capi/list') {
      if (f.paytr_token !== b64(f.utoken + SALT)) { st.badHash++; return send(res, { status: 'error', err_msg: 'hash' }); }
      return send(res, st.cards[f.utoken] || []);
    }
    if (path === '/odeme/capi/delete') {
      if (f.paytr_token !== b64(f.ctoken + f.utoken + SALT)) { st.badHash++; return send(res, { status: 'error', err_msg: 'hash' }); }
      st.cards[f.utoken] = (st.cards[f.utoken] || []).filter((c) => c.ctoken !== f.ctoken); return send(res, { status: 'success' });
    }
    if (path === '/odeme') {
      const tok = b64(f.merchant_id + f.user_ip + f.merchant_oid + f.email + f.payment_amount + f.payment_type + f.installment_count + f.currency + f.test_mode + f.non_3d + SALT);
      if (f.paytr_token !== tok) { st.badHash++; return send(res, { status: 'failed', reason: 'hash' }); }
      st.payments.push({ oid: f.merchant_oid, amount: f.payment_amount, recurring: f.recurring_payment === '1', non_3d: f.non_3d, has_card_number: !!f.card_number, currency: f.currency, test_mode: f.test_mode });
      if (f.recurring_payment === '1') { // stored-card charge from the Worker (sync_mode)
        const ok = (st.cards[f.utoken] || []).some((c) => c.ctoken === f.ctoken) && !st.declineNext; st.declineNext = false;
        send(res, ok ? { status: 'success', utoken: f.utoken, ctoken: f.ctoken } : { status: 'failed', err_msg: 'Kart limiti yetersiz' });
        setTimeout(() => notify(f, ok ? 'success' : 'failed'), 50); return;
      }
      // first payment, posted by the buyer's browser
      if (!/^\d{16}$/.test(f.card_number || '') || !f.cvv || !f.cc_owner) { res.writeHead(302, { location: f.merchant_fail_url }); return res.end(); }
      if (f.store_card === '1') { f.utoken = 'u' + (++st.n); st.cards[f.utoken] = [{ ctoken: 'c' + (++st.n), last_4: f.card_number.slice(-4), require_cvv: '0', month: f.expiry_month, year: f.expiry_year }]; }
      await notify(f, f.card_number.endsWith('0002') ? 'failed' : 'success');
      res.writeHead(302, { location: f.merchant_ok_url }); return res.end();
    }
    send(res, { status: 'error', err_msg: 'unknown ' + path }, 404);
  });
}).listen(9998, () => console.log('mock paytr on 9998'));
