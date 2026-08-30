/* js/home-categories.js - 首页按一级分类分区块展示（参考 chinaz nav 主体） */
(function () {
  'use strict';

  const MAX_CHILDREN = 6;    // 每个大类默认展示多少个子行业标签
  const MAX_TOOLS = 8;       // 每个子行业默认展示多少个工具

  // ---- i18n 轻量辅助（与 js/i18n.js 并存但不强依赖）----
  function isEn() {
    var l = '';
    try {
      if (window.I18n && typeof window.I18n.get === 'function') l = window.I18n.get() || '';
    } catch (e) { /* ignore */ }
    if (!l) l = document.documentElement.lang || '';
    return String(l).toLowerCase().indexOf('en') === 0;
  }
  // 名称/描述按语言取：英文态优先 en，否则中文
  function nOf(o) { return (isEn() && o && o.en) ? o.en : ((o && o.name) || ''); }
  function dOf(o) {
    var d = (o && o.desc) || '';
    // 描述与名称相同时不重复展示
    return (d && d === o.name) ? '' : d;
  }
  function titleOf(o) {
    var n = nOf(o), d = dOf(o);
    return n + (d ? ' - ' + d : '');
  }

  function ce(tag, cls, html) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (html !== undefined && html !== null) {
      if (typeof html === 'string') el.innerHTML = html; else el.appendChild(html);
    }
    return el;
  }

  function renderToolCard(t) {
    return ce('a', 'hc-tool-card', `
      <span class="hc-tool-icon" style="background:${t.bg || '#f5f5f5'}">${t.icon || '🔧'}</span>
      <span class="hc-tool-body">
        <span class="hc-tool-name">${nOf(t)}</span>
        <span class="hc-tool-desc">${dOf(t)}</span>
      </span>
    `);
  }

  function renderSection(g, container) {
    const section = ce('section', 'hc-section');
    section.dataset.group = g.key;

    // 头部：大类名 + 数量 + 查看全部
    const head = ce('div', 'hc-section-head');
    head.innerHTML = `
      <div class="hc-section-title">
        <span class="hc-section-icon">${g.icon}</span>
        <span class="hc-section-name">${nOf(g)}</span>
        <span class="hc-section-count">${g.count} ${isEn() ? 'tools' : '工具'}</span>
      </div>
      <a class="hc-section-more" href="tools/${g.children[0] ? g.children[0].key : g.key}/index.html">${isEn() ? 'View all' : '查看全部'} →</a>
    `;

    // 子行业标签
    const visibleChildren = g.children.slice(0, MAX_CHILDREN);
    const tabs = ce('div', 'hc-tabs');
    visibleChildren.forEach((c, i) => {
      const btn = ce('button', 'hc-tab' + (i === 0 ? ' active' : ''));
      btn.dataset.child = c.key;
      btn.innerHTML = `<span class="hc-tab-icon">${c.icon}</span><span class="hc-tab-name">${nOf(c)}</span><span class="hc-tab-count">${c.count}</span>`;
      btn.onclick = () => switchChild(section, g, c.key);
      tabs.appendChild(btn);
    });

    // 工具网格
    const grid = ce('div', 'hc-grid');
    grid.dataset.child = visibleChildren[0] ? visibleChildren[0].key : '';
    fillGrid(grid, visibleChildren[0]);

    section.appendChild(head);
    section.appendChild(tabs);
    section.appendChild(grid);
    container.appendChild(section);
  }

  function fillGrid(grid, child) {
    grid.innerHTML = '';
    if (!child || !child.top || !child.top.length) {
      grid.innerHTML = `<div class="hc-empty">${isEn() ? 'No tools yet' : '暂无工具'}</div>`;
      return;
    }
    child.top.slice(0, MAX_TOOLS).forEach(t => {
      const card = renderToolCard(t);
      card.href = t.url;
      card.title = titleOf(t);
      grid.appendChild(card);
    });
  }

  function switchChild(section, g, childKey) {
    const child = g.children.find(c => c.key === childKey);
    if (!child) return;

    section.querySelectorAll('.hc-tab').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.child === childKey);
    });
    const grid = section.querySelector('.hc-grid');
    grid.dataset.child = childKey;
    fillGrid(grid, child);

    // 更新"查看全部"链接
    const more = section.querySelector('.hc-section-more');
    if (more) more.href = `tools/${childKey}/index.html`;
  }

  async function init() {
    const container = document.getElementById('homeCategoriesBody');
    if (!container) return;

    const render = groups => {
      container.innerHTML = '';
      groups.forEach(g => renderSection(g, container));
    };

    try {
      const res = await fetch('/json/industry-groups.json');
      const groups = await res.json();
      render(groups);
      // 语言切换后按新语言重渲染（分类名/工具名中英字段不同）
      window.addEventListener('toolbox:langchange', () => render(groups));
    } catch (e) {
      container.innerHTML = `<div class="hc-empty">${isEn() ? 'Failed to load categories, please refresh' : '分类数据加载失败，请刷新重试'}</div>`;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
