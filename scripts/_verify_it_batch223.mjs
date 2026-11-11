// 第223批 · IT-N196~N198 html-entities-encode（JSDOM 真机）
//  N196 码点范围未校验（进批探测：已由其他 Agent 修好，补证据）
//  N197 用 div.innerHTML 解码触发外部资源请求（进批探测：已修为纯文本替换，补证据）
//  N198 有/无分号两条解码路径不一致（真修：单次纯文本扫描统一出口）
//  顺带修：dec() 是另一个产结果入口却未被历史/明细表包装
// 用法：node scripts/_verify_it_batch223.mjs [可选：另一个页面路径，用于旧源码差分]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.argv[2] || 'tools/it/html-entities-encode.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) {
  checks.push([n, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 180) : ''));
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

let tableData = null, exportCalls = [], history = [], alerts = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/html-entities-encode.html',
  beforeParse(w) {
    w.alert = (m) => { alerts.push(String(m)); };
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
    w.navigator.clipboard = { writeText: () => Promise.resolve() };
    w.TBKit = {
      util: { isEn: () => false, exportTable(sel, name) { exportCalls.push({ sel, name, rows: tableData && tableData.rows }); }, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: {
        table(sel, cfg) {
          tableData = cfg;
          const el = w.document.querySelector(sel);
          if (el) el.innerHTML = '<tr><th>' + cfg.head.map(esc).join('</th><th>') + '</th></tr>' +
            cfg.rows.map(r => '<tr><td>' + r.map(esc).join('</td><td>') + '</td></tr>').join('');
        }
      },
      preset: { bar() {} },
      history: {
        list() { return history.slice(); },
        last() { return history.length ? history[0].d : null; },
        record(r) { history.unshift({ t: Date.now(), d: r }); },
        mount() {}, clear() { history = []; }
      }
    };
  }
});
const w = dom.window, d = w.document;
const $ = id => d.getElementById(id);

function dec(text) {
  $('input').value = text;
  let err = null;
  try { w.dec(); } catch (e) { err = e.message; }
  return { out: String($('output').value ?? ''), err };
}
function enc(text) {
  $('input').value = text;
  w.enc();
  return String($('output').value ?? '');
}

// ══════════════ N196 码点范围（已修补证据） ══════════════
const oob = dec('a&#1114112;b');
check('N196 &#1114112; 越界码点原样保留且不抛异常', oob.err === null && oob.out === 'a&#1114112;b', JSON.stringify(oob.out));
check('N196 &#x110000; 十六进制越界同样原样保留', dec('&#x110000;').out === '&#x110000;', '');
check('N196 代理区 &#xD800; 原样保留', dec('&#xD800;').out === '&#xD800;', '');
check('N196 代理区十进制 &#55296; 原样保留', dec('&#55296;').out === '&#55296;', '');
check('N196 合法码点 &#x1F600; 正常解为 emoji', dec('&#x1F600;').out === '\u{1F600}', JSON.stringify(dec('&#x1F600;').out));
check('N196 &#0; 合法零码点不抛错', dec('&#0;').err === null && dec('&#0;').out.charCodeAt(0) === 0, '');

// ══════════════ N197 纯文本零 DOM（已修补证据） ══════════════
const decStart = html.indexOf('function dec()');
const decEnd = html.indexOf('\nfunction copyResult', decStart);
const decSrc = decStart >= 0 ? html.slice(decStart, decEnd > decStart ? decEnd : undefined) : '';
// 注释里会提到这些 API 名做说明，故只判「实际赋值/调用语句」
check('N197 dec() 源码零 DOM API 调用（无 innerHTML 赋值 / DOMParser / createElement）',
  !!decSrc && !/\.innerHTML\s*=|new\s+DOMParser|document\.createElement\s*\(/.test(decSrc),
  decSrc.slice(0, 80));
check('N197 粘贴 img 标签解码后原样保留（不建 DOM，不会被吃掉）',
  dec('<img src="https://x.example/track.png">').out === '<img src="https://x.example/track.png">', '');
check('N197 粘贴 script 标签解码后原样保留',
  dec('<script>alert(1)</script>').out === '<script>alert(1)</script>', '');
check('N197 标签与实体混合时只解实体、标签不动',
  dec('<b>&amp;</b>').out === '<b>&</b>', JSON.stringify(dec('<b>&amp;</b>').out));

// ══════════════ N198 统一解码路径（真修） ══════════════
check('N198 混合写法 &#65; &amp 解为 A &（不再因上下文不同）', dec('&#65; &amp').out === 'A &', JSON.stringify(dec('&#65; &amp').out));
check('N198 仅有 &amp 也解为 &', dec('&amp').out === '&', JSON.stringify(dec('&amp').out));
check('N198 仅有 &#65 解为 A（数字实体无分号）', dec('&#65').out === 'A', JSON.stringify(dec('&#65').out));
check('N198 仅有 &#x41 解为 A（十六进制无分号）', dec('&#x41').out === 'A', JSON.stringify(dec('&#x41').out));
check('N198 三种形态混排无分号一次解完', dec('&lt &#65 &#x42 &gt').out === '< A B >', JSON.stringify(dec('&lt &#65 &#x42 &gt').out));
const legacyOut = dec('&nbsp &copy &reg').out; // 输入里三个实体之间有空格，输出也保留这些空格
check('N198 legacy 子集 &nbsp / &copy / &reg 无分号可解',
  legacyOut.includes('\u00A0') && legacyOut.includes('\u00A9') && legacyOut.includes('\u00AE') &&
  !legacyOut.includes('&nbsp') && !legacyOut.includes('&copy') && !legacyOut.includes('&reg'),
  JSON.stringify(legacyOut));
check('N198 非 legacy 命名实体无分号保留（&rarr）', dec('&rarr').out === '&rarr', '');
check('N198 AT&T 不被误改', dec('AT&T').out === 'AT&T', JSON.stringify(dec('AT&T').out));
check('N198 未知实体 &notin 不被误改', dec('&notin').out === '&notin', '');
check('N198 表外实体 &alpha; 原样保留（表只有 39 条，不虚报完整）', dec('&alpha;').out === '&alpha;', '');
check('N198 单次扫描不二次解码：&amp;lt; → &lt;', dec('&amp;lt;').out === '&lt;', JSON.stringify(dec('&amp;lt;').out));
check('N198 单次扫描不二次解码：&amp;amp → &amp', dec('&amp;amp').out === '&amp', JSON.stringify(dec('&amp;amp').out));
check('N198 带分号命名实体仍正常解', dec('&lt;&gt;&quot;&amp;').out === '<>"&', '');
check('N198 结果与实体出现顺序无关', dec('&amp &#65;').out === '& A' && dec('&#65; &amp').out === 'A &', '');

// ══════════════ 全链路 / 状态链 ══════════════
history = []; tableData = null; exportCalls = [];
w.eval('__html_entities_encode_last=0');
const chainDec = dec('&#84;&amp;&#111;&#108;&#66;&#111;&#120;');
check('链路 解码产出真实结果 T&olBox', chainDec.out === 'T&olBox', chainDec.out);
check('链路 解码入口写历史（修前只包装 enc ⇒ 0 条）', history.length >= 1 &&
  String((history[0].d || {})['结果'] ?? '').includes('T&olBox'), 'hist=' + history.length);
check('链路 明细表含「结果」列与解码结果', !!tableData && tableData.head.includes('结果') &&
  tableData.rows.some(r => r.some(c => String(c).includes('T&olBox'))), tableData ? tableData.head.join('/') : 'no table');
w.__html_entities_encodeExport();
check('链路 导出携带解码结果行', exportCalls.length >= 1 &&
  (exportCalls[0].rows || []).some(r => r.some(c => String(c).includes('T&olBox'))), 'exports=' + exportCalls.length);
let seqErr = null;
try { enc('a<b'); dec('&lt;'); enc('c&d'); } catch (e) { seqErr = e.message; }
check('状态链 enc/dec 快速连续切换无异常且末次生效', seqErr === null && $('output').value === 'c&amp;d', seqErr || '');
alerts = [];
let emptyErr = null;
try { dec(''); } catch (e) { emptyErr = e.message; }
check('状态链 空输入弹提示且不抛错', emptyErr === null && alerts.length === 1, emptyErr || 'alerts=' + alerts.length);
check('状态链 非法→恢复后可正常解码', dec('').err === null && dec('&#65;').out === 'A', '');
check('模板 ResText 对 textarea 读 value（IT-N140 已修补证据）',
  typeof w.__html_entities_encodeResText === 'function' && /isField\s*=\s*r\.tagName/.test(html), '');

// ══════════════ 公式 / i18n 三源 / EN 态 ══════════════
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/html-entities-encode.json', 'utf8'));
const f = html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
check('公式 页面说明已补解码规则（单次扫描 / 码点范围 / 零 DOM）', !!f &&
  /单次纯文本扫描/.test(f[1]) && /0xD800–0xDFFF/.test(f[1]) && /amp\/lt\/gt\/quot\/nbsp\/copy\/reg/.test(f[1]),
  f ? f[1].slice(-70) : 'missing');
check('公式 en JSON 含同文中文键与英译', !!f && !!en.map[f[1]] &&
  /single plain-text scan/.test(en.map[f[1]]) && /external resource requests/.test(en.map[f[1]]),
  f ? String(en.map[f[1]] || '').slice(-70) : 'no formula');

const domEn = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/html-entities-encode.html?lang=en-US',
  beforeParse(we) {
    we.alert = (m) => { alerts.push('EN:' + String(m)); };
    we.ToolBox = { showToast() {}, copyText() {} };
    we.TBKit = { util: { isEn: () => true, exportTable() {}, diffBox() {} }, chart: { line() {}, bar() {} },
      matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, last() { return null; }, record() {}, mount() {} } };
  }
});
const we = domEn.window, de = we.document;
de.getElementById('input').value = '';
alerts = [];
we.dec();
check('EN 态空输入 alert 为英文（动态串零 CJK）',
  alerts.length === 1 && /Enter HTML entity to decode/.test(alerts[0]) && !/[一-鿿]/.test(alerts[0]), alerts.join('|'));

// ══════════════ 汇总 ══════════════
const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exit(1);
}
