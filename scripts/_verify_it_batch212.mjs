// 第212批 · IT-N554/N555/N556 unicode-lookup 检索/名称表/复制（JSDOM 真机 · 已修项补证据）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/unicode-lookup.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

let copied = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/unicode-lookup.html',
  beforeParse(w) {
    w.alert = () => {};
    Object.defineProperty(w.navigator, 'clipboard', {
      configurable: true,
      value: { writeText(t) { copied = String(t); return Promise.resolve(); } }
    });
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const search = d.getElementById('search');
const grid = d.getElementById('grid');

function query(q) {
  search.value = q;
  w.eval('search()');
  return grid.innerHTML;
}

// ── IT-N554 码点 / 名称 / 逐字符检索 ──
const byCp = query('U+2603');
check('N554 U+ 码点检索出 1 张卡', (byCp.match(/unicode-card/g) || []).length === 1, byCp.slice(0, 180));
check('N554 码点检索命中雪人', /☃/.test(byCp) && /SNOWMAN/i.test(byCp), byCp.slice(0, 180));
const by0x = query('0x1F600');
check('N554 0x 码点检索命中 emoji', /😀/.test(by0x) && (by0x.match(/unicode-card/g) || []).length === 1, by0x.slice(0, 180));
const byName = query('snowman');
check('N554 名称子串检索命中', /☃/.test(byName) && /SNOWMAN/i.test(byName), byName.slice(0, 180));
const byChars = query('A😀');
check('N554 逐字符检索正确处理代理对', (byChars.match(/unicode-card/g) || []).length === 2 && /😀/.test(byChars), byChars.slice(0, 200));
const badCp = query('U+110000');
check('N554 越界码点不产字符', !/unicode-card/.test(badCp), badCp.slice(0, 120));

// ── IT-N555 内置标准名称表 ──
const count = w.eval('Object.keys(UNICODE_NAMES).length');
check('N555 名称表规模 ≥ 1000', count >= 1000, 'count=' + count);
check('N555 U+2603 返回标准名', /SNOWMAN/i.test(w.eval('lookupName(0x2603)')), w.eval('lookupName(0x2603)'));
check('N555 CJK 表外码点按规则推导', /CJK UNIFIED IDEOGRAPH/.test(w.eval('lookupName(0x4E2D)')), w.eval('lookupName(0x4E2D)'));
check('N555 未收录码点如实标注', /名称未收录/.test(w.eval('lookupName(0x2B73F)')), w.eval('lookupName(0x2B73F)'));
w.eval('showDetail(0x2603)');
check('N555 详情面板展示真实名称', /SNOWMAN/i.test(d.getElementById('detail').innerHTML), d.getElementById('detail').innerHTML.slice(0, 160));

// ── IT-N556 特定字符的复制按钮 ──
const detailHtml = d.getElementById('detail').innerHTML;
check('N556 复制字符按钮走 data-code', /copyChar\(this\)/.test(detailHtml) && /data-code="9731"/.test(detailHtml), detailHtml.slice(-220));
copied = null;
const quoteBtn = d.createElement('button');
quoteBtn.setAttribute('data-code', '34');
w.copyChar(quoteBtn);
await new Promise(r => setTimeout(r, 0));
check('N556 复制引号字符本身而非 HTML 实体', copied === '"', JSON.stringify(copied));
copied = null;
const emojiBtn = d.createElement('button');
emojiBtn.setAttribute('data-code', '128512');
w.copyChar(emojiBtn);
await new Promise(r => setTimeout(r, 0));
check('N556 复制 emoji 代理对字符', copied === '😀', JSON.stringify(copied));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
