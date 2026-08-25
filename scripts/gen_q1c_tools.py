#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 批次 03 生成器：6 个 it-tools 风格工具。
 - yaml-to-toml / toml-to-yaml / yaml-to-json / toml-to-json（纯前端解析+序列化，无外部依赖）
 - emoji-picker（可搜索 Emoji 选择器，点击复制）
 - latex（LaTeX 常用符号/命令速查表，可搜索）
复用 gen_q1_tools 的 TEMPLATE / render / render_inputs / render_reset。
用法：python3 scripts/gen_q1c_tools.py
"""
import os, json
from gen_q1_tools import TEMPLATE, IND_ZH, BASE, render_inputs, render_reset, render

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")

# ---- 共享 JS：YAML / TOML 解析与序列化（每个页面内联，纯前端无 CDN）----
YAML_JS = r"""
function yScalar(s){
  s=s.trim();
  if(s==='')return '';
  if((s[0]==='"'&&s.slice(-1)==='"')||(s[0]==="'"&&s.slice(-1)==="'")) return s.slice(1,-1);
  if(s==='true')return true; if(s==='false')return false;
  if(s==='null'||s==='~')return null;
  if(/^-?\d+$/.test(s))return parseInt(s,10);
  if(/^-?\d+\.\d+$/.test(s))return parseFloat(s);
  return s;
}
function yIsMapEntry(s){ var kv=s.match(/^([^:]+):\s?(.*)$/); return kv && /^[\u4e00-\u9fa5A-Za-z0-9_\-\s]/.test(kv[1]) && s.indexOf(':')>0; }
function parseYaml(text){
  var lines=text.replace(/\r/g,'').split('\n');
  var items=[];
  for(var i=0;i<lines.length;i++){ var raw=lines[i]; var s=raw.trim(); if(!s||s[0]==='#') continue; items.push({ind:raw.length-raw.trimStart().length, content:s}); }
  if(!items.length) return {};
  var p={i:0};
  return yBlock(items, items[0].ind, p);
}
function yBlock(items, indent, p){
  if(p.i>=items.length) return {};
  if(items[p.i].content[0]==='-'){
    var arr=[];
    while(p.i<items.length && items[p.i].ind===indent && items[p.i].content[0]==='-'){
      var item=items[p.i].content.slice(1).trim(); p.i++;
      if(item===''){ arr.push(yBlock(items, items[p.i].ind, p)); }
      else if(yIsMapEntry(item)){ arr.push(yMapFrom(items, indent+2, p, item)); }
      else { arr.push(yScalar(item)); }
    }
    return arr;
  }
  var obj={};
  while(p.i<items.length && items[p.i].ind===indent){
    var line=items[p.i].content;
    var kv=line.match(/^([^:]+):\s?(.*)$/);
    if(!kv){ p.i++; continue; }
    var key=kv[1].trim(); var val=kv[2].trim(); p.i++;
    if(val===''){ if(p.i<items.length && items[p.i].ind>indent) obj[key]=yBlock(items, items[p.i].ind, p); else obj[key]={}; }
    else obj[key]=yScalar(val);
  }
  return obj;
}
function yMapFrom(items, mapIndent, p, firstItem){
  var m={};
  var kv=firstItem.match(/^([^:]+):\s?(.*)$/);
  var key=kv[1].trim(); var val=kv[2].trim();
  if(val===''){ if(p.i<items.length && items[p.i].ind>mapIndent) m[key]=yBlock(items, items[p.i].ind, p); else m[key]={}; }
  else m[key]=yScalar(val);
  while(p.i<items.length && items[p.i].ind===mapIndent && items[p.i].content[0]!=='-'){
    var line=items[p.i].content; var kv2=line.match(/^([^:]+):\s?(.*)$/);
    if(!kv2) break;
    var k2=kv2[1].trim(); var v2=kv2[2].trim(); p.i++;
    if(v2===''){ if(p.i<items.length && items[p.i].ind>mapIndent) m[k2]=yBlock(items, items[p.i].ind, p); else m[k2]={}; }
    else m[k2]=yScalar(v2);
  }
  return m;
}
function yNeedQ(v){ return /[:#\-\[\]\{\},]/.test(v)||v.trim()!==v||v===''||/^\d/.test(v)||v==='true'||v==='false'||v==='null'; }
function yVal(v){
  if(v===null||v===undefined) return 'null';
  if(typeof v==='boolean') return v?'true':'false';
  if(typeof v==='number') return String(v);
  if(typeof v==='string'){ return yNeedQ(v)? ('"'+v.replace(/"/g,'\\"')+'"') : v; }
  return String(v);
}
function dumpYaml(node,pad,sort,isRoot){
  if(isRoot===undefined)isRoot=true;
  var out='';
  if(node instanceof Array){
    for(var i=0;i<node.length;i++){
      var it=node[i];
      if(it!==null && typeof it==='object' && !(it instanceof Array)){
        var ks=Object.keys(it); if(sort)ks=ks.slice().sort();
        for(var j=0;j<ks.length;j++){ var kk=ks[j]; out+=(j===0?pad+'- ':pad+'  ')+kk+': '+yVal(it[kk])+'\n'; }
      } else out+=pad+'- '+yVal(it)+'\n';
    }
    return out;
  }
  var keys=Object.keys(node); if(sort)keys=keys.slice().sort();
  for(var i=0;i<keys.length;i++){
    var k=keys[i]; var v=node[k];
    var p=isRoot?'':pad;
    if(v instanceof Array) out+=p+k+':\n'+dumpYaml(v,pad+'  ',sort,false);
    else if(v!==null && typeof v==='object') out+=p+k+':\n'+dumpYaml(v,pad+'  ',sort,false);
    else out+=p+k+': '+yVal(v)+'\n';
  }
  return out;
}
"""

TOML_JS = r"""
function tLit(v){
  if(v===null||v===undefined) return '""';
  if(typeof v==='boolean') return v?'true':'false';
  if(typeof v==='number') return String(v);
  if(v instanceof Array) return '['+v.map(tLit).join(', ')+']';
  return '"'+String(v).replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'"';
}
function tVal(s){
  s=s.trim();
  if(s[0]==='"'){ var m=s.match(/^"((?:[^"\\]|\\.)*)"/); return m? m[1].replace(/\\n/g,'\n').replace(/\\t/g,'\t').replace(/\\"/g,'"') : s; }
  if(s==='true')return true; if(s==='false')return false;
  if(s==='')return '';
  if(/^-?\d+$/.test(s))return parseInt(s,10);
  if(/^-?\d+\.\d+$/.test(s))return parseFloat(s);
  if(s[0]==='['){ var inner=s.slice(1,s.lastIndexOf(']')); if(inner.trim()==='')return []; return inner.split(',').map(function(x){return tVal(x);}); }
  return s;
}
function stripComment(s){
  var out=''; var q=false;
  for(var i=0;i<s.length;i++){ var c=s[i]; if(c==='"'&&s[i-1]!=='\\'){q=!q;} if(c==='#'&&!q) break; out+=c; }
  return out.trim();
}
function parseToml(text){
  var lines=text.replace(/\r/g,'').split('\n');
  var root={}; var cur=root;
  for(var i=0;i<lines.length;i++){
    var s=lines[i].trim();
    if(!s||s[0]==='#') continue;
    if(s[0]==='['){
      var close=s.indexOf(']'); if(close<0) continue;
      var header=s.slice(1,close);
      if(header[0]==='['){
        var name=header.slice(1).trim(); var parts=name.split('.');
        var obj=root; for(var p=0;p<parts.length-1;p++){ obj=obj[parts[p]]=obj[parts[p]]||{}; }
        var arr=obj[parts[parts.length-1]]=obj[parts[parts.length-1]]||[];
        var elem={}; arr.push(elem); cur=elem;
      } else {
        var parts2=header.split('.'); var obj2=root;
        for(var q=0;q<parts2.length;q++){ obj2=obj2[parts2[q]]=obj2[parts2[q]]||{}; }
        cur=obj2;
      }
      continue;
    }
    var eq=s.indexOf('='); if(eq<0) continue;
    var key=s.slice(0,eq).trim(); var val=stripComment(s.slice(eq+1));
    if(key[0]==='"'){ var km=key.match(/^"((?:[^"\\]|\\.)*)"$/); if(km) key=km[1].replace(/\\"/g,'"'); }
    var ps=key.split('.'); var o=cur;
    for(var j=0;j<ps.length-1;j++){ o=o[ps[j]]=o[ps[j]]||{}; }
    o[ps[ps.length-1]]=tVal(val);
  }
  return root;
}
function tKey(k){ return /^[A-Za-z0-9_-]+$/.test(k) ? k : '"'+String(k).replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'"'; }
function dumpTable(t,sort,prefix){
  prefix=prefix||'';
  var out=''; var keys=Object.keys(t); if(sort)keys=keys.slice().sort();
  for(var i=0;i<keys.length;i++){ var k=keys[i]; var v=t[k];
    if(!(v!==null && typeof v==='object')) out+=tKey(k)+' = '+tLit(v)+'\n'; }
  for(var i=0;i<keys.length;i++){ var k=keys[i]; var v=t[k];
    if(v instanceof Array){
      if(v.length && typeof v[0]==='object' && v[0]!==null){
        for(var a=0;a<v.length;a++){ out+='\n[['+tKey(k)+']]\n'+dumpTable(v[a],sort); }
      } else { out+=tKey(k)+' = '+tLit(v)+'\n'; }
    } else if(v!==null && typeof v==='object'){
      out+='\n['+(prefix?prefix+'.':'')+tKey(k)+']\n'+dumpTable(v,sort,prefix?(prefix+'.'+k):k);
    }
  }
  return out;
}
function dumpToml(node,sort){ return dumpTable(node,sort,''); }
"""

def indent_of(sel):
    if sel == "tab": return "'\\t'"
    return sel  # "2" / "4"

# ---- 工具定义 ----
TOOLS = [
{
 "slug":"yaml-to-toml","industry":"it","cat":"dev","icon":"🔧","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"YAML 转 TOML 转换器",
 "h1":"YAML 转 TOML 转换器",
 "h2":"🔧 YAML 转 TOML 转换器",
 "desc":"YAML 转 TOML 转换器 - 粘贴 YAML 文本，一键转换为 TOML，支持嵌套映射、列表与常用标量。纯前端本地处理。",
 "intro":"在 Rust/Go 项目配置、pyproject、Cargo.toml 等场景常需要在 YAML 与 TOML 之间迁移。粘贴 YAML，立即得到结构等价的 TOML。",
 "inputs":[
   {"id":"source","label":"YAML 源文本","type":"textarea","rows":"8","value":"server:\n  host: 0.0.0.0\n  port: 8080\n  debug: true\nfeatures:\n  - logging\n  - metrics\ndb:\n  url: postgres://localhost:5432\n  pool: 16"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": YAML_JS + TOML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 YAML 文本</p>'; return; }
var obj=parseYaml(src);
if(obj && obj.__err){ document.getElementById('result').innerHTML='<p class="muted">解析失败：'+escH(obj.__err)+'</p>'; return; }
var pad = 'indent'==='tab' ? '\t' : (' ').repeat(parseInt(document.getElementById('indent').value||'2',10));
var sort=document.getElementById('top_1').checked;
var toml=dumpToml(obj,sort);
var html='<div class="result-title">TOML 输出</div><pre class="code-block">'+escH(toml)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "转换按结构等价进行：YAML 映射→TOML 表，YAML 列表→TOML 数组；嵌套映射会展开为 [section] 小节。",
   "TOML 不支持 YAML 的锚点/合并（&anchor、*alias）与多行折叠，这类高级语法会被忽略或报错。",
   "字符串中含特殊字符（冒号、#、方括号等）会自动加引号以保证 TOML 合法。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 YAML ↔ TOML 对照</h3>
  <table class="ref-table">
    <tr><th>YAML</th><th>TOML</th></tr>
    <tr><td>key: value</td><td>key = "value"</td></tr>
    <tr><td>list:\\n  - a\\n  - b</td><td>list = ["a", "b"]</td></tr>
    <tr><td>[a, b, c]</td><td>arr = ["a", "b", "c"]</td></tr>
    <tr><td>parent:\\n  child: 1</td><td>[parent]\\nchild = 1</td></tr>
  </table>
  <p>本工具支持常见子集（映射、列表、标量、注释、嵌套小节）；极复杂 YAML 建议先用 JSON 中转。</p>
</div>
"""
},
{
 "slug":"toml-to-yaml","industry":"it","cat":"dev","icon":"🔧","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"TOML 转 YAML 转换器",
 "h1":"TOML 转 YAML 转换器",
 "h2":"🔧 TOML 转 YAML 转换器",
 "desc":"TOML 转 YAML 转换器 - 粘贴 TOML 文本，一键转换为 YAML，支持 [section]、[[数组表]] 与常用标量。纯前端本地处理。",
 "intro":"从 Cargo.toml / pyproject 等迁移到 Kubernetes、GitHub Actions 等 YAML 配置时，用本工具把 TOML 结构转成 YAML。",
 "inputs":[
   {"id":"source","label":"TOML 源文本","type":"textarea","rows":"8","value":"title = \"demo\"\nversion = \"1.0.0\"\n\n[server]\nhost = \"0.0.0.0\"\nport = 8080\n\n[database]\nurl = \"postgres://localhost\"\npool = 16\n\n[[database.replicas]]\nname = \"r1\"\nweight = 1"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": TOML_JS + YAML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 TOML 文本</p>'; return; }
var obj=parseToml(src);
var pad = document.getElementById('indent').value==='tab' ? '\t' : (' ').repeat(parseInt(document.getElementById('indent').value||'2',10));
var sort=document.getElementById('top_1').checked;
var yaml=dumpYaml(obj,pad,sort);
var html='<div class="result-title">YAML 输出</div><pre class="code-block">'+escH(yaml)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "TOML 的 [section] 表转为 YAML 嵌套映射；[[数组表]] 转为 YAML 列表，每个元素是一个映射。",
   "TOML 的数组（[1,2,3]）转为 YAML 行内或块列表。",
   "时间戳等 TOML 专有类型会按字符串保留，避免信息丢失。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 TOML → YAML 要点</h3>
  <table class="ref-table">
    <tr><th>TOML</th><th>YAML</th></tr>
    <tr><td>key = "v"</td><td>key: v</td></tr>
    <tr><td>[sec]</td><td>sec:</td></tr>
    <tr><td>[[arr]]</td><td>arr:\\n  - ...</td></tr>
    <tr><td>list = [1,2]</td><td>list:\\n  - 1\\n  - 2</td></tr>
  </table>
</div>
"""
},
{
 "slug":"yaml-to-json","industry":"it","cat":"dev","icon":"🔧","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"YAML 转 JSON 转换器",
 "h1":"YAML 转 JSON 转换器",
 "h2":"🔧 YAML 转 JSON 转换器",
 "desc":"YAML 转 JSON 转换器 - 粘贴 YAML 文本，一键转换为格式化 JSON，支持嵌套映射与列表。纯前端本地处理。",
 "intro":"在 CI、API、前端配置里常需要把 YAML（如 GitHub Actions、docker-compose）转成 JSON。粘贴即转，可设缩进。",
 "inputs":[
   {"id":"source","label":"YAML 源文本","type":"textarea","rows":"8","value":"name: ToolBox\nversion: 2.1\nactive: true\nitems:\n  - id: 1\n    name: alpha\n  - id: 2\n    name: beta"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": YAML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 YAML 文本</p>'; return; }
var obj=parseYaml(src);
if(obj && obj.__err){ document.getElementById('result').innerHTML='<p class="muted">解析失败：'+escH(obj.__err)+'</p>'; return; }
if(document.getElementById('sort').checked){
  obj=sortKeys(obj);
}
var n=parseInt(document.getElementById('indent').value||'2',10);
var json=JSON.stringify(obj, null, document.getElementById('indent').value==='tab'?'\\t':n);
var html='<div class="result-title">JSON 输出</div><pre class="code-block">'+escH(json)+'</pre>';
document.getElementById('result').innerHTML=html;
function sortKeys(o){ if(!(o!==null&&typeof o==='object'))return o; if(o instanceof Array)return o.map(sortKeys); var r={};Object.keys(o).sort().forEach(function(k){r[k]=sortKeys(o[k]);}); return r; }
""",
 "notes":[
   "转换结果可直接粘贴进 JSON 配置、REST 请求体或代码。",
   "支持常见 YAML 子集：映射、列表、标量（字符串/数字/布尔/null）；不支持锚点、多文档等高级特性。",
   "缩进可选 2/4 空格或 Tab，便于对接不同代码风格。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 常用 YAML 片段</h3>
  <table class="ref-table">
    <tr><th>写法</th><th>含义</th></tr>
    <tr><td>key: value</td><td>映射键值</td></tr>
    <tr><td>- item</td><td>列表元素</td></tr>
    <tr><td>key: [a, b]</td><td>行内列表</td></tr>
    <tr><td># 注释</td><td>注释行</td></tr>
  </table>
</div>
"""
},
{
 "slug":"toml-to-json","industry":"it","cat":"dev","icon":"🔧","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"TOML 转 JSON 转换器",
 "h1":"TOML 转 JSON 转换器",
 "h2":"🔧 TOML 转 JSON 转换器",
 "desc":"TOML 转 JSON 转换器 - 粘贴 TOML 文本，一键转换为格式化 JSON，支持 [section] 与 [[数组表]]。纯前端本地处理。",
 "intro":"把 Cargo.toml、pyproject.toml 等配置转成 JSON，方便在脚本、API、前端里消费。粘贴即转，可设缩进。",
 "inputs":[
   {"id":"source","label":"TOML 源文本","type":"textarea","rows":"8","value":"name = \"ToolBox\"\nversion = \"2.1\"\n\n[server]\nhost = \"0.0.0.0\"\nport = 8080\n\n[database]\nurl = \"postgres://x\"\npool = 16"},
   {"id":"indent","label":"缩进","type":"select","opts":[["2","2 空格"],["4","4 空格"],["tab","Tab"]]},
   {"id":"sort","label":"按键名排序输出","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc": TOML_JS + r"""
var src=document.getElementById('source').value||'';
if(!src.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 TOML 文本</p>'; return; }
var obj=parseToml(src);
if(document.getElementById('sort').checked){ obj=sortKeys(obj); }
var n=parseInt(document.getElementById('indent').value||'2',10);
var json=JSON.stringify(obj, null, document.getElementById('indent').value==='tab'?'\\t':n);
var html='<div class="result-title">JSON 输出</div><pre class="code-block">'+escH(json)+'</pre>';
document.getElementById('result').innerHTML=html;
function sortKeys(o){ if(!(o!==null&&typeof o==='object'))return o; if(o instanceof Array)return o.map(sortKeys); var r={};Object.keys(o).sort().forEach(function(k){r[k]=sortKeys(o[k]);}); return r; }
""",
 "notes":[
   "TOML [section] 转为嵌套 JSON 对象；[[数组表]] 转为 JSON 数组。",
   "字符串、整数、浮点、布尔、数组、内联表都会被正确解析。",
   "结果缩进可选 2/4 空格或 Tab。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📋 TOML 基础</h3>
  <table class="ref-table">
    <tr><th>写法</th><th>含义</th></tr>
    <tr><td>key = "v"</td><td>字符串</td></tr>
    <tr><td>[section]</td><td>表</td></tr>
    <tr><td>[[arr]]</td><td>数组表</td></tr>
    <tr><td>list = [1, 2]</td><td>数组</td></tr>
  </table>
</div>
"""
},
]

# ---- Emoji 数据集（char, 名称, 关键词）----
EMOJI_DATA = [
 ["😀","grinning","笑 开心 微笑"],["😂","joy","大笑 笑哭 开心"],["🥰","smiling hearts","爱心 喜欢 爱"],
 ["😎","sunglasses","酷 墨镜 帅"],["🤔","thinking","思考 想 疑问"],["😴","sleeping","睡 困 累"],
 ["😭","sob","哭 难过 伤心"],["😡","rage","生气 怒 愤怒"],["🥳","partying","庆祝 派对 生日"],
 ["🤯","mind blown","震惊 爆炸 惊"],["😇","angel","天使 善良 圣洁"],["🤒","sick","病 发烧 不舒服"],
 ["👍","thumbs up","赞 好 同意 顶"],["👎","thumbs down","踩 差 不同意"],["👏","clap","鼓掌 赞 好"],
 ["🙏","pray","拜托 谢谢 祈祷 合十"],["💪","muscle","加油 力量 强"],["🤝","handshake","合作 握手 成交"],
 ["🔥","fire","火 热 赞 火爆"],["⭐","star","星 收藏 推荐"],["✨","sparkles","闪 亮 新"],
 ["💡","idea","想法 灯泡 创意"],["✅","check","对 完成 通过 勾"],["❌","cross","错 失败 叉"],
 ["⚠️","warning","警告 注意 小心"],["❓","question","问 疑问 问题"],["❗","exclamation","感叹 重要"],
 ["💯","hundred","满分 100 完美"],["🎉","tada","庆祝 彩带 恭喜"],["🎁","gift","礼物 礼 奖励"],
 ["❤️","red heart","爱 红心 喜欢"],["🧡","orange heart","橙心 友情"],["💛","yellow heart","黄心 快乐"],
 ["💚","green heart","绿心 自然"],["💙","blue heart","蓝心 宁静"],["💜","purple heart","紫心 浪漫"],
 ["🖤","black heart","黑心 酷"],["💔","broken heart","心碎 失恋"],["💕","two hearts","双心 爱意"],
 ["🌟","glowing star","亮星 闪耀"],["🌈","rainbow","彩虹 多元 美好"],["☀️","sun","太阳 晴 白天"],
 ["🌙","moon","月亮 夜 晚"],["⛅","cloud sun","多云 阴 天气"],["🌧️","rain","雨 下雨 天气"],
 ["❄️","snow","雪 冬天 冷"],["⚡","zap","闪电 快 电"],["🌊","wave","海浪 水 波浪"],
 ["🌸","cherry blossom","樱花 花 春天"],["🌹","rose","玫瑰 花 爱情"],["🌻","sunflower","向日葵 花 阳光"],
 ["🍀","clover","幸运草 运气 四叶草"],["🌿","leaf","叶 草 绿"],["🍎","apple","苹果 水果 健康"],
 ["🍊","orange","橘子 橙子 水果"],["🍋","lemon","柠檬 酸 水果"],["🍉","watermelon","西瓜 水果 夏"],
 ["🍓","strawberry","草莓 水果 甜"],["🍒","cherries","樱桃 水果"],["🍑","peach","桃子 水果 可爱"],
 ["🥑","avocado","牛油果 健康 轻食"],["🍔","burger","汉堡 快餐 吃"],["🍕","pizza","披萨 吃 美食"],
 ["🌮","taco","塔可 墨西哥 美食"],["🍜","ramen","拉面 面 美食"],["🍚","rice","米饭 饭 主食"],
 ["☕","coffee","咖啡 喝 提神"],["🍵","tea","茶 喝"],["🍺","beer","啤酒 喝 庆祝"],
 ["🍷","wine","红酒 酒 浪漫"],["🥤","soda","饮料 汽水"],["🍰","cake","蛋糕 甜点 生日"],
 ["🍪","cookie","饼干 甜点"],["🍩","donut","甜甜圈 甜"],["🍫","chocolate","巧克力 甜 爱"],
 ["⚽","soccer","足球 运动"],["🏀","basketball","篮球 运动"],["🏈","football","橄榄球 运动"],
 ["⚾","baseball","棒球 运动"],["🎾","tennis","网球 运动"],["🏐","volleyball","排球 运动"],
 ["🏓","ping pong","乒乓 运动"],["🎱","8 ball","台球 桌球"],["🏸","badminton","羽毛球 运动"],
 ["🥅","goal","球门 进球"],["🎯","target","目标 靶 准"],["🎮","game","游戏 玩 手柄"],
 ["🎲","dice","骰子 随机 游戏"],["🎰","slot","老虎机 赌 运气"],["🎸","guitar","吉他 音乐 弹"],
 ["🎹","piano","钢琴 音乐 键"],["🎤","mic","麦克 唱歌 音乐"],["🎧","headphones","耳机 听 音乐"],
 ["🎵","note","音符 音乐 歌"],["🎶","notes","音符 旋律 音乐"],["📱","phone","手机 电话 通讯"],
 ["💻","laptop","电脑 笔记本 工作"],["🖥️","desktop","台式机 电脑"],["⌨️","keyboard","键盘 打字"],
 ["🖱️","mouse","鼠标 点击"],["💾","floppy","保存 软盘 存储"],["💡","bulb","灯泡 想法"],
 ["🔋","battery","电池 电量"],["🔌","plug","插头 充电 电"],["📡","satellite","信号 卫星 网络"],
 ["📷","camera","相机 拍照 摄影"],["📹","video","摄像机 录像"],["🎥","movie","电影 拍摄 摄像机"],
 ["📺","tv","电视 看"],["⏰","alarm","闹钟 时间 提醒"],["⏱️","stopwatch","秒表 计时"],
 ["📅","calendar","日历 日期 安排"],["📆","tearing calendar","月历 日期"],["🗓️","spiral calendar","日程 计划"],
 ["💰","money bag","钱 财富 赚"],["💵","dollar","美元 钱 现金"],["💴","yen","日元 钱"],
 ["💶","euro","欧元 钱"],["💷","pound","英镑 钱"],["🪙","coin","硬币 钱 币"],
 ["🏆","trophy","奖杯 胜利 冠军"],["🥇","gold medal","金牌 第一 冠军"],["🥈","silver medal","银牌 第二"],
 ["🥉","bronze medal","铜牌 第三"],["🎖️","military","勋章 荣誉"],["🌍","globe","地球 世界 全球"],
 ["🌎","americas","地球 美洲 世界"],["🌏","asia","地球 亚洲 世界"],["🗺️","map","地图 导航 旅行"],
 ["🚀","rocket","火箭 发射 快 启动"],["✈️","airplane","飞机 飞 旅行"],["🚗","car","车 汽车 开车"],
 ["🚕","taxi","出租车 打车"],["🚌","bus","公交 大巴 车"],["🚄","bullettrain","高铁 火车 快"],
 ["🚲","bike","自行车 骑行"],["🛵","scooter","滑板车 摩托"],["⛵","sailboat","帆船 船 航海"],
 ["🏠","house","家 房子 住宅"],["🏢","office","办公室 写字楼 工作"],["🏥","hospital","医院 医疗 健康"],
 ["🏫","school","学校 教育"],["🏬","department","百货 商场"],["🏪","convenience","便利店 超市"],
 ["👶","baby","婴儿 宝宝"],["👦","boy","男孩 孩子"],["👧","girl","女孩 孩子"],
 ["👨","man","男人 男士"],["👩","woman","女人 女士"],["👴","old man","老爷爷 老"],
 ["👵","old woman","老奶奶 老"],["🐶","dog","狗 宠物 汪"],["🐱","cat","猫 宠物 喵"],
 ["🐭","mouse","老鼠 宠物"],["🐰","rabbit","兔子 宠物"],["🐻","bear","熊 动物"],
 ["🐼","panda","熊猫 国宝 可爱"],["🐨","koala","考拉 动物"],["🦁","lion","狮子 动物 王"],
 ["🐯","tiger","老虎 动物"],["🦊","fox","狐狸 动物"],["🐸","frog","青蛙 动物"],
 ["🐵","monkey","猴子 动物"],["🐧","penguin","企鹅 动物"],["🦄","unicorn","独角兽 梦幻 神奇"],
 ["🐝","bee","蜜蜂 昆虫"],["🦋","butterfly","蝴蝶 昆虫 美丽"],["🐢","turtle","乌龟 慢 动物"],
 ["🐍","snake","蛇 动物"],["🐠","tropical","热带鱼 鱼 海洋"],["🐬","dolphin","海豚 海洋 聪明"],
 ["✊","fist","拳 加油 握拳"],["✋","raised hand","手 停 手掌"],["👌","ok","OK 好 没问题 圈"],
 ["🤞","fingers crossed","好运 祈祷 交叉"],["👋","wave","你好 再见 招手"],["🤙","call me","打电话 手势 鱼"],
 ["🔍","search","搜索 放大镜 查"],["🔎","search","搜索 查找 放大镜"],["❤️‍🔥","heart fire","热爱 火 热血"],
 ["💥","boom","爆炸 冲击 炸"],["💢","anger","生气 怒 青筋"],["💬","speech","对话 气泡 说话"],
 ["👀","eyes","看 眼睛 注视"],["🧠","brain","脑 聪明 思考"],["💭","thought","想法 思考 云"],
 ["🔒","lock","锁 安全 私密"],["🔑","key","钥匙 关键 解锁"],["🛡️","shield","盾 保护 安全"],
 ["✈️","plane","飞机"],["📌","pin","图钉 定位 标记"],["📍","round pin","定位 位置 地点"],
 ["🔔","bell","铃 通知 提醒"],["📣","megaphone","喇叭 宣传 喊"],["💬","comment","评论 留言"],
]

# ---- LaTeX 数据集（命令, 示例, 说明）----
LATEX_DATA = [
 ["\\alpha","α","小写希腊字母 alpha"],["\\beta","β","小写希腊字母 beta"],["\\gamma","γ","小写希腊字母 gamma"],
 ["\\delta","δ","小写希腊字母 delta"],["\\epsilon","ε","小写希腊字母 epsilon"],["\\theta","θ","小写希腊字母 theta"],
 ["\\lambda","λ","小写希腊字母 lambda"],["\\mu","μ","小写希腊字母 mu"],["\\pi","π","圆周率 pi"],
 ["\\sigma","σ","小写希腊字母 sigma"],["\\phi","φ","小写希腊字母 phi"],["\\omega","ω","小写希腊字母 omega"],
 ["\\Gamma","Γ","大写希腊字母 Gamma"],["\\Delta","Δ","大写希腊字母 Delta"],["\\Theta","Θ","大写希腊字母 Theta"],
 ["\\Lambda","Λ","大写希腊字母 Lambda"],["\\Sigma","Σ","大写希腊字母 Sigma"],["\\Phi","Φ","大写希腊字母 Phi"],
 ["\\Omega","Ω","大写希腊字母 Omega"],["\\times","×","乘号"],["\\div","÷","除号"],
 ["\\pm","±","正负号"],["\\leq","≤","小于等于"],["\\geq","≥","大于等于"],
 ["\\neq","≠","不等于"],["\\approx","≈","约等于"],["\\equiv","≡","恒等于"],
 ["\\infty","∞","无穷"],["\\partial","∂","偏导"],["\\nabla","∇","梯度算符"],
 ["\\sum","∑","求和"],["\\prod","∏","求积"],["\\int","∫","积分"],
 ["\\oint","∮","环路积分"],["\\sqrt{x}","√x","平方根"],["\\frac{a}{b}","a/b","分式"],
 ["\\binom{n}{k}","C(n,k)","二项式系数"],["\\vec{v}","v⃗","向量"],["\\hat{x}","x̂","帽子（单位向量）"],
 ["\\bar{x}","x̄","均值（上划线）"],["\\dot{x}","ẋ","对时间导数"],["\\ddot{x}","ẍ","对时间二阶导"],
 ["\\lim","lim","极限"],["\\log","log","对数"],["\\ln","ln","自然对数"],
 ["\\exp","exp","指数"],["\\sin","sin","正弦"],["\\cos","cos","余弦"],
 ["\\tan","tan","正切"],["\\arcsin","arcsin","反正弦"],["\\arctan","arctan","反正切"],
 ["\\det","det","行列式"],["\\matrix","矩阵","无括号矩阵"],["\\begin{pmatrix}","( )","带圆括号矩阵"],
 ["\\begin{bmatrix}","[ ]","带方括号矩阵"],["\\begin{cases}","{ }","分段函数"],["\\mathbb{R}","ℝ","实数集"],
 ["\\mathbb{N}","ℕ","自然数集"],["\\mathbb{Z}","ℤ","整数集"],["\\mathbb{C}","ℂ","复数集"],
 ["\\mathcal{L}","L","花体 L（拉普拉斯/损失）"],["\\forall","∀","任意"],["\\exists","∃","存在"],
 ["\\in","∈","属于"],["\\notin","∉","不属于"],["\\subset","⊂","子集"],
 ["\\subseteq","⊆","包含于"],["\\cup","∪","并集"],["\\cap","∩","交集"],
 ["\\emptyset","∅","空集"],["\\to","→","趋于/映射到"],["\\mapsto","↦","映射为"],
 ["\\Rightarrow","⇒","推出"],["\\Leftarrow","⇐","由…推出"],["\\Leftrightarrow","⇔","等价"],
 ["\\wedge","∧","逻辑与"],["\\vee","∨","逻辑或"],["\\neg","¬","逻辑非"],
 ["\\oplus","⊕","直和/异或"],["\\otimes","⊗","张量积"],["\\langle\\rangle","⟨⟩","内积括号"],
 ["\\cdot","·","点乘"],["\\circ","∘","复合"],["\\star","⋆","星乘"],
 ["\\hbar","ℏ","约化普朗克常数"],["\\nabla^2","∇²","拉普拉斯算符"],["\\partial^2","∂²","二阶偏导"],
 ["^{2}","上标 2","上标（平方）"],["_{i}","下标 i","下标"],["\\text{...}","正文","数学模式中插入文本"],
 ["\\mathrm{d}","d","正体微分 d"],["\\langle x \\rangle","⟨x⟩","期望值"],["\\delta_{ij}","δ_ij","克罗内克 delta"],
 ["\\epsilon_0","ε₀","真空介电常数"],["\\mu_0","μ₀","真空磁导率"],["c^2","c²","光速平方"],
 ["E=mc^2","E=mc²","质能方程"],["\\hbar\\omega","ℏω","光子能量"],["\\frac{1}{2}mv^2","½mv²","动能"],
 ["\\nabla\\cdot E","∇·E","高斯定律（散度）"], ["\\oint E\\cdot dA","∮E·dA","电通量积分"],["\\vec{F}=m\\vec{a}","F=ma","牛顿第二定律"],
 ["\\begin{equation}","","单行编号公式环境"],["\\begin{align}","","多行对齐公式（& 对齐）"],["\\begin{gather}","","多行居中公式"],
 ["\\tilde{x}","x̃","波浪号"],["\\acute{x}","x́","锐音符"],["\\grave{x}","x̀","重音符"],["\\check{x}","x̌","抑扬符"],["\\breve{x}","x̆","短音符"],["\\widetilde{xy}","xỹ","宽波浪号"],
 ["\\mathbf{x}","x","粗体（向量/矩阵）"],["\\mathit{x}","x","斜体"],["\\mathsf{x}","x","无衬线体"],["\\mathfrak{x}","x","哥特体"],["\\tt{x}","x","等宽体"],
 ["\\,","thin","极细间距"],["\\:","med","中等间距"],["\\;","thick","粗间距"],["\\!","neg","负间距"],["\\quad","1em","1em 间距"],["\\qquad","2em","2em 间距"],
 ["\\odot","⊙","阿达马积（逐元乘）"],["\\setminus","∖","集合差"],["\\supset","⊃","超集"],["\\sqsubseteq","⊑","方包含于"],["\\cong","≅","同构"],["\\sim","∼","相似/渐近"],["\\propto","∝","正比于"],["\\perp","⊥","垂直"],["\\parallel","∥","平行"],["\\angle","∠","角"],["\\triangle","△","三角形"],["\\aleph","ℵ","阿列夫基数"],["\\prime","′","撇（导数记号）"],
 ["\\bigoplus","⨁","大直和"],["\\bigotimes","⨂","张大张量积"],["\\bigcup","⋃","大并集"],["\\bigcap","⋂","大交集"],["\\bigwedge","⋀","大 wedge"],["\\bigvee","⋁","大 vee"],
 ["\\varsigma","ς","小写 v 变体"],["\\vartheta","ϑ","小写 theta 变体"],["\\varphi","φ","小写 phi 变体"],["\\varkappa","ϰ","小写 kappa 变体"],["\\varepsilon","ε","小 epsilon 变体"],["\\Xi","Ξ","大写 Xi"],["\\Pi","Π","大写 Pi"],["\\Psi","Ψ","大写 Psi"],["\\Upsilon","Υ","大写 Upsilon"],
 ["\\leftarrow","←","左箭头"],["\\rightarrow","→","右箭头"],["\\uparrow","↑","上箭头"],["\\downarrow","↓","下箭头"],["\\leftrightarrow","↔","左右箭头"],["\\hookrightarrow","↪","钩箭头"],["\\longrightarrow","⟶","长右箭头"],["\\Longrightarrow","⟹","长双右箭头"],["\\nearrow","↗","右上箭头"],["\\searrow","↘","右下箭头"],["\\swarrow","↙","左下箭头"],["\\nwarrow","↖","左上箭头"],
 ["\\%","%","百分号"],["\\#","#","井号"],["\\$","$","美元符"],["\\&","&","和号"],["\\_","_","下划线"],["\\{","{","左花括号"],["\\}","}","右花括号"],["\\backslash","\\","反斜杠"],["\\lfloor","⌊","左下取整"],["\\rfloor","⌋","右下取整"],["\\lceil","⌈","左上取整"],["\\rceil","⌉","右上取整"],["\\mid","∣","整除"],["\\nmid","∤","不整除"],["\\colon","∶","关系冒号"],
 ["\\ldots","…","水平省略号"],["\\cdots","⋯","居中省略号"],["\\vdots","⋮","竖直省略号"],["\\ddots","⋱","对角省略号"],["\\mp","∓","负正号"],["\\quad\\quad","2em","双四字间隔"],
]

TOOLS += [
{
 "slug":"emoji-picker","industry":"it","cat":"dev","icon":"😊","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Emoji 选择器",
 "h1":"Emoji 选择器",
 "h2":"😊 Emoji 选择器",
 "desc":"Emoji 选择器 - 输入关键词搜索 emoji，按分类筛选，点击即可复制。内置常用 emoji 数据集，纯前端本地处理。",
 "intro":"写文案、注释、社交内容时想快速插入 emoji？输入中文或英文关键词（如“笑”“fire”“爱心”），点一下就复制到剪贴板。",
 "inputs":[
   {"id":"q","label":"搜索关键词（中/英，如 笑 / fire / 爱心）","type":"text","value":"","placeholder":"笑 / fire / 爱心"}
 ],
 "calc":"""
var EMOJI=%s;
function copyEmoji(btn){ var ch=btn.querySelector('.ec').textContent; var t=document.createElement('textarea'); t.value=ch; document.body.appendChild(t); t.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(t); var tip=document.getElementById('copyTip'); if(tip){tip.textContent='已复制 '+ch;} }
var q=(document.getElementById('q').value||'').toLowerCase().trim();
var list=EMOJI.filter(function(e){ return !q || e[1].toLowerCase().indexOf(q)>=0 || e[2].toLowerCase().indexOf(q)>=0 || e[0]===q; });
var html='<div class="result-title">共 '+list.length+' 个 emoji（点击复制）</div><div class="emoji-grid">';
for(var i=0;i<list.length;i++){ var e=list[i]; html+='<button type="button" class="emoji-cell" onclick="copyEmoji(this)"><span class="ec">'+e[0]+'</span><span class="en">'+escH(e[1])+'</span></button>'; }
html+='</div><div id="copyTip" class="muted" style="margin-top:8px;"></div>';
document.getElementById('result').innerHTML=html;
""" % json.dumps(EMOJI_DATA, ensure_ascii=False),
 "notes":[
   "支持中英文关键词，按 emoji 名称与中文释义模糊匹配；留空显示全部。",
   "点击任意 emoji 即复制到剪贴板（兼容无 HTTPS/剪贴板 API 的环境，使用 execCommand 兜底）。",
   "内置约 180 个常用 emoji；更多字符建议用系统输入法的 emoji 面板。"
 ],
 "ref":""
},
{
 "slug":"latex","industry":"it","cat":"dev","icon":"📐","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"LaTeX 符号与命令速查",
 "h1":"LaTeX 符号与命令速查",
 "h2":"📐 LaTeX 符号与命令速查",
 "desc":"LaTeX 符号与命令速查 - 搜索常用 LaTeX 数学符号与命令，查看写法与示例，点击复制命令。纯前端本地处理。",
 "intro":"写论文、笔记、公式时记不住某个符号的 LaTeX 命令？输入关键词（如 alpha、积分、求和、向量）即时筛选，点命令即复制。",
 "inputs":[
   {"id":"q","label":"搜索（中/英，如 alpha / 积分 / 矩阵 / 向量）","type":"text","value":"","placeholder":"alpha / 积分 / 矩阵"}
 ],
 "calc":"""
var LATEX=%s;
function copyLatex(btn){ var cmd=btn.textContent; var t=document.createElement('textarea'); t.value=cmd; document.body.appendChild(t); t.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(t); var tip=document.getElementById('copyTip'); if(tip){tip.textContent='已复制 '+cmd;} }
var q=(document.getElementById('q').value||'').toLowerCase().trim();
var list=LATEX.filter(function(e){ return !q || e[0].toLowerCase().indexOf(q)>=0 || e[2].toLowerCase().indexOf(q)>=0; });
var html='<div class="result-title">共 '+list.length+' 条（点击命令复制）</div><table class="sym-table"><tr><th>命令</th><th>示例</th><th>说明</th></tr>';
for(var i=0;i<list.length;i++){ var e=list[i]; html+='<tr><td><button type="button" class="copy-btn" onclick="copyLatex(this)">'+escH(e[0])+'</button></td><td class="sym-ex">'+escH(e[1])+'</td><td>'+escH(e[2])+'</td></tr>'; }
html+='</table><div id="copyTip" class="muted" style="margin-top:8px;"></div>';
document.getElementById('result').innerHTML=html;
""" % json.dumps(LATEX_DATA, ensure_ascii=False),
 "notes":[
   "覆盖希腊字母、运算符号、关系符号、大型算符、矩阵/括号、集合、逻辑、导数与常见物理公式命令。",
   "命令中的反斜杠为 LaTeX 转义符；复制到编辑器/Markdown 数学块（如 $...$ 或 $$...$$）即可渲染。",
   "本工具为文本速查，不含 KaTeX/MathJax 实时渲染；需要预览渲染结果请接入对应库。"
 ],
 "ref":""
},
]

import json

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
