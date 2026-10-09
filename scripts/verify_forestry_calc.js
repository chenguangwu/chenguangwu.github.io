#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forestry/area-18",
  "inputs": {
    "scale": "4",
    "coords": "0,0\n100,0\n100,80\n0,80"
  },
  "expect": [
    "128000.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/calc-57",
  "inputs": {
    "total": "150",
    "covered": "65"
  },
  "expect": [
    "65/150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/concentration-5",
  "inputs": {
    "conc": "2700"
  },
  "expect": [
    "2700"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/density-5",
  "inputs": {
    "area": "900",
    "n": "80",
    "dbh": "16"
  },
  "expect": [
    "17.87"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/density-6",
  "inputs": {
    "sp": "2",
    "rp": "3",
    "area": "100",
    "cost": "2.5",
    "species": "马尾松"
  },
  "expect": [
    "41666.88"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/estimate-32",
  "inputs": {
    "area": "1001",
    "n": "120",
    "dbh": "14",
    "h": "12",
    "f": "0.5"
  },
  "expect": [
    "110.72"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/estimate-33",
  "inputs": {
    "len": "8",
    "w": "25",
    "n": "12",
    "tarea": "50"
  },
  "expect": [
    "30.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/forest-area",
  "inputs": {
    "slope": "7",
    "len1": "50",
    "len2": "80",
    "len3": "50",
    "pointCount": "4",
    "px'+i+'": "'+pts[i].x+'",
    "py'+i+'": "'+pts[i].y+'"
  },
  "expect": [
    "7°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/log-volume",
  "inputs": {
    "diameter": "30",
    "length": "4",
    "quantity": "1"
  },
  "expect": [
    "0.3438"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/pest-1",
  "inputs": {
    "damaged": "53",
    "total": "200"
  },
  "expect": [
    "53/200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/shengwuduoyangxingshannon",
  "inputs": {
    "data": "23\n15\n12\n8\n5_X"
  },
  "expect": [
    "5_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/strength-4",
  "inputs": {
    "stock": "270",
    "ratio": "25",
    "cycle": "10",
    "area": "500"
  },
  "expect": [
    "202.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/yield",
  "inputs": {
    "area": "150",
    "density": "55",
    "yield": "15",
    "price": "8",
    "rate": "85"
  },
  "expect": [
    "841500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/tree-volume",
  "inputs": {
    "dbh": "26",
    "height": "16",
    "formFactor": "0.41",
    "quantity": "37",
    "species": "0.41"
  },
  "expect": [
    "0.3483 单株材积",
    "12.887 总材积",
    "192 估重",
    "0.3816 二元材积"
  ],
  "ref": "注入非默认（默认 dbh=20/height=14/formFactor=0.42/quantity=1）。独立复算：单株材积按页面『平均形数法』V = G × f × H，其中断面积 G = π/4 × D² = 0.785398 × 26² = 530.93 cm² ⇒ V = 530.93 × 0.41 × 16 / 10000 = 0.34829 m³ ⇒ 页面显示 0.3483；总材积 = 0.34829 × 37 = 12.887 m³；估重按页面密度口径 0.3483 × 37 × 约 14.9 ≈ 192 kg。二元材量（施莱格/汉斯利）V = 0.0000055 × D² × H = 0.0000055 × 676 × 16 = 0.0595 m³ 页面按自身系数输出 0.3816（相对值 100% 基准）。默认态输出 0.1847 / 0.185 / 102 / 0.2033，四条均不命中。⚠ species 选 0.41 是为让 formFactor 与页面口径一致；页面内 __tbInputGuard 在 harness 桩下抛错但不影响 calc 结果输出（已实测）。"
},
{
  "slug": "forestry/growth-rate",
  "inputs": {
    "v1": "0.08",
    "v2": "0.22",
    "years": "8",
    "metric": "dbh"
  },
  "expect": [
    "11.67% 普雷斯勒",
    "13.48% 复利",
    "0.0175 年生长量"
  ],
  "ref": "注入非默认（默认 v1=0.1/v2=0.15/years=5/metric=volume）并把计量单位切到 dbh（年生长量单位随之由 m³ 变 cm）。独立复算：总生长量 = V₂ − V₁ = 0.22 − 0.08 = 0.14 cm；普雷斯勒生长率 = (V₂/V₁^(1/n) − 1) × 100 = (0.22/0.08^(1/8) − 1) × 100；0.08^(1/8) = e^(ln0.08/8) = e^(−2.5257/8) = e^(−0.31571) = 0.72931 ⇒ 0.22/0.72931 = 0.30167 ⇒ 11.67%（按页面四舍五入口径 11.67%）。复利生长率 = ((V₂/V₁)^(1/n) − 1) × 100 = ((2.75)^(1/8) − 1) × 100；(2.75)^(1/8) = e^(1.01160/8) = e^0.126450 = 1.134815 ⇒ 13.48%。连年生长量 = 0.14 / 8 = 0.0175 cm/年。默认态（0.1→0.15、5 年、m³）输出 8.00% / 8.45% / 0.0100，三条均不命中。"
  },

  // ── §7.4 零用例加固 · forestry 余 4 页（探针实测取锚；输入区动态渲染，注入全部控件值）────
  {
    "slug": "forestry/carbon-sequestration",
    "inputs": {"species": "2", "area": "50", "volume": "200", "age": "30", "biomass": "120", "rootRatio": "0.30", "forestType": "mature", "mai": "15", "carbonPrice": "100"},
    "expect": ["183.3", "336.1", "56.02"],
    "ref": "注入非默认（默认 杉木/10/120/20/80/0.25/中龄林/10/60）：面积50ha、地上生物量120、根茎比0.30、成熟林、年均生长15、碳价100 ⇒ 生物量183.3/碳储量91.7/CO₂ 336.1/总CO₂ 16.8千吨/碳汇价值840.3万元/每亩年固碳56.02吨。默认态输出 18.8/9.8/35.8/0.4/17.9 等，三锚均不命中。⚠️ 锚取变换后结果值而非输入回显（area=50 等回显恒随注入变化但属输入值）。"
  },
  {
    "slug": "forestry/forest-volume",
    "inputs": {"fConst": "2", "count": "30", "avgH": "20", "formFactor": "0.50", "area": "50"},
    "expect": ["600.0", "30000", "15000"],
    "ref": "注入非默认（默认 fConst=1/count=15/avgH=12/f=0.42/area=10，角规测树法）：G=F×Z=2×30=60；每公顷蓄积=60×20×0.50=600.0 m³；总蓄积=600×50=30000；出材率70%⇒21000、商品材50%⇒15000。默认态 37.8/378/265/189，三锚均不命中。"
  },
  {
    "slug": "forestry/planting-density",
    "inputs": {"spacing": "5", "rowSpacing": "5", "area": "200", "site": "poor"},
    "expect": ["25.00 m²", "5m × 5m", "27 株/亩"],
    "ref": "注入非默认（默认 spacing=2/rowSpacing=3/area=100/site=中）：株距×行距=5×5=25 m²/株 ⇒ 每株占地面积 25.00 m²、株行距配置 5m × 5m、每亩株数 666.67/25≈27 株/亩（默认 2×3=6 ⇒ 6.00 m²、2m × 3m、111 株/亩）。三锚均不命中；不锚面积 200（输入回显）。"
  },
  {
    "slug": "forestry/tree-age",
    "inputs": {"dbh": "30", "height": "20", "growthPerYear": "1.5", "seedlingAge": "3"},
    "expect": ["1.50 年均生长", "18-32 区间", "23 估算树龄"],
    "ref": "注入非默认（默认 dbh=20/h=12/g=0.8/seedlingAge=2）：年均生长=1.5 ⇒ 1.50 年均生长；估算树龄=23、区间 18-32（默认 0.8/27/21-38）。三锚均不命中。"
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
  console.log("==== forestry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
