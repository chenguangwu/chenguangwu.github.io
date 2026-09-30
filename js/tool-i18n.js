/*
 * tool-i18n.js — 工具页国际化运行时
 * 依赖：js/i18n.js（须在之前以 defer 加载，自动 init 并挂载语言切换器到 .nav）
 *
 * 职责：
 *  1. 翻译工具页公共框架（chrome）：面包屑首页/行业名、相关工具标题、使用说明标题、复制/下载/示例/清空按钮、等待输入占位等。
 *     通过选择器批量处理，无需逐个工具页加 data-i18n，覆盖全部 5000+ 工具页。
 *  2. 加载 per-industry 字典 i18n/tools/<industry>.json（若存在），注册到 I18n 语言包，
 *     使工具专属内容（标题/简介/输入标签/说明项）通过 data-i18n="<industry>.<slug>.*" 翻译。
 *  3. 监听 toolbox:langchange 重新应用。
 */
(function () {
  'use strict';
  if (!window.I18n) return;
  var I18n = window.I18n;
  function isEnglish() { return I18n.get() === 'en-US'; }
  function sharedI18nUrl(name) { return '/i18n/tools/' + name; }

  function getIndustry() {
    var m = document.querySelector('meta[name="toolbox"]');
    if (!m) return null;
    var c = m.getAttribute('content') || '';
    var mm = c.match(/industry=([^,\s]+)/);
    return mm ? mm[1].trim() : null;
  }

  function getSlug() {
    var m = document.querySelector('meta[name="toolbox"]');
    if (!m) return null;
    var c = m.getAttribute('content') || '';
    var mm = c.match(/slug=([^,\s]+)/);
    if (mm) return mm[1].trim();
    // 兜底：从文件名推断
    var f = location.pathname.split('/').pop().replace(/\.html$/, '');
    return f || null;
  }

  // ---- 框架翻译（chrome）：对所有语言（含 zh-CN 做幂等还原）----
  function applyChrome() {
    var lang = I18n.get();
    var isZh = !isEnglish();

    // 面包屑：首页
    var bcLinks = document.querySelectorAll('.breadcrumb a');
    if (bcLinks.length > 0) {
      var home = bcLinks[0];
      if (home.textContent.trim() === '首页' || !isZh) {
        home.textContent = I18n.t('bc.home', '首页');
      }
    }
    // 面包屑：行业名（保留图标，仅替换文字）
    if (bcLinks.length > 1) {
      var indLink = bcLinks[1];
      var ind = getIndustry();
      var txt = indLink.textContent;
      var m = txt.match(/^(\S+)\s+(.*)$/);
      var icon = m ? m[1] : '';
      var nameZh = m ? m[2] : txt;
      if (ind && !isZh) {
        indLink.textContent = (icon ? icon + ' ' : '') + I18n.indName({ key: ind }, ind);
      } else if (ind && isZh && icon && nameZh) {
        indLink.textContent = icon + ' ' + I18n.indName({ key: ind, name: nameZh }, ind);
      }
    }

    // 相关工具标题
    var rt = document.querySelector('.related-tools-title') || document.querySelector('.related-tools h3');
    if (rt) rt.textContent = I18n.t('tool.related', '🔗 相关工具');

    // 使用说明标题
    var nt = document.querySelector('.tool-notes-title');
    if (nt) nt.textContent = I18n.t('tool.notes', '⚠️ 使用说明与注意事项');

    // 顶部返回链接（保持 ToolBox 品牌）
    var back = document.querySelector('.nav > a');
    if (back && back.getAttribute('href') && back.getAttribute('href').indexOf('index.html') > -1) {
      // 仅当为纯返回链接（无图标）时翻译文案
      if (!isZh && /ToolBox/.test(back.textContent)) back.textContent = I18n.t('nav.back', '← ToolBox');
    }

    // 常见按钮文案（按已知中文精确匹配替换，避免误伤）
    translateButtons(isZh);
    // 通用 UI 词精确短语自动英文化（label/button/option 确定性部分）
    translateGenericUI(isZh);
    // 工具正文中文短语精确映射（h1/h3/h4/li/th/td/label/button/option/textarea/span/a/div 确定性正文）
    translateBodyPhrases(isZh);
    // 相关工具卡片：英文模式用 slug->en/ed 映射替换中文 SEO 描述（消除全局组件中文残留）
    translateRelatedTools(isZh);
    // 【第三层】per-tool 全量英文字典：最后执行 ⇒ 覆盖 -body.json / 共享短语表的低质与未覆盖值
    if (isEnglish()) loadEnDict(getIndustry(), getSlug());
    applyEnDict(isZh);
  }

  function translateButtons(isZh) {
    var map = {
      '📋 复制结果': 'tool.copy',
      '📋 复制': 'tool.copy',
      '💾 下载 JSON': 'tool.download',
      '💾 下载': 'tool.download',
      '📦 示例': 'tool.sample',
      '🗑️ 清空': 'tool.clear'
    };
    var btns = document.querySelectorAll('.toolbar .btn, .json-actions .btn, button.btn');
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i];
      var label = b.textContent.trim();
      if (map[label]) {
        b.textContent = isZh ? label : I18n.t(map[label], label);
      }
    }
    // 等待输入占位
    var waits = document.querySelectorAll('.json-output');
    for (var j = 0; j < waits.length; j++) {
      if (waits[j].textContent.trim() === '等待输入...') {
        waits[j].textContent = isZh ? '等待输入...' : I18n.t('tool.waiting', 'Waiting for input...');
      }
    }
  }

  // ---- 通用 UI 词精确短语自动英文化（零 MT，基于全站真实高频短语提取）----
  // 仅精确匹配完整短语，避免误翻正文里的相同字词；覆盖 label/button/option 的确定性 UI 词。
  // 工具专属内容（公式标签/说明段落/列表）由 data-i18n + 行业字典 en-US 逐条手翻覆盖。
  // 【致命时序 bug 修复 2026-09-29】旧写法在此处对 window.__TI18N_EN 一次性快照：
  // 本 IIFE 由页面静态引入、先于 boot() 动态加载的 tool-i18n-en.js 执行 ⇒ 线上英文态
  // GEN_UI_MAP / BODY_PHRASE_MAP 恒为 {}（全局层整体空转：按钮 / tab / 下拉选项 / label
  // 全部残留中文），而 per-tool 字典是运行时 fetch 赋值的活变量照常生效 —— 形成线上
  // 「部分翻部分不翻」而本地探针（先注入数据再执行脚本）全绿的假象。
  // 现改为空初始化 + syncEnMaps() 实时读取（init / applyAll 两个入口都会调用）。
  var GEN_UI_MAP = {};
  var GEN_ORIG = new WeakMap();
  // 剥离开头的 emoji/符号前缀，返回 {prefix, core}，用于按钮「emoji+中文」与 GEN_UI_MAP 核心词匹配
  function stripEmojiPrefix(s) {
    var m = s.match(/^[^一-鿿A-Za-z]+/);
    if (!m) return { prefix: '', core: s.trim() };
    return { prefix: m[0].trim(), core: s.slice(m[0].length).trim() };
  }
  function translateGenericUI(isZh) {
    var nodes = document.querySelectorAll('label, button.btn, .toolbar .btn, select option, .json-actions .btn, .tab-btn');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      // 守卫：含「表单控件」或「带 id 后代」的容器不得整节点替换 —— el.textContent = tr
      // 会把容器内的 <input>/<select>/<textarea> 或页面按 id 引用的子容器一并删除（如
      // random-string 复选框 <label><input>是</label>、diff 的 leftDiff/rightDiff 等），
      // 使页面 JS 读 getElementById(id) 时抛 "Cannot read properties of null"。
      if (el.children && el.children.length && el.querySelector('input,select,textarea,[id]')) continue;
      var txt = el.textContent.trim();
      if (isZh) { if (GEN_ORIG.has(el)) el.textContent = GEN_ORIG.get(el); continue; }
      var sp = stripEmojiPrefix(txt);
      var tr = GEN_UI_MAP[txt] || GEN_UI_MAP[sp.core] || GEN_UI_MAP[sp.core.replace(/\s+/g, '')];
      if (tr) {
        if (!GEN_ORIG.has(el)) GEN_ORIG.set(el, txt);
        el.textContent = sp.prefix ? (sp.prefix + ' ' + tr) : tr;
      }
    }
  }

  // ---- 工具正文中文短语精确映射（零 MT，逐条人工翻译；accessibility 试点首批）----
  // 与 GEN_UI_MAP 同源：英文模式下对 h1/h3/h4/p/li/th/td/label/button/option/textarea/span/a/div 的
  // 整节点 textContent 做精确匹配替换，避免误翻正文；未匹配的中文保留（不中英混排）。
  // 全局 boilerplate（功能特点/使用场景/常见问题/工具简介/健康类说明）一次翻译，全站共用模板页受益；
  // 行业专属短语按行业分批追加。调用前跳过 data-i18n 元素（交 I18n.apply 处理）。
  var BODY_PHRASE_MAP = {};   // 实际数据由 syncEnMaps() 运行时同步（同 GEN_UI_MAP 时序 bug，见上）

  // 全局层数据同步：tool-i18n-en.js 可能晚于本脚本动态加载，
  // 每次进入翻译流程（init / applyAll）前必须重读 window.__TI18N_EN。
  function syncEnMaps() {
    if (window.__TI18N_EN) {
      GEN_UI_MAP = window.__TI18N_EN.GEN_UI_MAP || {};
      BODY_PHRASE_MAP = window.__TI18N_EN.BODY_PHRASE_MAP || {};
    }
  }
  // ---- 相关工具卡片：英文模式用 slug->en/ed 映射替换中文 SEO 描述 ----
  var SLUG_EN = null;
  function loadSlugEn() {
    if (SLUG_EN) return Promise.resolve(SLUG_EN);
    return fetch(sharedI18nUrl('slug-en.json'))
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (d) { SLUG_EN = d || {}; return d || {}; })
      .catch(function () {
        SLUG_EN = {};
        return {};
      });
  }
  var RT_ORIG = new WeakMap();
  function cleanRelatedName(rawName) {
    if (!rawName) return rawName;
    var s = String(rawName).replace(/[\r\n\t]/g, ' ').replace(/\s+/g, ' ').trim();
    s = s.replace(/^[^:：]*?(?:工具名|名称|标题|描述|简介|说明)\s*[：:]\s*/, '');
    s = s.replace(/\s*\|\s*ToolBox[^|]*$/i, '');
    var sepIndex = s.indexOf(' - ');
    if (sepIndex > -1) return s.slice(0, sepIndex).trim();
    return s;
  }
  function normalizeRelatedKey(rawHref, currentIndustry) {
    if (!rawHref || !currentIndustry) return null;
    var href = (rawHref || '').split('?')[0].split('#')[0].trim();
    if (!href) return null;
    if (/^(https?:)?\/\//.test(href) || href.indexOf('javascript:') === 0 || href.indexOf('mailto:') === 0) return null;

    href = href.replace(/^(\.\.\/)+/, '');
    href = href.replace(/^\.\//, '');
    href = href.replace(/^\/+/, '');
    if (/index$/i.test(href)) return null;
    if (!/\.html$/i.test(href)) return null;
    href = href.replace(/\.html$/i, '');

    var parts = href.split('/').filter(function (seg) { return seg; });
    if (!parts.length) return null;
    if (parts[0] === 'tools' && parts.length > 1) {
      parts.shift();
    }
    if (parts.length === 1) {
      return currentIndustry + '/' + parts[0];
    }
    if (parts.length !== 2) {
      return null;
    }
    var ind = parts[parts.length - 2];
    var slug = parts[parts.length - 1];
    if (!ind || !slug) return null;
    if (/^index$/i.test(ind) || /^index$/i.test(slug)) return null;
    return ind + '/' + slug;
  }
  function translateRelatedTools(isZh) {
    var cards = document.querySelectorAll('.related-tool-card, .rt-item');
    var currentIndustry = getIndustry();
    for (var i = 0; i < cards.length; i++) {
      var a = cards[i];
      var rtName = a.querySelector('.rt-name');
      var rtDesc = a.querySelector('.rt-desc');
      if (isZh) {
        if (RT_ORIG.has(a)) {
          var o = RT_ORIG.get(a);
          if (rtName) rtName.textContent = o.n;
          if (rtDesc) rtDesc.textContent = o.d;
        }
        continue;
      }
      if (!RT_ORIG.has(a)) {
        RT_ORIG.set(a, {
          n: rtName ? cleanRelatedName(rtName.textContent) : '',
          d: rtDesc ? rtDesc.textContent : ''
        });
      }
      var href = a.getAttribute('href') || '';
      var key = normalizeRelatedKey(href, currentIndustry);
      if (!key) continue;
      (function (nameEl, descEl, k) {
        loadSlugEn().then(function (map) {
          var info = map[k];
          if (!info) {
            if (nameEl) nameEl.textContent = cleanRelatedName(nameEl.textContent);
            if (descEl) descEl.textContent = cleanRelatedName(descEl.textContent);
            return;
          }
          if (nameEl && info.en) nameEl.textContent = info.en;
          if (descEl && info.ed) descEl.textContent = info.ed;
          else if (descEl) descEl.textContent = cleanRelatedName(descEl.textContent);
        });
      })(rtName, rtDesc, key);
    }
  }

  var BODY_CHANGED = [];
  function translateBodyPhrases(isZh) {
    for (var k = 0; k < BODY_CHANGED.length; k++) {
      BODY_CHANGED[k].el.textContent = BODY_CHANGED[k].orig;
    }
    BODY_CHANGED = [];
    if (isZh) return;
    var ind = getIndustry();
    var indMap = ind ? BODY_IND_PHRASES[ind] : null;
    var nodes = document.querySelectorAll('h1, h3, h4, p:not(.intro), li, th, td, label, button.btn, select option, textarea, span, a, div');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.hasAttribute('data-i18n')) continue;
      if (el.closest && el.closest('[data-i18n]')) continue;
      if (el.querySelector && el.querySelector('[data-i18n]')) continue;
      // 守卫：含「表单控件」或「带 id 后代」的容器不得整节点替换 —— el.textContent = tr
      // 会连同容器内的 <input>/<select>/<textarea> 或页面 JS 按 id 引用的子容器（如 diff 的
      // leftDiff/rightDiff/unifiedDiff）一起删除，使 getElementById(id) 返回 null 抛
      // "Cannot read properties of null"。英文态实测 text-diff 中招：div.diff-panel 文本
      // 「原始文本」命中短语映射，整节点替换抹掉了 leftDiff 容器。
      // 这类容器的正文交由第三层 per-tool 字典（文本节点级替换，applyEnDict）处理，不丢译。
      if (el.children && el.children.length && el.querySelector('input,select,textarea,[id]')) continue;
      var txt = el.textContent.trim();
      var tr = null;
      if (BODY_PHRASE_MAP.hasOwnProperty(txt)) tr = BODY_PHRASE_MAP[txt];
      else if (COMMON_PHRASES.hasOwnProperty(txt)) tr = COMMON_PHRASES[txt];
      else if (indMap && indMap.hasOwnProperty(txt)) tr = indMap[txt];
      if (tr) {
        BODY_CHANGED.push({ el: el, orig: txt });
        el.textContent = tr;
      }
    }
  }

  // ---- 工具专属内容（data-i18n 指向 <industry>.<slug>.*）----
  function applyToolContent() {
    I18n.apply(document);
    // 同步切换器选中态
    var sels = document.querySelectorAll('.lang-switcher select');
    for (var i = 0; i < sels.length; i++) {
      if (sels[i].value !== I18n.get()) sels[i].value = I18n.get();
    }
  }

  function loadIndustryDict(industry) {
    if (!industry) return;
    var url = sharedI18nUrl(industry + '.json');
    if (window.fetch) {
      fetch(url, { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (dict) {
          if (!dict) return;
  // 字典格式：{ "<slug>": { "en-US": {...} } } 或扁平 { "<slug>": {...} }
          for (var slug in dict) {
            if (!Object.prototype.hasOwnProperty.call(dict, slug)) continue;
            var entry = dict[slug];
            if (!entry) continue;
            for (var lang in entry) {
              if (!Object.prototype.hasOwnProperty.call(entry, lang)) continue;
              I18n.addPack(lang, prefixKeys(entry[lang], industry + '.' + slug + '.'));
            }
          }
          applyToolContent();
        })
        .catch(function () { /* 字典缺失则忽略，回退中文 */ });
    }
  }

  function prefixKeys(obj, prefix) {
    var out = {};
    for (var k in obj) {
      if (!Object.prototype.hasOwnProperty.call(obj, k)) continue;
      out[prefix + k] = obj[k];
    }
    return out;
  }

  // ---- 工具正文（h2 标题 / 简介段落）动态英文化 ----
  // 数据源：i18n/tools/<industry>-body.json（scripts/gen_tool_i18n_en.py 生成，slug -> {title, intro}）
  // 设计：不改动 5254 个工具页 HTML，运行时按 slug 查表翻译；保留 emoji、公式 h2 跳过、data-i18n 已管理的页不重复处理。
  var BODY_MAP = {};   // { industry: { slug: { title, intro } } }
  var ORIG = {};       // { slug: { title, intro } } 原文缓存，用于切回中文还原
  var BODY_IND_PHRASES = {};   // { industry: { text: en } } 逐行业正文短语（按需加载，避免全局大表死重）
  var COMMON_PHRASES = {};     // { text: en } 跨行业通用短语（common-phrases.json，全站只加载一次）

  function isFormula(text) {
    if (!text) return false;
    return /[∑∫∂√≈≠≥≤×÷²³⁴⁵πΔΩμλσφθ]/.test(text);
  }

  function loadIndustryBody(industry) {
    if (!industry || BODY_MAP[industry]) return;
    var url = sharedI18nUrl(industry + '-body.json');
    if (window.fetch) {
      fetch(url, { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (map) {
          if (map) { BODY_MAP[industry] = map; applyToolBody(); }
        })
        .catch(function () { /* 字典缺失则忽略，回退中文 */ });
    }
  }

  // ---- 工具正文（逐行业独有短语）按需加载 ----
  // 数据源：i18n/tools/<industry>-phrases.json（按行业切分的 n=1 长尾手翻短语，扁平 { 中文: 英文 }）
  // 与 BODY_PHRASE_MAP 同源机制，但按行业隔离、运行时按需 fetch，避免 9 万条全量进全局大表拖慢每页加载。
  // 索引清单：i18n/tools/phrases-index.json（构建期产出，列出真正有 phrases 数据的行业）。
  // 全站仅部分行业生成过 phrases 数据；缺失行业若直接 fetch 会打到 404（虽被静默回退，
  // 但每页一次无谓请求）。改为先取索引、只对清单内行业发请求 → 0 个 404，
  // 且将来补生成 phrases 后由构建自动纳入索引、无需改这里。
  var PHRASES_INDEX = null;         // string[] | null
  var PHRASES_INDEX_PROMISE = null;

  // 跨行业通用短语：i18n/tools/common-phrases.json（全站只加载一次）
  // 高频通用文案（面包屑标签、通用 FAQ、通用 UI）放这里，避免 277 个行业文件各存一份，
  // 也避免继续撑大 BODY_PHRASE_MAP（该表已逾 400KB，每页都要加载）。
  var COMMON_PHRASES_PROMISE = null;

  function loadCommonPhrases() {
    if (COMMON_PHRASES_PROMISE) return COMMON_PHRASES_PROMISE;
    if (!window.fetch) { COMMON_PHRASES_PROMISE = Promise.resolve(null); return COMMON_PHRASES_PROMISE; }
    COMMON_PHRASES_PROMISE = fetch(sharedI18nUrl('common-phrases.json'))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (map) {
        if (map) {
          COMMON_PHRASES = map;
          if (isEnglish()) translateBodyPhrases(false);
        }
        return COMMON_PHRASES;
      })
      .catch(function () { return COMMON_PHRASES; });
    return COMMON_PHRASES_PROMISE;
  }

  function loadPhrasesIndex() {
    if (PHRASES_INDEX !== null) return Promise.resolve(PHRASES_INDEX);
    if (PHRASES_INDEX_PROMISE) return PHRASES_INDEX_PROMISE;
    if (!window.fetch) { PHRASES_INDEX = []; return Promise.resolve(PHRASES_INDEX); }
    PHRASES_INDEX_PROMISE = fetch(sharedI18nUrl('phrases-index.json'))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (obj) { PHRASES_INDEX = (obj && obj.industries) || []; return PHRASES_INDEX; })
      .catch(function () { PHRASES_INDEX = []; return PHRASES_INDEX; });
    return PHRASES_INDEX_PROMISE;
  }

  function loadIndustryPhrases(ind) {
    if (!ind || BODY_IND_PHRASES[ind]) return;
    if (!window.fetch) return;
    loadPhrasesIndex().then(function (list) {
      if (!list || list.indexOf(ind) < 0) return;   // 该行业无 phrases 数据 → 不发请求（避免 404）
      var url = sharedI18nUrl(ind + '-phrases.json');
      fetch(url, { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (map) {
          if (!map) return;
          BODY_IND_PHRASES[ind] = map;
          if (isEnglish()) translateBodyPhrases(false);
        })
        .catch(function () { /* 字典缺失则忽略，回退中文 */ });
    });
  }

  function applyToolBody() {
    var ind = getIndustry(), slug = getSlug();
    if (!ind || !slug) return;
    var lang = I18n.get();
    var card = document.querySelector('.tool-card-accent') || document.querySelector('.card');
    if (!card) return;
    var h2 = card.querySelector('h2');
    var introP = card.querySelector('p');

    // 兜底：多卡片布局页的主工具卡内可能完全没有 <p>（其唯一的 <p data-zh> 落在次级卡片里），
    // 此时 introP 为 null，中文态会漏掉该段落 → 用户看到静态英文。
    // 该段落是「小节说明」而非主介绍，英文态**不可**套用 body.intro，故独立成 FB_INTRO，
    // 只在非英文态写回 data-zh 原文。
    var fbP = null;
    if (!introP) {
      var _cand = document.querySelectorAll('p[data-zh]');
      for (var _i = 0; _i < _cand.length; _i++) {
        if (!_cand[_i].hasAttribute('data-i18n')) { fbP = _cand[_i]; break; }
      }
    }

    // 已由 data-i18n 管理的（6 个手工工具页）交给 I18n.apply，跳过避免冲突
    var skipH2 = !!(h2 && (h2.querySelector('[data-i18n]') || isFormula(h2.textContent)));
    var skipIntro = !!(introP && introP.hasAttribute('data-i18n'));

    // 首次调用缓存原文（按字段独立判断，避免 h2 捕获定义 ORIG[slug] 后阻断 introP 捕获）。
    // 优先用 data-zh（构建期保存的中文原文）：预渲染英文到静态 HTML 后 textContent 已是英文，
    // 若不取 data-zh，中文用户切回会被钉死成英文。
    if (!skipH2 && h2 && (!ORIG[slug] || ORIG[slug].title === undefined)) {
      ORIG[slug] = ORIG[slug] || {};
      var _zhT = h2.getAttribute('data-zh');
      ORIG[slug].title = (_zhT != null) ? _zhT : h2.textContent;
    }
    if (!skipIntro && introP && (!ORIG[slug] || ORIG[slug].intro === undefined)) {
      ORIG[slug] = ORIG[slug] || {};
      var _zhI = introP.getAttribute('data-zh');
      ORIG[slug].intro = (_zhI != null) ? _zhI : introP.textContent;
    }

    if (!isEnglish()) {
      if (!skipH2 && h2 && ORIG[slug] && ORIG[slug].title != null) h2.textContent = ORIG[slug].title;
      if (!skipIntro && introP && ORIG[slug] && ORIG[slug].intro != null) introP.textContent = ORIG[slug].intro;
      // 兜底段落：同样在被切成英文前缓存 data-zh，并写回中文原文
      if (fbP) {
        ORIG[slug] = ORIG[slug] || {};
        if (ORIG[slug].fbIntro === undefined) ORIG[slug].fbIntro = fbP.getAttribute('data-zh');
        if (ORIG[slug].fbIntro != null) fbP.textContent = ORIG[slug].fbIntro;
      }
      return;
    }

    // 短语数据必须无条件加载：否则 -body.json 里没有该 slug 的页面会在这里提前 return，
    // 导致 common / 行业 phrases 永远加载不到，正文短语始终不翻译。
    loadCommonPhrases();
    loadIndustryPhrases(ind);

    var body = BODY_MAP[ind] && BODY_MAP[ind][slug];
    if (!body) {
      // 即便该工具没有 body 数据，切到英文时也要把已就绪的短语应用上去
      if (isEnglish()) {
        loadCommonPhrases().then(function () { translateBodyPhrases(false); });
      }
      return;
    }
    if (!skipH2 && h2 && body.title) {
      var m = h2.textContent.match(/^([^\u4e00-\u9fffA-Za-z0-9]*)([\s\S]*)$/);
      var icon = (m && m[1]) ? m[1] : '';
      h2.textContent = icon + body.title;
    }
    if (!skipIntro && introP && body.intro) {
      introP.textContent = body.intro;
    }
    // 数据可能已在首次加载（中文态）时就绪，切换语言时 promise 直接命中缓存、
    // 不会再走 then 分支，这里补一次确保短语被应用
    if (isEnglish()) {
      loadCommonPhrases().then(function () { translateBodyPhrases(false); });
    }
  }

  function init() {
    syncEnMaps();   // tool-i18n-en.js 动态加载完成后才进入此处，必须先同步全局层词表
    if (typeof I18n.applyLangAttr === 'function') I18n.applyLangAttr();
    applyChrome();
    applyToolContent();
    var ind = getIndustry();
    loadIndustryDict(ind);
    loadIndustryBody(ind);
    loadCommonPhrases();
    loadIndustryPhrases(ind);
    applyToolBody();
  }

  var EN_DATA_SRC = '/js/tool-i18n-en.js';
  function applyAll() {
    syncEnMaps();   // 语言切换事件入口同样先同步全局层词表（数据可能刚动态加载完）
    applyChrome();
    applyToolContent();
    applyToolBody();
    loadIndustryPhrases(getIndustry());
  }
  function boot() {
    if (!isEnglish() || window.__TI18N_EN) { init(); return; }
    var s = document.createElement('script');
    s.src = EN_DATA_SRC;
    s.onload = init; s.onerror = init;
    document.head.appendChild(s);
  }
  function onLangChange() {
    if (!isEnglish() || window.__TI18N_EN) { applyAll(); return; }
    var s = document.createElement('script');
    s.src = EN_DATA_SRC;
    s.onload = applyAll; s.onerror = applyAll;
    document.head.appendChild(s);
  }
  // ================= 第三层：per-tool 全量英文字典（一工具一文件）=================
  // 数据源：i18n/tools/en/<industry>/<slug>.json
  //   结构：{ "slug": "<slug>", "industry": "<ind>", "map": { "<简体原文>": "<英文>" } }
  //   索引：i18n/tools/en/<industry>/_index.json → { "tools": ["<slug>", …] }（只对已有字典的工具发请求，零 404）
  //
  // 设计要点：
  //   1) 文本节点级替换（TreeWalker SHOW_TEXT）：只改文本、不动 DOM 结构，保住 deep-dive 里的
  //      term-link 内链与嵌套标签（既有 translateBodyPhrases 用 el.textContent = tr 会整体覆盖、破坏内链）；
  //   2) [data-zh] 元素（h2 / 首 p，构建期已把英文预渲染进静态 HTML）：以 data-zh 的中文原文为键查表；
  //   3) 在 applyChrome 内最后执行 ⇒ 优先级高于 -body.json 与共享短语表，覆盖其低质 / 未覆盖值；
  //   4) 中文态（zh-CN 与 zh-TW）只还原、不替换。EN_ORIG 精确回写原值 ⇒ 简 ↔ 英 任意切换无损；
  //      繁体页是构建期静态产物（文本为繁体、不走运行时 i18n），同形文本命中则受益、
  //      异形文本保持繁体原文（英文态不作要求），中文态一律完整还原、不破坏繁体页效果。
  var EN_DICT = null;      // 当前工具 { 原文: 英文 }
  var EN_KEY = null;       // '<industry>/<slug>'，防止重复加载
  var EN_INDEX = {};       // { industry: Set<slug> | EMPTY_SET }
  var EN_ORIG = [];        // [{node, orig}] 或 [{el, orig}]，用于精确还原
  var EN_EMPTY_SET = { has: function () { return false; } };

  // 全局通用层：i18n/tools/en/_common.json —— 全站模板句（工具简介 / 常见问题 / 参数说明 …）
  // 单独成层的原因：这类文案在 4779 页重复出现，放进 per-tool 字典会产生数千份冗余；且它们
  // 多为「<h4><span class="h4-icon">📝</span>工具简介</h4>」这种被内层 span 拆开的形态，
  // 既有元素级 textContent 匹配会拼成「📝工具简介」而查不到键 —— 文本节点级匹配正好解决。
  var EN_COMMON = null;
  var EN_COMMON_LOADING = false;

  function loadEnCommon() {
    if (EN_COMMON || EN_COMMON_LOADING || !window.fetch) return Promise.resolve(EN_COMMON);
    EN_COMMON_LOADING = true;
    return fetch(sharedI18nUrl('en/_common.json'))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        EN_COMMON = d || {};
        EN_COMMON_LOADING = false;
        if (isEnglish()) applyEnDict(false);
        return EN_COMMON;
      })
      .catch(function () { EN_COMMON = {}; EN_COMMON_LOADING = false; return EN_COMMON; });
  }

  // 前缀标签字典：i18n/tools/en/_prefix.json —— 专门收纳「固定中文标签 + 变量值」类动态结果串的
  // 标签片段（如 "原始大小：""应用场景：""清理结果（"）。运行时对文本节点做「前缀子串替换」：
  // 当整串精确匹配失败、但文本以某前缀键开头时，只翻译该前缀、变量值原样保留。
  // 与 EN_COMMON 物理隔离 ⇒ 绝不会把通用词（如"分析"）拿去做前缀匹配误伤正文；前缀键一律由
  // 我们显式收录（几乎都带结尾分隔符 ：:（，天然是"标签"形态），零误伤。
  var EN_PREFIX = null;
  var EN_PREFIX_LOADING = false;
  var EN_PREFIX_KEYS = null;   // 排序后的键（长→短），用于 longestPrefixKey 快速匹配
  function loadEnPrefix() {
    if (EN_PREFIX || EN_PREFIX_LOADING || !window.fetch) return Promise.resolve(EN_PREFIX);
    EN_PREFIX_LOADING = true;
    return fetch(sharedI18nUrl('en/_prefix.json'))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        EN_PREFIX = d || {};
        EN_PREFIX_KEYS = Object.keys(EN_PREFIX).sort(function (a, b) { return b.length - a.length; });
        EN_PREFIX_LOADING = false;
        if (isEnglish()) applyEnDict(false);
        return EN_PREFIX;
      })
      .catch(function () { EN_PREFIX = {}; EN_PREFIX_KEYS = []; EN_PREFIX_LOADING = false; return EN_PREFIX; });
  }
  // 边界守卫用：汉字判定（局部声明，不依赖文件后段 HAS_CJK_RE 的声明顺序）
  var PREFIX_CJK_RE = /[\u4e00-\u9fff]/;
  // 返回文本最长的、可作为前缀命中的键（文本以该键开头，含"文本节点恰等于该键"的孤立标签形态）；无则 null
  // 边界守卫（2026-09-30）：命中键后若**紧跟汉字** ⇒ 该键只是更长中文词的开头（"质量分数"里的"质量"、
  // "时间管理"里的"时间"），它不是标签，必须跳过，否则把词劈成两半产出 "Mass分数" / "Time 管理"。
  // 只有键后是空白/数字/拉丁/标点/串尾才算真标签边界。副作用为零：真正完整的译文键后必是边界，
  // 恒不被拦（全站实测 541 例半译串因此转为干净中文残留，无一处正确译文被丢）。
  function longestPrefixKey(text) {
    if (!EN_PREFIX_KEYS || !text) return null;
    for (var i = 0; i < EN_PREFIX_KEYS.length; i++) {
      var k = EN_PREFIX_KEYS[i];
      if (text.length < k.length || text.indexOf(k) !== 0) continue;
      if (text.length > k.length && PREFIX_CJK_RE.test(text.charAt(k.length))) continue;
      return k;
    }
    return null;
  }
  // 子串级前缀匹配（全量）：把文本「任意位置」出现的所有「带全角冒号：的标签键」一次性译掉。
  // 双语混合结果串如 "Asset-liability ratio:55% | 流动比率：1.8 | 收入：5000万 | 净利润率：12%"
  // 里多个中文标签分散在中间，单次只替一个键会漏掉其余 ⇒ 这里循环替到无可替为止，变量值原样保留。
  // 只匹配以 "：" 结尾的键 ⇒ 天然是「标签：」形态，正文叙述极少用全角冒号紧跟中文值，误伤概率极低；
  // 英文译文用半角 ":" 不含全角冒号 ⇒ 替换结果不会再被同一键命中，循环必然收敛（另加 guard 兜底）。
  // 普通不带冒号的前缀键仍只走 longestPrefixKey 的开头匹配，不受影响。
  // 边界守卫（2026-09-30）：命中的「…：」若**前一位仍是汉字** ⇒ 它只是更长中文词的尾巴
  // （"网度换算："里的"换算："、"水溶液沸点判定："里的"判定："），跳过该处命中，否则同样劈词。
  function replaceColonLabelsAll(text) {
    if (!EN_PREFIX_KEYS || !text) return null;
    var out = text, changed = false, guard = 0;
    while (guard++ < 40) {
      var hit = null, at = -1;
      for (var i = 0; i < EN_PREFIX_KEYS.length; i++) {
        var k = EN_PREFIX_KEYS[i];
        if (k.charAt(k.length - 1) !== '：') continue;
        var p = out.indexOf(k);
        while (p > 0 && PREFIX_CJK_RE.test(out.charAt(p - 1))) p = out.indexOf(k, p + 1);
        if (p >= 0) { hit = k; at = p; break; }
      }
      if (!hit) break;
      out = out.slice(0, at) + EN_PREFIX[hit] + out.slice(at + hit.length);
      changed = true;
    }
    return changed ? out : null;
  }

  function loadEnIndex(ind) {
    if (EN_INDEX[ind]) return Promise.resolve(EN_INDEX[ind]);
    if (!window.fetch) { EN_INDEX[ind] = EN_EMPTY_SET; return Promise.resolve(EN_EMPTY_SET); }
    return fetch(sharedI18nUrl('en/' + ind + '/_index.json'))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        EN_INDEX[ind] = new Set((d && d.tools) || []);
        return EN_INDEX[ind];
      })
      .catch(function () { EN_INDEX[ind] = EN_EMPTY_SET; return EN_EMPTY_SET; });
  }

  function loadEnDict(ind, slug) {
    loadEnCommon();       // 全局通用层随之加载（独立于本工具是否已有字典）
    loadEnPrefix();       // 前缀标签层随之加载（覆盖"标签+变量"动态结果串）
    if (!ind || !slug || !window.fetch) return;
    var key = ind + '/' + slug;
    if (EN_KEY === key) return;      // 已加载 / 加载中，避免重复请求
    EN_KEY = key;
    loadEnIndex(ind).then(function (set) {
      if (!set || !set.has(slug)) return;
      fetch(sharedI18nUrl('en/' + ind + '/' + slug + '.json'), { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!d || !d.map) return;
          EN_DICT = d.map;
          if (isEnglish()) applyChrome();   // 重跑全流程 ⇒ 第三层依旧最后落地
        })
        .catch(function () { /* 字典缺失：忽略，回退既有机制 */ });
    });
  }

  // 语言切换器内部（简体中文/繁體中文/English 等语言名）按惯例用本语言显示，不翻译
  function isExcludedEl(el) {
    var c = el;
    while (c && c.nodeName && c.nodeName.toLowerCase() !== 'body') {
      var cls = (c.getAttribute && c.getAttribute('class')) || '';
      if (/(^|\s)lang-switcher(\s|$)/.test(cls)) return true;
      c = c.parentNode;
    }
    return false;
  }

  function restoreEn() {
    for (var i = 0; i < EN_ORIG.length; i++) {
      var it = EN_ORIG[i];
      if (it.node) { if (it.node.parentNode) it.node.nodeValue = it.orig; }
      else if (it.el && it.attr) { if (it.el.parentNode) it.el.setAttribute(it.attr, it.orig); }
      else if (it.el) { it.el.textContent = it.orig; }
    }
    EN_ORIG = [];
  }

  // 查表：per-tool 字典优先（更具体），全局通用层兜底
  function pickEn(key) {
    if (EN_DICT && EN_DICT[key]) return EN_DICT[key];
    if (EN_COMMON && EN_COMMON[key]) return EN_COMMON[key];
    return null;
  }

  // ---- 纯中文标点节点：字符级转换 ----
  // 中文标点常以「孤立文本节点」出现（如 <b>加密</b>：<code>x</code> 的「：」、<code>x</code>。</p> 的「。」），
  // 且存在组合形态（「）。」「），」…）无法用全等查表穷举 ⇒ 对「整节点仅由中文标点构成」的节点按字符映射。
  // 判据严格（不含字母/数字/汉字），因此绝不会触碰正文文字，零误伤。
  var PUNCT_CHAR = {
    '：': ': ', '，': ', ', '、': ', ', '；': '; ', '。': '.',
    '！': '!', '？': '?', '）': ')', '（': '(', '「': '"', '」': '"'
  };
  var PUNCT_HAS_RE = /[\u3002\uFF0C\u3001\uFF1B\uFF1A\uFF01\uFF1F\u300C\u300D\uFF08\uFF09]/;
  var HAS_CJK_RE = /[\u4e00-\u9fff]/;
  function convertPunct(s) {
    // 含中文标点、且不含任何汉字 ⇒ 视为「标点载体节点」（可能夹带数字/代码，如 “=65、”“=97）。”“：”）。
    // 含汉字的节点一律不碰，由 per-tool 字典按整句翻译。
    if (!PUNCT_HAS_RE.test(s) || HAS_CJK_RE.test(s)) return null;
    var out = '';
    for (var i = 0; i < s.length; i++) {
      var c = s.charAt(i);
      out += PUNCT_CHAR[c] || c;
    }
    return out === s ? null : out;
  }

  function applyEnDict(isZh) {
    restoreEn();
    if (isZh || (!EN_DICT && !EN_COMMON)) { stopDynObserver(); return; }

    // (a) [data-zh]：英文态下静态文本已是构建期预渲染的英文，中文原文保存在 data-zh
    var dzs = document.querySelectorAll('[data-zh]');
    for (var i = 0; i < dzs.length; i++) {
      if (dzs[i].children && dzs[i].children.length) continue;   // 只处理纯文本元素，不动结构
      var zh = dzs[i].getAttribute('data-zh');
      if (!zh) continue;
      var tr = pickEn(zh);
      if (!tr) continue;
      EN_ORIG.push({ el: dzs[i], orig: dzs[i].textContent });
      dzs[i].textContent = tr;
    }

    // (b) 可见文本节点级替换（保留 DOM 结构与内链）
    var root = document.body || document.documentElement;
    var NF = window.NodeFilter;
    if (!root || !document.createTreeWalker || !NF) return;
    var walker = document.createTreeWalker(root, NF.SHOW_TEXT, null, false);
    var n;
    while ((n = walker.nextNode())) {
      var parent = n.parentNode;
      if (!parent) continue;
      var tag = (parent.nodeName || '').toUpperCase();
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
      var raw = n.nodeValue;
      if (!raw) continue;
      var k = raw.trim();
      if (!k) continue;
      var matchedKey = k;
      var en = pickEn(k);
      if (!en) {
        // ① 全量替换：把串中「任意位置」的所有「标签：」片段一次译清（含串首标签 + 中间多标签的
        //    双语混合结果串）。必须排在 longestPrefixKey 之前 —— 否则串首恰为已知标签时会走串首
        //    单次分支，只译第一个、漏掉串中其余标签。
        var all = replaceColonLabelsAll(k);
        if (all) { en = all; }
        else {
          // ② 非冒号前缀标签（149 条短标签）仅在串首命中
          var pf = longestPrefixKey(k);
          if (pf) { matchedKey = pf; en = EN_PREFIX[pf]; }
        }
      }
      if (!en) en = convertPunct(k);
      if (!en || en === k) continue;
      var idx = raw.indexOf(matchedKey);
      EN_ORIG.push({ node: n, orig: raw });
      n.nodeValue = raw.slice(0, idx) + en + raw.slice(idx + matchedKey.length);
    }

    // (c) 元素属性翻译（placeholder / title / aria-label / alt）：属性不是文本节点，
    // 文本节点级替换（(b)）与 translateGenericUI（el.textContent）都碰不到，
    // 此前全站英文态这些属性里的汉字永远不翻译（最典型：输入框 placeholder、面包屑 nav aria-label）。
    // 与 (b) 共用同一套 per-tool 字典 + 全局 _common 兜底，精确匹配才替换 ⇒ 零误伤；
    // 原文存入 EN_ORIG，中文态精确还原。不翻译 value（表单控件逻辑值，如分隔符 "," 不能动）。
    var ATTR_KEYS = ['placeholder', 'title', 'aria-label', 'alt'];
    var attrEls = document.querySelectorAll('[placeholder],[title],[aria-label],[alt]');
    for (var ai = 0; ai < attrEls.length; ai++) {
      var ae = attrEls[ai];
      if (isExcludedEl(ae)) continue;
      for (var ak = 0; ak < ATTR_KEYS.length; ak++) {
        var aName = ATTR_KEYS[ak];
        var aVal = ae.getAttribute(aName);
        if (!aVal) continue;
        var aValT = aVal.trim();
        var aTr = pickEn(aValT);
        if (!aTr) {
          // ① 全量替换「标签：」片段（title="五险一金: ¥4,500.00" 等「标签+值」），值原样保留
          var aAll = replaceColonLabelsAll(aValT);
          if (aAll) aTr = aAll;
          else {
            // ② 非冒号前缀标签仅在串首命中
            var apf = longestPrefixKey(aValT);
            if (apf) aTr = EN_PREFIX[apf];
          }
        }
        if (!aTr || aTr === aVal) continue;
        EN_ORIG.push({ el: ae, attr: aName, orig: aVal });
        ae.setAttribute(aName, aTr);
      }
    }

    // (d) 开启动态节点增量翻译：覆盖「本次全量扫描之后才插入」的内容
    startDynObserver();
  }

  // ---- (d) 动态节点增量翻译（MutationObserver）----
  // 站点大量内容是「翻译被执行之后才注入 DOM」的：tool-page-runtime 的「复制结果/导出 TXT/试算示例」
  // 按钮、工具页内联 JS 渲染的结果标签与预设名、hot 组件后续重绘等。(a)(b)(c) 是一次性全量扫描，
  // 结构上覆盖不到后插入的节点 ⇒ 英文态长期残留中文，且字典里其实有译文也白搭。
  // 这里在英文态下对新增节点做增量翻译，复用同一套字典 / 同一套排除规则 / 同一个 EN_ORIG：
  //   · 译好的节点再次进来时 pickEn 不命中 ⇒ 自然收敛，不会自我循环放大；
  //   · applying 抑制位挡掉「我们自己的写入」触发的二次回调；
  //   · 切回中文时 stopDynObserver + restoreEn 逐项精确还原，与静态还原口径一致。
  var ATTR_KEYS_DYN = ['placeholder', 'title', 'aria-label', 'alt'];
  var dynObs = null;
  var dynApplying = false;

  function dynTranslateNode(node) {
    if (!node) return;
    if (node.nodeType === 3) {
      var parent = node.parentNode;
      if (!parent) return;
      var tg = (parent.nodeName || '').toUpperCase();
      if (tg === 'SCRIPT' || tg === 'STYLE' || tg === 'NOSCRIPT') return;
      if (isExcludedEl(parent)) return;
      var raw = node.nodeValue;
      if (!raw) return;
      var key = raw.trim();
      if (!key) return;
      var matchedKey = key;
      var out = pickEn(key);
      if (!out) {
        // 全量替换优先（含串首标签 + 中间多标签），非冒号前缀标签兜底
        var all2 = replaceColonLabelsAll(key);
        if (all2) { out = all2; }
        else {
          var pf = longestPrefixKey(key);
          if (pf) { matchedKey = pf; out = EN_PREFIX[pf]; }
        }
      }
      if (!out) out = convertPunct(key);
      if (!out || out === key) return;
      var at = raw.indexOf(matchedKey);
      EN_ORIG.push({ node: node, orig: raw });
      node.nodeValue = raw.slice(0, at) + out + raw.slice(at + matchedKey.length);
      return;
    }
    if (node.nodeType !== 1) return;
    var tagName = (node.nodeName || '').toUpperCase();
    if (tagName === 'SCRIPT' || tagName === 'STYLE' || tagName === 'NOSCRIPT') return;
    if (isExcludedEl(node)) return;
    for (var i = 0; i < ATTR_KEYS_DYN.length; i++) {
      var an = ATTR_KEYS_DYN[i];
      var av = node.getAttribute(an);
      if (!av) continue;
      var avT = av.trim();
      var tv = pickEn(avT);
      if (!tv) {
        var avAll = replaceColonLabelsAll(avT);
        if (avAll) tv = avAll;
        else {
          var avpf = longestPrefixKey(avT);
          if (avpf) tv = EN_PREFIX[avpf];
        }
      }
      if (!tv || tv === av) continue;
      EN_ORIG.push({ el: node, attr: an, orig: av });
      node.setAttribute(an, tv);
    }
  }

  function dynTranslateSubtree(node) {
    if (!node) return;
    dynTranslateNode(node);
    if (node.nodeType === 1 && node.childNodes) {
      // 子节点集合是 live 的，先快照再遍历，避免翻译时的写入造成索引漂移
      var kids = Array.prototype.slice.call(node.childNodes, 0);
      for (var i = 0; i < kids.length; i++) dynTranslateSubtree(kids[i]);
    }
  }

  function startDynObserver() {
    if (dynObs || typeof MutationObserver === 'undefined') return;
    var root = document.body || document.documentElement;
    if (!root) return;
    dynObs = new MutationObserver(function (records) {
      if (dynApplying || !isEnglish()) return;
      dynApplying = true;
      try {
        for (var i = 0; i < records.length; i++) {
          var rec = records[i];
          var added = rec.addedNodes;
          if (added && added.length) {
            for (var j = 0; j < added.length; j++) dynTranslateSubtree(added[j]);
          }
          if (rec.type === 'attributes' && rec.target) dynTranslateNode(rec.target);
        }
      } catch (e) { /* 单个节点异常不影响整页翻译 */ }
      // MutationObserver 回调是微任务，这里放到下一个宏任务再解锁，
      // 确保「我们自己的写入」所产生的记录在同一抑制窗口内被跳过。
      setTimeout(function () { dynApplying = false; }, 0);
    });
    dynObs.observe(root, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ATTR_KEYS_DYN
    });
  }

  function stopDynObserver() {
    if (!dynObs) return;
    dynObs.disconnect();
    dynObs = null;
    dynApplying = false;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  // 【事件目标 bug 修复 2026-09-29】i18n.js 的 set() 在 window 上 dispatch('toolbox:langchange')
  // （Event 默认不冒泡、target 为 window），挂在 document 上的监听器永远收不到 ⇒
  // 切换语言后 applyAll 从不触发，内容区停留原语言，用户必须手动刷新才生效（老板实测投诉）。
  // 修复：改挂 window，与 i18n.js 的派发目标一致（common.js 同事件也是 window 监听）。
  window.addEventListener('toolbox:langchange', onLangChange);
})();
