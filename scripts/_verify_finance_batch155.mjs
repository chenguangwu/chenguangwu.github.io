// 复核失败重做：F-N189 第二批 + 42–44 批 7 页 —— JSDOM 真机全链路（输入→输出→历史→趋势/表格）。
import { JSDOM } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

function makeDom(slug) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const m = html.match(/function __([A-Za-z0-9_]+)Score\(/);
  const p = m ? m[1] : '';
  const trends = [], tables = [];
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`,
    runScripts: 'dangerously', pretendToBeVisual: true,
    beforeParse(w) {
      const noop = () => {};
      w.ToolBox = {
        showToast: noop, escHtml: s => String(s), copyText: noop, downloadText: noop,
        toggleToolTheme: noop, setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        createTable: () => '',
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = () => 'blob:test';
      w.URL.revokeObjectURL = noop;
      w.HTMLAnchorElement.prototype.click = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
      w.eval(TK);
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (h, c) => { trends.push(c); return line(h, c); };
      const tbl = w.TBKit.matrix.table;
      w.TBKit.matrix.table = (h, c) => { tables.push(c); return tbl(h, c); };
    },
  });
  return { w: dom.window, p, trends, tables };
}

async function ready(w) {
  if (w.document.readyState === 'complete') return;
  await new Promise(res => w.addEventListener('load', res, { once: true }));
}

// 5 个校验页：失败输入在长中性描述之后才给结论（或本身是长度错误），历史必须记未通过
const validators = [
  ['gstin-validator', '27ABCDE1234F1Z1', 'GSTIN'],
  ['meid-validator', 'A00000000000001', 'MEID'],
  ['abn-validator', '51824753557', 'ABN'],
  ['aadhaar-validator', '2'.repeat(100), 'Aadhaar 100位'],
  ['bic-validator', '2'.repeat(100), 'BIC'],
];
for (const [slug, bad, name] of validators) {
  const { w, p, trends, tables } = makeDom(slug);
  await ready(w);
  const d = w.document;
  const el = d.getElementById('input');
  el.value = bad;
  el.dispatchEvent(new w.Event('input', { bubbles: true }));
  await new Promise(res => setTimeout(res, 30));
  w.eval(`__${p}Extras(true)`);
  const hist = w.TBKit.history.list();
  const rec = hist.length ? hist[0].d : null;
  const res = rec ? String(rec['结果'] || '') : '';
  check(`${name}-历史score=0`, rec && rec.__tbScore === 0, JSON.stringify({ score: rec && rec.__tbScore, res: res.slice(0, 120) }));
  const full = String(w.eval(`__${p}FullResText()`) || '');
  check(`${name}-全文含失败结论`, /无效|错误|必须为|失败|Invalid|invalid|must|Failed|未通过/.test(full), full.slice(-120));
  check(`${name}-历史摘要与全文分离`, !res.includes('❌') || res.length <= 80, res.slice(-40));
  w.close();
}

// 2 个计算页：清空必填项后计算，历史必须记未通过（不是记通过/不记录）
const calculators = [
  ['calc-5', 'cost', '投资成本'],
  ['dca-calculator', 'monthly', '每月金额'],
];
for (const [slug, id, name] of calculators) {
  const { w, p, trends, tables } = makeDom(slug);
  await ready(w);
  const d = w.document;
  d.getElementById(id).value = '';
  w.eval('calc()');
  w.eval(`__${p}Extras(true)`);
  const hist = w.TBKit.history.list();
  const rec = hist.length ? hist[0].d : null;
  const res = rec ? String(rec['结果'] || '') : '';
  check(`清空${name}-历史score=0`, rec && rec.__tbScore === 0, JSON.stringify({ score: rec && rec.__tbScore, res: res.slice(0, 120) }));
  check(`清空${name}-结果含请填写`, res.includes('请填写'), res.slice(0, 120));
  w.close();
}

// 生成源护栏：不得用统一词表批量生成判定（F-N189 生成源禁绕过）
const wire = readFileSync(`${ROOT}/scripts/_ux_wire.py`, 'utf8');
check('生成源apply_custom护栏仍在', /business-verdict-required/.test(wire));

const failed = checks.filter(c => !c[1]).length;
console.log('\nBATCH155 checks=' + checks.length + ' failed=' + failed);
process.exit(failed ? 1 : 0);
