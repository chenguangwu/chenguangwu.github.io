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
    inputs: { people: "6", type: "bbq", drink: "yes" },
    expect: ["72 串", "2100 g", "1200 g", "13 瓶"],
    ref: "中式烤串：肉串 12×6=72 串；肉 350×6=2100 g；蔬菜 200×6=1200 g；"
       + "饮品 round(6×700/330)=round(12.73)=13 瓶",
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
    inputs: { dur: "10", seg: "2", style: "breath" },
    expect: ["10 分钟", "5 段", "呼吸觉察"],
    ref: "分段数 = Math.max(1, round(10/2)) = 5 段；方式 breath → 呼吸觉察",
  },

  // ── 婚宴桌数 ────────────────────────────────────────────────
  {
    slug: "fun/wedding-banquet",
    inputs: { guests: "120", type: "round10", backup: "mid" },
    expect: ["12 桌", "2 桌", "14 桌", "约 108 人"],
    ref: "主桌 ceil(120/10)=12；备桌 mid=2；合计 14 桌；"
       + "到场估算 ceil(120×0.9)=108 人（金额走 toLocaleString，不作断言避免 ICU 差异）",
  },

  // ── 步幅与速度换算 ──────────────────────────────────────────
  {
    slug: "fun/step-stride",
    inputs: { cadence: "170", stride: "0.75", weight: "65" },
    expect: ["2.13", "7.65", "1333"],
    ref: "ms = 170×0.75/60 = 2.125 → 2.13 m/s；kmh = 2.125×3.6 = 7.65 km/h；"
       + "每公里步数 = round(1000/0.75) = 1333 步",
  },
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 300));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
