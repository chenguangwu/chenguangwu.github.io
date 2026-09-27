#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "psychology/attachment-style-test",
  "inputs": {
    "at' + i + '_' + l.v + '": "' + l.v + '_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychology/calc-12",
  "inputs": {
    "s-life": "0",
    "s-health": "10",
    "s-relation": "10",
    "s-work": "10",
    "s-finance": "10",
    "s-growth": "10",
    "s-leisure": "10",
    "s-safety": "10",
    "s-self": "10",
    "s-mood": "10"
  },
  "expect": [
    "最短板：生活满意度（0 分）"
  ],
  "ref": "inputs 写 10 个滑杆（id=s-<维度键>）：life=0、其余=10 ⇒ getScores 求和 90 ⇒ level(90)='很高'；min=0 落在 life、max=10 落在 health。默认 DEFAULTS=[7,6,7,6,5,6,5,7,6,6] 合计 61 ⇒ 最短板是经济状况（5 分）。注入态唯一产出「最短板：生活满意度（0 分）」，双态可区分。"
},
{
  "slug": "psychology/generator-20",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychology/holland-career-test",
  "inputs": {
    "hl' + i + '_' + val + '": "' + val + '_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychology/random-12",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机卡片生成器，具体存活率非每次必现；改断言确定性生成标题）（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "psychology/tester-2",
  "clicks": [
    "for(var i=0;i<MT_QS.length;i++){MT_ANS[i]=(i%2);}MT_CUR=MT_QS.length-1;calc();"
  ],
  "expect": [
    "ESTJ"
  ],
  "ref": "60 题全作答（MT_ANS[i]=i%2）→ calc 出完整 MBTI 结果（ESTJ，E 52%/I 48% 等）。回退默认（MT_ANS 全 null）→ calc 提示「还有 60 题未作答」，不命中 ESTJ。"
},

{
  "slug": "psychology/phq9-assessment",
  "clicks": [
    "for(var i=0;i<PHQ_QS.length;i++){PHQ_ANS[i]=3;}calc();"
  ],
  "expect": [
    "27 / 27",
    "总分 27（0–27）"
  ],
  "ref": "PHQ-9 共 9 题、量表 0–3；9 题全选「几乎每天」(3) ⇒ 总分 27（0–27），≥20 ⇒ 重度抑郁。默认态 PHQ_ANS 全 null，calc 只输出「还有 9 题未作答」，与本值不重合"
},
{
  "slug": "psychology/assessor",
  "clicks": [
    "for(var i=0;i<AS_QS.length;i++){AS_ANS[i]=3;}calc();"
  ],
  "expect": [
    "30 / 40",
    "拖延程度 75%"
  ],
  "ref": "拖延量表 10 题、量表 0–4（满分 40）；全选「经常」(3) ⇒ 总分 30，≤30 ⇒ 中度拖延；pct=round(30/40*100)=75%。默认态 10 题均未作答，不命中"
},
{
  "slug": "psychology/self-test-pressure",
  "clicks": [
    "for(var i=0;i<PSS_QS.length;i++){PSS_ANS[i]=3;}calc();"
  ],
  "expect": [
    "22 / 40",
    "压力负荷 55%"
  ],
  "ref": "PSS 10 题、量表 0–4，其中 4 题为反向题（计分 4−3=1）⇒ 总分 = 3×6 + 1×4 = 22（满分 40），≤26 ⇒ 较高压力；pct=round(22/40*100)=55%"
},
{
  "slug": "psychology/calc-self-assess",
  "clicks": [
    "for(var i=0;i<LR_QS.length;i++){LR_ANS[i]=3;}calc();"
  ],
  "expect": [
    "20 / 30",
    "乐观指数 67%"
  ],
  "ref": "LOT-R 乐观量表 6 题；计分 v=选项+1=4，其中 2 题反向（6−4=2）⇒ 4×4+2×2=20（满分 30），≥18 ⇒ 中等乐观；pct=round(20/30*100)=67%"
},
{
  "slug": "psychology/rater",
  "clicks": [
    "for(var i=0;i<PSQI_ITEMS.length;i++){PSQI_ANS[i]=3;}calc();"
  ],
  "expect": [
    "21 / 21",
    "睡眠质量指数 100%"
  ],
  "ref": "PSQI 睡眠量表 7 题、每题 0–3（满分 21）；全选 3 ⇒ 总分 21 ⇒ >15 ⇒ 睡眠质量很差；pct=round(21/21*100)=100%。默认态未作答不命中"
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
  console.log("==== psychology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
