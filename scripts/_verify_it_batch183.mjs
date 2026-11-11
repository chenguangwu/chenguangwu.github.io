// 第183批 · IT-N456/N457 url-qr 真二维码解码级验证
// 判别核心：真 QR 的格式信息位通过 BCH(15,5) 校验、EC 字段随 L/M/Q/H 变化、
// 矩阵尺寸随内容长度自适应；旧假实现（随机点阵）格式位恒 0、无视 EC 等级、恒 29×29。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/url-qr.html';
const html = fs.readFileSync(PAGE, 'utf8');
const qrLib = fs.readFileSync('js/qrcode.js', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

function mkDom() {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.com/tools/it/url-qr.html',
    beforeParse(w) {
      w.i18nText = k => k;
      w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
      };
      // JSDOM 无 canvas：stub getContext 让 generate() 的绘制路径不抛错（矩阵本身直接读 qr 对象）。
      w.HTMLCanvasElement.prototype.getContext = function () {
        return { fillStyle: '', fillRect() {}, clearRect() {}, drawImage() {} };
      };
    }
  });
  const w = dom.window;
  // 页面以 <script src> 外链编码器，JSDOM 不加载外部脚本；手动注入与生产同源的库。
  try { w.eval(qrLib); } catch (e) { /* 旧假源码页面没有该库也无妨 */ }
  return w;
}

// 从矩阵左上角读格式信息 15 位（标准 QR 布局，MSB first）
function fmtBits(qr) {
  const b = [];
  for (let i = 0; i <= 5; i++) b.push(qr.isDark(8, i) ? 1 : 0);
  b.push(qr.isDark(8, 7) ? 1 : 0);
  b.push(qr.isDark(8, 8) ? 1 : 0);
  b.push(qr.isDark(7, 8) ? 1 : 0);
  for (let i = 5; i >= 0; i--) b.push(qr.isDark(i, 8) ? 1 : 0);
  return b;
}
function bchValid(v) {
  const g = 0x537;
  let d = v ^ 0x5412; // 先解除掩码异或，得到 (data5<<10 | bch10)
  for (let i = 14; i >= 10; i--) if (d & (1 << i)) d ^= g << (i - 10);
  return d === 0; // 合法格式码字的 BCH 余数为 0
}
function fmtValue(bits) { let v = 0; for (const b of bits) v = (v << 1) | b; return v; }
function ecField(v) { return ((v ^ 0x5412) >> 10) >> 3; } // L=1 M=0 Q=3 H=2

const w = mkDom();

// —— 判别1：真实编码器被加载且 renderQR 返回可解码矩阵 ——
const hasEncoder = (() => { try { return typeof w.qrcode === 'function'; } catch (e) { return false; } })();
check('加载真实 QR 编码器', hasEncoder, typeof w.qrcode);
const rM = w.renderQR('https://github.com', 'M');
check('renderQR 返回 qr 对象', !!(rM && rM.qr && typeof rM.qr.isDark === 'function'), rM && rM.n);

if (rM && rM.qr) {
  const q = rM.qr;
  const bits = fmtBits(q);
  const v = fmtValue(bits);
  check('格式位 BCH 校验通过（真 QR 特征）', bchValid(v), '0x' + v.toString(16));
  const ec = ecField(v);
  check('M 级格式位 EC 字段=0', ec === 0, 'ec=' + ec);

  // —— 判别2：EC 字段随 L/M/Q/H 变化（假实现恒 0） ——
  const ecMap = { L: 1, M: 0, Q: 3, H: 2 };
  const gotEc = {};
  let ecOk = true;
  for (const lv of ['L', 'M', 'Q', 'H']) {
    const r = w.renderQR('https://github.com', lv);
    gotEc[lv] = r && r.qr ? ecField(fmtValue(fmtBits(r.qr))) : 'NA';
    if (gotEc[lv] !== ecMap[lv]) ecOk = false;
  }
  check('EC 字段随 L/M/Q/H 四档变化', ecOk, JSON.stringify(gotEc));

  // —— 判别3：矩阵尺寸随内容长度自适应（假实现恒 29×29） ——
  const nShort = w.renderQR('https://a.co', 'L').n;
  const nLong = w.renderQR('https://example.com/' + 'x'.repeat(120), 'L').n;
  check('矩阵尺寸随内容增长', nLong > nShort, nShort + ' -> ' + nLong);
  check('短 URL 非固定 29×29', nShort !== 29, 'nShort=' + nShort);

  // —— 判别4：不同纠错等级产生不同矩阵（假实现忽略等级） ——
  function sig(qr) {
    const n = qr.getModuleCount(); let s = '';
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) s += qr.isDark(r, c) ? '1' : '0';
    return s;
  }
  const qL = w.renderQR('https://example.com/pay', 'L').qr;
  const qH = w.renderQR('https://example.com/pay', 'H').qr;
  check('不同 EC 等级矩阵不同', sig(qL) !== sig(qH), 'L/H 签名长度 ' + sig(qL).length);

  // —— 判别5：UTF-8 中文按多字节编码（字节数 > 字符数） ——
  const cnText = 'https://例子.测试/路径';
  const rCn = w.renderQR(cnText, 'M');
  const bytesCn = w.qrByteLen(cnText);
  check('中文按 UTF-8 多字节计数', bytesCn > cnText.length, bytesCn + ' bytes vs ' + cnText.length + ' chars');
  check('中文 URL 生成有效矩阵', !!(rCn && rCn.qr && bchValid(fmtValue(fmtBits(rCn.qr)))), rCn && rCn.n);
} else {
  for (const n of ['格式位 BCH 校验通过（真 QR 特征）', 'M 级格式位 EC 字段=0', 'EC 字段随 L/M/Q/H 四档变化',
    '矩阵尺寸随内容增长', '短 URL 非固定 29×29', '不同 EC 等级矩阵不同', '中文按 UTF-8 多字节计数', '中文 URL 生成有效矩阵']) check(n, false, 'renderQR 无 qr 对象');
}

// —— 判别6：generate() 走真编码器路径，结果区含版本/字节信息 ——
try { w.generate(); } catch (e) { /* stub canvas 已避免绘制抛错 */ }
const outHtml = w.document.getElementById('output').innerHTML;
check('generate 输出真实版本信息', /最小版本 V\d+/.test(outHtml) || /beyond V10/.test(outHtml), outHtml.replace(/<[^>]*>/g, ' ').slice(0, 90));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
