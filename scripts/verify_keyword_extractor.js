#!/usr/bin/env node
// Exercise the page's actual tokenizer in both supported and fallback browsers.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '../tools/it/keyword-extractor.html'), 'utf8');
const start = html.indexOf('  var CJK_RE =');
const end = html.indexOf('  /* ===== 状态 ===== */', start);
assert(start >= 0 && end > start, 'tokenizer source not found');
const source = html.slice(start, end);
function load(intl) {
  const ctx = { Intl: intl, CN_STOPS: new Set(), EN_STOPS: new Set() };
  vm.createContext(ctx);
  vm.runInContext(source, ctx);
  return ctx;
}
class Segmenter {
  segment() {
    return [
      { segment: '自然语言', isWordLike: true },
      { segment: '处理', isWordLike: true },
      { segment: '自然语言', isWordLike: true },
      { segment: '，', isWordLike: false },
      { segment: 'apple', isWordLike: true }
    ];
  }
}
const modern = load({ Segmenter });
assert.deepStrictEqual(Array.from(modern.tokenizeChinese('ignored')), ['自然语言', '处理', '自然语言']);
const modernWords = modern.deduplicateSubstrings(modern.sortFreq(modern.countFrequency(modern.tokenizeChinese('ignored'))));
assert.strictEqual(modernWords[0].word, '自然语言');
assert.strictEqual(modernWords[0].count, 2);
const legacy = load({});
const legacyWords = legacy.deduplicateSubstrings(legacy.sortFreq(legacy.countFrequency(legacy.tokenizeChinese('自然语言自然语言'))));
assert(legacyWords.some(x => x.word === '自然语言' && x.count === 2));
assert(!legacyWords.some(x => x.word === '自然语' || x.word === '自然'));
const distinct = legacy.deduplicateSubstrings([{ word: '自然', count: 3 }, { word: '自然语言', count: 2 }]);
assert(distinct.some(x => x.word === '自然'), 'higher-frequency shorter term must survive');
assert.deepStrictEqual(Array.from(modern.tokenizeEnglish('Apple apple banana')), ['apple', 'apple', 'banana']);
console.log('keyword extraction: modern, fallback, frequency and English checks passed');
