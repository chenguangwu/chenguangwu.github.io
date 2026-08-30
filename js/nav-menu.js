/* js/nav-menu.js - 全站 2 级分类导航（顶部横向菜单 + 下拉面板 + 移动端抽屉）
 * 布局参考 chinaz tools/nav，UI 用 ToolBox 橙紫风格。
 * 依赖：window.INDUSTRY_INFO（js/industry-info.js 提供）
 */
(function () {
  'use strict';

  const CLS_ACTIVE = 'active';
  const CLS_OPEN = 'open';
  let groups = [];
  let activeGroupIndex = 0;
  let activeChildIndex = 0;
  let loaded = false;
  let hoverTimer = null;

  // ---- i18n 轻量辅助（与 js/i18n.js 并存但不强依赖）----
  function _t(key, fb) {
    if (window.I18n && window.I18n.t) return window.I18n.t(key, fb);
    return fb !== undefined ? fb : key;
  }

  // 当前是否为英文态（i18n 未就绪时回退 <html lang>）
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
    if (!o) return '';
    // 英文态取英文描述：多数工具没有实质英文描述（ed 为空），此时只显示名称，
    // 不回退中文描述，避免「英文名 + 中文描述」混排
    var d = isEn() ? (o.ed || '') : (o.desc || '');
    return (d && d === nOf(o)) ? '' : d;
  }
  // 名称 + 描述拼成卡片 title（悬浮提示）
  function titleOf(o) {
    var n = nOf(o), d = dOf(o);
    return n + (d ? ' - ' + d : '');
  }

  // ---- DOM 创建辅助 ----
  function $(sel) { return document.querySelector(sel); }
  function ce(tag, cls, html) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (html !== undefined && html !== null) {
      if (typeof html === 'string') el.innerHTML = html; else el.appendChild(html);
    }
    return el;
  }

  // ---- 数据加载 ----
  async function loadGroups() {
    if (loaded) return groups;
    try {
      const res = await fetch('/json/industry-groups.json');
      groups = await res.json();
      loaded = true;
    } catch (e) {
      groups = [];
    }
    return groups;
  }

  // ---- 渲染顶部导航 ----
  function renderTopNav(container) {
    container.innerHTML = '';
    const inner = ce('div', 'tb-nav-inner');
    // 不渲染 Logo：第二行只放分类，返回首页由第一行 .nav-top 的 Logo 承担

    const menu = ce('ul', 'tb-nav-menu');
    groups.forEach((g, i) => {
      const li = ce('li', 'tb-nav-item');
      const a = ce('a', 'tb-nav-link', `<span class="tb-nav-link-icon">${g.icon}</span><span>${nOf(g)}</span>`);
      a.href = '#';
      a.dataset.index = i;
      li.appendChild(a);
      menu.appendChild(li);
    });

    const right = ce('div', 'tb-nav-right');
    // 不渲染搜索按钮：第一行 .nav-top 已有搜索框，此处去重（老板要求）
    // 主题切换：桌面由旧 nav-top 提供，此处主要服务移动端（顶部只有这一层导航）
    const themeBtn = ce('button', 'tb-nav-theme-btn', '<span id="tbNavThemeIcon">🌙</span>');
    themeBtn.title = _t('nav.theme', '切换主题');
    themeBtn.onclick = () => { if (typeof window.toggleTheme === 'function') window.toggleTheme(); };

    const mobileToggle = ce('button', 'tb-nav-mobile-toggle', '☰');
    mobileToggle.title = _t('nav.menu', '菜单');
    mobileToggle.onclick = () => { toggleMobileDrawer(true); };
    right.appendChild(themeBtn);
    right.appendChild(mobileToggle);

    inner.appendChild(menu);
    inner.appendChild(right);
    container.appendChild(inner);

    // 事件：桌面 hover/click 一级菜单展开下拉
    menu.addEventListener('mouseover', e => {
      const link = e.target.closest('.tb-nav-link');
      if (!link) return;
      const idx = parseInt(link.dataset.index, 10);
      if (hoverTimer) clearTimeout(hoverTimer);
      hoverTimer = setTimeout(() => showMegaPanel(idx), 80);
    });
    menu.addEventListener('mouseleave', () => {
      if (hoverTimer) clearTimeout(hoverTimer);
      // 鼠标离开导航条且不进入面板时关闭；面板 mouseenter 会重新定时
    });
    menu.addEventListener('click', e => {
      const link = e.target.closest('.tb-nav-link');
      if (!link) return;
      e.preventDefault();
      const idx = parseInt(link.dataset.index, 10);
      showMegaPanel(idx);
    });
  }

  // ---- 渲染下拉面板 ----
  function renderMegaPanel(container) {
    container.innerHTML = '';
    const inner = ce('div', 'tb-megapanel-inner');
    const head = ce('div', 'tb-megapanel-head');
    const catCol = ce('div', 'tb-megapanel-cats');
    const toolsCol = ce('div', 'tb-megapanel-tools');
    head.appendChild(catCol);
    head.appendChild(toolsCol);
    inner.appendChild(head);
    container.appendChild(inner);

    // 鼠标进入面板保持打开；离开整个导航条关闭
    container.addEventListener('mouseenter', () => {
      if (hoverTimer) clearTimeout(hoverTimer);
    });
    container.addEventListener('mouseleave', () => {
      closeMegaPanel();
    });
  }

  function showMegaPanel(groupIndex) {
    activeGroupIndex = groupIndex;
    activeChildIndex = 0;
    const panel = $('#tbMegapanel');
    const container = $('#tbTopnav');
    if (!panel || !container) return;

    const g = groups[groupIndex];
    if (!g) return;

    // 高亮当前一级菜单
    container.querySelectorAll('.tb-nav-link').forEach((a, i) => {
      a.classList.toggle(CLS_ACTIVE, i === groupIndex);
    });

    const catCol = panel.querySelector('.tb-megapanel-cats');
    const toolsCol = panel.querySelector('.tb-megapanel-tools');

    // 按子行业数量决定左侧列数与宽度：目标是一屏放得下、不用滚动
    // （工程制造 69 个→4 列，商业办公 51 个→4 列，健康医疗 34 个→3 列）
    const head = panel.querySelector('.tb-megapanel-head');
    if (head) {
      const n = g.children ? g.children.length : 0;
      // 目标：一屏装下全部二级分类，不再出现面板内滚动
      // 69 个（工程制造）→5 列 14 行，51 个（商业办公）→4 列 13 行
      const cols = n <= 16 ? 1 : n <= 32 ? 2 : n <= 48 ? 3 : n <= 64 ? 4 : 5;
      const width = [0, 190, 370, 540, 700, 760][cols];
      head.style.setProperty('--tb-cat-cols', String(cols));
      head.style.setProperty('--tb-cats-width', width + 'px');
    }

    // 左侧子行业列表
    catCol.innerHTML = '';
    const catTitle = ce('div', 'tb-megapanel-cats-title', nOf(g));
    catCol.appendChild(catTitle);
    const catList = ce('ul', 'tb-megapanel-cat-list');
    g.children.forEach((c, i) => {
      const li = ce('li', 'tb-megapanel-cat-item' + (i === 0 ? ' ' + CLS_ACTIVE : ''));
      li.dataset.index = i;
      li.innerHTML = `<span class="tb-cat-icon">${c.icon}</span><span class="tb-cat-name">${nOf(c)}</span><span class="tb-cat-count">${c.count}</span>`;
      li.onclick = () => selectChild(i);
      catList.appendChild(li);
    });
    catCol.appendChild(catList);

    // 右侧工具网格（默认显示第一个子行业）
    renderToolsCol(toolsCol, g, 0);

    panel.classList.add(CLS_OPEN);
  }

  function selectChild(childIndex) {
    activeChildIndex = childIndex;
    const panel = $('#tbMegapanel');
    const g = groups[activeGroupIndex];
    if (!panel || !g) return;
    const items = panel.querySelectorAll('.tb-megapanel-cat-item');
    items.forEach((li, i) => li.classList.toggle(CLS_ACTIVE, i === childIndex));
    renderToolsCol(panel.querySelector('.tb-megapanel-tools'), g, childIndex);
  }

  function renderToolsCol(toolsCol, group, childIndex) {
    const c = group.children[childIndex];
    if (!c) return;
    toolsCol.innerHTML = '';
    const header = ce('div', 'tb-megapanel-tools-header');
    header.innerHTML = `<span class="tb-tools-header-icon">${c.icon}</span><span class="tb-tools-header-name">${nOf(c)}</span><a class="tb-tools-header-more" href="/tools/${c.key}/index.html">${isEn() ? 'View all' : '查看全部'} ${c.count} ${isEn() ? 'tools' : '个工具'} →</a>`;
    toolsCol.appendChild(header);

    const grid = ce('div', 'tb-megapanel-tools-grid');
    if (c.top && c.top.length) {
      c.top.forEach(t => {
        const card = ce('a', 'tb-megapanel-tool-card');
        card.href = t.url;
        card.title = titleOf(t);
        card.innerHTML = `
          <span class="tb-tool-icon" style="background:${t.bg || '#f5f5f5'}">${t.icon || '🔧'}</span>
          <span class="tb-tool-body">
            <span class="tb-tool-name">${nOf(t)}</span>
            <span class="tb-tool-desc">${dOf(t)}</span>
          </span>`;
        grid.appendChild(card);
      });
    } else {
      grid.innerHTML = `<div class="tb-megapanel-empty">${_t('nav.no_tools', '暂无工具')}</div>`;
    }
    toolsCol.appendChild(grid);
  }

  function closeMegaPanel() {
    const panel = $('#tbMegapanel');
    const container = $('#tbTopnav');
    if (panel) panel.classList.remove(CLS_OPEN);
    if (container) container.querySelectorAll('.tb-nav-link').forEach(a => a.classList.remove(CLS_ACTIVE));
  }

  // ---- 移动端抽屉 ----
  function renderMobileDrawer() {
    let drawer = $('#tbMobileDrawer');
    if (drawer) return drawer;
    drawer = ce('div', 'tb-mobile-drawer');
    drawer.id = 'tbMobileDrawer';
    drawer.innerHTML = `
      <div class="tb-mobile-drawer-mask" onclick="window.tbNavCloseDrawer()"></div>
      <div class="tb-mobile-drawer-panel">
        <div class="tb-mobile-drawer-head">
          <span class="tb-mobile-drawer-title">分类导航</span>
          <button class="tb-mobile-drawer-close" onclick="window.tbNavCloseDrawer()">✕</button>
        </div>
        <div class="tb-mobile-drawer-body"></div>
      </div>`;
    document.body.appendChild(drawer);
    window.tbNavCloseDrawer = () => toggleMobileDrawer(false);
    return drawer;
  }

  function toggleMobileDrawer(show) {
    const drawer = renderMobileDrawer();
    drawer.classList.toggle(CLS_OPEN, !!show);
    document.body.style.overflow = show ? 'hidden' : '';
  }

  function renderMobileBody() {
    const drawer = renderMobileDrawer();
    const body = drawer.querySelector('.tb-mobile-drawer-body');
    body.innerHTML = '';
    groups.forEach((g, i) => {
      const section = ce('div', 'tb-mobile-section');
      const head = ce('div', 'tb-mobile-section-head');
      head.innerHTML = `<span class="tb-mobile-section-icon">${g.icon}</span><span>${nOf(g)}</span><span class="tb-mobile-section-count">${g.count}</span>`;
      head.onclick = () => {
        section.classList.toggle(CLS_OPEN);
      };
      const list = ce('ul', 'tb-mobile-section-list');
      g.children.forEach(c => {
        const li = ce('li', 'tb-mobile-section-item');
        const a = ce('a');
        a.href = `/tools/${c.key}/index.html`;
        a.innerHTML = `<span class="tb-mobile-cat-icon">${c.icon}</span><span>${nOf(c)}</span><span class="tb-mobile-cat-count">${c.count}</span>`;
        li.appendChild(a);
        list.appendChild(li);
      });
      section.appendChild(head);
      section.appendChild(list);
      body.appendChild(section);
    });
  }

  // ---- 初始化：插入导航结构 ----
  async function init() {
    await loadGroups();
    if (!groups.length) return;

    // 在 body 最开头插入导航容器
    const topnav = ce('nav', 'tb-topnav');
    topnav.id = 'tbTopnav';
    const megapanel = ce('div', 'tb-megapanel');
    megapanel.id = 'tbMegapanel';

    // 已有 body 时插入到最前面
    const mount = () => {
      document.body.insertBefore(topnav, document.body.firstChild);
      document.body.insertBefore(megapanel, topnav.nextSibling);
      // 打标记：只有挂了新导航的页面才由 CSS 调整 body 顶部留白，
      // 避免影响未注入导航的静态页（guides / 404 等）
      document.body.classList.add('tb-has-topnav');
    };

    if (document.body) {
      mount();
    } else {
      document.addEventListener('DOMContentLoaded', mount);
    }

    renderTopNav(topnav);
    renderMegaPanel(megapanel);
    renderMobileBody();

    // 点击页面其他区域关闭面板
    document.addEventListener('click', e => {
      if (!e.target.closest('#tbTopnav') && !e.target.closest('#tbMegapanel')) {
        closeMegaPanel();
      }
    });

    // 语言切换后重渲染（中英文分类名/工具名来自同一份数据的不同字段）
    window.addEventListener('toolbox:langchange', () => {
      renderTopNav(topnav);
      renderMobileBody();
      // 面板若正展开，必须连内容一起重渲染，否则里面仍是切换前的语言
      const panel = $('#tbMegapanel');
      const wasOpen = panel && panel.classList.contains(CLS_OPEN);
      closeMegaPanel();
      if (wasOpen) showMegaPanel(activeGroupIndex);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
