// 第243批探测 · IT-N32/N38/N39（xml-formatter / stats-1 / text-statistics）
//  N32 XML 格式化/压缩须保留根元素、CDATA、注释与文本内换行
//  N38 字数统计按字素簇 + 扩展汉字 + 连字符词 + 裸 CR 行切分
//  N39 文本统计句子切分保护小数/缩写、行数识别裸 CR
// 用法：node scripts/_verify_it_batch243.mjs [旧页目录]
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
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
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
// 三页分属不同目录；旧备份 /tmp/bk243 把三页平铺在同一目录，故旧态用 basename。
const PATHS = {
  'xml-formatter.html': 'tools/it/xml-formatter.html',
  'stats-1.html': 'tools/text/stats-1.html',
  'text-statistics.html': 'tools/it/text-statistics.html'
};
const p = (name) => OLD_DIR ? OLD_DIR + '/' + name : PATHS[name];

// ══════════════ N32 XML 根元素 / CDATA / 注释 / 压缩换行 ══════════════
{
  const dom = makeDom(p('xml-formatter.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('input'), out = d.getElementById('output');
  // 格式化：根元素 + CDATA 存活
  input.value = '<root><!-- c --><a>1</a><raw><![CDATA[<x>2</x>]]></raw></root>';
  w.doBeautify();
  let s = out.textContent;
  check('N32 格式化保留根元素 root', /<root>/.test(s) && /<\/root>/.test(s), s.slice(0, 160).replace(/\n/g, '\\n'));
  check('N32 格式化保留 CDATA 原文', s.indexOf('<![CDATA[<x>2</x>]]>') >= 0 && s.indexOf('<raw/>') < 0, s.slice(0, 160).replace(/\n/g, '\\n'));
  check('N32 格式化保留根外注释', s.indexOf('<!-- c -->') >= 0, s.slice(0, 100).replace(/\n/g, '\\n'));
  // 压缩：文本节点内换行须保留
  input.value = '<a>line1\nline2</a>';
  w.doMinify();
  s = out.textContent;
  check('N32 压缩保留文本内换行且保留根元素', s.indexOf('<a>line1\nline2</a>') >= 0, s.replace(/\n/g, '\\n'));
  // 多根非法 XML 报错
  input.value = '<a/><b/>';
  w.doValidate();
  check('N32 多根非法 XML 明确报错', /解析错误|❌/.test(d.getElementById('err').textContent), d.getElementById('err').textContent.slice(0, 80));
}

// ══════════════ N38 stats-1 计数口径 ══════════════
{
  const dom = makeDom(p('stats-1.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('text'), res = d.getElementById('res');
  function val(label) {
    const m = res.textContent.match(new RegExp(label + '[^0-9]*([0-9,]+)'));
    return m ? m[1].replace(/,/g, '') : null;
  }
  // emoji 字素簇：😀 记 1（旧 UTF-16 记 2）
  input.value = '😀';
  w.calc();
  check('N38 emoji 按字素簇计 1（非 UTF-16 的 2）', val('总字符数（含空白）') === '1', res.textContent.replace(/\s+/g, ' ').slice(0, 120));
  // 扩展汉字 𠮷（U+20BB7）计入中文
  input.value = '𠮷';
  w.calc();
  check('N38 扩展 B 汉字计入中文（非 0）', val('中文字符数') === '1', res.textContent.replace(/\s+/g, ' ').slice(0, 120));
  // 连字符词：well-known 记 1 词
  input.value = 'well-known';
  w.calc();
  check('N38 连字符词 well-known 计 1 词', val('英文单词数') === '1', res.textContent.replace(/\s+/g, ' ').slice(0, 120));
  // 裸 CR 切行：a\rb → 2 行（textarea 会规范化 \r 为 \n，须覆盖 value getter 注入真裸 CR）
  Object.defineProperty(input, 'value', { get: () => 'a\rb', configurable: true });
  w.calc();
  check('N38 裸 CR 切分为 2 行', val('行数') === '2', res.textContent.replace(/\s+/g, ' ').slice(0, 120));
  delete input.value;
  // 口径说明同步（字素簇、扩展A/B、CRLF/CR/LF）
  check('N38 口径说明改为字素簇与扩展 A/B', /字素簇/.test(d.body.textContent) && /扩展 A\/B/.test(d.body.textContent), 'body checked');
}

// ══════════════ N39 text-statistics 句子 / 行 ══════════════
{
  const dom = makeDom(p('text-statistics.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('textInput');
  function stat(label) {
    const t = d.getElementById('result').textContent.replace(/\s+/g, ' ');
    const m = t.match(new RegExp('([0-9]+)\\s*' + label));
    return m ? m[1] : null;
  }
  // 小数不切句：Version 3.14 is out → 1 句
  input.value = 'Version 3.14 is out';
  w.analyze();
  check('N39 小数 3.14 不当句末（1 句）', stat('句子') === '1', d.getElementById('result').textContent.replace(/\s+/g, ' ').slice(0, 200));
  // 缩写不切句：Dr. Smith left. → 1 句
  input.value = 'Dr. Smith left.';
  w.analyze();
  check('N39 缩写 Dr. 不当句末（1 句）', stat('句子') === '1', d.getElementById('result').textContent.replace(/\s+/g, ' ').slice(0, 200));
  // 裸 CR 切行：a\rb → 2 行（覆盖 value getter 注入真裸 CR）
  Object.defineProperty(input, 'value', { get: () => 'a\rb', configurable: true });
  w.analyze();
  check('N39 裸 CR 切分为 2 行', stat('行数') === '2', d.getElementById('result').textContent.replace(/\s+/g, ' ').slice(0, 200));
  delete input.value;
  // 中文句号仍切句：你好。世界 → 2 句
  input.value = '你好。世界';
  w.analyze();
  check('N39 中文句号仍正常切句（2 句）', stat('句子') === '2', d.getElementById('result').textContent.replace(/\s+/g, ' ').slice(0, 200));
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
