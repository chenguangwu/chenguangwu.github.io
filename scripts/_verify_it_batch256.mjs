// 第256批 JSDOM 验证：IT-N149 Atbash 概念 / N150 三页历史防抖去重 / N151 三页模式回填
// 用法: node scripts/_verify_it_batch256.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const pg = (f) => OLD ? `${OLD}/${f}` : f;
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function makeDom(file) {
  const html = fs.readFileSync(pg(file), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://x.com/', beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
    w.TBKit = { util: { isEn: () => false, exportTable() {}, diffBox() {} }, chart: { bar() {}, line() {} },
      matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount: (s, cb) => { w.__mountCb = cb; }, clear() {} } };
    const ls = {};
    Object.defineProperty(w, 'localStorage', { configurable: true, value: {
      getItem: k => (k in ls ? ls[k] : null), setItem: (k, v) => { ls[k] = String(v); },
      removeItem: k => { delete ls[k]; }, clear: () => { for (const k in ls) delete ls[k]; }
    }});
  }});
  return { dom, html };
}

// N149: Atbash 概念文案
{
  const { html } = makeDom('tools/it/atbash-cipher.html');
  check('N149 删除错误「特例」说法', !/位移为13时的特例|shift of 13/.test(html), 'zh page');
  check('N149 新增对合但映射不同说明', /镜像置换 f\(x\)=25/.test(html) && /f\(x\)=x\+13/.test(html), 'concept');
  const en = fs.readFileSync(OLD ? `${OLD}/atbash.en.json` : 'i18n/tools/en/it/atbash-cipher.json', 'utf8');
  check('N149 英文映射同步', /involution/.test(en) && /f\(x\)=25-x/.test(en) && !/special case of the Caesar/.test(en), 'en map');
}

// N150/N151 三页
const pages = [
  { file: 'tools/it/atbash-cipher.html', histKey: 'atbash_history', prefix: '__atbash_cipher', modeVar: 'currentMode',
    save: (w) => { w.saveHistory('Hello', 'Svool', 'encrypt'); w.saveHistory('He', 'Sv', 'encrypt'); w.saveHistory('Hello', 'Svool', 'encrypt'); },
    expectN: 2 },
  { file: 'tools/it/playfair-cipher.html', histKey: 'playfair_history', prefix: '__playfair_cipher', modeVar: 'currentMode',
    save: (w) => { w.saveHistory('HELLO', 'CIPHER', 'KEY', 'encrypt'); w.saveHistory('HEL', 'CIP', 'KEY', 'encrypt'); w.saveHistory('HELLO', 'CIPHER', 'KEY', 'encrypt'); },
    expectN: 2 },
  { file: 'tools/it/vigenere-visualizer.html', histKey: 'vigenere_history', prefix: '__vigenere_visualizer', modeVar: 'currentMode',
    save: (w) => { w.saveHistory('HELLO', 'RIJVS', 'KEY', 'encrypt'); w.saveHistory('HEL', 'RIJ', 'KEY', 'encrypt'); w.saveHistory('HELLO', 'RIJVS', 'KEY', 'encrypt'); },
    expectN: 2 },
];
for (const spec of pages) {
  const { dom, html } = makeDom(spec.file);
  const w = dom.window;
  w.localStorage.clear();
  spec.save(w);
  const hist = JSON.parse(w.localStorage.getItem(spec.histKey) || '[]');
  check(`${spec.file} N150 去重不刷前缀`, hist.length === spec.expectN, 'n=' + hist.length);
  check(`${spec.file} N150 防抖调度`, new RegExp(spec.prefix + 'ScheduleHistory').test(html), 'scheduled');
  // N151 setMode 无参保留模式
  w.setMode('decrypt');
  w.setMode();
  const m = w.eval(spec.modeVar);
  check(`${spec.file} N151 setMode 无参保留模式`, m === 'decrypt', 'mode=' + m);
  // N151 __mode 记录 + 回填传参
  check(`${spec.file} N151 记录含 __mode`, /rec\.__mode=currentMode/.test(html), 'record');
  check(`${spec.file} N151 回填用 __mode`, /setMode\(rec\.__mode/.test(html), 'restore');
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
