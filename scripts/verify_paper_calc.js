#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
const path = require("path");
const ROLL_PATH = path.join(__dirname, "..", "tools", "paper", "roll-length.html");

// 581 复核失败：calcLen() 有有效层数守卫，copyResult() 却只查三个参数；
// 复制与计算必须共用同一判据，否则页面提示无法成卷时仍可复制出虚假长度。
function rollLengthStaticChecks() {
  const src = fs.readFileSync(ROLL_PATH, "utf8");
  const body = (name) => {
    const i = src.indexOf("function " + name + "(");
    if (i < 0) return "";
    const j = src.indexOf("\nfunction ", i + 1);
    return src.slice(i, j < 0 ? src.length : j);
  };
  const calc = body("calcLen");
  const copy = body("copyResult");
  const calcGuard = /var layers = Math\.round\(\(D - d\) \/ \(2 \* t\)\)/.test(calc)
    && /layers < 1/.test(calc);
  const copyGuard = /Math\.round\(\(D - d\) \/ \(2 \* t\)\) < 1/.test(copy);
  return [
    {
      name: "纸卷长度计算与复制共用有效层数守卫",
      ok: calcGuard && copyGuard && /无法形成有效缠绕层数/.test(copy),
    },
  ];
}

const GRADE_PATH = path.join(__dirname, "..", "tools", "paper", "paper-grade.html");
function paperGradeStaticChecks() {
  const src = fs.readFileSync(GRADE_PATH, "utf8");
  const filter = src.slice(src.indexOf("function filterTable()"), src.indexOf("</script>", src.indexOf("function filterTable()")));
  const exp = src.slice(src.indexOf("window.__pgExport=function()"), src.indexOf("function __pgFillTabs", src.indexOf("window.__pgExport=function()")));
  return [
    { name: "纸种搜索纳入分类标题并处理空态", ok: /catMatch/.test(filter) && /g\.name/.test(filter) && /pgEmpty/.test(filter) && /cat\.style\.display/.test(filter) },
    { name: "导出改为带指标名和单位的长表", ok: /Paper type/.test(exp) && /Metric/.test(exp) && /Unit/.test(exp) && /Coating deviation/.test(exp) && /Cross-direction fold/.test(exp) && /Bursting strength/.test(exp) },
  ];
}

const CASES = [
{
  "slug": "paper/basis-weight",
  "inputs": {
    "gsmInput": "120",
    "reamGsm": "70"
  },
  "expect": [ "120.0 g/m²" ],
  "ref": "auto-restore"
},
{
  "slug": "paper/detector-17",
  "inputs": {
    "defSize": "5.5",
    "defPerSqm": "8",
    "area": "10"
  },
  "expect": [ "15442 最大缺陷尺寸：5.5" ],
  "ref": "auto-restore"
},
{
  "slug": "paper/moisture-calc",
  "inputs": {
    "wetWeight": "150",
    "dryWeight": "92"
  },
  "expect": [
    "38.67%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/pulp-yield",
  "inputs": {
    "rawInput": "1500",
    "pulpInput": "480"
  },
  "expect": [
    "0.3200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/roll-length",
  "inputs": {
    "outerDia": "1500",
    "coreDia": "76",
    "paperThk": "0.1",
    "targetLen": "500",
    "coreDia2": "76",
    "paperThk2": "0.1"
  },
  "expect": [
    "17626094"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/calc-concentration-1",
  "inputs": {
    "wet": "750",
    "dry": "20",
    "vol": "480",
    "target": "3"
  },
  "expect": [
    "4250.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/carbon-5",
  "inputs": {
    "v0": "1000",
    "v1": "20"
  },
  "expect": [
    "12.28%",
    "0.1400",
    "16.67%"
  ],
  "ref": "v0=1000,v1=20 → 成纸灰分=0.7×20/(100+0.7×20)×100=12.28%、填料纤维比 0.7×20/100=0.1400、加入量占比 200/1200=16.67%（默认 800/15 → 9.50%/0.1050/13.04%；swap 84.85%/5.6000/90.91%，均不重合；第 1/2 行 200.00/140.00 为对称量，不作 expect）"
},
{
  "slug": "paper/naipo-dingpo-zhishu",
  "inputs": {
    "v0": "350",
    "v1": "80"
  },
  "expect": [
    "4.375",
    "3.57",
    "45.83%"
  ],
  "ref": "v0=350,v1=80 → 耐破指数=350/80=4.375 kPa·m²/g、换算 350×0.0102=3.57 kgf/cm²、相对 3.0 基准 (4.375-3)/3×100=45.83%（默认 250/60 → 4.167/2.55/38.89%；swap 0.240/0.61/-92.00%，均不重合）"
},
{
  "slug": "paper/strength-1",
  "inputs": {
    "rctFace": "6000",
    "rctLiner": "4000",
    "rctMed": "2500",
    "d": "3.6",
    "eff": "0.5",
    "ectDirect": "",
    "L": "400",
    "W": "300",
    "H": "300",
    "sf": "3",
    "boxWt": "15"
  },
  "expect": [
    "(6000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/strength-10",
  "inputs": {
    "v0": "180",
    "v1": "75"
  },
  "expect": [
    "2400.0",
    "2.4000",
    "140.00%"
  ],
  "ref": "v0=180,v1=75 → 剥离强度=180×1000/75=2400.0 N/m、2.4000 kN/m、相对 1.0 kN/m 富余 (2.4-1)×100=140.00%（默认 100/50 → 2000.0/2.0000/100.00%；swap 500.0/0.5000/-50.00%，均不重合）"
},
{
  "slug": "paper/strength-9",
  "inputs": {
    "v0": "750",
    "v1": "80"
  },
  "expect": [
    "9.375",
    "937.5",
    "17.19%"
  ],
  "ref": "v0=750,v1=80 → 撕裂指数=750/80=9.375 mN·m²/g、每 100 g/m² 归一化 937.5 mN、相对 8.0 基准 (9.375-8)/8×100=17.19%（默认 500/60 → 8.333/833.3/4.17%；swap 0.120/12.0/-98.50%，均不重合）"
},
{
  "slug": "paper/roll-length",
  "inputs": { "targetLen": "500", "coreDia2": "-76", "paperThk2": "0.1" },
  "expect": ["纸芯内径不能留空，且需为 ≥0 的数值"],
  "ref": "12-K6：负纸芯内径旧实现仍算 D=263.5 mm、壁厚 169.8 mm、层数 1698；现在拒绝。默认纸芯 76 合法不出现该文案。"
},
{
  "slug": "paper/roll-length",
  "inputs": { "targetLen": "600", "coreDia2": "100", "paperThk2": "0.15" },
  "expect": ["353.0 mm"],
  "ref": "12-K6 回归（避开默认 500/76/0.1）：D=√(4×0.15×600000/π+100²)=√124591.56=353.0 mm。"
},
{
  "slug": "paper/roll-length",
  "inputs": { "outerDia": "100", "coreDia": "-10", "paperThk": "0.1" },
  "expect": ["纸芯内径需≥0"],
  "ref": "12-K6 续：calcLen 旧实现只校验 D>d 与 t>0，负纸芯照样算出长度；现拒绝并提示纸芯内径 ≥0。"
},
{
  "slug": "paper/roll-length",
  "inputs": { "outerDia": "100", "coreDia": "99.5", "paperThk": "1" },
  "expect": ["无法形成有效缠绕层数"],
  "ref": "外径与纸芯差 0.5 mm、纸厚 1 mm ⇒ 层数 round(0.25)=0，旧实现再算 lengthM/layers 得 Infinity（显示破折号）；现在层数 <1 时直接拒绝。"
},
{ slug:"paper/detector-17", inputs:{"defSize":"","defPerSqm":"","area":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{
  "slug": "paper/roll-length",
  "clicks": ["document.getElementById('outerDia').value='200';document.getElementById('coreDia').value='';document.getElementById('paperThk').value='0.1';calcLen();document.getElementById('__tbProbe').textContent=document.getElementById('lenResult').innerText;"],
  "expect": ["纸芯内径不能留空"],
  "ref": "清空纸芯不得按 0 计算；必须明确输入 0 才允许无缝纸芯。"
},
{
  "slug": "paper/pulp-yield",
  "clicks": ["document.getElementById('rawInput').value='1000';document.getElementById('pulpInput').value='';calc();document.getElementById('__tbProbe').textContent=document.getElementById('result').innerText;"],
  "expect": ["必须是有限数值"],
  "ref": "纸浆重量留空不得按 0 输出 0% 得率。"
},
{
  "slug": "paper/pulp-yield",
  "clicks": ["document.getElementById('rawInput').value='1000';document.getElementById('pulpInput').value='-50';calc();document.getElementById('__tbProbe').textContent=document.getElementById('result').innerText;"],
  "expect": ["纸浆重量不能为负"],
  "ref": "负纸浆重量不得得到负得率。"
},
{
  "slug": "paper/pulp-yield",
  "clicks": ["document.getElementById('rawInput').value='1000';document.getElementById('pulpInput').value='480';calc();document.getElementById('__tbProbe').textContent=document.getElementById('result').innerText;"],
  "expect": ["中低得率区间（40–60%）","不能单独判定浆种"],
  "ref": "48% 只给得率区间，不再宣称是化学浆。"
},
{
  "slug": "paper/basis-weight",
  "clicks": ["document.getElementById('knownReamKg').value='12.5';calcReverseGsm();document.getElementById('__tbProbe').textContent=document.getElementById('reverseResult').innerText;"],
  "expect": ["29.09 g/m²"],
  "ref": "787×1092mm、500 张/令，12.5kg 反算 12.5×1000/(0.787×1.092×500)=29.09 g/m²。"
},
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

  const stat = rollLengthStaticChecks().concat(paperGradeStaticChecks());
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== paper calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
