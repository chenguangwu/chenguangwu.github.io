#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // 注：collectStrings 在剥离 <strong> 标签时会插入空格，故期望值含「： 」后的空格
  { slug: "martial/breathing-rhythm", inputs: {"breathRate":"30"}, expect: ["呼吸周期： 2.00 秒"] },
  { slug: "martial/kick-height", inputs: {"kickHeight":"200"}, expect: ["高度比（身高）： 117.6%"] },
  // routine-timer：standardTime 由 loadStandard() 按套路类型重算为区间中值（taijiquan → 360），
  // 完成耗时由 manualTime 注入（原仅计时器可写，页面加载即 myTime=0 → 速度比率 Infinity%，
  // 2026-09-23 已补 manualTime 输入 + myTime<=0 守卫）。
  // 例1 taijiquan 中值 360、耗时 330 → 速度比率 360/330×100 = 109.1%（在 300~420 允许范围内）
  { slug: "martial/routine-timer", inputs: { "routineType": "taijiquan", "manualTime": "330" }, expect: ["标准： 360 秒", "速度比率： 109.1%"] },
  // 例2 changquan 中值 80、耗时 95 → 速度比率 80/95×100 = 84.2%、偏差 +15.0、
  //     超上限扣分 (95−90)×0.5 = 2.5
  { slug: "martial/routine-timer", inputs: { "routineType": "changquan", "manualTime": "95" }, expect: ["速度比率： 84.2%", "+15.0"] },
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