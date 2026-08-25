/* B5-08 本地隐私数据管理（纯前端，不上传任何数据）
 *
 * 暴露 window.ToolBox.Privacy：
 *   list()    -> [{key, kind, size, preview}]
 *   clear()   -> 清空全部本地使用数据（收藏/历史/周报/工具链/AI 配额/主题/语言）
 *   export()  -> 触发下载当前本地数据 JSON（用户可自检）
 *   open()    -> 打开管理弹窗
 *
 * 默认不向任何第三方发送用户输入、查询内容或个人标识。
 */
(function (global) {
  'use strict';

  // 工具产生的本地数据 key 模式
  var KNOWN = [
    'favTools', 'recentTools',
    'toolbox_chain_run', 'toolbox_chain_payload',
    'toolbox_ai_unlocked',
    'theme', 'toolbox_lang',
    'toolbox_privacy_ack'
  ];
  var QUOTA_RE = /^toolbox_ai_quota_\d{8}$/;

  function isOwn(key) {
    if (KNOWN.indexOf(key) >= 0) return true;
    if (QUOTA_RE.test(key)) return true;
    return false;
  }

  function kindOf(key) {
    if (key === 'favTools') return '收藏';
    if (key === 'recentTools') return '最近使用';
    if (key === 'toolbox_chain_run' || key === 'toolbox_chain_payload') return '工具链状态';
    if (key === 'toolbox_ai_unlocked') return 'AI 解锁';
    if (QUOTA_RE.test(key)) return 'AI 每日配额';
    if (key === 'theme') return '主题';
    if (key === 'toolbox_lang') return '语言';
    if (key === 'toolbox_privacy_ack') return '隐私确认';
    return '其他';
  }

  function list() {
    var out = [];
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (!isOwn(k)) continue;
      var v = localStorage.getItem(k) || '';
      var preview = v.length > 60 ? v.slice(0, 60) + '…' : v;
      out.push({ key: k, kind: kindOf(k), size: v.length, preview: preview });
    }
    out.sort(function (a, b) { return a.kind.localeCompare(b.kind); });
    return out;
  }

  function clear() {
    var removed = [];
    var toDel = [];
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (isOwn(k)) toDel.push(k);
    }
    toDel.forEach(function (k) { localStorage.removeItem(k); removed.push(k); });
    return removed;
  }

  function exportData() {
    var data = {};
    list().forEach(function (it) { data[it.key] = localStorage.getItem(it.key); });
    var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'toolbox-local-data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function openModal() {
    var existing = document.getElementById('tb-privacy-modal');
    if (existing) { existing.style.display = 'flex'; return; }
    var items = list();
    var rows = items.length
      ? items.map(function (it) {
          return '<tr><td>' + esc(it.kind) + '</td><td><code>' + esc(it.key) +
            '</code></td><td>' + it.size + ' B</td><td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' +
            esc(it.preview) + '</td></tr>';
        }).join('')
      : '<tr><td colspan="4" style="text-align:center;color:var(--muted)">暂无本地数据</td></tr>';

    var hasMetrics = !!(global.ToolBox && global.ToolBox.Metrics);
    var optin = hasMetrics && global.ToolBox.Metrics.enabled();
    var mSummary = hasMetrics ? global.ToolBox.Metrics.summary() : { total: 0, by: {} };
    var mLine = '本机累计事件 ' + mSummary.total + ' 条';

    var box = document.createElement('div');
    box.id = 'tb-privacy-modal';
    box.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:9999;padding:16px';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-labelledby', 'tb-priv-title');
    box.innerHTML =
      '<div style="background:var(--card);color:var(--text);max-width:640px;width:100%;border-radius:16px;padding:20px;box-shadow:0 20px 60px rgba(0,0,0,.3);max-height:90vh;overflow:auto">' +
        '<h3 id="tb-priv-title" style="margin:0 0 6px">🗂️ 本地数据管理</h3>' +
        '<p style="color:var(--muted);font-size:13px;margin:0 0 12px">ToolBox 纯前端运行，以下数据仅存于你的浏览器，不会上传任何服务器。</p>' +
        '<div style="overflow:auto"><table style="width:100%;border-collapse:collapse;font-size:13px">' +
          '<thead><tr style="text-align:left;color:var(--muted)"><th>类型</th><th>键</th><th>大小</th><th>预览</th></tr></thead>' +
          '<tbody>' + rows + '</tbody></table></div>' +
        (hasMetrics ?
        '<div style="margin-top:16px;padding:14px;border:1px solid var(--border);border-radius:12px;background:var(--bg)">' +
          '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">' +
            '<div style="font-size:13px;font-weight:600">📊 匿名使用指标（可选）</div>' +
            '<button id="tb-priv-metrics-toggle" aria-label="开启或关闭匿名使用指标" style="padding:6px 12px;border:1px solid var(--border);border-radius:999px;background:var(--card);color:var(--text);cursor:pointer;font-size:12px">' +
              (optin ? '● 已开启 · 点击关闭' : '○ 已关闭 · 点击开启') +
            '</button>' +
          '</div>' +
          '<p style="color:var(--muted);font-size:12px;line-height:1.7;margin:8px 0 0">仅记录工具打开/复制/下载/指南点击/工具链完成/AI 推理成败等匿名事件，含工具文件名与行业，<b>绝不含用户输入、查询内容或个人标识</b>，数据只存在本机、可随时清空。默认关闭。</p>' +
          '<p id="tb-priv-metrics-summary" style="font-size:12px;margin:8px 0 0;color:var(--text)">' + mLine + '</p>' +
          '<button id="tb-priv-metrics-clear" aria-label="清空匿名使用指标" style="margin-top:8px;padding:5px 12px;border:1px solid var(--border);border-radius:10px;background:var(--card);color:var(--text);cursor:pointer;font-size:12px">清空指标数据</button>' +
        '</div>' : '') +
        '<div style="display:flex;gap:8px;margin-top:16px;flex-wrap:wrap">' +
          '<button id="tb-priv-export" aria-label="导出本地数据备份" style="padding:8px 14px;border:1px solid var(--border);border-radius:10px;background:var(--bg);color:var(--text);cursor:pointer">导出备份</button>' +
          '<button id="tb-priv-clear" aria-label="清空全部本地数据" style="padding:8px 14px;border:none;border-radius:10px;background:#EF4444;color:#fff;cursor:pointer">清空全部本地数据</button>' +
          '<button id="tb-priv-close" aria-label="关闭本地数据管理弹窗" style="padding:8px 14px;border:1px solid var(--border);border-radius:10px;background:var(--card);color:var(--text);cursor:pointer">关闭</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(box);

    var prevFocus = document.activeElement;
    function close() {
      box.style.display = 'none';
      document.removeEventListener('keydown', onKey);
      if (prevFocus && prevFocus.focus) { try { prevFocus.focus(); } catch (e) {} }
    }
    function onKey(e) { if (e.key === 'Escape') { e.preventDefault(); close(); } }
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.getElementById('tb-priv-close').onclick = close;
    document.getElementById('tb-priv-export').onclick = function () { exportData(); };
    document.getElementById('tb-priv-clear').onclick = function () {
      var removed = clear();
      alert('已清空 ' + removed.length + ' 项本地数据');
      close();
      if (global.ToolBox && global.ToolBox.refreshNav) global.ToolBox.refreshNav();
    };
    var toggleBtn = document.getElementById('tb-priv-metrics-toggle');
    if (toggleBtn) {
      toggleBtn.onclick = function () {
        if (!global.ToolBox || !global.ToolBox.Metrics) return;
        var now = !global.ToolBox.Metrics.enabled();
        global.ToolBox.Metrics.setEnabled(now);
        toggleBtn.textContent = now ? '● 已开启 · 点击关闭' : '○ 已关闭 · 点击开启';
      };
    }
    var mClearBtn = document.getElementById('tb-priv-metrics-clear');
    if (mClearBtn) {
      mClearBtn.onclick = function () {
        if (global.ToolBox && global.ToolBox.Metrics) global.ToolBox.Metrics.clear();
        var s = document.getElementById('tb-priv-metrics-summary');
        if (s) s.textContent = '本机累计事件 0 条';
      };
    }
    document.addEventListener('keydown', onKey);
    var closeBtn = document.getElementById('tb-priv-close');
    if (closeBtn && closeBtn.focus) closeBtn.focus();
  }

  global.ToolBox = global.ToolBox || {};
  global.ToolBox.Privacy = { list: list, clear: clear, export: exportData, open: openModal };
})(window);
