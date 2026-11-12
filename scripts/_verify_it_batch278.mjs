// 第278批 JSDOM 验证：IT-N328 JSON 空串 → YAML null / IT-N329 压缩拍平缩进
// 用法: node scripts/_verify_it_batch278.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const file = OLD ? `${OLD}/tools/it/json-to-yaml.html` : 'tools/it/json-to-yaml.html';
const html = fs.readFileSync(file, 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/json-to-yaml.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, toast() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
      preset: { bar() {} },
    };
    w.i18nText = () => '';
    w.alert = () => {};
  },
});
const w = dom.window, d = w.document;
const input = d.getElementById('input'), output = d.getElementById('output');

function run(json, fn) {
  input.value = json;
  w[fn]();
  return output.textContent || '';
}

// ---------- N328：空字符串与 null 可区分 ----------
let out = run('{"k":"","port":null}', 'doYaml');
check('N328 空字符串输出双引号 k: ""', /^k: ""$/m.test(out), JSON.stringify(out));
check('N328 null 仍输出裸 null', /^port: null$/m.test(out), JSON.stringify(out));

out = run('{"a":"","b":"x"}', 'doYaml');
check('N328 空串不影响普通字符串', /^a: ""$/m.test(out) && /^b: x$/m.test(out), JSON.stringify(out));

// ---------- N329：压缩只删空行、保留缩进 ----------
out = run('{"a":{"b":1}}', 'doMinYaml');
check('N329 压缩保留嵌套两空格缩进', out === '---\na:\n  b: 1', JSON.stringify(out));

out = run('{"list":[{"x":1},{"y":2}]}', 'doMinYaml');
check('N329 压缩保留列表项缩进', /^  -$/m.test(out) && /^    x: 1$/m.test(out) && /^    "y": 2$/m.test(out), JSON.stringify(out));

out = run('{"a":{"b":1}}', 'doYaml');
check('N329 正常转换仍有缩进（回归）', /^---\na: *\n  b: 1$/.test(out), JSON.stringify(out));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
