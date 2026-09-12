#!/usr/bin/env node
/**
 * ai 分类关键计算逻辑独立验证（收口批次 C）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_ai_calc.js
 *   node scripts/verify_ai_calc.js cosine-similarity sigmoid
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 分类准确率评估（混淆矩阵四指标）────────────────────────
  {
    slug: "ai/ai",
    inputs: { tp: "80", fp: "10", fn: "15", tn: "95" },
    expect: ["87.50", "88.89", "84.21", "86.49"],
    ref: "N=200；准确率=(80+95)/200×100=87.50；精确率=80/90×100=88.89；"
       + "召回率=80/95×100=84.21；F1=2×80/(2×80+10+15)×100=160/185×100=86.49",
  },

  // ── 欧氏距离（含曼哈顿、余弦）──────────────────────────────
  {
    slug: "ai/ai-4",
    inputs: { a1: "1", a2: "2", a3: "3", b1: "4", b2: "5", b3: "6" },
    expect: ["5.1962", "9.0000", "0.9746"],
    ref: "欧氏=√(9+9+9)=√27=5.1962；曼哈顿=3+3+3=9.0000；"
       + "余弦=(4+10+18)/(√14·√77)=32/√1078=32/32.83291=0.9746",
  },

  // ── 交叉熵损失 ─────────────────────────────────────────────
  {
    slug: "ai/cross-entropy",
    inputs: { y: "1", p: "0.8", n: "100" },
    expect: ["0.2231", "22.3144"],
    ref: "单样本=−[1·ln0.8+0·ln0.2]=−ln0.8=0.22314355→0.2231；批量=0.22314355×100=22.3144",
  },

  // ── Sigmoid 与对数几率 ─────────────────────────────────────
  {
    slug: "ai/sigmoid",
    inputs: { z: "2", threshold: "0.5" },
    expect: ["0.880797", "正类", "2.0000"],
    ref: "σ(2)=1/(1+e⁻²)=0.880797；0.880797≥0.5→正类；"
       + "对数几率=ln[p/(1−p)]=ln(0.880797/0.119203)=ln7.389056=2.0000（应还原为 z）",
  },

  // ── Softmax 概率分布 ───────────────────────────────────────
  {
    slug: "ai/softmax",
    inputs: { z1: "2", z2: "1", z3: "0.5", z4: "0.2" },
    expect: ["56.94", "20.95", "12.71", "9.41"],
    ref: "e²=7.389056, e¹=2.718282, e^0.5=1.648721, e^0.2=1.221403；Σ=12.977462；"
       + "P1=7.389056/12.977462×100=56.94；P2=20.95；P3=12.71；P4=9.41",
  },

  // ── Cohen's Kappa ──────────────────────────────────────────
  {
    slug: "ai/cohens-kappa",
    inputs: { tp: "50", tn: "40", fp: "10", fn: "5" },
    expect: ["0.857", "0.503", "0.712"],
    ref: "N=105；Po=(50+40)/105=0.857；Pe=[(60×55)+(45×50)]/105²=5550/11025=0.503；"
       + "κ=(0.857143−0.503401)/(1−0.503401)=0.353741/0.496599=0.712",
  },

  // ── AUC 秩次法（Mann-Whitney U）───────────────────────────
  {
    slug: "ai/auc-rank",
    inputs: { nPos: "20", nNeg: "30", sumRank: "400" },
    expect: ["190", "0.3167"],
    ref: "U=ΣRank − nPos(nPos+1)/2 = 400 − 20×21/2 = 400−210=190；"
       + "AUC=U/(nPos·nNeg)=190/(20×30)=190/600=0.3167",
  },

  // ── 学习率指数衰减 ─────────────────────────────────────────
  {
    slug: "ai/lr-decay",
    inputs: { lr0: "0.001", gamma: "0.95", epoch: "10" },
    expect: ["0.000599"],
    ref: "lr=lr₀×γ^epoch=0.001×0.95¹⁰=0.001×0.598736939=0.000598737→toFixed(6)=0.000599",
  },

  // ── Transformer 参数量 ─────────────────────────────────────
  {
    slug: "ai/transformer-params",
    inputs: { L: "12", d: "768", vocab: "30000" },
    expect: ["0.85", "0.23"],
    ref: "主体=12·L·d²/1e8=12×12×768²/1e8=84934656/1e8=0.85 亿；"
       + "嵌入=vocab×d/1e8=30000×768/1e8=23040000/1e8=0.23 亿",
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
      if (r.sample) console.log("     got: " + r.sample.slice(0, 300));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
