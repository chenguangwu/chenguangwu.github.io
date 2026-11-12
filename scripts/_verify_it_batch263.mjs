// 第263批 JSDOM 验证：IT-N159/N160 Playfair 原理区数字与 deep-dive 算例 + Q 填充文档化
// 用法: node scripts/_verify_it_batch263.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const f = (rel) => OLD ? `${OLD}/${rel}` : rel;
const html = fs.readFileSync(f('tools/it/playfair-cipher.html'), 'utf8');
const enMap = JSON.parse(fs.readFileSync(f('i18n/tools/en/it/playfair-cipher.json'), 'utf8')).map;
const dd = JSON.parse(fs.readFileSync(f('i18n/tools/content_deepdive.json'), 'utf8'))['it/playfair-cipher'];

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const toasts = [];
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/playfair.html',
  beforeParse(w) {
    w.alert = m => toasts.push(String(m));
    w.ToolBox = { showToast: m => toasts.push(String(m)), copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
    };
    w.i18nText = (zh, en) => enMode ? (en || zh) : zh;
  },
});
const w = dom.window, d = w.document;
const bodyText = () => d.body.textContent || '';

// ---------- IT-N159：25×25=625，不得再写 26×26=676 ----------
{
  const t = bodyText();
  check('N159 原理区不再出现 676', !/26×26=676/.test(t), 'found=' + (t.match(/26×26=676/g) || []).length);
  check('N159 原理区给出 625', /25×25=625/.test(t));
  check('N159 给出 6×6 变体 1296', /36×36=1296/.test(t));
  check('N159 说明 I/J 合并后为 25 字母', /I\/J 合并后只有 25 个字母/.test(t));
}
// ---------- IT-N160：deep-dive 算例可复现 ----------
{
  const title = d.querySelector('.dd-ex-title') ? d.querySelector('.dd-ex-title').textContent : '';
  const body = d.querySelector('.dd-ex-body') ? d.querySelector('.dd-ex-body').textContent : '';
  check('N160 示例标注默认密钥 PLAYFAIR', /PLAYFAIR/.test(title), 'title=' + title);
  check('N160 示例给出完整 5×5 方阵', /PLAYF \/ IRBCD \/ EGHKM \/ NOQST \/ UVWXZ/.test(body), 'body=' + body.slice(0, 160));
  check('N160 示例结果为 EB', /`EB`/.test(body));
  check('N160 旧错串 BM 已清除', !/`BM`/.test(body));
  check('N160 权威源 title 同步', /PLAYFAIR/.test(dd.examples[0].title), 'dd.title=' + dd.examples[0].title);
  check('N160 权威源 body 含 EB 不含 BM', /`EB`/.test(dd.examples[0].body) && !/`BM`/.test(dd.examples[0].body));
  // 用页面自身函数实算交叉验证（不依赖文档写死的值）
  try { w.setMode('encrypt'); } catch (_) { /* old source setMode 可能用残留输入自跑 */ }
  d.getElementById('key').value = 'PLAYFAIR';
  d.getElementById('input').value = 'HI';
  d.getElementById('output').value = '';
  let err = null;
  try { w.process(); } catch (e) { err = String(e && e.message || e); }
  const out = d.getElementById('output').value;
  check('N160 页面实算 HI+PLAYFAIR 得 EB', err === null && out === 'EB', 'out=' + out + ' err=' + err);
  check('N160 文档结果与页面实算一致', /`EB`/.test(body) && out === 'EB', 'out=' + out);
}
// ---------- Q 备用填充字母文档化（第261批留存建议） ----------
{
  const t = bodyText();
  const li = Array.from(d.querySelectorAll('.formula-list li')).map(x => x.textContent).join(' | ');
  check('Q 原理区说明 X 本身改用 Q', /该字母本身为 X 时改用 Q/.test(li), 'li=' + li.slice(0, 180));
  check('Q FAQ0 给出 XX → XQ XQ', /`XQ XQ`/.test(t));
  check('Q FAQ1 说明字母本身为 X 时改用 Q', /字母本身为 X 时改用 Q/.test(t));
  check('Q 权威源 FAQ0 同步', /`XQ XQ`/.test(dd.faqs[0].a), 'faq0=' + dd.faqs[0].a.slice(0, 120));
  check('Q 权威源 FAQ1 同步', /字母本身为 X 时改用 Q/.test(dd.faqs[1].a));
}
// ---------- 英文 map 键/译文同步（防止 EN 态残留 CJK） ----------
{
  const zhKeys = [
    '：明文两两分组，同一组内字母相同则插入 X（该字母本身为 X 时改用 Q，避免生成 XX 同字母对），末尾为奇数补 X。',
    '普莱费尔密码是第一个广泛使用的双字母替换密码。与单字母替换密码相比，它的安全性大大提高，因为频率分析针对的是单个字母，而本页 5×5 方阵把 I/J 合并后只有 25 个字母，对应 25×25=625 种可能的字母对，使得频率分析变得困难得多；若采用 6×6 含数字的变体，则为 36×36=1296 种。',
    '加密 "HI"（默认密钥 PLAYFAIR）',
    '默认密钥 PLAYFAIR 构造的 5×5 方阵（I/J 合并）为 PLAYF / IRBCD / EGHKM / NOQST / UVWXZ。H 在第 3 行第 3 列、I 在第 2 行第 1 列，不同行不同列时取矩形另两角 E 与 B ⇒ `EB`，与工具实算一致。',
    '插入填充字母（如 X）隔开，如 `LL` → `LX L`；重复字母本身是 X 时改用 Q（`XX` → `XQ XQ`），否则会生成规则不允许的 XX 同字母对。',
    '因为 Playfair 以两个字母为一组处理：明文先去掉非字母字符、把 J 合并到 I，若同一组内两字母相同则在中间插入填充字母（通常为 X，字母本身为 X 时改用 Q），末组不足时也补一个，因此密文长度恒为偶数。解密后需自行去掉这些填充并恢复断词。',
  ];
  zhKeys.forEach((k, i) => check(`英文 map 新键存在 #${i + 1}`, Object.prototype.hasOwnProperty.call(enMap, k)));
  const vals = zhKeys.map(k => enMap[k] || '');
  check('英文 map 六个译文均无 CJK', vals.every(v => v && !/[\u4e00-\u9fff]/.test(v)), JSON.stringify(vals.map(v => v.slice(0, 60))));
  check('英文译文含 625 与 EB', vals.some(v => /625/.test(v)) && vals.some(v => /`EB`/.test(v)));
}
// ---------- 历史修复回归（本批不得回退第261批功能） ----------
{
  const pairs = w.prepareText('XX');
  check('回归 XX 仍用 Q 填充', JSON.stringify(pairs) === '[["X","Q"],["X","Q"]]', JSON.stringify(pairs));
  try { w.setMode('encrypt'); } catch (_) { /* ignore */ }
  d.getElementById('key').value = 'KEY';
  d.getElementById('input').value = 'HELLO';
  w.process();
  check('回归 HELLO+KEY 仍为 DBNVMI', d.getElementById('output').value === 'DBNVMI', 'out=' + d.getElementById('output').value);
  try { w.setMode('decrypt'); } catch (_) { /* ignore */ }
  d.getElementById('input').value = 'Z';
  d.getElementById('output').value = '';
  let err = null;
  try { w.process(); } catch (e) { err = String(e && e.message || e); }
  check('回归 奇数密文仍给偶数提示', err === null && /偶数个字母/.test(d.getElementById('pairList').innerHTML), 'err=' + err);
  enMode = true;
  d.getElementById('input').value = 'Z';
  try { w.process(); } catch (_) { /* ignore */ }
  check('回归 英文态提示仍为英文', /even number of letters/.test(d.getElementById('pairList').innerHTML));
  enMode = false;
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
