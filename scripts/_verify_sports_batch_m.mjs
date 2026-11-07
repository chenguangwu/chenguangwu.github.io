// scripts/_verify_sports_batch_m.mjs — SF-N105/N106/N108 体育参考 M 批运行期证据
//
// 本页两个功能都由按钮触发（输入框无 oninput 重算），门禁 harness 只派发 input/change 事件，
// 打不出结果 ⇒ 无法用 expect 断言。故由本脚本直接调用页面函数取证：
//   ① SF-N105 Cooper 单位：2400 m 必须落在「42.4」而不是按公里直代系数的 75.0；
//   ② SF-N106 帐篷推荐方向：低风速应回三季帐，高风速回高山帐（原实现恒定高山帐）；
//   ③ SF-N108 公式框位置：VO2max 公式必须位于 #panel-vo2 内，攀岩面板不得再出现 VO2 公式。
// 用法：node scripts/_verify_sports_batch_m.mjs [--head]（--head 读 HEAD 版做回退判别）
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

const REL = 'tools/sports/sports-reference.html';

// ── SF-N105：Cooper 12 分钟跑必须按「英里」口径换算 ──
{
  const w = await loadPage(REL);
  const doc = w.document;
  doc.getElementById('vo2Method').value = 'cooper';
  doc.getElementById('vo2Value').value = '2400';
  try { w.calcVo2(); } catch (e) {}
  const txt = String(doc.getElementById('vo2Result').textContent || '');
  const vo2 = (txt.match(/^([\d.]+)VO2max/) || [])[1];
  check('SF-N105 Cooper 2400 m ⇒ 42.4 ml/kg/min', vo2 === '42.4', '页面=' + vo2);
  check('SF-N105 不再是按公里直代系数的 75.0', vo2 !== '75.0', '页面=' + vo2);
  check('SF-N105 评级随之为「好」（37–44）', /好评级/.test(txt), txt.slice(0, 24));
}

// ── SF-N106：帐篷推荐按抗风上限升序取首个可承受型号 ──
{
  const w = await loadPage(REL);
  const doc = w.document;
  const run = (v) => {
    doc.getElementById('windSpeed').value = String(v);
    try { w.checkWindTent(); } catch (e) {}
    return String(doc.getElementById('windResult').textContent || '');
  };
  const t5 = run(5), t40 = run(40), t60 = run(60), t88 = run(88), t120 = run(120);
  check('SF-N106 5 km/h ⇒ 三季帐', /推荐帐篷类型：三季帐/.test(t5), t5.slice(0, 40));
  check('SF-N106 40 km/h ⇒ 三季帐（上限 50 ≥ 40，仍用最低档）', /推荐帐篷类型：三季帐/.test(t40), t40.slice(0, 40));
  check('SF-N106 60 km/h ⇒ 四季帐', /推荐帐篷类型：四季帐/.test(t60), t60.slice(0, 40));
  check('SF-N106 88 km/h ⇒ 高山帐', /推荐帐篷类型：高山帐/.test(t88), t88.slice(0, 40));
  check('SF-N106 120 km/h ⇒ 不建议扎营', /不建议扎营/.test(t120), t120.slice(0, 40));
}

// ── SF-N108：VO2max 公式框必须挂在 VO2max 面板，攀岩面板不得含 VO2 公式 ──
{
  const w = await loadPage(REL);
  const doc = w.document;
  const climb = doc.getElementById('panel-climbing');
  const vo2 = doc.getElementById('panel-vo2');
  const climbTxt = climb ? String(climb.textContent || '') : '';
  const vo2Txt = vo2 ? String(vo2.textContent || '') : '';
  check('SF-N108 攀岩面板不再出现 VO2max 公式', climbTxt !== '' && !/VO2max 估算/.test(climbTxt), 'climb 片段=' + climbTxt.slice(0, 40));
  check('SF-N108 VO2max 面板已含公式框', /VO2max 估算/.test(vo2Txt) && /35\.97/.test(vo2Txt));
  check('SF-N108 攀岩面板改为抱石/绳索对照口径说明', /V 级为抱石/.test(climbTxt), 'climb 片段=' + climbTxt.slice(0, 60));
}

console.log('\n==== sports M 批运行期证据: ' + pass + '/' + (pass + fail) + ' ====');
process.exit(fail ? 1 : 0);
