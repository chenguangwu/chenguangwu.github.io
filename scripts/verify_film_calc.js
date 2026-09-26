#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "film/aspect-ratio",
  "inputs": {
    "width": "1920",
    "height": "1080",
    "srcWidth": "1920",
    "srcHeight": "1080",
    "ratio": "2.35"
  },
  "expect": [
    "2.3500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/color-grading",
  "inputs": {},
  "expect": [
    "2000-50000K"
  ],
  "ref": "结构性不可注入（2026-09-26 复核，原 ref 为 auto-restore(default) 未评估项）：页面有 `#searchInput` / `#filterSelect` 与顶层 `filterData()`，但 filterData 的唯一副作用是 `tr.style.display = '' | 'none'` —— harness 的 collectStrings 只采 DOM 的 `value`/`innerHTML`/`textContent`，**不采 style**，且 textContent 对隐藏行同样返回文本 ⇒ 任何过滤态与默认态采集结果完全相同。改用 `tr.remove()` 能让行消失，但那是 harness 侧删 DOM、不测页面筛选逻辑（折扣注入）⇒ 维持 no_inputs，断言初始化渲染串。"
},
{
  "slug": "film/convert-time-1",
  "inputs": {
    "h": "7",
    "m": "0",
    "s": "10",
    "f": "0",
    "fps": "25"
  },
  "expect": [
    "25210.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/editing-timecode",
  "inputs": {
    "tcInput": "01:23:45:12",
    "totalFrames": "181251"
  },
  "expect": [
    "7552.125"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/render-time",
  "inputs": {
    "totalFrames": "6480",
    "frameTime": "8",
    "nodes": "4",
    "fps": "24",
    "hoursPerDay": "24",
    "retryRate": "5"
  },
  "expect": [
    "54432"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/vfx-shot",
  "inputs": {
    "shotCount": "180",
    "shotDuration": "5",
    "hoursPerShot": "40",
    "teamSize": "8",
    "dailyRate": "1500"
  },
  "expect": [
    "112.5"
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
  console.log("==== film calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
