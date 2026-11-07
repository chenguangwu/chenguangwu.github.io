// 两态锁：R-N5 净趸缴参数校验与逐年明细、R-N6 结构化数值/错误不进历史、R-N7 深挖示例改用本页死亡给付模型
// 用法：node scripts/_verify_insurance_batch_rn5_rn7.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const file = 'tools/insurance/net-single-premium.html';
const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const hist = [];
const ctx = { chart: null };
const dom = new JSDOM(raw, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.ToolBox = {
      setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
      showToast() {}, downloadText() {}, showError() {}, copyText() {},
      formatNumber(n, d) { const v = Number(n); return isFinite(v) ? v.toFixed(typeof d === 'number' ? d : 2) : String(n); }
    };
    w.i18nText = (k) => String(k);
    w.TBKit = {
      util: {
        isEn: () => false, diffBox() {}, exportTable() {},
        exportCsv() { return true; }
      },
      history: {
        record(o) { hist.unshift({ t: Date.now(), d: JSON.parse(JSON.stringify(o)) }); },
        list() { return hist.slice(); },
        last() { return hist.length ? hist[0].d : null; },
        mount() {}, clear() {}
      },
      matrix: {
        table(host, opt) {
          const el = w.document.querySelector(host);
          if (!el) return;
          const rows = (opt && opt.rows) || [];
          let h = '<table><tbody>';
          for (const r of rows) h += '<tr>' + r.map(c => '<td>' + (c == null ? '' : c) + '</td>').join('') + '</tr>';
          el.innerHTML = h + '</tbody></table>';
        }
      },
      chart: { line(host, opt) { ctx.chart = opt; }, bar() {} },
      preset: { bar() {} }
    };
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const out = () => norm(w.document.getElementById('result').textContent);
// 记录器有 1s 节流，测试里清零以模拟用户间隔点击
const kick = () => { try { w.__net_single_premium_last = 0; } catch (e) {} w.calcTool(); };
const base = () => { set('B', 1000000); set('q', 0.01); set('i', 0.03); set('n', 10); };

// ── 守护：默认参数结论 + 逐年明细 ──
base(); kick();
const d0 = out();
assert(/81,763\.70 ?净趸缴保费/.test(d0), `默认 100万/1%/3%/10年 应为 81,763.70；实际=「${d0.slice(0, 120)}」`);
assert(/8\.18 ?占保额比例/.test(d0), `占保额比例应为 8.18%；实际=「${d0.slice(0, 120)}」`);
assert(/折现因子/.test(d0) && /0\.970874/.test(d0), `应附逐年折现因子明细（0.970874）；实际=「${d0.slice(0, 260)}」`);
assert(/生存至期末概率/.test(d0) && /0\.904382/.test(d0), `应给出生存至期末概率 0.904382；实际=「${d0.slice(0, 260)}」`);

// ── R-N5-①：死亡率越界必须拒绝 ──
base(); set('q', 1.5); kick();
const e1 = out();
assert(/必须在 ?0[–-]1 ?之间/.test(e1), `死亡率 1.5 应被拒绝（0≤q≤1）；实际=「${e1.slice(0, 160)}」`);
assert(!/\d{2,},\d{3}\.\d{2}/.test(e1), `死亡率越界不得输出任何保费金额；实际=「${e1.slice(0, 160)}」`);

// ── R-N5-②：保障年数非整数必须拒绝 ──
base(); set('n', 1.5); kick();
assert(/必须是正整数/.test(out()), `保障年数 1.5 应被拒绝；实际=「${out().slice(0, 160)}」`);

// ── R-N5-③：利率 −1 必须拒绝 ──
base(); set('i', -1); kick();
assert(/必须大于 ?[\-−]1/.test(out()), `年利率 −1 应被拒绝（v 为无穷）；实际=「${out().slice(0, 160)}」`);

// ── R-N5-④：保额为 0 必须拒绝 ──
base(); set('B', 0); kick();
assert(/不能为 ?0|必须大于 ?0/.test(out()), `保额 0 应被拒绝（分母守卫或 B>0 校验）；实际=「${out().slice(0, 160)}」`);
base(); set('B', -1000); kick();
assert(/必须大于 ?0/.test(out()), `保额为负应被 B>0 校验拒绝；实际=「${out().slice(0, 160)}」`);

// ── R-N5-⑤：零死亡率边界要单独说明 ──
base(); set('q', 0); kick();
assert(/年死亡率为 ?0/.test(out()), `q=0 应说明边界含义；实际=「${out().slice(0, 200)}」`);

// ── R-N6-①：历史记录里存结构化数值，趋势按数值画而不是 81 ──
base(); hist.length = 0; kick();
const rec = hist.length ? hist[0].d : null;
assert(!!rec, `默认计算应写入历史；实际条数=${hist.length}`);
assert(rec && String(rec['NSP数值']) === '81763.70', `历史应存结构化数值 81763.70；实际=${rec ? JSON.stringify(rec['NSP数值']) : '无记录'}`);
ctx.chart = null;
set('B', 2000000); kick();
assert(hist.length === 2, `第二次计算后应有 2 条历史；实际=${hist.length}`);
const chartData = (ctx.chart && ctx.chart.series && ctx.chart.series[0] && ctx.chart.series[0].data) || [];
assert(chartData.some(v => Number(v) > 10000), `趋势数据应为真实量级（>10000）；实际数据=${JSON.stringify(chartData)}`);
assert(!chartData.some(v => Math.abs(Number(v) - 81) < 0.5), `趋势不得出现被千分位截断的 81；实际数据=${JSON.stringify(chartData)}`);

// ── R-N6-②：必填守卫文案不得进历史（旧实现只过滤「请输入」，漏了「请填写」）──
base(); hist.length = 0; kick();
const before = hist.length;
set('B', ''); kick();
assert(hist.length === before, `留空导致的「请填写…」不得写入历史；实际 ${before} → ${hist.length}（末条=${hist.length ? JSON.stringify(hist[0].d) : '空'}）`);

// ── R-N7：深挖示例必须用本页死亡给付模型 ──
const dd = norm(w.document.querySelector('.deep-dive').textContent);
assert(/81,763\.70/.test(dd), `深挖示例应给出本页模型的 81,763.70；实际${/81,763\.70/.test(dd) ? '已给' : '缺失'}`);
assert(/死亡概率/.test(dd) && /折现赔付/.test(dd), `深挖示例应逐项写死亡概率与折现赔付；实际${/折现赔付/.test(dd) ? '已写' : '缺失'}`);
assert(/不可互换|不是同一对象/.test(dd), `深挖示例应说明确定年金与本页模型不可互换；实际${/不可互换|不是同一对象/.test(dd) ? '已声明' : '缺失'}`);

w.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] R-N5/R-N7 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] R-N5/R-N7 锁 PASS`);
