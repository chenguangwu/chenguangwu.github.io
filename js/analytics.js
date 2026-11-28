// ToolBox 统一统计入口：百度统计、51.la（网站统计 + 应用监控）、Microsoft Clarity。
// 新增或调整统计平台时，只修改本文件，页面无需逐页改动。
(function (window, document) {
  'use strict';

  if (window.__tbAnalyticsBootstrapped) return;
  window.__tbAnalyticsBootstrapped = true;

  function loadScript(id, src, onload) {
    try {
      if (document.getElementById(id)) return;
      var script = document.createElement('script');
      script.id = id;
      script.async = true;
      script.src = src;
      if (onload) script.onload = function () {
        try { onload(); } catch (e) {}
      };
      (document.head || document.documentElement).appendChild(script);
    } catch (e) {}
  }

  function runSafely(fn) {
    try { fn(); } catch (e) {}
  }

  // 统一事件上报。各平台单独隔离，任一 SDK 异常都不能影响业务代码。
  var pendingLaTracks = [];
  function trackLa(args) {
    if (window.LA && typeof window.LA.track === 'function') {
      window.LA.track.apply(window.LA, args);
    } else if (pendingLaTracks.length < 50) {
      pendingLaTracks.push(args);
    }
  }
  function flushLaTracks() {
    var pending = pendingLaTracks.splice(0);
    pending.forEach(function (args) { runSafely(function () { trackLa(args); }); });
  }

  var analytics = {
    track: function (eventIdentification, customParams, ids) {
      runSafely(function () {
        if (customParams && typeof customParams === 'object' && Object.keys(customParams).length) {
          if (ids !== undefined) trackLa([eventIdentification, customParams, ids]);
          else trackLa([eventIdentification, customParams]);
        } else if (ids !== undefined) {
          trackLa([eventIdentification, ids]);
        } else {
          trackLa([eventIdentification]);
        }
      });
      runSafely(function () {
        if (!window._hmt || typeof window._hmt.push !== 'function') return;
        var category = customParams && customParams.category || eventIdentification;
        var label = customParams && customParams.label || '';
        window._hmt.push(['_trackEvent', eventIdentification, category, label]);
      });
    }
  };
  window.ToolBox = window.ToolBox || {};
  window.ToolBox.Analytics = analytics;

  // 51.la
  runSafely(function () {
    loadScript('LA_COLLECT', 'https://sdk.51.la/js-sdk-pro.min.js', function () {
      if (window.LA && typeof window.LA.init === 'function') {
        window.LA.init({
          id: '3R0rVW6KKmLfdAFz',
          ck: '3R0rVW6KKmLfdAFz',
          autoTrack: true
        });
        flushLaTracks();
      }
    });
  });

  // 51.la 应用监控（性能监控）：与网站统计共用统一入口，使用监控专用 ID。
  // 官方提供两种安装：静态 <script src="...perf..." crossorigin="anonymous"> + init，
  // 或异步 IIFE 插入后在 onload 里 init。本站取异步等价方案（统一 loadScript 动态插入），
  // 覆盖全站页面，并保留静态写法的 sendSuspicious:true 参数。
  // 不设 crossOrigin 属主动选择：perf 端点实测返回 access-control-allow-origin:*
  //（与无 CORS 头的 v6-widget 挂件端点不同），loadScript 统一不设该属性，与其他统计脚本一致。
  runSafely(function () {
    loadScript('LA_PERF_MONITOR', 'https://sdk.51.la/perf/js-sdk-perf.min.js', function () {
      if (window.LingQue && typeof window.LingQue.Monitor === 'function') {
        new window.LingQue.Monitor().init({ id: '3RsOdL1MNE7j4CCN', sendSuspicious: true });
      }
    });
  });

  // Microsoft Clarity：初始化前设置全页遮罩；其他采集通道仍须核验。
  runSafely(function () {
    document.documentElement.setAttribute('data-clarity-mask', 'true');
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    loadScript('tb-clarity-sdk', 'https://www.clarity.ms/tag/y48102uvzx?ref=bwt');
  });

  // 百度统计与自动推送
  runSafely(function () {
    window._hmt = window._hmt || [];
    loadScript('tb-baidu-statistics', 'https://hm.baidu.com/hm.js?f2993fe19b2862986dd8dbfa0ffcebb8');
  });
})(window, document);
