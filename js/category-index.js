/*
 * category-index.js —— 分类落地页工具列表「JSON 增强」
 *
 * 背景：分类页原本把本行业全部工具卡片（含英文描述长文本）内联进 HTML，
 * 单页最大 ~256KB、276 个分类页合计 ~5.7MB。改为构建期只内联轻量静态链接
 * （href + 中文名 + 中文描述，保证 SEO 锚文本与可见描述；繁体页由 OpenCC 自动转繁体），
 * 运行时本脚本 fetch /json/industry-<ind>.json，按 file slug 匹配，把链接增强为富卡片
 * （图标 + 中文名[静态已转繁体] + 英文名 + 中文描述[静态] + 英文描述，均取自 json）。
 *
 * SEO：静态链接 + 中文名 + 中文描述始终在 HTML 中（Google 无需执行 JS 即可抓取）；
 * 本脚本仅在 JS 可用时做视觉增强，失败则保留静态链接，不影响可读性与索引。
 */
(function () {
  'use strict';
  var lists = document.querySelectorAll('.category-tool-list[data-ind]');
  if (!lists.length) return;

  var cache = {};
  function load(ind) {
    if (cache[ind]) return cache[ind];
    cache[ind] = fetch('/json/industry-' + ind + '.json', { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : []; })
      .catch(function () { return []; });
    return cache[ind];
  }

  function slugOf(href) {
    var m = (href || '').split('/').pop();
    return m.replace(/\.html$/, '');
  }

  function enhance(a, rec) {
    var zhNameEl = a.querySelector('.t-zh');
    var zhDescEl = a.querySelector('.t-zh-desc');
    // 中文名/描述来自静态 DOM（繁体页已被 OpenCC 转繁体），增强时不覆盖，保持繁体一致
    var zhName = zhNameEl ? zhNameEl.textContent : (a.getAttribute('data-zh') || '');
    var zhDesc = zhDescEl ? zhDescEl.textContent : (a.getAttribute('data-zhdesc') || '');
    var icon = (rec && rec.icon) || '🔧';
    var enName = (rec && rec.en) || '';
    var enDesc = (rec && rec.ed) || '';
    a.classList.add('tb-megapanel-tool-card');
    a.innerHTML =
      '<span class="tb-tool-icon" style="background:#f5f5f5">' + icon + '</span>' +
      '<span class="tb-tool-body">' +
        '<span class="tb-tool-name"><span class="t-zh">' + zhName + '</span><span class="t-en">' + enName + '</span></span>' +
        '<span class="tb-tool-desc"><span class="t-zh">' + zhDesc + '</span><span class="t-en">' + enDesc + '</span></span>' +
      '</span>';
  }

  for (var i = 0; i < lists.length; i++) {
    (function (list) {
      var ind = list.getAttribute('data-ind');
      load(ind).then(function (arr) {
        var map = {};
        if (arr) {
          for (var k = 0; k < arr.length; k++) {
            var t = arr[k];
            if (t && t.file) map[String(t.file).replace(/\.html$/, '')] = t;
          }
        }
        var links = list.querySelectorAll('a.cat-tool');
        for (var j = 0; j < links.length; j++) {
          enhance(links[j], map[slugOf(links[j].getAttribute('href'))] || {});
        }
      });
    })(lists[i]);
  }
})();
