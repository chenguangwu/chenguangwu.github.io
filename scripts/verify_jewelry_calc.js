#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "jewelry/convert-31",
  "inputs": {
    "val": "1",
    "from": "4.166666666666667"
  },
  "expect": [
    "4.166666666666667"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/diamond-carat",
  "inputs": {
    "d": "9.5",
    "w": "0",
    "h": "3.9"
  },
  "expect": [
    "2.1470"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/gem-hardness",
  "inputs": { "filter": "7-7.5" },
  "expect": [
    "硬度因品种略有差异6.5-7.5 锂辉石(紫锂辉) Kunzite"
  ],
  "ref": "按硬度档筛选的图鉴页：默认 all 渲染全表 ⇒ 任何单行文本都是逃生项，只能锚「仅过滤态成立的跨行相邻串」。注入 7-7.5 后顺序为 祖母绿/海蓝宝石/碧玺/紫水晶/黄水晶/石榴石/锂辉石，而默认全表中「石榴石」后紧邻「橄榄石」⇒ 跨行串「石榴石…锂辉石(紫锂辉) Kunzite」仅过滤态成立（判别器换回 all 即全表 ⇒ 该串消失）。非默认输入+独立复算。"
},
{
  "slug": "jewelry/gold-purity",
  "inputs": {
    "weight": "15",
    "custom": "750"
  },
  "expect": [
    "11.2500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/pearl-grading",
  "inputs": {
    "size": "14"
  },
  "expect": [
    "4.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/ring-size",
  "inputs": {
    "circum": "55",
    "diameter": "26.5"
  },
  "expect": [
    "26.52"
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
  console.log("==== jewelry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
