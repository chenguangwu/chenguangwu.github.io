#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "office/excel-formula-reference",
  "inputs": {},
  "expect": [
    "COUNTIFS(条件区域1"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "office/mindmap",
  "inputs": {
    "editor": ""
  },
  "expect": [
    "请检查网络连接后刷新页面重试"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：render() 产出 SVG / Canvas 布局，harness 无真实布局与字体度量；"
     + "默认态文案本身即渲染失败提示，注入 editor 后 mindmap 容器仍为空（2026-09-25 实测）。"
},
{
  "slug": "office/pdf-split",
  "inputs": {},
  "clicks": [
    "totalPages=20;document.getElementById('rangeInput').value='1,3,5-7';updateRangePreview();"
  ],
  "expect": [
    "将提取 <strong>5</strong> 页",
    "1, 3, 5, 6, 7"
  ],
  "ref": "（2026-09-24 记为「默认空态，只能断言「已选」」）updateRangePreview() 读 #rangeInput 文本 → parseRanges(input,totalPages) 解析页码区间 → 写 #rangePreview。totalPages 初始为 0（必须等真实 PDF 上传），但它是顶层 `let`，直接赋值即可；parseRanges 的越界校验按该值做（1/3/5-7 在 1..20 内合法）。独立复算：去重排序后 = [1,3,5,6,7] ⇒ 5 页。旧锚「已选」来自 updateThumbStatus() 的空态（selectedPages 为空），默认态必命中，判别力 0，已弃。"
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
  console.log("==== office calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
