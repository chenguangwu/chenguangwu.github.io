#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
// 第八批加固：urology 全部用例去默认化 / 修复破损与退化
// 每条用例输入均 ≠ 页面默认值，且 expect 断言「页面计算出的结果文本」（非输入值、非静态表字面量）。
// 判别力由 scripts/discriminate_check.js 反向验证（模拟注入失败须 FAIL）。
const CASES = [
{
  "slug": "urology/assessor-pressure",
  "inputs": { "pdet": "120", "qmax": "15" },
  "expect": ["BOOI=90（梗阻）", "BCI=195（强收缩力）"],
  "ref": "de-default: pdet120/qmax15→BOOI90 梗阻（标签外纯净串）"
},
{
  "slug": "urology/bladder-capacity",
  "inputs": { "voided": "800", "pvr": "100", "age": "45" },
  "expect": ["900 mL", "膀胱容量偏大"],
  "ref": "de-default: 800/100→900mL 偏大"
},
{
  "slug": "urology/calc-volume",
  "inputs": { "d1": "3.0", "d2": "2.5", "d3": "3.0", "formula": "0.52", "psa": "" },
  "expect": ["11.7", "偏小"],
  "ref": "de-default: 椭球 vol 11.7 偏小（data-grid 数字与 mL 分离）"
},
{
  "slug": "urology/canyuniaoliang-jingfubchao-tuisuan",
  "inputs": { "w": "7", "d": "6", "h": "5", "formula": "0.75" },
  "expect": ["157.5", "残余尿增多"],
  "ref": "de-default: 经腹 vol 157.5 残余尿增多（数字与 mL 分离）"
},
{
  "slug": "urology/hydronephrosis",
  "inputs": { "apd": "30", "cortex": "4", "subject": "adult" },
  "expect": ["重度", "4 mm"],
  "ref": "de-default: apd30/cortex4→重度 + <5mm 皮质萎缩"
},
{
  "slug": "urology/penile-rigidity",
  "inputs": { "ehs": "2", "npt_n": "2", "npt_d": "8", "npt_r": "60" },
  "expect": ["最大硬度60%", "2次/夜"],
  "ref": "de-default: ehs2+NPT(2/8/60均低于正常)→异常器质性ED；expect取动态独有'最大硬度60%'/'2次/夜'，避静态EHS分级表碰撞（ehs:1恰等于校验器误取的首option）"
},
{
  "slug": "urology/prostate-volume",
  "inputs": { "d1": "5", "d2": "4", "d3": "5", "psa": "8", "formula": "0.5236" },
  "expect": ["52.4 mL", "增生程度：重度增大"],
  "ref": "de-default: 椭球 vol 52.4mL 重度增大"
},
{
  "slug": "urology/psa-density",
  "inputs": { "psa": "12", "vol": "25", "age": "50" },
  "expect": ["0.480", "风险分级：高危", "穿刺建议：建议前列腺穿刺活检"],
  "ref": "de-default: PSAD0.480 高危 活检"
},
{
  "slug": "urology/residual-urine",
  "inputs": { "w": "6", "h": "5", "d": "5", "voided": "350", "formula": "0.7" },
  "expect": ["105 mL", "程度：中度尿潴留"],
  "ref": "de-default: PVR 105mL 中度尿潴留"
},
{
  "slug": "urology/urethral-stricture",
  "inputs": { "qmax": "5", "qave": "4", "vol": "200", "time": "40", "curve": "plateau" },
  "expect": ["高度可疑尿道狭窄"],
  "ref": "de-default: score10→高度可疑（避开静态依据串）"
},
{
  "slug": "urology/urine-flow-rate",
  "inputs": { "age": "60", "qmax": "8", "vol": "200" },
  "expect": ["梗阻可能"],
  "ref": "de-default: 男 qmax8→梗阻可能（标签外纯净串，避静态参考串与子串碰撞）"
},
{
  "slug": "urology/urodynamics",
  "inputs": { "pdet": "120", "qmax": "5", "pdetmax": "130", "fdv": "100", "mcc": "200" },
  "expect": ["145"],
  "ref": "de-default: BCI145（避开默认 BCI110/BOOI110）"
},
{
  "slug": "urology/varicocele-grading",
  "inputs": { "diam": "5.0", "reflux": "4.0" },
  "expect": ["3级（重度）"],
  "ref": "de-default: diam5→3级重度（避开静态显微结扎术串）"
},
{
  "slug": "urology/calc-1",
  "inputs": { "q0": "3", "q1": "3", "q2": "3", "q3": "3", "q4": "3", "q5": "3", "q6": "3" },
  "expect": ["21 分（0-35 分）"],
  "ref": "fix broken template: q0-6=3→总分21（数字在 strong 内，空格感知）"
},
{
  "slug": "urology/catheter-selection",
  "inputs": { "patient": "adult_female" },
  "expect": ["14 Fr"],
  "ref": "de-default: 成人女性→推荐14Fr（computed 串，避静态表/回声）"
},
{
  "slug": "urology/hematuria-differential",
  "inputs": { "morph": "dysmorphic" },
  "expect": ["肾小球性血尿"],
  "ref": "de-default: dysmorphic→肾小球性（strong 内文本，避回声）"
},
{
  "slug": "urology/hydrocele-assessment",
  "inputs": { "age": "infant", "trans": "positive", "depth": "60" },
  "expect": ["大量积液", "60 mm"],
  "ref": "de-default: depth60→大量积液（避开输入值回声）"
},
{
  "slug": "urology/iief5-score",
  "inputs": { "q0": "3", "q1": "3", "q2": "3", "q3": "3", "q4": "3" },
  "expect": ["IIEF-5 总分：15 / 25", "轻中度 ED"],
  "ref": "fix broken template: q0-4=3→总分15"
},
{
  "slug": "urology/ipss-score",
  "inputs": { "qol": "1" },
  "expect": ["（满意）"],
  "ref": "de-default: qol1→（满意）（strong 后纯净串，避回声）"
},
{
  "slug": "urology/rater-4",
  "inputs": { "e1": "5", "e2": "5", "e3": "5", "e4": "5", "e5": "5" },
  "expect": ["IIEF-5总分25分（22-25分）"],
  "ref": "fix: e1-5=5→总分25/25（标签外纯净串）"
},
{
  "slug": "urology/stone-composition",
  "inputs": { "search": "zzz" },
  "expect": ["未找到匹配的结石成分"],
  "ref": "fix no_inputs: 注入无匹配词→未找到（空搜索默认渲染9石会假通过）"
},
{
  "slug": "urology/stone-size-assessment",
  "inputs": { "size": "15", "loc": "renal" },
  "expect": ["自发排石率低"],
  "ref": "de-default: size15/renal→prob=2(<30)策略'自发排石率低'（避2%⊂42%子串逃逸；回退42%/75%输出均无此串）"
},
{
  "slug": "urology/turp-parameters",
  "inputs": { "vol": "40", "method": "turp" },
  "expect": ["48 分钟"],
  "ref": "de-default: turp+vol40→48min（依赖 vol，避 method 静态串）"
},
{
  "slug": "urology/uti-diagnosis",
  "inputs": { "count": "mid" },
  "expect": ["菌落计数过低，多为标本污染"],
  "ref": "de-default: count mid+无勾选→污染分支（count high 恰为 select 真实默认，须改用 mid）"
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
  console.log("==== urology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
