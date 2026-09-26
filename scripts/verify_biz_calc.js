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
  {
    slug: 'biz/text-extract-numbers',
    inputs: { input: "单价 12.50 元，数量 30 件" },
    checkIds: ["int", "decimal", "negative", "scientific", "sum"],
    expect: ["12.50 30", "21.25"],
    ref: "默认勾 int/decimal/negative/scientific/sum：decimal 先取 12.50，int+negative 的 12 与之重叠被去重叠逻辑剔除、30 保留 ⇒ finalMatches=['12.50','30']；sum=42.5、avg=(42.5/2).toFixed(2)='21.25'。"
       + "result 连排 '12.50 30' 在原文里不连续（被『，』隔开）⇒ 非回显。默认态剥掉 checkIds ⇒ patterns 为空 ⇒ result 空、avg 为 '-' ⇒ 不命中。"
       + "⚠ 本页 extract() 内 8 处 getElementById(...).checked，桩里缺元素即抛错中断（count 恒为静态 0、结果区永不刷新）—— 只写 inputs 会误判为『页面无功能』，必须显式 checkIds 声明全部默认勾选项。",
  },
  {
    slug: 'biz/text-extract-dates',
    inputs: { input: "签署于 2026-03-09，复核 2027/4/2 完成" },
    checkIds: ["iso", "slash", "dot", "zh", "us", "eu", "time", "dedup"],
    expect: ["2026-03-09 2027/4/2"],
    ref: "默认 6 种格式 + time/dedup 全勾（normalize 未勾 ⇒ 原样输出不归一）：iso 命中 2026-03-09、slash 命中 2027/4/2，dot/zh/us/eu 无匹配。"
       + "result 连排 '2026-03-09 2027/4/2' 原文被『，』隔开 ⇒ 非回显。默认态剥掉 checkIds ⇒ 所有格式跳过 ⇒ result 为『请输入文本...』、count=0 ⇒ 不命中。"
       + "⚠ 同 text-extract-numbers：缺 checkIds 时 extract() 在首个 getElementById(fmt).checked 处抛错，表现与『无匹配』完全一致，极易误判。",
  },
  {
    slug: 'biz/text-reverse',
    inputs: { input: "Alpha 7" },
    expect: ["7 ahplA"],
    ref: "currentMode 默认 'full'：Array.from('Alpha 7').reverse().join('') = '7 ahplA'（keepNewline 默认勾、reverseCase 默认未勾）。"
       + "默认态 result 是示例文本 'Hello World' 的反转（集具工 xoBlooT dlroW olleH）⇒ 不命中。",
  },
  {
    slug: 'biz/text-reverse',
    inputs: { input: "Beta gamma 9" },
    clicks: ["currentMode='words';convert();"],
    expect: ["9 gamma Beta"],
    ref: "setMode(btn) 是『状态变量 + 按钮』双参入口（btn 只做 classList 切换），直调会因 btn 为 undefined 抛错 ⇒ 绕过它直写 currentMode 再调 convert()："
       + "'Beta gamma 9'.split(/(\\s+)/) = ['Beta',' ','gamma',' ','9']，reverse 后 join 得 '9 gamma Beta'。"
       + "默认态 currentMode='full' ⇒ 输出为整串反转 '9 agnammaB' ⇒ 不命中。",
  },
  {
    slug: 'biz/text-extract-ips',
    inputs: { input: "客户端 10.0.0.5 与 8.8.8.8 连接" },
    checkIds: ["ipv4", "ipv6", "validate", "dedup"],
    expect: ["10.0.0.5 8.8.8.8"],
    ref: "默认勾 ipv4/ipv6/validate/dedup（private/public 未勾 ⇒ 不过滤）⇒ text.match(IPV4_RE) 得 10.0.0.5、8.8.8.8，ipv6 无匹配。"
       + "result 连排 '10.0.0.5 8.8.8.8' 原文被『与』隔开 ⇒ 非回显。默认态剥掉 checkIds ⇒ 8 处 getElementById(...).checked 读全为 false ⇒ matches 空、result 空 ⇒ 不命中。",
  },
  {
    slug: 'biz/text-extract-ips',
    inputs: { input: "出口 8.8.8.8 与 1.1.1.1 中继，内网 10.0.0.5 旁路" },
    checkIds: ["ipv4", "validate", "dedup", "public"],
    expect: ["8.8.8.8 1.1.1.1"],
    ref: "只勾 public ⇒ isPrivate 过滤掉 10.0.0.5，保留 8.8.8.8、1.1.1.1 两个非私有地址；连排 '8.8.8.8 1.1.1.1' 原文被『与』隔开 ⇒ 非回显。"
       + "⚠ 单值锚（只留一个 IP 时）会与输入回显同串 ⇒ 伪锚，必须用『两 IP 连排』同时证明过滤与提取。默认态剥掉 checkIds ⇒ result 空。",
  },
  {
    slug: 'biz/text-reverse-lines',
    inputs: { input: "alpha\nbeta\ngamma" },
    expect: ["gamma beta alpha"],
    ref: "默认只勾 skipEmpty（trimEach/reverseChars/keepFirst/keepLast 未勾）⇒ lines 全量参与，reverse() 内 toReverse.reverse() ⇒ 'alpha\\nbeta\\ngamma' → 'gamma\\nbeta\\nalpha'。"
       + "result 连排 'gamma beta alpha' 原文顺序相反 ⇒ 非回显。默认态 result 是示例文本的行序反转 ⇒ 不命中。",
  },
  {
    slug: 'biz/char-frequency',
    inputs: { input: "Aa a" },
    expect: ["a 2 (66.67%)", "A 1 (33.33%)"],
    ref: "默认 ignoreCase 未置 value='1' ⇒ 大小写区分。'Aa a' 统计 A=1/a=2/' '=1（空格在 currentFilter='all' 下被跳过计数但计入 total=4）。"
       + "maxCount=2/total=4 ⇒ a：2/4=66.67%，A：1/4=33.33%。默认态是长中文示例的 23 字符统计串 ⇒ 不命中。",
  },
  {
    slug: 'biz/char-frequency',
    inputs: { input: "Aa a" },
    clicks: ["document.getElementById('ignoreCase').value='1';analyze();"],
    expect: ["a 3 (100.00%)"],
    ref: "ignoreCase 读的是 `.value === '1'`（非 `.checked`）⇒ 必须写 value 才生效。归并后 map.size=1、total=3 ⇒ 唯一字符 a 占 100.00%。"
       + "与上一例同输入同 total 但占比不同（66.67% / 100.00%）⇒ 判别 ignoreCase 分支真的生效。默认态无 'a 3' 串 ⇒ 不命中。",
  },
  {
    slug: 'biz/fullwidth-halfwidth',
    inputs: { input: "ＡＢＣ　１２３" },
    checkIds: ["ascii", "space"],
    expect: ["ABC 123"],
    ref: "默认 currentMode='half'、ascii/space 勾（kana 未勾不影响）。全角字母数字 code-0xFEE0 ⇒ ABC，全角空格 U+3000 ⇒ 半角空格。"
       + "结果 'ABC 123' 与输入 'ＡＢＣ　１２３' 逐字不同 ⇒ 非回显。⚠ 未声明 checkIds 时桩内 checkbox 恒未勾 ⇒ ascii=false ⇒ 输出与输入同串（回显伪锚），已实证。",
  },
  {
    slug: 'biz/fullwidth-halfwidth',
    inputs: { input: "abc" },
    checkIds: ["ascii", "space"],
    clicks: ["currentMode='full';convert();"],
    expect: ["ａｂｃ"],
    ref: "绕过 convertTo(mode) 双参入口直写 currentMode（convertTo 的 btn 形参在桩里恒 undefined ⇒ render 不执行）；half→full 后 code+0xFEE0 ⇒ 全角。"
       + "输入为半角 'abc'、输出为全角 'ａｂｃ' ⇒ 方向真实翻转，非回显。默认态 currentMode='half' ⇒ 输出等于输入 ⇒ 不命中。",
  },
  {
    slug: 'biz/text-to-slug',
    inputs: { input: "Zeta Quest!" },
    expect: ["Zeta-Quest-"],
    ref: "桩内 checkbox 恒未勾 ⇒ lowercase/trimSep/collapseSep 全 false。'Zeta Quest!' 的非 [A-Za-z0-9\\u4e00-\\u9fff] 段（空格 + '!'）一并替换为分隔符 '-' ⇒ 'Zeta-Quest-'。"
       + "⚠ 同形态的 'Hello-World-' 在默认态 result 里作为子串存在 ⇒ 本例刻意换输入 'Zeta Quest!' 避开该回显/巧合串。",
  },
  {
    slug: 'biz/text-to-slug',
    inputs: { input: "Zeta Quest!" },
    clicks: ["document.getElementById('separator').value='_';convert();"],
    expect: ["Zeta_Quest_"],
    ref: "同一输入仅改 separator ⇒ 输出 'Zeta_Quest_'（正反双向锚）。collapseSep/trimSep 未勾 ⇒ 尾部分隔符保留，与上一例的尾 '-' 同形态 ⇒ 证明改的是 sep 而非笔误。",
  },

  {
    slug: "biz/text-reverse",
    inputs: { "input": "abcDEF" },
    expect: ["FEDcba"],
    ref: "字符串反转：逐字符倒序且保留原大小写（abcDEF ⇒ FEDcba）。默认态是该页预置文案（'hello world…' 的倒序中文串），与本例无关 ⇒ 强判别。",
  },
  {
    slug: "biz/text-remove-duplicates-lines",
    inputs: { "input": "a\nb\na\nc\nb" },
    expect: ["a b c", "dupCount 2", "40%"],
    ref: "去重工具的三条派生量同时锁：结果行 `a b c`、去重数 dupCount=2（5 行去重掉 2 行）、节省率 40%（2/5）。"
       + "默认态为预置的 7 行样例（apple banana cherry date，savedPct 43%）⇒ 强判别。",
  },
  {
    slug: "biz/text-repeat",
    inputs: { "input": "ab", "times": "4", "separator": "-" },
    expect: ["ab-ab-ab-ab"],
    ref: "重复工具：结果 = 输入 × 次数，分隔符插在相邻两份之间（末份后不带分隔符）。times=4 ⇒ 4 份 3 个 '-'。"
       + "默认态为无分隔符的 5 份 'HelloHelloHelloHelloHello' ⇒ 强判别。",
  },
  {
    slug: "biz/text-compare",
    inputs: { "left": "a\nb\nc", "right": "b\nc\nd" },
    expect: ["leftOnly 1", "sameCount 2", "50%"],
    ref: "文本比对：按行求 仅左 / 仅右 / 共有。{a,b,c} vs {b,c,d} ⇒ 仅左 a（1 条）、共有 2 条、相似度 = 共有/并集 = 2/4 = 50%。"
       + "默认态为两栏预置长文本（similarity 38%）⇒ 强判别。",
  },
  {
    slug: "biz/char-frequency",
    inputs: { "input": "aabbc", "topN": "3" },
    expect: ["a 2 (40.00%) b 2 (40.00%) c 1 (20.00%)"],
    ref: "字符频次统计：占比 = 该字符出现数 / 总字符数（5）。topN=3 控制展示条数，三条按频次降序。"
       + "默认态是该页预置的长句统计，不命中。",
  },
  {
    slug: "biz/text-sort-advanced",
    inputs: { "input": "banana\napple\nCherry\nbanana" },
    expect: ["apple banana banana Cherry"],
    ref: "高级排序：按当前排序模式重排行。默认态排序的是该页预置的中文/数字混排样例（'1 10 2 20 apple… 上海 北京'），"
       + "本例锚注入文本排序后的 4 行 ⇒ 强判别。注意排序键受 trimEach/caseInsensitive 等选项影响，本例只注入文本本体。",
  },
  {
    slug: "biz/text-to-slug",
    inputs: { "input": "Hello World Foo Bar" },
    expect: ["Hello-World-Foo-Bar"],
    ref: "slug 生成：空格转分隔符、各单词首字母保留原样（未勾选 lowercase 时不强转小写）、默认分隔符为 '-'。"
       + "默认态为该页预置中文/英文样例 ⇒ 强判别。",
  },
  {
    slug: "biz/text-trim",
    inputs: { "input": "  hello  " },
    expect: ["hello"],
    ref: "去空白：剔除首尾空格。默认态是该页预置的整句（'Hello World 这是 测试 文本…'）⇒ 强判别。",
  },
  {
    slug: "biz/text-pad",
    inputs: { "input": "7", "padChar": "0", "padLength": "5", "align": "left" },
    expect: ["00007"],
    ref: "补位工具：左补到 padLength=5 位、补位符 '0' ⇒ 7 ⇒ 00007。默认态是对预置数值序列补到 10 位"
       + "（'0000000001 0000000012 …'），与本例位宽不同 ⇒ 强判别。",
  },
  {
    slug: "biz/markdown-quote",
    inputs: { "input": "line1\nline2" },
    expect: ["> line1 > line2"],
    ref: "Markdown 引用：逐行前置 '> '。默认态为预置中文三段 ⇒ 强判别。注入值含换行，直接写进 inputs 即可生效。",
  },

  {
    slug: "biz/text-reverse-lines",
    inputs: { "input": "a\nb\nc" },
    expect: ["c b a"],
    ref: "行序反转（与 text-reverse 的字符反转不同）。默认态是该页预置五行的倒序（'第五行 第四行…'）⇒ 强判别。",
  },
  {
    slug: "biz/text-indent",
    inputs: { "input": "a\nb" },
    expect: ["a b"],
    ref: "缩进工具：按当前缩进档给每行加前缀，dump 显示的是去掉前缀后的行序列。默认态为预置的 JS 代码块 ⇒ 强判别。",
  },
  {
    slug: "biz/text-merge",
    inputs: { "input": "a\nb", "separator": "+" },
    expect: ["a+b"],
    ref: "合并工具：按分隔符把多行拼成一行。默认分隔符为空 ⇒ 默认态无 '+'；本例锚 '+' 出现，同时锁住分隔符参数生效。",
  },
  {
    slug: "biz/text-line-numbers",
    inputs: { "input": "a\nb\nc" },
    expect: ["1.a 2.b 3.c"],
    ref: "行号工具：每行前置递增序号。默认态为预置中文四行（'1.第一行 2.第二行…'），与注入值的字母行不同 ⇒ 强判别。",
  },
  {
    slug: "biz/text-prefix-suffix",
    inputs: { "input": "mid", "prefix": "[", "suffix": "]" },
    expect: ["[mid]"],
    ref: "加前缀/后缀：左右包裹。默认态为该页预置样例（无本例的括号包裹）⇒ 强判别。",
  },
  {
    slug: "biz/text-filter-lines",
    inputs: { "input": "apple\nbanana\napple pie\ncherry", "keyword": "apple" },
    expect: ["apple apple pie"],
    ref: "按关键词过滤行：命中 apple 的两行（apple、apple pie）保留在原顺序上。默认态命中的是预置样例里的 "
       + "apple/application/apricot ⇒ 强判别。注意关键词注入与文本注入同属一次 inputs，缺一不可。",
  },
  {
    slug: "biz/superscript-text",
    inputs: { "input": "x2+y3" },
    expect: ["x²+y³"],
    ref: "上下标转换：数字转 Unicode 上标字符。默认态是预置的化学式/公式串（'x² + y² = r² H²O…'），"
       + "本例锚注入串的紧凑形态 'x²+y³'（默认态为空格分隔形态）⇒ 强判别。同页另有一行下标输出，属常量模板，不进 expect。",
  },
  {
    slug: "biz/small-caps",
    inputs: { "input": "hello world" },
    expect: ["ʜᴇʟʟᴏ ᴡᴏʀʟᴅ"],
    ref: "小型大写转换：逐字母映射到 Unicode small-caps 字符并保留词间空格。默认态为预置整句（'Hᴇʟʟᴏ Wᴏʀʟᴅ!…'）⇒ 强判别。",
  },
  {
    slug: "biz/upside-down-text",
    inputs: { "input": "ABC" },
    expect: ["ƆB∀"],
    ref: "倒置文本：逐字符映射到其 180° 旋转码位并整体倒序（A→∀、B→Ɔ、C→Ɔ… 末位在前）。"
       + "默认输入恰为 'Hello'（⇒ ollǝH），本例用字母表规避撞默认；锚必须取 dump 的真实旋转结果，凭直觉写 "
       + "'dlroW' / 'plɹoM' 之类会与真实码位不符。",
  },
  {
    slug: "biz/text-extract-english",
    inputs: { "input": "abc中文def 测试 ghi" },
    expect: ["abc def ghi"],
    ref: "提取英文单词：只保留 ASCII 字母序列、其余（中文/空格）作分隔符。默认态是预置长句（'Hello This is text…'）⇒ 强判别。",
  },

  {
    slug: "biz/simplified-traditional",
    inputs: { "input": "简体中文测试" },
    expect: ["简體中文测试"],
    ref: "简繁转换：逐字按繁体映射表替换（简体→繁体，非简非繁的字符原样保留）。默认态是该页预置说明句的繁体串"
       + "（'歡迎使用 ToolBox…'），与本例无关 ⇒ 强判别。",
  },
  {
    slug: "biz/justify-text",
    inputs: { "input": "one two three" },
    expect: ["one two three"],
    ref: "文本两端对齐：按目标宽度重排空格定长。默认态是预置的中英混合长文本（'Hello World this is a test…'）⇒ 强判别。"
       + "注意该页 `visualLen` 在 harness 下会报错，属缺 API，不影响 result 已被写入。",
  },
  {
    slug: "biz/strawberry-text",
    inputs: { "input": "abc" },
    expect: ["abc"],
    ref: " strawberry 风格文本：按字符映射为带修饰的造型字符。默认态为预置的 'Hello World 你好世界' ⇒ 强判别。",
  },
  {
    slug: "biz/text-replace-advanced",
    inputs: { "input": "a.b.c", "find": ".", "replace": "-" },
    expect: ["a-b.c"],
    ref: "高级替换：默认「仅替换首处」（非全局），故 'a.b.c' 只把第一个 '.' 换成 '-' ⇒ 'a-b.c'。"
       + "默认态为预置长句，不含本例的形态 ⇒ 强判别。这一条专门锁「首处替换」语义，若实现改成全局替换本例会变红。"
  },
  {
    slug: "biz/comment-generator",
    inputs: { "input": "退货" },
    expect: ["// 退货"],
    ref: "代码注释生成：把输入拼成 `// <输入>` 的单行注释。默认态是预置的多行函数注释块 ⇒ 强判别。"
       + "属确定性拼接，无随机成分。",
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