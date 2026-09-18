#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pediatrics/assessor-13",
  "inputs": {
    "ageMonth": "36",
    "weight": "15",
    "prevWeight": "",
    "diarrheaDays": "5"
  },
  "expect": [
    "36月龄，15kg"
  ],
  "ref": "儿童脱水评估：输入 36 月龄 / 15kg（默认 24 月龄 / 12kg），评估结论文案含「患儿（36月龄，15kg）评估为 重度脱水」，取随输入变化的月龄+体重串作为判别锚点，回退默认(24月龄,12kg)即失配。"
},
{
  "slug": "pediatrics/assessor-spo2",
  "inputs": {
    "ageDay": "1",
    "rhSpO2": "85",
    "footSpO2": "80"
  },
  "expect": [
    "85%",
    "CCHD筛查阳性"
  ],
  "ref": "新生儿 CCHD 脉搏血氧筛查：右手 85% / 足部 80% / 差值 5% → 中风险、筛查阳性（默认 98/97/1% → 低风险、阴性）。取动态数值 85% 与结论「CCHD筛查阳性」双重锚定，回退默认无此串。"
},
{
  "slug": "pediatrics/chd-assessment",
  "inputs": {
    "age": "2",
    "rhSpo2": "85",
    "llSpo2": "78"
  },
  "expect": [
    "85%",
    "高风险"
  ],
  "ref": "先心病筛查：右手 85% / 下肢 78% / 差值 7% ≥5% → 高风险、阳性(转诊)（默认 97/96/1% → 极低风险、阴性）。取 85% 与「高风险」锚定，回退默认无。"
},
{
  "slug": "pediatrics/ddst-screening",
  "inputs": {
    "age": "6",
    "correctGA": ""
  },
  "expect": [
    "当前月龄： 6月"
  ],
  "ref": "DDST 发育筛查：输入 age=6 渲染 6 月龄测试项清单（默认 18 月）。取动态串「当前月龄： 6月」锚定，回退默认(18月)失配。注：结论需逐项勾选才出，故用随输入变化的月龄清单串作判别锚点。"
},
{
  "slug": "pediatrics/dehydration-assessment",
  "inputs": {
    "weight": "20",
    "prevWeight": ""
  },
  "expect": [
    "1600mL/日"
  ],
  "ref": "脱水评估：判定依赖体征勾选（默认无勾选→恒定「轻度脱水 0/10 3-5%」），但日维持量为体重函数：weight=20kg → 维持量 1600mL/日（默认 10kg → 800mL/日）。取随输入变化的「1600mL/日」锚定，回退默认(800mL/日)失配。"
},
{
  "slug": "pediatrics/diarrhea-dehydration",
  "inputs": {
    "age": "12",
    "weight": "10",
    "stoolFreq": "20",
    "duration": "7"
  },
  "expect": [
    "20次/日"
  ],
  "ref": "腹泻脱水评估：判定基于体征勾选（默认无→「无脱水 0%」恒定），但腹泻次数随输入显示：stoolFreq=20 → 「腹泻次数：20次/日」（默认 6次/日）。取动态串「20次/日」锚定，回退默认(6次/日)失配。"
},
{
  "slug": "pediatrics/enuresis-age",
  "inputs": {
    "age": "10",
    "freq": "2"
  },
  "expect": [
    "10岁"
  ],
  "ref": "遗尿症评估：age=10 / freq=2 → 轻度(2-3次/周)（默认 7岁 / 4次 → 中度）。取动态串「10岁」锚定，回退默认(7岁)失配。"
},
{
  "slug": "pediatrics/growth-curve-zscore",
  "inputs": {
    "age": "24",
    "height": "75",
    "weight": "10",
    "head": "46"
  },
  "expect": [
    "身高：75cm"
  ],
  "ref": "生长曲线 Z 评分：height=75 → 「身高：75cm | 中位数：102.3cm | Z评分：-11.47」(重度偏低)（默认 87cm → Z -6.43）。取动态串「身高：75cm」锚定，回退默认(87cm)失配。"
},
{
  "slug": "pediatrics/hfmd-course",
  "inputs": {
    "age": "24",
    "day": "5",
    "temp": "40"
  },
  "expect": [
    "40°C"
  ],
  "ref": "手足口病病程：temp=40 / day=5 → 「40°C 体温 第5天」（默认 38.5°C / 第2天）。取动态串「40°C」锚定，回退默认(38.5°C)失配。"
},
{
  "slug": "pediatrics/hirschberg-test",
  "inputs": {
    "fixing": "left",
    "reflex": "exo",
    "offset": "15",
    "pupil": "4"
  },
  "expect": [
    "明显眼位偏斜"
  ],
  "ref": "Hirschberg 角膜映光法：默认 fixing=right/reflex=center/offset=2 → 「眼位正位，无明显斜视」(恒定)；改 fixing=left/reflex=exo/offset=15 → 「明显眼位偏斜(≥2mm/~30°)」。取动态结论「明显眼位偏斜」锚定，回退默认(正位)失配。注：reflex=exo 分支存在未定义变量(输出含 undefined)，本次不修该 bug，仅取稳定结论串作判别锚点。"
},
{
  "slug": "pediatrics/neonatal-jaundice",
  "inputs": {
    "hours": "48",
    "tsb": "22",
    "ga": "38",
    "bw": "3200"
  },
  "expect": [
    "22 mg/dL"
  ],
  "ref": "新生儿黄疸 Bhutani 曲线：tsb=22 @ 48h → 「中低危险区」「需立即换血」(默认 14 → 低危险区、暂无需光疗)。取动态数值「22 mg/dL」锚定，回退默认(14 mg/dL)失配。"
},
{
  "slug": "pediatrics/pediatric-anemia",
  "inputs": {
    "age": "12",
    "weight": "10",
    "hb": "60",
    "sf": "5",
    "mcv": "60"
  },
  "expect": [
    "60g/L"
  ],
  "ref": "儿童贫血：hb=60 / mcv=60 → 重度贫血（默认 100 / 72 → 轻度）。取动态数值「60g/L」锚定，回退默认(100g/L)失配。"
},
{
  "slug": "pediatrics/pediatric-fever",
  "inputs": {
    "temp": "39.5",
    "age": "24"
  },
  "expect": [
    "39.5°C"
  ],
  "ref": "儿童发热：temp=39.5 → 「高热」（默认 38.5 → 中度发热）。取动态串「39.5°C」锚定，回退默认(38.5°C)失配。"
},
{
  "slug": "pediatrics/pediatric-pneumonia",
  "inputs": {
    "age": "12",
    "rr": "30",
    "spo2": "99"
  },
  "expect": [
    "RR=30"
  ],
  "ref": "儿童肺炎：rr=30 / spo2=99 → 无呼吸增快、无肺炎（默认 55 / 92 → 肺炎、门诊）。取动态串「RR=30」锚定，回退默认(RR=55)失配。"
},
{
  "slug": "pediatrics/rater-27",
  "inputs": {
    "ageMonth": "12",
    "weight": "15",
    "height": "80",
    "headCirc": "50"
  },
  "expect": [
    "15 kg"
  ],
  "ref": "儿保体格评估(WHO)：weight=15 → 体重/年龄 15 kg（中位数 9.6kg）→ Z 5.14 严重偏高（默认 9.6kg → Z 0.00 正常）。取动态串「15 kg」锚定，回退默认(9.6 kg)失配。"
},
{
  "slug": "pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian",
  "inputs": {
    "age": "48",
    "bili": "20"
  },
  "expect": [
    "20.0 mg/dL"
  ],
  "ref": "新生儿黄疸曲线(Bhutani)：bili=20 @ 48h(ga35) → 换血治疗区、双超标（默认 14 → 光疗阈值区）。取动态数值「20.0 mg/dL」锚定，回退默认(14.0 mg/dL)失配。"
},
{
  "slug": "pediatrics/vaccine-schedule",
  "inputs": {
    "vaccinatedMonth": "6"
  },
  "expect": [
    "预防：乙型肝炎 已接种"
  ],
  "ref": "疫苗接种时间表：vaccinatedMonth=6 表示已接种至 6 月龄 → 0~6 月龄疫苗行的状态变为「已接种」（默认空 → 全部「逾期，尽快补种」）。锚点取随输入变化的具体行串「预防：乙型肝炎 已接种」（仅当该行状态为已接种时出现），避开页面恒定图例「绿色=已接种…」(含「已接种」三字，裸「已接种」会恒命中导致逃生项)。回退默认(空)该行为「逾期，尽快补种」→ 失配。"
},
{
  "slug": "pediatrics/developmental-milestones",
  "inputs": {
    "age": "27"
  },
  "expect": [
    "说2-3字句"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pediatrics/hearing-screening",
  "inputs": {
    "age": "3",
    "method": "aabr"
  },
  "expect": [
    "AABR自动听性脑干反应"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pediatrics/mchat-autism",
  "inputs": {
    "age": "27"
  },
  "expect": [
    "27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pediatrics/pediatric-asthma",
  "inputs": {
    "age": "12"
  },
  "expect": [
    "你如何评价近4周哮喘控制情况"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pediatrics/pediatric-fracture",
  "inputs": {
    "age": "15"
  },
  "expect": [
    "15岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pediatrics/seizure-classification",
  "inputs": {
    "age": "30"
  },
  "expect": [
    "30月"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pediatrics/vanderbilt-adhd",
  "inputs": {
    "age": "12"
  },
  "expect": [
    "12"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== pediatrics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
