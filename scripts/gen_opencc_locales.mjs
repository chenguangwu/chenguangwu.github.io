#!/usr/bin/env node
/**
 * Generate SEO-crawlable Traditional Chinese pages from the zh-CN source.
 *
 * Source pages remain canonical. zh-tw/ is the generated artifact:
 * HTML and JSON are localized, while shared CSS/JS/images stay at the root.
 * Run through _build.py or `npm run build:i18n`; never edit locale output.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { availableParallelism } from 'node:os';
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import { fileURLToPath } from 'node:url';
import OpenCC from 'opencc-js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SITE = 'https://chenguangwu.github.io';
const MARKER = '.toolbox-opencc-locale';
const ROOT_PAGES = ['index.html', 'search.html', 'chains.html', 'about.html', 'sitemap.html', 'embed.html', '404.html'];
const LOCALES = [
  { code: 'zh-TW', dir: 'zh-tw', to: 'twp', og: 'zh_TW' }
];
const PUBLIC_PREFIXES = ['tools/', 'guides/'];
const SKIP_TAGS = new Set(['script', 'style', 'pre', 'code', 'textarea', 'template']);
const TRANSLATABLE_ATTRS = new Set(['title', 'placeholder', 'aria-label', 'alt', 'data-i18n-fb', 'data-i18n-ph-fb', 'data-i18n-title-fb', 'data-zh']);
const DEFAULT_WORKERS = Math.min(4, Math.max(1, availableParallelism()));

function normalizeRel(rel) {
  return rel.split(path.sep).join('/').replace(/^\.\//, '');
}

async function exists(file) {
  try { await fs.access(file); return true; } catch { return false; }
}

async function walk(dir, extension) {
  const out = [];
  async function visit(current) {
    const entries = await fs.readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) await visit(full);
      else if (entry.isFile() && entry.name.endsWith(extension)) out.push(full);
    }
  }
  if (await exists(dir)) await visit(dir);
  return out.sort();
}

async function sourcePages() {
  const pages = [];
  for (const name of ROOT_PAGES) {
    const full = path.join(ROOT, name);
    if (await exists(full)) pages.push(full);
  }
  for (const prefix of PUBLIC_PREFIXES) {
    const found = await walk(path.join(ROOT, prefix), '.html');
    pages.push(...found.filter((file) => !file.endsWith('.en.html')));
  }
  return pages;
}

function isPublicHtml(rel) {
  return ROOT_PAGES.includes(rel) || PUBLIC_PREFIXES.some((prefix) => rel.startsWith(prefix));
}

function urlPath(rel) {
  return rel === 'index.html' ? '/' : `/${rel}`;
}

function localeUrl(locale, rel) {
  return rel === 'index.html' ? `${SITE}/${locale.dir}/` : `${SITE}/${locale.dir}/${rel}`;
}

function originalUrl(rel) {
  return `${SITE}${urlPath(rel)}`;
}

function splitUrl(raw) {
  const match = raw.match(/^([^?#]*)([?#][\s\S]*)?$/);
  return { base: match ? match[1] : raw, suffix: match?.[2] || '' };
}

function isExternal(raw) {
  return !raw || raw.startsWith('#') || /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(raw);
}

function resolveTarget(fromRel, raw) {
  const { base, suffix } = splitUrl(raw);
  if (isExternal(base)) return null;
  const clean = base.startsWith('/') ? base.slice(1) : path.posix.normalize(path.posix.join(path.posix.dirname(fromRel), base));
  if (clean.startsWith('../')) return null;
  return { rel: clean, suffix };
}

function rewriteAssetUrl(fromRel, raw, locale) {
  const target = resolveTarget(fromRel, raw);
  if (!target) return raw;
  // Existing standalone English guide pages remain their own canonical files;
  // they are not OpenCC source pages and therefore are not generated below
  // each Traditional locale.
  if (target.rel.endsWith('.en.html')) return `/${target.rel}${target.suffix}`;
  if (isPublicHtml(target.rel)) return `/${locale.dir}/${target.rel}${target.suffix}`;
  if (target.rel.startsWith('json/')) return `/${locale.dir}/${target.rel}${target.suffix}`;
  return `/${target.rel}${target.suffix}`;
}

function rewriteHostedUrl(raw, fromRel, locale) {
  if (!raw || !raw.startsWith(SITE)) return raw;
  const suffix = raw.slice(SITE.length);
  const { base, suffix: query } = splitUrl(suffix);
  const rel = base.replace(/^\//, '') || 'index.html';
  if (isPublicHtml(rel)) return `${localeUrl(locale, rel)}${query}`;
  return raw;
}

function convertJson(value, converter) {
  if (typeof value === 'string') return converter(value);
  if (Array.isArray(value)) return value.map((item) => convertJson(item, converter));
  if (value && typeof value === 'object') {
    const out = {};
    for (const [key, item] of Object.entries(value)) out[key] = convertJson(item, converter);
    return out;
  }
  return value;
}

function setJsonLdLocale(value, locale) {
  if (Array.isArray(value)) return value.map((item) => (item === 'zh-CN' || item === 'zh_CN') ? locale.code : setJsonLdLocale(item, locale));
  if (value && typeof value === 'object') {
    for (const [key, item] of Object.entries(value)) {
      value[key] = key === 'inLanguage' ? locale.code : setJsonLdLocale(item, locale);
    }
  }
  return value;
}

function rewriteJsonLdUrls(value, fromRel, locale) {
  if (typeof value === 'string') return rewriteHostedUrl(value, fromRel, locale);
  if (Array.isArray(value)) return value.map((item) => rewriteJsonLdUrls(item, fromRel, locale));
  if (value && typeof value === 'object') {
    for (const [key, item] of Object.entries(value)) value[key] = rewriteJsonLdUrls(item, fromRel, locale);
  }
  return value;
}

async function copyLocalizedJson(locale, converter) {
  const files = await walk(path.join(ROOT, 'json'), '.json');
  for (const file of files) {
    const rel = normalizeRel(path.relative(ROOT, file));
    const destination = path.join(ROOT, locale.dir, rel);
    await fs.mkdir(path.dirname(destination), { recursive: true });
    const raw = await fs.readFile(file, 'utf8');
    const payload = JSON.parse(raw);
    await fs.writeFile(destination, `${JSON.stringify(convertJson(payload, converter))}\n`, 'utf8');
  }
}

async function writeRegionalPack(locale, converter) {
  // Dynamic chrome is shared JS, so it is not part of the converted HTML. Keep
  // this compact pack for its stable i18n keys; page-specific content uses its
  // already converted static text and data-i18n fallback attributes.
  const base = {
    'brand.sub': '工具百科',
    'bc.home': '首页',
    'nav.back': '← ToolBox',
    'tool.related': '🔗 相关工具',
    'tool.notes': '⚠️ 使用说明与注意事项',
    'tool.guide_link': '📖 使用指南',
    'common.loading': '加载中…',
    'footer.desc': '5000+ 跨行业纯前端工具，数据不离开你的浏览器。',
    'footer.privacy': '纯前端 · 数据不离开浏览器',
    'search.placeholder': '搜索工具、分类或功能...',
    'state.load_fail': '加载失败，请刷新后重试'
  };
  const out = {};
  for (const [key, value] of Object.entries(base)) out[key] = converter(value);
  await fs.writeFile(path.join(ROOT, 'i18n', `locale-${locale.code}.json`),
    `${JSON.stringify(out, null, 2)}\n`, 'utf8');
}

async function readHtmlHead(file) {
  // Locale metadata is injected before </head>. Reading the whole multi-MB
  // tool body during --check added avoidable I/O on CI and sandbox disks.
  const handle = await fs.open(file, 'r');
  try {
    const buffer = Buffer.allocUnsafe(128 * 1024);
    const { bytesRead } = await handle.read(buffer, 0, buffer.length, 0);
    return buffer.toString('utf8', 0, bytesRead);
  } finally {
    await handle.close();
  }
}

function localeHead(rel, locale) {
  const cn = originalUrl(rel);
  const en = `${cn}${cn.includes('?') ? '&' : '?'}lang=en-US`;
  const links = [
    '<!-- TOOLBOX-HREFLANG -->',
    `<link rel="alternate" hreflang="zh-CN" href="${cn}">`,
    ...LOCALES.map((item) => `<link rel="alternate" hreflang="${item.code}" href="${localeUrl(item, rel)}">`),
    `<link rel="alternate" hreflang="en-US" href="${en}">`,
    `<link rel="alternate" hreflang="x-default" href="${cn}">`,
    `<meta property="og:locale" content="${locale.og}">`,
    '<meta property="og:locale:alternate" content="zh_CN">',
    '<meta property="og:locale:alternate" content="en_US">'
  ];
  return links.join('\n') + '\n';
}

function rewriteSeo(html, rel, locale) {
  const canonical = localeUrl(locale, rel);
  // 旧实现会从 hreflang 标记一直删到 </head>。构建脚本后来会在该标记
  // 之后注入导航资源（nav-menu.css / industry-info.js / nav-menu.js），因此
  // 不能把标记之后的整段 head 一起移除；只清理旧的语言标签，其他资源原样保留。
  html = html.replace(/<!-- TOOLBOX-HREFLANG -->\s*/gi, '');
  html = html.replace(/\s*<link\b[^>]*\bhreflang=[^>]*>\s*/gi, '\n');
  html = html.replace(/\s*<meta\b[^>]*\bproperty=["']og:locale(?::alternate)?["'][^>]*>\s*/gi, '\n');
  html = html.replace(/(<link\b[^>]*\brel=["']canonical["'][^>]*\bhref=["'])[^"']*(["'])/i, `$1${canonical}$2`);
  html = html.replace(/(<meta\b[^>]*\bproperty=["']og:url["'][^>]*\bcontent=["'])[^"']*(["'])/i, `$1${canonical}$2`);
  return html.replace(/<\/head>/i, `${localeHead(rel, locale)}</head>`);
}

function transformHtml(raw, rel, locale, converter) {
  let html = raw.replace(/<html\b([^>]*)>/i, (all, attrs) => {
    const cleaned = attrs.replace(/\s(?:lang|data-opencc-locale)=["'][^"']*["']/gi, '');
    return `<html${cleaned} lang="${locale.code}" data-opencc-locale="${locale.dir}">`;
  });
  // script/style/noscript contents are protected from language conversion, but
  // their opening tags still need root-safe asset URLs in a nested locale path.
  html = html.replace(/<(?!\/)([a-z][\w:-]*)([^>]*)>/gi, (all, tag, attrs) => {
    const rewritten = attrs.replace(/\s(href|src|action)=(["'])([\s\S]*?)\2/gi,
      (match, name, quote, value) => ` ${name}=${quote}${rewriteAssetUrl(rel, value, locale)}${quote}`);
    return `<${tag}${rewritten}>`;
  });
  let depth = 0;
  // Split only on a real tag (a letter must immediately follow '<'). This
  // deliberately leaves prose such as "<120 mmHg" as text rather than
  // consuming it through the next real tag.
  html = html.split(/(<\/?[a-zA-Z][^>]*>)/g).map((token) => {
    if (!token) return token;
    if (!token.startsWith('<')) return depth ? token : converter(token);
    const name = token.match(/^<\/?\s*([a-zA-Z][\w:-]*)/);
    if (!name) return depth ? token : converter(token);
    const close = /^<\//.test(token);
    const tag = name[1].toLowerCase();
    if (close) {
      if (SKIP_TAGS.has(tag)) depth = Math.max(0, depth - 1);
      return token;
    }
    const protectedTag = SKIP_TAGS.has(tag);
    if (protectedTag) {
      depth += 1;
      return token;
    }
    if (depth) return token;
    return token.replace(/\s([\w:-]+)=(["'])([\s\S]*?)\2/g, (match, attr, quote, value) => {
      const lower = attr.toLowerCase();
      if (TRANSLATABLE_ATTRS.has(lower)) return ` ${attr}=${quote}${converter(value)}${quote}`;
      return match;
    });
  }).join('');
  html = html.replace(/<script\b([^>]*type=["']application\/ld\+json["'][^>]*)>([\s\S]*?)<\/script>/gi, (all, attrs, data) => {
    try {
      const parsed = rewriteJsonLdUrls(setJsonLdLocale(convertJson(JSON.parse(data), converter), locale), rel, locale);
      const json = JSON.stringify(parsed);
      return `<script${attrs}>${json}</script>`;
    } catch { return all; }
  });
  // The homepage deliberately pre-renders a few English i18n nodes. Restore
  // only those known, simple nodes from their source fallback. A generic
  // cross-page regex is unsafe because historical guide prose can contain raw
  // '<' comparison symbols.
  const staticFallbackKeys = ['hero.title', 'hero.sub', 'hero.tags', 'hero.chain',
    'foot.tool_json', 'foot.tool_qr', 'foot.tool_pwd', 'foot.tool_color',
    'foot.tool_regex', 'foot.tool_timestamp'];
  html = html.replace(/(<([a-z][\w:-]*)\b[^>]*\bdata-i18n=(["'])([^"']+)\3[^>]*\bdata-i18n-fb=(["'])([^"']*)\5[^>]*>)([^<]*)(<\/\2>)/gi,
    (all, open, tag, keyQuote, key, fallbackQuote, fallback, text, close) =>
      staticFallbackKeys.includes(key) ? `${open}${converter(fallback)}${close}` : all);
  html = rewriteSeo(html, rel, locale);
  return html.replace(/[ \t]+(?=\r?\n)/g, '');
}

async function buildPageChunk(locale, pages) {
  const converter = OpenCC.Converter({ from: 'cn', to: locale.to });
  const destination = path.join(ROOT, locale.dir);
  for (const page of pages) {
    const rel = normalizeRel(path.relative(ROOT, page));
    const out = path.join(destination, rel);
    const raw = await fs.readFile(page, 'utf8');
    await fs.writeFile(out, transformHtml(raw, rel, locale, converter), 'utf8');
  }
}

function runPageWorker(locale, pages) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(new URL(import.meta.url), {
      workerData: { task: 'build-pages', locale, pages }
    });
    worker.once('error', reject);
    worker.once('exit', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`OpenCC worker exited with code ${code}`));
    });
  });
}

async function buildLocale(locale, pages) {
  const destination = path.join(ROOT, locale.dir);
  if (await exists(destination)) {
    if (!await exists(path.join(destination, MARKER))) {
      throw new Error(`Refusing to overwrite ${locale.dir}: missing ${MARKER}`);
    }
    await fs.rm(destination, { recursive: true, force: true });
  }
  await fs.mkdir(destination, { recursive: true });
  const outputDirs = new Set(pages.map((page) =>
    path.dirname(path.join(destination, normalizeRel(path.relative(ROOT, page))))
  ));
  await Promise.all([...outputDirs].map((dir) => fs.mkdir(dir, { recursive: true })));

  const requestedWorkers = Number.parseInt(process.env.TOOLBOX_OPENCC_WORKERS || '', 10);
  const workerCount = Math.min(
    pages.length,
    Number.isFinite(requestedWorkers) && requestedWorkers > 0 ? requestedWorkers : DEFAULT_WORKERS
  );
  if (workerCount === 1) {
    await buildPageChunk(locale, pages);
  } else {
    const chunks = Array.from({ length: workerCount }, () => []);
    pages.forEach((page, index) => chunks[index % workerCount].push(page));
    await Promise.all(chunks.map((chunk) => runPageWorker(locale, chunk)));
  }

  const converter = OpenCC.Converter({ from: 'cn', to: locale.to });
  await copyLocalizedJson(locale, converter);
  await writeRegionalPack(locale, converter);
  await fs.writeFile(path.join(destination, MARKER), `generated from zh-CN by scripts/gen_opencc_locales.mjs\n`, 'utf8');
  console.log(`[opencc] ${locale.dir}: ${pages.length} HTML pages + localized JSON (${workerCount} workers)`);
}

async function check() {
  const pages = await sourcePages();
  let failed = false;
  for (const locale of LOCALES) {
    const root = path.join(ROOT, locale.dir);
    if (!await exists(path.join(root, MARKER))) { console.error(`[opencc] missing ${locale.dir}/${MARKER}`); failed = true; continue; }
    for (const page of pages) {
      const rel = normalizeRel(path.relative(ROOT, page));
      const file = path.join(root, rel);
      if (!await exists(file)) { console.error(`[opencc] missing ${locale.dir}/${rel}`); failed = true; continue; }
      const html = await readHtmlHead(file);
      if (!html.includes(`lang="${locale.code}"`) || !html.includes(`hreflang="${locale.code}"`)) {
        console.error(`[opencc] invalid locale head: ${locale.dir}/${rel}`); failed = true;
      }
    }
  }
  if (failed) process.exitCode = 1;
  else console.log(`[opencc] verified ${pages.length} pages for ${LOCALES.length} locales`);
}

if (!isMainThread) {
  if (workerData?.task !== 'build-pages') throw new Error('Unknown OpenCC worker task');
  await buildPageChunk(workerData.locale, workerData.pages);
  parentPort?.postMessage({ ok: true });
} else {
  const pages = await sourcePages();
  if (process.argv.includes('--check')) await check();
  else for (const locale of LOCALES) await buildLocale(locale, pages);
}
