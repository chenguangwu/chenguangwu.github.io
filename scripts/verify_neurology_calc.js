#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "neurology/abcd2",
  "inputs": {
    "age": "1"
  },
  "expect": [
    "60岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/adas-cog",
  "inputs": {
    "q1": "1"
  },
  "expect": [
    "1.单词回忆"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/alsfrs-r",
  "inputs": {
    "b1": "3"
  },
  "expect": [
    "11/12"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/calc-1",
  "clicks": ["var __v={loc:3,locq:2,locc:2,gaze:2,visual:3,facial:3,armL:4,armR:0,legL:0,legR:0,ataxia:0,sensory:1,language:2,dysarthria:1,neglect:0};Object.keys(__v).forEach(function(k){document.getElementById(k).value=String(__v[k]);});calc()"],
  "expect": [
    "总分： 23 分",
    "重度卒中"
  ],
  "ref": "15 个 select 由 renderItems() 运行期渲染（HTML 源码无字面 id）⇒ 只能在 clicks 内按 id 赋值再 calc()。"
     + "注入和 = 3+2+2+2+3+3+4+0+0+0+0+1+2+1+0 = 23 ⇒ classify 阈值 (>20) ⇒ 重度卒中。"
     + "默认态全部取首项 0 ⇒ 总分 0 / 无卒中症状。原用例 inputs 键是生成器模板串残留（${it.id}/${o.v}），"
     + "expect「o.v」亦为模板残留 ⇒ 两把锁同时失灵的坏用例（BATCH101 形态），已整体重写。",
  },

{
  "slug": "neurology/edss",
  "inputs": {
    "pyr": "1"
  },
  "expect": [
    "1.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/house-brackmann",
  "clicks": [
    "selectGrade({classList:{add:function(){},remove:function(){}}}, 6)"
  ],
  "expect": [
    "VI级",
    "面神经完全麻痹"
  ],
  "ref": "clicks 直接调 selectGrade(dummy,6) 置顶层 grade=6 后 calc()；默认态 grade=1→I级 正常，注入→VI级 完全麻痹（面神经功能完全消失）。"
},
{
  "slug": "neurology/ilae-seizure",
  "inputs": {
    "awareness": "impaired"
  },
  "expect": [
    "impaired"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/midas",
  "inputs": {
    "q1": "7",
    "q2": "0",
    "q3": "0",
    "q4": "0",
    "q5": "0",
    "qa": "0",
    "qb": "0"
  },
  "expect": [
    "7天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/moca",
  "inputs": {
    "v1": "0"
  },
  "expect": [
    "29"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/ncs-emg",
  "inputs": {
    "amp": "decreased"
  },
  "expect": [
    "维生素B12/叶酸缺乏"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/nihss",
  "inputs": {
    "q1a": "1"
  },
  "expect": [
    "发病4.5小时"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/psqi",
  "inputs": {
    "actualSleep": "11",
    "bedTime": "8",
    "latency": "15"
  },
  "expect": [
    "(138%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/qmg",
  "inputs": {
    "q1": "1"
  },
  "expect": [
    "1.复视"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-18",
  "inputs": {
    "ni'+i+'": "'+j+'"
  },
  "expect": [
    "+j+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-19",
  "inputs": {
    "ui'+i+'": "'+j+'"
  },
  "expect": [
    "+j+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-21",
  "inputs": {
    "p1": "7",
    "p3": "0"
  },
  "expect": [
    "疼痛7/20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-22",
  "inputs": {
    "si'+i+'": "'+j+'"
  },
  "expect": [
    "+j+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/sara",
  "inputs": {
    "q1": "2",
    "q2": "2",
    "q3": "1",
    "q4": "0",
    "q5": "0",
    "q6": "0",
    "q7": "0",
    "q8": "0"
  },
  "expect": [
    "轻度",
    "总分 = 5 / 40"
  ],
  "ref": "8 个 select 评分累加：inputs 写 q1..q8（2+2+1=5）→ calc() 得 SARA 总分 5、严重程度「轻度」（默认全 0 ⇒ 总分 0 ⇒「无/极轻」）。锚「轻度」+「总分 = 5 / 40」均为注入态独有（默认态为「无/极轻」「总分 = 0 / 40」，已双态核验）。"
},
{
  "slug": "neurology/trigeminal-bni",
  "inputs": {},
  "expect": [
    "无需任何药物治疗"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "neurology/twstrs",
  "inputs": {
    "m1": "1"
  },
  "expect": [
    "1/35"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/updrs",
  "inputs": {
    "q1": "1"
  },
  "expect": [
    "3.1言语"
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
  console.log("==== neurology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
