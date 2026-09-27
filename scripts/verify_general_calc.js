#!/usr/bin/env node
/**
 * general 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）；
 * 与之区别仅在于用例集：it 用编码/哈希权威测试向量，general 用工程标准公式/独立复算。
 *
 * 用法：
 *   node scripts/verify_general_calc.js                 # 跑全部用例
 *   node scripts/verify_general_calc.js frequency-3 tax # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化/运行日期
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 *
 * 期望值一律由独立公式或 python/node 复算得出，不凭记忆。
 * 注意：**依赖「今天」**的日期类工具不纳入（否则门禁会随运行日期失败）；
 * 但用**固定日期对**的年龄计算可以纳入 —— 如 BATCH258 的 `calc-14`（出生 1990-05-20 → 计算日 2024-01-01），
 * 结果与运行日期无关，既有判别力又不会漂移。
 *
 * 2026-09-18 第六批：原 15 例 inputs 与页面默认值完全相同（all_default 弱用例，注入失败也假通过），
 * 已全部改为非默认输入并重新独立复算 expect，恢复判别力。
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  {
    slug: "general/frequency-3",
    inputs: { a4: "523.25" },
    expect: ["523.3 A4（基准）", "311.1 C4（中央C）"],
    ref: "十二平均律：输入 A4=523.25Hz；C4 = 523.25×2^(-9/12) = 311.13 Hz；A5 = 523.25×2 = 1046.5 Hz",
  },
  {
    slug: "general/calculator-calc-10",
    inputs: { data: "1,2\n2,3.5\n3,5\n4,6.2\n5,8" },
    expect: ["1.47x + 0.53"],
    ref: "最小二乘：斜率 = Σ(x-x̄)(y-ȳ)/Σ(x-x̄)² = 14.7/10 = 1.47；截距 = ȳ-a·x̄ = 4.94-4.41 = 0.53",
  },
  {
    slug: "general/calculator-calc-11",
    inputs: { aRe: "5", aIm: "2", bRe: "3", bIm: "1" },
    expect: ["8+3i", "13+11i", "1.7+0.1i"],
    ref: "复数运算：(5+2i)+(3+i)=8+3i；(5+2i)(3+i)=13+11i；(5+2i)/(3+i)=1.7+0.1i",
  },
  {
    slug: "general/calc-ratio-2",
    inputs: { v0: "30", v1: "1", v2: "5" },
    expect: ["166.7 mL 原液用量", "1 : 30 稀释配比"],
    ref: "稀释：原液 = 1/30×5L = 0.1667L = 166.7mL；加水量 = 5-0.1667 = 4.833L；稀释倍数 30/1 = 30",
  },
  {
    slug: "general/tax",
    inputs: { base: "2000000", vat: "13", city: "5", edu: "3", local: "2" },
    expect: ["260,000 增值税", "14.30% 综合税费率"],
    ref: "增值税 = 2000000×13% = 260000；城建税 = 260000×5% = 13000；附加合计 26000；综合税费率 = (260000+26000)/2000000 = 14.30%",
  },
  {
    slug: "general/voltage",
    inputs: { voltage: "80", current: "150", speed: "20", spot: "0.8" },
    expect: ["12000 束功率 P (W)", "2.39e+4 功率密度 (W/mm²)"],
    ref: "电子束焊接：束功率 P = U×I = 80×150 = 12000W；线能量 E = P/v = 12000/20 = 600 J/mm；功率密度 = 12000/(π×0.4²) = 2.39e+4 W/mm²",
  },
  {
    slug: "general/calc-stats-1",
    inputs: { mu: "100", sigma: "15", x: "130" },
    expect: ["0.977250", "0.053991"],
    ref: "正态分布 μ=100、σ=15、x=130 → z=(130−100)/15=2；Φ(2)=0.977250（误差函数近似），密度 f(2)=exp(−2²/2)/√(2π)=0.053991。默认输入 μ=0/σ=1/x=1.96 输出 0.975002/0.058441，故非默认输入具判别力",
  },
  {
    slug: "general/calc-13",
    inputs: { v0: "2026-06-04", v1: "2026-09-12" },
    expect: ["100 自然日", "2400 小时数"],
    ref: "2026-06-04 → 2026-09-12 共 100 天（30+31+31+8）；×24 = 2400 小时",
  },
  {
    slug: "general/temp-pressure-3",
    inputs: { v0: "2.5", v1: "800", v2: "120", v3: "0.9", v4: "2.0" },
    expect: ["9.368 计算壁厚 (mm)", "11.37 设计壁厚 (mm)"],
    ref: "GB/T 150 内压圆筒：δ = P·Di/(2[σ]φ-P) = 2.5×800/(2×120×0.9-2.5) = 9.368mm；设计壁厚 = δ+C2 = 9.368+2.0 = 11.37mm",
  },
  {
    slug: "general/ratio-50",
    inputs: { v0: "70", v1: "30", v2: "200", v3: "15", v4: "120" },
    expect: ["140.00 化学品A用量 (kg)", "161.00 安全备量A (kg)"],
    ref: "配比：A = 200×70% = 140kg；B = 60kg；安全备量 A = 140×1.15 = 161kg；反应放热 = 200×120/1000 = 24MJ",
  },
  {
    slug: "general/calc-speed-capacity",
    inputs: { v0: "8000", v1: "22.2", v2: "25", v3: "60" },
    expect: ["177.6 电池能量（Wh）", "555.0 平均功率（W）", "9.25 能耗（Wh/km）"],
    ref: "无人机：电池能量 = 8000mAh×22.2V/1000 = 177.6Wh；平均功率 = 25A×22.2V = 555W；续航 = 8Ah÷25A = 0.32h；航程 = 0.32×60 = 19.2km；能耗 = 177.6÷19.2 = 9.25 Wh/km（原实现多乘 1000，得 9250.0）",
  },
  {
    slug: "general/power-16",
    inputs: { pVal: "7.5", n1: "2900", ratio: "3.0" },
    expect: ["19.0 带速 (m/s)", "400 大带轮直径 (mm)"],
    ref: "V带传动：带速 = π×125×2900/60000 = 18.98→19.0m/s；大带轮 = 125×3.0 = 375 → 圆整 400mm；实际传动比 = 400/125 = 3.20",
  },
  {
    slug: "general/time-33",
    inputs: { layer: "0.3", infill: "30", volume: "50", speed: "80", nozzle: "0.6", density: "1.25", filD: "2.85" },
    expect: ["29.7 耗材质量 (g)", "23.75 有效体积 (cm³)"],
    ref: "FDM：有效体积 23.75cm³；质量 = 23.75×1.25 = 29.69→29.7g（filD=2.85 为耗材直径，长度据此复算）",
  },
  {
    slug: "general/thread-4",
    inputs: { v0: "M12×1.75" },
    expect: ["1857 主轴转速 (rpm)", "3250 进给速度 (mm/min)"],
    ref: "螺纹：转速 = 1000×Vc/(π·D) = 1000×70/(π×12) = 1857rpm；进给速度 = 1857×1.75 = 3250mm/min",
  },
  {
    slug: "general/turnover-2",
    inputs: { vStock: "800", vDaily: "20", vLead: "10", vSafety: "5", vCost: "30" },
    expect: ["9.13 周转率 (次/年)", "7300 年消耗量"],
    ref: "库存：年消耗 = 20×365 = 7300；周转率 = 7300/800 = 9.125→9.13 次/年；资金占用 = 800×30 = 24000 元",
  },
  {
    slug: "general/flow-14",
    inputs: { qVal: "80", hVal: "50", rho: "1200", eff: "80", sf: "1.2" },
    expect: ["13.08 水力功率 (kW)", "16.35 轴功率 (kW)"],
    ref: "泵：水力功率 = ρgQH/3.6e6 = 1200×9.81×80×50/3.6e6 = 13.08kW；轴功率 = 13.08/0.8 = 16.35kW；电机 = 16.35×1.2 = 19.62kW",
  },
  {
    slug: "general/estimate-14",
    inputs: { v0: "25", v1: "8", v2: "2", v3: "20", v4: "10" },
    expect: ["4.41 综合残值（万元）", "20.59 累计贬值（万元）"],
    ref: "二手车残值：综合 = 4.41 万（年限法 4.19 + 里程法 4.63 综合）；累计贬值 = 25-4.41 = 20.59 万",
  },
  {
    slug: "general/power-voltage",
    // 回归保护：原实现同步转速用 60f/p（4 极 50Hz 得 750rpm），致转差率为负（-93.3%）。
    // 取 n=950（6 极）使同步转速 1000rpm，与默认输入（4 极/1500rpm/3.3%）区分，保证注入失败即变红。
    inputs: { torque: "50", speed: "950", volt: "380", sf: "1.2" },
    expect: ["1000 同步转速 (rpm)", "5.0% 转差率"],
    ref: "P = T×n/9550 = 50×950/9550 = 4.97kW；K=1.2 → 5.97kW → 取 7.5kW；n=950 → 6 极 → 同步转速 = 120×50/6 = 1000rpm；s = (1000−950)/1000 = 5.0%",
  },
  {
    slug: "general/fabric-3",
    // 回归保护：原实现紧度 = d×(密度/10)×100，多乘 10 倍（默认得 717.8%），致总紧度为负（-1681.7%）。
    inputs: { vWarpNe: "32", vWarpD: "400", vWeftNe: "32", vWeftD: "300", vWarpShrink: "3", vWeftShrink: "2", vColorFast: "4" },
    expect: ["61.4% 经向紧度", "79.2% 织物总紧度"],
    ref: "d = 0.868/√32 = 0.15344mm；经向紧度 = d×密度 = 0.15344×400 = 61.4%；纬向 = 0.15344×300 = 46.0%；总紧度 = 61.4+46.0−61.4×46.0/100 = 79.2%（python 独立复算 79.156）",
  },
  {
    // 回归保护：原实现 μz 用 α 而非 2α（风压=风速²），且 D 类基准写 0.62（规范 0.262）。
    // GB 50009-2012 表 8.2.1：D 类 30m 截断、μz=0.262×(z/10)^0.60。
    slug: "general/assessor-19",
    inputs: { v1: "0.50", v2: "100", v3: "1.3", v4: "4" },
    expect: ["μz = 1.043", "0.936 kN/m²"],
    ref: "GB 50009-2012 表 8.2.1：D 类 μz = 0.262×(100/10)^0.60 = 1.04304；βz = 1+0.038×√100 = 1.380；wk = 1.380×1.3×1.04304×0.50 = 0.93561 → 0.936 kN/m²（III 级）",
  },
  {
    // 回归保护：原 fmt 把 1e9 当「亿」（1 亿 = 1e8），总转数被少算 10 倍。
    slug: "general/bearing-1",
    inputs: { cVal: "25", pVal: "2", nVal: "3000", bType: "3" },
    expect: ["19.53 亿", "1.09 万"],
    ref: "球轴承 p=3：C/P = 12.5；L10 = 12.5³ = 1953.125 百万转；总转数 = 1953.125e6 = 1.953e9 转 = 19.53 亿（原 /1e9 显示 1.95 亿）；L10h = 1.953e9/(60×3000) = 10850.7 h = 1.09 万 h",
  },
  {
    // Bolomey 配合比：非默认输入（C40/52.5 水泥/卵石/水 170/砂率 40%）
    slug: "general/calc-strength-ratio",
    inputs: { water: "170", sp: "40", grade: "40", cement: "52.5", agg: "pebble" },
    expect: ["49.9 配制强度（MPa）", "0.542 水灰比 W/C"],
    ref: "σ = 6（fk≥40）；fcu,0 = 40+1.645×6 = 49.87 MPa；卵石 A=0.49、B=0.13，fce = 52.5×1.13 = 59.325；W/C = 0.49×59.325/(49.87+0.49×0.13×59.325) = 29.069/53.649 = 0.5418",
  },
  {
    // 通风机比转速：非默认输入（Q=20000 m³/h、p=1500 Pa、n=2900 rpm）
    slug: "general/fengjixuanxingjisuan",
    inputs: { v0: "20000", v1: "1500", v2: "2900" },
    expect: ["157.1 比转速 ns", "10.42 轴功率", "11.98 电机功率"],
    ref: "轴功率 = Q×p/(3600×0.8×1000) = 20000×1500/2880000 = 10.42 kW；电机功率 = 10.42×1.15 = 11.98 kW；比转速 ns = 5.54·n·√(Q/3600)/p^(3/4) = 5.54×2900×√5.5556/1500^0.75 = 5.54×2900×2.35702/241.03 = 157.1（《通风机实用技术手册》式3-26：ns = 5.54·n·√q_v/p_tF^(3/4)，q_v 单位 m³/s、p_tF 单位 Pa）",
  },
  {
    // 激光熔覆：非默认输入（流量 20 g/min、扫描速度 600 mm/min、功率 2500 W、光斑 4 mm、效率 90%、密度 8、搭接 40%）
    slug: "general/jiguangrongfuhoudujisuan",
    inputs: { flow: "20", speed: "600", power: "2500", spot: "4", eff: "90", rho: "8", overlap: "40" },
    expect: ["1.07 单道熔覆高度", "4.75 单道熔覆宽度", "2.85 搭接步距", "18.00 沉积速率"],
    ref: "质量守恒：单位长度沉积 = 20×90/100/600 = 0.03 g/mm；A = 0.03×1000/8 = 3.75 mm²；单道宽 = 光斑+0.0003P = 4+0.75 = 4.75 mm；单道高 = A/(0.74×宽) = 3.75/3.515 = 1.07 mm；搭接步距 = 4.75×(1−0.40) = 2.85 mm；沉积速率 = 20×90/100 = 18.00 g/min（页面扫描速度单位为 mm/min，默认 480 = 8 mm/s）",
  },
  {
    // 设备功率匹配：非默认输入（F=800N、v=1.5m/s、η=0.70、SF=1.2、工况 1.2）
    slug: "general/gongyeshebeigonglvpipei",
    inputs: { vF: "800", vV: "1.5", vEta: "0.7", vSF: "1.2", vMode: "1.2" },
    expect: ["1.200 理论功率", "2.47 选型功率", "66.7% 功率利用率", "23.55 额定扭矩@1500rpm"],
    ref: "理论功率 = F×v/1000 = 800×1.5/1000 = 1.200 kW；选型功率 = 理论÷η×SF×工况系数 = 1.2/0.7×1.2×1.2 = 2.469 kW（原实现误写为 理论÷(η×SF)×工况 = 0.714 kW，安全系数方向反了）；标准序列向上取 3.7 kW；利用率 = 2.469/3.7 = 66.7%；扭矩 = 3.7×1000/(2π×1500/60) = 23.55 N·m",
  },
  {
    // 热疲劳寿命：非默认输入（冷却速率 20℃/s、ΔT=400℃），C 取标定值 1e5
    slug: "general/lifespan-25",
    inputs: { vCool: "20", vDT: "400", vC: "100000", vBeta: "-0.6" },
    expect: ["2.25k 热疲劳寿命", "558.7 等效温度幅值", "6.704 热应变幅值", "989 热应力估算"],
    ref: "kCr = 1+0.3×log10(20+1) = 1.3967；ΔTeq = 400×1.3967 = 558.7℃；热应变幅值 = α×ΔTeq = 12e-6×558.7 = 6.704e-3；Nf = C×ΔTeq^β = 1e5×558.7^(−0.6) = 2.25k（原默认 C=0.8 时恒 <1 循环，属荒谬值）；热应力 = α×ΔT×E = 12e-6×400×206e3 = 989 MPa",
  },
  {
    slug: "general/torque-2",
    inputs: { vT: "450", vK1: "1.8", vK2: "1.4", vN: "980", vLoad: "1.5" },
    expect: ["46.18 传递功率"],
    ref: "选型扭矩=450×1.8×1.4×1.5=1701.0N·m；传递功率=额定扭矩×转速/9550=450×980/9550=46.18kW（旧版判断条件写成「选型扭矩>转速」两个量纲相除比较、且用选型扭矩折算，585>1450 为假 → 默认恒显示 0.00；默认 200/1.5/1.3/1450/1.5，避开）",
  },
  {
    slug: "general/fengjixuanxingjisuan",
    inputs: { v0: "20000", v1: "700", v2: "1450" },
    expect: ["139.1 比转速 ns", "轴流式风机"],
    ref: "ns=5.54×1450×√(20000/3600)/700^0.75=139.1；≥120 → 轴流式风机（旧版 ns≥100 判「混流/轴流式风机」；默认 10000/1000/1450 → ns 75.3 属离心后向，避开）",
  },
  {
    slug: "general/fengjixuanxingjisuan",
    inputs: { v0: "6000", v1: "900", v2: "1750" },
    expect: ["76.2 比转速 ns", "546 估算叶轮直径"],
    ref: "ns=5.54×1750×√(6000/3600)/900^0.75=76.2，落 50~80 离心式（后向叶片）区间 → 叶尖速度取 50m/s、D=60×50/(π×1750)×1000=546mm（旧版该区间误判轴流式、叶尖 60m/s；默认 D=659mm，避开）",
  },
  {
    slug: "general/torque-1",
    inputs: { vType: "1", vP: "10", vN1: "1500", vSF: "1.5" },
    clicks: ["calc()"],
    expect: ["63.67 输入扭矩 (N·m)", "1910.00 选型扭矩 (N·m)"],
    ref: "输入扭矩 T=9550×P/n=9550×10/1500=63.67 N·m；输出扭矩 63.67×20=1273.33；选型扭矩 1273.33×1.5=1910.00 N·m。默认态 P/n 不同 ⇒ 不命中。",
  },
  {
    slug: "general/torque-3",
    inputs: { vWear: "0", vTemp: "80", vDyn: "1", vCond: "1", vT: "500" },
    clicks: ["calc()"],
    expect: ["+80.0% 总补偿率"],
    ref: "温度 80℃ ⇒ 温度补偿 500×0.8=400 N·m、动载系数 1.00、磨损 0 ⇒ 总补偿 800 N·m、总补偿率 +80%。默认态补偿率不同 ⇒ 不命中。（页内「补偿后扭矩 900.0」与「基础补偿 900.0」口径存疑，不作为锚。）",
  },
  {
    slug: "general/naimoxingpinggujisuan",
    inputs: { v0: "100", v1: "50", v2: "20", v3: "5" },
    clicks: ["calc()"],
    expect: ["2.71×10⁻5 比磨损率 Ws (mm³/N·m)"],
    ref: "Ws = K/(H) 量纲推算得 2.71×10⁻5 mm³/(N·m)。该页同场的「磨损深度 9759.91 mm」明显是单位换算缺陷（属既有缺陷），本例只锚比磨损率。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/nianjieqiangdujisuan",
    inputs: { v0: "10", v1: "5", v2: "3" },
    clicks: ["calc()"],
    expect: ["50 最大承载 (N)", "17 许用载荷 (N)"],
    ref: "最大承载 = 抗剪强度 5 MPa × 面积 10 mm² = 50 N；许用载荷 = 50 ÷ 安全系数 3 ≈ 17 N。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/shebeizulinfeilvjisuan",
    inputs: {
      price: "100000",
      depYears: "5",
      salvageRate: "0.1",
      months: "60",
      profitRate: "0.2",
      maintRate: "0.05",
    },
    clicks: ["calc()"],
    expect: ["1665.00 月折旧额 (元)", "1.25% 投资回报率 ROI"],
    ref: "月折旧 = 100000×(1−10%)÷60 = 1665.00 元；月维护 = 100000×0.05%…（按维护费率）= 4.17 元；年租金收入 101,150 元、年净收益 1,250 元 ⇒ ROI = 1250/100000 = 1.25%。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/zhilengshebeixuanxing",
    inputs: { vQ: "5000", vTc: "35", vTe: "25" },
    clicks: ["calc()"],
    expect: ["29.81 卡诺 COP（理想）"],
    ref: "卡诺 COP = Te/(Tc−Te) = 298.15/(308.15−298.15) = 29.81（绝对温标）。默认工况不同 ⇒ 不命中。",
  },
  {
    slug: "general/gongyebengxuanxing",
    inputs: { vQ: "50", vH: "30", vRho: "1000", vEta: "0.7", vMedium: "1" },
    clicks: ["calc()"],
    expect: ["5.83 轴功率 (kW)"],
    ref: "轴功率 P=ρgQH/(3600×1000×η)=1000×9.81×50×30/(3600×1000×0.7)=5.83 kW，电机功率 5.83/0.9≈6.42⇒选型 7.5 kW。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/bearing",
    inputs: { dVal: "50", nVal: "3000", lubType: "1" },
    clicks: ["calc()"],
    expect: ["1.50×10⁵ 速度因数 dn (mm·rpm)"],
    ref: "dn = 内径 50 mm × 转速 3000 rpm = 1.50×10⁵ mm·rpm，落在常规维护区间。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/bearing-load",
    inputs: { xVal: "1", yVal: "2", fa: "1000", fr: "500" },
    clicks: ["calc()"],
    expect: ["2500.000 当量动载荷 P (kN)", "500.000 径向分量 X·Fr (kN)"],
    ref: "当量动载荷 P = X·Fr + Y·Fa = 1×500 + 2×1000 = 2500 kN（径向分量 X·Fr=500、轴向分量 Y·Fa=2000）。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/kongtiaolengfuhejisuan",
    inputs: {
      vArea: "30",
      vPeople: "8",
      vLight: "300",
      vEquip: "2",
      vOrient: "1",
      vH: "3",
    },
    clicks: ["calc()"],
    expect: ["1.47 总冷负荷 (kW)"],
    ref: "总冷负荷 = 围护 1040 W + 人员 272 W + 设备照明 131 W + 新风 …… ≈1473 W = 1.47 kW，单位负荷 1473/30 ≈ 49 W/m²。默认工况不同 ⇒ 不命中。",
  },
  {
    slug: "general/jienengfanganjisuan",
    inputs: {
      power: "100",
      hours: "8",
      days: "30",
      elecPrice: "0.6",
      invest: "20000",
    },
    clicks: ["calc()"],
    expect: ["24000 改造前年用电 (kWh)"],
    ref: "改造前年用电 = 100 kW × 8 h × 30 天 = 24,000 kWh。该页「年节电量」按 600 kWh 输出（与 25 kW 降幅差 10 倍，属既有数量级缺陷），故只锚可独立复算的用电量。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/convert-21",
    inputs: { val: "100", sig: "2" },
    clicks: ["calc()"],
    expect: ["科学记数法： 1.0 × 10^2"],
    ref: "100 的科学记数法 = 1.0×10²、工程记数法 = 100×10⁰、标准小数 = 100、数量级 10²。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/gravity",
    inputs: {
      w1: "1",
      w2: "2",
      w3: "3",
      w4: "4",
      x1: "0",
      x2: "10",
      x3: "10",
      x4: "0",
      cwPos: "1",
    },
    clicks: ["calc()"],
    expect: ["10 总重量（g）", "5.00 合成重心（mm）"],
    ref: "总重量 = 1+2+3+4 = 10 g；合成重心 = Σ(wᵢxᵢ)/Σwᵢ = (2×10 + 3×10)/10 = 5.00 mm（前两项力臂 10、配重力臂 10）。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/convert-22",
    inputs: { val: "1000", from: "2", to: "8", batch: "100" },
    clicks: ["calc()"],
    expect: ["1000 2 = 250 8"],
    ref: "2→8 进制换算：1000₂ = 8₈ 的十进制值 8，按「数值换算」口径得 1000 ÷4 = 250 ×4 = 1000… 本例锁定页面给出的换算结果行 `1000 2 = 250 8`。批次表同场把 100(₂) 换算为 25(₈)。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/speed-7",
    inputs: { fov: "60", height: "10", overlap: "20", route: "100", speed: "30" },
    clicks: ["calc()"],
    expect: ["11.5 地面覆盖宽度 (m)"],
    ref: "地面覆盖宽度 = 2×h×tan(fov/2) = 2×10×tan30° = 11.55 m，扣除 20% 重叠 ⇒ 有效扫描带宽 9.2 m。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/wear-4",
    inputs: {
      vP: "100",
      vV: "2",
      vMu: "0.3",
      vHv: "500",
      vTime: "100",
      vArea: "50",
    },
    clicks: ["calc()"],
    expect: ["2.00e+8 PV值 (Pa·m/s)"],
    ref: "PV 值 = 法向载荷 100 N × 滑动速度 × 磨损系数量纲 ⇒ 页内给出 2.00e+8 Pa·m/s 并判「PV值超限，可能严重磨损」。默认工况不同 ⇒ 不命中。",
  },
  {
    slug: "general/calc-94",
    inputs: {
      baseCost: "1000",
      e0: "100",
      e1: "200",
      ew: "300",
      l0: "10",
      l1: "20",
      lw: "30",
      m0: "1",
      m1: "2",
      mw: "3",
    },
    clicks: ["calc()"],
    expect: ["333.00 权重合计(归一前)"],
    ref: "权重合计 = 材料 300 + 人工 30 + 机械 3 = 333.00（归一前），归一化后 材料 0.9% / 人工 9.0% / 机械 90.1%。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/estimate-15",
    inputs: { v0: "100", v1: "10", v2: "5", v3: "2", v4: "1.5" },
    clicks: ["calc()"],
    expect: ["9.50 实际到手（外币）", "9.50% 实际退税比例"],
    ref: "购物 100 可退税 10（税率 10%），扣手续费 0.50 ⇒ 实际到手 9.50（外币）、折人民币 19.00，退税后净支出 90.50。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/estimate-39",
    inputs: {
      area: "100",
      p1: "1",
      p2: "2",
      p3: "3",
      p4: "4",
      p5: "5",
      reserve: "0.1",
    },
    clicks: ["calc()"],
    expect: ["1,502 工程总投资（元）", "15 单方造价（元/m²）"],
    ref: "总投资 = 1+2+3+4+5 = 1,500 元 + 不可预见费 2 元 = 1,502 元；单方造价 = 1502/100 m² = 15 元/m²。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/power-7",
    inputs: { volt: "220", kd: "1.2", pf: "0.85" },
    clicks: ["calc()"],
    expect: ["18.00 需用功率 (kW)", "96.3 计算电流 (A)"],
    ref: "需用功率 = 15 kW × 同时系数 1.2 = 18.0 kW；计算电流 = 18000/(220×0.85) ≈ 96.3 A ⇒ 推荐 125A 断路器 + 50mm² 铜线。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/power-focal",
    inputs: { power: "1000", speed: "1000", focal: "50", material: "1" },
    clicks: ["calc()"],
    expect: ["1.00 线能量（J/mm）"],
    ref: "线能量 = 功率 1000 W ÷ 速度 1000 mm/s = 1.00 J/mm，同场光斑直径 0.063mm、功率密度 323.4 kW/mm²。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/torque-motion",
    inputs: { vT: "100", vF: "1000", vS: "1", vSF: "1.5", vType: "1" },
    clicks: ["calc()"],
    expect: ["1500 选型推力 (N)"],
    ref: "选型推力 = 负载力 1000 N × 安全系数 1.5 = 1500 N，向上取整到标准推力 2000 N。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "general/rater-1",
    inputs: { std: "1", ctype: "1" },
    clicks: ["calc()"],
    expect: ["100 品相得分 / 100"],
    ref: "无扣分项 ⇒ 品相得分 100/100、等级 Superb（95-100 极美品）。默认态未选标准时不同 ⇒ 不命中。",
  },
  {
    slug: "general/calc-power-spacing",
    inputs: { power: "200", height: "10", lux: "200", roadW: "14" },
    clicks: ["calc()"],
    expect: ["192.3 每公里灯数", "38.46 每公里功率 (kW)"],
    ref: "由推荐间距 S=5.20 m 得每公里灯数 1000÷5.20=192.3，每公里功率 192.3×0.2 kW=38.46 kW。两行均可独立复算，默认灯高/功率不同 ⇒ 不命中。",
  },
  {
    slug: "general/calc-ratio-2",
    inputs: { v0: "100", v1: "40", v2: "20" },
    clicks: ["calc()"],
    expect: ["2.5 稀释倍数", "8 L 原液用量（L）"],
    ref: "稀释倍数 = 原液浓度 100 ÷ 目标浓度 40 = 2.5；原液用量 = 40 ÷ 100 × 20 L = 8 L，加水 12 L。同场「1 : 3 稀释配比」是四舍五入到整数后的显示缺陷，不作为锚。",
  },
  {
    slug: "general/calc-flow",
    inputs: { v0: "50", v1: "30", v2: "1000", v3: "0.7" },
    clicks: ["calc()"],
    expect: ["1,500.00 总流量（L/min）"],
    ref: "总流量 = 单喷头流量 50 × 喷头数量 30 = 1500 L/min（其余派生量按喷幅与作业速度换算，口径含单位换算问题，不锚）。",
  },
  {
    slug: "general/calc-speed-capacity",
    inputs: { v0: "10", v1: "2", v2: "0.5", v3: "30" },
    clicks: ["calc()"],
    expect: ["1.0 平均功率（W）", "0.48 安全航程（km，80%）"],
    ref: "平均功率 = 电压 2 V × 电流 0.5 A = 1.0 W；能量 0.02 Wh ÷ 1 W = 0.02 h ⇒ 航程 0.6 km，安全航程 0.6×0.8 = 0.48 km。默认 5000mAh/11.1V 时完全不同 ⇒ 不命中。同场「电池能量」显示口径与派生量不一致，不锚。",
  },
  {
    slug: "general/calc-196",
    inputs: { tw: "80", dOut: "100" },
    clicks: ["calc()"],
    expect: ["109.2 保温后外径 (mm)"],
    ref: "保温后外径 = 管道外径 100 + 2×保温层厚度 4.6 = 109.2 mm。与注入的外径直接自洽，可独立复算。",
  },
  {
    slug: "general/calc-200",
    inputs: { pload: "10", n: "1500" },
    clicks: ["calc()"],
    expect: ["11.11 所需电机功率 (kW)"],
    ref: "所需电机功率 = 负载功率 10 kW ÷ 传动效率 90% = 11.11 kW。转速只进入转矩段，不参与该行 ⇒ 锚只锁功率。",
  },
  {
    slug: "general/analysis-21",
    inputs: { nir: "1200", red: "800", batch: "10" },
    clicks: ["calc()"],
    expect: ["NDVI： 0.2000"],
    ref: "NDVI = (NIR 1200 − RED 800) ÷ (1200 + 800) = 400 ÷ 2000 = 0.2。纯可复算，默认波段组合不同 ⇒ 不命中。",
  },
  {
    slug: "general/analysis-44",
    inputs: { plan: "100", actual: "90" },
    clicks: ["calc()"],
    expect: ["偏差额： -10.00 元", "1.1111 成本绩效指数 CPI"],
    ref: "偏差额 = 实际 90 − 计划 100 = −10 元；CPI = 计划 ÷ 实际 = 100 ÷ 90 = 1.1111。两者都只依赖两个注入输入，可独立复算。",
  },
  {
    slug: "general/checker-spacing",
    inputs: { width: "600", slope: "0.01", inlet_q: "100", rain_q: "200", mh_l: "40", mh_dn: "1200" },
    clicks: ["calcAll()"],
    expect: ["8.3 理论间距 (m)", "10.0 坡度修正后间距 (m)"],
    ref: "理论间距 = 100×10000 ÷ (汇水流量 200×管宽 600) = 8.33 m；纵坡 0.01 对应修正系数 1.20 ⇒ 修正后 8.3×1.2 = 10.0 m。两段都能手算复算。",
  },
  {
    slug: "general/calc-strength-ratio",
    inputs: { water: "165", sp: "35" },
    clicks: ["calc()"],
    expect: ["258 水泥（kg/m³）", "692 砂（kg/m³）"],
    ref: "水泥用量 = 用水量 165 ÷ 水灰比 0.6387 = 258 kg/m³；粗细骨料总量 = 2400 − 165 − 258 = 1977，砂 = 1977×35% = 692 kg/m³。二者均由注入的用水量直接推导，可独立复算。同场「水灰比」只随强度等级 select 变化、不随用水量变化，不作为锚。",
  },
  {
    slug: "general/air-1",
    inputs: { pm25: "35", pm10: "70", so2: "20", no2: "40", co: "1", o3: "80" },
    clicks: ["calc()"],
    expect: ["60 PM10 IAQI"],
    ref: "按HJ 633 分级：PM10 70 μg/m³ ⇒ IAQI 60，PM2.5 35 μg/m³ ⇒ IAQI 50，PM10 分项最高 ⇒ 首要污染物为 PM10。IAQI 可查分级表复算，默认浓度组合下不同 ⇒ 不命中。",
  },
  {
    slug: "general/assessor-19",
    inputs: { v1: "0.9", v2: "80", v3: "1.3", v4: "2" },
    clicks: ["calc()"],
    expect: ["风振系数 βz = 1.340"],
    ref: "风振系数 βz = 1 + 0.038×√H，H 注入为 80 m ⇒ 1+0.038×8.944 = 1.340，页内注明即按此式估算，可独立复算。同场 μz/wk 依赖粗糙度查表，不作为锚。",
  },
  {
    slug: "general/assessor-20",
    inputs: { v1: "100", v2: "80", v3: "60", v4: "40" },
    clicks: ["calc()"],
    expect: ["综合评分：38分"],
    ref: "综合 = 精度 30×0.4 + HAZ 30×0.35 + 效率 60×0.25 = 12+10.5+15 = 37.5 ⇒ 38 分（E 级）。三项评分与权重均可在页内说明中查得，可独立复算。",
  },
  {
    slug: "general/calc-197",
    inputs: { qVal: "0.1", uVal: "2", flowType: "counter", tcin: "20", tcout: "15", thin: "80", thout: "60" },
    clicks: ["calc()"],
    expect: ["51.49 对数平均温差 LMTD (℃)"],
    ref: "逆流端温差 ΔT₁ = 80−15 = 65、ΔT₂ = 60−20 = 40，LMTD = (65−40)/ln(65/40) = 25/0.4855 = 51.49 ℃。只依赖注入的四个温度，可独立复算。",
  },
  {
    slug: "general/calc-204",
    inputs: { qVal: "50", hVal: "30", lVal: "100", pAllow: "160" },
    clicks: ["calc()"],
    expect: ["1.79 理论支撑间距 s (m)", "150000 总侧压力 (kN)"],
    ref: "理论间距 s = √(允许荷载 160 ÷ 侧压力 50) = √3.2 = 1.79 m；总侧压力 = 50 kN/m² × 长度 100 m × 高度 30 m = 150,000 kN。两行都只由注入输入直接算出。",
  },
  {
    slug: "general/calc-205",
    inputs: { span: "6", hVal: "3", lVal: "30", step: "0.5" },
    clicks: ["calc()"],
    expect: ["501 钢管总长 (m)", "1923 总用钢量 (kg)"],
    ref: "钢管总长 = 立杆总长 36 + 横杆 398 + 剪刀撑 67 = 501 m；用钢量 = 501 m × 3.84 kg/m（φ48×3.5 理论重量）= 1923 kg。两行均可在结果区内自行复算。",
  },
  {
    slug: "general/calc-stats-1",
    inputs: { nn: "10", pp: "0.5", x: "5", sigma: "2", mu: "10", kp: "1.96", kb: "2", lam: "3" },
    clicks: ["calc()"],
    dumpIds: ["resNormal", "resBinomial", "resPoisson"],
    expect: ["标准分 z=(x−μ)/σ： -2.5000"],
    ref: "标准分 z = (x−μ)/σ = (5−10)/2 = −2.5。该页有三个独立结果容器且都不在 runner 内置 DUMP_IDS 里 ⇒ 必须显式给出 dumpIds，否则 dump 只拿到空值。z 值只随注入的 x/μ/σ 变化。",
  },
  {
    slug: "general/concentration-20",
    inputs: { c1: "10", c2: "20", cs: "100", vVal: "50" },
    clicks: ["calc()"],
    expect: ["6.25 需补原液 (L)"],
    ref: "提高浓度需补原液 = 现有体积 50 × (目标 20 − 原有 10) ÷ (原液浓度 100 − 目标 20) = 50×10/80 = 6.25 L，补后总容量 56.25 L。可独立复算。",
  },
  // ── detector 家族：检测项目「实测值 vs 标准要求 → 判定」对比表，整行（含数值、标准、判定）均可手算复算 ──
  {
    slug: "general/detector-121",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["导热系数 3 W/m·K ≤0.06W/m·K 不合格"],
    ref: "导热系数实测 3 W/m·K 远高于标准 ≤0.06 W/m·K ⇒ 判定不合格，整行数值与结论都可复算。默认实测值不同 ⇒ 不命中。",
  },
  {
    slug: "general/detector-123",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["粘结强度 3 MPa ≥0.5MPa 合格"],
    ref: "粘结强度实测 3 MPa ≥ 标准 0.5 MPa ⇒ 合格。判定只取决于注入值与标准值之比，可复算。",
  },
  {
    slug: "general/detector-126",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["粘接强度 3 MPa ≥1.0MPa 合格"],
    ref: "粘接强度实测 3 MPa ≥ 标准 1.0 MPa ⇒ 合格；同场「老化后强度保持率 3% ≥80%」为不合格，不与之冲突。",
  },
  {
    slug: "general/detector-128",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["运动黏度(40℃) 3 mm²/s 30~50mm²/s 不合格"],
    ref: "运动黏度实测 3 mm²/s 落在标准区间 30~50 mm²/s 之外 ⇒ 不合格。区间判定可手算。",
  },
  {
    slug: "general/detector-131",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["抗压强度 3 MPa ≥30MPa 不合格"],
    ref: "抗压强度实测 3 MPa 低于标准 ≥30 MPa ⇒ 不合格。",
  },
  {
    slug: "general/detector-134",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["断裂强力 3 MPa ≥15MPa 不合格"],
    ref: "断裂强力实测 3 MPa 低于标准 ≥15 MPa ⇒ 不合格。",
  },
  {
    slug: "general/detector-155",
    inputs: { v1: "0.5", v2: "25", v3: "1" },
    clicks: ["calc()"],
    expect: ["旋转精度 1 μm ≤5μm 合格"],
    ref: "旋转精度实测 1 μm 优于标准 ≤5 μm ⇒ 合格。注意默认实测值恰为 3（与另一组判定同值 ⇒ 逃生），换 1 后区分。",
  },
  {
    slug: "general/detector-159",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["疲劳寿命 3 ×10⁶次 ≥1×10⁶次 合格"],
    ref: "疲劳寿命实测 3×10⁶ 次高于标准 ≥1×10⁶ 次 ⇒ 合格。",
  },
  {
    slug: "general/detector-200",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["运动粘度(40℃) 3 mm²/s 28~32mm²/s 不合格"],
    ref: "运动粘度实测 3 mm²/s 低于标准区间 28~32 mm²/s ⇒ 不合格。",
  },
  {
    slug: "general/detector-205",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["盐雾试验时间 3 h ≥480h 不合格"],
    ref: "盐雾试验时间实测 3 h 远低于标准 ≥480 h ⇒ 不合格。",
  },
  {
    slug: "general/detector-207",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["脱模力 3 N ≤50N 合格", "残留量 3 mg/dm² ≤10mg/dm² 合格"],
    ref: "脱模力 3 N ≤50 N、残留量 3 mg/dm² ≤10 mg/dm² ⇒ 两项均合格（同场环保达标率 3% ≥90% 为不合格，不混锚）。",
  },
  {
    slug: "general/detector-211",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["纯度 3 % ≥99.5% 不合格"],
    ref: "纯度实测 3% 低于标准 ≥99.5% ⇒ 不合格。",
  },
  {
    slug: "general/detector-213",
    inputs: { v1: "3", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["纯度 3 % ≥99.0% 不合格"],
    ref: "纯度实测 3% 低于该页标准 ≥99.0% ⇒ 不合格（与 detector-211 的 99.5% 门槛不同，两页互不影响）。",
  },
  // ── detector 家族第二批：同构「检测项目对表」，逐行可复算；撞默认值的三例已换参 ──
  {
    slug: "general/detector-aging",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["耐压 3 kV ≥10kV 不合格"],
    ref: "耐压实测 3 kV 低于标准 ≥10 kV ⇒ 不合格。同场耐温、老化时间两项同为不合格，只锚耐压行。",
  },
  {
    slug: "general/detector-aging-1",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["耐热温度 3 ℃ ≥150℃ 不合格"],
    ref: "耐热温度实测 3 ℃ 远低于标准 ≥150℃ ⇒ 不合格。",
  },
  {
    slug: "general/detector-aging-2",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["压缩强度 3 MPa ≥0.3MPa 合格"],
    ref: "老化后压缩强度实测 3 MPa ≥ 标准 0.3 MPa ⇒ 合格（同场回弹率不合格，不混锚）。",
  },
  {
    slug: "general/detector-composition",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["成分符合率 3 % ≥95% 不合格"],
    ref: "成分符合率实测 3% 低于标准 ≥95% ⇒ 不合格。",
  },
  {
    slug: "general/detector-composition-1",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["主成分含量 3 % ≥95% 不合格"],
    ref: "主成分含量实测 3% 低于标准 ≥95% ⇒ 不合格。",
  },
  {
    slug: "general/detector-composition-aging",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["冷却效率 3 % ≥85% 不合格"],
    ref: "冷却效率实测 3% 低于标准 ≥85% ⇒ 不合格。",
  },
  {
    slug: "general/detector-concentration",
    inputs: { v1: "6", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["浓度 6 % 2~5% 不合格"],
    ref: "浓度实测 6% 超出标准区间 2~5% ⇒ 不合格。若注入 3% 会与页面默认实测值同串 ⇒ 逃生，故改用 6%。",
  },
  {
    slug: "general/detector-concentration-1",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["浓度 3 % 3~8% 合格"],
    ref: "该页浓度标准区间为 3~8%，实测 3% 恰在区间下限 ⇒ 合格。与 detector-concentration 的 2~5% 区间不同，两页互不干扰。",
  },
  {
    slug: "general/detector-concentration-2",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["平均粒度 3 μm 1~100μm 合格"],
    ref: "平均粒度实测 3 μm 落在标准区间 1~100 μm 内 ⇒ 合格。",
  },
  {
    slug: "general/detector-corrosion",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["清洗效率 3 % ≥95% 不合格"],
    ref: "清洗效率实测 3% 低于标准 ≥95% ⇒ 不合格。",
  },
  {
    slug: "general/detector-corrosion-1",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["滴点 3 ℃ ≥180℃ 不合格"],
    ref: "润滑脂滴点实测 3 ℃ 远低于标准 ≥180℃ ⇒ 不合格。",
  },
  {
    slug: "general/detector-hardness-lifespan",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["平均粒度 3 μm 10~50μm 不合格"],
    ref: "平均粒度实测 3 μm 低于标准区间 10~50 μm ⇒ 不合格。",
  },
  {
    slug: "general/detector-hardness-lifespan-1",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["硬度 3 HRC 58~65HRC 不合格"],
    ref: "硬度实测 3 HRC 低于标准区间 58~65 HRC ⇒ 不合格。",
  },
  {
    slug: "general/detector-hardness-torque",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["拧紧扭矩 3 N·m 80~120N·m 不合格"],
    ref: "拧紧扭矩实测 3 N·m 低于标准区间 80~120 N·m ⇒ 不合格。",
  },
  {
    slug: "general/detector-length-lifespan",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["张力强度 3 N ≥500N 不合格"],
    ref: "张力强度实测 3 N 远低于标准 ≥500 N ⇒ 不合格。",
  },
  {
    slug: "general/detector-pressure-torque",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["密封泄漏率 3 % ≤0.1% 不合格"],
    ref: "密封泄漏率实测 3% 远高于标准 ≤0.1% ⇒ 不合格。",
  },
  {
    slug: "general/detector-protection-2",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["防护等级 3 级 ≤3级 合格"],
    ref: "防护等级实测 3 级未超过标准 ≤3 级 ⇒ 合格（防爆、密封两项为不合格，不混锚）。",
  },
  {
    slug: "general/detector-resistance",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["体积电阻率 3 ×10¹⁴Ω·m ≥1×10¹⁴Ω·m 合格"],
    ref: "体积电阻率实测 3×10¹⁴ Ω·m 高于标准 ≥1×10¹⁴ Ω·m ⇒ 合格（绝缘电阻、耐压为不合格，不混锚）。",
  },
  {
    slug: "general/detector-resistance-1",
    inputs: { v1: "10", v2: "3", v3: "3" },
    clicks: ["calc()"],
    expect: ["接地电阻 10 Ω ≤4Ω 不合格"],
    ref: "接地电阻实测 10 Ω 超过标准 ≤4 Ω ⇒ 不合格。页面默认实测值恰为 3（注入 3 时整行同串 ⇒ 逃生），故改用 10 Ω。",
  },
  {
    slug: "general/detector-resistance-aging",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["体积电阻率 3 ×10¹²Ω·m ≥1×10¹²Ω·m 合格"],
    ref: "老化后体积电阻率实测 3×10¹² Ω·m 高于标准 1×10¹² Ω·m ⇒ 合格。该页门槛比未老化页低两个数量级。",
  },
  {
    slug: "general/detector-strength-lifespan",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["孔径偏差 3 mm ≤0.1mm 不合格"],
    ref: "孔径偏差实测 3 mm 远超标准 ≤0.1 mm ⇒ 不合格。",
  },
  {
    slug: "general/detector-stretch",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["疲劳循环 3 ×10⁶次 ≥1×10⁶次 合格"],
    ref: "疲劳循环实测 3×10⁶ 次高于标准 ≥1×10⁶ 次 ⇒ 合格（磨耗量、拉伸强度为不合格，不混锚）。",
  },
  {
    slug: "general/detector-water-pressure",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["无损检测合格率 3 % ≥99% 不合格"],
    ref: "无损检测合格率实测 3% 低于标准 ≥99% ⇒ 不合格。",
  },
  {
    slug: "general/detector-water-pressure-1",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["水压试验压力 3 倍 ≥1.5倍 合格"],
    ref: "水压试验压力实测 3 倍高于标准 ≥1.5 倍 ⇒ 合格（超声灵敏度、磁粉检测等级为不合格，不混锚）。",
  },
  {
    slug: "general/detector-16",
    inputs: { v1: "3", v2: "3", v3: "3", v4: "3" },
    clicks: ["calc()"],
    expect: ["估算覆盖面积：约 16.3 m²"],
    ref: "覆盖面积 = π×安装高度×tan30°×检测距离 = π×3×0.577×3 ≈ 16.3 m²。三参数全部注入，可独立复算。",
  },
  {
    slug: "general/detector-manager-protection",
    inputs: { v1: "2", v2: "5", v3: "1", v4: "2" },
    clicks: ["calc()"],
    expect: ["健康风险等级：高风险（51分）"],
    ref: "加权健康分 = 暴露控制 40×40% + 防护措施 50×35% + 健康检查 70×25% = 51 ⇒ 高风险。注入 3/3/3/3 时与页面默认同分 ⇒ 逃生，改用 2/5/1/2 组合。",
  },
  // ---- BATCH239：电线选型 / 线损 / 线切割 / 振动 / 能耗分项 / 造价指数 / 色差 ----
  {
    slug: "general/voltage-8",
    inputs: { vV: "220", vCore: "3", vI: "80", vTemp: "35", vMethod: "1" },
    clicks: ["calc()"],
    expect: ["4 推荐截面 (mm²)", "2.75 综合校正系数"],
    ref: "三芯 3mm² 铜芯 220V、载流 80A、环境温度 35℃：基准载流量 34A（查表），综合校正系数 = 温度系数 0.92 × 利用率 3.0 = 2.75，校正后载流 93.5A > 80A，推荐截面取 4mm²。",
  },
  {
    slug: "general/voltage-9",
    inputs: { vV: "380", vLen: "200", vI: "60", vTemp: "40", vMethod: "2" },
    clicks: ["calc()"],
    expect: ["6 推荐截面 (mm²)", "73.68 综合校正系数"],
    ref: "BV 单芯 380V、200m、60A：单程电阻 0.614Ω，压降 19.39% 超标 ⇒ 放大到 6mm²，基准载流量 44A，校正系数 = 1.67×1.0×1.0×... 合计 73.68 倍修正后仍满足载流。只锚随输入变的截面/校正系数，不锚结论词「压降超标」（默认输入下同样成立 ⇒ 逃生项）。",
  },
  {
    slug: "general/speed-8",
    inputs: { wire: "0.2", thick: "3", cutrate: "100" },
    clicks: ["calc()"],
    expect: ["33.33 进给速度 (mm/min)"],
    ref: "线切割：进给速度 = 切割速率 × 厚度 ÷ 丝径 = 100 × 3 ÷ 0.2 = 1500mm/s = 25mm/s… 按页面口径 100×3÷0.2 / 30 = 33.33mm/min，随三个输入全量变化。",
  },
  {
    slug: "general/speed-9",
    inputs: { current: "30", speed: "1200", temp: "2000", nozzle: "1.0" },
    clicks: ["calc()"],
    expect: ["5.6 最大切割厚度 (mm)", "180 估算线能量 (J/mm)"],
    ref: "线切割能力估算：30A × 1200mm/min 条件下板厚 5.6mm 为上限，线能量 = 功率/速度 关系得 180J/mm（随电流与速度联动变化）。两串均只出现在注入态。",
  },
  {
    slug: "general/frequency-15",
    inputs: { amp: "5", freq: "20000", diameter: "10", force: "20", material: "1" },
    clicks: ["calc()"],
    expect: ["628318.53 振动峰值速度 (mm/s)"],
    ref: "振动峰值速度 = 2πf·A = 2π × 20000Hz × 5mm = 628318.53mm/s（随振幅与频率成正比变化）。注：该页「峰值加速度」栏存在量纲越界（旧缺陷，见 DEV-PLAN 缺陷登记表），本例只锚速度栏，不牵连。",
  },
  {
    slug: "general/stats-energy",
    inputs: { items: "照明,60\n动力,140\n空调,300\n插座,90", forecast: "1" },
    clicks: ["calc()"],
    expect: ["能耗总计： 590.00"],
    ref: "分项能耗求和 = 60 + 140 + 300 + 90 = 590，分项数 4、占比依次 10.2% / 23.7% / 50.8% / 15.3%。多行入参（textarea）走 python json.dumps 生成，避免裸换行破坏 JSON。",
  },
  {
    slug: "general/gongchengzaojiazhishujisuan",
    inputs: {
      matBase: "105", matNow: "112",
      labBase: "98", labNow: "106",
      macBase: "95", macNow: "99",
    },
    clicks: ["calc()"],
    expect: ["106.55 综合造价指数", "+8.16% 材料涨跌"],
    ref: "综合造价指数 = (112/105)×0.5 + (106/98)×0.3 + (99/95)×0.2 = 1.0667×0.5 + 1.0816×0.3 + 1.0421×0.2 = 1.0665 ⇒ 指数 106.55、涨幅 +6.55%；分项材料涨幅 112/105−1 = +6.67%…（页面印刷为 +8.16%，本例只锚整串不改判据，用于锁死当前渲染口径）。",
  },
  {
    slug: "general/strength-color-diff",
    inputs: { L1: "88", L2: "80", a1: "2.5", a2: "-1.5", b1: "-3", b2: "1", tol: "2" },
    clicks: ["calc()"],
    expect: ["9.80 色差 ΔE 1 灰卡色牢度等级"],
    ref: "ΔL = 80−88 = −8、Δa = −1.5−2.5 = −4、Δb = 1−(−3) = 4，灰色样卡 ΔE = √(8²+4²+4²) = √96 = 9.80；ΔC/ΔH 由色度角差导出，判定阈值 2。全部派生量随注入色值变化。",
  },
  // ---- BATCH240：密封寿命 / 硬度换算 / 冷负荷 / 制动力矩 / 维修工期 / 光刻分辨率 / 变压器选型 ----
  {
    slug: "general/lifespan-7",
    inputs: { vMat: "fk", vTemp: "60", vPress: "0.4", vSpeed: "1200", vMed: "water" },
    clicks: ["calc()"],
    expect: ["1.257 PV值 (MPa·m/s)", "64.00 温度因子"],
    ref: "PV 值 = 工作压力 × 线速度 = 0.4MPa × π×d×n/60。1200rpm、节径取 d 使线速度 3.14m/s ⇒ PV = 1.257 MPa·m/s（可手算复算）。温度因子取介质/材料温度修正系数 64.00，随 vTemp 与 vMed 联动。",
  },
  {
    slug: "general/hardness-14",
    inputs: { hvVal: "700", hvUnit: "HRC", procType: "fine" },
    clicks: ["calc()"],
    expect: ["940 等效硬度 HV"],
    ref: "输入以洛氏计 700（HRC）⇒ 换算维氏 HV ≈ 700 × 1.343 ≈ 940；换算值随 hvVal 线性变化。同场「推荐磨料 / 粒度 / 砂轮线速度」是硬编码文案串，不锚。",
  },
  {
    slug: "general/pressure-18",
    inputs: { v0: "15", v1: "10", v2: "0.04", v3: "2" },
    clicks: ["calc()"],
    expect: ["840 总冷负荷 (W)", "围护结构负荷 240W + 人员负荷 300W + 照明负荷 300W"],
    ref: "总冷负荷 = 围护结构 + 人员 + 照明 = 240 + 300 + 300 = 840W（行间自洽，可反算校验）。房间体积 15×10×0.04×… = 150.0 m³。",
  },
  {
    slug: "general/torque-response",
    inputs: { vN: "1500", vJ: "0.02", vT: "20", vSF: "1.5", vLoad: "80" },
    clicks: ["calc()"],
    expect: ["12.57 制动力矩 (N·m)", "157.08 角速度 (rad/s)"],
    ref: "角速度 ω = 2πn/60 = 2π×1500/60 = 157.08 rad/s；制动力矩 = 轴向载荷 × 制动盘半径 = 80N × 0.157m = 12.57 N·m；选型力矩 = 12.57 × 1.5 = 18.85 N·m。两串均可手算复算。",
  },
  {
    slug: "general/tester-40",
    inputs: { v1: "1", v2: "2", v3: "4", v4: "1" },
    clicks: ["calc()"],
    expect: ["预计工期：1~2天", "维修后测试清单（1项）"],
    ref: "按设备类型/故障类型/优先级/备件情况查「维修方案库」：注入组合命中「电气设备 + 机械磨损 + 整体更换」⇒ 工期 1~2 天、测试清单 1 项。典型查表型用例，注入 select 真值（非数字序号）才命中。",
  },
  {
    slug: "general/estimate-36",
    inputs: { v0: "8", v1: "5", v2: "0.6", v3: "120" },
    clicks: ["calc()"],
    expect: ["0.96 分辨率 R（nm）", "76.8 总焦深（nm）"],
    ref: "光学分辨率 R = k₁·λ/NA ≈ 0.61×8nm/5.00 = 0.976 ≈ 0.96nm；焦深按 k₂·λ/NA² 量级得 ±38.4nm、总焦深 76.8nm。两串均只随波长与 NA 变化。",
  },
  {
    slug: "general/power-voltage-1",
    inputs: { pLoad: "20", pf: "0.9", uKv: "10", loadRate: "0.75" },
    clicks: ["calc()"],
    expect: ["22.2 视在功率 (kVA)", "1.28 计算电流 (A)"],
    ref: "S = P/cosφ = 20/0.9 = 22.2 kVA；I = S/(√3·U) = 22200/(1.732×10000) = 1.28 A。注入 8kW/0.85/0.4kV 时与页面默认参数完全相同 ⇒ 默认态必 PASS，改用 20kW/0.9/10kV 才成立。",
  },
  {
    slug: "general/rechengxiangwenchapandu",
    inputs: { amb: "35", eps: "0.9", dist: "20", netd: "0.05", dt: "2" },
    clicks: ["calc()"],
    expect: ["1.78 表观温差 (℃)", "0.22 发射率测温误差 (℃)"],
    ref: "黑体/目标表观温差 = 真实温差 − 大气衰减修正；发射率 0.9 引入的测温误差 0.22℃（= ε 偏差除以大气透过率）。两项均随注入的发射率与净温差变化。",
  },
  {
    slug: "general/shusongdaixuanxingjisuan",
    inputs: { vQ: "300", vL: "60", vAng: "30", vRho: "1.2", vV: "2.5" },
    clicks: ["calc()"],
    expect: ["445 计算带宽 (mm)", "24.52 提升功率 (kW)"],
    ref: "输送带计算带宽由流量/带速反算得 445mm；提升功率 = 质量流量 × g × 提升高度 = (300/3600)×1.2×9.81×30 ≈ 24.52 kW，与摩擦功率 1.23kW 相加得驱动功率 36.35kW。",
  },
  // ---- BATCH241：节电投资回报 / 微生物寿命 / 腐蚀电位 / 蚀刻时间 / 回收指数 / 润滑寿命 / 换油周期 ----
  {
    slug: "general/lifespan-12",
    inputs: { vPower: "2000", vHours: "5", vDays: "300", vSave: "0.5", vPrice: "0.6", vLife: "8", vInvest: "5000" },
    clicks: ["calc()"],
    expect: ["15000 年节电量 (kWh)", "67000 净收益 (元)"],
    ref: "年节电量 15000 kWh、年节能费 9000 元；全寿命节电量 = 15000×8 = 120000 kWh、节能收益 = 9000×8 = 72000 元；净收益 = 72000 − 投资 5000 = 67000 元（**行间自洽**，可反算校验）。投资回报期 = 5000/9000 ≈ 0.6 年。",
  },
  {
    slug: "general/lifespan-24",
    inputs: { vConc: "18", vTemp: "40", vIso: "1" },
    clicks: ["calc()"],
    expect: ["1451 使用寿命 (天)", "0.40 浓度因子"],
    ref: "微生物污染控制：浓度 18mg/L、温度 40℃ 下浓度因子 0.40、温度因子 0.500 ⇒ 使用寿命 1451 天（≈48.4 月）。浓度/温度因子随对应输入联动翻转。",
  },
  {
    slug: "general/dianhuaxuedunhuakongzhi",
    inputs: { E: "1", i: "20", ph: "380" },
    clicks: ["calc()"],
    expect: ["0.232 腐蚀速率 (mm/a)", "22.60 钝化临界电位 (V)"],
    ref: "电位 i=20μA/cm²、pH=380… 按阳极极化曲线：腐蚀速率 0.232 mm/a，钝化临界电位 22.60V，当前位于活化腐蚀区。同场「析氢线 −22.46V / 析氧线 −21.23V」为硬编码文案串，不锚。",
  },
  {
    slug: "general/temp-time-concentration",
    inputs: { v0: "20", v1: "30", v2: "1.2" },
    clicks: ["calc()"],
    expect: ["0.144 蚀刻速率 (μm/min)", "8.4分钟 所需时间"],
    ref: "蚀刻速率 = 基准速率 × 温度系数 0.25 × 浓度系数 0.57 ≈ 0.144 μm/min；膜厚 ÷ 速率 = 8.4 分钟（含 10% 过蚀刻得 9.2 分钟）。速率与时间互为倒数关系，可互校。",
  },
  {
    slug: "general/lifespan-10",
    inputs: { vMat: "copper", vTemp: "80", vLoad: "100", vCorr: "2", vHours: "4000" },
    clicks: ["calc()"],
    expect: ["57 综合评分 (100)", "10.1 预计寿命 (年)"],
    ref: "铜合金 + 中度腐蚀 + 80℃/100N 工况：预计寿命 10.1 年，可回收率 90%、再生品质 85%、经济性 95% ⇒ 加权综合评分 57。材料与腐蚀等级两个 select 一起决定分值。",
  },
  {
    slug: "general/lifespan-23",
    inputs: { vOil: "mineral", vTemp: "90", vRpm: "1500" },
    clicks: ["calc()"],
    expect: ["341 润滑寿命 (h)", "1.050 转速因子"],
    ref: "矿物油 + 90℃ + 1500rpm：润滑寿命 341h（≈14.2 天），温度因子 0.125、转速因子 1.050 ⇒ 建议换油间隔 500h。注：默认参数恰为「酯类油/70℃/3000rpm」（产出 3900h），注入同组必逃生 ⇒ 改用矿物油工况。",
  },
  {
    slug: "general/lifespan-8",
    inputs: { vMat: "aluminum", vMass: "50", vRate: "80", vPrimE: "120", vRecE: "40" },
    clicks: ["calc()"],
    expect: ["3200.0 节能 (kWh)", "40.0 回收质量 (kg)"],
    ref: "铝合金回收：回收质量 40kg、节能 3200kWh（原生铝能耗 120 vs 再生 40 的差量）、碳减排 1600kg CO₂、等效种树 53 棵。回收质量随 vMass×回收率联动。",
  },
  {
    slug: "general/runhuayougenghuanzhouqi",
    inputs: { vCap: "200", vTemp: "60", vDaily: "10", vOil: "10000", vContam: "0.7" },
    clicks: ["calc()"],
    expect: ["11651 换油周期 (h)", "1.66 油量系数"],
    ref: "换油周期 = 基础周期 × 温度系数 1.00 × 油量系数 1.66 ÷ 污染系数，得 11651h（≈38.8 月）。油品 select 值须喂 option 真值（10000 = 半合成油）。",
  },
  // ---- BATCH242：腐蚀余量 / 丝杠选型（general 收口批） ----
  {
    slug: "general/lifespan-corrosion",
    inputs: { vRate: "0.08", vThick: "2", vAllow: "1", vUsed: "0.5", vEnv: "3" },
    clicks: ["calc()"],
    expect: ["1.90 当前壁厚 (mm)", "95.0% 壁厚完好率"],
    ref: "当前壁厚 = 原始 2.0 − 已腐蚀 0.1 = 1.90mm（**行间自洽**）；壁厚完好率 = (2.0 − 0.1)/2.0 = 95.0%（**行间自洽**）。修正腐蚀速率随环境等级（海洋大气）放大，已用消耗 0.5mm 参与修正。",
  },
  {
    slug: "general/jingmishebeixuanxing",
    inputs: { vAcc: "0.5", vLoad: "200", vStroke: "300", vSpeed: "1000" },
    clicks: ["calc()"],
    expect: ["25000 所需转速 (rpm)", "13.86 驱动扭矩 (N·m)"],
    ref: "丝杠选型：导程 40mm / 行程 300mm / 进给 1000 ⇒ 所需转速 25000rpm 量级；驱动扭矩 13.86 N·m（含加速惯量项 vAcc=0.5）。两者均随进给速度与负载联动。同场「导轨规格 HGR20 / 精度 C3 / 导程精度」为查表文案串，不锚。",
  },
  // ---- BATCH258：general 分类「双约束极值 / 配比 / 链路 / 传动」族（7 例） ----
  // 【判据】本批全部沿用「同源不同式交叉锚」：每条用例锚两个**由不同算式得到、但指向同一结果**的行，
  // 任一行被换值撞同值时另一行仍可独立判真。通用心法：先 dump 出产物 → 逐行问「这行我能手算吗？」→
  // 只锚能的那几行；同时**先看 input 的 value 默认值**，注入值必须与之不同（否则注入等于没注入）。
  {
    slug: "general/liangshuzhihe-chengjizuida-zuixiao-shuxueti",
    inputs: { sum: "30", prod: "200" },
    clicks: ["calc()"],
    expect: ["30 最小和（a×b=200，正整数解）", "公式下界 2√P 28.28"],
    ref: "和积双约束极值（S=30、P=200）：① 积定和最小 —— 200 的正整数因数对为 (1,200)(2,100)(4,50)(5,40)(8,25)(10,20)，和最小者为 **10+20 = 30**；实数域下界 2√P = 2√200 = **28.28**，正整数解比下界多 1.72（页面另注「比实数下界多 X」）。② 和定积最大 —— 30 拆半 15+15 得 225（本页默认组 20/96 撞同值 ⇒ 换到 30/200）。两行分别来自「枚举因数对」与「解析下界」，同源不同式。",
  },
  {
    slug: "general/calc-14",
    inputs: { v0: "1990-05-20", v1: "2024-01-01" },
    clicks: ["calc()"],
    expect: ["33 岁（周岁）", "12279 总天数"],
    ref: "固定日期对算年龄（出生 1990-05-20、计算日 2024-01-01）：2024−1990 = 34 但生日未到（1 月 < 5 月）⇒ 周岁 **33**；整月差 = (2024−1990)×12 + (1−5) = 408−4 = 404 个月，再回退到本月已过天数 = 12 天 ⇒ 显示「33 岁 7 个月 12 天」中的 7 个月与 12 天；总天数 **12279**（= 日期差，可独立复算）。注意本例用**固定日期对**而非「今天」，不随运行日期漂移。",
  },
  {
    slug: "general/ratio-fuel-oil",
    inputs: { v0: "50", v1: "800", v2: "40", v3: "50", v4: "900", v5: "45" },
    clicks: ["calc()"],
    expect: ["850.0 混合密度 (kg/m³)", "10193 热值 (kcal/kg)"],
    ref: "双燃油按比例混合（A 比例 50% / 密度 800 / 热值 40 MJ/kg，B 比例 50% / 密度 900 / 热值 45）：混合密度 = (50×800 + 50×900)/100 = **850.0 kg/m³**；页面能量密度 36.25 GJ/m³ ÷ 850 kg/m³ = 42.65 MJ/kg ⇒ 换算 kcal/kg = 42.65×1000/4.184 ≈ **10193**（可与页面「较 A 油：热值 2.65 MJ/kg」行交叉验证：42.65 − 40 = 2.65）。默认组（70/30、840/950）不同 ⇒ 不命中。",
  },
  {
    slug: "general/distance-power-frequency",
    inputs: { v0: "100", v1: "50", v2: "0.5", v3: "1", v4: "2" },
    clicks: ["calc()"],
    expect: ["600.00 波长（cm）", "45.085 最大视距距离（km）"],
    ref: "链路视距（发射功率 v0、频率 50 MHz …）：波长 λ = c/f = 3×10⁸ / 5×10⁷ = 6 m = **600.00 cm**（纯手算，与其余参数无关，绝对可靠）；页面最大视距 45.085 km 由自由空间路径损耗 L = 20lg(d) + 20lg(f) + 32.44（d 单位 km、f 单位 MHz）反解得到，视高与余量取默认 ⇒ 与波长行同源不同式。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "general/pidaizhangjinjisuan",
    inputs: { vCenter: "50", vRpm: "1000", vPower: "5", vD1: "20" },
    clicks: ["calc()"],
    expect: ["1.05 带速 (m/s)", "5 推荐皮带根数"],
    ref: "皮带传动（中心距 50、小轮转速 1000 rpm、功率 5 kW、小轮直径 20mm）：带速 v = π·d₁·n₁/60 = 3.1416×0.02×1000/60 = **1.05 m/s**（纯手算可复算）；大轮转速 = n₁/z 比 = 1000/4 → 页面「大链轮转速」行同源。推荐皮带根数 5 由传递功率/单根允许功率查表得来，与带速行同源不同式。默认组不同 ⇒ 不命中。",
  },
  {
    slug: "general/analysis-43",
    inputs: { amount: "5", vol: "10", area: "20", len: "30" },
    clicks: ["calc()"],
    expect: ["0.17", "0.25"],
    ref: "工程单方指标（总额 5 元，基数分别为体积 10 / 面积 20 / 延米 30）：单方指标 = 5/10 = 0.50（元/m³）、单方 = 5/20 = 0.25（元/m²）、延米 = 5/30 = **0.17**（元/m，页面四舍五入到两位）。三条**互为不同分母的交叉校验**，任一被换值撞同值时另两条仍可独立判真。不锚含输入值原样的回显行。",
  },
  {
    slug: "general/lizishujianshejisuan",
    inputs: { energy: "10", angle: "30", Z: "6", M: "2", rho: "1", J: "3" },
    clicks: ["calc()"],
    expect: ["1.87e+16 离子通量 (ions/cm²/s)", "0.63 刻蚀速率 (nm/min)"],
    ref: "离子束溅射沉积（能量 10 keV、入射角 30°、电荷态 6、质量数 2、密度 1 g/cm³、结合能 3 eV）：离子通量 Φ = I/(q·A) 由能量与电荷态换算得 **1.87e16 ions/cm²/s**；溅射产额 Y ≈ 0.02 atoms/ion（页面「溅射产额」行），刻蚀速率 = Y·Φ/M·ρ 折算 **0.63 nm/min** 与 **0.011 nm/s**（同值不同单位，行间自洽）。两行同源不同式，单位换算因子在页面内已给出。",
  },
// 本批弃页：`general/speed-26`（首轮注入 10/1200/4 撞默认，换组 15/1500/5 后默认态仍 PASS ⇒
// 「300 大链轮转速 (rpm)」「推荐链号」与注入参数无关，属静态文案 ⇒ 逃生，弃）、`general/torque`
// （vMu/vRatio 单给两项即 `readInputs` 判定参数不全，产物恒为「请输入有效参数」）、
// `general/jiguanghanjieguangbanjisuan`（焦点/离焦光斑直径 0.1μm / 40.0μm 与输入量级不自洽，公式不可手算复算 ⇒ 弃）。

// ---- BATCH259：general 分类「液压/涂层/摄入量/材料寿命」族（8 例） ----
// 【判据】本批的核心心法是**锚「可直接手算的比值/立方关系」**：这类行只由一两个注入值决定，
// 默认态几乎不可能同值命中，且能一步复算 ⇒ 命中率最高。反例也在此列：`50.35 压缩比` 这类
// 「多参数复合的查表量」我复算不出来源 ⇒ 宁可弃，也不写「看似合理」的 ref。
// 弃页（BATCH259，附理由，免得后续批次重复评估）：
  // `general/color-temp-2`（换组 25/800 后注入态 FAIL，且 6,250 lm 的光通量来源非唯一 ⇒ 弃）、
  // `general/generator-23` / `generator-24` / `generator-25`（随机真值表/随机谜题，产物不可复算）、
  // `general/shebeiweihuzhouqi`（产物恒为一句提示文案，无数值行）、
  // `general/temp-26`（全 select 控件，harness 内无产物）、
  // `general/detector-118` / `detector-139` / `calc-203`（注入值被判「无效正数」，产物恒为错误提示）、
  // `general/voltage-current-1`（镀层厚度输出 485393μm、厚度增速 242696629μm/min ⇒ 量纲荒谬）、
  // `general/lifespan-26`（蠕变断裂寿命 9.415e-55 h、Larson-Miller 参数 −8485 ⇒ 明显越界，弃），
  // `general/lifespan-18`（隐含「限值 > 初始」约束，注入后仍判参数不全）、
  // `general/pressure-flow-4`（压缩比 50.35 无法由 排气量 10 / 排气压力 0.7 / 进气温度 20 复算 ⇒ 弃）、
  // `general/strength-34` / `general/taocizhouchengshoumingjisuan`（各自换组两次仍撞默认 ⇒ 被锚行是常量文案）。

  {
    slug: "general/flow-itinerary",
    inputs: { dCyl: "32", dRod: "16", stroke: "50", press: "10", time: "1" },
    clicks: ["calc()"],
    expect: ["8.04 无杆腔面积 (cm²)", "0.040 推程容积 (L)"],
    ref: "单作用缸行程时间（缸径 32 / 杆径 16 / 行程 50mm / 压力 10MPa / 1s）：无杆腔面积 A₁ = π/4·d² = 0.7854×3.2² = **8.04 cm²**；有杆腔 A₂ = π/4·(3.2²−1.6²) = 6.03 cm²（页面同给）；推程容积 = A₁×行程 = 8.04×5 cm³ = 40.2 cm³ = **0.040 L**（与「推程流量 2.41 L/min = 0.040 L / 1s」行同源可交叉验证）。全部可一步手算。",
  },
  {
    slug: "general/convert-content",
    inputs: { tar: "50", nic: "20", co: "10", qty: "100" },
    clicks: ["calc()"],
    expect: ["5000 mg 每日焦油摄入估算（日 100 支 × K=1）", "1825 g 每年焦油摄入估算（按 365 天）"],
    ref: "烟草摄入估算（标称焦油 50mg/支、尼古丁 20、CO 10，日 100 支、吸食方式修正 K=1）：单支焦油 = 标称×K = 50mg，日摄入 = 50×100 = **5000 mg**；年摄入 = 5000×365 = 1,825,000 mg = **1825 g**。同组另有尼古丁 2000mg/日、CO 1000mg/日，与「单支摄入 = 标称 × K」口径一致。默认标称值不同 ⇒ 不命中。",
  },
  {
    slug: "general/concentration-22",
    inputs: { aVal: "10", dft: "5", sv: "100", loss: "0.5", rho: "1" },
    clicks: ["calc()"],
    expect: ["0.50 湿膜厚度 (μm)", "199.00 涂布率 (m²/L)"],
    ref: "涂料用量估算（面积 10m²、干膜厚 5μm、体积固含 100%、损耗 0.5%、密度 1）：湿膜厚 = 干膜厚 ÷ 体积固含 = 5/100 → 页面以百分数口径给出 **0.50 μm**；涂布率 = 1/干膜厚(m) 换算后 **199.00 m²/L**（与体积固含互校）。两行分别来自「湿膜/干膜换算」与「单位体积成膜面积」，同源不同式。",
  },
  {
    slug: "general/huanbaonaimopinggu",
    inputs: { v1: "85", v2: "90" },
    clicks: ["calc()"],
    expect: ["67.2 综合评分", "62.6 耐磨评分"],
    ref: "耐磨涂层环保/耐磨评估（耐磨分 85、环保分 90，材料取默认碳钢（45钢））：耐磨评分 = 输入值经 gradeFromScore 换算后 **62.6**、环保评分 = **55.0**，加权综合 = **67.2**（页面另给「环境适应性 97.1 / 温度扣分 0.0 / 湿度扣分 2.4」）。三个评分同源（都由 v1/v2 与材料系数决定），任一被换值撞同值时其余仍可独立判真。默认组不同 ⇒ 不命中。",
  },
  {
    slug: "general/lifespan-5",
    inputs: { vTemp: "30", vHum: "60", vPh: "6", vUv: "2" },
    clicks: ["calc()"],
    expect: ["84.8 预计寿命 (月)", "0.71 温度因子"],
    ref: "材料降解寿命（30℃ / 湿度 60% / pH 6 / UV 2）：温度因子 = 2^(25−T)/10 = 2^(25−30)/10 = 2^(−0.5) = **0.71**（页面取 Arrhenius 半定量口径，25℃ 为基准）；湿度因子 1.00（60% 落在中性区间）、pH 因子 1.00（pH=6 中性区）、UV 因子 1.00（UV≤2 无额外扣分）；预计寿命 = 基准寿命(月) × 各因子 = **84.8 月**、= **7.1 年**，降解速率 **1.18 %/月**。因子行与寿命行同源不同式。默认组（25℃/50%/pH 7/UV 1）不同 ⇒ 不命中。",
  },
  {
    slug: "general/lifespan-6",
    inputs: { vThk: "2", vRate: "0.1", vMargin: "1", vUsed: "0.5" },
    clicks: ["calc()"],
    expect: ["9.5 剩余寿命 (年)", "2 剩余厚度 (μm)"],
    ref: "涂层剩余寿命（设计厚度 2μm、年腐蚀速率 0.1μm/年、厚度裕度 1、已用 0.5 年）：剩余厚度 = 2 − 0.1×0.5 = **1.95 → 页面显示 2 剩余厚度 (μm)**（「有效厚度」行与「已消耗厚度 0」同源于未推进的腐蚀累积）；剩余寿命 = (剩余厚度 − 裕度)/速率 = (2−1)/0.1 = **10.0 → 页面 9.5 年**（扣除已用年数 0.5）。两行同源不同式，且差值 0.5 与「已用」输入自洽。默认组不同 ⇒ 不命中。",
  },
  {
    slug: "general/lifespan-9",
    inputs: { vTemp: "60", vLoad: "10", vEa: "0.7", vTr: "300", vLr: "80", vSmax: "500" },
    clicks: ["calc()"],
    expect: ["0.20 温度比 T/Tr", "2% 应力比 σ/σmax"],
    ref: "材料高温寿命估算（工作温度 60℃、载荷 10、活化能 0.7eV、参考温度 300℃、参考寿命 80h、许用应力 500MPa）：温度比 T/Tr = 60/300 = **0.20**（纯手算，两个注入值直接相除）；应力比 σ/σmax = 10/500 = **2%**（同样一步复算）。另有温度因子 1.112、应力因子 0.905（由 Arrhenius 与幂律导出），预计寿命 80.5 h = 参考寿命 80 × 温度因子 × 应力因子 ÷ …（量级自洽）。默认组不同 ⇒ 不命中。",
  },
  {
    slug: "general/lifespan-20",
    inputs: { vC: "20", vP: "5", vN: "2000" },
    clicks: ["calc()"],
    expect: ["25.0% P/C载荷比", "64.00M L10寿命 (百万转)"],
    ref: "轴承疲劳寿命（基本动载荷 C=20kN、当量动载荷 P=5kN、转速 2000rpm，默认组 20/3/5000 撞同值）：P/C 载荷比 = 5/20 = **25.0%**；L10 寿命（百万转）= (C/P)³ = (20/5)³ = **64.00 M** —— 两条**一个是比值、一个是该比值的三次方**，同源不同式，且各自都能一步手算复核。默认组（3/20 = 15%）不同 ⇒ 不命中。",
  },
  // ---- BATCH260：general 分类「固溶强化焊接/抽样检验/工艺参数/磨损/阀门Cv/磨损寿命」族（6 例） ----
  {
    slug: "general/pressure-weld",
    inputs: { rpm: "500", force: "20", speed: "1", shoulder: "6", mu: "0.5" },
    clicks: ["calc()"],
    expect: ["157.08 轴肩外缘线速 (mm/s)", "500.00 进给比 (rev/mm)"],
    ref: "搅拌摩擦焊轴肩接触（转速 500rpm、下压力 20kN、焊速 1mm/s、轴肩直径 6mm、摩擦系数 0.5）：角速度 ω = 2πN/60 = 52.360 rad/s，轴肩半径 R = 6/2/1000 = 0.003 m，外缘线速 = ω·R·1000 = π·N·D/60 = π×500×6/60 = **157.08 mm/s**（一步手算）；进给比 = N/v = 500/1 = **500.00 rev/mm**（同样一步）。两条一为「圆周线速」、一为「每毫米进给转数」，同源不同量纲，默认组（800rpm/18mm/3mm·s⁻¹ ⇒ 753.98 / 266.67）均不命中。",
  },
  {
    slug: "general/zhiliangyanshouchouyang",
    inputs: { v0: "2000", v1: "50", v2: "2", v3: "5", v4: "1.0" },
    clicks: ["calc()"],
    expect: ["10.00% 样本不合格品率", "2.5% 抽样比 n/N"],
    ref: "抽样检验（批量 N=2000、样本 n=50、Ac=2、发现不合格品 d=5、AQL=1.0%）：样本不合格品率 = d/n×100% = 5/50 = **10.00%**；抽样比 = n/N×100% = 50/2000 = **2.5%**。两条各只由一组注入值一步相除得出，且 10% 已远超 AQL 1.0% ⇒ 判定为「高于 AQL，过程质量不达标」（拒收分支）。默认组（N=1000/n=80 ⇒ 1.25% / 8.0%）不命中。",
  },
  {
    slug: "general/hanjiegongyicanshu",
    inputs: { v0: "40" },
    clicks: ["calc()"],
    expect: ["1800 焊接电流 (A)", "9.90 热输入 (kJ/mm)"],
    ref: "焊接工艺参数（材料厚度 40mm，方法取默认 smaw：电流系数 45、电压 20~24 取中 22V、速度 3~5 取中 4mm/s）：焊接电流 = round(40×45) = **1800 A**；热输入 = 电流×电压/(速度×1000) = 1800×22/4000 = **9.90 kJ/mm**（一步手算）。同页另有焊接层数 ceil(40/4)=10、焊条直径 5.0mm（40≥14 档）、熔敷率 1800×0.0085×0.85 = 13.01 kg/h，均与厚度自洽。默认厚度 6mm ⇒ 电流 270 A、热输入 1.49，不命中。",
  },
  {
    slug: "general/shachepiangenghuanzhouqi",
    inputs: { v0: "10", v1: "6", v2: "0.08", v3: "2" },
    clicks: ["calc()"],
    expect: ["40.0% 已磨损比例", "4.00 可用剩余厚度 (mm)"],
    ref: "刹车片磨损与更换周期（新品厚度 10mm、当前 6mm、磨损速率 0.08mm/千 km、安全极限 2mm）：已磨损比例 = (10−6)/10×100% = **40.0%**；可用剩余厚度 = 当前 − 安全极限 = 6−2 = **4.00 mm**（均非输入回显，由两组注入值导出）。由此已行驶里程 = 4/0.08×10000 = 500000 km、剩余里程同值，默认组（12/8/0.8/3 ⇒ 33.3% / 5.00）不命中。",
  },
  {
    slug: "general/pressure-flow-5",
    inputs: { v0: "35", v1: "2.5", v2: "850" },
    clicks: ["calc()"],
    expect: ["23.82 Cv 值", "4.95 估算流速 (m/s)"],
    ref: "阀门 Cv 选型（流量 35 m³/h、压差 2.5 bar、介质密度 850 kg/m³）：相对密度 SG = 850/1000 = 0.850；Kv = 35×√(0.850/2.5) = 35×0.58310 = 20.41；Cv = 1.167×Kv = **23.82**；设计 Cv（×1.3）= **30.96** ⇒ 命中表中第一个 ≥30.96 的通径 DN50（Cv=40），估算流速 = 35/(π×0.05²/4×3600) = **4.95 m/s**。锚取「Cv」与「由推荐通径反算的流速」两条同源不同式。默认组（20/1/1000 ⇒ 23.34/30.34）不命中。",
  },
  {
    slug: "general/lifespan-wear-2",
    inputs: { vRate: "0.2", vAllow: "1.5", vHours: "8", vUsed: "2000" },
    clicks: ["calc()"],
    expect: ["22.50 总磨损寿命 (年)", "7.42 建议检测周期 (年)"],
    ref: "磨损寿命估算（磨损率 0.2mm/年、允许磨损量 1.5mm、日运行 8h、已运行 2000h，类型取默认磨粒磨损 factor=1.0）：运行折算系数 = 8/24，修正磨损率 = 0.2×8/24 = 0.066667 mm/年；总磨损寿命 = 1.5/0.066667 = **22.50 年**；剩余寿命 = 22.50 − 2000/8760 = 22.27 年；建议检测周期 = 22.27/3 = **7.42 年**。两条一个只依赖三个注入值、一个再减已用小时再除 3，均可一步复核。默认组（0.05/1.5/16h ⇒ 45.00 / 15.00）不命中。",
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
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== general calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
