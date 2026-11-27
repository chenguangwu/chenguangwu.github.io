#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "martial/breathing-rhythm", inputs: {"breathRate":"30"}, expect: ["呼吸周期 2.00 秒", "加总 100.0%"], ref: "独立复算：呼吸周期=60÷30=2.00 秒；默认 breathRate=12 → 5.00 秒，锚点不命中，依赖注入。" },
  { slug: "martial/kick-height", inputs: {"kickHeight":"200"}, expect: ["高度比（身高）： 117.6%"], ref: "独立复算：高度比=踢高÷身高=200÷170=117.6%；默认 kickHeight=150 → 88.2%。" },
  { slug: "martial/routine-timer", inputs: { "routineType": "taijiquan", "manualTime": "330" }, expect: ["标准： 360 秒", "速度比率： 109.1%"], ref: "独立复算：taijiquan 标准时长取区间中值 360 秒；330 → 速度比率=360÷330×100=109.1%。" },
  { slug: "martial/routine-timer", inputs: { "routineType": "changquan", "manualTime": "95" }, expect: ["速度比率： 84.2%", "+15.0"], ref: "独立复算：changquan 标准 80 秒；95 → 速度比率=80÷95×100=84.2%、偏差=95−80=+15.0。" },
  { slug: "martial/stance-center", inputs: {"frontRatio":"80"}, expect: ["前脚 80%"], ref: "独立复算：前脚承重比直接取 80%。0 与空值分别处理，不再用 50% 兜底。" },
  { slug: "martial/strike-resistance", inputs: {"trainYears":"3","freq":"7"}, expect: ["训练记录示意指数： 119"], ref: "独立复算：年限系数 1.0、频率系数 min(1.5,0.6+7×0.12)=1.44，前臂指数=40+55×1.44=119。" },
  {
    "slug": "martial/breathing-rhythm",
    "clicks": ["document.getElementById('breathRate').value='30';document.getElementById('inhaleRatio').value='0.5';document.getElementById('holdPct').value='5';calc();"],
    "expect": ["吸气 0.63s", "屏息 0.10s", "呼气 1.27s", "加总 100.0%"],
    "ref": "独立复算：周期=60÷30=2.00s；屏息=2.00×5%=0.10s；剩余1.90s按1:2拆为吸0.63s/呼1.27s，加总100%。"
  },
  {
    "slug": "martial/kick-height",
    "clicks": ["document.getElementById('height').value='120';document.getElementById('legLen').value='54';document.getElementById('kickHeight').value='120';document.getElementById('kickType').value='side';calc();"],
    "expect": ["估算踢腿角度： 90.0°", "高度比（腿长）： 222.2%"],
    "ref": "独立复算：角度=asin(120/(54+60))=asin(1.05) 截断为 90.0°；腿长 54 → 高度比=120÷54=222.2%。"
  },
  {
    "slug": "martial/routine-timer",
    "clicks": ["document.getElementById('standardTime').value='42';document.getElementById('tolerance').value='42';document.getElementById('manualTime').value='42';document.getElementById('routineType').value='nanquan';compare();"],
    "expect": ["完成时长： 42.0 秒", "扣分估算"],
    "ref": "独立复算：标准42、容差42、耗时42 → 速度100%，nanquan 下限75 非太极 → 扣分(75−42)×0.5=16.5。"
  },
  {
    "slug": "martial/stance-center",
    "clicks": ["document.getElementById('stepWidth').value='80';document.getElementById('height').value='170';document.getElementById('frontRatio').value='42';document.getElementById('squatDepth').value='42';document.getElementById('stanceType').value='bow';calc();"],
    "expect": ["重心水平偏移： 后6.4 cm", "重心高度估算： 51.5 cm"],
    "ref": "独立复算：偏移=(0.42−0.5)×80=−6.4cm；弓步高度=170×0.55−42=51.5cm。"
  },
  {
    "slug": "martial/strike-resistance",
    "clicks": ["document.getElementById('trainYears').value='1';document.getElementById('freq').value='42';calc();"],
    "expect": ["训练记录示意指数： 90"],
    "ref": "独立复算：年限系数0.6、频率系数封顶1.5，前臂=40+55×0.9=89.5→90。"
  }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== martial calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();