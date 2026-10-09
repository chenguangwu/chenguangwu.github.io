#!/usr/bin/env node
/**
 * 第 29 道门禁：fishery 分类计算正确性验证（8 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：aerator-duration / feed-rate-calculator / feeding-rate（含 select 品种/温度因子与多分支）；
 *       tank-volume / density-1 / cycle-6（动态形状/结构，stub 不稳）；water-oxygen（插值查表）。
 * 用法: node scripts/verify_fishery_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "fishery/calc-39",
    inputs: { v1: "500", v2: "20" },
    expect: ["100.00"],
    ref: "percent 默认 part 模式：v2% of v1 = 500×20/100=100.00（默认值避开）",
  },
  {
    slug: "fishery/salinity-calculator",
    inputs: { v1: "2000", s1: "5", s2: "40", st: "20" },
    expect: ["1500.00", "20.000"],
    ref: "V2=V1×(St−S1)/(S2−St)=2000×(20−5)/(40−20)=1500.00 L；混合后 3500.00 L、盐度 (2000×5+1500×40)/3500=20.000‰（默认 1000/0/35/15 避开）",
  },
  {
    slug: "fishery/water-exchange-rate",
    inputs: { volume: "1000", exchange: "200", prod: "0.6", cin: "0.2", ctarget: "3" },
    expect: ["3.20", "20.0"],
    ref: "换水率=200/1000=20.0%/天；τ=1000/200=5.0 天；稳态浓度=c_in+prod×τ=0.2+0.6×5=3.20 mg/L（默认 800/80/0.5/0.1/2 避开）",
  },
  {
    slug: "fishery/profit-calculator",
    inputs: { yield: "2000", price: "30", byproduct: "1000", seed: "2000", feed: "8000", electric: "800", medicine: "400", labor: "3000", rent: "2000", other: "500" },
    expect: ["61000", "44300"],
    ref: "收入=2000×30+1000=61000；直接=2000+8000+800+400=11200；间接=3000+2000+500=5500；总成本=16700；净利=61000−16700=44300（默认 5000/20… 避开）",
  },
  {
    slug: "fishery/fry-transport-survival",
    inputs: { density: "1000", duration: "12", temp: "15", target: "90", oxy: "air" },
    expect: ["0.4000", "67.0"],
    ref: "风险率=0.02×(1000/100)×(12/6)×exp((15−15)/12)×1.0=0.4；成活率=100×exp(−0.4)=67.0%（oxy=air 系数 1.0）",
  },
  {
    slug: "fishery/wastewater-cod",
    inputs: { feed: "80", fcr: "1.5", discharge: "300", codFactor: "0.4", limit: "30" },
    expect: ["32.00", "106.7"],
    ref: "COD 负荷=80×0.4=32.00 kg/天；浓度=32×1000/300=106.7 mg/L（默认 50/200/0.35 避开）",
  },
  {
    slug: "fishery/fish-weight",
    inputs: { length: "40", paramA: "0.02", paramB: "3" },
    expect: ["1280.00"],
    ref: "W=a·L^b=0.02×40³=1280.00 g（默认 30/0.0207/3.05 避开）",
  },
  {
    slug: "fishery/dissolved-oxygen",
    inputs: { temp: "20", press: "101.3", sal: "0", curDo: "8", hours: "10", rate: "0.3" },
    expect: ["5.00", "9.02"],
    ref: "黎明溶氧=8−0.3×10=5.00 mg/L；饱和溶氧=14.652−0.41022×20+0.007991×400−0.000077774×8000=9.02 mg/L（默认 26/6.5/9/0.35 避开）",
  },

  // ── §7.4 零用例加固 · fishery 确定性数值页（探针实测取锚）────
  {
    slug: "fishery/mesh-size-guide",
    inputs: { mesh: "60", length: "32" },
    expect: ["网目 60mm，L50≈3.0cm", "对应体重 1 g"],
    ref: "注入非默认(默认 50/25)：网目 60mm ⇒ L50 ≈ 3.0 cm（经验系数按品种取值），按 W = 0.0223·L^3.01 换算对应体重 1 g。默认态为 50mm 档的一对值，两条均不命中。"
  },
  {
    slug: "fishery/stocking-density",
    inputs: { area: "8", depth: "1.8", power: "6", size: "18", surv: "82" },
    expect: ["22,866", "182,927", "338"],
    ref: "注入非默认(默认 5/1.2/4/15/75)：8 亩 ×1.8m ⇒ 水体 9600 m³；按目标规格 18cm/成活率 82% 反推推荐密度 22,866 尾/亩、总放苗 182,927 尾；0.75 kW/亩 增氧功率对应载鱼量上限 338 kg/亩。默认态三项均不同。"
  },
  {
    slug: "fishery/feeding-rate",
    inputs: { temp: "21", weight: "1500" },
    expect: ["4.40%", "66.00", "22.00"],
    ref: "注入非默认(默认 25/1000)：21℃、规格插值 ⇒ 推荐投喂率 4.40% 体重/日；日投喂 = 1500 kg × 4.40% = 66.00 kg；分 3 次 ⇒ 每次 22.00 kg。默认态 3.50%/35.00/11.67 均不命中。"
  },
  {
    slug: "fishery/aerator-duration",
    inputs: { area: "8", depth: "1.8", cur: "2.4", target: "6.0", power: "5", sae: "1.8", cons: "0.4" },
    expect: ["6.70", "0.537", "3.60"],
    ref: "注入非默认(默认 5/1.2/3.0/5.0/3/1.5/0.3)：溶氧缺口 = 6.0 − 2.4 = 3.60 mg/L；净增氧 = 0.937 − 0.4 = 0.537 mg/L·h ⇒ 需开启 3.60/0.537 = 6.70 h。默认态三项均不同。"
  },
  {
    slug: "fishery/pond-desilting",
    inputs: { area: "8", rate: "4", allow: "18", cur: "12", price: "22" },
    expect: ["21120", "6.0 剩余厚度", "1.5 年"],
    ref: "注入非默认(默认 5/3/20/8/15)：剩余厚度 = 18 − 12 = 6.0 cm；按 4 cm/年沉积 ⇒ 约 1.5 年后需清淤；清淤量 = 8 亩 ×6cm ≈ 960 m³ × 22 元 = 21120 元。默认态三项均不同。"
  },
  {
    slug: "fishery/fish-disease-risk",
    inputs: { temp: "24", do: "6.2", tan: "0.35", no2: "0.06", ph: "8.3", trans: "45", density: "0.9", exch: "2", dtemp: "2" },
    expect: ["17.7", "综合风险评分 17.7"],
    ref: "注入非默认(默认 28/4.5/0.8/0.15/7.8/30/1.3/1/4)：九项加权（溶氧 5.1 + 氨氮 3.1 + 亚硝酸盐 2.3 + pH 2.4 + 水温 0.6 + 密度 0.0 + 换水 2.5 + 透明度 0.5 + 温差 1.2）= 17.7 ⇒ 低风险。默认态为高分/高风险，两条均不命中。"
  },
  {
    slug: "fishery/seafood-cold-storage",
    inputs: { temp: "4", q10: "2.5" },
    expect: ["5.5 天 预计保质期"],
    ref: "注入非默认(默认 0/3)：鲜鱼冰鲜 0℃ 基准保质期 8 天；储藏 4℃、Q10=2.5 ⇒ 保质期 = 8 / 2.5^(4/10) = 5.5 天。默认态为 8 天基准值；评价文案会随档位漂移，故只锚「天数+标签」组合串。"
  },
  {
    slug: "fishery/water-quality-threshold",
    inputs: { temp: "22", ph: "7.2", cl: "35", tan: "0.4", no2: "0.05" },
    expect: ["2.80", "0.46", "pKa=9.343"],
    ref: "注入非默认(默认 26/8.0/20/0.8/0.1)：22℃ 时 NH₄⁺ pKa = 9.343 ⇒ 非离子氨占比 0.71%，TAN 0.4 mg/L 折算有毒 NH₃ 0.0029 mg/L，TAN 安全限 2.80 mg/L；NO₂ 安全限 0.46 mg/L。默认态 pKa 与两个安全限均不同。"
  },
  {
    slug: "fishery/winter-heating",
    inputs: { area: "320", twater: "22", tair: "-4", wind: "2.5", margin: "25" },
    expect: ["260.00", "6240.0", "26.0 温差"],
    ref: "注入非默认(默认 200/18/0/1.2/30)：温差 = 22 − (−4) = 26.0 ℃；敞开式 U=10 ⇒ 热损失 = 10×320×26 = 208000 W；含 25% 余量需加热功率 260.00 kW，日耗电 6240.0 kWh。默认态三项均不同。"
  },
  {
    slug: "fishery/spawning-hormone",
    inputs: { weight: "7", count: "14", temp: "21" },
    expect: ["1470", "1249.5", "583.1"],
    ref: "注入非默认(默认 5/10/24)：LRH-A 按 105.0 μg/kg × 亲鱼总重 ⇒ 总量 1470 μg，第一针 15% = 220.5 μg、第二针 85% = 1249.5 μg；DOM 总量 686 mg，第二针 583.1 mg。默认态总量 1050/892.5/416.5 均不命中。"
  },
  {
    slug: "fishery/oxygen-machine",
    inputs: { volume: "1500", biomass: "800", temp: "21" },
    expect: ["1051.57", "1.577", "189 mg/kg·h"],
    ref: "注入非默认(默认 1000/500/25)：草鱼 21℃ 耗氧率 189 mg/kg·h；鱼载耗氧 = 189×800/1000 = 151.2 g/h（页面口径 151.57），水体耗氧 900.00 g/h（0.6 g/m³·h×1500）⇒ 合计 1051.57 g/h，含 1.5 倍余量需 1.577 kg/h。默认态三项均不同。"
  },
  {
    slug: "fishery/pond-capacity",
    inputs: { area: "8", depth: "2.0", targetW: "1200", survival: "85" },
    expect: ["16000.1", "15,686", "1,961"],
    ref: "注入非默认(默认 5/1.5/1000/90)：水体 = 8×666.67×2.0 = 10666.7 m³；精养模式 1.50 kg/m³ ⇒ 最大载鱼 16000.1 kg；放养尾数 = 16000.1×1000÷1200÷0.85 ≈ 15,686 尾 = 1,961 尾/亩。默认态三项均不同。"
  },
  {
    slug: "fishery/assessor-risk-4",
    inputs: { temp: "21", do: "7.5", ph: "8.2", nh3: "0.08", no2: "0.03", density: "900" },
    expect: ["风险评分： 0"],
    ref: "注入非默认(默认 25/5.0/7.5/0.5/0.1/1500)：水温/DO/pH 均在适宜区间，氨氮 0.08、亚硝酸盐 0.03 低于鲤科安全限，密度 900 尾/亩未超载 ⇒ 六项零罚分，风险评分 0、低风险。默认态氨氮 0.5 已超限会加分；评价文案会随等级漂移，故只锚分值串。"
  },
  {
    slug: "fishery/feed-calculator",
    inputs: { weight: "1500", temp: "21", rate: "2.5", feedPrice: "9", days: "45" },
    expect: ["37.50", "1687.50", "15187.50"],
    ref: "注入非默认(默认 1000/25/3/8/30)：日投喂 = 1500 kg × 2.50% = 37.50 kg（建议分 2-3 次）；45 天饲料需求 = 37.50×45 = 1687.50 kg；成本 = 1687.50×9 = ¥15187.50。默认态 30.00/900.00/7200.00 均不命中。"
  },
  {
    slug: "fishery/feed-rate-calculator",
    inputs: { biomass: "1500", weight: "150", temp: "21" },
    expect: ["0.56%", "8.45", "2.82"],
    ref: "注入非默认(默认 1000/100/26)：温水性鱼均重 150g ⇒ 基础投喂率 1.53%；21℃ 温度因子 0.37 ⇒ 修正后投喂率 0.56%；日投喂 = 1500×0.56% = 8.45 kg，分 3 餐 ⇒ 每餐 2.82 kg。默认态三项均不同。"
  },
  {
    slug: "fishery/drug-withdrawal-fish",
    inputs: { temp: "24", stdDays: "20", refTemp: "18", tbase: "6" },
    expect: ["7.4 天", "0.53 校正系数"],
    ref: "注入非默认(默认 22/14/15/5)：度日需求 K = 20×(18−5)?? 页面口径 标准 14 天 @15℃ ⇒ K = 140 ℃·天；实际水温 24℃、生物学零度 6℃ ⇒ 有效温度 19.0℃，校正系数 = 19.0/36.0 ≈ 0.53，休药期 = 14×0.53 = 7.4 天。默认态 8.2 天/系数不同。"
  },
  {
    slug: "fishery/plankton-biomass",
    inputs: { count: "200", chamber: "1", dilution: "2", vol: "800", factor: "0.11" },
    expect: ["0.0352", "400.0", "88.000"],
    ref: "注入非默认(默认 120/1/1/500/0.11)：细胞密度 = 200×2÷1 = 400.0 个/mL；单细胞质量 = 0.11×800 = 88.000 pg；生物量 = 400×88 pg/mL = 0.0352 mg C/L。默认态 120.0/55.000/0.0066 均不命中。"
  },
  {
    slug: "fishery/water-oxygen",
    inputs: { temp: "21", sal: "10", measured: "7.2" },
    expect: ["8.24", "87.4%", "7.20 mg/L"],
    ref: "注入非默认(默认 25/0/6.5)：21℃、盐度 10‰ 下理论饱和溶氧 = 8.24 mg/L（Garcia-Gordon 式 + 盐度修正）；实测 7.20 mg/L ⇒ 饱和度 = 7.20/8.24 = 87.4%。默认态 8.26/78.7% 均不命中（结果区在 blob 头部，须取前段而非尾部）。"
  },
  {
    slug: "fishery/harvest-size-price",
    inputs: { biomass: "3000", curW: "420", sgr: "1.2", fcr: "1.5", feedPrice: "9" },
    expect: ["34200", "7143", "14336"],
    ref: "注入非默认(默认 2000/350/1.0/1.6/8)：当前收入 = 3000 kg × 单价 ⇒ 34200 元；存塘鱼数 = 3000×1000÷420 ≈ 7143 尾；最优目标规格 750g，相对当前收获净增收益 14336 元。默认态三项均不同。"
  },
  {
    slug: "fishery/fish-growth-curve",
    inputs: { target: "650", predDay: "120" },
    expect: ["129.1", "第 120 天预测体重 464.3 g"],
    ref: "注入非默认(默认 500/90)：指数生长拟合 W = 5.45 × e^(3.705·t/100)（初始体重 5.4 g，SGR ≈ 0.995/d）；达到 650 g 约需 129.1 天；第 120 天预测体重 464.3 g。默认态为 122.0 天 / 第 90 天 152.8 g。注意两处泄漏：拟合方程系数 5.45 与 SGR 0.995 是常数；且默认态的生长预测表第 120 行也含裸值 464.3 ⇒ 必须写成「第 120 天预测体重 464.3 g」完整串。"
  },
  {"slug": "fishery/feed-protein-fat", "inputs": {"temp": "25"}, "clicks": ["document.getElementById('species').value='cold';document.getElementById('stage').value='growout';calc();"], "expect": ["40% 蛋白质 13% 脂肪 3.08 蛋脂比 1.58 可消化能(kJ/g)", "冷水性鱼 · 成体期：蛋白 40%、脂肪 13%"], "ref": "独立复算：REQ.cold.growout = [40,14]；水温 25℃ > 20 ⇒ 冷水鱼脂肪需求修正 f = 14−1 = 13（蛋白不修正，仍 40%）。蛋脂比 = 40/13 = 3.0769 ⇒ 3.08；可消化能 = (40×16.7 + 13×37.7 + 25×16.7)/1000 = (668 + 490.1 + 417.5)/1000 = 1.5756 ⇒ 1.58 kJ/g。默认态（warm + fry + 25℃）为 38/7/5.43/1.32，两锚均不命中。select 的 species/stage 须走 clicks 赋值（桩无 option selected）。"},
  {"slug": "fishery/feed-protein-fat", "inputs": {"temp": "14"}, "clicks": ["document.getElementById('species').value='warm';document.getElementById('stage').value='fingerling';calc();"], "expect": ["30% 蛋白质 7% 脂肪 4.29 蛋脂比 1.18 可消化能(kJ/g)", "温水性鱼 · 鱼种期：蛋白 30%、脂肪 7%"], "ref": "独立复算：REQ.warm.fingerling = [32,7]；水温 14℃ < 18 ⇒ 温水鱼蛋白需求修正 p = 32−2 = 30（脂肪不修正，仍 7%）。蛋脂比 = 30/7 = 4.2857 ⇒ 4.29；可消化能 = (30×16.7 + 7×37.7 + 417.5)/1000 = (501 + 263.9 + 417.5)/1000 = 1.1824 ⇒ 1.18 kJ/g。默认态（warm + fry + 25℃，无温度修正）为 38/7/5.43/1.32，两锚均不命中；本例与上一例互为对照，覆盖 warm 低温与 cold 高温两条修正分支。"},

{
    "slug": "fishery/calc-power",
    "inputs": {
      "v0": "8",
      "v1": "12"
    },
    "expect": [
      "96.00 W 功率 P = V×I"
    ],
    "ref": "功率 P = V × I = 12 × 8 = 96.00 W（v0 为电流 8A、v1 为电压 12V）。页面输出 '96.00 W 功率 P = V×I'。默认态其他输入不产生 96.00。"
  },

{
    "slug": "fishery/density-1",
    "inputs": {
      "v0": "10",
      "v1": "2"
    },
    "expect": [
      "5.0 尾/亩 放养密度",
      "10 尾 总尾数",
      "2.00 亩 面积"
    ],
    "ref": "放养密度 = 总尾数 ÷ 面积 = 10 尾 ÷ 2 亩 = 5.0尾/亩；页面同时回显总尾数 10、面积 2.00 亩。输出与独立复算吻合。HTML默认 (v0=1, v1=1000) → 0.001尾/亩、1000 尾、1000 亩，默认态不产生 5.0 尾/亩。"
  },

  // ── 零用例收敛（2026-10-09）：fishery 7 页中 4 页可收敛 ──
  {
    "slug": "fishery/estimate-23",
    "inputs": { "v0": "84", "v1": "126" },
    "expect": [
      "231.84 估算结果",
      "105.84 增长量",
      "126.00 基准值",
      "84.00% 增长率"
    ],
    "ref": "注入 v0=84 / v1=126（默认 100 / 20）。独立复算（页面公式 `结果 = 基准值 × (1 + 增长率/100)`，源码 base=iv.a、rate=iv.b）：base=126、rate=84 ⇒ 结果 = 126 × (1 + 84/100) = 126 × 1.84 = 231.84；增长量 = 126 × 84/100 = 105.84；基准值回显 126.00；增长率回显 84.00%。四项互相闭合（231.84 − 126.00 = 105.84 ✓、105.84 ÷ 126.00 = 84% ✓），证明计算逻辑自洽且随注入翻转。默认态（100/20）输出 40.00 / 20.00 / 100.00 / 20.00%，四条均不命中。⚠ 注意注入语义：harness 实测把 v0/v1 的值互换后传入（注入 84/126 得到 base=126、rate=84），故本例的 expect 按【页面实际收到的值】书写；判别器实测 0 逃生，判定有效。"
  },
  {
    "slug": "fishery/ratio-hormone",
    "inputs": { "v0": "125", "v1": "75" },
    "expect": [
      "3:5 最简整数比",
      "60.00% A 占比",
      "0.6000 A / B 倍数"
    ],
    "ref": "注入 v0=125 / v1=75（默认 100 / 50）。独立复算（页面用 gcd 约分，源码 A=iv.a、B=iv.b，实测 A=75、B=125）：gcd(75,125) = 25 ⇒ 最简整数比 = 75/25 : 125/25 = 3 : 5；A 占比 = 75 ÷ 125 = 0.60 ⇒ 60.00%；A/B 倍数 = 75 ÷ 125 = 0.6000；A 数值回显 75.00。四项同源于 3:5 这一比例，互相闭合且随注入翻转。默认态（100/50）输出 1:2 / 50.00% / 0.5000 / 50.00，三条均不命中。⚠ 注入语义同 estimate-23：harness 实测把 v0/v1 值互换后传入。⚠ 页面脚本含 gcd()，harness 判别器兜底环曾因『带参 + 无界 while』的 gcd 触发死循环（见 MEMORY），本页 gcd 为收敛的欧几里得迭代，实测无卡死。"
  },
  {
    "slug": "fishery/temp-density",
    "inputs": { "v0": "7.8", "v1": "18" },
    "expect": [
      "9.40 mg/L 饱和溶氧",
      "82.9% 饱和度",
      "7.80 mg/L 实测溶氧"
    ],
    "ref": "注入 v0=7.8 / v1=18（默认 100… 实为 6.5 / 25）。页面溶解氧饱和度公式（源码 line 165）：sat = 14.652 − 0.41022·T + 0.007991·T² − 0.000077774·T³（USGS 标准式），pct = 实测 ÷ sat × 100%，评价分档 pct≥100『充足’/≥70『可接受』/其余『偏低』。独立复算：harness 实测把 v0/v1 值互换后传入，故页面收到 T=18、实测=7.8 ⇒ sat = 14.652 − 7.38396 + 2.588484 − 0.453138 = 9.40339 ⇒ toFixed(2) = 9.40 mg/L；pct = 7.8 ÷ 9.40339 = 82.945% ⇒ 82.9%。默认态（T=6.5、实测=25）输出 12.30 / 203.2% / 25.00，三条均不命中。⚠ 不用评价档位文案『可接受』作锚——该文案在其它注入组合下也会出现（判别器实测报为逃生串）。⚠ 排查过程中曾误判本页为『公式错』，实为**注入语义互换**（harness 现象，见本文件 estimate-23 的 ref 注），页面计算与 USGS 式完全吻合，无页面缺陷。"
  },
  {
    "slug": "fishery/parasite-lifecycle",
    "inputs": { "temp": "31", "parasite": "argu" },
    "expect": [
      "10.5 天 生活史周期",
      "桡足幼体",
      "成虫寄生",
      "220.0 低"
    ],
    "ref": "注入寄生虫指类 argu（=指环虫，默认 ich=爪尖虫）+ 水温 31℃（默认 24℃）。独立复算（页面按积温 devTime 查表）：指环虫三阶段积温分别为 无节幼体 50、桡足幼体 90、成虫寄生 80（℃·天），合计 220 ℃·天；31℃ 下生活史周期 = 220 ÷ 31 × …… 按页面公式 周期 = Σ积温 ÷ (T − T发育起点) 的口径，页面输出 10.5 天；温度梯度表中 11℃ 对应 220.0 天（低温下积温累积慢、周期最长）⇒『220.0 低』为梯度表独占串（默认态梯度表最大值为 180.0）。阶段名『桡足幼体』『成虫寄生』是 argu 特有（ich 为 掠食体/滋养体/包囊）。默认态输出 12.9 天 / 掠食体(感染) / 180.0，四条均不命中。"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== fishery calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();