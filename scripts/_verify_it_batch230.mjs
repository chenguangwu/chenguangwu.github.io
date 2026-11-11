// 第230批 · IT-N227 + IT-N230~N232（rabbit 1 条 + sms-qr 3 条；N230 为已修补证据）
//  N227 解密格式靠猜、非法 IV 静默全 0（真修：跟随输出格式 + IV 严格 16 hex）
//  N230 伪随机二维码（进批探测：其他 Agent 已引入真实 MIT qrcode.js，补证据）
//  N231 号码未编码/# 截断（真修：去空格连字符 + 严格号码校验）
//  N232 NaN 守卫吞掉合法正文（真修：文本结果不再做 NaN 正则扫描）
// 用法：node scripts/_verify_it_batch230.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

function makeDom(htmlPath, en) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, setResult(id, v) { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } };
      w.TBKit = {
        util: { isEn: () => !!en, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
      };
      // JSDOM 无 canvas 包，给 2D 上下文最小桩；二维码模块矩阵仍由真实 QR 库计算
      if (w.HTMLCanvasElement && w.HTMLCanvasElement.prototype) {
        w.HTMLCanvasElement.prototype.getContext = () => ({ fillStyle: '', fillRect() {}, clearRect() {}, drawImage() {} });
      }
      // sms-qr 依赖本地真实 QR 库；JSDOM 不自动加载外链脚本，这里注入同源原文件
      try { w.eval(fs.readFileSync('js/qrcode.js', 'utf8')); } catch (e) {}
    }
  });
  return { dom, w: dom.window, d: dom.window.document, html };
}

const RAB = OLD_DIR ? OLD_DIR + '/rabbit.orig.html' : 'tools/it/rabbit.html';
const SMS = OLD_DIR ? OLD_DIR + '/sms.orig.html' : 'tools/it/sms-qr.html';

// ══════════════ N227 rabbit ══════════════
const R = makeDom(RAB), rw = R.w, rd = R.d;
const toasts = [];
rw.ToolBox.showToast = (m) => toasts.push(String(m));
rd.getElementById('key').value = '00000000000000000000000000000000';
rd.getElementById('iv').value = 'abcdefghijklmnop';
rd.getElementById('outputFormat').value = 'hex';
rd.getElementById('input').value = '616263';
rd.getElementById('output').value = 'OLD';
toasts.length = 0;
rw.decrypt();
check('N227 非 hex IV 明确报错而非静默当全 0', rd.getElementById('output').value === '' && toasts.some(t => /IV|16/.test(t)),
  'out=' + JSON.stringify(rd.getElementById('output').value) + ' toast=' + JSON.stringify(toasts));
let ivErr = '';
try { rw.eval("document.getElementById('iv').value='abc';getIV()"); } catch (e) { ivErr = String(e.message || e); }
check('N227 IV 长度不符直接抛错', /16/.test(ivErr), ivErr);
rd.getElementById('iv').value = '';
rd.getElementById('input').value = 'zzzz'; // 非 hex，也非合法 base64 字符组合
rd.getElementById('output').value = 'OLD';
toasts.length = 0;
rw.decrypt();
check('N227 Hex 模式下非 hex 密文被拒绝（不再猜 Base64）', rd.getElementById('output').value === '' && toasts.some(t => /Hex|hex|Base64|16/.test(t)),
  'out=' + JSON.stringify(rd.getElementById('output').value) + ' toast=' + JSON.stringify(toasts));
rd.getElementById('input').value = 'c6a7275ef85495d87ccd5d376705b7ed';
rd.getElementById('iv').value = '0000000000000000';
rw.decrypt();
check('N227 合法 Hex 密文仍可正常解密', rd.getElementById('output').value.length === 16 &&
  [...rd.getElementById('output').value].every(c => c.charCodeAt(0) === 0), 'len=' + rd.getElementById('output').value.length);
check('N227 源码已去掉密文基数正则猜测', !/\[0-9a-fA-F\\s\]\+/.test(R.html) && /fmt==='hex'/.test(R.html), '');
let oddErr = '';
try { rw.eval("hexToBytes('abc')"); } catch (e) { oddErr = String(e.message || e); }
check('N227 奇数位 hex 直接报错而非 parseInt(NaN)→0', /偶数|even/.test(oddErr), oddErr);
const RE = makeDom(RAB, true);
let enIvErr = '';
try { RE.w.eval("document.getElementById('iv').value='abc';getIV()"); } catch (e) { enIvErr = String(e.message || e); }
check('N227 英文态 IV 报错无汉字', !/[\u4e00-\u9fff]/.test(enIvErr) && /IV/.test(enIvErr), enIvErr);

// ══════════════ N230~N232 sms-qr ══════════════
const S = makeDom(SMS), sw = S.w, sd = S.d;
check('N230 页面加载真实 qrcode-generator 库且无伪随机填充', /js\/qrcode\.js/.test(S.html) && !/rnd\(\)|const N=27/.test(S.html), '');
const qrInfo = sw.eval("(function(){var q=qrcode(0,'M');q.addData('sms:13800138000?body=Hi');q.make();var n=q.getModuleCount(),dark=0;for(var r=0;r<n;r++)for(var c=0;c<n;c++)if(q.isDark(r,c))dark++;return n+'/'+dark;})()");
check('N230 真实 QR 编码产生模块矩阵（非固定 27×随机点）', /^\d+\/\d+$/.test(qrInfo) && Number(qrInfo.split('/')[0]) >= 21 && Number(qrInfo.split('/')[1]) > 50, qrInfo);
function build(phone, msg) {
  sd.getElementById('phone').value = phone;
  sd.getElementById('msg').value = msg;
  return sw.buildSms();
}
check('N231 空格/连字符号码归一化', build('138 0013-8000', 'Hi') === 'sms:13800138000?body=Hi', build('138 0013-8000', 'Hi'));
check('N231 国际号 + 前缀保留', build('+86 139-1234-5678', 'Hi') === 'sms:+8613912345678?body=Hi', build('+86 139-1234-5678', 'Hi'));
check('N231 #/& 不再造成截断：非法号码直接报错', (() => {
  try { build('13800138000#test&x', 'Hi'); return false; } catch (e) { return /5–15|5-15/.test(String(e.message)); }
})(), '');
check('N231 正文仍按 UTF-8 百分号编码', build('13800138000', 'a b&c#中文') === 'sms:13800138000?body=a%20b%26c%23%E4%B8%AD%E6%96%87', build('13800138000', 'a b&c#中文'));
sd.getElementById('phone').value = '13800138000';
sd.getElementById('msg').value = 'NaN';
sw.generate();
check('N232 正文含 NaN 正常出码（不再误报无效值）', /sms:13800138000\?body=NaN/.test(sd.getElementById('output').innerHTML) && !/无效值/.test(sd.getElementById('output').innerHTML),
  sd.getElementById('output').textContent.slice(0, 160));
const genSrc = S.html.slice(S.html.indexOf('function generate()'), S.html.indexOf('function escapeHtml'));
check('N232 页面不再对结果 HTML 做 NaN/Infinity 扫描', !/计算结果含无效值/.test(genSrc) && !/\/Infinity\//.test(genSrc) && !/NaN\(\[\^A-Za-z\]\)/.test(genSrc), '');
sd.getElementById('phone').value = '<img src=x onerror=alert(1)>';
sd.getElementById('msg').value = 'Hi';
sw.generate();
check('N231 非法号码的统一错误提示不回显输入、不产生 DOM 注入', !sd.getElementById('output').querySelector('img') &&
  /电话号码仅支持/.test(sd.getElementById('output').textContent) && !/img src=x/.test(sd.getElementById('output').innerHTML),
  sd.getElementById('output').innerHTML.slice(0, 160));
const SE = makeDom(SMS, true);
let enErr = '';
try { SE.w.eval("document.getElementById('phone').value='abc';buildSms()"); } catch (e) { enErr = String(e.message || e); }
check('N231 英文态号码报错无汉字', !/[\u4e00-\u9fff]/.test(enErr) && /Phone number/.test(enErr), enErr);
if (!OLD_DIR) {
  const enR = JSON.parse(fs.readFileSync('i18n/tools/en/it/rabbit.json', 'utf8'));
  const enS = JSON.parse(fs.readFileSync('i18n/tools/en/it/sms-qr.json', 'utf8'));
  const dd = JSON.parse(fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8'));
  check('三源同步：rabbit 英文映射含严格 IV/格式说明', Object.keys(enR.map).some(k => k.startsWith('按 RFC 4503 实现') && /IV 必须恰好 16 位/.test(k)), '');
  check('三源同步：sms-qr 英文映射含号码校验与示例', Object.keys(enS.map).some(k => k.includes('5–15 位数字')) &&
    Object.keys(enS.map).some(k => k.includes('sms:13800138000?body=Hi')), '');
  check('三源同步：deep-dive 已改为 sms: 示例', /sms:13800138000\?body=Hi/.test(dd['it/sms-qr'].examples[0].body), '');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
