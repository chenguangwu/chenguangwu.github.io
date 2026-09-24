#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "edu2/exam-analysis",
  "inputs": {
    "fullScore": "120",
    "passLine": "50",
    "excellentLine": "80",
    "scoreInput": "甲,108\n乙,96\n丙,90\n丁,72\n戊,60"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "85.2 平均分",
    "17.14 标准差",
    "100.0% 及格率"
  ],
  "ref": "满分 120 / 及格线 50% / 优秀线 80% ⇒ 及格分 60、优秀分 96；5 人 108/96/90/72/60 ⇒ 均值 426/5=85.2、标准差 √(1468.8/5)=17.14、及格 5/5=100.0%、优秀 2/5=40.0%（独立复算）。默认走 loadSample 15 人（74.9 / 14.24 / 80.0%）⇒ 三个锚点全不命中。原 expect「不及格」由 loadSample 兜底渲染的等级词产出（常量）⇒ 已替换。**注意不锚 40.0%** —— 该串在默认兜底段（60% 以下 6/15）同样出现，无判别力。"
},
{
  "slug": "edu2/exam-countdown",
  "inputs": {
    "examName": "高考_X"
  },
  "expect": [
    "高考_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "edu2/schedule-conflict",
  "inputs": {
    "courseInput": "物理,王老师,D401,2,1,2\n化学,王老师,E502,2,1,2\n生物,赵老师,D401,2,1,2\n历史,孙老师,F603,4,1,2"
  },
  "clicks": [
    "detect()"
  ],
  "expect": [
    "物理（D401） 化学（E502）",
    "D401 物理（王老师） 生物（赵老师）"
  ],
  "ref": "4 条课程两两比对：物理·化学 同为周二第 1-2 节且同教师王老师 ⇒ 教师冲突 1；物理·生物 同为周二第 1-2 节且同教室 D401 ⇒ 教室冲突 1；历史在周四 ⇒ 无冲突（独立复算）。默认走 loadSample 8 条（0/0/无冲突）⇒ 两个锚点不命中；且样本课程名与锚点无交集（样本含「物理,王老师,A101」但无全角括号写法）⇒ 原 expect「A101」是 sample 文本常量 ⇒ 已替换。"
},
{
  "slug": "edu2/wrong-book",
  "inputs": {
    "filterStatus": "pending"
  },
  "clicks": [
    "data=[{id:'w1',subject:'数学',type:'选择题',question:'函数定义域求解',reason:'粗心',answer:'x>0',status:'pending',created:'2026-09-01',reviewDate:'2026-09-30'},{id:'w2',subject:'英语',type:'完形填空',question:'词义辨析',reason:'词汇量不足',answer:'选B',status:'mastered',created:'2026-09-05',reviewDate:'2026-09-25'},{id:'w3',subject:'数学',type:'解答题',question:'导数应用求极值',reason:'概念不清',answer:'先求导',status:'reviewing',created:'2026-09-10',reviewDate:'2026-09-28'}];render()"
  ],
  "expect": [
    "数学（1 题）",
    "函数定义域求解",
    "解析：x>0"
  ],
  "ref": "顶层 var data 用 clicks 覆写三条（pending / reviewing / mastered 各一）+ filterStatus=pending（非默认「全部状态」）⇒ filtered 只剩 1 条 ⇒ 列表渲染「数学（1 题）」与题目、解析文本（独立复算：bySubject 按 filtered 分组）。默认 data 为空、filterStatus 为空 ⇒ 只渲染「暂无错题…」（0 错题总数）⇒ 三个锚点全不命中。原 expect「pending」是 fStatus 下拉的 option value 常量 ⇒ 已替换。**不锚 dueCount 与「剩 N 天」** —— 依赖运行日、日期一变即失效。注：兜底阶段无参调用 loadData() 会用桩 getItem(null) 清空 data，但 expect 在阶段 2 已判定（同 BATCH103 的 assessor-risk-8）。"
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
  console.log("==== edu2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
