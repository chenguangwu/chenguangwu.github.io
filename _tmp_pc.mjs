import fs from 'fs';
import { JSDOM, VirtualConsole } from 'jsdom';
const TK = fs.readFileSync('js/tool-kit.js', 'utf8');

function parsePresets(src) {
  const m = src.match(/TBKit\.preset\.bar\('[^']+',\s*(\[[\s\S]*?\])\s*,/);
  if (!m) return null;
  try { return eval('(' + m[1] + ')'); } catch (e) { return null; }
}

let totalBtn = 0, totalBad = 0, absentTotal = 0;
for (const f of process.argv.slice(2)) {
  const html = fs.readFileSync(f, 'utf8');
  const presets = parsePresets(html);
  if (!presets) { console.log('?? 解析失败', f); continue; }
  const vc = new VirtualConsole(); const errs = [];
  vc.on('jsdomError', e => errs.push(String(e.message || e).slice(0, 110)));
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://e.com/', virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = { setResult(id, h) { const el = w.document.getElementById(id); if (el) el.innerHTML = h; }, toggleToolTheme() {}, formatNumber(x) { return String(x); }, initToolTheme() {} };
      try { w.eval(TK); } catch (e) { errs.push('TBK:' + e.message); }
    }
  });
  await new Promise(r => setTimeout(r, 400));
  const d = dom.window.document;
  const boxes = [...d.querySelectorAll('[id$="Presets"],[id$="presets"]')];
  const box = boxes.find(b => b.querySelector('button')) || boxes[0] || null;
  const btns = box ? [...box.querySelectorAll('button')] : [];
  let pageBad = 0, pageBtn = 0;
  const nonDefault = presets.filter(p => !/默认/.test(p.label || ''));
  const btnList = btns.slice(1); // 第 0 个按钮是「默认参数」，其余按 presets 顺序对应
  for (let i = 0; i < nonDefault.length; i++) {
    const p = nonDefault[i];
    const label = p.label || '';
    const btn = btnList[i];
    if (!btn) { console.log('  [缺按钮]', f, label); pageBad++; continue; }
    btn.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
    await new Promise(r => setTimeout(r, 120));
    const miss = []; let absent = 0;
    for (const [k, v] of Object.entries(p.values || {})) {
      const el = d.getElementById(k);
      if (!el) { absent++; continue; }
      if (el.type === 'checkbox' || el.type === 'radio') {
        const wantOn = !!v && v !== '0' && v !== 'false';
        if (el.checked !== wantOn) miss.push(k + ': 勾选期望' + wantOn + ' 实为' + el.checked);
      } else {
        const actual = el.value;
        if (String(actual) !== String(v)) miss.push(k + ': 期望' + JSON.stringify(v) + ' 实为' + JSON.stringify(actual));
      }
    }
    absentTotal += absent;
    pageBtn++; totalBtn++;
    if (miss.length) { pageBad++; totalBad++; console.log('  [不符]', f, label, '->', miss.slice(0, 4).join('; ')); }
  }
  const tag = pageBad ? 'FAIL' : 'OK';
  console.log(tag + ' ' + f + ' 场景' + pageBtn + (pageBad ? ' 失败' + pageBad : ''));
}
console.log('\n合计按钮 ' + totalBtn + '，失败项 ' + totalBad + '，跨模式缺元素键 ' + absentTotal + '（多模式页正常）');
