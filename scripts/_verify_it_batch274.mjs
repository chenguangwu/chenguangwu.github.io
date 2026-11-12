// 第274批 JSDOM 验证：IT-N320 XML 混合内容 / IT-N321 子网规模上限
// 用法: node scripts/_verify_it_batch274.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = (rel) => OLD ? `${OLD}/tools/it/${rel}` : `tools/it/${rel}`;
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function stubs(w) {
  w.ToolBox = {
    showToast() {}, copyText() {}, exportCsv() {},
    createTable(heads, rows) { return '<table>' + rows.length + ' rows</table>'; },
  };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {} }, matrix: { table() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {} },
    preset: { bar() {} },
  };
  w.i18nText = () => '';
}

// ---------- IT-N320：xml-to-json ----------
{
  const dom = new JSDOM(fs.readFileSync(page('xml-to-json.html'), 'utf8'), {
    runScripts: 'dangerously', url: 'https://x.com/xml-to-json.html',
    beforeParse: stubs,
  });
  const w = dom.window, d = w.document;
  d.getElementById('attrs').checked = false;
  d.getElementById('input').value = '<p>Hello <b>world</b>!</p>';
  w.doBeautify();
  const out = d.getElementById('output').textContent || '';
  check('N320 混合内容保留直接文本 #text', out.indexOf('"#text": "Hello !"') >= 0 && out.indexOf('"b": "world"') >= 0, 'out=' + out.replace(/\s+/g, ' ').slice(0, 120));
  d.getElementById('input').value = '<r><a>one</a><b>two</b></r>';
  w.doBeautify();
  const leaf = d.getElementById('output').textContent || '';
  check('N320 纯子元素结构不误加 #text（回归锚）', leaf.indexOf('"a": "one"') >= 0 && leaf.indexOf('"b": "two"') >= 0 && leaf.indexOf('#text') < 0, 'out=' + leaf.replace(/\s+/g, ' ').slice(0, 100));
  d.getElementById('attrs').checked = true;
  d.getElementById('input').value = '<book id="b1">text</book>';
  w.doBeautify();
  const attr = d.getElementById('output').textContent || '';
  check('N320 属性 + 文本叶节点仍合并（回归锚）', attr.indexOf('"@id": "b1"') >= 0 && attr.indexOf('"#text": "text"') >= 0, 'out=' + attr.replace(/\s+/g, ' ').slice(0, 100));
}

// ---------- IT-N321：calc-subnet ----------
{
  const dom = new JSDOM(fs.readFileSync(page('calc-subnet.html'), 'utf8'), {
    runScripts: 'dangerously', url: 'https://x.com/calc-subnet.html',
    beforeParse: stubs,
  });
  const w = dom.window, d = w.document;
  const html = fs.readFileSync(page('calc-subnet.html'), 'utf8');
  check('N321 input[max] 设为 4096', /id="subN"[^>]*max="4096"/.test(html));
  d.getElementById('ip').value = '10.0.0.0';
  d.getElementById('cidr').value = '8';
  d.getElementById('subN').value = '4097'; // 超限但仍只会在旧态渲染 8192 行，避免测试把旧页跑死
  const t0 = Date.now();
  w.divideSubnets();
  const elapsed = Date.now() - t0;
  const msg = d.getElementById('subRes').innerHTML || '';
  check('N321 超 4096 规模直接拒绝（不渲染巨表）', msg.indexOf('超出展示上限') >= 0 && msg.indexOf('8192 rows') < 0, 'msg=' + msg.replace(/<[^>]*>/g, '').slice(0, 60) + ' ms=' + elapsed);
  check('N321 拒绝路径耗时极短', elapsed < 200, 'ms=' + elapsed);
  d.getElementById('subN').value = '4';
  w.divideSubnets();
  const normal = d.getElementById('subRes').innerHTML || '';
  check('N321 合法 N=4 仍正常渲染（回归锚）', normal.indexOf('rows') >= 0 && normal.indexOf('超出展示上限') < 0, 'head=' + normal.slice(0, 60));
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
