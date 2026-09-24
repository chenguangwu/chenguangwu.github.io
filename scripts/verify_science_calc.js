#!/usr/bin/env node
/**
 * science 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）。
 * 用例以物理 / 化学 / 统计的确定公式为主，期望值一律由标准公式独立复算得出，不凭记忆。
 *
 * 用法：
 *   node scripts/verify_science_calc.js                       # 跑全部用例
 *   node scripts/verify_science_calc.js newtons-second molar-mass-calculator  # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  // ── 经典力学 ─────────────────────────────────────────────────
  {
    slug: "science/newtons-second",
    // 原 all_default 弱用例（m=10/a=3 恰等于页面默认）
    inputs: { m: "12", a: "4" },
    expect: ["48.0 N 合外力", "14.4000 加速度换算"],
    ref: "改为 m=12/a=4：F = 12×4 = 48.0 N、kN = 0.048000、km/h/s = 4×3.6 = 14.4000、kgf = 48/9.80665 = 4.8946。默认态 30.0 N / 0.030000 / 10.8000 / 3.0591",
  },
  {
    slug: "science/kinetic-energy",
    // 原 all_default 弱用例（m=10/v=5 恰等于页面默认）
    inputs: { m: "12", v: "4" },
    expect: ["96.0 J 动能", "16.0000 速度平方"],
    ref: "改为 m=12/v=4：E = ½×12×16 = 96.0 J、v² = 2E/m = 16.0000、kJ = 0.096000、m·E = 1152.000。默认态 125.0 J / 25.0000 / 0.125000 / 1250.000",
  },
  {
    slug: "science/pendulum-period",
    // 原 all_default 弱用例（L=1/g=9.81 恰等于页面默认）
    inputs: { L: "2.5", g: "9.8" },
    expect: ["3.173 s 周期", "1.9799 角频率"],
    ref: "改为 L=2.5/g=9.8：T = 2π√(2.5/9.8) = 3.173 s、f = 1/T = 0.3151 Hz、ms = 3173.488、ω = √(9.8/2.5) = 1.9799 rad/s。默认态 2.006 s / 0.4985 / 2006.067 / 3.1321",
  },

  // ── 电学（欧姆定律）─────────────────────────────────────────
  {
    slug: "science/ohms-law-calculator",
    inputs: { v: "10", r: "5" }, // calcVar 默认 'i'（求解电流）
    expect: ["2.00 C"],
    ref: "欧姆定律 I = V/R；10 ÷ 5 = 2 A → 电荷量 Q=I=2 → 2.00 C（resQ，toFixed(2)）",
  },

  // ── 化学（摩尔质量 / pH）────────────────────────────────────
  {
    slug: "science/molar-mass-calculator",
    // 原 all_default 弱用例（formula=H2O 恰等于页面默认）
    inputs: { formula: "C6H12O6" },
    expect: ["180.156 元素组成", "72.060", "40.00%"],
    ref: "改为 C6H12O6：M = 12.01×6 + 1.008×12 + 16.00×6 = 180.156（toFixed(3)）；C 行质量 12.01×6 = 72.060、占比 72.06/180.156 = 40.00%。**同批修复页面真缺陷**：元素组成「占比」列原写成 (m/total×100)，而 total 是循环内累加中的前缀和 ⇒ 首行恒 100.00%：H2O 显示 100.00%+88.81% = 188.81%、C6H12O6 显示 100.00%+14.37%+53.29% = 167.66%（占比合计 >100% 物理不可能）。已改为先累加求 total、再第二趟算占比：C6H12O6 → 40.00%/6.71%/53.29%（合计 100.00%）、H2O → 11.19%/88.81%。默认态 18.016、无「72.060」与「40.00%」",
  },
  {
    slug: "science/ph-calculator",
    // ⚠ 默认页签是「H⁺→pH」，读的是 id="H"（默认 0.001）；id="ph" 属于另两个页签，
    // 旧用例注入 ph:"3" 对默认页签**无效**，expect「3.00 / 1.000e-3」实由默认 H=0.001
    // 算出 = 逃生项（判别器修好 deep-dive 后置控件盲区后暴露）。改为注入 H。
    inputs: { H: "0.0005" },
    expect: ["[OH⁻] 2.000e-11 mol/L", "pOH 10.70"],
    ref: "H=5e-4 → pH=-log10(5e-4)=3.30；[OH⁻]=1e-14/5e-4=2.000e-11；pOH=14-3.301=10.70。默认 H=0.001 得 pH 3.00 / [OH⁻] 1.000e-11 / pOH 11.00（跨档）",
  },

  {
    slug: "science/mean-calculator",
    inputs: { data: "1,2,4" },
    expect: ["2.333"],
    ref: "算术平均 = (1+2+4)/3 = 2.333（fmt：round(x·1e10)/1e10 后 toLocaleString，默认最多 3 位小数）",
  },

  {
    slug: "science/p-value-calculator",
    inputs: { alpha: "0.05", z0: "2.5", tail0: "two" },
    expect: ["p = 0.012"],
    ref: "z=2.5 → Φ(2.5)=0.99379，双侧 p = 2×(1−Φ) = 2×min(Φ,1−Φ) = 0.01242，fmt 显示 p = 0.012 并判定拒绝 H₀。原实现 2(1−|Φ−0.5|) 得 1.0124（p>1）且误判不拒绝",
  },

  {
    slug: "science/chi-square-calculator",
    inputs: { obs: "35, 25, 25, 15" },
    expect: ["p = 0.046"],
    ref: "O=[35,25,25,15]、E 留空 → 等概率 E=25：χ² = Σ(O−E)²/E = 4+0+0+4 = 8，df = k−1 = 3，右尾 p = P(χ²₃>8) = 0.0460（精确不完全 Gamma）。原 Wilson–Hilferty 近似漏括号得 p≈0.604（χ²=12.5/df=4 更极端：0.994 vs 真值 0.014）",
  },
  // ── 效应量（Cohen's d → U₃）──────────────────────────────────
  {
    slug: "science/effect-size-calculator",
    inputs: { m1: "112", mu0: "100", sd1: "8" }, // mode0（单样本，默认页签）
    expect: ["93.32%"],
    ref: "d = (M−μ₀)/SD = (112−100)/8 = 1.5 → Cohen's U₃ = Φ(1.5) = 0.9331928 → 93.32%（页面 toFixed(2)）。原实现把「r²」写成 d²，此例得 225% 远超 1，物理上不可能；Φ 经 Python math.erf 独立复算",
  },
  {
    slug: "science/effect-size-calculator",
    inputs: { m1: "95", mu0: "100", sd1: "10" },
    expect: ["30.85%"],
    ref: "d = (95−100)/10 = −0.5 → Φ(−0.5) = 0.3085375 → 30.85%；d 为负时百分位必须 <50%（不得对 d 取绝对值），Python math.erf 独立复算",
  },

  // ── 陨石撞击坑（CMM 标度律 + 千吨当量）─────────────────────
  {
    slug: "science/meteor-crater-estimator",
    inputs: { meteorDiameter: "50", meteorVelocity: "13", meteorDensity: "7800", impactAngle: "45", targetDensity: "2700", targetType: "sedimentary" }, // 巴林杰陨石坑参数
    expect: ["1.22 km", "202.9 m", "5.91 km"],
    ref: "CMM 瞬态坑 D=1.161(ρi/ρt)^(1/3)·L^0.78·v^0.44·g^-0.22·sin^(1/3)45° = 1.161×(7800/2700)^(1/3)×50^0.78×13000^0.44×9.80665^-0.22×0.8909 = 1217 m → 1.22 km（巴林杰坑实测 1.186 km）；深度 1217/6 = 202.9 m；E=4.314e16 J → 10312 kt → 20psi 半径 0.28×10312^0.33 = 5.91 km。原实现 D=0.07(E/ρ)^(1/4) 仅得 0.12 km（偏小 10 倍）、破坏半径误代入「吨」高估 10 倍",
  },

  // ── 样本量（E 按百分比输入）────────────────────────────────
  {
    slug: "science/sample-size-calculator",
    inputs: { N: "5000", conf: "0.99", e: "3", p: "0.4" },
    expect: ["推荐样本量 n = 1308"],
    ref: "E=3% → 0.03；z*=2.5758；n₀=6.6349×0.4×0.6/0.0009=1769.306 → 无限总体 1770；有限修正 1769.306/(1+1768.306/5000)=1307.052 → 1308。原实现直接以 E=3 代入（未 /100）→ 默认态算出 n=1",
  },

  // ── 星等亮度比（方向性）────────────────────────────────────
  {
    slug: "science/star-magnitude-compare",
    inputs: { mag1: "6.0", mag2: "1.0" },
    expect: ["星等2 (1) 的天体更亮，亮度是星等1的 100.02 倍"],
    ref: "Δm=m2−m1=−5，F₁/F₂=2.512^(−5)=1/100.02 ⇒ 星等2 更亮 100.02 倍（星等越小越亮）。原实现两分支方向写反，此处会答成「星等1 更亮」",
  },
  {
    slug: "science/star-magnitude-compare",
    inputs: { mag1: "-1.46", mag2: "0.03" }, // 天狼星 vs 织女星
    expect: ["星等1 (-1.46) 的天体更亮，亮度是星等2的 3.94 倍"],
    ref: "Δm=0.03−(−1.46)=1.49，F₁/F₂=2.512^1.49=3.94 ⇒ 天狼星（星等更小）更亮 3.94 倍",
  },

  // ── 密度（kg/m³ 取值精度 + lb/ft³ 换算）────────────────────
  {
    slug: "science/density-physics",
    inputs: { m: "0.003", V: "0.0012" },
    expect: ["2.500 kg/m³", "0.400000"],
    ref: "ρ=0.003/0.0012=2.5 kg/m³（原实现 rho.toFixed(0) 会显示为 3）；比容 1/ρ=0.4 m³/kg → 0.400000",
  },
  {
    slug: "science/density-physics",
    inputs: { m: "1.5", V: "0.0006" },
    expect: ["156.070", "2.500000"],
    ref: "ρ=2500 kg/m³ → lb/ft³ = 2500×0.062428 = 156.070（新增卡片，替代原无意义的 V/ρ「m⁶/kg」）；g/cm³ = 2500/1000 = 2.5 → 2.500000",
  },

  // ── 物理单位换算（默认同量纲）───────────────────────────────
  {
    slug: "science/convert-power",
    inputs: { val: "1", from: "N", to: "lbf" },
    expect: ["0.224809"],
    ref: "1 N = 0.2248089 lbf（1 lbf = 4.448222 N）。原默认 from=牛顿（力）/ to=公制马力（功率）量纲不同 ⇒ 打开即显示「请选择同量纲单位」，已把默认改为同类。注：harness 的 select 桩取首个 option，故默认态需显式注入 to 才能验证",
  },

  // ── 极昼极夜（跨年区间 / 白夜口径）──────────────────────────
  {
    slug: "science/polar-day-night",
    inputs: { inputLat: "80", hemisphere: "N" },
    expect: ["131 极昼天数", "10月17日 — 2月24日（跨年）", "163 白夜天数"],
    ref: "北纬 80°：极昼需 δ>10° ⇒ 第 107–237 日（4/17–8/25，131 天）；极夜区间跨年（10/17–次年 2/24，131 天）；白夜＝午夜太阳高度 > −6°（民用曙暮光）= 163 天。原实现取「年内首末命中日」⇒ 极夜显示「1月1日 — 12月31日 持续 64 天」（自相矛盾）；白夜用「日照>17h」代理 ⇒ 70°N 只算 53 天（民用曙暮光实为 108 天）",
  },
  {
    slug: "science/polar-day-night",
    inputs: { inputLat: "80", hemisphere: "S" },
    expect: ["10月17日 — 2月24日（跨年）", "4月17日 — 8月25日"],
    ref: "南纬 80°＝季节相反：极昼 10/17–次年 2/24（跨年，131 天）、极夜 4/17–8/25（131 天）。同一纬度两半球互换后区间仍须闭合（跨年标记只出现在 12→1 月的区间）",
  },

  // ── T 分数百分位（解读须与 Z 一致）──────────────────────────
  {
    slug: "science/t-score-calculator",
    inputs: { x: "88", M: "70", sd: "10" },
    expect: ["高于均值（前 3.6%）", "Φ(1.8) = 96.41%"],
    ref: "z=(88−70)/10=1.8，T=68；Φ(1.8)=0.964070 ⇒ 上尾 3.59%→3.6%。原实现按 T 分桶写死「高于均值（前 15.9%）」（T=65/Z=1.5 时实际 6.7%，T=68/Z=1.8 时 3.6%）",
  },

  // ── 公积金贷款额度（封顶 + 月供文案）────────────────────────
  {
    slug: "science/provident-fund",
    inputs: { salary: "20000", selfPct: "12", empPct: "12", months: "120", loanRate: "3.1", loanYears: "30", multi: "15", cityCap: "80" },
    expect: ["800,000", "3,416.13"],
    ref: "月缴存 20000×(12%+12%)=4,800；120 月余额 576,000；余额×15 = 8,640,000 → 受当地上限 80 万封顶 ⇒ 800,000。等额本息 P=800,000、r=3.1%/12、n=360 ⇒ 月供 3,416.13。原实现不封顶（直接显示 8,640,000）且月供文案硬编码「按 50 万元」与实际额度不符",
  },

  // ── 百分位（中位数卡片须与 P50 插值一致）────────────────────
  {
    slug: "science/percentile-calculator",
    inputs: { data: "2,4,4,4,5,5,7,9", percentiles: "25,50,75,90" },
    expect: ["4.5 中位数 P50", "P 75 = 5.5"],
    ref: "n=8 偶数样本：P50=(4+5)/2=4.5（线性插值 pos=(n−1)×0.5=3.5）；P75 pos=(n−1)×0.75=5.25 ⇒ 5×0.75+7×0.25=5.5。原卡片取 sorted[floor((n−1)/2)]=sorted[3]=4（下中位元素），与本页详情插值结果自相矛盾",
  },

  // ── 单因素方差分析 p 值（上尾直算，极小值不显示为 0）────────
  {
    slug: "science/anova-calculator",
    inputs: { groups: "10, 12, 14, 11, 13\n13, 15, 17, 14, 16\n12, 11, 13, 12, 12" },
    expect: ["p = 0.0057", "F = 8.182"],
    ref: "三组均值 12/15/12、总均值 13：SSB=30、SSW=22 ⇒ MSB=15、MSW=1.8333 ⇒ F=8.1818，df=(2,12)；p=(df2/(df2+df1·F))^6=0.005735 ⇒ 显示 0.0057。原实现 p=1−fCDF(F) 在 F 大时 I_x→1 发生灾难性抵消（默认数据 F=25.554 时直接截成 0；此例同时验证 fmtP 的 toFixed(4) 分支——注意不要用 p<1e-4 的数据，默认数据已显示「< 0.0001」，会变成逃生项）",
  },
  {
    slug: "science/anova-calculator",
    inputs: { groups: "10, 12, 14, 11, 13\n13, 15, 16, 12, 14\n11, 13, 12, 14, 10" },
    expect: ["p = 0.1101", "p ≥ 0.05，不拒绝 H₀"],
    ref: "组均值 12/14/12、总均值 12.667：SSB=13.333、SSW=30 ⇒ MSB=6.667、MSW=2.5 ⇒ F=2.667；p=(12/(12+2×2.667))^6=0.11010（与 F(2,12) 密度数值积分 0.110102 一致）⇒ 不拒绝 H₀。中等 p 走 fmtP 的 toFixed(4) 分支",
  },
  {
    slug: "science/astronomy-toolkit",
    inputs: { meteorDiameter: "50", meteorSpeed: "13", meteorDensity: "7800", meteorAngle: "45", groundDensity: "2700" },
    expect: ["1.217 km", "684.7 倍广岛原子弹"],
    ref: "巴林杰陨石坑参数（铁陨石 L=50 m、v=13 km/s、ρi=7800、ρt=2700、45°）：CMM 瞬态坑 D_tc=1.161×(7800/2700)^(1/3)×50^0.78×13000^0.44×9.80665^−0.22×sin^(1/3)45°=1217.4 m，未超 2.5 km 过渡径（不折减）→ 1.217 km；E=0.5×(4/3)π·25³×7800×13000²=4.314e16 J ⇒ 广岛当量 684.7 倍。原实现把 CMM 与另一条 D=0.07(E/ρ)^(1/4) 取平均 ⇒ 仅 619 m，且与同站 science/meteor-crater-estimator 同参数给出的 1.22 km 自相矛盾",
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
  console.log("==== science calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();