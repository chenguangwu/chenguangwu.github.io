#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "office/excel-formula-reference",
  "inputs": {},
  "clicks": [
    "document.getElementById('keyword').value='数字';render();"
  ],
  "expect": [
    "求平均值。 TEXT 分类：文本",
    "分类：统计 =AVERAGE(数字1,数字2,...) 求平均值。 TEXT"
  ],
  "ref": "（推翻 auto-restore）关键词过滤型页：render() 读 #keyword 后对 DATA 做顺序保持型过滤，命中项依次 appendChild 进 #list，collectStrings 采集其 innerHTML（标签→空格）⇒ 过滤态的「相邻条目」串可被断言。注入关键词「数字」⇒ 只有 SUM / AVERAGE / TEXT 命中（三处 syntax 含「数字」），于是 AVERAGE 与 TEXT 在全表中间隔 IF、VLOOKUP、INDEX、MATCH、SUMIFS、COUNTIFS 六项，在过滤态却紧邻 ⇒ 锚跨边界串「求平均值。 TEXT 分类：文本」（默认全量渲染下 AVERAGE 之后是 IF，故默认态必失配）。另一条锚「分类：统计 =AVERAGE(...) 求平均值。 TEXT」同属该边界。已实测排除的逃生项候选：`=TEXT(数字,\"0.00\")` 与 `TEXT 分类：文本 =TEXT(数字,\"0.00\") 数字转文本与格式控制。` —— 二者整段是 TEXT 条目自身的渲染结果，默认全量渲染里同样 contiguous ⇒ 判别力 0（BATCH110①「锚不得成为默认态某串的子串」）。"
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
