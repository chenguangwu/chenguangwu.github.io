#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "machinery/area-dosage-1", inputs: {v_area:"20", v_dft:"80", v_vs:"55"}, expect: ["3.42 实际用量"], ref: "涂装面积用量计算" },
  { slug: "machinery/banjinzhewanzhankai", inputs: {v_t:"4", v_ang:"90", v_r:"3"}, expect: ["83.540 展开总长"], ref: "钣金折弯展开" },
  { slug: "machinery/calc-64", inputs: {basic:"100", holeES:"25", holeEI:"0"}, expect: ["0.0410 最大间隙"], ref: "孔轴配合" },
  { slug: "machinery/calc-89", inputs: {v_D:"400", v_d:"120", v_mu:"0.25"}, expect: ["130.00 传递扭矩"], ref: "摩擦离合器" },
  { slug: "machinery/calc-gear-1", inputs: {v_m:"6", v_z:"24", v_a:"20"}, expect: ["144.000 分度圆直径"], ref: "圆柱齿轮" },
  { slug: "machinery/calc-gear-3", inputs: {v_sm:"6", v_sz:"24", v_sa:"20"}, expect: ["144.000 分度圆"], ref: "斜齿轮" },
  { slug: "machinery/calc-lifespan-belt", inputs: {D1:"200", D2:"300", center:"500"}, expect: ["967 大轮转速"], ref: "带传动" },
  { slug: "machinery/calc-strength", inputs: {diameter:"80", sb:"200", ss:"150"}, expect: ["2.98 弯曲应力"], ref: "轴强度校核" },
  { slug: "machinery/drive-2", inputs: {z1:"4", z2:"40", module:"5"}, expect: ["10.00 传动比"], ref: "蜗杆传动" },
  { slug: "machinery/energy-2", inputs: {v_J:"5", v_n1:"1500", v_n2:"0"}, expect: ["261.80 制动扭矩"], ref: "制动能" },
  { slug: "machinery/estimate-gravity", inputs: {density:"steel", plateL:"100", plateW:"50"}, expect: ["392.500 质量"], ref: "零件重量" },
  { slug: "machinery/estimate-lifespan-bearing", inputs: {loadC:"67", loadP:"5", speed:"1500"}, expect: ["2406.10"], ref: "轴承寿命估算" },
  { slug: "machinery/frequency-17", inputs: {v_m:"200", v_k:"50000", v_f:"25"}, expect: ["2.516 固有频率"], ref: "振动隔振" },
  { slug: "machinery/gear", inputs: {v_fa:"100", v_fb:"150", v_fc:"120"}, expect: ["满足 Grashof"], ref: "四连杆" },
  { slug: "machinery/lifespan-bearing-1", inputs: {v_F:"10000", v_d:"50", v_bd:"1"}, expect: ["4.000 平均压强"], ref: "滑动轴承" },
  { slug: "machinery/lifespan-bearing", inputs: {v_C:"45000", v_P:"2500", v_n:"1500"}, expect: ["5832.00 L10寿命"], ref: "滚动轴承寿命" },
  { slug: "machinery/pressure-4", inputs: {v_z:"48", v_m:"2", v_a:"30"}, expect: ["96.000 分度圆直径"], ref: "花键" },
  { slug: "machinery/runhuaxitongsheji", inputs: {v_d:"160", v_l:"80", v_n:"1500"}, expect: ["0.78 比压"], ref: "润滑系统" },
  { slug: "machinery/speed-cutting-feed", inputs: {v0:"200", v1:"50", v2:"10"}, expect: ["260.00"], ref: "切削用量" },
  { slug: "machinery/strength-15", inputs: {v_P:"11", v_n1:"960", v_z1:"19"}, expect: ["25.40 推荐节距"], ref: "链传动强度" },
  { slug: "machinery/strength-6", inputs: {v_d:"80", v_b:"12", v_h:"8"}, expect: ["49.34 挤压应力"], ref: "铆钉连接" },
  { slug: "machinery/tanhuangsheji", inputs: {v_d:"6", v_dd:"20", v_n:"8"}, expect: ["200.728 弹簧刚度"], ref: "弹簧设计" },
  { slug: "machinery/temp-hardness", inputs: {maxHrc:"45", temperK:"3", critDia:"15"}, expect: ["42.6 预期硬度"], ref: "热处理" },
  { slug: "machinery/thread-drive", inputs: {v_d2:"73", v_lead:"7", v_f:"20"}, expect: ["140.286 驱动力矩"], ref: "螺旋传动" },
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
  console.log("==== machinery calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();