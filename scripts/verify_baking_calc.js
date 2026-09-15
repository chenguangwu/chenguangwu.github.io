#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "baking/baker-percentage", inputs: {"flourWeight":"500","targetTotal":"800","newPct":"50"}, expect: ["复制配方"] },
  { slug: "baking/convert-28", inputs: {"flour":"500","pct":"60"}, expect: ["面粉"] },
  { slug: "baking/convert-temp", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "baking/dough-hydration", inputs: {"flour":"500","water":"350"}, expect: ["较高含水量"] },
  { slug: "baking/fermentation-time", inputs: {"baseTime":"60","actualTemp":"24","actualHumidity":"70"}, expect: ["湿度适宜"] },
  { slug: "baking/mold-volume", inputs: {"'+side+'D":"'+(side==='from'?'15':'20')+'","'+side+'H":"7","'+side+'S":"'+(side==='from'?'15':'20')+'","'+side+'L":"'+(side==='from'?'15':'20')+'","'+side+'W":"10"}, expect: ["高度"] },
  { slug: "baking/mold", inputs: {"v0":"100","v1":"50","v2":"10"}, expect: ["合计"] },
  { slug: "baking/oven-temp", inputs: {"tempC":"180","tempF":"50"}, expect: ["请输入有效温度"] },
  { slug: "baking/recipe-scaler", inputs: {"factor":"1.5"}, expect: ["黄油"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== baking calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();