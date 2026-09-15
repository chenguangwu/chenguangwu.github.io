#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "fire-rescue/calc-pressure-1",
  "inputs": {
    "len": "30",
    "flow": "6.5"
  },
  "expect": [
    "0.0642"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/calc-time-response",
  "inputs": {
    "rti": "75",
    "tg": "300",
    "u": "2.0",
    "ti": "20",
    "tact": "68"
  },
  "expect": [
    "53.03"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/chemical-spill",
  "inputs": {
    "amount": "150",
    "wind": "3"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/confined-space-rescue",
  "inputs": {
    "o2": "29.5",
    "lel": "0",
    "h2s": "0",
    "co": "0",
    "entrySize": "0.6",
    "depth": "5"
  },
  "expect": [
    "超出安全范围(19.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/detector-11",
  "inputs": {
    "rated": "45",
    "measured": "15"
  },
  "expect": [
    "45mA"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/detector-20",
  "inputs": {},
  "expect": [
    "50140"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "fire-rescue/dizhensoujiuzhichengjisuan",
  "inputs": {
    "weight": "75",
    "angle": "45",
    "count": "4",
    "allow": "30"
  },
  "expect": [
    "106.07"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-alarm-zone",
  "inputs": {
    "floors": "9",
    "floorArea": "2000",
    "fireZones": "2",
    "height": "3.5"
  },
  "expect": [
    "18000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-extinguisher-selection",
  "inputs": {
    "area": "150"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-fighting-tactics",
  "inputs": {
    "fireArea": "300"
  },
  "expect": [
    "300"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-investigation",
  "inputs": {
    "burnArea": "75"
  },
  "expect": [
    "75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-load",
  "inputs": {
    "area": "150"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-resistance-rating",
  "inputs": {
    "height": "75"
  },
  "expect": [
    "2.00h"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-risk-assessment",
  "inputs": {
    "height": "36",
    "area": "5000",
    "density": "0.5"
  },
  "expect": [
    "36"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/high-rise-fire",
  "inputs": {
    "height": "120",
    "floors": "25",
    "fireFloor": "15",
    "ladder": "54"
  },
  "expect": [
    "120"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/hydrant-flow",
  "inputs": {
    "pressure": "3.25",
    "hoseLen": "25",
    "resistA": "0.0000147",
    "sk": "13"
  },
  "expect": [
    "3209.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/length-distance",
  "inputs": {
    "ppump": "3.8",
    "pnozzle": "0.2",
    "height": "0",
    "flow": "6.5"
  },
  "expect": [
    "1681.6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/post-fire-assessment",
  "inputs": {
    "fireTemp": "900",
    "duration": "2"
  },
  "expect": [
    "混凝土强度损失约70%以上"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/power-2",
  "inputs": {
    "flow": "30",
    "head": "60",
    "eff": "75",
    "sf": "1.15"
  },
  "expect": [
    "23.54"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/pressure-flow",
  "inputs": {
    "p1": "3.5",
    "p2": "0.3",
    "len": "20"
  },
  "expect": [
    "326.31"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/rescue-route",
  "inputs": {
    "floors": "15",
    "entrances": "2",
    "roadWidth": "6",
    "vehicles": "4"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/rope-rescue",
  "inputs": {
    "load": "150",
    "eff": "90",
    "angle": "90",
    "mbs": "30"
  },
  "expect": [
    "1.47"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/smoke-management",
  "inputs": {
    "qfire": "7500",
    "z": "5",
    "zl": "0",
    "hc": "3",
    "nports": "2",
    "portmax": "15000"
  },
  "expect": [
    "196160"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/speed-3",
  "inputs": {
    "mass": "120",
    "dia": "12",
    "mu": "0.2",
    "wraps": "2",
    "height": "10"
  },
  "expect": [
    "120kg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/sprinkler-design",
  "inputs": {
    "totalArea": "1500",
    "headArea": "12.5",
    "pressure": "0.10",
    "kfactor": "80",
    "opArea": "0"
  },
  "expect": [
    "1500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/temp-6",
  "inputs": {
    "time": "15"
  },
  "expect": [
    "10.25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/time-41",
  "inputs": {
    "thick": "15"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/time-air",
  "inputs": {
    "vol": "9.8",
    "press": "30",
    "alarm": "5.5",
    "freq": "20"
  },
  "expect": [
    "148.1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/time-evacuation",
  "inputs": {
    "aset": "15",
    "tdet": "1",
    "tpre": "2",
    "tmove": "4"
  },
  "expect": [
    "15.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/time-lux",
  "inputs": {
    "cap": "18000",
    "volt": "12",
    "power": "5",
    "eff": "100",
    "lux": "5",
    "area": "100",
    "uf": "0.7"
  },
  "expect": [
    "18000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/ventilation-tactics",
  "inputs": {
    "btype": "2"
  },
  "expect": [
    "利用楼梯井/管道井竖向排烟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/water-rescue",
  "inputs": {
    "temp": "23",
    "velocity": "0",
    "distance": "30"
  },
  "expect": [
    "23°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/wildfire-spread",
  "inputs": {
    "wind": "30",
    "slope": "15",
    "humidity": "40",
    "temp": "30",
    "hours": "3"
  },
  "expect": [
    "61473"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/zuranyangzhishupanding",
  "inputs": {
    "loi": "45",
    "material": "18"
  },
  "expect": [
    "18.0"
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
  console.log("==== fire-rescue calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
