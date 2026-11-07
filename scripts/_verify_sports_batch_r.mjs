// scripts/_verify_sports_batch_r.mjs — SF-N95 / N98 体育 R 批运行期证据
//
// ① SF-N95 举重「跨体重预测总成绩」：标题/meta/说明一直承诺、结果却只有当前体重的系数与总成绩。
//    本批补「目标体重」输入 + 等效成绩（Sinclair 归一化逆运算），并明确不是增重/减重预测。
// ② SF-N98 马术「3 种比赛类型」：三种类型共用同一四维等权模型，类型只切换判读说明 ——
//    本批把这点写进评分说明、障碍赛罚分折算口径与功能特点，消除「类型不参与计分」的名实不符。
// 用法：node scripts/_verify_sports_batch_r.mjs [--head]（--head 读 HEAD 版做回退判别）
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
      try { w.alert = noop; w.confirm = () => true; } catch (e) {}
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  return dom.window;
}

// ── SF-N95：跨体重等效成绩 ──
{
  const REL = 'tools/sports/juzhongzongchengji-sinclair-xishu.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const has95 = !!doc.getElementById('targetBw');
  check('SF-N95 新增「目标体重」输入', has95);
  if (!has95) {
    console.log('  SKIP SF-N95 其余断言（HEAD 版无该输入）');
    w.close();
  } else {
    const setBase = () => {
      doc.getElementById('gender').value = 'm';
      doc.getElementById('bw').value = '73';
      doc.getElementById('snatch').value = '140';
      doc.getElementById('cj').value = '170';
      doc.getElementById('age').value = '25';
    };
    const detail = () => doc.getElementById('detail').textContent.replace(/\s+/g, ' ');

    setBase();
    doc.getElementById('targetBw').value = '95';
    w.calc();
    check('SF-N95 目标 95 kg ⇒ 等效 352.4 kg（310×1.2857÷1.1309）', /等效总成绩 ≈ 352\.4 kg/.test(detail()), detail().slice(-260));

    doc.getElementById('targetBw').value = '105';
    w.calc();
    check('SF-N95 目标 105 kg ⇒ 等效 365.7 kg', /等效总成绩 ≈ 365\.7 kg/.test(detail()), detail().slice(-260));

    doc.getElementById('targetBw').value = '81';
    w.calc();
    check('SF-N95 默认目标 81 kg ⇒ 等效 327.9 kg', /等效总成绩 ≈ 327\.9 kg/.test(detail()), detail().slice(-260));

    // 老将模式：基数换成老将修正总成绩
    doc.getElementById('age').value = '40';
    doc.getElementById('targetBw').value = '95';
    w.calc();
    check('SF-N95 老将模式以修正总成绩为基数（40 岁、目标 95 ⇒ 363.9 kg）', /等效总成绩 ≈ 363\.9 kg/.test(detail()), detail().slice(-300));

    // 留空 / 0 / 负值 ⇒ 关闭并说明
    doc.getElementById('age').value = '25';
    doc.getElementById('targetBw').value = '';
    w.calc();
    check('SF-N95 目标体重留空 ⇒ 关闭提示', /跨体重预测已关闭：目标体重需为大于 0 的数值/.test(detail()), detail().slice(-200));
    doc.getElementById('targetBw').value = '-5';
    w.calc();
    check('SF-N95 目标体重 −5 ⇒ 同样关闭', /跨体重预测已关闭/.test(detail()), detail().slice(-200));

    check('SF-N95 公式框写明「逆运算、非增重/减重预测」', /逆运算、同等相对实力换算，非增重\/减重预测/.test(read(REL)));
    w.close();
  }
}

// ── SF-N98：马术三种类型共用等权模型（说明写清）──
{
  const REL = 'tools/sports/rater-36.html';
  const src = read(REL);
  check('SF-N98 评分说明写明「共用同一套四维等权模型」', /三种比赛类型（盛装舞步 \/ 场地障碍 \/ 三项赛）共用同一套四维等权模型/.test(src));
  check('SF-N98 障碍赛说明补罚分折算（一次碰杆扣 2 分）', /换算到 10 分制时按 ×0\.5 折算，故一次碰杆在此扣 2 分/.test(src));
  check('SF-N98 功能特点改为「共用同一四维等权模型」', /3种比赛类型（共用同一四维等权模型，类型切换判读说明）/.test(src));

  const w = await loadPage(REL);
  const doc = w.document;
  const score = () => {
    const t = doc.getElementById('res').textContent.replace(/\s+/g, ' ');
    const m = t.match(/最终得分 \/?\s*([\d.]+)/) || t.match(/^([\d.]+)最终得分/);
    return m ? m[1] : null;
  };
  const setScores = () => {
    doc.getElementById('g1').value = '10';
    doc.getElementById('g2').value = '8';
    doc.getElementById('g3').value = '7';
    doc.getElementById('g4').value = '7';
    doc.getElementById('penalty').value = '2';
  };
  const out = {};
  for (const ty of ['0', '1', '2']) {
    doc.getElementById('type').value = ty;
    setScores();
    w.calc();
    out[ty] = { score: score(), text: doc.getElementById('res').textContent };
  }
  check('SF-N98 三种类型的最终得分一致（同一四维等权模型）',
    out['0'].score === out['1'].score && out['1'].score === out['2'].score && out['0'].score === '7.0',
    JSON.stringify(Object.keys(out).map((k) => out[k].score)));
  check('SF-N98 类型切换仍改变判读说明（盛装舞步 vs 障碍赛文案不同）',
    out['0'].text !== out['1'].text && /盛装舞步/.test(out['0'].text) && /障碍赛/.test(out['1'].text));
  w.close();
}

console.log('==== sports batch R ' + pass + '/' + (pass + fail) + (HEAD ? ' (HEAD)' : '') + ' ====');
if (fail) process.exit(1);
