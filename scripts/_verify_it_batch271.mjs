// 第271批 JSDOM 验证：IT-N271 gitignore 预设全量赋值（不叠加旧勾选）
// 用法: node scripts/_verify_it_batch271.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/gitignore-generator.html` : 'tools/it/gitignore-generator.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

let presetList = null, afterCb = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/gi.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
      preset: { bar: (host, list, after) => { presetList = list; afterCb = after; } },
    };
    w.i18nText = (z) => z;
  },
});
const w = dom.window, d = w.document;
// 预设在 DOMContentLoaded 的 boot 中渲染，等一个事件循环让 stub 捕获 presetList
await new Promise(r => setTimeout(r, 50));
const IDS = ['top_py', 'top_node', 'top_go', 'top_rust', 'top_java', 'top_dotnet', 'top_c', 'top_ide'];
function checkedCount() { return IDS.filter(id => d.getElementById(id) && d.getElementById(id).checked).length; }
function checkedIds() { return IDS.filter(id => d.getElementById(id) && d.getElementById(id).checked); }
// 模拟 tool-kit setValue 的 '0'/'false' = 未勾选语义
function applyPreset(p) {
  for (const k in p.values) {
    const el = d.getElementById(k);
    if (!el) continue;
    const v = p.values[k];
    const off = v === false || v === 0 || v === '0' || v === 'false' || v === 'off' || v === '' || v == null;
    el.checked = !off;
  }
  if (typeof afterCb === 'function') afterCb();
}

check('N271 预设条已渲染（4 个预设）', !!presetList && presetList.length === 4, 'n=' + (presetList && presetList.length));
if (presetList) {
  // 每个预设 values 都含全部 8 个键
  let allFull = true, short = [];
  presetList.forEach((p, i) => {
    if (Object.keys(p.values).length !== 8 || !IDS.every(id => id in p.values)) { allFull = false; short.push(p.label + '(' + Object.keys(p.values).length + ')'); }
  });
  check('N271 每个预设显式列出全部 8 个勾选框', allFull, 'short=' + short.join(','));
  // 全 '0'/'1' 值（无 'py'/'node' 这类字符串误当 true）
  const badVals = [];
  presetList.forEach(p => IDS.forEach(id => { if (!['0', '1'].includes(String(p.values[id]))) badVals.push(p.label + '.' + id + '=' + p.values[id]); }));
  check('N271 所有值为 0/1（无裸字符串）', badVals.length === 0, 'bad=' + badVals.slice(0, 3).join(','));

  // 默认参数：只勾 Node
  const def = presetList[0];
  applyPreset(def);
  check('N271 默认参数只勾 Node（1 项）', checkedCount() === 1 && checkedIds()[0] === 'top_node', 'ids=' + checkedIds().join(','));

  // 切到 Python+Node：只勾两项（不叠加）
  applyPreset(presetList[1]);
  check('N271 Python+Node 只勾 2 项（不叠加旧勾选）', checkedCount() === 2 && checkedIds().includes('top_py') && checkedIds().includes('top_node'), 'ids=' + checkedIds().join(','));

  // 从多勾状态切到 C+IDE：应清空前面 6 项
  IDS.forEach(id => { const e = d.getElementById(id); if (e) e.checked = true; }); // 人为全勾
  applyPreset(presetList[3]);
  check('N271 从全勾选 C+IDE 只留 2 项（旧勾选被清）', checkedCount() === 2 && checkedIds().includes('top_c') && checkedIds().includes('top_ide'), 'ids=' + checkedIds().join(','));

  // 再切默认参数：从 C+IDE 切回只勾 Node
  applyPreset(def);
  check('N271 从 C+IDE 切回默认只勾 Node', checkedCount() === 1 && checkedIds()[0] === 'top_node', 'ids=' + checkedIds().join(','));
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
