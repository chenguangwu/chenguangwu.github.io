// 第 981 批复核失败重做证据：功率因数补偿页「合法 → 无效目标」真实浏览器历史链路。
// 旧 verify_electrical_calc.js 用自建 TBKit/DOM 桩，不能证明真实浏览器里事件与历史导出的行为；
// 本脚本用 puppeteer-core + 本机 Chrome + 本地 HTTP server 加载真实页面，注入真实 TBKit（js/common.js 由页面引入），
// 依次验证：合法计算进入历史 → 等待（确认无节流丢尾）→ 无效目标被拦截且不写历史/不进导出 → 恢复合法可继续记录。
//
// 用法：env -u NODE_OPTIONS node scripts/_verify_power_factor_history_browser_981.mjs
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REL = 'tools/electrical/power-factor-compensation.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pass = 0, fail = 0;
const ok = (n, c, e) => { if (c) { pass++; console.log('  ✅ ' + n); } else { fail++; console.log('  ❌ ' + n + (e ? '  → ' + e : '')); } };
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = path.join(ROOT, p);
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    const ctx = await browser.createBrowserContext();
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    await page.goto('http://127.0.0.1:' + port + '/' + REL, { waitUntil: 'networkidle0' });

    const setVals = (power, pf1, pf2) => page.evaluate((p, a, b) => {
      const s = (id, v) => { const el = document.getElementById(id); if (el) { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); } };
      s('power', p); s('pf1', a); s('pf2', b);
    }, String(power), String(pf1), String(pf2));
    const histLen = () => page.evaluate(() => { try { return TBKit.history.list().length; } catch (e) { return -1; } });
    const histDump = () => page.evaluate(() => { try { return JSON.stringify(TBKit.history.list()); } catch (e) { return ''; } });
    const resultText = () => page.evaluate(() => String((document.getElementById('result') || {}).textContent || ''));

    // 清空历史起点，避免上次运行残留
    await page.evaluate(() => { try { TBKit.history.clear(); } catch (e) {} });

    // ① 合法计算进入历史
    await setVals(200, 0.75, 0.95);
    await sleep(200);
    const len1 = await histLen();
    ok('合法计算写入一条历史', len1 >= 1, 'len=' + len1);

    // ② 等待超过旧节流窗口（1s），确认合法态已稳定记录
    await sleep(1200);
    const len2 = await histLen();
    ok('等待后历史长度不回退（无节流丢尾）', len2 >= len1, 'len1=' + len1 + ' len2=' + len2);

    // ③ 无效目标（pf2=0，超出 0~1）被拦截，不写历史、不留无效结论
    await setVals(200, 0.75, 0);
    await sleep(200);
    const len3 = await histLen();
    const txt3 = await resultText();
    const dump3 = await histDump();
    ok('无效目标不新增历史', len3 === len2, 'len2=' + len2 + ' len3=' + len3);
    ok('无效目标显示拦截提示', /请输入有效参数|目标功率因数/.test(txt3), txt3);
    ok('历史导出串不含无效目标 0 对应条目', dump3.indexOf('"pf2":"0"') < 0 && dump3.indexOf('"pf2":0') < 0, dump3.slice(0, 200));

    // ④ 恢复合法计算（不同值），验证仍可记录，且历史里是新的合法值
    await setVals(150, 0.80, 0.98);
    await sleep(200);
    const len4 = await histLen();
    const dump4 = await histDump();
    ok('恢复合法后可继续记录', len4 > len3, 'len3=' + len3 + ' len4=' + len4);
    ok('新历史条目为合法值 pf2=0.98', dump4.indexOf('0.98') >= 0, dump4.slice(0, 200));
    ok('无脚本异常', errs.length === 0, errs.join(' | '));

    await ctx.close();
  } finally {
    await browser.close();
    server.close();
  }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})();
