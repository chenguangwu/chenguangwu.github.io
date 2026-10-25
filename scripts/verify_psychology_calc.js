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
    "总分 27（0–27）",
    "【PHQ-9 抑郁自评（患者健康问卷）】 结果：PHQ-9 总分 27/27 → 抑郁程度：重度；第 9 条目（自伤念头）3 分（9 题全部作答）"
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
    "压力负荷 55%",
    "【知觉压力量表（PSS-10）】 结果：PSS-10 总分 22/40（压力负荷 55%）→ 压力分级：较高压力；10 题全部作答（含 4 道反向计分题）"
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
},
{
  "slug": "psychology/psqi-assessment",
  "clicks": [
    "PSQI_ANS.qual=3;PSQI_ANS.latM=90;PSQI_ANS.latF=3;PSQI_ANS.hours=5;PSQI_ANS.bed='23:00';PSQI_ANS.wake='05:00';PSQI_ANS.d1=3;PSQI_ANS.d2=3;PSQI_ANS.d3=3;PSQI_ANS.d4=3;PSQI_ANS.d5=3;PSQI_ANS.d6=3;PSQI_ANS.d7=3;PSQI_ANS.med=3;PSQI_ANS.day1=3;PSQI_ANS.day2=3;calc()"
  ],
  "expect": [
    "【匹兹堡睡眠质量指数（PSQI）】 结果：PSQI 全局分 18/21 → 睡眠质量：严重睡眠问题；7 成分得分 主观质量 3、入睡时长 3、睡眠时长 2、睡眠效率 1、睡眠障碍 3、助眠药物 3、日间功能 3（各 0–3）"
  ],
  "ref": "步进向导页（PSQI_STEPS，答案存 PSQI_ANS 对象）。注入：主观质量 3、入睡>60 分钟(latM=90→latMlvl=3)、入睡频次 3 ⇒ c2=max(3,3)=3；卧床 5 小时 ⇒ c3=2；23:00–05:00 卧床 6 小时、睡眠 5 小时 ⇒ 效率 83% ⇒ c4=1；7 个困扰条目各 3（dsum=21）⇒ c5=3；用药 3 ⇒ c6=3；日间各 3 ⇒ c7=3。合计 3+3+2+1+3+3+3=18 >15 ⇒「严重睡眠问题」。默认态 PSQI_ANS 空 ⇒ 只输出未作答提示，零交集。"
},
{
  "slug": "psychology/sas-assessment",
  "clicks": [
    "for(var i=0;i<SAS_ANS.length;i++)SAS_ANS[i]=4;calc()"
  ],
  "expect": [
    "【Zung 焦虑自评量表（SAS）】 结果：SAS 粗分 65/80 → 标准分 81/100 → 分级：重度焦虑；高分条目 15 项（≥3 分表示该症状近期明显）"
  ],
  "ref": "SAS 20 题 1–4 分、含 5 道反向题（SAS_REV[i] 为真时计 5−v）。全部填 4 ⇒ 非反向 15 题各 4 分 + 反向 5 题各 1 分 = 65 粗分；标准分 round(65×1.25)=81 ≥70 ⇒「重度焦虑」；sig≥3 的条目恰为 15 个非反向题。默认态 SAS_ANS 全 null ⇒ 只输出未作答提示，零交集。"
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

  console.log("==== psychology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
