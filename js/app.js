/* 全站行业字典（266 个行业：中文名 + emoji 图标）
   已抽到 js/industry-info.js（首页与工具页共用），由 scripts/gen_industry_info.py 生成。
   此处直接引用，保持旧代码 INDUSTRY_INFO 用法不变。 */
const INDUSTRY_INFO = (typeof window !== 'undefined' && window.INDUSTRY_INFO) || {};

const HOT_INDUSTRIES = ['it','design','biz','life','finance','health','edu','science','fun','marketing','travel','legal'];

const CAT_INFO = {
  dev:       { name: '开发工具', icon: '🔧' },
  encode:    { name: '编码解码', icon: '🔐' },
  text:      { name: '文本处理', icon: '📝' },
  generate:  { name: '生成器',   icon: '🎲' },
  convert:   { name: '格式转换', icon: '🔄' },
  math:      { name: '数学计算', icon: '🧮' },
  calculator:{ name: '通用计算器', icon: '🔢' },
  design:    { name: '设计工具', icon: '🎨' },
  image:     { name: '图片处理', icon: '🖼️' },
  validator: { name: '验证器',   icon: '✅' },
  reference: { name: '速查表',   icon: '📚' },
  game:      { name: '游戏趣味', icon: '🎮' },
  finance:   { name: '金融投资', icon: '💰' },
  health:    { name: '健康医疗', icon: '💪' },
  engineer:  { name: '工程计算', icon: '⚙️' },
};

const HOT_TOOLS = [
  { n: 'JSON 格式化',      en: 'JSON Formatter',      d: '格式化并高亮显示 JSON 数据',       ed: 'Format and highlight JSON data',       i: 'it',     c: 'dev',       u: 'tools/it/json-formatter.html', ic: '📋', b: '#e8f5e9' },
  { n: 'Base64 编解码',    en: 'Base64 Encode/Decode', d: '在线 Base64 编码和解码工具',        ed: 'Online Base64 encoder and decoder',    i: 'it',     c: 'encode',    u: 'tools/it/base64.html',         ic: '🔐', b: '#f3e5f5' },
  { n: '二维码生成',       en: 'QR Code Generator',   d: '快速生成二维码，支持多种格式',       ed: 'Generate QR codes quickly, multiple formats', i: 'it', c: 'generate', u: 'tools/it/qrcode-generator.html', ic: '📱', b: '#e3f2fd' },
  { n: '密码生成器',       en: 'Password Generator',  d: '生成高强度随机密码',                ed: 'Generate strong random passwords',        i: 'it',     c: 'generate',  u: 'tools/it/password-generator.html', ic: '🔐', b: '#fff3e0' },
  { n: 'Markdown 转 HTML', en: 'Markdown to HTML',    d: '手写解析器，支持语法高亮',          ed: 'Hand-written parser with syntax highlight', i: 'it', c: 'convert', u: 'tools/it/markdown-to-html.html', ic: '📝', b: '#e8eaf6' },
  { n: '时间戳转换',       en: 'Timestamp Converter', d: 'Unix 时间戳与日期互转',             ed: 'Convert between Unix timestamp and date', i: 'life',   c: 'convert',   u: 'tools/life/timestamp.html',    ic: '⏰', b: '#fce4ec' },
  { n: '单位换算',         en: 'Unit Converter',      d: '全面的单位转换器',                  ed: 'Comprehensive unit converter',            i: 'life',   c: 'convert',   u: 'tools/life/unit-converter.html', ic: '🔄', b: '#e0f7fa' },
  { n: 'BMI 计算器',       en: 'BMI Calculator',      d: '健康体重指数计算',                  ed: 'Body Mass Index calculator',              i: 'health', c: 'math',      u: 'tools/health/bmi-calculator.html', ic: '⚖️', b: '#ffebee' },
  { n: '颜色选择器',       en: 'Color Picker',        d: '专业的颜色工具',                    ed: 'Professional color tool',                 i: 'design', c: 'design',    u: 'tools/design/color-picker.html', ic: '🎨', b: '#f3e5f5' },
  { n: '正则表达式测试',   en: 'Regex Tester',        d: '在线测试正则表达式',                ed: 'Test regular expressions online',         i: 'it',     c: 'dev',       u: 'tools/it/regex.html',          ic: '🔍', b: '#e8f5e9' },
  { n: 'UUID 生成',        en: 'UUID Generator',      d: '生成各种格式的 UUID',               ed: 'Generate UUIDs in various formats',       i: 'it',     c: 'generate',  u: 'tools/it/uuid-v4-generator.html', ic: '🆔', b: '#fff8e1' },
  { n: '字数统计',         en: 'Word Counter',        d: '统计文本字数和字符数',              ed: 'Count words and characters in text',       i: 'finance',c: 'text',      u: 'tools/finance/word-counter.html', ic: '📊', b: '#e3f2fd' },
  { n: '文本去重',         en: 'Text Deduplicate',    d: '移除重复的行',                      ed: 'Remove duplicate lines',                   i: 'biz',    c: 'text',      u: 'tools/biz/text-dedup.html',    ic: '🔄', b: '#e8f5e9' },
  { n: '汇率换算',         en: 'Currency Converter',  d: '常用货币汇率换算',                  ed: 'Common currency exchange conversion',      i: 'finance',c: 'finance',   u: 'tools/finance/currency-converter.html', ic: '💱', b: '#fff3e0' },
  { n: '倒计时器',         en: 'Countdown Timer',     d: '在线倒计时工具',                    ed: 'Online countdown timer',                   i: 'it',     c: 'generate',  u: 'tools/it/stopwatch.html',      ic: '⏱️', b: '#fce4ec' },
  { n: '番茄钟',           en: 'Pomodoro Timer',      d: '专注工作计时器',                    ed: 'Focus work timer',                         i: 'edu',    c: 'generate',  u: 'tools/it/pomodoro.html',       ic: '🍅', b: '#e8f5e9' },
  { n: 'IP 计算器',        en: 'IP Calculator',       d: '子网掩码和 IP 地址计算',            ed: 'Subnet mask and IP address calculation',   i: 'it',     c: 'dev',       u: 'tools/it/ip-calculator.html',  ic: '🌐', b: '#e3f2fd' },
  { n: '哈希计算',         en: 'Hash Calculator',     d: 'MD5/SHA1/SHA256 等哈希值',          ed: 'MD5/SHA1/SHA256 and more hash values',      i: 'it',     c: 'encode',    u: 'tools/it/hash.html',           ic: '🔒', b: '#f3e5f5' },
  { n: 'HTML 转义',        en: 'HTML Escape',         d: 'HTML 字符转义工具',                 ed: 'HTML character escape tool',               i: 'it',     c: 'encode',    u: 'tools/it/html-escape.html',    ic: '<>', b: '#e8eaf6' },
  { n: '颜色转换',         en: 'Color Converter',     d: 'RGB/HEX/HSL 颜色互转',              ed: 'RGB/HEX/HSL color conversion',             i: 'it',     c: 'convert',   u: 'tools/it/color-converter.html', ic: '🎨', b: '#f3e5f5' },
];

// ===== i18n 辅助（B3-04 多语言）=====
// 仅在 I18n 引擎加载后翻译；未加载时回退中文原文，保证向后兼容
function _t(k, fb) { return (window.I18n && window.I18n.t) ? window.I18n.t(k, fb) : fb; }
function _ind(info, key) { return (window.I18n && window.I18n.indName) ? window.I18n.indName(info, key) : (info && info.name || ''); }
function _cat(info, key) { return (window.I18n && window.I18n.catName) ? window.I18n.catName(info, key) : (info && info.name || ''); }
// 热门工具网格：按当前语言取 en/ed，否则回退中文（批次2 i18n）
function _tn(t) { const en = (window.I18n && window.I18n.get && window.I18n.get() !== 'zh-CN'); return (en && t.en) ? t.en : (t.n || t.name || ''); }
function _td(t) { const en = (window.I18n && window.I18n.get && window.I18n.get() !== 'zh-CN'); return (en && t.ed) ? t.ed : (t.d || t.desc || ''); }

let currentView = 'home';
let currentIndustry = 'it';
let currentCategory = 'all';
let currentQuality = 'all'; // all | A | B | C，按质量等级筛选
let searchQuery = '';
let currentTools = HOT_TOOLS;
let allSearchIndex = null;
let loadedIndustries = {};
let favorites = JSON.parse(localStorage.getItem('favTools') || '[]');
let recents = JSON.parse(localStorage.getItem('recentTools') || '[]');
let searchIndexLoaded = false;
let previousView = 'hot';
let industriesExpanded = false;
let searchDebounceTimer = null;

// 语言切换后，重新渲染所有由 JS 注入的动态视图（行业/分类/质量标签 + 当前网格）
function refreshI18nViews() {
  if (window.I18n) window.I18n.apply(document);
  renderIndustries();
  renderBreadcrumbNav();
  renderCategoryTags();
  renderQualityTags();
  renderHotSpotlight();
  if (currentView === 'search') {
    if (typeof renderSearchResults === 'function') renderSearchResults();
  } else if (currentView === 'home') {
    renderExploreGuide();
  } else if (currentView === 'hot' || currentView === 'recent' || currentView === 'fav') {
    renderHotRecentFav();
  } else if (currentIndustry && currentView === currentIndustry) {
    loadIndustry(currentIndustry);
  } else {
    renderTools();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  renderBreadcrumbNav();
  renderHotSpotlight();
  renderCategoryTags();
  renderQualityTags();
  renderExploreGuide();
  const _th = document.getElementById('tabHot');
  if (_th) _th.classList.remove('active');
  setupScroll();
  setupKeyboard();
  updateCounts();
  window.addEventListener('toolbox:langchange', refreshI18nViews);
});

function initTheme() {
  let t = localStorage.getItem('theme');
  if (!t && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) t = 'dark';
  t = t || 'light';
  document.body.classList.toggle('dark', t === 'dark');
  document.documentElement.setAttribute('data-theme', t === 'dark' ? 'dark' : 'light');
  updateThemeIcons(t);
}

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark');
  const t = isDark ? 'dark' : 'light';
  localStorage.setItem('theme', t);
  document.documentElement.setAttribute('data-theme', t);
  updateThemeIcons(t);
}

function updateThemeIcons(t) {
  const icon = t === 'dark' ? '☀️' : '🌙';
  const d = document.getElementById('themeIconDesktop');
  const m = document.getElementById('themeIconMobile');
  if (d) d.textContent = icon;
  if (m) m.textContent = icon;
}

function renderIndustries() {
  const grid = document.getElementById('industryGrid');
  if (!grid) return;
  const industries = industriesExpanded ? Object.entries(INDUSTRY_INFO) : Object.entries(INDUSTRY_INFO).slice(0, 12);
  let html = '';
  for (const [key, info] of industries) {
    const count = (window.INDUSTRY_COUNTS && window.INDUSTRY_COUNTS[key]) || '';
    html += `<button onclick="selectIndustry('${key}')" class="industry-card" title="${_ind(info, key)}">
      <div class="industry-card-head">
        <span class="industry-icon">${info.icon}</span>
        <span class="industry-name">${_ind(info, key)}${count ? ` <small style="color:var(--muted);font-weight:400;font-size:12px">(${count})</small>` : ''}</span>
      </div>
    </button>`;
  }
  grid.innerHTML = html;
  const btn = document.getElementById('showMoreIndustries');
  if (btn) {
    btn.textContent = industriesExpanded ? _t('ind.collapse', '收起 ↑') : _t('ind.view_all', '查看全部 {n} 个行业 →').replace('{n}', Object.keys(INDUSTRY_INFO).length);
    btn.style.display = Object.keys(INDUSTRY_INFO).length > 12 ? '' : 'none';
  }
}

function showAllIndustries() {
  industriesExpanded = !industriesExpanded;
  renderIndustries();
}

let breadcrumbExpanded = false;

function renderBreadcrumbNav() {
  const track = document.getElementById('breadcrumbTrack');
  if (!track) return;
  const counts = window.INDUSTRY_COUNTS || {};
  const entries = Object.entries(INDUSTRY_INFO).map(([key, info]) => ({
    key, info, count: counts[key] || 0
  }));
  // 按工具数量降序排序，数量相同的按名称
  entries.sort((a, b) => b.count - a.count || a.info.name.localeCompare(b.info.name, 'zh'));
  const DEFAULT_VISIBLE = 16; // 4列 x 4行，分批展示
  const visibleEntries = breadcrumbExpanded ? entries : entries.slice(0, DEFAULT_VISIBLE);
  const hasMore = entries.length > DEFAULT_VISIBLE;

  let html = `<a href="index.html" class="breadcrumb-item all"><span class="bc-icon">🏠</span><span>${_t('tabbar.home', '首页')}</span></a>`;
  for (const { key, info, count } of visibleEntries) {
    const hot = count >= 100 ? ' hot' : '';
    const name = _ind(info, key);
    html += `<a href="tools/${key}/index.html" class="breadcrumb-item${hot}" title="${name}">
      <span class="bc-icon">${info.icon}</span>
      <span>${name}</span>
      ${count ? `<span class="bc-count">${count}</span>` : ''}
    </a>`;
  }
  if (hasMore) {
    html += `<div class="breadcrumb-item-all-wrap">
      <button class="breadcrumb-toggle-btn ${breadcrumbExpanded ? 'expanded' : ''}" onclick="toggleBreadcrumbNav()">
        ${breadcrumbExpanded
          ? _t('breadcrumb.collapse', '收起分类')
          : _t('breadcrumb.expand', '展开全部 {n} 个分类').replace('{n}', entries.length)}
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
    </div>`;
  }
  track.innerHTML = html;
}

function toggleBreadcrumbNav() {
  breadcrumbExpanded = !breadcrumbExpanded;
  renderBreadcrumbNav();
}

function renderHotSpotlight() {
  const grid = document.getElementById('hotSpotlightGrid');
  if (!grid) return;
  grid.innerHTML = HOT_TOOLS.slice(0, 8).map(t => {
    const url = t.u || t.url;
    return `<a class="hot-spotlight-card" href="${url}" target="_blank" rel="noopener" onclick="addToRecent('${url}')">
      <div class="hot-spotlight-icon" style="background:${t.b || t.bg || '#f5f5f5'}">${t.ic || t.icon || '🔧'}</div>
      <div class="hot-spotlight-info">
        <div class="hot-spotlight-name">${_tn(t)}</div>
        <div class="hot-spotlight-desc">${_td(t)}</div>
      </div>
    </a>`;
  }).join('');
}

function renderCategoryTags() {
  const container = document.getElementById('categoryTags');
  if (!container) return;
  let html = `<button class="cat-tag active" data-cat="all" aria-pressed="true" onclick="selectCategory('all')">${_t('common.all', '全部')}</button>`;
  for (const [key, info] of Object.entries(CAT_INFO)) {
    html += `<button class="cat-tag" data-cat="${key}" aria-pressed="false" onclick="selectCategory('${key}')">${info.icon} ${_cat(info, key)}</button>`;
  }
  container.innerHTML = html;
}

function selectCategory(cat) {
  currentCategory = cat;
  document.querySelectorAll('.cat-tag').forEach(el => {
    const isActive = el.dataset.cat === cat;
    el.classList.toggle('active', isActive);
    el.setAttribute('aria-pressed', isActive ? 'true' : 'false');
  });
  if (currentView === 'search') {
    renderSearchResults();
  } else if (currentView === 'home') {
    if (cat === 'all') {
      renderExploreGuide();
    } else {
      ensureSearchIndexLoaded().then(() => renderCategoryBrowse(cat));
    }
  } else if (currentView === 'hot' || currentView === 'recent' || currentView === 'fav') {
    ensureSearchIndexLoaded().then(() => renderHotRecentFav());
  } else {
    renderTools();
  }
  scrollToTools();
}

function renderHotToolsSSR() {
  const grid = document.getElementById('toolsGrid');
  if (grid) grid.innerHTML = renderToolCards(HOT_TOOLS);
}

function setGridMode(mode) {
  const grid = document.getElementById('toolsGrid');
  const countEl = document.getElementById('resultCount');
  if (grid) grid.className = mode === 'guide' ? '' : 'tools-grid';
  if (countEl) countEl.style.display = mode === 'guide' ? 'none' : '';
}

function renderExploreGuide() {
  setGridMode('guide');
  const grid = document.getElementById('toolsGrid');
  if (!grid) return;
  const counts = window.INDUSTRY_COUNTS || {};
  const top = Object.entries(INDUSTRY_INFO)
    .map(([k, v]) => ({ k, ...v, count: counts[k] || 0 }))
    .filter(x => x.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);
  const chips = top.map(x =>
    `<a class="guide-chip" href="tools/${x.k}/index.html"><span class="gc-icon">${x.icon}</span><span class="gc-name">${_ind(x, x.k)}</span><span class="gc-count">${x.count}</span></a>`
  ).join('');
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = _t('explore.title', '🧭 探索工具');
  grid.innerHTML = `<div class="explore-guide">
    <div class="explore-guide-head">
      <div class="explore-guide-emoji">🧭</div>
      <div class="explore-guide-text">
        <div class="explore-guide-title">${_t('explore.subtitle', '开始探索 5000+ 在线工具')}</div>
        <div class="explore-guide-sub">${_t('explore.hint', '选择上方「功能分类」或「分类导航」，也可直接搜索 · 纯前端处理，数据不上传')}</div>
      </div>
    </div>
    <div class="explore-guide-label">🔥 ${_t('explore.hot', '热门行业直达')}</div>
    <div class="explore-guide-tags">${chips}</div>
  </div>`;
}

function renderCategoryBrowse(cat) {
  setGridMode('grid');
  const info = CAT_INFO[cat] || { name: cat, icon: '📁' };
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = `${info.icon} ${_cat(info, cat)}`;
  let tools = (allSearchIndex || []).filter(t => t.c === cat)
    .map(t => ({ n: t.n, d: t.d, i: t.i, c: t.c, u: t.u, ic: t.ic, b: t.b, q: t.q, en: t.en, ed: t.ed }));
  tools = applyQuality(tools);
  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${tools.length} ${_t('cat.suffix_tools', '个工具')}`;
  const grid = document.getElementById('toolsGrid');
  if (!grid) return;
  if (tools.length === 0) {
    grid.innerHTML = `<div class="loading">📁<br>${_t('cat.empty', '该分类暂无工具')}</div>`;
  } else {
    grid.innerHTML = renderToolCards(tools);
  }
}

function goHome() {
  currentView = 'home';
  currentCategory = 'all';
  searchQuery = '';
  const di = document.getElementById('searchInputDesktop');
  const mi = document.getElementById('searchInputMobile');
  if (di) di.value = '';
  if (mi) mi.value = '';
  renderExploreGuide();
  updateCatTagsAll();
  updateQuickTabs('home');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function selectIndustry(ind) {
  currentView = ind;
  currentIndustry = ind;
  clearSearch();
  loadIndustry(ind);
}

async function loadIndustry(ind) {
  currentIndustry = ind;
  currentView = ind;
  updateQuickTabs('tabBarGrid');
  const info = INDUSTRY_INFO[ind];
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = `${info.icon} ${_ind(info, ind)}`;

  setGridMode('grid');
  const grid = document.getElementById('toolsGrid');
  if (grid) grid.innerHTML = `<div class="loading">${_t('common.loading', '⏳ 加载中...')}</div>`;

  if (loadedIndustries[ind]) {
    currentTools = loadedIndustries[ind];
    renderTools();
  } else {
    try {
      const res = await fetch(`json/industry-${ind}.json`);
      const tools = await res.json();
      loadedIndustries[ind] = tools;
      currentTools = tools;
      renderTools();
    } catch (e) {
      if (grid) grid.innerHTML = `<div class="loading" style="color:#ef4444">${_t('state.load_fail', '❌ 加载失败，请刷新重试')}</div>`;
    }
  }
  currentCategory = 'all';
  updateCatTagsAll();
  setTimeout(() => {
    const s = document.getElementById('toolsSection');
    if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
}

function updateCatTagsAll(cat = 'all') {
  document.querySelectorAll('.cat-tag').forEach(el => {
    const isActive = el.dataset.cat === cat;
    el.classList.toggle('active', isActive);
    el.setAttribute('aria-pressed', isActive ? 'true' : 'false');
  });
}

function updateQuickTabs(activeId) {
  const active = (() => {
    if (!activeId) return null;
    if (activeId === 'home' || activeId === 'tabBarHome') return 'tabBarHome';
    if (activeId === 'grid' || activeId === 'tabBarGrid') return 'tabBarGrid';
    if (activeId === 'hot' || activeId === 'tabHot' || activeId === 'tabBarHot') return 'tabBarHot';
    if (activeId === 'recent' || activeId === 'tabRecent') return null;
    if (activeId === 'fav' || activeId === 'tabFav' || activeId === 'tabBarFav') return 'tabBarFav';
    return null;
  })();
  const topActive = (() => {
    if (!activeId) return null;
    if (activeId === 'hot' || activeId === 'tabHot') return 'tabHot';
    if (activeId === 'recent' || activeId === 'tabRecent') return 'tabRecent';
    if (activeId === 'fav' || activeId === 'tabFav') return 'tabFav';
    if (activeId === 'tabBarHot' || activeId === 'tabBarGrid' || activeId === 'tabBarHome' || activeId === 'tabBarFav') return null;
    return null;
  })();

  ['tabHot', 'tabRecent', 'tabFav'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    const isActive = id === topActive;
    el.classList.toggle('active', isActive);
    el.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    el.setAttribute('aria-current', isActive ? 'page' : 'false');
  });
  ['tabBarHome','tabBarGrid','tabBarHot','tabBarFav'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('active');
    el.setAttribute('aria-current', 'false');
    el.setAttribute('aria-pressed', 'false');
  });
  const tabBarId = active;
  if (tabBarId) {
    const bar = document.getElementById(tabBarId);
    if (bar) {
      bar.classList.add('active');
      bar.setAttribute('aria-current', 'page');
      bar.setAttribute('aria-pressed', 'true');
    }
  }
}

function showHotTools() {
  currentView = 'hot';
  currentCategory = 'all';
  clearSearch();
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = _t('tab.hot', '🔥 热门工具');
  updateQuickTabs('tabHot');
  updateCatTagsAll();
  currentTools = HOT_TOOLS;
  renderHotRecentFav();
  scrollToTools();
}

function showRecentTools() {
  currentView = 'recent';
  clearSearch();
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = _t('tab.recent', '🕐 最近使用');
  updateQuickTabs('tabRecent');
  updateCatTagsAll();
  ensureSearchIndexLoaded().then(() => renderHotRecentFav());
  scrollToTools();
}

function showFavTools() {
  currentView = 'fav';
  clearSearch();
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = _t('tab.fav', '❤️ 我的收藏');
  updateQuickTabs('tabFav');
  updateCatTagsAll();
  ensureSearchIndexLoaded().then(() => renderHotRecentFav());
  scrollToTools();
}

function showAllTools() {
  goHome();
  updateQuickTabs('home');
}

function showIndustries() {
  const s = document.getElementById('breadcrumbNav');
  if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' });
  updateQuickTabs('tabBarGrid');
}

function scrollToTools() {
  setTimeout(() => {
    const s = document.getElementById('toolsSection');
    if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
}

/* ---------- 工具质量分级（A 专业 / B 标准 / C 轻量） ---------- */
const QUALITY_INFO = {
  A: { label: '专业', icon: '💎', color: '#7C3AED', desc: '含公式说明、图表或多参数计算' },
  B: { label: '标准', icon: '🔹', color: '#3B82F6', desc: '具备完整交互与计算逻辑' },
  C: { label: '轻量', icon: '📄', color: '#9CA3AF', desc: '速查/参考类轻量页面' }
};

// 兼容两种数据源：search-index 用 q，industry-*.json 用 quality
function qOf(t) { return t.q || t.quality || 'B'; }

// 按当前质量筛选，并让 A 级工具优先展示
function applyQuality(tools) {
  if (currentQuality !== 'all') {
    return tools.filter(t => qOf(t) === currentQuality);
  }
  const rank = { A: 0, B: 1, C: 2 };
  return tools
    .map((t, i) => ({ t, i }))
    .sort((a, b) => (rank[qOf(a.t)] ?? 1) - (rank[qOf(b.t)] ?? 1) || a.i - b.i)
    .map(x => x.t);
}

function renderQualityTags() {
  const box = document.getElementById('qualityTags');
  if (!box) return;
  let html = `<span class="q-tag-label">${_t('quality.label', '质量')}</span>`;
  html += `<button class="q-tag active" data-q="all" aria-pressed="true" onclick="selectQuality('all')">${_t('common.all', '全部')}</button>`;
  for (const [key, info] of Object.entries(QUALITY_INFO)) {
    html += `<button class="q-tag" data-q="${key}" aria-pressed="false" title="${_t('quality.' + key + '.desc', info.desc)}" onclick="selectQuality('${key}')">${info.icon} ${_t('quality.' + key, info.label)}</button>`;
  }
  box.innerHTML = html;
}

function selectQuality(q) {
  currentQuality = q;
  document.querySelectorAll('.q-tag').forEach(el => {
    const isActive = el.dataset.q === q;
    el.classList.toggle('active', isActive);
    el.setAttribute('aria-pressed', isActive ? 'true' : 'false');
  });
  if (currentView === 'search') {
    renderSearchResults();
  } else if (currentView === 'home') {
    if (currentCategory === 'all') {
      // 首页引导态：切换质量时展示对应等级的工具列表
      if (q === 'all') { renderExploreGuide(); }
      else { ensureSearchIndexLoaded().then(() => renderQualityBrowse(q)); }
    } else {
      ensureSearchIndexLoaded().then(() => renderCategoryBrowse(currentCategory));
    }
  } else if (currentView === 'hot' || currentView === 'recent' || currentView === 'fav') {
    ensureSearchIndexLoaded().then(() => renderHotRecentFav());
  } else if (currentIndustry && currentView === currentIndustry) {
    renderTools();
  } else {
    renderTools();
  }
}

function renderQualityBrowse(q) {
  setGridMode('grid');
  const info = QUALITY_INFO[q] || { label: q, icon: '🏅', desc: '' };
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = `${info.icon} ${_t('quality.' + q, info.label + '级工具')}`;
  let tools = (allSearchIndex || []).filter(t => qOf(t) === q)
    .map(t => ({ n: t.n, d: t.d, i: t.i, c: t.c, u: t.u, ic: t.ic, b: t.b, q: t.q, en: t.en, ed: t.ed }));
  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${tools.length} ${_t('cat.suffix_tools', '个工具')}`;
  const grid = document.getElementById('toolsGrid');
  if (!grid) return;
  grid.innerHTML = tools.length
    ? renderToolCards(tools.slice(0, 600))
    : `<div class="loading">🏅<br>${_t('quality.empty', '该等级暂无工具')}</div>`;
}

function renderTools() {
  let tools = currentTools;
  if (currentCategory !== 'all') {
    tools = tools.filter(t => (t.c || t.cat) === currentCategory);
  }
  tools = applyQuality(tools);
  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${tools.length} ${_t('cat.suffix_tools', '个工具')}`;
  const grid = document.getElementById('toolsGrid');
  if (grid) grid.innerHTML = renderToolCards(tools);
}

function renderHotRecentFav() {
  setGridMode('grid');
  let tools = [];
  if (currentView === 'hot') {
    // 功能分类筛选时从全量数据中筛选，否则显示热门工具
    if (currentCategory !== 'all' && allSearchIndex) {
      tools = allSearchIndex.map(t => ({ n: t.n, d: t.d, i: t.i, c: t.c, u: t.u, ic: t.ic, b: t.b, q: t.q, en: t.en, ed: t.ed }))
        .filter(t => t.c === currentCategory);
      const titleEl = document.getElementById('toolsGridTitle');
      if (titleEl) {
        const catName = CAT_INFO[currentCategory] ? CAT_INFO[currentCategory].name : currentCategory;
        titleEl.textContent = `${CAT_INFO[currentCategory] ? CAT_INFO[currentCategory].icon : '📁'} ${catName} - ${_t('tab.all', '全部工具')}`;
      }
    } else {
      tools = HOT_TOOLS;
      const titleEl = document.getElementById('toolsGridTitle');
      if (titleEl) titleEl.textContent = _t('tab.hot', '🔥 热门工具');
    }
  } else if (currentView === 'recent') {
    tools = recents.map(url => {
      if (allSearchIndex) {
        const t = allSearchIndex.find(item => item.u === url);
        if (t) return { n: t.n, d: t.d, i: t.i, c: t.c, u: t.u, ic: t.ic, b: t.b, q: t.q, en: t.en, ed: t.ed };
      }
      const hot = HOT_TOOLS.find(h => h.u === url);
      if (hot) return hot;
      return null;
    }).filter(Boolean);
  } else if (currentView === 'fav') {
    tools = favorites.map(url => {
      if (allSearchIndex) {
        const t = allSearchIndex.find(item => item.u === url);
        if (t) return { n: t.n, d: t.d, i: t.i, c: t.c, u: t.u, ic: t.ic, b: t.b, q: t.q, en: t.en, ed: t.ed };
      }
      const hot = HOT_TOOLS.find(h => h.u === url);
      if (hot) return hot;
      return null;
    }).filter(Boolean);
  }
  if (currentCategory !== 'all' && currentView !== 'hot') {
    tools = tools.filter(t => (t.c || t.cat) === currentCategory);
  }
  if (currentQuality !== 'all') tools = tools.filter(t => qOf(t) === currentQuality);
  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${tools.length} ${_t('cat.suffix_tools', '个工具')}`;
  const grid = document.getElementById('toolsGrid');
  if (!grid) return;
  if (tools.length === 0) {
    const emptyText = currentView === 'recent' ? _t('view.empty_recent', '暂无最近使用记录') : currentView === 'fav' ? _t('view.empty_fav', '暂无收藏工具') : _t('view.empty', '暂无数据');
    grid.innerHTML = `<div class="loading">${currentView === 'recent' ? '🕐' : currentView === 'fav' ? '❤️' : '🔥'}<br>${emptyText}</div>`;
    return;
  }
  grid.innerHTML = renderToolCards(tools);
}

function renderToolCards(tools) {
  const favSet = new Set(favorites);
  return tools.map((t, i) => {
    const icon = t.ic || t.icon || '🔧';
    const bg = t.b || t.bg || '#f5f5f5';
    const url = t.u || t.url;
    const name = _tn(t);
    const desc = _td(t);
    const isFav = favSet.has(url);
    const qc = t.q || t.quality;
    const qi = qc && QUALITY_INFO[qc] ? QUALITY_INFO[qc] : null;
    const qBadge = qi && qc !== 'B'
      ? `<span class="tool-q q-${qc}" title="${_t('quality.' + qc + '.desc', qi.desc)}">${qi.icon} ${_t('quality.' + qc, qi.label)}</span>`
      : '';
    return `<a class="tool-card" href="${url}" target="_blank" rel="noopener" onclick="addToRecent('${url}')">
      <div class="tool-card-head">
        <div class="tool-icon">${icon}</div>
        <button class="tool-fav ${isFav ? 'active' : ''}" onclick="event.preventDefault();event.stopPropagation();toggleFav('${url}')">${isFav ? '⭐' : '☆'}</button>
      </div>
      <div class="tool-name">${name}${qBadge}</div>
      <div class="tool-desc">${desc}</div>
    </a>`;
  }).join('');
}

function toggleFav(url) {
  const idx = favorites.indexOf(url);
  if (idx > -1) favorites.splice(idx, 1);
  else favorites.push(url);
  localStorage.setItem('favTools', JSON.stringify(favorites));
  if (currentView === 'hot' || currentView === 'recent' || currentView === 'fav') {
    renderHotRecentFav();
  } else {
    renderTools();
  }
}

function addToRecent(url) {
  recents = recents.filter(u => u !== url);
  recents.unshift(url);
  if (recents.length > 50) recents = recents.slice(0, 50);
  localStorage.setItem('recentTools', JSON.stringify(recents));
}

function updateCounts() {}

async function ensureSearchIndexLoaded() {
  if (allSearchIndex) return allSearchIndex;
  try {
    const res = await fetch('json/search-index.json');
    allSearchIndex = await res.json();
    searchIndexLoaded = true;
    return allSearchIndex;
  } catch (e) {
    console.error('Failed to load search index:', e);
    return [];
  }
}

function onSearchInput(e, isMobile) {
  const input = e.target;
  const query = input.value.trim();
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => performSearch(query, isMobile), 150);
}

function onSearchKey(e, isMobile) {
  if (e.key === 'Enter') {
    e.preventDefault();
    const query = e.target.value.trim();
    performSearch(query, isMobile);
    if (isMobile) closeMobileSearch();
    else e.target.blur();
  } else if (e.key === 'Escape') {
    clearSearch();
    if (isMobile) closeMobileSearch();
  }
}

async function performSearch(query, isMobile) {
  searchQuery = query.toLowerCase();
  if (!searchQuery) {
    clearSearch();
    return;
  }
  previousView = currentView !== 'search' ? currentView : previousView;
  currentView = 'search';
  const titleEl = document.getElementById('toolsGridTitle');
  if (titleEl) titleEl.textContent = _t('search.results', '🔍 搜索结果');
  await ensureSearchIndexLoaded();
  renderSearchResults();
  if (isMobile) renderMobileSearchResults();
  if (!isMobile) scrollToToolsHeader();
}

function scrollToToolsHeader() {
  const header = document.querySelector('.tools-header');
  if (!header) return;
  const navHeight = window.innerWidth < 768 ? 56 : 72;
  const rect = header.getBoundingClientRect();
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const targetY = scrollTop + rect.top - navHeight - 12;
  window.scrollTo({ top: targetY, behavior: 'smooth' });
}

function clearSearch() {
  const di = document.getElementById('searchInputDesktop');
  const mi = document.getElementById('searchInputMobile');
  if (di) di.value = '';
  if (mi) mi.value = '';
  searchQuery = '';
  if (currentView === 'search') {
    if (previousView === 'home') renderExploreGuide();
    else if (previousView === 'hot') showHotTools();
    else if (previousView === 'recent') showRecentTools();
    else if (previousView === 'fav') showFavTools();
    else selectIndustry(previousView);
  }
}

function renderSearchResults() {
  setGridMode('grid');
  if (!allSearchIndex || !searchQuery) { renderTools(); return; }
  const q = searchQuery;
  let tools = toolboxSearch(q, 300).map(t => ({ n: t.n, d: t.d, i: t.i, c: t.c, u: t.u, ic: t.ic, b: t.b, q: t.q, en: t.en, ed: t.ed }));
  if (currentCategory !== 'all') tools = tools.filter(t => t.c === currentCategory);
  if (currentQuality !== 'all') tools = tools.filter(t => qOf(t) === currentQuality);
  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${tools.length} ${_t('cat.suffix_tools', '个工具')}`;
  const grid = document.getElementById('toolsGrid');
  if (grid) {
    if (tools.length === 0) {
      const sug = fuzzySuggest(q, 8);
      const sugHtml = sug.length
        ? '<div style="margin-top:14px;display:flex;flex-wrap:wrap;gap:8px;justify-content:center">' +
          sug.map(t => `<a href="${t.u}" style="padding:6px 12px;border:1px solid var(--border);border-radius:999px;text-decoration:none;color:var(--text)">${escapeHtml(_tn(t))}</a>`).join('') +
          '</div>'
        : '';
      grid.innerHTML = `<div class="loading">🔍<br>${_t('search.no_match', '没有找到匹配的工具')}<br><small style="color:var(--muted)">${_t('search.no_match_hint', '试试其他关键词，或看看这些相关工具：')}</small>` + sugHtml + '</div>';
    } else {
      grid.innerHTML = renderToolCards(tools);
    }
  }
}

function renderMobileSearchResults() {
  const container = document.getElementById('mobileSearchResults');
  if (!container) return;
  if (!searchQuery) {
    container.innerHTML = `<div style="text-align:center;padding:48px 0;color:var(--muted)">${_t('search.placeholder_hint', '输入关键词开始搜索')}</div>`;
    return;
  }
  const q = searchQuery;
  let tools = toolboxSearch(q, 30).map(t => ({ n: t.n, d: t.d, u: t.u, ic: t.ic, en: t.en, ed: t.ed }));
  if (tools.length === 0) {
    const sug = fuzzySuggest(q, 6);
    const sugHtml = sug.length
      ? sug.map(t => `
    <a href="${t.u}" class="mobile-search-item" onclick="addToRecent('${t.u}');closeMobileSearch()">
      <div class="mobile-search-item-head">
        <div class="mobile-search-icon">${t.ic || '🔧'}</div>
        <div style="flex:1;min-width:0">
          <div class="mobile-search-name">${escapeHtml(_tn(t))}</div>
          <div class="mobile-search-desc">${_t('search.related', '相关推荐')}</div>
        </div>
      </div>
    </a>`).join('')
      : '';
    container.innerHTML = `<div style="text-align:center;padding:32px 0;color:var(--muted)">${_t('search.no_match', '未找到相关工具')}<br><small>${_t('search.no_match_hint', '试试这些相关工具：')}</small></div>` + sugHtml;
    return;
  }
  container.innerHTML = tools.map(t => `
    <a href="${t.u}" class="mobile-search-item" onclick="addToRecent('${t.u}');closeMobileSearch()">
      <div class="mobile-search-item-head">
        <div class="mobile-search-icon">${t.ic || '🔧'}</div>
        <div style="flex:1;min-width:0">
          <div class="mobile-search-name">${_tn(t)}</div>
          <div class="mobile-search-desc">${_td(t) || ''}</div>
        </div>
      </div>
    </a>
  `).join('');
}

function openMobileSearch() {
  const modal = document.getElementById('mobileSearchModal');
  if (modal) {
    modal.style.display = 'block';
    setTimeout(() => {
      modal.classList.add('open');
      setTimeout(() => { const i = document.getElementById('searchInputMobile'); if (i) i.focus(); }, 300);
    }, 10);
  }
}

function closeMobileSearch() {
  const modal = document.getElementById('mobileSearchModal');
  if (modal) {
    modal.classList.remove('open');
    setTimeout(() => { modal.style.display = 'none'; }, 300);
  }
}

function setupScroll() {
  window.addEventListener('scroll', () => {
    const btn = document.getElementById('jumpTop');
    if (btn) {
      if (window.scrollY > 300) btn.classList.add('show');
      else btn.classList.remove('show');
    }
  }, { passive: true });
}

function setupKeyboard() {
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) {
      e.preventDefault();
      if (window.innerWidth >= 768) {
        const d = document.getElementById('searchInputDesktop');
        if (d) d.focus();
      } else {
        openMobileSearch();
      }
    }
    // Ctrl+K / Cmd+K 唤起全局命令面板搜索
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      cmdkToggle();
    }
  });
  // 平台检测：Mac 显示 ⌘K，其他显示 Ctrl K
  const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform) || /Mac/.test(navigator.userAgent);
  const kbd = document.getElementById('navSearchKbd');
  if (kbd) kbd.textContent = isMac ? '⌘K' : 'Ctrl K';
}

/* ===================== Ctrl+K 命令面板搜索 ===================== */
let cmdkFuse = null;
let cmdkResults = [];
let cmdkActive = 0;
let cmdkOpened = false;

function cmdkInitFuse() {
  if (cmdkFuse || !allSearchIndex) return;
  cmdkFuse = new Fuse(allSearchIndex, {
    keys: [
      { name: 'n', weight: 0.42 },
      { name: 's', weight: 0.28 },
      { name: 'al', weight: 0.30 },
      { name: 'py', weight: 0.15 },
      { name: 'pyi', weight: 0.15 },
      { name: 'd', weight: 0.13 },
      { name: 'i', weight: 0.05 },
      { name: 'c', weight: 0.05 },
    ],
    threshold: 0.38,
    ignoreLocation: true,
    minMatchCharLength: 1,
    includeMatches: true,
    includeScore: true,
  });
}

// B5-01: fuzzy "did you mean" suggestions for empty-result searches.
function fuzzySuggest(q, limit) {
  if (!allSearchIndex) return [];
  const qn = (q || '').trim().toLowerCase().replace(/\s+/g, '');
  // 无效查询（连续重复/单种类字符）不给建议，避免噪声；长度过短也不建议
  if (qn.length < 2 || /(.)\1\1/.test(qn) || new Set(qn.split('')).size < 2) return [];
  cmdkInitFuse();
  if (!cmdkFuse) return [];
  const res = cmdkFuse.search(qn, { limit: limit || 8 });
  // 只取高质量相似，过滤 Fuse 宽松配置产生的低相似噪声
  return res.filter(r => (r.score || 1) <= 0.3).map(r => r.item);
}

// B5-01: hybrid search ranker. Exact/prefix/contains/pinyin/alias matches are
// scored deterministically (guaranteeing exact-name-first), and Fuse fuzzy
// fills in typos / obscure pinyin that have no direct substring hit.
function toolboxScore(t, q) {
  const name = (t.n || '').toLowerCase();
  const slug = (t.s || '').toLowerCase();
  const aliasArr = (t.al || []).map(a => String(a).toLowerCase());
  const py = (t.py || '').toLowerCase();
  const pyi = (t.pyi || '').toLowerCase();
  const qn = q.replace(/\s+/g, '');
  // 无效查询（连续重复字符如 zzz、或单一种类字符）直接判负。否则拼音首字母
  // 失真（pyi 把 zh-zh-zh 压成 zzz）会让 zzz 误命中一堆不相关工具。
  if (/(.)\1\1/.test(qn) || new Set(qn.split('')).size < 2) return -1;
  // 拉丁短词（≤3 字符的拼音/英文）极易在长拼音串里子串误命中，降级为
  // 精确/前缀/token 级匹配，禁止任意子串包含；中文短词保持正常子串匹配。
  const latinShort = /^[a-z0-9]+$/.test(q) && q.length <= 3;
  if (name === q) return 1000;
  if (name.startsWith(q)) return 920 - name.length;
  if (!latinShort && name.indexOf(q) >= 0) return 820 - name.indexOf(q);
  if (pyi && pyi === q) return 660;
  if (pyi && pyi.startsWith(q) && q.length >= 2) return 640 - q.length;
  if (!latinShort && py && py.indexOf(q) >= 0) return 600 - py.indexOf(q) * 0.5;
  if (!latinShort && pyi && pyi.indexOf(q) >= 0) return 580 - pyi.indexOf(q) * 0.5;
  if (!latinShort && slug.indexOf(q) >= 0) return 560 - slug.indexOf(q) * 0.5;
  if (aliasArr.indexOf(q) >= 0) return 520;
  if (latinShort) {
    const toks = (s) => (s || '').split(/[^a-z0-9]+/i).filter(Boolean);
    if (aliasArr.some(a => a.startsWith(q))) return 515;
    if (toks(pyi).some(tok => tok === q || tok.startsWith(q))) return 510;
    if (toks(py).some(tok => tok === q || tok.startsWith(q))) return 505;
  }
  return -1;
}

// Split a query into one or more AND-term sets. A single token that mixes CJK
// and latin/digit runs (e.g. "格式化json") is also segmented into
// ["格式化","json"] so multi-concept queries typed without spaces still match
// (closes P1-02 验收: "格式化json" -> "JSON 格式化").
function segmentQuery(raw) {
  const spaceTerms = raw.split(/\s+/).filter(Boolean);
  if (spaceTerms.length > 1) return [spaceTerms];
  const token = spaceTerms[0] || '';
  const seg = (token.match(/[一-鿿]+|[a-z0-9]+/gi) || []).filter(Boolean);
  if (seg.length > 1) return [[token], seg];
  return [[token]];
}

function toolboxSearch(query, limit) {
  let q = (query || '').toLowerCase().trim();
  if (!q || !allSearchIndex) return [];
  // pinyin spaces are not part of the continuous py/pyi fields; strip them
  // before matching so "ji suan qi" behaves like "jisuanqi".
  const qNoSpace = q.replace(/\s+/g, '');
  const termSets = segmentQuery(q);
  const singleWhole = (t) => toolboxScore(t, q) >= 0 || (qNoSpace !== q && toolboxScore(t, qNoSpace) >= 0);
  const matchesSet = (t, set) => set.every(term => toolboxScore(t, term) >= 0);
  const scoreSet = (t, set) => set.reduce((s, term) => s + Math.max(toolboxScore(t, term), 0), 0);
  const pass = (t) => termSets.some(set => set.length === 1 ? singleWhole(t) : matchesSet(t, set));
  const scoreOf = (t) => Math.max(...termSets.map(set =>
    set.length === 1
      ? Math.max(toolboxScore(t, set[0]), qNoSpace !== set[0] ? toolboxScore(t, qNoSpace) : -1)
      : scoreSet(t, set)));
  const direct = allSearchIndex
    .filter(pass)
    .sort((a, b) => scoreOf(b) - scoreOf(a));
  // Typo correction (P3-3): when direct hits are scarce and the query is
  // latin-only (pinyin/english), scan pinyin fields with a sliding-window
  // edit distance (<=2). py/pyi include the description, so a whole-string
  // distance would always fail; the window search finds the best local match
  // (e.g. "jisqanqi" -> "jisuanqi" inside "fangdaijisuanqi...").
  let corrected = [];
  // 滑动窗口纠错门槛：仅对 ≥4 字符、无连续重复、字符种类≥3 的拉丁查询启用，
  // 避免 zzz/aaaa 这类无效词在 py 字段里捞回一堆不相关工具的“伪纠错”。
  if (direct.length < 3 && /^[a-z]+$/.test(qNoSpace) && qNoSpace.length >= 4 && !/(.)\1\1/.test(qNoSpace) && new Set(qNoSpace.split('')).size >= 3) {
    corrected = allSearchIndex
      .map(t => {
        const py = (t.py || '').toLowerCase();
        const pyi = (t.pyi || '').toLowerCase();
        let best = -1;
        if (py) {
          const d = windowEditDistance(py, qNoSpace, 1);
          if (d >= 0) best = Math.max(best, d);
        }
        if (pyi) {
          const d = windowEditDistance(pyi, qNoSpace, 1);
          if (d >= 0) best = Math.max(best, d);
        }
        return best >= 0 ? { t: t, s: 480 - best * 40 } : null;
      })
      .filter(x => x && !direct.some(d => d.u === x.t.u))
      .sort((a, b) => b.s - a.s)
      .slice(0, 8)
      .map(x => x.t);
  }
  cmdkInitFuse();
  let fuzzy = [];
  // 仅长查询（≥4 字符）用 Fuse 做高质量补充，并对结果严格按 score 过滤。
  // 否则宽松的 Fuse 配置（minMatchCharLength:1）会让 zzz/qwe/abc 等短字母词
  // 返回海量低相似噪声，表现为“无效关键词返回一堆结果”。
  if (q.length >= 4) {
    const fz = cmdkFuse ? cmdkFuse.search(q, { limit: 300 }) : [];
    const seen = new Set(direct.map(t => t.u).concat(corrected.map(t => t.u)));
    fuzzy = fz
      .filter(r => !seen.has(r.item.u) && (r.score || 1) <= 0.3)
      .map(r => r.item);
  }
  return direct.concat(corrected, fuzzy).slice(0, limit || 20);
}

function levenshtein(a, b) {
  if (a === b) return 0;
  const m = a.length, n = b.length;
  if (!m) return n;
  if (!n) return m;
  let prev = new Array(n + 1);
  let cur = new Array(n + 1);
  for (let j = 0; j <= n; j++) prev[j] = j;
  for (let i = 1; i <= m; i++) {
    cur[0] = i;
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
    }
    const tmp = prev; prev = cur; cur = tmp;
  }
  return prev[n];
}

// Sliding-window edit distance: finds the best substring window of `text`
// within edit distance `maxD` of `q`. Returns the distance (>=0) or -1.
// Windows of length len(q)+{-1,0,1} cover one-char insertions/deletions.
function windowEditDistance(text, q, maxD) {
  const tl = text.length, ql = q.length;
  if (tl < ql - 1) return -1;
  let best = maxD + 1;
  for (let wl = ql - 1; wl <= ql + 1; wl++) {
    if (wl < 1) continue;
    for (let s = 0; s + wl <= tl; s++) {
      const d = levenshtein(text.slice(s, s + wl), q);
      if (d < best) best = d;
      if (best === 0) return 0;
    }
  }
  return best <= maxD ? best : -1;
}

function cmdkHighlight(text, matches) {
  if (!matches || !matches.length) return escapeHtml(text);
  const idxs = new Set();
  matches.forEach(m => {
    if (m.key === 'n' || m.key === 'd') {
      (m.indices || []).forEach(([s, e]) => { for (let i = s; i <= e; i++) idxs.add(i); });
    }
  });
  if (!idxs.size) return escapeHtml(text);
  let out = '';
  for (let i = 0; i < text.length; i++) {
    const ch = escapeHtml(text[i]);
    out += idxs.has(i) ? `<mark>${ch}</mark>` : ch;
  }
  return out;
}

function escapeHtml(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
}

function cmdkToggle() { cmdkOpened ? cmdkClose() : cmdkOpen(); }

function cmdkOpen() {
  const overlay = document.getElementById('cmdkOverlay');
  if (!overlay) return;
  overlay.setAttribute('aria-label', _t('cmdk.title', '工具搜索'));
  cmdkOpened = true;
  overlay.classList.add('open');
  ensureSearchIndexLoaded().then(() => {
    cmdkInitFuse();
    const input = document.getElementById('cmdkInput');
    if (input) { input.value = ''; input.focus(); }
    cmdkRender('');
  });
}

function cmdkClose() {
  const overlay = document.getElementById('cmdkOverlay');
  if (!overlay) return;
  cmdkOpened = false;
  overlay.classList.remove('open');
  const input = document.getElementById('cmdkInput');
  if (input) input.blur();
}


function cmdkRender(query) {
  const box = document.getElementById('cmdkResults');
  if (!box) return;
  if (!query.trim()) {
    // 空查询展示热门工具
    const hot = (HOT_TOOLS || []).slice(0, 8);
    cmdkResults = hot;
    box.innerHTML = `<div class="cmdk-group-label">${_t('tab.hot', '🔥 热门工具')}</div>` + hot.map((t, i) =>
      cmdkItemHtml(t, i, _tn(t), _td(t), false)
    ).join('');
    cmdkActive = 0;
    cmdkUpdateActive();
    return;
  }
  cmdkInitFuse();
  const items = toolboxSearch(query, 30);
  cmdkResults = items;
  if (!cmdkResults.length) {
    box.innerHTML = `<div class="cmdk-empty">🔍<br>${_t('search.no_match', '未找到相关工具')}<br><small>${_t('search.no_match_hint', '试试其他关键词，或检查这些相关工具：')}</small></div>`;
    return;
  }
  box.innerHTML = items.map((t, i) =>
    cmdkItemHtml(t, i, _tn(t), _td(t), true, null)
  ).join('');
  cmdkActive = 0;
  cmdkUpdateActive();
}

function cmdkItemHtml(t, i, name, desc, isSearch, matches) {
  const industry = INDUSTRY_INFO[t.i] || { name: t.i || '', icon: '🔧' };
  const cat = CAT_INFO[t.c] || { name: t.c || '' };
  const nameHtml = isSearch ? cmdkHighlight(name, matches) : escapeHtml(name);
  const descHtml = isSearch ? cmdkHighlight(desc || '', matches) : escapeHtml(desc || '');
  return `<div class="cmdk-item${i === cmdkActive ? ' active' : ''}" data-idx="${i}" data-url="${t.u}"
      onmouseenter="cmdkSetActive(${i})" onclick="cmdkGo(${i})">
    <div class="cmdk-item-ic" style="background:${t.b || '#f3f4f6'}">${t.ic || '🔧'}</div>
    <div class="cmdk-item-body">
      <div class="cmdk-item-name">${nameHtml}</div>
      <div class="cmdk-item-desc">${descHtml}</div>
    </div>
    <div class="cmdk-item-meta">${industry.icon} ${_ind(industry, t.i)}</div>
  </div>`;
}

function cmdkSetActive(i) {
  cmdkActive = i;
  cmdkUpdateActive();
}

function cmdkUpdateActive() {
  const items = document.querySelectorAll('#cmdkResults .cmdk-item');
  items.forEach((el, i) => {
    el.classList.toggle('active', i === cmdkActive);
    if (i === cmdkActive) el.scrollIntoView({ block: 'nearest' });
  });
}

function cmdkGo(i) {
  const t = cmdkResults[i];
  if (!t) return;
  if (typeof addToRecent === 'function') addToRecent(t.u);
  window.location.href = t.u;
}

function cmdkInputHandler(e) {
  cmdkRender(e.target.value);
}

function cmdkKeydown(e) {
  if (!cmdkOpened) return;
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    cmdkActive = Math.min(cmdkActive + 1, cmdkResults.length - 1);
    cmdkUpdateActive();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    cmdkActive = Math.max(cmdkActive - 1, 0);
    cmdkUpdateActive();
  } else if (e.key === 'Enter') {
    e.preventDefault();
    cmdkGo(cmdkActive);
  } else if (e.key === 'Escape') {
    e.preventDefault();
    cmdkClose();
  }
}

// 绑定命令面板事件（DOMContentLoaded 后）
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('cmdkInput');
  if (input) {
    input.addEventListener('input', cmdkInputHandler);
    input.addEventListener('keydown', cmdkKeydown);
  }
  const overlay = document.getElementById('cmdkOverlay');
  if (overlay) overlay.addEventListener('click', cmdkClose);
});
