// 全空态探针：把所有文本/数字输入清空后跑一次，检查结果区是否仍给出数字/结论。
// 判据（命中即候选缺陷）：结果容器文本含 ≥3 位数字或包含「推荐/建议/等级/合规/超期/达标」等结论词。
// 用法：node scripts/_probe_empty_state.mjs --list=文件 [--json=out]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const listArg = argv.find((a) => a.startsWith('--list='));
const jsonArg = argv.find((a) => a.startsWith('--json='));

const anyStub = () => new Proxy({}, { get(t, k) { if (k === 'then') return undefined; return () => ({}); }, set() { return true; } });

function build(raw, url) {
  return new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = { copyText() {}, showToast() {}, formatNumber: (n) => String(n), escHtml: (s) => String(s ?? ''), esc: (s) => String(s ?? ''),
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid() {}, clearInvalid() {}, createTable: (h, r) => '<table>' + h + r + '</table>',
        debounce: (f) => function (...a) { return f.apply(this, a); }, $: (id) => w.document.getElementById(id) };
      w.i18nText = (k) => String(k ?? '');
      const ctx = new Proxy({}, { get(t, k) { if (k === 'measureText') return () => ({ width: 10 }); if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} }); if (k === 'canvas') return { width: 600, height: 300 }; return () => {}; }, set() { return true; } });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctx; } catch (e) {}
      w.TBKit = { util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} },
        matrix: anyStub(), chart: anyStub(), preset: anyStub() };
    },
  });
}

const TEXTY = ['text', 'number', 'search', 'url', 'email', 'password', 'tel'];
const VERDICT = /推荐|建议|等级|合规|超期|未到期|达标|不合格|通过|风险|评分|结论/;
const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim();

const list = fs.readFileSync(listArg.slice(7), 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const out = [];
for (const rel of list) {
  const raw = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  let dom;
  try { dom = build(raw, 'https://x.test/' + rel); } catch (e) { continue; }
  const w = dom.window;
  await new Promise((r) => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); setTimeout(r, 1200); });
  const inputs = [...w.document.querySelectorAll('input')].filter((e) => TEXTY.includes(String(e.type || 'text').toLowerCase()));
  if (!inputs.length) continue;
  for (const el of inputs) { el.value = ''; el.dispatchEvent(new w.Event('input', { bubbles: true })); el.dispatchEvent(new w.Event('change', { bubbles: true })); }
  const NAMES = [...new Set((raw.match(/on(?:input|change|keyup|click)="([A-Za-z_$][\w$]*)\(/g) || []).map((s) => s.match(/"([A-Za-z_$][\w$]*)\(/)[1]).concat(['calc', 'calculate', 'calcTool', 'compute', 'update', 'generate', 'render', 'run']))];
  for (const n of NAMES) { try { if (typeof w[n] === 'function') w[n](); } catch (e) {} }
  const boxes = [...w.document.querySelectorAll('[id]')].filter((el) => /result|res|output|out|answer|score|total|detail|summary/i.test(el.id) && el.tagName !== 'INPUT' && el.tagName !== 'SELECT');
  let best = '', bestScore = 0;
  for (const b of boxes) {
    const t = norm(b.textContent);
    const digits = (t.match(/\d/g) || []).length;
    const score = digits + (VERDICT.test(t) ? 2 : 0);
    if (score > bestScore) { bestScore = score; best = b.id + ' :: ' + t.slice(0, 90); }
  }
  const digits = (best.split('::')[1] || '').match(/\d/g) || [];
  if (digits.length >= 3 || VERDICT.test(best)) out.push({ f: rel, hit: best });
}
console.log('候选', out.length, '/', list.length);
for (const r of out) console.log(r.f + '  ' + r.hit);
if (jsonArg) fs.writeFileSync(jsonArg.slice(7), JSON.stringify(out, null, 1));
