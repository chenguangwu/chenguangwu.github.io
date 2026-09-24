#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "psychiatry/aq-autism",
  "clicks": [ "pick(0,2)", "pick(1,0)", "pick(2,2)", "pick(3,0)", "pick(4,0)", "pick(5,0)", "pick(6,0)",
    "pick(7,2)", "pick(8,0)", "pick(9,2)", "pick(10,2)", "pick(11,0)", "pick(12,0)", "pick(13,2)", "pick(14,2)",
    "pick(15,0)", "pick(16,2)", "pick(17,0)", "pick(18,0)", "pick(19,0)", "pick(20,0)", "pick(21,0)",
    "pick(22,0)", "pick(23,2)", "pick(24,2)", "pick(25,0)", "pick(26,2)", "pick(27,2)", "pick(28,2)",
    "pick(29,2)", "pick(30,2)", "pick(31,2)", "pick(32,0)", "pick(33,2)", "pick(34,0)", "pick(35,2)",
    "pick(36,2)", "pick(37,2)", "pick(38,0)", "pick(39,2)", "pick(40,0)", "pick(41,0)", "pick(42,0)",
    "pick(43,2)", "pick(44,0)", "pick(45,0)", "pick(46,2)", "pick(47,2)", "pick(48,2)", "pick(49,2)"],
  "expect": [
    "临床显著 总分 50 / 50", "≥32 临床临界32"
  ],
  "ref": "AQ-50 五十项逐项点选（FWD 项选「完全同意」j=0、其余选「稍微不同意」j=2）：FWD 24 项 + 非 FWD 26 项各得 1 分 ⇒ AQ 总分 50/50 ⇒ 落 total>31 分支「临床显著」；五个维度分卡 社交技巧/注意力转换/注意细节/沟通/想象力 均 10/10（各维度均为 10 项，全得分）。默认（未作答）只渲染「已作答 0/50 项」提示，与注入态零交集。in-clicks 通道：via=click"
},
{
  "slug": "psychiatry/asrs-adhd",
  "clicks": [ "pick(0,4)", "pick(1,4)", "pick(2,4)", "pick(3,4)", "pick(4,4)", "pick(5,4)"],
  "expect": [
    "筛查阳性 阳性项 6/6 · 总分 24/24", "≥4 阳性标准4"
  ],
  "ref": "ASRS 六项全选「非常频繁」j=4（SH 阈值 [3,4]/[3,4]/[3,4]/[3,4]/[2,3,4]/[2,3,4] 全部命中）⇒ 阳性项 6/6 ≥4 ⇒「筛查阳性」；总分 6×4 = 24/24。默认态为「筛查阴性」+ 提示框，零交集。via=click"
},
{
  "slug": "psychiatry/assessor-risk-5",
  "inputs": {
    "ide0": "0",
    "ide1": "0",
    "ide2": "1",
    "ide3": "0",
    "ide4": "0",
    "beh0": "0",
    "beh1": "0",
    "beh2": "0"
  },
  "expect": [
    "中风险",
    "3级（0=无）",
    "需一周内精神科评估，建立安全计划，定期随访，关注情绪变化"
  ],
  "ref": "C-SSRS 自杀意念第3项=是（其余=否）→ maxIdeation=2 → ideationLevels[3]，风险等级落 maxIdeation>=2 分支=「中风险」；表格「自杀意念最高级别」=maxIdeation+1=3级；处置文案取该分支原文。默认（全否）为「极低风险」/0级且不显示危机热线，注入与默认输出零交集"
},
{
  "slug": "psychiatry/bis11-impulse",
  "clicks": [ "pick(0,0)", "pick(1,3)", "pick(2,3)", "pick(3,3)", "pick(4,3)", "pick(5,3)", "pick(6,0)",
    "pick(7,0)", "pick(8,0)", "pick(9,0)", "pick(10,3)", "pick(11,0)", "pick(12,0)", "pick(13,3)", "pick(14,0)",
    "pick(15,3)", "pick(16,3)", "pick(17,3)", "pick(18,3)", "pick(19,0)", "pick(20,3)", "pick(21,3)",
    "pick(22,3)", "pick(23,3)", "pick(24,3)", "pick(25,3)", "pick(26,3)", "pick(27,3)", "pick(28,0)",
    "pick(29,0)"],
  "expect": [
    "极高 总分 120 / 120", "48 非计划(12-48)"
  ],
  "ref": "BIS-11 三十项按反向/正向分别取满分选项（REV 11 项选 j=0 ⇒ 5-(0+1)=4；其余 19 项选 j=3 ⇒ 3+1=4）⇒ 总分 120/120 ⇒ 落 total>95 分支「极高」；三维度分卡 注意 28/运动 44/非计划 48 均为各自满分。默认（未作答）为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/cage-substance",
  "clicks": [ "pick(0,0)", "pick(1,0)", "pick(2,0)", "pick(3,0)"],
  "expect": [
    "筛查阳性 总分 4 / 4", "≥2 阳性标准2"
  ],
  "ref": "CAGE 四项全选「是」j=0 ⇒ yes=4 ≥2 ⇒「筛查阳性」；总分 4/4、「是」项数 4。默认态为提示框（未作答），零交集。via=click"
},
{
  "slug": "psychiatry/calc-1",
  "inputs": {
    "q0": "3",
    "q1": "3",
    "q2": "2",
    "q3": "2",
    "q4": "1",
    "q5": "2",
    "q6": "2",
    "q7": "1",
    "q8": "2"
  },
  "expect": [
    "中重度抑郁",
    "建议尽快寻求专业心理或精神科帮助"
  ],
  "ref": "PHQ-9 九项=3,3,2,2,1,2,2,1,2 → 总分 18（14<18≤19）→ classify 落「中重度抑郁」；q8=2>0 触发第9项自伤念头警示文案。默认态总分 0 落「无或极轻微抑郁」且无警示，零交集"
},
{
  "slug": "psychiatry/cdrisc-resilience",
  "clicks": [ "pick(0,4)", "pick(1,4)", "pick(2,4)", "pick(3,4)", "pick(4,4)", "pick(5,4)", "pick(6,4)",
    "pick(7,4)", "pick(8,4)", "pick(9,4)"],
  "expect": [
    "较高 总分 40 / 40", "4.0 条目均分"
  ],
  "ref": "CD-RISC-10 十项全选「几乎总是(4)」⇒ 总分 40/40 ⇒ 落 total>29 分支「较高」；条目均分 (40/10).toFixed(1) = 4.0、韧性水平 100%。默认态为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/cssrs-suicide",
  "clicks": [ "pickI(0,0)", "pickI(1,0)", "pickI(2,0)", "pickI(3,0)", "pickI(4,0)", "pickB(0,0)", "pickB(1,0)",
    "pickB(2,0)", "pickB(3,0)", "pickR(0)"],
  "expect": [
    "极高危", "最高意念等级 5/5 · 自杀行为：有"
  ],
  "ref": "C-SSRS 五项目杀意念 + 四项自杀行为全选「是」+ 最近尝试「是(0)」⇒ doneI=5、doneB=4、B[3]=0 且 RECENT=0 ⇒ 落 anyBeh 且 actualAttempt&&recent 分支「极高危」（该分支要求「任一行为=是 + 第4项实际尝试=是 + 近3个月=是」三条同时成立，默认态不可达）；hotline 块同时出现。默认态为提示框「请完成全部问题（含最近尝试时间）」，零交集。via=click"
},
{
  "slug": "psychiatry/eat26-eating",
  "clicks": [ "pick(0,5)", "pick(1,5)", "pick(2,5)", "pick(3,5)", "pick(4,5)", "pick(5,5)", "pick(6,5)",
    "pick(7,0)", "pick(8,5)", "pick(9,5)", "pick(10,5)", "pick(11,5)", "pick(12,0)", "pick(13,5)", "pick(14,5)",
    "pick(15,5)", "pick(16,5)", "pick(17,5)", "pick(18,5)", "pick(19,5)", "pick(20,5)", "pick(21,5)",
    "pick(22,5)", "pick(23,5)", "pick(24,0)", "pick(25,5)"],
  "expect": [
    "高风险 总分 78 / 78", "≥20 临界值20"
  ],
  "ref": "EAT-26 二十六项按反向/正向分别取满分（REV_IDX 3 项选 j=0 ⇒ REV[0]=3；其余 23 项选 j=5 ⇒ NORM[5]=3）⇒ 总分 78/78 ≥20 ⇒「高风险」；A[3]、A[8] 均 5 ≥3 ⇒ 追加暴食/催吐就医提示。默认（未作答）为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/gad7-anxiety",
  "clicks": [ "pick(0,3)", "pick(1,3)", "pick(2,3)", "pick(3,3)", "pick(4,3)", "pick(5,3)", "pick(6,3)"],
  "expect": [
    "重度焦虑 总分 21 / 21", "100% 严重度占比"
  ],
  "ref": "GAD-7 七项全选「几乎每天」j=3 ⇒ 总分 21/21 ⇒ 落 total>14 分支「重度焦虑」；严重度占比 round(21/21*100) = 100%。默认态为「已作答 0/7 项」提示，零交集。via=click"
},
{
  "slug": "psychiatry/isi-insomnia",
  "clicks": [ "pick(0,4)", "pick(1,4)", "pick(2,4)", "pick(3,4)", "pick(4,4)", "pick(5,4)", "pick(6,4)"],
  "expect": [
    "重度失眠 总分 28 / 28", "100% 严重度占比"
  ],
  "ref": "ISI 七项全选最重选项 j=4 ⇒ 总分 28/28 ⇒ 落 total>21 分支「重度失眠」；严重度占比 round(28/28*100) = 100%。注意 #quiz 内选项文本含「重度」二字，故 expect 必须与「失眠 总分 28 / 28」绑成连续串。默认态为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/les-stress",
  "clicks": [ "toggle(0)", "toggle(1)", "toggle(2)", "toggle(3)", "toggle(4)", "toggle(5)"],
  "expect": [
    "高风险 LCU总分 417 · 事件数 6", "约80% 疾病风险"
  ],
  "ref": "LES 42 项生活事件勾选前六项（配偶死亡100 + 离婚73 + 夫妻分居65 + 判刑或入狱63 + 亲密家庭成员死亡63 + 个人受伤或患病53 = 417 LCU）⇒ 417 ≥300 ⇒ 落 t>=300 分支「高风险」；卡面 LCU总分 417、勾选事件数 6、疾病风险 约80%。默认（未勾选）t=0 为「低风险 / 约30%」，跨档且零交集。via=click"
},
{
  "slug": "psychiatry/lsas-social",
  "clicks": [ "pickF(0,3)", "pickF(1,3)", "pickF(2,3)", "pickF(3,3)", "pickF(4,3)", "pickF(5,3)", "pickF(6,3)",
    "pickF(7,3)", "pickF(8,3)", "pickF(9,3)", "pickF(10,3)", "pickF(11,3)", "pickF(12,3)", "pickF(13,3)",
    "pickF(14,3)", "pickF(15,3)", "pickF(16,3)", "pickF(17,3)", "pickF(18,3)", "pickF(19,3)", "pickF(20,3)",
    "pickF(21,3)", "pickF(22,3)", "pickF(23,3)", "pickV(0,3)", "pickV(1,3)", "pickV(2,3)", "pickV(3,3)",
    "pickV(4,3)", "pickV(5,3)", "pickV(6,3)", "pickV(7,3)", "pickV(8,3)", "pickV(9,3)", "pickV(10,3)",
    "pickV(11,3)", "pickV(12,3)", "pickV(13,3)", "pickV(14,3)", "pickV(15,3)", "pickV(16,3)", "pickV(17,3)",
    "pickV(18,3)", "pickV(19,3)", "pickV(20,3)", "pickV(21,3)", "pickV(22,3)", "pickV(23,3)"],
  "expect": [
    "极重度 总分 144 / 144", "78 表现型"
  ],
  "ref": "LSAS 24 项「恐惧/焦虑」与「回避」双列全选最高档 j=3 ⇒ 恐惧 72 + 回避 72 = 总分 144/144 ⇒ 落 total>90 分支「极重度」；表现型 13×3×2 = 78、社交型 11×3×2 = 66。默认态为「已完成 0/48 个评分」提示，零交集。via=click"
},
{
  "slug": "psychiatry/mdq-bipolar",
  "clicks": [ "pick(0,0)", "pick(1,0)", "pick(2,0)", "pick(3,0)", "pick(4,0)", "pick(5,0)", "pick(6,0)",
    "pick(7,0)", "pick(8,0)", "pick(9,0)", "pick(10,0)", "pick(11,0)", "pick(12,0)", "pickP2(0)", "pickP3(2)"],
  "expect": [
    "筛查阳性", "三条标准同时满足"
  ],
  "ref": "MDQ 三部分全答阳性：第一部分 13 项全选「是」(yes=13≥7)、第二部分选「是」(P2=0)、第三部分选「中度问题」(P3=2≥2) ⇒ screen=true「筛查阳性」。注意三条「满足/不满足」卡面文案里「不满足」**包含**「满足」子串，故 expect 不可锚「满足 标准N」，改锚结论串「三条标准同时满足」。默认态为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/mmpi2-personality",
  "inputs": {
    "sc0": "75",
    "sc1": "68"
  },
  "expect": [
    "多个临床量表达到临床显著升高(T≥65)",
    "75 临床显著"
  ],
  "ref": "MMPI-2 十量表 T 分（动态 id sc0..sc9 由 buildInputs 模板生成，默认 value=50）：Hs=75、D=68，其余 50 → v≥65 的升高量表数=2 → 触发「多个临床量表达到临床显著升高」警示；grade(75)=显著升高、grade(68)=临床显著，最高量表 Hs、最高 T 分 75。原用例 inputs 为 JS 模板残骸键（纯回显垃圾），本次改为真实动态 id"
},
{
  "slug": "psychiatry/panss-schizophrenia",
  "clicks": [ "pick(0,7)", "pick(1,7)", "pick(2,7)", "pick(3,7)", "pick(4,7)", "pick(5,7)", "pick(6,7)",
    "pick(7,7)", "pick(8,7)", "pick(9,7)", "pick(10,7)", "pick(11,7)", "pick(12,7)", "pick(13,7)", "pick(14,7)",
    "pick(15,7)", "pick(16,7)", "pick(17,7)", "pick(18,7)", "pick(19,7)", "pick(20,7)", "pick(21,7)",
    "pick(22,7)", "pick(23,7)", "pick(24,7)", "pick(25,7)", "pick(26,7)", "pick(27,7)", "pick(28,7)",
    "pick(29,7)"],
  "expect": [
    "显著/重度 总分 210 / 210", "+0 复合指数P-N"
  ],
  "ref": "PANSS 三十项（P 7 + N 7 + G 16）全评 7 分 ⇒ 总分 210/210 ⇒ 落 total>95 分支「显著/重度」；阳性 P 49/49、阴性 N 49/49、一般 G 112/112、复合指数 P-N = 0 显示为「+0」。默认（0=未评）为「已评定 0/30 项」提示，零交集。via=click"
},
{
  "slug": "psychiatry/pcl5-ptsd",
  "clicks": [ "pick(0,4)", "pick(1,4)", "pick(2,4)", "pick(3,4)", "pick(4,4)", "pick(5,4)", "pick(6,4)",
    "pick(7,4)", "pick(8,4)", "pick(9,4)", "pick(10,4)", "pick(11,4)", "pick(12,4)", "pick(13,4)", "pick(14,4)",
    "pick(15,4)", "pick(16,4)", "pick(17,4)", "pick(18,4)", "pick(19,4)"],
  "expect": [
    "重度 总分 80 / 80", "DSM-5 症状群筛查：符合"
  ],
  "ref": "PCL-5 二十项全选「极其严重」j=4 ⇒ 总分 80/80 ⇒ 落 total>35 分支「重度」；四个症状群 B 20/C 8/D 28/E 24 均满分 ⇒ DSM-5 症状群筛查判定「符合」。默认态为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/pdss-panic",
  "clicks": [ "pick(0,4)", "pick(1,4)", "pick(2,4)", "pick(3,4)", "pick(4,4)", "pick(5,4)", "pick(6,4)"],
  "expect": [
    "重度 总分 28 / 28 · 均分 4.0", "≥8 临界值8"
  ],
  "ref": "PDSS 七项全选最重档 j=4 ⇒ 总分 28/28 ⇒ 落 total>13 分支「重度」；均分 (28/7).toFixed(1) = 4.0。注意 #quiz 第 1 题选项含「2-3次」等文本，旧 expect 正是该静态串（默认全量渲染即命中＝逃生项），本次改锚结果卡。默认态为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/phq15-somatization",
  "clicks": [ "pick(0,2)", "pick(1,2)", "pick(2,2)", "pick(3,2)", "pick(4,2)", "pick(5,2)", "pick(6,2)",
    "pick(7,2)", "pick(8,2)", "pick(9,2)", "pick(10,2)", "pick(11,2)", "pick(12,2)", "pick(13,2)", "pick(14,2)"],
  "expect": [
    "高 总分 30 / 30", "≥10 中重度临界10"
  ],
  "ref": "PHQ-15 十五项全选「很多困扰」j=2 ⇒ 总分 30/30 ⇒ 落 total>14 分支「高」；中重度临界卡显示 ≥10。默认态为提示框，零交集。via=click"
},
{
  "slug": "psychiatry/phq9-depression",
  "clicks": [ "pick(0,3)", "pick(1,3)", "pick(2,3)", "pick(3,3)", "pick(4,3)", "pick(5,3)", "pick(6,3)",
    "pick(7,3)", "pick(8,3)"],
  "expect": [
    "重度抑郁 总分 27 / 27", "DSM-5 重性抑郁发作筛查：符合"
  ],
  "ref": "PHQ-9 九项全选「几乎每天」j=3 ⇒ 总分 27/27 ⇒ 落 total>19 分支「重度抑郁」；症状条目(≥2) = 9 ⇒ DSM-5 重性抑郁发作筛查「符合」；第 9 题自伤念头得分 ⇒ 追加危机提示。默认态为「已作答 0/9 项」提示，零交集。via=click"
},
{
  "slug": "psychiatry/rater-23",
  "inputs": {
    "f0": "3", "f1": "3", "f2": "3", "f3": "3", "f4": "3", "f5": "3", "f6": "3", "f7": "3",
    "f8": "3", "f9": "3", "f10": "3", "f11": "3", "f12": "3", "f13": "3", "f14": "3", "f15": "3",
    "f16": "3", "f17": "3", "f18": "3", "f19": "3", "f20": "3", "f21": "3", "f22": "3", "f23": "3",
    "a0": "3", "a1": "3", "a2": "3", "a3": "3", "a4": "3", "a5": "3", "a6": "3", "a7": "3",
    "a8": "3", "a9": "3", "a10": "3", "a11": "3", "a12": "3", "a13": "3", "a14": "3", "a15": "3",
    "a16": "3", "a17": "3", "a18": "3", "a19": "3", "a20": "3", "a21": "3", "a22": "3", "a23": "3"
  },
  "expect": [
    "重度社交焦虑",
    "144/144",
    "78/78"
  ],
  "ref": "LSAS 24 项（表演型 13 + 社交互动型 11，动态 id f_i/a_i 由 buildList 模板生成，浏览器默认 selected=2）：全部取 3 → 恐惧 72 + 回避 72 = 144 → 落 total≥105 分支「重度社交焦虑」；表演型 13×3×2=78/78、社交互动型 11×3×2=66/66、总分 144/144。默认态（全 2）为 96 分「显著社交焦虑」，零交集"
},
{
  "slug": "psychiatry/rater-24",
  "inputs": {
    "q0": "4", "q1": "4", "q2": "4", "q3": "4", "q4": "4", "q5": "4", "q6": "4", "q7": "4",
    "q8": "4", "q9": "4", "q10": "4", "q11": "4", "q12": "4", "q13": "4", "q14": "4", "q15": "4",
    "q16": "4", "q17": "4", "q18": "4", "q19": "4", "q20": "4", "q21": "4", "q22": "4", "q23": "4",
    "q24": "4"
  },
  "expect": [
    "高心理韧性",
    "100/100",
    "4.00/4.0"
  ],
  "ref": "CD-RISC 25 项（动态 id q0..q24 由 buildList 模板生成，浏览器默认 selected=2）：全部 4 → 总分 100/100（max=25×4）→ 落 total≥80 分支「高心理韧性」；均分 (100/25).toFixed(2)=4.00/4.0；得分率 100%。默认态（全 2）=50 分「中等心理韧性」、均分 2.00/4.0，零交集"
},
{
  "slug": "psychiatry/self-assess-4",
  "inputs": {
    "q0": "4",
    "q1": "3",
    "q2": "2",
    "q3": "2",
    "q4": "3",
    "q5": "3"
  },
  "expect": [
    "高度疑似成人ADHD",
    "阳性项数：6/6",
    "混合型表现"
  ],
  "ref": "ASRS-v1.1 六项（动态 id q0..q5，positiveFrom 前4项=2、后2项=3）：4,3,2,2,3,3 → 阳性项 6（≥5）→「高度疑似成人ADHD」；注意力缺陷 4/4 + 多动冲动 2/2 均阳性 → typeDesc「混合型表现」。原用例 inputs 为 JS 模板残骸键（纯回显垃圾），本次改为真实动态 id。默认态全 0 为「筛查阴性」，零交集"
},
{
  "slug": "psychiatry/ybocs-ocd",
  "clicks": [ "pick(0,4)", "pick(1,4)", "pick(2,4)", "pick(3,4)", "pick(4,4)", "pick(5,4)", "pick(6,4)",
    "pick(7,4)", "pick(8,4)", "pick(9,4)"],
  "expect": [
    "极重度 总分 40 / 40", "20 强迫行为(0-20)"
  ],
  "ref": "Y-BOCS 十项（强迫思维 5 + 强迫行为 5）全选「极重度」j=4 ⇒ 总分 40/40 ⇒ 落 total>31 分支「极重度」；强迫思维 20/20、强迫行为 20/20。默认态为「已作答 0/10 项」提示，零交集。via=click"
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
  console.log("==== psychiatry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
