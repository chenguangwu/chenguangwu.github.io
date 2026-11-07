// FE-N54 运行期两态锁（random-picker.html）
// 缺陷：记录的「结果」是「🎲 抽取中...」占位串，而非真实抽取项（包装器在 start() 同步返回即抓取，真实结果需等 15×80ms 动画）。
// 修复：① __random_pickerResText 把「抽取中」视为无结果；② 在 interval 真实定格后再调用 __random_pickerExtras() 记录。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import process from 'process';
import fs from 'fs';

const file = 'tools/fun/random-picker.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');

function makeTBKit(dom) {
  return {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    matrix: { table() {} },
    chart: { line() {} },
    history: {
      _recs: [],
      record(rec) { this._recs.push(rec); },
      last() { return this._recs[this._recs.length - 1] || null; },
      list() { return this._recs; },
      mount() {},
    },
  };
}

function run() {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    beforeParse(w) { w.TBKit = makeTBKit(w); },
  });
  const d = dom.window.document;
  d.getElementById('items').value = '苹果\n香蕉\n橙子\n葡萄';
  d.getElementById('seed').value = 'testseed123';
  d.getElementById('unique').checked = true;
  dom.window.start();
  return dom;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const dom = run();
  await sleep(1500); // 等 interval 定格（15×80ms=1200ms）+ 缓冲
  const recs = dom.window.TBKit.history._recs;
  const items = ['苹果', '香蕉', '橙子', '葡萄'];
  const got = recs.length ? (recs[recs.length - 1]['结果'] || '') : '(无记录)';
  const isReal = items.includes(got);
  const isPlaceholder = got.includes('抽取中');
  const pass = recs.length >= 1 && isReal && !isPlaceholder;
  console.log(`[N54] 记录条数=${recs.length} 末条结果="${got}" 真实项=${isReal} 占位串=${isPlaceholder} → ${pass ? 'PASS(记到真实结果)' : 'FAIL(记到占位串/无记录)'}`);
  process.exit(pass ? 0 : 1);
})();
