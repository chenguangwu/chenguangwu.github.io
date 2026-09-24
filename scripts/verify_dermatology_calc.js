#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原为 no_inputs 弱用例：expect「5-氟尿嘧啶(5-FU)乳膏」只在默认 1 级（轻度）分支出现，与输入无关。
  "slug": "dermatology/actinic-keratosis",
  "checkIds": [
    "r1",
    "r2"
  ],
  "expect": [
    "存在高危特征（快速增大、出血/溃疡）",
    "高危特征： 快速增大、出血/溃疡（已加4分）"
  ],
  "ref": "勾选 r1(快速增大)+r2(出血/溃疡) → isHighRisk=true → grade「高危病变」、恶变风险 >10%/年，并输出「存在高危特征（快速增大、出血/溃疡）」与「已加4分」。回退默认（四项均未勾选）→ 走 1/2/3 级分支，两串均不命中。"
},
{
  // 原为 all_default 弱用例：expect「12」= 默认态「0 / 12」里的分母，与输入无关。
  // 该页为脂溢性皮炎四项症状评分（红斑/脱屑/瘙痒/受累面积，各 0-3），满分 12。
  "slug": "dermatology/assessor-14",
  "inputs": {
    "d1": "3",
    "d2": "2",
    "d3": "3",
    "d4": "1"
  },
  "expect": [
    "9 / 12"
  ],
  "ref": "总分 = 3+2+3+1 = 9 → 渲染「严重程度评分： 9 / 12」并落重度分支（>7）。回退默认（d1..d4 全 0）→ 得 0 分、走轻度分支，串「9 / 12」不命中。"
},
{
  "slug": "dermatology/calc-1",
  "inputs": {
    "age": "45",
    "head": "9",
    "armR": "9",
    "armL": "9",
    "front": "18",
    "back": "18",
    "legR": "18",
    "legL": "18",
    "perineum": "1"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例：expect「瘙痒可外用弱效激素短程」属默认 I 级分支的建议文案，
  // 且该串只在 grade=1（默认）时出现，与勾选无关。
  // grade 只能由 selectGrade(btn,g) 点击改写，harness 无点击 ⇒ 恒为 1；可注入点是受累部位/感染警示。
  "slug": "dermatology/chilblain-grading",
  "checkIds": [
    "s1",
    "s2",
    "s3",
    "s5"
  ],
  "expect": [
    "受累部位：手、足、耳/鼻",
    "已继发感染，需局部抗感染处理"
  ],
  "ref": "勾选 s1(手)+s2(足)+s3(耳/鼻) → sites=[手,足,耳/鼻]，输出「受累部位：手、足、耳/鼻」；勾选 s5 → 输出感染警示「已继发感染，需局部抗感染处理」。回退默认（全未勾选）→ 无部位行、无警示，两串均不命中。"
},
{
  // 结构性不可注入（保留在 no_inputs 基线）：14 个过敏原卡片由 renderGrid() 拼 HTML 生成，
  // 反应强度靠卡片内 <button onclick="setReact(...)"> 点击写入 selections；静态 HTML 无 input/select/textarea，
  // harness 无 clicks 且按钮不在 elements 表内 ⇒ 只能渲染默认提示串。
  "slug": "dermatology/contact-dermatitis-patch",
  "inputs": {},
  "expect": [
    "请点击选择阳性的过敏原及反应强度"
  ],
  "ref": "结构性不可注入：过敏原网格 + 反应强度按钮均由 JS 模板生成（renderGrid/setReact），静态 HTML 无带 id 的表单控件；selections 仅能由点击写入。expect 锚定默认提示「请点击选择阳性的过敏原及反应强度」。"
},
{
  "slug": "dermatology/dermatoscopy-abcd",
  "inputs": {
    "borderScore": "7"
  },
  "expect": [
    "0.70"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/easi-eczema",
  "inputs": {
    "age": "child"
  },
  "expect": [
    "0.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/gags-acne",
  "inputs": {
    "loc0": "1"
  },
  "expect": [
    "前额"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例：expect「推荐外用20%氯化铝溶液」属默认 grade=2 分支建议文案，与勾选无关。
  // grade 同理只能由 selectGrade 点击改写（恒 2）；可注入点是部位/分型提示/警示。
  "slug": "dermatology/hdss-hyperhidrosis",
  "checkIds": [
    "s3",
    "s4",
    "s6",
    "s7",
    "s9"
  ],
  "expect": [
    "部位：足底、头面部",
    "符合原发性局灶性多汗症特征"
  ],
  "ref": "勾选 s3(足底)+s4(头面部) → 输出「部位：足底、头面部」；勾选 s6+s7+s9 → primary=true → 输出分型提示「符合原发性局灶性多汗症特征（局灶、年轻发病、睡眠停止）」。回退默认（全未勾选）→ 无部位行、primary=false（且 !s9 → 显示继发性警示），两串均不命中。"
},
{
  // 原为 no_inputs 弱用例：expect「局部冷敷15-20分钟」只在默认总分 ≤5（轻度）分支出现。
  "slug": "dermatology/insect-bite-reaction",
  "inputs": {
    "insectType": "bee"
  },
  "checkIds": [
    "sys1",
    "sys2",
    "sys3"
  ],
  "expect": [
    "发热、淋巴结肿大、全身皮疹",
    "蜂蜇伤特别注意"
  ],
  "ref": "勾选 sys1/2/3 → sysSymptoms 依次为 发热、淋巴结肿大、全身皮疹，sysScore=6 并输出「发热、淋巴结肿大、全身皮疹（已加6分）」；insectType=bee → 输出蜂蜇伤专属提示。回退默认（三项均未勾选、insectType=蚊虫）→ 两串均不命中。"
},
{
  "slug": "dermatology/leprosy-grading",
  "inputs": {
    "leprosyType": "BT"
  },
  "expect": [
    "界限类偏结核样型(BT)"
  ],
  "ref": "auto-restore"
},
{
  // 结构性不可注入（保留在 no_inputs 基线）：四种痱型由 selectType(el, idx) 点击按钮切换 currentType，
  // 静态 HTML 无表单控件 ⇒ harness 无法注入，只能渲染默认 currentType=0（晶痱）的内容。
  "slug": "dermatology/miliaria-classification",
  "inputs": {},
  "expect": [
    "脱离高温环境后1-2天内水疱干涸脱屑自愈"
  ],
  "ref": "结构性不可注入：痱型卡片由 selectType(按钮) 切换内部变量 currentType，静态 HTML 无带 id 的 input/select/textarea。expect 锚定默认型别（晶痱）的病程文案「脱离高温环境后1-2天内水疱干涸脱屑自愈」。"
},
{
  "slug": "dermatology/onychomycosis-grading",
  "inputs": {
    "hyphae": "1"
  },
  "expect": [
    "坚持3-6个月"
  ],
  "ref": "auto-restore"
},
{
  // 原为 all_default 弱用例：expect「头颈(×0.1)」是数据卡片的静态标签，与输入无关。
  // PASI = Σ 区域系数×(E+I+D)×A；四区系数 0.1/0.2/0.3/0.4。
  "slug": "dermatology/pasi-score",
  "inputs": {
    "h_e": "1",
    "h_i": "1",
    "h_d": "1",
    "h_a": "1",
    "u_e": "2",
    "u_i": "2",
    "u_d": "2",
    "u_a": "2",
    "t_e": "3",
    "t_i": "3",
    "t_d": "3",
    "t_a": "3",
    "l_e": "4",
    "l_i": "4",
    "l_d": "4",
    "l_a": "4"
  },
  "expect": [
    "30.0 PASI 总分 / 重度"
  ],
  "ref": "头颈 0.1×(1+1+1)×1=0.3、上肢 0.2×(2+2+2)×2=2.4、躯干 0.3×(3+3+3)×3=8.1、下肢 0.4×(4+4+4)×4=19.2 → 合计 30.0 → 重度分支（>12）。回退默认（16 个 select 全 0）→ 0.0 分、轻度分支，串「30.0 PASI 总分 / 重度」不命中。"
},
{
  // 原为 all_default 弱用例：expect「0/10」= 默认态「符合特征 0/10 ｜ 核心特征 0/4」里的默认计分，与输入无关。
  "slug": "dermatology/pityriasis-rosea",
  "checkIds": [
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8"
  ],
  "expect": [
    "符合特征 8/10 ｜ 核心特征 4/4"
  ],
  "ref": "勾选 f1..f8 → score=8、coreFeats=4 → 满足 score≥8 且 core≥3 → 高度符合分支，并输出「符合特征 8/10 ｜ 核心特征 4/4」。回退默认（十项全未勾选）→ 「符合特征 0/10 ｜ 核心特征 0/4」、走尚需鉴别分支，不命中。"
},
{
  // 原为 all_default 弱用例：expect「14」= 默认态「VSS总分： 0 / 14」里的分母，与输入无关。
  // VSS（温哥华瘢痕量表）：厚度 0-3、血管分布 0-3、柔韧性 0-5、颜色 0-3，满分 14。
  "slug": "dermatology/rater-28",
  "inputs": {
    "v1": "1",
    "v2": "2",
    "v3": "3",
    "v4": "1"
  },
  "expect": [
    "VSS总分： 7 / 14"
  ],
  "ref": "总分 = 1+2+3+1 = 7 → 渲染「VSS总分： 7 / 14」并落中度疤痕分支（≤7）。回退默认（v1..v4 全 0）→ 「VSS总分： 0 / 14」轻度疤痕，不命中。"
},
{
  "slug": "dermatology/salt-alopecia",
  "inputs": {
    "top": "75",
    "back": "0",
    "right": "0",
    "left": "0"
  },
  "expect": [
    "30%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dermatology/scorad-index",
  "inputs": {
    "area": "30",
    "c1": "5",
    "c2": "3"
  },
  "expect": [
    "14.0"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例：expect「使用含2%酮康唑」是默认总分 ≤4（轻度）分支的建议文案，与输入无关。
  "slug": "dermatology/seborrheic-dermatitis",
  "inputs": {
    "d1": "1",
    "d2": "1",
    "d3": "1",
    "d4": "1",
    "d5": "1",
    "d6": "0"
  },
  "expect": [
    "5 分 脂溢性皮炎 / 中度"
  ],
  "ref": "总分 = 1+1+1+1+1+0 = 5 → 落中度分支（≤10）并渲染「5 分 脂溢性皮炎 / 中度」。回退默认（六项全 0）→ 「0 分 脂溢性皮炎 / 轻度」、使用含 2% 酮康唑建议，不命中。"
},
{
  "slug": "dermatology/vasi-vitiligo",
  "inputs": {
    "r1_u": "7",
    "r1_d": "100",
    "r2_u": "0",
    "r2_d": "100",
    "r3_u": "0",
    "r3_d": "100",
    "r4_u": "0",
    "r4_d": "100",
    "r5_u": "0",
    "r5_d": "100"
  },
  "expect": [
    "7.0%"
  ],
  "ref": "auto-restore"
},
{
  // 原为 all_default 弱用例：expect「色素(0-2)」是数据卡片的静态标签，与输入无关。
  // VSS（此处为 3 维 + 高度共 4 项）：色素 0-2、血管 0-3、柔韧 0-5、高度 0-3，满分 13。
  "slug": "dermatology/vss-scar",
  "inputs": {
    "p": "1",
    "v": "2",
    "pl": "3",
    "h": "1"
  },
  "expect": [
    "7 VSS 总分 / 中度（满分13）"
  ],
  "ref": "总分 = 1+2+3+1 = 7 → 落中度分支（≤7）并渲染「7 VSS 总分 / 中度（满分13）」。回退默认（p/v/pl/h 全 0）→ 「0 VSS 总分 / 轻度（满分13）」，不命中。"
},
{
  // 结构性不可注入（保留在 no_inputs 基线）：荧光色卡片由 renderGrid() 生成，疾病说明由 selectFluor(btn,i) 点击渲染；
  // 静态 HTML 无带 id 的表单控件 ⇒ 只能渲染默认空结果（renderGrid 不写 result）。
  "slug": "dermatology/wood-lamp",
  "inputs": {},
  "expect": [
    "颜色加深/对比增强"
  ],
  "ref": "结构性不可注入：荧光色卡片渲染与疾病说明均由 JS（renderGrid/selectFluor 按钮）驱动，静态 HTML 无 input/select/textarea。expect 锚定页面内置的「颜色加深/对比增强」分类名，属保留型常量串。"
},
{
  // 原为 no_inputs 弱用例：expect「72小时内抗病毒治疗」是默认总分 ≤3（低风险）分支的建议文案，与输入无关。
  "slug": "dermatology/zoster-phn",
  "inputs": {
    "age": "2",
    "pain": "2",
    "prodrome": "2",
    "rash": "0",
    "immuno": "0",
    "ophthalmic": "0",
    "dm": "0",
    "sex": "0"
  },
  "expect": [
    "6 分 PHN 中风险"
  ],
  "ref": "PHN 风险分 = 2+2+2+0+0+0+0+0 = 6 → 落中风险分支（≤7）并渲染「6 分 PHN 中风险」。回退默认（八项全 0）→ 「0 分 PHN 低风险」、72 小时抗病毒建议，不命中。"
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
  console.log("==== dermatology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
