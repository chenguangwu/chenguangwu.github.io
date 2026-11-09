// 复选框/单选历史状态回归锁：验证「快照完整 + 恢复前清空未记录项」。
// 用法：node scripts/_verify_checkbox_history.mjs --cat=it --pages=a,b,c [--verbose]
//       node scripts/_verify_checkbox_history.mjs --list=tools/...（默认读内置样本）
//
// 背景（IT 静态审计确认）：全站 302 页共用同一 Snap 模板，原先
// `var v=(t==='checkbox'||t==='radio')?(e.checked?(e.value||'1'):''):e.value;`
// 只记录「勾选中的项」⇒ 两个真缺陷：
//   ① 历史恢复只遍历已存键，不会清理当前多勾的项（600→777→恢复 600 仍得 777）；
//   ② 全部不勾（如 chmod 000）时快照为空 ⇒ Extras 早退，该状态永远不入历史。
// 修复：快照改记 '1'/'0' 全量；恢复前先清空记录里没有的勾选。
//
// 另有一套「旧模板变体」页面（`__<pre>Raw(id)` + `__<pre>Restore(rec)` + 显式
// record 字段表，全站 802 页里 3 页带复选框）：同一根因的两个缺陷表现一致，
// 但快照入口不是 Snap()、且勾选态原先根本没进 record。本锁按模板类型分别取快照。
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';

const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const catArg = (argv.find((a) => a.startsWith('--cat=')) || '--cat=it').slice(6);
const pagesArg = argv.find((a) => a.startsWith('--pages='));

// 内置回归样本：两套模板各有代表，进 run_gates 做防复发哨兵（不追求全覆盖，
// 全覆盖的 62 分类抽样另有 /tmp 批量跑法）。
const DEFAULT_SAMPLE = [
  'it/chmod-calculator',        // Snap 模板 + 3 个静态复选框（600/777 缺陷原始现场）
  'it/text-cleaner',            // Snap 模板 + 14 个复选框，全不勾时无结果（SKIP 分支）
  'biz/text-compare',           // Snap 模板 + 文本域混排
  'civil/rebar-anchorage',      // 旧模板 Raw/Restore 变体
  'health/milk-tea-calories',   // 旧模板变体 + Extras 越作用域变量（曾整体静默失效）
  'welding/weld-strength',      // 旧模板变体（单复选框）
  'it/xml-to-yaml', 'it/random-string', 'it/yaml-to-json', 'it/toml-to-json',
  'it/yaml-to-xml', 'it/csv-to-yaml', 'it/toml-to-xml', 'it/toml-to-yaml',
  'it/yaml-to-toml', 'it/whitespace', 'it/xml-to-toml',
];

const TARGETS = pagesArg
  ? pagesArg.slice(8).split(',').map((s) => s.trim()).filter(Boolean).map((slug) => ({ cat: catArg, slug }))
  : DEFAULT_SAMPLE.map((s) => { const i = s.indexOf('/'); return { cat: s.slice(0, i), slug: s.slice(i + 1) }; });
if (!TARGETS.length) { console.error('usage: node scripts/_verify_checkbox_history.mjs [--cat=<dir> --pages=a,b]'); process.exit(2); }

let pass = 0, fail = 0, skip = 0;
const failed = [];
const assert = (c, m) => { if (c) pass++; else { fail++; failed.push(m); } };

function build(raw, url) {
  const state = { hist: null, arr: [] };
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = {
        copyText() {}, showToast() {}, formatNumber(n) { return String(n); },
        escHtml: (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'),
        esc: (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'),
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      const ctxStub = new Proxy({}, {
        get(t, k) {
          if (k === 'canvas') return { width: 600, height: 300 };
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          return () => {};
        },
        set() { return true; },
      });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctxStub; } catch (e) {}
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: {
          // 记录形状必须与真实 TBKit 一致：{t, d}。少了 d 会让 Render 里
          // it.d[...] 抛错被 try/catch 吞掉 ⇒ mount 不注册，误判成「恢复不生效」。
          list: () => state.arr.slice(),
          last: () => (state.arr.length ? state.arr[0].d : null),
          record(o) { state.arr.unshift({ t: Date.now(), d: o }); },
          clear() { state.arr.length = 0; },
          diffLast() { return null; },
          mount(sel, cb) { state.hist = cb; },
        },
        matrix: { table() {} }, chart: { line() {}, bar() {} }, preset: { bar() {} },
      };
    },
  });
  return { dom, w: dom.window, state };
}

const ready = (w) => new Promise((res) => {
  if (w.document.readyState === 'complete') return res();
  w.addEventListener('load', res);
  setTimeout(res, 4000);
});

for (const { cat, slug } of TARGETS) {
  const f = `tools/${cat}/${slug}.html`;
  const tag = `[${slug}] `;
  if (!fs.existsSync(f)) { assert(false, tag + '页面不存在: ' + f); continue; }
  const raw = fs.readFileSync(f, 'utf8');
  const preM = raw.match(/function __(\w+?)Snap\(\)\{/);
  const rawPreM = raw.match(/function __(\w+?)Raw\(id\)\{/);
  if (!preM && !rawPreM) { assert(false, tag + '未找到 Snap/Raw 快照函数'); continue; }
  const pre = (preM || rawPreM)[1];
  // true = 旧模板变体（Raw 逐字段 + 显式 record 字段表）
  const isRawTpl = !preM && !!rawPreM;
  // 只取静态 id：动态生成的复选框（`id="chk-' + a.id + '"`）会带引号/加号，
  // 那样的「id」在 DOM 里根本不存在，会让断言凭空失败（energy/standby-power-calculator 实测）。
  // 属性顺序不固定（type 可能写在 id 之后），故先抓整个 <input …> 再判类型。
  const boxIds = (raw.match(/<input\b[^>]*>/gi) || [])
    .filter((x) => /type\s*=\s*["']?checkbox/i.test(x))
    .map((x) => (x.match(/id\s*=\s*(["'])([^"']*)\1/) || [])[2])
    // 引号必须配对：JS 拼接模板 `id="chk-' + a.id + '"` 的引号不配对，取不到 id
    // （否则会截出假 id `chk-`，凭空 FAIL，energy/standby-power-calculator 实测）。
    .filter((id) => id && /^[A-Za-z0-9_-]+$/.test(id))
    .filter((id, i, a) => a.indexOf(id) === i);
  if (!boxIds.length) { skip++; console.log(`  ↷ ${tag} 页面无复选框，跳过`); continue; }

  let built;
  try { built = build(raw, `https://x.test/${f}`); }
  catch (e) { assert(false, tag + 'JSDOM 初始化异常：' + String(e.message || e).slice(0, 120)); continue; }
  const { w, state, dom } = built;
  try {
    await ready(w);
    const on = () => { boxIds.forEach((id) => { const e = w.document.getElementById(id); if (e) e.checked = true; }); };
    const off = () => { boxIds.forEach((id) => { const e = w.document.getElementById(id); if (e) e.checked = false; }); };
    const half = () => { boxIds.forEach((id, i) => { const e = w.document.getElementById(id); if (e) e.checked = i < Math.ceil(boxIds.length / 2); }); };
    // 旧模板变体没有独立快照函数，勾选态是 Extras 里写进 record 的 ⇒ 直接读最近一条记录。
    const snap = () => (isRawTpl
      ? ((state.arr[0] && state.arr[0].d) || {})
      : (w.eval(`__${pre}Snap()`) || {}));
    const extras = () => { w.eval(`__${pre}_last=0`); w.eval(`__${pre}Extras()`); };
    // Extras 首行要求 ResText 非空才继续 ⇒ 必须先让页面算一次（否则 Render 不执行、
    // mount 不注册，恢复回调根本不存在，会误判成「恢复不生效」）。
    const runCalc = () => {
      const cands = [];
      const re = /on(?:change|click)="([A-Za-z_$][\w$]*)\(\)"/g;
      let m; while ((m = re.exec(raw))) if (!cands.includes(m[1])) cands.push(m[1]);
      for (const fn of cands) { try { w.eval(fn + '()'); } catch (e) {} }
      try { w.eval(`__${pre}Extras()`); } catch (e) {}
      const box = w.document.querySelector('.result-box, #result, #output');
      if (box && !String(box.textContent || box.value || '').trim()) box.textContent = '输入： 测试 结果： 通过';
    };
    runCalc();

    // ① 快照必须覆盖全部复选框（未勾也要有 '0'），否则 000 这类状态永远不入历史
    half(); extras();
    const s1 = snap();
    const missing = boxIds.filter((id) => s1[id] == null);
    assert(missing.length === 0, tag + '快照应包含全部复选框（缺 ' + missing.slice(0, 3).join(',') + '）');
    const zeros = boxIds.filter((id) => s1[id] === '0').length;
    assert(zeros === boxIds.length - Math.ceil(boxIds.length / 2), tag + '未勾选项应记 0，实测 0 值 ' + zeros);

    // ② 全不勾也必须入历史（前提：该状态下页面还有结果可记；无结果则记为 SKIP）
    off(); extras();
    const resOff = (() => { try { return String(w.eval(`__${pre}ResText()`)); } catch (e) { return ''; } })();
    if (!resOff) { skip++; console.log(`  ↷ ${tag} 全不勾时无结果，跳过「空状态入历史」断言`); }
    const recOff = state.arr[0] && state.arr[0].d;
    // Extras 会把快照键截到 12 个（页面模板固定行为，顺序是 input/select/textarea 的 DOM 序，
    // 不是复选框序）⇒ 只断言「进了记录的复选框键必须是 0」，未进记录的（被截断）不判红；
    // 但仍要求「记录确实产生」——这才是原缺陷（空快照 ⇒ Extras 早退 ⇒ 000 永不入库）的判据。
    if (resOff) {
      const inRec = boxIds.filter((id) => recOff && id in recOff);
      assert(!!recOff, tag + '全不勾状态应入历史');
      assert(inRec.every((id) => String(recOff[id]) === '0'), tag + '全不勾状态入历史的复选框键应为 0');
    }

    // ③ 报错点：稀疏旧记录恢复时必须清掉当前多勾的项
    on();
    const sparse = {};
    boxIds.slice(0, 1).forEach((id) => { sparse[id] = '1'; });
    state.hist && state.hist(sparse);
    const after = boxIds.filter((id) => { const e = w.document.getElementById(id); return e && e.checked; }).length;
    assert(!!state.hist, tag + '应注册历史恢复回调');
    assert(after === 1, tag + '稀疏记录恢复后应只剩 1 项勾选，实测 ' + after);

    // ④ 完整记录恢复
    on();
    const full = {};
    boxIds.forEach((id) => { full[id] = '0'; });
    state.hist && state.hist(full);
    const afterAllOff = boxIds.filter((id) => { const e = w.document.getElementById(id); return e && e.checked; }).length;
    assert(afterAllOff === 0, tag + '完整全 0 记录恢复后应无勾选，实测 ' + afterAllOff);
    if (boxIds.some((id) => w.document.getElementById(id).value === '0')) {
      off();
      const mixed = {};
      boxIds.forEach((id, i) => { mixed[id] = i % 2 ? '0' : '1'; });
      state.hist(mixed);
      assert(boxIds.every((id, i) => w.document.getElementById(id).checked === (i % 2 === 0)), tag + '混合 0/1 快照恢复错误');
      state.hist(Object.fromEntries(boxIds.map((id) => [id, true])));
      assert(boxIds.every((id) => w.document.getElementById(id).checked), tag + '旧布尔 true 恢复错误');
      state.hist(Object.fromEntries(boxIds.map((id) => [id, false])));
      assert(boxIds.every((id) => !w.document.getElementById(id).checked), tag + '布尔 false 恢复错误');
    }
  } catch (e) {
    assert(false, tag + '运行期异常：' + String((e && e.message) || e).slice(0, 140));
  } finally {
    dom.window.close();
  }
  if (verbose) console.log(`  · ${tag}${boxIds.length} 个复选框`);
}

console.log(fail === 0
  ? `[复选框历史锁] PASS（${pass} PASS / 0 FAIL${skip ? ` / ${skip} SKIP` : ''}）`
  : `[复选框历史锁] FAIL（${pass} PASS / ${fail} FAIL${skip ? ` / ${skip} SKIP` : ''}）`);
if (fail) failed.slice(0, 25).forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
