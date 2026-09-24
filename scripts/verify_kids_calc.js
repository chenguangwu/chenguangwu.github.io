#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "kids/focus-timer",
  "inputs": {
    "focusMin": "25",
    "restMin": "8",
    "goalCount": "6"
  },
  "clicks": ["renderStats()"],
  "expect": [
    "6 今日目标"
  ],
  "ref": "目标数直接由 goalCount 渲染 ⇒ 注入 6 得「6 今日目标」（默认 4）。"
     + "原 expect「今日完成度」是统计卡标题（静态文本，回退默认仍命中 ⇒ 逃生项）。"
     + "注：今日番茄 / 累计番茄取自 localStorage（harness 恒空 ⇒ 恒 0），不可断言。",
  },
{
  "slug": "kids/memory-palace",
  "inputs": {
    "srcInput": "圆周率 3.1415926",
    "cellCount": "12"
  },
  "expect": [
    "12"
  ],
  "ref": "auto-restore"
},
{
  "slug": "kids/mirror-letter",
  "inputs": {
    "typeSel": "number"
  },
  "expect": [
    "number"
  ],
  "ref": "auto-restore"
},
{
  "slug": "kids/multiplication-practice",
  "inputs": {},
  "expect": [
    "50%"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "kids/stroke-order",
  "inputs": {
    "charInput": "永",
    "speedSel": "900"
  },
  "expect": [
    "900"
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
  console.log("==== kids calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
