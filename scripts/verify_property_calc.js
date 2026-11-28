#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "property/analysis-40",
  "inputs": {
    "data": "租金收益率,3.2,4.5,high\n空置率,8,5,low\n能耗成本,12,9,low\n客户满意度,78,85,high"
  },
  "expect": [
    "改进空间评分： 32.6%",
    "优先改进（Top3）：空置率（60.0%）"
  ],
  "ref": "4 项均为落后项，改进空间评分=落后项加权平均 rel×100=（0.2889+0.6+0.3333+0.0824)/4×100=32.6；按 rel×权重降序取 Top3（空置率60.0%/能耗成本33.3%/租金收益率28.9%）。非默认输入+独立复算。"
},
{
  "slug": "property/analysis-40",
  "inputs": {
    "data": "满意度,95,90,high\n费用率,8,10,low"
  },
  "expect": [
    "—（无落后项）",
    "无落后项，无需优先改进"
  ],
  "ref": "自身已优于标杆：两项 rel 均为负，改进空间评分不得为正值，Top3 显示无落后项；优势不推高改进空间。"
},
{
  "slug": "property/analysis-40",
  "inputs": {
    "data": "投诉率,5,0,low\n坏方向,10,20,medium"
  },
  "expect": [
    "绝对差 5.00（相对不适用）",
    "第 2 行：方向只能是 high 或 low"
  ],
  "ref": "零基准显示绝对差并标相对不适用；非法方向逐行列出跳过原因，不再静默忽略。"
},
{
  "slug": "property/assessor-manager-1",
  "inputs": {
    "vendorName": "",
    "contractAmt": "75",
    "contractTerm": "12"
  },
  "expect": [
    "75万"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/calc-shared-property-fee",
  "inputs": {
    "totalArea": "150",
    "sharedRatio": "20",
    "feeRate": "2.5",
    "sharedFeeRate": "0.5",
    "customPeriod": "12"
  },
  "expect": [
    "390.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/checker-11",
  "inputs": {},
  "clicks": ["var __m={plan:5,do:1,check:4,act:2};Object.keys(__m).forEach(function(s){for(var i=0;i<4;i++){document.getElementById(s+i).value=String(__m[s]);}});calc()"],
  "expect": [
    "3.00 综合成熟度",
    "发展中 成熟度等级",
    "60% 体系完整度",
    "8 薄弱项",
    "D-检查执行 1.00 未建立 4项"
  ],
  "ref": "16 个评分 <select id=\"<stage><i>\"> 由 buildList() 拼 innerHTML 生成（静态无 id ⇒ clicks 赋值后调 calc()）：P=5/D=1/C=4/A=2 ⇒ 阶段均值 5.00/1.00/4.00/2.00，overall=(5+1+4+2)/4=3.00 ⇒ 发展中、完整度 3/5=60%、薄弱项 D 阶段 4 项 + A 阶段 4 项 = 8（默认值在桩下为空 ⇒ 0.00/薄弱/0%/16）。非默认输入+独立复算。"
},
{
  "slug": "property/checker-7",
  "clicks": [
    "Object.keys(dims).forEach(function(k){dims[k].items.forEach(function(it,i){var el=document.getElementById(k+i);if(el)el.value='1';});});calc();"
  ],
  "expect": [
    "25.0%",
    "综合品质得分 25.0%"
  ],
  "ref": "clicks 遍历 dims 各模块 item 设 value='1'（v=1≤2→issue），得分率 pct=Σ(w)/(4Σw)*100=25.0%、等级不合格；默认全 0→0.0% 不合格，故「25.0%」可区分。注入后显式 calc()。"
},
{
  "slug": "property/checker-recorder-drill",
  "inputs": {
    "drillCount": "75",
    "evacTime": "180",
    "inspector": ""
  },
  "expect": [
    "75人"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/cost-profit",
  "inputs": {
    "v0": "500",
    "v1": "800"
  },
  "expect": [
    "300.00",
    "37.50%",
    "62.50%",
    "1.60"
  ],
  "ref": "重做后真实预算：利润=收入-成本=800-500=300.00；利润率=300/800=37.50%（默认 270/324 得 54.00/16.67%，注入失败即不命中）"
},
{
  clicks: ["calc()"],
  "slug": "property/cycle-elevator",
  "inputs": {},
  "expect": [
    "🛗 暂无电梯，请在上方添加"
  ],
  "ref": "空态：未添加电梯时显示引导文案；原自动用例输入键为模板字符串 logDate_'+el.id+'，注入不到真实节点，改为空态断言。"
},
{
  "slug": "property/elevator-energy",
  "inputs": {
    "liftCount": "5",
    "floors": "18",
    "floorHeight": "3",
    "power": "11",
    "loadRate": "40",
    "tripsPerDay": "200",
    "tripFloors": "6",
    "idleHours": "20",
    "idlePower": "0.5",
    "price": "0.8"
  },
  "expect": [
    "26255"
  ],
  "ref": "5 台 × 14.39 kWh/台日 × 365 ≈ 26255 kWh；含默认速度 1.6、启停附加 10%、无再生"
},
{
  clicks: ["calc()"],
  "slug": "property/energy",
  "inputs": {
    "v0": "9600",
    "v1": "10000",
    "v2": "100"
  },
  "expect": [
    "96.00",
    "1.00",
    "0.96"
  ],
  "ref": "公共能耗分摊=9600×100÷10000=96.00，面积占比=1.00%，单位面积成本=0.96 元/㎡（默认值同此，注入失败即不命中）"
},
{
  "slug": "property/fee-allocation",
  "inputs": {
    "totalFee": "75000"
  },
  "expect": [
    "75000"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "property/rater-performance",
  "inputs": {
    "v0": "95",
    "w0": "20",
    "v1": "80",
    "w1": "20",
    "v2": "90",
    "w2": "15",
    "v3": "88",
    "w3": "15",
    "v4": "92",
    "w4": "15",
    "v5": "85",
    "w5": "15"
  },
  "expect": [
    "88.3"
  ],
  "ref": "客户满意度 95、其余默认： (95×20 + 80×20 + 90×15 + 88×15 + 92×15 + 85×15) ÷ 100 = 88.25 → 88.3。默认 85 为 86.3，可区分；128 等超范围值现改为点名报错。"
},
{
  "slug": "property/report-manager",
  "inputs": { "data": "物业费,320000,180000\n停车费,85000,22000\n广告位,40000,5000\n公共能耗,0,96000" },
  "expect": [
    "收入合计： 445000.00",
    "支出合计： 303000.00",
    "收支结余： +142000.00"
  ],
  "ref": "收入=320000+85000+40000+0=445000；支出=180000+22000+5000+96000=303000；结余=+142000；结余率=31.91%（默认 260000+60000=320000 / 150000+18000+45000=213000 / +107000，避开）"
},
{
  "slug": "property/response-1",
  "inputs": {
    "v0": "2026-11-27T09:00",
    "v1": "2026-11-27T11:00"
  },
  "expect": [
    "120.0 分钟",
    "2.00 h",
    "超时"
  ],
  "ref": "维修响应时长=响应-报修=11:00-09:00=120 分钟（默认 09:30/10:05 得 35 分钟，注入失败即不命中；含跨日与 B>=A 校验）"
},
{
  "slug": "property/response-4",
  "inputs": {
    "v0": "2026-11-27T09:00",
    "v1": "2026-11-27T11:30",
    "v2": "2026-11-27T20:00",
    "v3": "2026-11-28T11:00"
  },
  "expect": [
    "150.0 分钟",
    "660.0 分钟",
    "900.0 分钟"
  ],
  "ref": "响应=11:30-09:00=150 分钟，完成总时长=20:00-09:00=660 分钟，回访间隔=次日11:00-前日20:00=900 分钟（实际跨日 15h=900，注入失败即不命中）"
},
{
  "slug": "property/shared-area",
  "inputs": {
    "innerArea": "4800",
    "unitCount": "40"
  },
  "expect": [ "4800.00 ㎡ 套内总面积" ],
  "ref": "动态部位行在桩内无法完整渲染，本用例只锚定套内总面积注入；分摊结果另用显式部位行用例校验"
},
{
  "slug": "property/stats-manager",
  "inputs": {
    "tot": "300",
    "rent_cnt": "150",
    "visits": "450",
    "dur": "3",
    "price": "6",
    "rent_fee": "400"
  },
  "expect": [
    "3.00",
    "68.75",
    "303,000.00"
  ],
  "ref": "车场：总车位300/包月150 → 临停位150，周转率=450/150=3.00；在场=450×3/24=56.25，占用率=(150+56.25)/300=68.75%；月临停=450×3×6×30=243000，月租=150×400=60000，合计 303000.00（独立复算，非页面默认值）"
},
  {
    "slug": "property/cycle-10",
    "inputs": {
      "routeName": "abc123测试",
      "routeLast": "2026-11-06",
      "newChk": "abc123测试",
      "routeFreq": "7"
    },
    "expect": [
      "📍 abc123测试 周期 每 7 天",
      "1 巡检路线"
    ],
    "ref": "注入路线名与有效上次日期 2026-11-06、7 天周期：卡片应按「数值 + 标签」输出 1 条路线，7 天周期在近 12 个月计划 1 次、完成 0 次、完成率 0.0%，当前逾期 1 条；同时验证无效日期不再进入统计。"
  },
  {
    "slug": "property/cycle-10",
    "clicks": ["var d=parseDateLocal('2026-11-06');document.getElementById('__tbProbe').textContent='P10DATE '+((d.getFullYear()===2026&&d.getMonth()===10&&d.getDate()===6)?'OK':'BAD');"],
    "expect": ["P10DATE OK"],
    "ref": "本地日期解析：旧 addDays 用 new Date('YYYY-MM-DD') 按 UTC 午夜解析，UTC-8 等地区显示会提前一天；现 parseDateLocal 按年月日构造本地日期。"
  },
  {
    "slug": "property/cycle-10",
    "clicks": ["var ds=dueState({last:todayStr(),freq:1});document.getElementById('__tbProbe').textContent='P10SOON '+((ds.days===1&&ds.label==='剩余 1 天')?'OK':'BAD');"],
    "expect": ["P10SOON OK"],
    "ref": "到期标签：旧实现 days≤2 一律写「今日到期」，明日/后日到期被误报；现仅 0 天为「今日到期」，1–2 天显示「剩余 N 天」。"
  },
  {
    "slug": "property/cycle-10",
    "clicks": ["routes=[{id:'RA',name:'A',freq:7,last:todayStr(),checkpoints:['x'],history:[]},{id:'RB',name:'B',freq:7,last:todayStr(),checkpoints:['y'],history:[]}];selectedIdx=1;inspecting={routeIdx:1,routeId:'RB',results:[{name:'y',status:'正常',note:''}]};routes.splice(0,1);selectedIdx=0;finishInspection();document.getElementById('__tbProbe').textContent='P10ID '+((routes.length===1&&routes[0].id==='RB'&&routes[0].history.length===1)?'OK':'BAD');"],
    "expect": ["P10ID OK"],
    "ref": "巡检归属：旧 finishInspection 按数组下标回写，巡检中删除前面的路线会写到错误路线或 undefined；现按路线 id 查找，找不到则丢弃并提示。"
  },
  {
    "slug": "property/cycle-10",
    "clicks": ["var d=nextFromDate('2026-01-31',{freqMode:'months',freq:1});document.getElementById('__tbProbe').textContent='P10MONTH '+((fmtD(d)==='2026-02-28')?'OK':'BAD');"],
    "expect": ["P10MONTH OK"],
    "ref": "自然月周期：1 月 31 日加 1 个自然月，2 月无 31 日，应落到 2026-02-28，而不是 3 月 3 日。"
  },
  {
    "slug": "property/cycle-10",
    "clicks": ["routes=[{id:'RC',name:'C',freq:7,last:todayStr(),checkpoints:['甲','乙'],history:[]}];selectedIdx=0;startInspection();var h=document.getElementById('inspectBody').innerHTML;document.getElementById('__tbProbe').textContent='P10UN '+((h.indexOf('value=\"未检查\" selected')>=0&&h.indexOf('value=\"正常\" selected')<0)?'OK':'BAD');"],
    "expect": ["P10UN OK"],
    "ref": "巡检默认态：所有检查点初始为「未检查」，不得默认「正常」后直接完成。"
  },
  {
    "slug": "property/cleaning-allocation",
    "inputs": { "staffCount": "2" },
    "dynDom": true,
    "expect": ["2 保洁人数"],
    "ref": "保洁人数卡片直读 staffCount：注入 2 ⇒ 结果区「2 保洁人数」；页面默认 4 ⇒「4 保洁人数」，不含「2 保洁人数」⇒ 注入失败必 FAIL。动态任务行在桩内未登记（querySelectorAll 取不到 .task-row），故断言只锚定人数分支，不伪造工作量数值。"
  },
  {
    "slug": "property/cleaning-allocation",
    "inputs": { "staffCount": "0" },
    "dynDom": true,
    "expect": ["保洁人数：必须大于 0"],
    "ref": "人数 0 不再被 max(1,输入) 静默兜底为 1；结果区必须点名「保洁人数：必须大于 0」且不生成分配。"
  },
  {
  clicks: ["calc()"],
    "slug": "property/irrigation-schedule",
    "inputs": { "days": "10", "seed": "7", "rainProb": "80" },
    "dynDom": true,
    "expect": ["10 日浇灌排程", "种子 7、雨概率 80%", "3384 L"],
    "ref": "seed=7 + rainProb=80% 固定序列下 10 天总水量 3384 L；同时断言标题随天数变为「10 日浇灌排程」而非硬编码 14 日，以及模拟天气横幅明确种子与概率。默认 seed=42/25%/14 天三项均不同 ⇒ 注入失败必 FAIL。"
  },
  {
  clicks: ["calc()"],
    "slug": "property/irrigation-schedule",
    "inputs": { "days": "7", "startDate": "2024-06-15", "weatherMode": "manual", "manualWeather": "1,晴,32,0\n2,多云,31,0\n3,小雨,26,0.6\n4,晴,33,0\n5,晴,34,0\n6,阴,28,0.1\n7,大雨,24,1.2" },
    "dynDom": true,
    "expect": ["7 日浇灌排程", "天气来自手动输入", "第 1、5 天", "雨天 2 天"],
    "ref": "手动逐日天气覆盖 7 天；第 3、7 天有效降雨跳过且不顺延，草坪/灌木间隔 4 天，实际浇灌只剩第 1、5 天，跳过原因含「雨天 2 天」。随机模式无法产出该组合 ⇒ 强判别。"
  },
  {
  clicks: ["calc()"],
    "slug": "property/irrigation-schedule",
    "inputs": { "startDate": "" },
    "dynDom": true,
    "expect": ["起始日期：请填写"],
    "ref": "起始日期清空后必须显式报错，不再隐式取当天。"
  },
  {
  clicks: ["calc()"],
    "slug": "property/irrigation-schedule",
    "inputs": { "days": "0" },
    "dynDom": true,
    "expect": ["排程天数：应在 1–30 之间"],
    "ref": "排程天数 0 不得静默回退为 7 天，必须点名范围错误。"
  },
  {
    "slug": "property/rater-performance",
    "inputs": { "w0": "30", "w1": "20", "w2": "15", "w3": "15", "w4": "15", "w5": "15" },
    "expect": ["110 权重合计（原始，用于归一）"],
    "ref": "六维权重合计 30+20+15+15+15+15=110（默认合计 100）。显示原始权重合计并注明用于归一，不再把 110 误写成 110% 或「已归一」。锚完整数值+label 组合串：默认合计 100 不含该串 ⇒ 强判别。"
  },
  {
    "slug": "property/rater-performance",
    "inputs": { "v0": "120" },
    "expect": ["客户满意度得分：不能大于 100"],
    "ref": "得分 120 必须点名拒绝，不再静默截断为 100；输入框保留原值。"
  },
  {
    "slug": "property/rater-performance",
    "inputs": { "w1": "-5" },
    "expect": ["设施维护权重：不能小于 0"],
    "ref": "负权重必须点名拒绝，不再静默归零。"
  },
  {
    "slug": "property/rater-performance",
    "inputs": { "v5": "10", "w5": "0" },
    "expect": ["86.5", "环境品质 （不计入）", "权重为 0、不参与评分与排序：环境品质"],
    "ref": "环境品质 10 分但权重 0：不计入综合得分（其余权重合计 85 → 86.5），且不得出现在优先改进，页面需标注「不计入」。默认 15% 权重时得分为 86.3 不含 86.5 ⇒ 强判别。"
  },
  {
    "slug": "property/rater-performance",
    "inputs": { "gradeA": "85", "gradeB": "75", "gradeC": "65", "gradeD": "55" },
    "expect": ["86.3", "A级 · 优秀", "A≥85"],
    "ref": "默认 86.3 为 B 级；把 A 下限调到 85 后应变为 A 级，证明评级阈值可配置而非固定 90。"
  },
  {
    "slug": "property/rater-performance",
    "inputs": { "gradeA": "80", "gradeB": "90" },
    "expect": ["评级阈值：必须严格递减（A > B > C > D）"],
    "ref": "A 下限低于 B 下限必须报错，不得按顺序静默套用。"
  },
{ slug:"property/assessor-manager-1", inputs:{"contractAmt":""}, expect:["请填写合同金额"], ref:"核心检测值留空不得给出合格/优秀评级（DETCLR）" },
{ slug:"property/elevator-energy", inputs:{"liftCount":"","floors":"","floorHeight":"","power":"","loadRate":"","tripsPerDay":"","tripFloors":"","idleHours":"","idlePower":"","price":"","speed":"","startStop":"","regen":"","meterMonthly":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）；含新增速度/启停/再生字段" },
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

  console.log("==== property calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
