#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "psychology/attachment-style-test",
  "clicks": ["applyAttachPreset('secure')"],
  "expect": ["焦虑 2.00 · 回避 2.00"],
  "ref": "页面自带预设入口 applyAttachPreset('secure')：36 题按维度填 2 分（反向题填 6 分）⇒ computeScores 焦虑/回避两维均值均为 2.00 ⇒ classify=安全型，结果区渲染「焦虑 2.00 · 回避 2.00」及安全型解读。"
       + "默认态 state 全 0、结果区为空，零交集。原用例把模板串 at' + i + '_' + l.v 当 input id（题干与选项由 renderQuiz 的 innerHTML 生成，桩不登记），属桩盲区；现改为页面真实预设按钮入口。"
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
    "【幸福感指数（10 维度自评）】 结果：幸福感总分 90/100（10 维度平均 9.0）→ 等级：很高；最短板 生活满意度 0 分、最强项 身心健康 10 分；较常模(62)+28"
  ],
  "ref": "inputs 写 10 个滑杆（id=s-<维度键>）：life=0、其余=10 ⇒ getScores 求和 90 ⇒ level(90)='很高'；min=0 落在 life、max=10 落在 health。"
       + "【已修逃生项】原首锚「最短板：生活满意度（0 分）」在注入失败时仍命中：滑杆由 buildSliders() 用 innerHTML 动态生成，桩不解析 innerHTML，"
       + "getElementById('s-*') 落空 → parseInt('')||0 = 0，10 维全 0 ⇒ 最短板恰好也是生活满意度 0 分。"
       + "（原 ref 假设默认 DEFAULTS 生效取 61 分，与实际桩行为不符。）现只保留整条 EMR 结果串，含「幸福感总分 90/100」，"
       + "注入失败态为 0/100，零交集。"
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
    "拖延程度 75%",
    "【拖延症程度评估（近 2 周自评）】 结果：拖延总分 30/40（拖延程度 75%）→ 分级：中度拖延；10 题全部作答"
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
    "18 / 30",
    "乐观指数 60%",
    "【乐观倾向自评（LOT 类量表）】 结果：乐观总分 18/30（乐观指数 60%）→ 分级：中等乐观；6 题全部作答（含反向计分题）"
  ],
  "ref": "LOT-R 乐观量表 6 题（3 乐观 + 3 悲观）；计分 v=选项+1=4，其中 3 题反向（6−4=2）⇒ 3×4+3×2=18（满分 30），≥18 ⇒ 中等乐观；pct=round(18/30*100)=60%"
},
{
  "slug": "psychology/rater",
  "clicks": [
    "for(var i=0;i<PSQI_ITEMS.length;i++){PSQI_ANS[i]=3;}calc();"
  ],
  "expect": [
    "21 / 21",
    "睡眠质量指数 100%",
    "【睡眠质量评分（PSQI 简化版 · 7 项）】 结果：PSQI 简化版总分 21/21（睡眠质量指数 100%）→ 分级：睡眠质量很差；7 项全部作答"
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
},
{
  "slug": "psychology/self-assess",
  "clicks": [
    "for(var i=0;i<EQ_QS.length;i++){EQ_ANS[i]=3;}calc();"
  ],
  "expect": [
    "【情商（EQ）自评 · Goleman 五要素】 结果：EQ 总分 80/100（80%）→ 分级：高情商；五维度得分 自我认知:16/优秀、自我管理:16/优秀、自我激励:16/优秀、同理心:16/优秀、社交技能:16/优秀"
  ],
  "ref": "EQ 20 题分 5 维度（每维度 4 题、0–4 分 ⇒ 维度满分 20、总分 100）；全选 3（计分 v=选项+1=4）⇒ 每维度 16 分、总分 80 ≥80 ⇒「高情商」；维度分 ≥16 判定「优秀」，5 个维度全部优秀。默认态 EQ_ANS 全 null ⇒ 只输出未作答提示，零交集。"
},
{
  "slug": "psychology/bubble-tea-personality-quiz",
  "clicks": ["document.getElementById('btCard').toBlob=function(){throw new Error('boom')};document.getElementById('btPngBtn').fire('click');"],
  "expect": ["导出失败：Error"],
  "ref": "失败注入：结果卡 toBlob 必抛 Error ⇒ 导出入口必须 toast「导出失败：Error」并终止。修复前异常裸冒成 pageerror、且成功提示「已导出 PNG」仍会执行（给出错误事实）；默认态无该串 ⇒ 判别明确。"
},
{
  "slug": "psychology/enneagram-test",
  "clicks": ["document.getElementById('enCardCanvas').toBlob=function(){throw new Error('boom')};document.getElementById('enPngBtn').fire('click');"],
  "expect": ["导出失败：Error"],
  "ref": "失败注入：结果卡 toBlob 必抛 Error ⇒ 导出入口必须 toast「导出失败：Error」并终止。修复前异常裸冒成 pageerror、且成功提示「已导出结果卡 PNG」仍会执行；默认态无该串 ⇒ 判别明确。"
},
{
  "slug": "psychology/tester-3",
  "clicks": [
    "pJump(0)", "pPick(0)", "pJump(1)", "pPick(0)", "pJump(2)", "pPick(0)",
    "pJump(3)", "pPick(0)", "pJump(4)", "pPick(0)", "pJump(5)", "pPick(0)",
    "pJump(6)", "pPick(0)", "pJump(7)", "pPick(0)", "pJump(8)", "pPick(0)",
    "pJump(9)", "pPick(0)", "pJump(10)", "pPick(0)", "pJump(11)", "pPick(0)"
  ],
  "expect": ["你的主导学习风格：V", "12 / 12（100%）"],
  "ref": "VARK 12 题全选第 1 项（视觉）⇒ V=12、总分 12/12=100%，主导 V。默认仅未答提示（0/12），零交集。"
},
{
  "slug": "psychology/analysis-2",
  "clicks": ["for(var i=0;i<24;i++){pPick(0);}"],
  "expect": ["红色 · 活泼热情", "24 / 24（100%）"],
  "ref": "FPA 四色人格 24 题，每题第 1 项对应红色。全选第 1 项 ⇒ 红 24、总分 24 ⇒ 占比渲染「24 / 24（100%）」，主导色「红色 · 活泼热情」。"
       + "pPick 内 setTimeout 由桩立即执行，逐题推进到第 24 题后 calc()。默认态未作答、结果区为空，零交集。"
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
