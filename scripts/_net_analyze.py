#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""13 个 telecom 独立工具页的「结果速读」解读器（每页独有、纯本地文本解析）。

每个值是注入到页面内联 <script> 的 JS 片段，定义 window.__ntAnalyze(id, text, isEn)。
约定：
- 只读 text（共享 JS render() 传入的 display 文本），不发任何网络请求；
- 解析失败/字段缺失时返回空串或「无法解读」，绝不编造结果；
- 返回 HTML 字符串，结构用 .nt-an-item / .nt-an-tag；
- 文案在 JS 内按 isEn 取中英，不依赖 i18n map（动态结果）。
- 模板里的字面量需由生成器做 str.format，故 JS 里的花括号须写成 {{ }}。
"""

ANALYZE = {
  # T1 公网 IP：判断 IP 版本、是否保留/私有地址、来源可靠性、时区是否可得
  't1': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || text.indexOf('failed') >= 0) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var m = text.match(/(?:IP|地址)[:：]\s*([0-9A-Fa-f:.]+)/);
  var ip = m ? m[1] : '';
  if (ip) {
    var ver = ip.indexOf(':') >= 0 ? 'IPv6' : 'IPv4';
    item(en ? 'Address type' : '地址版本', ver, 'good',
      en ? 'Detected from the reported address.' : '根据返回地址判断。');
    if (/^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[01])\.|^127\.|^169\.254\./.test(ip)) {
      item(en ? 'Address class' : '地址性质', en ? 'Private / reserved' : '私有/保留地址', 'warn',
        en ? 'This is not a public routable address; an upstream proxy or VPN may be in use.'
            : '这不是公网可路由地址，可能存在代理或 VPN 出口。');
    } else {
      item(en ? 'Address class' : '地址性质', en ? 'Public' : '公网地址', 'good',
        en ? 'Globally routable address.' : '全球可路由地址。');
    }
  }
  var src = (text.match(/(?:来源|Source)[:：]\s*([^\n]+)/) || [])[1];
  if (src) {
    item(en ? 'Data source' : '命中数据源', '', '',
      (en ? 'Source used: ' : '本次采用：') + src.replace(/<\/?[^>]+>/g, ''));
  }
  var tz = (text.match(/(?:时区|Timezone)[:：]\s*([^\n]+)/) || [])[1];
  item(en ? 'Timezone' : '时区字段', tz && tz.indexOf('—') < 0 ? (en ? 'Available' : '可用') : (en ? 'Missing' : '缺失'),
    tz && tz.indexOf('—') < 0 ? 'good' : 'warn',
    en ? 'Geolocation timezone from the source.' : '来源提供的归属地时区。');
  var v6 = /IPv6[:：]\s*([0-9A-Fa-f:]+)/.test(text);
  item(en ? 'IPv6' : 'IPv6 探测', v6 ? (en ? 'Detected' : '已获取') : (en ? 'None' : '无'), v6 ? 'good' : 'warn',
    en ? 'Separate IPv6 probe result.' : '单独 IPv6 探测的结果。');
  return out.join('');
};
""",
  # T2 IP 归属地：判断查询 IP 是否公网、归属是否完整、ASN 是否可得
  't2': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('格式不合法') >= 0 || /Invalid IP/.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var q = (text.match(/(?:查询 IP|Queried IP)[:：]\s*([^\n]+)/) || [])[1];
  if (q) {
    q = q.trim();
    var private = /^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[01])\.|^127\./.test(q);
    item(en ? 'Queried address' : '查询地址', private ? (en ? 'Private' : '内网') : (en ? 'Public' : '公网'),
      private ? 'warn' : 'good',
      private ? (en ? 'Private addresses have no public geolocation.' : '内网地址没有公网归属信息。')
              : (en ? 'Public address, geolocation may be available.' : '公网地址，可查询归属。'));
  }
  var region = (text.match(/(?:归属|Region)[:：]\s*([^\n]+)/) || [])[1];
  var known = region && !/^[\s—\/]*$/.test(region.replace(/\//g, ''));
  item(en ? 'Geolocation' : '归属地', known ? (en ? 'Found' : '有数据') : (en ? 'Empty' : '空'),
    known ? 'good' : 'warn',
    en ? 'Region fields returned by the source.' : '来源返回的地区字段。');
  var asn = (text.match(/ASN[:：]\s*([^\n]+)/) || [])[1];
  item(en ? 'ASN' : '自治系统号', asn && asn.indexOf('—') < 0 ? (en ? 'Available' : '可用') : (en ? 'Missing' : '缺失'),
    asn && asn.indexOf('—') < 0 ? 'good' : 'warn',
    en ? 'ASN helps identify the network operator.' : 'ASN 有助于识别网络运营方。');
  return out.join('');
};
""",
  # T3 本机内网 IP：统计地址个数、识别 mDNS 混淆、判断多网卡
  't3': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /fail|unavailable/i.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var lines = text.split('\n').filter(function (l) { return /\d|local/.test(l); });
  var ips = lines.filter(function (l) { return /\d+\.\d+\.\d+\.\d+/.test(l); });
  item(en ? 'Address count' : '地址数量', String(lines.length), 'good',
    (en ? 'Host candidates collected: ' : '收集到的 host 候选：') + lines.length);
  var mdns = /\.local\b/.test(text);
  item(en ? 'mDNS obfuscation' : 'mDNS 混淆', mdns ? (en ? 'On' : '已启用') : (en ? 'Off' : '未发现'),
    mdns ? 'warn' : 'good',
    mdns ? (en ? 'Some real LAN IPs are hidden behind .local names.' : '部分真实内网 IP 被 .local 名称隐藏。')
         : (en ? 'No .local obfuscation detected.' : '未检测到 .local 混淆。'));
  var multi = ips.length > 1;
  item(en ? 'Multiple NICs' : '多网卡', multi ? (en ? 'Yes' : '是') : (en ? 'No' : '否'), 'good',
    (en ? 'Distinct IPv4 host addresses: ' : '不同 IPv4 地址数：') + ips.length);
  return out.join('');
};
""",
  # T4 网站可达性：解析汇总、判断整体网络健康
  't4': r"""
window.__ntAnalyze = function (id, text, en) {
  var m = text.match(/(?:汇总|Summary)[:：]\s*(\d+)\s*\/\s*(\d+)/);
  if (!m) return '';
  var pass = parseInt(m[1], 10), total = parseInt(m[2], 10);
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var ratio = total ? pass / total : 0;
  var lv = ratio === 1 ? 'good' : (ratio === 0 ? 'bad' : 'warn');
  var tag = ratio === 1 ? (en ? 'All reachable' : '全部可达')
    : (ratio === 0 ? (en ? 'All blocked' : '全部不可达') : (en ? 'Partial' : '部分可达'));
  item(en ? 'Reachability' : '可达比例', tag, lv, pass + '/' + total);
  if (ratio === 0) {
    item(en ? 'Likely cause' : '可能原因', en ? 'Check network' : '检查网络', 'bad',
      en ? 'No favicon loaded; check DNS, firewall or offline state.' : '所有 favicon 均未载入，检查 DNS、防火墙或离线状态。');
  } else if (ratio < 1) {
    item(en ? 'Note' : '说明', en ? 'Reference only' : '仅供参考', 'warn',
      en ? 'Favicon probing cannot read HTTP status codes.' : 'favicon 探测无法读取 HTTP 状态码。');
  }
  return out.join('');
};
""",
  # T5 URL 可达性：解析结果行、探测方式、耗时
  't5': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /failed/i.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var ok = /可达|Reachable/.test(text) && !/不可达|Unreachable/.test(text);
  item(en ? 'Result' : '探测结果', ok ? (en ? 'Reachable' : '可达') : (en ? 'Not reachable' : '不可达'),
    ok ? 'good' : 'bad', en ? 'Network-layer probe result.' : '网络层探测结果。');
  var way = (text.match(/(?:方式|Method)[:：]\s*([^\n]+)/) || [])[1];
  if (way) item(en ? 'Method' : '探测方式', '', '', way.replace(/<\/?[^>]+>/g, ''));
  var ms = (text.match(/(?:耗时|Latency|Time)[:：]\s*(\d+)\s*ms/) || [])[1];
  if (ms) {
    var n = parseInt(ms, 10);
    item(en ? 'Latency' : '耗时', n < 200 ? (en ? 'Fast' : '较快') : (n < 1000 ? (en ? 'Normal' : '正常') : (en ? 'Slow' : '较慢')),
      n < 200 ? 'good' : (n < 1000 ? 'warn' : 'bad'), ms + ' ms');
  }
  item(en ? 'Caveat' : '注意', en ? 'No status code' : '无状态码', 'warn',
    en ? 'no-cors hides HTTP status; this only shows network acceptance.' : 'no-cors 隐藏 HTTP 状态码，仅反映网络层是否被接受。');
  return out.join('');
};
""",
  # T6 WebRTC 泄露：判断公网 IP 一致性、内网暴露条数
  't6': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /No ICE candidates/.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var cons = (text.match(/(?:一致性|Consistency)[:：]\s*([^\n]+)/) || [])[1] || '';
  var match = /一致|Match/.test(cons);
  item(en ? 'Public IP consistency' : '公网 IP 一致性',
    match ? (en ? 'Match' : '一致') : (en ? 'Check' : '需关注'), match ? 'good' : 'warn',
    en ? 'Whether STUN srflx matches the public IP from T1.' : 'STUN 映射地址是否与公网 IP 查询一致。');
  var privLine = (text.match(/(?:内网地址|Private addresses)[:：]\s*([^\n]+)/) || [])[1] || '';
  var privCount = privLine && privLine.indexOf('—') < 0 ? privLine.split(',').length : 0;
  item(en ? 'Private addresses' : '内网地址暴露', String(privCount), privCount ? 'warn' : 'good',
    en ? 'Local IPs visible to WebRTC.' : 'WebRTC 可见的本地地址数量。');
  item(en ? 'Leak risk' : '泄露风险', privCount ? (en ? 'Possible' : '可能存在') : (en ? 'Low' : '较低'),
    privCount ? 'warn' : 'good',
    en ? 'Private IPs exposed via ICE can aid fingerprinting.' : 'ICE 暴露内网地址可用于指纹识别。');
  return out.join('');
};
""",
  # T7 NAT 类型：解析推断类型、映射数量、给出 P2P 含义
  't7': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /failed/i.test(text)) return '';
  var m = text.match(/(?:NAT 类型推断|NAT type)[:：]\s*([^\n]+)/);
  if (!m) return '';
  var type = m[1].trim();
  var cone = /锥形|Cone/.test(type) && !/对称|Symmetric/.test(type);
  var sym = /对称|Symmetric/.test(type);
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var lv = sym ? 'warn' : (cone ? 'good' : 'warn');
  item(en ? 'Inferred type' : '推断类型', type, lv,
    en ? 'Heuristic from STUN mapping ports.' : '根据 STUN 映射端口的启发式推断。');
  var maps = (text.match(/stun:/g) || []).length;
  var got = (text.match(/:(\d+)\s*(?:\n|$)/g) || []).length;
  item(en ? 'STUN responses' : '有效映射', got + ' / ' + maps, got >= 2 ? 'good' : 'warn',
    en ? 'At least two mappings are needed to compare ports.' : '至少需要两个映射才能比较端口。');
  if (cone) item(en ? 'P2P implication' : 'P2P 影响', en ? 'Easier' : '较易穿透', 'good',
    en ? 'Stable external port favors direct peer-to-peer connections.' : '固定对外端口有利于 P2P 直连。');
  else if (sym) item(en ? 'P2P implication' : 'P2P 影响', en ? 'Harder' : '较难穿透', 'warn',
    en ? 'Per-target ports make direct P2P harder; relaying may be needed.' : '每目标不同端口使 P2P 更难，可能需要中继。');
  return out.join('');
};
""",
  # T8 DNS 出口：本页只给配置说明，解读明确"需配置"、不伪造结果
  't8': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  item(en ? 'Status' : '当前状态', en ? 'Setup required' : '需配置', 'warn',
    en ? 'No endpoint is configured; no DNS egress result is fabricated.' : '本页未配置接口，不会伪造 DNS 出口结果。');
  var steps = (text.match(/^\s*\d+[.、]/gm) || []).length;
  if (steps) item(en ? 'Setup steps' : '配置步骤', String(steps), 'good',
    (en ? 'Steps listed to build your own resolver-log endpoint: ' : '搭建自有解析日志接口的步骤：') + steps);
  item(en ? 'Why' : '原因', en ? 'Honest degradation' : '诚实降级', 'good',
    en ? 'Real DNS egress IP must come from your own authoritative DNS logs.' : '真实 DNS 出口 IP 必须从你自己的权威 DNS 日志读取。');
  return out.join('');
};
""",
  # T9 CDN 节点：解析边缘标识、RTT、缓存命中
  't9': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /failed/i.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var edge = (text.match(/(?:边缘标识|Edge)[:：]\s*([^\n]+)/) || [])[1];
  var hasEdge = edge && edge.indexOf('—') < 0 && !/RTT|回退|fallback/i.test(edge);
  item(en ? 'Edge header' : '边缘标识', hasEdge ? (en ? 'Available' : '可读') : (en ? 'Fallback' : '已降级'),
    hasEdge ? 'good' : 'warn',
    hasEdge ? (en ? 'Edge ID read from response headers.' : '从响应头读到边缘节点标识。')
            : (en ? 'Headers hidden by CORS; using RTT fingerprint.' : '响应头被 CORS 隐藏，改用 RTT 指纹。'));
  var rtts = (text.match(/(\d+)\s*ms/g) || []).map(function (s) { return parseInt(s, 10); }).filter(function (n) { return isFinite(n); });
  if (rtts.length) {
    var min = Math.min.apply(null, rtts), max = Math.max.apply(null, rtts);
    item(en ? 'RTT range' : '往返时延', min + '–' + max + ' ms', min < 100 ? 'good' : (min < 300 ? 'warn' : 'bad'),
      en ? 'Minimum/maximum across probes.' : '各次探测的最小/最大值。');
  }
  var hit = /HIT|命中/.test(text);
  if (hit) item(en ? 'Cache' : '缓存命中', en ? 'HIT' : '命中', 'good',
    en ? 'CDN reports a cache hit for this file.' : 'CDN 报告该文件缓存命中。');
  return out.join('');
};
""",
  # T10 代理分流：解析推断模式、两组通过数、给出结论
  't10': r"""
window.__ntAnalyze = function (id, text, en) {
  var mode = (text.match(/(?:代理模式推断|Proxy mode)[:：]\s*([^\n]+)/) || [])[1];
  if (!mode) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var fail = /故障|failure/.test(mode);
  var split = /分流|split/.test(mode);
  item(en ? 'Inferred mode' : '推断模式', mode, fail ? 'bad' : (split ? 'warn' : 'good'),
    en ? 'Inferred from domestic/global reachability differences.' : '根据国内/国外可达性差异推断。');
  var cn = (text.match(/(?:国内目标|Domestic)[:：]\s*(\d+)\s*\/\s*(\d+)/) || []);
  var gl = (text.match(/(?:国外目标|Global)[:：]\s*(\d+)\s*\/\s*(\d+)/) || []);
  if (cn.length === 3) item(en ? 'Domestic targets' : '国内目标', cn[1] + '/' + cn[2],
    cn[1] === cn[2] ? 'good' : 'warn', en ? 'Reachable / total.' : '可达数 / 总数。');
  if (gl.length === 3) item(en ? 'Global targets' : '国外目标', gl[1] + '/' + gl[2],
    gl[1] === gl[2] ? 'good' : 'warn', en ? 'Reachable / total.' : '可达数 / 总数。');
  item(en ? 'Caveat' : '注意', en ? 'Heuristic' : '启发式', 'warn',
    en ? 'Cannot read system proxy settings; favicon results may mislead.' : '无法读取系统代理设置，favicon 结果可能误判。');
  return out.join('');
};
""",
  # T11 测速：解析下行/延迟/抖动，给出带宽等级
  't11': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /failed/i.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var dl = parseFloat((text.match(/(?:下行|Download)[:：]\s*([\d.]+)/) || [])[1]);
  if (isFinite(dl)) {
    var lv = dl >= 50 ? 'good' : (dl >= 10 ? 'warn' : 'bad');
    var tag = dl >= 50 ? (en ? 'Fast' : '较快') : (dl >= 10 ? (en ? 'Moderate' : '一般') : (en ? 'Slow' : '较慢'));
    item(en ? 'Download' : '下行速率', tag, lv, dl.toFixed(2) + ' Mbps');
  }
  var lat = parseFloat((text.match(/(?:延迟|Latency)[:：]\s*([\d.]+)/) || [])[1]);
  if (isFinite(lat)) {
    var llv = lat < 50 ? 'good' : (lat < 150 ? 'warn' : 'bad');
    item(en ? 'Latency' : '延迟', lat < 50 ? (en ? 'Low' : '低') : (lat < 150 ? (en ? 'Normal' : '正常') : (en ? 'High' : '高')),
      llv, lat.toFixed(1) + ' ms');
  }
  var jit = parseFloat((text.match(/(?:抖动|Jitter)[:：]\s*([\d.]+)/) || [])[1]);
  if (isFinite(jit)) item(en ? 'Jitter' : '抖动', jit < 20 ? (en ? 'Stable' : '稳定') : (en ? 'Variable' : '波动'),
    jit < 20 ? 'good' : 'warn', jit.toFixed(1) + ' ms');
  item(en ? 'Note' : '注意', en ? 'Estimate' : '粗略估算', 'warn',
    en ? 'Public endpoint, affected by node and congestion.' : '公共端点，受节点与拥塞影响，仅供参考。');
  return out.join('');
};
""",
  # T12 指纹：解析哈希长度、算法、特征维度，给出唯一性提示
  't12': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text || text.indexOf('失败') >= 0 || /failed/i.test(text)) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var hash = (text.match(/(?:指纹哈希|Fingerprint hash)[:：]\s*([0-9a-fA-F]+)/) || [])[1];
  if (hash) {
    var strong = hash.length === 64;
    item(en ? 'Hash algorithm' : '哈希算法', strong ? 'SHA-256' : 'FNV-1a', strong ? 'good' : 'warn',
      (en ? 'Hash length: ' : '哈希长度：') + hash.length);
  }
  var fields = (text.match(/\n[^\n]+[:：]/g) || []).length;
  item(en ? 'Trait dimensions' : '特征维度', String(fields), fields >= 6 ? 'good' : 'warn',
    en ? 'Number of local traits collected.' : '本地采集的特征项数量。');
  item(en ? 'Privacy' : '隐私提示', en ? 'Local only' : '仅本地', 'good',
    en ? 'Computed in your browser and never uploaded by this page.' : '在浏览器本地计算，本页不上传。');
  item(en ? 'Uniqueness' : '唯一性', en ? 'Not anonymous' : '非匿名', 'warn',
    en ? 'Such traits can be used to identify devices; do not treat as an anonymous ID.' : '此类特征可用于识别设备，勿当作匿名标识。');
  return out.join('');
};
""",
  # T13 服务状态：统计正常/降级/故障/未知，给出整体健康度
  't13': r"""
window.__ntAnalyze = function (id, text, en) {
  if (!text) return '';
  var out = [];
  function item(k, tag, lv, v) {
    out.push('<div class="nt-an-item"><span class="nt-an-k">' + k + '</span>' +
      (tag ? '<span class="nt-an-tag" data-lv="' + lv + '">' + tag + '</span>' : '') + v + '</div>');
  }
  var ok = (text.match(/operational/g) || []).length;
  var degraded = (text.match(/degraded/g) || []).length;
  var outage = (text.match(/outage|major|critical/g) || []).length;
  var unknown = (text.match(/unknown/g) || []).length;
  var total = ok + degraded + outage + unknown;
  if (!total) return '';
  item(en ? 'Services checked' : '检查服务数', String(total), 'good',
    en ? 'Status endpoints read this run.' : '本次读取的状态接口数。');
  item(en ? 'Operational' : '正常', String(ok), ok === total ? 'good' : 'warn',
    en ? 'Services reporting normal operation.' : '报告正常的服务数。');
  if (degraded) item(en ? 'Degraded' : '降级', String(degraded), 'warn',
    en ? 'Services reporting degraded performance.' : '报告性能降级的服务数。');
  if (outage) item(en ? 'Outage' : '故障', String(outage), 'bad',
    en ? 'Services reporting an active outage.' : '报告故障的服务数。');
  if (unknown) item(en ? 'Unknown' : '未知', String(unknown), 'warn',
    en ? 'Endpoints that could not be read; not assumed healthy.' : '未能读取的接口，不臆测为正常。');
  var health = outage ? 'bad' : (degraded || unknown ? 'warn' : 'good');
  item(en ? 'Overall' : '整体状态', health === 'good' ? (en ? 'Healthy' : '正常')
    : (health === 'warn' ? (en ? 'Degraded' : '需关注') : (en ? 'Incident' : '有故障')), health,
    en ? 'Based only on reported statuses.' : '仅依据各服务上报状态。');
  return out.join('');
};
""",
}
