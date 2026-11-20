import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs'; import path from 'path';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const list = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const anyStub = () => new Proxy({}, { get(t, k) { if (k === 'then') return undefined; return () => ({}); }, set() { return true; } });
const ERR = /请输入|无效|不能为空|错误|NaN|Infinity|undefined|超出范围|请选择|请填写|不合法/;
for (const rel of list) {
  const raw = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const errs = [];
  const dom = new JSDOM(raw, { runScripts: 'dangerously', url: 'https://x.test/' + rel, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole().on('jsdomError', e => errs.push(String(e && e.message).slice(0, 80))),
    beforeParse(w) {
      w.ToolBox = { copyText() {}, showToast() {}, formatNumber: n => String(n), escHtml: s => String(s ?? ''), esc: s => String(s ?? ''),
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid() {}, clearInvalid() {}, createTable: (h, r) => '<table>' + h + r + '</table>', debounce: f => f, $: id => w.document.getElementById(id) };
      w.i18nText = k => String(k ?? '');
      const ctx = new Proxy({}, { get(t, k) { if (k === 'measureText') return () => ({ width: 10 }); if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} }); if (k === 'canvas') return { width: 600, height: 300 }; return () => {}; }, set() { return true; } });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctx; } catch (e) {}
      w.__presets = [];
      function setValue(id, val) {
        const f = w.document.getElementById(id); if (!f) return false;
        if (f.tagName === 'SELECT' || f.tagName === 'TEXTAREA' || f.tagName === 'INPUT') {
          if (f.type === 'checkbox' || f.type === 'radio') {
            const off = val === false || val === 0 || val === '0' || val === 'false' || val === 'off' || val === '' || val == null;
            f.checked = !off;
          } else f.value = val;
          f.dispatchEvent(new w.Event(f.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true }));
          f.dispatchEvent(new w.Event('change', { bubbles: true }));
          return true;
        }
        return false;
      }
      w.TBKit = { util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} },
        matrix: anyStub(), chart: anyStub(),
        preset: { bar(host, list2, after) {
          const id = String(host || '').replace(/^[#.]/, '');
          let box = w.document.getElementById(id);
          if (!box) { box = w.document.createElement('div'); box.id = id; w.document.body.appendChild(box); }
          box.innerHTML = '';
          list2.forEach(p => {
            const b = w.document.createElement('button');
            b.type = 'button'; b.className = 'tbk-preset-btn'; b.textContent = p.label || '';
            b.__p = p; b.addEventListener('click', () => {
              const miss = [];
              for (const k in (p.values || {})) { if (!setValue(k, p.values[k])) miss.push(k); }
              if (after) { try { after(); } catch (e) { errs.push('after:' + String(e.message).slice(0, 60)); } }
              b.__miss = miss;
            });
            box.appendChild(b); w.__presets.push(b);
          });
          return box;
        } } };
    } });
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); setTimeout(r, 1200); });
  try { w.eval('if(typeof __builtRows!=="undefined"){}'); } catch (e) {}
  const snap = () => {
    const boxes = [...w.document.querySelectorAll('[id]')].filter(el => /result|res$|^res|output|answer|summary|score|out$/i.test(el.id) && !['INPUT','SELECT','TEXTAREA'].includes(el.tagName));
    return boxes.map(x => (x.textContent || '').replace(/\s+/g, ' ').trim()).filter(Boolean).join('|');
  };
  const base = snap();
  const rows = [];
  const btns = w.__presets || [];
  for (const b of btns) {
    b.click();
    await new Promise(r => setTimeout(r, 60));
    const t = snap();
    rows.push({ preset: b.textContent, miss: b.__miss || [], text: t.slice(0, 220), same: t === base, bad: /undefined|NaN|Infinity/.test(t), err: !!ERR.test(t) });
  }
  const bad = rows.filter(r => r.bad || (r.same && !/默认参数|Default/.test(r.preset)));
  if (bad.length) {
    console.log('== ' + rel + '  presets=' + rows.length + ' bad=' + bad.length + (errs.length ? ' err=' + JSON.stringify(errs.slice(0, 2)) : ''));
    for (const r of bad.slice(0, 4)) console.log('   [' + r.preset + ']' + (r.same ? ' NOEFFECT' : '') + (r.bad ? ' UNDEF' : '') + ' miss=' + (r.miss.join(',') || '-') + ' text=' + r.text.slice(0, 120));
  }
}
