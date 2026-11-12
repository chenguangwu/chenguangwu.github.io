// 验证 TypeScript 编译器页两处修复（第293批，IT 清单）：
//   ① 缺 ts 全局时 showDiagnostics 不抛错、失败提示写进界面；
//   ② 输入变化立即清空 jsOutput，防抖窗口内复制/下载不取旧输出。
// 用法: node scripts/_verify_ts_compiler.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/typescript-compiler.html', 'utf8');
// 取主脚本块（第526行起的 <script>，无 type/src 属性），跳过 text/plain 示例与外链。
const blocks = [...html.matchAll(/<script(?![^>]*\b(?:src|type)\b)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
const mainJs = blocks.join('\n');
if (!mainJs) { console.log('FAIL 无法提取主脚本块'); process.exit(1); }

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function boot() {
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'https://x.com/tools/it/typescript-compiler.html' });
  const w = dom.window;
  // 最小桩：ToolBox / I18n / TBKit / fetch。故意不定义 ts（缺库场景）。
  w.ToolBox = {
    escHtml(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); },
    showToast() {}, copyText() {}, downloadText() {}, i18nText(k) { return k || ''; },
  };
  w.I18n = { get() { return 'zh-CN'; }, apply() {}, t(k) { return k; }, indName(k) { return k; }, applyLangAttr() {}, addPack() {} };
  w.TBKit = { util: { isEn() { return false; } } };
  if (!w.fetch) w.fetch = () => Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
  // 只执行主脚本块，不执行 text/plain 示例块（那是 TS 源码，不是 JS）。
  // const/let/function 在 eval 词法作用域内，不自动挂 window：末尾显式导出引用供断言调用。
  let initError = null;
  try {
    w.eval(mainJs + '\n;window.__showDiagnostics = typeof showDiagnostics === "function" ? showDiagnostics : null;');
    // JSDOM 构造后 readyState 可能仍为 loading ⇒ 派发 DOMContentLoaded 触发页面 init 绑定事件。
    w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
  } catch (e) { initError = String(e.message || e); }
  return { w, d: w.document, initError };
}

// ① 缺 ts：showDiagnostics 直接被加载失败超时分支调用，必须无异常且写入提示。
{
  const { w, d, initError } = boot();
  check('主脚本缺 ts 时不抛错', initError === null, initError || '无异常');
  let thrown = null;
  try {
    w.__showDiagnostics([{ category: 1, code: 0, messageText: 'TypeScript 编译器加载失败，请检查网络后刷新页面。', start: 0 }], '');
  } catch (e) { thrown = String(e.message || e); }
  check('缺 ts 时 showDiagnostics 不抛错', thrown === null, thrown || '无异常');
  const body = d.getElementById('diagBody').textContent || '';
  check('失败提示写入诊断面板', body.includes('加载失败'), body.slice(0, 45));
  const count = d.getElementById('diagCount').textContent;
  check('失败计数非 0', count === '1', 'count=' + count);
}

// ② 链式 messageText（DiagnosticMessageChain）在无 ts 时也能展平。
{
  const { w, d, initError } = boot();
  let thrown = null;
  try {
    w.__showDiagnostics([{ category: 1, code: 0,
      messageText: { messageText: '外层错误', next: { messageText: '内层细节', next: undefined } }, start: 0 }], '');
  } catch (e) { thrown = String(e.message || e); }
  check('链式诊断消息展平不抛错', thrown === null, thrown || '无异常');
  const body = d.getElementById('diagBody').textContent || '';
  check('链式消息两层都可见', body.includes('外层错误') && body.includes('内层细节'), body.slice(0, 50));
}

// ③ 输入变化立即清空输出：派发 input 事件后 jsOutput 必须为空（防抖未触发）。
{
  const { w, d, initError } = boot();
  const out = d.getElementById('jsOutput');
  const ta = d.getElementById('tsInput');
  out.value = 'OLD-JS';
  ta.value = 'const x: number = 1;';
  let thrown = null;
  try { ta.dispatchEvent(new w.Event('input')); } catch (e) { thrown = String(e.message || e); }
  check('input 事件不抛错', thrown === null, thrown || '无异常');
  check('输入变化立即清空旧输出', out.value === '', 'value=' + JSON.stringify(out.value.slice(0, 30)));
  const meta = d.getElementById('statSize').textContent;
  check('统计同步归零', meta === '0', 'statSize=' + meta);
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
