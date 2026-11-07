// 两态锁：R-H4 两全保险深挖示例按本页模型重算 / R-H5 q>1、非整数年数等参数边界
// 用法：node scripts/_verify_insurance_batch_rh4_rh5.mjs [--head]
// 当前态应全部 PASS；--head 读取 git show HEAD:<file>（提交前版本）应出现 FAIL。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const CJK = /[一-鿿　-〿＀-￯]/;
// content_deepdive.json >1MB，execSync 默认 1MB maxBuffer 会 ENOBUFS；两态都要能读完
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');
const json = (f) => JSON.parse(rd(f));

const NEW_T = '保额 100 万、q=1%、3%、20 年';
const NEW_B = '按本页逐年模型：身故给付现值 136,786.19 元（Σ B·vᵗ·ₜp·q）；20 年生存概率 0.817907，满期给付现值 452,855.24 元（B·v²⁰·ₙp）；合计 589,641.43 元 ÷ 期初年金系数 14.877475 = 年缴保费 39,633.17 元。若省略生存概率，满期现值会写成 55.37 万、年保费约 4.7 万，比本页高约 19%。';
const OLD_T = '保额 100 万、3%、20 年';
const OLD_B = '身故现值 = 100万×A₁ₙ(3%,20) ≈ 100万×0.1488 = 14.88万；满期现值 = 100万×v²⁰ = 100万×0.5537 = 55.37万；两全现值 ≈ 70.25万，分摊为年保费约 4.7万/年。';
const NEW_FQ_HEAD = '校验：四项必填且为合法数值（留空不再按 0 兜底）；保额 >0、0 ≤ q < 1';

function load(file) {
  const raw = rd(file);
  const ctx = { csv: null, tableExport: false, table: [], hist: [], toast: [] };
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast(m) { ctx.toast.push(String(m)); }, showError() {}, downloadText() {}, copyText() {},
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
          isEn: () => false, diffBox() {}, exportTable() { ctx.tableExport = true; },
          exportCsv(name, rows) { ctx.csv = { name, rows }; return true; }
        },
        history: { record(r) { ctx.hist.push(r || {}); }, list: () => [], last: () => null, mount() {}, clear() {} },
        matrix: {
          table(host, opt) {
            const el = w.document.querySelector(host);
            const rows = (opt && opt.rows) || [];
            ctx.table = rows.map(r => (r || []).map(c => (c == null ? '' : String(c))).join(' | '));
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
  return { dom, w: dom.window, ctx, raw };
}
const ready = async (w) => {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 60));
};
const setVal = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };

// ══════════ R-H5：参数边界与错误态 ══════════
console.log('— R-H5 两全保险参数边界 —');
{
  const { dom, w, ctx, raw } = load('tools/insurance/endowment-premium.html');
  await ready(w);
  const out = () => norm(w.document.getElementById('result') && w.document.getElementById('result').textContent);
  const rows = () => (w.document.querySelectorAll('#endowment_premiumTable tbody tr') || []).length;
  const reset = () => { w.resetForm(); if ('__endowment_premium_last' in w) w.__endowment_premium_last = 0; };

  // 守护：默认结果（含本批新增的期末生存概率）
  reset();
  const d = out();
  assert(/39,633\.17/.test(d) && /136,786\.19/.test(d) && /452,855\.24/.test(d),
    `默认态应输出本页模型数值 39,633.17 / 136,786.19 / 452,855.24；实际=「${d.slice(0, 180)}」`);
  assert(/0\.817907 ?期末生存概率/.test(d), `结果区应给出期末生存概率 0.817907；实际=「${d.slice(0, 180)}」`);

  // 公式框明确写出新校验
  const fq = norm(w.document.querySelector('.formula-eq') && w.document.querySelector('.formula-eq').textContent);
  assert(fq.includes(NEW_FQ_HEAD), `公式框应写明新校验口径；实际=「${fq.slice(-160)}」`);
  assert(/0 ≤ q < 1/.test(fq) && /1 到 1000 之间的正整数/.test(fq), '公式框应写明 q 上界与年数正整数约束');

  // 五种非法输入都应拒绝，且不得产出扭曲数值
  const bad = [
    ['q=1.5', 'q', 1.5, '年死亡率 q 必须在 0（含）到 1（不含）之间'],
    ['n=1.5', 'n', 1.5, '保险年数必须是 1 到 1000 之间的正整数'],
    ['n=1001', 'n', 1001, '保险年数必须是 1 到 1000 之间的正整数'],
    ['B=0', 'B', 0, '保额必须大于 0'],
    ['i=-1.5', 'i', -1.5, '年利率 i 必须大于'],
  ];
  for (const [name, id, v, want] of bad) {
    reset(); setVal(w, id, v); w.calcTool();
    const o = out();
    assert(o.includes(want), `${name} 应被拒绝（${want}）；实际=「${o.slice(0, 150)}」`);
    assert(!/两全年保费 \(元\)|Infinity|NaN/.test(o), `${name} 拒绝态不得输出主结果卡；实际=「${o.slice(0, 150)}」`);
  }

  // 错误态：清旧明细表 + 不写历史 + 拦截导出
  reset(); setVal(w, 'q', 1.5);
  const histBefore = ctx.hist.length;
  w.calcTool();
  const flat = (ctx.table || []).join(' || ');
  assert(/请先修正输入/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 180)}`);
  assert(rows() <= 2, `非法输入后旧明细行应被清空；实际行数=${rows()}`);
  assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);
  ctx.csv = null; ctx.tableExport = false;
  try { w.__endowment_premiumExport(); } catch (e) {}
  assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);
  assert(/请先完成一次有效计算/.test((ctx.toast || []).join(' ')), '拦截时应给出明确提示');

  // 有效态导出：当前完整输入 + 结果 + 逐期明细
  reset(); setVal(w, 'B', 250000); w.calcTool();
  ctx.csv = null; ctx.tableExport = false;
  try { w.__endowment_premiumExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/保额 \(元\),250000/.test(c), `CSV 应含当前保额 250000；实际首段=${c.slice(0, 150)}`);
    assert(/两全年保费 \(元\)/.test(c) && /期末生存概率/.test(c), `CSV 应含核心结果与期末生存概率；实际首段=${c.slice(0, 180)}`);
    assert(ctx.csv.rows.length >= 30, `CSV 应含 20 期逐期明细（≥30 行）；实际=${ctx.csv.rows.length}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }
  dom.window.close();
}

// ══════════ R-H4：深挖示例与本页模型同口径 ══════════
console.log('— R-H4 两全保险深挖示例 —');
{
  const { dom, w } = load('tools/insurance/endowment-premium.html');
  await ready(w);
  const title = norm(w.document.querySelector('.dd-ex-title') && w.document.querySelector('.dd-ex-title').textContent);
  const body = norm(w.document.querySelector('.dd-ex-body') && w.document.querySelector('.dd-ex-body').textContent);
  assert(title === NEW_T, `算例标题应写明 q=1%；实际=「${title}」`);
  assert(body === NEW_B, `算例正文应按本页逐年模型给出数值；实际=「${body.slice(0, 170)}」`);
  assert(!/A₁ₙ|14\.88万|70\.25万/.test(title + ' ' + body), `算例不得残留旧的「不乘生存概率」口径；实际=「${(title + ' ' + body).slice(0, 170)}」`);
  for (const k of ['136,786.19', '452,855.24', '589,641.43', '14.877475', '39,633.17', '0.817907']) {
    assert(body.includes(k), `算例应含可复核算值 ${k}`);
  }

  // 示例数值必须等于默认输入下主计算的结果
  w.resetForm();
  const d = norm(w.document.getElementById('result') && w.document.getElementById('result').textContent);
  for (const k of ['39,633.17', '136,786.19', '452,855.24', '0.817907']) {
    assert(d.includes(k) && body.includes(k), `示例 ${k} 应与页面默认计算一致（结果区=「${d.slice(0, 120)}」）`);
  }

  // 英文 map 键 = 中文源串、值无 CJK、旧键已删
  const m = json('i18n/tools/en/insurance/endowment-premium.json').map;
  assert(!!m[NEW_T] && !CJK.test(m[NEW_T]), `工具页英文 map 应含新标题键；实际=${m[NEW_T]}`);
  assert(!!m[NEW_B] && !CJK.test(m[NEW_B]), `工具页英文 map 应含新正文键；实际=${String(m[NEW_B]).slice(0, 80)}`);
  assert(!m[OLD_T] && !m[OLD_B], '工具页英文 map 不得残留旧示例键');
  const fq = norm(w.document.querySelector('.formula-eq') && w.document.querySelector('.formula-eq').textContent);
  assert(!!m[fq] && !CJK.test(m[fq]), `英文 map 应含与 HTML 逐字一致的新 formula-eq 键；实际=${String(m[fq]).slice(0, 80)}`);

  // 指南静态页 + guide 英文 map（正文键带前导「：」）
  const gd = new JSDOM(rd('guides/endowment-premium-guide.html'));
  const gtxt = norm(gd.window.document.body.textContent);
  assert(gtxt.includes(NEW_T) && gtxt.includes('39,633.17'), `指南页算例应同步新数值；实际片段=「${gtxt.slice(gtxt.indexOf('算例参考'), gtxt.indexOf('算例参考') + 160)}」`);
  assert(!gtxt.includes('14.88万') && !gtxt.includes('70.25万'), '指南页不得残留旧算例');
  const gm = json('i18n/guides/endowment-premium-guide.json').map;
  assert(!!gm[NEW_T] && !CJK.test(gm[NEW_T]), `指南英文 map 应含新标题键；实际=${gm[NEW_T]}`);
  assert(!!gm['：' + NEW_B] && !CJK.test(gm['：' + NEW_B]), `指南英文 map 应含「：+新正文」键；实际=${String(gm['：' + NEW_B]).slice(0, 80)}`);
  assert(!gm[OLD_T] && !gm['：' + OLD_B], '指南英文 map 不得残留旧示例键');

  // 生成真源与页面、指南三者一致
  const dd = json('i18n/tools/content_deepdive.json')['insurance/endowment-premium']['examples'][0];
  assert(dd.title === NEW_T && dd.body === NEW_B, 'content_deepdive.json 的示例应与页面算例逐字一致');
  assert(rd('scripts/apply_insurance.py').includes(NEW_T), '生成脚本 apply_insurance.py 应同步新示例，防重跑回退');
  dom.window.close();
  gd.window.close();
}

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-H4/R-H5 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
