// 第227批 · IT-N212~N216（nanoid-generator 3 条 + markdown-table-generator 2 条，JSDOM 真机）
//  N212 自定义字母表 >256 时后半段不可达（真修：32 位拒绝采样）
//  N213 字母表按 UTF-16 码元，emoji 拆孤立代理（真修：Array.from 码点）
//  N214 历史/图表读首个 .result-box 静态块（真修：读 #results 的 code）
//  N215 Markdown 单元格反斜杠未转义破坏列（真修：先转义 \ 再转义 |）
//  N216 表头/首行 oninput 回写占位，光标跳末尾无法删列（真修：不写回）
// 用法：node scripts/_verify_it_batch227.mjs [旧页目录；提供时对两页做差分]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 150) : '')); }

function makeDom(htmlPath, url) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  let history = [], tableData = null, exports = [];
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: url || 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {} };
      w.i18nText = (k, f) => (k == null || k === '') ? (f != null ? f : '') : (f || String(k));
      // 真 crypto：JSDOM 的 window.crypto.getRandomValues 可用
      w.TBKit = {
        util: { isEn: () => false, exportTable(sel, name) { exports.push({ sel, name, rows: tableData && tableData.rows }); }, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table(sel, cfg) { tableData = cfg; } }, preset: { bar() {} },
        history: { list() { return history.slice(); }, last() { return history.length ? history[history.length - 1] : null; },
          record(r) { history.push(r); }, mount() {}, clear() { history = []; } }
      };
    }
  });
  return { dom, w: dom.window, d: dom.window.document, html, history, getTable: () => tableData, exports };
}

const NANOID = OLD_DIR ? OLD_DIR + '/nanoid.orig.html' : 'tools/it/nanoid-generator.html';
const MDTABLE = OLD_DIR ? OLD_DIR + '/mdtable.orig.html' : 'tools/it/markdown-table-generator.html';

// ══════════════ nanoid ══════════════
const N = makeDom(NANOID), nw = N.w, nd = N.d, $N = id => nd.getElementById(id);
// 选自定义字母表
function useCustom(alpha) {
  const radio = nd.querySelector('input[name=alphabet][value=custom]');
  if (radio) radio.checked = true;
  $N('customAlpha').value = alpha;
}

// N212 大字母表（300 个不同码点）全可达：length 上限 100，多次生成累积采样
const alpha300 = Array.from({ length: 300 }, (_, i) => String.fromCodePoint(0x4E00 + i)).join('');
useCustom(alpha300);
$N('length').value = '100'; $N('count').value = '10';
let gen300ok = true, seen300 = new Set(), allCharsOk = true;
const set300 = new Set(Array.from(alpha300));
try {
  for (let round = 0; round < 60; round++) {
    nw.gen();
    const codes = $N('results').querySelectorAll('code');
    for (const code of codes) {
      const id = code.textContent || '';
      Array.from(id).forEach(c => { seen300.add(c); if (!set300.has(c)) allCharsOk = false; });
    }
  }
} catch (e) { gen300ok = false; }
check('N212 300 字母表采样覆盖 >256 个不同码点（后段可达）', gen300ok && seen300.size > 256, 'seen=' + seen300.size);
check('N212 生成串全由自定义字母表字符组成（无越界代理）', allCharsOk, 'allInAlphabet=' + allCharsOk);

// N213 emoji 字母表：一个 emoji 一个码点，不产生孤立代理
useCustom('😀😁😃😄');
$N('length').value = '100'; $N('count').value = '1';
let emojiOk = true, emojiStr = '';
try {
  nw.gen();
  const code = $N('results').querySelector('code'); emojiStr = code ? code.textContent : '';
  const allowed = new Set(['😀', '😁', '😃', '😄']);
  emojiOk = Array.from(emojiStr).every(c => allowed.has(c)) && Array.from(emojiStr).length === 100;
} catch (e) { emojiOk = false; }
check('N213 emoji 字母表按码点生成，无孤立代理项', emojiOk, 'codepoints=' + Array.from(emojiStr).length);
check('N213 emoji 字母表长度校验按码点（4 个 emoji 通过 ≥2 校验）', (() => {
  useCustom('😀😁'); $N('length').value = '8'; $N('count').value = '1';
  nw.gen();
  return $N('results').querySelector('code') !== null;
})(), '');
check('N213 单 emoji 字母表（1 码点但 2 码元）应被拒绝', (() => {
  useCustom('😀'); $N('length').value = '8'; $N('count').value = '1';
  let err = '';
  try { nw.gen(); } catch (e) { err = e.message; }
  const shown = ($N('results').textContent || '') + ($N('results').innerHTML || '');
  return /至少/.test(err) || /至少/.test(shown);
})(), ($N('results').textContent || '').slice(0, 80));

// N214 历史 ResText 读 #results 的 code，不是静态说明块
N.history.length = 0;
useCustom('0123456789abcdef');
$N('length').value = '8'; $N('count').value = '2';
nw.gen();
$N('length').value = '24'; $N('count').value = '2';
nw.gen();
try { nw.__nanoid_generator_last = 0; nw.__nanoid_generatorExtras(); } catch (e) {}
const hjson = JSON.stringify(N.history);
check('N214 历史 res 含实际 ID（8 位与 24 位），非静态说明', /[A-Za-z0-9_-]{8}/.test(hjson) && /[A-Za-z0-9_-]{24}/.test(hjson) && !/默认长度 21 字符/.test(hjson), hjson.slice(0, 240));
check('N214 ResText 源码不再 querySelector(.result-box)', (() => {
  const m = N.html.match(/function __nanoid_generatorResText\(\)\{[\s\S]*?\n\}/);
  return !!m && !/querySelector\(['"]\.result-box/.test(m[0]) && /getElementById\(['"]results/.test(m[0]);
})(), '');

// ══════════════ markdown-table ══════════════
const M = makeDom(MDTABLE), mw = M.w, md = M.d, $M = id => md.getElementById(id);
// 暴露页面 script 内函数（在 script 块作用域，用 eval 可能拿不到；用 __pageEval 风格）
const pageFns = {};
const iframeEval = code => {
  try { return mw.eval(code); } catch (e) { return undefined; }
};

// N215 反斜杠先转义
$M('rows').value = '1'; $M('cols').value = '1';
$M('headerLine').value = 'a\\|b';
$M('bodyLine').value = 'a\\|b';
mw.renderPreview ? mw.renderPreview() : iframeEval('renderPreview()');
let out = $M('output').value || '';
check('N215 a\\|b 源文本产出 a\\\\\\|b（先转义反斜杠）', /a\\\\\\\|b/.test(out) || out.includes('a\\\\\\|b'), JSON.stringify(out.slice(0, 120)));
check('N215 单元格仍是 1 列（竖线未重新成为分隔符）', (() => {
  const line = out.split('\n')[0];
  const sep = out.split('\n')[1];
  // 1 列时表头行形态固定：| <cell> |，分隔行只有一段 :---
  return /^\| .+ \|$/.test(line) && /^\| :-+ \|$/.test(sep);
})(), JSON.stringify(out.split('\n').slice(0, 2)));

// N216 编辑期不写回输入
$M('cols').value = '3';
$M('headerLine').value = 'a';
$M('bodyLine').value = 'x';
$mwSync();
function $mwSync() { mw.syncColumns ? mw.syncColumns() : iframeEval('syncColumns()'); }
check('N216 syncColumns 不写回表头（输入保持 a）', $M('headerLine').value === 'a', $M('headerLine').value);
check('N216 syncColumns 不写回首行（输入保持 x）', $M('bodyLine').value === 'x', $M('bodyLine').value);
check('N216 缺列仍由预览占位 C2/C3 补齐', /C2/.test($M('output').value) && /C3/.test($M('output').value), $M('output').value.slice(0, 120));
check('N216 syncColumns 源码不写 input.value', (() => {
  const m = M.html.match(/function syncColumns\(\)\s*\{[\s\S]*?\n\s*\}/);
  return !!m && !/\.value\s*=/.test(m[0]);
})(), '');

// 状态链：连续编辑 → 预览跟随
$M('headerLine').value = '甲,乙'; $M('bodyLine').value = '1,2';
$mwSync();
check('状态链 连续编辑后预览反映最新输入', /甲/.test($M('output').value) && /乙/.test($M('output').value), $M('output').value.slice(0, 100));

// ══════════════ 公式 / i18n 三源（仅修好版）══════════════
if (!OLD_DIR) {
  const enN = JSON.parse(fs.readFileSync('i18n/tools/en/it/nanoid-generator.json', 'utf8'));
  const enM = JSON.parse(fs.readFileSync('i18n/tools/en/it/markdown-table-generator.json', 'utf8'));
  const fN = N.html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
  const fM = M.html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
  check('公式 nanoid 说明含码点/拒绝采样新口径且 en 同键', !!fN && /Unicode 码点/.test(fN[1]) && /拒绝采样/.test(fN[1]) && !!enN.map[fN[1]] && /rejection sampling/.test(enN.map[fN[1]]), fN ? fN[1].slice(-60) : 'missing');
  check('公式 markdown 说明含反斜杠转义顺序且 en 同键', !!fM && /反斜杠转义为双反斜杠/.test(fM[1]) && !!enM.map[fM[1]] && /backslashes are doubled first/.test(enM.map[fM[1]]), fM ? fM[1].slice(-60) : 'missing');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
