#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "clinical-nursing/assessor-pressure-risk",
  "inputs": {
    "duration": "6",
    "bmi": "22",
    "age": "55"
  },
  "expect": [
    "6h"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/assessor-rater-risk",
  "inputs": {
    "m1": "15"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/bag-valve-mask",
  "inputs": {
    "ageGroup": "child"
  },
  "expect": [
    "200-300"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/barthel-index",
  "clicks": [
    "scores.eating=0;scores.bathing=0;scores.grooming=0;scores.dressing=0;scores.bowels=5;scores.bladder=5;scores.toilet=5;scores.transfer=10;scores.walking=10;scores.stairs=5;renderItems();calc()"
  ],
  "expect": [
    "40",
    "大部分ADL需他人帮助，建议加强护理，预防并发症"
  ],
  "ref": "静态量表页(无input)：clicks 页面作用域直写 scores 十项=40 分，落「≥25 重度依赖」分支专属 desc（默认 100 分走「完全自理」、零参兜底 scores[undefined]=undefined→total=NaN 走 else 亦为另一分支，两者均不含该串）。"
},
{
  "slug": "clinical-nursing/braden-score",
  "clicks": [
    "selectScore('sensory',2);selectScore('moisture',2);selectScore('activity',2);selectScore('mobility',2);selectScore('nutrition',2);selectScore('friction',3)"
  ],
  "expect": [
    "每2小时翻身一次"
  ],
  "ref": "静态按钮量表页：逐维 selectScore 到 total=2*5+3=13 落「中度风险(13-14)」分支，其 desc 独有串「每2小时翻身一次」。默认 total=23 走「无风险」；零参兜底 scores[undefined]=undefined→total=NaN 走 else「极度风险」(每1小时翻身)，两态均不含该串（故非逃生项）。"
},
{
  "slug": "clinical-nursing/calc-rater-risk",
  "inputs": {
    "b1": "3"
  },
  "expect": [
    "22"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/chest-compression-depth",
  "inputs": {
    "bodyType": "thin"
  },
  "expect": [
    "瘦弱患者注意控制力度"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/cold-compress-timer",
  "inputs": {
    "sensitivity": "sensitive"
  },
  "expect": [
    "14分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/convert-flow-concentration",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/cvc-maintenance",
  "inputs": {
    "cathVol": "4.5",
    "extraFlush": "2"
  },
  "expect": [
    "4.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/cycle-7",
  "inputs": {
    "ptInput": "12床 李四",
    "startInput": "2026-09-24T08:30"
  },
  "clicks": [
    "selectedType='腕部约束';startRestraint()"
  ],
  "expect": [
    "12床 李四",
    "已约束时长（2小时松解提醒）"
  ],
  "ref": "约束计时页：inputs 写入患者名与开始时间(非默认空值)，clicks 选约束类型后 startRestraint() 渲染进行中卡片。默认无进行中约束。"
},
{
  "slug": "clinical-nursing/fall-emergency-flow",
  "clicks": [
    "toggleStep(0);toggleStep(1);toggleStep(2);toggleStep(3);toggleStep(4)"
  ],
  "expect": [
    "5/8"
  ],
  "ref": "静态步骤勾选页：连续 toggleStep 前 5 步，进度文本由 completedSteps.length 派生为 5/8。默认 0/8；零参兜底 completedSteps 不变。"
},
{
  "slug": "clinical-nursing/gastric-tube-depth",
  "inputs": {
    "noseEar": "27",
    "earXiphoid": "25",
    "height": "170",
    "noseXiphoid": "43"
  },
  "expect": [
    "27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/generator-pressure",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/iv-drip-rate",
  "inputs": {
    "volume": "750",
    "hours": "4",
    "minutes": "0"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/morse-score",
  "clicks": [
    "selectScore('history',25);selectScore('gait',10)"
  ],
  "expect": [
    "保持病区环境安全"
  ],
  "ref": "静态按钮量表页：selectScore 到 total=25+10=35 落「低度跌倒风险(25-50)」分支，其 desc 独有串「保持病区环境安全」。默认全 0 走「无跌倒风险」；零参兜底 total=NaN 落 else「高度跌倒风险」，两态均不含该串。"
},
{
  "slug": "clinical-nursing/ostomy-bag-timing",
  "inputs": {
    "stomaType": "ileostomy"
  },
  "expect": [
    "ileostomy"
  ],
  "ref": "回肠造口(stomaType=ileostomy) 更换周期 5天；默认 colostomy 为 7天。「正常更换周期」两型都含（原逃生项），改锚定随输入变化的类型值 ileostomy（回退默认 colostomy 不出现）。"
},
{
  "slug": "clinical-nursing/oxygen-concentration",
  "inputs": {
    "flowRate": "5"
  },
  "expect": [
    "鼻导管5L/min对应FiO2约41%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/pain-nrs",
  "clicks": [
    "selectPain(2)"
  ],
  "expect": [
    "可考虑非药物干预"
  ],
  "ref": "NRS 面部表情点击页：selectPain(2) 落 getLevel 返回「轻度疼痛」分支，其 desc 独有串「可考虑非药物干预」。默认 selectPain(0) 走「无痛」；零参兜底 getLevel(undefined) 因 undefined<=各 max 均 false 返回 labels[last]「重度疼痛」，两态均不含该串。"
},
{
  "slug": "clinical-nursing/pressure-injury-description",
  "inputs": {
    "woundL": "6",
    "woundW": "2",
    "woundD": "0"
  },
  "expect": [
    "6cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/reminder-time-1",
  "inputs": {
    "coldDur": "30",
    "restDur": "30",
    "checkDur": "5"
  },
  "expect": [
    "30.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/restraint-check",
  "inputs": {
    "restraintSite": "ankle"
  },
  "expect": [
    "按压足趾甲床后颜色恢复"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/restraint-duration",
  "inputs": {
    "startTime": "08:00",
    "totalHours": "7"
  },
  "expect": [
    "14"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/suction-pressure",
  "inputs": {
    "currentPressure": "90"
  },
  "clicks": [
    "currentAge='newborn';checkPressure()"
  ],
  "expect": [
    "当前压力 90 mmHg 超过安全范围（60-80mmHg），有黏膜损伤风险！"
  ],
  "ref": "吸痰负压校验页：inputs 写 90mmHg(非默认)，clicks 切 currentAge='newborn' 后 checkPressure() 走新生儿安全区间(60-80mmHg)越界分支。默认 adult 区间不同。"
},
{
  "slug": "clinical-nursing/surgical-position-risk",
  "clicks": [
    "selectPosition('lithotomy',{classList:{add:function(){}}})"
  ],
  "expect": [
    "截石位压力点评估",
    "腘窝血管神经丰富，避免腿架直接压迫"
  ],
  "ref": "静态体位卡片页：selectPosition('lithotomy', btn) 需第二参 btn(classList) 否则抛错，故传哑对象；输出该体位专属标题与压力点。默认初始化走 supine(平卧位)。"
},
{
  "slug": "clinical-nursing/tracheostomy-dressing",
  "inputs": {
    "firstDressing": "08:00_X"
  },
  "expect": [
    "00_X"
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
  console.log("==== clinical-nursing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
