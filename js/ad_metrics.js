// 广告点击埋点（Microsoft Clarity 自定义事件）
// 完整版：上报广告点击事件 + 位置维度(ad_pos) + 所在页维度(ad_page)
// 仅监听广告位点击，不干扰普通点击；clarity() 未就绪时自动排队，安全。
(function () {
  'use strict';

  // 广告位选择器：首页 .ad-banner 容器 / 其内部可点卡片 / 工具页 .tool-ad-banner（前向兼容）
  var AD_SELECTOR = '.ad-banner, .ad-banner-card, .tool-ad-banner';

  function resolvePos(el) {
    // 优先用广告位自身的 data-ad-pos；否则沿容器向上找
    var node = el;
    while (node && node !== document.body) {
      if (node.dataset && node.dataset.adPos) return node.dataset.adPos;
      node = node.parentElement;
    }
    return 'unknown';
  }

  function resolvePage() {
    var m = location.pathname.match(/tools\/([^\/]+)\//);
    if (m && m[1]) return m[1];
    if (location.pathname.indexOf('/guides/') === 0) return 'guide';
    if (location.pathname === '/' || location.pathname === '/index.html') return 'home';
    return 'other';
  }

  document.addEventListener('click', function (e) {
    var ad = e.target.closest ? e.target.closest(AD_SELECTOR) : null;
    if (!ad) return;
    var pos = resolvePos(ad);
    var page = resolvePage();
    if (typeof window.clarity === 'function') {
      // set 写入自定义维度，event 触发自定义事件
      window.clarity('set', 'ad_pos', pos);
      window.clarity('set', 'ad_page', page);
      window.clarity('event', 'ad_click');
    }
  }, true);
})();
