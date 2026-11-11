// 第206批 · IT-N259 qrcode SEO 口径一致（只生成、无识别宣称）（真机 + 静态检查）
// 注：源码修复已在 HEAD（其他 Agent 所为），本批只补证据 + 清单销账。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/qrcode.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

const dom = new JSDOM(html, { url: 'https://example.com/tools/it/qrcode.html' });
const d = dom.window.document;

// ── title / h1 / JSON-LD name 三者一致 ──
const title = d.querySelector('title').textContent.trim();
const h1 = d.querySelector('h1').textContent.trim();
check('title 为二维码生成器', /二维码生成器/.test(title) && !/识别|解析/.test(title), title);
check('h1 为二维码生成器', h1 === '二维码生成器', h1);
check('title 与 h1 口径一致', title.indexOf('二维码生成器') >= 0 && h1 === '二维码生成器');

// ── keywords 无识别/解析宣称 ──
const kw = d.querySelector('meta[name=keywords]').content;
check('keywords 无识别/解析宣称', !/识别|解析|扫码解析|decode/i.test(kw), kw);

// ── meta description / og / twitter 无识别宣称 ──
for (const sel of ['meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]']) {
  const el = d.querySelector(sel);
  if (el) check(sel + ' 无识别宣称', !/识别|解析.*上传|上传.*解析/.test(el.content), el.content.slice(0, 60));
}

// ── JSON-LD WebApplication name/description ──
const scripts = [...d.querySelectorAll('script[type="application/ld+json"]')];
let ldOk = true, ldName = '';
for (const s of scripts) {
  try {
    const o = JSON.parse(s.textContent);
    if (o['@type'] === 'WebApplication') {
      ldName = o.name || '';
      if (/识别|解析/.test(ldName) || /识别|上传.*解析/.test(o.description || '')) ldOk = false;
    }
  } catch (e) {}
}
check('JSON-LD name 无识别宣称', ldOk && /二维码/.test(ldName), ldName);

// ── 无文件上传/解码入口（与宣称一致）──
check('无 file input（生成器本无名解码）', d.querySelectorAll('input[type=file]').length === 0);
check('无解码相关控件 id', !/id="[^"]*(decode|upload|scan)[^"]*"/i.test(html));

// ── intro/deep-dive 无"上传图片解析"宣称；"深度解析"栏目名允许 ──
const bodyText = d.body.textContent;
check('无「上传二维码图片解析」宣称', bodyText.indexOf('上传二维码图片解析') < 0);
check('无「生成与解析二维码」宣称', bodyText.indexOf('生成与解析二维码') < 0);
check('保留正确技术描述「扫码定位」', bodyText.indexOf('扫码定位') >= 0);

// ── 源码权威源无残留（build 不重注入）──
const override = fs.readFileSync('i18n/tools/_en_override.json', 'utf8');
check('_en_override 无识别宣称', !/二维码识别|上传二维码图片解析/.test(override));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
