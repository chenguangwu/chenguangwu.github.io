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

  function ensureRuntime(){
    initToolTheme();
    registerServiceWorker();
    initToolIntro();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureRuntime);
  } else {
    ensureRuntime();
  }
})();
