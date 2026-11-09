// scripts/_verify_sports_batch_n.mjs — SF-N93/N94/N99 体育 N 批运行期证据
//
// 门禁 harness 只能断「依赖输入变化的输出串」，以下三项属于「页面结构 / 文案与代码口径一致性」，
// 用 expect 断言会退化成静态锚（默认态也命中 ⇒ 逃生项），故由本脚本直取 DOM 取证：
//   ① SF-N99 电解质：折算食盐口径必须写成「钠(mg) ÷ 393」，全页不得再出现「钠 ÷ 0.393」
//      （代码 A*B*23/393 本来就是对的，错的是三处文案，差 1000 倍）；
//   ② SF-N94 VO2max 估算法选项：原 3 个选项只有 2 套算法（method 1 与 2 完全同式），
//      选项数必须收敛为 2，且历史 method=2 仍能算出与 method=1 相同结果（向后兼容）；
//   ③ SF-N93 时间空串（不只是 0）：原 `+value||1` 兜底成 1 秒 ⇒ VO2max ≈ 28983.5 的荒谬值。
// 用法：node scripts/_verify_sports_batch_n.mjs [--head]（--head 读 HEAD 版做回退判别）
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
        history: { list: () => [], last: () => null, record: noop, mount: (_, cb) => { w.restoreHistory = cb; }, clear: noop },
        preset: { bar: noop }, chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      try { w.alert = noop; } catch (e) {}
    },
  });
  await new Promise((r) => setTimeout(r, 150));
  return dom.window;
}

// ── SF-N99：折算食盐口径（文案 393 vs 代码 /393）──
{
  const REL = 'tools/sports/dianjiezhi-diushi-buchong.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const src = read(REL);
  // 全页静态文本（含公式框 / info-box）不得再出现「钠 ÷ 0.393」这种差 1000 倍的口径
  const bad = /钠\s*÷\s*0\.393|食盐\s*[=≈]\s*钠\s*÷\s*0\.393/.test(src);
  check('SF-N99 页面不再出现「钠 ÷ 0.393」错误口径', !bad, 'still has 钠 ÷ 0.393');
  check('SF-N99 公式框写明「钠(mg) ÷ 393」', /折算食盐\s*=\s*钠\(mg\)\s*÷\s*393/.test(src));
  check('SF-N99 info-box 写明「折算食盐(g) = 钠(mg) ÷ 393」', /折算食盐\(g\) = 钠\(mg\) ÷ 393/.test(src));

  // 代码口径实算：2.0 L × 50 mmol/L × 23 = 2300 mg 钠 ⇒ 2300/393 = 5.85 g
  doc.getElementById('v0').value = '2.0';
  doc.getElementById('v1').value = '50';
  w.calc();
  const res = doc.getElementById('res').textContent.replace(/\s+/g, ' ');
  check('SF-N99 实算 2.0L×50mmol/L ⇒ 钠 2300 mg', /2300 mg/.test(res), res.slice(0, 120));
  check('SF-N99 实算折算食盐 5.85 g（= 2300/393，非 2300/0.393≈5852）', /5\.85 g/.test(res) && !/5852|5851/.test(res), res.slice(0, 160));
  const tip = doc.getElementById('res').textContent;
  check('SF-N99 结果区提示同步为 ÷393 口径', /折算食盐\(g\) = 钠\(mg\) ÷ 393/.test(tip));
  w.close();
}

// ── SF-N94 + SF-N93：VO2max 估算法选项与时间校验 ──
{
  const REL = 'tools/sports/estimate-tester.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const opts = Array.from(doc.querySelectorAll('#method option'));
  check('SF-N94 方法选项收敛为 2 个（原 3 选项只有 2 套算法）', opts.length === 2, 'options=' + opts.map(o => o.value + ':' + o.textContent).join(','));
  check('SF-N94 选项值仍为 0/1', opts.length === 2 && opts[0].value === '0' && opts[1].value === '1');
  check('SF-N94 已无「英制」重复项', !opts.some(o => /英制/.test(o.textContent)));

  // 通过真实历史恢复入口验证旧记录：3000 m 的 Cooper 结果与 1.5 英里结果不同。
  const timeEl = doc.getElementById('time');
  const distEl = doc.getElementById('distance');
  w.__estimate_testerRender(['method'], '结果', false);
  w.restoreHistory({method:'2', distance:'3000', time:'720', age:'25', gender:'0', weight:'70'});
  const restored = (doc.querySelector('#res .stat-card .val') || {}).textContent;
  check('SF-N94 旧 method=2 恢复为 1.5 英里法（43.8）', doc.getElementById('method').value === '1' && restored === '43.8', 'method=' + doc.getElementById('method').value + ' result=' + restored);
  w.restoreHistory({method:'0', distance:'3000', time:'720', age:'25', gender:'0', weight:'70'});
  const cooper = (doc.querySelector('#res .stat-card .val') || {}).textContent;
  check('SF-N94 Cooper 旧记录仍按原方法恢复', doc.getElementById('method').value === '0' && cooper === '55.8', 'result=' + cooper);

  // SF-N93：时间空串（不是 0）时不得兜底成 1 秒
  doc.getElementById('method').value = '1';
  timeEl.value = '';
  w.calc();
  const res = doc.getElementById('res').textContent;
  check('SF-N93 时间空串 ⇒ 停算提示', /1\.5 英里跑时间需大于 0 秒/.test(res), res.slice(0, 100));
  check('SF-N93 时间空串 ⇒ 不再出现 28983.5 量级荒谬值', !/28983|28984/.test(res));

  // SF-N93 姊妹：12 分钟跑距离过短
  doc.getElementById('method').value = '0';
  distEl.value = '400';
  w.calc();
  const res2 = doc.getElementById('res').textContent;
  check('SF-N93 距离 400 m ⇒ 停算提示', /12 分钟跑距离需大于 504\.9 米/.test(res2), res2.slice(0, 100));
  check('SF-N93 距离过短 ⇒ 不再把负 VO2max 硬钳成 0 并评级', !/很差/.test(res2));
  w.close();
}

console.log('==== sports batch N ' + pass + '/' + (pass + fail) + (HEAD ? ' (HEAD)' : '') + ' ====');
if (fail) process.exit(1);
