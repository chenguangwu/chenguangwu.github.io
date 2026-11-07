// 两态锁：B-F4 索提诺「倍数」分支去掉 ||1 兜底 + 下行标准差必须 > 0；B-F10 每次计算不再二次写「对比结果」历史
// 用法：node scripts/_verify_investment_batch_bf4_bf10.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const file = 'tools/investment/sortino-ratio.html';
const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const hist = [];          // 模拟 TBKit.history 存储，用于观测写入条数
const tableRows = [];     // 模拟 matrix.table 真实渲染，观测明细表是否被清空
let barCalls = 0;

const dom = new JSDOM(raw, {
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
          for (const r of rows) h += '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>';
          h += '</tbody></table>';
          el.innerHTML = h;
          tableRows.length = 0;
          for (const r of rows) tableRows.push([String(r[0]), String(r[1])]);
        }
      },
      chart: { line() {}, bar() { barCalls++; } },
      preset: { bar() {} }
    };
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);
const norm = (el) => ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const out = () => norm(w.document.getElementById('result'));
const run = () => w.calcTool();

// ── 守护：常规输入口径不变（15/3/6 ⇒ 2.000，倍数 6÷12=0.500）──
set('rp', 15); set('rf', 3); set('dd', 6); run();
assert(/2\.000 ?索提诺比率/.test(out()), `15/3/6 索提诺应为 2.000；实际=「${out().slice(0, 140)}」`);
assert(/0\.500 ?下行风险\/超额收益 倍数/.test(out()), `15/3/6 倍数应为 6÷12=0.500；实际=「${out().slice(0, 160)}」`);
assert(/12\.0000 ?超额收益/.test(out()), `超额收益应为 12.0000；实际=「${out().slice(0, 160)}」`);

// ── B-F4-①：超额收益为 0 时倍数必须显示「—」，不得用 ||1 兜底成 σd ──
set('rf', 15); run();
const z = out();
assert(!/6\.000 ?下行风险\/超额收益 倍数/.test(z), `超额收益 0 时不得输出假倍数 6.000（||1 兜底）；实际=「${z.slice(0, 160)}」`);
assert(/— ?下行风险\/超额收益 倍数/.test(z), `超额收益 0 时倍数应显示「—」；实际=「${z.slice(0, 160)}」`);
assert(/无定义/.test(z), `应说明倍数在超额收益为 0 时无定义；实际=「${z.slice(0, 200)}」`);
assert(/0\.000 ?索提诺比率/.test(z), `超额收益 0 时索提诺本身为 0.000（守护）；实际=「${z.slice(0, 160)}」`);

// ── B-F4-②：下行标准差为 0 / 负数必须拒绝，不得算出负比率 ──
set('rf', 3); set('dd', -6); run();
assert(/必须大于 0/.test(out()), `下行标准差 −6 应被拒绝（须大于 0）；实际=「${out().slice(0, 160)}」`);
assert(!/[\-\u2212]2\.000 ?索提诺比率/.test(out()), `下行标准差 −6 不得输出索提诺 −2.000；实际=「${out().slice(0, 160)}」`);

set('dd', 0); run();
assert(/必须大于 0|分母/.test(out()), `（守护）下行标准差 0 原本已被分母守卫拦住；实际=「${out().slice(0, 160)}」`);

// ── B-F4-③：非法输入时明细表不得残留上一次结果 ──
set('dd', -6); run();
const flat = tableRows.map(r => r.join(' ')).join(' | ');
assert(!/2\.000/.test(flat) && !/0\.500/.test(flat), `非法输入后明细表不得残留旧值；实际=${flat.slice(0, 160)}`);
assert(/请先填写有效/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 160)}`);

// ── B-F4-④：非法输入时敏感性图不得重绘（dd<0 会画出反向曲线）──
const before = barCalls;
set('rp', 15); set('rf', 3); set('dd', -6); run();
assert(barCalls === before, `下行标准差为负时不应重绘索提诺曲线（调用次数 ${before} → ${barCalls}）`);

// ── B-F10：每次计算只写 1 条历史，不再追加「对比结果」附属记录 ──
hist.length = 0;
set('rp', 15); set('rf', 3); set('dd', 6); run();
assert(hist.length === 1, `一次计算后历史应为 1 条（原实现为 2 条：页面摘要 + 对比结果）；实际=${hist.length}`);
const keys = hist.length ? Object.keys(hist[0].d) : [];
assert(keys.indexOf('对比结果') < 0 && keys.indexOf('Compare') < 0, `历史记录不应再含「对比结果」附属字段；实际字段=${keys.join(',')}`);
assert(keys.indexOf('rp') >= 0 && keys.indexOf('result') >= 0, `历史记录应保留可复原的输入与结果字段；实际字段=${keys.join(',')}`);

set('rp', 20); run();
assert(hist.length === 2, `第二次计算后历史应为 2 条（原实现 4 条）；实际=${hist.length}`);

w.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] B-F4/B-F10 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] B-F4/B-F10 锁 PASS`);
