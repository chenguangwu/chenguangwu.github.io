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
  "ref": "auto-restore(default)；**2026-09-26 复核判死（勿重复评估）**：① 当前 expect「全部12种」是难度按钮（困难）的常驻文本，默认态必命中 ⇒ 判别力 0；② `window.setMode('chord')` 实测抛错（EarTrainer.setMode 里 `document.querySelectorAll('.mode-tab')[1].classList.add('active')`，harness DOM 中 `.mode-tab` 不足 2 个）⇒ 抛错点之后的 renderRefTable() 根本没执行；③ 可达的 `window.setDifficulty('hard')` 只写 state + renderDifficulty()（纯 class 切换）+ generateQuestion()，**不产生任何新文本**。 ⇒ 无可用注入通道。"
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
  "clicks": ["changeOctave(2);"],
  "expect": [
    "C5AD5SE5DF5FG5GA5HB5JC#5WD#5EF#5TG#5YA#5U"
  ],
  "ref": "独立复算：默认 currentOctave=3，changeOctave(+2) 抬到 5（钳制区间 1–7 内），renderPiano() 按 2 个八度重绘，白/黑键标签由 NOTE_NAMES[n]+octave 拼出 ⇒ C5…B5、C6…B6 连续整串，同帧 #octaveDisplay 由 3 变 5。锚取整条标签行 —— 旧锚「3UC4AD4S…」本身就是默认态产物、判别力为 0。"
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
},
  {
    slug: "music/bpm-converter",
    inputs: { reverseMs: "600" },
    expect: ["100.00 BPM"],
    ref: '独立复算：反向计算 时长(ms)→BPM，四分音符 div=1，BPM=60000×1/600=100.00。注入 reverseMs=600 触发 calcReverse()，reverseResult 显示「100.00 BPM」。默认态 reverseMs=500→120.00 BPM，不命中；全页仅 reverseResult 区含「BPM」数字格式。'
  },
  {
    slug: "music/bpm-converter",
    inputs: { reverseMs: "300" },
    expect: ["200.00 BPM"],
    ref: '独立复算：BPM=60000/300=200.00。注入 reverseMs=300。默认态 120.00 BPM，不命中。'
  },
  {
    slug: "music/bpm-converter",
    inputs: { reverseMs: "400" },
    expect: ["150.00 BPM"],
    ref: '独立复算：BPM=60000/400=150.00。注入 reverseMs=400。默认态 120.00 BPM，不命中。'
  },
  {
    slug: "music/bpm-converter",
    inputs: { reverseMs: "1000" },
    expect: ["60.00 BPM"],
    ref: '独立复算：BPM=60000/1000=60.00。注入 reverseMs=1000。默认态 120.00 BPM，不命中。'
  },
  {
    slug: "music/bpm-converter",
    inputs: { reverseMs: "750" },
    expect: ["80.00 BPM"],
    ref: '独立复算：BPM=60000/750=80.00。注入 reverseMs=750。默认态 120.00 BPM，不命中。'
  },
  {
    slug: "music/bpm-converter",
    inputs: { reverseMs: "1500" },
    expect: ["40.00 BPM"],
    ref: '独立复算：BPM=60000/1500=40.00（达 bpm 下限 40）。注入 reverseMs=1500。默认态 120.00 BPM，不命中。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { freqInput: "220" },
    clicks: ["calcFreq2Note()"],
    expect: ["A3 220.0000 Hz"],
    ref: '独立复算：midi=69+12·log2(220/440)=57→A3，exactFreq=440×2^((57-69)/12)=220.0000。锚取完整 result 名+四位小数频率串（含派生值），默认态 freq2note=A4 440.0000 不命中、参考表为 toFixed(1) 不命中。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { freqInput: "880" },
    clicks: ["calcFreq2Note()"],
    expect: ["A5 880.0000 Hz"],
    ref: '独立复算：midi=69+12·log2(880/440)=81→A5，exactFreq=440×2^((81-69)/12)=880.0000。锚 \'A5 880.0000 Hz\' 默认态无。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { freqInput: "330" },
    clicks: ["calcFreq2Note()"],
    expect: ["E4 329.6276 Hz"],
    ref: '独立复算：midi=69+12·log2(330/440)=64.02→round 64→E4，exactFreq=440×2^((64-69)/12)=329.6276（含入尾数，dump 实测非手算）。锚唯一。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { freqInput: "246.94" },
    clicks: ["calcFreq2Note()"],
    expect: ["B3 246.9417 Hz"],
    ref: '独立复算：midi=69+12·log2(246.94/440)=59.0→B3，exactFreq=440×2^((59-69)/12)=246.9417。锚唯一。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { freqInput: "261.63" },
    clicks: ["calcFreq2Note()"],
    expect: ["C4 261.6256 Hz"],
    ref: '独立复算：midi=69+12·log2(261.63/440)=60.0→C4（中央 C），exactFreq=440×2^((60-69)/12)=261.6256。锚唯一。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { freqInput: "174.61" },
    clicks: ["calcFreq2Note()"],
    expect: ["F3 174.6141 Hz"],
    ref: '独立复算：midi=69+12·log2(174.61/440)=53.0→F3，exactFreq=440×2^((53-69)/12)=174.6141。锚唯一。注：音符→频率方向因 harness 注入 octaveInput(number) 后 read 为 NaN 不兼容，本批仅加固频率→音符方向。'
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "180", ob: "120", nb: "180" },
    clicks: ["calc()"],
    expect: ["变速比 ×1.5000"],
    ref: '180s/120BPM→180BPM 变速比1.5000 提速50% 目标时长120s'
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "180", ob: "120", nb: "80" },
    clicks: ["calc()"],
    expect: ["变速比 ×0.6667"],
    ref: '180s/120BPM→80BPM 变速比0.6667 提速-33% 目标时长270s'
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "180", ob: "100", nb: "125" },
    clicks: ["calc()"],
    expect: ["变速比 ×1.2500"],
    ref: '180s/100BPM→125BPM 变速比1.2500 提速25% 目标时长144s'
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "180", ob: "200", nb: "100" },
    clicks: ["calc()"],
    expect: ["变速比 ×0.5000"],
    ref: '180s/200BPM→100BPM 变速比0.5000 提速-50% 目标时长360s'
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "180", ob: "100", nb: "200" },
    clicks: ["calc()"],
    expect: ["变速比 ×2.0000"],
    ref: '180s/100BPM→200BPM 变速比2.0000 提速100% 目标时长90s'
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "180", ob: "144", nb: "120" },
    clicks: ["calc()"],
    expect: ["变速比 ×0.8333"],
    ref: '180s/144BPM→120BPM 变速比0.8333 提速-17% 目标时长216s'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "8000", bd: "16", ch: "1", dur: "60" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 0.92 MB"],
    ref: '8000/16/1/60s 电话级单声道 0.92MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "44100", bd: "16", ch: "2", dur: "300" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 50.47 MB"],
    ref: '44100/16/2/300s CD音质5分钟 50.47MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "48000", bd: "24", ch: "2", dur: "120" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 32.96 MB"],
    ref: '48000/24/2/120s 专业录音2分钟 32.96MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "96000", bd: "16", ch: "2", dur: "60" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 21.97 MB"],
    ref: '96000/16/2/60s 高清1分钟 21.97MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "22050", bd: "8", ch: "1", dur: "180" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 3.79 MB"],
    ref: '22050/8/1/180s AM广播单声道3分钟 3.79MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "192000", bd: "32", ch: "2", dur: "30" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 43.95 MB"],
    ref: '192000/32/2/30s 母带30秒 43.95MB'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "60", timeSig: "4/4" },
    clicks: ["calculate()"],
    expect: ["拍号 4/4 | 小节时长 4.00s"],
    ref: '60BPM/4/4 小节时长4.00s'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "60", timeSig: "3/4" },
    clicks: ["calculate()"],
    expect: ["拍号 3/4 | 小节时长 3.00s"],
    ref: '60BPM/3/4 小节时长3.00s'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "240", timeSig: "4/4" },
    clicks: ["calculate()"],
    expect: ["拍号 4/4 | 小节时长 1.00s"],
    ref: '240BPM/4/4 小节时长1.00s'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "90", timeSig: "2/4" },
    clicks: ["calculate()"],
    expect: ["拍号 2/4 | 小节时长 1.33s"],
    ref: '90BPM/2/4 小节时长1.33s'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "75", timeSig: "6/8" },
    clicks: ["calculate()"],
    expect: ["拍号 6/8 | 小节时长 2.40s"],
    ref: '75BPM/6/8 小节时长2.40s'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "100", timeSig: "3/4" },
    clicks: ["calculate()"],
    expect: ["拍号 3/4 | 小节时长 1.80s"],
    ref: '100BPM/3/4 小节时长1.80s'
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
