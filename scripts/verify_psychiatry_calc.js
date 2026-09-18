#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "psychiatry/aq-autism",
  "inputs": {},
  "expect": [
    "0/50"
  ],
  "ref": "无可注入控件：AQ-50 为 span.q-opt + onclick=pick(i,j) + 内存数组 A 的答题页，页面无任何 <input>/<select>/<textarea>（calc 只读全局数组，不读 DOM），门禁无法注入输入；仅能断言默认态「未完成」分支。见 DEV-PLAN §10.6 缺陷 G"
},
{
  "slug": "psychiatry/asrs-adhd",
  "inputs": {},
  "expect": [
    "0/6"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
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
  "inputs": {},
  "expect": [
    "0/30"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/cage-substance",
  "inputs": {},
  "expect": [
    "0/4"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
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
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/cssrs-suicide",
  "inputs": {},
  "expect": [
    "最近一次实际尝试是否在过去3个月内"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 I/B），同缺陷 G，仅默认态断言（该串由 render() 生成）"
},
{
  "slug": "psychiatry/eat26-eating",
  "inputs": {},
  "expect": [
    "0/26"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/gad7-anxiety",
  "inputs": {},
  "expect": [
    "0/7"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/isi-insomnia",
  "inputs": {},
  "expect": [
    "0/7"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/les-stress",
  "inputs": {},
  "expect": [
    "重大疾病风险约30%"
  ],
  "ref": "无可注入控件：生活事件卡片为 div.e-card + onclick=toggle(i) + 内存对象 sel，页面无表单控件，LCU 全由 sel 累加。仅能断言默认态（LCU=0 落 t<150 分支）"
},
{
  "slug": "psychiatry/lsas-social",
  "inputs": {},
  "expect": [
    "0/48"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/mdq-bipolar",
  "inputs": {},
  "expect": [
    "第一部分0/13"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
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
  "inputs": {},
  "expect": [
    "0/30"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/pcl5-ptsd",
  "inputs": {},
  "expect": [
    "0/20"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/pdss-panic",
  "inputs": {},
  "expect": [
    "2-3次"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/phq15-somatization",
  "inputs": {},
  "expect": [
    "0/15"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
},
{
  "slug": "psychiatry/phq9-depression",
  "inputs": {},
  "expect": [
    "0/9"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
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
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "无可注入控件（span+onclick+内存数组 A），同缺陷 G，仅默认态断言"
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
