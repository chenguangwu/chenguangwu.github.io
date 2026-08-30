#!/usr/bin/env python3
"""it-tools 对标 · 第二梯队生成器（前 6 个）：BIP39助记词/北约音标/OG元标签/BasicAuth/字符串混淆/Email规范化。
用法：python3 scripts/gen_itools_t2.py
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

TOOLS = []

def gen(fn, icon, bg, title, desc, body, script, extra_head=''):
    html = (TPL
        .replace('__ICON__', icon).replace('__BG__', bg)
        .replace('__TITLE__', esc(title)).replace('__DESC__', esc(desc))
        .replace('__FN__', fn).replace('__BODY__', body)
        .replace('__SCRIPT__', script).replace('__EXTRA_HEAD__', extra_head))
    open(os.path.join(OUT_DIR, fn), 'w', encoding='utf-8').write(html)
    print('OK:', os.path.join(OUT_DIR, fn))

# ============ 1. BIP39 助记词生成器 ============
TOOLS.append(dict(
    fn='bip39-generator.html', icon='🪙', bg='#fef9c3',
    title='BIP39 助记词生成器',
    desc='生成符合 BIP39 标准的加密货币助记词（12/15/18/21/24 词）：基于浏览器加密级随机数，支持批量生成，可复制为逗号/空格分隔。',
    extra_head='''<script src="https://cdn.jsdelivr.net/npm/bip39@3.1.0/dist/bip39.min.js"></script>''',
    body='''    <div class="input-row">
      <label>词数</label>
      <select id="words" style="flex:1">
        <option value="12" selected>12 词（128 bit 熵）</option>
        <option value="15">15 词（160 bit）</option>
        <option value="18">18 词（192 bit）</option>
        <option value="21">21 词（224 bit）</option>
        <option value="24">24 词（256 bit）</option>
      </select>
      <label>数量</label>
      <input type="number" id="count" value="1" min="1" max="10" style="flex:1">
    </div>
    <div class="result-box" id="result"></div>
    <div id="mnemList" style="font-size:14px;line-height:2.1;font-family:'SF Mono','Courier New',monospace;word-break:break-all;"></div>
    <div class="toolbar">
      <button class="btn primary" onclick="gen()">生成助记词</button>
      <button class="btn" onclick="copyAll()">复制全部</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">🔒 助记词由 <code>crypto.getRandomValues</code> 在本机生成，绝不上传。请抄写并离线保存，切勿泄露！bip39 库来自 jsdelivr CDN（已内置标准英文词表）。</p>''',
    script='''var list=[];
function gen(){
  var words=parseInt(document.getElementById('words').value)||12;
  var n=parseInt(document.getElementById('count').value)||1;if(n<1)n=1;if(n>10)n=10;
  var out=document.getElementById('result');
  if(!window.bip39){out.innerHTML='<p style="color:var(--danger)">bip39 库加载失败，请检查网络（jsdelivr CDN）</p>';return;}
  var bits=words*11/3*8;
  var entropy=new Uint8Array(bits/8);
  list=[];
  for(var j=0;j<n;j++){
    crypto.getRandomValues(entropy);
    var hex=Array.from(entropy).map(function(b){return b.toString(16).padStart(2,'0');}).join('');
    try{
      var m=bip39.entropyToMnemonic(hex);
      list.push(m);
    }catch(e){out.innerHTML='<p style="color:var(--danger)">生成失败：'+((e&&e.message)||e)+'</p>';return;}
  }
  document.getElementById('mnemList').innerHTML=list.map(function(m,i){
    return '<div style="background:rgba(0,0,0,.03);border-radius:10px;padding:10px 14px;margin-bottom:8px;">'+m+' <button class="btn" style="padding:1px 10px;font-size:12px;margin-left:6px;" onclick="copyOne('+i+')">复制</button></div>';
  }).join('');
  out.innerHTML='<p>已生成 <strong>'+n+'</strong> 组 · <strong>'+words+'</strong> 词助记词（'+bits+' bit 熵）</p>';
}
function copyOne(i){ToolBox.copyText(list[i]);if(ToolBox.showToast)ToolBox.showToast('已复制第 '+(i+1)+' 组');}
function copyAll(){if(!list.length){if(ToolBox.showToast)ToolBox.showToast('请先生成');return;}ToolBox.copyText(list.join('\\n'));if(ToolBox.showToast)ToolBox.showToast('已复制全部 '+list.length+' 组');}'''))

# ============ 2. 北约音标字母转换 ============
TOOLS.append(dict(
    fn='nato-alphabet.html', icon='📻', bg='#e0f2fe',
    title='北约音标字母转换',
    desc='把文本转换为北约音标字母（Alpha/Bravo/Charlie...），支持正反双向转换：字母→音标词、音标词→字母，适合无线电通话、电话报号。',
    body='''    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">方向：</span>
      <label style="flex:0 0 auto;"><input type="radio" name="dir" value="to" checked onchange="convert()"> 字母 → 音标</label>
      <label style="flex:0 0 auto;"><input type="radio" name="dir" value="from" onchange="convert()"> 音标 → 字母</label>
    </div>
    <div class="input-row">
      <textarea id="input" placeholder="字母→音标：输入如 Hello World；音标→字母：输入如 Hotel Echo Lima Lima Oscar" style="min-height:120px" oninput="convert()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:120px" placeholder="转换结果将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="convert()">转换</button>
      <button class="btn" onclick="copyOut()">复制结果</button>
    </div>''',
    script='''var NATO={A:'Alpha',B:'Bravo',C:'Charlie',D:'Delta',E:'Echo',F:'Foxtrot',G:'Golf',H:'Hotel',I:'India',J:'Juliett',K:'Kilo',L:'Lima',M:'Mike',N:'November',O:'Oscar',P:'Papa',Q:'Quebec',R:'Romeo',S:'Sierra',T:'Tango',U:'Uniform',V:'Victor',W:'Whiskey',X:'X-ray',Y:'Yankee',Z:'Zulu'};
var REV={};Object.keys(NATO).forEach(function(k){REV[NATO[k].toLowerCase()]=k;});
function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function convert(){
  var raw=document.getElementById('input').value;
  var toNato=document.querySelector('input[name=dir]:checked').value==='to';
  var out=document.getElementById('result');
  if(!raw.trim()){document.getElementById('output').value='';out.innerHTML='';return;}
  if(toNato){
    var lines=raw.toUpperCase().split(/\\n/);
    var all=[];
    lines.forEach(function(line){
      var parts=[];
      for(var i=0;i<line.length;i++){
        var ch=line[i];
        if(ch===' '){parts.push('|');continue;}
        if(NATO[ch])parts.push(ch+'='+NATO[ch]);
        else if(/\\d/.test(ch))parts.push(ch);
      }
      all.push(parts.join('  '));
    });
    document.getElementById('output').value=raw.toUpperCase().split('').map(function(c){return NATO[c]?NATO[c]:(c===' '?'':c);}).filter(Boolean).join(' ');
    out.innerHTML='<p>✅ 已转换 <strong>'+raw.replace(/\\s/g,'').length+'</strong> 个字母</p>';
  }else{
    var words=raw.trim().split(/[\\s,;]+/).filter(Boolean);
    var letters=words.map(function(w){
      var k=w.toLowerCase().replace(/[^a-z]/g,'');
      if(REV[k])return REV[k];
      if(k.length===1&&/^[a-z]$/.test(k))return k.toUpperCase();
      return '?';
    });
    document.getElementById('output').value=letters.join('');
    out.innerHTML='<p>✅ 已还原 <strong>'+letters.length+'</strong> 个音标词</p>';
  }
}'''))

# ============ 3. OG 元标签生成器 ============
TOOLS.append(dict(
    fn='og-meta-tag-generator.html', icon='🖋️', bg='#fdf4ff',
    title='OG 元标签生成器',
    desc='可视化生成 Open Graph + Twitter Card 全套 meta 标签：标题/描述/图片/URL/类型/站点名，一键复制 HTML，提升社交分享效果。',
    body='''    <div class="input-row">
      <div><label>页面标题</label><input type="text" id="f_title" placeholder="ToolBox - 5000+ 免费在线工具" oninput="build()"></div>
    </div>
    <div class="input-row">
      <div><label>页面描述</label><input type="text" id="f_desc" placeholder="JSON格式化、二维码生成等 6256 个实用工具，纯前端运行" oninput="build()"></div>
    </div>
    <div class="input-row">
      <div><label>图片 URL</label><input type="text" id="f_img" placeholder="https://example.com/og-image.png" oninput="build()"></div>
    </div>
    <div class="input-row">
      <div><label>页面 URL</label><input type="text" id="f_url" placeholder="https://example.com/page" oninput="build()"></div>
      <div><label>类型</label>
        <select id="f_type" onchange="build()" style="flex:1">
          <option value="website">website</option><option value="article">article</option>
          <option value="product">product</option><option value="profile">profile</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>站点名</label><input type="text" id="f_site" placeholder="ToolBox" oninput="build()"></div>
      <div><label>地区</label><input type="text" id="f_locale" value="zh_CN" oninput="build()"></div>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:220px;font-family:'SF Mono','Courier New',monospace;font-size:12.5px;" placeholder="生成的 meta 标签将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="build()">生成</button>
      <button class="btn" onclick="copyOut()">复制 HTML</button>
    </div>''',
    script='''function escA(s){return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;');}
function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('请先填写内容');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制 meta 标签');}
function build(){
  var t=document.getElementById('f_title').value.trim();
  var d=document.getElementById('f_desc').value.trim();
  var img=document.getElementById('f_img').value.trim();
  var url=document.getElementById('f_url').value.trim();
  var type=document.getElementById('f_type').value;
  var site=document.getElementById('f_site').value.trim();
  var loc=document.getElementById('f_locale').value.trim()||'zh_CN';
  if(!t&&!d&&!img&&!url){document.getElementById('output').value='';document.getElementById('result').innerHTML='';return;}
  var L=[];
  L.push('<!-- Open Graph -->');
  L.push('<meta property="og:title" content="'+escA(t||'')+'">');
  L.push('<meta property="og:description" content="'+escA(d||'')+'">');
  if(img)L.push('<meta property="og:image" content="'+escA(img)+'">');
  if(url)L.push('<meta property="og:url" content="'+escA(url)+'">');
  L.push('<meta property="og:type" content="'+type+'">');
  if(site)L.push('<meta property="og:site_name" content="'+escA(site)+'">');
  L.push('<meta property="og:locale" content="'+escA(loc)+'">');
  L.push('');
  L.push('<!-- Twitter Card -->');
  L.push('<meta name="twitter:card" content="'+(img?'summary_large_image':'summary')+'">');
  L.push('<meta name="twitter:title" content="'+escA(t||'')+'">');
  L.push('<meta name="twitter:description" content="'+escA(d||'')+'">');
  if(img)L.push('<meta name="twitter:image" content="'+escA(img)+'">');
  document.getElementById('output').value=L.join('\\n');
  var cnt=L.filter(function(x){return /^<meta/.test(x);}).length;
  document.getElementById('result').innerHTML='<p>✅ 已生成 <strong>'+cnt+'</strong> 条 meta 标签（'+type+'）</p>';
}'''))

# ============ 4. Basic Auth 生成器 ============
TOOLS.append(dict(
    fn='basic-auth-generator.html', icon='🔑', bg='#fffbeb',
    title='Basic Auth 生成器',
    desc='一键生成 HTTP Basic 认证所需的 Authorization 头与 URL 形式：用户名+密码 → Base64 令牌，支持中文用户名，供接口调试与开发使用。',
    body='''    <div class="input-row">
      <div><label>用户名</label><input type="text" id="f_user" placeholder="admin" oninput="generate()"></div>
      <div><label>密码</label><input type="password" id="f_pass" placeholder="••••••" oninput="generate()"></div>
    </div>
    <div class="result-box" id="result"></div>
    <div style="display:flex;flex-direction:column;gap:10px;">
      <div>
        <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:4px;">Authorization 请求头</div>
        <input type="text" id="headerOut" readonly style="font-family:monospace;font-size:13px;padding:10px;border-radius:10px;border:1px solid var(--border,#E5E7EB);width:100%;box-sizing:border-box;">
      </div>
      <div>
        <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:4px;">URL 形式（curl / 浏览器访问）</div>
        <input type="text" id="urlOut" readonly style="font-family:monospace;font-size:13px;padding:10px;border-radius:10px;border:1px solid var(--border,#E5E7EB);width:100%;box-sizing:border-box;">
      </div>
      <div>
        <div style="font-size:12px;color:var(--muted,#6B7280);margin-bottom:4px;">Base64 令牌</div>
        <input type="text" id="tokenOut" readonly style="font-family:monospace;font-size:13px;padding:10px;border-radius:10px;border:1px solid var(--border,#E5E7EB);width:100%;box-sizing:border-box;">
      </div>
    </div>
    <div class="toolbar" style="margin-top:12px;">
      <button class="btn primary" onclick="generate()">生成</button>
      <button class="btn" onclick="copyField('headerOut')">复制请求头</button>
      <button class="btn" onclick="copyField('tokenOut')">复制令牌</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 提示：Basic 认证为明文 Base64（非加密），务必仅在 HTTPS 下使用。curl 示例：<code>curl -u user:pass https://api.example.com</code></p>''',
    script='''function b64(str){try{return btoa(unescape(encodeURIComponent(str)));}catch(e){try{return btoa(str);}catch(e2){return '';}}}
function copyField(id){var el=document.getElementById(id);var v=el.value.trim();if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function generate(){
  var user=document.getElementById('f_user').value;
  var pass=document.getElementById('f_pass').value;
  var out=document.getElementById('result');
  if(!user&&!pass){['headerOut','urlOut','tokenOut'].forEach(function(id){document.getElementById(id).value='';});out.innerHTML='';return;}
  var token=b64(user+':'+pass);
  document.getElementById('headerOut').value='Authorization: Basic '+token;
  document.getElementById('urlOut').value='https://'+encodeURIComponent(user)+':'+encodeURIComponent(pass)+'@example.com/';
  document.getElementById('tokenOut').value=token;
  out.innerHTML='<p>✅ 已生成 Basic 认证信息（令牌 '+token.length+' 字符）</p>';
}'''))

# ============ 5. 字符串混淆器 ============
TOOLS.append(dict(
    fn='string-obfuscator.html', icon='🎭', bg='#f5f3ff',
    title='字符串混淆器',
    desc='把文本转为难以阅读的形式：Unicode 全角、倒序、ROT13、Base64、十六进制转义、HTML 实体，一键复制，常用于代码/脚本混淆。',
    body='''    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">混淆方式：</span>
      <select id="mode" style="flex:2" onchange="obfuscate()">
        <option value="full">Unicode 全角</option>
        <option value="rev">倒序</option>
        <option value="rot13">ROT13</option>
        <option value="b64">Base64</option>
        <option value="hex">\\x 十六进制转义</option>
        <option value="entity">HTML 实体</option>
      </select>
    </div>
    <div class="input-row">
      <textarea id="input" placeholder="输入要混淆的文本，如：Hello World 123" style="min-height:120px" oninput="obfuscate()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:120px" placeholder="混淆结果将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="obfuscate()">混淆</button>
      <button class="btn" onclick="copyOut()">复制结果</button>
    </div>''',
    script='''var FW={'!':'！','"':'＂','#':'＃','$':'＄','%':'％','&':'＆','\\'':'＇','(':'（',')':'）','*':'＊','+':'＋',',':'，','-':'－','.':'．','/':'／',':':'：',';':'；','<':'＜','=':'＝','>':'＞','?':'？','@':'＠','[':'［','\\\\':'＼',']':'］','^':'＾','_':'＿','`':'｀','{':'｛','|':'｜','}':'｝','~':'～',' ':'　'};
function fullwidth(s){
  var r='';
  for(var i=0;i<s.length;i++){
    var c=s[i];
    var code=c.charCodeAt(0);
    if(code>=33&&code<=126)r+=FW[c]||String.fromCharCode(code+0xFEE0);
    else r+=c;
  }
  return r;
}
function rot13(s){return s.replace(/[a-zA-Z]/g,function(c){var base=c<='Z'?65:97;return String.fromCharCode((c.charCodeAt(0)-base+13)%26+base);});}
function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function obfuscate(){
  var text=document.getElementById('input').value;
  var mode=document.getElementById('mode').value;
  var out=document.getElementById('result');
  var result='';
  if(!text){document.getElementById('output').value='';out.innerHTML='';return;}
  switch(mode){
    case 'full': result=fullwidth(text);break;
    case 'rev': result=text.split('').reverse().join('');break;
    case 'rot13': result=rot13(text);break;
    case 'b64': result=btoa(unescape(encodeURIComponent(text)));break;
    case 'hex': result=Array.from(unescape(encodeURIComponent(text))).map(function(c){return '\\\\x'+c.charCodeAt(0).toString(16).padStart(2,'0');}).join('');break;
    case 'entity': result=text.replace(/[<>&"]/g,function(m){return {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m];}).replace(/[^\\x20-\\x7E]/g,function(c){return '&#'+c.charCodeAt(0)+';';});break;
  }
  document.getElementById('output').value=result;
  out.innerHTML='<p>✅ 混淆完成：原文 <strong>'+text.length+'</strong> 字符 → 输出 <strong>'+result.length+'</strong> 字符</p>';
}'''))

# ============ 6. Email 规范化 ============
TOOLS.append(dict(
    fn='email-normalizer.html', icon='📧', bg='#ecfdf5',
    title='Email 规范化',
    desc='清洗邮箱地址：去空格、转小写，并智能处理 Gmail 的点号与 + 标签（Gmail 忽略点号与 + 后缀），避免重复注册与格式错误。',
    body='''    <div class="input-row">
      <input type="text" id="input" placeholder="输入邮箱地址，如： John.Doe+tag @ Gmail.COM" style="flex:2" oninput="normalize()">
      <label style="flex:0 0 auto;margin:0;"><input type="checkbox" id="opt_gmail" checked> 启用 Gmail 点号/+标签归一</label>
    </div>
    <div class="result-box" id="result"></div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
      <div style="flex:1;min-width:200px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:12px;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">规范化前</div>
        <div id="beforeOut" style="font-size:15px;font-weight:600;word-break:break-all;margin-top:4px;">—</div>
      </div>
      <div style="flex:1;min-width:200px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:12px;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">规范化后</div>
        <div id="afterOut" style="font-size:15px;font-weight:600;color:var(--primary);word-break:break-all;margin-top:4px;">—</div>
      </div>
    </div>
    <div class="toolbar">
      <button class="btn primary" onclick="normalize()">规范化</button>
      <button class="btn" onclick="copyAfter()">复制结果</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 Gmail 中 <code>john.doe@gmail.com</code>、<code>johndoe@gmail.com</code>、<code>john.doe+tag@gmail.com</code> 是同一邮箱。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyAfter(){var v=document.getElementById('afterOut').textContent;if(!v||v==='—'){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function normalize(){
  var raw=document.getElementById('input').value;
  var useGmail=document.getElementById('opt_gmail').checked;
  var out=document.getElementById('result');
  document.getElementById('beforeOut').textContent=raw.trim()||'—';
  if(!raw.trim()){document.getElementById('afterOut').textContent='—';out.innerHTML='';return;}
  var notes=[];
  var lower=raw.trim().toLowerCase();
  if(raw.trim()!==lower)notes.push('已转小写');
  var at=lower.lastIndexOf('@');
  if(at<=0){document.getElementById('afterOut').textContent='❌ 无效邮箱';out.innerHTML='<p style="color:var(--danger)">缺少 @ 符号，不是有效邮箱</p>';return;}
  var local=lower.slice(0,at),domain=lower.slice(at+1);
  if(!/^[a-z0-9.!#$%&\'*+/=?^_`{|}~-]+$/.test(local)||!/^[a-z0-9.-]+\\.[a-z]{2,}$/.test(domain)){
    document.getElementById('afterOut').textContent='❌ 无效邮箱';
    out.innerHTML='<p style="color:var(--danger)">邮箱格式无效（本地名或域名不合法）</p>';return;
  }
  var isGmail=/gmail\\.com$/.test(domain)||/googlemail\\.com$/.test(domain);
  if(useGmail&&isGmail){
    var before=local;
    local=local.replace(/\\./g,'').split('+')[0];
    if(local!==before)notes.push('已去除 Gmail 点号与 + 标签');
  }
  var result=local+'@'+domain;
  document.getElementById('afterOut').textContent=result;
  out.innerHTML='<p>✅ 规范化完成'+(notes.length?'：<strong>'+escH(notes.join('；'))+'</strong>':'')+'</p>';
}'''))

# ============ 8. 列表转换器 ============
TOOLS.append(dict(
    fn='list-converter.html', icon='📋', bg='#f0fdfa',
    title='列表转换器',
    desc='把逐行列表一键转为各种格式：逗号分隔、JSON 数组、SQL IN 子句、HTML 列表、引号包裹、竖线分隔、CSV，开发数据处理必备。',
    body='''    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">输出格式：</span>
      <select id="mode" style="flex:2" onchange="convert()">
        <option value="comma">逗号分隔</option>
        <option value="quote">带引号（"a","b"）</option>
        <option value="json">JSON 数组</option>
        <option value="sql">SQL IN 子句</option>
        <option value="csv">CSV 行</option>
        <option value="html">HTML &lt;li&gt; 列表</option>
        <option value="pipe">竖线分隔</option>
        <option value="bullet">Markdown 列表</option>
      </select>
    </div>
    <div class="input-row">
      <textarea id="input" placeholder="每行一个项目，如：&#10;apple&#10;banana&#10;cherry" style="min-height:150px" oninput="convert()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <textarea id="output" readonly style="min-height:150px" placeholder="转换结果将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="convert()">转换</button>
      <button class="btn" onclick="copyOut()">复制结果</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function convert(){
  var lines=document.getElementById('input').value.split(/\\r?\\n/).map(function(s){return s.trim();}).filter(Boolean);
  var mode=document.getElementById('mode').value;
  var out=document.getElementById('result');
  var result='';
  if(!lines.length){document.getElementById('output').value='';out.innerHTML='';return;}
  switch(mode){
    case 'comma': result=lines.join(', ');break;
    case 'quote': result=lines.map(function(v){return '"'+v.replace(/"/g,'\\\\"')+'"';}).join(', ');break;
    case 'json': result=JSON.stringify(lines,null,2);break;
    case 'sql': result='('+lines.map(function(v){return "'"+v.replace(/'/g,"''")+"'";}).join(', ')+')';break;
    case 'csv': result=lines.map(function(v){return '"'+v.replace(/"/g,'""')+'"';}).join('\\n');break;
    case 'html': result=lines.map(function(v){return '<li>'+escH(v)+'</li>';}).join('\\n');break;
    case 'pipe': result=lines.join(' | ');break;
    case 'bullet': result=lines.map(function(v){return '- '+v;}).join('\\n');break;
  }
  document.getElementById('output').value=result;
  out.innerHTML='<p>✅ 已转换 <strong>'+lines.length+'</strong> 个项目</p>';
}'''))

# ============ 9. Numeronym 数字缩写生成器 ============
TOOLS.append(dict(
    fn='numeronym-generator.html', icon='🔢', bg='#fff1f2',
    title='Numeronym 数字缩写',
    desc='把单词转换为数字缩写（首字母+中间字符数+尾字母）：internationalization → i18n、accessibility → a11y，批量转换整段文本。',
    body='''    <div class="input-row">
      <textarea id="input" placeholder="输入文本，如：internationalization accessibility localization" style="min-height:120px" oninput="generate()"></textarea>
    </div>
    <div class="result-box" id="result"></div>
    <div style="background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:14px;margin-bottom:12px;font-size:18px;font-weight:700;color:var(--primary);word-break:break-all;" id="outBig">—</div>
    <textarea id="output" readonly style="min-height:100px" placeholder="逐词对照将显示在这里..."></textarea>
    <div class="toolbar">
      <button class="btn primary" onclick="generate()">生成</button>
      <button class="btn" onclick="copyOut()">复制结果</button>
    </div>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function copyOut(){var v=document.getElementById('output').value;if(!v){if(ToolBox.showToast)ToolBox.showToast('结果为空');return;}ToolBox.copyText(v);if(ToolBox.showToast)ToolBox.showToast('已复制');}
function numeronym(w){
  var alpha=w.replace(/[^A-Za-z]/g,'');
  if(alpha.length<=2)return w;
  var first=w[0],last=w[w.length-1];
  return first+(alpha.length-2)+last;
}
function generate(){
  var text=document.getElementById('input').value;
  var out=document.getElementById('result');
  if(!text.trim()){document.getElementById('outBig').textContent='—';document.getElementById('output').value='';out.innerHTML='';return;}
  var words=text.split(/\\s+/);
  var result=words.map(numeronym).join(' ');
  document.getElementById('outBig').textContent=result;
  var mapping=words.map(function(w){
    var n=numeronym(w);
    return w!==n?w+' → '+n:w;
  }).join('\\n');
  document.getElementById('output').value=mapping;
  out.innerHTML='<p>✅ 已转换 <strong>'+words.length+'</strong> 个单词</p>';
}'''))

# ============ 10. Benchmark 基准测试 ============
TOOLS.append(dict(
    fn='benchmark-builder.html', icon='⚡', bg='#fef3e2',
    title='Benchmark 基准测试',
    desc='在线测量浏览器 JavaScript 运算性能：整数/浮点/字符串/数组/对象五种负载，每秒操作数（ops/sec）对比，一键复制测试代码。',
    body='''    <div class="input-row" style="align-items:center;">
      <span style="white-space:nowrap;font-size:13px;">负载类型：</span>
      <select id="type" style="flex:2" onchange="stopRun()">
        <option value="int">整数运算</option>
        <option value="float">浮点运算</option>
        <option value="str">字符串处理</option>
        <option value="array">数组操作</option>
        <option value="object">对象操作</option>
      </select>
      <span style="white-space:nowrap;font-size:13px;">时长</span>
      <select id="ms" style="flex:1">
        <option value="1000">1 秒</option>
        <option value="2000">2 秒</option>
        <option value="5000">5 秒</option>
      </select>
    </div>
    <div class="result-box" id="result"></div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px;">
      <div style="flex:1;min-width:160px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:14px;text-align:center;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">运行耗时</div>
        <div id="msOut" style="font-size:24px;font-weight:700;color:var(--primary);">—</div>
      </div>
      <div style="flex:1;min-width:160px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:14px;text-align:center;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">运算次数</div>
        <div id="opsOut" style="font-size:24px;font-weight:700;color:var(--primary);">—</div>
      </div>
      <div style="flex:1;min-width:160px;background:var(--bg,#FFFAF7);border:1px solid var(--border,#E5E7EB);border-radius:12px;padding:14px;text-align:center;">
        <div style="font-size:12px;color:var(--muted,#6B7280);">性能（ops/sec）</div>
        <div id="rateOut" style="font-size:24px;font-weight:700;color:var(--primary);">—</div>
      </div>
    </div>
    <div class="toolbar">
      <button class="btn primary" id="runBtn" onclick="run()">▶ 开始测试</button>
      <button class="btn" onclick="copyCode()">复制测试代码</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 测试运行期间页面可能短暂卡顿，属正常现象。结果受浏览器/设备影响，仅供参考。</p>''',
    script='''var running=false,stopFlag=false;
function stopRun(){running=false;stopFlag=true;var b=document.getElementById('runBtn');if(b){b.textContent='▶ 开始测试';b.disabled=false;}}
function run(){
  if(running)return;
  running=true;stopFlag=false;
  var type=document.getElementById('type').value;
  var duration=parseInt(document.getElementById('ms').value)||1000;
  var btn=document.getElementById('runBtn');
  btn.textContent='⏳ 测试中...';btn.disabled=true;
  setTimeout(function(){
    var start=performance.now(),ops=0;
    var guard=function(){return stopFlag;};
    try{
      while(!stopFlag&&performance.now()-start<duration){
        switch(type){
          case 'int':{var s=0;for(var i=0;i<500;i++)s+=i*i;ops++;}break;
          case 'float':{var f=0;for(var j=0;j<500;j++)f+=Math.sin(j)*Math.cos(j)+Math.sqrt(j+1);ops++;}break;
          case 'str':{var t='';for(var k=0;k<100;k++)t+='str'+k;var len=t.length;ops++;}break;
          case 'array':{var a=[];for(var m=0;m<200;m++)a.push(m);a.sort(function(x,y){return y-x;});ops++;}break;
          case 'object':{var o={};for(var n=0;n<200;n++)o['k'+n]=n;var keys=Object.keys(o).length;ops++;}break;
        }
      }
    }catch(e){}
    var elapsed=performance.now()-start;
    var rate=elapsed>0?Math.round(ops*1000/elapsed):0;
    document.getElementById('msOut').textContent=elapsed.toFixed(0)+' ms';
    document.getElementById('opsOut').textContent=ops.toLocaleString();
    document.getElementById('rateOut').textContent=rate.toLocaleString()+' ops/s';
    var score=rate>1000000?'🚀 极快':rate>100000?'💪 很快':rate>10000?'👍 正常':rate>1000?'🐢 偏慢':'🪫 较慢（可能后台占用）';
    document.getElementById('result').innerHTML='<p>'+score+' · '+type+' 负载完成（'+elapsed.toFixed(0)+'ms / '+ops.toLocaleString()+' ops）</p>';
    running=false;btn.textContent='▶ 开始测试';btn.disabled=false;
  },30);
}
function copyCode(){
  var code='// Benchmark 测试片段（'+document.getElementById('type').value+'）\\nvar start=performance.now(),ops=0;\\nwhile(performance.now()-start<1000){\\n  // 在此放入被测代码\\n  ops++;\\n}\\nconsole.log(ops+" ops/sec");';
  ToolBox.copyText(code);if(ToolBox.showToast)ToolBox.showToast('已复制测试代码');
}'''))

# ============ 11. 摄像头录制 ============
TOOLS.append(dict(
    fn='camera-recorder.html', icon='📹', bg='#f1f5f9',
    title='摄像头录制',
    desc='浏览器内直接调用摄像头录制视频（WebM 格式）：实时预览、开始/停止、下载录制文件，全程本地录制，数据不上传。',
    body='''    <div class="result-box" id="result"></div>
    <div style="background:#000;border-radius:16px;overflow:hidden;margin-bottom:14px;">
      <video id="preview" autoplay playsinline muted style="width:100%;max-height:380px;display:block;"></video>
    </div>
    <div class="toolbar">
      <button class="btn primary" id="startBtn" onclick="startRec()">🎥 开始录制</button>
      <button class="btn danger" id="stopBtn" onclick="stopRec()" disabled>⏹ 停止并下载</button>
      <button class="btn" onclick="stopStream()">关闭摄像头</button>
    </div>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">🔒 视频仅在本地录制与保存，不会上传任何服务器。首次使用需授予摄像头/麦克风权限。录制格式为 WebM（Chrome/Edge/Firefox 支持）。</p>''',
    script='''var mediaRecorder=null,chunks=[],stream=null;
function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function startRec(){
  var out=document.getElementById('result');
  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){
    out.innerHTML='<p style="color:var(--danger)">当前浏览器不支持摄像头访问（需 HTTPS 环境）</p>';return;
  }
  navigator.mediaDevices.getUserMedia({video:true,audio:true}).then(function(s){
    stream=s;
    var v=document.getElementById('preview');
    v.srcObject=s;v.play().catch(function(){});
    if(window.MediaRecorder){
      chunks=[];
      mediaRecorder=new MediaRecorder(s);
      mediaRecorder.ondataavailable=function(e){if(e.data&&e.data.size)chunks.push(e.data);};
      mediaRecorder.onstop=function(){
        var blob=new Blob(chunks,{type:'video/webm'});
        var a=document.createElement('a');
        a.href=URL.createObjectURL(blob);
        a.download='recording-'+Date.now()+'.webm';
        document.body.appendChild(a);a.click();document.body.removeChild(a);
        URL.revokeObjectURL(a.href);
        out.innerHTML='<p style="color:var(--success)">✅ 录制完成，已下载 '+Math.round(blob.size/1024)+' KB 视频文件</p>';
      };
      mediaRecorder.start(250);
      document.getElementById('startBtn').disabled=true;
      document.getElementById('stopBtn').disabled=false;
      out.innerHTML='<p style="color:var(--success)">🔴 正在录制...</p>';
    }else{
      out.innerHTML='<p style="color:var(--warning)">当前浏览器不支持 MediaRecorder，仅可预览</p>';
    }
  }).catch(function(e){
    out.innerHTML='<p style="color:var(--danger)">无法访问摄像头：'+escH((e&&e.message)||e)+'（请检查权限设置）</p>';
  });
}
function stopRec(){
  var out=document.getElementById('result');
  if(mediaRecorder&&mediaRecorder.state!=='inactive')mediaRecorder.stop();
  if(stream)stream.getTracks().forEach(function(t){t.stop();});
  mediaRecorder=null;stream=null;
  document.getElementById('startBtn').disabled=false;
  document.getElementById('stopBtn').disabled=true;
  document.getElementById('preview').srcObject=null;
  if(out.innerHTML.indexOf('正在录制')>-1)out.innerHTML='';
}
function stopStream(){
  stopRec();
}'''))

# ============ 12. PDF 签名检查 ============
TOOLS.append(dict(
    fn='pdf-signature-checker.html', icon='📜', bg='#faf5ff',
    title='PDF 签名检查',
    desc='检查 PDF 文件是否包含数字签名：解析 PDF 内部的 ByteRange 与 Contents 引用，识别签名存在性（不做密码学验证），纯本地解析不上传。',
    body='''    <div class="input-row">
      <input type="file" id="file" accept=".pdf,application/pdf" onchange="check()" style="flex:2">
    </div>
    <div class="result-box" id="result"></div>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr style="background:rgba(0,0,0,.04);"><td style="padding:8px 10px;font-weight:600;">检查项</td><td style="padding:8px 10px;font-weight:600;">结果</td></tr>
      <tr><td style="padding:8px 10px;">文件大小</td><td id="d_size" style="padding:8px 10px;">—</td></tr>
      <tr><td style="padding:8px 10px;">PDF 头</td><td id="d_head" style="padding:8px 10px;">—</td></tr>
      <tr><td style="padding:8px 10px;">/ByteRange 签名引用</td><td id="d_br" style="padding:8px 10px;">—</td></tr>
      <tr><td style="padding:8px 10px;">/Contents 签名值</td><td id="d_ct" style="padding:8px 10px;">—</td></tr>
      <tr><td style="padding:8px 10px;">签名区域字节数</td><td id="d_bytes" style="padding:8px 10px;">—</td></tr>
    </table>
    <p style="font-size:12px;color:var(--muted,#9CA3AF);margin-top:10px;">💡 本工具检测签名"是否存在"（基于 PDF 结构），不做签名内容有效性验证。文件仅在本机解析，绝不上传。</p>''',
    script='''function escH(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function fmtSize(n){return n<1024?n+' B':n<1048576?(n/1024).toFixed(1)+' KB':(n/1048576).toFixed(2)+' MB';}
function setCell(id,v,color){var el=document.getElementById(id);el.textContent=v;el.style.color=color||'';}
function check(){
  var out=document.getElementById('result');
  var f=document.getElementById('file').files[0];
  if(!f){out.innerHTML='';return;}
  setCell('d_size',fmtSize(f.size));
  var reader=new FileReader();
  reader.onload=function(e){
    var buf=new Uint8Array(e.target.result);
    var head='%PDF-'+(buf[5]||'')+'.'+(buf[6]||'');
    setCell('d_head',head,/^%PDF-\\d$/.test(head)?'var(--success)':'var(--danger)');
    var text='';
    for(var i=0;i<buf.length;i++)text+=String.fromCharCode(buf[i]);
    var br=/\\/ByteRange\\s*\\[\\s*(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\\]/.exec(text);
    var ct=/\\/Contents\\s*\\[?\\s*(<[0-9A-Fa-f\\s]+>|\\d+)\\s*\\]?/.exec(text);
    if(br){setCell('d_br',br[0].replace(/\\s+/g,' '),'var(--success)');setCell('d_bytes',(parseInt(br[4],10)-parseInt(br[3],10))+' bytes','var(--success)');}
    else{setCell('d_br','未找到','var(--danger)');setCell('d_bytes','—');}
    if(ct){setCell('d_ct','已找到（'+ct[1].replace(/\\s+/g,'').length+' hex 字符）','var(--success)');}
    else{setCell('d_ct','未找到','var(--danger)');}
    if(br&&ct){
      out.innerHTML='<p style="color:var(--success)">✅ 检测到数字签名：文件包含 PDF 签名结构（ByteRange + Contents）</p><p style="font-size:12px;color:var(--muted,#6B7280);">注：仅确认签名存在，未做签名有效性/证书链验证</p>';
    }else{
      out.innerHTML='<p style="color:var(--warning)">⚠️ 未检测到数字签名（该 PDF 可能未签名）</p>';
    }
  };
  reader.readAsArrayBuffer(f);
}'''))

def main():
    for t in TOOLS:
        gen(t['fn'], t['icon'], t['bg'], t['title'], t['desc'], t['body'], t['script'], t.get('extra_head',''))
    print(f'\\n第二梯队前 6 个已生成 → {OUT_DIR}')

if __name__ == '__main__':
    main()
