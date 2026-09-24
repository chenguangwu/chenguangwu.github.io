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
  "inputs": {
    "char": "河"
  },
  "clicks": ["query()"],
  "expect": [
    "部首： 氵 / 三点水",
    "总笔画： 8"
  ],
  "ref": "DATA['河'] = [氵, 三点水, 8, 水流, hé, 河]。只锚 d[0]/d[1]/d[2] 渲染出的部首与总笔画。"
     + "刻意不锚「读音」「字形」两行：页面模板把 d[3] 当读音、d[4] 当字形，而 DATA 的 d[3] 是字形描述、"
     + "d[4] 是拼音 ⇒ 输出「读音： 水流」「字形： hé （河）」，属字段错位真缺陷（已记 DEV-PLAN §九）；"
     + "锚它会把缺陷固化成期望值。默认态 char 空 ⇒ 「请输入一个汉字进行查询」。",
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
