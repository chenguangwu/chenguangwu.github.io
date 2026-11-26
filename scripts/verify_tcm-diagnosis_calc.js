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
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-diagnosis/constitution-test.html','utf8');document.getElementById('__tbProbe').textContent='CT831 '+((h.indexOf('未答完不能生成体质判定')>=0&&h.indexOf('仍然计算')<0&&h.indexOf('未形成确定体质判定')>=0&&h.indexOf('参考判定：是')>=0)?'OK':'BAD');"],
  "expect": ["CT831 OK"],
  "ref": "第831批：未答完旧实现可按中间值强制计算。现在未答完停算、不再给「仍然计算」；全部答完但各类均未达阈值时输出「未形成确定体质判定」而非主体质。源码守卫断三处关键串。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
},
  {
    "slug": "tcm-diagnosis/pulse-diagnosis",
    "inputs": {
      "searchBox": "abc123测试"
    },
    "expect": [
      "abc123测试\n未找到匹配的脉象"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchBox\":\"abc123测试\"}，输出区含「abc123测试\n未找到匹配的脉象」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "tcm-diagnosis/ten-questions",
    "inputs": {
      "pName": "abc123测试",
      "pAge": "42",
      "pGender": "女"
    },
    "expect": [
      "═════ 患者：abc123测试 性别：女 年龄：42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pName\":\"abc123测试\",\"pAge\":\"42\",\"pGender\":\"女\"}，输出区含「═════ 患者：abc123测试 性别：女 年龄：42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "tcm-diagnosis/ten-questions",
    "inputs": { "pName": "张三" },
    "expect": ["患者：张三 性别：男 年龄：？岁"],
    "ref": "单字段注入（2026-11-05 补 oninput + 事件委托）：仅填姓名，其余留空 ⇒ 300ms 防抖后自动生成记录，未答项统一「（未述）」；默认态为「填写问诊内容后点击…」不出现记录。"
  }
,
{
  "slug": "tcm-diagnosis/formula-matching",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-diagnosis/formula-matching.html','utf8');var i=h.indexOf('天麻钩藤饮');var seg=i>=0?h.slice(i,i+400):'';var ok=seg.indexOf('温服')>=0&&seg.indexOf('用法')<0;document.getElementById('__tbProbe').textContent='FMUSAGE '+(ok?'OK':'BAD');})();"],
  "expect": ["FMUSAGE OK"],
  "ref": "第1320批·天麻钩藤饮字段名错配修复源码形态强锚：原数据对象把用法写成 用法:'温服'，详情读取 f.usage 故用法区空；改为 usage 后修复。旧版无 usage:'温服' ⇒ BAD。"
},
{
  "slug": "tcm-diagnosis/ten-questions",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-diagnosis/ten-questions.html','utf8');var i=h.indexOf('function resetForm(){');var seg=i>=0?h.slice(i,i+560):'';var ok=seg.indexOf(\"getElementById('pGender')\")>=0&&seg.indexOf(\"value='男'\")>=0;document.getElementById('__tbProbe').textContent='TQRESET '+(ok?'OK':'BAD');})();"],
  "expect": ["TQRESET OK"],
  "ref": "第1321批·重置未清性别下拉修复源码形态强锚：原 resetForm 只清文本/单选，pGender 沿用上次值；修复后显式设 pGender='男'。旧版无该重置 ⇒ BAD。"
},
{
  "slug": "tcm-diagnosis/ten-questions",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-diagnosis/ten-questions.html','utf8');var i=h.indexOf('function __tqLive(){');var j=h.indexOf('function __tqPresetView()',i);var seg=(i>=0&&j>i)?h.slice(i,j):'';var ok=seg.indexOf('__tqPresetView();')>=0&&seg.indexOf('generate(true)')<0;document.getElementById('__tbProbe').textContent='TQLIVE '+(ok?'OK':'BAD');})();"],
  "expect": ["TQLIVE OK"],
  "ref": "第197批·输入 300ms 静默生成完整记录修复源码形态强锚：__tqLive 只调用 __tqPresetView 出草稿，不再 auto generate(true)；旧版含 generate(true) ⇒ BAD。"
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

  console.log("==== tcm-diagnosis calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
