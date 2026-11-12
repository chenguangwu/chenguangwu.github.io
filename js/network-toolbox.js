/* network-toolbox.js — 13 项纯前端网络工具
 * 无后端、无密钥、不埋点。所有结果只写当前页与内存；不写入第三方。
 */
(function () {
  'use strict';

  function isEn() {
    if (/(?:^|[?&])lang=en/i.test(location.search)) return true;
    return !!(window.I18n && typeof I18n.get === 'function' && I18n.get() === 'en-US');
  }
  function t(zh, en) { return isEn() ? en : zh; }
  function dash(v) { return (v === undefined || v === null || v === '') ? '—' : String(v); }
  function iso() { return new Date().toISOString(); }

  // 每个工具：{ state, display, copy }
  var ST = Object.create(null);
  var RUNNING = Object.create(null);

  function render(id, state, display, copyText) {
    var box = document.getElementById('result-' + id);
    var card = document.getElementById('card-' + id);
    var badge = card && card.querySelector('.nt-badge');
    var label = { idle: t('空态', 'Idle'), loading: t('加载中', 'Loading'), ok: t('成功', 'OK'), error: t('失败', 'Error') };
    if (box) { box.textContent = display; box.setAttribute('data-s', state); }
    if (badge) { badge.setAttribute('data-s', state); badge.textContent = label[state] || state; }
    ST[id] = { state: state, display: display, copy: copyText === undefined ? display : copyText };
    var btn = card && card.querySelector('[data-run]');
    if (btn) {
      if (state === 'error') btn.textContent = t('重试', 'Retry');
      else if (state === 'ok' && btn.textContent === t('重试', 'Retry')) btn.textContent = t('重新执行', 'Run again');
    }
    // 仅成功结果落本机历史；隐私模式/禁用存储时静默跳过，不影响工具本身
    if (state === 'ok') {
      var old = loadHistory()[id];
      ST[id].prevCopy = old ? old.copy : '';   // 写入前保留上一次，供「对比上次」
      ST[id].prevTime = old ? old.time : 0;
      saveHistory(id, ST[id].copy);
    }
    renderHistory();
  }

  // ---- 本机历史（localStorage）：只存最近一次成功结果，绝不上传 ----
  var HIST_KEY = 'ntHist_v1';
  function loadHistory() {
    try { return JSON.parse(localStorage.getItem(HIST_KEY) || '{}') || {}; }
    catch (e) { return {}; }
  }
  function saveHistory(id, copyText) {
    try {
      var h = loadHistory();
      h[id] = { copy: String(copyText || ''), time: Date.now() };
      localStorage.setItem(HIST_KEY, JSON.stringify(h));
    } catch (e) { /* 存储不可用：静默跳过 */ }
  }
  function fmtTime(ts) {
    if (!ts) return '—';
    try { return new Date(ts).toLocaleString(); } catch (e) { return String(ts); }
  }
  function shortSumm(s) {
    s = String(s || '').replace(/\s+/g, ' ').trim();
    return s.length > 80 ? s.slice(0, 80) + '…' : (s || '—');
  }
  function diffLines(a, b) {
    var al = String(a || '').split('\n'), bl = String(b || '').split('\n');
    var out = [], n = Math.max(al.length, bl.length);
    for (var i = 0; i < n; i++) {
      if (al[i] === bl[i]) out.push('  ' + (al[i] === undefined ? '' : al[i]));
      else {
        if (al[i] !== undefined) out.push('- ' + al[i]);
        if (bl[i] !== undefined) out.push('+ ' + bl[i]);
      }
    }
    return out.join('\n');
  }
  function renderHistory() {
    var body = document.getElementById('ntHistoryBody');
    if (!body) return;
    var hist = loadHistory();
    var ids = Object.keys(RUNNERS);
    var rows = [];
    var label = { idle: t('空态', 'Idle'), loading: t('加载中', 'Loading'), ok: t('成功', 'OK'), error: t('失败', 'Error') };
    for (var i = 0; i < ids.length; i++) {
      var id = ids[i];
      var cur = ST[id];
      var prev = hist[id];
      if (!cur && !prev) continue;
      var state = cur ? cur.state : 'idle';
      var stateTxt = label[state] || state;
      // 「上次」= 本次写入前保存的 prevCopy；若无本次运行则用 localStorage 里的最近成功结果
      var lastCopy = (cur && cur.prevCopy) ? cur.prevCopy : (prev ? prev.copy : '');
      var lastTime = (cur && cur.prevTime) ? cur.prevTime : (prev ? prev.time : 0);
      var summ = lastCopy ? shortSumm(lastCopy) : '—';
      var time = fmtTime(lastTime);
      var canDiff = !!(cur && cur.copy && cur.prevCopy);
      var name = t(TITLE_ZH[id] || id, TITLE_EN[id] || id);
      var op = canDiff
        ? '<button type="button" class="btn" data-diff="' + id + '">' + t('对比上次', 'Compare') + '</button>'
        : '—';
      rows.push('<tr><td>' + name + '</td><td data-s="' + state + '">' + stateTxt + '</td><td>' + time + '</td>' +
        '<td>' + esc(summ) + '</td><td>' + op + '</td></tr>');
    }
    if (!rows.length) {
      body.innerHTML = '<tr><td colspan="5">' + t('尚未有运行记录，先点上面任意工具的「执行」按钮。', 'No run history yet. Run any tool above to record a result.') + '</td></tr>';
    } else {
      body.innerHTML = rows.join('');
    }
  }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function showDiff(id, btn) {
    var s = ST[id];
    if (!s || !s.prevCopy) return;
    var body = document.getElementById('ntHistoryBody');
    if (!body) return;
    var tr = btn.closest ? btn.closest('tr') : null;
    var next = tr && tr.nextElementSibling;
    if (next && next.classList && next.classList.contains('nt-diff-row')) {
      next.remove(); return; // 再点收起
    }
    var d = diffLines(s.prevCopy, s.copy);
    var row = document.createElement('tr');
    row.className = 'nt-diff-row';
    var td = document.createElement('td');
    td.colSpan = 5;
    var pre = document.createElement('div');
    pre.className = 'nt-hist-diff';
    pre.textContent = t('- 上次  /  + 本次', '- previous  /  + current') + '\n' + d;
    td.appendChild(pre);
    row.appendChild(td);
    if (tr && tr.parentNode) tr.parentNode.insertBefore(row, next || null);
  }
  var TITLE_ZH = { t1: 'T1 多源 IP 查询', t2: 'T2 任意 IP 查询', t3: 'T3 本机内网 IP', t4: 'T4 目标站点可达性',
    t5: 'T5 自定义 URL 可达性', t6: 'T6 WebRTC 泄露检测', t7: 'T7 NAT 类型推断', t8: 'T8 DNS 出口查询',
    t9: 'T9 CDN 边缘节点探测', t10: 'T10 代理分流规则测试', t11: 'T11 下行 + 延迟测速',
    t12: 'T12 浏览器指纹', t13: 'T13 服务状态看板' };
  var TITLE_EN = { t1: 'T1 Multi-source IP', t2: 'T2 Arbitrary IP', t3: 'T3 Local Private IP',
    t4: 'T4 Site Reachability', t5: 'T5 Custom URL', t6: 'T6 WebRTC Leak', t7: 'T7 NAT Type',
    t8: 'T8 DNS Egress', t9: 'T9 CDN Edge', t10: 'T10 Proxy Routing', t11: 'T11 Speed Test',
    t12: 'T12 Browser Fingerprint', t13: 'T13 Service Status' };

  function errInfo(e, kind) {
    if (kind === 'timeout' || (e && (e.name === 'AbortError' || e.name === 'TimeoutError'))) {
      return t('超时', 'Timeout') + (e && e.message ? '：' + e.message : '');
    }
    if (e && (e.status === 429 || /429/.test(String(e.message)))) return t('接口限流', 'Rate limited');
    if (e instanceof SyntaxError) return t('格式错误', 'Invalid format') + '：' + (e.message || '');
    if (e && /JSON|parse/i.test(String(e.message))) return t('格式错误', 'Invalid format') + '：' + e.message;
    return t('网络错误', 'Network error') + (e && e.message ? '：' + e.message : '');
  }

  // 统一超时封装：AbortController 取消，区分超时与网络错误
  function fetchTimed(url, ms, opts) {
    var ctrl = (typeof AbortController === 'function') ? new AbortController() : null;
    var timer = null;
    var init = Object.assign({}, opts || {});
    if (ctrl) init.signal = ctrl.signal;
    var p = fetch(url, init);
    if (!ctrl) return p;
    return new Promise(function (resolve, reject) {
      timer = setTimeout(function () { ctrl.abort(); }, ms);
      p.then(function (r) { clearTimeout(timer); resolve(r); },
        function (e) { clearTimeout(timer); reject(e); });
    });
  }

  async function fetchJson(url, ms) {
    var r = await fetchTimed(url, ms, { cache: 'no-store' });
    if (!r.ok) { var e = new Error('HTTP ' + r.status); e.status = r.status; throw e; }
    return await r.json();
  }

  function median(nums) {
    if (!nums.length) return 0;
    var a = nums.slice().sort(function (x, y) { return x - y; });
    var m = Math.floor(a.length / 2);
    return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }
  function legacyCopy(text) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    } catch (e) { return false; }
  }
  function toast(msg, ok) {
    try { if (window.ToolBox && typeof ToolBox.showToast === 'function') ToolBox.showToast(msg, ok ? 'success' : 'danger'); } catch (e) { /* 忽略 */ }
  }

  function candidateParts(candidate) {
    var tok = String(candidate || '').trim().split(/\s+/);
    var idx = tok.indexOf('typ');
    var type = idx >= 0 && tok[idx + 1] ? tok[idx + 1] : 'host';
    var proto = tok[2] || 'udp';
    var ip = tok[4] || '';
    var port = tok[5] || '';
    return { ip: ip, port: port, type: type, proto: proto, raw: String(candidate || '') };
  }

  // ================= T1 多源 IP 查询 =================
  var IP_SOURCES = [
    { name: 'ipwho.is', url: 'https://ipwho.is/', parse: function (j) {
      return { ip: j.ip, version: j.type ? String(j.type).replace(/[^46]/g, '') : (j.ip && j.ip.indexOf(':') >= 0 ? '6' : '4'),
        country: j.country, region: j.region, city: j.city,
        isp: j.connection && j.connection.isp, asn: j.connection && j.connection.asn, timezone: j.timezone, domain: null };
    } },
    { name: 'ipapi.co', url: 'https://ipapi.co/json/', parse: function (j) {
      return { ip: j.ip, version: j.ip && j.ip.indexOf(':') >= 0 ? '6' : '4', country: j.country_name,
        region: j.region, city: j.city, isp: j.org, asn: j.asn, timezone: j.timezone, domain: null };
    } },
    { name: 'api.ip.sb', url: 'https://api.ip.sb/geoip', parse: function (j) {
      return { ip: j.ip, version: j.ip && j.ip.indexOf(':') >= 0 ? '6' : '4', country: j.country,
        region: j.region, city: j.city, isp: j.isp, asn: j.asn, timezone: j.timezone, domain: null };
    } },
    { name: 'api64.ipify.org', url: 'https://api64.ipify.org?format=json', parse: function (j) {
      return { ip: j.ip, version: j.ip && j.ip.indexOf(':') >= 0 ? '6' : '4', country: null,
        region: null, city: null, isp: null, asn: null, timezone: null, domain: null };
    } }
  ];

  function t1Text(d) {
    return 'IP: ' + dash(d.ip) + '\n' +
      t('版本', 'Version') + ': IPv' + dash(d.version) + '\n' +
      t('位置', 'Location') + ': ' + dash(d.country) + ' / ' + dash(d.region) + ' / ' + dash(d.city) + '\n' +
      'ISP: ' + dash(d.isp) + '\n' +
      'ASN: ' + dash(d.asn) + '\n' +
      t('时区', 'Timezone') + ': ' + dash(d.timezone) + '\n' +
      t('来源', 'Source') + ': ' + dash(d.source) + '\n' +
      t('时间', 'Time') + ': ' + d.time;
  }

  async function runT1() {
    render('t1', 'loading', t('正在查询公网 IP…', 'Querying public IP…'));
    var data = null, source = '', lastErr = null;
    for (var i = 0; i < IP_SOURCES.length; i++) {
      var s = IP_SOURCES[i];
      try { data = s.parse(await fetchJson(s.url, 6000)); source = s.name; break; }
      catch (e) { lastErr = e; }
    }
    if (!data) {
      render('t1', 'error', t('查询失败', 'Query failed') + '：' + errInfo(lastErr));
      return;
    }
    data.source = source; data.time = iso();
    ST.t1PublicIp = data.ip;
    render('t1', 'ok', t1Text(data), t1Text(data));
    // IPv6 单独探测，失败静默跳过
    try {
      var r = await fetchTimed('https://v6.ident.me', 6000, { cache: 'no-store' });
      var v6 = (await r.text()).trim();
      if (v6 && v6.indexOf(':') > 0) {
        ST.t1IPv6 = v6;
        var box = document.getElementById('result-t1');
        if (box) box.textContent += '\nIPv6: ' + v6;
        ST.t1.copy += '\nIPv6: ' + v6;
        if (ST.t1.display.indexOf('IPv6:') < 0) ST.t1.display += '\nIPv6: ' + v6;
        // IPv6 行是 render 之后异步追加的，需重写历史，保证存档与展示/复制完全一致
        saveHistory('t1', ST.t1.copy);
        renderHistory();
      }
    } catch (e) { /* 无 IPv6 时静默跳过 */ }
  }

  // ================= T2 任意 IP 查询 =================
  function validIp(s) {
    s = String(s || '').trim();
    if (/^(25[0-5]|2[0-4]\d|1?\d?\d)(\.(25[0-5]|2[0-4]\d|1?\d?\d)){3}$/.test(s)) return '4';
    if (/^[0-9A-Fa-f:]+$/.test(s) && s.indexOf(':') >= 0 && !/::.*::/.test(s)) {
      var parts = s.split('::');
      var left = parts[0] ? parts[0].split(':').length : 0;
      var right = parts[1] ? parts[1].split(':').length : 0;
      if (parts.length === 1 ? left === 8 : left + right < 8) return '6';
    }
    return '';
  }
  function t2Text(ip, d) {
    return t('查询 IP', 'Queried IP') + ': ' + ip + '\n' +
      t('归属', 'Region') + ': ' + dash(d.country) + ' / ' + dash(d.region) + ' / ' + dash(d.city) + '\n' +
      'ISP: ' + dash(d.isp) + '\n' +
      'ASN: ' + dash(d.asn) + '\n' +
      t('域名', 'Domain') + ': ' + dash(d.domain);
  }
  async function runT2() {
    var input = document.getElementById('t2-ip');
    var ip = input ? input.value.trim() : '';
    if (!validIp(ip)) {
      render('t2', 'error', t('IP 格式不合法，未发送请求。', 'Invalid IP format; no request sent.'));
      return;
    }
    render('t2', 'loading', t('正在查询…', 'Querying…'));
    var d = null, lastErr = null;
    try {
      var j = await fetchJson('https://ipwho.is/' + encodeURIComponent(ip), 6000);
      d = { country: j.country, region: j.region, city: j.city,
        isp: j.connection && j.connection.isp, asn: j.connection && j.connection.asn,
        domain: (j.connection && j.connection.domain) || null };
      if (j.success === false) throw new Error(j.message || 'not found');
    } catch (e) {
      lastErr = e;
      try {
        var k = await fetchJson('https://ipapi.co/' + encodeURIComponent(ip) + '/json/', 6000);
        d = { country: k.country_name, region: k.region, city: k.city, isp: k.org, asn: k.asn, domain: null };
      } catch (e2) { lastErr = e2; }
    }
    if (!d) { render('t2', 'error', t('查询失败', 'Query failed') + '：' + errInfo(lastErr)); return; }
    var text = t2Text(ip, d);
    render('t2', 'ok', text, text);
  }

  // ================= T3 本机内网 IP =================
  function collectCandidates(config, seconds) {
    return new Promise(function (resolve) {
      var out = [], done = false;
      if (typeof RTCPeerConnection !== 'function') { resolve(out); return; }
      var pc;
      try { pc = new RTCPeerConnection(config || { iceServers: [] }); }
      catch (e) { resolve(out); return; }
      function finish() {
        if (done) return; done = true;
        try { pc.close(); } catch (e) {}
        resolve(out);
      }
      pc.onicecandidate = function (ev) {
        if (!ev.candidate) { finish(); return; }
        out.push(candidateParts(ev.candidate.candidate));
      };
      try {
        pc.createDataChannel('nt');
        pc.createOffer().then(function (o) { return pc.setLocalDescription(o); }).catch(finish);
      } catch (e) { finish(); }
      setTimeout(finish, seconds * 1000);
    });
  }
  async function runT3() {
    render('t3', 'loading', t('正在收集本机地址…', 'Collecting local addresses…'));
    var all = await collectCandidates({ iceServers: [] }, 3);
    var hosts = all.filter(function (c) { return c.type === 'host'; });
    if (!hosts.length) { render('t3', 'error', t('未获取到 host candidate（浏览器可能禁用了 WebRTC 或已启用 mDNS 混淆）', 'No host candidate (WebRTC disabled or mDNS obfuscated)')); return; }
    var lan = hosts.filter(function (c) { return !/\.local$/i.test(c.ip); });
    var mdns = hosts.filter(function (c) { return /\.local$/i.test(c.ip); });
    var text = t('内网 IP（host candidate）:', 'Private IPs (host candidate):') + '\n' +
      (lan.length ? lan.map(function (c) { return c.ip + ' (' + c.proto + ')'; }).join('\n') : '—') + '\n\n' +
      t('mDNS 混淆地址:', 'mDNS obfuscated:') + '\n' +
      (mdns.length ? mdns.map(function (c) { return c.ip + ' (' + c.proto + ')'; }).join('\n') : '—');
    render('t3', 'ok', text, text);
  }

  // ================= T4 favicon 可达性 =================
  function probeImage(url, timeout) {
    return new Promise(function (resolve) {
      var img = new Image(), done = false, t0 = (performance && performance.now) ? performance.now() : Date.now();
      function fin(status) {
        if (done) return; done = true;
        var now = (performance && performance.now) ? performance.now() : Date.now();
        resolve({ status: status, ms: Math.round(now - t0) });
      }
      img.onload = function () { fin('ok'); };
      img.onerror = function () { fin('fail'); };
      img.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + '_=' + Date.now();
      setTimeout(function () { fin('timeout'); }, timeout);
    });
  }
  var T4_TARGETS = [
    { name: 'Google', url: 'https://www.google.com/favicon.ico' },
    { name: 'GitHub', url: 'https://github.com/favicon.ico' },
    { name: 'Cloudflare', url: 'https://www.cloudflare.com/favicon.ico' },
    { name: 'OpenAI', url: 'https://openai.com/favicon.ico' }
  ];
  async function probeGroup(targets) {
    // 并发上限 5
    var out = [];
    for (var i = 0; i < targets.length; i += 5) {
      var batch = targets.slice(i, i + 5);
      var settled = await Promise.allSettled(batch.map(function (x) { return probeImage(x.url, 8000); }));
      settled.forEach(function (r, j) {
        out.push({ name: batch[j].name, group: batch[j].group || (batch[j].cn ? 'cn' : 'global'),
          status: r.status === 'fulfilled' ? r.value.status : 'fail', ms: r.status === 'fulfilled' ? r.value.ms : 0 });
      });
    }
    return out;
  }
  async function runT4() {
    render('t4', 'loading', t('正在探测 4 个站点…', 'Probing 4 sites…'));
    var rows = await probeGroup(T4_TARGETS);
    var pass = rows.filter(function (r) { return r.status === 'ok'; }).length;
    var lines = rows.map(function (r) {
      var markS = r.status === 'ok' ? '✅ ' + t('可达', 'Reachable') : (r.status === 'timeout' ? '⏱ ' + t('超时', 'Timeout') : '❌ ' + t('不可达', 'Unreachable'));
      return r.name + ': ' + markS + ' ' + r.ms + 'ms';
    });
    var text = lines.join('\n') + '\n' + t('汇总', 'Summary') + ': ' + pass + '/' + rows.length + ' ' + t('可达', 'reachable');
    render('t4', 'ok', text, text);
  }

  // ================= T5 自定义 URL =================
  async function runT5() {
    var input = document.getElementById('t5-url');
    var url = input ? input.value.trim() : '';
    if (!url) { render('t5', 'error', t('请输入 URL', 'Enter a URL')); return; }
    if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
    render('t5', 'loading', t('正在探测…', 'Probing…'));
    var t0 = (performance && performance.now) ? performance.now() : Date.now();
    var method = 'fetch no-cors', status = '', lastErr = null;
    try {
      await fetchTimed(url, 8000, { mode: 'no-cors', cache: 'no-store' });
      status = t('可达', 'Reachable');
    } catch (e) {
      lastErr = e;
      var origin;
      try { origin = new URL(url).origin; } catch (x) { origin = url; }
      var r = await probeImage(origin + '/favicon.ico', 8000);
      method = 'image';
      status = r.status === 'ok' ? t('可达', 'Reachable') : (r.status === 'timeout' ? t('超时', 'Timeout') : t('不可达', 'Unreachable'));
    }
    var now = (performance && performance.now) ? performance.now() : Date.now();
    var text = 'URL: ' + url + '\n' + t('方式', 'Method') + ': ' + method + '\n' +
      t('结果', 'Result') + ': ' + status + '\n' + t('耗时', 'Time') + ': ' + Math.round(now - t0) + 'ms';
    render('t5', status === t('不可达', 'Unreachable') ? 'error' : 'ok', text, text);
  }

  // ================= T6 WebRTC 泄露 =================
  async function runT6() {
    render('t6', 'loading', t('正在收集 ICE 候选…', 'Collecting ICE candidates…'));
    var stun = new URLSearchParams(location.search).get('stun') || 'stun:stun.l.google.com:19302';
    var list = await collectCandidates({ iceServers: [{ urls: stun }] }, 5);
    if (!list.length) { render('t6', 'error', t('未获取到 ICE 候选（WebRTC 不可用或 STUN 不可达）', 'No ICE candidates')); return; }
    var pub = ST.t1PublicIp || '—';
    var srflx = list.filter(function (c) { return c.type === 'srflx'; });
    var consistent = (!pub || pub === '—') ? t('未获取', 'Unavailable') :
      (srflx.some(function (c) { return c.ip === pub; }) ? t('一致', 'Match') : t('不一致', 'Mismatch'));
    var priv = list.filter(function (c) { return c.type === 'host'; }).map(function (c) { return c.ip; });
    var text = t('WebRTC ICE 候选:', 'WebRTC ICE candidates:') + '\n' +
      list.map(function (c) { return c.ip + ' type=' + c.type + ' proto=' + c.proto; }).join('\n') + '\n' +
      t('公网 IP（来自 T1）:', 'Public IP (from T1):') + ' ' + pub + '\n' +
      t('一致性:', 'Consistency:') + ' ' + consistent + '\n' +
      t('内网地址:', 'Private addresses:') + ' ' + (priv.length ? priv.join(', ') : '—');
    render('t6', 'ok', text, text);
  }

  // ================= T7 NAT 推断 =================
  var STUNS = ['stun:stun.l.google.com:19302', 'stun:stun1.l.google.com:19302', 'stun:stun.cloudflare.com:3478'];
  async function stunMapping(url) {
    var list = await collectCandidates({ iceServers: [{ urls: url }] }, 5);
    var s = list.filter(function (c) { return c.type === 'srflx'; })[0];
    return s ? { ip: s.ip, port: s.port } : null;
  }
  async function runT7() {
    render('t7', 'loading', t('正在向 3 个 STUN 查询映射…', 'Querying 3 STUN servers…'));
    var maps = [];
    for (var i = 0; i < STUNS.length; i++) {
      try { maps.push({ stun: STUNS[i], map: await stunMapping(STUNS[i]) }); }
      catch (e) { maps.push({ stun: STUNS[i], map: null }); }
    }
    var got = maps.filter(function (m) { return m.map && m.map.port; });
    var type = got.length < 2 ? t('无法判断', 'Undetermined') :
      (got.every(function (m) { return m.map.port === got[0].map.port; }) ? t('锥形 NAT', 'Cone NAT') : t('对称 NAT', 'Symmetric NAT'));
    var text = t('NAT 类型推断:', 'NAT type:') + ' ' + type + '\n' + t('各 STUN 映射:', 'STUN mappings:') + '\n' +
      maps.map(function (m) { return m.stun + ': ' + (m.map ? m.map.ip + ':' + m.map.port : '—'); }).join('\n');
    render('t7', 'ok', text, text);
  }

  // ================= T8 DNS 出口（需自有域名，降级） =================
  async function runT8() {
    var text = t('DNS 出口查询需要自有域名：\n1) 在权威 DNS 为 *.dns.<你的域名> 配置日志；\n2) 页面随机 token 加载 1x1 图片触发递归查询；\n3) 通过静态接口按 token 取回解析器 IP。\n本页未配置任何自有域名接口，故不提供结果（不伪造数据）。',
      'DNS egress lookup requires your own domain:\n1) Log queries for *.dns.<your-domain> at authoritative DNS;\n2) Load a 1x1 image with a random token to trigger resolution;\n3) Fetch the resolver IP by token from a static endpoint.\nNo domain endpoint is configured here, so no result is provided (no fabricated data).');
    var badge = document.querySelector('#card-t8 .nt-badge');
    if (badge) { badge.setAttribute('data-s', 'idle'); badge.textContent = t('需配置', 'Setup required'); }
    render('t8', 'idle', text, text);
  }

  // ================= T9 CDN 边缘 =================
  async function runT9() {
    var input = document.getElementById('t9-url');
    var url = input ? input.value.trim() : '';
    if (!url) { render('t9', 'error', t('请输入 URL', 'Enter a URL')); return; }
    render('t9', 'loading', t('正在探测 CDN…', 'Probing CDN…'));
    var rows = [];
    for (var i = 0; i < 3; i++) {
      var u = url + (url.indexOf('?') >= 0 ? '&' : '?') + '_=' + Date.now() + i;
      var t0 = (performance && performance.now) ? performance.now() : Date.now();
      try {
        var r = await fetchTimed(u, 8000, { cache: 'no-store' });
        var ms = Math.round(((performance && performance.now) ? performance.now() : Date.now()) - t0);
        var edge = r.headers.get('cf-ray') || r.headers.get('x-served-by') || r.headers.get('x-cache') || t('不可读', 'unreadable');
        rows.push({ url: url, edge: edge, rtt: ms });
      } catch (e) { rows.push({ url: url, edge: t('不可读', 'unreadable'), rtt: -1 }); }
    }
    var okRows = rows.filter(function (r) { return r.rtt >= 0; });
    var text = t('CDN 探测结果:', 'CDN probe:') + '\n' +
      rows.map(function (r) { return r.url + ': ' + t('边缘标识', 'Edge') + '=' + r.edge + ' RTT=' + (r.rtt >= 0 ? r.rtt : '—') + 'ms'; }).join('\n') + '\n' +
      t('推断命中:', 'Likely edge:') + ' ' + (okRows.length && okRows[0].edge !== t('不可读', 'unreadable') ? okRows[0].edge : t('无法确定', 'Undetermined'));
    render('t9', okRows.length ? 'ok' : 'error', text, text);
  }

  // ================= T10 代理分流 =================
  var CN_TARGETS = [
    { name: 'Baidu', url: 'https://www.baidu.com/favicon.ico', group: 'cn' },
    { name: 'Taobao', url: 'https://www.taobao.com/favicon.ico', group: 'cn' },
    { name: 'QQ', url: 'https://www.qq.com/favicon.ico', group: 'cn' }
  ];
  var GLOBAL_TARGETS = [
    { name: 'Google', url: 'https://www.google.com/favicon.ico', group: 'global' },
    { name: 'GitHub', url: 'https://github.com/favicon.ico', group: 'global' },
    { name: 'Cloudflare', url: 'https://www.cloudflare.com/favicon.ico', group: 'global' }
  ];
  async function runT10() {
    render('t10', 'loading', t('正在探测国内/国外目标…', 'Probing CN/global targets…'));
    var rows = await probeGroup(CN_TARGETS.concat(GLOBAL_TARGETS));
    var cn = rows.filter(function (r) { return r.group === 'cn'; });
    var gl = rows.filter(function (r) { return r.group === 'global'; });
    var cnOk = cn.filter(function (r) { return r.status === 'ok'; }).length;
    var glOk = gl.filter(function (r) { return r.status === 'ok'; }).length;
    var mode;
    if (!cnOk && !glOk) mode = t('网络或代理故障', 'Network/proxy failure');
    else if (cnOk === cn.length && glOk === gl.length) mode = t('可能为全局代理', 'Possible global proxy') + ' / ' + t('直连', 'Direct');
    else if (!cnOk && glOk) mode = t('异常，可能国内被误代理', 'Abnormal: domestic possibly proxied');
    else if (cnOk === cn.length && glOk < gl.length) mode = t('规则分流', 'Rule-based split') + ' / ' + t('直连', 'Direct');
    else mode = t('规则分流', 'Rule-based split');
    var text = t('代理模式推断:', 'Proxy mode:') + ' ' + mode + '\n' +
      t('国内目标:', 'Domestic:') + ' ' + cnOk + '/' + cn.length + '\n' +
      t('国外目标:', 'Global:') + ' ' + glOk + '/' + gl.length + '\n' +
      t('明细:', 'Details:') + '\n' +
      rows.map(function (r) { return r.name + ' (' + r.group + '): ' + (r.status === 'ok' ? t('可达', 'reachable') : t('不可达', 'unreachable')) + ' ' + r.ms + 'ms'; }).join('\n');
    render('t10', 'ok', text, text);
  }

  // ================= T11 测速 =================
  var SPEED_ENDPOINT = 'https://speed.cloudflare.com/__down?bytes=';
  async function downloadOnce(bytes, timeout) {
    var t0 = (performance && performance.now) ? performance.now() : Date.now();
    var r = await fetchTimed(SPEED_ENDPOINT + bytes, timeout || 30000, { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    var total = 0;
    if (r.body && r.body.getReader) {
      var reader = r.body.getReader();
      for (;;) { var chunk = await reader.read(); if (chunk.done) break; total += (chunk.value && chunk.value.length) || 0; }
    } else {
      var buf = await r.arrayBuffer(); total = buf.byteLength;
    }
    var ms = ((performance && performance.now) ? performance.now() : Date.now()) - t0;
    return { bytes: total, sec: ms / 1000, mbps: total * 8 / Math.max(ms, 1) / 1000 };
  }
  async function runT11() {
    render('t11', 'loading', t('预热与延迟测试…', 'Warm-up and latency test…'));
    var latencies = [];
    try {
      await downloadOnce(256 * 1024, 30000);
      for (var i = 0; i < 10; i++) {
        var d = await downloadOnce(0, 30000);
        latencies.push(Math.max(0, d.sec * 1000));
      }
    } catch (e) { render('t11', 'error', t('测速失败', 'Speed test failed') + '：' + errInfo(e)); return; }
    var latency = median(latencies);
    var jitter = median(latencies.map(function (x) { return Math.abs(x - latency); }));
    var rounds = [1, 5, 10], results = [];
    for (var k = 0; k < rounds.length; k++) {
      for (var j = 0; j < 2; j++) {
        try { results.push({ mb: rounds[k], mbps: (await downloadOnce(rounds[k] * 1024 * 1024, 30000)).mbps }); }
        catch (e) { /* 单轮失败跳过，取剩余轮次中位数 */ }
        var box = document.getElementById('result-t11');
        if (box) box.textContent = t('正在测速', 'Testing') + ' ' + rounds[k] + 'MB (' + (j + 1) + '/2)…';
      }
    }
    if (!results.length) { render('t11', 'error', t('测速失败：所有下载轮次均不可用', 'All download rounds failed')); return; }
    var mbps = median(results.map(function (r) { return r.mbps; }));
    var text = t('下行', 'Download') + ': ' + mbps.toFixed(2) + ' Mbps\n' +
      t('延迟', 'Latency') + ': ' + latency.toFixed(1) + ' ms\n' +
      t('抖动', 'Jitter') + ': ' + jitter.toFixed(1) + ' ms\n' +
      t('测试端点', 'Endpoint') + ': ' + SPEED_ENDPOINT + '{bytes}\n' +
      t('轮次', 'Rounds') + ': ' + results.length + ' ' + t('轮，取中位数', 'rounds, median used');
    render('t11', 'ok', text, text);
  }

  // ================= T12 浏览器指纹 =================
  async function fnv1a(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = (h * 0x01000193) >>> 0; }
    return ('00000000' + h.toString(16)).slice(-8);
  }
  async function runT12() {
    render('t12', 'loading', t('正在本地计算指纹…', 'Computing fingerprint locally…'));
    try {
      var nav = navigator, scr = screen;
      var canvasHash = '—', renderer = '—';
      try {
        var c = document.createElement('canvas'); c.width = 280; c.height = 60;
        var ctx = c.getContext('2d');
        if (ctx) {
          ctx.textBaseline = 'top'; ctx.font = '14px Arial';
          ctx.fillStyle = '#f60'; ctx.fillRect(0, 0, 120, 30);
          ctx.fillStyle = '#069'; ctx.fillText('ToolBox-FP-🌐', 2, 2);
          canvasHash = await fnv1a(c.toDataURL());
        }
      } catch (e) { canvasHash = '—'; }
      try {
        var cv = document.createElement('canvas');
        var gl = cv.getContext('webgl') || cv.getContext('experimental-webgl');
        if (gl) {
          var ext = gl.getExtension('WEBGL_debug_renderer_info');
          renderer = ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)) : '—';
        }
      } catch (e) { renderer = '—'; }
      var feat = {
        userAgent: nav.userAgent || '—', platform: nav.platform || '—',
        languages: (nav.languages || []).join(',') || nav.language || '—',
        timezone: (Intl.DateTimeFormat().resolvedOptions().timeZone) || '—',
        screen: scr.width + 'x' + scr.height + ' @' + (window.devicePixelRatio || 1) + 'x ' + (scr.colorDepth || '—') + 'bit',
        cpu: nav.hardwareConcurrency || '—', memory: nav.deviceMemory || '—',
        canvasHash: canvasHash, webgl: renderer
      };
      var raw = JSON.stringify(feat);
      var hash;
      if (window.crypto && crypto.subtle && window.TextEncoder) {
        var buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(raw));
        hash = Array.from(new Uint8Array(buf)).map(function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
      } else hash = await fnv1a(raw) + t('（FNV-1a 降级）', ' (FNV-1a fallback)');
      var text = t('指纹哈希', 'Fingerprint hash') + ': ' + hash + '\n' +
        'UA: ' + feat.userAgent + '\n' +
        t('平台', 'Platform') + ': ' + feat.platform + '\n' +
        t('语言', 'Languages') + ': ' + feat.languages + '\n' +
        t('时区', 'Timezone') + ': ' + feat.timezone + '\n' +
        t('屏幕', 'Screen') + ': ' + feat.screen + '\n' +
        'CPU: ' + feat.cpu + ' ' + t('核', 'cores') + '\n' +
        'Canvas ' + t('哈希', 'hash') + ': ' + feat.canvasHash + '\n' +
        'WebGL Renderer: ' + feat.webgl;
      render('t12', 'ok', text, text);
      ST.t12Raw = raw;
    } catch (e) { render('t12', 'error', t('指纹计算失败', 'Fingerprint failed') + '：' + errInfo(e)); }
  }

  // ================= T13 服务状态 =================
  var STATUS_APIS = [
    { name: 'GitHub', url: 'https://www.githubstatus.com/api/v2/status.json' },
    { name: 'Cloudflare', url: 'https://www.cloudflarestatus.com/api/v2/status.json' },
    { name: 'Vercel', url: 'https://www.vercel-status.com/api/v2/status.json' },
    { name: 'npm', url: 'https://status.npmjs.org/api/v2/status.json' }
  ];
  async function runT13() {
    render('t13', 'loading', t('正在读取 4 个服务状态…', 'Reading 4 status endpoints…'));
    var rows = await Promise.allSettled(STATUS_APIS.map(function (s) { return fetchJson(s.url, 5000); }));
    var lines = [];
    rows.forEach(function (r, i) {
      var name = STATUS_APIS[i].name, status = 'unknown', updated = '—';
      if (r.status === 'fulfilled' && r.value && r.value.status && r.value.status.indicator) {
        var ind = r.value.status.indicator;
        status = ind === 'none' ? 'operational' : (ind === 'minor' ? 'degraded' : (ind === 'major' || ind === 'critical') ? 'outage' : 'unknown');
        updated = (r.value.status.updated_at || r.value.page && r.value.page.updated_at || '—');
      }
      lines.push(name + ': ' + status + ' ' + t('更新于', 'updated at') + ' ' + updated);
    });
    var text = t('服务状态:', 'Service status:') + '\n' + lines.join('\n');
    render('t13', 'ok', text, text);
  }

  // ================= 调度与事件 =================
  var RUNNERS = { t1: runT1, t2: runT2, t3: runT3, t4: runT4, t5: runT5, t6: runT6, t7: runT7,
    t8: runT8, t9: runT9, t10: runT10, t11: runT11, t12: runT12, t13: runT13 };

  async function run(id) {
    if (RUNNING[id]) return;
    RUNNING[id] = true;
    try { await RUNNERS[id](); }
    catch (e) { render(id, 'error', t('执行失败', 'Failed') + '：' + errInfo(e)); }
    finally { RUNNING[id] = false; }
  }

  function init() {
    var grid = document.getElementById('ntGrid');
    if (grid) {
      grid.addEventListener('click', function (ev) {
        var runBtn = ev.target && ev.target.closest ? ev.target.closest('[data-run]') : null;
        if (runBtn) { run(runBtn.getAttribute('data-run')); return; }
        var copyBtn = ev.target && ev.target.closest ? ev.target.closest('[data-copy]') : null;
        if (copyBtn) {
          var id = copyBtn.getAttribute('data-copy');
          var s = ST[id];
          if (!s || !s.copy || s.state === 'idle') { toast(t('暂无结果可复制', 'No result to copy'), false); return; }
          copyText(s.copy).then(function () { toast(t('已复制', 'Copied'), true); });
          return;
        }
      });
    }
    // 对比按钮在历史表内（ntGrid 之外），单独委托
    var histBody = document.getElementById('ntHistoryBody');
    if (histBody) {
      histBody.addEventListener('click', function (ev) {
        var diffBtn = ev.target && ev.target.closest ? ev.target.closest('[data-diff]') : null;
        if (diffBtn) { showDiff(diffBtn.getAttribute('data-diff'), diffBtn); }
      });
    }
    var t2 = document.getElementById('t2-ip');
    if (t2) t2.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); run('t2'); } });
    var t5 = document.getElementById('t5-url');
    if (t5) t5.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); run('t5'); } });
    var all = document.getElementById('ntCopyAll');
    if (all) all.addEventListener('click', function () {
      var parts = Object.keys(RUNNERS).filter(function (id) { return ST[id] && ST[id].state === 'ok' && ST[id].copy; })
        .map(function (id) { return '[' + id.toUpperCase() + ']\n' + ST[id].copy; });
      if (!parts.length) { toast(t('暂无结果可复制', 'No result to copy'), false); return; }
      copyText(parts.join('\n\n')).then(function () { toast(t('已复制全部结果', 'All results copied'), true); });
    });
    // 首次渲染历史表（从本机恢复），随后 T1 自动执行会再次刷新
    renderHistory();
    // T1 页面加载后自动执行一次
    run('t1');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // 暴露给测试与控制台
  window.NT = { run: run, render: render, ST: ST, runners: RUNNERS, validIp: validIp, t1Text: t1Text };
})();
