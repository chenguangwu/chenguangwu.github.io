// js/tool-search.js — ToolBox 全站统一的「实时下拉搜索」组件
//
// 目标：顶部搜索框输入即出下拉结果（图标 + 工具名 + 描述），与 404 页搜索体验一致。
// 唯一实现：404 页、全站统一顶栏（common.js 注入）、任何带 data-tb-search 的输入框共用本文件，
// 避免多份内联实现漂移（历史上 404 与 search.html 各写一份 → 描述字段口径不一致）。
//
// 关键口径（防"名称当描述"复发）：
//   - 名称：en-US 取 t.en，否则 t.n
//   - 描述：en-US 取 t.ed，否则 t.d（**不是 t.desc**，tools.json 的 desc 是历史坏数据）
//   - 繁体：数据源走 I18n.assetUrl('/json/tools.json') → /zh-tw/json/tools.json（构建期繁体化）
//   - 拼音：t.py（全拼）/ t.pyi（首字母），与首页 search.html 的容错口径一致
//
// 用法：
//   ToolBoxSearch.mount(inputEl, { panel: optPanelEl, limit: 8 })
//   ToolBoxSearch.mountAll()   // 扫描 .nav-search input[name=q] 与 input[data-tb-search]
(function () {
  'use strict';

  var DATA_URL = '/json/tools.json';
  var INDEX = null;          // 精简索引（内存共享，同一页面只 fetch 一次）
  var LOADING = false;
  var WAITERS = [];
  var INSTANCES = [];

  // ---------- 环境适配 ----------
  function assetUrl(u) {
    try { if (window.I18n && window.I18n.assetUrl) return window.I18n.assetUrl(u); } catch (e) {}
    return u;
  }
  function isEn() {
    try { return !!(window.I18n && window.I18n.isEnglish && window.I18n.isEnglish()); } catch (e) {}
    return false;
  }
  function T(k, fb) {
    try { if (window.I18n && window.I18n.t) return window.I18n.t(k, fb); } catch (e) {}
    return fb;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ---------- 索引加载（懒加载 + 内存缓存） ----------
  function toItem(t) {
    return {
      n: t.name || '',
      en: t.en || '',
      d: t.d || t.desc || '',
      ed: t.ed || '',
      i: t.industry || '',
      u: t.url || '',
      ic: t.icon || '🔧',
      b: t.bg || '#f5f5f5',
      q: t.quality || '',
      h: t.hot || 0,
      al: t.al || [],
      py: String(t.py || '').toLowerCase(),
      pyi: String(t.pyi || '').toLowerCase()
    };
  }

  function loadIndex(cb) {
    if (INDEX) { if (cb) cb(INDEX); return; }
    if (cb) WAITERS.push(cb);
    if (LOADING) return;
    LOADING = true;
    var url = assetUrl(DATA_URL);
    fetch(url)
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (raw) {
        INDEX = (Array.isArray(raw) ? raw : []).map(toItem);
      })
      .catch(function () { INDEX = []; })
      .then(function () {
        LOADING = false;
        var q = WAITERS.slice();
        WAITERS.length = 0;
        for (var i = 0; i < q.length; i++) { try { q[i](INDEX); } catch (e) {} }
      });
  }

  // ---------- 匹配打分（名称 > 英文名 > 别名 > 拼音 > 描述；同级按热度） ----------
  function scoreOf(it, ql) {
    var nm = it.n.toLowerCase(), en = it.en.toLowerCase();
    var s = 0, i, a;
    if (nm === ql || en === ql) s = 120;
    else if (nm.indexOf(ql) === 0 || en.indexOf(ql) === 0) s = 100;
    else if (nm.indexOf(ql) !== -1 || en.indexOf(ql) !== -1) s = 80;
    if (!s) {
      for (i = 0; i < it.al.length; i++) {
        a = String(it.al[i]).toLowerCase();
        if (a === ql) { s = 70; break; }
        if (a.indexOf(ql) !== -1 && s < 55) s = 55;
      }
    }
    if (!s && it.py) {
      if (it.py.indexOf(ql) === 0) s = 60;
      else if ((' ' + it.pyi + ' ').indexOf(' ' + ql) !== -1) s = 58;
      else if (it.py.indexOf(ql) !== -1) s = 40;
    }
    if (!s && (it.d.toLowerCase().indexOf(ql) !== -1 || it.ed.toLowerCase().indexOf(ql) !== -1)) s = 25;
    if (s) s += Math.min(9, Math.round(it.h / 2500));   // 热度微调，不改变量级
    return s;
  }

  function query(q, limit) {
    var ql = String(q || '').trim().toLowerCase();
    if (!ql || !INDEX) return [];
    var hits = [];
    for (var i = 0; i < INDEX.length; i++) {
      var sc = scoreOf(INDEX[i], ql);
      if (sc > 0) hits.push({ it: INDEX[i], sc: sc });
    }
    hits.sort(function (a, b) { return b.sc - a.sc || b.it.h - a.it.h; });
    var all = hits.map(function (x) { return x.it; });
    if (limit === 0) return all;          // 0 = 全量（搜索结果页需要完整列表）
    return all.slice(0, limit || 8);
  }

  // ---------- 实例渲染 ----------
  function nameOf(it) { return (isEn() && it.en) ? it.en : it.n; }
  function descOf(it) { return (isEn() && it.ed) ? it.ed : it.d; }

  function itemHtml(it, idx) {
    var badge = (it.q && it.q !== 'B') ? '<span class="tb-sr-q">' + esc(it.q) + '</span>' : '';
    return '<a class="tb-sr-item" role="option" data-idx="' + idx + '" href="' + esc(assetUrl('/' + it.u)) + '">' +
      '<span class="tb-sr-ic" style="background:' + esc(it.b) + '">' + esc(it.ic) + '</span>' +
      '<span class="tb-sr-info">' +
        '<span class="tb-sr-name"><span class="tb-sr-nm">' + esc(nameOf(it)) + '</span>' + badge + '</span>' +
        '<span class="tb-sr-desc">' + esc(descOf(it)) + '</span>' +
      '</span></a>';
  }

  function allRowHtml(q) {
    return '<a class="tb-sr-all" href="' + esc(assetUrl('/search.html')) + '?q=' + encodeURIComponent(q) + '">' +
      esc(T('search.view_all', '查看全部搜索结果')) + ' →</a>';
  }

  function panelOf(inst) {
    if (inst.panel) return inst.panel;
    var holder = inst.input.parentNode;
    inst.panel = document.createElement('div');
    inst.panel.className = 'tb-sr-panel';
    inst.panel.setAttribute('role', 'listbox');
    inst.panel.hidden = true;
    holder.appendChild(inst.panel);
    return inst.panel;
  }

  function close(inst) {
    if (!inst.panel) return;
    inst.panel.hidden = true;
    inst.panel.innerHTML = '';
    inst.active = -1;
  }

  function paint(inst, html) {
    var p = panelOf(inst);
    p.innerHTML = html;
    p.hidden = false;
    inst.active = -1;
  }

  function refresh(inst) {
    var q = String(inst.input.value || '').trim();
    if (!q) { close(inst); return; }
    if (!INDEX) {
      if (!LOADING) loadIndex();
      paint(inst, '<div class="tb-sr-tip">' + esc(T('search.searching', '正在加载工具索引…')) + '</div>');
      return;
    }
    var hits = query(q, inst.limit);
    if (!hits.length) {
      paint(inst, '<div class="tb-sr-tip">' + esc(T('search.no_match', '没有找到匹配的工具')) + '</div>' + allRowHtml(q));
      return;
    }
    var html = '';
    for (var i = 0; i < hits.length; i++) html += itemHtml(hits[i], i);
    paint(inst, html + allRowHtml(q));
  }

  function move(inst, delta) {
    var items = inst.panel ? inst.panel.querySelectorAll('.tb-sr-item') : [];
    if (!items.length) return;
    inst.active = (inst.active + delta + items.length) % items.length;
    for (var i = 0; i < items.length; i++) items[i].classList.toggle('is-active', i === inst.active);
  }

  function openActive(inst) {
    var items = inst.panel ? inst.panel.querySelectorAll('.tb-sr-item') : [];
    if (inst.active >= 0 && items[inst.active]) {
      location.href = items[inst.active].getAttribute('href');
      return true;
    }
    return false;
  }

  // ---------- 挂载 ----------
  function mount(input, opts) {
    if (!input || input.__tbSearchMounted) return null;
    opts = opts || {};
    input.__tbSearchMounted = true;
    input.setAttribute('autocomplete', 'off');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');

    var inst = {
      input: input,
      panel: opts.panel || null,
      limit: opts.limit || 8,
      active: -1,
      timer: null
    };

    // 面板容器：优先复用宿主内已静态放置的面板（如 404.html 的 #searchResults），
    // 否则在宿主末尾新建。宿主取 input 最近的 .search-wrap / .nav-search，
    // 保证面板绝对定位的参照物与 CSS 的一致性。
    var host = null;
    try { host = input.closest('.nav-search, .search-wrap'); } catch (e) { host = null; }
    if (!host) host = input.parentNode;
    if (!inst.panel) inst.panel = host.querySelector('.tb-sr-panel');
    if (inst.panel) {
      inst.panel.classList.add('tb-sr-panel');
      inst.panel.setAttribute('role', 'listbox');
      inst.panel.hidden = true;
    } else {
      try {
        if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
      } catch (e) { host.style.position = 'relative'; }
      inst.panel = document.createElement('div');
      inst.panel.className = 'tb-sr-panel';
      inst.panel.setAttribute('role', 'listbox');
      inst.panel.hidden = true;
      host.appendChild(inst.panel);
    }

    input.addEventListener('input', function () {
      clearTimeout(inst.timer);
      var v = input.value;
      inst.timer = setTimeout(function () { refresh(inst); }, v.trim() ? 120 : 0);
    });
    input.addEventListener('focus', function () {
      loadIndex();
      if (input.value.trim()) refresh(inst);
    });
    input.addEventListener('blur', function () { setTimeout(function () { close(inst); }, 180); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(inst, 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(inst, -1); }
      else if (e.key === 'Enter') {
        if (openActive(inst)) e.preventDefault();   // 已用方向键选中 → 直达该工具
      } else if (e.key === 'Escape') {
        close(inst);
        input.blur();
      }
    });
    // 点击项：先于 blur 生效
    document.addEventListener('mousedown', function (e) {
      if (inst.panel && inst.panel.contains(e.target)) e.preventDefault();
    });

    INSTANCES.push(inst);
    return inst;
  }

  function mountAll() {
    var inputs = document.querySelectorAll('.nav-search input[name="q"], input[data-tb-search]');
    for (var i = 0; i < inputs.length; i++) mount(inputs[i]);
  }

  function refreshAll() {
    for (var i = 0; i < INSTANCES.length; i++) {
      var inst = INSTANCES[i];
      if (inst.input.value.trim()) refresh(inst);
    }
  }

  // 语言切换后重渲染（名称/描述语言变化）
  window.addEventListener('toolbox:langchange', refreshAll);

  // 顶栏由 common.js 运行时注入 → 用观察者 + 定时兜底确保挂上
  function autoMount() {
    mountAll();
    if (INSTANCES.length) return;
    var n = 0;
    var timer = setInterval(function () {
      mountAll();
      if (INSTANCES.length || ++n > 40) clearInterval(timer);
    }, 100);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(autoMount, 0); });
  } else {
    setTimeout(autoMount, 0);
  }
  try {
    if (window.MutationObserver) {
      var mo = new MutationObserver(function () { mountAll(); });
      mo.observe(document.documentElement, { childList: true, subtree: true });
    }
  } catch (e) {}

  window.ToolBoxSearch = {
    mount: mount,
    mountAll: mountAll,
    preload: function () { loadIndex(); },
    ready: function (cb) { loadIndex(cb); },        // 索引就绪回调（搜索结果页启动用）
    getIndex: function () { return INDEX; },
    // 搜索：下拉与搜索结果页共用同一打分器，保证「下拉能搜到、结果页却没有」不再发生。
    // limit 省略=8（下拉默认）；limit=0=全量（搜索结果页）。
    search: function (q, limit) { return query(q, limit); },
    // 共享逐词打分器：首页网格搜索（toolboxSearch）与顶栏下拉统一口径时复用，
    // 传入 (query, item)，返回 >0 表示命中及权重（与下拉完全一致）。
    score: function (q, item) { return scoreOf(item, String(q || '').trim().toLowerCase()); },
    format: { nameOf: nameOf, descOf: descOf }
  };
})();
