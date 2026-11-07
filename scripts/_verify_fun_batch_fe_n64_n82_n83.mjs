// 两态锁：FE-N64（color-guess 重置取消换题定时器）、FE-N82（riddle 关键词真实匹配）、FE-N83（riddle 同池不重复抽取）
// 用法：node scripts/_verify_fun_batch_fe_n64_n82_n83.mjs [--head]
//   --head 用 git show HEAD:<file> 取修复前版本，验证旧版确实 FAIL（判别力）。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

function loadHtml(file) {
  return head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
}

function boot(html, beforeParse) {
  return new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      // 最小 TBKit / ToolBox 桩（页面脚本可能调用记录/提示）
      w.TBKit = {
        util: { isEn: () => false },
        history: { record() {}, last: () => null, list: () => [], mount() {} },
        matrix: { table() {} }, chart: { line() {} },
        preset: { bar() {} }, utilx: {}
      };
      w.ToolBox = { showToast() {}, downloadText() {}, showError() {} };
      if (beforeParse) beforeParse(w);
    }
  });
}

// ============ FE-N64 : 重置后旧换题定时器必须作废 ============
{
  const html = loadHtml('tools/fun/color-guess.html');
  const dom = boot(html);
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  if (typeof w.start !== 'function' || typeof w.choose !== 'function' || typeof w.reset !== 'function') {
    console.log('  ✗ start/choose/reset 不可见，N64 锁无法判定');
    failures++;
  } else {
    w.start();                                   // 第 1 轮出题
    const tgt = w.eval('target');                // 顶层 let ⇒ 全局词法绑定，eval 可见
    const opt = w.document.querySelector('.opt');
    w.choose(tgt, opt);                          // 答题 ⇒ 启动 1s 换题定时器
    w.reset();                                   // 立刻重置（应作废旧定时器）
    await sleep(1300);                           // 越过 1s 边界
    const out = (w.document.getElementById('output').textContent || '').trim();
    const rnd = w.eval('round');
    // 修复版：重置后 stay 在「点击开始」提示、round=0；HEAD：旧回调 1s 后 nextRound() ⇒ 第 1 轮、round=1
    assert(/点击/.test(out) && rnd === 0,
      `重置后旧换题定时器应作废（提示保持「点击"开始"开始游戏」、round=0）；实际 提示=「${out}」 round=${rnd}`);
  }
  dom.window.close();
}

// ============ FE-N82 / FE-N83 : riddle-generator ============
{
  const html = loadHtml('tools/fun/riddle-generator.html');
  const dom = boot(html, (w) => { w.Math.random = () => 0; }); // 钉死随机 ⇒ 结果确定，暴露「无去重」缺陷
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  const topicEl = w.document.getElementById('topic');
  const res = () => (w.document.getElementById('result').textContent || '').replace(/\s+/g, ' ').trim();
  const face = () => { const m = res().match(/谜面：([^答]*?)(?:分类：|答案：|$)/); return m ? m[1].trim() : ''; };

  // --- N82-a 默认值应为存在的分类（原为不存在的「天气」）---
  assert(topicEl.value === '动物', `默认关键词应为存在的分类「动物」；实际=「${topicEl.value}」`);

  // --- N82-b 未命中应显式提示，而非静默回退 ---
  topicEl.value = '天气';
  w.generate();
  assert(/未命中/.test(res()) && /回退/.test(res()),
    `输入不存在的「天气」应显式提示未命中并说明回退；实际结果=「${res().slice(0, 60)}」`);

  // --- N82-c 关键词应做包含匹配（「动」→ 动物分类），并显示命中数 ---
  topicEl.value = '动';
  w.generate();
  assert(/分类：动物/.test(res()), `关键词「动」应命中「动物」分类；实际结果=「${res().slice(0, 60)}」`);

  // --- N83 同一池内连抽不重复（普通池 2 条）---
  topicEl.value = '普通';
  w.generate();
  const a = face();
  w.generate();
  const b = face();
  assert(a && b && a !== b,
    `普通池（2 条）连抽两次应不重复；实际 第1条=「${a}」 第2条=「${b}」`);

  // --- N83-b 抽完自动循环：第 3 次应回到池内（仍属普通池两条之一）---
  w.generate();
  const c = face();
  assert(c === a || c === b, `抽完 2 条后再抽应循环回到池内；实际 第3条=「${c}」`);

  dom.window.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] N64/N82/N83 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] N64/N82/N83 锁 PASS`);
