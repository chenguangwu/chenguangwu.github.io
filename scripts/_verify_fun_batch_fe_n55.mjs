// FE-N55 运行期两态锁（random-picker.html）
// 缺陷（历史）：不放回抽完会静默重新洗牌，永不提示「已空」。
// 当前源码已修复：if(unique){... if(pool.length===0){ 显示「所有选项已抽完！」; return; }}
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import process from 'process';
import fs from 'fs';

const file = 'tools/fun/random-picker.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');

function makeTBKit() {
  return {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    matrix: { table() {} }, chart: { line() {} },
    history: { _recs: [], record(r) { this._recs.push(r); }, last() { return null; }, list() { return this._recs; }, mount() {} },
  };
}

function run() {
  const dom = new JSDOM(html, { runScripts: 'dangerously', beforeParse(w) { w.TBKit = makeTBKit(); } });
  const d = dom.window.document;
  d.getElementById('items').value = 'A\nB';
  d.getElementById('seed').value = 'seed55';
  d.getElementById('unique').checked = true;
  return dom;
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const dom = run();
  // 不重复模式：2 个选项，抽 2 次后池空，第 3 次「开始」应提示已抽完而非静默重洗
  for (let i = 0; i < 3; i++) { dom.window.start(); await sleep(1300); }
  const out = dom.window.document.getElementById('output').textContent || '';
  const showsEmpty = out.includes('所有选项已抽完');
  console.log(`[N55] 第3次开始后的 output="${out.slice(0, 40)}" 含「已抽完」=${showsEmpty} → ${showsEmpty ? 'PASS(抽完提示生效)' : 'FAIL(静默重洗/无提示)'}`);
  process.exit(showsEmpty ? 0 : 1);
})();
