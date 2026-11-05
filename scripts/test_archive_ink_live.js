#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
(async () => {
  const page = fs.readFileSync(path.join(__dirname, '../tools/printing/estimate-ink.html'), 'utf8');
  const script = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function calcSingle()') || s.includes('function calcSingle(live)'));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { runScripts: 'dangerously', url: 'https://example.test/' });
  const document = dom.window.document;
  dom.window.ToolBox = { createTable: () => '' };
  dom.window.eval(script);
  let history = 0;
  dom.window.saveHistory = () => { history++; };
  const area = document.getElementById('sArea');
  area.value = '0.5';
  area.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  await new Promise(resolve => setTimeout(resolve, 350));
  assert.ok(document.getElementById('sRes').textContent.includes('0.5'), '输入应实时计算');
  assert.strictEqual(history, 0, '实时计算不应写入历史');
  document.getElementById('sWaste').checked = false;
  document.getElementById('sWaste').dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  assert.strictEqual(history, 0, '更改损耗选项不应写入历史');
  dom.window.calcSingle();
  assert.strictEqual(history, 1, '手动计算应写入历史');
  console.log('PASS 油墨实时计算与历史');
  dom.window.close();
})().catch(err => { console.error(err); process.exitCode = 1; });
