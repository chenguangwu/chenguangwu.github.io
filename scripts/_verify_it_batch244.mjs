// 第244批探测 · 时间示例修正 + IT-N42/N44 复核（time-format-converter / timestamp-converter）
//  示例 1690000000 的正确 UTC 值是 2023-07-22T04:26:40.000Z（旧文档写 08:53:20）
//  N42 裸数字 0/1 走时间戳分支（1970-01-01），不得被 V8 当成年份 2000/2001
//  N44 时区表用 IANA 时区 + Intl 动态 DST，夏季纽约/伦敦偏移正确
// 用法：node scripts/_verify_it_batch244.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 240) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom(file) {
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + file.split('/').pop(),
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const fmt = file => OLD_DIR ? OLD_DIR + '/' + file : 'tools/it/' + file;

// ══════════════ 时间示例权威值（三源） ══════════════
{
  const dom = makeDom(fmt('time-format-converter.html'));
  const body = dom.window.document.body.textContent;
  check('示例用正确 UTC 值 04:26:40', body.indexOf('2023-07-22T04:26:40.000Z') >= 0 && body.indexOf('2023-07-22 12:26:40') >= 0, 'new UTC value present');
  check('示例不再有错误 08:53:20', body.indexOf('08:53:20') < 0, body.indexOf('08:53:20') >= 0 ? 'still wrong' : 'clean');
  // 独立权威值：1690000000 秒 = 04:26:40 UTC（Node Date 复算）
  const utc = new Date(1690000000 * 1000).toISOString();
  check('权威复算 1690000000=04:26:40Z', utc === '2023-07-22T04:26:40.000Z', utc);
  // 三源同步（旧态从备份目录读 JSON，保证判别力）
  const ddPath = OLD_DIR ? OLD_DIR + '/content_deepdive.json' : 'i18n/tools/content_deepdive.json';
  const dd = JSON.stringify(JSON.parse(fs.readFileSync(ddPath,'utf8'))['it/time-format-converter']);
  check('deepdive 权威源示例已改正', dd.indexOf('04:26:40') >= 0 && dd.indexOf('08:53:20') < 0, 'dd checked');
  const enPath = OLD_DIR ? OLD_DIR + '/time-format-converter.json' : 'i18n/tools/en/it/time-format-converter.json';
  const en = fs.readFileSync(enPath,'utf8');
  check('en 映射示例已改正', en.indexOf('04:26:40') >= 0 && en.indexOf('08:53:20') < 0, 'en checked');
}

// ══════════════ N42 裸数字 0/1 走时间戳 ══════════════
{
  const dom = makeDom(fmt('time-format-converter.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('inTime'), out = d.getElementById('out');
  input.value = '0';
  w.convertTime();
  let s = out.textContent.replace(/\s+/g, ' ');
  check('N42 裸数字 0 → 1970 而非 2000', s.indexOf('1970-01-01') >= 0 && s.indexOf('2000-01-01') < 0, s.slice(0, 160));
  input.value = '1';
  w.convertTime();
  s = out.textContent.replace(/\s+/g, ' ');
  check('N42 裸数字 1 → 1970 而非 2001', s.indexOf('1970-01-01') >= 0 && s.indexOf('2001-01-01') < 0, s.slice(0, 160));
  // parseInput 直接断言（避免输出格式差异）
  const p0 = w.parseInput('0'), p1 = w.parseInput('1');
  check('N42 parseInput(0/1) 均为 1970 时间戳', p0 && p1 && p0.getUTCFullYear() === 1970 && p1.getUTCFullYear() === 1970, (p0&&p0.toISOString())+' / '+(p1&&p1.toISOString()));
}

// ══════════════ N44 IANA 时区 + DST ══════════════
{
  const dom = makeDom(fmt('timestamp-converter.html'));
  const w = dom.window, d = w.document;
  // 2026-07-01T12:00:00Z 夏令时：纽约 EDT(-4)=08:00、伦敦 BST(+1)=13:00
  const date = new Date('2026-07-01T12:00:00Z');
  const ny = w.formatInZone(date, 'America/New_York');
  const ld = w.formatInZone(date, 'Europe/London');
  check('N44 夏令时纽约 EDT 显示 08:00', /08:00/.test(ny), ny);
  check('N44 夏令时伦敦 BST 显示 13:00', /13:00/.test(ld), ld);
  // 冬季标准时回归：2026-01-01T12:00:00Z 纽约 EST(-5)=07:00
  const winter = new Date('2026-01-01T12:00:00Z');
  const nyW = w.formatInZone(winter, 'America/New_York');
  check('N44 冬季纽约 EST 显示 07:00', /07:00/.test(nyW), nyW);
  // TIMEZONES 表用 IANA 名而非固定偏移
  const src = fs.readFileSync(fmt('timestamp-converter.html'),'utf8');
  check('N44 时区表为 IANA 标识', src.indexOf("America/New_York") >= 0 && src.indexOf("Europe/London") >= 0 && /timeZone\s*:/.test(src), 'IANA zones present');
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
