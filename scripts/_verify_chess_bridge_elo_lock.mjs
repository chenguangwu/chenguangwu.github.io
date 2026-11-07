// 正确性锁定（非两态）：桥牌加倍宕墩罚分阶梯 + Elo 复制/历史取结果区而非下拉框
// 用途：台账中这两条为「陈旧证据」——当前源码已正确，按纪律只复核 + 补锁定用例，不改源码。
// 用法：node scripts/_verify_chess_bridge_elo_lock.mjs
import { JSDOM } from 'jsdom';
import fs from 'fs';

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

// ============ 桥牌：从真实源码抽取 calcPenalty 并跑权威标准值 ============
{
  const html = fs.readFileSync('tools/chess/bridge-scoring.html', 'utf8');
  const m = html.match(/function calcPenalty\(undertricks,doubled,vul\)\{[\s\S]*?\n\}/);
  if (!m) {
    console.log('  ✗ 无法抽出 calcPenalty（源码结构变更？）'); failures++;
  } else {
    const fn = new Function(m[0] + '\nreturn calcPenalty;')();
    // 权威标准（定约桥牌罚分表，1 墩 = 1 trick 未完成）：
    //   未加倍：无局 50/墩、有局 100/墩
    //   加倍：无局 100 / 200 / 200 / 之后 300；有局 200 / 之后 300
    //   再加倍：以上全部 ×2
    const table = [
      [1, 0, 0, 50], [3, 0, 0, 150], [2, 0, 1, 200], [3, 0, 1, 300],
      [1, 1, 0, 100], [2, 1, 0, 300], [3, 1, 0, 500], [4, 1, 0, 800],
      [1, 1, 1, 200], [2, 1, 1, 500], [3, 1, 1, 800],
      [2, 2, 0, 600], [3, 2, 0, 1000],
      [2, 2, 1, 1000], [1, 2, 1, 400],
    ];
    let ok = true, detail = [];
    for (const [u, d, v, want] of table) {
      const got = fn(u, d, v);
      if (got !== want) { ok = false; detail.push(`宕${u}${d === 0 ? '未加倍' : d === 1 ? '加倍' : '再加倍'}${v ? '有局' : '无局'}: 期望${want} 实际${got}`); }
    }
    assert(ok, `加倍/再加倍宕墩罚分符合标准表：${ok ? '15 组全部一致' : detail.join('；')}`);
    assert(fn(2, 1, 1) === 500, `4♠有局加倍宕 2 墩应为 500（台账原记录 400 已不成立）；实际=${fn(2, 1, 1)}`);
  }
}

// ============ Elo：复制与历史应取 #resultBox，不得读 #result 下拉框 ============
{
  const html = fs.readFileSync('tools/chess/elo-rating.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.__copied = [];
      // JSDOM 未实现 innerText，垫成 textContent（页面用 innerText 取结果区文本）
      try {
        Object.defineProperty(w.HTMLElement.prototype, 'innerText', {
          configurable: true,
          get() { return this.textContent; },
          set(v) { this.textContent = v; }
        });
      } catch (e) {}
      w.ToolBox = { copyText: (t) => w.__copied.push(String(t)), showToast() {}, downloadText() {}, showError() {} };
      w.i18nText = (k) => String(k);
      w.TBKit = { util: { isEn: () => false }, history: { record() {}, last: () => null, list: () => [], mount() {} }, matrix: { table() {} }, chart: { line() {} } };
    }
  });
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);
  const $ = (id) => w.document.getElementById(id);

  assert($('result') && $('result').tagName === 'SELECT',
    `前提校验：#result 仍是对局结果下拉框（tagName=${$('result') && $('result').tagName}）`);

  $('myRating').value = '2000'; $('oppRating').value = '1800'; $('kValue').value = '40'; $('games').value = '5';
  w.calc();
  w.__copied.length = 0;
  w.copyResult();
  const copied = w.__copied[0] || '';
  assert(w.__copied.length === 1 && /等级分|每局|预期/.test(copied),
    `复制内容应来自计算结果区（含等级分/每局/预期等计算串）；实际=「${copied.slice(0, 80)}」`);
  assert(!/和棋（0\.5分）/.test(copied) && !/失败（0分）/.test(copied),
    `复制内容不得是下拉框三个选项的完整文字（「胜利（1分）和棋（0.5分）失败（0分）」）；实际=「${copied.slice(0, 80)}」`);

  const resText = typeof w.__elo_ratingResText === 'function' ? w.__elo_ratingResText() : '';
  assert(/2048|等级分/.test(resText),
    `历史「结果」列文本应取自结果区（含新等级分）；实际=「${resText.slice(0, 80)}」`);
  dom.window.close();
}

if (failures > 0) { console.log(`\n[锁定] 桥牌/Elo FAIL (${failures})`); process.exit(1); }
console.log('\n[锁定] 桥牌/Elo PASS（源码已正确，本脚本为回归护栏）');
