// 第233批探测 · IT-N273~N277（phone-qr 3 条 + protobuf-parser 2 条）
//  N273 假二维码 → 已引入真 qrcode.js（探测确认）
//  N274 已带 tel: 的输入不剥离空白（待修）
//  N275 无 PNG 下载 + 无静区（待修 / 静区已修）
//  N276 map<> 解析（主路径已修，oneof 内待确认）
//  N277 校验只数括号（已修，探测确认）
// 用法：node scripts/_verify_it_batch233.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 170) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, escHtml: s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
      };
      // canvas 最小桩：记录 fillRect 调用，getContext 返回可用对象
      w.HTMLCanvasElement.prototype.getContext = function () {
        if (!this.__rects) this.__rects = [];
        return {
          set fillStyle(v) {}, get fillStyle() { return '#000'; },
          fillRect(x, y, w2, h) { if (w2 > 0 && h > 0) this.__owner.__rects.push([x, y, w2, h]); },
          clearRect() {}, setTransform() {}, drawImage() {}, beginPath() {}, fill() {},
          getImageData() { return { data: new Uint8ClampedArray(4) }; }
        };
      };
      // 让 ctx 能访问 canvas（fillRect 里的 this 是 ctx）
      const origGet = w.HTMLCanvasElement.prototype.getContext;
      w.HTMLCanvasElement.prototype.getContext = function () {
        const canvas = this;
        if (!canvas.__rects) canvas.__rects = [];
        const ctx = {
          rects: canvas.__rects,
          set fillStyle(v) {}, get fillStyle() { return '#000'; },
          fillRect(x, y, w2, h) { if (w2 > 0 && h > 0) canvas.__rects.push([x, y, w2, h]); },
          clearRect() {}, setTransform() {}, drawImage() {}, beginPath() {}, fill() {},
          getImageData() { return { data: new Uint8ClampedArray(4) }; }
        };
        return ctx;
      };
    }
  });
  // 注入轻量 qrcode 库桩（仅当页面用外链 <script> 且 JSDOM 未加载时）
  const w = dom.window;
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, w, d: w.document, html };
}

const PQ = makeDom(OLD_DIR ? OLD_DIR + '/phone-qr.html' : 'tools/it/phone-qr.html');
const PB = makeDom(OLD_DIR ? OLD_DIR + '/protobuf-parser.html' : 'tools/it/protobuf-parser.html');
const rawPQ = fs.readFileSync(OLD_DIR ? OLD_DIR + '/phone-qr.html' : 'tools/it/phone-qr.html', 'utf8');
const rawPB = fs.readFileSync(OLD_DIR ? OLD_DIR + '/protobuf-parser.html' : 'tools/it/protobuf-parser.html', 'utf8');
let pw = PQ.w, bw = PB.w, pd = PQ.d, bd = PB.d;

// ══════════════ N273 真 QR ══════════════
check('N273 引入 js/qrcode.js 真二维码库', /js\/qrcode\.js/.test(rawPQ), '');
check('N273 drawQR 用 qrcode() 生成并按 isDark 绘制', /qrcode\(0,\s*'M'\)/.test(rawPQ) && /isDark\(/.test(rawPQ), '');
check('N273 画布留 4 模块静区', /margin\s*=\s*4/.test(rawPQ), '');

// ══════════════ N274 tel: 前缀空白 ══════════════
// 真机：输入带 tel: 且含空格，检查载荷（output 的 qr-text）是否剥离空白
function genPayload(input) {
  const el = pd.getElementById('phone');
  if (!el) return null;
  el.value = input;
  try { pw.generate(); } catch (e) { return 'THROW:' + e.message; }
  const qt = pd.querySelector ? pd.querySelector('.qr-text') : null;
  // JSDOM 有 querySelector
  const out = pd.getElementById('output');
  const m = String(out ? out.innerHTML : '').match(/qr-text[^>]*>([^<]*)</);
  return m ? m[1] : (qt ? qt.textContent : null);
}
const p1 = genPayload('tel:+86 138 0013 8000');
check('N274 已带 tel: 的输入剥离空白', p1 === 'tel:+8613800138000', 'payload=' + p1);
const p2 = genPayload('  +86 138 0013 8000  ');
check('N274 无 tel: 前缀输入先 trim 再剥离', p2 === 'tel:+8613800138000', 'payload=' + p2);

// ══════════════ N275 PNG 下载 ══════════════
check('N275 有 PNG 下载按钮（toDataURL）', /toDataURL\(['"]image\/png/.test(rawPQ), '');
check('N275 有下载入口 onclick', /downloadPNG|下载.*PNG|download.*png/i.test(rawPQ), '');

// ══════════════ N276 map<> 解析 ══════════════
function parse(input) {
  const el = bd.getElementById('input');
  if (!el) return null;
  el.value = input;
  try { bw.parseProto(); } catch (e) { return 'THROW:' + e.message; }
  const out = bd.getElementById('output'), err = bd.getElementById('err');
  return { out: String(out ? out.textContent : ''), err: String(err ? err.textContent : '') };
}
const r1 = parse('syntax = "proto3"; message M { map<string, Address> tags = 1; }');
check('N276 message 内 map<> 解析成功', r1 && r1.err.indexOf('❌') < 0 && /"map<string, Address>"/.test(r1.out) && /"tags"/.test(r1.out), r1 ? (r1.err + ' | ' + r1.out.slice(0, 80)) : 'null');
const r2 = parse('syntax = "proto3"; message M { oneof pick { map<string, string> opts = 1; } }');
check('N276 oneof 内 map<> 解析成功', r2 && r2.err.indexOf('❌') < 0 && /opts/.test(r2.out), r2 ? r2.err : 'null');

// ══════════════ N277 校验复用 parseProto ══════════════
function validate(input) {
  const el = bd.getElementById('input');
  if (!el) return null;
  el.value = input;
  try { bw.doValidate(); } catch (e) { return 'THROW:' + e.message; }
  const err = bd.getElementById('err'), out = bd.getElementById('output');
  return { err: String(err ? err.textContent : ''), out: String(out ? out.textContent : '') };
}
const v1 = validate('message X { int32 a }'); // 缺 = 编号与分号
check('N277 非法 .proto 校验报失败', v1 && /❌/.test(v1.err), v1 ? v1.err : 'null');
const v2 = validate('not proto at all');
check('N277 任意文本校验报失败', v2 && /❌/.test(v2.err), v2 ? v2.err : 'null');
const v3 = validate('syntax = "proto3"; message M { int32 a = 1; }');
check('N277 合法 .proto 校验通过', v3 && /✅/.test(v3.err), v3 ? v3.err : 'null');

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
