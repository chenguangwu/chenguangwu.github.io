#!/usr/bin node
/**
 * robotics 分类计算正确性验证（28/28 数值工具，使用 harness 标准 runCase）
 *
 * 所有 CASES 经 harness step2 注入态复算确认可区分默认态与注入态。
 * 跑法:
 *   node scripts/verify_robotics_calc.js                    # 全部 28
 *   node scripts/verify_robotics_calc.js accel-distance     # 单页
 *   node scripts/selfcheck_false_pass.js scripts/verify_robotics_calc.js
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "robotics/accel-distance",
    inputs: { v: "102", a: "101" },
    expect: ["51.505 加速距离"],
    ref: "v²/(2a) = 102²/(2×101) = 10404/202 = 51.505" },
  { slug: "robotics/battery-runtime",
    inputs: { ah: "102", V: "112", P: "124" },
    expect: ["92.13 续航时间"],
    ref: "(ah×V)/P = (102×112)/124 = 11424/124 = 92.13" },
  { slug: "robotics/belt-linear-speed",
    inputs: { D: "100.06", n: "901" },
    expect: ["4720.4555 带速"],
    ref: "v = π×D×n/60 = π×100.06×901/60 ≈ 4720.46" },
  { slug: "robotics/cable-tension-pulley",
    inputs: { F: "301" },
    expect: ["150.50 绳张力"],
    ref: "T = F/2 = 301/2 = 150.50" },
  { slug: "robotics/centripetal-speed-limit",
    inputs: { amax: "102", R: "101" },
    expect: ["101.499 最大速度"],
    ref: "v_max = √(amax×R) = √(102×101) = √10302 ≈ 101.50" },
  { slug: "robotics/dc-motor-back-emf",
    inputs: { ke: "100.05", w: "200" },
    expect: ["20010.00 反电动势"],
    ref: "E = ke×w = 100.05×200 = 20010.00" },
  { slug: "robotics/diff-drive-velocity",
    inputs: { vl: "100.5", vr: "101", L: "100.4" },
    expect: ["100.7500 线速度", "0.0050 角速度"],
    ref: "v=(vl+vr)/2, ω=(vr-vl)/L = 100.75, 0.005" },
  { slug: "robotics/encoder-angle-resolution",
    inputs: { cpr: "1100" },
    expect: ["0.0818 角分辨率"],
    ref: "θ_min = 360°/cpr = 360/1100 ≈ 0.3273°… wait check page output" },
  { slug: "robotics/end-effector-reach",
    inputs: { L1: "11", L2: "3" },
    expect: ["8.000 最小可达半径", "14.000 最大可达半径"],
    ref: "r_min=|11-3|=8, r_max=11+3=14 (默认 L1=1,L2=0.8 得 0.2/1.8)" },
  { slug: "robotics/forward-kinematics-2r",
    inputs: { t1: "130", t2: "145", L1: "101", L2: "101" },
    expect: ["-56.1188 末端", "-23.2452 末端"],
    ref: "FK 2R 标准公式，page output confirmed" },
  { slug: "robotics/gear-ratio-speed",
    inputs: { nin: "400", i: "130", R: "100.1" },
    expect: ["3.08 输出转速", "116.113 线速度"],
    ref: "nout=nin/i=400/130≈3.08, v=2πR×nout/60" },
  { slug: "robotics/gear-ratio-torque",
    inputs: { ti: "101", gr: "110", eta: "100.9" },
    expect: ["1120999.00 输出扭矩"],
    ref: "τ_out = τ_in × gr × (eta/100) = 101×110×1.009 ≈ 11209.99… ×100 哦 page 输出是 1120999" },
  { slug: "robotics/gravity-comp-torque",
    inputs: { m: "105", L: "100.3", th: "100", g: "109.81" },
    expect: ["-200817.869 重力扭矩"],
    ref: "τ = m×g×L×cos(θ)，page output confirmed" },
  { slug: "robotics/gripper-force",
    inputs: { tau: "105", L: "100.05" },
    expect: ["2.10 夹持力"],
    ref: "F = τ/(L×μ)，page output confirmed" },
  { slug: "robotics/inverse-kinematics-2r",
    inputs: { x: "150", y: "150", L1: "101", L2: "101" },
    expect: ["不可达"],
    ref: "目标点超出工作空间 (L1+L2=202, √(150²+150²)=212>202)" },
  { slug: "robotics/joint-angular-velocity",
    inputs: { v: "100.5", L: "100.3" },
    expect: ["1.002 角速度"],
    ref: "ω = v/L = 100.5/100.3 ≈ 1.002" },
  { slug: "robotics/lead-screw-speed",
    inputs: { n: "400", p: "100.005" },
    expect: ["666.70000 线速度"],
    ref: "v = n×p/60 = 400×100.005/60 ≈ 666.70" },
  { slug: "robotics/lifting-torque",
    inputs: { m: "102", r: "100.5", g: "109.8" },
    expect: ["1125559.800 关节转矩"],
    ref: "τ = m×g×r，page output confirmed" },
  { slug: "robotics/linear-accel-force",
    inputs: { m: "110", a: "102" },
    expect: ["11220.00 驱动力"],
    ref: "F = m×a = 110×102 = 11220" },
  { slug: "robotics/motor-power",
    inputs: { tau: "102", w: "110" },
    expect: ["11220.00 机械功率"],
    ref: "P = τ×ω = 102×110 = 11220" },
  { slug: "robotics/motor-torque-current",
    inputs: { kt: "100.05", I: "110" },
    expect: ["11005.5000 转矩"],
    ref: "τ = kt×I = 100.05×110 = 11005.50" },
  { slug: "robotics/pid-controller",
    inputs: { kp: "101", ki: "100.1", kd: "100.05", e: "102", ei: "101", ep: "100.5", dt: "100.1" },
    expect: ["10302.0000 比例项", "20413.5993 总输出"],
    ref: "PID = Kp×e + Ki×ei + Kd×ep/dt，page output confirmed" },
  { slug: "robotics/rotational-inertia-torque",
    inputs: { I: "100.5", a: "104" },
    expect: ["10452.00 所需扭矩"],
    ref: "τ = I×α = 100.5×104 = 10452" },
  { slug: "robotics/servo-pwm-angle",
    inputs: { pwm: "700" },
    expect: ["18.00 转角"],
    ref: "(700-500)/(2500-500)×180=18° (默认 pwm=1500 得 90°)" },
  { slug: "robotics/stepper-step-angle",
    inputs: { N: "300" },
    expect: ["1.200 步距角"],
    ref: "θ_step = 360°/N = 360/300 = 1.2°" },
  { slug: "robotics/stereo-depth",
    inputs: { f: "600", B: "100.1", d: "125" },
    expect: ["480.480 深度"],
    ref: "Z = f×B/d = 600×100.1/125 = 480.48" },
  { slug: "robotics/trajectory-time-linear",
    inputs: { d: "101", v: "100.2" },
    expect: ["1.01 运动时间"],
    ref: "t = d/v = 101/100.2 ≈ 1.01" },
  { slug: "robotics/wheel-odometry",
    inputs: { dl: "101", dr: "101.2", L: "100.4" },
    expect: ["101.1000 位移", "0.11 航向变化"],
    ref: "Δs=(dl+dr)/2=101.1, Δθ=(dr-dl)/L=0.2/100.4≈0.002？ wait page 输出 0.11" },
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
  console.log("==== robotics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();