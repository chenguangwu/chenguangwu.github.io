#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "stage/beam-angle",
  "inputs": {
    "beamAngle": "38",
    "distance": "10",
    "intensity": "50000"
  },
  "expect": [
    "37.25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stage/dimmer-curve",
  "inputs": {
    "dmxInput": "192"
  },
  "expect": ["square\n192\n调光曲线： 平方律曲线 DMX 输入： 192 / 255 （75.3%） 实际输出： 144.6 / 255 （56.7%） 亮度增益： 0.753×\n线性 192 平方律 145 S曲线 216 指数 125"],
  "ref": "auto-restore"
},
{
  "slug": "stage/light-position",
  "inputs": {
    "height": "9",
    "hDistance": "5",
    "projAngle": "45",
    "height2": "6",
    "beamAngle2": "25"
  },
  "expect": [
    "10.30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stage/light-position",
  "clicks": ["document.getElementById('beamAngle2').value='180';calcPos();"],
  "expect": ["光束角需在 0-180°"],
  "ref": "光束角 180°：旧实现 tan(90°) 得 Infinity/极大照射面积；现要求 0<光束角<180 并提示。默认 25° 合法，不命中。"
},
{
  "slug": "stage/light-position",
  "clicks": ["document.getElementById('beamAngle2').value='';calcPos();"],
  "expect": ["光束角需在 0-180°"],
  "ref": "光束角清空：旧 parseFloat(...)||0 按 0 输出零半径/零面积；现提示缺项，不再给出确定结果。"
},
{
  "slug": "stage/light-position",
  "clicks": ["document.getElementById('beamAngle2').value='-20';calcPos();"],
  "expect": ["光束角需在 0-180°"],
  "ref": "负光束角：旧实现得到负半径与负面积；现拦截。"
},
{
  "slug": "stage/power-load",
  "inputs": {
    "powerFactor": "3.9",
    "safetyMargin": "20"
  },
  "expect": [
    "总电流： 30.4 A"
  ],
  "ref": "总电流 = 26.10kW/(√3×220×3.9)… 页面输出 30.4 A（原单断言“30.4”命中深度解析示例里的“总功率 30.40 kW” → 逃生项）"
},
{
  "slug": "stage/stage-color-filter",
  "inputs": {
    "srcK": "4800",
    "targetK": "5600"
  },
  "expect": [ "-29 建议滤色片：" ],
  "ref": "auto-restore"
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

  console.log("==== stage calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
