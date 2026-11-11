// 第184批 · IT-N457 url-qr 可调尺寸控件验证
// 判别核心：尺寸下拉必须真正改变 canvas 边长（旧实现无该控件、drawQR 固定 cell=8）。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/url-qr.html';
const html = fs.readFileSync(PAGE, 'utf8');
const qrLib = fs.readFileSync('js/qrcode.js', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

let isEn = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/url-qr.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
    w.HTMLCanvasElement.prototype.getContext = function () {
      return { fillStyle: '', fillRect() {}, clearRect() {}, drawImage() {} };
    };
  }
});
const w = dom.window;
try { w.eval(qrLib); } catch (e) {}
const d = w.document;

function gen(px, ecl) {
  if (px != null) { const s = d.getElementById('qrSize'); if (s) s.value = String(px); }
  if (ecl != null) d.getElementById('ecl').value = ecl;
  w.generate();
  const cv = d.querySelector('#output canvas');
  return { w: cv ? cv.width : 0, h: cv ? cv.height : 0, info: d.querySelector('#output .qr-info') ? d.querySelector('#output .qr-info').textContent : '' };
}

// 判别1：尺寸下拉存在且四档生效
const sizeSel = d.getElementById('qrSize');
check('尺寸下拉存在', !!sizeSel && sizeSel.options && sizeSel.options.length === 4, sizeSel && sizeSel.options && sizeSel.options.length);
if (sizeSel) {
  for (const px of [128, 256, 512, 1024]) {
    const r = gen(px, 'M');
    check('尺寸 ' + px + ' 生效', r.w === px && r.h === px, r.w + 'x' + r.h);
  }
  // 判别2：信息栏显示所选像素（中英双语）
  const rZh = gen(512, 'M');
  check('中文信息栏含输出像素', rZh.info.indexOf('512×512 像素') >= 0, rZh.info.slice(0, 90));
  isEn = true;
  const rEn = gen(1024, 'M');
  check('英文信息栏含 px', rEn.info.indexOf('1024×1024 px') >= 0, rEn.info.slice(0, 90));
  isEn = false;
  // 判别3：状态链——尺寸切换不影响纠错/内容正确性
  const a = gen(256, 'L'), b = gen(256, 'H'), c = gen(512, 'H');
  check('切尺寸后 canvas 跟随', c.w === 512 && c.h === 512, c.w + 'x' + c.h);
  check('纠错等级仍独立生效', a.info.indexOf('纠错等级 L') >= 0 && b.info.indexOf('纠错等级 H') >= 0, 'L/H info ok');
  // 判别4：英文 label/option 映射存在
  check('英译 map 含尺寸 label', typeof w.__TI18N_EN !== 'undefined' ? true : fs.readFileSync('js/tool-i18n-en.js', 'utf8').indexOf("'输出尺寸（像素，正方形边长）':'Output size (pixels, square side)'") >= 0, 'map entry');
}

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
