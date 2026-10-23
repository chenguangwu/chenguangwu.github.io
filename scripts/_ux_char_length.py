#!/usr/bin/env python3
# _ux_char_length.py — UX 工具特异性功能重做 · F-CHAR-1（pilot）
# 给「距离/长度类」工具注入一个自包含的「距离量级感知」特征模块：
#   输入米数 → 自动对照常见参照物（跑道/珠峰/马拉松/赤道/地月/日地），建立量级概念。
# 设计要点：
#   1. 自包含：自带 <input> + 参照数据，不读主 calc，不耦合页面逻辑。
#   2. 构建安全：注入 <section>（div 非 p，避开 _prerender_tool_body 首 p 覆写）置于 </body> 前；查重防重复。
#   3. 英文态零中文：静态 HTML 不放中文，全部文本由 JS 按 ?lang=en-US（读 location.search，
#      不依赖 TBKit 加载时序）填充；EN 态全英文、ZH 态全中文，--check 真机审计无残留。
import sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'id="__charDist"'   # 查重标记

# 参照物：[中文名, 英文名, 米]
REFS = [
    ["标准跑道一圈", "Standard track lap", 400],
    ["足球场长度", "Soccer field length", 105],
    ["一层楼高", "One floor height", 3],
    ["成年人身高", "Adult height", 1.7],
    ["珠穆朗玛峰", "Mount Everest", 8848.86],
    ["马拉松", "Marathon", 42195],
    ["赤道周长", "Earth equator", 40075000],
    ["地月距离", "Earth–Moon", 384400000],
    ["日地距离", "Earth–Sun", 149600000000],
]

def build_section():
    rows_js = ",\n".join('    [%r, %r, %r]' % (c, e, v) for c, e, v in REFS)
    # 静态 HTML 文本全部留空，由 JS 按语言填充（避免静态中文被 i18n 扫描残留）
    html = r'''<section class="char-module" id="__charDist" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="__charDistTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="__charDistDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:10px;">
    <input type="number" id="__charDistVal" value="1000" min="0" step="any" style="width:160px;padding:6px 8px;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text);" oninput="__charDistUpdate()">
    <span id="__charDistUnit"></span>
  </div>
  <div id="__charDistOut" style="font-size:14px;line-height:1.8;"></div>
  <details style="margin-top:10px;">
    <summary id="__charDistSum" style="cursor:pointer;color:var(--primary);font-size:13px;"></summary>
    <table style="width:100%;border-collapse:collapse;margin-top:8px;font-size:13px;">
      <thead><tr><th style="text-align:left;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charDistTh1"></th><th style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charDistTh2"></th></tr></thead>
      <tbody id="__charDistRef"></tbody>
    </table>
  </details>
</section>
<script>
(function(){
  var REFS = [
''' + rows_js + r'''
  ];
  function __charFmt(n, en){
    if(n>=1e8) return (en? (n/1e9).toFixed(2)+' billion m' : (n/1e8).toFixed(2)+' 亿米');
    if(n>=1e4) return (n/1000).toFixed(n>=1e6?0:1)+' km';
    if(n>=1000) return (n/1000).toFixed(2)+' km';
    if(n>=1) return n.toFixed(n<10?2:0)+' m';
    return (n*100).toFixed(1)+' cm';
  }
  function __charIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function __charDistUpdate(){
    var en = __charIsEn();
    var v = parseFloat(document.getElementById('__charDistVal').value);
    var out = document.getElementById('__charDistOut');
    if(!isFinite(v)||v<=0){ out.textContent=''; return; }
    var below=null, above=null;
    for(var i=0;i<REFS.length;i++){
      if(REFS[i][2]<=v) below=REFS[i];
      if(REFS[i][2]>=v && above===null) above=REFS[i];
    }
    var parts=[];
    if(below) parts.push((v/below[2]).toFixed(2)+' × '+(en?below[1]:below[0]));
    if(above && above!==below) parts.push((v/above[2]).toFixed(3)+' × '+(en?above[1]:above[0]));
    out.textContent = (en?'≈ ':'约 ')+parts.join(' / ');
    var tb=document.getElementById('__charDistRef');
    if(tb && !tb.dataset.filled){
      var rows='';
      for(var j=0;j<REFS.length;j++){
        rows+='<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">'+(en?REFS[j][1]:REFS[j][0])+'</td><td style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);">'+__charFmt(REFS[j][2], en)+'</td></tr>';
      }
      tb.innerHTML=rows; tb.dataset.filled='1';
    }
  }
  function __charInit(){
    var en = __charIsEn();
    document.getElementById('__charDistTitle').textContent = en?'📏 Distance Magnitude Sense':'📏 距离量级感知';
    document.getElementById('__charDistDesc').textContent = en?'Enter a length or distance in meters to compare against common references.':'输入一个长度或距离（米），直观对照常见参照物，建立量级概念。';
    document.getElementById('__charDistSum').textContent = en?'Common distance references':'常见距离参照';
    document.getElementById('__charDistUnit').textContent = en?'meters (m)':'米 (m)';
    document.getElementById('__charDistTh1').textContent = en?'Reference':'参照物';
    document.getElementById('__charDistTh2').textContent = en?'Length':'长度';
    __charDistUpdate();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__charInit);
  else __charInit();
})();
</script>
'''
    return html

def inject(path):
    s = open(path, encoding='utf-8').read()
    if MARK in s:
        return False  # 已注入，跳过
    sec = build_section()
    if '</body>' in s:
        s = s.replace('</body>', sec + '\n</body>', 1)
    else:
        s = s + sec
    open(path, 'w', encoding='utf-8').write(s)
    return True

def main():
    targets = sys.argv[1:] or []
    if not targets:
        print("usage: _ux_char_length.py <tool1.html> [tool2.html] ...")
        sys.exit(1)
    done = 0
    skip = 0
    for t in targets:
        p = t if os.path.isabs(t) else os.path.join(ROOT, t)
        if not os.path.exists(p):
            print("MISS", t); continue
        if inject(p): done += 1
        else: skip += 1
    print("injected=%d skipped(already)=%d" % (done, skip))

if __name__ == '__main__':
    main()
