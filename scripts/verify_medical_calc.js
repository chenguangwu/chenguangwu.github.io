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
  "expect": ["对乙酰氨基酚（扑热息痛）（解热镇痛） 布洛芬（解热镇痛） 阿莫西林（抗生素） 阿莫西林克拉维酸（抗生素） 头孢氨苄（先锋IV）（抗生素） 头孢呋辛酯（抗生素） 头孢曲松（抗生素） 阿奇霉素（抗生素） 克拉霉素（抗生素） 苯巴比妥（抗癫痫）（神经系统） 苯妥英钠（抗癫痫）（神经系统） 地塞米松（激素） 泼尼松（强的松）（激素） 万古霉素（抗生素） 氨茶碱（呼吸系统） 左乙拉西坦（神经系统）\nq4h（每4小时） q6h（每6小时） q8h（每8小时） q12h（每12小时） q24h（每日一次）\n对乙酰氨基酚（扑热息痛） 分类：解热镇痛 | 推荐剂量：10-15 mg/kg/次 | 常用间隔 q6h 每4-6小时一次，儿童单次不超过 15mg/kg，日总量≤60mg/kg（成人≤4g/日）。\n暂无计算记录\n30\nmid\n375.0 mg 单次剂量 375.0 mg 每日总量（1次） 1.80 g 儿童最大日剂量 ✓ 当前剂量在安全范围内。给药方案：375.0 mg q0h，每日 1 次。"],
  "ref": "auto-restore"
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
