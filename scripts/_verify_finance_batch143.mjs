// F-N30 已修未删核实：NPV 页清空初始投资后的状态链（stats/detail/chart/导出/历史）。
// 真机 JSDOM：runScripts:'dangerously' + TBKit 桩 + 真实 input/click。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const ROOT = new URL('..', import.meta.url).pathname;
const HTML = fs.readFileSync(ROOT + 'tools/finance/npv-calculator.html', 'utf8');
let pass = 0, fail = 0;
const check = (name, ok, extra = '') => {
  if (ok) { pass++; console.log('PASS ' + name); }
  else { fail++; console.log('FAIL ' + name + (extra ? ' | ' + extra : '')); }
};

// TBKit 桩：history 真实契约 list()->[{t,d}] / last()->d / record({...})->{t,d}
function makeDom() {
  const hist = [];
  const tb = {
    util: { isEn: () => false, diffBox: () => {} },
    history: {
      list: () => hist.slice(),
      last: () => (hist.length ? hist[hist.length - 1].d : null),
      record: (rec) => { hist.push({ t: Date.now(), d: rec }); },
      mount: () => {},
    },
    matrix: { table: () => {} },
    chart: { line: () => {} },
  };
  const dom = new JSDOM(HTML, {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    beforeParse(w) {
      w.TBKit = tb;
      w.ToolBox = {
        showToast: () => {}, downloadText: (name, text) => { w.__lastDownload = { name, text }; },
        toggleToolTheme: () => {}, escHtml: (s) => String(s),
      };
      w.HTMLCanvasElement.prototype.getContext = () => ({ clearRect(){}, scale(){}, beginPath(){}, moveTo(){}, lineTo(){}, stroke(){}, fillText(){}, fillRect(){}, arc(){}, closePath(){}, setLineDash(){}, save(){}, restore(){}, measureText:()=>({width:0}) });
      Object.defineProperty(w.HTMLCanvasElement.prototype, 'clientWidth', { get(){return 600;} });
      Object.defineProperty(w.HTMLCanvasElement.prototype, 'clientHeight', { get(){return 300;} });
    },
  });
  return { dom, w: dom.window, hist };
}

const { w, hist } = makeDom();
const d = w.document;
const $ = (id) => d.getElementById(id);
const text = (id) => ($(id)?.textContent || '').replace(/\s+/g, ' ').trim();

// 1) 合法计算：初始 10000 / 10% / 四期 +3000 ⇒ 有明细、有统计
$('init').value = '10000';
$('rate').value = '10';
w.eval('calc()');
check('合法态：统计卡有 NPV', text('stats').includes('NPV 净现值'));
check('合法态：明细表有第0期', text('detail').includes('第0期'));

// 2) 状态切换：清空初始投资（真实 input 事件驱动 calc）
$('init').value = '0';
w.eval('calc()');
check('清空后：stats 显示请输入初始投资', text('stats').includes('请输入初始投资'));
check('清空后：detail 无旧明细（第0期消失）', !text('detail').includes('第0期'));
check('清空后：detail 明示明细与导出已清空', text('detail').includes('明细与导出已清空'));

// 3) 导出拦截：清空后 exportCSV 不触发下载
w.__lastDownload = null;
w.eval('exportCSV()');
check('清空后：exportCSV 不下载', w.__lastDownload === null);

// 4) 历史 score：清空后 ResText 含「请输入」⇒ score=0（拒绝态不记通过）
w.eval('__npv_calculator_last=0'); // 绕过 1 秒节流
w.eval('__npv_calculatorExtras()');
if (hist.length) {
  const lastScore = hist[hist.length - 1].d.__tbScore;
  check('清空后：历史 __tbScore=0（拒绝态）', lastScore === 0, 'score=' + lastScore);
} else {
  check('清空后：历史写入拒绝态', false, '无历史记录');
}

// 5) 恢复：重新输入合法值 ⇒ 明细回来
$('init').value = '8000';
$('rate').value = '10';
w.eval('calc()');
check('恢复后：明细表重新出现第0期', text('detail').includes('第0期'));

console.log(`\nBATCH143 ALL PASS | ${pass + fail} checks | pass=${pass} fail=${fail}`);
process.exit(fail ? 1 : 0);
