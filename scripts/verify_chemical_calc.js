#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chemical/calc-pipeline-pressure-drop",
  "inputs": {
    "v0": "300",
    "v1": "150",
    "v2": "2.0",
    "v3": "850",
    "v4": "0.0005",
    "v5": "0.1"
  },
  "expect": [
    "3.29 kPa",
    "1020000",
    "0.0039",
    "0.394 m"
  ],
  "ref": "独立复算：D=300mm=0.3m/L=150m/v=2/ρ=850/μ=0.0005/ε=0.1mm ⇒ Re=850×2×0.3÷0.0005=1020000（湍流，锚Re）；Haaland f=1/[−1.74·ln((0.1÷1000)/(3.7×0.3)+6.9÷1020000)]²≈0.0039（锚f）；ΔP=f×(150÷0.3)×(850×2²÷2)≈3287Pa=3.29kPa（锚kPa）；液柱=3287÷(850×9.81)≈0.394m（锚液柱，区别于水柱0.335m）。页面默认 200/100/1.5/1000/0.001/0.045 四锚均不命中，四值全依赖注入。"
},
{
  "slug": "chemical/convert-capacity-tank",
  "clicks": ["document.getElementById('type').value='vcyl';document.getElementById('mode').value='level';document.getElementById('d').value='6';document.getElementById('w').value='3';document.getElementById('L').value='12';document.getElementById('h').value='3';document.getElementById('Vt').value='314.159';calc();document.getElementById('__tbProbe').textContent=document.getElementById('res').innerHTML"],
  "expect": ["容积 V = 84.823 m³"],
  "ref": "立式圆柱 直径 6m、液位 3m → V=π·3²·3=84.823 m³（默认 d=10/h=4 → 314.159，注入态不重合；clicks 全量赋值避免同 slug 用例共享 DOM 时串态）"
},
{
  "slug": "chemical/convert-capacity-tank",
  "inputs": { "type": "vcyl", "mode": "level", "d": "8", "w": "3", "L": "10", "h": "3", "Vt": "150.796" },
  "clicks": ["calc();document.getElementById('__tbProbe').textContent=document.getElementById('res').innerHTML"],
  "expect": ["容积 V = 150.796 m³", "充装率 = 30.00%"],
  "ref": "682 批复核失败回归（存量逃生项收紧）：立式罐 d=8、L=10、液位 3 ⇒ V=π·4²·3=150.796，满罐 502.655，充装率 30.00%；旧用例注入值与页面默认 d=10/L=12/h=4 完全相同，默认态即命中 33.33%/942.478，判别器判逃生。现改为全非默认输入，默认态两锚均不命中。"
},
{
  "slug": "chemical/convert-capacity-tank",
  "clicks": ["document.getElementById('type').value='hcyl';document.getElementById('mode').value='volume';document.getElementById('d').value=2.4;document.getElementById('L').value=8;document.getElementById('Vt').value=18.0956;calc();document.getElementById('__tbProbe').textContent=document.getElementById('res').innerHTML"],
  "expect": ["18.096 m³", "液位 1.200 m"],
  "ref": "卧式罐反算：d=2.4、L=8 满罐 36.191，目标 18.0956（半满）⇒ 液位 1.200m、充装率 50.00%；旧版无卧式与反算，必失败"
},
{
  "slug": "chemical/convert-capacity-tank",
  "clicks": ["document.getElementById('type').value='vcyl';document.getElementById('mode').value='level';document.getElementById('d').value='10';document.getElementById('w').value='3';document.getElementById('L').value='12';document.getElementById('h').value='13';document.getElementById('Vt').value='314.159';calc();document.getElementById('__tbProbe').textContent=document.getElementById('res').innerHTML"],
  "expect": ["液位须在 0~12.00 m 之间"],
  "ref": "液位 13m 超过罐高 12m 须拦截，不得算出 1021 m³ 的超过满罐容积结果（682 批）"
},
{
  "slug": "chemical/convert-capacity-tank",
  "inputs": { "Vt": "0", "d": "2.4", "L": "8", "w": "3", "mode": "volume" },
  "clicks": [
    "var out=[];['vcyl','hcyl','box'].forEach(function(t){document.getElementById('type').value=t;calc();var h=String(document.getElementById('res').innerHTML);out.push(h.indexOf('液位 0.000 m')>=0&&h.indexOf('充装率 = 0.00%')>=0?'Y':'N');});document.getElementById('__tbProbe').textContent='VT0 '+out.join('');"
  ],
  "expect": ["VT0 YYY"],
  "ref": "682 批复核失败回归：目标容积 0 表示空罐，应反算液位 0、充装率 0%；旧条件 `!(Vt>0)` 与提示「0~满罐」自相矛盾，三种罐型都被拦截。注入 Vt=0（默认 314.159）并逐型断言，探针串只在新口径出现。"
},
{
"slug": "chemical/convert-density-crude",
"inputs": {
"val": "30",
"unit": "api"
},
"expect": [
"876.2 kg/m³"
],
"ref": "复算：SG = 141.5 ÷ (30+131.5) = 0.87616 → ρ = 876.2 kg/m³（每桶 139.30 kg，判中质原油）；默认 API=35 得 849.8 ⇒ 不命中"
},
{
  "slug": "chemical/detector-39",
  "inputs": {
    "conc": "0.2",
    "vol": "20.00",
    "mass": "0.2500",
    "molar": "180.00",
    "ratio": "2",
    "threshold": "95.0",
    "g_mass": "0.6000",
    "g_dry": "0.5700",
    "g_factor": "1.050",
    "g_threshold": "97.0"
  },
  "expect": [
    "99.75",
    "≥97%"
  ],
  "ref": "去默认化（原 expect「纯度」是静态标签词）：harness 末次调用为 calcG（重量法页签），纯度 = m2×F/m1×100 = 0.57×1.05/0.6×100 = 99.75% ≥ 97 ⇒ 合格、判定行显示「≥97%」。默认 0.485×1/0.5 得 97.00%、阈值 98%，两串均不命中。注：本页滴定法页签的 conc/vol/mass/molar 不影响最终 res（被 calcG 覆盖），故须改 g_* 四键"
},
{
  "slug": "chemical/miaomu-guige-zhiliang-yanshou-biaozhun",
  "inputs": {
    "v0": "200",
    "v1": "180",
    "v2": "165"
  },
  "expect": [
    "90.0%",
    "82.5%",
    "86.3"
  ],
  "ref": "独立复算：抽检200/合格180/规格符合165 ⇒ 合格率=180÷200=90.0%（锚1）、规格符合率=165÷200=82.5%（锚2）、综合得分=(90+82.5)×0.5=86.25→86.3（锚3）。页面默认 100/92/88 得 92.0%/88.0%/90.0% 三锚均不命中，全依赖注入；原用例缺 ref 说明判别依据，补齐。"
},
{
  "slug": "chemical/mixture-ratio",
  "inputs": {
    "ca": "60",
    "ma": "200",
    "cb": "30",
    "mb": "100",
    "c1": "95",
    "v1": "500",
    "c2": "70",
    "value": "25",
    "al1": "95",
    "al2": "40"
  },
  "expect": [
    "混合浓度 50.00%",
    "混合比 (A:B) 200 : 100"
  ],
  "ref": "去默认化（原 expect「混合比」是静态标签词，默认态同样命中 = 逃生项）：A 60%×200 + B 30%×100，总质量 300 ⇒ 混合浓度 (12000+3000)/300 = 50.00%；混合比 200 : 100。默认 80/100/20/300 得 35.00% 与 100 : 300（v1 只影响「稀释」页签，不影响本结果，故须改 ca/ma/cb/mb）"
},
{
  "slug": "chemical/mixture-ratio",
  "clicks": ["cur='alcohol';renderModes();renderParams();document.getElementById('al1').value=60;document.getElementById('v1').value=500;document.getElementById('al2').value=40;calc();document.getElementById('__tbProbe').textContent=document.getElementById('result').innerHTML"],
  "expect": ["500mL 60° 酒", "250mL 水"],
  "ref": "酒精稀释结果句跟随输入酒精度（681，N213）：60vol% 500mL → 40vol%，v2=750mL、加水 250mL；修复前结果句硬编码「500mL 95° 酒」，与输入 60° 不符（默认 95° 会命中旧串，故必须改 al1=60）"
},
{
  "slug": "chemical/reaction-yield",
  "inputs": {
    "theo": "25",
    "actual": "21.25",
    "na": "0.5",
    "nb": "0.3",
    "ratio": "1",
    "m": "10",
    "m1": "100",
    "m2": "80",
    "coef": "1",
    "small": "5",
    "times": "10",
    "yield": "80",
    "big": "75"
  },
  "expect": [
    "85.00%",
    "3.75 g"
  ],
  "ref": "去默认化（原 expect「损失量」是卡片标签，与输入无关）：默认页签 cur=yield，产率 = 21.25/25×100 = 85.00%（70≤x<90 ⇒ 🟢 优秀），损失量 = 25−21.25 = 3.75 g。默认 7.5/10 得 75.00% 与 2.50 g，注入失败即不命中"
},
{
  "slug": "chemical/reaction-yield",
  "clicks": ["cur='scale';renderModes();renderParams();calc()"],
  "inputs": {
    "small": "5",
    "times": "10",
    "yield": "90",
    "big": "80"
  },
  "expect": ["55.6 g", "44.4 g"],
  "ref": "新增回归：小试 5 g、收率 90% ⇒ 小试理论量 5/0.9=5.556 g，放大 10 倍 = 55.6 g；放大收率 80% ⇒ 预计 44.4 g。旧实现直接用 5×10=50 g，会把理论量低估 10%"
},
{
  "slug": "chemical/solution-concentration",
  "inputs": {
    "mass": "90",
    "molar": "45",
    "vol": "0.5",
    "solute": "10",
    "total": "100",
    "mg": "5",
    "kg": "1",
    "c1": "2",
    "v1": "100",
    "c2": "0.5"
  },
  "expect": [
    "4.0000 mol/L",
    "180.00 g/L"
  ],
  "ref": "去默认化（原 expect「质量浓度」是卡片标签）：默认页签=摩尔浓度，n = 90/45 = 2.0000 mol，C = 2.0000/0.5 = 4.0000 mol/L，质量浓度 = 90/0.5 = 180.00 g/L。默认 58.5/58.5/1 得 1.0000 mol/L 与 58.50 g/L，注入失败即不命中（注意：若只改 mass 与 vol 成比例，C 与质量浓度会与默认重合，必须打破比例）"
},
{
  "slug": "chemical/solution-concentration",
  "inputs": {
    "mg": "20",
    "kg": "2"
  },
  "clicks": ["cur='ppm';renderParams();calc()"],
  "expect": [
    "10 ppm",
    "10,000 ppb",
    "0.0010%"
  ],
  "ref": "ppm 换算修正：ppm = 溶质(mg) ÷ 溶液(kg) = 20/2 = 10（原实现多乘 1000 会得 10,000）；ppb = 10×1000 = 10,000；百分比 = 10/10000 = 0.0010%。默认页签为摩尔浓度、默认输入 5 mg/1 kg ⇒ 默认态不含这三串，注入或切页签失败即不命中。"
},
{
  "slug": "chemical/analysis-cost-7",
  "inputs": {
    "data": "11,22,33,44,55",
    "budget": "100",
    "topn": "2"
  },
  "expect": [
    "55.00",
    "60.00%",
    "超支 65.00"
  ],
  "ref": "非默认输入+独立复算：合计165、最大分项55、前2大项累计占比60.00%、对比预算100超支65（默认数据 800,200,1200,300,500,150 均不含 55.00/60.00%/超支65.00，注入失败即不命中）"
},
{
  "slug": "chemical/checker-15",
  "inputs": {
    "m0_0": "2",
    "m0_1": "2",
    "m0_2": "2",
    "m0_3": "1",
    "m0_4": "0",
    "m1_0": "2",
    "m1_1": "2",
    "m1_2": "2",
    "m1_3": "1",
    "m1_4": "1",
    "m1_5": "0",
    "m2_0": "2",
    "m2_1": "2",
    "m2_2": "2",
    "m2_3": "2",
    "m2_4": "1"
  },
  "expect": [
    "75%",
    "7/10",
    "8/12"
  ],
  "ref": "去默认化（原 expect「0/10」＝全零默认态即命中）：16 个 select 由 innerHTML 模板按 m{mi}_{ii} 生成，id 为确定值可注入。一、标准管理 2+2+2+1+0=7/10（70%），二、过程检查 2+2+2+1+1+0=8/12（67%），三、整改闭环 2+2+2+2+1=9/10（90%）；总分 24/32 ⇒ 合规度 round(75%)=75%（良好）。默认全 0 ⇒ 0% / 0-10 / 0-12，三串均不命中。注：id 不在静态 HTML 字面量里，discriminate_check 取不到默认值会「跳过」，已用同口径探针补验「注入 PASS + 回退全 0 FAIL」"
},
{
  "slug": "chemical/molar-mass",
  "inputs": {
    "formula": "H2O",
    "mass": "27"
  },
  "expect": [
    "9.025e+23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chemical/convert-density-crude",
  "inputs": {
    "val": "0",
    "unit": "rho"
  },
  "expect": [
    "相对密度 SG 与密度 ρ 需填写大于 0 的数值"
  ],
  "ref": "新增回归：密度 0 曾被兜底成 0.0001 → API 1414868.5°。现应提示并拒绝计算；默认 API 35 不出现该提示"
},
{
  "slug": "chemical/calc-pipeline-pressure-drop",
  "inputs": {
    "v0": "200",
    "v1": "100",
    "v2": "1.5",
    "v3": "800",
    "v4": "0.001",
    "v5": "0.045"
  },
  "expect": [
    "0.174 m",
    "0.218 m"
  ],
  "ref": "新增回归：ρ=800 时 ΔP=1.71 kPa，折合水柱（ρ 固定 1000）= 1710÷9810 = 0.174 m，折合液柱（当前 ρ）= 1710÷(800×9.81) = 0.218 m；旧实现只给 ÷(ρ×9.81) 却标成水柱（0.218 m），与水柱口径差 25%"
},
{
  "slug": "chemical/convert-capacity-tank",
  "inputs": { "type": "box", "d": "", "w": "3", "h": "4" },
  "expect": ["请填写长、宽、罐高（米）后再计算。"],
  "ref": "空态守卫（2026-11-05，2026-11-16 第 682 批改文案）：长方体模式清空任一边长后不再输出「容积 V = 0.000 m³」与「每米液深容积」，只给填写提示；罐高改由 L 字段承担（h 仍为液位），故提示统一为「罐高」。⚠ 判空只认空串——0 边长为合法输入，仍按公式算 0。"
},
{
  "slug": "chemical/molar-mass",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/' +'tools/chemical/molar-mass.html','utf8');var h=globalThis.__tbFs.readFileSync(process.cwd()+'/'+'tools/chemical/molar-mass.html','utf8');var i=h.indexOf(\"if (!formula)\");var s=i>=0?h.slice(i,i+620):'';var ok=(s.match(/getElementById\\('result'\\).innerHTML=''/g)||[]).length>=2&&s.indexOf('\u672a\u77e5\u5143\u7d20')>=0;document.getElementById('__tbProbe').textContent='MOLCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["MOLCLR OK"],
  "ref": "第1345批 molar-mass 三早退(空式/未知元素/molar<=0)原只 showToast，不清 #result(元素组成明细表)；改为三处同步清空。"
}
,
{
  "slug": "chemical/solution-concentration",
  "inputs": {
    "mass": "0"
  },
  "expect": [
    "请填写大于 0 的质量"
  ],
  "ref": "质量=0 时清空摩尔浓度卡（SOLCLR）；旧实现仅 toast，1.0000 mol/L 旧值残留"
},
{
  "slug": "chemical/mixture-ratio",
  "inputs": {
    "ma": "0"
  },
  "expect": [
    "请填写大于 0 的两组分质量"
  ],
  "ref": "质量=0 时清空混合浓度/配比（MIXCLR）；旧实现仅 toast，35.00%/400 残留"
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

  console.log("==== chemical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
