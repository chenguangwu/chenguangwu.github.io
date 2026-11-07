// scripts/_verify_sports_batch_e.mjs — SF-N37/N38 睡袋 E 批运行期证据
//
// 门禁 harness 采集元素 innerHTML/textContent 时**剥掉标签**，参考表的「当前推荐行」高亮是
// `<tr style="background:var(--bg-active)…">` 内联样式 ⇒ blob 里完全看不见，无法用 expect 断言。
// 故 N38（首屏高亮错行）改由 JSDOM 运行期读 ref-table 的 HTML 直接比对「高亮行名 == 结果卡推荐名」。
// N37（普通型零余量）的文案与余量卡已由 verify_sports_calc.js blob 用例覆盖，本脚本再补一条运行期取值。
// 用法：node scripts/_verify_sports_batch_e.mjs [--head]（--head 读 HEAD 版做回退判别）
import { readFileSync } from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM, VirtualConsole } from 'jsdom';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HEAD = process.argv.includes('--head');
const read = (rel) => HEAD
  ? execFileSync('git', ['show', 'HEAD:' + rel], { cwd: ROOT, encoding: 'utf8', maxBuffer: 30e6 })
  : readFileSync(path.join(ROOT, rel), 'utf8');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}

async function loadPage(rel) {
  const html = read(rel);
  const vc = new VirtualConsole();
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://x.test/' + rel,
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => false, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop,
          setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      try { w.alert = noop; } catch (e) {}
    },
  });
  // JSDOM 的 DOMContentLoaded 是异步触发的：必须等它跑完，页面 DOMContentLoaded 里首次 calc() 的
  // 渲染结果（含 SF-N38 的首屏高亮）才会落盘，否则读到的 result/ref-table 还是空壳。
  await new Promise((r) => setTimeout(r, 150));
  return dom.window;
}

const REL = 'tools/sports/sleeping-bag-rating.html';

// SF-N38：默认态（环境 5℃ / 普通型）首屏「结果卡推荐」与「参考表高亮行」必须同名。
// HEAD 版 DOMContentLoaded 里固定 updateRefTable(1) 会覆盖 calc() 设的 recommendedIdx(0)：
// 结果卡「+10°C 夏季」、参考表高亮「+5°C 三季」⇒ 不一致。
{
  const w = await loadPage(REL);
  const doc = w.document;
  const resHTML = String(doc.getElementById('result').innerHTML || '');
  const rec = (resHTML.match(/<div class="val">([^<]+)<\/div><div class="lbl">推荐睡袋<\/div>/) || [])[1] || '';
  const refHTML = String(doc.getElementById('ref-table').innerHTML || '');
  const hlRow = (refHTML.match(/<tr style="background:var\(--bg-active\)[^"]*">([\s\S]*?)<\/tr>/) || [])[1] || '';
  const hl = (hlRow.match(/<strong>([^<]+)<\/strong>/) || [])[1] || '';
  check('SF-N38 首屏参考表高亮行 == 结果卡推荐睡袋', !!rec && rec === hl, '推荐=' + rec + ' 高亮=' + hl);
}

// SF-N37：普通型预留 3°C 余量 + 明示保温余量卡（运行期取值，blob 已覆盖文案，此处独立复算）
{
  const w = await loadPage(REL);
  const doc = w.document;
  doc.getElementById('temp-slider').value = '-2';
  doc.getElementById('temp-input').value = '-2';
  doc.getElementById('sleeper-type').value = 'normal';
  try { w.calc(); } catch (e) {}
  const resHTML = String(doc.getElementById('result').innerHTML || '');
  const target = (resHTML.match(/<div class="val">(-?\d+)°C<\/div><div class="lbl">目标下限温度/) || [])[1];
  const margin = (resHTML.match(/<div class="val">([+-]?\d+)°C<\/div><div class="lbl">保温余量/) || [])[1];
  check('SF-N37 普通型目标下限 = 环境−3（−2 ⇒ −5）', target === '-5', 'target=' + target);
  check('SF-N37 保温余量 = 环境 − 选中下限（−2 −(−5) = +3）', margin === '+3', 'margin=' + margin);
}

console.log('\n==== sports E 批运行期证据: ' + pass + '/' + (pass + fail) + ' ====');
process.exit(fail ? 1 : 0);
