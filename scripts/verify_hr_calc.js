#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hr/annual-leave-calc",
  "inputs": {
    "tenure": "3",
    "months": "6"
  },
  "expect": [
    "2.5 天"
  ],
  "ref": "工龄3年落入1-10年档=5天，按在职月份折算 5×6/12=2.5 天（默认 1年/12月 得 5.0 天）"
},
{
  "slug": "hr/assessor-training-hr",
  "inputs": {
    "trainees": "45",
    "hours": "24",
    "preScore": "6.0",
    "postScore": "8.0",
    "satisfaction": "9.0",
    "passRate": "92"
  },
  "expect": [
    "82.9/100"
  ],
  "ref": "L1=9.0×10=90、L2=92、L3=min(100,(8-6)/6×100×2)=66.667，(90+92+66.667)/3=82.889→82.9（默认 30/16/5.5/7.8/8.5/88 得 85.5）"
},
{
  "slug": "hr/attendance-stats",
  "inputs": {
    "workDays": "20",
    "lateFine": "30",
    "earlyFine": "25",
    "absentFine": "300"
  },
  "expect": [
    "525 元"
  ],
  "ref": "扣款合计=Σ(迟到×30+早退×25+旷工×300)=2×30 + 1×25 + (3×30+2×25+1×300)=60+25+440=525（默认 20/20/200 得 360）"
},
{
  "slug": "hr/bandwidth-1",
  "inputs": {
    "v0": "360",
    "v1": "120"
  },
  "expect": [
    "480.00"
  ],
  "ref": "通用双输入页（h1 未命中任一模式正则→兜底分支）：总和=A+B=360+120=480.00（默认 100/50 得 150.00）"
},
{
  "slug": "hr/calc-81",
  "inputs": {
    "v0": "250",
    "v1": "75"
  },
  "expect": [
    "325.00"
  ],
  "ref": "通用双输入页兜底分支：总和=250+75=325.00（默认 100/50 得 150.00）"
},
{
  "slug": "hr/comp-time-calculator",
  "inputs": {
    "hours": "6",
    "dayType": "weekend",
    "workday": "8"
  },
  "expect": [
    "1.5 天"
  ],
  "ref": "休息日倍数2：折算补休=6×2/8=1.5 天（默认 12h/工作日/8h 得 2.3 天）"
},
{
  "slug": "hr/eap-xinli-zixun-weiji-ziyuan",
  "inputs": {
    "v0": "200",
    "v1": "80"
  },
  "expect": [
    "280.00"
  ],
  "ref": "通用双输入页兜底分支：总和=200+80=280.00（默认 100/50 得 150.00）"
},
{
  "slug": "hr/gross-up-calculator",
  "inputs": {
    "afterTax": "12000",
    "rate": "0.2",
    "threshold": "5000"
  },
  "expect": [
    "15680.56"
  ],
  "ref": "二分迭代反算税前：net=gross×(1-0.20)−税(max(0,gross×0.8−5000)) 收敛于 15680.56（默认 8000/0.225/5000 得 10451.61）"
},
{
  "slug": "hr/hris-zizhuyuaiduibijisuanqi",
  "inputs": {
    "v0": "140",
    "v1": "35"
  },
  "expect": [
    "175.00"
  ],
  "ref": "通用双输入页兜底分支：总和=140+35=175.00（默认 100/50 得 150.00）"
},
{
  "slug": "hr/overtime-pay-calc",
  "inputs": {
    "hourly": "30",
    "weekday": "10",
    "weekend": "8",
    "holiday": "4"
  },
  "expect": [
    "1290.00 元"
  ],
  "ref": "总加班费=30×(1.5×10 + 2.0×8 + 3.0×4)=450+480+360=1290.00 元（默认工时全 0 得 0.00 元）"
},
{
  "slug": "hr/performance-ranking",
  "inputs": {
    "v0": "88",
    "v1": "76"
  },
  "expect": [
    "164.0"
  ],
  "ref": "h1 含「得分」命中评分分支：总分=A+B=88+76=164.0（默认 100/50 得 150.0）"
},
{
  "slug": "hr/performance-score",
  "inputs": {
    "excellentPct": "50",
    "failPct": "15"
  },
  "expect": [
    "88.1 88.1 优秀"
  ],
  "ref": "优秀比例 50% → exCount=round(4×0.5)=2，张三(加权 90×0.5+85×0.3+88×0.2=88.1)由第2名升为「优秀」（默认 20% 时 exCount=1 → 张三为「良好」）"
},
{
  "slug": "hr/social-insurance",
  "inputs": {
    "salary": "15000",
    "base": "12000"
  },
  "expect": [
    "7,212 元"
  ],
  "ref": "缴费基数 12000：单位 37.6%=4512、个人 22.5%=2700，合计 7212 元（默认基数 10000 得 6010 元）"
},
{
  "slug": "hr/analysis-29",
  "inputs": {
    "data": "2,4,6,8,10"
  },
  "expect": [
    "2.83"
  ],
  "ref": "均值 6、总体方差 8 → 标准差 √8=2.83（原用例 expect 命中 textarea.value 回显，未验证任何计算；默认数据集标准差 23.02）"
},
  // 注：hr/analysis-conversion-recruit 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "hr/annual-leave-prorate",
  "inputs": {
    "start": "2026-02-01",
    "years": "12",
    "end": "2026-12-31"
  },
  "expect": [
    "9.15 天"
  ],
  "ref": "工龄 12 年→基数 10 天；当年在职 334/365 → 折算精确值 10×334/365=9.15 天（原用例 expect 命中 date input 回显；默认 3-15 入职/5年 得 4.00 天）"
},
{
  "slug": "hr/generator-36",
  "inputs": {
    "cnt": "12"
  },
  "expect": [
    "12. "
  ],
  "ref": "生成条数=cnt=12，末条带编号「12. 」（内容经 Math.random 打乱，故只断言条数上界；默认 cnt=5 时最多到「5.」）"
},
{
  "slug": "hr/recruitment-funnel",
  "inputs": {
    "position": "Java工程师",
    "preset": "campus"
  },
  "expect": [
    "1.50%"
  ],
  "ref": "预设切校园招聘（2000→30）：整体转化率 30/2000×100=1.50%（原用例 expect 命中 select.value 回显；默认技术岗 500→10 得 2.00%）"
},
{
  "slug": "hr/stats-funnel-recruit",
  "inputs": {
    "resume": "1000",
    "interview": "300",
    "offer": "90",
    "hire": "60"
  },
  "expect": [
    "30.00",
    "6.00"
  ],
  "ref": "招聘漏斗：简历1000→面试300→offer90→入职60；面试转化300/1000=30.00%、整体60/1000=6.00%（独立复算，非默认输入）"
},
  // 注：hr/stats-report-attendance 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "hr/tracking-hours",
  "inputs": {
    "required": "50",
    "deadline": "2025-12-31",
    "dept": "研发部"
  },
  "expect": [
    "62%"
  ],
  "ref": "人均学时 (45+38+20+40+12)/5=31，平均完成率 31/50=62%（原用例 via=delEmp 命中兜底删行后的破坏态 37%；默认要求 40h 得 78%）"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== hr calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
