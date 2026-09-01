/*
 * ToolBox 通用工具体验增强模块 (js/tool-ux.js)
 * 设计原则：纯前端、本地、零冲突、可幂等重复加载。
 * 不重复页面既有工具栏，只补齐页面间未统一的轻量增强：
 *   1) 对「确实没有」复制/下载工具栏的结果区，注入一个复制/下载操作条；
 *   2) 输入校验友好提示（focusout 时给出具体原因，不拦截页面逻辑）；
 *   3) 输入值 localStorage 持久化（仅回填用户空字段，不覆盖页面默认/示例）；
 *   4) 结果区加 aria-live，提升屏幕阅读器可访问性。
 */
(function () {
  'use strict';

  if (window.__TOOL_UX__) return; // 去重：防止被多次引入重复执行
  window.__TOOL_UX__ = true;

  var PERSIST_PREFIX = 'tb_ux_';
  var PERSIST_NS = (function () {
    try { return PERSIST_PREFIX + (location.pathname || 'page'); } catch (e) { return PERSIST_PREFIX + 'page'; }
  })();

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function isInputField(el) {
    if (!el) return false;
    var t = (el.tagName || '').toLowerCase();
    if (t === 'textarea' || t === 'select') return true;
    if (t === 'input') {
      var ty = (el.getAttribute('type') || 'text').toLowerCase();
      return !(ty === 'submit' || ty === 'button' || ty === 'reset' || ty === 'hidden' || ty === 'file' || ty === 'password');
    }
    return false;
  }

  function fieldKey(el, idx) {
    return PERSIST_NS + '#' + (el.id || el.name || ('ix' + idx));
  }

  /* ---------- 1) 结果区复制/下载操作条 ---------- */
  var RESULT_SELECTORS = [
    '#output', '#result', '#resultArea', '#resultBox', '#result-area', '#out', '#res',
    '.result-box', '.result', '.json-output', '.tool-output', '[data-result]', 'pre.result'
  ];

  function findResultContainer() {
    for (var i = 0; i < RESULT_SELECTORS.length; i++) {
      var nodes = $all(RESULT_SELECTORS[i]);
      for (var j = 0; j < nodes.length; j++) {
        var el = nodes[j];
        if (el.offsetParent === null) continue;            // 不可见跳过
        var t = (el.tagName || '').toLowerCase();
        if (t === 'input' || t === 'button') continue;     // 非展示区
        if (el.classList.contains('tool-ux-bar')) continue;
        return el;
      }
    }
    return null;
  }

  function hasNearbyToolbar(res) {
    var rr = res.getBoundingClientRect();
    var rc = (rr.top + rr.bottom) / 2;
    var btns = $all('button, input[type="submit"]');
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i];
      var br = b.getBoundingClientRect();
      if (br.width === 0 && br.height === 0) continue;
      var bc = (br.top + br.bottom) / 2;
      var dy = Math.abs(bc - rc);
      if (dy < 340 && br.left < rr.right + 220 && br.right > rr.left - 220) return true;
    }
    return false;
  }

  function getResultText(res) {
    if (res.value != null && typeof res.value === 'string') return res.value;
    return (res.innerText || res.textContent || '').replace(/\n{3,}/g, '\n\n').trim();
  }

  function fmtFileName() {
    var title = (document.title || 'toolbox-result').replace(/\s*[-–]\s*ToolBox\s*$/i, '').replace(/[\\/:*?"<>|]+/g, '_').trim();
    return (title || 'toolbox-result').slice(0, 60) + '.txt';
  }

  function downloadText(text, filename) {
    try {
      var blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
      return true;
    } catch (e) { return false; }
  }

  function toast(msg, type) {
    try {
      if (window.ToolBox && typeof window.ToolBox.showToast === 'function') { window.ToolBox.showToast(msg, type || 'success'); return; }
    } catch (e) {}
    try {
      var t = document.createElement('div');
      t.textContent = msg;
      t.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:' +
        (type === 'error' ? '#EF4444' : '#10B981') + ';color:#fff;padding:10px 18px;border-radius:12px;font-size:13px;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,.2);';
      document.body.appendChild(t);
      setTimeout(function () { t.remove(); }, 2200);
    } catch (e) {}
  }

  function enhanceResults() {
    var res = findResultContainer();
    if (!res) return;
    if (hasNearbyToolbar(res)) return; // 页面已有工具栏，不重复注入
    if (res.parentNode && $('.tool-ux-bar', res.parentNode)) return;

    var bar = document.createElement('div');
    bar.className = 'tool-ux-bar';
    bar.setAttribute('role', 'toolbar');
    bar.setAttribute('aria-label', '结果操作');

    var copyBtn = document.createElement('button');
    copyBtn.type = 'button';
    copyBtn.className = 'btn';
    copyBtn.textContent = '📋 复制结果';
    copyBtn.addEventListener('click', function () {
      var txt = getResultText(res);
      if (!txt) { toast('暂无结果', 'info'); return; }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt).then(function () { toast('已复制结果'); }, function () { fallbackCopy(txt); });
      } else { fallbackCopy(txt); }
    });

    var dlBtn = document.createElement('button');
    dlBtn.type = 'button';
    dlBtn.className = 'btn';
    dlBtn.textContent = '💾 下载结果';
    dlBtn.addEventListener('click', function () {
      var txt = getResultText(res);
      if (!txt) { toast('暂无结果', 'info'); return; }
      if (downloadText(txt, fmtFileName())) toast('已下载结果'); else toast('下载失败', 'error');
    });

    bar.appendChild(copyBtn);
    bar.appendChild(dlBtn);

    try {
      if (res.parentNode) res.parentNode.insertBefore(bar, res);
    } catch (e) {}
  }

  function fallbackCopy(text) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.cssText = 'position:fixed;left:-9999px;opacity:0;';
      document.body.appendChild(ta); ta.select();
      document.execCommand('copy'); ta.remove(); toast('已复制结果');
    } catch (e) { toast('复制失败，请手动选择', 'error'); }
  }

  /* ---------- 2) 输入校验友好提示 ---------- */
  function friendlyReason(el) {
    if (el.validity && el.validity.valueMissing) return '此项为必填，请填写后再继续';
    if (el.validity && el.validity.typeMismatch) {
      var ty = (el.getAttribute('type') || '').toLowerCase();
      if (ty === 'email') return '请输入有效的邮箱地址';
      if (ty === 'url') return '请输入有效的网址（含 http(s)://）';
      if (ty === 'number') return '请输入有效的数字';
      return '格式不正确，请检查后重试';
    }
    if (el.validity && el.validity.tooShort) return '内容过短，至少 ' + (el.getAttribute('minlength') || '?') + ' 个字符';
    if (el.validity && el.validity.tooLong) return '内容过长，最多 ' + (el.getAttribute('maxlength') || '?') + ' 个字符';
    if (el.validity && el.validity.rangeUnderflow) return '数值不能小于 ' + el.getAttribute('min');
    if (el.validity && el.validity.rangeOverflow) return '数值不能大于 ' + el.getAttribute('max');
    if (el.validity && el.validity.stepMismatch) return '请输入合法的步进值（如 ' + el.getAttribute('step') + ' 的倍数）';
    if (el.validity && el.validity.patternMismatch) return '格式不符合要求，请按提示填写';
    if (el.validity && el.validity.badInput) return '请输入有效内容';
    return '输入有误，请检查后重试';
  }

  function enhanceValidation() {
    document.addEventListener('focusout', function (e) {
      var el = e.target;
      if (!isInputField(el)) return;
      if (typeof el.checkValidity !== 'function') return;
      if (!el.checkValidity()) {
        el.setAttribute('aria-invalid', 'true');
        if (!el.hasAttribute('data-ux-orig-title')) el.setAttribute('data-ux-orig-title', el.title || '');
        el.title = friendlyReason(el);
        el.classList.add('ux-field-error');
      } else {
        el.removeAttribute('aria-invalid');
        el.classList.remove('ux-field-error');
        if (el.hasAttribute('data-ux-orig-title')) {
          el.title = el.getAttribute('data-ux-orig-title');
          el.removeAttribute('data-ux-orig-title');
        }
      }
    }, true);
  }

  /* ---------- 3) 输入值 localStorage 持久化 ---------- */
  var persistTimer = null;
  function saveField(el, idx) {
    try {
      var v;
      var t = (el.tagName || '').toLowerCase();
      if (t === 'select') v = el.value;
      else if (t === 'textarea' || t === 'input') v = el.value;
      else return;
      if (el.type === 'checkbox' || el.type === 'radio') v = el.checked ? '1' : '0';
      localStorage.setItem(fieldKey(el, idx), v);
    } catch (e) {}
  }

  function enhancePersistence() {
    var fields = $all('.container input, .container textarea, .container select').filter(isInputField);
    if (!fields.length) return;

    fields.forEach(function (el, idx) {
      // 回填：仅当用户之前存过值、且当前字段为空时，避免覆盖页面默认/示例
      try {
        var saved = localStorage.getItem(fieldKey(el, idx));
        if (saved != null && saved !== '') {
          var t = (el.tagName || '').toLowerCase();
          var empty = (el.value === '' || el.value == null);
          if (el.type === 'checkbox' || el.type === 'radio') {
            if (saved === '1' && !el.checked) el.checked = true;
          } else if (empty) {
            el.value = saved;
          }
        }
      } catch (e) {}

      var evt = (el.tagName || '').toLowerCase() === 'select' ? 'change' : 'input';
      el.addEventListener(evt, function () {
        if (persistTimer) clearTimeout(persistTimer);
        var cur = idx;
        persistTimer = setTimeout(function () { saveField(el, cur); }, 300);
      });
      el.addEventListener('change', function () { saveField(el, idx); });
    });
  }

  /* ---------- 4) 结果区可访问性 ---------- */
  function enhanceA11y() {
    var res = findResultContainer();
    if (res && !res.hasAttribute('aria-live')) {
      try { res.setAttribute('aria-live', 'polite'); res.setAttribute('tabindex', '-1'); } catch (e) {}
    }
  }

  function init() {
    try { enhanceResults(); } catch (e) {}
    try { enhanceValidation(); } catch (e) {}
    try { enhancePersistence(); } catch (e) {}
    try { enhanceA11y(); } catch (e) {}
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
