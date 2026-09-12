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
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  {
    slug: "general/frequency-3",
    inputs: { a4: "440" },
    expect: ["261.63", "440.00"],
    ref: "十二平均律：C4 = 440×2^(-9/12) = 261.626 Hz，A4 = 440 Hz（key49=A4）",
  },
  {
    slug: "general/calculator-calc-10",
    inputs: { data: "1,2\n2,3.5\n3,5\n4,6.2\n5,8" },
    expect: ["1.47x + 0.53"],
    ref: "最小二乘：斜率 = Σ(x-x̄)(y-ȳ)/Σ(x-x̄)² = 14.7/10 = 1.47；截距 = ȳ-a·x̄ = 4.94-4.41 = 0.53",
  },
  {
    slug: "general/calculator-calc-11",
    inputs: { aRe: "3", aIm: "4", bRe: "1", bIm: "2" },
    expect: ["4+6i", "-5+10i", "2.2-0.4i"],
    ref: "复数运算：(3+4i)+(1+2i)=4+6i；(3+4i)(1+2i)=-5+10i；(3+4i)/(1+2i)=(11-2i)/5=2.2-0.4i",
  },
  {
    slug: "general/calc-ratio-2",
    inputs: { v0: "20", v1: "0.5", v2: "10" },
    expect: ["250 mL", "9,750 mL", "1 : 40"],
    ref: "稀释：原液 = 0.5/20×10L = 0.25L = 250mL；加水 = 10-0.25 = 9.75L；稀释倍数 20/0.5 = 40",
  },
  {
    slug: "general/tax",
    inputs: { base: "1000000", vat: "9", city: "7", edu: "3", local: "2" },
    expect: ["90,000", "6,300", "10.08%"],
    ref: "增值税 = 1000000×9% = 90000；城建税 = 90000×7% = 6300；综合税费率 = (90000+10800)/1000000 = 10.08%",
  },
  {
    slug: "general/voltage",
    inputs: { voltage: "60", current: "100", speed: "10", spot: "0.5" },
    expect: ["6000 束功率", "600.0 线能量"],
    ref: "电子束焊接：束功率 P = U×I = 60×100 = 6000W；线能量 E = P/v = 6000/10 = 600 J/mm",
  },
  {
    slug: "general/calc-stats-1",
    inputs: { data: "10,20,30,40,50,60,70,80" },
    expect: ["525.00", "22.91", "360.00"],
    ref: "总体方差 = Σ(x-45)²/8 = 4200/8 = 525；总体标准差 = √525 = 22.9129；总和 = 360",
  },
  {
    slug: "general/calc-21",
    inputs: { v0: "1000000", v1: "0" },
    expect: ["200,000", "800,000"],
    ref: "偶然所得税 = 1000000×20% = 200000；税后净得 = 1000000-200000 = 800000",
  },
  {
    slug: "general/calc-13",
    inputs: { v0: "2026-06-04", v1: "2026-09-12" },
    expect: ["100 自然日", "2400 小时数"],
    ref: "2026-06-04 → 2026-09-12 共 100 天（30+31+31+8）；×24 = 2400 小时",
  },
  {
    slug: "general/temp-pressure-3",
    inputs: { v0: "1.6", v1: "1000", v2: "137", v3: "0.85", v4: "1.5" },
    expect: ["6.917", "8.42", "1.66"],
    ref: "GB/T 150 内压圆筒：δ = P·Di/(2[σ]φ-P) = 1.6×1000/(2×137×0.85-1.6) = 6.917mm；设计壁厚 = δ+C2 = 8.42mm；[Pw] = 2[σ]φδe/(Di+δe) = 1.66MPa",
  },
  {
    slug: "general/ratio-50",
    inputs: { v0: "60", v1: "40", v2: "100", v3: "10", v4: "80" },
    expect: ["60.00 化学品A", "66.00 安全备量A"],
    ref: "配比：A = 100×60% = 60kg；B = 40kg；安全备量 A = 60×1.1 = 66kg",
  },
  {
    slug: "general/calc-speed-capacity",
    inputs: { v0: "5000", v1: "11.1", v2: "15", v3: "40" },
    expect: ["55.5 电池能量", "13.33 理论最大航程"],
    ref: "无人机：电池能量 = 5000mAh×11.1V = 55.5Wh；航程 = 40km/h×(20/60)h = 13.33km",
  },
  {
    slug: "general/pressure-18",
    inputs: { v0: "30", v1: "3", v2: "1.2", v3: "4" },
    expect: ["5520 总冷负荷", "2.54"],
    ref: "冷负荷 = 围护4320 + 人员600 + 照明600 = 5520W；制冷量 = 5520×1.15 = 6348W；匹数 = 6348/2500 = 2.54",
  },
  {
    slug: "general/power-16",
    inputs: { pVal: "5.5", n1: "1450", ratio: "2.5" },
    expect: ["315 大带轮", "9.5 带速"],
    ref: "V带传动：带速 = π×125×1450/60000 = 9.49m/s；大带轮 = 125×2.5 = 312.5 → 圆整 315mm",
  },
  {
    slug: "general/time-33",
    inputs: { layer: "0.2", infill: "20", volume: "30", speed: "60", nozzle: "0.4", density: "1.24", filD: "1.75" },
    expect: ["498.9 耗材长度", "14.9 耗材质量"],
    ref: "FDM：耗材长度 = 12000mm³/(π×(1.75/2)²) = 4989mm = 498.9cm；质量 = 12cm³×1.24 = 14.88g",
  },
  {
    slug: "general/thread-4",
    inputs: { v0: "M10×1.5" },
    expect: ["2228 主轴转速", "3342 进给速度"],
    ref: "螺纹：转速 = 1000×Vc/(π·D) = 1000×70/(π×10) = 2228rpm；进给速度 = 2228×1.5 = 3342mm/min",
  },
  {
    slug: "general/turnover-2",
    inputs: { vStock: "500", vDaily: "10", vLead: "15", vSafety: "7", vCost: "50" },
    expect: ["7.30 周转率", "3650 年消耗量"],
    ref: "库存：年消耗 = 10×365 = 3650；周转率 = 3650/500 = 7.3 次/年",
  },
  {
    slug: "general/flow-14",
    inputs: { qVal: "50", hVal: "30", rho: "1000", eff: "75", sf: "1.15" },
    expect: ["4.09 水力功率", "5.45 轴功率"],
    ref: "泵：水力功率 = ρgQH/3.6e6 = 1000×9.81×50×30/3.6e6 = 4.09kW；轴功率 = 4.09/0.75 = 5.45kW",
  },
  {
    slug: "general/estimate-14",
    inputs: { v0: "15", v1: "5", v2: "1.5", v3: "15", v4: "6" },
    expect: ["8.04 综合残值", "6.66 年限法残值"],
    ref: "二手车残值：年限法 = 15×(1-55.6%) = 6.66 万；里程法 = 15×(1-37.1%) = 9.43 万；综合 = (6.66+9.43)/2 = 8.04 万",
  },
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 200));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
