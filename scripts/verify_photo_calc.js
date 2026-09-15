#!/usr/bin/env node
/**
 * 第 44 道门禁：photo 分类计算正确性验证（18 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除（非数值/依赖外部状态，stub 无验证意义）：
 *   - golden-hour：依赖日期/地理位置计算日出日落，非确定性
 *   - convert-focal：含 select 画幅换算 + 文本输出，无稳定单值
 *   - photo-11：快门下限 1/4000 截断 + 多段中间量，取值依赖倒推
 *   - card-capacity/photo-7 等已覆盖同类公式
 * 用法: node scripts/verify_photo_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "photo/bracketing-plan",
    inputs: { range: "9", step: "3", base: "2" },
    expect: ["-2.5", "6.5"],
    ref: "张数=9/3+1=4；最低EV=2−9/2=−2.5；最高EV=2+9/2=6.5（默认 3/1/0→4/−1.5/1.5，避开）" },

  { slug: "photo/card-capacity",
    inputs: { card: "128", per: "40", jpeg: "8" },
    expect: ["3200", "16000"],
    ref: "RAW=128×1000/40=3200；JPEG=128×1000/8=16000（默认 64/25/5→2560/12800，避开）" },

  { slug: "photo/depth-of-field",
    inputs: { f: "35", n: "8", s: "3", c: "0.03" },
    expect: ["5.14", "7.09"],
    ref: "H=35²/(8×0.03)+35=5139.17mm=5.14m；后景深=H×smm/(H−smm+f)/1000=5.14×… →7.09m（默认 50/2.8/5→29.81/4.29/6.00，避开）" },

  { slug: "photo/dpi",
    inputs: { width_px: "6000", height_px: "4000", print_w: "20", dpi: "300" },
    expect: ["13.3", "762.0"],
    ref: "打印高度=4000/6000×20=13.3cm；当前DPI=6000/(20/2.54)=762.0（默认 3000/2000/30/300→20.0/254.0，避开）" },

  { slug: "photo/dynamic-range",
    inputs: { maxL: "4096", minL: "2", sensorStops: "14" },
    expect: ["11.00"],
    ref: "DR=log2(4096/2)=log2(2048)=11.00 档（默认 1024/1→10.00，避开）" },

  { slug: "photo/equivalent-focal",
    inputs: { focal: "60", crop: "1.5", sensorW: "36" },
    expect: ["90.0", "22.6"],
    ref: "等效焦距=60×1.5=90.0mm；视角=2·atan(36/(2×90))×180/π=22.6°（默认 35/1.5→52.5/37.8，避开）" },

  { slug: "photo/ev",
    inputs: { aperture: "11", shutter: "0.008", iso: "400" },
    expect: ["11.88", "13.88"],
    ref: "EV100=log2(11²/0.008)−log2(400/100)=13.88−2=11.88；实际EV=13.88（默认 2.8/0.01/100→9.61，避开）" },

  { slug: "photo/field-of-view",
    inputs: { focal: "24", sensor: "36", sensorH: "24" },
    expect: ["73.7", "53.1"],
    ref: "水平=2·atan(36/48)×180/π=73.7°；垂直=2·atan(24/48)×180/π=53.1°（默认 50/36/24→39.6/27.0，避开）" },

  { slug: "photo/flash-gn",
    inputs: { gn: "60", dist: "4", iso: "400" },
    expect: ["15.0", "21.4"],
    ref: "可用光圈=60/4=15.0 f；最远有效=60/2.8=21.4m（默认 40/5/100→8.0/14.3，避开）" },

  { slug: "photo/hyperfocal",
    inputs: { f: "35", n: "11", c: "0.03" },
    expect: ["3747", "3.75"],
    ref: "H=35²/(11×0.03)+35=3712.12+35=3747mm=3.75m（默认 24/8→2424/2.42，避开）" },

  { slug: "photo/mired",
    inputs: { k: "3200", shift: "20" },
    expect: ["312.5"],
    ref: "Mired=10⁶/3200=312.5（默认 5600→178.6，避开）" },

  { slug: "photo/nd-filter",
    inputs: { base: "0.01", stops: "6", target: "1.28" },
    expect: ["0.64", "7.00"],
    ref: "新快门=0.01×2⁶=0.64s；达标档数=log2(1.28/0.01)=log2(128)=7.00 档（默认 0.01/10→10.24/9.97，避开）" },

  { slug: "photo/photo-3",
    inputs: { gn: "48", aperture: "8", iso: "400" },
    expect: ["12.00"],
    ref: "实际ISO距离=48/8×√(400/100)=6×2=12.00m（默认 36/4/100→9.00，避开）" },

  { slug: "photo/photo-8",
    inputs: { mp: "45", depth: "16", compression: "2" },
    expect: ["85.83", "42.92"],
    ref: "未压缩=45×10⁶×16/8/1048576=85.83MB；压缩后=85.83/2=42.92MB（默认 24/14/3→40.05/13.35，避开）" },

  { slug: "photo/print-size",
    inputs: { width: "6000", height: "4000", dpi: "300", unit: "mm" },
    expect: ["508.0", "338.7"],
    ref: "宽=6000/300×25.4=508.0mm；高=4000/300×25.4=338.7mm（默认 3000/2000/72→1058.3/705.6，避开）" },

  { slug: "photo/raw-size",
    inputs: { mp: "50", bit: "16", fps: "12" },
    expect: ["100.0", "72.00"],
    ref: "RAW=50×10⁶×16/8/10⁶=100.0MB；分钟@10帧=100×12×60/1000=72.00GB（默认 24/14/10→42.0/25.2，避开）" },

  { slug: "photo/safe-shutter",
    inputs: { focal: "200", crop: "1", ibis: "2" },
    expect: ["0.0050", "0.0013"],
    ref: "安全快门=1/(200×1)=0.0050s；防抖后=1/(200×2²)=0.0013s（默认 50/1.5/3→0.0133/0.0017，避开）" },

  { slug: "photo/calc-exposure-aperture",
    inputs: { aperture: "11", shutter: "1/250", iso: "200" },
    expect: ["13.88"],
    ref: "EV100=log2(11²/(1/250))−log2(200/100)=log2(30250)−1=14.88−1=13.88（默认 f8/1÷125/ISO100→12.97，避开）" },
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
  console.log("==== photo calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();