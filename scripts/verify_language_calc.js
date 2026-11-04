#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "language/calc-1",
  "inputs": {
    "knownRatio": "90"
  },
  "expect": [
    "90"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "language/calc-2",
  "inputs": {
    "wordCount": "1200",
    "comprehension": "80",
    "minutes": "3",
    "seconds": "30"
  },
  "expect": [
    "342.9"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例（inputs 空），expect「commencer」是 quickList 静态标签（逃生项）。
  // 该页输入框只绑 onkeydown（回车触发 lookup），harness 只派发 input/change/keyup ⇒ 命中发生在
  // 兜底阶段调用 lookup()（via=lookup），但注入值确由 verbInput 读出，属真实注入。
  // finir 属第二组 -ir：词干 fin + is/is/it/issons/issez/issent。
  "slug": "language/french-verb-conjugator",
  "inputs": {
    "verbInput": "finir"
  },
  "expect": [
    "nous finissons",
    "vous finissez"
  ],
  "ref": "第二组 -ir 规则：词干 fin + is/is/it/issons/issez/issent，变位表按 PRONOUNS=[je,tu,il/elle,nous,vous,ils/elles] 渲染 ⇒ 「nous finissons」「vous finissez」仅在注入态出现。默认态 verbInput 为空 → lookup() 首行 return、#result 不被改写 ⇒ 两串均失配。**注意**：整页 quickList（parler/aimer/finir/commencer…）是静态标签，一律不可作 expect。"
},
{
  "slug": "language/generator-19",
  "inputs": {
    "phrase": "Application Programming Interface\n区块链技术"
  },
  "expect": [
    "1. Application Programming Interface → 缩写 ： API",
    "2. 区块链技术 → 缩写 ： 区链技"
  ],
  "ref": "真实短语输入：英文按单词取首字母（API）→ 输出「1. Application Programming Interface → 缩写 ： API」；中文按内置词表最大正向匹配分词为「区块/链/技术」，取各词组首字 ⇒ 区链技（不再隔字取字成区链术）→「2. 区块链技术 → 缩写 ： 区链技」。默认 textarea 为「Natural Language Processing / Machine Learning」⇒ 默认输出 NLP、ML，两条断言均失配；页面静态深度解析虽有 API 字样，但不含带序号与「→ 缩写 ：」的完整行。"
},
{
  "slug": "language/idiom-solitaire",
  "inputs": {
    "timeLimit": "20"
  },
  "expect": [
    "20"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例（inputs 空），expect「请输入韩文内容」是空态占位文案（逃生项）。
  // 注入 한글 后逐字拆初/中/终声并给罗马字转写。
  "slug": "language/korean-hangul-decomposer",
  "inputs": {
    "hangulInput": "한글"
  },
  "expect": [
    "罗马字转写: haᆫg/keuᆯ",
    "初声: ᄒ 히읗 [h] 中声: ᅡ 아 [a] 终声: ᆫ 니은"
  ],
  "ref": "한 = ㅎ(히읗) + ㅏ(아) + ㄴ(니은)、글 = ㄱ(기역) + ㅡ(으) + ㄹ(디귿) ⇒ 拆解串「初声: ᄒ 히읗 [h] 中声: ᅡ 아 [a] 终声: ᆫ 니은」与汇总串「罗马字转写: haᆫg/keuᆯ」。默认态输入为空 → 只输出「请输入韩文内容」占位，两串均失配。"
},
{
  // 原为 all_default 弱用例（两个 textarea 注入值均为空串 = 页面默认），expect「154」是动词表静态计数（逃生项）。
  // 注入后同时驱动「首字母缩写」与「字符数统计」两个面板。
  "slug": "language/language-toolkit",
  "inputs": {
    "acronymInput": "World Health Organization",
    "charInput": "Hello 世界！AB 12."
  },
  "expect": [
    "• World → W • Health → H • Organization → O",
    "15\n2\n7\n2\n2\n2\n2\n1\n0\n0"
  ],
  "ref": "① 缩写：三词各取首字母（acroCase 默认 upper，radio 落 checked 默认态）→ WHO，明细项「• World → W • Health → H • Organization → O」；② 字符统计「Hello 世界！AB 12.」→ 总字符 15 / 汉字 2 / 字母 7 / 数字 2 / 标点 2 / 空格 2 / 单词 2 / 句子 1（blob 按元素创建顺序拼接，故用换行符做连续断言）。默认态两 textarea 皆空 ⇒ 缩写面板隐藏、字符统计区显示「—」与「请输入文本后再统计。」提示，两组 expect 均失配。"
},
{
  // 原为 no_inputs 弱用例（inputs 空），expect「gentlemen.」是 PHRASES 全量列表里的静态短语（逃生项）。
  // 检索过滤型：q=please 命中 4 条，卡片子集变化 ⇒ 只能锚「仅过滤态成立的跨卡片相邻串」。
  "slug": "language/phrase-translator",
  "inputs": {
    "search-input": "please"
  },
  "expect": [
    "礼貌 例: Please forgive me for my mistake. 便宜点",
    "购物 例: Can you make it cheaper? 请说慢一点"
  ],
  "ref": "haystack = zh+en+cat（不含 ex），please 命中 请原谅我(idx12)/便宜点(30)/请说慢一点(41)/请再说一遍(42)。默认态（q 空）渲染全部 48 条、卡片按原序相邻（12→13、30→31），故「礼貌 例: Please forgive me for my mistake. 便宜点」「购物 例: Can you make it cheaper? 请说慢一点」两条跨卡片相邻串仅过滤态成立；单卡片文本在默认态必然出现，不可作 expect。"
},
{
  "slug": "language/stats-2",
  "inputs": {
    "text": "Hello hi 你好，世界！AB CD."
  },
  "expect": [
    "21",
    "18"
  ],
  "ref": "字符统计：'Hello hi 你好，世界！AB CD.' → 总字符(含空格)21、不含空格18（独立复算：Hello5+空格1+hi2+空格1+你好，3+世界！3+AB2+空格1+CD2+.1=21；空白3处→18），非默认输入（默认文本回退得16/15）"
},
{
  "slug": "language/text-polisher",
  "inputs": {
    "input": "我觉得这个方案其实非常好，然后我们赶紧开始开始吧。"
  },
  "expect": [
    "这个方案非常好，随后我们赶紧开始吧。",
    "已优化 4 处"
  ],
  "ref": "本地口语清理：删除填充词「我觉得」「其实」各 1 处、把「然后」改写为「随后」1 处、合并重复词「开始开始」为「开始」1 处 ⇒ 共 4 处；输出「这个方案非常好，随后我们赶紧开始吧。」且信息区显示「已优化 4 处」。默认输入含多余空格与半角标点但不是口语句，默认态既无「随后」也无「已优化 4 处」⇒ 两条断言仅注入态成立。"
},
{
  // 原为 all_default 弱用例（注入键为空串 = 页面默认），expect「Tomorrow」是 QUICK 静态词表（逃生项），已废弃。
  // 「谢谢你好」是连续中文，必须靠最大正向匹配切成「谢谢 + 你好」才能逐段译出；旧实现按整段 /[\u4e00-\u9fa5]+/g
  // 切词后整段查不到词条即落空，故该串仅修复后成立。
  "slug": "language/translator",
  "inputs": {
    "src-text": "谢谢你好"
  },
  "expect": [
    "Thank you. Hello."
  ],
  "ref": "最大正向匹配：谢谢(Thank you) + 你好(Hello) ⇒ 相邻译文以「. 」连接并补句末句点 ⇒ 「Thank you. Hello.」；未命中片段保留原文。src-lang/tgt-lang 默认即 zh→en，默认态 src-text 为空 → trans() 提前 return，#tgt-text 保持空 ⇒ 该串失配。"
},
{
  "slug": "language/vocabulary-builder",
  "clicks": ["localStorage.getItem=function(k){if(k==='vocab_fav')return JSON.stringify(['aberrant']);return null;};state.cat='fav';pickWord();"],
  "expect": [
    "aberrant"
  ],
  "ref": "独立复算：注入的收藏表 ['aberrant'] 命中 WORDS.gre[0]，pickWord() 走 state.cat==='fav' 分支 ⇒ pool 只含该词，#word 渲染单词名、#phonetic 渲染 /æˈberənt/。注入路径复刻 .cat-btn[data-c=fav] 的真实 onclick（state.cat=b.dataset.c; pickWord()），仅把 dataset.c 换成注入的收藏表。选 gre 词条是因为默认 state.cat='cet4'：cet4 池内任一随机词都产不出该串，规避 pickWord() 的 Math.random() 导致的默认态偶发命中。"
},
  {
    "slug": "language/german-gender-quiz",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "Wolf (狼)\nabc123测试\n0\n1\n0\n未找到包含 \"abc123测试\" 的名词。当前词库包含 184 个名词。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「Wolf (狼)\nabc123测试\n0\n1\n0\n未找到包含 \"abc123测试\"…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "language/grammar-checker",
    "inputs": {
      "input-text": "He go home. She go home."
    },
    "clicks": [
      "check()"
    ],
    "expect": [
      "主谓一致",
      "问题密度： 1.00"
    ],
    "ref": "主谓一致规则 + 密度：注入 2 句、2 处 he/she + go 缺 -s ⇒ 问题 2、句数 2、密度 1.00（建议局部修订）。默认样例无问题、密度 0.00 ⇒ 注入失败即不命中。"
  },
  {
    "slug": "language/grammar-checker",
    "inputs": {
      "input-text": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n5\n0\n1\n0"
    ],
    "ref": "EL-J14 同步：注入 5 字符无规则文本后，统计口径为字符 5 / 单词 0 / 句 1 / 问题 0（修复前零长度正则刷出 5 条假问题）。锚「1 2 3\\n5\\n0\\n1\\n0」四统计串：默认样例（73 字符 / 2 词 / 2 句）不命中 ⇒ 零逃生。"
  },
  {
    "slug": "language/spanish-accent-rules",
    "inputs": {
      "wordInput": "abc123测试"
    },
    "expect": [
      "abc123测试\n分析结果: abc123测试 ab c 1 2 3 测 试 重音音节 试 (第1音节，从后数) 以辅音(非n/s)结尾，重音在末音节 总音节数 7 个音节 音节划分: ab - c - 1 - 2 - 3 - 测 - 试 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"wordInput\":\"abc123测试\"}，输出区含「abc123测试\n分析结果: abc123测试 ab c 1 2 3 测 试 重…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "language/vocabulary-builder",
    "clicks": [
      "var s={vocab_streak:JSON.stringify({days:1,last:'2024-11-01'})};localStorage.getItem=function(k){return s[k]||null;};localStorage.setItem=function(k,v){s[k]=String(v);};var o=[];checkStreak(new Date(2024,10,2,7,30));o.push(document.getElementById('s-streak').textContent);checkStreak(new Date(2024,10,2,8,30));o.push(document.getElementById('s-streak').textContent);checkStreak(new Date(2024,10,3,0,30));o.push(document.getElementById('s-streak').textContent);document.getElementById('vbHidden').textContent='QSTREAK:'+o.join('|');"
    ],
    "expect": [
      "QSTREAK:2|2|3"
    ],
    "ref": "EL-J9 回归（本地日界）：昨日 2024-11-01 已有 1 天，本地 11-02 07:30 首练 ⇒ 2 天；同日 08:30 再练不得再加 ⇒ 仍 2；本地 11-03 00:30 ⇒ 3。旧实现按 UTC 日期：11-02 07:30（UTC 仍 11-01）判同日不增 ⇒ 1，08:30（UTC 11-02）才增 ⇒ 2，11-03 00:30（UTC 仍 11-02）又不增 ⇒ 2，即 1|2|2，必 FAIL。"
  },
  {
    "slug": "language/grammar-checker",
    "inputs": {
      "input-text": "<script>teh</script>"
    },
    "clicks": [
      "check()"
    ],
    "expect": [
      "&lt;script&gt; teh &lt;/script&gt;"
    ],
    "ref": "EL-J14 回归：输入含真实标签 <script> 且命中 teh 规则时，原文入 innerHTML 前必须转义 ⇒ 结果区出现实体串「&lt;script&gt;teh&lt;/script&gt;」（采集器把 <mark> 高亮标签剥成空格，故锚点为带空格的 &lt;script&gt; teh &lt;/script&gt;）。旧实现直接拼原文，innerHTML 里是真 <script> 标签，采集器剥标签后只剩 teh，不可能命中实体串。"
  },
  {
    "slug": "language/grammar-checker",
    "inputs": {
      "input-text": "<b>teh</b>"
    },
    "clicks": [
      "check()"
    ],
    "expect": [
      "&lt;b&gt; teh &lt;/b&gt;"
    ],
    "ref": "EL-J14 回归（<b> 变体）：转义后实体串为「&lt;b&gt;teh&lt;/b&gt;」，<mark> 被剥成空格后锚点为「&lt;b&gt; teh &lt;/b&gt;」。旧实现把 <b> 当真实标签渲染/吞掉，采集器剥标签后只剩 teh，不命中。"
  },
  {
    "slug": "language/calc-2",
    "inputs": {
      "wordCount": "800",
      "comprehension": "150",
      "minutes": "3",
      "seconds": "30"
    },
    "expect": [
      "请输入有效的字数、用时和理解度（理解度须为 0–100）。"
    ],
    "ref": "EL-J25 回归：理解度 150 越界必须拒绝。独立复算：字面速度 800 / 3.5 = 228.571 → 228.6 字/分，150% 时旧实现输出有效速度 342.9 > 字面速度，属无效值。默认理解度 80 显示 182.9 且无此提示串 ⇒ 强判别。"
  },
  {
    "slug": "language/calc-2",
    "inputs": {
      "wordCount": "800",
      "comprehension": "-10",
      "minutes": "3",
      "seconds": "30"
    },
    "expect": [
      "请输入有效的字数、用时和理解度（理解度须为 0–100）。"
    ],
    "ref": "EL-J25 下界：理解度 -10 越界必须拒绝（旧实现会输出有效速度 228.6 × -10% = -22.9 字/分）。默认理解度 80 无此提示串 ⇒ 强判别。"
  },
  {
    "slug": "language/calc-2",
    "inputs": {
      "wordCount": "800",
      "comprehension": "100",
      "minutes": "3",
      "seconds": "30"
    },
    "expect": [
      "理解度 100%，有效速度 = 228.6 × 100% = 228.6 字/分"
    ],
    "ref": "EL-J25 上界：理解度 100% 合法且有效速度封顶等于字面速度。独立复算：800 / (3 + 30/60) = 228.571 → 228.6；有效 = min(228.571, 228.571 × 1.0) = 228.6，不大于字面速度。默认 80% 输出 182.9，本串不命中。"
  }

  // ── 空态回归：textarea 清空后必须提示「请输入」，不得输出全 0 统计 ──
  ,{
    "slug": "language/stats-2",
    "inputs": { "text": "" },
    "expect": ["请输入待统计文本后再统计。"],
    "ref": "空态回归：textarea 清空时旧实现按空串统计并输出「总字符数 0 … 行数 0」九项伪结果；现要求提示且不输出统计值。默认示例文本非空（16/15 等数值），不含该提示 ⇒ 强判别。"
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

  console.log("==== language calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
