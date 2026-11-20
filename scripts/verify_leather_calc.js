#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "leather/area-20",
  "inputs": {
    "thickness": "5.5",
    "area": "18"
  },
  "expect": [ "5.50 厚度" ],
  "ref": "auto-restore"
},
{
  "slug": "leather/area-20",
  "inputs": {
    "thickness": "2.5",
    "area": "22"
  },
  "expect": [ "面积22ft² → 头层中皮" ],
  "ref": "面积分级统一为 ft²（680，N210）：22 ft² 落在 15~25 → **中皮**（公式框原写 2.04m² 判「大张」）；厚度 2.5 为头层 → 综合「头层中皮」。默认 18 ft² 也是中皮、「中皮/头层中皮」撞默认态；改锚含面积的整串「面积22ft² → 头层中皮」（历史行带面积，默认 18ft² 不含）。"
},
{
  "slug": "leather/area-20",
  "inputs": {
    "thickness": "",
    "area": "18"
  },
  "expect": [ "请填写有效的厚度与面积" ],
  "ref": "空厚度停算（680，N211）：原 `num('')=0` 仍输出「二层薄皮/碎皮/二层碎皮」并写历史；现厚度为空即标红、清空结果并中止（默认 2.5 合法，不含该提示）。"
},
{
  "slug": "leather/area-20",
  "inputs": {
    "thickness": "-1",
    "area": "18"
  },
  "expect": [ "请填写有效的厚度与面积" ],
  "ref": "负厚度停算（680，N211）：厚度 -1 原按 <0.8 判「二层薄皮」；现须 >0，标红并中止（默认合法）。"
},
{
  "slug": "leather/assessor-21",
  "inputs": {
    "thickness": "5",
    "penetration": "1.6",
    "uniformity": "8",
    "fastness": "4"
  },
  "expect": [
    "32.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/calc-dosage-4",
  "inputs": {
    "weight": "200",
    "lr": "1.5",
    "conc": "12"
  },
  "expect": [
    "300.0 液量 (L)",
    "36.00 硫化钠用量 (kg)",
    "18.00% 占皮重比例"
  ],
  "ref": "液量=皮重×液比=200×1.5=300.0 L；硫化钠用量=液量×浓度%=300×12%=36.00 kg；占皮重=36/200=18.00%。原用例浓度 60% 超页面 0–20% 上限，仅触发校验提示，期望 180.00 恒不成立；已改为合法且三值均偏离默认（默认 100/2.0/3）的输入。"
},
{
  "slug": "leather/calc-dosage-4",
  "inputs": {
    "weight": "250",
    "lr": "1.8",
    "conc": "5"
  },
  "expect": [
    "450.0 液量 (L)",
    "22.50 硫化钠用量 (kg)",
    "9.00% 占皮重比例"
  ],
  "ref": "新增回归：默认 100 kg 皮、液比 2.0、浓度 3% ⇒ 液量 200 L、硫化钠 6.00 kg（占皮重 6%）。旧默认浓度 60% 会得 120.00 kg，约为皮重的 120%"
},
{
  "slug": "leather/colorfast",
  "inputs": {
    "hours": "30",
    "irr": "42"
  },
  "expect": [
    "4536.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/concentration-6",
  "inputs": {
    "weight": "150",
    "lr": "1.0",
    "ph": "3.0",
    "salt": "8"
  },
  "expect": [ "150.0 液量" ],
  "ref": "auto-restore"
},
{
  "slug": "leather/convert-area-weight",
  "inputs": {
    "w": "150",
    "a": "0.5"
  },
  "expect": [
    "300.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/convert-area-weight",
  "inputs": {
    "w": "250",
    "a": "0.4"
  },
  "expect": [
    "2.0482 oz/ft²"
  ],
  "ref": "面密度 250/0.4 = 625 g/m² ⇒ oz/ft² = 625/305.1517 = 2.0482（旧系数 30.5153 会得 20.4814，放大 10 倍）。仅锚盎司项：g/ft²/ g/yd² 修复前后同为 58.064/522.58，若并入 expect 会因 OR 语义让旧版照样通过。默认 100/0.5 = 200 g/m² 得 0.6554 oz/ft²，与本值不重合"
},
{
  "slug": "leather/paoguangliangdupinggu",
  "inputs": {
    "rpm": "1200",
    "press": "0.3",
    "times": "3"
  },
  "expect": [
    "100.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/strength-8",
  "inputs": {
    "w": "15",
    "thk": "2",
    "load": "200",
    "tear": "40"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/temp-9",
  "inputs": {
    "l0": "75",
    "l1": "45",
    "ts": "95"
  },
  "expect": [
    "40.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/time-34",
  "inputs": {
    "thk": "6",
    "act": "5000",
    "temp": "38"
  },
  "expect": [
    "61"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/time-concentration",
  "inputs": {
    "conc": "18",
    "hours": "16",
    "weight": "100"
  },
  "expect": [
    "23.04%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/tushicenghoudu",
  "inputs": {
    "b1": "120",
    "b2": "35",
    "m1": "120",
    "m2": "25",
    "t1": "50",
    "t2": "15",
    "dens": "1.2"
  },
  "expect": [ "66.3 总厚度" ],
  "ref": "auto-restore"
},
{
  "slug": "leather/xueyunhoudukongzhi",
  "inputs": {
    "before": "2.0",
    "target": "1.2",
    "rpm": "4000",
    "feed": "8"
  },
  "expect": [ "2.00 刀痕间距 (mm/rev)", "0.80 切除量 (mm)", "70 一般 · 匹配评分" ],
  "ref": "运动学重写：间距 = 1000×8÷4000 = 2.00 mm/rev；切除量 = 2.0−1.2 = 0.80mm；间距 ≤2 档 ⇒ 70 分「一般」。默认态（2.0/1.5/1200/8）间距 6.67、切除 0.50、30 分，三处均不命中。旧实现仅 min(100,rpm/feed×10)，输出 100，与本例不符。"
},
{
  "slug": "leather/yield-rate-1",
  "inputs": {
    "c0": "3000",
    "vol": "500",
    "c1": "300"
  },
  "expect": [
    "90.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/yield-rate-1",
  "inputs": {"c0":"0","vol":"500","c1":"300"},
  "clicks": ["calc();var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='YIELDC0 '+(h.indexOf('废液铬浓度须大于 0')>=0&&h.indexOf('0.00%')<0?'OK':'BAD '+h.slice(0,80));"],
  "expect": ["YIELDC0 OK"],
  "ref": "N189 c0=0 守卫：旧版仅 setInvalid 标红仍算 rate=0「较差」并写历史；修复后早退提示「废液铬浓度须大于 0」且不出 0.00%。默认 c0=3000 合法不命中，零逃生。"
},
{
  "slug": "leather/yield-rate",
  "inputs": {
    "c0": "7500",
    "c1": "800",
    "weight": "100",
    "lr": "2.0"
  },
  "expect": [
    "89.33%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/colorfast",
  "clicks": ["document.getElementById('hours').value='0';calc();var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='CF186 '+(h.indexOf('照射时间与辐照度均须大于 0')>=0&&h.indexOf('1 级')<0?'OK':'BAD '+h.slice(0,80))"],
  "expect": ["CF186 OK"],
  "ref": "12-N186：旧 calc 只用 setInvalid 画红框，无 return，清空/0/负值仍照算 energy=0 → 「1 级 很差，极易褪色」并写历史。修复后 h>0&&ir>0 守卫 + lastResult 清空 + 中英提示。本用例注入 hours=0，要求提示存在且不含 1 级；默认 20h/42W → 7 级，注入失败不命中 ⇒ 零逃生。评级模型方向（N184）属专业口径，本例不触碰。"
},
{
  "slug": "leather/assessor-21",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/leather/assessor-21.html','utf8');var js=h.slice(h.indexOf('function calc(){'),h.indexOf('function copyReport()'));var d=JSON.parse(globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['leather/assessor-21'];var ok=js.indexOf('QB/T 4672')<0&&JSON.stringify(d).indexOf('QB/T 4672')<0&&h.indexOf('上述分级仅为自定义示例')>=0&&h.indexOf('染色质量符合标准')<0;document.getElementById('__tbProbe').textContent='DYEGRADE '+(ok?'OK':'BAD');"],
  "expect": ["DYEGRADE OK"],
  "ref": "12-N223/N229：公式框原承诺「综合得分=穿透率40%+均匀度30%+色牢度30%」及 A/B/C 分档，代码与深解实际走三项同时满足阈值；改为与实现一致的优等/一等/合格门槛。算例穿透率 60% 未达一等品 70%，改判合格品；英译源同步。旧版旧综合得分串与旧算例命中 ⇒ 变红；默认态不产生该哨兵，零逃生。"
},{
  "slug": "leather/colorfast",
    clicks: ["document.getElementById('hours').value='30';document.getElementById('irr').value='42';calc();var t=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='CFREFBAR '+(t.indexOf('4536.0')>=0&&t.indexOf('8 级')<0?'OK':'BAD');"],
  "expect": ["CFREFBAR OK"],
  "ref": "12-N185：calc 对 energy≥4800 输出「8 级」，但参考标尺 bands 最后一档为 7 级 hi:null，同屏出现 7/8 级两个结论。现 7 级改 hi:4800 并补 8 级档（lo:4800,hi:null），与 calc 输出范围对齐；不改评级方向与阈值（N184 方向倒置仍待专业裁断）。源码形态哨兵旧版必红。"
} ,
{
  "slug": "leather/calc-dosage-4",
  "clicks": ["var c=document.getElementById('conc'),l=document.getElementById('lr'),r=document.getElementById('res');c.value='10';l.value='1';calc();var a=r.innerHTML.indexOf('超过 10%')<0&&r.innerHTML.indexOf('超过皮重的 10%')<0;c.value='11';l.value='2';calc();var b=r.innerHTML.indexOf('浓度超过 10%')>=0&&r.innerHTML.indexOf('超过皮重的 10%')>=0&&lastResult.indexOf('超过皮重的 10%')>=0;document.getElementById('__tbProbe').textContent='LEATHERWARN '+(a&&b?'OK':'BAD');"],
  "expect": ["LEATHERWARN OK"],
  "ref": "浓度及占皮重均在严格大于 10% 时提示并随复制结果保留，10% 不触发。"
},
{ slug:"leather/assessor-21", inputs:{"thickness":"","penetration":"","uniformity":"","fastness":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" }
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

  console.log("==== leather calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
