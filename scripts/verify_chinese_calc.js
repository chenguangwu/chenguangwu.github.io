#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chinese/chinese-character",
  "inputs": {},
  "expect": [
    "13"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chinese/chinese-radical-lookup",
  "inputs": {},
  "expect": [
    "请输入一个汉字进行查询"
  ],
  "ref": "auto-restore(default)"
},
{
  // 原为 no_inputs 弱用例：expect「(鼠)1901年」只是年份下拉动态拼接文本「1900年 (鼠)1901年 (牛)…」的子串，与注入无关。
  // 注入 solarDate=2027-02-06（= 农历正月初一，经 lunardate 独立库核对）→ 干支「丁未年」+ 副标题整串。
  // 注意：不可用「正月初一」「丙午年」「2026-02-17」——深链示例 block 已含这些字面量（outside-script 命中，属逃生项）。
  "slug": "chinese/lunar-calendar",
  "inputs": {
    "solarDate": "2027-02-06"
  },
  "expect": [
    "丁未年",
    "2027年 · 羊年 · 公历 2027-02-06"
  ],
  "ref": "公历 2027-02-06 → 农历正月初一（lunardate 独立核对，非取页面自输出）；2027 干支：(2027-4)%10=3→丁、(2027-4)%12=7→未 → 丁未年；生肖 (2027-4)%12 → 羊。空输入时 convertSolarToLunar 提前 return，两串均不出现。"
},
{
  "slug": "chinese/stroke-order-viewer",
  "inputs": {
    "word": "永_X"
  },
  "expect": [
    "永_X"
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
  console.log("==== chinese calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
