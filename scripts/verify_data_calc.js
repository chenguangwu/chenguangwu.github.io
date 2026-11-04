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
},
  {
    "slug": "data/generator-14",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "EAN-13: 7395250459689 QR数据: JiX3X0gPF4x7nhvqzhoPG2ybZX35DOVXhYPk5AHGCY5Cra2 2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「EAN-13: 7395250459689 QR数据: JiX3X0gPF4x7…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "data/generator-report",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "划 > 风险提示 7. 财务收支报表 指标：完成率 117% 环比 23% 新增 1408"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「划 > 风险提示 7. 财务收支报表 指标：完成率 117% 环比 23% 新增…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "data/random-1",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "GB）： 1. #03D670 rgb(3, 214, 112) 2. #A09D12 rgb(160, 157, 18) 3. #71E300 rgb(113, 227, 0) 4. #AF4A6D rgb(175, 74, 109) 5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「GB）： 1. #03D670 rgb(3, 214, 112) 2. #A09…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    // 2026-11-05 随机源改 crypto.getRandomValues 后，原具体验证码锚点依赖 harness 的
    // 种子 Math.random，必然失效。改为直接校验三个生成函数的「长度 × 字符集」。
    "slug": "data/random-4",
    "clicks": [
      '(function(){var d=genCode(DIGITS,6),a=genCode(LETTERS,6),m=genCode(MIXED,6);var ok=/^[0-9]{6}$/.test(d)&&/^[A-Za-z]{6}$/.test(a)&&/^[A-Za-z0-9]{6}$/.test(m);document.getElementById("res").innerHTML=ok?"R4-CODE-FMT-OK-3x6":"R4-CODE-FMT-FAIL:"+d+a+m;})()'
    ],
    "expect": [
      "R4-CODE-FMT-OK-3x6"
    ],
    "ref": "genCode 三个分支：数字列仅 [0-9]、字母列仅 [A-Za-z]、混合列 [A-Za-z0-9]，长度均为 6。随机内容不可断言，故校验长度与字符集；默认输出由 5 行混合码组成，不含标记。生成路径已改 crypto.getRandomValues（拒绝采样无模偏），无 crypto 时显式提示。"
  },
  {
    // 2026-11-05 随机源改 crypto.getRandomValues 后，原「具体密码串」锚点依赖 harness
    // 的种子 Math.random，必然失效。改为「条数 × 长度 × 字符集」结构断言。
    "slug": "data/random-3",
    "inputs": {
      "cnt": "3"
    },
    "clicks": [
      'gen();(function(){var h=document.getElementById("res").innerHTML;var m=h.match(/<strong>[^<]*<\\/strong>/g)||[];var c=[];for(var i=0;i<3;i++)c.push(genPassword());var ok=m.length===3&&c.every(function(x){return x.length===16&&x.split("").every(function(ch){return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?".indexOf(ch)>=0;});});document.getElementById("res").innerHTML=ok?"R3-PWD-FMT-OK-3x16":("R3-PWD-FMT-FAIL:count="+m.length);})()'
    ],
    "expect": [
      "R3-PWD-FMT-OK-3x16"
    ],
    "ref": "输入条数 3 ⇒ gen() 渲染 3 条 <strong>（条数不看具体值）；另独立调用 genPassword() 3 次校验格式：固定 16 位（先各取 1 位大写/小写/数字/符号，其余 12 位从并集取，再 Fisher-Yates 打乱），逐位校验 88 字符表。gen() 输出经 escHtml 转义（字符表含 & < >，原样拼 innerHTML 会被解析成标签、显示残缺），故条数断言用 m.length 而非解析 <strong> 内文。默认 cnt=5 ⇒ 条数断言不命中。生成与打乱均用 crypto.getRandomValues（拒绝采样无模偏）。"
  },
  {
    slug: "data/yaml-json",
    inputs: { input: "{\"a\":1,\"b\":2}" },
    expect: ["a: 1 b: 2"],
    ref: 'JSON→YAML：{a:1,b:2} → `a: 1\\nb: 2`，collectStrings 折叠换行→空格，锚 `a: 1 b: 2`（纯字符串确定性映射）'
  },

  {
    slug: "data/yaml-json",
    inputs: { input: "{\"name\":\"Tom\"}" },
    expect: ["name: Tom"],
    ref: 'JSON→YAML：{name:Tom} → `name: Tom`（Tom 无特殊字符不引号），锚 `name: Tom`'
  },

  {
    slug: "data/yaml-json",
    inputs: { input: "{\"list\":[1,2,3]}" },
    expect: ["list: - 1 - 2 - 3"],
    ref: 'JSON→YAML：数组 [1,2,3] → `list:\\n  - 1\\n  - 2\\n  - 3` 折叠为 `list: - 1 - 2 - 3`'
  },

  {
    slug: "data/yaml-json",
    inputs: { input: "{\"x\":{\"y\":true}}" },
    expect: ["x: y: true"],
    ref: 'JSON→YAML：嵌套对象 {x:{y:true}} → `x:\\n  y: true` 折叠为 `x: y: true`'
  },

  {
    slug: "data/yaml-json",
    inputs: { input: "{\"n\":null}" },
    expect: ["n: null"],
    ref: 'JSON→YAML：{n:null} → `n: null`（null 映射）'
  },

  {
    slug: "data/yaml-json",
    inputs: { input: "{\"arr\":[\"a\",\"b\"]}" },
    expect: ["arr: - a - b"],
    ref: 'JSON→YAML：字符串数组 [a,b] → `arr:\\n  - a\\n  - b` 折叠为 `arr: - a - b`'
  },

  {
    "slug": "data/csv-json",
    "inputs": { "input": "a,b,c\n9,8,7" },
    "expect": ["\"col_1\":\"9\"", "\"col_3\":\"7\""],
    "ref": "csv→json(无表头)：首行作数据、列名 col_1/2/3 ⇒ 输出 [{\"col_1\":\"a\",\"col_2\":\"b\",\"col_3\":\"c\"},{\"col_1\":\"9\",\"col_2\":\"8\",\"col_3\":\"7\"}]；锚取仅由注入数据出现的值（默认 textarea 为 name/age/city，不出现 col_1\":\"9），注入失败即不命中。"
  },

  {
    "slug": "data/csv-json",
    "inputs": { "input": "x,y\n100,200" },
    "expect": ["\"col_2\":\"200\""],
    "ref": "csv→json(无表头)：第二行第二列 200 ⇒ \"col_2\":\"200\"（默认 textarea 无该值，注入失败即不命中）。"
  },
  {
    "slug": "data/csv-json",
    "inputs": { "input": "x,y\n100,200" },
    "copyCheck": { "fn": "copyResult", "expect": "\"col_2\":\"200\"" },
    "ref": "复制路径：注入转换后 copyResult(event) 写入剪贴板的内容必须等于结果区 \"col_2\":\"200\"，且 then 回调不抛异常；旧实现 .then 内读隐式 event.target 会抛 TypeError 被 Promise 吞掉。"
  },

  {
    "slug": "data/yaml-json",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n错误: Unexpected non-whitespace character after JSON at position 2 (line 2 column 1)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n错误: Unexpected non-whitespace char…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },


];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== data calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
