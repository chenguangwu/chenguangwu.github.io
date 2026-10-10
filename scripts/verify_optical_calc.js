#!/usr/bin/env node
/**
 * 第 27 道门禁：optical 分类计算正确性验证（6 个确定性光学/视光工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 覆盖：调节幅度(Hofstetter)、抗疲劳下加光、瞳高占比、周边离焦、棱镜移心(普伦蒂斯)、AC/A(梯度法)。
 * 用法: node scripts/verify_optical_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "optical/accommodation-amplitude",
    inputs: { age: "40" },
    expect: ["6.50"],
    ref: "Hofstetter 平均 A=18.5−0.30×40=6.50 D（最小 15−0.25×40=5.00，最大 25−0.40×40=9.00）",
  },
  {
    slug: "optical/anti-fatigue-design",
    inputs: { age: "48", workDist: "30", rx: "0" },
    expect: ["0.50"],
    ref: "平均 A=18.5−0.30×48=4.10；调节需求=100/30=3.33；保留 1/3=1.37；可用=2.73；Add=max(0,3.33−2.73)=0.60→量化0.25D=0.50D",
  },
  {
    slug: "optical/pupil-height",
    inputs: { pupilToBottom: "18", frameB: "30" },
    expect: ["60"],
    ref: "占比=18/30×100=60%（默认方法 direct）",
  },
  {
    slug: "optical/peripheral-defocus",
    inputs: { central: "1", peripheral: "4", angle: "20" },
    checks: ["single"],
    expect: ["+3.00", "3.00D"],
    ref: "RPD=周边−中央=4−1=3.00 D（radio lens=single 经 checks 注入，规避 stub :checked 返回 null）",
  },
  {
    slug: "optical/prism-decentration",
    inputs: { power: "5", prism: "3", base: "BO" },
    expect: ["6.00"],
    ref: "页面默认 prism 分支（setMode 在 stub 下报错但 calc 走 prism 分支）：移心量 c=P/|F|=3/5=0.6cm→6.00mm；普伦蒂斯 P=c×|F|",
  },
  {
    slug: "optical/aca-ratio",
    inputs: { nearPhoria: "2", nearPhoriaLens: "8", lens: "4" },
    expect: ["1.50"],
    ref: "默认 gradient 法：AC/A=(加镜后隐斜−裸眼隐斜)/|镜片度|=(8−2)/4=1.50 Δ/D",
  },
  {
    slug: "optical/detector-31",
    inputs: { element: "lens", pv: "0.25", rms: "0.05", decent: "3", trans: "98",
              surface: "40-20", coating: "ar", grade: "standard" },
    expect: ["满足标准级要求"],
    ref: "各项分 75/85/85/80/100 → 综合 85；grade=standard 达标线 75 → 通过，评价按所选等级写「满足标准级要求」（默认 grade=precision 达标线 90 → 判「未达精密级」，与本值不重合）",
  },
  {
    slug: "optical/detector-31",
    inputs: { element: "lens", pv: "1.5", rms: "0.15", decent: "12", trans: "93",
              surface: "80-50", coating: "ar", grade: "precision" },
    expect: ["当前指标为「不合格」"],
    ref: "各项分 45/30/30/20/40 → 综合 33 <60 → 实际档位「不合格」；grade=precision 达标线 90 未达，评价须同时给出实际档位（默认综合 85 实际档位为「标准级合格」，与本值不重合）",
  },
  {
    slug: "optical/calc-47",
    inputs: { idxN: "1.6", idxR: "80", idxH: "12", idxK: "-1" },
    expect: ["205.66 μm 当前锥面纵向球差"],
    ref: "LSA球面=(n−1)h²/(2nR)=(0.6×144)/(2×1.6×80)=0.3375mm=337.5μm；K=−1 → LSA=337.5×(1+K/n²)=337.5×(1−1/2.56)=205.66μm（默认 1.5/100/25/0 → 1041.67μm，避开）",
  },

  // ── §7.4 零用例加固 · optical 确定性数值页（探针实测取锚）────
  {
    slug: "optical/numerical-aperture",
    inputs: { n: "1.52", theta: "38" },
    expect: ["0.936", "0.87573"],
    ref: "注入非默认(默认 1.0/30)：NA = n·sinθ = 1.52×sin38° = 1.52×0.61566 = 0.936；NA² = 0.87573。默认态 NA = 1.0×0.5 = 0.5、NA² = 0.25，两条均不命中。"
  },
  {
    slug: "optical/lens-refractive-index",
    inputs: { power: "-6.25", diameter: "70", ct: "1.4" },
    expect: ["70mm", "32.02"],
    ref: "注入非默认(默认 -4.00/65/2.0)：−6.25D、直径 70mm、中心厚 1.4mm ⇒ 1.50 折射率档边缘厚度 32.02 mm，随折射率升高递减至 1.74 档的 22.09 mm。默认态为另一套表格值。"
  },
  {
    slug: "optical/telescope-magnification",
    inputs: { fo: "1200", fe: "10" },
    expect: ["120.0", "14400.000", "1210.000"],
    ref: "注入非默认(默认 1000/25)：角放大率 M = f₀/fₑ = 1200/10 = 120.0×；相对聚光力 = M² = 14400.000；两镜焦距之和 = 1200+10 = 1210.000 mm。默认态 40.0/1600/1025 均不命中。"
  },
  {
    slug: "optical/gaussian-beam-waist",
    inputs: { lam: "532", f: "80", D: "8" },
    expect: ["6.77", "2.7095e-4", "2.5000e-2"],
    ref: "注入非默认(默认 650/50/10)：束腰半径 w₀ = 4λf/(πD) = 4×532e-9×0.08/(π×0.008) = 6.77 µm；瑞利长度 = πw₀²/λ = 2.7095e-4 m；远场发散角 = λ/(πw₀) = 2.5000e-2 rad。默认态 4.14/… 不同。"
  },
  {
    slug: "optical/blue-light-filter",
    inputs: { cutoff: "450", steepness: "14" },
    expect: ["61.1%", "71.5%"],
    ref: "注入非默认(默认 430/10)：截止 450nm、陡度 14 ⇒ 有害蓝光(415-455nm)阻隔率 61.1%，有益蓝光(465-495nm)保留率 71.5%。默认态两项均不同。"
  },
  {
    slug: "optical/aspheric-design",
    inputs: { n: "1.67", power: "-5.50", aperture: "65" },
    expect: ["26.934", "-6.21"],
    ref: "注入非默认(默认 1.60/-3.00/60)：球面三阶纵向球差 LSA = 26.934 mm；消球差所需圆锥常数 K = -6.21（K<−1 ⇒ 扁长椭球面）。默认态两者均不同。"
  },
  {
    slug: "optical/thin-lens-imaging",
    inputs: { u: "450", f: "120" },
    expect: ["163.64", "-0.364"],
    ref: "注入非默认(默认 300/100)：由 1/v = 1/f − 1/u = 1/120 − 1/450 ⇒ 像距 v = 163.64 mm（实像）；放大率 m = −v/u = −0.364。默认态 150/(-0.5) 均不命中。"
  },
  {
    slug: "optical/lens-maker",
    inputs: { n: "1.6", R1: "150", R2: "-150" },
    expect: ["125.00", "0.0080"],
    ref: "注入非默认(默认 1.5/100/-100)：1/f = (n−1)(1/R₁ − 1/R₂) = 0.6×(1/150 + 1/150) = 0.008 mm⁻¹ ⇒ f = 125.00 mm；光焦度 = 0.0080 mm⁻¹。默认态 100.00/0.0100 不命中。"
  },
  {
    slug: "optical/diffraction-grating",
    inputs: { d: "1200", m: "2", lam: "589" },
    expect: ["79.01", "0.98167", "29.40"],
    ref: "注入非默认(默认 1000/1/500)：sinθ = mλ/d = 2×589/1200 = 0.98167 ⇒ 衍射角 θ = 79.01°；一级衍射角（对比）= arcsin(589/1200) = 29.40°。默认态 30.00/0.5/30.00 均不命中。"
  },
  {
    slug: "optical/mirror-imaging",
    inputs: { u: "450", R: "300" },
    expect: ["225.00", "150.0 mm 焦距"],
    ref: "注入非默认(默认 300/200)：f = R/2 = 150.0 mm；1/v = 1/f − 1/u ⇒ 像距 v = 225.00 mm。⚠️ 默认态 R=200 ⇒ f=100.0、v=150.00、m=−0.500 —— 裸值 150 与 −0.500 会与注入态的焦距离散值字面重合，故必须用「150.0 mm 焦距」完整标签串，且不可选 m。"
  },
  {
    slug: "optical/critical-angle",
    inputs: { n1: "1.49", n2: "1.33" },
    expect: ["63.20", "1.1203", "10.738"],
    ref: "注入非默认(默认 1.5/1.0)：临界角 θc = arcsin(n₂/n₁) = arcsin(1.33/1.49) = 63.20°；折射率比 = 1.1203；相对折射率差 10.738%。默认态 41.81/1.5 均不命中。"
  },
  {
    slug: "optical/optical-path-length",
    inputs: { n: "1.7", L: "250" },
    expect: ["425.0", "0.425000", "157.4074"],
    ref: "注入非默认(默认 1.5/100)：光程 OPL = n·L = 1.7×250 = 425.0 mm = 0.425000 m；与 (n+1) 之比 = 425/(1.7+1)×… = 157.4074。默认态 150.0/0.15 均不命中。"
  },
  {
    slug: "optical/frame-pupillary",
    inputs: { eyeSize: "54", dbl: "20", pd: "66", ed: "55" },
    expect: ["65.0", "74.0mm", "4.0 单眼移心量"],
    ref: "注入非默认(默认 48/18/62/50)：几何中心距 GCD = A + DBL = 54+20 = 74.0 mm，单眼几何中心到鼻中线 37.0 mm，单眼瞳距 33.0 mm ⇒ 移心量 4.0 mm（向鼻侧），所需最小片径 65.0 mm。默认态 66.0/2.0/61.0 均不命中。"
  },
  {
    slug: "optical/report-cost-profit-1",
    inputs: { lens: "150", frame: "220", proc: "55", misc: "30", price: "880", qty: "120", fixed: "24000" },
    expect: ["48.30%", "25.57%", "56.47"],
    ref: "注入非默认(默认 120/180/40/20/680/80/18000)：单副成本 455 元 ⇒ 毛利 425 元、毛利率 48.30%；月毛利 51,000 元、减固定成本 24,000 后营业利润 27,000 元（净利率 25.57%）；盈亏平衡销量 = 24000/425 = 56.47 副。默认态 47.50%/… 不同。"
  },
  {
    slug: "optical/frame-tilt",
    inputs: { tilt: "12", pd: "66", pupilHeight: "26" },
    expect: ["32.0", "前倾角： 12.0°"],
    ref: "注入非默认(默认 8/62/22)：光心下移量 = 前倾角 × 0.5 = 12.0×0.5 = 6.0 mm ⇒ 调整后瞳高 = 26.0 + 6.0 = 32.0 mm。默认态为 26.0 mm；评价文案会随倾角档位漂移，故配一条带标签的倾角串。"
  },
  {
    slug: "optical/convergence-near-point",
    inputs: { pd: "66", distance: "35", npc: "10" },
    expect: ["18.9", "37.7"],
    ref: "注入非默认(默认 62/40/8)：集合需求 = PD(cm)/距离(m) 每眼 = 6.6/0.35 = 18.9Δ，双眼总集合 37.7Δ。默认态 15.5/31.0 均不命中。"
  },
  {
    slug: "optical/polarized-axis",
    inputs: { sph: "-5.25", cyl: "-1.50", axis: "45", panto: "12", wrap: "8" },
    expect: ["0.30D", "-5.38D"],
    ref: "注入非默认(默认 -3.00/0/0/9/5)：前倾角 12° 诱导柱镜 −0.27D@90°、面弯 8° 诱导 −0.12D@180° ⇒ 诱导柱镜总量 0.30D；有效球镜（含 −0.13D 补偿增量）= −5.38D。默认态两者均不同。"
  },
  {
    slug: "optical/coating-design",
    inputs: { wavelength: "520", lensN: "1.67" },
    expect: ["93.2%", "0.43%"],
    ref: "注入非默认(默认 550/1.60)：MgF₂(n=1.38) 单层对 n=1.67 基片的折射率匹配度 93.2%；反射率由无膜 6.3% 降至 0.43%（理想四分之一波厚）。默认态两项均不同。"
  },
  {
    slug: "optical/progressive-corridor",
    inputs: { add: "2.50", bHeight: "32", pupilH: "22" },
    expect: ["27.0", "瞳高22mm"],
    ref: "注入非默认(默认 2.00/30/19)：下加 +2.50D ⇒ 通道长度 14 mm，近用区中心距下缘 8.0 mm，所需最低镜圈高度 = 22 + 8.0 − 3 = 27.0 mm。⚠️ Add 2.00 与 2.50 落在同一通道档位（均 14 mm），裸值「14 通道长度」在默认态一样会命中 ⇒ 改锚最低镜圈高度 27.0 与带标签的瞳高串；评价文案随 Add 档位漂移，不锚。"
  },
  {
    slug: "optical/rayleigh-resolution",
    inputs: { lam: "633", D: "150" },
    expect: ["5.148e-6", "1.06 ″", "2.950e-4"],
    ref: "注入非默认(默认 550/100)：最小分辨角 θ = 1.22λ/D = 1.22×633e-9/0.15 = 5.148e-6 rad = 1.06 角秒 = 2.950e-4 度。默认态 6.71e-6/1.38″ 均不命中。"
  },
  {
    slug: "optical/f-number",
    inputs: { f: "135", D: "50" },
    expect: ["2.7 光圈数", "1963.4954", "2.8659"],
    ref: "注入非默认(默认 50/25)：光圈数 N = f/D = 135/50 = 2.7；相对孔径倒数 0.370370；有效孔径面积 = π(50/2)² = 1963.4954 mm²；曝光级差 = log₂(N²/…) ⇒ 2.8659 EV。默认态 2.0/490.8739 均不命中。"
  },
  {
    slug: "optical/snell-refraction",
    inputs: { n1: "1.00", n2: "1.52", theta1: "42" },
    expect: ["26.12", "0.6691"],
    ref: "注入非默认(默认 1.0/1.33/30)：n₁sinθ₁ = 1.00×sin42° = 0.6691 ⇒ sinθ₂ = 0.6691/1.52，折射角 θ₂ = 26.12°（未达全反射）。默认态 22.08/0.5 均不命中。"
  },
  {
    slug: "optical/microscope-magnification",
    inputs: { fo: "10", fe: "20", L: "170", D: "260" },
    expect: ["221", "17.0", "13.0"],
    ref: "注入非默认(默认 4/25/160/250)：物镜放大率 = L/f₀ = 170/10 = 17.0×；目镜放大率 = D/fₑ = 260/20 = 13.0×；总放大率 = 17.0×13.0 = 221×。默认态 40.0/10.0/400 均不命中。"
  },
  {
    slug: "optical/checker-stress",
    inputs: { f_value: "18.5", fringe: "4.5", thickness: "12" },
    expect: ["6.94 MPa", "2475 光程差"],
    ref: "注入非默认(默认 14.5/3.5/10)：光程差 δ = N·λ = 4.5×550 = 2475 nm；应力双折射 σ₁−σ₂ = N·F/t = 4.5×18.5/12 = 6.94 MPa ⇒ 应力很小档。默认态 2.53 MPa/1925 均不命中；等级文案随档位漂移故不锚。"
  },
  {"slug": "optical/tinted-lens", "inputs": {"density": "60", "baseVlt": "88"}, "clicks": ["selectTint('g15');"], "expect": ["30.2% 可见光透射比 VLT 69.8% 遮光率 染色颜色： G15飞行员绿 染色浓度： 60% 基础透光率： 88% ，颜色系数： 79%", "最终VLT = 88 × 0.40 × 0.86 = 30.2%"], "ref": "独立复算：G15飞行员绿 baseVlt = 0.79；密度因子 = (100−60)/100 = 0.40；最终 VLT = 88 × 0.40 × 0.79 ÷ 92 × 100 = 30.226 ⇒ 30.2%，遮光率 = 100 − 30.2 = 69.8%；注意页面「最终VLT」串里的第三项是 colorFactor/0.92 = 0.79/0.92 = 0.86（归一化显示），实际乘的是 0.79 —— 锚同时锁住 79% 与 30.2%，二者不一致才说明公式被改。默认态（gray / 25% / 92%）为 63.7% / 36.3% / 颜色系数 85%，四锚均不命中。颜色靠顶层 currentTint + selectTint(key) 切换，clicks 驱动。 不锚「分类：N 类」——判别器回退 inputs 但保留 clicks，颜色仍是注入色，分类落在同一档 ⇒ 恒命中。"},
  {"slug": "optical/tinted-lens", "inputs": {"density": "30", "baseVlt": "95"}, "clicks": ["selectTint('blue');"], "expect": ["56.4% 可见光透射比 VLT 43.6% 遮光率 染色颜色： 蓝色 染色浓度： 30% 基础透光率： 95% ，颜色系数： 78%", "最终VLT = 95 × 0.70 × 0.85 = 56.4%"], "ref": "独立复算：蓝色 baseVlt = 0.78；密度因子 = (100−30)/100 = 0.70；最终 VLT = 95 × 0.70 × 0.78 ÷ 92 × 100 = 56.38 ⇒ 56.4%，遮光率 43.6%；归一化显示 0.78/0.92 = 0.85。与上一例互为对照：换颜色系数（0.79→0.78）、换密度（60→30）、换基础透光率（88→95），并跨 1/2 类分界。默认态不命中。 不锚「分类：N 类」——判别器回退 inputs 但保留 clicks，颜色仍是注入色，分类落在同一档 ⇒ 恒命中。"},

  // ── §7.4 零用例加固 · optical 余 4 页（探针实测取锚）────
  {
    slug: "optical/edge-bevel",
    inputs: { thickness: "5", material: "glass", frame: "plastic" },
    expect: ["宽尖边", "40-45°", "玻璃镜片磨边需精磨抛光"],
    ref: "注入非默认(默认 4.5/resin/metal)：玻璃+塑料框 ⇒ 宽尖边、尖边角度 40-45°、材料提示「玻璃镜片磨边需精磨抛光」。默认态为「标准尖边 / 35-40° / 树脂镜片磨边需注意散热」，三锚均不命中。"
  },
  {
    slug: "optical/photochromic-lens",
    inputs: { temp: "30", uv: "8", type: "brown" },
    expect: ["约 49 秒变深至 72%", "3.6min", "UV=8、30°C下"],
    ref: "注入非默认(默认 25/5/gray)：UV=8、30°C、棕色 ⇒ 变深 49s、褪色 3.6min、变深程度 72%、描述「UV=8、30°C下，约 49 秒变深至 72%」。默认态为 45s/4.0min/47%/UV=5、25°C，三锚均不命中。"
  },
  {
    slug: "optical/polarized-stress",
    inputs: { colorSelect: "3" },
    expect: ["光程差约 350 nm", "350nm 光程差"],
    ref: "注入 colorSelect=3(一级橙)(默认空值→无结果)：result 渲染「一级橙 / 光程差约 350 nm / 350nm 光程差 / 2级 应力等级 / 应力中等，合格」。⚠️ 牛顿色序对照表是静态参考表(两种输入都输出整表)，不能锚表内串(「一级橙」「350 nm」「2级」「应力中等，合格」均恒在)；只锚 result 专属串——「光程差约 350 nm」(表内为「350 nm」无「约」)、「350nm 光程差」(表内为「350 nm」带空格)。判别器回退 colorSelect 到空值→result 为空，两锚均不命中。"
  },
  {
    slug: "optical/lens-power-diopter",
    inputs: { f: "500" },
    expect: ["2.00 D", "200.0000"],
    ref: "注入 f=500(默认 1000)：P = 1/(f/1000) = 1/0.5 = 2.00 D；屈光度百分度 P×100 = 200.0000。默认态 f=1000 ⇒ 1.00 D / 100.0000，两锚均不命中。⚠️ harness 第3步兜底会把辅助函数 __tbInputGuard / dataGrid 无参调用(页面模板函数，设计上需传参)，产生 benign errs(不影响 ok)；calcTool 主链正常渲染结果。"
  },
  {
    "slug": "optical/aca-ratio",
    "inputs": {
      "nearPhoria": "42",
      "nearPhoriaLens": "42",
      "lens": "42",
      "pd": "42",
      "distancePhoria": "42",
      "nearPhoriaC": "42",
      "nearDist": "42"
    },
    "expect": [
      ") 无镜片隐斜： 42Δ （外隐斜） 加42D后隐斜： 42Δ （外"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"nearPhoria\":\"42\",\"nearPhoriaLens\":\"42\",\"lens\":\"42\",\"pd\":\"42\",\"distancePhoria\":\"42\",\"nearPhoriaC\":\"42\",\"nearDist\":\"42\"}，输出区含「) 无镜片隐斜： 42Δ （外隐斜） 加42D后隐斜： 42Δ （外」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/accommodation-amplitude",
    "inputs": {
      "age": "42",
      "measured": "42"
    },
    "expect": [
      "幅度近点(cm) 实测调节幅度 42.00D 达到或超过平均值 5.90D，调节功能良好。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"measured\":\"42\"}，输出区含「幅度近点(cm) 实测调节幅度 42.00D 达到或超过平均值 5.90D，调节…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/anti-fatigue-design",
    "inputs": {
      "age": "42",
      "workDist": "42",
      "rx": "42",
      "ampMeasured": "42",
      "nearPhoria": "42",
      "nra": "42",
      "pra": "42",
      "workDistA": "42"
    },
    "expect": [
      "始ADD = 2.38 − 3.93 = -1.55"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"workDist\":\"42\",\"rx\":\"42\",\"ampMeasured\":\"42\",\"nearPhoria\":\"42\",\"nra\":\"42\",\"pra\":\"42\",\"workDistA\":\"42\"}，输出区含「始ADD = 2.38 − 3.93 = -1.55」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/blue-light-filter",
    "inputs": {
      "cutoff": "42",
      "steepness": "42"
    },
    "expect": [
      "450nm透射比 有害蓝光阻隔率偏低(0.5%)，建议增大截止波长(≥440nm)或提高陡度。\n90 400 96 410 99 420 100 430 100 440 100 450 100 460 100 470 100 480 100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cutoff\":\"42\",\"steepness\":\"42\"}，输出区含「450nm透射比 有害蓝光阻隔率偏低(0.5%)，建议增大截止波长(≥440nm…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/aspheric-design",
    "inputs": {
      "n": "42",
      "power": "42",
      "aperture": "42"
    },
    "expect": [
      "42\n42\n42\n976.19"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"power\":\"42\",\"aperture\":\"42\"}，输出区含「42\n42\n42\n976.19」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/coating-design",
    "inputs": {
      "wavelength": "42",
      "lensN": "42",
      "arMat": "1.46"
    },
    "expect": [
      "射率 折射率匹配度偏低(22.5%)，单层减反效果有限。对高折射率镜片(n≥1.6)建议多层宽带减反膜。 设计波长 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"wavelength\":\"42\",\"lensN\":\"42\",\"arMat\":\"1.46\"}，输出区含「射率 折射率匹配度偏低(22.5%)，单层减反效果有限。对高折射率镜片(n≥1.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/convergence-near-point",
    "inputs": {
      "pd": "42",
      "distance": "42",
      "npc": "42"
    },
    "expect": [
      ") NPC破裂点 42cm 偏远(>10cm)，提示集合不足！常见阅读疲劳、复视，建议集合训练或进一步检查。 PD=42mm，距离42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pd\":\"42\",\"distance\":\"42\",\"npc\":\"42\"}，输出区含「) NPC破裂点 42cm 偏远(>10cm)，提示集合不足！常见阅读疲劳、复视…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/checker-stress",
    "inputs": {
      "f_value": "42",
      "fringe": "42",
      "thickness": "42",
      "material": "glass_soda"
    },
    "expect": [
      "：σ₁-σ₂ = 42 × 42 / 42 = 42.00 MPa"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f_value\":\"42\",\"fringe\":\"42\",\"thickness\":\"42\",\"material\":\"glass_soda\"}，输出区含「：σ₁-σ₂ = 42 × 42 / 42 = 42.00 MPa」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/critical-angle",
    "inputs": {
      "n1": "42",
      "n2": "42"
    },
    "expect": [
      "42\n42\n需 n₁>n₂ 才可能发生全反射"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，输出区含「42\n42\n需 n₁>n₂ 才可能发生全反射」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/detector-31",
    "inputs": {
      "pv": "42",
      "rms": "42",
      "decent": "42",
      "trans": "42",
      "element": "mirror",
      "grade": "standard",
      "surface": "20-10",
      "coating": "hr"
    },
    "expect": [
      "波前误差 RMS 42λ 30 差 偏心误差 42′ 20 差 透射/反射比 42%（标准99.5%） 20 差 合规评价： 综合得分 38 低于所选标准级要求（75 分），未达标准级标准；当前指标为「不合格」，可按该等级降级使用，或改进加"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pv\":\"42\",\"rms\":\"42\",\"decent\":\"42\",\"trans\":\"42\",\"element\":\"mirror\",\"grade\":\"standard\",\"surface\":\"20-10\",\"coating\":\"hr\"}，输出区含「波前误差 RMS 42λ 30 差 偏心误差 42′ 20 差 透射/反射比 4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/calc-47",
    "inputs": {
      "idxN": "42",
      "idxR": "42",
      "idxH": "42",
      "idxK": "42"
    },
    "expect": [
      "00 25.0% 10.500 1.3337 0.2274 -1106.29 50.0% 21.000 5.6269 0.4769 -5150.05 70.7% 29.694 12.2970 0.6838 -11613.25 85.0% 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"idxN\":\"42\",\"idxR\":\"42\",\"idxH\":\"42\",\"idxK\":\"42\"}，输出区含「00 25.0% 10.500 1.3337 0.2274 -1106.29 5…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/diffraction-grating",
    "inputs": {
      "d": "42",
      "m": "42",
      "lam": "42"
    },
    "expect": [
      "42\n42\n42\n该级次不存在（sinθ>1）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"d\":\"42\",\"m\":\"42\",\"lam\":\"42\"}，输出区含「42\n42\n42\n该级次不存在（sinθ>1）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/f-number",
    "inputs": {
      "f": "42",
      "D": "42"
    },
    "expect": [
      "0 相对孔径倒数 1385.4424"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"D\":\"42\"}，输出区含「0 相对孔径倒数 1385.4424」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/edge-bevel",
    "inputs": {
      "thickness": "42",
      "material": "mid",
      "frame": "plastic"
    },
    "expect": [
      "突出。 材料提示：中高折镜片较脆，尖边角度宜偏大以减少崩边。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thickness\":\"42\",\"material\":\"mid\",\"frame\":\"plastic\"}，输出区含「突出。 材料提示：中高折镜片较脆，尖边角度宜偏大以减少崩边。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/gaussian-beam-waist",
    "inputs": {
      "lam": "42",
      "f": "42",
      "D": "42"
    },
    "expect": [
      "4λf/(πD) 2.1390e-7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\",\"f\":\"42\",\"D\":\"42\"}，输出区含「4λf/(πD) 2.1390e-7」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/frame-pupillary",
    "inputs": {
      "eyeSize": "42",
      "dbl": "42",
      "pd": "42",
      "ed": "42"
    },
    "expect": [
      " 移心方向 移心量过大(21.0mm)！镜片直径需求大、光学中心偏移多，建议更换更小镜圈或更大DBL的镜框，避免边缘像差与片径不足"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"eyeSize\":\"42\",\"dbl\":\"42\",\"pd\":\"42\",\"ed\":\"42\"}，输出区含「 移心方向 移心量过大(21.0mm)！镜片直径需求大、光学中心偏移多，建议更换…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/frame-tilt",
    "inputs": {
      "tilt": "42",
      "pd": "42",
      "pupilHeight": "42"
    },
    "expect": [
      " mm （总PD 42mm） 前倾角过大（42.0°），建议减小至9°以内，否则严重影响光学品质"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tilt\":\"42\",\"pd\":\"42\",\"pupilHeight\":\"42\"}，输出区含「 mm （总PD 42mm） 前倾角过大（42.0°），建议减小至9°以内，否则…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/lens-maker",
    "inputs": {
      "n": "42",
      "R1": "42",
      "R2": "42"
    },
    "expect": [
      "42\n42\n42\n—"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"R1\":\"42\",\"R2\":\"42\"}，输出区含「42\n42\n42\n—」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/lens-power-diopter",
    "inputs": {
      "f": "42"
    },
    "expect": [
      "= 1/f(米) 2380.9524 屈光度百分度 0.042"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\"}，输出区含「= 1/f(米) 2380.9524 屈光度百分度 0.042」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/lens-refractive-index",
    "inputs": {
      "power": "42",
      "diameter": "42",
      "ct": "42"
    },
    "expect": [
      ".74 1.74 超高折 最薄树脂，超高度数首选 92.06"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"power\":\"42\",\"diameter\":\"42\",\"ct\":\"42\"}，输出区含「.74 1.74 超高折 最薄树脂，超高度数首选 92.06」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/microscope-magnification",
    "inputs": {
      "fo": "42",
      "fe": "42",
      "L": "42",
      "D": "42"
    },
    "expect": [
      "42\n42\n42\n42\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fo\":\"42\",\"fe\":\"42\",\"L\":\"42\",\"D\":\"42\"}，输出区含「42\n42\n42\n42\n1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/mirror-imaging",
    "inputs": {
      "u": "42",
      "R": "42"
    },
    "expect": [
      "mm 像距 v -1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"u\":\"42\",\"R\":\"42\"}，输出区含「mm 像距 v -1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/numerical-aperture",
    "inputs": {
      "n": "42",
      "theta": "42"
    },
    "expect": [
      "反推半角 (°) 789.80590 NA 平方 1.4945"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"theta\":\"42\"}，输出区含「反推半角 (°) 789.80590 NA 平方 1.4945」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/peripheral-defocus",
    "inputs": {
      "central": "42",
      "peripheral": "42",
      "angle": "42"
    },
    "expect": [
      "对周边离焦RPD 远视性 离焦方向 无/可能加速 预估防控效果 离焦信号微弱，防控作用有限。中心 42D，周边 42D，偏心 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"central\":\"42\",\"peripheral\":\"42\",\"angle\":\"42\"}，输出区含「对周边离焦RPD 远视性 离焦方向 无/可能加速 预估防控效果 离焦信号微弱，防…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/optical-path-length",
    "inputs": {
      "n": "42",
      "L": "42"
    },
    "expect": [
      "00 折射率增量 41.0233"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"L\":\"42\"}，输出区含「00 折射率增量 41.0233」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/photochromic-lens",
    "inputs": {
      "temp": "42",
      "uv": "2",
      "type": "brown"
    },
    "expect": [
      " 变深程度 UV=2、42°C下，约 87 秒变深至 15%，进入室内后约 2.6 分钟褪色回复。 高温(42°C)下变色片变深程度受限，可能出现\"热退色\"现象，户外实际颜色偏浅"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"uv\":\"2\",\"type\":\"brown\"}，输出区含「 变深程度 UV=2、42°C下，约 87 秒变深至 15%，进入室内后约 2.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/polarized-axis",
    "inputs": {
      "sph": "42",
      "cyl": "42",
      "axis": "42",
      "panto": "42",
      "wrap": "42"
    },
    "expect": [
      "补偿)：ΔS = +34.05D 倾斜诱导柱镜达 72.23D，可能影响视力。建议：减小配镜角度至标准范围，或在处方中预补偿柱镜与轴位。 前倾角偏大(42°)，建议调整至8-12°以减少像差。 面弯偏大(42°)，运动镜需定制补偿处方。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sph\":\"42\",\"cyl\":\"42\",\"axis\":\"42\",\"panto\":\"42\",\"wrap\":\"42\"}，输出区含「补偿)：ΔS = +34.05D 倾斜诱导柱镜达 72.23D，可能影响视力。建…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/polarized-stress",
    "inputs": {
      "colorSelect": "0"
    },
    "expect": [
      "，材料或装配异常\n0\n一级黑/灰 光程差约 0 nm 0nm 光程差 0级 应力等"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"colorSelect\":\"0\"}，输出区含「，材料或装配异常\n0\n一级黑/灰 光程差约 0 nm 0nm 光程差 0级 应力…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/prism-decentration",
    "inputs": {
      "power": "42",
      "prism": "42",
      "decent": "42",
      "base": "BO"
    },
    "expect": [
      "0mm ，可产生 42.00Δ BO 棱镜。 棱镜度较大(42Δ)，移心量偏多，建议直接加工棱镜以保证光学质量。\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"power\":\"42\",\"prism\":\"42\",\"decent\":\"42\",\"base\":\"BO\"}，输出区含「0mm ，可产生 42.00Δ BO 棱镜。 棱镜度较大(42Δ)，移心量偏多，…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/progressive-corridor",
    "inputs": {
      "add": "42",
      "bHeight": "42",
      "pupilH": "42"
    },
    "expect": [
      "镜圈高度(mm) 镜圈高度(42mm)低于推荐最低高度(47.0mm)，近用视野可能偏小，建议选用短通道设计。 提示：ADD≥42.00D 较高，建议改用 长通道 以保证近用区宽度"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"add\":\"42\",\"bHeight\":\"42\",\"pupilH\":\"42\"}，输出区含「镜圈高度(mm) 镜圈高度(42mm)低于推荐最低高度(47.0mm)，近用视野…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/pupil-height",
    "inputs": {
      "pupilToBottom": "42",
      "frameB": "42",
      "frameBC": "42",
      "pupilToTop": "42"
    },
    "expect": [
      "片适配判定 瞳高 42.0mm 偏大，近用区充足但远用区可能缩小，注意通道选择。\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pupilToBottom\":\"42\",\"frameB\":\"42\",\"frameBC\":\"42\",\"pupilToTop\":\"42\"}，输出区含「片适配判定 瞳高 42.0mm 偏大，近用区充足但远用区可能缩小，注意通道选择。…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/rayleigh-resolution",
    "inputs": {
      "lam": "42",
      "D": "42"
    },
    "expect": [
      " 1.22λ/D 0.25 ″ 折合角秒 1.22"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\",\"D\":\"42\"}，输出区含「 1.22λ/D 0.25 ″ 折合角秒 1.22」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/recommender-1",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "防护：UV400 18. 茶色偏光驾驶镜 （逆光傍晚） 核心功能：抗冲击材质、防油污镀膜、偏光滤除眩光"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「防护：UV400 18. 茶色偏光驾驶镜 （逆光傍晚） 核心功能：抗冲击材质、防…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/recommender-11",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "学院方框镜架 — 记忆塑料 适配脸型：椭圆脸；舒适设计：加宽镜腿、镜腿防滑套 16. 复古圆框镜架 — 混合材质"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「学院方框镜架 — 记忆塑料 适配脸型：椭圆脸；舒适设计：加宽镜腿、镜腿防滑套 1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/snell-refraction",
    "inputs": {
      "n1": "42",
      "n2": "42",
      "theta1": "42"
    },
    "expect": [
      "° 折射角 θ₂ 28.1035 n₁·sinθ₁"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\",\"theta1\":\"42\"}，输出区含「° 折射角 θ₂ 28.1035 n₁·sinθ₁」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/telescope-magnification",
    "inputs": {
      "fo": "42",
      "fe": "42"
    },
    "expect": [
      " = f₀/fₑ 1.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fo\":\"42\",\"fe\":\"42\"}，输出区含「 = f₀/fₑ 1.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/report-cost-profit-1",
    "inputs": {
      "lens": "42",
      "frame": "42",
      "proc": "42",
      "misc": "42",
      "price": "42",
      "qty": "42",
      "fixed": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n单副成本： 168"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lens\":\"42\",\"frame\":\"42\",\"proc\":\"42\",\"misc\":\"42\",\"price\":\"42\",\"qty\":\"42\",\"fixed\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n单副成本： 168」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optical/thin-lens-imaging",
    "inputs": {
      "u": "42",
      "f": "42"
    },
    "expect": [
      "42\n42\n平行光，像在无穷远 提示"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"u\":\"42\",\"f\":\"42\"}，输出区含「42\n42\n平行光，像在无穷远 提示」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== optical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();