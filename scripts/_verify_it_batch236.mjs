// 第236批探测 · IT-N285~N287（numeronym-generator 3 条）
//  N285 首尾取原始 token（含标点）→ 乱码
//  N286 无 7 字母阈值，短词也被缩写
//  N287 复制的是逐词对照不是展示结果；i18nText undefined
// 用法：node scripts/_verify_it_batch236.mjs [旧页目录]
import fs from 'fs';
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
      let cap = '';
      w.ToolBox = { showToast(m) { w.__toast = m; }, copyText(t) { cap = t; } };
      w.__getCap = () => cap;
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
      };
    }
  });
  const w = dom.window;
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, w, d: w.document, html };
}

const NM = makeDom(OLD_DIR ? OLD_DIR + '/numeronym-generator.html' : 'tools/it/numeronym-generator.html');
const raw = fs.readFileSync(OLD_DIR ? OLD_DIR + '/numeronym-generator.html' : 'tools/it/numeronym-generator.html', 'utf8');
const w = NM.w, d = NM.d;

function num(word) { try { return w.numeronym(word); } catch (e) { return 'THROW:' + e.message; } }

// ══════════════ N285 标点词 ══════════════
check('N285 internationalization, → i18n,', num('internationalization,') === 'i18n,', num('internationalization,'));
check('N285 (internationalization) → (i18n)', num('(internationalization)') === '(i18n)', num('(internationalization)'));
check('N285 internationalization. → i18n.', num('internationalization.') === 'i18n.', num('internationalization.'));

// ══════════════ N286 短词阈值 ══════════════
check('N286 the 不缩写（默认阈值≥7）', num('the') === 'the', num('the'));
check('N286 quick(5) 不缩写', num('quick') === 'quick', num('quick'));
check('N286 internationalization(18) 仍缩写', num('internationalization') === 'i18n', num('internationalization'));
// 真机 generate 段落
try {
  d.getElementById('input').value = 'the quick brown fox';
  w.generate();
  const big = d.getElementById('outBig').textContent;
  check('N286 段落短词原样保留', big === 'the quick brown fox', big);
} catch (e) { check('N286 段落短词原样保留', false, e.message); }

// ══════════════ N287 复制源与 toast ══════════════
check('N287 i18nText 已定义', typeof w.i18nText === 'function', typeof w.i18nText);
try {
  d.getElementById('input').value = 'internationalization';
  w.generate();
  const big = d.getElementById('outBig').textContent;
  w.copyOut();
  const cap = w.__getCap();
  check('N287 复制的是展示结果 i18n 而非对照表', cap === 'i18n' && big === 'i18n', 'cap=' + cap + ' big=' + big);
} catch (e) { check('N287 复制的是展示结果 i18n 而非对照表', false, e.message); }
// 空结果 toast 非 undefined
try {
  d.getElementById('input').value = '';
  w.generate();
  w.copyOut();
  check('N287 空结果 toast 有文案非 undefined', !!w.__toast && /undefined/.test(String(w.__toast)) === false, 'toast=' + w.__toast);
} catch (e) { check('N287 空结果 toast 有文案非 undefined', false, e.message); }

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
