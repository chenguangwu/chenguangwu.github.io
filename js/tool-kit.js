/*
 * ToolBox 工具页体验组件库 (js/tool-kit.js)
 * ---------------------------------------------------------------------------
 * 定位：UX-Q4 专项的公共能力层。页面不再各自内联几百行图表/历史/导出代码，
 * 统一调用本库，保证「个性化形态」可规模化落地且体积受控。
 *
 * 硬约束：
 *   1) 纯前端、零外部依赖（图表全部自绘 SVG，禁 CDN、禁新依赖）；
 *   2) 幂等：重复加载只执行一次（window.__TBKIT__ 守卫）；
 *   3) 零侵入：不自动改写页面已有 DOM，只做「页面显式声明/调用」的挂载；
 *   4) 主题兼容：颜色一律走 CSS 变量（--primary/--border/--text/--text-muted/--card-bg），
 *      深色 [data-theme=dark] 自动跟随；
 *   5) 可访问性：SVG 加 role="img" + <title>，按钮带 aria-label。
 *
 * ⚠ 调用方铁律（关系到 verify 门禁）：
 *   无头门禁沙箱不加载任何外部 <script>，页面内联脚本里直接写 TBKit.xxx() 会
 *   ReferenceError 导致整页门禁失败。所有调用必须做存在性守卫：
 *       if (typeof TBKit !== 'undefined') { TBKit.chart.line('#c', data); }
 *   或统一用 TBKit 提供的安全包装：
 *       TBK(function (K) { K.chart.line('#c', data); });
 *   —— TBK() 在库缺失时静默跳过，在真实浏览器里正常执行。
 *   另：verify 用例的 expect 只允许锚定「页面原有文本/数值输出」，禁止依赖图表 DOM。
 *
 * 用法（API 式）：
 *   TBK(function (K) {
 *     K.chart.line('#chart', { labels: [...], series: [{ name: '月供', data: [...] }] });
 *     K.preset.bar('#presets', [{ label: '30年商业贷', values: { rate: 4.9, years: 30 } }], recalc);
 *     K.history.record({ monthly: 5307 });
 *     K.history.mount('#history');
 *   });
 *
 * 用法（声明式，B 档页零改 JS 即可挂载）：
 *   <div data-tb="history"></div>
 *   <div data-tb="preset" data-tb-presets='[{"label":"示例","values":{"a":3,"b":4,"c":5}}]'></div>
 */
(function () {
  'use strict';

  if (window.__TBKIT__) return;
  window.__TBKIT__ = true;

  /* ============================ 基础工具 ============================ */

  var PALETTE = ['#3B82F6', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6', '#06B6D4', '#EC4899', '#84CC16'];

  // 组件内置文案双语：组件自己渲染的 UI 文本不进页面 i18n 字典，
  // 故在此自带中英两套，英文态（?lang=en-US）自动切英文，杜绝中文残留。
  var T = {
    zh: { tip: '试试：', hist: '🕘 最近计算', clear: '清空', empty: '暂无记录', search: '搜索…', copyTip: '点击复制', actions: '结果操作' },
    en: { tip: 'Try:', hist: '🕘 Recent', clear: 'Clear', empty: 'No records', search: 'Search…', copyTip: 'Click to copy', actions: 'Result actions' }
  };
  function isEn() {
    try {
      if (/lang=en-US/i.test(location.search)) return true;
      var l = (document.documentElement && document.documentElement.lang) || '';
      return /^en/i.test(l);
    } catch (e) { return false; }
  }
  function tt(k) {
    var pack = isEn() ? T.en : T.zh;
    return pack[k] || T.zh[k] || k;
  }

  function $(sel, root) {
    if (!sel) return null;
    if (typeof sel !== 'string') return sel;
    return (root || document).querySelector(sel);
  }

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) {
      for (var k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
        if (attrs[k] == null) continue;
        n.setAttribute(k, String(attrs[k]));
      }
    }
    if (children) {
      for (var i = 0; i < children.length; i++) {
        if (children[i]) n.appendChild(children[i]);
      }
    }
    return n;
  }

  var SVGNS = 'http://www.w3.org/2000/svg';
  function s(tag, attrs, children) {
    var n = document.createElementNS(SVGNS, tag);
    if (attrs) {
      for (var k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
        if (attrs[k] == null) continue;
        n.setAttribute(k, String(attrs[k]));
      }
    }
    if (children) {
      for (var i = 0; i < children.length; i++) {
        if (children[i]) n.appendChild(children[i]);
      }
    }
    return n;
  }

  function num(v) {
    var n = typeof v === 'number' ? v : parseFloat(v);
    return isFinite(n) ? n : 0;
  }

  /** 数字美化：12345.678 → 12,345.68（保留 2 位，可指定） */
  function fmt(v, digits) {
    var n = num(v);
    var d = digits == null ? 2 : digits;
    var neg = n < 0;
    var a = Math.abs(n);
    var out;
    if (a !== 0 && (a >= 1e12 || a < 1e-6)) {
      out = a.toExponential(2);
    } else {
      out = a.toFixed(d);
      var parts = out.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      out = parts.join('.');
      if (d > 0) out = out.replace(/0+$/, '').replace(/\.$/, '');
    }
    return (neg ? '-' : '') + out;
  }

  function niceMax(v) {
    if (v <= 0) return 1;
    var exp = Math.floor(Math.log(v) / Math.LN10);
    var base = Math.pow(10, exp);
    var f = v / base;
    var m = f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10;
    return m * base;
  }

  function toast(msg, type) {
    try {
      if (window.ToolBox && typeof window.ToolBox.showToast === 'function') {
        window.ToolBox.showToast(msg, type || 'success');
        return;
      }
    } catch (e) {}
    try {
      var t = document.createElement('div');
      t.textContent = msg;
      t.setAttribute('role', 'status');
      t.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:' +
        (type === 'error' ? '#EF4444' : '#10B981') + ';color:#fff;padding:10px 18px;border-radius:12px;' +
        'font-size:13px;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,.2);';
      document.body.appendChild(t);
      setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 2200);
    } catch (e2) {}
  }

  /** 安全包装：库缺失时静默跳过（verify 沙箱安全） */
  function TBK(fn) {
    if (typeof fn !== 'function') return;
    try { fn(window.TBKit); } catch (e) {}
  }

  /* ============================ 图表 ============================ */

  /**
   * 通用画布：返回 {svg, w, h}，统一 viewBox 与内边距。
   * opts: {height, padding, title}
   */
  function canvas(host, opts) {
    opts = opts || {};
    var h = opts.height || 220;
    var pad = opts.padding == null ? { t: 16, r: 16, b: 28, l: 44 } : opts.padding;
    var w = 640;
    var svg = s('svg', {
      viewBox: '0 0 ' + w + ' ' + h,
      width: '100%',
      height: h,
      preserveAspectRatio: 'xMidYMid meet',
      role: 'img',
      'aria-label': opts.title || '图表',
      style: 'display:block;max-width:100%;overflow:visible;'
    });
    if (opts.title) svg.appendChild(s('title', {}, [document.createTextNode(opts.title)]));
    return { svg: svg, w: w, h: h, pad: pad, iw: w - pad.l - pad.r, ih: h - pad.t - pad.b };
  }

  function mount(host, svg) {
    var box = $(host);
    if (!box) return null;
    box.innerHTML = '';
    box.appendChild(svg);
    return svg;
  }

  function axis(c, min, max, opts) {
    var g = s('g', {});
    var ticks = (opts && opts.ticks) || 4;
    for (var i = 0; i <= ticks; i++) {
      var y = c.pad.t + c.ih * (i / ticks);
      g.appendChild(s('line', {
        x1: c.pad.l, y1: y, x2: c.pad.l + c.iw, y2: y,
        stroke: 'var(--border, #E5E7EB)', 'stroke-width': 1
      }));
      var val = max - (max - min) * (i / ticks);
      var tx = s('text', {
        x: c.pad.l - 6, y: y + 4, 'text-anchor': 'end',
        fill: 'var(--text-muted, #6B7280)', 'font-size': 10
      });
      tx.appendChild(document.createTextNode(fmt(val, 1)));
      g.appendChild(tx);
    }
    return g;
  }

  function legend(c, names) {
    if (!names || !names.length) return null;
    var g = s('g', {});
    var x = c.pad.l;
    for (var i = 0; i < names.length; i++) {
      g.appendChild(s('rect', { x: x, y: 2, width: 10, height: 10, rx: 2, fill: PALETTE[i % PALETTE.length] }));
      var t = s('text', { x: x + 14, y: 11, 'font-size': 11, fill: 'var(--text, #374151)' });
      t.appendChild(document.createTextNode(names[i]));
      g.appendChild(t);
      x += 20 + names[i].length * 7;
    }
    return g;
  }

  var chart = {};

  /** 折线 / 面积图 */
  chart.line = function (host, cfg) {
    cfg = cfg || {};
    var labels = cfg.labels || [];
    var series = cfg.series || [];
    if (!series.length) return null;
    var c = canvas(host, { height: cfg.height || 220, title: cfg.title });
    var all = [];
    series.forEach(function (se) { (se.data || []).forEach(function (v) { all.push(num(v)); }); });
    var max = cfg.max == null ? niceMax(Math.max.apply(null, all.concat([0])) * 1.1) : cfg.max;
    var min = cfg.min == null ? 0 : cfg.min;
    if (max === min) max = min + 1;

    c.svg.appendChild(axis(c, min, max, { ticks: cfg.ticks || 4 }));

    var n = Math.max(labels.length, 1);
    var stepX = n > 1 ? c.iw / (n - 1) : 0;

    series.forEach(function (se, si) {
      var data = se.data || [];
      var color = se.color || PALETTE[si % PALETTE.length];
      var pts = data.map(function (v, i) {
        return [c.pad.l + (n > 1 ? i * stepX : c.iw / 2), c.pad.t + c.ih * (1 - (num(v) - min) / (max - min))];
      });
      if (!pts.length) return;
      var d = pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' ');
      if (cfg.area !== false && series.length === 1) {
        c.svg.appendChild(s('path', {
          d: d + ' L' + pts[pts.length - 1][0].toFixed(1) + ' ' + (c.pad.t + c.ih) +
             ' L' + pts[0][0].toFixed(1) + ' ' + (c.pad.t + c.ih) + ' Z',
          fill: color, 'fill-opacity': 0.12, stroke: 'none'
        }));
      }
      c.svg.appendChild(s('path', { d: d, fill: 'none', stroke: color, 'stroke-width': 2, 'stroke-linejoin': 'round' }));
      pts.forEach(function (p, i) {
        var dot = s('circle', { cx: p[0], cy: p[1], r: 3, fill: color });
        var tt = s('title', {});
        tt.appendChild(document.createTextNode((labels[i] != null ? labels[i] + '：' : '') + fmt(data[i])));
        dot.appendChild(tt);
        c.svg.appendChild(dot);
      });
    });

    // X 轴标签（最多显示 8 个，避免拥挤）
    var showEvery = Math.ceil(n / 8) || 1;
    labels.forEach(function (lb, i) {
      if (i % showEvery !== 0 && i !== n - 1) return;
      var t = s('text', {
        x: c.pad.l + (n > 1 ? i * stepX : c.iw / 2), y: c.h - 8,
        'text-anchor': 'middle', 'font-size': 10, fill: 'var(--text-muted, #6B7280)'
      });
      t.appendChild(document.createTextNode(lb));
      c.svg.appendChild(t);
    });
    if (series.length > 1) {
      var lg = legend(c, series.map(function (x) { return x.name || ''; }));
      if (lg) c.svg.appendChild(lg);
    }
    return mount(host, c.svg);
  };

  /** 柱状图（支持多系列分组） */
  chart.bar = function (host, cfg) {
    cfg = cfg || {};
    var labels = cfg.labels || [];
    var series = cfg.series || [{ name: '', data: cfg.data || [] }];
    var c = canvas(host, { height: cfg.height || 220, title: cfg.title });
    var all = [];
    series.forEach(function (se) { (se.data || []).forEach(function (v) { all.push(num(v)); }); });
    var rawMax = all.length ? Math.max.apply(null, all) : 0;
    var max = cfg.max == null ? niceMax(rawMax * 1.15 || 1) : cfg.max;
    var min = cfg.min == null ? 0 : cfg.min;
    if (max === min) max = min + 1;
    c.svg.appendChild(axis(c, min, max, { ticks: cfg.ticks || 4 }));

    var n = Math.max(labels.length, 1);
    var groupW = c.iw / n;
    var barW = Math.min(38, (groupW * 0.7) / series.length);
    series.forEach(function (se, si) {
      var color = se.color || PALETTE[si % PALETTE.length];
      (se.data || []).forEach(function (v, i) {
        var x = c.pad.l + i * groupW + (groupW - barW * series.length) / 2 + si * barW;
        var hgt = Math.max(1, c.ih * (num(v) - min) / (max - min));
        var y = c.pad.t + c.ih - hgt;
        var r = s('rect', { x: x, y: y, width: barW - 2, height: hgt, rx: 3, fill: color });
        var tt = s('title', {});
        tt.appendChild(document.createTextNode((labels[i] != null ? labels[i] + '：' : '') + fmt(v)));
        r.appendChild(tt);
        c.svg.appendChild(r);
      });
    });
    var showEvery = Math.ceil(n / 8) || 1;
    labels.forEach(function (lb, i) {
      if (i % showEvery !== 0 && i !== n - 1) return;
      var t = s('text', {
        x: c.pad.l + i * groupW + groupW / 2, y: c.h - 8,
        'text-anchor': 'middle', 'font-size': 10, fill: 'var(--text-muted, #6B7280)'
      });
      t.appendChild(document.createTextNode(lb));
      c.svg.appendChild(t);
    });
    if (series.length > 1) {
      var lg = legend(c, series.map(function (x) { return x.name || ''; }));
      if (lg) c.svg.appendChild(lg);
    }
    return mount(host, c.svg);
  };

  /** 饼图 / 环形图（center 有值时为环形） */
  chart.pie = function (host, cfg) {
    cfg = cfg || {};
    var items = cfg.items || cfg.data || [];
    var total = items.reduce(function (a, b) { return a + Math.abs(num(b.value != null ? b.value : b)); }, 0);
    if (!total) return null;
    var c = canvas(host, { height: cfg.height || 220, padding: { t: 10, r: 10, b: 10, l: 10 }, title: cfg.title });
    var cx = c.w / 2, cy = c.h / 2;
    var R = Math.min(c.w, c.h) / 2 - 12;
    var r0 = cfg.center ? R * 0.58 : 0;
    var a0 = -Math.PI / 2;
    items.forEach(function (it, i) {
      var v = Math.abs(num(it.value != null ? it.value : it));
      if (!v) return;
      var a1 = a0 + (v / total) * Math.PI * 2;
      var large = (a1 - a0) > Math.PI ? 1 : 0;
      var p = [
        'M', (cx + r0 * Math.cos(a0)).toFixed(1), (cy + r0 * Math.sin(a0)).toFixed(1),
        'L', (cx + R * Math.cos(a0)).toFixed(1), (cy + R * Math.sin(a0)).toFixed(1),
        'A', R, R, 0, large, 1, (cx + R * Math.cos(a1)).toFixed(1), (cy + R * Math.sin(a1)).toFixed(1)
      ];
      if (r0) p.push('L', (cx + r0 * Math.cos(a1)).toFixed(1), (cy + r0 * Math.sin(a1)).toFixed(1),
                    'A', r0, r0, 0, large, 0, (cx + r0 * Math.cos(a0)).toFixed(1), (cy + r0 * Math.sin(a0)).toFixed(1));
      else p.push('L', cx, cy);
      p.push('Z');
      var path = s('path', { d: p.join(' '), fill: it.color || PALETTE[i % PALETTE.length] });
      var tt = s('title', {});
      tt.appendChild(document.createTextNode((it.label || '') + ' ' + fmt(v) + '（' + (v / total * 100).toFixed(1) + '%）'));
      path.appendChild(tt);
      c.svg.appendChild(path);
      a0 = a1;
    });
    if (cfg.center) {
      var t1 = s('text', { x: cx, y: cy - 2, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--text-muted, #6B7280)' });
      t1.appendChild(document.createTextNode(cfg.centerLabel || ''));
      var t2 = s('text', { x: cx, y: cy + 18, 'text-anchor': 'middle', 'font-size': 18, 'font-weight': 700, fill: 'var(--primary, #FF6B35)' });
      t2.appendChild(document.createTextNode(cfg.center));
      c.svg.appendChild(t1); c.svg.appendChild(t2);
    }
    return mount(host, c.svg);
  };

  /** 仪表盘（0–100 或自定义区间） */
  chart.gauge = function (host, cfg) {
    cfg = cfg || {};
    var v = num(cfg.value), min = num(cfg.min || 0), max = cfg.max == null ? 100 : num(cfg.max);
    var pct = Math.min(1, Math.max(0, (v - min) / (max - min || 1)));
    var c = canvas(host, { height: cfg.height || 150, padding: { t: 8, r: 8, b: 8, l: 8 }, title: cfg.title });
    var cx = c.w / 2, cy = c.h - 20, R = Math.min(c.w / 2 - 20, c.h - 40);
    var a0 = Math.PI, a1 = 0;
    var ang = Math.PI + pct * Math.PI;
    function pt(a, r) { return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; }
    var bg = s('path', {
      d: 'M ' + pt(a0, R).join(' ') + ' A ' + R + ' ' + R + ' 0 0 1 ' + pt(a1, R).join(' '),
      fill: 'none', stroke: 'var(--border, #E5E7EB)', 'stroke-width': 14, 'stroke-linecap': 'round'
    });
    var fg = s('path', {
      d: 'M ' + pt(a0, R).join(' ') + ' A ' + R + ' ' + R + ' 0 0 1 ' + pt(ang, R).join(' '),
      fill: 'none', stroke: cfg.color || 'var(--primary, #FF6B35)', 'stroke-width': 14, 'stroke-linecap': 'round'
    });
    var tt = s('title', {}); tt.appendChild(document.createTextNode(fmt(v)));
    fg.appendChild(tt);
    c.svg.appendChild(bg); c.svg.appendChild(fg);
    var tv = s('text', { x: cx, y: cy - 6, 'text-anchor': 'middle', 'font-size': 24, 'font-weight': 700, fill: 'var(--text, #111827)' });
    tv.appendChild(document.createTextNode(cfg.text != null ? cfg.text : fmt(v)));
    c.svg.appendChild(tv);
    var tl = s('text', { x: cx, y: cy + 12, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--text-muted, #6B7280)' });
    tl.appendChild(document.createTextNode(cfg.label || ''));
    c.svg.appendChild(tl);
    return mount(host, c.svg);
  };

  /** 雷达图 */
  chart.radar = function (host, cfg) {
    cfg = cfg || {};
    var axes = (cfg.axes || []).map(function (a) { return a.label != null ? a.label : a; });
    var vals = cfg.values || [];
    if (axes.length < 3) return null;
    var c = canvas(host, { height: cfg.height || 240, padding: { t: 14, r: 14, b: 14, l: 14 }, title: cfg.title });
    var cx = c.w / 2, cy = c.h / 2, R = Math.min(c.w, c.h) / 2 - 30;
    var max = cfg.max == null ? niceMax(Math.max.apply(null, vals.concat([1])) * 1.15) : cfg.max;
    var N = axes.length;
    function angAt(i) { return -Math.PI / 2 + i * Math.PI * 2 / N; }
    for (var r = 1; r <= 4; r++) {
      var pts = [];
      for (var i = 0; i < N; i++) {
        var rr = R * r / 4;
        pts.push((cx + rr * Math.cos(angAt(i))).toFixed(1) + ',' + (cy + rr * Math.sin(angAt(i))).toFixed(1));
      }
      c.svg.appendChild(s('polygon', { points: pts.join(' '), fill: 'none', stroke: 'var(--border, #E5E7EB)', 'stroke-width': 1 }));
    }
    for (var j = 0; j < N; j++) {
      var a = angAt(j);
      c.svg.appendChild(s('line', { x1: cx, y1: cy, x2: cx + R * Math.cos(a), y2: cy + R * Math.sin(a), stroke: 'var(--border, #E5E7EB)' }));
      var lx = cx + (R + 16) * Math.cos(a), ly = cy + (R + 16) * Math.sin(a);
      var t = s('text', { x: lx, y: ly + 4, 'font-size': 10, 'text-anchor': Math.abs(Math.cos(a)) < 0.2 ? 'middle' : (Math.cos(a) > 0 ? 'start' : 'end'), fill: 'var(--text-muted, #6B7280)' });
      t.appendChild(document.createTextNode(axes[j]));
      c.svg.appendChild(t);
    }
    var vp = vals.map(function (v, i) {
      var rr = R * Math.min(1, num(v) / max);
      return (cx + rr * Math.cos(angAt(i))).toFixed(1) + ',' + (cy + rr * Math.sin(angAt(i))).toFixed(1);
    }).join(' ');
    c.svg.appendChild(s('polygon', { points: vp, fill: cfg.color || PALETTE[0], 'fill-opacity': 0.22, stroke: cfg.color || PALETTE[0], 'stroke-width': 2 }));
    return mount(host, c.svg);
  };

  /** 直方图（自动分箱） */
  chart.histogram = function (host, cfg) {
    cfg = cfg || {};
    var data = (cfg.data || []).map(num);
    if (!data.length) return null;
    var bins = cfg.bins || Math.min(20, Math.max(6, Math.round(Math.sqrt(data.length))));
    var mn = Math.min.apply(null, data), mx = Math.max.apply(null, data);
    if (mn === mx) { mn -= 0.5; mx += 0.5; }
    var w = (mx - mn) / bins;
    var counts = new Array(bins).fill(0);
    data.forEach(function (v) {
      var i = Math.min(bins - 1, Math.floor((v - mn) / w));
      counts[i]++;
    });
    var labels = counts.map(function (_, i) { return fmt(mn + w * (i + 0.5), 1); });
    return chart.bar(host, { labels: labels, series: [{ name: cfg.name || '频数', data: counts }], height: cfg.height, title: cfg.title });
  };

  /** 时间轴（节点 + 标签） */
  chart.timeline = function (host, cfg) {
    cfg = cfg || {};
    var items = cfg.items || [];
    if (!items.length) return null;
    var c = canvas(host, { height: cfg.height || 120, padding: { t: 34, r: 12, b: 24, l: 12 }, title: cfg.title });
    var y = c.pad.t + 10;
    c.svg.appendChild(s('line', { x1: c.pad.l, y1: y, x2: c.pad.l + c.iw, y2: y, stroke: 'var(--border, #E5E7EB)', 'stroke-width': 2 }));
    var n = items.length;
    items.forEach(function (it, i) {
      var x = c.pad.l + (n > 1 ? c.iw * i / (n - 1) : c.iw / 2);
      var dot = s('circle', { cx: x, cy: y, r: 6, fill: it.color || (it.strong ? 'var(--primary, #FF6B35)' : PALETTE[i % PALETTE.length]) });
      var tt = s('title', {}); tt.appendChild(document.createTextNode((it.date || '') + ' ' + (it.label || '')));
      dot.appendChild(tt);
      c.svg.appendChild(dot);
      var t1 = s('text', { x: x, y: y - 14, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 600, fill: 'var(--text, #111827)' });
      t1.appendChild(document.createTextNode(it.date || ''));
      c.svg.appendChild(t1);
      var t2 = s('text', { x: x, y: y + 20, 'text-anchor': 'middle', 'font-size': 10, fill: 'var(--text-muted, #6B7280)' });
      t2.appendChild(document.createTextNode(it.label || ''));
      c.svg.appendChild(t2);
    });
    return mount(host, c.svg);
  };

  /* ============================ 预设场景 ============================ */

  var preset = {};

  function setValue(field, val) {
    try {
      var f = $(field);
      if (!f) return;
      if (f.tagName === 'SELECT' || f.tagName === 'TEXTAREA' || f.tagName === 'INPUT') {
        if (f.type === 'checkbox' || f.type === 'radio') f.checked = !!val;
        else f.value = val;
        var ev = f.tagName === 'SELECT' ? 'change' : 'input';
        f.dispatchEvent(new Event(ev, { bubbles: true }));
        f.dispatchEvent(new Event('change', { bubbles: true }));
      }
    } catch (e) {}
  }

  /**
   * 渲染预设场景条。
   * @param host 容器
   * @param list [{label, values:{字段选择器或id: 值}}]
   * @param after 填充后的回调（通常是页面的 calc 函数）
   */
  preset.bar = function (host, list, after) {
    var box = $(host);
    if (!box || !list || !list.length) return null;
    box.innerHTML = '';
    var wrap = el('div', { class: 'tbk-presets', role: 'group', 'aria-label': '常用场景' });
    var tip = el('span', { class: 'tbk-presets-tip' });
    tip.textContent = tt('tip');
    wrap.appendChild(tip);
    list.forEach(function (p) {
      var b = el('button', { type: 'button', class: 'tbk-preset-btn' });
      b.textContent = (isEn() && p.labelEn) ? p.labelEn : p.label;
      b.addEventListener('click', function () {
        for (var k in p.values) {
          if (!Object.prototype.hasOwnProperty.call(p.values, k)) continue;
          setValue('#' + k, p.values[k]);
        }
        if (typeof after === 'function') { try { after(); } catch (e) {} }
        var all = wrap.querySelectorAll('.tbk-preset-btn');
        for (var i = 0; i < all.length; i++) all[i].classList.remove('active');
        b.classList.add('active');
      });
      wrap.appendChild(b);
    });
    box.appendChild(wrap);
    return wrap;
  };

  /* ============================ 历史记录 ============================ */

  var history = {};
  function hkey() {
    try { return 'tbk_hist_' + (location.pathname || 'p'); } catch (e) { return 'tbk_hist_p'; }
  }

  history.list = function () {
    try {
      var raw = localStorage.getItem(hkey());
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    } catch (e) { return []; }
  };

  history.clear = function () {
    try { localStorage.removeItem(hkey()); } catch (e) {}
  };

  /** 记录一次计算：obj 里放要展示的摘要字段 */
  history.record = function (obj) {
    if (!obj) return;
    try {
      var arr = history.list();
      arr.unshift({ t: Date.now(), d: obj });
      arr = arr.slice(0, 20);
      localStorage.setItem(hkey(), JSON.stringify(arr));
    } catch (e) {}
  };

  history.last = function () {
    var a = history.list();
    return a.length ? a[0].d : null;
  };

  /** 与上一条记录做差，返回 {field: {from, to, delta}} */
  history.diffLast = function (fields) {
    var a = history.list();
    if (a.length < 2) return null;
    var cur = a[0].d, prev = a[1].d, out = {};
    (fields || Object.keys(cur)).forEach(function (f) {
      if (num(prev[f]) === num(cur[f])) return;
      out[f] = { from: num(prev[f]), to: num(cur[f]), delta: num(cur[f]) - num(prev[f]) };
    });
    return out;
  };

  function fmtTime(ts) {
    var d = new Date(ts);
    function p(x) { return (x < 10 ? '0' : '') + x; }
    return p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  }

  /** 挂载历史面板；onPick 回调用于回填 */
  history.mount = function (host, onPick, limit) {
    var box = $(host);
    if (!box) return null;
    var arr = history.list().slice(0, limit || 6);
    box.innerHTML = '';
    if (!arr.length) return null;
    var wrap = el('div', { class: 'tbk-history' });
    var hd = el('div', { class: 'tbk-history-hd' });
    var t = el('span', {}); t.textContent = tt('hist');
    var clr = el('button', { type: 'button', class: 'tbk-link-btn', 'aria-label': isEn() ? 'Clear history' : '清空历史' });
    clr.textContent = tt('clear');
    clr.addEventListener('click', function () { history.clear(); box.innerHTML = ''; });
    hd.appendChild(t); hd.appendChild(clr);
    wrap.appendChild(hd);
    var ul = el('ul', { class: 'tbk-history-list' });
    arr.forEach(function (it) {
      var li = el('li', {});
      var btn = el('button', { type: 'button', class: 'tbk-history-item' });
      var when = el('span', { class: 'tbk-history-time' });
      when.textContent = fmtTime(it.t);
      var body = el('span', { class: 'tbk-history-body' });
      var parts = [];
      for (var k in it.d) {
        if (!Object.prototype.hasOwnProperty.call(it.d, k)) continue;
        parts.push(k + ' ' + (typeof it.d[k] === 'number' ? fmt(it.d[k]) : it.d[k]));
      }
      body.textContent = parts.join(' · ');
      btn.appendChild(when); btn.appendChild(body);
      btn.addEventListener('click', function () { if (typeof onPick === 'function') { try { onPick(it.d); } catch (e) {} } });
      li.appendChild(btn);
      ul.appendChild(li);
    });
    wrap.appendChild(ul);
    box.appendChild(wrap);
    return wrap;
  };

  /* ============================ 导出 / 复制 ============================ */

  var exp = {};

  function download(text, filename, mime) {
    try {
      var blob = new Blob([text], { type: (mime || 'text/plain') + ';charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url; a.download = filename;
      document.body.appendChild(a); a.click();
      setTimeout(function () { a.parentNode.removeChild(a); URL.revokeObjectURL(url); }, 200);
      return true;
    } catch (e) { toast('下载失败', 'error'); return false; }
  }

  exp.csv = function (filename, rows) {
    var lines = (rows || []).map(function (r) {
      return r.map(function (c) {
        var v = c == null ? '' : String(c);
        return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
      }).join(',');
    }).join('\n');
    // BOM 保证 Excel 打开中文不乱码
    return download('\ufeff' + lines, filename, 'text/csv');
  };

  exp.text = function (filename, text) { return download(text, filename, 'text/plain'); };

  exp.svg = function (filename, svgEl) {
    try {
      var src = svgEl && svgEl.outerHTML ? svgEl.outerHTML : '';
      if (!src) return false;
      return download('<?xml version="1.0" encoding="UTF-8"?>\n' + src, filename, 'image/svg+xml');
    } catch (e) { return false; }
  };

  exp.copy = function (text) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { toast('已复制'); }, function () { fallbackCopy(text); });
        return;
      }
    } catch (e) {}
    fallbackCopy(text);
  };

  function fallbackCopy(text) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;left:-9999px;opacity:0;';
      document.body.appendChild(ta); ta.select();
      document.execCommand('copy');
      ta.parentNode.removeChild(ta);
      toast('已复制');
    } catch (e) { toast('复制失败，请手动选择', 'error'); }
  }

  /* ============================ 分享 / 回填 ============================ */

  var share = {};

  /** 生成带参数的分享链接（写进 hash，不发服务器） */
  share.link = function (obj) {
    try {
      var q = [];
      for (var k in obj) {
        if (!Object.prototype.hasOwnProperty.call(obj, k)) continue;
        q.push(encodeURIComponent(k) + '=' + encodeURIComponent(obj[k]));
      }
      return location.origin + location.pathname + '#' + q.join('&');
    } catch (e) { return ''; }
  };

  share.copyLink = function (obj) {
    var u = share.link(obj);
    if (!u) return;
    exp.copy(u);
    try { history.replaceState(null, '', u); } catch (e) {}
  };

  /** 读取 hash 参数（分享链接回填用） */
  share.params = function () {
    var out = {};
    try {
      var h = (location.hash || '').replace(/^#/, '');
      if (!h) return out;
      h.split('&').forEach(function (kv) {
        var i = kv.indexOf('=');
        if (i < 1) return;
        out[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1));
      });
    } catch (e) {}
    return out;
  };

  /* ============================ 速查矩阵 ============================ */

  var matrix = {};

  /** rows: 二维数组；可搜索 + 单击复制单元格 */
  matrix.table = function (host, cfg) {
    var box = $(host);
    if (!box) return null;
    cfg = cfg || {};
    var head = cfg.head || [], rows = cfg.rows || [];
    box.innerHTML = '';
    if (cfg.search !== false) {
      var inp = el('input', { type: 'search', class: 'tbk-matrix-search', placeholder: tt('search'), 'aria-label': isEn() ? 'Search table' : '搜索表格' });
      box.appendChild(inp);
      inp.addEventListener('input', function () {
        var kw = inp.value.trim().toLowerCase();
        var trs = table.querySelectorAll('tbody tr');
        for (var i = 0; i < trs.length; i++) {
          trs[i].style.display = !kw || trs[i].textContent.toLowerCase().indexOf(kw) >= 0 ? '' : 'none';
        }
      });
    }
    var table = el('table', { class: 'tbk-matrix' });
    if (head.length) {
      var thead = el('thead', {}), tr = el('tr', {});
      head.forEach(function (h) { var th = el('th', {}); th.textContent = h; tr.appendChild(th); });
      thead.appendChild(tr); table.appendChild(thead);
    }
    var tbody = el('tbody', {});
    rows.forEach(function (r) {
      var tr = el('tr', {});
      r.forEach(function (c) {
        var td = el('td', {});
        td.textContent = c;
        td.title = tt('copyTip');
        td.addEventListener('click', function () { exp.copy(String(c)); });
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    box.appendChild(table);
    return table;
  };

  /* ============================ 声明式挂载 ============================ */

  function mountDeclared() {
    try {
      var nodes = document.querySelectorAll('[data-tb]');
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        var kind = n.getAttribute('data-tb');
        if (kind === 'history') history.mount(n);
        else if (kind === 'preset') {
          var raw = n.getAttribute('data-tb-presets');
          var list = null;
          try { list = raw ? JSON.parse(raw) : null; } catch (e) { list = null; }
          if (list) preset.bar(n, list);
        }
      }
    } catch (e) {}
  }

  function injectStyles() {
    if (document.getElementById('tbk-style')) return;
    var css = [
      '.tbk-presets{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 12px;}',
      '.tbk-presets-tip{font-size:12px;color:var(--text-muted,#6B7280);}',
      '.tbk-preset-btn{font-size:12px;padding:5px 12px;border-radius:999px;border:1px solid var(--border,#E5E7EB);',
      'background:var(--card-bg,#fff);color:var(--text,#374151);cursor:pointer;transition:.15s;}',
      '.tbk-preset-btn:hover{border-color:var(--primary,#FF6B35);color:var(--primary,#FF6B35);}',
      '.tbk-preset-btn.active{background:var(--primary,#FF6B35);color:#fff;border-color:var(--primary,#FF6B35);}',
      '.tbk-history{margin-top:10px;border-top:1px dashed var(--border,#E5E7EB);padding-top:8px;}',
      '.tbk-history-hd{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--text-muted,#6B7280);}',
      '.tbk-link-btn{border:none;background:none;color:var(--text-muted,#6B7280);font-size:12px;cursor:pointer;text-decoration:underline;}',
      '.tbk-history-list{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-direction:column;gap:4px;}',
      '.tbk-history-item{display:flex;gap:10px;width:100%;text-align:left;border:none;background:transparent;',
      'font-size:12px;color:var(--text,#374151);padding:4px 6px;border-radius:6px;cursor:pointer;}',
      '.tbk-history-item:hover{background:var(--bg-subtle,#F9FAFB);}',
      '.tbk-history-time{color:var(--text-muted,#6B7280);flex:0 0 auto;}',
      '.tbk-history-body{flex:1 1 auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}',
      '.tbk-matrix-search{width:100%;margin-bottom:8px;padding:6px 10px;font-size:13px;border-radius:8px;',
      'border:1px solid var(--border,#E5E7EB);background:var(--card-bg,#fff);color:var(--text,#374151);}',
      '.tbk-matrix{width:100%;border-collapse:collapse;font-size:13px;}',
      '.tbk-matrix th,.tbk-matrix td{border:1px solid var(--border,#E5E7EB);padding:6px 8px;text-align:left;}',
      '.tbk-matrix td{cursor:copy;}',
      '.tbk-matrix tbody tr:hover td{background:var(--bg-subtle,#F9FAFB);}'
    ].join('');
    var st = document.createElement('style');
    st.id = 'tbk-style';
    st.textContent = css;
    document.head.appendChild(st);
  }

  function init() {
    injectStyles();
    mountDeclared();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.TBKit = {
    version: '1.0.0',
    util: { fmt: fmt, num: num, toast: toast, el: el, svg: s, palette: PALETTE },
    chart: chart,
    preset: preset,
    history: history,
    export: exp,
    share: share,
    matrix: matrix
  };
  window.TBK = TBK;
})();
