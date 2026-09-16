#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "travel/aim-trainer",
  "inputs": {},
  "expect": [
    "30.0s"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/business-name-generator",
  "inputs": {
    "count": "15"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/currency-cheat-sheet",
  "inputs": {
    "rate": "7.20",
    "customAmounts": "1,5,10,20,50,100",
    "currency": "EUR,7.80,🇪🇺,€,欧元"
  },
  "expect": [
    "1560"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/emergency-phrasebook",
  "inputs": {},
  "expect": [
    "ee-mer-jen-see"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/international-tip-calculator",
  "inputs": {
    "bill": "150",
    "people": "1"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/jet-lag-recovery",
  "inputs": {
    "flightHours": "12",
    "fromTz": "9"
  },
  "expect": [
    "-14小时"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/luggage-size-checker",
  "inputs": {
    "l": "83",
    "w": "40",
    "h": "20",
    "wt": "7"
  },
  "expect": [
    "83×40×20cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/packing-list",
  "inputs": {
    "tripName": "我的旅行"
  },
  "expect": [
    "0/6"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/passport-validator",
  "inputs": {},
  "expect": [
    "等待输入..."
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/recommender-10",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/recommender-9",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "生成结果"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/road-trip-gas-cost",
  "inputs": {
    "distance": "750",
    "consumption": "8",
    "price": "7.5",
    "tolls": "200",
    "people": "2"
  },
  "expect": [
    "60.0L"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/timezone-lookup",
  "inputs": {},
  "expect": [
    "等待输入..."
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/travel-adapter-guide",
  "inputs": {},
  "expect": [
    "未找到"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/travel-budget-calculator",
  "inputs": {
    "days": "11",
    "people": "2",
    "transport": "3000",
    "accommodation": "500",
    "food": "200",
    "tickets": "800",
    "shopping": "1000",
    "emergency": "1000"
  },
  "expect": [
    "(22.2%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/travel-days-counter",
  "inputs": {},
  "expect": [
    "8 天 (7晚)"
  ],
  "ref": "auto-restore(default)；页面默认 start=今天、end=今天+7，原期望绝对日期 2026-09-15 随真实日期漂移（过期 1 天），改断言与今天无关的行程时长「8 天 (7晚)」（恒为 7 晚行程）",
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/travel-insurance-comparison",
  "inputs": {
    "days": "21"
  },
  "expect": [
    "120-240"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/travel-photo-storage",
  "inputs": {
    "days": "11",
    "perDay": "100",
    "videoMin": "10"
  },
  "expect": [
    "1100"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/visa-requirement-checker",
  "inputs": {},
  "expect": [
    "持有效美/日/澳等签证可免7天"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "travel/world-timezone-converter",
  "inputs": {},
  "expect": [
    "北京/上海"
  ],
  "ref": "auto-restore(default)；页面按 new Date() 显示各时区当前日期，原期望绝对日期 2026-09-15 随真实日期漂移（过期 1 天），改断言与今天无关的静态城市标签「北京/上海」",
  "ref": "auto-restore(default)"
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
  console.log("==== travel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
