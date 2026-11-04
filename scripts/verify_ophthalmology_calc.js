#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ophthalmology/amblyopia-stereopsis",
  "inputs": {
    "age": "5",
    "stereoLevel": "60"
  },
  "expect": [
    "60"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
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
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
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
