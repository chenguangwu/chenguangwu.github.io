// 验证小节 h2[data-zh] 在中文态被还原（第291批）；公式型 h2 不得被误替换。
// 背景：fermentation-time 的「Yeast Conversion」为中文态残留英文；主 h2 由
// applyToolBody() 还原，但小节 h2 不在 ORIG.title 管辖，且 restoreAllDataZh()
// 原选择器未含 h2 ⇒ 永久钉死英文。
// 用法: node scripts/_verify_h2_data_zh.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const i18nJs = fs.readFileSync('js/tool-i18n.js', 'utf8');
const PAGES = [
  'baking/fermentation-time',      // 小节 h2「Yeast Conversion」残留（老板报的同类问题）
  'agriculture/calc-38',           // 主 h2 + 公式引据区，对照不被误伤
  'it/barcode-itf',                // 对照
  'statistics/percentile-rank',    // 公式型 h2，必须保留公式英文
];
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function load(slug, lang) {
  const html = fs.readFileSync('tools/' + slug + '.html', 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'https://x.com/tools/' + slug + '.html?lang=' + lang });
  const w = dom.window;
  w.I18n = {
    get() { return lang; }, apply() {}, t(k) { return k; },
    indName(k) { return k; }, applyLangAttr() {}, addPack() {},
  };
  w.ToolBox = w.ToolBox || { showToast() {}, toggleToolTheme() {} };
  w.TBKit = w.TBKit || { util: { isEn() { return lang === 'en-US'; } } };
  if (!w.fetch) w.fetch = () => Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
  try { w.eval(i18nJs); } catch (e) { /* 桩缺失全局时忽略初始化异常 */ }
  w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
  return w;
}

for (const slug of PAGES) {
  const w = load(slug, 'zh-CN');
  const d = w.document;
  // 小节 h2[data-zh] 含中文锚、当前英文、非公式、无子元素 ⇒ 必须被还原
  const bad = Array.from(d.querySelectorAll('h2[data-zh]')).filter(el => {
    const zh = el.getAttribute('data-zh') || '';
    const cur = el.textContent || '';
    if (!/[\u4e00-\u9fff]/.test(zh) || /[\u4e00-\u9fff]/.test(cur)) return false;
    if (el.children && el.children.length) return false;
    // isFormula 口径：公式符号不还原
    return !/[∑∫∂√≈≠≥≤×÷²³⁴⁵πΔΩμλσφθ=]/.test(cur);
  });
  check(slug + ' 中文态小节 h2 全还原', bad.length === 0,
    '未还原=' + bad.length + (bad.length ? ' ' + bad.slice(0, 2).map(e => e.textContent.trim().slice(0, 30)).join('|') : ''));

  // 语言往返：切英文再切回中文，h2 仍为中文
  const w2 = load(slug, 'en-US');
  w2.I18n.get = () => 'zh-CN';
  w2.TBKit.util.isEn = () => false;
  w2.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
  const bad2 = Array.from(w2.document.querySelectorAll('h2[data-zh]')).filter(el => {
    const zh = el.getAttribute('data-zh') || '';
    const cur = el.textContent || '';
    return /[\u4e00-\u9fff]/.test(zh) && !/[\u4e00-\u9fff]/.test(cur) && !(el.children && el.children.length)
      && !/[∑∫∂√≈≠≥≤×÷²³⁴⁵πΔΩμλσφθ=]/.test(cur);
  });
  check(slug + ' 语言往返后 h2 仍中文', bad2.length === 0, '未还原=' + bad2.length);
}

// 公式型 h2 专项：percentile-rank 的公式标题必须原样保留（不被中文锚误替换）
const pr = load('statistics/percentile-rank', 'zh-CN');
const formulaH2 = Array.from(pr.document.querySelectorAll('h2')).find(e => /PR\s*=/.test(e.textContent || ''));
check('公式型 h2 保留英文公式', !!formulaH2 && /PR\s*=/.test(formulaH2.textContent),
  formulaH2 ? formulaH2.textContent.trim().slice(0, 45) : 'no formula h2');

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
