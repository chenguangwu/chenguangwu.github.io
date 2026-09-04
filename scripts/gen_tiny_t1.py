#!/usr/bin/env python3
"""Tiny Helpers 对标 · 6 个高价值工具（tools/it/）：位运算计算器 / ASCII 目录树 / clamp 计算器 / box-shadow 生成器 / CAA 记录生成器 / HTML 嵌套检查器。
用法：python3 scripts/gen_tiny_t1.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'tools', 'it')
os.makedirs(OUT_DIR, exist_ok=True)

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=dev,industry=it,icon=__ICON__,bg=__BG__">
<title>__TITLE__ - ToolBox</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="https://chenguangwu.github.io/tools/it/__FN__">
<meta property="og:title" content="__TITLE__ - ToolBox">
<meta property="og:description" content="__DESC__">
<meta property="og:type" content="website">
<meta property="og:url" content="https://chenguangwu.github.io/tools/it/__FN__">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="__TITLE__ - ToolBox">
<meta name="twitter:description" content="__DESC__">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<link rel="stylesheet" href="../../css/common.css">
<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard','copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool','toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script><!-- TOOLBOX-API-STUB -->
<script src="../../js/common.js" defer></script>
</head>
<body>
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ __TITLE__</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>
<div class="container">
  <div class="card">
    <h2>__ICON__ __TITLE__</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">__DESC__</p>
__BODY__
  </div>
</div>
<script>
__SCRIPT__
</script>
</body>
</html>
'''

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

TOOLS = []

def gen(fn, icon, bg, title, desc, body, script):
    html = (TPL.replace('__ICON__', icon).replace('__BG__', bg)
        .replace('__TITLE__', esc(title)).replace('__DESC__', esc(desc))
        .replace('__FN__', fn).replace('__BODY__', body).replace('__SCRIPT__', script))
    open(os.path.join(OUT_DIR, fn), 'w', encoding='utf-8').write(html)
    print('OK:', os.path.join(OUT_DIR, fn))

# ============ 1. 位运算计算器 ============
TOOLS.append(dict(
    fn='bitwise-calculator.html', icon='🧮', bg='#eef2ff',
    title='位运算计算器',
    desc='32 位位运算计算器：AND/OR/XOR/NOT/左移/右移，支持十进制/十六进制/二进制输入，实时可视化位翻转。',
    body='''    <div class="input-row">
      <div><label>数值 A</label><input type="text" id="a" placeholder="如 255、0xff、0b1111" oninput="calc()"></div>
      <div><label>运算</label>
        <select id="op" onchange="calc()">
          <option value="AND">AND 与</option><option value="OR">OR 或</option>
          <option value="XOR">XOR 异或</option><option value="NOT">NOT 取反</option>
          <option value="SHL">&lt;&lt; 左移</option><option value="SHR">&gt;&gt; 右移</option>
        </select>
      </div>
      <div><label>数值 B</label><input type="text" id="b" placeholder="如 240" oninput="calc()"></div>
    </div>
    <div class="result-box" id="result"></div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:14px;margin-bottom:12px;">
      <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:6px;">结果（32 位可视化）</div>
      <div id="bitsOut" style="font-family:monospace;font-size:15px;line-height:2;word-break:break-all;"></div>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="calc()">计算</button>
      <button class="btn" onclick="copyRes()">复制结果</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function parseNum(s){
  s=String(s).trim().toLowerCase().replace(/_/g,'');
  if(!s)return NaN;
  if(/^0x/.test(s))return parseInt(s,16);
  if(/^0b/.test(s))return parseInt(s.slice(2),2);
  if(/^0o/.test(s))return parseInt(s.slice(2),8);
  return parseInt(s,10);
}
function toBits(v){
  var b='';
  for(var i=31;i>=0;i--)b+=((v>>>i)&1)===1?'1':'0';
  return b;
}
function copyRes(){var v=document.getElementById('resVal');if(!v||v.textContent==='—'){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v.textContent);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function calc(){
  var op=document.getElementById('op').value;
  var va=parseNum(document.getElementById('a').value);
  var vb=parseNum(document.getElementById('b').value);
  var out=document.getElementById('result');
  var bits=document.getElementById('bitsOut');
  if(op==='NOT'){if(isNaN(va)){out.innerHTML='<p style="color:var(--danger)">请输入数值 A</p>';bits.innerHTML='';return;}}
  else if(isNaN(va)||isNaN(vb)){out.innerHTML='<p style="color:var(--danger)">请输入有效的数值（支持 255 / 0xff / 0b1111）</p>';bits.innerHTML='';return;}
  var r;
  switch(op){
    case 'AND':r=va&vb;break;case 'OR':r=va|vb;break;case 'XOR':r=va^vb;break;
    case 'NOT':r=~va;break;case 'SHL':r=(va<<(vb&31))|0;break;case 'SHR':r=va>>(vb&31);break;
  }
  var unsigned=r>>>0;
  var b=toBits(unsigned);
  bits.innerHTML='<div style="color:var(--muted,#6B7280);font-size:12px;">'+escH(b.slice(0,8))+' <span style="opacity:.5">|</span> '+escH(b.slice(8,16))+' <span style="opacity:.5">|</span> '+escH(b.slice(16,24))+' <span style="opacity:.5">|</span> '+escH(b.slice(24))+'</div>';
  var resDec=(r<0)?r.toString():String(unsigned);
  out.innerHTML='<p>结果：<strong id="resVal" style="font-size:22px;color:var(--primary);font-family:monospace;">'+resDec+'</strong> '+
    '<span style="font-size:13px;color:var(--muted,#6B7280);">= 0x'+unsigned.toString(16).toUpperCase()+' = 0b'+unsigned.toString(2)+'</span></p>';
}'''))

# ============ 2. ASCII 目录树生成器 ============
TOOLS.append(dict(
    fn='ascii-tree-generator.html', icon='🌳', bg='#f0fdf4',
    title='ASCII 目录树生成器',
    desc='把路径列表一键生成 ASCII 目录树（├── └── │ 风格），支持文件/文件夹标记，复制进 README 或文档。',
    body='''    <div class="input-row">
      <textarea id="paths" placeholder="每行一个路径，如：&#10;src/index.js&#10;src/components/Button.js&#10;src/utils/format.js&#10;README.md" style="min-height:180px" oninput="build()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:220px;font-family:'SF Mono','Courier New',monospace;font-size:12.5px;" placeholder="生成的 ASCII 目录树将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="build()">生成</button>
      <button class="btn" onclick="copyOut()">复制</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function build(){
  var lines=document.getElementById('paths').value.split(/\\r?\\n/).map(function(s){return s.replace(/^\\s+|\\s+$/g,'');}).filter(Boolean);
  var out=document.getElementById('result');
  if(!lines.length){document.getElementById('output').value='';out.innerHTML='';return;}
  var tree={};
  lines.forEach(function(l){
    var parts=l.split('/');
    var node=tree;
    parts.forEach(function(p,idx){
      if(!p)return;
      var isFile=idx===parts.length-1;
      if(!node[p])node[p]={_file:isFile,_children:{}};
      if(!isFile)node=node[p]._children;
    });
  });
  var outLines=[];
  function render(node,prefix,isRoot){
    var keys=Object.keys(node);
    keys.forEach(function(k,idx){
      var isLast=idx===keys.length-1;
      var isFile=node[k]._file;
      var connector=isRoot?'':(isLast?'└── ':'├── ');
      outLines.push(prefix+connector+k+(isFile?'':'/'));
      if(!isFile){
        var childPrefix=prefix+(isRoot?'':(isLast?'    ':'│   '));
        render(node[k]._children,childPrefix,false);
      }
    });
  }
  render(tree,'',true);
  document.getElementById('output').value=outLines.join('\\n');
  out.innerHTML='<p>✅ 已生成 <strong>'+outLines.length+'</strong> 行目录树（'+lines.length+' 个路径）</p>';
}'''))

# ============ 3. CSS clamp 计算器 ============
TOOLS.append(dict(
    fn='clamp-calculator.html', icon='📐', bg='#fef3e2',
    title='CSS clamp 计算器',
    desc='响应式字号 clamp() 计算器：输入最小/首选/最大字号与视口范围，生成流畅缩放表达式并实时预览。',
    body='''    <div class="input-row">
      <div><label>最小字号</label><input type="number" id="min" value="16" min="1" max="200" step="0.5" oninput="calc()"></div>
      <div><label>首选字号</label><input type="number" id="pref" value="24" min="1" max="200" step="0.5" oninput="calc()"></div>
      <div><label>最大字号</label><input type="number" id="max" value="48" min="1" max="300" step="0.5" oninput="calc()"></div>
    </div>
    <div class="input-row">
      <div><label>最小视口 (px)</label><input type="number" id="vwMin" value="375" min="200" max="2000" oninput="calc()"></div>
      <div><label>最大视口 (px)</label><input type="number" id="vwMax" value="1440" min="400" max="4000" oninput="calc()"></div>
    </div>
    <div class="result-box" id="result"></div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:14px;margin-bottom:12px;">
      <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:6px;">实时预览（拖动浏览器宽度观察字号变化）</div>
      <div id="preview" style="font-weight:700;color:var(--primary);">响应式字体效果预览</div>
      <input type="range" id="slider" min="320" max="1920" value="800" style="width:100%;margin-top:10px;" oninput="slide()">
      <div style="font-size:12px;color:var(--muted,#6B7280);margin-top:4px;">当前视口：<span id="vwNow">800</span>px</div>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="calc()">生成</button>
      <button class="btn" onclick="copyClamp()">复制 clamp()</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function fmt(n){return Math.round(n*100)/100;}
function calc(){
  var min=parseFloat(document.getElementById('min').value)||16;
  var pref=parseFloat(document.getElementById('pref').value)||24;
  var max=parseFloat(document.getElementById('max').value)||48;
  var vwMin=parseFloat(document.getElementById('vwMin').value)||375;
  var vwMax=parseFloat(document.getElementById('vwMax').value)||1440;
  if(vwMin>=vwMax){document.getElementById('result').innerHTML='<p style="color:var(--danger)">最小视口必须小于最大视口</p>';return;}
  var slope=(pref-min)/(vwMin/100);   // 每 100vw 增长 px
  var slope2=(max-min)/(vwMax/100);
  var vw=Math.max(slope,slope2);
  var rem=pref-vw*vwMin/100;
  var clamp='clamp('+fmt(min)+'px, '+fmt(vw)+'vw + '+fmt(rem)+'px, '+fmt(max)+'px)';
  document.getElementById('result').innerHTML=
    '<p>生成表达式：<code style="background:rgba(0,0,0,.05);padding:4px 10px;border-radius:8px;font-size:14px;">'+escH(clamp)+'</code></p>'+
    '<p style="font-size:12px;color:var(--muted,#6B7280);">斜率 '+fmt(vw)+'vw · 截距 '+fmt(rem)+'px · 视口 '+vwMin+'~'+vwMax+'px</p>';
  window._clamp=clamp;
  slide();
}
function slide(){
  var w=parseInt(document.getElementById('slider').value)||800;
  document.getElementById('vwNow').textContent=w;
  var min=parseFloat(document.getElementById('min').value)||16;
  var max=parseFloat(document.getElementById('max').value)||48;
  var vwMin=parseFloat(document.getElementById('vwMin').value)||375;
  var vwMax=parseFloat(document.getElementById('vwMax').value)||1440;
  var t=Math.max(0,Math.min(1,(w-vwMin)/(vwMax-vwMin)));
  var size=fmt(min+(max-min)*t);
  document.getElementById('preview').style.fontSize=size+'px';
}
function copyClamp(){
  if(!window._clamp){calc();if(!window._clamp){if(ToolBox.showToast)ToolBox.showToast('请先计算');return;}}
  ToolBox.copyText(window._clamp);
  if(ToolBox.showToast)ToolBox.showToast('已复制 '+window._clamp.slice(0,40)+'...');
}
calc();'''))

# ============ 4. Box-shadow 生成器 ============
TOOLS.append(dict(
    fn='box-shadow-generator.html', icon='🎛️', bg='#faf5ff',
    title='Box-shadow 生成器',
    desc='可视化 CSS box-shadow 生成器：偏移/模糊/扩散/颜色/内阴影实时调节，实时预览并复制 CSS 代码。',
    body='''    <div class="input-row">
      <div><label>X 偏移</label><input type="number" id="x" value="0" step="1" oninput="render()"></div>
      <div><label>Y 偏移</label><input type="number" id="y" value="4" step="1" oninput="render()"></div>
      <div><label>模糊</label><input type="number" id="blur" value="12" min="0" step="1" oninput="render()"></div>
      <div><label>扩散</label><input type="number" id="spread" value="0" step="1" oninput="render()"></div>
    </div>
    <div class="input-row">
      <div><label>颜色</label><input type="color" id="color" value="#1f2937" oninput="render()"></div>
      <div><label>透明度</label><input type="range" id="alpha" min="0" max="100" value="25" oninput="render()"></div>
      <label style="flex:0 0 auto;align-self:center;"><input type="checkbox" id="inset" onchange="render()"> 内阴影 (inset)</label>
    </div>
    <div class="result-box" id="result"></div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:16px;padding:40px;text-align:center;margin-bottom:14px;">
      <div id="target" style="width:140px;height:140px;background:var(--card,#fff);border-radius:16px;margin:0 auto;transition:box-shadow .1s;"></div>
    </div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:12px 14px;margin-bottom:12px;">
      <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:4px;">CSS 代码</div>
      <div id="cssOut" style="font-family:monospace;font-size:13px;word-break:break-all;">—</div>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="copyCss()">复制 CSS</button>
      <button class="btn" onclick="reset()">重置</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyCss(){var v=document.getElementById('cssOut').textContent;if(!v||v==='—'){if(ToolBox.showToast)ToolBox.showToast('请先调节');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制 CSS');}
function reset(){['x','y','blur','spread'].forEach(function(id,i){document.getElementById(id).value=[0,4,12,0][i];});document.getElementById('color').value='#1f2937';document.getElementById('alpha').value=25;document.getElementById('inset').checked=false;render();}
function hexToRgba(hex,a){
  var h=hex.replace('#','');
  if(h.length===3)h=h.split('').map(function(c){return c+c;}).join('');
  var n=parseInt(h,16);
  return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+(a/100).toFixed(2)+')';
}
function render(){
  var x=parseInt(document.getElementById('x').value)||0;
  var y=parseInt(document.getElementById('y').value)||0;
  var blur=parseInt(document.getElementById('blur').value)||0;
  var spread=parseInt(document.getElementById('spread').value)||0;
  var color=document.getElementById('color').value;
  var alpha=parseInt(document.getElementById('alpha').value)||0;
  var inset=document.getElementById('inset').checked;
  var rgba=hexToRgba(color,alpha);
  var css='box-shadow: '+(inset?'inset ':'')+x+'px '+y+'px '+blur+'px '+spread+'px '+rgba+';';
  document.getElementById('target').style.boxShadow=(inset?'inset ':'')+x+'px '+y+'px '+blur+'px '+spread+'px '+rgba;
  document.getElementById('cssOut').textContent=css;
  document.getElementById('result').innerHTML='<p>偏移 <strong>'+x+'px '+y+'px</strong> · 模糊 <strong>'+blur+'px</strong> · 扩散 <strong>'+spread+'px</strong> · '+(inset?'内阴影':'外阴影')+' · 透明度 '+alpha+'%</p>';
}
render();'''))

# ============ 5. CAA 记录生成器 ============
TOOLS.append(dict(
    fn='caa-record-generator.html', icon='🛡️', bg='#ecfdf5',
    title='CAA 记录生成器',
    desc='生成 DNS CAA 记录：指定域名与允许的证书颁发机构，输出标准 CAA 资源记录，防止证书误签发。',
    body='''    <div class="input-row">
      <div><label>域名</label><input type="text" id="domain" placeholder="如 example.com" style="flex:2" oninput="gen()"></div>
      <div><label>签发标志</label>
        <select id="flag" onchange="gen()">
          <option value="0">0（默认）</option><option value="128">128（关键）</option>
        </select>
      </div>
    </div>
    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">允许的 CA：</span>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ca_google" checked onchange="gen()"> Google Trust Services</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ca_lets" checked onchange="gen()"> Let\'s Encrypt</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ca_digicert" onchange="gen()"> DigiCert</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ca_comodo" onchange="gen()"> Sectigo/Comodo</label>
    </div>
    <div class="input-row" style="align-items:center;">
      <label style="flex:0 0 auto;"><input type="checkbox" id="opt_iodef" onchange="gen()"> 添加 iodef（违规报告邮箱）</label>
      <input type="email" id="iodefEmail" placeholder="security@example.com" style="flex:1;display:none;" oninput="gen()">
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:140px;font-family:'SF Mono','Courier New',monospace;font-size:13px;" placeholder="生成的 CAA 记录将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="gen()">生成</button>
      <button class="btn" onclick="copyOut()">复制记录</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 CAA（Certification Authority Authorization）限制哪些 CA 可为你的域名签发证书。添加后证书签发机构会检查该记录。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('请先填写域名');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制 CAA 记录');}
function gen(){
  var d=document.getElementById('domain').value.trim().replace(/^\\.+|\\s+$/g,'');
  var flag=document.getElementById('flag').value;
  var out=document.getElementById('result');
  var iodef=document.getElementById('opt_iodef');
  document.getElementById('iodefEmail').style.display=iodef.checked?'block':'none';
  if(!d){document.getElementById('output').value='';out.innerHTML='';return;}
  var recs=[];
  if(document.getElementById('ca_google').checked)recs.push(flag+' issue "pki.goog"');
  if(document.getElementById('ca_lets').checked)recs.push(flag+' issue "letsencrypt.org"');
  if(document.getElementById('ca_digicert').checked)recs.push(flag+' issue "digicert.com"');
  if(document.getElementById('ca_comodo').checked)recs.push(flag+' issue "sectigo.com"');
  if(iodef.checked){
    var em=document.getElementById('iodefEmail').value.trim();
    recs.push(flag+' iodef "mailto:'+(em||'security@example.com')+'"');
  }
  if(!recs.length){document.getElementById('output').value='';out.innerHTML='<p style="color:var(--warning)">请至少选择一个 CA</p>';return;}
  var lines=recs.map(function(r){return d+'  CAA  '+r;});
  document.getElementById('output').value=lines.join('\\n');
  out.innerHTML='<p>✅ 已生成 <strong>'+recs.length+'</strong> 条 CAA 记录（粘贴到 DNS 服务商）</p>';
}'''))

# ============ 6. HTML 标签嵌套检查器 ============
TOOLS.append(dict(
    fn='html-nesting-checker.html', icon='🧬', bg='#fdf2f8',
    title='HTML 嵌套检查器',
    desc='检查 HTML 标签嵌套是否合法：未闭合标签、错误嵌套、隐式闭合，报告问题行号与修复建议。',
    body='''    <div class="input-row">
      <textarea id="html" placeholder='粘贴 HTML，如：<div><p>文本</div>' style="min-height:200px;font-family:'SF Mono','Courier New',monospace;font-size:13px;" oninput="check()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <div id="report" style="font-size:13px;line-height:1.9;"></div>
    <div class="toolbar">
      <button class="btn primary" onclick="check()">检查</button>
    </div>''',
    script='''var VOID=/^(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr)$/i;
var RAW=/^(script|style|textarea|title)$/i;
function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function check(){
  var src=document.getElementById('html').value;
  var out=document.getElementById('result');
  var rep=document.getElementById('report');
  if(!src.trim()){out.innerHTML='';rep.innerHTML='';return;}
  var stack=[],errors=[],i=0;
  var tagRe=/<\\/?([a-zA-Z][a-zA-Z0-9-]*)((?:\\s[^>]*)?)>/g;
  var m,pos=0,line=1;
  while((m=tagRe.exec(src))!==null){
    var before=src.slice(pos,m.index);
    line+=before.split('\\n').length-1;
    var name=m[1],isClose=m[0][1]==='/';
    if(isClose){
      if(RAW.test(name)&&m[0].indexOf('</')===0){continue;}
      if(stack.length===0){errors.push('第 '+line+' 行：多余的闭合标签 </'+name+'>');}
      else{
        var idx=-1;
        for(var k=stack.length-1;k>=0;k--){if(stack[k].name.toLowerCase()===name.toLowerCase()){idx=k;break;}}
        if(idx===-1){errors.push('第 '+line+' 行：</'+name+'> 与未打开的标签不匹配');}
        else{
          for(var j=stack.length-1;j>idx;j--){
            errors.push('第 '+line+' 行：</'+name+'> 闭合时，<'+stack[j].name+'> 未显式闭合（隐式闭合）');
          }
          stack.length=idx;
        }
      }
    }else{
      if(!VOID.test(name)&&!RAW.test(name)){
        if(/\\/>$/.test(m[0]))continue; // 自闭合
        stack.push({name:name,line:line});
      }
    }
    pos=tagRe.lastIndex;
    line=1; // 已按 before 累计
    // 重新基于 m.index 计算行号（简单方式）
  }
  // 简化行号修正：整体重算
  errors=[];
  stack=[];
  var re=/<\\/?([a-zA-Z][a-zA-Z0-9-]*)((?:\\s[^>]*)?)>/g;
  var mm,prev=0,curLine=1;
  while((mm=re.exec(src))!==null){
    var seg=src.slice(prev,mm.index);
    curLine+=seg.split('\\n').length-1;
    prev=re.lastIndex;
    var nm=mm[1],cl=mm[0][1]==='/';
    if(cl){
      if(stack.length===0){errors.push('第 '+curLine+' 行：多余的闭合标签 </'+nm+'>');continue;}
      var ix=-1;
      for(var q=stack.length-1;q>=0;q--){if(stack[q].name.toLowerCase()===nm.toLowerCase()){ix=q;break;}}
      if(ix===-1){errors.push('第 '+curLine+' 行：</'+nm+'> 与未打开的标签不匹配');}
      else{
        for(var w=stack.length-1;w>ix;w--){errors.push('第 '+curLine+' 行：<'+stack[w].name+'> 被隐式闭合（</'+nm+'> 闭合了它）');}
        stack.length=ix;
      }
    }else{
      if(!VOID.test(nm)&&!RAW.test(nm)&&!/\\/>$/.test(mm[0]))stack.push({name:nm,line:curLine});
    }
  }
  stack.forEach(function(s){errors.push('第 '+s.line+' 行：<'+s.name+'> 未闭合');});
  if(!errors.length){
    out.innerHTML='<p style="color:var(--success)">✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签）</p>';
    rep.innerHTML='';
  }else{
    out.innerHTML='<p style="color:var(--danger)">❌ 发现 <strong>'+errors.length+'</strong> 个问题：</p>';
    rep.innerHTML='<div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:12px 14px;">'+errors.map(function(e){return '<div>⚠️ '+escH(e)+'</div>';}).join('')+'</div>';
  }
}'''))

def main():
    for t in TOOLS:
        gen(t['fn'], t['icon'], t['bg'], t['title'], t['desc'], t['body'], t['script'])
    print(f'\\nTiny Helpers 对标 6 个工具已生成 → {OUT_DIR}')

if __name__ == '__main__':
    main()
