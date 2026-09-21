#!/usr/bin/env node
/**
 * 第 43 道门禁：metalwork 分类计算正确性验证（14 个确定性数值估算工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除（非数值/非确定性，stub 无验证意义）：
 *   - analysis-35/39、analysis-simulator、analysis-cost-price-5：流程/多分支文本结论，非单一数值
 *   - detector-21/23/24/55、detector-mold、resistance-2、surface-finish、pressure-casting：
 *     选择器/评分器输出多段文本，结论随字典变动
 *   - recorder-9：createJob/calcSoaking 依赖 state 与参考温度联动，非纯函数
 *   - carbon-8 等 2 输入模板页：calc 依据 h1 标题关键词分支，标题依赖注入，非稳定
 *   - thread-spec / detector-55：纯静态查表/无输入
 * 用法: node scripts/verify_metalwork_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
{
  "slug": "metalwork/analysis-36",
  "inputs": { "qty": "500", "data": "气孔,45,2\n缩松,28,3\n夹渣,15,2\n砂眼,8,1" },
  "expect": [
    "缺陷总数： 96",
    "加权缺陷指数： 212",
    "缺陷率： 19.20%"
  ],
  "ref": "总数=45+28+15+8=96；加权=45×2+28×3+15×2+8×1=90+84+30+8=212；缺陷率=96/500=19.20%（默认 200 件 30/70/15.00%，避开）"
},

  { slug: "metalwork/assessor-34",
    inputs: { testType: "nss", duration: "300", coating: "zn", stdDuration: "240",
              corrosionArea: "0", blister: "4", rust: "2", cracking: "0",
              rustType: "none", reqGrade: "6" },
    expect: ["7.8", "耐蚀性良好"],
    ref: "腐蚀面积0→Rp10；扣分 rust2×0.5=1 + blister4×0.3=1.2 = 2.2；finalRp=10−2.2=7.8（≥7→良好）；300≥240 且无红锈 → 合格（默认 corrosionArea0.5→Rp6.0 合格，避开）" },

  { slug: "metalwork/cable-tray-sizing",
    inputs: { od: "10", cnt: "10", fill: "40" },
    expect: ["15.7"],
    ref: "A₁=π×10²/4=78.54；A=78.54×10=785.4；A_need=785.4/0.4=1963.5；最小满足规格 100×50=5000；填充率=785.4/5000×100=15.7%（默认 od20/cnt10→100×100/31.4%，避开）" },

  { slug: "metalwork/calc-feed",
    inputs: { dia: "20", z: "4", vc: "100", fz: "0.1" },
    expect: ["1592"],
    ref: "n=1000×100/(π×20)=1591.5→1592 rpm（默认 vc120→1910，避开）" },

  { slug: "metalwork/calc-gear-2",
    inputs: { module: "3", teeth: "20", method: "hob", vc: "60", feed: "1", material: "carbon" },
    expect: ["56.38", "52.50"],
    ref: "d=3×20=60.00；df=3×(20−2.5)=52.50；db=60×cos20°=56.38（默认 m2/z24→d48.00/df43.00/db45.11，避开）" },

  { slug: "metalwork/calc-pressure-mold",
    inputs: { thickness: "3", material: "custom", shear: "480", perimeter: "120" },
    expect: ["172.8", "224.6"],
    ref: "F=120×3×480=172800 N=172.8 kN；Fd=172.8×1.3=224.6 kN（默认 t2/L100/τ350→70.0/91.0，避开）" },

  { slug: "metalwork/calc-stretch",
    inputs: { l0: "50", l1: "65", a0: "100", a1: "60" },
    expect: ["30.00", "40.00"],
    ref: "δ=(65−50)/50×100=30.00%；ψ=(100−60)/100×100=40.00%（默认 100/125/12.57/7.85→25.00/37.55，避开）" },

  { slug: "metalwork/sheet-bend",
    inputs: { thickness: "2", radius: "3", angle: "90", kfactor: "0.40", l1: "50", l2: "50" },
    expect: ["95.969"],
    ref: "BA=(π/180)×(3+0.4×2)×90=5.969；OSSB=tan45°×(3+2)=5.000；BD=2×5.000−5.969=4.031；L=50+50−4.031=95.969（默认 R1.5/L1 50/L2 40，避开）" },

  { slug: "metalwork/tester-19",
    inputs: { cableType: "pvc", ir: "10", temp: "40", cr: "0.2", cs: "2.5", ratedV: "6", len: "100" },
    expect: ["17.0"],
    ref: "1<ratedV=6≤8.7 → 试验电压=2.5×6×1000+2000=17000 V=17.0 kV；温度修正系数=0.5^((40−20)/10)=0.25，R₂₀=10×0.25=2.5 MΩ·km（默认 ratedV0.6→3.5kV，避开）" },

  { slug: "metalwork/thread",
    inputs: { threadType: "metric", diameter: "24", pitch: "3", material: "carbon",
              threadDir: "external", batch: "single" },
    expect: ["22.05", "20.32"],
    ref: "d2=d−0.64952P=24−1.94856=22.05；d1=d−1.22687P=24−3.68061=20.32（默认 d10/P1.5→9.03/8.16，避开）" },


  { slug: "metalwork/welding-heat",
    inputs: { current: "200", voltage: "25", speed: "30", eff: "0.8" },
    expect: ["0.800"],
    ref: "E=(U·I·η·60)/v=(25×200×0.8×60)/30=8000 J/cm=8.00 kJ/cm=0.800 kJ/mm（默认 180/24/25/0.85→0.881，避开）" },

  { slug: "metalwork/lifespan-1",
    inputs: { power: "100", capacity: "10000", voltage: "24", efficiency: "90",
              dod: "80", batType: "custom" },
    expect: ["172.8"],
    ref: "capAh=10000/1000=10；W=10×24=240 Wh；Wu=240×0.9×0.8=172.8 Wh；batType=custom 避免 onBatChange 用预设电压覆盖（默认 5000/3.7/85/80→12.6 Wh，避开）" },

  { slug: "metalwork/pinpaijiazhipinggujisuan",
    inputs: { revenue: "1000", profitRate: "20", multiplier: "10", yearFactor: "2",
              industry: "custom", marketShare: "50" },
    expect: ["20000"],
    ref: "品牌利润=1000×20%=200；份额系数=min(50/10,5)=5；品牌价值=200×10×2×5=20000 万元；industry=custom 避免 onIndustryChange 用预设乘数覆盖（默认 5000/15/5/1.2/10→4500，避开）" },
{
  "slug": "metalwork/analysis-39",
  "inputs": {
    "data": "V1,10\nV2,12\nV3,9",
    "mag": "100",
    "len": "20"
  },
  "expect": [
    "平均晶粒度级别 G： 8.07",
    "级别极差： 0.83",
    "平均截距： 19.63 μm"
  ],
  "ref": "Lr=20/100=0.2mm；nL=50/60/45，G=8.00/8.53/7.70，均值8.07、极差0.83；截距20.00/16.67/22.22，均值19.63μm"
},
{
  "slug": "metalwork/analysis-cost-price-5",
  "inputs": {
    "data": "52000\n54500\n53100\n56800\n55200\n58900\n57400"
  },
  "expect": [
    "均值： 55414.29",
    "变异系数（波动率）： 4.41%",
    "最大回撤： -2.82%"
  ],
  "ref": "n=7 均值 55414.29、样本标准差 2446.38、CV 4.41%；极差 6900、首末 10.38%、最大回撤 −2.82%（默认 4 期 48000..50100 均值 48975 避开）"
},
{
  "slug": "metalwork/analysis-35",
  "inputs": { "trials": "12", "data": "飞边,8,2\n欠铸,5,3\n粘模,3,2\n气孔,6,1" },
  "expect": [
    "问题总数： 22",
    "试模问题密度： 1.83",
    "加权问题指数： 43"
  ],
  "ref": "总数 8+5+3+6=22；密度 22/12=1.83；加权 8×2+5×3+3×2+6×1=43（默认 6 次试模、飞边 4×2 与欠铸 2×3 → 6/1.00/14，避开；最高频与最高加权默认同为飞边故不作断言）"
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
  console.log("==== metalwork calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();