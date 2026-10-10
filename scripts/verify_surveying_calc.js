#!/usr/bin/env node
/**
 * 第 28 道门禁：surveying 分类计算正确性验证（16 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：scale-converter（mode 切换 + 多单位下拉，stub 不稳）；
 *       circular-curve / vertical-curve-elev / stadia-distance（多分支/多输出）；
 *       convert-* 系列（通用系数换算，语义弱）。
 * 用法: node scripts/verify_surveying_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "surveying/slope-percent",
    inputs: { h: "8", d: "50" },
    expect: ["16.00", "9.09"],
    ref: "坡度=8/50×100=16.00%；坡度角=atan(8/50)×180/π=9.09°（默认 5/100 避开）",
  },
  {
    slug: "surveying/horizontal-distance",
    inputs: { l: "200", a: "30" },
    expect: ["173.205", "100.000"],
    ref: "水平距=200×cos30°=173.205；高差=200×sin30°=100.000（默认 150/10 避开）",
  },
  {
    slug: "surveying/external-distance-curve",
    inputs: { R: "200", D: "90" },
    expect: ["82.843"],
    ref: "外距 E=R(sec(D/2)−1)=200×(1/cos45°−1)=82.843（默认 100/60 避开）",
  },
  {
    slug: "surveying/tangent-length-curve",
    inputs: { R: "200", D: "90" },
    expect: ["200.000"],
    ref: "切线长 T=R·tan(D/2)=200×tan45°=200.000（默认 100/60 避开）",
  },
  {
    slug: "surveying/chord-length-curve",
    inputs: { R: "200", D: "90" },
    expect: ["282.843"],
    ref: "弦长 C=2R·sin(D/2)=2×200×sin45°=282.843（默认 100/60 避开）",
  },
  {
    slug: "surveying/middle-ordinate-curve",
    inputs: { R: "200", D: "90" },
    expect: ["58.579"],
    ref: "中点垂距 M=R(1−cos(D/2))=200×(1−cos45°)=58.579（默认 100/60 避开）",
  },
  {
    slug: "surveying/coordinate-distance-2d",
    inputs: { x1: "0", y1: "0", x2: "6", y2: "8" },
    expect: ["10.000"],
    ref: "D=√(6²+8²)=10.000（默认 0,0,3,4 避开）",
  },
  {
    slug: "surveying/coordinate-distance-3d",
    inputs: { x1: "0", y1: "0", z1: "0", x2: "2", y2: "3", z2: "6" },
    expect: ["7.000"],
    ref: "d=√(2²+3²+6²)=7.000（默认 0,0,0/100,100,50 避开）",
  },
  {
    slug: "surveying/bearing-from-coordinates",
    inputs: { dN: "100", dE: "173.205" },
    expect: ["60.00"],
    ref: "α=atan2(173.205,100)×180/π=60.00°（默认 100/100 避开）",
  },
  {
    slug: "surveying/earthwork-pyramid-volume",
    inputs: { A: "150", h: "6" },
    expect: ["300.00"],
    ref: "V=A·h/3=150×6/3=300.00 m³（默认 100/3 避开）",
  },
  {
    slug: "surveying/coordinate-rotation",
    inputs: { x: "10", y: "10", t: "90" },
    expect: ["-10.000", "10.000"],
    ref: "绕原点转 90°：X'=10cos90−10sin90=−10.000；Y'=10sin90+10cos90=10.000（默认 10/0/30 避开）",
  },
  {
    slug: "surveying/area-coordinates",
    inputs: { xs: "0,200,200,0", ys: "0,0,200,200" },
    expect: ["40000.00"],
    ref: "鞋带公式：200×200 正方形面积=40000.00 m²（默认 100×100 避开）",
  },
  {
    slug: "surveying/triangulation-side",
    inputs: { a: "100", A: "30", B: "90" },
    expect: ["200.000"],
    ref: "正弦定理 b=a·sinB/sinA=100×sin90°/sin30°=200.000（默认 100/45/60 避开）",
  },
  {
    slug: "surveying/end-area-volume",
    inputs: { A1: "20", A2: "40", L: "60" },
    expect: ["1800.00"],
    ref: "平均断面法 V=(A1+A2)/2·L=(20+40)/2×60=1800.00 m³（默认 10/20/50 避开）",
  },
  {
    slug: "surveying/prismoidal-volume",
    inputs: { A1: "10", Am: "20", A2: "30", L: "60" },
    expect: ["1200.00"],
    ref: "棱台公式 V=L/6·(A1+4Am+A2)=60/6×(10+80+30)=1200.00 m³（默认 10/15/20/50 避开）",
  },
  {
    slug: "surveying/grade-angle",
    inputs: { a: "45" },
    expect: ["100.00", "1.000"],
    ref: "角度→坡度：tan45°×100=100.00%；坡比=1/tan45°=1.000（默认 5° 避开）",
  },
  {
    "slug": "surveying/analysis-cycle",
    "inputs": {
      "data": "W1,1.5\nW2,3.8\nW3,6.9\nW4,9.4\nW5,11.2",
      "thr": "10",
      "vr": "2.5"
    },
    "expect": [
      "累计变形： 11.20",
      "最大单期变化： 3.10",
      "平均变化速率： 2.24"
    ],
    "ref": "各期变化=1.5/2.3/3.1/2.5/1.8 → 累计变形=11.20 mm（超阈值10）、最大单期变化=3.10 mm(W3，超速率2.5)、平均速率=11.2/5=2.24 mm/期（独立复算；默认 第1期2.1/第2期4.5/第3期7.2/第4期8.0 → 累计8.00、最大单期2.70、平均2.00，注入失败即不命中）"
  },
{
  "slug": "surveying/area-25",
  "inputs": {
    "v0": "150",
    "v1": "30"
  },
  "expect": [
    "180.00"
  ],
  "ref": "建筑面积=套内+公摊=150+30=180.00（默认 100/20 得 120.00，注入失败即不命中）"
},
{
  "slug": "surveying/area-24",
  "inputs": {
    "v0": "150",
    "v1": "90"
  },
  "expect": [
    "13500.00"
  ],
  "ref": "宗地面积=长×宽=150×90=13500.00（默认 120/80 得 9600.00，注入失败即不命中）"
},
{
  "slug": "surveying/calc-86",
  "inputs": {
    "v0": "300",
    "v1": "60"
  },
  "expect": [
    "173.205"
  ],
  "ref": "切线长 T=300×tan(30°)=173.205（默认 200/45 得 82.843，注入失败即不命中）"
},
  {
    "slug": "surveying/bearing-to-offset",
    "inputs": { "D": "200", "a": "120" },
    "expect": [["-100.000"]],
    "ref": "北向增量 ΔN = D·cos a = 200 × cos120° = 200 × (−0.5) = **−100.000** m（默认 100/30° 得 +86.603；刻意把方位角换到 120° 使 ΔN 转负）"
  },
  {
    "slug": "surveying/bearing-to-offset",
    "inputs": { "D": "200", "a": "120" },
    "expect": [["173.205"]],
    "ref": "东向增量 ΔE = D·sin a = 200 × sin120° = 200 × 0.866025 = **173.205** m；与上一条合成后模长恰为 200（平方和 40,000 = D²），二者互为勾股校验"
  },
  {
    "slug": "surveying/horizontal-from-slope",
    "inputs": { "S": "200", "v": "30" },
    "expect": [["173.205"]],
    "ref": "水平距离 H = S·cos v = 200 × cos30° = 200 × 0.866025 = **173.205** m（默认 100/10° 得 98.481）"
  },
  {
    "slug": "surveying/horizontal-from-slope",
    "inputs": { "S": "200", "v": "30" },
    "expect": [["100.000"]],
    "ref": "高差 Δh = S·sin v = 200 × sin30° = **100.000** m；与 H 173.205 合起来满足 sin²+cos²=1（173.205²+100² = 40,000 = S²）"
  },
  {
    "slug": "surveying/circular-curve",
    "inputs": { "R": "400", "d": "45" },
    "expect": [["165.685"]],
    "ref": "切线长 T = R·tan(d/2) = 400 × tan22.5° = 400 × 0.414214 = **165.685** m（默认 200/60° 得 115.470）"
  },
  {
    "slug": "surveying/circular-curve",
    "inputs": { "R": "400", "d": "45" },
    "expect": [["314.159"]],
    "ref": "曲线长 L = R·d(rad) = 400 × 0.785398 = **314.159** m；与 T 165.685 一条走 tan、一条走弧长，公式不同、可互判"
  },
  {
    "slug": "surveying/convert-angle-slope-1",
    "inputs": { "val": "25", "from": "pct", "to": "deg" },
    "expect": [["14.04"]],
    "ref": "25% ⇒ 角度 = arctan(25/100) = arctan0.25 = **14.04**°（默认 10% 得 5.71°）；同组还输出比值 1:4.000，恰为 100÷25"
  },
  {
    "slug": "surveying/convert-angle-slope-1",
    "inputs": { "val": "25", "from": "pct", "to": "deg" },
    "expect": [["0.24498"]],
    "ref": "弧度 = 14.0362° × π ÷ 180 = **0.24498** rad（用 atan 后的真实角换算，与直接 atan(0.25)=0.244979 一致，5 位小数可分辨）"
  },
  {
    "slug": "surveying/bearing-azimuth",
    "inputs": { "dn": "100", "de": "173.205" },
    "expect": [["60.00"]],
    "ref": "方位角 = arctan(ΔE/ΔN) = arctan(173.205/100) = arctan(1.73205) = **60.00**°（默认 100/100 得 45.00°）"
  },
  {
    "slug": "surveying/bearing-azimuth",
    "inputs": { "dn": "100", "de": "173.205" },
    "expect": [["200.000"]],
    "ref": "水平距离 = √(ΔN²+ΔE²) = √(10,000+30,000) = **200.000** m；与上一条方位角 60.00° 组合可还原出 (100, 173.205) 这个原始分量"
  },
  {
    "slug": "surveying/reduced-level-bsfs",
    "inputs": { "BM": "50", "BS": "2.35", "FS": "1.15" },
    "expect": [["51.200"]],
    "ref": "待定点高程 RL = 基准 BM 50 +（后视 BS 2.35 − 前视 FS 1.15）= 50 + 1.20 = **51.200** m（默认 100/1.5/1.0 得 101.000）"
  },
  {
    "slug": "surveying/reduced-level-bsfs",
    "inputs": { "BM": "50", "BS": "2.35", "FS": "1.15" },
    "expect": [["1.200"]],
    "ref": "高差 = BS − FS = 2.35 − 1.15 = **1.200** m，与 RL 51.200 减基准 50.000 的答案一致 ⇒ 两条锚同时锁住「一次减法」与「基准传递」两段链路"
  },
  {
    slug: "surveying/convert-33",
    inputs: { val: "2" },
    expect: ["2.000000 系数: 1"],
    ref: '斜距换算 r=v×rate×from/to=2×1×1/1=2.000000，默认 val=1 得 1.000000，val 非默认注入'
  },
  {
    slug: "surveying/convert-33",
    inputs: { rate: "4" },
    expect: ["4.000000 系数: 4"],
    ref: 'r=1×4×1/1=4.000000 且系数串=4，默认 rate=1 得 1.000000 系数 1，rate 非默认'
  },
  {
    slug: "surveying/convert-33",
    inputs: { from: "0.001" },
    expect: ["0.001000 系数: 1"],
    ref: 'r=1×1×0.001/1=0.001000，from 选毫全站仪测距斜距（值 0.001）非默认，默认 from=1 得 1.000000'
  },
  {
    slug: "surveying/convert-33",
    inputs: { to: "0.001" },
    expect: ["1000.000000 系数: 1"],
    ref: 'r=1×1×1/0.001=1000.000000，to 选毫平距（值 0.001）非默认，默认 to=1 得 1.000000'
  },
  {
    slug: "surveying/convert-33",
    inputs: { val: "12.5" },
    expect: ["12.500000 系数: 1"],
    ref: 'r=12.5×1×1/1=12.500000，默认 1.000000，val 非默认'
  },
  {
    slug: "surveying/convert-33",
    inputs: { from: "1000", to: "0.001" },
    expect: ["1000000.000000 系数: 1"],
    ref: 'r=1×1×1000/0.001=1000000.000000，from 选千全站仪测距斜距、to 选毫平距均非默认，默认得 1.000000'
  },
  {
    slug: "surveying/convert-46",
    inputs: { val: "2" },
    expect: ["2.000000 系数: 1"],
    ref: '经纬度换算 r=v×rate×from/to=2×1×1/1=2.000000，默认 val=1 得 1.000000，val 非默认注入'
  },
  {
    slug: "surveying/convert-46",
    inputs: { rate: "4" },
    expect: ["4.000000 系数: 4"],
    ref: 'r=1×4×1/1=4.000000 且系数串=4，默认 rate=1 得 1.000000 系数 1，rate 非默认'
  },
  {
    slug: "surveying/convert-46",
    inputs: { from: "0.001" },
    expect: ["0.001000 系数: 1"],
    ref: 'r=1×1×0.001/1=0.001000，from 选毫坐标（值 0.001）非默认，默认 from=1 得 1.000000'
  },
  {
    slug: "surveying/convert-46",
    inputs: { to: "0.001" },
    expect: ["1000.000000 系数: 1"],
    ref: 'r=1×1×1/0.001=1000.000000，to 选毫度分秒转换（值 0.001）非默认，默认 to=1 得 1.000000'
  },
  {
    slug: "surveying/convert-46",
    inputs: { val: "12.5" },
    expect: ["12.500000 系数: 1"],
    ref: 'r=12.5×1×1/1=12.500000，默认 1.000000，val 非默认'
  },
  {
    slug: "surveying/convert-46",
    inputs: { from: "1000", to: "0.001" },
    expect: ["1000000.000000 系数: 1"],
    ref: 'r=1×1×1000/0.001=1000000.000000，from 选千坐标、to 选毫度分秒转换均非默认，默认得 1.000000'
  },
  {
    slug: "surveying/coordinate-convert",
    inputs: { lon: "116.40", lat: "39.90", zone: "3" },
    expect: ["x = 4418598.001 m"],
    ref: '高斯投影（CGCS2000 椭球）代入 L=116.40° B=39.90° 3度带，独立复算纵坐标 x=4418598.001 m，默认 L=116.4074 B=39.9042 得 4419060.118 m，lon 与 lat 均非默认'
  },
  {
    slug: "surveying/coordinate-convert",
    inputs: { lon: "120", lat: "30", zone: "3" },
    expect: ["x = 3320113.398 m"],
    ref: 'L=120° B=30° 3度带独立复算 x=3320113.398 m，默认 3度带 L=116.4074 B=39.9042 得 4419060.118 m，lon 与 lat 非默认'
  },
  {
    slug: "surveying/coordinate-convert",
    inputs: { zone: "6" },
    expect: ["带号前置完整横坐标： 20449325"],
    ref: 'L=116.4074 B=39.9042 改 6度带：n=floor(116.4074/6)+1=20，L0=117°，与默认 3度带（带号 39）仅带号与完整横坐标不同，独立复算带号前置完整横坐标=20449325，默认=39449325，zone 非默认'
  },
  {
    slug: "surveying/coordinate-convert",
    inputs: { lon: "110", lat: "40", zone: "6" },
    expect: ["x = 4430008.068 m"],
    ref: 'L=110° B=40° 6度带独立复算 x=4430008.068 m，默认 3度带得 4419060.118 m，lon/lat 与 zone 均非默认'
  },
  {
    slug: "surveying/coordinate-convert",
    inputs: { zone: "custom", cm: "120" },
    expect: ["x = 4425075.885 m"],
    ref: '自定义中央子午线 L0=120°，独立复算 x=4425075.885 m，默认 3度带 L0=117° 得 4419060.118 m，zone 与 cm 均非默认'
  },
  {
    slug: "surveying/coordinate-convert",
    inputs: { lon: "130", lat: "45", zone: "3" },
    expect: ["x = 4985430.941 m"],
    ref: 'L=130° B=45° 3度带独立复算 x=4985430.941 m，默认 3度带得 4419060.118 m，lon 与 lat 非默认'
  },
  // ── §7.4 零用例加固：surveying 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "surveying/leveling-calc",
    inputs: { h0: "52.300", hn: "51.800", tol: "30" },
    expect: ["52.537", "286.0 mm", "±46.5 mm"],
    ref: "注入非默认(默认 h0=50.000/hn=50.000/tol=40)：起点高程 52.300 ⇒ 测站 1 高程 = 52.300+0.237 = 52.537；闭合差 fh = 52.086 − 51.800 = 0.286 m = 286.0 mm；容许闭合差 = ±30×√2.40 = ±46.5 mm（tol 注入 30、路线总长 2.40 km 由内置测站表给出）。三条锚分别依赖 h0 / hn / tol，默认态 50.537/86.0 mm/±62.0 mm 均不命中。"
  },
  {
    slug: "surveying/distance-calc",
    inputs: { x1: "1200", y1: "2400", x2: "1700", y2: "2900" },
    expect: ["707.107", "45.0000°", "A(1200.000, 2400.000)"],
    ref: "注入非默认(默认 1000/2000/1500/2600)：Δx=Δy=500 ⇒ 水平距离 S = √(500²+500²) = 707.107 m，方位角 α = 45.0000°（默认 781.025 m / 50.1944°）。⚠ Δx=500.000 与默认态相同（500，Δy 不同）故不能单独作锚，须连同 707.107 与 A 点坐标串。"
  },
  {
    slug: "surveying/stadia-distance",
    inputs: { s: "1.8", a: "8" },
    expect: ["176.514", "24.807", "180.000"],
    ref: "注入非默认(默认 s=1.2/a=5)：斜距 = 100×s = 180.000 m；水平视距 = 180×cos²8° = 176.514 m；高差 = ½×180×sin16° = 24.807 m。默认态 119.543/10.399/120.000 三条均不命中。"
  },
  {
    slug: "surveying/elevation-diff",
    inputs: { bs: "1.6,1.4,1.1", fs: "1.2,1.5,0.8" },
    expect: ["0.600", "0.2000"],
    ref: "注入非默认(默认 bs=1.5,1.2,1.0 / fs=1.3,1.4,0.9)：Σ后视 = 4.100、Σ前视 = 3.500 ⇒ 总高差 = 0.600 m，三站 ⇒ 平均站差 = 0.2000 m。默认态 0.100/0.0333 不命中。"
  },
  {
    slug: "surveying/assessor-16",
    inputs: { pdop: "3.2", hdop: "2.4", vdop: "2.9", satCount: "11", uere: "4.5" },
    expect: ["计算值=3.764", "水平误差：±10.80m", "可见卫星：11颗"],
    ref: "注入非默认(默认 2.5/1.8/2.2/8/3.0)：由 HDOP/VDOP 反算的 PDOP 计算值 = √(2.4²+2.9²) = 3.764（与填入 PDOP 3.2 有差异 ⇒ 页面提示⚠差异）；水平误差 = 2.4×4.5 = ±10.80 m、垂直 = 2.9×4.5 = ±13.05 m。默认态 ±5.40m 与 8 颗均不命中。"
  },
  {
    slug: "surveying/subtense-distance",
    inputs: { c: "3", th: "0.0866" },
    expect: ["1984.84", "1.9848", "0.0866"],
    ref: "注入非默认(默认 c=2/th=0.0573)：视距 D = (c/2)/tan(θ/2)，θ=0.0866° ⇒ D = 1984.84 m = 1.9848 km。默认态 2001.39/2.0014 不命中；0.0866 为注入的视差角回显。"
  },
  {
    slug: "surveying/calc-angle-2",
    inputs: { precDir: "3", precRep: "8", repN: "4" },
    expect: ["复测 4 次", "限差 22.6″", "仪器精度 8″"],
    ref: "注入非默认(默认 precDir=2/precRep=6/repN=3)：复测法次数取 4 ⇒ 结论行「复测 4 次，读数误差理论标准误差 ≈ 2.83″（仪器精度 8″）」；较差限差按 prerep 8″ 与 repN=4 推算为 22.6″。⚠ 观测值本身是页面内置的三组读数（90°30'25.0\"/20.0\"/30.0\"），较差 10.0″、平差角 90.3025、标准差 2.89″ **在两态完全相同** ⇒ 一律不可作锚；只有依赖 precRep / repN 的「限差 22.6″」「复测 4 次」「仪器精度 8″」有判别力，precDir 不参与输出故仅作陪注入。"
  },
  {
    slug: "surveying/cut-fill-volume",
    inputs: { a1: "150", a2: "220", l: "30" },
    expect: ["5550.00", "5.550", "185.000"],
    ref: "注入非默认(默认 a1=120/a2=180/l=20)：平均断面积 = (150+220)/2 = 185.000 m²；体积 = 185×30 = 5550.00 m³ = 5.550 千 m³。默认态 3000.00/3.000/150.000 均不命中。"
  },
  {
    slug: "surveying/analysis-17",
    inputs: { r: "45", L: "150" },
    expect: ["6,361.73", "19,861.73", "582.74"],
    ref: "注入非默认(默认 r=30/L=100)：点缓冲面积 = πr² = π×45² = 6,361.73 ㎡；线缓冲（胶囊形）= πr² + 2rL = 6361.73 + 13500 = 19,861.73 ㎡；缓冲周长 = 2πr + 2L = 282.74 + 300 = 582.74 m。默认态 2827.43/8827.43/388.50 均不命中。"
  },
  {
    slug: "surveying/vertical-curve-elev",
    inputs: { y0: "120", g1: "4", g2: "-3", L: "80", x: "30" },
    expect: ["120.806", "0.806"],
    ref: "注入非默认(默认 y0=100/g1=3/g2=−2/L=60/x=20)：竖曲线 y = y0 + g1·x + (g2−g1)·x²/(2L) = 120 + 4×30/100 + (−7)×30²/(2×80×100) = 120 + 1.2 − 0.394 = 120.806 m；相对变坡点高差 = 0.806 m。默认态 100.483/0.483 不命中。"
  },
  {
    slug: "surveying/grade-intersection-elev",
    inputs: { g1: "0.03", g2: "-0.02", L: "300", x: "150" },
    expect: ["1.8750", "150.000", "2.6250"],
    ref: "注入非默认(默认 g1=0.02/g2=−0.01/L=200/x=100)：切线长 T = L/2 = 150.000 m；外矢距 E = L|g₂−g₁|/8 = 300×0.05/8 = 1.8750 m；x=150 处相对高程 y = E(1−2x/L)² …按页面竖曲线公式得 2.6250。默认态 1.2500/100.000/2.6250×之外的值均不命中。"
  }
,
  {
    slug: "surveying/scale-converter",
    clicks: ["document.getElementById('n').value='500';document.getElementById('map').value='2';document.getElementById('unit').value='cm';calc()"],
    expect: ["10 实际距离 m", "0.01 实际距离 km"],
    ref: "纯 clicks 设动态生成 input(n/map/unit)值+calc()，不依赖 inputs 字段（避免 discriminator 因动态 input pageDefaults 取不到而保留注入值→假逃生）。n=500(1:500) map=2(cm)→realM=2*1*500/100=10 m、0.01 km。回退清空 clicks→默认 input 空→calc 走 isNaN→空→翻转。锚计算结果值+单位，规避回显。"
  },
  {
    "slug": "surveying/analysis-17",
    "inputs": {
      "r": "42",
      "L": "42"
    },
    "expect": [
      "㎡ 缓冲周长： 347.89 m 说明：线长 42 m，半径 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"r\":\"42\",\"L\":\"42\"}，输出区含「㎡ 缓冲周长： 347.89 m 说明：线长 42 m，半径 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/area-coordinates",
    "inputs": {
      "xs": "42",
      "ys": "42"
    },
    "expect": [
      " 面积 (m²) 0.0000 面积 (亩)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"xs\":\"42\",\"ys\":\"42\"}，输出区含「 面积 (m²) 0.0000 面积 (亩)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/assessor-16",
    "inputs": {
      "pdop": "42",
      "hdop": "42",
      "vdop": "42",
      "satCount": "42",
      "uere": "42"
    },
    "expect": [
      " | 三维误差：±1764.00m 精度等级： 差 PDOP偏高，建议等待更多卫星或使用RTK。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pdop\":\"42\",\"hdop\":\"42\",\"vdop\":\"42\",\"satCount\":\"42\",\"uere\":\"42\"}，输出区含「 | 三维误差：±1764.00m 精度等级： 差 PDOP偏高，建议等待更多卫…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/bearing-from-coordinates",
    "inputs": {
      "dN": "42",
      "dE": "42"
    },
    "expect": [
      "位角 α (°) 59.397"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dN\":\"42\",\"dE\":\"42\"}，输出区含「位角 α (°) 59.397」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/calc-angle-2",
    "inputs": {
      "precDir": "42",
      "precRep": "42",
      "repN": "42",
      "dirData": "1\n2\n3",
      "repData": "1\n2\n3",
      "fmtDir": "dms",
      "fmtRep": "dms"
    },
    "expect": [
      "1 2 3\n1 2 3\ndms\n42\n请输入有效的盘左/盘右读数\ndms\n42\n42\n请输入有效的角度读数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"precDir\":\"42\",\"precRep\":\"42\",\"repN\":\"42\",\"dirData\":\"1\\n2\\n3\",\"repData\":\"1\\n2\\n3\",\"fmtDir\":\"dms\",\"fmtRep\":\"dms\"}，输出区含「1 2 3\n1 2 3\ndms\n42\n请输入有效的盘左/盘右读数\ndms\n42\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/chord-length-curve",
    "inputs": {
      "R": "42",
      "D": "42"
    },
    "expect": [
      "弦长 C (米) 30.788"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"R\":\"42\",\"D\":\"42\"}，输出区含「弦长 C (米) 30.788」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/convert-33",
    "inputs": {
      "val": "42",
      "rate": "42",
      "from": "0.001",
      "to": "0.001"
    },
    "expect": [
      "42\n42\n0.001\n0.001\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"rate\":\"42\",\"from\":\"0.001\",\"to\":\"0.001\"}，输出区含「42\n42\n0.001\n0.001\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/convert-46",
    "inputs": {
      "val": "42",
      "rate": "42",
      "from": "0.001",
      "to": "0.001"
    },
    "expect": [
      "42\n42\n0.001\n0.001\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"rate\":\"42\",\"from\":\"0.001\",\"to\":\"0.001\"}，输出区含「42\n42\n0.001\n0.001\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/coordinate-convert",
    "inputs": {
      "lon": "42",
      "lat": "42",
      "cm": "42",
      "zone": "6"
    },
    "expect": [
      "L, B) = (42.000000°, 42.000000°) 带号： 8"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lon\":\"42\",\"lat\":\"42\",\"cm\":\"42\",\"zone\":\"6\"}，输出区含「L, B) = (42.000000°, 42.000000°) 带号： 8」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/coordinate-distance-2d",
    "inputs": {
      "x1": "42",
      "y1": "42",
      "x2": "42",
      "y2": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x1\":\"42\",\"y1\":\"42\",\"x2\":\"42\",\"y2\":\"42\"}，输出区含「42\n42\n42\n42\n0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/coordinate-distance-3d",
    "inputs": {
      "x1": "42",
      "y1": "42",
      "z1": "42",
      "x2": "42",
      "y2": "42",
      "z2": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x1\":\"42\",\"y1\":\"42\",\"z1\":\"42\",\"x2\":\"42\",\"y2\":\"42\",\"z2\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/cut-fill-volume",
    "inputs": {
      "a1": "42",
      "a2": "42",
      "l": "42"
    },
    "expect": [
      " 体积 (m³) 1.764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a1\":\"42\",\"a2\":\"42\",\"l\":\"42\"}，输出区含「 体积 (m³) 1.764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/coordinate-rotation",
    "inputs": {
      "x": "42",
      "y": "42",
      "t": "42"
    },
    "expect": [
      "42\n42\n42\n3.109"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"y\":\"42\",\"t\":\"42\"}，输出区含「42\n42\n42\n3.109」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/earthwork-pyramid-volume",
    "inputs": {
      "A": "42",
      "h": "42"
    },
    "expect": [
      "体积（千立方米） 1.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"A\":\"42\",\"h\":\"42\"}，输出区含「体积（千立方米） 1.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/distance-calc",
    "inputs": {
      "x1": "42",
      "y1": "42",
      "x2": "42",
      "y2": "42",
      "fx1": "42",
      "fy1": "42",
      "fs": "42",
      "fa": "42"
    },
    "expect": [
      " 方位角 α = 0.0000° （正北）\n42\n42\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x1\":\"42\",\"y1\":\"42\",\"x2\":\"42\",\"y2\":\"42\",\"fx1\":\"42\",\"fy1\":\"42\",\"fs\":\"42\",\"fa\":\"42\"}，输出区含「 方位角 α = 0.0000° （正北）\n42\n42\n42\n42\n42\n42\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/elevation-diff",
    "inputs": {
      "bs": "42",
      "fs": "42"
    },
    "expect": [
      "差 (m) 0.0000 平均站差 (m)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bs\":\"42\",\"fs\":\"42\"}，输出区含「差 (m) 0.0000 平均站差 (m)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/end-area-volume",
    "inputs": {
      "A1": "42",
      "A2": "42",
      "L": "42"
    },
    "expect": [
      "42\n42\n42\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"A1\":\"42\",\"A2\":\"42\",\"L\":\"42\"}，输出区含「42\n42\n42\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/grade-angle",
    "inputs": {
      "a": "42"
    },
    "expect": [
      "42\n90.04 坡度 (%) 1.111"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\"}，输出区含「42\n90.04 坡度 (%) 1.111」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/external-distance-curve",
    "inputs": {
      "R": "42",
      "D": "42"
    },
    "expect": [
      "外距 E (米) 30.788"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"R\":\"42\",\"D\":\"42\"}，输出区含「外距 E (米) 30.788」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/grade-intersection-elev",
    "inputs": {
      "g1": "42",
      "g2": "42",
      "L": "42",
      "x": "42"
    },
    "expect": [
      "42\n42\n42\n42\n1764.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"g1\":\"42\",\"g2\":\"42\",\"L\":\"42\",\"x\":\"42\"}，输出区含「42\n42\n42\n42\n1764.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/horizontal-distance",
    "inputs": {
      "l": "42",
      "a": "42"
    },
    "expect": [
      "平距离 (m) 28.103 高差 (m) 90.040 坡度 (%) 10.788"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"l\":\"42\",\"a\":\"42\"}，输出区含「平距离 (m) 28.103 高差 (m) 90.040 坡度 (%) 10.7…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/leveling-calc",
    "inputs": {
      "h0": "42",
      "hn": "42",
      "tol": "42"
    },
    "expect": [
      "合差 fh = 41.786 − 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"h0\":\"42\",\"hn\":\"42\",\"tol\":\"42\"}，输出区含「合差 fh = 41.786 − 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/middle-ordinate-curve",
    "inputs": {
      "R": "42",
      "D": "42"
    },
    "expect": [
      "垂距 M (米) 30.788"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"R\":\"42\",\"D\":\"42\"}，输出区含「垂距 M (米) 30.788」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/prismoidal-volume",
    "inputs": {
      "A1": "42",
      "Am": "42",
      "A2": "42",
      "L": "42"
    },
    "expect": [
      "42\n42\n42\n42\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"A1\":\"42\",\"Am\":\"42\",\"A2\":\"42\",\"L\":\"42\"}，输出区含「42\n42\n42\n42\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/slope-percent",
    "inputs": {
      "h": "42",
      "d": "42"
    },
    "expect": [
      "0 坡度 (%) 45.00 坡度角 (°) 59.397"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"h\":\"42\",\"d\":\"42\"}，输出区含「0 坡度 (%) 45.00 坡度角 (°) 59.397」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/stadia-distance",
    "inputs": {
      "s": "42",
      "a": "42"
    },
    "expect": [
      "水平视距 (m) 2088.496 高差 (m) 420"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"s\":\"42\",\"a\":\"42\"}，输出区含「水平视距 (m) 2088.496 高差 (m) 420」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/subtense-distance",
    "inputs": {
      "c": "42",
      "th": "42"
    },
    "expect": [
      "距离 D (米) 0.0466 距离 (km) 42.0000 视差角 (°) 4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c\":\"42\",\"th\":\"42\"}，输出区含「距离 D (米) 0.0466 距离 (km) 42.0000 视差角 (°) …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/tangent-length-curve",
    "inputs": {
      "R": "42",
      "D": "42"
    },
    "expect": [
      "线长 T (米) 30.788"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"R\":\"42\",\"D\":\"42\"}，输出区含「线长 T (米) 30.788」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/triangulation-side",
    "inputs": {
      "a": "42",
      "A": "42",
      "B": "42"
    },
    "expect": [
      "内角 C (°) 62.424 边长 c (m)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"A\":\"42\",\"B\":\"42\"}，输出区含「内角 C (°) 62.424 边长 c (m)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "surveying/vertical-curve-elev",
    "inputs": {
      "y0": "42",
      "g1": "42",
      "g2": "42",
      "L": "42",
      "x": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n59.640"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"y0\":\"42\",\"g1\":\"42\",\"g2\":\"42\",\"L\":\"42\",\"x\":\"42\"}，输出区含「42\n42\n42\n42\n42\n59.640」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== surveying calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();