// 第 118 批真机回归：接手复核方收尾（文本族 / 密码族 / 剩余计算页 10 页）。
// 覆盖：真实入口漏包装、结果容器错配、按业务状态判结论、节流不丢最后一次、导出强制刷新、趋势。
// 两种模式：
//   calc —— 页面有真实拒绝态，断言合法记 1 / 非法记 0 / 趋势含 1 与 0。
//   text —— 纯文本或 range 归一化工具，没有业务失败态，断言连续输入每次都记 1 且尾部不丢。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';

const cases = [
  // --- 有真实拒绝态 ---
  // number-to-words：number input 把非数字归一化为 ''；尾部改用另一个合法值 88（Score=1），
  // 这样「旧实现丢最后一次」也会变红，不依赖两个不同的非法字符串。
  { slug: 'number-to-words', id: 'inputVal', mode: 'calc', invalid: 'abc123测试', tail: '88', tailScore: 1, buttonEach: true },
  { slug: 'tax-bracket', id: 'income', mode: 'calc', invalid: '-1', tail: '-7', tailScore: 0, buttonEach: true },
  { slug: 'vat-calculator', id: 'customRate', mode: 'calc', invalid: '-1', tail: '-7', tailScore: 0, buttonEach: false },
  // --- 无业务失败态（Score 恒 1 属正确判定）---
  { slug: 'mirror-text', id: 'input', mode: 'text', alt: 'Alpha Beta ToolBox', tail: 'Gamma Delta 中文', buttonEach: false },
  { slug: 'text-reverse-words', id: 'input', mode: 'text', alt: 'One Two Three', tail: 'Four Five 中文', buttonEach: false },
  { slug: 'word-frequency', id: 'input', mode: 'text', alt: 'alpha beta alpha', tail: 'gamma delta gamma', buttonEach: false },
  { slug: 'word-wrap', id: 'input', mode: 'text', alt: '需要换行的第二段文本内容', tail: '第三段换行测试文本 ToolBox', buttonEach: false },
  { slug: 'vcard-qr', id: 'fn', mode: 'text', alt: '李', tail: '王', buttonEach: true },
  // range 输入会被浏览器归一化到 min=4，长度非法态不存在；生成入口是按钮，必须每次点。
  { slug: 'password', id: 'pwLen', mode: 'text', alt: '24', tail: '32', buttonEach: true },
  { slug: 'password-generator-advanced', id: 'len', mode: 'text', alt: '28', tail: '36', buttonEach: true },
];

let failed = false;
const results = [];
for (const c of cases) {
  const { slug, id, mode, buttonEach } = c;
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const prefix = html.match(/var (__[A-Za-z0-9_]+)_last=0,/)?.[1];
  const downloads = [], trends = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s),
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '', copyText() {}, downloadText() {}, toggleToolTheme() {},
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8'));
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (h, cfg) => { trends.push(Array.from(cfg.series[0].data)); return line(h, cfg); };
    }
  });
  const w = dom.window, doc = w.document, el = doc.getElementById(id);
  await new Promise(res => w.addEventListener('load', res));
  const check = (label, ok) => {
    console.log(`${ok ? 'PASS' : 'FAIL'} ${slug} ${label}`);
    if (!ok) { failed = true; results.push(`${slug} ${label}`); }
  };
  const btns = Array.from(doc.querySelectorAll('button[onclick]')).filter(b => {
    const o = b.getAttribute('onclick') || '';
    return /^calc\(|^calcTool\(|^generatePW\(|^generate\(|^convert\(|^reverse\(|^wrap\(|^analyze\(/.test(o);
  });
  const valid = el?.value ?? '';
  const reset = () => { w.TBKit.history.clear(); if (prefix) w.eval(`${prefix}_last=0;${prefix}_skip=false`); };
  const enter = v => {
    el.value = v;
    el.dispatchEvent(new w.Event('input', { bubbles: true }));
    if (buttonEach && btns.length) { try { btns[0].click(); } catch (e) {} }
    else if (!w.TBKit.history.list().length && btns.length) { try { btns[0].click(); } catch (e) {} }
  };
  check('加载无脚本异常且有输入与前缀', !jsErr && !!el && !!prefix);

  // 1) 默认输入记通过
  reset(); enter(valid);
  const vRec = w.TBKit.history.list()[0];
  check('默认输入记通过', vRec?.d.__tbScore === 1);
  if (vRec?.d.__tbScore !== 1) console.log('  DIAG valid=', JSON.stringify({ score: vRec?.d.__tbScore, n: w.TBKit.history.list().length, jsErr }));

  if (mode === 'calc') {
    // 2) 非法输入记未通过
    reset(); enter(c.invalid);
    const iRec = w.TBKit.history.list()[0];
    check('非法参数记未通过', iRec?.d.__tbScore === 0);
    if (iRec?.d.__tbScore !== 0) console.log('  DIAG invalid=', JSON.stringify({ score: iRec?.d.__tbScore, n: w.TBKit.history.list().length }));

    // 3) 导出强制刷新含最新失败
    reset(); enter(valid); enter(c.invalid);
    const exportBtn = prefix && doc.querySelector(`[onclick="${prefix}Export()"]`);
    if (exportBtn) {
      exportBtn.click();
      const recs = w.TBKit.history.list();
      const ok = recs.length >= 2 && recs[0].d.__tbScore === 0 && downloads.length > 0 && String(downloads[0]).length > 0;
      check('导出强制刷新含最新失败', ok);
      if (!ok) console.log('  DIAG export=', JSON.stringify({ n: recs.length, scores: recs.map(r => r.d.__tbScore), dl: downloads.map(d => String(d).slice(0, 80)) }));
    } else check('存在导出入口', false);

    // 4) 节流收尾
    reset(); enter(valid); enter(c.invalid); enter(c.tail);
    await new Promise(res => setTimeout(res, 1150));
    const tail = w.TBKit.history.list()[0]?.d;
    const tailOk = tail?.[id] === c.tail && tail?.__tbScore === c.tailScore;
    check('节流结束保留最终输入', tailOk);
    if (!tailOk) console.log('  DIAG tail=', JSON.stringify({ input: tail?.[id], score: tail?.__tbScore, n: w.TBKit.history.list().length }));

    check('趋势含通过与未通过', trends.some(t => t.includes(1) && t.includes(0)));
  } else {
    // 2) 换成另一个明确不同的输入，也要记一条且快照带该值。
    // 单独一次输入（reset 把 _last 归零，不会被节流挂起）；连续输入的节流收尾由第 4 项覆盖。
    reset(); enter(c.alt);
    const aRec = w.TBKit.history.list()[0];
    const altOk = aRec?.d.__tbScore === 1 && String(aRec?.d?.[id]) === String(el.value);
    check('换值输入记通过且快照带新值', altOk);
    if (!altOk) console.log('  DIAG alt=', JSON.stringify({ score: aRec?.d.__tbScore, snap: aRec?.d?.[id], live: el.value, n: w.TBKit.history.list().length }));

    // 3) 导出强制刷新含最后一次输入
    reset(); enter(valid); enter(c.alt);
    const exportBtn = prefix && doc.querySelector(`[onclick="${prefix}Export()"]`);
    if (exportBtn) {
      exportBtn.click();
      const recs = w.TBKit.history.list();
      const ok = recs.length >= 2 && String(recs[0].d?.[id]) === String(c.alt) && downloads.length > 0 && String(downloads[0]).length > 0;
      check('导出强制刷新含最后一次输入', ok);
      if (!ok) console.log('  DIAG export=', JSON.stringify({ n: recs.length, snap: recs[0]?.d?.[id], want: c.alt, dl: downloads.map(d => String(d).slice(0, 80)) }));
    } else check('存在导出入口', false);

    // 4) 连续三次输入后，节流收尾必须落在最后一次
    reset(); enter(valid); enter(c.alt); enter(c.tail);
    await new Promise(res => setTimeout(res, 1150));
    const tail = w.TBKit.history.list()[0]?.d;
    const tailOk = String(tail?.[id]) === String(c.tail) && tail?.__tbScore === 1;
    check('节流结束保留最终输入', tailOk);
    if (!tailOk) console.log('  DIAG tail=', JSON.stringify({ input: tail?.[id], score: tail?.__tbScore, want: c.tail, n: w.TBKit.history.list().length }));

    check('趋势含连续通过记录', trends.some(t => t.length >= 2 && t.every(v => v === 1)));
  }
  w.close();
}
console.log(`\n=== BATCH118 ${failed ? 'FAILED' : 'ALL PASS'} | ${cases.length} pages x 6 checks | failed=${results.length} ===`);
if (results.length) console.log(results.join('\n'));
process.exit(failed ? 1 : 0);
