// 两态锁：FE-N61（keyboard-heatmap 真实打字也要写入历史；示例累加须显式提示）
// 用法：node scripts/_verify_fun_batch_fe_n61.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const file = 'tools/fun/keyboard-heatmap.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const recorded = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.TBKit = {
      util: { isEn: () => false, diffBox() {}, exportTable() {} },
      history: {
        record(rec) { recorded.push(rec); },
        last: () => recorded.at(-1) || null,
        list: () => recorded.slice().reverse().map(d => ({ t: Date.now(), d })),
        mount() {}
      },
      matrix: { table() {} },
      chart: { line() {} },
      preset: { bar() {} }
    };
    w.ToolBox = { showToast() {}, downloadText() {}, showError() {} };
    w.i18nText = (k) => String(k);
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);

if (typeof w.onKey !== 'function') {
  console.log('  ✗ onKey 不可见，N61 锁无法判定');
  failures++;
} else {
  // —— 模拟真实打字：3 个字母键 ——
  const ta = w.document.getElementById('typeArea');
  ta.value = 'abc';
  w.onKey({ key: 'a', repeat: false });
  w.onKey({ key: 'b', repeat: false });
  w.onKey({ key: 'c', repeat: false });
  await sleep(900); // 越过 500ms 防抖 + 记录器 1s 节流的首个窗口
  assert(recorded.length >= 1,
    `真实打字后应写入历史记录（数据表/历史/趋势/导出才有内容）；实际记录数=${recorded.length}`);
  const hasTyped = recorded.some(r => String(r.typeArea || r['typeArea'] || '').indexOf('abc') >= 0);
  assert(hasTyped,
    `写入的记录应反映当前输入内容（typeArea=abc）；实际首条键=${JSON.stringify(Object.keys(recorded[0] || {}))}`);

  // 首次入库后在节流窗口内继续输入，停下后必须补写最后状态。
  ta.value = 'abcd';
  w.onKey({ key: 'd', repeat: false });
  await sleep(1100);
  assert(recorded.at(-1)?.typeArea === 'abcd', '节流窗口内输入后停止，历史必须保存最终状态');
  ta.value = 'abcde';
  w.onKey({ key: 'e', repeat: false });
  w.dispatchEvent(new w.Event('pagehide'));
  assert(recorded.at(-1)?.typeArea === 'abcde', '离开或刷新前必须立即补写待保存状态');
  ta.value = 'abcdef'; w.onKey({ key: 'f', repeat: false });
  const countBeforeReset = recorded.length;
  w.resetHeat(); await sleep(1100);
  assert(recorded.length === countBeforeReset, '清空后待写定时器不得重新写入旧历史');

  // —— 示例累加必须显式提示 ——
  const before = recorded.length;
  w.loadSample();
  await sleep(50);
  const resTxt = (w.document.getElementById('result').textContent || '').replace(/\s+/g, ' ').trim();
  assert(/累加/.test(resTxt),
    `点「载入示例文本」应显式提示「已累加到当前统计」；实际结果区=「${resTxt.slice(0, 80)}」`);
  const totalTxt = (w.document.getElementById('totalKeys').textContent || '').trim();
  assert(/^\d+$/.test(totalTxt) && Number(totalTxt) > 3,
    `示例应累加到总按键（保留原有累加语义）；实际总按键=${totalTxt}`);
  void before;
}

dom.window.close();

// 使用真实历史与表格实现验证复核原始时序、页面离开及重载后记录。
const makeReal = (saved = {}) => new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://example.test/tools/fun/keyboard-heatmap.html',
  beforeParse(w) {
    for (const [k, v] of Object.entries(saved)) w.localStorage.setItem(k, v);
    w.ToolBox = { showToast() {}, downloadText() {}, showError() {} };
    w.i18nText = k => String(k);
    w.eval(fs.readFileSync('js/tool-kit.js', 'utf8'));
  }
});
const real = makeReal(), rw = real.window;
await new Promise(r => { if (rw.document.readyState === 'complete') r(); else rw.addEventListener('load', r); });
const area = rw.document.getElementById('typeArea');
area.value = 'a'; rw.onKey({ key: 'a', repeat: false });
await sleep(620);
area.value = 'ab'; rw.onKey({ key: 'b', repeat: false });
await sleep(1300);
assert(rw.TBKit.history.last()?.typeArea === 'ab', '真实存储按原始复现时序保存最终 ab');
assert(rw.document.querySelector('#keyboard_heatmapTable')?.textContent.includes('ab'), '真实明细表显示最终 ab');
area.value = 'abc'; rw.onKey({ key: 'c', repeat: false });
rw.dispatchEvent(new rw.Event('pagehide'));
const saved = Object.fromEntries(Array.from({ length: rw.localStorage.length }, (_, i) => rw.localStorage.key(i)).map(k => [k, rw.localStorage.getItem(k)]));
real.window.close();
const reloaded = makeReal(saved);
await new Promise(r => { if (reloaded.window.document.readyState === 'complete') r(); else reloaded.window.addEventListener('load', r); });
assert(reloaded.window.TBKit.history.last()?.typeArea === 'abc', '刷新后真实本地历史保留离开前最终状态');
reloaded.window.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] N61 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] N61 锁 PASS`);
