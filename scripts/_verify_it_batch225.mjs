// 第225批 · IT-N202~N206（plist-parser 3 条 + char-encoder 2 条，JSDOM 真机）
//  N202 plist real/date/data 往返保型（真修）
//  N203 plist 超安全整数精度保留（真修）
//  N204 plist 控制字符未转义产出非法 XML（真修）
//  N205 char-encoder ASCII 行按 UTF-8 字节数误判（真修）
//  N206 char-encoder 清空残留字节视图（真修）
// 顺带修：plist-parser 重复注入同名函数让成功提示变红
// 用法：node scripts/_verify_it_batch225.mjs [旧页目录；提供时对两页做差分兼容]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  let tableData = null, history = [];
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table(sel, cfg) { tableData = cfg; } },
        preset: { bar() {} },
        history: { list() { return history.slice(); }, last() { return history.length ? history[0].d : null; },
          record(r) { history.unshift({ t: Date.now(), d: r }); }, mount() {}, clear() { history = []; } }
      };
    }
  });
  return { dom, w: dom.window, d: dom.window.document, html, getTable: () => tableData, getHist: () => history };
}

const PLIST = OLD_DIR ? OLD_DIR + '/plist.orig.html' : 'tools/it/plist-parser.html';
const CHAR = OLD_DIR ? OLD_DIR + '/char.orig.html' : 'tools/it/char-encoder.html';

// ══════════════ plist-parser ══════════════
const P = makeDom(PLIST);
const pw = P.w, pd = P.d, $ = id => pd.getElementById(id);
function pparse(xml) { $('input').value = xml; pw.plistToJson(); return { out: $('output').textContent, err: $('err').textContent, cls: $('err').className }; }
function pgen(json) { $('input').value = json; pw.jsonToPlist(); return { out: $('output').textContent, err: $('err').textContent, cls: $('err').className }; }
const head = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n';
const wrap = body => head + body + '\n</plist>';

// N202 real / date / data 保型
const rReal = pparse(wrap('<real>1.0</real>'));
check('N202 real 1.0 解析为类型标记对象而非整数 1', /"__plistType": "real"/.test(rReal.out) && /"value": "1\.0"/.test(rReal.out), rReal.out);
const rDate = pparse(wrap('<date>2020-01-01T00:00:00Z</date>'));
check('N202 date 解析保留 date 标记与原文', /"__plistType": "date"/.test(rDate.out) && /2020-01-01T00:00:00Z/.test(rDate.out), rDate.out);
const rData = pparse(wrap('<data>AAECAw==</data>'));
check('N202 data 解析保留 data 标记与 base64', /"__plistType": "data"/.test(rData.out) && /AAECAw==/.test(rData.out), rData.out);
// 往返：JSON（带标记）→ plist 还原原生标签
const rtReal = pgen(rReal.out);
check('N202 real 往返仍为 <real>1.0</real> 不是 <integer>', /<real>1\.0<\/real>/.test(rtReal.out) && !/<integer>1<\/integer>/.test(rtReal.out), rtReal.out);
const rtDate = pgen(rDate.out);
check('N202 date 往返仍为 <date> 不是 <string>', /<date>2020-01-01T00:00:00Z<\/date>/.test(rtDate.out) && !/<string>/.test(rtDate.out), rtDate.out);
const rtData = pgen(rData.out);
check('N202 data 往返仍为 <data> 不是 <string>', /<data>AAECAw==<\/data>/.test(rtData.out) && !/<string>/.test(rtData.out), rtData.out);
// 普通 integer 不受影响
check('N202 普通 integer 30 仍是数字 30', /"age": 30|\b30\b/.test(pparse(wrap('<integer>30</integer>')).out), pparse(wrap('<integer>30</integer>')).out);

// N203 大整数
const bigRaw = '9007199254740993';
const rBig = pparse(wrap('<integer>' + bigRaw + '</integer>'));
check('N203 超安全整数保留原始十进制串不就近改写',
  /9007199254740993/.test(rBig.out) && !/9007199254740992/.test(rBig.out), rBig.out);
const rtBig = pgen(rBig.out);
check('N203 大整数往返写回 <integer>9007199254740993</integer>',
  /<integer>9007199254740993<\/integer>/.test(rtBig.out), rtBig.out);
check('N203 安全范围内整数仍按数字解析（根节点纯数字）', pparse(wrap('<integer>9007199254740991</integer>')).out.trim() === '9007199254740991',
  pparse(wrap('<integer>9007199254740991</integer>')).out);

// N204 控制字符
const ctrl = JSON.stringify({ a: 'x\u0001y' });
const rCtrl = pgen(ctrl);
check('N204 输出不含裸 U+0001 控制字符', !/\u0001/.test(rCtrl.out) && /xy|&\#/.test(rCtrl.out), JSON.stringify(rCtrl.out));
check('N204 状态栏提示剔除 1 个不可打印字符', /剔除 1 个不可打印字符/.test(rCtrl.err), rCtrl.err);
const rtCtrl = pparse(rCtrl.out);
check('N204 生成的 plist 可被本页解析器再次解析（无 parsererror）', !/XML 解析错误|parsererror/.test(rtCtrl.err) && /xy/.test(rtCtrl.out), rtCtrl.err + ' | ' + rtCtrl.out);
check('N204 \t \n \r 合法空白不被剔除', !/剔除/.test(pgen(JSON.stringify({ a: 'a\tb\nc\rd' })).err), pgen(JSON.stringify({ a: 'a\tb\nc\rd' })).err);
check('N204 连续转换重置计数（第二次无控制字符不残留提示）', (() => {
  pgen(ctrl); const second = pgen(JSON.stringify({ a: 'clean' })); return !/剔除/.test(second.err);
})(), '');

// 重复函数 / 成功提示颜色
check('plist setErr / setOut / clearAll / loadSample 各只剩一份定义',
  ['setErr', 'setOut', 'clearAll', 'loadSample'].every(n => (P.html.match(new RegExp('function ' + n + '\\(', 'g')) || []).length === 1),
  ['setErr', 'setOut', 'clearAll', 'loadSample'].map(n => n + '=' + (P.html.match(new RegExp('function ' + n + '\\(', 'g')) || []).length).join(','));
check('plist 成功态状态栏为绿色 ok 类', /\bok\b/.test(pgen('{"a":1}').cls), pgen('{"a":1}').cls);
check('plist 失败态状态栏为红色非 ok 类', (() => { const r = pgen('{bad'); return !/\bok\b/.test(r.cls) && /❌/.test(r.err); })(), '');

// ══════════════ char-encoder ══════════════
const C = makeDom(CHAR);
const cw = C.w, cd = C.d, $$ = id => cd.getElementById(id);
function cconvert(text) { $$('input').value = text; cw.convert(); return $$('results').textContent; }
// N205 ASCII 行
const asciiRes = cconvert('Hello');
check('N205 纯 ASCII 文本 ASCII 行输出十进制码点不标「多字节序列」',
  /72 101 108 108 111/.test(asciiRes) && !/多字节序列|Multi-byte sequence/.test(asciiRes), asciiRes.slice(0, 120));
const mixRes = cconvert('A中');
check('N205 含非 ASCII 时逐点标注 U+4E2D 且不再整行「多字节序列」',
  /非ASCII\(U\+4E2D\)|Non-ASCII\(U\+4E2D\)/.test(mixRes) && !/多字节序列:|Multi-byte sequence:/.test(mixRes), mixRes.slice(0, 140));
check('N205 ASCII 行与 UTF-8 字节行内容不再完全重复（混合文本）', (() => {
  // 取两张卡的 val：ASCII 行含 U+ 标注，UTF-8 bytes 行是纯字节，必不相同
  const cards = [...cd.querySelectorAll('.format-card')].map(c => [c.querySelector('.name').textContent, c.querySelector('.val').textContent]);
  const a = cards.find(x => /ASCII/.test(x[0])), b = cards.find(x => /UTF-8 Bytes/.test(x[0]));
  return !!a && !!b && a[1] !== b[1];
})(), '');
check('N205 单字符 ASCII「A」仍为 65', /65/.test(cconvert('A')), cconvert('A').slice(0, 80));
// N206 清空
cconvert('Hello');
check('N206 清空前字节视图有内容', /U\+0048|104|H/.test($$('byteViewBox').textContent), $$('byteViewBox').textContent.slice(0, 80));
cw.clearAll();
check('N206 clearAll 后字节视图被清空', $$('byteViewBox').textContent.trim() === '' && $$('byteViewBox').innerHTML === '', JSON.stringify($$('byteViewBox').innerHTML.slice(0, 80)));
check('N206 clearAll 后结果与输入框也为空', $$('results').textContent.trim() === '' && $$('input').value === '', '');
// 状态链
cconvert('Hi');
check('状态链 清空后再次转换正常产出 Base64', /SGk=/.test(cconvert('Hi')), cconvert('Hi').slice(-120));

// ══════════════ 公式 / i18n 三源 ══════════════
if (!OLD_DIR) {
  const enP = JSON.parse(fs.readFileSync('i18n/tools/en/it/plist-parser.json', 'utf8'));
  const f = P.html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
  check('公式 plist 说明含 __plistType / 大整数 / 控制字符三条新规则', !!f &&
    /__plistType/.test(f[1]) && /大整数/.test(f[1]) && /控制字符/.test(f[1]), f ? f[1].slice(-80) : 'missing');
  check('公式 plist en JSON 同文中文键与英译', !!f && !!enP.map[f[1]] &&
    /__plistType/.test(enP.map[f[1]]) && /control characters/.test(enP.map[f[1]]), f ? String(enP.map[f[1]] || '').slice(-80) : 'no formula');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
