#!/usr/bin/env node
/**
 * 第 34 道门禁：math 分类计算正确性验证（31 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经复核「不等于」默认值输出，杜绝假通过。
 * 跳过：geometry-calculator / calculus-tools / formula-calculator（图形/函数选择式交互 demo）；
 *       equation-solver（需先经 renderTypes/renderInputs 建立 selectedType 状态）。
 * 用法: node scripts/verify_math_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "math/percent-change", inputs: { old: "50", new: "75" }, expect: ["50.00"], ref: "变化率=(new−old)/old×100=(75−50)/50×100=50.00%（默认 80→100 避开）" },
  { slug: "math/quadratic-solver", inputs: { a: "1", b: "-5", c: "6" }, expect: ["3.0000"], ref: "Δ=b²−4ac=25−24=1；x₁=(5+1)/2=3.0000（x₂=2.0000；默认 1,−3,2 避开）" },
  { slug: "math/log-base", inputs: { x: "81", b: "3" }, expect: ["4.000000"], ref: "log₃81=ln81/ln3=4.000000（默认 1000,10 避开）" },
  { slug: "math/gcd-lcm", inputs: { a: "1071", b: "462" }, expect: ["23562"], ref: "gcd(1071,462)=21；lcm=1071×462/21=23562（默认 48,36 避开）" },
  { slug: "math/distance-2d", inputs: { x1: "0", y1: "0", x2: "6", y2: "8" }, expect: ["10.0000"], ref: "d=√(6²+8²)=10.0000（默认 (0,0)-(3,4)=5.0000 避开）" },
  { slug: "math/slope-line", inputs: { x1: "0", y1: "0", x2: "2", y2: "6" }, expect: ["3.0000"], ref: "斜率 k=(6−0)/(2−0)=3.0000（默认 (1,2)-(4,8)=2.0000 避开）" },
  { slug: "math/fibonacci-n", inputs: { n: "30" }, expect: ["832,040"], ref: "F(30)=832040（千分位 832,040；默认 n=20→6765 避开）" },
  { slug: "math/factorial-calc", inputs: { n: "12" }, expect: ["4.7900e+8"], ref: "12!=479001600=4.7900e+8（科学计数法；默认 n=10 避开）" },
  { slug: "math/combination", inputs: { n: "12", r: "5" }, expect: ["792"], ref: "C(12,5)=792（默认 10,3→120 避开）" },
  { slug: "math/permutation", inputs: { n: "9", r: "4" }, expect: ["3,024"], ref: "P(9,4)=9×8×7×6=3024（千分位 3,024；默认 10,3→720 避开）" },
  { slug: "math/root-calc", inputs: { x: "27" }, expect: ["3.000000"], ref: "∛27=3.000000（√27=5.196152；默认 x=2 避开）" },
  { slug: "math/power-calc", inputs: { x: "3", y: "7" }, expect: ["2,187"], ref: "3⁷=2187（千分位 2,187；默认 2^10 避开）" },
  { slug: "math/modulo-calc", inputs: { a: "1000", b: "7" }, expect: ["6.0000"], ref: "1000 mod 7=6（1000=142×7+6；默认 17 mod 5=2 避开）" },
  { slug: "math/law-of-sines", inputs: { b: "12", A: "40", B: "60" }, expect: ["8.907"], ref: "a=b·sinA/sinB=12×sin40°/sin60°=12×0.642788/0.866025=8.907（默认 10,30°,45° 避开）" },
  { slug: "math/law-of-cosines", inputs: { a: "5", b: "7", C: "60" }, expect: ["6.245"], ref: "c=√(a²+b²−2ab·cosC)=√(25+49−70×0.5)=√39=6.245（默认 3,4,90° 避开）" },
  { slug: "math/dot-product", inputs: { ax: "2", ay: "3", az: "4", bx: "5", by: "6", bz: "7" }, expect: ["56.00"], ref: "A·B=2×5+3×6+4×7=10+18+28=56.00（默认 (1,2,3)·(4,5,6)=32.00 避开）" },
  { slug: "math/determinant-2x2", inputs: { a: "3", b: "1", c: "2", d: "5" }, expect: ["13.00"], ref: "|A|=ad−bc=3×5−1×2=13.00（默认 1,2,3,4→−2.00 避开）" },
  { slug: "math/geometric-series-sum", inputs: { a: "3", r: "2", n: "5" }, expect: ["93.0000"], ref: "Sₙ=a(1−rⁿ)/(1−r)=3×(1−32)/(1−2)=93.0000（默认 1,0.5,4 避开）" },
  { slug: "math/arithmetic-series-sum", inputs: { n: "20", a1: "2", an: "40" }, expect: ["420.00"], ref: "Sₙ=n(a₁+aₙ)/2=20×(2+40)/2=420.00（默认 10,1,10 避开）" },
  { slug: "math/nth-term-geometric", inputs: { a1: "3", r: "2", n: "6" }, expect: ["96.000"], ref: "aₙ=a₁·r^(n−1)=3×2⁵=96.000（默认 2,3,4 避开）" },
  { slug: "math/herons-area", inputs: { a: "5", b: "5", c: "6" }, expect: ["12.000"], ref: "s=(5+5+6)/2=8；A=√(s(s−a)(s−b)(s−c))=√(8×3×3×2)=√144=12.000（默认 3,4,5 避开）" },
  { slug: "math/exponent-solve", inputs: { a: "3", b: "81" }, expect: ["4.0000"], ref: "由 3^x=81 得 x=ln81/ln3=4.0000（默认 2,8 避开）" },
  { slug: "math/quadratic-discriminant", inputs: { a: "2", b: "3", c: "5" }, expect: ["-31.00"], ref: "Δ=b²−4ac=9−40=−31.00（默认 1,−3,2→1.00 避开）" },
  { slug: "math/circular-permutation", inputs: { n: "7" }, expect: ["720"], ref: "圆排列数=(n−1)!=6!=720（默认 n=5→24 避开）" },
  { slug: "math/combination-repetition", inputs: { n: "6", r: "4" }, expect: ["126"], ref: "可重复组合 C(n+r−1,r)=C(9,4)=126（默认 5,3→35 避开）" },
  { slug: "math/prime-check", inputs: { n: "91" }, expect: ["不是质数"], ref: "91=7×13，非质数（默认 n=97 为质数，避开）" },
  { slug: "math/arithmetic-mean-math", inputs: { xs: "10, 20, 30, 40" }, expect: ["25.0000"], ref: "算术平均=(10+20+30+40)/4=25.0000（默认 1,2,3,4,5→3.0000 避开）" },
  { slug: "math/multinomial-coefficient", inputs: { n: "8", k1: "4", k2: "2", k3: "2" }, expect: ["420"], ref: "多项式系数=8!/(4!2!2!)=40320/96=420（默认 6,3,2,1→60 避开）" },
  { slug: "math/calc-1", inputs: { ofA: "160", ofP: "25" }, expect: ["40.0000"], ref: "求百分量模式：160 的 25%=40.0000（默认 200 的 15%=30.0000 避开）" },
  { slug: "math/calc-3", inputs: { a: "6", b: "8", c: "" }, expect: ["10.00"], ref: "勾股定理求斜边：c=√(6²+8²)=10.00（默认 3,4→5.00 避开）" },
  { slug: "math/calc-4", inputs: { radius: "7" }, expect: ["153.9380"], ref: "圆面积=πr²=π×49=153.9380（周长=43.9823；默认 r=5 避开）" },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== math calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();