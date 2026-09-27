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
  },
  // ── 配方施肥量（氮磷钾单质肥按折纯率折算，默认态三量全等故无判别力）──
  {
    slug: "agriculture/calculator-calc-ratio",
    inputs: { nNeed: "150", pNeed: "75", kNeed: "112.5", area: "2.4",
      nFert: "34", nPct: "46", pFert: "18", pPct: "46", kFert: "50", kPct: "60",
      price: "3.2", nEff: "55", pEff: "22", kEff: "65" },
    dumpIds: ["res"],
    expect: ["1422.92", "3893.89", "12460.44"],
    ref: "独立复算：N = 150 ÷ (0.46 × 0.55) × 2.4 = 1422.924901 ⇒ 1422.92；P = 75 ÷ (0.46 × 0.22) × 2.4 = 1778.656126 ⇒ 1778.66（本页只取 2 位）；K = 112.5 ÷ (0.60 × 0.65) × 2.4 = 692.307692 ⇒ 692.31；总量 3893.888720 ⇒ 3893.89；成本 = 3893.888720 × 3.2 = 12460.4439 ⇒ 12460.44。默认态为 521.74 / 1293.48 / 1293.48，三条均不命中。",
  },
  // ── 作物施肥配方（单产系数放大 Needs，肥料按含量反算用量）──
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: { crop: "1", yield: "620", area: "12", fertN: "3", fertP: "5", fertK: "9" },
    dumpIds: ["result"],
    expect: ["1207.6", "681.2", "1 : 0.50 : 0.72"],
    ref: "独立复算（CROPS[1]=小麦 yield450 n14 p7 k10；FERTILIZERS[3]=硝酸铵 n34、[5]=重过磷酸钙 p46、[9]=氯化钾 k60）：factor = 620 ÷ 450 = 1.377778；needN = 14 × 1.377778 = 19.2889 ⇒ 19.3、needP = 7 × 1.377778 = 9.6444 ⇒ 9.6、needK = 10 × 1.377778 = 13.7778 ⇒ 13.8；亩养分总量 = 19.2889 + 9.6444 + 13.7778 = 42.7111 ⇒ 42.7；硝酸铵 = 19.2889 × 12 ÷ 0.34 = 681.1765 ⇒ 681.2（产物同为 56.8 kg/亩 = 681.1765 ÷ 12）；重过磷酸钙 = 9.6444 × 12 ÷ 0.46 = 250.4348 ⇒ 250.4；氯化钾 = 13.7778 × 12 ÷ 0.60 = 276.0；总施肥量 = 1207.6113 ⇒ 1207.6；NPK 比 = 9.6444 ÷ 19.2889 = 0.4978 ⇒ 0.50、13.7778 ÷ 19.2889 = 0.7155 ⇒ 0.72。默认态为 575.0 / 375.0 / 200.0 / 1 : 0.50 : 0.83，三条均不命中。注：crop / fertN / fertP / fertK 的 option value 是 CROPS / FERTILIZERS 的数组下标字符串，灌作物名（如 wheat）会取到 undefined。",
  },
  // ── 灌溉制度（计划湿润层净灌水 → 按水利用系数还原毛灌量）──
  {
    slug: "agriculture/irrigation-calculator",
    inputs: { method: "drip", soil: "clay", area: "8", depth: "40",
      moisture: "55", price: "0.8", cycle: "10" },
    dumpIds: ["result"],
    expect: ["52.9", "422.8", "1014.77"],
    ref: "独立复算（clay: gamma=1.35, fc=30；drip: eff=0.92）：田间持水量上限 betaMax=30、下限 betaMin=55%×30=16.5；净灌水 = 667 × 0.40 × (30−16.5) ÷ 100 × 1.35 = 48.6243 m³/亩；毛灌 = 48.6243 ÷ 0.92 = 52.8525 ⇒ 52.9 m³/亩；总毛灌 = 52.8525 × 8 = 422.82 ⇒ 422.8 m³；单次水费 = 422.82 × 0.8 = 338.256 ⇒ 338.26 元；月用水 = 52.8525 × 8 × 30 ÷ 10 = 1268.46 ⇒ 1268.5 m³，月费 = 1268.46 × 0.8 = 1014.77 元。默认态为 34.9 / 349.3 / 748.43，三条均不命中。",
  },
  // ── 收获计划（半机械化：机械占日进度 70%，人工按人均日效率配人数）──
  {
    slug: "agriculture/harvest-planner",
    inputs: { area: "240", yield: "520", method: "semi",
      days: "6", hours: "10", laborCost: "180", machineCost: "95" },
    dumpIds: ["result"],
    expect: ["124.8", "23520", "98.0"],
    ref: "独立复算（小麦 manual=1.5 亩/人·班, machine=8 亩/台·班）：总产 = 240 × 520 ÷ 1000 = 124.8 t；日进度 = 240 ÷ 6 = 40 亩/天；人工区 = 40 × 0.3 = 12 亩，人均日效率 = 1.5 × 10 ÷ 8 = 1.875 ⇒ 需工 = ⌈12 ÷ 1.875⌉ = 7 人；机械区 = 40 × 0.7 = 28 亩 ⇒ ⌈28 ÷ (8 × 10)⌉ = 1 台；机械费 = 240 × 95 × 0.7 = 15960 元，人工费 = 7 × 6 × 180 = 7560 元，合计 23520 元；亩均 = 23520 ÷ 240 = 98.0 元/亩；公斤成本 = 23520 ÷ (124.8 × 1000) = 0.188 元/kg。默认态为 50.0 / 10500 / 105.0，三条均不命中。",
  },  // ── 水肥一体化配比（目标EC − 水源EC → 施肥量 / 母液方案）────
  {
    slug: "agriculture/fertigation-ratio",
    inputs: { targetEC: "2", waterEC: "0.2", dripFlow: "3", dripperCount: "800", duration: "45", fertType: "3", solubility: "150", stockRatio: "100" },
    expect: ["3.60", "6.48", "24.0"],
    ref: "独立复算：净增EC = 2.0 − 0.2 = 1.8；肥料浓度 = 1.8 ÷ ecPer(0.5) = 3.6 g/L；" +
       + "总流量 = 3 × 800 = 2400 L/h；灌水总量 = 2400 × (45/60) = 1800 L = 1.80 m³；" +
       + "总用肥 = 3.6 × 1800 ÷ 1000 = 6.48 kg；NPK 各按配方百分比：30-10-10 ⇒ 氮 1.94 / 磷 0.65 / 钾 0.65；" +
       + "母液浓度 = 3.6 × 100 = 360.0 g/L、母液体积 = 1800 ÷ 100 = 18.0 L、需称肥料 6.48 kg、" +
       + "注肥速率 = 18 ÷ 0.75 = 24.0 L/h；360 g/L > 溶解度 150 ⇒ 触发超溶解度警告。" +
       + "默认态（1.5 / 0.3 / 2 L/h / 500 滴灌管 / 30 min / 20-20-20 / 200 倍）为 2.40 / 1.20 / 10.0，三条均不命中。",
  },

  // ── 冠层覆盖度（圆冠面积 ÷ 单株占地 × (1−重叠率)）────────
  {
    slug: "agriculture/canopy-coverage",
    inputs: { rowSpacing: "80", plantSpacing: "40", canopyDiam: "50", canopyShape: "circle", overlap: "10" },
    expect: ["55.2%", "2083", "1963"],
    ref: "独立复算：圆冠单株面积 = π × (50/2)² = 1963.4954 ⇒ toFixed(0) '1963' cm²；" +
       + "单株占地面积 = 80 × 40 = 3200 cm²；原始覆盖度 = 1963.4954 ÷ 3200 × 100 = 61.35985%；" +
       + "扣重叠 = 61.35985 × (1 − 10/100) = 55.22386 ⇒ toFixed(1) '55.2'%；" +
       + "LAI = 0.5522386 × 3.5 = 1.9328 ⇒ '1.93'；" +
       + "种植密度 = round(666.67 ÷ 0.32) = round(2083.34) = 2083 株/亩。" +
       + "默认态（60/30/35/circle/5%）为 50.8% / 3704 / 962，三条均不命中。" +
       + "注：评价词档位（部分覆盖）在默认态同值，未作锚。",
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