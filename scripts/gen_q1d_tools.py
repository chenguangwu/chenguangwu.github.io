#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 批次 04 生成器：6 个工具。
 - xml-to-yaml / yaml-to-xml / xml-to-toml / toml-to-xml（XML↔JSON↔YAML/TOML，纯前端）
 - random-string（随机字符串生成器，可选字符集）
 - whitespace（文本空白清理：去空行/首尾空白/合并空格）
复用 gen_q1_tools 的 TEMPLATE/render，gen_q1c_tools 的 YAML_JS/TOML_JS 解析与序列化。
用法：python3 scripts/gen_q1d_tools.py
"""
import os, json
from gen_q1_tools import TEMPLATE, IND_ZH, BASE, render_inputs, render_reset, render
from gen_q1c_tools import YAML_JS, TOML_JS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")

XML_JS = r"""
function escXml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function escAttr(s){return escXml(s).replace(/"/g,'&quot;');}
function xmlToJson(xml){
  xml=xml.replace(/<!--[\s\S]*?-->/g,'').replace(/<\?[\s\S]*?\?>/g,'').replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g,function(m,c){return c;});
  var pos=0;
  function skipws(){ while(pos<xml.length && /\s/.test(xml[pos])) pos++; }
  function parseEl(){
    var gt=xml.indexOf('>',pos); if(gt<0) return null;
    var head=xml.slice(pos+1,gt); pos=gt+1;
    var selfClose=false;
    if(head.slice(-1)==='/'){ selfClose=true; head=head.slice(0,-1); }
    var sp=head.search(/\s/);
    var name= sp<0? head : head.slice(0,sp);
    var attrStr= sp<0? '' : head.slice(sp+1);
    var attrs={};
    var re=/([\w:-]+)\s*=\s*"([^"]*)"/g, m;
    while((m=re.exec(attrStr))){ attrs[m[1]]=m[2]; }
    if(selfClose) return {name:name, val:nodeVal(name,attrs,null,'')};
    var children=[]; var text='';
    while(pos<xml.length){
      if(xml[pos]==='<'){
        if(xml.substr(pos,2)==='</'){ var cgt=xml.indexOf('>',pos); pos=cgt+1; break; }
        var ch=parseEl(); if(ch) children.push(ch);
      } else {
        var nxt=xml.indexOf('<',pos); if(nxt<0) nxt=xml.length;
        var tx=xml.slice(pos,nxt); pos=nxt;
        if(tx.trim()!=='') text+=tx;
      }
    }
    return {name:name, val:nodeVal(name,attrs,children,text)};
  }
  function nodeVal(name,attrs,children,text){
    if(children && children.length){
      var obj={};
      for(var a in attrs){ if(attrs.hasOwnProperty(a)) obj['@'+a]=attrs[a]; }
      var groups={};
      for(var k=0;k<children.length;k++){ var c=children[k]; (groups[c.name]=groups[c.name]||[]).push(c.val); }
      for(var g in groups){ obj[g]= groups[g].length===1? groups[g][0] : groups[g]; }
      if(text && text.trim()) obj['#text']=text.trim();
      return obj;
    }
    var v=text?text.trim():'';
    if(Object.keys(attrs).length){ var o={}; for(var a2 in attrs)o['@'+a2]=attrs[a2]; if(v)o['#text']=v; return o; }
    return v;
  }
  skipws();
  if(xml[pos]!=='<') return {__err:'输入不是合法的 XML（未找到根元素）'};
  var root=parseEl();
  if(!root) return {__err:'XML 解析失败'};
  var out={}; out[root.name]=root.val;
  return out;
}
function jsonToXml(obj){
  function ser(name,val){
    if(val && typeof val==='object' && !Array.isArray(val)){
      var attrs=''; var inner='';
      for(var k in val){
        if(k[0]==='@') attrs+=' '+k.slice(1)+'="'+escAttr(val[k])+'"';
        else if(k==='#text') inner+=val[k];
        else { var v=val[k]; if(Array.isArray(v)){ for(var i=0;i<v.length;i++) inner+=ser(k,v[i]); } else inner+=ser(k,v); }
      }
      return '<'+name+attrs+'>'+inner+'</'+name+'>';
    }
    if(Array.isArray(val)){ return val.map(function(x){return ser(name,x);}).join(''); }
    return '<'+name+'>'+escXml(val===null?'':val)+'</'+name+'>';
  }
  var keys=Object.keys(obj);
  if(keys.length!==1) return '<root>'+keys.map(function(k){return ser(k,obj[k]);}).join('')+'</root>';
  return ser(keys[0], obj[keys[0]]);
}
"""

def indent_of(sel):
    return "'\\t'" if sel == "tab" else "parseInt(%s,10)" % sel

TOOLS = [
{
 "slug":"xml-to-yaml","industry":"it","cat":"dev","icon":"🧩","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"XML 转 YAML 转换器",
 "h1":"XML 转 YAML 转换器",
 "h2":"🧩 XML 转 YAML 转换器",
 "desc":"XML 转 YAML 转换器 - 粘贴 XML，转换为 YAML（属性写作 @attr，文本写作 #text）。纯前端本地解析。",
 "intro":"在配置迁移、接口联调时常需要把 XML 转成更易读的 YAML。粘贴 XML，立即得到结构等价的 YAML。",
 "inputs":[
   {"id":"source","label":"XML 源文本","type":"textarea","rows":"8","value":"<note>\n  <to>Tony</to>\n  <from>Anna</from>\n  <heading>Reminder</heading>\n  <body>Don't forget me!</body>\n  <items id=\"1\">\n    <item>Apple</item>\n    <item>Banana</item>\n  </items>\n</note>"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": XML_JS + YAML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 XML 文本</p>'; return; }
var obj=xmlToJson(src);
if(obj && obj.__err){ document.getElementById('result').innerHTML='<p class="muted">解析失败：'+escH(obj.__err)+'</p>'; return; }
var pad = document.getElementById('indent').value==='tab' ? '\t' : (' ').repeat(parseInt(document.getElementById('indent').value||'2',10));
var sort=document.getElementById('top_1').checked;
var yaml=dumpYaml(obj,pad,sort);
document.getElementById('result').innerHTML='<div class="result-title">YAML 输出</div><pre class="code-block">'+escH(yaml)+'</pre>';
""",
 "notes":[
   "XML 属性在 YAML 中表示为以 @ 开头的键（如 @id），元素文本表示为 #text。",
   "重复的同名子元素会转为 YAML 列表；多个同级元素按顺序保留。",
   "命名空间、CDATA、注释等会被忽略或归一化；极复杂 XML 建议人工核对。"
 ],
 "ref":""
},
{
 "slug":"yaml-to-xml","industry":"it","cat":"dev","icon":"🧩","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"YAML 转 XML 转换器",
 "h1":"YAML 转 XML 转换器",
 "h2":"🧩 YAML 转 XML 转换器",
 "desc":"YAML 转 XML 转换器 - 粘贴 YAML，转换为 XML（@attr 写作属性，#text 写作元素文本）。纯前端本地解析。",
 "intro":"把 YAML 配置转回 XML，常用于老系统、SOAP 接口或某些构建工具。粘贴 YAML，立即得到 XML。",
 "inputs":[
   {"id":"source","label":"YAML 源文本","type":"textarea","rows":"8","value":"note:\n  to: Tony\n  from: Anna\n  heading: Reminder\n  body: Don't forget me!\n  items:\n    - Apple\n    - Banana"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": YAML_JS + XML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 YAML 文本</p>'; return; }
var obj=parseYaml(src);
if(obj && obj.__err){ document.getElementById('result').innerHTML='<p class="muted">解析失败：'+escH(obj.__err)+'</p>'; return; }
var xml=jsonToXml(obj);
document.getElementById('result').innerHTML='<div class="result-title">XML 输出</div><pre class="code-block">'+escH(xml)+'</pre>';
""",
 "notes":[
   "YAML 中以 @ 开头的键会转为 XML 属性（如 @id → id=\"...\"），#text 键转为元素文本。",
   "列表会展开为多个同名元素；标量直接作为元素文本。",
   "转换按约定进行，复杂结构建议人工核对属性/元素的选择。"
 ],
 "ref":""
},
{
 "slug":"xml-to-toml","industry":"it","cat":"dev","icon":"🧩","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"XML 转 TOML 转换器",
 "h1":"XML 转 TOML 转换器",
 "h2":"🧩 XML 转 TOML 转换器",
 "desc":"XML 转 TOML 转换器 - 粘贴 XML，转换为 TOML（属性写作 @attr，文本写作 #text）。纯前端本地解析。",
 "intro":"在 Rust/Go 配置、pyproject 等 TOML 场景，常需要把 XML 数据转成 TOML。粘贴 XML，立即得到 TOML。",
 "inputs":[
   {"id":"source","label":"XML 源文本","type":"textarea","rows":"8","value":"<config>\n  <name>demo</name>\n  <port>8080</port>\n  <db url=\"x\" pool=\"16\"/>\n</config>"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": XML_JS + TOML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 XML 文本</p>'; return; }
var obj=xmlToJson(src);
if(obj && obj.__err){ document.getElementById('result').innerHTML='<p class="muted">解析失败：'+escH(obj.__err)+'</p>'; return; }
var sort=document.getElementById('top_1').checked;
var toml=dumpToml(obj,sort);
document.getElementById('result').innerHTML='<div class="result-title">TOML 输出</div><pre class="code-block">'+escH(toml)+'</pre>';
""",
 "notes":[
   "XML 属性转为 TOML 中以 @ 开头的键；重复同名子元素转为 TOML 数组。",
   "TOML 不支持 XML 的属性和混合内容的全部语义，转换按约定归一化。",
   "极复杂 XML 建议人工核对。"
 ],
 "ref":""
},
{
 "slug":"toml-to-xml","industry":"it","cat":"dev","icon":"🧩","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"TOML 转 XML 转换器",
 "h1":"TOML 转 XML 转换器",
 "h2":"🧩 TOML 转 XML 转换器",
 "desc":"TOML 转 XML 转换器 - 粘贴 TOML，转换为 XML（@attr 写作属性，#text 写作元素文本）。纯前端本地解析。",
 "intro":"把 TOML 配置转回 XML，用于老系统或需要 XML 的接口。粘贴 TOML，立即得到 XML。",
 "inputs":[
   {"id":"source","label":"TOML 源文本","type":"textarea","rows":"8","value":"[config]\nname = \"demo\"\nport = 8080\n\n[config.db]\nurl = \"x\"\npool = 16"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": TOML_JS + XML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 TOML 文本</p>'; return; }
var obj=parseToml(src);
if(obj && obj.__err){ document.getElementById('result').innerHTML='<p class="muted">解析失败：'+escH(obj.__err)+'</p>'; return; }
var xml=jsonToXml(obj);
document.getElementById('result').innerHTML='<div class="result-title">XML 输出</div><pre class="code-block">'+escH(xml)+'</pre>';
""",
 "notes":[
   "TOML 中以 @ 开头的键会转为 XML 属性；数组展开为多个同名元素。",
   "转换按约定进行，复杂结构建议人工核对。"
 ],
 "ref":""
},
{
 "slug":"random-string","industry":"it","cat":"dev","icon":"🎲","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"随机字符串生成器",
 "h1":"随机字符串生成器",
 "h2":"🎲 随机字符串生成器",
 "desc":"随机字符串生成器 - 设置长度与字符集（大写/小写/数字/符号），批量生成随机字符串，可一键复制。纯前端本地生成。",
 "intro":"做临时令牌、测试数据、盐值、密码片段时常需要随机字符串。设置长度与字符集，立即生成，可去重与复制。",
 "inputs":[
   {"id":"len","label":"长度","value":"16","step":"1","min":"1","max":"128"},
   {"id":"cnt","label":"数量","value":"5","step":"1","min":"1","max":"50"},
   {"id":"upper","label":"包含大写字母 A-Z","type":"checkbox","opts":[["upper","是"]]},
   {"id":"lower","label":"包含小写字母 a-z","type":"checkbox","opts":[["lower","是"]]},
   {"id":"digit","label":"包含数字 0-9","type":"checkbox","opts":[["digit","是"]]},
   {"id":"sym","label":"包含符号 !@#$%","type":"checkbox","opts":[["sym","是"]]}
 ],
 "calc":"""
var len=parseInt(document.getElementById('len').value||'16',10)||16; if(len>128)len=128; if(len<1)len=1;
var cnt=parseInt(document.getElementById('cnt').value||'5',10)||5; if(cnt>50)cnt=50; if(cnt<1)cnt=1;
var set='';
if(document.getElementById('top_upper').checked) set+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
if(document.getElementById('top_lower').checked) set+='abcdefghijklmnopqrstuvwxyz';
if(document.getElementById('top_digit').checked) set+='0123456789';
if(document.getElementById('top_sym').checked) set+='!@#$%^&*()-_=+[]{};:,.<>?';
if(!set){ document.getElementById('result').innerHTML='<p class="muted">请至少选择一种字符集</p>'; return; }
var out=[];
for(var n=0;n<cnt;n++){
  var s='';
  var buf=new Uint32Array(len);
  if(window.crypto&&window.crypto.getRandomValues){ window.crypto.getRandomValues(buf); } else { for(var b=0;b<len;b++) buf[b]=Math.floor(Math.random()*4294967296); }
  for(var i=0;i<len;i++){ s+=set[buf[i]%set.length]; }
  out.push(s);
}
var html='<div class="result-title">生成 '+cnt+' 个随机字符串（点击复制）</div>';
html+='<div class="code-list">';
for(var k=0;k<out.length;k++){ html+='<div class="code-row"><code>'+escH(out[k])+'</code><button class="copy-btn" onclick="copyText(this)">复制</button></div>'; }
html+='</div>';
// 强度评估：熵 = len * log2(charsetSize)
var ent=Math.round(len*Math.log(set.length)/Math.log(2));
var strength, sc;
if(ent<40){ strength='弱'; sc='#dc2626'; }
else if(ent<60){ strength='中'; sc='#d97706'; }
else if(ent<120){ strength='强'; sc='#16a34a'; }
else { strength='极强'; sc='#15803d'; }
html+='<div class="result-title">强度评估</div>';
html+='<table class="ref-table"><tr><th>字符集大小</th><td>'+set.length+'</td></tr>'
    +'<tr><th>单串长度</th><td>'+len+'</td></tr>'
    +'<tr><th>理论熵值</th><td>'+ent+' bits</td></tr>'
    +'<tr><th>强度评级</th><td style="color:'+sc+';font-weight:600;">'+strength+'</td></tr></table>';
html+='<p class="muted">熵值按 log2(字符集大小)×长度 估算，仅衡量可猜测空间，不代表抗破解能力。</p>';
document.getElementById('result').innerHTML=html;
function copyText(btn){ var code=btn.parentNode.querySelector('code'); var t=code?code.textContent:''; var ta=document.createElement('textarea'); ta.value=t; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(ta); }
""",
 "notes":[
   "使用浏览器 crypto.getRandomValues 生成密码学安全的随机值；不支持时回退到 Math.random。",
   "长度上限 128、数量上限 50，避免一次性生成过多造成卡顿。",
   "符号集含常见安全符号；如需自定义可手动编辑结果。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 用法建议</h3>
  <table class="ref-table">
    <tr><th>用途</th><th>建议</th></tr>
    <tr><td>临时令牌</td><td>16–32 位，含大小写+数字+符号</td></tr>
    <tr><td>测试数据</td><td>8–16 位即可</td></tr>
    <tr><td>盐值(salt)</td><td>≥16 位随机</td></tr>
  </table>
</div>
"""
},
{
 "slug":"whitespace","industry":"it","cat":"dev","icon":"🧹","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"文本空白清理工具",
 "h1":"文本空白清理工具",
 "h2":"🧹 文本空白清理工具",
 "desc":"文本空白清理工具 - 去除首尾空白、删除空行、合并连续空格、可选末尾换行，一键整理杂乱文本。纯前端本地处理。",
 "intro":"从网页、PDF、表格复制来的文本常常带着多余空行和首尾空格。粘贴进来，勾选需要的清理项，立即得到整洁文本。",
 "inputs":[
   {"id":"source","label":"待清理文本","type":"textarea","rows":"8","value":"  第一行   \n\n  第二行   有多余   空格\n\n\n  第三行\n"},
   {"id":"trim","label":"去除每行首尾空白","type":"checkbox","opts":[["trim","是"]]},
   {"id":"blank","label":"删除空行","type":"checkbox","opts":[["blank","是"]]},
   {"id":"collapse","label":"合并连续空格为单个","type":"checkbox","opts":[["collapse","是"]]},
   {"id":"trail","label":"确保末尾单个换行","type":"checkbox","opts":[["trail","是"]]}
 ],
 "calc":"""
var text=document.getElementById('source').value||'';
var rawLines=text.split(/\\n|\\r\\n|\\r/);
var rawChars=text.length;
var blankBefore=rawLines.filter(function(l){return l.trim()==='';}).length;
var lines=rawLines;
if(document.getElementById('top_trim').checked) lines=lines.map(function(l){return l.replace(/^\\s+|\\s+$/g,'');});
if(document.getElementById('top_blank').checked) lines=lines.filter(function(l){return l.trim()!=='';});
if(document.getElementById('top_collapse').checked) lines=lines.map(function(l){return l.replace(/[ \\t]+/g,' ');});
var out=lines.join('\\n');
if(document.getElementById('top_trail').checked){ out=out.replace(/\\n+$/,'')+'\\n'; }
var blankAfter=lines.filter(function(l){return l.trim()==='';}).length;
// 空白字符明细
var tabCount=(text.match(/\\t/g)||[]).length;
var spaceCount=(text.match(/ /g)||[]).length;
var crlfCount=(text.match(/\\r\\n/g)||[]).length;
var crCount=(text.match(/\\r(?!\\n)/g)||[]).length;
var lfAlone=(text.match(/(?<!\\r)\\n/g)||[]).length;
document.getElementById('result').innerHTML='<div class="result-title">清理结果（'+lines.length+' 行）</div><pre class="code-block">'+escH(out)+'</pre>'
  +'<div class="result-title">处理统计</div>'
  +'<table class="ref-table"><tr><th>原始行数</th><td>'+rawLines.length+'</td></tr>'
  +'<tr><th>处理后行数</th><td>'+lines.length+'</td></tr>'
  +'<tr><th>删除空行</th><td>'+(blankBefore-blankAfter)+'</td></tr>'
  +'<tr><th>原始字符数</th><td>'+rawChars+'</td></tr>'
  +'<tr><th>处理后字符数</th><td>'+out.length+'</td></tr></table>'
  +'<div class="result-title">空白字符明细</div>'
  +'<table class="ref-table"><tr><th>空格 (space)</th><td>'+spaceCount+'</td></tr>'
  +'<tr><th>制表符 (tab)</th><td>'+tabCount+'</td></tr>'
  +'<tr><th>Windows 换行 (CRLF)</th><td>'+crlfCount+'</td></tr>'
  +'<tr><th>旧 Mac 换行 (CR)</th><td>'+crCount+'</td></tr>'
  +'<tr><th>Unix 换行 (LF)</th><td>'+lfAlone+'</td></tr></table>';
// 逐行对照预览（前 5 行）
var prevN=Math.min(5, Math.max(rawLines.length, lines.length));
var preview='<div class="result-title">逐行对照预览（前 '+prevN+' 行）</div><table class="ref-table">'
  +'<tr><th>行</th><th>原始</th><th>处理后</th></tr>';
for(var pi=0; pi<prevN; pi++){
  var rv=pi<rawLines.length?rawLines[pi]:'';
  var cv=pi<lines.length?lines[pi]:'';
  preview+='<tr><td>'+(pi+1)+'</td><td><code>'+escH(rv)+'</code></td><td><code>'+escH(cv)+'</code></td></tr>';
}
preview+='</table>';
document.getElementById('result').innerHTML+=preview;
""",
 "notes":[
   "清理为纯本地操作，文本不会上传；适合处理从网页/PDF/Excel 复制的乱序文本。",
   "各选项可单独勾选；默认全部开启即可应付大多数场景。",
   "合并空格仅针对空格与制表符，不影响换行。"
 ],
 "ref":""
},
]

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
