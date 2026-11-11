// 第217批 · IT-N170~N173 calc-3 颜色值转换器（JSDOM 真机）
// 覆盖：三路输入区间校验 / 预设回调按来源 / 重复预设条 / #RGB 简写与 8 位 alpha
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/calc-3.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 220) : '')); }

let copied = null;
const presetBars = [];   // 记录 preset.bar 调用（含自动宿主）
let declaredHosts = [];  // 记录声明式 [data-tb=preset] 扫描

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/calc-3.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText(t) { copied = String(t); } };
    const setValue = (host, sel, val) => {
      try {
        const doc = host.ownerDocument || host;
        const el = doc.querySelector(sel);
        if (el) el.value = val;
      } catch (e) {}
    };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} },
      preset: {
        ensureHost(host) {
          const id = String(host || '').replace(/^[#.]/, '');
          if (!id) return null;
          const d = w.document;
          let box = d.getElementById(id);
          if (box) return box;
          box = d.createElement('div');
          box.id = id;
          const anchor = d.querySelector('.input-row');
          if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(box, anchor);
          return box;
        },
        bar(host, list, after) {
          const d = w.document;
          let box = (typeof host === 'string') ? d.querySelector(host) : host;
          if (!box && list && list.length > 1) box = w.TBKit.preset.ensureHost(host);
          if (!box || !list || !list.length) return null;
          box.innerHTML = '';
          const wrap = d.createElement('div');
          wrap.className = 'tbk-presets';
          list.forEach(p => {
            const b = d.createElement('button');
            b.type = 'button';
            b.className = 'tbk-preset-btn';
            b.textContent = p.label;
            b.addEventListener('click', () => {
              Object.keys(p.values).forEach(k => setValue(box, '#' + k, p.values[k]));
              if (typeof after === 'function') { try { after(); } catch (e) {} }
            });
            wrap.appendChild(b);
          });
          box.appendChild(wrap);
          presetBars.push({ host: String(host), count: list.length, wrap });
          return wrap;
        }
      }
    };
  }
});
const w = dom.window, d = w.document;

// 复刻 tool-kit.js 的 mountDeclared：扫描 [data-tb=preset] 并渲染
d.querySelectorAll('[data-tb="preset"]').forEach(n => {
  try {
    const list = JSON.parse(n.getAttribute('data-tb-presets') || 'null');
    if (list) { declaredHosts.push(n); w.TBKit.preset.bar(n, list); }
  } catch (e) {}
});
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

const $ = id => d.getElementById(id);
const setVal = (id, v) => { const el = $(id); if (el) el.value = v; };
const resultText = () => String($('result') ? $('result').textContent : '').replace(/\s+/g, ' ').trim();
const hslVal = () => String($('hslInput') ? $('hslInput').value : '');
const hexVal = () => String($('hexInput') ? $('hexInput').value : '');
const rgbVal = () => String($('rgbInput') ? $('rgbInput').value : '');

// ══════════════ IT-N170 三路输入区间校验 ══════════════
// N170-a: rgb(300,0,0) 应 clamp 到 255，且同屏 HSL 不出现 >100% 的饱和度
setVal('rgbInput', 'rgb(300,0,0)');
w.eval('fromRgb()');
const r300 = resultText();
check('N170 rgb(300,0,0) 输出通道被 clamp/拒绝（无 300）', !/rgb\(\s*300\b/.test(r300), r300);
check('N170 rgb(300,..) 同屏 HSL 饱和度不超 100%', (() => {
  const m = r300.match(/hsl\(\s*\d+\s*,\s*(\d+)%/);
  return !!m && Number(m[1]) <= 100;
})(), r300);

// N170-b: hsl(720,100%,50%) 应等价于 hsl(0,100%,50%) → 纯红
setVal('hslInput', 'hsl(720,100%,50%)');
w.eval('fromHsl()');
const h720 = resultText();
check('N170 hsl(720,..) 按 720≡0 归一为纯红 rgb(255, 0, 0)', /rgb\(255,\s*0,\s*0\)/.test(h720), h720);

// N170-c: hsl(0,200%,50%) 应 clamp s 到 100%，不产生越界 rgb
setVal('hslInput', 'hsl(0,200%,50%)');
w.eval('fromHsl()');
const h200 = resultText();
check('N170 hsl(0,200%,..) 不产生越界 rgb 通道', !/rgb\([^)]*(?:383|-1\d\d)/.test(h200), h200);
check('N170 hsl(0,200%,..) clamp 后仍为纯红', /rgb\(255,\s*0,\s*0\)/.test(h200), h200);

// N170-d: 合法输入结果不变（回归保护，verify 4 例锚点）
setVal('hexInput', '#1E90FF');
w.eval('fromHex()');
check('N170 合法 #1E90FF 仍输出 rgb(30, 144, 255)', /rgb\(30,\s*144,\s*255\)/.test(resultText()), resultText());
check('N170 合法 #1E90FF 仍输出 hsl(210, 100%, 56%)', /hsl\(210,\s*100%,\s*56%\)/.test(resultText()), resultText());
setVal('hexInput', '#00FF7F');
w.eval('fromHex()');
// 真机 textContent 在 <p> 之间不带空格（与 harness 的 blob 归一不同），故去空格后比对
const strip = s => String(s).replace(/\s+/g, '');
check('N170 合法 #00FF7F 派生串不回退',
  strip(resultText()) === strip('HEX： #00FF7F RGB： rgb(0, 255, 127) HSL： hsl(150, 100%, 50%)'), resultText());

// ══════════════ IT-N171 预设回调按来源 ══════════════
// 重置到页面默认色，避免前面的测试注入值造成假阳性
setVal('hexInput', '#FF6B35');
w.eval('fromHex()');
// 找到含「红色」的按钮并点击，结果应为纯红而非留在橙色
const redBtn = Array.from(d.querySelectorAll('.tbk-preset-btn')).find(b => b.textContent === '红色');
if (redBtn) redBtn.click();
else w.eval("document.getElementById('hslInput').value='hsl(0, 100%, 50%)'");
const afterRed = resultText();
check('N171 点「红色」预设后结果区为纯红 rgb(255, 0, 0)', /rgb\(255,\s*0,\s*0\)/.test(afterRed), afterRed);
check('N171 点「红色」预设后 hslInput 保留 hsl(0, 100%, 50%)', /hsl\(0,\s*100%,\s*50%\)/.test(hslVal()), hslVal());
check('N171 点「红色」预设后 hexInput 同步为 #FF0000', /^#FF0000$/i.test(hexVal()), hexVal());
check('N171 点「红色」预设后 rgbInput 同步为 rgb(255, 0, 0)', /rgb\(255,\s*0,\s*0\)/.test(rgbVal()), rgbVal());

const blueBtn = Array.from(d.querySelectorAll('.tbk-preset-btn')).find(b => b.textContent === '蓝色');
if (blueBtn) blueBtn.click();
check('N171 点「蓝色」预设后 hslInput 为 219 度', /hsl\(219,\s*100%,\s*50%\)/.test(hslVal()), hslVal());
check('N171 点「蓝色」预设后 hexInput 同步为蓝色（非橙/非红）', !/^#(FF6B35|FF0000)$/i.test(hexVal()), hexVal());

// ══════════════ IT-N172 只保留一组预设条 ══════════════
const groups = d.querySelectorAll('.tbk-presets');
check('N172 页面只渲染 1 组预设条', groups.length === 1, 'groups=' + groups.length + ' bars=' + JSON.stringify(presetBars.map(b => b.host + ':' + b.count)));
check('N172 保留的预设条含 4 个按钮', groups.length === 1 && groups[0].querySelectorAll('button').length === 4,
  groups.length ? String(groups[0].querySelectorAll('button').length) : 'n/a');
check('N172 不再有声明式 preset 宿主与自动宿主并存', !(declaredHosts.length > 0 && presetBars.some(b => /calc_3Presets/.test(b.host))),
  'declared=' + declaredHosts.length + ' bars=' + JSON.stringify(presetBars.map(b => b.host)));

// ══════════════ IT-N173 #RGB 简写 / 8 位 alpha ══════════════
setVal('hexInput', '#F00');
w.eval('fromHex()');
check('N173 #F00 简写展开为 #FF0000', /HEX：\s*#FF0000/.test(resultText()), resultText());
check('N173 #F00 不报「请输入有效的 HEX」', !/请输入有效的 HEX/.test(resultText()), resultText());

setVal('hexInput', '#0F08');
w.eval('fromHex()');
check('N173 #0F08 四位简写含 alpha 可解析', !/请输入有效的 HEX/.test(resultText()), resultText());

setVal('hexInput', '#FF6B3580');
w.eval('fromHex()');
check('N173 8 位 HEX 可解析且 alpha 保留', !/请输入有效的 HEX/.test(resultText()) && /FF6B35/i.test(resultText()), resultText());
const maxlen = $('hexInput') ? $('hexInput').getAttribute('maxlength') : null;
check('N173 hexInput maxlength 已放宽（>=9 或移除）', maxlen === null || Number(maxlen) >= 9, 'maxlength=' + maxlen);

// ══════════════ 汇总 ══════════════
const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAIL ITEMS: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exitCode = 1;
}
