// 第222批 · IT-N191~N195 unit-converter-advanced（JSDOM 真机 + 独立复算）
//  N191 温度「℃」预设被校验直接拒绝
//  N192 文档承诺「压强与能量」，UI 下拉与因子表都没有
//  N193 极小值被 toFixed(6)+去零吞成 0（进批探测：已由其他 Agent 修好，补证据）
//  N194 数值框清空/非法输入静默当 0；温度大小写敏感；用户输入直接进 innerHTML（本批加固 XSS）
//  N195 长度表用 nm 表海里（进批探测：已修 nm=1e-9 / nmi=1852，本批补 um）
// 用法：node scripts/_verify_it_batch222.mjs [可选：另一个页面路径，用于旧源码差分]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.argv[2] || 'tools/it/unit-converter-advanced.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) {
  checks.push([n, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : ''));
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

let tableData = null, exportCalls = [], history = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/unit-converter-advanced.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable(sel, name) { exportCalls.push({ sel, name, rows: tableData && tableData.rows }); }, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: {
        table(sel, cfg) {
          tableData = cfg;
          const el = w.document.querySelector(sel);
          if (el) el.innerHTML = '<tr><th>' + cfg.head.map(esc).join('</th><th>') + '</th></tr>' +
            cfg.rows.map(r => '<tr><td>' + r.map(esc).join('</td><td>') + '</td></tr>').join('');
        }
      },
      preset: { bar() {} },
      history: {
        list() { return history.slice(); },
        last() { return history.length ? history[0].d : null; },
        record(r) { history.unshift({ t: Date.now(), d: r }); },
        mount() {}, clear() { history = []; }
      }
    };
  }
});
const w = dom.window, d = w.document;
const $ = id => d.getElementById(id);

function calc(cat, val, from) {
  $('cat').value = cat;
  $('val').value = String(val);
  $('from').value = from;
  w.calcTool();
  return { text: String($('result').textContent ?? ''), html: String($('result').innerHTML ?? '') };
}
// 从 data-grid 卡片里按 label 取数值
function card(r, label) {
  const m = r.html.match(new RegExp('<div class="num"[^>]*>([^<]*)</div><div class="label">' + label + '</div>'));
  return m ? m[1] : null;
}
const near = (a, b, tol = 1e-4) => a !== null && Math.abs(Number(a) - b) <= tol;

// ══════════════ N191 温度别名归一 ══════════════
const t1 = calc('temp', 100, '℃');
check('N191 预设「℃」不再被拒，100℃ → 212.00°F / 373.15K',
  /212\.00/.test(t1.text) && /373\.15/.test(t1.text) && !/温度单位请用/.test(t1.text), t1.text.slice(0, 90));
check('N191 ℃ 结果只出 2 张目标卡（归一后的 from 参与去重）',
  (t1.html.match(/data-card/g) || []).length === 2, 'cards=' + (t1.html.match(/data-card/g) || []).length);
check('N191 °C 别名等价 C', /212\.00/.test(calc('temp', 100, '°C').text), '');
check('N191 ℉ 别名等价 F（212℉ → 100℃）', /100\.00/.test(calc('temp', 212, '℉').text), '');
check('N191 小写 c 不区分大小写', /212\.00/.test(calc('temp', 100, 'c').text), '');
check('N191 非法温度单位仍给出明确提示', /温度单位请用/.test(calc('temp', 100, 'rankine').text), '');
check('N191 normTempUnit 覆盖 6 种写法', typeof w.normTempUnit === 'function' &&
  ['C', 'c', '℃', '°C', 'CELSIUS'].every(x => w.normTempUnit(x) === 'C') &&
  ['F', '℉', '°F'].every(x => w.normTempUnit(x) === 'F') && w.normTempUnit('K') === 'K', typeof w.normTempUnit);

// ══════════════ N192 压强 / 能量两类 ══════════════
const opts = [...d.querySelectorAll('#cat option')].map(o => o.value);
check('N192 下拉含 pressure 与 energy', opts.includes('pressure') && opts.includes('energy'), opts.join(','));
const p1 = calc('pressure', 1, 'bar');
check('N192 1 bar = 100000 Pa（结果不再是不可选项报错）',
  !/不支持单位/.test(p1.text) && card(p1, 'pa') === '100000', JSON.stringify(p1.text.slice(0, 100)));
// 独立复算：1 psi = 1 lbf/in² = 4.4482216152605 N / (0.0254 m)² = 6894.757293168... Pa
const psiFromDef = 4.4482216152605 / (0.0254 * 0.0254);
check('N192 1 bar 的 psi 与 lbf/in² 定义独立复算一致',
  near(card(p1, 'psi'), 1e5 / psiFromDef, 1e-4), 'got=' + card(p1, 'psi') + ' expect=' + (1e5 / psiFromDef).toFixed(6));
check('N192 1 atm = 101325 Pa（精确定义）', card(calc('pressure', 1, 'atm'), 'pa') === '101325', '');
check('N192 1 Torr = 101325/760 Pa（精确定义）',
  near(card(calc('pressure', 760, 'torr'), 'pa'), 101325, 1e-3), '');
const e1 = calc('energy', 1, 'kwh');
check('N192 1 kWh = 3600000 J（精确定义）',
  !/不支持单位/.test(e1.text) && card(e1, 'j') === '3600000', JSON.stringify(e1.text.slice(0, 100)));
check('N192 1 kWh 的 cal 与 1 cal = 4.184 J 独立复算一致',
  near(card(e1, 'cal'), 3.6e6 / 4.184, 1e-4), 'got=' + card(e1, 'cal'));
check('N192 1 kWh 的 BTU 与 1 BTU_IT = 1055.05585262 J 独立复算一致',
  near(card(e1, 'btu'), 3.6e6 / 1055.05585262, 1e-4), 'got=' + card(e1, 'btu'));
const evCard = card(calc('energy', 1, 'j'), 'ev');
const eVExpect = 1 / 1.602176634e-19;
check('N192 1 eV = 1.602176634e-19 J（2019 SI 定义）',
  near(Number(evCard) / eVExpect, 1, 1e-5), 'got=' + evCard + ' expect=' + eVExpect.toExponential(6));
check('N192 大数结果用科学计数，不输出 ≥15 位伪精度整数',
  /e\+/.test(String(evCard)) && !/^\d{15,}$/.test(String(evCard)), 'ev=' + evCard);

// ══════════════ N193 小值科学计数（已修补证据） ══════════════
const small = calc('data', 1, 'bit');
check('N193 1 bit → GB 不再显示 0', card(small, 'GB') !== '0' && /e-/.test(String(card(small, 'GB'))),
  'GB=' + card(small, 'GB'));
check('N193 1 bit → GB 与 0.125/2³⁰ 独立复算一致（指数形态）',
  Math.abs(Number(card(small, 'GB')) - 0.125 / 1073741824) < 1e-15, 'GB=' + card(small, 'GB'));
check('N193 1 nm → m 为 1e-9', card(calc('length', 1, 'nm'), 'm') === '1e-9', '');

// ══════════════ N194 空值 / XSS / 状态链 ══════════════
check('N194 数值框清空不再静默当 0 换算',
  /请输入有效数值/.test(calc('length', '', 'km').text) && (calc('length', '', 'km').html.match(/data-card/g) || []).length === 0, '');
check('N194 非法数值 abc 不再静默当 0 换算', /请输入有效数值/.test(calc('length', 'abc', 'km').text), '');
check('N194 非有限值 Infinity 不再静默当 0 换算', /请输入有效数值/.test(calc('length', 'Infinity', 'km').text), '');
const xss = calc('mass', 1, '<img src=x onerror=N222XSS>');
check('N194 用户输入的尖括号进结果区前已转义（无裸 img 标签）',
  !/<img/i.test(xss.html) && /&lt;img/i.test(xss.html) && /N222XSS/.test(xss.html), xss.html.slice(0, 140));
check('N194 原型链键 __proto__ 不再被当作合法单位',
  /不支持单位/.test(calc('mass', 1, '__proto__').text), '');
check('N194 页面 </div 未闭合残留已修', !/<\/div(?![^>]*>)/.test(html), '');
// 合法 → 非法 → 恢复
calc('length', 5, 'km');
const okOut = String($('result').textContent ?? '');
calc('length', '', 'km');
calc('length', 7, 'km');
const recover = String($('result').textContent ?? '');
check('N194 状态链 合法→非法→恢复 结果随输入更新且不残留非法态',
  /1000|5000/.test(okOut) && !/请输入有效数值/.test(recover) && recover !== okOut, recover.slice(0, 70));

// ══════════════ N195 长度单位语义（已修补证据 + um） ══════════════
check('N195 nm = 纳米 1e-9 m（不再是海里）', card(calc('length', 1, 'nm'), 'm') === '1e-9', '');
check('N195 nmi = 国际海里 1852 m', card(calc('length', 1, 'nmi'), 'm') === '1852', '');
// 1e-6 恰好等于阈值（判据是「小于 1e-6」），走 toFixed 分支显示 0.000001，两种形态都合法
check('N195 补 um = 微米 1e-6 m', Number(card(calc('length', 1, 'um'), 'm')) === 1e-6,
  'um→m=' + card(calc('length', 1, 'um'), 'm'));

// ══════════════ 全链路 / 导出 ══════════════
history = []; tableData = null; exportCalls = [];
// 全站历史模板有 1s 节流（防同一批重复记录）；这里模拟真实用户操作间隔，重置节流时钟
w.eval('__unit_converter_advanced_last=0');
calc('pressure', 2, 'bar');
const chainOut = String($('result').textContent ?? '');
check('链路 压强输入产出真实结果', /200000/.test(chainOut), chainOut.slice(0, 80));
check('链路 历史记录取自 #result 且表格含「结果」列', history.length >= 1 &&
  !!tableData && tableData.head.includes('结果') &&
  tableData.rows.some(r => r.some(c => String(c).includes('200000'))), 'hist=' + history.length);
w.__unit_converter_advancedExport();
check('链路 导出走明细表且携带结果行', exportCalls.length >= 1 &&
  exportCalls[0].sel === '#unit_converter_advancedTable' &&
  (exportCalls[0].rows || []).some(r => r.some(c => String(c).includes('200000'))), 'exports=' + exportCalls.length);
let seqErr = null;
try { calc('mass', 3, 'kg'); calc('energy', 4, 'kj'); } catch (e) { seqErr = e.message; }
check('链路 快速连续不同类别输入无异常且末次生效', seqErr === null &&
  /4000/.test(String($('result').textContent ?? '')), seqErr || '');
w.resetForm();
check('链路 重置回到 length/1/km 默认值', $('cat').value === 'length' && $('val').value === '1' &&
  /1000/.test(String($('result').textContent ?? '')), '');

// ══════════════ 公式 / i18n 三源 ══════════════
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/unit-converter-advanced.json', 'utf8'));
const f = html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
check('公式 页面说明已含别名归一/小值/压强与能量因子', !!f &&
  /℃、°C 视为 C/.test(f[1]) && /1e-6 的非零结果改用科学计数法/.test(f[1]) &&
  /6894\.757293168/.test(f[1]) && /1\.602176634e-19/.test(f[1]), f ? f[1].slice(0, 60) : 'missing');
check('公式 en JSON 含同文中文键与英译（旧「keep 6 decimals」口径已清）', !!f && !!en.map[f[1]] &&
  /case-insensitive/.test(en.map[f[1]]) && /scientific notation/.test(en.map[f[1]]) &&
  !Object.values(en.map).some(v => /results keep 6 decimals and trailing zeros are trimmed/.test(v)),
  f ? String(en.map[f[1]] || '').slice(0, 60) : 'no formula');
const genUi = fs.readFileSync('js/tool-i18n-en.js', 'utf8');
check('i18n GEN_UI_MAP 已含「压强」英译', /'压强':'Pressure'/.test(genUi) && /'能量':'Energy'/.test(genUi), '');

// ══════════════ EN 态动态串零 CJK ══════════════
const domEn = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/unit-converter-advanced.html?lang=en-US',
  beforeParse(we) {
    we.ToolBox = { showToast() {}, copyText() {} };
    we.TBKit = {
      util: { isEn: () => true, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, last() { return null; }, record() {}, mount() {} }
    };
  }
});
const we = domEn.window, de = we.document;
function enCalc(cat, val, from) {
  de.getElementById('cat').value = cat;
  de.getElementById('val').value = String(val);
  de.getElementById('from').value = from;
  we.calcTool();
  return String(de.getElementById('result').textContent ?? '');
}
const CJK = /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/;
const enCases = [enCalc('length', '', 'km'), enCalc('temp', 100, 'rankine'), enCalc('mass', 1, 'nope')];
check('EN 态三条动态结果串零 CJK（空值/温度单位/不支持单位）',
  enCases.every(t => !CJK.test(t)) && enCases.every(t => /Conversion result/.test(t)),
  enCases.map(t => t.slice(0, 55)).join(' | '));

// ══════════════ 汇总 ══════════════
const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exit(1);
}
