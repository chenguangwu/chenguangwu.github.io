// 第204批 · IT-N256/N257 device-info 快照趋势标量 + 复制全部换行（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/device-info.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

let copied = '', records = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/device-info.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = (k, fb) => (fb != null ? fb : '');
    w.ToolBox = { copyText() {}, showToast() {}, toggleToolTheme() {}, downloadText() {} };
    Object.defineProperty(w.navigator, 'clipboard', { configurable: true, value: { writeText(t) { copied = String(t); return Promise.resolve(); } } });
    w.TBKit = {
      util: { isEn: () => false, exportTable() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      history: {
        list() { return records.map((d, i) => ({ t: Date.now() - i * 1000, d })); },
        record(d) { records.unshift(Object.assign({}, d)); },
        diffLast(keys) {
          if (records.length < 2) return null;
          const o = {};
          for (const k of keys) o[k] = { delta: (records[0][k] || 0) - (records[1][k] || 0) };
          return o;
        },
        last() { return records[0] || null; },
        mount() {}, clear() { records = []; }
      }
    };
    w.console = { warn() {}, log() {}, error() {} };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

// ── IT-N256：__v 不再是恒定核心数，改为视口面积 ──
{
  const r = w.__tbDevRec();
  check('__v 等于视口面积 innerWidth*innerHeight', r.__v === w.innerWidth * w.innerHeight, '__v=' + r.__v + ' vw/vh=' + w.innerWidth + '/' + w.innerHeight);
  check('快照含视口字段', typeof r['视口'] === 'string' && r['视口'].indexOf('x') >= 0, JSON.stringify(r['视口']));
  // 改视口 → __v 变化（趋势不再水平线）
  const before = w.__tbDevRec().__v;
  w.innerWidth = 1234; w.innerHeight = 567;
  const after = w.__tbDevRec().__v;
  check('视口变化 → __v 变化', after === 1234 * 567 && after !== before, 'before=' + before + ' after=' + after);
  // 两次快照 __v 不同 → diffLast delta 非零
  w.innerWidth = 800; w.innerHeight = 600; w.__tbDevSave();
  w.innerWidth = 1024; w.innerHeight = 768; w.__tbDevSave();
  check('两次快照 __v 不同（对比非零）', records.length >= 2 && records[0].__v !== records[1].__v, JSON.stringify(records.map(r => r.__v)));
}

// ── IT-N257：复制全部逐条 label: value 换行 ──
{
  copied = '';
  w.__tbDevCopy();
  check('复制内容按行分隔（含换行）', copied.indexOf('\n') >= 0 && copied.split('\n').length >= 5, 'lines=' + copied.split('\n').length);
  check('每行是 label: value 格式', /^[^:]+: .+/.test(copied.split('\n')[0]), JSON.stringify(copied.split('\n')[0]));
  check('label 与数值间有冒号空格（不再粘连）', copied.indexOf('屏幕分辨率: ') >= 0 || copied.indexOf('分辨率: ') >= 0, JSON.stringify(copied.slice(0, 60)));
  check('含 UserAgent 块', copied.indexOf('UserAgent:') >= 0);
  check('无整块粘连（单行超长）', copied.split('\n').every(l => l.length < 200), 'maxlen=' + Math.max(...copied.split('\n').map(l => l.length)));
}

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
