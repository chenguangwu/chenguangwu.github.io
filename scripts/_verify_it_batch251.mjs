// 第251批探测 · IT-N133/N134/N135（usb-version）
//  N133 三个下拉框有 option（复核）
//  N134 版本数据覆盖 1.0/1.1，USB-C 2.0 不再误判「仅承载较低速率」
//  N135 3.1 明确 Gen2=10Gbps / Gen1=5Gbps，符合更名口径
// 用法：node scripts/_verify_it_batch251.mjs [旧页目录]
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
  const file = OLD_DIR ? OLD_DIR + '/usb-version.html' : 'tools/it/usb-version.html';
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/usb-version.html',
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const page = () => OLD_DIR ? OLD_DIR + '/usb-version.html' : 'tools/it/usb-version.html';

// ══════════════ N133 下拉选项（复核） ══════════════
{
  const dom = makeDom(), d = dom.window.document;
  for (const id of ['v', 'v2', 'conn']) {
    const sel = d.getElementById(id);
    check('N133 #' + id + ' 有可选项', sel && sel.options.length >= 3, sel ? 'n=' + sel.options.length : 'missing');
  }
}

// ══════════════ N134 数据覆盖 + USB-C 口径 ══════════════
{
  const dom = makeDom(), w = dom.window, d = w.document;
  const opts = Array.from(d.getElementById('v').options).map(o => o.value);
  let info = null;
  try { info = w.eval('USB_INFO'); } catch (e) {}
  check('N134 版本数据唯一源存在', !!info, info ? 'USB_INFO' : 'missing');
  if (info) {
    const need = ['1.0', '1.1', '2.0', '3.0', '3.1', '3.2', '4.0'];
    const missing = need.filter(v => !opts.includes(v) || !info[v]);
    check('N134 1.0/1.1 等版本全有数据', missing.length === 0, missing.length ? 'missing=' + missing.join(',') : 'all 7 covered');
  }
  d.getElementById('v').value = '1.1';
  d.getElementById('v2').value = '2.0';
  w.calcTool();
  const grid = String(w.__result).split('<div style="margin-top')[0];
  check('N134 1.1 不再回退 3.2', /12 Mbps/.test(grid) && !/20 Gbps/.test(grid), grid.slice(0, 140));
  d.getElementById('v').value = '2.0';
  d.getElementById('conn').value = 'usbc';
  w.calcTool();
  check('N134 USB2.0+USB-C 不再说较低速率', /USB 2.0 全速（480 Mbps）/.test(w.__result) && !/仅承载较低速率/.test(w.__result), w.__result.slice(0, 200));
}

// ══════════════ N135 3.1 Gen1/Gen2 口径 ══════════════
{
  const html = fs.readFileSync(page(), 'utf8');
  check('N135 页面无裸 3.1=10G 说法', !/3\.1 10G\b/.test(html), 'checked');
  check('N135 明确 Gen2/Gen1 区分', /3\.1 Gen2（10 Gbps）/i.test(html) && /Gen1 为 5 Gbps/.test(html), 'checked');
  const dom = makeDom(), w = dom.window, d = w.document;
  d.getElementById('v').value = '3.1';
  d.getElementById('v2').value = '2.0';
  w.calcTool();
  check('N135 3.1 结果标注 Gen2 且提示 Gen1', /10 Gbps（Gen2；Gen1 为 5 Gbps）/.test(w.__result), w.__result.slice(0, 160));
}

// ══════════════ 英文映射覆盖 ══════════════
{
  const dom = makeDom(), w = dom.window;
  let info = null;
  try { info = w.eval('USB_INFO'); } catch (e) {}
  const pairs = info ? Object.values(info).flat() : [];
  const en = JSON.parse(fs.readFileSync(OLD_DIR ? OLD_DIR + '/usb-version.en.json' : 'i18n/tools/en/it/usb-version.json', 'utf8')).map;
  const miss = pairs.filter(s => /[\u4e00-\u9fff]/.test(s) && !en[s]);
  check('版本数据英文映射齐全', miss.length === 0, miss.length ? miss.join(' | ') : 'all mapped');
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
