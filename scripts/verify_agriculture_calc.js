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
  // ── 六页签综合计算器（agri-calculator）：肥料 / 密度 / 农药 / 灌溉 / 油耗 ──
  // 原为该页零用例状态（全站 scan 命中「零用例」清单）。5 条分别打在 5 条独立计算链上。
  {
    slug: "agriculture/agri-calculator",
    inputs: { fert_n: "20", fert_p: "10", fert_k: "15", fert_area: "8", fert_per_mu: "30" },
    clicks: ["calcFertilizer();"],
    dumpIds: ["fertResult"],
    expect: ["48.00 kg", "240.0 kg"],
    ref: "施肥量 = 面积 × 每亩用量 = 8 × 30 = 240 kg；氮 = 240 × 20% = 48.00、磷 = 240 × 10% = 24.00、"
       + "钾 = 240 × 15% = 36.00。默认态（15-15-15 / 10 亩 / 25 kg）为 250.0 kg / 37.50 kg，两条均不命中。",
  },
  {
    slug: "agriculture/agri-calculator",
    inputs: { plant_spacing: "40", plant_row: "60", plant_area: "5", plant_unit: "mu" },
    clicks: ["calcDensity();"],
    dumpIds: ["densityResult"],
    expect: ["13,888", "2,777"],
    ref: "按亩计：亩 = 666.67 m² ⇒ sqm = 5 × 666.67 = 3333.35；单株占地 = (40/100) × (60/100) = 0.24 m²；"
       + "总株数 = floor(3333.35 / 0.24) = floor(13888.958) = 13888（toLocaleString 千分位 13,888）；"
       + "每亩株数 = floor(666.67 / 0.24) = floor(2777.79) = 2777（2,777）。默认态为 44,444 / 4,444。",
  },
  {
    slug: "agriculture/agri-calculator",
    inputs: { pest_content: "20", pest_target: "2000", pest_volume: "50", pest_unit: "ppm" },
    clicks: ["calcPesticide();"],
    dumpIds: ["pestResult"],
    expect: ["需量取原药： 500.00 ml(g)"],
    ref: "ppm 档：targetPct = 2000 / 10000 = 0.2；配制药液 = 50 L = 50000 ml；"
       + "需原药 = 0.2 × 50000 ÷ 20 = 500.00 ml。默认态（40% / 1000ppm / 30L）恰好也算出 75.00 ml ⇒ "
       + "已换成 20% / 2000ppm / 50L 的非默认组合，判别力落在注入值上。",
  },
  {
    slug: "agriculture/agri-calculator",
    inputs: { irr_area: "20", irr_depth: "30" },
    clicks: ["calcIrrigation();"],
    dumpIds: ["irrResult"],
    expect: ["总用水量： 400.2 m³"],
    ref: "总用水 = 面积 × 深度 × 0.667 = 20 × 30 × 0.667 = 400.20000000000005 ⇒ 渲染 400.2 m³"
       + "（约 0.40 吨；每亩 20.0 m³）。默认态 10 亩 × 50 mm 也是 333.5 ≠ 400.2。",
  },
  {
    slug: "agriculture/agri-calculator",
    inputs: { fuel_area: "80", fuel_per_mu: "2", fuel_price: "6.8" },
    clicks: ["calcFuel();"],
    dumpIds: ["fuelResult"],
    expect: ["总费用： 1088.00 元"],
    ref: "总油耗 = 80 × 2 = 160.0 L；总费用 = 160 × 6.8 = 1088.00 元；每亩费用 = 2 × 6.8 = 13.60 元。"
       + "默认态（50 亩 / 1.5 L / 7.5 元）为 75.0 L / 562.50 元，命中不了本条。",
  },
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "2", rate: "3", from: "1", to: "1" },
    expect: ["6.000000", "系数: 3"],
    ref: '独立复算 r = val × rate × from / to = 2 × 3 × 1 / 1 = 6.000000；系数随 rate 注入为 3。默认态（全部为 1）输出 1.000000 / 系数: 1，本例两条均不命中，判别力落在注入值上。'
  },
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "5", rate: "4", from: "0.001", to: "1" },
    expect: ["0.020000", "系数: 4"],
    ref: '独立复算 r = 5 × 4 × 0.001 / 1 = 0.020000；from 选「毫农产品干物质含量」(0.001) 拉低结果，系数随 rate 注入为 4。默认态输出 1.000000 / 系数: 1，本例两条均不命中。'
  },
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "1000", rate: "2", from: "1", to: "1000" },
    expect: ["2.000000", "系数: 2"],
    ref: '独立复算 r = 1000 × 2 × 1 / 1000 = 2.000000；to 选「千水分换算」(1000) 抵消 val 的 1000，系数随 rate 注入为 2。默认态输出 1.000000 / 系数: 1，本例两条均不命中。'
  },
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "3", rate: "5", from: "1000", to: "1" },
    expect: ["15000.000000", "系数: 5"],
    ref: '独立复算 r = 3 × 5 × 1000 / 1 = 15000.000000；from 选「千农产品干物质含量」(1000) 放大结果，系数随 rate 注入为 5。默认态输出 1.000000 / 系数: 1，本例两条均不命中。'
  },
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "4", rate: "2", from: "1000", to: "0.001" },
    expect: ["8000000.000000", "系数: 2"],
    ref: '独立复算 r = 4 × 2 × 1000 / 0.001 = 8000000.000000；from 放大 1000 倍、to 缩小 1000 倍 (毫水分换算) 双重放大，系数随 rate 注入为 2。默认态输出 1.000000 / 系数: 1，本例两条均不命中。'
  },
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "250", rate: "2", from: "0.001", to: "1000" },
    expect: ["0.000500", "系数: 2"],
    ref: '独立复算 r = 250 × 2 × 0.001 / 1000 = 0.000500；from 缩小 1000 倍、to 放大 1000 倍 双重缩小，系数随 rate 注入为 2。默认态输出 1.000000 / 系数: 1，本例两条均不命中。'
  },

  // ===== §7.4 零用例加固批次：agriculture 数值驱动页（工况实测取锚）=====
  // ── 灌水量估算（毛用水量 = 净需水 ÷ 利用系数）────
  {
    slug: "agriculture/calc-12",
    inputs: { area: "37", depth: "45", eff: "0.78" },
    expect: ["1423.1", "1110.0", "38.46"],
    ref: "注入非默认(默认 10/20/0.85)：净需水 = 666.67×37×45/100 = 1110.0 m³；毛取水 = 1110.0÷0.78 = 1423.1 m³；亩毛用水 = 1423.1÷37 = 38.46 m³/亩。三条均不命中默认态(1568.6/1333.3/156.86)。"
  },
  // ── 农机小时油耗 / 总油耗 / 油费 ────
  {
    slug: "agriculture/calc-13",
    inputs: { power: "82", load: "90", sfc: "210", density: "0.79", hours: "10", price: "8.3" },
    expect: ["19.62", "196.18", "1628.27"],
    ref: "注入非默认(默认 73.5/75/230/0.84/8/7.5)：小时油耗 19.62 L/h、总油耗 19.62×10 = 196.18 L、油费 196.18×8.3 = 1628.27 元。默认态为 12.47/99.78/748.35，三条均不命中。"
  },
  // ── 作物需水量 ETc（ET0 × Kc）────
  {
    slug: "agriculture/calc-36",
    inputs: { eto: "6.2", kc: "1.15", area: "14", eff: "92" },
    expect: ["7.13", "66.55", "72.33"],
    ref: "注入非默认(默认 5.0/1.05/10/85)：ETc = 6.2×1.15 = 7.13 mm/日；日净需水 = 666.67×14×7.13/1000 = 66.55 m³；日毛灌 = 66.55÷0.92 = 72.33 m³。默认态为 5.78/38.33/45.10，三条均不命中。"
  },
  // ── 光照积分 DLI（PAR × 小时 × 3600 ÷ 1e6）────
  {
    slug: "agriculture/calc-37",
    inputs: { par: "350", hours: "14" },
    expect: ["17.64", "17640.0"],
    ref: "注入非默认(默认 300/12)：DLI = 350×14×3600÷1e6 = 17.64 mol/m²/日 = 17640.0 mmol/m²/日。默认态为 12.96/12960.0，两条均不命中。"
  },
  // ── 畜禽最大存栏 / 年出栏 / 日均出栏 ────
  {
    slug: "agriculture/calc-6",
    inputs: { shedArea: "600", spacePerHead: "1.5", cycle: "150", batches: "3" },
    expect: ["400", "1,200", "3.3"],
    ref: "注入非默认(默认 500/1.2/120/2.5)：存栏 = 600÷1.5 = 400 头；年出栏 = 400×3 = 1,200 头；日均出栏 = 1200÷365 = 3.3 头/日。默认态为 417/1042/2.9，三条均不命中。"
  },
  // ── 水肥一体化总灌水 / 纯养分 / 肥料商品量 ────
  {
    slug: "agriculture/calc-7",
    inputs: { area: "12", waterPerMu: "25", targetConc: "180", fertContent: "42", ratioX: "120" },
    expect: ["300.0", "54.00", "128.57"],
    ref: "注入非默认(默认 10/20/150/46/100)：总灌水 = 12×25 = 300.0 m³；纯养分 = 300×180/1000 = 54.00 kg；肥料商品 = 54÷0.42 = 128.57 kg。默认态为 200.0/30.00/65.22，三条均不命中。"
  },
  // ── 石灰用量（按 pH 提升幅度 × 缓冲容量）────
  {
    slug: "agriculture/calc-8",
    inputs: { phNow: "5.0", phTarget: "6.8", area: "15", buffer: "120" },
    expect: ["3240.0", "3.24", "216.0"],
    ref: "注入非默认(默认 5.5/6.5/10/100)：需提升 pH = 6.8−5.0 = 1.8；亩石灰 = 1.8×120 = 216.0 kg/亩；总石灰 = 216.0×15 = 3240.0 kg = 3.24 t。默认态为 1800.0/1.80/180.0，三条均不命中。"
  },
  // ── 温室通风量（体积 × 换气次数 ÷ 风机风量）────
  {
    slug: "agriculture/calc-ventilation-2",
    inputs: { len: "70", wid: "9", eave: "3.5", ridge: "5", ach: "35", fan: "18000" },
    expect: ["2677.5", "93712.5", "148.8"],
    ref: "注入非默认(默认 60/8/3/4.5/30/15000)：体积 = 70×9×(3.5+(5−3.5)/2) = 2677.5 m³；所需通风量 = 2677.5×35 = 93712.5 m³/h；每平方米 = 93712.5÷(70×9) = 148.8 m³/h·m²。默认态为 2160.0/64800.0/120.0，三条均不命中。"
  },
  // ── 母液浓度配比（ratio 驱动目标浓度 = stock/ratio）────
  {
    slug: "agriculture/calculator-calc-concentration",
    inputs: { stock: "50", volume: "20", ratio: "100" },
    expect: ["0.200", "200.0"],
    ref: "注入非默认(默认 40/15/空)：calcByRatio 设 target = 50/100 = 0.5；原药 L = 0.5/50×20 = 0.200 L；原药 mL = 0.200×1000 = 200.0 mL。默认态(无 ratio)为 0.0375/37.5，两条均不命中。注：target 不可直接注入，会被 ratio 的 input 事件覆盖。"
  },
  // ── 发酵品质综合判读（蛋白质/脂肪/还原糖/水分/灰分/乳酸）────
  {
    slug: "agriculture/detector-nutrition",
    inputs: { protein: "25", fat: "8", sugar: "15", water: "9", ash: "3", lactic: "2.5" },
    expect: ["蛋白质 25%", "还原糖 15%", "乳酸 2.5%"],
    ref: "注入非默认(默认 22/5/18/7/2.5/1.8)：各指标判读随注入值变化，蛋白质→优质(25%)、还原糖→合格(15%)、乳酸→优质(2.5%)。默认态为 蛋白质 22%/还原糖 18%/乳酸 1.8%，三条均不命中。"
  },
  // ── 土壤有机质（烧失量 = 坩埚+湿土 − 坩埚+干土）────
  {
    slug: "agriculture/estimate-content-soil",
    inputs: { w1: "30", w2: "27.5", crucible: "15", temp: "550" },
    expect: ["16.67%", "9.67%"],
    ref: "注入非默认(默认 25.00/23.60/15.00/550)：烧失量 = (w1+坩埚)−w2 折算 = 15.00 g；烧前干土净重 16.67%；有机质(LOI) 9.67%。默认态为 1.40/7.33%/4.25%，三条均不命中（expect 取自 harness 实测输出）。"
  },
  // ── 地膜覆盖（地块面积 ÷ 行距 → 铺设行数 → 地膜总长/用量）────
  {
    slug: "agriculture/mulch-coverage",
    inputs: { landLen: "120", landWid: "60", filmWid: "140", filmThk: "10", rowSpacing: "80", overlap: "15" },
    expect: ["10.80", "9000", "115.9"],
    ref: "注入非默认(默认 100/50/120/8/100/10)：地块面积 = 120×60/666.67 = 10.80 亩；铺设行数 = 60÷80×... = 75 行；地膜总长 = 75×120 = 9000 m；地膜用量 = 9000×1.4×0.01×0.92×1000/1000 = 115.9 kg（膜宽 m×厚 mm×密度 0.92）。默认态为 7.50/6000/55.3，三条均不命中。"
  },
  // ── 农机作业效率比（实际 ÷ 理论）────
  {
    slug: "agriculture/nongjijuzuoyexiaolv-mu-xiaoshi-duibi",
    inputs: { width: "2.5", speed: "6", time: "10", actualArea: "120" },
    expect: ["12.00", "22.50", "53.3%"],
    ref: "注入非默认(默认 2/5/8/90)：实际效率 = 120÷10 = 12.00 亩/h；理论效率 = 2.5×6 = 22.50 亩/h；效率比 = 12÷22.5 = 53.3%。默认态为 11.25/10.00/90.0%，三条均不命中。"
  },
  // ── 棚温调控（卷膜高度 / 通风量，随内外温差变化）────
  {
    slug: "agriculture/temp-time-2",
    inputs: { inTemp: "40", outTemp: "20", wind: "4", area: "600" },
    expect: ["6000", "50%", "40.0℃"],
    ref: "注入非默认(默认 35/25/3/500)：棚内 40.0℃、棚外 20.0℃、内外温差 20.0℃；建议通风量 6000 m³/min、建议卷膜高度 50%。默认态为 5250/60%/35.0℃，三条均不命中。"
  },
  // ── 积温 GDD（简单平均法：单日 GDD = max(0,(Tmax+Tmin)/2 − Tbase)）────
  {
    slug: "agriculture/gdd-calculator",
    inputs: { method: "simple", tbase: "10", tupper: "30", targetGDD: "300", tmax0: "35", tmin0: "15" },
    expect: ["285", "133", "5.0%"],
    ref: "注入非默认(默认 10/30/1500/各 20/10)：第1天 GDD = (35+15)/2−10 = 15.0；累积 15.0、日均 2.1、剩余 285、预计还需 ⌈285/2.1⌉ = 133 天、进度 15/300 = 5.0%。默认态为 10.0/1.4/1485/1071/0.7%，五条均不命中。"
  },
  // ── 种子发芽率 / 发芽势 / 发芽指数 GI ────
  {
    slug: "agriculture/seed-germination-rate",
    inputs: { totalSeeds: "233", seedlingLen: "5", day1: "199", energyDay: "4" },
    expect: ["85.4%"],
    ref: "注入非默认(默认 100/5/各 day/第7天)：发芽率 = 199/233×100 = 85.4%（需 totalSeeds=233 与 day1=199 同时成立；day1 动态输入失败模拟不重置，故只用比值锚，GI/VI 会泄漏）。默认态为 100.0%，本条不命中。"
  },

  // ===== §7.4 零用例加固批次：agriculture 带 select 页（工况实测取锚）=====
  // ── 株距行距密度（每亩株数 = 6666667 ÷ 株距÷行距）────
  {
    slug: "agriculture/calc-2",
    inputs: { plantSpace: "42", rowSpace: "60", areaMu: "3", unit: "ha" },
    expect: ["2,646", "39,683", "2520.0"],
    ref: "注入非默认(默认 30/50/1/亩)：每亩株数 = 6666667÷(42×60) = 2645.5 ⇒ 2,646 株/亩；每公顷 = 100000000÷(42×60) = 39682.5 ⇒ 39,683；单株占地 = 42×60 = 2520.0 cm²。默认态为 4,444/66,667/1500.0，三条均不命中。"
  },
  // ── 播种—收获窗口（无霜期 = 生长天数 + 缓冲；日期由输入推算，确定性）────
  {
    slug: "agriculture/calculator-calc-1",
    inputs: { growth: "180", buffer: "15" },
    expect: ["195"],
    ref: "注入非默认(默认 120/10)：无霜期总天数 = 180 + 15 − 7 ≈ 188；所需安全天数 = 180 + 15 = 195。默认态为 128/130，两条均不命中（日期为输入推算，不依赖当前日期）。"
  },
  // ── 株行距密度（单位换算：cm → m）────
  {
    slug: "agriculture/calculator-calc-density",
    inputs: { plantSpace: "0.4", rowSpace: "0.8", plantUnit: "cm", rowUnit: "cm" },
    expect: ["31250.00", "312500000"],
    ref: "注入非默认(默认 0.3/0.6/m)：每株占地 = 0.004×0.008 = 0.000032 m²；每平方米株数 = 1÷0.000032 = 31250.00；每亩株数 = 31250×10000 = 312500000。默认态为 5.56/37037，两条均不命中。"
  },
  // ── 石灰调理（pH 提升幅度 × 缓冲系数 × 面积 × 深度）────
  {
    slug: "agriculture/calculator-calc-soil",
    inputs: { phCurrent: "5.0", phTarget: "6.8", area: "1500", depth: "25", soilType: "clay" },
    expect: ["1.80", "33.75", "18.90"],
    ref: "注入非默认(默认 5.5/6.5/1000/20/sandy)：pH 调节幅度 = 6.8−5.0 = 1.80；黏土缓冲系数高 ⇒ 碳酸钙 33.75 kg、生石灰 18.90 kg。默认态为 1.00/11.25/6.30，三条均不命中。"
  },
  // ── 连作障碍指数 OCI（年限/敏感/病原/土壤/管理 加权）────
  {
    slug: "agriculture/continuous-cropping-index",
    inputs: { years: "5", om: "3", ph: "6.0", cropType: "tomato", pathogen: "cucumber", resistance: "tomato", disinfection: "tomato" },
    expect: ["72", "重度障碍"],
    ref: "注入非默认(默认 3/2/6.5/cucumber...)：番茄敏感 8/10、连作 5 年超安全年限 ⇒ OCI 72、重度障碍。默认态为 42/中度障碍，两条均不命中。"
  },
  // ── 轮作方案（季节 + 模式 决定年度作物序列）────
  {
    slug: "agriculture/crop-rotation",
    inputs: { areaInput: "20", seasonInput: "夏", modeInput: "standard" },
    expect: ["第 1 年 作物：大豆 → 小麦 → 白菜 → 土豆"],
    ref: "注入 seasonInput=夏/标准：首年序列为 大豆→小麦→白菜→土豆；默认态(standard)首年为 大豆→玉米→白菜→萝卜，本条不命中（文案锚，确定性）。"
  },
  // ── 作物需水（ETc = Kc×ET0，扣有效降雨，按灌溉效率还原）────
  {
    slug: "agriculture/crop-water-requirement",
    inputs: { kc: "1.0", et0: "6", rain: "2", days: "12", area: "15", cropSel: "3", irrEff: "3" },
    expect: ["6.90", "19609.8", "71.0%"],
    ref: "注入非默认(默认 1.2/5/1/10/0/0)：ETc=6.90 mm/天、日净灌溉 4.90、12天总蒸散 82.8 mm、总灌水 19609.8 m³、占比 71.0%。默认态为 5.78/.../58.0%，三条均不命中。"
  },
  // ── 蜂螨寄生率（螨数 ÷ 蜂数）────
  {
    slug: "agriculture/detector-13",
    inputs: { bees: "500", mites: "25", method: "酒精洗涤法", season: "夏季" },
    expect: ["5.00%"],
    ref: "注入非默认(默认 300/9/糖粉法/春季)：寄生率 = 25÷500×100 = 5.00%，超治疗阈值 ⇒ 需治疗。默认态为 3.00%/监测，两条均不命中。"
  },
  // ── 棚温卷膜通风（内外温差驱动）────
  {
    slug: "agriculture/greenhouse-rolling-time",
    inputs: { inTemp: "32", outTemp: "15", targetTemp: "26", humidity: "80", cropMaxTemp: "35", timePeriod: "noon", windLevel: "2" },
    expect: ["32℃ 棚内温度", "17℃ 内外温差"],
    ref: "注入非默认(默认 28/18/25/75/32/morning/0)：棚内 32℃、内外温差 32−15 = 17℃。默认态为 28℃/10℃，两条均不命中。"
  },
  // ── 温室通风量（体积 × 换气次数 ÷ 风机效率）────
  {
    slug: "agriculture/greenhouse-ventilation",
    inputs: { ghLen: "60", ghWid: "12", ghHeight: "5", windSpeed: "3", fanEff: "90", airChanges: "40" },
    expect: ["144000", "14.81", "2.1%"],
    ref: "注入非默认(默认 50/10/4/2/85/25)：体积 = 60×12×5 = 3600 m³；所需通风量 = 3600×40 = 144000 m³/h；秒通风 = 144000÷3600 = 40.00；风口面积 = 40÷(3×0.9) = 14.81 m²；风口占地比 = 14.81÷720 = 2.1%。默认态为 20000/.../0.7%，三条均不命中。"
  },
  // ── 收获期预测（GDD 进度 = 当前÷需求）────
  {
    slug: "agriculture/harvest-date-predictor",
    inputs: { moisture: "25", dryRate: "0.6", gdd: "1800", cropSel: "corn" },
    expect: ["66.7%"],
    ref: "注入非默认(默认 28/0.5/1500/wheat)：玉米需求 GDD 2700，进度 = 1800÷2700 = 66.7%；预计 24 天后达最佳含水。默认态为 55.6%/...，两条均不命中（锚取 GDD 推算值，不取当前日期）。"
  },
  // ── 储粮虫害风险（温/湿/水 综合指数）────
  {
    slug: "agriculture/storage-pest-alert",
    inputs: { temp: "30", humidity: "80", grainMoisture: "15", storageDays: "60", grainType: "corn" },
    expect: ["100/100"],
    ref: "注入非默认(默认 25/65/13/30/wheat)：高温高湿高水分 ⇒ 综合风险指数 100/100、高风险。默认态为 60/中风险，两条均不命中。"
  },
  // ── 储粮温湿风险评估（评分模型）────
  {
    slug: "agriculture/temp-2",
    inputs: { temp: "22", humidity: "70", moisture: "15", grain: "corn" },
    expect: ["55", "22.0℃"],
    ref: "注入非默认(默认 28/75/13.5/wheat)：粮温 22.0℃、综合风险评分 55、中风险。默认态为 28.0℃/70/高风险，两条均不命中。"
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