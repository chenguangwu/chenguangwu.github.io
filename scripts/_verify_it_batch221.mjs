// 第221批 · IT-N185~N190 shell-script-formatter（JSDOM 真机 + bash -n 实算）
//  N185 压缩把 && / | / else / case / heredoc 拼成非法脚本（进批探测：源码已修，补证据销账）
//  N186 行尾 ) 被误判为 case 分支模式，缩进整体漂移
//  N187 单独成行的 then / do 多缩进一级且深度多开一层
//  N188 函数/块闭合 } 未先减级
//  N189 heredoc 起始行不参与缩进，字符串/注释里的 << 被当成 here-doc
//  N190 校验用全局关键字计数（字符串/注释误计）且结果覆盖格式化输出
// 用法：node scripts/_verify_it_batch221.mjs [可选：另一个页面路径，用于旧源码差分]
import fs from 'fs';
import { spawnSync } from 'child_process';
import { JSDOM } from 'jsdom';

const PAGE = process.argv[2] || 'tools/it/shell-script-formatter.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) {
  checks.push([n, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 220) : ''));
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

let tableData = null, exportCalls = [], history = [], langchange = 0;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/shell-script-formatter.html',
  beforeParse(w) {
    w.alert = () => {};
    w.URL.createObjectURL = () => 'blob:probe';
    w.URL.revokeObjectURL = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: {
        isEn: () => false,
        exportTable(sel, name) { exportCalls.push({ sel, name, rows: tableData && tableData.rows }); },
        diffBox() {}
      },
      chart: { line() {}, bar() {} },
      matrix: {
        table(sel, cfg) {
          tableData = cfg;
          const el = w.document.querySelector(sel);
          if (!el) return;
          el.innerHTML = '<tr><th>' + cfg.head.map(esc).join('</th><th>') + '</th></tr>' +
            cfg.rows.map(r => '<tr><td>' + r.map(esc).join('</td><td>') + '</td></tr>').join('');
        }
      },
      preset: { bar() {} },
      history: {
        // 真实 TBKit：list() 返回 {t, d} 包装，last() 返回扁平的 d
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
d.addEventListener('toolbox:langchange', () => { langchange++; });

function fmt(src, indent = '2') {
  $('indent').value = indent;
  $('input').value = src;
  w.formatShell();
  return String($('output').textContent ?? '');
}
function minify(src) {
  $('input').value = src;
  w.minifyShell();
  return String($('output').textContent ?? '');
}
function validate(src) {
  $('input').value = src;
  w.doValidate();
  return { err: String($('err').textContent ?? ''), cls: $('err').className };
}
function depths(txt) { return txt.split('\n').map(x => (x.match(/^ */) || [''])[0].length); }
function bashOK(script) {
  const r = spawnSync('bash', ['-n'], { input: script, encoding: 'utf8' });
  return { ok: r.status === 0, err: (r.stderr || '').trim() };
}
const IF_AND = 'if true; then\n echo a &&\n echo b\nfi';
const IF_ELSE = 'if true; then\necho a\nelse\necho b\nfi';
const CASE_SRC = 'case "$1" in\n  start)\n    echo start\n    ;;\n  *)\n    echo usage\n    ;;\nesac';
const HEREDOC_SRC = 'cat <<EOF\nhello world\nEOF\necho done';

// ══════════════ N185 压缩（进批探测：已由其他 Agent 修好，补真机证据） ══════════════
const m1 = minify(IF_AND);
check('N185 && 续行压缩保留换行且不插分号', /echo a &&\necho b/.test(m1) && !m1.includes('&&;'), JSON.stringify(m1));
check('N185 && 续行压缩结果 bash -n 通过', bashOK(m1).ok, bashOK(m1).err);
const m2 = minify(IF_ELSE);
check('N185 else 行不被拼成 else;', /\nelse\n/.test(m2) && !m2.includes('else;'), JSON.stringify(m2));
check('N185 if/else 压缩结果 bash -n 通过', bashOK(m2).ok, bashOK(m2).err);
const m3 = minify(CASE_SRC);
check('N185 case ... in 压缩结果 bash -n 通过', bashOK(m3).ok, bashOK(m3).err);
const m4 = minify(HEREDOC_SRC);
check('N185 heredoc 正文原样保留且未插入分号', /cat <<EOF\nhello world\nEOF/.test(m4) && !m4.includes(';'), JSON.stringify(m4));
check('N185 heredoc 压缩结果 bash -n 通过', bashOK(m4).ok, bashOK(m4).err);
const m5 = minify('  echo "a <<EOF"\n    echo next  ');
check('N185 字符串里的 <<EOF 不再误触发 heredoc（下一行仍被 trim）',
  m5.split('\n')[1] === 'echo next', JSON.stringify(m5));

// ══════════════ N186 行尾 ) 误判为 case 分支 ══════════════
const f1 = fmt('if true; then\necho $(date)\necho hi\nfi', '2');
check('N186 echo $(date) 后缩进不漂移（0,2,2,0）', depths(f1).join(',') === '0,2,2,0', depths(f1).join(','));
check('N186 命令替换格式化结果 bash -n 通过', bashOK(f1).ok, bashOK(f1).err);
const f2 = fmt('arr=(1 2 3)\necho done', '2');
check('N186 数组赋值不误开层级（0,0）', depths(f2).join(',') === '0,0', depths(f2).join(','));
const f3 = fmt('if true; then\necho $(date)\necho hi\nfi', '4');
check('N186 4 空格档同样不漂移（0,4,4,0）', depths(f3).join(',') === '0,4,4,0', depths(f3).join(','));

// ══════════════ N187 单独成行的 then / do ══════════════
const f4 = fmt('if [ "$x" = 1 ]\nthen\necho hi\nfi', '2');
check('N187 then 与 if 同列、正文一级、fi 与 if 同列（0,0,2,0）', depths(f4).join(',') === '0,0,2,0', depths(f4).join(','));
check('N187 多行 then 格式化结果 bash -n 通过', bashOK(f4).ok, bashOK(f4).err);
const f5 = fmt('for f in *\ndo\necho "$f"\ndone', '2');
check('N187 do 与 for 同列、正文一级、done 与 for 同列（0,0,2,0）', depths(f5).join(',') === '0,0,2,0', depths(f5).join(','));
check('N187 多行 do 格式化结果 bash -n 通过', bashOK(f5).ok, bashOK(f5).err);

// ══════════════ N188 } 闭合本行减级 ══════════════
const f6 = fmt('f() {\necho x\n}', '2');
check('N188 } 与 { 同列（0,2,0）', depths(f6).join(',') === '0,2,0', depths(f6).join(','));
check('N188 函数格式化结果 bash -n 通过', bashOK(f6).ok, bashOK(f6).err);
const f7 = fmt(String(w.eval('SAMPLE')), '2');
const sampleLines = f7.split('\n');
const braceOpen = sampleLines.findIndex(x => x.trim() === '}');
const idxFn = sampleLines.findIndex(x => /^backup\(\) \{$/.test(x.trim()));
// 比较「前导空格数」而不是整行长度（"backup() {" 与 "}" 本身长度不同）
const lead = x => (String(x).match(/^ */) || [''])[0].length;
check('N188 自带示例里的 } 与函数声明同列', braceOpen > 0 && idxFn >= 0 &&
  lead(sampleLines[braceOpen]) === lead(sampleLines[idxFn]),
  'lines=' + sampleLines.length + ' fnLead=' + (idxFn >= 0 ? lead(sampleLines[idxFn]) : '?') +
  ' closeLead=' + (braceOpen >= 0 ? lead(sampleLines[braceOpen]) : '?'));

// ══════════════ N189 heredoc 缩进与误判 ══════════════
const f8 = fmt('if true; then\ncat <<EOF\nhello world\nEOF\nfi', '2');
check('N189 heredoc 起始行参与缩进、正文原样保留',
  f8.split('\n')[1] === '  cat <<EOF' && f8.includes('\nhello world\nEOF\n'), JSON.stringify(f8));
check('N189 heredoc 缩进结果 bash -n 通过', bashOK(f8).ok, bashOK(f8).err);
const f9 = fmt('if true; then\necho "a <<EOF"\necho done\nfi', '2');
check('N189 字符串里的 << 不触发 heredoc（后续行正常缩进）',
  depths(f9).join(',') === '0,2,2,0', depths(f9).join(','));
const f10 = fmt('if true; then\n# cat <<EOF\necho done\nfi', '2');
check('N189 注释里的 << 不触发 heredoc（后续行正常缩进）',
  depths(f10).join(',') === '0,2,2,0', depths(f10).join(','));
const f11 = fmt(CASE_SRC, '2');
// case 8 行：case(0) / pattern(2) / body(4) / ;;(2) / pattern(2) / body(4) / ;;(2) / esac(0)
check('N189/N186 case 分支层级正确（0,2,4,2,2,4,2,0）',
  depths(f11).join(',') === '0,2,4,2,2,4,2,0', depths(f11).join(','));
check('N189 case 格式化结果 bash -n 通过', bashOK(f11).ok, bashOK(f11).err);

// ══════════════ N190 校验剥离噪声且不覆盖输出 ══════════════
fmt('if true; then\necho hi\nfi', '2');
const before = String($('output').textContent ?? '');
const v1 = validate('echo "if fi"\n# done esac\necho "{"');
check('N190 字符串/注释里的关键字与括号不误计（校验通过）', /校验通过/.test(v1.err) && !/未平衡/.test(v1.err), v1.err.slice(-80));
check('N190 校验不覆盖「输出结果」', String($('output').textContent ?? '') === before,
  JSON.stringify(String($('output').textContent ?? '').slice(0, 50)));
check('N190 校验结果写入状态栏且含统计', /块开头/.test(v1.err) && /行数: 3/.test(v1.err), v1.err.slice(0, 60));
check('N190 通过态状态栏为绿色 ok 类', /\bok\b/.test(v1.cls), v1.cls);
const v2 = validate('if true; then\necho "fi"\necho hi');
check('N190 真实不平衡脚本报「块未平衡」', /块未平衡/.test(v2.err), v2.err.slice(-80));
check('N190 失败态状态栏不为 ok 类', !/\bok\b/.test(v2.cls), v2.cls);
const v3 = validate('cat <<EOF\nif fi done esac {{ }}\nEOF\necho ok');
check('N190 heredoc 正文里的关键字不参与计数（校验通过）', /校验通过/.test(v3.err) && !/未平衡/.test(v3.err), v3.err.slice(-80));
check('N190 校验剥离函数 shellCode 存在且剥掉字符串', typeof w.shellCode === 'function' &&
  !/<<EOF/.test(w.shellCode('echo "a <<EOF"')), typeof w.shellCode);

// ══════════════ 全链路 / 状态链 / 导出 ══════════════
history = []; tableData = null; exportCalls = [];
$('indent').value = '2';
$('input').value = 'if true; then\necho z221\nfi';
w.doBeautify();
const chainOut = String($('output').textContent ?? '');
check('链路 doBeautify 输出含注入值', /echo z221/.test(chainOut), chainOut.slice(0, 80));
check('链路 历史记录 1 条且结果取自 output', history.length === 1 &&
  String((history[0].d || {})['结果'] ?? '').includes('echo z221'), 'history=' + history.length);
check('链路 明细表 head 含「结果」列且 rows 含该结果', !!tableData &&
  tableData.head.includes('结果') && tableData.rows.some(r => r.some(c => String(c).includes('echo z221'))),
  tableData ? tableData.head.join('/') : 'no table');
w.__shell_script_formatterExport();
check('链路 导出走明细表且携带结果行', exportCalls.length >= 1 &&
  exportCalls[0].sel === '#shell_script_formatterTable' &&
  (exportCalls[0].rows || []).some(r => r.some(c => String(c).includes('echo z221'))),
  'exports=' + exportCalls.length);
// 快速连续不同输入：末次生效、无异常
let seqErr = null;
try {
  $('input').value = 'echo first'; w.doBeautify();
  $('input').value = 'echo second'; w.doBeautify();
} catch (e) { seqErr = e.message; }
check('状态链 快速连续两次不同输入无异常且末次生效', seqErr === null &&
  /echo second/.test(String($('output').textContent ?? '')) && !/echo first/.test(String($('output').textContent ?? '')), seqErr || '');
// 非法/空输入
let emptyErr = null;
try { $('input').value = ''; w.doBeautify(); w.minifyShell(); w.doValidate(); } catch (e) { emptyErr = e.message; }
check('状态链 空输入三入口均不抛错', emptyErr === null, emptyErr || '');
// 清空
w.clearAll();
check('状态链 清空后 output 为占位文案且状态栏为空',
  /等待输入/.test(String($('output').textContent ?? '')) && String($('err').textContent ?? '') === '',
  String($('output').textContent ?? '').slice(0, 40));
// 恢复合法输入
let recoverErr = null;
try { $('input').value = 'echo recovered'; w.doBeautify(); } catch (e) { recoverErr = e.message; }
check('状态链 非法→恢复后正常产出', recoverErr === null && /echo recovered/.test(String($('output').textContent ?? '')), recoverErr || '');

// ══════════════ 公式与 i18n 三源 ══════════════
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/shell-script-formatter.json', 'utf8'));
// 公式文本里含字面量 <<，不能用 [^<]*（会在 << 处截断），改用非贪婪任意字符
const formulaNew = html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
check('公式 页面 formula-eq 已改为新算法说明', !!formulaNew && /case 块计数/.test(formulaNew[1]) && /不插入分号/.test(formulaNew[1]),
  formulaNew ? formulaNew[1].slice(0, 50) : 'missing');
check('公式 en JSON 含同文中文键与英译', !!formulaNew && !!en.map[formulaNew[1]] &&
  /case-block counter/.test(en.map[formulaNew[1]]),
  formulaNew ? String(en.map[formulaNew[1]] || '').slice(0, 60) : 'no formula');
check('公式 旧宽泛判据文案已清除', !/以右括号结尾时深度再加 1/.test(html) && !/ending with a closing parenthesis add another 1/.test(JSON.stringify(en.map)), '');

// ══════════════ 汇总 ══════════════
const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exit(1);
}
