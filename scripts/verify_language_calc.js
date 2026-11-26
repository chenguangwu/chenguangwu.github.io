#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug":"language/language-toolkit",
  "inputs":{"acronymInput":"École e\u0301cole 中文 World"},
  "expect":["École → É", "école → É", "中文 → 已跳过（仅支持英文/拉丁字母）"],
  "ref":"带重音拉丁字母、组合重音及混合中文应正确取首字母。"
},
{
  "slug": "language/calc-1",
  "inputs": {
    "knownRatio": "90"
  },
  "expect": [
    "90"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"manger"},"expect":["nous mangeons"],"ref":"manger 的现在时 nous 保留 e。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"commencer"},"expect":["nous commençons"],"ref":"commencer 的现在时 nous 使用 ç。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"acheter"},"expect":["achète"],"ref":"acheter 的单数词干变为 achèt。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"appeler"},"expect":["j'appelle","nous appelons","appellerai"],"ref":"appeler 双写 l：je/tu/il/ils 及将来时双写，nous/vous 保持单 l。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"jeter"},"expect":["je jette","nous jetons","jetterai"],"ref":"jeter 双写 t：单数双写，nous/vous 保持单 t。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"préférer"},"expect":["je préfère","nous préférons","ai préféré"],"ref":"préférer 保留重音，单数 é→è，nous/vous 保持 é，过去分词 préféré。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"courir"},"expect":["无法可靠生成","未收录的 -ir"],"ref":"未收录的 -ir 可能属第三组，必须提示而不是套第二组规则。"},
{"slug":"language/french-verb-conjugator","inputs":{"verbInput":"ficeler"},"expect":["无法可靠生成","未收录的拼写变体"],"ref":"未收录的 -eler 不猜双写形式。"},
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
// 已移除 language/idiom-solitaire（原 inputs timeLimit=20，expect ["20"]）。
// 原因：① 原注入 20 恰为页面 select 默认选中项，expect「20」只是 select 值回显 ⇒ 默认态即命中；
// ② 计时只走 setInterval 写进度条样式、不产文本；③ 尝试改锚 clicks startGame() ⇒「游戏结束！共接 0 个成语」
// 仍被 harness 兜底阶段的无参函数 endGame() 复现（discriminate via=endGame）⇒ 依旧零判别力。
// 无安全的注入态专属文本通道 ⇒ 按纪律删除而非保留 skip。
{
  // 原为 no_inputs 弱用例（inputs 空），expect「请输入韩文内容」是空态占位文案（逃生项）。
  // 注入 한글 后逐字拆初/中/终声并给罗马字转写。
  "slug": "language/korean-hangul-decomposer",
  "inputs": {
    "hangulInput": "한글"
  },
  "expect": [
    "RR 罗马字转写（已处理基本连音）: hanggeul",
    "终声: ᆯ 리을"
  ],
  "ref": "RL-韩语终声与罗马字修复：한=ㅎ(히읗)+ㅏ(아)+ㄴ(니은)终声 n ⇒ hang；글=ㄱ(기역)+ㅡ(으)+ㄹ终声 l ⇒ geul。旧版终声名表从 8 起整体错位（리을 误作 디귿）、罗马字直接拼 Unicode 终声字母（haᆫg/keuᆯ）；修复后 FINAL_NAMES[8]=리을、FINAL_ROMA 映射 8→l ⇒「罗马字转写: hang/geul」与「终声: ᆯ 리을」。默认态输入为空只输出占位，两串均失配。"
},
{"slug":"language/korean-hangul-decomposer","inputs":{"hangulInput":"바"},"expect":["RR 罗马字: ba"],"ref":"바 的初声ㅂ在音节首按 RR 转 b，不再把教学音值 b/p 拼进转写。"},
{"slug":"language/korean-hangul-decomposer","inputs":{"hangulInput":"한국어"},"expect":["hangugeo","基本连音","上下文音变未建模"],"ref":"한국어 的 국 终声ㄱ移到后字ㅇ，得到 hangugeo；同时明确连音之外音变未建模。"},
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
  // EL-F16：中文输入不再输出单字冒充缩写，明确跳过并提示（旧版输出「中华人民共和国 → 中」）。
  "slug": "language/language-toolkit",
  "inputs": {
    "acronymInput": "中华人民共和国 World Health"
  },
  "expect": [
    "中华人民共和国 → 已跳过（仅支持英文/拉丁字母）",
    "已跳过 1 个非拉丁字母词，未计入缩写"
  ],
  "ref": "注入「中华人民共和国 World Health」：新实现按词查找首个拉丁字母，中文词无拉丁字母⇒跳过并在明细写「中华人民共和国 → 已跳过（仅支持英文/拉丁字母）」，汇总写「已跳过 1 个非拉丁字母词，未计入缩写」。旧实现中文分支取 w.charAt(0) 输出「中华人民共和国 → 中」，两条断言全失配；默认态 acronymInput 为空⇒缩写面板隐藏，同样失配。**注意**：英文共有串「• World → W • Health → H」旧版也成立，按「或」语义会让整条用例假绿，禁止列入。"
},
{
  // EL-F16 补充：全中文输入明确拒算，不再输出单个汉字冒充缩写（旧版输出「中」）。
  "slug": "language/language-toolkit",
  "inputs": {
    "acronymInput": "中华人民共和国"
  },
  "expect": [
    "未识别到英文/拉丁字母词；本生成器仅支持英文/拉丁字母输入。"
  ],
  "ref": "只输入中文时新实现 result 为空⇒缩写位「—」并在明细写「未识别到英文/拉丁字母词；本生成器仅支持英文/拉丁字母输入。」；旧实现把整段中文当一个词取首字输出「中」，该串失配；默认态 acronymInput 为空⇒面板隐藏不显示提示，同样失配。"
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
  "slug": "language/phrase-translator",
  "inputs": {
    "search-input": "pleasezz"
  },
  "clicks": ["var q=document.getElementById('search-input').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/language/phrase-translator.html','utf8');var d=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var ok=q==='pleasezz'&&h.indexOf('支持多种语言互转')<0&&h.indexOf('中英文常用语互查')>=0&&d.indexOf('¿Cuánto')<0&&d.indexOf('Je ne comprends')<0;document.getElementById('__tbProbe').textContent='PTL20 '+(ok?'OK':'BAD');"],
  "expect": ["PTL20 OK"],
  "ref": "EL-J20：词库只有中英，intro 与深挖示例须删「支持多种语言互转」及西语/法语虚标，改中英互查口径；旧版两处虚标均在，源码哨兵必 BAD。"
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
  "slug": "language/vocabulary-builder",
  "clicks": ["var s={vocab_fav:JSON.stringify(['existing'])};localStorage.getItem=function(k){return s[k]||null;};localStorage.setItem=function(k,v){s[k]=String(v);};state.cat='cet4';pickWord();var w=state.current.w;mark('known');var after=JSON.parse(s.vocab_fav||'[]');var noAuto=after.indexOf(w)<0&&after.length===1;state.current={cat:'cet4',w:w};toggleFav();var added=JSON.parse(s.vocab_fav).indexOf(w)>=0;toggleFav();var removed=JSON.parse(s.vocab_fav).indexOf(w)<0;document.getElementById('vbHidden').textContent='JFAV:'+(noAuto&&added&&removed?'OK':'BAD');"],
  "expect": ["JFAV:OK"],
  "ref": "EL-J7：标记「认识」不得自动塞收藏，星标须可显式加入与移出；旧版 mark('known') 无条件 push 且无 toggleFav，必 BAD。"
},
{
  "slug": "language/vocabulary-builder",
  "clicks": ["var s={};localStorage.getItem=function(k){return s[k]||null;};localStorage.setItem=function(k,v){s[k]=String(v);};state.current={cat:'cet4',w:'TESTWORD'};mark('known');var r1=JSON.parse(s.vocab_review||'{}')['cet4_TESTWORD'];state.current={cat:'cet4',w:'TESTWORD'};mark('known');var r2=JSON.parse(s.vocab_review||'{}')['cet4_TESTWORD'];var same=r1&&r2&&r1.step===0&&r1.due===r2.due&&r1.due===dayKeyAfter(1);r2.due=localDateKey();s.vocab_review=JSON.stringify({cet4_TESTWORD:r2});state.current={cat:'cet4',w:'TESTWORD'};updateReview('known');var r3=JSON.parse(s.vocab_review).cet4_TESTWORD;state.current={cat:'cet4',w:'TESTWORD'};updateReview('fuzzy');var r4=JSON.parse(s.vocab_review).cet4_TESTWORD;var ok=same&&r3.step===1&&r3.due===dayKeyAfter(2)&&r4.step===0&&r4.due===dayKeyAfter(1);document.getElementById('vbHidden').textContent='JDUE:'+(ok?'OK':'BAD');"],
  "expect": ["JDUE:OK"],
  "ref": "EL-J8：首次安排 1 天，提前复习不升级；到期后安排 2 天，模糊重置为 1 天。"
},
  {
    "slug": "language/german-gender-quiz",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "未找到包含 \"abc123测试\" 的名词。当前词库包含 183 个名词。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「Wolf (狼)\nabc123测试\n0\n1\n0\n未找到包含 \"abc123测试\"…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "language/german-gender-quiz",
    "clicks": ["document.getElementById('__tbProbe').textContent='GQFIX '+NOUN_CONFLICTS.length+'/'+UNIQUE_NOUNS.length+'/'+NOUNS.length+'/'+NOUNS.filter(function(n){return n.word==='Augen';}).length;"],
    "expect": ["GQFIX 0/183/183/0"],
    "ref": "EL-F20 数据自检：删除复数独立词条 Augen、伪条目 der Haus 与两条完全重复（Mädchen/Buch）后，NOUNS/UNIQUE_NOUNS 均为 183，同词同义不同性冲突 NOUN_CONFLICTS=0，Augen 独立词条数为 0。旧版无 NOUN_CONFLICTS 变量且 UNIQUE_NOUNS=184、含 Augen ⇒ 该串失配。",
  },
  {
    "slug": "language/german-gender-quiz",
    "inputs": { "searchInput": "Augen" },
    "expect": ["未找到包含 \"augen\" 的名词。当前词库包含 183 个名词。"],
    "ref": "EL-F20 行为回归：搜「Augen」应无命中（正确词形是单数 das Auge，复数 die Augen 只在详情展示，不作为独立测验词条）；旧版词库含 Augen/die 会命中并显示表格，该提示串失配。",
  },
  {
    "slug": "language/german-gender-quiz",
    "clicks": ["localStorage.clear();wrongQueue=[];reviewMode=false;reviewWords=[];renderReview();currentNoun={word:'Haus',gender:'das',meaning:'房子'};answered=false;answer('die');document.getElementById('__tbProbe').textContent='GERMQ '+wrongQueue.length+' '+document.getElementById('reviewCount').textContent;"],
    "expect": ["GERMQ 1 1"],
    "ref": "答错后词条进入本地错词队列，队列计数与界面同步为 1。"
  },
  {
    "slug": "language/german-gender-quiz",
    "clicks": ["localStorage.clear();wrongQueue=['Haus'];saveReview();reviewMode=false;reviewWords=[];startReview();currentNoun={word:'Haus',gender:'das',meaning:'房子'};answered=false;answer('das');var after=wrongQueue.length;reviewMode=false;reviewWords=[];clearReview();document.getElementById('__tbProbe').textContent='GERMRV '+after+' '+wrongQueue.length+' '+document.getElementById('reviewCount').textContent;"],
    "expect": ["GERMRV 0 0 0"],
    "ref": "集中复习答对后移出队列；清空队列后界面计数归零。"
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
    "slug": "language/spanish-accent-rules",
    "inputs": { "wordInput": "casa" },
    "expect": [ "音节划分: ca - sa" ],
    "ref": "元音间单辅音归后一音节：casa 应为 ca-sa（旧实现把辅音拼进当前音节，整词当 1 音节）。默认输入为页面预设词，不命中。"
  },
  {
    "slug": "language/spanish-accent-rules",
    "inputs": { "wordInput": "meses" },
    "expect": [ "音节划分: me - ses" ],
    "ref": "元音+单辅音+元音连续切分：meses 应为 me-ses（旧实现 meses 整词 1 音节）。"
  },
  {
    "slug": "language/spanish-accent-rules",
    "inputs": { "wordInput": "cafe" },
    "expect": [ "以元音/n/s结尾，重音在倒数第二音节" ],
    "ref": "无符号词 cafe 按规则重音在倒数第二音节（español 默认态为「以辅音结尾、末音节」）。原锚「按规则无需重音符号」是通用文案、撞默认态；改锚随词尾类型变化的重音规则串，仍保留「不给出绿色✓不需要」的中性表述意图（同一注入态下方文案为「若你指的是 café…请补写符号」）。"
  },
  {
    "slug": "language/spanish-accent-rules",
    "clicks": [
      "document.getElementById('wordInput').value='casa';analyze();document.getElementById('wordInput').value='';analyze();document.getElementById('__tbProbe').textContent='CLR '+((String(document.getElementById('result').innerHTML).indexOf('请输入西语单词')>=0)?'1':'0');"
    ],
    "expect": [ "CLR 1" ],
    "ref": "清空输入须清空旧结果：旧实现 analyze() 在空串直接 return，结果区保留上一个单词的音节与重音结论。现写入「请输入西语单词」。默认态无探针串 ⇒ 零逃生。"
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
  },
{
  "slug": "language/ipa-practice",
  "clicks": ["showDetail('θ')"],
  "expect": ["清齿间摩擦音。舌尖放在上下齿之间", "θɪŋk"],
  "ref": "showDetail('θ') 渲染 /θ/ 详情：发音方法「清齿间摩擦音。舌尖放在上下齿之间，气流摩擦而出。」+ 例词 think /θɪŋk/。默认详情区为空（只渲染音标卡片网格），零交集。"
},
{
  // EL-F19：/e/ 术语按 IPA 官方表改为 close-mid（半闭），旧版写「半开」。
  "slug": "language/ipa-practice",
  "clicks": ["showDetail('e')"],
  "expect": ["半闭前不圆唇元音。口形比 i: 大，舌头稍后缩。"],
  "ref": "showDetail('e') 渲染 /e/ 详情：IPA 官方元音表 e=close-mid front unrounded（半闭前不圆唇），旧版误写「半开前不圆唇」（open-mid 是 ɛ/ɔ/ʌ/ɜ），该串失配；默认详情区为空，零交集。"
},
{
  // EL-F19 源码哨兵：/i:/ 例词删去跨语言的「茶 chá」，且 /e/ 术语已改。
  "slug": "language/ipa-practice",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/language/ipa-practice.html','utf8');var ok=!/茶/.test(h)&&!/chá/.test(h)&&h.indexOf('半闭前不圆唇元音')>=0;document.getElementById('__tbProbe').textContent='IPAFIX '+(ok?'OK':'BAD');"],
  "expect": ["IPAFIX OK"],
  "ref": "IPA_DATA 的 /i:/ 例词原混中文「茶 chá (类似)」（韵母 /a/ 与 /i:/ 无关），删除后页面无「茶」/「chá」；同时 /e/ 描述改「半闭」。旧版两者皆不满足 ⇒ IPAFIX BAD。"
},
{
  "slug": "language/riyuwushiyintulianxi-dianjifayin",
  "clicks": ["onKana(11)"],
  "expect": ["し 假名 shi 罗马字"],
  "ref": "onKana(11) ⇒ 平假名第 12 格「し / shi」：详情卡渲染两行数据卡「し · 假名」「shi · 罗马字」。默认未点选、详情区为空，零交集；网格内虽有「し」「shi」拼接文本，但不含「し 假名 shi 罗马字」这一带标签分隔的序列。"
},
{
  "slug": "language/stats-2",
  "inputs": { "text": "１２３④😀" },
  "clicks": ["calc();var h=document.getElementById('res').innerHTML;var ok=h.indexOf('数字字符数：<strong>3</strong>')>=0&&h.indexOf('总字符数（含空格）：<strong style=\"color:var(--primary);\">5</strong>')>=0;document.getElementById('__tbProbe').textContent='JWIDE:'+(ok?'OK':'BAD');"],
  "expect": ["JWIDE:OK"],
  "ref": "EL-J27：全角 １２３ 应计入数字（3），emoji 按 Unicode 码点计 1 字符（总 5）；旧版只认半角 [0-9] 且 t.length 把 emoji 算 2 ⇒ BAD。"
},
{
  "slug": "language/riyuwushiyintulianxi-dianjifayin",
  "clicks": ["quizRight=3;quizTotal=5;answerQuiz(0);var before=quizTotal;resetQuizStats(1);var after=quizTotal;var shown=document.getElementById('quizTotal').textContent;document.getElementById('__tbProbe').textContent='JRESET:'+(before===6&&after===0&&shown==='0'?'OK':'BAD');"],
  "expect": ["JRESET:OK"],
  "ref": "EL-J34：答题统计须可显式重置，重置后内存计数与 DOM 同时归零；旧版 resetAll 为空函数、无 resetQuizStats ⇒ BAD。"
},
{
  "slug": "language/language-toolkit",
  "clicks": [
    "practiceCorrect=0;practiceTotal=0;var i=document.getElementById('practiceInput');"
    + "currentPracticeKana={kana:'し',romaji:'shi'};practiceAnswered=false;i.disabled=false;i.value='si';checkPractice();"
    + "var a=practiceCorrect,b=practiceTotal;"
    + "currentPracticeKana={kana:'を',romaji:'wo'};practiceAnswered=false;i.disabled=false;i.value='o';checkPractice();"
    + "var c=practiceCorrect;"
    + "currentPracticeKana={kana:'し',romaji:'shi'};practiceAnswered=false;i.disabled=false;i.value='xi';checkPractice();"
    + "document.getElementById('__tbProbe').textContent='ELF14 a='+a+'/'+b+' w='+c+' x='+practiceCorrect+'/'+practiceTotal"
    + "+' fb='+document.getElementById('practiceFeedback').textContent;"
  ],
  "expect": ["ELF14 a=1/1 w=2 x=2/3 fb=✗ 错误。し 的罗马音是 shi（也接受 si）"],
  "ref": "EL-F14：し 接受 si、を 接受 o（旧实现只认单一 Hepburn 拼写，两例均判错）；xi 仍判错且反馈列出可接受变体「也接受 si」。默认未作答、练习反馈为空 ⇒ 强判别。"
},
{
  "slug": "language/language-toolkit",
  "clicks": [
    "practiceCorrect=0;practiceTotal=0;var i=document.getElementById('practiceInput');"
    + "var __np=nextPractice;nextPractice=function(){};"
    + "currentPracticeKana={kana:'し',romaji:'shi'};practiceAnswered=false;i.disabled=false;i.value='shi';"
    + "checkPractice();checkPractice();var q=practiceAnswered,t=practiceTotal,c2=practiceCorrect;nextPractice=__np;"
    + "document.getElementById('__tbProbe').textContent='ELF15 total='+t+' correct='+c2+' ans='+(q?'Y':'N');"
  ],
  "expect": ["ELF15 total=1 correct=1 ans=Y"],
  "ref": "EL-F15：答题后 practiceAnswered 置真并禁用输入，同一题连按回车（连续两次 checkPractice）只计 1 题。旧实现无守卫 ⇒ total=2/correct=2 必 FAIL。"
},
{
  "slug": "language/language-toolkit",
  "clicks": [
    "var all=getAllKana(),hist=all.filter(function(x){return x.kana==='ゐ'||x.kana==='ゑ';}).length;"
    + "document.getElementById('__tbProbe').textContent='ELF14KANA hist='+hist+' n='+all.length;"
  ],
  "expect": ["ELF14KANA hist=0"],
  "ref": "EL-F14：ゐ/ゑ 为历史假名，已从练习题库 getAllKana() 排除（仍保留在五十音图表中）。旧实现两者均在池内 ⇒ hist=2 必 FAIL。"
}
,
{
  "slug": 'language/german-gender-quiz',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/language/german-gender-quiz.html\',\'utf8\');var i=h.indexOf(\'function switchMode(mode) {\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'if(!mode) return;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'GERMH0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['GERMH0 OK'],
  "ref": "第1337批·历史恢复无参切换抛错修复源码形态强锚：旧版 function switchMode(mode) { 无参调用解引用参数/全局event抛错被 catch 吞、结果不重算；修复后无参分支安全返回或重算主结果。旧版无 ⇒ BAD。"
},
{
  "slug": "language/spanish-accent-rules",
  "clicks": ["var a=splitSyllables('país').join('-'),b=splitSyllables('río').join('-');document.getElementById('__tbProbe').textContent='ES '+a+' '+b;"],
  "expect": ["ES pa-ís rí-o"],
  "ref": "重音弱元音 í/ú 纳入 WEAK 且与 hasAccent 命中时断开二重元音：país→pa-ís、río→rí-o；修复前 í 不算元音，得到 país 单音节/错误重读。"
},
{
  "slug": "language/riyuwushiyintulianxi-dianjifayin",
  "clicks": ["quizOn=true;cur='hira';nextQuiz();var before=document.getElementById('quizOpts').innerHTML;setKana('kata');var after=document.getElementById('quizOpts').innerHTML;document.getElementById('__tbProbe').textContent='KANA '+(/[ぁ-ん]/.test(before))+' '+(!/[ぁ-ん]/.test(after));"],
  "expect": ["KANA true true"],
  "ref": "练习中切到片假名后 setKana 立即重绘当前题：选项全部为片假名（无平假名），重播也按 chars() 取片假名发音；统计由按钮 resetQuizStats(1) 清零。修复前只刷新字表，选项仍是切换前字形。"
},
{
  "slug": "language/ipa-practice",
  "clicks": ["var s=__tbFs.readFileSync('tools/language/ipa-practice.html','utf8');document.getElementById('__tbProbe').textContent='IPA '+(/en-GB/.test(s))+' '+(/不评估用户发音/.test(s));"],
  "expect": ["IPA true true"],
  "ref": "朗读改为请求 en-GB 并优先选英式 voice，与示例的英式音标一致；页面明确正确率按描述选择题计分、不评估发音。"
},
{
  "slug": "language/ipa-practice",
  "clicks": ["var s=__tbFs.readFileSync('tools/language/ipa-practice.html','utf8');document.getElementById('__tbProbe').textContent='IPA2 '+(/答题正确率/.test(s))+' '+(/选择正确次数/.test(s));"],
  "expect": ["IPA2 true true"],
  "ref": "标准引据表把“练习正确率/正确发音”改为“答题正确率/选择正确次数”，与选择描述的实际逻辑一致。"
},
{
  "slug": "language/vocabulary-builder",
  "clicks": ["var s=__tbFs.readFileSync('tools/language/vocabulary-builder.html','utf8');document.getElementById('__tbProbe').textContent='VOC '+((s.indexOf('英语单词卡片与间隔复习')>=0)+' '+(!/在线语言翻译工具/.test(s)));"],
  "expect": ["VOC true true"],
  "ref": "title/description/OG/Twitter/JSON-LD 统一改为英语单词卡片与间隔复习，清除“在线语言翻译工具”误标（源码形态判定，构建会刷新 meta）。"
},
{"slug":"language/idiom-solitaire","clicks":["var ok=true;for(var i=0;i<30;i++){startGame();if(!hasContinuation(chain[0].text,[]))ok=false;endGame();}var dead=IDIOM_DB.filter(function(x){return !hasContinuation(x,[]);}).length;document.getElementById('__tbProbe').textContent='IDIOM '+ok+' '+(dead>0);"],"expect":["IDIOM true true"],"ref":"开局只从“尾字仍有后继”的成语中抽取；连续 30 次开局均可继续。词库中确实存在死端条目（dead>0），但不会再被选作开局。"},

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
