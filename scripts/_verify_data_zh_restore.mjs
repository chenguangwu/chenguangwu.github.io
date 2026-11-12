// 验证「构建期英文预渲染 + data-zh 中文原文」在中文态被完整还原。
// 背景：2026-11-12 老板实测中文下 Formula & Standard References 区域仍是英文。
// 根因：restoreAllDataZh() 只覆盖 p[data-zh]，公式引据区的 h3/th/td/span 未还原。
// 用法: node scripts/_verify_data_zh_restore.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const i18nJs = fs.readFileSync('js/tool-i18n.js', 'utf8');
// 代表性页面：覆盖 agriculture(公式引据) / it / 多个行业
const pages = [
  'agriculture/calc-38',
  'agriculture/crop-water-requirement',
  'agriculture/fertilizer-calculator',
  'it/barcode-itf',
];
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

for (const slug of pages) {
  const html = fs.readFileSync('tools/' + slug + '.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'outside-only', url: 'https://x.com/tools/' + slug + '.html',
  });
  const w = dom.window;
  // 提供最小 I18n 桩：默认中文（zh-CN），让 tool-i18n 走中文还原分支
  w.I18n = {
    get() { return 'zh-CN'; },
    apply() {},
    t(k) { return k; },
    indName(k) { return k; },
    applyLangAttr() {},
    addPack() {},
  };
  // tool-i18n 依赖 window.ToolBox / TBKit / fetch 等，给最小桩避免 init 抛错
  w.ToolBox = w.ToolBox || { showToast() {}, toggleToolTheme() {} };
  w.TBKit = w.TBKit || { util: { isEn() { return false; } } };
  if (!w.fetch) w.fetch = () => Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
  w.ToolBox = w.ToolBox || {};
  try { w.eval(i18nJs); } catch (e) { /* 部分页依赖缺失全局，忽略初始化异常 */ }
  // 直接取页面里定义的 restoreAllDataZh 并调用（它不在 window 上时从 applyToolBody 走）
  // tool-i18n.js 是 IIFE，restoreAllDataZh 非全局；通过 DOMContentLoaded 触发主流程。
  w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

  const d = w.document;
  // 统计：data-zh 含汉字、当前文本不含汉字的纯文本元素（应全部被还原为 0）
  const leftover = Array.from(d.querySelectorAll('[data-zh]')).filter(el => {
    if (el.children && el.children.length) return false;
    const zh = el.getAttribute('data-zh') || '';
    const cur = el.textContent || '';
    return /[\u4e00-\u9fff]/.test(zh) && !/[\u4e00-\u9fff]/.test(cur);
  });
  check(slug + ' 中文态 data-zh 全还原', leftover.length === 0,
    '未还原数=' + leftover.length + (leftover.length ? ' 样例=' + leftover.slice(0, 2).map(e => e.textContent.slice(0, 25)).join('|') : ''));

  const box = d.getElementById('constRefBox');
  if (box) {
    const h3 = box.querySelector('h3[data-zh]');
    check(slug + ' 公式引据标题中文', !!h3 && /[\u4e00-\u9fff]/.test(h3.textContent),
      h3 ? h3.textContent.slice(0, 30) : 'no h3');
    const ths = Array.from(box.querySelectorAll('th[data-zh]'));
    const badTh = ths.filter(e => !/[\u4e00-\u9fff]/.test(e.textContent));
    check(slug + ' 公式引据表头中文', ths.length > 0 && badTh.length === 0,
      '表头=' + ths.length + ' 未还原=' + badTh.length);
  }
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
