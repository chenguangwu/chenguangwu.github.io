#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 5（wear-tire / lifespan-brake / resistance-1 / current-3 / temp-pressure-1）。

wear-tire 轮胎磨损速率与剩余寿命；lifespan-brake 刹车片剩余寿命；resistance-1 车载电路
电流/线径/压降选型；current-3 起动机功率与效率；temp-pressure-1 胎压随温度变化。
算例均按各页 deep-dive 示例口径实现并经 node 实跑复核。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ---------------------------------------------------------------- wear-tire
WT_INPUTS = '''    <div class="input-row">
      <div><label>新胎花纹深度 (mm)</label><input type="number" id="newD" value="8" oninput="calc()" min="0.1" step="0.1"></div>
      <div><label>当前花纹深度 (mm)</label><input type="number" id="curD" value="6" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>已行驶里程 (万 km)</label><input type="number" id="km" value="2" oninput="calc()" min="0" step="0.1"></div>
      <div><label>更换极限深度 (mm)</label><input type="number" id="minD" value="3" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>年均行驶里程 (万 km)</label><input type="number" id="kmY" value="1.5" oninput="calc()" min="0" step="0.1"></div>
      <div><label>轮胎数量（成本核算）</label><input type="number" id="cnt" value="4" oninput="calc()" min="1" step="1"></div>
    </div>'''

WT_CARDS = '''  <div class="card">
    <h3>📖 花纹深度与磨损参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">花纹深度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议</th>
      </tr>
      <tr><td style="padding:6px 8px;">8 mm（新胎）</td><td style="padding:6px 8px;">全新</td><td style="padding:6px 8px;">正常使用</td></tr>
      <tr><td style="padding:6px 8px;">5 ~ 7 mm</td><td style="padding:6px 8px;">良好</td><td style="padding:6px 8px;">关注磨损均匀性</td></tr>
      <tr><td style="padding:6px 8px;">3 ~ 4 mm</td><td style="padding:6px 8px;">注意</td><td style="padding:6px 8px;">湿地性能下降，规划更换</td></tr>
      <tr><td style="padding:6px 8px;">1.6 mm（法定极限）</td><td style="padding:6px 8px;">危险</td><td style="padding:6px 8px;">必须更换</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔁 定期换位</h4>
      <p>驱动轴与前轴磨损更快。建议每 1 万 km 前后交叉换位，可显著均衡四轮磨损、延长整组寿命。</p>
    </div>
    <div class="scene-card">
      <h4>📉 速率突变要查因</h4>
      <p>某侧磨损明显偏快，多因胎压长期偏低、四轮定位失准（外倾/前束）或驾驶激进，先补气与做定位再评估换胎。</p>
    </div>
    <div class="info-box">💡 磨损速率按「已磨深度 ÷ 已行驶里程」实测推算，比按年限估算可靠；但驾驶习惯变化会改变后续速率。</div>
  </div>'''

WT_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var nw=val('newD'),cu=val('curD'),km=val('km'),mn=val('minD');
  var kmY=val('kmY'),cnt=Math.round(val('cnt'));
  if(isNaN(nw)||isNaN(cu)||isNaN(km)||isNaN(mn)||nw<=0||nw<=mn||km<=0||cu<0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效深度与里程（新胎深度须大于极限）</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var worn=nw-cu;
  if(worn<0){ worn=0; }
  var rate=worn/km;
  var left=cu-mn;
  var pct=(nw-mn)>0?worn/(nw-mn)*100:0;
  var remainWanKm=(rate>0&&left>0)?left/rate:null;
  var years=(remainWanKm!=null&&kmY>0)?remainWanKm/kmY:null;
  var perK=rate/10;
  R.innerHTML='<div class="safe-val">磨损速率 '+fmtNum(perK,3)+' mm/千km</div>'+
    '<div class="safe-sub">剩余可磨 '+fmtNum(left,1)+' mm'+(remainWanKm!=null?' · 预计还可跑 '+fmtNum(remainWanKm,1)+' 万 km':'')+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(perK,3)+'</div><div class="l">磨损速率 (mm/千km)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(worn,1)+'</div><div class="l">已磨深度 (mm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(pct,0)+'%</div><div class="l">磨损占比</div></div>'+
    '<div class="dist-card"><div class="v">'+(remainWanKm!=null?fmtNum(remainWanKm,1):'--')+'</div><div class="l">剩余里程 (万 km)</div></div>'+
    '<div class="dist-card"><div class="v">'+(years!=null?fmtNum(years,1):'--')+'</div><div class="l">剩余年数 (年)</div></div>'+
    '<div class="dist-card"><div class="v">'+(cnt>0?cnt:0)+'</div><div class="l">整组需换条数</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">磨损速率 =（新胎深度 − 当前深度）÷ 已行驶里程</div>'+
    '<div class="fb-row">剩余可磨量 = 当前深度 − 更换极限深度</div>'+
    '<div class="fb-row">剩余里程 = 剩余可磨量 ÷ 磨损速率</div>'+
    '<div class="fb-row">剩余年数 = 剩余里程 ÷ 年均行驶里程</div>'+
    '<div class="fb-row">本次：'+fmtNum(nw,1)+' → '+fmtNum(cu,1)+' mm，'+fmtNum(km,1)+' 万 km 磨掉 '+fmtNum(worn,1)+' mm</div>';
  var ad='';
  if(left<=0){ ad='<div class="tip-warn">⚠️ 当前花纹已达/低于更换极限 '+fmtNum(mn,1)+' mm，必须立即更换，湿地制动距离会急剧变长。</div>'; }
  else if(cu<=1.6){ ad='<div class="tip-warn">⚠️ 当前花纹 '+fmtNum(cu,1)+' mm 已低于常见法定极限 1.6mm，禁止继续使用。</div>'; }
  else if(left<=1){ ad='<div class="tip-info">ℹ️ 剩余仅 '+fmtNum(left,1)+' mm，建议尽快安排换胎并检查四轮定位。</div>'; }
  else{ ad='<div class="tip-success">✅ 剩余可磨 '+fmtNum(left,1)+' mm，按当前速率还可行驶约 '+fmtNum(remainWanKm,1)+' 万 km。</div>'; }
  ad+='<div class="tip-info">ℹ️ 建议每 1 万 km 做一次换位并复测四轮深度，单侧明显偏快时优先检查胎压与四轮定位。</div>';
  A.innerHTML=ad;
}
calc();'''

# ------------------------------------------------------------ lifespan-brake
LB_INPUTS = '''    <div class="input-row">
      <div><label>刹车片新品厚度 (mm)</label><input type="number" id="newT" value="12" oninput="calc()" min="0.1" step="0.1"></div>
      <div><label>当前剩余厚度 (mm)</label><input type="number" id="curT" value="6" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>月均磨损量 (mm/月)</label><input type="number" id="rateM" value="0.5" oninput="calc()" min="0.01" step="0.01"></div>
      <div><label>更换极限厚度 (mm)</label><input type="number" id="minT" value="2" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>用车工况</label><select id="cond" onchange="calc()">
        <option value="1.0" selected>城市日常</option>
        <option value="0.8">高速长途为主</option>
        <option value="1.3">山路 / 频繁制动</option>
        <option value="1.6">营运重载</option>
      </select></div>
      <div><label>月均行驶里程 (km)</label><input type="number" id="kmM" value="1200" oninput="calc()" min="1" step="any"></div>
    </div>'''

LB_CARDS = '''  <div class="card">
    <h3>📖 刹车片厚度与更换参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余厚度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议</th>
      </tr>
      <tr><td style="padding:6px 8px;">≥ 6 mm</td><td style="padding:6px 8px;">良好</td><td style="padding:6px 8px;">正常使用，定期复测</td></tr>
      <tr><td style="padding:6px 8px;">4 ~ 6 mm</td><td style="padding:6px 8px;">中等</td><td style="padding:6px 8px;">列入下次保养更换计划</td></tr>
      <tr><td style="padding:6px 8px;">2 ~ 4 mm</td><td style="padding:6px 8px;">接近极限</td><td style="padding:6px 8px;">尽快更换，避免伤盘</td></tr>
      <tr><td style="padding:6px 8px;">&lt; 2 mm</td><td style="padding:6px 8px;">危险</td><td style="padding:6px 8px;">立即更换，金属背板会刮伤刹车盘</td></tr>
    </table>
    <div class="scene-card">
      <h4>📏 厚度比里程更可靠</h4>
      <p>厚度是直接测量值，里程只是间接推算。每次保养量四轮厚度，任一轮达极限即换，不必等四轮同时到限。</p>
    </div>
    <div class="scene-card">
      <h4>🔊 磨损报警信号</h4>
      <p>多数刹车片带金属报警片，磨损到限会发出尖锐异响；电子报警车型则点亮仪表提示。出现异响应尽快检查。</p>
    </div>
    <div class="info-box">💡 前轮承担约 60%~70% 制动力，磨损通常快于后轮，更换周期不宜按同一条线判断。</div>
  </div>'''

LB_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var nw=val('newT'),cu=val('curT'),rateM=val('rateM'),mn=val('minT');
  var cond=parseFloat(str('cond')),kmM=val('kmM');
  if(isNaN(nw)||isNaN(cu)||isNaN(rateM)||isNaN(mn)||nw<=0||rateM<=0||nw<=mn||cu<0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效厚度与月均磨损量</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var effRate=rateM*(cond>0?cond:1);
  var left=cu-mn;
  var months=(effRate>0)?(left/effRate):0;
  var wornPct=(nw-mn)>0?(nw-cu)/(nw-mn)*100:0;
  var kmLeft=months*kmM;
  var yearN=months/12;
  R.innerHTML='<div class="safe-val">剩余寿命约 '+fmtNum(months,1)+' 个月</div>'+
    '<div class="safe-sub">剩余可用厚度 '+fmtNum(left,1)+' mm（工况系数 '+fmtNum(cond,1)+'）</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(months,1)+'</div><div class="l">剩余寿命 (月)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(left,1)+'</div><div class="l">剩余可用厚度 (mm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(effRate,2)+'</div><div class="l">修正后月磨损 (mm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(wornPct,0)+'%</div><div class="l">已磨损占比</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(kmLeft,0)+'</div><div class="l">剩余里程 (km)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(yearN,1)+'</div><div class="l">剩余年限 (年)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">剩余可用厚度 = 当前厚度 − 更换极限厚度</div>'+
    '<div class="fb-row">剩余寿命（月）= 剩余可用厚度 ÷ 月均磨损量</div>'+
    '<div class="fb-row">工况修正：高速 ×0.8 / 城市 ×1.0 / 山路 ×1.3 / 营运重载 ×1.6</div>'+
    '<div class="fb-row">剩余里程 = 剩余寿命（月）× 月均行驶里程</div>'+
    '<div class="fb-row">本次：'+fmtNum(cu,1)+' mm → 极限 '+fmtNum(mn,1)+' mm，按 '+fmtNum(effRate,2)+' mm/月 计</div>';
  var ad='';
  if(cu<=mn){ ad='<div class="tip-warn">⚠️ 当前厚度 '+fmtNum(cu,1)+' mm 已达或低于更换极限 '+fmtNum(mn,1)+' mm，必须立即更换。</div>'; }
  else if(months<=3){ ad='<div class="tip-warn">⚠️ 剩余寿命仅约 '+fmtNum(months,1)+' 个月，建议尽快安排更换，避免金属背板刮伤刹车盘。</div>'; }
  else if(months<=8){ ad='<div class="tip-info">ℹ️ 剩余约 '+fmtNum(months,1)+' 个月，可列入下次保养计划。</div>'; }
  else{ ad='<div class="tip-success">✅ 剩余约 '+fmtNum(months,1)+' 个月（'+fmtNum(kmLeft,0)+' km），正常使用并定期复测即可。</div>'; }
  if(cond>=1.3){ ad+='<div class="tip-info">ℹ️ 当前按严苛工况修正（×'+fmtNum(cond,1)+'），实际磨损受驾驶习惯与载重影响较大。</div>'; }
  A.innerHTML=ad;
}
calc();'''

# ------------------------------------------------------------- resistance-1
RS_INPUTS = '''    <div class="input-row">
      <div><label>系统电压 (V)</label><input type="number" id="volt" value="12" oninput="calc()" min="1" step="0.1"></div>
      <div><label>用电器功率 (W)</label><input type="number" id="pow" value="120" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>线路长度 (m，单程)</label><input type="number" id="len" value="5" oninput="calc()" min="0" step="0.1"></div>
      <div><label>选用线径 (mm²)</label><input type="number" id="area" value="2.5" oninput="calc()" min="0.1" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>导线材质</label><select id="mat" onchange="calc()">
        <option value="0.0175" selected>铜（ρ=0.0175）</option>
        <option value="0.0282">铝（ρ=0.0282）</option>
      </select></div>
      <div><label>允许压降比例 (%)</label><input type="number" id="tol" value="3" oninput="calc()" min="1" max="20" step="0.5"></div>
    </div>'''

RS_CARDS = '''  <div class="card">
    <h3>📖 线径载流量与保险丝选型</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">线径 (mm²)</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">参考载流 (A)</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议保险丝 (A)</th>
      </tr>
      <tr><td style="padding:6px 8px;">0.75</td><td style="padding:6px 8px;">6 ~ 8</td><td style="padding:6px 8px;">5</td></tr>
      <tr><td style="padding:6px 8px;">1.0</td><td style="padding:6px 8px;">8 ~ 11</td><td style="padding:6px 8px;">10</td></tr>
      <tr><td style="padding:6px 8px;">1.5</td><td style="padding:6px 8px;">12 ~ 15</td><td style="padding:6px 8px;">15</td></tr>
      <tr><td style="padding:6px 8px;">2.5</td><td style="padding:6px 8px;">16 ~ 20</td><td style="padding:6px 8px;">20</td></tr>
      <tr><td style="padding:6px 8px;">4.0</td><td style="padding:6px 8px;">25 ~ 32</td><td style="padding:6px 8px;">30</td></tr>
    </table>
    <div class="scene-card">
      <h4>⚡ 压降才是关键</h4>
      <p>低电压大电流场景下，线路电阻造成的压降常比载流量更早成为瓶颈。压降 = 电流 × 线路电阻，双线回路长度需按往返计。</p>
    </div>
    <div class="scene-card">
      <h4>🧯 保险丝双原则</h4>
      <p>保险丝额定电流应「略高于工作电流、明显低于线径载流量」，才能既保证正常用电又在线路短路时及时熔断防起火。</p>
    </div>
    <div class="info-box">💡 搭铁回路与插接件氧化同样会产生附加电阻。灯光变暗时优先检查搭铁点与接头，而非直接换大功率灯泡。</div>
  </div>'''

RS_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var volt=val('volt'),pow=val('pow'),len=val('len'),area=val('area');
  var rho=parseFloat(str('mat')),tol=val('tol');
  if(isNaN(volt)||isNaN(pow)||volt<=0||pow<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的电压与功率</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var cur=pow/volt;
  var res=(area>0)?rho*(2*(len>0?len:0))/area:0;
  var drop=cur*res;
  var endV=volt-drop;
  var dropPct=(volt>0)?drop/volt*100:0;
  var minArea=(area>0)?area*Math.ceil((dropPct/(tol>0?tol:1))*10)/10:0;
  var recArea=(rho*(2*(len>0?len:0))*cur/(volt*(tol>0?tol:100)))*100;
  var tbl=[{a:0.75,i:8},{a:1.0,i:11},{a:1.5,i:15},{a:2.5,i:20},{a:4.0,i:32},{a:6.0,i:44}];
  var need=tbl[5].a, fuse=tbl[5].i;
  for(var k=0;k<tbl.length;k++){ if(cur<=tbl[k].i){ need=tbl[k].a; fuse=tbl[k].i; break; } }
  var recFuse=Math.ceil(cur/5)*5;
  R.innerHTML='<div class="safe-val">工作电流 '+fmtNum(cur,2)+' A</div>'+
    '<div class="safe-sub">压降 '+fmtNum(drop,2)+' V（'+fmtNum(dropPct,1)+'%）· 末端电压 '+fmtNum(endV,2)+' V</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(cur,2)+'</div><div class="l">工作电流 (A)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(res,4)+'</div><div class="l">线路电阻 (Ω)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(drop,2)+'</div><div class="l">线路压降 (V)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(dropPct,1)+'%</div><div class="l">压降比例</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(need,2)+'</div><div class="l">建议最小线径 (mm²)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(fuse,0)+'</div><div class="l">建议保险丝 (A)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">工作电流 I = 功率 P ÷ 系统电压 U</div>'+
    '<div class="fb-row">线路电阻 R = ρ × 2L ÷ A（双线回路，L 为单程长度）</div>'+
    '<div class="fb-row">线路压降 ΔU = I × R；末端电压 = U − ΔU</div>'+
    '<div class="fb-row">压降比例 = ΔU ÷ U（工程建议控制在 '+fmtNum(tol,1)+'% 以内）</div>'+
    '<div class="fb-row">本次：'+fmtNum(cur,1)+' A × '+fmtNum(res,4)+' Ω = '+fmtNum(drop,2)+' V</div>';
  var ad='';
  if(dropPct>tol){ ad='<div class="tip-warn">⚠️ 压降达 '+fmtNum(dropPct,1)+'%，超过设定上限 '+fmtNum(tol,1)+'%。建议加粗线径至约 '+fmtNum(Math.ceil(recArea*2)/2,1)+' mm² 以上，或缩短走线、就近取电。</div>'; }
  else{ ad='<div class="tip-success">✅ 压降 '+fmtNum(dropPct,1)+'%，在设定上限 '+fmtNum(tol,1)+'% 之内，末端设备可正常工作。</div>'; }
  if(cur>tbl[tbl.length-1].i){ ad+='<div class="tip-warn">⚠️ 电流 '+fmtNum(cur,1)+' A 超出常见车载线径载流量，需选用 '+fmtNum(cur/8+1,1)+' mm² 以上线径并单独走线。</div>'; }
  ad+='<div class="tip-info">ℹ️ 保险丝建议 '+fmtNum(recFuse,0)+' A（略高于工作电流），且明显低于所选线径的载流量。</div>';
  A.innerHTML=ad;
}
calc();'''

# ---------------------------------------------------------------- current-3
CU_INPUTS = '''    <div class="input-row">
      <div><label>电池端电压 (V)</label><input type="number" id="volt" value="11.5" oninput="calc()" min="1" step="0.1"></div>
      <div><label>启动电流 (A)</label><input type="number" id="cur" value="180" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>输出机械功率 (W)</label><input type="number" id="pout" value="1500" oninput="calc()" min="0" step="any"></div>
      <div><label>曲轴转速 (rpm)</label><input type="number" id="rpm" value="200" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>输出扭矩 (N·m，可留空自动反推)</label><input type="number" id="tq" value="" oninput="calc()" min="0" step="any"></div>
      <div><label>健康效率参考下限 (%)</label><input type="number" id="ref" value="50" oninput="calc()" min="1" max="100" step="1"></div>
    </div>'''

CU_CARDS = '''  <div class="card">
    <h3>📖 起动机效率与故障判读</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">现象</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">可能原因</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">排查顺序</th>
      </tr>
      <tr><td style="padding:6px 8px;">启动无力、电流偏大</td><td style="padding:6px 8px;">起动机内部磨损 / 回路电阻升高</td><td style="padding:6px 8px;">先测电压与线缆压降，再拆检起动机</td></tr>
      <tr><td style="padding:6px 8px;">启动瞬间电压跌破 9V</td><td style="padding:6px 8px;">电瓶亏电 / 桩头氧化 / 内阻增大</td><td style="padding:6px 8px;">清洁桩头 → 测内阻 → 必要时换电瓶</td></tr>
      <tr><td style="padding:6px 8px;">效率长期低于 50%</td><td style="padding:6px 8px;">电枢、碳刷磨损或机械卡滞</td><td style="padding:6px 8px;">检修或更换起动机总成</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔋 冷启动为何电流大</h4>
      <p>冷态机油黏度高、机械阻力大，起动机需输出更大扭矩，电流随之升高、效率下降，属正常现象。</p>
    </div>
    <div class="scene-card">
      <h4>📉 内阻与电瓶健康</h4>
      <p>电瓶内阻随老化上升，启动瞬间端电压跌落更明显。以内阻与冷启动电流（CCA）评估健康度比看电压更可靠。</p>
    </div>
    <div class="info-box">💡 起动机效率为「输出机械功率 ÷ 输入电功率」，直流起动机典型值约 60%~75%，其余转化为铜损与铁损发热。</div>
  </div>'''

CU_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var volt=val('volt'),cur=val('cur'),pout=val('pout'),rpm=val('rpm');
  var tqIn=parseFloat(document.getElementById('tq').value),ref=val('ref');
  if(isNaN(volt)||isNaN(cur)||isNaN(pout)||volt<=0||cur<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的电压、电流与输出功率</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var pin=volt*cur;
  var eff=(pin>0)?pout/pin*100:0;
  var loss=pin-pout;
  var res=volt/cur;
  var tq=(!isNaN(tqIn)&&tqIn>0)?tqIn:((rpm>0)?pout*9550/rpm:0);
  R.innerHTML='<div class="safe-val">效率 '+fmtNum(eff,1)+'%</div>'+
    '<div class="safe-sub">输入电功率 '+fmtNum(pin,0)+' W · 热损耗 '+fmtNum(loss,0)+' W</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(pin,0)+'</div><div class="l">输入电功率 (W)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(pout,0)+'</div><div class="l">输出机械功率 (W)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(eff,1)+'%</div><div class="l">起动机效率</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(loss,0)+'</div><div class="l">发热损耗 (W)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(res,4)+'</div><div class="l">等效回路电阻 (Ω)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(tq,2)+'</div><div class="l">输出扭矩 (N·m)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">输入电功率 Pin = 端电压 U × 启动电流 I</div>'+
    '<div class="fb-row">起动机效率 η = 输出机械功率 Pout ÷ 输入电功率 Pin</div>'+
    '<div class="fb-row">发热损耗 = Pin − Pout（铜损 + 铁损 + 机械损耗）</div>'+
    '<div class="fb-row">等效回路电阻 R = U ÷ I；由转速反推扭矩 T = 9550 × Pout ÷ n</div>'+
    '<div class="fb-row">本次：'+fmtNum(volt,1)+' V × '+fmtNum(cur,0)+' A = '+fmtNum(pin,0)+' W，效率 '+fmtNum(eff,1)+'%</div>';
  var ad='';
  if(eff<ref){ ad='<div class="tip-warn">⚠️ 效率 '+fmtNum(eff,1)+'% 低于健康下限 '+fmtNum(ref,0)+'%：优先排查电瓶端电压与线缆压降，再检查电枢、碳刷磨损与机械卡滞。</div>'; }
  else if(eff>85){ ad='<div class="tip-warn">⚠️ 效率 '+fmtNum(eff,1)+'% 明显高于直流起动机典型区间（60%~75%），请核对输出功率与电流是否为同一工况所测。</div>'; }
  else{ ad='<div class="tip-success">✅ 效率 '+fmtNum(eff,1)+'% 处于直流起动机典型区间（60%~75%），供电链路与起动机状态正常。</div>'; }
  ad+='<div class="tip-info">ℹ️ 启动瞬间端电压跌破 9V 且带不动，多为电瓶亏电、桩头氧化或起动机卡滞；冷启动电流偏大、效率略低属正常。</div>';
  A.innerHTML=ad;
}
calc();'''

# ----------------------------------------------------------- temp-pressure-1
TP_INPUTS = '''    <div class="input-row">
      <div><label>冷胎充气压力 (bar)</label><input type="number" id="p1" value="2.4" oninput="calc()" min="0.1" step="0.01"></div>
      <div><label>充气时温度 (℃)</label><input type="number" id="t1" value="25" oninput="calc()" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>行驶后胎温 (℃)</label><input type="number" id="t2" value="55" oninput="calc()" step="0.5"></div>
      <div><label>车辆标准胎压 (bar)</label><input type="number" id="std" value="2.4" oninput="calc()" min="0.1" step="0.01"></div>
    </div>
    <div class="input-row">
      <div><label>季节场景</label><select id="season" onchange="calc()">
        <option value="normal" selected>常温</option>
        <option value="winter">冬季（气温低于 0℃）</option>
        <option value="summer">夏季高温</option>
      </select></div>
      <div><label>环境温度 (℃)</label><input type="number" id="amb" value="25" oninput="calc()" step="0.5"></div>
    </div>'''

TP_CARDS = '''  <div class="card">
    <h3>📖 温度对胎压的影响</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">温升 (℃)</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">胎压增幅 (2.4bar 基准)</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">+10</td><td style="padding:6px 8px;">约 +0.07 ~ 0.08 bar</td><td style="padding:6px 8px;">市区行驶常见</td></tr>
      <tr><td style="padding:6px 8px;">+20</td><td style="padding:6px 8px;">约 +0.15 ~ 0.17 bar</td><td style="padding:6px 8px;">持续行驶</td></tr>
      <tr><td style="padding:6px 8px;">+30</td><td style="padding:6px 8px;">约 +0.22 ~ 0.26 bar</td><td style="padding:6px 8px;">高速长途</td></tr>
      <tr><td style="padding:6px 8px;">−20</td><td style="padding:6px 8px;">约 −0.15 ~ 0.17 bar</td><td style="padding:6px 8px;">冬季停放，需补气</td></tr>
    </table>
    <div class="scene-card">
      <h4>❄️ 冬天胎压报警</h4>
      <p>气温每下降约 10℃，胎压降低约 0.07~0.1 bar。冬季报警多为正常冷缩，补到标准值即可；若补气后仍频繁报警，查慢漏或传感器。</p>
    </div>
    <div class="scene-card">
      <h4>🚫 热胎别放气</h4>
      <p>行驶后胎压虚高属正常，此时放气会导致冷却后胎压不足。标准值均指冷胎，应按冷胎读数调整。</p>
    </div>
    <div class="info-box">💡 本工具按「表压 × 绝对温度比」工程近似计算，与行业经验值「每升 10℃ 增 0.07~0.1bar」一致。</div>
  </div>'''

TP_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var p1=val('p1'),t1=val('t1'),t2=val('t2'),std=val('std');
  var season=str('season'),amb=val('amb');
  if(isNaN(p1)||isNaN(t1)||isNaN(t2)||p1<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的压力与温度</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var k1=t1+273.15, k2=t2+273.15;
  var p2=p1*k2/k1;
  var delta=p2-p1;
  var per10=delta/((t2-t1)/10);
  var devStd=0;
  if(!isNaN(amb)&&!isNaN(std)&&std>0){
    var pAmb=p1*((amb+273.15)/k1);
    devStd=pAmb-std;
  }
  R.innerHTML='<div class="safe-val">热态胎压约 '+fmtNum(p2,2)+' bar</div>'+
    '<div class="safe-sub">增幅 '+(delta>=0?'+':'')+fmtNum(delta,2)+' bar · 每 10℃ 约 '+fmtNum(per10,2)+' bar</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(p1,2)+'</div><div class="l">冷胎压力 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(p2,2)+'</div><div class="l">热态压力 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+(delta>=0?'+':'')+fmtNum(delta,2)+'</div><div class="l">压力变化 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(per10,3)+'</div><div class="l">每 10℃ 变化 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(t2-t1,1)+'</div><div class="l">温升 (℃)</div></div>'+
    '<div class="dist-card"><div class="v">'+(isNaN(devStd)?'--':(devStd>=0?'+':'')+fmtNum(devStd,2))+'</div><div class="l">相对标准偏差 (bar)</div></div>';
  F.innerHTML=
    '<div class="fb-title">计算口径</div>'+
    '<div class="fb-row">压力比 = 绝对温度比：P₂ = P₁ ×（T₂ + 273.15）÷（T₁ + 273.15）</div>'+
    '<div class="fb-row">每 10℃ 变化 ≈ 冷胎压力 × 10 ÷ 绝对温度 × 压力</div>'+
    '<div class="fb-row">环境温度换算：P（环境）= P₁ ×（T环境 + 273.15）÷（T₁ + 273.15）</div>'+
    '<div class="fb-row">经验校核：每升 10℃ 胎压增约 0.07~0.1 bar（本例 '+fmtNum(per10,3)+' bar）</div>';
  var ad='';
  if(Math.abs(per10)>0.15){ ad='<div class="tip-warn">⚠️ 每 10℃ 变化 '+fmtNum(per10,3)+' bar 偏离经验区间（0.07~0.10），请核对输入温度是否为同一状态下的读数。</div>'; }
  else{ ad='<div class="tip-success">✅ 每 10℃ 变化 '+fmtNum(per10,3)+' bar，与行业经验值（0.07~0.10）一致。</div>'; }
  ad+='<div class="tip-info">ℹ️ 热态读数偏高属正常，标准胎压指冷胎值（停车 3 小时以上或行驶不足 2km），切勿按热胎读数放气。</div>';
  if(season==='winter'){ ad+='<div class="tip-warn">⚠️ 冬季气温低，冷胎压力会自然下降约 '+(isNaN(devStd)?'0.1~0.2':fmtNum(Math.abs(devStd),2))+' bar，请及时补到标准值。</div>'; }
  else if(season==='summer'){ ad+='<div class="tip-info">ℹ️ 夏季高温长途行驶胎压升幅明显，冷胎按标准下限充气更稳妥，无需提前放气。</div>'; }
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='wear-tire', title='轮胎磨损速率测算', icon='🔘', accent='#4b5563',
         desc='按新胎与当前花纹深度、已行驶里程计算磨损速率，预估剩余寿命与换胎时点。',
         inputs=WT_INPUTS, cards=WT_CARDS,
         notes='磨损速率按实测推算，驾驶习惯与路况变化会影响后续实际速率',
         js=WT_JS),
    dict(slug='lifespan-brake', title='刹车片剩余寿命计算', icon='⏳', accent='#b91c1c',
         desc='由刹车片新品厚度、当前厚度与月均磨损量计算剩余可用厚度与使用寿命，支持工况修正。',
         inputs=LB_INPUTS, cards=LB_CARDS,
         notes='厚度为直接测量值最可靠，里程推算仅供趋势参考，任一轮到限即应更换',
         js=LB_JS),
    dict(slug='resistance-1', title='车载电路电阻与电流计算', icon='⚡', accent='#b45309',
         desc='按用电器功率与系统电压计算工作电流，核算线路压降并给出线径与保险丝选型建议。',
         inputs=RS_INPUTS, cards=RS_CARDS,
         notes='压降按双线回路计算，搭铁点与插接件氧化会产生附加电阻',
         js=RS_JS),
    dict(slug='current-3', title='起动机电流效率计算', icon='🔌', accent='#0f766e',
         desc='由电池端电压、启动电流与输出机械功率计算起动机效率与发热损耗，辅助启动无力诊断。',
         inputs=CU_INPUTS, cards=CU_CARDS,
         notes='直流起动机典型效率约 60%~75%，冷启动电流偏大属正常现象',
         js=CU_JS),
    dict(slug='temp-pressure-1', title='胎压随温度变化计算', icon='🌡️', accent='#7c3aed',
         desc='按理想气体近似计算胎压随温度的变化，预判行驶温升与冬季冷缩对胎压的影响。',
         inputs=TP_INPUTS, cards=TP_CARDS,
         notes='标准胎压指冷胎读数，热胎测量值偏高属正常，不应按热胎读数放气',
         js=TP_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-18s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch5: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
