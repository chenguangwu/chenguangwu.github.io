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

  // 阶段二·取长补短：示例填充（试算）通用增强
  // 对所有「固定输入 + 主操作按钮 + 无既有试算按钮」的工具页注入「✨ 试算示例」按钮，
  // 点击时自动填充合理示例值并触发主计算，让用户一键看到工具效果（对标竞品标配示例）。
  // 动态生成输入的工具（如选公式后才 innerHTML 出 input）初始 DOM 无输入，自动跳过，安全。
  function enhanceExampleFill(){
    try {
      var TB = window.ToolBox;
      if (!TB) return;
      var injected = false;
      function tryInject(){
        if (injected) return;
        var raw = document.querySelectorAll('input,select,textarea');
        var inputs = [];
        for (var i = 0; i < raw.length; i++) {
          var n = raw[i];
          if (n.type === 'hidden' || n.type === 'submit' || n.type === 'button' ||
              n.type === 'reset' || n.type === 'image') continue;
          if (n.offsetParent === null) continue; // 不可见跳过
          if (n.closest && n.closest('.tb-result-actions')) continue;
          inputs.push(n);
        }
        if (inputs.length < 1) return; // 无输入（动态生成类尚未出现）暂不注入
        var main = findMainButton();
        if (!main) return;
        var allBtns = document.querySelectorAll('button');
        for (var k = 0; k < allBtns.length; k++) {
          if (/试算|示例|example|fill|填入|demo/i.test(allBtns[k].textContent || '')) return;
        }
        if (main.parentNode && main.parentNode.querySelector('.tb-demo-btn')) return;
        var demo = document.createElement('button');
        demo.type = 'button';
        demo.className = 'btn tb-demo-btn';
        demo.textContent = '✨ 试算示例';
        demo.addEventListener('click', function () { fillAndDemo(main); });
        if (main.nextSibling) main.parentNode.insertBefore(demo, main.nextSibling);
        else main.parentNode.appendChild(demo);
        injected = true;
      }
      tryInject();
      if (injected) return;
      // 动态生成输入的工具（选公式/类型后才 innerHTML 出 input）：监听 DOM 变化重试注入
      if (window.MutationObserver) {
        var pending = false;
        var mo = new MutationObserver(function () {
          if (pending) return;
          pending = true;
          setTimeout(function () {
            pending = false;
            if (tryInject()) { try { mo.disconnect(); } catch (e2) {} }
          }, 300);
        });
        mo.observe(document.body, { childList: true, subtree: true });
        setTimeout(function () { try { mo.disconnect(); } catch (e2) {} }, 12000);
      }
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

  function placeholderNum(el){
    var p = el.placeholder || '';
    var m = p.match(/-?\d+(\.\d+)?/);
    return m ? parseFloat(m[0]) : null;
  }

  function fillAndDemo(main){
    try {
      var raw = document.querySelectorAll('input,select,textarea');
      for (var i = 0; i < raw.length; i++) {
        var el = raw[i];
        if (el.type === 'hidden' || el.type === 'submit' || el.type === 'button' ||
            el.type === 'reset' || el.type === 'image') continue;
        if (el.offsetParent === null) continue;
        if (el.closest && el.closest('.tb-result-actions')) continue;
        if (el.value && String(el.value).trim() !== '') continue; // 不覆盖已填
        if (el.tagName === 'SELECT') {
          var opt = el.querySelector('option:not([disabled])');
          if (opt) el.value = opt.value;
        } else if (el.type === 'number') {
          var v = placeholderNum(el);
          if (v === null && el.min !== '' && !isNaN(parseFloat(el.min))) v = parseFloat(el.min);
          if (v === null) v = 1;
          el.value = String(v);
        } else {
          el.value = el.placeholder || '示例';
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
      if (main) main.click();
    } catch (e) {}
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
    enhanceExampleFill();
    enhanceInputValidation();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureRuntime);
  } else {
    ensureRuntime();
  }
})();
