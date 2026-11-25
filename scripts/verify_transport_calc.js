#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "transport/calc-4",
  "inputs": {},
  "clicks": ["toggle(0,true);toggle(13,true);calc()"],
  "expect": [
    "¥300 累计罚款",
    "10 累计记分",
    "2 距12分剩余"
  ],
  "ref": "违法项 checkbox 由 renderList() 拼 innerHTML 生成（静态无 id ⇒ clicks 调 toggle(idx,true) 后 calc()）：勾 0 不按规定会车（¥100/扣1）与 13 高速公路违法占用快车道（¥200/扣9）⇒ 累计 ¥300、记分 10、距 12 分剩 2（默认未勾 ⇒ 仅提示「请勾选违法行为后再计算。」）。非默认输入+独立复算。"
},
{
  "slug": "transport/calc-53",
  "inputs": {
    "q1": "480",
    "q2": "380",
    "q3": "410",
    "q4": "350",
    "hourly": "120,80,50,40,60,180,450,780,820,700,650,720,760,690,640,720,820,950,1050,880,620,400,260,160"
  },
  "expect": [
    "480"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "transport/calculator-calc-3",
  "inputs": {
    "hours": "7",
    "minutes": "30",
    "firstHour": "10",
    "afterHour": "5",
    "dailyCap": "60"
  },
  "expect": [
    "42.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-depreciation",
  "inputs": {
    "cost": "300000",
    "life": "5",
    "salvageRate": "5"
  },
  "expect": [ "300,000 购车原值" ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-fuel",
  "inputs": {
    "distance": "750",
    "consumption": "7.5",
    "price": "8.00"
  },
  "expect": [ "450.00 总油费" ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-speed",
  "inputs": {
    "speed": "180",
    "reaction": "0.75",
    "slope": "0"
  },
  "expect": [
    "169.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-speed",
  "inputs": { "speed": "120", "reaction": "", "slope": "0" },
  "expect": ["请填写反应时间（≥0 s"],
  "ref": "反应时间留空不再按 0 计算；0 合法但必须显式填写。"
},
{
  "slug": "transport/calculator-calc-speed",
  "inputs": { "speed": "120", "reaction": "0", "slope": "0" },
  "expect": ["0.0 反应距离 (m)", "理论距离参考"],
  "ref": "反应时间 0 为合法输入：反应距离 0.0m，仍输出理论距离，但不再给出“安全”结论。"
},
{
  "slug": "transport/calculator-calc-speed",
  "inputs": { "speed": "120", "reaction": "1", "slope": "-80" },
  "expect": ["制动距离无解"],
  "ref": "μ=0.75、坡度 −80% 使分母 ≤0；停止计算并提示，不再输出 Infinity。"
},
{
  "slug": "transport/calculator-calc-tire",
  "inputs": {
    "oldSpec": "225/45R17_X",
    "newSpec": "225/50R17"
  },
  "expect": [ "请使用如 225" ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-tire",
  "inputs": { "oldSpec": "000/00R00", "newSpec": "225/50R17" },
  "expect": ["尺寸超出合理范围"],
  "ref": "全零规格不再通过格式校验；胎宽/扁平比/轮辋须在合理区间。"
},
{
  "slug": "transport/calculator-calc-tire",
  "inputs": { "oldSpec": "500/45R17", "newSpec": "225/50R17" },
  "expect": ["尺寸超出合理范围"],
  "ref": "胎宽 500mm 超出 50–400 合理范围，阻断计算并清空旧表。"
},
{
  "slug": "transport/convert-fuel-oil",
  "inputs": {
    "val": "45"
  },
  "expect": [
    "5.23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/convert-fuel-oil",
  "inputs": { "val": "30", "from": "mpg", "to": "mpg" },
  "expect": ["30.00 MPG"],
  "ref": "同单位换算不得取倒数：from=to=mpg、输入 30 时大字结果应为 30.00 MPG；旧实现无条件先算 r=235.2146/v 并据此输出，得到 7.84 MPG。默认 to=l100、val=45 ⇒ 5.23，不含 30.00 MPG。"
},
{
  "slug": "transport/convert-fuel-oil",
  "inputs": { "val": "12.34", "from": "l100", "to": "l100" },
  "expect": ["12.34 L/100km"],
  "ref": "同单位换算：from=to=l100、输入 12.34 时结果应为 12.34 L/100km；旧实现输出 235.2146/12.34=19.06 L/100km（倒数）。原输入 7.84 撞页面静态换算表（默认态也含「7.84 L/100km」）；改唯一值 12.34 ⇒ 默认态不含，零逃生。"
},
{
  "slug": "transport/convert-fuel-oil",
  "inputs": { "val": "30", "gal": "uk", "from": "mpg", "to": "l100" },
  "expect": ["9.42 L/100km"],
  "ref": "英制加仑（683 批）：30 MPG(UK) → 282.4809/30 = 9.4160 ≈ 9.42 L/100km；旧版无 gal 选项且恒用 235.2146（得 7.84），默认美制也含 7.84 ⇒ 必须切 UK 才命中 9.42"
},
{
  "slug": "transport/convert-volume-weight",
  "inputs": {
    "l": "60",
    "w": "30",
    "h": "20"
  },
  "expect": [
    "60×30×20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/convert-volume-weight",
  "clicks": [
    "document.getElementById('l').value='50';document.getElementById('w').value='40';document.getElementById('h').value='30';document.getElementById('d').value='5000';document.getElementById('actual').value='8';calc();var a=String(document.getElementById('res').innerHTML);var okHeavy=a.indexOf('计费重量 12.00 kg')>=0&&a.indexOf('取体积重')>=0;document.getElementById('actual').value='20';calc();var b=String(document.getElementById('res').innerHTML);var okActual=b.indexOf('计费重量 20.00 kg')>=0&&b.indexOf('取实际重量')>=0;document.getElementById('__tbProbe').textContent='CVW1288 '+(okHeavy&&okActual?'OK':'BAD');"
  ],
  "expect": ["CVW1288 OK"],
  "ref": "12-K11 补全计费重量功能：标题/meta/引据表承诺「实重 vs 体积重取大者」但旧页面无实重输入、只输出体积重。50×40×30÷5000=12 kg，实重 8<12 ⇒ 计费重 12.00 kg「取体积重」；实重 20>12 ⇒ 计费重 20.00 kg「取实际重量」。旧版无 actual 输入（getElementById 返回 null 报错/无计费重输出）⇒ 红；默认 actual 留空不产计费重串，注入失败零逃生。"
},
{
  "slug": "transport/convert-volume-weight",
  "inputs": { "l": "50", "w": "40", "h": "30", "d": "5000", "actual": "" },
  "expect": ["未填写实际重量：仅输出体积重"],
  "ref": "实重留空明确标注未提供，不再静默跳过比较。"
},
{
  "slug": "transport/convert-volume-weight",
  "inputs": { "l": "50", "w": "40", "h": "30", "d": "5000", "actual": "0" },
  "expect": ["计费重量 12.00 kg", "取体积重"],
  "ref": "实重 0 为合法值并参与比较：体积重 12kg > 0 ⇒ 计费 12.00kg 取体积重。"
},
{
  "slug": "transport/convert-volume-weight",
  "inputs": { "l": "50", "w": "40", "h": "30", "d": "5000", "actual": "-5" },
  "expect": ["实际重量不得为负"],
  "ref": "负实重明确报错，不再当作未填写而跳过比较。"
},
{
  "slug": "transport/cycle-signal",
  "inputs": {
    "cycle": "90",
    "satFlow": "1800",
    "phaseCount": "2"
  },
  "expect": [
    "流量比之和 Y 0.700",
    "相位饱和度 x 0.787"
  ],
  "ref": "Y=0.35+0.35=0.700，L=10，C=90；相位饱和度 x=Y×C/(C−L)=0.7×90/80=0.7875，toFixed(3) 得 0.787，页面单独显示“0.700 流量比之和 Y”“0.788 相位饱和度 x”。旧实现直接显示 Y=0.700 为饱和度。"
},
{
  "slug": "transport/cycle-signal",
  "inputs": { "cycle": "90", "satFlow": "1800", "phaseCount": "3" },
  "expect": ["流量比之和 Y 须在 0–1 之间"],
  "ref": "三相位默认 y 各 0.35 ⇒ Y=1.05≥1 过饱和，Webster 无解；停止输出方案并提示。"
},
{
  "slug": "transport/cycle-signal",
  "inputs": { "cycle": "10", "satFlow": "1800", "phaseCount": "2" },
  "expect": ["周期须大于总损失时间"],
  "ref": "C=10、L=10 ⇒ 有效绿灯 0，停止输出。"
},
{
  "slug": "transport/estimate-capacity",
  "inputs": {
    "laneW": "3.5",
    "shoulder": "3.0",
    "speed": "120",
    "heavy": "10",
    "volume": "1800",
    "phf": "0.92"
  },
  "expect": [
    "1,684",
    "1,431",
    "1.26"
  ],
  "ref": "lw3.5 ⇒ f_w=0.85+(3.5−3.0)×0.25=0.975；S=1900×0.975×1×(1/1.1)=1684；C=round(1684×0.85)=1431；V/C=1800/1431=1.258≈1.26。旧 f_w=1+(3.5−3.6)/2=0.95 ⇒ S=1641/C=1395，可判别。"
},
{
  "slug": "transport/estimate-energy",
  "inputs": {
    "capacity": "90",
    "consumption": "20",
    "soc": "80"
  },
  "expect": ["450 满电续航 (km) 360 当前可行驶 (km) 20.0 实际能耗", "冬季续航较标准下降约 23%"],
  "ref": "长期用例：90kWh、20kWh/100km、SOC80、标准模式 ⇒ 满电450、当前360、实际能耗20.0；冬季×1.3 ⇒ 346km、降23%。新增续航影响因素提示不影响核心数值。"
},
{
  "slug": "transport/estimate-energy",
  "inputs": { "capacity": "60", "consumption": "15", "soc": "" },
  "expect": ["请填写剩余电量 0–100%"],
  "ref": "剩余电量留空不再按 0 计算；空电须显式填 0。"
},
{
  "slug": "transport/estimate-energy",
  "inputs": { "capacity": "60", "consumption": "15", "soc": "120" },
  "expect": ["请填写剩余电量 0–100%"],
  "ref": "SOC 120% 越界拒绝估算，不再静默钳制到 100%。"
},
{
  "slug": "transport/estimate-speed-time",
  "inputs": {
    "distance": "600",
    "speed": "100",
    "restCount": "2",
    "restMin": "20",
    "depart": "08:00"
  },
  "expect": [
    "6小时40分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/noise",
  "inputs": {
    "volume": "3000",
    "speed": "80",
    "heavy": "8",
    "distance": "30"
  },
  "expect": [
    "(3000)"
  ],
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

  console.log("==== transport calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
