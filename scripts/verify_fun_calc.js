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
  // ── 烧烤食材分量 ────────────────────────────────────────────
  {
    slug: "fun/bbq-portion",
    inputs: { people: "14", type: "korean", drink: "yes" },
    clicks: ["calcTool()"],
    expect: ["6300 g", "2800 g", "30 瓶"],
    ref: "韩式烤肉（meatPer=450、skewerPer=0）：肉 450×14=6300 g；蔬菜 200×14=2800 g；"
       + "主食 150×14=2100 g；含饮品 round(14×700/330)=round(29.70)=30 瓶。"
       + "原 expect 的 72 串/2100 g/1200 g/13 瓶 即默认态（6 人中式含饮品）输出，属逐字回显默认结果、零判别力；"
       + "且 2100 g 与默认态肉类总量同值（回退默认仍命中，会成逃生项）故不入断言。",
  },

  // ── 火锅食材分量 ────────────────────────────────────────────
  {
    slug: "fun/hotpot-portion",
    inputs: { people: "4", style: "meat", intensity: "normal" },
    expect: ["1320 g", "600 g", "360 g", "320 g", "1000 ml"],
    ref: "总量 4×600×1.0=2400 g；肉 2400×0.55=1320；蔬菜 2400×0.25=600；"
       + "豆制品 2400×0.15=360；主食 4×80=320；汤底 4×250=1000 ml",
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

  // ── 婚宴桌数 ────────────────────────────────────────────────
  {
    slug: "fun/wedding-banquet",
    inputs: { guests: "120", type: "round10", backup: "mid" },
    expect: ["14 桌"],
    ref: "主桌 ceil(120/10)=12；备桌 mid=2；合计 14 桌；到场估算 ceil(120×0.9)=108 人。"
       + "原 expect 含「12 桌」「约 108 人」为备桌无关项（回退 backup=none 仍命中，逃生项），且「2 桌」会撞「12 桌」子串；"
       + "收紧为仅「14 桌 合计预订桌数」（backup=none 时为 12 桌 → 失配）。",
  },

  // ── 步幅与速度换算 ──────────────────────────────────────────
  {
    slug: "fun/step-stride",
    inputs: { cadence: "170", stride: "0.75", weight: "65" },
    expect: ["2.13", "7.65"],
    ref: "ms = 170×0.75/60 = 2.125 → 2.13 m/s；kmh = 2.125×3.6 = 7.65 km/h；"
       + "每公里步数 = round(1000/0.75) = 1333 步",
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

  // ── 婚宴场地桌数估算 ─────────────────────────────────────────
  {
    slug: "fun/wedding-banquet",
    inputs: { guests: "137", type: "square8", backup: "big" },
    expect: ["18 桌 主桌数（方桌 8 人）", "21 桌 合计预订桌数", "约 124 人 按 90% 到场率估算"],
    ref: "type=square8 ⇒ perTable=8；主桌数=ceil(137/8)=18；按 90% 到场=ceil(137×0.9)=ceil(123.3)=124；"
       + "backup=big ⇒ backupN=3；合计=18+3=21。默认态为 120 人/round10/none ⇒ 12 桌、约 108 人、12 桌合计，三条锚全部失配。"
       + "（「20-40 桌」等容纳参考表为与输入无关的常量块，已回避。）",
  },

  // ── FEN 局面解析 ─────────────────────────────────────────────
  {
    slug: "fun/chess-fen-viewer",
    inputs: { fen: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b Kq e3 0 1" },
    expect: ["轮到： 黑方 / 王车易位： Kq / 吃过路兵： e3"],
    ref: "按空格切分后 parts[1]='b' ⇒ 黑方、parts[2]='Kq' ⇒ 王车易位、parts[3]='e3' ⇒ 吃过路兵。"
       + "默认 FEN（'… w KQkq - 0 1'）三条字段分别是白方 / KQkq / 减号，与本锚不重合。",
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

  // ── 数值换算（系数版） ───────────────────────────────────────
  {
    slug: "fun/convert-speed-stride",
    inputs: { val: "2.5", rate: "3", from: "1000", to: "0.001" },
    expect: ["7500000.000000", "系数: 3"],
    ref: "r = v×rate×f/t = 2.5×3×1000/0.001 = 7500000 ⇒ toFixed(6) 即 7500000.000000；系数行直接回显 rate=3。"
       + "默认态 val=1/rate=1/first option 的 value=1 ⇒ r=1.000000，与本锚不重合。"
       + "注：本页标题「步幅与速度换算（步频×步长）」与实际公式（通用 v×rate×f/t 系数换算）不符，"
       + "且与 fun/step-stride 同名重复，属占位模板页，建议后续按通用模板页口径重做。",
  },

];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== fun calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();