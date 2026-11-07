import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const file = 'tools/music/rhythm-trainer.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');

let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

// ---------- N70: clock source of onTap ----------
// Probe: stub AudioContext.currentTime and performance.now so every access is logged.
// Drive the real flow (startTraining → count-in → isRecording armed → onTap);
// the FIRST clock read inside onTap reveals which time base is used.
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  beforeParse(w) {
    w.__audioTime = 100.5; // AudioContext.currentTime value we control
    w.__clockLog = [];
    class StubAudioCtx {
      constructor() { this.state = 'running'; this.destination = {}; }
      get currentTime() { w.__clockLog.push('audio'); return w.__audioTime; }
      resume() {}
      createOscillator() { return { type:'', frequency:{ setValueAtTime(){} }, connect(){}, start(){}, stop(){} }; }
      createGain() { return { gain:{ setValueAtTime(){}, exponentialRampToValueAtTime(){} }, connect(){} }; }
    }
    w.AudioContext = StubAudioCtx;
    w.webkitAudioContext = StubAudioCtx;
  }
});
const w = dom.window;

// wait for DOMContentLoaded scripts to define globals
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(50);

// patch performance.now (prototype method → own property shadow, keep original for restore)
const patchPerfNow = () => {
  const stub = () => { w.__clockLog.push('perf'); return 5000; }; // performance clock → 5.0 s
  try { Object.defineProperty(w.performance, 'now', { configurable: true, writable: true, value: stub }); }
  catch (e) { try { w.performance.now = stub; } catch (e2) {} }
};
patchPerfNow();

if (typeof w.onTap !== 'function' || typeof w.startTraining !== 'function') {
  console.log('  ✗ window.onTap/startTraining 不可见（脚本结构变更？），N70 锁无法判定');
  failures++;
} else {
  // Shorten count-in to the minimum: BPM caps at 200 → 4 * (60/200) = 1.2s
  const inp = w.document.getElementById('bpmInput');
  if (inp) inp.value = '200';
  if (typeof w.adjustBPM === 'function') w.adjustBPM(0);

  w.startTraining();
  // wait for count-in to arm recording (tapBtn becomes enabled)
  const tapBtn = w.document.getElementById('tapBtn');
  for (let i = 0; i < 40 && tapBtn && tapBtn.disabled; i++) await sleep(100);

  patchPerfNow(); // re-patch in case anything reset it
  w.__clockLog.length = 0;
  w.onTap();
  const first = w.__clockLog[0];
  // 修复版 onTap 首读 AudioContext.currentTime → 'audio'；HEAD 版首读 performance.now → 'perf'
  assert(first === 'audio', `onTap 首读 AudioContext 时钟（与 startTime 同源）；实际首读=${first}${tapBtn && tapBtn.disabled ? '（录音未武装）' : ''}`);
  try { w.stopTraining && w.stopTraining(); } catch (e) {}
}

// ---------- N71: measureNum off-by-one ----------
// Extract the exact 3 computation lines from source and run in isolation.
const srcFor = (s) => {
  const m1 = s.match(/const beatIdx = Math\.floor\(r\.noteIndex \/ subdivision\) \+ 1;/);
  const m2 = s.match(/const measureNum = Math\.floor\((?:\(beatIdx - 1\) \/ 4|beatIdx \/ 4)\) \+ 1;/);
  const m3 = s.match(/const beatInMeasure = \(\(beatIdx - 1\) % 4\) \+ 1;/);
  if (!m1 || !m2 || !m3) return null;
  return m1[0] + '\n' + m2[0] + '\n' + m3[0] + '\nreturn {beatIdx, measureNum, beatInMeasure};';
};
const fnText = srcFor(html);
if (!fnText) {
  console.log('  ✗ 无法抽出 N71 计算行（源码结构变更？）');
  failures++;
} else {
  const run = new Function('r', 'subdivision', fnText);
  // subdivision=1, 第1小节第4拍 → noteIndex=3 → beatIdx=4 → 应落在第1小节
  const res = run({ noteIndex: 3 }, 1);
  // 修复版 measureNum=Math.floor(3/4)+1=1；HEAD 版 Math.floor(4/4)+1=2（错标到下一小节）
  assert(res.measureNum === 1 && res.beatInMeasure === 4,
    `第1小节第4拍应显示「第1小节 第4拍」；实际 第${res.measureNum}小节 第${res.beatInMeasure}拍`);
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] N70/N71 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] N70/N71 锁 PASS`);
process.exit(0);
