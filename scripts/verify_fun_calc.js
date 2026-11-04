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