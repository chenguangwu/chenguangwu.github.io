// 第198批 · IT-N246/N247/N248 binary-to-text 严格解码/历史评分/FAQ 口径（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/binary-to-text.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

let isEn = false;
const alerts = [];
const hist = [];   // [{t, d}, ...] 与页面 TBKit.history.list() 形态一致

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/binary-to-text.html',
  beforeParse(w) {
    w.alert = m => { alerts.push(String(m)); };
    w.i18nText = k => k;
    w.TextDecoder = TextDecoder;           // JSDOM window 默认无 TextDecoder
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    Object.defineProperty(w.navigator, 'clipboard', {
      configurable: true,
      value: { writeText() { return Promise.resolve(); } }
    });
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: { bar() {} },
      history: {
        list() { return hist.slice(); },
        record(d) { hist.unshift({ t: Date.now(), d: Object.assign({}, d) }); },
        last() { return hist.length ? hist[0].d : null; },
        mount() {}, clear() {}
      }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

function setInput(s) {
  d.getElementById('input').value = s;
  w.eval('__binary_to_text_last = 0;');   // 绕开 1s 节流，确保每次都 record
  w.eval('convert()');
  return d.getElementById('output').value;
}

// ── IT-N247 合法 UTF-8 仍正常解码 ──
check('合法 UTF-8 Hi 正常解码', setInput('01001000 01101001') === 'Hi', JSON.stringify(d.getElementById('output').value));

// 空格由字节 00100000 还原（FAQ 新口径的实证）
check('空格字节 00100000 还原', setInput('01000001 00100000 01000010') === 'A B', JSON.stringify(d.getElementById('output').value));

// ── IT-N247 非法 UTF-8：Latin-1 对照 + 十六进制字节列表 + 非法字节数 ──
const badOut = setInput('11111111 01000001');
check('非法 UTF-8 明确告警', /非法 UTF-8|invalid UTF-8/.test(badOut), badOut.slice(0, 60));
check('非法 UTF-8 给 Latin-1 对照', badOut.indexOf('Latin-1') >= 0);
check('非法 UTF-8 给十六进制字节 0xFF/0x41', badOut.indexOf('0xFF') >= 0 && badOut.indexOf('0x41') >= 0);
check('非法 UTF-8 含非法字节计数', /含 1 个非法 UTF-8 字节|1 invalid UTF-8 byte/.test(badOut), badOut.slice(0, 40));
check('非法 UTF-8 保留 Latin-1 字节 ÿA', badOut.indexOf('\u00FF\u0041') >= 0);

// ── IT-N247 BOM 不再被吞 ──
const bomOut = setInput('11101111 10111011 10111111 01000001');
check('BOM 保留 U+FEFF（ignoreBOM:true）', bomOut.indexOf('\uFEFF') >= 0, JSON.stringify(bomOut.slice(0, 20)));

// ── IT-N246 错误词评分启发式已删除 ──
check('score(含中文错误词)=1', w.eval("__binary_to_textScore('页面显示：错误')") === 1);
check('score(Error 404)=1', w.eval("__binary_to_textScore('Error 404')") === 1);

// ── IT-N246 历史链：含错误词的结果仍记通过 ──
setInput('01000001'); // "A"
hist.length = 0;
w.eval('__binary_to_text_last = 0;');
w.eval('convert()');
check('历史链写入成功', hist.length >= 1, 'n=' + hist.length);
check('历史 __tbScore=1', hist.length >= 1 && hist[0].d.__tbScore === 1, JSON.stringify(hist[0] && hist[0].d));

// 强制写一条含「错误」词结果的记录，验证不再假性掉零
w.eval("TBKit.history.record({input:'01000001',结果:'页面显示：错误',__tbScore:__binary_to_textScore('页面显示：错误')})");
check('含错误词记录 verdict=通过', hist[0].d.__tbScore === 1, String(hist[0].d.__tbScore));

// ── IT-N248 FAQ / formula-eq 页面文案 ──
const body = d.body.textContent;
check('FAQ 含「直接报错并中止」新口径', body.indexOf('直接报错并中止') >= 0);
check('FAQ 含 00100000 空格还原说明', body.indexOf('00100000') >= 0);
check('formula-eq 含 fatal:true 严格解码', body.indexOf('fatal:true') >= 0 && body.indexOf('ignoreBOM:true') >= 0);

// ── IT-N248 三源（页面 / en JSON / deep-dive）一致 ──
const enJson = JSON.parse(fs.readFileSync('i18n/tools/en/it/binary-to-text.json', 'utf8'));
const deep = JSON.parse(fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8'));
function collect(o, acc) {
  if (o && typeof o === 'object') for (const k in o) { acc.push(k); if (typeof o[k] === 'string') acc.push(o[k]); else collect(o[k], acc); }
  return acc;
}
const enAll = collect(enJson, []).join('\n');
const deepAll = collect(deep['it/binary-to-text'] || {}, []).join('\n');
check('en JSON 同步 00100000 口径', enAll.indexOf('00100000') >= 0);
check('en JSON 同步 直接报错中止口径', /直接报错并中止|reports an error and stops|reports an error/i.test(enAll));
check('deep-dive FAQ 同步 00100000', deepAll.indexOf('00100000') >= 0);
check('deep-dive FAQ 同步 直接报错中止', /直接报错并中止|直接报错/.test(deepAll));

// ── 长度非 8 倍数直接报错（FAQ 新口径实证）──
alerts.length = 0;
setInput('0100000');
check('非 8 倍数触发 alert 中止', alerts.some(a => /8 的倍数/.test(a)), alerts.join(' | '));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
