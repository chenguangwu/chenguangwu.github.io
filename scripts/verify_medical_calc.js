#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "medical/assessor-risk-3",
  "inputs": {
    "ph": "9",
    "water": "1500",
    "protein": "1.2",
    "sodium": "3000",
    "oxalate": "150"
  },
  "expect": [
    "4/20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calc-34",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30"
  },
  "expect": [
    "1898"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "weight": "30",
    "age": ""
  },
  "expect": [
    "300.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-due-date",
  "inputs": {
    "cycle": "42"
  },
  "expect": [
    "42"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "750",
    "dur": "4",
    "conc": "0.4",
    "w": "60"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "2.0",
    "meld_cr": "1.0",
    "meld_inr": "1.2",
    "meld_na": "140",
    "gcs_e": "3"
  },
  "expect": [
    "E3+V5+M6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "1",
    "from": "18"
  },
  "expect": [
    "18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/convert-time-infusion",
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
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "90",
    "height": "170",
    "age": "30",
    "perDose": "10"
  },
  "expect": [
    "900.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/drug-info",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "未找到匹配药物"
  ],
  "ref": "关键词过滤型：inputs 写 search=zzzqx ⇒ oninput=render() 过滤 34 种药物得空集 ⇒ 结果区渲染「未找到匹配药物」。默认态（search 空）渲染全部 34 种、blob 内无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "medical/estimate-metabolism",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30",
    "bf": ""
  },
  "expect": [
    "+149.3%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/medical-calculator",
  "inputs": {
    "dose_weight": "90",
    "dose_per_kg": "10",
    "dose_freq": "3",
    "iv_volume": "500",
    "iv_time": "120",
    "glucose_mmol": "5.6",
    "glucose_mg": "100.9",
    "temp_value": "36.5",
    "bp_sbp": "120",
    "bp_dbp": "80",
    "timer_custom_min": ""
  },
  "expect": [
    "900.0mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/reminder-2",
  "inputs": {
    "medName": "阿莫西林胶囊",
    "medBatch": "B20260118",
    "medExpiry": "2027-03-15",
    "medSpec": "0.25g×24粒",
    "medLocation": "客厅药箱"
  },
  "clicks": ["addMed()"],
  "expect": [
    "阿莫西林胶囊 0.25g×24粒",
    "1 药品总数",
    "批号：B20260118"
  ],
  "ref": "addMed() 要求 medName 与 medExpiry 均非空（否则 showToast 后直接 return），两项都要注入；"
     + "入表后 renderAll() 刷新 medList 与 statGrid。不锚「剩 N 天」与安全/注意/紧急计数 —— 均随运行日漂移。"
     + "默认态 meds 为空 ⇒ 列表恒「暂无药品记录」、总数恒 0。",
},
{
  "slug": "medical/stats-4",
  "inputs": {
    "cases": "阑尾切除,55\n阑尾切除,72\n阑尾切除,64\n阑尾切除,88\n阑尾切除,61"
  },
  "expect": [
    "68.0",
    "89.0",
    "12.75"
  ],
  "ref": "手术时长：5 例 55/72/64/88/61 → 均值 340/5=68.0 分钟，样本标准差 12.75，排台上限 P95=68.0+1.645×12.75=89.0（独立复算，非页面默认记录）"
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
  console.log("==== medical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
