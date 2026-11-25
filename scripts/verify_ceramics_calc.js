#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {
    "wet": "150",
    "dry": "135",
    "fired": "120",
    "targetFired": "200",
    "totalShrink": "18"
  },
  "clicks": [
    "calc();calcReverse()"
  ],
  "expect": [
    "20.00%",
    "10.00%",
    "11.11%",
    "243.90"
  ],
  "ref": "S干=(150−135)/150=10.00%、S烧=(135−120)/135=11.11%、S总=(150−120)/150=20.00%（独立复算）；反向 L₀=L₂/(1−S总)=200/(1−0.18)=243.90 mm。默认 120/112/100 ⇒ 6.67% / 10.71% / 16.67%、L₀=116.28 ⇒ 四个锚点全不命中。原 expect「公式」是 calcReverse 的 step-line 标签常量（默认态同样渲染）⇒ 已替换。"
},
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {"wet":"100","dry":"120","fired":"130"},
  "clicks": ["calc();"],
  "expect": ["尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成"],
  "ref": "注入 100/120/130（干坯大于湿坯、烧成大于干坯），calc() 报「尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成」且不产生 .big-result；默认 120/112/100 合法 ⇒ 不含该错误串。"
},
{
  "slug": "ceramics/glaze-ratio",
  "inputs": {
    "totalW": "1500",
    "w_'+idx+'": "-"
  },
  "expect": [
    "375.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {"wet":"100","dry":"120","fired":"130"},
  "clicks": ["calc();"],
  "expect": ["尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成"],
  "ref": "注入 100/120/130（干坯大于湿坯、烧成大于干坯），calc() 报「尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成」且不产生 .big-result；默认 120/112/100 合法 ⇒ 不含该错误串。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["MATS[4].pct='-5';calc();"],
  "expect": [
    "比例须为 0–100 的有限数"
  ],
  "ref": "第 5 项氧化锌比例注入 -5，calc() 逐行校验后列出「第 5 项「氧化锌」比例须为 0–100 的有限数（当前 -5）」并清空称量表；默认全 0–100 合法 ⇒ 不出现该文案。"
},
{
  "slug": "ceramics/glaze-temp",
  "inputs": {
    "coneTargetTemp": "1150"
  },
  "expect": [
    "最接近测温锥：4 · 1142°C · 中温"
  ],
  "ref": "改用页面真实计算输入：#coneTargetTemp（默认 1200，oninput=__coneLookup）。注入 1150 ⇒ 与 CONES 最近的锥 4（1142°C，中温），差值 +8°C（「高于锥号 4（1142°C）8°C」）、华氏 ≈2102.0 °F，判定在 ±30°C 容差内。原断言「1060°C」是默认全量表 CONES 的常量行（锥 01），与输入无关 ⇒ 零判别力，且该页本就有可注入的计算器，无需以 no_inputs 兜底。"
},
{
  "slug": "ceramics/kiln-firing",
  "clicks": ["switchTab('porcelain');"],
  "expect": [
    "峰值温度 1300°C；可计算段：升温 18.3 h + 保温 2.5–3.0 h + 慢冷 6.3 h = 约 27.0–27.5 小时（不含自然冷却段）。"
  ],
  "ref": "独立复算 porcelain：升温 (150−25)/50=2.5 +(600−150)/70=6.43 +(950−600)/100=3.5 +(1100−950)/50=3 +(1300−1100)/70=2.86 =18.29，保温 排湿1.5+氧化0.5+高保温0.5~1=2.5~3，慢冷 (1300−800)/80=6.25，合计 27.04~27.54 ⇒ 27.0–27.5 h；自然冷却未计入。switchTab() 切到 porcelain 后 render() 由 __kfEstimate 逐段按温度区间÷速率计保温，不再取静态 totalDesc。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {
    "diameter": "23"
  },
  "expect": [
    "0.230"
  ],
  "ref": "auto-restore"
}
,
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["MATS.forEach(function(m){m.pct=0;});MATS[0].pct=90;calc();var h=String(document.getElementById('result').innerHTML);var w=document.getElementById('w_0');document.getElementById('__tbProbe').textContent='TB828G '+((h.indexOf('低于 100%')>=0&&h.indexOf('不再用输入总重估算加水')>=0&&h.indexOf('需加水量')<0&&w&&w.value==='—')?'OK':'BAD');"],
  "expect": ["TB828G OK"],
  "ref": "第828批：配方合计 90% 时旧实现仍按输入总重算加水与釉浆。现在 |sum−100|>0.5 即停算，列出补足/扣减百分点表并把称量输入置 —，不输出需加水量。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {"diameter":"23","maxRpm":"60"},
  "expect": ["超过设备最高 60 rpm", "可用转速 ≈ 60 rpm（设备限幅后）"],
  "ref": "第828批：23cm 开孔标准偏好理论约 90 rpm，设备最高 60 rpm 时限幅到 60；旧实现硬编码 30–320 且仍称推荐。现在显示理论/可用/实际/偏差并明确限幅，探针断超限说明与可用转速文案。"
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

  console.log("==== ceramics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
