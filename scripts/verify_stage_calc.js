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
  "expect": ["理论曲线输出： 144.6 / 255", "亮度增益： 0.753×"],
  "ref": "【更新】输出改为「理论曲线输出」并附非实测说明；平方律 192/255 => (192/255)^2×255=144.6。"
},
{
  "slug": "stage/dimmer-curve",
  "inputs": {"dmxInput": "50%"},
  "expect": ["DMX 输入： 128 / 255 （50.2%）","理论曲线输出： 31.8 / 255"],
  "ref": "百分比输入：50% 四舍五入为 DMX 128；平方律输出 (128/255)^2×255≈31.8，证明确实按百分比换算而非当 0/50 直通。"
},
{
  "slug": "stage/dimmer-curve",
  "inputs": {"dmxInput": ""},
  "expect": ["空值不会按 0 计算"],
  "ref": "空输入旧版 parseFloat||0 当 0 输出全黑；现直接提示，不输出曲线结果。"
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
  "expect": ["留空不会按 0 计算"],
  "ref": "光束角清空：旧 parseFloat(...)||0 按 0 输出零半径/零面积；现明确提示缺项并由 lastPos=null 拒绝复制。"
},
{
  "slug": "stage/light-position",
  "clicks": ["document.getElementById('beamAngle2').value='-20';calcPos();"],
  "expect": ["光束角需在 0-180°"],
  "ref": "负光束角：旧实现得到负半径与负面积；现拦截。"
},
{
  clicks: ["calc()"],
  "slug": "stage/power-load",
  "inputs": {
    "powerFactor": "0.9",
    "safetyMargin": "20"
  },
  "expect": ["总电流： 51.3 A", "最不利相约 78.2 A", "初步断路器参考： 100 A"],
  "ref": "默认 380V 三相：总功率 30.40kW/(√3×380×0.9)=51.3A；单相全集中一相时最不利 37.8+40.4=78.2A；裕度20%后93.9A，标准档参考100A（80%上限对应125A）。"
},
{
  "slug": "stage/power-load",
  "inputs": {"powerFactor": "0", "safetyMargin": "20"},
  "expect": ["功率因数须在 0（不含）到 1（含）之间"],
  "ref": "功率因数 0 不再被 `||1` 当作 1，显式拒绝。"
},
{
  "slug": "stage/power-load",
  "inputs": {"powerFactor": "", "safetyMargin": ""},
  "expect": ["留空不会被当作 0 或 1"],
  "ref": "空值与合法 0 区分；两项都空时不输出 51.3A 之类确定结果。"
},
{
  "slug": "stage/dimmer-curve",
  "inputs": {"dmxInput": "50abc"},
  "expect": ["请输入完整数值", "不接受"],
  "ref": "完整格式匹配，不再用 parseFloat 把 50abc 当 50；同时复制按钮置灰。"
},
{
  "slug": "stage/beam-angle",
  "inputs": {"beamAngle": "", "distance": "10", "intensity": "50000"},
  "expect": ["留空不会按 0 计算"],
  "ref": "光束角留空不再落成 0 后报范围错误，明确提示缺项。"
},
{
  "slug": "stage/light-position",
  "clicks": ["document.getElementById('projAngle').value='10';calcPos();"],
  "expect": ["不能形成封闭光斑"],
  "ref": "投射角 10° ≤ 半光束角 12.5°，下缘光线平行或高于舞台面，不应再输出圆截面面积当照射面积。"
},
{
  "slug": "stage/light-position",
  "clicks": ["document.getElementById('projAngle').value='45';document.getElementById('height2').value='6';document.getElementById('beamAngle2').value='25';calcPos();"],
  "expect": ["长轴 5.32 m", "面积 15.72 m²"],
  "ref": "45° 斜照、6m、25°：斜距8.49m、圆截面半径1.88m；舞台椭圆短轴3.76m、长轴3.76/sin45°=5.32m、面积π×2.66×1.88=15.72m²。"
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
