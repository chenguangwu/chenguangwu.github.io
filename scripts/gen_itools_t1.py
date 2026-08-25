#!/usr/bin/env python3
"""it-tools 对标 · 第一梯队生成器：10 个开发者工具（tools/it/，cat=dev,industry=it）。
每个工具独立实现真实逻辑（非空壳模板），纯前端、数据不上传。
用法：python3 scripts/gen_itools_t1.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根
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
<script src="../../js/common.js"></script>
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

def gen(fn, icon, bg, title, desc, body, script, extra_head=''):
    html = (TPL
        .replace('__ICON__', icon).replace('__BG__', bg)
        .replace('__TITLE__', esc(title)).replace('__DESC__', esc(desc))
        .replace('__FN__', fn).replace('__BODY__', body)
        .replace('__SCRIPT__', script).replace('__EXTRA_HEAD__', extra_head))
    p = os.path.join(OUT_DIR, fn)
    open(p, 'w', encoding='utf-8').write(html)
    print('OK:', p)

# ============ 1. 数学表达式求值器 ============
TOOLS = []

TOOLS.append(dict(
    fn='math-evaluator.html', icon='🧮', bg='#e8f0fe',
    title='数学表达式求值器',
    desc='在线计算数学表达式：支持 + - * / % ^ ( ) 与 sin/cos/tan/sqrt/abs/ln/log/floor/ceil/round/min/max 等函数，自动保存最近 20 条历史。',
    body='''    <div class="input-row">
      <input type="text" id="expr" placeholder="如：2^10 + sqrt(144) * sin(pi/6) + 15%" style="flex:3" onkeydown="if(event.key==='Enter')calc()">
      <button class="btn primary" onclick="calc()">计算</button>
      <button class="btn" onclick="document.getElementById('expr').value='';calc()">清空</button>
    </div>
    <div class="toolbar">
      <button class="btn" onclick="insertFn('(')">( )</button>
      <button class="btn" onclick="insertFn('^')">^</button>
      <button class="btn" onclick="insertFn('sqrt(')">√</button>
      <button class="btn" onclick="insertFn('sin(')">sin</button>
      <button class="btn" onclick="insertFn('cos(')">cos</button>
      <button class="btn" onclick="insertFn('ln(')">ln</button>
      <button class="btn" onclick="insertFn('pi')">π</button>
    </div>
    <div class="result-box" id="result"></div>
    <h3 style="margin-top:16px;font-size:15px;">🕐 最近计算历史</h3>
    <div id="hist" style="font-size:13px;line-height:2;"></div>
    <button class="btn" onclick="clearHist()" style="margin-top:8px;">清空历史</button>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function fmt(n){
  if(!isFinite(n)) return String(n);
  var abs=Math.abs(n);
  if(abs>=1e15||(abs>0&&abs<1e-9)) return n.toExponential(6);
  return String(Math.round(n*1e10)/1e10);
}
function insertFn(s){
  var el=document.getElementById('expr');
  el.value=el.value.slice(0,el.selectionStart||el.value.length)+s+el.value.slice(el.selectionEnd||el.value.length);
  el.focus(); calc();
}
function renderHist(){
  var h;
  try{h=JSON.parse(localStorage.getItem('mathHist')||'[]');}catch(e){h=[];}
  document.getElementById('hist').innerHTML=h.length?h.map(function(x){
    return '<div>'+escH(x.e)+' = <strong style="color:var(--primary)">'+fmt(x.v)+'</strong> <button class="btn" style="margin-left:6px;padding:2px 10px;font-size:12px;" onclick="document.getElementById(\\'expr\\').value='+JSON.stringify(x.e).replace(/</g,'\\u003c')+';calc()">复用</button></div>';
  }).join(''):'<span style="color:var(--muted,#9CA3AF)">暂无记录</span>';
}
function clearHist(){localStorage.removeItem('mathHist');renderHist();}
function calc(){
  var expr=document.getElementById('expr').value.trim();
  var out=document.getElementById('result');
  if(!expr){out.innerHTML='';return;}
  if(expr.length>200){out.innerHTML='<p style="color:var(--danger)">表达式过长（≤200 字符）</p>';return;}
  if(!/^[0-9+\\-*\\/%^().,\\sA-Za-z%]+$/.test(expr)){out.innerHTML='<p style="color:var(--danger)">表达式含非法字符（仅支持数字、运算符与函数名）</p>';return;}
  try{
    var js=expr.replace(/\\^/g,'**').replace(/(\\d+)\\s*%/g,'($1/100)');
    var fn=new Function('Math','sin','cos','tan','sqrt','abs','ln','log','floor','ceil','round','min','max','pi','e','return ('+js+')');
    var val=fn(Math,Math.sin,Math.cos,Math.tan,Math.sqrt,Math.abs,Math.log,Math.log10,Math.floor,Math.ceil,Math.round,Math.min,Math.max,Math.PI,Math.E);
    if(typeof val!=='number'||!isFinite(val))throw new Error('结果不是有效数字');
    out.innerHTML='<p>结果：<strong style="font-size:22px;color:var(--primary)">'+fmt(val)+'</strong></p>';
    var h;
    try{h=JSON.parse(localStorage.getItem('mathHist')||'[]');}catch(e){h=[];}
    h.unshift({e:expr,v:val});if(h.length>20)h.pop();
    localStorage.setItem('mathHist',JSON.stringify(h));
    renderHist();
  }catch(e){out.innerHTML='<p style="color:var(--danger)">表达式无效：'+escH((e&&e.message)||e)+'</p>';}
}
renderHist();'''))

# ============ 2. JSON 压缩 / 美化 ============
TOOLS.append(dict(
    fn='json-minify.html', icon='🗜️', bg='#fef3e2',
    title='JSON 压缩/格式化',
    desc='一键压缩或美化 JSON：显示原始/输出体积与压缩率，支持 JSON5 常见写法纠错提示，纯前端处理。',
    body='''    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">模式：</span>
      <label style="flex:0 0 auto;"><input type="radio" name="mode" value="min" checked onchange="process()"> 压缩</label>
      <label style="flex:0 0 auto;"><input type="radio" name="mode" value="pretty" onchange="process()"> 美化</label>
    </div>
    <div class="input-row">
      <textarea id="input" placeholder='粘贴 JSON 到此处，如：{"name":"ToolBox","tools":6246}' style="min-height:180px" oninput="process()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:180px" placeholder="输出结果将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="process()">转换</button>
      <button class="btn" onclick="copyOut()">复制结果</button>
      <button class="btn" onclick="document.getElementById('input').value='';process()">清空</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function copyOut(){
  var v=document.getElementById('output').value;
  if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}
  ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');
}
function process(){
  var raw=document.getElementById('input').value.trim();
  var out=document.getElementById('result');
  if(!raw){document.getElementById('output').value='';out.innerHTML='';return;}
  var mode=document.querySelector('input[name=mode]:checked').value;
  try{
    var obj=JSON.parse(raw);
    var outStr=mode==='min'?JSON.stringify(obj):JSON.stringify(obj,null,2);
    document.getElementById('output').value=outStr;
    var origLen=new Blob([raw]).size,outLen=new Blob([outStr]).size;
    var rate=origLen?((1-outLen/origLen)*100).toFixed(1):'0';
    var html='<p>原始 <strong>'+origLen+'</strong> 字节 → 输出 <strong>'+outLen+'</strong> 字节';
    if(mode==='min')html+=' · 压缩率 <strong>'+rate+'%</strong>';
    html+='</p>';
    if(mode==='min'&&rate<0)html+='<p style="color:var(--warning)">⚠️ 压缩后反而更大，小 JSON 建议保留美化格式</p>';
    out.innerHTML=html;
  }catch(e){
    var m=(e&&e.message)||String(e);
    out.innerHTML='<p style="color:var(--danger)">JSON 解析失败：'+escH(m)+'</p>';
    document.getElementById('output').value='';
  }
}'''))

# ============ 3. JSON 转 CSV ============
TOOLS.append(dict(
    fn='json-to-csv.html', icon='📊', bg='#e6f7f2',
    title='JSON 转 CSV',
    desc='把 JSON 数组一键转为 CSV 表格：自动提取所有字段为表头，支持嵌套对象序列化、下载 .csv 文件。',
    body='''    <div class="input-row">
      <textarea id="input" placeholder='粘贴 JSON 数组，如：[{"name":"张三","age":30,"city":"上海"},{"name":"李四","age":25,"city":"北京"}]' style="min-height:180px"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:180px" placeholder="CSV 输出将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="toCSV()">转换</button>
      <button class="btn" onclick="copyOut()">复制 CSV</button>
      <button class="btn" onclick="downloadCSV()">⬇ 下载 .csv</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){
  var v=document.getElementById('output').value;
  if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}
  ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');
}
function toCSV(){
  var raw=document.getElementById('input').value.trim();
  var out=document.getElementById('result');
  if(!raw){document.getElementById('output').value='';out.innerHTML='';return;}
  try{
    var data=JSON.parse(raw);
    if(!Array.isArray(data)||!data.length){out.innerHTML='<p style="color:var(--danger)">请输入非空 JSON 数组</p>';return;}
    var keys=[];
    data.forEach(function(o){
      if(o&&typeof o==='object')Object.keys(o).forEach(function(k){if(keys.indexOf(k)===-1)keys.push(k);});
    });
    function cell(v){
      if(v===null||v===undefined)return '';
      if(typeof v==='object')v=JSON.stringify(v);
      return '"'+String(v).replace(/"/g,'""')+'"';
    }
    var lines=[keys.map(cell).join(',')];
    data.forEach(function(o){
      lines.push(keys.map(function(k){return cell(o?o[k]:'');}).join(','));
    });
    var csv=lines.join('\\n');
    document.getElementById('output').value=csv;
    out.innerHTML='<p>已转换 <strong>'+data.length+'</strong> 行 × <strong>'+keys.length+'</strong> 列，UTF-8 编码（Excel 打开如乱码请另存为 UTF-8 BOM）</p>';
  }catch(e){out.innerHTML='<p style="color:var(--danger)">解析失败：'+escH((e&&e.message)||e)+'</p>';document.getElementById('output').value='';}
}
function downloadCSV(){
  var csv=document.getElementById('output').value;
  if(!csv){if(ToolBox.showToast)ToolBox.showToast('请先转换');return;}
  var blob=new Blob(['\\ufeff'+csv],{type:'text/csv;charset=utf-8;'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob);a.download='data.csv';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
  if(ToolBox.showToast)ToolBox.showToast('已下载 data.csv');
}'''))

# ============ 4. 随机 Token 生成器 ============
TOOLS.append(dict(
    fn='token-generator.html', icon='🎟️', bg='#fdf2f8',
    title='随机 Token 生成器',
    desc='基于浏览器加密级随机数（crypto.getRandomValues）批量生成高强度 Token：自定义长度、字符集、数量，一键复制。',
    body='''    <div class="input-row">
      <label>长度</label>
      <input type="number" id="len" value="32" min="4" max="256" style="flex:1">
      <label>数量</label>
      <input type="number" id="count" value="1" min="1" max="20" style="flex:1">
    </div>
    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">字符集：</span>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ch_upper" checked> A-Z</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ch_lower" checked> a-z</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ch_digit" checked> 0-9</label>
      <label style="flex:0 0 auto;"><input type="checkbox" id="ch_sym"> !@#$%^&*</label>
    </div>
    <div class="result-box" id="result"></div>
    <div id="tokList" style="font-size:13px;line-height:2;font-family:'SF Mono','Courier New',monospace;word-break:break-all;"></div>
    <div class="toolbar">
      <button class="btn primary" onclick="gen()">生成</button>
      <button class="btn" onclick="copyAll()">复制全部</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">🔒 随机数来自 <code>crypto.getRandomValues</code>，仅在本机生成，不上传。</p>''',
    script='''var SETS={upper:'ABCDEFGHIJKLMNOPQRSTUVWXYZ',lower:'abcdefghijklmnopqrstuvwxyz',digit:'0123456789',sym:'!@#$%^&*()-_=+[]{};:,.?/~'};
var toks=[];
function gen(){
  var len=parseInt(document.getElementById('len').value)||32;if(len<4)len=4;if(len>256)len=256;
  var n=parseInt(document.getElementById('count').value)||1;if(n<1)n=1;if(n>20)n=20;
  var chars='';
  ['upper','lower','digit','sym'].forEach(function(k){if(document.getElementById('ch_'+k).checked)chars+=SETS[k];});
  var out=document.getElementById('result');
  if(!chars){out.innerHTML='<p style="color:var(--danger)">请至少选择一种字符集</p>';return;}
  var rnd=new Uint32Array(Math.max(len,1));
  toks=[];
  for(var j=0;j<n;j++){
    crypto.getRandomValues(rnd);
    var s='';
    for(var i=0;i<len;i++)s+=chars[rnd[i]%chars.length];
    toks.push(s);
  }
  document.getElementById('tokList').innerHTML=toks.map(function(t,i){
    return '<div>'+t+' <button class="btn" style="padding:1px 10px;font-size:12px;margin-left:6px;" onclick="copyOne('+i+')">复制</button></div>';
  }).join('');
  out.innerHTML='<p>已生成 <strong>'+n+'</strong> 个 · <strong>'+len+'</strong> 位（信息熵 ≈ <strong>'+Math.round(len*Math.log2(chars.length))+'</strong> bit）</p>';
}
function copyOne(i){ToolBox.copyText(toks[i]);if(ToolBox.showToast)ToolBox.showToast('已复制第 '+(i+1)+' 个');}
function copyAll(){if(!toks.length){if(ToolBox.showToast)ToolBox.showToast('请先生成');return;}ToolBox.copyText(toks.join('\\n'));if(ToolBox.showToast)ToolBox.showToast('已复制全部 '+toks.length+' 个');}'''))

# ============ 5. Bcrypt 哈希 ============
TOOLS.append(dict(
    fn='bcrypt.html', icon='🔒', bg='#eef2ff',
    title='Bcrypt 哈希/校验',
    desc='Bcrypt 密码哈希生成与验证：选择成本因子（rounds），生成 60 位标准哈希，支持原文+哈希一键校验。全程浏览器本地计算，数据不上传。',
    extra_head='''<script src="https://cdn.jsdelivr.net/npm/bcryptjs@2.4.3/dist/bcrypt.min.js"></script>''',
    body='''    <div class="input-row">
      <label>明文</label>
      <input type="password" id="plain" placeholder="输入要哈希或验证的文本" style="flex:2">
      <label>成本因子</label>
      <select id="rounds" style="flex:1">
        <option value="8">8（快，约 50ms）</option>
        <option value="10" selected>10（推荐，约 150ms）</option>
        <option value="12">12（约 600ms）</option>
        <option value="14">14（慢，约 2.4s）</option>
      </select>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="hashOut" readonly style="min-height:80px" placeholder="生成的 Bcrypt 哈希（$2a$10$...）将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="genHash()">生成哈希</button>
      <button class="btn" onclick="verify()">校验哈希</button>
      <button class="btn" onclick="copyHash()">复制哈希</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 Bcrypt 内置盐值（salt），相同明文每次生成结果不同；校验时自动从哈希中提取盐。bcryptjs 库来自 jsdelivr CDN，计算完全在本地。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function genHash(){
  var txt=document.getElementById('plain').value;
  var rounds=parseInt(document.getElementById('rounds').value)||10;
  var out=document.getElementById('result');
  if(!txt){out.innerHTML='<p style="color:var(--warning)">请先输入要哈希的文本</p>';return;}
  out.innerHTML='<p>⏳ 计算中（'+rounds+' 轮）...此过程在浏览器本地进行，请稍候</p>';
  setTimeout(function(){
    try{
      var hash=bcrypt.hashSync(txt,rounds);
      document.getElementById('hashOut').value=hash;
      out.innerHTML='<p style="color:var(--success)">✅ 已生成 Bcrypt 哈希（rounds='+rounds+'，60 位）</p>';
    }catch(e){out.innerHTML='<p style="color:var(--danger)">生成失败：'+escH((e&&e.message)||e)+'</p>';}
  },30);
}
function verify(){
  var txt=document.getElementById('plain').value;
  var h=document.getElementById('hashOut').value.trim();
  var out=document.getElementById('result');
  if(!h){out.innerHTML='<p style="color:var(--warning)">请先生成或粘贴要验证的哈希</p>';return;}
  if(!txt){out.innerHTML='<p style="color:var(--warning)">请输入要校验的明文</p>';return;}
  setTimeout(function(){
    try{
      var ok=bcrypt.compareSync(txt,h);
      out.innerHTML=ok?'<p style="color:var(--success)">✅ 匹配！明文与哈希一致</p>':'<p style="color:var(--danger)">❌ 不匹配（明文或哈希有误）</p>';
    }catch(e){out.innerHTML='<p style="color:var(--danger)">哈希格式无效：'+escH((e&&e.message)||e)+'</p>';}
  },30);
}
function copyHash(){
  var h=document.getElementById('hashOut').value.trim();
  if(!h){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}
  ToolBox.copyText(h);if(ToolBox.showToast)ToolBox.showToast('已复制哈希');
}'''))

# ============ 6. Crontab 生成器 ============
TOOLS.append(dict(
    fn='crontab-generator.html', icon='⏰', bg='#f3e8ff',
    title='Crontab 生成器',
    desc='可视化生成 Linux crontab 定时任务表达式：选择分/时/日/月/周，一键生成 5 段 cron 语法并给出中文说明，附常用预设。',
    body='''    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">常用预设：</span>
      <button class="btn" onclick="preset('* * * * *')">每分钟</button>
      <button class="btn" onclick="preset('*/5 * * * *')">每 5 分钟</button>
      <button class="btn" onclick="preset('0 * * * *')">每小时</button>
      <button class="btn" onclick="preset('0 9 * * *')">每天 9:00</button>
      <button class="btn" onclick="preset('0 9 * * 1')">每周一 9:00</button>
      <button class="btn" onclick="preset('30 8 1 * *')">每月 1 日 8:30</button>
    </div>
    <div class="input-row">
      <div><label>分钟 (0-59)</label><input type="text" id="f_min" value="0" oninput="build()"></div>
      <div><label>小时 (0-23)</label><input type="text" id="f_hour" value="9" oninput="build()"></div>
      <div><label>日期 (1-31)</label><input type="text" id="f_dom" value="*" oninput="build()"></div>
      <div><label>月份 (1-12)</label><input type="text" id="f_mon" value="*" oninput="build()"></div>
      <div><label>星期 (0-6)</label><input type="text" id="f_dow" value="*" oninput="build()"></div>
    </div>
    <div class="result-box" id="result"></div>
    <input type="text" id="cronOut" readonly style="font-family:'SF Mono','Courier New',monospace;font-size:15px;padding:12px;border-radius:10px;border:1px solid var(--border,#E5E7EB);width:100%;box-sizing:border-box;">
    <div class="toolbar" style="margin-top:12px;">
      <button class="btn primary" onclick="copyCron()">复制表达式</button>
      <button class="btn" onclick="build()">重新生成</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">支持 * 、*/n 步进、a,b 列表、a-b 范围。五段依次为：分 时 日 月 周。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function preset(expr){
  var p=expr.split(/\\s+/);
  document.getElementById('f_min').value=p[0];
  document.getElementById('f_hour').value=p[1];
  document.getElementById('f_dom').value=p[2];
  document.getElementById('f_mon').value=p[3];
  document.getElementById('f_dow').value=p[4];
  build();
}
function valid(s,min,max){return /^[*]|^[*]\\/\\d+$|^\\d+(-\\d+)?(,\\d+(-\\d+)?)*$/.test(s);}
function fieldDesc(zh,f,min,max,allText){
  if(f==='*')return allText;
  if(f.indexOf('*/')===0)return '每 '+f.slice(2)+' '+zh;
  if(f.indexOf('-')>0){var r=f.split('-');return zh+' '+r[0]+'-'+r[1];}
  if(f.indexOf(',')>-1)return zh+' '+f.split(',').join('、');
  return zh+' '+f;
}
function build(){
  var f=[document.getElementById('f_min').value.trim(),document.getElementById('f_hour').value.trim(),
         document.getElementById('f_dom').value.trim(),document.getElementById('f_mon').value.trim(),
         document.getElementById('f_dow').value.trim()];
  var out=document.getElementById('result');
  var bad='';
  if(!valid(f[0],0,59))bad='分钟';
  else if(!valid(f[1],0,23))bad='小时';
  else if(!valid(f[2],1,31))bad='日期';
  else if(!valid(f[3],1,12))bad='月份';
  else if(!valid(f[4],0,6))bad='星期';
  if(bad){out.innerHTML='<p style="color:var(--danger)">⚠️ '+bad+' 字段格式无效（支持 *、*/n、a-b、a,b）</p>';document.getElementById('cronOut').value='';return;}
  var expr=f.join(' ');
  document.getElementById('cronOut').value=expr;
  var parts=[
    fieldDesc('分钟',f[0],0,59,'每分钟'),
    fieldDesc('小时',f[1],0,23,'每小时'),
    fieldDesc('日期',f[2],1,31,'每天'),
    fieldDesc('月份',f[3],1,12,'每月'),
    fieldDesc('星期',f[4],0,6,'每周')
  ];
  var zhTxt;
  if(f[0]==='*')zhTxt=parts[0];
  else if(f[1]==='*')zhTxt=parts[1];
  else if(f[2]==='*'&&f[4]==='*')zhTxt='每月 '+parts[3]+' '+parts[2]+' '+parts[1]+' '+parts[0];
  else if(f[2]==='*')zhTxt='每 '+parts[4]+' '+parts[1]+' '+parts[0];
  else zhTxt='每月 '+parts[3]+' '+parts[2]+' '+parts[1]+' '+parts[0];
  out.innerHTML='<p>✅ 表达式：<code style="background:rgba(0,0,0,.05);padding:2px 8px;border-radius:6px;">'+escH(expr)+'</code></p><p>中文说明：<strong>'+escH(zhTxt)+'</strong></p>';
}
function copyCron(){
  var v=document.getElementById('cronOut').value;
  if(!v){if(ToolBox.showToast)ToolBox.showToast('请先生成');return;}
  ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制 cron 表达式');
}
build();'''))

# ============ 7. Chmod 权限计算器 ============
TOOLS.append(dict(
    fn='chmod-calculator.html', icon='🔐', bg='#fff7ed',
    title='Chmod 权限计算器',
    desc='可视化计算 Linux 文件权限：勾选属主/组/其他用户的读(4)写(2)执行(1)权限，实时得到数字模式与符号模式，附常见权限速查。',
    body='''    <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:14px;">
      <tr style="text-align:center;font-weight:600;color:var(--muted,#6B7280);">
        <td style="padding:8px;">用户</td><td>读 r (4)</td><td>写 w (2)</td><td>执行 x (1)</td>
      </tr>
      <tr style="text-align:center;">
        <td style="padding:8px;font-weight:600;">属主 (user)</td>
        <td><input type="checkbox" id="r0" checked onchange="calc()"></td>
        <td><input type="checkbox" id="w0" checked onchange="calc()"></td>
        <td><input type="checkbox" id="x0" checked onchange="calc()"></td>
      </tr>
      <tr style="text-align:center;">
        <td style="padding:8px;font-weight:600;">组 (group)</td>
        <td><input type="checkbox" id="r1" checked onchange="calc()"></td>
        <td><input type="checkbox" id="w1" onchange="calc()"></td>
        <td><input type="checkbox" id="x1" onchange="calc()"></td>
      </tr>
      <tr style="text-align:center;">
        <td style="padding:8px;font-weight:600;">其他 (others)</td>
        <td><input type="checkbox" id="r2" checked onchange="calc()"></td>
        <td><input type="checkbox" id="w2" onchange="calc()"></td>
        <td><input type="checkbox" id="x2" onchange="calc()"></td>
      </tr>
    </table>
    <div class="result-box" id="result"></div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px;">
      <div style="flex:1;min-width:140px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:12px;text-align:center;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">数字模式</div>
        <div id="numOut" style="font-size:26px;font-weight:700;color:var(--primary);font-family:monospace;">755</div>
      </div>
      <div style="flex:1;min-width:140px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:12px;text-align:center;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">符号模式</div>
        <div id="symOut" style="font-size:26px;font-weight:700;color:var(--primary);font-family:monospace;">rwxr-xr-x</div>
      </div>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="copyPerm()">复制 chmod 命令</button>
      <button class="btn" onclick="quick('777')">777</button>
      <button class="btn" onclick="quick('755')">755</button>
      <button class="btn" onclick="quick('644')">644</button>
      <button class="btn" onclick="quick('700')">700</button>
      <button class="btn" onclick="quick('600')">600</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function quick(d){
  var map={'7':[1,1,1],'6':[1,1,0],'5':[1,0,1],'4':[1,0,0],'3':[0,1,1],'2':[0,1,0],'1':[0,0,1],'0':[0,0,0]};
  for(var i=0;i<3;i++){
    var m=map[d[i]]||[0,0,0];
    document.getElementById('r'+i).checked=!!m[0];
    document.getElementById('w'+i).checked=!!m[1];
    document.getElementById('x'+i).checked=!!m[2];
  }
  calc();
}
function calc(){
  var digits='',syms=[];
  for(var i=0;i<3;i++){
    var r=document.getElementById('r'+i).checked,w=document.getElementById('w'+i).checked,x=document.getElementById('x'+i).checked;
    digits+=(r?4:0)+(w?2:0)+(x?1:0);
    syms.push((r?'r':'-')+(w?'w':'-')+(x?'x':'-'));
  }
  document.getElementById('numOut').textContent=digits;
  document.getElementById('symOut').textContent=syms.join('');
  var tips={
    '755':'目录/可执行程序常用：属主全权限，组/其他可读可执行',
    '644':'普通文件常用：属主读写，组/其他只读',
    '777':'⚠️ 所有用户全权限，有安全风险，谨慎使用',
    '700':'仅属主可读可写可执行（私密文件/脚本）',
    '600':'仅属主可读可写（私钥、配置文件）',
    '444':'所有用户只读',
    '555':'所有用户可读可执行（防写）',
    '000':'无任何权限'
  };
  var tip=tips[digits]||'读(4)+写(2)+执行(1) 之和为该用户组权限位';
  document.getElementById('result').innerHTML='<p><code>chmod '+digits+' file</code> → '+escH(syms.join(''))+' · '+escH(tip)+'</p>';
}
function copyPerm(){
  var d=document.getElementById('numOut').textContent;
  ToolBox.copyText('chmod '+d+' <file>');
  if(ToolBox.showToast)ToolBox.showToast('已复制 chmod '+d+' 命令');
}
calc();'''))

# ============ 8. 按键码 Keycode 查询 ============
TOOLS.append(dict(
    fn='keycode-info.html', icon='⌨️', bg='#e0f2fe',
    title='按键码 Keycode 查询',
    desc='按下任意键，实时显示 event.key / code / keyCode / 修饰键等全部按键信息，附常见按键码速查表，前端开发调试利器。',
    body='''    <div class="input-row" style="align-items:center;">
      <button class="btn primary" id="focusBtn" style="flex:0 0 auto;">🎯 点击后按任意键</button>
      <span style="font-size:13px;color:var(--muted,#6B7280);">焦点在页面上时按下任意键即可捕获（无需输入框）</span>
    </div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:16px;padding:22px;text-align:center;margin-bottom:14px;">
      <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:6px;">event.key</div>
      <div id="keyOut" style="font-size:42px;font-weight:700;color:var(--primary);min-height:52px;line-height:1.2;">—</div>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:14px;">
      <tr style="background:rgba(0,0,0,.04);">
        <td style="padding:8px 10px;font-weight:600;">属性</td><td style="padding:8px 10px;font-weight:600;">值</td><td style="padding:8px 10px;font-weight:600;">说明</td>
      </tr>
      <tr><td style="padding:8px 10px;font-family:monospace;">event.code</td><td id="codeOut" style="padding:8px 10px;font-family:monospace;">—</td><td style="padding:8px 10px;font-size:12px;color:var(--muted,#6B7280);">物理按键位置（推荐）</td></tr>
      <tr><td style="padding:8px 10px;font-family:monospace;">event.key</td><td id="keyRawOut" style="padding:8px 10px;font-family:monospace;">—</td><td style="padding:8px 10px;font-size:12px;color:var(--muted,#6B7280);">按键字符值</td></tr>
      <tr><td style="padding:8px 10px;font-family:monospace;">keyCode (废弃)</td><td id="kcOut" style="padding:8px 10px;font-family:monospace;">—</td><td style="padding:8px 10px;font-size:12px;color:var(--muted,#6B7280);">旧式数字键码，仅兼容用</td></tr>
      <tr><td style="padding:8px 10px;font-family:monospace;">修饰键</td><td id="modOut" style="padding:8px 10px;font-family:monospace;">—</td><td style="padding:8px 10px;font-size:12px;color:var(--muted,#6B7280);">Ctrl/Shift/Alt/Meta</td></tr>
    </table>
    <div class="result-box" id="result"></div>
    <details style="font-size:13px;margin-top:8px;"><summary style="cursor:pointer;font-weight:600;">📋 常见按键码速查（keyCode）</summary>
      <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">
        <tr style="background:rgba(0,0,0,.04);"><td style="padding:6px 8px;font-weight:600;">键</td><td style="padding:6px 8px;font-weight:600;">keyCode</td><td style="padding:6px 8px;font-weight:600;">键</td><td style="padding:6px 8px;font-weight:600;">keyCode</td></tr>
        <tr><td style="padding:6px 8px;">Enter</td><td style="padding:6px 8px;">13</td><td style="padding:6px 8px;">Space</td><td style="padding:6px 8px;">32</td></tr>
        <tr><td style="padding:6px 8px;">Backspace</td><td style="padding:6px 8px;">8</td><td style="padding:6px 8px;">Tab</td><td style="padding:6px 8px;">9</td></tr>
        <tr><td style="padding:6px 8px;">Escape</td><td style="padding:6px 8px;">27</td><td style="padding:6px 8px;">Delete</td><td style="padding:6px 8px;">46</td></tr>
        <tr><td style="padding:6px 8px;">ArrowUp</td><td style="padding:6px 8px;">38</td><td style="padding:6px 8px;">ArrowDown</td><td style="padding:6px 8px;">40</td></tr>
        <tr><td style="padding:6px 8px;">ArrowLeft</td><td style="padding:6px 8px;">37</td><td style="padding:6px 8px;">ArrowRight</td><td style="padding:6px 8px;">39</td></tr>
        <tr><td style="padding:6px 8px;">0-9</td><td style="padding:6px 8px;">48-57</td><td style="padding:6px 8px;">A-Z</td><td style="padding:6px 8px;">65-90</td></tr>
        <tr><td style="padding:6px 8px;">F1-F12</td><td style="padding:6px 8px;">112-123</td><td style="padding:6px 8px;">Shift/Ctrl/Alt</td><td style="padding:6px 8px;">16/17/18</td></tr>
      </table>
    </details>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
var last=null;
window.addEventListener('keydown',function(e){
  if(e.key==='F12'){} // 允许默认
  last=e;
  var key=e.key===' '?'Space':e.key==='\\t'?'Tab':e.key;
  document.getElementById('keyOut').textContent=key;
  document.getElementById('codeOut').textContent=e.code||'—';
  document.getElementById('keyRawOut').textContent=e.key||'—';
  document.getElementById('kcOut').textContent=(e.keyCode||e.which||'—');
  var mods=[];
  if(e.ctrlKey)mods.push('Ctrl');if(e.shiftKey)mods.push('Shift');if(e.altKey)mods.push('Alt');if(e.metaKey)mods.push('Meta');
  document.getElementById('modOut').textContent=mods.join(' + ')||'无';
  document.getElementById('result').innerHTML='<p>捕获到 <code>keydown</code> 事件 · '+(mods.length?mods.join(' + ')+' + ':'')+escH(key)+'</p>';
  if(e.target&&e.target.tagName==='BUTTON')return;
  e.preventDefault();
});
document.addEventListener('DOMContentLoaded',function(){
  var b=document.getElementById('focusBtn');
  if(b)b.addEventListener('click',function(){if(ToolBox.showToast)ToolBox.showToast('已就绪，请按任意键');});
});'''))

# ============ 9. 随机端口生成器 ============
TOOLS.append(dict(
    fn='random-port-generator.html', icon='🌐', bg='#ecfdf5',
    title='随机端口生成器',
    desc='批量生成 1024-65535 随机 TCP/UDP 端口，可自动避开常用保留端口，附常见端口速查表。',
    body='''    <div class="input-row">
      <label>生成数量</label>
      <input type="number" id="count" value="5" min="1" max="20" style="flex:1">
      <label style="flex:0 0 auto;margin:0;"><input type="checkbox" id="skip" checked onchange="gen()"> 避开常用保留端口</label>
    </div>
    <div class="result-box" id="result"></div>
    <div id="portList" style="font-size:15px;line-height:2.2;font-family:'SF Mono','Courier New',monospace;"></div>
    <div class="toolbar">
      <button class="btn primary" onclick="gen()">生成</button>
      <button class="btn" onclick="copyAll()">复制全部</button>
    </div>
    <details style="font-size:13px;margin-top:10px;"><summary style="cursor:pointer;font-weight:600;">📋 常见端口速查</summary>
      <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">
        <tr style="background:rgba(0,0,0,.04);"><td style="padding:6px 8px;font-weight:600;">端口</td><td style="padding:6px 8px;font-weight:600;">服务</td><td style="padding:6px 8px;font-weight:600;">端口</td><td style="padding:6px 8px;font-weight:600;">服务</td></tr>
        <tr><td style="padding:6px 8px;">80</td><td style="padding:6px 8px;">HTTP</td><td style="padding:6px 8px;">443</td><td style="padding:6px 8px;">HTTPS</td></tr>
        <tr><td style="padding:6px 8px;">22</td><td style="padding:6px 8px;">SSH</td><td style="padding:6px 8px;">3306</td><td style="padding:6px 8px;">MySQL</td></tr>
        <tr><td style="padding:6px 8px;">5432</td><td style="padding:6px 8px;">PostgreSQL</td><td style="padding:6px 8px;">6379</td><td style="padding:6px 8px;">Redis</td></tr>
        <tr><td style="padding:6px 8px;">8080</td><td style="padding:6px 8px;">HTTP 备用</td><td style="padding:6px 8px;">3000</td><td style="padding:6px 8px;">Node 开发</td></tr>
        <tr><td style="padding:6px 8px;">27017</td><td style="padding:6px 8px;">MongoDB</td><td style="padding:6px 8px;">9200</td><td style="padding:6px 8px;">Elasticsearch</td></tr>
      </table>
    </details>''',
    script='''var RESERVED=[20,21,22,23,25,53,80,110,123,143,443,465,587,993,995,1080,1433,1521,2375,3000,3306,3389,5432,6379,8080,8443,8888,9000,9200,27017];
var ports=[];
function gen(){
  var n=parseInt(document.getElementById('count').value)||5;if(n<1)n=1;if(n>20)n=20;
  var skip=document.getElementById('skip').checked;
  var rnd=new Uint32Array(1);
  ports=[];
  var guard=0;
  while(ports.length<n&&guard<1000){
    guard++;
    crypto.getRandomValues(rnd);
    var p=1024+(rnd[0]%(65535-1024+1));
    if(skip&&RESERVED.indexOf(p)!==-1)continue;
    if(ports.indexOf(p)===-1)ports.push(p);
  }
  document.getElementById('portList').innerHTML=ports.map(function(p,i){
    return '<div>'+p+' <span style="font-size:12px;color:var(--muted,#9CA3AF);">/tcp·udp</span> <button class="btn" style="padding:1px 10px;font-size:12px;margin-left:6px;" onclick="copyOne('+i+')">复制</button></div>';
  }).join('');
  document.getElementById('result').innerHTML='<p>已生成 <strong>'+ports.length+'</strong> 个随机端口（1024-65535'+(skip?'，已避开常用保留端口':'')+'）</p>';
}
function copyOne(i){ToolBox.copyText(String(ports[i]));if(ToolBox.showToast)ToolBox.showToast('已复制端口 '+ports[i]);}
function copyAll(){if(!ports.length){if(ToolBox.showToast)ToolBox.showToast('请先生成');return;}ToolBox.copyText(ports.join(', '));if(ToolBox.showToast)ToolBox.showToast('已复制全部端口');}
gen();'''))

# ============ 10. SVG 占位图生成器 ============
TOOLS.append(dict(
    fn='svg-placeholder-generator.html', icon='🖼️', bg='#fdf4ff',
    title='SVG 占位图生成器',
    desc='在线生成 SVG 占位图：自定义宽高、文字、背景色与文字色，实时预览，可复制 SVG 代码或下载 .svg 文件，适合原型与文档。',
    body='''    <div class="input-row">
      <div><label>宽度 (px)</label><input type="number" id="w" value="400" min="10" max="2000" oninput="render()"></div>
      <div><label>高度 (px)</label><input type="number" id="h" value="200" min="10" max="2000" oninput="render()"></div>
      <div><label>文字</label><input type="text" id="txt" value="400 × 200" oninput="render()"></div>
    </div>
    <div class="input-row">
      <div><label>背景色</label><input type="color" id="bg" value="#f3f4f6" oninput="render()"></div>
      <div><label>文字色</label><input type="color" id="fg" value="#6b7280" oninput="render()"></div>
      <div style="display:flex;gap:8px;align-items:flex-end;">
        <button class="btn primary" onclick="render()">生成</button>
        <button class="btn" onclick="copySvg()">复制 SVG</button>
        <button class="btn" onclick="downloadSvg()">⬇ 下载</button>
      </div>
    </div>
    <div class="result-box" id="result"></div>
    <div id="preview" style="background:#fff;border:1px dashed var(--border,#E5E7EB);border-radius:12px;padding:18px;margin-bottom:14px;text-align:center;"></div>
    <textarea id="svgCode" readonly style="min-height:120px;font-family:'SF Mono','Courier New',monospace;font-size:12px;" placeholder="SVG 代码将显示在这里..."></textarea>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function render(){
  var w=parseInt(document.getElementById('w').value)||400;if(w<10)w=10;if(w>2000)w=2000;
  var h=parseInt(document.getElementById('h').value)||200;if(h<10)h=10;if(h>2000)h=2000;
  var text=document.getElementById('txt').value||(w+' × '+h);
  var bg=document.getElementById('bg').value||'#f3f4f6';
  var fg=document.getElementById('fg').value||'#6b7280';
  var fs=Math.max(12,Math.min(48,Math.floor(Math.min(w,h)/8)));
  var svg='<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'" role="img">'+
    '<rect width="100%" height="100%" fill="'+bg+'"/>'+
    '<text x="50%" y="50%" fill="'+fg+'" font-size="'+fs+'" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif">'+escH(text)+'</text>'+
    '</svg>';
  document.getElementById('svgCode').value=svg;
  document.getElementById('preview').innerHTML=svg;
  document.getElementById('result').innerHTML='<p>SVG 尺寸 <strong>'+w+' × '+h+'</strong> · 文件约 <strong>'+(new Blob([svg]).size)+'</strong> 字节</p>';
}
function copySvg(){
  var v=document.getElementById('svgCode').value;
  if(!v){if(ToolBox.showToast)ToolBox.showToast('请先生成');return;}
  ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制 SVG 代码');
}
function downloadSvg(){
  var v=document.getElementById('svgCode').value;
  if(!v){if(ToolBox.showToast)ToolBox.showToast('请先生成');return;}
  var blob=new Blob([v],{type:'image/svg+xml'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob);a.download='placeholder.svg';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
  if(ToolBox.showToast)ToolBox.showToast('已下载 placeholder.svg');
}
render();'''))

# ============ 写入 ============
def main():
    for t in TOOLS:
        gen(t['fn'], t['icon'], t['bg'], t['title'], t['desc'],
            t['body'], t['script'], t.get('extra_head', ''))
    print(f'\n共生成 {len(TOOLS)} 个工具 → {OUT_DIR}')

if __name__ == '__main__':
    main()
