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
  // 把任意值安全地转成展示文本：对象不直接 String（否则 [object Object]），
  // 优先取常见可读字段，否则退化为 JSON。数组逐项展开。
  function dash(v) {
    if (v === undefined || v === null || v === '') return '—';
    if (Array.isArray(v)) return v.map(dash).join(', ');
    if (typeof v === 'object') {
      for (var k in { id: 1, name: 1, description: 1, abbr: 1, utc: 1, value: 1, text: 1 }) {
        if (v[k] !== undefined && v[k] !== null && v[k] !== '') return String(v[k]);
      }
      try { return JSON.stringify(v); } catch (e) { return String(v); }
    }
    return String(v);
  }
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
    renderAnalysis(id, state, display);
    renderHistory();
  }

  // 每个独立页在 <script> 内提供 window.__ntAnalyze(id, text, isEn) 做本工具专属的
  // 结果解读（纯本地文本解析，不发请求、不伪造数据）。解读失败不影响主结果。
  function renderAnalysis(id, state, display) {
    var box = document.getElementById('analysis-' + id);
    if (!box) return;
    if (state !== 'ok' || typeof window.__ntAnalyze !== 'function') {
      if (box) { box.innerHTML = ''; box.setAttribute('data-s', state); }
      return;
    }
    try {
      var html = window.__ntAnalyze(id, String(display || ''), isEn());
      box.innerHTML = html || '';
      box.setAttribute('data-s', 'ok');
    } catch (e) {
      box.innerHTML = '';
      box.setAttribute('data-s', 'error');
    }
  }

  // ---- 本机历史（localStorage）：只存最近一次成功结果，绝不上传 ----
  var HIST_KEY = 'ntHist_v1';
  // 独立页在正文内联脚本里按工具提供 __ntStorage 适配层（key 隔离）；
  // 适配层缺失时退回统一 key，保证共享脚本在任意环境都能用。
  function loadHistory() {
    if (window.__ntStorage && typeof window.__ntStorage.read === 'function') {
      try { return window.__ntStorage.read() || {}; } catch (e) { return {}; }
    }
    try { return JSON.parse(localStorage.getItem(HIST_KEY) || '{}') || {}; }
    catch (e) { return {}; }
  }
  function saveHistory(id, copyText) {
    try {
      var h = loadHistory();
      h[id] = { copy: String(copyText || ''), time: Date.now() };
      if (window.__ntStorage && typeof window.__ntStorage.write === 'function') window.__ntStorage.write(h);
      else localStorage.setItem(HIST_KEY, JSON.stringify(h));
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
      // ipwho.is 的 timezone 是 {id, abbr, offset, name, utc...} 对象；取 id 展示，避免 [object Object]
      var tz = j.timezone;
      var tzText = (tz && typeof tz === 'object') ? (tz.id || tz.name || tz.utc || '') : tz;
      return { ip: j.ip, version: j.type ? String(j.type).replace(/[^46]/g, '') : (j.ip && j.ip.indexOf(':') >= 0 ? '6' : '4'),
        country: j.country, region: j.region, city: j.city,
        isp: j.connection && j.connection.isp, asn: j.connection && j.connection.asn, timezone: tzText, domain: null };
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
    var text = t('本页不向任何公开 IP 接口发起请求，因此无法自动显示你的出口 IP。\n自查步骤：\n1) 打开路由器/光猫管理页，查看 WAN 侧 IPv4/IPv6 地址；\n2) 或在你信任的网络服务商官网/客户端查看“当前连接 IP”；\n3) 把查到的 IP 粘贴到本机记事本核对，勿提交给陌生网站。\n说明：出口 IP 可能因代理、VPN、CGNAT 而变化；本页只做本地说明，不采集、不上传。',
      'This page sends no request to public IP services, so it cannot display your egress IP automatically.\nCheck locally:\n1) Open your router or ONT admin page and read the WAN IPv4/IPv6 address;\n2) Or read the current connection IP in a trusted ISP portal/client;\n3) Keep the result in a local note; do not submit it to unknown sites.\nNote: egress IP can change with proxy, VPN or CGNAT; this page only explains and never collects or uploads.');
    render('t1', 'ok', text, text);
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
    var text = t('IP 格式校验通过：' + ip + '（IPv' + validIp(ip) + '）。\n本页不把该地址发送给 ipwho.is、ipapi.co 或任何第三方接口，因此不显示国家/城市/ISP/ASN。\n归属地查询建议：使用本地离线 IP 库（如 MaxMind GeoLite2 离线库）、运营商 whois 或有权查询的内部系统；查询前确认数据合规与授权。',
      'IP format is valid: ' + ip + ' (IPv' + validIp(ip) + ').\nThis page does not send it to ipwho.is, ipapi.co or any third-party API, so country/city/ISP/ASN are not shown.\nUse an offline IP database (such as MaxMind GeoLite2), carrier whois, or an authorized internal system; confirm compliance and authorization before querying.');
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
    var text = t('观测范围：仅 4 个固定站点的 favicon 图片加载（点击后才请求），不代表整站、DNS、API、代理或网络是否正常。', 'Scope: only favicon image loads from 4 fixed sites, requested after you click; this does not prove the whole site, DNS, API, proxy or network is healthy.') + '\n' + lines.join('\n') + '\n' + t('图片加载成功', 'Images loaded') + ': ' + pass + '/' + rows.length;
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
    var text = t('本页不访问 STUN 服务器，也不向第三方发送 WebRTC/网络候选信息，因此无法自动判定 NAT 类型。\n本地排查步骤：\n1) 在路由器管理页查看 NAT/端口映射与 UPnP 状态；\n2) 用两台不同网络的设备尝试 P2P 直连，记录是否必须中继；\n3) 需要精确判定时，在受控环境使用自建 STUN/TURN 并评估隐私与合规。\n结论：仅凭浏览器页面不能可靠区分全锥/受限/端口受限/对称 NAT，本页不给出猜测结果。',
      'This page does not contact STUN servers or send WebRTC/network candidates to third parties, so it cannot determine NAT type automatically.\nLocal checks:\n1) Inspect NAT/port mapping and UPnP in the router admin page;\n2) Try P2P between two networks and note whether relay is required;\n3) For exact classification, use a self-hosted STUN/TURN in a controlled environment after privacy and compliance review.\nA browser page alone cannot reliably distinguish cone/restricted/port-restricted/symmetric NAT, so no guessed result is shown.');
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
    render('t10', 'loading', t('正在观测固定站点加载…', 'Observing fixed-site loads…'));
    var rows = await probeGroup(CN_TARGETS.concat(GLOBAL_TARGETS));
    var cn = rows.filter(function (r) { return r.group === 'cn'; });
    var gl = rows.filter(function (r) { return r.group === 'global'; });
    var cnOk = cn.filter(function (r) { return r.status === 'ok'; }).length;
    var glOk = gl.filter(function (r) { return r.status === 'ok'; }).length;
    var text = t('观测范围：仅固定站点的 favicon 图片加载成功/失败与耗时；不读取系统代理配置，也不推断代理模式或分流规则。', 'Scope: only fixed-site favicon load success/failure and timing; this does not read system proxy settings or infer proxy mode or routing rules.') + '\n' +
      t('国内目标加载:', 'Domestic loads:') + ' ' + cnOk + '/' + cn.length + '\n' +
      t('国外目标加载:', 'Global loads:') + ' ' + glOk + '/' + gl.length + '\n' +
      t('逐项观测:', 'Per-target observations:') + '\n' +
      rows.map(function (r) { return r.name + ' (' + r.group + '): ' + (r.status === 'ok' ? t('加载成功', 'loaded') : t('加载失败/超时', 'failed/timeout')) + ' ' + r.ms + 'ms'; }).join('\n') + '\n' +
      t('结论：图片加载受 CDN、缓存、拦截与跨域策略影响，无法据此判定代理模式；如需判断分流，请核对系统/路由代理配置与浏览器网络面板。', 'Conclusion: image loads are affected by CDN, cache, blocking and cross-origin policy, so proxy mode cannot be inferred; check system/router proxy settings and browser network panel instead.');
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
    var text = t('本页不向 speed.cloudflare.com 或其他 CDN 拉取测试文件，因此不显示下载速率。\n原因：自动测速会产生大流量、结果受 CDN/并发/缓存影响，且会把请求发往第三方。\n本地核对步骤：\n1) 用运营商官方测速页或你信任的测速工具，在同一时段多次测试；\n2) 有线与 Wi‑Fi 分开记录，避免把无线瓶颈当成宽带不足；\n3) 对照套餐带宽与路由器协商速率，关注延迟、抖动和丢包而不只看峰值。\n本页只提供方法，不发起测速请求。',
      'This page does not download test files from speed.cloudflare.com or any CDN, so no download rate is shown.\nAutomatic tests consume large traffic and are affected by CDN, concurrency and caching, while sending requests to third parties.\nLocal checks:\n1) Use your ISP official speed page or a trusted tool, repeated in the same time window;\n2) Record wired and Wi-Fi separately to avoid mistaking wireless limits for broadband limits;\n3) Compare plan bandwidth and router negotiated rate; watch latency, jitter and loss, not only peak speed.\nThis page provides method only and sends no speed-test request.');
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
    var text = t('本页不请求 GitHub、Cloudflare、Vercel、npm 的状态接口，因此不显示实时状态。\n请手动打开官方状态页核对（以官方页面为准）：\nGitHub: https://www.githubstatus.com/\nCloudflare: https://www.cloudflarestatus.com/\nVercel: https://www.vercel-status.com/\nnpm: https://status.npmjs.org/\n提示：浏览器跨域限制与接口限流会使自动汇总不稳定；本页只提供入口，不采集、不上传。',
      'This page does not call the GitHub, Cloudflare, Vercel or npm status APIs, so no live status is shown.\nOpen the official status pages manually (official pages are authoritative):\nGitHub: https://www.githubstatus.com/\nCloudflare: https://www.cloudflarestatus.com/\nVercel: https://www.vercel-status.com/\nnpm: https://status.npmjs.org/\nCross-origin limits and rate limits make automated aggregation unstable; this page provides entry points only and never collects or uploads data.');
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

  // 独立工具页：body 上 data-tool="tX" 指定本页工具；聚合页无此属性则沿用原逻辑
  var CURRENT = (document.body && document.body.getAttribute('data-tool')) || '';

  function init() {
    // 事件委托绑 document：聚合页与独立页（无 #ntGrid）共用同一份 JS
    document.addEventListener('click', function (ev) {
      var fillBtn = ev.target && ev.target.closest ? ev.target.closest('[data-fill]') : null;
      if (fillBtn) {
        var target = document.getElementById(fillBtn.getAttribute('data-fill'));
        if (target) { target.value = fillBtn.getAttribute('data-value') || ''; target.focus(); }
        return;
      }
      var runBtn = ev.target && ev.target.closest ? ev.target.closest('[data-run]') : null;
      if (runBtn) {
        var rid = runBtn.getAttribute('data-run');
        if (CURRENT && rid !== CURRENT) return;  // 独立页忽略非本工具按钮
        run(rid); return;
      }
      // 无输入项工具的「立即刷新」预设：真实执行一次本页工具
      var quickBtn = ev.target && ev.target.closest ? ev.target.closest('[data-action="run"]') : null;
      if (quickBtn && CURRENT) { run(CURRENT); return; }
      var copyBtn = ev.target && ev.target.closest ? ev.target.closest('[data-copy]') : null;
      if (copyBtn) {
        var id = copyBtn.getAttribute('data-copy');
        if (CURRENT && id !== CURRENT) return;
        var s = ST[id];
        if (!s || !s.copy || s.state === 'idle') { toast(t('暂无结果可复制', 'No result to copy'), false); return; }
        copyText(s.copy).then(function () { toast(t('已复制', 'Copied'), true); });
        return;
      }
    });
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
    // 首次渲染历史表（从本机恢复），随后自动执行会再次刷新
    renderHistory();
    // 独立页：运行本页工具（按需自动执行）；聚合页：T1 自动执行一次
    var autoId = CURRENT || 't1';
    // 需要用户输入的工具有输入控件时不自动跑（避免空输入直接报错），其余自动执行
    var needsInput = (autoId === 't2' || autoId === 't5');
    var hasInput = !!document.getElementById(autoId === 't2' ? 't2-ip' : (autoId === 't5' ? 't5-url' : ''));
    if (!needsInput || !hasInput) run(autoId);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // 暴露给测试与控制台
  window.NT = { run: run, render: render, ST: ST, runners: RUNNERS, validIp: validIp, t1Text: t1Text };
})();
