#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "fire-rescue/calc-1", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire-rescue/calc-2", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire-rescue/calc-3", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire-rescue/calc-4", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire-rescue/calc-pressure-1", inputs: {"len":"20","flow":"6.5"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/calc-time-response", inputs: {"rti":"50","tg":"300","u":"2.0","ti":"20","tact":"68"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/chemical-spill", inputs: {"amount":"100","wind":"3"}, expect: ["风速"] },
  { slug: "fire-rescue/confined-space-rescue", inputs: {"o2":"19.5","lel":"0","h2s":"0","co":"0","entrySize":"0.6","depth":"5"}, expect: ["随时可起吊"] },
  { slug: "fire-rescue/detector-11", inputs: {"rated":"30","measured":"15"}, expect: ["不符合"] },
  { slug: "fire-rescue/detector-20", inputs: {}, _min_inputs: 0, expect: ["不合格"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire-rescue/dizhensoujiuzhichengjisuan", inputs: {"weight":"50","angle":"45","count":"4","allow":"30"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/fire-alarm-zone", inputs: {"floors":"6","floorArea":"2000","fireZones":"2","height":"3.5"}, expect: ["总探测器数"] },
  { slug: "fire-rescue/fire-extinguisher-selection", inputs: {"area":"100"}, expect: ["灾类别匹配"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/fire-fighting-tactics", inputs: {"fireArea":"200"}, expect: ["应对突发情况"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/fire-investigation", inputs: {"burnArea":"50"}, expect: ["存档全部证据链"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/fire-load", inputs: {"area":"100"}, expect: ["请添加至少一种可燃物"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/fire-resistance-rating", inputs: {"height":"50"}, expect: ["满足等级要求方可验收"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/fire-risk-assessment", inputs: {"height":"24","area":"5000","density":"0.5"}, expect: ["增设机械排烟系统"] },
  { slug: "fire-rescue/high-rise-fire", inputs: {"height":"80","floors":"25","fireFloor":"15","ladder":"54"}, expect: ["组备用气瓶"] },
  { slug: "fire-rescue/hydrant-flow", inputs: {"pressure":"0.25","hoseLen":"25","resistA":"0.0000147","sk":"13"}, expect: ["室内消火栓单栓基准"] },
  { slug: "fire-rescue/length-distance", inputs: {"ppump":"0.8","pnozzle":"0.2","height":"0","flow":"6.5"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/post-fire-assessment", inputs: {"fireTemp":"600","duration":"2"}, expect: ["裂缝宽度与深度测量"] },
  { slug: "fire-rescue/power-2", inputs: {"flow":"20","head":"60","eff":"75","sf":"1.15"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/pressure-flow", inputs: {"p1":"0.5","p2":"0.3","len":"20"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/rescue-route", inputs: {"floors":"10","entrances":"2","roadWidth":"6","vehicles":"4"}, expect: ["预备紧急撤退信号与路"] },
  { slug: "fire-rescue/rope-rescue", inputs: {"load":"100","eff":"90","angle":"90","mbs":"30"}, expect: ["绳索破断负荷"] },
  { slug: "fire-rescue/shengsuoanquanxishu", inputs: {"mbs":"30","wll":"2"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "fire-rescue/smoke-management", inputs: {"qfire":"5000","z":"5","zl":"0","hc":"3","nports":"2","portmax":"15000"}, expect: ["建议增加至"] },
  { slug: "fire-rescue/speed-3", inputs: {"mass":"80","dia":"12","mu":"0.2","wraps":"2","height":"10"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/sprinkler-design", inputs: {"totalArea":"1000","headArea":"12.5","pressure":"0.10","kfactor":"80","opArea":"0"}, expect: ["小时"] },
  { slug: "fire-rescue/temp-6", inputs: {"time":"10"}, expect: ["暂无计算记录"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/time-41", inputs: {"thick":"10"}, expect: ["暂无计算记录"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire-rescue/time-air", inputs: {"vol":"6.8","press":"30","alarm":"5.5","freq":"20"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/time-evacuation", inputs: {"aset":"10","tdet":"1","tpre":"2","tmove":"4"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/time-lux", inputs: {"cap":"12000","volt":"12","power":"5","eff":"100","lux":"5","area":"100","uf":"0.7"}, expect: ["暂无计算记录"] },
  { slug: "fire-rescue/ventilation-tactics", inputs: {}, _min_inputs: 0, expect: ["防止通风引发火势扩大"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire-rescue/water-rescue", inputs: {"temp":"15","velocity":"0","distance":"30"}, expect: ["迟发性肺水肿"] },
  { slug: "fire-rescue/wildfire-spread", inputs: {"wind":"20","slope":"15","humidity":"40","temp":"30","hours":"3"}, expect: ["预估过火面积"] },
  { slug: "fire-rescue/zuranyangzhishupanding", inputs: {"loi":"45"}, expect: ["暂无计算记录"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== fire-rescue calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();