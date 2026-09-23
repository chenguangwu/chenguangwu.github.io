#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chemical/calc-pipeline-pressure-drop",
  "inputs": {
    "v0": "300",
    "v1": "150",
    "v2": "2.0",
    "v3": "850",
    "v4": "0.0005",
    "v5": "0.1"
  },
  "expect": [
    "3.29 kPa",
    "1020000",
    "0.0039",
    "0.394 m"
  ]
},
{
  "slug": "chemical/convert-capacity-tank",
  "inputs": {
    "val": "2.5",
    "rate": "1.6"
  },
  "expect": [
    "4.000000",
    "系数: 1.6"
  ],
  "ref": "去默认化（原 expect「系数」是静态标签，默认态必命中＝逃生项）：r = 2.5 × 1.6 × 1 / 1 = 4.000000（toFixed(6)）；系数行回显 1.6。默认 val=1/rate=1 得 1.000000 与「系数: 1」，注入失败即不命中"
},
{
  "slug": "chemical/convert-density-crude",
  "inputs": {
    "val": "3.2",
    "rate": "0.75"
  },
  "expect": [
    "2.400000",
    "系数: 0.75"
  ],
  "ref": "去默认化：r = 3.2 × 0.75 × 1 / 1 = 2.400000（toFixed(6)）；系数行回显 0.75。默认 1/1 得 1.000000 与「系数: 1」，注入失败即不命中"
},
{
  "slug": "chemical/detector-39",
  "inputs": {
    "conc": "0.2",
    "vol": "20.00",
    "mass": "0.2500",
    "molar": "180.00",
    "ratio": "2",
    "threshold": "95.0",
    "g_mass": "0.6000",
    "g_dry": "0.5700",
    "g_factor": "1.050",
    "g_threshold": "97.0"
  },
  "expect": [
    "99.75",
    "≥97%"
  ],
  "ref": "去默认化（原 expect「纯度」是静态标签词）：harness 末次调用为 calcG（重量法页签），纯度 = m2×F/m1×100 = 0.57×1.05/0.6×100 = 99.75% ≥ 97 ⇒ 合格、判定行显示「≥97%」。默认 0.485×1/0.5 得 97.00%、阈值 98%，两串均不命中。注：本页滴定法页签的 conc/vol/mass/molar 不影响最终 res（被 calcG 覆盖），故须改 g_* 四键"
},
{
  "slug": "chemical/miaomu-guige-zhiliang-yanshou-biaozhun",
  "inputs": {
    "v0": "200",
    "v1": "180",
    "v2": "165"
  },
  "expect": [
    "90.0%",
    "82.5%",
    "86.3"
  ]
},
{
  "slug": "chemical/mixture-ratio",
  "inputs": {
    "ca": "60",
    "ma": "200",
    "cb": "30",
    "mb": "100",
    "c1": "95",
    "v1": "500",
    "c2": "70",
    "value": "25",
    "al1": "95",
    "al2": "40"
  },
  "expect": [
    "混合浓度 50.00%",
    "混合比 (A:B) 200 : 100"
  ],
  "ref": "去默认化（原 expect「混合比」是静态标签词，默认态同样命中 = 逃生项）：A 60%×200 + B 30%×100，总质量 300 ⇒ 混合浓度 (12000+3000)/300 = 50.00%；混合比 200 : 100。默认 80/100/20/300 得 35.00% 与 100 : 300（v1 只影响「稀释」页签，不影响本结果，故须改 ca/ma/cb/mb）"
},
{
  "slug": "chemical/reaction-yield",
  "inputs": {
    "theo": "25",
    "actual": "21.25",
    "na": "0.5",
    "nb": "0.3",
    "ratio": "1",
    "m": "10",
    "m1": "100",
    "m2": "80",
    "coef": "1",
    "small": "5",
    "times": "10",
    "yield": "80",
    "big": "75"
  },
  "expect": [
    "85.00%",
    "3.75 g"
  ],
  "ref": "去默认化（原 expect「损失量」是卡片标签，与输入无关）：默认页签 cur=yield，产率 = 21.25/25×100 = 85.00%（70≤x<90 ⇒ 🟢 优秀），损失量 = 25−21.25 = 3.75 g。默认 7.5/10 得 75.00% 与 2.50 g，注入失败即不命中"
},
{
  "slug": "chemical/solution-concentration",
  "inputs": {
    "mass": "90",
    "molar": "45",
    "vol": "0.5",
    "solute": "10",
    "total": "100",
    "mg": "5",
    "kg": "1",
    "c1": "2",
    "v1": "100",
    "c2": "0.5"
  },
  "expect": [
    "4.0000 mol/L",
    "180.00 g/L"
  ],
  "ref": "去默认化（原 expect「质量浓度」是卡片标签）：默认页签=摩尔浓度，n = 90/45 = 2.0000 mol，C = 2.0000/0.5 = 4.0000 mol/L，质量浓度 = 90/0.5 = 180.00 g/L。默认 58.5/58.5/1 得 1.0000 mol/L 与 58.50 g/L，注入失败即不命中（注意：若只改 mass 与 vol 成比例，C 与质量浓度会与默认重合，必须打破比例）"
},
{
  "slug": "chemical/analysis-cost-7",
  "inputs": {
    "data": "11,22,33,44,55",
    "budget": "100",
    "topn": "2"
  },
  "expect": [
    "55.00",
    "60.00%",
    "超支 65.00"
  ],
  "ref": "非默认输入+独立复算：合计165、最大分项55、前2大项累计占比60.00%、对比预算100超支65（默认数据 800,200,1200,300,500,150 均不含 55.00/60.00%/超支65.00，注入失败即不命中）"
},
{
  "slug": "chemical/checker-15",
  "inputs": {
    "m0_0": "2",
    "m0_1": "2",
    "m0_2": "2",
    "m0_3": "1",
    "m0_4": "0",
    "m1_0": "2",
    "m1_1": "2",
    "m1_2": "2",
    "m1_3": "1",
    "m1_4": "1",
    "m1_5": "0",
    "m2_0": "2",
    "m2_1": "2",
    "m2_2": "2",
    "m2_3": "2",
    "m2_4": "1"
  },
  "expect": [
    "75%",
    "7/10",
    "8/12"
  ],
  "ref": "去默认化（原 expect「0/10」＝全零默认态即命中）：16 个 select 由 innerHTML 模板按 m{mi}_{ii} 生成，id 为确定值可注入。一、标准管理 2+2+2+1+0=7/10（70%），二、过程检查 2+2+2+1+1+0=8/12（67%），三、整改闭环 2+2+2+2+1=9/10（90%）；总分 24/32 ⇒ 合规度 round(75%)=75%（良好）。默认全 0 ⇒ 0% / 0-10 / 0-12，三串均不命中。注：id 不在静态 HTML 字面量里，discriminate_check 取不到默认值会「跳过」，已用同口径探针补验「注入 PASS + 回退全 0 FAIL」"
},
{
  "slug": "chemical/molar-mass",
  "inputs": {
    "formula": "H2O",
    "mass": "27"
  },
  "expect": [
    "9.025e+23"
  ],
  "ref": "auto-restore"
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
  console.log("==== chemical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
