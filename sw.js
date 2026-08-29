/* ToolBox Service Worker - 分层缓存 + 发布即失效
 *
 * 2026-08-29 重构：修复「站点更新后仍展示旧内容，必须无痕模式才看得到新版本」。
 * 旧实现的静态资源分支是 cache-first（`return cached || fetchPromise`），
 * 一旦 Cache Storage 命中就永远返回旧副本，叠加硬编码缓存名 tb-sw-v3（不随发布变化），
 * 导致 CSS/JS/JSON 被永久钉死在首次安装时的版本。
 *
 * 现行策略：
 *   1. CSS/JS/JSON 走「网络优先」，仅超时/断网时回退缓存 —— 在线访问永远拿到最新版本。
 *   2. 网络请求附加 ?_swv=BUILD 版本戳（BUILD 由 _build.py 按共享资源内容 hash 写入，
 *      内容不变则戳不变，构建幂等），绕过浏览器与 CDN 的 HTTP 缓存。
 *   3. 缓存名带 BUILD：发布后旧缓存由 activate 自动清理，无需人工改版本号。
 *   4. 图片/字体等命名稳定、内容基本不变的资源仍用 cache-first，节省流量。
 *   5. 紧急开关：站点根下放 sw-kill.json = {"disabled": true} 可一键停用本 SW。
 *
 * 缓存分层：
 *   SHELL    - 应用外壳预缓存（离线兜底，仅在断网时命中）
 *   RUNTIME  - 静态资源（css/js/json/img），LRU 裁剪
 *   TOOLS    - 已访问页面 HTML，网络优先并持久化
 * AI 模型由 Transformers.js 自行缓存于独立 Cache Storage，不在此重复缓存。
 */
const BUILD = 'a41ed7fb03';                       // 由 _build.py 注入（内容 hash，勿手改）
const SHELL = 'tb-shell-v4';
const RUNTIME = 'tb-rt-v4-' + BUILD;
const TOOLS = 'tb-tools-v4-' + BUILD;
const KEEP = new Set([SHELL, RUNTIME, TOOLS]);
const MAX_RUNTIME = 400;   // 静态资源 LRU 上限
const MAX_TOOLS = 800;     // 页面 HTML LRU 上限
const NET_TIMEOUT = 3000;  // 网络优先超时（ms），超时回退缓存

// 预缓存核心应用外壳（仅作离线兜底：在线时一律走网络优先，不会被旧副本钉死）
const PRECACHE = [
  '/',
  '/index.html',
  '/404.html',
  '/manifest.json',
  '/css/common.css',
  '/css/style.css',
  '/js/app.js',
  '/js/common.js',
  '/js/chart.js',
  '/js/i18n.js',
  '/js/freemium.js',
  '/js/ai-core.js',
  '/js/qrcode.js',
  '/vendor/fuse.min.js',
  '/chains.html',
  '/search.html',
  '/favicon.svg',
  '/logo-128.png',
  '/logo-192.png',
  '/logo-512.png',
  '/apple-touch-icon.png'
];

let KILLED = false; // 紧急开关命中后停止拦截，全部请求放行到网络

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL).then((cache) => cache.addAll(PRECACHE).catch(() => {})).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    checkKillSwitch()
      .then(() => caches.keys())
      .then((keys) => Promise.all(
        // 清理所有历史版本缓存（含旧版 tb-sw-v3 / tb-runtime-v3 / tb-tools-v3）
        keys.filter((k) => k.indexOf('tb-') === 0 && !KEEP.has(k)).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// 紧急开关：站点根下 sw-kill.json = {"disabled":true} 时清空缓存并注销自身
async function checkKillSwitch() {
  try {
    const resp = await fetch('/sw-kill.json?_swv=' + BUILD, { cache: 'no-store' });
    if (!resp.ok) return;
    const data = await resp.json();
    if (data && data.disabled === true) {
      KILLED = true;
      const keys = await caches.keys();
      await Promise.all(keys.map((k) => caches.delete(k)));
      await self.registration.unregister();
    }
  } catch (e) { /* 无 kill 文件即正常运行 */ }
}

// LRU 裁剪：超出预算时按插入顺序删除最旧条目
function trimCache(name, max) {
  return caches.open(name).then((cache) => cache.keys().then((keys) => {
    const over = keys.length - max;
    if (over <= 0) return;
    return Promise.all(keys.slice(0, over).map((k) => cache.delete(k)));
  }));
}

function putCache(name, req, resp) {
  if (!resp || resp.status !== 200 || resp.type === 'opaque') return;
  const copy = resp.clone();
  caches.open(name).then((cache) => cache.put(req, copy)).then(() => {
    if (name === RUNTIME) return trimCache(RUNTIME, MAX_RUNTIME);
    if (name === TOOLS) return trimCache(TOOLS, MAX_TOOLS);
  }).catch(() => {});
}

// 附加版本戳，绕过浏览器 HTTP 缓存与 CDN 缓存；BUILD 不变则 URL 不变，仍可命中 CDN
function busted(req) {
  try {
    const u = new URL(req.url);
    u.searchParams.set('_swv', BUILD);
    return new Request(u.toString(), {
      method: 'GET', credentials: 'same-origin', redirect: 'follow', cache: 'reload'
    });
  } catch (e) {
    return req;
  }
}

const OFFLINE_FALLBACK = new Response('', { status: 504, statusText: 'SW Offline' });

// 网络优先：成功即写入缓存；超时或断网回退缓存；仍无则回退 fallback
function networkFirst(req, cacheName, fallback) {
  const net = fetch(busted(req)).then((resp) => {
    putCache(cacheName, req, resp);
    return resp;
  });
  const timer = new Promise((_, reject) => setTimeout(() => reject(new Error('sw-timeout')), NET_TIMEOUT));
  return Promise.race([net, timer]).catch(() =>
    caches.match(req).then((cached) => cached || fallback || OFFLINE_FALLBACK)
  );
}

// 缓存优先：用于内容稳定的资源（图片/字体/图标）
function cacheFirst(req) {
  return caches.match(req).then((cached) => {
    if (cached) return cached;
    return fetch(busted(req)).then((resp) => {
      putCache(RUNTIME, req, resp);
      return resp;
    });
  });
}

self.addEventListener('fetch', (event) => {
  if (KILLED) return; // 紧急开关：不拦截，全部走网络
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // 不拦截跨域（CDN / AI 模型由库自理）

  const path = url.pathname;

  if (req.mode === 'navigate') {
    // 导航请求：网络优先，断网回退页面缓存，再回退首页（离线可用）
    event.respondWith(networkFirst(req, TOOLS, caches.match('/index.html')));
    return;
  }

  // 内容稳定的资源：cache-first
  if (/\.(png|jpe?g|gif|webp|avif|ico|svg|woff2?|ttf|eot)$/.test(path)) {
    event.respondWith(cacheFirst(req));
    return;
  }

  // CSS/JS/JSON：网络优先（发布即生效），断网回退缓存
  if (/\.(css|js|mjs|json)$/.test(path)) {
    event.respondWith(networkFirst(req, RUNTIME, null));
    return;
  }

  // 其它（工具页 HTML 直接访问等）：网络优先并持久化到 TOOLS
  event.respondWith(networkFirst(req, TOOLS, caches.match('/index.html')));
});

// 供页面调用：手动清缓存 / 立即接管
self.addEventListener('message', (event) => {
  const data = event.data || {};
  if (data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  } else if (data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys()
        .then((keys) => Promise.all(keys.filter((k) => k.indexOf('tb-') === 0).map((k) => caches.delete(k))))
        .then(() => self.registration.unregister())
    );
  }
});
