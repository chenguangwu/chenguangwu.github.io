#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 三期（gen_q1g）生成器：13 个 it-tools 风格校验/生成/速查类 A 级工具。
复用 gen_q1e 的 TEMPLATE 范式（inputs + calcTool）。
用法：python3 scripts/gen_q1g_tools.py
生成（行业/文件）：
  it/xml-validator.html              XML 校验
  it/csv-validator.html              CSV 校验
  it/css-minify.html                 CSS 压缩
  it/js-minify.html                  JS 压缩
  it/markdown-lint.html              Markdown 检查
  it/hash-identifier.html            哈希算法识别
  it/gitignore-generator.html        .gitignore 生成
  it/dockerfile-generator.html       Dockerfile 生成
  it/sitemap-generator.html          sitemap.xml 生成
  design/color-blindness-sim.html    色盲模拟
  it/nginx-config-generator.html     Nginx 配置生成
  it/kubernetes-yaml-generator.html  Kubernetes YAML 生成
  it/meta-tags-generator.html         Meta 标签生成
"""
import os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
BASE = "https://chenguangwu.github.io"

IND_ZH = {"it": "IT开发", "design": "平面设计"}

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
 "slug":"xml-validator","industry":"it","cat":"dev","icon":"🧩","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"XML 校验器",
 "h1":"XML 校验器",
 "h2":"🧩 XML 校验器",
 "desc":"XML 校验器 - 粘贴 XML 文档，检查是否格式良好（well-formed）：标签是否配对、属性是否引号闭合、是否有非法字符。纯前端本地解析。",
 "intro":"XML 要求标签严格嵌套且正确关闭。本工具用浏览器 DOMParser 解析，报告任何格式错误及大致位置，帮助你在部署前修好配置文件。",
 "inputs":[
   {"id":"src","label":"粘贴 XML","type":"textarea","rows":"7","value":"<?xml version=\"1.0\"?>\n<note>\n  <to>Tony</to>\n  <from>Anna</from>\n  <body>Hi!</body>\n</note>"}
 ],
 "calc":"""
var xml=document.getElementById('src').value;
var html='<div class="result-title">校验结果</div>';
if(!xml.trim()){html+='<p class="muted">请粘贴 XML 内容。</p>';document.getElementById('result').innerHTML=html;return;}
try{
  var doc=new DOMParser().parseFromString(xml,'application/xml');
  var err=doc.getElementsByTagName('parsererror');
  if(err.length){html+='<p style="color:#dc2626;">⚠️ 格式错误</p><pre class="code-box" style="white-space:pre-wrap;font-size:12px;color:#dc2626;">'+escH(err[0].textContent)+'</pre>';}
  else{
    var root=doc.documentElement;
    html+='<div class="big-result" style="font-size:15px;">✅ XML 格式良好</div>';
    html+='<p class="muted">根元素：&lt;'+escH(root?root.tagName:'?')+'&gt;，元素总数 '+doc.getElementsByTagName('*').length+'</p>';
  }
}catch(e){html+='<p style="color:#dc2626;">⚠️ '+escH(e.message)+'</p>';}
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "XML 与 HTML 不同：所有标签必须闭合，属性必须用引号包裹，大小写敏感，且只能有一个根元素。",
   "DOMParser 在浏览器环境可解析，但不同引擎报错信息措辞不同；生产校验建议用专用 XML 校验器（如 xmllint）。",
   "注意 XML 声明 `<?xml ...?>` 应位于文件第一行，前面不能有空行或 BOM。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常见错误</h3>
  <table class="ref-table">
    <tr><th>问题</th><th>修正</th></tr>
    <tr><td>标签未闭合</td><td>&lt;br&gt; → &lt;br/&gt;</td></tr>
    <tr><td>属性无引号</td><td>id=x → id=\"x\"</td></tr>
    <tr><td>多个根</td><td>用单个根包裹全部</td></tr>
  </table>
</div>
"""
},
{
 "slug":"csv-validator","industry":"it","cat":"dev","icon":"📊","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"CSV 校验器",
 "h1":"CSV 校验器",
 "h2":"📊 CSV 校验器",
 "desc":"CSV 校验器 - 粘贴 CSV 文本，检查各行列数是否一致、引号是否平衡、是否存在空字段，定位数据问题行。纯前端本地解析。",
 "intro":"CSV 用逗号分隔、引号包裹含逗号的字段。列数不一致或引号未闭合会导致导入失败。本工具逐行解析并报告异常行号，便于清洗数据。",
 "inputs":[
   {"id":"src","label":"粘贴 CSV（首行为表头）","type":"textarea","rows":"7","value":"name,age,city\nAlice,30,Beijing\nBob,25,Shanghai\nCarol,28"},
   {"id":"sep","label":"分隔符","type":"text","value":","}
 ],
 "calc":"""
function parseLine(line,sep){
  var out=[],cur='',q=false;
  for(var i=0;i<line.length;i++){
    var c=line[i];
    if(q){
      if(c==='\"'&&line[i+1]==='\"'){cur+='\"';i++;}
      else if(c==='\"'){q=false;}
      else cur+=c;
    }else{
      if(c==='\"'){q=true;}
      else if(c===sep){out.push(cur);cur='';}
      else cur+=c;
    }
  }
  out.push(cur);
  return {fields:out,open:q};
}
var src=document.getElementById('src').value.replace(/\\r/g,'');
var sep=document.getElementById('sep').value||',';
var lines=src.split(/\\n/).filter(function(l,i,a){return l.length>0||i<a.length-1;});
if(!lines.length){document.getElementById('result').innerHTML='<div class="result-title">提示</div><p class="muted">请粘贴 CSV。</p>';return;}
var expect=parseLine(lines[0],sep).fields.length;
var issues=[];
for(var i=0;i<lines.length;i++){
  var r=parseLine(lines[i],sep);
  if(r.open)issues.push('第 '+(i+1)+' 行：引号未闭合');
  else if(r.fields.length!==expect)issues.push('第 '+(i+1)+' 行：列数 '+r.fields.length+'（应为 '+expect+'）');
}
var html='<div class="result-title">校验结果</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+lines.length+'</div><div class="label">行数</div></div>';
html+='<div class="data-card"><div class="num">'+expect+'</div><div class="label">标准列数</div></div>';
html+='<div class="data-card"><div class="num" style="color:'+(issues.length?'#dc2626':'#16a34a')+';">'+issues.length+'</div><div class="label">问题</div></div>';
html+='</div>';
if(issues.length){html+='<ul style="margin-top:10px;font-size:13px;color:#dc2626;">'+issues.map(function(x){return '<li>'+escH(x)+'</li>';}).join('')+'</ul>';}
else html+='<p style="color:#16a34a;margin-top:10px;">✅ 未发现列数/引号问题。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "RFC 4180 规定：每行字段数应一致，字段内含逗号/换行时用双引号包裹，引号内字面引号写成两个双引号。",
   "本工具以首行列数为基准比对；若表头本身列数异常，后续全部行会判为不一致，请先确认表头正确。",
   "分号、制表符分隔的「CSV」可改分隔符参数（欧洲常用分号）。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 转义示例</h3>
  <table class="ref-table">
    <tr><th>原文</th><th>CSV</th></tr>
    <tr><td>a,b</td><td>"a,b"</td></tr>
    <tr><td>say &quot;hi&quot;</td><td>&quot;say &quot;&quot;hi&quot;&quot;&quot;</td></tr>
  </table>
</div>
"""
},
{
 "slug":"css-minify","industry":"it","cat":"dev","icon":"🎯","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"CSS 压缩器",
 "h1":"CSS 压缩器",
 "h2":"🎯 CSS 压缩器",
 "desc":"CSS 压缩器 - 去除注释、多余空白与末尾分号，缩小 CSS 体积以加速加载，保留语义不变。纯前端本地压缩。",
 "intro":"上线前压缩 CSS 可减少传输体积、提升首屏速度。本工具去除 /* */ 注释与冗余空白，输出精简 CSS，体积对比一目了然。",
 "inputs":[
   {"id":"src","label":"粘贴 CSS","type":"textarea","rows":"7","value":".btn {\n  /* 主按钮 */\n  color: #fff;\n  background: #3B82F6;\n}\n\n.box {\n  margin: 0 auto;\n}"}
 ],
 "calc":"""
var css=document.getElementById('src').value;
function minify(s){
  s=s.replace(/\\/\\*[\\s\\S]*?\\*\\//g,'');
  s=s.replace(/\\s+/g,' ');
  s=s.replace(/\\s*([{}:;,>])\\s*/g,'$1');
  s=s.replace(/;\\}/g,'}');
  s=s.replace(/\\s+/g,' ').trim();
  return s;
}
var out=minify(css);
var html='<div class="result-title">压缩结果</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+css.length+'</div><div class="label">原始字节</div></div>';
html+='<div class="data-card"><div class="num">'+out.length+'</div><div class="label">压缩后</div></div>';
html+='<div class="data-card"><div class="num">'+(css.length?Math.round((1-out.length/css.length)*100):0)+'%</div><div class="label">节省</div></div>';
html+='</div>';
html+='<pre class="code-box" style="white-space:pre-wrap;word-break:break-all;font-size:12px;">'+escH(out)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "压缩仅去注释与空白，不改变选择器与声明语义；但会移除 source map 关联与可读性，发布版勿保留源注释。",
   "本工具不重写属性（如合并 0px→0），属于「安全压缩」；激进压缩（变量内联、自动前缀）需交给构建工具（cssnano/esbuild）。",
   "生产环境应同时开启 Gzip/Brotli，文本压缩对 CSS 收益最大。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 说明</h3>
  <p>压缩后请本地预览效果是否一致；涉及 <code>content</code> 伪元素里特殊空格时，过度去空白可能需谨慎。本工具保留声明间必要空格。</p>
</div>
"""
},
{
 "slug":"js-minify","industry":"it","cat":"dev","icon":"⚡","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"JS 压缩器",
 "h1":"JS 压缩器",
 "h2":"⚡ JS 压缩器",
 "desc":"JS 压缩器 - 去除 JS 中的注释与多余空白，缩小脚本体积。保守压缩，不重命名变量，适合快速瘦身。纯前端本地压缩。",
 "intro":"部署前压缩 JS 可减小下载体积。本工具去除 // 与 /* */ 注释并压缩空白，保留代码结构，便于回看与调试定位。",
 "inputs":[
   {"id":"src","label":"粘贴 JavaScript","type":"textarea","rows":"7","value":"// 计算总价\nfunction total(items) {\n  /* 遍历累加 */\n  var s = 0;\n  for (var i = 0; i < items.length; i++) {\n    s += items[i];\n  }\n  return s;\n}"}
 ],
 "calc":"""
var js=document.getElementById('src').value;
function minify(s){
  s=s.replace(/\\/\\*[\\s\\S]*?\\*\\//g,'');
  s=s.replace(/\\/\\/[^\\n]*/g,'');
  s=s.replace(/\\s+/g,' ');
  s=s.replace(/\\s*([=+\\-*/%<>{},;:()\\[\\]]\\s*)/g,'$1');
  s=s.replace(/\\s+/g,' ').trim();
  return s;
}
var out=minify(js);
var html='<div class="result-title">压缩结果</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+js.length+'</div><div class="label">原始字节</div></div>';
html+='<div class="data-card"><div class="num">'+out.length+'</div><div class="label">压缩后</div></div>';
html+='<div class="data-card"><div class="num">'+(js.length?Math.round((1-out.length/js.length)*100):0)+'%</div><div class="label">节省</div></div>';
html+='</div>';
html+='<pre class="code-box" style="white-space:pre-wrap;word-break:break-all;font-size:12px;">'+escH(out)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "本压缩为「安全型」：只去注释与空白，不重命名变量、不改作用域，几乎不改变行为。",
   "真正的生产压缩应交给 Terser/esbuild：会做变量重命名、死代码消除、常量折叠，体积更小但不可读。",
   "压缩会删除版权/许可证注释，若需保留请用 /*! 开头的重要注释（本工具一并移除，发布前请确认）。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 建议</h3>
  <p>仅做快速瘦身可用本工具；CI 流水线里推荐集成 Terser 以获得更优压缩率与 tree-shaking。</p>
</div>
"""
},
{
 "slug":"markdown-lint","industry":"it","cat":"dev","icon":"📝","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Markdown 检查器",
 "h1":"Markdown 检查器",
 "h2":"📝 Markdown 检查器",
 "desc":"Markdown 检查器 - 检查标题层级是否连续、列表是否规范、链接格式是否正确、有无重复标题，给出改进建议。纯前端本地检查。",
 "intro":"规范的 Markdown 更易渲染与维护。本工具扫描常见风格问题（如跳级标题、列表缺空格、空链接），逐条列出便于修正。",
 "inputs":[
   {"id":"src","label":"粘贴 Markdown","type":"textarea","rows":"8","value":"# 标题\n\n## 小节\n\n### 跳级到三级（上面缺二级? 实际有二级）\n\n- 列表项\n-列表缺空格\n\n[空链接]()\n\n![图](img.png)"}
 ],
 "calc":"""
var md=document.getElementById('src').value;
var lines=md.split(/\\n/);
var issues=[];
var lastH=0;var heads={};
for(var i=0;i<lines.length;i++){
  var L=lines[i];
  var hm=L.match(/^(#{1,6})\\s/);
  if(hm){
    var lv=hm[1].length;
    if(lastH&&lv>lastH+1)issues.push('第 '+(i+1)+' 行：标题从 H'+lastH+' 跳到 H'+lv+'（建议连续）');
    lastH=lv;
    var txt=L.replace(/^#+/,'').trim();
    heads[txt]=(heads[txt]||0)+1;
    if(heads[txt]>1)issues.push('第 '+(i+1)+' 行：标题重复「'+txt+'」');
  }
  if(/^\\s*[-*]\\S/.test(L))issues.push('第 '+(i+1)+' 行：列表符号后缺空格');
  var links=L.match(/\\[([^\\]]*)\\]\\(([^)]*)\\)/g)||[];
  for(var k=0;k<links.length;k++){var m=links[k].match(/\\[([^\\]]*)\\]\\(([^)]*)\\)/);if(!m[2])issues.push('第 '+(i+1)+' 行：空链接地址');}
}
var html='<div class="result-title">检查结果</div><div class="data-grid">';
html+='<div class="data-card"><div class="num">'+lines.length+'</div><div class="label">行数</div></div>';
html+='<div class="data-card"><div class="num" style="color:'+(issues.length?'#dc2626':'#16a34a')+';">'+issues.length+'</div><div class="label">问题</div></div>';
html+='</div>';
if(issues.length)html+='<ul style="margin-top:10px;font-size:13px;color:#dc2626;">'+issues.map(function(x){return '<li>'+escH(x)+'</li>';}).join('')+'</ul>';
else html+='<p style="color:#16a34a;margin-top:10px;">✅ 未发现明显风格问题。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "标题建议从 H1 起逐层递增，跳级会影响文档大纲与 SEO 锚点。",
   "无序列表 `-`/`*` 后需一个空格；有序列表 `1. ` 后也需空格，否则不渲染为列表。",
   "本检查为风格辅助，不覆盖 CommonMark 全部语法；导出前仍建议用官方解析器预览。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常见规范</h3>
  <table class="ref-table">
    <tr><th>写法</th><th>说明</th></tr>
    <tr><td># 标题</td><td>H1 一个文档一个</td></tr>
    <tr><td>- 项</td><td>符号后空格</td></tr>
    <tr><td>[文本](url)</td><td>链接需地址</td></tr>
  </table>
</div>
"""
},
{
 "slug":"hash-identifier","industry":"it","cat":"dev","icon":"🔍","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"哈希算法识别",
 "h1":"哈希算法识别",
 "h2":"🔍 哈希算法识别",
 "desc":"哈希算法识别 - 输入一段哈希值，根据长度、字符集与特征前缀推测可能的算法（MD5/SHA1/SHA256/SHA512/BCrypt 等）。纯前端本地识别。",
 "intro":"拿到一串哈希却不知算法时，可用长度快速定位。本工具按十六进制长度与常见前缀（如 $2a$/$bcrypt$）匹配，列出可能算法供参考。",
 "inputs":[
   {"id":"h","label":"哈希值","type":"text","value":"5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"}
 ],
 "calc":"""
var v=document.getElementById('h').value.trim();
var html='<div class="result-title">识别结果</div>';
if(!v){html+='<p class="muted">请输入哈希值。</p>';document.getElementById('result').innerHTML=html;return;}
var hex=/^[0-9a-fA-F]+$/.test(v);
var L=v.length;
var cands=[];
if(v.indexOf('$2a$')===0||v.indexOf('$2y$')===0||v.indexOf('$2b$')===0)cands.push(['BCrypt','前缀 $2a$/2y$/2b$']);
if(v.indexOf('$1$')===0)cands.push(['MD5-Crypt','前缀 $1$']);
if(v.indexOf('$argon2')===0)cands.push(['Argon2','前缀 $argon2']);
if(hex){
  var map={32:['MD5','128 位'],40:['SHA-1','160 位'],64:['SHA-256','256 位'],56:['SHA-224','224 位'],96:['SHA-384','384 位'],128:['SHA-512','512 位'],12:['CRC32 / 短校验','32 位十六进制']};
  if(map[L])cands.push([map[L][0],map[L][1]+'（'+L+' 位十六进制）']);
  if(L%2!==0)cands.push(['注意','奇数长度不是标准十六进制哈希']);
}
if(!cands.length)cands.push(['未知','无法仅凭该值判定']);
html+='<div class="data-grid">';
for(var i=0;i<cands.length;i++)html+='<div class="data-card"><div class="num" style="font-size:13px;">'+escH(cands[i][0])+'</div><div class="label">'+escH(cands[i][1])+'</div></div>';
html+='</div>';
html+=L%2===0?'':'<p class="muted" style="margin-top:8px;">长度 '+L+'。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "长度对应：MD5=32、SHA1=40、SHA224=56、SHA256=64、SHA384=96、SHA512=128 个十六进制字符。",
   "密码哈希常带前缀：$2a$/$2y$ 为 BCrypt，$1$ 为传统 MD5-Crypt，$argon2 开头为 Argon2，这些能直接判定。",
   "仅靠哈希值无法反推原文（单向）；识别算法只帮你判断后续校验/存储方式，不能「解密」。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 长度对照</h3>
  <table class="ref-table">
    <tr><th>算法</th><th>十六进制长度</th></tr>
    <tr><td>MD5</td><td>32</td></tr>
    <tr><td>SHA-1</td><td>40</td></tr>
    <tr><td>SHA-256</td><td>64</td></tr>
    <tr><td>SHA-512</td><td>128</td></tr>
  </table>
</div>
"""
},
{
 "slug":"gitignore-generator","industry":"it","cat":"dev","icon":"🚫","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":".gitignore 生成器",
 "h1":".gitignore 生成器",
 "h2":"🚫 .gitignore 生成器",
 "desc":".gitignore 生成器 - 勾选常用语言/框架模板（Python/Node/Go/Rust/Java 等），一键合并生成 .gitignore 内容。纯前端本地生成。",
 "intro":"不同技术栈需忽略的文件各异（依赖目录、构建产物、虚拟环境）。选择你的栈，本工具拼出对应 .gitignore，开箱即用。",
 "inputs":[
   {"id":"langs","label":"选择技术栈（可多选）","type":"checkbox","opts":[["py","Python"],["node","Node.js"],["go","Go"],["rust","Rust"],["java","Java/Kotlin"],["dotnet",".NET"],["c","C/C++"],["ide","IDE/编辑器"]]}
 ],
 "calc":"""
var T={
 'py':['__pycache__/','*.py[cod]','*.egg-info/','.venv/','venv/','env/'],
 'node':['node_modules/','npm-debug.log*','yarn-error.log','dist/','.next/'],
 'go':['*.exe','*.test','/vendor/'],
 'rust':['target/','**/*.rs.bk'],
 'java':['*.class','*.jar','.gradle/','build/'],
 'dotnet':['bin/','obj/','*.user'],
 'c':['*.o','*.out','*.a'],
 'ide':['.idea/','.vscode/','*.swp']
};
var sel=[];
document.querySelectorAll('input[data-name]').forEach(function(el){if(el.checked&&T[el.value])sel.push(el.value);});
var html='<div class="result-title">.gitignore</div>';
if(!sel.length){html+='<p class="muted">请至少选择一种技术栈。</p>';document.getElementById('result').innerHTML=html;return;}
var lines=['# Generated by ToolBox .gitignore Generator'];
for(var i=0;i<sel.length;i++){lines.push('');lines.push('# '+(document.querySelector('input[id=\"top_'+sel[i]+'\"]').nextSibling.textContent.trim()));var arr=T[sel[i]];for(var j=0;j<arr.length;j++)lines.push(arr[j]);}
html+='<pre class="code-box" style="white-space:pre;font-size:12.5px;overflow-x:auto;">'+escH(lines.join('\\n'))+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "勾选项对应各生态官方社区模板的精简版；多栈项目直接合并即可，重复项无害。",
   ".gitignore 对已被跟踪的文件不生效——若误提交了 node_modules，需先 git rm --cached 再忽略。",
   "机密文件（.env）务必忽略；但 .gitignore 不是安全边界，敏感信息请勿入库。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 提示</h3>
  <p>生成后保存为项目根目录的 .gitignore 即可。可继续手动追加项目特有忽略项。</p>
</div>
"""
},
{
 "slug":"dockerfile-generator","industry":"it","cat":"dev","icon":"🐳","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Dockerfile 生成器",
 "h1":"Dockerfile 生成器",
 "h2":"🐳 Dockerfile 生成器",
 "desc":"Dockerfile 生成器 - 选择基础镜像、暴露端口与启动命令，生成可用的 Dockerfile 文本，便于容器化应用。纯前端本地生成。",
 "intro":"容器化第一步是写 Dockerfile。填入基础镜像、工作目录、暴露端口与启动命令，本工具拼出标准 Dockerfile 供复制到项目根目录。",
 "inputs":[
   {"id":"base","label":"基础镜像","type":"text","value":"node:20-alpine"},
   {"id":"port","label":"暴露端口","value":"3000","step":"1","min":"0"},
   {"id":"cmd","label":"启动命令","type":"text","value":"npm start"}
 ],
 "calc":"""
var base=document.getElementById('base').value.trim()||'node:20-alpine';
var port=Math.floor(num('port'));
var cmd=document.getElementById('cmd').value.trim()||'npm start';
var L=['FROM '+base,'WORKDIR /app','COPY . /app','RUN npm install --production','EXPOSE '+(port||'3000'),'CMD ["'+cmd.replace(/"/g,'')+'"]'];
var html='<div class="result-title">Dockerfile</div>';
html+='<pre class="code-box" style="white-space:pre;font-size:12.5px;overflow-x:auto;">'+escH(L.join('\\n'))+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "示例为单阶段构建；生产建议用多阶段构建（builder 阶段编译、runtime 阶段只拷产物）以减小镜像。",
   "EXPOSE 仅声明文档化端口，真正映射由 docker run -p 决定；二者应一致。",
   "COPY . /app 前应放 .dockerignore 排除 node_modules 等，避免上下文臃肿与缓存失效。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 多阶段示例片段</h3>
  <pre class="code-box" style="white-space:pre;font-size:12px;">FROM node:20 AS build\nWORKDIR /app\nCOPY . .\nRUN npm ci && npm run build\nFROM node:20-alpine\nCOPY --from=build /app/dist /app\nCMD [\"npm\",\"start\"]</pre>
</div>
"""
},
{
 "slug":"sitemap-generator","industry":"it","cat":"dev","icon":"🗺️","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Sitemap 生成器",
 "h1":"Sitemap 生成器",
 "h2":"🗺️ Sitemap 生成器",
 "desc":"Sitemap 生成器 - 每行粘贴一个 URL，生成标准 sitemap.xml（含可选 lastmod/优先级），便于提交搜索引擎。纯前端本地生成。",
 "intro":"网站收录靠 sitemap 告诉爬虫有哪些页面。填入全部 URL（每行一个），本工具生成符合 sitemap 协议的 XML，保存为 sitemap.xml 即可。",
 "inputs":[
   {"id":"urls","label":"URL 列表（每行一个，含 https://）","type":"textarea","rows":"7","value":"https://example.com/\nhttps://example.com/about\nhttps://example.com/contact"}
 ],
 "calc":"""
var urls=document.getElementById('urls').value.split(/\\n/).map(function(x){return x.trim();}).filter(function(u){return /^https?:\\/\\//.test(u);});
var html='<div class="result-title">sitemap.xml</div>';
if(!urls.length){html+='<p class="muted">请每行粘贴一个以 http(s):// 开头的 URL。</p>';document.getElementById('result').innerHTML=html;return;}
var today=new Date().toISOString().slice(0,10);
var body=urls.map(function(u){return '  <url>\\n    <loc>'+escH(u)+'</loc>\\n    <lastmod>'+today+'</lastmod>\\n  </url>';}).join('\\n');
var xml='<?xml version=\"1.0\" encoding=\"UTF-8\"?>\\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\\n'+body+'\\n</urlset>';
html+='<div class="data-grid"><div class="data-card"><div class="num">'+urls.length+'</div><div class="label">URL 数</div></div></div>';
html+='<pre class="code-box" style="white-space:pre;font-size:12px;overflow-x:auto;">'+escH(xml)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "单 sitemap 最多 50000 条 URL 且文件不超过 50MB；超限需用 sitemap 索引文件拆分。",
   "URL 必须是绝对地址且可被爬虫访问；含非 ASCII 需做百分号编码。",
   "生成后放到站点根目录并在 robots.txt 声明 Sitemap 路径，再到搜索引擎后台提交。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 结构</h3>
  <pre class="code-box" style="white-space:pre;font-size:12px;">&lt;urlset xmlns=\".../0.9\"&gt;\n  &lt;url&gt;&lt;loc&gt;https://x/&lt;/loc&gt;&lt;/url&gt;\n&lt;/urlset&gt;</pre>
</div>
"""
},
{
 "slug":"color-blindness-sim","industry":"design","cat":"design","icon":"👁️","bg":"#eef2ff","accent":"#6366F1","indicon":"🎨",
 "title":"色盲模拟器",
 "h1":"色盲模拟器",
 "h2":"👁️ 色盲模拟器",
 "desc":"色盲模拟器 - 输入一个颜色，按红/绿/蓝三型色觉缺陷的矩阵模拟其在色盲眼中的显示，检查配色可达性。纯前端本地计算。",
 "intro":"约 8% 男性有色觉缺陷。输入颜色，本工具用近似色盲矩阵变换 RGB，预览红绿蓝三类色盲下的观感，帮助校验对比与辨识度。",
 "inputs":[
   {"id":"hex","label":"颜色 HEX","type":"text","value":"#FF5733"},
   {"id":"type","label":"色盲类型","type":"select","opts":[["pro","红色盲 Protanopia"],["deu","绿色盲 Deuteranopia"],["tri","蓝色盲 Tritanopia"]]}
 ],
 "calc":"""
function h2r(h){h=h.replace('#','');if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];return [parseInt(h.substr(0,2),16),parseInt(h.substr(2,2),16),parseInt(h.substr(4,2),16)];}
function toHex(r,g,b){function p(x){var s=Math.max(0,Math.min(255,Math.round(x))).toString(16);return s.length<2?'0'+s:s;}return '#'+p(r)+p(g)+p(b);}
var M={pro:[[0.567,0.433,0],[0.558,0.442,0],[0,0.242,0.758]],deu:[[0.625,0.375,0],[0.7,0.3,0],[0,0.3,0.7]],tri:[[0.95,0.05,0],[0,0.433,0.567],[0,0.475,0.525]]};
var hex=document.getElementById('hex').value.trim();
var type=document.getElementById('type').value;
var m=/^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.exec(hex);
var html='<div class="result-title">模拟结果</div>';
if(!m){html+='<p style="color:#dc2626;">⚠️ 请输入有效 HEX 颜色。</p>';document.getElementById('result').innerHTML=html;return;}
var c=h2r(hex),mtx=M[type];
var r=c[0]*mtx[0][0]+c[1]*mtx[0][1]+c[2]*mtx[0][2];
var g=c[0]*mtx[1][0]+c[1]*mtx[1][1]+c[2]*mtx[1][2];
var b=c[0]*mtx[2][0]+c[1]*mtx[2][1]+c[2]*mtx[2][2];
var out=toHex(r,g,b);
html+='<div class="data-grid">';
html+='<div class="data-card"><div class="num" style="background:'+hex+';color:'+hex+';">·</div><div class="label">'+escH(hex)+' 原色</div></div>';
html+='<div class="data-card"><div class="num" style="background:'+out+';color:'+out+';">·</div><div class="label">'+out+' 模拟</div></div>';
html+='</div>';
html+='<p class="muted" style="margin-top:8px;">类型：'+(type==='pro'?'红色盲':type==='deu'?'绿色盲':'蓝色盲')+'（近似矩阵）。</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "色盲模拟仅为近似：真实色觉缺陷因人而异，矩阵法（Machado/Brettel）更精细，本工具用简化线性变换。",
   "设计可达性应以 WCAG 对比度为准（正文≥4.5:1）；不要只依赖色盲模拟，更要保证文字与背景对比充分。",
   "避免「仅靠颜色」传达信息（如图表图例），应叠加形状/文字标签。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 WCAG 对比度</h3>
  <table class="ref-table">
    <tr><th>场景</th><th>要求</th></tr>
    <tr><td>正文</td><td>≥ 4.5:1</td></tr>
    <tr><td>大字</td><td>≥ 3:1</td></tr>
    <tr><td>图形</td><td>≥ 3:1</td></tr>
  </table>
</div>
"""
},
{
 "slug":"nginx-config-generator","industry":"it","cat":"dev","icon":"🪙","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Nginx 配置生成器",
 "h1":"Nginx 配置生成器",
 "h2":"🪙 Nginx 配置生成器",
 "desc":"Nginx 配置生成器 - 选择静态站点或反向代理场景，填入域名、端口、根目录等，生成可用 server 块配置。纯前端本地生成。",
 "intro":"Nginx 常用于托管静态站点或反向代理后端。选择场景并填参数，本工具生成标准 server 块，复制到站点配置即可启用。",
 "inputs":[
   {"id":"mode","label":"场景","type":"select","opts":[["static","静态站点"],["proxy","反向代理"]]},
   {"id":"domain","label":"域名（server_name）","type":"text","value":"example.com"},
   {"id":"root","label":"静态根目录 / 代理上游","type":"text","value":"/var/www/html"},
   {"id":"port","label":"监听端口","value":"80","step":"1","min":"1"}
 ],
 "calc":"""
var mode=document.getElementById('mode').value;
var domain=document.getElementById('domain').value.trim()||'_';
var root=document.getElementById('root').value.trim()||'/var/www/html';
var port=Math.floor(num('port'))||80;
var cfg;
if(mode==='static'){
  cfg='server {\\n  listen '+port+';\\n  server_name '+domain+';\\n  root '+root+';\\n  index index.html;\\n  location / {\\n    try_files $uri $uri/ =404;\\n  }\\n}';
}else{
  cfg='server {\\n  listen '+port+';\\n  server_name '+domain+';\\n  location / {\\n    proxy_pass '+root+';\\n    proxy_set_header Host $host;\\n    proxy_set_header X-Real-IP $remote_addr;\\n  }\\n}';
}
var html='<div class="result-title">nginx 配置</div>';
html+='<pre class="code-box" style="white-space:pre;font-size:12.5px;overflow-x:auto;">'+escH(cfg)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "反向代理的 proxy_pass 末尾是否带 / 影响路径拼接：带 / 会剥离 location 前缀，按需选择。",
   "配置改完用 nginx -t 校验语法，再 nginx -s reload 生效，避免写错导致服务中断。",
   "生产应补 TLS（listen 443 ssl）、gzip、缓存头等；本工具只生成最小可用骨架。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常用指令</h3>
  <table class="ref-table">
    <tr><th>指令</th><th>作用</th></tr>
    <tr><td>try_files</td><td>静态回退</td></tr>
    <tr><td>proxy_pass</td><td>转发上游</td></tr>
    <tr><td>nginx -t</td><td>校验语法</td></tr>
  </table>
</div>
"""
},
{
 "slug":"kubernetes-yaml-generator","industry":"it","cat":"dev","icon":"☸️","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Kubernetes YAML 生成器",
 "h1":"Kubernetes YAML 生成器",
 "h2":"☸️ Kubernetes YAML 生成器",
 "desc":"Kubernetes YAML 生成器 - 填应用名、镜像、端口与副本数，生成 Deployment + Service 清单，便于 kubectl apply。纯前端本地生成。",
 "intro":"部署到 K8s 通常需 Deployment 与 Service 两份清单。填入关键参数，本工具拼出标准 YAML，复制到集群即可 apply。",
 "inputs":[
   {"id":"name","label":"应用名","type":"text","value":"web"},
   {"id":"image","label":"镜像","type":"text","value":"nginx:latest"},
   {"id":"port","label":"容器端口","value":"80","step":"1","min":"1"},
   {"id":"replicas","label":"副本数","value":"2","step":"1","min":"1"}
 ],
 "calc":"""
var name=document.getElementById('name').value.trim()||'app';
var image=document.getElementById('image').value.trim()||'nginx:latest';
var port=Math.floor(num('port'))||80;
var rep=Math.max(1,Math.floor(num('replicas')));
var y='apiVersion: apps/v1\\nkind: Deployment\\nmetadata:\\n  name: '+name+'\\nspec:\\n  replicas: '+rep+'\\n  selector:\\n    matchLabels:\\n      app: '+name+'\\n  template:\\n    metadata:\\n      labels:\\n        app: '+name+'\\n    spec:\\n      containers:\\n      - name: '+name+'\\n        image: '+image+'\\n        ports:\\n        - containerPort: '+port+'\\n---\\napiVersion: v1\\nkind: Service\\nmetadata:\\n  name: '+name+'\\nspec:\\n  selector:\\n    app: '+name+'\\n  ports:\\n  - port: '+port+'\\n    targetPort: '+port+'\\n  type: ClusterIP\\n';
var html='<div class="result-title">k8s 清单</div>';
html+='<pre class="code-box" style="white-space:pre;font-size:12px;overflow-x:auto;">'+escH(y)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "image: latest 不利于回滚与可重现部署，生产应锁定具体版本/tag 或 digest。",
   "Service 的 targetPort 须与容器 containerPort 一致；对外暴露需改 type: NodePort/LoadBalancer 或接 Ingress。",
   "生成后 kubectl apply -f 部署；变更镜像建议走滚动更新与探针（liveness/readiness）保障可用性。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 清单结构</h3>
  <p>Deployment（副本/镜像）+ Service（暴露）；用 <code>---</code> 分隔多文档。资源限制（resources）、探针建议另行补充。</p>
</div>
"""
},
{
 "slug":"meta-tags-generator","industry":"it","cat":"dev","icon":"🏷️","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Meta 标签生成器",
 "h1":"Meta 标签生成器",
 "h2":"🏷️ Meta 标签生成器",
 "desc":"Meta 标签生成器 - 填标题、描述、图片与站点地址，生成 SEO 与社交分享（Open Graph / Twitter Card）所需的 meta 标签。纯前端本地生成。",
 "intro":"社交平台分享链接时靠 OG/Twitter 标签渲染卡片。填入页面信息，本工具生成完整 meta 片段，粘到 <head> 即可提升分享展示。",
 "inputs":[
   {"id":"title","label":"页面标题","type":"text","value":"我的网站"},
   {"id":"desc","label":"页面描述","type":"text","value":"一个用 ToolBox 构建的工具站"},
   {"id":"url","label":"页面 URL","type":"text","value":"https://example.com/"},
   {"id":"img","label":"分享图片 URL","type":"text","value":"https://example.com/og.png"}
 ],
 "calc":"""
var t=document.getElementById('title').value.trim();
var d=document.getElementById('desc').value.trim();
var u=document.getElementById('url').value.trim();
var img=document.getElementById('img').value.trim();
var L=[];
L.push('<title>'+t+'</title>');
L.push('<meta name=\"description\" content=\"'+d+'\">');
L.push('<meta property=\"og:title\" content=\"'+t+'\">');
L.push('<meta property=\"og:description\" content=\"'+d+'\">');
L.push('<meta property=\"og:type\" content=\"website\">');
L.push('<meta property=\"og:url\" content=\"'+u+'\">');
L.push('<meta property=\"og:image\" content=\"'+img+'\">');
L.push('<meta name=\"twitter:card\" content=\"summary_large_image\">');
L.push('<meta name=\"twitter:title\" content=\"'+t+'\">');
L.push('<meta name=\"twitter:description\" content=\"'+d+'\">');
L.push('<meta name=\"twitter:image\" content=\"'+img+'\">');
var html='<div class="result-title">Meta 标签</div>';
html+='<pre class="code-box" style="white-space:pre;font-size:12px;overflow-x:auto;">'+escH(L.join('\\n'))+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "OG 图片建议 1200×630 像素、小于 1MB，过小的图在部分平台不展示大卡。",
   "og:type 文章用 article、视频用 video.other；本工具默认 website。",
   "改完可用社交平台调试器（如 Facebook Sharing Debugger）预览卡片抓取效果。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 关键字段</h3>
  <table class="ref-table">
    <tr><th>字段</th><th>用途</th></tr>
    <tr><td>og:title</td><td>分享标题</td></tr>
    <tr><td>og:image</td><td>分享图</td></tr>
    <tr><td>twitter:card</td><td>大图卡</td></tr>
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
                  '<input type="checkbox" id="top_%s" value="%s">%s</label>'%(o[0],o[0],o[1])
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
