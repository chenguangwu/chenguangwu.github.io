// 验证紧急开关文件、构建版本戳以及 Service Worker 实际激活行为。
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const { spawnSync } = require('child_process');
const root = path.resolve(__dirname, '..');
let failures = 0;
async function check(name, fn) {
  try { await fn(); console.log('PASS ' + name); }
  catch (e) { failures++; console.error('FAIL ' + name + ': ' + e.message); }
}

async function activation(mode) {
  const handlers = {}, deleted = [], requests = [];
  let unregistered = false, claimed = false, responded = false;
  const caches = {
    keys: async () => ['tb-old', 'other-app'],
    delete: async key => { deleted.push(key); return true; },
    match: async () => new Response('cached', { status: 200 }),
  };
  const self = {
    location: { origin: 'https://example.test' },
    addEventListener: (type, fn) => { handlers[type] = fn; },
    registration: { unregister: async () => { unregistered = true; } },
    clients: { claim: async () => { claimed = true; } },
  };
  const fetch = async (url, opts) => {
    requests.push([url, opts]);
    if (mode === 'network') throw new Error('network');
    if (mode === '404') return { ok: false };
    if (mode === 'invalid') return { ok: true, json: async () => { throw new Error('invalid JSON'); } };
    return { ok: true, json: async () => ({ disabled: mode === 'true' ? true : mode === 'string' ? 'true' : false }) };
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'sw.js'), 'utf8'), { self, caches, fetch, URL, Request, Response, setTimeout, clearTimeout });
  let pending;
  handlers.activate({ waitUntil: p => { pending = p; } });
  await pending;
  handlers.fetch({ request: new Request('https://example.test/test.png'), respondWith: () => { responded = true; } });
  return { deleted, unregistered, claimed, responded, requests };
}

(async () => {
  await check('发布开关存在且 disabled 为布尔值', () => {
    const data = JSON.parse(fs.readFileSync(path.join(root, 'sw-kill.json'), 'utf8'));
    assert.strictEqual(typeof data.disabled, 'boolean');
  });
  await check('开关变化改变构建版本，内容不变保持稳定', () => {
    const python = `import ast, hashlib, os, tempfile\nfrom pathlib import Path\nsrc = Path('_build.py').read_text(encoding='utf8')\ntree = ast.parse(src)\nfn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_sw_build')\nwith tempfile.TemporaryDirectory() as d:\n    ns = {'os': os, 'hashlib': hashlib, 'ROOT': d}\n    exec(compile(ast.Module(body=[fn], type_ignores=[]), '_build.py', 'exec'), ns)\n    p = Path(d) / 'sw-kill.json'\n    p.write_text('{"disabled":false}', encoding='utf8')\n    first = ns['compute_sw_build']()\n    assert first == ns['compute_sw_build'](), 'unchanged content changed build'\n    p.write_text('{"disabled":true}', encoding='utf8')\n    assert first != ns['compute_sw_build'](), 'switch change did not change build'\n`;
    const result = spawnSync('python3', ['-c', python], { cwd: root, encoding: 'utf8' });
    assert.strictEqual(result.status, 0, result.stderr);
  });
  for (const mode of ['false', 'true', '404', 'invalid', 'network', 'string']) {
    await check('激活开关 ' + mode, async () => {
      const out = await activation(mode);
      assert.strictEqual(out.claimed, true);
      assert.match(out.requests[0][0], /^\/sw-kill\.json\?_swv=[a-f0-9]+$/);
      assert.strictEqual(out.requests[0][1].cache, 'no-store');
      assert.strictEqual(out.unregistered, mode === 'true');
      assert.strictEqual(out.responded, mode !== 'true');
      assert.strictEqual(out.deleted.includes('other-app'), mode === 'true');
    });
  }
  process.exitCode = failures ? 1 : 0;
})();
