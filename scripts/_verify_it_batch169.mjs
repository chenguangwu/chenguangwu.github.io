import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/regex-common.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

function boot(lang) {
  return new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.com/tools/it/regex-common.html' + (lang ? '?lang=' + lang : ''),
    beforeParse(w) {
      w.i18nText = k => k;
      w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); }, setResult(id, v) { const el = w.document.getElementById(id); if (el) el.innerHTML = v; } };
      w.TBKit = {
        util: { isEn: () => lang === 'en-US', exportTable() {}, diffBox() {} },
        chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
      };
    }
  });
}

const dom = boot();
const w = dom.window;
const d = w.document;
const cat = d.getElementById('cat');

// 结构：8 个真实 option + 默认 email
check('下拉含 8 个 option', cat.options.length === 8, 'options=' + cat.options.length);
check('默认选中 email', cat.value === 'email', 'value=' + cat.value);
const vals = Array.from(cat.options).map(o => o.value).join(',');
check('8 类值齐全', vals === 'email,phone,idcard,url,ipv4,date,chinese,username', vals);

function run(c, txt) {
  cat.value = c;
  d.getElementById('txt').value = txt;
  cat.dispatchEvent(new w.Event('change', { bubbles: true }));
  w.calcTool();
  return d.getElementById('result').textContent;
}

// 8 类切换：每类注入该类专属文本，断言输出类别名 + 命中内容
{
  const o = run('email', 'a@b.com');
  check('email 切换', o.includes('邮箱地址') && o.includes('a@b.com'), o.slice(0, 70));
}
{
  const o = run('phone', '13812345678');
  check('phone 切换', o.includes('中国大陆手机号') && o.includes('13812345678'), o.slice(0, 70));
}
{
  const o = run('idcard', '11010119900101123X');
  check('idcard 切换', o.includes('身份证号') && o.includes('11010119900101123X'), o.slice(0, 70));
}
{
  const o = run('url', 'https://example.com/x');
  check('url 切换', o.includes('URL 链接') && o.includes('https://example.com/x'), o.slice(0, 70));
}
{
  const o = run('ipv4', '10.0.0.1');
  check('ipv4 切换', o.includes('IPv4 地址') && o.includes('10.0.0.1'), o.slice(0, 70));
}
{
  const o = run('date', '2026-01-02');
  check('date 切换', o.includes('日期 YYYY-MM-DD') && o.includes('2026-01-02'), o.slice(0, 70));
}
{
  const o = run('chinese', '中文abc');
  check('chinese 切换', o.includes('中文字符') && o.includes('中文'), o.slice(0, 70));
}
{
  const o = run('username', 'user_123');
  check('username 切换', o.includes('用户名(字母数字_3-16)') && o.includes('user_123'), o.slice(0, 70));
}
// 切换确实改变结果：同一输入在 email / phone 下结论不同
{
  const txt = 'a@b.com 13812345678';
  const a = run('email', txt), b = run('phone', txt);
  check('同文本切换类别改变结果', a.includes('邮箱地址') && b.includes('中国大陆手机号') && a !== b, 'email≠phone');
}
// 重置回到 email
{
  w.resetForm();
  check('resetForm 回 email', cat.value === 'email', 'value=' + cat.value);
}
// 英文态：i18n 脚本未在此脚本加载，仅确认 option 中文文本已就位（--check 负责英语残留验收）
{
  const labels = Array.from(cat.options).map(o => o.textContent).join('|');
  check('option 中文原文就位', labels.includes('邮箱地址') && labels.includes('中国大陆手机号'), labels.slice(0, 80));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch169 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
