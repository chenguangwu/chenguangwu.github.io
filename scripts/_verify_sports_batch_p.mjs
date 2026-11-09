// scripts/_verify_sports_batch_p.mjs — SF-N92 / SF-N109 体育 P 批运行期证据
//
// ① SF-N92 举重体重级别：巴黎周期男子级别为 55/61/67/73/81/89/96/102/109/+109，
//    原实现缺 89kg 与 102kg 两级（88 kg 被判 96kg、101 kg 被判 109kg）。级别判定在 #detail
//    的「估算体重级别」行里，harness 采集得到，但为一次覆盖 5 个边界档位，统一由本脚本遍历断言。
// ② SF-N109 运动记录预设：原实现 `records=[预设]` 覆盖内存且不落盘 ⇒ 用户历史在下次「添加记录」
//    时被整体写回覆盖。现改为追加 + 立即持久化。该路径只由按钮触发，harness 驱动不了，故实地跑。
// 用法：node scripts/_verify_sports_batch_p.mjs [--head]（--head 读 HEAD 版做回退判别）
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

async function loadPage(rel, seedStorage) {
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
      if (seedStorage) {
        try { w.localStorage.setItem(seedStorage.key, JSON.stringify(seedStorage.value)); } catch (e) {}
      }
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  return dom.window;
}

// ── SF-N92：巴黎周期男子级别 10 档 ──
{
  const REL = 'tools/sports/juzhongzongchengji-sinclair-xishu.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const cases = [
    ['55', '55kg'], ['61', '61kg'], ['67', '67kg'], ['73', '73kg'], ['81', '81kg'],
    ['88', '89kg'], ['90', '96kg'], ['100', '102kg'], ['101', '102kg'], ['105', '109kg'], ['110', '+109kg'],
  ];
  let bad = [];
  for (const [bw, want] of cases) {
    doc.getElementById('gender').value = 'm';
    doc.getElementById('bw').value = bw;
    doc.getElementById('snatch').value = '120';
    doc.getElementById('cj').value = '150';
    w.calc();
    const t = doc.getElementById('detail').textContent.replace(/\s+/g, ' ');
    const m = t.match(/估算体重级别：\s*([^（(]+)/);
    const got = m ? m[1].trim() : '(none)';
    if (got !== want) bad.push(bw + 'kg→' + got + '（应 ' + want + '）');
  }
  check('SF-N92 男子 11 个体重档位判定全对（含 89kg / 102kg）', bad.length === 0, bad.join('；'));
  w.close();
}

// ── SF-N109：预设追加而非覆盖、且立即落盘 ──
{
  const REL = 'tools/sports/sports-stats.html';
  const KEY = 'toolbox_sport_stats';
  const seed = [
    { id: 900001, sport: '跑步', minutes: 42, distance: 8, cal: 500, date: '2026-10-01' },
    { id: 900002, sport: '骑行', minutes: 33, distance: 12, cal: 400, date: '2026-10-02' },
  ];
  const w = await loadPage(REL, { key: KEY, value: seed });
  const doc = w.document;
  const before = w.eval('records.length');
  check('SF-N109 初始载入 2 条历史（可读 localStorage）', before === 2, 'before=' + before);

  w.applySportPreset('run');
  const after = w.eval('records.length');
  const stored = JSON.parse(w.localStorage.getItem(KEY) || '[]').length;
  check('SF-N109 载入「跑步周」后记录数 = 2 历史 + 2 示例 = 4', after === 4, 'after=' + after);
  check('SF-N109 示例立即落盘（localStorage 同步为 4 条）', stored === 4, 'stored=' + stored);
  const kept = w.eval('records.filter(function(r){return r.id>=900001&&r.id<=900002;}).length');
  check('SF-N109 原历史记录未被覆盖', kept === 2, 'kept=' + kept);

  // 随后「添加记录」不得把历史冲掉
  doc.getElementById('aMinutes').value = '25';
  doc.getElementById('aDistance').value = '4';
  doc.getElementById('aCal').value = '200';
  w.addRecord();
  const finalLen = w.eval('records.length');
  const finalStored = JSON.parse(w.localStorage.getItem(KEY) || '[]').length;
  const kept2 = w.eval('records.filter(function(r){return r.id>=900001&&r.id<=900002;}).length');
  check('SF-N109 添加新记录后总数 = 5 且历史仍在', finalLen === 5 && kept2 === 2, 'len=' + finalLen + ' kept=' + kept2);
  check('SF-N109 添加后持久化一致（5 条）', finalStored === 5, 'stored=' + finalStored);
  w.close();
}

{
  const KEY = 'toolbox_sport_stats';
  const w = await loadPage('tools/sports/sports-stats.html', { key: KEY, value: [{ id: 100001, sport: '历史', minutes: 20, distance: 1, date: '2026-11-08' }] });
  w.Date.now = () => 100000;
  w.applySportPreset('run'); w.applySportPreset('run');
  let saved = JSON.parse(w.localStorage.getItem(KEY));
  check('SF-N109 固定时钟重复预设 ID 唯一', new Set(saved.map(r => r.id)).size === 5);
  const firstPreset = saved.find(r => r.sport !== '历史');
  w.deleteRecord(firstPreset.id);
  saved = JSON.parse(w.localStorage.getItem(KEY));
  check('SF-N109 删除预设仅删除一条并保留历史', saved.length === 4 && saved.some(r => r.sport === '历史'));
  w.deleteRecord(100001);
  saved = JSON.parse(w.localStorage.getItem(KEY));
  check('SF-N109 删除历史仅删除一条并保留预设', saved.length === 3 && saved.every(r => r.sport !== '历史'));
  w.document.getElementById('aMinutes').value = '20'; w.addRecord();
  w.document.getElementById('aMinutes').value = '20'; w.addRecord();
  saved = JSON.parse(w.localStorage.getItem(KEY));
  check('SF-N109 同毫秒连续添加记录仍不碰撞', new Set(saved.map(r => r.id)).size === 5);
  w.close();
}
{
  const KEY = 'toolbox_sport_stats';
  const w = await loadPage('tools/sports/sports-stats.html', { key: KEY, value: [
    { id: 100001, sport: '跑步', minutes: 20, distance: 1, date: '2026-11-08' },
    { id: 100001, sport: '骑行', minutes: 30, distance: 2, date: '2026-11-07' }
  ] });
  const buttons = w.document.querySelectorAll('#records button');
  buttons[0].click();
  const saved = JSON.parse(w.localStorage.getItem(KEY));
  check('SF-N109 旧重复 ID 删除所选一条不误删另一条', saved.length === 1 && saved[0].sport === '骑行');
  w.close();
}
console.log('==== sports batch P ' + pass + '/' + (pass + fail) + (HEAD ? ' (HEAD)' : '') + ' ====');
if (fail) process.exit(1);
