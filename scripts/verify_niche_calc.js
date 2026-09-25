#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "niche/aquarium-light",
  "inputs": {},
  "expect": [
    "0.3-0.5"
  ],
  "ref": "auto-restore(default)｜结构性不可注入：唯一排他串是空集提示「未找到匹配的水草」，但兜底链中 selectLevel() 无参执行会置 currentLevel=undefined ⇒ renderPlants() 恒得空集并渲染同一提示 ⇒ 默认/失败态同串，锚点无法区分（discriminate 实测判为逃生项）。"
},
{
  "slug": "niche/audio-sample-rate",
  "inputs": {
    "duration": "90"
  },
  "expect": [
    "0.69"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/candle-burn-time",
  "inputs": {
    "weight": "300",
    "diameter": "70"
  },
  "expect": [
    "36小时26分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/ceramic-firing",
  "inputs": {
    "fireType": "glaze"
  },
  "expect": [
    "过石英转变点573°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/convert-fps",
  "inputs": {
    "val": "45",
    "fps": "30"
  },
  "expect": [
    "1.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/convert-sample",
  "inputs": {
    "val": "66150",
    "sr": "44.1"
  },
  "expect": [
    "66150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/fish-tank-volume",
  "inputs": {
    "length": "90",
    "width": "30",
    "diameter": "40",
    "frontLen": "60",
    "backLen": "50",
    "bowWidth": "30",
    "height": "35",
    "substrate": "5"
  },
  "expect": [
    "19.26"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/honey-estimator",
  "inputs": {
    "hives": "15",
    "area": "50"
  },
  "expect": [
    "12250"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/lawn-mowing",
  "inputs": {
    "season": "summer"
  },
  "expect": [
    "6cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/pet-age",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "44岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/photography-exposure",
  "inputs": {
    "aperture": "1.8"
  },
  "expect": [
    "1/15s"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/pruning-calendar",
  "inputs": {
    "searchInput": "zzzqx"
  },
  "expect": [
    "未找到匹配的植物"
  ],
  "ref": "关键词过滤型：inputs 写 searchInput=zzzqx ⇒ oninput=filterPlants() ⇒ renderPlants() 得空集 ⇒ 「未找到匹配的植物」。默认态渲染当季 16 种植物全量、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "niche/recommender-temp-pottery",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "niche/succulent-watering",
  "inputs": {
    "season": "summer"
  },
  "expect": [
    "每20天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/video-fps",
  "inputs": {
    "duration": "15"
  },
  "expect": [
    "1800"
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
  console.log("==== niche calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
