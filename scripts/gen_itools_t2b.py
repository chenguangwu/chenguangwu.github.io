#!/usr/bin/env python3
"""it-tools 对标 · 优化点 4 个：Base64文件转换/二维码美化/任意进制互转/多算法哈希器。
用法：python3 scripts/gen_itools_t2b.py
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
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:type" content="website">
<meta property="og:url" content="https://chenguangwu.github.io/tools/it/__FN__">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESC__">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<link rel="stylesheet" href="../../css/common.css">
<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard','copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool','toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script><!-- TOOLBOX-API-STUB -->
<script src="../../js/common.js" defer></script>
__EXTRA_HEAD__
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

def gen(fn, icon, bg, title, desc, body, script, extra_head=''):
    html = (TPL
        .replace('__ICON__', icon).replace('__BG__', bg)
        .replace('__TITLE__', esc(title)).replace('__DESC__', esc(desc))
        .replace('__FN__', fn).replace('__BODY__', body)
        .replace('__SCRIPT__', script).replace('__EXTRA_HEAD__', extra_head))
    open(os.path.join(OUT_DIR, fn), 'w', encoding='utf-8').write(html)
    print('OK:', os.path.join(OUT_DIR, fn))

# ============ 1. Base64 文件转换 ============
TOOLS.append(dict(
    fn='base64-file.html', icon='🗂️', bg='#e6f7f2',
    title='Base64 文件转换',
    desc='文件与 Base64 互转：图片/文档/压缩包转 Base64 字符串（含 data URI 前缀选项），或粘贴 Base64 还原为文件下载。纯本地处理，文件不上传。',
    body='''    <div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;">
      <button class="btn primary" onclick="document.getElementById('file').click()">📁 选择文件 → Base64</button>
      <input type="file" id="file" style="display:none" onchange="fileToBase64(this.files[0])">
      <label style="flex:0 0 auto;align-self:center;font-size:13px;"><input type="checkbox" id="opt_datauri" checked> 带 data URI 前缀</label>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="b64Out" readonly style="min-height:120px" placeholder="文件的 Base64 字符串将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn" onclick="copyB64()">复制 Base64</button>
      <button class="btn" onclick="downloadB64()">⬇ 还原为文件</button>
    </div>
    <hr style="border:none;border-top:1px solid var(--border,#E5E7EB);margin:18px 0;">
    <p style="font-size:13px;color:var(--muted,#6B7280);margin-bottom:8px;">或：粘贴 Base64 / data URI，还原为文件：</p>
    <div class="input-row">
      <textarea id="b64In" placeholder="粘贴 Base64 或 data:image/png;base64,... 字符串" style="min-height:100px"></textarea>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="b64ToFile()">还原为文件</button>
      <button class="btn" onclick="b64ToText()">尝试以文本解码</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">🔒 所有转换均在浏览器本地完成，文件绝不上传。大文件（>50MB）建议直接使用文件系统工具。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
var lastFile=null,lastB64='';
function fileToBase64(f){
  var out=document.getElementById('result');
  if(!f){out.innerHTML='';return;}
  lastFile=f;
  var reader=new FileReader();
  reader.onload=function(e){
    var full=e.target.result;
    lastB64=document.getElementById('opt_datauri').checked?full:full.split(',')[1]||'';
    document.getElementById('b64Out').value=lastB64;
    out.innerHTML='<p>✅ 已转换：<strong>'+escH(f.name)+'</strong>（'+fmtSize(f.size)+'）→ Base64 <strong>'+fmtSize(lastB64.length)+'</strong></p>';
  };
  reader.readAsDataURL(f);
}
function fmtSize(n){return n<1024?n+' B':n<1048576?(n/1024).toFixed(1)+' KB':(n/1048576).toFixed(2)+' MB';}
function copyB64(){var v=document.getElementById('b64Out').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('请先转换文件');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制 Base64');}
function downloadB64(){
  var v=document.getElementById('b64Out').value.trim();
  if(!v){if(ToolBox.showToast)ToolBox.showToast('请先转换文件');return;}
  var parts=v.split(',');
  var mime=(parts[0]&&/^data:([^;]+)/.exec(parts[0]))?RegExp.$1:'application/octet-stream';
  var data=parts.length>1?parts.slice(1).join(','):v;
  try{
    var bin=atob(data);
    var arr=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++)arr[i]=bin.charCodeAt(i);
    var blob=new Blob([arr],{type:mime});
    var a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download=lastFile?('b64-'+lastFile.name):('file.'+(mime.split('/')[1]||'bin'));
    document.body.appendChild(a);a.click();document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
    if(ToolBox.showToast)ToolBox.showToast('已下载还原文件');
  }catch(e){if(ToolBox.showToast)ToolBox.showToast('Base64 无效：'+(e.message||e));}
}
function b64ToFile(){
  var v=document.getElementById('b64In').value.trim();
  var out=document.getElementById('result');
  if(!v){out.innerHTML='<p style="color:var(--warning)">请先粘贴 Base64</p>';return;}
  var parts=v.split(',');
  var mime=(parts[0]&&/^data:([^;]+)/.exec(parts[0]))?RegExp.$1:'application/octet-stream';
  var data=parts.length>1?parts.slice(1).join(','):v;
  try{
    var bin=atob(data);
    var arr=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++)arr[i]=bin.charCodeAt(i);
    var blob=new Blob([arr],{type:mime});
    var a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download='decoded.'+(mime.split('/')[1]||'bin');
    document.body.appendChild(a);a.click();document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
    out.innerHTML='<p style="color:var(--success)">✅ 已还原 '+fmtSize(arr.length)+' 字节文件并触发下载（'+escH(mime)+'）</p>';
  }catch(e){out.innerHTML='<p style="color:var(--danger)">Base64 无效：'+escH((e.message)||e)+'</p>';}
}
function b64ToText(){
  var v=document.getElementById('b64In').value.trim();
  var out=document.getElementById('result');
  if(!v){out.innerHTML='';return;}
  var parts=v.split(',');
  var data=parts.length>1?parts.slice(1).join(','):v;
  try{
    var bin=atob(data);
    var bytes=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
    var text=new TextDecoder('utf-8').decode(bytes);
    document.getElementById('b64In').value=text;
    out.innerHTML='<p style="color:var(--success)">✅ 已解码为文本（'+fmtSize(bytes.length)+'）</p>';
  }catch(e){out.innerHTML='<p style="color:var(--danger)">解码失败（可能不是文本内容）：'+escH((e.message)||e)+'</p>';}
}'''))

# ============ 2. 二维码美化生成器 ============
TOOLS.append(dict(
    fn='qr-beautify.html', icon='🎨', bg='#fdf2f8',
    title='二维码美化生成器',
    desc='生成个性化彩色二维码：自定义前景/背景色、容错级别与模块圆角样式，实时预览并下载 PNG，适合名片、海报与品牌物料。',
    extra_head='''<script src="../../js/qrcode.js"></script>''',
    body='''    <div class="input-row">
      <textarea id="text" placeholder="输入二维码内容：网址、文本、WiFi 配置等" style="min-height:90px" oninput="draw()">https://toolbox.example.com</textarea>
    </div>
    <div class="input-row">
      <div><label>前景色</label><input type="color" id="fg" value="#1F2937" oninput="draw()"></div>
      <div><label>背景色</label><input type="color" id="bg" value="#ffffff" oninput="draw()"></div>
      <div><label>容错级别</label>
        <select id="ecc" onchange="draw()" style="flex:1">
          <option value="L">L（7%）</option><option value="M" selected>M（15%）</option>
          <option value="Q">Q（25%）</option><option value="H">H（30%）</option>
        </select>
      </div>
      <div><label>模块样式</label>
        <select id="style" onchange="draw()" style="flex:1">
          <option value="round" selected>圆角</option><option value="square">直角</option>
        </select>
      </div>
    </div>
    <div class="result-box" id="result"></div>
    <div style="background:#fff;border:1px dashed var(--border,#E5E7EB);border-radius:16px;padding:20px;text-align:center;margin-bottom:14px;">
      <canvas id="qrCanvas" style="max-width:100%;"></canvas>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="draw()">生成</button>
      <button class="btn" onclick="downloadPng()">⬇ 下载 PNG</button>
      <button class="btn" onclick="copyBase64()">复制 Base64</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 容错级别越高，二维码被遮挡/损坏时的可识别性越强（但模块更密）。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function draw(){
  var text=document.getElementById('text').value;
  var out=document.getElementById('result');
  var canvas=document.getElementById('qrCanvas');
  var ctx=canvas.getContext('2d');
  ctx.clearRect(0,0,canvas.width,canvas.height);
  if(!text.trim()){out.innerHTML='';return;}
  var ecc=document.getElementById('ecc').value;
  var fg=document.getElementById('fg').value;
  var bg=document.getElementById('bg').value;
  var round=document.getElementById('style').value==='round';
  var qr;
  try{
    qr=new qrcode(0,ecc);
    qr.addData(text);
    qr.make();
  }catch(e){out.innerHTML='<p style="color:var(--danger)">内容过长或无效：'+escH((e.message)||e)+'</p>';return;}
  var count=qr.getModuleCount();
  var size=Math.min(520,count*8);
  var cell=size/count;
  canvas.width=size;canvas.height=size;
  ctx.fillStyle=bg;
  ctx.fillRect(0,0,size,size);
  ctx.fillStyle=fg;
  var r=round?cell*0.35:0;
  for(var row=0;row<count;row++){
    for(var col=0;col<count;col++){
      if(!qr.isDark(row,col))continue;
      var x=col*cell,y=row*cell;
      if(r>0){
        ctx.beginPath();
        ctx.moveTo(x+r,y);
        ctx.arcTo(x+cell,y,x+cell,y+cell,r);
        ctx.arcTo(x+cell,y+cell,x,y+cell,r);
        ctx.arcTo(x,y+cell,x,y,r);
        ctx.arcTo(x,y,x+cell,y,r);
        ctx.closePath();
        ctx.fill();
      }else{
        ctx.fillRect(x,y,cell,cell);
      }
    }
  }
  out.innerHTML='<p>✅ 已生成 <strong>'+count+' × '+count+'</strong> 模块 · 容错 <strong>'+ecc+'</strong> · '+size+'px</p>';
}
function downloadPng(){
  var c=document.getElementById('qrCanvas');
  if(!c.width){if(ToolBox.showToast)ToolBox.showToast('请先生成二维码');return;}
  var a=document.createElement('a');
  a.href=c.toDataURL('image/png');
  a.download='qrcode-'+Date.now()+'.png';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  if(ToolBox.showToast)ToolBox.showToast('已下载 PNG');
}
function copyBase64(){
  var c=document.getElementById('qrCanvas');
  if(!c.width){if(ToolBox.showToast)ToolBox.showToast('请先生成二维码');return;}
  ToolBox.copyText(c.toDataURL('image/png'));
  if(ToolBox.showToast)ToolBox.showToast('已复制 Base64 图片');
}
draw();'''))

# ============ 3. 任意进制转换器 ============
TOOLS.append(dict(
    fn='integer-base-converter.html', icon='🔢', bg='#eef2ff',
    title='任意进制转换器',
    desc='支持 2-36 进制任意互转与超大整数（BigInt）：输入数字与源进制，实时得到目标进制结果，附二进制/八进制/十进制/十六进制一览。',
    body='''    <div class="input-row">
      <div><label>数字</label><input type="text" id="num" placeholder="如：ff、1010、255" style="flex:2" oninput="convert()"></div>
      <div><label>源进制</label><input type="number" id="fromBase" value="16" min="2" max="36" style="flex:1" oninput="convert()"></div>
      <div><label>目标进制</label><input type="number" id="toBase" value="10" min="2" max="36" style="flex:1" oninput="convert()"></div>
    </div>
    <div class="result-box" id="result"></div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:16px;padding:18px;margin-bottom:14px;">
      <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:6px;">转换结果</div>
      <div id="mainOut" style="font-size:26px;font-weight:700;color:var(--primary);word-break:break-all;font-family:monospace;">—</div>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr style="background:rgba(0,0,0,.04);"><td style="padding:8px 10px;font-weight:600;">进制</td><td style="padding:8px 10px;font-weight:600;">值</td></tr>
      <tr><td style="padding:8px 10px;">二进制 (2)</td><td id="r2" style="padding:8px 10px;font-family:monospace;">—</td></tr>
      <tr><td style="padding:8px 10px;">八进制 (8)</td><td id="r8" style="padding:8px 10px;font-family:monospace;">—</td></tr>
      <tr><td style="padding:8px 10px;">十进制 (10)</td><td id="r10" style="padding:8px 10px;font-family:monospace;">—</td></tr>
      <tr><td style="padding:8px 10px;">十六进制 (16)</td><td id="r16" style="padding:8px 10px;font-family:monospace;">—</td></tr>
      <tr><td style="padding:8px 10px;">Base32 (32)</td><td id="r32" style="padding:8px 10px;font-family:monospace;">—</td></tr>
      <tr><td style="padding:8px 10px;">Base36 (36)</td><td id="r36" style="padding:8px 10px;font-family:monospace;">—</td></tr>
    </table>
    <div class="toolbar" style="margin-top:12px;">
      <button class="btn primary" onclick="convert()">转换</button>
      <button class="btn" onclick="copyMain()">复制结果</button>
    </div>''',
    script='''var DIGITS='0123456789abcdefghijklmnopqrstuvwxyz';
function toBigInt(str,base){
  var s=String(str).trim().toLowerCase().replace(/^0+/, '')||'0';
  var v=0n;
  for(var i=0;i<s.length;i++){
    var d=DIGITS.indexOf(s[i]);
    if(d<0||d>=base)throw new Error('第 '+(i+1)+' 位 "'+s[i]+'" 不是 '+base+' 进制的有效数字');
    v=v*BigInt(base)+BigInt(d);
  }
  return v;
}
function fromBigInt(v,base){
  if(v===0n)return '0';
  var s='',n=v;
  while(n>0n){s=DIGITS[Number(n%BigInt(base))]+s;n=n/BigInt(base);}
  return s;
}
function convert(){
  var str=document.getElementById('num').value.trim();
  var fb=parseInt(document.getElementById('fromBase').value)||10;
  var tb=parseInt(document.getElementById('toBase').value)||10;
  if(fb<2)fb=2;if(fb>36)fb=36;if(tb<2)tb=2;if(tb>36)tb=36;
  document.getElementById('fromBase').value=fb;document.getElementById('toBase').value=tb;
  var out=document.getElementById('result');
  if(!str){document.getElementById('mainOut').textContent='—';['r2','r8','r10','r16','r32','r36'].forEach(function(id){document.getElementById(id).textContent='—';});out.innerHTML='';return;}
  try{
    var v=toBigInt(str,fb);
    document.getElementById('mainOut').textContent=fromBigInt(v,tb);
    document.getElementById('r2').textContent=fromBigInt(v,2);
    document.getElementById('r8').textContent=fromBigInt(v,8);
    document.getElementById('r10').textContent=v.toString();
    document.getElementById('r16').textContent=fromBigInt(v,16);
    document.getElementById('r32').textContent=fromBigInt(v,32);
    document.getElementById('r36').textContent=fromBigInt(v,36);
    out.innerHTML='<p>✅ '+fb+' 进制 → '+tb+' 进制 · 数值约 <strong>'+(v.toString().length)+'</strong> 位十进制</p>';
  }catch(e){out.innerHTML='<p style="color:var(--danger)">'+((e.message)||e)+'</p>';document.getElementById('mainOut').textContent='❌';}
}
function copyMain(){var v=document.getElementById('mainOut').textContent;if(!v||v==='—'||v==='❌'){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}'''))

# ============ 4. 多算法哈希器 ============
TOOLS.append(dict(
    fn='hash-multi.html', icon='🧬', bg='#f0fdf4',
    title='多算法哈希器',
    desc='一键计算多种哈希：MD5 / SHA-1 / SHA-256 / SHA-512 / CRC32，支持多算法同时输出与大小写切换。SHA 走浏览器原生 crypto.subtle，全程本地。',
    body='''    <div class="input-row">
      <textarea id="input" placeholder="输入要计算哈希的文本，如：Hello ToolBox" style="min-height:120px" oninput="calc()"></textarea>
    </div>
    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">算法：</span>
      <label style="flex:0 0 auto;"><input type="checkbox" id="al_md5" checked> MD5</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="al_sha1" checked> SHA-1</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="al_sha256" checked> SHA-256</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="al_sha512"> SHA-512</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="al_crc32"> CRC32</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="opt_upper"> 大写</label>
    </div>
    <div class="result-box" id="result"></div>
    <div id="outBox" style="display:flex;flex-direction:column;gap:10px;"></div>
    <div class="toolbar" style="margin-top:12px;">
      <button class="btn primary" onclick="calc()">计算</button>
      <button class="btn" onclick="copyAll()">复制全部</button>
    </div>''',
    script='''var CRC_TABLE=(function(){var t=[];for(var n=0;n<256;n++){var c=n;for(var k=0;k<8;k++)c=c&1?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c>>>0;}return t;})();
function crc32(str){
  var crc=0xFFFFFFFF;
  for(var i=0;i<str.length;i++){
    crc=(crc>>>8)^CRC_TABLE[(crc^str.charCodeAt(i))&0xFF];
  }
  return (crc^0xFFFFFFFF)>>>0;
}
function md5(str){
  function rotl(x,n){return (x<<n)|(x>>>(32-n));}
  function add32(a,b){var l=(a&0xFFFF)+(b&0xFFFF);return (((a>>16)+(b>>16)+(l>>16))<<16)|(l&0xFFFF);}
  var K=[0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391];
  var S=[7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21];
  var bytes=[];
  for(var i=0;i<str.length;i++)bytes.push(str.charCodeAt(i));
  var bitLen=bytes.length*8;
  bytes.push(0x80);
  while(bytes.length%64!==56)bytes.push(0);
  bytes.push(bitLen&0xFF,(bitLen>>>8)&0xFF,(bitLen>>>16)&0xFF,(bitLen>>>24)&0xFF,0,0,0,0);
  var a0=0x67452301,b0=0xEFCDAB89,c0=0x98BADCFE,d0=0x10325476;
  for(var off=0;off<bytes.length;off+=64){
    var M=[];for(var j=0;j<16;j++)M[j]=bytes[off+j*4]|(bytes[off+j*4+1]<<8)|(bytes[off+j*4+2]<<16)|(bytes[off+j*4+3]<<24);
    var A=a0,B=b0,C=c0,D=d0;
    for(var j2=0;j2<64;j2++){
      var F,g;
      if(j2<16){F=(B&C)|(~B&D);g=j2;}
      else if(j2<32){F=(D&B)|(~D&C);g=(5*j2+1)%16;}
      else if(j2<48){F=B^C^D;g=(3*j2+5)%16;}
      else{F=C^(B|~D);g=(7*j2)%16;}
      F=add32(add32(add32(F,A),K[j2]),M[g]);
      var tmp=D;D=C;C=B;B=add32(B,rotl(F,S[j2]));A=tmp;
    }
    a0=add32(a0,A);b0=add32(b0,B);c0=add32(c0,C);d0=add32(d0,D);
  }
  function hex(n){var s='';for(var i=0;i<4;i++){s+=('00'+((n>>>(i*8))&0xFF).toString(16)).slice(-2);}return s;}
  return hex(a0)+hex(b0)+hex(c0)+hex(d0);
}
function toHex(buf){
  return Array.from(new Uint8Array(buf)).map(function(b){return b.toString(16).padStart(2,'0');}).join('');
}
function calc(){
  var text=document.getElementById('input').value;
  var upper=document.getElementById('opt_upper').checked;
  var box=document.getElementById('outBox');
  var out=document.getElementById('result');
  if(!text){box.innerHTML='';out.innerHTML='';return;}
  var items=[];
  function push(label,hash){
    if(upper)hash=String(hash).toUpperCase();
    items.push('<div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:12px 14px;">'+
      '<div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:4px;">'+label+'</div>'+
      '<div style="font-family:monospace;font-size:13.5px;word-break:break-all;">'+hash+' <button class="btn" style="padding:1px 10px;font-size:12px;float:right;margin-left:6px;" onclick="copyItem(this)">复制</button></div></div>');
  }
  var selected=0;
  if(document.getElementById('al_md5').checked){push('MD5',md5(text));selected++;}
  if(document.getElementById('al_sha1').checked){push('SHA-1','—');selected++;}
  if(document.getElementById('al_sha256').checked){push('SHA-256','—');selected++;}
  if(document.getElementById('al_sha512').checked){push('SHA-512','—');selected++;}
  if(document.getElementById('al_crc32').checked){push('CRC32',crc32(text).toString(16));selected++;}
  box.innerHTML=items.join('');
  // SHA 系列走异步 crypto.subtle
  var jobs=[];
  if(document.getElementById('al_sha1').checked)jobs.push(['SHA-1','SHA-1']);
  if(document.getElementById('al_sha256').checked)jobs.push(['SHA-256','SHA-256']);
  if(document.getElementById('al_sha512').checked)jobs.push(['SHA-512','SHA-512']);
  if(jobs.length&&window.crypto&&crypto.subtle){
    var enc=new TextEncoder().encode(text);
    Promise.all(jobs.map(function(j){return crypto.subtle.digest(j[1],enc).then(function(buf){return [j[0],toHex(buf)];});})).then(function(res){
      res.forEach(function(r){
        var v=upper?r[1].toUpperCase():r[1];
        var boxes=box.querySelectorAll('div');
        for(var i=0;i<boxes.length;i++){
          if(boxes[i].textContent.indexOf(r[0]+'复制')>-1&&boxes[i].querySelector('div:last-child')){
            var target=boxes[i].querySelector('div:nth-child(2)');
            if(target){target.firstChild.textContent=v;}
            break;
          }
        }
      });
    }).catch(function(){});
  }
  out.innerHTML='<p>✅ 已计算 <strong>'+selected+'</strong> 种算法（'+text.length+' 字符）</p>';
}
function copyItem(btn){var v=btn.parentNode.childNodes[0].nodeValue;ToolBox.copyText(btn.parentNode.textContent.replace('复制','').trim());if(ToolBox.showToast)ToolBox.showToast('已复制');}
function copyAll(){var box=document.getElementById('outBox');if(!box.innerHTML){if(ToolBox.showToast)ToolBox.showToast('请先计算');return;}var lines=[];box.querySelectorAll('div > div').forEach(function(d){var label=d.childNodes[0].textContent;var val=d.querySelector('div');if(val)lines.push(label+': '+val.textContent.replace('复制','').trim());});ToolBox.copyText(lines.join('\\n'));if(ToolBox.showToast)ToolBox.showToast('已复制全部');}
calc();'''))

def main():
    for t in TOOLS:
        gen(t['fn'], t['icon'], t['bg'], t['title'], t['desc'], t['body'], t['script'], t.get('extra_head',''))
    print(f'\\n优化点 4 个已生成 → {OUT_DIR}')

if __name__ == '__main__':
    main()
