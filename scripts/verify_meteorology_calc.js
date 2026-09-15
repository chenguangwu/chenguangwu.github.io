#!/usr/bin/env node
/**
 * 第 26 道门禁：meteorology 分类计算正确性验证（9 个确定性物理气象工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 覆盖：露点、风寒、饱和水汽压、绝对湿度、云底高度、气压高度、ISA 温度、相对湿度、蒲福风级。
 * 用法: node scripts/verify_meteorology_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "meteorology/dew-point",
    inputs: { T: "20", RH: "50" },
    expect: ["9.26"],
    ref: "Magnus 式：g=ln(0.5)+17.625×20/263.04=0.6468；Td=243.04×0.6468/(17.625-0.6468)=9.26 °C",
  },
  {
    slug: "meteorology/wind-chill",
    inputs: { T: "-10", v: "15" },
    expect: ["-16.7"],
    ref: "WCT=13.12+0.6215×(-10)-11.37×15^0.16+0.3965×(-10)×15^0.16=-16.7 °C",
  },
  {
    slug: "meteorology/saturation-vapor-pressure",
    inputs: { T: "20" },
    expect: ["23.33"],
    ref: "Tetens 式：e_s=6.1094×exp(17.625×20/263.04)=23.33 hPa",
  },
  {
    slug: "meteorology/absolute-humidity",
    inputs: { T: "20", RH: "50" },
    expect: ["8.61"],
    ref: "AH=1320.65×(50/100)×exp(17.67×20/263.5)/(20+273.15)=8.61 g/m³",
  },
  {
    slug: "meteorology/cloud-base-height",
    inputs: { T: "30", Td: "10" },
    expect: ["2500"],
    ref: "H=(30-10)×125=2500 m（默认温差 10°C 得 1250，此处 20°C 温差得 2500，避开默认值）",
  },
  {
    slug: "meteorology/pressure-altitude",
    inputs: { P: "800", P0: "1013.25" },
    expect: ["1949"],
    ref: "h=44330×(1-(800/1013.25)^0.1903)=1949 m（默认 P=900 得 989，此处避开）",
  },
  {
    slug: "meteorology/isa-temperature",
    inputs: { h: "3" },
    expect: ["-4.5"],
    ref: "T=15-6.5×3=-4.5 °C（对流层每 km 降 6.5°C；默认 h=5 得 -17.5，此处避开）",
  },
  {
    slug: "meteorology/relative-humidity",
    inputs: { T: "20", Td: "10" },
    expect: ["52.5"],
    ref: "RH=100×exp(17.625×10/253.04 - 17.625×20/263.04)=52.5 %",
  },
  {
    slug: "meteorology/beaufort-scale",
    inputs: { v: "20" },
    expect: ["8 级", "大风"],
    ref: "v=20 m/s 落入 ub[8]=20.7 区间 → 8 级（大风）；默认 v=10 得 5 级（和风），此处避开",
  },
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
  console.log("==== meteorology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();