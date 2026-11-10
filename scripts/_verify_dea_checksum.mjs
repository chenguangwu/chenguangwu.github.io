import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const html = readFileSync('tools/finance/dea-validator.html', 'utf8');
const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: new VirtualConsole() });
const { window } = dom;
const input = window.document.getElementById('input');
const output = window.document.getElementById('output');
assert.equal(input.value, 'AB1111119', 'default example uses a correct check digit');
for (const base of ['123456', '013462', '011878', '999999', '000000', '123040']) {
  const digits = [...base].map(Number);
  const check = (digits[0] + digits[2] + digits[4] + 2 * (digits[1] + digits[3] + digits[5])) % 10;
  for (const [suffix, valid] of [[check, true], [(check + 1) % 10, false]]) {
    input.value = `AB${base}${suffix}`;
    window.validate();
    assert.ok(output.textContent.includes(valid ? '✅ 通过' : '❌ 未通过'), `${input.value}: ${output.textContent}`);
  }
}
assert.match(window.document.querySelector('.deep-dive').textContent, /不代表。DEA 注册状态/);
window.close();
console.log('PASS DEA checksum examples and registration disclaimer');
