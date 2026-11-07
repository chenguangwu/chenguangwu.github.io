// scripts/_verify_sports_batch_o.mjs — SF-N96/N97/N101/N113 体育 O 批运行期证据
//
// 门禁 harness 只能断「依赖输入变化的输出串」，以下四项属「公式框/文案与代码口径一致性」
// 与「表单属性边界」，用 expect 断言会退化成静态锚（默认态也命中 ⇒ 逃生项），故直取 DOM：
//   ① SF-N101 睡眠恢复：公式框权重维度必须与代码 0.45×时长 + 0.35×深睡 + 0.20×入睡 一致；
//   ② SF-N96 疲劳指数：公式框归一化必须与代码 min(CK/1000×100,100)、clamp((BUN−5)/8×100) 一致；
//   ③ SF-N97 马术 rater-36：公式框不得再是跳水模板（「4 名裁判」「动作类型」），须为四维均值 − 罚分×0.5；
//   ④ SF-N113 力量计划：周训练天数 max 必须 = 7，且第八~十四日标签已清除（原可填 14）。
// 用法：node scripts/_verify_sports_batch_o.mjs [--head]（--head 读 HEAD 版做回退判别）
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
        preset: { bar: noop },
        chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
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

// ── SF-N101 / N102：睡眠恢复指数 ──
{
  const REL = 'tools/sports/shuimianhuifuzhiliang.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const eq = doc.querySelector('.formula-eq').textContent.replace(/\s+/g, ' ');
  check('SF-N101 公式框权重维度含「0.45×时长评分」', /0\.45\s*×\s*时长评分/.test(eq), eq);
  check('SF-N101 公式框含「0.35×深睡评分」与「0.20×入睡评分」', /0\.35\s*×\s*深睡评分/.test(eq) && /0\.20\s*×\s*入睡评分/.test(eq), eq);
  check('SF-N101 公式框不再出现「深睡占比」（该维度代码里不存在）', !/深睡占比/.test(eq), eq);

  // 口径可复算：8.2 h / 25% / 20 min ⇒ 100 / 100 / 90 ⇒ 45+35+18 = 98
  doc.getElementById('dur').value = '8.2';
  doc.getElementById('deep').value = '25';
  doc.getElementById('latency').value = '20';
  doc.getElementById('awake').value = '0';
  w.calc();
  const res = doc.getElementById('res').textContent.replace(/\s+/g, ' ');
  check('SF-N101 公式框口径可复算 8.2h/25%/20min ⇒ 96（45+35+15.6，latScore(20)=78）', /睡眠恢复指数：96/.test(res), res.slice(0, 160));

  // SF-N102：0 h 停算，且不再输出保底 70.75 / 55 分等级
  doc.getElementById('dur').value = '0';
  w.calc();
  const res0 = doc.getElementById('res').textContent;
  check('SF-N102 0 h ⇒ 停算提示', /睡眠时长需大于 0 h/.test(res0), res0.slice(0, 120));
  check('SF-N102 0 h ⇒ 不再给出「恢复良好/一般」等级', !/恢复良好|恢复一般|恢复充分/.test(res0));
  w.close();
}

// ── SF-N96：疲劳恢复趋势 FI 归一化口径 ──
{
  const REL = 'tools/sports/pilaohuifuqushi.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const eq = doc.querySelector('.formula-eq').textContent.replace(/\s+/g, ' ');
  check('SF-N96 公式框含「0.6×CK 评分 + 0.4×BUN 评分」', /0\.6\s*×\s*CK\s*评分\s*\+\s*0\.4\s*×\s*BUN\s*评分/.test(eq), eq);
  check('SF-N96 公式框给出代码口径「CK ÷ 1000 × 100」', /CK\s*÷\s*1000\s*×\s*100/.test(eq), eq);
  check('SF-N96 公式框不再出现 w₁/w₂ 泛式', !/w₁|w₂/.test(eq), eq);

  // 口径可复算：CK 320 / BUN 6.5（默认）⇒ CK 评分 32、BUN 评分 18.75 ⇒ FI = 26.7 → 页面 27
  doc.getElementById('ck').value = '320';
  doc.getElementById('bun').value = '6.5';
  doc.getElementById('hours').value = '12';
  w.calc();
  const res = doc.getElementById('res').textContent.replace(/\s+/g, ' ');
  check('SF-N96 公式框口径可复算 CK320/BUN6.5 ⇒ FI 26.7→27', /27\s*综合疲劳指数/.test(res), res.slice(0, 200));
  w.close();
}

// ── SF-N97：马术 rater-36 公式框不再是跳水模板 ──
{
  const REL = 'tools/sports/rater-36.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const eq = doc.querySelector('.formula-eq').textContent.replace(/\s+/g, ' ');
  check('SF-N97 公式框含四维「步态质量 + 跳跃技术 + 骑手姿态 + 路线准确性」',
    /步态质量\s*\+\s*跳跃技术\s*\+\s*骑手姿态\s*\+\s*路线准确性/.test(eq), eq);
  check('SF-N97 公式框不再出现「跳水」/「裁判」', !/跳水|裁判/.test(eq), eq);

  // 可复算：10/8/7/7（均为 select 实有档位）、罚分 2 ⇒ 8.00 − 1.00 = 7.00 → 7.0「良好」
  doc.getElementById('type').value = '0';
  doc.getElementById('g1').value = '10';
  doc.getElementById('g2').value = '8';
  doc.getElementById('g3').value = '7';
  doc.getElementById('g4').value = '7';
  doc.getElementById('penalty').value = '2';
  w.calc();
  const res = doc.getElementById('res').textContent.replace(/\s+/g, ' ');
  check('SF-N97 公式框口径可复算 (10+8+7+7)/4−2×0.5 ⇒ 7.0', /7\.0\s*最终得分/.test(res), res.slice(0, 160));
  w.close();
}

// ── SF-N113：周训练天数上限 ──
{
  const REL = 'tools/sports/strength-5.html';
  const raw = read(REL);
  check('SF-N113 周训练天数 max=7', /id="days"[^>]*max="7"/.test(raw), (raw.match(/id="days"[^>]*/) || [''])[0]);
  check('SF-N113 不再含「第八日…第十四日」标签', !/第八日|第十一日|第十四日/.test(raw));

  const w = await loadPage(REL);
  const doc = w.document;
  doc.getElementById('total').value = '420';
  doc.getElementById('days').value = '8';
  w.calc();
  const res = doc.getElementById('res').textContent;
  check('SF-N113 填 8 天 ⇒ 停算提示', /周训练天数需在 2–7 天之间/.test(res), res.slice(0, 120));

  doc.getElementById('days').value = '7';
  w.calc();
  const res7 = doc.getElementById('res').textContent.replace(/\s+/g, ' ');
  check('SF-N113 填 7 天 ⇒ 合法并排到「周日」', /周日 · 低强度/.test(res7), res7.slice(-120));
  w.close();
}

console.log('==== sports batch O ' + pass + '/' + (pass + fail) + (HEAD ? ' (HEAD)' : '') + ' ====');
if (fail) process.exit(1);
