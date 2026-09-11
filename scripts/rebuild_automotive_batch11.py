#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 11。

scheduler-cycle-maintenance 保养排程表（含完成记录与历史日志）
shipping-cost-compare       快递运费比价
speed-tire                  轮胎规格与速度等级
tester-10                   喷油嘴清洗均衡测试
说明：tester-10 的 deep-dive 原为「四轮定位参数检测」，与页面（喷油嘴测试）不符，另由 fix 脚本同步。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ============================================== scheduler-cycle-maintenance
SC_INPUTS = '''    <div class="input-row">
      <div><label>当前里程 (km)</label><input type="number" id="km" value="52000" oninput="calc()" min="0" step="500"></div>
      <div><label>上次保养里程 (km)</label><input type="number" id="last" value="45000" oninput="calc()" min="0" step="500"></div>
    </div>
    <div class="input-row">
      <div><label>月均行驶里程 (km)</label><input type="number" id="kmM" value="1500" oninput="calc()" min="1" step="100"></div>
      <div><label>提醒提前量 (km)</label><input type="number" id="ahead" value="1000" oninput="calc()" min="0" step="100"></div>
    </div>
    <div class="input-row">
      <div><label>机油类型</label>
        <select id="oil" onchange="calc()">
          <option value="5000">矿物油（5000 km）</option>
          <option value="7500">半合成（7500 km）</option>
          <option value="10000" selected>全合成（10000 km）</option>
        </select>
      </div>
      <div><label>使用工况</label>
        <select id="cond" onchange="calc()">
          <option value="1.0" selected>标准工况</option>
          <option value="0.8">严苛工况（短途拥堵/多尘/重载）</option>
        </select>
      </div>
    </div>'''

SC_CARDS = '''  <div class="card">
    <h3>📋 排程项目与基准周期</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">基准周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">时间上限</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">严苛工况</th>
      </tr>
      <tr><td style="padding:6px 8px;">机油 + 机滤</td><td style="padding:6px 8px;">按所选机油类型</td><td style="padding:6px 8px;">6~12 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">空气滤芯</td><td style="padding:6px 8px;">15000 km</td><td style="padding:6px 8px;">12 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">空调滤芯</td><td style="padding:6px 8px;">15000 km</td><td style="padding:6px 8px;">12 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">汽油滤芯</td><td style="padding:6px 8px;">35000 km</td><td style="padding:6px 8px;">24 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">刹车油</td><td style="padding:6px 8px;">40000 km</td><td style="padding:6px 8px;">24 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">防冻液</td><td style="padding:6px 8px;">60000 km</td><td style="padding:6px 8px;">48 月</td><td style="padding:6px 8px;">×0.9</td></tr>
      <tr><td style="padding:6px 8px;">火花塞</td><td style="padding:6px 8px;">45000 km</td><td style="padding:6px 8px;">—</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">变速箱油</td><td style="padding:6px 8px;">70000 km</td><td style="padding:6px 8px;">48 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">正时皮带</td><td style="padding:6px 8px;">80000 km</td><td style="padding:6px 8px;">60 月</td><td style="padding:6px 8px;">按手册</td></tr>
    </table>
    <div class="scene-card">
      <h4>🗂️ 完成记录与历史日志</h4>
      <p>清单确认后点「记录本次保养完成」，当前里程与时间会写入浏览器本地存储，历史日志按时间倒序列出。数据仅保存在本机浏览器，不会上传，清除浏览器数据会一并丢失。</p>
    </div>
    <div class="scene-card">
      <h4>📐 排程口径</h4>
      <p>各项目按「基准周期 × 工况系数」得实际周期，再按周期整倍数滚动定位下次到期里程（如 10000 km 周期、当前 52000 km 则下次 60000 km）。剩余里程小于提前量即列入「即将到期」，超期则列入「已逾期」。</p>
    </div>
    <div class="info-box">💡 本表为通用参考排程，不同车型手册差异较大，实际以随车保养手册与 4S 店记录为准。</div>
  </div>'''

SC_JS = H + '''
var SC_KEY='tb_auto_maint_log_v1';
function scLog(){
  try{ var s=localStorage.getItem(SC_KEY); return s?JSON.parse(s):[]; }catch(e){ return []; }
}
function scSave(a){
  try{ localStorage.setItem(SC_KEY, JSON.stringify(a)); }catch(e){}
}
function scRender(){
  var box=document.getElementById('logBox');
  if(!box) return;
  var a=scLog();
  if(!a.length){ box.innerHTML='<div class="scene-card"><p>暂无记录。完成保养后点击上方按钮即可留下日志。</p></div>'; return; }
  var s='<div class="scene-card"><h4>历史日志（'+a.length+' 条）</h4>';
  for(var i=0;i<a.length;i++){
    var r=a[i];
    s+='<p>· '+r.d+' | '+fmtNum(r.km,0)+' km | '+r.items+'</p>';
  }
  s+='</div>';
  box.innerHTML=s;
}
function scRecord(){
  var km=val('km'), ahead=val('ahead');
  var oilIv=val('oil'), cond=val('cond');
  var ITEMS=scItems(oilIv,cond);
  var hit=[];
  for(var i=0;i<ITEMS.length;i++){
    var o=ITEMS[i], left=o.next-km;
    if(left<=ahead) hit.push(o.name);
  }
  var now=new Date();
  var ds=now.getFullYear()+'-'+('0'+(now.getMonth()+1)).slice(-2)+'-'+('0'+now.getDate()).slice(-2);
  var a=scLog();
  a.unshift({d:ds, km:km, items:hit.length?hit.join('、'):'常规检查'});
  if(a.length>20) a=a.slice(0,20);
  scSave(a); scRender();
  var b=document.getElementById('logTip');
  if(b) b.innerHTML='<div class="tip-info">✅ 已记录 '+ds+' · '+fmtNum(km,0)+' km · '+(hit.length?hit.join('、'):'常规检查')+'</div>';
}
function scItems(oilIv, cond){
  var raw=[
    ['机油 + 机滤', oilIv, 12, cond],
    ['空气滤芯', 15000, 12, cond*0.8+0.2],
    ['空调滤芯', 15000, 12, cond*0.8+0.2],
    ['汽油滤芯', 35000, 24, cond*0.8+0.2],
    ['刹车油', 40000, 24, cond*0.8+0.2],
    ['防冻液', 60000, 48, cond*0.9+0.1],
    ['火花塞', 45000, 0, cond*0.8+0.2],
    ['变速箱油', 70000, 48, cond*0.8+0.2],
    ['正时皮带', 80000, 60, 1.0]
  ];
  var km=val('km'), out=[];
  for(var i=0;i<raw.length;i++){
    var cyc=raw[i][1]*raw[i][3];
    if(cyc<1000) cyc=1000;
    var next=Math.ceil(km/cyc)*cyc;
    if(next<=km) next=km+cyc;
    out.push({name:raw[i][0], cyc:cyc, monBase:raw[i][2], next:next, left:next-km});
  }
  return out;
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var km=val('km'), last=val('last'), kmM=val('kmM'), ahead=val('ahead');
  var oilIv=val('oil'), cond=val('cond');
  var ITEMS=scItems(oilIv,cond);

  var overdue=[], soon=[], ok=[];
  var rows='';
  for(var i=0;i<ITEMS.length;i++){
    var o=ITEMS[i], left=o.left;
    var st, col;
    if(left<=0){ st='已逾期'; col='#dc2626'; overdue.push(o.name); }
    else if(left<=ahead){ st='即将到期'; col='#d97706'; soon.push(o.name); }
    else { st='正常'; col='#059669'; ok.push(o.name); }
    var lm=kmM>0?left/kmM:Infinity;
    rows+='<tr><td style="padding:5px 8px;">'+o.name+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(o.cyc,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(o.next,0)+'</td>'
      +'<td style="padding:5px 8px;color:'+col+';">'+fmtNum(left,0)+'</td>'
      +'<td style="padding:5px 8px;">'+(isFinite(lm)&&lm>=0?fmtNum(lm,1):'—')+'</td>'
      +'<td style="padding:5px 8px;color:'+col+';">'+st+'</td></tr>';
  }

  var sinceKm=km-last;
  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">已逾期</div><div class="result-value">'+overdue.length+' 项</div></div>'
    +'<div class="result-item"><div class="result-label">即将到期</div><div class="result-value">'+soon.length+' 项</div></div>'
    +'<div class="result-item"><div class="result-label">状态正常</div><div class="result-value">'+ok.length+' 项</div></div>'
    +'<div class="result-item"><div class="result-label">距上次保养</div><div class="result-value">'+fmtNum(sinceKm,0)+' km</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>本次建议施工</h4><p>'+(overdue.length+soon.length?overdue.concat(soon).join('、'):'暂无需进店')+'</p><p>合并一次施工可省工时</p></div>'
    +'<div class="dist-card"><h4>机油实际周期</h4><p>'+fmtNum(oilIv*cond,0)+' km</p><p>基准 '+fmtNum(oilIv,0)+' km × 工况 '+fmtNum(cond,2)+'</p></div>'
    +'<div class="dist-card"><h4>最短剩余</h4><p>'+fmtNum(Math.min.apply(null,ITEMS.map(function(x){return x.left;})),0)+' km</p><p>按提前量 '+fmtNum(ahead,0)+' km 预警</p></div>'
    +'<div class="dist-card"><h4>里程折算</h4><p>'+(kmM>0?fmtNum(kmM/30.44,1)+' km/天':'—')+'</p><p>月均 '+fmtNum(kmM,0)+' km</p></div>'
    +'</div>';

  F.innerHTML='<div class="formula-title">📐 排程口径</div>'
    +'<div class="formula-line">实际周期 = 基准周期 × 工况系数（严苛工况 0.8）</div>'
    +'<div class="formula-line">下次到期里程 = ⌈当前里程 ÷ 实际周期⌉ × 实际周期</div>'
    +'<div class="formula-line">剩余里程 = 下次到期里程 − 当前里程；剩余月数 = 剩余里程 ÷ 月均里程</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">实际周期</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">下次到期</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (月)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>'
    +'<div style="margin-top:10px;"><button type="button" onclick="scRecord()" style="padding:8px 14px;border:0;border-radius:10px;background:#0369a1;color:#fff;cursor:pointer;font-size:13px;">记录本次保养完成</button></div>'
    +'<div id="logTip"></div>';

  var ad='';
  if(overdue.length) ad+='<div class="tip-bad">⛔ 已逾期 '+overdue.length+' 项：'+overdue.join('、')+'，应尽快安排施工，逾期过久会加速磨损并影响质保。</div>';
  if(soon.length) ad+='<div class="tip-warn">⚠️ 即将到期 '+soon.length+' 项：'+soon.join('、')+'，建议并入同一次进店施工以减少工时。</div>';
  if(!overdue.length&&!soon.length) ad+='<div class="tip-info">✅ 全部项目状态正常，最近一项尚有 '+fmtNum(Math.min.apply(null,ITEMS.map(function(x){return x.left;})),0)+' km 到期，无需提前保养。</div>';
  A.innerHTML=ad+'<div id="logBox"></div>';
  scRender();
}
calc();'''

# ================================================== shipping-cost-compare
SH_INPUTS = '''    <div class="input-row">
      <div><label>实际重量 (kg)</label><input type="number" id="w" value="8" oninput="calc()" min="0.1" step="0.1"></div>
      <div><label>长 (cm)</label><input type="number" id="l" value="50" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>宽 (cm)</label><input type="number" id="wd" value="40" oninput="calc()" min="1" step="1"></div>
      <div><label>高 (cm)</label><input type="number" id="h" value="30" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>抛比（体积除数）</label>
        <select id="ratio" onchange="calc()">
          <option value="6000" selected>6000（常见快递）</option>
          <option value="8000">8000（部分空运/轻抛）</option>
          <option value="12000">12000（陆运专线）</option>
        </select>
      </div>
      <div><label>配送区域</label>
        <select id="zone" onchange="calc()">
          <option value="0" selected>同城 / 省内</option>
          <option value="1">邻省</option>
          <option value="2">跨省（3 区）</option>
          <option value="3">偏远（4 区 / 新疆西藏）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>保价金额 (元，0 为不保价)</label><input type="number" id="ins" value="0" oninput="calc()" min="0" step="100"></div>
      <div><label>保价费率 (%/元)</label><input type="number" id="insr" value="0.5" oninput="calc()" min="0" max="5" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>自定义首重价 (元，0 用参考价)</label><input type="number" id="cw" value="0" oninput="calc()" min="0" step="1"></div>
      <div><label>自定义续重价 (元/kg，0 用参考价)</label><input type="number" id="cn" value="0" oninput="calc()" min="0" step="0.5"></div>
    </div>'''

SH_CARDS = '''  <div class="card">
    <h3>💰 计费重量与资费口径</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">渠道参考</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">首重</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">同城/省内</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">邻省</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">跨省</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">偏远</th>
      </tr>
      <tr><td style="padding:6px 8px;">经济快递</td><td style="padding:6px 8px;">1 kg</td><td style="padding:6px 8px;">6 / 2</td><td style="padding:6px 8px;">8 / 3</td><td style="padding:6px 8px;">10 / 4</td><td style="padding:6px 8px;">18 / 8</td></tr>
      <tr><td style="padding:6px 8px;">标准快递</td><td style="padding:6px 8px;">1 kg</td><td style="padding:6px 8px;">9 / 2.5</td><td style="padding:6px 8px;">11 / 4</td><td style="padding:6px 8px;">13 / 5</td><td style="padding:6px 8px;">22 / 10</td></tr>
      <tr><td style="padding:6px 8px;">时效快递</td><td style="padding:6px 8px;">1 kg</td><td style="padding:6px 8px;">13 / 3</td><td style="padding:6px 8px;">18 / 6</td><td style="padding:6px 8px;">23 / 8</td><td style="padding:6px 8px;">30 / 15</td></tr>
      <tr><td style="padding:6px 8px;">大件陆运</td><td style="padding:6px 8px;">3 kg</td><td style="padding:6px 8px;">15 / 2</td><td style="padding:6px 8px;">20 / 3</td><td style="padding:6px 8px;">25 / 4</td><td style="padding:6px 8px;">45 / 8</td></tr>
    </table>
    <p style="font-size:12px;color:var(--text-secondary,#6b7280);">表内为「首重价 / 续重价（元/kg）」的常见公开口径示例，仅用于横向对比的相对关系；实际报价随月结协议、促销与具体网点浮动，请用上方「自定义首重价 / 续重价」填入你的实际报价再比。</p>
    <div class="scene-card">
      <h4>⚖️ 计费重量取大者</h4>
      <p>体积重 = 长 × 宽 × 高 ÷ 抛比。计费重量取「实际重量」与「体积重」的较大值。蓬松轻抛货常按体积重计费，例如 60×50×40 cm 的箱子体积重 20 kg，实重仅 15 kg 也按 20 kg 收费。</p>
    </div>
    <div class="scene-card">
      <h4>🛡️ 保价与理赔</h4>
      <p>保价费通常按声明价值的千分之几收取并设最低收费。未保价的丢失破损多按运费倍数或设上限赔付，高价值物品建议足额保价并留存打包视频与运单。</p>
    </div>
    <div class="info-box">💡 比价时别只看运费：上门取件、送货上楼、超区附加、燃油附加与退件费都会改变总成本。</div>
  </div>'''

SH_JS = H + '''
// 参考资费：首重价/续重价（元/kg），按区域档位 [同城, 邻省, 跨省, 偏远]
var SH_CH=[
  {name:'经济快递', first:1, p:[[6,2],[8,3],[10,4],[18,8]]},
  {name:'标准快递', first:1, p:[[9,2.5],[11,4],[13,5],[22,10]]},
  {name:'时效快递', first:1, p:[[13,3],[18,6],[23,8],[30,15]]},
  {name:'大件陆运', first:3, p:[[15,2],[20,3],[25,4],[45,8]]}
];
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var w=val('w'), l=val('l'), wd=val('wd'), h=val('h');
  var ratio=val('ratio'), zone=parseInt(str('zone'),10)||0;
  var insAmt=val('ins'), insR=val('insr');
  var cw=val('cw'), cn=val('cn');

  var volW=(l*wd*h)/ratio;
  var chargeW=Math.max(w, volW);
  var byVol=volW>w;
  var insFee=insAmt>0?Math.max(1, insAmt*insR/100):0;

  var list=[];
  for(var i=0;i<SH_CH.length;i++){
    var c=SH_CH[i];
    var f=parseFloat(c.p[zone][0]), n=parseFloat(c.p[zone][1]);
    var custom=(i===0&&cw>0);
    var useF=custom?cw:f, useN=(i===0&&cn>0)?cn:n;
    var extra=Math.max(0, Math.ceil(chargeW-c.first));
    var freight=useF+extra*useN;
    list.push({name:c.name, first:c.first, f:useF, n:useN, extra:extra, freight:freight, total:freight+insFee, ref:(custom?'自定义':f+' / '+n)});
  }
  list.sort(function(a,b){ return a.total-b.total; });
  var cheap=list[0], dear=list[list.length-1];

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">实际重量</div><div class="result-value">'+fmtNum(w,2)+' kg</div></div>'
    +'<div class="result-item"><div class="result-label">体积重</div><div class="result-value">'+fmtNum(volW,2)+' kg</div></div>'
    +'<div class="result-item"><div class="result-label">计费重量</div><div class="result-value">'+fmtNum(chargeW,2)+' kg</div></div>'
    +'<div class="result-item"><div class="result-label">最低总价</div><div class="result-value">'+cheap.name+' '+fmtNum(cheap.total,2)+' 元</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>计费重量依据</h4><p>'+(byVol?'体积重':'实际重量')+'</p><p>抛比 '+fmtNum(ratio,0)+'，体积 '+fmtNum(l*wd*h/1000000,4)+' m³</p></div>'
    +'<div class="dist-card"><h4>保价费</h4><p>'+fmtNum(insFee,2)+' 元</p><p>'+(insAmt>0?'按 '+fmtNum(insR,2)+'% 计，最低 1 元':'未保价')+'</p></div>'
    +'<div class="dist-card"><h4>最低 vs 最高</h4><p>差 '+fmtNum(dear.total-cheap.total,2)+' 元</p><p>'+cheap.name+' ↔ '+dear.name+'</p></div>'
    +'<div class="dist-card"><h4>续重档位</h4><p>'+fmtNum(chargeW-cheap.first>0?Math.ceil(chargeW-cheap.first):0,0)+' kg</p><p>'+cheap.name+' 首重 '+fmtNum(cheap.first,0)+' kg</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<list.length;i++){
    var it=list[i];
    rows+='<tr><td style="padding:5px 8px;">'+(i===0?'🥇 ':'')+it.name+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(it.f,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(it.n,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(it.extra,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(it.freight,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(it.total,2)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计费口径</div>'
    +'<div class="formula-line">体积重 = 长 × 宽 × 高 ÷ 抛比；计费重量 = max(实际重量, 体积重)</div>'
    +'<div class="formula-line">运费 = 首重价 + ⌈计费重量 − 首重⌉ × 续重单价（不足首重按首重计）</div>'
    +'<div class="formula-line">总价 = 运费 + 保价费（保价金额 × 费率，最低 1 元）</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">渠道</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">首重价</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">续重价</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">续重档位</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">运费</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">总价 (元)</th></tr>'
    +rows+'</table>';

  var ad='';
  ad+='<div class="tip-info">📦 计费重量 '+fmtNum(chargeW,2)+' kg'+(byVol?'（体积重大于实重，按体积重计费）':'（实重大于体积重，按实重计费）')+'，最低总价 '+cheap.name+' '+fmtNum(cheap.total,2)+' 元。</div>';
  if(byVol) ad+='<div class="tip-warn">⚠️ 属轻抛货，缩小包装或压缩体积可直接降档省钱。</div>';
  if(chargeW>30&&list[3]) ad+='<div class="tip-info">🚚 计费重量较大，大件陆运参考总价 '+fmtNum(list.filter(function(x){return x.name==='大件陆运';})[0].total,2)+' 元，可优先对比零担专线。</div>';
  if(insAmt>0) ad+='<div class="tip-info">🛡️ 已计保价费 '+fmtNum(insFee,2)+' 元，声明价值 '+fmtNum(insAmt,0)+' 元。</div>';
  else ad+='<div class="tip-warn">⚠️ 未填写保价金额。高价值物品建议保价，未保价的赔付上限通常远低于货值。</div>';
  A.innerHTML=ad;
}
calc();'''

# ============================================================== speed-tire
ST_INPUTS = '''    <div class="input-row">
      <div><label>断面宽度 (mm)</label><input type="number" id="w" value="225" oninput="calc()" min="100" max="400" step="5"></div>
      <div><label>扁平比 (%)</label><input type="number" id="ar" value="55" oninput="calc()" min="20" max="90" step="5"></div>
    </div>
    <div class="input-row">
      <div><label>轮辋直径 (英寸)</label><input type="number" id="rim" value="17" oninput="calc()" min="12" max="24" step="0.5"></div>
      <div><label>车辆最高车速 (km/h)</label><input type="number" id="vmax" value="230" oninput="calc()" min="60" max="400" step="5"></div>
    </div>
    <div class="input-row">
      <div><label>原厂断面宽度 (mm)</label><input type="number" id="w0" value="215" oninput="calc()" min="100" max="400" step="5"></div>
      <div><label>原厂扁平比 (%)</label><input type="number" id="ar0" value="55" oninput="calc()" min="20" max="90" step="5"></div>
    </div>
    <div class="input-row">
      <div><label>原厂轮辋直径 (英寸)</label><input type="number" id="rim0" value="17" oninput="calc()" min="12" max="24" step="0.5"></div>
      <div><label>允许直径偏差 (%)</label><input type="number" id="tol" value="3" oninput="calc()" min="1" max="10" step="0.5"></div>
    </div>'''

ST_CARDS = '''  <div class="card">
    <h3>🔤 速度等级与载重指数</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">速度等级</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">最高时速</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">常见用途</th>
      </tr>
      <tr><td style="padding:6px 8px;">S</td><td style="padding:6px 8px;">180 km/h</td><td style="padding:6px 8px;">经济型家轿</td></tr>
      <tr><td style="padding:6px 8px;">T</td><td style="padding:6px 8px;">190 km/h</td><td style="padding:6px 8px;">紧凑型轿车</td></tr>
      <tr><td style="padding:6px 8px;">H</td><td style="padding:6px 8px;">210 km/h</td><td style="padding:6px 8px;">中型轿车主流</td></tr>
      <tr><td style="padding:6px 8px;">V</td><td style="padding:6px 8px;">240 km/h</td><td style="padding:6px 8px;">中高功率轿车 / SUV</td></tr>
      <tr><td style="padding:6px 8px;">W</td><td style="padding:6px 8px;">270 km/h</td><td style="padding:6px 8px;">性能车</td></tr>
      <tr><td style="padding:6px 8px;">Y</td><td style="padding:6px 8px;">300 km/h</td><td style="padding:6px 8px;">高性能跑车</td></tr>
    </table>
    <div class="scene-card">
      <h4>📏 规格换算口径</h4>
      <p>轮胎直径 = 轮辋直径 × 25.4 + 2 × 断面宽度 × 扁平比 ÷ 100（mm）。例如 225/55R17：17 × 25.4 + 2 × 225 × 0.55 = 431.8 + 247.5 = 679.3 mm。周长 = π × 直径，每公里转数 = 1000000 ÷ 周长。</p>
    </div>
    <div class="scene-card">
      <h4>⚠️ 升级改装要点</h4>
      <p>直径偏差建议控制在 ±3% 以内，超出会使速度表与里程表明显失真，还可能干涉轮拱或影响 ABS/ESP 标定。升级时优先「加宽降扁平比」保持直径接近原厂，同时核对轮毂 ET 值与胎宽是否干涉。</p>
    </div>
    <div class="info-box">💡 换胎后速度表偏差按比例产生：表显速度 ×（新周长 ÷ 原周长）≈ 实际速度。偏差明显时需重新标定或自行换算。</div>
  </div>'''

ST_JS = H + '''
function stDia(w,ar,rim){ return rim*25.4 + 2*w*ar/100; }
function stClass(v){
  var t=[['Q',160],['R',170],['S',180],['T',190],['U',200],['H',210],['V',240],['W',270],['Y',300]];
  for(var i=0;i<t.length;i++){ if(v<=t[i][1]) return t[i]; }
  return ['Y(超)',300];
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var w=val('w'), ar=val('ar'), rim=val('rim'), vmax=val('vmax');
  var w0=val('w0'), ar0=val('ar0'), rim0=val('rim0'), tol=val('tol');

  var dia=stDia(w,ar,rim), circ=Math.PI*dia, turns=1000000/circ;
  var dia0=stDia(w0,ar0,rim0), circ0=Math.PI*dia0;
  var diffPct=dia0>0?(dia-cir0/Math.PI)/dia0*100:0;
  var speedErr=circ0>0?circ/circ0:1;
  var cls=stClass(vmax);
  var ok=Math.abs(diffPct)<=tol;

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">轮胎直径</div><div class="result-value">'+fmtNum(dia,1)+' mm</div></div>'
    +'<div class="result-item"><div class="result-label">轮胎周长</div><div class="result-value">'+fmtNum(circ,1)+' mm</div></div>'
    +'<div class="result-item"><div class="result-label">每公里转数</div><div class="result-value">'+fmtNum(turns,1)+' 转</div></div>'
    +'<div class="result-item"><div class="result-label">推荐速度等级</div><div class="result-value">'+cls[0]+'（'+cls[1]+' km/h）</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>原厂直径</h4><p>'+fmtNum(dia0,1)+' mm</p><p>'+fmtNum(w0,0)+'/'+fmtNum(ar0,0)+'R'+fmtNum(rim0,1)+'</p></div>'
    +'<div class="dist-card"><h4>直径偏差</h4><p>'+(diffPct>0?'+':'')+fmtNum(diffPct,2)+' %</p><p>容差 ±'+fmtNum(tol,1)+'% → '+(ok?'可接受':'超限')+'</p></div>'
    +'<div class="dist-card"><h4>速度表偏差</h4><p>表显 100 → 实际 '+fmtNum(100*speedErr,1)+'</p><p>比例 '+fmtNum(speedErr,4)+'</p></div>'
    +'<div class="dist-card"><h4>规格写法</h4><p>'+fmtNum(w,0)+'/'+fmtNum(ar,0)+'R'+fmtNum(rim,1)+'</p><p>侧壁高度 '+fmtNum(w*ar/100,1)+' mm</p></div>'
    +'</div>';

  var rows='';
  var ars=[ar-10,ar-5,ar,ar+5,ar+10];
  for(var i=0;i<ars.length;i++){
    if(ars[i]<20||ars[i]>90) continue;
    var dd=stDia(w,ars[i],rim), dp=dia0>0?(dd-dia0)/dia0*100:0;
    rows+='<tr><td style="padding:5px 8px;">'+fmtNum(w,0)+'/'+fmtNum(ars[i],0)+'R'+fmtNum(rim,1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(dd,1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(Math.PI*dd,1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(1000000/(Math.PI*dd),1)+'</td>'
      +'<td style="padding:5px 8px;">'+(dp>0?'+':'')+fmtNum(dp,2)+' %</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 换算与判定</div>'
    +'<div class="formula-line">直径 = 轮辋直径 × 25.4 + 2 × 断面宽度 × 扁平比 ÷ 100</div>'
    +'<div class="formula-line">周长 = π × 直径；每公里转数 = 1000000 ÷ 周长</div>'
    +'<div class="formula-line">直径偏差 = (新直径 − 原厂直径) ÷ 原厂直径 × 100%</div>'
    +'<div class="formula-line">实际车速 = 表显车速 × (新周长 ÷ 原厂周长)</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">规格</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">直径 (mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">周长 (mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">转/公里</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">vs 原厂</th></tr>'
    +rows+'</table>';

  var ad='';
  ad+='<div class="tip-info">🔘 '+fmtNum(w,0)+'/'+fmtNum(ar,0)+'R'+fmtNum(rim,1)+' 直径 '+fmtNum(dia,1)+' mm、周长 '+fmtNum(circ,1)+' mm，最高车速 '+fmtNum(vmax,0)+' km/h 对应 '+cls[0]+' 级（'+cls[1]+' km/h）。</div>';
  if(!ok) ad+='<div class="tip-warn">⚠️ 直径相对原厂偏差 '+fmtNum(diffPct,2)+'%，超过 ±'+fmtNum(tol,1)+'% 容差，速度表与里程表会有可感知误差，请重新选择规格或做仪表标定。</div>';
  else ad+='<div class="tip-info">📏 直径偏差 '+fmtNum(diffPct,2)+'%，在 ±'+fmtNum(tol,1)+'% 容差内，速度表影响可接受。</div>';
  if(Math.abs(speedErr-1)>0.005) ad+='<div class="tip-info">🧭 表显 100 km/h 时实际约 '+fmtNum(100*speedErr,1)+' km/h，注意限速区间的换算。</div>';
  A.innerHTML=ad;
}
calc();'''

# =============================================================== tester-10
T10_INPUTS = '''    <div class="input-row">
      <div><label>1 缸喷油量 (mL)</label><input type="number" id="c1" value="50.5" oninput="calc()" min="0.1" step="0.1"></div>
      <div><label>2 缸喷油量 (mL)</label><input type="number" id="c2" value="49.8" oninput="calc()" min="0.1" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>3 缸喷油量 (mL)</label><input type="number" id="c3" value="50.2" oninput="calc()" min="0.1" step="0.1"></div>
      <div><label>4 缸喷油量 (mL)</label><input type="number" id="c4" value="46.5" oninput="calc()" min="0.1" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>标准喷油量 (mL)</label><input type="number" id="std" value="50" oninput="calc()" min="0.1" step="0.1"></div>
      <div><label>允许偏差 (%)</label><input type="number" id="tol" value="5" oninput="calc()" min="1" max="30" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>测试次数（同缸重复）</label><input type="number" id="rep" value="1" oninput="calc()" min="1" max="10" step="1"></div>
      <div><label>测量时长 (s)</label><input type="number" id="dur" value="60" oninput="calc()" min="5" max="300" step="5"></div>
    </div>'''

T10_CARDS = '''  <div class="card">
    <h3>🚙 喷油嘴偏差诊断参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">偏差范围</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">判定</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议处置</th>
      </tr>
      <tr><td style="padding:6px 8px;">≤ ±3%</td><td style="padding:6px 8px;">均衡良好</td><td style="padding:6px 8px;">无需处理，定期观察</td></tr>
      <tr><td style="padding:6px 8px;">±3% ~ ±5%</td><td style="padding:6px 8px;">轻微偏差</td><td style="padding:6px 8px;">可先行免拆清洗观察</td></tr>
      <tr><td style="padding:6px 8px;">±5% ~ ±10%</td><td style="padding:6px 8px;">明显失准</td><td style="padding:6px 8px;">拆检超声波清洗并复测</td></tr>
      <tr><td style="padding:6px 8px;">＞ ±10%</td><td style="padding:6px 8px;">堵塞或损坏</td><td style="padding:6px 8px;">更换该缸喷油嘴并做匹配</td></tr>
    </table>
    <div class="scene-card">
      <h4>📉 偏差过大的典型表现</h4>
      <p>某缸喷油量偏低会造成该缸混合气偏稀，表现为怠速抖动、冷启动困难、加速无力，并可能触发 P030x 失火故障码；长期失火还会因未燃燃油进入排气而烧蚀三元催化。喷油量偏大则表现为油耗升高、黑烟与积碳加剧。</p>
    </div>
    <div class="scene-card">
      <h4>🧪 测试与清洗方式</h4>
      <p>台架测试把喷油嘴装在专用设备上，以固定压力与脉宽连续喷射并称量各缸流量，结果最可比。免拆清洗通过进气或燃油管路引入清洗剂，成本低但对严重堵塞效果有限。清洗后应按同一时长复测，对比前后流量与雾化形态。</p>
    </div>
    <div class="info-box">💡 各缸偏差须在同一喷油压力、同一脉宽与同一时长下测量才有可比性；不同时长测得的绝对流量不可直接横向比较。</div>
  </div>'''

T10_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var c=[val('c1'),val('c2'),val('c3'),val('c4')];
  var std=val('std'), tol=val('tol');
  var rep=val('rep'), dur=val('dur');

  var n=c.length, sum=0;
  for(var i=0;i<n;i++) sum+=c[i];
  var mean=sum/n;

  // 样本标准差（n-1）
  var ss=0;
  for(var i=0;i<n;i++) ss+=(c[i]-mean)*(c[i]-mean);
  var sd=n>1?Math.sqrt(ss/(n-1)):0;
  var cv=mean>0?sd/mean*100:0;

  var dev=[], maxI=0;
  for(var i=0;i<n;i++){
    var dv=mean>0?(c[i]-mean)/mean*100:0;
    dev.push(dv);
    if(Math.abs(dv)>Math.abs(dev[maxI])) maxI=i;
  }
  var maxDev=dev[maxI];
  var bad=0, mild=0;
  for(var i=0;i<n;i++){ if(Math.abs(dev[i])>tol) bad++; else if(Math.abs(dev[i])>3) mild++; }
  var verdict = bad>0 ? (Math.abs(maxDev)>10?'堵塞或损坏，建议更换':'明显失准，建议拆检清洗')
              : (mild>0?'轻微偏差，可免拆清洗观察':'均衡良好');
  var cls = bad>0 ? (Math.abs(maxDev)>=2*tol?'bad':'warn') : (mild>0?'warn':'ok');

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">平均喷油量</div><div class="result-value">'+fmtNum(mean,2)+' mL</div></div>'
    +'<div class="result-item"><div class="result-label">最大偏差</div><div class="result-value">'+(maxDev>0?'+':'')+fmtNum(maxDev,2)+' %（'+(maxI+1)+' 缸）</div></div>'
    +'<div class="result-item"><div class="result-label">标准差 (n−1)</div><div class="result-value">'+fmtNum(sd,3)+' mL</div></div>'
    +'<div class="result-item"><div class="result-label">离散系数 CV</div><div class="result-value">'+fmtNum(cv,2)+' %</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>相对标准值</h4><p>'+(std>0?(mean>std?'+':'')+fmtNum((mean-std)/std*100,2):'—')+' %</p><p>标准 '+fmtNum(std,1)+' mL</p></div>'
    +'<div class="dist-card"><h4>超差缸数</h4><p>'+bad+' / '+n+' 缸</p><p>容差 ±'+fmtNum(tol,0)+'%</p></div>'
    +'<div class="dist-card"><h4>最大与最小</h4><p>'+fmtNum(Math.max.apply(null,c),2)+' / '+fmtNum(Math.min.apply(null,c),2)+' mL</p><p>极差 '+fmtNum(Math.max.apply(null,c)-Math.min.apply(null,c),2)+' mL</p></div>'
    +'<div class="dist-card"><h4>均衡判定</h4><p style="font-size:12px;">'+verdict+'</p><p>'+fmtNum(dur,0)+' s × '+fmtNum(rep,0)+' 次</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<n;i++){
    var dv=dev[i], st,col;
    if(Math.abs(dv)>tol){ st='超差'; col='#dc2626'; }
    else if(Math.abs(dv)>3){ st='轻微偏差'; col='#d97706'; }
    else { st='正常'; col='#059669'; }
    var flow=dur>0?c[i]/(dur/60):0;
    rows+='<tr><td style="padding:5px 8px;">'+(i+1)+' 缸</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(c[i],2)+'</td>'
      +'<td style="padding:5px 8px;">'+(dv>0?'+':'')+fmtNum(dv,2)+' %</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(flow,2)+'</td>'
      +'<td style="padding:5px 8px;color:'+col+';">'+st+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">平均喷油量 = Σ 各缸喷油量 ÷ 缸数</div>'
    +'<div class="formula-line">各缸偏差率 = (该缸喷油量 − 平均喷油量) ÷ 平均喷油量 × 100%</div>'
    +'<div class="formula-line">样本标准差 s = √[Σ(xᵢ − x̄)² ÷ (n − 1)]；离散系数 CV = s ÷ x̄ × 100%</div>'
    +'<div class="formula-line">折算流量 = 喷油量 ÷ (测量时长 ÷ 60)，单位 mL/min</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">气缸</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">喷油量 (mL)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">偏差</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">折算流量 (mL/min)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>';

  var ad='';
  if(bad>0) ad+='<div class="tip-bad">⛔ '+(maxI+1)+' 缸偏差 '+fmtNum(maxDev,2)+'%，超出 ±'+fmtNum(tol,0)+'% 容差，判定「'+verdict+'」。清洗后须按同一时长复测，确认偏差回落至容差内。</div>';
  else if(mild>0) ad+='<div class="tip-warn">⚠️ 各缸均在容差内但存在 3% 以上偏差，离散系数 '+fmtNum(cv,2)+'%，可先做免拆清洗并观察怠速抖动与失火计数。</div>';
  else ad+='<div class="tip-info">✅ 四缸喷油量均衡（最大偏差 '+fmtNum(maxDev,2)+'%，离散系数 '+fmtNum(cv,2)+'%），无明显堵塞迹象。</div>';
  if(cv>5) ad+='<div class="tip-warn">📊 离散系数 '+fmtNum(cv,2)+'% 偏大，说明缸间一致性较差，建议结合故障码与失火计数进一步确认。</div>';
  if(dur<30) ad+='<div class="tip-info">⏱️ 测量时长仅 '+fmtNum(dur,0)+' s，短时长测量误差占比偏高，建议延长至 60 s 以上再比较。</div>';
  if(rep>1) ad+='<div class="tip-info">🔁 已按 '+fmtNum(rep,0)+' 次重复测试，建议取多次均值后再比较以降低随机误差。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='scheduler-cycle-maintenance', title='车辆保养项目周期排程表', icon='🔧', accent='#0369a1',
         desc='输入当前里程，自动生成到期/超期/即将保养清单，支持记录完成与历史日志',
         inputs=SC_INPUTS, cards=SC_CARDS,
         notes='各项目按「基准周期 × 工况系数」的整倍数滚动排程，实际以随车保养手册为准；记录仅存本机浏览器',
         js=SC_JS),
    dict(slug='shipping-cost-compare', title='快递运费比价器', icon='💰', accent='#b45309',
         desc='快递运费比价器，输入重量与配送区域对比主流快递公司运费，辅助寄件选择性价比渠道。',
         inputs=SH_INPUTS, cards=SH_CARDS,
         notes='表内资费为公开常见口径示例，实际报价随协议与网点浮动，可用自定义单价填入实际报价后再比',
         js=SH_JS),
    dict(slug='speed-tire', title='轮胎规格选择计算', icon='🚗', accent='#0f766e',
         desc='输入断面宽度、扁平比、轮辋直径，计算轮胎直径、周长、每公里转数，并推荐速度等级。',
         inputs=ST_INPUTS, cards=ST_CARDS,
         notes='直径偏差建议控制在 ±3% 以内；改装后速度表与里程表会按周长比例产生固定误差',
         js=ST_JS),
    dict(slug='tester-10', title='喷油嘴（清洗/均衡）测试', icon='🚙', accent='#4b5563',
         desc='喷油嘴在线测试工具，输入各缸喷油量数据评估清洗均衡效果，计算平均喷油量与偏差，辅助发动机维修诊断，纯前端。',
         inputs=T10_INPUTS, cards=T10_CARDS,
         notes='各缸数据须在同一喷油压力、脉宽与时长下测得才有可比性；清洗后按同一时长复测',
         js=T10_JS),
]


def main():
    ok = 0
    total = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        total += 1
        good, msg = L.rebuild(slug, **t)
        print('%-28s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch11: %d/%d ----' % (ok, total))


if __name__ == '__main__':
    main()
