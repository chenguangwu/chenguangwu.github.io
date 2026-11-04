#!/usr/bin/env node
/**
 * 页内数字自洽扫描器（只报偏差，不自动改）
 *
 * 用法：
 *   node scripts/audit_page_numbers.js                       # 跑内置用例页
 *   node scripts/audit_page_numbers.js civil/masonry-bearing # 指定页（默认态实跑）
 *   node scripts/audit_page_numbers.js --all-civil           # 扫描某行业全部页（默认态）
 *
 * 两类检查：
 *   A. 算式实算：抽取页面可见文本里的 `纯数字算式 =/≈ 数值`，本地求值比对。
 *   B. 示例 vs 输出：对内置用例页注入示例输入、真实点击「计算」，把示例段落里的
 *      结果数字与输出卡片数字比对；按 >10% / >1% / 四舍五入 分级。
 *
 * 只输出偏差清单，不修改任何文件。
 */
const fs = require('fs');
const path = require('path');
const http = require('http');
const puppeteer = require('/Users/cgw/node_modules/puppeteer-core');

const ROOT = path.resolve(__dirname, '..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

// 内置用例：示例段落使用了非默认输入，必须注入后实跑。
// inputs 取自页面 / 深挖示例（.dd-example）声明的算例输入。
const CASES = [
  { slug: 'civil/rebar-anchorage', inputs: { fy: '360', ft: '1.43', d: '20', za: '1.0' } },
  { slug: 'civil/calc-strength-ratio', inputs: { grade: '30', cement: '42.5', agg: 'crushed', water: '195', sp: '34' } },
  { slug: 'civil/concrete-wb-ratio', inputs: { fcu: '38.2', fb: '42.5', aa: '0.53', ab: '0.20' } },
  { slug: 'civil/masonry-bearing', inputs: { f: '1.5', b: '240', L: '3000', phi: '0.9', h0: '3000', mortar: '5' } },
  { slug: 'civil/wind-load', inputs: { w0: '0.45', mz: '1.39', ms: '0.8', bz: '1.6' } },
  { slug: 'construction/calc-1', inputs: { od: '48', thickness: '3.0', fy: '205', h: '1.8', k: '1.155', a: '0.3', area: '1.35', load: '2', self: '0.35' } },
  { slug: 'construction/calc-204', inputs: { lVal: '6', hVal: '3', qVal: '30', pAllow: '30' } },
  { slug: 'construction/calc-206', inputs: { qVal: '3', wVal: '0.5', mzVal: '1.0', msVal: '1.3', aVal: '1.5', hStep: '1.8', hVal: '30' } },
];

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2' };

function serve() {
  return new Promise(resolve => {
    const server = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      if (p.endsWith('/')) p += 'index.html';
      const f = path.join(ROOT, p);
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('404'); }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

function numTokens(s) {
  return (String(s).match(/[-+]?\d+(?:,\d{3})*(?:\.\d+)?/g) || [])
    .map(t => parseFloat(t.replace(/,/g, '')))
    .filter(n => Number.isFinite(n));
}

function fmt(n) { return Math.abs(n) >= 100 ? n.toFixed(1) : n.toPrecision(4); }

function grade(claim, actual) {
  const diff = Math.abs(claim - actual);
  const base = Math.max(Math.abs(claim), Math.abs(actual), 1e-9);
  const rel = diff / base;
  if (rel > 0.10) return '>10%';
  if (rel > 0.01) return '>1%';
  return '四舍五入';
}

function evaluate(expr, claim) {
  // 只接受纯数字算式（允许 1.5e3 科学计数），避免把公式符号（f_y、λ 等）误当表达式
  if (!/^[\d\s.,()+\-*/×÷^%eE]+$/.test(expr)) return null;
  let e = expr.replace(/,/g, '').replace(/×/g, '*').replace(/÷/g, '/').replace(/^\+/, '');
  e = e.replace(/(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)/g, 'Math.pow($1,$2)');
  if (!/^[\d\s().+\-*/eE]+$/.test(e.replace(/Math\.pow/g, ''))) return null;
  try {
    const v = Function('"use strict";return (' + e + ')')();
    return Number.isFinite(v) ? v : null;
  } catch (_) {
    return null;
  }
}

function collect(page) {
  return page.evaluate(() => {
    const vis = el => {
      const st = getComputedStyle(el);
      return st.display !== 'none' && st.visibility !== 'hidden' && el.getClientRects().length > 0;
    };
    const outSel = '#res,#result,.result-box,.data-grid,.data-card,#calc_1Table,#calc_204Table,#calc_206Table,.tbk-panel';
    return {
      example: textOf('.dd-example', false),
      notes: textOf('.tool-notes, .info-box', false),
      table: [...document.querySelectorAll('table td, table th')].map(el => el.innerText.trim()).join('\n'),
      output: textOf(outSel),
      body: textOf('.container'),
    };
    function textOf(sel, onlyVisible) {
      return [...document.querySelectorAll(sel)]
        .filter(el => (onlyVisible === false ? true : vis(el)))
        .map(el => el.innerText || el.textContent || '')
        .join('\n');
    }
  });
}

async function runCase(browser, base, c) {
  const page = await browser.newPage();
  await page.goto(base + '/tools/' + c.slug + '.html?lang=zh-CN', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForFunction('window.ToolBox && typeof window.ToolBox.setResult === "function"', { timeout: 15000 }).catch(() => {});
  const before = await collect(page);
  if (c.inputs) {
    await page.evaluate(inputs => {
      for (const [id, val] of Object.entries(inputs)) {
        const el = document.getElementById(id);
        if (!el) continue;
        el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }, c.inputs);
    const btn = await page.$('.toolbar .btn.primary, .btn.primary');
    if (btn) await btn.click();
    await new Promise(r => setTimeout(r, 450));
  }
  const after = await collect(page);
  await page.close();
  return { before, after };
}

function checkEquations(text, slug) {
  const rows = [];
  const re = /(?<![\w.×÷*/+\-^])([0-9][0-9\s.,()+\-*/×÷^%eE]{2,})\s*[=≈]\s*([-+]?\d+(?:\.\d+)?)/g;
  let m;
  while ((m = re.exec(text))) {
    const expr = m[1].trim();
    const claim = parseFloat(m[2]);
    if (!/[+\-*/×÷^]/.test(expr)) continue;
    // 右值后紧跟「/数字」说明这是分数中间值（如 22.5/42.7≈0.527），不是独立断言
    if (/^\s*\/\s*\d/.test(text.slice(re.lastIndex))) continue;
    const v = evaluate(expr, claim);
    if (v === null) continue;
    const rel = Math.abs(v - claim) / Math.max(Math.abs(claim), Math.abs(v), 1e-9);
    if (rel > 0.01) rows.push({ slug, kind: '算式', detail: `${expr} = ${claim}（实算 ${fmt(v)}）`, level: grade(claim, v), rel });
  }
  return rows;
}

function checkClaims(slug, exampleText, outputText) {
  const outNums = numTokens(outputText);
  if (!outNums.length) return [];
  const rows = [];
  const seen = new Set();
  // 只把示例段落里「≈ / 约 / 为 / 等于」后的数字当作结果声明，避免把 = 定义式当断言
  const re = /(?:[≈约]|为|等于)\s*([-+]?\d+(?:\.\d+)?)/g;
  let m;
  while ((m = re.exec(exampleText))) {
    const claim = parseFloat(m[1]);
    if (seen.has(claim)) continue;
    seen.add(claim);
    if (claim === 0 || Math.abs(claim) > 1e6) continue;
    // 跳过分数中间值与区间下限（如 22.5/42.7、30–40）
    if (/^\s*[/–\-]\s*\d/.test(exampleText.slice(re.lastIndex))) continue;
    // 精确/四舍五入命中：输出中存在同值或按声明小数位四舍五入后相同的数
    const dec = (m[1].split('.')[1] || '').length;
    const hit = outNums.some(n => Math.abs(n - claim) <= Math.pow(10, -dec) / 2 + 1e-9);
    if (hit) continue;
    let best = Infinity, bestN = 0;
    for (const n of outNums) { const d = Math.abs(n - claim); if (d < best) { best = d; bestN = n; } }
    rows.push({ slug, kind: '示例', detail: `页面 ${claim} vs 实算最接近 ${fmt(bestN)}`, level: grade(claim, bestN), rel: best / Math.max(Math.abs(claim), Math.abs(bestN), 1e-9) });
  }
  return rows;
}

(async () => {
  const args = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const server = await serve();
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'] });
  const rows = [];
  let cases = CASES;
  if (args.length) cases = args.map(s => ({ slug: s }));
  for (const c of cases) {
    try {
      const r = await runCase(browser, base, c);
      if (process.env.AUDIT_DEBUG) console.log('[debug]', c.slug, 'ex=', r.after.example.length, 'out=', r.after.output.length, 'exText=', r.after.example.slice(0, 80).replace(/\n/g, ' '));
      rows.push(...checkEquations(r.after.example + '\n' + r.after.notes + '\n' + r.after.table, c.slug));
      if (c.inputs) rows.push(...checkClaims(c.slug, r.after.example, r.after.output));
    } catch (e) {
      rows.push({ slug: c.slug, kind: '错误', detail: e.message.split('\n')[0], level: '>10%', rel: 99 });
    }
  }
  await browser.close();
  server.close();
  rows.sort((a, b) => b.rel - a.rel);
  const tiers = ['>10%', '>1%', '四舍五入'];
  let i = 0;
  for (const t of tiers) {
    const list = rows.filter(r => r.level === t);
    if (!list.length) continue;
    console.log(`\n## ${t}（${list.length} 条）`);
    for (const r of list) {
      i++;
      console.log(`${i}. [${r.kind}] ${r.slug} | ${r.detail}`);
    }
  }
  if (!rows.length) console.log('未发现偏差。');
  process.exitCode = rows.some(r => r.level === '>1%' || r.level === '>10%') ? 1 : 0;
})();
