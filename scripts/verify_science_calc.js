#!/usr/bin/env node
/**
 * science 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）。
 * 用例以物理 / 化学 / 统计的确定公式为主，期望值一律由标准公式独立复算得出，不凭记忆。
 *
 * 用法：
 *   node scripts/verify_science_calc.js                       # 跑全部用例
 *   node scripts/verify_science_calc.js newtons-second molar-mass-calculator  # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  // ── 经典力学 ─────────────────────────────────────────────────
  {
    slug: "science/newtons-second",
    inputs: { m: "10", a: "3" },
    expect: ["30.0 N"],
    ref: "牛顿第二定律 F = m·a；10 × 3 = 30 → 30.0 N（页面 toFixed(1)）",
  },
  {
    slug: "science/kinetic-energy",
    inputs: { m: "10", v: "5" },
    expect: ["125.0 J"],
    ref: "动能 E = ½mv²；0.5 × 10 × 25 = 125 → 125.0 J（页面 toFixed(1)）",
  },
  {
    slug: "science/pendulum-period",
    inputs: { L: "1", g: "9.81" },
    expect: ["2.006 s"],
    ref: "单摆周期 T = 2π√(L/g)；2π√(1/9.81) = 2.0064… → 2.006 s（页面 toFixed(3)）",
  },

  // ── 电学（欧姆定律）─────────────────────────────────────────
  {
    slug: "science/ohms-law-calculator",
    inputs: { v: "10", r: "5" }, // calcVar 默认 'i'（求解电流）
    expect: ["2.00 C"],
    ref: "欧姆定律 I = V/R；10 ÷ 5 = 2 A → 电荷量 Q=I=2 → 2.00 C（resQ，toFixed(2)）",
  },

  // ── 化学（摩尔质量 / pH）────────────────────────────────────
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "H2O" },
    expect: ["18.016"],
    ref: "H₂O 摩尔质量 = 1.008×2 + 16.00 = 18.016 g/mol（页面 total.toFixed(3)，O 原子量取 16.00）",
  },
  {
    slug: "science/ph-calculator",
    inputs: { input: "3" }, // mode 默认 'ph'
    expect: ["3.00", "1.000e-3"],
    ref: "pH=3 → [H⁺]=10⁻³=1.000e-3 mol/L；resPh=3.00、resH=1.000e-3（toFixed(2)/toExponential(3)）",
  },

  // ── 统计 ───────────────────────────────────────────────────
  {
    slug: "science/z-score-calculator",
    inputs: { x: "75", mu: "50", sigma: "10" },
    expect: ["2.5"],
    ref: "标准分数 Z = (x−μ)/σ；(75−50)/10 = 2.5（fmt(z)，输出 'Z = 2.5'）",
  },
  {
    slug: "science/mean-calculator",
    inputs: { data: "1,2,4" },
    expect: ["2.333"],
    ref: "算术平均 = (1+2+4)/3 = 2.333（fmt：round(x·1e10)/1e10 后 toLocaleString，默认最多 3 位小数）",
  },
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 200));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
