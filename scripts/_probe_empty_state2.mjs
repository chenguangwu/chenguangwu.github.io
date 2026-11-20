// 空态探针 v2：对比「默认态结果」与「全清空结果」。
// 仅当两者不同、且清空后结果仍含数字或结论词、且不含提示语时才算候选（排除静态参考表与已有提示）。
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
const PROMPT = /请(输入|填写|选择|检查|为)|⚠|须|需填写|必填|未填写|无法计算|不计算/;
const VERDICT = /推荐|建议|等级|合规|超期|未到期|达标|不合格|风险|评分|结论|偏高|偏低|良好|优良|适宜/;

const list = fs.readFileSync(listArg.slice(7), 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const out = [];
for (const rel of list) {
  const raw = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  let dom;
  try { dom = build(raw, 'https://x.test/' + rel); } catch (e) { continue; }
  const w = dom.window;
  await new Promise((r) => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); setTimeout(r, 1200); });
  const names = [...new Set((raw.match(/on(?:input|change|keyup|click)="([A-Za-z_$][\w$]*)\(/g) || []).map((s) => s.match(/"([A-Za-z_$][\w$]*)\(/)[1]).concat(['calc', 'calculate', 'calcTool', 'compute', 'update', 'generate', 'render', 'run']))];
  const run = () => { for (const n of names) { try { if (typeof w[n] === 'function') w[n](); } catch (e) {} } };
  const boxes = () => [...w.document.querySelectorAll('[id]')].filter((el) => /result|res$|^res|output|answer|score|summary/i.test(el.id) && el.tagName !== 'INPUT' && el.tagName !== 'SELECT');
  const snap = () => { const parts = []; for (const b of boxes()) parts.push((b.textContent || '').replace(/\s+/g, ' ').trim()); return parts.join('|'); };
  run(); const T1 = snap();
  const inputs = [...w.document.querySelectorAll('input')].filter((e) => TEXTY.includes(String(e.type || 'text').toLowerCase()));
  if (!inputs.length) continue;
  for (const el of inputs) { el.value = ''; el.dispatchEvent(new w.Event('input', { bubbles: true })); el.dispatchEvent(new w.Event('change', { bubbles: true })); }
  run(); const T2 = snap();
  if (!T1 || T1 === T2) continue;                 // 静态/与输入无关
  if (PROMPT.test(T2)) continue;                  // 已给提示
  const digits = (T2.match(/\d/g) || []).length;
  if (digits < 3 && !VERDICT.test(T2)) continue;
  out.push({ f: rel, t2: T2.slice(0, 110) });
}
console.log('候选 ' + out.length + ' / ' + list.length);
for (const r of out) console.log(r.f + '  ' + r.t2);
if (jsonArg) fs.writeFileSync(jsonArg.slice(7), JSON.stringify(out, null, 1));
