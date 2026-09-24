#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "archaeology/artifact-measurement",
  "inputs": {
    "len": "20",
    "wid": "10",
    "thk": "4",
    "mass": "800",
    "rim": "12",
    "base": "6"
  },
  "expect": [
    "800.0 近似体积 cm³",
    "0.40 厚宽比 T/W",
    "2.00 口底比"
  ],
  "ref": "非默认输入（默认 12.0/8.0/3.0/240/9.0/5.0）：近似体积 = 20×10×4 = 800.0 cm³；密度 = 800÷800 = 1.00 g/cm³；长宽比 = 20÷10 = 2.00；厚宽比 = 4÷10 = 0.40；口底比 = 12÷6 = 2.00。默认态为 288.0 / 0.83 / 1.50 / 0.38 / 1.80（三串均不含）。注：材质 select、编号/名称文本框与密度参考行只回显静态值 ⇒ 不锚。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": {
    "len": "100",
    "wid": "60",
    "side": "10",
    "gap": "2"
  },
  "expect": [
    "60 探方总数",
    "2260.0 隔梁面积 m²"
  ],
  "ref": "非默认输入（默认 60/40/5/1）：nL = ceil(100÷10) = 10、nW = ceil(60÷10) = 6 ⇒ 探方总数 = 60；发掘面积 = 60×10² = 6000.0 m²；布方占地 = (10×10+9×2) × (6×10+5×2) = 118×70 = 8260.0 m² ⇒ 隔梁面积 = 8260 − 6000 = 2260.0 m²。默认态为 96 探方 / 2400.0 发掘 / 3337.0 占地 / 937.0 隔梁（两串均不含）。**注意**：越界提示「部分探方超出遗址范围，请核对尺寸」看似专属、实为零判别力 —— 默认态 nL=12 ⇒ siteLen = 12×5+11×1 = 71 > 遗址长 60 ⇒ 默认同样越界、同样命中该分支（首版曾误锚此串，默认态 via=calc 逃逸，已剔除）。"
},
{
  "slug": "archaeology/dating-method",
  "inputs": {
    "grpFilter": "radiocarbon"
  },
  "expect": [
    "radiocarbon"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/pottery-typology",
  "inputs": {
    "stageFilter": "early"
  },
  "expect": [
    "early"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/stats-density",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/stratum-identify",
  "inputs": {
    "ageFilter": "geo"
  },
  "expect": [
    "geo"
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
  console.log("==== archaeology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
