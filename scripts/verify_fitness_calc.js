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