#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "fengshui/birthday-analysis",
  "inputs": {
    "birthDate": "1990-01-01",
    "birthHour": "1"
  },
  "expect": [
    "(0)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fengshui/fengshui-calculator",
  "inputs": {
    "angleSlider": "0",
    "angleInput": "0",
    "houseDir": "45"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fengshui/fengshui-guide",
  "inputs": {},
  "expect": [
    "是研究环境与人类居住关系的学问"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "fengshui/good-day-selector",
  "inputs": {
    "startDate": "2026-10-01"
  },
  "clicks": [
    "selectActivity('wedding');findGoodDays();"
  ],
  "expect": [
    "未来30天（建除十二神）"
  ],
  "ref": "date 输入 + 顶层 currentActivity 状态：inputs 写 startDate=2026-10-01、clicks 调 selectActivity('wedding') 置 currentActivity 后 findGoodDays() 渲染 30 天吉凶结果区；默认态（无 startDate）findGoodDays 早返回 toast、结果区为空，故「未来30天（建除十二神）」为排他锚点（已双态核验默认态无此串）。"
},
{
  "slug": "fengshui/zodiac-lookup",
  "inputs": {
    "birthYear": "2985"
  },
  "expect": [
    "2985"
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
  console.log("==== fengshui calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
