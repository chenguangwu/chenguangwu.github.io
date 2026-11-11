// 第186批 · IT-N461 api-sign-generator 真 MD5 验证
// 判别核心：MD5 模式必须输出 RFC 1321 真值（node crypto 权威源），而非 SHA-256 前 32 位。
import fs from 'fs';
import { createHash } from 'crypto';
import { webcrypto } from 'crypto';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/api-sign-generator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/api-sign-generator.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    Object.defineProperty(w, 'crypto', { value: webcrypto, configurable: true });
    w.TextEncoder = TextEncoder;
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;

// 判别1：md5Hex 对 RFC 权威向量与长度边界全对（node crypto 逐条对照）
let bad = 0;
for (const n of [0, 1, 3, 14, 26, 55, 56, 57, 63, 64, 65, 77, 119, 120, 200]) {
  const s = 'a'.repeat(n);
  const got = await w.md5Hex(s);
  const want = createHash('md5').update(s).digest('hex');
  if (got !== want) bad++;
}
check('MD5 对 15 组权威向量全对', bad === 0, 'bad=' + bad);

// 判别2：与 SHA-256 前 32 位明确不同（拆穿旧假实现）
const probe = 'a=1&secret=s';
const realMd5 = createHash('md5').update(probe).digest('hex');
const shaPrefix = createHash('sha256').update(probe).digest('hex').slice(0, 32);
check('真 MD5 与 SHA256 前缀不同', realMd5 !== shaPrefix, realMd5 + ' vs ' + shaPrefix);

// 判别3：runSign 的 MD5 路径输出真值
async function runMd5(secret, params) {
  d.getElementById('algo').value = 'md5';
  d.getElementById('secret').value = secret;
  d.getElementById('params').value = params;
  await w.runSign();
  await new Promise(r => setTimeout(r, 20));
  return d.getElementById('out').textContent;
}
const r = await runMd5('s', 'a=1');
const wantSign = createHash('md5').update('a=1&secret=s').digest('hex');
check('runSign MD5 输出真签', r.indexOf('签名结果：' + wantSign) >= 0, r.slice(0, 110));

// 判别4：中文 UTF-8 按字节摘要
const cn = '中文测试';
const cnGot = await w.md5Hex(cn);
const cnWant = createHash('md5').update(Buffer.from(cn, 'utf8')).digest('hex');
check('中文按 UTF-8 摘要', cnGot === cnWant, cnGot + ' vs ' + cnWant);

// 判别5：状态链 MD5→SHA256→MD5 不串味
await runMd5('s', 'a=1');
d.getElementById('algo').value = 'sha256'; await w.runSign(); await new Promise(x => setTimeout(x, 20));
const shaTxt = d.getElementById('out').textContent;
check('切 SHA256 输出 64 位', /签名结果：[0-9a-f]{64}/.test(shaTxt), shaTxt.slice(0, 90));
const r2 = await runMd5('s', 'a=1');
check('切回 MD5 仍真值', r2.indexOf('签名结果：' + wantSign) >= 0, r2.slice(0, 100));

// 判别6：下拉与说明文案已改为真 MD5
const opt = d.querySelector('#algo option[value=md5]').textContent;
check('下拉不再谎称 SHA256 前缀', opt.indexOf('SHA-256 取前 32 位') < 0 && opt.indexOf('RFC 1321') >= 0, opt);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
