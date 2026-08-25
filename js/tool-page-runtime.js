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
    window.addEventListener('load', function(){
      navigator.serviceWorker.register('/sw.js').catch(function(){});
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
