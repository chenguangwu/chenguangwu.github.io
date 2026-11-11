// 第249批探测 · IT-N124/N125/N126/N127/N128/N129（barcode-code128 / barcode-upc）
//  N124 Code128 混合 ASCII 0~127 支持 A/B 子集切换
//  N125 空输入不再被 || ' ' 吞掉
//  N126 引据表 3 条 2 空 → 3 条 3 空
//  N127 UPC 空/非数字/位数不再静默补零或截断（复核）
//  N128 UPC 12 位校验位必须核对（复核）
//  N129 UPC 首位数字印在左静区
// 用法：node scripts/_verify_it_batch249.mjs [旧文件目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s) };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
  w.navigator.clipboard = { writeText: () => Promise.resolve() };
}
function makeDom(name) {
  const file = OLD_DIR ? OLD_DIR + '/' + name : 'tools/it/' + name;
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + name,
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
function loadLib(w) {
  const lib = OLD_DIR ? OLD_DIR + '/barcode-lib.js' : 'js/barcode-lib.js';
  w.eval(fs.readFileSync(lib, 'utf8'));
  return w.ToolBoxBarcode;
}

// ══════════════ N124 Code128 混合子集 ══════════════
{
  const dom = makeDom('barcode-code128.html'), w = dom.window;
  loadLib(w);
  const mixed = w.eval("(function(){var r=ToolBoxBarcode.encode('code128','a\\u0001');return JSON.stringify({ok:r.ok,sub:r.detail&&r.detail.subset,bits:r.ok?r.bits.length:0,err:r.error});})()");
  let m = {};
  try { m = JSON.parse(mixed); } catch (e) {}
  check('N124 可打印+控制混合串成功编码', m.ok === true && /A|B/.test(m.sub || ''), mixed);
  check('N124 混合串标注子集切换', /B\/A|A\/B/.test(m.sub || ''), m.sub);
  const highMix = w.eval("(function(){var r=ToolBoxBarcode.encode('code128','\\u0001~');return JSON.stringify({ok:r.ok,sub:r.detail&&r.detail.subset,err:r.error});})()");
  let h = {};
  try { h = JSON.parse(highMix); } catch (e) {}
  check('N124 控制符+波浪号 A→B 切换', h.ok === true && /A\/B/.test(h.sub || ''), highMix);
  const validBits = w.eval("(function(){var r=ToolBoxBarcode.encode('code128','a\\u0001');return r.ok && /^[01]+$/.test(r.bits) && r.bits.length%11===13%11;})()");
  check('N124 编码位串结构合法', validBits === true, validBits);
  const nonAscii = w.eval("(function(){var r=ToolBoxBarcode.encode('code128','中文');return JSON.stringify({ok:r.ok,err:r.error});})()");
  check('N124 非 ASCII 仍明确拒绝', /仅支持 ASCII 0~127/.test(nonAscii), nonAscii);
}

// ══════════════ N125 空输入不再补空格 ══════════════
{
  const dom = makeDom('barcode-code128.html'), w = dom.window;
  let captured = 'NOT_CALLED';
  w.ToolBoxBarcode = {
    encode(type, text) { captured = text; return { ok: false, error: 'stub' }; },
    renderCanvas() { return {}; }
  };
  w.document.getElementById('data').value = '';
  w.generate();
  check('N125 空输入原样传给编码库', captured === '', JSON.stringify(captured));
}

// ══════════════ N126 引据表条空数 ══════════════
{
  const file = OLD_DIR ? OLD_DIR + '/barcode-code128.html' : 'tools/it/barcode-code128.html';
  const html = fs.readFileSync(file, 'utf8');
  check('N126 引据改 3 条 3 空', /3 条 3 空/.test(html) && !/3 条 2 空/.test(html), 'checked');
  check('N126 英文同步 3 bars + 3 spaces', /3 bars \+ 3 spaces/.test(html) && !/3 bars \+ 2 spaces/.test(html), 'checked');
}

// ══════════════ N127 UPC 非法输入不再静默补全 ══════════════
{
  const dom = makeDom('barcode-upc.html'), w = dom.window;
  const empty = w.eval("JSON.stringify(window.buildUPC(''))");
  const alpha = w.eval("JSON.stringify(window.buildUPC('abcdefghijk'))");
  const short = w.eval("JSON.stringify(window.buildUPC('1234567890'))");
  check('N127 空输入明确报错', /"error":"empty"/.test(empty), empty);
  check('N127 纯字母明确报错', /"error":"nonDigit"/.test(alpha), alpha);
  check('N127 位数不足不静默补零', /"error":"length"/.test(short), short);
  const valid = w.eval("(function(){var r=window.buildUPC('03600029145');return r.ok!==false&&r.d==='036000291452';})()");
  check('N127 合法 11 位仍自动补校验位', valid === true, valid);
}

// ══════════════ N128 UPC 12 位校验位 ══════════════
{
  const dom = makeDom('barcode-upc.html'), w = dom.window;
  const bad = w.eval("JSON.stringify(window.buildUPC('036000291453'))");
  const good = w.eval("(function(){var r=window.buildUPC('036000291452');return r.ok!==false&&r.d==='036000291452';})()");
  check('N128 错误校验位拒绝并给正确值', /"error":"check"/.test(bad) && /"expect":2/.test(bad), bad);
  check('N128 正确校验位正常生成', good === true, good);
}

// ══════════════ N129 UPC 首位在左静区 ══════════════
{
  const dom = makeDom('barcode-upc.html'), w = dom.window;
  const placement = w.eval(`(function(){
    var calls=[];var orig=document.createElement;
    document.createElement=function(tag){
      if(tag!=='canvas')return orig.apply(document,arguments);
      return {width:0,height:0,getContext:function(){return {fillStyle:'',font:'',textAlign:'',fillRect:function(){},fillText:function(t,x,y){calls.push([String(t),x,y]);}};}};
    };
    try{window.drawBarcode('10100011010011011010010011010101110100111010100111101010110010110101110010110111000101','036000291452');}catch(e){calls.push(['ERR '+e.message,0,0]);}
    document.createElement=orig;
    return JSON.stringify(calls);
  })()`);
  let calls = [];
  try { calls = JSON.parse(placement); } catch (e) {}
  const texts = calls.map(c => c[0]);
  check('N129 首位单独印在左静区', texts[0] === '0' && calls[0][1] < 15, JSON.stringify(calls[0]));
  check('N129 其余分 5+6 两组', texts[1] === '36000' && texts[2] === '291452', texts.join('|'));
  check('N129 左静区留出宽度', w.eval("Math.round(document.querySelector('#output')?1:1)") === 1 && /leftQuiet=24/.test(fs.readFileSync(OLD_DIR ? OLD_DIR + '/barcode-upc.html' : 'tools/it/barcode-upc.html','utf8')), 'checked');
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
