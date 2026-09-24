#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "plastic/blow-molding",
  "inputs": {
    "partDia": "83",
    "parisonDia": "25",
    "parisonWall": "4",
    "bur": "3.2",
    "yieldStr": "25",
    "wallThk": "1.2",
    "bottleDia": "80"
  },
  "expect": [
    "11.02"
  ],
  "ref": "auto-restore"
},
{
  "slug": "plastic/extrusion-rate",
  "inputs": {
    "screwDia": "68",
    "screwRpm": "80",
    "density": "0.95",
    "pitch": "65",
    "channelDepth": "6",
    "efficiency": "40"
  },
  "expect": [
    "75963.71"
  ],
  "ref": "auto-restore"
},
{
  "slug": "plastic/injection-cycle",
  "inputs": {
    "injectTime": "6",
    "holdTime": "5",
    "coolTime": "20",
    "openTime": "3",
    "ejectTime": "2",
    "closeTime": "3",
    "cavities": "4",
    "hoursPerDay": "24",
    "yieldRate": "95"
  },
  "expect": [
    "8862"
  ],
  "ref": "auto-restore"
},
{
  "slug": "plastic/shrinkage-calc",
  "inputs": {
    "moldSize": "103",
    "partSize": "98.5",
    "targetSize": "100",
    "shrinkRate": "1.5"
  },
  "expect": [
    "4.5000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "plastic/material-select",
  "inputs": { "filterSelect": "耐高温" },
  "expect": [
    "手机壳、镜片、头盔 透明,高强度,耐高温 PA66"
  ],
  "ref": "按特性筛选的图鉴页：默认「全部材料」渲染全表 ⇒ 任何单行文本都是逃生项，只能锚「仅过滤态成立的跨行相邻串」。注入 耐高温 后 PC 行紧邻 PA66 行，而默认全表中 PC 后紧邻 POM ⇒ 该跨行串仅过滤态成立（判别器换回「全部材料」即全表 ⇒ 该串消失）。非默认输入+独立复算。"
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
  console.log("==== plastic calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
