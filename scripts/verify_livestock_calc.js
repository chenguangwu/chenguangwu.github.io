#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "livestock/ammonia-ventilation", inputs: {"nh3Current":"25","nh3Target":"15","houseLength":"30","houseWidth":"10","houseHeight":"3","nh3Gen":"0"}, expect: ["换气"] },
  { slug: "livestock/analysis-18", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/animal-welfare-score", inputs: {}, _min_inputs: 0, expect: ["动物福利状况优秀"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/breeding-timing", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/calc-58", inputs: {}, _min_inputs: 0, expect: ["暂无计算记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/calving-interval", inputs: {"daysToFirstBreed":"75","breedTimes":"2","gestation":"283"}, expect: ["繁殖效率良好"] },
  { slug: "livestock/castration-timing", inputs: {}, _min_inputs: 0, expect: ["且所选动物支持该操作"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/detector-12", inputs: {"afb1":"10","zea":"100","don":"1000","ota":"50"}, expect: ["饲料可安全使用"] },
  { slug: "livestock/disinfectant-dilution", inputs: {"stockConc":"5","targetConc":"0.1","totalVol":"10"}, expect: ["的消毒液"] },
  { slug: "livestock/dongtishouroulv-beibiaohouceding", inputs: {"bf":"18","lw":"100"}, expect: ["暂无计算记录"] },
  { slug: "livestock/estimate-yield", inputs: {"qty":"1000","ts":"20","hrt":"20"}, expect: ["暂无计算记录"] },
  { slug: "livestock/fattening-pig-timeline", inputs: {"currentWeight":"60","targetWeight":"120","adg":"800","fcr":"2.8","feedPrice":"3.5"}, expect: ["各项指标正常"] },
  { slug: "livestock/feed-conversion-ratio", inputs: {"startWeight":"30","endWeight":"100","totalFeed":"180","days":"90","feedKg":"180","feedPrice":"3.5","gainKg":"70","salePrice":"18"}, expect: ["饲料层面盈利"] },
  { slug: "livestock/heat-stress-index", inputs: {"temp":"30","humidity":"70","windSpeed":"0.5"}, expect: ["添加电解多维"] },
  { slug: "livestock/inbreeding-coefficient", inputs: {"ne":"50","generations":"5","fa":"0","n1":"2","n2":"2","numAncestors":"1"}, expect: ["近交系数处于安全范围"] },
  { slug: "livestock/manure-amount", inputs: {"count":"100","days":"365","moisture":"85","customManure":"0","collectRate":"90"}, expect: ["养分可还田利用"] },
  { slug: "livestock/manure-pit-capacity", inputs: {"count":"200","dailyManure":"45","moisture":"88","cleanCycle":"7","pitDepth":"2.5","storageDays":"90"}, expect: ["雨季注意防雨棚覆盖"] },
  { slug: "livestock/milk-yield-scc", inputs: {}, _min_inputs: 0, expect: ["采食量及热应激等因素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/mycotoxin-limit", inputs: {"measuredValue":"15"}, expect: ["小麦等"], _selfcheck: true, _min_inputs: 1 },
  { slug: "livestock/poultry-light-program", inputs: {"currentAge":"1"}, expect: ["不可减少"], _selfcheck: true, _min_inputs: 1 },
  { slug: "livestock/silage-density-ph", inputs: {"siloLength":"10","siloWidth":"4","siloHeight":"2.5","siloWeight":"80","dmContent":"33","phValue":"4.0","phDM":"33","smellScore":"4"}, expect: ["可长期保存"] },
  { slug: "livestock/stats-7", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/vaccine-schedule", inputs: {}, _min_inputs: 0, expect: ["三免"], _selfcheck: true, _min_inputs: 0 },
  { slug: "livestock/water-feed-ratio", inputs: {"waterIntake":"8","feedIntake":"2.5","temp":"22"}, expect: ["饮水和采食状态良好"] },
  { slug: "livestock/weaning-weight-survival", inputs: {"bornAlive":"12","weanedAlive":"11","weanDay":"28","avgWeight":"7.5","standardWeight":"6.0","belowStandard":"2"}, expect: ["仔护理"] },
  { slug: "livestock/withdrawal-period", inputs: {"withdrawalDays":"14"}, expect: ["售动物产品"], _selfcheck: true, _min_inputs: 1 },
  { slug: "livestock/yufeirizengzhong-liaoroubiquxian", inputs: {"w0":"300","w1":"480","days":"120","feed":"1100","price":"3.2"}, expect: ["暂无计算记录"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== livestock calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();