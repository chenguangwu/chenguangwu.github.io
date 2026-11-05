#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
for (const [slug, id, value] of [
  ['capillary-pressure', 'g', '0.05'],
  ['capillary-rise', 'gamma', '0.05'],
  ['cavitation-number', 'p', '80000'],
  ['chezy-velocity', 'C', '60'],
]) {
  const page = fs.readFileSync(path.join(__dirname, `../tools/fluid/${slug}.html`), 'utf8');
  const script = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function calcTool()'));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { runScripts: 'dangerously' });
  const document = dom.window.document;
  dom.window.ToolBox = { setResult: (target, text) => { document.getElementById(target).innerHTML = text; } };
  dom.window.eval(script);
  const before = document.getElementById('result').textContent;
  const field = document.getElementById(id);
  field.value = value;
  field.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  assert.notStrictEqual(document.getElementById('result').textContent, before, `${slug}: 输入改变后应刷新结果`);
  console.log('PASS', slug);
  dom.window.close();
}
