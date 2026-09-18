#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "metallurgy/alloy-ratio",
  "inputs": {
    "steelW": "8",
    "initPct": "1"
  },
  "expect": [
    "3.046"
  ],
  "ref": "de-default: 8t/初始1%→总原料加入量 3.046 t（Cr 1.36/0.57 + Ni 0.64/0.9702；默认 5t/0% 为 2.043）"
},
{
  "slug": "metallurgy/calc-1",
  "inputs": {
    "totalMass": "2000",
    "targetMain": "92",
    "targetAdd": "8",
    "mainPurity": "99.5",
    "addPurity": "97",
    "addContent": "45"
  },
  "expect": [
    "89.264"
  ],
  "ref": "de-default: 2000kg/92+8/97%/45%→有效成分总占比 89.264%（默认 1000kg 组为 94.706%）"
},
{
  "slug": "metallurgy/calc-88",
  "inputs": {
    "tC": "2.2",
    "tSi": "3.5",
    "tMn": "1.5",
    "bC": "8",
    "bSi": "10",
    "bMn": "25"
  },
  "expect": [
    "偏差 +0.04%"
  ],
  "ref": "de-default: 目标2.2/3.5/1.5、烧损8/10/25→fC=2.2384 → C 偏差 +0.04%（默认组偏差为 −0.89/+1.23/+0.77）"
},
{
  "slug": "metallurgy/calc-temp-1",
  "inputs": {
    "v0": "200",
    "v1": "80"
  },
  "expect": [
    "473.15 K"
  ],
  "ref": "de-default: 通用模板落「温度」分支（h1 含温度）→A 开尔文 200+273.15=473.15 K（默认 100 → 373.15）"
},
{
  "slug": "metallurgy/convert-hardness",
  "inputs": {
    "val": "250",
    "rate": "2.5"
  },
  "expect": [
    "625.000000"
  ],
  "ref": "de-default: 250×2.5×1/1=625 → 结果 625.000000（默认 1×1×1/1=1.000000）"
},
{
  "slug": "metallurgy/decarburization",
  "inputs": {
    "temp": "1150",
    "time": "10",
    "ratio": "0.8"
  },
  "expect": [
    "脱碳较明显"
  ],
  "ref": "de-default: 1150°C/10h/ratio0.8 → xMm≈0.865 mm 落「脱碳较明显」档（默认 1100/2/0.5 → 0.158 属「轻微脱碳，一般可接受」）"
},
{
  "slug": "metallurgy/energy-1",
  "inputs": {
    "v0": "150",
    "v1": "40"
  },
  "expect": [
    "6.0000 kW"
  ],
  "ref": "de-default: 通用模板落「功率/能耗」分支（h1 含能耗）→A×B=6000 W=6.0000 kW（默认 100×50=5.0000 kW）"
},
{
  "slug": "metallurgy/estimate-temp-time-1",
  "inputs": {
    "v0": "250",
    "v1": "90"
  },
  "expect": [
    "523.15 K"
  ],
  "ref": "de-default: 通用模板落「温度」分支（首个命中，h1 含温度）→A 开尔文 250+273.15=523.15 K（默认 100 → 373.15）"
},
{
  "slug": "metallurgy/heat-treatment",
  "inputs": {
    "thickness": "80",
    "temp": "900",
    "heatRate": "120",
    "holdCoef": "2.0"
  },
  "expect": [
    "792 分钟"
  ],
  "ref": "de-default: 80mm/900°C/120°C·h/系数2.0/淬火 → 升温616+保温160+冷却16=792 分钟（默认组 603.75 → 604 分钟）"
},
{
  "slug": "metallurgy/power-6",
  "inputs": {
    "v0": "300",
    "v1": "25"
  },
  "expect": [
    "7.5000 kW"
  ],
  "ref": "de-default: 通用模板落「功率/能耗」分支（h1 含功率）→300×25=7500 W=7.5000 kW（默认 100×50=5.0000 kW）"
},
{
  "slug": "metallurgy/solidification-time",
  "inputs": {
    "dim1": "300",
    "dim2": "250",
    "dim3": "40",
    "kCoef": "3.0"
  },
  "expect": [
    "7.17"
  ],
  "ref": "de-default: 板件 300×250×40、K=3.0 → V=3000/A=1940/M=1.5464 → t=7.17 分钟（默认 200×200×30、K=2.0 → 2.66）"
},
{
  "slug": "metallurgy/steel-calc-1",
  "inputs": {
    "hf": "8",
    "lw": "200",
    "N": "50",
    "V": "20",
    "M": "2",
    "ffw": "200"
  },
  "expect": [
    "41.2%"
  ],
  "ref": "de-default: 角焊缝 he=5.6/A=1120，复合应力 82.46 → 应力比 41.2%（默认组 267.22/160=167.0%，验算「不满足」→「满足」；注意「满足」⊂「不满足」故锚应力比）"
},
{
  "slug": "metallurgy/steel-profile-weight",
  "inputs": {
    "type": "channel",
    "d1": "100",
    "d2": "50",
    "t": "8",
    "len": "12"
  },
  "expect": [
    "106.03 kg"
  ],
  "ref": "de-default: 槽钢 (100+50−16)×8×0.00785×1.05=8.836 kg/m × 12m = 106.03 kg（默认圆钢 20×6m=14.81 kg）"
},
{
  "slug": "metallurgy/analysis-34",
  "inputs": {
    "data": "2,4,6,8,10"
  },
  "expect": [
    "2.83"
  ],
  "ref": "de-default: 标准差 σ=√8=2.83（原 expect \"80_X\" 为 textarea.value 回显，calc 全坏亦通过；默认 10..80 组 σ=22.91）"
},
{
  "slug": "metallurgy/analysis-grade",
  "inputs": {
    "data": "5,15,25,35,45"
  },
  "expect": [
    "14.14"
  ],
  "ref": "de-default: 均值25、方差200 → σ=14.14（原 expect \"80_X\" 为 textarea.value 回显）"
},
{
  "slug": "metallurgy/analysis-heatmap",
  "inputs": {
    "data": "100,200,300"
  },
  "expect": [
    "81.65"
  ],
  "ref": "de-default: 均值200、方差6666.67 → σ=81.65（原 expect \"80_X\" 为 textarea.value 回显）"
},
{
  "slug": "metallurgy/analysis-price-1",
  "inputs": {
    "data": "11,22,33,44"
  },
  "expect": [
    "151.25"
  ],
  "ref": "de-default: 均值27.50、方差151.25（原 expect \"80_X\" 为 textarea.value 回显）"
},
{
  "slug": "metallurgy/stats-10",
  "inputs": {
    "data": "50,60,70,80,90,100"
  },
  "expect": [
    "291.67"
  ],
  "ref": "de-default: 均值75、方差1750/6=291.67（原 expect \"80_X\" 为 textarea.value 回显）"
},
{
  "slug": "metallurgy/calc-time-solid",
  "inputs": {
    "C": "0.15"
  },
  "expect": [
    "0.94"
  ],
  "ref": "de-default: C=0.15 → 最长凝固 0.15×2.5²=0.9375 → 0.94 min（默认 C=0.094 → 0.59；截面为动态无 id 行不可注入，故锚 C 驱动的计算值）"
},
{
  "slug": "metallurgy/hardness-conversion",
  "inputs": {
    "inVal": "100"
  },
  "expect": [
    "- 布氏 HBW"
  ],
  "ref": "de-default: inVal 超首轴值(68) → hb 插值返回空 → 卡片显示「- 布氏 HBW」（默认 45 → 68.0/760/940/2820）。注：本页 interp 的 xs 递减而实现假设递增，任意范围内输入恒取首行 68/760/940，结果与输入无关（已登记 DEV-PLAN §10.6）；refTable 静态表（有 id，进 blob）恒含 2820，故不可锚 σb"
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
  console.log("==== metallurgy calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
