#!/usr/bin/env node
/**
 * biz 分类关键计算逻辑独立验证（收口批次 C）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_biz_calc.js
 *   node scripts/verify_biz_calc.js checker-8 meeting-cost-calculator
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 服务质量检查（四维度加权 + 响应时间折算 + 投诉超额扣分）────
  {
    slug: "biz/checker-8",
    inputs: {
      certRate: "90", trainRate: "85", uniform: "95", attendance: "90",
      patrol: "92", accessLog: "88", responseTime: "4", logComplete: "90",
      monitorCov: "95", equipOk: "90", comm: "85",
      csat: "88", complaintRes: "86", complaintCnt: "6",
    },
    expect: ["满意度88%/投诉解决86%/月投诉6次"],
    ref: "人员=(90+85+95+90)/4=90；流程=(92+88+80+90)/4=87.5→88（响应 4 分钟→80 分）；"
       + "装备=(95+90+85)/3=90；满意度=(88+86)/2−(6−5)×3=84；"
       + "总分=90×.25+88×.30+90×.20+84×.25=87.9→88 → 良好",
  },

  // ── 会议成本（人·小时计价）────────────────────────────────────
  {
    slug: "biz/meeting-cost-calculator",
    inputs: { duration: "60", attendees: "5", hourlyRate: "100", roomCost: "200" },
    expect: ["¥700.00", "¥11.67", "¥140.00"],
    ref: "hours=60/60=1；人力=1×5×100=500；总成本=500+200=700.00；"
       + "每分钟=700/60=11.666→11.67；人均=700/5=140.00",
  },

  // ── 胜任力评估（岗位权重加权平均）─────────────────────────────
  {
    slug: "biz/assessor-49",
    inputs: { jobType: "tech", d1: "8", d2: "7", d3: "9", d4: "7", d5: "7", d6: "8" },
    expect: ["7.90", "优秀"],
    ref: "技术岗权重 [.30,.10,.25,.10,.15,.10]："
       + "8×.30+7×.10+9×.25+7×.10+7×.15+8×.10=2.4+.7+2.25+.7+1.05+.8=7.90 → ≥7 优秀",
  },

  // ── 单价对比（单位归一化到克后比较）───────────────────────────
  {
    slug: "biz/unit-price-compare",
    inputs: { a_q: "400", a_u: "g", a_p: "10", b_q: "2", b_u: "kg", b_p: "36" },
    expect: ["0.0250 元/g", "1.39 倍", "商品 B（每克更低 0.0180 元）"],
    ref: "A=10/400=0.0250 元/g；B=36/(2×1000)=0.0180 元/g；B 更划算；"
       + "倍数=0.0250/0.0180=1.3889→1.39（独立复算）。"
       + "原注入 500g/12 元 与 1kg/20 元 = 页面默认值 ⇒ 默认态同样命中（all_default）；"
       + "改后默认态 0.0240/0.0200/1.20 倍，与本例三个锚点零交集。",
  },

  // ── 风险矩阵（可能性×影响分级）────────────────────────────────
  {
    slug: "biz/assessor-risk-8",
    inputs: { scene: "production" },
    clicks: [
      "riskData=[{name:'设备点检缺失',likelihood:5,impact:4},{name:'作业许可未落实',likelihood:4,impact:4},{name:'培训不到位',likelihood:2,impact:2}];calc()",
    ],
    expect: ["设备点检缺失", "极高风险-需立即处置", "安全培训/设备点检/作业许可/防护装置/应急演练"],
    ref: "顶层 var riskData 用 clicks 覆写：5×4=20、4×4=16、2×2=4 ⇒ maxRisk=20 ⇒ 极高风险-需立即处置；"
       + "scene=production（非默认 building）⇒ 防控方向=sceneMeasures['production']（独立复算）。"
       + "原注入 scene=building 且沿默认 riskData（3×3=9/2×5=10/3×2=6 ⇒ maxRisk=10）⇒ 默认态同样命中「高风险-需优先整改」（all_default）。"
       + "改后默认态为 高风险-需优先整改 + building 门禁措施，与本例三个锚点零交集。"
       + "注：兜底阶段会无参调用 removeRisk/addRisk 破坏 riskData（删首项、加「新风险点」），"
       + "但 expect 在 clicks 执行后立即判定（阶段 2），早于该破坏 ⇒ 「设备点检缺失」仍可命中。",
  },

  // ── 演示计时（总时长均分到每页）───────────────────────────────
  {
    slug: "biz/presentation-timer",
    inputs: { slideCount: "4", totalMin: "1" },
    expect: ["00:15"],
    ref: "总秒=1×60=60；每页=⌊60/4⌋=15 → fmtTime(15)=00:15",
  },

  // ── 文本折行（字符模式定长切分）───────────────────────────────
  {
    slug: "biz/text-wrap",
    inputs: { input: "abcdefghij", wrapWidth: "4" },
    expect: ["abcd efgh ij"],
    ref: "stub 下「按单词换行」复选框默认未选中 → 字符模式；宽度 4 切分为 abcd/efgh/ij，"
       + "换行符默认 LF（stub 采集时空白归一化为空格）",
  },

  // ── 字符画边框（视觉宽度 + 左右内边距）───────────────────────
  {
    slug: "biz/text-box-drawing",
    inputs: { input: "Hi", style: "single", padX: "1", padY: "0" },
    expect: ["┌────┐", "│ Hi │"],
    ref: "视觉宽=2；内容宽=2+2×1=4 → 顶边 ┌+─×4+┐；内容行 │+空格+Hi+空格+│；"
       + "上下填充 0，底边 └+─×4+┘",
  },

  // ── 文本统计（中英分算 / 句长 / 行长派生量）────────────────────
  {
    slug: "biz/text-stats",
    inputs: { input: "Hello 世界 123" },
    expect: ["平均句长： 3.0 词/句", "平均行长： 12.0 字符/行"],
    ref: "chars=12 / 不含空格=10 / 中文字=2 / 英文词=1 / 数字=3 / 单词=3 / 行数=1 / 句子数=1"
       + "（[。！？!?] 命中 0，回落 text.trim()?1:0）⇒ 句长 3/1=3.0、行长 12/1=12.0。"
       + "默认态为内置示例文本（句长 1.5、行长 26.0）⇒ 不命中。",
  },

  // ── 单位价格比较（元/g 归一 + 划算判定 + 倍数）─────────────────
  {
    slug: "biz/unit-price-compare",
    inputs: { a_p: "15" },
    expect: ["0.0300 元/g", "更划算：商品 A", "1.50 倍"],
    ref: "a=500×1=500 g、b=1×1000=1000 g（kg→1000）；A 单价 15/500=0.0300、B 单价 20/1000=0.0200 元/g"
       + " ⇒ 0.0300>0.0200 取 better=A；倍数 0.0300/0.0200=1.50。"
       + "默认态为 0.0240 / 0.0200、更划算 B、1.20 倍 ⇒ 三项均不命中。",
  },

  // ── Markdown 渲染（表格分支的连排 cell）───────────────────────
  {
    slug: "biz/markdown",
    inputs: { editor: "| 甲 | 乙 |\n|---|---|\n| 24 | 36 |\n| 81 | 90 |" },
    expect: ["甲 乙 24 36 81 90", "36 81"],
    ref: "parseMD 表格分支：表头按 | 切分去空 ⇒ 甲/乙 两个 <th>，数据行 ⇒ 24/36 与 81/90 四个 <td>；"
       + "剥标签后连排为『甲 乙 24 36 81 90』。该串只存在于渲染产物 —— 页面原始文本是"
       + "『| 甲 | 乙 | |---|---| | 24 | 36 | …』，『甲 乙 24』在原文中不连续 ⇒ 非输入回显。"
       + "默认态 textarea 为空、preview 显示占位文案 ⇒ 不命中。",
  },

  // ── 大小写/命名风格转换（getWords 分词 + 连字符拼接）─────────────
  {
    slug: "biz/text-case",
    inputs: { input: "Abc Def" },
    clicks: ["convert('kebab');"],
    expect: ["abc-def"],
    ref: "getWords('Abc Def')：先把 ([a-z])([A-Z]) 插空格 ⇒ ['Abc','Def']，再按 [\\s_-]+ 切分 ⇒ 两词；"
       + "kebab=join('-').toLowerCase() ⇒ 'abc-def'。默认态 case-btn 的示例示例串为 'hello-world' /"
       + " 'HELLO WORLD' 等（.example 文本会进 blob）⇒ 不含 'abc-def'。",
  },
  {
    slug: "biz/text-case",
    inputs: { input: "Abc Def" },
    clicks: ["convert('camel');"],
    expect: ["abcDef"],
    ref: "camel：首词 toLowerCase、后续词首字母大写 ⇒ 'abc' + 'Def' = 'abcDef'（默认示例 'helloWorld' 不命中）。",
  },
  {
    slug: "biz/text-case",
    inputs: { input: "Abc Def" },
    clicks: ["convert('alternate');"],
    expect: ["AbC dEf"],
    ref: "alternate：逐字符翻转大小写、非字母原样输出。up 初值 false：A→true 得 'A'、b→'b'、c→'C'、"
       + "空格原样、D→'d'、e→'E'、f→'f' ⇒ 'AbC dEf'。默认示例 'hElLo WoRlD' 不命中。",
  },
  {
    slug: "biz/text-case",
    inputs: { input: "Abc Def" },
    clicks: ["convert('constant');"],
    expect: ["ABC_DEF"],
    ref: "constant=getWords().join('_').toUpperCase() ⇒ 'ABC_DEF'。默认示例 'HELLO_WORLD' 不命中。",
  },

  // ── 文本行去重（多模式 + 统计派生量）────────────────────────────
  {
    slug: "biz/text-dedup",
    inputs: { input: "bbb\naaa\nbbb\nccc" },
    clicks: ["currentMode='dup-only';convert();"],
    expect: ["bbb"],
    ref: "dup-only：countMap(bbb=2,aaa=1,ccc=1) ⇒ 出现>1 的行 [bbb,bbb]，再按首次出现去重 ⇒ ['bbb']。"
       + "默认态示例为 apple/banana 一类水果行 ⇒ 不含 'bbb'。",
  },
  {
    slug: "biz/text-dedup",
    inputs: { input: "bbb\naaa\nbbb\nccc" },
    clicks: ["currentMode='unique-only';convert();"],
    expect: ["aaa ccc"],
    ref: "unique-only：只保留计数==1 的行 ⇒ ['aaa','ccc'] ⇒ join('\\n')，采集时空白归一 ⇒ 'aaa ccc'。"
       + "首版误锚单字符 'c'（默认态示例行里本就含 c ⇒ 逃生项）。",
  },
  {
    slug: "biz/text-dedup",
    inputs: { input: "bbb\naaa\nbbb\nccc" },
    clicks: ["currentMode='dedup-case';convert();"],
    expect: ["bbb aaa ccc"],
    ref: "dedup-case：以 toLowerCase 为键去重但**输出原行** ⇒ 三行顺序保留 ⇒ 'bbb aaa ccc'（空白归一后）。"
       + "默认态为 apple/banana 的字典序 ⇒ 不命中。",
  },

  // ── 文本行排序（Intl.Collator / 长度 / 数值首数）─────────────────
  {
    slug: "biz/text-sort",
    inputs: { input: "pear\napple\nfig" },
    clicks: ["opt='length-asc';sort();"],
    expect: ["fig pear apple"],
    ref: "length-asc：按 a.length-b.length ⇒ fig(3) < pear(4) < apple(5) ⇒ 'fig pear apple'（空白归一后）。"
       + "默认态 opt='asc' 按 Collator 排得 apple/fig/pear ⇒ 不命中。",
  },
  {
    slug: "biz/text-sort",
    inputs: { input: "item 10\nitem 9\nitem 2" },
    clicks: ["opt='num-asc';sort();"],
    expect: ["item 2 item 9 item 10"],
    ref: "num-asc：正则 -?\\d+(\\.\\d+)? 取**首个**数parseFloat ⇒ 10/9/2，升序 ⇒ 2,9,10。"
       + "默认态为字典序 ⇒ 不命中。",
  },
  {
    slug: "biz/text-sort",
    inputs: { input: "pear\napple\nfig" },
    clicks: ["opt='length-desc';sort();"],
    expect: ["apple pear fig"],
    ref: "length-desc：长度降序 ⇒ apple(5) > pear(4) > fig(3)。与 length-asc 的锚互为反向，"
       + "可防「排序根本没生效」的假通过。",
  },

  // ── 邮箱提取（锚必须落在「结果区连排」而非输入回显）───────────────
  {
    slug: "biz/text-extract-emails",
    inputs: { input: "联系 a1@toolbox.com 或 b2@mail.org 咨询" },
    clicks: ["extractEmails();"],
    expect: ["a1@toolbox.com 复制 b2@mail.org 复制"],
    ref: "正则 /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/g 命中 2 处 ⇒ 结果区每封邮箱渲染成"
       + " '<span class=email>…</span><button>复制</button>'，剥标签后连排为『a1@toolbox.com 复制 b2@mail.org 复制』。"
       + "⚠ 该串刻意带后缀『 复制』：邮箱原文就在 textarea 里（回显必命中），只有加上结果区独有的按钮文案才测到提取；"
       + "直接锚 'a1@toolbox.com' 属伪锚。默认态 input 为空 ⇒ 早返回、result 为空 ⇒ 不命中。",
  },

  // ── URL 提取（分隔词打断 ⇒ 结果连排非输入子串）──────────────────
  {
    slug: "biz/text-extract-urls",
    inputs: { input: "见 http://alpha.com 与 https://beta.org 结束" },
    expect: ["http://alpha.com https://beta.org"],
    ref: "两条 URL 均未带协议头 ⇒ 补成 http://alpha.com / http…（beta 已是 https）；默认分隔符 join 空格"
       + " ⇒ 结果 textContent 为『http://alpha.com https://beta.org』。原文里两段之间是『与』，"
       + "该串在输入中不连续 ⇒ 非回显。默认态 textarea 为示例文本 ⇒ 不命中。",
  },

  // ── 文本分割（段数标签只随注入出现）────────────────────────────
  {
    slug: "biz/text-split",
    inputs: { input: "apple,banana,cherry" },
    clicks: ["split();"],
    expect: ["（共 3 段）"],
    ref: "mode 默认 delimiter、分隔符 ',' ⇒ 'apple,banana,cherry'.split(',') = 3 段；trimEach/skipEmpty 默认勾选但不影响。"
       + "countLabel 写入『（共 3 段）』。默认态 textarea 为 5 段示例文本，countLabel 为空串 ⇒ 不命中。"
       + "⚠ 另一候选锚 '3 cherry'（序号+段内容）在默认态示例里同样存在 ⇒ 逃生项，已弃用。",
  },
];

// ---------------------------------------------------------------- main
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
  console.log("==== biz calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();