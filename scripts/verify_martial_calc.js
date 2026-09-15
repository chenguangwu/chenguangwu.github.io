#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // 注：collectStrings 在剥离 <strong> 标签时会插入空格，故期望值含「： 」后的空格
  { slug: "martial/breathing-rhythm", inputs: {"breathRate":"30"}, expect: ["呼吸周期： 2.00 秒"] },
  { slug: "martial/kick-height", inputs: {"kickHeight":"200"}, expect: ["高度比（身高）： 117.6%"] },
  // routine-timer 的 standardTime 会被 loadStandard() 按套路类型重算为区间中值，
  // 故改用 routineType 驱动：taijiquan 中值 (300+420)/2 = 360。
  { slug: "martial/routine-timer", inputs: {"routineType":"taijiquan"}, expect: ["标准： 360 秒"] },
  { slug: "martial/stance-center", inputs: {"frontRatio":"80"}, expect: ["前脚 80%"] },
  { slug: "martial/strike-resistance", inputs: {"trainYears":"3","freq":"7"}, expect: ["硬度指数： 119"] }
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
  console.log("==== martial calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();