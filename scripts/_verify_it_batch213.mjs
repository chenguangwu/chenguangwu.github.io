// 第213批 · IT-N1 toml-formatter 严格校验/重复键/多行字符串（JSDOM 真机 · 已修项补证据）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/toml-formatter.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/toml-formatter.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

// ── 统一严格解析器：裸值 / 重复键必须拒绝 ──
function parseThrows(src) { try { w.eval('parseToml')(src); return false; } catch (e) { return true; } }
check('IT-N1 裸值 a = nope 被拒绝', parseThrows('a = nope'));
check('IT-N1 重复键被拒绝', parseThrows('a = 1\na = 2'));
check('IT-N1 合法文档仍可解析', !parseThrows('title = "ok"\n[srv]\nport = 8080'));

// ── validateTomlStrict 与 parseToml 同源 ──
const strictBad = w.eval('validateTomlStrict')('a = nope');
check('IT-N1 验证入口对裸值返回 err', !!strictBad.err, JSON.stringify(strictBad));
const strictDup = w.eval('validateTomlStrict')('a = 1\na = 2');
check('IT-N1 验证入口对重复键返回 err', !!strictDup.err, JSON.stringify(strictDup));
const strictOk = w.eval('validateTomlStrict')('a = 1');
check('IT-N1 验证入口合法文档 err=null 且有统计', !strictOk.err && strictOk.kv === 1, JSON.stringify(strictOk));

// ── 多行字符串完整保留 ──
const ml = w.eval('parseToml')('desc = """hello\nworld\n"""');
check('IT-N1 多行字符串不截断', ml.desc.indexOf('hello') >= 0 && ml.desc.indexOf('world') >= 0, JSON.stringify(ml.desc));
check('IT-N1 多行字符串保留行间换行', /\n/.test(ml.desc), JSON.stringify(ml.desc));

// ── 三条 UI 入口一致拒绝 / 一致成功 ──
const input = d.getElementById('input');
const output = d.getElementById('output');
const errMsg = d.getElementById('error-msg');

input.value = 'a = nope';
w.eval('validateToml()');
check('IT-N1 验证按钮显示错误', errMsg.style.display === 'block' && /❌/.test(errMsg.textContent), errMsg.textContent);
check('IT-N1 验证失败不输出通过提示', !/验证通过/.test(output.textContent), output.textContent.slice(0, 100));

input.value = 'a = 1\na = 2';
w.eval('formatToml()');
check('IT-N1 格式化重复键不静默保留末值', errMsg.style.display === 'block' && !/^a = 2/.test(output.textContent.trim()), 'out=' + JSON.stringify(output.textContent.trim()));

input.value = 'a = 1';
w.eval('formatToml()');
check('IT-N1 合法输入格式化正常', /a = 1/.test(output.textContent), output.textContent.slice(0, 100));

const tomlInput = d.getElementById('toml-input');
const jsonOutput = d.getElementById('json-output');
tomlInput.value = 'desc = """hello\nworld\n"""';
w.eval('tomlToJson()');
check('IT-N1 TOML→JSON 多行字符串不丢内容', /hello/.test(jsonOutput.textContent) && /world/.test(jsonOutput.textContent), jsonOutput.textContent.slice(0, 160));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
