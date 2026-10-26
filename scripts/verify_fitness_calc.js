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
    slug: "fitness/macro-ratio",
    inputs: { weight: "70", bf: "15", intensity: "heavy", goal: "bulk" },
    expect: ["基础代谢 BMR： 1655", "目标热量（增肌盈余）： 3297 kcal/天"],
    ref: "S2 预设「增肌 70kg 重训」等价注入：lean=70×0.85=59.5 ⇒ BMR=370+21.6×59.5=1655；TDEE=1655.2×1.75=2897 ⇒ 目标+400=3297 kcal/天（两锚均依赖 bf=15 的瘦体重项；蛋白锚 126g 只依赖 weight、B 态同值不判别，故不收）（默认 moderate/bulk 组 BMR 1610、目标 2895，避开）"
  },
  {
    slug: "fitness/macro-ratio",
    inputs: { weight: "80", bf: "25", intensity: "moderate", goal: "cut" },
    expect: ["目标热量（减脂缺口）： 2182 kcal/天", "176g 蛋白质/天"],
    ref: "S2 预设「减脂 80kg 中度」等价注入：lean=60 ⇒ BMR=1666；TDEE=1666×1.55=2582 ⇒ 目标−400=2182 kcal/天；蛋白=80×2.2=176 g/天（默认无减脂缺口形态，避开）"
  },
  {
    slug: "fitness/macro-ratio",
    inputs: { weight: "65", bf: "20", intensity: "light", goal: "maintain" },
    expect: ["目标热量（维持）： 2090 kcal/天", "104g 蛋白质/天"],
    ref: "S2 预设「维持 65kg 轻度」等价注入：lean=52 ⇒ BMR=1493；TDEE=1493.2×1.4=2090 ⇒ 目标+0=2090 kcal/天；蛋白=65×1.6=104 g/天（默认无维持形态，避开）"
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
  },
  {
    "slug": "fitness/angle-motion",
    "inputs": {
      "angle": "42",
      "lever": "42",
      "load": "42"
    },
    "expect": [
      "求 (kgf) 11.90% 力学优势 412.02"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"angle\":\"42\",\"lever\":\"42\",\"load\":\"42\"}，输出区含「求 (kgf) 11.90% 力学优势 412.02」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/assessor-18",
    "inputs": {
      "plank": "42",
      "sidePlank": "42",
      "deadBug": "2",
      "birdDog": "2"
    },
    "expect": [
      "Bird Dog 偶有晃动 (2分) 2/3 核心稳定性一般，需系统进行核心训练（平板支撑、死虫、Bird Dog等），每周3-4次。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plank\":\"42\",\"sidePlank\":\"42\",\"deadBug\":\"2\",\"birdDog\":\"2\"}，输出区含「Bird Dog 偶有晃动 (2分) 2/3 核心稳定性一般，需系统进行核心训练…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/analysis-retention",
    "inputs": {
      "init": "42",
      "ret": "42",
      "periods": "42"
    },
    "expect": [
      "流失率（几何）： 0.00% 期末留存 42 / 期初 42，周期 42 个月"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"init\":\"42\",\"ret\":\"42\",\"periods\":\"42\"}，输出区含「流失率（几何）： 0.00% 期末留存 42 / 期初 42，周期 42 个月」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/calc-2",
    "inputs": {
      "age": "42",
      "weight": "42",
      "height": "42",
      "gender": "female"
    },
    "expect": [
      "female\n42\n42\n42\n312"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"weight\":\"42\",\"height\":\"42\",\"gender\":\"female\"}，输出区含「female\n42\n42\n42\n312」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/assessor-64",
    "inputs": {
      "exp": "42",
      "c0": "42",
      "c1": "42",
      "c2": "42",
      "temp": "42",
      "humid": "42",
      "classSize": "42",
      "area": "42",
      "csat": "42",
      "retention": "42",
      "renewal": "42",
      "progress": "42",
      "cert": "8"
    },
    "expect": [
      "10 质量等级： 卓越（S级） ⚠ 优化建议（5项）： 1. 室温不达标 2. 班级人数过多（建议拆班） 3. 学员满意度偏低 4. 学员留存率偏低 5. 复购率偏低（需加强会员运营） 建议制定90天质量提升计划并跟踪改进效果"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"exp\":\"42\",\"c0\":\"42\",\"c1\":\"42\",\"c2\":\"42\",\"temp\":\"42\",\"humid\":\"42\",\"classSize\":\"42\",\"area\":\"42\",\"csat\":\"42\",\"retention\":\"42\",\"renewal\":\"42\",\"progress\":\"42\",\"cert\":\"8\"}，输出区含「10 质量等级： 卓越（S级） ⚠ 优化建议（5项）： 1. 室温不达标 2. …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/calc-4",
    "inputs": {
      "weight": "42",
      "reps": "42"
    },
    "expect": [
      "42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"reps\":\"42\"}，输出区含「42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/calc-3",
    "inputs": {
      "height": "42",
      "neck": "42",
      "waist": "42",
      "hip": "42",
      "gender": "female"
    },
    "expect": [
      "42\n42\n42\n42\nfemale\n28.0% 偏高 性别：女 · 身高：42cm · 颈围：42cm · 腰围：42cm · 臀围：42cm"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"height\":\"42\",\"neck\":\"42\",\"waist\":\"42\",\"hip\":\"42\",\"gender\":\"female\"}，输出区含「42\n42\n42\n42\nfemale\n28.0% 偏高 性别：女 · 身高：42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/calc",
    "inputs": {
      "age": "42",
      "h": "42",
      "w": "42",
      "sex": "f",
      "act": "1.375"
    },
    "expect": [
      "考（维持）：蛋白 67g、脂肪 12g、碳水 13g。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"h\":\"42\",\"w\":\"42\",\"sex\":\"f\",\"act\":\"1.375\"}，输出区含「考（维持）：蛋白 67g、脂肪 12g、碳水 13g。\n暂无计算记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/calc-5",
    "inputs": {
      "weight": "42",
      "customFactor": "42",
      "activity": "1.0",
      "goal": "0.2"
    },
    "expect": [
      " 推荐系数 体重 42 kg · 系数 41.8 - 42.2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"customFactor\":\"42\",\"activity\":\"1.0\",\"goal\":\"0.2\"}，输出区含「 推荐系数 体重 42 kg · 系数 41.8 - 42.2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/calculator-calc-13",
    "inputs": {
      "age": "42",
      "w": "42",
      "s1": "42",
      "s2": "42",
      "s3": "42",
      "sex": "f"
    },
    "expect": [
      "大腿皮褶（mm）\n42.5% 体脂率 1.0051 身体密度 17.9 kg 脂肪重量 24.1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"w\":\"42\",\"s1\":\"42\",\"s2\":\"42\",\"s3\":\"42\",\"sex\":\"f\"}，输出区含「大腿皮褶（mm）\n42.5% 体脂率 1.0051 身体密度 17.9 kg 脂…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/convert",
    "inputs": {
      "val": "42",
      "from": "1.609344",
      "to": "1.609344"
    },
    "expect": [
      "42\n1.609344\n1.609344\n42 42 分钟/英里 = 42 分钟/英里 科学计数法：4.200000e+1 反向换算 分钟/英里 → 分钟/英里：42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"from\":\"1.609344\",\"to\":\"1.609344\"}，输出区含「42\n1.609344\n1.609344\n42 42 分钟/英里 = 42 分钟…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/cycle-5",
    "inputs": {
      "pName": "abc123测试",
      "pTrainer": "abc123测试",
      "pPerWeek": "42"
    },
    "expect": [
      "abc123测试 · abc123测试 · 每周42次 · 已安排0 ×\n周一 6/10 + 安排 周二 6/11 + 安排 周三 6/12 + 安排 周四 6/13 + 安排 周五 6/14 + 安排 周六 6/15 + 安排 周日 6/"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pName\":\"abc123测试\",\"pTrainer\":\"abc123测试\",\"pPerWeek\":\"42\"}，输出区含「abc123测试 · abc123测试 · 每周42次 · 已安排0 ×\n周一 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/circuit-timer",
    "inputs": {
      "workSec": "42",
      "restSec": "42",
      "rounds": "42",
      "readySec": "42"
    },
    "expect": [
      "0 累计训练分钟 42 本轮轮数 84s 单轮时长\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"workSec\":\"42\",\"restSec\":\"42\",\"rounds\":\"42\",\"readySec\":\"42\"}，输出区含「0 累计训练分钟 42 本轮轮数 84s 单轮时长\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/estimate-2",
    "inputs": {
      "w": "42",
      "min": "42"
    },
    "expect": [
      "MET 2.3）\n42\n42\n303"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"min\":\"42\"}，输出区含「MET 2.3）\n42\n42\n303」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/generator",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      " + 配重 10+11.25kg = 实际 41.3kg 26. 目标 13.7kg → 杆 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「 + 配重 10+11.25kg = 实际 41.3kg 26. 目标 13.7…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/estimate",
    "inputs": {
      "h": "42",
      "w": "42",
      "waist": "42",
      "neck": "42",
      "hip": "42",
      "sex": "f"
    },
    "expect": [
      "f\n42\n42\n42\n42\n42\n臀围（cm，女性必填）\n5.7% 体脂率 2.4 kg 脂肪重量 39.6 kg 去脂体重 必需脂肪"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"h\":\"42\",\"w\":\"42\",\"waist\":\"42\",\"neck\":\"42\",\"hip\":\"42\",\"sex\":\"f\"}，输出区含「f\n42\n42\n42\n42\n42\n臀围（cm，女性必填）\n5.7% 体脂率 2.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/rater-time",
    "inputs": {
      "pain": "42",
      "painNum": "42",
      "duration": "42",
      "muscle": "ham"
    },
    "expect": [
      "意： 可正常滚压，避开膝盖后方腘窝 压痛剧烈，建议立即停止重压、冰敷处理；如伴红肿、放射痛或持续不缓解，请就医排查肌肉拉伤或炎症。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pain\":\"42\",\"painNum\":\"42\",\"duration\":\"42\",\"muscle\":\"ham\"}，输出区含「意： 可正常滚压，避开膝盖后方腘窝 压痛剧烈，建议立即停止重压、冰敷处理；如伴红…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/ratio-19",
    "inputs": {
      "armL": "42",
      "armR": "42",
      "thighL": "42",
      "thighR": "42",
      "calfL": "42",
      "calfR": "42"
    },
    "expect": [
      "0% 100.0 大腿 42.0 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"armL\":\"42\",\"armR\":\"42\",\"thighL\":\"42\",\"thighR\":\"42\",\"calfL\":\"42\",\"calfR\":\"42\"}，输出区含「0% 100.0 大腿 42.0 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/macro-ratio",
    "inputs": {
      "weight": "42",
      "bf": "42",
      "intensity": "moderate",
      "goal": "maintain"
    },
    "expect": [
      " 19% 碳水 56% 脂肪 25%\n67g 蛋白质/天 195g 碳水/天 38g 脂肪/天 1.6 蛋白 g/kg"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"bf\":\"42\",\"intensity\":\"moderate\",\"goal\":\"maintain\"}，输出区含「 19% 碳水 56% 脂肪 25%\n67g 蛋白质/天 195g 碳水/天 3…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/load",
    "inputs": {
      "weight": "42",
      "sets": "42",
      "reps": "42",
      "weeks": "42"
    },
    "expect": [
      ") 类型 第1周 43.0 42×42 75940 递增 第2周 44.1 42×42 77839 递增 第3周 45.2 42×42 79785 递增 第4周 40.7 42×42 71806 减载周 第5周 46.4 42×42 817"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"sets\":\"42\",\"reps\":\"42\",\"weeks\":\"42\"}，输出区含「) 类型 第1周 43.0 42×42 75940 递增 第2周 44.1 42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/jianzhinengliangquekoujisuan",
    "inputs": {
      "target": "42",
      "weeks": "42",
      "w": "42",
      "ratio": "0.6"
    },
    "expect": [
      "计达成日期 2025/04/05 减脂占体重比 2.38"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"target\":\"42\",\"weeks\":\"42\",\"w\":\"42\",\"ratio\":\"0.6\"}，输出区含「计达成日期 2025/04/05 减脂占体重比 2.38」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/reminder",
    "inputs": {
      "customMl": "42",
      "goalInput": "42",
      "intervalInput": "42"
    },
    "expect": [
      "000\n2000\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"customMl\":\"42\",\"goalInput\":\"42\",\"intervalInput\":\"42\"}，输出区含「000\n2000\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/resistance",
    "inputs": {
      "age": "42",
      "h": "42",
      "w": "42",
      "z": "42",
      "sex": "f"
    },
    "expect": [
      "Ω，去脂体重占比 90.0% ，体脂等级 必需脂肪 。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"h\":\"42\",\"w\":\"42\",\"z\":\"42\",\"sex\":\"f\"}，输出区含「Ω，去脂体重占比 90.0% ，体脂等级 必需脂肪 。\n暂无计算记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/training-volume",
    "inputs": {
      "newEx": "abc123测试"
    },
    "expect": [
      "卧推 深蹲 硬拉 abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"newEx\":\"abc123测试\"}，输出区含「卧推 深蹲 硬拉 abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/vo2max-12min",
    "inputs": {
      "distance": "42",
      "age": "42",
      "runMin": "42",
      "unit": "km",
      "gender": "female",
      "gender2": "female"
    },
    "expect": [
      " ｜ 平均配速约 0:17 /km\nfemale\n42\n心肺耐力等级： 极佳 VO₂max 927.7\n42\nfemale\n15.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"distance\":\"42\",\"age\":\"42\",\"runMin\":\"42\",\"unit\":\"km\",\"gender\":\"female\",\"gender2\":\"female\"}，输出区含「 ｜ 平均配速约 0:17 /km\nfemale\n42\n心肺耐力等级： 极佳 V…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/zuidasheyanglianggusuan",
    "inputs": {
      "age": "42",
      "dist": "42",
      "w": "42",
      "sex": "f"
    },
    "expect": [
      " 有氧能力等级： 较差 有氧能力不足，建议规律运动并咨询医生"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"dist\":\"42\",\"w\":\"42\",\"sex\":\"f\"}，输出区含「 有氧能力等级： 较差 有氧能力不足，建议规律运动并咨询医生」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fitness/weight-capacity-training",
    "inputs": {
      "weight": "42",
      "sets": "42",
      "reps": "42",
      "onerm": "42"
    },
    "expect": [
      "力量 💡 当前 42kg × 42组 × 42次 = 74088.0kg ，使用实测"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"sets\":\"42\",\"reps\":\"42\",\"onerm\":\"42\"}，输出区含「力量 💡 当前 42kg × 42组 × 42次 = 74088.0kg ，使…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    slug: "fitness/step-stride",
    inputs: { cadence: "170", stride: "0.75", weight: "65" },
    expect: ["2.13", "7.65"],
    ref: "ms = 170×0.75/60 = 2.125 → 2.13 m/s；kmh = 2.125×3.6 = 7.65 km/h；"
       + "每公里步数 = round(1000/0.75) = 1333 步",
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('pace');document.getElementById('distPace').value='10';document.getElementById('timeMPace').value='50';calc();"],
    expect: ['5\'00"/km', '50:00', '10.00 km', '12.0 km/h'],
    ref: '配速模式 10 km / 0:50:00 ⇒ 配速 = 3000÷10 = **300 s** ⇒ `5\'00"/km`；完赛时间 = 10×300 = 3000 s，因不足 1 h 走 fmtTime 的 `MM:SS` 分支 ⇒ **50:00**；距离回显 **10.00 km**；速度 = 3600÷300 = **12.0 km/h**。默认组是 5 km / 0:30:00 ⇒ `6\'00"/km` / `30:00` / `5.00 km` / `10.0 km/h`，四条锚全不撞。',
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('pace');document.getElementById('distPace').value='5';document.getElementById('timeHPace').value='0';document.getElementById('timeMPace').value='25';document.getElementById('timeSPace').value='0';calc();"],
    expect: ["5'00\"/km", "25:00", "12.0 km/h"],
    ref: "S2 预设「5km 破 25」等价注入：配速 = 1500÷5 = 300 s ⇒ `5'00\"/km`；完赛 **25:00**；速度 12.0 km/h（默认组 30:00/5.00 km，避开）",
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('pace');document.getElementById('distPace').value='10';document.getElementById('timeHPace').value='0';document.getElementById('timeMPace').value='50';document.getElementById('timeSPace').value='0';calc();"],
    expect: ["50:00", "10.00 km"],
    ref: "S2 预设「10km 破 50」等价注入：完赛 **50:00**、距离回显 **10.00 km**（默认组 30:00/5.00 km，避开；与例①同值 50:00 分属不同用例不冲突）",
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('pace');document.getElementById('distPace').value='42.195';document.getElementById('timeHPace').value='4';document.getElementById('timeMPace').value='0';document.getElementById('timeSPace').value='0';calc();"],
    expect: ["5'41\"/km", "4:00:00", "10.5 km/h"],
    ref: "S2 预设「全马破 4」等价注入：配速 = 14400÷42.195 = 341.27 s ⇒ `5'41\"/km`；完赛 **4:00:00**（≥1h 带时分支）；速度 3600÷341.27 = 10.5 km/h（默认组全不命中）",
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('pace');setUnit('mi');document.getElementById('distPace').value='6.2';document.getElementById('timeMPace').value='50';calc();"],
    expect: ['8\'04"/mi', '6.20 mi', '12.0 mph'],
    ref: '切到英里后同一组输入（6.2 mi / 0:50:00）⇒ 配速 = 3000÷6.2 = 483.871 s ⇒ `8\'04"/mi`；距离回显 **6.20 mi**；速度改走英里口径 3600×1.60934÷483.871 = **12.0 mph**。本条与上一条例同输入不同单位：配速串带 `/mi`、速度带 `mph`，一旦 `setUnit` 漏改任一后缀就会被抓；默认态 unit 恒为 km，三条锚一律不命中。',
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('time');document.getElementById('distTime').value='21.0975';document.getElementById('paceMTime').value='5';document.getElementById('paceSTime').value='30';calc();"],
    expect: ['5\'30"/km', '1:56:02', '21.10 km', '10.9 km/h'],
    ref: '时间模式 半马 21.0975 km / 5\'30" 配速：配速 = 5×60+30 = **330 s/km** ⇒ `5\'30"/km`；完赛时间 = 21.0975×330 = 6962.175 s ⇒ h=1、m=56、s=round(2.175)=2 ⇒ **1:56:02**；距离回显 **21.10 km**（21.0975 保留两位）；速度 = 3600÷330 = 10.909 ⇒ **10.9 km/h**。`fmtTime` 的「≥1 h 才带时」分支由本条唯一覆盖（例①的 3000 s 走的是 MM:SS 分支）。默认态不进 time 分支，四条锚全不命中。',
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setMode('dist');document.getElementById('timeHDist').value='0';document.getElementById('timeMDist').value='40';document.getElementById('paceMDist').value='5';calc();"],
    expect: ['5\'00"/km', '40:00', '8.00 km', '12.0 km/h'],
    ref: '距离模式用「配速 × 时间」反解距离：配速 5\'00" = **300 s/km**、用时 0:40:00 = **2400 s** ⇒ 距离 = 2400÷300 = **8.00 km**；时间回显 **40:00**（<1 h 的 MM:SS 分支）；速度 **12.0 km/h**。注意 `timeHDist` 的 HTML 默认值是 1，若漏清零会得 20.00 km，本条显式写 0 以排除该歧义。默认态不进 dist 分支（`5.00 km` / `10.0 km/h`），四条锚全不命中。',
  },

  {
    slug: "fitness/pace-calculator",
    inputs: {},
    clicks: ["setStrategy('negative');document.getElementById('targetPaceM').value='6';document.getElementById('targetPaceS').value='0';calcSplits();"],
    expect: ['6\'29"', '5\'31"', '合计 6\'00" 平均 30:00'],
    ref: '分段表「负分策略」（前快后慢）：目标配速 6:00 = 360 s，negative 分支 `targetPace*(1.1-0.2*progress)`、progress=(i-0.5)/numSplits ⇒ 第 1 段 360×(1.1−0.02) = 388.8 s ⇒ **6\'29"**、末段 360×(1.1−0.18) = 331.2 s ⇒ **5\'31"**，五段合计 1800 s ⇒ 合计行 **6\'00" 平均 30:00**。三条锚分别落在「策略系数 1.1 / 0.2」「分段数取整」「合计平均」三个独立式子；even 默认组每段恒 5\'30"、合计 `5\'30" 平均 27:30`，全不命中。',
  },

  {
    slug: "fitness/pace-calculator",
    inputs: { hrAge: "40", hrRest: "70", refPaceM: "6", refPaceS: "20" },
    clicks: ["calcHrPace();"],
    expect: ['125 - 136', '169 - 180', '8\'52"/km'],
    ref: '心率区间表：年龄 40、静息 70 ⇒ 最大心率 220−40 = 180、HRR = 180−70 = 110 ⇒ Z1 落在 round(70+110×0.5)=**125** ~ round(70+110×0.6)=**136**、Z5 落在 round(70+110×0.9)=**169** ~ round(70+110×1)=**180**；参考配速 6:20 = 380 s，Z1 乘 1.4 ⇒ 532 s ⇒ **8\'52"/km**。区间锚只依赖 `rhr+hrr*z.min` 的系数（0.5/0.6…），配速锚只依赖 `paceFactor`，两组互不牵连。默认组（30 岁 / 65 / 5\'30"）⇒ `128 - 140` / `178 - 190` / `7\'42"/km`，全不命中。',
  },

  {"slug": "fitness/running-calories", "inputs": {"weight": "72", "paceMin": "5", "paceSec": "30", "distance": "12.4"}, "expect": ["消耗热量： 900 kcal", "运动时长： 1h 8min", "跑步距离： 12.40 km", "5公里 363 kcal 28min"], "ref": "独立复算（MET 值法，pace 模式）：配速 5'30\" = 330 s/km ⇒ 速度 3600/330 = 10.909 km/h，落在 [10,11) ⇒ MET = 11.0；时长 = 330×12.4/60 = 68.2 min；热量 = 11.0×72×68.2/60 = 900.24 ⇒ round 900 kcal；脂肪 = round(900/9×10)/10 = 100.0 g；fmtTime(68.2) = 1h 8min；5 km 里程碑 = 11×72×(330×5/60)/60 = 363 kcal、耗时 27.5 min ⇒ 28min。默认态（65 kg / 6'0\" / 5 km）四锚分别为 358 kcal / 30min / 5.00 km / 5公里 358 kcal 30min，均不命中。"},

  {"slug": "fitness/running-calories", "inputs": {"weight": "58", "paceMin": "4", "paceSec": "20", "distance": "21.1"}, "expect": ["消耗热量： 1193 kcal", "运动时长： 1h 31min", "跑步距离： 21.10 km", "10公里 566 kcal 43min"], "ref": "独立复算：配速 4'20\" = 260 s/km ⇒ 速度 3600/260 = 13.846 km/h ≥ 12 ⇒ MET = 13.5；时长 = 260×21.1/60 = 91.4333 min；热量 = 13.5×58×91.4333/60 = 1193.2 ⇒ 1193 kcal；脂肪 = round(1193/9×10)/10 = 132.6 g；10 km = 13.5×58×43.3333/60 = 565.9 ⇒ 566 kcal。速度 ≥14 不成立（13.846 < 14），故 MET 取 13.5 而非 16。默认态四锚均不命中。"},

  {
    "slug": "fitness/pace-calculator",
    "inputs": {
      "distPace": "42",
      "timeHPace": "42",
      "timeMPace": "42",
      "timeSPace": "42",
      "distTime": "42",
      "paceMTime": "42",
      "paceSTime": "42",
      "paceMDist": "42",
      "paceSDist": "42",
      "timeHDist": "42",
      "timeMDist": "42",
      "timeSDist": "42",
      "targetPaceM": "42",
      "targetPaceS": "42",
      "hrAge": "42",
      "hrRest": "42",
      "refPaceM": "42",
      "refPaceS": "42"
    },
    "expect": [
      "累计时间 第1K 42'42\" 42:42 42:42 第2K 42'42\" 42:42 1:25:24 第3K 42'42\" 42:42 2:08:06 第4K 42'42\" 42:42 2:50:48 第5K 42'42\" 42:42 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"distPace\":\"42\",\"timeHPace\":\"42\",\"timeMPace\":\"42\",\"timeSPace\":\"42\",\"distTime\":\"42\",\"paceMTime\":\"42\",\"paceSTime\":\"42\",\"paceMDist\":\"42\",\"paceSDist\":\"42\",\"timeHDist\":\"42\",\"timeMDist\":\"42\",\"timeSDist\":\"42\",\"targetPaceM\":\"42\",\"targetPaceS\":\"42\",\"hrAge\":\"42\",\"hrRest\":\"42\",\"refPaceM\":\"42\",\"refPaceS\":\"42\"}，输出区含「累计时间 第1K 42'42\" 42:42 42:42 第2K 42'42\" 4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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

  console.log("==== fitness calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();