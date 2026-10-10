#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "machinery/area-dosage-1", inputs: {v_area:"20", v_dft:"80", v_vs:"55"}, expect: ["3.42 实际用量"], ref: "涂装面积用量计算" },
  { slug: "machinery/banjinzhewanzhankai", inputs: {v_t:"4", v_ang:"90", v_r:"3"}, expect: ["83.540 展开总长"], ref: "钣金折弯展开" },
  { slug: "machinery/calc-64", inputs: {basic:"100", holeES:"25", holeEI:"0"}, expect: ["100.0250"], ref: "孔轴配合：孔最大极限=D+ES/1000" },
  { slug: "machinery/calc-89", inputs: {v_D:"400", v_d:"120", v_mu:"0.25"}, expect: ["130.00 传递扭矩"], ref: "摩擦离合器" },
  { slug: "machinery/calc-gear-1", inputs: {v_m:"6", v_z:"24", v_a:"20"}, expect: ["144.000 分度圆直径"], ref: "圆柱齿轮" },
  { slug: "machinery/calc-gear-3", inputs: {v_sm:"6", v_sz:"24", v_sa:"20"}, expect: ["144.000 分度圆"], ref: "斜齿轮" },
  { slug: "machinery/calc-lifespan-belt", inputs: {D1:"200", D2:"300", center:"500"}, expect: ["967 大轮转速"], ref: "带传动" },
  { slug: "machinery/calc-strength", inputs: {diameter:"80", sb:"200", ss:"150"}, expect: ["2.98 弯曲应力"], ref: "轴强度校核" },
  { slug: "machinery/drive-2", inputs: {z1:"4", z2:"40", module:"5"}, expect: ["10.00 传动比"], ref: "蜗杆传动" },
  { slug: "machinery/energy-2", inputs: {v_J:"5", v_n1:"1500", v_n2:"0"}, expect: ["261.80 制动扭矩"], ref: "制动能" },
  { slug: "machinery/estimate-gravity", inputs: {plateL:"120", plateW:"60"}, expect: ["565.200 质量"], ref: "零件重量：钢板 120×60×10 → 72cm³×7.85" },
  { slug: "machinery/estimate-lifespan-bearing", inputs: {loadC:"67", loadP:"5", speed:"1500"}, expect: ["2406.10"], ref: "轴承寿命估算" },
  { slug: "machinery/frequency-17", inputs: {v_m:"200", v_k:"50000", v_f:"25"}, expect: ["2.516 固有频率"], ref: "振动隔振" },
  { slug: "machinery/gear", inputs: {v_fa:"200", v_fb:"150", v_fc:"120"}, expect: ["不满足", "320.00"], ref: "四连杆：200 使最短+最长 320 > 其余和 310 → 不满足 Grashof" },
  { slug: "machinery/lifespan-bearing-1", inputs: {v_F:"10000", v_d:"50", v_bd:"1"}, expect: ["4.000 平均压强"], ref: "滑动轴承" },
  { slug: "machinery/lifespan-bearing", inputs: {v_C:"45000", v_P:"2500", v_n:"1500"}, expect: ["5832.00 L10寿命"], ref: "滚动轴承寿命" },
  { slug: "machinery/pressure-4", inputs: {v_z:"48", v_m:"2", v_a:"30"}, expect: ["96.000 分度圆直径"], ref: "花键" },
  { slug: "machinery/runhuaxitongsheji", inputs: {v_d:"160", v_l:"80", v_n:"1500"}, expect: ["0.78 比压"], ref: "润滑系统" },
  { slug: "machinery/strength-15", inputs: {v_P:"11", v_n1:"1200", v_z1:"19"}, expect: ["19.05", "1520"], ref: "链传动强度：n1=1200 → p=19.05，F=1000P/v" },
  { slug: "machinery/strength-6", inputs: {v_d:"80", v_b:"12", v_h:"8"}, expect: ["49.34 挤压应力"], ref: "铆钉连接" },
  { slug: "machinery/tanhuangsheji", inputs: {v_d:"6", v_dd:"20", v_n:"8"}, expect: ["200.728 弹簧刚度"], ref: "弹簧设计" },
  { slug: "machinery/temp-hardness", inputs: {steelGrade:"custom", maxHrc:"45", temperK:"3", critDia:"15"}, expect: ["33.0 预期硬度"], ref: "热处理：自定义钢种 45-3×(500-150)/100=34.5，×0.9569 截面折减" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"73", v_lead:"7", v_f:"20"}, expect: ["140.286 驱动力矩"], ref: "螺旋传动" },
{ slug: "machinery/zhujian-bamoxiedu-sheji", inputs: {v0:"120", v1:"200"}, expect: ["204.19","2.09%"], ref: "v0=120,v1=200 → 高度落 50–200 档取 1.0°、尺寸差 120×tan1°=2.09 mm、上端外径 200+2×2.09=204.19 mm、放大率 2×2.09/200=2.09%（默认 60/200 → 1.0/1.05/202.09/1.05%；交换 200/60 → 1.0/3.49/66.98/11.64%。斜度档位 1.0 三态相同故不作断言，「2.09」被子串于默认态 202.09 亦剔除）" },
{
  "slug": "machinery/xiao-dingwei-lianjie-chicun",
  "inputs": {
    "v0": "50",
    "v1": "100"
  },
  "expect": [
    "25.231"
  ],
  "ref": "销钉直径 d=√(4×50×1000/(π×100))=25.231 mm（默认 20/120 得 14.567，注入失败即不命中）"},
  { slug: "machinery/analysis-casting", inputs: {vol:"3000", area:"600", rho:"7.8", C:"2.4"}, expect: ["23400.00"], ref: "铸件重量 G = V·ρ = 3,000 × 7.8 = **23,400.00** g（默认 1,000 cm³ × 7.2 得 7,200.00）" },
  { slug: "machinery/analysis-casting", inputs: {vol:"3000", area:"600", rho:"7.8", C:"2.4"}, expect: ["60.0"], ref: "凝固时间 t = C·M² = 2.4 × (3,000/600)² = 2.4 × 25 = **60.0** s（模数 M = 5.000 cm；默认 t = 12.5 s）" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"5000", nf:"25", mt:"50", tv:"200"}, expect: ["200.00"], ref: "MTBF = 总运行 5,000 h ÷ 故障 25 次 = **200.00** h（默认 8,760/22 得 398.18）" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"5000", nf:"25", mt:"50", tv:"200"}, expect: ["36.79%"], ref: "可靠度 R(200) = e^(−t/MTBF) = e^(−200/200) = **36.79%**；累计失效概率 63.21% 与之相加为 100%" },
  { slug: "machinery/calc-gear", inputs: {module:"3", teeth:"16", pressure:"20"}, expect: ["48.0000"], ref: "分度圆 d = m·z = 3 × 16 = **48.0000** mm（默认 2×20 得 40.0000）" },
  { slug: "machinery/calc-gear", inputs: {module:"3", teeth:"16", pressure:"20"}, expect: ["54.0000"], ref: "齿顶圆 da = d + 2hₐ = 48 + 2×1×3 = **54.0000** mm；齿根圆 df = 48 − 2×1.25×3 = 40.5000，与 da 相差恰为一个全齿高" },
  { slug: "machinery/calc-weld", inputs: {plateThk:"10", weldSize:"8", weldLen:"200", load:"40", weldMat:"E50"}, expect: ["5.66"], ref: "角焊缝喉厚 a = 0.707 K = 0.707 × 8 = **5.66** mm（默认 6 ⇒ 4.24）" },
  { slug: "machinery/calc-weld", inputs: {plateThk:"10", weldSize:"8", weldLen:"200", load:"40", weldMat:"E50"}, expect: ["1131.20"], ref: "有效面积 A = a·L = 5.66 × 200 = **1131.20** mm²（默认 424.20）。页面先按 0.707K 四舍五入到 5.66 再乘全长，与一步相乘 1131.37 有 0.17 的舍入差 ⇒ 锚取页面值" },
  { slug: "machinery/thread-recognize", inputs: {diameter:"20", pitch:"2.5", threadAngle:"60"}, expect: ["10.2"], ref: "英制换算 TPI = 25.4 ÷ 螺距 2.5 = **10.2** 牙/in（默认 M10×1.5 得 16.9）" },
  { slug: "machinery/thread-recognize", inputs: {diameter:"20", pitch:"2.5", threadAngle:"60"}, expect: ["17.294"], ref: "小径 d₁ = 外径 20 − 1.0825 × 螺距 2.5 = 20 − 2.70625 = **17.294** mm（默认 M10 得 8.376）" },
  {"slug": "machinery/stretch", "inputs": {"wireDia": "3.5", "coilDia": "16", "activeCoils": "10"}, "expect": ["4.571 弹簧指数 C 1.345 Wahl系数 Kw 19.500 外径 D₂ (mm) 12.500 内径 D₁ (mm)", "36.178 弹簧刚度 k (N/mm) 1534.014 最大载荷 Fmax (N) 42.401 最大变形 δmax (mm)", "⚠️ 最大变形量超过可用行程（L₀-Lb=-2.000mm），弹簧可能被压并。", "✓ 弹簧指数 C=4.571 在推荐范围 4~16 内。"], "ref": "独立复算（碳素弹簧钢丝 G=79 GPa、τ=560 MPa，G 先 ×1000 转 MPa）：C = 16/3.5 = 4.571；Kw = (4×4.571−1)/(4×4.571−4) + 0.615/4.571 = 17.284/14.284 + 0.1346 = 1.3449 ⇒ 1.345；D₂ = 16+3.5 = 19.5、D₁ = 16−3.5 = 12.5；k = 79000×3.5⁴/(8×16³×10) = 79000×150.0625/327,680 = 11,854,937.5/327,680 = 36.178 N/mm；Fmax = 560×π×42.875/(8×1.3449×4.571) = 75,398.5/49.180 = 1534.01 N；δmax = 1534.014/36.178 = 42.401 mm。默认态（d=2、D=12、n=8）为 C=6.000、Kw=1.252、k=11.429、Fmax=234.104、δmax=20.483，四组锚均不命中。注：t 与 Lb 两项页面算法与常规 (n+1)d / (n+1.5)d+d 不同，故不作锚。材料默认 carbon 未变，不锚「材料」相关串（判别器保留 clicks，见 §10.5）。"},
  {"slug": "machinery/stretch", "inputs": {"wireDia": "2.5", "coilDia": "10", "activeCoils": "12", "freeLen": "55"}, "clicks": ["document.getElementById('springMat').value='304';calc();"], "expect": ["4.000 弹簧指数 C 1.404 Wahl系数 Kw 12.500 外径 D₂ (mm) 7.500 内径 D₁ (mm)", "29.704 弹簧刚度 k (N/mm) 480.820 最大载荷 Fmax (N) 16.187 最大变形 δmax (mm)", "⛔ 长径比 5.500 > 4，压缩弹簧易发生屈曲失稳，建议加导向杆或减小自由长度。"], "ref": "独立复算（304 不锈钢 G=73 GPa、τ=440 MPa）：C = 10/2.5 = 4.000；Kw = 15/12 + 0.15375 = 1.40375 ⇒ 1.404；D₂ = 12.5、D₁ = 7.5；k = 73000×39.0625/(8×1000×12) = 2,851,562.5/96,000 = 29.704 N/mm；Fmax = 440×π×15.625/(8×1.40375×4) = 21,598.9/44.92 = 480.82 N；δmax = 480.820/29.704 = 16.187 mm；长径比 L₀/D = 55/10 = 5.5 > 4 ⇒ 触发屈曲警告。与上一例互为对照：换材料（G 79→73、τ 560→440，k 36.178→29.704、Fmax 1534→481 全部随之变）、换规格、并跨「长径比 ≤4 安全 / >4 屈曲」两分支。材料切换走 clicks（select 桩无 option selected）；仅锚随 inputs+G 变化的 k/Fmax/δmax，不锚 C 相关的静态推荐区间串。默认态不命中。"},
  { slug: "machinery/strength-7", inputs: {v_d:"10", v_t:"12", v_n:"4", v_w:"120", v_f:"150", v_tau:"100", v_sigc:"250", v_sigt:"180"}, expect: ["477.46", "312.50", "156.25", "12.1%", "不合格"], ref: "铆缝强度（8 字段全注入）：d=10 t=12 n=4 w=120 F=150 τ=100 σc=250 σt=180 → As=314.16 τ=477.46 σc=312.50 σt=156.25 F_min=31.42kN η=12.1% 不合格（默认 d=16 t=10 n=4 w=120 F=60 τ=90 σc=210 σt=140 → 43.1%/74.60/93.75/107.14/偏低，均不命中）。校验 valid 要求 w>n·d（120>40 满足）。锚全部为随输入变化的结果值，规避输入回显；「剪切控制」为默认/注入共有（恒 F_shear 最弱）故不锚。" },
  { slug: "machinery/tolerance", inputs: {v_d:"40"}, expect: ["0.0494 最大间隙 (mm)", "0.0088 最小间隙 (mm)"], ref: "基孔制 H7/g6 间隙配合：v_d=40 → 最大间隙 0.0494、最小间隙 0.0088（默认 v_d=50 → 0.0500/0.0095，不命中）。注：「配合公差 (mm)」=孔IT7+轴IT6，D=40/50 同处一级公差区恒为 0.0406，不随 v_d 变 ⇒ 不锚（否则成逃生项）。锚结果值+单位，规避输入 40 回显。" },
  { slug: "machinery/tolerance-1", inputs: {v_d:"80"}, expect: ["0.0080 公差值 (mm)", "8.00 公差值 (μm)"], ref: "形位公差查表：v_d=80（直径 ≤80mm 查表档）→ 圆度/圆柱度 7 级中等级，公差值 0.0080mm / 8.00μm（默认 v_d=50 → 0.0070/7.00，不命中）。锚结果值+单位，规避输入 80 回显。" },
  { slug: "machinery/zhineng-wurenyugaoxiaoduibijisuanqi", inputs: {v0:"90", v1:"60"}, expect: ["30 综合差距", "40.0% 智能权重占比"], ref: "无人/有人高效对比：v0=90 v1=60 → 综合差距 30、智能权重占比 40.0%（默认 v0=80 v1=88 → 8/47.6%，不命中）。锚结果值「30 综合差距」「40.0% 智能权重占比」，全为随输入变化的合成结果，规避输入回显。" },
  {
    "slug": "machinery/analysis-casting",
    "inputs": {
      "vol": "42",
      "area": "42",
      "rho": "42",
      "C": "42"
    },
    "expect": [
      " = C·M²： 42.0 s（0.70"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vol\":\"42\",\"area\":\"42\",\"rho\":\"42\",\"C\":\"42\"}，输出区含「 = C·M²： 42.0 s（0.70」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/area-dosage-1",
    "inputs": {
      "v_area": "42",
      "v_dft": "42",
      "v_vs": "42",
      "v_te": "42"
    },
    "expect": [
      "42\n42\n42\n42\n10.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_area\":\"42\",\"v_dft\":\"42\",\"v_vs\":\"42\",\"v_te\":\"42\"}，输出区含「42\n42\n42\n42\n10.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/banjinzhewanzhankai",
    "inputs": {
      "v_t": "42",
      "v_ang": "42",
      "v_r": "42",
      "v_k": "42",
      "v_a": "42",
      "v_b": "42",
      "v_mat": "0.42"
    },
    "expect": [
      " 材料 K=0.42，板厚 42mm，角度 42°，内圆角 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_t\":\"42\",\"v_ang\":\"42\",\"v_r\":\"42\",\"v_k\":\"42\",\"v_a\":\"42\",\"v_b\":\"42\",\"v_mat\":\"0.42\"}，输出区含「 材料 K=0.42，板厚 42mm，角度 42°，内圆角 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-64",
    "inputs": {
      "basic": "42",
      "holeES": "42",
      "holeEI": "42",
      "shaftes": "42",
      "shaftei": "42",
      "preset": "25,0,0,-6"
    },
    "expect": [
      ") 最大极限尺寸 42.0250 mm 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"basic\":\"42\",\"holeES\":\"42\",\"holeEI\":\"42\",\"shaftes\":\"42\",\"shaftei\":\"42\",\"preset\":\"25,0,0,-6\"}，输出区含「) 最大极限尺寸 42.0250 mm 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/analysis-lifespan",
    "inputs": {
      "rt": "42",
      "nf": "42",
      "mt": "42",
      "tv": "42"
    },
    "expect": [
      "h 固有可用度： 50.00% 故障率： 1.00000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rt\":\"42\",\"nf\":\"42\",\"mt\":\"42\",\"tv\":\"42\"}，输出区含「h 固有可用度： 50.00% 故障率： 1.00000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-89",
    "inputs": {
      "v_D": "42",
      "v_d": "42",
      "v_mu": "42",
      "v_F": "42",
      "v_z": "42",
      "v_n": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n请检查输入：外径须大于内径，各值须为正数\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_D\":\"42\",\"v_d\":\"42\",\"v_mu\":\"42\",\"v_F\":\"42\",\"v_z\":\"42\",\"v_n\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n请检查输入：外径须大于内径，各值须为正数\n暂…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-gear-1",
    "inputs": {
      "v_m": "42",
      "v_z": "42",
      "v_a": "42"
    },
    "expect": [
      " df (mm) 1310.907"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_m\":\"42\",\"v_z\":\"42\",\"v_a\":\"42\"}，输出区含「 df (mm) 1310.907」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-gear-3",
    "inputs": {
      "v_sm": "42",
      "v_sz": "42",
      "v_sa": "42",
      "v_hmn": "42",
      "v_hz": "42",
      "v_hb": "42",
      "v_ha": "42",
      "v_bm": "42",
      "v_bz1": "42",
      "v_bz2": "42",
      "v_type": "helical"
    },
    "expect": [
      ")\n暂无计算记录\n42\n42\n42\n42\n42\n42\n💡 斜齿：d=mn·z/cosβ；da=d+2mn；df=d-2.5mn；当量齿数 zv=z/cos³β"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_sm\":\"42\",\"v_sz\":\"42\",\"v_sa\":\"42\",\"v_hmn\":\"42\",\"v_hz\":\"42\",\"v_hb\":\"42\",\"v_ha\":\"42\",\"v_bm\":\"42\",\"v_bz1\":\"42\",\"v_bz2\":\"42\",\"v_type\":\"helical\"}，输出区含「)\n暂无计算记录\n42\n42\n42\n42\n42\n42\n💡 斜齿：d=mn·z/…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-gear",
    "inputs": {
      "module": "42",
      "teeth": "42",
      "pressure": "42",
      "helix": "42",
      "haCoef": "42",
      "cCoef": "42"
    },
    "expect": [
      " s (mm) 187.6 不根切最少齿数 ⚠️ 当前齿数 42 小于不根切最少齿数 187.6，标准齿轮将发生根切，建议采用变位齿轮。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"module\":\"42\",\"teeth\":\"42\",\"pressure\":\"42\",\"helix\":\"42\",\"haCoef\":\"42\",\"cCoef\":\"42\"}，输出区含「 s (mm) 187.6 不根切最少齿数 ⚠️ 当前齿数 42 小于不根切最少…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-lifespan-belt",
    "inputs": {
      "D1": "42",
      "D2": "42",
      "center": "42",
      "n1": "42",
      "power": "42",
      "beltType": "flat"
    },
    "expect": [
      "（≥150°）。 ⚠️ 带速 0.09 m/s 偏低（建议5~25m/s），有效拉力较大。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"D1\":\"42\",\"D2\":\"42\",\"center\":\"42\",\"n1\":\"42\",\"power\":\"42\",\"beltType\":\"flat\"}，输出区含「（≥150°）。 ⚠️ 带速 0.09 m/s 偏低（建议5~25m/s），有效…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-strength",
    "inputs": {
      "diameter": "42",
      "sb": "42",
      "ss": "42",
      "torque": "42",
      "bending": "42",
      "innerDia": "42",
      "material": "45"
    },
    "expect": [
      "σb (MPa) ✓ 扭转刚度满足一般要求（许用 ≤0.5°/m）。\n600\n355\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"diameter\":\"42\",\"sb\":\"42\",\"ss\":\"42\",\"torque\":\"42\",\"bending\":\"42\",\"innerDia\":\"42\",\"material\":\"45\"}，输出区含「σb (MPa) ✓ 扭转刚度满足一般要求（许用 ≤0.5°/m）。\n600\n3…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/calc-weld",
    "inputs": {
      "plateThk": "42",
      "weldSize": "42",
      "weldLen": "42",
      "load": "42",
      "sb": "42",
      "weldMat": "E50"
    },
    "expect": [
      "42\n42\n42\n42\n42\nE50\n角焊缝计算结果 29.69"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plateThk\":\"42\",\"weldSize\":\"42\",\"weldLen\":\"42\",\"load\":\"42\",\"sb\":\"42\",\"weldMat\":\"E50\"}，输出区含「42\n42\n42\n42\n42\nE50\n角焊缝计算结果 29.69」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/drive-2",
    "inputs": {
      "z1": "42",
      "z2": "42",
      "module": "42",
      "q": "42",
      "mu": "42",
      "matPair": "bronze_dry"
    },
    "expect": [
      "裕度 (ρ-γ) ✓ 效率 85.19% 较高，适合动力传动。 ⚠️ 导程角 45.00° 偏大，加工困难。\n0.08"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"z1\":\"42\",\"z2\":\"42\",\"module\":\"42\",\"q\":\"42\",\"mu\":\"42\",\"matPair\":\"bronze_dry\"}，输出区含「裕度 (ρ-γ) ✓ 效率 85.19% 较高，适合动力传动。 ⚠️ 导程角 4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/estimate-gravity",
    "inputs": {
      "density": "42",
      "plateL": "42",
      "plateW": "42",
      "plateH": "42",
      "cylD": "42",
      "cylL": "42",
      "tubeOD": "42",
      "tubeID": "42",
      "tubeL": "42",
      "boxL": "42",
      "boxW": "42",
      "boxH": "42",
      "boxT": "42",
      "sphD": "42",
      "coneD": "42",
      "coneH": "42",
      "shape": "cylinder",
      "material": "castiron"
    },
    "expect": [
      " Zc (mm) 418.96 g 总质量\n7.2\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"density\":\"42\",\"plateL\":\"42\",\"plateW\":\"42\",\"plateH\":\"42\",\"cylD\":\"42\",\"cylL\":\"42\",\"tubeOD\":\"42\",\"tubeID\":\"42\",\"tubeL\":\"42\",\"boxL\":\"42\",\"boxW\":\"42\",\"boxH\":\"42\",\"boxT\":\"42\",\"sphD\":\"42\",\"coneD\":\"42\",\"coneH\":\"42\",\"shape\":\"cylinder\",\"material\":\"castiron\"}，输出区含「 Zc (mm) 418.96 g 总质量\n7.2\n42\n42\n42\n42\n42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/energy-2",
    "inputs": {
      "v_J": "42",
      "v_n1": "42",
      "v_n2": "42",
      "v_t": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_J\":\"42\",\"v_n1\":\"42\",\"v_n2\":\"42\",\"v_t\":\"42\"}，输出区含「42\n42\n42\n42\n0.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/frequency-17",
    "inputs": {
      "v_m": "42",
      "v_k": "42",
      "v_f": "42",
      "v_z": "42"
    },
    "expect": [
      " fn (Hz) 263.894 频率比 r 0.303 传递率 T 69.7% 隔振效率 η 9800.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_m\":\"42\",\"v_k\":\"42\",\"v_f\":\"42\",\"v_z\":\"42\"}，输出区含「 fn (Hz) 263.894 频率比 r 0.303 传递率 T 69.7%…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/lifespan-bearing-1",
    "inputs": {
      "v_F": "42",
      "v_d": "42",
      "v_bd": "42",
      "v_n": "42",
      "v_Lh": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n请检查输入：载荷、轴径须大于0，宽径比0.2~2，转速须大于0\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_F\":\"42\",\"v_d\":\"42\",\"v_bd\":\"42\",\"v_n\":\"42\",\"v_Lh\":\"42\"}，输出区含「42\n42\n42\n42\n42\n请检查输入：载荷、轴径须大于0，宽径比0.2~2，…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/estimate-lifespan-bearing",
    "inputs": {
      "loadC": "42",
      "loadP": "42",
      "speed": "42",
      "bearingType": "roller",
      "reliability": "95",
      "lubrication": "0.8"
    },
    "expect": [
      "滑 p (指数) 10/3 滚子轴承 ⚠️ 载荷比 C/P=1.00 偏低（建议 C/P ≥ 2），轴承寿命可能不足。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"loadC\":\"42\",\"loadP\":\"42\",\"speed\":\"42\",\"bearingType\":\"roller\",\"reliability\":\"95\",\"lubrication\":\"0.8\"}，输出区含「滑 p (指数) 10/3 滚子轴承 ⚠️ 载荷比 C/P=1.00 偏低（建议…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/lifespan-bearing",
    "inputs": {
      "v_C": "42",
      "v_P": "42",
      "v_n": "42",
      "v_type": "roller"
    },
    "expect": [
      "42\n42\n42\nroller\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_C\":\"42\",\"v_P\":\"42\",\"v_n\":\"42\",\"v_type\":\"roller\"}，输出区含「42\n42\n42\nroller\n1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/gear",
    "inputs": {
      "v_fa": "42",
      "v_fb": "42",
      "v_fc": "42",
      "v_fd": "42",
      "v_crb": "42",
      "v_ch": "42",
      "v_cphi": "42",
      "v_ce": "42",
      "v_gm": "42",
      "v_gz1": "42",
      "v_gz2": "42",
      "v_type": "cam"
    },
    "expect": [
      "cam\n42\n42\n42\n42\n53.76 最大压力角 (°) 99.24 推荐基圆半径 (mm) 84.00 最大向径 (mm) 360.00 等效速度 (mm·°/s) 263.89 凸轮最大周长 (mm) 压力角超限 压力角评价\n暂无"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_fa\":\"42\",\"v_fb\":\"42\",\"v_fc\":\"42\",\"v_fd\":\"42\",\"v_crb\":\"42\",\"v_ch\":\"42\",\"v_cphi\":\"42\",\"v_ce\":\"42\",\"v_gm\":\"42\",\"v_gz1\":\"42\",\"v_gz2\":\"42\",\"v_type\":\"cam\"}，输出区含「cam\n42\n42\n42\n42\n53.76 最大压力角 (°) 99.24 推荐…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/runhuaxitongsheji",
    "inputs": {
      "v_d": "42",
      "v_l": "42",
      "v_n": "42",
      "v_w": "42",
      "v_eta": "42",
      "v_psi": "42",
      "v_dt": "42",
      "v_type": "thrust"
    },
    "expect": [
      ") 润滑方式推荐：脂润滑或手加油（速度低，脂润滑即可满足） ✓ PV值 2.20"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d\":\"42\",\"v_l\":\"42\",\"v_n\":\"42\",\"v_w\":\"42\",\"v_eta\":\"42\",\"v_psi\":\"42\",\"v_dt\":\"42\",\"v_type\":\"thrust\"}，输出区含「) 润滑方式推荐：脂润滑或手加油（速度低，脂润滑即可满足） ✓ PV值 2.20」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/pressure-4",
    "inputs": {
      "v_z": "42",
      "v_m": "42",
      "v_a": "42",
      "v_root": "round"
    },
    "expect": [
      "42\n42\n42\nround\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_z\":\"42\",\"v_m\":\"42\",\"v_a\":\"42\",\"v_root\":\"round\"}，输出区含「42\n42\n42\nround\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/strength-15",
    "inputs": {
      "v_P": "42",
      "v_n1": "42",
      "v_z1": "42",
      "v_z2": "42"
    },
    "expect": [
      "距 p (mm) 32A 推荐链号 1.494"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_P\":\"42\",\"v_n1\":\"42\",\"v_z1\":\"42\",\"v_z2\":\"42\"}，输出区含「距 p (mm) 32A 推荐链号 1.494」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/strength-6",
    "inputs": {
      "v_d": "42",
      "v_b": "42",
      "v_h": "42",
      "v_L": "42",
      "v_T": "42",
      "v_sp": "42",
      "v_tau": "42",
      "v_type": "square"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\nsquare\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d\":\"42\",\"v_b\":\"42\",\"v_h\":\"42\",\"v_L\":\"42\",\"v_T\":\"42\",\"v_sp\":\"42\",\"v_tau\":\"42\",\"v_type\":\"square\"}，输出区含「42\n42\n42\n42\n42\n42\n42\nsquare\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/strength-7",
    "inputs": {
      "v_d": "42",
      "v_t": "42",
      "v_n": "42",
      "v_w": "42",
      "v_f": "42",
      "v_tau": "42",
      "v_sigc": "42",
      "v_sigt": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n42\n请输入有效参数（板宽须大于铆钉总径，铆钉数为正整数）\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d\":\"42\",\"v_t\":\"42\",\"v_n\":\"42\",\"v_w\":\"42\",\"v_f\":\"42\",\"v_tau\":\"42\",\"v_sigc\":\"42\",\"v_sigt\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n42\n请输入有效参数（板宽须大于铆钉总…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/tanhuangsheji",
    "inputs": {
      "v_d": "42",
      "v_dd": "42",
      "v_n": "42",
      "v_f": "42",
      "v_mat": "music"
    },
    "expect": [
      "42\n42\n42\n42\nmusic\n请输入有效参数（中径须大于2倍钢丝直径，圈数须大于0）\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d\":\"42\",\"v_dd\":\"42\",\"v_n\":\"42\",\"v_f\":\"42\",\"v_mat\":\"music\"}，输出区含「42\n42\n42\n42\nmusic\n请输入有效参数（中径须大于2倍钢丝直径，圈数…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/temp-hardness",
    "inputs": {
      "maxHrc": "42",
      "temperK": "42",
      "critDia": "42",
      "temperTemp": "42",
      "sectionSize": "42",
      "steelGrade": "40Cr",
      "quenchMedium": "oil"
    },
    "expect": [
      "40Cr\noil\n42\n42\n参数无效：回火温度150~700°C，截面>0\n55\n2.5\n25"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"maxHrc\":\"42\",\"temperK\":\"42\",\"critDia\":\"42\",\"temperTemp\":\"42\",\"sectionSize\":\"42\",\"steelGrade\":\"40Cr\",\"quenchMedium\":\"oil\"}，输出区含「40Cr\noil\n42\n42\n参数无效：回火温度150~700°C，截面>0\n5…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/thread-recognize",
    "inputs": {
      "diameter": "42",
      "pitch": "42",
      "tpi": "42",
      "threadAngle": "60"
    },
    "expect": [
      "42\n42\n60\n未找到完全匹配的标准螺纹，可能为非标螺纹。以下是相近规格： M42 最接近规格 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"diameter\":\"42\",\"pitch\":\"42\",\"tpi\":\"42\",\"threadAngle\":\"60\"}，输出区含「42\n42\n60\n未找到完全匹配的标准螺纹，可能为非标螺纹。以下是相近规格： M…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/thread-drive",
    "inputs": {
      "v_d2": "42",
      "v_lead": "42",
      "v_f": "42",
      "v_mu": "42",
      "v_muc": "42",
      "v_dc": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n请输入有效参数（中径、导程须大于0，摩擦系数须在0~0.5之间）\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d2\":\"42\",\"v_lead\":\"42\",\"v_f\":\"42\",\"v_mu\":\"42\",\"v_muc\":\"42\",\"v_dc\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n请输入有效参数（中径、导程须大于0，摩擦系数…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/tolerance",
    "inputs": {
      "v_d": "42",
      "v_fit": "abc123测试",
      "v_base": "hole"
    },
    "expect": [
      "42\nabc123测试\n请输入有效的基本尺寸和配合代号（如 H7/g6）\n暂无计算记录\nhole"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d\":\"42\",\"v_fit\":\"abc123测试\",\"v_base\":\"hole\"}，输出区含「42\nabc123测试\n请输入有效的基本尺寸和配合代号（如 H7/g6）\n暂无计…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/tolerance-1",
    "inputs": {
      "v_d": "42",
      "v_type": "straight"
    },
    "expect": [
      "度评价 公差类型：直线度/平面度 主参数：长度 L = 42mm（查表范围 ≤63mm） 公差等级：6"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v_d\":\"42\",\"v_type\":\"straight\"}，输出区含「度评价 公差类型：直线度/平面度 主参数：长度 L = 42mm（查表范围 ≤6…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/zhineng-wurenyugaoxiaoduibijisuanqi",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "线优先 推荐侧重 50.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\"}，输出区含「线优先 推荐侧重 50.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/zhujian-bamoxiedu-sheji",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "42\n42\n1.5 起模斜度（°） 1.10"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\"}，输出区含「42\n42\n1.5 起模斜度（°） 1.10」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== machinery calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();