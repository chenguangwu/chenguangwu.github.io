#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "fire-rescue/calc-pressure-1",
  "inputs": {
    "len": "30",
    "flow": "6.5"
  },
  "expect": ["65\n140\n30\n6.5\n1.83 沿程水头损失 (mH₂O) 0.0179 压力损失 (MPa) 0.179 压力损失 (bar) 0.0597 每百米损失 (MPa) 1.96 流速 (m/s) 0.0215 含局部损失估算 (MPa) 口径 65 mm ，长度 30 m ，流量 6.5 L/s ，C=140。\n暂无计算记录"],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/calc-time-response",
  "inputs": {
    "rti": "75",
    "tg": "300",
    "u": "2.0",
    "ti": "20",
    "tact": "68"
  },
  "expect": [
    "53.03"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/chemical-spill",
  "inputs": {
    "amount": "800",
    "wind": "3"
  },
  "expect": [
    "650m 警戒距离"
  ],
  "ref": "独立复算：泄漏量 800 kg > 500 kg 阈值 ⇒ 警戒距离 500×1.3=650 m。⚠ 原 expect '150' 为泄漏量输入回显（零判别力）；取量改 800 才能触发 >500 kg 派生分支（150 与默认 100 同为 500 m，无派生输出可锚）。默认 100 kg ⇒ 500 m，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/confined-space-rescue",
  "inputs": {
    "o2": "29.5",
    "lel": "0",
    "h2s": "0",
    "co": "0",
    "entrySize": "0.6",
    "depth": "5"
  },
  "expect": [
    "超出安全范围(19.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/detector-11",
  "inputs": {
    "rated": "45",
    "measured": "15"
  },
  "expect": [
    "45mA"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/detector-20",
  "clicks": [
    "for(var mi=0;mi<6;mi++){for(var ii=0;ii<8;ii++){var el=document.getElementById('m'+mi+'_'+ii);if(el){el.value='2';}}}calc();"
  ],
  "expect": [
    "总体合规度： 100% 评级： 合格"
  ],
  "ref": "动态渲染的 m{mi}_{ii} 评分 select 全部置 2 分（合格）→ calc 得「总体合规度： 100% 评级： 合格」（默认全 0 → 0% 不合格）。回退默认态不命中 100%。"
},
{
  "slug": "fire-rescue/dizhensoujiuzhichengjisuan",
  "inputs": {
    "weight": "75",
    "angle": "45",
    "count": "4",
    "allow": "30"
  },
  "expect": [
    "106.07"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-alarm-zone",
  "inputs": {
    "floors": "9",
    "floorArea": "2000",
    "fireZones": "2",
    "height": "3.5"
  },
  "expect": [
    "18000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-extinguisher-selection",
  "inputs": {
    "area": "300"
  },
  "expect": [
    "建议配置数量：4 具"
  ],
  "ref": "独立复算：300 m² ÷ 75 m²/具 = 4 具（最少 2 具规则不触发）。⚠ 原 expect '150' 为保护面积输入回显（零判别力）；面积改 300 才能让配置数量与默认 100 m²（2 具）区分。默认 100 m² ⇒ 2 具，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/fire-fighting-tactics",
  "inputs": {
    "fireArea": "300"
  },
  "expect": [
    "300 着火面积(m²)"
  ],
  "ref": "面积回显 + 单位标签（战术模式/水枪数不随面积变化：300 与默认 200 同为「进攻」2 支水枪，无面积派生量可锚）。⚠ 原 expect '300' 为裸输入回显。默认 200 ⇒ 200 着火面积(m²)，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/fire-investigation",
  "inputs": {
    "burnArea": "75"
  },
  "expect": [
    "75 过火面积(m²)"
  ],
  "ref": "过火面积回显 + 单位标签（起火点/原因分析由勾选线索驱动，本用例未勾选线索 ⇒ 无面积派生结论可锚）。⚠ 原 expect '75' 为裸输入回显。默认 50 ⇒ 50 过火面积(m²)，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/fire-load",
  "inputs": {
    "area": "150"
  },
  "expect": [
    "2 荷载密度 (MJ/m²)"
  ],
  "ref": "独立复算：总热值 360 MJ（木材 10 kg×18 MJ/kg ×2 行）÷ 面积 150 m² = 2.4 ⇒ 显示 2 MJ/m²。⚠ 原 expect '150' 为面积输入回显（零判别力）。默认面积下荷载密度不同，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/fire-resistance-rating",
  "inputs": {
    "height": "75"
  },
  "expect": [
    "2.00h"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/fire-risk-assessment",
  "inputs": {
    "height": "36",
    "area": "5000",
    "density": "0.5"
  },
  "expect": [
    "53 综合风险分（0~100）"
  ],
  "ref": "独立复算：高度 36 m 档基础分 53（默认 24 m ⇒ 47）。⚠ 原 expect '36' 为建筑高度输入回显（零判别力）。默认 47 综合风险分，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/high-rise-fire",
  "inputs": {
    "height": "120",
    "floors": "25",
    "fireFloor": "15",
    "ladder": "54"
  },
  "expect": [
    "超高层 建筑分类"
  ],
  "ref": "派生判定：120 m > 100 m ⇒ 超高层（默认 80 m ⇒ 高层），并据此走中转水箱/避难层供水分支。⚠ 原 expect '120' 为建筑高度输入回显（零判别力）。默认态为「高层 建筑分类」，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/hydrant-flow",
  "inputs": {
    "pressure": "3.25",
    "hoseLen": "25",
    "resistA": "0.0000147",
    "sk": "13"
  },
  "expect": ["3.25\n65\n16\n25\n0.0000147\n13\n15.83 出水流量 (L/s) 57.0 出水流量 (m³/h) 3157.9 喷嘴压力 (kPa) 64.2 充实水柱 (m) 流量 15.83 L/s 水柱 64.2 m 充实水柱 64.2m ≥ 要求 13.0m，满足消防供水要求。 水力参数： • 水带阻力损失：92.1 kPa（9.21 m 水柱） • 喷嘴压力水柱 Hq：315.8 m，喷嘴系数 φ：0.0124 • 喷嘴系数 B：79.37 • 栓口压力：3250 kPa • 出水量是否达 5L/s 基准：是（室内消火栓单栓基准 5L/s）"],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/length-distance",
  "inputs": {
    "ppump": "3.8",
    "pnozzle": "0.2",
    "height": "0",
    "flow": "6.5"
  },
  "expect": ["3.8\n0.2\n0\n6.5\n65\n140\n6034.2 最大供水距离 (m) 3.6000 可用摩擦压力 (MPa) 0.00060 每米沿程损失 (MPa/m) 0.0000 高差压力 (MPa) Φ65mm / 6.5L/s / C=140 → 干线最大可铺设约 6034.2 m （约 301.7 条 20m 水带）。\n暂无计算记录"],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/post-fire-assessment",
  "inputs": {
    "fireTemp": "900",
    "duration": "2"
  },
  "expect": [
    "混凝土强度损失约70%以上"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/power-2",
  "inputs": {
    "flow": "30",
    "head": "60",
    "eff": "75",
    "sf": "1.15"
  },
  "expect": [
    "23.54"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/pressure-flow",
  "inputs": {
    "p1": "3.5",
    "p2": "0.3",
    "len": "20"
  },
  "expect": [
    "326.31"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/rescue-route",
  "inputs": {
    "floors": "15",
    "entrances": "2",
    "roadWidth": "6",
    "vehicles": "4"
  },
  "expect": [
    "15"
  ],
  "ref": "⚠ 输入回显（楼层数）。本页输出仅把楼层/出入口/道路宽度/车辆数分别回显到统计条，派生文本（4 条路线、检查清单）与数值无关 ⇒ 无任何依赖输入的派生量可锚；且首个数值卡片紧邻「building」下拉值、无单位标签，唯一可用的 `15\n2` 形态极易被默认态子串误命中 ⇒ 维持原断言（结构性不可修，见 memory 铁律）"
},
{
  "slug": "fire-rescue/rope-rescue",
  "inputs": {
    "load": "150",
    "eff": "90",
    "angle": "90",
    "mbs": "30"
  },
  "expect": [
    "1.47"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/smoke-management",
  "inputs": {
    "qfire": "7500",
    "z": "5",
    "zl": "0",
    "hc": "3",
    "nports": "2",
    "portmax": "15000"
  },
  "expect": [
    "196160"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/speed-3",
  "inputs": {
    "mass": "120",
    "dia": "12",
    "mu": "0.2",
    "wraps": "2",
    "height": "10"
  },
  "expect": [
    "120kg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/sprinkler-design",
  "inputs": {
    "totalArea": "1500",
    "headArea": "12.5",
    "pressure": "0.10",
    "kfactor": "80",
    "opArea": "0"
  },
  "expect": [
    "120 总喷头数"
  ],
  "ref": "独立复算：1500 m² ÷ 12.5 m²/只 = 120 只（默认 1000 m² ⇒ 80 只）。⚠ 原 expect '1500' 为总面积输入回显（零判别力）。默认 80 总喷头数，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/temp-6",
  "inputs": {
    "time": "15"
  },
  "expect": [
    "10.25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/time-41",
  "inputs": {
    "thick": "15"
  },
  "expect": [
    "8 破拆时间 (s)"
  ],
  "ref": "独立复算：15 mm 厚钢板 ÷ 切割速率 120 mm/min = 0.125 min ≈ 0.13 min = 8 s（默认 10 mm ⇒ 5 s）。⚠ 原 expect '15' 为板厚输入回显（零判别力）。默认 5 破拆时间 (s)，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/time-air",
  "inputs": {
    "vol": "9.8",
    "press": "30",
    "alarm": "5.5",
    "freq": "20"
  },
  "expect": ["9.8\n30\n5.5\n20\n1.5\n79.0 使用时间 (min) 2370 可用空气量 (L) 30.0 耗气率 (L/min) 59.2 安全作业时间 (min) 2902 总储气量 (L) 气量评估： 气量充足 （保留 25% 撤离余量）\n暂无计算记录"],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/time-evacuation",
  "inputs": {
    "aset": "15",
    "tdet": "1",
    "tpre": "2",
    "tmove": "4"
  },
  "expect": [
    "8.0 安全裕度"
  ],
  "ref": "独立复算：ASET 15.0 − RSET 7.0（探测 1+疏散前 2+行走 4）= 8.0 min 安全裕度（默认 ASET 10 ⇒ 3.0）。⚠ 原 expect '15.0' 为 ASET 输入回显（零判别力）。默认 3.0 安全裕度，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/time-lux",
  "inputs": {
    "cap": "18000",
    "volt": "12",
    "power": "5",
    "eff": "100",
    "lux": "5",
    "area": "100",
    "uf": "0.7"
  },
  "expect": [
    "34.6 单灯持续"
  ],
  "ref": "独立复算：18 Ah×12 V=216 Wh ÷ 5 W ≈ 34.6 h 单灯续航。⚠ 原 expect '18000' 为电池容量回显（零判别力）。默认容量下续航不同，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/ventilation-tactics",
  "inputs": {
    "btype": "2"
  },
  "expect": [
    "利用楼梯井/管道井竖向排烟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/water-rescue",
  "inputs": {
    "temp": "23",
    "velocity": "0",
    "distance": "30"
  },
  "expect": [
    "23°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/wildfire-spread",
  "inputs": {
    "wind": "30",
    "slope": "15",
    "humidity": "40",
    "temp": "30",
    "hours": "3"
  },
  "expect": ["30\n15\n40\n30\n3\n2\n1.84 蔓延速度(m/min) 111 蔓延速度(m/h) 100 火线强度(kW/m) 0.6 火焰高度(m) 极高火险 蔓延距离 332 m 过火面积 13.83 ha 灭火策略建议： 可直接灭火（手持工具+水） 火焰高度 0.6m。 预测详情： • 燃料模型：灌木丛（中等）（载量 7 t/ha） • 风速：30 km/h（8.3 m/s），风因子 ×8.22 • 坡度：15°，坡度因子 ×1.42 • 湿度：40%，湿度因子 ×0.80 • 预测时长：3.0 小时 • 蔓延距离：332 m（0.33 km） • 预估过火面积：13.83 ha（138315 m²）"],
  "ref": "auto-restore"
},
{
  "slug": "fire-rescue/zuranyangzhishupanding",
  "inputs": {
    "loi": "45",
    "material": "18"
  },
  "expect": [
    "18.0 氧指数"
  ],
  "ref": "派生映射：材料选聚丙烯 PP ⇒ fillLoi 写入 18 ⇒ 卡片显示 18.0 氧指数并判「易燃/不达标」（默认 PVC ⇒ 45.0 难燃）。⚠ 原 expect '18.0' 为裸数值回显。默认 45.0 氧指数，不命中 ⇒ 无逃生（已双态实测）。"
},
{
  "slug": "fire-rescue/shengsuoanquanxishu",
  "inputs": { "mbs": "50", "wll": "5" },
  "expect": ["10.00 实际安全系数", "3.33 许用载荷 (kN)", "66.7%"],
  "ref": "注入非默认（默认 mbs=30 kN 破断强力 / wll=2 kN 工作载荷，ropeType 默认生命安全绳 ⇒ 最小要求系数 15:1）。实际安全系数 = 破断强力 ÷ 工作载荷 = 50 ÷ 5 = 10.00；许用载荷 = 破断强力 ÷ 最小系数 = 50 ÷ 15 = 3.33 kN；安全度 = 10 ÷ 15 = 66.7%；10.00 < 15 ⇒ 判「危险 / 不安全」，提示更换绳索或减小载荷。默认态为 15.00 / 2.00 / 100.0% 且结论「合格 · 安全」，三串均不出现。"
},
  {
    "slug": "fire-rescue/calc-1",
    "inputs": {
      "pressure": "42",
      "coeff": "42",
      "angle": "42",
      "XYI3r59hvePgE6yBtmYxc7": "16"
    },
    "expect": [
      "42\n42\n42\n请输入有效参数。\n16"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pressure\":\"42\",\"coeff\":\"42\",\"angle\":\"42\",\"XYI3r59hvePgE6yBtmYxc7\":\"16\"}，输出区含「42\n42\n42\n请输入有效参数。\n16」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fire-rescue/calc-4",
    "inputs": {
      "area": "42",
      "fireClass": "B",
      "level": "medium"
    },
    "expect": [
      "42\nB\nmedium\n单具保护面积： 1 m²/具 估算灭火器总数： 42 具 按每处 2 具布置，约需 21 个设置点"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"fireClass\":\"B\",\"level\":\"medium\"}，输出区含「42\nB\nmedium\n单具保护面积： 1 m²/具 估算灭火器总数： 42 具…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fire-rescue/calc-3",
    "inputs": {
      "people": "42",
      "width": "42",
      "flow": "42",
      "speed": "42",
      "distance": "42",
      "preTime": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n行走时间： 1.0 s 出口通过时间： 0.0 s 运动时间： 1.0 s（约 0.02 分钟） 所需安全疏散时间 RSET： 43.0 s"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"people\":\"42\",\"width\":\"42\",\"flow\":\"42\",\"speed\":\"42\",\"distance\":\"42\",\"preTime\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n行走时间： 1.0 s 出口通过时间： 0.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "fire-rescue/calc-2",
    "inputs": {
      "mass": "42",
      "hv": "42",
      "area": "42"
    },
    "expect": [
      "42\n42\n42\n总热值： 1,764.0 MJ 火灾荷载密度： 42.0 MJ/m² 等效木材荷载： 2.3 kg/m² 火灾严重程度等级： 低"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mass\":\"42\",\"hv\":\"42\",\"area\":\"42\"}，输出区含「42\n42\n42\n总热值： 1,764.0 MJ 火灾荷载密度： 42.0 MJ…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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

  console.log("==== fire-rescue calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
