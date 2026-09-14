#!/usr/bin/env node
/**
 * 第 41 道门禁：ophthalmology 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值/示例预设，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除（无确定性数值输出，stub 无验证意义）：
 *   - 图形/画布类：amsler-grid-test / astigmatism-chart / eye-chart-toolkit / ishihara-test（canvas 绘制）
 *   - 分区点选/问卷类：fluorescein-staining / meibomian-grading / osdi-scale / pupil-reflex /
 *     rater-7 / rater-8 / self-assess-2 / visual-fatigue-vas / amblyopia-stereopsis
 *   - 自适应问答类：vision-screening-21（多步自适应，非一次函数）
 *   - 其余计算页（calc-length-1 / corneal-endothelium / iol-power / refraction-error / strabismus-angle）
 *     部分被上方同类覆盖或依赖 tab 状态，见各自归并说明。
 * 用法: node scripts/verify_ophthalmology_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "ophthalmology/analysis-12",
    inputs: { data: "11,23,29,41" },
    expect: ["26.00", "10.82"],
    ref: "均值=(11+23+29+41)/4=26.00；中位数=(23+29)/2=26.00；方差=((−15)²+(−3)²+3²+15²)/4=117→σ=10.82（默认数据 10..80→均值45.00/σ22.91，避开）" },

  { slug: "ophthalmology/axial-length",
    inputs: { al: "24.0", vMeas: "1555", eyeType: "1532" },
    expect: ["23.645"],
    ref: "校正后眼轴=24.0×(1532/1555)=23.645mm（默认 23.5/1532/1555→23.853，避开）" },

  { slug: "ophthalmology/calc-1",
    inputs: { iop: "20", cct: "600" },
    expect: ["23.9"],
    ref: "Doughty 线性校正：20+((600−544)/10)×0.7=23.92→23.9mmHg（默认空→提示输入，避开）" },

  { slug: "ophthalmology/cd-ratio",
    inputs: { od: "0.8", os: "0.3" },
    expect: ["0.80", "高度可疑"],
    ref: "OD C/D=0.80>0.7→高度可疑（默认 0.4/0.5→未见异常，避开）" },

  { slug: "ophthalmology/convert-42",
    inputs: { from: "sn", val: "40", to: "log" },
    expect: ["0.30"],
    ref: "Snellen 20/40→小数=20/40=0.5→logMAR=−log10(0.5)=0.30（默认 dec→dec,1.0→1.00，避开）" },

  { slug: "ophthalmology/corneal-curvature",
    inputs: { k1: "42.00", k2: "45.00", ax: "10" },
    expect: ["3.00", "顺规(WTR)"],
    ref: "角膜散光=|45−42|=3.00D；陡峭轴=norm180(10+90)=100°→60–120→顺规(WTR)（默认 42.5/43.75/90→1.25/逆规，避开）" },

  { slug: "ophthalmology/detector-6",
    inputs: { age: "5", method: "titmus", sa: "150" },
    expect: ["边界值"],
    ref: "5岁阈值=100角秒；150>100 且 ≤200→边界值（默认 age=3/sa=40→阈值200→正常，避开）" },

  { slug: "ophthalmology/iop-correction",
    inputs: { iop: "20", cct: "500" },
    expect: ["21.1", "正常偏薄"],
    ref: "四法均值=(Ehlers 21.42+Doughty 20.84+Feltgen 21.50+比值 20.8)/4=21.14→21.1；CCT 500∈[500,540)→正常偏薄（默认 18/545→17.4/正常，避开）" },

  { slug: "ophthalmology/oct-rnfl",
    inputs: { age: "40", g: "70", s: "60", i: "70", n: "50", t: "40" },
    expect: ["102"],
    ref: "年龄校正预期全局 RNFL=100−(40−50)×0.2=102μm（默认 age=60→98，且默认 78μm 已触发同样结论文案，故仅断言唯一数值 102，避开）" },

  { slug: "ophthalmology/pterygium-measurement",
    inputs: { cd: "12", head: "3.0", width: "4.0", length: "5.0" },
    expect: ["50.0"],
    ref: "角膜半径=12/2=6mm；遮盖比=3.0/6×100=50.0%（默认 11.5/2.0→34.8%，避开；T2 为两态共有文案故不断言）" },

  { slug: "ophthalmology/tear-breakup-time",
    inputs: { but: "4" },
    expect: ["4.0", "明显异常"],
    ref: "BUT=4<5秒→明显异常（默认 BUT=7→泪膜不稳定，避开）" },

  { slug: "ophthalmology/visual-acuity-converter",
    inputs: { type: "snellen20", value: "40" },
    expect: ["20/40"],
    ref: "Snellen 20/40→小数 0.5→logMAR 0.30→Snellen 20ft=20/40（默认 20/1→正常，避开）" },

  { slug: "ophthalmology/visual-field-analysis",
    inputs: { md: "-8", psd: "4.2", vfi: "85" },
    expect: ["-8.0"],
    ref: "MD=−8 显示 −8.0 dB（默认 −6.5 与真实值同为'中期'分期文案，故仅断言唯一数值 −8.0，避开）" },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const errs = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`  OK ${c.slug} (${r.via})`);
    } else {
      errs.push(c);
      console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 400)}`);
    }
  }
  console.log(`\n==== ophthalmology calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
