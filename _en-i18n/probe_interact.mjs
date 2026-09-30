import { chromium } from 'playwright';
import fs from 'fs';
const BASE = process.env.AUDIT_BASE || 'http://127.0.0.1:8774';
const pages = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const outArg = process.argv[3];
// 计算类动词（中英双语）：EN 态下按钮文本已被字典译为英文
const COMPUTE = /^(计算|生成|分析|执行|运行|开始|评估|检测|查询|转换|运算|统计|测一测|测测|立即|提交|解析|处理|Calculate|Compute|Generate|Analyse|Analyze|Run|Start|Evaluate|Convert|Process|Submit|Query|Parse|Detect|Measure|Simulate|Build|Create|Compare|Test|Check|Add|Insert|Find|Extract)/i;
const SKIP = /^(重置|清空|清除|复位|复制|下载|分享|导出|打印|保存|折叠|展开|切换|中文|Reset|Clear|Copy|Download|Share|Export|Print|Save|Toggle|Theme|Favorites|Recent|Hot|Menu|Close|Set|Show|Hide|Open|Back|Next|Prev)/i;
const NAVCLS = /nav|tb-nav|icon-btn|breadcrumb|theme|toc|share/i;
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1360, height: 900 } });
await ctx.route('**/*', r => { const u = r.request().url(); if (/\/sw\.js(\?|$)/.test(u)) return r.abort(); return r.continue(); });
const res = {};
const scanCJK = (p) => p.evaluate(() => {
  const out = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while (n = w.nextNode()) {
    const s = (n.nodeValue || '').trim();
    if (!s) continue;
    if (!/[\u4e00-\u9fff]/.test(s)) continue;
    const el = n.parentElement; if (!el) continue;
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') continue;
    if (el.closest('[class*=lang],[id*=lang],[class*=Lang],[id*=Lang],[class*=locale]')) continue;
    out.push(s.slice(0, 120));
  }
  return [...new Set(out)];
});
let n = 0;
for (const pg of pages) {
  n++;
  const p = await ctx.newPage();
  try {
    await p.goto(BASE + pg + '?lang=en-US', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await p.waitForTimeout(1100);
    const before = await scanCJK(p);
    const btns = await p.$$('button, input[type=submit], [role=button], a.btn');
    let clicked = 0;
    for (const btn of btns) {
      let t = '';
      try { t = (await btn.innerText()).trim(); } catch (e) { }
      if (!t) { try { t = (await btn.getAttribute('value')) || ''; } catch (e) { } }
      if (!t) continue;
      let cls = '';
      try { cls = (await btn.getAttribute('class')) || ''; } catch (e) { }
      if (NAVCLS.test(cls)) continue;
      if (COMPUTE.test(t) && !SKIP.test(t)) {
        try { await btn.click({ timeout: 1500 }); clicked++; await p.waitForTimeout(600); } catch (e) { }
        if (clicked >= 3) break;
      }
    }
    await p.waitForTimeout(700);
    const after = await scanCJK(p);
    const newOnes = after.filter(s => !before.includes(s));
    res[pg] = { clicked, beforeN: before.length, afterN: after.length, newOnes };
  } catch (e) {
    res[pg] = { error: String(e).slice(0, 140) };
  }
  await p.close();
  if (n % 100 === 0) { console.log('progress', n, '/', pages.length); fs.writeFileSync(outArg, JSON.stringify(res, null, 1)); }
}
fs.writeFileSync(outArg, JSON.stringify(res, null, 1));
console.log('done', Object.keys(res).length, 'pages');
await b.close();
