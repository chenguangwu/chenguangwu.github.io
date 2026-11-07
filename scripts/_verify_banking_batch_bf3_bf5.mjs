// 两态锁：B-F3 税后等效收益率统一百分数口径 + 输入校验；B-F5 几何平均收益率序列统一百分数口径 + 逐项校验
// 用法：node scripts/_verify_banking_batch_bf3_bf5.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

function load(file) {
  const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  return new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast() {}, downloadText() {}, showError() {}, copyText() {}
      };
      w.i18nText = (k) => String(k);
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() {} },
        history: { record() {}, last: () => null, list: () => [], mount() {} },
        matrix: { table() {} }, chart: { line() {}, bar() {} }, preset: { bar() {} }
      };
    }
  });
}
const norm = (el) => ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };

// ───────── B-F3 税后等效收益率 ─────────
{
  const dom = load('tools/banking/tax-equivalent-yield.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const out = () => norm(w.document.getElementById('result'));
  const run = () => w.calcTool();

  // 1) 百分数口径：3% / 25% ⇒ TEY 4.000%、应税需高出 1.000 个百分点
  set(w, 'muni', 3); set(w, 'tax', 25); run();
  const a = out();
  assert(/4\.000 ?税后等效收益率 TEY/.test(a), `3% 免税 + 25% 税率应得 TEY 4.000%；实际=「${a.slice(0, 140)}」`);
  assert(/1\.000 ?应税需高出的百分点/.test(a), `应税需高出应为 1.000 个百分点；实际=「${a.slice(0, 140)}」`);
  assert(/25\.0 ?边际税率/.test(a), `边际税率应回显 25.0%；实际=「${a.slice(0, 140)}」`);

  // 2) 免税收益率 0 ⇒ 拒绝（原实现输出 0.000%）
  set(w, 'muni', 0); set(w, 'tax', 25); run();
  assert(/免税收益率须大于 0/.test(out()), `0 免税收益率应被拒绝；实际=「${out().slice(0, 120)}」`);

  // 3) 税率 100% ⇒ 明确拒绝（原实现显示「—」）
  set(w, 'muni', 3); set(w, 'tax', 100); run();
  assert(/边际税率须在 0–100% 之间/.test(out()), `100% 税率应被明确拒绝（分母为 0）；实际=「${out().slice(0, 120)}」`);

  // 4) 负税率 ⇒ 拒绝
  set(w, 'tax', -5); run();
  assert(/边际税率须在 0–100% 之间/.test(out()), `负税率应被拒绝；实际=「${out().slice(0, 120)}」`);

  // 5) 守护：税率 0 时 TEY 等于免税收益率（两态同值）
  set(w, 'muni', 3); set(w, 'tax', 0); run();
  assert(/3\.000 ?税后等效收益率 TEY/.test(out()), `税率 0 时 TEY 应等于 3.000%；实际=「${out().slice(0, 120)}」`);
  w.close();
}

// ───────── B-F5 几何平均收益率 ─────────
{
  const dom = load('tools/investment/geometric-mean-return.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const out = () => norm(w.document.getElementById('result'));
  const run = () => w.calcTool();

  // 1) 百分数序列：+20%、−10%、+15% ⇒ 7.49%
  set(w, 'r', '20, -10, 15'); run();
  const a = out();
  assert(/7\.49 ?几何平均收益率 g/.test(a), `20/−10/15（%）应得 7.49%；实际=「${a.slice(0, 140)}」`);
  assert(/1\.242000 ?累计增长倍数/.test(a), `累计增长倍数应为 1.20×0.90×1.15=1.242；实际=「${a.slice(0, 140)}」`);

  // 2) 非数字项 ⇒ 指出第几项（原实现静默「—」）
  set(w, 'r', 'abc, 10'); run();
  assert(/第 1 项「abc」不是有效数字/.test(out()), `非法项应被指名拒绝；实际=「${out().slice(0, 120)}」`);

  // 3) −100% ⇒ 拒绝（1+r=0）
  set(w, 'r', '10, -100'); run();
  assert(/第 2 项收益率 -100% 不合法/.test(out()), `−100% 单期应被拒绝；实际=「${out().slice(0, 120)}」`);

  // 4) 页面自查：计算说明示例已改为百分数写法
  const docText = norm(w.document.documentElement);
  assert(/10,20,−5 → 7\.83%/.test(docText), `计算说明示例应为「10,20,−5 → 7.83%」；实际${/0\.1,0\.2,−0\.05/.test(docText) ? '仍是小数写法' : '未找到百分数写法'}`);
  assert(/收益率序列 r（%/.test(docText), `输入标签应标注百分数口径；实际${/收益率序列 r（%/.test(docText) ? '已标注' : '未标注'}`);
  w.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] B-F3/B-F5 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] B-F3/B-F5 锁 PASS`);
