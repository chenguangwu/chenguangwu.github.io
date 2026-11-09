// G10 续批（2026-11-11）：「恢复历史后只重绘不重算」回归锁。
//
// 多页 restore 回调在把 A 换成历史答案后只调 render()、不调 calc()，
// 导致 #result（含分级/结论/门诊记录）仍停留在恢复前的旧结论。
// 修复：restore 回调末尾补 calc()，使恢复后立即按历史答案重算。
//
// 本锁用 JSDOM + TBKit.history.mount 捕获回调，注入历史答案后断言结果区
// 已按新答案重算（不再残留旧结论）。
//
// 负向对照：换回修复前版本（--root 指向 HEAD 抽取目录）2/2 全红，已实测。
//
// 用法：node scripts/_verify_history_restore_recompute.mjs [--root=<dir>] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const rootArg = argv.find((a) => a.startsWith('--root='));
const BASE = rootArg ? rootArg.slice('--root='.length) : ROOT;

const CASES = [
  {
    cat: 'psychiatry', slug: 'phq9-depression', mountFn: '__quizMountHist',
    ans: '3,3,3,3,3,3,3,3,3', want: '重度抑郁',
    desc: '恢复 9×3=27 历史答案 ⇒ #result 重算为「重度抑郁」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'cage-substance', mountFn: '__cageMountHist',
    ans: '0,0,0,0', want: '筛查阳性',
    desc: '恢复 4×「是」历史答案 ⇒ #result 重算为「筛查阳性」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'gad7-anxiety', mountFn: '__gd7MountHist',
    ans: '3,3,3,3,3,3,3', want: '重度焦虑',
    desc: '恢复 7×3=21 历史答案 ⇒ #result 重算为「重度焦虑」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'isi-insomnia', mountFn: '__isiMountHist',
    ans: '4,4,4,4,4,4,4', want: '重度失眠',
    desc: '恢复 7×4=28 历史答案 ⇒ #result 重算为「重度失眠」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'ybocs-ocd', mountFn: '__ybocMountHist',
    ans: '4,4,4,4,4,4,4,4,4,4', want: '极重度',
    desc: '恢复 10×4=40 历史答案 ⇒ #result 重算为「极重度」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'pcl5-ptsd', mountFn: '__pcl5MountHist',
    ans: '4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4', want: '重度',
    desc: '恢复 20×4=80 历史答案 ⇒ #result 重算为「重度」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'mdq-bipolar', mountFn: '__mdqMountHist',
    ans: '0,0,0,0,0,0,0,0,0,0,0,0,0', p2: 0, p3: 3, want: '筛查阳性',
    desc: '恢复 13×「是」+P2同期+P3中/重度 ⇒ #result 重算为「筛查阳性」（修复前只 render 不 calc，结论残留旧值）',
  },
];

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
        markInvalid() {}, clearInvalid() {},
        createTable: () => '', debounce: (fn) => fn, $: (id) => w.document.getElementById(id),
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
        history: {
          list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; },
          mount(sel, cb) { w.__histCb = cb; },
        },
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

let pass = 0, fail = 0;
const failed = [];

for (const c of CASES) {
  const f = path.join(BASE, 'tools', c.cat, c.slug + '.html');
  const tag = `[${c.slug}] `;
  if (!fs.existsSync(f)) { fail++; failed.push(tag + '页面不存在'); continue; }
  let dom;
  try {
    dom = build(fs.readFileSync(f, 'utf8'), `https://x.test/tools/${c.cat}/${c.slug}.html`);
    await ready(dom.window);
    const w = dom.window;
    w[c.mountFn]();                 // 注册 mount → 捕获回调存入 w.__histCb
    const cb = w.__histCb;
    if (typeof cb !== 'function') { fail++; failed.push(`${tag}未捕获到 history.mount 回调`); continue; }
    cb({ ans: c.ans, p2: c.p2, p3: c.p3 }); // 模拟用户点击历史记录
    const got = String(w.document.getElementById('result').textContent || '');
    if (got.includes(c.want)) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${c.desc}  ⇒ 命中「${c.want}」`);
    } else {
      fail++;
      failed.push(`${tag}${c.desc}\n      期望包含 ${JSON.stringify(c.want)} / 实测 ${JSON.stringify(got).slice(0, 120)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

for (const [cat, slug, prefix] of [
  ['cardiology', 'aortic-dissection', 'aortic_dissection'],
  ['forensic-medicine', 'wound-description', 'wound_description'],
  ['hematology', 'itp-risk-score', 'itp_risk_score'],
  ['ophthalmology', 'visual-fatigue-vas', 'visual_fatigue_vas'],
  ['tcm-pharmacy', 'tcm-adr-assessment', 'tcm_adr_assessment'],
]) {
  let dom;
  try {
    dom = build(fs.readFileSync(path.join(BASE, 'tools', cat, slug + '.html'), 'utf8'), `https://x.test/tools/${cat}/${slug}.html`);
    await ready(dom.window);
    const w = dom.window;
    const groups = Array.from(w.document.querySelectorAll('input[type=radio][id]')).reduce((m, e) => ((m[e.name] ||= []).push(e), m), {});
    const entries = Object.values(groups).filter((g) => g.length > 1);
    const expect = (ok, label) => { if (ok) pass++; else { fail++; failed.push(`[${slug}] ${label}`); } };
    expect(entries.length > 0, '必须有单选组');
    w[`__${prefix}Render`]([], '结果', false);
    const record = {};
    entries.forEach((group) => group.forEach((e, i) => { record[e.id] = i === 0 ? '1' : '0'; }));
    w.__histCb(record);
    expect(entries.every((group) => group[0].checked && group.slice(1).every((e) => !e.checked)), '完整状态快照恢复选项错误');
    const zeroGroup = entries.find((group) => group.some((e) => e.value === '0'));
    if (zeroGroup) {
      const zero = zeroGroup.find((e) => e.value === '0');
      w.__histCb({ [zero.id]: '0' });
      expect(zero.checked, '旧稀疏记录中选中的零值丢失');
    }
    entries.forEach((group) => { group[group.length - 1].checked = true; });
    const snap = w[`__${prefix}Snap`]();
    expect(entries.every((group) => group.every((e) => Object.hasOwn(snap, e.id))), '快照丢失单选项');
    let saved;
    w.TBKit.history.record = (rec) => { saved = rec; };
    w.document.getElementById('result').textContent = '已完成';
    w[`__${prefix}Extras`]();
    expect(!!saved && entries.every((group) => group.every((e) => Object.hasOwn(saved, e.id))), '保存记录不得截断单选答案');
    if (saved) {
      entries.forEach((group) => { group[0].checked = true; });
      w.__histCb(saved);
      expect(entries.every((group) => group[group.length - 1].checked), '保存后恢复所有单选组');
      if (Object.keys(snap).length > 12) {
        const before = saved;
        w.TBKit.history.last = () => before;
        w.document.getElementById('result').textContent = before['结果'];
        w[`__${prefix}_last`] = 0;
        entries[entries.length - 1][0].checked = true;
        saved = null;
        w[`__${prefix}Extras`]();
        expect(!!saved, '后续题目变更不得被去重忽略');
      }
    }
  } catch (e) { fail++; failed.push(`[${slug}] 运行期异常：${e.message}`); }
  finally { if (dom) dom.window.close(); }
}

console.log(fail === 0
  ? `[历史恢复重算锁] PASS（${pass} PASS / 0 FAIL）`
  : `[历史恢复重算锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
