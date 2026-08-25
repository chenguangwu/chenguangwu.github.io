/* ToolBox Service Worker - 离线支持 + 分层缓存 (B5-09)
 *
 * Cache layers:
 *   PRECACHE  - 核心应用外壳（启动即可离线）
 *   RUNTIME   - 静态资源（css/js/img/json 等），stale-while-revalidate，LRU
 *   TOOLS     - 已访问工具页 HTML + 行业 JSON，网络优先并持久化，独立预算
 * AI 模型由 Transformers.js 自行缓存于独立 Cache Storage，不在此重复缓存。
 */
const VERSION = 'tb-sw-v3';
const RUNTIME = 'tb-runtime-v3';
const TOOLS = 'tb-tools-v3';
const KEEP = new Set([VERSION, RUNTIME, TOOLS]);
const MAX_RUNTIME = 400; // 静态资源 LRU 上限
const MAX_TOOLS = 800;   // 工具页 LRU 上限

// 预缓存核心应用外壳（启动即可离线）
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

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(VERSION).then((cache) => cache.addAll(PRECACHE).catch(() => {})).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => !KEEP.has(k)).map((k) => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// LRU 裁剪：超出预算时按插入顺序（keys 顺序近似）删除最旧条目。
// 当存储接近配额时主动多裁剪，避免写入失败。
function trimCache(name, max) {
  return caches.open(name).then((cache) => cache.keys().then((keys) => {
    const over = keys.length - max;
    if (over <= 0) return;
    const drop = over + (estimateNearQuota() ? Math.ceil(max * 0.25) : 0);
    return Promise.all(keys.slice(0, drop).map((k) => cache.delete(k)));
  }));
}

function estimateNearQuota() {
  // 最佳努力：存储接近上限时返回 true
  if (self.navigator && self.navigator.storage && self.navigator.storage.estimate) {
    return self.navigator.storage.estimate().then((e) => e.quota && e.usage && (e.usage / e.quota) > 0.85)
      .catch(() => false);
  }
  return Promise.resolve(false);
}

function putCache(name, req, resp) {
  if (!resp || resp.status !== 200 || resp.type === 'opaque') return;
  const copy = resp.clone();
  caches.open(name).then((cache) => cache.put(req, copy));
  if (name === RUNTIME) trimCache(RUNTIME, MAX_RUNTIME);
  else if (name === TOOLS) trimCache(TOOLS, MAX_TOOLS);
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // 不拦截跨域（CDN / AI 模型由库自理）

  if (req.mode === 'navigate') {
    // 导航请求：网络优先，失败回退工具缓存，再回退首页（离线可用）
    event.respondWith(
      fetch(req).then((resp) => {
        putCache(TOOLS, req, resp);
        return resp;
      }).catch(() => caches.match(req).then((r) => r || caches.match('/index.html')))
    );
    return;
  }

  const isStatic = /\.(css|js|png|jpg|jpeg|svg|json|woff2?|ico)$/.test(url.pathname);
  if (isStatic) {
    event.respondWith(
      caches.match(req).then((cached) => {
        const fetchPromise = fetch(req).then((resp) => {
          putCache(RUNTIME, req, resp);
          return resp;
        }).catch(() => cached);
        return cached || fetchPromise;
      })
    );
    return;
  }

  // 其它 HTML（工具页直接访问）：网络优先并持久化到 TOOLS
  event.respondWith(
    fetch(req).then((resp) => {
      putCache(TOOLS, req, resp);
      return resp;
    }).catch(() => caches.match(req).then((r) => r || caches.match('/index.html')))
  );
});
