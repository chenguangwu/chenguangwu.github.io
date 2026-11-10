// G10 回归锁：输入失效后必须清空旧结果 / 旧明细表 / 可复制的数据。
//
// 每页一条「清空某必填项 ⇒ 结果必须离开上一次的展示」断言。
// 这些页在 2026-11-08 第 48 批修复，本锁防复发（改默认值/改模板时会被这里挡住）。
//
// 用法：node scripts/_verify_stale_result.mjs [--cat=<dir> --pages=a,b] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

const CASES = [
  {
    cat: 'health', slug: 'insulin-dose',
    probe: `(function(){document.getElementById('currentBg').value='';calc();
      var b=document.getElementById('breakdown').innerHTML;
      return [document.getElementById('doseVal').textContent,
              /输入无效/.test(b)&&!/餐时剂量|校正剂量|活性胰岛素|总计/.test(b)?1:0,
              document.getElementById('doseMarker').style.left,
              (typeof __insulin_doseResText==='function'?__insulin_doseResText():'n/a')].join('|');})()`,
    want: '--|1|0%|',
    desc: '清空当前血糖 ⇒ 主剂量回 --、旧剂量明细不残留（仅显示输入无效提示）、标尺归零、历史文本判无效',
  },
  {
    cat: 'engineering', slug: 'thermal-expansion',
    probe: `(function(){var t=document.getElementById('thermal_expansionTable');
      t.innerHTML='<table><tr><td>旧行</td></tr></table>';
      document.getElementById('L0').value='0';calcTool();
      return t.querySelectorAll('tr').length+'|'+(/请输入有效参数/.test(document.getElementById('result').textContent)?1:0);})()`,
    want: '0|1',
    desc: 'L₀=0 ⇒ 主结果报错且明细表旧行被清空（否则导出行旧数据）',
  },
  {
    cat: 'agriculture', slug: 'calculator-calc-concentration',
    probe: `(function(){var t=document.getElementById('calculator_calc_concentrationTable');
      t.innerHTML='<table><tr><td>旧行</td></tr></table>';
      document.getElementById('stock').value='';calc();
      return t.querySelectorAll('tr').length;})()`,
    want: '0',
    desc: '清空原药浓度 ⇒ 明细表旧行被清空（否则导出行旧数据）',
  },
  {
    cat: 'science', slug: 'science-pressure-converter',
    probe: `(function(){document.getElementById('val').value='';convert();
      return String(lastResult)+'|'+(/\\d/.test(document.getElementById('unitGrid').textContent)?1:0);})()`,
    want: 'null|0',
    desc: '清空数值 ⇒ 换算网格清空且 lastResult 置空（复制/保存不再带走旧值）',
  },
  {
    cat: 'fun', slug: 'typing-rhythm',
    // 必须先跑出一次评分，否则初始态本来就是 '-'、断言毫无判别力（实测 HEAD 也会 PASS）。
    // 3 次等间隔按键 ⇒ iv=[200,200] ⇒ 均值 200、标准差 0、CV 0 ⇒ 评分 100。
    probe: `(function(){times=[1000,1200,1400];analyze();
      var before=document.getElementById('scoreV').textContent;
      times=[1000,1200];analyze();
      return before+'→'+document.getElementById('scoreV').textContent;})()`,
    want: '100→-',
    desc: '按键样本不足 ⇒ 旧评分作废（100 → -，结果区回占位）',
  },
  {
    cat: 'edu', slug: 'multiplication-table',
    probe: `(function(){var i=document.getElementById('pAnswer');i.value='';checkAnswer();
      return document.getElementById('pFeedback').textContent;})()`,
    want: '请输入答案后再提交',
    desc: '空答案提交 ⇒ 不再显示上一题的「✅ 正确 / ❌ 错误」',
  },
  // ── 第 50 批（2026-11-08）：校验失败 return 但未清结果区 —「输入失效后旧结果残留」同类缺陷 ──
  {
    cat: 'energy', slug: 'battery-life',
    probe: `(function(){document.getElementById('capacity').value='';calc();
      return document.getElementById('result').innerHTML.length;})()`,
    want: '0',
    desc: '清空电池容量 ⇒ 容量/功耗≤0 分支 return 前清空主结果区（修复前残留旧续航）',
  },
  {
    cat: 'fishery', slug: 'profit-calculator',
    probe: `(function(){document.getElementById('yield').value='';calc();
      return document.getElementById('result').innerHTML.length;})()`,
    want: '0',
    desc: '清空产量 ⇒ 产量≤0 分支 return 前清空主结果区（修复前残留旧利润核算）',
  },
  {
    cat: 'endocrinology', slug: 'insulin-adjustment',
    probe: `(function(){document.getElementById('weight').value='';calc();
      return document.getElementById('result').innerHTML.length;})()`,
    want: '0',
    desc: '清空体重 ⇒ 体重≤0 分支 return 前清空主结果区（修复前残留旧胰岛素方案）',
  },
  {
    cat: 'food-processing', slug: 'filling-volume',
    probe: `(function(){document.getElementById('dia').value='';calc();
      return document.getElementById('result').innerHTML.length;})()`,
    want: '0',
    desc: '清空内径 ⇒ 内径≤0 分支 return 前清空主结果区（修复前残留旧灌装量）',
  },
  {
    cat: 'nutrition', slug: 'calc-3',
    probe: `(function(){document.getElementById('calories').value='';calculate();
      return document.getElementById('result').innerHTML.length;})()`,
    want: '0',
    desc: '清空卡路里 ⇒ 卡路里≤0 分支 return 前清空主结果区（修复前残留旧营养素）',
  },
  {
    cat: 'tcm-chemistry', slug: 'content-assay',
    probe: `(function(){document.getElementById('isConc').value='';calcFactor();
      return document.getElementById('factorResult').innerHTML.length+'|'+document.getElementById('assayResult').innerHTML.length;})()`,
    want: '0|0',
    desc: '清空内标浓度 ⇒ 校正因子校验 return 前清空因子区与含量区（修复前两区残留旧结果）',
  },
];

const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const catArg = argv.find((a) => a.startsWith('--cat='));
const pagesArg = argv.find((a) => a.startsWith('--pages='));
let cases = CASES;
if (catArg || pagesArg) {
  const cat = catArg ? catArg.slice(6) : null;
  const slugs = pagesArg ? pagesArg.slice(8).split(',').map((s) => s.trim()) : null;
  cases = CASES.filter((c) => (!cat || c.cat === cat) && (!slugs || slugs.includes(c.slug)));
}
if (!cases.length) { console.error('没有匹配的用例'); process.exit(2); }

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

for (const c of cases) {
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
  ? `[G10 残留锁] PASS（${pass} PASS / 0 FAIL）`
  : `[G10 残留锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
