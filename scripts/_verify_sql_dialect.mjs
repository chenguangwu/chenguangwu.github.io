// IT-N282 方言切换强锁（verify harness stub DOM 不解析 onchange 属性，故独立用 JSDOM 真机验证）
// 用法: node scripts/_verify_sql_dialect.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/sql-escape.html', 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://x.com/tools/it/sql-escape.html' });
const w = dom.window, d = w.document;
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

// 1) select#dialect 必须绑定 onchange=__escLive()
const sel = d.getElementById('dialect');
check('dialect 绑定 onchange=__escLive()', /__escLive\(\)/.test(sel.getAttribute('onchange') || ''),
  String(sel.getAttribute('onchange')));

// 2) 真实派发 change：MySQL 转义结果在切到 PostgreSQL 后必须重算
d.getElementById('input').value = "It's fine";
w.esc();
const before = d.getElementById('output').value;
check('MySQL 初始转义为反斜杠写法', before === "It\\'s fine", JSON.stringify(before));
sel.value = 'postgres';
sel.dispatchEvent(new w.Event('change', { bubbles: true }));
const after = d.getElementById('output').value;
check('切 PostgreSQL 后自动重算为双单引号', after === "It''s fine", JSON.stringify(after));

// 3) 切回 MySQL 也应自动重算回反斜杠写法
sel.value = 'mysql';
sel.dispatchEvent(new w.Event('change', { bubbles: true }));
check('切回 MySQL 自动重算回反斜杠', d.getElementById('output').value === "It\\'s fine",
  JSON.stringify(d.getElementById('output').value));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
