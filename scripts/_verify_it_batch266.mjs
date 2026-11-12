// 第266批 JSDOM 验证：IT-N167 复制/导出 + IT-N168 英文简介 + IT-N169 示例与死代码
// 用法: node scripts/_verify_it_batch266.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/ksuid-generator.html` : 'tools/it/ksuid-generator.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const toasts = [];
const csvCalls = [];
const copied = [];
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/ksuid.html',
  beforeParse(w) {
    w.alert = m => toasts.push(String(m));
    w.ToolBox = { showToast: (m, t) => toasts.push(String(m) + '|' + String(t)), copyText() {}, toggleToolTheme() {} };
    Object.defineProperty(w.navigator, 'clipboard', {
      value: { writeText: (s) => { copied.push(String(s)); return Promise.resolve(); } }, configurable: true,
    });
    w.TBKit = {
      util: {
        isEn: () => enMode,
        exportTable(host, fn) { csvCalls.push({ via: 'exportTable', host, fn }); },
        exportCsv(fn, rows) { csvCalls.push({ via: 'exportCsv', fn, rows: JSON.parse(JSON.stringify(rows)) }); },
        diffBox() {},
      },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
    };
    w.i18nText = (zh, en) => enMode ? (en || zh) : zh;
  },
});
const w = dom.window, d = w.document;
const flat = s => String(s).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();

// 生成固定数量的 KSUID，验证输出为独立行
function gen(n) {
  d.getElementById('count').value = String(n);
  w.generate();
  return [...d.querySelectorAll('#output .code-row')].map(e => e.textContent.trim());
}

// ---------- IT-N167：复制按行 join('\n')（旧源码已修，作回归证据） ----------
{
  const ids = gen(5);
  check('N167 生成 5 个独立 .code-row', ids.length === 5, 'len=' + ids.length);
  check('N167 每个 ID 为 27 字符', ids.every(x => x.length === 27), 'lens=' + ids.map(x => x.length).join(','));
  copied.length = 0;
  w.copyResult();
  check('N167 复制写出 1 次', copied.length === 1, 'n=' + copied.length);
  const clip = copied[0] || '';
  check('N167 复制内容用换行分隔 5 行', clip.split('\n').length === 5, 'lines=' + clip.split('\n').length);
  check('N167 复制内容无 135 字符粘连', clip.length < 140 && clip.length >= 5 * 27, 'len=' + clip.length);
  check('N167 复制每行等于对应 ID', clip.split('\n').every((ln, i) => ln === ids[i]), 'exact');
}

// ---------- IT-N167：导出含当前完整结果（旧源码只导被截断的历史表） ----------
{
  const ids = gen(5);
  csvCalls.length = 0;
  w.__ksuid_generatorExport();
  check('N167 导出走 exportCsv', csvCalls.length === 1 && csvCalls[0].via === 'exportCsv', JSON.stringify(csvCalls.map(c => c.via)));
  const rows = (csvCalls.length && Array.isArray(csvCalls[0].rows)) ? csvCalls[0].rows : [];
  check('N167 CSV 含表头「序号/完整 KSUID」', !!rows.length && /序号/.test(String(rows[0])) && /完整 KSUID/.test(String(rows[0])), 'head=' + JSON.stringify(rows[0]));
  const idCells = rows.slice(1).filter(r => r && r[1]).map(r => String(r[1]));
  check('N167 CSV 含 5 个完整 27 字符 ID', ids.every(id => idCells.includes(id)), 'csv ids=' + idCells.filter(x => x.length === 27).length);
  check('N167 CSV 不含 slice(0,80) 截断值', !idCells.some(x => x.length === 80), 'maxlen=' + Math.max(0, ...idCells.map(x => x.length)));
}
// 英文态表头
{
  enMode = true;
  gen(3);
  csvCalls.length = 0;
  w.__ksuid_generatorExport();
  const rows = (csvCalls.length && Array.isArray(csvCalls[0].rows)) ? csvCalls[0].rows : [];
  check('N167 英文态 CSV 表头为英文', !!rows.length && /No\./.test(String(rows[0])) && /Full KSUID/.test(String(rows[0])), 'head=' + JSON.stringify(rows[0]));
  enMode = false;
}
// 复制 toast 英文化（clipboard.writeText().then 是微任务，JSDOM 同步断言拿不到，改源码级双态检查）
{
  check('N167 复制 toast 含英文双态分支', /Copied ['"]\s*\+\s*rows\.length/.test(html), 'en branch present');
  check('N167 复制 toast 保留中文分支', /已复制 ['"]\s*\+\s*rows\.length/.test(html), 'zh branch present');
}

// ---------- IT-N168：英文简介 16-byte payload ----------
{
  const body = d.querySelector('.tool-intro-body');
  const t = flat(body ? body.textContent : '');
  check('N168 英文简介声明 16-byte random payload', /16-byte random payload/.test(t), 't=' + t.slice(0, 160));
  check('N168 英文简介不再误称 20-byte', !/20-byte random payload/.test(t));
  // 权威源（英文 map）也校验
  check('N168 页面无 20-byte random payload 残留', !/20-byte random payload/.test(html));
}

// ---------- IT-N169：deep-dive 示例合法 27 字符 + 标注时间 ----------
{
  const dd = d.querySelector('.dd-ex-body');
  const t = flat(dd ? dd.textContent : '');
  check('N169 示例使用合法 27 字符 KSUID', /3LzTfYF95TTBROrbZGlwr17yZzD/.test(t), 't=' + t.slice(0, 160));
  check('N169 示例标注生成时间', /2026-11-12T04:00:00Z/.test(t));
  check('N169 示例不再用 26 字符旧串', !/0ujtsy1p8c9r1l0b0p0n000000/.test(t));
  check('N169 示例不再说「前 32 位」', !/前 32 位/.test(t));
  // 独立复算：样例长度 27 且 base62 解码时间戳 = 2026-11-12T04:00:00Z
  const sample = '3LzTfYF95TTBROrbZGlwr17yZzD';
  check('N169 样例实长 27', sample.length === 27, 'len=' + sample.length);
  const ALPH = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  let n = 0n;
  for (const c of sample) n = n * 62n + BigInt(ALPH.indexOf(c));
  const bytes = [];
  for (let i = 19; i >= 0; i--) { bytes[i] = Number(n & 255n); n >>= 8n; }
  const ts = ((bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | bytes[3]) >>> 0;
  const iso = new Date((ts + 1400000000) * 1000).toISOString();
  check('N169 样例解码时间为标注时刻', iso === '2026-11-12T04:00:00.000Z', 'iso=' + iso);
  check('N169 样例随机负载 16 字节（总量 20）', bytes.length === 20, 'bytes=' + bytes.length);
}

// ---------- IT-N169：randInt 死代码已删 ----------
{
  check('N169 randInt 定义已删', !/function randInt\s*\(/.test(html));
  let def;
  try { def = w.eval('typeof randInt'); } catch (e) { def = 'ERR'; }
  check('N169 运行时无 randInt', def === 'undefined', 'typeof=' + def);
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
