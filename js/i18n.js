// js/i18n.js — ToolBox 多语言国际化引擎（纯前端，localStorage 持久化）
//
// 用法：
//   <script src="js/i18n.js"></script> 放在 app.js / common.js 之前
//   HTML 元素加 data-i18n="key" 翻译文本，data-i18n-ph="key" 翻译 placeholder，data-i18n-title="key" 翻译 title
//   切换语言：I18n.set('en-US') / I18n.set('zh-CN') 或点击页面右上角语言下拉
//   动态渲染行业/分类名：I18n.indName(info, key) / I18n.catName(info, key)
//
// 规范见 docs/i18n-spec.md。en-US 为唯一全局回退，zh-CN 为默认。
(function () {
  'use strict';

// ===== 语言注册表（LANG_REGISTRY）=====
// fallback: 缺失键回退到的语言；zh-CN 默认(无 fallback)，en-US 唯一全局回退
// 说明：本项目当前只保留 zh-CN + en-US 两语，其他语言先暂停。
var LANG_REGISTRY = [
  { code: 'zh-CN', label: '中文',    dir: 'ltr', fallback: null,    isDefault: true },
  { code: 'en-US', label: 'English', dir: 'ltr', fallback: null }
];

  var FALLBACK = 'en-US';

// ===== 地区子标签 → locale 映射（navigator.language 匹配用）=====
  var REGION_MAP = {
    'zh': 'zh-CN', 'cn': 'zh-CN', 'hk': 'zh-CN', 'tw': 'zh-CN', 'mo': 'zh-CN',
    'en': 'en-US', 'us': 'en-US', 'gb': 'en-US', 'au': 'en-US', 'ca': 'en-US', 'nz': 'en-US'
  };

  // ===== 时区 → locale 兜底（纯前端无 IP 地理时的次级判定）=====
  var TIMEZONE_MAP = {
    // 目前保留 en-US/zh-CN 两语，不依赖时区兜底到其他语种
  };

  // ===== 语言包（PACKS）=====
  // zh-CN 留空 => 通过 data-i18n-fb 回退页面原始中文
  // 其余语言包可在 i18n/<code>.json 加载或由构建注入；v1 先复用 en-US 回退
  var PACKS = {
    'zh-CN': {},
    'en-US': {
      // 通用 UI
      'app.name': 'ToolBox',
      'nav.search': 'Search',
      'nav.theme': 'Toggle theme',
      'nav.hot': 'Hot tools',
      'nav.recent': 'Recent',
      'nav.fav': 'Favorites',
      'nav.guide': 'User Guide',
      'nav.cat': 'Categories',
      'hero.title': 'Free Online Tools',
      'hero.sub': '6000+ free tools, all running locally in your browser. No sign-up, your data stays private.',
      'hero.tags': 'Popular:',
      'hero.chain': 'Tool Chains: link multiple tools, output flows into the next input',
      'tab.hot': '🔥 Hot Tools',
      'tab.all': 'All Tools',
      'tab.fav': 'Favorites',
      'tab.recent': 'Recent',
      'section.why': 'Why ToolBox',
      'section.cat': 'Categories',
      'section.hotcat': 'Popular Categories',
      'section.hottools': 'Popular Tools',
      'section.comtools': 'Common Tools',
      'section.about': 'About',
      'btn.allHot': 'All hot tools →',
      // 工具页公共框架（chrome）
      'bc.home': 'Home',
      'tool.related': '🔗 Related Tools',
      'tool.notes': '⚠️ Usage Notes & Cautions',
      'tool.copy': '📋 Copy Result',
      'tool.download': '💾 Download',
      'tool.sample': '📦 Example',
      'tool.clear': '🗑️ Clear',
      'tool.waiting': 'Waiting for input...',
      'tool.fav': 'Favorites',
      'tool.fav_add': 'Add to favorites',
      'tool.fav_remove': 'Remove favorite',
      'tool.theme_toggle': 'Toggle theme',
      'tool.guide_link': '📖 User Guide',
      'tool.copy_ok': 'Copied',
      'tool.subscript': 'Subscript',
      'tool.superscript': 'Superscript',
      'tool.result_empty': 'Result is empty',
      'tool.device_mobile': 'mobile',
      'tool.device_pc': 'desktop',
      'nav.back': '← ToolBox',
      'cat.suffix_tools': 'Tools',
      'btn.allInd': 'View all industries →',
      'search.placeholder': 'Search tools, categories or features...',
      'search.mobile': 'Search tools...',
      'search.cmdk': 'Search 6000+ tools, categories or features...',
      'cmdk.title': 'Tool Search',
      'cmdk.select': 'Select',
      'cmdk.open': 'Open',
      'cmdk.close': 'Close',
      'cmdk.pure': 'Pure frontend · Data stays in your browser',
      'common.copy': 'Copy',
      'common.use': 'Use',
      'common.all': 'All',
      'lang.switch': 'Language',
      'quality.label': 'Quality',
      'quality.A': 'Professional Tools',
      'quality.A.desc': 'Formula explanations, charts & multi-parameter calculations',
      'quality.B': 'Standard Tools',
      'quality.B.desc': 'Full interaction and calculation logic',
      'quality.C': 'Lite Tools',
      'quality.C.desc': 'Quick reference / lookup pages',
      'explore.title': '🧭 Explore Tools',
      'explore.subtitle': 'Explore 6000+ free online tools',
      'explore.hint': 'Pick a category above, or search directly · Pure frontend, your data stays local',
      'explore.hot': 'Popular Industries',
      'footer.privacy': 'Pure frontend · Data never leaves your browser',
      // 移动端底部 Tab
      'tabbar.home': 'Home',
      'tabbar.cat': 'Categories',
      'tabbar.search': 'Search',
      'tabbar.hot': 'Hot',
      'tabbar.fav': 'Favorites',
      // 功能分类
      'cat_text': 'Text', 'cat_encode': 'Encode', 'cat_convert': 'Convert',
      'cat_generate': 'Generator', 'cat_dev': 'Developer', 'cat_design': 'Design',
      'cat_image': 'Image', 'cat_math': 'Math', 'cat_validator': 'Validator',
      'cat_reference': 'Reference', 'cat_game': 'Games', 'cat_finance': 'Finance',
      'cat_calculator': 'Calculator', 'cat_health': 'Health', 'cat_engineer': 'Engineering',
      // 行业：12 个默认 + 部分常见行业的英文名（其余回退中文名）
      'ind_it': 'IT & Dev', 'ind_finance': 'Finance', 'ind_design': 'Design',
      'ind_biz': 'Business', 'ind_marketing': 'Marketing', 'ind_science': 'Science',
      'ind_health': 'Health', 'ind_life': 'Daily Life', 'ind_edu': 'Education',
      'ind_legal': 'Legal', 'ind_fun': 'Fun', 'ind_travel': 'Travel',
      'ind_ai': 'AI & ML', 'ind_data': 'Data Analysis', 'ind_engineering': 'Engineering',
      'ind_electronics': 'Electronics', 'ind_sales': 'Sales', 'ind_startup': 'Startup',
      'ind_image': 'Image', 'ind_video': 'Video', 'ind_music': 'Music',
      'ind_writing': 'Writing', 'ind_food': 'Food', 'ind_home': 'Home',
      'ind_language': 'Language', 'ind_exam': 'Exam', 'ind_history': 'History',
      'ind_literature': 'Literature', 'ind_math': 'Math', 'ind_stats': 'Statistics',
      'ind_medical': 'Medical', 'ind_entertainment': 'Entertainment', 'ind_sports': 'Sports',
      'ind_chinese': 'Chinese Culture',       'ind_yi': 'I Ching', 'ind_fengshui': 'Feng Shui',
      // 行业补全（批次2：补齐缺失的 ind_* 键，覆盖首页行业标签/面包屑）
      'ind_fortune': 'Fortune', 'ind_agriculture': 'Agriculture', 'ind_construction': 'Construction',
      'ind_manufacturing': 'Manufacturing', 'ind_logistics': 'Logistics', 'ind_energy': 'Energy',
      'ind_environment': 'Environment', 'ind_automotive': 'Automotive', 'ind_beauty': 'Beauty',
      'ind_pet': 'Pet Care', 'ind_parenting': 'Parenting', 'ind_gardening': 'Gardening',
      'ind_mining': 'Mining', 'ind_textile': 'Textile', 'ind_chemical': 'Chemical',
      'ind_fishery': 'Fishery', 'ind_forestry': 'Forestry', 'ind_livestock': 'Livestock',
      'ind_audit': 'Audit', 'ind_eco': 'Eco', 'ind_edu2': 'Education', 'ind_encode': 'Encode',
      'ind_gardening2': 'Gardening', 'ind_kids': 'Kids',
      'ind_legal2': 'Legal Services', 'ind_library': 'Library',
      'ind_logistics2': 'Warehousing', 'ind_maritime': 'Maritime',
      'ind_martial': 'Martial Arts', 'ind_medical2': 'Medical Specialist',
      'ind_misc': 'Miscellaneous', 'ind_misc2': 'Misc Tools',
      'ind_museum': 'Museums', 'ind_pet-training': 'Pet Training',
      'ind_petrochem': 'Petrochemical', 'ind_pets': 'Pets',
      'ind_photo2': 'Photography', 'ind_restaurant': 'Restaurant',
      'ind_service': 'Services', 'ind_statistics': 'Statistics',
      'ind_textile2': 'Textile', 'ind_woodworking': 'Woodworking',
      // 首页静态/动态渲染扩展键（批次2）
      'why.sub': 'Not just another skinned tool site — a toolbox that is truly on your side',
      'why.c1_title': 'Data never leaves your browser',
      'why.c1_desc': 'All computation happens locally. No server, no upload, no data collection. Handle sensitive files with peace of mind.',
      'why.c2_title': 'Instant pure-frontend load',
      'why.c2_desc': 'No backend wait, no loading spinners. Ready on open; speed depends on your device, not the server.',
      'why.c3_title': 'No ads, no login',
      'why.c3_desc': 'No popups, no forced sign-up, no limits. Use and go. Free forever.',
      'why.c4_title': '6000+ full coverage',
      'why.c4_desc': 'From developers to daily life, 200+ niche industries in one place. No jumping between a dozen sites.',
      'hero.badge1': 'Runs pure-frontend',
      'hero.badge2': 'Data stays in browser',
      'hero.badge3': 'No login required',
      'hero.badge4': 'Free forever, no ads',
      'breadcrumb.nav': 'Categories',
      'ad.label': '— Sponsored —',
      'ad.taobao_title': 'Taobao Picks',
      'ad.taobao_desc': 'Curated quality goods, limited-time offers',
      'ad.taobao_cta': 'Shop now →',
      'ad.taobao_desc_m': 'Curated quality goods',
      'foot.tool_json': 'JSON Formatter',
      'foot.tool_qr': 'QR Code Generator',
      'foot.tool_pwd': 'Password Generator',
      'foot.tool_color': 'Color Picker',
      'foot.tool_regex': 'Regex Tester',
      'foot.tool_timestamp': 'Timestamp Converter',
      'foot.sitemap': 'Sitemap',
      'foot.contact': 'Contact & Feedback',
      'foot.manage_data': 'Manage Local Data',
      'ind.view_all': 'View all {n} industries →',
      'ind.collapse': 'Collapse ↑',
      'cat.empty': 'No tools in this category',
      'common.loading': 'Loading...',
      'state.loading': 'Loading...',
      'state.load_fail': 'Load failed, please refresh and try again',
      'quality.empty': 'No tools at this quality level',
      'view.empty_recent': 'No recent tools',
      'view.empty_fav': 'No favorite tools',
      'view.empty': 'No data',
      'search.results': '🔍 Search Results',
      'search.no_match': 'No matching tools found',
      'search.no_match_hint': 'Try other keywords, or check these related tools:',
      'search.placeholder_hint': 'Type keywords to start searching',
      'search.related': 'Related Tools',
      'toast.copy_success': 'Copied to clipboard',
      'toast.copy_failed': 'Copy failed, please copy manually',
      'toast.copy_prompt': 'Please copy manually:',
      'toast.copy_target_missing': 'No copyable result found',
      'toast.element_not_found': 'Element not found',
      'toast.fav_added': 'Added to favorites ❤️',
      'toast.fav_removed': 'Removed from favorites',
      'toast.reset': 'Reset',
      'toast.cleared': 'Cleared',
      'toast.history_cleared': 'History cleared',
      'toast.history_restored': 'History restored',
      'toast.history_loaded': 'History loaded',
      'toast.deleted': 'Deleted',
      'toast.saved': 'Saved',
      'toast.loaded': 'Loaded',
      'toast.empty_data': 'No data',
      'toast.needs_calculation': 'Please calculate first',
      'toast.needs_generate': 'Please generate first',
      'toast.invalid_input': 'Please enter valid input',
      'toast.empty_source': 'No content to process',
      'toast.empty_export': 'No data to export',
      'toast.empty_download': 'No downloadable content',
      'toast.export_ok': 'Exported successfully',
      'toast.export_failed': 'Export failed',
      'toast.import_ok': 'Imported successfully',
      'toast.import_failed': 'Import failed',
      'toast.empty_favorite': 'No favorites yet',
      'validate.number': 'Please enter a valid number',
      'privacy.badge_title': 'This tool runs on pure frontend. Data is processed locally and never uploaded (click to manage local data)',
      'privacy.badge_text': 'Local Mode',
      'privacy.badge_aria': 'Local data management',
      'tool.file_upload_hint': 'Please upload an image first',
      'tool.image_load_error': 'Image failed to load',
      'tool.image_load_ok': 'Image loaded',
      'ad.label_promo': '— Sponsored —',
      'ad.label': '— Advertising —',
      'ad.taobao_title': 'Taobao Picks',
      'ad.taobao_desc': 'Curated quality products, limited-time offers',
      'ad.taobao_cta': 'Check it out →',
      'ad.track_event': 'Ad click',
      'ad.fallback_text': '⭐ Bookmark ToolBox: 6000+ free tools anytime · Pure frontend · Data stays in browser'
    }
  };

  var KEY = 'toolbox_lang';
  var current = 'zh-CN';

  // ===== 工具函数 =====
  function isValidLang(lang) {
    for (var i = 0; i < LANG_REGISTRY.length; i++) {
      if (LANG_REGISTRY[i].code === lang) return true;
    }
    return false;
  }

  // 规范化：兼容旧调用 set('en'/'zh')，en_US→en-US，未知→null
  function normalize(lang) {
    if (!lang) return null;
    if (lang === 'en') return 'en-US';
    if (lang === 'zh') return 'zh-CN';
    lang = String(lang).replace('_', '-');
    if (isValidLang(lang)) return lang;
    var base = lang.split('-')[0].toLowerCase();
    if (REGION_MAP[base]) return REGION_MAP[base];
    return null;
  }

  // 判定语言（优先级：?lang > localStorage > 浏览器含中文变体?中文 : 页面默认<html lang>）
  function detect() {
    try {
      var params = new URLSearchParams(location.search);
      var u = normalize(params.get('lang'));
      if (u) return u;
    } catch (e) {}
    try {
      var s = localStorage.getItem(KEY);
      var sn = normalize(s);
      if (sn) return sn;
    } catch (e) {}
    // 中文优先：未显式指定(?lang/localStorage)时，默认跟随页面 <html lang>（中文），
    // 确保中文搜索引擎(含 Googlebot, 其渲染 locale=en-US)渲染后索引中文；
    // 仅当用户浏览器语言含中文变体时才跟随浏览器。英文真实用户可点语言按钮或带 ?lang=en 显式切换。
    var htmlLang = (document.documentElement && document.documentElement.lang || '').toLowerCase();
    var pageDefault = normalize(htmlLang) || 'zh-CN';
    var langs = (navigator.languages && navigator.languages.length)
      ? navigator.languages : [navigator.language];
    for (var i = 0; i < langs.length; i++) {
      var n = normalize(langs[i]);
      if (n === 'zh-CN') return 'zh-CN';
    }
    return pageDefault;
  }

  function get() { return current; }

  // 回退链解析：current -> current.fallback -> ... -> en-US
  function resolve(key, fb) {
    var seen = {};
    var l = current;
    while (l && !seen[l]) {
      seen[l] = true;
      var pack = PACKS[l];
      if (pack && pack.hasOwnProperty(key)) return pack[key];
      var reg = null;
      for (var i = 0; i < LANG_REGISTRY.length; i++) {
        if (LANG_REGISTRY[i].code === l) reg = LANG_REGISTRY[i];
      }
      l = reg ? reg.fallback : null;
    }
    return (fb == null) ? key : fb;
  }

  function t(key, fallback) { return resolve(key, fallback); }

  function indName(info, key) {
    if (!info) return '';
    if (current !== 'zh-CN') {
      if (info.en) return info.en;
      var en = t('ind_' + (key || info.key), null);
      if (en && en.indexOf('ind_') !== 0) return en;
      return info.name || '';
    }
    return info.name || '';
  }
  function catName(info, key) {
    if (!info) return '';
    if (current !== 'zh-CN') {
      if (info.en) return info.en;
      var en = t('cat_' + (key || info.key), null);
      if (en && en.indexOf('cat_') !== 0) return en;
      return info.name || '';
    }
    return info.name || '';
  }

  // 注册/合并一个语言包（工具页 per-industry 字典用）
  function addPack(lang, dict) {
    if (!lang || !dict) return;
    if (!PACKS[lang]) PACKS[lang] = {};
    for (var k in dict) {
      if (Object.prototype.hasOwnProperty.call(dict, k)) PACKS[lang][k] = dict[k];
    }
  }

  function applyLangAttr() {
    try {
      if (!document.documentElement) return;
      document.documentElement.lang = current;
      var reg = null;
      for (var i = 0; i < LANG_REGISTRY.length; i++) {
        if (LANG_REGISTRY[i].code === current) reg = LANG_REGISTRY[i];
      }
      document.documentElement.dir = (reg && reg.dir === 'rtl') ? 'rtl' : 'ltr';
    } catch (e) {}
  }

  function apply(root) {
    root = root || document;
    var nodes = root.querySelectorAll('[data-i18n],[data-i18n-ph],[data-i18n-title]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.hasAttribute('data-i18n')) {
        var k = el.getAttribute('data-i18n');
        var txt = t(k, el.getAttribute('data-i18n-fb') || el.textContent);
        if (txt) el.textContent = txt;
      }
      if (el.hasAttribute('data-i18n-ph')) {
        el.setAttribute('placeholder', t(el.getAttribute('data-i18n-ph'), el.getAttribute('placeholder')));
      }
      if (el.hasAttribute('data-i18n-title')) {
        el.setAttribute('title', t(el.getAttribute('data-i18n-title'), el.getAttribute('title')));
      }
    }
    updateSwitchers();
  }

  function updateSwitchers() {
    var sels = document.querySelectorAll('.lang-switcher select');
    for (var i = 0; i < sels.length; i++) {
      if (sels[i].value !== current) sels[i].value = current;
    }
  }

  // 注入语言下拉（替代原二进制 中/EN 按钮）
  function mountSwitcher(container) {
    if (!container || container.querySelector('.lang-switcher')) return;
    var wrap = document.createElement('div');
    wrap.className = 'lang-switcher nav-icon-btn';
    wrap.style.cssText = 'display:inline-flex;align-items:center;gap:6px;padding:0 10px;';
    var flag = document.createElement('span');
    flag.className = 'lang-flag-icon';
    flag.textContent = '\uD83C\uDF10'; // 🌐
    flag.style.cssText = 'font-size:16px;pointer-events:none;';
    var sel = document.createElement('select');
    sel.setAttribute('aria-label', 'Language / 语言');
    sel.title = 'Language / 语言';
    sel.style.cssText = 'background:transparent;border:none;color:inherit;font:inherit;cursor:pointer;outline:none;appearance:none;-webkit-appearance:none;';
    for (var i = 0; i < LANG_REGISTRY.length; i++) {
      var o = document.createElement('option');
      o.value = LANG_REGISTRY[i].code;
      o.textContent = LANG_REGISTRY[i].label;
      if (LANG_REGISTRY[i].code === current) o.selected = true;
      sel.appendChild(o);
    }
    sel.onchange = function () { set(sel.value); };
    var caret = document.createElement('span');
    caret.className = 'lang-caret';
    caret.textContent = '▾';
    caret.style.cssText = 'font-size:10px;opacity:.6;pointer-events:none;';
    wrap.appendChild(flag);
    wrap.appendChild(sel);
    wrap.appendChild(caret);
    container.appendChild(wrap);
  }

  function autoMount() {
    var a = document.querySelector('.nav-actions');
    if (a) mountSwitcher(a);
    var m = document.querySelector('.nav-mobile-actions');
    if (m) mountSwitcher(m);
    if (!a && !m) {
      var n = document.querySelector('.nav');
      if (n) mountSwitcher(n);
    }
  }

  // 工具页标题同步（P1）：构建期已将 <title> 预渲染为英文以优化国际 SEO 首抓，
  // 中文模式切回 <meta name="title-zh"> 保存的中文标题；英文/其他模式恢复 <title> 原值。
  var _descZh = '';
  function syncTitle() {
    try {
      var titleEl = document.querySelector('title');
      if (!titleEl) return;
      if (current === 'en-US') {
        var enMeta = document.querySelector('meta[name="title-en"]');
        if (enMeta && enMeta.getAttribute('content')) {
          document.title = enMeta.getAttribute('content');
        }
      } else {
        document.title = titleEl.textContent;
      }
    } catch (e) {}
  }
  function syncDesc() {
    try {
      var descEl = document.querySelector('meta[name="description"]');
      if (!descEl) return;
      if (current === 'en-US') {
        var enMeta = document.querySelector('meta[name="desc-en"]');
        if (enMeta && enMeta.getAttribute('content')) {
          descEl.setAttribute('content', enMeta.getAttribute('content'));
        }
      } else {
        descEl.setAttribute('content', _descZh);
      }
    } catch (e) {}
  }

  function set(lang, opts) {
    opts = opts || {};
    var nl = normalize(lang);
    if (!nl) nl = FALLBACK;
    current = nl;
    if (opts.persist !== false) {
      try { localStorage.setItem(KEY, current); } catch (e) {}
    }
    try {
      var url = new URL(location.href);
      url.searchParams.set('lang', current);
      history.replaceState(null, '', url);
    } catch (e) {}
    applyLangAttr();
    apply(document);
    syncTitle();
    syncDesc();
    if (window.dispatchEvent) window.dispatchEvent(new Event('toolbox:langchange'));
  }

  function init() {
    try {
      var _dEl = document.querySelector('meta[name="description"]');
      if (_dEl) _descZh = _dEl.getAttribute('content') || '';
    } catch (e) {}
    try {
      current = detect();
    } catch (e) { current = FALLBACK; }
    applyLangAttr();
    apply(document);
    syncTitle();
    syncDesc();
    autoMount();
  }

  window.I18n = {
    get: get, set: set, t: t,
    indName: indName, catName: catName,
    apply: apply, applyLangAttr: applyLangAttr, mountSwitcher: mountSwitcher, init: init,
    addPack: addPack,
    LANG_REGISTRY: LANG_REGISTRY, detect: detect, normalize: normalize,
    FALLBACK: FALLBACK
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 页面加载完成后，根据 URL ?lang 参数兜底自动对齐语言。
  // 临时覆盖语义：persist:false 不写 localStorage，避免覆盖用户手动选择的语言偏好。
  function ensureLangFromQuery() {
    try {
      var params = new URLSearchParams(location.search);
      var q = normalize(params.get('lang'));
      if (q && q !== current) set(q, { persist: false });
    } catch (e) {}
  }
  if (document.readyState === 'complete') {
    ensureLangFromQuery();
  } else {
    window.addEventListener('load', ensureLangFromQuery);
  }
})();
