#!/usr/bin/env node
/**
 * escHtml 回归护栏
 *
 * 目的：js/common.js 的 ToolBox.escHtml 被全站 1400+ 处调用，且大量用于
 * value="..." 属性上下文。历史上它用 textContent→innerHTML 实现，只编码
 * & < > 而放过引号，导致 66 处/53 页属性注入。本脚本锁定两件事：
 *   1) & < > " ' 必须全部编码；
 *   2) 不得回退成 textContent→innerHTML（引号不被放过）。
 *
 * 运行：node scripts/verify_esc_html.js
 * 退出码：0 = 全部通过；1 = 存在回归。
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
let failed = 0;

function check(name, ok, detail) {
  console.log(`${ok ? '✅' : '❌'} ${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) failed++;
}

// 1) 取出 escHtml 定义并求值
const commonSrc = fs.readFileSync(path.join(ROOT, 'js', 'common.js'), 'utf8');
const m = commonSrc.match(/function\s+escHtml\s*\(s\)\s*\{[\s\S]*?\n\}/);
check('js/common.js 中存在 escHtml 定义', !!m);
let escHtml = null;
if (m) {
  try { escHtml = new Function('return (' + m[0] + ')')(); }
  catch (e) { check('escHtml 定义可解析', false, e.message); }
}

if (escHtml) {
  // 2) 回归护栏：不得回退成 textContent→innerHTML
  check(
    '实现未回退为 textContent→innerHTML',
    !/textContent/.test(m[0]) && !/d\.innerHTML/.test(m[0]),
    '函数体内不得出现 textContent / d.innerHTML'
  );

  // 3) 五类字符全部编码
  const input = '"\'<>&';
  const output = escHtml(input);
  check('双引号 " 被编码为 &quot;', output.includes('&quot;') && !output.includes('"'), output);
  check('单引号 \' 被编码为 &#39;', output.includes('&#39;') && !output.includes("'"), output);
  check('< 被编码为 &lt;', output.includes('&lt;') && !output.includes('<'), output);
  check('> 被编码为 &gt;', output.includes('&gt;') && !output.includes('>'), output);
  check('& 被编码为 &amp;', output.includes('&amp;'), output);

  // 4) 属性上下文典型载荷整串必须不含裸引号/尖括号
  const payload = 'a" onmouseover="alert(1)';
  const escaped = escHtml(payload);
  check('属性注入载荷被完整编码', escaped === 'a&quot; onmouseover=&quot;alert(1)', escaped);

  // 5) 空值语义保持
  check('null / undefined 返回空串', escHtml(null) === '' && escHtml(undefined) === '');
}

// 6) 真实调用页抽查：静态源码中必须有 escHtml( 调用
const spotPages = [
  'tools/it/api-sign-generator.html',
  'tools/advertising/storyboard-timeline.html',
  'tools/metalwork/analysis-35.html'
];
for (const rel of spotPages) {
  const p = path.join(ROOT, rel);
  const exists = fs.existsSync(p);
  check(`调用页存在：${rel}`, exists);
  if (exists) {
    const src = fs.readFileSync(p, 'utf8');
    check(`调用页含 escHtml(：${rel}`, /escHtml\s*\(/.test(src));
  }
}

console.log(`\n==== escHtml regression: fail=${failed} ====`);
process.exit(failed === 0 ? 0 : 1);
