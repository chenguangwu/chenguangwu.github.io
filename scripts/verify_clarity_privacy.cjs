// Regression tests for the shared Clarity integration; network privacy is verified separately.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const source = fs.readFileSync(path.join(__dirname, '../js/analytics.js'), 'utf8');

function boot(options = {}) {
  const scripts = [];
  const attrs = {};
  const root = { setAttribute(key, value) { if (options.maskFailure) throw Error('mask failed'); attrs[key] = value; } };
  const document = {
    documentElement: root,
    head: { appendChild(script) { scripts.push({ ...script, mask: attrs['data-clarity-mask'] }); } },
    getElementById(id) { return scripts.find(s => s.id === id); },
    createElement() { return {}; },
  };
  const window = {};
  const context = vm.createContext({ window, document });
  vm.runInContext(source, context);
  return { window, scripts, context };
}

const checks = [
  ['Clarity SDK loads only after full-page masking', () => {
    const { scripts } = boot();
    const sdk = scripts.find(s => s.id === 'tb-clarity-sdk');
    assert(sdk, 'Clarity SDK is missing');
    assert.strictEqual(sdk.mask, 'true');
    assert.match(sdk.src, /^https:\/\/www\.clarity\.ms\/tag\/y48102uvzx(?:\?|$)/);
  }],
  ['initialization is idempotent', () => {
    const { scripts, context } = boot();
    vm.runInContext(source, context);
    assert.strictEqual(scripts.filter(s => s.id === 'tb-clarity-sdk').length, 1);
  }],
  ['arbitrary event names and parameters are not sent to Clarity', () => {
    const { window } = boot();
    const calls = [];
    window.clarity = (...args) => calls.push(args);
    window.ToolBox.Analytics.track('SECRET_EVENT', { label: 'SECRET_LABEL', key: 'SECRET_VALUE' }, 'SECRET_ID');
    assert.deepStrictEqual(calls, []);
  }],
  ['mask failure prevents SDK load and leaves other analytics available', () => {
    const { scripts, window } = boot({ maskFailure: true });
    assert(!scripts.some(s => s.id === 'tb-clarity-sdk'));
    assert(scripts.some(s => s.id === 'tb-baidu-statistics'));
    assert.strictEqual(typeof window.ToolBox.Analytics.track, 'function');
  }],
];
let failures = 0;
for (const [name, fn] of checks) {
  try { fn(); console.log('PASS ' + name); }
  catch (error) { failures++; console.error('FAIL ' + name + ': ' + error.message); }
}
process.exitCode = failures ? 1 : 0;
