// 广告点击埋点：统一交给 ToolBox.Analytics，同时上报三家统计平台。
(function () {
  'use strict';

  var AD_SELECTOR = '.ad-banner, .ad-banner-card, .tool-ad-banner';

  function resolvePos(el) {
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
    try {
      if (window.ToolBox && ToolBox.Analytics) ToolBox.Analytics.track('ad_tb', {
        ad_pos: pos,
        ad_page: page
      });
    } catch (e) {}
  }, true);
})();
