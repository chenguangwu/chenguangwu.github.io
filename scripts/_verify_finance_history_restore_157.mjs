// 第 1024 批复核失败（第 157 批历史恢复链）重做证据：五页真实点击历史快照恢复。
// 老板裁断：密码工具页不保存明文历史，password-generator-advanced 不重测恢复明文；
// 其余 calc-4 / compound-interest / credit-card-interest / irr-calculator / npv-calculator
// 必须在 JSDOM 中点击真实 TBKit.history.mount 渲染的历史项，逐项确认字段回填、结果重算与待处理输入不残留。
//
// 与旧脚本的区别：旧 batch115/116/118/143 只测记录、节流、导出、趋势，NPV 的“恢复”是重新输入；
// 本脚本先产生一条通过历史，再把输入与结果区写脏，点击历史项，断言输入与结果同时回到原快照。
//
// 用法：node scripts/_verify_finance_history_restore_157.mjs [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const verbose = process.argv.includes('--verbose');

const CASES = [
  { slug: 'calc-4', input: 'amount', dirty: '777777', resultIds: ['summary', 'res'] },
  {
    slug: 'compound-interest', input: 'principal', dirty: '77777',
    resultIds: ['totalFV', 'totalInvested', 'totalInterest', 'totalReturn', 'simpleFV', 'calcNotice', 'rule72', 'yearTableBody'],
  },
  { slug: 'credit-card-interest', input: 'billAmount', dirty: '77777', resultIds: ['resultBox', 'adviceBox'] },
  // irrWarn 正常态是 display:none，calc() 不会重写它；把哨兵写进去会制造假失败，故不纳入脏化锚点。
  { slug: 'irr-calculator', input: 'discountRate', dirty: '17', resultIds: ['irrValue', 'npvValue', 'irrDetail'] },
  { slug: 'npv-calculator', input: 'init', dirty: '77777', resultIds: ['stats', 'detail'] },
];

let pass = 0;
let fail = 0;
const failures = [];
const check = (slug, label, ok, detail = '') => {
  if (ok) {
    pass++;
    if (verbose) console.log(`PASS ${slug} ${label}`);
  } else {
    fail++;
    failures.push(`${slug} ${label}${detail ? ' | ' + detail : ''}`);
    console.log(`FAIL ${slug} ${label}${detail ? ' | ' + detail : ''}`);
  }
};
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();

function buildDom(slug, errors) {
  const file = path.join(ROOT, 'tools', 'finance', `${slug}.html`);
  const html = fs.readFileSync(file, 'utf8');
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => errors.push(String(e.message).slice(0, 180)));

  return new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      const byId = (id) => w.document.getElementById(String(id).replace(/^#/, ''));
      w.ToolBox = {
        showToast() {}, toast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {},
        escHtml: (s) => String(s == null ? '' : s),
        esc: (s) => String(s == null ? '' : s),
        csvCell: (v) => String(v == null ? '' : v),
        formatNumber: (v, d) => {
          const n = Number(v);
          return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v);
        },
        setResult: (id, value) => { const el = byId(id); if (el) el.innerHTML = value; },
        createTable: () => '',
        markInvalid() {}, clearInvalid() {},
        debounce: (fn) => fn,
        $: byId,
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = (b) => { w.__lastDownload = b.text; return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, key) => (key === 'createLinearGradient' || key === 'createRadialGradient')
          ? () => ({ addColorStop() {} }) : () => {},
      });
      // 关键：不桩化 TBKit.history.mount，直接加载生产 tool-kit.js，
      // 让恢复入口是真实的历史项按钮点击，而不是直接调用页面回调。
      w.eval(fs.readFileSync(path.join(ROOT, 'js', 'tool-kit.js'), 'utf8'));
    },
  });
}

function watchNodes(w, ids) {
  const out = [];
  ids.forEach((id) => {
    const el = w.document.getElementById(id);
    if (el) out.push(el);
  });
  return out;
}

function outputText(w, ids) {
  const parts = [];
  watchNodes(w, ids).forEach((el) => {
    const t = norm(el.textContent);
    if (t) parts.push(t);
  });
  return parts.join(' || ');
}

for (const c of CASES) {
  const errors = [];
  let dom;
  try {
    dom = buildDom(c.slug, errors);
    const w = dom.window;
    const d = w.document;
    await new Promise((resolve) => {
      if (d.readyState === 'complete') resolve();
      else w.addEventListener('load', resolve);
    });

    const input = d.getElementById(c.input);
    check(c.slug, '主输入存在', !!input);
    check(c.slug, '结果锚点齐全', watchNodes(w, c.resultIds).length === c.resultIds.length);
    check(c.slug, '加载无脚本异常', errors.length === 0, errors.join(' | '));
    if (!input || errors.length) continue;

    const valid = input.value;
    check(c.slug, '默认输入非空', !!valid);

    // 1) 真实输入事件产生一条通过历史
    input.value = valid;
    input.dispatchEvent(new w.Event('input', { bubbles: true }));
    await wait(1150);
    const records = w.TBKit.history.list();
    const first = records[0]?.d;
    check(c.slug, '历史记通过且快照带主输入', records.length >= 1 && first?.__tbScore === 1 && String(first?.[c.input]) === valid,
      JSON.stringify({ n: records.length, score: first?.__tbScore, snap: first?.[c.input], want: valid }));

    const historyBtn = d.querySelector('.tbk-history-item');
    check(c.slug, '真实历史项按钮已渲染', !!historyBtn);
    if (!historyBtn) continue;

    const before = outputText(w, c.resultIds);
    check(c.slug, '恢复前结果区有内容', before.length > 0);

    // 2) 把输入和结果区写脏，模拟“待处理输入 + 旧结果残留”；不清历史、不触发计算。
    input.value = c.dirty;
    watchNodes(w, c.resultIds).forEach((el) => { el.textContent = 'RESTORE_SENTINEL'; });

    // 3) 点击真实历史项，走生产恢复回调
    historyBtn.click();
    await wait(1150);

    check(c.slug, '恢复字段回到历史输入', input.value === valid,
      JSON.stringify({ got: input.value, want: valid }));
    const after = outputText(w, c.resultIds);
    check(c.slug, '恢复后结果按快照重算', !!after && after === before,
      JSON.stringify({ before: before.slice(0, 160), after: after.slice(0, 160) }));
    check(c.slug, '结果区无恢复前脏哨兵', after.indexOf('RESTORE_SENTINEL') < 0);

    const laterRecords = w.TBKit.history.list();
    check(c.slug, '脏输入未被写成历史',
      !laterRecords.some((r) => String(r?.d?.[c.input]) === c.dirty),
      JSON.stringify(laterRecords.map((r) => r?.d?.[c.input]).slice(0, 3)));
    check(c.slug, '延迟后恢复值未被节流覆盖', input.value === valid,
      JSON.stringify({ got: input.value, want: valid }));
  } catch (e) {
    fail++;
    failures.push(`${c.slug} 运行期异常：${String(e && e.message || e).slice(0, 180)}`);
    console.log(`FAIL ${c.slug} 运行期异常 | ${String(e && e.message || e).slice(0, 180)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

console.log(`\n=== 157 批五页历史快照恢复 | pass=${pass} fail=${fail} ===`);
if (failures.length) {
  console.log(failures.join('\n'));
  process.exit(1);
}
process.exit(0);
