#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hvac/cooling-tower",
  "inputs": {
    "flow": "800",
    "twIn": "40",
    "twOut": "33",
    "twb": "26",
    "cycles": "4",
    "driftRate": "0.002"
  },
  "expect": [
    "6,513.1",
    "12.80",
    "1.600"
  ],
  "ref": "非默认输入（默认 600/37/32/27/3/0.001）：冷却范围 dT = 40 − 33 = 7 °C；散热量 Q = 4.187 × 800 × 1000 × 7 ÷ 3600 = 6513.111 kW ⇒ 显示「6,513.1」；蒸发 E = 800×7×0.0015 = 8.40、飘水 D = 800×0.002 = 1.600、排污 B = 8.40÷(4−1) = 2.80、总补水 M = 8.40+1.600+2.80 = 12.80。默认态为 3,489.2 / 7.35 / 0.600。"
},
{
  "slug": "hvac/duct-calculator",
  "inputs": {
    "Q": "5000",
    "v": "10"
  },
  "expect": [
    "0.1389 所需截面积 F (m²)"
  ],
  "ref": "非默认输入（默认 3600/5）：所需截面积 F_req = Q÷(3600×v) = 5000÷(3600×10) = 0.138889 m² ⇒ 显示 0.1389（页面对 F_req 取 toFixed(4)）。该量只由 Q、v 决定，不随形状分支/管径取值变化（本页 harness 下恒走圆形分支且 diaD 不可注入，故不锚任何含管径的量），也不在零参兜底函数 suggestSize() 渲染的文案里。默认态 F_req = 3600÷(3600×5) = 0.2000，不含该串。"
},
{
  "slug": "hvac/pump-calculator",
  "inputs": {
    "q": "76",
    "L": "150",
    "d": "100",
    "lambda": "0.022",
    "kexi": "10",
    "dz": "8",
    "eta": "0.75",
    "margin": "12"
  },
  "expect": [
    "流速偏高，注意水力噪声与管路磨损",
    "2.69 管内流速 v (m/s)"
  ],
  "ref": "非默认输入（默认 50/120/100/0.025/12/10/0.70/10）：管内流速 v = Q÷(3600×πd²/4) = 76÷(3600×π×0.1²/4) = 76÷28.2743 = 2.6880 m/s ⇒ 卡片显示「2.69 管内流速 v (m/s)」；2.5 < v ≤ 3.0 落 velocityGrade 的「偏高」分支，tip「流速偏高，注意水力噪声与管路磨损」。默认态 v = 50÷28.2743 = 1.7684 ⇒ 显示 1.77、落「合理」分支（tip 不同），两串均不含。另算：速度头 v²/2g = 0.3683 m、沿程 hf = 0.022×(150/0.1)×0.3683 = 12.15 m、局部 hj = 10×0.3683 = 3.68 m、总损 15.84 m、扬程 H = (15.84+8)×1.12 = 26.70 m、轴功率 N = 1000×9.81×76×26.70÷(3600×1000×0.75) = 7.37 kW。注：原第二项锚截面积 0.00785，但默认管径同为 100mm ⇒ 默认态亦命中（零判别力），已换为随输入变化的流速串。"
},
{
  "slug": "hvac/supply-air",
  "inputs": {
    "coolLoad": "4800",
    "deltaT": "10",
    "roomVol": "200"
  },
  "expect": [
    "换气次数适宜（7.2 次/h）",
    "0.398"
  ],
  "ref": "非默认输入（默认 2500/8/120）：送风量 Ls = 4800÷(1.2×1005×10) = 0.398010 m³/s ⇒ 显示「0.398」；Lh = 1432.84 m³/h ⇒ 换气次数 n = 1432.84÷200 = 7.164 次/h（5–10 区间）⇒ 评价框文案「换气次数适宜（7.2 次/h），处于舒适空调推荐区间，气流组织良好。」；推荐送风口数 = ceil(1432.84÷500) = 3 个、单风口 478 m³/h。默认态为 7.8 次/h（同为「适宜」但数值不同）。"
},
{
  "slug": "hvac/air-filter",
  "inputs": {
    "airflow": "2003",
    "filtW": "592",
    "filtH": "592",
    "filtArea": ""
  },
  "expect": [
    "2003"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/chiller-efficiency",
  "inputs": {
    "capacityKw": "503",
    "capacityRt": "142.17",
    "powerKw": "90",
    "tIn": "12",
    "tOut": "7",
    "cop100": "5.6",
    "cop75": "6.3",
    "cop50": "6.8",
    "cop25": "6.0"
  },
  "expect": [
    "143.02"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/dehumidifier",
  "inputs": {
    "volume": "123",
    "temp": "26",
    "ach": "0.5",
    "rh1": "80",
    "rh2": "55"
  },
  "expect": [
    "61.5×1.168×5.39/1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/fan-selector",
  "inputs": {
    "Q": "10003",
    "dP": "800",
    "eta": "75",
    "etaMotor": "90",
    "n": "1450",
    "K": "1.15"
  },
  "expect": [
    "2222.89"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/fresh-air-load",
  "inputs": {
    "people": "23",
    "stdAir": "30",
    "indoorT": "26",
    "indoorRH": "55",
    "outdoorT": "34",
    "outdoorRH": "65"
  },
  "expect": [
    "690×1.2×1.01×8.00/3600"
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
  console.log("==== hvac calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
