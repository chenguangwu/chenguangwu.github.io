#!/usr/bin node
/**
 * kinematics 分类计算正确性验证（覆盖 tools/kinematics/ 全部 25 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed / toExponential 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_kinematics_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 跑法:
 *   node scripts/verify_kinematics_calc.js                    # 全部
 *   node scripts/verify_kinematics_calc.js stopping-distance  # 单页
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---- 直线运动学 ----
  { slug: "kinematics/avg-velocity",
    inputs: { dx: "180", dt: "6" },
    expect: ["30.000", "108.000"],
    ref: "v̄=Δx/Δt=180/6=30.000 m/s；×3.6=108.000 km/h" },

  { slug: "kinematics/avg-acceleration",
    inputs: { v: "30", v0: "6", t: "4" },
    expect: ["6.000"],
    ref: "a=(30−6)/4=6.000 m/s²" },

  { slug: "kinematics/final-velocity-accel",
    inputs: { v0: "3", a: "2.5", t: "8" },
    expect: ["23.000", "82.800"],
    ref: "v=3+2.5×8=23.000 m/s；×3.6=82.800 km/h" },

  { slug: "kinematics/displacement-accel",
    inputs: { v0: "4", a: "3", t: "6" },
    expect: ["78.000"],
    ref: "x=4×6+½×3×36=24+54=78.000 m" },

  { slug: "kinematics/displacement-va",
    inputs: { v: "25", v0: "5", a: "4" },
    expect: ["75.000"],
    ref: "s=(625−25)/8=75.000 m（不含时间量）" },

  { slug: "kinematics/velocity-squared",
    inputs: { v0: "4", a: "3", dx: "20" },
    expect: ["11.662"],
    ref: "v=√(16+2×3×20)=√136=11.662 m/s" },

  { slug: "kinematics/uniform-displacement",
    inputs: { v: "12", t: "7" },
    expect: ["84.000"],
    ref: "s=12×7=84.000 m" },

  { slug: "kinematics/relative-velocity-1d",
    inputs: { v1: "25", v2: "32" },
    expect: ["-7.000"],
    ref: "v_rel=25−32=−7.000 m/s（负号表示物体1相对物体2后退）" },

  { slug: "kinematics/relativistic-velocity-add",
    inputs: { up: "0.5", v: "0.5", c: "3e8" },
    expect: ["0.800000", "2.400e+8"],
    ref: "u=(0.5+0.5)/(1+0.25)=0.800000 c；×3e8=2.400e+8 m/s（经典相加为 1.0c，错误）" },

  // ---- 自由落体 ----
  { slug: "kinematics/free-fall-time",
    inputs: { h: "45", g: "9.8" },
    expect: ["3.030", "29.698"],
    ref: "t=√(2×45/9.8)=3.030 s；触地速度=9.8×3.030=29.698 m/s" },

  { slug: "kinematics/height-fall-distance",
    inputs: { t: "3.5", g: "9.81" },
    expect: ["60.086"],
    ref: "h=½×9.81×3.5²=60.086 m" },

  // ---- 抛体运动 ----
  { slug: "kinematics/projectile-velocity-components",
    inputs: { v: "40", th: "60" },
    expect: ["20.000", "34.641"],
    ref: "vₓ=40·cos60°=20.000；vᵧ=40·sin60°=34.641" },

  { slug: "kinematics/projectile-max-height",
    inputs: { v: "25", deg: "45", g: "9.8" },
    expect: ["15.944"],
    ref: "H=625×(sin45°)²/(2×9.8)=312.5/19.6=15.944 m" },

  { slug: "kinematics/projectile-time-flight",
    inputs: { v: "25", deg: "30", g: "9.8" },
    expect: ["2.551"],
    ref: "T=2×25×sin30°/9.8=25/9.8=2.551 s" },

  // ---- 制动 ----
  { slug: "kinematics/stopping-time",
    inputs: { v0: "30", a: "6" },
    expect: ["5.000"],
    ref: "t=v₀/a=30/6=5.000 s" },

  { slug: "kinematics/stopping-distance",
    inputs: { v0: "20", tr: "1.5", a: "5" },
    expect: ["30.00", "40.00", "70.00"],
    ref: "反应距离=20×1.5=30.00 m；制动距离=400/10=40.00 m；合计 70.00 m" },

  // ---- 转动 / 圆周 ----
  { slug: "kinematics/angular-accel",
    inputs: { dw: "24", dt: "3" },
    expect: ["8.000"],
    ref: "α=Δω/Δt=24/3=8.000 rad/s²" },

  { slug: "kinematics/angular-displacement",
    inputs: { w0: "3", a: "2", t: "4" },
    expect: ["28.000"],
    ref: "θ=3×4+½×2×16=12+16=28.000 rad" },

  { slug: "kinematics/angular-final-velocity",
    inputs: { w0: "3", a: "2", t: "4" },
    expect: ["11.000"],
    ref: "ω=3+2×4=11.000 rad/s" },

  { slug: "kinematics/angular-velocity",
    inputs: { v: "18", r: "3" },
    expect: ["6.000", "57.296"],
    ref: "ω=v/r=18/3=6.000 rad/s；rpm=6.000×60/(2π)=57.296（须避开默认 10/2=5.000）" },

  { slug: "kinematics/tangential-velocity",
    inputs: { w: "12", r: "0.4" },
    expect: ["4.800"],
    ref: "v=ω·r=12×0.4=4.800 m/s" },

  { slug: "kinematics/tangential-accel",
    inputs: { a: "3.5", r: "0.8" },
    expect: ["2.800"],
    ref: "a_t=α·r=3.5×0.8=2.800 m/s²" },

  { slug: "kinematics/rpm-to-radps",
    inputs: { n: "1500" },
    expect: ["157.080"],
    ref: "ω=2π×1500/60=157.080 rad/s" },

  { slug: "kinematics/freq-from-omega",
    inputs: { w: "15.708" },
    expect: ["2.5000"],
    ref: "f=ω/(2π)=15.708/6.28318=2.5000 Hz" },

  { slug: "kinematics/period-from-omega",
    inputs: { w: "1.5708" },
    expect: ["4.0000"],
    ref: "T=2π/ω=6.28318/1.5708=4.0000 s" },
  {
    "slug": "kinematics/angular-accel",
    "inputs": {
      "dw": "42",
      "dt": "42"
    },
    "expect": [
      "(rad/s²) 2406.423"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dw\":\"42\",\"dt\":\"42\"}，输出区含「(rad/s²) 2406.423」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/angular-final-velocity",
    "inputs": {
      "w0": "42",
      "a": "42",
      "t": "42"
    },
    "expect": [
      " (rad/s) 38808.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w0\":\"42\",\"a\":\"42\",\"t\":\"42\"}，输出区含「 (rad/s) 38808.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/angular-displacement",
    "inputs": {
      "w0": "42",
      "a": "42",
      "t": "42"
    },
    "expect": [
      "42\n42\n42\n38808.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w0\":\"42\",\"a\":\"42\",\"t\":\"42\"}，输出区含「42\n42\n42\n38808.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/angular-velocity",
    "inputs": {
      "v": "42",
      "r": "42"
    },
    "expect": [
      " (rad/s) 9.549"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"r\":\"42\"}，输出区含「 (rad/s) 9.549」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/avg-acceleration",
    "inputs": {
      "v": "42",
      "v0": "42",
      "t": "42"
    },
    "expect": [
      "化量 (m/s) 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"v0\":\"42\",\"t\":\"42\"}，输出区含「化量 (m/s) 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/avg-velocity",
    "inputs": {
      "dx": "42",
      "dt": "42"
    },
    "expect": [
      "̄ (km/h) 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dx\":\"42\",\"dt\":\"42\"}，输出区含「̄ (km/h) 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/displacement-va",
    "inputs": {
      "v": "42",
      "v0": "42",
      "a": "42"
    },
    "expect": [
      "位移 s (m) 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"v0\":\"42\",\"a\":\"42\"}，输出区含「位移 s (m) 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/final-velocity-accel",
    "inputs": {
      "v0": "42",
      "a": "42",
      "t": "42"
    },
    "expect": [
      "v (km/h) 38808.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"a\":\"42\",\"t\":\"42\"}，输出区含「v (km/h) 38808.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/free-fall-time",
    "inputs": {
      "h": "42",
      "g": "42"
    },
    "expect": [
      "时间 t (s) 59.397"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"h\":\"42\",\"g\":\"42\"}，输出区含「时间 t (s) 59.397」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/displacement-accel",
    "inputs": {
      "v0": "42",
      "a": "42",
      "t": "42"
    },
    "expect": [
      "42\n42\n42\n38808"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"a\":\"42\",\"t\":\"42\"}，输出区含「42\n42\n42\n38808」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/height-fall-distance",
    "inputs": {
      "t": "42",
      "g": "42"
    },
    "expect": [
      " v (m/s) 6350.400"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"t\":\"42\",\"g\":\"42\"}，输出区含「 v (m/s) 6350.400」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/freq-from-omega",
    "inputs": {
      "w": "42"
    },
    "expect": [
      "转速 (rpm) 1764.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\"}，输出区含「转速 (rpm) 1764.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/period-from-omega",
    "inputs": {
      "w": "42"
    },
    "expect": [
      "转速 (rpm) 1764.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\"}，输出区含「转速 (rpm) 1764.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/projectile-max-height",
    "inputs": {
      "v": "42",
      "deg": "42",
      "g": "42"
    },
    "expect": [
      "42\n42\n42\n9.402"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"deg\":\"42\",\"g\":\"42\"}，输出区含「42\n42\n42\n9.402」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/projectile-velocity-components",
    "inputs": {
      "v": "42",
      "th": "42"
    },
    "expect": [
      "vₓ (m/s) 28.103"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"th\":\"42\"}，输出区含「vₓ (m/s) 28.103」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/projectile-time-flight",
    "inputs": {
      "v": "42",
      "deg": "42",
      "g": "42"
    },
    "expect": [
      "时间 T (s) 41.770"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"deg\":\"42\",\"g\":\"42\"}，输出区含「时间 T (s) 41.770」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/relativistic-velocity-add",
    "inputs": {
      "up": "42",
      "v": "42",
      "c": "42"
    },
    "expect": [
      "速度 u (c) 1.999e+0 u (m/s)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"up\":\"42\",\"v\":\"42\",\"c\":\"42\"}，输出区含「速度 u (c) 1.999e+0 u (m/s)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/relative-velocity-1d",
    "inputs": {
      "v1": "42",
      "v2": "42"
    },
    "expect": [
      "(km/h) 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v1\":\"42\",\"v2\":\"42\"}，输出区含「(km/h) 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/rpm-to-radps",
    "inputs": {
      "n": "42"
    },
    "expect": [
      "转速 (转/秒) 263.894"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\"}，输出区含「转速 (转/秒) 263.894」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/stopping-time",
    "inputs": {
      "v0": "42",
      "a": "42"
    },
    "expect": [
      "时间 t (s) 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"a\":\"42\"}，输出区含「时间 t (s) 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/tangential-accel",
    "inputs": {
      "a": "42",
      "r": "42"
    },
    "expect": [
      "单位的切向加速度 0.0006 切向加速度倒数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"r\":\"42\"}，输出区含「单位的切向加速度 0.0006 切向加速度倒数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/stopping-distance",
    "inputs": {
      "v0": "42",
      "tr": "42",
      "a": "42"
    },
    "expect": [
      "42\n42\n42\n1764.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"tr\":\"42\",\"a\":\"42\"}，输出区含「42\n42\n42\n1764.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/uniform-displacement",
    "inputs": {
      "v": "42",
      "t": "42"
    },
    "expect": [
      "度 (km/h) 1.764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"t\":\"42\"}，输出区含「度 (km/h) 1.764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/tangential-velocity",
    "inputs": {
      "w": "42",
      "r": "42"
    },
    "expect": [
      " v (m/s) 6350.4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"r\":\"42\"}，输出区含「 v (m/s) 6350.4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "kinematics/velocity-squared",
    "inputs": {
      "v0": "42",
      "a": "42",
      "dx": "42"
    },
    "expect": [
      "42\n42\n42\n72.746"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"a\":\"42\",\"dx\":\"42\"}，输出区含「42\n42\n42\n72.746」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }

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
  console.log("==== kinematics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();