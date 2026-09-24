#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tcm-diagnosis/auscultation",
  "clicks": [
    "showItem(ausData.sound.items[1])"
  ],
  "expect": [
    "语声低微，少言而沉静"
  ],
  "ref": "默认仅渲染听声音 12 项的 name+desc；点击项后 showItem() 把「异常表现/辨证提示/病机分析」写入 #result ⇒ 该串仅点击态出现。原 expect「说话声音低沉断续」是列表里的 desc，默认态恒在（常量型逃生项）。"
},
{
  "slug": "tcm-diagnosis/constitution-test",
  "clicks": [
    "constitutions.forEach(function(cc){cc.q.forEach(function(_,j){answers[cc.id+'_'+j]=5;});})",
    "calcScore()"
  ],
  "expect": [
    "转化分：100分（判定：是）"
  ],
  "ref": "27 题（9 体质×3）全部作答 5 分 ⇒ 各体质原始分满分。平和质含反向题得 33 分，气虚质 100 分居首 ⇒ 主体质气虚质、转化分 100。默认态 answers 全空 ⇒ calcScore 因 confirm 未实现而早退，无任何结果（原 expect「1分」是评分按钮文案，零判别力）。"
},
{
  "slug": "tcm-diagnosis/disease-nature",
  "clicks": [
    "currentNature='wind';checkedSym={w1:true,w2:true,w3:true,w4:true};analyze()"
  ],
  "expect": [
    "67%（高度符合，4/6项）"
  ],
  "ref": "选中「风邪」并勾选 w1..w4 共 4 条 ⇒ 4/6 = 66.67 → 67%，等级 ≥60 为「高度符合」。默认态 currentNature 为空 ⇒ analyze 早退，结果区为空。"
},
{
  "slug": "tcm-diagnosis/disease-tracking",
  "inputs": {
    "tongueBody": "淡白"
  },
  "expect": [
    "淡白"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/eight-principles",
  "clicks": [
    "sel.biaoli='li';sel.hanre='re';sel.xushi='shi';sel.yinyang='yang';deduce()"
  ],
  "expect": [
    "里实热证：热结里实，治宜清热泻火/通腑泄热，方如白虎汤、承气汤类。"
  ],
  "ref": "四诊素取 里/热/实/阳 ⇒ 综合证名「里热实证」，synthesize 命中 li+re+shi 分支。默认态 sel 四项全空 ⇒ deduce 早退（原 expect「正虚与邪实并见」是虚实夹杂卡片的 desc，默认恒在）。"
},
{
  "slug": "tcm-diagnosis/etiology-tree",
  "inputs": {},
  "expect": [
    "医生诊治失误致病情加重或变生他病"
  ],
  "ref": "结构性不可注入：页面仅 treeContainer 一个容器，节点由 buildNode() 渲染，交互只有 classList.toggle('expanded')（不进 blob），copyTree() 写剪贴板（桩无实现）⇒ 无任何随输入变化的输出。维持 no_inputs，断言初始化渲染串。"
},
{
  "slug": "tcm-diagnosis/formula-matching",
  "clicks": [
    "showDetail('桂枝汤')"
  ],
  "expect": [
    "解肌发表，调和营卫"
  ],
  "ref": "showDetail('桂枝汤') 把功效/主治/组成/用法/注意写入 #detailModal；列表卡片只渲染 name/cat/source/syndrome/herbs，**不含 effect** ⇒ 默认态无此串。原 expect「全部」是分类 chip 文案（默认恒在，逃生项）。"
},
{
  "slug": "tcm-diagnosis/generator-29",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/meridian-differentiation",
  "clicks": [
    "currentMeridian='lung';showDetail()"
  ],
  "expect": [
    "中府、尺泽、列缺、太渊、鱼际、少商"
  ],
  "ref": "currentMeridian='lung'（手太阴肺经）⇒ showDetail() 输出常用穴位串。卡片只渲染 name+area ⇒ 默认态无。原 expect「肩臂内侧前缘」是卡片 area（默认恒在，逃生项）。"
},
{
  "slug": "tcm-diagnosis/misdiagnosis-training",
  "clicks": [
    "userAnswers=CASES.map(function(c){return c.correct;});showScore()"
  ],
  "expect": [
    "您的中医辨证思维扎实"
  ],
  "ref": "userAnswers 全部填正确答案 ⇒ percent=100 ≥80 ⇒ finalLesson 取「优秀」分支文案（textContent 入 blob）。默认兜底会无参调 selectAnswer() 得「回答错误」，无该文案。"
},
{
  "slug": "tcm-diagnosis/san-jiao-differentiation",
  "clicks": [
    "currentJiao='shang';showDetail()"
  ],
  "expect": [
    "清宫汤送服安宫牛黄丸、至宝丹"
  ],
  "ref": "currentJiao='shang'（上焦证）⇒ showDetail() 列出上焦三证型，含「逆传心包」代表方「清宫汤送服安宫牛黄丸、至宝丹」。默认仅渲染三焦 brief（原 expect「温邪犯肺或逆传心包」即上焦 brief，逃生项）。"
},
{
  "slug": "tcm-diagnosis/self-test-constitution",
  "inputs": {
    "q0": "2"
  },
  "expect": [
    "13"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/spirit-observation",
  "clicks": [
    "checked={e4:true,f4:true,b4:true};analyze()"
  ],
  "expect": [
    "高度警惕：假神提示病情危重"
  ],
  "ref": "e4/f4/b4 是唯一三条 type='fake' 的观察项 ⇒ scores.fake=3 居首 ⇒ maxType='fake' ⇒ 输出假神警示。默认态 checked 为空 ⇒ analyze 早退（原 expect「肌肉不削反应灵敏…」是观察项 label 串联，默认恒在）。"
},
{
  "slug": "tcm-diagnosis/syndrome-element",
  "clicks": [
    "selLoc.heart=true;selNat.qixu=true;derive()"
  ],
  "expect": [
    "保元汤、养心汤"
  ],
  "ref": "病位选「心」+ 病性选「气虚」⇒ 推导证名「心气虚证」，deriveFormula 命中 心∩气虚 分支 ⇒ 保元汤、养心汤。默认 selLoc/selNat 为空（渲染「未选择病位/病性」）⇒ 无结果（原 expect 是病位卡 desc，逃生项）。"
},
{
  "slug": "tcm-diagnosis/tcm-medical-record",
  "inputs": {
    "present": "",
    "analysis": "",
    "formula": "",
    "advice": "",
    "pType": "复诊"
  },
  "expect": [
    "复诊"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/tongue-diagnosis",
  "clicks": [
    "selected.color='red';selected.shape='normal';selected.motion='flexible';selected.coatColor='yellow';selected.coatNature='thick';analyze()"
  ],
  "expect": [
    "邪热炽盛，治宜清热泻火、凉血解毒。"
  ],
  "ref": "红舌+黄苔 ⇒ synthesize 命中「实热证」分支（默认态是淡红舌+白苔+正常/灵活 ⇒ 输出「舌象基本正常或病情轻浅」）。故该串仅注入态出现。"
},
{
  "slug": "tcm-diagnosis/treatment-principle",
  "inputs": {
    "nature": "寒"
  },
  "expect": [
    "用温热性质的方药治疗寒证"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/wei-qi-ying-xue",
  "clicks": [
    "currentLevel='qi';simulate()"
  ],
  "expect": [
    "顺传进展：气分证 → 营分证 → 血分证"
  ],
  "ref": "currentLevel='qi'（气分证，idx=1≠0）⇒ simulate 走非首层分支，输出顺传路径「气分证 → 营分证 → 血分证」。默认仅渲染四层节点名（原 expect「卫分证」即节点名，逃生项）。"
},
{
  "slug": "tcm-diagnosis/zang-fu-differentiation",
  "clicks": [
    "currentZang='heart';showSyndrome(zangFu.heart.syndromes[4])"
  ],
  "expect": [
    "血府逐瘀汤、瓜蒌薤白半夏汤"
  ],
  "ref": "第 5 个证型「心脉痹阻」代表方剂。syndrome 卡片只渲染 name+nature（默认态含「心·心脉痹阻 实证」）⇒ 方剂串仅在 showSyndrome 的 #result 出现（原 expect 锚「心脉痹阻」即卡片名，逃生项）。"
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
  console.log("==== tcm-diagnosis calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
