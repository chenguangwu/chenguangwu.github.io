#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "funeral/ceremony-timeline",
  "inputs": {
    "startTime": "09:00",
    "scale": "medium"
  },
  "expect": [
    "medium"
  ],
  "ref": "auto-restore"
},
{
  "slug": "funeral/funeral-budget-planner",
  "inputs": {
    "newCat": "ritual"
  },
  "expect": [
    "ritual"
  ],
  "ref": "auto-restore"
},
{
  "slug": "funeral/grave-design",
  "inputs": {
    "title": "故先考",
    "name": "李公讳某某",
    "birthYear": "一九四五年",
    "deathYear": "二〇二三年",
    "stoneW": "3.8",
    "stoneH": "1.0",
    "plotL": "2.5",
    "plotW": "1.5",
    "epitaph": "慈父一生勤俭持家，德厚流光，恩泽子孙。痛于二〇二三年某月某日溘然长逝，享年七十八岁。立碑永志，以示追思。"
  },
  "expect": [
    "3.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "funeral/memorial-date",
  "inputs": {
    "memTitle": "先考_X",
    "memName": ""
  },
  "expect": [
    "先考_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "funeral/urn-size",
  "inputs": {
    "weight": "98",
    "height": "170"
  },
  "expect": [
    "23×16×16"
  ],
  "ref": "auto-restore"
},
  {
    "slug": "funeral/reminder-3",
    "inputs": {
      "sName": "abc123测试",
      "sDate": "abc123测试",
      "lName": "abc123测试",
      "lYear": "42",
      "lMonth": "2"
    },
    "expect": [
      "，请在上方添加。\n⚠ 计算结果含无效值，请检查输入是否为有效正数。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sName\":\"abc123测试\",\"sDate\":\"abc123测试\",\"lName\":\"abc123测试\",\"lYear\":\"42\",\"lMonth\":\"2\"}，输出区含「，请在上方添加。\n⚠ 计算结果含无效值，请检查输入是否为有效正数。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== funeral calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
