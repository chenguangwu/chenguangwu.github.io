// 第 120 批真机回归：F-N102/103（simple-interest）、F-N106（tax-bracket）真修，
// 并核实 F-N104（预设口径）与 F-N105（税后余额口径）已由前批修复。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 自建桩。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
let failed = false;
const bad = [];

function load(slug) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const downloads = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 160) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s), copyText() {}, downloadText() {}, toggleToolTheme() {},
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '',
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8'));
    }
  });
  return { w: dom.window, doc: dom.window.document, downloads, get jsErr() { return jsErr; } };
}
const check = (label, ok, diag) => {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${label}`);
  if (!ok) { failed = true; bad.push(label); if (diag) console.log('  DIAG ' + diag); }
};

// ---------------------------------------------------------------- simple-interest
{
  const { w, doc, downloads, jsErr } = load('simple-interest');
  await new Promise(r => w.addEventListener('load', r));
  check('simple-interest 加载无脚本异常', !jsErr, jsErr);

  // F-N102 复现：本金 10000 / 5% / 3 年 / 每年取息
  doc.getElementById('principal').value = '10000';
  doc.getElementById('rate').value = '5';
  doc.getElementById('years').value = '3';
  doc.getElementById('mode').value = 'annual';
  w.eval('calc()');
  const res = doc.getElementById('resultBox').textContent;
  check('simple-interest 结果区含年度现金流与合计', res.includes('每年取息现金流') && res.includes('合计') && res.includes('1,500'), res.slice(-160));

  downloads.length = 0;
  doc.querySelector('[onclick="__simple_interestExport()"]').click();
  const csv = downloads.map(d => String(d)).join('\n');
  check('F-N102 导出当前结果明细（含现金流行与合计）',
    csv.includes('结果明细') && /第 1 年末/.test(csv) && csv.includes('1,500') && !csv.includes('时间,本金'),
    csv.slice(0, 260));

  // F-N103：清空后可见容器与历史一并清空
  w.eval('clearAll()');
  const ids = ['simple_interestTable', 'simple_interestDiff', 'simple_interestChart', 'simple_interestHist'];
  const left = ids.map(id => [id, (doc.getElementById(id)?.innerHTML || '').length]);
  check('F-N103 清空后历史表/趋势图/差异框/历史列表全空',
    left.every(x => x[1] === 0) && w.TBKit.history.list().length === 0,
    JSON.stringify({ left, hist: w.TBKit.history.list().length }));
  check('F-N103 清空后结果区为占位态', /请输入数据|Enter data/.test(doc.getElementById('resultBox').textContent),
    doc.getElementById('resultBox').textContent);

  // 非 annual 模式也要能导出当前结果（不能退回历史表）
  doc.getElementById('principal').value = '25000';
  doc.getElementById('rate').value = '4.5';
  doc.getElementById('years').value = '4';
  doc.getElementById('mode').value = 'simple';
  w.eval('calc()');
  downloads.length = 0;
  doc.querySelector('[onclick="__simple_interestExport()"]').click();
  const csv2 = downloads.map(d => String(d)).join('\n');
  check('F-N102 非取息模式也导出当前结果', csv2.includes('29,500') && csv2.includes('结果明细') && !csv2.includes('时间,本金'), csv2.slice(0, 220));
  w.close();
}

// ---------------------------------------------------------------- tax-bracket
{
  const { w, doc, downloads, jsErr } = load('tax-bracket');
  await new Promise(r => w.addEventListener('load', r));
  check('tax-bracket 加载无脚本异常', !jsErr, jsErr);

  doc.getElementById('income').value = '100000';
  w.eval('calc()');
  const res = doc.getElementById('resultBox').textContent;
  // F-N105 核实：口径说明已由前批修好
  check('F-N105 核实：税后余额已注明应税所得口径',
    res.includes('税后余额（应纳税所得额 − 个税，未扣五险一金与专项附加）') && !res.includes('税后所得：'),
    res.slice(0, 240));

  downloads.length = 0;
  doc.querySelector('[onclick="__tax_bracketExport()"]').click();
  const csv = downloads.map(d => String(d)).join('\n');
  check('F-N106 导出分档计算明细（含各档金额与合计）',
    csv.includes('结果明细') && csv.includes('第 1 档') && csv.includes('1,080') && csv.includes('累计应纳税') && !csv.includes('时间,应纳税所得额'),
    csv.slice(0, 300));

  // F-N104 核实：预设标签已改为「应纳税所得额」，不是年薪口径
  const presetTxt = doc.getElementById('tax_bracketPresets')?.textContent || '';
  check('F-N104 核实：预设标签为应纳税所得额口径',
    presetTxt.includes('应纳税所得额 10 万') && !presetTxt.includes('年薪 10 万'), presetTxt.slice(0, 200));
  w.close();
}

console.log(`\n=== BATCH120 ${failed ? 'FAILED' : 'ALL PASS'} | failed=${bad.length} ===`);
if (bad.length) console.log(bad.join('\n'));
process.exit(failed ? 1 : 0);
