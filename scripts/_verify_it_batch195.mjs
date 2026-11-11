// 第195批 · IT-N113/N114/N115/N116 IPv6 ULA 生成器四项修复（JSDOM 真机）
import fs from 'fs';
import { webcrypto } from 'crypto';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/ipv6-ula.html';
const ENFILE = 'i18n/tools/en/it/ipv6-ula.json';
const DDFILE = 'i18n/tools/content_deepdive.json';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 140) : '')); }

let isEn = false;
let grvCalls = 0;
let history = [];
let tableRows = null, tableName = '', toastMsgs = [];
let copiedText = '';
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/ipv6-ula.html',
  beforeParse(w) {
    w.alert = () => {};
    // 真机注入 webcrypto，并统计 getRandomValues 调用次数（IT-N114）
    Object.defineProperty(w, 'crypto', {
      configurable: true,
      value: {
        getRandomValues(a) { grvCalls++; return webcrypto.getRandomValues(a); }
      }
    });
    w.i18nText = k => k;
    w.ToolBox = { showToast(m) { toastMsgs.push(String(m)); }, copyText() {}, downloadText() {} };
    Object.defineProperty(w.navigator, 'clipboard', {
      configurable: true,
      value: { writeText(t) { copiedText = String(t); return Promise.resolve(); } }
    });
    w.TBKit = {
      util: {
        isEn: () => isEn,
        exportTable(_sel, name) { tableName = name; },
        downloadText() {}
      },
      matrix: { table(_sel, cfg) { tableRows = cfg.rows; } },
      preset: { bar() {}, select() {} },
      history: {
        list() { return history; },
        last() { return history.length ? history[history.length - 1].d : null; },
        record(r) { history.push({ t: Date.now(), d: r }); },
        mount() {}, clear() { history = []; }
      }
    };
  }
});
const w = dom.window;
const d = w.document;
function fire(n) { d.dispatchEvent(new w.Event(n, { bubbles: true })); }
function run(cnt) {
  d.getElementById('cnt').value = String(cnt);
  grvCalls = 0;
  w.eval('calcTool()');
  return d.getElementById('result').textContent;
}
fire('DOMContentLoaded');

// 判别1：IT-N113 上限 clamp 到 50
const t99 = run(99);
check('cnt=99 clamp 到 50', t99.indexOf('IPv6 ULA（50 个）') >= 0, t99.slice(0, 40));
check('cnt=99 生成 50 条前缀', (t99.match(/示例 /g) || []).length === 50);
const t0 = run(0);
check('cnt=0 非法回退为 3', t0.indexOf('IPv6 ULA（3 个）') >= 0, t0.slice(0, 40));
const tNeg = run(-5);
check('cnt=-5 clamp 到下限 1', tNeg.indexOf('IPv6 ULA（1 个）') >= 0);

// 判别2：IT-N114 安全随机（crypto.getRandomValues 真调用 + 结构合规 + 无降级告警）
grvCalls = 0;
const t10 = run(10);
check('安全随机：getRandomValues 被多次调用', grvCalls >= 20, 'calls=' + grvCalls);
check('安全随机：无降级告警', t10.indexOf('非安全伪随机') < 0);
const pairs = t10.match(/(fd[0-9A-F]{2}:[0-9A-F]{4}:[0-9A-F]{4})::\/48\s+示例\s+\1::([0-9A-F]{4}:[0-9A-F]{4}:[0-9A-F]{4}:[0-9A-F]{4})/g) || [];
check('生成 10 条前缀', pairs.length === 10, 'n=' + pairs.length);
const structOk = pairs.length === 10;
check('前缀/示例地址结构合规（40位全局ID+16位接口标识4组）', structOk, pairs[0] || '');
const fdOk = (t10.match(/fd[0-9A-F]{2}:[0-9A-F]{4}:[0-9A-F]{4}::\/48/g) || []).length === 10;
check('fd 前缀合法（前8位 11111101）', fdOk);
// 两次生成结果不同（真随机，非固定串）
const t10b = run(10);
check('两次生成结果不同', t10 !== t10b);

// 判别3：IT-N115 说明纠错（页面 + 权威源 + en JSON 三源一致）
check('页面说明为 8 位 fd', t10.indexOf('fd = 二进制 1111 1101，共 8 位，其中 L 位为 1') >= 0, t10.slice(-140));
check('页面说明 40 位全局 ID + 16 位子网', t10.indexOf('后接 40 位全局 ID + 16 位子网') >= 0);
check('页面说明无旧 48 位全局 ID 说法', t10.indexOf('48 位全局 ID') < 0);
const dd = JSON.parse(fs.readFileSync(DDFILE, 'utf8'));
const ddStr = JSON.stringify(dd);
check('权威源含 40 位全局 ID 新说法', ddStr.indexOf('40 位全局 ID 随机，后接 16 位子网 ID') >= 0);
check('权威源无旧 48 位全局 ID 说法', ddStr.indexOf('48 位全局 ID 随机') < 0);
const en = JSON.parse(fs.readFileSync(ENFILE, 'utf8'));
const enStr = JSON.stringify(en);
check('en JSON 含 1 到 50', enStr.indexOf('1 到 50') >= 0 && (enStr.indexOf('1–50') >= 0 || enStr.indexOf('1 to 50') >= 0));
check('en JSON 无旧 1 到 20', enStr.indexOf('1 到 20') < 0);
check('en JSON 含 40 位全局 ID 新说法', enStr.indexOf('40 位全局 ID 随机，后接 16 位子网 ID') >= 0);

// 判别4：IT-N116 复制全部前缀 + 导出当前产物
run(3);
tableRows = null; tableName = ''; copiedText = '';
try { w.eval('copyUlaPrefixes({target:{textContent:"复制全部前缀"}})'); } catch (e) { copiedText = ''; }
check('复制按钮把本次前缀写入剪贴板', copiedText.split('::/48').length - 1 === 3 && copiedText.indexOf('fd') === 0, copiedText.slice(0, 70));
try { w.eval('__ipv6_ulaExport()'); } catch (e) { tableName = ''; }
check('导出文件名为 ipv6-ula.csv', tableName === 'ipv6-ula.csv', tableName);
check('导出表为本次生成的 3 行前缀/示例地址', Array.isArray(tableRows) && tableRows.length === 3 && tableRows[0][0].indexOf('::/48') > 0 && tableRows[0][1].indexOf('::') > 0, JSON.stringify(tableRows && tableRows[0]));
check('页面含复制按钮', d.getElementById('result').innerHTML.indexOf('复制全部前缀') >= 0);

// 判别5：英文态文案
isEn = true;
const ten = run(2);
check('英文态计数标题', ten.indexOf('IPv6 ULA（2') >= 0 || d.getElementById('result').textContent.indexOf('IPv6 ULA（2') >= 0);
check('英文态含 Copy all prefixes', d.getElementById('result').innerHTML.indexOf('Copy all prefixes') >= 0);
check('英文态含 40-bit global ID', d.getElementById('result').textContent.indexOf('40-bit global ID') >= 0);
isEn = false;

// 判别6：状态链 合法 → 非法 → 恢复
const valid = run(4);
check('状态链合法', valid.indexOf('IPv6 ULA（4 个）') >= 0);
d.getElementById('cnt').value = 'abc';
w.eval('calcTool()');
check('状态链非法回退 3', d.getElementById('result').textContent.indexOf('IPv6 ULA（3 个）') >= 0);
const recovered = run(5);
check('状态链恢复', recovered.indexOf('IPv6 ULA（5 个）') >= 0);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
