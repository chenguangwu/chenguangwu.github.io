#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "53",
    "sgVal": "0.85"
  },
  "expect": [
    "766.1707"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "-130",
    "sgVal": "0.85"
  },
  "expect": [
    "超出原油常见范围"
  ],
  "ref": "修复前 API=-130 输出密度 94.24 g/cm³ 且标「超重质」无警示；现保留计算但给出范围提示"
},
{
  "slug": "petrochem/catalyst-calc",
  "inputs": {
    "flow": "7500",
    "lsv": "2",
    "density": "850",
    "bulkDensity": "700",
    "flow2": "5000",
    "residence": "30",
    "density2": "850",
    "bulkDensity2": "700"
  },
  "expect": [
    "088.24"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/distillation-yield",
  "inputs": {
    "feed": "1500",
    "prodCount": "4",
    "prod${i}": "${name}",
    "amt${i}": "${amt}"
  },
  "expect": [ "1,500 损失/残液" ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/pipe-pressure",
  "inputs": {
    "flow": "75",
    "diameter": "100",
    "length": "500",
    "density": "850",
    "viscosity": "5",
    "roughness": "0.045"
  },
  "expect": [
    "093.9005"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/tank-capacity",
  "inputs": {
    "diameter": "15",
    "length": "12",
    "density": "850",
    "level": "8",
    "safety": "90"
  },
  "expect": [
    "120.58"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/catalyst-calc",
  "inputs": {
    "flow": "5000",
    "lsv": "2",
    "density": "850",
    "bulkDensity": "0"
  },
  "expect": [
    "请输入正的流量、空速、进料密度与催化剂堆积密度"
  ],
  "ref": "修复前堆积密度清空/0 直接按 0 得装量 0 kg（负堆密度还得负质量）；现与流量/空速/进料密度一并校验并提示补全。默认 700 不出现该文案。"
},
{
  "slug": "petrochem/catalyst-calc",
  "clicks": [
    "switchMode('time');document.getElementById('__tbProbe').textContent='CATSW='+(String(document.getElementById('resultTime').innerHTML).indexOf('催化剂体积')>=0?'Y':'N');"
  ],
  "expect": [
    "CATSW=Y"
  ],
  "ref": "修复前切到停留时间模式只切面板、未改输入前 resultTime 为空；现 switchMode 立即调用 calcTime()，默认 5000 kg/h、30 s、850 kg/m³、700 kg/m³ ⇒ 体积流量 5.88 m³/h、装量 0.049 m³ / 34.31 kg。默认态无该探针串。"
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

  console.log("==== petrochem calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
