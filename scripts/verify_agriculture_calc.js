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
    inputs: { area: "25", fuel: "40", hours: "5", price: "8.2" },
    expect: ["1.600", "328.00", "13.12"],
    ref: "非默认输入（默认 20/15/4/7.5）：亩耗油 = 40 ÷ 25 = 1.600 L/亩；燃油总成本 = 40 × 8.2 = 328.00 元；亩油耗成本 = 1.6 × 8.2 = 13.12 元/亩。三式均随输入变化（默认态输出 0.750 / 112.50 / 5.63）。"
  },
  // ── 存栏密度估算（数量 = 面积 × 密度 × 存活率）──────────────────
  {
    slug: "agriculture/estimate-area-density",
    inputs: { area: "1500", unit: "m2", density: "5", weight: "4", survival: "80" },
    expect: ["24000.00", "10666.72"],
    ref: "非默认输入（默认 2000/8/2.5/95）：areaFactor(m²)=1，存栏 = 1500 × 5 × 1 × 0.80 = 6000；总生物量 = 6000 × 4 = 24000.00 kg；单位面积生物量 = 24000 ÷ 1500 = 16 kg/m² ⇒ ×666.67 = 10666.72 kg/亩。默认态为 15200 / 38000.00。"
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
    inputs: { targetEC: "2.6", waterEC: "0.2", fertEC: "8.0", targetPH: "6.2" },
    expect: ["30.00%", "0.3000"],
    ref: "非默认输入（默认 2.0/0.5/2.5/6.0）：肥料 EC 贡献 = 2.6 − 0.2 = 2.4；稀释比例 = 2.4 ÷ 8.0 = 0.3000；注肥泵比例 = 30.00%；稀释倍数 = 3.3。默认态为 0.6000 / 60.00%（本批特意把 fertEC 提到 8.0 以打破与默认同值的 0.6）。"
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
    inputs: { nutrient: "赖氨酸", total: "500", nameA: "菜粕", valA: "46", nameB: "麸皮", valB: "10", target: "22" },
    expect: ["33.33%", "166.67", "赖氨酸 含量约为 22.00%"],
    ref: "非默认输入（默认 粗蛋白/100/豆粕43/玉米8/18）：Pearson 法 partA = |10−22| = 12、partB = |46−22| = 24、sum = 36；菜粕占比 = 12/36 = 33.33%、重量 = 0.3333 × 500 = 166.67 kg；麸皮 = 66.67% / 333.33 kg；配比验证 = (166.67×46 + 333.33×10) ÷ 500 = 22.00%。默认态为 28.57% / 28.57 kg / 18.00%。"
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
    inputs: { area: "1500", unit: "m2", density: "5", weight: "4", survival: "80" },
    expect: ["24000.00", "10666.72"],
    ref: "非默认输入（默认 2000/8/2.5/95）：areaFactor(m²)=1，存栏 = 1500 × 5 × 1 × 0.80 = 6000；总生物量 = 6000 × 4 = 24000.00 kg；单位面积生物量 = 24000 ÷ 1500 = 16 kg/m² ⇒ ×666.67 = 10666.72 kg/亩。默认态为 15200 / 38000.00。"
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
  }
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