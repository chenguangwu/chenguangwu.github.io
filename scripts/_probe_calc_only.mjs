import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs'; import path from 'path';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const list = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const anyStub = () => new Proxy({}, { get(t, k) { if (k === 'then') return undefined; return () => ({}); }, set() { return true; } });
for (const rel of list) {
  const raw = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const dom = new JSDOM(raw, { runScripts: 'dangerously', url: 'https://x.test/' + rel, pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = { copyText() {}, showToast() {}, formatNumber: n => String(n), escHtml: s => String(s ?? ''), esc: s => String(s ?? ''),
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid() {}, clearInvalid() {}, createTable: (h, r) => '<table>' + h + r + '</table>', debounce: f => f, $: id => w.document.getElementById(id) };
      w.i18nText = k => String(k ?? '');
      const ctx = new Proxy({}, { get(t, k) { if (k === 'measureText') return () => ({ width: 10 }); if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} }); if (k === 'canvas') return { width: 600, height: 300 }; return () => {}; }, set() { return true; } });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctx; } catch (e) {}
      w.TBKit = { util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} }, matrix: anyStub(), chart: anyStub(), preset: anyStub() };
    } });
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); setTimeout(r, 1200); });
  for (const el of [...w.document.querySelectorAll('input,select,textarea')]) {
    if (el.tagName === 'SELECT') { el.selectedIndex = -1; el.value = ''; } else if (el.type === 'checkbox' || el.type === 'radio') { el.checked = false; } else el.value = '';
    el.dispatchEvent(new w.Event('input', { bubbles: true })); el.dispatchEvent(new w.Event('change', { bubbles: true }));
  }
  const fn = ['calc', 'calculate', 'compute', 'calcTool', 'run', 'calcDueDate', 'calc12', 'calc1', 'calcError', 'calcConvert', 'calcModulus', 'lookup', 'analyze', 'calcPCM', 'calculate'].map(n => (typeof w[n] === 'function' ? n : null)).filter(Boolean)[0];
  try { if (fn) w[fn](); } catch (e) {}
  const boxes = [...w.document.querySelectorAll('[id]')].filter(el => /result|res$|^res|output|answer|summary/i.test(el.id) && !['INPUT','SELECT','TEXTAREA'].includes(el.tagName));
  const t = boxes.map(b => (b.textContent || '').replace(/\s+/g, ' ').trim()).filter(Boolean).join('|');
  console.log(rel + ' [' + (fn || 'none') + '] ' + t.slice(0, 100));
}
