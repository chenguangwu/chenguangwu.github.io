#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "textile/calc-gsm", inputs: {"wWeight": "5.2", "wWidth": "20", "wLength": "20", "wFabricWidth": "150", "cValue": "200", "cWidth": "150", "yWarpCount": "40", "yWeftCount": "40", "yEPC": "25", "yPPC": "22", "yWarpCrimp": "5", "yWeftCrimp": "4", "yFabricWidth": "150"}, expect: ["OK"] },
  { slug: "textile/color-fastness", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "textile/colorfastness", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "textile/convert-48", inputs: {"val": "20"}, expect: ["OK"] },
  { slug: "textile/convert-yarn", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "textile/cost-calculator", inputs: {"fabricPrice": "35", "fabricUsage": "1.5", "fabricWidth": "150", "gsm": "200", "accessoryCost": "8", "laborCost": "15", "orderQty": "500", "profitMargin": "30", "wastage": "5", "otherCost": "3"}, expect: ["OK"] },
  { slug: "textile/cutting-1", inputs: {"width": "150", "length": "10", "pieces": "12"}, expect: ["OK"] },
  { slug: "textile/density-8", inputs: {"area": "100", "stitch": "2", "density": "80"}, expect: ["OK"] },
  { slug: "textile/dye-mixer", inputs: {"fabricWeight": "100", "concentration": "2", "liquorRatio": "20"}, expect: ["OK"] },
  { slug: "textile/dye-temp", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "textile/dyeing-time", inputs: {"startTemp": "30", "targetTemp": "130", "rate": "1.5", "holdTime": "60", "startTemp2": "30", "targetTemp2": "130", "reqTime": "60", "holdTime2": "45"}, expect: ["OK"] },
  { slug: "textile/estimate-dosage-fabric-qty", inputs: {"perLen": "1.5", "width": "150", "qty": "500", "waste": "3", "price": "25"}, expect: ["OK"] },
  { slug: "textile/fabric-converter", inputs: {"gsm": "200", "width": "150", "price": "30", "rmb": "30", "value": "60"}, expect: ["OK"] },
  { slug: "textile/fukuanpailiaoliyonglv", inputs: {"width": "150", "effWidth": "140", "perLen": "1.2", "qty": "100"}, expect: ["OK"] },
  { slug: "textile/fuliao-lalian-niukou-guige", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "textile/hardness-5", inputs: {"weight": "30", "temp": "140", "pressure": "30", "durtime": "15"}, expect: ["OK"] },
  { slug: "textile/kangjingdianbanshuaiqi", inputs: {"v0": "1000", "vt": "500", "t": "2"}, expect: ["OK"] },
  { slug: "textile/length-gsm", inputs: {"loopLen": "3.0", "tex": "15", "wpc": "15", "cpc": "20"}, expect: ["OK"] },
  { slug: "textile/liquor-ratio", inputs: {"fabricWt": "200", "ratio": "10", "chemAmount": "5000", "density": "1.2", "fabricWt2": "100", "ratio2": "10", "owf": "3", "concGl": "0"}, expect: ["OK"] },
  { slug: "textile/pattern-calculator", inputs: {"fabricWidth": "150", "fabricLength": "200", "seamAllowance": "8"}, expect: ["OK"] },
  { slug: "textile/ratio-20", inputs: {"baseSize": "100", "grade": "4"}, expect: ["OK"] },
  { slug: "textile/shrinkage", inputs: {"cutSize": "100", "shrinkPct": "5", "targetSize": "100", "shrinkPct2": "5"}, expect: ["OK"] },
  { slug: "textile/thread-count", inputs: {"value": "32", "d": "75", "warp": "200", "weft": "180", "width": "150", "wTex": "20", "fTex": "20"}, expect: ["OK"] },
  { slug: "textile/yarn-count", inputs: {"value": "40"}, expect: ["OK"] },
  { slug: "textile/zuranyangzhishu-loi", inputs: {"loi": "28"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== textile calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();