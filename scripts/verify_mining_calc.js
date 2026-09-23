#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "mining/calc-1",
  "inputs": {
    "q": "0.5",
    "k": "0.35",
    "a": "4.0",
    "b": "3.0",
    "H": "12",
    "W": "3.0",
    "holes": "25",
    "stem": "2.5"
  },
  "expect": [
    "72.00 单孔药量（kg）",
    "144.00 单孔爆破方量（m³）",
    "3600.0 总爆破方量（m³）"
  ],
  "ref": "去默认化（原 expect「近似」出堵塞长度说明行，与输入无关）：单孔方量 = a×b×H = 4.0×3.0×12 = 144.00；总方量 = 144×25 = 3600.0；单孔药量 = q×144 = 0.5×144 = 72.00；总药量 = 1800.00。默认 0.45/3.0/2.5/10/20 得 33.75 / 75.00 / 1500.0，注入失败即不命中"
},
{
  "slug": "mining/calc-ventilation",
  "inputs": {
    "workers": "45",
    "diesel": "150",
    "explosive": "60",
    "gas": "2",
    "cmax": "0.8",
    "leak": "1.15"
  },
  "expect": [
    "4 × 150 600.0",
    "1725.0 设计风量 (m³/min)",
    "28.75 设计风量 (m³/s)"
  ],
  "ref": "去默认化（原 expect「暂无计算记录」＝历史占位串，恒命中）：按人数 4×45=180.0、按柴油 4×150=600.0、按炸药 25×60=1500.0（控制项）、按瓦斯 100×2/0.8=250.0；设计风量 = 1500.0×1.15 = 1725.0 m³/min = 28.75 m³/s。默认 30/120/50/3/1/1.2 得 480.0 / 1250.0 / 1500.0 / 25.00，注入失败即不命中"
},
{
  "slug": "mining/checker-training-hr",
  "inputs": {
    "gas": "1.5",
    "vent": "6000",
    "ventReq": "7500",
    "equip": "90",
    "train": "85",
    "hours": "20",
    "rect": "88",
    "monitor": "98"
  },
  "expect": [
    "达标项目： 1/6",
    "0.80倍需求",
    "不达标（停产整顿）"
  ],
  "ref": "去默认化（原 expect「本要求」出自末尾静态标准依据文案，与输入无关）：瓦斯 1.5%>1.0 不达标、风量 6000/7500=0.80 倍<1.0 不达标、设备完好率 90%<95% 不达标、培训 85%<90% 且 20h<24h 不达标、整改率 88%<90% 不达标、监测 98%≥95% 达标 ⇒ 1/6，等级「不达标（停产整顿）」。默认全达标 6/6、一级，三串均不命中"
},
{
  "slug": "mining/convert-grade-ore",
  "inputs": {
    "val": "3.6",
    "rate": "0.85"
  },
  "expect": [
    "3.060000",
    "系数: 0.85"
  ],
  "ref": "去默认化（原 expect「系数」是静态标签）：r = 3.6 × 0.85 × 1 / 1 = 3.060000（toFixed(6)）；系数行回显 0.85。默认 1/1 得 1.000000 与「系数: 1」，注入失败即不命中"
},
{
  "slug": "mining/excavation-volume",
  "inputs": {
    "swell": "1.25",
    "price": "35",
    "L": "30",
    "W": "12",
    "D": "3",
    "W1": "12",
    "W2": "6",
    "slope": "1",
    "D1": "20",
    "D2": "10",
    "H": "5"
  },
  "expect": [
    "1350.0 m³",
    "¥37,800"
  ],
  "ref": "去默认化（原 expect「单价」是卡片标签）：默认形状=长方体基坑，原状方量 = 30×12×3 = 1080.0 m³；松方量 = 1080×1.25 = 1350.0 m³；车次 = ceil(1350/20) = 68；总造价 = 1080×35 = ¥37,800。默认 25×10×2 / ×1.3 / ¥20 得 500.0 / 650.0 / ¥10,000。**注意**：本页 L/W/D 三个控件由 renderParams 模板写在 deep-dive 标记**之后**（第 244 行起），`pageDefaults` 只能取到 swell/price ⇒ 判别器模拟失败时 L/W/D 保持注入值不变，故 expect **不得**断言「1080.0 m³」（原状方量，换回 swell/price 后仍命中＝逃生项）。松方量与总造价同时依赖 swell=1.25 / price=35，回退即变 1404.0 m³ 与 ¥21,600，才会真正变红"
},
{
  "slug": "mining/haulage-optimization",
  "inputs": {
    "totalTonnage": "2400",
    "shiftMinutes": "480",
    "carCapacity": "25",
    "loadFactor": "0.85",
    "loadTime": "6",
    "haulTime": "15",
    "dumpTime": "4",
    "returnTime": "12",
    "waitTime": "3",
    "utilization": "80"
  },
  "expect": [
    "21.25 实际载重 (吨)",
    "2,448 吨（余量 2.0%）",
    "300 吨/小时"
  ],
  "ref": "去默认化（原 expect「各项指标合理」是结论词，默认态同样合理）：循环 = 6+15+4+12+3 = 40.0 min；实际载重 = 25×0.85 = 21.25 吨；班趟数 = 480×0.80/40 = 9.6；单车班产量 = 9.6×21.25 = 204 吨；所需矿车数 = ceil(2400/204) = 12；总运输能力 = 12×204 = 2,448 吨（余量 2.0%）；小时强度 = 2400/8 = 300 吨/小时。默认 1500/20/0.9/5/12/3/10/3/75 得 18.00 / 1,571 吨（余量 4.7%）/ 188 吨/小时，注入失败即不命中"
},
{
  "slug": "mining/mineral-density",
  "inputs": {
    "mass": "1440",
    "volume": "600",
    "solidVol": "480"
  },
  "expect": [
    "3.00 t/m³",
    "2.40 t/m³",
    "孔隙比 (e) 0.25"
  ],
  "ref": "去默认化（原 expect「孔隙比」是静态标签）：真密度 = 1440/480 = 3.00 t/m³；体积密度 = 1440/600 = 2.40 t/m³；孔隙率 = (600−480)/600 = 20.0%；孔隙比 e = 120/480 = 0.25。默认 1000/500/350 得 2.86 / 2.00 / 30.0% / 0.43，注入失败即不命中"
},
{
  "slug": "mining/ore-grade",
  "inputs": {
    "gradeInput": "5.0",
    "oreAmount": "200000",
    "metalPrice": "400"
  },
  "expect": [
    "1,000.00 金属含量 (kg)",
    "2,000.00 元/吨",
    "品位评价： 富矿"
  ],
  "ref": "去默认化（原 expect「品位」是静态标签）：金属量 = 5.0 g/t × 200000 t = 1,000,000 g = 1,000.00 kg（1.0000 吨）；品位 = 0.0005%；价值 = 1,000,000 g × 400 元/g = 400,000,000.00 元；每吨 = 400,000,000/200000 = 2,000.00 元/吨；评价「富矿」。默认 3.5/100000/500 得 350.00 kg / 1,750.00 元/吨 / 工业品位，注入失败即不命中"
},
{
  "slug": "mining/reserve-estimate",
  "inputs": {
    "areaInput": "80000",
    "thickInput": "6.0",
    "densityInput": "2.5",
    "gradeInput": "2.0",
    "recoveryInput": "90"
  },
  "expect": [
    "480,000 矿石体积 (m³)",
    "1,200,000 地质储量 (吨)",
    "1,080,000 可采储量 (吨)",
    "2.1600 吨"
  ],
  "ref": "去默认化（原 expect「中型矿床」等级词与默认同档，换值后仍是中型 ⇒ 无判别力）：体积 = 80000×6.0 = 480,000 m³；地质储量 = 480000×2.5 = 1,200,000 吨；可采 = ×0.90 = 1,080,000 吨；金属总量 = 1,200,000×2.0 g = 2,400.00 kg（2.4000 吨）；可采金属量 = 2.4000×0.90 = 2.1600 吨。默认 50000/12.5/2.8/3.2/85 得 625,000 / 1,750,000 / 1,487,500 / 4.7600，注入失败即不命中（「储量规模： 中型矿床」两档相同，不可作 expect）"
},
{
  "slug": "mining/analysis-cost-3",
  "inputs": {
    "output": "10000",
    "cost": "5000000",
    "grade": "2.5",
    "waste": "30000",
    "price": "60000"
  },
  "expect": [
    "500.00",
    "3.00",
    "250",
    "20000.00",
    "66.67%"
  ],
  "ref": "非默认输入+独立复算：吨矿成本500.00、剥采比3.00、金属产量250、单位金属成本20000.00、毛利率66.67%（默认5000/2000000/1.8/10000/55000 输出400/2/90/22222.22/59.60，注入失败即不命中）"
},
{
  "slug": "mining/estimate-reserve",
  "inputs": {},
  "expect": [
    "请先添加至少一个块段"
  ],
  "ref": "结构性不可注入（2026-09-24 定性）：块段行由 addBlock() 按钮 + class 选择器（.b-area/.b-thick/.b-density/.b-grade）动态生成，静态 HTML 里除 id=blockBody/blockTable/historyBox/res 外**无任何带 id 的控件**，harness 无 clicks 且 addBlock 无参调用不产生默认块段 ⇒ 只能断言空态提示。保留在 no_inputs 基线内，勿重复选批"
},
{
  "slug": "mining/safety-check",
  "inputs": {
    "riskValue": "18"
  },
  "expect": [
    "18"
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
  console.log("==== mining calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
