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
  // ── 水肥 EC 注肥比例：EC 差超过母液 EC（物理不可能，需拦截）────
  {
    slug: "agriculture/ratio-10",
    inputs: { targetEC: "3.0", waterEC: "0.5", fertEC: "2.0", targetPH: "6.0" },
    expect: ["提高到至少 2.50 dS/m"],
    ref: "非默认输入：肥料 EC 贡献 = 3.0 − 0.5 = 2.50 > 母液 EC 2.0 ⇒ 注肥比例将超过 100%，页面必须拦截并给出所需最小母液 EC 2.50 dS/m（旧实现会显示 125.00%）。默认态贡献 1.5 < 2.5，不进入该分支。"
  },
  // ── 干物质换算（干物质 = 鲜重 × (1 − 含水率)）────────────────────
  {
    slug: "agriculture/dry-matter-conversion",
    inputs: { freshWeight: "1000", moisture1: "20" },
    expect: ["800.00", "200.00", "80.0%"],
    ref: "干物质 = 1000 × (1 − 0.2) = 800.00；水分 = 1000 − 800 = 200.00；"
       + "干物质率 = 80.0%",
  },
  // ── 含水率越界（>100%）必须输入侧拦截，避免负干物质/除零 ──────────
  {
    slug: "agriculture/dry-matter-conversion",
    inputs: { freshWeight: "1000", moisture1: "120" },
    expect: ["鲜重须大于 0，含水率须在 0–100% 之间"],
    ref: "含水率 120% 旧实现算得干物质 −200.00 kg 仍照常输出；修复后拦截。默认 75% 不出现该提示。",
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
    ref: "理论产量 0 → 损失率 = (0-415)/0×100 = NaN；修复前输出 NaN%，应给守卫提示 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
{
    slug: "agriculture/assessor-1",
    inputs: { theoryYield: "500", actualYield: "450", fieldLoss: "20", threshLoss: "10" },
    expect: ["10.00", "4.00", "2.00"],
    ref: "损失率=(500-450)/500×100=10.00%；田间落粒=20/500×100=4.00%；脱粒=10/500×100=2.00%；"+
         "机械标准限值 3.0%，10%>3×1.5=4.5% → 不合格（修复前 10%>3% 即标红但不写阈值比较）",
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
      nFert: "34", nPct: "46", pFert: "46", pPct: "46", kFert: "50", kPct: "60",
      price: "3.2", nEff: "55", pEff: "22", kEff: "65" },
    dumpIds: ["res"],
    expect: ["1422.92", "3893.89", "12460.44"],
    ref: "独立复算：N = 150 ÷ (0.46 × 0.55) × 2.4 = 1422.924901 ⇒ 1422.92；P = 75 ÷ (0.46 × 0.22) × 2.4 = 1778.656126 ⇒ 1778.66（本页只取 2 位）；K = 112.5 ÷ (0.60 × 0.65) × 2.4 = 692.307692 ⇒ 692.31；总量 3893.888720 ⇒ 3893.89；成本 = 3893.888720 × 3.2 = 12460.4439 ⇒ 12460.44。pFert 取 46 的重过磷酸钙（data-n 缺省 = 0，不带 DAP 氮抵扣）。默认态为 521.74 / 1293.48 / 1293.48，三条均不命中。",
  },
  // ── 配方施肥量：选 DAP（18-46-0）时应从氮肥用量中抵扣其携入氮 ──
  {
    slug: "agriculture/calculator-calc-ratio",
    inputs: { nNeed: "150", pNeed: "75", kNeed: "0", area: "2.4",
      nFert: "34", nPct: "46", pPct: "46", kFert: "50", kPct: "60",
      price: "0", nEff: "55", pEff: "22", kEff: "65" },
    clicks: ["document.getElementById('pFert').selectedIndex=1;calc();"],
    dumpIds: ["res"],
    expect: ["157.48 氮肥用量", "320.16 DAP 携入氮", "1936.13 肥料总量"],
    ref: "独立复算：pFert 取第 2 项 DAP（value=46、data-n=18）⇒ P = 75 ÷ (0.46 × 0.22) × 2.4 = 1778.6561 kg，携入纯氮 = 1778.6561 × 18% = 320.1581 ⇒ 320.16 kg；N 需求 = 150 × 2.4 = 360，抵扣后 = 39.8419，尿素 = 39.8419 ÷ (0.46 × 0.55) = 157.4779 ⇒ 157.48 kg；总量 = 157.48 + 1778.66 = 1936.13 kg。旧实现不抵扣 DAP 携入氮会得 1422.92 kg 且不显示携入氮卡，三条均不命中。",
  },
  // ── 作物施肥配方（单产系数放大 Needs，肥料按含量反算用量）──
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: { crop: "1", yield: "620", area: "12", fertN: "3", fertP: "5", fertK: "9" },
    dumpIds: ["result"],
    expect: ["1207.6", "681.2", "1 : 0.50 : 0.72"],
    ref: "独立复算（CROPS[1]=小麦 yield450 n14 p7 k10；FERTILIZERS[3]=硝酸铵 n34、[5]=重过磷酸钙 p46、[9]=氯化钾 k60）：factor = 620 ÷ 450 = 1.377778；needN = 14 × 1.377778 = 19.2889 ⇒ 19.3、needP = 7 × 1.377778 = 9.6444 ⇒ 9.6、needK = 10 × 1.377778 = 13.7778 ⇒ 13.8；亩养分总量 = 19.2889 + 9.6444 + 13.7778 = 42.7111 ⇒ 42.7；硝酸铵 = 19.2889 × 12 ÷ 0.34 = 681.1765 ⇒ 681.2（产物同为 56.8 kg/亩 = 681.1765 ÷ 12）；重过磷酸钙 = 9.6444 × 12 ÷ 0.46 = 250.4348 ⇒ 250.4；氯化钾 = 13.7778 × 12 ÷ 0.60 = 276.0；总施肥量 = 1207.6113 ⇒ 1207.6；NPK 比 = 9.6444 ÷ 19.2889 = 0.4978 ⇒ 0.50、13.7778 ÷ 19.2889 = 0.7155 ⇒ 0.72。默认态为 575.0 / 375.0 / 200.0 / 1 : 0.50 : 0.83，三条均不命中。注：crop / fertN / fertP / fertK 的 option value 是 CROPS / FERTILIZERS 的数组下标字符串，灌作物名（如 wheat）会取到 undefined。",
  },
  // ── 磷/钾肥携入氮抵扣（2026-11-04）：磷酸二铵 18%N 须先从氮需求中扣除 ──
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: { crop: "1", yield: "450", area: "10", needN: "12", needP: "2", needK: "1", fertN: "0", fertP: "6", fertK: "9" },
    clicks: ["calc();"],
    dumpIds: ["result"],
    expect: ["243.9", "304.0", "7.8 kg（0.8 kg/亩）"],
    ref: "独立复算（FERTILIZERS[6]=磷酸二铵 n18/p46、[9]=氯化钾 k60、[0]=尿素 n46）：amtP = 2×10 ÷ 0.46 = 43.4783 kg，携入氮 = 43.4783 × 18% = 7.8261 ⇒ 7.8 kg（0.8 kg/亩）；剩余氮 = 120 − 7.8261 = 112.1739，尿素 = 112.1739 ÷ 0.46 = 243.8563 ⇒ 243.9 kg；氯化钾 = 1×10 ÷ 0.60 = 16.6667 kg；总施肥量 = 243.8563 + 43.4783 + 16.6667 = 304.0013 ⇒ 304.0 kg。旧实现不抵扣携入氮会得 260.9 kg 尿素 / 321.0 kg 总量且无携入氮提示，三条均不命中。",
  },

  {
    slug: "agriculture/fertilizer-calculator",
    inputs: {},
    clicks: ["document.getElementById('period').value='top';document.getElementById('area').value='10';document.getElementById('yield').value='450';document.getElementById('needN').value='8';document.getElementById('needP').value='0';document.getElementById('needK').value='0';document.getElementById('fertN').value='0';document.getElementById('fertP').value='';document.getElementById('fertK').value='';calc();"],
    dumpIds: ["result"],
    expect: ["173.9", "1 : 0.00 : 0.00"],
    ref: "S2 预设「小麦返青期追肥」等价注入：仅追氮肥 needN=8/P0/K0、尿素(46%)。amtN = 8×10÷0.46 = 173.913 ⇒ 173.9 kg；亩养分总量 = 8.0；总施肥量 = 173.9；NPK 比 = 1 : 0/8 : 0/8 = 1 : 0.00 : 0.00。默认态(needN12/P6/K10、尿素+过磷酸钙+氯化钾)总施肥 802.6、NPK 1:0.50:0.83，两条锚均不命中。注：needP=0 不再被 guard 误拦截（已修正 __D 分母）。",
  },
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: {},
    clicks: ["document.getElementById('period').value='top';document.getElementById('area').value='10';document.getElementById('yield').value='500';document.getElementById('needN').value='5';document.getElementById('needP').value='0';document.getElementById('needK').value='4';document.getElementById('fertN').value='0';document.getElementById('fertP').value='';document.getElementById('fertK').value='8';calc();"],
    dumpIds: ["result"],
    expect: ["108.7", "1 : 0.00 : 0.80"],
    ref: "S2 预设「水稻穗肥」等价注入：N5/P0/K4、尿素(46%)+氯化钾(60%)。amtN = 5×10÷0.46 = 108.696 ⇒ 108.7 kg；amtK = 4×10÷0.60 = 66.667 ⇒ 66.7 kg；亩养分 = 9.0；总施肥量 = 175.4；NPK 比 = 1 : 0/5 : 4/5 = 1 : 0.00 : 0.80。默认态不命中两条锚。",
  },
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: {},
    clicks: ["document.getElementById('period').value='top';document.getElementById('area').value='10';document.getElementById('yield').value='550';document.getElementById('needN').value='10';document.getElementById('needP').value='0';document.getElementById('needK').value='5';document.getElementById('fertN').value='0';document.getElementById('fertP').value='';document.getElementById('fertK').value='8';calc();"],
    dumpIds: ["result"],
    expect: ["217.4", "1 : 0.00 : 0.50"],
    ref: "S2 预设「玉米大喇叭口期追肥」等价注入：N10/P0/K5、尿素(46%)+氯化钾(60%)。amtN = 10×10÷0.46 = 217.391 ⇒ 217.4 kg；amtK = 5×10÷0.60 = 83.333 ⇒ 83.3 kg；亩养分 = 15.0；总施肥量 = 300.7；NPK 比 = 1 : 0/10 : 5/10 = 1 : 0.00 : 0.50。默认态不命中两条锚。",
  },
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: {},
    clicks: ["document.getElementById('period').value='top';document.getElementById('area').value='10';document.getElementById('yield').value='5000';document.getElementById('needN').value='8';document.getElementById('needP').value='0';document.getElementById('needK').value='6';document.getElementById('fertN').value='0';document.getElementById('fertP').value='';document.getElementById('fertK').value='8';calc();"],
    dumpIds: ["result"],
    expect: ["173.9", "1 : 0.00 : 0.75"],
    ref: "S2 预设「番茄膨果期追肥」等价注入：N8/P0/K6、尿素(46%)+氯化钾(60%)。amtN = 8×10÷0.46 = 173.913 ⇒ 173.9 kg；amtK = 6×10÷0.60 = 100.0 kg；亩养分 = 14.0；总施肥量 = 273.9；NPK 比 = 1 : 0/8 : 6/8 = 1 : 0.00 : 0.75。默认态不命中两条锚。",
  },
  // ── N-P-K 折纯汇总（2026-10-26）：多肥纯养分合计，避免重复计量 ──
  {
    slug: "agriculture/fertilizer-calculator",
    inputs: {},
    clicks: ["switchTab('purity');document.getElementById('pSel0').value='0';document.getElementById('pAmt0').value='50';document.getElementById('pSel1').value='4';document.getElementById('pAmt1').value='30';calcPurity();"],
    dumpIds: ["purityTotal"],
    expect: ["23.00", "4.80"],
    ref: "折纯：尿素(46%)50kg ⇒ N=23.0kg、过磷酸钙(16%)30kg ⇒ P₂O₅=4.8kg；其余行空。合计 N 23.00 / P₂O₅ 4.80 / K₂O 0.00 kg。switchTab('purity') 先触发 initPurity 建行，再注入 pSel/pAmt 后 calcPurity()。默认态（全空）合计为 0.00，两条锚均不命中。",
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
  // ── 收获日期预测（2026-11-04）：干燥速率 0 时旧实现直接判「0 天后可收」 ──
  {
    slug: "agriculture/harvest-date-predictor",
    inputs: { dryRate: "0", moisture: "28" },
    dumpIds: ["result"],
    expect: ["请输入大于 0 的日均降水速率（%/天）"],
    ref: "干燥速率 0（%/天）时旧分支 daysToHarvest=0，页面显示「预计 0 天后达到最佳收割含水量」，与含水 28% 仍高于适收上限矛盾；现改为显式拦截。默认干燥速率 0.5 不出现该提示。",
  },
  {
    slug: "agriculture/irrigation-calculator",
    inputs: { area: "8", depth: "40", moisture: "55", cycle: "0" },
    dumpIds: ["result"],
    expect: ["灌水周期须为不小于 1 的天数"],
    ref: "周期 0 天时月灌水次数为 30÷0 = Infinity，旧实现用 `|| 7` 静默回退 7 天、掩盖非法输入；现改为显式拦截（周期 ≥ 1 天）。默认周期 7 天不出现该提示。",
  },
  {
    slug: "agriculture/irrigation-calculator",
    inputs: { crop: "0", method: "drip", soil: "clay", area: "8", depth: "40", moisture: "55", price: "0.8", cycle: "10" },
    dumpIds: ["result"],
    expect: ["全生育期需水约600 mm ≈ 400 m³/亩", "全期约需灌 8 次"],
    ref: "选作物=水稻（water 600 mm）：600 mm × 0.667 = 400.2 ⇒ 400 m³/亩；净定额沿用上条 48.6243 m³/亩 ⇒ 全期次数 = round(400.2 ÷ 48.6243) = 8。旧实现只回填湿润层深度、作物需水量与 kc 全为死数据，两条锚均不命中。",
  },
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
    expect: ["1.15 肥料浓度(g/L)", "2.07 总用肥量(kg)", "24.0 注肥速率"],
    ref: "独立复算（页面口径 1 mS/cm ≈ 0.64 g/L）：净增EC = 2.0 − 0.2 = 1.8；肥料浓度 = 1.8 × 0.64 = 1.152 → 1.15 g/L；"
       + "总流量 = 3 × 800 = 2400 L/h；灌水总量 = 2400 × (45/60) = 1800 L = 1.80 m³；"
       + "总用肥 = 1.152 × 1800 ÷ 1000 = 2.0736 → 2.07 kg；NPK 按 30-10-10 ⇒ 氮 0.62 / 磷(P₂O₅) 0.21 / 钾(K₂O) 0.21；"
       + "母液浓度 = 1.152 × 100 = 115.2 g/L、母液体积 = 1800 ÷ 100 = 18.0 L、需称肥料 2.07 kg、"
       + "注肥泵速率 = 18.0 ÷ (45/60) = 24.0 L/h。旧用例按 ÷0.5 写的 3.60/6.48 与页面口径不符，已按 0.64 更正。"
       + "默认态（1.5 / 0.3 / 2 L/h / 500 滴灌管 / 30 min / 20-20-20 / 200 倍）三锚均不命中。",
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
  // ── 冠层覆盖度（照片网格法：绿色格 ÷ 总格）────
  {
    slug: "agriculture/canopy-coverage",
    inputs: { totalGrid: "150", greenGrid: "96", photoArea: "2.5" },
    clicks: ["currentTab=1;calc();"],
    dumpIds: ["result1"],
    expect: ["64.0%", "1.60", "0.90"],
    ref: "独立复算：覆盖度 = 96÷150×100 = 64.0%；冠层面积 = 2.5×0.64 = 1.60 m²；裸地 = 2.5−1.60 = 0.90 m²。默认态（100 格 / 65 绿 / 1 m²）为 65.0% / 0.65 / 0.35，三条均不命中。",
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
  // ── 地膜覆盖：行距大于有效膜宽（无重叠，覆盖率 <100%）────
  {
    slug: "agriculture/mulch-coverage",
    inputs: { landLen: "120", landWid: "40", filmWid: "100", filmThk: "8", rowSpacing: "200", overlap: "0" },
    expect: ["7.20", "50.0%", "17.7"],
    ref: "独立复算：地块面积 = 120×40/666.67 = 7.20 亩（4800 m²）；铺膜行数 = 40×100÷200 = 20 行；膜长 = 20×120 = 2400 m；有效膜宽 = 1.00 m ⇒ 铺设面积 2400 m² < 地块 4800 m²，覆盖率 = 50.0%，重叠率 = 0.0%，膜重 = 2400×1.0×8e-6×920 = 17.7 kg。默认态为 7.50 亩 / 100.0% / 44.2 kg，三条派生锚均不命中；「0.0%」在默认输出里已存在（属静态/回退命中），故不再作为 expect，只留三个随注入改变的数值锚。"
  },
  // ── 农机作业效率比（实际 ÷ 理论）────
  {
    slug: "agriculture/nongjijuzuoyexiaolv-mu-xiaoshi-duibi",
    inputs: { width: "2.5", speed: "6", time: "10", actualArea: "120" },
    expect: ["12.00", "22.50", "53.3%"],
    ref: "注入非默认(默认 2/5/8/90)：实际效率 = 120÷10 = 12.00 亩/h；理论效率 = 2.5×6 = 22.50 亩/h；效率比 = 12÷22.5 = 53.3%。默认态为 11.25/10.00/90.0%，三条均不命中。"
  },
  // ── 农机作业效率：实际面积超过理论面积（效率比须封顶 100% 并告警）────
  {
    slug: "agriculture/nongjijuzuoyexiaolv-mu-xiaoshi-duibi",
    inputs: { width: "3", speed: "8", time: "5", actualArea: "300" },
    expect: ["60.00 实际效率", "100.0% 效率比", "实际面积比理论值多 120.00 亩"],
    ref: "独立复算：理论面积 = 3×8×5×1.5 = 180 亩；实际效率 = 300÷5 = 60.00 亩/h；理论效率 = 180÷5 = 36.00 亩/h ⇒ 原始比值 166.7%，实际面积超出 120.00 亩，必须封顶为 100.0% 并输出「实际面积比理论值多 120.00 亩」。旧实现不封顶会显示 166.7%、损失面积 -84 亩；默认态（2/5/8/90）为 11.25/90.0%/损失 30 亩，三条均不命中。"
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
    expect: ["285", "19", "5.0%"],
    ref: "注入非默认(默认 10/30/1500/各 20/10)：第1天 GDD = (35+15)/2−10 = 15.0；累积 15.0、日均 15.0（仅统计已填写行、留空行不再按 0 计入）、剩余 285、预计还需 ⌈285/15⌉ = 19 天、进度 15/300 = 5.0%。默认态为 10.0/1.4/1485/1071/0.7%，五条均不命中。"
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
    expect: ["1.80", "506.25", "283.50", "33.75"],
    ref: "注入非默认(默认 5.5/6.5/1000/20/sandy)：pH 调节幅度 = 6.8−5.0 = 1.80；黏土系数 15 kg/(100㎡·pH)、深度系数 25/20=1.25 ⇒ CaCO₃ = 1.8×15×1500/100×1.25 = 506.25 kg；生石灰 CaO = 506.25×0.56 = 283.50 kg；每 100㎡ = 506.25÷1500×100 = 33.75 kg。旧系数 1.0 会得 33.75/18.90，与 506.25/283.50 明显不同；默认态为 1.00/60.00/33.60/6.00，四条均不命中。"
  },
  // ── NDVI 单点：反射率超出 0–1 必须拦截（旧实现会算出 0.6 并误判茂密）──
  {
    slug: "agriculture/analysis-21",
    inputs: { nir: "1.5", red: "0.2", batch: "0.8,0.2" },
    dumpIds: ["res", "batchRes"],
    expect: ["请输入 0–1 范围内的反射率"],
    ref: "独立复算：NIR=1.5 超出反射率合法区间 0–1 ⇒ 页面必须给出「请输入 0–1 范围内的反射率（NIR、RED），且两者之和不能为 0」，而不是按 (1.5−0.2)/(1.5+0.2)=0.7647 输出分级。默认输入 0.35/0.10 合法、不含该提示 ⇒ 只有范围校验分支生效才命中。"
  },
  // ── NDVI 批量：非法行标「输入异常」，合法行按公式分级 ──
  {
    slug: "agriculture/analysis-21",
    inputs: { nir: "0.7", red: "0.1", batch: "1.2,0.3\n0.7,0.1\n0.5,0.5" },
    dumpIds: ["res", "batchRes"],
    expect: ["输入异常", "0.7500 茂密植被 / 森林", "0.0000 裸土 / 岩石 / 建筑"],
    ref: "独立复算：单点 (0.7−0.1)/(0.7+0.1)=0.600/0.800=0.7500 ⇒ 茂密植被/森林；批量第 1 行 NIR=1.2 越界 ⇒ 输入异常，第 2 行 0.7500 茂密，第 3 行 (0.5−0.5)/1.0=0.0000 ⇒ 裸土。默认单点 0.35/0.10=0.5556、批量仅一行，三条锚均不命中。"
  },
  // ── 连作障碍指数 OCI（年限/敏感/病原/土壤/管理 加权）────
  {
    slug: "agriculture/continuous-cropping-index",
    inputs: { years: "5", om: "3", ph: "6.0", cropType: "tomato", pathogen: "3", resistance: "0", disinfection: "1" },
    expect: ["72", "重度障碍"],
    ref: "注入非默认(默认 3/2/6.5/cucumber/病原3/抗性1/消毒1)：番茄敏感 8/10、连作 5 年超安全年限(2 年) ⇒ 年限因子封顶 100、病原 60、土壤 20、管理 80 ⇒ OCI=30+16+15+3+8=72、重度障碍。旧用例把 select 塞成 cucumber/tomato 等非法值，靠 NaN 静默回退才得出 72；改为合法档位后同样命中，默认态 64.75/中度障碍两条均不命中。"
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
  // ── 作物需水：计算天数 0 与负值必须显式拒绝（旧实现 `|| 1` 把 0 当 1 天）──
  {
    slug: "agriculture/crop-water-requirement",
    inputs: { kc: "1.0", et0: "6", rain: "2", days: "0", area: "15", cropSel: "3", irrEff: "70" },
    expect: ["计算天数必须大于0"],
    ref: "天数 0：旧实现 `+value || 1` 回退成 1 天并照常输出（总蒸散 6.0 mm、总灌水 75.4 m³）；修复后显式拒绝。默认 days=10 正常计算，不出现该提示。"
  },
  {
    slug: "agriculture/crop-water-requirement",
    inputs: { kc: "1.0", et0: "6", rain: "2", days: "-5", area: "15", cropSel: "3", irrEff: "70" },
    expect: ["计算天数必须大于0"],
    ref: "天数 −5：旧实现接受负值（总蒸散 −30 mm、总灌水为负）；修复后显式拒绝。默认 days=10 不出现该提示。"
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
  // ── 棚温卷膜（温度达标但湿度 >85%，需短时排湿）────
  {
    slug: "agriculture/greenhouse-rolling-time",
    inputs: { inTemp: "26", outTemp: "18", targetTemp: "26", humidity: "95", cropMaxTemp: "35", timePeriod: "noon", windLevel: "1" },
    expect: ["温度26℃在合理范围，但湿度95%偏高，需短时通风排湿", "短时卷膜排湿 15–30 分钟"],
    ref: "独立复算：棚温 26℃ 等于目标 26℃ ⇒ 温度分支为 maintain；湿度 95% > 85 且非早晨 ⇒ 本页改判卷膜通风并输出动态原因「温度26℃在合理范围，但湿度95%偏高，需短时通风排湿」与高湿分支独有操作「短时卷膜排湿 15–30 分钟」。默认态（28/18/75/morning）不含这两句，且旧实现维持现状时也不产生 ⇒ 只有高湿分支生效才会命中。"
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
  // ── 生育期天数（单输入，输出随 growthDays 变化；日期为推算，不取锚）────
  {
    slug: "agriculture/calc-15",
    inputs: { growthDays: "180" },
    expect: ["180 生育期天数"],
    ref: "注入非默认(默认 120)：生育期天数 = growthDays = 180 天。默认态为 120 生育期天数，本条不命中（日期为推算值，仅取天数锚）。"
  },
  {
    slug: "agriculture/straw-return",
    inputs: { targetCN: "30", fertType: "sulfate", soilOM: "3.6" },
    expect: ["目标C/N比：30:1", "需补硫酸铵：19.0 kg/亩（含纯氮4.00kg）", "预计分解周期：60天", "土壤有机质适中(3.6%)"],
    ref: "碳/氮/秸秆量由 onStrawChange 从 strawType 静态表回填，harness 注入会被覆盖 ⇒ 只注三个静态项。Python Decimal 复算：碳输入 = 45%×400 = 180.00 kg/亩；目标 30:1 ⇒ 需纯氮 = 180.00/30 − 0.5%×400 = 6.000 − 2.000 = 4.000；硫酸铵含氮 21% ⇒ 4.000/0.21 = 19.0476 → toFixed(1) = 19.0。默认态为 20:1 + 尿素 + 1.5%，四个锚全不命中。"
  },
  {
    slug: "agriculture/straw-return",
    inputs: { targetCN: "25", fertType: "carbonate", soilOM: "0.8" },
    expect: ["目标C/N比：25:1", "需补碳铵：30.6 kg/亩（含纯氮5.20kg）", "预计分解周期：45天", "土壤有机质偏低(0.8%)"],
    ref: "Python Decimal 复算：需纯氮 = 180.00/25 − 2.000 = 7.200 − 2.000 = 5.200；碳铵含氮 17% ⇒ 5.200/0.17 = 30.5882 → toFixed(1) = 30.6。默认态 20:1 + 尿素 + 1.5% ⇒ 四锚全不命中；且 25:1 与默认输出的「20-25:1」区间串不同（锚取「目标C/N比：25:1」整段，非裸 25:1）。"
  },
  // ── 秸秆还田：目标 C/N 为空/0 时不得 `|| 25` 静默回退 ──────────
  {
    slug: "agriculture/straw-return",
    inputs: { targetCN: "", fertType: "sulfate", soilOM: "3.6" },
    clicks: ["document.getElementById('targetCN').value='';calc();"],
    expect: ["请输入有效的秸秆参数（秸秆量、碳含量、氮含量与目标C/N均须大于0）"],
    ref: "旧实现 `+value || 25` 把空值/0 静默回退成 25:1 并照常出结果，与同函数内 `targetCN<=0` 的校验声明矛盾；改为 parseFloat 后空值（NaN）显式拒绝。默认 select 为 20:1，正常计算不出现该提示。"
  },
{
    "slug": "agriculture/calc-38",
    "inputs": {
      "values": "10 20 30 40"
    },
    "expect": [
      "60.00% 克里斯琴森系数 Cu"
    ],
    "ref": "克里斯琴森均匀系数 Cu = 100 × (1 − Σ|x_i − x̄| ÷ (n·x̄))；x̄=25，Σ|x_i−x̄|=40，n·x̄=100 → Cu = 100 × (1 − 0.40) = 60.00%。页面输出 '60.00% 克里斯琴森系数 Cu'。默认态其他输入不产生 60.00%。"
  },

  // ── 零用例收敛（2026-10-09）：agriculture 8 页中仅本页可收敛 ──
  {
    "slug": "agriculture/pesticide-dose",
    "inputs": { "activePct": "25", "targetPpm": "200", "water": "45", "area": "2.5" },
    "expect": ["0.09 总用药量", "5000 稀释倍数", "113 总用水量", "11.3升", "至113升"],
    "ref": "注入 ppm 法非默认组合（默认 40% / 500ppm / 30L / 1亩）。独立复算（页面 ppm 分支公式：稀释倍数 = 10⁶ ÷ 目标ppm；每亩用药量 = (亩用水量 ÷ 稀释倍数) × (100 ÷ 有效成分%)）：稀释倍数 = 1,000,000 ÷ 200 = 5000；每亩 = (45 ÷ 5000) × (100 ÷ 25) = 0.009 × 4 = 0.036 mL ⇒ toFixed(2) = 0.04；总量 = 0.036 × 2.5 = 0.09 mL；总用水量 = 45 × 2.5 = 112.5 L ⇒ toFixed(0) = 113；母液水量 = 总用水量 × 10% = 11.25 ⇒ toFixed(1) = 11.3。四条独占锚均与默认态不同：默认态为『2000 稀释倍数 / 30 总用水量 / 3.0升 母液 / 总量 0.04』。⚠ 不用『0.04 每亩用药量』——默认态每亩 0.036 同样 toFixed(2) = 0.04，属逃生串（判别器已实测报出）。"
  },

  // ── 零用例收敛（2026-10-09）：crop-yield 此前被误判为拼接 id 盲区，实为可收敛 ──
  {
    "slug": "agriculture/crop-yield",
    "inputs": { "spikes": "123", "grains": "45", "weight": "67" },
    "expect": ["3708.4"],
    "ref": "穗数-粒数-粒重法（2026-10-26 修复量纲 bug：原代码 /100/10 多除 10，致默认小麦 40×35×45 只算 63kg/亩、恒判低产；正确公式 = 万穗×粒数×千粒重÷100）：yieldPerMu = 123×45×67/100 = 3708.45 → toFixed(1) 『3708.4』（浮点 3708.449…）；水分 13% adj 不变。默认态 40/35/45 → 630.0，本条不命中。⚠ 本页 initCrops 用 select.innerHTML 动态填『作物』选项，harness 旧版 innerHTML setter 不解析 <option> ⇒ 整页初始化失败；已在 verify_it_calc.js 的 makeEl.innerHTML setter 补 <option> 解析修复。"
  },
  // ── S2 场景预设（2026-10-26）：clicks 后置注入绕过 boot 期 initCrops→applyCrop 对 spike 输入的重置 ──
  {
    "slug": "agriculture/crop-yield",
    "inputs": {},
    "clicks": ["document.getElementById('spikes').value='22';document.getElementById('grains').value='120';document.getElementById('weight').value='27';document.getElementById('area').value='10';document.getElementById('moisture').value='13.5';calc();"],
    "expect": ["708.7", "高产(超平均25%)"],
    "ref": "S2 预设「水稻测产」等价注入：22万穗×120粒×27g/100 = 712.8 kg/亩；水分 13.5% adj = 712.8×86.5/87 = 708.7；对照水稻参考 600 → 高产(超平均18%)…实际 ratio=708.7/600=1.18 → 超平均 18%？（锚取亩产量 708.7 主值）。默认态（小麦 40/35/45/13%）→ 630.0，两锚均不命中。"
  },
  {
    "slug": "agriculture/crop-yield",
    "inputs": {},
    "clicks": ["document.getElementById('spikes').value='0.45';document.getElementById('grains').value='550';document.getElementById('weight').value='350';document.getElementById('area').value='10';document.getElementById('moisture').value='14';calc();"],
    "expect": ["856.3", "高产(超平均55%)"],
    "ref": "S2 预设「玉米测产」等价注入：0.45万穗×550粒×350g/100 = 866.25 kg/亩；水分 14% adj = 866.25×86/87 = 856.3；对照玉米参考 550 → ratio 1.557 → 高产(超平均56%)（页面整数化后 55%/56% 以实跑为准，主锚 856.3）。默认态不含 856.3。"
  },
  {
    "slug": "agriculture/crop-yield",
    "inputs": {},
    "clicks": ["document.getElementById('method').value='sample';document.getElementById('sampleArea').value='2';document.getElementById('sampleWeight').value='1.8';document.getElementById('dryFactor').value='0.85';calc();"],
    "expect": ["510.0"],
    "ref": "S2 预设「样方实测(小麦)」等价注入：样方法 1.8×0.85×666.67/2 = 510.0 kg/亩（水分默认 13% adj 不变）。默认穗数态 630.0，不命中。"
  },

  // ── 零用例收敛（2026-10-09）：pesticide-interval（确定性日期推算部分）──
  {
    "slug": "agriculture/pesticide-interval",
    "inputs": { "sprayDate": "2026-01-01", "phiDays": "7" },
    "expect": ["2026年1月8日", "2026年1月1日"],
    "ref": "施药日 2026-01-01 + PHI 7 天 ⇒ 最早采收日 2026年1月8日（formatDate 无补零）；施药日期卡 2026年1月1日。默认态 sprayDate 空 → 提示『请选择施药日期』，两条锚均不命中。（now 被 harness 冻结，距安全采收天数非确定，故只锚确定性的日期推算『施药日+PHI』。）"
  },
  {
    "slug": "agriculture/pesticide-interval",
    "inputs": { "sprayDate": "2026-01-01", "phiDays": "0" },
    "expect": ["0天", "2026年1月1日"],
    "ref": "PHI=0 为合法标签值（农业农村部农药登记标签实例标注「安全间隔期0天」，见 plan/standards-map.md）：0 天 ⇒ 最早采收日 = 施药日 2026年1月1日，数据卡显示「0天」。默认 phiDays=7 时结果为「7天」且采收日为 1月8日，两条锚均不命中（旧实现 `+value || 7` 把 0 静默回退 7 天，已修）。"
  },
  {
    "slug": "agriculture/pesticide-interval",
    "inputs": { "sprayDate": "2026-01-01", "phiDays": "-1" },
    "expect": ["安全间隔期应为农药标签标注的天数"],
    "ref": "负天数无标签依据 ⇒ 显式拒绝，提示改为「应为农药标签标注的天数（不小于 0 的整数）」；默认 phiDays=7 不出现该提示。"
  },
  {
    "slug": "agriculture/assessor-1",
    "inputs": {
      "theoryYield": "42",
      "actualYield": "42",
      "fieldLoss": "42",
      "threshLoss": "42",
      "crop": "rice",
      "method": "manual"
    },
    "expect": [
      ") 脱粒清选损失：42kg(100.00%) 标准限值：≤2% 评估等级： 优秀 损失率在标准允许范围内。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"theoryYield\":\"42\",\"actualYield\":\"42\",\"fieldLoss\":\"42\",\"threshLoss\":\"42\",\"crop\":\"rice\",\"method\":\"manual\"}，输出区含「) 脱粒清选损失：42kg(100.00%) 标准限值：≤2% 评估等级： 优秀…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-12",
    "inputs": {
      "area": "42",
      "depth": "42",
      "eff": "0.42"
    },
    "expect": [
      "2800.0",
      "1176.0",
      "28.00"
    ],
    "ref": "注入非默认(默认 10/20/0.85)：净需水 = 42×666.67×42/1000 = 1176.0 m³；毛取水 = 1176.0÷0.42 = 2800.0 m³；亩净用水 = 1176.0÷42 = 28.00 m³/亩。原用例 eff=42（>1）会让净水量大于毛水量、违反物理，已改 0.42 并在页面拦截 eff>1；默认态为 156.9/133.3/13.33，三条均不命中。"
  },
  {
    "slug": "agriculture/calc-12",
    "inputs": { "area": "0", "depth": "20", "eff": "0.85" },
    "expect": ["不能为 0"],
    "ref": "0 面积由页面输入守卫显式拒绝（「area」是本计算的分母，不能为 0），不再静默输出 0；eff>1 另由 calc() 拦截。默认 10/20/0.85 不出现该提示。"
  },
  {
    "slug": "agriculture/calculator-calc-1",
    "inputs": { "frostStart": "2026-04-20", "frostEnd": "2026-10-15", "growth": "110", "buffer": "12" },
    "expect": ["2026年6月15日", "2026年10月3日"],
    "ref": "倒推口径（修正确证缺陷）：最晚播种日 = 无霜期终日 − 生育期 − 安全余量 = 10/15 − 122 = 2026年6月15日；预计收获 = 6/15 + 110 = 2026年10月3日。旧实现「初日 + 余量」会误报 2026年5月2日/8月30日，把播种窗口整体前移且夸大约 2 个月。"
  },
  {
    "slug": "agriculture/calculator-calc-1",
    "inputs": { "frostStart": "2026-05-01", "frostEnd": "2026-09-01", "growth": "150", "buffer": "10" },
    "expect": ["无可行播期"],
    "ref": "无霜期 123 天 < 生育期 150 + 余量 10 ⇒ 倒推的最晚播种日 2026年3月25日早于初日，必须显式提示无可行播期；默认窗口充足不出现该提示。"
  },
  {
    "slug": "agriculture/greenhouse-ventilation",
    "inputs": { "ghLen": "50", "ghWid": "10", "ghHeight": "4", "windSpeed": "0", "fanEff": "85" },
    "expect": ["进风口风速必须大于 0"],
    "ref": "0 m/s 时所需风口面积在数学上为无穷大，旧实现按 0 m² 显示并判「自然通风充足」；改为显式拒绝。默认风速 2 时不出现该提示。"
  },
  {
    "slug": "agriculture/machinery-efficiency",
    "inputs": { "totalArea": "0" },
    "expect": ["作业总面积必须大于 0"],
    "ref": "总面积 0 时旧实现亩成本恒为 0 并把零成本农机判为「成本最低」；改为显式拒绝。默认 200 亩不出现该提示。"
  },
  {
    "slug": "agriculture/machinery-efficiency",
    "inputs": { "eff0": "0", "eff1": "0", "eff2": "0" },
    "dynInputs": true,
    "expect": ["请至少输入一台有效农机数据"],
    "ref": "时间利用率 0% 的农机实际效率为 0、亩成本恒为 0，旧的宽条件 width/speed>0 会把它选为「成本最低」；改为按 eff 在 1–100 之间过滤，三台全 0 时无有效农机。默认三台 85/80/70 不出现该提示。eff0..2 由 renderMachines() 运行期生成 ⇒ 声明 dynInputs 让桩按生成结果登记默认值，否则首屏 calc 读到空串即命中该提示（假通过）。"
  },
  {
    "slug": "agriculture/calc-flow",
    "inputs": { "v0": "2", "v1": "6", "v2": "8", "v3": "10" },
    "expect": ["12.00", "6.00", "120.00", "30.0", "9.0"],
    "ref": "单位换算核对（40 = 666.67 ÷ 16.667）：总流量 = 2×6 = 12.00 L/min；亩用药液 = 40×12/(8×10) = 6.00 L/亩；作业效率 = 8×10×1.5 = 120.00 亩/h；单亩耗时 = 3600/120 = 30.0 s；mL/m² = 6/666.667×1000 = 9.0。默认 1.2/4/6/6 为 4.80/5.33/54.00/66.7/8.0，五条均不命中。"
  },
  {
    "slug": "agriculture/irrigation-uniformity",
    "clicks": ["applyIrrPreset('partial')"],
    "expect": ["77.4%", "54.8%"],
    "ref": "均匀度口径核对：局部堵塞 [42,41,43,28,12,43,42,41]，均值 36.5，偏差和 66 ⇒ CU = (1−66/292)×100 = 77.4%；最低 1/4 取 ceil(8/4)=2 点 (12+28)/2=20 ⇒ DU = 20/36.5×100 = 54.8%。默认均匀态为 100% 附近，两条均不命中。"
  },
  {
    "slug": "agriculture/agri-calculator",
    "inputs": {
      "fert_n": "42",
      "fert_p": "42",
      "fert_k": "42",
      "fert_area": "42",
      "fert_per_mu": "42",
      "plant_spacing": "42",
      "plant_row": "42",
      "plant_area": "42",
      "pest_content": "42",
      "pest_target": "42",
      "pest_volume": "42",
      "irr_area": "42",
      "irr_depth": "42",
      "hatch_date": "abc123测试",
      "fuel_area": "42",
      "fuel_per_mu": "42",
      "fuel_price": "42",
      "plant_unit": "sqm",
      "pest_unit": "pct"
    },
    "expect": [
      "/亩 肥料总量： 1764.0 kg\n42\n42\n42\nsqm\n238 总株数（株） 3,779 每亩株数 42.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fert_n\":\"42\",\"fert_p\":\"42\",\"fert_k\":\"42\",\"fert_area\":\"42\",\"fert_per_mu\":\"42\",\"plant_spacing\":\"42\",\"plant_row\":\"42\",\"plant_area\":\"42\",\"pest_content\":\"42\",\"pest_target\":\"42\",\"pest_volume\":\"42\",\"irr_area\":\"42\",\"irr_depth\":\"42\",\"hatch_date\":\"abc123测试\",\"fuel_area\":\"42\",\"fuel_per_mu\":\"42\",\"fuel_price\":\"42\",\"plant_unit\":\"sqm\",\"pest_unit\":\"pct\"}，输出区含「/亩 肥料总量： 1764.0 kg\n42\n42\n42\nsqm\n238 总株数（…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-13",
    "inputs": {
      "power": "42",
      "load": "42",
      "sfc": "42",
      "density": "42",
      "hours": "42",
      "price": "42"
    },
    "expect": [
      "小时油耗 L/h 0.74 总油耗 L 0.02 平均 L/h 31.12"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"power\":\"42\",\"load\":\"42\",\"sfc\":\"42\",\"density\":\"42\",\"hours\":\"42\",\"price\":\"42\"}，输出区含「小时油耗 L/h 0.74 总油耗 L 0.02 平均 L/h 31.12」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-15",
    "inputs": {
      "harvestDate": "abc123测试",
      "growthDays": "42",
      "safeDate": "abc123测试"
    },
    "expect": [
      "abc123测试\n42\nabc123测试\n—-—-— 建议播种日期 42 生育期天数 —-—-— 苗期约至 —-—-— 成熟期约至 建议播种日期 —-—-— 在安全播种窗口内，适宜播种。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"harvestDate\":\"abc123测试\",\"growthDays\":\"42\",\"safeDate\":\"abc123测试\"}，输出区含「abc123测试\n42\nabc123测试\n—-—-— 建议播种日期 42 生育期…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-36",
    "inputs": {
      "eto": "4",
      "kc": "1.5",
      "area": "10",
      "eff": "100"
    },
    "expect": [
      "6.00",
      "40.00",
      "280.00",
      "1200.00"
    ],
    "ref": "作物系数定义域核对（Kc 0–3 且 >0）：ETc = 1.5×4 = 6.00 mm/日；日净需水 = 6×10×666.67/1000 = 40.00 m³；周 = 280.00；月 = 1200.00。原用例 kc=42 超出定义域会被显式拒绝；默认 5.0/1.0/10/85 为 5.00/33.33/39.22/233.33/1000.00，四条均不命中。"
  },
  {
    "slug": "agriculture/calc-37",
    "inputs": {
      "par": "42",
      "hours": "42"
    },
    "expect": [
      "42\n42\n请输入有效的正数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"par\":\"42\",\"hours\":\"42\"}，输出区含「42\n42\n请输入有效的正数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-2",
    "inputs": {
      "plantSpace": "42",
      "rowSpace": "42",
      "areaMu": "42",
      "unit": "ha"
    },
    "expect": [
      "42\n42\n42\nha\n3,779 株 / 亩 56,689 株 / 公顷 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plantSpace\":\"42\",\"rowSpace\":\"42\",\"areaMu\":\"42\",\"unit\":\"ha\"}，输出区含「42\n42\n42\nha\n3,779 株 / 亩 56,689 株 / 公顷 17…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-7",
    "inputs": {
      "area": "42",
      "waterPerMu": "42",
      "targetConc": "42",
      "fertContent": "42",
      "ratioX": "42"
    },
    "expect": [
      " 总灌水量 m³ 74.09 纯养分 kg 176.40 肥料商品 kg 4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"waterPerMu\":\"42\",\"targetConc\":\"42\",\"fertContent\":\"42\",\"ratioX\":\"42\"}，输出区含「 总灌水量 m³ 74.09 纯养分 kg 176.40 肥料商品 kg 4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-6",
    "inputs": {
      "shedArea": "42",
      "spacePerHead": "42",
      "cycle": "42",
      "batches": "42"
    },
    "expect": [
      "明： 存栏量 = 42 ÷ 42.00 = 1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"shedArea\":\"42\",\"spacePerHead\":\"42\",\"cycle\":\"42\",\"batches\":\"42\"}，输出区含「明： 存栏量 = 42 ÷ 42.00 = 1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-ventilation-2",
    "inputs": {
      "len": "42",
      "wid": "42",
      "eave": "42",
      "ridge": "42",
      "ach": "42",
      "fan": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n74088"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"len\":\"42\",\"wid\":\"42\",\"eave\":\"42\",\"ridge\":\"42\",\"ach\":\"42\",\"fan\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n74088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calculator-calc-density",
    "inputs": {
      "plantSpace": "42",
      "rowSpace": "42",
      "plantUnit": "cm",
      "rowUnit": "cm"
    },
    "expect": [
      "每平方米株数 3779 每亩株数 56689 每公顷株数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plantSpace\":\"42\",\"rowSpace\":\"42\",\"plantUnit\":\"cm\",\"rowUnit\":\"cm\"}，输出区含「每平方米株数 3779 每亩株数 56689 每公顷株数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calc-8",
    "inputs": {
      "phNow": "6.0",
      "phTarget": "7.0",
      "area": "8",
      "buffer": "1.2"
    },
    "expect": [
      "9.6",
      "1.20"
    ],
    "ref": "pH 定义域核对（0–14）：提升 1.0 个 pH × 缓冲系数 1.2 × 8 亩 = 石灰 9.6 kg；折 0.01 t 显示 1.20（页面把 t 与 kg/亩 同网格渲染，这里锚 9.6 与 1.20）。原用例 pH=42 超域会被显式拒绝；默认 5.5/6.5/10/100 为 1000.0 kg，两条均不命中。"
  },
  {
    "slug": "agriculture/calculator-calc-concentration",
    "inputs": {
      "stock": "42",
      "target": "42",
      "volume": "42",
      "ratio": "42"
    },
    "expect": [
      "42\n1.0000\n42\n42\n1.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"stock\":\"42\",\"target\":\"42\",\"volume\":\"42\",\"ratio\":\"42\"}，输出区含「42\n1.0000\n42\n42\n1.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calculator-calc-1",
    "inputs": {
      "frostStart": "abc123测试",
      "frostEnd": "abc123测试",
      "growth": "42",
      "buffer": "42"
    },
    "expect": [
      "42\n42\nabc123测试\nabc123测试\nInvalid Date 最晚播种日期 Invalid Date 预计收获日期 — 无霜期总天数 84"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"frostStart\":\"abc123测试\",\"frostEnd\":\"abc123测试\",\"growth\":\"42\",\"buffer\":\"42\"}，输出区含「42\n42\nabc123测试\nabc123测试\nInvalid Date 最晚播…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calculator-calc-ratio-1",
    "inputs": {
      "nutrient": "abc123测试",
      "total": "42",
      "nameA": "abc123测试",
      "valA": "42",
      "nameB": "abc123测试",
      "valB": "42",
      "target": "42"
    },
    "expect": [
      "42\n42\n42\n42\nabc123测试\nabc123测试\nabc123测试\n—% abc123测试 占比 —% abc123测试 占比 — abc123测试 重量 (kg) — abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"nutrient\":\"abc123测试\",\"total\":\"42\",\"nameA\":\"abc123测试\",\"valA\":\"42\",\"nameB\":\"abc123测试\",\"valB\":\"42\",\"target\":\"42\"}，输出区含「42\n42\n42\n42\nabc123测试\nabc123测试\nabc123测试\n—…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calculator-calc-ratio",
    "inputs": {
      "nNeed": "42",
      "pNeed": "42",
      "kNeed": "42",
      "area": "42",
      "nPct": "42",
      "pPct": "42",
      "kPct": "42",
      "price": "42",
      "nEff": "42",
      "pEff": "42",
      "kEff": "42",
      "nFert": "34",
      "pFert": "46",
      "kFert": "50"
    },
    "expect": [
      "34\n46\n50\n42\n42\n42\n42\n34\n46\n50\n42\n42\n42\n42\n12352.9"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"nNeed\":\"42\",\"pNeed\":\"42\",\"kNeed\":\"42\",\"area\":\"42\",\"nPct\":\"42\",\"pPct\":\"42\",\"kPct\":\"42\",\"price\":\"42\",\"nEff\":\"42\",\"pEff\":\"42\",\"kEff\":\"42\",\"nFert\":\"34\",\"pFert\":\"46\",\"kFert\":\"50\"}（pFert 46 为重过磷酸钙首项，data-n=0），输出区含「34\n46\n50\n…\n12352.9」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/calculator-calc-soil",
    "inputs": {
      "phCurrent": "42",
      "phTarget": "42",
      "area": "42",
      "depth": "42",
      "soilType": "loam"
    },
    "expect": [
      "42\n42\n42\n42\nloam\n请填写有效的 pH 值与面积参数。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phCurrent\":\"42\",\"phTarget\":\"42\",\"area\":\"42\",\"depth\":\"42\",\"soilType\":\"loam\"}，输出区含「42\n42\n42\n42\nloam\n请填写有效的 pH 值与面积参数。\n暂无计算记…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/continuous-cropping-index",
    "inputs": {
      "years": "42",
      "om": "42",
      "ph": "3.5",
      "cropType": "tomato",
      "pathogen": "2",
      "resistance": "0",
      "disinfection": "5"
    },
    "expect": [
      "建议轮作换茬 • 土壤pH偏离适宜范围，建议调酸或调碱 • 建议使用抗性品种或嫁接苗降低连作障碍"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"years\":\"42\",\"om\":\"42\",\"ph\":\"42\",\"cropType\":\"tomato\",\"pathogen\":\"2\",\"resistance\":\"0\",\"disinfection\":\"5\"}，输出区含「建议轮作换茬 • 土壤pH偏离适宜范围，建议调酸或调碱 • 建议使用抗性品种或嫁…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/canopy-coverage",
    "inputs": {
      "rowSpacing": "42",
      "plantSpacing": "42",
      "canopyDiam": "42",
      "overlap": "42",
      "totalGrid": "42",
      "greenGrid": "42",
      "photoArea": "42",
      "canopyShape": "square"
    },
    "expect": [
      "植密度(株/亩) 2.03 估算LAI 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rowSpacing\":\"42\",\"plantSpacing\":\"42\",\"canopyDiam\":\"42\",\"overlap\":\"42\",\"totalGrid\":\"42\",\"greenGrid\":\"42\",\"photoArea\":\"42\",\"canopyShape\":\"square\"}，输出区含「植密度(株/亩) 2.03 估算LAI 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
  "slug": "agriculture/convert-content-1",
  "inputs": {
    "val": "88.5",
    "unit": "dry",
    "wb": "12"
  },
  "expect": [
    "13.559%"
  ],
  "ref": "复算：干物质 88.5% → 水分 11.5%，湿基 12% 折算干基 = 12 ÷ (1−0.115) = 13.559%；默认干物质 86% 得 13.953% ⇒ 不命中"
},
  // ── 干物质换算：初重参与折算（干重/水分按鲜重计算，旧实现恒用 100 kg）──
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "80", unit: "dry", wb: "15", initW: "500" },
    dumpIds: ["res"],
    expect: ["18.750%", "500.00 kg 湿样 → 绝干 400.00 kg，含水 100.00 kg"],
    ref: "独立复算：干物质 80% ⇒ 水分 20%；干重 = 500×0.80 = 400.00 kg、水分 = 500×0.20 = 100.00 kg；湿基 15% 折算干基 = 15 ÷ (1−0.2) = 18.750%；干湿比 = 1/0.8 = 1.2500。旧实现固定按 100 kg 输出「100.00 kg 湿样 → 绝干 80.00 kg」，本锚不命中；默认（86%/12%/100kg）为 13.953%、100 kg 湿样，亦不命中。"
  },
  // ── 干物质换算：初重为 0 必须拦截（旧实现按 100kg 静默兜底）──
  {
    slug: "agriculture/convert-content-1",
    inputs: { val: "86", unit: "dry", wb: "12", initW: "0" },
    dumpIds: ["res"],
    expect: ["初重需为大于 0 的数值"],
    ref: "独立复算：initW=0 不满足「初重 > 0」⇒ 页面必须输出「初重需为大于 0 的数值」；旧实现 raw=\"\" 才回退 100、对 0 会算出 0 kg 干重并显示 0.00，默认输入 100 kg 合法 ⇒ 只有初重校验分支才命中。"
  },
  {
    "slug": "agriculture/crop-water-requirement",
    "inputs": {
      "kc": "42",
      "et0": "42",
      "rain": "42",
      "days": "42",
      "area": "42",
      "cropSel": "1",
      "irrEff": "70"
    },
    "expect": [
      "溉量(mm/天) 2116.8 42天总蒸散(mm) 14119.1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"kc\":\"42\",\"et0\":\"42\",\"rain\":\"42\",\"days\":\"42\",\"area\":\"42\",\"cropSel\":\"1\",\"irrEff\":\"70\"}，输出区含「溉量(mm/天) 2116.8 42天总蒸散(mm) 14119.1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/crop-rotation",
    "inputs": {
      "areaInput": "42",
      "seasonInput": "夏",
      "modeInput": "simple"
    },
    "expect": [
      "第 2 年 作物：番茄 → 萝卜 🍅 春季·番茄 🥕 秋季·萝卜"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"areaInput\":\"42\",\"seasonInput\":\"夏\",\"modeInput\":\"simple\"}，输出区含「第 2 年 作物：番茄 → 萝卜 🍅 春季·番茄 🥕 秋季·萝卜」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/cycle-honey",
    "inputs": {
      "hiveName": "abc123测试",
      "hiveLoc": "abc123测试",
      "hiveCycle": "42",
      "hiveStart": "abc123测试",
      "extrDate": "abc123测试",
      "extrAmount": "42"
    },
    "expect": [
      "。\n暂无摇蜜记录\nabc123测试\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"hiveName\":\"abc123测试\",\"hiveLoc\":\"abc123测试\",\"hiveCycle\":\"42\",\"hiveStart\":\"abc123测试\",\"extrDate\":\"abc123测试\",\"extrAmount\":\"42\"}，输出区含「。\n暂无摇蜜记录\nabc123测试\nabc123测试\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/detector-13",
    "inputs": {
      "bees": "42",
      "mites": "42",
      "method": "酒精洗涤法",
      "season": "夏季"
    },
    "expect": [
      "螨） 危害等级： 严重危害 夏季防治阈值 2% / 治疗阈值 3% 处置建议： 夏季寄生率严重超标，蜂群濒临崩溃风险，须紧急双甲脒/草酸连治，并结合换王、断子等措施挽救"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bees\":\"42\",\"mites\":\"42\",\"method\":\"酒精洗涤法\",\"season\":\"夏季\"}，输出区含「螨） 危害等级： 严重危害 夏季防治阈值 2% / 治疗阈值 3% 处置建议： …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/detector-nutrition",
    "inputs": {
      "protein": "42",
      "fat": "42",
      "sugar": "42",
      "water": "42",
      "ash": "42",
      "lactic": "42"
    },
    "expect": [
      "测 判读 蛋白质 42% 优质 脂肪 42% 偏高 还原糖 42% 优质 水分 42% 偏高 灰分 42% 偏高 乳酸(发酵度) 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"protein\":\"42\",\"fat\":\"42\",\"sugar\":\"42\",\"water\":\"42\",\"ash\":\"42\",\"lactic\":\"42\"}，输出区含「测 判读 蛋白质 42% 优质 脂肪 42% 偏高 还原糖 42% 优质 水分 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/dry-matter-conversion",
    "inputs": {
      "freshWeight": "42",
      "moisture1": "42",
      "dryWeight": "42",
      "moisture2": "42",
      "actualWeight": "42",
      "actualMoisture": "42",
      "standardMoisture": "42"
    },
    "expect": [
      " 含水率/100)\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"freshWeight\":\"42\",\"moisture1\":\"42\",\"dryWeight\":\"42\",\"moisture2\":\"42\",\"actualWeight\":\"42\",\"actualMoisture\":\"42\",\"standardMoisture\":\"42\"}，输出区含「 含水率/100)\n42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/dli-calculator",
    "inputs": {
      "ppfd": "800",
      "hours": "12",
      "lightPPFD": "200",
      "lightHours": "4",
      "cropType": "medium"
    },
    "expect": [
      "34.6 自然光DLI(mol/m²/d)",
      "37.4 总DLI(mol/m²/d)"
    ],
    "ref": "光照时长定义域核对（0–24 h）：自然光 DLI = 800×12×3600÷1e6 = 34.56 ⇒ 34.6；补光 = 200×4×3600÷1e6 = 2.88 ⇒ 2.9；总 = 37.44 ⇒ 37.4。原用例 hours=42 超出 24 h 会被显式拒绝；默认 400×12（17.3）与 0 补光不命中。"
  },
  {
    "slug": "agriculture/calc-36",
    "inputs": { "eto": "4", "kc": "0", "area": "10", "eff": "85" },
    "expect": ["作物系数 Kc 应在 0–3 之间且大于 0"],
    "ref": "Kc=0 时 ETc 恒为 0，会让灌水需求整体消失；旧条件 kc>=0 放行，改为 kc>0 且 ≤3 显式拒绝。默认 kc=1.0 不出现该提示。"
  },
  {
    "slug": "agriculture/calc-8",
    "inputs": { "phNow": "15", "phTarget": "7", "area": "8", "buffer": "1.2" },
    "expect": ["应在 0–14 之间"],
    "ref": "pH 定义域 0–14：旧实现只校验 buf/area<0，pH=15 会照算；改为超域显式拒绝。默认 5.5/6.5 不出现该提示。"
  },
  {
    "slug": "agriculture/continuous-cropping-index",
    "inputs": { "years": "3", "om": "2", "ph": "0", "cropType": "tomato", "pathogen": "3", "resistance": "1", "disinfection": "1" },
    "expect": ["pH 3–10"],
    "ref": "pH 0 旧实现被 `||7` 静默回退到 7（判为适宜），用户输入 0 却按中性土壤评分；改为按输入框 3–10 域显式拒绝。默认 6.5 不出现该提示。"
  },
  {
    "slug": "agriculture/dli-calculator",
    "inputs": { "ppfd": "800", "hours": "25", "lightPPFD": "0", "lightHours": "0", "cropType": "medium" },
    "expect": ["0–24 小时"],
    "ref": "光照时长 25 h/日 超出物理定义域（旧实现只拦负值会照算 72.0 mol/m²/d）；改为自然光与补光时长均须 0–24 h。默认 10/0 小时不出现该提示。"
  },
  {
    "slug": "agriculture/estimate-yield-rate",
    "inputs": { "fert": "225", "uptake": "400", "soil": "90" },
    "expect": ["表观利用率须为 0–100%"],
    "ref": "作物吸收 400 > 土壤供肥 90 + 施肥 225 = 315 ⇒ 表观利用率 137.8% 无物理意义；改为要求吸收量介于 [土壤供肥, 土壤供肥+施肥] 显式拒绝。默认 180/90/225（40%）不出现该提示。"
  },
  {
    "slug": "agriculture/estimate-soil",
    "inputs": { "years": "5", "init": "100", "rate": "10", "threshold": "0" },
    "expect": ["阈值密度必须大于 0"],
    "ref": "阈值 0 时旧实现把障碍指数直接置 0（视作安全），掩盖了任何病原菌累积；改为 threshold>0 显式拒绝。默认阈值 100 不出现该提示。"
  },
  {
    "slug": "agriculture/harvest-date-predictor",
    "inputs": { "sowDate": "2026-05-01", "moisture": "120", "dryRate": "0.5", "gdd": "1500" },
    "expect": ["含水量应在 0–100% 之间"],
    "ref": "含水量 120% 超出定义域（旧实现照算降水天数）；改为 0–100% 显式拒绝。默认 28% 不出现该提示。"
  },
  {
    "slug": "agriculture/harvest-date-predictor",
    "inputs": { "sowDate": "2099-01-01", "moisture": "28", "dryRate": "0.5", "gdd": "1500" },
    "expect": ["播种日期不能晚于今天"],
    "ref": "未来播期的「已生长天数」为负、GDD 进度无意义；改为显式拒绝。默认播期为过去日期，不出现该提示。"
  },
  {
    "slug": "agriculture/assessor-1",
    "inputs": { "theoryYield": "450", "actualYield": "500", "fieldLoss": "15", "threshLoss": "10" },
    "expect": ["实际收获产量不能为负或高于理论产量"],
    "ref": "实际 500 > 理论 450 时旧实现总损失为 −50、损失率 −11.1% 并判「优秀」；改为显式拒绝。默认 415 < 450 不出现该提示。"
  },
  {
    "slug": "agriculture/detector-nutrition",
    "inputs": { "protein": "120", "fat": "5", "sugar": "18", "water": "7", "ash": "2.5", "lactic": "1.8" },
    "expect": ["各营养成分含量应在 0–100% 之间"],
    "ref": "蛋白质 120% 超出质量分数定义域（旧实现只查 NaN 会照算并给出等级）；改为 0–100% 显式拒绝。默认 22% 不出现该提示。"
  },
  {
    "slug": "agriculture/calc-38",
    "inputs": { "values": "0,0,0,0,0,0,0,0" },
    "expect": ["收集水量均值必须大于 0"],
    "ref": "8 个测点全 0 时均值 0，旧实现 CU 与 CV 均变成 Infinity/NaN 仍渲染；改为均值必须 >0 显式拒绝。默认 120/135/… 不出现该提示。"
  },
  {
    "slug": "agriculture/estimate-3",
    "inputs": {
      "kc": "42",
      "et0": "42",
      "days": "42",
      "area": "42",
      "rain": "42",
      "crop": "0.85"
    },
    "expect": [
      "0.85\n42\n42\n42\n42\n35.7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"kc\":\"42\",\"et0\":\"42\",\"days\":\"42\",\"area\":\"42\",\"rain\":\"42\",\"crop\":\"0.85\"}，输出区含「0.85\n42\n42\n42\n42\n35.7」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/estimate-content-soil",
    "inputs": {
      "w1": "42",
      "w2": "42",
      "crucible": "42",
      "temp": "42"
    },
    "expect": [
      "42\n42\n42\n烧前干土净重需大于0，请检查坩埚空重是否填写正确\n暂无计算记录\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w1\":\"42\",\"w2\":\"42\",\"crucible\":\"42\",\"temp\":\"42\"}，输出区含「42\n42\n42\n烧前干土净重需大于0，请检查坩埚空重是否填写正确\n暂无计算记录…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/estimate-area-density",
    "inputs": {
      "area": "42",
      "density": "42",
      "weight": "42",
      "survival": "42",
      "unit": "mu"
    },
    "expect": [
      "42\n42\n42\n42\nmu\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"density\":\"42\",\"weight\":\"42\",\"survival\":\"42\",\"unit\":\"mu\"}，输出区含「42\n42\n42\n42\nmu\n1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/estimate-fuel-engine-oil",
    "inputs": {
      "area": "42",
      "fuel": "42",
      "hours": "42",
      "price": "42"
    },
    "expect": [
      "42\n42\n42\n42\n1.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"fuel\":\"42\",\"hours\":\"42\",\"price\":\"42\"}，输出区含「42\n42\n42\n42\n1.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/estimate-area-yield",
    "inputs": {
      "yieldInput": "42",
      "area": "42",
      "dmRate": "42",
      "baleWeight": "42",
      "unit": "t_ha"
    },
    "expect": [
      "176.40 鲜草总产量（kg）",
      "74.09 干草产量（kg）",
      "2 估算干草捆数"
    ],
    "ref": "注入 t_ha 单位并复算：42 t/ha × 0.1 kg/㎡（1 t/ha = 1000kg/10000㎡）× 42㎡ = 176.40 kg 鲜草；干物质 42% ⇒ 74.09 kg；42 kg/捆 ⇒ 2 捆。旧实现按 0.0001 系数把吨当 kg，鲜草只有 0.1764 kg，三条锚均不命中。默认态（3000 kg/亩 × 10000㎡ = 45000 kg）不命中。"
  },
  {
    "slug": "agriculture/estimate-yield-rate",
    "inputs": {
      "fert": "42",
      "uptake": "42",
      "soil": "42",
      "element": "P2O5"
    },
    "expect": [
      "42\n42\n42\nP2O5\n0.00% 磷(P₂O₅) 表观利用率 过低 利用率评价 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fert\":\"42\",\"uptake\":\"42\",\"soil\":\"42\",\"element\":\"P2O5\"}，输出区含「42\n42\n42\nP2O5\n0.00% 磷(P₂O₅) 表观利用率 过低 利用率…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/fertigation-ratio",
    "inputs": {
      "targetEC": "42",
      "waterEC": "42",
      "dripFlow": "42",
      "dripperCount": "42",
      "duration": "42",
      "solubility": "42",
      "fertType": "2",
      "stockRatio": "200"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n2\n200\n水源EC已达到或超过目标EC，无需注肥"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"targetEC\":\"42\",\"waterEC\":\"42\",\"dripFlow\":\"42\",\"dripperCount\":\"42\",\"duration\":\"42\",\"solubility\":\"42\",\"fertType\":\"2\",\"stockRatio\":\"200\"}，输出区含「42\n42\n42\n42\n42\n42\n2\n200\n水源EC已达到或超过目标EC，无…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/estimate-soil",
    "inputs": {
      "years": "42",
      "init": "42",
      "rate": "42",
      "threshold": "42"
    },
    "expect": [
      "42\n42\n42\n42\n248949044.7 连作障碍指数 104.56×10⁶"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"years\":\"42\",\"init\":\"42\",\"rate\":\"42\",\"threshold\":\"42\"}，输出区含「42\n42\n42\n42\n248949044.7 连作障碍指数 104.56×10…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/fertilizer-efficiency",
    "inputs": {
      "fertUptake": "42",
      "fertInput": "42",
      "ckUptake": "42",
      "nutrientType": "P2O5"
    },
    "expect": [
      "g/亩) 评价： 偏低需优化 磷肥参考范围：12%~25% 利用率偏低，建议：①分次施用减少流失；②深施覆土；③配合有机肥；④调整施肥时期"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fertUptake\":\"42\",\"fertInput\":\"42\",\"ckUptake\":\"42\",\"nutrientType\":\"P2O5\"}，输出区含「g/亩) 评价： 偏低需优化 磷肥参考范围：12%~25% 利用率偏低，建议：①…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/fertilizer-calculator",
    "inputs": {
      "area": "42",
      "yield": "42",
      "needN": "42",
      "needP": "42",
      "needK": "42",
      "period": "top"
    },
    "expect": [
      "PK比例 : N:42.0 P₂O₅:42.0 K₂O:42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"yield\":\"42\",\"needN\":\"42\",\"needP\":\"42\",\"needK\":\"42\",\"period\":\"top\"}，输出区含「PK比例 : N:42.0 P₂O₅:42.0 K₂O:42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/greenhouse-ventilation",
    "inputs": {
      "ghLen": "42",
      "ghWid": "42",
      "ghHeight": "42",
      "windSpeed": "42",
      "fanEff": "42",
      "airChanges": "25"
    },
    "expect": [
      "42\n42\n42\n25\n42\n42\n74088"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ghLen\":\"42\",\"ghWid\":\"42\",\"ghHeight\":\"42\",\"windSpeed\":\"42\",\"fanEff\":\"42\",\"airChanges\":\"25\"}，输出区含「42\n42\n42\n25\n42\n42\n74088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/greenhouse-rolling-time",
    "inputs": {
      "inTemp": "32",
      "outTemp": "20",
      "targetTemp": "28",
      "humidity": "60",
      "cropMaxTemp": "34",
      "timePeriod": "noon",
      "windLevel": "2"
    },
    "expect": [
      "12℃ 内外温差 60% 棚内湿度"
    ],
    "ref": "注入非默认(inTemp 32 / outTemp 20 / humidity 60；默认 28/18/75)：温差 = 32−20 = 12℃，棚内湿度 60%；目标 28℃、棚温 32℃ 未超作物上限 34℃ ⇒ 维持「保持现状」。旧 42 组全部为输入回显且提示文案在默认态同样出现，回退默认即命中；改用派生温差/湿度锚，默认态为 10℃/75%，锚不命中。"
  },
  {
    "slug": "agriculture/gdd-calculator",
    "inputs": {
      "tbase": "42",
      "tupper": "42",
      "targetGDD": "42",
      "method": "single"
    },
    "expect": [
      "6天 第7天\nsingle\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tbase\":\"42\",\"tupper\":\"42\",\"targetGDD\":\"42\",\"method\":\"single\"}，输出区含「6天 第7天\nsingle\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/harvest-date-predictor",
    "inputs": {
      "sowDate": "abc123测试",
      "moisture": "42",
      "dryRate": "42",
      "gdd": "42",
      "cropSel": "corn"
    },
    "expect": [
      "生长度日进度： 1.6%",
      "当前：42℃·d"
    ],
    "ref": "自动补强（B类零用例）：注入{\"gdd\":\"42\",\"cropSel\":\"corn\"}等，输出「生长度日进度： 1.6%」（42/2700=1.5556→1.6）与「当前：42℃·d」。⚠ 原 expect 锚在「…| 120天 玉米收割要点…」上，而「已生长天数」由页面 new Date() 与今日相减得出 ⇒ 随时区/日期变化（Asia/Shanghai=120、UTC=121），CI 在 UTC 必红。已改为由注入量 gdd 决定、与时钟无关的锚点（默认 gdd=1800⇒66.7%，不含 1.6%/42℃·d ⇒ 强判别、零逃生）。"
  },
  {
    "slug": "agriculture/irrigation-calculator",
    "inputs": {
      "area": "42",
      "depth": "42",
      "moisture": "42",
      "price": "42",
      "cycle": "42",
      "method": "sprinkler",
      "soil": "loam"
    },
    "expect": [
      ".8 浆果膨大期\n42\nsprinkler\nloam\n42\n42\n42\n42\n🏦 喷灌 灌溉方案 75.8"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"depth\":\"42\",\"moisture\":\"42\",\"price\":\"42\",\"cycle\":\"42\",\"method\":\"sprinkler\",\"soil\":\"loam\"}，输出区含「.8 浆果膨大期\n42\nsprinkler\nloam\n42\n42\n42\n42\n\ud83c…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/harvest-loss-rate",
    "inputs": {
      "theoryYield": "42",
      "actualYield": "42",
      "headerLoss": "42",
      "threshLoss": "42",
      "scatterLoss": "42",
      "transportLoss": "42"
    },
    "expect": [
      "分析 割台/掉穗 42kg 100.00% 脱粒/清选 42kg 100.00% 夹带/抛撒 42kg 100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"theoryYield\":\"42\",\"actualYield\":\"42\",\"headerLoss\":\"42\",\"threshLoss\":\"42\",\"scatterLoss\":\"42\",\"transportLoss\":\"42\"}，输出区含「分析 割台/掉穗 42kg 100.00% 脱粒/清选 42kg 100.00%…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/harvest-planner",
    "inputs": {
      "area": "42",
      "yield": "42",
      "days": "42",
      "hours": "42",
      "laborCost": "42",
      "machineCost": "42",
      "method": "combine"
    },
    "expect": [
      "果纹清晰\n500\n42\n42\n42\n42\n42\ncombine"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"yield\":\"42\",\"days\":\"42\",\"hours\":\"42\",\"laborCost\":\"42\",\"machineCost\":\"42\",\"method\":\"combine\"}，输出区含「果纹清晰\n500\n42\n42\n42\n42\n42\ncombine」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/irrigation-uniformity",
    "inputs": {
      "pt0": "42", "pt1": "41", "pt2": "43", "pt3": "28",
      "pt4": "12", "pt5": "43", "pt6": "42", "pt7": "41",
      "pt8": "42", "pt9": "43", "pt10": "41", "pt11": "42"
    },
    "expect": [
      "84.1% 克里斯琴森系数CU",
      "70.4% 分布均匀度DU",
      "38.33 平均灌水量"
    ],
    "ref": "重写：原注入裸键 pt（页面只生成 pt0..ptN、统一读 getElementById('pt'+k)，裸 pt 从不被读取 ⇒ 注入落空、断言「均值) × 100\\n42」是把输入回显当结果）。改为页面真实动态键 pt0..pt11（pointCount=12）：均值 =(42+41+43+28+12+43+42+41+42+43+41+42)/12=38.33；Σ|xi−x̄|=73.32 ⇒ CU=(1−73.32/(12×38.33))×100=84.1%；最低 1/4 取 ceil(12/4)=3 点 (12+28+41)/3=27 ⇒ DU=27/38.33×100=70.4%。默认态 12 个测点读数均空(0) ⇒ CU 0.0%/DU 0.0%/均值 0.00，三条均不命中。不锚「均匀性良好（CU 80%–90%）」——该结论串随档位变化但默认态也有同句式，易与档位抖动混同。该页 12 个测点输入为 JS 动态生成，已由 lib_dynamic_defaults.js 解析运行期默认值，本批起纳入判别（不再计入 skipped）。"
  },
  {
    "slug": "agriculture/machinery-efficiency",
    "inputs": {
      "totalArea": "42",
      "laborCost": "42"
    },
    "expect": [
      "油单价(元/L)\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalArea\":\"42\",\"laborCost\":\"42\"}，输出区含「油单价(元/L)\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/mulch-coverage",
    "inputs": {
      "landLen": "200",
      "landWid": "100",
      "filmWid": "120",
      "filmThk": "8",
      "rowSpacing": "100",
      "overlap": "10"
    },
    "expect": [
      "20000 地膜总长(m) 176.6 地膜用量(kg)"
    ],
    "ref": "注入非默认(landLen 200 / landWid 100；默认 100/50)：地块 200×100m ⇒ 30.00 亩；铺设行数 = 100/1.00 = 100 行；总长 = 100×200 = 20000 m；用量 = 20000×1.2m×0.008m×0.92g/cm³ ≈ 176.6 kg。旧 42 组超出页面合法区间（膜宽/行距 ≥1、搭接 ≤ 有效膜宽），输出「搭接量过大」静态提示且输入回显 42，回退默认即命中，故换成合法参数 + 派生数值锚。"
  },
  {
    "slug": "agriculture/seed-germination-rate",
    "inputs": {
      "totalSeeds": "42",
      "seedlingLen": "42",
      "energyDay": "4"
    },
    "expect": [
      "数 第7天发芽数\n42\n4\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalSeeds\":\"42\",\"seedlingLen\":\"42\",\"energyDay\":\"4\"}，输出区含「数 第7天发芽数\n42\n4\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/ratio-10",
    "inputs": {
      "targetEC": "42",
      "waterEC": "42",
      "fertEC": "42",
      "targetPH": "42"
    },
    "expect": [
      "42\n42\n42\n⚠️ 水源 EC 已达到或超过目标 EC，无需额外注肥，建议先处理水源或降低水源 EC\n暂无计算记录\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"targetEC\":\"42\",\"waterEC\":\"42\",\"fertEC\":\"42\",\"targetPH\":\"42\"}，输出区含「42\n42\n42\n⚠️ 水源 EC 已达到或超过目标 EC，无需额外注肥，建议先…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/nongjijuzuoyexiaolv-mu-xiaoshi-duibi",
    "inputs": {
      "width": "42",
      "speed": "42",
      "time": "42",
      "actualArea": "42"
    },
    "expect": [
      "种加肥、转移等），建议优化作业路线与减少空行\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"speed\":\"42\",\"time\":\"42\",\"actualArea\":\"42\"}，输出区含「种加肥、转移等），建议优化作业路线与减少空行\n暂无计算记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/soil-organic-matter",
    "inputs": {
      "beforeWeight": "42",
      "afterWeight": "42",
      "temp": "400",
      "factor": "1.8"
    },
    "expect": [
      "42\n42\n400\n1.8\n灼烧后重量不应大于灼烧前，请检查数据"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"beforeWeight\":\"42\",\"afterWeight\":\"42\",\"temp\":\"400\",\"factor\":\"1.8\"}，输出区含「42\n42\n400\n1.8\n灼烧后重量不应大于灼烧前，请检查数据」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/storage-pest-alert",
    "inputs": {
      "temp": "38",
      "humidity": "35",
      "grainMoisture": "28",
      "storageDays": "120",
      "grainType": "corn"
    },
    "expect": [
      "中等风险 综合风险指数：75/100",
      "粉斑螟 15℃ 28~32℃ 37 低"
    ],
    "ref": "自动补强（B类零用例）改用合法非默认输入（38℃/35%RH/28% 水分/120 天/玉米；旧 42 组因页面新增 0~40% 含水率校验被拦截）：综合风险指数 75/100 ⇒ 中等风险；粉斑螟风险指数 37 ⇒ 低。默认态（25/65/13/30/小麦）为 96/100、高风险且无粉斑螟行，两条均不命中。"
  },
  {
    "slug": "agriculture/straw-return",
    "inputs": {
      "carbon": "42",
      "nitrogen": "42",
      "strawAmount": "42",
      "soilOM": "42",
      "strawType": "corn",
      "targetCN": "25",
      "fertType": "carbonate"
    },
    "expect": [
      "43\n0.7\n600\n25\ncarbonate\n42\n36.0 需补碳铵(kg/亩) 6.12"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"carbon\":\"42\",\"nitrogen\":\"42\",\"strawAmount\":\"42\",\"soilOM\":\"42\",\"strawType\":\"corn\",\"targetCN\":\"25\",\"fertType\":\"carbonate\"}，输出区含「43\n0.7\n600\n25\ncarbonate\n42\n36.0 需补碳铵(kg/…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "agriculture/temp-time-2",
    "inputs": {
      "inTemp": "38",
      "outTemp": "18",
      "wind": "5",
      "area": "500"
    },
    "expect": [
      "5000",
      "38%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inTemp\":\"38\",\"outTemp\":\"18\",\"wind\":\"5\",\"area\":\"500\"}（风速 5 m/s 在 0–20 校验范围内）：温差 20℃ ⇒ 通风量 = 20×500×0.5 = 5000 m³/min；卷膜高度 = round(1×0.375×100) = 38%。原自动注入 wind=42 超出 0–20 m/s，会被输入校验拦截，故同步改为合法非默认值；默认态（35/25/3/500）为 2500/42%，不含 5000/38%。"
  },
  {
    "slug": "agriculture/temp-2",
    "inputs": {
      "temp": "38",
      "humidity": "35",
      "moisture": "28",
      "grain": "wheat"
    },
    "expect": [
      "中风险 虫害风险等级 61 综合风险评分",
      "储粮水分偏高叠加温湿度风险"
    ],
    "ref": "自动补强（B类零用例）改用合法非默认输入（38℃/35%RH/28% 水分/小麦；旧 42 组因页面新增 0~40% 含水率校验被拦截）：综合评分 61 ⇒ 水分超安全值把等级升为中风险；并输出仅高水分叠加温湿度才有的建议「储粮水分偏高叠加温湿度风险」。默认态（28/75/13.5/稻谷）为高风险且无该句，两条均不命中。"
  },
  // ── 种子发芽：发芽数超过供试种子数应拦截（不再给「优质种」）────
  {
    "slug": "agriculture/seed-germination-rate",
    "inputs": { "totalSeeds": "10", "seedlingLen": "12", "energyDay": "4", "day1": "12" },
    "expect": ["发芽数合计超过供试种子数，请核对逐日记录"],
    "ref": "供试 10 粒、第 1 天即记录 12 粒 ⇒ 累计 12 > 10，页面必须拦截并提示；旧实现按 120.0% 判「优质种」。默认态 100 粒/逐日 14… 不触发该提示。"
  },
  // ── 种子发芽：增删记录日保留已录入值（只追加末行）──────────────
  {
    "slug": "agriculture/seed-germination-rate",
    "inputs": { "totalSeeds": "100", "seedlingLen": "12", "energyDay": "4" },
    "clicks": ["['5','7','1','2','3','4','5'].forEach(function(v,i){document.getElementById('day'+(i+1)).value=v;});addDay();calc();"],
    "expect": ["28.0%", "15.0%"],
    "ref": "7 天依次改为 5/7/1/2/3/4/5 后点「+ 添加记录日」：若保留已录入值，累计 = 5+7+1+2+3+4+5 + 新行默认 1 = 28 ⇒ 28.0%，发芽势(前4天)=5+7+1+2=15 ⇒ 15.0%；旧实现整表重建回默认值，累计 76 ⇒ 76.0%/66.0%，两条均不命中。"
  },
  // ── 灌溉均匀度：n=5 时 DU 取样按 25% 向上取整（ceil(5/4)=2）───
  {
    "slug": "agriculture/irrigation-uniformity",
    "inputs": {},
    "clicks": ["pointCount=5;renderPoints();['40','38','36','34','12'].forEach(function(v,i){document.getElementById('pt'+i).value=v;});calc();"],
    "expect": ["75.0%", "71.9%", "31.9%"],
    "ref": "5 点 [40,38,36,34,12]：均值 32；CU = 1 − 40/(5×32) = 75.0%；四分位取样 q1=ceil(5/4)=2 ⇒ (12+34)/2=23 ⇒ DU = 23/32 = 71.9%；CV = sqrt(104)/32 = 31.9%。旧实现 floor(5/4)=1 ⇒ DU=12/32=37.5%，71.9% 不命中；默认 12 点亦不含这三条。"
  },
  // ── 秸秆还田：氮含量 0 时不再显示 999:1 / Infinity，直接拦截 ────
  {
    "slug": "agriculture/straw-return",
    "inputs": { "strawType": "wheat", "carbon": "45", "nitrogen": "0", "strawAmount": "400", "targetCN": "20", "fertType": "urea" },
    "expect": ["请输入有效的秸秆参数（秸秆量、碳含量、氮含量与目标C/N均须大于0）"],
    "ref": "氮含量 0 ⇒ C/N 无定义，页面必须拦截；旧实现显示 999.0:1、复制出 Infinity:1，并照常给补氮量。默认氮 0.5 走正常计算，不出现该提示。"
  },
  // ── 化肥利用率：差减法 >100% 应判「数据异常」而非「高效利用」───
  {
    "slug": "agriculture/fertilizer-efficiency",
    "inputs": { "fertUptake": "20", "fertInput": "10", "ckUptake": "5", "nutrientType": "N" },
    "expect": ["150.0%", "数据异常", "利用率超过100%，数据异常"],
    "ref": "利用率 = (20−5)÷10×100 = 150.0%，超过物理上限 ⇒ 判「数据异常」并提示复核；默认 12.5/15/7 ⇒ 36.7%，不命中。旧实现给「高效利用」。"
  },
  // ── 土壤有机质：换算系数 0 时应拦截（避免有机质结果恒为 0/无效）──
  {
    "slug": "agriculture/soil-organic-matter",
    "inputs": { "beforeWeight": "10", "afterWeight": "9.6", "temp": "550", "factor": "0" },
    "expect": ["换算系数必须大于0"],
    "ref": "换算系数 0 ⇒ 有机质 = 有机碳 × 0 恒为 0，页面必须拦截；默认 1.724 正常计算，不出现该提示。"
  },
  // ── 作物需水：降雨「时段合计」口径先折算日均，跨日雨量不被逐日全扣 ──
  {
    "slug": "agriculture/crop-water-requirement",
    "inputs": { "kc": "1.0", "et0": "6", "rain": "40", "rainMode": "total", "days": "10", "area": "15", "irrEff": "70" },
    "expect": ["2.00", "285.9", "33.3%"],
    "ref": "ETc = 6.00；10 天合计雨 40 mm ⇒ 日均 4.00 mm，日净 = 2.00 mm；总净 20 mm，毛水 28.57 mm，15 亩 ⇒ 285.9 m³；净/蒸散 = 33.3%。若按日均口径误把 40 当 mm/天，日净为 0、总灌水 0，三条均不命中；默认态（雨 1 mm/天）亦不命中。"
  },
  // ── 作物测产：穗数/粒数/千粒重留空或为 0 时应拦截，不再判「低产」──
  {
    "slug": "agriculture/crop-yield",
    "inputs": { "method": "spike", "area": "10", "moisture": "13", "spikes": "0", "grains": "35", "weight": "45" },
    "expect": ["请填写测产所需的面积与产量参数（均须大于0）"],
    "ref": "穗数 0 ⇒ 单产 0，页面必须拦截；旧实现按 0 kg/亩 输出并判「低产」。默认 40 万穗/35 粒/45 g 不触发该提示。"
  },
  // ── 积温：目标积温 0 时进度分母为 0，应拦截 ─────────────────────
  {
    "slug": "agriculture/gdd-calculator",
    "inputs": { "method": "single", "tbase": "10", "tupper": "30", "targetGDD": "0" },
    "expect": ["目标积温必须大于0"],
    "ref": "目标积温 0 ⇒ 进度 = 总积温/0；旧实现输出 Infinity 占位「—」。默认 1500 不触发。"
  },
  // ── 饲料配比：原料名/营养成分未经转义直接拼 innerHTML ⇒ DOM XSS ───────────
  {
    "slug": "agriculture/calculator-calc-ratio-1",
    "inputs": {
      "nutrient": "<img src=x onerror=alert(1)>",
      "total": "100",
      "nameA": "<img src=x onerror=alert(1)>",
      "valA": "43",
      "nameB": "<img src=x onerror=alert(1)>",
      "valB": "8",
      "target": "18"
    },
    "expect": ["&lt;img src=x onerror=alert(1)&gt;"],
    "ref": "注入 <img src=x onerror=alert(1)> 到营养成分/原料 A/原料 B 名称框：旧实现原样拼进 res.innerHTML ⇒ 生成真实 img 元素；修复后经 ToolBox.escHtml 转义，输出只含实体 &lt;img…&gt;（harness 剥标签不会吞掉实体串）。默认原料名「豆粕/玉米」不含实体，注入态才命中；输入框 value 原文不含 &lt; 前缀，故不能靠回显通过。"
  },
  // ── 农药 ppm / 亩用量口径（2026-11-04）：稀释倍数须按制剂实物量算，不能乘以有效成分% ──
  {
    slug: "agriculture/pesticide-dose",
    inputs: { water: "15", area: "1", activePct: "25", pesticidePerMu: "3" },
    clicks: ["currentMethod=METHODS.find(function(m){return m.id==='dosage';});calc();"],
    dumpIds: ["result"],
    expect: ["5000 稀释倍数", "3.00 每亩用药量(ml/g)"],
    ref: "亩用量反推分支：稀释倍数 = 15 L × 1000 ÷ 3 g = 5000 倍；目标 ppm = 25% × 10000 ÷ 5000 = 50 ppm。旧实现把分母再乘 effectivePct/100（3 × 0.25），得 20000 倍（差 4 倍），两条锚均不命中；默认 ppm 模式（10%、20 ppm）虽同为 5000 倍，但亩用药量为 0.00，第二条不命中。"
  },
  // ── 零用例补强：孵化 / 种植倒计时（基准日冻结 2024-06-15） ──
  {
    slug: "agriculture/countdown-4",
    inputs: { batchName: "批次A" },
    clicks: ["state.startDate='2024-06-01';render()"],
    expect: ["第 15 天", "距离出壳约 7 天"],
    ref: "基准日冻结 2024-06-15：入孵 2024-06-01 ⇒ dayNum = floor(14 天) + 1 = 15、hatchingDay = 06-22 ⇒ left = 7 ⇒ 卡片显示「第 15 天」「距离出壳约 7 天」。默认 state.startDate 为空 ⇒ render 直接隐藏 heroBox，两条锚均不命中（判别时清空 clicks 即回到该默认态）。"
  },
  {
    slug: "agriculture/countdown-cycle",
    inputs: { cropSel: "0", plantDate: "2024-06-01" },
    clicks: ["addPlanting()"],
    expect: ["86 天后收获", "已生长 14/100 天 (14%)", "当前：幼苗期"],
    ref: "番茄 = CROPS[0]（cycle 100 天）：种植 2024-06-01、基准日 2024-06-15 ⇒ elapsed = 14、left = 100 − 14 = 86 ⇒「86 天后收获」；frac = 14/100 = 0.14 落在 0.07 < f ≤ 0.25 ⇒「幼苗期」，进度串「已生长 14/100 天 (14%)」。默认无种植记录 ⇒ 列表显示空态「还没有种植记录」，三条锚均不命中（判别时清空 clicks/inputs 即回该默认态）。"
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

  console.log("==== agriculture calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();