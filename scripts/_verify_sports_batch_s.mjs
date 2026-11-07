// scripts/_verify_sports_batch_s.mjs — SF-N114/115/116/117/118 体育 S 批运行期证据
//
// ① tester-1（俯卧撑/引体 1RM）
//    SF-N114 Brzycki 的 36/(37−r) 在 r→37 发散：r=36 得 855.7 kg / 12.22 倍体重判「精英」、r=38 得负值。
//            本批 r>15 不再取 Brzycki 均值（只用 Epley）、r>30 直接停算、输入加 max=30。
//    SF-N115 「上斜俯卧撑/脚垫高」两个方向相反的动作合并为同一 0.70：拆成手撑高台 0.41 与脚垫高 0.70。
//    SF-N116 俯卧撑分支不读附加负重（预设 added=5 被吞）：改为 体重×姿势系数 + 附加负重，且负重框两动作常显。
// ② tester-8（MAOD）
//    SF-N117 三个预设 5400/2700/3600 秒越过 max=600，算出 900/450/1020 ml/kg 仍判「优秀」：预设改 180/240/300 秒 + 越界停算。
//    SF-N118 全页无校验：空值/avgVo2>VO2max/restVo2 越界都照出结果（−50.0 也当分数）。
// 用法：node scripts/_verify_sports_batch_s.mjs [--head]（--head 读 HEAD 版做回退判别）
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

// ── SF-N114 / N115 / N116：tester-1 ──
{
  const REL = 'tools/sports/tester-1.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const txt = () => doc.getElementById('res').textContent.replace(/\s+/g, ' ').trim();
  const setIn = (o) => {
    doc.getElementById('move').value = o.move || 'pushup';
    if (w.toggleExtra) w.toggleExtra();
    doc.getElementById('bw').value = o.bw;
    doc.getElementById('reps').value = o.reps;
    if (o.posture) doc.getElementById('posture').value = o.posture;
    doc.getElementById('added').value = o.added || '0';
    w.calc();
  };

  // SF-N114：原始复现值 36 次 ⇒ 必须停算（HEAD：855.7 kg / 12.22 倍「精英水平」）
  setIn({ move: 'pushup', bw: '70', reps: '36', posture: '0.64' });
  check('SF-N114 reps=36（原算出 855.7 kg / 12.22 倍「精英」）⇒ 停算', /力竭次数需在 1–30 次之间/.test(txt()), txt().slice(0, 160));
  check('SF-N114 reps=36 不再输出 855.7 / 12.22', !/855\.7|12\.22/.test(txt()), txt().slice(0, 160));

  setIn({ move: 'pushup', bw: '70', reps: '42', posture: '0.64' });
  check('SF-N114 reps=42（原算出负值 −755.6）⇒ 停算', /力竭次数需在 1–30 次之间/.test(txt()), txt().slice(0, 160));

  // r>15 且 ≤30：只用 Epley，不取均值
  setIn({ move: 'pushup', bw: '80', reps: '20', posture: '0.70', added: '0' });
  check('SF-N114 reps=20 ⇒ Brzycki 不参与', /不参与（次数 >15，公式发散）/.test(txt()), txt().slice(0, 260));
  check('SF-N114 reps=20 ⇒ 只用 Epley：负荷 56、1RM 93.3、相对力量 1.17',
    /推算 1RM[\s\S]*93\.3/.test(txt()) && /1\.17/.test(txt()), txt().slice(0, 260));

  // r=15 仍取两式均值（边界含 15）
  setIn({ move: 'pullup', bw: '70', reps: '15', added: '0' });
  check('SF-N114 reps=15（边界）⇒ 仍取两式均值 109.8', /109\.8/.test(txt()) && !/不参与/.test(txt()), txt().slice(0, 260));

  // SF-N115：上斜与脚垫高拆开
  const opts = Array.from(doc.querySelectorAll('#posture option')).map((o) => o.value + '|' + o.textContent.trim());
  check('SF-N115 姿势选项 ≥4 且上斜 0.41 / 脚垫高 0.70 分离',
    opts.length >= 4 && opts.some((s) => s.startsWith('0.41|') && /上斜/.test(s)) && opts.some((s) => s.startsWith('0.70|') && /脚垫高/.test(s)),
    opts.join(' / '));
  check('SF-N115 不再有「上斜俯卧撑/脚垫高」合并项', !opts.some((s) => /上斜俯卧撑\/脚垫高/.test(s)), opts.join(' / '));

  // SF-N116：俯卧撑分支叠加附加负重
  setIn({ move: 'pushup', bw: '80', reps: '15', posture: '0.41', added: '5' });
  check('SF-N116 俯卧撑叠加附加负重：80×0.41+5=37.8 kg',
    /自重负荷比例 41% × 体重 80 kg \+ 附加负重 5 kg = 37\.8 kg/.test(txt()), txt().slice(0, 260));
  check('SF-N116 俯卧撑 1RM 均值 59.3', /59\.3/.test(txt()), txt().slice(0, 260));
  check('SF-N116 俯卧撑模式下附加负重输入框可见', doc.getElementById('pullupOpt').style.display !== 'none',
    'display=' + JSON.stringify(doc.getElementById('pullupOpt').style.display));

  // 预设的姿势值同步为 0.41
  check('SF-N115 负重预设「上斜俯卧撑 15 次」姿势改为 0.41', /"posture":"0\.41"[^}]*"added":5/.test(read(REL)));
  w.close();
}

// ── SF-N117 / N118：tester-8（MAOD）──
{
  const REL = 'tools/sports/tester-8.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const txt = () => doc.getElementById('res').textContent.replace(/\s+/g, ' ').trim();
  const setIn = (o) => {
    for (const k of ['vo2max', 'weight', 'duration', 'avgVo2', 'restVo2']) doc.getElementById(k).value = String(o[k]);
    doc.getElementById('exercise').value = o.exercise || '0';
    w.calc();
  };
  const ok = { vo2max: 42, weight: 42, duration: 300, avgVo2: 30, restVo2: 3.5 };

  // SF-N118：合法值出正确结果
  setIn(ok);
  check('SF-N118 合法值 42/42/300/30/3.5 ⇒ MAOD 60.0「良好」',
    /您的MAOD为60\.0ml\/kg，属于良好水平/.test(txt()), txt().slice(0, 400));

  // SF-N117：时长越界（原预设 5400 秒 ⇒ 900.0 ml/kg「优秀」）
  setIn({ ...ok, duration: 5400 });
  check('SF-N117 时长 5400（原 900.0 ml/kg「优秀」）⇒ 停算', /全力运动持续时间需在 10–600 秒之间/.test(txt()), txt().slice(0, 200));
  check('SF-N117 时长 5400 不再输出 900.0 / 优秀', !/900\.0/.test(txt()), txt().slice(0, 200));

  setIn({ ...ok, duration: 3600 });
  check('SF-N117 时长 3600（原 1020.0）⇒ 停算', /全力运动持续时间需在 10–600 秒之间/.test(txt()), txt().slice(0, 200));

  // 预设本身全部落在 10–600
  const src = read(REL);
  const presetDur = Array.from(src.matchAll(/['"]?duration['"]?\s*:\s*['"]?(\d+)/g)).map((m) => +m[1]);
  check('SF-N117 预设时长全部落在 10–600 秒内',
    presetDur.length >= 4 && presetDur.every((d) => d >= 10 && d <= 600), JSON.stringify(presetDur));

  // SF-N118：avgVo2 > VO2max（原 −50.0 照出结果）
  setIn({ ...ok, avgVo2: 60, vo2max: 50 });
  check('SF-N118 avgVo2 60 > VO2max 50（原 −50.0）⇒ 停算', /不能高于 VO2max（50）/.test(txt()), txt().slice(0, 200));
  check('SF-N118 不再输出 −50.0', !/-50\.0/.test(txt()), txt().slice(0, 200));

  // SF-N118：restVo2 越界（原 B 类用例注入 42 照样出结果）
  setIn({ ...ok, restVo2: 42 });
  check('SF-N118 restVo2=42 越界 ⇒ 停算', /静息摄氧量需在 1–10 ml\/kg\/min 之间/.test(txt()), txt().slice(0, 200));

  // SF-N118：清空 avgVo2（原 75.0「优秀」）
  setIn({ ...ok, avgVo2: '' });
  check('SF-N118 清空平均摄氧量（原 75.0「优秀」）⇒ 停算', /运动中平均摄氧量需在 10–100 ml\/kg\/min 之间/.test(txt()), txt().slice(0, 200));
  check('SF-N118 清空后不再输出 75.0', !/75\.0/.test(txt()), txt().slice(0, 200));

  // 清空时长
  setIn({ ...ok, duration: '' });
  check('SF-N118 清空时长（原 0.0「较弱」）⇒ 停算', /全力运动持续时间需在 10–600 秒之间/.test(txt()), txt().slice(0, 200));

  check('SF-N117/N118 公式框写明「需氧量以 VO2max 为上限」的简化口径与不可比性',
    /需氧量以 VO2max 作为上限/.test(src) && /不可与实验室 MAOD 文献值直接比较/.test(src));
  w.close();
}

console.log('==== sports batch S ' + pass + '/' + (pass + fail) + (HEAD ? ' (HEAD)' : '') + ' ====');
if (fail) process.exit(1);
