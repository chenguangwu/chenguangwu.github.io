// 真机「断词 garble」探针：只抓由 i18n 替换层产出的中英夹杂断词。
// 判据：英文字母紧邻汉字（无空格），如 "Mass分数"、"Time 格式"→不算（有空格）… 所以同时用两种签名：
//   MIX_ADJ  = [A-Za-z][\u4e00-\u9fff] | [\u4e00-\u9fff][A-Za-z]   （紧邻断词）
//   MIX_ANY  = 同串同时含拉丁与汉字                                  （广义混排残留）
// 关键：只报「EN 态出现、简中源态不出现」的串 = 替换层造出来的，排除源码自带（如 "JSON格式化"）。
// 用法: node _en-i18n/probe_garble.mjs <pages.json> <out.json> [baseUrl]
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';

const pages = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const outPath = process.argv[3] || '/tmp/en_audit/garble_probe.json';
const BASE = process.argv[4] || process.env.AUDIT_BASE || 'http://127.0.0.1:8774';

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1360, height: 900 } });
await ctx.route('**/*', (r) => {
  const u = r.request().url();
  if (/\/sw\.js(\?|$)/.test(u)) return r.abort();
  if (/\.(png|jpe?g|gif|webp|avif|woff2?|ttf|eot)(\?|$)/.test(u)) return r.abort();
  return r.continue();
});

const COMPUTE = /^(计算|生成|分析|执行|运行|开始|评估|检测|查询|转换|运算|统计|测一测|测测|立即|提交|解析|处理|Calculate|Compute|Generate|Analyse|Analyze|Run|Start|Evaluate|Convert|Process|Submit|Query|Parse|Detect|Measure|Simulate|Build|Create|Compare|Test|Check|Add|Insert|Find|Extract)/i;
const SKIP = /^(重置|清空|清除|复位|复制|下载|分享|导出|打印|保存|折叠|展开|切换|中文|Reset|Clear|Copy|Download|Share|Export|Print|Save|Toggle|Theme|Favorites|Recent|Hot|Menu|Close|Set|Show|Hide|Open|Back|Next|Prev)/i;
const NAVCLS = /nav|tb-nav|icon-btn|breadcrumb|theme|toc|share/i;

const scan = (p) => p.evaluate(() => {
  const CJK = /[\u4e00-\u9fff]/;
  const LAT = /[A-Za-z]/;
  const ADJ = /[A-Za-z][\u4e00-\u9fff]|[\u4e00-\u9fff][A-Za-z]/;
  const out = [];
  const push = (s) => {
    s = (s || '').trim();
    if (!s || !CJK.test(s) || !LAT.test(s)) return;
    out.push({ t: s.slice(0, 140), adj: ADJ.test(s) });
  };
  const isSwitcher = (el) => { let c = el; while (c && c.nodeName && c.nodeName.toLowerCase() !== 'body') { const cls = (c.getAttribute && c.getAttribute('class')) || ''; if (/(^|\s)lang-switcher(\s|$)/.test(cls)) return true; c = c.parentNode; } return false; };
  document.querySelectorAll('body *').forEach((el) => {
    if (/SCRIPT|STYLE|NOSCRIPT/.test(el.tagName)) return;
    if (isSwitcher(el)) return;
    if (el.offsetParent === null && el.tagName !== 'BODY') return;
    Array.from(el.childNodes).filter((n) => n.nodeType === 3).forEach((n) => push(n.textContent));
    ['placeholder', 'title', 'aria-label', 'alt'].forEach((a) => { const v = el.getAttribute(a); if (v) push(v); });
  });
  return out;
});

async function loadAndScan(page, url, interact) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(1500);
  if (interact) {
    const btns = await page.$$('button, input[type=submit], [role=button], a.btn');
    let clicked = 0;
    for (const btn of btns) {
      let t = ''; try { t = (await btn.innerText()).trim(); } catch (e) { }
      if (!t) { try { t = (await btn.getAttribute('value')) || ''; } catch (e) { } }
      if (!t) continue;
      let cls = ''; try { cls = (await btn.getAttribute('class')) || ''; } catch (e) { }
      if (NAVCLS.test(cls)) continue;
      if (COMPUTE.test(t) && !SKIP.test(t)) {
        try { await btn.click({ timeout: 1500 }); clicked++; await page.waitForTimeout(500); } catch (e) { }
        if (clicked >= 3) break;
      }
    }
    await page.waitForTimeout(600);
  }
  return scan(page);
}

const report = {};
let done = 0, pagesWithGarble = 0, totAdj = 0, totAny = 0;

for (const pg of pages) {
  const page = await ctx.newPage();
  try {
    const en = await loadAndScan(page, BASE + pg + '?lang=en-US', true);
    const zh = await loadAndScan(page, BASE + pg, false);
    const zhSet = new Set(zh.map((x) => x.t));
    const enMap = new Map(en.map((x) => [x.t, x.adj]));
    const garble = [];
    for (const [t, adj] of enMap) {
      if (zhSet.has(t)) continue;         // 源态也有 ⇒ 非替换层所致
      garble.push({ t, adj });
    }
    const adjList = garble.filter((g) => g.adj);
    if (garble.length) pagesWithGarble++;
    totAdj += adjList.length; totAny += garble.length;
    if (garble.length) report[pg] = garble;
  } catch (e) {
    report[pg] = { error: String(e).slice(0, 160) };
  }
  await page.close();
  done++;
  if (done % 20 === 0) console.log(`progress ${done}/${pages.length} pagesWithGarble=${pagesWithGarble} adj=${totAdj} any=${totAny}`);
}

await browser.close();
mkdirSync('/tmp/en_audit', { recursive: true });
writeFileSync(outPath, JSON.stringify(report, null, 1));
console.log('DONE pages=', pages.length, 'pagesWithGarble=', pagesWithGarble, 'adjGarble=', totAdj, 'anyMixed=', totAny);
console.log('report ->', outPath);
