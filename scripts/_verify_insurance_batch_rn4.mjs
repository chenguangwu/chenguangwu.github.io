// 两态锁：R-N4 保费页「默认参数」预设与初始/重置不一致、负输入生成负保费、导出仍是历史摘要
// 用法：node scripts/_verify_insurance_batch_rn4.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();

const file = 'tools/insurance/premium-calc.html';
const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const ctx = { presets: null, csv: null, tableExport: false, toast: [], hist: [] };
const dom = new JSDOM(raw, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.ToolBox = {
      setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
      showToast(m) { ctx.toast.push(String(m)); }, downloadText() {}, showError() {}, copyText() {},
      formatNumber(n, d) {
        const v = Number(n);
        if (!isFinite(v)) return String(n);
        const s = v.toFixed(typeof d === 'number' ? d : 2);
        const p = s.split('.');
        p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        return p.join('.');
      }
    };
    w.i18nText = (k) => String(k);
    w.TBKit = {
      util: {
        isEn: () => false, diffBox() {}, exportTable() { ctx.tableExport = true; },
        exportCsv(name, rows) { ctx.csv = { name, rows }; return true; },
        formatNumber(n, d) { const v = Number(n); return isFinite(v) ? v.toFixed(typeof d === 'number' ? d : 2) : String(n); }
      },
      history: { record(r) { ctx.hist.push(r || {}); }, list: () => [], last: () => null, mount() {}, clear() {} },
      matrix: { table() {} },
      chart: { line() {}, bar() {} },
      preset: { bar(host, items) { ctx.presets = items; } }
    };
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);

const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const val = (id) => { const e = w.document.getElementById(id); return e ? String(e.value) : ''; };
const result = () => norm(w.document.getElementById('result').textContent);
const stat = () => norm(w.document.getElementById('statGrid').textContent);
const run = () => w.calc();
const reset = () => w.resetInputs();
const FIELDS = ['sumInsured', 'baseRate', 'age', 'job', 'term', 'payMode'];

console.log('— R-N4 保费测算 —');

// ① 守护：页面初始 / 重置口径
reset();
assert(/1,125\.00 ?应缴保费|1,125\.00/.test(result() + ' ' + stat()),
  `重置后应缴保费应为 1,125.00；实际=「${(result() + ' ' + stat()).slice(0, 170)}」`);
assert(/90\.0%/.test(stat()), `默认综合系数应为 90.0%；实际=「${stat().slice(0, 140)}」`);
const resetVals = FIELDS.map(val);

// ② 核心：预设「默认参数」必须与初始 / 重置逐字段一致
const ps = ctx.presets || [];
const def = ps.find(it => it && it.label === '默认参数');
assert(!!def, `应注册「默认参数」预设；实际=${ps.map(p => p && p.label).join('/')}`);
if (def) {
  const pv = FIELDS.map(k => String(def.values[k] == null ? '' : def.values[k]));
  const diff = FIELDS.filter((k, i) => pv[i] !== resetVals[i]).map((k, i) => k);
  assert(pv.every((x, i) => x === resetVals[i]),
    `「默认参数」预设应与初始/重置逐字段一致；不一致字段=${diff.join(',') || '无'} | 预设=${pv.join('/')} | 重置=${resetVals.join('/')}`);

  // 模拟点击预设：写 values → calc，结果必须与重置后逐字一致
  const before = result() + '|' + stat();
  FIELDS.forEach(k => set(k, def.values[k]));
  run();
  const after = result() + '|' + stat();
  assert(after === before,
    `点击「默认参数」后结果不应改变；重置=「${before.slice(0, 110)}」 预设=「${after.slice(0, 110)}」`);
}

// ③ 负保额必须拒绝，且不得输出负保费
reset(); set('sumInsured', -500000); run();
const e1 = result();
assert(/必须大于 ?0/.test(e1), `负保额应被拒绝；实际=「${e1.slice(0, 180)}」`);
assert(!/-1,125\.00|-1125\.00/.test(e1 + ' ' + stat()), `负保额不得输出 −1125.00 应缴保费；实际=「${(e1 + ' ' + stat()).slice(0, 180)}」`);
assert(stat() === '', `错误态应清空 statGrid 旧数值；实际=「${stat().slice(0, 140)}」`);

// ④ 负费率必须拒绝
reset(); set('baseRate', -2.5); run();
assert(/不能为负数/.test(result()), `负费率应被拒绝；实际=「${result().slice(0, 180)}」`);

// ⑤ 保额 0 与留空必须拒绝
reset(); set('sumInsured', 0); run();
assert(/必须大于 ?0（当前 0）/.test(result()), `保额 0 应被拒绝；实际=「${result().slice(0, 180)}」`);
reset(); set('baseRate', ''); run();
assert(/不能为空/.test(result()), `费率留空应被拒绝；实际=「${result().slice(0, 180)}」`);

// ⑥ 错误态不写历史、导出拦截
reset();
const histBefore = ctx.hist.length;
set('sumInsured', -500000); run();
assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);
ctx.csv = null; ctx.tableExport = false;
try { w.__premium_calcExport(); } catch (e) {}
assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);

// ⑦ 有效输入导出当前完整输入 + 保费分解
reset(); set('sumInsured', 800000); set('baseRate', 3); run();
ctx.csv = null; ctx.tableExport = false;
try { w.__premium_calcExport(); } catch (e) {}
if (ctx.csv) {
  const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
  assert(/保险金额 \(元\),800000\.00/.test(c), `CSV 应含当前保额；实际首段=${c.slice(0, 130)}`);
  assert(/基础费率 \(‰\),3/.test(c), `CSV 应含当前费率；实际首段=${c.slice(0, 130)}`);
  assert(/应缴保费 \(元\),2160\.00/.test(c), `CSV 应含当前应缴保费 2160.00；实际首段=${c.slice(0, 200)}`);
} else {
  assert(false, '有效输入后导出应调用 exportCsv');
}

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-N4 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
dom.window.close();
process.exit(failures ? 1 : 0);
