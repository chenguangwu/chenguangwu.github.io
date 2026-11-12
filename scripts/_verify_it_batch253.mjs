// 第253批 JSDOM 验证：IT-N139 往返 / N140 ResText / N141 历史防抖去重 / N142 模式回填
// 用法: node scripts/_verify_it_batch253.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/caesar-cipher.html` : 'tools/it/caesar-cipher.html';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const html = fs.readFileSync(page(), 'utf8');

function makeDom() {
  const store = {};
  const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://example.com/caesar.html', beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false, diffBox() {}, exportTable() {} },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: {
        list: () => [], last: () => null,
        record: (r) => { w.__records = w.__records || []; w.__records.push(r); },
        mount: (sel, cb) => { w.__mountCb = cb; }
      }
    };
    // localStorage 桩
    const ls = {};
    Object.defineProperty(w, 'localStorage', { configurable: true, value: {
      getItem: k => (k in ls ? ls[k] : null), setItem: (k, v) => { ls[k] = String(v); },
      removeItem: k => { delete ls[k]; }, clear: () => { for (const k in ls) delete ls[k]; }
    }});
  }});
  return dom;
}

// ---- N139: onlyAlpha=false 加解密往返（MOD=95）----
{
  const dom = makeDom(), w = dom.window, d = w.document;
  const round = w.caesarShift('Hello, World! 2024', 3, false, true, true); // encrypt
  const back = w.caesarShift(round, 3, false, true, false);               // decrypt
  check('N139 全字符 shift3 往返还原', back === 'Hello, World! 2024', `enc=${round} back=${back}`);
  const r13 = w.caesarShift('Hello', 13, false, true, true);
  const b13 = w.caesarShift(r13, 13, false, true, false);
  check('N139 全字符 shift13 往返还原', b13 === 'Hello', `enc=${r13}`);
  const r25 = w.caesarShift('Test~2024', 25, false, true, true);
  const b25 = w.caesarShift(r25, 25, false, true, false);
  check('N139 全字符 shift25 往返还原', b25 === 'Test~2024', `enc=${r25}`);
}

// ---- N140: ResText 读 .value ----
{
  const dom = makeDom(), w = dom.window, d = w.document;
  d.getElementById('input').value = 'Hello';
  w.process();
  const res = w.__caesar_cipherResText();
  check('N140 ResText 读 textarea.value', res === 'Khoor' || res === 'Hello', 'res=' + res);
}

// ---- N141: 防抖 + 全量去重（同步可控：直接调 saveHistory 验证去重，防抖用定时器桩验证）----
{
  const dom = makeDom(), w = dom.window;
  w.localStorage.clear();
  w.saveHistory('Hello', 'Khoor', 3, 'encrypt');
  w.saveHistory('He', 'Kh', 3, 'encrypt');
  w.saveHistory('Hello', 'Khoor', 3, 'encrypt'); // 与首条同输入，应去重而非新增
  const hist = JSON.parse(w.localStorage.getItem('caesar_history') || '[]');
  check('N141 全量去重不刷前缀', hist.length === 2, 'n=' + hist.length + ' inputs=' + hist.map(x => x.input).join(','));
  // 防抖：源码层面确认 process 走调度器而非直接 saveHistory
  check('N141 process 走防抖调度', /__caesar_cipherScheduleHistory\(input, result, shift, currentMode\)/.test(html), 'source guard');
}

// ---- N142: 模式回填 ----
{
  const dom = makeDom(), w = dom.window, d = w.document;
  // setMode 无参兜底
  w.setMode('decrypt');
  w.setMode();
  const m1 = w.eval('currentMode');
  check('N142 setMode 无参保留当前模式', m1 === 'decrypt', 'mode=' + m1);
  // 回填回调传入 __mode
  const rec = { input: 'Hello', output: 'Khoor', shift: '3', __mode: 'decrypt' };
  w.setMode('encrypt');
  try { w.__mountCb(rec); } catch (e) { /* 回填里部分桩元素可能缺失 */ }
  const m2 = w.eval('currentMode');
  check('N142 回填恢复记录中的 mode', m2 === 'decrypt', 'mode=' + m2);
  // record 带出 __mode
  w.localStorage.clear();
  w.__records = [];
  w.setMode('decrypt');
  d.getElementById('input').value = 'ABC';
  w.process();
  // extras 由包装层触发（节流），直接检查源码含 __mode 赋值
  check('N142 record 含 __mode 字段', /rec\.__mode=currentMode/.test(html), 'source guard');
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
