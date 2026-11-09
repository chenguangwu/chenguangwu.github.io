// scripts/_verify_sports_batch_q.mjs — SF-N110 / N112 体育 Q 批运行期证据
//
// 两处都是「页面标题/引据表/公式框承诺、但代码未实现」的功能缺口，本批补实现：
//   ① SF-N112 stats-8：新增「射门 / 射正 / 进球 / xG」四项输入与「射正率、射门转化率、
//      射正转化率、进球 − xG」四项输出 + 射正≤射门、进球≤射正 校验；xG 由用户填、本页不建模。
//   ② SF-N110 sports-stats：新增心率输入、配速（min/km）与配速/心率趋势图 + 7/14/30 条滚动均值。
//      趋势图由 TBKit.chart.line 绘制，harness 的 stub 是空函数 ⇒ 门禁里看不见，故在此用 spy 取证。
// 用法：node scripts/_verify_sports_batch_q.mjs [--head]（--head 读 HEAD 版做回退判别）
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

const chartCalls = [];
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
        chart: { line: (sel, opt) => { chartCalls.push({ sel, opt }); }, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      try { w.alert = noop; w.confirm = () => true; } catch (e) {}
      if (seedStorage) { try { w.localStorage.setItem(seedStorage.key, JSON.stringify(seedStorage.value)); } catch (e) {} }
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  return dom.window;
}

// ── SF-N112：stats-8 射门 / 射正 / 进球 / xG ──
{
  const REL = 'tools/sports/stats-8.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const txt = (id) => doc.getElementById(id).textContent.replace(/\s+/g, ' ');
  const has112 = ['shots', 'shotsOn', 'goals', 'xg'].every((id) => !!doc.getElementById(id));
  check('SF-N112 新增射门/射正/进球/xG 四个输入', has112);
  if (!has112) { console.log('  SKIP SF-N112 其余断言（HEAD 版无这四项输入）'); w.close(); }
  else {

  doc.getElementById('matchMin').value = '90';
  doc.getElementById('possMin').value = '54';
  doc.getElementById('passTotal').value = '500';
  doc.getElementById('passOk').value = '420';
  doc.getElementById('oppTotal').value = '300';
  doc.getElementById('oppOk').value = '240';
  doc.getElementById('shots').value = '20';
  doc.getElementById('shotsOn').value = '9';
  doc.getElementById('goals').value = '4';
  doc.getElementById('xg').value = '2.5';
  w.calc();
  let t = txt('res');
  check('SF-N112 射正率 9/20 = 45.00%', /本方射正率：\s*45\.00%/.test(t), t.slice(0, 200));
  check('SF-N112 射门转化率 4/20 = 20.00%', /射门转化率（进球 ÷ 射门）：\s*20\.00%/.test(t), t.slice(0, 240));
  check('SF-N112 射正转化率 4/9 = 44.44%', /射正转化率（进球 ÷ 射正）：\s*44\.44%/.test(t), t.slice(0, 280));
  check('SF-N112 进球 − xG = +1.50 且判「优于期望」', /进球 − xG：\s*\+1\.50/.test(t) && /把握机会优于期望/.test(t), t.slice(-160));

  // xG 留空 ⇒ 不比较
  doc.getElementById('xg').value = '';
  w.calc();
  t = txt('res');
  check('SF-N112 xG 留空 ⇒ 不做期望进球比较', /未填写 xG，不做期望进球比较/.test(t), t.slice(-160));

  // 校验：进球 > 射正
  doc.getElementById('xg').value = '1.2';
  doc.getElementById('shots').value = '10';
  doc.getElementById('shotsOn').value = '4';
  doc.getElementById('goals').value = '5';
  w.calc();
  check('SF-N112 进球 5 > 射正 4 ⇒ 停算提示', /进球数不能多于射正次数/.test(txt('res')), txt('res').slice(0, 120));

  // 校验：射正 > 射门
  doc.getElementById('goals').value = '1';
  doc.getElementById('shotsOn').value = '11';
  w.calc();
  check('SF-N112 射正 11 > 射门 10 ⇒ 停算提示', /射正次数不能多于射门次数/.test(txt('res')), txt('res').slice(0, 120));
  w.close();
  }
}

// ── SF-N112：引据表 xG 口径改为「用户填写」 ──
{
  const REL = 'tools/sports/stats-8.html';
  const src = read(REL);
  check('SF-N112 引据表 xG 行改为「由用户按其数据源口径填写」', /由用户按其数据源口径填写/.test(src) && !/按射门位置与方式赋权估算进球概率/.test(src));
  check('SF-N112 公式框补射正率/转化率/进球−xG 口径', /射正率 = 射正 ÷ 射门 × 100%/.test(src) && /进球 − xG 为相对期望进球的超额/.test(src));
}

// ── SF-N110：sports-stats 配速 / 心率趋势 ──
{
  const REL = 'tools/sports/sports-stats.html';
  const KEY = 'toolbox_sport_stats';
  chartCalls.length = 0;
  const seed = [
    { id: 800003, sport: '跑步', minutes: 36, distance: 6, cal: 360, hr: 146, date: '2026-10-18' },
    { id: 800002, sport: '跑步', minutes: 40, distance: 8, cal: 420, hr: 150, date: '2026-10-16' },
    { id: 800001, sport: '跑步', minutes: 30, distance: 5, cal: 300, hr: 154, date: '2026-10-15' },
  ];
  const w = await loadPage(REL, { key: KEY, value: seed });
  const doc = w.document;
  const has110 = !!doc.getElementById('speedTrend') && !!doc.getElementById('aHr');
  check('SF-N110 新增心率输入与配速/心率趋势容器', has110);
  if (!has110) { console.log('  SKIP SF-N110 其余断言（HEAD 版无趋势段）'); w.close(); }
  else {
  const trend = doc.getElementById('speedTrend').textContent.replace(/\s+/g, ' ');

  // 配速：6.00 / 5.00 / 6.00 ⇒ 平均 5.67，近 7 条滚动均值同为 5.67
  check('SF-N110 平均配速 5.67 分/km（36/6、40/8、30/5）', /平均配速 5\.67 分\/km/.test(trend), trend.slice(0, 220));
  check('SF-N110 平均心率 150 bpm（146/150/154）', /平均心率 150 bpm/.test(trend), trend.slice(0, 260));
  check('SF-N110 心率记录条数 3 条', /有心率记录 3 条/.test(trend), trend.slice(0, 260));

  // 图：应各调一次 chart.line，且配速数据按日期升序
  const paceCall = chartCalls.find((c) => c.sel === '#paceTrendChart');
  const hrCall = chartCalls.find((c) => c.sel === '#hrTrendChart');
  check('SF-N110 配速趋势图被绘制（#paceTrendChart）', !!paceCall);
  check('SF-N110 配速序列按日期升序 = [6.00, 5.00, 6.00]',
    !!paceCall && JSON.stringify(paceCall.opt.series[0].data) === JSON.stringify([6, 5, 6]),
    paceCall ? JSON.stringify(paceCall.opt.series[0].data) : 'none');
  check('SF-N110 心率趋势图被绘制且序列 = [154, 150, 146]',
    !!hrCall && JSON.stringify(hrCall.opt.series[0].data) === JSON.stringify([154, 150, 146]),
    hrCall ? JSON.stringify(hrCall.opt.series[0].data) : 'none');

  // 窗口切换 14 ⇒ 说明文案跟随
  doc.getElementById('maWindow').value = '14';
  w.render();
  const trend14 = doc.getElementById('speedTrend').textContent.replace(/\s+/g, ' ');
  check('SF-N110 滚动窗口切 14 条生效', /近 14 条滚动均值/.test(trend14), trend14.slice(0, 160));

  // 无距离记录（仅力量训练）⇒ 配速显示「—」，不报错
  doc.getElementById('aSport').value = '健身';
  doc.getElementById('aMinutes').value = '40';
  doc.getElementById('aDistance').value = '';
  doc.getElementById('aCal').value = '300';
  doc.getElementById('aHr').value = '128';
  w.addRecord();
  const trendMix = doc.getElementById('speedTrend').textContent.replace(/\s+/g, ' ');
  check('SF-N110 记录行显示心率（… · 128bpm）', /128bpm/.test(doc.getElementById('records').textContent));
  check('SF-N110 混合记录时配速统计只算有距离记录（仍 3 条）', /有距离记录 3 条/.test(trendMix), trendMix.slice(0, 200));
  w.close();
  }
}

{
  chartCalls.length = 0;
  const seed = [8, 1, 6, 3, 7, 2, 5, 4].map(n => ({ id: n, sport: '跑步', minutes: n * 10, distance: 10, hr: 100 + n, date: `2026-11-0${n}` }));
  const w = await loadPage('tools/sports/sports-stats.html', { key: 'toolbox_sport_stats', value: seed });
  let pace = chartCalls.filter(c => c.sel === '#paceTrendChart').at(-1);
  check('SF-N110 倒序插入按实际日期升序', JSON.stringify(pace?.opt.series[0].data) === JSON.stringify([1,2,3,4,5,6,7,8]));
  check('SF-N110 最近七条均值按日期选择', /近 7 条滚动均值\s*5\.00/.test(w.document.getElementById('speedTrend').textContent));
  w.applySportPreset('run');
  pace = chartCalls.filter(c => c.sel === '#paceTrendChart').at(-1);
  check('SF-N110 追加旧预设不改变最近均值', /近 7 条滚动均值\s*5\.00/.test(w.document.getElementById('speedTrend').textContent));
  check('SF-N110 旧预设排在新日期之前', pace?.opt.labels[0] === '2026-10-15' && pace?.opt.labels.at(-1) === '2026-11-08');
  const recentDates = Array.from(w.document.querySelectorAll('#records .meta'), el => el.textContent.slice(0, 10));
  check('SF-N110 最近记录也按日期从新到旧排列', recentDates[0] === '2026-11-08' && recentDates.at(-1) === '2026-10-15');
  w.close();
}
{
  chartCalls.length = 0;
  const seed = [
    { id: 3, sport: '跑步', minutes: 30, distance: 10, date: '2026-11-08' },
    { id: 2, sport: '跑步', minutes: 20, distance: 10, date: '2026-11-08' },
    { id: 1, sport: '跑步', minutes: 10, distance: 10, date: '2026-11-05' }
  ];
  const w = await loadPage('tools/sports/sports-stats.html', { key: 'toolbox_sport_stats', value: seed });
  const pace = chartCalls.filter(c => c.sel === '#paceTrendChart').at(-1);
  check('SF-N110 同日按插入顺序稳定排列', JSON.stringify(pace?.opt.series[0].data) === JSON.stringify([1,2,3]));
  w.close();
}
console.log('==== sports batch Q ' + pass + '/' + (pass + fail) + (HEAD ? ' (HEAD)' : '') + ' ====');
if (fail) process.exit(1);
