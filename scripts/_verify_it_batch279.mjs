// 第279批 JSDOM 验证：IT-N330 OTP 复制粘连倒计时 / IT-N331 矩阵维度变更后 null 解引用
// 用法: node scripts/_verify_it_batch279.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const root = OLD || '.';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function stub(w) {
  w.ToolBox = { showToast() {}, toast() {} };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {} }, matrix: { table() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {} },
    preset: { bar() {} },
  };
  w.i18nText = () => '';
  w.alert = () => {};
}

// ---------- N330：复制源只取 .code-row ----------
let copied = '';
const otp = new JSDOM(fs.readFileSync(`${root}/tools/it/otp-generator.html`, 'utf8'), {
  runScripts: 'dangerously', url: 'https://x.com/otp-generator.html',
  beforeParse(w) {
    stub(w);
    Object.defineProperty(w.navigator, 'clipboard', {
      value: { writeText(t) { copied = String(t); return Promise.resolve(); } }, configurable: true,
    });
  },
});
const wo = otp.window;
wo.document.getElementById('output').innerHTML = '<div class="code-row">123456</div><div class="timer">30 秒后刷新</div><div class="progress"><div class="progress-bar"></div></div>';
wo.copyResult();
check('N330 剪贴板只有 6 位数字（不含倒计时）', copied === '123456', JSON.stringify(copied));
check('N330 剪贴板不含「秒后刷新」', copied.indexOf('秒') < 0, JSON.stringify(copied));

// ---------- N331：改维度未重建矩阵 ----------
const mx = new JSDOM(fs.readFileSync(`${root}/tools/it/matrix-multiplier.html`, 'utf8'), {
  runScripts: 'dangerously', url: 'https://x.com/matrix-multiplier.html',
  beforeParse(w) { stub(w); },
});
const wm = mx.window, dm = wm.document;
dm.getElementById('ar').value = '2'; dm.getElementById('ac').value = '3';
dm.getElementById('br').value = '3'; dm.getElementById('bc').value = '2';
let thrown = null;
try { wm.calculate(); } catch (e) { thrown = String(e && e.message || e); }
const out = dm.getElementById('output').innerHTML || '';
check('N331 维度变更后计算不抛 null 解引用', thrown === null || !/null|undefined/.test(thrown), 'err=' + thrown);
check('N331 给出先构建或自动重建（结果区有有效内容）', /构建矩阵|result-matrix|维度不匹配/.test(out) || /result-matrix/.test(dm.getElementById('output').textContent || ''), 'out=' + out.slice(0, 120));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
