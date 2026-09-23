#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "floral/golden-ratio",
  "inputs": {
    "containerH": "15",
    "containerW": "12"
  },
  "expect": [
    "花器"
  ]
},
{
  "slug": "floral/price",
  "inputs": {
    "budget": "8800",
    "basketLo": "200",
    "basketHi": "400",
    "wreathLo": "100",
    "wreathHi": "260",
    "share": "50"
  },
  "expect": [
    "花篮 18 个 / 花圈 18 个",
    "数量区间：26 ~ 58 件",
    "合计 8640.00 元"
  ]
},
{
  "slug": "floral/spiral-bouquet",
  "inputs": {
    "stemLength": "45",
    "mainRatio": "60"
  },
  "expect": [
    "复制清单"
  ]
},
{
  // 原为 all_default 弱用例：5 个数字全等于页面默认，expect「备用」是常量文案（逃生项）。
  "slug": "floral/wedding-flowers",
  "inputs": {
    "tables": "30",
    "guests": "200",
    "price": "8",
    "bridesmaidCount": "6",
    "boutonCount": "12"
  },
  "checkIds": [
    "itemBridal",
    "itemBridesmaid",
    "itemBouton",
    "itemCorsage",
    "itemCenter",
    "itemArch",
    "itemAisle",
    "itemWelcome"
  ],
  "expect": [
    "桌花×30桌",
    "通道花瓣×20米"
  ],
  "ref": "桌花数量 = CENTER_FLOWERS[centerStyle] × tables(=30)；通道花瓣米数 = max(5, ceil(guests/10)) = max(5,20) = 20。回退默认（tables=15 / guests=150）→ 「桌花×15桌」「通道花瓣×15米」，两串均不命中。"
},
{
  "slug": "floral/bloom-stage",
  "inputs": {},
  "expect": [
    "花瓣展开约1/2至2/3"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "floral/preservative",
  "inputs": {
    "water": "750"
  },
  "expect": [
    "0.15"
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
  console.log("==== floral calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
