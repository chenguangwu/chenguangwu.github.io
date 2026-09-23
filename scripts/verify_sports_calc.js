#!/usr/bin/env node
/**
 * sports 分类关键计算逻辑独立验证（§4.1.1 收口批次 C）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 用例以运动科学 / 体能计算的确定公式为主，期望值一律由标准公式独立复算得出。
 *
 * 用法：
 *   node scripts/verify_sports_calc.js
 *   node scripts/verify_sports_calc.js tester-1 estimate-tester
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 力量 / 1RM ──────────────────────────────────────────────
  {
    slug: "sports/tester-1",
    inputs: { bw: "70", reps: "10", move: "pullup", added: "0" }, // pullup → load = 体重 + 附加负重(0) = 70
    expect: ["93.3", "1.33"],
    ref: "Epley = 70×(1+10/30)=93.3 kg；相对力量 = 93.3/70 = 1.33（页面 toFixed(1)/toFixed(2)）",
  },

  // ── 最大摄氧量 ──────────────────────────────────────────────
  {
    slug: "sports/estimate-tester",
    inputs: { method: "0", distance: "3000" }, // method 0 = Cooper 12 分钟跑
    expect: ["55.8", "优秀 体能等级"],
    ref: "去默认化：Cooper VO2max = (3000−504.9)/44.73 = 55.75 → 55.8 ml/kg/min，等级跨到「优秀」。默认 2400 → 42.4（一般）。注意「优秀」二字在页面静态参考标准表里已出现，单独用会被默认态命中，必须与「体能等级」绑成连续串",
  },

  // ── 心率储备（Karvonen）────────────────────────────────────
  {
    slug: "sports/calc-heart-rate-1",
    inputs: { age: "45", restHr: "60", formula: "fox" }, // fox: 220−age
    expect: ["175 最大心率", "115 储备心率", "118–175"],
    ref: "去默认化：最大心率 = 220−45 = 175 bpm；储备心率 HRR = 175−60 = 115；Karvonen 区间 = 60+115×[0.5,1] = 118–175 bpm。默认 age 30 → 190 / 130 / 125–190。注意页面另有 maxHr 输入框（默认 190）在 fox 公式下不参与计算，其回显值不可作 expect",
  },

  // ── 氧脉搏 ──────────────────────────────────────────────────
  {
    slug: "sports/yangmaiboxiaolv",
    inputs: { vo2: "2800", hr: "160" }, // phase 默认 '' → a-vO2diff 0.05
    expect: ["17.50", "0.269", "2.80"],
    ref: "去默认化：氧脉搏 O₂pulse = 2800/160 = 17.50 ml/beat；相对氧脉搏 = 17.5/65 = 0.269 ml/beat/kg；VO₂ = 2.80 L/min。默认 3200/180 → 17.78 / 0.274 / 3.20",
  },

  // ── 骑行齿比 ────────────────────────────────────────────────
  {
    slug: "sports/calculator-calc-9",
    inputs: { chainring: "52", cog: "13", circ: "2.105", cadence: "90", targetSpeed: "30" },
    expect: ["4.00 齿比", "8.42", "45.5", "105.5"],
    ref: "去默认化：齿比 = 52/13 = 4.00；每圈距离 = 2.105×4 = 8.42 m；90rpm 速度 = 8.42×90×60/1000 = 45.5 km/h；齿轮英寸 = 8.42/0.0254/π ≈ 105.5。默认 50/11 → 4.55 / 9.57 / 51.7 / 119.9",
  },

  // ── 坡度百分比 ──────────────────────────────────────────────
  {
    slug: "sports/calc-angle-slope",
    inputs: { v1: "250", v2: "18" }, // m 默认 'part'（求部分值）
    expect: ["18% of 250 = 45.00"],
    ref: "去默认化：250×18/100 = 45.00。默认 100/20 → 20% of 100 = 20.00。整串包含公式展示原文，避免只锚结果数字",
  },

  // ── 游泳 SWOLF ──────────────────────────────────────────────
  {
    slug: "sports/swimming-stroke-efficiency",
    inputs: { "pool-length": "25", "stroke-count": "16", "swim-time": "42", "stroke-type": "freestyle" }, // 页面真实 id 带连字符
    expect: ["58.0", "1.56", "22.9", "35.71"],
    ref: "去默认化：**标准 SWOLF = 划次 + 时间 = 16 + 42 = 58.0**（BATCH54 已修掉原式「划次 + 时间/5」的量纲错）；DPS = 25/16 = 1.56 m；SR = 16/42×60 = 22.9 次/分；速度 = 25/42×60 = 35.71 m/min。默认 20/30 → 50.0 / 1.25 / 40.0 / 50.00",
  },

  // ── 出汗率 ──────────────────────────────────────────────────
  {
    slug: "sports/estimate-35",
    inputs: { pre: "75", post: "73.5", dur: "90", intake: "750", urine: "200" },
    expect: ["2050", "1.37", "2.00%", "23 ml/min"],
    ref: "去默认化：体重差 −1.50 kg，实际出汗量 = 1500 + 750(补液) − 200(排尿) = 2050 ml；出汗率 = 2.05 kg / 1.5 h = 1.37 L/h（23 ml/min）；净脱水率 = 1.5/75 = 2.00%。默认 70/69.2/60/500/0 → 1300 ml、1.30 L/h（22 ml/min）、1.14%",
  },
  {
    "slug": "sports/stats-11",
    "inputs": {
      "data": "陈一,92\n陈二,78\n陈三,55\n陈四,84\n陈五,66",
      "full": "100",
      "pass": "60"
    },
    "expect": [
      "平均分： 75.00",
      "及格率： 80.00%",
      "最高分： 92"
    ],
    "ref": "总分=92+78+55+84+66=375，平均=375/5=75.00；中位数=78.00；≥60 者4人 → 及格率80.00%；最高92（陈一）、最低55（陈三）；等级分布优秀1/良好1/及格2/不及格1（独立复算；默认 张三88、李四72、王五95、赵六61 → 平均79.00、及格率100.00%，注入失败即不命中）"
  },

{
  "slug": "sports/analysis-19",
  "inputs": {
    "data": "1,进攻,成功\n2,防守,成功\n3,防守,失败\n4,进攻,成功\n5,进攻,失败\n6,防守,成功\n7,进攻,成功\n8,防守,成功"
  },
  "expect": [
    "进攻成功率： 75.00%",
    "攻防转换： 5 次",
    "综合成功： 6/8"
  ],
  "ref": "进攻4成功3=75.00%、防守4成功3=75.00%；类型切换 5 次；综合 6/8=75.00%（默认 3 回合 50.00%/100.00%/66.67% 避开）"
},
{
  "slug": "sports/pingpangqiu-xiangchi-faqiu-defen",
  "inputs": {
    "v0": "12",
    "v1": "7"
  },
  "expect": [
    "19.0",
    "9.5",
    "5.0"
  ],
  "ref": "乒乓球总分=相持+发球=12+7=19.0；平均=9.5；分差=5.0（默认 8/5 得 13.0，注入失败即不命中）"
},
{
  "slug": "sports/taiquandao-hengti-xiapi-defen",
  "inputs": {
    "v0": "15",
    "v1": "8"
  },
  "expect": [
    "23.0",
    "11.5",
    "7.0"
  ],
  "ref": "跆拳道总分=横踢+下劈=15+8=23.0；平均=11.5；分差=7.0（默认 6/4 得 10.0/5.0/2.0，注入失败即不命中；避开默认总分 10.0 巧合命中）"
},
{
  "slug": "sports/rouren-qianqu-cequ-jinbu",
  "inputs": {
    "v0": "3",
    "v1": "12"
  },
  "expect": [
    "9.00",
    "300.00%",
    "7.50"
  ],
  "ref": "柔韧进步=后-前=12-3=9.00；相对提升=9/3×100=300.00%；平均=7.50（默认 5/9 得 4.00/80.00%/7.00，注入失败即不命中）"
},
{
  "slug": "sports/jianzhong-tuoshui-buye-kongzhi",
  "inputs": {
    "v0": "3",
    "v1": "1.3"
  },
  "expect": [
    "3.90 L",
    "1.95 L",
    "3900 mL"
  ],
  "ref": "补液量=体重差×系数=3×1.3=3.90 L；2h 分次=1.95 L；毫升=3900（默认 2/1.5 得 3.00 L，注入失败即不命中）"
},
{
  "slug": "sports/baofali-zongtiao-lidingtiaoyuan",
  "inputs": {
    "v0": "4",
    "v1": "9.8"
  },
  "expect": [
    "0.816 m",
    "4.00",
    "0.816 s"
  ],
  "ref": "纵跳高度 h=v0²/2g=16/19.6=0.816 m；v0=4.00；滞空=2v0/g=8/9.8=0.816 s（默认 3/9.8 得 0.459 m，注入失败即不命中）"
},
{
  "slug": "sports/lingmin-zhefanpao-chengji",
  "inputs": {
    "v0": "25",
    "v1": "12"
  },
  "expect": [
    "2.08 m/s",
    "7.50",
    "4.80 s/10m"
  ],
  "ref": "平均速度=距离/用时=25/12=2.08 m/s；km/h=7.50；配速=12/25×10=4.80 s/10m（默认 10/15 得 0.67 m/s/2.40/15.00 s/10m，注入失败即不命中）"
},
  {
    "slug": "sports/jixianwei-kuai-man-leixingtuice",
    "inputs": { "v0": "200", "v1": "6" },
    "expect": ["33.33", "均衡型"],
    "ref": "力耐比=200/6=33.33；倾向=均衡型（默认240/5=48.00→快肌主导；swapValues 240/5→5/240 输出慢肌/有氧耐力训练，注入失败均不命中 33.33/均衡型）"
  },
  {
    "slug": "sports/dianjiezhi-diushi-buchong",
    "inputs": { "v0": "2.0", "v1": "50" },
    "expect": ["2300 mg", "5.85 g", "3.00 L"],
    "ref": "钠丢失=2.0×50×23=2300mg；食盐=2300/393=5.85g；补液=2.0×1.5=3.00L（默认1.5/40→1380mg/3.51g/2.25L，注入失败即不命中）"
  },
  {
    "slug": "sports/hongxibao-xieyang-shiyingxing",
    "inputs": { "v0": "1200", "v1": "4" },
    "expect": ["7.2", "3.8 g/L", "中等"],
    "ref": "携氧指数=1.2×4×1.5=7.2；Hb=1.2×4×0.8=3.8g/L；7.2≥5中等（默认2500/4→15.0/8.0/显著，注入失败即不命中）"
  },
  {
    "slug": "sports/pingheng-biyandanjiao-shichang",
    "inputs": { "v0": "5", "v1": "60" },
    "expect": ["4.0", "1.25", "平衡良好"],
    "ref": "常模=(70-60)×0.4=4.0；比=5/4.0=1.25<1.5→平衡良好（默认30/40→12.0/2.50/平衡优秀；swap 30/40→40/30→16.0/2.50/平衡优秀；注入失败均不命中 4.0/1.25/平衡良好）"
  },
  {
    "slug": "sports/rehab-motion",
    "inputs": { "v0": "60", "v1": "15" },
    "expect": ["900 kg", "45 s", "90 kg"],
    "ref": "总负荷=60×15=900kg；单组=15×3=45s；周增=900×0.1=90kg（默认70/12→840/36/84，注入失败即不命中）"
  },
  // ── 最大累积氧亏 MAOD（BATCH54：时长输入单位为「秒」，原代码直接当代分钟用 → 虚高 60 倍）──
  {
    slug: "sports/tester-8",
    inputs: { vo2max: "60", weight: "80", duration: "180", avgVo2: "40", restVo2: "3.5" },
    expect: ["60.0", "4.8"], // 「良好」是页内静态参考表的固有文案，不能作 expect（逃生项）
    ref: "时长 180 秒 = 3 分钟；需氧=60×80×3÷1000=14.40 L；摄氧=40×80×3÷1000=9.60 L；"
       + "氧亏=4.80 L；MAOD=4.80÷80×1000=60.0 ml/kg（≥55 判良好）。"
       + "修复前因未换算分钟，同样输入会算出 864 L 与 3600 ml/kg",
  },

  // ── SWOLF 效率指数（BATCH54：原式写成 划次+秒/5 → 20+6=26 误判精英）──
  {
    slug: "sports/swimming-stroke-efficiency",
    inputs: { "pool-length": "50", "stroke-count": "36", "swim-time": "40", "stroke-type": "freestyle" },
    expect: ["76.0"],
    ref: "SWOLF 标准定义 = 划次 + 用时(秒) = 36+40 = 76.0（50 m 池另减 12 参与评级）；"
       + "修复前的 /5 会算出 36+8=44.0，并把本例误判为精英",
  },

  // ── 举重 Sinclair 体重级别（BATCH54：边界原用 < ，73.00 kg 被抬到 81kg 级）──
  {
    slug: "sports/juzhongzongchengji-sinclair-xishu",
    inputs: { gender: "m", bw: "88", snatch: "100", cj: "130" },
    expect: ["1.168", "268.7", "96kg"],
    ref: "Sinclair 系数=10^(0.7519·(log10(88/175.508))²)=10^(0.7519×0.089940)=1.1684→1.168；"
       + "总成绩 230×1.1684=268.73→268.7 kg；体重 88 kg 属 ≤96 的 96kg 级",
  },

  // ── 马拉松分段（BATCH54：距离列原为恒空三元，半马之后整列空白）──
  {
    slug: "sports/calculator-calc-time",
    // distance 必须显式注入：harness 的 select 桩取首个 option(5 公里)，忽略 selected 的 42.195
    inputs: { distance: "42.195", th: "3", tm: "30", ts: "0" },
    expect: ["4:59", "半程马拉松 21.098", "3:30:00"],
    ref: "总用时 12600 s ÷ 42.195 km = 298.61 s/km = 4:59/km；半程 21.0975×298.61=6300 s=1:45:00；"
       + "分段表 21.0975 km 处应显示「半程马拉松 21.098 km」而非空白的「 km」",
  },

  // ── 1RM 推算（Epley / Brzycki）──────────────────────────────
  {
    slug: "sports/convert-47",
    inputs: { w: "120", r: "3" },
    expect: ["132.0", "90.9", "291.0", "118.8"],
    ref: "Epley=120×(1+3/30)=132.00 kg；强度=120/132=90.9%；折合 132×2.2046=291.0 lb；90% 1RM=118.8 kg",
  },

  // ── 加速过程动力学 ──────────────────────────────────────────
  {
    slug: "sports/speed-5",
    inputs: { v0: "5", v1: "15", t: "2", m: "80" },
    expect: ["5.00", "400.0", "20.00", "8000.0"],
    ref: "a=(15−5)/2=5.00 m/s²；F=80×5=400.0 N；s=(5+15)/2×2=20.00 m；"
       + "ΔKE=0.5×80×(225−25)=8000.0 J；平均功率=8000/2=4000.0 W",
  },

  // ── 赛事满意度（问卷样本为 0 时不得输出 NaN）─────────────────
  {
    slug: "sports/assessor-csat",
    inputs: { total: "0", attend: "0", satisfied: "0", neutral: "0", dissatisfied: "0",
              promoters: "0", passives: "0", detractors: "0" },
    expect: ["无有效问卷", "无有效样本"],
    ref: "CSAT=满意/(满意+一般+不满意) 与 NPS 分母均为 0 ⇒ 修复前输出 NaN% / NaN；应给出无有效样本提示",
  },

  // ── Cooper 12 分钟跑（每分钟摄氧量原为 vo2max/3.5 且单位标 ml）──
  {
    slug: "sports/estimate-tester",
    inputs: { method: "0", distance: "3000", weight: "70" },
    expect: ["55.8", "3.90"],
    ref: "Cooper：VO2max=(3000−504.9)/44.73=55.782→55.8 ml/kg/min；"
       + "绝对每分钟摄氧量=55.782×70÷1000=3.90 L/min（修复前显示 16 ml，那是 VO2max÷3.5 的 MET 倍数）",
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
  console.log("==== sports calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();