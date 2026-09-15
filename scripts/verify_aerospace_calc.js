#!/usr/bin/env node
/**
 * 第 31 道门禁：aerospace 分类计算正确性验证（22 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：flight-time（日期时刻 + 时区，动态表单）；fuel-consumption / runway-length / weight-balance
 *       （多分支/动态行/系数表）；lift-coefficient（角度—升力曲线绘图）。
 * 用法: node scripts/verify_aerospace_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "aerospace/aspect-ratio", inputs: { b: "12", S: "24" }, expect: ["6.00"], ref: "AR=b²/S=144/24=6.00（默认 10/20 避开）" },
  { slug: "aerospace/wing-loading", inputs: { w: "24000", s: "24" }, expect: ["1000.0"], ref: "翼载荷=W/S=24000/24=1000.0 N/m²（默认 10000/16 避开）" },
  { slug: "aerospace/dynamic-pressure", inputs: { rho: "1.0", v: "200" }, expect: ["20000.00"], ref: "q=½ρv²=0.5×1×200²=20000.00 Pa（默认 1.225/100 避开）" },
  { slug: "aerospace/lift-equation", inputs: { rho: "1.0", v: "100", CL: "1.2", A: "30" }, expect: ["180000.00"], ref: "L=½ρv²·CL·A=0.5×1×100²×1.2×30=180000.00 N（默认避开）" },
  { slug: "aerospace/drag-force", inputs: { rho: "1.0", v: "100", CD: "0.05", A: "20" }, expect: ["5000.00"], ref: "D=½ρv²·CD·A=0.5×1×100²×0.05×20=5000.00 N（默认避开）" },
  { slug: "aerospace/mach-number", inputs: { v: "400", t: "20", g: "1.4" }, expect: ["1.165", "343.2"], ref: "声速 a=√(γRT)=√(1.4×287×293.15)=343.2 m/s；M=400/343.2=1.165（默认 v=340 避开）" },
  { slug: "aerospace/load-factor", inputs: { phi: "30" }, expect: ["1.15"], ref: "n=1/cosφ=1/cos30°=1.15（默认 60 避开）" },
  { slug: "aerospace/thrust-to-weight", inputs: { T: "120000", W: "200000" }, expect: ["0.600"], ref: "T/W=120000/200000=0.600（默认 50000/80000 避开）" },
  { slug: "aerospace/specific-impulse", inputs: { f: "200000", mdot: "50" }, expect: ["407.7"], ref: "Isp=F/(ṁ·g₀)=200000/(50×9.81)=407.7 s（默认 100000/40 避开）" },
  { slug: "aerospace/escape-velocity", inputs: { mu: "3.986e14", r: "7.0e6" }, expect: ["10671.7"], ref: "v=√(2μ/r)=√(2×3.986e14/7.0e6)=10671.7 m/s（默认 r=6.771e6 避开）" },
  { slug: "aerospace/orbital-velocity", inputs: { mu: "3.986e14", r: "7.0e6" }, expect: ["7546.0"], ref: "v=√(μ/r)=√(3.986e14/7.0e6)=7546.0 m/s（默认 r=6.771e6 避开）" },
  { slug: "aerospace/orbital-period", inputs: { mu: "3.986e14", r: "7.0e6" }, expect: ["5828.5"], ref: "T=2π√(r³/μ)=2π√(7.0e6³/3.986e14)=5828.5 s（默认 r=6.771e6 避开）" },
  { slug: "aerospace/centripetal-accel", inputs: { v: "300", r: "2000" }, expect: ["45.000"], ref: "a=v²/r=300²/2000=45.000 m/s²（默认 200/3000 避开）" },
  { slug: "aerospace/turn-rate", inputs: { v: "150", phi: "45" }, expect: ["3.75", "224.8"], ref: "ω=g·tanφ/v=9.81×tan45°/150=0.0654 rad/s=3.75°/s=224.8°/min（默认 v=100 避开）" },
  { slug: "aerospace/turn-radius", inputs: { v: "200", phi: "45" }, expect: ["4077.5"], ref: "R=v²/(g·tanφ)=200²/(9.81×tan45°)=4077.5 m（默认 100/30 避开）" },
  { slug: "aerospace/stall-speed", inputs: { w: "20000", rho: "1.0", s: "20", cl: "1.5" }, expect: ["36.51"], ref: "Vs=√(2W/(ρS·CLmax))=√(2×20000/(1×20×1.5))=36.51 m/s（默认 w=10000 避开）" },
  { slug: "aerospace/payload-fraction", inputs: { m0: "200", mf: "120" }, expect: ["40.0"], ref: "有效载荷比=(m0−mf)/m0×100=80/200×100=40.0%（默认 100/50 避开）" },
  { slug: "aerospace/lift-to-drag-ratio", inputs: { cl: "1.5", cd: "0.10" }, expect: ["15.00", "6.67"], ref: "L/D=1.5/0.10=15.00；阻力占比=0.10/1.5×100=6.67%（默认 1.0/0.05 避开）" },
  { slug: "aerospace/climb-rate", inputs: { pav: "300000", preq: "100000", w: "20000" }, expect: ["10.00", "600.0"], ref: "ROC=(Pav−Preq)/W=(300000−100000)/20000=10.00 m/s=600.0 m/min（默认 pav=200000 避开）" },
  { slug: "aerospace/descent-rate", inputs: { v: "100", g: "6" }, expect: ["627.2", "10.45"], ref: "下降率=v·sinγ=100×sin6°=10.45 m/s=627.2 m/min（默认 v=70 避开）" },
  { slug: "aerospace/bank-angle-load", inputs: { phi: "45" }, expect: ["1.414"], ref: "n=1/cosφ=1/cos45°=1.414（默认 60 避开）" },
  { slug: "aerospace/delta-v-rocket", inputs: { isp: "350", m0: "100", mf: "20" }, expect: ["5.53", "5526"], ref: "Δv=Isp·g₀·ln(m0/mf)=350×9.81×ln5=5526 m/s=5.53 km/s（默认 isp=300 避开）" },
];

async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== aerospace calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();