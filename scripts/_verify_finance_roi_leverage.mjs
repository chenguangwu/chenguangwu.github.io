import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM, VirtualConsole } from 'jsdom';

function page(slug, setup) {
  return new JSDOM(readFileSync(`tools/finance/${slug}.html`, 'utf8'), {
    url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(),
    beforeParse(window) { if (setup) setup(window); }
  });
}
function set(window, values) {
  for (const [id, value] of Object.entries(values)) window.document.getElementById(id).value = value;
}
for (const en of [false, true]) {
  const dom = page('calc-5', w => {
    w.eval(readFileSync('js/toolbox-stub.js', 'utf8'));
    w.TBKit = { util: { isEn: () => en } };
  });
  const w = dom.window, d = w.document;
  for (const [value, expected, error] of [['0', '-100.00%', false], ['-50000', '—', true], ['50000', '-12.94%', false]]) {
    set(w, { cost: '100000', value, extra: '0', years: '5' });
    w.calc();
    assert.equal(d.querySelectorAll('#summary .num')[2].textContent, expected);
    const text = d.getElementById('res').textContent;
    if (error) assert.match(text, en ? /Loss exceeds principal; compound annualization is undefined/ : /亏损超过本金，无法按复利年化/);
    else {
      assert.match(text, new RegExp(expected.replace('.', '\\.')));
      assert.doesNotMatch(text, /亏损超过本金|Loss exceeds principal/);
    }
  }
  w.close();
}
{
  const dom = page('analysis-risk');
  const w = dom.window, d = w.document;
  for (const interest of ['0', '10000']) {
    set(w, { s: '1000000', v: '600000', f: '400000', i: interest, t: '25', n: '100000', dec: '2' });
    w.calc();
    assert.deepEqual([...d.querySelectorAll('#statGrid .val')].slice(0, 3).map(e => e.textContent), ['—', '—', '—']);
    assert.match(d.getElementById('res').textContent, /DOL\/DFL\/DCL 杠杆系数无定义/);
    assert.match(d.getElementById('res').textContent, /DFL = 0\.00 ÷ \(0\.00 − (?:0|10000)\.00\) = —/);
  }
  w.close();
}
{
  const dom = page('currency-lookup');
  const w = dom.window, d = w.document;
  for (const [code, expected] of [['JPY', '0（无小数）'], ['USD', '2（1/100）']]) {
    set(w, { input: code }); w.validate();
    assert.ok(d.getElementById('output').textContent.includes(expected));
  }
  w.close();
}
console.log('PASS ROI, leverage and currency boundaries');
