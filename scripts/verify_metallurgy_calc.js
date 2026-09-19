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
    "data": "0.62,0.64,0.61,0.65,0.63,0.60",
    "cert": "0.63",
    "blank": "0.63",
    "spadd": "0.30",
    "spfound": "0.92",
    "rsdlim": "3",
    "relim": "2"
  },
  "expect": [
    "96.67",
    "-0.79"
  ],
  "ref": "化验质量统计：mean=0.6250%；RE=(0.625−0.63)÷0.63=−0.79%（依赖 cert），加标回收率=(0.92−0.63)÷0.30=96.67%（依赖 blank/spadd/spfound）。两项均依赖数值输入框，回退默认时分别为 +25.00% 与 95.00%，必不命中。注：RSD 只依赖 textarea，而该输入在回退模拟中不参与替换，按其设 expect 会被判逃生项，故不采用"
},
{
  "slug": "metallurgy/analysis-grade",
  "inputs": {
    "qOre": "2400",
    "gradeOre": "1.20",
    "gradeConc": "26",
    "gradeTail": "0.12"
  },
  "expect": [
    "4.17",
    "90.42",
    "21.67"
  ],
  "ref": "二产品平衡：Q=2400t、α=1.20%、β=26%、θ=0.12% → γ=(1.20−0.12)/(26−0.12)=4.17%、ε=γ·β/α=90.42%、富集比=26/1.20=21.67（独立复算，非页面默认 1000/0.85/22/0.09）"
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
    "charge": "150",
    "billet": "138",
    "product": "130.5"
  },
  "expect": [
    "92.00",
    "94.57",
    "19.50"
  ],
  "ref": "金属收得与成材：收得率=138/150=92.00%，成材率=130.5/138=94.57%，金属总损耗=150−130.5=19.50 t（独立复算，非页面默认值）"
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
    "inType": "hv",
    "inVal": "300"
  },
  "expect": [
    "29.8 洛氏 HRC",
    "≈ 900 MPa"
  ],
  "ref": "de-default: 非默认 inType=hv（默认 hrc）+ inVal=300（默认 45）。Python 独立复算（DATA 按输入列升序重排后插值）：HV 300 落在 284(HRC28)~302(HRC30) 之间，t=16/18=0.8889 → HRC=28+0.8889×2=29.78→29.8、HBW=280+0.8889×15=293→293、HV=300、σb=300×3.0=900 MPa。默认态输出 45.0/429/446/1338，两条 expect 均不命中。**缺陷 E 已修**：buildAxis 现按输入列升序重排；此前 DATA 四列全递减而 interp 假定 xs 递增，任意输入恒取首行（HRC45 与 60 输出完全相同）。refTable 静态表（有 id，进 blob）恒含 300/2820，故不可单独锚数字，须带「洛氏 HRC」「MPa」上下文"
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
