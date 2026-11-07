// 两态锁：FE-N78（breakout 位移按时间差归一化，帧率无关）
// 用法：node scripts/_verify_fun_batch_fe_n78.mjs [--head]
// 观测手法：桩 canvas.getContext（记录 arc）读出球位置；桩 requestAnimationFrame 手动逐帧；
//          桩 performance.now 控制帧间隔 —— 无需给页面加任何调试钩子。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const file = 'tools/fun/breakout.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const BALL_R = 6; // 与页面 var BALL_R = 6 对齐

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, downloadText() {}, showError() {}, toggleToolTheme() {} };
    w.i18nText = (k) => String(k);
    w.TBKit = { util: { isEn: () => false }, history: { record() {}, last: () => null, list: () => [], mount() {} }, matrix: { table() {} }, chart: { line() {} }, export: {} };

    w.__arcs = [];
    w.__t = 1000;
    try { Object.defineProperty(w.performance, 'now', { configurable: true, writable: true, value: () => w.__t }); } catch (e) {}

    // canvas 2d 上下文桩：记录 arc 调用（球体半径 === BALL_R 的那次即球心）
    w.HTMLCanvasElement.prototype.getContext = function () {
      const store = {};
      return new Proxy(store, {
        get(t, p) {
          if (p === 'arc') return (x, y, r) => { w.__arcs.push({ x, y, r }); };
          if (p === 'canvas') return null;
          if (p in t) return t[p];
          return () => ({ width: 0, height: 0, addColorStop() {} });
        },
        set(t, p, v) { t[p] = v; return true; }
      });
    };

    // 手动帧驱动：不自动排下一帧，由测试显式调用
    w.requestAnimationFrame = (cb) => { w.__raf = cb; return 1; };
    w.cancelAnimationFrame = () => {};
  }
});

const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);

if (typeof w.startGame !== 'function') {
  console.log('  ✗ startGame 不可见，N78 锁无法判定');
  failures++;
} else {
  w.startGame();                       // 起局：首帧在 __t=1000 执行，lastFrame=1000
  // 发球（keydown ' ' → launchBall）
  w.document.dispatchEvent(new w.KeyboardEvent('keydown', { key: ' ', bubbles: true }));

  const step = (t) => {
    w.__t = t;
    w.__arcs.length = 0;
    w.__raf();                          // 执行一帧 gameLoop
    const ball = w.__arcs.filter(a => Math.abs(a.r - BALL_R) < 1e-6)[0];
    return ball ? ball.y : null;
  };

  const y0 = step(1016.667);            // 帧1：dt=16.667 → k≈1
  const y1 = step(1016.667 + 33.334);   // 帧2：dt=33.334 → k≈2
  const y2 = step(1016.667 + 50.001);   // 帧3：dt=16.667 → k≈1

  if (y0 === null || y1 === null || y2 === null) {
    console.log('  ✗ 未能从 canvas arc 读取球心位置（draw 结构变更？）');
    failures++;
  } else {
    const dBig = Math.abs(y1 - y0);     // 33.334ms 帧的位移
    const dSmall = Math.abs(y2 - y1);   // 16.667ms 帧的位移
    const ratio = dSmall > 1e-9 ? dBig / dSmall : Infinity;
    // 修复版：按时间差归一化 ⇒ 33.3ms 帧位移约为 16.7ms 帧的 2 倍（ratio≈2）
    // HEAD 版：每帧固定位移 ⇒ ratio≈1（高刷屏球速翻倍）
    assert(ratio > 1.5,
      `33.3ms 帧位移应约为 16.7ms 帧的 2 倍（帧率无关）；实际 d(33.3ms)=${dBig.toFixed(2)} d(16.7ms)=${dSmall.toFixed(2)} ratio=${ratio.toFixed(2)}`);
  }
}

dom.window.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] N78 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] N78 锁 PASS`);
