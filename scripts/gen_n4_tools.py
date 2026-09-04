#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N4-02 首批 A 级工具生成器（批次 01：it 行业 5 个交互式工具）。
参照 scripts/gen_civil_eng_tools.py 模板化范式，但 body/script 为自定义交互式布局。

用法：python3 scripts/gen_n4_tools.py
生成 5 个工具页（幂等，覆盖写）：
  tools/it/url-params.html            URL 参数解析器
  tools/it/image-to-base64.html       图片转 Base64
  tools/it/csv-to-html-table.html     CSV 转 HTML 表格
  tools/it/line-ending-converter.html 换行符转换器
  tools/it/code-line-counter.html     代码行数统计
"""
import os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
IT_ZH = "IT 开发"
BASE = "https://chenguangwu.github.io"

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
<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard','copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool','toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script><!-- TOOLBOX-API-STUB -->
<script src="../../js/common.js" defer></script>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"__BASE__/"},{"@type":"ListItem","position":2,"name":"__CATZH__","item":"__BASE__/tools/__INDUSTRY__/index.html"},{"@type":"ListItem","position":3,"name":"__TITLE__","item":"__BASE__/tools/__INDUSTRY__/__SLUG__.html"}]}
</script>

<meta property="og:image" content="__BASE__/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">
<meta name="twitter:image" content="__BASE__/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">
    <meta property="og:type" content="website">
    <meta name="twitter:title" content="__TITLE__">
    <meta name="twitter:description" content="__DESC__">

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"__TITLE__","url":"__BASE__/tools/__INDUSTRY__/__SLUG__.html","applicationCategory":"DeveloperApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","description":"__TITLE__","image":"__BASE__/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}
</script>

<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
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
  <a href="index.html">💻 __CATZH__</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">__TITLE__</span>
</nav>
<div class="container">
  <div class="card tool-card-accent" style="--tool-accent:__ACCENT__;">
    <h2>__H2__</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">__INTRO__</p>

__BODY__

  </div>

<!-- 注意事项区块 -->
<div class="tool-notes" style="--tool-accent:__ACCENT__;">
  <div class="tool-notes-title">⚠️ 使用说明与注意事项</div>
  <ul>
      <li>本工具纯前端运行，数据不会上传到服务器</li>
      <li>建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用</li>
      <li>处理结果请自行核对后再用于生产环境</li>
  </ul>
</div>
<!-- /注意事项区块 -->
</div>

<script>
__SCRIPT__
</script>
</body>
</html>
"""

# ---------- 工具定义 ----------

TOOLS = [
# ============ 1. URL 参数解析器 ============
{
 "slug":"url-params","industry":"it","cat":"dev","icon":"🔗","bg":"#e0f2fe",
 "accent":"#0EA5E9",
 "title":"URL 参数解析器",
 "h1":"URL 参数解析器",
 "h2":"🔗 URL 参数解析器",
 "desc":"URL 参数解析器 - 解析 URL 的 query 参数为键值对，支持编辑/新增/删除并重新生成 URL。纯前端本地处理，数据不上传。",
 "intro":"粘贴一个带查询参数的 URL，自动拆解为键值对表格；可修改值、删除或新增参数，实时重新拼装 URL 并一键复制。",
 "body":"""
    <div style="margin-bottom:12px;">
      <label for="urlInput">目标 URL</label>
      <input type="text" id="urlInput" value="https://example.com/search?q=toolbox&lang=zh-CN&page=2" placeholder="https://example.com/path?a=1&b=2" oninput="calcTool()" style="font-size:14px;">
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
      <button type="button" class="btn" onclick="addParam()">+ 新增参数</button>
      <button type="button" class="btn primary" onclick="copyUrl()">复制新 URL</button>
      <button type="button" class="btn" onclick="copyParamsJson()">复制参数 JSON</button>
      <button type="button" class="btn" onclick="importJson()">从 JSON 导入</button>
      <button type="button" class="btn" onclick="toggleEncoding()" id="encBtn">值解码显示：开</button>
    </div>
    <div id="jsonImportBox" style="display:none;margin-bottom:12px;">
      <label for="jsonInput">参数 JSON（对象形式）</label>
      <textarea id="jsonInput" rows="4" spellcheck="false" placeholder='{"q":"toolbox","page":"2"}' style="font-family:'SF Mono',monospace;font-size:12.5px;"></textarea>
      <div style="margin-top:6px;">
        <button type="button" class="btn" onclick="applyJsonImport()">应用导入</button>
        <button type="button" class="btn" onclick="hideJsonImport()">取消</button>
      </div>
    </div>
    <div id="paramsBox"></div>
    <div class="result-box" id="result" style="margin-top:12px;"></div>
    <script id="paramRowTpl" type="text/template">
      <div class="param-row">
        <input type="text" class="p-key" placeholder="参数名" value="{k}" oninput="calcTool()">
        <span class="p-eq">=</span>
        <input type="text" class="p-val" placeholder="参数值" value="{v}" oninput="calcTool()">
        <button type="button" class="p-del" onclick="delParam(this)" aria-label="删除参数">✕</button>
      </div>
    </script>
    <style>
    .param-row{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap;}
    .param-row input{flex:1;min-width:120px;font-size:13px;padding:9px 12px;}
    .param-row .p-key{flex:0 1 36%;}
    .param-row .p-eq{color:var(--text-muted);}
    .p-del{width:36px;height:36px;border-radius:10px;border:1px solid var(--border);background:transparent;color:var(--danger);cursor:pointer;font-size:14px;flex:0 0 36px;}
    .p-del:hover{background:var(--bg-hover);}
    .out-url{font-family:'SF Mono','Courier New',monospace;font-size:13px;word-break:break-all;background:var(--result-bg);border:1px solid var(--border);border-radius:10px;padding:12px;}
    </style>
""",
 "script":r"""
var _decMode = true;
function esc(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}
function calcTool(){
  var raw=(document.getElementById('urlInput').value||'').trim();
  if(!raw){raw='https://example.com/search?q=toolbox&lang=zh-CN&page=2';}
  var qm=raw.indexOf('?');
  var base=qm>=0?raw.slice(0,qm):raw;
  var qs=qm>=0?raw.slice(qm+1):'';
  var pairs=[];
  if(qs){qs.split('&').forEach(function(p){if(!p)return;var i=p.indexOf('=');var k=i>=0?p.slice(0,i):p;var v=i>=0?p.slice(i+1):'';pairs.push({k:decodeURIComponent(k.replace(/\+/g,' ')),v:decodeURIComponent(v.replace(/\+/g,' '))});});}
  var box=document.getElementById('paramsBox');
  var tpl=document.getElementById('paramRowTpl').innerHTML;
  var out='';
  if(!pairs.length){out='<p class="tip-mini" style="color:var(--text-muted);">该 URL 无查询参数，可点击「新增参数」添加。</p>';}
  pairs.forEach(function(p){out+=tpl.replace('{k}',esc(p.k)).replace('{v}',esc(p.v));});
  box.innerHTML=out;
  renderUrl();
}
function renderUrl(){
  var base=document.getElementById('urlInput').value.split('?')[0];
  var rows=document.querySelectorAll('#paramsBox .param-row');
  var parts=[];
  rows.forEach(function(r){
    var k=r.querySelector('.p-key').value.trim();
    if(!k)return;
    var v=r.querySelector('.p-val').value;
    parts.push(encodeURIComponent(k).replace(/%20/g,'+')+'='+encodeURIComponent(v).replace(/%20/g,'+'));
  });
  var url=parts.length?base+'?'+parts.join('&'):base;
  document.getElementById('result').innerHTML='<div class="out-url">'+esc(url)+'</div>';
  return url;
}
function collectPairs(){
  var rows=document.querySelectorAll('#paramsBox .param-row');
  var out={};
  rows.forEach(function(r){
    var k=r.querySelector('.p-key').value.trim();
    if(!k)return;
    out[k]=r.querySelector('.p-val').value;
  });
  return out;
}
function copyParamsJson(){
  var obj=collectPairs();
  var json=JSON.stringify(obj,null,2);
  ToolBox.copyText(json,'参数 JSON 已复制','复制失败');
}
function importJson(){
  document.getElementById('jsonImportBox').style.display='block';
}
function hideJsonImport(){document.getElementById('jsonImportBox').style.display='none';}
function applyJsonImport(){
  var raw=document.getElementById('jsonInput').value.trim();
  var obj;
  try{obj=JSON.parse(raw);}catch(e){ToolBox.showToast('JSON 解析失败：'+e.message);return;}
  if(!obj||typeof obj!=='object'||Array.isArray(obj)){ToolBox.showToast('请输入对象形式的 JSON');return;}
  var box=document.getElementById('paramsBox');
  var tpl=document.getElementById('paramRowTpl').innerHTML;
  var out='';
  Object.keys(obj).forEach(function(k){out+=tpl.replace('{k}',esc(k)).replace('{v}',esc(String(obj[k])));});
  box.innerHTML=out;
  document.getElementById('jsonImportBox').style.display='none';
  document.getElementById('jsonInput').value='';
  renderUrl();
}
function toggleEncoding(){
  _decMode=!_decMode;
  document.getElementById('encBtn').textContent='值解码显示：'+( _decMode?'开':'关');
  calcTool();
}
function addParam(){
  var tpl=document.getElementById('paramRowTpl').innerHTML;
  document.getElementById('paramsBox').insertAdjacentHTML('beforeend',tpl.replace('{k}','').replace('{v}',''));
}
function delParam(btn){btn.parentElement.remove();renderUrl();}
function copyUrl(){
  var url=renderUrl();
  var ok=ToolBox.copyText(url,'复制成功','复制失败');
  if(ok){ToolBox.showToast('新 URL 已复制');}
}
calcTool();
""",
},
# ============ 2. 图片转 Base64 ============
{
 "slug":"image-to-base64","industry":"it","cat":"encode","icon":"🖼️","bg":"#fce7f3",
 "accent":"#EC4899",
 "title":"图片转 Base64",
 "h1":"图片转 Base64",
 "h2":"🖼️ 图片转 Base64",
 "desc":"图片转 Base64 - 将本地图片转换为 Base64 data URL，支持 PNG/JPG/WebP/GIF，纯前端本地处理，图片不上传。",
 "intro":"选择或拖入图片，本地转换为 Base64 编码字符串，可预览、查看大小并一键复制，适合内嵌图片到 HTML/CSS/小程序。",
 "body":"""
    <div id="dropZone" style="border:2px dashed var(--border);border-radius:14px;padding:26px 16px;text-align:center;cursor:pointer;margin-bottom:14px;transition:all .2s;">
      <div style="font-size:30px;margin-bottom:6px;">📁</div>
      <div style="font-size:14px;color:var(--text-light);">点击选择图片，或将图片拖拽到此处</div>
      <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">支持 PNG / JPG / WebP / GIF，建议 < 5MB</div>
      <input type="file" id="fileInput" accept="image/*" style="display:none;">
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
      <button type="button" class="btn" onclick="document.getElementById('fileInput').click()">选择图片</button>
      <button type="button" class="btn primary" onclick="copyBase64()">复制 Base64</button>
      <button type="button" class="btn" onclick="copyDataUrl()">复制 data:URL</button>
      <button type="button" class="btn" onclick="downloadImg()">下载图片</button>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px;padding:10px 14px;background:var(--result-bg);border:1px solid var(--border);border-radius:12px;">
      <label for="outFmt" style="margin:0;">输出 data:URL 前缀</label>
      <select id="outFmt" onchange="refreshDataUrl()" style="width:auto;padding:8px 12px;font-size:13px;">
        <option value="keep">保持原格式</option>
        <option value="png">强制 PNG</option>
        <option value="jpeg">强制 JPEG</option>
        <option value="webp">强制 WebP</option>
      </select>
    </div>
    <div style="border-top:1px solid var(--border);margin:14px 0;padding-top:14px;">
      <label for="b64TextInput">Base64 → 图片（粘贴解码预览）</label>
      <textarea id="b64TextInput" rows="4" spellcheck="false" placeholder="粘贴以 data:image/ 开头或纯 base64 的字符串" style="font-family:'SF Mono',monospace;font-size:12px;"></textarea>
      <div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;">
        <button type="button" class="btn" onclick="decodeB64()">解码预览</button>
        <button type="button" class="btn" onclick="document.getElementById('b64TextInput').value='';document.getElementById('b64PreviewBox').innerHTML='';">清空</button>
      </div>
      <div id="b64PreviewBox" style="margin-top:10px;"></div>
    </div>
    <div class="result-box" id="result"></div>
    <style>
    #dropZone.drag-over{border-color:var(--primary);background:var(--bg-active);}
    .b64-out{font-family:'SF Mono','Courier New',monospace;font-size:11px;word-break:break-all;background:var(--result-bg);border:1px solid var(--border);border-radius:10px;padding:12px;max-height:180px;overflow:auto;margin-top:8px;line-height:1.5;}
    .img-prev{max-width:160px;max-height:160px;border-radius:10px;border:1px solid var(--border);margin-top:8px;}
    .b64-stat{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;}
    .b64-stat span{font-size:12px;color:var(--text-light);background:var(--result-bg);border:1px solid var(--border);padding:5px 10px;border-radius:8px;}
    </style>
""",
 "script":r"""
var _b64='';var _dataUrl='';var _mime='image/png';
function init(){
  var dz=document.getElementById('dropZone');
  dz.addEventListener('click',function(){document.getElementById('fileInput').click();});
  dz.addEventListener('dragover',function(e){e.preventDefault();dz.classList.add('drag-over');});
  dz.addEventListener('dragleave',function(){dz.classList.remove('drag-over');});
  dz.addEventListener('drop',function(e){e.preventDefault();dz.classList.remove('drag-over');var f=e.dataTransfer.files&&e.dataTransfer.files[0];if(f)handleFile(f);});
  document.getElementById('fileInput').addEventListener('change',function(){var f=this.files&&this.files[0];if(f)handleFile(f);});
}
function fmtSize(bytes){
  if(bytes<1024)return bytes+' B';
  if(bytes<1024*1024)return (bytes/1024).toFixed(1)+' KB';
  return (bytes/(1024*1024)).toFixed(2)+' MB';
}
function buildDataUrl(mime,b64){return 'data:'+mime+';base64,'+b64;}
function currentDataUrl(){
  var fmt=document.getElementById('outFmt').value;
  var mime=_mime;
  if(fmt==='png')mime='image/png';
  else if(fmt==='jpeg')mime='image/jpeg';
  else if(fmt==='webp')mime='image/webp';
  return buildDataUrl(mime,_b64);
}
function refreshDataUrl(){
  if(!_b64)return;
  _dataUrl=currentDataUrl();
  var img=document.querySelector('.img-prev');
  if(img)img.src=_dataUrl;
  var out=document.querySelector('.b64-out');
  if(out)out.textContent=_dataUrl;
}
function handleFile(file){
  if(!file.type||file.type.indexOf('image/')!==0){ToolBox.setResult('result','<p class="tip-error">请选择图片文件（PNG/JPG/WebP/GIF）。</p>');return;}
  if(file.size>10*1024*1024){ToolBox.setResult('result','<p class="tip-error">图片超过 10MB，请压缩后再试。</p>');return;}
  var reader=new FileReader();
  reader.onload=function(e){
    _dataUrl=e.target.result;
    _b64=_dataUrl.split(',')[1]||'';
    _mime=file.type||'image/png';
    var img=new Image();
    img.onload=function(){showResult(file,img.width,img.height);};
    img.onerror=function(){showResult(file,0,0);};
    img.src=_dataUrl;
  };
  reader.onerror=function(){ToolBox.setResult('result','<p class="tip-error">读取文件失败，请重试。</p>');};
  reader.readAsDataURL(file);
}
function showResult(file,w,h){
  var kb=(file.size/1024).toFixed(1);
  var b64kb=(_b64.length*0.75/1024).toFixed(1);
  var expand=(_b64.length*0.75/file.size*100).toFixed(1);
  var mime=_mime||file.type||'image/png';
  var sizeTxt=(w&&h)?w+'×'+h+'px':'尺寸未知';
  _dataUrl=currentDataUrl();
  ToolBox.setResult('result',
    '<div style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start;">'+
      '<img class="img-prev" src="'+_dataUrl+'" alt="预览">'+
      '<div style="flex:1;min-width:220px;">'+
        '<div class="b64-stat"><span>类型 '+esc(mime)+'</span><span>尺寸 '+sizeTxt+'</span><span>原图 '+fmtSize(file.size)+'</span><span>Base64 '+fmtSize(_b64.length)+'</span><span>膨胀 '+expand+'%</span></div>'+
        '<div class="b64-out">'+esc(_dataUrl)+'</div>'+
      '</div>'+
    '</div>');
}
function copyBase64(){
  if(!_b64){ToolBox.showToast('请先选择图片');return;}
  ToolBox.copyText(_b64,'Base64 已复制','复制失败');
}
function copyDataUrl(){
  if(!_dataUrl){ToolBox.showToast('请先选择图片');return;}
  _dataUrl=currentDataUrl();
  ToolBox.copyText(_dataUrl,'data:URL 已复制','复制失败');
}
function downloadImg(){
  if(!_dataUrl){ToolBox.showToast('请先选择图片');return;}
  _dataUrl=currentDataUrl();
  var a=document.createElement('a');
  a.href=_dataUrl;
  a.download='toolbox-image.'+(_mime.split('/')[1]||'png');
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
function decodeB64(){
  var raw=document.getElementById('b64TextInput').value.trim();
  if(!raw){ToolBox.showToast('请先粘贴 Base64 字符串');return;}
  var dataUrl;
  if(raw.indexOf('data:image')===0){dataUrl=raw;}
  else{dataUrl='data:image/png;base64,'+raw;}
  var box=document.getElementById('b64PreviewBox');
  box.innerHTML='<div style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start;">'+
    '<img class="img-prev" src="'+esc(dataUrl)+'" alt="解码预览" onerror="this.style.display=\'none\';document.getElementById(\'b64Err\').style.display=\'block\';">'+
    '<div style="flex:1;min-width:200px;">'+
      '<div class="b64-stat"><span>字符数 '+raw.length+'</span><span>估算大小 '+fmtSize(Math.floor(raw.length*0.75))+'</span></div>'+
      '<div id="b64Err" style="display:none;color:var(--danger);font-size:13px;margin-top:6px;">解码失败：Base64 字符串无效或不是图片数据。</div>'+
    '</div></div>';
}
function calcTool(){if(!_dataUrl){ToolBox.setResult('result','<p style="color:var(--text-muted);font-size:13px;">请选择一张图片，转换结果会显示在这里。数据全程在本地处理，不会上传。</p>');}}
function esc(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}
init();calcTool();
""",
},
# ============ 3. CSV 转 HTML 表格 ============
{
 "slug":"csv-to-html-table","industry":"it","cat":"generate","icon":"📊","bg":"#dcfce7",
 "accent":"#10B981",
 "title":"CSV 转 HTML 表格",
 "h1":"CSV 转 HTML 表格",
 "h2":"📊 CSV 转 HTML 表格",
 "desc":"CSV 转 HTML 表格 - 将 CSV 数据解析为带边框的 HTML table 代码，支持自定义分隔符，实时预览。纯前端本地处理。",
 "intro":"粘贴 CSV 数据，自动解析（支持引号转义与换行），生成可直接使用的 HTML <table> 代码，右侧实时预览渲染效果。",
 "body":"""
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px;">
      <label for="sepSel">分隔符</label>
      <select id="sepSel" onchange="calcTool()" style="width:auto;padding:9px 12px;font-size:13px;">
        <option value=",">逗号 ,</option>
        <option value=";">分号 ;</option>
        <option value="&#9;">制表符 Tab</option>
        <option value="|">竖线 |</option>
      </select>
      <label style="margin-left:8px;display:inline-flex;align-items:center;gap:6px;cursor:pointer;"><input type="checkbox" id="withHeader" checked onchange="calcTool()" style="width:auto;"> 首行为表头</label>
      <button type="button" class="btn" style="margin-left:8px;" onclick="document.getElementById('csvFile').click()">读取 CSV 文件</button>
      <input type="file" id="csvFile" accept=".csv,.tsv,.txt" style="display:none;">
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;" class="csv-grid">
      <div class="text-block">
        <label for="csvInput">CSV 数据</label>
        <textarea id="csvInput" rows="10" spellcheck="false" style="font-family:'SF Mono',monospace;font-size:12.5px;" oninput="calcTool()">name,age,city
Alice,28,Shanghai
Bob,35,Beijing
Carol,31,Shenzhen</textarea>
      </div>
      <div class="text-block">
        <label>HTML 代码</label>
        <textarea id="htmlOut" rows="10" readonly spellcheck="false" style="font-family:'SF Mono',monospace;font-size:12.5px;background:var(--result-bg);"></textarea>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0;">
      <button type="button" class="btn primary" onclick="copyHtml()">复制 HTML 代码</button>
      <button type="button" class="btn" onclick="downloadHtml()">下载 .html 文件</button>
    </div>
    <div class="result-box" id="result" style="margin-bottom:12px;"></div>
    <div id="previewBox" style="overflow-x:auto;"></div>
    <style>
    .csv-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
    @media(max-width:700px){.csv-grid{grid-template-columns:1fr;}}
    .text-block textarea{width:100%;min-height:180px;resize:vertical;}
    table.csv-prev{border-collapse:collapse;width:100%;font-size:13px;background:#fff;}
    table.csv-prev th,table.csv-prev td{border:1px solid #d1d5db;padding:6px 10px;text-align:left;}
    table.csv-prev th{background:#f3f4f6;font-weight:600;}
    </style>
""",
 "script":r"""
function parseCSV(text,sep){
  text=(text||'').replace(/^\uFEFF/,'');
  var rows=[];var row=[];var field='';var inQ=false;
  for(var i=0;i<text.length;i++){
    var c=text.charAt(i);
    if(inQ){
      if(c==='"'){ if(text.charAt(i+1)==='"'){field+='"';i++;} else {inQ=false;} }
      else field+=c;
    }else{
      if(c==='"'){inQ=true;}
      else if(c===sep){row.push(field);field='';}
      else if(c==='\n'){row.push(field);rows.push(row);row=[];field='';}
      else if(c!=='\r'){field+=c;}
    }
  }
  if(field!==''||row.length){row.push(field);rows.push(row);}
  return rows.filter(function(r){return r.length>1||(r.length===1&&r[0].trim()!=='');});
}
function escH(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}
function calcTool(){
  var raw=(document.getElementById('csvInput').value||'').trim();
  if(!raw){raw='name,age,city\nAlice,28,Shanghai\nBob,35,Beijing';}
  var sep=document.getElementById('sepSel').value;
  var header=document.getElementById('withHeader').checked;
  var rows=parseCSV(raw,sep);
  if(!rows.length){document.getElementById('htmlOut').value='<!-- 空数据 -->';document.getElementById('previewBox').innerHTML='<p class="tip-mini" style="color:var(--text-muted);">未解析到有效数据。</p>';return;}
  var h='';
  var dataStart=0;
  if(header){dataStart=1;h='<table>\n  <thead>\n    <tr>\n';rows[0].forEach(function(c){h+='      <th>'+escH(c)+'</th>\n';});h+='    </tr>\n  </thead>\n  <tbody>\n';}
  else{h='<table>\n  <tbody>\n';}
  for(var i=dataStart;i<rows.length;i++){
    h+='    <tr>\n';
    rows[i].forEach(function(c){h+='      <td>'+escH(c)+'</td>\n';});
    h+='    </tr>\n';
  }
  var h= header?'  </tbody>\n</table>':'  </tbody>\n</table>';
  document.getElementById('htmlOut').value=h;
  document.getElementById('previewBox').innerHTML='<div style="font-size:12px;color:var(--text-muted);margin-bottom:6px;">预览（'+rows.length+' 行）</div>'+h;
  var cols=header&&rows.length>1?rows[0].length:rows[0].length;
  var dataRows=header?Math.max(0,rows.length-1):rows.length;
  document.getElementById('result').innerHTML=
    '<div style="display:flex;gap:10px;flex-wrap:wrap;">'+
      '<span class="stat-pill">数据行 <b style="color:var(--primary);">'+dataRows+'</b></span>'+
      '<span class="stat-pill">列数 <b style="color:var(--primary);">'+cols+'</b></span>'+
      '<span class="stat-pill">总行 <b style="color:var(--primary);">'+rows.length+'</b></span>'+
    '</div>';
}
function copyHtml(){
  var v=document.getElementById('htmlOut').value;
  if(!v||v.indexOf('table')<0){ToolBox.showToast('请先输入 CSV 数据');return;}
  ToolBox.copyText(v,'HTML 代码已复制','复制失败');
}
function downloadHtml(){
  var v=document.getElementById('htmlOut').value;
  if(!v||v.indexOf('table')<0){ToolBox.showToast('请先输入 CSV 数据');return;}
  var blob=new Blob(['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>CSV 表格</title><style>table{border-collapse:collapse;width:100%;font-size:14px;}th,td{border:1px solid #ccc;padding:6px 10px;text-align:left;}th{background:#f3f4f6;}</style></head><body>',v,'</body></html>'],{type:'text/html;charset=utf-8'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='csv-table.html';
  document.body.appendChild(a);
  a.click();
  setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},100);
}
document.getElementById('csvFile').addEventListener('change',function(){
  var f=this.files&&this.files[0];if(!f)return;
  var r=new FileReader();
  r.onload=function(e){
    document.getElementById('csvInput').value=e.target.result;
    var name=f.name.toLowerCase();
    if(name.indexOf('.tsv')>=0){document.getElementById('sepSel').value='\t';}
    calcTool();
  };
  r.readAsText(f);
});
calcTool();
""",
},
# ============ 4. 换行符转换器 ============
{
 "slug":"line-ending-converter","industry":"it","cat":"convert","icon":"↩️","bg":"#fef9c3",
 "accent":"#EAB308",
 "title":"换行符转换器",
 "h1":"换行符转换器",
 "h2":"↩️ 换行符转换器",
 "desc":"换行符转换器 - 检测并转换文本的换行符（CRLF / LF / CR），统计各类型数量，跨平台代码文件必用。纯前端本地处理。",
 "intro":"粘贴文本，自动统计 CRLF（Windows）、LF（Unix/macOS）、CR（老 Mac）三种换行符数量，一键转换为目标格式，解决跨平台文件乱码与 Git 换行告警。",
 "body":"""
    <div style="margin-bottom:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
      <label for="targetSel">目标换行符</label>
      <select id="targetSel" style="width:auto;padding:9px 12px;font-size:13px;">
        <option value="&#13;&#10;">CRLF（Windows）</option>
        <option value="&#10;" selected>LF（Unix / macOS）</option>
        <option value="&#13;">CR（老 Mac）</option>
      </select>
      <button type="button" class="btn" onclick="document.getElementById('leFile').click()">读取文本文件</button>
      <input type="file" id="leFile" accept=".txt,.csv,.json,.js,.py,.html,.css,.md,.xml,.sql,.log" style="display:none;">
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;" class="le-grid">
      <div class="text-block">
        <label for="leInput">原始文本</label>
        <textarea id="leInput" rows="10" spellcheck="false" style="font-family:'SF Mono',monospace;font-size:12.5px;" oninput="calcTool()">第一行&#13;&#10;第二行&#13;&#10;第三行</textarea>
      </div>
      <div class="text-block">
        <label for="leOutput">转换结果</label>
        <textarea id="leOutput" rows="10" readonly spellcheck="false" style="font-family:'SF Mono',monospace;font-size:12.5px;background:var(--result-bg);"></textarea>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0;">
      <button type="button" class="btn" onclick="calcTool()">转换</button>
      <button type="button" class="btn primary" onclick="copyLe()">复制结果</button>
      <button type="button" class="btn" onclick="copyRaw()">复制原始文本</button>
      <button type="button" class="btn" onclick="clearLe()">清空</button>
    </div>
    <div class="result-box" id="result"></div>
    <div style="margin-top:12px;">
      <label>检测详情</label>
      <div id="leDetail" class="result-box" style="font-size:12.5px;line-height:1.8;"></div>
    </div>
    <div style="margin-top:12px;">
      <label>换行符可视化（前 8 处）</label>
      <div id="leViz" class="result-box" style="font-family:'SF Mono','Courier New',monospace;font-size:12px;line-height:1.7;word-break:break-all;"></div>
    </div>
    <style>
    .le-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
    @media(max-width:700px){.le-grid{grid-template-columns:1fr;}}
    .text-block textarea{width:100%;min-height:180px;resize:vertical;}
    .le-stat{display:inline-flex;gap:6px;align-items:center;font-size:12px;background:var(--result-bg);border:1px solid var(--border);border-radius:8px;padding:5px 10px;margin-right:8px;margin-bottom:6px;}
    .le-stat b{color:var(--primary);}
    </style>
""",
 "script":r"""
function countLE(s){
  var crlf=(s.match(/\r\n/g)||[]).length;
  var cr=(s.match(/\r(?!\n)/g)||[]).length;
  var lf=(s.match(/(?<!\r)\n/g)||[]).length;
  return {crlf:crlf,cr:cr,lf:lf};
}
function byteLen(s){
  var n=0;
  for(var i=0;i<s.length;i++){
    var c=s.charCodeAt(i);
    if(c<0x80)n+=1;
    else if(c<0x800)n+=2;
    else if(c>=0xD800&&c<0xDC00){n+=4;i++;}
    else n+=3;
  }
  return n;
}
function mainLE(c){
  var max=Math.max(c.crlf,c.lf,c.cr);
  if(max===0)return '无换行符';
  if(max===c.crlf)return 'CRLF (Windows)';
  if(max===c.lf)return 'LF (Unix/macOS)';
  return 'CR (老 Mac)';
}
function leViz(s){
  if(!s)return '';
  var out='',count=0;
  for(var i=0;i<s.length&&count<8;i++){
    var ch=s.charAt(i);
    var nxt=s.charAt(i+1);
    if(ch==='\r'&&nxt==='\n'){out+='<mark style="background:#fde68a;padding:0 2px;border-radius:3px;">\\r\\n</mark>';i++;count++;}
    else if(ch==='\n'){out+='<mark style="background:#bbf7d0;padding:0 2px;border-radius:3px;">\\n</mark>';count++;}
    else if(ch==='\r'){out+='<mark style="background:#fecaca;padding:0 2px;border-radius:3px;">\\r</mark>';count++;}
    else{out+=ch.replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/&/g,'&amp;');}
  }
  if(count>=8)out+=' …';
  return out||'<span style="color:var(--text-muted);">（空文本）</span>';
}
function calcTool(){
  var raw=document.getElementById('leInput').value||'';
  if(!raw){raw='line1\nline2\nline3';}
  var target=document.getElementById('targetSel').value;
  var c=countLE(raw);
  var total=c.crlf+c.cr+c.lf;
  var out=raw.replace(/\r\n|\r|\n/g,target);
  document.getElementById('leOutput').value=out;
  var h='';
  h+='<span class="le-stat">CRLF <b>'+c.crlf+'</b></span>';
  h+='<span class="le-stat">LF <b>'+c.lf+'</b></span>';
  h+='<span class="le-stat">CR <b>'+c.cr+'</b></span>';
  h+='<span class="le-stat">总换行 <b>'+total+'</b></span>';
  if(!total){h+='<p class="tip-mini" style="color:var(--text-muted);margin-top:4px;">文本中未检测到换行符。</p>';}
  document.getElementById('result').innerHTML=h;
  var det='<b>主换行符：</b>'+mainLE(c)+'　<b>文本行数：</b>'+(total?total+1:1)+'　<b>字符数：</b>'+raw.length+'　<b>UTF-8 大小：</b>'+byteLen(raw)+' B';
  det+='<br><b>转换说明：</b>已将所有换行符统一替换为所选目标格式，跨平台粘贴/提交不再错乱。';
  document.getElementById('leDetail').innerHTML=det;
  document.getElementById('leViz').innerHTML=leViz(raw);
}
function copyLe(){
  var v=document.getElementById('leOutput').value;
  if(!v){ToolBox.showToast('请先输入文本');return;}
  ToolBox.copyText(v,'转换结果已复制','复制失败');
}
function copyRaw(){
  var v=document.getElementById('leInput').value;
  if(!v){ToolBox.showToast('请先输入文本');return;}
  ToolBox.copyText(v,'原始文本已复制','复制失败');
}
function clearLe(){
  document.getElementById('leInput').value='';
  document.getElementById('leOutput').value='';
  document.getElementById('result').innerHTML='';
  document.getElementById('leDetail').innerHTML='';
}
document.getElementById('leFile').addEventListener('change',function(){
  var f=this.files&&this.files[0];if(!f)return;
  var r=new FileReader();
  r.onload=function(e){document.getElementById('leInput').value=e.target.result;calcTool();};
  r.readAsText(f);
});
calcTool();
""",
},
# ============ 5. 代码行数统计 ============
{
 "slug":"code-line-counter","industry":"it","cat":"text","icon":"📄","bg":"#e0f2fe",
 "accent":"#0EA5E9",
 "title":"代码行数统计",
 "h1":"代码行数统计",
 "h2":"📄 代码行数统计",
 "desc":"代码行数统计 - 按语言识别注释规则统计代码总行、代码行、注释行与空行，支持 C/JS/Python/HTML/SQL 等。纯前端本地处理。",
 "intro":"粘贴代码或选择代码文件，自动按扩展名匹配语言注释规则（//、/* */、#、<!-- -->、-- 等），统计总行数、代码行、注释行与空行。",
 "body":"""
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px;">
      <label for="langSel">语言</label>
      <select id="langSel" onchange="calcTool()" style="width:auto;padding:9px 12px;font-size:13px;">
        <option value="auto">自动识别（按扩展名）</option>
        <option value="js">JavaScript / TypeScript</option>
        <option value="c">C / C++ / Java / Go / Rust</option>
        <option value="py">Python</option>
        <option value="html">HTML / XML</option>
        <option value="sql">SQL</option>
        <option value="sh">Shell / Bash</option>
        <option value="css">CSS / SCSS</option>
      </select>
      <button type="button" class="btn" onclick="document.getElementById('codeFile').click()">选择文件</button>
      <input type="file" id="codeFile" accept=".js,.ts,.c,.cpp,.java,.go,.rs,.py,.html,.xml,.sql,.sh,.bash,.css,.scss,.json,.md" style="display:none;">
    </div>
    <div class="text-block">
      <label for="codeInput">代码</label>
      <textarea id="codeInput" rows="12" spellcheck="false" style="font-family:'SF Mono',monospace;font-size:12.5px;" oninput="calcTool()">/**
 * 示例：计算两数之和
 */
function add(a, b) {
  // 返回和
  return a + b;
}

// 空行上方是一个空行
console.log(add(1, 2));</textarea>
    </div>
    <div style="margin-top:12px;" id="result"></div>
    <style>
    .code-stat{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-top:4px;}
    .code-stat .cs{background:var(--result-bg);border:1px solid var(--border);border-radius:12px;padding:12px;text-align:center;}
    .code-stat .cs .n{font-size:24px;font-weight:700;color:var(--primary);}
    .code-stat .cs .l{font-size:12px;color:var(--text-light);margin-top:2px;}
    .code-stat .cs.total .n{color:var(--text);}
    .code-stat .cs.comment .n{color:var(--accent,#10B981);}
    .code-stat .cs.blank .n{color:var(--text-muted);}
    </style>
""",
 "script":r"""
var LANGS={
  js:{ext:['js','ts','jsx','tsx','mjs','cjs'],line:['//'],block:[['/*','*/']],string:[['"','"'],["'","'"],['`','`']]},
  c:{ext:['c','cpp','h','hpp','java','go','rs','swift','kt','cs'],line:['//'],block:[['/*','*/']],string:[['"','"'],["'","'"],['`','`']]},
  py:{ext:['py'],line:['#'],block:[['\x22\x22\x22','\x22\x22\x22'],["'''","'''"]],string:[['"','"'],["'","'"],['\x22\x22\x22','\x22\x22\x22'],["'''","'''"]]},
  html:{ext:['html','xml','svg','vue','jsx','tsx'],line:[],block:[['<!--','-->']],string:[['"','"'],["'","'"]]},
  sql:{ext:['sql'],line:['--'],block:[['/*','*/']],string:[['"','"'],["'","'"]]},
  sh:{ext:['sh','bash','zsh'],line:['#'],block:[],string:[['"','"'],["'","'"]]},
  css:{ext:['css','scss','less'],line:[],block:[['/*','*/']],string:[]}
};
function detectLang(fname){
  var ext=(fname.split('.').pop()||'').toLowerCase();
  for(var k in LANGS){if(LANGS[k].ext.indexOf(ext)>=0)return k;}
  return 'js';
}
function isInStr(chunks,i,lang){
  var strs=LANGS[lang]?LANGS[lang].string:[];
  for(var s=0;s<strs.length;s++){
    var a=strs[s][0],b=strs[s][1];
    var c0=chunks[i],c1=chunks[i+1];
    if(a.length>1){if((c0+c1).indexOf(a)===0)return true;}else if(c0===a)return true;
    if(b&&b.length>1){if((c0+c1).indexOf(b)===0)return true;}else if(b&&c0===b)return true;
  }
  return false;
}
function calcTool(){
  var raw=document.getElementById('codeInput').value||'';
  if(!raw){raw='// demo\nfunction f(){\n  return 1;\n}\n\n/* done */';}
  var sel=document.getElementById('langSel').value;
  var lang=sel==='auto'?'js':sel;
  var lineRules=LANGS[lang]?LANGS[lang].line:[];
  var blockRules=LANGS[lang]?LANGS[lang].block:[];
  var lines=raw.split('\n');
  var total=lines.length,code=0,comment=0,blank=0;
  var inBlock=false;
  for(var i=0;i<lines.length;i++){
    var line=lines[i];
    if(!line.trim()){blank++;continue;}
    var t=line.trim();
    var isComment=false;
    if(inBlock){comment++;var endAt=-1;for(var b=0;b<blockRules.length;b++){var idx=t.indexOf(blockRules[b][1]);if(idx>=0){endAt=Math.max(endAt,idx);}}if(endAt>=0){inBlock=false;t=t.slice(endAt+2).trim();isComment=t===''?true:false;}else{continue;}}
    if(!isComment){
      for(var l=0;l<lineRules.length;l++){if(t.indexOf(lineRules[l])===0){isComment=true;break;}}
    }
    if(!isComment&&!inBlock){
      for(var b2=0;b2<blockRules.length;b2++){
        var s=blockRules[b2][0],e=blockRules[b2][1];
        var si=t.indexOf(s);
        if(si>=0){var rest=t.slice(si+2);if(rest.indexOf(e)<0){inBlock=true;}isComment=true;break;}
      }
    }
    if(isComment){comment++;}else{code++;}
  }
  var ratio=total?(code/total*100).toFixed(1):'0';
  document.getElementById('result').innerHTML=
    '<div class="code-stat">'+
      '<div class="cs total"><div class="n">'+total+'</div><div class="l">总行数</div></div>'+
      '<div class="cs"><div class="n">'+code+'</div><div class="l">代码行</div></div>'+
      '<div class="cs comment"><div class="n">'+comment+'</div><div class="l">注释行</div></div>'+
      '<div class="cs blank"><div class="n">'+blank+'</div><div class="l">空行</div></div>'+
      '<div class="cs"><div class="n">'+ratio+'%</div><div class="l">代码占比</div></div>'+
    '</div>';
}
document.getElementById('codeFile').addEventListener('change',function(){
  var f=this.files&&this.files[0];if(!f)return;
  var r=new FileReader();
  r.onload=function(e){
    document.getElementById('codeInput').value=e.target.result;
    if(document.getElementById('langSel').value==='auto'){
      var l=detectLang(f.name);
      var map={'js':0,'c':1,'py':2,'html':3,'sql':4,'sh':5,'css':6};
      document.getElementById('langSel').selectedIndex=map[l]||0;
    }
    calcTool();
  };
  r.readAsText(f);
});
calcTool();
""",
},
]

# ---------- 渲染 ----------

def render(t):
    body = t["body"]
    # 归一化缩进：去掉 body 每行的前导空行
    lines = body.strip("\n").split("\n")
    # 找出最小公共缩进（忽略空行）
    indents = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
    pad = min(indents) if indents else 0
    body = "\n".join(l[pad:] if l.strip() else "" for l in lines)
    return (TEMPLATE
            .replace("__CAT__", t["cat"])
            .replace("__INDUSTRY__", t["industry"])
            .replace("__ICON__", t["icon"])
            .replace("__BG__", t["bg"])
            .replace("__ACCENT__", t["accent"])
            .replace("__SLUG__", t["slug"])
            .replace("__TITLE__", H.escape(t["title"]))
            .replace("__H1__", H.escape(t["h1"]))
            .replace("__H2__", H.escape(t["h2"]))
            .replace("__INTRO__", H.escape(t["intro"]))
            .replace("__DESC__", H.escape(t["desc"]))
            .replace("__CATZH__", IT_ZH)
            .replace("__BASE__", BASE)
            .replace("__BODY__", body)
            .replace("__SCRIPT__", t["script"].strip()))


def main():
    count = 0
    for t in TOOLS:
        out_dir = os.path.join(TOOLS_DIR, t["industry"])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, t["slug"] + ".html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(t))
        count += 1
        print("  + tools/%s/%s.html" % (t["industry"], t["slug"]))
    print("共生成 %d 个工具页" % count)


if __name__ == "__main__":
    main()
