// 两态锁：R-H11 IBNR 深挖示例与因子法同口径 / R-H6 均衡年保费利率结论方向
// 用法：node scripts/_verify_insurance_batch_rh11_rh6.mjs [--head]
// 当前态应全部 PASS；--head 读取 git show HEAD:<file>（提交前版本）应出现 FAIL。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const CJK = /[一-鿿　-〿＀-￯]/;
const rd = (f) => head ? execSync(`git show HEAD:${f}`).toString() : fs.readFileSync(f, 'utf8');
const json = (f) => JSON.parse(rd(f));

const NEW_T = '已报案 400 万、发展因子 1.25';
const NEW_B = 'IBNR = 已报案 400 万 × (1.25 − 1) = 100 万；最终赔款估计 = 400 万 × 1.25 = 500 万。因子 >1 时与「已发生 − 已报告」等价（已发生即终极赔款 500 万）。';
const OLD_T = '已发生 400 万、已报告 320 万';
const OLD_B = 'IBNR = 400−320 = 80 万。即已发生未报告赔款约 80 万。';
const NEW_NOTE = '固定净趸缴保费时，利率上升使年金现值系数变小，均衡年保费随之上升。';
const OLD_NOTE = '年保费随利率上升而下降。';

function load(file) {
  const raw = rd(file);
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast() {}, showError() {}, downloadText() {}, copyText() {},
        formatNumber(n, d) {
          const v = Number(n);
          if (!isFinite(v)) return String(n);
          const s = v.toFixed(typeof d === 'number' ? d : 2);
          const p = s.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); return p.join('.');
        }
      };
      w.i18nText = (k) => String(k);
      w.TBKit = {
        util: {
          isEn: () => false, diffBox() {}, exportTable() {},
          exportCsv() { return true; },
          formatNumber(n, d) { return w.ToolBox.formatNumber(n, d); }
        },
        history: { record() {}, list: () => [], last: () => null, mount() {}, clear() {} },
        matrix: {
          table(host, opt) {
            const el = w.document.querySelector(host);
            const rows = (opt && opt.rows) || [];
            if (el) el.innerHTML = '<table><tbody>' + rows.map(r =>
              '<tr>' + r.map(c => '<td>' + (c == null ? '' : c) + '</td>').join('') + '</tr>'
            ).join('') + '</tbody></table>';
          }
        },
        chart: { line() {}, bar() {} },
        preset: { bar() {} }
      };
    }
  });
  return { dom, w: dom.window, raw };
}
const ready = async (w) => {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 60));
};
const setVal = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };

// ══════════ R-H11：IBNR 深挖示例口径 ══════════
console.log('— R-H11 IBNR 深挖示例 —');
{
  const { dom, w } = load('tools/insurance/ibnr-reserve.html');
  await ready(w);
  const title = norm(w.document.querySelector('.dd-ex-title') && w.document.querySelector('.dd-ex-title').textContent);
  const body = norm(w.document.querySelector('.dd-ex-body') && w.document.querySelector('.dd-ex-body').textContent);
  assert(title === NEW_T, `工具页算例标题应与因子法一致；实际=「${title}」`);
  assert(body === NEW_B, `工具页算例正文应与因子法一致；实际=「${body.slice(0, 160)}」`);
  assert(!/400−320|80 万|已报告 320 万/.test(title + ' ' + body), `算例不得再出现「已发生−已报告」的 80 万口径；实际=「${(title + ' ' + body).slice(0, 160)}」`);
  assert(/1\.25 − 1|100 万|500 万/.test(body), `算例应给出可复核的 1.25−1 / 100 万 / 500 万；实际=「${body.slice(0, 160)}」`);

  // 英文 map：键必须逐字等于页面中文串，值不得泄漏 CJK
  const m = json('i18n/tools/en/insurance/ibnr-reserve.json').map;
  assert(!!m[NEW_T] && !CJK.test(m[NEW_T]), `工具页英文 map 应含新标题键且值无 CJK；实际=${m[NEW_T]}`);
  assert(!!m[NEW_B] && !CJK.test(m[NEW_B]), `工具页英文 map 应含新正文键且值无 CJK；实际=${String(m[NEW_B]).slice(0, 80)}`);
  assert(!m[OLD_T] && !m[OLD_B], '工具页英文 map 不得残留旧示例键');

  // guide 静态页与 guide 英文 map（正文键带前导「：」）
  const gd = new JSDOM(rd('guides/ibnr-reserve-guide.html'));
  const gtxt = norm(gd.window.document.body.textContent);
  assert(gtxt.includes(NEW_T), `指南页算例应同步新标题；实际片段=「${gtxt.slice(gtxt.indexOf('算例参考'), gtxt.indexOf('算例参考') + 120)}」`);
  assert(!gtxt.includes(OLD_T) && !gtxt.includes('400−320'), '指南页算例不得残留旧口径');
  const gm = json('i18n/guides/ibnr-reserve-guide.json').map;
  assert(!!gm[NEW_T] && !CJK.test(gm[NEW_T]), `指南英文 map 应含新标题键；实际=${gm[NEW_T]}`);
  assert(!!gm['：' + NEW_B] && !CJK.test(gm['：' + NEW_B]), `指南英文 map 应含「：+新正文」键；实际=${String(gm['：' + NEW_B]).slice(0, 80)}`);
  assert(!gm[OLD_T] && !gm['：' + OLD_B], '指南英文 map 不得残留旧示例键');

  // 运行期一致性：示例数字必须等于默认输入下主计算的结果
  setVal(w, 'reported', 4000000); setVal(w, 'factor', 1.25);
  try { w.calcTool(); } catch (e) {}
  const out = norm(w.document.getElementById('result') && w.document.getElementById('result').textContent);
  assert(/1,000,000\.00/.test(out), `默认 400 万 × 1.25 应得 IBNR 1,000,000.00（示例 100 万）；实际=「${out.slice(0, 180)}」`);
  assert(/5,000,000\.00/.test(out), `最终赔款估计应为 5,000,000.00（示例 500 万）；实际=「${out.slice(0, 180)}」`);
  dom.window.close();
  gd.window.close();
}

// ══════════ R-H6：均衡年保费利率结论方向 ══════════
console.log('— R-H6 利率结论表述 —');
{
  const { dom, w, raw } = load('tools/insurance/level-premium-life.html');
  await ready(w);
  const lis = Array.from(w.document.querySelectorAll('.tool-notes ul li')).map(e => norm(e.textContent));
  assert(lis.includes(NEW_NOTE), `计算说明第 2 条应改为「利率上升→年金因子变小→年保费上升」；实际=${JSON.stringify(lis)}`);
  assert(!lis.some(x => x.includes(OLD_NOTE)), `计算说明不得再写「${OLD_NOTE}」；实际=${JSON.stringify(lis)}`);
  const fq = norm(w.document.querySelector('.formula-eq') && w.document.querySelector('.formula-eq').textContent);
  assert(/利率越高年金现值系数越小、均衡年保费越高/.test(fq), `公式框应保留正确的利率方向；实际=「${fq.slice(-90)}」`);
  assert(raw.includes('均衡年保费随缴费年数递减并趋饱和') && !raw.includes('均衡年保费随缴费年数反比下降'),
    '图表标题应改为「递减并趋饱和」，不得再用不准确的「反比下降」');
  const lm = json('i18n/tools/en/insurance/level-premium-life.json').map;
  assert(!!lm[NEW_NOTE] && !CJK.test(lm[NEW_NOTE]), `英文 map 应含新 note 键且值无 CJK；实际=${lm[NEW_NOTE]}`);
  assert(!lm[OLD_NOTE], '英文 map 不得残留旧 note 键');

  // 运行期方向实证：i=3% → 5713.34，i=6% → 7410.69，年保费随利率上升
  const out = () => norm(w.document.getElementById('result') && w.document.getElementById('result').textContent);
  setVal(w, 'nsp', 85000); setVal(w, 'n', 20); setVal(w, 'i', 0.03);
  try { w.calcTool(); } catch (e) {}
  const r3 = out();
  setVal(w, 'i', 0.06);
  try { w.calcTool(); } catch (e) {}
  const r6 = out();
  const pick = (s) => { const m = s.match(/([\d,]+\.\d{2})\s*均衡年保费/); return m ? Number(m[1].replace(/,/g, '')) : NaN; };
  const p3 = pick(r3), p6 = pick(r6);
  assert(/5,713\.34/.test(r3), `i=3% 时均衡年保费应为 5,713.34；实际=「${r3.slice(0, 150)}」`);
  assert(/7,410\.69/.test(r6), `i=6% 时均衡年保费应为 7,410.69；实际=「${r6.slice(0, 150)}」`);
  assert(isFinite(p3) && isFinite(p6) && p6 > p3, `运行期应证实 p(6%)=${p6} > p(3%)=${p3}`);
  // 说明文案与运行期方向一致（避免「改了文案但方向又写反」）
  assert(/均衡年保费随之上升/.test(NEW_NOTE) && p6 > p3, '计算说明的上升结论必须与运行期数值方向一致');
  dom.window.close();
}

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-H11/R-H6 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
