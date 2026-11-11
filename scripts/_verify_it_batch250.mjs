// 第250批探测 · IT-N130/N131/N132（bluetooth-version）
//  N130 两个版本下拉框与场景下拉框均有 option（复核）
//  N131 所有可选项都有独立数据，4.0 不再静默回退 5.3
//  N132 meta/og/twitter/JSON-LD 描述去重
// 用法：node scripts/_verify_it_batch250.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.__result = '';
  w.ToolBox = {
    showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s),
    setResult(id, html) { w.__result = String(html); }
  };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom() {
  const file = OLD_DIR ? OLD_DIR + '/bluetooth-version.html' : 'tools/it/bluetooth-version.html';
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/bluetooth-version.html',
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const page = () => OLD_DIR ? OLD_DIR + '/bluetooth-version.html' : 'tools/it/bluetooth-version.html';

// ══════════════ N130 下拉框选项（复核） ══════════════
{
  const dom = makeDom(), d = dom.window.document;
  for (const id of ['v', 'v2', 'scene']) {
    const sel = d.getElementById(id);
    check('N130 #' + id + ' 有可选项', sel && sel.options.length >= 3, sel ? 'n=' + sel.options.length : 'missing');
  }
}

// ══════════════ N131 版本数据覆盖 ══════════════
{
  const dom = makeDom(), w = dom.window, d = w.document;
  const opts = Array.from(d.getElementById('v').options).map(o => o.value);
  let info = null;
  try { info = w.eval('BT_INFO'); } catch (e) {}
  check('N131 版本数据唯一源存在', !!info, info ? 'BT_INFO' : 'missing');
  if (info) {
    const missing = opts.filter(v => !info[v]);
    check('N131 每个选项都有独立数据', missing.length === 0, missing.length ? 'missing=' + missing.join(',') : 'all ' + opts.length + ' covered');
  }
  // 4.0 必须显示 4.0 自身的 BLE 引入说明，而不是 5.3 的回退文案。
  d.getElementById('v').value = '4.0';
  d.getElementById('v2').value = '5.0';
  w.calcTool();
  const html = w.__result;
  check('N131 4.0 不再回退 5.3', /BLE 低功耗引入/.test(html) && !/连接子评级/.test(html), html.slice(0, 140));
  // 未知版本明确报错而不是静默回退。
  const sel = d.getElementById('v');
  Object.defineProperty(sel, 'value', { get: () => '9.9', configurable: true });
  w.calcTool();
  check('N131 未知版本明确报错', /未知蓝牙版本/.test(w.__result), w.__result.slice(0, 100));
}

// ══════════════ N132 SEO 描述去重 ══════════════
{
  const html = fs.readFileSync(page(), 'utf8');
  check('N132 重复描述已清零', !/蓝牙版本速查是一款免费的在线IT 开发工具，蓝牙版本速查/.test(html), 'checked');
  check('N132 新描述落地', (html.match(/蓝牙版本速查：对比各蓝牙版本的速率、距离与核心特性/g) || []).length >= 4, 'checked');
}

// ══════════════ 英文映射覆盖 ══════════════
{
  const dom = makeDom(), w = dom.window;
  let info = null;
  try { info = w.eval('BT_INFO'); } catch (e) {}
  const pairs = info ? Object.values(info).flat() : [];
  const en = JSON.parse(fs.readFileSync(OLD_DIR ? OLD_DIR + '/bluetooth-version.en.json' : 'i18n/tools/en/it/bluetooth-version.json', 'utf8')).map;
  const miss = pairs.filter(s => /[\u4e00-\u9fff]/.test(s) && !en[s]);
  check('版本数据英文映射齐全', miss.length === 0, miss.length ? miss.join(' | ') : 'all mapped');
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
