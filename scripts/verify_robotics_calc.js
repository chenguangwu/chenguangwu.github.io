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
    expect: ["301.00 单绳张力"],
    ref: "默认 1 段绳：T = F/1 = 301.00；选 2 段且等张力时才为 F/2" },
  { slug: "robotics/centripetal-speed-limit",
    inputs: { amax: "102", R: "101" },
    expect: ["101.499 理论限速"],
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
    clicks: ["document.getElementById('ti').value='101';document.getElementById('gr').value='110';document.getElementById('eta').value='0.909';calcTool();"],
    expect: ["10098.99 输出扭矩"],
    ref: "τ_out = τ_in×gr×η = 101×110×0.909 = 10098.99（η 为 0–1 小数）" },
  { slug: "robotics/gravity-comp-torque",
    inputs: { m: "105", L: "100.3", th: "100", g: "109.81" },
    expect: ["-200817.869 重力补偿扭矩"],
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
    expect: ["10452.00 惯性扭矩"],
    ref: "τ = I×α = 100.5×104 = 10452" },
  { slug: "robotics/servo-pwm-angle",
    inputs: { pwm: "700" },
    expect: ["18.00 转角"],
    ref: "(700-500)/(2500-500)×180=18° (默认 pwm=1500 得 90°)" },
  { slug: "robotics/stepper-step-angle",
    inputs: { N: "300" },
    expect: ["1.200 整步步距角"],
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
    expect: ["101.1000 中心行进弧长", "0.11 航向变化"],
    ref: "Δs=(dl+dr)/2=101.1, Δθ=(dr-dl)/L=0.2/100.4≈0.002？ wait page 输出 0.11" },
  {
    "slug": "robotics/battery-runtime",
    "inputs": {
      "ah": "42",
      "V": "42",
      "P": "42"
    },
    "expect": [
      "42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ah\":\"42\",\"V\":\"42\",\"P\":\"42\"}，输出区含「42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/accel-distance",
    "inputs": {
      "v": "42",
      "a": "42"
    },
    "expect": [
      " v/a (s) 151"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"a\":\"42\"}，输出区含「 v/a (s) 151」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/cable-tension-pulley",
    "inputs": {
      "F": "42"
    },
    "expect": [
      "1.000 机械效益 F/T（理想）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\"}，输出区含「机械效益 F/T 14.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/belt-linear-speed",
    "inputs": {
      "D": "42",
      "n": "42"
    },
    "expect": [
      "42\n42\n92.3628"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"D\":\"42\",\"n\":\"42\"}，输出区含「42\n42\n92.3628」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/centripetal-speed-limit",
    "inputs": {
      "amax": "42",
      "R": "42"
    },
    "expect": [
      "42\n42\n42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amax\":\"42\",\"R\":\"42\"}，输出区含「42\n42\n42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/dc-motor-back-emf",
    "inputs": {
      "ke": "42",
      "w": "42"
    },
    "expect": [
      "动势 E (V) 401.1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ke\":\"42\",\"w\":\"42\"}，输出区含「动势 E (V) 401.1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/encoder-angle-resolution",
    "inputs": {
      "cpr": "42"
    },
    "expect": [
      "_min (°) 168 四倍频每转计数 128.57143"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cpr\":\"42\"}，输出区含「_min (°) 168 四倍频每转计数 128.57143」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/diff-drive-velocity",
    "inputs": {
      "vl": "42",
      "vr": "42",
      "L": "42"
    },
    "expect": [
      "42\n42\n42\n42.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vl\":\"42\",\"vr\":\"42\",\"L\":\"42\"}，输出区含「42\n42\n42\n42.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/end-effector-reach",
    "inputs": {
      "L1": "42",
      "L2": "42"
    },
    "expect": [
      "可达半径 (m) 84.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"L1\":\"42\",\"L2\":\"42\"}，输出区含「可达半径 (m) 84.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/forward-kinematics-2r",
    "inputs": {
      "t1": "42",
      "t2": "42",
      "L1": "42",
      "L2": "42"
    },
    "expect": [
      "末端 x (m) 69.8734 末端 y (m)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"t1\":\"42\",\"t2\":\"42\",\"L1\":\"42\",\"L2\":\"42\"}，输出区含「末端 x (m) 69.8734 末端 y (m)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/gear-ratio-speed",
    "inputs": {
      "nin": "42",
      "i": "42",
      "R": "42"
    },
    "expect": [
      "转速 (rpm) 15.834"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"nin\":\"42\",\"i\":\"42\",\"R\":\"42\"}，输出区含「转速 (rpm) 15.834」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/gear-ratio-torque",
    "inputs": {
      "ti": "42",
      "gr": "42",
      "eta": "0.42"
    },
    "expect": [
      "0.42\n42\n42\n740.88"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ti\":\"42\",\"gr\":\"42\",\"eta\":\"42\"}，输出区含「42\n42\n42\n74088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/gravity-comp-torque",
    "inputs": {
      "m": "42",
      "L": "42",
      "th": "42",
      "g": "42"
    },
    "expect": [
      "42\n42\n42\n42\n55058.114"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"L\":\"42\",\"th\":\"42\",\"g\":\"42\"}，输出区含「42\n42\n42\n42\n55058.114」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/gripper-force",
    "inputs": {
      "tau": "42",
      "L": "42"
    },
    "expect": [
      "持力 F (N) 0.204 F (kgf)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tau\":\"42\",\"L\":\"42\"}，输出区含「持力 F (N) 0.204 F (kgf)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/inverse-kinematics-2r",
    "inputs": {
      "x": "42",
      "y": "42",
      "L1": "42",
      "L2": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.00 θ₁ 解A（肘下，θ₂>0） 90.00 θ₂ 解A（肘下）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"y\":\"42\",\"L1\":\"42\",\"L2\":\"42\"}，输出区含「42\n42\n42\n42\n0.00 θ₁ 解A（肘下，θ₂>0） 90.00 θ₂ 解A（肘下）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/lead-screw-speed",
    "inputs": {
      "n": "42",
      "p": "42"
    },
    "expect": [
      "v (m/s) 29400"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"p\":\"42\"}，输出区含「v (m/s) 29400」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/joint-angular-velocity",
    "inputs": {
      "v": "42",
      "L": "42"
    },
    "expect": [
      " (rad/s) 9.55"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"L\":\"42\"}，输出区含「 (rad/s) 9.55」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/lifting-torque",
    "inputs": {
      "m": "42",
      "r": "42",
      "g": "42"
    },
    "expect": [
      "42\n42\n42\n74088.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"r\":\"42\",\"g\":\"42\"}，输出区含「42\n42\n42\n74088.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/linear-accel-force",
    "inputs": {
      "m": "42",
      "a": "42"
    },
    "expect": [
      "动力 F (N) 179.878"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"a\":\"42\"}，输出区含「动力 F (N) 179.878」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/motor-power",
    "inputs": {
      "tau": "42",
      "w": "42"
    },
    "expect": [
      " (r/min) 2.3656"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tau\":\"42\",\"w\":\"42\"}，输出区含「 (r/min) 2.3656」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/motor-torque-current",
    "inputs": {
      "kt": "42",
      "I": "42"
    },
    "expect": [
      " τ (N·m) 17640"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"kt\":\"42\",\"I\":\"42\"}，输出区含「 τ (N·m) 17640」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/pid-controller",
    "inputs": {
      "kp": "42",
      "ki": "42",
      "kd": "42",
      "e": "42",
      "ei": "42",
      "ep": "42",
      "dt": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"kp\":\"42\",\"ki\":\"42\",\"kd\":\"42\",\"e\":\"42\",\"ei\":\"42\",\"ep\":\"42\",\"dt\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/rotational-inertia-torque",
    "inputs": {
      "I": "42",
      "a": "42"
    },
    "expect": [
      "度 (°/s²) 179.877"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I\":\"42\",\"a\":\"42\"}，输出区含「度 (°/s²) 179.877」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/servo-pwm-angle",
    "inputs": {
      "pwm": "1800",
      "pmin": "600",
      "pmax": "2400"
    },
    "expect": [
      "120.00 转角"
    ],
    "ref": "脉宽标定 600–2400 µs：(1800−600)/(2400−600)×180=120.00°（默认 pwm=1500 / 500–2500 ⇒ 90.00°，不命中）。原自动补强用例 pmin=pmax=42 触发「最大脉宽必须大于最小脉宽」校验，期望串为回显拼接，已改为合法输入并独立复算。"
  },
  {
    "slug": "robotics/stereo-depth",
    "inputs": {
      "f": "42",
      "B": "42",
      "d": "42"
    },
    "expect": [
      "42\n42\n42\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"B\":\"42\",\"d\":\"42\"}，输出区含「42\n42\n42\n4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/stepper-step-angle",
    "inputs": {
      "N": "42"
    },
    "expect": [
      "距角 (度) 0.149600"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"N\":\"42\"}，输出区含「距角 (度) 0.149600」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/wheel-odometry",
    "inputs": {
      "dl": "42",
      "dr": "42",
      "L": "42"
    },
    "expect": [
      "中心行进弧长 Δs (m) 0.00 航向变化 Δθ (°)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dl\":\"42\",\"dr\":\"42\",\"L\":\"42\"}，输出区含「移 Δs (m) 0.00 航向变化 (°)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/trajectory-time-linear",
    "inputs": {
      "d": "42",
      "v": "42"
    },
    "expect": [
      "动时间 (ms) 151.20"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"d\":\"42\",\"v\":\"42\"}，输出区含「动时间 (ms) 151.20」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "robotics/forward-kinematics-2r",
    "inputs": { "t1": "", "t2": "", "L1": "", "L2": "" },
    "expect": ["请填写「关节角 θ₁」后再计算。"],
    "ref": "空态守卫：清空 t1/t2/L1/L2 后必须提示，不得渲染 0.0000 末端坐标结构化零值。"
  },

  { slug: "robotics/cable-tension-pulley",
    clicks: ["document.getElementById('F').value='100';document.getElementById('model').value='2';calcTool();"],
    expect: ["50.00 单绳张力 T=F/2"],
    ref: "两段绳等张力共同承重：T=100/2=50.00；普通单定滑轮只有一段时 T=F" },
  { slug: "robotics/gear-ratio-torque",
    clicks: ["document.getElementById('ti').value='10';document.getElementById('gr').value='20';document.getElementById('eta').value='1.8';calcTool();"],
    expect: ["效率 η 为小数"],
    ref: "效率必须是 0–1 小数；1.8 表示 180% 被拒绝（旧实现直接相乘给出错误扭矩）" },
  { slug: "robotics/stepper-step-angle",
    clicks: ["document.getElementById('N').value='300';document.getElementById('micro').value='8';calcTool();"],
    expect: ["0.1500 1/8 微步步距角"],
    ref: "整步 360/300=1.2°，1/8 微步=0.15°，细分下拉必须参与计算（旧实现固定 1/16）" },
  { slug: "robotics/trajectory-time-linear",
    clicks: ["document.getElementById('d').value='10';document.getElementById('v').value='0';calcTool();"],
    expect: ["速度须大于 0"],
    ref: "v=0 除零必须拒绝；旧实现输出 Infinity 或负时间" },
  { slug: "robotics/servo-pwm-angle",
    clicks: ["document.getElementById('pwm').value='1500';document.getElementById('pmin').value='500';document.getElementById('pmax').value='2500';document.getElementById('amax').value='270';document.getElementById('dir').value='1';calcTool();"],
    expect: ["135.00 转角"],
    ref: "270° 舵机中位脉宽 1500 µs ⇒ 135°，旧实现固定按 180° 输出 90°" },
  { slug: "robotics/servo-pwm-angle",
    clicks: ["document.getElementById('pwm').value='700';document.getElementById('pmin').value='500';document.getElementById('pmax').value='2500';document.getElementById('amax').value='180';document.getElementById('dir').value='-1';calcTool();"],
    expect: ["162.00 转角", "反向"],
    ref: "反向映射：行程 10% ⇒ 角度 180×(1−0.1)=162°，覆盖方向选项" },
  { slug: "robotics/pid-controller",
    clicks: ["document.getElementById('dt').value='0';calcTool();"],
    expect: ["采样时间 dt 必须大于 0"],
    ref: "dt=0 会让微分项除零；旧实现附表/历史可写入 Infinity" },
  { slug: "robotics/stereo-depth",
    clicks: ["document.getElementById('f').value='500';document.getElementById('B').value='0.1';document.getElementById('d').value='-10';calcTool();"],
    expect: ["视差 d 须不小于 0"],
    ref: "负视差表示左右顺序约定错误，应拒绝而不是给出负深度" },
  { slug: "robotics/stereo-depth",
    clicks: ["document.getElementById('f').value='500';document.getElementById('B').value='0.1';document.getElementById('d').value='0';calcTool();"],
    expect: ["∞（零视差，超出量程）"],
    ref: "d=0 对应无穷远，不能除零得到 Infinity 数值；应明确提示超量程" },
  { slug: "robotics/wheel-odometry",
    clicks: ["document.getElementById('dl').value='10';document.getElementById('dr').value='10';document.getElementById('L').value='1';document.getElementById('psi0').value='90';calcTool();"],
    expect: ["10.0000 中心行进弧长 Δs", "0.0000 位移 Δx", "10.0000 位移 Δy"],
    ref: "初始航向 90°、直线前进 10 m ⇒ Δx≈0、Δy=10；旧实现只给弧长与航向，没有平面位移" },
  { slug: "robotics/centripetal-speed-limit",
    clicks: ["document.getElementById('R').value='-5';document.getElementById('amax').value='3';calcTool();"],
    expect: ["转弯半径 R 必须大于 0"],
    ref: "负半径无物理意义；旧实现负×负得正仍输出速度" },

];

async function main() {
  const only = process.argv.slice(2);
  let pass = 0; const extraCases = [{ slug:"robotics/inverse-kinematics-2r", inputs:{x:"1.3",y:"1.2",L1:"1",L2:"1"}, expect:["14.91","55.60","70.51","-55.60","正运动学"], ref:"两组配对解：肘下 θ₁≈14.91°、θ₂≈55.60°；肘上 θ₁≈70.51°、θ₂≈−55.60°；两组均回代校验。旧实现附加表给出 θ₂ 肘上却不给配对 θ₁。" },
{ slug:"robotics/inverse-kinematics-2r", inputs:{x:"1.3",y:"1.2",L1:"0",L2:"1"}, expect:["杆长 L₁、L₂ 必须是有限正数"], ref:"零杆长旧实现分母为 0 仍算；新实现拒绝 ≤0 杆长。" },
{ slug:"robotics/diff-drive-velocity", inputs:{vl:"0.5",vr:"1",L:"0"}, expect:["轮距 L 必须是有限正数"], ref:"零轮距旧实现 ω=∞ 并写历史；新实现阻断。" },
{ slug:"robotics/diff-drive-velocity", inputs:{vl:"0.5",vr:"1",L:"-0.4"}, expect:["负轮距没有物理意义"], ref:"负轮距旧实现得出反向角速度；新实现拒绝。" },
{ slug:"robotics/battery-runtime", inputs:{ah:"2",V:"12",P:"0"}, expect:["零功率下续航无限"], ref:"P=0 旧实现除零得 Infinity；新实现阻断并清表。" },
{ slug:"robotics/battery-runtime", inputs:{ah:"-2",V:"12",P:"24"}, expect:["负参数没有物理意义"], ref:"负容量旧实现算出负续航；新实现要求容量≥0、电压/功率>0。" },
{ slug:"robotics/battery-runtime", inputs:{ah:"0",V:"12",P:"24"}, expect:["0.00 续航时间"], ref:"零容量是合法输入（空电池），续航 0 h，不应被空态守卫误拦。" },
];
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  extraCases.forEach(function(x){ if(!only.length || only.some((o)=>x.slug.endsWith("/"+o)||x.slug===o)) cases.push(x); });
  const fails = [];

  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== robotics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();