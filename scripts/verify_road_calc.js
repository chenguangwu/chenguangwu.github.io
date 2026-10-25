#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "road/convert-angle-slope",
  "inputs": {
    "val": "15"
  },
  "expect": [
    "15.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/curve-calc",
  "inputs": {
    "inE": "9",
    "inF": "0.15",
    "inAlpha": "60",
    "inB": "7.5",
    "inP": "125"
  },
  "expect": [
    "/(127×0.240)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/grade-calc",
  "inputs": {
    "inH1": "150",
    "inH2": "108",
    "inL": "200",
    "inBc": "7.5",
    "inHc": "15"
  },
  "expect": [
    "150.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/pavement-design",
  "inputs": {
    "inW18": "750",
    "inMR": "35",
    "inD1": "15"
  },
  "expect": ["750\n95\n0.45\n35\n4.2\n2.5\n15\n0.44\n0.14\n0.11\n5.70\n81 cm\n23 cm\n43 cm\n面层 15cm SN 2.60 基层 23cm SN 1.27 底基层 43cm SN 1.86\n输入轴载： 750 万次 (W18=7,500,000) 可靠度： 95% (ZR=-1.645)，S0=0.45 路基模量： 35 MPa = 5076 psi 服务能力损失： ΔPSI = 4.2 − 2.5 = 1.7 所需结构数： SN = 5.694 → 取 5.70 各层分配： 面层：15 cm，a1=0.44，SN₁=2.60 基层：23 cm，a2=0.14，SN₂=1.27 底基层：43 cm，a3=0.11，SN₃=1.86 实际结构数： SN = 5.73 满足要求 路面总厚度： 81 cm"],
  "ref": "auto-restore"
},
{
  "slug": "road/sight-distance",
  "inputs": {
    "inT": "5.5",
    "inF": "0.33",
    "inG": "0",
    "inV1": "50",
    "inV2": "65",
    "inV3": "60",
    "inT1": "3.6",
    "inT2": "9.0",
    "inTd": "3.0",
    "inAd": "3.4"
  },
  "expect": [
    "5.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/traffic-capacity",
  "inputs": {
    "inPT": "23",
    "inFlow": "2000"
  },
  "expect": ["23\n2000\nfreeway\n2\n100\n3.5\n1.5\n2.0\n1.0\n4400 pcu/h\n3470 pcu/h\n2429 pcu/h\n0.576\n服务水平 LOS C — 稳定流 (V/C=0.576)\n道路类型： 高速/一级 基本通行能力： C₀ = 2200 pcu/h/ln × 2车道 = 4400 pcu/h 车道宽修正： f_w = 0.97(车道) × 1.00(侧向) = 0.970 大型车修正： f_HV = 1/[1+23%×(2−1)] = 0.813 驾驶员修正： f_p = 1 可能通行能力： C = 4400×0.970×0.813×1 = 3470 pcu/h 设计通行能力： 2429 pcu/h (C级，V/C=0.7) 实际流量： 2000 pcu/h 饱和度 V/C： 0.576 → LOS C (稳定流) 校核： 满足设计要求 基本通行能力 4400 可能通行能力 3470 实际流量 2000 设计通行能力 2429"],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== road calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
