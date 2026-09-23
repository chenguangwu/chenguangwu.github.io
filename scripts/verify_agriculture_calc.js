#!/usr/bin/env node
/**
 * agriculture 分类关键计算逻辑独立验证（收口批次 C）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_agriculture_calc.js
 *   node scripts/verify_agriculture_calc.js estimate-3 ratio-10
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 作物需水（ETc = ET0 × Kc，净需水扣雨量）────────────────────
  {
    slug: "agriculture/estimate-3",
    inputs: { kc: "1.1", et0: "3.7", days: "13", area: "1234", rain: "5" },
    expect: ["4.07", "52.91", "47.91", "65.29"],
    ref: "ETc = 3.7 × 1.1 = 4.07；总需水深 = 4.07 × 13 = 52.91；"
       + "净灌溉 = 52.91 − 5 = 47.91；总需水 = 52.91 × 1234 ÷ 1000 = 65.29 m³",
  },
  // ── 肥料表观利用率（(吸收−土壤基础)÷施肥量）──────────────────────
  {
    slug: "agriculture/estimate-yield-rate",
    inputs: { element: "N", fert: "150", uptake: "90", soil: "40" },
    expect: ["33.33%"],
    ref: "来自肥料的吸收 = 90 − 40 = 50；利用率 = 50 ÷ 150 × 100 = 33.33%",
  },
  // ── 农机油耗（亩耗油 = 总耗油 ÷ 面积）──────────────────────────
  {
    slug: "agriculture/estimate-fuel-engine-oil",
    inputs: { area: "20", fuel: "15", hours: "4", price: "7.5" },
    expect: ["0.750", "3.75", "112.50"],
    ref: "亩耗油 = 15 ÷ 20 = 0.750；每小时油耗 = 15 ÷ 4 = 3.75；"
       + "燃油总成本 = 15 × 7.5 = 112.50 元",
  },
  // ── 存栏密度估算（数量 = 面积 × 密度 × 存活率）──────────────────
  {
    slug: "agriculture/estimate-area-density",
    inputs: { area: "2000", unit: "m2", density: "8", weight: "2.5", survival: "95" },
    expect: ["15200", "38000.00", "7.60"],
    ref: "存栏 = 2000 × 8 × 1 × 0.95 = 15200；总生物量 = 15200 × 2.5 = 38000.00；"
       + "折算密度 = 15200 ÷ 2000 = 7.60 只/㎡",
  },
  // ── 土壤有机质（烧失率 × 温度校正 × 换算系数）────────────────────
  {
    slug: "agriculture/soil-organic-matter",
    inputs: { beforeWeight: "10", afterWeight: "9.6", temp: "550", factor: "1.724" },
    expect: ["0.4000", "4.00%", "2.32%"],
    ref: "灼烧失重 = 10 − 9.6 = 0.4000；烧失率 = 0.4 ÷ 10 × 100 = 4.00%；"
       + "有机碳 = 4 × 0.58 = 2.32%；有机质 = 2.32 × 1.724 = 4.00%",
  },
  // ── 水肥 EC 注肥比例（(目标EC−水源EC) ÷ 肥料EC）──────────────────
  {
    slug: "agriculture/ratio-10",
    inputs: { targetEC: "2.0", waterEC: "0.5", fertEC: "2.5", targetPH: "6.0" },
    expect: ["60.00%", "0.6000", "1.7"],
    ref: "肥料 EC 贡献 = 2.0 − 0.5 = 1.5；稀释比例 = 1.5 ÷ 2.5 = 0.6000；"
       + "注肥泵比例 = 60.00%；稀释倍数 = 1 ÷ 0.6 = 1.7",
  },
  // ── 干物质换算（干物质 = 鲜重 × (1 − 含水率)）────────────────────
  {
    slug: "agriculture/dry-matter-conversion",
    inputs: { freshWeight: "1000", moisture1: "20" },
    expect: ["800.00", "200.00", "80.0%"],
    ref: "干物质 = 1000 × (1 − 0.2) = 800.00；水分 = 1000 − 800 = 200.00；"
       + "干物质率 = 80.0%",
  },
  // ── 光照积分 DLI（PPFD × 小时 × 3600 ÷ 1e6）────────────────────
  {
    slug: "agriculture/dli-calculator",
    inputs: { ppfd: "200", hours: "8", lightPPFD: "0", lightHours: "0", cropType: "low" },
    expect: ["5.8"],
    ref: "自然光 DLI = 200 × 8 × 3600 ÷ 1e6 = 5.76 → 5.8；补光 0.0；总 DLI = 5.8",
  },
  // ── 收获损失率（总损失 = 理论 − 实际）──────────────────────────
  {
    slug: "agriculture/harvest-loss-rate",
    inputs: { theoryYield: "500", actualYield: "470", headerLoss: "8", threshLoss: "6", scatterLoss: "10", transportLoss: "6" },
    expect: ["30.0", "6.00%"],
    ref: "总损失 = 500 − 470 = 30.0 kg/亩；损失率 = 30 ÷ 500 × 100 = 6.00%",
  },
  // ── 配比混合（十字交叉法：占比 = |另一方−目标| ÷ 两差之和）────────
  {
    slug: "agriculture/calculator-calc-ratio-1",
    inputs: { nutrient: "粗蛋白", total: "100", nameA: "豆粕", valA: "43", nameB: "玉米", valB: "8", target: "18" },
    expect: ["28.57%", "71.43%"],
    ref: "partA = |8 − 18| = 10，partB = |43 − 18| = 25，和 = 35；"
       + "A 占比 = 10 ÷ 35 = 28.57%；B 占比 = 25 ÷ 35 = 71.43%",
  },
  // ── 肥料当季利用率（差减法）───────────────────────────────────
  {
    slug: "agriculture/fertilizer-efficiency",
    inputs: { fertUptake: "30", fertInput: "50", ckUptake: "10", nutrientType: "N" },
    expect: ["40.0%", "20.0"],
    ref: "利用率 = (30 − 10) ÷ 50 × 100 = 40.0%；肥料养增量 = 20.0 kg/亩",
  },
  // ── 连作障碍指数（当前密度 = 初始 × (1+年增率)^年限）──────────────
  {
    slug: "agriculture/estimate-soil",
    inputs: { years: "5", init: "1000", rate: "20", threshold: "5000" },
    expect: ["49.8", "预警"],
    ref: "当前密度 = 1000 × 1.2⁵ = 2488.32；指数 = 2488.32 ÷ 5000 × 100 = 49.8；"
       + "30 ≤ 49.8 ≤ 60 → 预警",
  },

  // ── 收获损失评估（BATCH55：理论产量 0 时损失率 NaN，无守卫）──
  {
    slug: "agriculture/assessor-1",
    inputs: { theoryYield: "0", actualYield: "415", fieldLoss: "15", threshLoss: "10" },
    expect: ["理论产量必须大于 0"],
    ref: "理论产量 0 → 损失率 = (0-415)/0×100 = NaN；修复前输出 NaN%，应给守卫提示",
  },
  {
    slug: "agriculture/assessor-1",
    inputs: { theoryYield: "500", actualYield: "450", fieldLoss: "20", threshLoss: "10" },
    expect: ["10.00", "4.00", "2.00"],
    ref: "损失率=(500-450)/500×100=10.00%；田间落粒=20/500×100=4.00%；脱粒=10/500×100=2.00%；"+
         "机械标准限值 3.0%，10%>3×1.5=4.5% → 不合格（修复前 10%>3% 即标红但不写阈值比较）",
  },

  // ── 养殖面积密度估算（BATCH55：面积 0 时密度除零 NaN）──
  {
    slug: "agriculture/estimate-area-density",
    inputs: { area: "0", unit: "m2", density: "5", weight: "2", survival: "90" },
    expect: ["请填写有效的参数"],
    ref: "面积 0 → 折算密度 = 存栏/0 = NaN；修复前输出 NaN，已收紧 valid 要求面积>0",
  },

  // ── 草地面积产量估算（BATCH55：面积 0 时单产除零 NaN）──
  {
    slug: "agriculture/estimate-area-yield",
    inputs: { area: "0", unit: "kg_mu", yieldInput: "30000", dmRate: "30", baleWeight: "25" },
    expect: ["请填写有效的参数"],
    ref: "面积 0 → 每亩干草 = 干草/0 = NaN；修复前输出 NaN，已收紧 valid 要求面积>0",
  },
  {
    slug: "agriculture/estimate-area-yield",
    inputs: { yieldInput: "60000", area: "1500", dmRate: "25", baleWeight: "30", unit: "kg_mu" },
    expect: ["134999.33", "33749.83", "2.25", "1125"],
    ref: "鲜草=60000×1500/666.67=134999.33 kg；干草=134999.33×25%=33749.83 kg；"+
         "折合亩=1500/666.67=2.25 亩；草捆=33749.83/30=1125 个（与默认态 fresh=44999.78 明显不同，有判别力）",
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
  console.log("==== agriculture calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();