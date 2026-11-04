#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "welding/analysis-37",
  "inputs": {
    "data": "气孔,45\n夹渣,20\n未焊透,15\n裂纹,8\n咬边,6\n其他,6"
  },
  "expect": [
    "缺陷总数： 100",
    "A 类（主要缺陷）： 3 项",
    "累计占比 80.00%"
  ],
  "ref": "总数100；累计占比45.00/65.00/80.00 ≤80% 共3项为A类"
},
{
  "slug": "welding/analysis-38",
  "inputs": { "cur": "220", "volt": "26", "spd": "5", "pre": "25", "eff": "0.8" },
  "expect": [
    "热输入： 915.20",
    "t8/5 冷却时间： 4.75",
    "平均冷却速率： 63.18"
  ],
  "ref": "Q=0.8×26×220/5=915.20 J/mm；t8/5=915.20/(2π×0.025)×(1/475−1/775)=4.75 s；速率 300/4.75=63.18 °C/s（默认 180/24/4/20 → 864.00/4.41/68.07，避开）"
},
{
  "slug": "welding/calc-1",
  "inputs": {
    "diameter": "6.2",
    "thickness": "8",
    "voltage": "24",
    "speed": "3"
  },
  "expect": ["6.2\n8\nflat\nbasic\n24\n3\n186 ~ 279 推荐电流范围（A） 233 推荐电流（A） 111.84 热输入 E（kJ/mm） 6.2 mm / 8 mm 焊条/板厚 焊接位置：平焊，焊条类型：低氢型"],
  "ref": "auto-restore"
},
{
  "slug": "welding/detector-25",
  "inputs": {
    "plateThick": "36",
    "circDef": "3",
    "stripDef": "8",
    "evalArea": "500"
  },
  "expect": [
    "22.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/detector-25",
  "inputs": {
    "ndtMethod": "rt",
    "weldType": "fillet",
    "plateThick": "24",
    "circDef": "3",
    "stripDef": "8",
    "evalArea": "500"
  },
  "expect": [
    "角焊缝通常不宜采用射线检测"
  ],
  "ref": "角焊缝 + RT 应给出适用性提示（NB/T 47013 的 RT 评定针对对接接头）；默认 butt+rt 不含该串 ⇒ 可判别。原代码 weldType 仅回显、不参与条件分支（死控件）。"
},
{
  "slug": "welding/energy-cost-1",
  "inputs": {
    "current": "300",
    "voltage": "24",
    "time": "30",
    "price": "1.0",
    "duty": "60",
    "eff": "85"
  },
  "expect": [
    "2.541"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/flow-ratio",
  "inputs": {
    "nozzle": "18",
    "flow": "20",
    "ar": "80",
    "co2": "20"
  },
  "expect": [
    "16.0 Ar 流量 (L/min) 4.0 CO₂ 流量 (L/min)"
  ],
  "ref": "按混合气配比拆分总流量：总流量 20 L/min、Ar 80% / CO₂ 20% ⇒ Ar 16.0 L/min、CO₂ 4.0 L/min（页面口径由百分比反算，非输入回显）。总流量必须偏离默认 15 L/min——否则分项串与默认态同值，会成为逃生项。旧期望 0.98 已随页面改版失效。"
},
{
  "slug": "welding/hancaixuanyongtuijian",
  "inputs": {
    "thickness": "12"
  },
  "expect": [
    "136"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/hanjiegongzhuangjiajusheji",
  "inputs": {
    "length": "1500",
    "width": "500",
    "weight": "50"
  },
  "expect": [
    "147.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/hanjiezidonghuapinggu",
  "inputs": {
    "output": "15000",
    "seamlen": "0.5",
    "mansec": "120",
    "labor": "50",
    "robotcost": "30",
    "workdays": "250"
  },
  "expect": [ "7500 年焊缝总长" ],
  "ref": "auto-restore"
},
{
  "slug": "welding/hanjiezidonghuapinggu",
  "inputs": {
    "output": "5000",
    "seamlen": "2",
    "mansec": "600",
    "labor": "60",
    "robotcost": "30",
    "workdays": "250"
  },
  "expect": [ "32000", "9.4" ],
  "ref": "算例低产量支路：人工 5000×600/3600×60=50,000 元；机器人 5000×240/3600×60×0.6+6,000=18,000 元；节省 32,000 元；回收期 300,000/32,000=9.4 年 ⇒ 评级≥5 年「需谨慎评估」。expect 只锚 32000/9.4 两个派生量：默认态（10000 件）回收期 45.0 年同样含「需谨慎评估」，带上该评级串会变成逃生项。"
},
{
  "slug": "welding/speed-voltage-current",
  "inputs": {
    "thickness": "9"
  },
  "expect": [
    "23.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/stress",
  "inputs": {
    "thickness": "15",
    "length": "300",
    "leg": "6",
    "yield": "235"
  },
  "expect": [
    "0.46°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/temp-10",
  "inputs": {
    "thickness": "18",
    "preheat": "100"
  },
  "expect": [
    "18"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "welding/temp-time-6",
  "inputs": {
    "thickness": "30",
    "ce": "0.45",
    "c": "0.18",
    "mn": "1.4",
    "cr": "0.1",
    "mo": "0"
  },
  "expect": [
    "130"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/temp-time-6",
  "inputs": {
    "thickness": "30",
    "ce": "0.45",
    "c": "0.22",
    "mn": "1.6",
    "cr": "0.35",
    "mo": "0.15"
  },
  "expect": ["0.587 简化式 CEV（不含 Ni/Cu）"],
  "ref": "页面元素估算仅取 C/Mn/Cr/Mo（简化式，不含 Ni/Cu）：0.22+1.6/6+(0.35+0.15)/5=0.587。旧标签「IIW 公式计算 CEV」会让人误以为已含 Ni/Cu 项，故收紧为简化式标签；默认元素 0.18/1.4/0.1/0 得 0.433，不命中。"
},
{
  "slug": "welding/calc-1",
  "inputs": {
    "diameter": "5",
    "thickness": "8",
    "voltage": "0",
    "speed": "3"
  },
  "expect": ["— 热输入 E（kJ/mm）"],
  "ref": "U=0 时线能量无法估算：旧代码直接 toFixed 输出 0.00 kJ/mm（伪值）；改为显示「—」，且推荐电流仍随直径 5 mm 输出。默认直径 3.2/U=24/v=3 得 111.84，不命中。"
},
{
  "slug": "welding/ventilation-protection",
  "inputs": {
    "consume": "5",
    "volume": "500",
    "hours": "8"
  },
  "expect": [
    "20000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/wps-hanjiegongyiguichengbianzhi",
  "inputs": {
    "diameter": "4.2",
    "current": "200",
    "voltage": "24",
    "speed": "30",
    "preheat": "20",
    "pass": "2"
  },
  "expect": [
    "4.2mm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "welding/weld-strength",
  "inputs": { "F": "50", "hf": "6", "lw": "200", "fvw": "160" },
  "checkIds": ["deduct"],
  "expect": ["188.0", "63.32", "39.6%"],
  "ref": "真机默认勾选「扣除两端弧坑」⇒ L_eff=200−2×6=188.0mm、A_e=0.7×6×188=789.6→790mm²、τ=50000/789.6=63.32MPa、利用率=63.32/160=39.6%（若未开扣除则为 200/840/59.52，用来验证开关默认态）"
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

  console.log("==== welding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
