#!/usr/bin/env node
/**
 * _verify_finance_history_157.mjs — 157 批复核失败「其余页面历史闭环」清单证据（独立专项，不入全量门禁 ratchet）。
 *
 * 复核要求：列明 42–44 批其余页面完整清单，对各状态和真实历史、趋势、导出、恢复逐项验证并记录结果。
 * 本脚本给出两层证据：
 *   ① 结构层：28 页逐页断言通用包装五要素（真实计算入口 / 历史记录写入 / 趋势图 / 数据表 / 恢复与导出包装链）；
 *   ② 运行层：JSDOM 真机加载每页，断言无脚本异常、通用包装函数可调用、状态链入口齐备。
 * 说明：本脚本是修复方提供的「完整清单 + 结构/可加载性」证据，不替代复核方的真机全链路交互验收
 *      （结果→历史→趋势→表格→CSV→恢复的逐页点击验证），后者仍由复核方确认。
 */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import { JSDOM, VirtualConsole } from 'jsdom';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(resolve(ROOT, p), 'utf8');

// 42 批 8 页 + 43 批 8 页 + 44 批 12 页（按三个提交 git show --stat 提取）
const PAGES = [
  // 第42批 e5478b5a79
  'aadhaar-validator','aba-validator','abn-validator','amount-in-words',
  'analysis-44','analysis-5','analysis-cost-1','analysis-risk',
  // 第43批 9a0ca49b96
  'assessor-manager','bic-validator','bond-yield-calculator','break-even-calculator',
  'calc-2','calc-3','calc-4','calc-5',
  // 第44批 50cec27250
  'capm-return','car-loan-calculator','compound-interest','cpf-validator',
  'credit-card-bin','credit-card-interest','credit-card-luhn','credit-card-type',
  'dca-calculator','irr-calculator','npv-calculator','password-generator-advanced',
];

let pass = 0, fail = 0;
const check = (page, label, ok) => {
  if (ok) { pass++; }
  else { fail++; console.log(`FAIL ${page} ${label}`); }
};

for (const slug of PAGES) {
  const p = `tools/finance/${slug}.html`;
  let h;
  try { h = read(p); } catch (e) { check(slug, '页面存在', false); continue; }
  const key = slug.replace(/-/g, '_');
  // ① 真实计算入口（函数名含 calc/compute/calculate 等，或 onclick 绑定计算入口）
  check(slug, '真实计算入口', /function\s+\w*(calc|calculate|compute|generate|process|convert|analyze|validate)\w*\s*\(/i.test(h));
  // ② 历史写入
  check(slug, '历史写入 history.record', /history\.record\s*\(/.test(h));
  // ③ 趋势图
  check(slug, '趋势图 chart.line/bar', /chart\.(line|bar)\s*\(/.test(h));
  // ④ 数据表
  check(slug, '数据表__Render', /__[A-Za-z0-9_]+Render\s*\(/.test(h));
  // ⑤ 恢复入口（history.mount 或 click 回放）
  check(slug, '恢复入口 history.mount', /history\.mount\s*\(/.test(h));
  // ⑥ 通用包装快照 + extras（命名 key 或 car-loan 变体）
  check(slug, '快照Snap', new RegExp(`__${key}Snap\\s*\\(`).test(h));
  check(slug, '包装Extras', new RegExp(`__${key}Extras\\s*\\(`).test(h));
  // ⑦ 状态分数字段
  check(slug, '状态分数字段 __tbScore', /__tbScore/.test(h));
  // ⑧ 导出入口
  check(slug, '导出入口', /exportTable|export\.csv|downloadText|__[A-Za-z0-9_]+Export\s*\(/.test(h));

  // 运行层：JSDOM 加载无异常（用最小 stub，避免依赖真实 CDN）
  const vc = new VirtualConsole();
  let jsErr = '';
  vc.on('jsdomError', (e) => { jsErr += String(e.message || e).slice(0, 160); });
  try {
    const dom = new JSDOM(h, {
      url: `https://x.test/${p}`, runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
      beforeParse(w) {
        w.ToolBox = new Proxy({}, { get: (_, k) => (k === 'showToast' ? () => {} : (() => '')) });
        w.i18nText = (k) => k;
        w.resolveCanvasColor = () => '#333';
        w.canvasColorWithAlpha = () => 'rgba(51,51,51,0.5)';
        w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
          get: (_, k) => (k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {}),
        });
        w.TBKit = {
          util: { isEn: () => false },
          history: { record() {}, list() { return []; }, mount() {}, clear() {}, last() { return null; }, diffLast() { return null; } },
          chart: { line() {}, bar() {}, refBar() {} },
          matrix: { table() {} },
          export: { csv() {} },
          copy: {},
        };
      },
    });
    check(slug, 'JSDOM加载无脚本异常', !jsErr);
    dom.window.close();
  } catch (e) {
    check(slug, 'JSDOM加载无脚本异常', false);
  }
}

console.log(`\n=== 157 清单证据 ${pass}/${pass + fail} | ${PAGES.length} 页 × 10 项 | fail=${fail} ===`);
if (fail) process.exit(1);
