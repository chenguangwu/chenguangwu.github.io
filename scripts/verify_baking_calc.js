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
    "flour": "750",
    "pct": "72"
  },
  "expect": [
    "540.0 g",
    "1 : 1.389",
    "1290.00 g"
  ],
  "ref": "非默认输入（默认 500/60）：配料重 = 750 × 72 ÷ 100 = 540 ⇒ 主行「540.0 g」；主料与配料合计 = 750 + 540 = 1290 ⇒ 换算链「1290.00 g」；粉水比例 = 100 ÷ 72 = 1.389 ⇒「1 : 1.389」。默认态为 300.0 g / 800.00 g / 1 : 1.667。"
},
{
  "slug": "baking/convert-temp",
  "inputs": {
    "val": "4",
    "rate": "2.5",
    "from": "1000",
    "to": "1"
  },
  "expect": [
    "10000.000000",
    "系数: 2.5"
  ],
  "ref": "非默认输入（默认 val=1、rate=1，from/to 首项均为 1）：结果 = 4 × 2.5 × 1000 ÷ 1 = 10000 ⇒ 页面展示 r.toFixed(6) = 10000.000000；系数行回显 rate = 2.5。默认态为 1.000000 / 系数: 1。"
},
{
  "slug": "baking/dough-hydration",
  "inputs": {
    "flour": "800",
    "water": "400"
  },
  "expect": [
    "极低含水量",
    "紧实干硬，难以揉制 · 适合贝果、椒盐脆饼"
  ],
  "ref": "非默认输入（默认 500/350 ⇒ 70%）：含水量 = 400 ÷ 800 × 100 = 50%（hydVal 显示 50%，但页面静态参考表已含「50%」故不锚）；50 < 56 落 getHydInfo 首分支 ⇒ grade「极低含水量」、desc「紧实干硬，难以揉制 · 适合贝果、椒盐脆饼」（默认 70% 落 <73 的「较高含水量」分支）。"
},
{
  "slug": "baking/fermentation-time",
  "inputs": {
    "baseTime": "40",
    "actualTemp": "17",
    "actualHumidity": "75",
    "fermType": "cold"
  },
  "expect": [
    "100 分钟",
    "修正系数 ×0.4",
    "约 1.7 小时（基准 40 分钟）"
  ],
  "ref": "非默认输入（默认 60/24/70/yeast）：fermType=cold ⇒ q10 = 2.5；tempFactor = 2.5^((17−27)/10) = 2.5^(−1) = 0.4；humFactor = 1 + (75−75)×0.008 = 1；totalFactor = 0.4 ⇒ 实际时长 = 40 ÷ 0.4 = 100 分钟；小时 = 100/60 = 1.667 ⇒ 显示「约 1.7 小时（基准 40 分钟）」；系数徽标「修正系数 ×0.4」。默认态为 76.9 分钟 / ×0.8。"
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
