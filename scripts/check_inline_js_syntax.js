#!/usr/bin/env node
/*
 * 门禁：工具页 inline <script> 语法检查
 *
 * 背景（缺陷 N）：构建期英文预渲染曾把英文 intro 注入到 <script> 内 JS 字符串
 * 的 <p> 提示位，未转义撇号 / 引入换行 → 脚本整块 SyntaxError，计算器静默失效。
 * 这类故障不会被既有门禁（静态结构 / 链接 / 资源 / calc 冒烟 / 用例断言）捕获，
 * 故单列一道：逐页对所有 inline 脚本做语法解析，任一失败即红。
 *
 * 判定口径：
 *  - 只查「内联」脚本（无 src），跳过 type=module（无法用 new Function 解析）
 *    与非 JS 类型（application/ld+json、importmap 等）。
 *  - 跳过含字面 "<script" 的片段（抽取不可靠，非本门禁职责）与 TOOLBOX-API-STUB。
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const TOOLS = path.join(ROOT, 'tools');

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const files = walk(TOOLS, []);
let checked = 0;
const bad = [];

for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const re = /<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/g;
  let m;
  while ((m = re.exec(html))) {
    const attrs = m[1] || '';
    const code = m[2];
    if (!code.trim()) continue;
    if (/type\s*=\s*["']module["']/.test(attrs)) continue;
    const tm = attrs.match(/type\s*=\s*["']([^"']*)["']/);
    if (tm && !/javascript/i.test(tm[1])) continue;
    if (/<script/i.test(code)) continue;
    if (/TOOLBOX-API-STUB/.test(code)) continue;
    checked++;
    try {
      // 仅做语法解析（不执行）
      new Function(code);
    } catch (err) {
      bad.push({ file: path.relative(ROOT, f), err: err.message });
      break; // 每页只报一次
    }
  }
}

console.log('inline scripts checked: %d', checked);
if (bad.length) {
  console.error('\n✗ inline JS 语法错误 %d 页：', bad.length);
  for (const b of bad) console.error('   %s :: %s', b.file, b.err);
  console.error('\n提示：多为构建期注入把文案写进 JS 字符串时未转义引号/换行所致（缺陷 N）。');
  process.exit(1);
}
console.log('✓ 全部 inline JS 语法正确');
