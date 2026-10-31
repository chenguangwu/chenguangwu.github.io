#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "transport/calc-4",
  "inputs": {},
  "clicks": ["toggle(0,true);toggle(13,true);calc()"],
  "expect": [
    "¥300 累计罚款",
    "10 累计记分",
    "2 距12分剩余"
  ],
  "ref": "违法项 checkbox 由 renderList() 拼 innerHTML 生成（静态无 id ⇒ clicks 调 toggle(idx,true) 后 calc()）：勾 0 不按规定会车（¥100/扣1）与 13 高速公路违法占用快车道（¥200/扣9）⇒ 累计 ¥300、记分 10、距 12 分剩 2（默认未勾 ⇒ 仅提示「请勾选违法行为后再计算。」）。非默认输入+独立复算。"
},
{
  "slug": "transport/calc-53",
  "inputs": {
    "q1": "480",
    "q2": "380",
    "q3": "410",
    "q4": "350",
    "hourly": "120,80,50,40,60,180,450,780,820,700,650,720,760,690,640,720,820,950,1050,880,620,400,260,160"
  },
  "expect": [
    "480"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-3",
  "inputs": {
    "hours": "7",
    "minutes": "30",
    "firstHour": "10",
    "afterHour": "5",
    "dailyCap": "60"
  },
  "expect": [
    "42.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-depreciation",
  "inputs": {
    "cost": "300000",
    "life": "5",
    "salvageRate": "5"
  },
  "expect": [ "300,000 购车原值" ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-fuel",
  "inputs": {
    "distance": "750",
    "consumption": "7.5",
    "price": "8.00"
  },
  "expect": [ "450.00 总油费" ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-speed",
  "inputs": {
    "speed": "180",
    "reaction": "0.75",
    "slope": "0"
  },
  "expect": [
    "169.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-tire",
  "inputs": {
    "oldSpec": "225/45R17_X",
    "newSpec": "225/50R17"
  },
  "expect": [ "请使用如 225" ],
  "ref": "auto-restore"
},
{
  "slug": "transport/convert-fuel-oil",
  "inputs": {
    "val": "45"
  },
  "expect": [
    "5.23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/convert-volume-weight",
  "inputs": {
    "l": "60",
    "w": "30",
    "h": "20"
  },
  "expect": [
    "60×30×20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/cycle-signal",
  "inputs": {
    "cycle": "90",
    "satFlow": "1800",
    "phaseCount": "3"
  },
  "expect": [
    "1.050"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-4",
  "inputs": {
    "boxL": "60",
    "boxW": "30",
    "boxH": "25",
    "boxWt": "8"
  },
  "expect": [
    "76.9%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-capacity",
  "inputs": {
    "laneW": "6.75",
    "shoulder": "3.0",
    "speed": "120",
    "heavy": "10",
    "volume": "1800",
    "phf": "0.92"
  },
  "expect": [
    "6.75"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-energy",
  "inputs": {
    "capacity": "90",
    "consumption": "20",
    "soc": "80"
  },
  "expect": ["90\n20\n80\n1.00\n450 满电续航 (km) 360 当前可行驶 (km) 20.0 实际能耗 0.20 kWh/公里 当前电量 80%，可行驶约 360 km 。\n标准 450 km 夏季 429 km 冬季 346 km ❄️ 冬季续航较标准下降约 23% ，较夏季少约 82 km。"],
  "ref": "2026-10-25 修复 kWh/公里 卡片：原式 100/effCons×cap/100 实为满电续航数值（90/17.05=5.28，锚定了 bug 输出），正确为实际能耗÷100（cons=20、soc=80 修正后 effCons=17.0 → 0.17 kWh/km；判别器换回默认 cons=15 → 0.13，不重合）"
},
{
  "slug": "transport/estimate-speed-time",
  "inputs": {
    "distance": "600",
    "speed": "100",
    "restCount": "2",
    "restMin": "20",
    "depart": "08:00"
  },
  "expect": [
    "6小时40分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/noise",
  "inputs": {
    "volume": "3000",
    "speed": "80",
    "heavy": "8",
    "distance": "30"
  },
  "expect": [
    "(3000)"
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

  console.log("==== transport calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
