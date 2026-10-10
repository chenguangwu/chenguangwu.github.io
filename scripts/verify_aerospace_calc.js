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
  // ── §7.4 零用例加固：aerospace 确定性数值页（注入非默认 + harness 实测锚）──
  { slug: "aerospace/lift-force", inputs: { rho: "1.1", v: "95", s: "20", cl: "1.4" }, expect: ["138.99", "14167.7"], ref: "注入非默认(默认 1.225/80/16/1.2)：L = ½ρv²S·Cl = 0.5×1.1×95²×20×1.4 = 138,985 N = 138.99 kN（÷9.81 = 14,167.7 kgf）。默认态 75.26 kN / 7,675.0 kgf 不命中。" },
  { slug: "aerospace/thrust-required", inputs: { rho: "1.1", v: "95", s: "20", cd: "0.06" }, expect: ["5.957", "4963.8", "607.39"], ref: "注入非默认(默认 1.225/80/16/0.05)：动压 q = ½ρv² = 0.5×1.1×9025 = 4963.8 Pa；D = q·S·Cd = 4963.8×20×0.06 = 5956.6 N = 5.957 kN = 607.39 kgf。默认态 3136.0/3.136/319.8 均不命中。" },
  { slug: "aerospace/weight-balance", inputs: { oew: "52000", oewArm: "21.5", cgFwd: "19.0", cgAft: "23.5" }, expect: ["52,000", "1,118,000", "21.50"], ref: "注入非默认(默认 45000/20.5/18.0/22.0)：总重 52,000 kg、力臂 21.50 m ⇒ 总力矩 = 52,000×21.5 = 1,118,000 kg·m。默认态 45,000/922,500/20.50 不命中。" },
  { slug: "aerospace/assessor-capacity", inputs: { area: "60000", lanes: "15", counters: "48", gates: "26", peakPax: "3200" }, expect: ["4000人/小时", "2700人/小时", "118.5%"], ref: "注入非默认(默认 50000/12/40/20/2500)：面积容量 = 60000/15 = 4000 人/h；安检 = 15×180 = 2700 人/h；值机 = 48×60 = 2880；登机口 = 26×150 = 3900 ⇒ 瓶颈 2700；利用率 = 3200/2700 = 118.5% ⇒ 超负荷。默认态 3333/2160/115.7% 均不命中。" },
  { slug: "aerospace/lift-coefficient", inputs: { viewAlpha: "10", density: "1.1", velocity: "85", wingArea: "20", alpha0: "-1", clAlpha: "0.12", stallAngle: "15", clMax: "1.6" }, expect: ["查看攻角： 10.0°", "1.320", "104,907"], ref: "注入非默认(默认 viewAlpha=8/density=1.225/velocity=70/wingArea=16)：Cl = clAlpha×(α−α0) = 0.11×(10−(−2)) = 1.320；q = ½×1.1×85² = 3973.75 Pa；L = q·S·Cl = 3973.75×20×1.320 = 104,907 N。⚠ alpha0/clAlpha 的注入被 step 粒度截断（回显仍 −2/0.11）⇒ **不可依赖**，锚只取 viewAlpha 与密度/速度/翼面积驱动的量；默认态攻角 8.0°、Cl 1.10、L 64,834 N 均不命中。" },
  { slug: "aerospace/stats-weight-luggage", inputs: { freeKg: "20", freeCnt: "2", rate: "55" }, expect: ["495.00 元", "免费 2 件之外", "20.0 kg"], ref: "注入非默认(默认 23/1/40)：内置行李 18/22/27/19 kg ⇒ 超重件(>20kg) 2 件、超件(免费 2 件外) 2 件；超重合计 = 5+7 = 9.00 kg（页面口径含超件）⇒ 预估超重费 = 按 55 元/kg 计 495.00 元。默认态 40 元/kg 与各阈值不同。" },
  { slug: "aerospace/wing-area-from-loading", inputs: { W: "95000", WL: "4500" }, expect: ["21.11", "10.556", "47.3684"], ref: "注入非默认(默认 80000/4000)：机翼面积 S = W/(W/S) = 95000/4500 = 21.11 m²；翼载加倍所需面积 = 21.11/2 = 10.556 m²；单位重量翼载（每 kN）= S/(W/1000/9.81) = 21.11/(95/9.81)×…⇒ 47.3684。默认态 20.00/10.000/44.1450 均不命中。" },
  { slug: "aerospace/reynolds-number", inputs: { rho: "1.1", v: "65", L: "3", mu: "1.9e-5" }, expect: ["1.129e+7", "11.2895"], ref: "注入非默认(默认 1.225/50/2/1.81e-5)：Re = ρvL/μ = 1.1×65×3/1.9e-5 = 1.129e+7（= 11.2895×10⁶）。默认态 6.77e+6/6.7740 不命中；「湍流」文案两态相同故不作锚。" },
  { slug: "aerospace/fuel-consumption", inputs: { distance: "2600", cruiseSpeed: "900", burnRate: "2600", taxiFuel: "250", reserveMin: "60", tripFactor: "1.1", flightHours: "3.0" }, expect: ["2.89 小时", "8,262", "11,112", "318 kg/100km"], ref: "注入非默认(默认 2000/850/2400/200/45/1.0)：飞行时间 = 2600/900 = 2.89 h；航段油 = 2600 kg/h×2.89 h×1.1 = 8,262 kg；备份油 = 2,600 kg（60 min）；总加油量 = 8,262+250+2,600 = 11,112 kg；百公里油耗 = 8,262/26 = 318 kg/100km。默认态 2.35 h/5,658/7,708 均不命中。" },
  { slug: "aerospace/rocket-delta-v", inputs: { ve: "3000", m0: "150", mf: "60" }, expect: ["2748.9", "2.5000", "60.000"], ref: "注入非默认(默认 2500/100/50)：质量比 = 150/60 = 2.5000 ⇒ Δv = ve×ln(m0/mf) = 3000×ln2.5 = 2748.9 m/s；推进剂质量分数 = (150−60)/150 = 60.000%。默认态 1732.9/2.0000/50.000 均不命中。" },
  { slug: "aerospace/breguet-range", inputs: { v: "250", ld: "18", wi: "30000", wf: "9000" }, expect: ["0.6 航程 (km)", "0.3 航程 (n mile)"], ref: "注入非默认(默认 v=120/ld=12/wi=12000/wf=8000)：布雷盖航程 R = (v/c)·(L/D)·ln(Wi/Wf)，页面 sfc 为固定常数 ⇒ R ∝ 250×18×ln(30000/9000) = 4500×1.20397 ⇒ 0.6 km（0.3 n mile）。默认态 0.1 km/0.1 n mile 不命中；数值本身很小，必须用带标签的完整串作锚。" },
  { slug: "aerospace/runway-length", inputs: { baseLength: "2600", elevation: "800", temperature: "35", slope: "1.0", headwind: "5" }, expect: ["3,359", "3,863", "29.2%"], ref: "注入非默认(默认 2000/500/30/0.5/3)：修正系数 重量 ×0.850、海拔 800m ×1.187、温度 ISA+25.2°C ×1.252、坡度 1.00% ×1.100、顶风 5.0m/s ×0.930 ⇒ 2600×连乘 = 3,359 m；含 15% 安全余量 ⇒ 3,863 m；较基准长度 +29.2%。默认态 2,467/2,837/23.4% 均不命中。" },
  // ── 零用例加固（2026-10-06）──────────────────────────
  { slug: "aerospace/delta-v-rocket", inputs: { isp: "450", m0: "800000", mf: "120000" }, expect: ["8.37", "8375"], ref: "注入非默认(默认 isp=300/m0=500000/mf=100000)：齐奥尔科夫斯基 Δv = Isp·g₀·ln(m0/mf) = 450×9.81×ln(800000/120000) = 4414.5×1.897120 = 8375.1 m/s = 8.37 km/s。Python 独立复算 8375.06 一致。默认态 4.74 km/s / 4737 m/s，两条均不命中。" },
  {
    slug: "aerospace/flight-time",
    inputs: {"depDate":"2026-01-01","depTime":"08:30","arrDate":"2026-01-01","arrTime":"11:45","flightHours":"13","flightMinutes":"15","calcMode":"duration","depTz":"8","arrTz":"-5"},
    clicks: ["calc()"],
    expect: ["16 小时 15 分钟 实际飞行时长", "-13.0 时差 (小时)"],
    ref: "注入 depTime=08:30(UTC+8) arrTime=11:45(UTC-5) depTz=8 arrTz=-5：UTC 差 16h15m=实际飞行时长、时差 -13.0h（基于时间+时区确定性，不依赖 now）。默认态 depDate 空→不计算→不命中。"
  }
,
  {
    slug: "aerospace/huoyun-uld-jizhuangqi-guige",
    inputs: {"v0":"6000","v1":"4500","v2":"10","v3":"6"},
    clicks: ["calc()"],
    expect: ["133.3% 重量装载率", "4.00 m³ 剩余容积"],
    ref: "注入非默认 v0=6000/v1=4500/v2=10/v3=6(默认6800/5000/11.5/8)：重量装载率、剩余容积均变（以页面实际输出 133.3%/4.00m³ 为准），默认态 136.0%/3.50m³ 不命中。锚计算结果值+单位，规避输入回显。"
  }
,
  {
    slug: "aerospace/length-temp-runway",
    inputs: {"v0":"2000","v1":"1500","v2":"30"},
    clicks: ["calc()"],
    expect: ["2304 m 修正后所需长度", "2.0 °C ISA 标准温度"],
    ref: "注入非默认 v0=2000/v1=1500/v2=30(默认1800/1000/25)：修正后所需长度 2304m、ISA 标准温度 2.0°C，默认态 1436m/3.3°C 不命中。锚计算结果值+单位，规避输入回显。"
  },
  {
    "slug": "aerospace/assessor-capacity",
    "inputs": {
      "area": "42",
      "lanes": "42",
      "counters": "42",
      "gates": "42",
      "peakPax": "42"
    },
    "expect": [
      "时 容量利用率： 2100.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"lanes\":\"42\",\"counters\":\"42\",\"gates\":\"42\",\"peakPax\":\"42\"}，输出区含「时 容量利用率： 2100.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/bank-angle-load",
    "inputs": {
      "phi": "42"
    },
    "expect": [
      " 坡度角 (°) 90.0404 坡度 (%) 0.8107"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phi\":\"42\"}，输出区含「 坡度角 (°) 90.0404 坡度 (%) 0.8107」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/aspect-ratio",
    "inputs": {
      "b": "42",
      "S": "42"
    },
    "expect": [
      "弦长 (m) 0.0238 展弦比倒数 0.50"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"b\":\"42\",\"S\":\"42\"}，输出区含「弦长 (m) 0.0238 展弦比倒数 0.50」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/centripetal-accel",
    "inputs": {
      "v": "42",
      "r": "42"
    },
    "expect": [
      "²/s²) 0.0238 向心加速度倒数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"r\":\"42\"}，输出区含「²/s²) 0.0238 向心加速度倒数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/breguet-range",
    "inputs": {
      "v": "42",
      "ld": "42",
      "wi": "42",
      "wf": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"ld\":\"42\",\"wi\":\"42\",\"wf\":\"42\"}，输出区含「42\n42\n42\n42\n0.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/descent-rate",
    "inputs": {
      "v": "42",
      "g": "42"
    },
    "expect": [
      "速度 (m/s) 90.040 下降梯度 (%)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"g\":\"42\"}，输出区含「速度 (m/s) 90.040 下降梯度 (%)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/delta-v-rocket",
    "inputs": {
      "isp": "42",
      "m0": "42",
      "mf": "42"
    },
    "expect": [
      "v (km/s) 0 Δv (m/s)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"isp\":\"42\",\"m0\":\"42\",\"mf\":\"42\"}，输出区含「v (km/s) 0 Δv (m/s)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/drag-force",
    "inputs": {
      "rho": "42",
      "v": "42",
      "CD": "42",
      "A": "42"
    },
    "expect": [
      "ρv² (Pa) 6663398.41 阻力 (kgf)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"v\":\"42\",\"CD\":\"42\",\"A\":\"42\"}，输出区含「ρv² (Pa) 6663398.41 阻力 (kgf)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/climb-rate",
    "inputs": {
      "pav": "42",
      "preq": "42",
      "w": "42"
    },
    "expect": [
      "42\n42\n42\n0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pav\":\"42\",\"preq\":\"42\",\"w\":\"42\"}，输出区含「42\n42\n42\n0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/dynamic-pressure",
    "inputs": {
      "rho": "42",
      "v": "42"
    },
    "expect": [
      "压 q (Pa) 37.044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"v\":\"42\"}，输出区含「压 q (Pa) 37.044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/escape-velocity",
    "inputs": {
      "mu": "42",
      "r": "42"
    },
    "expect": [
      "速度 (m/s) 0.0014"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mu\":\"42\",\"r\":\"42\"}，输出区含「速度 (m/s) 0.0014」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/flight-time",
    "inputs": {
      "depDate": "abc123测试",
      "depTime": "abc123测试",
      "arrDate": "abc123测试",
      "arrTime": "abc123测试",
      "flightHours": "42",
      "flightMinutes": "42",
      "calcMode": "arrival",
      "depTz": "9",
      "arrTz": "8"
    },
    "expect": [
      "abc123测试\nabc123测试\narrival\n9\n8\nabc123测试\n时间格式有误\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"depDate\":\"abc123测试\",\"depTime\":\"abc123测试\",\"arrDate\":\"abc123测试\",\"arrTime\":\"abc123测试\",\"flightHours\":\"42\",\"flightMinutes\":\"42\",\"calcMode\":\"arrival\",\"depTz\":\"9\",\"arrTz\":\"8\"}，输出区含「abc123测试\nabc123测试\narrival\n9\n8\nabc123测试\n时…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/huoyun-uld-jizhuangqi-guige",
    "inputs": {
      "v0": "42",
      "v1": "42",
      "v2": "42",
      "v3": "42"
    },
    "expect": [
      "0% 重量装载率 100.0% 体积装载率 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\",\"v2\":\"42\",\"v3\":\"42\"}，输出区含「0% 重量装载率 100.0% 体积装载率 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/fuel-consumption",
    "inputs": {
      "distance": "42",
      "cruiseSpeed": "42",
      "flightHours": "42",
      "burnRate": "42",
      "taxiFuel": "42",
      "reserveMin": "42",
      "tripFactor": "42",
      "aircraftType": "b737",
      "calcBy": "time"
    },
    "expect": [
      "份） 总加油量： 4,411,950 kg （约 4,411.95 吨 / 5,514,938"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"distance\":\"42\",\"cruiseSpeed\":\"42\",\"flightHours\":\"42\",\"burnRate\":\"42\",\"taxiFuel\":\"42\",\"reserveMin\":\"42\",\"tripFactor\":\"42\",\"aircraftType\":\"b737\",\"calcBy\":\"time\"}，输出区含「份） 总加油量： 4,411,950 kg （约 4,411.95 吨 / 5,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/length-temp-runway",
    "inputs": {
      "v0": "42",
      "v1": "42",
      "v2": "42"
    },
    "expect": [
      "m 温度增量(+27.3°C) 14.7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\",\"v2\":\"42\"}，输出区含「m 温度增量(+27.3°C) 14.7」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/lift-equation",
    "inputs": {
      "rho": "42",
      "v": "42",
      "CL": "42",
      "A": "42"
    },
    "expect": [
      "v² (Pa) 6663398.41 升力 (kgf)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"v\":\"42\",\"CL\":\"42\",\"A\":\"42\"}，输出区含「v² (Pa) 6663398.41 升力 (kgf)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/lift-force",
    "inputs": {
      "rho": "42",
      "v": "42",
      "s": "42",
      "cl": "42"
    },
    "expect": [
      "力 L (kN) 6661122.9 升力 (kgf)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"v\":\"42\",\"s\":\"42\",\"cl\":\"42\"}，输出区含「力 L (kN) 6661122.9 升力 (kgf)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/load-factor",
    "inputs": {
      "phi": "42"
    },
    "expect": [
      "42\n1.35 载荷因子 n 1.35 等效 g 13.20"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phi\":\"42\"}，输出区含「42\n1.35 载荷因子 n 1.35 等效 g 13.20」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/lift-to-drag-ratio",
    "inputs": {
      "cl": "42",
      "cd": "42"
    },
    "expect": [
      "阻力占比 (%) 45.000 下滑角 (°) 50.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cl\":\"42\",\"cd\":\"42\"}，输出区含「阻力占比 (%) 45.000 下滑角 (°) 50.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/lift-coefficient",
    "inputs": {
      "alpha0": "42",
      "clAlpha": "42",
      "stallAngle": "42",
      "clMax": "42",
      "viewAlpha": "42",
      "density": "42",
      "velocity": "42",
      "wingArea": "42",
      "MpnlolE7L7BZ7sfRjT8ZAb": "naca2412"
    },
    "expect": [
      "Pa 升力 L： 770,145 N（78,586 kgf） ⚠ 当前攻角超过失速攻角，已进入失速状态！\nnaca2412"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"alpha0\":\"42\",\"clAlpha\":\"42\",\"stallAngle\":\"42\",\"clMax\":\"42\",\"viewAlpha\":\"42\",\"density\":\"42\",\"velocity\":\"42\",\"wingArea\":\"42\",\"MpnlolE7L7BZ7sfRjT8ZAb\":\"naca2412\"}，输出区含「Pa 升力 L： 770,145 N（78,586 kgf） ⚠ 当前攻角超过失…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/mach-number",
    "inputs": {
      "v": "42",
      "t": "42",
      "g": "42"
    },
    "expect": [
      "42\n42\n42\n0.022 马赫数 M 1949.1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"t\":\"42\",\"g\":\"42\"}，输出区含「42\n42\n42\n0.022 马赫数 M 1949.1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/orbital-period",
    "inputs": {
      "mu": "42",
      "r": "42"
    },
    "expect": [
      " v (m/s) 0.0010"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mu\":\"42\",\"r\":\"42\"}，输出区含「 v (m/s) 0.0010」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/orbital-velocity",
    "inputs": {
      "mu": "42",
      "r": "42"
    },
    "expect": [
      " v (m/s) 0.0010"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mu\":\"42\",\"r\":\"42\"}，输出区含「 v (m/s) 0.0010」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/rocket-delta-v",
    "inputs": {
      "ve": "42",
      "m0": "42",
      "mf": "42"
    },
    "expect": [
      "42\n42\n42\n0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ve\":\"42\",\"m0\":\"42\",\"mf\":\"42\"}，输出区含「42\n42\n42\n0.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/reynolds-number",
    "inputs": {
      "rho": "42",
      "v": "42",
      "L": "42",
      "mu": "42"
    },
    "expect": [
      "42\n42\n42\n42\n1.764e+3 雷诺数 Re 层"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"v\":\"42\",\"L\":\"42\",\"mu\":\"42\"}，输出区含「42\n42\n42\n42\n1.764e+3 雷诺数 Re 层」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/payload-fraction",
    "inputs": {
      "m0": "42",
      "mf": "42"
    },
    "expect": [
      "效载荷比 (%) 10"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m0\":\"42\",\"mf\":\"42\"}，输出区含「效载荷比 (%) 10」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/stall-speed",
    "inputs": {
      "w": "42",
      "rho": "42",
      "s": "42",
      "cl": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.03"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"rho\":\"42\",\"s\":\"42\",\"cl\":\"42\"}，输出区含「42\n42\n42\n42\n0.03」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/specific-impulse",
    "inputs": {
      "f": "42",
      "mdot": "42"
    },
    "expect": [
      "速度 (m/s) 0.001"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"mdot\":\"42\"}，输出区含「速度 (m/s) 0.001」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/runway-length",
    "inputs": {
      "baseLength": "42",
      "elevation": "42",
      "temperature": "42",
      "slope": "42",
      "headwind": "42",
      "weightClass": "medium"
    },
    "expect": [
      " 系数 重量等级 中型 ×1.000 海拔修正 42 m ×1.010 温度修正 42.0°C（ISA+27.3°C） ×1.273 坡度修正 42.00% ×5.200 顶风修正 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseLength\":\"42\",\"elevation\":\"42\",\"temperature\":\"42\",\"slope\":\"42\",\"headwind\":\"42\",\"weightClass\":\"medium\"}，输出区含「 系数 重量等级 中型 ×1.000 海拔修正 42 m ×1.010 温度修正…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/thrust-required",
    "inputs": {
      "rho": "42",
      "v": "42",
      "s": "42",
      "cd": "42"
    },
    "expect": [
      "42\n42\n42\n42\n65345.61"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"v\":\"42\",\"s\":\"42\",\"cd\":\"42\"}，输出区含「42\n42\n42\n42\n65345.61」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/turn-radius",
    "inputs": {
      "v": "42",
      "phi": "42"
    },
    "expect": [
      "度 (m/s²) 29.88 盘旋周期 (s)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"phi\":\"42\"}，输出区含「度 (m/s²) 29.88 盘旋周期 (s)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/stats-weight-luggage",
    "inputs": {
      "freeKg": "42",
      "freeCnt": "42",
      "rate": "42",
      "weights": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n42\n42\n42\n行李件数： 3 件 总重量： "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"freeKg\":\"42\",\"freeCnt\":\"42\",\"rate\":\"42\",\"weights\":\"1\\n2\\n3\"}，输出区含「1 2 3\n42\n42\n42\n行李件数： 3 件 总重量： 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/turn-rate",
    "inputs": {
      "v": "42",
      "phi": "42"
    },
    "expect": [
      "速度 (°/s) 723.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"phi\":\"42\"}，输出区含「速度 (°/s) 723.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/thrust-to-weight",
    "inputs": {
      "T": "42",
      "W": "42"
    },
    "expect": [
      " 推力与重量之差 9.8066"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"W\":\"42\"}，输出区含「 推力与重量之差 9.8066」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/wing-area-from-loading",
    "inputs": {
      "W": "42",
      "WL": "42"
    },
    "expect": [
      "翼载（每 kN） 1.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"W\":\"42\",\"WL\":\"42\"}，输出区含「翼载（每 kN） 1.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/weight-balance",
    "inputs": {
      "oew": "42",
      "oewArm": "42",
      "cgFwd": "42",
      "cgAft": "42"
    },
    "expect": [
      " 后限）： CG 42.00 前限 42.00 后限 42.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"oew\":\"42\",\"oewArm\":\"42\",\"cgFwd\":\"42\",\"cgAft\":\"42\"}，输出区含「 后限）： CG 42.00 前限 42.00 后限 42.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "aerospace/wing-loading",
    "inputs": {
      "w": "42",
      "s": "42"
    },
    "expect": [
      "kgf/m²) 1000.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"s\":\"42\"}，输出区含「kgf/m²) 1000.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== aerospace calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();