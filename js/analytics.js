// ToolBox 统一统计入口：百度统计、51.la、Microsoft Clarity。
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
      runSafely(function () {
        if (typeof window.clarity !== 'function') return;
        if (customParams && typeof customParams === 'object') {
          Object.keys(customParams).forEach(function (key) {
            if (key === 'category' || key === 'label') return;
            window.clarity('set', key, String(customParams[key]).slice(0, 64));
          });
        }
        window.clarity('event', eventIdentification);
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

  // Microsoft Clarity
  runSafely(function () {
    window.__tbClarityLoaded = true;
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    loadScript('tb-clarity-sdk', 'https://www.clarity.ms/tag/y48102uvzx?ref=bwt');
  });

  // 百度统计与自动推送
  runSafely(function () {
    window._hmt = window._hmt || [];
    loadScript('tb-baidu-statistics', 'https://hm.baidu.com/hm.js?f2993fe19b2862986dd8dbfa0ffcebb8');
    loadScript('tb-baidu-push', 'https://zz.bdstatic.com/linksubmit/push.js');
  });
})(window, document);
