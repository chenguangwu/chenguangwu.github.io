#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "food/analysis-cost-6",
  "inputs": {
    "price": "68",
    "mainC": "18",
    "auxC": "6",
    "seaC": "3",
    "otherC": "5",
    "target": "60"
  },
  "expect": [
    "36.00",
    "52.94",
    "80.00",
    "47.06"
  ],
  "ref": "菜品成本：总成本=18+6+3+5=32.00；毛利=68-32=36.00；毛利率=36/68=52.94%；目标毛利率60%建议售价=32/(1-0.6)=80.00（独立复算；默认组 总成本=26.00/毛利=32.00/毛利率=55.17%，注入失败即不命中）"
},
{
  "slug": "food/analysis-menu",
  "inputs": {
    "menu": "红烧肉,18,48,60\n蒜蓉西兰花,6,22,95\n菌菇汤,9,28,40"
  },
  "expect": [
    "67.00",
    "4,080.00",
    "72.73"
  ],
  "ref": "菜单毛利率：总营收=2880+2090+1120=6090.00，总毛利=1800+1520+760=4080.00 → 综合毛利率 67.00%；蒜蓉西兰花单品毛利率 1520/2090=72.73%（独立复算，非页面默认菜单）",
},
{
  "slug": "food/beer-gravity-estimator",
  "inputs": {
    "water": "30",
    "efficiency": "75",
    "attenuation": "75",
    "malt-wt-' + idx + '": "' + m.weight + '",
    "malt-ppg-' + idx + '": "' + (m.ppg || 35) + '"
  },
  "expect": [
    "1.005"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/calc-concentration",
  "inputs": {
    "v1": "150",
    "v2": "20"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/checker-13",
  "inputs": {
    "s0": "14",
    "s1": "8",
    "s2": "9",
    "s3": "10",
    "s4": "8",
    "s5": "7",
    "tvc": "5000"
  },
  "expect": [
    "14/10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/convert-19",
  "inputs": {
    "og": "4.05",
    "fg": "1.010"
  },
  "expect": [
    "413.04"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/convert-concentration",
  "inputs": {
    "val": "30"
  },
  "expect": [
    "1.129"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/convert-ratio-seasoning",
  "inputs": {
    "base": "15",
    "mult": "3"
  },
  "expect": [
    "45.0g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/dough-fermentation-time",
  "inputs": {
    "temp": "38",
    "yeast": "1"
  },
  "expect": [
    "建议降温至30°C以下"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/food-calculator",
  "inputs": {
    "bakeOriginalSize": "30",
    "bakeTargetSize": "24",
    "coffeePowder": "18",
    "saltFoodWeight": "1000",
    "saltWeight": "30"
  },
  "expect": [
    "706.9cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/food-calorie-counter",
  "clicks": [
    "addFood('主食类',0);addFood('蛋白质类',1);"
  ],
  "expect": [
    "281 总热量 (千卡)"
  ],
  "ref": "去默认化（原 expect「116」＝主食类米饭卡片恒显的卡路里标签，注入失败仍命中 → 逃生项）：clicks 调 addFood 加米饭(116)+鸡胸肉(165)，totals 渲染「281 总热量 (千卡) 14g 蛋白质 (估) 9g 脂肪 (估) 35g 碳水 (估)」；默认 totals 为「0 总热量 (千卡)」不含 281，注入失败即不命中。（addFood 内 localStorage.setItem 在 harness 下可用，渲染先于写入，totals 已正确生成。）"
},
{
  "slug": "food/food-pairing",
  "inputs": {
    "searchInput": "番"
  },
  "clicks": ["toggle('番茄');toggle('鸡蛋');analyze()"],
  "expect": [
    "番茄 + 鸡蛋 = 经典组合",
    "番茄富含番茄红素",
    "鸡蛋是百搭食材"
  ],
  "ref": "click 驱动页：selected 是页面顶层 Set，只有 toggle(name) 能写入；注入 番茄+鸡蛋 后 analyze() 出搭配分析。"
     + "默认态 selected 为空 ⇒ analyze() 走 showToast 分支、results 恒空 ⇒ 三项均不命中。"
     + "不锚 selected 区的「番茄 ✕ 鸡蛋 ✕」—— 兜底阶段无参 toggle() 会往 Set 里塞入 undefined，"
     + "该串变成「番茄 ✕ 鸡蛋 ✕ undefined ✕」不稳定。原 expect「undefined」正来源于此。",
},
{
  "slug": "food/nutrition-calculator",
  "inputs": {
    "grams": "200",
    "foodSel": "白米饭"
  },
  "clicks": [
    "addFood();"
  ],
  "expect": [
    "碳水 56.0g"
  ],
  "ref": "inputs 注入静态控件（grams / foodSel）+ clicks 触发 addFood()：白米饭每 100g 为 kcal 130 / 蛋白 2.6 / 脂肪 0.3 / 碳水 28，200g 即 factor=2 ⇒ 独立复算 kcal 260、蛋白 5.2g、脂肪 0.6g、碳水 56.0g。旧锚是 select 里全部食物名的静态拼接（默认态即渲染）⇒ 判别力 0；新锚取「碳水 56.0g」——碳水值由 grams 驱动且默认态列表为空（`summary` 隐藏、dishList 空串）不产出该串 ⇒ 零逃生项。注意 addFood 会清空 grams，写值必须在触发前完成（inputs 阶段天然先于 clicks）。"
},
{
  "slug": "food/oil-absorption-estimator",
  "inputs": {
    "weight": "750",
    "time": "5",
    "temp": "180"
  },
  "expect": [
    "1013"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/recipe-generator",
  "inputs": {
    "cuisine": "sichuan"
  },
  "expect": [
    "sichuan"
  ],
  "ref": "菜系 cuisine=sichuan（默认 chinese）；生成器输出菜谱内容相同，仅菜系值随输入变化。「做法」为恒定标签（原逃生项），改锚定 sichuan。"
},
{
  "slug": "food/report-cost-profit",
  "inputs": {
    "rev": "50000",
    "food": "18000",
    "labor": "9000",
    "rent": "6000",
    "util": "2000",
    "other": "1500"
  },
  "expect": [
    "毛利： 32000.00",
    "营业利润： 13500.00",
    "盈亏平衡营收： 28906.25"
  ],
  "ref": "毛利=50000-18000=32000（毛利率64.00%）；期间费用=9000+6000+2000+1500=18500；营业利润=32000-18500=13500；盈亏平衡营收=18500÷0.64=28906.25（独立复算；默认 10000/4000/2500/1500/500/500 → 毛利6000、利润1000、保本8333.33，注入失败即不命中）"
},
{
  "slug": "food/soup-ratio-optimizer",
  "inputs": {
    "soupVol": "1500",
    "saltPref": "0",
    "umamiPref": "0",
    "sourPref": "0"
  },
  "expect": [
    "1500ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/stats-ingredient",
  "inputs": {
    "data": "黑豆,200\n菠菜,150\n全麦面包,100"
  },
  "expect": [
    "总膳食纤维： 26.70",
    "占成人推荐量(25 g/天)： 106.80"
  ],
  "ref": "膳食纤维：黑豆8.7×2=17.40 + 菠菜2.2×1.5=3.30 + 全麦面包6.0×1=6.00 = 26.70g；占RDA(25g)=106.80%（独立复算；默认 燕麦/苹果/西兰花=11.2g/44.80%，注入失败即不命中）"
},
{
  "slug": "food/stats-simulator-flavor",
  "inputs": {
    "data": "甜,12\n咸,55\n辣,18\n酸,15"
  },
  "expect": [
    "最偏好： 咸",
    "55.00%"
  ],
  "ref": "口味分布：总100，咸55→55.00% 最高（独立复算；默认 甜40/咸25/辣20/酸15 最偏好甜，注入失败即不命中）"
},
{
  "slug": "food/syrup-brix-converter",
  "inputs": {
    "inp-brix": "30",
    "inp-sg": "1.0833",
    "inp-baume": "11.1"
  },
  "expect": [
    "30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/vitamin-c-compare",
  "inputs": {
    "dailyNeed": "150"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/wine-alcohol-converter",
  "inputs": {
    "og-input": "4.09",
    "fg-input": "0.995",
    "conv-val": "15"
  },
  "expect": [
    "4.0900"
  ],
  "ref": "auto-restore"
},
  {
    slug: "food/convert-20",
    inputs: { variety: "4" },
    expect: ["1600 菜品辣度（SHU）", "品种：卡宴，公开参考区间 30000 至 50000 SHU（中值 40000）"],
    ref: '注入 variety=4（卡宴，区间30000–50000，中值40000）：base=40000；dish=40000×20÷500=1600；ppm=40000÷15=2666.7；mg=2666.7×20÷1000=53.33；maxG=5000×500÷40000=62.5。默认态 variety=0（甜椒,base=0）→菜品辣度0、辣度等级「不辣」、品种为甜椒，注入失败即三项均不命中（已 dump 实测确认）。'
  },
  {
    slug: "food/convert-20",
    inputs: { variety: "7" },
    expect: ["37929 菜品辣度（SHU）", "品种：鬼椒 Bhut Jolokia，公开参考区间 855000 至 1041427 SHU（中值 948214）"],
    ref: '注入 variety=7（鬼椒 Bhut Jolokia，区间855000–1041427，中值948214）：base=(855000+1041427)/2=948213.5→948214；dish=948213.5×20÷500=37928.54→37929；ppm=948213.5÷15=63214.2；mg=63214.2×20÷1000=1264.28；maxG=5000×500÷948213.5=2.6。默认甜椒 base=0→菜品辣度0、等级不辣，注入失败不命中（已 dump 实测确认）。'
  },
  {
    slug: "food/convert-20",
    inputs: { mode: "shu", shuIn: "120000" },
    expect: ["4800 菜品辣度（SHU）", "品种：自定义输入，公开参考区间 120000 至 120000 SHU（中值 120000）"],
    ref: '注入 mode=shu & shuIn=120000：base=120000；dish=120000×20÷500=4800；ppm=120000÷15=8000.0；mg=8000.0×20÷1000=160.00；maxG=5000×500÷120000=20.8。默认 mode=dish&variety=0→base=0、菜品辣度0，注入失败不命中（已 dump 实测确认）。'
  },
  {
    slug: "food/convert-20",
    inputs: { variety: "8", amount: "10", totalW: "1000" },
    expect: ["18500 菜品辣度（SHU）", "品种：卡罗莱纳死神，公开参考区间 1500000 至 2200000 SHU（中值 1850000）"],
    ref: '注入 variety=8（卡罗莱纳死神，区间1500000–2200000，中值1850000）& amount=10 & totalW=1000：base=1850000；dish=1850000×10÷1000=18500；ppm=1850000÷15=123333.3；mg=123333.3×10÷1000=1233.33；maxG=5000×1000÷1850000=2.7。默认甜椒 base=0→菜品辣度0，注入失败不命中（已 dump 实测确认）。'
  },
  {
    slug: "food/convert-20",
    inputs: { variety: "5", amount: "50", totalW: "200", target: "8000" },
    expect: ["18750 菜品辣度（SHU）", "不超过目标 8000 SHU：最大用量 21.3 g，当前浓度需稀释 2.34 倍"],
    ref: '注入 variety=5（泰椒，区间50000–100000，中值75000）& amount=50 & totalW=200 & target=8000：base=75000；dish=75000×50÷200=18750；ppm=75000÷15=5000.0；mg=5000.0×50÷1000=250.00；maxG=8000×200÷75000=21.3；dil=18750÷8000=2.34。默认 target=5000 且甜椒base=0→最大用量0.0、稀释0.00倍，且「不超过目标 8000 SHU」整串默认态为「不超过目标 5000 SHU」不命中（已 dump 实测确认）。'
  },
  {
    slug: "food/convert-20",
    inputs: { variety: "2", amount: "100", totalW: "800", target: "3000" },
    expect: ["656 菜品辣度（SHU）", "品种：墨西哥椒 Jalapeño，公开参考区间 2500 至 8000 SHU（中值 5250）"],
    ref: '注入 variety=2（墨西哥椒 Jalapeño，区间2500–8000，中值5250）& amount=100 & totalW=800 & target=3000：base=5250；dish=5250×100÷800=656.25→656；ppm=5250÷15=350.0；mg=350.0×100÷1000=35.00；maxG=3000×800÷5250=457.1；dil=656.25÷3000=0.22。默认甜椒base=0→菜品辣度0、等级不辣，注入失败不命中（已 dump 实测确认）。'
  }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== food calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
