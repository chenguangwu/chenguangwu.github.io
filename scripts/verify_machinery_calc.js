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
  {"slug": "machinery/stretch", "inputs": {"wireDia": "2.5", "coilDia": "10", "activeCoils": "12", "freeLen": "55"}, "clicks": ["document.getElementById('springMat').value='304';calc();"], "expect": ["4.000 弹簧指数 C 1.404 Wahl系数 Kw 12.500 外径 D₂ (mm) 7.500 内径 D₁ (mm)", "29.704 弹簧刚度 k (N/mm) 480.820 最大载荷 Fmax (N) 16.187 最大变形 δmax (mm)", "⛔ 长径比 5.500 > 4，压缩弹簧易发生屈曲失稳，建议加导向杆或减小自由长度。"], "ref": "独立复算（304 不锈钢 G=73 GPa、τ=440 MPa）：C = 10/2.5 = 4.000；Kw = 15/12 + 0.15375 = 1.40375 ⇒ 1.404；D₂ = 12.5、D₁ = 7.5；k = 73000×39.0625/(8×1000×12) = 2,851,562.5/96,000 = 29.704 N/mm；Fmax = 440×π×15.625/(8×1.40375×4) = 21,598.9/44.92 = 480.82 N；δmax = 480.820/29.704 = 16.187 mm；长径比 L₀/D = 55/10 = 5.5 > 4 ⇒ 触发屈曲警告。与上一例互为对照：换材料（G 79→73、τ 560→440，k 36.178→29.704、Fmax 1534→481 全部随之变）、换规格、并跨「长径比 ≤4 安全 / >4 屈曲」两分支。材料切换走 clicks（select 桩无 option selected）；仅锚随 inputs+G 变化的 k/Fmax/δmax，不锚 C 相关的静态推荐区间串。默认态不命中。"}
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