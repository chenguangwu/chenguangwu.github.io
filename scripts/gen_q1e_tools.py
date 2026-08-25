#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 一期（gen_q1e）生成器：13 个 it-tools 风格转换/编码/速查类 A 级工具。
复用 gen_q1_tools 的 TEMPLATE 范式（inputs + calcTool），新增 type="text" 输入支持。
用法：python3 scripts/gen_q1e_tools.py
生成（行业/文件）：
  it/roman-numeral-converter.html      罗马数字转换器
  it/mime-type-lookup.html             MIME 类型速查
  it/http-methods-reference.html       HTTP 方法速查
  it/json-repair.html                  JSON 修复
  text/text-to-braille.html            文本转盲文
  text/text-to-1337.html               文本转 Leet 语
  encode/binary-to-ascii.html          二进制/十六进制转 ASCII
  text/text-to-ascii-art.html          文本转 ASCII 艺术字
  it/triangle-calculator.html          三角形计算器
  it/prime-checker.html                质数检测
  design/color-shade-generator.html    颜色明暗生成器
  it/ipv4-range-expander.html           IPv4 范围展开
  it/ipv6-converter.html                IPv6 地址转换
"""
import os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
BASE = "https://chenguangwu.github.io"

IND_ZH = {"it": "IT开发", "design": "平面设计", "text": "文本处理", "encode": "编码转换"}

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
 "slug":"roman-numeral-converter","industry":"it","cat":"dev","icon":"🔢","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"罗马数字转换器",
 "h1":"罗马数字转换器",
 "h2":"🔢 罗马数字转换器",
 "desc":"罗马数字转换器 - 在阿拉伯数字（1–3999）与罗马数字之间双向换算，附转换规则速查表。纯前端本地计算，无需上传。",
 "intro":"罗马数字用 I/V/X/L/C/D/M 表示 1/5/10/50/100/500/1000，相同的符号并排表示相加，小的符号放在大的左边表示相减（如 IV=4）。输入数字或罗马串即可立即互转。",
 "inputs":[
   {"id":"number","label":"阿拉伯数字（1–3999）","value":"1984","step":"1","min":"1","max":"3999"},
   {"id":"roman","label":"罗马数字（反向转换时填写）","type":"textarea","rows":"2","value":"MCMLXXXIV"},
   {"id":"dir","label":"转换方向","type":"select","opts":[["to","数字 → 罗马"],["from","罗马 → 数字"]]}
 ],
 "calc":"""
var dir=document.getElementById('dir').value;
var M=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]];
function toRoman(v){var s='';for(var i=0;i<M.length;i++){while(v>=M[i][1]){s+=M[i][0];v-=M[i][1];}}return s;}
var RMAP={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};
function fromRoman(s){s=(s||'').toUpperCase().replace(/[^IVXLCDM]/g,'');var t=0,p=0;for(var i=s.length-1;i>=0;i--){var c=RMAP[s[i]]||0;if(c<p){t-=c;}else{t+=c;}p=c;}return t;}
var html='<div class="result-title">转换结果</div>';
if(dir==='to'){
  var n=Math.floor(num('number'));
  if(n<1||n>3999){html+='<p class="muted">请输入 1–3999 之间的整数。</p>';}
  else{html+='<div class="big-result">'+n+' = <b>'+toRoman(n)+'</b></div><p class="muted">'+n+' 的罗马数字写法为 '+toRoman(n)+'</p>';}
}else{
  var s=document.getElementById('roman').value.trim();
  if(!s){html+='<p class="muted">请在上方填入罗马数字（如 MCMLXXXIV）。</p>';}
  else{html+='<div class="big-result">'+escH(s)+' → <b>'+fromRoman(s)+'</b></div>';}
}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "罗马数字没有 0，也没有表示超过 3999 的标准写法（大数用上划线表示，本工具仅支持 1–3999）。",
   "左减规则只适用于 I(1)/X(10)/C(100) 紧邻下一个更大的五或十倍数：IV=4、IX=9、XL=40、XC=90、CD=400、CM=900，不能出现 IL 或 IC 这类写法。",
   "钟表、版权年份、章节编号、纪念碑铭文常使用罗马数字，转换后可方便核对。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📏 罗马数字符号表</h3>
  <table class="ref-table">
    <tr><th>符号</th><th>值</th><th>说明</th></tr>
    <tr><td>I</td><td>1</td><td>最小单位</td></tr>
    <tr><td>V</td><td>5</td><td>—</td></tr>
    <tr><td>X</td><td>10</td><td>—</td></tr>
    <tr><td>L</td><td>50</td><td>—</td></tr>
    <tr><td>C</td><td>100</td><td>—</td></tr>
    <tr><td>D</td><td>500</td><td>—</td></tr>
    <tr><td>M</td><td>1000</td><td>最大标准单位</td></tr>
  </table>
  <p>组合示例：IV=4、IX=9、XL=40、XC=90、CD=400、CM=900；1984 = MCMLXXXIV（M+CM+LXXX+IV）。</p>
</div>
"""
},
{
 "slug":"mime-type-lookup","industry":"it","cat":"dev","icon":"📎","bg":"#ecfeff","accent":"#06B6D4","indicon":"💻",
 "title":"MIME 类型速查",
 "h1":"MIME 类型速查",
 "h2":"📎 MIME 类型速查",
 "desc":"MIME 类型速查 - 输入文件扩展名查对应 MIME（如 json→application/json），或反向由 MIME 查常见扩展名。纯前端本地查询。",
 "intro":"MIME（Multipurpose Internet Mail Extensions）类型用于标识文件的内容格式，浏览器、服务器、API 都靠它决定如何处理数据。输入扩展名或 MIME 即可双向查询。",
 "inputs":[
   {"id":"q","label":"扩展名或 MIME（如 json / application/json，不含点）","type":"text","value":"json"},
   {"id":"dir","label":"查询方向","type":"select","opts":[["ext","扩展名 → MIME"],["mime","MIME → 扩展名"]]}
 ],
 "calc":"""
var MAP={'json':'application/json','xml':'application/xml','html':'text/html','htm':'text/html','css':'text/css','js':'text/javascript','mjs':'text/javascript','csv':'text/csv','txt':'text/plain','md':'text/markdown','pdf':'application/pdf','zip':'application/zip','png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','gif':'image/gif','webp':'image/webp','svg':'image/svg+xml','ico':'image/x-icon','bmp':'image/bmp','mp3':'audio/mpeg','wav':'audio/wav','ogg':'audio/ogg','mp4':'video/mp4','webm':'video/webm','woff':'font/woff','woff2':'font/woff2','ttf':'font/ttf','otf':'font/otf','jsonld':'application/ld+json','yaml':'application/yaml','yml':'application/yaml','toml':'application/toml','rss':'application/rss+xml','atom':'application/atom+xml','wasm':'application/wasm','geojson':'application/geo+json','xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document','pptx':'application/vnd.openxmlformats-officedocument.presentationml.presentation'};
var q=document.getElementById('q').value.trim().toLowerCase();
var dir=document.getElementById('dir').value;
var html='<div class="result-title">查询结果</div>';
if(dir==='ext'){
  if(q.charAt(0)==='.')q=q.slice(1);
  var m=MAP[q];
  if(m){html+='<div class="big-result">.'+escH(q)+' → <b>'+escH(m)+'</b></div>';}
  else{html+='<p class="muted">未收录该扩展名，可能是非常用或不常见格式。</p>';}
}else{
  var hits=[];for(var k in MAP){if(MAP[k]===q)hits.push(k);}
  if(hits.length){html+='<div class="big-result">'+escH(q)+' → <b>.'+hits.join(' / .')+'</b></div>';}
  else{html+='<p class="muted">未收录该 MIME 类型。</p>';}
}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "MIME 类型由类型/子类型组成，中间用斜杠分隔，如 text/html、image/png、application/json。",
   "同一个扩展名在不同系统可能有不同 MIME（如 js 在旧规范是 application/javascript，现代多为 text/javascript），以服务端实际配置为准。",
   "设置 Content-Type 头错误会导致浏览器不执行脚本或下载而非预览，调试接口时常用本工具核对。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常见 MIME 速查表</h3>
  <table class="ref-table">
    <tr><th>扩展名</th><th>MIME</th></tr>
    <tr><td>.json</td><td>application/json</td></tr>
    <tr><td>.html</td><td>text/html</td></tr>
    <tr><td>.css</td><td>text/css</td></tr>
    <tr><td>.js</td><td>text/javascript</td></tr>
    <tr><td>.csv</td><td>text/csv</td></tr>
    <tr><td>.png</td><td>image/png</td></tr>
    <tr><td>.jpg</td><td>image/jpeg</td></tr>
    <tr><td>.svg</td><td>image/svg+xml</td></tr>
    <tr><td>.pdf</td><td>application/pdf</td></tr>
    <tr><td>.zip</td><td>application/zip</td></tr>
  </table>
</div>
"""
},
{
 "slug":"http-methods-reference","industry":"it","cat":"dev","icon":"🌐","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"HTTP 方法速查",
 "h1":"HTTP 方法速查",
 "h2":"🌐 HTTP 方法速查",
 "desc":"HTTP 方法速查 - 查看 GET/POST/PUT/PATCH/DELETE 等标准方法的语义、是否安全、是否幂等、典型用途与注意事项。纯前端查阅。",
 "intro":"HTTP 方法（动词）描述对资源执行的操作。理解 safe（安全）与 idempotent（幂等）有助于设计可缓存、可重试的 RESTful 接口。选择方法即可查看详情。",
 "inputs":[
   {"id":"method","label":"HTTP 方法","type":"select","opts":[["GET","GET"],["POST","POST"],["PUT","PUT"],["PATCH","PATCH"],["DELETE","DELETE"],["HEAD","HEAD"],["OPTIONS","OPTIONS"],["CONNECT","CONNECT"],["TRACE","TRACE"]]}
 ],
 "calc":"""
var M={
 'GET':{safe:true,idem:true,desc:'获取资源表示，不改变服务器状态。',use:'读取数据、查询列表、渲染页面。',note:'可被缓存、可书签；请求体通常语义上忽略。'},
 'POST':{safe:false,idem:false,desc:'向资源提交数据，通常由服务器决定新建资源的 URI。',use:'创建资源、提交表单、触发处理。',note:'非幂等，重复提交可能创建多个资源；部分实现用于局部更新也非标准。'},
 'PUT':{safe:false,idem:true,desc:'用请求体完整替换指定 URI 的资源。',use:'整体更新、创建（客户端指定 URI）。',note:'幂等：多次相同请求结果一致；缺失字段会被清空。'},
 'PATCH':{safe:false,idem:false,desc:'对资源做部分修改（补丁）。',use:'局部更新单个字段。',note:'非幂等（除非补丁文档本身幂等）；与 PUT 的区别在于是否整体替换。'},
 'DELETE':{safe:false,idem:true,desc:'删除指定 URI 的资源。',use:'删除资源。',note:'幂等：第一次删除后重复删除通常返回 404 而非错误。'},
 'HEAD':{safe:true,idem:true,desc:'与 GET 相同但只返回响应头、不返回响应体。',use:'探测资源是否存在、查看元数据/大小。',note:'安全且幂等；常用于健康检查与缓存校验。'},
 'OPTIONS':{safe:true,idem:true,desc:'返回目标资源支持的通信选项（如允许的 Method/Header）。',use:'CORS 预检、探测接口能力。',note:'常在跨域请求前由浏览器自动发送（预检）。'},
 'CONNECT':{safe:false,idem:false,desc:'建立到目标服务器的隧道（通常用于 HTTPS 代理）。',use:'HTTP 代理的端到端隧道。',note:'将连接转为隧道，不是常规资源操作。'},
 'TRACE':{safe:true,idem:true,desc:'回显请求，用于诊断（多数服务器出于安全默认禁用）。',use:'回路诊断、调试。',note:'存在 XST 跨站追踪风险，生产环境一般关闭。'}
};
var m=document.getElementById('method').value;
var d=M[m];
var html='<div class="result-title">'+escH(m)+' 方法</div>';
html+='<div class="data-grid">';
html+='<div class="data-card"><div class="num">'+(d.safe?'是':'否')+'</div><div class="label">安全 Safe</div></div>';
html+='<div class="data-card"><div class="num">'+(d.idem?'是':'否')+'</div><div class="label">幂等 Idempotent</div></div>';
html+='</div>';
html+='<p><b>语义：</b>'+escH(d.desc)+'</p>';
html+='<p><b>典型用途：</b>'+escH(d.use)+'</p>';
html+='<p class="muted"><b>注意：</b>'+escH(d.note)+'</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "Safe（安全）：方法不应改变服务器状态，GET/HEAD/OPTIONS/TRACE/CONNECT 中除 CONNECT 外被视为安全方法，可缓存。",
   "Idempotent（幂等）：多次相同请求产生相同最终状态，GET/PUT/DELETE/HEAD/OPTIONS/TRACE 幂等，POST/PATCH 不保证。",
   "REST 约定：查询用 GET、整体新建用 POST、整体更新用 PUT、局部更新用 PATCH、删除用 DELETE。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 方法对照速查表</h3>
  <table class="ref-table">
    <tr><th>方法</th><th>安全</th><th>幂等</th><th>含义</th></tr>
    <tr><td>GET</td><td>✅</td><td>✅</td><td>读取</td></tr>
    <tr><td>POST</td><td>❌</td><td>❌</td><td>新建/提交</td></tr>
    <tr><td>PUT</td><td>❌</td><td>✅</td><td>整体替换</td></tr>
    <tr><td>PATCH</td><td>❌</td><td>❌</td><td>局部修改</td></tr>
    <tr><td>DELETE</td><td>❌</td><td>✅</td><td>删除</td></tr>
    <tr><td>HEAD</td><td>✅</td><td>✅</td><td>仅头</td></tr>
    <tr><td>OPTIONS</td><td>✅</td><td>✅</td><td>选项</td></tr>
  </table>
</div>
"""
},
{
 "slug":"json-repair","industry":"it","cat":"dev","icon":"🛠️","bg":"#f5f3ff","accent":"#7C3AED","indicon":"💻",
 "title":"JSON 修复器",
 "h1":"JSON 修复器",
 "h2":"🛠️ JSON 修复器",
 "desc":"JSON 修复器 - 粘贴损坏的 JSON（尾随逗号、单引号、注释、多余引号），一键尝试修复并校验是否合法。纯前端本地处理。",
 "intro":"从接口日志、配置文件复制来的 JSON 常带尾随逗号、单引号键、JS 注释等问题，直接 JSON.parse 会报错。本工具尝试自动修复并输出可解析的结果。",
 "inputs":[
   {"id":"src","label":"粘贴损坏的 JSON","type":"textarea","rows":"6","value":"{\n  'name': 'ToolBox', // 工具站\n  \"tools\": [1, 2, 3,],\n}"}
 ],
 "calc":"""
var raw=document.getElementById('src').value;
function repair(s){
  s=s.replace(/\\/\\*[\\s\\S]*?\\*\\//g,'');
  s=s.replace(/\\/\\/[^\\n]*/g,'');
  s=s.replace(/([\\{,\\[\\:])\\s*'([^']+)'\\s*:/g,'$1\"$2\":');
  s=s.replace(/:\\s*'([^']*)'/g,':\"$1\"');
  s=s.replace(/,(\\s*[\\}\\]])/g,'$1');
  return s;
}
var fixed=repair(raw);
var ok=true,err='';
try{JSON.parse(fixed);}catch(e){ok=false;err=e.message;}
var html='<div class="result-title">修复结果</div>';
if(ok){html+='<div class="big-result" style="font-size:15px;">✅ JSON 合法，可复制使用</div>';}
else{html+='<p style="color:#dc2626;">⚠️ 仍无法解析：'+escH(err)+'</p>';}
html+='<pre class="code-box" style="white-space:pre-wrap;word-break:break-all;">'+escH(fixed)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "修复器会移除 /* */ 与 // 注释、把单引号键/值转成双引号、删除对象/数组尾随的逗号，覆盖大多数复制粘贴造成的错误。",
   "修复是启发式的：若结构本身严重损坏（缺括号、键名无引号且非数字），仍可能失败，请对照错误提示手动修正。",
   "处理敏感数据时请在本地完成，不要上传到第三方修复网站。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常见 JSON 错误与修复</h3>
  <table class="ref-table">
    <tr><th>问题</th><th>示例</th><th>修复</th></tr>
    <tr><td>尾随逗号</td><td>[1,2,3,]</td><td>[1,2,3]</td></tr>
    <tr><td>单引号</td><td>{'a':1}</td><td>{"a":1}</td></tr>
    <tr><td>行注释</td><td>{"a":1} // x</td><td>{"a":1}</td></tr>
    <tr><td>键无引号</td><td>{a:1}</td><td>{"a":1}</td></tr>
  </table>
</div>
"""
},
{
 "slug":"text-to-braille","industry":"text","cat":"text","icon":"⠿","bg":"#fefce8","accent":"#CA8A04","indicon":"✏️",
 "title":"文本转盲文",
 "h1":"文本转盲文",
 "h2":"⠿ 文本转盲文",
 "desc":"文本转盲文 - 将英文字母、数字与常见标点转换为盲文 Unicode 点字（U+2800 起），支持大写转写。纯前端本地转换。",
 "intro":"盲文用 6 点单元（2 列 × 3 行）表示字符，Unicode 在 U+2800 起为每个点字分配码位。输入文本即可逐字符转成盲文，便于触感阅读与无障碍排版预览。",
 "inputs":[
   {"id":"src","label":"输入文本（英文/数字/标点）","type":"textarea","rows":"3","value":"Hello 123!"}
 ],
 "calc":"""
var B={a:'⠁',b:'⠃',c:'⠉',d:'⠙',e:'⠑',f:'⠋',g:'⠛',h:'⠓',i:'⠊',j:'⠚',k:'⠅',l:'⠇',m:'⠍',n:'⠝',o:'⠕',p:'⠏',q:'⠟',r:'⠗',s:'⠎',t:'⠞',u:'⠥',v:'⠧',w:'⠺',x:'⠭',y:'⠽',z:'⠵','1':'⠂','2':'⠆','3':'⠒','4':'⠲','5':'⠢','6':'⠖','7':'⠶','8':'⠦','9':'⠔','0':'⠴','.':'⠲',',':'⠂','?':'⠦','!':'⠖',':':'⠒',';':'⠆','-':'⠤',"'":'⠄','(':'⠣',')':'⠜'};
var s=document.getElementById('src').value;
var out='';
for(var i=0;i<s.length;i++){
  var c=s[i];
  if(c===' '){out+=' ';continue;}
  var low=c.toLowerCase();
  out+=(B[low]||(c==='\\n'?'\\n':'■'));
}
var html='<div class="result-title">盲文结果</div>';
html+='<div style="font-size:32px;line-height:1.6;letter-spacing:4px;word-break:break-all;">'+escH(out)+'</div>';
html+='<p class="muted">大写字母默认按对应小写点字呈现（盲文大小写用前缀点区分，本工具仅做基础转写）。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "盲文基础拉丁字母 a–j 对应点 1–5，k–t 在 a–j 基础上加第 6 点（点 3-6），其余字母有专门的点位组合。",
   "数字 1–0 复用 a–j 的点字，前置 # 号（数符）区分；本工具直接输出数字点字。",
   "完整英语盲文还包含大写前缀（⠠）、数字前缀（⠼）及缩写（contractions），正式排版需专用规则。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 盲文字母点位（a–j）</h3>
  <table class="ref-table">
    <tr><th>字母</th><th>点字</th><th>点位</th></tr>
    <tr><td>a</td><td>⠁</td><td>1</td></tr>
    <tr><td>b</td><td>⠃</td><td>1-2</td></tr>
    <tr><td>c</td><td>⠉</td><td>1-4</td></tr>
    <tr><td>e</td><td>⠑</td><td>1-5</td></tr>
    <tr><td>j</td><td>⠚</td><td>2-4-5</td></tr>
  </table>
</div>
"""
},
{
 "slug":"text-to-1337","industry":"text","cat":"text","icon":"💬","bg":"#fefce8","accent":"#CA8A04","indicon":"✏️",
 "title":"文本转 Leet 语",
 "h1":"文本转 Leet 语",
 "h2":"💬 文本转 Leet 语（1337）",
 "desc":"文本转 Leet 语 - 将字母替换为数字与符号（a→4、e→3、t→7），支持低/中/高三档强度。纯前端本地转换。",
 "intro":"Leet（1337）语用形似的数字与符号替代字母，早年用于极客圈与游戏昵称。选择强度即可把普通文本转成 leet 风格。",
 "inputs":[
   {"id":"src","label":"输入文本","type":"textarea","rows":"3","value":"leet speak is fun"},
   {"id":"level","label":"替换强度","type":"select","opts":[["low","低（仅常见字母）"],["mid","中（更多替换）"],["high","高（全部可替）"]]}
 ],
 "calc":"""
var LOW={e:'3',a:'4',o:'0',t:'7',l:'1',s:'5'};
var MID={e:'3',a:'4',o:'0',t:'7',l:'1',s:'5',i:'1',b:'8',g:'6',z:'2'};
var HIGH={e:'3',a:'4',o:'0',t:'7',l:'1',s:'5',i:'1',b:'8',g:'6',z:'2',n:'|\\|',r:'|2',k:'|&lt;',f:'|='};
var lv=document.getElementById('level').value;
var MAP=lv==='low'?LOW:(lv==='mid'?MID:HIGH);
var s=document.getElementById('src').value;
var out='';
for(var i=0;i<s.length;i++){
  var c=s[i].toLowerCase();
  out+=(MAP[c]!==undefined?MAP[c]:s[i]);
}
var html='<div class="result-title">Leet 结果（'+lv+'）</div>';
html+='<div class="big-result" style="font-size:18px;word-break:break-all;">'+escH(out)+'</div>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "低强度只替换 e/a/o/t/l/s 等最常见字母，可读性最高；高强度几乎每个字母都替换，更像传统 1337。",
   "同一字母在不同 leet 方言里写法不一（如 a 也可写作 /\\、@），本工具采用通用一组映射。",
   "用于昵称、彩蛋、教学演示，正式文案请勿使用以免影响可访问性。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常见 Leet 映射</h3>
  <table class="ref-table">
    <tr><th>字母</th><th>Leet</th></tr>
    <tr><td>a</td><td>4 / @</td></tr>
    <tr><td>e</td><td>3</td></tr>
    <tr><td>o</td><td>0</td></tr>
    <tr><td>t</td><td>7</td></tr>
    <tr><td>s</td><td>5 / $</td></tr>
    <tr><td>l</td><td>1 / |_</td></tr>
  </table>
</div>
"""
},
{
 "slug":"binary-to-ascii","industry":"encode","cat":"encode","icon":"🔤","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"二进制/十六进制转 ASCII",
 "h1":"二进制/十六进制转 ASCII",
 "h2":"🔤 二进制 / 十六进制转 ASCII",
 "desc":"二进制/十六进制转 ASCII - 把 8 位一组的二进制串或 2 位一组的十六进制串还原为文本，自动忽略空格与换行。纯前端本地转换。",
 "intro":"每个 ASCII 字符占 8 位（1 字节），可用二进制 8 位或十六进制 2 位表示。粘贴连续编码串，选择进制即可解码为可读文本。",
 "inputs":[
   {"id":"src","label":"编码串（二进制或十六进制）","type":"textarea","rows":"4","value":"01001000 01101001 00100000 01010111 01101111 01110010 01101100 01100100 00100001"},
   {"id":"mode","label":"编码进制","type":"select","opts":[["bin","二进制（8 位/组）"],["hex","十六进制（2 位/组）"]]}
 ],
 "calc":"""
var s=document.getElementById('src').value.replace(/[^01a-fA-F]/g,'');
var mode=document.getElementById('mode').value;
var out='';
if(mode==='bin'){
  if(s.length%8!==0){document.getElementById('result').innerHTML='<div class="result-title">提示</div><p class="muted">二进制位数应为 8 的倍数（当前 '+s.length+' 位），请检查是否多/少了位。</p>';return;}
  for(var i=0;i<s.length;i+=8){out+=String.fromCharCode(parseInt(s.substr(i,8),2));}
}else{
  if(s.length%2!==0){document.getElementById('result').innerHTML='<div class="result-title">提示</div><p class="muted">十六进制字符数应为偶数（当前 '+s.length+' 个），请检查。</p>';return;}
  for(var j=0;j<s.length;j+=2){out+=String.fromCharCode(parseInt(s.substr(j,2),16));}
}
var html='<div class="result-title">解码结果</div>';
html+='<div class="big-result" style="font-size:18px;word-break:break-all;">'+escH(out)+'</div>';
html+='<p class="muted">共 '+out.length+' 个字符。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "二进制每组 8 位对应一个字节；十六进制每 2 位对应一个字节，空格、换行会被自动忽略。",
   "仅覆盖 ASCII（0–127）。非 ASCII（如中文 UTF-8）是多字节编码，需先做 UTF-8 字节拆解再逐字节转，本工具不直接支持。",
   "若结果出现乱码，多半是位数不对或混入了其他字符，请先清理输入。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>字符</th><th>二进制</th><th>十六进制</th></tr>
    <tr><td>A</td><td>01000001</td><td>41</td></tr>
    <tr><td>B</td><td>01000010</td><td>42</td></tr>
    <tr><td>a</td><td>01100001</td><td>61</td></tr>
    <tr><td>0</td><td>00110000</td><td>30</td></tr>
  </table>
</div>
"""
},
{
 "slug":"text-to-ascii-art","industry":"text","cat":"text","icon":"🎨","bg":"#fefce8","accent":"#CA8A04","indicon":"✏️",
 "title":"文本转 ASCII 艺术字",
 "h1":"文本转 ASCII 艺术字",
 "h2":"🎨 文本转 ASCII 艺术字",
 "desc":"文本转 ASCII 艺术字 - 把大写字母与数字渲染成 5×5 像素大字（ASCII Art），便于终端标题、README 装饰。纯前端本地生成。",
 "intro":"用等宽字符拼出 5 行高的像素大字，适合命令行横幅、项目 README 的开头装饰。仅支持大写 A–Z 与数字 0–9，其他字符留空。",
 "inputs":[
   {"id":"src","label":"输入文本（自动转大写，仅 A-Z 0-9）","type":"text","value":"HELLO"},
   {"id":"ch","label":"填充字符","type":"text","value":"#"}
 ],
 "calc":"""
var FONT={'A':'01110;10001;11111;10001;10001','B':'11110;10001;11110;10001;11110','C':'01111;10000;10000;10000;01111','D':'11110;10001;10001;10001;11110','E':'11111;10000;11110;10000;11111','F':'11111;10000;11110;10000;10000','G':'01111;10000;10111;10001;01111','H':'10001;10001;11111;10001;10001','I':'11111;00100;00100;00100;11111','J':'00111;00010;00010;10010;01100','K':'10001;10010;11100;10010;10001','L':'10000;10000;10000;10000;11111','M':'10001;11011;10101;10001;10001','N':'10001;11001;10101;10011;10001','O':'01110;10001;10001;10001;01110','P':'11110;10001;11110;10000;10000','Q':'01110;10001;10101;10010;01101','R':'11110;10001;11110;10010;10001','S':'01111;10000;01110;00001;11110','T':'11111;00100;00100;00100;00100','U':'10001;10001;10001;10001;01110','V':'10001;10001;10001;01010;00100','W':'10001;10001;10101;11011;10001','X':'10001;10001;01010;01010;10001','Y':'10001;10001;01010;00100;00100','Z':'11111;00010;00100;01000;11111','0':'01110;10011;10101;11001;01110','1':'00100;01100;00100;00100;01110','2':'11110;00001;01110;10000;11111','3':'11110;00001;01110;00001;11110','4':'10010;10010;11111;00010;00010','5':'11111;10000;11110;00001;11110','6':'01110;10000;11110;10001;01110','7':'11111;00001;00010;00100;00100','8':'01110;10001;01110;10001;01110','9':'01110;10001;01111;00001;01110'};
var s=document.getElementById('src').value.toUpperCase();
var ch=(document.getElementById('ch').value||'#');
if(ch.length>1)ch=ch[0];
var rows=['','','','',''];
for(var i=0;i<s.length;i++){
  var pat=FONT[s[i]];
  if(!pat){for(var r=0;r<5;r++){rows[r]+='     ';}continue;}
  var lines=pat.split(';');
  for(var r=0;r<5;r++){
    for(var c=0;c<5;c++){rows[r]+=(lines[r][c]==='1'?ch:' ');}
    rows[r]+='  ';
  }
}
var html='<div class="result-title">ASCII 艺术字</div>';
html+='<pre class="code-box" style="font-family:monospace;font-size:14px;line-height:1.1;">'+escH(rows.join('\\n'))+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "每个字符为 5 行 × 5 列像素网格，用填充字符（默认 #）表示点亮、空格表示熄灭，支持自定义填充字符。",
   "仅内置 A–Z 与 0–9 的字形；小写会自动转大写，其他字符（含中文、空格、符号）留空占位。",
   "渲染依赖等宽字体，复制后请在等宽环境下查看，宽度错乱时调小字号。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 提示</h3>
  <p>要把结果用于 README，可整体放进 <code>```text</code> 代码块；终端横幅建议填充字符用 <code>#</code> 或 <code>*</code>。</p>
  <p>如需更华丽的字体（斜体、阴影、小型/大型），可改用 figlet 等成熟工具，本工具主打轻量无依赖。</p>
</div>
"""
},
{
 "slug":"triangle-calculator","industry":"it","cat":"dev","icon":"📐","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"三角形计算器",
 "h1":"三角形计算器",
 "h2":"📐 三角形计算器",
 "desc":"三角形计算器 - 输入三条边长，计算周长、半周长、面积（海伦公式）与三个内角的角度，并判断三角形类型。纯前端本地计算。",
 "intro":"只要知道三条边长，就能用海伦公式求出面积，再用余弦定理求出每个内角。本工具还会判断是否为合法三角形，以及直角/锐角/钝角类型。",
 "inputs":[
   {"id":"a","label":"边长 a","value":"3","step":"0.01","min":"0"},
   {"id":"b","label":"边长 b","value":"4","step":"0.01","min":"0"},
   {"id":"c","label":"边长 c","value":"5","step":"0.01","min":"0"}
 ],
 "calc":"""
var a=num('a'),b=num('b'),c=num('c');
var html='<div class="result-title">计算结果</div>';
if(a<=0||b<=0||c<=0){html+='<p class="muted">边长必须为正数。</p>';document.getElementById('result').innerHTML=html;return;}
if(a+b<=c||a+c<=b||b+c<=a){html+='<p style="color:#dc2626;">⚠️ 这三条边不能构成三角形（两边之和需大于第三边）。</p>';document.getElementById('result').innerHTML=html;return;}
var p=a+b+c, s=p/2;
var area=Math.sqrt(s*(s-a)*(s-b)*(s-c));
function ang(x,y,z){return Math.acos((y*y+z*z-x*x)/(2*y*z))*180/Math.PI;}
var A=ang(a,b,c),B=ang(b,a,c),C=ang(c,a,b);
var type=(Math.abs(A-90)<1e-6||Math.abs(B-90)<1e-6||Math.abs(C-90)<1e-6)?'直角三角形':((A<90&&B<90&&C<90)?'锐角三角形':'钝角三角形');
html+='<div class="data-grid">';
html+='<div class="data-card"><div class="num">'+p.toFixed(3)+'</div><div class="label">周长</div></div>';
html+='<div class="data-card"><div class="num">'+s.toFixed(3)+'</div><div class="label">半周长</div></div>';
html+='<div class="data-card"><div class="num">'+area.toFixed(3)+'</div><div class="label">面积</div></div>';
html+='<div class="data-card"><div class="num">'+type+'</div><div class="label">类型</div></div>';
html+='</div>';
html+='<p style="margin-top:12px;"><b>三个内角：</b>∠A='+A.toFixed(2)+'°　∠B='+B.toFixed(2)+'°　∠C='+C.toFixed(2)+'°（合计 '+(A+B+C).toFixed(2)+'°）</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "海伦公式：面积 = √[s(s−a)(s−b)(s−c)]，其中 s 为半周长（周长的一半），对任意三角形都成立。",
   "余弦定理：cos A = (b²+c²−a²)/(2bc)，据此反推角度；三个角之和恒为 180°。",
   "判断类型：任一内角≈90° 为直角，三者都<90° 为锐角，否则为钝角（浮点误差用 1e-6 容差）。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常用公式</h3>
  <table class="ref-table">
    <tr><th>量</th><th>公式</th></tr>
    <tr><td>半周长 s</td><td>(a+b+c)/2</td></tr>
    <tr><td>面积</td><td>√[s(s−a)(s−b)(s−c)]</td></tr>
    <tr><td>角 A</td><td>arccos((b²+c²−a²)/(2bc))</td></tr>
  </table>
</div>
"""
},
{
 "slug":"prime-checker","industry":"it","cat":"dev","icon":"🔢","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"质数检测器",
 "h1":"质数检测器",
 "h2":"🔢 质数检测器",
 "desc":"质数检测器 - 判断一个整数是否为质数，若为合数则给出最小质因数与因数分解。纯前端本地计算，支持较大整数。",
 "intro":"质数（素数）只能被 1 和自身整除。本工具用试除法判定是否为质数，并对合数给出分解结果，方便学习数论与校验。",
 "inputs":[
   {"id":"n","label":"整数 n","value":"97","step":"1","min":"0"}
 ],
 "calc":"""
var n=Math.floor(num('n'));
var html='<div class="result-title">判定结果</div>';
if(n<2){html+='<p class="muted">小于 2 的数既不是质数也不是合数。</p>';document.getElementById('result').innerHTML=html;return;}
function isPrime(x){if(x<2)return false;if(x<4)return true;if(x%2===0)return false;for(var i=3;i*i<=x;i+=2){if(x%i===0)return false;}return true;}
if(isPrime(n)){html+='<div class="big-result">'+n+' 是质数 ✅</div>';}
else{
  var factors=[];var x=n;
  for(var d=2;d*d<=x;d++){while(x%d===0){factors.push(d);x/=d;}}
  if(x>1)factors.push(x);
  var min=factors[0];
  html+='<div class="big-result" style="font-size:16px;">'+n+' 是合数 ❌</div>';
  html+='<p><b>最小质因数：</b>'+min+'</p>';
  html+='<p><b>因数分解：</b>'+n+' = '+factors.join(' × ')+'</p>';
}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "质数大于 1 且只有 1 和自身两个正因数；2 是唯一偶质数，其余质数均为奇数。",
   "试除法只需检查到 √n 即可：若到 √n 都没有因数，更大因数必成对出现，无需继续。",
   "因数分解对密码学（RSA）至关重要，但大数分解在计算上极难，这正是公钥加密的安全基础。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 前 20 个质数</h3>
  <p>2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71</p>
</div>
"""
},
{
 "slug":"color-shade-generator","industry":"design","cat":"design","icon":"🎨","bg":"#eef2ff","accent":"#6366F1","indicon":"🎨",
 "title":"颜色明暗生成器",
 "h1":"颜色明暗生成器",
 "h2":"🎨 颜色明暗生成器",
 "desc":"颜色明暗生成器 - 输入一个基色（HEX），生成由浅到深的明暗梯度（tint 混白 / shade 混黑），用于配色与 UI 设计。纯前端本地计算。",
 "intro":"在基色上按比例混入白色得到 tint（更亮），混入黑色得到 shade（更暗）。指定档数即可生成一组协调的明暗色卡，方便做按钮、背景层次。",
 "inputs":[
   {"id":"hex","label":"基色 HEX（如 #6366F1）","type":"text","value":"#6366F1"},
   {"id":"steps","label":"每侧档数","value":"5","step":"1","min":"1"}
 ],
 "calc":"""
function h2r(h){h=h.replace('#','');if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];return [parseInt(h.substr(0,2),16),parseInt(h.substr(2,2),16),parseInt(h.substr(4,2),16)];}
function mix(c,t){return Math.round(c+(t-c)*1);}
function toHex(r,g,b){function p(x){var s=x.toString(16);return s.length<2?'0'+s:s;}return '#'+p(r)+p(g)+p(b);}
var hex=document.getElementById('hex').value.trim();
var m=/^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.exec(hex);
var html='<div class="result-title">明暗梯度</div>';
if(!m){html+='<p style="color:#dc2626;">⚠️ 请输入有效的 HEX 颜色（如 #6366F1）。</p>';document.getElementById('result').innerHTML=html;return;}
var rgb=h2r(hex);var steps=Math.max(1,Math.floor(num('steps')));
var cards='<div class="data-grid">';
for(var i=steps;i>=1;i--){var f=i/(steps+1);var r=mix(rgb[0],255*f),g=mix(rgb[1],255*f),b=mix(rgb[2],255*f);cards+='<div class="data-card"><div class="num" style="background:'+toHex(r,g,b)+';color:'+toHex(r,g,b)+';">·</div><div class="label">'+toHex(r,g,b)+'</div></div>';}
cards+='<div class="data-card"><div class="num" style="background:'+toHex(rgb[0],rgb[1],rgb[2])+';color:'+toHex(rgb[0],rgb[1],rgb[2])+';">·</div><div class="label">'+toHex(rgb[0],rgb[1],rgb[2])+' 基色</div></div>';
for(var j=1;j<=steps;j++){var f2=j/(steps+1);var r2=mix(rgb[0],0*f2),g2=mix(rgb[1],0),b2=mix(rgb[2],0);var rr=Math.round(rgb[0]*(1-f2)),gg=Math.round(rgb[1]*(1-f2)),bb=Math.round(rgb[2]*(1-f2));cards+='<div class="data-card"><div class="num" style="background:'+toHex(rr,gg,bb)+';color:'+toHex(rr,gg,bb)+';">·</div><div class="label">'+toHex(rr,gg,bb)+'</div></div>';}
cards+='</div>';
html+=cards;
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "tint 是基色混入白色（t→1 越亮），shade 是基色混入黑色（越暗），线性混合即可获得平滑过渡。",
   "HEX 支持 3 位简写（如 #F60）与 6 位标准写法，工具会自动展开。",
   "无障碍配色建议保证文字与背景的对比度（WCAG AA 至少 4.5:1），不要只看美观。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 说明</h3>
  <p>左→右为由浅（tint）到基色再到深（shade）的渐变；每侧档数即混入白/黑的比例步数。</p>
  <p>设计系统（如 Tailwind 的 50–900）常用这种按明度分档的色板组织方式。</p>
</div>
"""
},
{
 "slug":"ipv4-range-expander","industry":"it","cat":"dev","icon":"🌐","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"IPv4 范围展开器",
 "h1":"IPv4 范围展开器",
 "h2":"🌐 IPv4 范围展开器",
 "desc":"IPv4 范围展开器 - 输入 CIDR（如 192.168.1.0/24），计算网络地址、广播地址、可用主机数及首末可用 IP。纯前端本地计算。",
 "intro":"CIDR 用「IP/前缀长度」表示一段连续地址。本工具解析后给出该网段的网络地址、广播地址、可用主机范围与数量，常用于子网划分与防火墙规则核对。",
 "inputs":[
   {"id":"cidr","label":"CIDR（IP/前缀，如 192.168.1.0/24）","type":"text","value":"192.168.1.0/24"}
 ],
 "calc":"""
function ip2int(ip){var p=ip.split('.');if(p.length!==4)return NaN;for(var i=0;i<4;i++){var v=+p[i];if(v<0||v>255||isNaN(v))return NaN;}return ((+p[0])<<24)+((+p[1])<<16)+((+p[2])<<8)+(+p[3]);}
function int2ip(n){return ((n>>>24)&255)+'.'+((n>>>16)&255)+'.'+((n>>>8)&255)+'.'+(n&255);}
var v=document.getElementById('cidr').value.trim();
var m=/^([0-9.]+)\\/(\\d{1,2})$/.exec(v);
var html='<div class="result-title">网段解析</div>';
if(!m){html+='<p style="color:#dc2626;">⚠️ 格式应为 IP/前缀，如 192.168.1.0/24。</p>';document.getElementById('result').innerHTML=html;return;}
var ip=m[1],pref=+m[2];
if(pref>32||isNaN(ip2int(ip))){html+='<p style="color:#dc2626;">⚠️ 前缀应在 0–32，IP 须合法。</p>';document.getElementById('result').innerHTML=html;return;}
var base=ip2int(ip);
var mask=pref===0?0:((0xFFFFFFFF<<(32-pref))>>>0);
var net=(base & mask)>>>0;
var bcast=(net | (~mask>>>0))>>>0;
var hosts=(pref>=31)?0:(bcast-net-1);
var first=int2ip((net+1)>>>0), last=int2ip((bcast-1)>>>0);
html+='<div class="data-grid">';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+int2ip(net)+'</div><div class="label">网络地址</div></div>';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+int2ip(bcast)+'</div><div class="label">广播地址</div></div>';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+hosts+'</div><div class="label">可用主机数</div></div>';
html+='<div class="data-card"><div class="num" style="font-size:13px;">'+pref+'</div><div class="label">前缀长度</div></div>';
html+='</div>';
if(hosts>0)html+='<p style="margin-top:12px;"><b>可用范围：</b>'+first+' – '+last+'</p>';
else if(pref===31)html+='<p class="muted">/31 仅两个地址，常作点对点链路，无「可用主机范围」概念。</p>';
else html+='<p class="muted">/32 为单主机地址。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "子网掩码由前缀决定：/24 即 255.255.255.0，前 24 位为网络位、后 8 位为主机位。",
   "网络地址 = IP 与掩码按位与；广播地址 = 网络地址或上掩码取反；可用主机 = 总数 − 2（去掉网络与广播）。",
   "/31、/32 是特殊用途（链路/单主机），可用主机数为 0，本工具已单独提示。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常见前缀对照</h3>
  <table class="ref-table">
    <tr><th>前缀</th><th>掩码</th><th>可用主机</th></tr>
    <tr><td>/24</td><td>255.255.255.0</td><td>254</td></tr>
    <tr><td>/16</td><td>255.255.0.0</td><td>65534</td></tr>
    <tr><td>/8</td><td>255.0.0.0</td><td>16777214</td></tr>
  </table>
</div>
"""
},
{
 "slug":"ipv6-converter","industry":"it","cat":"dev","icon":"🌐","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"IPv6 地址转换器",
 "h1":"IPv6 地址转换器",
 "h2":"🌐 IPv6 地址转换器",
 "desc":"IPv6 地址转换器 - 把 IPv6 地址在压缩（::）与完整（8 组 16 位）形式之间互转，并拆分为 8 个 16 位段。纯前端本地解析。",
 "intro":"IPv6 用冒号分隔的 8 组 16 进制表示，连续全 0 段可压缩为 ::。本工具标准化输入并给出完整展开式与各段，便于核对与填写。",
 "inputs":[
   {"id":"addr","label":"IPv6 地址（可含 :: 压缩）","type":"text","value":"2001:db8::1"}
 ],
 "calc":"""
function expand(ip){
  ip=ip.trim().toLowerCase();
  var hasColon=ip.indexOf('::')>=0;
  var parts=ip.split(':');
  var segs=[];
  if(hasColon){
    var idx=parts.indexOf('');
    var left=parts.slice(0,idx).filter(function(p){return p!=='';});
    var right=parts.slice(idx+1).filter(function(p){return p!=='';});
    var need=8-left.length-right.length;
    if(need<0)return null;
    for(var i=0;i<need;i++)segs.push('0000');
    segs=left.concat(segs).concat(right);
  }else{
    segs=parts;
  }
  if(segs.length!==8)return null;
  for(var k=0;k<8;k++){if(!/^[0-9a-f]{1,4}$/.test(segs[k]))return null;segs[k]=('0000'+segs[k]).slice(-4);}
  return segs;
}
var ip=document.getElementById('addr').value;
var html='<div class="result-title">转换结果</div>';
var segs=expand(ip);
if(!segs){html+='<p style="color:#dc2626;">⚠️ 不是合法的 IPv6 地址。</p>';document.getElementById('result').innerHTML=html;return;}
html+='<div class="big-result" style="font-size:14px;word-break:break-all;">'+segs.join(':')+'</div>';
html+='<p class="muted">压缩形式：'+ip.trim()+'</p>';
html+='<p style="margin-top:8px;"><b>8 段：</b>'+segs.map(function(s,i){return '['+i+'] '+s;}).join('  ')+'</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "IPv6 共 128 位，写成 8 组、每组 4 个十六进制数字，组间用冒号分隔。",
   "压缩规则：连续的全 0 段可替换为 ::（一个地址只能压缩一次），如 2001:db8:0:0:0:0:0:1 → 2001:db8::1。",
   "每组前导 0 可省略（1:0:0:0 写作 1::），但 :: 只能出现一次，否则无法唯一还原。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 示例</h3>
  <table class="ref-table">
    <tr><th>压缩</th><th>完整</th></tr>
    <tr><td>::1</td><td>0000:0000:0000:0000:0000:0000:0000:0001</td></tr>
    <tr><td>2001:db8::1</td><td>2001:0db8:0000:0000:0000:0000:0000:0001</td></tr>
    <tr><td>fe80::1</td><td>fe80:0000:0000:0000:0000:0000:0000:0001</td></tr>
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
            elif ftype=="checkbox":
                boxes="".join(
                  '<label style="display:flex;align-items:center;gap:6px;cursor:pointer;font-size:13px;margin:4px 0;">'
                  '<input type="checkbox" id="top_%s" value="%s" data-name="%s">%s</label>'%(o[0],o[1].split(" ")[1] if " " in o[1] else "0",o[1].split(" ")[0],o[1])
                  for o in f.get("opts",[]))
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <div style="display:flex;flex-wrap:wrap;gap:0 16px;">%s</div>\n      </div>'%(f["id"],f["label"],boxes))
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
        elif ftype=="checkbox":
            for o in f.get("opts",[]):
                lines.append("document.getElementById('top_%s').checked=false;"%o[0])
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
