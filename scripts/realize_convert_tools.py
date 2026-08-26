#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROADMAP 批次5 · KEEP 真实实现：把占位 convert 伪工具重写为真实可用工具。

两种模式：
  factor : 对称线性单位换算。option value = 该单位相对基准单位的因子，calc: r = v*f/t
  algo   : 非对称/算法/查表换算。整块替换卡片输入区与 calc 逻辑

幂等：每个文件用哨兵标记 <!-- TOOLBOX-REALIZED --> 防重复注入。
用法：
  python3 scripts/realize_convert_tools.py [--dry-run] [--only 相对路径] [--limit N]
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = {
  # ===== factor 模式（对称线性标准换算）=====
  'ballistics/convert-45.html': ('factor', [('毫米 (mm)',1),('英寸 (in)',25.4)], '毫米 / 英寸 口径互转（1 in = 25.4 mm）'),
  'jewelry/convert-31.html': ('factor', [('K金',1),('纯度 (%)',100/24)], 'K金与纯度百分比互转（24K ≈ 100%）'),
  'fitness/convert.html': ('factor', [('分钟/公里',1),('分钟/英里',1.609344)], '跑步配速 分钟/公里 ↔ 分钟/英里（1 mi = 1.609344 km）'),
  'medical/convert-glucose.html': ('factor', [('mmol/L',1),('mg/dL',18)], '血糖 mmol/L ↔ mg/dL（×18）'),
  'general/convert-22.html': ('factor', [('无 (基准)',1),('十 (da)',1e1),('百 (h)',1e2),('千 (k)',1e3),('兆 (M)',1e6),('吉 (G)',1e9),('分 (d)',1e-1),('厘 (c)',1e-2),('毫 (m)',1e-3),('微 (µ)',1e-6),('纳 (n)',1e-9)], 'SI 单位词头换算（10 的幂次）'),

  # ===== algo 模式（确定正确的编码/格式/算法换算）=====
  'edu/convert-3.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">二进制 / 八进制 / 十进制 / 十六进制 / 三十六进制 互转</p>\n'
    '<div class="input-row"><div><label>输入数值</label><input type="text" id="val" value="1010" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从进制</label><select id="from" onchange="calc()"><option value="2">二进制 (2)</option><option value="8">八进制 (8)</option><option value="10">十进制 (10)</option><option value="16">十六进制 (16)</option><option value="36">三十六进制 (36)</option></select></div>\n'
    '<div><label>到进制</label><select id="to" onchange="calc()"><option value="2">二进制 (2)</option><option value="8">八进制 (8)</option><option value="10" selected>十进制 (10)</option><option value="16">十六进制 (16)</option><option value="36">三十六进制 (36)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=(document.getElementById('val').value||'').trim();var f=+document.getElementById('from').value;var t=+document.getElementById('to').value;var out='';try{var dec=parseInt(v,f);if(v===''||isNaN(dec)){out='请输入有效的'+f+'进制数';}else{out=dec.toString(t).toUpperCase();}}catch(e){out='输入无效';}document.getElementById('res').innerHTML='<p style=\"font-size:20px;color:var(--primary);\"><strong>'+out+'</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+f+' → '+t+' 进制</p>';}calc();function copyRes(){ToolBox.copyText(document.getElementById('res').innerText);}"),

  'edu/convert-2.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">HEX / RGB / HSL / CMYK 颜色代码互转</p>\n'
    '<div class="input-row"><div><label>输入颜色值</label><input type="text" id="val" value="#FF6B35" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从格式</label><select id="from" onchange="calc()"><option value="hex" selected>HEX</option><option value="rgb">RGB</option><option value="hsl">HSL</option><option value="cmyk">CMYK</option></select></div>\n'
    '<div><label>到格式</label><select id="to" onchange="calc()"><option value="hex">HEX</option><option value="rgb" selected>RGB</option><option value="hsl">HSL</option><option value="cmyk">CMYK</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function hexToRgb(h){h=h.replace('#','');if(h.length===3)h=h.split('').map(function(c){return c+c;}).join('');var n=parseInt(h,16);return [n>>16&255,n>>8&255,n&255];}\n"
    "function rgbToHex(r,g,b){return '#'+[r,g,b].map(function(x){var s=('0'+Math.round(x).toString(16)).slice(-2);return s;}).join('').toUpperCase();}\n"
    "function rgbToHsl(r,g,b){r/=255;g/=255;b/=255;var mx=Math.max(r,g,b),mn=Math.min(r,g,b),h,s,l=(mx+mn)/2;if(mx===mn){h=s=0;}else{var d=mx-mn;if(l>0.5)s=d/(2-mx-mn);else s=d/(mx+mn);switch(mx){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;default:h=(r-g)/d+4;}h/=6;}return [Math.round(h*360),Math.round(s*100),Math.round(l*100)];}\n"
    "function hslToRgb(h,s,l){h/=360;s/=100;l/=100;var r,g,b;if(s===0){r=g=b=l;}else{var q=l<0.5?l*(1+s):l+s-l*s;var p=2*l-q;var hu=function(t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;};r=hu(h+1/3);g=hu(h);b=hu(h-1/3);}return [r*255,g*255,b*255];}\n"
    "function rgbToCmyk(r,g,b){r/=255;g/=255;b/=255;var k=1-Math.max(r,g,b);if(k===1)return [0,0,0,100];var c=(1-r-k)/(1-k),m=(1-g-k)/(1-k),y=(1-b-k)/(1-k);return [Math.round(c*100),Math.round(m*100),Math.round(y*100),Math.round(k*100)];}\n"
    "function cmykToRgb(c,m,y,k){c/=100;m/=100;y/=100;k/=100;var r=255*(1-c)*(1-k),g=255*(1-m)*(1-k),b=255*(1-y)*(1-k);return [r,g,b];}\n"
    "function parseRgb(s){var m=s.match(/[\\d.]+/g);return m?m.slice(0,3).map(Number):null;}\n"
    "function parseHsl(s){var m=s.match(/[\\d.]+/g);return m?m.slice(0,3).map(Number):null;}\n"
    "function parseCmyk(s){var m=s.match(/[\\d.]+/g);return m?m.slice(0,4).map(Number):null;}\n"
    "function calc(){var v=(document.getElementById('val').value||'').trim();var from=document.getElementById('from').value;var to=document.getElementById('to').value;var rgb,out='';try{if(from==='hex'){rgb=hexToRgb(v);}else if(from==='rgb'){rgb=parseRgb(v);}else if(from==='hsl'){rgb=hslToRgb.apply(null,parseHsl(v));}else{rgb=cmykToRgb.apply(null,parseCmyk(v));}if(!rgb){out='输入无效';}else if(to==='hex'){out=rgbToHex(rgb[0],rgb[1],rgb[2]);}else if(to==='rgb'){out='rgb('+Math.round(rgb[0])+', '+Math.round(rgb[1])+', '+Math.round(rgb[2])+')';}else if(to==='hsl'){var h=rgbToHsl(rgb[0],rgb[1],rgb[2]);out='hsl('+h[0]+', '+h[1]+'%, '+h[2]+'%)';}else{var c=rgbToCmyk(rgb[0],rgb[1],rgb[2]);out='cmyk('+c[0]+'%, '+c[1]+'%, '+c[2]+'%, '+c[3]+'%)';}}catch(e){out='输入无效';}document.getElementById('res').innerHTML='<p style=\"font-size:18px;color:var(--primary);\"><strong>'+out+'</strong></p>';}calc();function copyRes(){ToolBox.copyText(document.getElementById('res').innerText);}"),

  'network/convert-11.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">IPv4 点分十进制 ↔ 二进制串 ↔ 十进制整数</p>\n'
    '<div class="input-row"><div><label>输入</label><input type="text" id="val" value="192.168.1.1" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从格式</label><select id="from" onchange="calc()"><option value="dot" selected>点分十进制</option><option value="bin">二进制串</option><option value="dec">十进制整数</option></select></div>\n'
    '<div><label>到格式</label><select id="to" onchange="calc()"><option value="dot">点分十进制</option><option value="bin" selected>二进制串</option><option value="dec">十进制整数</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function toBin32(n){var s='';for(var i=31;i>=0;i--){s+=((n>>i)&1);if(i%8===0&&i>0)s+='.';}return s;}\n"
    "function calc(){var v=(document.getElementById('val').value||'').trim();var from=document.getElementById('from').value;var to=document.getElementById('to').value;var dec,out='';try{if(from==='dot'){var ps=v.split('.');if(ps.length!==4||ps.some(function(x){return x===''||+x<0||+x>255;})){out='IPv4 格式无效';}else{dec=ps.reduce(function(a,x){return a*256+(+x);},0);}}else if(from==='bin'){var bs=v.replace(/\\./g,'');if(bs.length!==32||/[^01]/.test(bs)){out='二进制串应为32位0/1';}else{dec=parseInt(bs,2);}}else{dec=parseInt(v,10);if(isNaN(dec)||dec<0||dec>4294967295)out='整数超出 IPv4 范围';}if(out===''){if(to==='dot'){out=[(dec>>24)&255,(dec>>16)&255,(dec>>8)&255,dec&255].join('.');}else if(to==='bin'){out=toBin32(dec);}else{out=dec.toString(10);}}}catch(e){out='输入无效';}document.getElementById('res').innerHTML='<p style=\"font-size:18px;color:var(--primary);\"><strong>'+out+'</strong></p>';}calc();function copyRes(){ToolBox.copyText(document.getElementById('res').innerText);}"),

  'text/convert-6.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">小写 / 大写 / 首字母大写 文本转换</p>\n'
    '<div class="input-row"><div><label>输入文本</label><textarea id="val" rows="3" style="width:100%;" oninput="calc()">Hello World</textarea></div></div>\n'
    '<div class="input-row"><div><label>转换目标</label><select id="to" onchange="calc()"><option value="upper">全大写 (UPPER)</option><option value="lower" selected>全小写 (lower)</option><option value="title">首字母大写 (Title)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=document.getElementById('val').value||'';var to=document.getElementById('to').value;var out='';if(to==='upper'){out=v.toUpperCase();}else if(to==='lower'){out=v.toLowerCase();}else{out=v.replace(/\\b\\w/g,function(c){return c.toUpperCase();});}document.getElementById('res').innerHTML='<p style=\"font-size:16px;color:var(--primary);white-space:pre-wrap;\"><strong>'+out.replace(/</g,'&lt;')+'</strong></p>';}calc();function copyRes(){ToolBox.copyText(document.getElementById('res').innerText);}"),

  'general/convert-21.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">普通数字 ↔ 科学记数法（标准 ↔ 十进制指数）</p>\n'
    '<div class="input-row"><div><label>输入数值</label><input type="text" id="val" value="12345" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从格式</label><select id="from" onchange="calc()"><option value="num" selected>普通数字</option><option value="sci">科学记数法</option></select></div>\n'
    '<div><label>到格式</label><select id="to" onchange="calc()"><option value="num">普通数字</option><option value="sci" selected>科学记数法</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=(document.getElementById('val').value||'').trim();var from=document.getElementById('from').value;var to=document.getElementById('to').value;var num,out='';try{num=Number(v);if(v===''||!isFinite(num)){out='请输入有效数字';}else{if(to==='sci'){out=num.toExponential(4).replace('e',' × 10^').replace('^+','^').replace('E',' × 10^');out=num.toExponential(4);}else{out=String(num);}}}catch(e){out='输入无效';}document.getElementById('res').innerHTML='<p style=\"font-size:18px;color:var(--primary);\"><strong>'+out+'</strong></p>';}calc();function copyRes(){ToolBox.copyText(document.getElementById('res').innerText);}"),

  # ===== KEEP-2 factor（对称线性标准换算）=====
  'food-testing/convert-37.html': ('factor', [('氮含量 (%)',1),('蛋白质 (%)',6.25)], '蛋白质含量 = 氮含量 × 6.25（凯氏定氮通用换算系数）'),
  'shipping/convert-speed-1.html': ('factor', [('节 (kn)',1),('千米/时 (km/h)',1.852)], '航速 节 ↔ 千米/时（1 kn = 1.852 km/h）'),
  'energy/convert-emission.html': ('factor', [('CO₂',1),('CH₄（100年）',28),('N₂O（100年）',265),('SF₆',22800)], '温室气体 CO₂ 当量（CO₂e = 质量 × GWP，IPCC AR5 100年值；同质量下互转）'),

  # ===== KEEP-2 algo（确定公式/算法真实实现）=====
  'clinical-lab/convert-39.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">INR（国际标准化比值）= (受试者 PT / 正常对照 PT) ^ ISI</p>\n'
    '<div class="input-row"><div><label>受试者 PT (秒)</label><input type="number" id="pt" value="25" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>正常对照 PT (秒)</label><input type="number" id="ctrl" value="12" oninput="calc()"></div>\n'
    '<div><label>ISI（试剂敏感指数）</label><input type="number" id="isi" value="1.0" step="0.1" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var pt=+document.getElementById('pt').value||0;var ctrl=+document.getElementById('ctrl').value||0;var isi=+document.getElementById('isi').value||0;var out='';if(pt<=0||ctrl<=0||isi<=0){out='请输入有效正数';}else{var inr=Math.pow(pt/ctrl,isi);out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+inr.toFixed(2)+'</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">INR = ('+pt+' / '+ctrl+')^'+isi+'</p><p style=\"font-size:12px;color:var(--text-muted);\">仅供换算理解，不作诊断依据</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'gis/convert-angle-slope-1.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">坡度 百分比 ↔ 角度（tan 关系）</p>\n'
    '<div class="input-row"><div><label>输入值</label><input type="number" id="val" value="10" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从</label><select id="from" onchange="calc()"><option value="pct" selected>百分比 (%)</option><option value="deg">角度 (°)</option></select></div>\n'
    '<div><label>到</label><select id="to" onchange="calc()"><option value="pct">百分比 (%)</option><option value="deg" selected>角度 (°)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var from=document.getElementById('from').value;var to=document.getElementById('to').value;var out='';if(v<0){out='坡度应非负';}else{var pct,deg;if(from==='pct'){pct=v;deg=Math.atan(v/100)*180/Math.PI;}else{deg=v;pct=Math.tan(v*Math.PI/180)*100;}var res=(to==='pct')?pct:deg;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+res.toFixed(2)+' '+(to==='pct'?'%':'°')+'</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'ophthalmology/convert-42.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">视力 小数 / logMAR / Snellen(20/x) 互转</p>\n'
    '<div class="input-row"><div><label>输入值</label><input type="number" id="val" value="1.0" step="0.01" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>输入类型</label><select id="from" onchange="calc()"><option value="dec" selected>小数视力</option><option value="log">logMAR</option><option value="sn">Snellen 分母 x</option></select></div>\n'
    '<div><label>到</label><select id="to" onchange="calc()"><option value="dec">小数视力</option><option value="log" selected>logMAR</option><option value="sn">Snellen</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value;var from=document.getElementById('from').value;var to=document.getElementById('to').value;var dec;if(from==='dec'){dec=v;}else if(from==='log'){dec=Math.pow(10,-v);}else{dec=20/v;}var r;if(to==='dec'){r=dec;}else if(to==='log'){r=(dec<=0)?NaN:-Math.log10(dec);}else{r=20/dec;}var unit=(to==='dec')?'':(to==='log'?' logMAR':' (Snellen 20/'+Math.round(r)+')');document.getElementById('res').innerHTML='<p style=\"font-size:20px;color:var(--primary);\"><strong>'+(isFinite(r)?r.toFixed(2):'无效')+'</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+unit+'</p>';}calc();"),

  'niche/convert-fps.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">视频帧数 ↔ 时长（秒），需帧率 fps</p>\n'
    '<div class="input-row"><div><label>数值</label><input type="number" id="val" value="30" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>帧率 fps</label><input type="number" id="fps" value="30" oninput="calc()"></div></div>\n'
    '<div><label>方向</label><select id="mode" onchange="calc()"><option value="f2s" selected>帧 → 秒</option><option value="s2f">秒 → 帧</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var fps=+document.getElementById('fps').value||0;var mode=document.getElementById('mode').value;var out='';if(fps<=0){out='帧率需>0';}else{var r=(mode==='f2s')?v/fps:v*fps;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r.toFixed(2)+' '+(mode==='f2s'?'秒':'帧')+'</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'niche/convert-sample.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">音频采样点数 ↔ 时长（秒），需采样率</p>\n'
    '<div class="input-row"><div><label>数值</label><input type="number" id="val" value="44100" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>采样率 (kHz)</label><input type="number" id="sr" value="44.1" step="0.1" oninput="calc()"></div></div>\n'
    '<div><label>方向</label><select id="mode" onchange="calc()"><option value="p2s" selected>采样点 → 秒</option><option value="s2p">秒 → 采样点</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var sr=+document.getElementById('sr').value||0;var mode=document.getElementById('mode').value;var out='';if(sr<=0){out='采样率需>0';}else{var r=(mode==='p2s')?v/(sr*1000):v*(sr*1000);out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r.toFixed(2)+' '+(mode==='p2s'?'秒':'点')+'</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'music/convert-speed.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">歌曲变速：新时长 = 原时长 × (原BPM / 新BPM)</p>\n'
    '<div class="input-row"><div><label>原时长 (秒)</label><input type="number" id="dur" value="180" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>原 BPM</label><input type="number" id="ob" value="120" oninput="calc()"></div></div>\n'
    '<div><label>新 BPM</label><input type="number" id="nb" value="140" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var dur=+document.getElementById('dur').value||0;var ob=+document.getElementById('ob').value||0;var nb=+document.getElementById('nb').value||0;var out='';if(dur<=0||ob<=0||nb<=0){out='请输入有效正数';}else{var r=dur*(ob/nb);out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r.toFixed(1)+' 秒</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">提速 '+((nb/ob-1)*100).toFixed(0)+'%</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'sports/convert-47.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">1RM 估算（Epley 公式：1RM = 重量 × (1 + 次数/30)）</p>\n'
    '<div class="input-row"><div><label>重量 (kg)</label><input type="number" id="w" value="100" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>完成次数</label><input type="number" id="r" value="5" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">估算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var w=+document.getElementById('w').value||0;var r=+document.getElementById('r').value||0;var out='';if(w<=0||r<=0){out='请输入有效正数';}else{var rm=w*(1+r/30);out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+rm.toFixed(1)+' kg</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">约 '+Math.round(rm*0.95)+'–'+Math.round(rm*1.0)+' kg（估算区间）</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'sports/convert-time.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">铁人三项总完赛时间 = 游泳 + 骑车 + 跑步</p>\n'
    '<div class="input-row"><div><label>游泳 (秒)</label><input type="number" id="s" value="1200" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>骑车 (秒)</label><input type="number" id="b" value="3600" oninput="calc()"></div></div>\n'
    '<div><label>跑步 (秒)</label><input type="number" id="r" value="2400" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">合计</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function fmt(t){var h=Math.floor(t/3600),m=Math.floor((t%3600)/60),s=Math.round(t%60);return (h>0?h+'时':'')+m+'分'+s+'秒';}function calc(){var s=+document.getElementById('s').value||0;var b=+document.getElementById('b').value||0;var r=+document.getElementById('r').value||0;var total=s+b+r;document.getElementById('res').innerHTML='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+fmt(total)+'</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">共 '+total+' 秒</p>';}calc();"),

  'food/convert-19.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">酒精度（体积%）≈ (初比重 − 终比重) / 0.00736（经验近似，20℃）</p>\n'
    '<div class="input-row"><div><label>初比重 (OG)</label><input type="number" id="og" value="1.050" step="0.001" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>终比重 (FG)</label><input type="number" id="fg" value="1.010" step="0.001" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var og=+document.getElementById('og').value||0;var fg=+document.getElementById('fg').value||0;var out='';if(og<=0||fg<=0){out='请输入有效比重';}else{var abv=(og-fg)/0.00736;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+abv.toFixed(2)+' % vol</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">经验近似，实际以检测为准</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'food/convert-concentration.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">白利度 (Brix) ↔ 比重 (Specific Gravity) 经验换算</p>\n'
    '<div class="input-row"><div><label>输入值</label><input type="number" id="val" value="20" step="0.1" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从</label><select id="from" onchange="calc()"><option value="brix" selected>Brix (°Bx)</option><option value="sg">比重 SG</option></select></div></div>\n'
    '<div><label>到</label><select id="to" onchange="calc()"><option value="sg" selected>比重 SG</option><option value="brix">Brix (°Bx)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var from=document.getElementById('from').value;var to=document.getElementById('to').value;var sg,brix,out='';if(from==='brix'){brix=v;sg=1+brix/(258.6-(brix/258.2)*227.1);}else{sg=v;brix=((182.4601*sg-775.6821)*sg+1262.7794)*sg-669.5622;}var r=(to==='brix')?brix:sg;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r.toFixed(3)+' '+(to==='brix'?'°Bx':'SG')+'</strong></p>';document.getElementById('res').innerHTML=out;}calc();"),

  'film/convert-time-1.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">SMPTE 时间码：总帧 = ((时×3600+分×60+秒)×fps) + 帧</p>\n'
    '<div class="input-row"><div><label>时 (0-23)</label><input type="number" id="h" value="0" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>分</label><input type="number" id="m" value="0" oninput="calc()"></div>\n'
    '<div><label>秒</label><input type="number" id="s" value="10" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>帧</label><input type="number" id="f" value="0" oninput="calc()"></div></div>\n'
    '<div><label>帧率 fps</label><input type="number" id="fps" value="25" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var h=+document.getElementById('h').value||0;var m=+document.getElementById('m').value||0;var s=+document.getElementById('s').value||0;var f=+document.getElementById('f').value||0;var fps=+document.getElementById('fps').value||0;var out='';if(fps<=0){out='帧率需>0';}else{var tf=((h*3600+m*60+s)*fps)+f;out='<p style=\"font-size:20px;color:var(--primary);\"><strong>'+tf+' 帧</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+(tf/fps).toFixed(3)+' 秒</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'transport/convert-fuel-oil.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">燃油效率：L/100km = 235.2146 / MPG(美制)</p>\n'
    '<div class="input-row"><div><label>输入值</label><input type="number" id="val" value="30" step="0.1" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从</label><select id="from" onchange="calc()"><option value="mpg" selected>MPG (mi/gal)</option><option value="l100">L/100km</option></select></div></div>\n'
    '<div><label>到</label><select id="to" onchange="calc()"><option value="l100" selected>L/100km</option><option value="mpg">MPG</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var from=document.getElementById('from').value;var to=document.getElementById('to').value;var out='';if(v<=0){out='请输入有效正数';}else{var r=235.2146/v;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r.toFixed(2)+' '+(to==='l100'?'L/100km':'MPG')+'</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'baking/convert-28.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">烘焙百分比：配料重量 = 面粉重量 × 百分比% ÷ 100（面粉=100%）</p>\n'
    '<div class="input-row"><div><label>面粉重量 (g)</label><input type="number" id="flour" value="500" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>配料百分比 (%)</label><input type="number" id="pct" value="60" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var flour=+document.getElementById('flour').value||0;var pct=+document.getElementById('pct').value||0;var out='';if(flour<=0||pct<0){out='请输入有效数值';}else{var w=flour*pct/100;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+w.toFixed(1)+' g</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">面粉 '+flour+'g 的 '+pct+'% = '+w.toFixed(1)+'g</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'leather/convert-area-weight.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">面积重量 = 重量 ÷ 面积（g/m²）</p>\n'
    '<div class="input-row"><div><label>重量 (g)</label><input type="number" id="w" value="100" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>面积 (m²)</label><input type="number" id="a" value="0.5" step="0.01" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var w=+document.getElementById('w').value||0;var a=+document.getElementById('a').value||0;var out='';if(w<=0||a<=0){out='请输入有效正数';}else{var aw=w/a;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+aw.toFixed(1)+' g/m²</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'environment/convert-air-aqi.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">PM2.5（24h, µg/m³）→ AQI（US EPA 分段线性）</p>\n'
    '<div class="input-row"><div><label>PM2.5 浓度</label><input type="number" id="c" value="35" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var c=+document.getElementById('c').value||0;var bp=[[0,12,0,50],[12.1,35.4,51,100],[35.5,55.4,101,150],[55.5,150.4,151,200],[150.5,250.4,201,300],[250.5,350.4,301,400],[350.5,500.4,401,500]];var aqi='超标(>500)';for(var i=0;i<bp.length;i++){if(c>=bp[i][0]&&c<=bp[i][1]){aqi=Math.round((bp[i][3]-bp[i][2])/(bp[i][1]-bp[i][0])*(c-bp[i][0])+bp[i][2]);break;}}document.getElementById('res').innerHTML='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+aqi+'</strong></p>';}calc();"),

  'electronics/convert-capacitance.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">电容 EIA 编码 → 容值（3位码：前2有效，第3为10的指数；R 表示小数点）</p>\n'
    '<div class="input-row"><div><label>电容编码（如 104 / 4R7）</label><input type="text" id="code" value="104" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">解析</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var code=(document.getElementById('code').value||'').trim().toUpperCase();var out='';if(!/^[0-9]{3}$/.test(code)&&!/^[0-9]R[0-9]$/.test(code)){out='格式应为 3 位数字（如 104）或 xRx（如 4R7）';}else{var pf;if(code.indexOf('R')>=0){pf=parseFloat(code.replace('R','.'))*1e6;}else{var sig=parseInt(code.slice(0,2),10);var exp=parseInt(code[2],10);pf=sig*Math.pow(10,exp);}var nf=pf/1000,uf=pf/1e6,f=pf/1e9;out='<p style=\"font-size:20px;color:var(--primary);\"><strong>'+pf+' pF</strong></p><p style=\"font-size:13px;color:var(--text-muted);\">'+nf.toFixed(3)+' nF ｜ '+uf.toFixed(6)+' µF ｜ '+f.toFixed(9)+' F</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'food/convert-ratio-seasoning.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">配料配比缩放：新量 = 基准量 × 缩放倍数</p>\n'
    '<div class="input-row"><div><label>基准量 (g)</label><input type="number" id="base" value="10" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>缩放倍数 (×)</label><input type="number" id="mult" value="3" step="0.5" oninput="calc()"></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var base=+document.getElementById('base').value||0;var mult=+document.getElementById('mult').value||0;var out='';if(base<=0||mult<=0){out='请输入有效正数';}else{var r=base*mult;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r.toFixed(1)+' g</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+base+'g × '+mult+' = '+r.toFixed(1)+'g</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'transport/convert-volume-weight.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">体积重量 = 长×宽×高 ÷ 除数（航空常用 6000，部分 5000，单位 cm/kg）</p>\n'
    '<div class="input-row"><div><label>长 (cm)</label><input type="number" id="l" value="40" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>宽 (cm)</label><input type="number" id="w" value="30" oninput="calc()"></div>\n'
    '<div><label>高 (cm)</label><input type="number" id="h" value="20" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>除数</label><select id="d" onchange="calc()"><option value="6000" selected>6000</option><option value="5000">5000</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var l=+document.getElementById('l').value||0;var w=+document.getElementById('w').value||0;var h=+document.getElementById('h').value||0;var d=+document.getElementById('d').value||0;var out='';if(l<=0||w<=0||h<=0||d<=0){out='请输入有效正数';}else{var vw=l*w*h/d;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+vw.toFixed(2)+' kg</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+l+'×'+w+'×'+h+' ÷ '+d+'</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'textile/convert-48.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">纱支换算：特克斯 tex = g/1000m；英支 Ne = 590.5/tex；公支 Nm = 1000/tex</p>\n'
    '<div class="input-row"><div><label>输入值</label><input type="number" id="val" value="20" step="0.1" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>输入类型</label><select id="from" onchange="calc()"><option value="tex" selected>特克斯 tex</option><option value="ne">英支 Ne</option><option value="nm">公支 Nm</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var from=document.getElementById('from').value;var out='';if(v<=0){out='请输入有效正数';}else{var tex;if(from==='tex'){tex=v;}else if(from==='ne'){tex=590.5/v;}else{tex=1000/v;}var ne=590.5/tex,nm=1000/tex;out='<p style=\"font-size:18px;color:var(--primary);\"><strong>tex '+tex.toFixed(2)+' ｜ Ne '+ne.toFixed(1)+' ｜ Nm '+nm.toFixed(1)+'</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  # ===== KEEP-2 table（真实对照表型，静态真实数据）=====
  'cardiology/convert-rehab.html': ('table', '常见活动代谢当量（METs）', '依据 ACSM 公开标准，1 MET ≈ 静息代谢率，用于运动强度估算',
    '<table style="width:100%;border-collapse:collapse;font-size:13px;"><tr style="border-bottom:1px solid var(--color-border);"><th style="text-align:left;padding:6px;">活动</th><th style="text-align:right;padding:6px;">METs</th></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">静坐</td><td style="text-align:right;padding:6px;">1.0</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">步行 (4.8 km/h)</td><td style="text-align:right;padding:6px;">3.5</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">瑜伽</td><td style="text-align:right;padding:6px;">2.5</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">骑车（休闲）</td><td style="text-align:right;padding:6px;">5.8</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">游泳（休闲）</td><td style="text-align:right;padding:6px;">6.0</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">慢跑 (8 km/h)</td><td style="text-align:right;padding:6px;">8.3</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">爬楼梯</td><td style="text-align:right;padding:6px;">8.8</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">跳绳</td><td style="text-align:right;padding:6px;">11.8</td></tr>'
    '<tr><td style="padding:6px;">篮球（比赛）</td><td style="text-align:right;padding:6px;">6.5</td></tr></table>'),

  'food/convert-20.html': ('table', '常见辣椒斯科维尔辣度（SHU）', '斯科维尔指数（Scoville Heat Units） approximate 公开参考值',
    '<table style="width:100%;border-collapse:collapse;font-size:13px;"><tr style="border-bottom:1px solid var(--color-border);"><th style="text-align:left;padding:6px;">辣椒</th><th style="text-align:right;padding:6px;">SHU</th></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">甜椒</td><td style="text-align:right;padding:6px;">0</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">香蕉辣椒</td><td style="text-align:right;padding:6px;">100–900</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">墨西哥椒 Jalapeño</td><td style="text-align:right;padding:6px;">2,500–8,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">塞拉诺</td><td style="text-align:right;padding:6px;">10,000–23,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">卡宴</td><td style="text-align:right;padding:6px;">30,000–50,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">泰椒</td><td style="text-align:right;padding:6px;">50,000–100,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">哈瓦那</td><td style="text-align:right;padding:6px;">100,000–350,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">鬼椒 Bhut Jolokia</td><td style="text-align:right;padding:6px;">855,000–1,041,427</td></tr>'
    '<tr><td style="padding:6px;">卡罗莱纳死神</td><td style="text-align:right;padding:6px;">1,500,000–2,200,000</td></tr></table>'),

  'tcm-chemistry/convert-41.html': ('table', '常见物质口服 LD50（大鼠，mg/kg）', '半数致死量公开参考近似值，仅作毒理学常识对照',
    '<table style="width:100%;border-collapse:collapse;font-size:13px;"><tr style="border-bottom:1px solid var(--color-border);"><th style="text-align:left;padding:6px;">物质</th><th style="text-align:right;padding:6px;">LD50 (mg/kg)</th></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">水</td><td style="text-align:right;padding:6px;">&gt;90,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">食盐 NaCl</td><td style="text-align:right;padding:6px;">3,000</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">蔗糖</td><td style="text-align:right;padding:6px;">29,700</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">乙醇</td><td style="text-align:right;padding:6px;">7,060</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">维生素 C</td><td style="text-align:right;padding:6px;">11,900</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">阿司匹林</td><td style="text-align:right;padding:6px;">200</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">咖啡因</td><td style="text-align:right;padding:6px;">192</td></tr>'
    '<tr><td style="padding:6px;">尼古丁</td><td style="text-align:right;padding:6px;">50</td></tr></table>'),

  'sports/convert-13.html': ('table', '攀岩难度等级对照（V 级 ↔ YDS）', '美国野外攀岩常用等级近似映射',
    '<table style="width:100%;border-collapse:collapse;font-size:13px;"><tr style="border-bottom:1px solid var(--color-border);"><th style="text-align:left;padding:6px;">V 级</th><th style="text-align:right;padding:6px;">YDS</th></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V0</td><td style="text-align:right;padding:6px;">5.10</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V1</td><td style="text-align:right;padding:6px;">5.11a</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V2</td><td style="text-align:right;padding:6px;">5.11c</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V3</td><td style="text-align:right;padding:6px;">5.11d</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V4</td><td style="text-align:right;padding:6px;">5.12a</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V5</td><td style="text-align:right;padding:6px;">5.12c</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V6</td><td style="text-align:right;padding:6px;">5.12d</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V7</td><td style="text-align:right;padding:6px;">5.13a</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V8</td><td style="text-align:right;padding:6px;">5.13b</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">V10</td><td style="text-align:right;padding:6px;">5.13d</td></tr>'
    '<tr><td style="padding:6px;">V16</td><td style="text-align:right;padding:6px;">5.15b</td></tr></table>'),

  'niche/convert-23.html': ('table', '宠物年龄经验对照（等效人年）', '狗/猫年龄→人年常用经验估算（非精确生物学）',
    '<table style="width:100%;border-collapse:collapse;font-size:13px;"><tr style="border-bottom:1px solid var(--color-border);"><th style="text-align:left;padding:6px;">宠物年龄</th><th style="text-align:right;padding:6px;">狗 (人年)</th><th style="text-align:right;padding:6px;">猫 (人年)</th></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">1 岁</td><td style="text-align:right;padding:6px;">15</td><td style="text-align:right;padding:6px;">15</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">2 岁</td><td style="text-align:right;padding:6px;">24</td><td style="text-align:right;padding:6px;">24</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">3 岁</td><td style="text-align:right;padding:6px;">28</td><td style="text-align:right;padding:6px;">28</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">5 岁</td><td style="text-align:right;padding:6px;">36</td><td style="text-align:right;padding:6px;">36</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">7 岁</td><td style="text-align:right;padding:6px;">44</td><td style="text-align:right;padding:6px;">44</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">10 岁</td><td style="text-align:right;padding:6px;">56</td><td style="text-align:right;padding:6px;">56</td></tr>'
    '<tr><td style="padding:6px;">15 岁</td><td style="text-align:right;padding:6px;">76</td><td style="text-align:right;padding:6px;">76</td></tr></table>'),

  'archive/convert-ref-cite.html': ('table', 'GB/T 7714 参考文献著录格式', '常见文献类型的规范著录模板（顺序编码制）',
    '<table style="width:100%;border-collapse:collapse;font-size:13px;"><tr style="border-bottom:1px solid var(--color-border);"><th style="text-align:left;padding:6px;">类型</th><th style="text-align:left;padding:6px;">格式模板</th></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">期刊 [J]</td><td style="padding:6px;">[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 起止页.</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">图书 [M]</td><td style="padding:6px;">[序号] 作者. 书名[M]. 版次. 出版地: 出版者, 出版年: 引文页.</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">会议 [C]</td><td style="padding:6px;">[序号] 作者. 题名[C]. 出版地: 出版者, 出版年: 起止页.</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">学位论文 [D]</td><td style="padding:6px;">[序号] 作者. 题名[D]. 保存地: 保存单位, 年份.</td></tr>'
    '<tr style="border-bottom:1px solid var(--color-border);"><td style="padding:6px;">专利 [P]</td><td style="padding:6px;">[序号] 发明人. 专利名[P]. 专利国别, 专利号. 公告日期.</td></tr>'
    '<tr><td style="padding:6px;">标准 [S]</td><td style="padding:6px;">[序号] 标准编号, 标准名称[S].</td></tr></table>'),

  # ===== KEEP-2b 真实实现（最终剩余 4 个，确定正确）=====
  'road/convert-angle-slope.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">坡度 百分比 ↔ 角度（tan 关系）</p>\n'
    '<div class="input-row"><div><label>输入值</label><input type="number" id="val" value="10" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从</label><select id="from" onchange="calc()"><option value="pct" selected>百分比 (%)</option><option value="deg">角度 (°)</option></select></div>\n'
    '<div><label>到</label><select id="to" onchange="calc()"><option value="pct">百分比 (%)</option><option value="deg" selected>角度 (°)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function calc(){var v=+document.getElementById('val').value||0;var from=document.getElementById('from').value;var to=document.getElementById('to').value;var out='';if(v<0){out='坡度应非负';}else{var pct,deg;if(from==='pct'){pct=v;deg=Math.atan(v/100)*180/Math.PI;}else{deg=v;pct=Math.tan(v*Math.PI/180)*100;}var res=(to==='pct')?pct:deg;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+res.toFixed(2)+' '+(to==='pct'?'%':'°')+'</strong></p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'science/convert-power.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">力 / 能量 / 功率 三类物理量，须选同量纲单位互转</p>\n'
    '<div class="input-row"><div><label>数值</label><input type="number" id="val" value="1" step="0.01" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>从</label><select id="from" onchange="calc()">'
    '<option value="N">牛顿 N（力）</option><option value="kgf">千克力 kgf（力）</option><option value="lbf">磅力 lbf（力）</option><option value="dyn">达因 dyn（力）</option>'
    '<option value="J">焦耳 J（能）</option><option value="cal">卡路里 cal（能）</option><option value="kWh">千瓦时 kWh（能）</option><option value="eV">电子伏 eV（能）</option><option value="BTU">英热单位 BTU（能）</option><option value="erg">尔格 erg（能）</option>'
    '<option value="W">瓦 W（功率）</option><option value="kW">千瓦 kW（功率）</option><option value="hp">马力 hp（功率）</option><option value="PS">公制马力 PS（功率）</option></select></div>\n'
    '<div><label>到</label><select id="to" onchange="calc()">'
    '<option value="N">牛顿 N（力）</option><option value="kgf">千克力 kgf（力）</option><option value="lbf">磅力 lbf（力）</option><option value="dyn">达因 dyn（力）</option>'
    '<option value="J">焦耳 J（能）</option><option value="cal">卡路里 cal（能）</option><option value="kWh">千瓦时 kWh（能）</option><option value="eV">电子伏 eV（能）</option><option value="BTU">英热单位 BTU（能）</option><option value="erg">尔格 erg（能）</option>'
    '<option value="W">瓦 W（功率）</option><option value="kW">千瓦 kW（功率）</option><option value="hp">马力 hp（功率）</option><option value="PS" selected>公制马力 PS（功率）</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "var F={N:1,kgf:9.80665,lbf:4.44822,dyn:1e-5};var E={J:1,cal:4.184,kWh:3.6e6,eV:1.602e-19,BTU:1055.06,erg:1e-7};var P={W:1,kW:1000,hp:745.7,PS:735.5};function grp(u){if(u in F)return F;if(u in E)return E;if(u in P)return P;return null;}function fmt(n){if(n===0)return '0';var a=Math.abs(n);if(a>=1e6||a<1e-3)return n.toExponential(4);return (Math.round(n*1e6)/1e6).toString();}function calc(){var v=+document.getElementById('val').value;var f=document.getElementById('from').value;var t=document.getElementById('to').value;var gf=grp(f),gt=grp(t);var out='';if(isNaN(v)){out='请输入有效数字';}else if(!gf||!gt){out='请选择有效单位';}else if(gf!==gt){out='请选择同量纲单位（力 / 能 / 功率）';}else{var base=v*gf[f];var r=base/gt[t];out='<p style=\"font-size:20px;color:var(--primary);\"><strong>'+fmt(r)+'</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+v+' '+f+' = '+fmt(r)+' '+t+'</p>';}document.getElementById('res').innerHTML=out;}calc();"),

  'edu/convert-1.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">世界主要时区换算（标准时间，不含夏令时）</p>\n'
    '<div class="input-row"><div><label>源时间 (HH:MM)</label><input type="text" id="val" value="12:00" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>源时区</label><select id="from" onchange="calc()">'
    '<option value="-8">洛杉矶 PST (UTC-8)</option><option value="-7">丹佛 MST (UTC-7)</option><option value="-6">芝加哥 CST (UTC-6)</option><option value="-5">纽约 EST (UTC-5)</option><option value="0" selected>伦敦 UTC+0</option><option value="1">柏林/巴黎 CET (UTC+1)</option><option value="2">雅典 EET (UTC+2)</option><option value="3">莫斯科 (UTC+3)</option><option value="5">卡拉奇 (UTC+5)</option><option value="5.5">印度 IST (UTC+5.5)</option><option value="7">曼谷 (UTC+7)</option><option value="8">北京/上海/香港/新加坡 CST (UTC+8)</option><option value="9">东京/首尔 (UTC+9)</option><option value="10">悉尼 AEST (UTC+10)</option></select></div>\n'
    '<div><label>目标时区</label><select id="to" onchange="calc()">'
    '<option value="-8">洛杉矶 PST (UTC-8)</option><option value="-7">丹佛 MST (UTC-7)</option><option value="-6">芝加哥 CST (UTC-6)</option><option value="-5">纽约 EST (UTC-5)</option><option value="0">伦敦 UTC+0</option><option value="1" selected>柏林/巴黎 CET (UTC+1)</option><option value="2">雅典 EET (UTC+2)</option><option value="3">莫斯科 (UTC+3)</option><option value="5">卡拉奇 (UTC+5)</option><option value="5.5">印度 IST (UTC+5.5)</option><option value="7">曼谷 (UTC+7)</option><option value="8">北京/上海/香港/新加坡 CST (UTC+8)</option><option value="9">东京/首尔 (UTC+9)</option><option value="10">悉尼 AEST (UTC+10)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function ptime(s){var m=(s||'').match(/(\\d{1,2}):(\\d{2})/);return m?(+m[1]*60+(+m[2])):NaN;}function pad(n){return (n<10?'0':'')+n;}function calc(){var tm=ptime(document.getElementById('val').value);var f=+document.getElementById('from').value;var t=+document.getElementById('to').value;var out='';if(isNaN(tm)){out='请输入 HH:MM 格式';}else{var r=tm - f*60 + t*60;var dd=Math.floor(r/1440);var rm=((r%1440)+1440)%1440;var hh=Math.floor(rm/60),mm=rm%60;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+pad(hh)+':'+pad(mm)+'</strong></p>'+(dd>0?'<p style=\"font-size:12px;color:var(--text-muted);\">次日（+'+dd+'天）</p>':dd<0?'<p style=\"font-size:12px;color:var(--text-muted);\">前一日（'+dd+'天）</p>':'<p style=\"font-size:12px;color:var(--text-muted);\">同日</p>');}document.getElementById('res').innerHTML=out;}calc();"),

  'astronomy/convert-17.html': ('algo', None, None,
    '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">全球时区换算（标准时间，不含夏令时）</p>\n'
    '<div class="input-row"><div><label>源时间 (HH:MM)</label><input type="text" id="val" value="12:00" oninput="calc()"></div></div>\n'
    '<div class="input-row"><div><label>源时区</label><select id="from" onchange="calc()">'
    '<option value="-9">安克雷奇 (UTC-9)</option><option value="-8">洛杉矶 PST (UTC-8)</option><option value="-7">丹佛 MST (UTC-7)</option><option value="-6">芝加哥 CST (UTC-6)</option><option value="-5">纽约 EST (UTC-5)</option><option value="-3">巴西利亚 (UTC-3)</option><option value="0" selected>伦敦 UTC+0</option><option value="1">柏林/巴黎 CET (UTC+1)</option><option value="2">雅典 EET (UTC+2)</option><option value="3">莫斯科 (UTC+3)</option><option value="4">迪拜 (UTC+4)</option><option value="5">卡拉奇 (UTC+5)</option><option value="5.5">印度 IST (UTC+5.5)</option><option value="6">达卡 (UTC+6)</option><option value="7">曼谷 (UTC+7)</option><option value="8">北京/上海/香港/新加坡 CST (UTC+8)</option><option value="9">东京/首尔 (UTC+9)</option><option value="10">悉尼 AEST (UTC+10)</option><option value="11">所罗门 (UTC+11)</option><option value="12">奥克兰 (UTC+12)</option></select></div>\n'
    '<div><label>目标时区</label><select id="to" onchange="calc()">'
    '<option value="-9">安克雷奇 (UTC-9)</option><option value="-8">洛杉矶 PST (UTC-8)</option><option value="-7">丹佛 MST (UTC-7)</option><option value="-6">芝加哥 CST (UTC-6)</option><option value="-5">纽约 EST (UTC-5)</option><option value="-3">巴西利亚 (UTC-3)</option><option value="0">伦敦 UTC+0</option><option value="1" selected>柏林/巴黎 CET (UTC+1)</option><option value="2">雅典 EET (UTC+2)</option><option value="3">莫斯科 (UTC+3)</option><option value="4">迪拜 (UTC+4)</option><option value="5">卡拉奇 (UTC+5)</option><option value="5.5">印度 IST (UTC+5.5)</option><option value="6">达卡 (UTC+6)</option><option value="7">曼谷 (UTC+7)</option><option value="8">北京/上海/香港/新加坡 CST (UTC+8)</option><option value="9">东京/首尔 (UTC+9)</option><option value="10">悉尼 AEST (UTC+10)</option><option value="11">所罗门 (UTC+11)</option><option value="12">奥克兰 (UTC+12)</option></select></div></div>\n'
    '<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">转换</button></div>\n'
    '<div class="result-box" id="res"></div></div>',
    "function ptime(s){var m=(s||'').match(/(\\d{1,2}):(\\d{2})/);return m?(+m[1]*60+(+m[2])):NaN;}function pad(n){return (n<10?'0':'')+n;}function calc(){var tm=ptime(document.getElementById('val').value);var f=+document.getElementById('from').value;var t=+document.getElementById('to').value;var out='';if(isNaN(tm)){out='请输入 HH:MM 格式';}else{var r=tm - f*60 + t*60;var dd=Math.floor(r/1440);var rm=((r%1440)+1440)%1440;var hh=Math.floor(rm/60),mm=rm%60;out='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+pad(hh)+':'+pad(mm)+'</strong></p>'+(dd>0?'<p style=\"font-size:12px;color:var(--text-muted);\">次日（+'+dd+'天）</p>':dd<0?'<p style=\"font-size:12px;color:var(--text-muted);\">前一日（'+dd+'天）</p>':'<p style=\"font-size:12px;color:var(--text-muted);\">同日</p>');}document.getElementById('res').innerHTML=out;}calc();"),
}

SENTINEL = '<!-- TOOLBOX-REALIZED -->'

def realize_factor(path, units, sub):
    s = open(path, encoding='utf-8').read()
    if SENTINEL in s:
        return False
    # 删除 rate 输入行
    s = re.sub(r'<div><label>换算系数</label>.*?id="rate".*?</div>', '', s, flags=re.S)
    # 替换 from/to options
    opts = ''.join('<option value="%s">%s</option>' % (f, l) for l, f in units)
    s = re.sub(r'(<select id="from"[^>]*>).*?(</select>)', lambda m: m.group(1)+opts+m.group(2), s, flags=re.S)
    s = re.sub(r'(<select id="to"[^>]*>).*?(</select>)', lambda m: m.group(1)+opts+m.group(2), s, flags=re.S)
    # 副标题
    s = re.sub(r'<p style="font-size:13px[^"]*"[^>]*>.*?</p>', '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">%s</p>' % sub, s, count=1)
    # calc 逻辑
    new_calc = ("function calc(){var v=+document.getElementById(\"val\").value||0;var f=+document.getElementById(\"from\").value;var t=+document.getElementById(\"to\").value;var r=v*f/t;var fl=document.getElementById(\"from\").selectedOptions[0].text;var tl=document.getElementById(\"to\").selectedOptions[0].text;r=Number(r.toPrecision(12));document.getElementById(\"res\").innerHTML='<p style=\"font-size:22px;color:var(--primary);\"><strong>'+r+'</strong></p><p style=\"font-size:12px;color:var(--text-muted);\">'+v+' '+fl+' = '+r+' '+tl+'</p>';}calc();function copyRes(){ToolBox.copyText(document.getElementById(\"res\").innerText);}" + SENTINEL + "\n")
    s = re.sub(r'<script>\s*function calc.*?</script>', lambda m: '<script>\n' + new_calc + '\n</script>', s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    return True

def realize_algo(path, inner, script):
    s = open(path, encoding='utf-8').read()
    if SENTINEL in s:
        return False
    # 替换 h2 之后到 tool-notes 之前的输入区
    s = re.sub(r'(<h2>.*?</h2>).*?(<div class="tool-notes")', lambda m: m.group(1) + '\n' + inner + '\n' + m.group(2), s, flags=re.S)
    # 替换 calc script
    new_script = '<script>\n' + script + '\n' + SENTINEL + '\n</script>'
    s = re.sub(r'<script>\s*function calc.*?</script>', lambda m: new_script, s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    return True

def realize_table(path, title, intro, table_html):
    s = open(path, encoding='utf-8').read()
    if SENTINEL in s:
        return False
    fb = ('<div class="formula-box" style="margin-top:14px;">'
          '<div class="formula-title">数据说明</div>'
          '<div class="formula-desc">本表为公开标准对照值，纯前端静态展示，仅供速查参考，不构成专业建议。</div></div>')
    block = ('\n<div class="card" style="margin:16px 0;">'
             '<h3 style="margin-bottom:10px;">%s</h3>'
             '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">%s</p>'
             '%s%s</div>\n' % (title, intro, table_html, fb))
    s = re.sub(r'(<h2>.*?</h2>).*?(<div class="tool-notes")',
               lambda m: m.group(1) + block + m.group(2), s, flags=re.S)
    s = re.sub(r'<script>\s*function calc.*?</script>',
               '<script>\n/* 对照表型工具：静态真实数据展示 */\n' + SENTINEL + '\n</script>', s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    return True

def main():
    dry = '--dry-run' in sys.argv
    only = None
    limit = None
    for a in sys.argv[1:]:
        if a == '--dry-run':
            continue
        elif a == '--only':
            idx = sys.argv.index(a)
            only = sys.argv[idx+1] if idx+1 < len(sys.argv) else None
        elif a == '--limit':
            idx = sys.argv.index(a)
            limit = int(sys.argv[idx+1]) if idx+1 < len(sys.argv) else None
    items = [(k, v) for k, v in SPEC.items() if (only is None or k == only)]
    done = 0
    for rel, spec in items:
        if limit is not None and done >= limit:
            break
        path = os.path.join(ROOT, 'tools', rel)
        if not os.path.exists(path):
            print('SKIP 不存在:', rel)
            continue
        mode = spec[0]
        if dry:
            print('[DRY]', rel, '->', mode)
            continue
        if mode == 'factor':
            ok = realize_factor(path, spec[1], spec[2])
        elif mode == 'algo':
            ok = realize_algo(path, spec[3], spec[4])
        else:
            ok = realize_table(path, spec[1], spec[2], spec[3])
        print(('OK   ' if ok else 'SKIP ') + rel + ' (' + mode + ')')
        if ok:
            done += 1
    print('处理完成。' if not dry else 'Dry-run 完成。')

if __name__ == '__main__':
    main()
