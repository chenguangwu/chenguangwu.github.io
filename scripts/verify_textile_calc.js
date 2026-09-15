#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "textile/calc-gsm",
  "inputs": {
    "wWeight": "8.2",
    "wWidth": "20",
    "wLength": "20",
    "wFabricWidth": "150",
    "cValue": "200",
    "cWidth": "150",
    "yWarpCount": "40",
    "yWeftCount": "40",
    "yEPC": "25",
    "yPPC": "22",
    "yWarpCrimp": "5",
    "yWeftCrimp": "4",
    "yFabricWidth": "150"
  },
  "expect": [
    "30750.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/color-fastness",
  "inputs": {
    "fastType": "rub"
  },
  "expect": [
    "4(干)/3(湿)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/colorfastness",
  "inputs": {
    "origColor": "#1e88e5_X",
    "testColor": "#90caf9"
  },
  "expect": [
    "1e88e5_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/convert-48",
  "inputs": {
    "val": "30"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/convert-yarn",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/cost-calculator",
  "inputs": {
    "fabricPrice": "53",
    "fabricUsage": "1.5",
    "fabricWidth": "150",
    "gsm": "200",
    "accessoryCost": "8",
    "laborCost": "15",
    "orderQty": "500",
    "profitMargin": "30",
    "wastage": "5",
    "otherCost": "3"
  },
  "expect": [
    "156.39"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/cutting-1",
  "inputs": {
    "width": "225",
    "length": "10",
    "pieces": "12"
  },
  "expect": [
    "53.33%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/density-8",
  "inputs": {
    "area": "150",
    "stitch": "2",
    "density": "80"
  },
  "expect": [
    "12000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/dye-mixer",
  "inputs": {
    "fabricWeight": "150",
    "concentration": "2",
    "liquorRatio": "20"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/dye-temp",
  "inputs": {
    "dyeType": "vat"
  },
  "expect": [
    "升温至50-60°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/dyeing-time",
  "inputs": {
    "startTemp": "30",
    "targetTemp": "195",
    "rate": "1.5",
    "holdTime": "60",
    "startTemp2": "30",
    "targetTemp2": "130",
    "reqTime": "60",
    "holdTime2": "45"
  },
  "expect": [
    "195"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/estimate-dosage-fabric-qty",
  "inputs": {
    "perLen": "4.5",
    "width": "150",
    "qty": "500",
    "waste": "3",
    "price": "25"
  },
  "expect": [
    "57937.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/fabric-converter",
  "inputs": {
    "gsm": "300",
    "width": "150",
    "price": "30",
    "rmb": "30",
    "value": "60"
  },
  "expect": [
    "450.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/fukuanpailiaoliyonglv",
  "inputs": {
    "width": "225",
    "effWidth": "140",
    "perLen": "1.2",
    "qty": "100"
  },
  "expect": [
    "270.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/fuliao-lalian-niukou-guige",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "7500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/hardness-5",
  "inputs": {
    "weight": "45",
    "temp": "140",
    "pressure": "30",
    "durtime": "15"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/kangjingdianbanshuaiqi",
  "inputs": {
    "v0": "1500",
    "vt": "500",
    "t": "2"
  },
  "expect": [
    "1.262"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/length-gsm",
  "inputs": {
    "loopLen": "6",
    "tex": "15",
    "wpc": "15",
    "cpc": "20"
  },
  "expect": [
    "270.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/liquor-ratio",
  "inputs": {
    "fabricWt": "300",
    "ratio": "10",
    "chemAmount": "5000",
    "density": "1.2",
    "fabricWt2": "100",
    "ratio2": "10",
    "owf": "3",
    "concGl": "0"
  },
  "expect": [
    "300"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/pattern-calculator",
  "inputs": {
    "fabricWidth": "225",
    "fabricLength": "200",
    "seamAllowance": "8"
  },
  "expect": [
    "20.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/ratio-20",
  "inputs": {
    "partName": "胸围",
    "baseSize": "150",
    "grade": "4"
  },
  "expect": [
    "142.0cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/shrinkage",
  "inputs": {
    "cutSize": "150",
    "shrinkPct": "5",
    "targetSize": "100",
    "shrinkPct2": "5"
  },
  "expect": [
    "142.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/thread-count",
  "inputs": {
    "value": "48",
    "d": "75",
    "warp": "200",
    "weft": "180",
    "width": "150",
    "wTex": "20",
    "fTex": "20"
  },
  "expect": [
    "12.30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/yarn-count",
  "inputs": {
    "value": "60"
  },
  "expect": [
    "16.6667"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/zuranyangzhishu-loi",
  "inputs": {
    "loi": "42"
  },
  "expect": [
    "42.0%"
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
  console.log("==== textile calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
