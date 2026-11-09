#!/usr/bin/env node
// Focused tests of the page's own UTF-8 decoder and asynchronous clipboard handling.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const html = fs.readFileSync(path.join(__dirname, '../tools/it/hex-to-text.html'), 'utf8');
const script = html.match(/<script>\s*(function hexEnglish\(\)[\s\S]*?)<\/script>/);
assert(script, 'page decoder script not found');
const elements = Object.fromEntries(['input', 'output', 'hexStatus', 'hex_to_textTable', 'hex_to_textDiff', 'hex_to_textChart'].map(id => [id, {value: '', textContent: ''}]));
const document = {documentElement: {lang: 'zh-CN'}, getElementById: id => elements[id] || null};
let copied = '';
const navigator = {clipboard: {writeText: async value => {copied = value;}}};
const ctx = {document, navigator, TextDecoder, Uint8Array, setTimeout};
vm.createContext(ctx);
vm.runInContext(script[1], ctx);
(async () => {
  elements.input.value = '0xE4 0xB8 0xAD F0 9F 98 80';
  ctx.convert();
  assert.strictEqual(elements.output.value, '中😀');
  assert.strictEqual(elements.hexStatus.textContent, '');
  await ctx.copyResult();
  assert.strictEqual(copied, '中😀');
  assert.match(elements.hexStatus.textContent, /已复制/);
  for (const value of ['80', 'C0 AF', 'E4 B8']) {
    elements.input.value = value;
    elements.output.value = '上次结果';
    elements.hex_to_textTable.textContent = '上次结果';
    ctx.convert();
    assert.strictEqual(elements.output.value, '', value + ': stale output');
    assert.strictEqual(elements.hex_to_textTable.textContent, '', value + ': stale table');
    assert.match(elements.hexStatus.textContent, /不是有效的 UTF-8/, value);
  }
  for (const [value, expected] of [['G1', /十六进制字符/], ['A', /必须为偶数/], ['0x', /十六进制字符/]]) {
    elements.input.value = value;
    elements.output.value = '上次结果';
    ctx.convert();
    assert.strictEqual(elements.output.value, '');
    assert.match(elements.hexStatus.textContent, expected);
  }
  elements.input.value = '4869';
  ctx.convert();
  navigator.clipboard.writeText = async () => {throw new Error('denied');};
  await ctx.copyResult();
  assert.match(elements.hexStatus.textContent, /复制失败/);
  delete navigator.clipboard;
  await ctx.copyResult();
  assert.match(elements.hexStatus.textContent, /复制失败/);
  document.documentElement.lang = 'en-US';
  elements.input.value = 'FF';
  ctx.convert();
  assert.strictEqual(elements.output.value, '');
  assert.match(elements.hexStatus.textContent, /not valid UTF-8/);
  elements.input.value = '4869';
  ctx.convert();
  await ctx.copyResult();
  assert.match(elements.hexStatus.textContent, /Copy failed/);
  console.log('hex-to-text: strict UTF-8, stale state, clipboard and language checks passed');
})().catch(error => {console.error(error); process.exitCode = 1;});
