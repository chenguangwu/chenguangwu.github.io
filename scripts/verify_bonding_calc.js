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
    "12.0",
    "读数提示（示意）",
    "信号密度(个/100cm²)"
  ],
  "ref": "第1109批：6 个信号 / 50 cm² ⇒ 信号密度 12.0 个/100cm²；页面不再由信号数换算面积比，也不判不合格。旧实现 6/max(50/10,1)×100=120% 并直接判「不合格」，现只给读数提示与复检建议。"
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
  "slug": "bonding/assessor-cycle-lifespan",
  "inputs": { "sigmaB": "900", "deltaSigma": "300", "sigmaM": "150", "kt": "1.5", "designN": "0", "surface": "0.8" },
  "expect": ["设计循环次数按万次输入，不能为 0"],
  "ref": "designN=0 旧版 N/0=Infinity 仍判安全；新增 >0 校验后直接阻断。"
},
{
  "slug": "bonding/assessor-cycle-lifespan",
  "inputs": { "sigmaB": "600", "deltaSigma": "200", "sigmaM": "600", "kt": "2", "designN": "100", "surface": "0.8" },
  "expect": ["平均应力 σm 必须小于抗拉强度"],
  "ref": "σm=σb 时 Goodman 分母为 0，旧版会得到 Infinity 或无效值；新增 σm<σb 校验。"
},
{
  "slug": "bonding/detector-26",
  "inputs": { "designT": "0.3", "tolerance": "10", "measures": "-0.1,0.3,0.2", "defect": "0" },
  "expect": ["第 1 个测点“-0.1”须为大于 0", "旧结论已清除"],
  "ref": "第1109批：逐项校验不再静默丢点；负测点直接指出第 1 个测点并清空旧结论。"
},
{
  "slug": "bonding/analysis-cost-4",
  "inputs": { "data": "<b>坏</b>,4,5,0.6,96\n正常,1,1,0.6,100" },
  "expect": ["&lt;b&gt;坏&lt;/b&gt;", "单件成本 1.60"],
  "ref": "方案名含 HTML 必须转义输出，不能在本页执行标签；正常行 (1+0.6)/1=1.60 元。"
},
{
  "slug": "bonding/analysis-cost-4",
  "inputs": { "data": "坏行,4,5,0.6,120\n正常,1,1,0.6,100" },
  "expect": ["输入有误，未进行比较", "良品率须在 (0,100]"],
  "ref": "第1109批：良品率 120% 不再跳过单行后继续比较；整批输入有误即阻止比较，并标出原始行与字段。"
},
{
  "slug": "bonding/analysis-resolution",
  "inputs": { "sym": "界面失效", "sub": "塑料", "temp": "130", "cure": "8", "surf": "仅清洗" },
  "clicks": ["document.getElementById('sym').value='界面失效';document.getElementById('sub').value='塑料';document.getElementById('temp').value='130';document.getElementById('cure').value='8';document.getElementById('surf').value='仅清洗';calc();"],
  "expect": ["诊断现象： 界面失效", "已配置条件提示： 4 条"],
  "ref": "第1109批：界面失效 + 塑料 + 130℃ + 8min + 仅清洗命中 4 条已配置条件；页面不再叫「风险等级/高」，只显示条件提示 4 条，并声明不代表故障严重程度。"
},
{
  "slug": "bonding/analysis-resolution",
  "clicks": ["var cu=document.getElementById('cure'),te=document.getElementById('temp'),r=document.getElementById('res');cu.value='0';calc();var z=/固化时间须大于 0/.test(r.innerHTML);cu.value='-5';calc();var neg=/固化时间须大于 0/.test(r.innerHTML);cu.value='30';te.value='-300';calc();var tz=/温度须高于绝对零度/.test(r.innerHTML);te.value='25';cu.value='30';calc();var ok=/诊断现象/.test(r.innerHTML)&&/已配置条件提示/.test(r.innerHTML);document.getElementById('__tbProbe').textContent=(z&&neg&&tz&&ok)?'__BOND_G9_OK__':'__BOND_G9_BAD__ '+[z,neg,tz,ok].join(',');"],
  "expect": ["__BOND_G9_OK__"],
  "ref": "第1099批 G9：固化=0 或负曾被 `cure>0&&cure<10` 放过、表面已打磨时判「低风险」；现改为 cure<=0 直接拦截报错，温度低于绝对零度亦拦截，合法值正常诊断。旧版三哨兵全红。"
},
  {
    "slug": "bonding/detector-27",
    "inputs": { "echo":"-6","attenuation":"3","area":"100","signals":"2","defectArea":"20" },
    "expect": ["信号密度(个/100cm²)", "2.0", "缺陷面积比（含重叠重复计数）20.0%"],
    "ref": "第1109批：单独填有效缺陷面积 20/100 ⇒ 20.0% 面积比；信号密度仍为 2/100×100=2.0，两个指标分开显示，不把信号数当面积。"
  },
  {
    "slug": "bonding/detector-27",
    "inputs": { "echo":"-6","attenuation":"3","area":"100","signals":"2","defectArea":"200" },
    "expect": ["有效缺陷面积须在 0 与检测面积之间", "不保留旧结论"],
    "ref": "第1109批：缺陷面积 200>100 直接拒绝，避免面积比>100% 的无效读数；旧表清空。"
  },
  {
    "slug": "bonding/detector-26",
    "inputs": { "designT":"0.2","tolerance":"20","measures":"0.2mm,abc,0.3","defect":"0" },
    "expect": ["第 1 个测点“0.2mm”不是有效数字", "第 2 个测点“abc”不是有效数字", "未保留旧结论"],
    "ref": "第1109批：尾缀与字母不再被静默丢弃，逐项指出位置与原始内容并清空旧结论/表格/图表。"
  },
  {
    "slug": "bonding/analysis-cost-4",
    "inputs": { "data":"A,3元,5,0.6,96\nB,1.8,1.5,0.6,92" },
    "expect": ["第1行", "胶水成本“3元”", "未进行比较"],
    "ref": "第1109批：字段带“元”尾缀即整批阻止，指出原始行和字段，不再跳过坏行给出最优方案。"
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

  console.log("==== bonding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
