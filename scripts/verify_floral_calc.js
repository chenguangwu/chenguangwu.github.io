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
    "合计 8640.00 元",
    "余额 160.00 元"
  ],
  "ref": "独立复算：bAvg=(200+400)/2=300、wAvg=(100+260)/2=180、share=50% ⇒ mix=300×0.5+180×0.5=240；总数=⌊8800/240⌋=36，nB=round(36×0.5)=18、nW=18（锚花篮/花圈18）；合计=18×300+18×180=8640（锚金额）；数量区间 mixLo=200×0.5+100×0.5=150→⌊8800/150⌋=58、mixHi=400×0.5+260×0.5=330→⌊8800/330⌋=26（锚 26~58）。默认 budget5000/单价150-300/80-200/share60 三锚均不命中。"
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
  "clicks": ["calc()"],
  "expect": [
    "桌花×30桌",
    "通道花瓣×20米",
    "1212 枝（基础 1082 + 备用 130）",
    "9696 元"
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
  "slug": "floral/wedding-flowers",
  "inputs": {"tables":"0","guests":"100","price":"5","bridesmaidCount":"4","boutonCount":"8"},
  "checkIds": ["itemCenter"],
  "clicks": ["calc()"],
  "expect": ["勾选桌花时桌数须 ≥1"],
  "ref": "勾选桌花但 tables=0 ⇒ 必须拒绝，不能静默按 0 桌出结果。"
},
{
  "slug": "floral/price",
  "inputs": {"budget":"8800","basketLo":"400","basketHi":"300","wreathLo":"100","wreathHi":"260","share":"50"},
  "clicks": ["calc()"],
  "expect": ["花篮单价上限不能低于下限"],
  "ref": "上限 300 < 下限 400 ⇒ 直接提示，不再静默计算。"
},
{
  "slug": "floral/golden-ratio",
  "inputs": {"containerH":"15","containerW":"0"},
  "clicks": ["calc()"],
  "expect": ["请输入大于 0 的花器高度与直径"],
  "ref": "直径 0 不得进入 SVG，也不能回退为高度。"
},
{
  "slug": "floral/preservative",
  "inputs": {
    "water": "750"
  },
  "clicks": ["calc()"],
  "expect": [
    "15 g",
    "约包数（每包 10 g）"
  ],
  "ref": "500ml 标准包 10g ⇒ 1包；750ml ⇒ 750×10/500=15g、1.5包（独立复算）。默认 500ml ⇒ 10g、1包，两锚均不命中。"
},
{
  "slug": "floral/preservative",
  "inputs": {"water":"750"},
  "clicks": ["document.getElementById('presType').value='custom';toggleCustom();calc()"],
  "expect": ["15 g","每包 10 g"],
  "ref": "自定义 10g/500ml、每包10g，750ml ⇒ 15g、1.5包；验证按包装标签自定义路径。"

}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== floral calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
