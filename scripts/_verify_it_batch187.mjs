// 第187批 · IT-N462 api-sign-generator 预设/历史回调重算 + & 分隔解析
import fs from 'fs';
import { createHash } from 'crypto';
import { webcrypto } from 'crypto';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/api-sign-generator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

let presetApply = null;
let historyPick = null;
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
      chart: { line() {} }, matrix: { table() {} },
      preset: { bar(sel, presets, cb) { presetApply = (values) => { for (const k in values) { const e = w.document.getElementById(k); if (e) e.value = values[k]; } cb(); }; } },
      history: {
        add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {},
        mount(sel, cb) { historyPick = cb; }
      }
    };
  }
});
const w = dom.window;
const d = w.document;
await new Promise(r => setTimeout(r, 40)); // 等 DOMContentLoaded 触发 boot 注册预设/历史回调
const tick = () => new Promise(r => setTimeout(r, 25));

// 判别1：& 分隔解析成多个参数（parseParams 函数级）
function parse(v) { d.getElementById('params').value = v; const o = w.parseParams(); return o; }
const o1 = parse('a=1&b=2&c=3');
check('& 分隔解析成 3 参数', Object.keys(o1).length === 3 && o1.a === '1' && o1.b === '2' && o1.c === '3', JSON.stringify(o1));
const o2 = parse('a=1\nb=2\nc=3');
check('换行分隔仍兼容', Object.keys(o2).length === 3 && o2.c === '3', JSON.stringify(o2));

// 判别2：预设点击真正重算并得权威签名
if (presetApply) {
  presetApply({ secret: 'my_secret_key', algo: 'sha256', params: 'a=1&b=2&c=3' });
  await tick();
  const txt = d.getElementById('out').textContent;
  const want = createHash('sha256').update('a=1&b=2&c=3').digest('hex'); // hmac 另算
  // HMAC-SHA256 用 node：
  const { createHmac } = await import('crypto');
  const wantHmac = createHmac('sha256', 'my_secret_key').update('a=1&b=2&c=3').digest('hex');
  check('预设回调重算（含 & 参数）', txt.indexOf('待签名串：a=1&b=2&c=3&secret=my_secret_key') >= 0, txt.slice(0, 100));
  check('预设 HMAC 值正确', txt.indexOf(wantHmac) >= 0, 'want=' + wantHmac.slice(0, 16));
} else {
  check('预设回调已注册', false, 'presetApply null');
}

// 判别3：历史恢复回调重算
try { w.__api_sign_generatorRender(['secret','params','algo'], 'Result', false); } catch (e) {}
if (historyPick) {
  d.getElementById('secret').value = 'OLD';
  d.getElementById('params').value = 'x=9';
  d.getElementById('algo').value = 'md5';
  historyPick({ secret: 'hist_key', algo: 'sha256', params: 'p=1&q=2', __tbScore: 1, Result: 'x' });
  await tick();
  const txt = d.getElementById('out').textContent;
  check('历史恢复重载入输入', d.getElementById('secret').value === 'hist_key' && d.getElementById('params').value === 'p=1&q=2', d.getElementById('secret').value + '/' + d.getElementById('params').value);
  check('历史恢复重算结果', txt.indexOf('待签名串：p=1&q=2&secret=hist_key') >= 0, txt.slice(0, 100));
} else {
  check('历史回调已注册', false, 'historyPick null');
}

// 判别4：复制按钮仍只复制不重算（包装器没被破坏）
let copyOk = true;
try { w.copyResult(); } catch (e) { copyOk = false; }
await tick();
check('复制回调不抛异常', copyOk && !!d.getElementById('out'), 'copy=' + copyOk);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
