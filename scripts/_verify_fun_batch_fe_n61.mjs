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
        last: () => null,
        list: () => [],
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
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] N61 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] N61 锁 PASS`);
