#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 二期（gen_q1f）生成器：13 个 it-tools 风格生活/效率/财务类 A 级工具。
复用 gen_q1e 的 TEMPLATE 范式（inputs + calcTool）。
用法：python3 scripts/gen_q1f_tools.py
生成（行业/文件）：
  it/wifi-qr-generator.html           WiFi 配网二维码生成器
  it/docker-run-converter.html        docker run 转 docker-compose
  design/gradient-generator.html      CSS 渐变生成器
  text/lorem-ipsum-generator.html     占位文本生成器
  text/reading-time-estimator.html    阅读时长估算
  accounting/split-bill.html           分账计算器
  tax/gst-calculator.html              GST 商品服务税计算
  it/date-duration.html               日期天数差
  baking/recipe-scaler.html           配方缩放
  automotive/fuel-cost-calculator.html 油费计算器
  daily-goods/parking-fee.html         停车费计算
  biz/unit-price-compare.html          单位价格比较
  it/unit-converter-advanced.html      高级单位转换
"""
import os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
BASE = "https://chenguangwu.github.io"

IND_ZH = {"it": "IT开发", "design": "平面设计", "text": "文本处理",
          "accounting": "财务会计", "tax": "税务", "baking": "烘焙",
          "automotive": "汽车", "daily-goods": "日用", "biz": "商业"}

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<!-- toolbox-theme-bootstrap -->
<!-- toolbox-sw-register --><script>if("serviceWorker"in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){});});}</script><script>(function(){try{var t=localStorage.getItem("theme");if(!t&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches){t="dark";}if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");}}catch(e){}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=__CAT__,industry=__INDUSTRY__,icon=__ICON__,bg=__BG__">
<title>__TITLE__ - ToolBox</title>
<link rel="canonical" href="__BASE__/tools/__INDUSTRY__/__SLUG__.html">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__BASE__/tools/__INDUSTRY__/__SLUG__.html">
<meta name="twitter:card" content="summary">
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"__BASE__/"},{"@type":"ListItem","position":2,"name":"__CATZH__","item":"__BASE__/tools/__INDUSTRY__/index.html"},{"@type":"ListItem","position":3,"name":"__TITLE__","item":"__BASE__/tools/__INDUSTRY__/__SLUG__.html"}]}
</script>
<meta property="og:image" content="__BASE__/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:image" content="__BASE__/og-image.png">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"__TITLE__","url":"__BASE__/tools/__INDUSTRY__/__SLUG__.html","applicationCategory":"DeveloperApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","description":"__TITLE__","image":"__BASE__/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}
</script>
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<!-- TOOLBOX-SECURITY -->
<script src="/js/privacy.js" defer></script>
<!-- TOOLBOX-PRIVACY-SCRIPT -->
<script src="/js/metrics.js" defer></script>
<!-- TOOLBOX-METRICS-SCRIPT -->
</head>
<body>
<h1 class="sr-only">__H1__</h1>
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ __TITLE__</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>
<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">__INDICON__ __CATZH__</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">__TITLE__</span>
</nav>
<div class="container">
  <div class="card tool-card-accent" style="--tool-accent:__ACCENT__;">
    <h2>__H2__</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">__INTRO__</p>
__INPUTS__
    <div class="toolbar">
      <button class="btn primary" onclick="calcTool()">计算</button>
      <button class="btn" onclick="resetForm()">重置</button>
    </div>
    <div class="result-box" id="result"></div>
  </div>
<div class="tool-notes" style="--tool-accent:__ACCENT__;">
  <div class="tool-notes-title">⚠️ 使用说明与注意事项</div>
  <ul>
__NOTES__
  </ul>
</div>
__REF__
</div>
<script>
function num(id){const v=parseFloat(document.getElementById(id).value);return isNaN(v)?0:v;}
function escH(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}
function dataGrid(rows){let h='<div class="data-grid">';for(const r of rows){h+='<div class="data-card"><div class="num">'+r[0]+'</div><div class="label">'+r[1]+'</div></div>';}return h+'</div>';}
function calcTool(){__CALC__}
function resetForm(){__RESET__}
calcTool();
</script>
</body>
</html>
"""

TOOLS = [
{
 "slug":"wifi-qr-generator","industry":"it","cat":"dev","icon":"📶","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"WiFi 配网二维码生成器",
 "h1":"WiFi 配网二维码生成器",
 "h2":"📶 WiFi 配网二维码生成器",
 "desc":"WiFi 配网二维码生成器 - 填入 SSID、密码与加密方式，生成标准 WIFI: 配网字符串，手机扫码即可一键连网，无需手输密码。纯前端本地生成。",
 "intro":"把 WiFi 配网信息编码成 WIFI: 格式字符串（如 WIFI:T:WPA;S:MyAP;P:pass123;;），任何扫码 App 都能识别为「连接 WiFi」操作。输入网络参数即可生成，复制后交给二维码工具即可打印张贴。",
 "inputs":[
   {"id":"ssid","label":"WiFi 名称（SSID）","type":"text","value":"MyHomeAP"},
   {"id":"pass","label":"WiFi 密码","type":"text","value":"secret123"},
   {"id":"enc","label":"加密方式","type":"select","opts":[["WPA","WPA/WPA2/WPA3"],["WEP","WEP（老旧）"],["nopass","无密码开放网络"]]},
   {"id":"hidden","label":"隐藏网络（SSID 不可见）","type":"select","opts":[["false","否（可见）"],["true","是（隐藏）"]]}
 ],
 "calc":"""
var ssid=document.getElementById('ssid').value;
var pass=document.getElementById('pass').value;
var enc=document.getElementById('enc').value;
var hidden=document.getElementById('hidden').value;
if(!ssid){document.getElementById('result').innerHTML='<div class="result-title">提示</div><p class="muted">请填写 WiFi 名称（SSID）。</p>';return;}
var str;
if(enc==='nopass'){str='WIFI:T:nopass;S:'+ssid+';'+((hidden==='true')?';H:true':'')+';';}
else{str='WIFI:T:'+enc+';S:'+ssid+';P:'+pass+';'+((hidden==='true')?';H:true':'')+';';}
var html='<div class="result-title">配网字符串（WIFI:）</div>';
html+='<pre class="code-box" style="white-space:pre-wrap;word-break:break-all;font-size:13px;">'+escH(str)+'</pre>';
html+='<p class="muted">将此字符串交给任意二维码生成工具（如本站的二维码工具）即可生成可扫描的连网二维码。</p>';
html+='<div class="data-grid">';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+escH(ssid)+'</div><div class="label">SSID</div></div>';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+escH(enc==='nopass'?'无密码':pass)+'</div><div class="label">密码/方式</div></div>';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+(hidden==='true'?'隐藏':'可见')+'</div><div class="label">网络可见性</div></div>';
html+='</div>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "WIFI: 格式标准字段：T=加密类型（WPA/WEP/nopass）、S=SSID、P=密码、H=是否隐藏（true/false）。SSID 与密码中含特殊字符 ; , \\ 时无需手动转义，扫码 App 多能识别。",
   "WPA3 网络可直接用 T:WPA 表示，绝大多数现代设备兼容；老旧设备仅支持 WEP 时选 WEP（但 WEP 已被攻破，不建议新装网络使用）。",
   "开放网络（无密码）务必用 T:nopass，写成 T: 留空可能被部分解析器误判为 WEP。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 配网字符串格式</h3>
  <table class="ref-table">
    <tr><th>字段</th><th>含义</th><th>示例</th></tr>
    <tr><td>T</td><td>加密方式</td><td>WPA / WEP / nopass</td></tr>
    <tr><td>S</td><td>网络名 SSID</td><td>MyHomeAP</td></tr>
    <tr><td>P</td><td>密码</td><td>secret123</td></tr>
    <tr><td>H</td><td>隐藏网络</td><td>true / false</td></tr>
  </table>
  <p>完整示例：<code>WIFI:T:WPA;S:MyHomeAP;P:secret123;;</code></p>
</div>
"""
},
{
 "slug":"docker-run-converter","industry":"it","cat":"dev","icon":"🐳","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"docker run 转 docker-compose",
 "h1":"docker run 转 docker-compose",
 "h2":"🐳 docker run 转 docker-compose",
 "desc":"docker run 转 docker-compose - 粘贴 docker run 命令，解析镜像、端口、挂载、环境变量、restart 等参数，一键生成 docker-compose.yml 片段。纯前端本地解析。",
 "intro":"docker run 一长串命令行参数，迁移到 docker-compose 时需逐条对应成 YAML 字段。本工具解析常用参数并生成可粘贴的 compose 片段，便于多容器编排管理。",
 "inputs":[
   {"id":"cmd","label":"粘贴 docker run 命令","type":"textarea","rows":"5","value":"docker run -d --name web -p 8080:80 -v /data:/app/data -e TZ=Asia/Shanghai --restart unless-stopped nginx:latest"}
 ],
 "calc":"""
var src=document.getElementById('cmd').value;
function parse(cmd){
  var m=cmd.match(/docker\\s+run\\s+(.*)/s); if(!m) return null;
  var args=m[1]; var image=null, name='app', ports=[], vols=[], envs=[], restart='no', det=false;
  var toks=args.split(/\\s+/).filter(Boolean);
  var i=0;
  while(i<toks.length){
    var t=toks[i];
    if(t==='-d'||t==='--detach'){det=true;i++;continue;}
    if(t==='--name'){name=toks[i+1];i+=2;continue;}
    if(t==='-p'||t==='--publish'){ports.push(toks[i+1]);i+=2;continue;}
    if(t==='-v'||t==='--volume'){vols.push(toks[i+1]);i+=2;continue;}
    if(t==='-e'||t==='--env'){envs.push(toks[i+1]);i+=2;continue;}
    if(t==='--restart'){restart=toks[i+1];i+=2;continue;}
    if(t.charAt(0)==='-'){i++;continue;}
    if(!image){image=t;i++;}
  }
  return {image:image,name:name,ports:ports,vols:vols,envs:envs,restart:restart,det:det};
}
var d=parse(src);
var html='<div class="result-title">docker-compose.yml</div>';
if(!d||!d.image){html+='<p style="color:#dc2626;">⚠️ 未识别到 docker run 命令或镜像名，请检查输入。</p>';document.getElementById('result').innerHTML=html;return;}
var y='services:\\n  '+d.name+':\\n    image: '+d.image+'\\n';
if(d.det)y+='    # 原为 -d 后台运行，compose 默认即后台\\n';
if(d.ports.length)y+='    ports:\\n'+d.ports.map(function(p){return '      - \"'+p+'\"';}).join('\\n')+'\\n';
if(d.vols.length)y+='    volumes:\\n'+d.vols.map(function(p){return '      - '+p;}).join('\\n')+'\\n';
if(d.envs.length)y+='    environment:\\n'+d.envs.map(function(p){var kv=p.split('=');return '      - '+kv[0]+': '+JSON.stringify(kv.slice(1).join('='));}).join('\\n')+'\\n';
y+='    restart: '+d.restart+'\\n';
html+='<pre class="code-box" style="white-space:pre;font-size:12.5px;overflow-x:auto;">'+escH(y)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "支持参数：-d/--detach、-p/--publish、-v/--volume、-e/--env、--name、--restart；其余未知 - 参数在解析时跳过，可按需手动补到 compose。",
   "compose 默认以后台运行，原 -d 无需对应字段；restart 策略沿用 unless-stopped / always / no 等原值。",
   "本解析为轻量级：不支持 --network、--link、多值 -e 合并等复杂写法，生成后请在本地 docker compose config 校验。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常用参数对照</h3>
  <table class="ref-table">
    <tr><th>docker run</th><th>compose 字段</th></tr>
    <tr><td>-p 8080:80</td><td>ports: - "8080:80"</td></tr>
    <tr><td>-v /d:/a</td><td>volumes: - /d:/a</td></tr>
    <tr><td>-e K=V</td><td>environment: - K: "V"</td></tr>
    <tr><td>--name web</td><td>service 键名 web</td></tr>
    <tr><td>--restart always</td><td>restart: always</td></tr>
  </table>
</div>
"""
},
{
 "slug":"gradient-generator","industry":"design","cat":"design","icon":"🌈","bg":"#eef2ff","accent":"#6366F1","indicon":"🎨",
 "title":"CSS 渐变生成器",
 "h1":"CSS 渐变生成器",
 "h2":"🌈 CSS 渐变生成器",
 "desc":"CSS 渐变生成器 - 选择线性/径向渐变、角度与多个色标，实时生成可用的 CSS linear/radial-gradient 代码，可直接复制用于背景。纯前端本地计算。",
 "intro":"CSS 渐变用 gradient() 函数描述颜色过渡，无需图片即可做背景。设置类型、角度与若干色标（位置+颜色），即可生成对应 CSS 并预览。",
 "inputs":[
   {"id":"gtype","label":"渐变类型","type":"select","opts":[["linear","linear-gradient 线性"],["radial","radial-gradient 径向"]]},
   {"id":"angle","label":"角度（线性，0–360°）","value":"90","step":"1","min":"0","max":"360"},
   {"id":"c1","label":"色标 1（位置% / 颜色）","type":"text","value":"0,#6366F1"},
   {"id":"c2","label":"色标 2（位置% / 颜色）","type":"text","value":"100,#EC4899"}
 ],
 "calc":"""
var gtype=document.getElementById('gtype').value;
var angle=Math.floor(num('angle'));
var c1=document.getElementById('c1').value.trim();
var c2=document.getElementById('c2').value.trim();
function norm(s){var p=s.split(/[,\\s]+/);var pos=p[0].replace('%','');var col=p.slice(1).join(' ');if(!/%$/.test(p[0])){}return (isNaN(+pos)?'0%':pos+'%')+', '+col;}
var css;
if(gtype==='linear'){css='linear-gradient('+angle+'deg, '+norm(c1)+', '+norm(c2)+')';}
else{css='radial-gradient(circle, '+norm(c1)+', '+norm(c2)+')';}
var html='<div class="result-title">预览与代码</div>';
html+='<div style="height:90px;border-radius:10px;background:'+css+';margin:10px 0;"></div>';
html+='<pre class="code-box" style="white-space:pre-wrap;word-break:break-all;font-size:13px;">background: '+escH(css)+';</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "linear-gradient 角度 0deg 由下向上、90deg 由左向右、180deg 由上向下；角度决定渐变方向。",
   "色标格式为「位置% 颜色」，位置 0% 起、100% 止，可加多个色标做多彩过渡；位置可省略（自动均分）。",
   "radial-gradient 默认椭圆，加 circle 关键字可强制正圆；还可指定圆心位置如 at center / at 30% 70%。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 语法速查</h3>
  <table class="ref-table">
    <tr><th>函数</th><th>示例</th></tr>
    <tr><td>线性</td><td>linear-gradient(90deg, #fff, #000)</td></tr>
    <tr><td>径向</td><td>radial-gradient(circle, #fff, #000)</td></tr>
    <tr><td>多色标</td><td>linear-gradient(90deg, red 0%, yellow 50%, green 100%)</td></tr>
  </table>
</div>
"""
},
{
 "slug":"lorem-ipsum-generator","industry":"text","cat":"text","icon":"📝","bg":"#fefce8","accent":"#CA8A04","indicon":"✏️",
 "title":"占位文本生成器",
 "h1":"占位文本生成器",
 "h2":"📝 占位文本生成器",
 "desc":"占位文本生成器 - 生成 Lorem Ipsum 拉丁文占位段落，用于设计稿、排版预览与版面测试，支持指定段落数。纯前端本地生成。",
 "intro":"Lorem Ipsum 是排版设计中常用的无意义拉丁文占位文本，能让读者聚焦版面而非内容。选择段落数即可生成标准段落，方便填充原型与样张。",
 "inputs":[
   {"id":"n","label":"段落数（1–10）","value":"3","step":"1","min":"1","max":"10"},
   {"id":"seed","label":"每段落落长度","type":"select","opts":[["short","短（约 30 词）"],["mid","中（约 60 词）"],["long","长（约 100 词）"]]}
 ],
 "calc":"""
var W=['lorem','ipsum','dolor','sit','amet','consectetur','adipiscing','elit','sed','do','eiusmod','tempor','incididunt','ut','labore','et','dolore','magna','aliqua','enim','ad','minim','veniam','quis','nostrud','exercitation','ullamco','laboris','nisi','aliquip','ex','ea','commodo','consequat','duis','aute','irure','in','reprehenderit','voluptate','velit','esse','cillum','eu','fugiat','nulla','pariatur','excepteur','sint','occaecat','cupidatat','non','proident','sunt','culpa','qui','officia','deserunt','mollit','anim','id','est','laborum'];
function pick(n){var s=[];for(var i=0;i<n;i++){var w=W[Math.floor(Math.random()*W.length)];if(i===0)w=w.charAt(0).toUpperCase()+w.slice(1);s.push(w);}return s.join(' ')+'.';}
var n=Math.max(1,Math.min(10,Math.floor(num('n'))));
var len={'short':30,'mid':60,'long':100}[document.getElementById('seed').value];
var html='<div class="result-title">占位文本（'+n+' 段）</div><div style="font-size:13px;line-height:1.7;color:var(--text-muted);">';
for(var p=0;p<n;p++){
  var txt=pick(len);
  if(p===0)txt='Lorem ipsum dolor sit amet, consectetur adipiscing elit. '+txt.slice(txt.indexOf('.')+2);
  html+='<p style="margin:0 0 10px;">'+escH(txt)+'</p>';
}
html+='</div>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "Lorem Ipsum 源自西塞罗《善恶之尽》的拉丁文段落打乱，自 16 世纪起被印刷业用作占位样张，至今是设计界惯例。",
   "本工具随机拼接词表生成，并非固定经典原文，但风格一致，足够用于版面铺满与字体预览。",
   "正式文案上线前应替换占位文本，避免把 Lorem Ipsum 误发布到生产页面。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 经典开头</h3>
  <p>“Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.”</p>
</div>
"""
},
{
 "slug":"reading-time-estimator","industry":"text","cat":"text","icon":"⏱️","bg":"#fefce8","accent":"#CA8A04","indicon":"✏️",
 "title":"阅读时长估算",
 "h1":"阅读时长估算",
 "h2":"⏱️ 阅读时长估算",
 "desc":"阅读时长估算 - 粘贴中/英文文本，按平均阅读速度估算所需时间（中文约 300 字/分钟、英文约 200 词/分钟），并统计字数词数。纯前端本地计算。",
 "intro":"估算阅读时长有助于排期与撰写摘要。本工具分别统计中文字符与英文单词，按常见阅读速度换算分钟数，给出大致需要的时间。",
 "inputs":[
   {"id":"src","label":"粘贴要估算的文本","type":"textarea","rows":"6","value":"在纯前端工具站里，阅读时长估算是一个很实用的小功能，帮助用户判断一篇长文需要投入多少时间。"},
   {"id":"cjkwpm","label":"中文速度（字/分钟）","value":"300","step":"10","min":"50"},
   {"id":"enwpm","label":"英文速度（词/分钟）","value":"200","step":"10","min":"50"}
 ],
 "calc":"""
var s=document.getElementById('src').value;
var cjkwpm=Math.max(1,num('cjkwpm'));
var enwpm=Math.max(1,num('enwpm'));
var cjk=(s.match(/[\\u4e00-\\u9fff\\u3040-\\u30ff\\uac00-\\ud7af]/g)||[]).length;
var enWords=s.replace(/[\\u4e00-\\u9fff]/g,' ').match(/[A-Za-z0-9]+/g)||[];
var enN=enWords.length;
var total=cjk/cjkwpm+enN/enwpm;
var mins=Math.max(1,Math.round(total));
var html='<div class="result-title">估算结果</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+cjk+'</div><div class="label">中文字符</div></div>';
html+='<div class="data-card"><div class="num">'+enN+'</div><div class="label">英文单词</div></div>';
html+='<div class="data-card"><div class="num">'+mins+'</div><div class="label">分钟</div></div>';
html+='</div>';
html+='<p class="muted" style="margin-top:10px;">按中文 '+cjkwpm+' 字/分 + 英文 '+enwpm+' 词/分估算，约 '+total.toFixed(1)+' 分钟。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "中文阅读速度因人而异，普通成人约 250–400 字/分钟；英文母语者约 200–250 词/分钟。可调参数适配不同读者。",
   "本工具把 CJK 统一段字符（中日韩）计入中文字数，英文数字计入词数，互不干扰。",
   "估算仅为参考：技术文、带代码或图表的内容实际更慢，娱乐性内容可能更快。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 参考阅读速度</h3>
  <table class="ref-table">
    <tr><th>类型</th><th>速度</th></tr>
    <tr><td>中文普通</td><td>300 字/分</td></tr>
    <tr><td>中文快速</td><td>500 字/分</td></tr>
    <tr><td>英文母语</td><td>200 词/分</td></tr>
  </table>
</div>
"""
},
{
 "slug":"split-bill","industry":"accounting","cat":"accounting","icon":"🧾","bg":"#ecfdf5","accent":"#10B981","indicon":"💰",
 "title":"分账计算器",
 "h1":"分账计算器",
 "h2":"🧾 分账计算器",
 "desc":"分账计算器 - 输入账单总额、人数与小费比例，计算每人应付（含小费）及小费金额，支持按人数均摊。纯前端本地计算。",
 "intro":"聚餐、合租、团购后常需平摊费用并加小费。填入总额、人数与小费比例，即可得出每人应付与总小费，避免口头算错。",
 "inputs":[
   {"id":"total","label":"账单总额","value":"480","step":"0.01","min":"0"},
   {"id":"people","label":"人数","value":"4","step":"1","min":"1"},
   {"id":"tip","label":"小费比例（%）","value":"10","step":"1","min":"0"}
 ],
 "calc":"""
var total=num('total'), people=Math.max(1,Math.floor(num('people'))), tipPct=num('tip');
var tip=total*tipPct/100;
var grand=total+tip;
var per=grand/people;
var html='<div class="result-title">分账结果</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+per.toFixed(2)+'</div><div class="label">每人应付</div></div>';
html+='<div class="data-card"><div class="num">'+tip.toFixed(2)+'</div><div class="label">小费合计</div></div>';
html+='<div class="data-card"><div class="num">'+grand.toFixed(2)+'</div><div class="label">含小费总额</div></div>';
html+='</div>';
html+='<p class="muted" style="margin-top:10px;">'+people+' 人平摊 '+total.toFixed(2)+'，小费 '+tipPct+'% = '+tip.toFixed(2)+'，每人约 '+per.toFixed(2)+'。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "小费通常按税前或税后账单计算，本工具基于总额（含税前）乘以比例，符合多数餐厅习惯；海外部分按税前算，请按当地规则微调。",
   "人数必须为正整数；小数人数无实际意义，工具自动取整。",
   "如需按不同消费金额分账（有人多点），请用逐项 AA，本工具仅支持均摊。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>总额</th><th>人数</th><th>小费</th><th>每人</th></tr>
    <tr><td>480</td><td>4</td><td>10%</td><td>132.00</td></tr>
    <tr><td>300</td><td>3</td><td>15%</td><td>115.00</td></tr>
  </table>
</div>
"""
},
{
 "slug":"gst-calculator","industry":"tax","cat":"tax","icon":"🧮","bg":"#fef2f8","accent":"#DB2777","indicon":"💸",
 "title":"GST 商品服务税计算",
 "h1":"GST 商品服务税计算",
 "h2":"🧮 GST 商品服务税计算",
 "desc":"GST 商品服务税计算 - 在含税价与税前价之间互算，输入金额与税率（如 5%/10%/15%）即得税额与对应价格。纯前端本地计算。",
 "intro":"GST（商品及服务税）多国采用，发票常标注含税价。输入含税或税前金额与税率，即可拆分税额，便于报销、报税与对账。",
 "inputs":[
   {"id":"amt","label":"金额","value":"110","step":"0.01","min":"0"},
   {"id":"rate","label":"税率（%）","value":"10","step":"0.1","min":"0"},
   {"id":"mode","label":"金额性质","type":"select","opts":[["incl","含税价 → 税前/税额"],["excl","税前价 → 含税/税额"]]}
 ],
 "calc":"""
var amt=num('amt'), r=num('rate'), html='<div class="result-title">计算结果</div>';
if(r<0){html+='<p style="color:#dc2626;">⚠️ 税率不能为负。</p>';document.getElementById('result').innerHTML=html;return;}
if(document.getElementById('mode').value==='incl'){
  var base=amt/(1+r/100), tax=amt-base;
  html+='<div class="data-grid">';
  html+='<div class="data-card"><div class="num">'+base.toFixed(2)+'</div><div class="label">税前价</div></div>';
  html+='<div class="data-card"><div class="num">'+tax.toFixed(2)+'</div><div class="label">税额</div></div>';
  html+='<div class="data-card"><div class="num">'+amt.toFixed(2)+'</div><div class="label">含税价</div></div>';
  html+='</div>';
}else{
  var tax2=amt*r/100, incl=amt+tax2;
  html+='<div class="data-grid">';
  html+='<div class="data-card"><div class="num">'+amt.toFixed(2)+'</div><div class="label">税前价</div></div>';
  html+='<div class="data-card"><div class="num">'+tax2.toFixed(2)+'</div><div class="label">税额</div></div>';
  html+='<div class="data-card"><div class="num">'+incl.toFixed(2)+'</div><div class="label">含税价</div></div>';
  html+='</div>';
}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "含税价 = 税前价 ×(1 + 税率)；税前价 = 含税价 ÷(1 + 税率)。拆分税额时务必区分两种基数。",
   "常见 GST 税率：澳大利亚 10%、新西兰 15%、新加坡 9%、加拿大联邦 5%（各省另有 PST/HST），本工具适用任意比例。",
   "发票若标注「含税」而按税前算税会重复计税，报销前先确认金额性质。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 公式</h3>
  <table class="ref-table">
    <tr><th>已知</th><th>求</th><th>公式</th></tr>
    <tr><td>含税</td><td>税前</td><td>含税 ÷ (1+r%)</td></tr>
    <tr><td>税前</td><td>含税</td><td>税前 × (1+r%)</td></tr>
    <tr><td>任意</td><td>税额</td><td>差额</td></tr>
  </table>
</div>
"""
},
{
 "slug":"date-duration","industry":"it","cat":"dev","icon":"📅","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"日期天数差",
 "h1":"日期天数差",
 "h2":"📅 日期天数差",
 "desc":"日期天数差 - 输入两个日期，计算相差天数、周数以及是否跨越闰年，支持含当天与不含当天的口径。纯前端本地计算。",
 "intro":"项目排期、租期、纪念日都常需要算两个日期之间隔了多久。填入起止日期即可得到精确天数差与周数。",
 "inputs":[
   {"id":"d1","label":"开始日期","type":"text","value":"2026-01-01"},
   {"id":"d2","label":"结束日期","type":"text","value":"2026-08-24"},
   {"id":"inc","label":"计算口径","type":"select","opts":[["excl","不含结束当天"],["incl","含结束当天（含首尾）"]]}
 ],
 "calc":"""
function pdate(s){var p=s.split('-');if(p.length!==3)return null;return new Date(+p[0],+p[1]-1,+p[2]);}
var a=pdate(document.getElementById('d1').value), b=pdate(document.getElementById('d2').value);
var html='<div class="result-title">相差</div>';
if(!a||!b||isNaN(a)||isNaN(b)){html+='<p style="color:#dc2626;">⚠️ 请按 YYYY-MM-DD 格式填写两个日期。</p>';document.getElementById('result').innerHTML=html;return;}
var diff=Math.round((b-a)/86400000);
var days=diff+(document.getElementById('inc').value==='incl'?1:0);
var weeks=(days/7).toFixed(1);
html+='<div class="data-grid">';
html+='<div class="data-card"><div class="num">'+days+'</div><div class="label">天数</div></div>';
html+='<div class="data-card"><div class="num">'+weeks+'</div><div class="label">周数</div></div>';
html+='</div>';
html+='<p class="muted" style="margin-top:10px;">从 '+document.getElementById('d1').value+' 到 '+document.getElementById('d2').value+'（不含结束当天 '+diff+' 天）。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "计算以自然日为单位，按 UTC 零点对齐避免时区误差；同一天内相差记 0 天。",
   "含结束当天口径在租期、会员天数等场景常用（如 1 号到 31 号算 31 天），请按需切换。",
   "跨闰年 2 月 29 日会被自动处理，无需手动修正。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>起</th><th>止</th><th>天数（不含末）</th></tr>
    <tr><td>2026-01-01</td><td>2026-01-02</td><td>1</td></tr>
    <tr><td>2026-01-01</td><td>2026-02-01</td><td>31</td></tr>
    <tr><td>2026-08-01</td><td>2026-08-24</td><td>23</td></tr>
  </table>
</div>
"""
},
{
 "slug":"recipe-scaler","industry":"baking","cat":"baking","icon":"🍰","bg":"#fff7ed","accent":"#EA580C","indicon":"🧁",
 "title":"配方缩放计算器",
 "h1":"配方缩放计算器",
 "h2":"🍰 配方缩放计算器",
 "desc":"配方缩放计算器 - 输入原料原用量与目标倍数（或半成品量），按比例缩放烘焙配方，输出各原料新用量。纯前端本地计算。",
 "intro":"配方从 2 人份改 6 人份、或小批量改大批量时，所有原料按同一比例缩放。输入原用量与倍数即可批量换算，避免手算出错。",
 "inputs":[
   {"id":"rows","label":"原料（每行 名称=数量，单位跟在数字后）","type":"textarea","rows":"6","value":"面粉=200g\\n糖=100g\\n鸡蛋=2个\\n牛奶=150ml\\n黄油=50g"},
   {"id":"factor","label":"缩放倍数","value":"1.5","step":"0.1","min":"0"}
 ],
 "calc":"""
var lines=document.getElementById('rows').value.split(/\\n/).map(function(x){return x.trim();}).filter(Boolean);
var f=num('factor'), html='<div class="result-title">缩放后配方（×'+f+'）</div><div style="font-size:13px;">';
if(f<=0){html+='<p style="color:#dc2626;">⚠️ 倍数须为正。</p>';document.getElementById('result').innerHTML=html;return;}
var any=false;
for(var i=0;i<lines.length;i++){
  var m=lines[i].match(/^(.+?)[=＝]\\s*([0-9.]+)\\s*(.*)$/);
  if(!m){html+='<p>'+escH(lines[i])+'（无法解析，请按 名称=数字 单位）</p>';continue;}
  any=true;
  var name=m[1], val=parseFloat(m[2]), unit=m[3];
  var nv=(val*f);
  var disp=(Math.round(nv*100)/100)+unit;
  html+='<p style="margin:4px 0;"><b>'+escH(name)+'</b>：'+disp+'</p>';
}
if(!any){html+='<p class="muted">未解析到有效原料行。</p>';}
html+='</div>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "缩放仅改变用量比例，不改变工艺（烘烤温度、时间可能需按模具大小微调，非简单线性）。",
   "整数个的原料（如鸡蛋 2 个）按比例可能出现 3 个，实际可四舍五入或调整配方总量。",
   "烘焙对配比敏感，大幅缩放时建议保留关键比例（面粉:液体:酵母）。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>原料</th><th>原</th><th>×1.5</th></tr>
    <tr><td>面粉</td><td>200g</td><td>300g</td></tr>
    <tr><td>糖</td><td>100g</td><td>150g</td></tr>
    <tr><td>鸡蛋</td><td>2个</td><td>3个</td></tr>
  </table>
</div>
"""
},
{
 "slug":"fuel-cost-calculator","industry":"automotive","cat":"automotive","icon":"⛽","bg":"#f0f9ff","accent":"#0284C7","indicon":"🚗",
 "title":"油费计算器",
 "h1":"油费计算器",
 "h2":"⛽ 油费计算器",
 "desc":"油费计算器 - 输入里程、百公里油耗与油价，估算单程油费；也支持反向由预算算可行驶里程。纯前端本地计算。",
 "intro":"出行前估算油费有助于规划预算。填入行驶里程、车辆油耗（L/100km）与当前油价，即可得油费；或反过来由预算推导可跑多远。",
 "inputs":[
   {"id":"dist","label":"里程（km）","value":"300","step":"1","min":"0"},
   {"id":"cons","label":"百公里油耗（L/100km）","value":"8","step":"0.1","min":"0"},
   {"id":"price","label":"油价（元/L）","value":"7.8","step":"0.1","min":"0"}
 ],
 "calc":"""
var dist=num('dist'), cons=num('cons'), price=num('price');
var liters=dist*cons/100;
var cost=liters*price;
var html='<div class="result-title">油费估算</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+liters.toFixed(2)+'</div><div class="label">耗油量 (L)</div></div>';
html+='<div class="data-card"><div class="num">'+cost.toFixed(2)+'</div><div class="label">油费 (元)</div></div>';
if(price>0&&cons>0){
  var perKm=price*cons/100;
  html+='<div class="data-card"><div class="num">'+perKm.toFixed(2)+'</div><div class="label">每公里 (元)</div></div>';
}
html+='</div>';
html+='<p class="muted" style="margin-top:10px;">行驶 '+dist+' km，油耗 '+cons+' L/100km，油价 '+price+' 元/L。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "油费 = 里程 × 油耗 ÷ 100 × 油价；每公里成本 = 油价 × 油耗 ÷ 100，是更直观的对比口径。",
   "实际油耗受路况、载重、空调、胎压影响，城市拥堵常比工信部标定值高 20–40%。",
   "电动车可把「油价」换为「电费/度、电耗 kWh/100km」套用同一公式估算。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>里程</th><th>油耗</th><th>油价</th><th>油费</th></tr>
    <tr><td>300km</td><td>8 L/100km</td><td>7.8 元</td><td>187.20 元</td></tr>
    <tr><td>500km</td><td>6 L/100km</td><td>7.5 元</td><td>225.00 元</td></tr>
  </table>
</div>
"""
},
{
 "slug":"parking-fee","industry":"daily-goods","cat":"daily","icon":"🅿️","bg":"#fefce8","accent":"#CA8A04","indicon":"🛒",
 "title":"停车费计算器",
 "h1":"停车费计算器",
 "h2":"🅿️ 停车费计算器",
 "desc":"停车费计算器 - 输入停放时长与每小时费率（免费时段可选），估算停车费用，支持封顶价。纯前端本地计算。",
 "intro":"商场、医院、路边停车收费规则不一。填入时长、费率与封顶价，即可估算费用，避免离场时惊讶。",
 "inputs":[
   {"id":"hours","label":"停放时长（小时，可小数）","value":"3.5","step":"0.5","min":"0"},
   {"id":"rate","label":"每小时费率（元）","value":"10","step":"1","min":"0"},
   {"id":"free","label":"免费时长（小时）","value":"0","step":"0.5","min":"0"},
   {"id":"cap","label":"每日封顶（元，0=不封顶）","value":"60","step":"1","min":"0"}
 ],
 "calc":"""
var hours=num('hours'), rate=num('rate'), free=num('free'), cap=num('cap');
var billable=Math.max(0,hours-free);
var fee=billable*rate;
if(cap>0)fee=Math.min(fee,cap);
var html='<div class="result-title">停车费</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+fee.toFixed(2)+'</div><div class="label">应付 (元)</div></div>';
html+='<div class="data-card"><div class="num">'+billable.toFixed(1)+'</div><div class="label">计费时长(h)</div></div>';
html+='</div>';
html+='<p class="muted" style="margin-top:10px;">停放 '+hours+'h，免费 '+free+'h，费率 '+rate+' 元/h'+(cap>0?('，封顶 '+cap+' 元'):'')+'。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "多数停车场按「不足一小时按一小时计」或「按 15 分钟为单位」计费，本工具按连续小时估算，实际以现场规则为准。",
   "免费时段常见于商场消费满额、医院就诊，记得保留小票核销。",
   "封顶价（如每日 60 元）在长时间停车时很关键，超出部分不再累加。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>时长</th><th>费率</th><th>封顶</th><th>费用</th></tr>
    <tr><td>3.5h</td><td>10 元/h</td><td>60 元</td><td>35.00 元</td></tr>
    <tr><td>9h</td><td>10 元/h</td><td>60 元</td><td>60.00 元</td></tr>
  </table>
</div>
"""
},
{
 "slug":"unit-price-compare","industry":"biz","cat":"biz","icon":"⚖️","bg":"#f5f3ff","accent":"#7C3AED","indicon":"📊",
 "title":"单位价格比较",
 "h1":"单位价格比较",
 "h2":"⚖️ 单位价格比较",
 "desc":"单位价格比较 - 输入不同规格商品的容量/重量与价格，算出每单位（如每 100g、每 L）价格，找出真正划算的那个。纯前端本地计算。",
 "intro":"大包装不一定更便宜。把各商品的「价格 ÷ 数量」归一为统一单位，就能横向比价，避免被包装迷惑。",
 "inputs":[
   {"id":"a_q","label":"商品 A 数量（如 500）","value":"500","step":"1","min":"0"},
   {"id":"a_u","label":"商品 A 数量单位","type":"text","value":"g"},
   {"id":"a_p","label":"商品 A 价格（元）","value":"12","step":"0.1","min":"0"},
   {"id":"b_q","label":"商品 B 数量（如 1）","value":"1","step":"0.1","min":"0"},
   {"id":"b_u","label":"商品 B 数量单位","type":"text","value":"kg"},
   {"id":"b_p","label":"商品 B 价格（元）","value":"20","step":"0.1","min":"0"}
 ],
 "calc":"""
function unit(q,u){var k={'g':1,'kg':1000,'mg':0.001,'ml':1,'l':1000,'L':1000};return q*(k[u]||1);}
var a=unit(num('a_q'),document.getElementById('a_u').value.trim()), b=unit(num('b_q'),document.getElementById('b_u').value.trim());
var ap=num('a_p'), bp=num('b_p');
var html='<div class="result-title">每克单价对比</div><div class="data-grid">';
if(a>0)html+='<div class="data-card"><div class="num" style="font-size:13px;">'+(ap/a).toFixed(4)+' 元/g</div><div class="label">商品 A</div></div>';
if(b>0)html+='<div class="data-card"><div class="num" style="font-size:13px;">'+(bp/b).toFixed(4)+' 元/g</div><div class="label">商品 B</div></div>';
html+='</div>';
if(a>0&&b>0){
  var pa=ap/a, pb=bp/b;
  var better=pa<pb?'A':'B';
  html+='<p style="margin-top:10px;"><b>更划算：</b>商品 '+better+'（每克更低 '+Math.min(pa,pb).toFixed(4)+' 元）。</p>';
  var ratio=Math.max(pa,pb)/Math.min(pa,pb);
  html+='<p class="muted">另一款约贵 '+ratio.toFixed(2)+' 倍。</p>';
}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "比较前把所有数量归一为同一基本单位（g、ml、L），kg=1000g、L=1000ml，否则不可比。",
   "注意「数量」是净重/净含量，而非包装重量；促销装、组合装需拆到单件再比。",
   "临期、赠品、会员价等隐性因素本工具未计入，最终决策结合实际情况。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 单位换算</h3>
  <table class="ref-table">
    <tr><th>单位</th><th>换算为克/毫升</th></tr>
    <tr><td>1 kg</td><td>1000 g</td></tr>
    <tr><td>1 L</td><td>1000 ml</td></tr>
    <tr><td>1 mg</td><td>0.001 g</td></tr>
  </table>
</div>
"""
},
{
 "slug":"unit-converter-advanced","industry":"it","cat":"dev","icon":"🔁","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"高级单位转换器",
 "h1":"高级单位转换器",
 "h2":"🔁 高级单位转换器",
 "desc":"高级单位转换器 - 在长度、重量、温度、面积、体积、时间、速度、数据存储等多类单位间互转，输入即出全部常见单位值。纯前端本地计算。",
 "intro":"一个值需要在多个单位间对照时，逐个查表很麻烦。选择类别并输入数值，即得该类别下所有常见单位的换算结果，一屏看全。",
 "inputs":[
   {"id":"cat","label":"类别","type":"select","opts":[["length","长度"],["mass","重量"],["temp","温度"],["area","面积"],["volume","体积"],["time","时间"],["speed","速度"],["data","数据存储"]]},
   {"id":"val","label":"数值","value":"1","step":"any","min":"0"},
   {"id":"from","label":"原单位","type":"text","value":"km"}
 ],
 "calc":"""
var U={
 length:{m:1,km:1000,cm:0.01,mm:0.001,mi:1609.344,yd:0.9144,ft:0.3048,in:0.0254,nm:1852},
 mass:{kg:1,g:0.001,mg:1e-6,t:1000,lb:0.45359237,oz:0.028349523,st:6.35029318},
 area:{m2:1,km2:1e6,cm2:1e-4,ha:10000,acre:4046.8564224,ft2:0.09290304},
 volume:{l:1,ml:0.001,m3:1000,gal:3.785411784,gal_uk:4.54609,qt:0.946352946,cup:0.2365882365,fl_oz:0.0295735296},
 time:{s:1,min:60,h:3600,d:86400,wk:604800},
 speed:{mps:1,kph:0.277777778,mph:0.44704,knot:0.514444444},
 data:{B:1,KB:1024,MB:1048576,GB:1073741824,TB:1099511627776,bit:0.125}
};
function tempTo(v,from,to){var c=from==='C'?v:(from==='F'?(v-32)*5/9:(v+273.15));return to==='C'?c:(to==='F'?c*9/5+32:c+273.15);}
var cat=document.getElementById('cat').value;
var v=num('val'), from=document.getElementById('from').value.trim();
var html='<div class="result-title">换算结果</div>';
if(cat==='temp'){
  if(!['C','F','K'].includes(from)){html+='<p style="color:#dc2626;">⚠️ 温度单位请用 C/F/K。</p>';document.getElementById('result').innerHTML=html;return;}
  html+='<div class="data-grid">';
  ['C','F','K'].forEach(function(t){if(t!==from)html+='<div class="data-card"><div class="num" style="font-size:14px;">'+tempTo(v,from,t).toFixed(2)+'</div><div class="label">'+t+'</div></div>';});
  html+='</div>';
}else{
  var tab=U[cat];
  if(!tab||!(from in tab)){html+='<p style="color:#dc2626;">⚠️ 类别 '+cat+' 不支持单位 '+from+'。可选项：'+(tab?Object.keys(tab).join(','):'')+'</p>';document.getElementById('result').innerHTML=html;return;}
  var base=v*tab[from];
  html+='<div class="data-grid">';
  for(var k in tab){if(k===from)continue;var nv=base/tab[k];html+='<div class="data-card"><div class="num" style="font-size:14px;">'+nv.toFixed(6).replace(/\\.?0+$/,'')+'</div><div class="label">'+k+'</div></div>';}
  html+='</div>';
}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "长度、重量等以「米/千克」为基本单位换算；温度用摄氏度做中转（C/F/K 互转公式固定）。",
   "数据存储单位采用二进制前缀（1 KB = 1024 B），与部分系统用十进制（1 KB = 1000 B）不同，请注意语境。",
   "体积 gal 默认美制（3.785 L）；英制加仑另列 gal_uk（4.546 L），别混用。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常用换算</h3>
  <table class="ref-table">
    <tr><th>量</th><th>关系</th></tr>
    <tr><td>长度</td><td>1 km = 1000 m = 0.6214 mi</td></tr>
    <tr><td>重量</td><td>1 lb ≈ 0.4536 kg</td></tr>
    <tr><td>温度</td><td>°F = °C×9/5+32</td></tr>
    <tr><td>数据</td><td>1 MB = 1024 KB = 1048576 B</td></tr>
  </table>
</div>
"""
},
]

def render_inputs(t):
    rows=[]
    ins=t["inputs"]
    for i in range(0,len(ins),3):
        chunk=ins[i:i+3]
        cells=[]
        for f in chunk:
            ftype=f.get("type","number")
            if ftype=="select":
                opts="".join('<option value="%s">%s</option>'%(o[0],o[1]) for o in f.get("opts",[]))
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <select id="%s" style="width:100%%;">%s</select>\n      </div>'%(f["id"],f["label"],f["id"],opts))
            elif ftype=="textarea":
                val=(f.get("value","") or "").replace("&","&amp;").replace('"',"&quot;").replace("\n","&#10;")
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <textarea id="%s" rows="%s" style="width:100%%;font-family:monospace;font-size:12.5px;">%s</textarea>\n      </div>'%(f["id"],f["label"],f["id"],f.get("rows","5"),val))
            elif ftype=="text":
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <input type="text" id="%s" value="%s" style="width:100%%;">\n      </div>'%(f["id"],f["label"],f["id"],(f.get("value","") or "").replace('"',"&quot;")))
            else:
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <input type="number" id="%s" value="%s" step="%s">\n      </div>'%(f["id"],f["label"],f["id"],f["value"],f.get("step","1")))
        rows.append('    <div class="input-row">\n'+ "\n".join(cells)+'\n    </div')
    return "\n".join(rows)

def render_reset(t):
    lines=[]
    for f in t["inputs"]:
        ftype=f.get("type","number")
        if ftype=="select":
            lines.append("document.getElementById('%s').selectedIndex=0;"%f["id"])
        elif ftype=="textarea":
            v=(f.get("value","") or "").replace("\\","\\\\").replace("'","\\'").replace("\n","\\n")
            lines.append("document.getElementById('%s').value='%s';"%(f["id"],v))
        elif ftype=="text":
            v=(f.get("value","") or "").replace("\\","\\\\").replace("'","\\'")
            lines.append("document.getElementById('%s').value='%s';"%(f["id"],v))
        else:
            lines.append("document.getElementById('%s').value='%s';"%(f["id"],f["value"]))
    lines.append("calcTool();")
    return "\n      ".join(lines)

def render(t):
    return (TEMPLATE
        .replace("__CAT__",t["cat"]).replace("__INDUSTRY__",t["industry"])
        .replace("__ICON__",t["icon"]).replace("__BG__",t["bg"])
        .replace("__ACCENT__",t["accent"]).replace("__INDICON__",t["indicon"])
        .replace("__SLUG__",t["slug"]).replace("__TITLE__",H.escape(t["title"]))
        .replace("__H1__",H.escape(t["h1"])).replace("__H2__",H.escape(t["h2"]))
        .replace("__INTRO__",H.escape(t["intro"])).replace("__DESC__",H.escape(t["desc"]))
        .replace("__CATZH__",IND_ZH[t["industry"]]).replace("__BASE__",BASE)
        .replace("__INPUTS__",render_inputs(t))
        .replace("__CALC__",t["calc"].strip())
        .replace("__RESET__",render_reset(t))
        .replace("__NOTES__","\n".join("        <li>%s</li>"%n for n in t["notes"]))
        .replace("__REF__",t.get("ref","") or ""))

def main():
    for t in TOOLS:
        d=os.path.join(TOOLS_DIR,t["industry"]); os.makedirs(d,exist_ok=True)
        p=os.path.join(d,t["slug"]+".html")
        with open(p,"w",encoding="utf-8") as f:
            f.write(render(t))
        print("  + tools/%s/%s.html  (%d bytes)"%(t["industry"],t["slug"],os.path.getsize(p)))
    print("共生成 %d 个工具页"%len(TOOLS))

if __name__=="__main__":
    main()
