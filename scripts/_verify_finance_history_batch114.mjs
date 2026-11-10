// 第 114 批真机回归：接手复核方收尾（校验/查找族 14 页）。
// JSDOM 真机 + 真实 js/tool-kit.js，覆盖页面输出 → 历史 __tbScore → 趋势 → 表格 → CSV 导出。
// 重点：1 秒节流不得丢最后一次操作；结论必须按本页业务状态判定，不靠关键词词表。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';

// [slug, 主输入 id, 合法值（按本页算法实测）, 非法值, 结果容器 id]
const cases = [
  ['bic-lookup', 'input', 'DEUTDEFF500', 'abc123测试', 'output'],
  ['credit-card-validator', 'cardInput', '4532015112830366', 'abc123测试', 'result'],
  ['currency-lookup', 'input', 'USD', 'abc123测试', 'output'],
  ['msisdn-validator', 'input', '49155402372518', 'abc123测试', 'output'],
  ['nie-validator', 'input', 'Z1234567R', 'abc123测试', 'output'],
  ['npi-validator', 'input', '1234567893', 'abc123测试', 'output'],
  ['nric-validator', 'input', 'S1234567D', 'abc123测试', 'output'],
  ['postal-code-validator', 'input', '100000', 'abc123测试', 'output'],
  ['routing-number-validator', 'input', '011000015', 'abc123测试', 'output'],
  ['sin-validator', 'input', '130692544', 'abc123测试', 'output'],
  ['swift-bic-validator', 'input', 'DEUTDEFF500', 'abc123测试', 'output'],
  ['uan-validator', 'input', '333333333333', 'abc123测试', 'output'],
  ['voter-id-validator', 'input', 'ABC1234567', 'abc123测试', 'output'],
  ['zip-code-validator', 'input', '95014', 'abc123测试', 'output'],
];

let failed = false;
const results = [];
for (const [slug, inputId, valid, invalid, contId] of cases) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const pm = html.match(/var (__[A-Za-z0-9_]+)_last=0,/);
  const prefix = pm?.[1];
  const downloads = [], trends = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = { showToast() {}, escHtml: s => String(s) };
      w.i18nText = k => k;
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.eval(readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8'));
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (h, c) => { trends.push(Array.from(c.series[0].data)); return line(h, c); };
    }
  });
  const w = dom.window, doc = w.document, el = doc.getElementById(inputId);
  await new Promise(res => w.addEventListener('load', res));
  const check = (label, ok) => {
    console.log(`${ok ? 'PASS' : 'FAIL'} ${slug} ${label}`);
    if (!ok) { failed = true; results.push(`${slug} ${label}`); }
  };
  const enter = v => { el.value = v; el.dispatchEvent(new w.Event('input', { bubbles: true })); };
  const reset = () => { w.TBKit.history.clear(); if (prefix) w.eval(`${prefix}_last=0`); };
  const resultText = () => (doc.getElementById(contId)?.textContent || '').replace(/\s+/g, ' ').trim();
  check('加载无脚本异常且有输入与前缀', !jsErr && !!el && !!prefix);

  // 1) 合法值：页面判定有效，历史必须记通过
  reset(); enter(valid);
  const validRec = w.TBKit.history.list()[0];
  check(`合法值记通过 (${valid})`, validRec?.d.__tbScore === 1);

  // 2) 非法值：页面输出拒绝/警告，历史必须记未通过
  reset(); enter(invalid);
  const invalidRec = w.TBKit.history.list()[0];
  check('非法值记未通过', invalidRec?.d.__tbScore === 0);
  if (invalidRec?.d.__tbScore !== 0) console.log(`  DIAG invalid=`, JSON.stringify({ txt: resultText().slice(0, 150), score: invalidRec?.d.__tbScore }));

  // 3) 快速连续输入后点导出：导出前强制刷新，必须拿到最后一次失败
  reset();
  enter(valid); enter(invalid);
  const exportBtn = prefix && doc.querySelector(`[onclick="${prefix}Export()"]`);
  if (exportBtn) {
    exportBtn.click();
    const recs = w.TBKit.history.list();
    check('导出强制刷新含最新失败', recs.length === 2 && recs[0].d.__tbScore === 0 && downloads[0]?.includes('未通过'));
  } else check('存在导出入口', false);

  // 4) 节流结束保留最后一次输入（尾部定时器，不能丢最后一次）
  const tailVal = '9'.repeat(40);
  reset();
  enter(valid); enter(invalid); enter(tailVal);
  await new Promise(res => setTimeout(res, 1150));
  const tail = w.TBKit.history.list()[0]?.d;
  const tailOk = tail?.[inputId] === tailVal && tail?.__tbScore === 0;
  check('节流结束保留最终输入', tailOk);
  if (!tailOk) console.log(`  DIAG tail=`, JSON.stringify({ input: tail?.[inputId], score: tail?.__tbScore, count: w.TBKit.history.list().length }));

  // 5) 趋势同时含真实通过与失败
  check('趋势含通过与未通过', trends.some(t => t.includes(1) && t.includes(0)));
  w.close();
}
console.log(`\n=== BATCH114 ${failed ? 'FAILED' : 'ALL PASS'} | ${cases.length} pages x 6 checks | failed=${results.length} ===`);
if (results.length) console.log(results.join('\n'));
process.exit(failed ? 1 : 0);
