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
  "slug": "data/csv-analyzer",
  "inputs": {
    "csvInput": "name,note\nAlice,\"first\nsecond\"\nBob,ok",
    "delim": ","
  },
  "expect": ["还有 1 行", "Alice first second"],
  "ref": "引号内换行（2026-11-16）：整段按引号状态解析 ⇒ note 字段为「first\\nsecond」但只算 1 条数据，共 2 行；第二字段换行在表格里折成空格。旧实现先按换行切行 ⇒ 得到 3 条数据行、Alice 的 note 只剩 first ⇒ 不出现「还有 1 行」且统计行数偏多。"
},
{
  "slug": "data/csv-analyzer",
  "inputs": {
    "csvInput": "name,note\nAlice,\"say \"\"hi\"\"\"\nBob,x",
    "delim": ","
  },
  "expect": ["say \"hi\""],
  "ref": "转义双引号：\"\" 解析为一个 \"，预览显示 say \"hi\"；旧实现按奇偶翻转 inQuote，四个引号会互相抵消并把内容拆错。"
},
{
  "slug": "data/csv-analyzer",
  "inputs": {
    "csvInput": "a,b\n1,2,3\n4,5",
    "delim": ","
  },
  "expect": ["1 行字段数与表头（2 列）不一致"],
  "ref": "错列可见（2026-11-16）：第 2 行 3 列、表头 2 列 ⇒ 预览上方提示 1 行字段数不一致；旧实现静默按表头取前两列统计。缺列行（4,5 之后的第 3 行）不触发提示。"
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
  "slug": "data/data-cleaner",
  "inputs": { "inputData": "ＡＢＣ　１２３", "outputData": "", "maxLen": "" },
  "clicks": ["var btn=[].slice.call(document.querySelectorAll('.op-btn')).filter(function(b){return b.textContent.trim()==='全角转半角';})[0];if(btn)btn.click();"],
  "expect": ["ABC 123", "全角转半角"],
  "ref": "新增全角转半角：全角字母/数字转 ASCII，全角空格转普通空格；旧版无此操作，输入原样输出。"
},
{
  "slug": "data/data-cleaner",
  "inputs": { "inputData": "abc\n\n", "outputData": "", "maxLen": "" },
  "expect": ["1\n1\n去空白 · 去空行 · 去重"],
  "ref": "尾随空行不计条数（2026-11-16）：`abc\\n\\n` 只剩 1 条，原始/清洗后都显示 1；旧实现 `split('\\n').length` 得 3。默认样例首尾都有空行，旧值不等于 1 ⇒ 强判别。"
},
{
  "slug": "data/data-cleaner",
  "inputs": { "inputData": "😀ABC", "outputData": "", "maxLen": "1" },
  "expect": ["1\n😀\n1\n1"],
  "ref": "按字形簇截断（2026-11-16）：限长 1 时输出完整 😀 而不是半个代理项；旧实现按 UTF-16 码元 slice(0,1) ⇒ \\ud83d 孤立代理项。输入回显仍是 😀ABC，所以必须锚定「输出值\\n计数」这一组合。"
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
    "dataVals": "1,2,2,3,4,5,5,5,6",
    "bins": "3"
  },
  "expect": [
    "44.4%"
  ],
  "ref": "确定性算例：n=9、min=1、max=6、k=3 → h=1.6667，三组频数 3/2/4 → 频率 33.3%/22.2%/44.4%；默认 15 点 5 组最高 26.7%，注入态不含该串 ⇒ 区分真实分组与随机频数。"
},
{
  "slug": "data/pivot-table",
  "inputs": {
    "inputData": "地区,产品,销量\nA,X,10\nA,Y,\nA,X,abc\nB,Y,5",
    "rowField": "地区", "colField": "产品", "valField": "销量", "agg": "count"
  },
  "expect": ["A 1 0 1 B 0 1 1 合计 1 1 2"],
  "ref": "count 只统计可解析数值：A/X 有 10 一个有效值、A/Y 空值 0、B/Y 5；旧实现按匹配行计数会把空值算成 1。"
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
  "slug": "data/pivot-table",
  "inputs": {
    "inputData": "地区,产品,销量\nA,X,12abc\nA,X,Infinity\nA,X,\nA,X,0\nA,X,2.5",
    "rowField": "地区", "colField": "产品", "valField": "销量", "agg": "avg"
  },
  "expect": ["A 1.25 1.25"],
  "ref": "整串数字校验：12abc / Infinity / 空值均跳过，仅 0 与 2.5 有效 ⇒ 均值 1.25；旧 parseFloat 会把 12abc 当 12，均值变成 4.83。"
},
{
  "slug": "data/pivot-table",
  "inputs": {
    "inputData": "地区,产品,销量\nA,X,10\nA,Y,20\nB,X,100\nB,Y,200\nB,X,300",
    "rowField": "地区", "colField": "产品", "valField": "销量", "agg": "avg"
  },
  "expect": ["126.00"],
  "ref": "avg 合计语义（2026-11-16）：合并原始值后重新求均值 ⇒ 总计 (10+20+100+200+300)/5 = 126.00；旧实现把行均值再求和得 430，或列均值再平均。默认样例为 count，无 126.00。"
},
{
  "slug": "data/pivot-table",
  "inputs": {
    "inputData": "地区,产品,销量\nA,X,7\nA,Y,3\nB,X,5\nB,Y,9",
    "rowField": "地区", "colField": "产品", "valField": "销量", "agg": "min"
  },
  "expect": ["A 7 3 3 B 5 9 5 合计 5 3 3"],
  "ref": "min 合计取极值（2026-11-16）：行合计 A=min(7,3)=3、B=min(5,9)=5；列合计 X=5、Y=3；总计 3。旧实现对合计列求和 ⇒ 行 A 10/B 14、列 12/12、总计 24，整串不命中。"
},
{
  "slug": "data/pivot-table",
  "inputs": {
    "inputData": "地区,备注,销量\n华北,\"北京,朝阳\",10\n华北,\"上海,浦东\",20",
    "rowField": "地区", "colField": "备注", "valField": "销量", "agg": "sum"
  },
  "expect": ["北京,朝阳 上海,浦东", "华北 10 20 30"],
  "ref": "带逗号的引号字段（2026-11-16）：按 CSV 状态机解析后两列备注完整、销量 10+20 汇总 30；旧实现直接 split(',') ⇒ 备注只剩「\\\"北京」，第三段被当作销量 ⇒ 汇总错位。"
},
{
  "slug": "data/pivot-table",
  "inputs": {
    "inputData": "地区,产品,销量\n华北,<img src=x onerror=alert(1)>,10",
    "rowField": "地区", "colField": "产品", "valField": "销量", "agg": "sum"
  },
  "expect": ["&lt;img src=x onerror=alert(1)&gt;"],
  "ref": "用户内容转义（2026-11-16）：列值经 escPivot 后进入 innerHTML，尖括号变成实体；旧实现原样拼接，输入会被当成标签执行。默认样例行不含尖括号。"
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
    "expect": ["\"col_2\":\"200\""],
    "copyCheck": { "fn": "copyResult", "expect": "\"col_2\":\"200\"" },
    "ref": "复制路径：注入转换后 copyResult(event) 写入剪贴板的内容必须等于结果区 \"col_2\":\"200\"，且 then 回调不抛异常；旧实现 .then 内读隐式 event.target 会抛 TypeError 被 Promise 吞掉。"
  },
  {
    "slug": "data/csv-json",
    "inputs": { "input": "id,id\n00123,9007199254740993" },
    "checkIds": ["hasHeader", "parseNumber"],
    "expect": ["表头重复，转换会丢失列：id（第 1 与 2 列）"],
    "ref": "重复表头显式拒绝（2026-11-16）：旧实现两个同名列写同一对象键，后者覆盖前者且不报错；现提示重复列号并停止输出。默认样例行（name,age,city）不含该提示 ⇒ 强判别。"
  },
  {
    "slug": "data/csv-json",
    "inputs": { "input": "a,b\n1,2,3" },
    "checkIds": ["hasHeader", "parseNumber"],
    "expect": ["列数超出表头，多出的数据会被丢弃：第 2 行有 3 列（表头 2 列）"],
    "ref": "超列拒转：旧实现仅遍历表头列，第三列 3 被静默丢弃；现逐行报出超列位置并停止输出。缺列（列数更少）仍按空串补，不报错。"
  },
  {
    "slug": "data/csv-json",
    "inputs": { "input": "id,big,code\n1,9007199254740993,00123" },
    "checkIds": ["hasHeader", "parseNumber"],
    "expect": ["\"big\":\"9007199254740993\"", "\"code\":\"00123\"", "\"id\":1"],
    "ref": "数值精度保护：超安全整数 9007199254740993 保留字符串（旧实现 Number ⇒ …992），前导零编号 00123 保留字符串（旧实现 ⇒ 123）；普通整数 1 仍转数字。"
  },
  {
    "slug": "data/csv-json",
    "inputs": { "input": "a,b\n\"unclosed,2", "delimiter": ",", "quote": "\"" },
    "checkIds": ["hasHeader", "parseNumber"],
    "expect": ["CSV 引号未闭合"],
    "ref": "未闭合引号：旧实现把余下全部内容吞进字段并照常输出；现提示行号并停止转换，避免把错误解析结果当有效数据。限定符/分隔符两个 select 必须显式注入——桩里 select 默认值不是首个 option 的 value，不注入则 quote 为空、引号状态永不进入 ⇒ 假通过。"
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

  /* ---------- 2026-11-16（694 批）：YAML 解析与序列化修复 ---------- */
  {
    slug: "data/yaml-json",
    clicks: [
      "setDir('y2j');document.getElementById('input').value='list:\\n  - name: Tom\\n    age: 3';convert();"
    ],
    expect: ['"age": 3', '"name": "Tom"'],
    ref: "I-6 列表项多键对象：`- name: Tom` 后的同级缩进键 age 必须并入同一对象。旧实现在列表项命中 key 后遇到更深缩进直接 break ⇒ 输出仅 {\"list\":[{\"name\":\"Tom\"}]}，无 \"age\": 3。默认方向 j2y、默认输入为 JSON ⇒ 不命中。"
  },
  {
    slug: "data/yaml-json",
    clicks: [
      "setDir('y2j');document.getElementById('input').value='host: zzxhost # 注释';convert();"
    ],
    expect: ['"host": "zzxhost"'],
    ref: "I-7 行尾注释：引号外且 `#` 前有空白的注释应剥离。旧实现只跳过整行注释 ⇒ 值变成 \"zzxhost # 注释\"，不含 \"host\": \"zzxhost\"。改用唯一值 zzxhost 避开默认态 JSON 示例里的 localhost，确保零逃生。"
  },
  {
    slug: "data/yaml-json",
    clicks: [
      "setDir('y2j');document.getElementById('input').value='msg: |\\n  hello\\n  world';convert();"
    ],
    expect: ['"msg": "hello\\nworld\\n"'],
    ref: "I-7 块标量：`|` 保留换行、默认 clip 单个结尾换行 ⇒ JSON 值 hello\\\\nworld\\\\n。旧实现把 `|` 当嵌套对象入口、正文行无冒号被跳过 ⇒ \"msg\": null。"
  },
  {
    slug: "data/yaml-json",
    clicks: [
      "setDir('y2j');document.getElementById('input').value='- \"a:b\"';convert();"
    ],
    expect: ['"a:b"'],
    ref: "I-7 引号内冒号：`- \"a:b\"` 是标量而不是键值对。旧实现按第一个冒号切分 ⇒ [{\"\\\"a\":\"b\\\"\"}]；新增按引号状态找分隔冒号 ⇒ [\"a:b\"]。"
  },
  {
    slug: "data/yaml-json",
    inputs: { input: "{\"a: b\":1}" },
    expect: ['"a: b": 1'],
    ref: "I-8 JSON→YAML 键转义：含冒号空格的键必须加引号。旧实现键原样输出 `a: b: 1`（非法 YAML）；现键走 yamlString ⇒ `\"a: b\": 1`。"
  },
  {
    slug: "data/yaml-json",
    inputs: { input: "{\"k\":\"it's \\\"x\\\"\"}" },
    expect: ["k: \"it's \\\"x\\\"\""],
    ref: "I-8 混合引号：值同时含单双引号时统一用双引号 + JSON 转义。旧实现走单引号包裹且不转义内部单引号 ⇒ `k: 'it's \"x\"'`（非法）。"
  },
  {
    slug: "data/yaml-json",
    inputs: { input: "{\"version\":\"7.7.7\",\"port\":6060}" },
    expect: ['version: "7.7.7"', "port: 6060"],
    ref: "序列化回归：形似版本的字符串需保持字符串语义（加引号），整数仍裸写；此前 1.0.0 不加引号、回读时无法与字符串区分。改用唯一值 7.7.7/6060 避开默认态示例自带的 1.0.0/8080，确保零逃生。"
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
