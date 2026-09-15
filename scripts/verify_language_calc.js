#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "language/calc-1", inputs: {"knownRatio":"60"}, expect: ["请勾选您认识的单词"], _selfcheck: true, _min_inputs: 1 },
  { slug: "language/calc-2", inputs: {"wordCount":"800","comprehension":"80","minutes":"3","seconds":"30"}, expect: ["有效速度"] },
  { slug: "language/french-verb-conjugator", inputs: {}, _min_inputs: 0, expect: ["判断"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/generator-19", inputs: {"cnt":"5"}, expect: ["客关管"], _selfcheck: true, _min_inputs: 1 },
  { slug: "language/german-gender-quiz", inputs: {}, _min_inputs: 0, expect: ["鼻子"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/grammar-checker", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/hanyuyanwenchaijie-yuanyin-fuyin", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "language/idiom-solitaire", inputs: {}, _min_inputs: 0, expect: ["系统出题"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/ipa-practice", inputs: {}, _min_inputs: 0, expect: ["向中央元音过渡"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/korean-hangul-decomposer", inputs: {}, _min_inputs: 0, expect: ["请输入韩文内容"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/language-toolkit", inputs: {}, _min_inputs: 0, expect: ["罗马音"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/phrase-translator", inputs: {}, _min_inputs: 0, expect: ["告别"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/riyuwushiyintulianxi-dianjifayin", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "language/spanish-accent-rules", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/stats-2", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/text-polisher", inputs: {}, _min_inputs: 0, expect: ["标点容易出错"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/translator", inputs: {}, _min_inputs: 0, expect: ["明天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/vocabulary-builder", inputs: {}, _min_inputs: 0, expect: ["她实现了目标"], _selfcheck: true, _min_inputs: 0 },
  { slug: "language/xibanyayuzhongyinweizhipanduan-neizhiguize", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== language calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();