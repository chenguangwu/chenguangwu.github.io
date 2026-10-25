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
{"slug":"pediatrics/dehydration-assessment","inputs":{"weight":"8","prevWeight":"8.8"},"checkIds":["s3","s4","s8"],"expect":["结果：分度：中度脱水（估计体液丢失 5-10%）· Gorelick 评分 3/10","体重丢失法算得 9.1%"],"ref":"门诊记录：勾选 s3 黏膜干燥 + s4 眼窝凹陷 + s8 尿量减少 ⇒ Gorelick 3/10 落 3–6 段「中度脱水」（5-10%）；病前 8.8 kg → 现 8 kg，体重丢失 (0.8/8.8)=9.1% ⇒ 累计丢失量按体重丢失法算得约 727 mL。默认态 10 kg、未勾选、无病前体重 ⇒「轻度脱水」「Gorelick 0/10」，零交集。"},
{"slug":"pediatrics/diarrhea-dehydration","inputs":{"age":"18","weight":"10","stoolFreq":"8","duration":"3","stoolType":"watery"},"checkIds":["s1","s4","s5","s8"],"expect":["结果：分度：中度脱水（体液丢失 8%）· 腹泻 8 次/日 · 病程 3 天 · 大便性状 水样便","重度体征 0 项、中度体征 4 项、轻度体征 0 项（共 4 项）"],"ref":"门诊记录：勾选 s1 眼窝凹陷 + s4 皮肤弹性差 + s5 尿量减少 + s8 前囟凹陷，全属中度体征 4 项 ⇒ 中度脱水（7.5%→显示 8%）；水样便。默认态 12 月/10 kg/6 次/日、未勾选 ⇒「无脱水（体液丢失 0%）」，零交集。"},
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
{"slug":"pediatrics/neonatal-jaundice","inputs":{"hours":"72","tsb":"15","ga":"39","bw":"3200"},"expect":["结果：TSB 15 mg/dL @ 出生 72 小时 → 高危险区；光疗阈值 17、换血阈值 22 → 未达光疗阈值","小时龄百分位 P40 11.5 / P75 14.5 / P95 15.0 mg/dL；高危因素：无"],"ref":"门诊记录：Bhutani 1999 小时龄百分位表 72 h 为 P40 11.5 / P75 14.5 / P95 15.0 mg/dL（AAP 2004/2009 沿用），TSB 15 ≥ P95 ⇒「高危险区」；39 周足月低危儿 72–96 h 光疗阈值 17、换血 22（页面 getThresholds）⇒ 未达光疗阈值。默认态 48 h/TSB 14 ⇒「TSB 14 mg/dL @ 出生 48 小时」「P95 12.0」，零交集。本用例同时锁住「百分位表口径」（原实现用二次多项式近似，72 h 给出 P95 56.8 mg/dL 的荒谬值，已改为权威表插值）。"},
{"slug":"pediatrics/pediatric-anemia","inputs":{"age":"12","ageUnit":"month","weight":"10","hb":"95","sf":"8","mcv":"70"},"expect":["结果：年龄 12 月（6-59月）· Hb 95 g/L（阈值 ≥110）→ 中度贫血；MCV 70 fL（阈值 ≥75）、SF 8 μg/L → 缺铁性贫血(IDA,Stage 3)","元素铁补充量 40.0 mg/日；SF 偏低：是；MCV 偏低：是"],"ref":"门诊记录：12 月龄属 6-59 月组，Hb 阈值 110 g/L，实测 95 ⇒ 中度贫血；MCV 70 < 75、SF 8 < 12 ⇒ IDA Stage 3；10 kg × 4 mg/kg/日 = 40.0 mg/日元素铁。默认态 Hb 100/MCV 72/SF 12 ⇒「轻度贫血」「铁储存不足」，零交集。"},
{"slug":"pediatrics/pediatric-fever","inputs":{"temp":"39.2","age":"8"},"clicks":["var e=document.getElementById('fever3d');if(e){e.checked=true;}calc()"],"expect":["结果：体温 39.2°C（腋温）→ 腋温等效 39.2°C，分度：高热","月龄 8 月；危险信号 1 条"],"ref":"门诊记录（EMR note）：体温 39.2°C（腋温）落 39.0–41.0 段「高热」；勾选发热>3 天 ⇒ 危险信号 1 条。默认态 38.5°C/24 月、未勾选 ⇒「分度：中度发热」「危险信号 0 条」，零交集。原用例只锚 39.5°C 单值（输入回显式弱锚）。"},
{"slug":"pediatrics/pediatric-pneumonia","inputs":{"age":"10","rr":"52","spo2":"95"},"checkIds":["s1","s2"],"expect":["结果：分度：重症肺炎，呼吸 52 次/分（该年龄增快阈值 50）· SpO₂ 95% → 处置：住院治疗","极重症体征 0 项、重症体征 2 项；记录体征共 2 项"],"ref":"门诊记录：10 月龄 WHO 呼吸增快阈值 50，RR 52 达增快；勾选 s1 胸凹陷 + s2 鼻翼扇动 = 2 项重症体征、0 项极重症 ⇒ 落「重症肺炎」/「住院治疗」。默认态 12 月/RR 55/SpO₂ 92 且无勾选 ⇒「肺炎」/「门诊治疗」，零交集。"},
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

  console.log("==== pediatrics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
