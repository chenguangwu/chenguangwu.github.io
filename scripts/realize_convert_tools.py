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
        else:
            ok = realize_algo(path, spec[3], spec[4])
        print(('OK   ' if ok else 'SKIP ') + rel + ' (' + mode + ')')
        if ok:
            done += 1
    print('处理完成。' if not dry else 'Dry-run 完成。')

if __name__ == '__main__':
    main()
