#!/usr/bin/env node
/**
 * 第 27 道门禁：optical 分类计算正确性验证（6 个确定性光学/视光工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 覆盖：调节幅度(Hofstetter)、抗疲劳下加光、瞳高占比、周边离焦、棱镜移心(普伦蒂斯)、AC/A(梯度法)。
 * 用法: node scripts/verify_optical_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "optical/accommodation-amplitude",
    inputs: { age: "40" },
    expect: ["6.50"],
    ref: "Hofstetter 平均 A=18.5−0.30×40=6.50 D（最小 15−0.25×40=5.00，最大 25−0.40×40=9.00）",
  },
  {
    slug: "optical/anti-fatigue-design",
    inputs: { age: "48", workDist: "30", rx: "0" },
    expect: ["0.50"],
    ref: "平均 A=18.5−0.30×48=4.10；调节需求=100/30=3.33；保留 1/3=1.37；可用=2.73；Add=max(0,3.33−2.73)=0.60→量化0.25D=0.50D",
  },
  {
    slug: "optical/pupil-height",
    inputs: { pupilToBottom: "18", frameB: "30" },
    expect: ["60"],
    ref: "占比=18/30×100=60%（默认方法 direct）",
  },
  {
    slug: "optical/peripheral-defocus",
    inputs: { central: "1", peripheral: "4", angle: "20" },
    checks: ["single"],
    expect: ["+3.00", "3.00D"],
    ref: "RPD=周边−中央=4−1=3.00 D（radio lens=single 经 checks 注入，规避 stub :checked 返回 null）",
  },
  {
    slug: "optical/prism-decentration",
    inputs: { power: "5", prism: "3", base: "BO" },
    expect: ["6.00"],
    ref: "页面默认 prism 分支（setMode 在 stub 下报错但 calc 走 prism 分支）：移心量 c=P/|F|=3/5=0.6cm→6.00mm；普伦蒂斯 P=c×|F|",
  },
  {
    slug: "optical/aca-ratio",
    inputs: { nearPhoria: "2", nearPhoriaLens: "8", lens: "4" },
    expect: ["1.50"],
    ref: "默认 gradient 法：AC/A=(加镜后隐斜−裸眼隐斜)/|镜片度|=(8−2)/4=1.50 Δ/D",
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== optical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();