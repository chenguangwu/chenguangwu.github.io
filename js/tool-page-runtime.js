(function(){
  'use strict';

  if (window.__ToolBoxToolRuntime) return;
  window.__ToolBoxToolRuntime = true;

  function getStoredTheme(){
    try {
      var saved = localStorage.getItem('theme');
      if (saved) return saved;
    } catch (e) {}
    return '';
  }

  function resolveTheme(){
    var t = getStoredTheme();
    if (!t && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      t = 'dark';
    }
    return t === 'dark' ? 'dark' : 'light';
  }

  function applyTheme(theme){
    theme = theme === 'dark' ? 'dark' : 'light';
    if (document.body && document.body.classList) {
      document.body.classList.toggle('dark', theme === 'dark');
    }
    if (document.documentElement && document.documentElement.setAttribute) {
      document.documentElement.setAttribute('data-theme', theme);
    }
    if (window.ToolBox && typeof window.ToolBox.applyTheme === 'function') {
      window.ToolBox.applyTheme(theme);
    }
    var btn = document.querySelector('.theme-btn');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  function initToolTheme(){
    applyTheme(resolveTheme());
  }

  function registerServiceWorker(){
    if (document.__toolPageRuntimeSWRegistered) return;
    document.__toolPageRuntimeSWRegistered = true;
    if (!('serviceWorker' in navigator)) return;
    // 是否已被旧版本接管：首次安装不算「更新」，避免首访多刷新一次
    var hadController = !!navigator.serviceWorker.controller;
    var refreshing = false;
    window.__tbUserInteracted = window.__tbUserInteracted || false;
    ['pointerdown', 'keydown', 'input'].forEach(function(evt){
      window.addEventListener(evt, function(){ window.__tbUserInteracted = true; }, { once: true, passive: true });
    });
    window.addEventListener('load', function(){
      // updateViaCache:'none' —— 不让 HTTP 缓存拖延 sw.js 的更新检测
      navigator.serviceWorker.register('/sw.js', { updateViaCache: 'none' }).then(function(reg){
        reg.update().catch(function(){});
      }).catch(function(){});
    });
    navigator.serviceWorker.addEventListener('controllerchange', function(){
      // 新版本已接管：用户尚未操作则静默刷新一次立即呈现最新内容；
      // 正在输入/填表则不打断，等下次自然导航生效。
      if (refreshing || !hadController) return;
      refreshing = true;
      if (window.__tbUserInteracted) return;
      window.location.reload();
    });
  }

  function initToolIntro(){
    var headers = document.querySelectorAll('.tool-intro-header');
    if (!headers.length) return;
    if (document.__toolIntroRuntimeBound) return;
    document.__toolIntroRuntimeBound = true;
    document.addEventListener('click', function(e){
      var target = e.target;
      if (!(target && target.closest)) return;
      var header = target.closest('.tool-intro-header');
      if (!header) return;
      if (!header.parentElement) return;
      header.parentElement.classList.toggle('open');
    });
    document.addEventListener('keydown', function(e){
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var active = document.activeElement;
      if (!active || !active.closest) return;
      var header = active.closest('.tool-intro-header');
      if (!header) return;
      if (!header.parentElement) return;
      e.preventDefault();
      header.parentElement.classList.toggle('open');
    });
  }

  // 竞品通用能力「取长补短」：工具页结果区自动注入「复制结果 / 导出 TXT」操作条。
  // 这是从 calculator.net / rapidtables 等竞品学来的通用交互实践（仅加能力，不抄文案/代码），
  // 一次性覆盖全部工具页，无需逐页改动 HTML，也不影响各页原有 calc 逻辑。
  function enhanceToolResults(){
    try {
      var TB = window.ToolBox;
      if (!TB || typeof TB.copyFromElement !== 'function') return;
      var el = null;
      var selectors = [
        '#result', '#result-box', '#resultBox', '#output', '#output-box', '#outputBox',
        '.result-box', '.result', '[data-result]'
      ];
      for (var i = 0; i < selectors.length; i++) {
        var c = document.querySelector(selectors[i]);
        if (c) { el = c; break; }
      }
      // 兜底：任意含 result/output 的 id（排除注释/提示/计数等非结果节点）
      if (!el) {
        var all = document.querySelectorAll('[id]');
        for (var j = 0; j < all.length; j++) {
          var e2 = all[j];
          var id2 = (e2.id || '').toLowerCase();
          if (/result|output/.test(id2) && !/note|tip|hint|label|desc|count/.test(id2)) {
            var tag = e2.tagName;
            if (tag !== 'INPUT' && tag !== 'TEXTAREA' && tag !== 'SELECT' && tag !== 'BUTTON' && tag !== 'A' && tag !== 'META' && tag !== 'LINK') {
              el = e2; break;
            }
          }
        }
      }
      if (!el) return;
      if (!el.id) el.id = 'tb-tool-result';
      // 防止重复注入
      if (el.parentNode && el.parentNode.querySelector('.tb-result-actions')) return;
      var bar = document.createElement('div');
      bar.className = 'tb-result-actions toolbar';
      bar.style.marginTop = '12px';
      bar.style.gap = '8px';
      bar.style.display = 'flex';
      bar.style.flexWrap = 'wrap';
      var h1 = document.querySelector('h1');
      var rawName = (h1 ? h1.textContent : (document.title || 'tool')).trim();
      var name = rawName.replace(/\s+/g, '-').replace(/[^\w\u4e00-\u9fa5-]/g, '') || 'tool';
      var fname = name + '-result.txt';
      var copyBtn = document.createElement('button');
      copyBtn.type = 'button';
      copyBtn.className = 'btn';
      copyBtn.textContent = '📋 复制结果';
      copyBtn.addEventListener('click', function () { TB.copyFromElement(el.id, '结果已复制'); });
      var expBtn = document.createElement('button');
      expBtn.type = 'button';
      expBtn.className = 'btn';
      expBtn.textContent = '⬇️ 导出 TXT';
      expBtn.addEventListener('click', function () {
        var t = (el.innerText || el.textContent || '').trim();
        if (!t) { if (TB.toast) TB.toast('暂无结果可导出'); return; }
        TB.downloadText(fname, t);
      });
      bar.appendChild(copyBtn);
      bar.appendChild(expBtn);
      if (el.nextSibling) el.parentNode.insertBefore(bar, el.nextSibling);
      else el.parentNode.appendChild(bar);
    } catch (e) {}
  }

  function ensureRuntime(){
    initToolTheme();
    registerServiceWorker();
    initToolIntro();
    enhanceToolResults();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureRuntime);
  } else {
    ensureRuntime();
  }
})();
