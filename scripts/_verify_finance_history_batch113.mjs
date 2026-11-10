// 第 113 批真机回归：接手复核方「快速输入不丢最后一次 + 结论按业务状态判定」收尾。
// JSDOM 真机 + 真实 js/tool-kit.js，覆盖页面输出 → 历史 __tbScore → 趋势 → 表格 → CSV。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const todo = JSON.parse(readFileSync('/tmp/todo72.json', 'utf8'));
const byF = Object.fromEntries(todo.map(r => [r.f.replace('.html', ''), r]));

const cases = [
  ['cnpj-validator', 'input', ['11222333000181'], '11.222.333/0001-80'],
  ['dea-validator', 'input', ['AB1234563', 'AB1234567'], 'ABC123'],
  ['ein-validator', 'input', ['123456789'], 'abc123测试'],
  ['esn-validator', 'input', ['0A1B2C3D', '12345678901'], '123'],
  ['gst-validator', 'input', ['27AAPFU0939F1ZV'], '00AAPFU0939F1ZB'],
  ['iban-validator', 'ibanInput', ['DE89370400440532013000'], '000000000'],
  ['iccid-validator', 'input', ['8930123456789012347'], 'abc123测试'],
  ['ifsc-validator', 'input', ['SBIN0001234'], 'G1234567X'],
  ['imei-validator', 'input', ['490154203237518'], '490154203237517'],
  ['imsi-validator', 'input', ['310150123456789'], 'abc123测试'],
  ['ird-validator', 'input', ['49091850'], 'abc123测试'],
  ['isbn-validator', 'isbnInput', ['9780306406157'], '9780306406158'],
];

let failed = false;
const results = [];
for (const [slug, inputId, valids, invalid] of cases) {
  const prefix = byF[slug].pref;
  const downloads = [], trends = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8'), {
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
  const reset = () => { w.TBKit.history.clear(); w.eval(`${prefix}_last=0`); };
  check('加载无脚本异常', !jsErr && !!el);

  // 1) 合法值判通过
  reset();
  let validHit = null;
  for (const v of valids) {
    reset(); enter(v);
    if (w.TBKit.history.list()[0]?.d.__tbScore === 1) { validHit = v; break; }
  }
  check(`合法值记通过 (${validHit ?? 'none'})`, validHit !== null);

  // 2) 非法值记未通过（长/乱输入不再冒充通过）
  reset(); enter(invalid);
  check('非法值记未通过', w.TBKit.history.list()[0]?.d.__tbScore === 0);

  // 3) 快速连续输入后导出：导出前强制刷新，拿到最后一次失败
  reset();
  enter(validHit ?? valids[0]); enter(invalid);
  const exportBtn = doc.querySelector(`[onclick="${prefix}Export()"]`);
  if (exportBtn) {
    exportBtn.click();
    const recs = w.TBKit.history.list();
    check('导出强制刷新含最新失败', recs.length === 2 && recs[0].d.__tbScore === 0 && downloads[0]?.includes('未通过'));
  } else {
    check('存在导出入口', false);
  }

  // 4) 节流结束后保留最后一次输入
  reset();
  enter(validHit ?? valids[0]); enter(invalid); enter('9'.repeat(40));
  await new Promise(res => setTimeout(res, 1150));
  const tail = w.TBKit.history.list()[0]?.d;
  const tailOk = tail?.[inputId] === '9'.repeat(40) && tail?.__tbScore === 0;
  check('节流结束保留最终输入', tailOk);
  if (!tailOk) console.log(`  DIAG tail=`, JSON.stringify({ input: tail?.[inputId], score: tail?.__tbScore, count: w.TBKit.history.list().length }));

  // 5) 趋势含真实通过与失败
  check('趋势含通过与未通过', trends.some(t => t.includes(1) && t.includes(0)));
  w.close();
}
console.log(`\n=== BATCH113 ${failed ? 'FAILED' : 'ALL PASS'} | failed=${results.length} ===`);
if (results.length) console.log(results.join('\n'));
process.exit(failed ? 1 : 0);
