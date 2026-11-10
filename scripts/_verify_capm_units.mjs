import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const html = readFileSync(process.env.CAPM_HTML || 'tools/finance/capm-return.html', 'utf8');
const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: new VirtualConsole() });
const w = dom.window, d = w.document;
const el = id => d.getElementById(id);
function fill(rf, rm, obs, beta = '1.2') {
  for (const [id, v] of Object.entries({rf, rm, obs, beta})) el(id).value = v;
  w.capmCalc();
}
function check(label, expected, result) {
  const actual = ['unit', 'rf', 'rm', 'obs', 'beta'].map(id => el(id).value);
  assert.deepEqual(actual, expected, `${label}: fields`);
  assert.ok(el('result').textContent.includes(result), `${label}: result ${el('result').textContent}`);
  console.log(`PASS ${label}`);
}
function change(unit) { el('unit').value = unit; w.__capmSwitchUnit(); }
fill('0.003', '0.008', '0.01');
change('100'); check('low rates to percent', ['100', '0.3', '0.8', '1', '1.2'], '0.9000%');
w.__capmSwitchUnit(); check('duplicate change', ['100', '0.3', '0.8', '1', '1.2'], '0.9000%');
change('1'); check('low rates roundtrip', ['1', '0.003', '0.008', '0.01', '1.2'], '0.9000%');
fill('2', '1.2', '-0.01'); change('100'); check('over 100 and negative', ['100', '200', '120', '-1', '1.2'], '104.0000%');
change('1'); check('large rates roundtrip', ['1', '2', '1.2', '-0.01', '1.2'], '104.0000%');
fill('0.01', '0', '', '1'); change('100'); check('one percent, zero and optional blank', ['100', '1', '0', '', '1'], '0.0000%');
assert.ok(!el('result').textContent.includes('α ='), 'blank optional observation must not produce alpha');
change('1'); check('one percent roundtrip', ['1', '0.01', '0', '', '1'], '0.0000%');
fill('', '0.08', '0.1'); change('100'); check('required blank', ['100', '', '8', '10', '1.2'], '请输入无风险利率');
assert.equal(el('statGrid').textContent, '', 'required blank clears old statistics');
w.resetForm(); check('reset from percent', ['1', '0.03', '0.08', '0.10', '1.2'], '9.0000%');
change('100'); check('switch after reset', ['100', '3', '8', '10', '1.2'], '9.0000%');
w.close();
