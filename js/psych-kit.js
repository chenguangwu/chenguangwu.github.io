/* psych-kit.js — 心理/临床量表页面统一增强运行时
 * 纯前端：进度条、首次说明卡、未答确认、分级颜色徽章、高危求助热线横幅、
 * 复制结果摘要、结果保存为图片、localStorage 本地暂存、深色模式适配。
 * 全程浏览器本地运行，无任何网络请求与数据上传。
 */
(function () {
  'use strict';

  var S = document.querySelector('script[data-psych]');
  var CFG = {};
  try { CFG = JSON.parse(S ? (S.getAttribute('data-psych') || '{}') : '{}') || {}; } catch (e) { CFG = {}; }

  var KEY = CFG.key || (location.pathname.split('/').pop() || 'tool').replace(/\.html$/, '');
  var NAME = CFG.name || '';
  var KIND = CFG.kind || 'clinical';           // clinical | entertainment
  var MINUTES = CFG.minutes || 3;
  var RISK = CFG.risk || null;                 // {score_gte, item_gte:[idx,min], text_any:[...]}
  var NOTE = CFG.note || '';                   // 娱乐/参考类标识文案
  var PERIOD = CFG.period || '最近两周';        // 说明卡中的回溯期

  var LS_INTRO = 'pk:intro:' + KEY;
  var LS_ANS = 'pk:ans:' + KEY;
  var MAX_AGE = 24 * 3600 * 1000;

  var restoring = false;
  var lastScore = null;
  var lastLevel = null;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function lsGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { } }
  function lsDel(k) { try { window.localStorage.removeItem(k); } catch (e) { } }

  var LEVELS = [
    { key: 'severe', kw: ['极重度', '重度', '严重', '高危', '阳性', '显著'], color: '#dc2626', label: '重度/高危' },
    { key: 'moderate', kw: ['中重度', '中度', '中等'], color: '#ea580c', label: '中度' },
    { key: 'mild', kw: ['轻度', '关注', '边缘', '可疑'], color: '#ca8a04', label: '轻度/关注' },
    { key: 'none', kw: ['无', '阴性', '正常', '低危', '极低', '未达'], color: '#16a34a', label: '正常/低危' }
  ];

  function matchLevel(text) {
    var t = String(text || '');
    for (var i = 0; i < LEVELS.length; i++) {
      for (var j = 0; j < LEVELS[i].kw.length; j++) {
        if (t.indexOf(LEVELS[i].kw[j]) >= 0) return LEVELS[i];
      }
    }
    return null;
  }

  /* ---------------- 样式 ---------------- */
  var CSS = [
    '.pk-wrap{margin:0 0 14px;}',
    '.pk-progress{position:sticky;top:0;z-index:5;background:var(--card-bg,#fff);border:1px solid var(--border,#E5E7EB);border-radius:14px;padding:10px 12px;box-shadow:0 2px 8px rgba(0,0,0,.04);}',
    '.pk-progress-head{display:flex;justify-content:space-between;align-items:center;font-size:14px;color:var(--text-secondary,#6B7280);margin-bottom:8px;}',
    '.pk-progress-head b{color:var(--text-primary,#1F2937);font-size:15px;}',
    '.pk-dots{display:flex;flex-wrap:wrap;gap:4px;}',
    '.pk-dot{flex:1 1 0;min-width:8px;height:6px;border-radius:999px;background:var(--border,#E5E7EB);transition:background .2s;}',
    '.pk-dot.on{background:var(--color-primary,#FF6B35);}',
    '.pk-dot.cur{background:#FFB38A;}',
    '.pk-bar{height:6px;border-radius:999px;background:var(--border,#E5E7EB);overflow:hidden;margin-top:8px;}',
    '.pk-bar > i{display:block;height:100%;background:linear-gradient(90deg,#FF6B35,#7C3AED);transition:width .25s;}',
    '.pk-intro{border:1px solid var(--border,#E5E7EB);border-radius:16px;padding:18px;background:var(--card-bg,#fff);box-shadow:0 2px 10px rgba(0,0,0,.04);}',
    '.pk-intro h4{margin:0 0 10px;font-size:17px;color:var(--text-primary,#1F2937);}',
    '.pk-intro ul{margin:0 0 14px;padding-left:20px;font-size:15px;line-height:1.8;color:var(--text-secondary,#4B5563);}',
    '.pk-intro .pk-btn{min-width:140px;}',
    '.pk-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:12px;border:1px solid var(--border,#E5E7EB);background:var(--card-bg,#fff);color:var(--text-primary,#1F2937);font-size:15px;cursor:pointer;}',
    '.pk-btn.primary{background:linear-gradient(135deg,#FF6B35,#7C3AED);color:#fff;border-color:transparent;}',
    '.pk-btn.ghost{background:transparent;}',
    '.pk-resume{border:1px solid #FCD34D;background:rgba(245,158,11,.10);border-radius:14px;padding:12px;margin:0 0 12px;font-size:14px;color:#92400E;display:flex;flex-wrap:wrap;gap:8px;align-items:center;}',
    '.pk-hotline{border:1px solid #FDBA74;background:rgba(249,115,22,.12);border-radius:14px;padding:14px;margin:0 0 12px;font-size:15px;line-height:1.8;color:#9A3412;}',
    '.pk-hotline .pk-hl-title{font-weight:700;display:block;margin-bottom:4px;}',
    '.pk-hotline a{color:#C2410C;font-weight:700;text-decoration:underline;}',
    '.pk-badge{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:999px;color:#fff;font-size:14px;font-weight:600;}',
    '.pk-score{font-size:30px;font-weight:800;line-height:1.1;}',
    '.pk-scorecard{border:1px solid var(--border,#E5E7EB);border-radius:16px;padding:16px;margin:0 0 12px;background:var(--card-bg,#fff);}',
    '.pk-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px;}',
    '.pk-modal{position:fixed;inset:0;z-index:120;display:flex;align-items:center;justify-content:center;background:rgba(17,24,39,.55);padding:16px;}',
    '.pk-modal-card{width:100%;max-width:460px;max-height:88vh;overflow:auto;background:var(--card-bg,#fff);border-radius:20px;padding:20px;box-shadow:0 18px 46px rgba(0,0,0,.22);}',
    '.pk-modal-card h4{margin:0 0 10px;font-size:17px;color:var(--text-primary,#1F2937);}',
    '.pk-modal-card p{margin:0 0 12px;font-size:15px;line-height:1.75;color:var(--text-secondary,#4B5563);}',
    '.pk-modal-nums{font-size:14px;color:var(--text-secondary,#6B7280);background:rgba(0,0,0,.04);border-radius:12px;padding:10px;margin-bottom:14px;line-height:1.8;}',
    '.pk-modal-actions{display:flex;flex-wrap:wrap;gap:10px;}',
    '.pk-tag{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;font-size:14px;font-weight:600;background:rgba(124,58,237,.10);color:#6D28D9;border:1px solid rgba(124,58,237,.25);}',
    '.pk-hidden{display:none !important;}',
    '@media (max-width:640px){',
    '  .pk-actions .pk-btn{flex:1 1 100%;}',
    '  .q-opt,.pk-opt{min-height:44px;display:inline-flex;align-items:center;justify-content:center;padding:0 14px;}',
    '  .q-title{font-size:16px !important;line-height:1.7 !important;}',
    '  .toolbar{display:flex !important;flex-direction:column !important;gap:10px;}',
    '  .toolbar .btn,.toolbar button{min-height:44px;width:100%;}',
    '}',
    '@media (max-width:768px){',
    '  .result-box table,.pk-result table,.result-box + table{display:block;width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;}',
    '  .result-box td,.result-box th{white-space:normal;word-break:break-word;}',
    '}',
    '[data-theme="dark"] .pk-progress,[data-theme="dark"] .pk-intro,[data-theme="dark"] .pk-scorecard{background:#252540;border-color:#3A3A5C;}',
    '[data-theme="dark"] .pk-hotline{background:rgba(249,115,22,.20);border-color:#B45309;color:#FDBA74;}',
    '[data-theme="dark"] .pk-hotline a{color:#FED7AA;}',
    '[data-theme="dark"] .pk-resume{background:rgba(245,158,11,.16);color:#FCD34D;}',
    '[data-theme="dark"] .pk-btn{background:#252540;border-color:#3A3A5C;color:#E5E7EB;}',
    '[data-theme="dark"] .pk-modal-card{background:#252540;}',
    '[data-theme="dark"] .pk-tag{background:rgba(167,139,250,.16);color:#DDD6FE;border-color:rgba(167,139,250,.35);}',
    '@media (prefers-color-scheme: dark){',
    '  html:not([data-theme="light"]) .pk-progress,html:not([data-theme="light"]) .pk-intro,html:not([data-theme="light"]) .pk-scorecard{background:#252540;border-color:#3A3A5C;}',
    '  html:not([data-theme="light"]) .pk-hotline{background:rgba(249,115,22,.20);border-color:#B45309;color:#FDBA74;}',
    '  html:not([data-theme="light"]) .pk-hotline a{color:#FED7AA;}',
    '  html:not([data-theme="light"]) .pk-btn{background:#252540;border-color:#3A3A5C;color:#E5E7EB;}',
    '}'
  ].join('\n');

  function injectStyles() {
    if (document.getElementById('pk-kit-css')) return;
    var st = document.createElement('style');
    st.id = 'pk-kit-css';
    st.textContent = CSS;
    document.head.appendChild(st);
  }

  /* ---------------- DOM 探测 ---------------- */
  function resultEl() {
    return $('#result') || $('.result-box') || $('#res') || $('.result') || null;
  }
  function optRows() { return $$('.q-opts'); }
  function items() { return $$('#quiz .q-item').length ? $$('#quiz .q-item') : $$('.q-item'); }
  function readAnswers() {
    return optRows().map(function (row) {
      var opts = $$('.q-opt', row), idx = -1;
      opts.forEach(function (o, i) {
        if (o.classList.contains('active') || o.getAttribute('aria-checked') === 'true') idx = i;
      });
      return idx;
    });
  }
  function answeredItemCount() {
    var its = items(), n = 0;
    its.forEach(function (it) {
      var rows = $$('.q-opts', it);
      if (!rows.length) return;
      var ok = rows.every(function (r) { return !!$('.q-opt.active', r); });
      if (ok) n++;
    });
    return n;
  }

  /* ---------------- 进度条 ---------------- */
  function buildProgress() {
    var its = items();
    if (!its.length) return null;
    var host = $('#quiz') || its[0].parentNode;
    if (!host || $('#pk-progress')) return $('#pk-progress');
    var wrap = document.createElement('div');
    wrap.className = 'pk-wrap';
    wrap.id = 'pk-progress';
    var n = its.length;
    var dots = '';
    for (var di = 0; di < n; di++) dots += '<span class="pk-dot"></span>';
    wrap.innerHTML =
      '<div class="pk-progress">' +
      '  <div class="pk-progress-head"><span>进度 <b id="pk-cur">1</b> / ' + n + ' 题</span><span id="pk-done">已答 0 题</span></div>' +
      '  <div class="pk-dots">' + dots + '</div>' +
      '  <div class="pk-bar"><i id="pk-barfill" style="width:0%"></i></div>' +
      '</div>';
    host.parentNode.insertBefore(wrap, host);
    updateProgress();
    return wrap;
  }

  function updateProgress() {
    var its = items();
    if (!its.length) return;
    var n = its.length;
    var done = [];
    its.forEach(function (it) {
      var rows = $$('.q-opts', it);
      var ok = rows.length ? rows.every(function (r) { return !!$('.q-opt.active', r); }) : false;
      done.push(ok);
    });
    var c = done.filter(Boolean).length;
    var cur = n;
    for (var i = 0; i < n; i++) { if (!done[i]) { cur = i + 1; break; } }
    var elc = $('#pk-cur'); if (elc) elc.textContent = cur;
    var eld = $('#pk-done'); if (eld) eld.textContent = '已答 ' + c + ' 题';
    var dots = $$('.pk-dot');
    dots.forEach(function (d, i) {
      d.classList.toggle('on', !!done[i]);
      d.classList.toggle('cur', !done[i] && i === cur - 1);
    });
    var bf = $('#pk-barfill');
    if (bf) bf.style.width = Math.round(c / n * 100) + '%';
  }

  /* ---------------- 首次说明卡 ---------------- */
  function buildIntro() {
    var its = items();
    if (!its.length) return;
    var host = $('#quiz') || its[0].parentNode;
    if (!host || $('#pk-intro')) return;
    var seen = lsGet(LS_INTRO) === '1';
    var card = document.createElement('div');
    card.className = 'pk-wrap' + (seen ? ' pk-hidden' : '');
    card.id = 'pk-intro';
    var kindLine = KIND === 'clinical'
      ? '<li>本量表为自助筛查工具，约需 ' + MINUTES + ' 分钟完成。</li>'
      : '<li>本测试约需 ' + MINUTES + ' 分钟完成。</li>';
    card.innerHTML =
      '<div class="pk-intro">' +
      '  <h4>📋 开始前的说明</h4>' +
      '  <ul>' + kindLine +
      '    <li>答案无对错，请按' + PERIOD + '的真实感受选择。</li>' +
      '    <li>结果仅作参考，不构成诊断；所有数据仅在您的设备本地处理。</li>' +
      '  </ul>' +
      '  <button type="button" class="pk-btn primary" id="pk-start">开始作答</button>' +
      '</div>';
    host.parentNode.insertBefore(card, host);
    if (!seen) host.classList.add('pk-hidden');
    var btn = $('#pk-start');
    if (btn) btn.addEventListener('click', function () {
      lsSet(LS_INTRO, '1');
      host.classList.remove('pk-hidden');
      card.classList.add('pk-hidden');
      try { host.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch (e) { }
    });
  }

  /* ---------------- 本地暂存与恢复 ---------------- */
  function saveAnswers() {
    if (restoring) return;
    var a = readAnswers();
    if (!a.length) return;
    var any = a.some(function (v) { return v >= 0; });
    if (!any) { lsDel(LS_ANS); return; }
    lsSet(LS_ANS, JSON.stringify({ t: Date.now(), a: a }));
  }

  function buildResume() {
    var raw = lsGet(LS_ANS);
    if (!raw) return;
    var d = null;
    try { d = JSON.parse(raw); } catch (e) { return; }
    if (!d || !d.a || !d.a.some(function (v) { return v >= 0; })) return;
    if (Date.now() - d.t > MAX_AGE) { lsDel(LS_ANS); return; }
    var mins = Math.max(1, Math.round((Date.now() - d.t) / 60000));
    var mtxt = mins < 60 ? mins + ' 分钟前' : Math.round(mins / 60) + ' 小时前';
    var host = $('#quiz') || (items()[0] && items()[0].parentNode);
    if (!host || $('#pk-resume')) return;
    var box = document.createElement('div');
    box.id = 'pk-resume';
    box.className = 'pk-resume';
    box.innerHTML = '<span>检测到 ' + mtxt + ' 未完成的评估记录（仅保存在本机）。是否继续？</span>' +
      '<button type="button" class="pk-btn primary" id="pk-keep">继续作答</button>' +
      '<button type="button" class="pk-btn ghost" id="pk-drop">重新开始</button>';
    host.parentNode.insertBefore(box, host);
    $('#pk-keep').addEventListener('click', function () {
      restoring = true;
      var rows = optRows();
      d.a.forEach(function (v, i) {
        if (v >= 0 && rows[i]) {
          var os = $$('.q-opt', rows[i]);
          if (os[v]) { try { os[v].click(); } catch (e) { } }
        }
      });
      restoring = false;
      updateProgress();
      recalc();
      box.parentNode.removeChild(box);
    });
    $('#pk-drop').addEventListener('click', function () {
      lsDel(LS_ANS);
      box.parentNode.removeChild(box);
    });
  }

  function recalc() { try { if (typeof window.calc === 'function') window.calc(); } catch (e) { } }

  /* ---------------- 未答确认弹窗 ---------------- */
  function missingList() {
    var its = items(), miss = [];
    its.forEach(function (it, i) {
      var rows = $$('.q-opts', it);
      var ok = rows.length ? rows.every(function (r) { return !!$('.q-opt.active', r); }) : true;
      if (!ok) miss.push(i + 1);
    });
    return miss;
  }

  function confirmModal(miss, onOk) {
    var m = document.createElement('div');
    m.className = 'pk-modal';
    var shown = miss.slice(0, 30).join('、') + (miss.length > 30 ? ' 等' : '');
    m.innerHTML =
      '<div class="pk-modal-card" role="dialog" aria-modal="true">' +
      '  <h4>⚠️ 还有 ' + miss.length + ' 题未作答</h4>' +
      '  <p>未作答的题目：<span class="pk-modal-nums" style="display:inline;">' + shown + '</span></p>' +
      '  <p>确定用当前答案计算吗？未答题目不会按 0 分处理，结果可能偏低。</p>' +
      '  <div class="pk-modal-actions">' +
      '    <button type="button" class="pk-btn primary" id="pk-ok">确定计算</button>' +
      '    <button type="button" class="pk-btn ghost" id="pk-cancel">继续作答</button>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(m);
    $('#pk-ok').addEventListener('click', function () { m.parentNode.removeChild(m); onOk(); });
    $('#pk-cancel').addEventListener('click', function () { m.parentNode.removeChild(m); });
  }

  function wrapCalc() {
    // 包装页面全局 calc，使其在评分后主动触发结果增强（不依赖 MutationObserver）
    try {
      if (typeof window.calc === 'function' && !window.__pk_calc_wrapped) {
        var _c = window.calc;
        window.__pk_calc_wrapped = true;
        window.calc = function () {
          var r = _c.apply(this, arguments);
          setTimeout(enhanceResult, 0);
          return r;
        };
      }
    } catch (e) { }
  }

  function hookSubmit() {
    wrapCalc();
    var btns = $$('button, .btn').filter(function (b) {
      var oc = b.getAttribute('onclick') || '';
      return /calc\s*\(|计算|评估|评分|结果/.test(oc + b.textContent);
    });
    btns.forEach(function (b) {
      if (b.getAttribute('data-pk-hooked') === '1') return;
      b.setAttribute('data-pk-hooked', '1');
      b.addEventListener('click', function (e) {
        var miss = missingList();
        if (!miss.length) {                    // 全部作答 → 放行，calc 后增强
          setTimeout(enhanceResult, 30);
          return;
        }
        var rows = optRows();
        var answered = readAnswers().filter(function (v) { return v >= 0; }).length;
        if (!rows.length || answered === 0) {  // 结构不符或一题未答 → 不拦截
          setTimeout(enhanceResult, 30);
          return;
        }
        e.preventDefault();
        e.stopImmediatePropagation();
        confirmModal(miss, function () {
          try { if (typeof window.calc === 'function') window.calc(); else b.click(); } catch (err) { }
          setTimeout(enhanceResult, 30);
        });
      }, true);
    });
  }

  /* ---------------- 结果增强 ---------------- */
  function parseScore(text) {
    var m = String(text || '').match(/总分[^\d\-]{0,12}(\d+)/);
    if (m) return parseInt(m[1], 10);
    var v = $('.stat-card .val', resultEl());
    if (v) { var m2 = v.textContent.match(/(\d+)/); if (m2) return parseInt(m2[1], 10); }
    return null;
  }

  function hotlineHtml() {
    return '<div class="pk-hotline"><span class="pk-hl-title">🆘 本次结果提示存在较高心理风险</span>' +
      '如感到痛苦或有伤害自己的念头，请立即拨打 24 小时心理援助热线 ' +
      '<a href="tel:4001619995">400-161-9995</a>（<a href="tel:01082951332">010-82951332</a>），' +
      '生命热线 <a href="tel:4008211215">400-821-1215</a>，或前往最近医院急诊。</div>';
  }

  function isHighRisk(score, answers, text) {
    if (!RISK || KIND !== 'clinical') return false;
    if (typeof RISK.score_gte === 'number' && typeof score === 'number' && score >= RISK.score_gte) return true;
    if (RISK.item_gte && answers) {
      var idx = RISK.item_gte[0], min = RISK.item_gte[1];
      if (typeof answers[idx] === 'number' && answers[idx] >= min) return true;
    }
    if (RISK.text_any) {
      var t = String(text || '');
      for (var i = 0; i < RISK.text_any.length; i++) {
        if (t.indexOf(RISK.text_any[i]) >= 0) return true;
      }
    }
    return false;
  }

  function enhanceResult() {
    var box = resultEl();
    if (!box) return;
    var text = (box.textContent || '').trim();
    if (!text) return;
    var sig = text.length + ':' + text.slice(0, 40);
    if (box.getAttribute('data-pk-sig') === sig) return;
    box.setAttribute('data-pk-sig', sig);

    $$('.pk-hotline', box).forEach(function (n) { n.parentNode.removeChild(n); });
    $$('.pk-scorecard', box).forEach(function (n) { n.parentNode.removeChild(n); });
    $$('.pk-actions', box).forEach(function (n) { n.parentNode.removeChild(n); });

    lastScore = parseScore(text);
    var lv = matchLevel(text) || (function () {
      var sev = $('.sev-box', box);
      return sev ? matchLevel(sev.textContent) : null;
    })();
    lastLevel = lv;

    var answers = readAnswers();
    var high = isHighRisk(lastScore, answers, text);

    var head = '';
    if (high) head += hotlineHtml();

    if (lv && lastScore !== null) {
      head += '<div class="pk-scorecard">' +
        '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">' +
        '<div><div class="pk-score" style="color:' + lv.color + ';">' + lastScore + '</div>' +
        '<div style="font-size:13px;color:var(--text-secondary,#6B7280);margin-top:2px;">总分</div></div>' +
        '<span class="pk-badge" style="background:' + lv.color + ';">' + lv.label + '</span>' +
        '</div></div>';
    } else if (lv) {
      head += '<div class="pk-scorecard"><span class="pk-badge" style="background:' + lv.color + ';">' + lv.label + '</span></div>';
    }

    if (head) box.insertAdjacentHTML('afterbegin', head);

    var act = document.createElement('div');
    act.className = 'pk-actions';
    act.innerHTML =
      '<button type="button" class="pk-btn primary" id="pk-copy">📋 复制结果</button>' +
      '<button type="button" class="pk-btn" id="pk-img">🖼 保存为图片</button>';
    box.appendChild(act);

    $('#pk-copy').addEventListener('click', copySummary);
    $('#pk-img').addEventListener('click', exportImage);
  }

  function buildSummary() {
    var d = new Date();
    var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
    var date = d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
    var lv = lastLevel ? lastLevel.label : '';
    var lines = [];
    lines.push('【' + (NAME || document.title.replace(/\s*[-|].*$/, '')) + '】');
    lines.push('总分：' + (lastScore === null ? '—' : lastScore) + (lv ? '（' + lv + '）' : ''));
    lines.push('评估日期：' + date);
    lines.push('本结果为自助筛查，不替代专业诊断。');
    return lines.join('\n');
  }

  function copySummary() {
    var txt = buildSummary();
    var done = function () {
      try { if (window.ToolBox && window.ToolBox.showToast) { window.ToolBox.showToast('结果已复制', 'success'); return; } } catch (e) { }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(done, fallback);
    } else fallback();
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = txt; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (e) { }
      document.body.removeChild(ta); done();
    }
  }

  function wrapText(ctx, text, maxW) {
    var out = [], line = '';
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (ctx.measureText(line + ch).width > maxW && line) { out.push(line); line = ch; }
      else line += ch;
    }
    if (line) out.push(line);
    return out;
  }

  function exportImage() {
    try {
      var W = 720, PAD = 32, SCALE = 2;
      var c = document.createElement('canvas');
      var ctx = c.getContext('2d');
      var title = NAME || document.title.replace(/\s*[-|].*$/, '');
      var lv = lastLevel;
      var date = new Date();
      var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
      var dstr = date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate());
      var advice = '本结果为自助筛查，不替代专业诊断。如感到痛苦或有伤害自己的念头，请拨打 24 小时心理援助热线 400-161-9995。';
      var f = function (s, w) { return (w || 400) + ' ' + s + 'px -apple-system,"PingFang SC","Microsoft YaHei",sans-serif'; };
      ctx.font = f(15);
      var lines = wrapText(ctx, advice, W - PAD * 2);
      var H = PAD + 40 + 70 + 44 + lines.length * 26 + 60;
      c.width = W * SCALE; c.height = H * SCALE;
      ctx.scale(SCALE, SCALE);
      ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#FF6B35'; ctx.fillRect(0, 0, W, 6);
      ctx.fillStyle = '#1F2937'; ctx.font = f(20, 600); ctx.fillText(title, PAD, PAD + 26);
      ctx.fillStyle = '#6B7280'; ctx.font = f(13); ctx.fillText('评估日期：' + dstr, PAD, PAD + 50);
      if (lastScore !== null) {
        ctx.fillStyle = lv ? lv.color : '#1F2937';
        ctx.font = f(46, 800);
        ctx.fillText(String(lastScore), PAD, PAD + 108);
      }
      if (lv) {
        ctx.font = f(15, 600);
        var bw = ctx.measureText(lv.label).width + 24;
        var bx = PAD + (lastScore !== null ? ctx.measureText(String(lastScore)).width * 2.2 + 20 : 0);
        ctx.fillStyle = lv.color;
        roundRect(ctx, bx, PAD + 76, bw, 32, 16);
        ctx.fill();
        ctx.fillStyle = '#FFFFFF';
        ctx.fillText(lv.label, bx + 12, PAD + 97);
      }
      ctx.fillStyle = '#6B7280'; ctx.font = f(14);
      lines.forEach(function (ln, i) { ctx.fillText(ln, PAD, PAD + 150 + i * 26); });
      ctx.fillStyle = '#9CA3AF'; ctx.font = f(12);
      ctx.fillText('本结果由 ToolBox 本地生成，数据未上传。', PAD, H - 18);
      c.toBlob(function (blob) {
        if (!blob) return;
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url; a.download = title + '-结果-' + dstr + '.png';
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
      }, 'image/png');
    } catch (e) { }
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  /* ---------------- 娱乐/参考类标识 ---------------- */
  function buildTag() {
    if (!NOTE) return;
    if ($('#pk-tag')) return;
    var anchor =
      $('.tool-intro') || $('.tool-header') || $('main .container') ||
      $('#quiz') || $('main') || document.body;
    var t = document.createElement('div');
    t.id = 'pk-tag';
    t.className = 'pk-wrap';
    t.innerHTML = '<span class="pk-tag">🎯 ' + NOTE + '</span>';
    var host = $('#quiz');
    if (host && host.parentNode) host.parentNode.insertBefore(t, host);
    else if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(t, anchor);
  }

  /* ---------------- 事件绑定 ---------------- */
  function bindGlobal() {
    document.addEventListener('click', function (e) {
      var o = e.target.closest ? e.target.closest('.q-opt') : null;
      if (!o) return;
      setTimeout(function () {
        updateProgress();
        saveAnswers();
        if (restoring || window.innerWidth > 768) return;
        // 移动端：答完后滚动到下一题
        var rows = optRows();
        var idx = rows.indexOf(o.parentNode);
        for (var i = idx + 1; i < rows.length; i++) {
          if (!$('.q-opt.active', rows[i])) {
            var it = rows[i].closest ? rows[i].closest('.q-item') : rows[i];
            if (it) { try { it.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (err) { } }
            break;
          }
        }
      }, 60);
    }, false);

    window.addEventListener('beforeunload', function (e) {
      if (restoring) return;
      var a = readAnswers();
      var any = a.some(function (v) { return v >= 0; });
      var miss = missingList();
      if (any && miss.length) {
        e.preventDefault();
        e.returnValue = '作答内容将丢失，确定离开？';
        return '作答内容将丢失，确定离开？';
      }
    });
  }

  function observeResult() {
    var box = resultEl();
    if (!box) return;
    enhanceResult();
    if (window.MutationObserver) {
      var mo = new MutationObserver(function () { try { enhanceResult(); } catch (e) { } });
      mo.observe(box, { childList: true, subtree: true, characterData: true });
    } else {
      setInterval(function () { try { enhanceResult(); } catch (e) { } }, 500);
    }
  }

  /* ---------------- 启动 ---------------- */
  function boot() {
    try {
      injectStyles();
      buildTag();
      if (optRows().length) {
        buildIntro();
        buildProgress();
        buildResume();
        bindGlobal();
        hookSubmit();
      }
      observeResult();
    } catch (e) { }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
