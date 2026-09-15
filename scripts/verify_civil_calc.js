#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "civil/active-earth-rankine", inputs: {"gamma":"18","H":"5","phi":"30","c":"0"}, expect: ["主动土压力合力"] },
  { slug: "civil/beam-udl", inputs: {"L":"6","q":"20","E":"30","I":"8000","b":"200","h":"400"}, expect: ["跨中弯曲应力"] },
  { slug: "civil/calc-1", inputs: {"fcuk":"30","sigma":"5.0","wc":"0.50","mw":"190","beta":"38","rhoC":"3100","rhoS":"2650","rhoG":"2700","air":"1.0"}, expect: ["水泥"] },
  { slug: "civil/calc-2", inputs: {"straight1":"3000","straight2":"0","diameter":"20","angle1":"90","angle2":"0","bendFactor":"2.5","cover":"25","num":"1"}, expect: ["弯钩增加"] },
  { slug: "civil/carbonation-depth", inputs: {"K":"2.0","t":"30"}, expect: ["碳化深度"] },
  { slug: "civil/cft-capacity", inputs: {"D":"400","t":"10","fc":"40","fy":"345"}, expect: ["承载力"] },
  { slug: "civil/concrete-volume", inputs: {"a":"4","b":"0.4","c":"0.5","rho":"2400"}, expect: ["重量"] },
  { slug: "civil/concrete-wb-ratio", inputs: {"fcu":"38.2","fb":"45","aa":"0.53","ab":"0.20"}, expect: ["胶水比"] },
  { slug: "civil/excavation-earth", inputs: {"gamma":"19","H":"8","phi":"30","q":"10"}, expect: ["主动土压力合力"] },
  { slug: "civil/isolated-footing", inputs: {"N":"800","M":"80","fa":"200","gamma":"20","d":"1.5","B":"2.5"}, expect: ["基底压力满足要求"] },
  { slug: "civil/load-combination", inputs: {"Sg":"50","Sq":"30","gG":"1.3","gQ":"1.5"}, expect: ["组合效应"] },
  { slug: "civil/masonry-bearing", inputs: {"f":"2.5","b":"240","L":"3000","phi":"1.0"}, expect: ["材料抗力"] },
  { slug: "civil/one-way-slab", inputs: {"M":"8","h":"120","fc":"14.3","fy":"360","as":"20"}, expect: ["每米配筋"] },
  { slug: "civil/pile-capacity", inputs: {"d":"0.6","L":"15","qs":"40","qp":"2000","K":"2"}, expect: ["单桩承载力特征值"] },
  { slug: "civil/rc-beam-rebar", inputs: {"M":"150","b":"250","h":"500","fc":"14.3","fy":"360","as":"40"}, expect: ["配筋率"] },
  { slug: "civil/rebar-anchorage", inputs: {"fy":"360","ft":"1.43","d":"20","za":"1.0"}, expect: ["基本锚固长度"] },
  { slug: "civil/rebar-weight", inputs: {"d":"20","L":"9","n":"10"}, expect: ["总重"] },
  { slug: "civil/rock-mass-rating", inputs: {"s1":"12","s2":"13","s3":"10","s4":"20","s5":"10"}, expect: ["围岩级别"] },
  { slug: "civil/slope-stability-fos", inputs: {"gamma":"19","z":"3","alpha":"30","c":"10","phi":"28"}, expect: ["边坡稳定满足一般要求"] },
  { slug: "civil/two-way-slab", inputs: {"q":"10","lx":"4","ly":"5"}, expect: ["比值"] },
  { slug: "civil/wind-load", inputs: {"w0":"0.5","mz":"1.0","ms":"1.3","bz":"1.5"}, expect: ["风荷载标准值"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== civil calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();