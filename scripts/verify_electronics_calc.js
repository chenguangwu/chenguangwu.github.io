#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "electronics/analysis-22",
  "inputs": {
    "V": "6.7",
    "Ia": "25",
    "Is": "0.05",
    "duty": "5",
    "C": "2000"
  },
  "expect": [
    "0.00869"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/bandwidth",
  "inputs": {
    "gain": "15",
    "freq": "100000"
  },
  "expect": [
    "1.50e+6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/calc-63",
  "inputs": {
    "cur": "5",
    "oz": "1",
    "dt": "20"
  },
  "expect": [
    "1.816"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/calc-frequency",
  "inputs": {
    "l": "150",
    "freq": "1000"
  },
  "expect": [
    "0.9425"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/calc-time-2",
  "inputs": {
    "r": "15000",
    "c": "10"
  },
  "expect": [ "1.50e-1 时间常数" ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/capacitance",
  "inputs": {
    "cl": "24",
    "cs": "3"
  },
  "expect": [
    "推荐就近选取标准容值39pF"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/capacitor-calculator",
  "inputs": {
    "list": "100, 220, 470",
    "R": "15000",
    "C": "1000",
    "V": "5"
  },
  "expect": [
    "15000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/circuit-calculator",
  "inputs": {
    "L": "15",
    "C": "1",
    "R": "10",
    "val": "20",
    "f": "1000",
    "V": "5",
    "I": "2",
    "pf": "0.85"
  },
  "expect": [
    "1299.49"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/convert-capacitance",
  "inputs": {
    "code": "156"
  },
  "expect": [
    "0.015000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/crystal-divider",
  "inputs": {
    "xtal1": "24",
    "divider1": "8",
    "xtal2": "8",
    "multi": "9",
    "preDiv": "1",
    "outDiv": "2",
    "xtal3": "12",
    "target": "48"
  },
  "expect": [
    "晶振(24.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/current-pressure-drop",
  "inputs": {
    "im": "150",
    "temp": "25"
  },
  "expect": [
    "0.1156"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/dianyuanxiaolvldo-dcdc",
  "inputs": {
    "vin": "18",
    "vout": "5",
    "iout": "1",
    "eff": "90"
  },
  "expect": [
    "13.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/estimate-power-1",
  "inputs": {
    "vcc": "36",
    "rl": "8"
  },
  "expect": [
    "理论最大功率20.25W"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/frequency-11",
  "inputs": {
    "r": "15000",
    "c": "0.1",
    "l": "100"
  },
  "expect": [
    "×15000×1.00e-7)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/frequency-12",
  "inputs": {
    "r": "24000",
    "c": "0.01",
    "l": "100",
    "c1": "100",
    "c2": "100",
    "xf": "12"
  },
  "expect": [
    "663.146"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/frequency-13",
  "inputs": {
    "freq": "650",
    "len": "0.35"
  },
  "expect": [
    "理想0.115m"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/pcb-power",
  "inputs": {
    "power": "8",
    "area": "100",
    "ambient": "25",
    "coverage": "60"
  },
  "expect": ["8\n100\n2\n35\n25\n60\n26.2 °C\n温升 ΔT · 板温约 51.2 °C （环境 25°C）\n26.2 °C 温升 51.2 °C 板温 0.080 W/cm² 功率密度 35 W/m²·K 有效换热系数\n功率密度：0.080 W/cm² 功率密度中等，建议增加铺铜与通风孔。"],
  "ref": "auto-restore"
},
{
  "slug": "electronics/pcbzukangdieceng",
  "inputs": {
    "er": "7.4",
    "w": "0.2",
    "h": "0.1",
    "t": "0.035"
  },
  "expect": [
    "32.85"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/resistance-resistor",
  "inputs": {
    "bands": "5"
  },
  "expect": [
    "5色环"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/resistor-calculator",
  "inputs": {
    "list": "100, 200, 400",
    "vin": "18",
    "r1": "1000",
    "r2": "2000"
  },
  "expect": [ "最大值 400.00" ],
  "ref": "auto-restore"
},
{
  "slug": "electronics/smt-stencil",
  "inputs": {
    "padW": "3.5",
    "padL": "2.0",
    "reduce": "10",
    "pitch": "0.5",
    "transfer": "70"
  },
  "expect": [
    "3.150×1.800"
  ],
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

  console.log("==== electronics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
