// 第209批 · IT-N264/N265/N266 xml-to-yaml 首屏/嵌套对象/属性与键 + indent 回归（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/xml-to-yaml.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/xml-to-yaml.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const src = d.getElementById('source');
const result = d.getElementById('result');
const indent = d.getElementById('indent');

function run(xml, ind) {
  src.value = xml;
  indent.value = ind || '2';
  w.eval('calcTool()');
  return result.textContent;
}

// ── N264 首屏证据（其他 Agent 已在 HEAD 修好，本批只补证据）──
w.eval('resetForm()');
const init = src.value;
check('N264 textarea 初值无深潜 CSS', !/\.deep-dive\{/.test(init), 'len=' + init.length);
check('N264 textarea 初值只有示例的一个 </body>', (init.match(/<\/body>/g) || []).length === 1, 'count=' + (init.match(/<\/body>/g) || []).length);
check('N264 textarea 初值仅 note 示例', /^<note>[\s\S]*<\/note>$/.test(init) && init.split('\n').length <= 12, 'lines=' + init.split('\n').length);
const deep = d.querySelector('.deep-dive');
check('N264 深潜容器存在于 textarea 之外', !!deep && !deep.closest('textarea'));
check('N264 首屏输出无 CSS/深潜垃圾', !/style:/.test(result.textContent) && !/\.deep-dive/.test(result.textContent), result.textContent.slice(0, 120));

// ── N265 数组套对象证据（其他 Agent 已在 HEAD 修好，本批只补证据）──
const arr = run('<a><b><c><d>1</d></c></b><b><e>2</e></b></a>');
check('N265 数组套对象无 [object Object]', arr.indexOf('[object Object]') < 0, arr.slice(0, 160));
check('N265 嵌套对象键递归输出', /d: "1"/.test(arr) && /- e:/.test(arr), arr.slice(0, 160));

// ── N266 属性解析：单引号 / 引号内 > ──
const sq = run("<a b='v'>x</a>");
check('N266 单引号属性被解析', /"@b"/.test(sq) && /\bv\b/.test(sq), sq.slice(0, 160));
check('N266 元素文本键保留', /"#text"/.test(sq) && /\bx\b/.test(sq), sq.slice(0, 160));
const gt = run('<a b="x>y"><c>1</c></a>');
check('N266 属性值内 > 不截断标签', /"@b": x>y/.test(gt), gt.slice(0, 180));
check('N266 不产生假 #text', !/y">&/.test(gt) && !/#text: y"/.test(gt), gt.slice(0, 180));
check('N266 子元素 c 仍被解析', /\bc:/.test(gt), gt.slice(0, 180));

// ── N266 YAML 键合法性 @ / # ──
const attr = run('<items id="1">foo<item>a</item></items>');
check('N266 @id 键加双引号', /"@id"/.test(attr), attr.slice(0, 180));
check('N266 #text 键加双引号', /"#text"/.test(attr), attr.slice(0, 180));
check('N266 普通键保持裸写', /\bitem:/.test(attr) && !/"item"/.test(attr), attr.slice(0, 180));

// ── indent 口径回归：承诺几空格就是几空格 ──
const note = '<note><to>Tony</to><items><item>Apple</item><item>Banana</item></items></note>';
const i2 = run(note, '2');
check('indent=2 首层 2 空格', /\n {2}to: Tony/.test(i2), JSON.stringify(i2.slice(0, 120)));
check('indent=2 首层不是 4 空格', !/\n {4}to: Tony/.test(i2), JSON.stringify(i2.slice(0, 120)));
const i4 = run(note, '4');
check('indent=4 首层 4 空格', /\n {4}to: Tony/.test(i4), JSON.stringify(i4.slice(0, 120)));
const it = run(note, 'tab');
check('indent=tab 首层 1 个 tab', /\n\tto: Tony/.test(it), JSON.stringify(it.slice(0, 120)));
check('indent=2 数组项 6 空格', /\n {6}- Apple/.test(i2), JSON.stringify(i2.slice(0, 160)));

// ── 双语口径：en JSON 中文键与页面逐字一致 ──
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/xml-to-yaml.json', 'utf8'));
const enMap = en.map || {};
check('en JSON 含更新后的属性说明键', Object.prototype.hasOwnProperty.call(enMap, 'XML 属性在 YAML 中以加引号的键表示（如 "@id"），元素文本用 "#text" 键；引号保证严格 YAML 解析器不会把 @ / # 当保留字符或注释。'));
check('页面含更新后的属性说明', html.indexOf('XML 属性在 YAML 中以加引号的键表示') >= 0);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
