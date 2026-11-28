#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "railway/diaoche-zuoye-xiaolv-youhua",
  "inputs": {
    "v0": "240",
    "v1": "36"
  },
  "expect": [
    "180.00",
    "16.67%"
  ],
  "ref": "v0=240,v1=36 → 单钩耗时 240/36=6.67 min/钩、每小时 36/240×60=9.00 钩/h、日产 9×20=180.00 钩、相对 8 min/钩 偏差 (8-6.67)/8=16.67%（默认 300/30 → 10.00/6.00/120.00/-25.00%，交换 30/300 → 0.10/600.00/12000.00/98.75%，均不重合；单钩耗时「6.67」被「16.67%」包含，故仅锚 180.00 与 16.67%）"
},
{
  "slug": "railway/power-5",
  "inputs": {
    "v0": "300",
    "v1": "80"
  },
  "expect": [
    "6666.67",
    "22.22",
    "3.750",
    "7843.14"
  ],
  "ref": "v0=300,v1=80、默认效率 85% → 牵引功率 300×80÷3.6=6666.67 kW、每 kN 牵引力 80/3.6=22.22 kW/kN、单位速度牵引力 300/80=3.750 kN/(km/h)、所需柴油机标定功率 6666.67÷0.85=7843.14 kW；默认 200/60 其他值不同，故可锚定"
},
{
  "slug": "railway/power-5",
  "inputs": { "v0": "-200", "v1": "60" },
  "expect": ["传动效率须在 0–100%"],
  "ref": "12-G3：负牵引力旧版照算 -3333.33 kW，修复后字段守卫拦截并提示正数要求；默认态无该提示。"
},
{
  "slug": "railway/power-5",
  "inputs": { "v0": "200", "v1": "0" },
  "expect": ["「运行速度 (km/h)」是本计算的分母"],
  "ref": "12-G3：速度 0 旧版提示泄露内部键名「v1」，修复后分母提示使用中文标签；默认态无该提示。"
},
{
  clicks: ["calc()"],
  "slug": "railway/brake-distance",
  "inputs": { "v": "80", "tr": "2", "a": "0.8", "g": "0", "m": "400" },
  "expect": ["353.1", "0.082"],
  "ref": "平坡 80 km/h、反应 2 s、仅制动力减速度 0.8 m/s²：总停车距离 353.09→353.1 m，所需粘着 0.8/9.81=0.082。"
},
{
  "slug": "railway/brake-distance",
  "inputs": { "v": "80", "tr": "2", "a": "0.8", "g": "-20", "m": "400" },
  "expect": ["453.4", "0.082"],
  "ref": "20‰ 下坡：等效减速度 0.6038 m/s²，总停车距离 453.38→453.4 m；坡度只改变距离，所需粘着仍为 0.8/9.81=0.082。"
},
{
  "slug": "railway/diaoche-zuoye-xiaolv-youhua",
  "inputs": { "v0": "240", "v1": "0" },
  "expect": ["0.00", "0 钩不可计算"],
  "ref": "零钩：0 钩时平均耗时不可计算，小时/班产钩数按 0；旧版除零后仍展示其他指标。"
},
{
  "slug": "railway/diaoche-zuoye-xiaolv-youhua",
  "inputs": { "v0": "300", "v1": "3.5" },
  "expect": ["完成钩数须为非负整数"],
  "ref": "小数钩数旧版照算效率，修复后字段校验拦截。"
},
]; // end cases
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

  console.log("==== railway calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
