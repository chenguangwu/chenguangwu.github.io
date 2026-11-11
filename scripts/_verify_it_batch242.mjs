// 第242批探测 · IT-N308/N309/N311/N312（country-flag / decimal-encode）
//  N308 引据表无「国际区号 / E.164 / dial」承诺，口径统一为 ISO 3166-1
//  N309 仅收录 48 国时，无结果须明确提示（中英双语）
//  N311 文档口径统一为 UTF-8 字节，「中」= 228 184 173 而非码点 20013
//  N312 解码严格 /^\d+$/ 校验，65x / 0x41 必须拒绝
// 用法：node scripts/_verify_it_batch242.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 240) : ''));
}
function stub(w, state) {
  w.alert = (m) => { state.alerts.push(String(m)); };
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
  w.TBKit = {
    util: { isEn: () => state.en, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
  w.TextEncoder = globalThis.TextEncoder;
  w.TextDecoder = globalThis.TextDecoder;
}
function makeDom(file, state) {
  const html = fs.readFileSync(file, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + file.split('/').pop(),
    beforeParse: (w) => stub(w, state)
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, html };
}
const dir = (name) => OLD_DIR ? OLD_DIR + '/' + name : 'tools/it/' + name;

// ══════════════ N308 引据表口径 ══════════════
{
  const { html } = makeDom(dir('country-flag.html'), { alerts: [], en: false });
  const hasOldPromise = /国际区号|E\.164|Dialing code|dialing code|顶级域/.test(html);
  check('N308 页面无国际区号/E.164/顶级域承诺', !hasOldPromise, hasOldPromise ? 'still present' : 'clean');
  const hasIso = html.indexOf('ISO 3166-1') >= 0 || html.indexOf('ISO 国家代码') >= 0;
  check('N308 引据表改为 ISO 3166-1 口径', hasIso, hasIso ? 'ISO present' : 'ISO missing');
  const hasDialField = /\bdial\s*:/.test(html);
  check('N308 数据无 dial 空承诺字段', !hasDialField, hasDialField ? 'dial field found' : 'no dial field');
}

// ══════════════ N309 无结果提示（中文态） ══════════════
{
  const state = { alerts: [], en: false };
  const { dom } = makeDom(dir('country-flag.html'), state);
  const w = dom.window, d = w.document;
  d.getElementById('search').value = '巴基斯坦';
  w.render();
  const grid = d.getElementById('grid').innerHTML;
  const count = d.getElementById('count').textContent;
  check('N309 无结果提示明确收录范围', grid.indexOf('未找到匹配项') >= 0 && grid.indexOf('48') >= 0, grid.slice(0, 160));
  check('N309 计数附收录范围说明', count.indexOf('48') >= 0 && count.indexOf('0 个国家/地区') >= 0, count.slice(0, 120));
  d.getElementById('search').value = 'CN';
  w.render();
  const grid2 = d.getElementById('grid').innerHTML;
  const count2 = d.getElementById('count').textContent;
  check('N309 有结果时不显示空态提示', grid2.indexOf('未找到匹配项') < 0 && count2.indexOf('仅收录') < 0 && grid2.indexOf('country-card') >= 0, count2.slice(0, 80));
}

// ══════════════ N309 无结果提示（英文态零 CJK） ══════════════
{
  const state = { alerts: [], en: true };
  const { dom } = makeDom(dir('country-flag.html'), state);
  const w = dom.window, d = w.document;
  d.getElementById('search').value = 'Pakistan';
  w.render();
  const grid = d.getElementById('grid').innerHTML;
  const count = d.getElementById('count').textContent;
  const cjk = /[\u4e00-\u9fff]/.test(grid + count);
  check('N309 英文态空结果零 CJK', !cjk && grid.indexOf('No match') >= 0 && count.indexOf('only 48 common') >= 0, count.slice(0, 140) + ' | cjk=' + cjk);
}

// ══════════════ N311 文档口径：UTF-8 字节 ══════════════
{
  const { dom, html } = makeDom(dir('decimal-encode.html'), { alerts: [], en: false });
  const w = dom.window, d = w.document;
  const body = d.body.innerHTML;
  const badPoint = /Unicode 码点（或字节值）|“中”=20013|同一个码点|超过 127 的码点已不属于 ASCII/.test(body);
  check('N311 页面无「码点/中=20013」错误口径', !badPoint, badPoint ? 'still present' : 'clean');
  const goodByte = body.indexOf('UTF-8 字节') >= 0 && body.indexOf('228 184 173') >= 0;
  check('N311 页面明确 UTF-8 字节与中的字节示例', goodByte, goodByte ? 'byte口径OK' : 'missing byte example');
  d.getElementById('input').value = '中';
  d.getElementById('sep').value = ' ';
  w.enc();
  const out = d.getElementById('output').value;
  check('N311 enc(中) 输出 UTF-8 字节 228 184 173', out.trim() === '228 184 173', out);
  const dd = JSON.parse(fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8'))['it/decimal-encode'];
  const ddText = JSON.stringify(dd);
  check('N311 deepdive 权威源为字节口径', ddText.indexOf('228 184 173') >= 0 && ddText.indexOf('“中”=20013') < 0 && !/十进制码点表示字符|码点以十进制序列/.test(ddText), ddText.slice(0, 130));
  const enMap = fs.readFileSync('i18n/tools/en/it/decimal-encode.json', 'utf8');
  check('N311 英文 i18n 映射同步字节口径', enMap.indexOf('UTF-8 bytes') >= 0 && enMap.indexOf('228 184 173') >= 0 && !/decimal code points|one code point/.test(enMap), 'en map checked');
}

// ══════════════ N312 解码严格校验 ══════════════
{
  const state = { alerts: [], en: false };
  const { dom } = makeDom(dir('decimal-encode.html'), state);
  const w = dom.window, d = w.document;
  const input = d.getElementById('input'), output = d.getElementById('output');
  function decode(v) {
    state.alerts.length = 0;
    input.value = v;
    output.value = 'SENTINEL-KEEP';
    w.dec();
    return { alerts: state.alerts.slice(), out: output.value };
  }
  const r1 = decode('65x 66');
  check('N312 解码 65x 被拒绝（不静默按 65）', r1.alerts.some(a => a.indexOf('非法十进制数') >= 0) && r1.out === 'SENTINEL-KEEP', JSON.stringify(r1));
  const r2 = decode('0x41 0x42');
  check('N312 解码 0x41 被拒绝（不静默变 0）', r2.alerts.some(a => a.indexOf('非法十进制数') >= 0) && r2.out === 'SENTINEL-KEEP', JSON.stringify(r2));
  const r3 = decode('256 1');
  check('N312 解码 256 越界被拒绝', r3.alerts.some(a => a.indexOf('非法十进制数') >= 0) && r3.out === 'SENTINEL-KEEP', JSON.stringify(r3));
  const r4 = decode('72 101 108 108 111');
  check('N312 合法十进制正常解码 Hello', r4.out === 'Hello' && r4.alerts.length === 0, JSON.stringify(r4));
  const r5 = decode('065122');
  check('N312 无分隔符定长3位仍可解码 Az', r5.out === 'Az' && r5.alerts.length === 0, JSON.stringify(r5));
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
