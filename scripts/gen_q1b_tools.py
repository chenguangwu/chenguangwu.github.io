#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 批次 02 生成器：5 个 it-tools 风格工具（CSV/YAML/网络/文本/参考）。
复用 gen_q1_tools 的 TEMPLATE 范式（inputs + calcTool + __REF__）。
用法：python3 scripts/gen_q1b_tools.py
生成：
  it/csv-to-yaml.html       CSV 转 YAML
  it/mac-generator.html     MAC 地址生成器
  it/ipv6-ula.html          IPv6 ULA 生成器
  it/phone-parser.html      电话号码解析与格式化
  it/git-cheatsheet.html    Git 命令速查表
"""
from gen_q1_tools import TEMPLATE, IND_ZH, BASE, render_inputs, render_reset, render
import os

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")

TOOLS = [
{
 "slug":"csv-to-yaml","industry":"it","cat":"dev","icon":"📄","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"CSV 转 YAML 转换器",
 "h1":"CSV 转 YAML 转换器",
 "h2":"📄 CSV 转 YAML 转换器",
 "desc":"CSV 转 YAML 转换器 - 粘贴 CSV 文本，一键转为 YAML 列表（首行作表头）或纯数组，支持引号包裹字段。纯前端本地处理。",
 "intro":"在配置、CI、Kubernetes 等场景常需要在 CSV 与 YAML 之间互转。首行会被当作字段名生成键值对；若首行也想要数组，可勾选“无表头”。",
 "inputs":[
   {"id":"csv","label":"输入 CSV","type":"textarea","rows":"6","value":"name,age,city\nAlice,30,Beijing\nBob,25,Shanghai"},
   {"id":"nohead","label":"无表头（按列数组输出）","type":"checkbox","opts":[["1","是"]]}
 ],
 "calc":"""
var raw=document.getElementById('csv').value||'';
if(!raw.trim()){ document.getElementById('result').innerHTML='<p class="muted">请输入 CSV 文本</p>'; return; }
var lines=raw.replace(/\\r/g,'').split('\\n').filter(function(l){return l.length>0;});
function splitCsv(line){
  var out=[], cur='', q=false;
  for(var i=0;i<line.length;i++){
    var ch=line[i];
    if(ch==='\\\"'){ if(q && line[i+1]==='\\\"'){cur+='\\\"';i++;} else {q=!q;} }
    else if(ch===',' && !q){ out.push(cur); cur=''; }
    else { cur+=ch; }
  }
  out.push(cur); return out;
}
var rows=lines.map(splitCsv);
var nohead=document.getElementById('top_1') ? document.getElementById('top_1').checked : false;
var yaml='';
if(nohead){
  for(var r=0;r<rows.length;r++){ yaml+='- ['+rows[r].map(function(x){return JSON.stringify(x);}).join(', ')+']\\n'; }
}else{
  var head=rows[0];
  for(var r=1;r<rows.length;r++){
    yaml+='- '+head.map(function(h,c){return h+': '+JSON.stringify(rows[r][c]||'');}).join('\\n  ')+'\\n';
  }
}
var html='<div class="result-title">YAML 输出</div><pre class="code-block">'+escH(yaml)+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "逗号、换行、双引号会被自动按 RFC 4180 处理；包含逗号/换行的字段请用双引号包裹。",
   "无表头模式输出为嵌套数组，有表头模式输出为键值对列表。",
   "值为空时输出空字符串；如需 null 可后续手动替换。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📄 YAML 基础语法</h3>
  <table class="ref-table">
    <tr><th>结构</th><th>写法</th></tr>
    <tr><td>列表</td><td>- item1<br>- item2</td></tr>
    <tr><td>映射</td><td>key: value</td></tr>
    <tr><td>嵌套</td><td>parent:<br>&nbsp;&nbsp;child: 1</td></tr>
    <tr><td>多行文本</td><td>text: |<br>&nbsp;&nbsp;line1<br>&nbsp;&nbsp;line2</td></tr>
  </table>
  <p>本工具输出采用 2 空格缩进的标准 YAML；引号由 JSON.stringify 处理特殊字符，可被常见 YAML 解析器直接读取。</p>
</div>
"""
},
{
 "slug":"mac-generator","industry":"it","cat":"dev","icon":"🔗","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"MAC 地址生成器",
 "h1":"MAC 地址生成器",
 "h2":"🔗 MAC 地址生成器",
 "desc":"MAC 地址生成器 - 批量生成随机 MAC 地址，可选常见厂商 OUI 前缀，结果可一键复制。纯前端本地生成。",
 "intro":"做网络仿真、设备 Mock、MAC 过滤测试时常需要伪造 MAC。设置数量与前缀（可选），生成格式正确的 MAC 地址。",
 "inputs":[
   {"id":"cnt","label":"生成数量","value":"5","step":"1","min":"1","max":"50"},
   {"id":"oui","label":"OUI 厂商前缀","type":"select","opts":[["","随机（不使用 OUI）"],["00:1A:79","VMware"],["00:50:56","VMware ESX"],["02:00:00","本地管理/私有"],["3C:5A:B4","Google"],["AC:BC:32","Cisco"]]}
 ],
 "calc":"""
var cnt=Math.min(Math.max(parseInt(num('cnt'))||5,1),50);
var oui=document.getElementById('oui').value;
function rnd(){ return Math.floor(Math.random()*256).toString(16).toUpperCase().padStart(2,'0'); }
var lines=[];
for(var i=0;i<cnt;i++){
  var bytes = oui? oui.split(':') : [rnd(),rnd()];
  while(bytes.length<6){ bytes.push(rnd()); }
  lines.push(bytes.join(':'));
}
var html='<div class="result-title">生成的 MAC 地址（'+cnt+' 个）</div><pre class="code-block">'+escH(lines.join('\\n'))+'</pre>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "第二字节第 2 位（第 2 个十六进制字符的低位）为 1 表示“本地管理（LAA）”，为 0 表示“全局唯一（UAA）”。",
   "选 OUI 仅用于视觉上像某厂商，并不保证真实可达，仅供测试/Mock。",
   "每次点击“计算”重新随机生成。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>🔗 常见 OUI 厂商前缀</h3>
  <table class="ref-table">
    <tr><th>前缀</th><th>厂商</th></tr>
    <tr><td>00:1A:79</td><td>VMware</td></tr>
    <tr><td>00:50:56</td><td>VMware ESX</td></tr>
    <tr><td>AC:BC:32</td><td>Cisco</td></tr>
    <tr><td>3C:5A:B4</td><td>Google</td></tr>
    <tr><td>02:00:00</td><td>本地管理（私有）</td></tr>
  </table>
  <p>MAC 共 48 位（6 字节），前 24 位为 OUI（厂商分配），后 24 位由厂商自行分配。</p>
</div>
"""
},
{
 "slug":"ipv6-ula","industry":"it","cat":"dev","icon":"🌐","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"IPv6 ULA 生成器",
 "h1":"IPv6 ULA 生成器",
 "h2":"🌐 IPv6 ULA 生成器",
 "desc":"IPv6 ULA 生成器 - 生成 IPv6 唯一本地地址（fd00::/8）前缀与示例地址，支持随机全局 ID。纯前端本地生成。",
 "intro":"ULA（Unique Local Address）相当于 IPv6 的“内网地址”，前缀 fd00::/8，用于站点内部通信、不会路由到公网。生成 48 位前缀与完整示例地址。",
 "inputs":[
   {"id":"cnt","label":"生成数量","value":"3","step":"1","min":"1","max":"20"}
 ],
 "calc":"""
var cnt=Math.min(Math.max(parseInt(num('cnt'))||3,1),20);
function h(n){ var s=''; for(var i=0;i<n;i++){ s+=Math.floor(Math.random()*16).toString(16).toUpperCase(); } return s; }
function grp(s){ var o=[]; for(var i=0;i<s.length;i+=4){ o.push(s.substr(i,4)); } return o.join(':'); }
var lines=[];
for(var i=0;i<cnt;i++){
  var g=h(10); // 40-bit global ID
  var prefix='fd'+g.substr(0,2)+':'+g.substr(2,4)+':'+g.substr(6,4);
  var addr=prefix+'::'+grp(h(16));
  lines.push(prefix+'::/48   示例 '+addr);
}
var html='<div class="result-title">生成的 IPv6 ULA（'+cnt+' 个）</div><pre class="code-block">'+escH(lines.join('\\n'))+'</pre>';
html+='<p class="muted">前缀格式 fdxx:xxxx:xxxx::/48（第 8 位固定为 fd，即二进制 1111 1101 0 + 全局 ID 40 位 + 子网 16 位）</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "ULA 前缀固定以 fd00::/8 开头，第 9–48 位为随机全局 ID，保证站点间冲突概率极低。",
   "ULA 不可被公网路由，仅用于内部寻址；需要公网可用 2001:db8:: 等全球单播地址。",
   "IPv6 地址建议小写书写，此处为大写展示便于阅读。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>🌐 IPv6 地址类型速查</h3>
  <table class="ref-table">
    <tr><th>类型</th><th>前缀</th><th>用途</th></tr>
    <tr><td>ULA 唯一本地</td><td>fd00::/8</td><td>站点内网</td></tr>
    <tr><td>链路本地</td><td>fe80::/10</td><td>同网段</td></tr>
    <tr><td>全球单播</td><td>2000::/3</td><td>公网</td></tr>
    <tr><td>文档前缀</td><td>2001:db8::/32</td><td>文档示例</td></tr>
  </table>
  <p>ULA = fd + 40 位全局 ID + 16 位子网 ID + 64 位接口 ID，共 128 位。</p>
</div>
"""
},
{
 "slug":"phone-parser","industry":"it","cat":"dev","icon":"📞","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"电话号码解析与格式化",
 "h1":"电话号码解析与格式化",
 "h2":"📞 电话号码解析与格式化",
 "desc":"电话号码解析与格式化 - 输入任意格式电话号码，按所选国家输出 E.164 与国际/国内格式分组。纯前端本地处理。",
 "intro":"把用户粘贴的“138-0013-8000”这类乱序号码整理成标准格式。选择国家后得到带国家码的 E.164（+86...）与分组显示。",
 "inputs":[
   {"id":"phone","label":"输入电话号码","type":"text","value":"13800138000","placeholder":"如 13800138000"},
   {"id":"cc","label":"国家/地区","type":"select","opts":[["86","中国 +86"],["1","美国/加拿大 +1"],["44","英国 +44"],["81","日本 +81"],["91","印度 +91"],["852","香港 +852"],["886","台湾 +886"],["65","新加坡 +65"],["61","澳大利亚 +61"]]}
 ],
 "calc":"""
var phone=document.getElementById('phone').value||'';
var cc=document.getElementById('cc').value;
var digits=phone.replace(/[^0-9]/g,'');
if(!digits){ document.getElementById('result').innerHTML='<p class="muted">请输入数字电话号码</p>'; return; }
var e164='+'+cc+digits;
// 国内分组：从右按 3-4-4 简化
function grp(s){ var a=[]; while(s.length>4){ a.unshift(s.slice(-4)); s=s.slice(0,-4); } if(s) a.unshift(s); return a.join(' '); }
var national=grp(digits);
var html='<div class="result-title">解析结果</div>';
html+='<div class="big-result">E.164 <b>'+e164+'</b></div>';
html+='<p class="muted">国内格式（按位分组）：'+national+'</p>';
html+='<p class="muted">国家/地区代码：+'+cc+'</p>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "E.164 是国际电信标准格式：+ 国家码 + 国内号码（不含分隔符与首位 0）。",
   "本工具为轻量格式化（按位分组），不校验号段有效性；严格校验请用 libphonenumber 等服务。",
   "若原号码已含国家码，请选择对应国家再粘贴纯数字。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>📞 常用国家代码</h3>
  <table class="ref-table">
    <tr><th>代码</th><th>地区</th><th>代码</th><th>地区</th></tr>
    <tr><td>+86</td><td>中国</td><td>+1</td><td>美国/加拿大</td></tr>
    <tr><td>+44</td><td>英国</td><td>+81</td><td>日本</td></tr>
    <tr><td>+91</td><td>印度</td><td>+852</td><td>香港</td></tr>
    <tr><td>+886</td><td>台湾</td><td>+65</td><td>新加坡</td></tr>
  </table>
  <p>提示：很多国家国内号码首位为 0（如英国 0xxxx），写入 E.164 时需去掉该 0。</p>
</div>
"""
},
{
 "slug":"git-cheatsheet","industry":"it","cat":"dev","icon":"🌿","bg":"#eff6ff","accent":"#3B82F6","indicon":"💻",
 "title":"Git 命令速查表",
 "h1":"Git 命令速查表",
 "h2":"🌿 Git 命令速查表",
 "desc":"Git 命令速查表 - 按分类检索常用 Git 命令与说明，支持关键词过滤，复制即用的命令。纯前端本地检索。",
 "intro":"忘记某个 Git 操作怎么写？输入关键词（如 rebase / 回退 / 分支）即时过滤命令表，点“复制”拿走。",
 "inputs":[
   {"id":"q","label":"搜索关键词（命令/说明/分类）","type":"text","value":"","placeholder":"如 rebase、回退、分支"}
 ],
 "calc":"""
var DATA=[
 ['init','git init','在当前目录初始化仓库','基础'],
 ['clone','git clone <url>','克隆远程仓库到本地','基础'],
 ['status','git status','查看工作区状态','基础'],
 ['add','git add .','暂存所有改动','基础'],
 ['commit','git commit -m "msg"','提交暂存区','基础'],
 ['log','git log --oneline','查看简洁提交历史','基础'],
 ['branch','git branch','列出本地分支','分支'],
 ['checkout','git checkout <b>','切换分支','分支'],
 ['switch','git switch <b>','切换分支（新写法）','分支'],
 ['branch -c','git branch -c <b>','基于当前分支新建并切换','分支'],
 ['merge','git merge <b>','把分支合并到当前','分支'],
 ['rebase','git rebase <b>','把当前分支变基到目标','分支'],
 ['merge --abort','git merge --abort','中止进行中的合并','分支'],
 ['reset','git reset --soft HEAD~1','回退提交保留改动','回退'],
 ['revert','git revert <hash>','用新提交抵消某提交','回退'],
 ['checkout --','git checkout -- <f>','丢弃文件未暂存改动','回退'],
 ['clean','git clean -fd','删除未跟踪文件/目录','回退'],
 ['remote -v','git remote -v','查看远程地址','远程'],
 ['push','git push','推送当前分支','远程'],
 ['push -u','git push -u origin <b>','首次推送并关联上游','远程'],
 ['pull','git pull','拉取并合并远程','远程'],
 ['fetch','git fetch','仅获取远程更新不合并','远程'],
 ['stash','git stash','暂存工作区改动','暂存'],
 ['stash pop','git stash pop','恢复最近暂存','暂存'],
 ['diff','git diff','查看未暂存差异','查看'],
 ['diff --cached','git diff --cached','查看已暂存差异','查看'],
 ['show','git show <hash>','显示某提交内容','查看'],
 ['tag','git tag <v>','打标签','其他'],
 ['amend','git commit --amend','修改最近一次提交','其他'],
 ['cherry-pick','git cherry-pick <hash>','摘取某提交到当前','其他'],
 ['bisect','git bisect start','二分查找引入 bug 的提交','其他']
];
var q=document.getElementById('q').value.toLowerCase().trim();
var rows=DATA.filter(function(d){ return !q || d[0].toLowerCase().indexOf(q)>=0 || d[1].toLowerCase().indexOf(q)>=0 || d[2].toLowerCase().indexOf(q)>=0 || d[3].toLowerCase().indexOf(q)>=0; });
if(rows.length===0){ document.getElementById('result').innerHTML='<p class="muted">未找到匹配命令，换个关键词试试。</p>'; return; }
var html='<div class="result-title">匹配命令（'+rows.length+' 条）</div><table class="ref-table"><tr><th>分类</th><th>命令</th><th>说明</th></tr>';
for(var i=0;i<rows.length;i++){ html+='<tr><td>'+rows[i][3]+'</td><td><code>'+escH(rows[i][1])+'</code></td><td>'+escH(rows[i][2])+'</td></tr>'; }
html+='</table>';
document.getElementById('result').innerHTML=html;
""",
 "notes":[
   "rebase 会改写提交历史，协作分支上请谨慎使用；个人分支或 feature 分支更合适。",
   "reset --hard 会丢失未提交改动，必要时先用 stash 暂存。",
   "推送前建议先 pull / fetch 解决冲突，避免强制 push 覆盖他人提交。"
 ],
 "ref":"""
<div class="tool-ref">
  <h3>🌿 工作流建议</h3>
  <p><b>Feature 分支：</b>switch -c feat → 开发 → commit → push -u → PR/MR → merge。</p>
  <p><b>同步主干：</b>switch main → pull → switch feat → rebase main → push --force-with-lease。</p>
  <p><b>回退错误：</b>未推送用 reset/revert；已推送用 revert 生成新提交，安全可追溯。</p>
</div>
"""
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
