#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "welding/analysis-37",
  "inputs": {
    "data": "气孔,45\n夹渣,20\n未焊透,15\n裂纹,8\n咬边,6\n其他,6"
  },
  "expect": [
    "缺陷总数： 100",
    "A 类（主要缺陷）： 3 项",
    "累计占比 80.00%"
  ],
  "ref": "总数100；累计占比45.00/65.00/80.00 ≤80% 共3项为A类"
},
{
  "slug": "welding/analysis-38",
  "inputs": { "cur": "220", "volt": "26", "spd": "5", "pre": "25", "eff": "0.8" },
  "expect": [
    "热输入： 915.20",
    "t8/5 冷却时间： 4.75",
    "平均冷却速率： 63.18"
  ],
  "ref": "Q=0.8×26×220/5=915.20 J/mm；t8/5=915.20/(2π×0.025)×(1/475−1/775)=4.75 s；速率 300/4.75=63.18 °C/s（默认 180/24/4/20 → 864.00/4.41/68.07，避开）"
},
{
  "slug": "welding/calc-1",
  "inputs": {
    "diameter": "6.2",
    "thickness": "8",
    "voltage": "24",
    "speed": "3"
  },
  "expect": [
    "133.92"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/detector-25",
  "inputs": {
    "plateThick": "36",
    "circDef": "3",
    "stripDef": "8",
    "evalArea": "500"
  },
  "expect": [
    "22.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/energy-cost-1",
  "inputs": {
    "current": "300",
    "voltage": "24",
    "time": "30",
    "price": "1.0",
    "duty": "60",
    "eff": "85"
  },
  "expect": [
    "2.541"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/flow-ratio",
  "inputs": {
    "nozzle": "18",
    "flow": "15",
    "ar": "80",
    "co2": "20"
  },
  "expect": [
    "98.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/hancaixuanyongtuijian",
  "inputs": {
    "thickness": "12"
  },
  "expect": [
    "136"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/hanjiegongzhuangjiajusheji",
  "inputs": {
    "length": "1500",
    "width": "500",
    "weight": "50"
  },
  "expect": [
    "147.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/hanjiezidonghuapinggu",
  "inputs": {
    "output": "15000",
    "seamlen": "0.5",
    "mansec": "120",
    "labor": "50",
    "robotcost": "30",
    "workdays": "250"
  },
  "expect": [
    "15000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/speed-voltage-current",
  "inputs": {
    "thickness": "9"
  },
  "expect": [
    "23.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/stress",
  "inputs": {
    "thickness": "15",
    "length": "300",
    "leg": "6",
    "yield": "235"
  },
  "expect": [
    "0.46°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/temp-10",
  "inputs": {
    "thickness": "18",
    "preheat": "100"
  },
  "expect": [
    "18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/temp-time-6",
  "inputs": {
    "thickness": "30",
    "ce": "0.45",
    "c": "0.18",
    "mn": "1.4",
    "cr": "0.1",
    "mo": "0"
  },
  "expect": [
    "130"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/ventilation-protection",
  "inputs": {
    "consume": "5",
    "volume": "500",
    "hours": "8"
  },
  "expect": [
    "1200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/wps-hanjiegongyiguichengbianzhi",
  "inputs": {
    "diameter": "4.2",
    "current": "200",
    "voltage": "24",
    "speed": "30",
    "preheat": "20",
    "pass": "2"
  },
  "expect": [
    "4.2mm"
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
  console.log("==== welding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
