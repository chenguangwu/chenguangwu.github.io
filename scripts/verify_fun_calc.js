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