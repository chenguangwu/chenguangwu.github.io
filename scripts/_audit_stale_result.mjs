// G10 审计：输入失效后结果区是否残留旧结果（逐输入探测，避免跨字段约束误判）。
//
// 判据（每个输入 el 单独测，其余保持页面默认值 = 一个真实有效结果 R0）：
//   Rc = 把 el 清空后重算   Rd = 把 el 改成明显不同的值后重算
//   Rc === R0 且 Rd !== R0  ⇒ el 是参与计算的必填项，但清空后结果毫无变化 ⇒ 残留旧结果（STALE）
//   Rc === R0 且 Rd === R0  ⇒ el 根本没参与计算 ⇒ 死输入，不在本专项判定（unused）
//
// 用法：node scripts/_audit_stale_result.mjs --list=<file> [--json=/tmp/out.json]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';

const argv = process.argv.slice(2);
const listArg = argv.find((a) => a.startsWith('--list='));
const jsonArg = argv.find((a) => a.startsWith('--json='));
if (!listArg) { console.error('usage: node scripts/_audit_stale_result.mjs --list=<file>'); process.exit(2); }
const files = fs.readFileSync(listArg.slice(7), 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);

const anyStub = () => new Proxy({}, {
  get(t, k) { if (k === 'then') return undefined; return () => ({}); },
  set() { return true; },
});

function build(raw, url) {
  return new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = {
        copyText() {}, showToast() {}, formatNumber: (n) => String(n),
        escHtml: (s) => String(s == null ? '' : s), esc: (s) => String(s == null ? '' : s),
        // setResult / markInvalid / clearInvalid 是站点真实 API（js/common.js:2114），
        // 大量页面的 __tbInputGuard 靠它把「请输入…」写进结果区。桩缺它会让 calc() 抛错，
        // 结果区一动不动 ⇒ 被误判成「清空输入后结果残留」（本次实测踩过）。
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid(id) { const el = w.document.getElementById(id); if (el) el.classList.add('is-invalid'); },
        clearInvalid(id) { const el = w.document.getElementById(id); if (el) el.classList.remove('is-invalid'); },
        createTable: (h, r) => '<table>' + String(h) + String(r) + '</table>',
        debounce: (fn) => function (...a) { return fn.apply(this, a); },
        $: (id) => w.document.getElementById(id),
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      const ctx = new Proxy({}, {
        get(t, k) {
          if (k === 'canvas') return { width: 600, height: 300 };
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          return () => {};
        },
        set() { return true; },
      });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctx; } catch (e) {}
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} },
        matrix: anyStub(), chart: anyStub(), preset: anyStub(),
      };
    },
  });
}

const ready = (w) => new Promise((res) => {
  if (w.document.readyState === 'complete') return res();
  w.addEventListener('load', res);
  setTimeout(res, 3000);
});

const TEXTY = ['text', 'number', 'search', 'url', 'email', 'password', 'date', 'time', 'datetime-local', 'tel'];
const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim();
const ERRORISH = /请(输入|填写|选择|勾选|先)|无效|不合法|应在|不能为|必须|⚠|❌|失败|错误|Invalid|Please|must be/i;

// 结果区候选：站点统一容器。最终取「真正随输入变化」的那个（见主循环），
// 因为有些页的 .result-box 里还塞了静态段（截面表/示意图），直接取会把静态文本当结果。
function boxCandidates(w) {
  const out = [];
  for (const el of [w.document.querySelector('.result-box'), w.document.getElementById('result'),
    w.document.getElementById('output'), w.document.getElementById('res')]) {
    if (el && !out.includes(el)) out.push(el);
  }
  return out;
}

// 页面主计算入口：优先取 on* 内联回调名，其次退化为 calc/calcTool/calculate/compute。
function calcEntry(raw) {
  const names = [];
  const re = /on(?:input|change|keyup|click)="([A-Za-z_$][\w$]*)\(/g;
  let m; while ((m = re.exec(raw))) if (!names.includes(m[1])) names.push(m[1]);
  for (const d of ['calcTool', 'calc', 'calculate', 'compute', 'update', 'run']) {
    if (new RegExp(`function ${d}\\s*\\(|${d}\\s*=\\s*function`).test(raw) && !names.includes(d)) names.push(d);
  }
  return names;
}

const rows = [];
let skipNoBox = 0, skipNotResult = 0, pass = 0, stale = 0, err = 0;

for (const f of files) {
  if (!fs.existsSync(f)) continue;
  const raw = fs.readFileSync(f, 'utf8');
  let dom;
  try { dom = build(raw, `https://x.test/${f}`); }
  catch (e) { err++; rows.push({ f, v: 'ERR', why: String((e && e.message) || e).slice(0, 80) }); continue; }
  const w = dom.window;
  try {
    await ready(w);
    const cands = boxCandidates(w);
    if (!cands.length) { skipNoBox++; continue; }
    const els = [...w.document.querySelectorAll('input')]
      .filter((e) => TEXTY.includes(String(e.type || 'text').toLowerCase()) && e.id);
    if (!els.length) { skipNoBox++; continue; }

    const entry = calcEntry(raw);
    const runCalc = () => { for (const n of entry) { try { w.eval(n + '()'); } catch (e2) {} } };
    const fire = (e) => {
      try { e.dispatchEvent(new w.Event('input', { bubbles: true })); } catch (e2) {}
      try { e.dispatchEvent(new w.Event('change', { bubbles: true })); } catch (e2) {}
    };

    const orig = els.map((e) => e.value);
    const altOf = (v) => (/^-?\d+(\.\d+)?$/.test(v) ? String(parseFloat(v) * 2 || 7) : (v ? v + 'X' : '7'));
    const setAll = (fn) => { for (let i = 0; i < els.length; i++) els[i].value = fn(i, String(orig[i] || '')); };
    const texts = () => cands.map((c) => norm(c.textContent));

    // 先取默认态，再全量改值：挑「文本真的变了」的容器作为结果区。
    setAll((i, v) => v); runCalc();
    const tDef = texts();
    setAll((i, v) => altOf(v)); runCalc();
    const tAlt = texts();
    setAll((i, v) => v); runCalc();

    let ci = -1, best = 0;
    for (let k = 0; k < cands.length; k++) {
      const d = tDef[k] === tAlt[k] ? 0 : Math.abs(tAlt[k].length - tDef[k].length) + 1;
      if (d > best) { best = d; ci = k; }
    }
    if (ci < 0) { skipNotResult++; continue; }        // 候选容器都不随输入变 ⇒ 判不出结果区
    const box = cands[ci];
    const R0 = tDef[ci];
    if (!/\d/.test(R0) || ERRORISH.test(R0)) { skipNotResult++; continue; }
    const staleFields = [];
    let unused = 0;

    for (let i = 0; i < els.length; i++) {
      const el = els[i];
      const v = String(orig[i] || '');
      const alt = /^-?\d+(\.\d+)?$/.test(v) ? String(parseFloat(v) * 2 || 7) : (v ? v + 'X' : '7');

      // ① 先改成明显不同的值 ⇒ R1（证明该字段确实参与计算）
      el.value = alt; fire(el); runCalc();
      const R1 = norm(box.textContent);
      // ② 从「改值态」直接清空 ⇒ R2
      el.value = ''; fire(el); runCalc();
      const R2 = norm(box.textContent);
      // ③ 复原
      el.value = v; fire(el); runCalc();

      if (R1 === R0) { unused++; continue; }        // 改值也不影响结果 ⇒ 死输入，不在本专项
      // 关键：清空后结果若仍等于「改值态」的文本，说明清空根本没触发重算 ⇒ 残留旧结果。
      // 反例①：清空后走 `|| 默认值` 兜底，结果回到默认态文本（R2 === R0 且 ≠ R1）⇒ 不算残留。
      // 反例②：__tbInputGuard 对「空」与「格式错」给同一条提示（R2 === R1 但都是错误提示）⇒ 不算残留。
      if (R2 === R1 && !ERRORISH.test(R2)) staleFields.push(el.id);
    }

    if (staleFields.length) {
      stale++;
      rows.push({ f, v: 'STALE', fields: staleFields, r: R0.slice(0, 90) });
    } else pass++;
  } catch (e) {
    err++;
    rows.push({ f, v: 'ERR', why: String((e && e.message) || e).slice(0, 80) });
  } finally {
    try { w.close(); } catch (e) {}
  }
}

console.log(`\n===== G10 审计（清空必填项后结果残留）=====`);
console.log(`样本 ${files.length} / 残留 ${stale} / 正常 ${pass} / 无结果区 ${skipNoBox} / 结果区非结果 ${skipNotResult} / 异常 ${err}`);
for (const r of rows.slice(0, 80)) {
  console.log(`${r.v.padEnd(5)} ${r.f}${r.fields ? '  ← 清空未失效: ' + r.fields.join(',') : ''}${r.why ? '  ! ' + r.why : ''}`);
}
if (jsonArg) fs.writeFileSync(jsonArg.slice(7), JSON.stringify(rows, null, 1));
