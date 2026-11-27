#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
const path = require("path");
const P = (n) => path.join(__dirname, "..", "tools", "plastic", n);
function staticChecks() {
  const blow = fs.readFileSync(P("blow-molding.html"), "utf8");
  const extr = fs.readFileSync(P("extrusion-rate.html"), "utf8");
  const shrink = fs.readFileSync(P("shrinkage-calc.html"), "utf8");
  const inj = fs.readFileSync(P("injection-cycle.html"), "utf8");
  const mat = fs.readFileSync(P("material-select.html"), "utf8");
  return [
    { name: "吹塑明确圆截面面积比、轴向拉伸与均匀变形假设", ok: /axialStretch/.test(blow) && /圆截面面积比/.test(blow) && /不是通用表面积伸长/.test(blow) && /轴向拉伸比/.test(blow) && /均匀双向变形|均匀变形/.test(blow) },
    { name: "吹塑压力降级为静态应力换算且撤回推荐/选型结论", ok: /环向应力反算/.test(blow) && /不是热态型坯/.test(blow) && !/推荐吹胀压力：|理论最小吹胀压力|反推空压机/.test(blow) && !/再乘 1\.5 安全系数得推荐压力/.test(blow) },
    { name: "挤出复制复用有效结果快照", ok: /__extrValid/.test(extr) && /__extrText/.test(extr) && /if\(!__extrValid\)/.test(extr) },
    { name: "注塑复制复用统一校验状态", ok: /__injValid/.test(inj) && /if \(!__injValid\)/.test(inj) && inj.slice(inj.indexOf("function copyResult"), inj.indexOf("var phases")).indexOf("须为") < 0 },
    { name: "收缩率零收缩不显示无穷比例且复制复用状态", ok: /__shrinkRateValid/.test(shrink) && /__shrinkMoldValid/.test(shrink) && /无收缩（比例不适用）/.test(shrink) },
    { name: "选材搜索覆盖全部列并支持温度/强度/耐候筛选", ok: /row\.join\(" "|row\.join\(' '\)/.test(mat) && /minTemp/.test(mat) && /minStrength/.test(mat) && /climateFilter/.test(mat) && /参考范围/.test(mat) && /具体牌号/.test(mat) }
  ];
}
const CASES = [
{
  "slug": "plastic/blow-molding",
  "inputs": {"partDia":"83","parisonDia":"25","parisonWall":"4","bur":"3.2","yieldStr":"25","wallThk":"1.2","bottleDia":"80"},
  "expect": ["11.02"],
  "ref": "BUR²=(83/25)²≈11.02。"
},
{
  "slug": "plastic/extrusion-rate",
  "inputs": {"screwDia":"68","screwRpm":"80","density":"0.95","pitch":"65","channelDepth":"6","efficiency":"40"},
  "expect": ["75.96 cm³/rev", "6077 cm³/min", "138.6 kg/h"],
  "ref": "π/4×(68²−56²)×65/1000=75.96 cm³/rev；×80=6077 cm³/min；×0.95×0.40×3.6=138.6 kg/h。"
},
{
  "slug": "plastic/injection-cycle",
  "inputs": {"injectTime":"6","holdTime":"5","coolTime":"20","openTime":"3","ejectTime":"2","closeTime":"3","cavities":"4","hoursPerDay":"24","yieldRate":"95"},
  "expect": ["8862"],
  "ref": "周期 39 s，4 腔 24h、95% 良率日良品约 8862。"
},
{
  "slug": "plastic/shrinkage-calc",
  "inputs": {"moldSize":"103","partSize":"98.5","targetSize":"100","shrinkRate":"1.5"},
  "expect": ["4.5000"],
  "ref": "103−98.5=4.5 mm 收缩量。"
},
{
  "slug": "plastic/material-select",
  "inputs": {"filterSelect":"耐高温"},
  "expect": ["手机壳、镜片、头盔 透明 高强度 耐高温 PA66"],
  "ref": "按特性筛选后 PC 行紧邻 PA66 行，默认全表 PC 后为 POM ⇒ 该跨行串仅过滤态成立。"
},
{
  "slug": "plastic/blow-molding",
  "inputs": {"partDia":"","parisonDia":"25","parisonWall":"4","bur":"3.2","yieldStr":"25","wallThk":"1.2","bottleDia":"80"},
  "expect": ["制品直径与型坯直径均需大于 0"],
  "ref": "清空制品直径不得输出 0 与「偏小」。"
},
{
  "slug": "plastic/blow-molding",
  "inputs": {"partDia":"83","parisonDia":"25","parisonWall":"4","bur":"3.2","yieldStr":"","wallThk":"1.2","bottleDia":"80"},
  "expect": ["屈服强度、壁厚和直径均需大于 0"],
  "ref": "清空屈服强度不得输出 0 压强。"
},
{
  "slug": "plastic/injection-cycle",
  "inputs": {"injectTime":"6","holdTime":"5","coolTime":"20","openTime":"-3","ejectTime":"2","closeTime":"3","cavities":"4","hoursPerDay":"24","yieldRate":"95"},
  "expect": ["各工序时间与日运行小时须为非负数值"],
  "ref": "负工序时间不得参与周期。"
},
{
  "slug": "plastic/injection-cycle",
  "inputs": {"injectTime":"6","holdTime":"5","coolTime":"20","openTime":"3","ejectTime":"2","closeTime":"3","cavities":"4","hoursPerDay":"30","yieldRate":"95"},
  "expect": ["日运行小时须为非负数值"],
  "ref": "日运行 30 小时须拦截。"
},
{
  "slug": "plastic/shrinkage-calc",
  "inputs": {"moldSize":"100","partSize":"98.5","targetSize":"100","shrinkRate":"100"},
  "expect": ["收缩率须为 0–100%"],
  "ref": "100% 收缩率会除零。"
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

  const stat = staticChecks();
  const staticFails = stat.filter((x) => !x.ok);
  for (const x of staticFails) console.log("❌ [static] " + x.name);
  console.log("==== plastic calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
