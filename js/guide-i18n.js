/*
 * guide-i18n.js — 指南页（guides/*.html）内容区英文运行时（文本节点级替换）
 * 依赖：js/i18n.js（全站加载，提供 window.I18n + toolbox:langchange）
 * 由 js/i18n.js 的 init() 在指南页动态注入（仅 /guides/ 且非 .en.html / 非 index.html 生效）。
 *
 * 机制（与工具页 tool-i18n.js 的 applyEnDict 一致）：
 *  - EN 态下用 TreeWalker 遍历 main / .breadcrumb / .faq / .related / .back 的可见文本节点，
 *    按 i18n/guides/_common.json（共享固定文案）+ i18n/guides/<slug>.json（逐页）的精确整串映射替换；
 *  - 保留文本节点首尾空白（raw.slice），杜绝双空格；单向（切回中文不还原，语言切换走 URL 重载）。
 *  - 覆盖指南框架文案：面包屑「首页/使用指南」、相关工具标题、返回链接外壳。
 */
(function () {
  'use strict';
  if (!window.I18n) return;
  var I18n = window.I18n;

  function isEnglish() { return I18n.get() === 'en-US'; }

  function guideSlug() {
    var p = location.pathname.split('/');
    var last = p[p.length - 1] || '';
    if (p.indexOf('guides') === -1) return null;
    if (!last.endsWith('.html')) return null;
    if (last === 'index.html' || last.endsWith('.en.html')) return null;
    return last.replace(/\.html$/, '');
  }

  var SLUG = guideSlug();
  if (!SLUG) return;

  var EN_DICT = null;       // 当前指南 { 原文: 英文 }
  var EN_COMMON = null;     // 共享 { 原文: 英文 }
  var EN_COMMON_LOADING = false;
  var APPLIED = false;
  var CJK = /[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]/; // 仅 CJK 主/扩展区 + CJK 标点 + 全角，不含 ASCII 连字符

  function hasCJK(s) { return CJK.test(s); }

  function loadCommon() {
    if (EN_COMMON || EN_COMMON_LOADING || !window.fetch) return Promise.resolve(EN_COMMON);
    EN_COMMON_LOADING = true;
    return fetch('/i18n/guides/_common.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { EN_COMMON = d || {}; EN_COMMON_LOADING = false; return EN_COMMON; })
      .catch(function () { EN_COMMON = {}; EN_COMMON_LOADING = false; return EN_COMMON; });
  }

  function loadDict() {
    if (!window.fetch) return Promise.resolve(null);
    return fetch('/i18n/guides/' + SLUG + '.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d && d.map) EN_DICT = d.map; return d; })
      .catch(function () { return null; });
  }

  function pickEn(k) {
    if (EN_DICT && EN_DICT[k]) return EN_DICT[k];
    if (EN_COMMON && EN_COMMON[k]) return EN_COMMON[k];
    return null;
  }

  function translateChrome() {
    var bcLinks = document.querySelectorAll('.breadcrumb a');
    if (bcLinks[0] && bcLinks[0].textContent.trim() === '首页') bcLinks[0].textContent = 'Home';
    if (bcLinks[1] && bcLinks[1].textContent.trim() === '使用指南') bcLinks[1].textContent = 'User Guide';
    var rt = document.querySelector('.related h3'); if (rt) rt.textContent = 'Related Tools';
    var back = document.querySelector('.back a');
    if (back) {
      var t = back.textContent;
      back.textContent = t.replace('→ 打开', '→ Open').replace(/工具$/, 'Tool');
    }
  }

  function applyEnDict() {
    if (!isEnglish()) return;
    if (!EN_DICT && !EN_COMMON) return;
    var roots = [];
    var main = document.querySelector('main'); if (main) roots.push(main);
    var bc = document.querySelector('.breadcrumb'); if (bc) roots.push(bc);
    var faq = document.querySelector('.faq'); if (faq) roots.push(faq);
    var rel = document.querySelector('.related'); if (rel) roots.push(rel);
    var back = document.querySelector('.back'); if (back) roots.push(back);
    var NF = window.NodeFilter;
    if (!document.createTreeWalker || !NF) { translateChrome(); return; }
    for (var ri = 0; ri < roots.length; ri++) {
      var root = roots[ri];
      if (!root) continue;
      var walker = document.createTreeWalker(root, NF.SHOW_TEXT, null, false);
      var nodes = [];
      var n;
      while ((n = walker.nextNode())) nodes.push(n);
      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        var parent = node.parentNode;
        if (!parent) continue;
        var tag = (parent.nodeName || '').toUpperCase();
        if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
        var raw = node.nodeValue;
        if (!raw) continue;
        var k = raw.trim();
        if (!k || !hasCJK(k)) continue;
        var en = pickEn(k);
        if (!en || en === k) continue;
        var idx = raw.indexOf(k);
        if (idx < 0) continue;
        node.nodeValue = raw.slice(0, idx) + en + raw.slice(idx + k.length);
      }
    }
    translateChrome();
  }

  function apply() {
    if (!isEnglish()) return;
    if (APPLIED) { applyEnDict(); return; }
    loadCommon().then(function () { return loadDict(); }).then(function () {
      APPLIED = true;
      applyEnDict();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(apply, 0); });
  } else {
    apply();
  }
  window.addEventListener('toolbox:langchange', function () { apply(); });
})();
