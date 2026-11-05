#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const page = fs.readFileSync(path.join(__dirname, '../tools/process/rolled-throughput-yield.html'), 'utf8');
const script = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function __tbInputGuard'));
const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { runScripts: 'dangerously' });
const document = dom.window.document;
dom.window.ToolBox = { setResult: (id, text) => { document.getElementById(id).innerHTML = text; } };
dom.window.eval(script);
for (const [value, valid] of [['98', true], ['101', false], ['-5', false]]) {
  document.getElementById('y1').value = value;
  dom.window.calcTool();
  const result = document.getElementById('result').textContent;
  assert.strictEqual(result.includes('RTY (%)'), valid, `良率 ${value}% 的判定错误：${result}`);
  if (!valid) assert.ok(result.includes('良率'), '无效良率应给出提示');
}
console.log('PASS 工序良率范围校验');
dom.window.close();
