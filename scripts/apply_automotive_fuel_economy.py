#!/usr/bin/env python3
# 重建 automotive/fuel-economy.html（第三版，鲁棒写法）。
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'tools/automotive/fuel-economy.html')
s = open(p, encoding='utf-8').read()

# 以 </head> 为界切出干净 head（含 og/ld/script 注入，剔除任何畸形 body 残留）
head = s.split('</head>')[0] + '</head>'

CONTENT = '''<h1 class="sr-only">油耗计算器</h1>
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ 油耗计算器</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>
<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">🚗 汽车交通</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">油耗计算器</span>
</nav>
<div class="container">
  <div class="card tool-card-accent" style="--tool-accent:#dc2626;">
    <h2 data-zh="⛽ 油耗计算器">⛽ 油耗计算器</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="输入加油量、行驶里程与油价，计算百公里油耗、单次油费、可续航里程与碳排放">输入加油量、行驶里程与油价，计算百公里油耗、单次油费、可续航里程与碳排放。</p>
    <div class="input-row">
      <div><label>本次加油量 (L)</label><input type="number" id="fuelL" value="40" oninput="calc()" min="0" step="any"></div>
      <div><label>本次行驶里程 (km)</label><input type="number" id="dist" value="560" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>油价 (元/L)</label><input type="number" id="price" value="8" oninput="calc()" min="0" step="any"></div>
      <div><label>油箱容量 (L)</label><input type="number" id="tank" value="50" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>当前剩余油量 (L)</label><input type="number" id="remain" value="10" oninput="calc()" min="0" step="any"></div>
      <div><label>月度行驶里程 (km/月)</label><input type="number" id="monthKm" value="1500" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="safe-main" id="result"></div>
    <div class="dist-grid" id="distGrid"></div>
    <div class="formula-box" id="formulaBox"></div>
    <div id="adviceBox"></div>
  </div>
  <div class="card">
    <h3>📖 省油与用车建议</h3>
    <div class="scene-card">
      <h4>🛣️ 平稳驾驶</h4>
      <p>急加速、急刹车会显著抬高瞬时油耗。保持匀速、预判路况，城市工况可省油 10%–15%。</p>
    </div>
    <div class="scene-card">
      <h4>🔧 保养与胎压</h4>
      <p>胎压低于标准 20% 约增加 3% 油耗；按期更换空滤、机油，让发动机维持在设计工况。</p>
    </div>
    <div class="scene-card">
      <h4>📊 负载与风阻</h4>
      <p>车顶行李架、过多随车重物都会抬高风阻与滚动阻力。长途前清理后备箱可降耗。</p>
    </div>
    <div class="info-box">💡 油耗是滚动参考值：基于近期加油与里程推算，路况、空调、载重变化都会让实际值偏离。长途以实际加油节奏为准。</div>
  </div>

<!-- TOOLBOX-DEEP-DIVE -->
<style>
.deep-dive{max-width:960px;margin:16px auto;padding:0 16px;}
.deep-dive > .card{margin-bottom:0;}
@media(max-width:600px){.deep-dive{margin:14px auto;padding:0 12px;}}
.deep-dive .dd-list{margin:8px 0 16px;padding-left:20px;}
.deep-dive .dd-list li{margin:6px 0;line-height:1.75;}
.deep-dive .dd-example{background:var(--card-bg,#fff);border:1px solid var(--border,#eee);border-radius:10px;padding:12px 14px;margin:8px 0 16px;}
.deep-dive .dd-ex-title{font-weight:600;color:var(--tool-accent,#FF6B35);margin-bottom:6px;}
.deep-dive .dd-ex-body{font-size:13px;line-height:1.85;color:var(--text,#333);word-break:break-word;}
.deep-dive .dd-faq{margin:8px 0 4px;}
.deep-dive .dd-faq dt{font-weight:600;margin-top:10px;color:var(--text,#333);}
.deep-dive .dd-faq dd{margin:4px 0 0;font-size:13px;line-height:1.85;color:var(--text-muted,#666);}
</style>
<section class="deep-dive" data-deep-dive="1">
<div class="card">
<h2>📚 深度解析：油耗计算器</h2>
<h3>💡 常见使用场景</h3>
<ul class="dd-list">
<li>加油后记录加油量与里程，算本次百公里油耗，判断车辆工况是否异常。</li>
<li>结合油箱余量与油耗，估算可续航里程，规划加油节奏。</li>
<li>用月度行驶里程推算月度油费与碳排放，做用车成本预算。</li>
</ul>
<div class="dd-example"><div class="dd-ex-title">示例：40L 加满、行驶 560km、油价 8 元/L</div><div class="dd-ex-body">百公里油耗 = 40 ÷ 560 × 100 ≈ 7.14 L/100km；本次油费 = 40 × 8 = 320 元；若油箱余量 10L、油耗不变，可续航 ≈ 10 ÷ 7.14 × 100 ≈ 140km；月度行驶 1500km 油费 ≈ 1500 ÷ 100 × 7.14 × 8 ≈ 857 元；碳排放 ≈ 40 × 2.31 ≈ 92.4kg CO₂。</div></div>
<h3>❓ 常见问题（FAQ）</h3>
<dl class="dd-faq">
<dt>L/100km 和 mpg 怎么换算？</dt><dd>L/100km 与 mpg 互为倒数：mpg(US)≈235.2÷L/100km，mpg(UK)≈282.5÷L/100km。数值越小越费油（L/100km）或越大越省油（mpg）。</dd>
<dt>续航估算为什么常不准？</dt><dd>续航基于近期平均油耗与剩余油量，若接下来上高速或堵车，实际油耗偏离均值，续航就会失真。它只是滚动参考，长途仍应以实际加油节奏为准。</dd>
</dl>
</div>
</section>
<!-- 注意事项区块 -->
<div class="tool-notes" style="--tool-accent:#dc2626;">
  <div class="tool-notes-title">⚠️ 使用说明与注意事项</div>
  <ul>
    <li>本工具纯前端运行，数据不会上传到服务器</li>
    <li>建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用</li>
    <li>计算结果仅供参考，请以实际应用场景为准</li>
  </ul>
</div>
</div>
<script>
var CO2_PER_L=2.31;
function fmtNum(n,d){d=d==null?2:d;if(!isFinite(n))return '--';return parseFloat(n.toFixed(d)).toString();}
function calc(){
  var fuelL=parseFloat(document.getElementById('fuelL').value);
  var dist=parseFloat(document.getElementById('dist').value);
  var price=parseFloat(document.getElementById('price').value);
  var remain=parseFloat(document.getElementById('remain').value);
  var monthKm=parseFloat(document.getElementById('monthKm').value);
  if(!(fuelL>0)||!(dist>0)){
    document.getElementById('result').innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效数值</div>';
    document.getElementById('distGrid').innerHTML='';
    document.getElementById('formulaBox').innerHTML='';
    document.getElementById('adviceBox').innerHTML='';
    return;
  }
  var L100=fuelL/dist*100;
  var costOnce=fuelL*price;
  var range=(remain>0&&L100>0)?remain/L100*100:0;
  var monthCost=(monthKm>0)?monthKm/100*L100*price:0;
  document.getElementById('result').innerHTML='<div class="safe-val">'+fmtNum(L100,2)+' L/100km</div><div class="safe-sub">本次油费 '+fmtNum(costOnce,1)+' 元</div>';
  document.getElementById('distGrid').innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(L100,2)+'</div><div class="l">百公里油耗 (L)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(costOnce,1)+'</div><div class="l">本次油费 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(range,0)+'</div><div class="l">可续航 (km)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(monthCost,0)+'</div><div class="l">月度油费 (元)</div></div>';
  document.getElementById('formulaBox').innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">百公里油耗 = 加油量 ÷ 里程 × 100</div>'+
    '<div class="fb-row">可续航 = 剩余油量 ÷ 百公里油耗 × 100</div>'+
    '<div class="fb-row">月度油费 = 月里程 ÷ 100 × 百公里油耗 × 油价</div>'+
    '<div class="fb-row">碳排放 ≈ 油耗 × '+CO2_PER_L+' kg CO₂/L</div>';
  var advice='';
  if(L100>12){advice='<div class="tip-warn">⚠️ 油耗偏高（'+fmtNum(L100,1)+' L/100km），建议检查胎压、空滤与驾驶习惯。</div>';}
  else if(L100<=6){advice='<div class="tip-success">✅ 油耗表现优秀（'+fmtNum(L100,1)+' L/100km），用车成本可控。</div>';}
  else{advice='<div class="tip-info">ℹ️ 油耗处于常态区间（'+fmtNum(L100,1)+' L/100km），保持平稳驾驶即可。</div>';}
  document.getElementById('adviceBox').innerHTML=advice;
}
calc();
</script>'''

full = head + '\n<body>\n' + CONTENT + '\n</body>\n</html>\n'
open(p, 'w', encoding='utf-8').write(full)

chk = open(p, encoding='utf-8').read()
print('重建完成 | <body>:', '<body>' in chk, '| </body>:', '</body>' in chk,
      '| formula-box:', 'formula-box' in chk, '| inputs:', len(re.findall(r'<input\b', chk)),
      '| calc:', 'function calc' in chk, '| 总行数:', chk.count(chr(10)))
