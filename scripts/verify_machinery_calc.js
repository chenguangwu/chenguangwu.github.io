#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
const path = require("path");

// 911 复核重做：停止输出无依据的「精度保持寿命(h)/年数/等级」定量结论。
// 精度/润滑因子仅作相对比较系数，不派生寿命数值、等级与参考标尺；
// 保留 ISO 281 的 L10 疲劳寿命与明确标注为相对比较的折算系数。
function lifespan20ScopeChecks() {
  const src = fs.readFileSync(path.join(__dirname, "..", "tools", "machinery", "lifespan-20.html"), "utf8");
  const enPath = path.join(__dirname, "..", "i18n", "tools", "en", "machinery", "lifespan-20.json");
  const en = JSON.parse(fs.readFileSync(enPath, "utf8"));
  const enMap = en.map || en;
  // 结果卡与复制报告不得再出现定量精度保持寿命 / 年数 / 等级 / 参考标尺输出
  const noPrecisionLifeOutput = !src.includes("precisionLife=L10h*cf*lf")
    && !src.includes("精度保持寿命 (h)") && !src.includes("精度保持 (年)")
    && !src.includes("寿命等级") && !src.includes("'等级:'+grade")
    && !src.includes("TBKit.chart.refBar('#resRefBar'");
  const hasRelativeFactor = src.includes("相对折算系数") && src.includes("relFactor=cf*lf");
  const hasDisclaimer = src.includes("无可核验模型可换算为定量精度保持寿命")
    || src.includes("无可靠模型将其换算为定量精度保持寿命");
  const enSynced = Object.keys(enMap).some((k) => k.includes("为什么本页不再给出"))
    && Object.values(enMap).some((v) => String(v).includes("no reliable model converts them into a quantitative accuracy-retention life"));
  return [
    { name: "lifespan-20 停止输出定量精度保持寿命/年数/等级/标尺", ok: noPrecisionLifeOutput },
    { name: "lifespan-20 改为相对折算系数（非寿命预测）", ok: hasRelativeFactor },
    { name: "lifespan-20 明确无可核验模型换算为定量寿命", ok: hasDisclaimer },
    { name: "lifespan-20 新口径英文映射同步", ok: enSynced },
  ];
}

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
  { slug: "machinery/estimate-gravity", inputs: {shape:"plate", plateL:"-100", plateW:"50", plateH:"10"}, expect: ["尺寸须为正数"], ref: "987 负值守卫：板长 -100 mm 旧版算出负体积/负质量，修复后尺寸统一有限性与正值校验并拦截。" },
  { slug: "machinery/detector-stretch", inputs: {v1:"-0.5", v2:"22", v3:"1.2", hi1:"0.08", lo2:"20", lo3:"1"}, expect: ["实测值（不得为负）"], ref: "987 负值守卫：磨耗量 -0.5 g 旧版按 -0.5≤0.08 判「满足」，修复后负实测值拦截。" },
  { slug: "machinery/estimate-lifespan-bearing", inputs: {loadC:"67", loadP:"5", speed:"1500"}, expect: ["2406.10"], ref: "轴承寿命估算" },
  { slug: "machinery/frequency-17", inputs: {v_m:"200", v_k:"50000", v_f:"25"}, expect: ["2.516 固有频率"], ref: "振动隔振" },
  { slug: "machinery/gear", inputs: {v_fa:"200", v_fb:"150", v_fc:"120"}, expect: ["不满足", "320.00"], ref: "四连杆：200 使最短+最长 320 > 其余和 310 → 不满足 Grashof" },
  { slug: "machinery/lifespan-bearing-1", inputs: {v_F:"10000", v_d:"50", v_bd:"1"}, expect: ["4.000 平均压强"], ref: "滑动轴承" },
  { slug: "machinery/lifespan-bearing", inputs: {v_C:"45000", v_P:"2500", v_n:"1500"}, expect: ["5832.00 L10寿命"], ref: "滚动轴承寿命" },
  { slug: "machinery/pressure-4", inputs: {v_z:"48", v_m:"2", v_a:"30"}, expect: ["96.000 分度圆直径"], ref: "花键" },
  { slug: "machinery/runhuaxitongsheji", inputs: {v_d:"160", v_l:"80", v_n:"1500"}, expect: ["0.78 比压"], ref: "润滑系统" },
  { slug: "machinery/runhuaxitongsheji", inputs: {v_d:"80", v_l:"80", v_n:"1500", v_w:"10", v_eta:"30", v_psi:"1.5", v_dt:"20", v_type:"thrust"}, expect: ["推力滑动轴承按 d×L 作等效承载面积估算", "推力滑动轴承"], ref: "轴承类型参与计算：推力轴承输出等效面积提示与 PV 许用 8" },
  { slug: "machinery/shusongdaixuanxingjisuan", inputs: {vQ:"200", vL:"100", vAng:"200", vRho:"1.0", vV:"1.6"}, expect: ["倾角须在 0–30° 之间"], ref: "倾角越界拦截：200° 不再输出负提升高度/负功率" },
  { slug: "machinery/strength-15", inputs: {v_P:"11", v_n1:"1200", v_z1:"19"}, expect: ["19.05", "1520"], ref: "链传动强度：n1=1200 → p=19.05，F=1000P/v" },
  { slug: "machinery/strength-6", inputs: {v_d:"80", v_b:"12", v_h:"8"}, expect: ["49.34 挤压应力"], ref: "铆钉连接" },
  { slug: "machinery/tanhuangsheji", inputs: {v_d:"6", v_dd:"20", v_n:"8"}, expect: ["200.728 弹簧刚度"], ref: "弹簧设计" },
  { slug: "machinery/temp-hardness", inputs: {steelGrade:"custom", maxHrc:"45", temperK:"3", critDia:"15"}, expect: ["33.0 预期硬度"], ref: "热处理：自定义钢种 45-3×(500-150)/100=34.5，×0.9569 截面折减" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"73", v_lead:"7", v_f:"20"}, expect: ["140.286 驱动力矩"], ref: "螺旋传动" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"36.5", v_lead:"7", v_f:"30", v_mu:"0.12", v_muc:"0.12", v_dc:"40"}, expect: ["104.043 N·m（含推力轴承摩擦）"], ref: "下放力矩叠加推力轴承摩擦（674）：F=30 kN、μc=0.12、dc=40 → 螺纹项 30000×18.25×tan(3.349°)≈32043 + 轴承 30000×0.12×40/2=72000 = **104043 N·mm=104.043 N·m**（默认 20 kN/0.1/30 仅 51.362，修复前不含轴承项为 32.043）" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"36.5", v_lead:"30", v_f:"20", v_mu:"0.12", v_muc:"0.1", v_dc:"30"}, expect: ["—（不自锁，载荷会自行下放，必须配置制动器）"], ref: "非自锁文案（674）：导程 30 → λ=14.66°>ρ=6.84°，原同屏先写「不自锁（需制动）」又写「无需外力（重力自锁下放）」；现只提示载荷会自行下放、必须配制动器（默认导程 7 自锁，不含该串）" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"36.5", v_lead:"7", v_f:"20", v_mu:"0.06104573159689137", v_muc:"0.1", v_dc:"30"}, clicks: ["var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='TDCRIT '+((h.indexOf('满足自锁条件，载荷不会自行下落')>=0&&h.indexOf('必须配置制动器')<0&&/下放力矩：[\\d.]+ N·m（含推力轴承摩擦）/.test(h))?'OK':'BAD');"], expect: ["TDCRIT OK"], ref: "674 临界边界：mu=lead/(π·d2)=7/(π×36.5) ⇒ λ=ρ=3.4933°。修复前 isSelfLocking=true(λ<=ρ) 显示「满足自锁」但下放行用 rho>lambda=false 显示「必须配置制动器」，同屏自相矛盾；修复后两处统一 λ<=ρ，临界显示下放力矩数值（=轴承摩擦项）且与自锁判定一致。非临界默认 μ=0.12 不命中该精确串。" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"36.5", v_lead:"7", v_f:"0", v_mu:"0.12", v_muc:"0.1", v_dc:"30"}, expect: ["轴向载荷须大于 0"], ref: "轴向载荷为分子非分母（674）：F=0 原被 guard 误报「「v_f」是本计算的分母，不能为 0」；现按载荷须 >0 拦截并给出正确提示（默认 20 kN 合法）" },
{ slug: "machinery/zhujian-bamoxiedu-sheji", inputs: {v0:"120", v1:"200"}, expect: ["204.19","2.09%"], ref: "v0=120,v1=200 → 高度落 50–200 档取 1.0°、尺寸差 120×tan1°=2.09 mm、上端外径 200+2×2.09=204.19 mm、放大率 2×2.09/200=2.09%（默认 60/200 → 1.0/1.05/202.09/1.05%；交换 200/60 → 1.0/3.49/66.98/11.64%。斜度档位 1.0 三态相同故不作断言，「2.09」被子串于默认态 202.09 亦剔除）" },
{
  "slug": "machinery/xiao-dingwei-lianjie-chicun",
  "inputs": {
    "v0": "50",
    "v1": "100"
  },
  "expect": [
    "25.231", "17.841双销并联直径（mm）"
  ],
  "ref": "销钉直径 d=√(4×50×1000/(π×100))=25.231 mm；双销并联两销各担 F/2，每销直径=d/√2=17.841 mm（修复前误算 2d=50.46）。默认 20/120 得 d=14.567、双销 10.301，注入失败即不命中"},
  { slug: "machinery/analysis-casting", inputs: {vol:"3000", area:"600", rho:"7.8", C:"2.4"}, expect: ["23400.00"], ref: "铸件重量 G = V·ρ = 3,000 × 7.8 = **23,400.00** g（默认 1,000 cm³ × 7.2 得 7,200.00）" },
  { slug: "machinery/detector-159", inputs: {v1:"80", v2:"60", v3:"2", t1:"100", t2:"50", t3:"1"}, expect: ["-20.0%", "1 项低于设计限值"], ref: "刚度 80 低于设计下限 100 → 裕度 (80-100)/100×100% = -20.0%，共 1 项低于限值（默认 120/60/2 与 100/50/1 全满足，不含这两个串）" },
  { slug: "machinery/detector-134", inputs: {v1:"12", v2:"250", v3:"0.06", lo1:"15", lo2:"200", hi3:"0.1"}, expect: ["-20.0%", "1 项不满足设计限值"], ref: "断裂强力 12 < 下限 15 → 裕度 (12-15)/15×100% = -20.0%，共 1 项不满足（默认 18/250/0.06 与 15/200/0.1 全满足，不含这两个串）" },
  { slug: "machinery/detector-stretch", inputs: {v1:"0.1", v2:"18", v3:"1.2", hi1:"0.08", lo2:"20", lo3:"1"}, expect: ["-25.0%", "2 项不满足设计限值"], ref: "磨耗量 0.1 > 上限 0.08 → 裕度 (0.08-0.1)/0.08×100% = -25.0%；拉伸强度 18 < 下限 20 → -10.0%；共 2 项不满足（默认 0.06/22/1.2 与 0.08/20/1 全满足）" },
  { slug: "machinery/detector-hardness-torque", inputs: {v1:"130", v2:"31", v3:"0.08", lo1:"80", hi1:"120", lo2:"28", hi2:"34", hi3:"0.05"}, expect: ["-60.0%", "2 项不满足设计限值"], ref: "尺寸偏差 0.08 > 上限 0.05 → 裕度 (0.05-0.08)/0.05×100% = -60.0%；扭矩 130 > 上限 120 → 上侧裕度 (120-130)/120×100% = -8.3%；共 2 项不满足（默认 100/31/0.03 与 80~120/28~34/0.05 全满足）" },
  { slug: "machinery/detector-155", inputs: {v1:"3.5", v2:"25", v3:"3", hi1:"2.8", lo2:"5", hi2:"20", hi3:"5"}, expect: ["-25.0%", "2 项不满足设计限值"], ref: "振动速度 3.5 > 上限 2.8 → 裕度 (2.8-3.5)/2.8×100% = -25.0%；游隙 25 > 上限 20 → 上侧裕度 (20-25)/20×100% = -25.0%；共 2 项不满足（默认 2.0/12/3 与 2.8/5~20/5 全满足）" },
  { slug: "machinery/detector-134", inputs: {v1:"18", v2:"250", v3:"-1"}, expect: ["请输入有效的实测值"], ref: "负实测值拦截（670）：磨耗量 -1 g 物理不可能，按 ≤0.1 判原本会「合格」；现直接输出无效提示并中止（默认 0.06 合法，不含该串）" },
  { slug: "machinery/detector-hardness-torque", inputs: {v1:"100", v2:"31", v3:"-0.5"}, expect: ["请输入有效的实测值"], ref: "负实测值拦截（670）：尺寸偏差 -0.5 mm 按 ≤0.05 原本判「合格」；现判为无效输入（默认 0.03 合法，不含该串）" },
  { slug: "machinery/detector-155", inputs: {v1:"-1", v2:"12", v3:"3"}, expect: ["请输入有效的实测值"], ref: "负实测值拦截（670）：振动速度 -1 mm/s 按 ≤2.8 原本判「合格」；现判为无效输入（默认 2.0 合法，不含该串）" },
  { slug: "machinery/lifespan-20", inputs: {vClass:"p4", vC:"20", vP:"3", vN:"5000", vD:"40", vLube:"grease"}, expect: ["200.00k"], ref: "内径 40mm × 5000rpm → dn = **200.00k** mm·rpm（默认 25mm 得 125.00k，不含 200.00k；仅保留随 vD 变化的数值锚，避免 label 常驻造成逃生）" },
  { slug: "machinery/speed-26", inputs: {v0:"18", v1:"1450", v2:"2", v3:"2"}, expect: ["9.3", "19.3"], ref: "18kW×速度系数1.0 ÷ (kz=21/19 × ks=1.75) → 折算需求 **9.3** kW，08A 折算额定 10×1.105×1.75 = **19.3** kW（默认 5.5kW/960rpm/单排 得 6.1/8.9，不含这两个串）" },
  { slug: "machinery/speed-26", inputs: {v0:"400", v1:"960", v2:"1", v3:"1"}, expect: ["447.1", "223.7", "超出 06B~24A"], ref: "400kW 折算需求 **447.1** kW > 24A 折算额定 **223.7** kW → 页面明确提示「超出 06B~24A」，不再静默按 24A 通过（默认不含该串）" },
  { slug: "machinery/analysis-casting", inputs: {vol:"3000", area:"600", rho:"7.8", C:"2.4"}, expect: ["60.0"], ref: "凝固时间 t = C·M² = 2.4 × (3,000/600)² = 2.4 × 25 = **60.0** s（模数 M = 5.000 cm；默认 t = 12.5 s）" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"5000", nf:"25", mt:"50", tv:"200"}, expect: [ "0.00500 次/h" ], ref: "MTBF = 总运行 5,000 h ÷ 故障 25 次 = **200.00** h（默认 8,760/22 得 398.18）" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"5000", nf:"25", mt:"50", tv:"200"}, expect: ["36.79%"], ref: "可靠度 R(200) = e^(−t/MTBF) = e^(−200/200) = **36.79%**；累计失效概率 63.21% 与之相加为 100%" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"8760", nf:"22", mt:"-66", tv:"500"}, expect: ["累计维修时间须在 0 与总运行时间之间"], ref: "负维修时间拦截（672）：原按 mt=-66 得 MTTR -3.00 h、可用度 100.76%；现标红中止（默认 mt=66 合法，不含该串）" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"8760", nf:"22", mt:"9000", tv:"500"}, expect: ["累计维修时间须在 0 与总运行时间之间"], ref: "维修时间上限拦截（672）：累计维修 9,000 h > 总运行 8,760 h 物理不可能，MTTR 会大于 MTBF；现标红中止" },
  { slug: "machinery/analysis-lifespan", inputs: {rt:"8760", nf:"0.5", mt:"66", tv:"500"}, expect: ["故障次数须为正整数"], ref: "故障次数须为正整数（672）：0.5 次故障无统计意义，原按 0.5 次参与 MTBF=17,520 h；现标红中止" },
  { slug: "machinery/calc-gear", inputs: {module:"3", teeth:"16", pressure:"20"}, expect: ["48.0000"], ref: "分度圆 d = m·z = 3 × 16 = **48.0000** mm（默认 2×20 得 40.0000）" },
  { slug: "machinery/calc-gear", inputs: {module:"3", teeth:"16", pressure:"20"}, expect: ["54.0000"], ref: "齿顶圆 da = d + 2hₐ = 48 + 2×1×3 = **54.0000** mm；齿根圆 df = 48 − 2×1.25×3 = 40.5000，与 da 相差恰为一个全齿高" },
  { slug: "machinery/analysis-casting", inputs: {vol:"1000", area:"400", rho:"-5", C:"2.0"}, expect: ["体积、表面积、密度与凝固系数均须为正数"], ref: "986 负值守卫：密度 -5 旧版算出 -5000.00 g 并照常输出，修复后非正值拦截。" },
  { slug: "machinery/calc-89", inputs: {v_D:"200", v_d:"120", v_mu:"0.25", v_F:"2000", v_z:"2.5", v_n:"1500"}, expect: ["摩擦面数须为正整数"], ref: "986 整数守卫：摩擦面数 2.5 旧版接受并乘进扭矩，修复后非整数拦截。" },
  { slug: "machinery/calc-gear", inputs: {module:"2", teeth:"20", pressure:"90", helix:"0", haCoef:"1", cCoef:"0.25"}, expect: ["压力角须在 0 到 90 度之间"], ref: "986 角度守卫：α=90 旧版只标红不中止仍输出 db=0/pb=0，修复后提前拦截。" },
  { slug: "welding/calc-weld", inputs: {plateThk:"10", weldSize:"8", weldLen:"200", load:"40", weldMat:"E50"}, expect: ["5.66"], ref: "角焊缝喉厚 a = 0.707 K = 0.707 × 8 = **5.66** mm（默认 6 ⇒ 4.24）" },
  { slug: "welding/calc-weld", inputs: {plateThk:"10", weldSize:"8", weldLen:"200", load:"40", weldMat:"E50"}, expect: ["1131.20"], ref: "有效面积 A = a·L = 5.66 × 200 = **1131.20** mm²（默认 424.20）。页面先按 0.707K 四舍五入到 5.66 再乘全长，与一步相乘 1131.37 有 0.17 的舍入差 ⇒ 锚取页面值" },
  { slug: "machinery/calc-200", inputs: {pload:"1200", nVal:"1450", eff:"90"}, expect: ["1333.33", "超出 IEC 标准功率表上限"], ref: "所需功率 P = 1200 ÷ 0.9 = **1333.33** kW > 630 kW → 只输出所需功率与「超出 IEC 标准功率表上限」，不再推荐 630 kW 电机、不再给额定转矩/裕量（默认 7.5/90% 得 8.33 kW、推荐 11 kW，不含这两个串）" },
  { slug: "machinery/calc-200", inputs: {pload:"7.5", nVal:"1450", eff:"120"}, expect: ["传动效率不得超过 100%"], ref: "效率 120% 越界拦截（671）：原按 η=120 得所需 6.25 kW、推荐 7.5 kW、判「裕量合适」，与物理不符；现直接报错中止（默认 90% 合法，不含该串）" },
  { slug: "machinery/zhineng-wurenyugaoxiaoduibijisuanqi", inputs: {v0:"90", v1:"70", v2:"95"}, expect: ["无人化路线优先", "37.3%"], ref: "三路线评分（673）：合计 255，无人化 95 最高 → 「无人化路线优先」，权重 95/255 = **37.3%**；默认 88/80/75 时智能优先且权重 36.2%，不含这两个串" },
  { slug: "machinery/zhineng-wurenyugaoxiaoduibijisuanqi", inputs: {v0:"80", v1:"80", v2:"80"}, expect: ["智能/无人化/高效路线优先"], ref: "三项并列最高（673）：应同时列出三条路线，不再只按 A>B 判「高效路线优先」（默认 88/80/75 不含该串）" },
  { slug: "machinery/zhineng-wurenyugaoxiaoduibijisuanqi", inputs: {v0:"50", v1:"-50", v2:"0"}, expect: ["评分须为 0–100 的数值，且三项不能同时为 0"], ref: "负评分与合计为 0 拦截（673）：原 A+B=0 时占比出 Infinity，同屏仍给「智能路线优先」；现标红中止（默认合法，不含该串）" },
  { slug: "machinery/thread-recognize", inputs: {diameter:"20", pitch:"2.5", threadAngle:"60"}, expect: ["10.2"], ref: "英制换算 TPI = 25.4 ÷ 螺距 2.5 = **10.2** 牙/in（默认 M10×1.5 得 16.9）" },
  { slug: "machinery/thread-recognize", inputs: {diameter:"20", pitch:"2.5", threadAngle:"60"}, expect: ["17.294"], ref: "小径 d₁ = 外径 20 − 1.0825 × 螺距 2.5 = 20 − 2.70625 = **17.294** mm（默认 M10 得 8.376）" },
  {"slug": "machinery/stretch", "inputs": {"wireDia": "3.5", "coilDia": "16", "activeCoils": "10"}, "expect": ["4.571 弹簧指数 C 1.345 Wahl系数 Kw 19.500 外径 D₂ (mm) 12.500 内径 D₁ (mm)", "36.178 弹簧刚度 k (N/mm) 1534.014 最大载荷 Fmax (N) 42.401 最大变形 δmax (mm)", "⚠️ 最大变形量超过可用行程（L₀-Lb=-2.000mm），弹簧可能被压并。", "✓ 弹簧指数 C=4.571 在推荐范围 4~16 内。"], "ref": "独立复算（碳素弹簧钢丝 G=79 GPa、τ=560 MPa，G 先 ×1000 转 MPa）：C = 16/3.5 = 4.571；Kw = (4×4.571−1)/(4×4.571−4) + 0.615/4.571 = 17.284/14.284 + 0.1346 = 1.3449 ⇒ 1.345；D₂ = 16+3.5 = 19.5、D₁ = 16−3.5 = 12.5；k = 79000×3.5⁴/(8×16³×10) = 79000×150.0625/327,680 = 11,854,937.5/327,680 = 36.178 N/mm；Fmax = 560×π×42.875/(8×1.3449×4.571) = 75,398.5/49.180 = 1534.01 N；δmax = 1534.014/36.178 = 42.401 mm。默认态（d=2、D=12、n=8）为 C=6.000、Kw=1.252、k=11.429、Fmax=234.104、δmax=20.483，四组锚均不命中。注：t 与 Lb 两项页面算法与常规 (n+1)d / (n+1.5)d+d 不同，故不作锚。材料默认 carbon 未变，不锚「材料」相关串（判别器保留 clicks，见 §10.5）。"},
  {"slug": "machinery/stretch", "inputs": {"wireDia": "2.5", "coilDia": "10", "activeCoils": "12", "freeLen": "55"}, "clicks": ["document.getElementById('springMat').value='304';calc();"], "expect": ["4.000 弹簧指数 C 1.404 Wahl系数 Kw 12.500 外径 D₂ (mm) 7.500 内径 D₁ (mm)", "29.704 弹簧刚度 k (N/mm) 480.820 最大载荷 Fmax (N) 16.187 最大变形 δmax (mm)", "⛔ 长径比 5.500 > 4，压缩弹簧易发生屈曲失稳，建议加导向杆或减小自由长度。"], "ref": "独立复算（304 不锈钢 G=73 GPa、τ=440 MPa）：C = 10/2.5 = 4.000；Kw = 15/12 + 0.15375 = 1.40375 ⇒ 1.404；D₂ = 12.5、D₁ = 7.5；k = 73000×39.0625/(8×1000×12) = 2,851,562.5/96,000 = 29.704 N/mm；Fmax = 440×π×15.625/(8×1.40375×4) = 21,598.9/44.92 = 480.82 N；δmax = 480.820/29.704 = 16.187 mm；长径比 L₀/D = 55/10 = 5.5 > 4 ⇒ 触发屈曲警告。与上一例互为对照：换材料（G 79→73、τ 560→440，k 36.178→29.704、Fmax 1534→481 全部随之变）、换规格、并跨「长径比 ≤4 安全 / >4 屈曲」两分支。材料切换走 clicks（select 桩无 option selected）；仅锚随 inputs+G 变化的 k/Fmax/δmax，不锚 C 相关的静态推荐区间串。默认态不命中。"},
  { slug: "machinery/strength-7", inputs: {v_d:"10", v_t:"12", v_n:"4", v_w:"120", v_f:"150", v_tau:"100", v_sigc:"250", v_sigt:"180"}, expect: ["477.46", "312.50", "156.25", "12.1%", "不合格"], ref: "铆缝强度（8 字段全注入）：d=10 t=12 n=4 w=120 F=150 τ=100 σc=250 σt=180 → As=314.16 τ=477.46 σc=312.50 σt=156.25 F_min=31.42kN η=12.1% 不合格（默认 d=16 t=10 n=4 w=120 F=60 τ=90 σc=210 σt=140 → 43.1%/74.60/93.75/107.14/偏低，均不命中）。校验 valid 要求 w>n·d（120>40 满足）。锚全部为随输入变化的结果值，规避输入回显；「剪切控制」为默认/注入共有（恒 F_shear 最弱）故不锚。" },
  { slug: "machinery/tolerance", inputs: {v_d:"40"}, expect: ["0.0494 最大间隙 (mm)", "0.0088 最小间隙 (mm)"], ref: "基孔制 H7/g6 间隙配合：v_d=40 → 最大间隙 0.0494、最小间隙 0.0088（默认 v_d=50 → 0.0500/0.0095，不命中）。注：「配合公差 (mm)」=孔IT7+轴IT6，D=40/50 同处一级公差区恒为 0.0406，不随 v_d 变 ⇒ 不锚（否则成逃生项）。锚结果值+单位，规避输入 40 回显。" },
  { slug: "machinery/tolerance-1", inputs: {v_d:"80"}, expect: ["0.0080 公差值 (mm)", "8.00 公差值 (μm)"], ref: "形位公差查表：v_d=80（直径 ≤80mm 查表档）→ 圆度/圆柱度 7 级中等级，公差值 0.0080mm / 8.00μm（默认 v_d=50 → 0.0070/7.00，不命中）。锚结果值+单位，规避输入 80 回显。" },
  { slug: "machinery/zhineng-wurenyugaoxiaoduibijisuanqi", inputs: {v0:"90", v1:"60"}, expect: ["30 综合差距", "40.0% 智能权重占比"], ref: "三路线评分（673 起新增无人化评分，未注入时取页面默认 75）：v0=90 v1=60 v2=75 → 综合差距 30、智能权重 90/225 = 40.0%（默认 88/80/75 → 13/36.2%，不命中）。锚合成结果，规避输入回显。" },
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
      "42\n42\n42\n42\n42\n42\n请检查输入：外径须大于内径，摩擦面数须为正整数，各值须为正数\n暂无计算记录"
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
    "slug": "welding/calc-weld",
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
      ") 润滑方式推荐：脂润滑或手加油（端面速度低，脂润滑即可满足） ✓ PV值 2.20"
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
      "请输入有效参数（板宽须大于每排铆钉总径，铆钉数/剪切面数/每排数为正整数）"
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
      "42\n42\n42\n42\n42\n42\n请输入有效参数（中径、导程、轴向载荷须大于 0，摩擦系数须在 0~0.5 之间）\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例，674 更新提示词）：注入非默认输入{\"v_d2\":\"42\",\"v_lead\":\"42\",\"v_f\":\"42\",\"v_mu\":\"42\",\"v_muc\":\"42\",\"v_dc\":\"42\"}，μ=42 越界 ⇒ 输出「请输入有效参数（中径、导程、轴向载荷须大于 0，摩擦系数须在 0~0.5 之间）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
    "slug": "machinery/zhujian-bamoxiedu-sheji",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "42\n42\n1.5 起模斜度（°） 1.10"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\"}，输出区含「42\n42\n1.5 起模斜度（°） 1.10」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  { slug: "machinery/detector-194", inputs: { v3: "" }, expect: ["请填写使用年限（年）后再生成维修方案。"], ref: "空态守卫（2026-11-05）：清空使用年限（本页唯一可为空的计算字段）后不再渲染「使用年限：0年」+「建议方案：维修修复」整套结论，只给填写提示。⚠ 判空用原始空串而非数值 0——「0 年」（新装设备）是合法输入，仍照常计算。默认 v3=5 ⇒ 提示串不出现。" },
  { slug: "machinery/detector-194", inputs: { v1: "2", v3: "10" }, expect: ["设备：电机", "使用年限：10年", "建议方案：更换设备"], ref: "注入 电机 + 10 年：设备名改「电机」、年限回显 10、years>8 ⇒「建议方案：更换设备」（默认 泵类/5 年 ⇒ 维修修复，三条均不命中 ⇒ 与空态提示互斥）。" },
  { slug: "machinery/lifespan-18", inputs: { vNoise: "30", vLimit: "50", vSpeed: "1500", vLoad: "300" }, clicks: ["document.getElementById('vLube').value='mist';calc();"], expect: ["1.50k"], ref: "深解第二算例对齐（663）：载荷因子 (300/500)^0.3 = 0.858，rate = 0.0008×√1500×0.858×1×0.5 = 0.013291 dB/h，寿命 20/0.013291 = 1504.8 h ⇒ 显示 1.50k（默认 500N/脂润滑 ⇒ 645.5，不含该串）" },
  { slug: "machinery/pressure-4", inputs: { v_z: "30", v_m: "2", v_a: "30" }, expect: ["63.000 内花键大径"], ref: "内花键大径标签（664）：平齿根 DII = m(z+1.5) = 2×31.5 = 63.000 应标「内花键大径」，交换前此处显示「内花键小径」（默认 z=24 ⇒ 51.000，不含 63.000）" },
  { slug: "machinery/pressure-4", inputs: { v_z: "30", v_m: "2", v_a: "30" }, expect: ["58.000 内花键小径"], ref: "内花键小径标签（664）：平齿根 DIE2 = m(z−1) = 2×29 = 58.000 应标「内花键小径」，交换前此处显示「内花键大径」（默认 z=24 ⇒ 46.000，不含 58.000）" },
  { slug: "machinery/torque-3", inputs: { vT: "400", vTemp: "0", vWear: "20", vDyn: "1.5" }, clicks: ["var d=document.getElementById('vDyn'),c=document.getElementById('vCond');c.value='1.3';calc();saveHistory();d.value=1.0;c.value='1.0';calc();restoreHistory(0);var t=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='TC3 '+(t.indexOf('936.0')>=0&&String(d.value)==='1.5'&&c.value==='1.3'?'OK':'BAD');"], expect: ["TC3 OK"], ref: "历史恢复补齐动载/工况（665）：T=400、磨 20%、动载 1.5、工况 1.3 ⇒ 480×1.5×1.3 = 936.0 N·m；保存后把动载/工况改 1.0（显示 480.0），点恢复应回填 1.5/1.3 并复现 936.0。修复前恢复只回填 T/温/磨 ⇒ 480.0、BAD。" },
  { slug: "machinery/torque-2", inputs: { vT: "300", vK1: "1.2", vK2: "1.1", vN: "1450" }, clicks: ["var l=document.getElementById('vLoad');l.value='1.5';calc();saveHistory();l.value='3.0';calc();restoreHistory(0);var t=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='TC2 '+(t.indexOf('594.0')>=0&&l.value==='1.5'?'OK':'BAD');"], expect: ["TC2 OK"], ref: "历史恢复补齐负载特性（665）：T=300、K1=1.2、K2=1.1、负载 1.5 ⇒ 594.0 N·m；保存后把负载改 3.0（显示 1188.0），点恢复应回填 1.5 并复现 594.0。修复前恢复只回填四项 ⇒ 1188.0、BAD。" },
  { slug: "machinery/power-16", inputs: { pVal: "5.5", n1: "1450", ratio: "10" }, expect: ["超出 800mm 标准系列"], ref: "大带轮超系列拦截（666）：d₁=125，d₁×i=1250 > 800 ⇒ 提示「目标大带轮 ⌀1250mm 超出 800mm 标准系列」且实际传动比显示「—」（修复前静默截断为 800、显示 6.40；默认 i=2.5 不含该串）" },
  { slug: "machinery/power-16", inputs: { pVal: "22", n1: "100", ratio: "3" }, expect: ["转速过低", "减速机或链传动"], ref: "低转速带速不足提示（666）：n₁=100 ⇒ 带速 ≥5 m/s 需 d₁≥955mm（超 800 系列），页面提示改减速机/链传动（修复前 d₁=200、带速 1.05 m/s 仍照常「推荐」；默认 1450rpm 不含该串）" },
  { slug: "machinery/lifespan-23", inputs: { vTemp: "130", vRpm: "9000" }, clicks: ["document.getElementById('vOil').value='ester';calc();"], expect: ["18 建议换油间隔"], ref: "换油间隔不再被 500h 下限抬高（667）：酯类油 6000h、130℃、9000rpm ⇒ fTemp=0.5⁷=0.0078125、fRpm=0.85⁶=0.37715、寿命 23h，间隔 round(23×0.8)=18h（修复前 max(500,…)=500；默认 70℃/3000rpm 为 1040）" },
  { slug: "machinery/lifespan-23", inputs: { vTemp: "130", vRpm: "9000" }, clicks: ["document.getElementById('vOil').value='ester';calc();"], expect: ["润滑寿命不足 500h"], ref: "短寿命提示（667）：寿命 23h < 500h ⇒ advice 追加「润滑寿命不足 500h，建议缩短换油/补油周期并按状态监测」（默认 1300h 不含该串）" },
  { slug: "machinery/power-16", inputs: { pVal: "5.5", n1: "1450", ratio: "10" }, expect: ["几何派生值不适用"], ref: "666 复核（超系列停止派生）：d₁×i=1250>800 ⇒ 中心距/带长/包角显示「—」，总结与复制文本标注几何派生值不适用；默认 i=2.5 不含该串" },
  { slug: "machinery/power-16", inputs: { pVal: "5.5", n1: "6000", ratio: "2" }, expect: ["增大带轮无法降速"], ref: "666 复核（高速不反向增轮）：n₁=6000 ⇒ 最小标准轮径 80mm 下带速 25.1>25；v 与 d₁ 正相关，旧 while 逐档增轮反把带速推高并推到 800mm，现明确提示无法降速；默认 1450rpm 不含该串" },
{
  "slug": "machinery/bearing-1",
  "inputs": {"cVal":"50","pVal":"5","nVal":"1500","bType":"3","reli":"95","aisoVal":"0.8"},
  "expect": ["512.0","5688.9"],
  "ref": "C/P=10，L10=1000 百万转；a1(95%)=0.64、aISO=0.8 ⇒ Lnm=0.512×1000=512.0 百万转，Lnmh=512e6/(60×1500)=5688.9 h。默认 90%/aISO=1 得 1000/11111 ⇒ 不命中"
},
{
  "slug": "machinery/bearing-1",
  "inputs": {"cVal":"50","pVal":"5","nVal":"1500","bType":"3","reli":"90","aisoVal":"0"},
  "expect": ["aISO 均需大于 0"],
  "ref": "aISO=0 不得输出修正寿命 0"
},
{
  "slug": "machinery/strength-15",
  "inputs": {"v_P":"100","v_n1":"960","v_z1":"19","v_z2":"57"},
  "expect": ["6.2 静强度安全系数"],
  "ref": "功率参与选型：100 kW/960 rpm/19 齿，初档 12A 圆周力 17267 N、破断 45.4 kN 安全系数 2.63<4 ⇒ 升档 16A，F=12952 N、80.2/12.952=6.19；默认 5.5 kW 为 12A、安全系数 47.8 ⇒ 不命中"
},
{
  "slug": "machinery/calc-gear",
  "inputs": {"module":"2","teeth":"13","pressure":"20","helix":"20","haCoef":"1","cCoef":"0.25"},
  "clicks": ["document.querySelector('input[name=gearType][value=helical]').checked=true;calc();"],
  "expect": ["14.4","小于不根切最少齿数"],
  "ref": "斜齿根切最少齿数：αt=atan(tan20°/cos20°)=21.17°，zmin=2×1×cos20°/sin²αt=14.4；z=13 应判根切。旧式 cos³β 得 12.7，13 齿会被误判不根切"
},
{
  "slug": "machinery/detector-194",
  "inputs": {"v1":"3","v2":"2","v3":"6","v4":"4"},
  "expect": ["更换设备","检查阀杆与阀座密封","经济寿命阈值 5 年"],
  "ref": "MM-H80：设备类型/运行模式须参与判定。阀门+频繁启停、6 年 > 阈值 5 ⇒ 更换；清单应为阀杆/执行机构，不得再给泵的轴承/联轴器套话。若仍只按 years>8，则 6 年会判维修 ⇒ 不命中"
},
{
  "slug": "machinery/detector-194",
  "inputs": {"v1":"1","v2":"1","v3":"","v4":"1"},
  "expect": ["请填写使用年限（年）后再生成维修方案"],
  "ref": "空年限不得按 0 年输出「维修修复」结论"
},
{
  "slug": "machinery/jingmishebeixuanxing",
  "inputs": {"vAcc":"50","vLoad":"50","vStroke":"500","vSpeed":"15"},
  "expect": ["C7","±50μm/300mm"],
  "ref": "MM-H91：定位精度 50μm 判 C7，导程精度须随等级显示 ±50μm/300mm；旧逻辑按导程 5mm 显示 ±3μm/300mm，与 C7 自相矛盾。默认 acc10/lead5 为 C3/±3 ⇒ 不命中"
},
{
  "slug": "machinery/lifespan-7",
  "inputs": {"vMat":"nbr","vTemp":"300","vPress":"1","vSpeed":"500","vShaft":"50","vMed":"oil"},
  "expect": ["材料可能分解，不可继续使用","10"],
  "ref": "NBR 上限 120℃：130℃ 取 0.05、300℃ 远超 20℃ 取 0.001，寿命触底 10h；旧逻辑两个温度同为 0.05/231h，无法区分超温程度"
},
{
  "slug": "machinery/lifespan-7",
  "inputs": {"vMat":"nbr","vTemp":"-50","vPress":"1","vSpeed":"500","vShaft":"50","vMed":"oil"},
  "expect": ["低于材料低温极限"],
  "ref": "NBR 低温下限 -30℃：-50℃ 须提示脆裂/更换材质；旧逻辑 Q10 外推得 2^13，寿命反而放大"
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

  const scopeStat = lifespan20ScopeChecks();
  const scopeFails = scopeStat.filter((s) => !s.ok);
  for (const s of scopeFails) console.log("❌ [static] " + s.name);

  console.log("==== machinery calc " + pass + "/" + cases.length + " ====");
  if (scopeFails.length) console.log("❌ static " + (scopeStat.length - scopeFails.length) + "/" + scopeStat.length + " 未通过");
  if (fails.length || scopeFails.length) process.exit(1);
}
if (require.main === module) main();