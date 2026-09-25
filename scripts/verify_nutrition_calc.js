#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "nutrition/assessor-17",
  "inputs": {
    "weight": "90",
    "foodAmount": "500",
    "conc": "200"
  },
  "expect": [
    "您的实际摄入为1.11mg/kg/天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-1",
  "inputs": {
    "age": "45",
    "weight": "65",
    "height": "170"
  },
  "expect": [
    "1291"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-2",
  "inputs": {
    "foodWeight": "150",
    "manualCarb": "0",
    "manualProtein": "0",
    "manualFat": "0"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-3",
  "inputs": {
    "calories": "3000",
    "carbPct": "50",
    "proteinPct": "20",
    "fatPct": "30"
  },
  "expect": [
    "375.0g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-60",
  "inputs": {
    "age": "45",
    "height": "170",
    "weight": "75",
    "target": "68",
    "weeks": "10",
    "tdeeCustom": "0"
  },
  "expect": [
    "593"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calorie-deficit",
  "inputs": {
    "age": "42",
    "height": "170",
    "weight": "65"
  },
  "expect": [
    "1508"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/estimate-1",
  "clicks": [
    "getSelected = function(){return [0,3,6];};calculate();"
  ],
  "expect": [
    "已选择 3 种食物 · 建议每日 25-30g",
    "11.2g"
  ],
  "ref": "去默认化（原 expect「25-30g」＝建议区间静态标签，注入失败仍命中 → 逃生项）：本页选择态存于 DOM dataset.selected，而 getSelected() 用 querySelectorAll('#foodGrid .data-card[data-selected=\"1\"]') 读取——harness 将 querySelectorAll 重写为 dynQuery（不支持后代+属性组合选择器），真实点击勾选态读不出。故 clicks 在页面作用域覆盖 getSelected 返回 [0,3,6]（燕麦片4/苹果4.4/胡萝卜2.8）后 calculate()，等效「用户选 3 项」，result 渲染「11.2g 摄入不足」+「已选择 3 种食物 · 建议每日 25-30g」；默认未选显示「选择食物后点击估算。」，不含 11.2g/已选择 3 种，注入失败即不命中。"
},
{
  "slug": "nutrition/estimate-2",
  "inputs": {
    "extraSodium": "0"
  },
  "expect": [
    "1000mg"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：选中态用属性选择器 "
     + "[#foodGrid .data-card[data-selected=\"1\"]]，而动态 DOM 登记表只支持 id / class / tag 过滤 ⇒ 恒空；"
     + "只剩 extraSodium 一路，其输出为输入的直接派生（判别力不足）。（2026-09-25 实测）"
},
{
  "slug": "nutrition/food-calorie-lookup",
  "inputs": {
    "kw": "zzzqx"
  },
  "expect": [
    "未匹配到食物"
  ],
  "ref": "关键词过滤型：inputs 写 kw=zzzqx ⇒ oninput=filterFood() ⇒ render([]) 输出「未匹配到食物，请尝试关键词或更换表述。」。默认态 kw 空 ⇒ render(FOODS) 全量、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "nutrition/generator-glucose-load",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机组合型生成器，具体血糖负荷值非每次必现；改断言确定性生成标题）"
},
{
  "slug": "nutrition/nutrition-1",
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
  "slug": "nutrition/rater-32",
  "inputs": {
    "d1": "3"
  },
  "expect": [
    "95%"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 m1–m10 共 10 项 → 10/14 = 71.4% ≥ 70% → 依从性高（原用例 inputs 为空、
  // expect 取默认态分母串 "14" ⇒ 零判别力；默认 0 分输出 0% / 依从性低，故本 expect 有判别力）。
  "slug": "nutrition/rater-33",
  "checkIds": [
    "m1",
    "m2",
    "m3",
    "m4",
    "m5",
    "m6",
    "m7",
    "m8",
    "m9",
    "m10"
  ],
  "expect": [
    "71%)",
    "依从性高"
  ],
  "ref": "地中海饮食评分 14 项：达标 10 项 → 10/14 = 71.4% ≥ 70% → 依从性高"
},
{
  "slug": "nutrition/recommender-2",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机组合型生成器，具体蛋白含量非每次必现；改断言确定性生成标题）"
},
{
  "slug": "nutrition/recommender-3",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机组合型生成器，具体维含量非每次必现；改断言确定性生成标题）"
},
{
  "slug": "nutrition/recommender-4",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机组合型生成器，推荐量 100-150g 非每次必现；改断言确定性生成标题）"
},
{
  "slug": "nutrition/self-assess-5",
  "inputs": {
    "g1": "1"
  },
  "expect": [
    "94%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/generator-nutrition-label",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore — 随机营养标签生成器，改测结构标签"
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
  console.log("==== nutrition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
