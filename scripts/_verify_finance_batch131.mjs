// 第 131 批真机回归：finance.md F-N71（calc-2 IRR 无实根误报 1000%）。
// 清单条目对应的修复与判别锁在前批已完成，本批按原始复现条件真机核实确认生效。
// JSDOM runScripts:'dangerously' + 自建 ToolBox 桩 + 真实 input / calc() / 状态链。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
function makeDom(en = false) {
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(readFileSync(`${ROOT}/tools/finance/calc-2.html`, 'utf8'), {
    url: 'https://x.test/tools/finance/calc-2.html' + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => en, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop,
          downloadText: noop },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop }, export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: d || 2, maximumFractionDigits: d || 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const txt = (c, id) => (c.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };

async function main() {
  console.log('== F-N71 IRR 无实根核实 ==');
  const c = makeDom();
  await ready(c);
  check('F-N71 加载无 JS 异常', c.jsErr === '', c.jsErr);
  const run = (initial, flows) => {
    set(c, 'initial', initial); set(c, 'flows', flows);
    c.w.eval('calc()');
    return { res: txt(c, 'res'), summary: txt(c, 'summary'), rate: c.w.eval('(function(){var f=[parseFloat(document.getElementById("initial").value)].concat(String(document.getElementById("flows").value).split(/[,，\\s\\n]+/).map(function(s){return parseFloat(s)}).filter(function(n){return !isNaN(n)}));return irr(f);})()') };
  };
  // 清单原始复现：initial=-100, flows=230,-132.5 ⇒ 判别式 <0 无实根
  const noRoot = run('-100', '230,-132.5');
  check('F-N71 无实根 irr() 返回 null', noRoot.rate === null, String(noRoot.rate));
  check('F-N71 无实根提示「无法计算 IRR（现金流无实根）」', /无法计算 IRR（现金流无实根）/.test(noRoot.res), noRoot.res.slice(0, 160));
  check('F-N71 无实根不输出 1000%/1000.0000%', !/1000(\.0+)?%/.test(noRoot.res + noRoot.summary), (noRoot.res + noRoot.summary).slice(0, 160));
  check('F-N71 无实根不写「NPV 约等于 0」结论', !/NPV 约等于 0/.test(noRoot.res), noRoot.res.slice(0, 160));
  check('F-N71 无实根清汇总卡', noRoot.summary === '', noRoot.summary.slice(0, 100));
  // 符号无变化：initial 与 flows 全为正（有现金流但无正负切换）
  const noSign = run('10000', '3000,3000');
  check('F-N71 现金流符号无变化提示数据不足', /符号没有变化或数据不足/.test(noSign.res), noSign.res.slice(0, 160));
  // 合法现金流仍正常算出 IRR（独立复算 23.3752%）
  const ok = run('-1000', '500,500,500');
  check('F-N71 合法现金流 IRR=23.3752%', /23\.3752%/.test(ok.res), ok.res.slice(0, 160));
  check('F-N71 合法态含 NPV≈0 结论文案（正确场景）', /NPV 约等于 0/.test(ok.res), ok.res.slice(0, 160));
  // 状态链：无实根 → 合法 → 无实根，结果正确切换
  run('-100', '230,-132.5');
  const chain = run('-1000', '500,500,500');
  check('F-N71 状态链恢复合法结果', /23\.3752%/.test(chain.res), chain.res.slice(0, 160));
  const back = run('-100', '230,-132.5');
  check('F-N71 状态链回退无实根提示', /无法计算 IRR（现金流无实根）/.test(back.res) && !/1000/.test(back.res), back.res.slice(0, 160));
  // 近机器精度重根/边界
  const multi = run('-100', '230,-132.5,10');
  check('F-N71 多变体现金流不崩溃', multi.res.length > 0, multi.res.slice(0, 120));

  console.log(`\nBATCH131 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
