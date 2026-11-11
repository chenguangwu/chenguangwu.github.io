// 第232批探测 · IT-N236~N240（rest-api-cheatsheet 2 条 + md5 3 条）
//  N236 错误格式 syntax 非法 JSON + 未引 RFC 9457
//  N237 deep-dive POST 建指向 /users/{id}
//  N238 HMAC 长密钥 TypeError（探测是否已被其他 agent 修复）
//  N239 取消 UTF-8 后非 ASCII 非标准摘要（探测是否仍在）
//  N240 虚假"批量生成/碰撞检测"宣称（探测是否已改真实功能）
// 用法：node scripts/_verify_it_batch232.mjs [旧页目录]
import fs from 'fs';
import crypto from 'crypto';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 170) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, escHtml: s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
      };
      // checkbox 状态由脚本控制
    }
  });
  const w = dom.window;
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, w, d: w.document, html };
}

const RA = makeDom(OLD_DIR ? OLD_DIR + '/rest-api-cheatsheet.html' : 'tools/it/rest-api-cheatsheet.html');
const MD = makeDom(OLD_DIR ? OLD_DIR + '/md5.html' : 'tools/it/md5.html');
const rawRA = fs.readFileSync(OLD_DIR ? OLD_DIR + '/rest-api-cheatsheet.html' : 'tools/it/rest-api-cheatsheet.html', 'utf8');
const rawMD = fs.readFileSync(OLD_DIR ? OLD_DIR + '/md5.html' : 'tools/it/md5.html', 'utf8');

// ══════════════ N236/N237 rest-api-cheatsheet ══════════════
let cmds = [];
try { cmds = RA.w.eval('COMMANDS'); } catch (e) {}
const errCmd = (cmds || []).find(c => c.cmd === '错误格式') || {};
let syntaxParseOk = false;
try { JSON.parse(errCmd.syntax); syntaxParseOk = true; } catch (e) {}
check('N236 错误格式 syntax 是合法 JSON', syntaxParseOk, errCmd.syntax);
check('N236 错误格式 syntax 含 code 冒号值结构', /"code"\s*:/.test(errCmd.syntax || ''), errCmd.syntax);
check('N236 引据表/页面提到 RFC 9457 problem+json', /9457/.test(rawRA) && /problem\+json/i.test(rawRA), '');
check('N237 deep-dive 未把 POST 建挂到 /users/{id}', !/GET 查、POST 建、PATCH 改/.test(rawRA), (rawRA.match(/用复数名词[^\n<]*/) || [''])[0]);

// ══════════════ N238 HMAC-MD5 文本 UTF-8 语义 + 长密钥 RFC 2104 ══════════════
// 本工具是文本 HMAC 工具：密钥/消息先按 UTF-8 编码成字节再做 HMAC-MD5。
// 参考值用 node crypto 按同一语义计算（不能套 RFC2202 原始字节向量，
// 那些向量把 key 当原始字节，而 UI 输入的是文本、会被 UTF-8 编码）。
const hmacMd5 = MD.w.hmacMd5;
const utf8El = MD.d.getElementById('utf8');
function hmac(key, msg) { return hmacMd5(key, msg); }
function ref(k, m) { return crypto.createHmac('md5', Buffer.from(k, 'utf8')).update(Buffer.from(m, 'utf8')).digest('hex'); }
const vectors = [
  { k: 'Jefe', m: 'what do ya want for nothing?' },
  { k: 'mysecret', m: 'Hello, HMAC-MD5!' },
  { k: 'abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789', m: 'long key 68 chars' }, // >64 字节触发先摘要
  { k: '密'.repeat(40), m: '中文长密钥 120 字节' }, // 中文长密钥
  { k: 'abc123测试', m: '1\n2\n3' }
];
let hmacPass = 0, hmacErr = '';
vectors.forEach((v, i) => {
  let got = '';
  try { got = hmac(v.k, v.m); } catch (e) { hmacErr = 'throw@' + i + ':' + e.message; }
  const exp = ref(v.k, v.m);
  if (got === exp) hmacPass++;
  else hmacErr += ' vec' + i + ' got=' + got + ' exp=' + exp;
});
check('N238 HMAC-MD5 文本UTF8语义5组（含>64字节/中文长密钥）与 crypto 一致', hmacPass === vectors.length, hmacErr || (hmacPass + '/' + vectors.length));
let cnLong = '', cnThrow = false;
try { cnLong = hmac('密'.repeat(40), 'msg'); } catch (e) { cnThrow = true; cnLong = e.message; }
check('N238 中文长密钥不抛 TypeError', !cnThrow && /^[0-9a-f]{32}$/.test(cnLong), cnLong);

// ══════════════ N239 UTF-8 勾选语义 ══════════════
const md5fn = MD.w.md5;
const CN = '密码学哈希函数测试';
const expUtf8 = crypto.createHash('md5').update(CN, 'utf8').digest('hex');
// utf8=true 应与标准一致
if (utf8El) utf8El.checked = true;
let gotUtf8 = ''; try { gotUtf8 = md5fn(CN); } catch (e) {}
check('N239 utf8=true 中文与标准 MD5(utf8) 一致', gotUtf8 === expUtf8, 'got=' + gotUtf8 + ' exp=' + expUtf8);
// utf8=false 当前行为
if (utf8El) utf8El.checked = false;
let gotNoUtf8 = ''; let noThrow = true; try { gotNoUtf8 = md5fn(CN); } catch (e) { noThrow = false; gotNoUtf8 = e.message; }
// 期望：取消后要么按明确 Latin-1 且给提示，要么勾选框被移除（恒 UTF-8）
const nonAsciiHandled = !noThrow ? false :
  (/仅支持|不支持非|Latin|UTF-8|latin/.test(rawMD) && gotNoUtf8 === '') || // 移除勾选/拒绝
  (gotNoUtf8 === expUtf8) || // 无论勾选都 UTF-8
  false;
console.log('    [info] utf8=false 中文结果=' + gotNoUtf8 + '（标准utf8=' + expUtf8 + '）');
check('N239 非 UTF-8 非 ASCII 不再产出非标准摘要', nonAsciiHandled, 'got=' + gotNoUtf8);

// ══════════════ N240 虚假宣称 ══════════════
check('N240 无"支持批量生成，MD5 碰撞检测参考"虚假宣称', !/支持批量生成，?MD5 碰撞检测参考/.test(rawMD), '');
check('N240 逐行批量为真实功能（lineResults + lineMode）', /lineResults/.test(rawMD) && /lineMode/.test(rawMD) && /split\('\\n'\)/.test(rawMD), '');
// 真机：开启 lineMode 后 calcText 产出逐行表格
let lineOk = false, lineInfo = '';
try {
  const lm = MD.d.getElementById('lineMode'), ti = MD.d.getElementById('textInput'), lr = MD.d.getElementById('lineResults');
  if (lm && ti && lr) {
    lm.checked = true; ti.value = 'abc\ndef';
    MD.w.calcText();
    const rows = (lr.innerHTML.match(/<tr>/g) || []).length;
    const hasMd5 = /900150983cd24fb0d6963f7d28e17f72/.test(lr.innerHTML);
    lineOk = rows >= 3 && hasMd5; // 表头 + 2 行
    lineInfo = 'rows=' + rows + ' hasMd5=' + hasMd5;
  }
} catch (e) { lineInfo = e.message; }
check('N240 逐行批量表真机产出2行且含 abc 的正确摘要', lineOk, lineInfo);

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
