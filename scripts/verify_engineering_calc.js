#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
// 2026-09-24 去默认化（BATCH69）：原 14 例里有 12 例的输入等于页面默认值、expect 又是
// 「轴向变形 / 公式 / 矩形 / 扭转角」这类**静态标签词** ⇒ 默认态同样命中（真逃生项）。
// 此前这批从未被判别器检到：判别器的 pageDefaults 按 deep-dive 标记截断，而本分类
// heat-transfer / material-calculator / stress-calculator 三页的表单在 deep-dive 之后
// （且存在重复 id），取不到默认值 ⇒ 整例静默判「跳过」。修好判别器后才暴露。
// 修法：输入改为非默认值，expect 全部换成 Python/笔算独立复算出的派生量。
const CASES = [
  { slug: "engineering/axial-stress", inputs: {"F":"30","A":"250","E":"210","L":"1.5"}, expect: ["5.714e-4", "0.857"], ref: "σ=F/A=30kN/250mm²=120.00 MPa；ε=σ/E=120/210000=5.714e-4；ΔL=ε·L=5.714e-4×1500mm=0.857 mm。默认 50/500/200/2 得 100.00 MPa / 9.524e-4 / 0.952 mm（原 expect「轴向变形」是静态标签词）" },
  { slug: "engineering/beam-calculator", inputs: {"length":"6","load":"15","E":"210","I":"800","limit":"300"}, expect: ["150.67 mm", "1680000.00"], ref: "简支梁均布 δ=5qL⁴/(384EI)：EI=210GPa×800cm⁴=1680 kN·m² ⇒ δ=5×15×6⁴/(384×1680)=0.15067 m=150.67 mm；许用 L/300=20.00 mm ⇒ 不满足。默认 5/10/200/500/250 得 81.38 mm（原 expect「公式」是静态词）" },
  { slug: "engineering/bending-stress", inputs: {"M":"36","b":"120","h":"240"}, expect: ["31.25", "1152000"], ref: "W=bh²/6=120×240²/6=1152000 mm³；σ=M/W=36e6/1152000=31.25 MPa。默认 20/150/300 得 W=2250000、σ=8.89 MPa（原 expect「最大弯曲应力」是静态标签词）" },
  { slug: "engineering/bolt-preload", inputs: {"T":"85","d":"16","K":"0.18"}, expect: ["29.51", "29514"], ref: "F=T/(K·d)=85/(0.18×0.016)=29514 N=29.51 kN。默认 100/12/0.2 得 41.67 kN（原 expect「预紧力」是静态标签词）" },
  { slug: "engineering/cantilever-deflection", inputs: {"P":"8","L":"2.5","E":"25","I":"8000"}, expect: ["20.83", "0.716"], ref: "δ=PL³/(3EI)=8000×15.625/(3×2e6)=0.02083 m=20.83 mm；θ=PL²/(2EI)=0.0125 rad=0.716°。默认 5/3/30/5000 得 30.00 mm / 0.859°（原 expect「自由端转角」是静态标签词）" },
  { slug: "engineering/heat-transfer", inputs: {"k":"0.04","A":"10","L":"0.2","T1":"20","T2":"0","h":"10","Ts":"80","Tinf":"20","eps":"0.9","T1K":"500","T2K":"300","h1":"10","h2":"20"}, expect: ["传热量 Q 40.00 W", "热阻 R 0.5000 K/W"], ref: "导热 Q=k·A·ΔT/L=0.04×10×20/0.2=40.00 W；R=L/(kA)=0.2/(0.04×10)=0.5000 K/W；q=Q/A=4 W/m²。默认 k=50/A=1/L=0.1/T1=100/T2=20 得 Q=40000.00 W、R=0.0020 K/W（原 expect「温差」是静态标签词）" },
  { slug: "engineering/material-calculator", inputs: {"b":"50","h":"200","L":"2","d":"5.5","D":"50","t":"5","a":"50","c":"50"}, radios: { material: "2" }, expect: ["重量 54.00 kg", "材料 铝 (2700 kg/m³)"], ref: "该页控件由 JS 模板 innerHTML 生成、材料靠 getElementsByName('material') 单选组读取 ⇒ 必须显式 radios 注入，否则 calc 取不到材料而抛错。矩形 b=50mm×h=200mm：A=10000mm²=100cm²、I=b·h³/12=3.3333e7mm⁴=3333.33cm⁴；V=0.01m²×2m=0.02m³=20.00L；铝 2700kg/m³ ⇒ 重量 54.00 kg、每米 27.00 kg/m。默认 b=100/L=1/钢7850 得 157.00 kg（体积同为 20.00 L，不可锚体积；原 expect「角钢」只是形状页签名）" },
  { slug: "engineering/poisson-strain", inputs: {"ex":"0.0018","nu":"0.32"}, expect: ["-5.760e-4", "6.480e-4"], ref: "ε_y=−ν·ε_x=−0.32×0.0018=−5.760e-4；ε_v=ε_x(1−2ν)=0.0018×0.36=6.480e-4。默认 0.001/0.3 得 −3.000e-4 / 4.000e-4。注：不可锚「0.320」——那是 ν 的输入值回显（原 expect「泊松比」是静态标签词）" },
  { slug: "engineering/pressure-vessel", inputs: {"P":"2.5","D":"1200","sigma":"150","phi":"0.9"}, expect: ["11.11", "13.11"], ref: "t=PD/(2σφ)=2.5×1200/(2×150×0.9)=3000/270=11.11 mm；计入腐蚀裕量 +2mm = 13.11 mm。默认 1.6/1000/130/0.85 得 7.24 / 9.24 mm（原 expect「计入腐蚀裕量后」是静态标签词）" },
  { slug: "engineering/section-inertia", inputs: {"shape":"1","b":"250","h":"500"}, expect: ["2604166667", "10416667"], ref: "矩形 I=bh³/12=250×500³/12=2.6041667e9 mm⁴；W=I/(h/2)=2604166667/250=1.0416667e7 mm³。默认 200/400 得 1.0667e9 / 5.3333e6（原 expect「矩形」是公式标签里的静态词）" },
  { slug: "engineering/shaft-torsion", inputs: {"T":"3.5","d":"60","G":"79","L":"1.2"}, expect: ["82.52", "2.394"], ref: "J=πd⁴/32=1272345 mm⁴；τ=Tr/J=3.5e6×30/1272345=82.52 MPa；θ=TL/(GJ)=0.04178 rad=2.394°。默认 2/50/80/1 得 81.49 MPa / 2.334°（原 expect「扭转角」是静态标签词）" },
  { slug: "engineering/stress-calculator", inputs: {"F":"80","A":"400","V":"45","M":"8000","W":"160","T":"1500","D":"60","d":"20"}, radios: { material: "2" }, expect: ["200.00 MPa", "安全系数 n 1.77"], ref: "材料表同样靠 getElementsByName('material') 读取，须 radios 注入（此处 index 2 = 45钢 yield 355）。σ=F/A=80kN/400mm²=200.00 MPa；许用=355/1.5=237 MPa；n=355/200=1.77；比例 56% ✅安全。默认 50/500 + Q235(235) 得 100.00 MPa / n=2.35（判定词「✅ 安全」两者皆命中，不可作 expect）" },
  { slug: "engineering/thermal-expansion", inputs: {"alpha":"17","L0":"12","dT":"55"}, expect: ["11.220", "0.0112"], ref: "ΔL=α·L₀·ΔT=17e-6×12×55=0.01122 m=11.220 mm。默认 12/10/40 得 4.800 mm / 0.0048 m（原 expect「膨胀量」是静态标签词）" },
  { slug: "engineering/weld-strength", inputs: {"F":"75","hf":"8","lw":"250"}, expect: ["53.57", "1400"], ref: "A_e=0.7·hf·lw=0.7×8×250=1400 mm²；τ=F/A_e=75000/1400=53.57 MPa。默认 50/6/200 得 840 mm² / 59.52 MPa（原 expect「焊缝剪应力」是静态标签词）" }
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
  console.log("==== engineering calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
