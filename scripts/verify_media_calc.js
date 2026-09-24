#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "media/assessor-25",
  "inputs": {
    "sent": "8000",
    "opened": "3200",
    "finished": "2000",
    "interact": "900",
    "readTime": "75",
    "words": "2200"
  },
  "expect": [
    "40.0% 打开率",
    "综合评分： 9/9"
  ],
  "ref": "原 all_default 弱用例（10000/2500/1200/350/45/1500 恰等于页面默认）+ expect「复制到后续内容」是结论文案常量。改为 sent=8000/opened=3200/finished=2000/interact=900/readTime=75/words=2200：打开率 3200/8000 = 40.0%、完读率 2000/3200 = 62.5%、互动率 900/3200 = 28.1%；阅读完成度 = 75s ÷（2200 字 ÷ 300 字/分 × 60 = 440s）= 17%；三项指标全达标 ⇒ 综合评分 9/9「阅读效果优秀」。默认态 25.0% / 48.0% / 14.0% ⇒ 不足 9 分（跨档）"
},
{
  "slug": "media/tester-14",
  "inputs": {
    "aShow": "6000",
    "aClick": "480",
    "bShow": "6000",
    "bClick": "360"
  },
  "expect": [
    "8.00% 方案A CTR",
    "推荐采用方案A"
  ],
  "ref": "原 all_default 弱用例（A 5000/250、B 5000/380 恰等于页面默认）+ expect「建议采用方案」是阈值判定文案。改为 A 480/6000、B 360/6000：CTR 8.00% vs 6.00%，相对提升 (8−6)/8 = 25.0% ⇒ 胜出方翻转为 A（默认态 B 380/5000 = 7.60% > A 250/5000 = 5.00%，胜出方为 B）"
},
{
  "slug": "media/tester-18",
  "inputs": {
    "aShow": "3000",
    "aClick": "250",
    "bShow": "3000",
    "bClick": "150"
  },
  "expect": [
    "8.33% 标题A CTR",
    "推荐采用标题A"
  ],
  "ref": "原 all_default 弱用例（A 3000/120、B 3000/210 恰等于页面默认）+ expect「继续迭代测试」是末尾静态建议文案。改为 A 250/3000、B 150/3000：CTR 8.33% vs 5.00%，相对提升 (8.33−5.00)/8.33 = 40.0% ⇒ 胜出方翻转为标题A（默认态 A 120/3000 = 4.00% < B 210/3000 = 7.00%，B 胜）"
},
{
  "slug": "media/analysis-26",
  "inputs": {
    "data": "物流太慢，包装破损，非常失望\n质量很好，客服耐心，强烈推荐\n一般般，没什么特别感觉"
  },
  "expect": [
    "情感倾向： 整体中性",
    "正面 1 / 负面 1 / 中性 1"
  ],
  "ref": "重做为舆情情感词频：3 条 → 负面1（失望）/正面1（推荐）/中性1（一般般），倾向整体中性（默认 正面2/负面1/中性0 → 偏正面，区分）。非默认输入 + 独立复算。"
},
{
  "slug": "media/analysis-funnel",
  "inputs": {
    "data": "2000,1000,400,120"
  },
  "expect": [
    "6.00%"
  ],
  "ref": "整体转化率 = 末环节/首环节 = 120/2000 = 6.00%（独立手算）"
},
{
  "slug": "media/tester-13",
  "inputs": {
    "title": "震惊！这个方法让你轻松月入过万",
    "platform": "toutiao"
  },
  "expect": [
    "适合toutiao"
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
  console.log("==== media calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
