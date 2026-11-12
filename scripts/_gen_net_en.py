#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 13 个 telecom 网络工具生成英文映射与注册（字节级插入，不改既有格式）。
复用 _gen_net_tools 的 TOOLS / RUN_LABEL / IDLE / INPUTS 中文文案 + 本文件英文字典。
产出：
- i18n/tools/en/telecom/<slug>.json  （per-tool map，新文件）
- 更新 i18n/tools/en/telecom/_index.json（数组追加）
- 更新 i18n/tools/telecom-body.json（对象追加）
- 更新 i18n/tools/_en_override.json（无缩进格式，对象追加）
- 更新 i18n/tools/slug-en.json（2 空格格式，对象追加）
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_net_tools import TOOLS, RUN_LABEL, IDLE, ROOT

COMMON = {
  '📡 通信技术': '📡 Telecommunications',
  '📐 工作原理与说明': '📐 How it works',
  '空态': 'Idle',
  '复制结果': 'Copy result',
  '📋 输出字段说明': '📋 Output fields',
  '❓ 常见问题': '❓ FAQ',
  '尚未执行，点击上方按钮开始。': 'Not run yet. Click the button above to start.',
  '🕘 本机运行记录与对比': '🕘 Local run history & comparison',
  '最近一次成功结果只保存在你本机浏览器（localStorage），不上传。可展开对比本次与上次输出的变化；换浏览器或清除站点数据后记录会消失。': 'Your last successful result is stored only in this browser (localStorage) and is never uploaded. Expand a row to compare the current output with the previous one. Clearing site data removes the record.',
  '状态': 'Status',
  '最近成功时间': 'Last success',
  '上次结果摘要': 'Previous result',
  '操作': 'Action',
  '常用预设：': 'Presets:',
  '常用预设 / 快捷操作：': 'Presets / shortcuts:',
  '立即刷新': 'Refresh now',
  '🔗 延伸工具': '🔗 Related tools',
  '以下工具与本页面常一起使用：': 'Tools commonly used with this page:',
  '子网划分工具': 'Subnet Planner',
  '带宽下载时间速算': 'Bandwidth & Download Time Calculator',
}

EN = {
 't1': dict(
  principle='Requests public IP geo services in order ipwho.is \u2192 ipapi.co \u2192 api.ip.sb \u2192 ipify; the first success is used, then IPv6 is probed separately. All requests use browser fetch with a 6s timeout and auto-failover.',
  fields=[('IP','Your current public IP address'),('版本','IPv4 or IPv6'),('位置','Country / region / city'),('ISP','Internet service provider'),('ASN','Autonomous system number'),('时区','IP timezone (taken from the source id field)'),('来源','Data source actually used'),('时间','Query time (ISO 8601)'),('IPv6','Separately detected IPv6 address (if any)')],
  faq=[('为什么结果和本地 IP 不同？','This shows your public exit IP (router WAN address), different from private LAN addresses like 192.168.x.x / 10.x.x.x.'),('多源回退是什么意思？','If the first API fails or times out, a backup is tried automatically; the "Source" field shows which one was used.'),('IP 查询准确吗？','Geolocation is inferred from third-party databases, city-level at best, and may be off \u2014 for reference only.')],
  run='Refresh', idle='Not queried yet. Click "Refresh" (auto-runs once on load).'),
 't2': dict(
  principle='Validates the IP format locally (IPv4 four octets / IPv6 colon groups) before sending any request; primary source ipwho.is falls back to ipapi.co. Enter triggers the query.',
  fields=[('查询 IP','The IP address you entered'),('归属','Country / region / city'),('ISP','The IP operator'),('ASN','Autonomous system number'),('域名','Associated domain (if provided by source)')],
  faq=[('支持哪些格式？','Standard IPv4 (e.g. 8.8.8.8) and IPv6 (e.g. 2001:4860:4860::8888). No request is sent for invalid formats.'),('能查内网 IP 吗？','Private reserved addresses (e.g. 192.168.1.1) have no public geolocation; results may be empty.'),('数据来源是谁？','Public APIs ipwho.is and ipapi.co; their databases maintain the geolocation.')],
  run='Look up', idle='Not queried yet. Enter an IP and click "Look up".'),
 't3': dict(
  principle='Creates an RTCPeerConnection without a STUN server and reads local NIC addresses from local SDP host candidates, closing after 3 seconds. No external server is contacted.',
  fields=[('内网 IP','LAN addresses from host candidates with protocol'),('mDNS 混淆地址','Real addresses hidden by browsers using .local suffixes')],
  faq=[('为什么需要点击按钮？','Browsers require WebRTC to be triggered by a user gesture, so click once after the page loads.'),('为什么显示 .local 结尾？','Some browsers enable mDNS obfuscation, replacing real private IPs with random .local names for privacy.'),('多网卡会显示多个吗？','Yes, all host candidates are listed, including Bluetooth and virtual adapters.')],
  run='Collect addresses', idle='Not collected yet. Click "Collect addresses".'),
 't4': dict(
  principle='Loads each site favicon in parallel and judges reachability via onload / onerror / timeout with approximate latency, max 5 concurrent. Image probing bypasses CORS but only checks network-layer reachability.',
  fields=[('站点','Target site being probed'),('状态','Reachable / timeout / unreachable'),('耗时','Approximate image load time in ms')],
  faq=[('这能代表网站正常吗？','Only that your network can fetch its favicon \u2014 not that all functions work, and no HTTP status code is read.'),('为什么有的站点总是不可达？','CDN blocking, favicon changes, or local network policy may affect it; results are indicative only.'),('会上传我的信息吗？','No. Your browser requests the target favicon directly, with no intermediary.')],
  run='Start probe', idle='Not probed yet. Click "Start probe".'),
 't5': dict(
  principle='First requests the URL with fetch no-cors to check network-layer acceptance; on failure falls back to requesting the site favicon. no-cors returns an opaque response, so status codes cannot be read.',
  fields=[('URL','Final requested full URL'),('方式','fetch no-cors or image'),('结果','Reachable / timeout / unreachable'),('耗时','Probe time in ms')],
  faq=[('为什么不显示 HTTP 状态码？','no-cors hides the response body, so only network acceptance can be judged, not 200/404 codes.'),('可以探测内网地址吗？','Yes, but mixed-content and CORS policies may make results inaccurate.'),('支持哪些协议？','Only http / https; https:// is added when the protocol is omitted.')],
  run='Probe', idle='Not probed yet. Enter a URL and click "Probe".'),
 't6': dict(
  principle='Uses a STUN server to make the browser enumerate all ICE candidates: host (local), srflx (public mapping), etc. Leakage is flagged if WebRTC exposes your real public or private IP. Add ?stun= to customize; closes after 5s.',
  fields=[('ICE 候选','Each candidate IP, type and protocol'),('内网地址','LAN IPs exposed by host candidates'),('STUN','STUN server in use')],
  faq=[('什么是 WebRTC 泄露？','Even with a proxy/VPN, WebRTC may bypass it via STUN and reveal your real IP; this tool detects that.'),('检测到泄露怎么办？','Disable WebRTC in browser settings or install a privacy extension.'),('STUN 服务器会记录我吗？','Public STUN is run by third parties and can see your public IP; use stun= with a server you trust.')],
  run='Check leak', idle='Not checked yet. Run "Public IP Lookup" first for a comparison baseline.'),
 't7': dict(
  principle='Queries several STUN servers for their public mappings and compares ports: identical ports suggest cone NAT; different ports suggest symmetric NAT. Heuristic only, not a precise detection.',
  fields=[('NAT 类型','Cone / symmetric / undetermined'),('各 STUN 映射','Public IP:port seen by each STUN server')],
  faq=[('结果准确吗？','Heuristic inference affected by multi-homing, carrier NAT tiers and STUN availability \u2014 for troubleshooting reference only.'),('锥形和对称有什么区别？','Cone NAT uses a fixed external port (easier P2P); symmetric assigns a different port per destination (harder to traverse).'),('为什么显示无法判断？','Fewer than 2 valid STUN mappings to compare, usually network restrictions or unreachable STUN.')],
  run='Infer NAT', idle='Not inferred yet. Click "Infer NAT".'),
 't8': dict(
  principle='Real DNS egress lookup requires: (1) query logging on your authoritative DNS for a dedicated subdomain; (2) load an image with a random token to trigger a resolution; (3) fetch the resolver IP by token from a static endpoint. This page configures no such endpoint, so it shows setup instructions and never fabricates data.',
  fields=[('状态','Setup required (this page provides no result)'),('配置步骤','Three steps to build your own DNS query logging')],
  faq=[('为什么直接显示配置说明？','The DNS egress IP must come from your own authoritative DNS logs; without a domain and endpoint it cannot be measured honestly, so no fake data is shown.'),('DNS 出口 IP 有什么用？','It reveals which recursive resolver handles your queries \u2014 useful for diagnosing DNS hijacking or privacy leaks.'),('需要后端吗？','Yes: your own domain and a log-reading endpoint. This tool provides neither and uploads nothing.')],
  run='View setup', idle='Requires your own domain to use.'),
 't9': dict(
  principle='Repeatedly requests the specified CDN file and tries to read cf-ray, x-served-by, x-cache edge headers; if CORS hides them, it falls back to round-trip time (RTT) as a node fingerprint.',
  fields=[('URL','CDN file address probed'),('边缘标识','Node identifier read from response headers'),('RTT','Single round-trip time in ms'),('推断命中','Suspected edge node hit')],
  faq=[('为什么读不到节点头？','Custom response headers on cross-origin requests are hidden unless the CDN allows them via CORS.'),('默认探测哪个 CDN？','jsDelivr static file by default; edit the input for other CDNs.'),('RTT 能定位节点吗？','Only a rough network-distance hint, not a precise physical location.')],
  run='Probe', idle='Not probed yet. Click "Probe".'),
 't10': dict(
  principle='Probes favicons of domestic (Baidu/Taobao/QQ) and global (Google/GitHub/Cloudflare) groups in parallel and infers the routing mode from reachability combinations: all-pass, rule-based split, global proxy or network failure. Heuristic, not reading system proxy config.',
  fields=[('代理模式','Inferred routing mode'),('国内目标','Domestic sites reachable count'),('国外目标','Global sites reachable count'),('明细','Per-site reachability and latency')],
  faq=[('这是读取系统代理设置吗？','No. It only infers from external site reachability differences; it cannot read browser/system proxy config.'),('结果为什么可能误判？','Site changes, CDN blocks and local network policy all affect favicon reachability; results are indicative only.'),('能测规则分流吗？','When domestic passes but global partly fails, it suggests rule-based split, but cannot give exact rules.')],
  run='Start test', idle='Not tested yet. Click "Start test".'),
 't11': dict(
  principle='Warms up the connection, takes 10 small requests for median latency and jitter, then downloads 1/5/10MB twice each for median download speed. Endpoint is Cloudflare public __down.',
  fields=[('下行','Median download speed (Mbps)'),('延迟','Median small-request round-trip (ms)'),('抖动','Median latency deviation (ms)'),('轮次','Valid download rounds and endpoint')],
  faq=[('这是专业测速吗？','No, a rough estimate from a public endpoint, affected by node, time and congestion.'),('会消耗流量吗？','Yes, about 30MB of test data in total \u2014 watch mobile data usage.'),('测速时要做什么？','Keep the page in the foreground and avoid competing bandwidth for steadier results.')],
  run='Start test', idle='Not tested yet. Click "Start test".'),
 't12': dict(
  principle='Reads UA, platform, language, timezone, screen resolution, CPU cores, Canvas and WebGL rendering traits locally, joins them and computes a SHA-256 fingerprint (FNV-1a fallback). All local, nothing uploaded.',
  fields=[('指纹哈希','SHA-256 hash of the trait string'),('UA / 平台','Browser and OS identifiers'),('语言 / 时区','Browser language and system timezone'),('屏幕','Resolution, scale and color depth'),('Canvas / WebGL','Graphics rendering traits')],
  faq=[('指纹会被上传吗？','No, all computed locally and shown only to you; this page has no analytics or uploads.'),('指纹能用来追踪我吗？','Sites can use similar traits to identify devices; do not treat it as an anonymous ID \u2014 this is a self-check demo.'),('为什么每次哈希可能变？','Changes in browser/system environment (screen, fonts, GPU driver) change the trait string.')],
  run='Recompute', idle='Not computed yet. Click "Recompute".'),
 't13': dict(
  principle='Concurrently reads public status JSON from each service, maps indicator to operational / degraded / outage and shows update time; unreadable ones show unknown instead of guessing.',
  fields=[('服务','GitHub / Cloudflare / Vercel / npm'),('状态','Operational / degraded / outage / unknown'),('更新于','Last status update time')],
  faq=[('数据来源可靠吗？','Read directly from each provider official public status API \u2014 authoritative.'),('为什么显示 unknown？','Endpoint timeout, CORS limits or temporary unavailability shows unknown rather than assuming healthy.'),('会定时刷新吗？','Click "Refresh status" to re-read; no auto-polling to avoid continuous traffic.')],
  run='Refresh status', idle='Not refreshed yet. Click "Refresh status".'),
}


FIELD_K_EN = {
  'IP': 'IP', '版本': 'Version', '位置': 'Location', 'ISP': 'ISP', 'ASN': 'ASN',
  '时区': 'Timezone', '来源': 'Source', '时间': 'Time', 'IPv6': 'IPv6',
  '查询 IP': 'Queried IP', '归属': 'Region', '域名': 'Domain',
  '内网 IP': 'Private IPs', 'mDNS 混淆地址': 'mDNS addresses',
  '站点': 'Site', '状态': 'Status', '耗时': 'Latency', 'URL': 'URL',
  '方式': 'Method', '结果': 'Result', 'ICE 候选': 'ICE candidates',
  '内网地址': 'Private addresses', 'STUN': 'STUN', 'NAT 类型': 'NAT type',
  '各 STUN 映射': 'STUN mappings', '配置步骤': 'Setup steps',
  '边缘标识': 'Edge ID', 'RTT': 'RTT', '推断命中': 'Likely edge',
  '代理模式': 'Proxy mode', '国内目标': 'Domestic', '国外目标': 'Global',
  '明细': 'Details', '下行': 'Download', '延迟': 'Latency', '抖动': 'Jitter',
  '轮次': 'Rounds', '指纹哈希': 'Fingerprint hash', 'UA / 平台': 'UA / platform',
  '语言 / 时区': 'Language / timezone', '屏幕': 'Screen', 'Canvas / WebGL': 'Canvas / WebGL',
  '服务': 'Service', '更新于': 'Updated at',
}

FAQ_Q_EN = {
  '为什么结果和本地 IP 不同？': 'Why does this differ from my local IP?',
  '多源回退是什么意思？': 'What is multi-source fallback?',
  'IP 查询准确吗？': 'Is the IP lookup accurate?',
  '支持哪些格式？': 'Which formats are supported?',
  '能查内网 IP 吗？': 'Can I look up private IPs?',
  '数据来源是谁？': 'Where is the data from?',
  '为什么需要点击按钮？': 'Why must I click a button?',
  '为什么显示 .local 结尾？': 'Why do I see .local addresses?',
  '多网卡会显示多个吗？': 'Will multiple NICs show up?',
  '这能代表网站正常吗？': 'Does this mean the site is healthy?',
  '为什么有的站点总是不可达？': 'Why is a site always unreachable?',
  '会上传我的信息吗？': 'Is my info uploaded?',
  '为什么不显示 HTTP 状态码？': 'Why no HTTP status code?',
  '可以探测内网地址吗？': 'Can I probe internal URLs?',
  '支持哪些协议？': 'Which protocols are supported?',
  '什么是 WebRTC 泄露？': 'What is a WebRTC leak?',
  '检测到泄露怎么办？': 'What if a leak is found?',
  'STUN 服务器会记录我吗？': 'Does the STUN server log me?',
  '结果准确吗？': 'Is the result accurate?',
  '锥形和对称有什么区别？': 'Cone vs symmetric?',
  '为什么显示无法判断？': 'Why undetermined?',
  '为什么直接显示配置说明？': 'Why only setup instructions?',
  'DNS 出口 IP 有什么用？': 'What is a DNS egress IP for?',
  '需要后端吗？': 'Does it need a backend?',
  '为什么读不到节点头？': 'Why can\'t I read edge headers?',
  '默认探测哪个 CDN？': 'Which CDN by default?',
  'RTT 能定位节点吗？': 'Can RTT locate a node?',
  '这是读取系统代理设置吗？': 'Does it read system proxy settings?',
  '结果为什么可能误判？': 'Why might it misjudge?',
  '能测规则分流吗？': 'Can it detect rule-based split?',
  '这是专业测速吗？': 'Is this a professional speed test?',
  '会消耗流量吗？': 'Does it use data?',
  '测速时要做什么？': 'What should I do during the test?',
  '指纹会被上传吗？': 'Is the fingerprint uploaded?',
  '指纹能用来追踪我吗？': 'Can it be used to track me?',
  '为什么每次哈希可能变？': 'Why does the hash change?',
  '数据来源可靠吗？': 'Is the data reliable?',
  '为什么显示 unknown？': 'Why unknown?',
  '会定时刷新吗？': 'Does it auto-refresh?',
}


def build_map(t):
    e = EN[t['id']]
    m = dict(COMMON)
    m[t['name']] = t['en']
    m[t['icon'] + ' ' + t['name']] = t['icon'] + ' ' + t['en']
    m[t['desc']] = t['ed']
    m[t['principle']] = e['principle']
    run_zh = RUN_LABEL[t['id']]
    idle_zh = IDLE.get(t['id'], '尚未执行，点击上方按钮开始。')
    m[run_zh] = e['run']
    m[idle_zh] = e['idle']
    # 历史表初始空态串含运行按钮文案，按工具动态生成整句映射
    m['尚未有运行记录，点击上方「' + run_zh + '」开始。'] = \
        'No run history yet. Click "' + e['run'] + '" above to start.'
    # 字段表：th 是字段 key，td 是字段描述 —— 两者都要映射
    for (k, v), (_, ev) in zip(t['fields'], e['fields']):
        m[k] = FIELD_K_EN.get(k, k)
        m[v] = ev
    # FAQ：问题用 FAQ_Q_EN，答案用 EN faq 的第二个元素（英文）
    for (q, a), (_, ea) in zip(t['faq'], e['faq']):
        m[q] = FAQ_Q_EN.get(q, q)
        m[a] = ea
    return {k: v for k, v in m.items() if k and v}


def insert_obj_before_close(path, entries_indent, entries):
    """在文件末尾的 } 前插入若干 JSON 条目（保持原格式）。"""
    s = open(path, encoding='utf-8').read().rstrip()
    assert s.endswith('}'), path
    body = s[:-1].rstrip()  # 去掉末尾 }
    add = ''.join(entries)
    # body 末尾可能是 { 空对象 或 已有内容
    if body.rstrip().endswith('{'):
        new = body + add + '\n}'
    else:
        new = body + ',\n' + add + '\n}'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new)


def main():
    idx_path = os.path.join(ROOT, 'i18n', 'tools', 'en', 'telecom', '_index.json')
    idx = json.load(open(idx_path, encoding='utf-8'))

    # 1) per-tool map（新文件，标准 dump）
    for t in TOOLS:
        m = build_map(t)
        out = {'slug': t['slug'], 'industry': 'telecom', 'name': t['en'], 'map': m}
        p = os.path.join(ROOT, 'i18n', 'tools', 'en', 'telecom', t['slug'] + '.json')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print('EN map', t['slug'], len(m))

    # 2) _index.json 数组追加（标准 dump 即可，格式是 2 空格）
    for t in TOOLS:
        if t['slug'] not in idx['tools']:
            idx['tools'].append(t['slug'])
    with open(idx_path, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
        f.write('\n')

    # 3) telecom-body.json（2 空格格式，用 dump 保留既有键）
    body_path = os.path.join(ROOT, 'i18n', 'tools', 'telecom-body.json')
    body = json.load(open(body_path, encoding='utf-8'))
    for t in TOOLS:
        body[t['slug']] = {'title': t['en'], 'intro': t['ed'], 'h1': t['en'],
                           'en': {'title': t['en'], 'intro': t['ed'], 'h1': t['en']}}
    with open(body_path, 'w', encoding='utf-8') as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
        f.write('\n')

    # 4) _en_override.json（紧凑格式，字节插入；dump 无法字节还原，故只追加不改既有）
    ov_path = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
    ov = json.load(open(ov_path, encoding='utf-8'))
    new_ov = [t for t in TOOLS if ('telecom/' + t['slug']) not in ov]
    if new_ov:
        s = open(ov_path, encoding='utf-8').read().rstrip()
        assert s.endswith('}')
        inner = s[:-1].rstrip()  # 末尾条目的 }
        parts = []
        for t in new_ov:
            key = json.dumps('telecom/' + t['slug'], ensure_ascii=False)
            val = json.dumps({'en': t['en'], 'ed': t['ed'], 'ind': 'telecom'}, ensure_ascii=False, separators=(',', ':'))
            parts.append(key + ':' + val)
        open(ov_path, 'w', encoding='utf-8').write(inner + ',\n' + ',\n'.join(parts) + '\n}')

    # 5) slug-en.json（indent=2 可字节还原，用 dict 追加 + dump）
    slug_path = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')
    slug = json.load(open(slug_path, encoding='utf-8'))
    for t in TOOLS:
        slug['telecom/' + t['slug']] = {'en': t['en'], 'ed': t['ed']}
    with open(slug_path, 'w', encoding='utf-8') as f:
        json.dump(slug, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print('DONE. index', len(idx['tools']), 'body', len(body), 'new_ov', len(new_ov))


if __name__ == '__main__':
    main()
