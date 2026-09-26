// 广告点击埋点：统一交给 ToolBox.Analytics，同时上报百度统计 / 51.la / Clarity。
//
// 本文件是**全站广告点击的唯一入口**，用 document 委托一次覆盖六个广告位：
//   ① 首页热门下方轮播   ② 首页最下方并排   ③ 工具页顶部轮播
//   ④ 工具页底部并排     ⑤ about 页底部并排 ⑥ 页脚文字链
// ⇒ 页面与各注入函数里**不要**再各写一份 click 绑定，否则同一次点击会上报两次
//   （委托是 capture 阶段、页面绑定通常是冒泡阶段，两者都会触发）。
//
// 位置取最近的 [data-ad-pos]；轮播第几帧取最近的 [data-ad-slot]（1 起）。
(function () {
  'use strict';

  var AD_SELECTOR = '.ad-banner, .ad-banner-card, .tool-ad-banner, .footer-friend-link';

  // 从点击目标向上找最近的 data-* 属性值（含自身）
  function closestData(el, key) {
    var node = el;
    while (node && node !== document.body) {
      if (node.dataset && node.dataset[key]) return node.dataset[key];
      node = node.parentElement;
    }
    return '';
  }

  function resolvePos(el) {
    return closestData(el, 'adPos') || 'unknown';
  }

  function resolvePage() {
    var m = location.pathname.match(/tools\/([^\/]+)\//);
    if (m && m[1]) return m[1];
    if (location.pathname.indexOf('/guides/') === 0) return 'guide';
    if (location.pathname === '/' || location.pathname === '/index.html') return 'home';
    return 'other';
  }

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var ad = t.closest(AD_SELECTOR);
    if (!ad) return;
    var params = {
      // 位置与帧号都要从**点击目标**向上找：ad 可能落在更外层容器上，
      // 从它往上找会越过夹在中间的 [data-ad-slot]
      // （工具页卡片类名是 .tool-ad-card、不在选择器里，closest 必然直接跳到 .tool-ad-banner）
      ad_pos: resolvePos(t) || resolvePos(ad) || 'unknown',
      ad_page: resolvePage()
    };
    // 轮播位才有帧号；非轮播位保持原有字段不变，避免污染历史口径
    var slot = closestData(t, 'adSlot');
    if (slot) params.ad_slot = Number(slot) || slot;
    try {
      if (window.ToolBox && ToolBox.Analytics) ToolBox.Analytics.track('ad_tb', params);
    } catch (err) {}
  }, true);
})();
