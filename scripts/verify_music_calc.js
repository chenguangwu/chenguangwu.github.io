#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "music/audio-converter",
  "inputs": {
    "sr": "66150",
    "bd": "16",
    "ch": "2",
    "dur": "180"
  },
  "expect": [
    "66150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/beat-subdivision",
  "inputs": {
    "bpm": "180",
    "metroBpm": "120",
    "metroAccVol": "80",
    "metroBeatVol": "50",
    "bpmA": "100",
    "bpmB": "140"
  },
  "expect": [
    "666.67ms"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/bpm-converter",
  "inputs": {
    "bpmInput": "120",
    "bpmSlider": "120",
    "reverseMs": "500",
    "sampleRate": "48000"
  },
  "expect": [
    "48000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/chord-notes",
  "inputs": {
    "chordInput": "F#m7"
  },
  "clicks": [
    "analyzeChord()"
  ],
  "expect": [
    "F#m7 · 小七和弦",
    "C# 554.37 Hz 纯五",
    "小七 (10半音)"
  ],
  "ref": "F# 小七和弦 intervals [0,3,7,10]：midi 60+6+0/3/7/10 = 66/69/73/76，midiToFreq 440×2^((n-69)/12) → 369.99/440.00/554.37/659.26 Hz，音级 根音/小三/纯五/小七。原 expect 的 261.63 是默认输入 C 的根音频率（逐字回显默认态、零判别力）。"
},
{
  "slug": "music/chord-progression",
  "inputs": {
    "bpmSlider": "150"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/convert-speed",
  "inputs": {
    "dur": "270",
    "ob": "120",
    "nb": "140"
  },
  "expect": [
    "231.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/ear-trainer",
  "inputs": {},
  "expect": [
    "全部12种"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/freq-note-converter",
  "inputs": {
    "a4Input": "660",
    "freqInput": "440",
    "octaveInput": "4"
  },
  "expect": [
    "440.4972"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/generator-1",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/guitar-fretboard",
  "clicks": [
    "setTuning('drop-d');setScale('A','minor');"
  ],
  "expect": [
    "A 小调： C# D E F# G# A B"
  ],
  "ref": "去默认化（原 expect「10」＝默认标准调弦 C 大调态下的静态串，注入失败仍命中 → 逃生项）：setTuning/setScale 为 window 全局函数，clicks 置 Drop D 调弦 + A 小调后 scaleNotesDisplay 渲染「A 小调： C# D E F# G# A B」；默认 C 大调显示「C 大调： C D E F G A B」，注入失败即不命中。"
},
{
  "slug": "music/music-analysis",
  "inputs": {
    "sample-rate": "66150",
    "bit-depth": "16",
    "channels": "2",
    "duration-sec": "60"
  },
  "expect": [
    "258.40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/music-player",
  "inputs": {
    "volume": "120"
  },
  "expect": [
    "120"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/music-theory",
  "inputs": {
    "scale-type": "minor"
  },
  "expect": [
    "b3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/piano-keyboard",
  "inputs": {},
  "expect": [
    "3UC4AD4SE4DF4FG4GA4HB4JC"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/random-training-rhythm",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "music/rhythm-trainer",
  "inputs": {
    "bpmInput": "140",
    "measureCount": "8"
  },
  "clicks": [
    "adjustBPM(75);startTraining()"
  ],
  "expect": [
    "200",
    "1 2 3 4 5 6 7 8"
  ],
  "ref": "adjustBPM 上界夹取：140+75=215 → Math.max(60,Math.min(200,215)) = 200，写回 bpmInput。startTraining 读 measureCount=8 → renderGrid 渲染 8 个小节标签 1..8。原 expect 的 NaN 是兜底阶段无参调用 adjustBPM() 把 bpmInput 写成 NaN 的副产物（零判别力）；默认态为 90+75=165 且 measureCount 回落首个 option=2（网格仅 1 2），两锚点均失配。注：startTraining 在 renderGrid() 之后才因缺 AudioContext 抛错，网格已渲染，断言不受影响。"
},
{
  "slug": "music/sheet-music",
  "clicks": [
    "setKey('G');"
  ],
  "expect": [
    "1 G 2 A 3 B 4 C↑ 5 D↑ 6 E↑ 7 F#↑ 1 G↑"
  ],
  "ref": "弱用例去默认化（BATCH118）：**推翻旧 ref「结构性不可注入」** —— setKey(k) 可经 clicks 直调，无需模拟 innerHTML 生成的 span 点击。原锚默认 C 大调调号条/唱名条；改 setKey('G') 后锚 G 大调音阶「1 G 2 A 3 B 4 C↑ 5 D↑ 6 E↑ 7 F#↑ 1 G↑」（↑ 八度标记随 offset 递变，与默认 C「1 C…1 C↑」逐串区分）。**注意**：单锚「G」不可用 —— 调号条恒列出全部 15 个调名（默认态必命中）；必须锚完整唱名复合串。清 clicks 兜底遍历不产出 ⇒ 零逃生项。"
},
{
  "slug": "music/web-tuner",
  "inputs": {
    "refFreq": "440"
  },
  "expect": [
    "440"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== music calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
