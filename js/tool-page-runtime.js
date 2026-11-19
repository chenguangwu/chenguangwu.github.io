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
      // updateViaCache:'none' —— 不让 HTTP 缓存拖延 sw.js 的更新检测
      navigator.serviceWorker.register('/sw.js', { updateViaCache: 'none' }).then(function(reg){
        reg.update().catch(function(){});
      }).catch(function(){});
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
      // 游戏/对战页的结果是胜负状态而非可复用数据，「复制结果/导出 TXT」无意义且干扰，
      // 整页跳过注入。用严格游戏动作词识别，避免误伤打字/测验等有真实计算价值的工具页。
      var bodyText = (document.body && document.body.textContent || '');
      if (/开始新局|开始游戏|开始对战|再来一局|悔1手|悔棋/.test(bodyText)) return;
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
      // 注意：本文件为 defer 脚本，执行时 common.js 可能尚未加载完毕，
      // 此时 window.ToolBox 上的方法仍是「入队占位(stub)」实现。common.js 就绪后会用
      // 一个全新的对象整体替换 window.ToolBox，导致此处闭包捕获的 TB 永久指向旧的
      // 占位对象 —— 表现为按钮点击无任何效果。因此点击时必须重新解析 window.ToolBox。
      function liveTB(){ return window.ToolBox || TB; }
      var copyBtn = document.createElement('button');
      copyBtn.type = 'button';
      copyBtn.className = 'btn';
      copyBtn.textContent = '📋 复制结果';
      copyBtn.addEventListener('click', function () {
        var T = liveTB();
        if (T && typeof T.copyFromElement === 'function') T.copyFromElement(el.id, '结果已复制');
      });
      var expBtn = document.createElement('button');
      expBtn.type = 'button';
      expBtn.className = 'btn';
      expBtn.textContent = '⬇️ 导出 TXT';
      expBtn.addEventListener('click', function () {
        var t = (el.innerText || el.textContent || '').trim();
        var T = liveTB();
        if (!t) { if (T && T.toast) T.toast('暂无结果可导出'); return; }
        if (T && typeof T.downloadText === 'function') T.downloadText(fname, t);
      });
      bar.appendChild(copyBtn);
      bar.appendChild(expBtn);
      if (el.nextSibling) el.parentNode.insertBefore(bar, el.nextSibling);
      else el.parentNode.appendChild(bar);
    } catch (e) {}
  }

  function findMainButton(){
    var b = document.querySelector('button.primary, .btn.primary, [class*="primary"]');
    if (b) return b;
    var kw = /(计算|转换|换算|生成|试算|运行|提交|开始|求值|加密|解密|编码|解码|格式化|解析|→|=>|＝)/;
    var btns = document.querySelectorAll('button, input[type="submit"], input[type="button"]');
    for (var i = 0; i < btns.length; i++) {
      var t = (btns[i].textContent || btns[i].value || '');
      if (kw.test(t)) return btns[i];
    }
    return null;
  }

  function ensureInputInvalidStyle(){
    try {
      if (document.getElementById('tb-invalid-style')) return;
      var s = document.createElement('style');
      s.id = 'tb-invalid-style';
      s.textContent = '.tb-invalid{border-color:#EF4444!important;box-shadow:0 0 0 2px rgba(239,68,68,.15)!important;}';
      (document.head || document.body || document.documentElement).appendChild(s);
    } catch (e) {}
  }

  function enhanceInputValidation(){
    try {
      ensureInputInvalidStyle();
      var main = findMainButton();
      if (!main) return; // 实时计算类工具（无主按钮）不注入
      main.addEventListener('click', function () {
        var raw = document.querySelectorAll('input,textarea');
        for (var i = 0; i < raw.length; i++) {
          var n = raw[i];
          if (n.type === 'hidden' || n.type === 'submit' || n.type === 'button' ||
              n.type === 'reset' || n.type === 'image' || n.type === 'checkbox' ||
              n.type === 'radio' || n.type === 'range') continue;
          if (n.offsetParent === null) continue;
          if (n.closest && n.closest('.tb-result-actions')) continue;
          if (n.value && String(n.value).trim() !== '') {
            n.classList.remove('tb-invalid');
            n.removeAttribute('title');
            continue;
          }
          n.classList.add('tb-invalid');
          n.setAttribute('title', '请填写此字段后再计算');
        }
      });
      document.addEventListener('focusout', function (e) {
        if (e.target && e.target.classList) e.target.classList.remove('tb-invalid');
      });
    } catch (e) {}
  }

  function ensureRuntime(){
    initToolTheme();
    registerServiceWorker();
    initToolIntro();
    enhanceToolResults();
    enhanceInputValidation();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureRuntime);
  } else {
    ensureRuntime();
  }
})();
