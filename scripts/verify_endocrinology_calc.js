#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原为 all_default 弱用例：4 个输入全等于页面 value，expect「12.0」是兜底预设 loadNormal() 写入的醛固酮值。
  "slug": "endocrinology/aldosterone-renin",
  "inputs": {
    "aldo": "7.5",
    "renin": "2.4",
    "k": "3.0",
    "bp": "140"
  },
  "expect": [
    "3.1 ng/dL : ",
    "7.5 醛固酮(ng/dL)"
  ],
  "ref": "ARR = aldo / renin = 7.5 / 2.4 = 3.125 → 大字渲染 arr.toFixed(1) = 「3.1」+ arrType（ng/dL : ng/mL/h 或 ng/dL : mU/L，故只锚前缀「3.1 ng/dL : 」）；醛固酮卡 = aldo.toFixed(1) = 「7.5」+ 标签。默认态（value 22/0.6 → ARR 36.7）与兜底预设态（loadNormal 12/1.8 → ARR 6.7、卡片 12.0）都不含这两串。"
},
{
  "slug": "endocrinology/calcium-pth-axis",
  "inputs": {
    "ca": "2.85",
    "alb": "40",
    "pth": "85",
    "phos": "0.78",
    "vitd": "18",
    "refPop": "child"
  },
  "expect": [
    "child"
  ],
  "ref": "auto-restore"
},
{
  // 原 expect「4.2」是输入回显值 umn，且默认页签为血浆 ⇒ 主输出不含，属无判别力断言。
  "slug": "endocrinology/catecholamine-test",
  "inputs": {
    "mn": "1.9",
    "nmn": "3.3"
  },
  "expect": [
    "血浆MN 1.90 nmol/L",
    "血浆NMN 3.30 nmol/L"
  ],
  "ref": "注入血浆游离 MN/NMN（默认页签 plasma）→ 结果卡按 toFixed(2) 渲染「1.90 / 3.30 nmol/L」；默认值 0.25 / 0.55（HTML value）与兜底预设态均不含这两串。注意尿液键（umn/unmn/une/ue/uda）属未激活页签，注入不影响主输出。"
},
{
  // 原 expect「午夜抑制阈值(140nmol/L)」是 SVG 图例的静态文字，恒定出现 → 逃生项。
  "slug": "endocrinology/cortisol-rhythm",
  "inputs": {
    "m8": "333",
    "m16": "111",
    "m0": "17"
  },
  "expect": [
    "晨起：333 nmol/L",
    "午夜：17 nmol/L"
  ],
  "ref": "注入 333/111/17 → 8:00 卡片「晨起：333 nmol/L」（333 落在 171-536 正常区）与 0:00 卡片「午夜：17 nmol/L 抑制良好」（17 < 阈值 140）。默认 value 420/280/220 与兜底预设 loadAdrenal（120/60/30）都不含这两串。"
},
{
  "slug": "endocrinology/cycle-hormone",
  "inputs": {
    "cycleDay": "6"
  },
  "expect": [
    "第6天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/detector-metabolism",
  "inputs": {
    "vma": "9.5",
    "hva": "4.2",
    "ne": "320",
    "epi": "45",
    "da": "25",
    "age": "45"
  },
  "expect": [
    "9.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/frax-score",
  "inputs": {
    "age": "65",
    "weight": "55",
    "height": "160",
    "bmdT": "-2.5",
    "gender": "male"
  },
  "expect": [
    "15.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/gh-stimulation-test",
  "inputs": {
    "age": "8",
    "sds": "-2.8",
    "igf1Sds": "-2.5",
    "gh_'+i+'": "",
    "gender": "female"
  },
  "expect": [
    "female"
  ],
  "ref": "auto-restore"
},
{
  // 原为 all_default 弱用例：ga/a1c/alb/age 全等于页面 value，expect「HbA1c(2-3月)」是静态标签。
  "slug": "endocrinology/glycated-albumin",
  "inputs": {
    "ga": "33.3",
    "a1c": "7.7",
    "alb": "44",
    "age": "60"
  },
  "expect": [
    "20.5 估算近期血糖(mmol/L)",
    "33.3% 糖化白蛋白(GA)"
  ],
  "ref": "估算近期血糖 = ga×0.583 + 1.1 = 33.3×0.583 + 1.1 = 20.5139 → toFixed(1) = 「20.5」；GA 大字 = ga.toFixed(1) = 「33.3%」。默认态（value 22 → 13.9）与兜底预设 loadPoor（28.5 → 17.7）都不含这两串。"
},
{
  "slug": "endocrinology/graves-trab",
  "inputs": {
    "trab": "8.5",
    "ft4": "28.5",
    "refRange": "1.5"
  },
  "expect": [
    "TRAb阳性(8.2倍上限)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/insulin-adjustment",
  "inputs": {
    "weight": "98",
    "tdi": "40",
    "a1c": "8.5",
    "targetA1c": "7.0",
    "fastingBg": "8.2",
    "targetFasting": "6.0"
  },
  "expect": [
    "2.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/mage-index",
  "inputs": {
    "threshold": "1.0",
    "unit": "mg"
  },
  "expect": [
    "mg"
  ],
  "ref": "auto-restore"
},
{
  // 原 expect「140/90mmHg」出自每条标准的静态阈值说明文字 → 逃生项。
  "slug": "endocrinology/metabolic-syndrome",
  "inputs": {
    "waist": "99",
    "sbp": "150",
    "dbp": "95",
    "fpg": "7.2",
    "tg": "3.2",
    "hdl": "0.8"
  },
  "expect": [
    "腰围 99cm",
    "血压 150/95"
  ],
  "ref": "注入 6 项代谢指标（gender 默认 male）→ 判定卡渲染实测值「腰围 99cm」「血压 150/95」（metCount 也会成 5/5，但「满足 5 / 5 项标准」在兜底预设 loadMS 下同样出现 ⇒ 不可用）。默认 value（82cm / 120-78）与兜底预设（96cm / 148-95）都不含这两串。"
},
{
  // 原 expect「14.5」= 兜底预设 loadDM 的 h1 值，注入失败仍命中 → 逃生项。
  "slug": "endocrinology/ogtt-interpretation",
  "inputs": {
    "fpg": "6.4",
    "h1": "12.3",
    "h2": "10.4",
    "h3": "7.7"
  },
  "expect": [
    "1h： 12.3 mmol/L",
    "2h： 10.4 mmol/L"
  ],
  "ref": "四个时点注入 6.4 / 12.3 / 10.4 / 7.7 → 各时点卡按「1h： 12.3 mmol/L」格式渲染。默认 value（5.3/10.5/8.8/7.0）、兜底预设 loadDM（8.1/14.5/13.2/9.8）与 loadGDM（11.5/9.2）都不含这两串（注意规避 GDM 预设的 11.5 / 9.2）。"
},
{
  "slug": "endocrinology/pcos-diagnosis",
  "inputs": {
    "cycle": "45",
    "periods": "6",
    "testosterone": "72",
    "fgScore": "9",
    "follicles": "16",
    "ovaryVol": "12",
    "criteria": "nih"
  },
  "expect": [
    "诊断成立(NIH标准)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/pituitary-tumor",
  "inputs": {
    "diameter": "12"
  },
  "expect": [
    "之后每6-12月"
  ],
  "ref": "auto-restore"
},
{
  // 原 expect「2.4-12.6」是 LH 参考范围静态文字，恒定出现 → 逃生项。
  "slug": "endocrinology/sex-hormone-cycle",
  "inputs": {
    "lh": "9.9",
    "fsh": "3.3",
    "e2": "77",
    "t": "88",
    "prl": "22",
    "p": "1.1"
  },
  "expect": [
    "LH/FSH 比值： 3.00"
  ],
  "ref": "LH/FSH = 9.9 / 3.3 = 3.00（toFixed(2)）→ 页面末行「LH/FSH 比值： 3.00 （≥2，提示PCOS可能）」。默认 value 与兜底预设 loadPCOS（5.2/... 比值≠3.00）都不含该串。"
},
{
  // 原为 all_default 弱用例：11 个数字全等于页面默认，expect「P0.13-P3」是等级词。
  "slug": "endocrinology/short-stature-prediction",
  "inputs": {
    "age": "8",
    "currentHt": "110",
    "weight": "25",
    "fatherHt": "176",
    "motherHt": "162",
    "gender": "male",
    "boneAge": "7",
    "prevHt": "103"
  },
  "checkIds": [
    "delayBone",
    "pituitaryMri"
  ],
  "expect": [
    "范围：170.5 - 180.5 cm"
  ],
  "ref": "男性遗传靶身高 MPH = (父176 + 母162 + 13) / 2 = 175.5，输出「175.5 cm 范围：170.5 - 180.5 cm（±5cm遗传波动）」。注意不可断言「175.5 cm」——回退默认（父170/母158）时页面的参考表里也含该串（逃生项）。"
},
{
  // 原为 all_default 弱用例：仅 tumorSize/tg 取页面默认，expect 是低危随访文案。
  "slug": "endocrinology/thyroid-cancer-risk",
  "inputs": {
    "tumorSize": "5.5",
    "tg": "9.9"
  },
  "checkIds": [
    "distant",
    "rair"
  ],
  "expect": [
    "RAIR(碘难治)：",
    "9.9 Tg(ng/mL)"
  ],
  "ref": "勾选 distant（远处转移）→ 初始风险分层「高危」；勾选 rair → 追加 RAIR(碘难治) 提示卡；tg=9.9 → 卡片显示「9.9 Tg(ng/mL)」（toFixed(1) 渲染，非原始输入回显）。注意「初始风险： 高危」不可用 —— 回退时兜底函数 loadHigh() 也会产出它（逃生项）。"
},
{
  "slug": "endocrinology/ti-rads",
  "clicks": [
    "selectOpt({dataset:{cat:'composition',pts:'2'},classList:{add:function(){},remove:function(){}}});",
    "selectOpt({dataset:{cat:'echogenicity',pts:'3'},classList:{add:function(){},remove:function(){}}});",
    "selectOpt({dataset:{cat:'shape',pts:'3'},classList:{add:function(){},remove:function(){}}});",
    "selectOpt({dataset:{cat:'margin',pts:'3'},classList:{add:function(){},remove:function(){}}});",
    "selectOpt({dataset:{cat:'echogenic',pts:'3'},classList:{add:function(){},remove:function(){}}});"
  ],
  "expect": [
    "TR5",
    "总分 14 分",
    "高度可疑（恶性风险>20%）"
  ],
  "ref": "clicks 直接调 selectOpt 累加 selections[cat]=pts 后 calc()；默认态 selections 总 2→TR2，注入 5 类（2+3+3+3+3=14）→TR5。独立复算：TI-RADS 5 类阈值 total>=7，14 命中 TR5（恶性风险>20%）。"
},
{
  // 原为 all_default 弱用例：bg=2.2 即页面默认，expect「3.2」是兜底预设 loadReactive() 写入的值（典型逃生项）。
  "slug": "endocrinology/whipple-triad",
  "inputs": {
    "bg": "2.0",
    "fasting": "1"
  },
  "checkIds": [
    "symptom"
  ],
  "expect": [
    "有低血糖症状+低血糖值，但补糖后症状未缓解",
    "满足 2/3 项"
  ],
  "ref": "fasting=1（空腹）→ 阈值 2.8；bg=2.0 < 2.8 且仅勾选 symptom → metCount=2（症状✓、血糖✓、补糖缓解✗）→ 走「!hasRelief」分支文案。注意不可断言「Whipple三联征完整」——兜底预设 loadInsulinoma()（bg1.8+两项全勾）也产出它（逃生项）。"
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
  console.log("==== endocrinology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
