#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 8。

analysis-diagnosis 故障码/数据流诊断；bus-arrival-estimator 公交到站预估；
calc-4 拖车球头载荷；catalyst 催化器转化效率；cheshenkongqizulixishu 车身空气阻力。
标题与描述严格沿用页面原有 <title>/<desc> 口径；算例按各页 deep-dive 示例口径实现并经 node 复核。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ==================================================== analysis-diagnosis
AD_INPUTS = '''    <div class="input-row">
      <div><label>故障码 1</label><input type="text" id="code1" value="P0301" oninput="calc()" placeholder="如 P0301"></div>
      <div><label>故障码 2（可留空）</label><input type="text" id="code2" value="P0171" oninput="calc()" placeholder="如 P0420"></div>
    </div>
    <div class="input-row">
      <div><label>故障码 3（可留空）</label><input type="text" id="code3" value="" oninput="calc()" placeholder="如 U0100"></div>
      <div><label>故障码 4（可留空）</label><input type="text" id="code4" value="" oninput="calc()" placeholder="如 C0035"></div>
    </div>
    <div class="input-row">
      <div><label>冷却液温度 (℃)</label><input type="number" id="coolant" value="92" oninput="calc()" step="1"></div>
      <div><label>短期燃油修正 STFT (%)</label><input type="number" id="stft" value="18" oninput="calc()" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>怠速转速 (rpm)</label><input type="number" id="rpm" value="750" oninput="calc()" step="50"></div>
      <div><label>节气门开度 (%)</label><input type="number" id="tps" value="12" oninput="calc()" step="1"></div>
    </div>'''

AD_CARDS = '''  <div class="card">
    <h3>🔤 故障码结构解读</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">位序</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">含义</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">示例（P0301）</th>
      </tr>
      <tr><td style="padding:6px 8px;">第 1 位</td><td style="padding:6px 8px;">所属系统</td><td style="padding:6px 8px;">P 动力总成</td></tr>
      <tr><td style="padding:6px 8px;">第 2 位</td><td style="padding:6px 8px;">0=ISO 通用 / 1=厂家自定义</td><td style="padding:6px 8px;">0 通用定义</td></tr>
      <tr><td style="padding:6px 8px;">第 3 位</td><td style="padding:6px 8px;">故障子类</td><td style="padding:6px 8px;">3 点火缺火</td></tr>
      <tr><td style="padding:6px 8px;">第 4-5 位</td><td style="padding:6px 8px;">具体部件或缸号</td><td style="padding:6px 8px;">01 第 1 缸</td></tr>
    </table>
    <div class="scene-card">
      <h4>🧭 系统首字母</h4>
      <p>P 动力总成（发动机/变速箱）、C 底盘（制动/转向/悬架）、B 车身（门窗/空调/安全气囊）、U 网络通信（CAN 总线）。先按首字母定位系统，再读后三位定位部件。</p>
    </div>
    <div class="scene-card">
      <h4>📈 数据流参考区间</h4>
      <p>冷却液温度 85~100 ℃；短期燃油修正 −10%~+10%（正值偏稀、负值偏浓）；怠速 700~900 rpm；节气门怠速开度 0~15%。多参数交叉比单看一码更可靠。</p>
    </div>
    <div class="info-box">💡 故障码只提示「哪个系统异常」，不等于已锁定损坏部件。应先看数据流是否支持该判断，再做零件级测量。</div>
  </div>'''

AD_JS = H + '''
var CODES={
 'P0101':'空气流量计(MAF)范围/性能故障','P0102':'空气流量计信号过低','P0103':'空气流量计信号过高',
 'P0113':'进气温度传感器电路电压过高','P0117':'冷却液温度传感器电路电压过低','P0118':'冷却液温度传感器电路电压过高',
 'P0120':'节气门位置传感器电路故障','P0128':'冷却液温度低于节温器调节温度',
 'P0130':'上游氧传感器电路故障','P0133':'上游氧传感器响应过慢','P0135':'上游氧传感器加热电路故障',
 'P0136':'下游氧传感器电路故障','P0141':'下游氧传感器加热电路故障',
 'P0171':'系统过稀（第 1 组）','P0172':'系统过浓（第 1 组）','P0174':'系统过稀（第 2 组）','P0175':'系统过浓（第 2 组）',
 'P0300':'随机/多缸失火','P0301':'第 1 缸失火','P0302':'第 2 缸失火','P0303':'第 3 缸失火',
 'P0304':'第 4 缸失火','P0305':'第 5 缸失火','P0306':'第 6 缸失火',
 'P0335':'曲轴位置传感器电路故障','P0340':'凸轮轴位置传感器电路故障',
 'P0401':'EGR 流量不足','P0420':'催化器效率低于阈值（第 1 组）','P0430':'催化器效率低于阈值（第 2 组）',
 'P0440':'燃油蒸发系统(EVAP)故障','P0442':'EVAP 系统小泄漏','P0455':'EVAP 系统大泄漏',
 'P0500':'车速传感器故障','P0505':'怠速控制系统故障','P0507':'怠速转速高于预期',
 'P0700':'变速箱控制系统故障','P0701':'变速箱控制系统范围/性能',
 'U0100':'与发动机控制模块通信丢失','U0121':'与 ABS 控制模块通信丢失','U0155':'与仪表模块通信丢失',
 'C0035':'左前轮速传感器电路故障','C0040':'右前轮速传感器电路故障',
 'B0001':'安全气囊系统故障','B1000':'车身控制模块故障'
};
var SYS={P:'动力总成（发动机/变速箱）',C:'底盘（制动/转向/悬架）',B:'车身（门窗/空调/安全气囊）',U:'网络通信（CAN 总线）'};

function parseCode(raw){
  var c=(raw||'').toUpperCase().replace(/[^A-Z0-9]/g,'');
  if(c.length<5) return null;
  var sys=SYS[c[0]]||'未知系统';
  var sub={0:'燃油与空气计量',1:'燃油与空气计量',2:'燃油与空气计量',3:'点火系统/失火',4:'排放控制',
           5:'车速与怠速控制',6:'ECU 与输出电路',7:'变速箱',8:'变速箱'}[c[2]]||'其他子类';
  return {code:c, sys:sys, sub:sub, std:c[1]==='0'?'ISO 通用定义':'厂家自定义',
          desc:CODES[c]||'（未收录该码，请对照车型维修手册）'};
}

function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var raws=[str('code1'),str('code2'),str('code3'),str('code4')];
  var list=[],rows='',seen={};
  for(var i=0;i<raws.length;i++){
    if(!raws[i]||!raws[i].trim()) continue;
    var p=parseCode(raws[i]);
    if(!p||seen[p.code]) continue;
    seen[p.code]=1; list.push(p);
    rows+='<tr><td style="padding:5px 8px;font-family:monospace;">'+p.code+'</td>'
      +'<td style="padding:5px 8px;">'+p.sys+'</td>'
      +'<td style="padding:5px 8px;">'+p.sub+'</td>'
      +'<td style="padding:5px 8px;">'+p.desc+'</td></tr>';
  }
  var ct=val('coolant'),stft=val('stft'),rpm=val('rpm'),tps=val('tps');

  var coolTxt, coolCls;
  if(ct>=85&&ct<=100){coolTxt='正常';coolCls='ok';}
  else if(ct<85){coolTxt='偏低（节温器常开或水温传感器偏差）';coolCls='warn';}
  else {coolTxt='过高（散热系统异常）';coolCls='bad';}

  var ftTxt, ftCls;
  if(stft>10){ftTxt='偏稀（可能进气漏气、油压不足或喷油器堵塞）';ftCls='warn';}
  else if(stft<-10){ftTxt='偏浓（可能喷油器渗漏、油压过高或空气计量偏大）';ftCls='warn';}
  else {ftTxt='正常';ftCls='ok';}

  var idleTxt, idleCls;
  if(rpm>=700&&rpm<=900){idleTxt='正常';idleCls='ok';}
  else if(rpm<700){idleTxt='偏低（积碳、节气门脏污或真空泄漏）';idleCls='warn';}
  else {idleTxt='偏高（怠速控制阀或节气门匹配异常）';idleCls='warn';}

  // 综合排查优先级
  var sysSet={},hasMisfire=false,hasLean=false;
  for(var i=0;i<list.length;i++){
    sysSet[list[i].code[0]]=1;
    if(/^P03/.test(list[i].code)) hasMisfire=true;
    if(list[i].code==='P0171'||list[i].code==='P0174') hasLean=true;
  }
  var acts=[];
  if(hasMisfire) acts.push('失火码：优先做点火线圈对调、火花塞间隙与缸压检查，确认是否随缸位转移。');
  if(hasLean&&stft>10) acts.push('过稀码 + 燃油修正大幅偏正：优先查进气歧管与真空管路漏气、MAF 数据流是否偏低。');
  if(sysSet['U']) acts.push('通信码：检查 CAN 总线插接件、线束短路/断路与模块供电搭铁。');
  if(sysSet['C']) acts.push('底盘码：优先检查对应轮速传感器线束与齿圈，避免影响 ABS/ESP。');
  if(sysSet['B']) acts.push('车身码：检查对应模块供电、搭铁与开关回路。');
  if(!acts.length) acts.push('未见高优先级组合特征，建议按故障码顺序逐条读取冻结帧数据后再定位。');

  var sysKeys=Object.keys(sysSet);
  var sysTxt=sysKeys.length?sysKeys.join(' / '):'—';

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">已识别故障码</div><div class="result-value">'+list.length+' 条</div></div>'
    +'<div class="result-item"><div class="result-label">涉及系统</div><div class="result-value">'+sysTxt+'</div></div>'
    +'<div class="result-item"><div class="result-label">冷却液温度</div><div class="result-value">'+fmtNum(ct,0)+' ℃</div></div>'
    +'<div class="result-item"><div class="result-label">燃油修正</div><div class="result-value">'+(stft>0?'+':'')+fmtNum(stft,0)+' %</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>冷却液温度</h4><p style="font-size:12px;">'+coolTxt+'</p></div>'
    +'<div class="dist-card"><h4>短期燃油修正</h4><p style="font-size:12px;">'+ftTxt+'</p></div>'
    +'<div class="dist-card"><h4>怠速转速</h4><p style="font-size:12px;">'+idleTxt+'</p></div>'
    +'<div class="dist-card"><h4>节气门开度</h4><p>'+fmtNum(tps,0)+' %</p><p style="font-size:12px;">'+(tps<=15?'怠速区间正常':'非怠速工况，需结合转速判断')+'</p></div>'
    +'</div>';

  F.innerHTML='<div class="formula-title">📐 故障码解析结果</div>'
    +(rows?'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:6px;">'
      +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">故障码</th>'
      +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">所属系统</th>'
      +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">子类</th>'
      +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th></tr>'
      +rows+'</table>'
      :'<div class="formula-line">请输入至少一个故障码（如 P0301）。</div>')
    +'<div class="formula-line" style="margin-top:10px;">结构：第 1 位系统 · 第 2 位 0=通用/1=厂家 · 第 3 位子类 · 第 4-5 位部件或缸号</div>';

  var ad='';
  for(var i=0;i<acts.length;i++) ad+='<div class="tip-info">🧭 '+acts[i]+'</div>';
  if(ftCls==='warn'||coolCls!=='ok'||idleCls!=='ok'||list.length===0)
    ad+='<div class="tip-warn">⚠️ 数据流存在偏离或未输入有效故障码，建议在热车怠速稳定工况下重新采集后再判断。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================= bus-arrival-estimator
BA_INPUTS = '''    <div class="input-row">
      <div><label>发车间隔 (分钟)</label><input type="number" id="interval" value="10" oninput="calc()" min="1" step="1"></div>
      <div><label>上一班离站时刻</label><input type="time" id="last" value="09:05" oninput="calc()"></div>
    </div>
    <div class="input-row">
      <div><label>当前时刻</label><input type="time" id="now" value="09:12" oninput="calc()"></div>
      <div><label>起点到本站行驶时间 (分钟)</label><input type="number" id="ride" value="0" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>平均误差 (±分钟)</label><input type="number" id="err" value="2" oninput="calc()" min="0" step="1"></div>
      <div><label>线路</label>
        <select id="line" onchange="calc()">
          <option value="1">1 路</option>
          <option value="2">2 路</option>
          <option value="3">3 路</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>对比线路发车间隔 (分钟)</label><input type="number" id="iv2" value="15" oninput="calc()" min="1" step="1"></div>
      <div><label>对比线路上一班离站</label><input type="time" id="last2" value="09:02" oninput="calc()"></div>
    </div>'''

BA_CARDS = '''  <div class="card">
    <h3>⏱️ 等待时长与发车间隔关系</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">发车间隔</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">平均等待</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">最长等待</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议预留</th>
      </tr>
      <tr><td style="padding:6px 8px;">5 分钟</td><td style="padding:6px 8px;">2.5 分钟</td><td style="padding:6px 8px;">5 分钟</td><td style="padding:6px 8px;">7 分钟</td></tr>
      <tr><td style="padding:6px 8px;">10 分钟</td><td style="padding:6px 8px;">5 分钟</td><td style="padding:6px 8px;">10 分钟</td><td style="padding:6px 8px;">13 分钟</td></tr>
      <tr><td style="padding:6px 8px;">15 分钟</td><td style="padding:6px 8px;">7.5 分钟</td><td style="padding:6px 8px;">15 分钟</td><td style="padding:6px 8px;">19 分钟</td></tr>
      <tr><td style="padding:6px 8px;">20 分钟</td><td style="padding:6px 8px;">10 分钟</td><td style="padding:6px 8px;">20 分钟</td><td style="padding:6px 8px;">25 分钟</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔁 换乘衔接</h4>
      <p>把前一条线的预计到达时刻加上步行与候车时间，再叠加换乘线路的发车间隔，判断能否赶上衔接班次。两条线间隔接近时建议预留 5 分钟以上缓冲。</p>
    </div>
    <div class="scene-card">
      <h4>📡 估算与实时的差别</h4>
      <p>固定间隔只是计划值，实际受路况、红绿灯、上下客时长与驾驶节奏影响会波动。精确到站应以车载 GPS 实时回传为准，本估算适合无实时数据的粗略参考。</p>
    </div>
    <div class="info-box">💡 早高峰与平峰发车间隔通常不同，建议按所在时段选用对应间隔；跨零点线路应注意时刻表跨日。</div>
  </div>'''

BA_JS = H + '''
function toMin(s){
  var p=(s||'').split(':'); if(p.length<2) return NaN;
  return parseInt(p[0],10)*60+parseInt(p[1],10);
}
function fmtT(m){
  m=((m%1440)+1440)%1440;
  var h=Math.floor(m/60), mm=m%60;
  return (h<10?'0':'')+h+':'+(mm<10?'0':'')+mm;
}
function nextArrival(last, iv, now, ride){
  var n=last+iv;
  if(iv<=0) return NaN;
  while(n<now) n+=iv;
  return n+ride;
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var iv=val('interval'), last=toMin(str('last')), now=toMin(str('now'));
  var ride=val('ride'), err=val('err');
  var iv2=val('iv2'), last2=toMin(str('last2'));
  var lineN=str('line');

  var arr=nextArrival(last,iv,now,ride);
  var wait=now-last, togo=arr-now;
  var wLo=arr-err, wHi=arr+err;
  var arr2=nextArrival(last2,iv2,now,ride);

  var best=(arr2&&arr2<arr)?'对比线路更早':'本线路更早';
  var who=arr2? (best==='对比线路更早'?'对比线路':'本线路') : '本线路';

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">下一班到达</div><div class="result-value">'+fmtT(arr)+'</div></div>'
    +'<div class="result-item"><div class="result-label">已等待</div><div class="result-value">'+fmtNum(wait,0)+' 分钟</div></div>'
    +'<div class="result-item"><div class="result-label">还需等待</div><div class="result-value">'+fmtNum(togo,0)+' 分钟</div></div>'
    +'<div class="result-item"><div class="result-label">到达窗口</div><div class="result-value">'+fmtT(wLo)+' ~ '+fmtT(wHi)+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>本线路（'+lineN+' 路）</h4><p>间隔 '+fmtNum(iv,0)+' 分钟</p><p>到达 '+fmtT(arr)+'（约 '+fmtNum(togo,0)+' 分钟后）</p></div>'
    +'<div class="dist-card"><h4>对比线路</h4><p>间隔 '+fmtNum(iv2,0)+' 分钟</p><p>到达 '+(arr2?fmtT(arr2):'—')+'（'+(arr2?('约 '+fmtNum(arr2-now,0)+' 分钟后'):'—')+'）</p></div>'
    +'<div class="dist-card"><h4>建议出发</h4><p>'+who+'</p><p>提前 '+fmtNum(Math.max(0,err+1),0)+' 分钟到站</p></div>'
    +'<div class="dist-card"><h4>线路平均间隔</h4><p>'+fmtNum((iv+iv2)/2,1)+' 分钟</p><p>综合平均等待约 '+fmtNum((iv+iv2)/4,1)+' 分钟</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<8;i++){
    var tag=(i===0)?'下一班':'第 '+(i+1)+' 班';
    rows+='<tr><td style="padding:5px 8px;">'+tag+'</td>'
      +'<td style="padding:5px 8px;">'+fmtT(arr+i*iv)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(arr+i*iv-now,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtT(arr+i*iv-err)+' ~ '+fmtT(arr+i*iv+err)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 估算口径</div>'
    +'<div class="formula-line">下一班发车 = 上一班离站时刻 + n × 发车间隔（取首个晚于当前时刻者）</div>'
    +'<div class="formula-line">预计到达 = 下一班发车时刻 + 起点到本站行驶时间</div>'
    +'<div class="formula-line">已等待 = 当前时刻 − 上一班离站时刻；还需等待 = 预计到达 − 当前时刻</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">班次</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">到达时刻</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">距现在 (分钟)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">到达窗口</th></tr>'
    +rows+'</table>';

  var ad='';
  ad+='<div class="tip-info">🚌 本线路下一班约 '+fmtT(arr)+' 到达，已等待 '+fmtNum(wait,0)+' 分钟，还需约 '+fmtNum(togo,0)+' 分钟；建议预留 '+fmtT(wLo)+'~'+fmtT(wHi)+' 的到达窗口。</div>';
  if(arr2&&arr2<arr) ad+='<div class="tip-warn">⚠️ 对比线路预计 '+fmtT(arr2)+' 到达，比本线路早 '+fmtNum(arr-arr2,0)+' 分钟，赶时间可考虑改乘。</div>';
  if(togo<=err) ad+='<div class="tip-warn">⚠️ 剩余等待已小于平均误差，建议立即到站等候，避免错过班次。</div>';
  A.innerHTML=ad;
}
calc();'''

# ============================================================ calc-4
C4_INPUTS = '''    <div class="input-row">
      <div><label>拖车总质量 (kg)</label><input type="number" id="gw" value="1500" oninput="calc()" min="1" step="10"></div>
      <div><label>牵引车球头额定上限 (kg)</label><input type="number" id="cap" value="250" oninput="calc()" min="0" step="10"></div>
    </div>
    <div class="input-row">
      <div><label>建议载荷下限 (%)</label><input type="number" id="lo" value="10" oninput="calc()" min="1" step="0.5"></div>
      <div><label>建议载荷上限 (%)</label><input type="number" id="hi" value="15" oninput="calc()" min="1" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>实测球头载荷 (kg)</label><input type="number" id="real" value="260" oninput="calc()" min="0" step="5"></div>
      <div><label>货物重心位置</label>
        <select id="pos" onchange="calc()">
          <option value="front">集中在轴组前方（增载荷）</option>
          <option value="center">居中于轴组上方（基准）</option>
          <option value="rear">集中在轴组后方（减载荷）</option>
        </select>
      </div>
    </div>'''

C4_CARDS = '''  <div class="card">
    <h3>📊 球头载荷比例参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">拖车总重</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">10%（下限）</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">15%（上限）</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型适用</th>
      </tr>
      <tr><td style="padding:6px 8px;">750 kg</td><td style="padding:6px 8px;">75 kg</td><td style="padding:6px 8px;">113 kg</td><td style="padding:6px 8px;">小型拖斗</td></tr>
      <tr><td style="padding:6px 8px;">1500 kg</td><td style="padding:6px 8px;">150 kg</td><td style="padding:6px 8px;">225 kg</td><td style="padding:6px 8px;">中型拖挂房车</td></tr>
      <tr><td style="padding:6px 8px;">2500 kg</td><td style="padding:6px 8px;">250 kg</td><td style="padding:6px 8px;">375 kg</td><td style="padding:6px 8px;">大型房车/船拖</td></tr>
      <tr><td style="padding:6px 8px;">3500 kg</td><td style="padding:6px 8px;">350 kg</td><td style="padding:6px 8px;">525 kg</td><td style="padding:6px 8px;">重型拖挂（需配重分布）</td></tr>
    </table>
    <div class="scene-card">
      <h4>⚖️ 过低与过高的后果</h4>
      <p>球头载荷低于总重 10% 时拖车易出现蛇形摇摆（尤其下坡与侧风），高于 15% 则会压轻牵引车前轴，削弱转向与制动能力，两者都危险。</p>
    </div>
    <div class="scene-card">
      <h4>🧱 配重原则</h4>
      <p>重物应集中在拖车轴组上方，避免堆在尾端（杠杆效应会放大摇摆）。调载后用球头秤实测，并同时核对牵引车的球头额定上限与整车允许总质量（GCWR）。</p>
    </div>
    <div class="info-box">💡 务必以牵引车说明书标注的 Tongue Load 上限为准，不同车型差异较大（常见 200~350 kg）。</div>
  </div>'''

C4_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var gw=val('gw'), cap=val('cap'), lo=val('lo'), hi=val('hi'), real=val('real');
  var pos=str('pos');

  var minL=gw*lo/100, maxL=gw*hi/100;
  var pct=gw>0?real/gw*100:0;
  var devLow=real-minL, devHigh=real-maxL;
  var st, cls;
  if(real<minL){ st='偏低（易摇摆）'; cls='warn'; }
  else if(real>maxL){ st='偏高（压轻前轴）'; cls='bad'; }
  else { st='正常区间'; cls='ok'; }
  if(cap>0&&real>cap){ st='超出牵引车额定上限，禁止上路'; cls='bad'; }

  var needMove=(cls==='bad'&&devHigh>0)?devHigh:((cls==='warn')?devLow:0);

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">建议载荷区间</div><div class="result-value">'+fmtNum(minL,0)+' ~ '+fmtNum(maxL,0)+' kg</div></div>'
    +'<div class="result-item"><div class="result-label">实测占比</div><div class="result-value">'+fmtNum(pct,1)+' %</div></div>'
    +'<div class="result-item"><div class="result-label">与上限偏差</div><div class="result-value">'+(devHigh>0?'+':'')+fmtNum(devHigh,0)+' kg</div></div>'
    +'<div class="result-item"><div class="result-label">判定</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>与下限偏差</h4><p>'+(devLow>0?'+':'')+fmtNum(devLow,0)+' kg</p><p>下限 '+fmtNum(minL,0)+' kg</p></div>'
    +'<div class="dist-card"><h4>牵引车额定上限</h4><p>'+fmtNum(cap,0)+' kg</p><p>余量 '+fmtNum(cap-real,0)+' kg</p></div>'
    +'<div class="dist-card"><h4>需调整量</h4><p>'+(needMove>0?fmtNum(needMove,0)+' kg':'无需调整')+'</p><p>'+(needMove>0?'向后移载或减载':'保持当前配载')+'</p></div>'
    +'<div class="dist-card"><h4>货物重心</h4><p>'+({front:'轴组前方',center:'轴组上方',rear:'轴组后方'})[pos]+'</p><p style="font-size:12px;">'+(pos==='rear'?'尾端配重会放大摇摆，不建议':'按轴组上方为中心分配较稳')+'</p></div>'
    +'</div>';

  var rows='';
  var list=[0.5,0.75,1,1.25,1.5];
  for(var i=0;i<list.length;i++){
    var g=gw*list[i], a=g*lo/100, b=g*hi/100;
    rows+='<tr><td style="padding:5px 8px;">'+fmtNum(g,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(a,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(b,0)+'</td>'
      +'<td style="padding:5px 8px;">'+(real/a<1?'低于下限':(real/b>1?'高于上限':'区间内'))+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">建议球头载荷 = 拖车总质量 × 10% ~ 15%</div>'
    +'<div class="formula-line">实测占比 = 实测球头载荷 ÷ 拖车总质量 × 100%</div>'
    +'<div class="formula-line">超限判定：实测 &gt; 上限 或 实测 &gt; 牵引车额定上限</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">总重 (kg)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">'+fmtNum(lo,0)+'%</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">'+fmtNum(hi,0)+'%</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">按实测 '+fmtNum(real,0)+' kg 判定</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 实测球头载荷 '+fmtNum(real,0)+' kg（占 '+fmtNum(pct,1)+'%）落在 '+fmtNum(minL,0)+'~'+fmtNum(maxL,0)+' kg 的推荐区间内。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 球头载荷偏低 '+fmtNum(Math.abs(devLow),0)+' kg，拖车高速或侧风时易摆动，建议把货物前移增加载荷。</div>';
  else ad+='<div class="tip-bad">⛔ 球头载荷超限 '+fmtNum(devHigh,0)+' kg，会压轻牵引车前轴、削弱转向与制动，须后移载或减载后复测。</div>';
  if(cap>0&&real>cap) ad+='<div class="tip-bad">⛔ 已超牵引车球头额定上限 '+fmtNum(cap,0)+' kg，属超载，禁止上路。</div>';
  if(pos==='rear') ad+='<div class="tip-warn">⚠️ 重物集中在轴组后方会因杠杆效应放大摇摆，建议移至轴组上方或前方。</div>';
  A.innerHTML=ad;
}
calc();'''

# =========================================================== catalyst
CT_INPUTS = '''    <div class="input-row">
      <div><label>催化前 HC (ppm)</label><input type="number" id="hc1" value="120" oninput="calc()" min="0" step="1"></div>
      <div><label>催化后 HC (ppm)</label><input type="number" id="hc2" value="18" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>催化前 CO (%)</label><input type="number" id="co1" value="0.8" oninput="calc()" min="0" step="0.01"></div>
      <div><label>催化后 CO (%)</label><input type="number" id="co2" value="0.06" oninput="calc()" min="0" step="0.01"></div>
    </div>
    <div class="input-row">
      <div><label>催化前 NOx (ppm)</label><input type="number" id="nx1" value="800" oninput="calc()" min="0" step="1"></div>
      <div><label>催化后 NOx (ppm)</label><input type="number" id="nx2" value="120" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>测试工况</label>
        <select id="mode" onchange="calc()">
          <option value="idle">怠速（无负荷）</option>
          <option value="2500">2500 rpm 高怠速</option>
          <option value="load">加载工况（底盘测功）</option>
        </select>
      </div>
      <div><label>发动机是否缺火</label>
        <select id="misfire" onchange="calc()">
          <option value="no">无缺火</option>
          <option value="yes">存在缺火</option>
        </select>
      </div>
    </div>'''

CT_CARDS = '''  <div class="card">
    <h3>🎯 三效催化器效率判据</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">成分</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">健康效率</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">偏低提示</th>
      </tr>
      <tr><td style="padding:6px 8px;">HC（未燃碳氢）</td><td style="padding:6px 8px;">＞ 90%</td><td style="padding:6px 8px;">涂层老化、积碳堵塞</td></tr>
      <tr><td style="padding:6px 8px;">CO（一氧化碳）</td><td style="padding:6px 8px;">＞ 90%</td><td style="padding:6px 8px;">氧化能力下降、空燃比异常</td></tr>
      <tr><td style="padding:6px 8px;">NOx（氮氧化物）</td><td style="padding:6px 8px;">＞ 80%</td><td style="padding:6px 8px;">还原能力下降、富氧工况过多</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔧 常见失效原因</h4>
      <p>含铅或高硫燃油会造成涂层中毒；长期缺火使未燃混合气在催化器内二次燃烧、高温烧熔载体；烧机油产生的磷、锌沉积也会覆盖活性位点。</p>
    </div>
    <div class="scene-card">
      <h4>📉 前后氧传感器交叉验证</h4>
      <p>催化器正常时下游氧传感器信号应比上游平稳得多。若前后信号趋于一致（下游也频繁波动），说明催化器已丧失储氧能力，通常对应 P0420/P0430。</p>
    </div>
    <div class="info-box">💡 效率判定须在热车、闭环工况下采集，冷启动阶段催化器尚未起燃，效率必然偏低，不能作为失效依据。</div>
  </div>'''

CT_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var hc1=val('hc1'),hc2=val('hc2'),co1=val('co1'),co2=val('co2'),nx1=val('nx1'),nx2=val('nx2');
  var mode=str('mode'),misfire=str('misfire');

  function eff(a,b){ return a>0 ? (a-b)/a*100 : 0; }
  var eHC=eff(hc1,hc2), eCO=eff(co1,co2), eNOx=eff(nx1,nx2);
  var worst=Math.min(eHC,eCO,eNOx);

  function judge(e,th){ return e>=th ? 'ok' : (e>=th*0.85 ? 'warn' : 'bad'); }
  var cHC=judge(eHC,90), cCO=judge(eCO,90), cNOx=judge(eNOx,80);
  var cls=(cHC==='bad'||cCO==='bad'||cNOx==='bad')?'bad':((cHC==='warn'||cCO==='warn'||cNOx==='warn')?'warn':'ok');
  var verdict=cls==='ok'?'催化器效率正常':(cls==='warn'?'效率轻度下降，建议复测':'催化器效率过低，疑似失效');

  function clr(c){ return c==='ok'?'#059669':(c==='warn'?'#d97706':'#dc2626'); }

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">HC 转化效率</div><div class="result-value" style="color:'+clr(cHC)+'">'+fmtNum(eHC,1)+' %</div></div>'
    +'<div class="result-item"><div class="result-label">CO 转化效率</div><div class="result-value" style="color:'+clr(cCO)+'">'+fmtNum(eCO,1)+' %</div></div>'
    +'<div class="result-item"><div class="result-label">NOx 转化效率</div><div class="result-value" style="color:'+clr(cNOx)+'">'+fmtNum(eNOx,1)+' %</div></div>'
    +'<div class="result-item"><div class="result-label">综合评价</div><div class="result-value">'+verdict+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>HC 前后对比</h4><p>'+fmtNum(hc1,0)+' → '+fmtNum(hc2,0)+' ppm</p><p>降幅 '+fmtNum(hc1-hc2,0)+' ppm</p></div>'
    +'<div class="dist-card"><h4>CO 前后对比</h4><p>'+fmtNum(co1,3)+' → '+fmtNum(co2,3)+' %</p><p>降幅 '+fmtNum(co1-co2,3)+' %</p></div>'
    +'<div class="dist-card"><h4>NOx 前后对比</h4><p>'+fmtNum(nx1,0)+' → '+fmtNum(nx2,0)+' ppm</p><p>降幅 '+fmtNum(nx1-nx2,0)+' ppm</p></div>'
    +'<div class="dist-card"><h4>最低效率</h4><p>'+fmtNum(worst,1)+' %</p><p>决定整体判定</p></div>'
    +'</div>';

  var rows='';
  var cases=[
    ['HC',hc1,hc2,eHC,90],
    ['CO',co1,co2,eCO,90],
    ['NOx',nx1,nx2,eNOx,80]
  ];
  for(var i=0;i<cases.length;i++){
    var c=cases[i], j=judge(c[3],c[4]);
    rows+='<tr><td style="padding:5px 8px;">'+c[0]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(c[1],3)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(c[2],3)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(c[3],1)+' %</td>'
      +'<td style="padding:5px 8px;">＞'+c[4]+'%</td>'
      +'<td style="padding:5px 8px;">'+(j==='ok'?'正常':(j==='warn'?'偏低':'失效'))+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">转化效率 η = (催化前浓度 − 催化后浓度) ÷ 催化前浓度 × 100%</div>'
    +'<div class="formula-line">判据：HC / CO ＞ 90%，NOx ＞ 80% 视为健康</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">成分</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">催化前</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">催化后</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">效率</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">健康线</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">判定</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ '+verdict+'：HC '+fmtNum(eHC,1)+'%、CO '+fmtNum(eCO,1)+'%、NOx '+fmtNum(eNOx,1)+'%，均达到健康线。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ '+verdict+'：最低效率 '+fmtNum(worst,1)+'%，建议热车闭环工况复测并对比前后氧传感器波形。</div>';
  else ad+='<div class="tip-bad">⛔ '+verdict+'：最低效率仅 '+fmtNum(worst,1)+'%，结合 P0420/P0430 与前后氧传感器信号趋同可判定失效，需更换。</div>';
  if(misfire==='yes') ad+='<div class="tip-bad">⛔ 存在缺火时未燃混合气会在催化器内二次燃烧，可能烧熔载体，须先排除缺火再加装或更换催化器。</div>';
  if(mode==='idle') ad+='<div class="tip-warn">⚠️ 怠速工况负荷低、排温不足，转化效率会低于实际路况，建议配合 2500 rpm 或加载工况复核。</div>';
  A.innerHTML=ad;
}
calc();'''

# ============================================ cheshenkongqizulixishu
CS_INPUTS = '''    <div class="input-row">
      <div><label>迎风面积 (m²)</label><input type="number" id="area" value="2.2" oninput="calc()" min="0.1" step="0.05"></div>
      <div><label>风阻系数 Cd</label><input type="number" id="cd" value="0.30" oninput="calc()" min="0.01" step="0.01"></div>
    </div>
    <div class="input-row">
      <div><label>车速 (km/h)</label><input type="number" id="v" value="100" oninput="calc()" min="0" step="5"></div>
      <div><label>空气密度 (kg/m³)</label><input type="number" id="rho" value="1.225" oninput="calc()" min="0.5" step="0.005"></div>
    </div>
    <div class="input-row">
      <div><label>对比车型 Cd</label><input type="number" id="cd2" value="0.38" oninput="calc()" min="0.01" step="0.01"></div>
      <div><label>传动效率 (%)</label><input type="number" id="eff" value="90" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>车身类型</label>
        <select id="body" onchange="calc()">
          <option value="sedan">轿车（Cd 约 0.25~0.35）</option>
          <option value="suv">SUV（Cd 约 0.35~0.45）</option>
          <option value="van">厢式车（Cd 约 0.40~0.55）</option>
        </select>
      </div>
      <div><label>车速单位</label>
        <select id="unit" onchange="calc()">
          <option value="kmh">km/h</option>
          <option value="mph">mph</option>
        </select>
      </div>
    </div>'''

CS_CARDS = '''  <div class="card">
    <h3>🚗 典型车型风阻系数参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">车型</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">Cd 范围</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">迎风面积</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">100km/h 风阻功率</th>
      </tr>
      <tr><td style="padding:6px 8px;">流线轿车</td><td style="padding:6px 8px;">0.24 ~ 0.30</td><td style="padding:6px 8px;">2.0 ~ 2.3 m²</td><td style="padding:6px 8px;">约 7 ~ 9 kW</td></tr>
      <tr><td style="padding:6px 8px;">普通轿车</td><td style="padding:6px 8px;">0.30 ~ 0.35</td><td style="padding:6px 8px;">2.1 ~ 2.4 m²</td><td style="padding:6px 8px;">约 9 ~ 11 kW</td></tr>
      <tr><td style="padding:6px 8px;">SUV</td><td style="padding:6px 8px;">0.35 ~ 0.45</td><td style="padding:6px 8px;">2.6 ~ 3.0 m²</td><td style="padding:6px 8px;">约 15 ~ 22 kW</td></tr>
      <tr><td style="padding:6px 8px;">厢式/微面</td><td style="padding:6px 8px;">0.40 ~ 0.55</td><td style="padding:6px 8px;">2.8 ~ 3.4 m²</td><td style="padding:6px 8px;">约 20 ~ 30 kW</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 平方与立方关系</h4>
      <p>空气阻力 F 与车速的平方成正比，而克服风阻所需的功率 P=F·v 与车速的立方成正比。因此车速翻倍时，风阻功率约增至 8 倍；这也是高速工况能耗骤增的根本原因。</p>
    </div>
    <div class="scene-card">
      <h4>🛠️ 降阻改装</h4>
      <p>封闭进气格栅、加装平整底盘护板、减小后视镜与行李架突出物、使用低滚阻轮胎与合适胎压，均可降低 Cd 或迎风面积；高速巡航时降阻收益最明显。</p>
    </div>
    <div class="info-box">💡 迎风面积可近似取「车宽 × 车高 × 0.75~0.85」，流线造型取高值；厂家风洞数据更准确。</div>
  </div>'''

CS_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var A2=val('area'), cd=val('cd'), v=val('v'), rho=val('rho');
  var cd2=val('cd2'), eff=val('eff');
  var body=str('body'), unit=str('unit');

  var vms = unit==='mph' ? v*0.44704 : v/3.6;
  var Fd = 0.5*rho*cd*A2*vms*vms;       // N
  var P = Fd*vms;                        // W
  var Peng = eff>0 ? P/(eff/100) : P;    // 发动机/电池输出功率
  var Fd2 = 0.5*rho*cd2*A2*vms*vms;
  var P2 = Fd2*vms;

  // 参考速度点
  var speeds = unit==='mph' ? [30,50,65,75,85,100] : [50,60,80,100,120,140];

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">空气阻力</div><div class="result-value">'+fmtNum(Fd,0)+' N</div></div>'
    +'<div class="result-item"><div class="result-label">克服风阻功率</div><div class="result-value">'+fmtNum(P/1000,1)+' kW</div></div>'
    +'<div class="result-item"><div class="result-label">所需输出功率</div><div class="result-value">'+fmtNum(Peng/1000,1)+' kW</div></div>'
    +'<div class="result-item"><div class="result-label">对比 Cd='+fmtNum(cd2,2)+'</div><div class="result-value">'+fmtNum(P2/1000,1)+' kW</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>车速换算</h4><p>'+fmtNum(v,0)+' '+(unit==='mph'?'mph':'km/h')+'</p><p>= '+fmtNum(vms,2)+' m/s</p></div>'
    +'<div class="dist-card"><h4>动压</h4><p>'+fmtNum(0.5*rho*vms*vms,0)+' Pa</p><p>0.5 · ρ · v²</p></div>'
    +'<div class="dist-card"><h4>Cd 差异影响</h4><p>'+fmtNum((cd2-cd)/cd*100,1)+' %</p><p>功率差 '+fmtNum((P2-P)/1000,1)+' kW</p></div>'
    +'<div class="dist-card"><h4>车速翻倍效应</h4><p>阻力 ×4</p><p>功率 ×8</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<speeds.length;i++){
    var sp=speeds[i];
    var vm = unit==='mph' ? sp*0.44704 : sp/3.6;
    var f=0.5*rho*cd*A2*vm*vm, p=f*vm, f2=0.5*rho*cd2*A2*vm*vm, p2=f2*vm;
    rows+='<tr><td style="padding:5px 8px;">'+sp+' '+(unit==='mph'?'mph':'km/h')+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(f,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(p/1000,1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(f2,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(p2/1000,1)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">空气阻力 F = 0.5 · ρ · Cd · A · v²</div>'
    +'<div class="formula-line">克服风阻功率 P = F · v（与车速立方成正比）</div>'
    +'<div class="formula-line">整车输出功率 = P ÷ 传动效率</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">车速</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">阻力 Cd='+fmtNum(cd,2)+' (N)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">功率 (kW)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">阻力 Cd='+fmtNum(cd2,2)+' (N)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">功率 (kW)</th></tr>'
    +rows+'</table>';

  var ad='';
  var ref={sedan:[0.25,0.35],suv:[0.35,0.45],van:[0.40,0.55]}[body];
  var inRange = cd>=ref[0] && cd<=ref[1];
  ad+='<div class="tip-info">🌬️ 当前车速 '+fmtNum(v,0)+' '+(unit==='mph'?'mph':'km/h')+' 下空气阻力 '+fmtNum(Fd,0)+' N，克服风阻需 '+fmtNum(P/1000,1)+' kW'+(eff<100?('（整车输出约 '+fmtNum(Peng/1000,1)+' kW）'):'')+'。</div>';
  if(!inRange) ad+='<div class="tip-warn">⚠️ Cd='+fmtNum(cd,2)+' 超出该车身类型的常见范围（'+fmtNum(ref[0],2)+'~'+fmtNum(ref[1],2)+'），请核对输入。</div>';
  if(P2>P*1.15) ad+='<div class="tip-warn">⚠️ 对比车型 Cd 高 '+fmtNum((cd2-cd)/cd*100,1)+'%，同速下风阻功率多 '+fmtNum((P2-P)/1000,1)+' kW，高速能耗劣势明显。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='analysis-diagnosis', title='诊断（故障码/数据流）分析', icon='🚙', accent='#475569',
         desc='整理汽车 OBD 故障码与实时数据流，按系统归类并给出可能成因与处理建议，辅助车主和维修人员判断车辆故障方向。',
         inputs=AD_INPUTS, cards=AD_CARDS,
         notes='故障码需用 OBD 读取器读取，数据流应在热车怠速稳定工况下采集',
         js=AD_JS),
    dict(slug='bus-arrival-estimator', title='公交到站时间预估', icon='🚌', accent='#0f766e',
         desc='输入公交发车间隔或具体时刻表与当前时间，估算下一班车的到达时刻与已等待时长，支持多线路对比查看。',
         inputs=BA_INPUTS, cards=BA_CARDS,
         notes='按固定间隔估算，实际受路况与上下客影响，精确到站请以实时 GPS 数据为准',
         js=BA_JS),
    dict(slug='calc-4', title='拖车球头载荷计算', icon='🚙', accent='#b45309',
         desc='根据拖车总质量和建议的球头载荷比例，估算拖车球头（Tongue Load）垂直载荷。',
         inputs=C4_INPUTS, cards=C4_CARDS,
         notes='球头载荷须用球头秤实测，并同时核对牵引车说明书标注的额定上限',
         js=C4_JS),
    dict(slug='catalyst', title='排气催化器效率计算', icon='🚗', accent='#0f766e',
         desc='输入催化前后 CO、HC、NOx 浓度，计算各成分催化转换效率及综合评价。',
         inputs=CT_INPUTS, cards=CT_CARDS,
         notes='须在热车闭环工况下采集，冷启动阶段催化器未起燃，效率偏低属正常',
         js=CT_JS),
    dict(slug='cheshenkongqizulixishu', title='车身空气阻力系数', icon='🚗', accent='#0369a1',
         desc='输入迎风面积、空气阻力系数 Cd 与车速，计算空气阻力、功率消耗及各速度下的阻力变化。',
         inputs=CS_INPUTS, cards=CS_CARDS,
         notes='迎风面积可近似取车宽×车高×(0.75~0.85)，车速单位支持 km/h 与 mph',
         js=CS_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-26s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch8: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
