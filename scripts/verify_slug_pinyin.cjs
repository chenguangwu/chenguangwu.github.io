#!/usr/bin/env node
// Focused browser-DOM check using the exact locally shipped library and page functions.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'tools/it/slug-generator-advanced.html'), 'utf8');
const dom = new JSDOM(html, { url: 'https://toolbox.local/tools/it/slug-generator-advanced.html', runScripts: 'outside-only' });
const w = dom.window;
w.eval(fs.readFileSync(path.join(root, 'js/pinyin-pro-3.29.5.min.js'), 'utf8'));
const start = html.indexOf('function randInt('), end = html.indexOf('function toggleToolTheme(', start);
assert(start >= 0 && end > start);
w.eval(html.slice(start, end));
const cases = [
  ['Hello 世界!', 'hello-shi-jie'],
  ['我的博客文章标题 - Part 1', 'wo-de-bo-ke-wen-zhang-biao-ti-part-1'],
  ['人工智能技术', 'ren-gong-zhi-neng-ji-shu'],
  ['产品发布', 'chan-pin-fa-bu'],
  ['高级 Slug 生成器', 'gao-ji-slug-sheng-cheng-qi'],
  ['重庆银行', 'chong-qing-yin-hang']
];
for (const [input, expected] of cases) assert.strictEqual(w.slugify(input, []), expected, input);
w.document.querySelector('#sep').value = '__';
assert.strictEqual(w.slugify('中文 test', []), 'zhong__wen__test');
w.document.querySelector('#trimSym').checked = false;
assert.strictEqual(w.slugify('中文', []), 'zhong__wen');
w.document.querySelector('#sep').value = '-';
w.document.querySelector('#trimSym').checked = true;
w.document.querySelector('#text').value = '𠀀龘';
w.generate();
assert(w.document.querySelector('#output').textContent.includes('u20000-da'));
assert(w.document.querySelector('#output').textContent.includes('未找到拼音'));
w.pinyinPro = undefined;
w.generate();
assert(w.document.querySelector('#output').textContent.includes('拼音数据未加载'));
assert(!w.document.querySelector('#output').textContent.includes('u20000-da'));
w.close();
console.log('slug pinyin: Chinese, polyphones, separator, unknown and missing library checks passed');
