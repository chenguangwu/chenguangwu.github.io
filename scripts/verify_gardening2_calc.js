#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gardening2/fertilizer-ppm",
  "inputs": {
    "targetPpm": "150",
    "waterAmount": "5",
    "nutrientPct": "12"
  },
  "clicks": ["calc()"],
  "expect": [
    "6.25 g"
  ],
  "ref": "养分需求=150 mg/L × 5 L=750 mg；肥料量=750/0.12=6250 mg=6.25 g。"
     + "原 expect「约滴数」是结果区静态标签（回退默认仍命中 ⇒ 逃生项），且 200/1/20 为默认态。"
},
{
  "slug": "gardening2/lawn-height",
  "clicks": [
    "currentSeason='winter';renderGrass();renderHeight();"
  ],
  "expect": [
    "2 cm 狗牙根（百慕大） · 冬季"
  ],
  "ref": "去默认化（原 expect「推荐2.5cm」＝默认春季态，注入失败仍命中 → 逃生项）：harness 将元素 click() 桩成空操作，故改直接置顶层全局 currentSeason='winter' 后调 renderGrass()/renderHeight()，heightDisplay 渲染冬季草种留茬「2 cm 狗牙根（百慕大） · 冬季 · 暖季型（休眠期）」；默认春季显示「2.5 cm ... · 春季」，注入失败即不命中。（getTip 在暖季型冬季分支报错但被 clicks 的 try/catch 吞掉，不影响 heightDisplay 已写入。）"
},
{
  "slug": "gardening2/pest-control",
  "inputs": {},
  "expect": [
    "10-14天"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening2/pruning-time",
  "inputs": {},
  "expect": [
    "冬季休眠期重剪至3-5芽"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening2/watering-frequency",
  "inputs": {
    "potSize": "23"
  },
  "expect": [
    "0.42"
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
  console.log("==== gardening2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
