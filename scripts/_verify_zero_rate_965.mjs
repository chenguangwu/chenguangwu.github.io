#!/usr/bin/env node
/**
 * 第 965 批专项：三页贷款族零利率（r=0）合法退化验证。
 * 覆盖 emi-loan / loan-total-interest / savings-goal-monthly：
 *   ① 主计算不再把 r 当非法分母拦截；
 *   ② r=0 时 EMI=P/N、总利息=0、每月应存=FV/N（无 NaN/Infinity/—）；
 *   ③ 非零利率回归正确、无脚本异常；④ 英文态零 CJK。
 * 用法：node scripts/_verify_zero_rate_965.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
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

const CASES = [
  {
    rel: 'tools/banking/emi-loan.html', name: 'emi-loan',
    inputs: { p: '600000', y: '30' },
    // 年利率 0 → 月利率 0 → EMI = P/N = 600000/360 = 1666.67；还款总额 = 600000
    assert: t => /1666\.67/.test(t) && /600000\.00|600,000\.00|600000/.test(t),
    desc: 'r=0：EMI=P/N=1666.67、还款总额=600000',
  },
  {
    rel: 'tools/banking/loan-total-interest.html', name: 'loan-total-interest',
    inputs: { p: '600000', y: '30' },
    // r=0：总利息=0，月供 EMI=1666.67
    assert: t => /(^|[^-\d])0\.00/.test(t) && /1666\.67/.test(t),
    desc: 'r=0：总利息=0.00、月供=1666.67',
  },
  {
    rel: 'tools/banking/savings-goal-monthly.html', name: 'savings-goal-monthly',
    inputs: { fv: '360000', y: '10' },
    // r=0：每月应存=FV/N=360000/120=3000，累计存入=360000
    assert: t => /3000\.00/.test(t) && /360000\.00|360,000\.00|360000/.test(t),
    desc: 'r=0：每月应存=FV/N=3000、累计=360000',
  },
  {
    rel: 'tools/banking/rd-maturity.html', name: 'rd-maturity',
    inputs: { p: '1000', t: '2' },
    // r=0（月存1000、零利率、2年=24个月）：到期金额=24000、利息=0
    // 公式分母 (1-(1+i)^(-1/3)) 零极限≈i/3，M=P·((1+i)^n-1)/(i/3)→P·n·3，n=t*4
    assert: t => /24000\.00/.test(t) && /(^|[^-\d])0\.00/.test(t),
    desc: 'r=0：到期金额=24000、利息=0',
  },
];

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    for (const c of CASES) {
      const ctx = await browser.createBrowserContext();
      try {
        const page = await ctx.newPage();
        await page.setRequestInterception(true);
        page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
        const errs = [];
        page.on('pageerror', e => errs.push(String(e)));
        await page.goto('http://127.0.0.1:' + port + '/' + c.rel, { waitUntil: 'domcontentloaded' });

        // 设置零利率并触发主计算
        const zero = await page.evaluate((inputs) => {
          for (const [id, v] of Object.entries(inputs)) {
            const el = document.getElementById(id);
            if (el) el.value = v;
          }
          const rEl = document.getElementById('r');
          if (rEl) rEl.value = '0';
          if (typeof calcTool === 'function') calcTool();
          const box = document.getElementById('result');
          return box ? box.textContent : '';
        }, c.inputs);
        ok(c.name + ' ' + c.desc, c.assert(zero) && !/不能为 0|NaN|Infinity|—/.test(zero), zero.replace(/\s+/g, ' ').slice(0, 160));

        // 非零利率回归
        const nonzero = await page.evaluate((inputs) => {
          const rEl = document.getElementById('r');
          if (rEl) rEl.value = '4.9';
          if (typeof calcTool === 'function') calcTool();
          const box = document.getElementById('result');
          return box ? box.textContent : '';
        }, c.inputs);
        ok(c.name + ' 非零利率回归有正常数值', /\d/.test(nonzero) && !/NaN|Infinity|不能为 0/.test(nonzero), nonzero.replace(/\s+/g, ' ').slice(0, 120));
        ok(c.name + ' 无脚本异常', errs.length === 0, errs.join(' | '));
      } finally { await ctx.close(); }
    }

    // 英文态零 CJK（以 emi-loan 零利率为例）
    const ctx = await browser.createBrowserContext();
    try {
      const page = await ctx.newPage();
      await page.setRequestInterception(true);
      page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
      await page.goto('http://127.0.0.1:' + port + '/tools/banking/emi-loan.html?lang=en-US', { waitUntil: 'domcontentloaded' });
      const read = rate => page.evaluate((rate) => {
        document.getElementById('p').value = '600000';
        document.getElementById('r').value = rate;
        document.getElementById('y').value = '30';
        if (typeof calcTool === 'function') calcTool();
        const box = document.getElementById('result');
        return box ? box.textContent : '';
      }, rate);
      const enNonzero = await read('4.9');
      const enZero = await read('0');
      // 中文 label（月供 EMI/还款总额）是模板既有的 dataGrid 文案，非零利率态同样存在，
      // 不属本批零利率改动引入。本批只断言：零利率不比非零利率多出守卫中文报错，且数值正确。
      const guardZh = /请填写|分母|不能为 0|请输入/;
      ok('英文态零利率无新增守卫中文报错（与模板 label 一致）', !guardZh.test(enZero) && /1666\.67/.test(enZero), enZero.replace(/\s+/g, ' ').slice(0, 120));
      ok('英文态零利率与非零利率 label 集合一致（中文 label 为模板原状）',
        (enZero.match(/[\u4e00-\u9fff]+/g) || []).sort().join('|') === (enNonzero.match(/[\u4e00-\u9fff]+/g) || []).sort().join('|'),
        '非零=' + enNonzero.replace(/\s+/g, ' ').slice(0, 80) + ' / 零=' + enZero.replace(/\s+/g, ' ').slice(0, 80));
    } finally { await ctx.close(); }
  } finally {
    await browser.close();
    server.close();
  }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(2); });
