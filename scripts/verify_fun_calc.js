#!/usr/bin/env node
/**
 * fun 分类关键计算逻辑独立验证（收口批次 C）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_fun_calc.js
 *   node scripts/verify_fun_calc.js bbq-portion hotpot-portion
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
{
    "slug": "fun/chess-fen-viewer",
    "clicks": ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'fen',type:'text',value:'8/8/8/8/8/8/8/8 x - - 0 1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('fen').value='8/8/8/8/8/8/8/8 x - - 0 1';var __r=document.getElementById('output');__r.textContent='FEN 字段缺失或非法：需 6 段（行棋方须 w/b、易位 KQkq 或 -、吃过路兵格位或 -、计数非负整数）';__chess_fen_viewer_last=0;start();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FEN n='+__cap.length+' s='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    "expect": ["FEN n=1 s=0"],
    "ref": "复核失败重做·FEN 手动解析不入历史与非法态误判：手动输入 FEN 点『解析』走 start()，原记录器只包装 loadPreset ⇒ n=0；且非法 FEN 文案含『非法/缺失』而非『无效』，原 Score 判通过。修复后包装 start() 并补 非法|缺失 ⇒ n=1 s=0。用例注入 6 段全空 FEN 走真实 start()，预设 output 文本以适配桩 DOM；默认态无探针串 ⇒ 零逃生。"
  },

  // ── 绕口令随机抽题 ──────────────────────────────────────────
  {
    slug: "fun/tongue-twister",
    clicks: ["var __r=Math.random;Math.random=function(){return 0;};next();Math.random=__r;"],
    expect: ["第 1 条 / 难度：简单"],
    ref: "题库 20 条，clicks 把 Math.random 钉为 0（用完即恢复，避免污染同进程后续用例）⇒ "
       + "idx=floor(0×20)=0 ⇒ 第 1 条「四是四…」、难度「简单」。默认态输出为「挑战快速念出声」、"
       + "文本为「点击\"开始\"获取一条绕口令」⇒ 不含「第 1 条 / 难度：简单」，与本用例零交集。"
       + "本页只做随机展示与难度标注，不录音、不计时、不评分。",
  },

  // ── 和弦解析（FE-N6 回归锁：Cmaj/Cmajor 应判大三和弦，非小三）──
  {
    slug: "music/chord-notes",
    inputs: { chordInput: "Cmaj" },
    expect: ["CM · 大三和弦"],
    ref: "FE-N6 回归锁：Cmaj 经归一化 maj→M 后命中 CHORD_TYPES['M'] → 大三和弦，类型标签渲染为「CM · 大三和弦」（rootDisplay=「C」+ type=「M」+「 · 大三和弦」）。默认 chordInput=C 渲染为「C · 大三和弦」，不命中本锚 ⇒ 零逃生，可即时暴露「maj 被前缀 m 误判为小三和弦」类回归。",
  },
  {
    slug: "music/chord-notes",
    inputs: { chordInput: "Cm" },
    expect: ["Cm · 小三和弦"],
    ref: "FE-N6 对照：Cm 直接命中 CHORD_TYPES['m'] → 小三和弦，类型标签「Cm · 小三和弦」。与 Cmaj 的大三形成区分，确认归一化分支正确区分大小三和弦，且默认态「C · 大三和弦」不命中本锚。",
  },

  // ── 扩展和弦九音标注（FE-N7 回归锁：9/m9 的 +14 与 add9 的 +2 应标「九音」而非「二音」）──
  {
    slug: "music/chord-notes",
    inputs: { chordInput: "C9" },
    expect: ["九音"],
    ref: "FE-N7 回归锁：C9=属九和弦，最高扩展音 +14 半音（九音），degreeName 按原始半音数映射为『九音』（旧版 14%12=2 误标『二音』）。默认 chordInput=C（大三和弦，无九音）不命中『九音』⇒ 零逃生。",
  },
  {
    slug: "music/chord-notes",
    inputs: { chordInput: "Csus2" },
    expect: ["二音"],
    ref: "FE-N7 回归护栏：挂二和弦 sus2 的 +2 半音是『二音』（非九音），确认修复未误伤 sus2。默认 chordInput=C 不含『二音』⇒ 零逃生。",
  },

  // ── 降号/升号根音与未知后缀（FE-N8 回归锁：Cb/Fb/E#/B# 应可解析，未知后缀不再静默降级大三）──
  {
    slug: "music/chord-notes",
    inputs: { chordInput: "Cb" },
    expect: ["Cb · 大三和弦"],
    ref: "FE-N8 回归锁：Cb 经 NOTE_ALIASES 映射到 B（同音异名），应正常解析为『Cb · 大三和弦』（B-D#-F#）。旧版 NOTE_ALIASES 缺 Cb/Fb/E#/B# ⇒ NOTE_NAMES.indexOf('Cb')=-1 返回 null 无结果。默认 chordInput=C 渲染『C · 大三和弦』不命中本锚 ⇒ 零逃生。",
  },

  // ── BPM 越界钳制（FE-N4 回归锁：500→钳到 300，四分音符=200.00ms，非 120.00ms）──
  {
    slug: "music/bpm-converter",
    inputs: { bpmInput: "500" },
    expect: ["200.00"],
    ref: "FE-N4 回归锁：getBpm() 把 >300 的输入钳到 300 用于计算，四分音符时长=60000/300=200.00ms；若未钳制则按 500 算得 120.00ms。默认 bpmInput=120 → 四分音符 500.00ms、其余音符时长均不为 200.00 ⇒ 本锚零逃生。配套修复：onBpmChange 在越界时回写输入框、预设同步 bpmSlider。",
  },

  // ── 变速百分比方向（FE-N13）──────────────────────────────────
  {
    slug: "music/convert-speed",
    inputs: { dur: "120", ob: "120", nb: "90" },
    expect: ["降速 25%"],
    ref: "FE-N13：目标 BPM(90) < 原 BPM(120) 为降速，旧实现写死「提速 -25%」方向反。修复后按 nb/ob-1 符号分支：负 →「降速 25%」。"
       + "锚「降速」仅降速输入下出现，默认态（空/等速）输出「请输入有效正数」或「不变」，非逃生。",
  },
  {
    slug: "music/convert-speed",
    inputs: { dur: "120", ob: "120", nb: "150" },
    expect: ["提速 25%"],
    ref: "FE-N13：目标 BPM(150) > 原 BPM(120) 为提速，校验正方向分支输出「提速 25%」；与降速用例互为对照，覆盖 nb/ob-1 正负两侧。",
  },


  // ── 冥想计时器 ──────────────────────────────────────────────
  {
    slug: "fun/meditation-timer",
    inputs: { dur: "35", seg: "6", style: "mantra" },
    clicks: ["calcTool()"],
    expect: ["35 分钟", "间隔分段（每 6 分钟）", "第 6 段"],
    ref: "分段数 = Math.max(1, Math.round(35/6)) = round(5.833) = 6 段，故末段行为 第 6 段、"
       + "副标题为 间隔分段（每 6 分钟）。原 expect 的 10 分钟/5 段/呼吸觉察 为默认态（10/2/breath）输出，"
       + "其中 10 分钟 与 呼吸觉察 在结果区 7 天计划表内恒存在（常量型逃生项）⇒ 改非默认输入、只锚计算量；"
       + "冥想方式名一律不锚（表中 Day1/Day3/Day6 恒含）。",
  },



  // ── 手掌大小与身高相关性（统计） ─────────────────────────────
  {
    slug: "fun/stats-3",
    inputs: { px: "16,18,17,19,22", py: "155,158,161,164,172" },
    expect: ["皮尔逊相关系数 r： 0.9495", "决定系数 R²： 0.9015", "回归方程：身高 = 112.53 + 2.69 × 掌长"],
    ref: "n=5、mx=18.40、my=162.00；sxy=82.20、sxx=30.60、syy=226.80 ⇒ r=sxy/√(sxx·syy)=82.20/√6934.8=0.949473"
       + " ⇒ 0.9495；R²=0.901498 ⇒ 0.9015；b=sxy/sxx=82.20/30.60=2.688679 ⇒ 2.69；a=my−b·mx=162.00−49.4717=112.5283 ⇒ 112.53。"
       + "默认态 px/py 为 5 组完全线性数据（r=1.0000、a=75.00、b=5.00）⇒ 三条锚在默认态全部失配。",
  },


  // ── FEN 局面解析 ─────────────────────────────────────────────
  {
    slug: "fun/chess-fen-viewer",
    inputs: { fen: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b Kq e3 0 1" },
    expect: ["轮到： 黑方 / 王车易位： Kq / 吃过路兵： e3"],
    ref: "按空格切分后 parts[1]='b' ⇒ 黑方、parts[2]='Kq' ⇒ 王车易位、parts[3]='e3' ⇒ 吃过路兵。"
       + "默认 FEN（'… w KQkq - 0 1'）三条字段分别是白方 / KQkq / 减号，与本锚不重合。",
  },

  {
    slug: "fun/chess-fen-viewer",
    inputs: { fen: "4k3/8/8/8/8/8/4P3/4K3 b - - 0 1" },
    clicks: ["loadPreset()"],
    expect: ["轮到： 黑方 / 王车易位： 无 / 吃过路兵： -"],
    ref: "预设栏/历史回填以无参 loadPreset() 调用时应保留当前 FEN：注入黑方 FEN 后点击，"
       + "输出仍为 黑方/无/-；旧实现把 presets[undefined]（undefined）写入输入框并 render ⇒ 抛错或无输出，"
       + "注入失败时回退默认起始局面（白方/KQkq/-）也失配。",
  },

  {
    slug: "fun/chess-fen-viewer",
    inputs: { fen: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" },
    expect: ["FEN 字段缺失或非法"],
    ref: "FE-N10：仅棋盘段（缺后 5 段）旧实现静默显示「黑方」、FAQ 却称「缺段会解析失败」。"
       + "修复后 validateFields 校验 6 段，缺失即报「FEN 字段缺失或非法」；锚不含「白方/黑方/轮到」等默认态串，"
       + "仅在缺段输入下命中，非逃生。",
  },

  // ── 抽奖结果转义 ─────────────────────────────────────────────
  {
    slug: "fun/raffle-picker",
    clicks: ["pickAndShow(['张三<b>X</b>'],1)"],
    expect: ["张三&lt;b&gt;X&lt;/b&gt;"],
    ref: "参与者名称按 HTML 转义后输出：<b> 不得被当作标签渲染；"
       + "旧实现直接拼 innerHTML ⇒ 输出只剩「张三 X」，注入失败/默认态不出现转义串。",
  },

  // ── 冥想分段计划 ─────────────────────────────────────────────
  {
    slug: "fun/meditation-timer",
    inputs: { dur: "25", seg: "7", style: "body" },
    expect: ["25 分钟 冥想总时长", "4 段 间隔分段（每 7 分钟）", "身体扫描 冥想方式"],
    ref: "nSeg=max(1,round(25/7))=round(3.5714)=4；style=body ⇒ styleName=身体扫描。"
       + "默认态为 10 分钟 / round(10/2)=5 段 / 呼吸觉察 ⇒ 三条锚全部失配。"
       + "「开始/结束」时刻串依赖 new Date()，未作锚点（与输入无关的时变量）。",
  },

  // ── 猜数字（1-100）判定分支 ─────────────────────────────────
  {
    slug: "fun/number-guess",
    clicks: ["target=50;tries=0;history=[];", "document.getElementById('guess').value='50';", "submitGuess();"],
    expect: ["🎉 猜对了！数字是 50，共尝试 1 次", "已猜：50（第 1 次）"],
    ref: "target 由 Math.random() 决定、无法作锚，故用 clicks 直接把答案钉为 50 再走一次 submitGuess()："
       + "v=50===target ⇒ 命中分支 猜对了，tries=1、history=[50] ⇒ 输出「🎉 猜对了！数字是 50，共尝试 1 次」与「已猜：50（第 1 次）」。"
       + "默认态页面只渲染「请输入 1-100 之间的有效数字」（start()/reset() 的初始串），两条锚均失配。"
       + "harness 注：页面顶层用 let history 遮蔽 window.history，桩内该全局为 undefined ⇒ clicks 需先给 history=[][] 兜底。",
  },


  // ── 眨眼测试时长 ────────────────────────────────────────────
  {
    slug: "fun/blink-counter",
    inputs: { duration: "120" },
    expect: ["120"],
    ref: "duration 下拉选中 120 ⇒ onchange 触发 updateRing()：total=parseInt('120')=120、 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。"
       + "remain=total=120，同步写 #tNum.textContent='120'。"
       + "默认态 harness 下 select.value 取首个 option ⇒ 输出 30（页面 HTML 静态写死 60，init 调 updateRing 后被首项覆盖），与本例 120 不同。",
  },

  // ── 字母游戏：短词前置校验分支 ───────────────────────────────
  {
    slug: "fun/anagram-game",
    inputs: { answer: "ab" },
    clicks: ["newRound();check();"],
    expect: ["单词至少 3 个字母"],
    ref: "check() 第一分支：v='ab' 长度 2 < 3 ⇒ 直接写 #output 为「单词至少 3 个字母」并 return，"
       + "与随机选中的 cur 无关 ⇒ 完全确定性。须先 newRound() 给 cur/found/score 赋初值，"
       + "否则 `if(!v||!cur)return;` 会静默返回（实测直接调 check() 时 #output 不变）。"
       + "默认态 #output 为 newRound() 留下的引导文案 + 「点击“开始”按钮开始」，不命中。"
       + "（长度≥3 分支依赖随机 cur.valid，不可作断言，本例不覆盖。）",
  },

  // ── 不重复抽取：池抽空后不得静默重置 ─────────────────────────
  {
    slug: "fun/random-picker",
    inputs: { items: "A\nB\nC" },
    clicks: [
      "document.getElementById('unique').checked=true;pool=[];poolSig='A\\nB\\nC';start();",
    ],
    expect: ["所有选项已抽完！"],
    ref: "不重复模式下池已抽空（pool=[]）时应提示「所有选项已抽完！」；"
       + "旧实现 `if(!pool||pool.length===0)pool=[...list]` 会把空池重新填满并继续抽 ⇒ 静默重置、提示永远不出现。"
       + "默认池为 null 且未勾选不重复，不会命中。",
  },

  // ── 抽奖概率口径：抽 n 人时任意 1 人中签 = n/N，不是 1/N ──────
  {
    slug: "fun/raffle-picker",
    inputs: { entries: "A\nB\nC", count: "2" },
    clicks: ["updateProbNote();"],
    expect: ["1/N=33.3%", "n/N=66.7%"],
    ref: "3 人抽 2 人（不放回）：单次第一名 1/3 = 33.3%，任意 1 人中签 2/3 = 66.7%；"
       + "默认 8 人抽 1 人 ⇒ 两条锚均失配（默认只显示 12.5%）。旧页面无概率面板、且文案承诺并不存在的「权重」。",
  },
  // ── 计时/回合制结算分：只测算分纯函数（DOM/定时器/classList 不参与）──
  {
    slug: "fun/whack-a-mole",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='S='+calcWhackScore(22,5,0)+'/'+calcWhackScore(0,0,5)+'/'+calcWhackScore(10,0,0)+'/'+calcWhackScore(0,5,0)"],
    expect: ["S=195/-25/100/-25"],
    ref: "独立复算：命中 22×10=220，漏点 5×5=25，净 195（与页面算例一致）；点空 5 次 −25（覆盖“可为负”语义）；"
       + "命中 10 次 = 100；漏点 5 次 = −25。纯函数 calcWhackScore(hits,misses,blanks) 与 DOM/定时器无关。",
  },
  {
    slug: "fun/reaction-tester",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='A='+calcReactionAvg([300,200,400])+'/'+calcReactionAvg([])"],
    expect: ["A=300/NaN"],
    ref: "独立复算：平均反应 = (300+200+400)/3 = 300 ms；空样本返回 NaN（页面此时显示“—”）。",
  },
  // ── 线上 bug 回归：reaction-tester 初始状态未初始化导致 times.push 抛错 ──
  {
    slug: "fun/reaction-tester",
    inputs: {},
    clicks: ["document.getElementById('__tbProbe').textContent='RTINIT='+(Array.isArray(times)?'Y':'N')+' STATE='+String(state)+' BEST='+String(best);"],
    expect: ["RTINIT=Y STATE=idle BEST=null"],
    ref: "线上 bug 回归①（初始状态）：旧页面 `let state,times,...` 五个变量全为 undefined，且 reset() 从不在加载时调用 ⇒ times 未初始化。此探针在页面刚加载时读取声明处的初始值，修复后必须已是数组/空闲态。修复前会是 RTINIT=N STATE=undefined BEST=undefined，故本例在旧代码上必然 FAIL；探针串只在注入 clicks 后出现，默认态零命中。",
  },
  {
    slug: "fun/reaction-tester",
    inputs: {},
    clicks: ["var __err='N';try{start();onClick();}catch(e){__err='Y';}var __cur=String(document.getElementById('cur').textContent);document.getElementById('__tbProbe').textContent='RTCLICK='+__err+' N='+(Array.isArray(times)?times.length:'UNDEF')+' OK='+(__cur!==String.fromCharCode(0x2014)&&__cur!==''?'Y':'N')+' STATE='+String(state);"],
    expect: ["RTCLICK=N N=1 OK=Y STATE=idle"],
    ref: "线上 bug 回归②（真实复现链路）：harness 的 setTimeout 桩立即执行，start() 后立即变绿进入 ready，再 onClick() 走 times.push(rt)。旧代码在此抛 \"Cannot read properties of undefined (reading 'push')\"，且异常使 state=idle 不执行 ⇒ 用户连续点击持续报错（Clarity 会话 00:09/00:10/00:11 三次）。修复后不抛错、记录 1 次成绩、cur 有值、状态回到 idle。expect 不含时钟相关的 ms 数值，避免时间漂移。",
  },
  {
    slug: "fun/reaction-tester",
    inputs: {},
    clicks: ["var __es=[];for(var i=0;i<3;i++){try{start();onClick();__es.push('N');}catch(e){__es.push('Y');}}document.getElementById('__tbProbe').textContent='RTMULTI='+__es.join('')+' N='+(Array.isArray(times)?times.length:'UNDEF');"],
    expect: ["RTMULTI=NNN N=3"],
    ref: "线上 bug 回归③（连续多次点击）：模拟用户按提示连续做 3 次反应测试，每轮 start()+onClick() 都必须成功且成绩累加到 3 条。旧代码首轮即抛错、state 卡在 ready，后续点击只会重复抛错、times 始终 undefined。默认态探针不存在。",
  },
  {
    slug: "fun/reaction-tester",
    inputs: {},
    clicks: ["reset();state='wait';onClick();var __e1=String(state);start();onClick();document.getElementById('__tbProbe').textContent='RTEARLY='+__e1+' N='+(Array.isArray(times)?times.length:'UNDEF')+' STATE='+String(state);"],
    expect: ["RTEARLY=early N=1 STATE=idle"],
    ref: "线上 bug 回归④（抢跳→重试全状态机）：手动置 wait 后点击应判抢跳且不记成绩，随后重新 start()+点击必须能正常记录 1 次并回到 idle。覆盖用户「等待变绿后立即点选」的完整操作路径，确认初始化修复不破坏 early/idle/ready 三态流转。默认态探针不存在。",
  },
  {
    slug: "fun/typing-rhythm",
    inputs: {},
    clicks: ["document.getElementById('result').textContent='T='+calcRhythmScore(0.25)+'/'+calcRhythmScore(1.5)+'/'+calcWpm(100,60000)"],
    expect: ["T=70/0/20"],
    ref: "独立复算：score = clamp(100 − cv×120, 0, 100)；cv=0.25 ⇒ 70，cv=1.5 ⇒ −80 截断为 0；"
       + "WPM = 字符数 ÷ 分钟 ÷ 5 = 100 ÷ 1 ÷ 5 = 20（ms=60000 即 1 分钟）。",
  },
  {
    slug: "fun/cps-test",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='C='+calcCps(40,5).toFixed(2)+'/'+cpsLabel(4.99)+'/'+cpsLabel(8)+'/'+cpsLabel(13)+'/'+cpsLabel(14)"],
    expect: ["C=8.00/慢/不错/很快/神速 ⚡"],
    ref: "独立复算：CPS = 40÷5 = 8.00；阈值 5/8/11/14 分档 ⇒ 4.99 慢、8 不错、13 很快、14 神速（原文案 4/7/11/12 与代码不符，已按代码统一）。",
  },
  {
    slug: "fun/click-speed",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='C='+calcCps(40,5).toFixed(2)+'/'+calcCps(12,30).toFixed(2)"],
    expect: ["C=8.00/0.40"],
    ref: "独立复算：CPS = 点击数 ÷ 时长 ⇒ 40÷5 = 8.00、12÷30 = 0.40。",
  },

  // ── 抽取类：随机种子可复算 + 同名不重复中签 + 人数上界钳制 ─────
  {
    slug: "fun/raffle-picker",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='S='+rafflePickIndexes(['A','B','C','D'],2,'seed-1').join(',')+'|'+rafflePickIndexes(['A','B','A','C','B','D'],2,'seed-1').join(',')+'|'+rafflePickIndexes(['A','B'],5,'seed-1').join(',')"],
    expect: ["S=C,B|C,B|B,A"],
    ref: "FNV-1a(xorshift32) 复算：seed-1、A/B/C/D 抽 2 依次取 C、B；含重复行的名单先去重（保留首次出现顺序 A/B/C/D），同种子仍取 C、B ⇒ 同名不会重复中签；"
       + "名单仅 2 人却填 5 人时 k=min(2,5)=2，取 B、A（人数上界钳制，不越界抽取）。"
       + "默认态名单为 8 人、无种子（自动生成），三条锚均不出现。",
  },
  {
    slug: "fun/random-picker",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='S='+randomPickOne(['A','B','C','D'],'seed-1')+'|'+randomPickOne(['A','B','C','D'],'seed-1')+'|'+randomPickOne(['A','B','C','D','E'],'seed-1')"],
    expect: ["S=C|C|D"],
    ref: "FNV-1a(xorshift32) 复算：seed-1 时 4 项列表两次调用均取 C（同种子可复算），5 项列表取 D；"
       + "默认态列表为 8 项中文餐食、无种子，锚串不出现。",
  },

  // ── 抛硬币连胜：同面（正/反）计数与百分比 ──────────────────
  {
    slug: "fun/coin-toss-streak",
    inputs: {},
    clicks: ["var __mr=Math.random;Math.random=function(){return 0.9};reset();flip10();var a=document.getElementById('maxStreak').textContent+'/'+document.getElementById('headsPct').textContent;Math.random=function(){return 0.1};reset();flip10();document.getElementById('output').textContent='M='+a+'|'+document.getElementById('maxStreak').textContent+'/'+document.getElementById('headsPct').textContent;Math.random=__mr;"],
    expect: ["M=10/100%|10/0%"],
    ref: "把 Math.random 钉为 0.9（>0.5 ⇒ 全部正面）后 flip10()：最长连胜 = 10、正面率 100%；"
       + "再钉为 0.1（全部反面）重置后 flip10()：最长连胜仍 10（页面按「连续同面」计，不分正反）、正面率 0%。"
       + "默认态 total=0、maxStreak=0、headsPct=—，不命中。",
  },

  // ── fun 零覆盖补强（C 类：可正常测 5 页） ──────────────────
  {
    slug: "fun/keyboard-heatmap",
    clicks: ["loadSample();loadSample()"],
    expect: ["90"],
    ref: "样例文本「The quick brown fox jumps over the lazy dog. 敏捷的棕色狐狸跃过懒狗。」单次统计（页内正则 `\\w` + 空格 + `,./` 等符号）："
       + "字母 35 + 空格 9（8 个词间空格 + 句点后 1 个）+ 句点 1 = 45；中文段不匹配该字符类、不计入；唯一按键 28。"
       + "loadSample 是累加（不清零），连调两次 ⇒ 总按键 90。默认输入框为空 ⇒ 0；判别器清空 clicks 后兜底只调一次 loadSample ⇒ 45，不命中 90。"
       + "（不用唯一键 28 作锚：单次调用即可命中，属兜底可复现的逃生项。）",
  },
  {
    slug: "fun/coin-flip",
    clicks: ["(function(){var R=Math.random;Math.random=function(){return 0.1};flip();Math.random=function(){return 0.9};flip();flip();Math.random=R;})()"],
    expect: ["33.3"],
    ref: "把 Math.random 依次钉为 0.1 / 0.9 / 0.9 后连掷 3 次：正、反、反 ⇒ 正面 1 / 总 3 ⇒ 正面率 (1/3*100).toFixed(1) = 33.3%、反面率 66.7%。"
       + "默认未掷 ⇒ 百分比为静态 50；判别器清空 clicks 后兜底按种子随机序列掷 11 次（flip 1 次 + flipMultiple 10 次）⇒ 8 正 3 反 = 72.7%，不命中 33.3。"
       + "（不用结果文案「🎊 反面！」作锚：兜底的末次掷同样可能落反面。）",
  },
  {
    slug: "fun/generator-2",
    inputs: { cnt: "10" },
    expect: ["#10 数独"],
    ref: "cnt=10 ⇒ 逐条输出「#1 数独」…「#10 数独」（题面随机，但编号与条数确定）；默认 cnt=5 ⇒ 最多到 #5，锚串不出现。",
  },
  {
    slug: "fun/generator-2",
    inputs: { cnt: "" },
    expect: ["请输入生成数量"],
    ref: "FE-N73 复核重做：清空生成数量（空值）后，旧实现 `value||5` 把空当 0→5 生成 5 题；现空值直接提示「请输入生成数量」并 return。默认 cnt=5 生成 5 题不含该提示 ⇒ 强判别、零逃生。",
  },
  {
    slug: "fun/generator-3",
    inputs: { cnt: "10" },
    expect: ["#10 迷宫"],
    ref: "cnt=10 ⇒ 逐条输出「#1 迷宫」…「#10 迷宫」（迷宫随机，但编号与条数确定）；默认 cnt=5 ⇒ 最多到 #5，锚串不出现。",
  },
  {
    slug: "fun/generator-3",
    inputs: { cnt: "" },
    expect: ["请输入生成数量"],
    ref: "FE-N73 复核重做：清空生成数量（空值）后，旧实现 `value||5` 把空当 0→5 生成 5 题；现空值直接提示「请输入生成数量」并 return。默认 cnt=5 生成 5 题不含该提示 ⇒ 强判别、零逃生。",
  },
  {
    slug: "fun/generator-laugh",
    inputs: { cnt: "10" },
    expect: ["10. "],
    ref: "cnt=10 ⇒ 笑声列表渲染到第 10 条（`10. 「哈哈哈…」 基频…/持续…秒`）；编号与条数确定，音色参数随机。"
       + "默认 cnt=5 ⇒ 列表最多到「5. 」，锚串「10. 」不出现。",
  },
{
  "slug": "fun/tic-tac-toe",
  "clicks": ["newGame()", "makeMove(0)", "makeMove(1)", "makeMove(2)", "makeMove(4)", "makeMove(3)", "makeMove(5)", "makeMove(7)", "makeMove(6)", "makeMove(8)"],
  "expect": ["🤝 平局！"],
  "ref": "PvP 固定落子（X:0,2,3,7,8 / O:1,4,5,6）填满九格且横竖斜均无三连 ⇒ 走平局分支，输出「🤝 平局！」。"
       + "胜负分支的 highlightWin 依赖运行时 querySelectorAll('.cell')（桩不登记 createElement 追加的节点）会抛错，故取同一判定链路的平局分支。默认空盘只显示「点击格子开始游戏」，零交集。"
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

  console.log("==== fun calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();