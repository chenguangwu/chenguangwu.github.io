#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "floral/golden-ratio",
  "inputs": {
    "containerH": "24",
    "containerW": "18"
  },
  "clicks": [
    "currentStyle='cascade';calc()"
  ],
  "expect": [
    "瀑布型 · 理想花艺高度 = 花器×1.25",
    "花器 24cm",
    "30 理想 (cm)"
  ],
  "ref": "clicks 把顶层 var currentStyle 切到 cascade（STYLE_CONFIG.cascade：min 1.0 / ideal 1.25 / max 1.5）⇒ 花器 24 ⇒ 理想 30、最矮 24、最高 36（独立复算）。默认 triangle（ideal 1.5）+ 花器 15 ⇒ 22.5 cm、「三角形 · 理想花艺高度 = 花器×1.5」，三个锚点全不命中。原 expect「花器」是 renderViz 的 SVG 文本常量（默认态同样渲染）⇒ 已替换。"
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
    "bouquetSize": "large",
    "bouquetStyle": "cascade",
    "stemLength": "60",
    "mainRatio": "75"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "共需 35 枝花材",
    "大型花束共35枝，瀑布型风格",
    "主花 75%"
  ],
  "ref": "large：SIZE_CONFIG.total=35；mainRatio 75 ⇒ 主花 round(35×0.75)=26、余 9 ⇒ 配花 round(9×0.6)=5、叶材 4（独立复算）；cascade：fillerRatio 0.5 ⇒ 中层 60×0.5=30、outerRatio 0.6 ⇒ 外圈 36、叶材 60×0.75=45。默认 medium(18)/round(60%)/45 ⇒「共需 18 枝花材」「中等花束共18枝，圆球型风格」「主花 60%」，三个锚点全不命中（harness 下 select 回落首个 option small/round，同样不命中）。原 expect「复制清单」是结果区按钮文本常量（每次渲染都带）⇒ 已替换。"
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
  "clicks": ["selectStage(5)"],
  "expect": [
    "部分开始出现花粉",
    "当天使用的花艺作品",
    "此阶段观赏性已达峰值"
  ],
  "ref": "selectStage(grade,el) 的 el 仅用于加 active 样式，省略即可；grade=5 ⇒ STAGES[5] 盛花期。"
     + "锚点只取 resultDetail 独有串：默认态 bloomCards 已渲染全部六张卡片，含「等级 5：盛花期」与"
     + "「完全盛开，花瓣外翻」⇒ 这两个串在默认态即命中、零判别力，必须改锚详情页专属文案。"
     + "原 expect「花瓣展开约1/2至2/3」正是卡片里 grade 3 的 desc。",
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
