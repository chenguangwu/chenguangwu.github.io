#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs=require("fs"), path=require("path");
function musicStaticChecks(){
  const read=(p)=>fs.readFileSync(path.join(__dirname,"..","tools","music",p),"utf8");
  const cp=read("chord-progression.html"), cn=read("chord-notes.html"), mt=read("music-theory.html"), gt=read("guitar-fretboard.html"), wt=read("web-tuner.html"), bs=read("beat-subdivision.html"), fq=read("freq-note-converter.html"), sp=read("convert-speed.html"), dt=read("detector.html"), ac=read("audio-converter.html"), ma=read("music-analysis.html"), mp=read("music-player.html"), et=read("ear-trainer.html"), rt=read("rhythm-trainer.html"), rr=read("random-training-rhythm.html"), pk=read("piano-keyboard.html"), sg=read("generator-1.html"), bp=read("bpm-converter.html");
  return [
    {name:"和弦进行降E映射、悲怆四级与大调高频",ok:/'Eb':3/.test(cp)&&!/'Eb':2/.test(cp)&&/qualities:\s*\['',\s*'m',\s*'',\s*'m'\]/.test(cp)&&/48 \+ chordRoot/.test(cp)&&/spellChordNote\(rootName/.test(cp)},
    {name:"和弦进行停止清理全部高亮定时器",ok:/highlightTimeouts/.test(cp)&&/highlightTimeouts\.forEach/.test(cp)&&/if \(isPlaying\) highlightChord/.test(cp)},
    {name:"和弦音符按音级拼写并修正A大三示例",ok:/spellFromRoot/.test(cn)&&/A C♯ E/.test(cn)&&!/A、A\+4\(半音\)=C、/.test(cn)},
    {name:"乐理小调与复音程按音级拼写",ok:/SCALE_STEPS/.test(mt)&&/stepOverride/.test(mt)&&/intervalName\(iv\)/.test(mt)&&/14:'9'/.test(mt)},
    {name:"吉他小调音阶与降号拼写",ok:/minor': \[0,2,3,5,7,8,10\]/.test(gt)&&/spellChordNote|calcScaleNotes/.test(gt)&&/NOTE_NAMES_FLAT/.test(gt)},
    {name:"调音器错误区分与目标随参考音刷新",ok:/PermissionDeniedError/.test(wt)&&/DevicesNotFoundError|NotFoundError/.test(wt)&&/targetBaseFreq \* refA4 \/ 440/.test(wt)&&/Microphone permission denied/.test(wt)&&/No microphone detected/.test(wt)&&!/global\.ToolBox/.test(wt)},
    {name:"节拍细分严格BPM、7/8分组与整小节格数",ok:/function readBpm/.test(bs)&&/readBpm\('bpm', 1, 999\)/.test(bs)&&/getMeterGroups/.test(bs)&&/group7/.test(bs)&&/共 \$\{cells\} 个细分格子/.test(bs)},
    {name:"节拍器播放中实时读取参数",ok:/function metroSettings/.test(bs)&&/readBpm\('metroBpm', 20, 300\)/.test(bs)&&/st\.interval/.test(bs)&&/setTimeout\(metroTick/.test(bs)&&!/setInterval\(\s*\(\) => \{\s*scheduleClick/.test(bs)},
    {name:"音符转频率八度整数与试听范围",ok:/octaveValid/.test(fq)&&/Math\.floor\(octave\) === octave/.test(fq)&&/canAudition/.test(fq)&&/AUDIBLE_MIN/.test(fq)&&!/Math\.max\(20, Math\.min\(freq, 20000\)/.test(fq)},
    {name:"变速比例与相对变化分开标注",ok:/目标速度占原速比例/.test(sp)&&/相对变化/.test(sp)&&/__ratio/.test(sp)},
    {name:"节拍检测新一轮清空旧结果",ok:/function clearResult/.test(dt)&&/updateDisplay[\s\S]{0,200}clearResult\(\)/.test(dt)&&/resetBPM[\s\S]{0,300}clearResult\(\)/.test(dt)},
    {name:"音频格式十进制容量与英文免责",ok:/totalBytes \/ 1e6/.test(ac)&&/320 \* 1000 \* dur \/ 8 \/ 1e6/.test(ac)&&/no upload or transcoding/.test(ac)&&!/Convert audio files between common formats/.test(ac)},
    {name:"音频分析容量十进制与统计清空",ok:/totalBytes \/ 1e6/.test(ma)&&/function clearStats/.test(ma)&&/clearStats\(\)/.test(ma)&&/bytesPerSec \/ 1000/.test(ma)},
    {name:"播放器按实际加入数反馈并跳过非音频",ok:/function isAudioFile/.test(mp)&&/const added = \[\]/.test(mp)&&/skipped\+\+/.test(mp)&&/已添加 \$\{added\.length\} 首，跳过 \$\{skipped\}/.test(mp)&&!/已添加 \$\{files\.length\} 首歌曲/.test(mp)},
    {name:"播放器 Promise/事件同步状态并修正历史索引",ok:/function attemptPlay/.test(mp)&&/p\.then\(\(\) => \{ updatePlayUI\(true\)/.test(mp)&&/showPlayError\(\); return false;/.test(mp)&&/audio\.addEventListener\('error'/.test(mp)&&/__tbHistSave\(\{时间:__tbTime\(\),曲目:t\.name/.test(mp)&&!/var t=playlist\[i\]/.test(mp)},
    {name:"听力训练播放方式用 data-style 选中",ok:/data-style="simultaneous"/.test(et)&&/data-style="arpeggio"/.test(et)&&/getAttribute\('data-style'\) === style/.test(et)&&!/textContent\.indexOf\(style/.test(et)},
    {name:"听力训练动态文案按语言生成",ok:/function intervalName/.test(et)&&/function chordName/.test(et)&&/L\('Easy \(4 intervals\)'/.test(et)&&/L\('Correct answer: '/.test(et)&&/L\('Correct!/.test(et)&&/L\('Wrong answer'/.test(et)&&/refreshLanguageUI/.test(et)},
    {name:"听力训练切题停止旧振荡器与定时器",ok:/function stopCurrentSound/.test(et)&&/activeOscs\.forEach/.test(et)&&/playTimers\.forEach/.test(et)&&/function generateQuestion\(\) \{\n    stopCurrentSound\(\)/.test(et)&&/if \(token === playToken\)/.test(et)},
    {name:"节奏训练额外点击计入分母并展示",ok:/extraTapIndices/.test(rt)&&/scoredUnits = results\.length \+ extraCount/.test(rt)&&/totalScore \/ scoredUnits/.test(rt)&&/Extra taps/.test(rt)&&/额外点击/.test(rt)},
    {name:"跟拍训练空值与越界拒绝启动",ok:/function readInt\(id, min, max\)/.test(rr)&&/Number\.isInteger\(n\) && n >= min && n <= max/.test(rr)&&/bpm === null \|\| sub === null \|\| bars === null/.test(rr)&&!/parseInt\(document\.getElementById\('tapBpm'\)\.value\)\|\|100/.test(rr)&&!/bpm=Math\.max\(40,Math\.min\(200,bpm\)\)/.test(rr)},
    {name:"钢琴键盘失焦/隐藏停止全部音符",ok:/window\.addEventListener\('blur', function\(\) \{\n    stopAllNotes\(\);/.test(pk)&&/document\.addEventListener\('visibilitychange'/.test(pk)&&/if \(document\.hidden\) stopAllNotes\(\)/.test(pk)&&/window\.addEventListener\('pagehide'/.test(pk)},
    {name:"音阶生成指定调性/正确拼写/试听键盘",ok:/function spellPitch/.test(sg)&&/const ROOTS = \[/.test(sg)&&/function buildScale/.test(sg)&&/function renderKeyboard/.test(sg)&&/function playScale/.test(sg)&&/随机练习/.test(sg)&&!/一律随机生成/.test(sg)},
    {name:"BPM 主/反向均须有效才记录导出",ok:/function __bpm_converterMainValid/.test(bp)&&/function __bpm_converterReverseValid/.test(bp)&&/if\(!mainOk \|\| !reverseOk\)/.test(bp)&&/if\(!reverseOk\)\{ delete snap\.reverseMs/.test(bp)&&/!__bpm_converterMainValid\(\) \|\| !__bpm_converterReverseValid\(\)/.test(bp)&&!/if\(!Number\.isFinite\(ms\) \|\| ms<=0\)\{\n        ToolBox\.showToast\('请先输入有效的时长值'\)/.test(bp)}
  ];
}
const CASES = [
{
    "slug": "music/ear-trainer",
    "clicks": ["var __oq=document.querySelectorAll;document.querySelectorAll=function(){return [{classList:{remove:function(){},add:function(){}}},{classList:{remove:function(){},add:function(){}}}];};EarTrainer.setMode('chord');document.querySelectorAll=__oq;var h=String(document.getElementById('refContent').innerHTML);var ok=(h.indexOf('C E-G')>=0&&h.indexOf('C E♭-G')>=0&&h.indexOf('C E-G♯')>=0&&h.indexOf('C E♭-G♭')>=0&&h.indexOf('A♭')<0&&h.indexOf('F#')<0);document.getElementById('__tbProbe').textContent='CHORDREF '+(ok?'OK':'BAD');"],
    "expect": ["CHORDREF OK"],
    "ref": "复核失败重做·FE-N39 和弦音级拼写：C 增三和弦（增三度叠增三度）应写 C E G♯，减三和弦（减三度叠减三度）应写 C E♭ G♭；旧实现把 CHORDS.intervals 直接喂给音程语境的 DEGREE_SPELL，得 C E A♭ / C E♭ F#。修复后 CHORDS 各带按音级 spell 字段、参考表用 ch.spell。用例切 chord 模式走真实 renderRefTable，断言四种和弦拼写齐全且旧的等音写法不再出现；修复前 BAD。默认态无探针串 ⇒ 零逃生。"
  },
{
    "slug": "music/ear-trainer",
    "clicks": ["var __oq=document.querySelectorAll;document.querySelectorAll=function(){return [{classList:{remove:function(){},add:function(){}}},{classList:{remove:function(){},add:function(){}}}];};EarTrainer.setMode('chord');document.querySelectorAll=__oq;var h=String(document.getElementById('refContent').innerHTML);var rows=[];var re=/<tr><td><strong>([^<]*)<\\/strong><\\/td><td>([^<]*)<\\/td><td>([^<]*)<\\/td><td>([^<]*)<\\/td><\\/tr>/g;var m;while((m=re.exec(h))){rows.push([m[1],m[2],m[3],m[4]]);}var __tbl={querySelectorAll:function(){return rows.map(function(r){return {querySelectorAll:function(){return r.map(function(c){return {textContent:c};});}};});}};var __hidden={innerHTML:'',appendChild:function(el){this.innerHTML+=String(el.innerHTML||'')+'|';}};var __oqs=document.querySelector;document.querySelector=function(s){if(s==='#refContent table tbody')return __tbl;if(s==='#earHidden tbody')return __hidden;return __oqs(s);};var __or=__earRow;__earRow=function(cells){return {innerHTML:cells.join('|')};};TBKit={util:{isEn:function(){return false;},exportTable:function(){}}};__earExport();document.querySelector=__oqs;__earRow=__or;document.getElementById('__tbProbe').textContent='EARCSV '+(__hidden.innerHTML.indexOf('G♯')>=0&&__hidden.innerHTML.indexOf('G♭')>=0?'OK':'BAD');"],
    "expect": ["EARCSV OK"],
    "ref": "复核失败重做·FE-N39 CSV 同步：__earExport() 直接复制 #refContent 参考表四列进 #earHidden 再导出；参考表按音级拼写修好后 CSV 同步为 G♯/G♭。用例以真实参考表行喂 __earExport、stub 中间 DOM，断言导出内容含 G♯/G♭；修复前参考表是 A♭/F# ⇒ BAD。默认态无探针串 ⇒ 零逃生。"
  },
{
  "slug": "music/audio-converter",
  "inputs": {
    "sr": "66150",
    "bd": "16",
    "ch": "2",
    "dur": "180"
  },
  "expect": [ "47.63 MB" ],
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
    "180 BPM — Presto（急板） | 拍号 4/4 | 小节时长 1.33s",
    "180 BPM",
    "333.3",
    "1333.33",
    "共 4 个细分格子",
    "拍号 4/4，每格 333.33ms",
    "BPM 100 时长(ms)"
  ],
  "ref": "默认参数整页回归：180 BPM 四分音符 333.33ms、全音符 1333.33ms、4/4 共 4 格；对比表含 BPM 100/140。可视化改为整小节格子后锚「共 4 个细分格子」，不再使用旧「拍1 拍2…」逐拍串。"
},
{
  "slug": "music/bpm-converter",
  "inputs": {
    "bpmInput": "120",
    "bpmSlider": "120",
    "reverseMs": "500",
    "sampleRate": "48000"
  },
  "expect": [ "96,000 一小节" ],
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
// 已移除 music/ear-trainer（inputs:{}，expect ["全部12种"]）。
// 原因：该锚是难度按钮（困难）常驻文本，默认态必命中 ⇒ 判别力 0；且复核确认无可用注入通道
// （setMode('chord') 在 harness DOM 抛错、可达的 setDifficulty('hard') 不产生新文本），
// 无法改出可判别锚 ⇒ 按纪律删除而非保留 skip。
{
  "slug": "music/freq-note-converter",
  "inputs": {
    "a4Input": "660",
    "freqInput": "440",
    "octaveInput": "4"
  },
  "expect": [
    "D4 440.4972 Hz",
    "最接近 D4"
  ],
  "ref": "注入 A4 参考 660 Hz（默认 440）+ 频率 440。以 A4=660 为基准时 440 Hz 最接近 D4：D4 = 660 × 2^(-7/12) = 440.4972 Hz，音分偏差 -2.0 cents。默认 A4=440 时 440 Hz 即 A4（440.0000 Hz）⇒ 两条均不命中独立复算值。⚠ 原 expect 只取裸数值『440.4972』，在判别器连续运行（前序用例残留 + 参考表全量渲染）下会在默认态命中 ⇒ 逃生项；改为带音名的合成串后判别力成立。"
},
{
  "slug": "music/generator-1",
  "inputs": {},
  "clicks": ["var r=buildScale(ROOTS[5],SCALES[0],4);var n=r.notes.map(function(x){return x.name;}).join(' ');document.getElementById('__tbProbe').textContent='SCALE '+n+' '+r.notes[3].freq.toFixed(2);"],
  "expect": ["SCALE F4 G4 A4 B♭4 C5 D5 E5 466.16"],
  "ref": "直接调用 buildScale 校验 F 大调：第四级按音级拼成 B♭（不是 A♯），跨 C 音级的 C5/D5/E5 八度正确，频率 466.16 Hz。旧实现只随机根音与调式且一律升号，无 buildScale ⇒ 无探针串。"
},
{
  "slug": "music/generator-1",
  "inputs": {},
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/music/generator-1.html','utf8');var ok=h.indexOf('随机数量需为 1–50 的整数')>=0&&h.indexOf('Number.isInteger(n)')>=0&&h.indexOf('n<1||n>50')>=0;document.getElementById('__tbProbe').textContent='GENEMPTY '+(ok?'OK':'BAD');"],
  "expect": ["GENEMPTY OK"],
  "ref": "随机练习模式的数量必须为非空 1–50 整数；源码守卫空串/非整数/越界统一报「随机数量需为 1–50 的整数」。旧实现无随机数量输入与校验 ⇒ 无探针串。"
},
{
  "slug": "music/guitar-fretboard",
  "clicks": [
    "setTuning('drop-d');setScale('A','minor');"
  ],
  "expect": [
    "A 小调： A B C D E F G"
  ],
  "ref": "A 小调自然音阶应为 A B C D E F G；旧实现用相对大调偏移叠加根音，输出 C# D E F# G# A B，属把 A 小调当 A 大调。"
},
{
  "slug": "music/guitar-fretboard",
  "clicks": [
    "setTuning('standard');setScale('C','minor');"
  ],
  "expect": [
    "C 小调： C D Eb F G Ab Bb"
  ],
  "ref": "C 自然小调应按调号拼成 C D Eb F G Ab Bb；旧实现根音错位成 A B C D E F G，且固定升号无法拼出降号音。"
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
    "264.60"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
  "slug": "music/random-training-rhythm",
  "inputs": { "cnt": "" },
  "expect": ["请输入生成数量"],
  "ref": "FE-N73 复核重做：清空生成数量（空值）后，旧实现 `value||5` 把空当 0→5 生成 5 题；现空值直接提示「请输入生成数量」并 return。默认 cnt=5 生成 5 题不含该提示 ⇒ 强判别、零逃生。"
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
    "refFreq": "442"
  },
  "expect": [
    "442"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
    expect: ["输入频率： 261.63 Hz", "最接近 C4"],
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
    expect: ["PCM 原始大小: 0.96 MB"],
    ref: '8000/16/1/60s 电话级单声道 0.92MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "44100", bd: "16", ch: "2", dur: "300" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 52.92 MB"],
    ref: '44100/16/2/300s CD音质5分钟 50.47MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "48000", bd: "24", ch: "2", dur: "120" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 34.56 MB"],
    ref: '48000/24/2/120s 专业录音2分钟 32.96MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "96000", bd: "16", ch: "2", dur: "60" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 23.04 MB"],
    ref: '96000/16/2/60s 高清1分钟 21.97MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "22050", bd: "8", ch: "1", dur: "180" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 3.97 MB"],
    ref: '22050/8/1/180s AM广播单声道3分钟 3.79MB'
  },
  {
    slug: "music/audio-converter",
    inputs: { sr: "192000", bd: "32", ch: "2", dur: "30" },
    clicks: ["calcPCM()"],
    expect: ["PCM 原始大小: 46.08 MB"],
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
    expect: ["拍号 6/8（分组 3+3 八分） | 小节时长 2.40s"],
    ref: '75BPM/6/8 小节时长2.40s'
  },
  {
    slug: "music/beat-subdivision",
    inputs: { bpm: "100", timeSig: "3/4" },
    clicks: ["calculate()"],
    expect: ["拍号 3/4 | 小节时长 1.80s"],
    ref: '100BPM/3/4 小节时长1.80s'
  },
  {
    slug: "music/web-tuner",
    inputs: { refFreq: "432" },
    clicks: ["window.__wtSetRefA4(+document.getElementById('refFreq').value);var n=window.__wtFreqToNote(440);document.getElementById('centsText').textContent='C:'+n.cents.toFixed(2)+'|N:'+n.full;"],
    expect: ["C:31.77|N:A4"],
    ref: '深度解析算例复算：A4=432 时 440 Hz → midiFloat=69+12·log2(440/432)=69.3177，音分 +31.77，仍判 A4。默认基准 440 下同一频率为 0.00 ⇒ 不命中。'
  },
  {
    slug: "music/web-tuner",
    inputs: { refFreq: "440" },
    clicks: ["window.__wtSetRefA4(+document.getElementById('refFreq').value);var n=window.__wtFreqToNote(446);document.getElementById('centsText').textContent='C:'+n.cents.toFixed(2)+'|N:'+n.full;"],
    expect: ["C:23.45|N:A4"],
    ref: '深度解析算例一复算：A4=440 时 446 Hz → midiFloat=69.2345，音分 +23.45，仍判 A4。默认态 centsText 为空、不含该串 ⇒ 不命中。'
  },
  {
    slug: "music/web-tuner",
    inputs: { refFreq: "440" },
    clicks: ["setTarget({classList:{contains:function(){return false;},add:function(){},remove:function(){}},dataset:{freq:'82.41'},textContent:'E2'});window.__wtRenderTarget(82.41);"],
    expect: ["目标 E2（82.41 Hz）｜当前距目标 0.0 音分（已对准（±5 音分内））"],
    ref: '第1064批：弦按钮不再只是高亮。点击首个 E2 按钮后 targetFreq=82.41；对 82.41 Hz 计算 1200·log2(f/82.41)=0，输出「距目标 0.0 音分（已对准）」。默认 targetFreq=0、targetText 只有「点击上方弦名可开启目标弦对照」，锚不命中。'
  },
  {
    slug: "music/freq-note-converter",
    inputs: { a4Input: "", freqInput: "440" },
    clicks: ["var e=document.getElementById('a4Input');e.value='';finishA4Edit();document.getElementById('freq2note').textContent='A4EDIT '+(+e.value===440?'OK':'BAD');"],
    expect: ["A4EDIT OK"],
    ref: "第1065批：A4 自定义输入清空/越界时，失焦必须恢复标准 440 Hz，不能输入框空白而内部仍沿用旧参考频率。空值触发 finishA4Edit 后 a4Input 回填 440；默认态输入框本就是 440、探针串不存在 ⇒ 锚不逃生。"
  },


{
  "slug": "music/chord-notes",
  "clicks": ["document.getElementById('chordInput').value='Bb';analyzeChord();document.getElementById('__tbProbe').textContent=document.getElementById('notesDisplay').innerText;"],
  "expect": ["Bb", "D", "F"],
  "ref": "Bb 大三和弦应为 Bb-D-F；旧实现把根音转成 A# 并显示 A# D F。"
},
{
  "slug": "music/chord-notes",
  "clicks": ["document.getElementById('chordInput').value='Cdim';analyzeChord();document.getElementById('__tbProbe').textContent=document.getElementById('notesDisplay').innerText;"],
  "expect": ["C", "E♭", "G♭"],
  "ref": "C 减三和弦应按音级拼成 C-E♭-G♭，不得写成 C-D#-F#。"
},
{
  "slug": "music/chord-notes",
  "clicks": ["document.getElementById('chordInput').value='Cdim7';analyzeChord();document.getElementById('__tbProbe').textContent=document.getElementById('notesDisplay').innerText+'|'+document.getElementById('intervalInfo').innerText;"],
  "expect": ["Bbb", "减七"],
  "ref": "Cdim7 的第四音是减七度（Bbb），不是大六度（A）；旧实现按半音数把 9 半音映射成六度 ⇒ 显示 A/大六。默认 C 大三和弦不含 Bbb/减七 ⇒ 零逃生。"
},
{
  "slug": "music/music-theory",
  "clicks": ["setRoot(0);document.getElementById('scale-type').value='minor';renderScale();document.getElementById('__tbProbe').textContent=document.getElementById('scale-display').innerText;"],
  "expect": ["C - D - Eb - F - G - Ab - Bb"],
  "ref": "C 自然小调必须按音级拼写 C-D-E♭-F-G-A♭-B♭；旧实现固定升号，显示 D#/G#/A#。"
},
{
  "slug": "music/music-theory",
  "clicks": ["setRoot(0);document.getElementById('chord-type').value='add9';renderChord();document.getElementById('__tbProbe').textContent=document.getElementById('chord-display').innerText;"],
  "expect": ["Cadd9", "D", "9"],
  "ref": "Cadd9 的九音应拼作 D 且音程标注 9，不得把 +14 半音标成 2。"
}
,
{
  "slug": "music/web-tuner",
  "inputs": { "refFreq": "440" },
  "clicks": ["var f=document.getElementById('refFreq');setTarget({classList:{contains:function(){return false;},add:function(){},remove:function(){}},dataset:{freq:'82.41'},textContent:'E2'});window.__wtSetRefA4(432);window.__wtRenderTarget(80.91);"],
  "expect": ["目标 E2（80.91 Hz）｜当前距目标 0.0 音分"],
  "ref": "A4 改为 432 后，E2=82.41×432/440=80.91 Hz；目标弦必须随参考音刷新，旧实现始终用 440 基准的 82.41 Hz，选 432 后偏差约 31.8 音分。"
},
{
  "slug": "music/web-tuner",
  "inputs": { "refFreq": "440" },
  "clicks": ["try{copyTunerReading();document.getElementById('centsText').textContent='COPY OK';}catch(e){document.getElementById('centsText').textContent='COPY ERR:'+e.name;}"],
  "expect": ["COPY OK"],
  "ref": "无有效读数时 copyTunerReading 必须安全返回并提示，不得因访问浏览器不存在的 global 抛 ReferenceError。默认 noteName 为「--」即进入空读数分支。"
}
,
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "" },
  "clicks": ["calculate()"],
  "expect": ["请输入 1–999 之间的有效 BPM", "BPM 无效，已清除计算结果"],
  "ref": "清空 BPM 必须报错并清空结果，不得静默回退 120 BPM；默认 120 不出现该提示，旧实现 `parseFloat||120` 会继续输出 500ms 结果。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "0" },
  "clicks": ["calculate()"],
  "expect": ["请输入 1–999 之间的有效 BPM"],
  "ref": "BPM=0 属越界，不得被当作未填写回退默认 120；页面标注范围 1–999。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "-20" },
  "clicks": ["calculate()"],
  "expect": ["请输入 1–999 之间的有效 BPM"],
  "ref": "负数 BPM 必须拒绝，旧实现会输出负时长。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "120", "timeSig": "7/8" },
  "clicks": ["document.getElementById('group7').value='2+2+3';calculate();"],
  "expect": ["拍号 7/8（分组 2+2+3 八分）", "每小节组数", "共 7 个细分格子"],
  "ref": "7/8 不能再按 7/3=2.333 拍处理；2+2+3 分组应显示 3 组、7 个八分格，且每格 125ms（120BPM 八分音符 250ms？7/8 小节 7×250ms=1750ms，7 格）。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "120", "timeSig": "7/8" },
  "clicks": ["document.getElementById('group7').value='3+2+2';calculate();"],
  "expect": ["拍号 7/8（分组 3+2+2 八分）", "组1（3八分）", "组2（2八分）"],
  "ref": "切换 7/8 分组后标签与重音分组必须同步为 3+2+2，不能仍显示固定 2+2+3。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "120", "timeSig": "4/4" },
  "clicks": ["document.getElementById('vizDivision').value='whole';calculate();"],
  "expect": ["共 1 个细分格子", "每格 2000.00ms"],
  "ref": "4/4 全音符跨 4 拍，整小节应只有 1 格（2000ms）；旧实现按每拍系数渲染出 4 个空格子。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "120", "timeSig": "6/8" },
  "clicks": ["document.getElementById('vizDivision').value='quarter';calculate();"],
  "expect": ["共 3 个细分格子", "每格 500.00ms"],
  "ref": "6/8 小节 1500ms，四分音符 500ms → 3 格；旧实现按 2 拍×1 渲染 2 格且时长口径不一致。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpm": "120", "timeSig": "6/8", "metroBpm": "120" },
  "clicks": ["selectNoteType('eighth');document.getElementById('vizDivision').value='eighth';calculate();var a=__bsMetroInfo();document.getElementById('metroBpm').value='240';var b=__bsMetroInfo();document.getElementById('bpm').value='240';document.getElementById('metroBpm').value='240';document.getElementById('timeSig').value='4/4';var c=__bsMetroInfo();document.getElementById('tempoLabel').textContent='M|'+a+'|'+b+'|'+c;"],
  "expect": ["M|120|6|250.00|0.0,750.0", "|240|6|125.00|"],
  "ref": "6/8 八分细分每小节 6 格，120BPM 间隔 250ms；把节拍器 BPM 改为 240 后同一函数立即返回 125ms，证明参数在播放中实时读取而非启动时捕获；切到 4/4 后组边界变为 0/250/500/750。"
},
{
  "slug": "music/beat-subdivision",
  "inputs": { "bpmA": "", "bpmB": "140" },
  "clicks": ["compareBPM()"],
  "expect": ["BPM A 与 BPM B 都需填写 1–999 之间的有效数字"],
  "ref": "BPM 对比清空任一侧必须报错，不得用 100/140 默认值继续输出对比表。"
}
,
{
  "slug": "music/freq-note-converter",
  "inputs": { "octaveInput": "4.9" },
  "clicks": ["calcNote2Freq()"],
  "expect": ["八度需为 0–8 的整数", "小数或越界输入不会参与计算"],
  "ref": "八度 4.9 必须拒绝并提示，不得 parseInt 成 4 后继续输出 C4；默认 4 不出现提示，旧实现会显示 C4。"
},
{
  "slug": "music/freq-note-converter",
  "inputs": { "freqInput": "30000" },
  "clicks": ["window.__fncAuditionAttempts=0;playFreq();document.getElementById('freq2note').textContent='PLAY '+window.__fncAuditionAttempts;"],
  "expect": ["PLAY 0"],
  "ref": "试听只支持 20–20000 Hz；30000 Hz 超范围应直接提示且不调用播放，不再静默钳制成 20000 Hz。playTone 尝试计数为 0 可区分「未播放」与「播放了钳制值」。"
},
{
  "slug": "music/freq-note-converter",
  "inputs": { "freqInput": "1" },
  "clicks": ["window.__fncAuditionAttempts=0;playFreq();window.__fncAuditionAttempts=window.__fncAuditionAttempts||0;document.getElementById('freq2note').textContent='PLAY '+window.__fncAuditionAttempts;"],
  "expect": ["PLAY 0"],
  "ref": "1 Hz 低于试听下限 20 Hz，必须提示不播放；旧实现会静默播放 20 Hz，与计算结果 1 Hz 不一致。"
},
{
  "slug": "music/convert-speed",
  "inputs": { "dur": "180", "ob": "120", "nb": "140" },
  "clicks": ["calc()"],
  "expect": ["提速 16.7%｜目标速度=原速的 116.7%"],
  "ref": "120→140：目标速度占原速 116.7%，相对原速变化 +16.7%；两个口径必须同时标出，不能把 116.7% 当提速幅度。"
},
{
  "slug": "music/detector",
  "inputs": {},
  "clicks": ["try{tapTimes=[1000,2000];updateDisplay();var r=document.getElementById('res');var had=r.style.display;tapTimes=[3000];updateDisplay();document.getElementById('bpmNum').textContent='DET '+had+'|'+r.style.display+'|'+r.innerHTML.length;}catch(e){document.getElementById('bpmNum').textContent='DETERR '+e.message;}"],
  "expect": ["DET block|none|0"],
  "ref": "新一轮只有 1 次点击时必须隐藏并清空上一轮 BPM 结果；旧实现只把 bpmNum 改「—」，res 仍 display:block 且保留旧 BPM。"
}
,
{
  "slug": "music/audio-converter",
  "inputs": { "sr": "44100", "bd": "", "ch": "2", "dur": "180" },
  "clicks": ["calcPCM()"],
  "expect": ["位深 1–64 bit", "都必须填写有效值"],
  "ref": "单项空值不得静默回退 16 bit；旧实现 `||16` 会继续输出容量，新实现逐项校验并在结果区给出范围提示。"
},
{
  "slug": "music/audio-converter",
  "inputs": { "sr": "44100", "bd": "16", "ch": "2", "dur": "-60" },
  "clicks": ["calcPCM()"],
  "expect": ["时长 >0 秒", "都必须填写有效值"],
  "ref": "负时长必须拒绝，旧实现会输出负容量。"
},
{
  "slug": "music/audio-converter",
  "inputs": { "sr": "44100", "bd": "16", "ch": "2", "dur": "180" },
  "clicks": ["calcPCM()"],
  "expect": ["转 MP3 320k: <strong>≈ 7.20 MB", "PCM 原始大小: 31.75 MB"],
  "ref": "十进制口径：44100×16/8×2×180=31,752,000 B=31.75 MB；320 kbps×1000×180/8/1e6=7.20 MB。旧实现按 MiB 与 1024 得 29.06/7.03，口径混杂。"
},
{
  "slug": "music/music-analysis",
  "inputs": { "sample-rate": "", "bit-depth": "16", "channels": "2", "duration-sec": "60" },
  "clicks": ["calcAudioSize()"],
  "expect": ["采样率 1–768000 Hz", "都必须填写有效值"],
  "ref": "采样率清空不得回退 44100；旧实现 `||44100` 静默输出默认容量。"
},
{
  "slug": "music/music-analysis",
  "inputs": {},
  "clicks": ["['stat-freq','stat-note','stat-cent','stat-octave'].forEach(function(id){document.getElementById(id).textContent='OLD';});clearStats();document.getElementById('audio-size-result').textContent='CLR '+['stat-freq','stat-note','stat-cent','stat-octave'].map(function(id){return document.getElementById(id).textContent;}).join('|');"],
  "expect": ["CLR —|—|—|—"],
  "ref": "clearStats 必须把频率/音名/音分/八度四项统计统一复位为「—」；旧实现静音与停止只清主显示，四项保留上一帧。"
}
,
{
  "slug": "music/music-player",
  "inputs": {},
  "clicks": ["var __o=URL.createObjectURL;URL.createObjectURL=function(){return 'blob:test';};handleFiles([{name:'good.mp3',type:'audio/mpeg'},{name:'bad.exe',type:'application/x-msdownload'},{name:'no-mime.flac',type:''}]);URL.createObjectURL=__o;document.getElementById('__tbProbe').textContent='FILES '+playlist.length+':'+document.querySelectorAll('.playlist-item').length;"],
  "expect": ["FILES 2:2"],
  "ref": "混合选择：仅计 audio MIME 与扩展名兜底的 2 个可播放文件，.exe 跳过；旧实现 push 前直接 return 却仍用 files.length=3 报「已添加 3 首」。"
}

];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  const stat=musicStaticChecks();
  const sf=stat.filter(x=>!x.ok);
  for(const x of sf) console.log("❌ [static] "+x.name);
  console.log("==== music calc " + pass + "/" + cases.length + " ====");
  if (fails.length||sf.length) process.exit(1);
}
if (require.main === module) main();
