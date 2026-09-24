#!/usr/bin/env node
/**
 * 第 24 道门禁：edu 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：exam-gpa-calculator / gpa-calculator / grade-weight-calculator / grade-calculator
 *       （依赖动态添加课程行，框架无法注入）；reading-speed / edu-unit-converter /
 *       essay-word-counter / calc-3 / countdown-5（无 function calc，实时 oninput）。
 * 用法: node scripts/verify_edu_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "edu/calc-2",
    inputs: { score: "92", mean: "80", sd: "6", direction: "higher" },
    expect: ["2.0000", "97.72%"],
    ref: "Z=(92−80)/6=2.0000；normalCDF(2.0)×100≈97.72%；direction=higher → 有效Z=2.0000。"
       + "原 85/75/10 为默认态（Z=1.0000/84.13）；等级词「优秀」两态同现 ⇒ 不入断言。",
  },
  {
    slug: "edu/calc-4",
    inputs: { currentScore: "80", currentWeight: "60", targetScore: "90", remainingParts: "2" },
    expect: ["25.00", "10.00"],
    ref: "剩余权重=100−60=40.0%；还需加权分=90−80=10.00；剩余考核均分=10/40×100=25.00；每项=25.00；25≤60 → 目标可行",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { examName: "t", total: "100", totalQ: "100", correct: "90", perQ: "0", passLine: "60" },
    expect: ["优秀", "4.0", "90"],
    ref: "perQ=0 → score=90/100×100=90；rate=90%；gpa(rate≥90→4.0)；grade 优秀 🏆",
  },
  {
    slug: "edu/quiz-score-percentage",
    inputs: { total: "50", correct: "40", points: "2" },
    expect: ["80"],
    ref: "pct=40/50×100=80%；score=40×2=80；grade A 很好 👍",
  },
  {
    slug: "edu/convert-2",
    inputs: { val: "#FF0000", from: "hex", to: "rgb" },
    expect: ["rgb(255, 0, 0)"],
    ref: "HEX #FF0000 → R255 G0 B0 → rgb(255, 0, 0)",
  },
  {
    slug: "edu/convert-3",
    inputs: { val: "FF", from: "16", to: "10" },
    expect: ["255"],
    ref: "parseInt('FF',16)=255；toString(10)='255'",
  },
  {
    slug: "edu/convert-area-volume",
    inputs: { val: "1", rate: "1", from: "1", to: "1000" },
    expect: ["0.001000"],
    ref: "r=1×1×1/1000=0.001000（toFixed(6)）",
  },
  {
    slug: "edu/xml-html-css-geshihua-yiyou-kebuchong",
    inputs: { src: '<div class="a"><p>hi</p></div>', lang: "html", indent: "4" },
    expect: ["原 30 → 新 36", "缩进宽度：4 空格"],
    ref: "HTML 缩进 4 空格：30 字符 → 36 字符（+2 换行 +4 缩进空格），3 行，最大嵌套深度 2 层",
  },
  // 注：edu/stats 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
  {
    slug: "edu/assessor-27",
    inputs: { d1: "8", d2: "7", d3: "6", d4: "9", d5: "7", d6: "8" },
    expect: ["7.50", "4级-管理级"],
    ref: "avg=(8+7+6+9+7+8)/6=45/6=7.50；7.50≥6.5 且 <8 → 4级-管理级",
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "400", imgs: "0", format: "essay", paper: "a4", fontSize: "1" },
    expect: ["2 页（约）"],
    ref: "effectivePer=400(essay)×1(a4)×0.8(font1)=320；effectiveW=400×(1+0)=400；pages=400/320=1.25 → ceil=2 页（单字符“2”会被默认 5000 字结果里的其他数字命中 → 逃生项）",
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
  console.log("==== edu calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();