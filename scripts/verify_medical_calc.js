#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "medical/assessor-risk-3",
  "inputs": {
    "ph": "9",
    "water": "1500",
    "protein": "1.2",
    "sodium": "3000",
    "oxalate": "150"
  },
  "expect": [
    "4/20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calc-34",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30"
  },
  "expect": [
    "1898"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "weight": "30",
    "age": ""
  },
  "expect": ["375.0 mg 单次剂量", "1.80 g 有效最大日剂量（取较小值）"],
  "ref": "auto-restore（D-N5 后同步：年龄空值按成人口径，且有效上限取 min(成人绝对上限, 儿童按体重上限)，原「儿童最大日剂量」标签改为「有效最大日剂量（取较小值）」；30 kg 扑热息痛中位仍为 1.80 g，故数值不变）"
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "drug": "5",
    "freq": "12",
    "tier": "high",
    "weight": "60",
    "age": ""
  },
  "expect": ["已超过最大日剂量 1.00 g"],
  "ref": "D-N5 年龄空值实况：头孢呋辛酯（idx 5）30 mg/kg q12h、60 kg ⇒ 单次 1800 mg、日 3600 mg；儿童按体重上限 60×60 = 3600 mg，成人绝对上限 1000 mg，有效上限 = min = 1000 mg ⇒ 超限并给出封顶 500.0 mg。旧实现年龄空值按儿童上限 3600 mg，日 3600 未超限、无该提示；默认态 500/20/中位/q0h 日 250 mg 远低于上限 1200 mg，不命中。",
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "drug": "0",
    "freq": "4",
    "tier": "high",
    "weight": "30",
    "age": "13"
  },
  "expect": ["年龄 13 岁：按儿童口径处理（未满 14 岁）", "已超过最大日剂量 1.80 g"],
  "ref": "D-N5 13 岁：对乙酰氨基酚上限档 15 mg/kg q4h、30 kg ⇒ 单次 450 mg、日 2700 mg；儿童按体重上限 60×30 = 1800 mg，成人绝对上限 4000 mg，有效上限 min = 1800 mg ⇒ 超限。旧实现 13 岁走儿童口径本也 1800 mg，但新增「年龄 13 岁」明确标注；默认态年龄空值只会显示「年龄未填写」，不命中。",
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "drug": "0",
    "freq": "4",
    "tier": "high",
    "weight": "30",
    "age": "14"
  },
  "expect": ["年龄 14 岁：按成人口径处理（≥14 岁）", "已超过最大日剂量 1.80 g"],
  "ref": "D-N5 14 岁边界：旧实现切到成人绝对上限 4000 mg ⇒ 日 2700 mg 不超限；修复后仍取 min(4000, 1800) = 1800 mg ⇒ 超限，结论与 13 岁一致不再翻转。默认态年龄空值为「年龄未填写」，不命中。",
},
{
  "slug": "medical/calculator-calc-due-date",
  "inputs": {
    "cycle": "42"
  },
  "expect": [
    "42"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "750",
    "dur": "4",
    "conc": "0.4",
    "w": "60"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "240",
    "dur": "4",
    "drop": "20",
    "drug": "nacl3"
  },
  "expect": ["当前 3%氯化钠 速率 = 0.510 mEq/kg/h"],
  "ref": "D-N8 首次切换实况：240 mL/4 h/60 kg，滴系数 20 ⇒ 60.0 mL/h；切换 3%NaCl 后默认浓度 0.51 mEq/mL ⇒ 30.6 mEq/h ÷ 60 kg = 0.510 mEq/kg/h，超过 0.5 限值应判超限。旧实现 onchange 先 calc（用旧浓度 0.4）再 toggle 改浓度 ⇒ 首次算得 0.400 并误判安全；默认态 drug=none 无该速率串 ⇒ 判别力成立（注入 conc 会掩盖该缺陷，故不注入）。",
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "2.0",
    "meld_cr": "1.0",
    "meld_inr": "1.2",
    "meld_na": "140",
    "gcs_e": "3"
  },
  "expect": [
    "E3+V5+M6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "3.0",
    "meld_cr": "2.0",
    "meld_inr": "1.5",
    "meld_na": "130"
  },
  "expect": [
    "MELD-Na = 26.0（已纳入血钠校正）"
  ],
  "ref": "W1-A 回归：标准 MELD = 3.78×ln(3.0) + 11.2×ln(1.5) + 9.57×ln(2.0) + 6.43 = 21.8；血钠 130（钳制区间内）⇒ MELD-Na = 21.8 + 1.32×7 − 0.033×21.8×7 = 26.0。四项输入均非默认（2.0/1.0/1.2/140）；旧实现输出 MELD-Na 恒 6，本串不命中。"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "1",
    "from": "1"
  },
  "expect": [
    "0.0555555555556"
  ],
  "ref": "2026-10-25 选项系数互换后（mmol=18/mg/dL=1 基准）：1 mg/dL→mmol/L = 1×1÷18=0.0555555555556；默认态（val=1,from=mmol(18) → 18）不含该串 ⇒ 强判别、零逃生。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "1000",
    "df": "15",
    "time": "60"
  },
  "expect": [
    "滴速 = 250.00 滴/分"
  ],
  "ref": "去默认化：滴速 = vol×df/time = 1000×15/60 = 250.00 滴/分。默认态 vol=500/df=20/time=120 ⇒ 83.33 滴/分，不命中。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "250",
    "df": "20",
    "time": "100"
  },
  "expect": [
    "滴速 = 50.00 滴/分"
  ],
  "ref": "去默认化：滴速 = 250×20/100 = 50.00 滴/分。默认态不命中。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "20",
    "time": "0"
  },
  "expect": ["输注时间须大于 0"],
  "ref": "D-N10 时长 0 实况：旧实现 time=0 ⇒ 500×20÷0 = Infinity 滴/分；修复后逐项守卫判 time>0 失败，清空主结果并提示「输注时间须大于 0」，不输出 Infinity/NaN。默认 time=120 有效，不含该提示 ⇒ 判别力成立。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "0",
    "time": "120"
  },
  "expect": ["滴系数须大于 0"],
  "ref": "D-N10 逐项校验：滴系数 0 时旧实现滴速 0、总滴数 0 且无提示；修复后判 df>0 失败并提示。默认 df=20 有效，不含该提示 ⇒ 判别力成立。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "0",
    "df": "20",
    "time": "120"
  },
  "expect": ["液体量须大于 0"],
  "ref": "D-N10 逐项校验：液体量 0 时旧实现滴速 0、总滴数 0 且无提示；修复后判 vol>0 失败并提示整句「液体量须大于 0」。默认 vol=500 有效，不含该提示 ⇒ 判别力成立。"
},
{
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "90",
    "height": "170",
    "age": "30",
    "perDose": "10"
  },
  "expect": [
    "900.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "24",
    "height": "118",
    "age": "6",
    "perDose": "10"
  },
  "clicks": ["document.getElementById('hepFunc').value='c';calc();"],
  "expect": [
    "6 岁：男童中位体重约 20.5 kg ，女童约 20.2 kg",
    "较同龄男童中位体重高 17%",
    "主要清除途径：肝脏 肝功能 C 级：建议显著减量"
  ],
  "ref": "WHO 生长标准 P50：6 岁男 20.5 kg / 女 20.2 kg；输入 24 kg ⇒ (24-20.5)/20.5=17.07% ⇒ 高 17%。对乙酰氨基酚（DRUGS[0]）经肝代谢，Child-Pugh C ⇒ 显著减量或避免。失败态：clicks 清空 ⇒ hepFunc 回落 normal、age 保持默认 30（非儿童）⇒ 参考体重段不出现、肝提示消失 ⇒ 三条均不命中。"
},
{
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "60",
    "height": "170",
    "age": "30",
    "perDose": "10"
  },
  "clicks": ["document.getElementById('drug').value='3';document.getElementById('renalFunc').value='severe';calc();"],
  "expect": [
    "药物：阿莫西林（Amoxicillin）",
    "主要清除途径：肾脏 肾功能重度下降：建议显著减量"
  ],
  "ref": "drug value=3 ⇒ DRUGS[3]=阿莫西林（索引序：对乙酰氨基酚0/布洛芬1/阿司匹林2/阿莫西林3），经肾排泄；肾功能重度下降（Ccr 15–29）⇒ 显著减量或延长间隔。默认药物为对乙酰氨基酚（肝脏）且 renalFunc 回落 normal ⇒ 两条均不命中。"
},
{
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "70",
    "height": "165",
    "age": "28"
  },
  "clicks": ["document.getElementById('drug').value='5';onDrugChange();"],
  "expect": [
    "2686.8 mg",
    "按体表面积（mg/m²）：1500 mg/m² × BSA 1.79 m²"
  ],
  "ref": "BSA 基准药物：头孢曲松（DRUGS[5]，成人 bsa=1500 mg/m²；childW=50 仅用于儿童）。复算：BSA=√(165×70÷3600)=1.79118 m²；单次=1.79118×1500=2686.773 → toFixed(1)=2686.8 mg。修复前按 weight 把 1500 当 mg/kg 乘 70 = 105000 mg。输入 70/165/28 均非默认（60/170/30），默认药物为对乙酰氨基酚 ⇒ 两条均不命中。"
},
{
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "20",
    "height": "118",
    "age": "5"
  },
  "clicks": ["document.getElementById('drug').value='2';onDrugChange();"],
  "expect": [
    "儿童禁用：「阿司匹林」",
    "未计算 剂量基准"
  ],
  "ref": "阿司匹林（DRUGS[2]）childW=0 且 childContra=true：5 岁（<14）⇒ basisFor 返回 contra ⇒ renderBlocked，结果区不输出数字剂量并显示儿童禁用/剂量基准未计算。修复前按成人 10 mg/kg×20 kg 输出 200.0 mg 且无结果区警示。注入 20/118/5 均非默认（60/170/30），失败态回落成人态 ⇒ 两条动态锚均不命中（「儿童禁用」原生字串在药物下拉与静态说明里恒存在，不能作锚）。"
},
{
  "slug": "medical/drug-info",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "未找到匹配药物"
  ],
  "ref": "关键词过滤型：inputs 写 search=zzzqx ⇒ oninput=render() 过滤 34 种药物得空集 ⇒ 结果区渲染「未找到匹配药物」。默认态（search 空）渲染全部 34 种、blob 内无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "medical/estimate-metabolism",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30",
    "bf": ""
  },
  "expect": [
    "+149.3%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/medical-calculator",
  "inputs": {
    "dose_weight": "90",
    "dose_per_kg": "10",
    "dose_freq": "3",
    "iv_volume": "500",
    "iv_time": "120",
    "glucose_mmol": "5.6",
    "glucose_mg": "100.9",
    "temp_value": "36.5",
    "bp_sbp": "120",
    "bp_dbp": "80",
    "timer_custom_min": ""
  },
  "expect": [
    "900.0mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/medical-calculator",
  "inputs": {
    "dose_weight": "60",
    "dose_per_kg": "10",
    "dose_freq": "1.5"
  },
  "expect": [
    "每次剂量 = 600.0mg / 1.5次 = 400.0mg"
  ],
  "ref": "D-N23 小数频次：旧实现 parseInt 把 1.5 截断为 1，每日 600.0mg 被算成每次 600.0mg；修复后 parseFloat 保留 1.5 ⇒ 600.0 ÷ 1.5 = 400.0mg。默认 freq=3 时该串为「600.0mg / 3次 = 200.0mg」，不命中 ⇒ 强判别。"
},
{
  "slug": "medical/reminder-2",
  "inputs": {
    "medName": "阿莫西林胶囊",
    "medBatch": "B20260118",
    "medExpiry": "2027-03-15",
    "medSpec": "0.25g×24粒",
    "medLocation": "客厅药箱"
  },
  "clicks": ["addMed()"],
  "expect": [
    "阿莫西林胶囊 0.25g×24粒",
    "1 药品总数",
    "批号：B20260118"
  ],
  "ref": "addMed() 要求 medName 与 medExpiry 均非空（否则 showToast 后直接 return），两项都要注入；"
     + "入表后 renderAll() 刷新 medList 与 statGrid。不锚「剩 N 天」与安全/注意/紧急计数 —— 均随运行日漂移。"
     + "默认态 meds 为空 ⇒ 列表恒「暂无药品记录」、总数恒 0。",
},
{
  "slug": "medical/stats-4",
  "inputs": {
    "cases": "阑尾切除,55\n阑尾切除,72\n阑尾切除,64\n阑尾切除,88\n阑尾切除,61"
  },
  "expect": [
    "68.0",
    "89.0",
    "12.75"
  ],
  "ref": "手术时长：5 例 55/72/64/88/61 → 均值 340/5=68.0 分钟，样本标准差 12.75，排台上限 P95=68.0+1.645×12.75=89.0（独立复算，非页面默认记录）"
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

  console.log("==== medical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
