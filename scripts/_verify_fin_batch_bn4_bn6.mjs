// 两态锁：B-N4 折现回收期区分留空/显式零 + 贴现率 > −100% + 逐期折现明细与导出；B-N6 仓位页历史保存并先恢复计算模式
// 用法：node scripts/_verify_fin_batch_bn4_bn6.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();

function load(file) {
  const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  const ctx = { hist: [], csv: null, mountCb: null };
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
          exportCsv(name, rows) { ctx.csv = { name, rows }; return true; }
        },
        history: {
          record(o) { ctx.hist.unshift({ t: Date.now(), d: JSON.parse(JSON.stringify(o)) }); },
          list() { return ctx.hist.slice(); },
          last() { return ctx.hist.length ? ctx.hist[0].d : null; },
          mount(host, cb) { ctx.mountCb = cb; },
          clear() {}
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
        chart: { line() {}, bar() {} },
        preset: { bar() {} }
      };
    }
  });
  return { dom, w: dom.window, ctx };
}

// ══════════════════ B-N4：折现回收期 ══════════════════
console.log('— B-N4 折现回收期 —');
{
  const { dom, w, ctx } = load('tools/investment/discounted-payback.html');
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const run = () => w.calcTool();

  // 守护：默认参数结论与逐期明细
  set('cf0', -1000); set('cf1', 500); set('cf2', 500); set('cf3', 500); set('r', 10); run();
  const d0 = out();
  assert(/2\.35 年 ?折现回收期/.test(d0), `默认 −1000/500/500/500、r=10 应为 2.35 年；实际=「${d0.slice(0, 150)}」`);
  assert(/243\.43 ?累计折现现金流（末期）/.test(d0), `末期累计折现应为 243.43；实际=「${d0.slice(0, 150)}」`);
  assert(/折现因子/.test(d0) && /1\.1000/.test(d0), `结果区应附逐期折现因子明细（1.1000）；实际=「${d0.slice(0, 220)}」`);

  // B-N4-①：期初留空不得当成 0（旧实现 → 0.00 年）
  set('cf0', ''); run();
  const e1 = out();
  assert(/不能为空/.test(e1), `期初现金流留空应被拒绝并说明；实际=「${e1.slice(0, 150)}」`);
  assert(!/0\.00 年/.test(e1), `期初留空不得输出「0.00 年」这一伪结论；实际=「${e1.slice(0, 150)}」`);

  // B-N4-②：中间某期留空同样拒绝（旧实现按 0 参与，回收期被拉长却当作正常结果）
  set('cf0', -1000); set('cf2', ''); run();
  assert(/不能为空/.test(out()), `第2年现金流留空应被拒绝；实际=「${out().slice(0, 150)}」`);

  // B-N4-③：贴现率 −100% 数学无定义
  set('cf2', 500); set('r', -100); run();
  const e3 = out();
  assert(/必须大于 ?[\-−]100/.test(e3), `贴现率 −100% 应被明确拒绝；实际=「${e3.slice(0, 160)}」`);
  assert(!/未回收/.test(e3), `贴现率 −100% 不得输出「未回收」冒充结论；实际=「${e3.slice(0, 160)}」`);

  // B-N4-④：未回收时给出末期累计值而不是只显示「未回收」
  set('cf0', -99999); set('cf1', 100); set('cf2', 100); set('cf3', 100); set('r', 10); run();
  const e4 = out();
  assert(/未回收/.test(e4), `四期仍为负应输出「未回收」；实际=「${e4.slice(0, 150)}」`);
  assert(/无法回收|仍为负/.test(e4), `未回收时应说明原因与末期累计值；实际=「${e4.slice(0, 220)}」`);

  // B-N4-⑤：CSV 导出当前完整输入 + 逐期明细（旧实现导出的是历史摘要表）
  set('cf0', -5000); set('cf1', 2000); set('cf2', 2500); set('cf3', 2500); set('r', 12); run();
  assert(/2\.69 年 ?折现回收期/.test(out()), `−5000/2000/2500/2500、r=12 应为 2.69 年；实际=「${out().slice(0, 150)}」`);
  ctx.csv = null;
  try { w.__discounted_paybackExport(); } catch (e) {}
  const csv = ctx.csv;
  assert(!!csv, `应调用 exportCsv 导出当前明细；实际=${csv ? '已调用' : '未调用（仍用 exportTable 导历史摘要）'}`);
  if (csv) {
    const flat = csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/期初现金流 CF₀,-5000\.00/.test(flat), `CSV 应含当前期初现金流；实际首段=${flat.slice(0, 120)}`);
    assert(/折现回收期,2\.69 年/.test(flat), `CSV 应含折现回收期结论；实际首段=${flat.slice(0, 160)}`);
    assert(/折现因子/.test(flat) && /1779\.45/.test(flat), `CSV 应含逐期折现明细（1779.45）；实际首段=${flat.slice(0, 200)}`);
  }
  // 非法输入后不得复用旧明细导出
  set('r', -100); run();
  ctx.csv = null;
  try { w.__discounted_paybackExport(); } catch (e) {}
  assert(!ctx.csv, `非法输入后导出应给出提示而不是拿旧明细出 CSV；实际=${ctx.csv ? '仍导出了' : '已拦截'}`);

  dom.window.close();
}

// ══════════════════ B-N6：仓位管理历史模式 ══════════════════
console.log('— B-N6 仓位管理计算模式落库 —');
{
  const { dom, w, ctx } = load('tools/securities/position-sizing.html');
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  // 记录器有 1s 节流：测试里显式清零，确保每次点击都被记录（与真实用户间隔点击等价）
  const kick = () => { try { w.__position_sizing_last = 0; } catch (e) {} w.calc(); };

  // 凯利模式下一次计算 → 记录里必须带模式
  w.switchTab('kelly', null);
  set('winRate', 55); set('winLossRatio', 1.5); set('totalCapital', 100000); set('riskPerTrade', 2000);
  ctx.hist.length = 0;
  kick();
  const recKelly = ctx.hist.length ? ctx.hist[0].d : null;
  assert(!!recKelly, `凯利模式计算后应写入历史；实际条数=${ctx.hist.length}`);
  const mk = recKelly ? (recKelly['计算模式'] || recKelly['Mode']) : undefined;
  assert(mk === '凯利公式', `历史记录应保存计算模式（凯利公式）；实际=${mk === undefined ? '字段缺失' : mk}`);
  const kellyText = out();

  // 切到固定风险再算一条
  w.switchTab('fixed', null);
  set('capital2', 100000); set('riskPct', 2); set('entryPrice', 10); set('stopPrice', 9); set('targetPrice', 12); set('feeRate', 0.1);
  kick();
  const recFixed = ctx.hist.length ? ctx.hist[0].d : null;
  const mf = recFixed ? (recFixed['计算模式'] || recFixed['Mode']) : undefined;
  assert(mf === '固定风险', `固定风险记录应标注固定风险；实际=${mf === undefined ? '字段缺失' : mf}`);

  // 恢复凯利记录：必须先切模式，再用凯利公式重算，结果应与当时一致
  assert(typeof ctx.mountCb === 'function', `应挂载历史点选回调；实际=${typeof ctx.mountCb}`);
  if (typeof ctx.mountCb === 'function') {
    let threw = null;
    try { ctx.mountCb(recKelly); } catch (e) { threw = e; }
    assert(!threw, `点选凯利记录不应抛错；实际=${threw ? threw.message : '正常'}`);
    assert(w.currentTab === 'kelly', `恢复后应回到凯利模式；实际 currentTab=${w.currentTab}`);
    const after = out();
    assert(norm(after) === norm(kellyText), `恢复后结果应与该记录当时的凯利结果一致；实际=「${after.slice(0, 90)}」 vs 记录时「${kellyText.slice(0, 90)}」`);
  }

  // 导出：带当前完整输入与模式
  ctx.csv = null;
  try { w.__position_sizingExport(); } catch (e) {}
  const csv = ctx.csv;
  assert(!!csv, `应调用 exportCsv 导出当前完整输入；实际=${csv ? '已调用' : '未调用（仍用 exportTable 导历史摘要）'}`);
  if (csv) {
    const flat = csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/计算模式,凯利公式/.test(flat), `CSV 应含当前计算模式；实际首段=${flat.slice(0, 150)}`);
    assert(/胜率（%）/.test(flat) && /总资金（元）/.test(flat), `CSV 应含当前输入项；实际首段=${flat.slice(0, 200)}`);
  }

  dom.window.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] B-N4/B-N6 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] B-N4/B-N6 锁 PASS`);
