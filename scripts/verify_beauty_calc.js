#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原 expect「风格」取自常量保养建议「💋 体型匀称适合各类穿搭风格」（默认女性必出）→ 逃生项。
  // 改超重档输入，断言由 BMI 派生的分级与对应建议；回退默认（165/55 → BMI 20.2 正常档）故必失配。
  "slug": "beauty/bmi-beauty",
  "inputs": {
    "height": "170",
    "weight": "85",
    "age": "35",
    "waist": "95",
    "hip": "105"
  },
  "expect": [
    "BMI 指数 · 肥胖",
    "💪 推荐有氧运动+力量训练"
  ],
  "ref": "BMI = 85 / 1.70² = 29.41 → classify() ≥28 → 「肥胖」（结果大字 29.4）；超重/肥胖档才追加「💪 推荐有氧运动+力量训练」。回退默认 165/55 → BMI 20.20 → 「正常」档，两条建议均不出现。"
},
{
  "slug": "beauty/aging-calculator",
  "inputs": {
    "realAge": "38"
  },
  "expect": [
    "38"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/analysis-cost-profit",
  "inputs": {
    "cus": "420",
    "price": "320",
    "mat": "60",
    "labor": "30000",
    "fixed": "35000"
  },
  "expect": [
    "毛利： 109200.00",
    "营业利润： 44200.00",
    "盈亏平衡客数： 250.00"
  ],
  "ref": "营收=420×320=134400，耗材=420×60=25200 → 毛利=109200（毛利率81.25%）；固定成本=30000+35000=65000 → 营业利润=44200（净利率32.89%）；单客边际贡献=320−60=260 → 盈亏平衡客数=65000/260=250.00（独立复算；默认 300/260/45/22000/26000 → 毛利64500、利润16500、保本223.26，注入失败即不命中）"
},
{
  "slug": "beauty/analysis-detector-diagnosis",
  "inputs": {
    "moisture": "38",
    "oil": "62",
    "pigment": "70",
    "pores": "55",
    "sensitivity": "65"
  },
  "expect": [
    "外油内干（敏感倾向）",
    "水分： 38 偏低",
    "油分： 62 偏高",
    "色素： 70 偏高",
    "敏感： 65 偏高"
  ],
  "ref": "非默认：水分38(<40偏低)、油分62(>55偏高)、色素70(>60偏高)、毛孔55(≤60正常)、敏感65(>50敏感倾向)；综合外油内干+敏感。默认value(50/42/45/40/30)输出中性/混合各项正常，注入失败即不命中"
},
{
  "slug": "beauty/assessor-risk-12",
  "inputs": {
    "productName": "测试面霜",
    "productType": "儿童化妆品"
  },
  "clicks": [
    "items.forEach(function(it,i){document.getElementById('c'+i).value='2';});['c0','c6','c7','c8'].forEach(function(k){document.getElementById(k).value='0';});calc()"
  ],
  "expect": [
    "70.6%",
    "48/68",
    "产品：测试面霜（儿童化妆品）"
  ],
  "ref": "16 条检查项（select id = c0..c15，运行期生成），权重合计 34 ⇒ maxScore = 34×2 = 68。clicks 先全置「2（符合）」再把 c0(w3)/c6(w3)/c7(w3)/c8(w1) 置「0（不符合）」⇒ score = 68 − 2×10 = **48**，pct = 48/68 = **70.6%** ⇒ 风险等级「中风险」（≥70），不合规项 4 条。inputs 另注入 productName/productType（静态控件，默认 value 为空串），结论句输出「产品：测试面霜（儿童化妆品）」。默认态（clicks 清空 + productName 回退空串）⇒ 全 0 分、产品名为「该产品」，三串均不命中。原 expect「0/68」是默认态分母常量（判别器亦判定 inputs 与默认值相同 ⇒ 被静默跳过）。"
},
{
  "slug": "beauty/calc-1",
  "inputs": {
    "q1": "dry|2"
  },
  "expect": [
    "dry"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/calc-2",
  "inputs": {
    "tone": "light"
  },
  "expect": [
    "C/NC15-NC20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/checker-14",
  "clicks": [
    "var __lv=['4','3','2','1'];dims.forEach(function(d,di){d.items.forEach(function(it,ii){document.getElementById('d'+di+'i'+ii).value=__lv[di];});});calc()"
  ],
  "expect": [
    "63.6%",
    "89/140"
  ],
  "ref": "4 维度×4 项的选择框 id 全由 buildList() 运行期拼 innerHTML 生成（静态源码 grep 不到 select）⇒ 用 clicks 在页面作用域按 `d{di}i{ii}` 写入分值再 calc()。注入：感官全「4」、理化全「3」、微生物全「2」、包装全「1」⇒ dimW=32/40/40/28（各项权重 w×4 求和），总分 = 4×8+3×10+2×10+1×7 = 89，pct = 89/140 = 63.6% ⇒「合格」。默认态（clicks 被清空）各 select 读空串 ⇒ 0 分 0.0%，两串均不命中。原 expect「有效成分含量在标示量90%-110%范围内」是 checklist 里的**题干文案**（默认全渲染即命中，常量型逃生项）。"
},
{
  "slug": "beauty/checker-assessor-1",
  "clicks": [
    "var __lv={plan:'5',do:'4',check:'2',act:'1'};Object.keys(__lv).forEach(function(k){stages[k].forEach(function(q,i){document.getElementById(k+i).value=__lv[k];});});calc()"
  ],
  "expect": [
    "3.00/5，等级：发展中",
    "改进、检查阶段"
  ],
  "ref": "PDCA 四阶段各 4 项（select id 由 buildList 运行期生成，形如 plan0/do0/check0/act0）⇒ clicks 按阶段写分再 calc()。注入 plan=5、do=4、check=2、act=1 ⇒ 阶段均分 5.00/4.00/2.00/1.00，综合 = (5+4+2+1)/4 = **3.00** ⇒ 等级「发展中」（2.5≤overall<3.5）；结论句的薄弱阶段拼接为「改进、检查」（reduce 从 check 起把 act 前置）。默认态 16 个 select 读空串 ⇒ 全 0 分、等级「薄弱」，两串均不命中。原 expect「0.00/5」是默认态常量（且与注入无关）。"
},
{
  "slug": "beauty/checker-assessor-2",
  "clicks": [
    "var __lv={check:'5',durability:'4',aesthetics:'2'};Object.keys(__lv).forEach(function(k){dims[k].items.forEach(function(it,i){document.getElementById(k+i).value=__lv[k];});});calc()"
  ],
  "expect": [
    "综合质量评分 76.0%，等级：良好",
    "40.0%"
  ],
  "ref": "三维各 5 项（id 由 buildList 生成：check0..4 / durability0..4 / aesthetics0..4）⇒ clicks 按维度写分再 calc()。注入 质量=5、持久=4、美观=2 ⇒ 各维满分（w 和×5）分别 65/55/50，得分 65/44/20 ⇒ 100.0%/80.0%/40.0%；综合 = 100×0.4 + 80×0.3 + 40×0.3 = **76.0** ⇒「良好」。默认态各 select 读空串 ⇒ 全 0 分「不合格」，两串均不命中。原 expect「质量40%+持久30%+美观30%」是 stat-card 里的**常量文案**（与输入无关）。注意：**不可锚「不合格」**（3 分类页的默认态/低分态都会出现该词）。"
},
{
  "slug": "beauty/face-hair-match",
  "clicks": [
    "selectFace('long')"
  ],
  "expect": [
    "长脸需要缩短面部视觉比例",
    "齐刘海必备"
  ],
  "ref": "页面 input/select/textarea 计数为 0；脸型卡片由 renderGrid() 拼 innerHTML（`<div class=\"face-btn\" onclick=\"selectFace('long')\">`），状态是顶层 `let currentFace='oval'` ⇒ clicks 直接调用 selectFace('long')（内部再 renderGrid/renderResult）。注入后 result 区输出长脸 tip「长脸需要缩短面部视觉比例，齐刘海是最佳选择。」与「建议长度：短发或中发为佳 / 适合刘海：齐刘海必备」。默认态为「鹅蛋脸」，两串均不命中（**不可锚「长脸」二字** —— 默认态 faceGrid 会渲染全部 7 个脸型名称）。原 expect「重点在于突出面部轮廓优势」恰是默认脸型（鹅蛋脸）的 tip，常量型逃生项。"
},
{
  "slug": "beauty/hair-color",
  "inputs": {
    "bleachLevel": "6"
  },
  "expect": [
    "6-7度可以驾驭大部分潮色"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/hair-dye-ratio",
  "inputs": {
    "colorAmt": "90"
  },
  "expect": [
    "180g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/makeup-shade",
  "clicks": [
    "currentSkinTone='warm';currentOccasion='date';currentFamily='all';generateRecommendation()"
  ],
  "expect": [
    "暖皮适合橘红色、南瓜色系",
    "约会可以选择带光泽感的质地"
  ],
  "ref": "input/select/textarea 计数为 0；肤色/场合靠 `.skin-tone-card`（onclick=setSkinTone）与 `.occasion-tabs button`（onclick=setOccasion）选择，状态是顶层 `let currentSkinTone/currentOccasion/currentFamily` ⇒ clicks 直接写状态再 generateRecommendation()（setSkinTone 内的 `querySelectorAll('.skin-tone-card')` 在桩下返回空数组，forEach 静默无操作，不抛错）。注入 warm + date ⇒ 搭配建议输出「暖皮适合橘红色、南瓜色系，避免过于冷调的玫红色」与「约会可以选择带光泽感的质地，更有亲和力」。默认态是 neutral + daily，两串均不命中。原 expect「雅诗兰黛420」是默认态（中性皮·日常通勤）推荐列表里的口红色号，常量型逃生项。"
},
{
  "slug": "beauty/nail-color-harmony",
  "clicks": [
    "pickColor(1,'#000000');pickColor(2,'#E74C3C')"
  ],
  "expect": [
    "无彩色+有彩色",
    "黑色搭配正红"
  ],
  "ref": "input/select/textarea 计数为 0；色卡由 renderSwatches() 拼 innerHTML（onclick=pickColor(which,hex)），状态是顶层 `let color1=colors[0];let color2=colors[5]` ⇒ clicks 调 pickColor 两次（每次内部 calc()）。注入 黑(#000000, h=null) + 正红(#E74C3C, h=0) ⇒ 命中「含黑/白/灰」分支 ⇒ relation = **无彩色+有彩色**、score = 85（两色明度均 <160 ⇒ light1===light2 且非双浅，不加不减）；advice = 「黑色搭配正红，简洁大方且突出彩色，是安全的高分搭配。」。默认态（正红 h=0 vs 嫩绿 h=75 ⇒ hueDiff 75）落在「中差色搭配」，两串均不命中。原 expect「100」是默认态得分（且是纯数字短串，易撞页内其它数字）。"
},
{
  "slug": "beauty/perming-rod",
  "inputs": {
    "targetCurl": "tight"
  },
  "expect": [
    "tight"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/rater-nail",
  "inputs": {
    "c1": "#f5d6c6_X",
    "c2": "#d63384",
    "c3": "#ffd43b"
  },
  "expect": [
    "f5d6c6_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/recommender-cycle",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore(default-hit)（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "beauty/recommender-face-shape",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/skin-tewl",
  "clicks": [
    "questions.forEach(function(q,qi){selectOpt(qi,0);});calcScore()"
  ],
  "expect": [
    "32 / 32 分",
    "重度流失"
  ],
  "ref": "input/select/textarea 计数为 0；8 道题由 renderQuiz() 拼 innerHTML（`<div class=\"opt-btn\" onclick=\"selectOpt(qi,oi)\">`），状态是顶层 `let answers=new Array(8).fill(null)` ⇒ clicks 先逐题选第 0 项（每题分值 4）再 calcScore()。注入后 totalScore = 8×4 = **32**，maxScore = 8×4 = 32 ⇒ 显示「32 / 32 分」，totalScore>26 ⇒「重度流失」+「皮肤屏障严重受损…」建议。默认态 8 题全 null ⇒ calcScore() 在 `answers.some(a=>a===null)` 处早退（仅弹 toast），结果区为空，两串均不命中。原 expect「1000-1500ml」是第 8 题**选项文案**（默认态 quiz 渲染即含，常量型逃生项）。"
},
{
  "slug": "beauty/skincare-routine",
  "inputs": {
    "ageGroup": "25"
  },
  "expect": [
    "25-30岁"
  ],
  "ref": "auto-restore"
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
  console.log("==== beauty calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
