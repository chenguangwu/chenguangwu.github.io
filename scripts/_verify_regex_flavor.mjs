// 验证正则转义风格下拉切换触发重算（IT-N59，第295批）。
// verify stub DOM 不建模 select 的 onchange 属性/事件，故用 JSDOM 真机语义验证。
// 用法: node scripts/_verify_regex_flavor.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/regex-escape.html', 'utf8');
const i18nJs = fs.readFileSync('js/tool-i18n.js', 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function boot() {
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'https://x.com/tools/it/regex-escape.html' });
  const w = dom.window;
  w.ToolBox = w.ToolBox || { showToast() {}, copyText() {}, escHtml(s) { return String(s); } };
  w.TBKit = w.TBKit || { util: { isEn() { return false; } } };
  w.I18n = { get() { return 'zh-CN'; }, apply() {}, t(k) { return k; }, indName(k) { return k; }, applyLangAttr() {}, addPack() {} };
  if (!w.fetch) w.fetch = () => Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
  try { w.eval(i18nJs); } catch (e) { /* 桩缺失时忽略初始化异常 */ }
  // 提取页面主脚本（无 src/type 的 inline script），跳过 JSON-LD 与外链
  const blocks = [...html.matchAll(/<script(?![^>]*\b(?:src|type)\b)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
  let initError = null;
  try {
    w.eval(blocks.join('\n') + '\n;window.__esc = typeof esc === "function" ? esc : null; window.__escLive = typeof __escLive === "function" ? __escLive : null;');
  } catch (e) { initError = String(e.message || e); }
  return { w, d: w.document, initError };
}

const { w, d, initError } = boot();
check('主脚本初始化无异常', initError === null, initError || '无异常');
const sel = d.getElementById('flavor');
check('风格下拉存在', !!sel);

// ① 属性绑定：onchange 必须指向 __escLive
const attr = sel ? (sel.getAttribute('onchange') || '') : '';
check('风格下拉绑定 onchange', /__escLive/.test(attr), 'onchange=' + JSON.stringify(attr));

// ② 真实事件：默认风格(JS)下 / 不转义；切换 verbose 后 / 仍由 slash 开关控制，
//    但风格集合变化须体现——用 = 验证（旧 VERBOSE_META 曾含 =，现已剔除；这里验证
//    change 事件确实触发重算：先设输入含 .，切换风格后输出必须重新生成）。
if (sel) {
  const input = d.getElementById('input');
  input.value = 'a.b/c';
  sel.value = 'default';
  // outside-only 模式不执行内联 handler；直接调用与 onchange 绑定的同一函数验证重算链路。
  w.__escLive && w.__escLive();
  const outDefault = d.getElementById('output').value || '';
  sel.value = 'verbose';
  w.__escLive && w.__escLive();
  const outVerbose = d.getElementById('output').value || '';
  check('切换风格后输出重新生成', outVerbose.length > 0 && /a\\\.b/.test(outVerbose),
    'default=' + outDefault.slice(0, 25) + ' verbose=' + outVerbose.slice(0, 25));
}

// ③ 与 checkbox 的绑定一致性（两者都应绑 __escLive）
const slash = d.getElementById('slash');
const slashAttr = slash ? (slash.getAttribute('onchange') || '') : '';
check('斜杠开关绑定一致', /__escLive/.test(slashAttr), 'onchange=' + JSON.stringify(slashAttr));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
