// scripts/_verify_sports_batch_j.mjs — SF-N78/N80/N81 J 批运行期证据
//
// N78（公式框权重与代码不符）、N80（回合时长口径三处矛盾）都是**说明文案 vs 计算口径**的一致性缺陷，
// 门禁 harness 的 expect 只认「依赖输入的字面串」，拿静态文案做 expect 就是逃生项（铁律⑥），
// 所以改由本脚本注入真实输入后：① 独立按公式框口径复算，② 比对页面实际输出，③ 断言公式框文字已改成实现口径。
// N81（年龄死输入）用两组年龄对照：估算最大心率行必须随年龄变化，且与录入最大心率分列。
// 用法：node scripts/_verify_sports_batch_j.mjs [--head]（--head 读 HEAD 版做回退判别）
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
  await new Promise((r) => setTimeout(r, 150));
  return dom.window;
}

const fill = (doc, map) => {
  for (const k of Object.keys(map)) {
    const el = doc.getElementById(k);
    if (el) { el.value = map[k]; }
  }
};

// ── SF-N78：柔道综合评分须与公式框口径一致（0.4 技术均值 + 0.3 每场技术得分 + 0.3 胜率）──
{
  const rel = 'tools/sports/rater-35.html';
  const w = await loadPage(rel);
  const doc = w.document;
  fill(doc, { ippon: '4', wazari: '1', yuko: '2', match: '8', win: '6', stand: '4', ground: '3', grip: '5' });
  try { w.calc(); } catch (e) {}
  const res = String(doc.getElementById('res').innerHTML || '');
  const shown = (res.match(/综合评分(\d+)分/) || [])[1];
  // 独立复算（按公式框口径）
  const techAvg = (4 * 10 + 3 * 10 + 5 * 10) / 3;          // 40
  const techScore = 4 * 1 + 1 * 0.5 + 2 * 0.2;              // 4.9
  const perMatch = Math.min(100, techScore / 8 * 100);      // 61.25
  const winRate = Math.round(6 / 8 * 100);                  // 75
  const want = Math.round(techAvg * 0.4 + perMatch * 0.3 + winRate * 0.3); // 57
  check('SF-N78 综合评分 == 公式框口径复算值（' + want + '）', shown === String(want), '页面=' + shown + ' 复算=' + want);
  const eq = String((doc.querySelector('.formula-eq') || {}).textContent || '');
  check('SF-N78 公式框已写明 0.4×技术均值', /0\.4\s*×\s*技术均值/.test(eq), 'eq=' + eq.slice(0, 60));
  check('SF-N78 公式框已写明 0.3×每场技术得分 + 0.3×胜率', /0\.3\s*×\s*每场技术得分/.test(eq) && /0\.3\s*×\s*胜率/.test(eq), 'eq=' + eq.slice(0, 80));
  check('SF-N78 公式框不再宣称「0.5·投技 + 0.5·寝技」两维等权', !/0\.5[·×]\s*投技/.test(eq), 'eq=' + eq.slice(0, 60));
}

// ── SF-N80：摔跤回合时长口径统一为「总时间 ÷ 回合数」（公式框不得再扣总间歇）──
{
  const rel = 'tools/sports/time-31.html';
  const w = await loadPage(rel);
  const doc = w.document;
  fill(doc, { total: '10', rounds: '5', rest: '20' });
  try { w.calc(); } catch (e) {}
  const res = String(doc.getElementById('res').innerHTML || '');
  const shown = (res.match(/<div class="num">([^<]+)<\/div><div class="label">单回合时长<\/div>/) || [])[1];
  const restMin = 20 / 60;
  const byCode = (10 / 5).toFixed(0) + ':00';                                    // 2:00
  const byOldFormula = (() => {                                                  // (10 − 4×20s)/5 = 1.733min
    const v = (10 - restMin * 4) / 5, m = Math.floor(v), s = Math.round((v - m) * 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  })();
  check('SF-N80 单回合时长 = 总时间÷回合数（10/5 ⇒ 2:00）', shown === byCode, '页面=' + shown + ' 期望=' + byCode);
  check('SF-N80 单回合时长不再按「扣总间歇」算（≠ ' + byOldFormula + '）', shown !== byOldFormula, '页面=' + shown);
  const eq = String((doc.querySelector('.formula-eq') || {}).textContent || '');
  check('SF-N80 公式框已改为「总时间 ÷ 回合数」', /总时间\s*÷\s*回合数/.test(eq), 'eq=' + eq.slice(0, 60));
  check('SF-N80 公式框不再写「(总时间 − 总间歇) / 回合数」', !/总时间\s*[−-]\s*总间歇/.test(eq), 'eq=' + eq.slice(0, 60));
  check('SF-N80 含间歇总时长 = 10 + 4×20s = 11:20', /<div class="num">11:20<\/div><div class="label">含间歇总时长<\/div>/.test(res), 'res=' + res.slice(0, 200));
}

// ── SF-N81：年龄参与计算（估算最大心率 = 220−年龄），与录入最大心率分列 ──
{
  const rel = 'tools/sports/tester-7.html';
  const w30 = await loadPage(rel);
  const d30 = w30.document;
  fill(d30, { vo2max: '52', atHr: '165', maxHr: '185', age: '30', rhr: '55', gender: '0' });
  try { w30.calc(); } catch (e) {}
  const h30 = String(d30.getElementById('res').innerHTML || '');
  const est30 = (h30.match(/<td>年龄估算最大心率<\/td><td>(\d+) bpm<\/td>/) || [])[1];

  const w50 = await loadPage(rel);
  const d50 = w50.document;
  fill(d50, { vo2max: '52', atHr: '165', maxHr: '185', age: '50', rhr: '55', gender: '0' });
  try { w50.calc(); } catch (e) {}
  const h50 = String(d50.getElementById('res').innerHTML || '');
  const est50 = (h50.match(/<td>年龄估算最大心率<\/td><td>(\d+) bpm<\/td>/) || [])[1];

  check('SF-N81 年龄 30 ⇒ 估算最大心率 190', est30 === '190', 'est30=' + est30);
  check('SF-N81 年龄 50 ⇒ 估算最大心率 170', est50 === '170', 'est50=' + est50);
  check('SF-N81 年龄变化会改变页面输出（死输入已修复）', !!est30 && !!est50 && est30 !== est50, '30→' + est30 + ' / 50→' + est50);
  check('SF-N81 「最大心率」行标注为录入/实测值而非「220-年龄」', /<td>最大心率<\/td><td>185 bpm<\/td><td>录入\/实测值<\/td>/.test(h30), 'h30 片段缺失');
}

console.log('\n==== sports J 批运行期证据: ' + pass + '/' + (pass + fail) + ' ====');
process.exit(fail ? 1 : 0);
