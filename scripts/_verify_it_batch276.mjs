// 第276批 JSDOM 验证：IT-N324 ITF 起止符 / IT-N325 规范化数字串唯一真值
// 用法: node scripts/_verify_it_batch276.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const file = OLD ? `${OLD}/tools/it/barcode-itf.html` : 'tools/it/barcode-itf.html';
const html = fs.readFileSync(file, 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

let canvasText = '', copied = '';
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/barcode-itf.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, copyText() {}, exportCsv() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
      preset: { bar() {} },
    };
    w.i18nText = () => '';
    w.alert = () => {};
    Object.defineProperty(w.navigator, 'clipboard', {
      value: { writeText(t) { copied = String(t); return Promise.resolve(); } }, configurable: true,
    });
    const ctx = {
      fillStyle: '', font: '', textAlign: '',
      fillRect() {}, fillText(t) { canvasText = String(t); },
    };
    if (w.HTMLCanvasElement && w.HTMLCanvasElement.prototype) {
      w.HTMLCanvasElement.prototype.getContext = function () { return ctx; };
      w.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:,'; };
    }
  },
});
const w = dom.window, d = w.document;

// ---------- N324：ISO/IEC 16390 起止符 ----------
const bits = w.buildITF('1234');
check('N324 起始 guard 为 1010（模块位）', bits.slice(0, 4) === '1010', 'head=' + bits.slice(0, 8));
check('N324 终止 guard 为宽窄元素 11010（模块位 111010111）', bits.slice(-9) === '111010111', 'tail=' + bits.slice(-9));
check('N324 宽窄比 3:1（W=3 模块 / N=1 模块）', /111/.test(bits) && /(?<!1)0(?!0)/.test(bits), 'len=' + bits.length);
check('N324 公式文案声明起止符与 3:1', html.indexOf('起始 1010 / 终止 11010') >= 0 && html.indexOf('宽窄比 3:1') >= 0);

// ---------- N325：规范化值为唯一真值 ----------
d.getElementById('data').value = 'ITF1234';
w.generate();
const barText = d.querySelector('#output .bar-text').textContent || '';
w.copyResult();
check('N325 画布文字为补零后真实编码值', canvasText === '1234', 'canvas=' + canvasText);
check('N325 页面 .bar-text 与画布一致', barText === canvasText, 'barText=' + barText);
check('N325 剪贴板与画布一致', copied === canvasText, 'copied=' + copied);
check('N325 三处不再出现原始输入 ITF1234', [canvasText, barText, copied].every(s => s.indexOf('ITF1234') < 0));

d.getElementById('data').value = '12345';
w.generate();
w.copyResult();
check('N325 奇数位输入三处统一为前补零 012345', canvasText === '012345' && d.querySelector('#output .bar-text').textContent === '012345' && copied === '012345', 'canvas=' + canvasText + ' copied=' + copied);

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
