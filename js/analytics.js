// ToolBox 统一统计入口：百度统计、51.la。
// 新增或调整统计平台时，只修改本文件，页面无需逐页改动。
(function (window, document) {
  'use strict';

  if (window.__tbAnalyticsBootstrapped) return;
  window.__tbAnalyticsBootstrapped = true;

  function loadScript(id, src, onload) {
    if (document.getElementById(id)) return;
    var script = document.createElement('script');
    script.id = id;
    script.async = true;
    script.src = src;
    if (onload) script.onload = onload;
    (document.head || document.documentElement).appendChild(script);
  }

  // 百度统计与自动推送
  window._hmt = window._hmt || [];
  loadScript('tb-baidu-statistics', 'https://hm.baidu.com/hm.js?f2993fe19b2862986dd8dbfa0ffcebb8');
  loadScript('tb-baidu-push', 'https://zz.bdstatic.com/linksubmit/push.js');

  // 51.la
  loadScript('LA_COLLECT', 'https://sdk.51.la/js-sdk-pro.min.js', function () {
    if (window.LA && typeof window.LA.init === 'function') {
      window.LA.init({
        id: '3R0rVW6KKmLfdAFz',
        ck: '3R0rVW6KKmLfdAFz',
        autoTrack: true
      });
    }
  });
})(window, document);
