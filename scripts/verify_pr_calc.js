#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pr/analysis-6",
  "inputs": {
    "txt": "入手三天就出现卡顿和失灵，客服态度敷衍，物流还延误了两天，申请退款也拖沓，体验很差，完全不值这个价格。"
  },
  "expect": [
    "-100.00",
    "17.78"
  ],
  "ref": "情感词频：总词量 45、负向命中 8 次且无正向命中 → 极性指数 −100.00%，情感词密度 8÷45=17.78%（默认正向文本为 +100.00%/16.67%，注入失败即不命中）"
},
{
  "slug": "pr/analysis-assessor",
  "inputs": { "data": "冠名权益,800000,300000\n现场展位,250000,120000\n媒体曝光,420000,150000\n社交传播,180000,60000" },
  "expect": [
    "媒体价值合计： 1650000.00",
    "投入合计： 630000.00",
    "赞助 ROI： 161.90%"
  ],
  "ref": "媒体价值 800000+250000+420000+180000=1650000；投入 300000+120000+150000+60000=630000；ROI=(1650000−630000)/630000=161.90%（默认两项 400000/210000/90.48%，避开；价值最高项默认与测试同为冠名权益，故不作断言）"
},
{
  "slug": "pr/analysis-density-1",
  "inputs": {
    "text": "人工智能助力医疗影像诊断，人工智能提升基层问诊效率，技术在药物研发中发挥作用。",
    "kw": "人工智能"
  },
  "expect": [
    "5.56",
    "出现 2 次"
  ],
  "ref": "关键词密度：正文中文字符 36 个、英文单词 0 个，总词数 36；关键词「人工智能」出现 2 次，密度=2÷36=5.56%（独立复算；默认正文绿色低碳出现 3 次/密度 3.45%、Smart Manufacturing 出现 1 次，注入失败即不命中）"
},
{
  "slug": "pr/assessor-56",
  "inputs": {
    "a1": "4"
  },
  "expect": [
    "97%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-57",
  "inputs": {
    "a1": "4"
  },
  "expect": [
    "96%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-58",
  "inputs": {
    "k1": "15",
    "k6": "5",
    "k7": "100"
  },
  "expect": [
    "0.33元"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-59",
  "inputs": {
    "p1": "75",
    "p2": "10",
    "p3": "100"
  },
  "expect": [
    "13%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-manager-2",
  "inputs": {
    "r1": "4"
  },
  "expect": [
    "96%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-risk",
  "inputs": {
    "s1": "5", "i1": "4", "s2": "1", "i2": "1", "s3": "1", "i3": "1", "s4": "1", "i4": "1", "s5": "1", "i5": "1"
  },
  "clicks": ["calc();"],
  "expect": [
    "极高风险",
    "高风险项数： 1 / 5"
  ],
  "ref": "非默认输入：s1=5,i1=4→r=20≥16 极高风险、highCount=1；其余四组=1 低风险。页面 onchange 触发 calc 但 harness 不自动跑，clicks 显式调一次。默认全 1→低风险、「高风险项数： 0 / 5」，故「高风险项数： 1 / 5」可区分。"
},
{
  "slug": "pr/media-invite",
  "inputs": {
    "mediaType": "paper"
  },
  "expect": [
    "paper"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/press-conference",
  "inputs": {
    "startTime": "14:00",
    "eventType": "press"
  },
  "expect": [
    "85"
  ],
  "ref": "auto-restore → 收紧：eventType=press 时 7 环节总时长 85 分（默认 product 为 135 分）。原 expect「25」取环节单行时长，回退默认仍可命中（逃生项），改锚定总时长「85」（product 为 135 → 失配）。"
},
{
  "slug": "pr/risk-assessment",
  "inputs": {
    "riskName": "供应链中断",
    "riskProb": "4",
    "riskImpact": "5"
  },
  "clicks": ["addRisk()"],
  "expect": [
    "平均风险值： 20.0",
    "（极高风险）",
    "1 高/极高"
  ],
  "ref": "风险值=概率×影响=4×5=20 ⇒ 极高风险；仅 1 项 ⇒ 平均=20.0。"
     + "原 expect「(12)」出自 loadSample 样本项（P:3 I:4），默认态列表为空、走兜底 addRisk() 也会命中 ⇒ 逃生项。"
     + "注：兜底阶段无参 addRisk() 会再追加一项，故断言须落在 click 阶段产物（已实测默认态 FAIL）。"
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
  console.log("==== pr calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
