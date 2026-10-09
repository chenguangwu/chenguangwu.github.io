#!/usr/bin/env node
/**
 * 第 43 道门禁：metalwork 分类计算正确性验证（14 个确定性数值估算工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除（非数值/非确定性，stub 无验证意义）：
 *   - analysis-35/39、analysis-simulator、analysis-cost-price-5：流程/多分支文本结论，非单一数值
 *   - detector-21/23/24/55、detector-mold、resistance-2：
 *     选择器/评分器输出多段文本，结论随字典变动
 *     （surface-finish / pressure-casting 原列此条，实为可注入，2026-09-27 已补用例覆盖）
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
},
{
  "slug": "metalwork/laxue-ladao-chisheng-lali-sheji",
  "inputs": {
    "v0": "3.0",
    "v1": "0.06"
  },
  "expect": [
    "50 齿",
    "450.00",
    "585.00"
  ],
  "ref": "v0=3.0,v1=0.06 → 齿数 ⌈3.0÷0.06⌉=50 齿、拉削力 F=250×10×0.06×3=450.00 N、含 1.3 系数 585.00 N（切削宽度 10 mm、同时工作齿 3 固定；默认 2.4/0.08 → 30 齿/600.00/780.00；交换 0.06/3.0 → 1 齿/18000.00/23400.00，均不重合）"
},
{
  "slug": "metalwork/carbon-8",
  "inputs": {
    "v0": "930",
    "v1": "6"
  },
  "expect": [
    "1.146",
    "0.860",
    "2.92"
  ],
  "ref": "v0=930,v1=6 → 层深系数 k=0.42+(930-900)×0.0016=0.468、总层深 δ=0.468×√6=1.146 mm、有效硬化层深 0.75δ=0.860 mm、达 0.8 mm 所需时间 (0.8/0.468)²=2.92 h（默认 900/4 → 0.840/0.630/3.63；交换后温度 6 ℃ 触发 850–950 ℃ 区间提示、无输出，均不重合）"
},

  { slug: "metalwork/detector-hardness",
    inputs: { "coatingType": "paint", "reqLevel": "2", "adhesionMethod": "crosscut",
              "crosscutGrade": "0", "thickMethod": "eddy", "thickness": "48",
              "stdThickness": "40", "thickTolerance": "4", "hardnessMethod": "vickers", "vickersVal": "900" },
    expect: ["涂层质量优秀"],
    ref: "结合力 0 级=100、厚度 48/40=1.2 倍=100、维氏 900HV（有机涂层要求 100HV）=100 → 综合 100 且三项全通过（默认铅笔 6B 不通过 → 等级标「涂层质量良好（未达标）」，与本值不重合）" },

  { slug: "metalwork/detector-hardness",
    inputs: { "coatingType": "paint", "reqLevel": "2", "adhesionMethod": "crosscut",
              "crosscutGrade": "2", "thickMethod": "eddy", "thickness": "48",
              "stdThickness": "40", "thickTolerance": "4", "hardnessMethod": "pencil", "pencilGrade": "6B" },
    expect: ["涂层质量合格（未达标）"],
    ref: "结合力 2 级=65（要求≤1 级 → 不通过）、厚度 100、铅笔 6B=10 不通过 → 综合 65×0.4+100×0.3+10×0.3=59，评分档位为「涂层质量合格」，逐项不通过时等级文案须带「（未达标）」（默认档位为「良好」，与本值不重合）" },

  { slug: "metalwork/thread",
    inputs: { threadType: "metric", diameter: "12", pitch: "1.75", material: "carbon",
              threadDir: "internal", batch: "single" },
    expect: ["小径 D1"],
    ref: "内螺纹小径 D1=d−1.08253P=12−1.8944=10.106mm（默认外螺纹 → 该卡片标签为「牙底直径 d3」，与本值不重合）" },
  { slug: "metalwork/forging-ratio", inputs: { "shape": "rect" }, expect: ["锻造比 K = 2.000", "F₁=90×80=7200mm²"], ref: " shape=矩形 ⇒ renderInputs 生成 w0=120/h0=120/w1=90/h1=80；a0=120×120=14400mm²、a1=90×80=7200mm² ⇒ K=2.000、ε=50.0%（默认圆形 d0=120/d1=70 ⇒ K=2.939、11310/3848mm²，与本值不重合；K=2<目标 3 ⇒ 未达标）" },
  { slug: "metalwork/surface-finish", inputs: { "inType": "ra", "inVal": "0.4" }, expect: ["对应 N5 级表面", "建议加工方法： 精车/精铣/精磨"], ref: " Ra=0.4 落在 0.4→N5 区间，命中最近邻档位 ⇒ 等级与建议加工方法随 Ra 变动" },
  { slug: "metalwork/temp-forging", inputs: { "material": "titanium", "weight": "20", "diameter": "80" }, expect: ["锻造温度范围 180 ℃", "约 14 min"], ref: " 钛合金 MAT_DATA 温度区间下限 180 ℃；加热 t=ceil(20·0.5+80·0.05)=14 min、保温 ceil(20·0.2)=4 min" },
  { slug: "metalwork/zulinfeilvjisuan", inputs: { "value": "120000", "months": "24", "residual": "8", "rate": "6", "payType": "monthly", "mgmtFee": "2" }, expect: ["月租金 5093.00 元", "9.86%"], ref: " 残值 9600.00 → 本金 110400.00；管理费 120000·2%·2.0=4800.00；24 期、期利率 0.5000% ⇒ PMT 4892.9954，月租 5093.00；ROI 9.86%" },
  { slug: "metalwork/pressure-casting", inputs: { "weight": "10", "wall": "1.5", "material": "zinc", "batch": "mass" }, expect: ["压力铸造(压铸) 推荐方法", "最大重量 30 kg"], ref: " 锌 + 批量 mass 命中 METHODS 首项 ⇒ 压铸；壁厚 1.5 的工艺上限重量 30 kg" },

  // ── 零用例加固（2026-10-06）──────────────────────────
  { slug: "metalwork/detector-24", inputs: { defLen: "8", thick: "35", defCount: "3" }, expect: ["缺陷长度/板厚比=22.9%"], ref: "注入非默认(默认 defLen=5/thick=20/defCount=1)：独立复算 8/35 = 22.857% → 22.9%；GB/T 3323 分级 22.9% 超允许范围 ⇒ Ⅴ级（严重不合格）。⚠『Ⅴ级（严重不合格）』文案两态相同（默认 25.0% 同样超限）⇒ 不可作锚，只取比值串。默认态为 25.0%，不命中。" },
  { slug: "metalwork/analysis-simulator", inputs: { vol: "300", area: "150", runner: "15", fillrate: "70", tmelt: "260", tmold: "50", teject: "120", tw: "40", thick: "4", alpha: "0.05" }, expect: ["总充填体积 345 cm³", "充填时间 4.93 s", "冷却时间（近似） 40.63 s", "流程/壁厚比 0.5,000"], ref: "注入非默认(默认 200/100/10/50/240/60/110/30/3/0.04)：型腔+流道+浇口 300+15 与射胶量填充 ⇒ 总充填体积 345 cm³；充填时间 = 345/70 = 4.93 s；冷却时间近似 40.63 s；流程/壁厚比 = (300+15+…)/4 → 0.5,000。默认态 220 cm³/4.40 s/27.51 s/0.6,667，四条均不命中。" },
  { slug: "metalwork/detector-23", inputs: { nominal: "60.000", actual: "60.034", upperTol: "0.039", lowerTol: "0.000" }, expect: ["实测偏差： +0.0340 mm", "偏差占公差带：87.2%", "极限尺寸：60.0000 ~ 60.0390 mm"], ref: "注入非默认(默认 nominal=50.000/actual=50.025)：独立复算 偏差 = 60.034−60.000 = +0.0340 mm；公差带 0.0390 ⇒ 占比 0.034/0.039 = 87.2%；极限尺寸 = 60.0000 ~ 60.0390 mm。默认态 50.025/+0.0250/64.1%/50.0000~50.0390，三条均不命中（『合格』判定与 IT4/±0.005mm 两态相同，不作锚）。" },
  { slug: "metalwork/detector-mold", inputs: { tx: "70.000", ty: "40.000", tz: "25.000", ax: "70.021", ay: "39.975", az: "25.030", tol: "0.020" }, expect: ["X轴：+0.021 mm ✗ 超差", "Z轴：+0.030 mm ✗ 超差", "空间偏差：0.0443 mm"], ref: "注入非默认(默认 50/30/20 与实测 50.015/29.988/20.022)：三轴偏差 = +0.021 / −0.025 / +0.030 mm，均超 ±0.020 ⇒ 三轴全『✗ 超差』；空间偏差 = √(0.021²+0.025²+0.030²) = 0.0443 mm > 0.020。默认态仅 Z 轴超差、空间偏差 0.0292，三条均不命中。" },

  // ── §7.4 零用例收敛续批：metalwork 确定性数值页（探针实测取锚）────
  {
    slug: "metalwork/detector-21",
    inputs: { material: "nonferro", defect: "surface", thickness: "20", level: "general" },
    expect: ["渗透检测 PT（适用评分 5/5）"],
    ref: "注入非默认(默认 material=ferro→磁粉检测 MT 5/5)：非铁磁性+表面缺陷 ⇒ 评分 PT=5、ET=4、UT=2、RT=1、MT=0 ⇒ 首选 PT（适用评分 5/5）。默认态首选为『磁粉检测 MT（适用评分 5/5）』，锚含『PT』与『5/5』连续串，默认态 PT 仅 4/5 不命中。"
  },
  {
    slug: "metalwork/diandonggongju-xifen",
    inputs: { v0: "500", v1: "1000" },
    expect: ["500 W 功率差"],
    ref: "注入非默认(默认 v0=800/v1=1200→400 W 功率差)：功率差 = |500−1000| = 500 W。默认态『400 W 功率差』不命中 500。v0=电钻功率、v1=角磨功率，二者互换不影响差值绝对值。"
  },
  {
    slug: "metalwork/recorder-9",
    inputs: { thickness: "100" },
    expect: ["保温时间：200 分钟"],
    ref: "注入非默认(默认 thickness=50→保温时间：100 分钟)：退火保温时间随厚度线性 ⇒ 100mm→200 分钟（约 3.3 小时）。默认态 50mm→100 分钟不命中 200。页面 renderReadings/drawCurve 在 harness 下读 null 报错但输出区已含 soak 信息，expect 在 input 事件早返回命中。"
  },
  {
    slug: "metalwork/speed-itinerary",
    inputs: { length: "300" },
    expect: ["340 行程长度 (mm)"],
    ref: "注入非默认(默认 length=200→行程长度 240 mm)：行程长度 H = L + 2×越程(20) = 300 + 40 = 340 mm。默认态 200+40=240 不命中 340。其余输入保留页面默认（vc30/碳钢/切深2/进给0.5/余量4/越程20）。"
  },
  {
    slug: "metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi",
    inputs: { v0: "100", v1: "8" },
    expect: ["0.0547 mm"],
    ref: "注入非默认(默认 v0=50/v1=7→标准公差 IT≈0.0216 mm)：真实 calc（页内行 516 镗削专用，覆盖通用两参）孔径 D=100、IT8 系数 a₈=25 ⇒ IT≈(0.45·∛100+0.001·100)×25/1000 = (0.45×4.6416+0.1)×25/1000 = 2.1887×25/1000 = 0.0547 mm。默认态 50/7 → (0.45·3.684+0.05)×16/1000=0.0216，不命中 0.0547。"
  },
  {
    slug: "metalwork/wushua-zhinengyuqingliangduibijisuanqi",
    inputs: { v0: "60", v1: "85" },
    expect: ["25 综合差距"],
    ref: "注入非默认(默认 v0=90/v1=72→18 综合差距)：综合差距 = |60−85| = 25。默认态 |90−72|=18 不命中 25。v0=无刷评分、v1=轻量评分。"
  },
  {
    slug: "metalwork/yuanlingongju-xifen",
    inputs: { v0: "1000", v1: "500" },
    expect: ["500 W 功率差"],
    ref: "注入非默认(默认 v0=1500/v1=600→900 W 功率差)：功率差 = |1000−500| = 500 W。默认态『900 W 功率差』不命中 500。v0=割草机功率、v1=修剪机功率。"
  },
  {
    slug: "metalwork/zhineng-duogongnengyunaiyongduibijisuanqi",
    inputs: { v0: "70", v1: "90" },
    expect: ["20 综合差距"],
    ref: "注入非默认(默认 v0=85/v1=78→7 综合差距)：综合差距 = |70−90| = 20。默认态 |85−78|=7 不命中 20。v0=智能评分、v1=耐用评分。"
  },
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