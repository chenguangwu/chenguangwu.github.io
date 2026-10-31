#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cognition/cognitive-assessment",
  "inputs": {
    "scaLen": "quick"
  },
  "expect": [
    "quick"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/corsi-block-test",
  "clicks": [
    "window.__cbResult={mode:'fwd',span:5.5,totalCorrect:10,trials:12,product:60,norms:[{g:'成人 (18–64)',m:5.5},{g:'儿童 (7–11)',m:4.8},{g:'老年 (65+)',m:4.9}]}; __cbEmr();"
  ],
  "expect": [
    "Corsi 广度 5.5（正序）· 正确 10/12 · 乘积分 60"
  ],
  "ref": "双态零交集：expect 依赖 clicks 注入的 __cbResult（span/mode/totalCorrect/trials/product）。判别器清空 clicks 后 finish() 不会触发、__cbEmr 不写门诊记录，blob 无此串 ⇒ 非逃生项。判据：Corsi 广度结果串随注入值变化。"
},
{
  "slug": "cognition/digit-span-test",
  "clicks": [
    "window.__dsResult={fwd:6,bwd:4,seq:4.5,total:4.8,trials:24,norms:{fwd:6.5,bwd:5.5,seq:5.0}}; __dsEmr();"
  ],
  "expect": [
    "总广度 4.8（三项条件均值）· 参考均值 5.7 → 低于参考均值 0.9 · 共 24 个试次"
  ],
  "ref": "双态零交集：expect 依赖 clicks 注入的 __dsResult（fwd/bwd/seq/total/trials/norms）。判别器清空 clicks 后 __dsEmr 不执行、门诊记录不渲染，blob 无此串 ⇒ 非逃生项。判据：总广度与参考均值差值随注入值变化。"
},
{
  "slug": "cognition/human-benchmark",
  "inputs": {
    "tArea": ""
  },
  "expect": [
    "9×9"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：8 个子测验全部由点击 / 倒计时 / 随机序列驱动，"
     + "成绩存 localStorage 历史；无表单输入路径可注入，注入 tArea 不触发任何渲染（2026-09-25 实测）。"
},
{
  "slug": "cognition/nback-training",
  "inputs": {
    "nbDur": "1350",
    "nbIsi": "500"
  },
  "expect": [
    "1350"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/schulte-table",
  "inputs": {
    "scMode": "letter"
  },
  "expect": [
    "letter"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/stroop-test",
  "inputs": {
    "stTimeout": "3750"
  },
  "expect": [
    "3750"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/time-perception",
  "inputs": {
    "bSel": "90"
  },
  "expect": [
    "90"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
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

  console.log("==== cognition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
