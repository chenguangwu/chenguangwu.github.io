// 第277批 JSDOM 验证：IT-N326 YAML 块标量 / IT-N327 行内注释
// 用法: node scripts/_verify_it_batch277.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const file = OLD ? `${OLD}/tools/it/yaml-to-json.html` : 'tools/it/yaml-to-json.html';
const html = fs.readFileSync(file, 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/yaml-to-json.html',
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

function parse(src) {
  d.getElementById('source').value = src;
  w.calcTool();
  const pre = d.querySelector('#result .code-block');
  const text = pre ? pre.textContent : '';
  try { return JSON.parse(text); } catch (e) { return { __parseError: String(e), __raw: text }; }
}

// ---------- N326：块标量 ----------
let o = parse('desc: |\n  hello\n  world\nname: test\n');
check('N326 | 块标量保留两行且后续同级键不丢', o.desc === 'hello\nworld\n' && o.name === 'test', JSON.stringify(o));

o = parse('desc: |-\n  hello\n  world\nname: test\n');
check('N326 |- 去掉末尾换行且后续键不丢', o.desc === 'hello\nworld' && o.name === 'test', JSON.stringify(o));

o = parse('desc: >\n  hello\n  world\nname: test\n');
check('N326 > 折叠为空格且带一个末尾换行', o.desc === 'hello world\n' && o.name === 'test', JSON.stringify(o));

o = parse('desc: >-\n  hello\n  world\nname: test\n');
check('N326 >- 折叠且无末尾换行', o.desc === 'hello world' && o.name === 'test', JSON.stringify(o));

o = parse('a: 1\ndesc: |\n  x\n  y\nz: 2\n');
check('N326 块标量前后键顺序保持', o.a === 1 && o.desc === 'x\ny\n' && o.z === 2, JSON.stringify(o));

// ---------- N327：行内注释 ----------
o = parse('port: 8080 # web port\nenabled: true # flag\nratio: 1.5 # r\nempty: null # e\nnote: hello # comment\n');
check('N327 行尾注释剥离后各类型恢复原值', o.port === 8080 && o.enabled === true && o.ratio === 1.5 && o.empty === null && o.note === 'hello', JSON.stringify(o));

o = parse('title: "a # b" # trailing\nurl: http://x.com/a#frag\nhash: "#tag" # tail\n');
check('N327 引号内 # 与无空格 # 不被误剥离', o.title === 'a # b' && o.url === 'http://x.com/a#frag' && o.hash === '#tag', JSON.stringify(o));

o = parse('n: 5#notcomment\nm: 6 # real\n');
check('N327 紧贴值的 # 保留，带空格的 # 剥离', o.n === '5#notcomment' && o.m === 6, JSON.stringify(o));

// ---------- 回归：默认示例 ----------
o = parse('name: ToolBox\nversion: 2.1\nactive: true\nitems:\n  - id: 1\n    name: alpha\n  - id: 2\n    name: beta');
check('回归：列表内 map 与浮点解析不退化', o.name === 'ToolBox' && o.version === 2.1 && o.items.length === 2 && o.items[1].name === 'beta', JSON.stringify(o));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
