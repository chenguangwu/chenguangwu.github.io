// 第188批 · IT-N463 rc4 解密按显式格式解析
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/rc4.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/rc4.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;
const tick = () => new Promise(r => setTimeout(r, 20));

function enc(plain, key, fmt, variant) {
  d.getElementById('key').value = key;
  d.getElementById('variant').value = variant || '0';
  d.getElementById('outputFormat').value = fmt;
  d.getElementById('input').value = plain;
  w.encrypt();
  return d.getElementById('output').value;
}
function dec(cipher, key, fmt, variant) {
  d.getElementById('key').value = key;
  d.getElementById('variant').value = variant || '0';
  d.getElementById('outputFormat').value = fmt;
  d.getElementById('input').value = cipher;
  w.decrypt();
  return d.getElementById('output').value;
}

// 判别1：清单复现——明文 1bb 加密得全 hex 字符的 Base64，解密须还原
const c1 = enc('1bb', 'mysecretkey', 'base64');
check('1bb 加密得歧义 Base64（全 hex 字符）', /^[0-9a-fA-F]+$/.test(c1) && c1.length % 2 === 0, 'cipher=' + c1);
const p1 = dec(c1, 'mysecretkey', 'base64');
check('歧义 Base64 解密还原 1bb', p1 === '1bb', 'got=' + JSON.stringify(p1));

// 判别2：批量往返——随机采样短明文，base64 模式全部往返一致
// 固定歧义样本（node RC4 复刻 + base64，密文恰为全 hex 字符且偶数长度）
const ambiguous = [['1b8','27FA'],['1b9','27FB'],['1bb','27Ea'],['1bc','27Eb'],['1bd','27Ec'],['1be','27Ed']];
let roundOk = 0;
for (const [plain, cipher] of ambiguous) {
  const p = dec(cipher, 'mysecretkey', 'base64');
  if (p === plain) roundOk++;
}
check('歧义样本 base64 往返全对', roundOk === ambiguous.length, roundOk + '/' + ambiguous.length);

// 判别3：hex 格式仍正常往返
const h = enc('hello', 'secret123', 'hex');
const ph = dec(h, 'secret123', 'hex');
check('hex 格式往返正常', /^[0-9a-f]+$/.test(h) && ph === 'hello', h + ' -> ' + ph);

// 判别4：格式不匹配的非法输入被拒（hex 模式喂非 hex）
d.getElementById('key').value = 'k';
d.getElementById('variant').value = '0';
d.getElementById('outputFormat').value = 'hex';
d.getElementById('input').value = 'not-hex!!';
const beforeOut = d.getElementById('output').value;
w.decrypt();
check('hex 模式拒非法字符', d.getElementById('output').value === beforeOut, 'output unchanged');

// 判别5：drop 变体往返
const cd = enc('payload', 'rc4test', 'base64', '2048');
const pd = dec(cd, 'rc4test', 'base64', '2048');
check('RC4-drop2048 往返', pd === 'payload', JSON.stringify(pd));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
