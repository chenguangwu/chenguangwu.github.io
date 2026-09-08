/**
 * 用轻量 DOM mock 在 Node 中执行工具页脚本，取回默认输入下的真实输出。
 *
 * 目的：为工具编写「深度解析」示例时，示例数字必须与工具实际输出一致，
 * 避免用编造算例误导用户（DEV-PLAN 第 4/9 条验收标准）。
 *
 * 用法：
 *   python3 scripts/tool_calc_probe.py <industry>   # 先生成 harness
 *   node scripts/tool_calc_run.js <industry>        # 再跑结果
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const industry = process.argv[2] || 'fire-rescue';
const harnessPath = path.join('/tmp', 'tool_calc_harness', `${industry}.json`);
if (!fs.existsSync(harnessPath)) {
  console.error('找不到 harness，请先运行: python3 scripts/tool_calc_probe.py ' + industry);
  process.exit(1);
}
const harness = JSON.parse(fs.readFileSync(harnessPath, 'utf-8'));

function makeEl(id, value) {
  const el = {
    id,
    value: value === undefined ? '' : String(value),
    innerHTML: '',
    textContent: '',
    innerText: '',
    checked: false,
    style: {},
    dataset: {},
    options: [],
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {},
    removeEventListener() {},
    appendChild() {},
    querySelector() { return null; },
    querySelectorAll() { return []; },
    focus() {},
    setAttribute() {},
    getAttribute() { return null; },
    closest() { return null; },
    remove() {},
  };
  return el;
}

function runOne(slug, cfg) {
  const els = {};
  for (const [k, v] of Object.entries(cfg.values || {})) els[k] = makeEl(k, v);
  // select 需要 options / selectedIndex，否则读 sel.options[sel.selectedIndex].value 会崩
  for (const [k, o] of Object.entries(cfg.options || {})) {
    if (!els[k]) continue;
    els[k].options = (o.values || []).map((v) => ({ value: v, text: v }));
    els[k].selectedIndex = o.selectedIndex || 0;
    Object.defineProperty(els[k], 'value', {
      get() {
        const i = this.selectedIndex >= 0 ? this.selectedIndex : 0;
        return this.options[i] ? this.options[i].value : '';
      },
      set(v) {
        const i = this.options.findIndex((x) => String(x.value) === String(v));
        if (i >= 0) this.selectedIndex = i;
      },
      configurable: true,
    });
  }

  const document = {
    getElementById(id) {
      if (!els[id]) els[id] = makeEl(id, '');
      return els[id];
    },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    createElement() { return makeEl('tmp', ''); },
    addEventListener() {},
    body: makeEl('body', ''),
    head: makeEl('head', ''),
  };

  const store = {};
  const localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
  };

  const fmt = (n, d) => {
    if (n === null || n === undefined || Number.isNaN(n)) return '-';
    const p = d === undefined ? 2 : d;
    return Number(n).toFixed(p).replace(/\.00$/, '');
  };

  const ToolBox = {
    $: (id) => document.getElementById(id),
    formatNumber: fmt,
    fmt,
    copyText() {},
    showToast() {},
    toast() {},
    toggleToolTheme() {},
    debounce: (fn) => fn,
    escapeHtml: (s) => String(s),
  };

  const sandbox = {
    document,
    localStorage,
    location: { pathname: `/tools/${cfg.industry}/${slug}.html`, href: 'https://chenguangwu.github.io/' },
    navigator: { userAgent: 'node', language: 'zh-CN' },
    window: {},
    ToolBox,
    i18nText: (k, fb) => fb || k || '',
    t: (k, fb) => fb || k || '',
    console,
    Math,
    JSON,
    parseFloat,
    parseInt,
    isNaN,
    Number,
    String,
    Array,
    Object,
    Date,
    setTimeout: () => 0,
    clearTimeout: () => {},
    setInterval: () => 0,
    alert() {},
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }),
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);

  for (const code of cfg.scripts || []) {
    try {
      vm.runInContext(code, sandbox, { timeout: 3000 });
    } catch (e) {
      return { slug, ok: false, error: 'script: ' + e.message };
    }
  }

  const entry = cfg.entry || 'calc';
  if (typeof sandbox[entry] !== 'function') {
    return { slug, ok: false, error: 'no entry fn: ' + entry };
  }
  try {
    sandbox[entry]();
  } catch (e) {
    return { slug, ok: false, error: 'run: ' + e.message };
  }

  const res = els[cfg.res_id];
  let text = res ? String(res.innerHTML || '') : '';
  text = text
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/(p|div|li|tr|h\d)>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n\s*\n+/g, '\n')
    .trim();
  return { slug, ok: Boolean(text), text };
}

const results = {};
for (const [slug, cfg] of Object.entries(harness)) {
  results[slug] = runOne(slug, cfg);
}
const outPath = path.join('/tmp', 'tool_calc_harness', `${industry}.out.json`);
fs.writeFileSync(outPath, JSON.stringify(results, null, 1), 'utf-8');

let ok = 0;
for (const [slug, r] of Object.entries(results)) {
  if (r.ok) ok++;
  console.log('='.repeat(70));
  console.log('## ' + slug + (r.ok ? '' : '  [FAIL ' + r.error + ']'));
  if (r.ok) console.log(r.text.slice(0, 900));
}
console.log(`\n成功 ${ok}/${Object.keys(results).length}，结果已写入 ${outPath}`);
