#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": {
    "avg24_sbp": "213",
    "avg24_dbp": "88",
    "day_sbp": "150",
    "day_dbp": "92",
    "night_sbp": "128",
    "night_dbp": "78",
    "lowest_sbp": "120",
    "morning_sbp": "165"
  },
  "expect": [
    "213/88"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": {
    "avg24_sbp": "148",
    "avg24_dbp": "86",
    "followDate": "2024-03-10"
  },
  "expect": [
    "随访计划（评估日 2024-03-10，24h平均 达到ABPM高血压阈值）",
    "第3次随访：2024-06-08（评估后 90 天"
  ],
  "ref": "随访计划生成器（03-66）：avg24 148/86 ≥130/80（2023 ESH/2018 ESC-ESH ABPM 阈值）⇒ 24h平均 达到ABPM高血压阈值 ⇒ 日程 14/30/90/365 天。2024-03-10 +90 天 = 2024-06-08（3 月余 21 + 4 月 30 + 5 月 31 = 82，余 8 天 → 6/8；闰年 2/29 在起点前不影响）。默认 followDate 为空 ⇒ 日程块不渲染；discriminator 将 avg24_sbp 换回默认 142、followDate 换回空 ⇒ 两条锚零交集。日期对固定、与运行日无关（铁律④）。"
},
{
  "slug": "cardiology/antiarrhythmic-class",
  "clicks": [
    "showClass('4', {classList:{add:function(){},remove:function(){}}})"
  ],
  "expect": [
    "IV类",
    "钙通道阻滞剂"
  ],
  "ref": "clicks 直接调 showClass('4', 哑 classList)→IV类 非二氢吡啶类钙通道阻滞剂（维拉帕米/地尔硫䓬）。默认态为 I类（钠通道阻滞剂），故「IV类」可区分。"
},
{
  // 原用例 inputs 为空、expect 取「非复杂型Stanford B型」—— 那是建立在**旧 harness 失真**上的：
  // extent 组真机默认选中 ascDesc（HTML checked），旧桩 getElementsByName 恒 [] ⇒ getRadio 返回 0
  // ⇒ 被当成「非升主动脉受累」而落入 B 型。2026-09-24 起 harness 回落 HTML 默认选中态，
  // 真机默认（extent=ascDesc）实为 **A 型**（急诊外科手术），故原 expect 已不成立。
  // 现改为显式声明输入（不再受默认态影响）：extent=descOnly → B 型；malPerf=1 → 复杂型 →
  // 紧急 TEVAR（默认态 A 型输出「急诊外科手术」，故本 expect 具判别力）。
  "slug": "cardiology/aortic-dissection",
  "radios": {
    "extent": "descOnly"
  },
  "checkIds": [
    "malPerf"
  ],
  "expect": [
    "紧急TEVAR(腔内修复)",
    "复杂型Stanford B型夹层"
  ],
  "ref": "extent=descOnly（仅降主动脉）→ Stanford B 型 / DeBakey IIIa；malPerf=脏器灌注不良 → complicated → 紧急 TEVAR 腔内修复"
},
{
  "slug": "cardiology/aortic-dissection",
  "radios": {
    "extent": "ascDesc"
  },
  "checkIds": [
    "htn"
  ],
  "clicks": [
    "var b=document.getElementById('result').innerHTML;document.getElementById('result').innerHTML=(/A型[\\s\\S]{0,12}累及升主动脉/.test(b)&&/I型/.test(b))?'__AD_A_OK__':'__AD_A_FAIL__'+b"
  ],
  "expect": [
    "__AD_A_OK__"
  ],
  "ref": "D-N94 示例回归：深解示例为「升+降全程 + 仅高血压 ⇒ Stanford A / DeBakey I / 急诊」，页面默认不预选范围（首屏显示「请选择夹层累及范围」）。clicks 读取结果区同时校验 Stanford A 与 DeBakey I，不选范围或分型错误均输出 FAIL。"
},
{
  // 出血增量公式 + 50–59 岁个体化分支
  "slug": "cardiology/aspirin-prevention",
  "inputs": {
    "age": "55",
    "ascvd": "12"
  },
  "checkIds": ["priorBleed", "anticoag"],
  "expect": [
    "谨慎个体化决策(C级)",
    "增加6–10例/1000人"
  ],
  "ref": "2 项出血因素 → 出血增量 (2×2+2)–(3×2+4)=6–10 例/1000人；55 岁、ASCVD 12% → 50–59 岁分支「谨慎个体化决策(C级)」。3 项及以上会落入「不推荐使用」分支，故取 2 项。默认无勾选 → factors=0 → 「推荐考虑…」+「增加2–7例」，两条均不命中。"
},
{
  // 原为 no_inputs 弱用例（空输入只能断言提示语，零判别力）。
  "slug": "cardiology/calc-1",
  "inputs": {
    "sbp": "150",
    "dbp": "95"
  },
  "checkIds": [
    "diabetes"
  ],
  "expect": [
    "血压分级： 1级高血压",
    "很高危"
  ],
  "ref": "classifyBP(150,95) → 1级高血压（轻度）（收缩压140-159 或 舒张压90-99）；riskLayer 见 diabetes=true → 「高危 / 很高危」（糖尿病/靶器官损害/确诊CVD 任一即高危）。回退默认（空输入）→ 仅提示「请输入有效的收缩压和舒张压」；不勾选 → 低危。两串均不命中。"
},
{
  // JNC 7 的 2 级边界：SBP≥160 或 DBP≥100（区别于 2017 ACC/AHA 的 ≥140/90）
  "slug": "cardiology/calc-1",
  "inputs": {
    "sbp": "165",
    "dbp": "102"
  },
  "expect": [
    "2级高血压",
    "收缩压 ≥160 或 舒张压 ≥100 mmHg"
  ],
  "ref": "classifyBP(165,102)：SBP≥160 → 2级高血压，描述串为「收缩压 ≥160 或 舒张压 ≥100 mmHg」。默认 118/76 → 正常血压，回退默认不命中；150/95 用例已单独锁定 1 级，本例锁定 JNC 7 的 2 级下界。"
},
{
  "slug": "cardiology/calc-3",
  "inputs": {
    "age": "2", "killip": "0"
  },
  "expect": [
    "2.2%"
  ],
  "ref": "auto-restore"
},
{
  // ≥75 岁计 3 分 → mortality[3]='3.1%'（默认 <65 岁为 0.8%）
  "slug": "cardiology/calc-3",
  "inputs": {
    "age": "3", "killip": "0"
  },
  "expect": [
    "3.1%"
  ],
  "ref": "age 选项值 3 = ≥75 岁计 3 分，其余默认未勾选 → 总分 3；mortality[3]='3.1%'。默认 <65 岁 → 0.8%，注入失败回退默认不命中。"
},
{
  "slug": "cardiology/cardiac-rehab-mets",
  "inputs": {
    "mets": "8",
    "weight": "70"
  },
  "expect": [
    "1960"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/chads2-vasc",
  "inputs": {
    "sex": "f"
  },
  "expect": ["f\n2\n3 CHA₂DS₂-VASc 总分 3.2% 卒中年风险 推荐OAC 抗凝建议 评分明细 年龄≥75岁 → +2 女性 → +1 总分 = 3 抗凝决策 推荐口服抗凝药(OAC)：华法林(INR 2–3)或DOAC(达比加群/利伐沙班/阿哌沙班/艾多沙班)。"],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/ckd-epi",
  "inputs": {
    "age": "98",
    "scr": "1.3",
    "uacr": "80", "sex": "m"
  },
  "expect": [
    "ACEI/ARB/SGLT2i治疗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "age": "93",
    "cacs": "280", "sex": "m"
  },
  "expect": [
    "50–75百分位"
  ],
  "ref": "注入 age=93/cacs=280：CACS=280 落 [100,400) → 中度钙化；年龄分位 50–75百分位（默认 age=62/cacs=280 同为中钙，但分位是 ≥75百分位 ⇒ 「50–75百分位」随注入变化、零交集）。原 expect「93岁」输入回显、「中度钙化」默认态同命中（cacs 默认恰为 280）均不可用。S3 参考区间标尺 refBar(#cacsRefBar) 已加（bands: 无/轻/中/广/重，max1500），harness 因 TBKit 守卫不渲染但文本定位已落 #result。"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "sex": "m",
    "age": "55",
    "cacs": "50",
    "followDate": "2024-01-15"
  },
  "expect": [
    "随访计划（评估日 2024-01-15，轻度钙化）",
    "第1次随访：2027-01-14（评估后 1095 天"
  ],
  "ref": "随访计划生成器铺开五（03-73）：CACS=50 → 轻度钙化 → 1095 天复查；2024-01-15+1095 天（含 2024-02-29 闰日，366+365+365）= 2027-01-14。followDate 默认空 ⇒ 日程块不渲染，老用例零交集。"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "sex": "f",
    "age": "70",
    "cacs": "600",
    "followDate": "2024-01-15"
  },
  "expect": [
    "随访计划（评估日 2024-01-15，广泛钙化）",
    "第1次随访：2025-01-14（评估后 365 天"
  ],
  "ref": "CACS=600 → 广泛钙化 → 365 天年度复查 + 冠脉 CTA 评估；2024-01-15+365 天（跨 2024-02-29）= 2025-01-14。"
},
{
  "slug": "cardiology/cpet-analysis",
  "inputs": {
    "peakVO2": "20.5",
    "at": "9.5",
    "veVco2": "34",
    "rer": "1.12",
    "pctPred": "58"
  },
  "expect": [ "20.5 峰值VO₂" ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/echo-report",
  "inputs": {
    "lvef": "72",
    "lvesv": "55",
    "lvidd": "56",
    "la": "42",
    "ao": "32",
    "rv": "22",
    "ea": "0.8",
    "eprime": "6"
  },
  "expect": [
    "72%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/grace-score",
  "inputs": {
    "age": "102",
    "hr": "95",
    "sbp": "130",
    "cr": "1.2", "killip": "1"
  },
  "expect": ["+64 心率 95次/分"],
  "ref": "auto-restore"
},
{
  // radios 注入单选组（htn=1 高血压、stroke=1 卒中史），checkIds 注入复选（drugs 合并抗血小板/NSAIDs、
  // alcohol 酗酒）→ 1+1+1+1 = 4 分 → 高危、出血风险 8.70%。
  // 原用例 inputs 为空、expect 取默认态 "1.13%"（0 分低危）⇒ 零判别力，已去默认化。
  "slug": "cardiology/has-bled",
  "radios": {
    "htn": "1",
    "stroke": "1", "bleed": "0", "inr": "0", "elderly": "0"
  },
  "checkIds": [
    "drugs",
    "alcohol"
  ],
  "expect": [
    "8.70%"
  ],
  "ref": "HAS-BLED 九项各 1 分：高血压 1 + 卒中史 1 + 合并抗血小板/NSAIDs 1 + 酗酒 1 = 4 分 → 高危（出血风险 8.70%）"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": {
    "pvcTotal": "8500",
    "pvcHr": ""
  },
  "expect": [
    "频发室早(24h 总量折算 ≥30次/小时) → Lown 2级"
  ],
  "ref": "D-N96 频发判定：只填 24h 总量 8500（≈354 次/小时）而每小时留空时，旧实现 `pvcHr=0` 落「偶发(<30次/小时) → Lown 1级」；修复后按 24h 总量折算判 2 级。默认 pvcTotal=8500、pvcHr=520 走「频发室早(≥30次/小时)」旧文案，与本串互斥。"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": {
    "pvcTotal": "12000",
    "totalBeats": "98000"
  },
  "expect": [
    "室早负荷 = 12000/98000 = 12.2%"
  ],
  "ref": "D-N97 总心搏参与：新增 24h 总心搏输入，12,000/98,000 = 12.2%，与深解示例一致；旧实现固定 100,000 得 12.0%。默认 100000 的分母不会产生 12.2%。"
},
{
  "slug": "cardiology/holter-grading",
  "checkIds": ["vt"],
  "inputs": {
    "vtSec": "30",
    "vtBeats": "0"
  },
  "expect": [
    "持续性室速"
  ],
  "ref": "D-N99 边界：同页引据写「非持续(<30s)/持续(≥30s)」，30 秒整应判持续性；旧实现 `vtSec>30` 会判 NSVT。未勾室速时不会输出「持续性室速」，默认 0 秒也走 NSVT。"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": { "pvcTotal": "200", "pvcHr": "5" },
  "clicks": ["calc()"],
  "expect": [
    "通常良性，定期随访观察"
  ],
  "ref": "D-N98 反面分支：纯低负荷（200 次/24h、pvcHr 5 ⇒ Lown 1 级、0.2%）仍保留「通常良性，定期随访观察」（默认态 8500/520 为 Lown 2 级、走「负荷虽低但需评估病因」分支，不含本串）。原用例只 calc() 注入=默认态故撞默认；改用低负荷输入验证修复未把低危也误改为评估文案。"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": {
    "pvcTotal": "12750",
    "pvcHr": "520",
    "vtBeats": "0",
    "vtSec": "0"
  },
  "expect": [
    "12750/100000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/hypertension-jnc",
  "inputs": {
    "sbp": "233",
    "dbp": "95"
  },
  "expect": [
    "233/95"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/hypertension-jnc",
  "inputs": {
    "sbp": "145",
    "dbp": "92",
    "followDate": "2024-01-15"
  },
  "checkIds": [
    "lipid"
  ],
  "expect": [
    "随访计划（评估日 2024-01-15，中危）",
    "第2次随访：2024-04-14（评估后 90 天"
  ],
  "ref": "随访计划生成器（03-65）：sbp=145→1级、dbp=92→1级 ⇒ 1级高血压；勾选血脂异常=1 个危险因素。按 JNC-7 风险分层表，Stage 1 + 1–2 个危险因素属「中危」（Stage 1 无危险因素才是低危）。中危日程 30/90 天：2024-01-15 +30 天 = 2024-02-14、+90 天 = 2024-04-14。默认 followDate 为空 ⇒ 日程块不渲染；discriminator 清空 checkIds 且回退输入 ⇒ 退回低危、无 90 天锚。日期对固定、与运行日无关（铁律④）。"
},
{
  "slug": "cardiology/myocardial-bridge",
  "inputs": {
    "compression": "98",
    "diastolic": "10",
    "length": "25",
    "depth": "3"
  },
  "expect": [
    "98%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nt-probnp",
  "inputs": {
    "age": "108",
    "ntprobnp": "1850"
  },
  "expect": [
    "NT-proBNP≥1800 pg/mL(>75岁截断值)",
    "NT-proBNP 1850 pg/mL → 落在 纳入区（>75岁，纳入截断 1800 pg/mL）"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nyha-classification",
  "inputs": {
    "walk": "480", "nyha": "2"
  },
  "expect": [
    "480米"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "8", "distribution": "circum"
  },
  "clicks": [
    "var b=document.getElementById('result').innerHTML;var m=/分级：<strong[^>]*>([^<]+)</.exec(b);document.getElementById('result').innerHTML=(m&&m[1]==='微量')?'__PE8_OK__':'__PE8_FAIL__'+(m?m[1]:b)"
  ],
  "expect": [
    "__PE8_OK__"
  ],
  "ref": "D-N102 预设标签：8mm 在五档表内属「微量（<10mm）」，原预设名却写「少量局限性积液」；已改名并补门禁用例。clicks 从结果区读回分级文本比对「微量」，默认 22mm 为「中量」，不会误命中。"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "30", "distribution": "circum"
  },
  "clicks": [
    "var b=document.getElementById('result').innerHTML;var m=/分级：<strong[^>]*>([^<]+)</.exec(b);document.getElementById('result').innerHTML=(m&&m[1]==='中量')?'__PE30_OK__':'__PE30_FAIL__'+(m?m[1]:b)"
  ],
  "expect": [
    "__PE30_OK__"
  ],
  "ref": "D-N103 边界：同页表格「中量 20–30mm、大量 >30mm」，30mm 整应判中量；旧实现 `depth<30` 把 30 判成大量并给出 1000–2000mL。默认 22mm 为中量，但本用例真实注入 30 后比对分级文本，边界写错即 FAIL。"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "0", "distribution": "circum"
  },
  "expect": [
    "未见心包积液"
  ],
  "ref": "D-N100 零深度：0 mm 应提示「未见心包积液」而非按 `depth<10` 给「微量 50–100mL」；旧实现 `parseFloat||0` 且无 0 守卫。默认 22mm 走中量，不命中该串。"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "-5", "distribution": "circum"
  },
  "expect": [
    "最大深度须为不小于 0 的数值"
  ],
  "ref": "D-N100 负值：负数深度属无效测量，旧实现 `||0` 后按微量输出；修复后单独提示。0 mm 走另一条「未见心包积液」文案，二者互斥。"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "33", "distribution": "circum"
  },
  "expect": [
    "2000mL"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/rater-risk-3",
  "inputs": {
    "age": "98",
    "hr": "80",
    "sbp": "130",
    "cr": "1.0"
  },
  "expect": [
    "114"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/statin-dose",
  "inputs": {
    "ldl": "6.8"
  },
  "expect": ["6.8\n1.8\n6.8 当前 LDL-C 1.8 目标 LDL-C 73.5% 所需降幅 高强度 他汀强度 计算过程 当前LDL-C = 6.8 mmol/L 目标LDL-C = 1.8 mmol/L 所需降幅 = (6.8−1.8)/6.8×100% = 73.5% 预计达标后LDL-C = 1.80 mmol/L 他汀强度等级： 高强度 联合用药建议 单药最大降幅可能不足，建议联合治疗 高强度他汀(最大降幅~55%) + 依折麦布(额外~20%) 联合后预期降幅：~64% 联合仍不达标：加用PCSK9抑制剂(额外降50–60%) 需联合用药 单药最大他汀可能无法达标，建议联合依折麦布和PCSK9抑制剂。"],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/timi-score",
  "inputs": {
    "s_age": "2", "s_bp": "0", "s_killip": "0", "s_wt": "0"
  },
  "expect": [
    "2/14"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/echo-report",
  "inputs": {
    "lvef": "25"
  },
  "expect": [
    "LVEF = 25% → 重度降低"
  ],
  "ref": "注入 LVEF 25%（默认 48%）→ 命中重度降低分支；新文案明确不下「终末期心衰」结论、须心衰专科评估。默认 48% 不含该句，0 逃生。"
},
{
  "slug": "cardiology/nyha-classification",
  "inputs": {
    "walk": "120", "nyha": "4"
  },
  "expect": [
    "是否进入终末期或需移植/LVAD 应由心衰专科"
  ],
  "ref": "注入 6MWT 120 米（默认 480）→ 极重度受损分支；页面只提示高死亡风险并要求心衰专科评估，不再写「终末期心衰/终末关怀」。默认 480 不含该句。"
},
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": { "avg24_sbp": "", "avg24_dbp": "80", "day_sbp": "130", "day_dbp": "80", "night_sbp": "120", "night_dbp": "70", "morning_sbp": "135", "lowest_sbp": "110" },
  "expect": ["请填写 8 项 ABPM 数值"],
  "ref": "03-91 核销：8 项任一空值即拦截，不再按 0 输出「0/0 正常 + 非杓型」并生成随访建议。"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": { "age": "60", "cacs": "", "sex": "m" },
  "expect": ["请填写有效年龄（1–120 岁）与 Agatston 钙化积分（≥0，无钙化请填 0）。"],
  "ref": "03-97 核销：钙化积分空值不再按 0 判「无钙化」并建议停用他汀，改为提示填写（0 分为合法值，须显式填 0）。补注入 sex=m 使提示从默认态的「请选择性别…」变为「请填写有效年龄…积分」（默认态全空只显示前者），原锚撞默认态故改之。"
},
{
  "slug": "cardiology/echo-report",
  "inputs": { "lvef": "" },
  "expect": ["请输入有效 LVEF（1–100%）"],
  "ref": "03-132 核销：LVEF 空值不再按 0 判「重度降低/终末期心衰、评估移植/LVAD」，改为拦截不出结论。"
},
{
  "slug": "cardiology/cpet-analysis",
  "inputs": { "peakVO2": "" },
  "expect": ["请填写全部 CPET 参数"],
  "ref": "03-138 核销：五项 CPET 参数任一空值即拦截，不再按 0 落入 Weber D 并「强烈推荐心脏移植/LVAD」。"
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

  console.log("==== cardiology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
