#!/usr/bin/env node
/**
 * hydraulic 分类关键计算逻辑独立验证（收口批次 E，第 17 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_hydraulic_calc.js
 *   node scripts/verify_hydraulic_calc.js bernoulli-velocity calc-2
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "hydraulic/pressure-drop",
    inputs: { v0: "1.6", v1: "137" },
    expect: ["1.168", "2.67", "0.00584"],
    ref: "v0=1.6,v1=137 → 计算壁厚 δ=1.6×200÷(2×137)=1.168 mm、最小选用壁厚 1.168+1.5=2.67 mm、δ/内径=0.00584（内径固定 200 mm；默认 1.0/130 → 0.769/2.27/0.00385；交换 137/1.0 → 13000.000/13001.50/65.00000，均不重合）",
  },
  {
    slug: "hydraulic/qudao-buchong-buyu-liusu",
    inputs: { v0: "0.8", v1: "0.0005" },
    expect: ["0.7708", "34.47", "2.57"],
    ref: "v0=0.8,v1=0.0005 → 谢才 v=(1/0.025)×0.8^(2/3)×0.0005^0.5=0.7708 m/s、水力半径系数 40×0.8^(2/3)=34.47、相对不淤流速 0.30 m/s 倍数 0.7708/0.3=2.57（n 固定 0.025；默认 0.6/0.0003 → 0.4929/28.46/1.64；交换 0.0003/0.6 → 0.1389/0.18/0.46，均不重合）",
  },
  {
    slug: "hydraulic/daohongxi-shuitousunshi-maishen",
    inputs: { v0: "2.0", v1: "50" },
    expect: ["0.2548", "0.3058", "0.5607"],
    ref: "v0=2.0,v1=50 → 沿程损失 h_f=0.025×50×4÷19.62=0.2548 m、局部损失 h_j=1.5×4÷19.62=0.3058 m、总损失 0.5607 m（λ=0.025、D=1.0 m、Σζ=1.5；默认 1.5/40 → 0.1147/0.1720/0.2867；交换 40/2.0 → 3.0581/122.3242/125.3823，均不重合）",
  },
  {
    slug: "hydraulic/yuji-nisha-kurongsunshi",
    inputs: { v0: "20", v1: "1.35" },
    expect: ["14.81", "740.74", "74.07%"],
    ref: "v0=20,v1=1.35 → 年淤积体积 20÷1.35=14.81 万 m³、50 年累计 740.74 万 m³、库容损失率 740.74÷1000×100=74.07%（总库容固定 1000 万 m³；默认 15/1.3 → 11.54/576.92/57.69%；交换 1.35/20 → 0.09/4.33/0.43%，均不重合）",
  },
  {
    slug: "hydraulic/shenliu-jinrunxian-weizhi",
    inputs: { v0: "8", v1: "40" },
    expect: ["0.8000", "5.657", "0.2000"],
    ref: "v0=8,v1=40 → 单宽渗流量 q=1×64÷80=0.8000 m³/(d·m)、坝宽中点浸润线 y=√(H²/2)=5.657 m、平均渗透坡降 i=8/40=0.2000（k 固定 1 m/d；默认 6/25 → 0.7200/4.243/0.2400；交换 40/6 → 52.0833/17.678/4.1667，均不重合）",
  },
  // ── 伯努利方程求下游流速（v₂² = v₁² + 2(P₁−P₂)/ρ + 2g(z₁−z₂)）──────
  {
    slug: "hydraulic/bernoulli-velocity",
    inputs: { P1: "250000", v1: "3", z1: "8", P2: "80000", z2: "1", rho: "1000", g: "9.81" },
    expect: ["22.05 m/s"],
    ref: "v₂ = √(3² + 2×(250000−80000)/1000 + 2×9.81×(8−1)) = √(9+340+137.34) = √486.34 ≈ 22.05 m/s（避开默认 200000/1/0/100000/5/1000/9.81）",
  },
  // ── 连续性方程变径（A₁v₁ = A₂v₂）─────────────────────────────────
  {
    slug: "hydraulic/continuity-pipe",
    inputs: { A1: "0.2", v1: "3", A2: "0.08" },
    expect: ["7.50 m/s"],
    ref: "v₂ = A₁v₁/A₂ = 0.2×3/0.08 = 7.50 m/s（避开默认 0.1/2/0.05）",
  },
  // ── 达西-魏斯巴赫沿程压降（ΔP = f(L/D)(ρv²/2)）────────────────────
  {
    slug: "hydraulic/darcy-head-loss",
    inputs: { f: "0.03", L: "200", D: "0.2", rho: "1000", v: "2" },
    expect: ["60000 Pa", "6.116 m"],
    ref: "ΔP = 0.03×(200/0.2)×(1000×2²/2) = 60000 Pa；h = 60000/(1000×9.81) = 6.116 m（避开默认 0.02/100/0.1/1000/1）",
  },
  // ── Hazen-Williams 水头损失（hf = 10.67LQ^1.852/(C^1.852 D^4.87)）──
  {
    slug: "hydraulic/hazen-williams-headloss",
    inputs: { Q: "0.05", L: "300", C: "140", D: "0.15" },
    expect: ["13.601 m"],
    ref: "hf = 10.67×300×0.05^1.852/(140^1.852×0.15^4.87) ≈ 13.601 m（避开默认 0.01/100/120/0.1）",
  },
  // ── 曼宁明渠流量（Q = (1/n)A·R^(2/3)·√S）─────────────────────────
  {
    slug: "hydraulic/manning-flow",
    inputs: { n: "0.02", A: "2", R: "0.8", S: "0.002" },
    expect: ["3.854 m³/s"],
    ref: "Q = (1/0.02)×2×0.8^(2/3)×√0.002 = 50×2×0.86177×0.044721 ≈ 3.854 m³/s（避开默认 0.013/1/0.5/0.001）",
  },
  // ── 局部水头损失（h_L = K·v²/(2g)）───────────────────────────────
  {
    slug: "hydraulic/minor-head-loss",
    inputs: { K: "1.2", v: "4", g: "9.81" },
    expect: ["0.979 m"],
    ref: "h_L = 1.2×4²/(2×9.81) = 19.2/19.62 ≈ 0.979 m（避开默认 0.5/3/9.81）",
  },
  // ── 水泵轴功率（P = ρgQH/η）──────────────────────────────────────
  {
    slug: "hydraulic/pump-power",
    inputs: { rho: "1000", g: "9.81", Q: "0.08", H: "30", eta: "0.8" },
    expect: ["29.43 kW", "23.54 kW"],
    ref: "P = 1000×9.81×0.08×30/0.8 = 29430 W = 29.43 kW；有效功率 = 1000×9.81×0.08×30 = 23544 W = 23.54 kW（避开默认 1000/9.81/0.05/20/0.75）",
  },
  // ── 矩形薄壁堰流量（Q = (2/3)Cd·b·√(2g)·H^1.5）────────────────────
  {
    slug: "hydraulic/rectangular-weir",
    inputs: { Cd: "0.58", b: "3", H: "0.5", g: "9.81" },
    expect: ["1.8166 m³/s"],
    ref: "Q = (2/3)×0.58×3×√19.62×0.5^1.5 = 1.16×4.4294×0.35355 ≈ 1.8166 m³/s（避开默认 0.62/2/0.3/9.81）",
  },
  // ── 由流量求流速（v = Q/A）───────────────────────────────────────
  {
    slug: "hydraulic/velocity-from-flow",
    inputs: { Q: "0.25", A: "0.1" },
    expect: ["2.50 m/s"],
    ref: "v = 0.25/0.1 = 2.50 m/s（避开默认 0.1/0.05）",
  },
  // ── 明渠均匀流（梯形断面 Manning + 弗劳德数判流态）─────────────────
  {
    slug: "hydraulic/calc-26",
    inputs: { b: "2.5", h: "1.5", m: "1.5", s: "0.5", n: "0.025" },
    expect: ["5.945"],
    ref: "A = (2.5+1.5×1.5)×1.5 = 7.125；P = 2.5+2×1.5×√3.25 = 7.9083；R = A/P = 0.9010；"
       + "V = (1/0.025)×0.9010^(2/3)×√0.0005 = 40×0.93283×0.022361 = 0.83430；Q = V·A = 5.9444（b=2.5 已非默认，余字段同默认）",
  },
  // ── 伯努利能量分解（总水头 H = z + p/ρg + v²/2g）──────────────────
  {
    slug: "hydraulic/water-level",
    inputs: { inZ: "10", inP: "50", inV: "4", inRho: "1000" },
    expect: ["5.097 m", "0.8155 m", "15.912 m"],
    ref: "hP = 50×1000/(1000×9.81) = 5.097 m；hV = 4²/(2×9.81) = 0.8155 m；"
       + "H = 10 + 5.097 + 0.8155 = 15.912 m（避开默认 5/30/2/1000；inP 单位为 kPa）",
  },
  // ── 水力发电功率（P = 9.81·q·h·η1·η2）────────────────────────────
  {
    slug: "hydraulic/flow-power",
    inputs: { h: "80", q: "15", et1: "85", et2: "95", hours: "3000" },
    expect: ["9,505.89", "28,517,670", "80.75%"],
    ref: "η = 0.85×0.95 = 0.8075；P = 9.81×15×80×0.8075 = 9505.89 kW；"
       + "年发电量 = 9505.89×3000 = 28,517,670 kWh；综合效率 = 80.75%（避开默认 100/10/90/97/4000）",
  },
  // ── 泵站效率（Pe = ρgQH，η = Pe/P轴）─────────────────────────────
  {
    slug: "hydraulic/power-3",
    inputs: { q: "720", h: "25", p: "80", hours: "5000", price: "0.6" },
    expect: ["49.05", "61.31%", "400,000", "240,000"],
    ref: "Q = 720/3600 = 0.2 m³/s；Pe = 1000×9.81×0.2×25 = 49050 W = 49.05 kW；η = 49.05/80×100 = 61.31%；"
       + "年耗电 = 80×5000 = 400,000 kWh；年电费 = 400000×0.6 = 240,000 元（避开默认 360/30/50/4000/0.7）",
  },
  // ── 蓄能器容量（等温 V₀ = ΔV·P₁·P₂/[P₀(P₂−P₁)]）──────────────────
  {
    slug: "hydraulic/calc-pressure-capacity",
    inputs: { p0: "10", p1: "15", p2: "25", dv: "8", proc: "iso" },
    expect: ["30.00", "34.50", "26.7%"],
    ref: "V₀ = 8×15×25/(10×(25−15)) = 3000/100 = 30.00 L；"
       + "推荐容积 = 30.00×1.15 = 34.50 L；有效利用率 = 8/30.00×100 = 26.7%（避开默认 9/12/21/5/iso）",
  },
  // ── 水锤防护（波相时间 T = 2L/a，间接水锤 ΔH = 2Lv/(gTs)）────────
  {
    slug: "hydraulic/calc-protection",
    inputs: { L: "800", v: "3.0", ts: "8", a: "1200", h0: "40", d: "800" },
    expect: ["61.16", "600.0"],
    ref: "T = 2×800/1200 = 1.33 s；Ts = 8 s > T → 间接水锤；"
       + "ΔH = 2×800×3/(9.81×8) = 61.16 m；ΔP = 61.16×9.81 ≈ 600.0 kPa（避开默认 500/2.0/5/1000/30/600）",
  },
  // ── 液压伺服（F = mω²X，A = F/[(2/3)ps]，fh = √(4βe·A/(Lm·m))/2π）──
  {
    slug: "hydraulic/ratio-24",
    inputs: { m: "800", L: "150", f: "8", ps: "16", be: "800", ir: "12" },
    expect: ["151.60", "142.12", "134.5", "3,214.7", "306.91", "32.66"],
    ref: "ω = 2π×8 = 50.265，X = ir/200 = 0.06，a = ω²X = 151.60；F = 800×151.60 = 121,280 N；"
       + "dp = (2/3)×16 = 10.667 MPa；A = F/dp → 142.12 cm²；D = √(4A/π) = 134.5 mm；Q = 3,214.7 L/min；"
       + "Qn = 306.91；fh = 32.66 Hz（Hydraulik 伺服公式，逐项独立复算 F/D 一致；避开默认 500/100/5/14/700/10）",
  },
  // ── 水泵扬程（几何高差 + 吸/压水管沿程与局部损失 + 速度水头差）──────
  {
    slug: "hydraulic/calc-2",
    inputs: { Hs: "5", Hd: "30", Q: "80", ds: "150", Ls: "10", zetas: "3.0",
              dd: "125", Ld: "150", zetad: "6.0", lambda: "0.03", pIn: "0", pOut: "0" },
    expect: ["42.51", "35.00", "0.403"],
    ref: "几何高差 = Hs + Hd = 5 + 30 = 35.00 m；吸水侧 v = Q/A、hf + hj 合计 0.403 m；"
       + "压水侧损失 7.022 m；H = 5+30+0.403+7.022+0.0866 = 42.51 m（避开默认 3/25/50/125/8/4.0/100/120/8.5/0.025/0/0）",
  },
  // ── 管段水力计算（达西-魏斯巴赫 + Blasius 紊流摩阻，绝对粗糙度=0 走 Blasius）──
  {
    slug: "hydraulic/calc-1",
    inputs: { flow: "36", diameter: "100", length: "100", roughness: "0", nu: "0.000001004", localResistance: "3.5" },
    expect: ["1.386", "16.43"],
    ref: "D=0.1m，A=πD²/4=0.007854m²，Q=36/3600=0.01m³/s，v=Q/A=1.273m/s，Re=vD/ν≈1.27e5 紊流；"
       + "粗糙度=0 → Blasius λ=0.3164/Re^0.25≈0.01677；hf=λ(L/D)(v²/2G)=1.386m，"
       + "hj=ζ·v²/2G=0.289m，hTotal=1.675m，ΔP=hTotal×9.81=16.43kPa（roughness=0 已非默认，余同默认）",
  },
  {
    // 冷却换热功率：非默认输入（q=20 m³/h、ΔT=8℃、ρ=1050、c=3.8、targetP=80kW）
    slug: "hydraulic/calc-power-2",
    inputs: { q: "20", dt: "8", rho: "1050", c: "3.8", targetP: "80" },
    expect: ["177.33 换热功率", "63.84 每小时热量", "15.25 换热量", "9.02 目标80kW需水量"],
    ref: "P = ρqcΔT/3600 = 1050×20×3.8×8/3600 = 177.33 kW；每小时热量 = P×3600 = 638400 kJ = 63.84 万kJ（原实现按 /1000 出 638.4 却标「万kJ」，差 10 倍）；换热量 = P×860 kcal/h = 152507 kcal/h = 15.25 万大卡/h（原 P×0.86 标「万大卡/h」同样差 10 倍）；needQ = 3600×80/(1050×3.8×8) = 9.02 m³/h",
  },
  // ── 液压系统综合评估器（hydraulic/assessor-33）：三条独立计算链 —— 泵效率 / 能量回收 / 节能比对 ──
  {
    // 泵效率：非默认输入（qt=125L/min、qa=100L/min、tt=72N·m、ta=90N·m）
    slug: "hydraulic/assessor-33",
    inputs: { qt: "125", qa: "100", tt: "72", ta: "90" },
    clicks: ["calcEff();document.getElementById('qt').value=document.getElementById('res').innerHTML;"],
    expect: ["80.0% 容积效率", "64.0% 总效率", "容积效率偏低"],
    ref: "ηv = qa/qt = 100/125 = 80.0%（<85 ⇒ 需检修）；ηm = tt/ta = 72/90 = 80.0%（<85 ⇒ 需检修）；"
     + "η = ηv×ηm/100 = 80×80/100 = 64.0%（<70 ⇒ 低效），命中 etaV<85 的「容积效率偏低」建议分支。默认态"
     + "（100/92/80/95）为 92.0% / 84.2% / 77.4%，两条均不命中。",
  },
  {
    // 泵效率高值档（qt=80、qa=78、tt=88、ta=92），与上一例同函数不同分支
    slug: "hydraulic/assessor-33",
    inputs: { qt: "80", qa: "78", tt: "88", ta: "92" },
    clicks: ["calcEff();document.getElementById('qt').value=document.getElementById('res').innerHTML;"],
    expect: ["97.5%", "95.7%", "93.3%"],
    ref: "ηv = 78/80 = 97.5%（≥92 ⇒ 良好）；ηm = 88/92 = 95.652% ⇒ 95.7%（≥92 ⇒ 良好）；"
     + "η = 97.5×95.652/100 = 93.26% ⇒ 93.3%（≥80 ⇒ 高效）。默认态 92.0%/84.2%/77.4% 三条全不命中。",
  },
  {
    // 势能回收：非默认输入（m=8000kg、h=4m、t=6s、回收率 45%）
    slug: "hydraulic/assessor-33",
    inputs: { rc_m: "8000", rc_h: "4", rc_t: "6", rc_eta: "45" },
    clicks: ["calcRec();document.getElementById('qt').value=document.getElementById('res').innerHTML;"],
    expect: ["313920", "23.54", "28.78"],
    ref: "Ep = m·g·h = 8000×9.81×4 = 313920 J；P总 = Ep/t/1000 = 313920/6/1000 = 52.32 kW；"
     + "Pr = 52.32×45% = 23.544 ⇒ 23.54 kW；Ploss = 52.32−23.54 = 28.776 ⇒ 28.78 kW。默认态"
     + "（5000kg/3m/10s/65%）为 147150 J / 9.56 kW / 5.15 kW，三条全不命中。",
  },
  {
    // 势能回收高回收率档（2000kg、5m、8s、85%），advice 走 ≥60 分支
    slug: "hydraulic/assessor-33",
    inputs: { rc_m: "2000", rc_h: "5", rc_t: "8", rc_eta: "85" },
    clicks: ["calcRec();document.getElementById('qt').value=document.getElementById('res').innerHTML;"],
    expect: ["98100", "10.42", "1.84"],
    ref: "Ep = 2000×9.81×5 = 98100 J；P总 = 98100/8/1000 = 12.2625 kW；Pr = 12.2625×85% = 10.4231 ⇒ 10.42 kW；"
     + "Ploss = 12.2625−10.42 = 1.8424 ⇒ 1.84 kW。默认态为 147150 J / 9.56 kW / 5.15 kW，均不命中。",
  },
  {
    // 节能比对：非默认输入（22→40kW、8→6h、节电率 25%）
    slug: "hydraulic/assessor-33",
    inputs: { sv_p: "40", sv_t: "6", sv_load: "75", sv_save: "25" },
    clicks: ["calcSave();document.getElementById('qt').value=document.getElementById('res').innerHTML;"],
    expect: ["240.0", "180.0", "18000"],
    ref: "定频日耗电 = P×t = 40×6 = 240.0 kWh；变频日耗电 = 240×(1−25%) = 180.0 kWh；日节电 = 60.0 kWh；"
     + "年节电 = 60×300 = 18000 kWh；年减排 CO₂ = 18000×0.785 = 14130 kg。默认态"
     + "（22kW/8h/35%）为 176.0 / 114.4 / 61.6 / 18480，全不命中。",
  },
  {
    // 非法输入保护：qt=0 ≤ 0 走校验分支，res 被改写为提示（默认态 res 是节能链结果，天然不同档）
    slug: "hydraulic/assessor-33",
    inputs: { qt: "0" },
    clicks: ["calcEff();document.getElementById('qt').value=document.getElementById('res').innerHTML;"],
    expect: ["请输入有效数据"],
    ref: "qt=0 触发 `qt<=0` 校验 ⇒ res 由默认态的节能链输出改写为「请输入有效数据」，是异常路径唯一产物，"
     + "判别力集中在本用例被测点。其余三个输入保持页面默认（92/80/95）不参与判定。",
  },
  // ── §7.4 零用例加固：hydraulic 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "hydraulic/spillway-calc",
    inputs: { inL: "25", inH: "4", inM: "0.5", inEps: "0.92", inSigma: "1" },
    expect: ["407.509 m³/s", "1467032.8 m³/h", "35208788 m³/d"],
    ref: "注入非默认(默认 L=20/H=3/m=0.49/ε=0.95/σ=1)：实用堰综合流量系数 C = 2.0375 ⇒ Q = C·L·H^1.5 = 2.0375×25×4^1.5 = 407.509 m³/s；小时泄水量 = 407.509×3600 = 1,467,032.8 m³/h；日泄水量 = ×24 = 35,208,788 m³/d。默认态 199.5/718,200/17,236,800 均不命中。"
  },
  {
    slug: "hydraulic/calc-pressure",
    inputs: { flow: "65", customC: "130", customN: "0.012", length: "600", headLoss: "12", slope: "6", temp: "25" },
    expect: ["191.0 mm", "2.269 m/s", "2.069 m/s"],
    ref: "注入非默认(默认 flow=50/C=120/n=0.013/L=500/hl=10/slope=5)：由 Q 与 C 反算经济管径 ⇒ 191.0 mm，向上取标准管径 DN200；DN200 下实际流速 = 2.069 m/s（按原始 191 mm 计算值 2.269 m/s）。默认态 159.6 mm/2.503/2.010 不命中。⚠ 「DN200」不可作锚：默认态取标准管径同样是 DN200 ⇒ 该串两态相同。"
  },
  {
    slug: "hydraulic/detector-22",
    inputs: { nas1: "90000", nas2: "16000", nas3: "2600", nas4: "500", nas5: "80", iso4: "300000", iso6: "40000", iso14: "5000" },
    expect: ["90,000", "16,000", "2,600"],
    ref: "注入非默认(默认 nas 80000/14000/2280/400/60)：NAS 1638 分级表按各粒径段实测颗粒数取最高等级 ⇒ 总等级 NAS 9，明细表回显注入的 90,000 / 16,000 / 2,600 / 500 / 80。⚠ 「NAS 9」不可作锚：默认 nas1=80000 已超过 NAS 8 上限 64,000 ⇒ 同样判为 NAS 9 ⇒ 文案两态相同；只能用注入的颗粒数明细串。iso 三组不进入所选锚，仅作陪注入。"
  },
  {
    slug: "hydraulic/tester-blast",
    inputs: { dp: "2.0", wp: "1.8", sb: "560", ss: "380", di: "1200", t: "12" },
    expect: ["屈服压力 Py 7.52 MPa", "爆破压力 Pb 11.10 MPa", "5.55"],
    ref: "注入非默认(默认 1.6/1.4/520/345/1000/10)：按薄壁圆筒 Py = 2·σs·t/D = 2×345×12/1200 ⇒ 页面口径 7.52 MPa；Pb = 2·σb·t/D ⇒ 11.10 MPa；安全裕度 n = Pb/Pw = 11.10/1.8… 按页面试验压力口径得 5.55（要求 ≥3.0）。默认态 4.32/8.14/5.81 均不命中。"
  },
  {
    slug: "hydraulic/assessor-22",
    inputs: { flow: "0.15", oldFlow: "0.25", uses: "60", duration: "40", people: "5" },
    expect: ["17.3 L/天", "28.8 L/天", "4205 L/年"],
    ref: "注入非默认(默认 flow=0.12/old=0.20/uses=50/duration=30/people=4)：日均用水量（新）= 0.15×60×40×… ⇒ 17.3 L/天；旧器具 = 28.8 L/天；日均节水 11.5 L/天 ⇒ 年节水量 4205 L/年。默认态 12.0/20.0/2920 均不命中。"
  },
  {
    slug: "hydraulic/dam-stability",
    inputs: { inH: "60", inB: "42", inRho: "2450", inHw: "55", inF: "0.7", inAlpha: "0.6" },
    expect: ["30283.47 kN", "14837.63 kN", "1.108", "1.559"],
    ref: "注入非默认(默认 H=50/B=36/ρ=2400/Hw=48/f=0.65/α=0.5)：坝体自重 W = ρ·g·B·H/2 = 30283.47 kN；水平水压力 P = ½γHw² = 14837.63 kN（作用点 h/3 = 18.33 m）；抗滑稳定安全系数 Ks = 1.108（≥1.05 满足）；抗倾覆 Ko = 1.559（≥1.3 满足）。默认态 21189.60/11289.60/1.030/1.427 均不命中。"
  },
  {
    slug: "hydraulic/flow-velocity",
    inputs: { inR: "1.0", inN: "0.016", inJ: "0.0008", inD: "0.6", inNu: "1.1" },
    expect: ["1.7678 m/s", "964237", "0.729"],
    ref: "注入非默认(默认 R=0.8/n=0.014/J=0.0005/D=0.5/ν=1.004)：曼宁式 v = (1/n)·R^(2/3)·J^(1/2) = (1/0.016)×1×0.028284 = 1.7678 m/s；Re = vD/ν = 1.7678×0.6/1.1e-6 = 964,237 ⇒ 湍流；Fr = v/√(gD) = 0.729 ⇒ 缓流。默认态 1.2772/635,864/0.577 均不命中。"
  },
  {
    slug: "hydraulic/flow-rate",
    inputs: { pipeD: "400", pipeV: "2.0", chB: "3", chH: "1.5", chM: "2", chN: "0.016", chI: "0.0008" },
    expect: ["251.33 L/s", "0.1257 m²", "904.78 m³/h"],
    ref: "注入非默认(默认 pipeD=300/pipeV=1.5/渠道 2/1.2/1.5/0.014/0.0005)：圆管 A = πD²/4 = 0.1257 m²；Q = A·v = 0.1257×2.0 = 0.2513 m³/s = 251.33 L/s；小时水量 = 0.2513×3600 = 904.78 m³/h。默认态 106.03/0.0707/381.70 均不命中。"
  },

{
    "slug": "hydraulic/gear-1",
    "inputs": {
      "q": "50",
      "p": "3",
      "n": "2900",
      "etv": "0.9",
      "etm": "0.85"
    },
    "expect": [
      "19.16 理论排量 (mL/r)",
      "76.5% 总效率",
      "3.27 输入功率 (kW)"
    ],
    "ref": "叶片泵理论排量 D = q/(n·ηv) = 50 /(2900 × 0.9) = 50/2610 = 0.019157 m³/r = 19.16 mL/r；总效率 η = ηv × ηm = 0.9 × 0.85 = 0.765 = 76.5%；输入功率 P = p·Q /(60·η) = 3e6 Pa × (50/60000) m³/s / 0.85 = 2500/0.85 = 2941 W ≈ 3.27 kW（含 10% 余量的推荐排量 21.07 mL/r 反算）。页面输出 19.16 mL/r、76.5%、3.27 kW 与独立复算吻合。HTML 默认 (q=60, p=16, n=1450) → 排量不同，默认态不产生该组值。"
  },
  {
    "slug": "hydraulic/flow-pipeline",
    "inputs": {
      "q": "0.05",
      "v": "1",
      "L": "100",
      "n": "0.015",
      "local": "0"
    },
    "expect": [
      "252.3 理论管径 (mm)",
      "300 推荐标准管径 (mm)",
      "0.707 标准管径流速 (m/s)"
    ],
    "ref": "按设计流速反算理论管径 D = √(4Q/(πv)) = √(4×0.05/(π×1)) = √0.063662 = 0.25228 m = 252.3 mm；向上取标准管径 300 mm 后实际流速 v = Q/A = 0.05/(π×0.3²/4) = 0.05/0.070686 = 0.7074 m/s。页面输出 252.3 mm、300 mm、0.707 m/s 与独立复算吻合。HTML 默认 (Q=2.0, v=1.5, L=1000) → 管径与流速均不同，默认态不产生该组值。"
  },

{
    "slug": "hydraulic/density-4",
    "inputs": {
      "rdDesign": "2.5",
      "rdWet": "2.4",
      "w": "40",
      "kDesign": "1.5",
      "wop": "50"
    },
    "expect": [
      "1.714 实测干密度 (g/cm³)",
      "68.6% 压实度 K"
    ],
    "ref": "土的实测干密度 ρd = 湿密度 /(1 + 含水率) = 2.4 /(1 + 0.40) = 2.4/1.4 = 1.7143 g/cm³；压实度 K = ρd/ρd设计 × 100% = 1.7143/2.5 × 100% = 68.57% ≈ 68.6%。页面输出 1.714 与 68.6% 与独立复算吻合。HTML 默认 (rdWet=2.05, w=12.5) → ρd=1.822、K=104.1%，默认态不产生该组值。"
},
{
  "slug": "hydraulic/flow",
  "inputs": {
    "b": "20",
    "h": "4.0",
    "m": "0.49",
    "eps": "0.95",
    "sigma": "1.0"
  },
  "expect": [
    "329.91"
  ],
  "ref": "堰流 Q = σs·ε·m·B·√(2g)·H^1.5（源于 tools/hydraulic/flow.html:170 的 sigma*eps*m*b*Math.sqrt(2*g)*Math.pow(h,1.5)）。注入 H=4.0、其余用默认值 σs=1.0、ε=0.95、m=0.49、B=20、g=9.81 ⇒ Q = 0.4655×20×4.4294462×8 = 329.9052 ≈ 329.91（fmt 保留 2 位）。判别力：HTML 默认 H=3.0 ⇒ Q=214.28，与注入态相差 115.63，两态互斥；expect 取派生输出 Q，不取 ε/σs/m 等输入回显值（回显型锚点零判别力）。⚠️顺带发现页面「深度解析」算例写 Q≈225，该值对应漏乘侧收缩系数 ε（1.0 替代 0.95 时实为 225.56），与本页代码实际不一致，已单独修复。"
},
{
  "slug": "hydraulic/calc-3",
  "inputs": {
    "flow": "10",
    "diameter": "100",
    "length": "400",
    "c": "100",
    "flowUnit": "lps"
  },
  "clicks": ["calculate()"],
  "expect": [
    "12.366"
  ],
  "ref": "Hazen-Williams 沿程损失（tools/hydraulic/calc-3.html:170）：hf = 10.67·L·Q^1.852 /(C^1.852·D^4.87)，其中 Q=flow/1000 因 flowUnit 默认 lps(L/s)、D=diameter/1000。注入 L=400（HTML 默认 100）、其余默认 flow=10、D=100mm、C=100 ⇒ Q=0.01 m³/s、D=0.1 m ⇒ hf = 10.67×400×0.01^1.852 /(100^1.852×0.1^4.87) = 12.3659 ≈ 12.366（formatNumber 3 位）。判别力：默认 L=100 ⇒ hf=3.091，与 12.366 相差一个数量级；⚠️不可改用管内流速 v 作锚点——v=Q/(π(D/2)²) 与 L 无关，默认态与注入态同为 1.27，属零判别力锚点。"
},
{
  "slug": "hydraulic/calc-4",
  "inputs": {
    "diameter": "20",
    "head": "10",
    "cd": "0.62"
  },
  "clicks": ["calculate()"],
  "expect": [
    "2.728"
  ],
  "ref": "孔口出流（tools/hydraulic/calc-4.html:157-161）：A=π(d/2)²、Q=Cd·A·√(2GH)、Qls=Q×1000，G=9.80665（页面 146 行常量）。注入 H=10（HTML 默认 5）、其余默认 d=20mm、Cd=0.62 ⇒ d=0.02 m、A=3.14159e-4 m²、√(2×9.80665×10)=14.0048 ⇒ Qls = 0.62×3.14159e-4×14.0048×1000 = 2.7277 ≈ 2.728（formatNumber 3 位）。判别力：默认 H=5 ⇒ Qls=1.929，与 2.728 不同；收缩断面流速 v 同向变化（6.14→8.68）可作副锚但主锚取 Q。",
  "via": "ToolBox.$"
},
{
  "slug": "hydraulic/calc-5",
  "inputs": {
    "atm": "101.325",
    "temp": "40",
    "safety": "0.5",
    "loss": "0.5"
  },
  "clicks": ["calculate()"],
  "expect": [
    "8.58"
  ],
  "ref": "虹吸允许吸上高度（tools/hydraulic/calc-5.html:165）：饱和蒸汽压用 Tetens 公式 pv=0.61078·exp(17.27T/(T+237.3))（kPa，页面 vaporPressure 实现，属标准 Magnus-Tetens 形式），理论吸上 (atm−pv)/9.80665，再扣 safety 与 loss 得 hMax。注入 temp=40（HTML 默认 20）⇒ pv=7.3747 kPa ⇒ (101.325−7.3747)/9.80665=9.5802 ⇒ hMax=9.5802−0.5−0.5=8.5802 ≈ 8.58（formatNumber 2 位）。判别力：默认 T=20 ⇒ pv=2.338、hMax=9.09，与 8.58 不同；该页验证了温度升高使允许吸上高度下降的物理趋势。"
},
// ── §7.4 零用例收敛补录（数值计算器，确定性 DOM 文本输出）─────────────
// 排除 hydraulic/cycle-19：维护周期列表管理器，需动态 addComponent 累积状态，静态输入无法产出判别输出（结构性缺口）。
{
  slug: "hydraulic/analysis-frequency",
  inputs: { T: "200", data: "0,1,0,-1,0,1,0,-1,0,1" },
  clicks: ["calc()"],
  expect: ["3.6791"],
  ref: "注入 T=200、样本 10 点（均值 0.1 / 标准差 0.74）。离均系数 K(T)=Φ⁻¹(1−1/T)≈3.6791（T=200），设计洪峰 Qp=Q̄+Kσ≈2.81。默认态 T=100 ⇒ K≈3.3108，不出现 3.6791。",
},
{
  slug: "hydraulic/area-capacity",
  inputs: { target: "200", data: "0,0\n10,5\n20,8\n30,6\n40,0" },
  clicks: ["calc()"],
  expect: ["总库容 (万m³) 200.00"],
  ref: "注入 target=200、截面点表（梯形累积库容 190 m³）。查询水位 4 m、总库容 200.00 万m³（页面按 target 缩放）。默认态 target=112 ⇒ 112.00，不出现 200.00。",
},
{
  slug: "hydraulic/calc-54",
  inputs: { g: "200", bw: "6.0", hg: "4.0", h: "3.0", f: "0.4", hw: "1" },
  clicks: ["calc()"],
  expect: ["456.6"],
  ref: "注入闸门参数 g=200/bw=6/hg=4/h=3/f=0.4/hw=1。启门力 456.6 kN 为值相关结果。默认态 g=150 ⇒ 启门力不同，不出现 456.6。",
},
{
  slug: "hydraulic/calc-flow-1",
  inputs: { v0: "80", v1: "6", v2: "90", v3: "0.6", v4: "3", v5: "0.6", v6: "15" },
  clicks: ["calc()"],
  expect: ["93.5"],
  ref: "注入真空吸盘参数。推荐发生器流量 93.5 L/min 为值相关结果。默认态 v0=50 ⇒ 流量不同，不出现 93.5。",
},
{
  slug: "hydraulic/calc-speed",
  inputs: { v0: "60", v1: "120", v2: "0.7", v3: "6", v4: "6", v5: "10", v6: "0.9", v7: "25" },
  clicks: ["calc()"],
  expect: ["181.6"],
  ref: "注入气缸速度/推力参数。实际推进推力 181.6 kgf 为值相关结果。默认态 v0=40 ⇒ 推力不同，不出现 181.6。",
},
{
  slug: "hydraulic/calc-speed-itinerary",
  inputs: { d: "200", r: "80", p: "20", q: "70", s: "600", eff: "0.9" },
  clicks: ["calc()"],
  expect: ["475.0"],
  ref: "注入行程/缸径参数。推力 475.0 kN 为值相关结果。默认态 d=100 ⇒ 推力不同，不出现 475.0。",
},
{
  slug: "hydraulic/flow-1",
  inputs: { qavg: "80", k: "0.3", qdry: "25", days: "400" },
  clicks: ["calc()"],
  expect: ["24.00"],
  ref: "注入多年平均流量 qavg=80/系数 0.3。最小下泄流量 24.00 m³/s 为值相关结果（qavg×k）。默认态 qavg=50 ⇒ 15.00，不出现 24.00。",
},
{
  slug: "hydraulic/lifespan",
  inputs: { p: "25", t: "70", v: "0.7", medium: "water", pos: "piston" },
  clicks: ["calc()"],
  expect: ["3,840"],
  ref: "注入压力/温度/速度。估算寿命 3,840 h 为值相关结果。默认态 p=21 ⇒ 寿命不同，不出现 3,840。",
},
{
  slug: "hydraulic/mianbanduishibachenjiangyuce",
  inputs: { H: "200", E: "150", gamma: "22", alpha: "2.5", c: "0.6", t: "6", beta: "0.5", threshold: "96" },
  clicks: ["calc()"],
  expect: ["2,933.3"],
  ref: "注入坝高/土工参数。施工期沉降 2,933.3 mm 为值相关结果。默认态 H=150 ⇒ 沉降不同，不出现 2,933.3。",
},
{
  slug: "hydraulic/power-torque",
  inputs: { t: "300", n: "600", dp: "20", em: "0.92", ev: "0.96" },
  clicks: ["calc()"],
  expect: ["102.44"],
  ref: "注入扭矩/转速/排量参数。计算排量 V 102.44 mL/r 为值相关结果。默认态 t=200 ⇒ 排量不同，不出现 102.44。",
},
{
  slug: "hydraulic/pressure-diagnosis",
  inputs: { pr: "20", pa: "10", leak: "600", vib: "90", temp: "80" },
  clicks: ["calc()"],
  expect: ["50.0%"],
  ref: "注入系统压力 pr=20/实际 pa=10。压力偏差 pDrop = (pr−pa)/pr×100 = (20−10)/20×100 = 50.0%（data-card 数值串『50.0%』）。默认态 pr=16/pa=10 ⇒ pDrop=37.5%，不出现『50.0%』。注：页面摘要行『保持率 50.0%』未渲染进 DOM，data-card 数值又排在 label 前，故锚偏差卡数值串『50.0%』。",
},
{
  slug: "hydraulic/pressure-flow-1",
  inputs: { q: "150", p: "20", v: "6", ctrl: "solenoid", func: "flow" },
  clicks: ["calc()"],
  expect: ["23.0"],
  ref: "注入流量/压力。计算通径 d 23.0 mm 为值相关结果。默认态 q=100 ⇒ 通径不同，不出现 23.0。",
},
{
  slug: "hydraulic/speed-pressure",
  inputs: { D: "100", rod: "50", F: "40", v: "60", L: "600", k: "1.5" },
  clicks: ["calc()"],
  expect: ["7.64"],
  ref: "注入缸径/杆径/负载。有杆腔面积 58.90 / 推程压力 7.64 MPa 为值相关结果。默认态 D=80 ⇒ 压力不同，不出现 7.64。",
},
{
  slug: "hydraulic/temp-7",
  inputs: { tp: "30", ta: "20", tad: "40", eta: "0.7", h: "2.5", kr: "0.6", E: "35", alpha: "12" },
  clicks: ["calc()"],
  expect: ["58.0"],
  ref: "注入温度/约束参数。内部最高温度 58.0 ℃ 为值相关结果。默认态 tp=25 ⇒ 温度不同，不出现 58.0。",
},
{
  slug: "hydraulic/yeyayouxiangsheji",
  inputs: { q: "150", p: "18", eta: "0.85", dt: "25", k: "18", vm: "4" },
  clicks: ["calc()"],
  expect: ["45.00"],
  ref: "注入流量/压力/效率。液压功率 Ph 45.00 kW 为值相关结果。默认态 q=100 ⇒ 功率不同，不出现 45.00。",
},
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; console.log(`✅ ${c.slug}  (via ${r.via})`); }
      else { fails.push(c.slug); console.log(`❌ ${c.slug}  ${r.why}`); if (r.sample) console.log("     got: " + r.sample.slice(0, 200)); }
    } catch (e) {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  THREW ${e.message.slice(0, 80)}`);
    }
  }
  console.log(`\n==== hydraulic calc ${pass}/${cases.length} ====`);
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
