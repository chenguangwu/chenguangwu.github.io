#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原为 all_default 弱用例：csvInput 为空串 = 页面默认；expect「field_0」是空表头回退命名的产物。
  // 注入两行 CSV + 显式勾选 hasHeader（页面 HTML 默认 checked，harness 的 getElementById(id).checked 需注入才为 true）
  // → 首行作表头、仅剩 1 行数据 → 「共解析 1 行」。
  "slug": "data/calc-1",
  "inputs": {
    "csvInput": "name,age\nAlice,30"
  },
  "checkIds": [
    "hasHeader"
  ],
  "expect": [
    "共解析 1 行"
  ],
  "ref": "parseCsv 后 hasHeader=true → dataRows = rows.slice(1) = 1 行，输出尾部为「共解析 1 行，2 列」。回退默认（hasHeader=false、csvInput 空）→ 2 行数据或「请输入 CSV 数据」，不命中。"
},
{
  // 原为 all_default 弱用例：jsonInput 空串 = 页面默认；expect「JSON」是常量字面（默认态同样命中）。
  // 注入含两个键的 JSON → formatJson 走 JSON.stringify(data, null, getIndent()=2) 分支。
  "slug": "data/calc-2",
  "inputs": {
    "jsonInput": "{\"alpha\":123,\"beta\":[1,2]}"
  },
  "expect": [
    "\"alpha\": 123",
    "\"beta\": ["
  ],
  "ref": "formatJson：text 非空且可解析 ⇒ JSON.stringify(data,null,2)，压空白后含「\"alpha\": 123」「\"beta\": [」（独立复算：缩进 2、冒号后 1 空格；\"beta\" 数组换行被压成空格 ⇒ \"beta\": [ 1, 2 ]）。默认 jsonInput 为空 ⇒ 输出「请输入 JSON 数据。」，与本例零交集。注：textarea 有 oninput ⇒ 阶段 1 注入后即命中；兜底阶段无参调用 minifyJson 会把 result 重写为压缩串（冒号后无空格）⇒ 既不产生锚点、也不影响已判定结果。"
},
{
  "slug": "data/chart-generator",
  "inputs": {
    "dataInput": "一月,30,#3b82f6\n二月,45,#10b981\n三月,60,#f59e0b\n四月,50,#ef4444\n五月,75,#8b5cf6\n六月,90,#ec4899_X"
  },
  "expect": [
    "ec4899_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "data/csv-analyzer",
  "inputs": {
    "csvInput": "name,age,score,city\n张三,25,85.5,北京\n李四,30,92.0,上海\n王五,28,78.5,广州\n赵六,35,88.0,深圳\n钱七,22,95.5,杭州\n孙八,40,72.0,成都_X"
  },
  "expect": [
    "成都_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "data/data-cleaner",
  "inputs": {
    "maxLen": "7",
    "inputData": "  张三\n李四\n张三\n王五\n\n赵六\n  李四\n王五\n钱七\n孙八\n王五\nabc\n  ",
    "outputData": ""
  },
  "expect": [
    "限长"
  ],
  "ref": "auto-restore"
},
{
  "slug": "data/data-visualizer",
  "inputs": {
    "bins": "12",
    "numsInput": "12 15 18 22 19 25 30 28 35 40 38 45 50 48 55 60 58 65 70 75 80 78 85 90 95 100 88 92 78 85"
  },
  "expect": [
    "92.7-100.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "data/generator-35",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "共 8 组"
  ],
  "ref": "auto-restore — 随机直方图生成器，改测结构标签（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "data/pivot-table",
  "inputs": {
    "rowField": "地区",
    "colField": "产品",
    "valField": "销量",
    "inputData": "地区,产品,销量,利润\n华北,A,100,20\n华北,B,150,30\n华东,A,200,40\n华东,B,180,36\n华南,A,120,24\n华南,B,90,18\n华北,A,110,22\n华东,B,160,32",
    "agg": "count"
  },
  "expect": [
    "(count)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "data/random-5",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  // 原为 all_default 弱用例：cnt=5 = 页面默认；expect「1000-9999」是表头常量。
  // 随机页无法锚具体值 ⇒ clicks 内固定 Math.random 为确定值，使三列均可独立复算。
  "slug": "data/random-6",
  "inputs": {
    "cnt": "8"
  },
  "clicks": [
    "var __r=Math.random;Math.random=function(){return 0.123456;};gen();Math.random=__r"
  ],
  "expect": [
    "12 0.1235 2111"
  ],
  "ref": "clicks 临时固定 Math.random⇒0.123456：randInt(0,100)=floor(0.123456×101)=floor(12.469)=12；randFloat(0,1,4)=(0.123456).toFixed(4)=0.1235；randInt(1000,9999)=floor(0.123456×9000)+1000=1111+1000=2111；cnt=8 ⇒ 8 行同值，blob 含连续串「12 0.1235 2111」（独立复算）。默认 cnt=5 且随机真值 ⇒ 该三列恰为这组值的概率≈10^-6，与本例零交集。**必须用完即恢复**：Math 是进程级全局对象，clicks 改它不恢复会污染同进程后续用例（实测令 random-7 默认态误命中）。"
},
{
  // 原为 all_default 弱用例：cnt=5 = 页面默认；expect「2020-01-01」是范围说明常量。
  "slug": "data/random-7",
  "inputs": {
    "cnt": "8"
  },
  "clicks": [
    "var __r=Math.random;Math.random=function(){return 0.5;};gen();Math.random=__r"
  ],
  "expect": [
    "1. 2025-07-01 2. 2025-07-01"
  ],
  "ref": "clicks 临时固定 Math.random⇒0.5（用完即恢复，防跨用例污染）：d=new Date(start+0.5×range)，start=2020-01-01、end=2030-12-31 相差 4017 天 ⇒ 0.5×4017=2008.5 天；2020-01-01→2025-01-01=1827 天（5 年=1825+2 个闰日），余 181.5 天 ⇒ 2025-07-01 12:00 ⇒ formatDate=2025-07-01；cnt=8 ⇒ 8 行同值（独立复算与 dump 实测双核一致）。默认 cnt=5 且随机真值 ⇒ 连续两行同为 2025-07-01 的概率≈0，与本例锚点零交集。"
},
{
  "slug": "data/random-9",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
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
  console.log("==== data calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
