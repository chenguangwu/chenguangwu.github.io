// 第199批 · IT-N249/N250/N251 chinese-name-generator 字数/去重/收藏toast（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/chinese-name-generator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

const toasts = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/chinese-name-generator.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = (k, fb) => (k ? (k === 'toast.fav_removed' ? '已取消收藏' : (fb != null ? fb : k)) : '');
    w.ToolBox = { showToast(msg) { toasts.push(String(msg)); }, toggleToolTheme() {}, copyText() {} };
    // localStorage stub
    const store = {};
    Object.defineProperty(w, 'localStorage', { configurable: true, value: {
      getItem(k) { return store[k] != null ? store[k] : null; },
      setItem(k, v) { store[k] = String(v); },
      removeItem(k) { delete store[k]; }
    }});
  }
});
const w = dom.window, d = w.document;
try { d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true })); } catch (e) {}

// ── IT-N249 双字词条已拆成单字 ──
const badM = w.maleChars.filter(c => Array.from(c).length !== 1);
check('maleChars 无双字条目', badM.length === 0, JSON.stringify(badM));

// ── IT-N249 复姓避让 + 字数精确 ──
// 反复调用，确认无论姓/字池组合，fullName 字数都等于目标
function genBatch(gender, len, style, n) {
  const bad = [];
  for (let i = 0; i < n; i++) {
    const it = w.generateOneName(gender, String(len), style);
    if (Array.from(it.name).length !== len) bad.push(it.name + '(len' + Array.from(it.name).length + ')');
  }
  return bad;
}
let bad249 = [];
for (const g of ['male', 'female', 'random']) {
  for (const len of [2, 3]) {
    for (const st of ['modern', 'classic', 'literary', 'random']) {
      bad249 = bad249.concat(genBatch(g, len, st, 40).map(x => g + '/' + len + '/' + st + ':' + x));
    }
  }
}
check('全组合 generated name 字数精确 (=nameLen)', bad249.length === 0, bad249.slice(0, 5).join(' | '));

// 复姓不可用于 2 字名：直接检验 generateOneName 在 2 字名时不会返回复姓姓
let compositeIn2 = [];
for (let i = 0; i < 200; i++) {
  const it = w.generateOneName('male', '2', 'modern');
  if (Array.from(it.surname).length >= 2) compositeIn2.push(it.surname + it.given);
}
check('2 字名不出现复姓', compositeIn2.length === 0, compositeIn2.slice(0, 5).join('/'));

// ── IT-N250 getCharPool 出口去重 ──
for (const g of ['male', 'female', 'random']) {
  for (const st of ['modern', 'classic', 'literary']) {
    const pool = w.getCharPool(g, st);
    const set = new Set(pool);
    check('getCharPool(' + g + ',' + st + ') 无重复', set.size === pool.length, 'n=' + pool.length + ' uniq=' + set.size);
  }
}

// 关键重复字不再被放大："薇/素/毅" 在现代池各只出现一次
const fPool = w.getCharPool('female', 'modern');
const mPool = w.getCharPool('male', 'modern');
check('female 现代池 薇/素 各1次', fPool.filter(c => c === '薇').length === 1 && fPool.filter(c => c === '素').length === 1);
check('male 现代池 毅 1次', mPool.filter(c => c === '毅').length === 1);

// ── IT-N251 取消收藏 toast 有明确文案 ──
w.favorites = [{ name: '测试名', gender: 'male', style: 'modern', time: Date.now() }];
toasts.length = 0;
w.toggleFav('测试名', 'male', 'modern');
check('取消收藏 toast 非 undefined/非空', toasts.length >= 1 && toasts[0] === '已取消收藏', JSON.stringify(toasts));
check('取消收藏从收藏表移除', w.favorites.length === 0, 'n=' + w.favorites.length);

// 收藏路径仍正常
toasts.length = 0;
w.toggleFav('新名字', 'female', 'classic');
check('收藏 toast 正常', toasts.some(t => t.indexOf('已收藏') >= 0), JSON.stringify(toasts));
check('收藏写入收藏表', w.favorites.length === 1 && w.favorites[0].name === '新名字');

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
