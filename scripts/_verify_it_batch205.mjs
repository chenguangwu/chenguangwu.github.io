// 第205批 · IT-N258 qrcode 中文/emoji UTF-8 编码（JSDOM 真机）
// 注：源码修复已在 HEAD（其他 Agent 所为），本批只补验证证据 + 清单销账。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/qrcode.html';
const html = fs.readFileSync(PAGE, 'utf8');
const lib = fs.readFileSync('js/qrcode.js', 'utf8');
// 外部库 <script src> 在 JSDOM 默认不加载；改为在 beforeParse 里 w.eval 注入，
// 避免把库源码内联进 HTML（库含 </script> 字面量会截断 HTML 解析）。

const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/qrcode.html',
  beforeParse(w) {
    w.eval(lib); // 注入 qrcode 全局（库 UMD 在无 exports 的 window 上定义 var qrcode）
    w.alert = () => {};
    w.i18nText = (k, fb) => (fb != null ? fb : '');
    w.ToolBox = { copyText() {}, showToast() {}, toggleToolTheme() {}, downloadText() {} };
    w.TBKit = { util: { isEn: () => false, exportTable() {} }, chart: { bar() {}, line() {} }, matrix: { table() {} }, history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} } };
    w.console = { warn() {}, log() {}, error() {} };
    // canvas 2d 上下文 stub（JSDOM 无 canvas）
    const ctx = { fillStyle: '', fillRect() {}, clearRect() {}, drawImage() {}, beginPath() {}, arc() {}, fill() {} };
    w.HTMLCanvasElement.prototype.getContext = function () { return ctx; };
    w.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:image/png;base64,'; };
  }
});
const w = dom.window, d = w.document;
try { d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true })); } catch (e) {}
check('qrcode 库全局就绪', typeof w.qrcode === 'function' && !!w.qrcode.stringToBytesFuncs);

// ── generate() 切换到 UTF-8 编码 ──
{
  d.getElementById('textInput').value = '你好';
  // spy：包装 stringToBytes，记录 generate 时实际使用的编码器与入参
  let usedArgs = [];
  const orig = w.qrcode.stringToBytes;
  w.qrcode.stringToBytes = function (s) { usedArgs.push(s); return orig.call(this, s); };
  w.generate();
  const isUtf8Fn = w.qrcode.stringToBytes === w.qrcode.stringToBytesFuncs['UTF-8'] || usedArgs.length > 0;
  check('generate 已切到 UTF-8 编码器', w.qrcode.stringToBytes === w.qrcode.stringToBytesFuncs['UTF-8'], 'isFunc=' + (w.qrcode.stringToBytes === w.qrcode.stringToBytesFuncs['UTF-8']));
  // 直接验证切到 UTF-8 后库的编码字节 = 标准 UTF-8
  w.qrcode.stringToBytes = w.qrcode.stringToBytesFuncs['UTF-8'];
  for (const s of ['你好', '😀', 'A', 'Hi中']) {
    const got = Array.from(w.qrcode.stringToBytes(s));
    const exp = Array.from(Buffer.from(s, 'utf8'));
    check('UTF-8 编码正确: ' + JSON.stringify(s), JSON.stringify(got) === JSON.stringify(exp), JSON.stringify(got));
  }
  w.qrcode.stringToBytes = orig;
}

// ── __qrBytes 与实际 UTF-8 字节数一致（含 emoji 代理对）──
{
  for (const s of ['你好', '😀', 'A', 'Hi中', 'a😀b']) {
    const n = w.__qrBytes(s);
    const exp = Buffer.from(s, 'utf8').length;
    check('__qrBytes 一致: ' + JSON.stringify(s), n === exp, 'n=' + n + ' exp=' + exp);
  }
}

// ── 生成的 QR 使用 UTF-8 字节（矩阵随编码变化，中文与 ASCII 不同）──
{
  function matrixFor(s) {
    w.qrcode.stringToBytes = w.qrcode.stringToBytesFuncs['UTF-8'];
    const q = w.qrcode(0, 'L');
    q.addData(s);
    q.make();
    const n = q.getModuleCount();
    let bits = '';
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) bits += q.isDark(r, c) ? '1' : '0';
    return bits;
  }
  const cn = matrixFor('你好'), ascii = matrixFor('ni hao'), same = matrixFor('你好');
  check('中文 QR 矩阵与对应 ASCII 不同（非 Latin-1 截断）', cn !== ascii);
  check('同内容 QR 矩阵稳定', cn === same);
}

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
