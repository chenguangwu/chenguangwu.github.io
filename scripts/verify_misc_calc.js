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
    "xMin": "-15",
    "xMax": "10",
    "yMin": "-10",
    "yMax": "10",
    "p_a": "0",
    "p_b": "10"
  },
  "expect": [
    "y = 0x + 10"
  ],
  "ref": "旧实现 v('p_a')||1 把斜率 a=0（水平线/零幅）改成 1，图例与图形走形。修复后 0 原样参与：线性图例 y = 0x + 10。默认 a=1,b=0 ⇒ y = 1x + 0，不命中；原用例锚 '-15' 是输入回显（恒绿）已删除。"
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
{
  "slug": "science/physics-constants",
  "inputs": {},
  "expect": [
    "原子物理"
  ],
  "ref": "auto-restore(default)；**2026-09-26 复核判死（勿重复评估）**：setCat(k) 走 initTabs()+renderList()，前者只给按钮切 active class（CATS 名称文本全部常驻），后者对 CONSTANTS 做 `filter(curCat==='all'||c.cat===curCat)` 后 map 渲染 —— 过滤是**顺序保持型**（命中行的顺序与原表一致）⇒ 注入态输出恒为「默认全量」的顺序子序列，任何常数名/数值都已被默认态包含（§10.5 B 组判据）。搜索框同理。`emptyHint` 只切 style.display（collectStrings 不采 style）。"
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

  console.log("==== misc calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
