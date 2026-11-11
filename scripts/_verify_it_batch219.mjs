// 第219批 · IT-N178~N180 http-cookies（JSDOM 真机 + 静态数据检查）
//  N178 英文简介不再宣称解析/构建（已修证据）
//  N179 Expires 示例星期与日期自洽且未过期（全站 5 页 11 处同类修正）
//  N180 Max-Age ≤0 删除语义 + 明细表表头双语
import fs from 'fs';
import { JSDOM } from 'jsdom';

const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

const PAGE = 'tools/it/http-cookies.html';
const html = fs.readFileSync(PAGE, 'utf8');
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/http-cookies.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
const $ = id => d.getElementById(id);

// ══════════════ N178 英文简介口径 ══════════════
const intro = html.match(/<p data-zh="([^"]*)">([^<]*)<\/p>/);
check('N178 中文简介是「属性与 JS 操作方法」类参考口径', intro && /属性和 JS 操作方法|属性（SameSite/.test(intro[1]), intro && intro[1]);
check('N178 英文简介不再宣称 Parse and build', !/Parse and build/i.test(html), /Parse and build/i.test(html) ? 'FOUND BAD' : 'clean');
check('N178 英文简介为 reference 口径', /searchable quick reference|Quick Reference/i.test(intro ? intro[2] : ''), intro && intro[2]);
check('N178 页面确实没有解析/构建输入框（简介与能力一致）',
  !/id="(cookieParser|setCookieBuilder|parseInput)"/.test(html) && !/function\s+parseCookieHeader/.test(html), 'no parser controls');

// ══════════════ N179 日期：星期自洽 + 未过期 ══════════════
// 全站同类：5 个 HTTP 页都用了 Wed, 21 Oct 2025（周二是 Tue、且已过期）
const PAGES = [
  'tools/it/http-cookies.html', 'tools/it/http-headers.html',
  'tools/it/http-response-headers.html', 'tools/it/http-cache.html'
];
const BAD = /Wed,\s*21 Oct 2025/;
for (const p of PAGES) {
  const s = fs.readFileSync(p, 'utf8');
  check('N179 ' + p.split('/').pop() + ' 不再有错的 Wed, 21 Oct 2025', !BAD.test(s), (s.match(BAD) || []).length + ' 处');
}
// 所有剩余 HTTP-date 示例的星期必须与 JS 实算一致，且不得是过去时间
const now = Date.now();
const dateExamples = new Set();
for (const p of PAGES) {
  const s = fs.readFileSync(p, 'utf8');
  const re = /(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})\s+(\d{2}:\d{2}:\d{2})\s+GMT/g;
  let m;
  while ((m = re.exec(s))) dateExamples.add(m[0]);
}
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
check('N179 至少收集到 1 个 HTTP-date 示例', dateExamples.size > 0, 'n=' + dateExamples.size);
let weekdayOk = true;
for (const t of dateExamples) {
  const dt = new Date(t);
  // 1970-01-01（JS 删 Cookie 标准写法）、2015/2026（条件请求/RFC 示例）星期都正确，
  // 属刻意的历史时间戳，不要求「未过期」；只判星期自洽 + 2025 错误串清零。
  if (DAYS[dt.getUTCDay()] !== t.slice(0, 3)) { weekdayOk = false; console.log('  WEEKDAY BAD:', t, '=>', dt.toUTCString()); }
}
check('N179 所有 HTTP-date 星期与 JS 实算一致（含保留的 1970/2015/2026 示例）', weekdayOk,
  [...dateExamples].join(' / ').slice(0, 180));
const fixed = 'Thu, 21 Oct 2027 07:28:00 GMT';
check('N179 替换后的示例星期正确且未过期',
  /Thu,\s*21 Oct 2027 07:28:00 GMT/.test(html) && DAYS[new Date(fixed).getUTCDay()] === 'Thu' && new Date(fixed).getTime() > now,
  'fixed=' + fixed + ' now=' + new Date(now).toISOString().slice(0, 10));
check('N179 4 页均无已过期的 2025 错误示例', PAGES.every(p => !/21 Oct 2025/.test(fs.readFileSync(p, 'utf8'))), 'checked 4 pages');

// ══════════════ N180 Max-Age 语义 + 表头双语 ══════════════
const maxAge = html.match(/"cmd":\s*"Max-Age"[\s\S]{0,320}?"desc":\s*"([^"]+)"/);
check('N180 Max-Age desc 含「0 或负数→立即删除」语义',
  !!maxAge && /0|负数/.test(maxAge[1]) && /删除/.test(maxAge[1]), maxAge && maxAge[1]);
// en JSON 对应英译也须含删除语义
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/http-cookies.json', 'utf8'));
const enHit = Object.entries(en.map || {}).find(([k]) => /存活秒数/.test(k));
check('N180 en JSON 有对应中文键', !!enHit, enHit && enHit[0].slice(0, 60));
check('N180 en JSON 英译含 delete 语义', !!enHit && /delet/i.test(String(enHit[1])), enHit && String(enHit[1]).slice(0, 100));

// 表头：__ckTable 在 IIFE 内，通过 DOMContentLoaded / toolbox:langchange 事件触发
function renderTable(mode) {
  enMode = mode;
  d.dispatchEvent(new w.Event('toolbox:langchange', { bubbles: true }));
  return [$('ckTh0'), $('ckTh1'), $('ckTh2'), $('ckTh3')].map(e => e ? e.textContent : '');
}
const zhHead = renderTable(false);
check('N180 中文态表头 th1 为「属性」', zhHead[1] === '属性', JSON.stringify(zhHead));
check('N180 中文态表头其余列也是中文', zhHead[2] === '分类' && zhHead[3] === '说明', JSON.stringify(zhHead));
const enHead = renderTable(true);
check('N180 英文态表头 th1 为 Attribute', enHead[1] === 'Attribute', JSON.stringify(enHead));
check('N180 英文态表头其余列为 Category/Description', enHead[2] === 'Category' && enHead[3] === 'Description', JSON.stringify(enHead));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAIL ITEMS: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exitCode = 1;
}
