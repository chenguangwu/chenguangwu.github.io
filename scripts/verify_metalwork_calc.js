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
const fs = require("fs");
globalThis.__tbFs = fs; // 供 clicks 内做源码形态判别（harness 点击串无 require）
const path = require("path");
const RECORDER_PATH = path.join(__dirname, "..", "tools", "metalwork", "recorder-9.html");

// 640 复核失败：syncTargetTemp() 对非法目标只标红，但 calcSoaking() 用 `+value || 0`
// 把当前目标改成 0，后续偏差、记录与导出继续按无效目标运行。
function recorderStaticChecks() {
  const src = fs.readFileSync(RECORDER_PATH, "utf8");
  const i = src.indexOf("function calcSoaking(");
  const j = src.indexOf("\nfunction ", i + 1);
  const body = i < 0 ? "" : src.slice(i, j < 0 ? src.length : j);
  return [
    {
      name: "保温计算不再用空/非法目标覆盖当前目标",
      ok: !/\+document\.getElementById\('targetTemp'\)\.value *\|\| *0/.test(body)
        && /tRaw!==''&&isFinite\(t\)&&t>0\) current\.target=t/.test(body),
    },
  ];
}

const CASES = [
  {
    slug: "metalwork/thread-spec",
    clicks: ["var __cap=null;TBKit={util:{isEn:function(){return false;},exportTable:function(sel,name){__cap={sel:sel,name:name};},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}}};var __oq=document.querySelector;document.querySelector=function(s){return {querySelectorAll:function(q){return [{tagName:'TR'}];}};};__thread_specExport();document.querySelector=__oq;document.getElementById('__tbProbe').textContent='EXPT sel='+(__cap?__cap.sel:'NA')+' name='+(__cap?__cap.name:'NA');"],
    expect: ["EXPT sel=#tableWrap name=thread-spec.csv"],
    ref: "复核失败重做·F-N189 第46批 螺纹规格：导出目标应是真实业务明细容器，而非历史记录表。旧实现把 TBKit.util.exportTable 指向 #<pre>Table（历史摘要），修复后指向该页业务明细容器。用例桩捕获 exportTable 的选择器与文件名，默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
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
{
  "slug": "metalwork/analysis-36",
  "inputs": { "qty": "500", "data": "气孔,-5,2" },
  "expect": ["数量须为正数，权重须在 1–3"],
  "ref": "993 计数/权重守卫：数量 -5 旧版照常算负总数与负缺陷率；修复后整表拒绝并提示范围，默认态合法不命中。"
},
{
  "slug": "metalwork/analysis-36",
  "inputs": { "qty": "500", "data": "<svg/onload=alert(1)>,45,2\n缩松,28,3" },
  "expect": [
    "&lt;svg/onload=alert(1)&gt;"
  ],
  "ref": "转义：缺陷类型名来自用户输入并拼进明细表与「数量最多缺陷」；未转义时 &lt;svg onload&gt; 会被当作标签执行。转义后实体文本保留。默认数据不含尖括号，不命中。"
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

  { slug: "metalwork/calc-gear-2",
    inputs: { module: "3", teeth: "20", helix: "20", method: "hob", vc: "60", feed: "1", material: "carbon" },
    expect: ["65.64", "52.95", "55.95"],
    ref: "斜齿 β=20°：mn=3×cos20°=2.819，da=60+2×2.819=65.64，df=60−2.5×2.819=52.95，αt=atan(tan20°/cos20°)=21.173°，db=60×cos21.173°=55.95；默认直齿 β=0 得 da=66.00/df=52.50/db=56.38，不含这三个串" },

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
    ref: "1<ratedV=6≤8.7 → 试验电压=2.5×6×1000+2000=17000 V=17.0 kV；温度修正系数=2^((40−20)/10)=4，R₂₀=10×4=40.0 MΩ·km（默认 ratedV0.6→3.5kV，避开）" },

  { slug: "metalwork/tester-19",
    inputs: { cableType: "pvc", ir: "1", temp: "40", cr: "0.2", cs: "2.5", ratedV: "0.6", len: "100" },
    expect: ["4.0 MΩ·km"],
    ref: "983 温度修正方向：实测 1 MΩ·km @ 40℃ 修正到 20℃ 应为 1×2^((40−20)/10)=4.0 MΩ·km；旧版用 0.5 指数得 0.25 且误判不合格。默认 temp=20/ir=500 → 500.0，不命中 4.0。" },

  { slug: "metalwork/tester-19",
    inputs: { cableType: "pvc", ir: "500", temp: "20", cr: "", cs: "70", ratedV: "0.6", len: "100" },
    expect: ["请输入有效参数（绝缘电阻、导体电阻、长度与额定电压须为正数，温度为有限数值）"],
    ref: "983 空值守卫：cr 清空后旧版 `+''||0` 得 0，0≤0.268×1.1 直接判导体合格；修复后 parseFloat('')=NaN 拦截。默认 cr=0.268 不命中该提示。" },

  { slug: "metalwork/thread",
    inputs: { threadType: "metric", diameter: "24", pitch: "3", material: "carbon",
              threadDir: "external", batch: "single" },
    expect: ["22.05", "20.32"],
    ref: "d2=d−0.64952P=24−1.94856=22.05；d1=d−1.22687P=24−3.68061=20.32（默认 d10/P1.5→9.03/8.16，避开）" },

  { slug: "metalwork/thread",
    inputs: { threadType: "metric", diameter: "40", pitch: "2", material: "carbon",
              threadDir: "external", batch: "medium" },
    expect: ["铣削螺纹 573"],
    ref: "985 备选转速与 vc 同比例：vc=60 m/min，基础 n=1000×60/(π×40)=477 rpm；铣削 vc×1.2=72 m/min，按同页 n=1000vc/(πd) 应为 573 rpm（旧版 n×0.8=382，与 vc 反向变动）。默认 batch=single 无该备选行，不命中。" },


  { slug: "metalwork/welding-heat",
    inputs: { current: "200", voltage: "25", speed: "30", eff: "0.8" },
    expect: [ "0.850 kJ/mm" ],
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
  "slug": "metalwork/analysis-cost-price-5",
  "inputs": {
    "data": "<svg/onload=alert(1)>,52000\n54500"
  },
  "expect": [
    "&lt;svg/onload=alert(1)&gt;"
  ],
  "ref": "转义：期次名取自「期次,价格」行首并拼进表格；未转义时 &lt;svg onload&gt; 会被当作标签执行。转义后实体文本保留。默认输入为纯数值，不命中。"
},
{
  "slug": "metalwork/analysis-cost-price-5",
  "inputs": { "data": "10\n-10" },
  "expect": ["价格须为非负有限数值"],
  "ref": "993 负价守卫（替代 973 零均值旧锚）：价格 -10 旧版参与均值/CV/回撤统计并制造零均值假合规；修复后整列拒绝并提示非负。合法默认期价格不含该串。"
},
{
  "slug": "metalwork/analysis-cost-price-5",
  "inputs": { "data": "0\n10\n20" },
  "expect": ["无法计算（首期为 0）"],
  "ref": "973 首期零除零：数据 0/10/20 首期=0，首末涨跌幅 (末−首)/首 除零无定义，应显示「—/无法计算（首期为 0）」；修复前显示 Infinity%。默认数据首期≠0 不含该串。"
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
  "slug": "metalwork/analysis-35",
  "inputs": { "trials": "6", "data": "飞边,-4,2\n欠铸,2,3" },
  "expect": ["已忽略 1 行", "次数须为正整数", "问题总数： 2"],
  "ref": "负数次数拦截（669）：飞边 -4 被拒并列出「次数须为正整数」，仅统计欠铸 2 个（修复前总数 -2、密度 -0.33、结论「问题较少」；默认 6/22 不含这些串）"
},
{
  "slug": "metalwork/analysis-35",
  "inputs": { "trials": "6", "data": "short shot,4,2\n飞边,4,2" },
  "expect": ["问题总数： 8"],
  "ref": "含空格问题名不再丢行（669）：仅按逗号/制表符切分，short shot 整名保留 ⇒ 总数 8、类型 2（修复前按空格切分导致该行被静默丢弃，总数 4、类型 1）。判别器实测「问题类型数： 2」在默认态也命中（默认数据恰为两类），已移除该逃生锚，仅保留依赖注入数据的总数 8（默认 22 不含）。"
},
{
  "slug": "metalwork/analysis-35",
  "inputs": { "trials": "6", "data": "short shot,-1,2" },
  "clicks": ["calc();var t=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='A35ALL '+((t.indexOf('（1 行无效）')>=0&&t.indexOf('short shot,-1,2')>=0&&t.indexOf('次数须为正整数')>=0)?'OK':'BAD:['+t+']');"],
  "expect": ["A35ALL OK"],
  "ref": "全行无效也必须列出被忽略行及原因（669 复核失败重做）：唯一数据行次数为 -1 ⇒ 无有效行，进入早退分支；修复前该分支只输出「请输入至少一行…（1 行无效）」后 return，后面的 skipped 逐条列表不执行，用户看不到「次数须为正整数」。现早退分支同样渲染 skipBox ⇒ 结果区同时含无效行数、行原文与原因。用单一探针串断言三项（expect 为「任一命中」，拆成三条会因「（1 行无效）」先命中而假通过）。默认数据无 -1 行且存在有效行 ⇒ 不进早退分支 ⇒ 探针 BAD。"
},
{
  "slug": "metalwork/analysis-35",
  "inputs": { "trials": "6", "data": "<svg/onload=alert(1)>,1,2" },
  "expect": ["&lt;svg/onload=alert(1)&gt;"],
  "ref": "问题名转义（669 复核 MM-H62）：标签被 escHtml 转义后输出 &lt;svg/onload=alert(1)&gt;，结果区不出现可执行 <svg>（默认数据不含该串）"
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
    ref: "结合力 0 级=100、厚度 48/40=1.2 倍=100、维氏 900HV（有机涂层要求 100HV）=100 → 综合 100 且三项全通过（997 后默认铅笔改为 HB，该用例改用维氏法仍与本值口径不同）" },

  { slug: "metalwork/detector-hardness",
    inputs: { "coatingType": "paint", "reqLevel": "2", "adhesionMethod": "crosscut",
              "crosscutGrade": "2", "thickMethod": "eddy", "thickness": "48",
              "stdThickness": "40", "thickTolerance": "4", "hardnessMethod": "pencil", "pencilGrade": "6B" },
    expect: ["涂层质量合格（未达标）"],
    ref: "结合力 2 级=65（要求≤1 级 → 不通过）、厚度 100、铅笔 6B=10 不通过 → 综合 65×0.4+100×0.3+10×0.3=59，评分档位为「涂层质量合格」，逐项不通过时等级文案须带「（未达标）」（默认档位为「良好」，与本值不重合）" },
  { slug: "metalwork/detector-hardness",
    inputs: { "coatingType": "paint", "reqLevel": "2", "adhesionMethod": "crosscut",
              "crosscutGrade": "0", "thickMethod": "eddy", "thickness": "48",
              "stdThickness": "40", "thickTolerance": "4", "hardnessMethod": "pencil" },
    expect: ["达标（48μm） 100 ✓ 涂层硬度 30% HB（中等） 46"],
    ref: "997 默认硬度档（MM-H136）：不注入 pencilGrade 时新默认 HB 满足油漆要求 HB（硬项 46 分、三项全通过），旧默认 6B 是 10 分且未达标。锚含 48μm 避开默认 50μm ⇒ 零逃生。" },

  { slug: "metalwork/thread",
    inputs: { threadType: "metric", diameter: "12", pitch: "1.75", material: "carbon",
              threadDir: "internal", batch: "single" },
    expect: ["小径 D1"],
    ref: "内螺纹小径 D1=d−1.08253P=12−1.8944=10.106mm（默认外螺纹 → 该卡片标签为「牙底直径 d3」，与本值不重合）" },
  { slug: "metalwork/forging-ratio", inputs: { "shape": "rect" }, expect: ["锻造比 K = 2.000", "F₁=90×80=7200mm²"], ref: " shape=矩形 ⇒ renderInputs 生成 w0=120/h0=120/w1=90/h1=80；a0=120×120=14400mm²、a1=90×80=7200mm² ⇒ K=2.000、ε=50.0%（默认圆形 d0=120/d1=70 ⇒ K=2.939、11310/3848mm²，与本值不重合；K=2<目标 3 ⇒ 未达标）" },
  { slug: "metalwork/surface-finish", inputs: { "inType": "ra", "inVal": "0.4" }, expect: ["对应 N5 级表面", "建议加工方法： 精车/精铣/精磨"], ref: " Ra=0.4 落在 0.4→N5 区间，命中最近邻档位 ⇒ 等级与建议加工方法随 Ra 变动" },
  { slug: "metalwork/temp-forging", inputs: { "material": "titanium", "weight": "20", "diameter": "80" }, expect: ["锻造温度范围 180 ℃", "约 14 min"], ref: " 钛合金 MAT_DATA 温度区间下限 180 ℃；加热 t=ceil(20·0.5+80·0.05)=14 min、保温 ceil(20·0.2)=4 min" },
  { slug: "metalwork/temp-forging", inputs: { material: "aluminum", weight: "10", diameter: "50" }, expect: ["最高加热（满量程 100%） 490℃"], ref: "995 温度条满量程（MM-H160）：铝合金 maxHeat=490℃，旧版满量程恒 1300 只画 38%；修复后以材料最高加热温度为满量程并在标签显示 100%。默认低碳钢虽同为 100%，但显示 1300℃，整串不命中 ⇒ 零逃生。" },
  { slug: "metalwork/zulinfeilvjisuan", inputs: { "value": "120000", "months": "24", "residual": "8", "rate": "6", "payType": "monthly", "mgmtFee": "2" }, expect: ["月租金 5093.00 元", "9.86%"], ref: " 残值 9600.00 → 本金 110400.00；管理费 120000·2%·2.0=4800.00；24 期、期利率 0.5000% ⇒ PMT 4892.9954，月租 5093.00；ROI 9.86%" },
  { slug: "metalwork/pressure-casting", inputs: { "weight": "10", "wall": "1.5", "material": "zinc", "batch": "mass" }, expect: ["压力铸造(压铸) 推荐方法", "最大重量 30 kg"], ref: " 锌 + 批量 mass 命中 METHODS 首项 ⇒ 压铸；壁厚 1.5 的工艺上限重量 30 kg" },

  // ── 零用例加固（2026-10-06）──────────────────────────
  { slug: "metalwork/detector-24", inputs: { defLen: "8", thick: "35", defCount: "3" }, expect: ["缺陷长度/板厚比=22.9%"], ref: "注入非默认(默认 defLen=5/thick=20/defCount=1)：独立复算 8/35 = 22.857% → 22.9%；GB/T 3323 分级 22.9% 超允许范围 ⇒ Ⅴ级（严重不合格）。⚠『Ⅴ级（严重不合格）』文案两态相同（默认 25.0% 同样超限）⇒ 不可作锚，只取比值串。默认态为 25.0%，不命中。" },
  { slug: "metalwork/detector-24", inputs: { defLen: "", thick: "20", defCount: "1" }, expect: ["缺陷长度须为正数"], ref: "空值拦截（668）：缺陷长度清空 ⇒ parseFloat('')=NaN，输出「请修正输入：缺陷长度须为正数。未进行档位评定。」（修复前空值按 0 计算并判 1 档；默认 5mm 不含该串）" },
  { slug: "metalwork/detector-24", inputs: { defLen: "5", thick: "20", defCount: "" }, expect: ["未填缺陷数量"], ref: "数量空值拦截（668）：缺陷数量清空 ⇒ 提示「未填缺陷数量（无缺陷请填 0）」，不再静默按 0 判 1 档（默认 1 个不含该串）" },
  { slug: "metalwork/detector-24", inputs: { defLen: "-5", thick: "", defCount: "-1" }, expect: ["缺陷长度须为正数；母材厚度须为正数；缺陷数量须为 ≥0 的整数"], ref: "负数/空值拦截（668）：defLen=-5、thick 清空、defCount=-1 ⇒ 三条错误同时列出，不再输出 1 档（默认 5/20/1 全合法，不含该串）" },
  { slug: "metalwork/analysis-simulator", inputs: { vol: "300", area: "150", runner: "15", fillrate: "70", tmelt: "260", tmold: "50", teject: "120", tw: "40", thick: "4", alpha: "0.05" }, expect: ["总充填体积 345 cm³", "充填时间 4.93 s", "冷却时间（近似） 40.63 s", "流程/壁厚比 0.5,000"], ref: "注入非默认(默认 200/100/10/50/240/60/110/30/3/0.04)：型腔+流道+浇口 300+15 与射胶量填充 ⇒ 总充填体积 345 cm³；充填时间 = 345/70 = 4.93 s；冷却时间近似 40.63 s；流程/壁厚比 = (300+15+…)/4 → 0.5,000。默认态 220 cm³/4.40 s/27.51 s/0.6,667，四条均不命中。" },
  { slug: "metalwork/analysis-simulator", inputs: { vol: "300", area: "150", runner: "15", fillrate: "70", tmelt: "240", tmold: "50", teject: "300", tw: "30", thick: "4", alpha: "0.05" }, expect: ["熔体温度＞顶出温度＞水温"], ref: "994 温度顺序守卫（MM-H122）：顶出 300℃ 高于熔体 240℃ 时旧版 ln 项为负仍出负冷却时间；修复后先拦截并要求 Tm>Te>Tw。默认 240/110/30 不含该串。" },
  { slug: "metalwork/detector-23", inputs: { nominal: "60.000", actual: "60.034", upperTol: "0.039", lowerTol: "0.000" }, expect: ["实测偏差： +0.0340 mm", "偏差占公差带：87.2%", "极限尺寸：60.0000 ~ 60.0390 mm"], ref: "注入非默认(默认 nominal=50.000/actual=50.025)：独立复算 偏差 = 60.034−60.000 = +0.0340 mm；公差带 0.0390 ⇒ 占比 0.034/0.039 = 87.2%；极限尺寸 = 60.0000 ~ 60.0390 mm。默认态 50.025/+0.0250/64.1%/50.0000~50.0390，三条均不命中（『合格』判定与 IT4/±0.005mm 两态相同，不作锚）。" },
  { slug: "metalwork/detector-23", inputs: { nominal: "60.000", actual: "60.034", upperTol: "-0.050", lowerTol: "0.050" }, expect: ["请输入有限尺寸，且上偏差须大于下偏差"], ref: "993 公差方向守卫：旧版空值 `||0` 与倒挂公差照算并归 IT01，修复后先拒绝上偏差≤下偏差；默认 0.039/0.000 不含该串。" },
  { slug: "metalwork/detector-mold", inputs: { tx: "70.000", ty: "40.000", tz: "25.000", ax: "70.021", ay: "39.975", az: "25.030", tol: "0.020" }, expect: ["X轴：+0.021 mm ✗ 超差", "Z轴：+0.030 mm ✗ 超差", "空间偏差：0.0443 mm"], ref: "注入非默认(默认 50/30/20 与实测 50.015/29.988/20.022)：三轴偏差 = +0.021 / −0.025 / +0.030 mm，均超 ±0.020 ⇒ 三轴全『✗ 超差』；空间偏差 = √(0.021²+0.025²+0.030²) = 0.0443 mm > 0.020。默认态仅 Z 轴超差、空间偏差 0.0292，三条均不命中。" },
  { slug: "metalwork/detector-mold", inputs: { tx: "50.000", ty: "30.000", tz: "20.000", ax: "50.015", ay: "29.988", az: "20.022", tol: "0" }, expect: ["公差须大于 0"], ref: "993 零公差守卫：旧版 tol=0 仍输出三轴超差与刀具补偿建议，修复后先拒绝非正公差；默认 ±0.020 不含该串。" },
  { slug: "metalwork/detector-mold", inputs: { tx: "50.000", ty: "30.000", tz: "20.000", ax: "50.019", ay: "30.019", az: "20.019", tol: "0.020" }, expect: ["空间偏差：0.0329 mm 公差要求：±0.020 mm 综合判定： 不合格（超差）"], ref: "994 空间偏差纳判定（MM-H139）：三轴各 +0.019 均未超 ±0.020，但空间偏差 √(3×0.019²)=0.0329>tol；旧版判「合格」，修复后判不合格。默认空间偏差 0.0292 且 Z 轴已超差，整串不命中。" },

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
    clicks: ["createJob();document.getElementById('targetTemp').value='900';syncTargetTemp();document.getElementById('__tbProbe').textContent='TGT '+current.target;"],
    expect: ["TGT 900"],
    ref: "目标温度编辑同步：createJob 后 current.target=850，把输入改为 900 再触发 syncTargetTemp ⇒ current.target 应为 900；旧实现 oninput 只调 renderCurrent，current.target 仍 850 ⇒ 探针『TGT 850』不命中。"
  },
  {
    slug: "metalwork/recorder-9",
    clicks: ["createJob();document.getElementById('logTemp').value='';addReading();document.getElementById('__tbProbe').textContent='READ '+current.readings.length;"],
    expect: ["READ 0"],
    ref: "测温值空输入拒绝：清空 logTemp 后 addReading 应提示并不落记录 ⇒ readings 长度 0；旧实现一元 `+''`=0 且 `!t&&t!==0` 对 0 放行，读数为 0℃ 入表 ⇒ 探针『READ 1』不命中。"
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
    slug: "metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html','utf8');document.getElementById('__tbProbe').textContent='SWAPRM '+(h.indexOf('swapValues')<0&&h.indexOf('互换 A/B')<0&&h.indexOf('onclick=\"swapValues()\"')<0?'OK':'BAD');"],
    expect: ["SWAPRM OK"],
    ref: "996量纲互换移除（MM-H157）：孔径 D（mm 正实数）与 IT 等级（5–10 整数）量纲不同，互换无业务意义；旧版仅凭两数同落 5–10 就互换，5.5/7 互换后 IT=5.5 被 calc 拒绝。修复后移除 ⇄ 按钮与 swapValues 函数；源码形态断言互换入口与函数均已消失，默认态不执行 clicks ⇒ 零逃生。"
  },
  {
    slug: "metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi",
    inputs: { v0: "5.5", v1: "7" },
    expect: ["D=5.5 可算"],
    ref: "996小数孔径回归：孔径 D=5.5（合法正实数）应能正常算出 IT 公差，而非报错。用 DOM 哨兵判定：结果容器出现「标准公差 IT」且无「等级需为 5–10」拒绝提示。旧版 5.5/7 单次 calc 本就能算（问题在互换），此用例仅做移除互换后的回归保护，判别力由 SWAPRM 用例承担。",
    clicks: ["var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent=(h.indexOf('标准公差 IT')>=0&&h.indexOf('等级需为 5–10')<0)?'D=5.5 可算':'BAD'"]
  },
  {
    slug: "metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi",
    inputs: { v0: "-50", v1: "7" },
    expect: ["孔径 D 须为正数"],
    ref: "996 孔径正值守卫（MM-H158）：旧版 cbrt(-50) 得负标准公差仍照常渲染；修复后先拦截 D≤0。默认 50 不含该串。"
  },
  {
    slug: "metalwork/wushua-zhinengyuqingliangduibijisuanqi",
    inputs: { v0: "60", v1: "85" },
    expect: ["25.0 综合差距"],
    ref: "注入非默认(默认 v0=90/v1=72→18.0 综合差距)：综合差距 = |60−85| = 25.0，按连续差值保留 1 位小数。默认态 |90−72|=18.0 不命中 25.0。v0=无刷评分、v1=轻量评分。"
  },
  {
    slug: "metalwork/wushua-zhinengyuqingliangduibijisuanqi",
    inputs: { v0: "90.5", v1: "72.2" },
    expect: ["18.3 综合差距"],
    ref: "983 小数精度：|90.5−72.2| = 18.3，差距按连续值保留 1 位小数（旧 toFixed(0) 记 18）。默认 90/72 → 18.0，不命中 18.3。"
  },
  {
    slug: "metalwork/zhineng-duogongnengyunaiyongduibijisuanqi",
    inputs: { v0: "85.5", v1: "78.2" },
    expect: ["7.3 综合差距"],
    ref: "983 小数精度：|85.5−78.2| = 7.3，差距按连续值保留 1 位小数（旧 toFixed(0) 记 7）。默认 85/78 → 7.0，不命中 7.3。"
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
    expect: ["20.0 综合差距"],
    ref: "注入非默认(默认 v0=85/v1=78→7.0 综合差距)：综合差距 = |70−90| = 20.0，按连续差值保留 1 位小数。默认态 |85−78|=7.0 不命中 20.0。v0=智能评分、v1=耐用评分。"
  },
  {
    "slug": "metalwork/analysis-simulator",
    "inputs": {
      "vol": "42",
      "area": "42",
      "runner": "42",
      "fillrate": "42",
      "tmelt": "42",
      "tmold": "42",
      "teject": "42",
      "tw": "42",
      "thick": "42",
      "alpha": "42"
    },
    "expect": [
      "熔体温度＞顶出温度＞水温"
    ],
    "ref": "994 温度顺序守卫同步：自动补强旧输入 tmelt=teject=tw=42 原在 ln 项 NaN 下仍输出「各项指标在常规区间」，属假合规；修复后统一拒绝 Tm≤Te≤Tw。默认态 240/110/30 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/cable-tray-sizing",
    "inputs": {
      "od": "42",
      "cnt": "42"
    },
    "expect": [
      "² 电缆总截面积 145471"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"od\":\"42\",\"cnt\":\"42\"}，输出区含「² 电缆总截面积 145471」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/assessor-34",
    "inputs": {
      "duration": "42",
      "stdDuration": "42",
      "corrosionArea": "42",
      "testType": "ass",
      "coating": "zn_ni",
      "blister": "2",
      "rust": "1",
      "cracking": "1",
      "rustType": "white",
      "reqGrade": "8"
    },
    "expect": [
      "结论： 耐盐雾性能不达标，腐蚀严重，需改进表面处理工艺或更换材料。 改进建议 • 腐蚀面积过大，建议增加涂层厚度或采用多层防护体系"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"duration\":\"42\",\"stdDuration\":\"42\",\"corrosionArea\":\"42\",\"testType\":\"ass\",\"coating\":\"zn_ni\",\"blister\":\"2\",\"rust\":\"1\",\"cracking\":\"1\",\"rustType\":\"white\",\"reqGrade\":\"8\"}，输出区含「结论： 耐盐雾性能不达标，腐蚀严重，需改进表面处理工艺或更换材料。 改进建议 •…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/calc-feed",
    "inputs": {
      "dia": "42",
      "z": "42",
      "vc": "42",
      "fz": "42"
    },
    "expect": [
      "度公式 Vf = 318 × 42 × 42 = 561498.6"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dia\":\"42\",\"z\":\"42\",\"vc\":\"42\",\"fz\":\"42\"}，输出区含「度公式 Vf = 318 × 42 × 42 = 561498.6」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/calc-gear-2",
    "inputs": {
      "module": "42",
      "teeth": "42",
      "vc": "42",
      "feed": "42",
      "method": "shape",
      "material": "alloy"
    },
    "expect": [
      " 1000 × 42 / (π × 1764.00) = 7.6"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"module\":\"42\",\"teeth\":\"42\",\"vc\":\"42\",\"feed\":\"42\",\"method\":\"shape\",\"material\":\"alloy\"}，输出区含「 1000 × 42 / (π × 1764.00) = 7.6」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/calc-stretch",
    "inputs": {
      "l0": "42",
      "l1": "42",
      "a0": "42",
      "a1": "42"
    },
    "expect": [
      "对收缩 ΔA = 42 - 42 = 0.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"l0\":\"42\",\"l1\":\"42\",\"a0\":\"42\",\"a1\":\"42\"}，输出区含「对收缩 ΔA = 42 - 42 = 0.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/calc-pressure-mold",
    "inputs": {
      "thickness": "42",
      "shear": "42",
      "perimeter": "42",
      "material": "midcarbon"
    },
    "expect": [
      " t × τ = 42 × 42 × 480 = 846.7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thickness\":\"42\",\"shear\":\"42\",\"perimeter\":\"42\",\"material\":\"midcarbon\"}，输出区含「 t × τ = 42 × 42 × 480 = 846.7」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/detector-21",
    "inputs": {
      "thickness": "42",
      "material": "nonferro",
      "defect": "subsurface",
      "level": "strict"
    },
    "expect": [
      " 详细说明 优势 内部缺陷灵敏度高 可测厚 无辐射 可现场检测 局限 对粗糙表面敏感 需耦合剂 缺陷定性需经验 对粗晶材料困难"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thickness\":\"42\",\"material\":\"nonferro\",\"defect\":\"subsurface\",\"level\":\"strict\"}，输出区含「 详细说明 优势 内部缺陷灵敏度高 可测厚 无辐射 可现场检测 局限 对粗糙表面…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/detector-23",
    "inputs": {
      "nominal": "42",
      "actual": "42",
      "upperTol": "42",
      "lowerTol": "42",
      "measureMethod": "offline"
    },
    "expect": [
      "请输入有限尺寸，且上偏差须大于下偏差"
    ],
    "ref": "993 公差方向守卫同步：自动补强旧输入 upperTol=lowerTol=42 原判「超差/尺寸偏小」，属倒挂公差假结果；修复后统一拒绝上偏差≤下偏差。默认态 0.039/0.000 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/detector-24",
    "inputs": {
      "defLen": "42",
      "thick": "42",
      "defCount": "42",
      "method": "ut"
    },
    "expect": [
      "评定区内缺陷数量：42 个 参考档位： 4 档（参考不合格） 缺陷指示长度=42mm，按本页尺寸阈值给出参考档位（未按波幅当量评定）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"defLen\":\"42\",\"thick\":\"42\",\"defCount\":\"42\",\"method\":\"ut\"}，输出区含「评定区内缺陷数量：42 个 参考档位： 4 档（参考不合格） 缺陷指示长度=42mm」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。668 批把「国家标准评定」降级为尺寸阈值参考档位并删去波幅当量表述。"
  },
  {
    "slug": "metalwork/detector-hardness",
    "inputs": {
      "pulloffVal": "42",
      "thickness": "42",
      "stdThickness": "42",
      "thickTolerance": "42",
      "vickersVal": "42",
      "nanoVal": "42",
      "adhesionMethod": "pulloff",
      "crosscutGrade": "1",
      "thickMethod": "magnetic",
      "hardnessMethod": "vickers",
      "pencilGrade": "5B",
      "coatingType": "zn",
      "reqLevel": "2"
    },
    "expect": [
      "pulloff\n1\n42\n42\n42\n42\nvickers\n5B\n42\n42\nzn\n2\n79"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pulloffVal\":\"42\",\"thickness\":\"42\",\"stdThickness\":\"42\",\"thickTolerance\":\"42\",\"vickersVal\":\"42\",\"nanoVal\":\"42\",\"adhesionMethod\":\"pulloff\",\"crosscutGrade\":\"1\",\"thickMethod\":\"magnetic\",\"hardnessMethod\":\"vickers\",\"pencilGrade\":\"5B\",\"coatingType\":\"zn\",\"reqLevel\":\"2\"}，输出区含「pulloff\n1\n42\n42\n42\n42\nvickers\n5B\n42\n42\nz…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/detector-mold",
    "inputs": {
      "ptName": "abc123测试",
      "tx": "42",
      "ty": "42",
      "tz": "42",
      "ax": "42",
      "ay": "42",
      "az": "42",
      "tol": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\nP2\n测量点：abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ptName\":\"abc123测试\",\"tx\":\"42\",\"ty\":\"42\",\"tz\":\"42\",\"ax\":\"42\",\"ay\":\"42\",\"az\":\"42\",\"tol\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\nP2\n测量点：abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/forging-ratio",
    "inputs": {
      "targetRatio": "42",
      "mode": "upset",
      "shape": "rect"
    },
    "expect": [
      "分步计算 步骤1 H₀=200mm，H₁=80mm，K=H₀/H₁=200/80 = 2.500"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"targetRatio\":\"42\",\"mode\":\"upset\",\"shape\":\"rect\"}，输出区含「分步计算 步骤1 H₀=200mm，H₁=80mm，K=H₀/H₁=200/80…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/diandonggongju-xifen",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "） 推荐机型 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\"}，输出区含「） 推荐机型 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/lifespan-1",
    "inputs": {
      "power": "42",
      "capacity": "42",
      "voltage": "42",
      "efficiency": "42",
      "dod": "42",
      "batType": "lipo"
    },
    "expect": [
      "续航时间 T = 0.03 / 42 = 0.00 h (0小时0分) ⚠️ 续航不足1小时，建议增大电池容量或降低功耗"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"power\":\"42\",\"capacity\":\"42\",\"voltage\":\"42\",\"efficiency\":\"42\",\"dod\":\"42\",\"batType\":\"lipo\"}，输出区含「续航时间 T = 0.03 / 42 = 0.00 h (0小时0分) ⚠️ 续…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/pinpaijiazhipinggujisuan",
    "inputs": {
      "revenue": "42",
      "profitRate": "42",
      "multiplier": "42",
      "yearFactor": "42",
      "marketShare": "42",
      "industry": "consumer"
    },
    "expect": [
      "请输入有效年限系数(0.5–3)"
    ],
    "ref": "995 年限范围同步：自动补强旧输入 yearFactor=42 原照常估算品牌价值，修复后按页面占位范围 0.5–3 拒绝。默认态 1.2 不含该串 ⇒ 强判别、零逃生。",
  },
  {
    "slug": "metalwork/pinpaijiazhipinggujisuan",
    "inputs": { revenue: "5000", profitRate: "90", multiplier: "5", yearFactor: "1.2", marketShare: "10", industry: "metalwork" },
    "expect": ["请输入有效品牌利润率(1-80)"],
    "ref": "995 利润率上限（MM-H142）：输入框自带 max=80，键盘输 90 旧版仍按 100 上限出估值；修复后按同页口径拒绝。默认 15% 不含该串 ⇒ 零逃生。"
  },
  {
    "slug": "metalwork/pressure-casting",
    "inputs": {
      "weight": "42",
      "wall": "42",
      "material": "steel",
      "batch": "medium"
    },
    "expect": [
      "量 单件~大批量 其他可选方法 方法 精度 表面 成本 熔模铸造(失蜡) CT4-CT7 Ra 1.6-6.3μm 高"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"wall\":\"42\",\"material\":\"steel\",\"batch\":\"medium\"}，输出区含「量 单件~大批量 其他可选方法 方法 精度 表面 成本 熔模铸造(失蜡) CT4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/recorder-9",
    "inputs": {
      "thickness": "42",
      "targetTemp": "42",
      "logTemp": "42",
      "logNote": "abc123测试",
      "processType": "正火"
    },
    "expect": [
      "0 ℃ 最高温度 42℃\n保温时间：70 分钟（约 1.2 小时）\n目标 42℃ 92℃ -8℃"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thickness\":\"42\",\"targetTemp\":\"42\",\"logTemp\":\"42\",\"logNote\":\"abc123测试\",\"processType\":\"正火\"}，输出区含「0 ℃ 最高温度 42℃\n保温时间：70 分钟（约 1.2 小时）\n目标 42℃…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/sheet-bend",
    "inputs": {
      "thickness": "42",
      "radius": "42",
      "angle": "42",
      "l1": "42",
      "l2": "42",
      "kfactor": "0.40"
    },
    "expect": [
      "2 − BD = 42 + 42 − 21.387 = 62.613 mm 结论 42mm 板、R42mm、42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thickness\":\"42\",\"radius\":\"42\",\"angle\":\"42\",\"l1\":\"42\",\"l2\":\"42\",\"kfactor\":\"0.40\"}，输出区含「2 − BD = 42 + 42 − 21.387 = 62.613 mm 结论…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/surface-finish",
    "inputs": {
      "inVal": "42",
      "inType": "rz"
    },
    "expect": [
      "面 火焰切割面\nrz\n42\n对应 NN10 级表面 12.5 Ra (μm) 50"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inVal\":\"42\",\"inType\":\"rz\"}，输出区含「面 火焰切割面\nrz\n42\n对应 NN10 级表面 12.5 Ra (μm) 5…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/resistance-2",
    "inputs": {
      "thickness": "42",
      "material": "alloy",
      "joint": "lap",
      "plateType": "medium"
    },
    "expect": [
      "42\nalloy\nlap\nthick\n埋弧焊 推荐方法 焊剂(无气体) 保护方式 高 焊缝质量 中"
    ],
    "ref": "995 板厚档位同步：厚度 42mm 按页内口径应归厚板(thick)，旧版沿用注入的 medium 仍可出同一方法；修复后 select 与评分统一由厚度派生。默认态 3mm/sheet 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/speed-itinerary",
    "inputs": {
      "length": "42",
      "vc": "42",
      "depth": "42",
      "feed": "42",
      "allowance": "42",
      "overrun": "42",
      "material": "alloy"
    },
    "expect": [
      " 每刀进给行程数 1 往复（L/f=42/42） 总往复次数 1 × 1 = 1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"length\":\"42\",\"vc\":\"42\",\"depth\":\"42\",\"feed\":\"42\",\"allowance\":\"42\",\"overrun\":\"42\",\"material\":\"alloy\"}，输出区含「 每刀进给行程数 1 往复（L/f=42/42） 总往复次数 1 × 1 = 1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/temp-forging",
    "inputs": {
      "weight": "42",
      "diameter": "42",
      "material": "midcarbon"
    },
    "expect": [
      ") 锻造温度参数 常用结构钢，锻造性能良好 始锻温度 120"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"diameter\":\"42\",\"material\":\"midcarbon\"}，输出区含「) 锻造温度参数 常用结构钢，锻造性能良好 始锻温度 120」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "metalwork/tester-19",
    "inputs": {
      "ir": "42",
      "temp": "42",
      "cr": "42",
      "ratedV": "42",
      "len": "42",
      "cableType": "xlpe",
      "cs": "4"
    },
    "expect": [
      "间 = 5 分钟 ✗ 综合判定：不合格 — 存在不达标项目，需排查故障点并整改后复测"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ir\":\"42\",\"temp\":\"42\",\"cr\":\"42\",\"ratedV\":\"42\",\"len\":\"42\",\"cableType\":\"xlpe\",\"cs\":\"4\"}，输出区含「间 = 5 分钟 ✗ 综合判定：不合格 — 存在不达标项目，需排查故障点并整改后…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/thread-spec",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "abc123测试\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「abc123测试\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。 [被覆盖的前条说明：⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。]"
  },
  {
    "slug": "metalwork/welding-heat",
    "inputs": {
      "current": "42",
      "voltage": "42",
      "speed": "42",
      "eff": "42",
      "process": "0.80"
    },
    "expect": [
      "输入 E ≈ 0.202 kJ/mm 2016 J/cm 2.02 kJ/cm 0.202"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"current\":\"42\",\"voltage\":\"42\",\"speed\":\"42\",\"eff\":\"42\",\"process\":\"0.80\"}，输出区含「输入 E ≈ 0.202 kJ/mm 2016 J/cm 2.02 kJ/cm …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/thread",
    "inputs": {
      "diameter": "42",
      "pitch": "42",
      "threadType": "unified",
      "material": "alloy",
      "threadDir": "internal",
      "batch": "medium"
    },
    "expect": [
      "螺距相对直径过大"
    ],
    "ref": "985 几何守卫（原自动补强用例同步）：注入 diameter=42/pitch=42 内螺纹，旧版输出负牙底直径 -3.466 mm 与 0.0 mm 底孔；修复后小径/中径/底孔出现非正值即拦截并提示「螺距相对直径过大」。默认 10×1.5 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/wushua-zhinengyuqingliangduibijisuanqi",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "两方案持平"
    ],
    "ref": "973 相等分值修正 + 983 判别力加固：注入 v0=v1=42，A=B 应判「两方案持平」。权重 50.0% 在旧版 A=B 时同样成立，属假绿锚，故只保留「两方案持平」作判别。默认 90/72 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/yuanlingongju-xifen",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "42\n42\n0 W 功率差 修剪机（高功率·粗枝） 推荐机型 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\"}，输出区含「42\n42\n0 W 功率差 修剪机（高功率·粗枝） 推荐机型 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/zhineng-duogongnengyunaiyongduibijisuanqi",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "两方案持平"
    ],
    "ref": "983 相等分值修正 + 判别力加固：注入 v0=v1=42，A=B 应判「两方案持平」。权重 50.0% 在旧版 A=B 时同样成立，属假绿锚，故只保留「两方案持平」作判别。默认 85/78 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/zulinfeilvjisuan",
    "inputs": {
      "value": "42",
      "months": "42",
      "residual": "42",
      "rate": "42",
      "mgmtFee": "42",
      "payType": "monthly_advance"
    },
    "expect": [
      "率 租赁方案（原值42元 / 42个月 / 月付(期初)） 设备原值 42.00 元 残值 42 × 42% = 17.64 元 需回收本金 42 - 18 = 24.36 元 总管理费 42 × 42% × 3.5年 = 61.74 元 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"value\":\"42\",\"months\":\"42\",\"residual\":\"42\",\"rate\":\"42\",\"mgmtFee\":\"42\",\"payType\":\"monthly_advance\"}，输出区含「率 租赁方案（原值42元 / 42个月 / 月付(期初)） 设备原值 42.00…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "metalwork/detector-55",
    "clicks": [
      "for(var m=0;m<3;m++){for(var i=0;i<6;i++){document.getElementById('m'+m+'_'+i).value='2';}}calc()"
    ],
    "expect": ["100%", "优秀"],
    "ref": "维修服务质量评分：3 模块 × 6 项、每项满分 2 ⇒ 总满分 36；18 个运行时下拉在页面作用域内逐一置「完全执行(2)」后调 calc() ⇒ 实得 36/36 = 100% ≥90 且无关键项缺失 ⇒「优秀」。"
       + "默认态（不执行 clicks）各下拉取不到值（+''=0）⇒ 实得 0%、★ 关键安全项未执行 ⇒「不合格（关键项未执行）」并压到 59%，两锚均不命中。"
       + "（下拉由 innerHTML 运行时生成，pageDefaults 取不到，故改用 clicks 显式驱动，避免进入 skip。）"
  },
  {
    "slug": "metalwork/detector-55",
    "clicks": [
      "var oldRef=(typeof TBKit!=='undefined'&&TBKit.chart)?TBKit.chart.refBar:null;var cap=null;if(typeof TBKit==='undefined'){TBKit={util:{isEn:function(){return false;}},chart:{},matrix:{},history:{},preset:{}};}if(!TBKit.chart)TBKit.chart={};TBKit.chart.refBar=function(sel,opt){cap=opt;};if(typeof calc==='function')calc();TBKit.chart.refBar=oldRef;var s=(cap&&cap.bands)?cap.bands.map(function(b){return (b.lo===null?'null':b.lo)+'-'+(b.hi===null?'null':b.hi)+'-'+(b.label&&b.label.zh?b.label.zh:'');}).join('|'):'NONE';document.getElementById('__tbProbe').textContent='BANDS '+s;"
    ],
    "expect": ["BANDS 90-null-优秀|75-90-良好|60-75-合格|null-60-不合格"],
    "ref": "994 标尺区间（MM-H131）：旧版第三段 lo:null/hi:75 把 <60 的不合格也标成合格；修复后补 60–75 合格段与 null–60 不合格段。探针截取 refBar 的 bands 实参，默认态不执行 clicks、无探针串 ⇒ 零逃生。"
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

  const stat = recorderStaticChecks();
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== metalwork calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();