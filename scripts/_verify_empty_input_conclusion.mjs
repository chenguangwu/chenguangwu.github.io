// G10 续批（2026-11-11）：空/无效输入仍给出「误导正向结论」回归锁。
//
// 与 _verify_stale_result.mjs 同族：多个工具对空/无效必填输入不拦截，
// 继续用默认值 / 内置数组算出结果，并给出「优秀 / 负载充足 / 热稳定性优异」
// 等正向结论（甚至把彩色等级条留在上一次评估）。本锁对 3 页各断言一条
// 「清空必填项 ⇒ 误导结论区必须被清空或回占位」。
//
// 负向对照：换回修复前版本（HEAD）3/3 全红，已实测。
//
// 用法：node scripts/_verify_empty_input_conclusion.mjs [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

const CASES = [
  {
    cat: 'energy', slug: 'water-tds-evaluator',
    // 清空 TDS ⇒ evaluate() 空分支只清 #result，必须同时把 #vizGrade（大号等级文字）
    // 与 #tdsBar（彩色水位条）复位，否则残留上一次评估的「优质饮用水 / 15% 彩条」。
    probe: `(function(){document.getElementById('tdsInput').value='';evaluate();
      return document.getElementById('vizGrade').textContent+'|'+document.getElementById('tdsBar').textContent;})()`,
    want: '输入TDS值开始评估|',
    desc: '清空 TDS ⇒ 大号等级文字回占位、彩色水位条文本清空（修复前残留旧等级）',
  },
  {
    cat: 'automotive', slug: 'voltage-1',
    // 清空发电机额定电流 ⇒ altCurrent<=0 分支必须清 #res 并 return，否则用默认电压 14.4
    // 与内置 38A 负载算出「负载充足（grade-excellent）」等误导正向结论。
    probe: `(function(){document.getElementById('altCurrent').value='';calc();
      return document.getElementById('res').innerHTML.length;})()`,
    want: '0',
    desc: '清空发电机额定电流 ⇒ 主结果区清空（修复前用默认电压/内置负载给出「负载充足」结论）',
  },
  {
    cat: 'leather', slug: 'temp-9',
    // 清空初始长度 ⇒ l0<=0 分支必须清 #res 并 return，否则 rate=0 命中 grade='优秀'
    // 给出「热稳定性优异」正向结论。
    probe: `(function(){document.getElementById('l0').value='';calc();
      return document.getElementById('res').innerHTML.length;})()`,
    want: '0',
    desc: '清空初始长度 ⇒ 主结果区清空（修复前 rate=0 命中「优秀/热稳定性优异」结论）',
  },
  {
    cat: 'encode', slug: 'encode-3',
    // 清空算法编号 ⇒ algo 经 `||0` 走 else 分支算出 SHA-512 默认长度（64 字节）作误导结论。
    // 修复后 algo 不在 1–4 时清空结果区并提示有效输入。
    probe: `(function(){document.getElementById('algo').value='';calc();
      return document.getElementById('result').textContent;})()`,
    want: '请输入有效算法编号：1=MD5、2=SHA1、3=SHA256、4=SHA512',
    desc: '清空算法编号 ⇒ 提示有效输入（修复前显示 SHA-512 默认 64 字节误导值）',
  },
];

const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');

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

let pass = 0, fail = 0;
const failed = [];

for (const c of CASES) {
  const f = path.join(ROOT, 'tools', c.cat, c.slug + '.html');
  const tag = `[${c.slug}] `;
  if (!fs.existsSync(f)) { fail++; failed.push(tag + '页面不存在'); continue; }
  let dom;
  try {
    dom = build(fs.readFileSync(f, 'utf8'), `https://x.test/tools/${c.cat}/${c.slug}.html`);
    await ready(dom.window);
    const got = String(dom.window.eval(c.probe));
    if (got === c.want) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${c.desc}  ⇒ ${got}`);
    } else {
      fail++;
      failed.push(`${tag}${c.desc}\n      期望 ${JSON.stringify(c.want)} / 实测 ${JSON.stringify(got)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

console.log(fail === 0
  ? `[空输入结论锁] PASS（${pass} PASS / 0 FAIL）`
  : `[空输入结论锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
