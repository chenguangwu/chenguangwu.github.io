/* ToolBox 轻量图表库（零依赖 Canvas，支持明暗主题 / 高 DPI）
 * 暴露到 window.ToolBox.chart：bar / line / gauge / donut / bars
 * 颜色自动读取 CSS 变量，随主题切换。
 */
(function () {
  'use strict';
  var PALETTE = ['#FF6B35', '#7C3AED', '#00C9A7', '#3B82F6', '#F59E0B', '#EF4444', '#10B981', '#8B5CF6'];

  function cssVar(name, fallback) {
    try {
      var v = getComputedStyle(document.documentElement).getPropertyValue(name);
      return (v && v.trim()) || fallback;
    } catch (e) { return fallback; }
  }
  function theme() {
    return {
      text: cssVar('--text', '#1F2937'),
      muted: cssVar('--text-muted', '#6B7280'),
      border: cssVar('--border', '#E5E7EB'),
      card: cssVar('--card', '#FFFFFF'),
      primary: cssVar('--primary', '#FF6B35'),
      grid: cssVar('--border', '#E5E7EB')
    };
  }
  function setup(canvas) {
    var dpr = window.devicePixelRatio || 1;
    var rect = canvas.getBoundingClientRect();
    var w = rect.width || canvas.parentElement.clientWidth || 320;
    var h = canvas.getAttribute('height') ? parseInt(canvas.getAttribute('height'), 10) : Math.round(w * 0.55);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    canvas.style.height = h + 'px';
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    return { ctx: ctx, w: w, h: h };
  }
  function niceMax(max) {
    if (max <= 0) return 1;
    var exp = Math.pow(10, Math.floor(Math.log10(max)));
    var f = max / exp;
    var nf = f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10;
    return nf * exp;
  }

  function drawBars(canvas, cfg) {
    var t = theme();
    var s = setup(canvas), ctx = s.ctx, w = s.w, h = s.h;
    var labels = cfg.labels || [], values = cfg.values || [];
    var padL = 38, padR = 12, padT = 14, padB = 26;
    var cw = w - padL - padR, ch = h - padT - padB;
    var max = niceMax(Math.max.apply(null, values.concat([1])));
    // grid + y labels
    ctx.strokeStyle = t.grid; ctx.fillStyle = t.muted; ctx.font = '11px sans-serif'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    for (var i = 0; i <= 4; i++) {
      var y = padT + ch - (ch * i / 4);
      ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(w - padR, y); ctx.stroke();
      ctx.fillText(fmt(max * i / 4), padL - 4, y);
    }
    var n = values.length;
    if (!n) return;
    var slot = cw / n, bw = Math.min(slot * 0.6, 46);
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    for (var j = 0; j < n; j++) {
      var x = padL + slot * j + (slot - bw) / 2;
      var bh = ch * (values[j] / max);
      var y0 = padT + ch - bh;
      var col = (cfg.colors && cfg.colors[j]) || PALETTE[j % PALETTE.length];
      ctx.fillStyle = col;
      roundRect(ctx, x, y0, bw, bh, 4); ctx.fill();
      ctx.fillStyle = t.muted;
      if (labels[j]) ctx.fillText(String(labels[j]), padL + slot * j + slot / 2, padT + ch + 5);
    }
  }

  function drawLine(canvas, cfg) {
    var t = theme();
    var s = setup(canvas), ctx = s.ctx, w = s.w, h = s.h;
    var labels = cfg.labels || [], values = cfg.values || [];
    var padL = 40, padR = 12, padT = 14, padB = 26;
    var cw = w - padL - padR, ch = h - padT - padB;
    var max = niceMax(Math.max.apply(null, values.concat([1])));
    var min = cfg.min != null ? cfg.min : 0;
    ctx.strokeStyle = t.grid; ctx.fillStyle = t.muted; ctx.font = '11px sans-serif'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    for (var i = 0; i <= 4; i++) {
      var y = padT + ch - (ch * i / 4);
      ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(w - padR, y); ctx.stroke();
      ctx.fillText(fmt(max * i / 4), padL - 4, y);
    }
    var n = values.length;
    if (!n) return;
    function px(i) { return padL + (n === 1 ? cw / 2 : cw * i / (n - 1)); }
    function py(v) { return padT + ch - ch * ((v - min) / (max - min || 1)); }
    // area
    var grad = ctx.createLinearGradient(0, padT, 0, padT + ch);
    grad.addColorStop(0, hexA(t.primary, 0.25)); grad.addColorStop(1, hexA(t.primary, 0.02));
    ctx.beginPath(); ctx.moveTo(px(0), py(values[0]));
    for (var k = 1; k < n; k++) ctx.lineTo(px(k), py(values[k]));
    ctx.lineTo(px(n - 1), padT + ch); ctx.lineTo(px(0), padT + ch); ctx.closePath();
    ctx.fillStyle = grad; ctx.fill();
    // line
    ctx.beginPath(); ctx.moveTo(px(0), py(values[0]));
    for (var m = 1; m < n; m++) ctx.lineTo(px(m), py(values[m]));
    ctx.strokeStyle = t.primary; ctx.lineWidth = 2.5; ctx.stroke();
    // points
    ctx.fillStyle = t.primary;
    for (var p = 0; p < n; p++) { ctx.beginPath(); ctx.arc(px(p), py(values[p]), 3, 0, 7); ctx.fill(); }
    ctx.fillStyle = t.muted; ctx.textAlign = 'center'; ctx.textBaseline = 'top'; ctx.font = '10px sans-serif';
    var step = Math.ceil(n / 6);
    for (var q = 0; q < n; q += step) { if (labels[q]) ctx.fillText(String(labels[q]), px(q), padT + ch + 5); }
  }

  function drawGauge(canvas, cfg) {
    var t = theme();
    var s = setup(canvas), ctx = s.ctx, w = s.w, h = s.h;
    var val = +cfg.value || 0, min = cfg.min != null ? cfg.min : 0, max = cfg.max != null ? cfg.max : 100;
    var label = cfg.label || '', unit = cfg.unit || '';
    var cx = w / 2, cy = h * 0.62, r = Math.min(w / 2, h * 0.62) - 14;
    var start = Math.PI * 0.75, end = Math.PI * 2.25, span = end - start;
    var frac = Math.max(0, Math.min(1, (val - min) / (max - min || 1)));
    // track
    ctx.lineWidth = Math.max(10, r * 0.16); ctx.lineCap = 'round';
    ctx.strokeStyle = t.grid;
    ctx.beginPath(); ctx.arc(cx, cy, r, start, end); ctx.stroke();
    // value
    var col = (cfg.colors && cfg.colors[0]) || t.primary;
    ctx.strokeStyle = col;
    ctx.beginPath(); ctx.arc(cx, cy, r, start, start + span * frac); ctx.stroke();
    // text
    ctx.fillStyle = t.text; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = 'bold 22px sans-serif';
    ctx.fillText(fmt(val) + (unit ? ' ' + unit : ''), cx, cy - 2);
    if (label) { ctx.fillStyle = t.muted; ctx.font = '12px sans-serif'; ctx.fillText(label, cx, cy + 22); }
  }

  function drawDonut(canvas, cfg) {
    var t = theme();
    var s = setup(canvas), ctx = s.ctx, w = s.w, h = s.h;
    var segs = cfg.segments || [];
    var total = segs.reduce(function (a, b) { return a + (b.value || 0); }, 0) || 1;
    var cx = w / 2, cy = h / 2, r = Math.min(w, h) / 2 - 8, ir = r * 0.6;
    var ang = -Math.PI / 2;
    segs.forEach(function (seg, i) {
      var a2 = ang + (seg.value / total) * Math.PI * 2;
      ctx.beginPath(); ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, ang, a2); ctx.closePath();
      ctx.fillStyle = (seg.color) || PALETTE[i % PALETTE.length]; ctx.fill();
      ang = a2;
    });
    ctx.beginPath(); ctx.arc(cx, cy, ir, 0, Math.PI * 2); ctx.fillStyle = t.card; ctx.fill();
    if (cfg.centerLabel) { ctx.fillStyle = t.text; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = 'bold 16px sans-serif'; ctx.fillText(cfg.centerLabel, cx, cy); }
  }

  function roundRect(ctx, x, y, w, h, r) {
    if (h < 0) { y += h; h = -h; }
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function fmt(v) {
    if (v === null || v === undefined || isNaN(v)) return '-';
    var a = Math.abs(v);
    if (a >= 1e8) return (v / 1e8).toFixed(1) + '亿';
    if (a >= 1e4) return (v / 1e4).toFixed(1) + '万';
    if (a >= 1000) return v.toLocaleString('zh-CN');
    if (a >= 100) return v.toFixed(0);
    if (a >= 10) return v.toFixed(1);
    return v.toFixed(2).replace(/\.?0+$/, '');
  }
  function hexA(hex, a) {
    hex = (hex || '#FF6B35').replace('#', '');
    if (hex.length === 3) hex = hex.split('').map(function (c) { return c + c; }).join('');
    var r = parseInt(hex.substr(0, 2), 16), g = parseInt(hex.substr(2, 2), 16), b = parseInt(hex.substr(4, 2), 16);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
  }

  function render(canvas, type, cfg) {
    if (!canvas) return;
    if (type === 'bar' || type === 'bars') drawBars(canvas, cfg);
    else if (type === 'line') drawLine(canvas, cfg);
    else if (type === 'gauge') drawGauge(canvas, cfg);
    else if (type === 'donut') drawDonut(canvas, cfg);
  }

  window.ToolBox = window.ToolBox || {};
  window.ToolBox.chart = {
    bar: function (c, cfg) { render(c, 'bar', cfg); },
    bars: function (c, cfg) { render(c, 'bar', cfg); },
    line: function (c, cfg) { render(c, 'line', cfg); },
    gauge: function (c, cfg) { render(c, 'gauge', cfg); },
    donut: function (c, cfg) { render(c, 'donut', cfg); },
    render: render
  };
  if (window.ToolBox.refreshCharts) {} // hook for theme switch
  // 主题切换后重绘所有图表
  if (window.ToolBox && !window.ToolBox._chartBound) {
    window.ToolBox._chartBound = true;
    // 注意：只缓存这一次，且必须是函数才调用。若本文件将来被提前到 common.js 之前
    // 加载，此处拿到会是入队占位实现 —— 届时应改为点击时动态解析 window.ToolBox。
    var origToggle = window.ToolBox.toggleToolTheme;
    window.ToolBox.toggleToolTheme = function () {
      if (typeof origToggle === 'function') {
        try { origToggle.apply(this, arguments); } catch (e) {}
      }
      try { redrawAll(); } catch (e) {}
    };
    document.addEventListener('DOMContentLoaded', function () {
      window.addEventListener('resize', debounce(redrawAll, 200));
    });
  }
  function debounce(fn, ms) { var t; return function () { clearTimeout(t); t = setTimeout(fn, ms); }; }
  function redrawAll() {
    var els = document.querySelectorAll('canvas[data-chart]');
    els.forEach(function (el) {
      try {
        var cfg = JSON.parse(el.getAttribute('data-chart-cfg') || '{}');
        render(el, el.getAttribute('data-chart'), cfg);
      } catch (e) {}
    });
  }
  window.ToolBox.redrawCharts = redrawAll;
})();
