#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "seismology/analysis-stress",
  "inputs": { "data": "节面A,30,60,-90\n节面B,45,80,10" },
  "expect": [
    "节面数： 2",
    "P 300.0°/75.0°",
    "T 120.0°/15.0°"
  ],
  "ref": "按 Aki&Richards 节面解除算：节面A(30/60/−90) 正断型，P 轴 300.0°/75.0°、B 轴 30.0°/0.0°、T 轴 120.0°/15.0°；节面B(45/80/10) 走滑型（默认 1 个节面 45/60/0，P 4.1°/20.7°，避开）"
},
{
  "slug": "seismology/assessor-30",
  "inputs": {
    "pga": "300",
    "pgv": "20",
    "damageIndex": "0.3"
  },
  "clicks": ["calc()"],
  "expect": [
    "0.306 g",
    "VIII度"
  ],
  "ref": "auto-restore"
},
{
  "slug": "seismology/assessor-31",
  "inputs": {
    "totalBldg": "150",
    "minorDmg": "30",
    "moderateDmg": "15",
    "severeDmg": "8",
    "partialCol": "3",
    "totalCol": "1",
    "water": "2.5",
    "power": "30",
    "gas": "1.0",
    "road": "15",
    "comm": "20",
    "landslide": "5",
    "rockfall": "10",
    "cracks": "3",
    "liquefaction": "2"
  },
  "expect": [
    "0.097"
  ],
  "ref": "auto-restore"
},
{
  "slug": "seismology/assessor-31",
  "inputs": {
    "totalBldg": "0"
  },
  "expect": [
    "请输入大于 0 的建筑总数（栋）"
  ],
  "ref": "新增回归：建筑总数 0 曾因 `||1` 兜底把倒塌 1 栋算成 100%、直接判毁灭性；现应提示输入非法"
},
{
  "slug": "seismology/generator-drill",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "seismology/stats-attenuation",
  "inputs": {
    "mags": "3.0,3.5,4.0,4.5,5.0,3.2,4.1,4.8"
  },
  "clicks": ["calc()"],
  "expect": [
    "0.41",
    "1.94",
    "未独立估计"
  ],
  "ref": "默认 5 个震级 + Mc 按样本最小：b=0.41、a=1.94，并明确标注 Mc 未独立估计；2 个震级另见 N<5 用例"
},
{
  "slug": "seismology/stats-attenuation",
  "inputs": { "mags": "4.0,4.0" },
  "expect": ["至少需要 5 个 ≥Mc 的震级"],
  "ref": "12-G8：等震级序列旧版 b≈8.69、a≈35.04，修复后拒绝无跨度样本；默认序列有跨度，不命中。"
},
{
  "slug": "seismology/stats-attenuation",
  "inputs": { "mags": "3.0,4.0,5.0", "c": "-10", "t": "10" },
  "expect": ["K 与 p 须大于 0"],
  "ref": "12-G8：c=-10,t=10 使 t+c=0，旧版显示 Infinity 后被清洗为破折号，修复后参数守卫提示；默认 c=1 不命中。"
},
{ slug:"seismology/assessor-30", inputs:{"pga":"","pgv":"","damageIndex":""}, clicks:["calc()"], expect:["至少填写 PGA、PGV、震害指数中的一项仪器/震害指标后再评估"], ref:"全部输入留空不得输出 0/0.00 假结果；未观测项不按 0，至少需一项仪器/震害指标（NUMCLR）" },
  { slug: "seismology/assessor-31", inputs: { power: "" }, expect: ["调查资料不完整"], ref: "第827批：生命线供电损坏率留空原按 0 参与评分并仍给出震害等级；现 15 项必须全部填写，未知数据不按 0 处理、不出结论。默认 power=30 ⇒ 不命中。" },
  { slug: "seismology/assessor-31", inputs: { totalBldg: "10", minorDmg: "4", moderateDmg: "3", severeDmg: "2", partialCol: "1", totalCol: "1" }, expect: ["建筑受损类别合计 11 栋已超过建筑总数 10 栋"], ref: "第827批：受损类别互斥，4+3+2+1+1=11 超过 10；旧实现把指数 Math.min 截到 1 并继续判「毁灭性」，现直接停算并列出合计。默认 57≤100 ⇒ 不命中。" },
  { slug: "seismology/assessor-31", inputs: { totalBldg: "10.5" }, expect: ["建筑栋数与崩塌处数须为非负整数"], ref: "第827批：建筑总数为小数时旧实现照算并显示 100% 等结论；现要求栋数/崩塌处数为非负整数。默认 100 ⇒ 不命中。" },
  { slug: "seismology/assessor-30", inputs: { pga: "981" }, clicks: ["calc()"], expect: ["IX度", "1.000 g", "未观测（不参与）"], ref: "第1121批：仅观测 PGA=981 时应为 IX 度并显示 1.000 g；PGV/震害指数必须标未观测而非按 0。" },
  { slug: "seismology/assessor-31", inputs: { totalBldg:"1000",minorDmg:"200",moderateDmg:"100",severeDmg:"50",partialCol:"20",totalCol:"10",water:"30",power:"40",gas:"2",road:"50",comm:"60",landslide:"20",rockfall:"10",cracks:"5",liquefaction:"3" }, clicks: ["calc()"], expect: ["37", "高指数区间"], ref: "第1121批：综合 0.3676 显示 37，只映射相对区间；不得出现安置人口或 I 级响应。" },
  { slug: "seismology/stats-attenuation", inputs: { mags:"3.0,3.5,4.0,4.5,5.0,3.2,4.1,4.8", mc:"", dM:"0.1" }, clicks: ["calc()"], expect: ["未独立估计", "0.41"], ref: "第1121批：Mc 留空用样本最小值并明确标注未独立估计，不静默当 0。" },
  { slug: "seismology/stats-attenuation", inputs: { mags:"3.0,4.0" }, clicks: ["calc()"], expect: ["至少需要 5 个 ≥Mc 的震级"], ref: "第1121批：N<5 不出 b 值，避免小样本拟合。" },
  { slug: "seismology/generator-drill", inputs: { cnt:"50" }, clicks: ["gen()"], expect: ["生成数量须为"], ref: "第1121批：数量 50 直接报错，不回退默认 5。" }
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

  console.log("==== seismology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
