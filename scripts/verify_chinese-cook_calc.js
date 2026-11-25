#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chinese-cook/cutting-sizes",
  "inputs": {
    "cut": "ding"
  },
  "expect": [
    "标准尺寸： 6-8 mm 形状特征： 立方小粒"
  ],
  "ref": "独立复算：切法「丁」⇒ 标准尺寸 6–8 mm、形状 立方小粒。⚠ 原 expect 'ding' 为切法选择值回显（零判别力）；默认切法为其他刀法，输出条目不同 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "chinese-cook/estimate-16",
  "inputs": {
    "v1": "150",
    "v2": "20"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/ingredient-substitute",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "的替代方案，请尝试其他关键词或查看下方速查表"
  ],
  "ref": "关键词过滤型：inputs 写 search=zzzqx ⇒ oninput=doSearch() ⇒ matched.length===0 ⇒ result 区渲染「未找到\"zzzqx\"的替代方案，请尝试其他关键词或查看下方速查表。」。锚点避开内层引号（防 extractCases 转义歧义）。默认态 kw 空 ⇒ showAll() 全量 14 条、blob 无该串（已双态核验）。"
},
{
  "slug": "chinese-cook/oil-temp",
  "inputs": {
    "temp": "5"
  },
  "expect": [
    "筷子周围气泡较多有声响"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/sauce-ratio",
  "inputs": {
    "spoons": "5"
  },
  "expect": [
    "15.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/wok-heat",
  "inputs": {
    "heat": "wang"
  },
  "expect": [
    "火力猛、升温快"
  ],
  "ref": "火候详情卡按 HEATS[heat] 渲染：注入 wang（旺火）⇒ 代表菜品「爆炒腰花、清炒时蔬」、火焰「高出锅底，色白亮」、温度「高温」。原注入 zhong 与页面默认 selected 相同 ⇒ 零判别力；且原锚「爆炒腰花、清炒时蔬」虽在旺火面板命中，但页面顶部四火候对照表静态含该词 ⇒ 撞默认态。改锚旺火面板专属特征说明「火力猛、升温快」（中火面板为「火力适中，均匀受热便于上色」，默认态不含）。"
}
,
{
  "slug": "chinese-cook/estimate-16",
  "inputs": {"v1": "", "v2": ""},
  "clicks": ["calc()"],
  "expect": ["请填写两项数值后再计算。"],
  "ref": "空态：两项清空后不再按 0 计算，改为提示；默认 500/20 ⇒ 100.00，不命中。"
},

  { slug: "chinese-cook/estimate-16", inputs: { v1: "200", v2: "15" },
    expect: ["200 的 15% = 30.00"],
    ref: "第827批：中文态「求部分值」不再硬编码英文 of；200×15%=30.00，默认 100/20=20.00 不含该串。" },
  { slug: "chinese-cook/estimate-16", inputs: { v1: "10", v2: "0" },
    clicks: ["m='percent';calc();"],
    expect: ["整体值为 0，不能作为分母计算百分比，请修改「整体」"],
    ref: "第827批：求百分比模式分母是「整体」(v2)；整体为 0 时旧提示误指「百分比为 0」。现明确指整体，默认模式不会出现该串。" },
  { slug: "chinese-cook/estimate-16", inputs: { v1: "0", v2: "10" },
    clicks: ["m='change';calc();"],
    expect: ["原值为 0，无法计算增长率，请修改「原值」"],
    ref: "第827批：增长率模式原值(v1)为 0 时旧提示误称「整体值为 0」；现按当前字段指向原值。"
  },
{
    "slug": "chinese-cook/sauce-ratio",
    "inputs": {"sauce":"tangcu","spoons":"0.001"},
    "expect": ["0.0030 勺","0.045 ml","用量过小"],
    "ref": "第866批：基准 0.001 勺时糖 3×0.001=0.003 勺，旧实现显示 0.00 勺；现按 2 位有效数字显示 0.0030，并提示用量过小建议放大或改用克/毫升。"
  },
  {
    "slug": "chinese-cook/sauce-ratio",
    "inputs": {"sauce":"tangcu","spoons":"3"},
    "expect": ["糖9.00 勺","糖3:醋3:酱油1:料酒1:水2","tangcu = 3:3:1:1:2"],
    "ref": "第866批：公式、表格与 SAUCES 实际预设统一为糖:醋:酱油:料酒:水=3:3:1:1:2。"
  },
  {
    "slug": "chinese-cook/ingredient-substitute",
    "inputs": {"search":"butter"},
    "clicks": ["doSearch();"],
    "expect": ["黄油","0.8:1","植物油"],
    "ref": "第866批：英文别名 butter 可命中黄油；植物油替代比例统一为按体积 0.8:1，并标注起酥/打发不适用。"
  },
  {
    "slug": "chinese-cook/ingredient-substitute",
    "inputs": {"search":"heavy cream"},
    "clicks": ["doSearch();"],
    "expect": ["淡奶油","牛奶+融化黄油","不可打发"],
    "ref": "第866批：补淡奶油条目及牛奶+黄油替代，注明仅煮制/烘焙面糊、不可打发。"
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

  console.log("==== chinese-cook calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
