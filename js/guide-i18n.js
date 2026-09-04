/*
 * guide-i18n.js — 指南页国际运行时
 * 依赖：js/i18n.js（defer 先加载，提供 window.I18n + toolbox:langchange 广播）
 * 字典来源：js/guide-en-pack.js（由 scripts/gen_*_guides.py 自动导出，含全批次合并英文）
 *
 * 机制：指南页正文为自由长文本，采用 data-i18n 显式标注 + 集中字典（非通用短语映射）。
 *  - 中文态：元素 textContent 还原为 data-i18n-fb（原文），保证零污染。
 *  - 英文态：从 GUIDE_EN_PACK 字典按 data-i18n="guide.<slug>.<field>[.i]" 取英文替换。
 */
(function () {
  'use strict';

  // 指南页不一定加载 common.js，仍统一复用同一统计加载器。
  if (!document.querySelector('script[src="/js/analytics.js"], script[src$="/js/analytics.js"]')) {
    var analytics = document.createElement('script');
    analytics.src = '/js/analytics.js';
    analytics.async = true;
    document.head.appendChild(analytics);
  }

  if (!window.I18n) return;
  var I18n = window.I18n;

  var GUIDE_EN = {};
  if (window.GUIDE_EN_PACK) {
    for (var k in window.GUIDE_EN_PACK) {
      if (Object.prototype.hasOwnProperty.call(window.GUIDE_EN_PACK, k)) GUIDE_EN[k] = window.GUIDE_EN_PACK[k];
    }
  }
  I18n.addPack('en-US', GUIDE_EN);

  function apply() {
    var lang = I18n.get();
    var isZh = (lang !== 'en-US');
    var nodes = document.querySelectorAll('[data-i18n^="guide."]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var key = el.getAttribute('data-i18n');
      var fb = el.getAttribute('data-i18n-fb');
      if (isZh) {
        if (fb != null) el.textContent = fb;
      } else {
        var en = I18n.t(key, null);
        if (en != null && en !== key) el.textContent = en;
        else if (fb != null) el.textContent = fb;
      }
    }
    // head 元信息随语言切换
    var headNodes = document.querySelectorAll('[data-i18n-head]');
    for (var j = 0; j < headNodes.length; j++) {
      var h = headNodes[j];
      var hkey = h.getAttribute('data-i18n-head');
      var hfb = h.getAttribute('data-i18n-head-fb');
      var attr = h.getAttribute('data-attr') || 'content';
      var val = isZh ? hfb : (I18n.t(hkey, null) || hfb);
      if (val != null) h.setAttribute(attr, val);
    }
  }

  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', apply);
    } else {
      apply();
    }
    window.addEventListener('toolbox:langchange', apply);
  }
  init();
})();
