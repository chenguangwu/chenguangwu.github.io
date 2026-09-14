#!/usr/bin/env node
/**
 * 第 33 道门禁：machinery 分类计算正确性验证（21 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：calc-gear / calc-weld / calc-strength（单选 radio 分支 + 材料系数表）、
 *       gear / calc-gear-3 斜齿锥齿分支、estimate-gravity 多形状分支（仅覆盖矩形板）、
 *       drive-2 蜗杆（MU_DATA 材料对表）、tolerance / tolerance-1（IT 公差表查表）、
 *       thread-recognize / temp-hardness（型号/硬度查表）、analysis-*（文本/多指标行）。
 * 用法: node scripts/verify_machinery_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "machinery/calc-gear-1", inputs: { v_m: "3", v_z: "30", v_a: "20" }, expect: ["90.000"], ref: "分度圆 d=m·z=3×30=90.000（默认 z=24→72，避开）" },
  { slug: "machinery/calc-64", inputs: { basic: "50", holeES: "25", holeEI: "0", shaftes: "-9", shaftei: "-25" }, expect: ["0.0500"], ref: "最大间隙 Xmax=(ES−ei)/1000=(25−(−25))/1000=0.0500 mm（最小间隙 Xmin=(EI−es)/1000=(0−(−9))/1000=0.0090）" },
  { slug: "machinery/calc-89", inputs: { v_D: "200", v_d: "60", v_mu: "0.3", v_F: "5000", v_z: "2", v_n: "1000" }, expect: ["195.00"], ref: "平均半径 Rm=(D+d)/4=65 mm；扭矩 T=μ·F·(Rm/1000)·z=0.3×5000×0.065×2=195.00 N·m（默认 d=120/μ=0.25 避开）" },
  { slug: "machinery/strength-7", inputs: { v_d: "10", v_t: "6", v_n: "2", v_w: "60", v_f: "50", v_tau: "120", v_sigc: "300", v_sigt: "200" }, expect: ["318.31"], ref: "剪切应力 τ=F/ΣA=50000/(2×π×10²/4)=50000/157.0796=318.31 MPa（默认 d=16/n=4 避开）" },
  { slug: "machinery/strength-6", inputs: { v_d: "10", v_b: "8", v_h: "8", v_L: "40", v_T: "100", v_sp: "200", v_tau: "100", v_type: "square" }, expect: ["125.00"], ref: "方头平键 l=L=40；挤压应力 σp=4T/(d·h·l)=4×100000/(10×8×40)=125.00 MPa（T 输入 N·m 内部×1000→N·mm；默认 d=40 避开）" },
  { slug: "machinery/speed-cutting-feed", inputs: { v0: "100", v1: "200", v2: "50" }, expect: ["400.00"], ref: "切削参数：r=p0·p1/p2=100×200/50=400.00（该页为通用乘除计算）" },
  { slug: "machinery/area-dosage-1", inputs: { v_area: "100", v_dft: "50", v_vs: "40", v_te: "60" }, expect: ["12.50"], ref: "理论涂布率=10·VS/DFT=10×40/50=8 m²/L；理论用量=area/涂布率=100/8=12.50 L（默认 area=10/DFT=80 避开）" },
  { slug: "machinery/energy-2", inputs: { v_J: "2", v_n1: "1500", v_n2: "0", v_t: "5" }, expect: ["24.67"], ref: "ω₁=2π·1500/60=157.0796 rad/s；制动能耗=½J·ω₁²=½×2×24674.0=24674 J=24.67 kJ（默认 J=2.5/t=3 避开）" },
  { slug: "machinery/thread-drive", inputs: { v_d2: "20", v_lead: "4", v_f: "10", v_mu: "0.1", v_muc: "0.05", v_dc: "30" }, expect: ["3.64"], ref: "螺纹升角 λ=atan(L/(π·d₂))=atan(4/(π×20))=3.64°（当量摩擦角 ρ=atan0.1=5.71°；默认 d2=36.5/lead=7 避开）" },
  { slug: "machinery/estimate-lifespan-bearing", inputs: { loadC: "30000", loadP: "5000", speed: "1500", bearingType: "ball", reliability: "90", lubrication: "1.0" }, expect: ["216.00"], ref: "球轴承 L₁₀=(C/P)^3=(30000/5000)³=216.00 百万转（默认 C=33.5/P=5 避开）" },
  { slug: "machinery/estimate-lifespan-bearing", inputs: { loadC: "50000", loadP: "10000", speed: "1000", bearingType: "roller", reliability: "90", lubrication: "1.0" }, expect: ["213.75"], ref: "滚子轴承 L₁₀=(C/P)^(10/3)=5^3.3333=213.75 百万转（默认 C=33.5 避开）" },
  { slug: "machinery/banjinzhewanzhankai", inputs: { v_t: "2", v_ang: "90", v_r: "1", v_k: "0.44", v_a: "50", v_b: "50" }, expect: ["96.953"], ref: "R/t=1/2；OSSB=(R+t)·tan(45°)=3；BA=(R+K·t)·(π·90/180)=1.88×1.5708=2.953；BD=2×3−2.953=3.047；展开长=a+b−BD=100−3.047=96.953 mm（默认 R=3 避开）" },
  { slug: "machinery/pressure-4", inputs: { v_z: "20", v_m: "3", v_a: "30", v_root: "flat" }, expect: ["60.000"], ref: "花键分度圆 D=m·z=3×20=60.000 mm（基圆 Db=D·cos30°=51.962；默认 z=24/m=2 避开）" },
  { slug: "machinery/estimate-gravity", inputs: { shape: "plate", material: "steel", plateL: "100", plateW: "60", plateH: "10" }, expect: ["471.000"], ref: "矩形板 V=100×60×10=60000 mm³=60 cm³；质量=V·ρ=60×7.85=471.000 g（默认 plateW=50 避开，钢密度 7.85）" },
  { slug: "machinery/zhujian-bamoxiedu-sheji", inputs: { v0: "30", v1: "40" }, expect: ["35.0"], ref: "通用判读页：综合评分=(a+b)/2=(30+40)/2=35.0 → 轻度（默认 100/50=75 避开）" },
  { slug: "machinery/calc-gear-3", inputs: { v_type: "spur", v_sm: "3", v_sz: "30", v_sa: "20" }, expect: ["90.000"], ref: "直齿（spur）分度圆 d=m·z=3×30=90.000（默认 z=24→72 避开）" },
  { slug: "machinery/frequency-17", inputs: { v_m: "100", v_k: "25000", v_f: "20", v_z: "0.05" }, expect: ["2.516"], ref: "固有频率 fn=(1/2π)√(k/m)=(1/2π)√(25000/100)=15.8114/6.2832=2.516 Hz（默认 k=50000/f=25 避开）" },
  { slug: "machinery/calc-lifespan-belt", inputs: { D1: "90", D2: "225", center: "600", n1: "1450", power: "7.5", beltType: "v" }, expect: ["2.50"], ref: "传动比 i=D₂/D₁=225/90=2.50（默认 D1=100/D2=300→3.00 避开；带速 v=π·D₁·n₁/60000=6.83 m/s）" },
  { slug: "machinery/lifespan-bearing", inputs: { v_C: "60000", v_P: "5000", v_n: "1200", v_type: "ball" }, expect: ["1728.00"], ref: "球轴承 L₁₀=(C/P)^3=(60000/5000)³=12³=1728.00 百万转（L₁₀h=1e6/(60×1200)×1728=24000 h；默认 C=22500/P=2500→729.00 避开）" },
  { slug: "machinery/lifespan-bearing-1", inputs: { v_F: "8000", v_d: "60", v_bd: "1.5", v_n: "1000", v_Lh: "20000" }, expect: ["4.654"], ref: "轴承宽 B=d·bd=60×1.5=90；平均压强 p=F/(d·B)=8000/5400=1.481 MPa；线速度 v=π·d·n/60000=3.142 m/s；pV=1.481×3.142=4.654 MPa·m/s（默认 F=5000/d=50 避开）" },
  { slug: "machinery/runhuaxitongsheji", inputs: { v_d: "100", v_l: "120", v_n: "1000", v_w: "20", v_eta: "30", v_psi: "1.5", v_dt: "20" }, expect: ["8.73"], ref: "投影面积=d·L=12000；比压 p=W/(d·L)=20000/12000=1.67 MPa；表面速度 v=π·d·n/60000=5.24 m/s；PV=p·v=1.67×5.24=8.73 MPa·m/s（默认 d=80/W=10 避开）" },
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
      console.log(`  OK ${c.slug}`);
    } else {
      errs.push(c);
      console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      console.log(`     ref: ${c.ref}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 300)}`);
    }
  }
  console.log(`\n==== machinery calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
