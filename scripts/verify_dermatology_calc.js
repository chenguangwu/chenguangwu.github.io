#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原为 no_inputs 弱用例：expect「5-氟尿嘧啶(5-FU)乳膏」只在默认 1 级（轻度）分支出现，与输入无关。
  "slug": "dermatology/actinic-keratosis",
  "checkIds": [
    "r1",
    "r2"
  ],
  "expect": [
    "存在高危特征（快速增大、出血/溃疡）",
    "高危特征： 快速增大、出血/溃疡（已加4分）"
  ],
  "ref": "勾选 r1(快速增大)+r2(出血/溃疡) → isHighRisk=true → grade「高危病变」、恶变风险 >10%/年，并输出「存在高危特征（快速增大、出血/溃疡）」与「已加4分」。回退默认（四项均未勾选）→ 走 1/2/3 级分支，两串均不命中。"
},
{
  "slug": "dermatology/assessor-14",
  "inputs": {},
  "expect": [
    "12"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/calc-1",
  "inputs": {
    "age": "45",
    "head": "9",
    "armR": "9",
    "armL": "9",
    "front": "18",
    "back": "18",
    "legR": "18",
    "legL": "18",
    "perineum": "1"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/chilblain-grading",
  "inputs": {},
  "expect": [
    "瘙痒可外用弱效激素短程"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/contact-dermatitis-patch",
  "inputs": {},
  "expect": [
    "请点击选择阳性的过敏原及反应强度"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/dermatoscopy-abcd",
  "inputs": {
    "borderScore": "7"
  },
  "expect": [
    "0.70"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/easi-eczema",
  "inputs": {
    "age": "child"
  },
  "expect": [
    "0.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/gags-acne",
  "inputs": {
    "loc0": "1"
  },
  "expect": [
    "前额"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/hdss-hyperhidrosis",
  "inputs": {},
  "expect": [
    "推荐外用20%氯化铝溶液"
  ],
  "ref": "auto-restore(default)"
},
{
  // 原为 no_inputs 弱用例：expect「局部冷敷15-20分钟」只在默认总分 ≤5（轻度）分支出现。
  "slug": "dermatology/insect-bite-reaction",
  "inputs": {
    "insectType": "bee"
  },
  "checkIds": [
    "sys1",
    "sys2",
    "sys3"
  ],
  "expect": [
    "发热、淋巴结肿大、全身皮疹",
    "蜂蜇伤特别注意"
  ],
  "ref": "勾选 sys1/2/3 → sysSymptoms 依次为 发热、淋巴结肿大、全身皮疹，sysScore=6 并输出「发热、淋巴结肿大、全身皮疹（已加6分）」；insectType=bee → 输出蜂蜇伤专属提示。回退默认（三项均未勾选、insectType=蚊虫）→ 两串均不命中。"
},
{
  "slug": "dermatology/leprosy-grading",
  "inputs": {
    "leprosyType": "BT"
  },
  "expect": [
    "界限类偏结核样型(BT)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/miliaria-classification",
  "inputs": {},
  "expect": [
    "脱离高温环境后1-2天内水疱干涸脱屑自愈"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/onychomycosis-grading",
  "inputs": {
    "hyphae": "1"
  },
  "expect": [
    "坚持3-6个月"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/pasi-score",
  "inputs": {},
  "expect": [
    "头颈(×0.1)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/pityriasis-rosea",
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/rater-28",
  "inputs": {},
  "expect": [
    "14"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/salt-alopecia",
  "inputs": {
    "top": "75",
    "back": "0",
    "right": "0",
    "left": "0"
  },
  "expect": [
    "30%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/scorad-index",
  "inputs": {
    "area": "30",
    "c1": "5",
    "c2": "3"
  },
  "expect": [
    "14.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/seborrheic-dermatitis",
  "inputs": {},
  "expect": [
    "使用含2%酮康唑"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/vasi-vitiligo",
  "inputs": {
    "r1_u": "7",
    "r1_d": "100",
    "r2_u": "0",
    "r2_d": "100",
    "r3_u": "0",
    "r3_d": "100",
    "r4_u": "0",
    "r4_d": "100",
    "r5_u": "0",
    "r5_d": "100"
  },
  "expect": [
    "7.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/vss-scar",
  "inputs": {},
  "expect": [
    "色素(0-2)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/wood-lamp",
  "inputs": {},
  "expect": [
    "颜色加深/对比增强"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dermatology/zoster-phn",
  "inputs": {},
  "expect": [
    "72小时内抗病毒治疗"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== dermatology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
