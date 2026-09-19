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
 * 注意：依赖「今天」的日期类工具（如 calc-14 年龄）刻意不纳入，否则门禁会随运行日期失败。
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
    expect: ["177.6 电池能量（Wh）", "555.0 平均功率（W）"],
    ref: "无人机：电池能量 = 8000mAh×22.2V/1000 = 177.6Wh；平均功率 555W → 续航 0.32h = 19.2min",
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
