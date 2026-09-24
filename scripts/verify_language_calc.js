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
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/idiom-solitaire",
  "inputs": {
    "timeLimit": "20"
  },
  "expect": [
    "20"
  ],
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
  "ref": "① 缩写：三词各取首字母（acroCase 默认 upper，radio 落 checked 默认态）→ WHO，明细项「• World → W • Health → H • Organization → O」；② 字符统计「Hello 世界！AB 12.」→ 总字符 15 / 汉字 2 / 字母 7 / 数字 2 / 标点 2 / 空格 2 / 单词 2 / 句子 1（blob 按元素创建顺序拼接，故用换行符做连续断言）。默认态两 textarea 皆空 ⇒ 缩写面板隐藏、统计全 0，两组 expect 均失配。"
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
    "input": "这是一段 测试文本，里面有  多余空格 。中英文 混排时 , 标点容易出错 。_X"
  },
  "expect": [
    "41"
  ],
  "ref": "auto-restore"
},
{
  // 原为 all_default 弱用例（两个注入键均为空串 = 页面默认），expect「Tomorrow」是 QUICK 静态词表（逃生项）。
  // QUICK=['你好',…,'Home'] 整体渲染进 #quick-row ⇒ 词表内任何英文词都零判别力，必须避开（Today/Tomorrow/
  // Sorry/Water/Fire/Home 全部在表内）。俄罗斯/西班牙 不在表内。
  "slug": "language/translator",
  "inputs": {
    "src-text": "俄罗斯 西班牙"
  },
  "expect": [
    "RussiaSpain"
  ],
  "ref": "src-lang/tgt-lang 默认即 zh→en：中文按 /[\u4e00-\u9fa5]+/g 切词得 [俄罗斯,西班牙] → 词典译为 [Russia,Spain] → src==='zh' 时以空串 join ⇒ 「RussiaSpain」（此 join 规则为本页既有行为，未来若改为空格连接需同步改 expect）。默认态 src-text 为空 → trans() 提前 return，#tgt-text 保持空 ⇒ 该串失配。"
},
{
  "slug": "language/vocabulary-builder",
  "inputs": {},
  "expect": [
    "50"
  ],
  "ref": "结构性不可注入（保留 no_inputs）：该页 input/select/textarea 计数为 0，词汇表与控件全由 JS 模板 + innerHTML 生成，且含无参预设函数 ⇒ harness 无任何按 id 的注入通道。expect「50」取默认渲染出的词汇条数（默认态派生量），非静态标签串。"
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
  console.log("==== language calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
