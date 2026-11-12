// 第281批 JSDOM 验证：IT-N334 Baudot 缺 8 / IT-N349 JWT 假 HMAC
// 用法: node scripts/_verify_it_batch281.mjs [OLD_DIR]
import fs from 'fs';
import nodeCrypto from 'crypto';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const root = OLD || '.';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function stub(w) {
  w.ToolBox = { showToast() {}, toast() {}, copyText() {} };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {} }, matrix: { table() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {} },
    preset: { bar() {} },
  };
  w.i18nText = () => '';
  w.alert = () => {};
}

// ---------- N334：Baudot ITA2 数字 8 ----------
const bd = new JSDOM(fs.readFileSync(`${root}/tools/it/baudot-code.html`, 'utf8'), {
  runScripts: 'dangerously', url: 'https://x.com/baudot-code.html',
  beforeParse(w) { stub(w); },
});
const wb = bd.window, db = wb.document;
db.getElementById('format').value = 'binary';
db.getElementById('input').value = '8';
wb.enc();
check('N334 单独 8 编码为 FIGS 切换 + code6', db.getElementById('output').value === '11011 00110', db.getElementById('output').value);
db.getElementById('input').value = 'H8I';
wb.enc();
check('N334 H8I 编码含 FIGS/LTRS 切换且 8 不丢', db.getElementById('output').value === '10100 11011 00110 11111 00110', db.getElementById('output').value);

// ---------- N349：JWT 标准 HMAC ----------
const jw = new JSDOM(fs.readFileSync(`${root}/tools/it/jwt-debugger.html`, 'utf8'), {
  runScripts: 'dangerously', url: 'https://x.com/jwt-debugger.html',
  beforeParse(w) {
    stub(w);
    w.TextEncoder = TextEncoder;
    try { Object.defineProperty(w, 'crypto', { value: nodeCrypto.webcrypto, configurable: true }); } catch (e) { /* JSDOM 可能只读 */ }
  },
});
const wj = jw.window, dj = wj.document;
const secret = 'your-secret-key';
const payload = '{"sub":"123"}';
const b64u = (s) => Buffer.from(s, 'utf8').toString('base64url');
const headerB64 = b64u(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
const payloadB64 = b64u(payload);
const expected = nodeCrypto.createHmac('sha256', secret).update(headerB64 + '.' + payloadB64).digest('base64url');

dj.getElementById('alg').value = 'HS256';
dj.getElementById('secret').value = secret;
dj.getElementById('gen-payload').value = payload;
await wj.generateJwt();
const token = dj.getElementById('gen-output').value || '';
const parts = token.split('.');
check('N349 生成三段 JWT', parts.length === 3, 'parts=' + parts.length);
check('N349 HS256 签名与 node crypto 标准一致', parts[2] === expected, 'got=' + parts[2] + ' / std=' + expected);

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
