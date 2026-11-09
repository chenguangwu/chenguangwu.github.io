// scripts/_verify_sports_batch_k.mjs — SF-N83/N86/N87 K 批运行期证据
//
// N86（引据表称加权、实现为等权）、N87（预设把 activity 置空导致回落跑步 13km/h）都属
// 「静态说明文案 / 预设参数」类问题：门禁 harness 的 expect 只认依赖输入的字面串，
// 拿静态文案断言就是逃生项（铁律⑥）。故由本脚本运行期取证：
//   ① 抓 TBKit.preset.bar 的预设配置，检查 activity 是否为空，并按预设值实算热量；
//   ② 按引据表口径（八项等权）独立复算，与页面输出的风险指数比对；
//   ③ 断言引据表/深度解析文案已改齐（不再写「加权」、示例为 8 维 23 分算例）。
// 用法：node scripts/_verify_sports_batch_k.mjs [--head]（--head 读 HEAD 版做回退判别）
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

async function loadPage(rel, onKit) {
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
        preset: { bar: (sel, items, cb) => { if (onKit) onKit(w, sel, items, cb); } },
        chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop },
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

// ── SF-N87：三个预设必须显式带活动类型，并按各自活动实算热量 ──
{
  const rel = 'tools/sports/calc-61.html';
  let presets = null;
  const w = await loadPage(rel, (win, sel, items) => { presets = items; });
  const doc = w.document;
  check('SF-N87 预设已注册（4 个）', Array.isArray(presets) && presets.length === 4, 'presets=' + (presets && presets.length));
  const names = ['跑步1小时', '步行90分', '适中45分'];
  const emptyAct = (presets || []).filter((p) => names.indexOf(p.label) >= 0 && !String((p.values || {}).activity || '').trim());
  check('SF-N87 三个预设 activity 均非空', emptyAct.length === 0, '空 activity 预设=' + emptyAct.map((p) => p.label).join(','));

  // 按「步行90分」预设实算：65kg × 1.5h × (快走 6km/h 5.0 MET × 0.9) = 438.75 → 439 kcal
  const walk = (presets || []).find((p) => p.label === '步行90分');
  if (walk) {
    for (const k of Object.keys(walk.values)) { const el = doc.getElementById(k); if (el) el.value = walk.values[k]; }
    try { w.calc(); } catch (e) {}
  }
  const sum = String(doc.getElementById('summary').innerHTML || '');
  const kcal = (sum.match(/(\d+)<\/div><div class="label">消耗 kcal/) || [])[1];
  check('SF-N87「步行90分」= 439 kcal（快走 6km/h，非跑步 13km/h 的 1035 kcal）', kcal === '439', '页面=' + kcal);
  const det = String(doc.getElementById('detail').innerHTML || '');
  check('SF-N87 明细中的活动名称为快走 6km/h', /活动：<strong>快走 6km\/h<\/strong>/.test(det), 'detail 片段=' + det.slice(0, 80));
}

// ── SF-N86：引据表/深解析文案改齐 + 八项等权口径可复现 ──
{
  const rel = 'tools/sports/assessor-risk-2.html';
  const w = await loadPage(rel);
  const doc = w.document;
  const body = String(doc.body.textContent || '');
  // 引据表单元格是「英文可见文本 + data-zh 存中文原文」（构建期预渲染），中文口径要查 data-zh
  const zhAttrs = Array.from(doc.querySelectorAll('[data-zh]')).map((e) => e.getAttribute('data-zh')).join('\n');
  check('SF-N86 引据表不再称「加权总分 / 乘以权重后求和」', !/加权总分/.test(zhAttrs) && !/乘以权重后求和/.test(zhAttrs));
  check('SF-N86 引据表已写明「8 项等权相加、满分 40」', /安全评分 = 8 项得分直接相加/.test(zhAttrs) && /满分 40/.test(zhAttrs), 'zh 片段缺失');
  const deepDive = JSON.parse(read('i18n/tools/content_deepdive.json'))['sports/assessor-risk-2'].examples[0].body;
  const english = JSON.parse(read('i18n/tools/en/sports/assessor-risk-2.json')).map[deepDive];
  check('SF-N86 深度解析示例改为 8 维算例（23 分 → 43/100）', /23 分/.test(body) && /43\/100/.test(body));
  check('SF-N86 构建源与页面算例一致并有英文译文', body.includes(deepDive) && !!english && /23 points/.test(english) && /43\/100/.test(english));

  const vals = { a1: '2', a2: '2', a3: '2', a4: '3', a5: '3', a6: '4', a7: '3', a8: '4' };
  for (const k of Object.keys(vals)) { const el = doc.getElementById(k); if (el) el.value = vals[k]; }
  try { w.calc(); } catch (e) {}
  const res = String(doc.getElementById('res').innerHTML || '');
  const score = (res.match(/>(\d+)<\/div><div class="lbl">风险指数\/100/) || [])[1];
  const total = vals && Object.keys(vals).reduce((a, k) => a + Number(vals[k]), 0);
  const want = Math.round((1 - total / 40) * 100);
  check('SF-N86 风险指数 == 等权求和复算值（' + want + '）', score === String(want), '页面=' + score + ' 复算=' + want);
  check('SF-N86 等级为「中高风险」（23 分落 16–24）', /中高风险/.test(res), 'res 片段=' + res.slice(0, 120));
}

// ── SF-N83：夹角 179.5° 必须被拦，不得再渲染 114.59 倍角度因子 ──
{
  const rel = 'tools/sports/analysis-spacing.html';
  const w = await loadPage(rel);
  const doc = w.document;
  doc.getElementById('angle').value = '179.5';
  try { w.calc(); } catch (e) {}
  const res = String(doc.getElementById('res').innerHTML || '');
  check('SF-N83 夹角 ≥170° 时停算并提示', /夹角 ≥170° 时角度因子已超过 5\.7/.test(res), 'res=' + res.slice(0, 120));
  check('SF-N83 不再渲染 114.59 倍角度因子', !/114\.59/.test(res), 'res=' + res.slice(0, 160));
}

console.log('\n==== sports K 批运行期证据: ' + pass + '/' + (pass + fail) + ' ====');
process.exit(fail ? 1 : 0);
