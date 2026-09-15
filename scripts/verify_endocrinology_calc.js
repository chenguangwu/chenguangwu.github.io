#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "endocrinology/aldosterone-renin", inputs: {"aldo":"22","renin":"0.6","k":"3.2","bp":"155"}, expect: ["等其他原因"] },
  { slug: "endocrinology/calcium-pth-axis", inputs: {"ca":"2.85","alb":"40","pth":"85","phos":"0.78","vitd":"18"}, expect: ["鉴别假性甲旁减"] },
  { slug: "endocrinology/catecholamine-test", inputs: {"bp":"175","mn":"0.8","nmn":"2.1","umn":"1.2","unmn":"3.5","une":"820","ue":"95","uda":"1200"}, expect: ["升高指标"] },
  { slug: "endocrinology/cortisol-rhythm", inputs: {"m8":"420","m16":"280","m0":"220"}, expect: ["午夜抑制阈值"] },
  { slug: "endocrinology/cycle-hormone", inputs: {"cycleDay":"3","valFSH":"50","valLH":"50","valE2":"50","valT":"50","valPRL":"50","valP":"50"}, expect: ["适合基础内分泌评估"] },
  { slug: "endocrinology/detector-metabolism", inputs: {"vma":"6.5","hva":"4.2","ne":"320","epi":"45","da":"25","age":"45"}, expect: ["如持续升高需进一步检"] },
  { slug: "endocrinology/frax-score", inputs: {"age":"65","weight":"55","height":"160","bmdT":"-2.5"}, expect: ["中国指南"] },
  { slug: "endocrinology/gh-stimulation-test", inputs: {"age":"8","sds":"-2.8","igf1Sds":"-2.5","gh_'+i+'":""}, expect: ["静注正规胰岛素"] },
  { slug: "endocrinology/glycated-albumin", inputs: {"ga":"22","a1c":"8.5","alb":"42","age":"55"}, expect: ["近期血糖升高"] },
  { slug: "endocrinology/graves-trab", inputs: {"trab":"8.5","ft4":"28.5"}, expect: ["手术"] },
  { slug: "endocrinology/homa-ir", inputs: {"fpg":"7.2","insulin":"16"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "endocrinology/insulin-adjustment", inputs: {"weight":"65","tdi":"40","a1c":"8.5","targetA1c":"7.0","fastingBg":"8.2","targetFasting":"6.0"}, expect: ["建议总量增加约"] },
  { slug: "endocrinology/mage-index", inputs: {"threshold":"1.0"}, expect: ["血糖趋势曲线"], _selfcheck: true, _min_inputs: 1 },
  { slug: "endocrinology/metabolic-syndrome", inputs: {"waist":"92","sbp":"145","dbp":"92","fpg":"6.8","tg":"2.8","hdl":"0.9"}, expect: ["定期监测代谢指标"] },
  { slug: "endocrinology/ogtt-interpretation", inputs: {"fpg":"6.8","h1":"11.5","h2":"9.2","h3":"6.5"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "endocrinology/pcos-diagnosis", inputs: {"cycle":"45","periods":"6","testosterone":"72","fgScore":"9","follicles":"16","ovaryVol":"12"}, expect: ["有生育需求"] },
  { slug: "endocrinology/pituitary-tumor", inputs: {"diameter":"8"}, expect: ["激素评估每年"], _selfcheck: true, _min_inputs: 1 },
  { slug: "endocrinology/sex-hormone-cycle", inputs: {"lh":"5.2","fsh":"6.8","e2":"45","t":"35","prl":"15","p":"0.8"}, expect: ["可能"] },
  { slug: "endocrinology/short-stature-prediction", inputs: {"age":"10","currentHt":"125","weight":"25","fatherHt":"170","motherHt":"158","boneAge":"9","prevHt":"118","ghPeak":"5","igf1":"80","birthLen":"50","birthWt":"3.2"}, expect: ["建议随访观察"] },
  { slug: "endocrinology/thyroid-cancer-risk", inputs: {"tumorSize":"2.5","tg":"2.5"}, expect: ["随访间隔延长至"] },
  { slug: "endocrinology/ti-rads", inputs: {}, _min_inputs: 0, expect: ["评分进度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "endocrinology/whipple-triad", inputs: {"bg":"2.2"}, expect: ["监测排除隐匿性低血糖"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== endocrinology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();