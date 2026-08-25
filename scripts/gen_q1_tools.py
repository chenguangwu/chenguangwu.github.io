#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 批次 01 生成器：6 个 it-tools 风格转换/生成类 A 级工具。
复用 gen_n4b_tools 的 TEMPLATE 范式（inputs + calcTool），扩展 __REF__ 参考表占位。
用法：python3 scripts/gen_q1_tools.py
生成（行业/文件）：
  design/px-to-rem.html         px 转 rem
  design/rem-to-px.html         rem 转 px
  design/flexbox-generator.html Flexbox 布局生成器
  design/vh-vw.html             视口单位转换（vh/vw ↔ px）
  it/text-to-ascii.html         文本转 ASCII / 二进制
  it/text-to-unicode.html       文本转 Unicode 码点
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
 "slug":"px-to-rem","industry":"design","cat":"design","icon":"📐","bg":"#eef2ff","accent":"#6366F1","indicon":"🎨",
 "title":"px 转 rem 计算器",
 "h1":"px 转 rem 计算器",
 "h2":"📐 px 转 rem 计算器",
 "desc":"px 转 rem 计算器 - 输入像素值与根字号（root font-size），一键把 px 换算成 rem，并给出常用尺寸速查表。纯前端本地计算。",
 "intro":"rem 是相对根元素字体大小的单位，做响应式与可访问性友好的布局时常用来替代写死的 px。输入像素值与根字号，立即得到 rem 值。",
 "inputs":[
   {"id":"px","label":"像素值（px）","value":"16","step":"1","min":"0"},
   {"id":"root","label":"根字号 root（px）","value":"16","step":"1","min":"1"}
 ],
 "calc":"""
var px=num('px'); var root=num('root'); if(root<=0){root=16;}
var rem=px/root;
var html='<div class="result-title">转换结果</div>';
html+='<div class="big-result">'+px+'px = <b>'+rem.toFixed(4)+'rem</b></div>';
html+='<p class="muted">基准根字号 root font-size = '+root+'px（1rem = '+root+'px）</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "rem 相对于根元素（<html>）的 font-size；修改根字号即可整体缩放页面，便于响应式与无障碍。",
   "浏览器默认根字号为 16px，很多团队会把 :root 设为 62.5%（即 10px）让 1rem=10px 方便心算。",
   "结果保留 4 位小数，实际使用时通常取 2–3 位（如 1.5rem）。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📏 常用尺寸速查表（root = 16px）</h3>
  <table class="ref-table">
    <tr><th>px</th><th>rem</th><th>常见用途</th></tr>
    <tr><td>8</td><td>0.5</td><td>小间距 / 描边</td></tr>
    <tr><td>12</td><td>0.75</td><td>辅助文字</td></tr>
    <tr><td>14</td><td>0.875</td><td>正文小字</td></tr>
    <tr><td>16</td><td>1</td><td>正文基准</td></tr>
    <tr><td>20</td><td>1.25</td><td>小标题</td></tr>
    <tr><td>24</td><td>1.5</td><td>标题 / 间距</td></tr>
    <tr><td>32</td><td>2</td><td>区块标题</td></tr>
    <tr><td>48</td><td>3</td><td>大标题</td></tr>
    <tr><td>64</td><td>4</td><td>页面主标题</td></tr>
  </table>
  <p>若采用 62.5% 根字号方案（1rem=10px），上表 rem 值直接除以 1.6 即可，例如 16px→1.6rem、24px→2.4rem。</p>
</div>
"""
},
{
 "slug":"rem-to-px","industry":"design","cat":"design","icon":"📏","bg":"#eef2ff","accent":"#6366F1","indicon":"🎨",
 "title":"rem 转 px 计算器",
 "h1":"rem 转 px 计算器",
 "h2":"📏 rem 转 px 计算器",
 "desc":"rem 转 px 计算器 - 输入 rem 值与根字号（root font-size），一键把 rem 换算回 px，并给出常用尺寸速查表。纯前端本地计算。",
 "intro":"当你拿到一份以 rem 为单位的标注或设计稿，需要换算成 px 落地到固定尺寸场景时，用本工具按当前根字号反算。",
 "inputs":[
   {"id":"rem","label":"rem 值","value":"1","step":"0.01","min":"0"},
   {"id":"root","label":"根字号 root（px）","value":"16","step":"1","min":"1"}
 ],
 "calc":"""
var rem=num('rem'); var root=num('root'); if(root<=0){root=16;}
var px=rem*root;
var html='<div class="result-title">转换结果</div>';
html+='<div class="big-result">'+rem+'rem = <b>'+px.toFixed(2)+'px</b></div>';
html+='<p class="muted">基准根字号 root font-size = '+root+'px（1rem = '+root+'px）</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "px = rem × 根字号；根字号改变时同一 rem 对应的 px 会整体变化。",
   "固定尺寸场景（如海报、原生 App 内嵌 WebView）常用 px；自适应网页推荐 rem。",
   "结果四舍五入到 2 位小数。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📏 常用尺寸速查表（root = 16px）</h3>
  <table class="ref-table">
    <tr><th>rem</th><th>px</th><th>常见用途</th></tr>
    <tr><td>0.5</td><td>8</td><td>小间距 / 描边</td></tr>
    <tr><td>0.75</td><td>12</td><td>辅助文字</td></tr>
    <tr><td>0.875</td><td>14</td><td>正文小字</td></tr>
    <tr><td>1</td><td>16</td><td>正文基准</td></tr>
    <tr><td>1.25</td><td>20</td><td>小标题</td></tr>
    <tr><td>1.5</td><td>24</td><td>标题 / 间距</td></tr>
    <tr><td>2</td><td>32</td><td>区块标题</td></tr>
    <tr><td>3</td><td>48</td><td>大标题</td></tr>
    <tr><td>4</td><td>64</td><td>页面主标题</td></tr>
  </table>
  <p>若采用 62.5% 根字号方案（1rem=10px），上表 px 值 = rem × 10，例如 1.6rem→16px、2.4rem→24px。</p>
</div>
"""
},
{
 "slug":"flexbox-generator","industry":"design","cat":"design","icon":"🧩","bg":"#f5f3ff","accent":"#7C3AED","indicon":"🎨",
 "title":"Flexbox 布局生成器",
 "h1":"Flexbox 布局生成器",
 "h2":"🧩 Flexbox 布局生成器",
 "desc":"Flexbox 布局生成器 - 可视化选择主轴方向、对齐方式、换行与间距，实时生成可复制的 CSS 代码与预览。纯前端本地处理。",
 "intro":"Flexbox 是现代 CSS 布局的核心。选择几个关键属性，立即得到对应的 display:flex CSS，并看到 1/2/3 三个项目的实时排列效果。",
 "inputs":[
   {"id":"dir","label":"flex-direction 主轴方向","type":"select","opts":[["row","row（水平）"],["row-reverse","row-reverse"],["column","column（垂直）"],["column-reverse","column-reverse"]]},
   {"id":"just","label":"justify-content 主轴对齐","type":"select","opts":[["flex-start","flex-start"],["center","center"],["flex-end","flex-end"],["space-between","space-between"],["space-around","space-around"],["space-evenly","space-evenly"]]},
   {"id":"ali","label":"align-items 交叉轴对齐","type":"select","opts":[["stretch","stretch"],["flex-start","flex-start"],["center","center"],["flex-end","flex-end"],["baseline","baseline"]]},
   {"id":"wrap","label":"flex-wrap 换行","type":"select","opts":[["nowrap","nowrap"],["wrap","wrap"],["wrap-reverse","wrap-reverse"]]},
   {"id":"gap","label":"gap 间距（px）","value":"12","step":"1","min":"0"}
 ],
 "calc":"""
var d=document.getElementById('dir').value;
var j=document.getElementById('just').value;
var a=document.getElementById('ali').value;
var w=document.getElementById('wrap').value;
var g=document.getElementById('gap').value||'0';
var css='.box {\\n  display: flex;\\n  flex-direction: '+d+';\\n  justify-content: '+j+';\\n  align-items: '+a+';\\n  flex-wrap: '+w+';\\n  gap: '+g+'px;\\n}';
var html='<div class="result-title">生成的 CSS</div><pre class="code-block">'+escH(css)+'</pre>';
html+='<div class="result-title">实时预览（3 个项目）</div>';
html+='<div class="flex-prev" style="display:flex;flex-direction:'+d+';justify-content:'+j+';align-items:'+a+';flex-wrap:'+w+';gap:'+g+'px;">';
html+='<div class="fp-item">1</div><div class="fp-item">2</div><div class="fp-item">3</div></div>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "justify-content 控制主轴（由 flex-direction 决定水平或垂直）上的对齐与分布。",
   "align-items 控制交叉轴上的对齐；stretch 会让项目拉伸填满交叉轴。",
   "flex-wrap:wrap 允许换行，配合 gap 可快速实现自适应网格。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>🧩 flex 属性速查</h3>
  <table class="ref-table">
    <tr><th>属性</th><th>常用取值</th><th>说明</th></tr>
    <tr><td>flex-direction</td><td>row / column / row-reverse / column-reverse</td><td>主轴方向</td></tr>
    <tr><td>justify-content</td><td>flex-start / center / flex-end / space-between / space-around / space-evenly</td><td>主轴对齐</td></tr>
    <tr><td>align-items</td><td>stretch / flex-start / center / flex-end / baseline</td><td>交叉轴对齐</td></tr>
    <tr><td>flex-wrap</td><td>nowrap / wrap / wrap-reverse</td><td>是否换行</td></tr>
    <tr><td>gap</td><td>任意长度（如 12px）</td><td>项目间距</td></tr>
  </table>
  <p>提示：要让单个项目在交叉轴居中可用 <code>align-self</code>；要控制项目伸缩用 <code>flex: 1</code> 或 <code>flex-grow/shrink/basis</code>。</p>
</div>
"""
},
{
 "slug":"vh-vw","industry":"design","cat":"design","icon":"📺","bg":"#ecfeff","accent":"#06B6D4","indicon":"🎨",
 "title":"视口单位转换（vh / vw ↔ px）",
 "h1":"视口单位转换（vh / vw ↔ px）",
 "h2":"📺 视口单位转换（vh / vw ↔ px）",
 "desc":"视口单位转换 - 在 vw/vh 与 px 之间按视口宽高互转，支持 px→vw、px→vh、vw→px、vh→px 四种模式。纯前端本地计算。",
 "intro":"vw = 视口宽度的 1%，vh = 视口高度的 1%。做全屏首屏、自适应间距时常用来替代写死的 px。选择模式并填入基准视口尺寸即可换算。",
 "inputs":[
   {"id":"mode","label":"转换模式","type":"select","opts":[["px2vw","px → vw（按宽度）"],["px2vh","px → vh（按高度）"],["vw2px","vw → px（按宽度）"],["vh2px","vh → px（按高度）"]]},
   {"id":"val","label":"数值","value":"100","step":"1","min":"0"},
   {"id":"base","label":"基准视口尺寸（px，宽或高视模式而定）","value":"1920","step":"1","min":"1"}
 ],
 "calc":"""
var mode=document.getElementById('mode').value;
var v=num('val'); var base=num('base'); if(base<=0){base=1920;}
var out='', tip='';
if(mode==='px2vw'){ out=(v/base*100).toFixed(4)+'vw'; tip='按视口宽度 '+base+'px 计算'; }
else if(mode==='px2vh'){ out=(v/base*100).toFixed(4)+'vh'; tip='按视口高度 '+base+'px 计算'; }
else if(mode==='vw2px'){ out=(v/100*base).toFixed(2)+'px'; tip='按视口宽度 '+base+'px 计算'; }
else { out=(v/100*base).toFixed(2)+'px'; tip='按视口高度 '+base+'px 计算'; }
var html='<div class="result-title">转换结果</div>';
html+='<div class="big-result">'+v+' → <b>'+out+'</b></div>';
html+='<p class="muted">'+tip+'</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "vw 永远基于视口【宽度】，vh 永远基于视口【高度】，二者互不相干。",
   "移动端注意：部分浏览器的 vh 包含地址栏高度，可用 dvh/svh/lvh 等动态视口单位更精准。",
   "100vw 在大屏可能超出预期并引发横向滚动，用于全宽时建议配合 overflow-x:hidden。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📺 常见视口断点参考</h3>
  <table class="ref-table">
    <tr><th>设备</th><th>宽度（px）</th><th>典型 vw 示例</th></tr>
    <tr><td>手机</td><td>360–414</td><td>100vw ≈ 360–414px</td></tr>
    <tr><td>平板</td><td>768–1024</td><td>50vw ≈ 384–512px</td></tr>
    <tr><td>笔记本</td><td>1280–1440</td><td>50vw ≈ 640–720px</td></tr>
    <tr><td>桌面</td><td>1920</td><td>50vw = 960px</td></tr>
  </table>
  <p>换算公式：vw = px ÷ 视口宽度 × 100；px = vw ÷ 100 × 视口宽度（vh 同理用高度）。</p>
</div>
"""
},
{
 "slug":"text-to-ascii","industry":"it","cat":"dev","icon":"🔤","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"文本转 ASCII 码 / 二进制",
 "h1":"文本转 ASCII 码 / 二进制",
 "h2":"🔤 文本转 ASCII 码 / 二进制",
 "desc":"文本转 ASCII 码 / 二进制 - 输入文本，逐字符列出字符、十进制 ASCII、十六进制与 8 位二进制。纯前端本地处理。",
 "intro":"在编码、调试、教学场景常需要查看字符的底层数值。输入任意文本，立即得到每个字符的 ASCII 十进制、十六进制与二进制表示（仅 ASCII 范围内字符，非 ASCII 会被跳过并提示）。",
 "inputs":[
   {"id":"txt","label":"输入文本","type":"textarea","rows":"4","value":"Hello, ToolBox!"}
 ],
 "calc":"""
var s=document.getElementById('txt').value||'';
if(!s){ document.getElementById('result').innerHTML='<p class="muted">请输入文本</p>'; return; }
var rows=[], skipped=0;
for(var i=0;i<s.length;i++){
  var c=s.charAt(i); var code=c.charCodeAt(0);
  if(code>127){ skipped++; continue; }
  var bin=code.toString(2); while(bin.length<8){bin='0'+bin;}
  rows.push([escH(c===' '?'·(空格)':c), code, '0x'+code.toString(16).toUpperCase(), bin]);
}
var html='<div class="result-title">逐字符编码（ASCII 0–127）</div>';
html+='<table class="ref-table"><tr><th>字符</th><th>十进制</th><th>十六进制</th><th>二进制</th></tr>';
for(var k=0;k<rows.length;k++){ html+='<tr><td>'+rows[k][0]+'</td><td>'+rows[k][1]+'</td><td>'+rows[k][2]+'</td><td><code>'+rows[k][3]+'</code></td></tr>'; }
html+='</table>';
if(skipped>0){ html+='<p class="muted">已跳过 '+skipped+' 个非 ASCII 字符（码点 >127，如中文），本表仅显示 ASCII 可打印/控制字符。</p>'; }
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "标准 ASCII 仅定义 0–127；128–255 为扩展 ASCII（依赖编码页），Unicode 汉字等不在此表。",
   "空格显示为「·(空格)」便于核对；换行/制表符会显示其控制字符码点。",
   "二进制固定为 8 位（1 字节）表示。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>🔤 常用 ASCII 可打印字符（32–126）</h3>
  <table class="ref-table">
    <tr><th>字符</th><th>十进制</th><th>十六进制</th><th>字符</th><th>十进制</th><th>十六进制</th></tr>
    <tr><td>空格</td><td>32</td><td>20</td><td>@</td><td>64</td><td>40</td></tr>
    <tr><td>!</td><td>33</td><td>21</td><td>A</td><td>65</td><td>41</td></tr>
    <tr><td>0</td><td>48</td><td>30</td><td>a</td><td>97</td><td>61</td></tr>
    <tr><td>9(制表)</td><td>57</td><td>39</td><td>z</td><td>122</td><td>7A</td></tr>
    <tr><td>:</td><td>58</td><td>3A</td><td>{</td><td>123</td><td>7B</td></tr>
    <tr><td>A</td><td>65</td><td>41</td><td>~</td><td>126</td><td>7E</td></tr>
  </table>
  <p>大写字母 A–Z = 65–90，小写 a–z = 97–122，数字 0–9 = 48–57，二者相差 32（异或 0x20 可互转）。</p>
</div>
"""
},
{
 "slug":"text-to-unicode","industry":"it","cat":"dev","icon":"🔣","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"文本转 Unicode 码点",
 "h1":"文本转 Unicode 码点",
 "h2":"🔣 文本转 Unicode 码点",
 "desc":"文本转 Unicode 码点 - 输入文本，逐字符（含中文/emoji）列出 Unicode 码点与 UTF-16 转义。纯前端本地处理。",
 "intro":"查看任意字符（包括中文、emoji、符号）的 Unicode 码点是调试国际化文本、字体与编码问题的常用操作。输入文本立即得到每个码点的 U+ 表示。",
 "inputs":[
   {"id":"txt","label":"输入文本","type":"textarea","rows":"4","value":"你好 ToolBox 🚀"}
 ],
 "calc":"""
var s=document.getElementById('txt').value||'';
if(!s){ document.getElementById('result').innerHTML='<p class="muted">请输入文本</p>'; return; }
var html='<div class="result-title">逐字符 Unicode 码点</div>';
html+='<table class="ref-table"><tr><th>字符</th><th>码点</th><th>UTF-16 转义</th></tr>';
var arr=Array.from(s);
for(var i=0;i<arr.length;i++){
  var c=arr[i]; var cp=c.codePointAt(0);
  var hex='U+'+cp.toString(16).toUpperCase();
  while(hex.length<hex.indexOf('+')+5){ hex=hex.slice(0,hex.indexOf('+')+1)+'0'+hex.slice(hex.indexOf('+')+1); }
  var utf16='\\\\u'+c.charCodeAt(0).toString(16).toUpperCase();
  while(utf16.length<6){ utf16='\\\\u0'+utf16.slice(2); }
  html+='<tr><td>'+escH(c)+'</td><td><code>'+hex+'</code></td><td><code>'+utf16+'</code></td></tr>';
}
html+='</table>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "Unicode 码点用 U+ 加十六进制表示；基本多文种平面（BMP）为 U+0000–U+FFFF，emoji 等多在辅助平面（如 🚀 = U+1F680）。",
   "UTF-16 转义 \\uXXXX 仅覆盖 BMP；辅助平面字符需代理对（两个 \\u 序列）。",
   "逐字符遍历使用码点迭代（Array.from），避免把 emoji 拆成两个代理项。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>🔣 常用 Unicode 符号</h3>
  <table class="ref-table">
    <tr><th>字符</th><th>码点</th><th>含义</th></tr>
    <tr><td>—</td><td>U+2014</td><td>破折号 em dash</td></tr>
    <tr><td>·</td><td>U+00B7</td><td>中间点</td></tr>
    <tr><td>©</td><td>U+00A9</td><td>版权</td></tr>
    <tr><td>®</td><td>U+00AE</td><td>注册商标</td></tr>
    <tr><td>€</td><td>U+20AC</td><td>欧元</td></tr>
    <tr><td>★</td><td>U+2605</td><td>实心星</td></tr>
    <tr><td>✓</td><td>U+2713</td><td>对勾</td></tr>
    <tr><td>🚀</td><td>U+1F680</td><td>火箭 emoji</td></tr>
  </table>
  <p>中文常用汉字位于 U+4E00–U+9FFF（CJK 统一表意文字）区间。</p>
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
            else:
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <input type="number" id="%s" value="%s" step="%s">\n      </div>'%(f["id"],f["label"],f["id"],f["value"],f.get("step","1")))
        rows.append('    <div class="input-row">\n'+ "\n".join(cells)+'\n    </div>')
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
