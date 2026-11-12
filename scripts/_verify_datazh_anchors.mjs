// 验证高置信通用英文表头已补 data-zh 中文锚点（第290批），防 build 还原/漏改。
// 用法: node scripts/_verify_datazh_anchors.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const i18nJs = fs.readFileSync('js/tool-i18n.js', 'utf8');

// 高置信通用词 → 中文（与 scripts/_zh_datazh_dict.py 的 TERMS 子集保持一致）
const TERMS = {
  'Value': '数值', 'Item': '项目', 'Category': '分类', 'Score': '得分',
  'Description': '说明', 'Type': '类型', 'Unit': '单位', 'Note': '备注',
  'Field': '字段', 'Name': '名称', 'Status': '状态', 'Grade': '等级',
  'Parameter': '参数', 'Option': '选项', 'Date': '日期', 'Result': '结果',
  'Symbol': '符号', 'Level': '等级', 'Time': '时间', 'Metric': '指标',
  'Body Part': '身体部位', 'Instruction': '说明', 'Level Name': '等级名称',
  'Food': '食物', 'Step': '步骤', 'Duration(s)': '时长（秒）',
};
// 抽样代表页（覆盖多分类），这些页在批处理中补过锚点
const PAGES = [
  'health/vo2-max-calculator', 'health/stretch-generator', 'health/dysphagia-food-guide',
  'it/barcode-itf', 'statistics/iqr', 'edu/countdown-5', 'music/ear-trainer',
];
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

for (const slug of PAGES) {
  const raw = fs.readFileSync('tools/' + slug + '.html', 'utf8');
  // 与注入脚本口径一致：script/style 块内的 innerHTML 模板本身有双语分支，
  // 不是 data-zh 锚点作用域（强行加引号会破坏 JS 语法），验证时先屏蔽。
  const html = raw.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, '');
  // 找无 data-zh 的 <td/th>英文表头，且该英文在词典中 ⇒ 漏补
  let missing = [];
  const re = /<(td|th)\b([^>]*)>([^<]{1,80})<\/\1>/gi;
  let m;
  while ((m = re.exec(html))) {
    const attrs = m[2], txt = m[3].trim();
    if (attrs.includes('data-zh')) continue;
    if (Object.prototype.hasOwnProperty.call(TERMS, txt)) {
      missing.push(txt);
    }
  }
  check(slug + ' 通用表头均已补锚', missing.length === 0,
    '漏补=' + missing.length + (missing.length ? ' ' + missing.slice(0, 3).join('|') : ''));

  // 所有新锚点：data-zh 值须为中文，英文可见文本保留
  const anchorRe = /<(td|th)\b([^>]*data-zh="([^"]+)"[^>]*)>([^<]{1,80})<\/\1>/gi;
  let a, badAnchor = 0, anchorCount = 0;
  while ((a = anchorRe.exec(html))) {
    const zh = a[3], txt = a[4].trim();
    if (!Object.prototype.hasOwnProperty.call(TERMS, txt)) continue;
    anchorCount++;
    if (zh !== TERMS[txt]) badAnchor++;
  }
  check(slug + ' 锚点中文值正确', badAnchor === 0,
    '锚点数=' + anchorCount + ' 错误=' + badAnchor);

  // 真机（JSDOM）：中文态下这些锚点必须被 tool-i18n 还原成中文，不允许仍显示英文。
  const dom = new JSDOM(raw, {
    runScripts: 'outside-only', url: 'https://x.com/tools/' + slug + '.html',
  });
  const w = dom.window;
  w.I18n = {
    get() { return 'zh-CN'; }, apply() {}, t(k) { return k; },
    indName(k) { return k; }, applyLangAttr() {}, addPack() {},
  };
  w.ToolBox = w.ToolBox || { showToast() {}, toggleToolTheme() {} };
  w.TBKit = w.TBKit || { util: { isEn() { return false; } } };
  if (!w.fetch) w.fetch = () => Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
  try { w.eval(i18nJs); } catch (e) { /* 桩缺失全局时忽略初始化异常 */ }
  w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
  const notRestored = [];
  for (const el of w.document.querySelectorAll('td[data-zh], th[data-zh]')) {
    const txt = (el.textContent || '').trim();
    const zh = el.getAttribute('data-zh') || '';
    if (!Object.prototype.hasOwnProperty.call(TERMS, txt)) continue;
    if (!/[\u4e00-\u9fff]/.test(zh)) continue;
    if (!/[\u4e00-\u9fff]/.test(el.textContent || '')) notRestored.push(txt);
  }
  check(slug + ' 真机中文态锚点还原', notRestored.length === 0,
    '未还原=' + notRestored.length + (notRestored.length ? ' ' + notRestored.slice(0, 3).join('|') : ''));
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
