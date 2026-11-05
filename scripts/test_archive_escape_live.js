#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const slugs = ['c-string', 'css', 'go', 'java', 'js', 'php', 'python', 'regex', 'rust', 'sql'];
for (const slug of slugs) {
  const page = fs.readFileSync(path.join(__dirname, `../tools/it/${slug}-escape.html`), 'utf8');
  const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const script = scripts.find(s => /function esc\(/.test(s));
  assert.ok(script, `${slug}: 转义脚本不存在`);
  const html = page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  const dom = new JSDOM(html, { runScripts: 'dangerously' });
  let alerts = 0;
  dom.window.alert = () => { alerts++; };
  dom.window.eval(script);
  const input = dom.window.document.getElementById('input');
  const output = dom.window.document.getElementById('output');
  input.value = 'a("b)';
  input.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  assert.ok(output.value && output.value !== 'a("b)', `${slug}: 输入应实时生成转义结果`);
  input.value = '';
  input.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  assert.strictEqual(output.value, '', `${slug}: 清空输入应清空输出`);
  assert.strictEqual(alerts, 0, `${slug}: 实时输入不能弹窗`);
  if (slug === 'go' || slug === 'rust') {
    dom.window.document.getElementById('kind').value = slug === 'go' ? 'rune' : 'char';
    input.value = 'ab';
    input.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
    assert.strictEqual(output.value, '', `${slug}: 多字符不能生成单字符字面量`);
    assert.strictEqual(alerts, 0, `${slug}: 实时输入非法字符不能弹窗`);
    dom.window.esc();
    assert.strictEqual(alerts, 1, `${slug}: 手动转义非法字符应提示`);
  }
  console.log('PASS', slug);
  dom.window.close();
}
