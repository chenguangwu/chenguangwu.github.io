#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "text/analysis-density",
  "inputs": {
    "data": "苹果苹果香蕉苹果 水果 apple apple",
    "kw": "苹果,apple"
  },
  "expect": [
    "25.00%",
    "16.67%"
  ],
  "ref": "非默认输入+独立复算：中文按字10/英文按词2→合计词数12；苹果出现3次密度25.00%、apple出现2次密度16.67%（默认文案不含这些串，注入失败即不命中）"
},
{
  "slug": "text/calc-1",
  "inputs": {
    "textA": "const a = 1;\nfunction foo() { return a + 2; }",
    "textB": "const a = 2;\nfunction foo() { return a + 3; }"
  },
  "clicks": ["calc()"],
  "expect": [
    "共 4 处差异",
    "const a = 1;",
    "return a + 3;"
  ],
  "ref": "逐行比对：A 两行与 B 两行均不同 ⇒ 差异行 2+2=4 处。"
     + "原 expect「console.log(」出自 textarea 里的默认示例文本（回退默认仍命中 ⇒ 逃生项），且 textA/textB 注入为空串。",
  },
{
  "slug": "text/convert-6",
  "inputs": {
    "val": "Hello World",
    "to": "lower"
  },
  "expect": [
    "lower"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "text/convert-7",
  "inputs": { "text": "my_variable_name" },
  "expect": ["camelCase: myVariableName", "PascalCase: MyVariableName", "snake_case: my_variable_name", "kebab-case: my-variable-name"],
  "ref": "命名格式互转：my_variable_name → camelCase=myVariableName / PascalCase=MyVariableName / snake_case=my_variable_name / kebab-case=my-variable-name（默认 hello_world 得 helloWorld/HelloWorld/hello_world/hello-world，注入失败即不命中）"
},
{
  "slug": "text/lorem-ipsum-generator",
  "inputs": {
    "n": "3",
    "seed": "mid"
  },
  "expect": [
    "mid"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "text/reading-time-estimator",
  "inputs": {
    "cjkwpm": "450",
    "enwpm": "200",
    "src": "在纯前端工具站里，阅读时长估算是一个很实用的小功能，帮助用户判断一篇长文需要投入多少时间。"
  },
  "expect": [ "450 字/分" ],
  "ref": "auto-restore"
},
{
  "slug": "text/reading-time-estimator",
  "inputs": {
    "cjkwpm": "450",
    "enwpm": "200",
    "src": ""
  },
  "expect": [ "请输入要估算的文本" ],
  "ref": "IT-N37 空文本：不再把空文本抬成 1 分钟，而是明确提示。默认示例含中文正文，不命中。"
},
{
  "slug": "text/reading-time-estimator",
  "inputs": {
    "cjkwpm": "0",
    "enwpm": "200",
    "src": "abc"
  },
  "expect": [ "请输入大于 0 的阅读速度" ],
  "ref": "IT-N37 速度校验：0 字/分非法 ⇒ 明确报错；修复前 Math.max(1,…) 把 0 抬成 1 后照常输出。默认速度 300/200，不命中。"
},
{
  "slug": "text/reading-time-estimator",
  "inputs": {
    "cjkwpm": "100",
    "enwpm": "200",
    "src": "中".repeat(110)
  },
  "expect": [ "2 分钟" ],
  "ref": "IT-N37 取整口径：110 中文字 @100 字/分 = 1.1 分钟 ⇒ 文档口径向上取整 = 2；修复前 Math.round 得 1。默认正文不足 1 分钟，不命中。"
},
{
  "slug": "text/sensitive-word-filter",
  "inputs": {
    "replaceWith": "*_X",
    "content": "",
    "words": "违法,垃圾,诈骗,外挂"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/stats-1",
  "inputs": {
    "text": "统计中文 English 测试 ABC 数字 99 与符号！"
  },
  "expect": [
    "24",
    "11"
  ],
  "ref": "字数统计：'统计中文 English 测试 ABC 数字 99 与符号！' → 含空白30、不含空白24、中文11、英文单词2(English/ABC)、数字组1(99)、行数1、非空行1（非默认输入，注入失败即不命中）"
},
{
  "slug": "text/text-to-1337",
  "inputs": {
    "src": "leet speak is fun",
    "level": "mid"
  },
  "expect": [ "15 fun" ],
  "ref": "auto-restore"
},
{
  "slug": "text/text-to-ascii-art",
  "inputs": {
    "src": "HELLO_X",
    "ch": "#"
  },
  "expect": [
    "HELLO_X"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "text/text-to-braille",
  "inputs": {
    "src": "Hello 123!_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
// ── 空态回归：textarea 清空后必须提示「请输入」，不得输出全 0 统计 ──
{
  "slug": "text/stats-1",
  "inputs": { "text": "" },
  "expect": ["请输入待统计文本后再统计。"],
  "ref": "空态回归：textarea 清空时旧实现输出「总字符数 0 / 不含空白 0 / 中文字符 0 … 非空行 0」七项伪结果；现要求提示且不输出统计值。默认示例文本非空（含 24/11 等数值），不含该提示 ⇒ 强判别。"
}
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

  console.log("==== text calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
