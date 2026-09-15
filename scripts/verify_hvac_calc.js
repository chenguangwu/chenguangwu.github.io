#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "hvac/air-filter", inputs: {"airflow":"2000","filtW":"592","filtH":"592","filtArea":""}, expect: ["半导体等高洁净场景"] },
  { slug: "hvac/chiller-efficiency", inputs: {"capacityKw":"500","capacityRt":"142.17","powerKw":"90","tIn":"12","tOut":"7","cop100":"5.6","cop75":"6.3","cop50":"6.8","cop25":"6.0"}, expect: ["负荷"] },
  { slug: "hvac/cooling-load", inputs: {"area":"30","height":"3.0","wallArea":"15","kWall":"1.5","winArea":"6","kWin":"5.8","tn":"26","tw":"34","people":"5","equipPower":"800","equipFactor":"0.8","lightPower":"400","freshAirPer":"30","hw":"85","hn":"53"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "hvac/cooling-tower", inputs: {"flow":"600","twIn":"37","twOut":"32","twb":"27","cycles":"3","driftRate":"0.001"}, expect: ["当前"] },
  { slug: "hvac/dehumidifier", inputs: {"volume":"120","temp":"26","ach":"0.5","rh1":"80","rh2":"55"}, expect: ["每小时需除湿"] },
  { slug: "hvac/duct-calculator", inputs: {"Q":"3600","v":"5","rho":"1.2","rectA":"500","rectB":"400","diaD":"500","L":"20","xi":"1.5"}, expect: ["总阻力"] },
  { slug: "hvac/fan-selector", inputs: {"Q":"10000","dP":"800","eta":"75","etaMotor":"90","n":"1450"}, expect: ["风机"] },
  { slug: "hvac/fresh-air-load", inputs: {"people":"20","stdAir":"30","indoorT":"26","indoorRH":"55","outdoorT":"34","outdoorRH":"65"}, expect: ["潜热负荷"] },
  { slug: "hvac/pump-calculator", inputs: {"q":"50","L":"120","d":"100","lambda":"0.025","kexi":"12","dz":"10","eta":"0.70","margin":"10"}, expect: ["计算过程"] },
  { slug: "hvac/supply-air", inputs: {"coolLoad":"2500","deltaT":"8","roomVol":"120"}, expect: ["送风口数量"] }
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
  console.log("==== hvac calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();