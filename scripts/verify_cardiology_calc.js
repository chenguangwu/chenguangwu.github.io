#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": {
    "avg24_sbp": "213",
    "avg24_dbp": "88",
    "day_sbp": "150",
    "day_dbp": "92",
    "night_sbp": "128",
    "night_dbp": "78",
    "lowest_sbp": "120",
    "morning_sbp": "165"
  },
  "expect": [
    "213/88"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/antiarrhythmic-class",
  "inputs": {},
  "expect": [
    "显著减慢0相上升速度和传导"
  ],
  "ref": "auto-restore(default)"
},
{
  // 原用例 inputs 为空、expect 取「非复杂型Stanford B型」—— 那是建立在**旧 harness 失真**上的：
  // extent 组真机默认选中 ascDesc（HTML checked），旧桩 getElementsByName 恒 [] ⇒ getRadio 返回 0
  // ⇒ 被当成「非升主动脉受累」而落入 B 型。2026-09-24 起 harness 回落 HTML 默认选中态，
  // 真机默认（extent=ascDesc）实为 **A 型**（急诊外科手术），故原 expect 已不成立。
  // 现改为显式声明输入（不再受默认态影响）：extent=descOnly → B 型；malPerf=1 → 复杂型 →
  // 紧急 TEVAR（默认态 A 型输出「急诊外科手术」，故本 expect 具判别力）。
  "slug": "cardiology/aortic-dissection",
  "radios": {
    "extent": "descOnly"
  },
  "checkIds": [
    "malPerf"
  ],
  "expect": [
    "紧急TEVAR(腔内修复)",
    "复杂型Stanford B型夹层"
  ],
  "ref": "extent=descOnly（仅降主动脉）→ Stanford B 型 / DeBakey IIIa；malPerf=脏器灌注不良 → complicated → 紧急 TEVAR 腔内修复"
},
{
  "slug": "cardiology/aspirin-prevention",
  "inputs": {
    "age": "83",
    "ascvd": "12"
  },
  "expect": [
    "83岁"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例（空输入只能断言提示语，零判别力）。
  "slug": "cardiology/calc-1",
  "inputs": {
    "sbp": "150",
    "dbp": "95"
  },
  "checkIds": [
    "diabetes"
  ],
  "expect": [
    "1级高血压（轻度）",
    "高危 / 很高危"
  ],
  "ref": "classifyBP(150,95) → 1级高血压（轻度）（收缩压140-159 或 舒张压90-99）；riskLayer 见 diabetes=true → 「高危 / 很高危」（糖尿病/靶器官损害/确诊CVD 任一即高危）。回退默认（空输入）→ 仅提示「请输入有效的收缩压和舒张压」；不勾选 → 低危。两串均不命中。"
},
{
  "slug": "cardiology/calc-3",
  "inputs": {
    "age": "2"
  },
  "expect": [
    "2.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/cardiac-rehab-mets",
  "inputs": {
    "mets": "8",
    "weight": "70"
  },
  "expect": [
    "1960"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/chads2-vasc",
  "inputs": {
    "sex": "f"
  },
  "expect": [
    "女性单独1分不增加卒中风险"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/ckd-epi",
  "inputs": {
    "age": "98",
    "scr": "1.3",
    "uacr": "80"
  },
  "expect": [
    "ACEI/ARB/SGLT2i治疗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "age": "93",
    "cacs": "280"
  },
  "expect": [
    "93岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/cpet-analysis",
  "inputs": {
    "peakVO2": "20.5",
    "at": "9.5",
    "veVco2": "34",
    "rer": "1.12",
    "pctPred": "58"
  },
  "expect": [
    "20.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/echo-report",
  "inputs": {
    "lvef": "72",
    "lvesv": "55",
    "lvidd": "56",
    "la": "42",
    "ao": "32",
    "rv": "22",
    "ea": "0.8",
    "eprime": "6"
  },
  "expect": [
    "72%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/grace-score",
  "inputs": {
    "age": "102",
    "hr": "95",
    "sbp": "130",
    "cr": "1.2"
  },
  "expect": [
    "72小时内冠脉造影"
  ],
  "ref": "auto-restore"
},
{
  // radios 注入单选组（htn=1 高血压、stroke=1 卒中史），checkIds 注入复选（drugs 合并抗血小板/NSAIDs、
  // alcohol 酗酒）→ 1+1+1+1 = 4 分 → 高危、出血风险 8.70%。
  // 原用例 inputs 为空、expect 取默认态 "1.13%"（0 分低危）⇒ 零判别力，已去默认化。
  "slug": "cardiology/has-bled",
  "radios": {
    "htn": "1",
    "stroke": "1"
  },
  "checkIds": [
    "drugs",
    "alcohol"
  ],
  "expect": [
    "8.70%"
  ],
  "ref": "HAS-BLED 九项各 1 分：高血压 1 + 卒中史 1 + 合并抗血小板/NSAIDs 1 + 酗酒 1 = 4 分 → 高危（出血风险 8.70%）"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": {
    "pvcTotal": "12750",
    "pvcHr": "520",
    "vtBeats": "0",
    "vtSec": "0"
  },
  "expect": [
    "12750/100000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/hypertension-jnc",
  "inputs": {
    "sbp": "233",
    "dbp": "95"
  },
  "expect": [
    "233/95"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/myocardial-bridge",
  "inputs": {
    "compression": "98",
    "diastolic": "10",
    "length": "25",
    "depth": "3"
  },
  "expect": [
    "98%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nt-probnp",
  "inputs": {
    "age": "108",
    "ntprobnp": "1850"
  },
  "expect": [
    "1800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nyha-classification",
  "inputs": {
    "walk": "480"
  },
  "expect": [
    "480米"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "33"
  },
  "expect": [
    "2000mL"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/rater-risk-3",
  "inputs": {
    "age": "98",
    "hr": "80",
    "sbp": "130",
    "cr": "1.0"
  },
  "expect": [
    "114"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/statin-dose",
  "inputs": {
    "ldl": "6.8"
  },
  "expect": [
    "(6.8−2.6)/6.8×100%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/timi-score",
  "inputs": {
    "s_age": "2"
  },
  "expect": [
    "2/14"
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
  console.log("==== cardiology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
