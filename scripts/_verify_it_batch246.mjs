// 第246批探测 · IT-N58/N97/N98/N99/N100（regex-escape / ssl-info）
//  N58 非法 \x/\u 转义不抛异常、保留字面
//  N97 英文简介与中文同为静态说明（无"从主机读取证书"承诺）
//  N98 仅一条预设栏、无截断省略号
//  N99 formatTime 临界值不跨档（59.7→1分钟、86399→1天、31535999→1年）
//  N100 算力负数明确拒绝并回退，不产出负时间
// 用法：node scripts/_verify_it_batch246.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom(file) {
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + file.split('/').pop(),
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const f = name => OLD_DIR ? OLD_DIR + '/' + name : 'tools/it/' + name;

// ══════════════ N58 正则转义非法逃逸 ══════════════
{
  const dom = makeDom(f('regex-escape.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('input'), out = d.getElementById('output');
  for (const bad of ['\\xZZ', '\\uZZZZ', '\\u{110000}', '\\u{']) {
    input.value = bad;
    let threw = false;
    try { w.unesc(); } catch (e) { threw = true; }
    check('N58 ' + JSON.stringify(bad) + ' 不抛异常', !threw, threw ? 'THREW' : 'ok');
  }
  // 合法仍正确
  input.value = '\\x41\\u4e2d';
  w.unesc();
  check('N58 合法转义正常解码 A中', out.value === 'A中', 'out=' + JSON.stringify(out.value));
}

// ══════════════ N97 英文静态说明 ══════════════
{
  const en = fs.readFileSync('i18n/tools/en/it/ssl-info.json','utf8');
  const enIt = fs.readFileSync('i18n/tools/it.json','utf8');
  check('N97 英文映射无"从主机读取证书"承诺', !/read certificate details \(issuer, validity, SAN\) from a host/i.test(en) && !/Decode and inspect SSL\/TLS certificate/i.test(en), 'checked');
  check('N97 英文为静态说明（browsers cannot read）', /Browsers cannot read remote certificates/i.test(en), 'checked');
  const html = fs.readFileSync(f('ssl-info.html'),'utf8');
  check('N97 页面中文 meta 为静态说明', /浏览器无法直接读取远程证书/.test(html), 'checked');
}

// ══════════════ N98 单预设栏 ══════════════
{
  const html = fs.readFileSync(f('ssl-info.html'),'utf8');
  const handWritten = (html.match(/data-tb="preset"/g) || []).length;
  check('N98 无手写 data-tb=preset（截断标签）', handWritten === 0 && !/ae…|aes1…/.test(html), 'handWritten=' + handWritten);
  check('N98 有显式预设宿主 ssl_infoPresets', /id="ssl_infoPresets"/.test(html), 'host present');
  const dom = makeDom(f('ssl-info.html'));
  const d = dom.window.document;
  const host = d.getElementById('ssl_infoPresets');
  check('N98 宿主存在于渲染 DOM', !!host, host ? 'found' : 'missing');
}

// ══════════════ N99 formatTime 临界值 ══════════════
{
  const dom = makeDom(f('ssl-info.html'));
  const ft = dom.window.formatTime;
  check('N99 59.7秒 → 1 分钟（非 60 秒）', ft(59.7) === '1 分钟', ft(59.7));
  check('N99 86399秒 → 1 天（非 24 小时）', ft(86399) === '1 天', ft(86399));
  check('N99 31535999秒 → 1 年（非 12 个月）', ft(31535999) === '1 年', ft(31535999));
  check('N99 常规值仍正确（90秒/2小时/2个月）', ft(90) === '2 分钟' && ft(7200) === '2 小时' && ft(5184000) === '2 个月', [ft(90),ft(7200),ft(5184000)].join('/'));
}

// ══════════════ N100 算力负数校验 ══════════════
{
  const dom = makeDom(f('ssl-info.html'));
  const w = dom.window, d = w.document;
  const speed = d.getElementById('calcSpeed'), crack = d.getElementById('crackTime');
  speed.value = '-100';
  w.estimate();
  check('N100 负数算力明确拒绝', /算力须为正数|Invalid speed/.test(crack.textContent) && !/不安全/.test(crack.textContent), crack.textContent.slice(0, 80));
  speed.value = '0';
  w.estimate();
  check('N100 零算力明确拒绝', /算力须为正数|Invalid speed/.test(crack.textContent), crack.textContent.slice(0, 80));
  speed.value = '1000000000000';
  w.estimate();
  check('N100 合法算力正常估算', !/算力须为正数|Invalid speed/.test(crack.textContent) && crack.textContent.length > 0, crack.textContent.slice(0, 80));
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
