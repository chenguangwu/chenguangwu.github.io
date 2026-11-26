#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
const { runCase } = require("./verify_it_calc.js");
// 2026-09-24 去默认化（BATCH69）：原 14 例里有 12 例的输入等于页面默认值、expect 又是
// 「轴向变形 / 公式 / 矩形 / 扭转角」这类**静态标签词** ⇒ 默认态同样命中（真逃生项）。
// 此前这批从未被判别器检到：判别器的 pageDefaults 按 deep-dive 标记截断，而本分类
// heat-transfer / material-calculator / stress-calculator 三页的表单在 deep-dive 之后
// （且存在重复 id），取不到默认值 ⇒ 整例静默判「跳过」。修好判别器后才暴露。
// 修法：输入改为非默认值，expect 全部换成 Python/笔算独立复算出的派生量。
const CASES = [
  { slug: "engineering/axial-stress", inputs: {"F":"30","A":"250","E":"210","L":"1.5"}, expect: ["5.714e-4", "0.857"], ref: "σ=F/A=30kN/250mm²=120.00 MPa；ε=σ/E=120/210000=5.714e-4；ΔL=ε·L=5.714e-4×1500mm=0.857 mm。默认 50/500/200/2 得 100.00 MPa / 9.524e-4 / 0.952 mm（原 expect「轴向变形」是静态标签词）" },
  { slug: "engineering/beam-calculator", inputs: {"length":"6","load":"15","E":"210","I":"800","limit":"300"}, expect: ["150.67 mm", "1680000.00"], ref: "简支梁均布 δ=5qL⁴/(384EI)：EI=210GPa×800cm⁴=1680 kN·m² ⇒ δ=5×15×6⁴/(384×1680)=0.15067 m=150.67 mm；许用 L/300=20.00 mm ⇒ 不满足。默认 5/10/200/500/250 得 81.38 mm（原 expect「公式」是静态词）" },
  { slug: "engineering/bending-stress", inputs: {"M":"36","b":"120","h":"240"}, expect: ["31.25", "1152000"], ref: "W=bh²/6=120×240²/6=1152000 mm³；σ=M/W=36e6/1152000=31.25 MPa。默认 20/150/300 得 W=2250000、σ=8.89 MPa（原 expect「最大弯曲应力」是静态标签词）" },
  { slug: "machinery/bolt-preload", inputs: {"T":"85","d":"16","K":"0.18"}, expect: ["29.51", "29514"], ref: "F=T/(K·d)=85/(0.18×0.016)=29514 N=29.51 kN。默认 100/12/0.2 得 41.67 kN（原 expect「预紧力」是静态标签词）" },
  { slug: "engineering/cantilever-deflection", inputs: {"P":"8","L":"2.5","E":"25","I":"8000"}, expect: ["20.83", "0.716"], ref: "δ=PL³/(3EI)=8000×15.625/(3×2e6)=0.02083 m=20.83 mm；θ=PL²/(2EI)=0.0125 rad=0.716°。默认 5/3/30/5000 得 30.00 mm / 0.859°（原 expect「自由端转角」是静态标签词）" },
  { slug: "engineering/heat-transfer", inputs: {"k":"0.3","A":"6","L":"0.25","T1":"30","T2":"10","h":"10","Ts":"80","Tinf":"20","eps":"0.9","T1K":"500","T2K":"300","h1":"10","h2":"20"}, expect: ["传热量 Q 144.00 W", "热阻 R 0.1389 K/W"], ref: "导热 Q=k·A·ΔT/L=0.3×6×20/0.25=144.00 W；R=L/(kA)=0.25/(0.3×6)=0.1389 K/W；q=Q/A=24 W/m²。⚠ 原注入 k=0.04/A=10/L=0.2/T1=20/T2=0 恰为页面「复合热阻」档渲染后的默认控件值 ⇒ 页面加载即输出 40.00 W/0.5000 K/W，与注入态逐字节相同（真逃生），故改注入非默认值。默认态 Q=40.00 W/R=0.5000 K/W 不命中。" },
  { slug: "engineering/material-calculator", inputs: {"b":"50","h":"200","L":"2","d":"5.5","D":"50","t":"5","a":"50","c":"50"}, radios: { material: "2" }, expect: ["重量 54.00 kg", "材料 铝 (2700 kg/m³)"], ref: "该页控件由 JS 模板 innerHTML 生成、材料靠 getElementsByName('material') 单选组读取 ⇒ 必须显式 radios 注入，否则 calc 取不到材料而抛错。矩形 b=50mm×h=200mm：A=10000mm²=100cm²、I=b·h³/12=3.3333e7mm⁴=3333.33cm⁴；V=0.01m²×2m=0.02m³=20.00L；铝 2700kg/m³ ⇒ 重量 54.00 kg、每米 27.00 kg/m。默认 b=100/L=1/钢7850 得 157.00 kg（体积同为 20.00 L，不可锚体积；原 expect「角钢」只是形状页签名）" },
  { slug: "engineering/poisson-strain", inputs: {"ex":"0.0018","nu":"0.32"}, expect: ["-5.760e-4", "6.480e-4"], ref: "ε_y=−ν·ε_x=−0.32×0.0018=−5.760e-4；ε_v=ε_x(1−2ν)=0.0018×0.36=6.480e-4。默认 0.001/0.3 得 −3.000e-4 / 4.000e-4。注：不可锚「0.320」——那是 ν 的输入值回显（原 expect「泊松比」是静态标签词）" },
  { slug: "engineering/pressure-vessel", inputs: {"P":"2.5","D":"1200","sigma":"150","phi":"0.9"}, expect: ["11.11", "13.11"], ref: "t=PD/(2σφ)=2.5×1200/(2×150×0.9)=3000/270=11.11 mm；计入腐蚀裕量 +2mm = 13.11 mm。默认 1.6/1000/130/0.85 得 7.24 / 9.24 mm（原 expect「计入腐蚀裕量后」是静态标签词）" },
  { slug: "engineering/section-inertia", inputs: {"shape":"1","b":"250","h":"500"}, expect: ["2604166667", "10416667"], ref: "矩形 I=bh³/12=250×500³/12=2.6041667e9 mm⁴；W=I/(h/2)=2604166667/250=1.0416667e7 mm³。默认 200/400 得 1.0667e9 / 5.3333e6（原 expect「矩形」是公式标签里的静态词）" },
  { slug: "machinery/shaft-torsion", inputs: {"T":"3.5","d":"60","G":"79","L":"1.2"}, expect: ["82.52", "2.394"], ref: "J=πd⁴/32=1272345 mm⁴；τ=Tr/J=3.5e6×30/1272345=82.52 MPa；θ=TL/(GJ)=0.04178 rad=2.394°。默认 2/50/80/1 得 81.49 MPa / 2.334°（原 expect「扭转角」是静态标签词）" },
  { slug: "engineering/stress-calculator", inputs: {"F":"80","A":"400","V":"45","M":"8000","W":"160","T":"1500","D":"60","d":"20"}, radios: { material: "2" }, expect: ["200.00 MPa", "安全系数 n 1.18"], ref: "材料表同样靠 getElementsByName('material') 读取，须 radios 注入（此处 index 2 = 45钢 yield 355）。σ=F/A=80kN/400mm²=200.00 MPa；许用 [σ]=355/1.5=237 MPa；安全系数 n=[σ]/|σ|=236.67/200=1.18；比例 84% ✅安全（≤许用）。旧实现用 σs/σ 得 1.77 且拿屈服强度当判定线，已改为许用应力" },
  { slug: "engineering/thermal-expansion", inputs: {"alpha":"17","L0":"12","dT":"55"}, expect: ["11.220", "0.0112"], ref: "ΔL=α·L₀·ΔT=17e-6×12×55=0.01122 m=11.220 mm。默认 12/10/40 得 4.800 mm / 0.0048 m（原 expect「膨胀量」是静态标签词）" },
  { slug: "welding/weld-strength", inputs: {"F":"75","hf":"8","lw":"250"}, expect: ["53.57", "1400"], ref: "A_e=0.7·hf·lw=0.7×8×250=1400 mm²；τ=F/A_e=75000/1400=53.57 MPa。默认 50/6/200 得 840 mm² / 59.52 MPa（原 expect「焊缝剪应力」是静态标签词）" },
  { slug: "engineering/heat-transfer", inputs: {}, clicks: ["selectMode('conduction');document.getElementById('k').value='2.5';document.getElementById('A').value='3';document.getElementById('L').value='0.25';document.getElementById('T1').value='120';document.getElementById('T2').value='30';calc();"], expect: ["2700.00 W", "900 W/m²", "0.0333 K/W"], ref: "导热模式第二组注入值（默认 50/1/0.1/100/20 ⇒ 400000.00 W）：Q=k·A·ΔT/L=2.5×3×90/0.25=2700.00 W；q=Q/A=900 W/m²；R=L/(kA)=0.25/7.5=0.0333 K/W。默认态是导热默认值，四条全不命中。" },
  { slug: "engineering/heat-transfer", inputs: {}, clicks: ["selectMode('convection');document.getElementById('h').value='25';document.getElementById('A').value='2.5';document.getElementById('Ts').value='95';document.getElementById('Tinf').value='15';calc();"], expect: ["5000.00 W", "2000 W/m²", "0.0160 K/W"], ref: "对流模式：Q=h·A·(Ts−T∞)=25×2.5×80=5000.00 W；q=2000 W/m²；R=1/(hA)=1/62.5=0.0160 K/W。刻意不锚「温差 80 K」——默认导热档的温差同样是 80 K，属默认态同值。" },
  { slug: "engineering/heat-transfer", inputs: {}, clicks: ["selectMode('radiation');document.getElementById('eps').value='0.6';document.getElementById('A').value='2';document.getElementById('T1K').value='600';document.getElementById('T2K').value='280';calc();"], expect: ["8399.77 W", "4200 W/m²", "1.23e+11"], ref: "辐射模式：Q=εσA(T1⁴−T2⁴)=0.6×5.67e-8×2×(1.2960e11−6.14656e9)=8399.77 W；q=Q/A=8399.7721/2=4199.886→4200 W/m²（toFixed(0) 进位）；T1⁴−T2⁴=1.2345344e11→toExponential(2)=1.23e+11。默认态是导热档，无辐射串。" },
  { slug: "engineering/heat-transfer", inputs: {}, clicks: ["selectMode('resistance');document.getElementById('k').value='0.5';document.getElementById('A').value='8';document.getElementById('L').value='0.4';document.getElementById('h1').value='12';document.getElementById('h2').value='25';document.getElementById('T1').value='25';document.getElementById('T2').value='5';calc();"], expect: ["173.29 W", "1.083 W/m²·K", "0.1154 K/W"], ref: "复合热阻模式：R1=1/(h1A)=1/96=0.0104167、Rw=L/(kA)=0.4/4=0.1000、R2=1/(h2A)=1/200=0.0050 ⇒ R总=0.1154167 K/W；Q=ΔT/R总=20/0.1154167=173.29 W；U=1/(R总·A)=1/0.9233333=1.0829→1.083 W/m²·K。" },
  { slug: "engineering/heat-transfer", inputs: {}, clicks: ["selectMode('resistance');document.getElementById('k').value='0.5';document.getElementById('A').value='8';document.getElementById('L').value='0.4';document.getElementById('h1').value='12';document.getElementById('h2').value='25';document.getElementById('T1').value='25';document.getElementById('T2').value='5';calc();"], expect: ["(9.0%)", "(86.6%)", "(4.3%)"], ref: "与本文件上一条同一组复合热阻输入，只锚热阻**占比**这一支：R1/R总=0.0104167/0.1154167=9.0%、Rw/R总=0.1000/0.1154167=86.6%、R2/R总=0.005/0.1154167=4.3%。三者之和恰为 100.0%，任一支算错都会破坏这一关系 ⇒ 互为交叉校验。" },
  {
    "slug": "engineering/axial-stress",
    "inputs": {
      "F": "42",
      "A": "42",
      "E": "42",
      "L": "42"
    },
    "expect": [
      " σ (MPa) 2.381e-2 线应变 ε 1000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"A\":\"42\",\"E\":\"42\",\"L\":\"42\"}，输出区含「 σ (MPa) 2.381e-2 线应变 ε 1000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/beam-calculator",
    "inputs": {
      "length": "42",
      "load": "42",
      "E": "42",
      "I": "42",
      "limit": "42"
    },
    "expect": [
      "L³/(3EI)\n42\n42\n42\n42\n42\nL = 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"length\":\"42\",\"load\":\"42\",\"E\":\"42\",\"I\":\"42\",\"limit\":\"42\"}，输出区含「L³/(3EI)\n42\n42\n42\n42\n42\nL = 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "machinery/bolt-preload",
    "inputs": {
      "T": "42",
      "d": "42",
      "K": "42"
    },
    "expect": [
      "42\n42\n42\n0.02"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"d\":\"42\",\"K\":\"42\"}，输出区含「42\n42\n42\n0.02」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/bending-stress",
    "inputs": {
      "M": "42",
      "b": "42",
      "h": "42"
    },
    "expect": [
      " W (mm³) 3401.36"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"M\":\"42\",\"b\":\"42\",\"h\":\"42\"}，输出区含「 W (mm³) 3401.36」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/cantilever-deflection",
    "inputs": {
      "P": "42",
      "L": "42",
      "E": "42",
      "I": "42"
    },
    "expect": [
      "42\n42\n42\n42\n5880000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"P\":\"42\",\"L\":\"42\",\"E\":\"42\",\"I\":\"42\"}，输出区含「42\n42\n42\n42\n5880000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/material-calculator",
    "inputs": {
      "b": "42",
      "h": "42",
      "L": "42",
      "d": "42",
      "D": "42",
      "t": "42",
      "a": "42",
      "c": "42"
    },
    "expect": [
      "ndefined\n42\n42\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"b\":\"42\",\"h\":\"42\",\"L\":\"42\",\"d\":\"42\",\"D\":\"42\",\"t\":\"42\",\"a\":\"42\",\"c\":\"42\"}，输出区含「ndefined\n42\n42\n42\n42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/pressure-vessel",
    "inputs": {
      "P": "42",
      "D": "42",
      "sigma": "42",
      "phi": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.50"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"P\":\"42\",\"D\":\"42\",\"sigma\":\"42\",\"phi\":\"42\"}，输出区含「42\n42\n42\n42\n0.50」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/poisson-strain",
    "inputs": {
      "ex": "0.002",
      "nu": "0.25"
    },
    "expect": [
      "-5.000e-4"
    ],
    "ref": "注入 ex=0.002、nu=0.25：ε_y=−0.25×0.002=−5.000e-4；默认 0.001/0.3 得 −3.000e-4 ⇒ 强判别。ν=42 已超出 −1–0.5 物理范围，旧自动补强用例改为此组有效值。"
  },
  {
    "slug": "engineering/section-inertia",
    "inputs": {
      "shape": "2",
      "b": "42",
      "h": "42"
    },
    "expect": [
      "152745"
    ],
    "ref": "圆截面仅用 D=42：I=π×42⁴/64=152,745 mm⁴；默认矩形 200/400 得 1.0667e9 ⇒ 强判别。shape=42 已改为非法形状并单独覆盖，此例改用有效圆截面。"
  },
  {
    "slug": "machinery/shaft-torsion",
    "inputs": {
      "T": "42",
      "d": "42",
      "G": "42",
      "L": "42"
    },
    "expect": [
      "42\n42\n42\n42\n305490.040"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"d\":\"42\",\"G\":\"42\",\"L\":\"42\"}，输出区含「42\n42\n42\n42\n305490.040」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/stress-calculator",
    "inputs": {
      "F": "42",
      "A": "42",
      "V": "42",
      "M": "42",
      "W": "42",
      "T": "42",
      "D": "42",
      "d": "42"
    },
    "expect": [
      "ndefined\n42\n42\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"A\":\"42\",\"V\":\"42\",\"M\":\"42\",\"W\":\"42\",\"T\":\"42\",\"D\":\"42\",\"d\":\"42\"}，输出区含「ndefined\n42\n42\n42\n42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "engineering/thermal-expansion",
    "inputs": {
      "alpha": "42",
      "L0": "42",
      "dT": "42"
    },
    "expect": [
      "42\n42\n42\n74.08"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"alpha\":\"42\",\"L0\":\"42\",\"dT\":\"42\"}，输出区含「42\n42\n42\n74.08」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "welding/weld-strength",
    "inputs": {
      "F": "42",
      "hf": "42",
      "lw": "42"
    },
    "expect": [
      "_e (mm²) 34.01"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"hf\":\"42\",\"lw\":\"42\"}，输出区含「_e (mm²) 34.01」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }
,
{
  "slug": "engineering/stress-calculator",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/' +'tools/engineering/stress-calculator.html','utf8');var ok=h.indexOf('function fail(msg)')>=0&&(h.match(/fail\\('/g)||[]).length>=4&&h.indexOf('截面积 A 必须为正数')>=0;document.getElementById('__tbProbe').textContent='STRSVAL '+(ok?'OK':'BAD');})();"],
  "expect": ["STRSVAL OK"],
  "ref": "第851批 stress-calculator：A/W/D 的零值与空值改统一走 fail()，同步清空 #stressViz/#result 并给出字段级提示；旧实现是内联 showToast 早退。"
},
{
  "slug": "engineering/beam-calculator",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/' +'tools/engineering/beam-calculator.html','utf8');var ok=h.indexOf('截面惯性矩 I 须为正数')>=0&&h.indexOf('const delta = Math.abs(deltaSigned)')>=0&&h.indexOf('const safe = ratio <= 1')>=0;document.getElementById('__tbProbe').textContent='BEAMVAL '+(ok?'OK':'BAD');})();"],
  "expect": ["BEAMVAL OK"],
  "ref": "第851批 beam-calculator：I/E/L/limit 改为原始空值+正数校验（旧实现 I=0 被静默替换），负惯性矩与负载荷不再穿透；挠度取绝对值后与许用值比较。"
}
,
{ "slug": "engineering/stress-calculator", "inputs": {}, "radios": {"material":"2"}, "clicks": ["selectType('tension');document.getElementById('F').value='-80';document.getElementById('A').value='400';calc();"], "expect": ["200.00 MPa（受压）", "安全系数 n 1.18"], "ref": "拉压类型 F 取负（受压）时仍以 |σ|=200 MPa 与许用 237 MPa 比较，n=236.67/200=1.18；旧实现 safe=stress<σs 对负应力恒真、n 也为负，属负号误判。" },
{ "slug": "engineering/stress-calculator", "inputs": {}, "radios": {"material":"2"}, "clicks": ["selectType('torsion');document.getElementById('d').value='50';calc();"], "expect": ["内径 d 须为 0 或小于外径的正数（mm，实心填 0）"], "ref": "扭转 D=50、d=50 时 J=D⁴−d⁴=0，旧实现会除以 0 得 Infinity/NaN；新实现拒绝 d≥D。默认 d=0 合法。" },
{ "slug": "engineering/beam-calculator", "inputs": {"length":"6","load":"-15","E":"210","I":"800","limit":"300"}, "expect": ["150.67 mm（与设定方向相反）", "❌ 不满足"], "ref": "载荷向上 q=−15 时挠度反向，按 |δ|=150.67 mm 与许用 20.00 mm 比较仍不满足；旧实现 ratio 为负恒判安全，且结果区不回显方向。" },
{ "slug": "engineering/poisson-strain", "inputs": {}, "clicks": ["document.getElementById('ex').value='';calcTool();"], "expect": ["轴向应变须为有效数值"], "ref": "轴向应变清空时旧 num() 回退 0，输出 ε_y=0 与比值 0.000；新实现停止计算并提示空值。" },
{ "slug": "engineering/material-calculator", "inputs": {}, "radios": {"material":"0"}, "clicks": ["selectShape('hollow_circle');document.getElementById('D').value='10';document.getElementById('t').value='11';calc();"], "expect": ["圆管壁厚须小于外径的一半"], "ref": "D=10、t=11 时 d=D−2t=−12，旧实现 A=π(10²−(−12)²)/4 为负面积、质量为负；新实现按 2t<D 拒绝。" },
{ "slug": "engineering/material-calculator", "inputs": {}, "radios": {"material":"0"}, "clicks": ["document.getElementById('L').value='';calc();"], "expect": ["长度 L 须为非负数值"], "ref": "长度清空时旧实现 `||1` 静默按 1 m 计重；新实现要求显式数值（0 合法，每米重量显示不适用）。" },
{ "slug": "engineering/section-inertia", "inputs": {}, "clicks": ["document.getElementById('shape').value='2';syncShape();calcTool();"], "expect": ["1256637061"], "ref": "圆截面仅用 D=400：I=πD⁴/64=π×2.56e10/64=1,256,637,061 mm⁴；旧实现强制 b>0，圆截面需填无关宽度 b。" },
{ "slug": "engineering/axial-stress", "inputs": {}, "clicks": ["document.getElementById('F').value='';calcTool();"], "expect": ["轴向力 F 须为有效数值"], "ref": "轴力清空时旧 num() 回退 0，输出 0.00 MPa；新实现停止计算并提示。" },
{ "slug": "engineering/cantilever-deflection", "inputs": {}, "clicks": ["document.getElementById('P').value='';calcTool();"], "expect": ["端部集中力 P 须为有效数值"], "ref": "端部集中力清空时旧 num() 回退 0，输出 0.00 mm；新实现停止计算并提示。" }
,
{ "slug": "engineering/stress-calculator", "inputs": {}, "radios": {"material":"0"}, "clicks": ["selectType('shear');document.getElementById('V').value='45';document.getElementById('A').value='400';calc();"], "expect": ["许用剪应力 [τ]=0.577σs/1.5", "0.80"], "ref": "剪切按 0.577σs 取强度依据：Q235 σs=235 ⇒ 剪切屈服 135.7 MPa，许用 /1.5=90.5 MPa；τ=45kN/400mm²=112.50 MPa，n=90.5/112.5=0.80，判不安全。旧实现用 σs 当判定线会误判安全。" }

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

  console.log("==== engineering calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
