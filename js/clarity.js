// 兼容旧页面引用：实际统计平台统一由 analytics.js 管理。
(function (window, document) {
  if (document.querySelector('script[src="/js/analytics.js"], script[src$="/js/analytics.js"]')) return;
  var script = document.createElement('script');
  script.src = '/js/analytics.js';
  script.async = true;
  document.head.appendChild(script);
})(window, document);
