#!/usr/bin/env node
/**
 * 第 29 道门禁：fishery 分类计算正确性验证（8 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：aerator-duration / feed-rate-calculator / feeding-rate（含 select 品种/温度因子与多分支）；
 *       tank-volume / density-1 / cycle-6（动态形状/结构，stub 不稳）；water-oxygen（插值查表）。
 * 用法: node scripts/verify_fishery_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "fishery/calc-39",
    inputs: { v1: "500", v2: "20" },
    expect: ["100.00"],
    ref: "percent 默认 part 模式：v2% of v1 = 500×20/100=100.00（默认值避开）",
  },
  {
    slug: "fishery/salinity-calculator",
    inputs: { v1: "2000", s1: "5", s2: "40", st: "20" },
    expect: ["1500.00", "20.000"],
    ref: "V2=V1×(St−S1)/(S2−St)=2000×(20−5)/(40−20)=1500.00 L；混合后 3500.00 L、盐度 (2000×5+1500×40)/3500=20.000‰（默认 1000/0/35/15 避开）",
  },
  {
    slug: "fishery/water-exchange-rate",
    inputs: { volume: "1000", exchange: "200", prod: "0.6", cin: "0.2", ctarget: "3" },
    expect: ["3.20", "20.0"],
    ref: "换水率=200/1000=20.0%/天；τ=1000/200=5.0 天；稳态浓度=c_in+prod×τ=0.2+0.6×5=3.20 mg/L（默认 800/80/0.5/0.1/2 避开）",
  },
  {
    slug: "fishery/profit-calculator",
    inputs: { yield: "2000", price: "30", byproduct: "1000", seed: "2000", feed: "8000", electric: "800", medicine: "400", labor: "3000", rent: "2000", other: "500" },
    expect: ["61000", "44300"],
    ref: "收入=2000×30+1000=61000；直接=2000+8000+800+400=11200；间接=3000+2000+500=5500；总成本=16700；净利=61000−16700=44300（默认 5000/20… 避开）",
  },
  {
    slug: "fishery/fry-transport-survival",
    inputs: { density: "1000", duration: "12", temp: "15", target: "90", oxy: "air" },
    expect: ["0.4000", "67.0"],
    ref: "风险率=0.02×(1000/100)×(12/6)×exp((15−15)/12)×1.0=0.4；成活率=100×exp(−0.4)=67.0%（oxy=air 系数 1.0）",
  },
  {
    slug: "fishery/wastewater-cod",
    inputs: { feed: "80", fcr: "1.5", discharge: "300", codFactor: "0.4", limit: "30" },
    expect: ["32.00", "106.7"],
    ref: "COD 负荷=80×0.4=32.00 kg/天；浓度=32×1000/300=106.7 mg/L（默认 50/200/0.35 避开）",
  },
  {
    slug: "fishery/fish-weight",
    inputs: { length: "40", paramA: "0.02", paramB: "3" },
    expect: ["1280.00"],
    ref: "W=a·L^b=0.02×40³=1280.00 g（默认 30/0.0207/3.05 避开）",
  },
  {
    slug: "fishery/dissolved-oxygen",
    inputs: { temp: "20", press: "101.3", sal: "0", curDo: "8", hours: "10", rate: "0.3" },
    expect: ["5.00", "9.02"],
    ref: "黎明溶氧=8−0.3×10=5.00 mg/L；饱和溶氧=14.652−0.41022×20+0.007991×400−0.000077774×8000=9.02 mg/L（默认 26/6.5/9/0.35 避开）",
  },
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
  console.log("==== fishery calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();