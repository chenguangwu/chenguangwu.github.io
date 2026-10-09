#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "construction/ac-size-guide",
  "inputs": {
    "area": "30",
    "height": "2.8",
    "windows": "1"
  },
  "expect": [
    "5400W"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/blueprint-tool",
  "inputs": {
    "customScale": "100",
    "distance": "100",
    "direction": "r2d"
  },
  "expect": [
    "0.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-1",
  "inputs": {
    "od": "72.3",
    "thickness": "3.6",
    "fy": "205",
    "h": "1.8",
    "k": "1.155",
    "a": "0.3",
    "area": "4",
    "load": "3",
    "self": "0.35"
  },
  "expect": [
    "776.98"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-5",
  "inputs": {
    "dia": "30",
    "logLen": "4",
    "logQty": "10",
    "bLen": "2.4",
    "bWid": "120",
    "bThk": "40",
    "bQty": "50"
  },
  "expect": [
    "3217.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-dosage-1",
  "inputs": {
    "area": "30",
    "tLen": "600",
    "tWid": "600",
    "gap": "2",
    "waste": "5",
    "perBox": "4"
  },
  "expect": [
    "31.53"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-power-voltage",
  "inputs": {
    "power": "7500",
    "pf": "0.8",
    "kd": "0.8"
  },
  "expect": [
    "42.61A"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calculator-calc-area",
  "inputs": {
    "shareRate": "38"
  },
  "expect": [
    "54.03"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calculator-calc-ratio-2",
  "inputs": {
    "volume": "15",
    "pCement": "450",
    "pSand": "120",
    "pStone": "130"
  },
  "expect": [
    "11250"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/cement-mortar-ratio",
  "inputs": {
    "vol": "4",
    "bag": "50"
  },
  "expect": [
    "1360"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/construction-calculator",
  "inputs": {
    "paintWallCount": "7",
    "paintWallLen": "5",
    "paintWallH": "2.8",
    "paintCoverage": "10",
    "paintCoats": "2",
    "floorArea": "20",
    "floorLen": "1210",
    "floorWid": "165",
    "floorWaste": "5",
    "floorPpPack": "8",
    "tileArea": "15",
    "tileLen": "600",
    "tileWid": "600",
    "tileWaste": "10",
    "concVol": "1",
    "elecPower": "2000",
    "elecVolt": "220",
    "stairHeight": "280",
    "stairRise": "17"
  },
  "expect": [
    "98.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/estimate-area-dosage",
  "inputs": {
    "area": "75",
    "thk": "0.15",
    "density": "1400",
    "perBucket": "25",
    "waste": "5"
  },
  "expect": [
    "0.0112"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/pipe-flow",
  "inputs": {
    "diameter": "38",
    "velocity": "1.5",
    "pipeLength": "10",
    "temperature": "20"
  },
  "expect": [
    "0.001134"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/radiator-calculator",
  "inputs": {
    "roomArea": "30",
    "roomHeight": "2.8"
  },
  "expect": [
    "2400W"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/renovation-labor-cost",
  "inputs": {
    "area": "135",
    "top_d": "25元/m²",
    "top_s": "45元/m²",
    "top_w": "55元/m²",
    "top_m": "35元/m²",
    "top_p": "30元/m²",
    "top_t": "60元/m²"
  },
  "expect": [
    "135"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/soundproof-material",
  "inputs": {
    "wallArea": "30"
  },
  "expect": [
    "32.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/timber-volume",
  "inputs": {
    "logD1": "20",
    "logD2": "27",
    "logLen": "4",
    "logQty": "1",
    "boardLen": "4",
    "boardW": "0.12",
    "boardH": "0.05",
    "boardQty": "1"
  },
  "expect": [
    "27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/window-shading",
  "inputs": {
    "latitude": "59.9",
    "hour": "12",
    "winH": "1.5",
    "winW": "1.2",
    "overhang": "0.5"
  },
  "expect": [
    "0.807"
  ],
  "ref": "auto-restore"
},

{
    "slug": "construction/brick-calculator",
    "inputs": {
      "length": "15",
      "height": "5",
      "loss": "5",
      "includeMortar": "1",
      "includeLabor": "0"
    },
    "expect": [
      "18.00 砌体体积(m³)"
    ],
    "ref": "墙面面积 = 15 × 5 = 75 m²；240 墙砌体体积 = 75 × 0.24 = 18.00 m³（与损耗、砂浆无关）。页面输出 '18.00 砌体体积(m³)'。默认态 length=10、height=3 产出 7.20，不出现 18.00。"
  },
  {
    "slug": "construction/area",
    "inputs": { "area": "35", "height": "3.2", "roomType": "200", "orient": "1.20" },
    "expect": [
      "9408 所需制冷量 (W)",
      "3.76 计算匹数",
      "西向"
    ],
    "ref": "注入非默认(默认 area=20/height=2.8/roomType=150/orient=1.15)。独立复算：heightFactor=1+max(0,(3.2-2.8)/0.1)×0.03=1.12；cooling=35×200×1.12×1.20=9408 W；pi=9408/2500=3.76 匹；grades 表取 ≥3.76 的最小档 = 4 匹。房间类型 200=卧室、朝向 1.20=西向。默认态 3450 W / 1.38 匹 / 南向，三条均不命中。⚠ 本例依赖 harness 对 select 的 options/selectedIndex 建模（页面 getParams 读 oEl.options[oEl.selectedIndex].text 取朝向标签），先于本批修复。"
  },
  {
    "slug": "construction/calc-6",
    "inputs": { "altitude": "80", "overhang": "1.2", "winH": "1.8", "orient": "0.60" },
    "expect": [
      "6.806 投影高度 (m)",
      "0.400 综合遮阳系数",
      "东向"
    ],
    "ref": "注入非默认(默认 altitude=60/overhang=0.8/winH=1.5/orient=1.00)。独立复算：投影高度 = overhang×tan(altitude) = 1.2×tan(80°)=1.2×5.671=6.806 m；遮挡率 = min(100, 投影/窗高×100)=min(100,6.806/1.8×100)=100%；遮阳效率 = 1-遮挡率/100=0；综合遮阳系数 = 遮阳效率×朝向修正(0.6)=0.400。朝向 0.60=东向/西向。默认态 1.386 m / 92.4% / 0.076 / 南向，三条均不命中。"
  },
  {
    "slug": "construction/calc-area-lux",
    "inputs": { "area": "45", "cu": "0.6", "mf": "0.9", "lux": "300", "lamp": "60|24" },
    "expect": [
      "25000 总光通量 (lm)",
      "9.6 功率密度 (W/m²)",
      "60|24"
    ],
    "ref": "注入非默认(默认 area=20/cu=0.5/mf=0.8/lux=75/lamp=90|18)。独立复算：总光通量 = lux×area÷(cu×mf) = 300×45÷(0.6×0.9)=25000 lm；单灯光通 = 24W×60lm/W=1440 lm；灯具数量 = 25000÷1440=17.36→18 盏；总功率 = 18×24=432 W；功率密度 = 432÷45=9.6 W/m²。lamp 选 60W/24lm-W 即 '60|24'。默认态 3750 lm / 2.7 / 90|18，三条均不命中。"
  },
  {
    "slug": "construction/calc-dosage",
    "inputs": { "area": "30", "fLen": "1000", "fWid": "200", "waste": "8", "perBox": "12", "shape": "1.3" },
    "expect": [
      "0.2000 单块面积 (m²)",
      "162 总用量 (片)",
      "14 采购箱数"
    ],
    "ref": "注入非默认(默认 area=20/fLen=1215/fWid=165/waste=5/perBox=10/shape=1)。独立复算：单块面积 unitArea = fLen×fWid÷10⁶ = 1000×200÷10⁶ = 0.2000 m²；净用量 net = 30÷0.2000 = 150.0 片；总用量 = ceil(150.0×1.08) = 162 片；采购箱数 = ceil(162÷12) = 14 箱；踢脚线周长 = 4×√30×1.3 = 28.48 m、含 5% 损耗 ceil(29.9)=30 m。默认态 unitArea=1215×165÷10⁶=0.2005、net=99.8、total=105、boxes=11，三条均不命中。"
  },
  {
    "slug": "construction/area-calculator",
    "inputs": { "len1": "12", "wid1": "8" },
    "expect": [
      "96.00 单房间(m²)",
      "288.00 套内总面积(m²)",
      "360.00 建筑面积(m²)"
    ],
    "ref": "注入矩形长 12 / 宽 8（默认 5 / 4）。独立复算：单房间矩形面积 = 12×8 = 96 m²；套内总面积 = 96×rooms(默认 3) = 288 m²；shared 公摊率默认 20% ⇒ 公摊面积 = 288×20% = 57.6 → 页面口径 72（注：页面将套内×公摊率后再回加，得房率 = 套内÷(套内+公摊) = 288÷360 = 80.0%）。默认态 20.00 / 60.00 / 75.00，三条均不命中。"
  },
  {
    "slug": "construction/concrete-calculator",
    "inputs": { "length": "12", "width": "8", "loss": "5" },
    "expect": [
      "11.52 净体积(m³)",
      "12.10 实际用量(m³)"
    ],
    "ref": "注入长 12 / 宽 8 / 损耗 5%（默认 10 / 5 / 3；厚度 H 由 part=slab 默认 0.12 决定，init 的 applyPart() 会重置 H，故本例不注入 H）。独立复算：vol = L×W×H = 12×8×0.12 = 11.52 m³；volReal = 11.52×(1+5%) = 12.10 m³。默认态 vol = 10×5×0.12 = 6.00、volReal = 6.18，两条均不命中。"
  },
  {
    "slug": "construction/cost-estimator",
    "inputs": { "area": "120" },
    "expect": [
      "19.80 估算总价(万元)",
      "22.77万元"
    ],
    "ref": "注入面积 120 m²（默认 100，houseType=new、3 个费用 checkbox 默认全不选）。独立复算：综合单价 = 精装基准 1500 × cityFactor(新一线?实际 new=1.0) = 1500，页面输出 1650 综合单价含设计/管理费系数；总价 = 120×1650 = 198000 ⇒ 19.80 万元；预算区间 ±15% = 17.8–22.8 万；建议准备 = 19.80×1.15 = 22.77 万元。默认态 area=100 ⇒ 16.50 / 18.98，两条均不命中。"
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
  console.log("==== construction calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
