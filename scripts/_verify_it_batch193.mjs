// 第193批 · IT-N110/N111/N112 base32 填充校验 + 解码历史 + 预设（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/base32-encode.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 120) : '')); }

let isEn = false;
let history = [];
let presetCfg = null;
let presetCb = null;
const alerts = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/base32-encode.html',
  beforeParse(w) {
    w.alert = m => alerts.push(String(m));
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: {
        isEn: () => isEn,
        exportTable() {}, diffBox() {}
      },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: {
        bar(sel, items, cb) { presetCfg = { sel, items }; presetCb = cb; }
      },
      history: {
        list() { return history; },
        last() { return history.length ? history[history.length - 1].d : null; },
        record(r) { history.push({ t: Date.now(), d: r }); },
        mount(el, cb) { /* 历史回填回调不参与本批断言 */ },
        clear() { history = []; }
      }
    };
  }
});
const w = dom.window;
const d = w.document;
function decode(v) {
  d.getElementById('input').value = v;
  d.getElementById('output').value = 'SENTINEL';
  alerts.length = 0;
  w.eval('__base32_encode_last=0;decode32()');
  return { out: d.getElementById('output').value, alert: alerts.join('|') };
}
function encode(v) {
  d.getElementById('input').value = v;
  d.getElementById('output').value = 'SENTINEL';
  w.eval('__base32_encode_last=0;encode32()');
  return d.getElementById('output').value;
}

// 判别1：填充数校验（IT-N110）
const r1 = decode('ME=======');
check('7 个填充被拒绝', r1.alert.indexOf('填充数无效') >= 0 && r1.out === 'SENTINEL', r1.alert || r1.out);
const r2 = decode('ME======');
check('6 个填充解出 a', r2.out === 'a' && !r2.alert, r2.alert || r2.out);
const r3 = decode('MZXW6YQ');
check('省略填充仍可解', r3.out === 'foob' && !r3.alert, r3.alert || r3.out);
const r4 = decode('MZXR');
check('残余位非零被拒绝', r4.alert.indexOf('填充位非零') >= 0 && r4.out === 'SENTINEL', r4.alert || r4.out);
const r5 = decode('A');
check('非法长度被拒绝', r5.alert.indexOf('长度无效') >= 0 && r5.out === 'SENTINEL', r5.alert || r5.out);
const r6 = decode('M=ZXW6YQ');
check('填充位置错误被拒绝', r6.alert.indexOf('填充位置无效') >= 0 && r6.out === 'SENTINEL', r6.alert || r6.out);
const r7 = decode('me======');
check('小写+规范填充可解', r7.out === 'a' && !r7.alert, r7.alert || r7.out);

// 判别2：解码历史与方向字段（IT-N111）
history = [];
decode('JBSWY3DP');
check('解码产生 1 条历史', history.length === 1, 'n=' + history.length);
check('解码历史方向=解码', history.length === 1 && history[0].d['方向'] === '解码', JSON.stringify(history[0] && history[0].d));
check('解码历史含输入与结果', history.length === 1 && history[0].d.input === 'JBSWY3DP' && history[0].d['结果'] === 'Hello', JSON.stringify(history[0] && history[0].d));
history = [];
encode('Hello');
check('编码历史方向=编码', history.length === 1 && history[0].d['方向'] === '编码', JSON.stringify(history[0] && history[0].d));
history = [];
decode('JBSWY3DP');
decode('JBSWY3DP');
check('同输入同方向不重复记历史', history.length === 1, 'n=' + history.length);

// 判别3：预设非空且回调真能跑（IT-N112）
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
check('预设宿主正确', presetCfg && presetCfg.sel === '#base32_encodePresets', presetCfg && presetCfg.sel);
check('预设 3 条', presetCfg && presetCfg.items.length === 3, presetCfg && presetCfg.items.map(x => x.label).join(' / '));
check('预设含中英标签', presetCfg && presetCfg.items.every(x => !!x.label && !!x.labelEn), JSON.stringify(presetCfg && presetCfg.items.map(x => x.labelEn)));
check('预设回调已注册', typeof presetCb === 'function');
if (presetCb) {
  d.getElementById('input').value = '中文测试';
  d.getElementById('output').value = 'SENTINEL';
  presetCb();
}
check('预设回调真能编码', d.getElementById('output').value === '4S4K3ZUWQ7TLLC7IV6KQ====', d.getElementById('output').value);
if (presetCb) {
  d.getElementById('input').value = 'JBSWY3DP';
  d.getElementById('output').value = 'SENTINEL';
  presetCb();
}
check('预设回调真能解码', d.getElementById('output').value === 'Hello', d.getElementById('output').value);

// 判别4：英文态错误消息走英译 helper
isEn = true;
const enErr = decode('ME=======');
check('英文态填充错误为英文', enErr.alert.indexOf('Invalid Base32 padding count') >= 0 && enErr.alert.indexOf('填充数') < 0, enErr.alert);
isEn = false;
const zhAgain = decode('ME=======');
check('切回中文态仍为中文', zhAgain.alert.indexOf('填充数无效') >= 0, zhAgain.alert);

// 判别5：状态链 合法 → 非法 → 恢复
check('状态链合法', decode('ME======').out === 'a');
check('状态链非法', decode('ME=======').out === 'SENTINEL');
check('状态链恢复', decode('ME======').out === 'a');

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
