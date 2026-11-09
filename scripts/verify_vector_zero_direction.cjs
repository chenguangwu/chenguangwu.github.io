#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const html = fs.readFileSync(path.join(__dirname, '../tools/it/vector-magnitude.html'), 'utf8');
const start = html.indexOf('function build(){'), end = html.indexOf('function toggleToolTheme()', start);
assert(start >= 0 && end > start);
for (const language of ['zh-CN', 'en-US']) {
  const dom = new JSDOM(html, {url: 'https://toolbox.local/?lang=' + language, runScripts: 'outside-only'});
  const w = dom.window, d = w.document;
  w.eval(html.slice(start, end));
  for (const dim of [2, 3]) {
    d.getElementById('dim').value = String(dim); w.build();
    for (let i=0;i<dim;i++) d.getElementById('v'+i).value = '0';
    w.calculate();
    const result = d.getElementById('output').textContent;
    assert.match(result, language === 'en-US' ? /Zero vector has no direction/ : /零向量无方向/);
    assert.doesNotMatch(result, /cos α\s*=|θ\s*=|α\s*=/, language + ' zero ' + dim);
    d.getElementById('v0').value = '3'; d.getElementById('v1').value = '4'; w.calculate();
    assert.match(d.getElementById('output').textContent, dim === 2 ? /θ = atan2/ : /cos α = 0\.6/);
  }
  w.close();
}
console.log('vector zero direction: 2D/3D zero and nonzero, Chinese and English passed');
