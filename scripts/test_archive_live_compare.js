#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

(async () => {
  const page = fs.readFileSync(path.join(__dirname, '../tools/biz/text-compare.html'), 'utf8');
  const script = page.match(/function getLines\(id\)\{[\s\S]*?\ncompare\(\);/)[0];
  const html = page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  const dom = new JSDOM(html, { runScripts: 'dangerously' });
  dom.window.eval(script);
  const document = dom.window.document;
  assert.strictEqual(document.getElementById('similarity').textContent, '38%');
  const left = document.getElementById('left');
  left.value = 'ToolBox 文本工具';
  left.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  await new Promise(resolve => setTimeout(resolve, 350));
  assert.strictEqual(document.getElementById('similarity').textContent, '17%', '输入后应实时刷新比较结果');
  const right = document.getElementById('right');
  right.value = 'toolbox 文本工具';
  right.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  await new Promise(resolve => setTimeout(resolve, 350));
  assert.strictEqual(document.getElementById('similarity').textContent, '0%');
  const ignoreCase = document.getElementById('ignoreCase');
  ignoreCase.checked = true;
  ignoreCase.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  await new Promise(resolve => setTimeout(resolve, 350));
  assert.strictEqual(document.getElementById('similarity').textContent, '100%', '更改选项后应实时刷新比较结果');
  left.value = '待清空';
  left.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  dom.window.clearAll();
  await new Promise(resolve => setTimeout(resolve, 350));
  assert.strictEqual(document.getElementById('leftResult').textContent, '点击"对比"按钮开始...', '清空后不能执行延迟比较');
  console.log('PASS 文本比较实时输入、选项和清空');
  dom.window.close();
})().catch(err => { console.error(err); process.exitCode = 1; });
