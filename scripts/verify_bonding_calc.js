#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "bonding/assessor-cycle-lifespan",
  "inputs": {
    "sigmaB": "900",
    "deltaSigma": "300",
    "sigmaM": "150",
    "kt": "1.5",
    "designN": "80",
    "surface": "0.8"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "421.4",
    "5.27"
  ],
  "ref": "σE=900×0.5×0.8/1.5=240.0 MPa；σEq=300/2/(1−150/900)=180.0 MPa；N=(240/180)^5×10^6=4.2140×10^6 → 421.4 万次；sf=421.4÷80=5.27 → 安全（独立复算）。默认 σb600/Δσ200/σm100/Kt2.0/设计100万次 ⇒ N=100.0 万次、sf=1.00，与本例两个锚点零交集。原 expect「建议结合实验验证」是该页 info-box 常驻文案（注入失败同样命中）⇒ 已替换。"
},
{
  "slug": "bonding/detector-26",
  "inputs": {
    "designT": "0.3",
    "tolerance": "10",
    "measures": "0.28,0.32,0.30,0.31,0.29,0.30,0.31,0.29",
    "defect": "1"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "13.3%",
    "0.280 mm",
    "6.7%"
  ],
  "ref": "avg=(0.28+0.32+0.30+0.31+0.29+0.30+0.31+0.29)/8=0.300；极差=0.32−0.28=0.04 ⇒ cv=0.04/0.30×100=13.3%；maxDev=max(|0.32−0.3|,|0.28−0.3|)/0.3×100=6.7%；测点1 偏差=(0.28−0.3)/0.3=−6.7% ⇒ 行内「0.280 mm」（独立复算）。默认 设计0.2/公差20/8 点 0.18…0.19 ⇒ avg0.199、maxDev15.0%、cv30.2%，与本例三个锚点零交集。原 expect「建议返修补胶后复检」= 默认态 advice（注入失败同样命中）⇒ 已替换。"
},
{
  "slug": "bonding/detector-27",
  "inputs": {
    "echo": "-2",
    "attenuation": "5",
    "area": "50",
    "signals": "6"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "120.0%",
    "超声波信号异常"
  ],
  "ref": "回波 −2≥−6 正常；底波衰减 5>4 异常 ⇒ 落「需复检」分支（!attenOk）；可疑信号面积比=6/max(50/10,1)×100=6/5×100=120.0%（独立复算）。默认 echo−6/衰减3/面积100/信号2 ⇒ 基本合格、面积比 20.0%，与本例两个锚点零交集。原 expect「可疑信号面积比」是该页 info-box 固定标签（注入失败同样命中）⇒ 已替换。material/adhesive 未被 calc() 读取（零影响键）⇒ 不注入。"
},
{
  "slug": "bonding/analysis-cost-4",
  "inputs": {
    "data": "环氧AB胶,4.0,5,0.6,96\n热熔胶,1.8,1.5,0.6,92\n结构胶带,6.0,2,0.6,99"
  },
  "expect": [
    "最优方案： 热熔胶",
    "节省： 59.75%",
    "单件成本 2.93"
  ],
  "ref": "单件成本=(材料+工时×费率)÷良品率：环氧AB胶(4.0+5×0.6)/0.96=7.29、热熔胶(1.8+1.5×0.6)/0.92=2.93、结构胶带(6.0+2×0.6)/0.99=7.27；最优=热熔胶，较基准节省=(7.29-2.93)/7.29=59.75%，有效工时5.21→1.63（提升68.70%）（独立复算；默认 环氧胶3.5/4/0.5/98、瞬干胶2.0/2/0.5/95 → 最优瞬干胶3.16，注入失败即不命中）"
},
{
  "slug": "bonding/analysis-resolution",
  "inputs": { "sym": "界面失效", "sub": "塑料", "temp": "130", "cure": "8", "surf": "仅清洗" },
  "expect": ["诊断现象： 界面失效", "风险等级： 高"],
  "ref": "重做为「粘接失效分析与排查」：sym/sub/temp/cure/surf 注入。独立复算：界面失效→2 条原因；sub=塑料/温度130>120/固化8<10/表面仅清洗 共 4 条预警→风险等级=高。默认 sym=开胶脱落、surf=未处理、temp=25、cure=30、sub=金属→风险=中，与本例「风险等级：高」零交集；诊断现象：界面失效 亦非默认首项（开胶脱落）。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== bonding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
