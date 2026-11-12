#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 13 个 telecom 分类的独立网络工具页。
统一竞品风格 UI（大标题区 + 醒目执行区 + 大结果展示 + 字段表 + FAQ + 相关工具），
共享 js/network-toolbox.js（body[data-tool] 标识当前工具）。
仅生成 tools/telecom/<slug>.html，不触碰其它文件。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'tools', 'telecom')

# 13 工具配置
TOOLS = [
  dict(id='t1', slug='public-ip-lookup', name='公网 IP 查询', en='Public IP Lookup', icon='🌌',
    desc='展示当前公网 IP、版本、地区、ISP、ASN、时区与数据来源，多源自动回退，IPv6 单独探测。',
    ed='Show your public IP, version, region, ISP, ASN and timezone with multi-source fallback and separate IPv6 detection.',
    principle='按 ipwho.is → ipapi.co → api.ip.sb → ipify 顺序请求公网 IP 归属服务，首个成功即采用；随后单独探测 IPv6 地址。全部请求走浏览器 fetch 并设 6 秒超时，失败自动切换下一数据源。',
    fields=[('IP','当前出口公网 IP 地址'),('版本','IPv4 或 IPv6'),('位置','国家 / 省州 / 城市'),('ISP','互联网服务提供商'),('ASN','自治系统编号'),('时区','IP 归属地时区（取数据源 id 字段）'),('来源','实际命中的数据源'),('时间','查询时间（ISO 8601）'),('IPv6','单独探测到的 IPv6 地址（若有）')],
    faq=[('为什么结果和本地 IP 不同？','这里显示的是你的公网出口 IP（路由器对外地址），与局域网内 192.168.x.x / 10.x.x.x 的内网 IP 不同。'),('多源回退是什么意思？','首个接口失败或超时会自动切换备用接口，提高成功率；结果里的「来源」字段会标明最终采用哪个源。'),('IP 查询准确吗？','归属地为第三方数据库推断，精确到城市级别，可能有误差，仅供参考。')]),
  dict(id='t2', slug='ip-geolocation', name='IP 归属地查询', en='IP Geolocation', icon='📍',
    desc='输入任意 IPv4/IPv6 查归属：国家、地区、城市、ISP、ASN、域名，先校验格式再请求。',
    ed='Look up any IPv4/IPv6 address for country, region, city, ISP, ASN and domain, with format validation before request.',
    principle='先本地校验 IP 格式（IPv4 四段十进制 / IPv6 冒号分组），合法才发请求；主源 ipwho.is 失败回退 ipapi.co。支持回车触发查询。',
    fields=[('查询 IP','你输入的 IP 地址'),('归属','国家 / 省州 / 城市'),('ISP','该 IP 的运营商'),('ASN','自治系统编号'),('域名','关联域名（若数据源提供）')],
    faq=[('支持哪些格式？','标准 IPv4（如 8.8.8.8）与 IPv6（如 2001:4860:4860::8888）。格式不合法时不会发送请求。'),('能查内网 IP 吗？','内网保留地址（如 192.168.1.1）没有公网归属信息，查询结果可能为空。'),('数据来源是谁？','使用 ipwho.is 与 ipapi.co 公开接口，归属数据库由对方维护。')]),
  dict(id='t3', slug='local-ip-address', name='本机内网 IP', en='Local IP Address', icon='🏠',
    desc='用无 STUN 的 WebRTC host candidate 收集本机内网地址，标注 mDNS 混淆地址。',
    ed='Collect your local private IP addresses via WebRTC host candidates (no STUN) and flag mDNS-obfuscated ones.',
    principle='创建不带 STUN 服务器的 RTCPeerConnection，通过本地 SDP 的 host candidate 读取网卡内网地址，3 秒后自动关闭连接。不连接任何外部服务器。',
    fields=[('内网 IP','host candidate 中的局域网地址及协议'),('mDNS 混淆地址','浏览器用 .local 后缀隐藏的真实地址')],
    faq=[('为什么需要点击按钮？','浏览器要求 WebRTC 由用户手势触发，页面加载后需手动点一次「收集本机地址」。'),('为什么显示 .local 结尾？','部分浏览器启用 mDNS 混淆，真实内网 IP 被替换成随机 .local 域名，属于隐私保护机制。'),('多网卡会显示多个吗？','会逐个列出所有 host candidate，包括蓝牙、虚拟网卡等产生的地址。')]),
  dict(id='t4', slug='site-reachability', name='网站可达性检测', en='Site Reachability', icon='🌐',
    desc='并发探测 Google / GitHub / Cloudflare / OpenAI 的 favicon，记录可达性与近似耗时。',
    ed='Probe favicons of Google, GitHub, Cloudflare and OpenAI in parallel, recording reachability and approximate latency.',
    principle='并发加载各站点的 favicon 图片，以 onload / onerror / 超时判定可达性并记录耗时，并发上限 5。图片探测绕过 CORS 限制，但只能判断网络层是否可达。',
    fields=[('站点','被探测的目标站点'),('状态','可达 / 超时 / 不可达'),('耗时','图片加载的近似毫秒数')],
    faq=[('这能代表网站正常吗？','只能说明本机网络层能取到 favicon，不等于网站全部功能正常，也不读取 HTTP 状态码。'),('为什么有的站点总是不可达？','可能是 CDN 拦截、favicon 改版或本地网络策略，结果仅供参考。'),('会上传我的信息吗？','不会，仅由浏览器直接请求目标 favicon，不经过任何中间服务器。')]),
  dict(id='t5', slug='url-reachability', name='URL 可达性检测', en='URL Reachability', icon='🔗',
    desc='输入任意 URL（无协议自动补 https://），用 fetch no-cors 或 favicon 图片判断网络层可达性。',
    ed='Enter any URL (https:// added automatically) and check network-layer reachability via fetch no-cors or favicon image.',
    principle='先用 fetch 的 no-cors 模式请求目标 URL 判断网络层是否接受连接；若失败则回退为请求该站点 favicon 图片。no-cors 返回 opaque 响应，无法读取状态码。',
    fields=[('URL','最终请求的完整地址'),('方式','fetch no-cors 或 image'),('结果','可达 / 超时 / 不可达'),('耗时','探测耗时（毫秒）')],
    faq=[('为什么不显示 HTTP 状态码？','no-cors 模式下浏览器隐藏响应内容，只能判断请求是否被网络层接受，无法读取 200/404 等状态码。'),('可以探测内网地址吗？','可以输入内网 URL，但受浏览器混合内容与 CORS 策略限制，结果可能不准确。'),('支持哪些协议？','仅 http / https，省略协议时默认补 https://。')]),
  dict(id='t6', slug='webrtc-leak-test', name='WebRTC 泄露检测', en='WebRTC Leak Test', icon='🔓',
    desc='用公共 STUN 收集全部 ICE 候选，解析 IP / 类型 / 协议，列出内网与 mDNS 地址。',
    ed='Collect all ICE candidates via public STUN, parse IP/type/protocol, and list private and mDNS addresses.',
    principle='通过 STUN 服务器让浏览器枚举所有 ICE 候选：host（本地）、srflx（公网映射）等。若 WebRTC 暴露了你的真实公网或内网 IP，即存在泄露。可用网址参数 stun= 自定义 STUN 服务器，5 秒后自动关闭连接。',
    fields=[('ICE 候选','每个候选的 IP、类型与协议'),('内网地址','host 类型暴露的局域网 IP'),('STUN','使用的 STUN 服务器')],
    faq=[('什么是 WebRTC 泄露？','即使使用代理/VPN，WebRTC 可能通过 STUN 绕过并暴露真实 IP，此工具帮你检测是否发生。'),('检测到泄露怎么办？','可在浏览器设置中禁用 WebRTC 或安装相关隐私扩展。'),('STUN 服务器会记录我吗？','公共 STUN 由第三方运营，理论上可看到你的公网 IP；可用 stun= 参数换用你信任的服务器。')]),
  dict(id='t7', slug='nat-type-test', name='NAT 类型检测', en='NAT Type Test', icon='🧭',
    desc='向 3 个公共 STUN 分别取 srflx 映射的 IP:端口，按端口是否一致推断锥形或对称 NAT。',
    ed='Query srflx mappings from 3 public STUN servers and infer cone vs symmetric NAT from port consistency.',
    principle='向多个 STUN 服务器分别发起映射请求，比较返回的公网映射端口：若各服务器看到的端口一致，多为锥形 NAT；端口各不相同则多为对称 NAT。基于 STUN 的启发式推断，非精确检测。',
    fields=[('NAT 类型','锥形 / 对称 / 无法判断'),('各 STUN 映射','每个 STUN 服务器看到的公网 IP:端口')],
    faq=[('结果准确吗？','这是启发式推断，受多出口、运营商多级 NAT、STUN 可用性影响，仅供网络排查参考。'),('锥形和对称有什么区别？','锥形 NAT 对外端口固定，便于 P2P 直连；对称 NAT 对每目标分配不同端口，P2P 更难穿透。'),('为什么显示无法判断？','少于 2 个 STUN 返回有效映射时无法比较，通常是网络限制或 STUN 不可达。')]),
  dict(id='t8', slug='dns-egress-lookup', name='DNS 出口查询', en='DNS Egress Lookup', icon='🧭',
    desc='说明如何用自有域名与权威 DNS 日志查出递归解析器的出口 IP；本页未配置接口，明确降级不伪造数据。',
    ed='Explains how to reveal your recursive resolver IP using your own domain and DNS logs; this page provides no endpoint and degrades honestly.',
    principle='真实查询 DNS 出口需要：① 在权威 DNS 为专属子域开启查询日志；② 页面用随机 token 加载图片触发一次解析；③ 从静态接口按 token 取回解析器 IP。本页不配置任何自有域名接口，因此只展示配置说明，不生成假结果。',
    fields=[('状态','需配置（本页不提供结果）'),('配置步骤','搭建自有域名解析日志的三步说明')],
    faq=[('为什么直接显示配置说明？','DNS 出口 IP 必须从你自己的权威 DNS 日志读取，没有自有域名和接口时无法真实测得，故不伪造数据。'),('DNS 出口 IP 有什么用？','可判断你的 DNS 查询经由哪个递归解析器，用于排查 DNS 劫持或隐私泄露。'),('需要后端吗？','需要自有域名和能读取日志的接口，本工具不提供也不上传任何数据。')]),
  dict(id='t9', slug='cdn-edge-check', name='CDN 节点探测', en='CDN Edge Check', icon='⚡',
    desc='请求同一 CDN 静态文件，读取 cf-ray / x-served-by / x-cache 响应头，读不到时退化为 RTT 指纹。',
    ed='Request the same CDN static file, read cf-ray / x-served-by / x-cache headers, falling back to RTT fingerprint.',
    principle='多次请求指定 CDN 文件，尝试读取 cf-ray、x-served-by、x-cache 等边缘节点响应头；若 CORS 隐藏了这些头，则退化为以往返时延（RTT）作为节点指纹。',
    fields=[('URL','被探测的 CDN 文件地址'),('边缘标识','从响应头读到的节点标识'),('RTT','单次往返时延（毫秒）'),('推断命中','疑似命中的边缘节点')],
    faq=[('为什么读不到节点头？','跨域请求的自定义响应头默认被浏览器隐藏（CORS），除非 CDN 显式允许，此时只能看 RTT。'),('默认探测哪个 CDN？','默认用 jsDelivr 的静态文件，可在输入框改成其它 CDN 地址。'),('RTT 能定位节点吗？','只能粗略反映网络远近，不能精确定位物理位置。')]),
  dict(id='t10', slug='proxy-routing-test', name='代理分流测试', en='Proxy Routing Test', icon='🔀',
    desc='分别探测国内组与国外组站点，按通过数推断可能的代理分流模式，并给出逐项明细。',
    ed='Probe domestic and global site groups separately to infer possible proxy routing mode with per-target details.',
    principle='并发探测国内组（百度/淘宝/QQ）与国外组（Google/GitHub/Cloudflare）的 favicon，按两组的可达性组合推断：全通、规则分流、全局代理或网络故障。属启发式推断，非读取系统代理配置。',
    fields=[('代理模式','推断出的分流模式'),('国内目标','国内站点可达数'),('国外目标','国外站点可达数'),('明细','逐站点可达性与耗时')],
    faq=[('这是读取系统代理设置吗？','不是，只通过外部站点的可达性差异推断，无法读取浏览器或系统的代理配置。'),('结果为什么可能误判？','站点改版、CDN 拦截、本地网络策略都会影响 favicon 可达性，结果仅供参考。'),('能测规则分流吗？','当国内通、国外部分不通时，通常提示规则分流，但无法给出具体规则。')]),
  dict(id='t11', slug='network-speed-test', name='网络测速', en='Network Speed Test', icon='🚀',
    desc='用 Cloudflare 测速端点：预热后多次小请求取延迟中位数与抖动，多轮下载取下行中位数。',
    ed='Use Cloudflare speed endpoint: warm-up, repeated small requests for latency/jitter, multi-round downloads for median download speed.',
    principle='先预热连接，再发 10 次小请求取延迟中位数与抖动；随后对 1/5/10MB 各下载 2 轮，取下行速率中位数。测速端点为 Cloudflare 公共 __down 接口。',
    fields=[('下行','下载速率中位数（Mbps）'),('延迟','小请求往返中位数（毫秒）'),('抖动','延迟偏差中位数（毫秒）'),('轮次','有效下载轮数与端点')],
    faq=[('这是专业测速吗？','不是，仅用公共端点做粗略估算，受节点、时段、网络拥塞影响较大。'),('会消耗流量吗？','会下载约 30MB 测试数据（多轮累加），请留意移动网络流量。'),('测速时要做什么？','保持页面在前台、避免同时占用带宽，结果更稳定。')]),
  dict(id='t12', slug='browser-fingerprint', name='浏览器指纹', en='Browser Fingerprint', icon='🔖',
    desc='本地采集 UA、语言、时区、屏幕、CPU、Canvas 与 WebGL 特征，计算哈希指纹。',
    ed='Collect UA, language, timezone, screen, CPU, Canvas and WebGL traits locally and compute a fingerprint hash.',
    principle='在浏览器本地读取 UA、平台、语言、时区、屏幕分辨率、CPU 核心数、Canvas 与 WebGL 渲染特征，拼接后用 SHA-256 计算指纹（不支持时降级 FNV-1a）。全部本地计算，不上报。',
    fields=[('指纹哈希','特征串的 SHA-256 哈希'),('UA / 平台','浏览器与系统标识'),('语言 / 时区','浏览器语言与系统时区'),('屏幕','分辨率、缩放与色深'),('Canvas / WebGL','图形渲染特征')],
    faq=[('指纹会被上传吗？','不会，全部在本地计算，结果只显示在你眼前，本页不埋点不上报。'),('指纹能用来追踪我吗？','站点可用类似特征识别设备，请勿把它当作匿名标识；本工具仅作科普自查。'),('为什么每次哈希可能变？','浏览器或系统环境变化（如屏幕、字体、GPU 驱动）会改变特征串。')]),
  dict(id='t13', slug='service-status', name='服务状态查询', en='Service Status', icon='📊',
    desc='聚合 GitHub / Cloudflare / Vercel / npm 的公开状态 JSON，5 秒超时，失败显示 unknown。',
    ed='Aggregate public status JSON from GitHub, Cloudflare, Vercel and npm with 5s timeout, showing unknown on failure.',
    principle='并发读取各服务的公开状态 JSON，把 indicator 映射为 operational / degraded / outage，并展示更新时间；读不到时明确显示 unknown，不猜测状态。',
    fields=[('服务','GitHub / Cloudflare / Vercel / npm'),('状态','正常 / 降级 / 故障 / 未知'),('更新于','状态最后更新时间')],
    faq=[('数据来源可靠吗？','直接读取各服务商官方状态页的公开 API，权威可靠。'),('为什么显示 unknown？','接口超时、CORS 限制或服务临时不可用时显示未知，不会臆测正常。'),('会定时刷新吗？','点击「刷新状态」重新读取，本页不自动轮询以免产生持续流量。')]),
]

TPL = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script src="/js/tool-page-runtime.js" defer></script>
<!-- TOOLBOX-TOOL-RUNTIME -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=dev,industry=telecom,icon={icon},bg=#e3f2fd">
<meta name="description" content="{desc}">
<meta name="keywords" content="{name},网络工具,IP,WebRTC,NAT,CDN,测速,指纹,通信技术,在线工具,免费工具,ToolBox">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://chenguangwu.github.io/tools/telecom/{slug}.html">
<meta property="og:title" content="{name} - 免费在线通信技术工具">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://chenguangwu.github.io/tools/telecom/{slug}.html">
<meta name="twitter:card" content="summary">
<title>{name} - 免费在线通信技术工具</title>
<meta name="theme-color" content="#FF6B35">
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="icon" href="../../favicon.ico" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="../../apple-touch-icon.png">
<link rel="stylesheet" href="../../css/common.css">
<style>
.nt-hero{{display:flex;gap:16px;align-items:flex-start;background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:22px 24px;margin-bottom:18px;}}
.nt-hero .ico{{font-size:40px;line-height:1;flex-shrink:0;}}
.nt-hero h2{{font-size:22px;margin:0 0 6px;color:var(--heading);}}
.nt-hero .sub{{font-size:14px;color:var(--text-muted);margin:0;line-height:1.7;}}
.nt-run{{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:22px 24px;margin-bottom:18px;}}
.nt-run .row{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:16px;}}
.nt-run input{{flex:1 1 320px;min-width:0;padding:12px 14px;font-size:15px;border:1px solid var(--border);border-radius:10px;background:var(--bg);color:var(--heading);}}
.nt-run .btn{{padding:12px 22px;font-size:15px;border-radius:10px;}}
.nt-run .btn.primary{{font-weight:600;}}
.nt-out{{font-family:'SF Mono','Courier New',monospace;font-size:15px;line-height:1.9;white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere;background:var(--bg);border:1px solid var(--border);border-left:4px solid var(--primary);border-radius:12px;padding:18px 20px;min-height:120px;max-height:520px;overflow:auto;color:var(--text-light);}}
.nt-out[data-s="ok"]{{border-left-color:#2e7d32;}}
.nt-out[data-s="error"]{{border-left-color:var(--danger);color:var(--danger);}}
.nt-badge{{font-size:12px;padding:4px 12px;border-radius:999px;background:var(--bg-hover);color:var(--text-muted);font-weight:500;white-space:nowrap;}}
.nt-badge[data-s="loading"]{{background:#fff3e0;color:#e65100;}}
.nt-badge[data-s="ok"]{{background:#e8f5e9;color:#2e7d32;}}
.nt-badge[data-s="error"]{{background:#ffebee;color:#c62828;}}
.nt-sec{{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:20px 24px;margin-bottom:18px;}}
.nt-sec h3{{font-size:17px;margin:0 0 14px;color:var(--heading);}}
.nt-sec p{{font-size:14px;color:var(--text-light);line-height:1.8;margin:0;}}
.nt-table{{width:100%;border-collapse:collapse;font-size:14px;}}
.nt-table th,.nt-table td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top;}}
.nt-table th{{color:var(--heading);font-weight:600;width:150px;background:var(--bg-hover);}}
.nt-table td{{color:var(--text-light);}}
.nt-faq details{{border-bottom:1px solid var(--border);padding:12px 0;}}
.nt-faq details:last-child{{border-bottom:0;}}
.nt-faq summary{{font-size:15px;font-weight:500;color:var(--heading);cursor:pointer;}}
.nt-faq .ans{{font-size:14px;color:var(--text-light);line-height:1.8;padding:10px 0 0;}}
.nt-preset{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 14px;font-size:13px;color:var(--text-muted);}}
.nt-preset button,.nt-preset a{{padding:6px 12px;font-size:12px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text-light);cursor:pointer;text-decoration:none;}}
.nt-preset button:hover,.nt-preset a:hover{{border-color:var(--primary);color:var(--primary);}}
.nt-hist{{width:100%;border-collapse:collapse;font-size:13px;}}
.nt-hist th,.nt-hist td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--border);}}
.nt-hist th{{color:var(--heading);font-weight:600;background:var(--bg-hover);}}
.nt-hist td{{color:var(--text-light);word-break:break-word;}}
.nt-hist button{{padding:4px 10px;font-size:11px;}}
.nt-diff{{margin-top:6px;padding:8px 10px;background:var(--bg);border-radius:6px;font-family:'SF Mono','Courier New',monospace;font-size:12px;white-space:pre-wrap;word-break:break-word;max-height:160px;overflow:auto;}}
mark{{background:rgba(255,107,53,.2);color:inherit;border-radius:2px;padding:0 2px;}}
@media(max-width:600px){{.nt-hero{{padding:18px;}}.nt-hero .ico{{font-size:32px;}}.nt-hero h2{{font-size:19px;}}.nt-run,.nt-sec{{padding:18px;}}.nt-table th{{width:auto;}}}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"}},{{"@type":"ListItem","position":2,"name":"通信技术","item":"https://chenguangwu.github.io/tools/telecom/index.html"}},{{"@type":"ListItem","position":3,"name":"{name}","item":"https://chenguangwu.github.io/tools/telecom/{slug}.html"}}]}}
</script>
<!-- TOOLBOX-WEBAPP-LD -->
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication","name":"{name}","url":"https://chenguangwu.github.io/tools/telecom/{slug}.html","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","inLanguage":["zh-CN", "zh-TW", "en-US"],"description":"{desc}","image":"https://chenguangwu.github.io/og-image.png","offers":{{"@type":"Offer","price":"0","priceCurrency":"CNY"}}}}
</script>
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">
<meta name="twitter:title" content="{name} - 免费在线通信技术工具">
<meta name="twitter:description" content="{desc}">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
<!-- TOOLBOX-SECURITY -->
<script src="/js/privacy.js" defer></script>
<!-- TOOLBOX-PRIVACY-SCRIPT -->
<script src="/js/metrics.js" defer></script>
<!-- TOOLBOX-METRICS-SCRIPT -->
<script src="../../js/i18n.js" defer></script>
<script src="../../js/tool-i18n.js" defer></script>
<!-- TOOLBOX-I18N-SCRIPT -->
<!-- TOOLBOX-HREFLANG -->
<link rel="preload" as="style" href="/css/nav-menu.css" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/nav-menu.css"></noscript>
<script src="/js/industry-info.js" defer></script>
<script src="/js/nav-menu.js" defer></script>
<script src="/js/tool-ux.js" defer></script>
<!-- TOOLBOX-TOOL-UX -->
<script src="/js/tool-kit.js" defer></script>
<!-- TOOLBOX-TOOL-KIT -->
<script src="/js/analytics.js" defer></script>
<!-- TOOLBOX-CLARITY -->
</head>
<body data-tool="{id}">
<h1 class="sr-only">{name}</h1>
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ {name}</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>
<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">📡 通信技术</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">{name}</span>
</nav>
<div class="container">
  <div class="nt-hero card tool-card-accent" style="--tool-accent:#FF6B35;">
    <div class="ico">{icon}</div>
    <div>
      <h2>{name}</h2>
      <p class="sub">{desc}</p>
    </div>
  </div>

  <div class="card formula-box">
    <div class="formula-title">📐 工作原理与说明</div>
    <div class="formula-eq">{principle}</div>
  </div>

  <div class="nt-run" id="card-{id}">
    <div class="row">
      <span class="nt-badge" data-s="idle" aria-live="polite">空态</span>
      {input_html}
      <button type="button" class="btn primary" data-run="{id}">{run_label}</button>
      <button type="button" class="btn success" data-copy="{id}">复制结果</button>
    </div>
    {preset_html}
    <div class="nt-out" id="result-{id}" data-s="idle" aria-live="polite">{idle_text}</div>
  </div>

  <div class="nt-sec">
    <h3>📋 输出字段说明</h3>
    <table class="nt-table">
      <tbody>{field_rows}</tbody>
    </table>
  </div>

  <div class="nt-sec">
    <h3>🕘 本机运行记录与对比</h3>
    <p style="font-size:13px;color:var(--text-muted);line-height:1.7;margin:0 0 12px;">最近一次成功结果只保存在你本机浏览器（localStorage），不上传。可展开对比本次与上次输出的变化；换浏览器或清除站点数据后记录会消失。</p>
    <div style="overflow-x:auto;">
      <table class="nt-hist">
        <thead><tr><th>状态</th><th>最近成功时间</th><th>上次结果摘要</th><th>操作</th></tr></thead>
        <tbody id="ntHistoryBody"><tr><td colspan="4">尚未有运行记录，点击上方「{run_label}」开始。</td></tr></tbody>
      </table>
    </div>
  </div>

  <div class="nt-sec">
    <h3>🔗 延伸工具</h3>
    <p style="font-size:13px;color:var(--text-muted);line-height:1.7;margin:0 0 12px;">以下工具与本页面常一起使用：</p>
    <div class="nt-preset">
      <a href="subnet-planner.html">子网划分工具</a>
      <a href="bandwidth-calculator.html">带宽下载时间速算</a>
    </div>
  </div>

  <div class="nt-sec nt-faq">
    <h3>❓ 常见问题</h3>
    {faq_html}
  </div>
</div>
<div class="related-tools" data-related-tools="1">
  <h3 class="related-tools-title">🔗 相关工具</h3>
  <div class="related-tools-grid"></div>
</div>
<script>
/* 本页独立的本机历史存储适配层：共享 JS 通过 window.__ntStorage 读写，
   key 按工具隔离，避免不同工具结果互相覆盖；无任何上传。 */
window.__ntStorage = (function () {{
  var KEY = 'ntHist_v1:{id}';
  return {{
    read: function () {{ try {{ return JSON.parse(localStorage.getItem(KEY) || '{{}}') || {{}}; }} catch (e) {{ return {{}}; }} }},
    write: function (v) {{ try {{ localStorage.setItem(KEY, JSON.stringify(v)); }} catch (e) {{}} }}
  }};
}})();
</script>
<script src="../../js/common.js" defer></script>
<script src="../../js/network-toolbox.js" defer></script>
</body>
</html>
'''

INPUTS = {
  't2': '<input type="text" id="t2-ip" placeholder="如 8.8.8.8 或 2001:4860:4860::8888" inputmode="text">',
  't5': '<input type="text" id="t5-url" placeholder="https://example.com" inputmode="url">',
  't9': '<input type="text" id="t9-url" value="https://cdn.jsdelivr.net/npm/jquery@3.7.1/package.json" inputmode="url">',
}
RUN_LABEL = {
  't1':'刷新查询','t2':'查询','t3':'收集本机地址','t4':'开始探测','t5':'探测','t6':'检测泄露',
  't7':'推断 NAT','t8':'查看配置说明','t9':'探测','t10':'开始测试','t11':'开始测速','t12':'重新计算','t13':'刷新状态',
}
IDLE = {
  't1':'尚未查询，点击「刷新查询」开始（页面加载后会自动查询一次）。',
  't6':'尚未检测。可先运行「公网 IP 查询」以获得对比基准。',
  't8':'需配置自有域名后才能使用。',
}
# 常用预设（真实功能：点击填入输入并可直接执行）
PRESETS = {
  't2': [('8.8.8.8', 't2-ip', '8.8.8.8'), ('1.1.1.1', 't2-ip', '1.1.1.1'), ('2001:4860:4860::8888', 't2-ip', '2001:4860:4860::8888')],
  't5': [('example.com', 't5-url', 'https://example.com'), ('github.com', 't5-url', 'https://github.com')],
  't9': [('jsDelivr', 't9-url', 'https://cdn.jsdelivr.net/npm/jquery@3.7.1/package.json'),
         # 用 package.json 而非 vue.global.prod.js：后者会被外部依赖审计当成未锁版本脚本，
         # 但它只是 CDN 响应头的探测目标，改 JSON 资源不影响 T9 功能。
         ('unpkg', 't9-url', 'https://unpkg.com/vue@3.5.13/package.json')],
}


def build(tool):
    tid = tool['id']
    inp = INPUTS.get(tid, '')
    field_rows = ''.join('<tr><th>%s</th><td>%s</td></tr>' % (k, v) for k, v in tool['fields'])
    faq_html = ''.join('<details><summary>%s</summary><div class="ans">%s</div></details>' % (q, a) for q, a in tool['faq'])
    presets = PRESETS.get(tid, [])
    if presets:
        btns = ''.join('<button type="button" data-fill="%s" data-value="%s">%s</button>' % (target, val, label) for label, target, val in presets)
        lead = '常用预设：'
    else:
        # 无输入项工具：预设 = 一键重新执行（真实动作，不是装饰按钮）
        btns = '<button type="button" data-action="run">立即刷新</button>'
        lead = '常用预设 / 快捷操作：'
    preset_html = '<div class="nt-preset"><span>' + lead + '</span>' + btns + '</div>'
    html = TPL.format(
        id=tid, slug=tool['slug'], name=tool['name'], en=tool['en'], icon=tool['icon'],
        desc=tool['desc'], ed=tool['ed'], principle=tool['principle'],
        input_html=inp, run_label=RUN_LABEL[tid], idle_text=IDLE.get(tid, '尚未执行，点击上方按钮开始。'),
        preset_html=preset_html, field_rows=field_rows, faq_html=faq_html,
    )
    return html


def main():
    os.makedirs(OUT, exist_ok=True)
    for tool in TOOLS:
        path = os.path.join(OUT, tool['slug'] + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(build(tool))
        print('WROTE', path)


if __name__ == '__main__':
    main()
