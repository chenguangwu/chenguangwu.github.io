#!/usr/bin/env node
/**
 * 第 36 道门禁：fitness 分类计算正确性验证（19 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 跳过：circuit-timer / reminder / rater-time（计时/进度类，含时间状态）；
 *       bodyfat-caliper（测量部位输入由 renderSites 动态生成，需先建状态）；
 *       training-volume / time-stretch（无独立确定性公式或交互式）；
 *       estimate-3 类图形选择式交互 demo。
 * 用法: node scripts/verify_fitness_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "fitness/angle-motion", inputs: { angle: "60", lever: "30", load: "20" },
    expect: ["50.97", "1019.5"],
    ref: "负荷重力=mg=20×9.81=196.20 N；力臂 r=0.30 m；力矩=196.20×0.30×sin60°=50.97 N·m；肌力=力矩/0.05=1019.5 N（默认 90°/35/10 避开）" },
  { slug: "fitness/calc", inputs: { sex: "m", age: "40", h: "180", w: "80", act: "1.375" },
    expect: ["1730", "2379"],
    ref: "Mifflin-St Jeor 男：BMR=10×80+6.25×180−5×40+5=1730 kcal；TDEE=1730×1.375=2378.75→2379（默认 30/175/70/1.55 避开）" },
  { slug: "fitness/calc-2", inputs: { gender: "female", age: "35", weight: "75", height: "178" },
    expect: ["1527"],
    ref: "Mifflin 女：BMR=10×75+6.25×178−5×35−161=1526.5→1527 kcal（默认男 30/65/170→1568 避开）" },
  { slug: "fitness/calc-3", inputs: { gender: "female", height: "165", neck: "32", waist: "75", hip: "95" },
    expect: ["54.2"],
    ref: "美海军女：BF=163.205×log₁₀(75+95−32)−97.684×log₁₀(165)−78.387=349.238−216.615−78.387=54.24→54.2%（默认男 170/38/80→20.2% 避开）" },
  { slug: "fitness/calculator-calc-13", inputs: { sex: "f", age: "25", w: "60", s1: "15", s2: "20", s3: "25" },
    expect: ["1.0447", "23.8", "14.3"],
    ref: "JP 3 点女：Σ=60；D=1.0994921−0.0009929×60+0.0000023×3600−0.0001392×25=1.0447181→1.0447；BF=495/1.0447181−450=23.81→23.8%；脂肪=60×23.81%=14.3 kg（默认男 30/70/12-18-15 避开）" },
  { slug: "fitness/estimate-2", inputs: { sport: "5", w: "80", min: "45" },
    expect: ["725", "3031", "16.1"],
    ref: "MET(跑步12km/h)=11.5；kcal=11.5×3.5×80/200×45=724.5→725 kcal；kJ=724.5×4.184=3031.3→3031；每分钟=16.1（默认 MET 9.8/70kg/30min→360 避开）" },
  { slug: "fitness/jianzhinengliangquekoujisuan", inputs: { target: "8", weeks: "10", w: "75", ratio: "0.5" },
    expect: ["880", "440"],
    ref: "总缺口=8×7700=61600 kcal；每日=61600/(10×7)=880 kcal；饮食=运动=880×0.5=440 kcal（默认 5kg/8周/ratio0.75→688/516/172 避开）" },
  { slug: "fitness/load", inputs: { weight: "80", sets: "5", reps: "6", weeks: "6" },
    expect: ["90.5", "+10.5", "+13.1"],
    ref: "每周×1.025（第 4 周减载×0.9）：第6周结束重量=80×1.025⁵=90.51→90.5 kg；增重=+10.5 kg；增幅=13.14%→+13.1%（默认 weeks=8→69.6/+9.6/+16.0 避开）" },
  { slug: "fitness/ratio-19", inputs: { armL: "34", armR: "36", thighL: "56", thighR: "58", calfL: "37", calfR: "37" },
    expect: ["96.9", "94.3"],
    ref: "上臂：均值 35、差 2、差率 5.71%→对称分 94.29→94.3；大腿：均值 57、差 2、差率 3.51%→96.49；小腿：37/37→100.0；综合=(94.29+96.49+100)/3=96.93→96.9（默认 33/33.5,55/55.5,37/37→99.2 避开）" },
  { slug: "fitness/resistance", inputs: { sex: "m", age: "30", h: "180", w: "85", z: "500" },
    expect: ["26.6", "64.8", "53.7"],
    ref: "阻抗指数=180²/500=64.8；TBW=1.20+0.45×64.8+0.18×85=45.66 L；FFM=45.66/0.732=62.38 kg；BF=(85−62.38)/85×100=26.62→26.6%；水分占比=45.66/85=53.72→53.7%（默认 175/70/450→13.3% 避开）" },
  { slug: "fitness/vo2max-12min", inputs: { distance: "3000", unit: "m", age: "30", gender: "male" },
    expect: ["55.8"],
    ref: "Cooper 12 分钟跑：VO₂max=(3000−504.9)/44.73=55.78→55.8 ml/kg/min（默认 2800 m→51.3 避开）" },
  { slug: "fitness/weight-capacity-training", inputs: { weight: "90", sets: "5", reps: "6", onerm: "" },
    expect: ["2700.0", "108.0", "83.3"],
    ref: "容量=90×5×6=2700.0 kg；估算 1RM=90×(1+6/30)=108.0 kg；强度=90/108×100=83.33→83.3%（默认 60kg/4×10→2400.0/80.0/75.0 避开）" },
  { slug: "fitness/zuidasheyanglianggusuan", inputs: { sex: "m", age: "30", dist: "3000", w: "75" },
    expect: ["55.8", "4.18"],
    ref: "VO₂max=(3000−504.9)/44.73=55.78→55.8；绝对摄氧量=55.78×75/1000=4.184→4.18 L（默认 2400 m/70kg→42.4/2.97 避开）" },
  { slug: "fitness/assessor-64", inputs: { cert: "10", exp: "6", c0: "9", c1: "8", c2: "9", temp: "24", humid: "50",
      classSize: "10", area: "60", csat: "90", retention: "80", renewal: "75", progress: "85" },
    expect: ["8.8", "8.4"],
    ref: "师资=10×0.6+min(6/10,1)×4=8.4；课程=(9+8+9)/3=8.667；环境=10×0.3+10×0.2+10×0.25+10×0.25=10.0；效果=9×0.3+8×0.3+7.5×0.2+8.5×0.2=8.3；综合=8.4×0.25+8.667×0.25+10×0.2+8.3×0.3=8.757→8.8（默认 exp5/8-8-7/12人→8.3 避开）" },
  { slug: "fitness/estimate", inputs: { sex: "m", h: "178", w: "75", waist: "88", neck: "39", hip: "95" },
    expect: ["18.0", "13.5"],
    ref: "美海军男：D=1.0324−0.19077×log₁₀(88−39)+0.15456×log₁₀(178)=1.0578；BF=495/1.0578−450=17.96→18.0%；脂肪=75×17.96%=13.47→13.5 kg（默认 175/70/82/38→14.6% 避开）" },
  { slug: "fitness/calc-4", inputs: { weight: "80", reps: "6" },
    expect: ["96.0", "92.9", "95.7", "97.2", "95.4"],
    ref: "Epley=80×(1+6/30)=96.0；Brzycki=80/(1.0278−0.0278×6)=92.91→92.9；Lombardi=80×6^0.1=95.70→95.7；Mayhew=80×100/(52.2+41.9e^−0.33)=97.18→97.2；平均=95.45→95.4（默认 60kg/8次→75.0 避开）" },
  { slug: "fitness/calc-5", inputs: { weight: "75", activity: "1.6", goal: "0.2", customFactor: "" },
    expect: ["120-150g"],
    ref: "系数=1.6+0.2=1.8；区间=[max(0.8,1.6), 2.0]×75=[120,150] g（默认 65kg/1.3+0.2→85-111g/1.5g/kg 避开）" },
  {
    slug: "fitness/convert",
    inputs: { val: "5", from: "1", to: "1.609344" },
    expect: ["3.10685596119", "8.04672"],
    ref: '跑步配速换算 r=val×f/t：v=5、f=1(分/公里)、t=1.609344(分/英里) ⇒ r=5×1/1.609344=3.10685596119；反向 v×t/f=5×1.609344/1=8.04672。默认 val=1、from=to=1 ⇒ r=1，两串均不出现（双态核验：注入 PASS / 默认 FAIL）。'
  },
  {
    slug: "fitness/convert",
    inputs: { val: "5", from: "1.609344", to: "1" },
    expect: ["8.04672", "3.106855961"],
    ref: '反向分支 r=val×f/t：v=5、f=1.609344(分/英里)、t=1(分/公里) ⇒ r=5×1.609344/1=8.04672；反向 v×t/f=5×1/1.609344=3.106855961。默认 from=to=1 ⇒ r=1，两串均不出现（双态核验：注入 PASS / 默认 FAIL）。'
  },
  {
    slug: "fitness/convert",
    inputs: { val: "10", from: "1", to: "1.609344" },
    expect: ["6.21371192237", "16.09344"],
    ref: 'r=val×f/t：v=10、f=1、t=1.609344 ⇒ r=10×1/1.609344=6.21371192237；反向 v×t/f=10×1.609344/1=16.09344。默认 v=1、from=to=1 ⇒ r=1，两串均不出现（双态核验：注入 PASS / 默认 FAIL）。'
  },
  {
    slug: "fitness/convert",
    inputs: { val: "10", from: "1.609344", to: "1" },
    expect: ["16.09344", "6.213711922"],
    ref: '反向分支 r=val×f/t：v=10、f=1.609344、t=1 ⇒ r=10×1.609344/1=16.09344；反向 v×t/f=10×1/1.609344=6.213711922。默认 from=to=1 ⇒ r=1，两串均不出现（双态核验：注入 PASS / 默认 FAIL）。'
  },
  {
    slug: "fitness/convert",
    inputs: { val: "3", from: "1", to: "1.609344" },
    expect: ["1.86411357671", "4.828032"],
    ref: 'r=val×f/t：v=3、f=1、t=1.609344 ⇒ r=3×1/1.609344=1.86411357671；反向 v×t/f=3×1.609344/1=4.828032。默认 v=1、from=to=1 ⇒ r=1，两串均不出现（双态核验：注入 PASS / 默认 FAIL）。'
  },
  {
    slug: "fitness/convert",
    inputs: { val: "7", from: "1.609344", to: "1" },
    expect: ["11.265408", "4.349598346"],
    ref: '反向分支 r=val×f/t：v=7、f=1.609344、t=1 ⇒ r=7×1.609344/1=11.265408；反向 v×t/f=7×1/1.609344=4.349598346。默认 from=to=1 ⇒ r=1，两串均不出现（双态核验：注入 PASS / 默认 FAIL）。'
  },
  // ── §7.4 零用例加固：fitness 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "fitness/analysis-retention",
    inputs: { init: "1200", ret: "700", periods: "8" },
    expect: ["58.33%", "41.67%", "6.52%"],
    ref: "注入非默认(默认 init=1000/ret=620/periods=6)：整体留存率 = 700/1200 = 58.33%；整体流失率 = 41.67%；月均流失率（几何）= 1 − (0.5833)^(1/8) = 6.52%。默认态 62.00%/38.00%/7.58% 均不命中。"
  },
  {
    slug: "fitness/circuit-timer",
    inputs: { workSec: "45", restSec: "25", rounds: "10", readySec: "15" },
    expect: ["70s 单轮时长", "第 1 / 10 轮"],
    ref: "注入非默认(默认 work=40/rest=20/rounds=8/ready=10)：单轮时长 = 45+25 = 70 s；总轮数取注入的 10 ⇒ 进度行「第 1 / 10 轮」。默认态 60s / 第 1 / 8 轮 不命中。"
  },
  {
    slug: "fitness/assessor-18",
    inputs: { plank: "90", sidePlank: "55" },
    expect: ["平板支撑 90秒 2/3", "10 / 12", "83%"],
    ref: "注入非默认(默认 plank=60/sidePlank=40)：平板支撑 90 秒落在 60–119 s 档 ⇒ 2/3 分；侧平板支撑 55 秒 ⇒ 2/3 分；连同死虫、Bird Dog 各 3/3 ⇒ 总分 10/12 = 83%，等级「核心稳定良好」。默认态 60 秒档位与总分不同。"
  },
  {
    slug: "fitness/macro-ratio",
    inputs: { weight: "82", bf: "22" },
    expect: ["2852 kcal/天", "148g 蛋白质/天", "381g 碳水/天"],
    ref: "注入非默认(默认 weight=70/bf=18)：按去脂体重与活动系数（增肌盈余）⇒ TDEE 2,452 kcal ⇒ 目标热量 2,852 kcal/天；宏量按 21/53/26% ⇒ 蛋白 148 g/天、碳水 381 g/天、脂肪 82 g/天。默认态 2,565 kcal/天 与各克数不同。"
  },
  {
    slug: "fitness/rater-time",
    inputs: { painNum: "7", duration: "90" },
    expect: ["（输入 90 秒，推荐 120 秒）", "滚动 90–120 秒"],
    ref: "注入非默认(默认 painNum=5/duration=60)：压痛 7 分属偏重档 ⇒ 推荐滚动时长 90–120 秒，页面回显「（输入 90 秒，推荐 120 秒）」。默认态推荐区间与回显串不同。⚠ 「45–60 秒」「每日 1–2 次」等为固定文案，两态相同，不可作锚。"
  },

{
    "slug": "fitness/calc-heart-rate",
    "inputs": {
      "age": "25",
      "rest": "70"
    },
    "expect": [
      "195 最大心率 (bpm)"
    ],
    "ref": "最大心率 = 220 − 25 = 195 bpm；储备心率 = 195 − 70 = 125。页面输出 '195 最大心率 (bpm)'。默认态 age=30、rest=65 → 190，不出现 195。"
  },

{
    "slug": "fitness/calculator-calc-constitution",
    "inputs": {
      "h": "180",
      "w": "75"
    },
    "expect": [
      "23.1 BMI 值"
    ],
    "ref": "BMI = 75 ÷ (1.80²) = 75 ÷ 3.24 = 23.15 → 23.1。页面输出 '23.1 BMI 值'。默认态 175/70 → 22.9，不出现 23.1。"
  },

{
    "slug": "fitness/calculator-calc-heart-rate",
    "inputs": {
      "age": "40"
    },
    "expect": [
      "180 Fox (220−年龄)"
    ],
    "ref": "Fox 最大心率 = 220 − 40 = 180 bpm。页面输出 '180 Fox (220−年龄)'。默认态 age=30 → 190，不出现 180。"
  },
  // ── 零用例收敛（2026-10-09）────────────────────────────
  {
    "slug": "fitness/time-stretch",
    "inputs": { "muscle": "chest", "level": "3", "phase": "recover" },
    "expect": [
      "5.4 min 每周总时长",
      "1.8 分钟",
      "恢复/康复 训练阶段",
      "门框拉伸"
    ],
    "ref": "注入三组非默认 select（默认 腘绳肌/初级/热身）。独立复算：页面按『肌肉群 × 柔韧性等级 × 训练阶段』查表给出每周总时长——胸肌 × 高级 × 恢复 = 5.4 min/周；单次总时长 = 静态拉伸 54 秒/组 × 2 组 = 108 秒 = 1.8 分钟。阶段说明与动作提示随 phase 切换为『恢复/康复』与门框拉伸（肩胛下沉）。默认态（腘绳肌/初级/热身）输出 10.0 min / 2 分钟 / 『热身（训练前）』/ 久坐易紧张，四条均不命中。⚠ 页面 applySnap() 读 window 上的 muscle 快照在 harness 桩下抛错，但 select 的 change 监听链本身已重渲染结果（实测 via=input event 通过）。"
  },

  // ── §7.4 零用例加固 · fitness 余 3 页（评分/测量类，注入非默认值）────
  {
    "slug": "fitness/assessor-63",
    "inputs": { "q1": "3", "q2": "4", "q3": "2", "q4": "5", "q5": "1" },
    "expect": ["15 / 25", "均值3.00", "评估质量一般"],
    "ref": "注入非默认（默认 5/5/5/5/5）：五项评分 3+4+2+5+1=15 ⇒ 总分 15/25、均值 3.00、等级「评估质量一般」（默认 25/25、均值5.00、评估质量优秀）。三锚均不命中；不锚 2/5/1 等输入回显。"
  },
  {
    "slug": "fitness/detector-15",
    "inputs": { "t1": "2", "t2": "3", "t3": "1", "sitHours": "10" },
    "expect": ["7 / 10", "久坐时间10小时"],
    "ref": "注入非默认（默认 0/0/0/8）：圆肩风险评分 2+3+1=6 加上久坐加权 ⇒ 7/10、久坐时间10小时文案随 sitHours 翻转（默认 0/10 正常、久坐时间8小时）。⚠️ 弃用「明显圆肩」作锚——正常态输出含「无明显圆肩」，该串是其子串 ⇒ 任何状态都命中（假逃生项，门禁已拦截）。现锚只取随注入翻转且不在正常态出现的「7 / 10」「久坐时间10小时」。"
  },
  {
    "slug": "fitness/bodyfat-caliper",
    "inputs": { "gender": "male", "age": "30", "sites": "3", "site_chest": "20", "site_abdomen": "30", "site_thigh": "25" },
    "expect": ["22.0%", "1.0487", "75.0 mm"],
    "ref": "注入非默认（默认 gender=male/sites=3 但皮褶部位空 ⇒ 提示「请填写全部测量部位」，无体脂结果）：皮褶总和 20+30+25=75mm；男性3点 Jackson-Pollock D=1.10938−0.0008267×75+0.0000016×75²−0.0002574×30=1.0487；Siri 体脂%=495/1.0487−450=22.0%。⚠ 站点输入 id 是 site_<部位名>(site_chest/abdomen/thigh) 而非 site_1/2/3（由 SITES[gender+sites] 动态决定）。判别器回退皮褶为空 ⇒ 回到「请填写全部测量部位」，三锚均不命中。"
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
  console.log("==== fitness calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();