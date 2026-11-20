#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ophthalmology/amblyopia-stereopsis",
  "inputs": {
    "age": "7",
    "stereoLevel": "100"
  },
  "expect": [
    "评估： 轻度异常",
    "年龄评估： 低于该年龄段正常值"
  ],
  "ref": "原注入 age=5/stereoLevel=60 与页面默认值完全相同（age 默认 5、stereo 默认 selected 60），且原锚「60」是下拉回显 ⇒ 零判别力。改为 7 岁 + 100″：stereo=100 ⇒ 分级走 stereo<=100 分支得「轻度异常」，年龄 7 岁（>6）且 100>60 ⇒ 「年龄评估：低于该年龄段正常值」。默认 5 岁/60″ 为「正常立体视 / 符合年龄段正常范围」，两锚均不命中。"
},
// 注：ophthalmology/analysis-12 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "ophthalmology/axial-length",
  "inputs": {
    "al": "35.5",
    "vMeas": "1532",
    "sAcd": "3.5",
    "vAcd": "1532",
    "sLt": "4.5",
    "vLt": "1641",
    "sVl": "15.5",
    "vVl": "1532"
  },
  "expect": [ "声速校正后 36.033" ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/calc-1",
  "inputs": {
    "iop": "25",
    "cct": "560"
  },
  "expect": [
    "校正眼压： 23.9 mmHg",
    "评估： 偏高"
  ],
  "ref": "页面 corrected = IOP − ((CCT−544)/10)×0.7（以 544μm 为标准角膜厚度）；注入 iop=25、cct=560 ⇒ 25−1.12=23.88 → 显示 23.9 mmHg，落入 classify() 的「偏高」(21–25]。默认空输入 ⇒「请输入有效的眼压和角膜厚度」，两串均不命中。★本批同时修页面真缺陷：原式为 `iop + ((cct−544)/10)*0.7`，厚角膜反而把校正值上抬，与本页文案「厚角膜实测被高估」以及姊妹页 iop-correction 的 Ehlers(520−cct)/Doughty(542−cct)/Feltgen(550−cct) 三种标准式符号相反 ⇒ 已改为减号，并同步生成器 apply_ophthalmology.py、content_deepdive.json、指南页。"
},
{
  "slug": "ophthalmology/calc-length-1",
  "inputs": {
    "al": "35.5",
    "k1": "43.5",
    "k2": "44.0",
    "acd": "3.2",
    "lt": "4.5",
    "aConst": "118.4"
  },
  "expect": [
    "-10.72"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/cd-ratio",
  "inputs": {
    "od": "3.4",
    "os": "0.5"
  },
  "expect": [
    "(1.00)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/convert-42",
  "inputs": {
    "val": "0.25"
  },
  "expect": ["0.60 logMAR", "五分记录法 4.40；小数视力 0.25；logMAR 0.60", "Snellen 20/80（6/24）；ETDRS 字母数 ≈ 25（0–70，20/20=55）"],
  "ref": "小数 0.25 ⇒ logMAR = −log10(0.25) = 0.60；五分记录法 5 + log10(0.25) = 4.40；Snellen 20/80（6/24）；ETDRS 字母数 round((1.10−0.60)/0.02)=25。默认态 1.0 ⇒「0.00 logMAR」「Snellen 20/20」「ETDRS 字母数 ≈ 55」，与本用例零交集。原用例注入 val=4（小数视力 4.0，超出 0.01–2.0 有效域）只会命中「无效」提示，已改为有效值。"
},
{
  "slug": "ophthalmology/corneal-curvature",
  "inputs": {
    "k1": "63.5",
    "k2": "43.75",
    "ax": "90",
    "convVal": "43.50"
  },
  "expect": [
    "19.75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/corneal-endothelium",
  "inputs": {
    "cellCount": "120",
    "frameArea": "0.025",
    "hex4": "0",
    "hex5": "8",
    "hex6": "60",
    "hex7": "10",
    "hex8": "2",
    "fixedCount": "100",
    "fixedArea": "0.0314",
    "cellAreas": ""
  },
  "expect": [
    "4800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/detector-6",
  "inputs": {
    "age": "5"
  },
  "expect": [
    "100角秒"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/eye-chart-toolkit",
  "inputs": {
    "ecWmm": "782",
    "ecWpx": "1920",
    "ecPpi": "92",
    "ecScale": "60"
  },
  "expect": [ "62 PPI" ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/fluorescein-staining",
  "checks": [
    "2"
  ],
  "expect": [
    "10 角膜染色评分 (0-15)",
    "重度染色"
  ],
  "ref": "角膜 5 区、结膜 6 区各 0–3 分，radio 由 buildZones() 运行期拼 innerHTML 生成（静态 HTML 无任何控件）。checks 声明所有 `:checked` 返回 value=2 ⇒ 角膜 10/15、结膜 12/18、总 22/33；分级只取角膜：10>6 ⇒「重度染色」。默认态各区未选 ⇒ 0 分、「无染色」。原 expect「结膜染色(0-18)」是 data-card 标签文案，与输入无关（常量型逃生项）。"
},
{
  "slug": "ophthalmology/iol-power",
  "inputs": {
    "al": "35.5",
    "k": "43.50",
    "aconst": "118.4"
  },
  "expect": [
    "-11.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/iop-correction",
  "inputs": {
    "iop": "27",
    "cct": "545"
  },
  "expect": [
    "26.4"
  ],
  "ref": "三公式均值：(25.225+26.94+27.15)/3=26.438→26.4；比值法 25.761 仅单列、不纳入均值。默认态 iop=15/cct=540 ⇒「校正后眼压(三公式估算均值)： 15.3」不命中该串。"
},
{
  "slug": "ophthalmology/meibomian-grading",
  "checks": [
    "3"
  ],
  "expect": [
    "15 MGD总评分 (0-15)",
    "极重度MGD"
  ],
  "ref": "5 项各 0–3 分（lossUpper/lossLower/dilation/secretion/lidMorph），静态 HTML 每项首个选项带 `checked`（value=0）。checks 声明所有 `:checked` 返回 value=3 ⇒ 总分 15/15 > 11 ⇒「极重度MGD」。默认全 0 ⇒ 0/15「无/轻度MGD」。原 expect「(0-15)」是结果区固定分母文案（常量型逃生项）。"
},
{
  "slug": "ophthalmology/oct-rnfl",
  "inputs": {
    "age": "90",
    "g": "78",
    "s": "95",
    "i": "90",
    "n": "65",
    "t": "60"
  },
  "expect": [
    "112"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/osdi-scale",
  "checks": [
    "2"
  ],
  "expect": [
    "分级： 重度干眼",
    "已答 12/12 题"
  ],
  "ref": "12 题 radio 由 buildQ() 运行期拼 innerHTML 生成（静态 HTML 无控件）。checks 声明所有 `:checked` 返回 value=2 ⇒ 每题 2 分；OSDI = (12×2)×100/(12×4) = 50 ⇒ ≥33 ⇒「重度干眼」，同时输出「已答 12/12 题」。默认未答 ⇒ 0 分「正常」+「已答 0/12 题」。原 expect「一半时间(2)」是 OPTS 选项标签文案（常量型逃生项）。"
},
{
  "slug": "ophthalmology/pterygium-measurement",
  "inputs": {
    "cd": "17.5",
    "head": "2.0",
    "width": "4.0",
    "length": "5.0"
  },
  "expect": [
    "22.9%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/rater-7",
  "inputs": {
    "v1": "3",
    "v2": "3",
    "v3": "2"
  },
  "expect": [
    "van Bijsterveld总分： 8 / 9",
    "眼表染色重度（7-9分）"
  ],
  "ref": "3 个 select（v1 鼻侧结膜 / v2 角膜 / v3 颞侧结膜，各 0–3，静态默认 value=0）⇒ 默认 0/9「轻度」。注入 3/3/2 ⇒ 总分 8 > 6 ⇒「重度」并输出「眼表染色重度（7-9分）…立即眼科就诊」建议。原 expect「0-3分」是轻度分级文案片段，与输入无关（常量型逃生项）。"
},
{
  "slug": "ophthalmology/rater-8",
  "inputs": {
    "v1": "1"
  },
  "expect": [
    "0.1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/refraction-error",
  "inputs": {
    "s": "-5",
    "c": "-1.00",
    "ax": "180",
    "s1": "-3.00",
    "c1": "-0.75",
    "ax1": "90",
    "s2": "-0.50",
    "c2": "-0.50",
    "ax2": "180"
  },
  "expect": [
    "-5.500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/self-assess-2",
  "inputs": {
    "o1": "1"
  },
  "expect": [
    "OSDI指数0.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/strabismus-angle",
  "inputs": {
    "inVal": "30",
    "mm": "2",
    "pd2": "4",
    "pr1": "10",
    "pr2": "15",
    "pr3": "0"
  },
  "expect": [
    "16.70"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/tear-breakup-time",
  "inputs": {
    "but": "11",
    "tbut": ""
  },
  "expect": [
    "11.0s"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/vision-screening-21",
  "inputs": {
    "vsAge": "teen"
  },
  "expect": [
    "teen"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "ophthalmology/visual-acuity-converter",
  "inputs": {
    "type": "decimal",
    "value": "0.5"
  },
  "expect": [
    "20/40 Snellen 20ft",
    "视力分级： 中度下降"
  ],
  "ref": "auto-restore（去默认化：小数视力 0.5 → logMAR=0.301、Snellen 20/0.5=20/40、分级「中度下降」。原断言「0.0)」只是 type=logmar 的输入提示文案，非计算结果）"
},
{
  "slug": "ophthalmology/visual-fatigue-vas",
  "inputs": {
    "vasSlider": "8"
  },
  "checks": [
    "3"
  ],
  "clicks": [
    "calc()"
  ],
  "expect": [
    "76 综合评分 (0-110)",
    "视疲劳程度： 重度"
  ],
  "ref": "VAS 滑块 0–10（页面权重 ×5）+ 12 项症状问卷（各 0–5，radio 由 buildQ() 运行期拼 innerHTML 生成）⇒ total = vas×5 + symTotal，满分 110；分级 ≤15 无/轻微、≤30 轻度、≤50 中度、>50 重度。滑块默认 5、问卷默认全未答 ⇒ 默认输出「请至少作答部分症状问卷」。注入 vasSlider=8 且 checks 全选 3 ⇒ 40 + 36 = 76 > 50 ⇒「重度」+「建议眼科就诊…」。calc() 只由按钮 onclick 触发（range 的 oninput 只调 updateVAS），故须 clicks 驱动。★原用例 inputs{vasSlider:5} 与页面默认值**完全相同**（零判别力，判别器判「跳过」），且 expect「从不(0)」是问卷选项标签文案（与输出无关的常量型逃生项）⇒ 本批一并去默认化。"
},
{
  "slug": "ophthalmology/visual-field-analysis",
  "inputs": {
    "md": "-9.5",
    "psd": "4.2",
    "vfi": "85"
  },
  "expect": [ "-9.5 dB" ],
  "ref": "auto-restore"
},
  {
    "slug": "ophthalmology/amsler-grid-test",
    "inputs": {
      "amNote": "abc123测试",
      "amEye": "right",
      "amGrid": "10",
      "amBg": "dark"
    },
    "expect": [
      "right\n10\ndark\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amNote\":\"abc123测试\",\"amEye\":\"right\",\"amGrid\":\"10\",\"amBg\":\"dark\"}，输出区含「right\n10\ndark\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "ophthalmology/pupil-reflex",
    "afterLoad": true,
    "clicks": ["sel.od=1;sel.os=2;sel.rapd=2;calc()"],
    "expect": ["双眼直接反射均减弱，警惕动眼神经(传出)障碍", "瞳孔反射异常，建议进一步评估"],
    "ref": "OD 直接反射 1（迟钝）+ OS 2（减弱）+ RAPD 2+ ⇒ 输出「双眼直接反射均减弱，警惕动眼神经(传出)障碍或广泛病变，建议排查。」与综合「瞳孔反射异常，建议进一步评估」。"
       + "页面用 innerHTML 批量生成分级按钮后立刻读 children[def].classList，桩默认 children 为空 ⇒ 初始化即抛错；afterLoad 开启浏览器保真初始化后可用。"
       + "默认态（3/3/0）为「瞳孔反射未见明显异常」⇒ 两条断言均不命中。"
  },
  {
    "slug": "ophthalmology/amsler-grid-test",
    "clicks": ["var __gei=document.getElementById.bind(document);document.getElementById=function(id){if(id==='amToast')return __gei('__svg_probe');return __gei(id);};var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom');};}return e;};document.getElementById('amPng').fire('click');"],
    "expect": ["导出失败：Error"],
    "ref": "失败注入：createElement('canvas') 的 toDataURL 必抛 Error，并把页面 toast 读取的 #amToast 重定向到 #__svg_probe ⇒ 必须出现「导出失败：Error」。"
       + "修复前异常裸冒成 pageerror、无任何可见提示且不弹「已导出 PNG」；默认态无该串 ⇒ 判别明确。"
  },
  {
    "slug": "ophthalmology/astigmatism-chart",
    "clicks": ["var __gei=document.getElementById.bind(document);document.getElementById=function(id){if(id==='asToast')return __gei('__svg_probe');return __gei(id);};var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom');};}return e;};document.getElementById('asPng').fire('click');"],
    "expect": ["导出失败：Error"],
    "ref": "失败注入：createElement('canvas') 的 toDataURL 必抛 Error，并把页面 toast 读取的 #asToast 重定向到 #__svg_probe ⇒ 必须出现「导出失败：Error」。"
       + "修复前异常裸冒成 pageerror、无任何可见提示且不弹「已导出 PNG」；默认态无该串 ⇒ 判别明确。"
  },
  {
    "slug": "ophthalmology/eye-chart-toolkit",
    "clicks": ["window.canvasExportError=window.canvasExportError||function(){return null;};document.getElementById('ecCanvas').toBlob=function(){throw new Error('boom')};document.getElementById('ecPng').fire('click');"],
    "expect": ["导出失败：Error"],
    "ref": "失败注入：ecCanvas.toBlob 必抛 Error ⇒ 导出入口必须 toast「导出失败：Error」并终止。"
       + "桩内未加载 canvasExportError（真机由共享脚本注入）⇒ 用例前先给恒返回 null 的替身，确保走到 toBlob。"
       + "修复前异常裸冒成 pageerror、无任何可见提示；默认态无该串 ⇒ 判别明确。"
  }
,
{
  "slug": "ophthalmology/eye-chart-toolkit",
  "clicks": [
    "(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/eye-chart-toolkit.html','utf8');var i=h.indexOf('function saveResult() {');var s=i>=0?h.slice(i,i+560):'';var ok=s.indexOf('if (!rowVal)')>=0&&s.indexOf('rows[rows.length - 1]')<0&&s.indexOf('请先在当前视力表测出一行识别结果再保存')>=0;document.getElementById('__tbProbe').textContent='EYESAVE '+(ok?'OK':'BAD');})();"
  ],
  "expect": [
    "EYESAVE OK"
  ],
  "ref": "第1312批·视力表空行误保存修复源码形态强锚（saveResult 在 IIFE 内，harness 无法直接调用）：旧版识别行留空时取最后一行当实测视力写入历史；修复后空行直接提示并 return。旧版含 rows[rows.length-1] 回退 ⇒ BAD。"
},
{
  "slug": "ophthalmology/iop-correction",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/iop-correction.html','utf8');var i=h.indexOf('var __ig=__tbInputGuard');var seg=i>=0?h.slice(i,i+300):'';var ok=seg.indexOf(\"('grid').innerHTML=''\")>=0&&seg.indexOf(\"('formulaList').innerHTML=''\")>=0;document.getElementById('__tbProbe').textContent='IOPCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["IOPCLR OK"],
  "ref": "第1322批·清空必填残留修复源码形态强锚：原 __tbInputGuard 空值分支只更新 result 即 return，grid/formulaList 沿用旧值；越界分支两处均清。修复后守卫分支同步清 grid 与 formulaList。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/refraction-error",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/refraction-error.html','utf8');var ok=h.indexOf(\"isNaN(s)||isNaN(c)||isNaN(ax)){$('singleResult').innerHTML='';return;}\")>=0&&h.indexOf(\".some(isNaN)){$('combineResult').innerHTML='';return;}\")>=0;document.getElementById('__tbProbe').textContent='REFCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["REFCLR OK"],
  "ref": "第1323批·屈光误差输入清空旧结果残留修复源码形态强锚：原 calcSingle/calcCombine 遇空值直接 return，旧处方结果保留；修复后两处 return 前清对应结果容器。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/tear-breakup-time",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/tear-breakup-time.html','utf8');var i=h.indexOf('if(isNaN(but)){');var seg=i>=0?h.slice(i,i+220):'';var ok=seg.indexOf(\"('resultRefBar').innerHTML=''\")>=0&&seg.indexOf(\"('barWrap').innerHTML=''\")>=0;document.getElementById('__tbProbe').textContent='TBUTCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["TBUTCLR OK"],
  "ref": "第1323批·泪膜破裂清空未清标尺修复源码形态强锚：原清空首次 BUT 只清 barWrap，resultRefBar 参考标尺留存；修复后同步清 resultRefBar。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/oct-rnfl",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/oct-rnfl.html','utf8');var ok=h.indexOf(\"[age,g,s,i,n,t].some(function(v){return !isFinite(v)||v<=0;})\")>=0&&h.indexOf(\"年龄与各项厚度须为正数\")>=0;document.getElementById('__tbProbe').textContent='OCTNEG '+(ok?'OK':'BAD');})();"],
  "expect": ["OCTNEG OK"],
  "ref": "第1324批·负年龄/负厚度参与分级修复源码形态强锚：原只拦 NaN，负厚度也会出 RNFL 分级；修复后年龄与各项厚度须为正数。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/axial-length",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/axial-length.html','utf8');var a=h.indexOf('function calcCorr(){'),b=h.indexOf('function calcSeg(){');var ca=a>=0?h.slice(a,b):'',cb=b>=0?h.slice(b,b+520):'';var ok=ca.indexOf(\"[al,vMeas,vTrue].some(function(v){return !isFinite(v)||v<=0;})\")>=0&&cb.indexOf(\"[acd,vAcd,lt,vLt,vl,vVl].some(function(v){return !isFinite(v)||v<=0;})\")>=0;document.getElementById('__tbProbe').textContent='ALNEG '+(ok?'OK':'BAD');})();"],
  "expect": ["ALNEG OK"],
  "ref": "第1324批·负眼轴/负声速参与运算修复源码形态强锚：原两分支只拦 NaN，负声速/零声速可致除零与荒谬 IOL 影响；修复后眼轴与声速须为正数。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/visual-field-analysis",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/visual-field-analysis.html','utf8');var ok=h.indexOf('psd<0||vfi<0||vfi>100')>=0&&h.indexOf('VFI 须在 0–100% 之间')>=0;document.getElementById('__tbProbe').textContent='VFIDOM '+(ok?'OK':'BAD');})();"],
  "expect": ["VFIDOM OK"],
  "ref": "第1325批·视野指标定义域守卫修复源码形态强锚：原只拦 NaN，PSD 负值/VFI 越界仍进 HAP 分级；修复后要求 PSD≥0、VFI∈[0,100]。MD 负值按习惯输入保留。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/vision-screening-21",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/vision-screening-21.html','utf8');var i=h.indexOf('window.__vsClearHist=');var seg=i>=0?h.slice(i,i+220):'';var ok=seg.indexOf(\"getElementById('__vsTrend')\")>=0&&seg.indexOf(\"__vt.innerHTML=''\")>=0;document.getElementById('__tbProbe').textContent='VSCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["VSCLR OK"],
  "ref": "第1326批·清空历史未清趋势图修复源码形态强锚：原 __vsClearHist 只存空历史并重渲染，#__vsTrend 旧趋势留存；修复后同步清空趋势容器。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/strabismus-angle",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/strabismus-angle.html','utf8');var i=h.indexOf('function switchTab(name,btn){');var j=h.indexOf('conv();hirsch();combine();',i+10);var seg=i>=0?h.slice(i,j+40):'';var ok=seg.indexOf('if(!name||!btn)')>=0&&seg.indexOf('conv();hirsch();combine(); return;')>=0;document.getElementById('__tbProbe').textContent='STRASHIST '+(ok?'OK':'BAD');})();"],
  "expect": ["STRASHIST OK"],
  "ref": "第1334批·历史恢复无参 switchTab 抛错不重算修复源码形态强锚：原 switchTab(name,btn) 在恢复处被无参调用，btn.classList.add 抛 TypeError 被 catch 吞掉、三个结果区停留旧值；修复后无参分支安全重算 conv/hirsch/combine 并 return。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/astigmatism-chart",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/astigmatism-chart.html','utf8');var i=h.indexOf(\"$('asLines').addEventListener('change'\");var seg=i>=0?h.slice(i,i+520):'';var ok=seg.indexOf('S.marked = { left: [], right: [] }')>=0&&seg.indexOf('S.lines = parseInt(this.value, 10)')>=0;document.getElementById('__tbProbe').textContent='ASLINES '+(ok?'OK':'BAD');})();"],
  "expect": ["ASLINES OK"],
  "ref": "第1334批·切换射线数标记索引错位修复源码形态强锚：标记存射线索引、角度=索引×(360/条数)，24↔36 切换后同索引角度全变、旧标记被误读；修复后切条数即清两眼 marked。旧版无 ⇒ BAD。"
},
{
  "slug": "ophthalmology/amsler-grid-test",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ophthalmology/amsler-grid-test.html','utf8');var a=h.indexOf(\"$('amEye').addEventListener('change'\");var b=h.indexOf('function goStep(st)');var s1=a>=0?h.slice(a,a+320):'';var s2=b>=0?h.slice(b,b+500):'';var ok=s1.indexOf('S.drawing = null; S.cursor = null;')>=0&&s2.indexOf('S.drawing = null; S.cursor = null;')>=0;document.getElementById('__tbProbe').textContent='AMDRAW '+(ok?'OK':'BAD');})();"],
  "expect": ["AMDRAW OK"],
  "ref": "第1334批·切换眼别未清未完成绘制串眼修复源码形态强锚：amEye change 与 goStep 两处切眼别只改 S.eye，正在绘制的 S.drawing 闭合后归到新眼；修复后两处均补清 S.drawing/S.cursor。旧版两处皆无 ⇒ BAD。"
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

  console.log("==== ophthalmology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
