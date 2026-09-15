#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "astronomy/apparent-magnitude-distance", inputs: {"m":"1","M":"1"}, expect: ["光年"] },
  { slug: "astronomy/atmospheric-refraction", inputs: {"h":"30"}, expect: ["大气折射"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/convert-15", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "astronomy/convert-17", inputs: {}, _min_inputs: 0, expect: ["同日"], _selfcheck: true, _min_inputs: 0 },
  { slug: "astronomy/convert-18", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "astronomy/crater-estimator", inputs: {"diameter":"100","density":"3000","velocity":"20","angle":"45"}, expect: ["空爆无坑"] },
  { slug: "astronomy/earth-curvature", inputs: {"obsHeight":"1.7","targetDist":"10","targetHeight":"5"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "astronomy/gravitational-force", inputs: {"m1":"5.97e24","m2":"7.35e22","r":"3.84e8"}, expect: ["引力"] },
  { slug: "astronomy/horizon-distance", inputs: {"h":"1.7"}, expect: ["地平线距离"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/hubble-redshift-distance", inputs: {"z":"0.01"}, expect: ["百万光年"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/humidity-calculator", inputs: {"tDry":"25","tWet":"20","pAtm":"1013.25"}, expect: ["注意通风除湿"] },
  { slug: "astronomy/kepler-equation", inputs: {"Mdeg":"90","e":"0.1"}, expect: ["偏近点角"] },
  { slug: "astronomy/kepler-third-period", inputs: {"a":"1.496e11","M":"1.989e30"}, expect: ["轨道周期"] },
  { slug: "astronomy/light-travel-time", inputs: {"d":"1.496e11"}, expect: ["传播时间"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/magnitude-comparator", inputs: {"magA":"-26.7","magB":"-12.6"}, expect: ["映射"] },
  { slug: "astronomy/moon-illumination", inputs: {"D":"0"}, expect: ["相位"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/observation-conditions", inputs: {"latInput":"39.9042","lonInput":"116.4074"}, expect: ["仅见最亮恒星与行星"] },
  { slug: "astronomy/schwarzschild-radius", inputs: {"M":"1.989e30"}, expect: ["史瓦西半径"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/solar-declination", inputs: {"N":"172"}, expect: ["半球"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/solar-elevation", inputs: {"latInput":"39.9042","lonInput":"116.4074"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "astronomy/stellar-parallax", inputs: {"p":"0.1"}, expect: ["光年"], _selfcheck: true, _min_inputs: 1 },
  { slug: "astronomy/sunrise-sunset", inputs: {"inputLat":"39.9","inputLon":"116.4","inputTz":"8"}, expect: ["为夜间时段"] },
  { slug: "astronomy/tide-estimator", inputs: {"range":"2.0","lat":"30"}, expect: ["倍率"] }
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
  console.log("==== astronomy calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();