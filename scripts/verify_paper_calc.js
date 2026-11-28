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
function strengthStaticChecks() {
  const s9 = fs.readFileSync(path.join(__dirname, "..", "tools", "paper", "strength-9.html"), "utf8");
  const s1 = fs.readFileSync(path.join(__dirname, "..", "tools", "paper", "strength-1.html"), "utf8");
  const conc = fs.readFileSync(path.join(__dirname, "..", "tools", "paper", "calc-concentration-1.html"), "utf8");
  const moist = fs.readFileSync(path.join(__dirname, "..", "tools", "paper", "moisture-calc.html"), "utf8");
  const naipo = fs.readFileSync(path.join(__dirname, "..", "tools", "paper", "naipo-dingpo-zhishu.html"), "utf8");
  const det = fs.readFileSync(path.join(__dirname, "..", "tools", "paper", "detector-17.html"), "utf8");
  return [
    { name: "纸浆浓度校验绝干率/体积/目标并声明纤维守恒", ok: /__concValid/.test(conc) && /dryPct>100/.test(conc) && /vol<=0/.test(conc) && /target<=0\|\|target>100/.test(conc) && /绝干纤维守恒/.test(conc) },
    { name: "水分阈值改为参考区间且复制复用校验", ok: /__moistureValid/.test(moist) && /文化用纸常见参考区间/.test(moist) && /不是所有纸种的标准限值/.test(moist) && /validateMoisture\(\)/.test(moist.slice(moist.indexOf('function copyResult'), moist.indexOf('var refData'))) },
    { name: "耐破移除跨量纲互换并统一标签与校验", ok: !/swapValues|互换 A\/B|评分 A|评分 B/.test(naipo) && /__naipoValid/.test(naipo) && /耐破度须大于 0/.test(naipo) && /纸样定量须大于 0/.test(naipo) && /不是标准限值/.test(naipo) },
    { name: "纸病改为参考阈值、严格校验并禁止无效复制", ok: !/GB\/T|15442|不合格品|合格品/.test(det) && /__detValid/.test(det) && /__dNum/.test(det) && /单项超出参考阈值/.test(det) && /不能为负/.test(det) && /area<=0/.test(det) && /非国家标准合格判定/.test(det) && /__detValid\)\{ToolBox\.showToast/.test(det) },
    { name: "撕裂页移除跨量纲互换与固定1.5倍结论", ok: !/1\.5|swapValues|互换 A\/B/.test(s9) && /撕裂力（实测，mN）/.test(s9) && /纸样定量（g\/m²）/.test(s9) },
    { name: "纸箱抗压区分计算与堆码有效性并保存ECT模式", ok: /baseValid/.test(s1) && /stackValid/.test(s1) && /ectMode/.test(s1) && /ectDirect/.test(s1) && /未保存 ECT 输入模式/.test(s1) },
  ];
}
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
  clicks: ["calc()"],
  "slug": "paper/detector-17",
  "inputs": {
    "defSize": "5.5",
    "defPerSqm": "8",
    "area": "10"
  },
  "expect": [ "参考阈值" ],
  "ref": "纸病结果改为参考阈值口径"
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
  clicks: ["calc()"],
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
    "24.00"
  ],
  "ref": "v0=180,v1=75 → 剥离强度=180×1000/75=2400.0 N/m、2.4000 kN/m、每厘米 24.00 N/cm；参考基准留空，不再输出 1.0 kN/m 富余度（默认 100/50 → 2000.0/2.0000/20.00）"
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
  clicks: ["calc()"],
  "slug": "paper/roll-length",
  "inputs": { "targetLen": "500", "coreDia2": "-76", "paperThk2": "0.1" },
  "expect": ["纸芯外径不能留空，且需为 ≥0 的数值"],
  "ref": "12-K6：负纸芯内径旧实现仍算 D=263.5 mm、壁厚 169.8 mm、层数 1698；现在拒绝。默认纸芯 76 合法不出现该文案。"
},
{
  clicks: ["calc()"],
  "slug": "paper/roll-length",
  "inputs": { "targetLen": "600", "coreDia2": "100", "paperThk2": "0.15" },
  "expect": ["353.0 mm"],
  "ref": "12-K6 回归（避开默认 500/76/0.1）：D=√(4×0.15×600000/π+100²)=√124591.56=353.0 mm。"
},
{
  clicks: ["calc()"],
  "slug": "paper/roll-length",
  "inputs": { "outerDia": "100", "coreDia": "-10", "paperThk": "0.1" },
  "expect": ["纸芯外径需≥0"],
  "ref": "12-K6 续：calcLen 旧实现只校验 D>d 与 t>0，负纸芯照样算出长度；现拒绝并提示纸芯内径 ≥0。"
},
{
  clicks: ["calc()"],
  "slug": "paper/roll-length",
  "inputs": { "outerDia": "100", "coreDia": "99.5", "paperThk": "1" },
  "expect": ["无法形成有效缠绕层数"],
  "ref": "外径与纸芯差 0.5 mm、纸厚 1 mm ⇒ 层数 round(0.25)=0，旧实现再算 lengthM/layers 得 Infinity（显示破折号）；现在层数 <1 时直接拒绝。"
},
{ slug:"paper/detector-17", inputs:{"defSize":"","defPerSqm":"","area":""}, expect:["请完整填写最大缺陷尺寸"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{
  "slug": "paper/roll-length",
  "clicks": ["document.getElementById('outerDia').value='200';document.getElementById('coreDia').value='';document.getElementById('paperThk').value='0.1';calcLen();document.getElementById('__tbProbe').textContent=document.getElementById('lenResult').innerText;"],
  "expect": ["纸芯外径不能留空"],
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
{
  "slug": "paper/strength-9",
  "clicks": ["document.getElementById('v0').value='-5';document.getElementById('v1').value='60';calc();document.getElementById('__tbProbe').textContent=document.getElementById('res').innerText;"],
  "expect": ["撕裂力不能为负"],
  "ref": "负撕裂力不得得到负指数；旧实现仍可计算。"
},
{
  "slug": "paper/strength-1",
  "inputs": {"sf":"0"},
  "expect": ["堆码参数不完整", "最大堆码层数"],
  "ref": "安全系数为 0 时仍可给出 ECT/BCT，但不得给出安全载荷与堆码结论，也不得保存历史。"
},
{
  "slug": "paper/strength-1",
  "inputs": {"boxWt":"0"},
  "expect": ["堆码参数不完整"],
  "ref": "箱重为 0 时不得显示最大堆码层数 1 的假安全结论。"
},
{
  "slug": "paper/calc-concentration-1",
  "inputs": {"dry":"120"},
  "expect": ["0–100%"],
  "ref": "绝干率超过 100% 必须拒绝，不得算出比湿浆还重的绝干纤维。"
},
{
  "slug": "paper/calc-concentration-1",
  "inputs": {"vol":"0"},
  "expect": ["体积若填写须>0"],
  "ref": "体积填 0 不得静默按 0 跳过体积浓度。"
},
{
  "slug": "paper/moisture-calc",
  "inputs": {"wetWeight":"","dryWeight":"92"},
  "expect": ["请填写有效的湿重与绝干重"],
  "ref": "湿重留空不得按 0 计算。"
},
{
  "slug": "paper/moisture-calc",
  "inputs": {"wetWeight":"90","dryWeight":"95"},
  "expect": ["干重不应大于湿重"],
  "ref": "干重大于湿重时不得输出负含水率。"
},
{
  "slug": "paper/naipo-dingpo-zhishu",
  "inputs": {"v0":"0","v1":"60"},
  "expect": ["耐破度须大于 0"],
  "ref": "耐破度 0 不得得到 0 指数与 -100% 偏差的伪结果。"
},
{
  "slug": "paper/naipo-dingpo-zhishu",
  "inputs": {"v0":"250","v1":"0"},
  "expect": ["分母，不能为 0"],
  "ref": "定量 0 不得触发除零（通用分母守卫）。"
},


{
  clicks: ["calc()"],
  "slug": "paper/detector-17",
  "inputs": {"defSize":"2.5","defPerSqm":"8","area":"10"},
  "expect": ["两项均超出参考阈值"],
  "ref": "尺寸与密度均超阈值时提示两项均超出，不再写不合格品。"
},
{
  clicks: ["calc()"],
  "slug": "paper/detector-17",
  "inputs": {"defSize":"5","defPerSqm":"3","area":"10"},
  "expect": ["单项超出参考阈值"],
  "ref": "仅尺寸超阈值时不得判为参考优等/参考一等。"
},

{
  clicks: ["calc()"],
  "slug": "paper/roll-length",
  "inputs": {"outerDia":"1000","coreDia":"100","paperThk":"0.1"},
  "expect": ["7775442"],
  "ref": "纸芯外径 100mm：π×(1000²−100²)/(4×0.1)≈7775442 mm；旧 76mm 内径为 7808621，不同。"
},
{
  "slug": "paper/strength-10",
  "inputs": {"v0":"180","v1":"75","v2":"1.2"},
  "expect": ["100.00%","参考基准由你填写"],
  "ref": "自填 1.2 kN/m：(2.4/1.2−1)×100=100.00%，且明确为用户自填、非通用标准。"
},
{
  "slug": "paper/strength-10",
  "inputs": {"v0":"-5","v1":"50"},
  "expect": ["剥离力」须不小于 0"],
  "ref": "负剥离力必须拒绝，不再算出负强度。"
},
{
  "slug": "paper/basis-weight",
  "clicks": ["document.getElementById('knownReamKg').value='12.5';calcReverseGsm();document.getElementById('reamSize').value='a4';document.getElementById('reamSize').dispatchEvent(new Event('change',{bubbles:true}));document.getElementById('__tbProbe').textContent=document.getElementById('reverseResult').innerText;"],
  "expect": ["g/m²"],
  "ref": "反算后切换规格，反算区必须自动重算（A4 面积变化，结果不再是 29.09）。"
},
{
  "slug": "paper/carbon-5",
  "inputs": {"v0":"800","v1":"-10","v2":"70"},
  "expect": ["加填率」须不小于 0"],
  "ref": "负加填率必须拒绝，不再得到 -80kg 的伪结果。"
},
{
  "slug": "paper/strength-1",
  "inputs": {"rctFace":"","rctLiner":"4000","rctMed":"2500"},
  "expect": ["估算模式须完整填写三项环压值"],
  "ref": "估算模式清空面纸环压不得再按 0 计算，必须提示补填或改用直接 ECT。"
},
{
  "slug": "paper/strength-1",
  "inputs": {"rctFace":"","rctLiner":"","rctMed":"","ectDirect":"7000"},
  "expect": ["直接输入 7000"],
  "ref": "直接 ECT 模式完全忽略三项环压；环压留空仍可算 BCT。"
},
{
  clicks: ["calc()"],
  "slug": "paper/detector-17",
  "inputs": {"defState":"measured","defSize":"2.5","defPerSqm":"0","area":"10"},
  "expect": ["相互矛盾"],
  "ref": "尺寸>0 而密度=0 必须拒绝，不生成等级。"
},
{
  clicks: ["calc()"],
  "slug": "paper/detector-17",
  "inputs": {"defState":"none","defSize":"0","defPerSqm":"0","area":"10"},
  "expect": ["不生成参考等级","未检出"],
  "ref": "未检出明确记录 0/0，只说明未检出，不生成等级。"
},
{
  clicks: ["calc()"],
  "slug": "paper/detector-17",
  "inputs": {"defState":"unknown","defSize":"0","defPerSqm":"12","area":"10"},
  "expect": ["尺寸未知","不生成参考等级"],
  "ref": "尺寸未知只输出估计缺陷数，不硬凑 0 尺寸等级。"
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

  const stat = rollLengthStaticChecks().concat(paperGradeStaticChecks()).concat(strengthStaticChecks());
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== paper calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
