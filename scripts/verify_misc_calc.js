#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "math/complex-number",
  "inputs": {
    "aRe": "6",
    "aIm": "4",
    "bRe": "1",
    "bIm": "-2"
  },
  "expect": [
    "(33.690068°)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "math/function-plotter",
  "inputs": {
    "xMin": "-10",
    "xMax": "10"
  },
  "clicks": [
    'setType("quadratic");document.getElementById("p_a").value="0";document.getElementById("p_b").value="10";document.getElementById("p_c").value="0";draw()'
  ],
  "expect": [
    "y = 0x² + 10x + 0"
  ],
  "ref": "参数输入 p_a/p_b 由 renderParams() 动态注入（静态 HTML 无默认值，inputs 注入无法被判别器回退），故改用点击序列切到二次函数并写入 a=0/b=10/c=0。旧实现 v('p_a')||1 把系数 0 改成 1（图例 y = 1x² + 10x + 0，零幅走形）。默认态为一次函数 y = 1x + 0，注入失败（clicks 被清空）时不命中。原用例锚 '-15' 是输入回显（恒绿）已删除。"
},
{
  "slug": "math/magic-square",
  "inputs": {
    "order": "8"
  },
  "expect": [
    "369"
  ],
  "ref": "auto-restore"
},
// 已移除 science/physics-constants（inputs:{}，expect ["原子物理"]）。
// 原因：该页为纯常量清单，默认态已渲染全部常数与全部分类标签；setCat() 只做「顺序保持型」过滤、
// 搜索框同理，emptyHint 只切 style.display ⇒ 任何注入态输出恒为默认全量的子序列，无任何可判别增量，
// 无法改出注入态专属锚 ⇒ 按纪律删除而非保留 skip。
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

  console.log("==== misc calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
