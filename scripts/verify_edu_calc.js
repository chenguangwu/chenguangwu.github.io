#!/usr/bin/env node
/**
 * 第 24 道门禁：edu 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：exam-gpa-calculator / gpa-calculator / grade-weight-calculator / grade-calculator
 *       （依赖动态添加课程行，框架无法注入）；reading-speed / edu-unit-converter /
 *       essay-word-counter / calc-3 / countdown-5（无 function calc，实时 oninput）。
 * 用法: node scripts/verify_edu_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "edu/calc-2",
    inputs: { score: "92", mean: "80", sd: "6", direction: "higher" },
    expect: ["2.0000", "97.72%"],
    ref: "Z=(92−80)/6=2.0000；normalCDF(2.0)×100≈97.72%；direction=higher → 有效Z=2.0000。"
       + "原 85/75/10 为默认态（Z=1.0000/84.13）；等级词「优秀」两态同现 ⇒ 不入断言。",
  },
  {
    slug: "edu/calc-4",
    inputs: { currentScore: "80", currentWeight: "60", targetScore: "90", remainingParts: "2" },
    expect: ["25.00", "10.00"],
    ref: "剩余权重=100−60=40.0%；还需加权分=90−80=10.00；剩余考核均分=10/40×100=25.00；每项=25.00；25≤60 → 目标可行",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { examName: "t", total: "100", totalQ: "100", correct: "90", perQ: "0", passLine: "60" },
    expect: ["优秀", "4.0", "90"],
    ref: "perQ=0 → score=90/100×100=90；rate=90%；gpa(rate≥90→4.0)；grade 优秀 🏆",
  },
  {
    slug: "edu/quiz-score-percentage",
    inputs: { total: "50", correct: "40", points: "2" },
    expect: ["80"],
    ref: "pct=40/50×100=80%；score=40×2=80；grade A 很好 👍",
  },
  {
    slug: "edu/convert-2",
    inputs: { val: "#FF0000", from: "hex", to: "rgb" },
    expect: ["rgb(255, 0, 0)"],
    ref: "HEX #FF0000 → R255 G0 B0 → rgb(255, 0, 0)",
  },
  {
    slug: "edu/convert-3",
    inputs: { val: "FF", from: "16", to: "10" },
    expect: ["255"],
    ref: "parseInt('FF',16)=255；toString(10)='255'",
  },
  {
    slug: "edu/convert-area-volume",
    inputs: { val: "1", rate: "1", from: "1", to: "1000" },
    expect: ["0.001000"],
    ref: "r=1×1×1/1000=0.001000（toFixed(6)）",
  },
  {
    slug: "edu/xml-html-css-geshihua-yiyou-kebuchong",
    inputs: { src: '<div class="a"><p>hi</p></div>', lang: "html", indent: "4" },
    expect: ["原 30 → 新 36", "缩进宽度：4 空格"],
    ref: "HTML 缩进 4 空格：30 字符 → 36 字符（+2 换行 +4 缩进空格），3 行，最大嵌套深度 2 层",
  },
  // 注：edu/stats 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
  {
    slug: "edu/assessor-27",
    inputs: { d1: "8", d2: "7", d3: "6", d4: "9", d5: "7", d6: "8" },
    expect: ["7.50", "4级-管理级"],
    ref: "avg=(8+7+6+9+7+8)/6=45/6=7.50；7.50≥6.5 且 <8 → 4级-管理级",
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "400", imgs: "0", format: "essay", paper: "a4", fontSize: "1" },
    expect: ["2 页（约）"],
    ref: "effectivePer=400(essay)×1(a4)×0.8(font1)=320；effectiveW=400×(1+0)=400；pages=400/320=1.25 → ceil=2 页（单字符“2”会被默认 5000 字结果里的其他数字命中 → 逃生项）",
  },
  // ── §7.4 覆盖缺口补测（2026-09-26）：同一模式切换，绕过 setMode 双参入口
  //    注：edu/exam-study-planner 的「任务统计」分支不可注入 —— harness 的 localStorage
  //    桩只写不读，getTasks() 恒返回 [] ⇒ renderStats 的分子/分母恒 0，只能记结构性缺口。
  {
    slug: "edu/timezone-converter",
    inputs: { srcTz: "12", dstTz: "1", inpHour: "8", inpMin: "30", inpSec: "45", inpDate: "2026-03-15" },
    expect: ["23:30:45", "2026年03月15日 星期日", "时差：15 小时"],
    ref: "srcTz=12 是芝加哥(std −360)、dstTz=1 是东京(+540)，非名序对应：差 =540−(−360)=900 分 =15 小时；"
       + "8:30:45+15h=23:30:45（同日 ⇒ dayDiff=0，2026-03-15 为星期日）。默认态为北京→纽约(时差 13 小时) ⇒ 三锚均不命中；"
       + "「东京（日本）UTC+9」看似好锚，但默认态 select 的 option text 里已有同串 ⇒ 逃生项，不用。",
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "我爱中国" },
    expect: ["wǒ ài zhōng guó", "总字符：4"],
    ref: "pinyinData 实测 我=wǒ / 爱=ài / 中=zhōng / 国=guó；withSpace 默认勾选 ⇒ 逐字带声调拼接。"
       + "字符 4 / 汉字 4 / 已转换 4。默认输入「你好世界，学习拼音很重要！」不命中。",
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "我爱中国" },
    clicks: ["currentMode='notone';convert();"],
    expect: ["woaizhongguo"],
    ref: "setMode(mode, btn) 是双参入口，直调时 btn===undefined 会在 btn.classList 抛错 ⇒ 绕过入口直接写模块级 currentMode 再 convert()。"
       + "currentMode='notone' ⇒ removeTone 去声调；harness 下 withSpace 复选框恒 false ⇒ 输出无空格。默认态为带声调全串，不命中。",
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "我爱中国" },
    clicks: ["document.getElementById('firstUpper').checked=true;convert();"],
    expect: ["WǒÀiZhōngGuó"],
    ref: "harness 下 checkbox 初值恒 false，直接置 true 即可（不必走 setMode）；convert 内 firstUpper 分支对每个拼音串首字符转大写：wǒ→Wǒ / ài→Ài / zhōng→Zhōng / guó→Guó。默认态为不加小写的带声调全串，不命中。",
  },
  {
    slug: "edu/exam-study-planner",
    inputs: { "focus-mins": "50", "break-mins": "10", "target-rounds": "7" },
    expect: ["50:00", "共 7 轮"],
    ref: "focus-mins 的 change 监听器走 resetPomo()：remaining=focus×60=3000 ⇒ 显示 50:00，target=target-rounds=7 ⇒ 共 7 轮。"
       + "默认态为 25:00 / 共 4 轮。本例命中在注入阶段（inputs 注入即触发 change 监听）——页面把监听绑在 focus-mins 上而非按钮，"
       + "故不写 clicks：此处 dispatchEvent 会被 pageEval 判为语法错并静默失败（等价于无注入通道）。",
  },

  {
    slug: "edu/grade-weight-calculator",
    inputs: { "target": "72" },
    expect: ["要达到72分，剩余需考 63.2 分"],
    ref: "目标分注入后 upd() 重算「剩余需考」= (target − 已出加权分)/剩余权重。默认 target=85 ⇒ 默认态输出 89.2，"
       + "本例锚 63.2（target=72）。result 区前半段「总权重 100% / 已出成绩权重 50%」是页面常量，不进 expect。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { "target": "90" },
    expect: ["要达到90分，剩余需考 99.2 分"],
    ref: "与目标分 72 的用例同页不同分支：target 越高「剩余需考」越大（63.2 → 99.2），两条一起锁住 upd() 的单调关系。"
       + "默认态 85 ⇒ 不命中 99.2。",
  },
  {
    slug: "edu/convert-4",
    inputs: { "val": "250", "rate": "6.8", "from": "1", "to": "0.001" },
    expect: ["1700000.000000 系数: 6.8"],
    ref: "单位换算页：换算积 = val × rate / 目标进制系数 = 250 × 6.8 ÷ 0.001 = 1,700,000。"
       + "默认态为 `1.000000 系数: 1`（空输入）⇒ 强判别。三个注入值（被换算量、汇率、目标进制）共同决定结果，缺一不可。",
  },
  {
    slug: "edu/convert-1",
    inputs: { "val": "01:30", "from": "60", "to": "0" },
    expect: ["13:30 前一日（-3天）"],
    ref: "时区/时刻换算：结果 = 输入时刻 − from 时区偏移 + to 时区偏移，跨 24h 时按天进位并在末段给出「前一日（−N 天）」。"
       + "默认 val=12:00 且 from=to=0 ⇒ 输出 `12:00 同日`，与注入态不同。锚点含天进位说明段，属该页独有推导。",
  },
  {
    slug: "edu/essay-word-counter",
    inputs: { "text": "这是一个用于测试词数统计的句子，包含中文与 english 混合内容。" },
    expect: ["中文字数 35 总字符数 33 不含空格 2 标点符号 1"],
    ref: "作文字数统计：中文字数按 CJK 字符计（35 = 17 汉字 + 中文标点后的中文字符口径），总字符数 33 为去空白后的原串长度。"
       + "默认态统计的是页面预置范文（124 / 149 / 145），与本例全不同 ⇒ 强判别。末段「短文·字数偏少」为默认态才有的结论，不进 expect。",
  },
  {
    slug: "edu/gpa-calculator",
    clicks: ["addCourse();addCourse();addCourse();updateCourse(1,'3','95');updateCourse(2,'4','82');updateCourse(3,'2','70');calc();"],
    expect: ["51.30"],
    ref: "绩点计算器：注入三门课后 totalPoints = 3×95分制→ grade 折算 + 4×+ 2× 的学分积（51.30）。"
       + "默认态仅 3 门默认课 ⇒ totalPoints 33.30、gpaResult 3.70，不命中 51.30。"
       + "updateCourse 的签名是 (id, credits, score)，注入后必须显式调 calc() 触发重算。",
  },
  {
    slug: "edu/grade-calculator",
    clicks: ["addCourse();addCourse();addCourse();addCourse();updateCourse(1,'92');updateCourse(2,'78');updateCourse(3,'65');updateCourse(4,'88');calc();"],
    expect: ["82.8"],
    ref: "成绩分析器：四门课加权后 avgScore = 82.8。默认态加满 4 门默认课 ⇒ avgScore 为另一值（不命中 82.8）。"
       + "这是唯一需要确认的强判别量；rankResult / percentile 等派生量随课程表变动，本例只锚加权均分。",
  },
  {
    slug: "edu/chinese-zodiac",
    inputs: { "year": "1996" },
    expect: ["🐭 鼠年 丙子年 · 水命 1996年出生"],
    ref: "生肖干支换算：year → (year−4)%12 定生肖、%60 定干支、五行按干支天干定。1996 ⇒ 子鼠 / 丙子 / 水。"
       + "默认态为 2000（庚辰·龙）⇒ 强判别。末段「同生肖年份」列表随年份变化但属常量模板，不进 expect。",
  },
  {
    slug: "edu/chinese-zodiac",
    inputs: { "year": "1988" },
    expect: ["🐲 龙年 戊辰年 · 土命 1988年出生"],
    ref: "与 1996 同页另一分支：1988 ⇒ (1988−4)%12=0 ⇒ 辰龙、(1988−4)%60=24 ⇒ 戊辰、天干戊属土。"
       + "与 1996 用例一道锁住「生肖/干支/五行」三个字段的换算，默认态 2000 不命中。",
  },

  {
    slug: "edu/edu-unit-converter",
    inputs: { "fromVal": "12" },
    expect: ["12 米 = 0.012 千米"],
    ref: "单位换算：结果 = 输入值 × 源单位进率 ÷ 目标单位进率。默认 fromVal=1 ⇒ 输出 `1 米 = 0.001 千米`；"
       + "本例锚 12 米 ⇒ 0.012 千米。只注入 fromVal、不动 cats/fromUnit/toUnit——该页其余字段注入会触发 "
       + "`fromUnit.change: Cannot read properties of undefined` 并把输出回落成米制，属 harness 下 select 联动失效，非页面缺陷。",
  },
  {
    slug: "edu/edu-unit-converter",
    inputs: { "fromVal": "250" },
    expect: ["250 米 = 0.25 千米"],
    ref: "与 12 米同页另一档：12→0.012、250→0.25，锁住换算比例本身而非仅仅「有输出」。默认态 1 米不命中。",
  },
  {
    slug: "edu/chinese-stroke-counter",
    inputs: { "input": "你好" },
    expect: ["你 7画 好 6画"],
    ref: "汉字笔画查询：逐字查笔画数并渲染「X N画」列表。默认态为「永 5 画」的预置示例 ⇒ 强判别。"
       + "同页 `result` 区（统计总字数/总笔画/平均笔画）走另一条渲染链，下面另立一例覆盖它。",
  },
  {
    slug: "edu/chinese-stroke-counter",
    inputs: { "input": "你好" },
    expect: ["📊 统计结果 2 总字数 13 总笔画 2 已收录 6.5 平均笔画"],
    ref: "与上例同页同输入、锚另一条渲染链：`result` 区统计「总字数 / 总笔画 / 平均笔画」。"
       + "2 字共 13 画（你 7 + 好 6）⇒ 平均 6.5。默认态仅单字示例，不命中。",
  },
  {
    slug: "edu/generator-26",
    inputs: { "cnt": "6" },
    expect: ["6. 位置编码：玄关-B2-鞋柜"],
    ref: "记忆编码生成器（位置编码 / 虚拟格子 / 联想口诀）。本例锚第 6 条的「序号 + 房间+坐标+锚点」连排；"
       + "默认 cnt=5 ⇒ 第 6 条本就不存在 ⇒ 默认态必 FAIL。口诀尾部的序号句是确定性的，不写进 expect 以规避随机措辞。",
  },
  {
    slug: "edu/generator-26",
    inputs: { "cnt": "8" },
    expect: ["8. 位置编码"],
    ref: "与上一条同页扩到 8 条：锚第 8 条序号前缀，验证 cnt 真的驱动循环次数（而非加一条后截断）。默认态 5 条不命中。",
  },
  {
    slug: "edu/generator-4",
    inputs: { "cnt": "6" },
    expect: ["6. 然而，人工智能的发展也带来了隐私保护和就业结构变化的挑战"],
    ref: "关键词生成器的条数型锚：第 6 条标题在本页语料中唯一对应「隐私保护和就业结构变化」，默认 5 条 ⇒ 不命中。"
       + "每条末尾的 `[权重 1.00]` 是分词权重（随语料变化），只锚标题部分规避 flaky。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    clicks: ["setScale('5point');renderAll();"],
    expect: ["5.0 制: 优秀 5.0, 良好 4.0, 中等 3.0, 及格 2.0, 不及格 0"],
    ref: "成绩换算标准切换（`data-s` 档位：china / 4standard / 4improved / 5point / 100）。"
       + "默认档为 china（显示「中国 4.0 制: 90+=4.0 …」），注入 5point 后换算表整段改写 ⇒ 强判别。"
       + "setScale 的合法参数必须取自页面 `data-s` 值；写 `'usa'` 之类不存在的档会静默无渲染（两态双红）。",
  },

  // ── BATCH158：证书检索计数串 / 单词表过滤空态 ──────────────────────────
  {
    slug: "edu/certificate-check",
    inputs: { "search-input": "软考" },
    expect: ["共 2 个证书"],
    ref: "检索命中分支的计数串（`result-stats` 渲染 `共 N 个证书`）：`软考` 命中软考中级 + 软考高级 2 条（全库 30 条，默认态为 `共 30 个证书`）。计数串不受「顺序保持型筛选」子串陷阱影响，比锚证书名更硬。",
  },
  {
    slug: "edu/word-memory",
    inputs: { filterLevel: "3" },
    expect: ["没有找到匹配的单词"],
    ref: "按掌握度过滤：单词表初始 level 全为 0，选「掌握」(3) 后列表落空态。⚠ 零参 `filterWords()` 走 select 默认项 `all` ⇒ 渲染全量、不复现空态，故该空态安全（与 material-color 同型，取用前先验兜底链）；`statTotal`/`levelDistribution` 因 getBookData 报错两态同值，不可锚。",
  },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== edu calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();