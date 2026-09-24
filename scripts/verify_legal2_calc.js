#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "legal2/compensation-n1",
  "inputs": {
    "avgSalary": "15000",
    "capSalary": "30000"
  },
  "expect": [
    "15000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "legal2/contract-dates",
  "inputs": {
    "noticeDays": "45"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "legal2/ip-protection",
  "inputs": {
    "ipType": "utility"
  },
  "expect": [
    "10 年 保护期限"
  ],
  "ref": "auto-restore"
},
{
  "slug": "legal2/keyword-extract",
  "inputs": {
    "docInput": "甲公司与乙公司于2025年3月签订设备采购合同，约定交货期限为60日，违约金按日万分之五计算，总价款人民币85万元。乙方逾期交货已构成违约，应依《中华人民共和国民法典》第五百七十七条承担违约责任，并赔偿甲方损失。"
  },
  "checkIds": ["extKeyword", "extDate", "extMoney", "extParty", "extLegal", "extLaw"],
  "clicks": ["extract()"],
  "expect": [
    "21 提取关键词",
    "106 文书字数",
    "违约 3 次"
  ],
  "ref": "六类提取开关均为 checkbox（extKeyword/extDate/extMoney/extParty/extLegal/extLaw），"
     + "桩内 checkbox 恒未勾 ⇒ 必须显式声明 checkIds 才会提取。注入文书 106 字 ⇒ 关键词 21、"
     + "法律术语 10、日期 1（2025年3月）、金额 2、当事人 2、法条引用 3；高频词 Top1「违约」3 次。"
     + "原 expect 是 loadSample 示例文书的首句（默认态常量），且 docInput 为空 ⇒ 输出全 0。",
  },
{
  "slug": "legal2/statute-deadline",
  "inputs": {
    "customYears": "3",
    "limitType": "1"
  },
  "expect": [
    "1 年 时效期间"
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
  console.log("==== legal2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
