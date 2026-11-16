#!/usr/bin/env node
/**
 * js/tool-kit.js chart.refBar 开放区间回归
 *
 * 背景（复核失败 810/816/827）：旧实现用 num(b.lo/hi) 归一化，num(null)=0，
 * 开放区间 {lo:null} / {hi:null} 被压成 0，末段变 [6,0) / [91,0) / [32,0)，
 * 高分永远落不进红带。此处直接断言归一化结果（不依赖 SVG 渲染）。
 *
 * 用法：node scripts/verify_toolkit_refbar.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function elStub(tag) {
  return {
    tagName: tag,
    style: {},
    attributes: {},
    children: [],
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this.attributes[k] = String(v); },
    getAttribute(k) { return Object.prototype.hasOwnProperty.call(this.attributes, k) ? this.attributes[k] : null; },
    addEventListener() {},
    querySelector() { return null; },
    querySelectorAll() { return []; },
  };
}

global.window = {};
global.location = { search: '' };
global.document = {
  readyState: 'complete',
  documentElement: { lang: 'zh-CN' },
  head: elStub('head'),
  body: elStub('body'),
  createElement: elStub,
  createElementNS: (_ns, tag) => elStub(tag),
  createTextNode: (t) => ({ nodeType: 3, textContent: String(t) }),
  getElementById() { return null; },
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
};

const src = fs.readFileSync(path.join(__dirname, '..', 'js', 'tool-kit.js'), 'utf8');
vm.runInThisContext(src, { filename: 'js/tool-kit.js' });
const K = global.window.TBKit;
if (!K || !K.chart || typeof K.chart._refBands !== 'function') {
  console.error('FAIL: TBKit.chart._refBands 未导出');
  process.exit(1);
}

const CASES = [
  {
    name: 'Glasgow 8 分应落「危重」红带',
    cfg: {
      value: 8,
      bands: [
        { lo: null, hi: 3, label: { zh: '轻症', en: 'Mild' } },
        { lo: 3, hi: 6, label: { zh: '重症', en: 'Severe' } },
        { lo: 6, hi: null, label: { zh: '危重', en: 'Critical' } },
      ],
    },
    check: (n) => n.hit === 2 && n.lo0 < 3 && n.hi0 > 8 && n.bands[0].lo === null && n.bands[2].hi === null,
  },
  {
    name: 'LSAS 95 分应落「极重度」末段',
    cfg: {
      value: 95,
      bands: [
        { lo: 0, hi: 61 }, { lo: 61, hi: 71 }, { lo: 71, hi: 81 },
        { lo: 81, hi: 91 }, { lo: 91, hi: null, label: { zh: '极重度', en: 'Very severe' } },
      ],
    },
    check: (n) => n.hit === 4 && n.lo0 === 0 && n.hi0 > 95,
  },
  {
    name: 'AQ 32 分应落「临床显著」末段',
    cfg: {
      value: 32,
      bands: [
        { lo: 0, hi: 26 }, { lo: 26, hi: 32 },
        { lo: 32, hi: null, label: { zh: '临床显著', en: 'Clinically significant' } },
      ],
    },
    check: (n) => n.hit === 2 && n.hi0 > 32,
  },
  {
    name: '显式 0 边界不得被当成缺省（0 是合法刻度）',
    cfg: { value: 7, bands: [{ lo: 0, hi: 5 }, { lo: 5, hi: 10 }] },
    check: (n) => n.bands[0].lo === 0 && n.hit === 1,
  },
];

let pass = 0;
const fails = [];
for (const c of CASES) {
  const n = K.chart._refBands(c.cfg);
  if (n && c.check(n)) {
    pass++;
    console.log(`PASS ${c.name}  →  hit=${n.hit} lo0=${n.lo0.toFixed(2)} hi0=${n.hi0.toFixed(2)}`);
  } else {
    fails.push(c.name);
    console.log(`FAIL ${c.name}  →  ${JSON.stringify(n)}`);
  }
}
console.log(`\nrefBar 开放区间回归：${pass}/${CASES.length}`);
if (fails.length) process.exit(1);
