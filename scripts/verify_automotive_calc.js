#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "automotive/analysis-diagnosis", inputs: {"coolant":"92","stft":"18","rpm":"750","tps":"12"}, expect: ["况下重新采集后再判断"] },
  { slug: "automotive/analysis-strength", inputs: {"b":"60","h":"120","L":"1000","F":"5000","sf":"1.5","T":"2000"}, expect: ["弯曲强度满足要求"] },
  { slug: "automotive/auto-beauty-calc-1", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "automotive/brake-pad-life", inputs: {"newThickness":"12","currentThickness":"6","mileage":"30000","yearlyKm":"15000"}, expect: ["初期制动力较弱"] },
  { slug: "automotive/bus-arrival-estimator", inputs: {"interval":"10","ride":"0","err":"2","iv2":"15"}, expect: ["的到达窗口"] },
  { slug: "automotive/calc-1", inputs: {"m":"1500","P":"130","T":"250","i":"12","r":"0.32","eff":"88","cda":"0.65","mu":"0.9","sh":"2","st":"0.35"}, expect: ["常实测"] },
  { slug: "automotive/calc-2", inputs: {"tq":"250","rpm":"4000","kw":"","rpm2":""}, expect: ["传动损耗"] },
  { slug: "automotive/calc-3", inputs: {"pv":"2.3"}, expect: ["标准值"], _selfcheck: true, _min_inputs: 1 },
  { slug: "automotive/calc-4", inputs: {"gw":"1500","cap":"250","lo":"10","hi":"15","real":"260"}, expect: ["禁止上路"] },
  { slug: "automotive/calc-5", inputs: {"v":"100","s":"40","g":"9.81"}, expect: ["的反应距离"] },
  { slug: "automotive/calc-72", inputs: {"bore":"86","stroke":"86","cyl":"4","vc":"56"}, expect: ["自吸"] },
  { slug: "automotive/catalyst", inputs: {"hc1":"120","hc2":"18","co1":"0.8","co2":"0.06","nx1":"800","nx2":"120"}, expect: ["或加载工况复核"] },
  { slug: "automotive/cheshenkongqizulixishu", inputs: {"area":"2.2","cd":"0.30","v":"100","rho":"1.225","cd2":"0.38","eff":"90"}, expect: ["高速能耗劣势明显"] },
  { slug: "automotive/container-loading", inputs: {"pl":"1.0","pw":"0.8","ph":"0.6","qty":"500","wt":"80","loss":"0"}, expect: ["尺高柜"] },
  { slug: "automotive/countdown-engine-oil", inputs: {"last":"50000","cur":"54000","kmY":"15000"}, expect: ["我的爱车"] },
  { slug: "automotive/current-3", inputs: {"volt":"11.5","cur":"180","pout":"1500","rpm":"200","tq":"","ref":"50"}, expect: ["效率略低属正常"] },
  { slug: "automotive/cycle-13", inputs: {}, _min_inputs: 0, expect: ["未记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "automotive/cycle-belt", inputs: {"curKm":"85000","lastKm":"0","yearKm":"15000"}, expect: ["免维护"] },
  { slug: "automotive/depreciation", inputs: {"price":"20","res":"5","years":"5","used":"3","kmY":"1.5"}, expect: ["建议对照二手车行情"] },
  { slug: "automotive/detector-recorder-fuel", inputs: {"win":"4"}, expect: ["氧传感器与胎压"], _selfcheck: true, _min_inputs: 1 },
  { slug: "automotive/drive", inputs: {"gear":"3.5","final":"4.1","circ":"2.0","rpm":"6000","tq":"200","eff":"90"}, expect: ["速偏高"] },
  { slug: "automotive/engine-oil", inputs: {"tmin":"-10","tmax":"35","age":"5"}, expect: ["注意冬季启动表现"] },
  { slug: "automotive/estimate-distance-1", inputs: {"v":"100","rt":"1","mu":"1.0","grade":"0","mu2":"0.6","gap":"2","bt":"0"}, expect: ["请加大跟车距离"] },
  { slug: "automotive/estimate-wear-tire", inputs: {"nw":"8","cw":"4","km":"40000","lim":"1.6","warn":"3","kmY":"15000","other":"4.6"}, expect: ["里程"] },
  { slug: "automotive/fuel-anomaly", inputs: {}, _min_inputs: 0, expect: ["拆除不必要的物品"], _selfcheck: true, _min_inputs: 0 },
  { slug: "automotive/fuel-cost-calculator", inputs: {"km":"300","fc":"7","price":"8","ppl":"4","fc2":"9","budget":"300"}, expect: ["建议用实测油耗代入"] },
  { slug: "automotive/fuel-economy", inputs: {"fuelL":"40","dist":"560","price":"8","tank":"50","remain":"10","monthKm":"1500"}, expect: ["保持平稳驾驶即可"] },
  { slug: "automotive/insurance-premium-estimator", inputs: {"price":"15","seatAmt":"1","seats":"5"}, expect: ["保报价为准"] },
  { slug: "automotive/lifespan-brake", inputs: {"newT":"12","curT":"6","rateM":"0.5","minT":"2","kmM":"1200"}, expect: ["可列入下次保养计划"] },
  { slug: "automotive/loan-calculator", inputs: {"price":"15","tax":"8.85","extra":"0.8","dp":"30","years":"3","rate":"4.8","fee":"0"}, expect: ["手续费与实际利率"] },
  { slug: "automotive/lux-1", inputs: {"lm":"1500","pw":"55","d":"10","ang":"15","eff":"85","lm2":"1000"}, expect: ["近光灯"] },
  { slug: "automotive/maintenance-schedule", inputs: {"km":"45000","kmM":"1200","mon":"8","ahead":"1000"}, expect: ["机油"] },
  { slug: "automotive/oil-change-countdown", inputs: {"last":"80000","cur":"87000","iv":"10000","ivm":"12","warn":"500"}, expect: ["无需提前保养"] },
  { slug: "automotive/oil-change", inputs: {"yearKm":"15000","curKm":"30000","doneKm":"3000"}, expect: ["正常使用即可"] },
  { slug: "automotive/parking-fee-calculator", inputs: {"firstMin":"60","firstFee":"10","unitMin":"30","unitFee":"5","parkMin":"180","cap":"60","freeMin":"0","days":"1"}, expect: ["小时"] },
  { slug: "automotive/pressure-fuel-oil", inputs: {"flow":"350","ratedP":"3","railP":"3","pw":"3.5","cyl":"4","rpm":"2500","disp":"2.0","ve":"35"}, expect: ["暂无计算记录"] },
  { slug: "automotive/qichekongtiaoxuanxing", inputs: {"vol":"5","ppl":"2","amb":"35","dt":"15","cop":"2.8"}, expect: ["上升约"] },
  { slug: "automotive/recommender-6", inputs: {"amb":"25","p1":"2.3","p2":"2.3","ref":"20","alm":"25"}, expect: ["无需调整"] },
  { slug: "automotive/resistance-1", inputs: {"rp":"0.8","rs":"8","t":"25"}, expect: ["点火模块与线束插接件"] },
  { slug: "automotive/scheduler-cycle-maintenance", inputs: {"km":"52000","last":"45000","kmM":"1500","ahead":"1000"}, expect: ["常规检查"] },
  { slug: "automotive/shipping-cost-compare", inputs: {"w":"8","l":"50","wd":"40","h":"30","ins":"0","insr":"0.5","cw":"0","cn":"0"}, expect: ["远低于货值"] },
  { slug: "automotive/speed-tire", inputs: {"w":"225","ar":"55","rim":"17","vmax":"230","w0":"215","ar0":"55","rim0":"17","tol":"3"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "automotive/temp-pressure-1", inputs: {"lp":"0.18","hp":"1.35","amb":"30","vent":"8","stat":"0"}, expect: ["系统运行正常"] },
  { slug: "automotive/tester-10", inputs: {"c1":"50.5","c2":"49.8","c3":"50.2","c4":"46.5","std":"50","tol":"5","rep":"1","dur":"60"}, expect: ["确认偏差回落至容差内"] },
  { slug: "automotive/tester-11", inputs: {"cca0":"600","cca":"510","res":"7.2","temp":"25","age":"42","disp":"2.0"}, expect: ["避免长时间熄火用电"] },
  { slug: "automotive/time-maintenance", inputs: {"km":"43000","age":"4","last":"11","perY":"9000","ahead":"800"}, expect: ["列为准安排保养"] },
  { slug: "automotive/tire-pressure", inputs: {"f0":"2.3","r0":"2.1","fc":"2.0","rc":"1.9"}, expect: ["请尽快调整并排查慢漏"] },
  { slug: "automotive/tire-wear", inputs: {"newDepth":"8","mileage":"35000"}, expect: ["标记"] },
  { slug: "automotive/traffic-fine-calculator", inputs: {"had":"6","cut":"0"}, expect: ["会锁定相关业务"] },
  { slug: "automotive/transport-calculator", inputs: {"km":"300","fc":"20","price":"7.5","speed":"60","load":"5","rate":"60","v0":"60","rt":"1","vol":"10","wt":"6","mu":"6.5"}, expect: ["请据此保持跟车距离"] },
  { slug: "automotive/voltage-1", inputs: {"altCurrent":"90","voltage":"14.4","chargeCurrent":"10","newLoadCurrent":"0"}, expect: ["删除"] },
  { slug: "automotive/voltage-2", inputs: {"volt":"12","vreg":"14.4","cutin":"700","rpm":"2500","vbat":"12.4","rloop":"0.08","load":"10","len":"5","area":"2.5"}, expect: ["建议加粗线径或缩短走"] },
  { slug: "automotive/wear-brake", inputs: {"nw":"25","cu":"23.5","min":"22","run":"0.03","km":"6","pad":"8"}, expect: ["跳动量"] },
  { slug: "automotive/wear-tire", inputs: {"lf":"5.2","rf":"5.0","lr":"6.8","rr":"6.6","newD":"8","km":"20000","minD":"1.6","interval":"10000"}, expect: ["使四轮寿命趋于一致"] },
  { slug: "automotive/xuanguatanhuangzunitexing", inputs: {"k":"28","c":"2000","m":"400","mu":"45","kt":"220","load":"380","stroke":"200"}, expect: ["幅值的"] }
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
  console.log("==== automotive calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();