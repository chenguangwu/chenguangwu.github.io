#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "woodwork/analysis-cost-price",
  "inputs": {
    "data": "3200,3300,3100,3400,3500",
    "ref": "3000",
    "warn": "10"
  },
  "expect": [
    "3300.00",
    "132.29",
    "4.01%",
    "3500.00",
    "+16.67%"
  ],
  "ref": "非默认输入+独立复算：均价3300、样本标准差132.29、CV4.01%、最新价3500、相对基准3000偏离+16.67%"
},
{
  "slug": "woodwork/angle-1",
  "inputs": {
    "v0": "45",
    "v1": "18",
    "v4": "45"
  },
  "expect": [
    "18×tan(45.0°)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/calculator-calc-15",
  "inputs": {
    "v0": "27",
    "v1": "60",
    "v4": "20",
    "v5": "6"
  },
  "expect": ["榫眼深 42.5 mm 已超过接合件厚度 20.0 mm"],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/convert-30",
  "inputs": { "mci": "30", "mcf": "12", "k": "0.26", "orig": "100" },
  "expect": ["4.68 %", "95.32 cm"],
  "ref": "初始 30%、终了 12%、收缩系数 0.26 → 线干缩率=(30−12)×0.26=4.68%，原 100cm 收缩后 ≈95.32cm（默认 30/8/0.26 → 5.72%/94.28，注入态不重合）"
},
{
  "slug": "woodwork/convert-30",
  "inputs": { "mci": "45", "mcf": "8", "k": "0.15", "orig": "100" },
  "clicks": ["document.getElementById('k').value='0.15';calc()"],
  "expect": ["3.30 %", "96.70 cm", "初始含水率高于纤维饱和点"],
  "ref": "初始 45%、终了 8%、径向系数 0.15 → (45−8)×0.15=5.55%，原 100cm→94.45cm"
},
{
  "slug": "woodwork/desk-dimensions",
  "inputs": {
    "height": "255",
    "mon": "24"
  },
  "expect": [ "椅面高度 181" ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/detector-32",
  "inputs": {
    "hcho": "3.8",
    "loadForce": "1200",
    "cycles": "10000",
    "stability": "0.15"
  },
  "expect": [ "3.8 mg/L", "存在不达标项目" ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/detector-37",
  "inputs": {
    "moisture": "21",
    "knotSize": "25",
    "width": "150",
    "knotCount": "3",
    "bend": "3"
  },
  "expect": [
    "21%"
  ],
  "ref": "auto-restore"
},
{ slug:"woodwork/detector-32", inputs:{"hcho":"","loadForce":"","stability":"","cycles":""}, expect:["请填写甲醛释放量与力学耐久指标"], ref:"核心检测值留空不得给出合格/优秀评级（DETCLR）" }
];
async function main() {
  const only = process.argv.slice(2);
  let pass = 0; const extraCases = [{ slug:"woodwork/angle-1", inputs:{v0:"100",v1:"18",v4:"45"}, expect:["目标斜切角须在 0–89.9°"], ref:"100° 旧实现静默截断到 89.9 并生成结果；新实现直接拒绝。默认 45° 不含提示。" },
{ slug:"woodwork/angle-1", inputs:{v0:"45",v1:"0",v4:"45"}, expect:["本计算的分母，不能为 0"], ref:"厚度 0 旧实现倒角/行程为 0 仍出结果；新实现拒绝 ≤0 厚度。" },
{ slug:"woodwork/angle-1", inputs:{v0:"0",v1:"18",v4:"45"}, expect:["0.0°"], ref:"0° 直切是合法输入，θ=0 时倒角宽 0、行程=t，不能被范围守卫误拦。" },
{ slug:"woodwork/analysis-cost-price", inputs:{data:"100xyz,200",ref:"100",warn:"10"}, expect:["无法解析的项"], ref:"parseFloat('100xyz') 旧实现静默取 100；新实现严格逐项校验并列出坏样本。" },
{ slug:"woodwork/analysis-cost-price", inputs:{data:"100,200",ref:"0",warn:"10"}, expect:["本计算的分母，不能为 0"], ref:"基准价 0 旧实现偏离率除零得 Infinity；新实现拒绝。" },
{ slug:"woodwork/analysis-cost-price", inputs:{data:"0,0",ref:"100",warn:"10"}, expect:["不适用（均价为 0）"], ref:"两个样本均为 0（合法）时均价 0，CV 标不适用而不是除零；偏离率仍可算。" },
{ slug:"woodwork/calculator-calc-15", inputs:{v0:"27",v1:"100",v4:"20",v5:"-10"}, expect:["端部榫肩不能为负"], ref:"宽 100、端肩 -10 旧实现得 120 mm 榫宽；新实现拒绝负肩，不给尺寸。" },
{ slug:"woodwork/calculator-calc-15", inputs:{v0:"27",v1:"100",v3:"through",v4:"20",v5:"50"}, expect:["榫宽 ≤ 0"], ref:"两肩 100 mm 等于工件宽度，旧实现榫宽 0、面积 0 仍展示；新实现阻断并提示。" },
{ slug:"woodwork/convert-30", inputs:{mci:"",mcf:"8",k:"0.26",orig:"100"}, expect:["请填写全部五项"], ref:"部分字段留空旧实现按 0 代入得 (-8)*0.26；新实现逐项提示缺失。" },
{ slug:"woodwork/convert-30", inputs:{mci:"0",mcf:"0",k:"0.26",orig:"100"}, expect:["0.00 %","100.00 cm"], ref:"显式 0% 含水率是合法输入，干缩率 0%、尺寸不变；不能把 0 当空值拦截。" },
];
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  extraCases.forEach(function(x){ if(!only.length || only.some((o)=>x.slug.endsWith("/"+o)||x.slug===o)) cases.push(x); });
  const fails = [];

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

  console.log("==== woodwork calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
