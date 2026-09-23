#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原 expect「复制配方」是结果卡里的按钮文案（常量），注入失败照样命中 = 逃生项。
  // 改非默认面粉/目标重量，断言由两者派生的缩放比例与新面粉重量（独立 Python 复算）。
  "slug": "baking/baker-percentage",
  "inputs": {
    "flourWeight": "600",
    "targetTotal": "1000"
  },
  "expect": [
    "缩放比例： ×0.989",
    "新面粉重量： 593.5 g"
  ],
  "ref": "配料表百分比和 totalPct=100+65+2+1.5=168.5；newFlour = 1000/168.5×100 = 593.4718 → fmtNum 取 1 位小数 = 593.5；ratio = 593.4718/600 = 0.98912 → fmtNum 取 3 位小数 = 0.989。回退默认（500/800）→ ×0.95 / 474.8 g，两串均不命中。"
},
{
  "slug": "baking/convert-28",
  "inputs": {
    "flour": "500",
    "pct": "60"
  },
  "expect": [
    "面粉"
  ]
},
{
  "slug": "baking/convert-temp",
  "inputs": {
    "val": "1",
    "rate": "1"
  },
  "expect": [
    "系数"
  ]
},
{
  "slug": "baking/dough-hydration",
  "inputs": {
    "flour": "500",
    "water": "350"
  },
  "expect": [
    "较高含水量"
  ]
},
{
  "slug": "baking/fermentation-time",
  "inputs": {
    "baseTime": "60",
    "actualTemp": "24",
    "actualHumidity": "70"
  },
  "expect": [
    "湿度适宜"
  ]
},
{
  "slug": "baking/mold-volume",
  "inputs": {
    "'+side+'D": "'+(side==='from'?'15':'20')+'",
    "'+side+'H": "7",
    "'+side+'S": "'+(side==='from'?'15':'20')+'",
    "'+side+'L": "'+(side==='from'?'15':'20')+'",
    "'+side+'W": "10"
  },
  "expect": [
    "高度"
  ]
},
{
  // 原 expect「请输入有效温度」由零参兜底调用 convertTemp() 触发（两个温度框皆空）→ 与注入无关的逃生项。
  // 改断言双向换算结果 + 按摄氏值分档的标签；回退默认（tempC=180、tempF 空）会落到错误分支，故必失配。
  "slug": "baking/oven-temp",
  "inputs": {
    "tempC": "160",
    "tempF": "320"
  },
  "expect": [
    "160°C = 320°F",
    "中低温 - 蛋糕、饼干"
  ],
  "ref": "160°C → f = 160×9/5+32 = 320°F；getTempLabel(160)：140 ≤ c < 170 → 「中低温 - 蛋糕、饼干」。回退默认 tempC=180 → 「180°C = 356°F」+「中温 - 面包、披萨（常用）」，且 tempF 变空后落到「请输入有效温度」分支，两串均不命中。"
},
{
  "slug": "baking/recipe-scaler",
  "inputs": {
    "factor": "4.5",
    "rows": "面粉=200g\\n糖=100g\\n鸡蛋=2个\\n牛奶=150ml\\n黄油=50g"
  },
  "expect": [
    "900g"
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
  console.log("==== baking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
