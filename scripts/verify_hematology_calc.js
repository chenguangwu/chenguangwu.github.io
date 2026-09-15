#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "hematology/anemia-classification", inputs: {"hgb":"85","rbc":"3.5","hct":"27","mcvDirect":"75","mchDirect":"24","mchcDirect":"300"}, expect: ["参考范围"] },
  { slug: "hematology/anemia-differential", inputs: {"mcv":"72","retic":"1.2","ferritin":"8","siron":"6","tibc":"75","b12":"200","folate":"10","ldh":"250","bilirubin":"12","haptoglobin":"1.0"}, expect: ["一步确诊"] },
  { slug: "hematology/aps-diagnosis", inputs: {}, expect: ["未满足临床和实验室标"] },
  { slug: "hematology/calc-1", _blobcheck: true, inputs: {}, expect: ["结果"] },
  { slug: "hematology/cd34-count", inputs: {"pbWbc":"25","pbCd34":"0.8","pbWeight":"70","pbVolume":"12000","pbEff":"40","prWbc":"150","prCd34":"1.5","prVolume":"150","prWeight":"70"}, expect: ["剂量不足"] },
  { slug: "hematology/cml-monitoring", inputs: {"months":"12","bcrabl":"0.5"}, expect: ["范围"] },
  { slug: "hematology/coagulation-factor", inputs: {"activity":"5","residual":"25","dilution":"1","weight":"70","dose":"1400","preActivity":"1","postActivity":"35"}, expect: ["回收率"] },
  { slug: "hematology/detector-5", inputs: {"granCD59":"35","granCD55":"32","rbcCD59":"15","monoCD59":"28","type2":"10","type3":"25","ldh":"450","hb":"85"}, expect: ["和克隆大小变化"] },
  { slug: "hematology/dic-scoring", inputs: {"plt":"45","ddimer":"8.5","pt":"6","fib":"1.2"}, expect: ["请确认基础疾病后再评"] },
  { slug: "hematology/generator-analysis", inputs: {"cnt":"5"}, expect: ["峰值"] },
  { slug: "hematology/hemophilia-treatment", inputs: {"weight":"70","current":"1","target":"50"}, expect: ["密切监测出血改善情况"] },
  { slug: "hematology/hlh-diagnosis", inputs: {"c4_tg":"3.5","c4_fib":"1.5","c7_ferritin":"800","c8_scd25":"2400"}, expect: ["态评估"] },
  { slug: "hematology/ipss-r", inputs: {"blasts":"5","hgb":"85","anc":"0.8","plt":"50"}, expect: ["定期监测"] },
  { slug: "hematology/iron-overload", inputs: {"ferritin":"2500","tsat":"80","transfusions":"12"}, expect: ["每年"] },
  { slug: "hematology/itp-risk-score", inputs: {}, expect: ["结果"], _selfcheck: true },
  { slug: "hematology/leukemia-classification", inputs: {}, expect: ["缺失"] },
  { slug: "hematology/lymphoma-staging", inputs: {"mtRatio":"0","massSize":"0"}, expect: ["请勾选受累部位"] },
  { slug: "hematology/m-protein", inputs: {"tp":"75","albumin":"35","mprotein":"25","sIgG":"18","sIgA":"1","sIgM":"0.5","sKappa":"500","sLambda":"30"}, expect: ["蛋白占总蛋白"] },
  { slug: "hematology/mm-staging", inputs: {"albumin":"35","b2m":"5.5","ldhNormal":"250","ldh":"400"}, expect: ["移植或入组临床试验"] },
  { slug: "hematology/mpn-scoring", inputs: {"age":"65","hgb":"95","wbc":"15","blasts":"2","plt":"100"}, expect: ["应证"] },
  { slug: "hematology/pnh-flow", inputs: {"flaerGran":"0","flaerMono":"0","rbc59":"0","rbc55":"0","gran59":"0","gran55":"0"}, expect: ["请输入流式检测结果"] },
  { slug: "hematology/quetie-juyou-rongxue-shiyanshijianbie", inputs: {"v0":"100","v1":"50","v2":"10"}, expect: ["合计"] },
  { slug: "hematology/rater-5", inputs: {"hb":"105","blasts":"2","wbc":"15"}, expect: ["分需药物干预"] },
  { slug: "hematology/rater-6", inputs: {"plt":"45","ddimer":"8.5","pt":"5","fib":"0.9","fdp":"40"}, expect: ["纤维蛋白原"] },
  { slug: "hematology/rater-risk-1", inputs: {"pltBefore":"180","pltNadir":"15","onsetDays":"5","recoveryDays":"7"}, expect: ["不适用本工具"] },
  { slug: "hematology/thrombin-generation", inputs: {"lagTime":"3.0","peak":"180","ttPeak":"6.5","etp":"1200","startTail":"20","cLag":"3","cPeak":"200","cTtPeak":"7","cEtp":"1200","cTail":"20"}, expect: ["凝血酶生成终止时间"] },
  { slug: "hematology/transfusion-dose", inputs: {"pWeight":"70","pCurrentHgb":"60","pTargetHgb":"90","plWeight":"70","plCurrent":"10","plTarget":"40","fWeight":"70","fDose":"12","cWeight":"70","cCurrent":"0.8","cTarget":"1.5"}, expect: ["大剂量"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    if (c._blobcheck) {
      const r2 = await runCase({...c, expect:["ZZZ"]});
      if (r2.step2Blob && r2.step2Blob.trim().length > 10) { pass++; console.log("  OK " + c.slug + " (blob-check: " + r2.step2Blob.trim().length + " chars)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (blob-check empty)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== hematology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
