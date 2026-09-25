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
