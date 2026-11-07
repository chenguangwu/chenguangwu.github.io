// 审计：__tbInputGuard 页在「必填项全空」时，明细表是否残留上一次的行（导出会带走旧数据）。
//
// 做法：预置一行假数据 → 清空 guard 声明的全部 id → 触发计算 → 明细表应 0 行。
// 用法：node scripts/_audit_guard_stale_table.mjs --list=<file> [--json=out.json]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';

const argv = process.argv.slice(2);
const listArg = argv.find((a) => a.startsWith('--list='));
const jsonArg = argv.find((a) => a.startsWith('--json='));
if (!listArg) { console.error('usage: node scripts/_audit_guard_stale_table.mjs --list=<file>'); process.exit(2); }
const files = fs.readFileSync(listArg.slice(7), 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);

const SENTINEL = '__TB_OLD_ROW__';
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
        copyText() {}, showToast() {}, toast() {}, formatNumber: (n) => String(n),
        escHtml: (s) => String(s == null ? '' : s), esc: (s) => String(s == null ? '' : s),
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid() {}, clearInvalid() {}, createTable: () => '', debounce: (fn) => fn,
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
      // matrix.table 必须按 js/tool-kit.js 真实实现桩：其首行是 box.innerHTML=''
      // （用 anyStub 会让「页面其实已重渲染空表」的页被误判成残留）
      const matrixTable = (host, cfg) => {
        const box = typeof host === 'string' ? (host.charAt(0) === '#' ? w.document.getElementById(host.slice(1)) : w.document.querySelector(host)) : host;
        if (!box) return null;
        cfg = cfg || {};
        const head = cfg.head || [], rows = cfg.rows || [];
        box.innerHTML = '';
        const table = w.document.createElement('table');
        if (head.length) {
          const thead = w.document.createElement('thead'), tr = w.document.createElement('tr');
          head.forEach((h) => { const th = w.document.createElement('th'); th.textContent = h; tr.appendChild(th); });
          thead.appendChild(tr); table.appendChild(thead);
        }
        const tbody = w.document.createElement('tbody');
        rows.forEach((r) => {
          const tr = w.document.createElement('tr');
          r.forEach((c) => { const td = w.document.createElement('td'); td.textContent = c; tr.appendChild(td); });
          tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        box.appendChild(table);
        return table;
      };
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} },
        matrix: new Proxy({ table: matrixTable }, {
          get(t, k) { return Object.prototype.hasOwnProperty.call(t, k) ? t[k] : () => ({}); },
        }),
        chart: anyStub(), preset: anyStub(),
      };
    },
  });
}

const ready = (w) => new Promise((res) => {
  if (w.document.readyState === 'complete') return res();
  w.addEventListener('load', res);
  setTimeout(res, 3000);
});

const rows = [];
let pass = 0, stale = 0, skipNoTbl = 0, skipNoGuard = 0, err = 0;

for (const f of files) {
  if (!fs.existsSync(f)) continue;
  const raw = fs.readFileSync(f, 'utf8');
  const tm = raw.match(/matrix\.table\('#([A-Za-z0-9_]+Table)'/);
  if (!tm) { skipNoTbl++; continue; }
  const gm = raw.match(/__tbInputGuard\(\[([^\]]*)\]/);
  if (!gm) { skipNoGuard++; continue; }
  const ids = gm[1].split(',').map((s) => s.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean);
  if (!ids.length) { skipNoGuard++; continue; }
  const tblId = tm[1];

  let dom;
  try { dom = build(raw, `https://x.test/${f}`); }
  catch (e) { err++; rows.push({ f, v: 'ERR', why: String((e && e.message) || e).slice(0, 70) }); continue; }
  const w = dom.window;
  try {
    await ready(w);
    const tb = w.document.getElementById(tblId);
    if (!tb) { skipNoTbl++; continue; }

    // 预置一行带唯一哨兵的「旧数据」，模拟用户上一轮已算出结果
    tb.innerHTML = '<table><tr><td>' + SENTINEL + '</td></tr></table>';

    const names = [];
    const re = /on(?:input|change|keyup)="([A-Za-z_$][\w$]*)\(/g;
    let m; while ((m = re.exec(raw))) if (!names.includes(m[1])) names.push(m[1]);
    for (const d of ['calcTool', 'calc', 'calculate', 'compute', 'update']) {
      if (new RegExp(`function ${d}\\s*\\(|${d}\\s*=\\s*function`).test(raw) && !names.includes(d)) names.push(d);
    }

    for (const id of ids) { const el = w.document.getElementById(id); if (el) el.value = ''; }
    for (const n of names) { try { w.eval(n + '()'); } catch (e2) {} }

    // 用哨兵判定：页面在无有效输入时会往表里写「请先填写…」空态提示，那不算残留；
    // 只有哨兵行仍在，才说明上一轮的数据没被清掉
    const left = String(tb.textContent || '').includes(SENTINEL) ? tb.querySelectorAll('tbody tr').length : 0;
    if (left === 0) pass++;
    else { stale++; rows.push({ f, v: 'STALE', tbl: tblId, left, txt: tb.textContent.replace(/\s+/g, ' ').slice(0, 60) }); }
  } catch (e) {
    err++; rows.push({ f, v: 'ERR', why: String((e && e.message) || e).slice(0, 70) });
  } finally {
    try { w.close(); } catch (e) {}
  }
}

console.log(`\n===== guard 页明细表残留审计 =====`);
console.log(`样本 ${files.length} / 已修 ${pass} / 残留 ${stale} / 无表 ${skipNoTbl} / 无 guard 调用 ${skipNoGuard} / 异常 ${err}`);
for (const r of rows.slice(0, 40)) console.log(`${r.v.padEnd(5)} ${r.f}${r.tbl ? '  tbl=#' + r.tbl + ' 剩 ' + r.left + ' 行' : ''}${r.txt ? '  [' + r.txt + ']' : ''}${r.why ? '  ! ' + r.why : ''}`);
if (jsonArg) fs.writeFileSync(jsonArg.slice(7), JSON.stringify(rows, null, 1));
