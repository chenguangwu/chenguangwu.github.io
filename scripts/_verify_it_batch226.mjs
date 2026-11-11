// 第226批 · IT-N207~N211（char-encoder 1 条 + basic-auth-generator 4 条，JSDOM 真机）
//  N207 char-encoder HTML 命名仅 9 项、标签名不符（真修：补全常见实体+改名）
//  N208 basic-auth 用户名含冒号不校验（真修）
//  N209 basic-auth 非 ASCII 无 charset 提示（真修）
//  N210 basic-auth 历史快照写密码明文（进批探测：已修，补证据）
//  N211 basic-auth copyField i18nText() 空参显示 undefined（进批探测：已修，补证据）
// 用法：node scripts/_verify_it_batch226.mjs [旧页目录；提供时对两页做差分兼容]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 150) : '')); }

function makeDom(htmlPath, url) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  let history = [], toasts = [], copied = [];
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: url || 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast(t) { toasts.push(String(t)); }, copyText(v) { copied.push(String(v)); } };
      w.i18nText = (key, fb) => (key == null || key === '') ? (fb != null ? fb : '') : (fb || String(key));
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return history.slice(); }, last() { return history.length ? history[history.length - 1] : null; },
          record(r) { history.push(r); }, mount() {}, clear() { history = []; } }
      };
    }
  });
  return { dom, w: dom.window, d: dom.window.document, html, history, toasts, copied };
}

const CHAR = OLD_DIR ? OLD_DIR + '/char.orig.html' : 'tools/it/char-encoder.html';
const AUTH = OLD_DIR ? OLD_DIR + '/auth.orig.html' : 'tools/it/basic-auth-generator.html';

// ══════════════ N207 char-encoder 命名实体 ══════════════
const C = makeDom(CHAR);
const cw = C.w, cd = C.d, $$ = id => cd.getElementById(id);
function cconv(text) { $$('input').value = text; cw.convert(); return [...cd.querySelectorAll('.format-card')].map(c => [c.querySelector('.name').textContent, c.querySelector('.val').textContent]); }
let cards = cconv('\u00a0\u2026\u2014\u00a9');
const entCard = cards.find(x => /实体|named/.test(x[0]));
check('N207 标签改为「常用 HTML 实体 / Common HTML entities」', !!entCard && /常用 HTML 实体|Common HTML entities/.test(entCard[0]), entCard ? entCard[0] : 'missing');
check('N207 补全 &nbsp; &hellip; &mdash; &copy;', !!entCard && /&nbsp;&hellip;&mdash;&copy;/.test(entCard[1]), entCard ? entCard[1] : '');
check('N207 无命名实体的字符（中/é）原样保留', (() => { const e = cconv('中é').find(x => /实体|named/.test(x[0])); return !!e && e[1] === '中é'; })(), '');
check('N207 &quot; 与 &apos; 输出规范（双引号/单引号）', (() => { const e = cconv('"\'&').find(x => /实体|named/.test(x[0])); return !!e && e[1] === '&quot;&apos;&amp;'; })(), '');

// ══════════════ basic-auth-generator ══════════════
const A = makeDom(AUTH);
const aw = A.w, ad = A.d, $ = id => ad.getElementById(id);

// N208 冒号校验
$('f_user').value = 'a:b'; $('f_pass').value = 'c';
aw.generate();
check('N208 用户名含冒号阻止生成并提示 RFC 7617', /用户名不能包含冒号|colon/.test($('result').innerHTML), $('result').innerHTML.slice(0, 100));
check('N208 冒号态三项输出被清空（不产出 a:b:c 令牌）',
  !$('tokenOut').value && !$('headerOut').value && !$('urlOut').value,
  'tok=' + $('tokenOut').value + ' hdr=' + $('headerOut').value);
$('f_user').value = 'alice'; $('f_pass').value = 'pw123';
aw.generate();
check('N208 合法用户名仍正常生成令牌', $('tokenOut').value === 'YWxpY2U6cHcxMjM=', $('tokenOut').value);

// N209 charset 提示
$('f_user').value = 'admin'; $('f_pass').value = '密码';
aw.generate();
check('N209 非 ASCII 凭据给出 UTF-8 charset 提示', /UTF-8.*RFC 7617|charset/.test($('result').innerHTML), $('result').innerHTML.slice(0, 160));
check('N209 纯 ASCII 凭据无 charset 提示（不冗余）', (() => {
  $('f_user').value = 'alice'; $('f_pass').value = 'pw123'; aw.generate();
  return !/charset|UTF-8/.test($('result').innerHTML);
})(), $('result').innerHTML.slice(0, 100));

// N210 历史不写密码明文（补证据）
A.history.length = 0;
$('f_user').value = 'admin'; $('f_pass').value = 'secret';
aw.generate();
// 触发 Extras：用页面真实函数（若存在）
try { aw.__basic_auth_generator_last = 0; aw.__basic_auth_generatorExtras(); } catch (e) {}
const histJSON = JSON.stringify(A.history);
check('N210 历史快照不含密码明文', !/secret/.test(histJSON), histJSON.slice(0, 200));
check('N210 历史快照不含 Base64 令牌 / Authorization 头 / 内嵌 URL',
  !/YWxpY2U6c2VjcmV0|Authorization: Basic|@example\.com/.test(histJSON), histJSON.slice(0, 200));
check('N210 快照源码只保留令牌长度（不含 f_pass 收集）', (() => {
  const m = A.html.match(/function __basic_auth_generatorSnap\(\)\{[\s\S]*?\n\}/);
  return !!m && !/f_pass|password|令牌['"]\s*:/.test(m[0]) && /令牌长度/.test(m[0]);
})(), '');

// N211 copyField 空参提示不显示 undefined（补证据）
A.toasts.length = 0; A.copied.length = 0;
$('headerOut').value = 'Authorization: Basic abc';
aw.copyField('headerOut');
check('N211 复制成功提示不含 undefined', A.toasts.every(t => !/undefined/.test(t)), JSON.stringify(A.toasts));
check('N211 复制内容正确写入剪贴板', A.copied.some(v => /Authorization: Basic abc/.test(v)), JSON.stringify(A.copied));

// 状态链：合法 → 冒号非法 → 恢复
$('f_user').value = 'ok'; $('f_pass').value = 'pass'; aw.generate();
const ok1 = $('tokenOut').value;
$('f_user').value = 'bad:user'; aw.generate();
const bad2 = $('tokenOut').value;
$('f_user').value = 'ok2'; aw.generate();
const ok3 = $('tokenOut').value;
check('状态链 合法→冒号非法→恢复：非法清空、恢复重新生成', !!ok1 && bad2 === '' && !!ok3 && ok1 !== ok3, [ok1, bad2, ok3].join(' / '));

// ══════════════ 公式 / i18n 三源（仅修好版）══════════════
if (!OLD_DIR) {
  const enC = JSON.parse(fs.readFileSync('i18n/tools/en/it/char-encoder.json', 'utf8'));
  check('i18n char 已把「HTML 命名」改为「常用 HTML 实体」且英译同步',
    !!enC.map['常用 HTML 实体'] && /Common HTML entities/.test(enC.map['常用 HTML 实体']) && !('HTML 命名' in enC.map), '');
  check('i18n char 格式清单串同步新标签', Object.keys(enC.map).some(k => k.includes('常用 HTML 实体') && k.includes('Unicode 码点')), '');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
