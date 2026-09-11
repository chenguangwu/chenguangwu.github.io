#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 9。

container-loading 集装箱装箱估算；countdown-engine-oil 机油更换里程倒计时（含本地多车记录）；
detector-recorder-fuel 油耗异常波动检测；estimate-distance-1 制动距离估算；
estimate-wear-tire 轮胎花纹磨损估算。标题与描述沿用页面原有口径，算例经 node 实跑复核。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ==================================================== container-loading
CL_INPUTS = '''    <div class="input-row">
      <div><label>单件长 (m)</label><input type="number" id="pl" value="1.0" oninput="calc()" min="0.01" step="0.05"></div>
      <div><label>单件宽 (m)</label><input type="number" id="pw" value="0.8" oninput="calc()" min="0.01" step="0.05"></div>
    </div>
    <div class="input-row">
      <div><label>单件高 (m)</label><input type="number" id="ph" value="0.6" oninput="calc()" min="0.01" step="0.05"></div>
      <div><label>货物件数</label><input type="number" id="qty" value="500" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>单件重量 (kg)</label><input type="number" id="wt" value="80" oninput="calc()" min="0" step="1"></div>
      <div><label>柜型</label>
        <select id="ct" onchange="calc()">
          <option value="67.7|26000|40 尺高柜 40HQ">40 尺高柜 40HQ（约 67.7 m³ / 26 t）</option>
          <option value="67.0|26000|40 尺标准柜 40GP">40 尺标准柜 40GP（约 67.0 m³ / 26 t）</option>
          <option value="59.0|26000|40 尺高柜（限高货物）">40 尺高柜（限高 2.5 m，约 59 m³）</option>
          <option value="33.2|22000|20 尺标准柜 20GP">20 尺标准柜 20GP（约 33.2 m³ / 22 t）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>亏舱预留 (%)</label><input type="number" id="loss" value="0" oninput="calc()" min="0" max="50" step="5"></div>
      <div><label>成本口径</label>
        <select id="mode" onchange="calc()">
          <option value="vol">按体积主导</option>
          <option value="both">体积与重量双约束</option>
        </select>
      </div>
    </div>'''

CL_CARDS = '''  <div class="card">
    <h3>📦 常见集装箱参数</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">柜型</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">内体积</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">限重</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">适用</th>
      </tr>
      <tr><td style="padding:6px 8px;">20 尺标准柜</td><td style="padding:6px 8px;">约 33.2 m³</td><td style="padding:6px 8px;">约 22 t</td><td style="padding:6px 8px;">重货、小批量</td></tr>
      <tr><td style="padding:6px 8px;">40 尺标准柜</td><td style="padding:6px 8px;">约 67.0 m³</td><td style="padding:6px 8px;">约 26 t</td><td style="padding:6px 8px;">轻泡货、大批量</td></tr>
      <tr><td style="padding:6px 8px;">40 尺高柜 HQ</td><td style="padding:6px 8px;">约 67.7 m³</td><td style="padding:6px 8px;">约 26 t</td><td style="padding:6px 8px;">轻货、需堆高</td></tr>
      <tr><td style="padding:6px 8px;">45 尺高柜</td><td style="padding:6px 8px;">约 76 m³</td><td style="padding:6px 8px;">约 26 t</td><td style="padding:6px 8px;">超轻货（部分航线受限）</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 亏舱从哪里来</h4>
      <p>货物形状不规则、需要留通道、不能倒置或限高时，实际可装体积常只有标称的 80%~90%。估算时应预留 10%~20% 亏舱系数，否则会出现「算得下、装不下」。</p>
    </div>
    <div class="scene-card">
      <h4>⚖️ 体积与重量双约束</h4>
      <p>轻泡货由体积决定箱数，重货由限重决定。取两者所需箱数的较大值才是可行方案；同时注意整箱毛重不得超过船公司与目的国的公路限重。</p>
    </div>
    <div class="info-box">💡 拼箱（LCL）适合不足一整柜的小批量；当估算箱数接近整数上限（如 4.8 柜）时，对比「5 个整柜」与「4 柜 + 拼箱」的成本再决策。</div>
  </div>'''

CL_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var pl=val('pl'),pw=val('pw'),ph=val('ph'),qty=val('qty'),wt=val('wt');
  var loss=val('loss'),mode=str('mode');
  var mp=str('ct').split('|');
  var vol0=parseFloat(mp[0]), maxW=parseFloat(mp[1]), ctName=mp[2];

  var unit=pl*pw*ph;
  var total=unit*qty;
  var eff=vol0*(1-Math.min(loss,50)/100);
  var byVol=eff>0?Math.ceil(total/eff):0;
  var totalW=wt*qty;
  var byWt=maxW>0?Math.ceil(totalW/maxW):0;
  var need=(mode==='both')?Math.max(byVol,byWt):byVol;
  var perW=need>0?totalW/need:0;
  var fill=need>0&&eff>0?(total/need)/eff*100:0;
  var overW=perW>maxW;

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">单件体积</div><div class="result-value">'+fmtNum(unit,3)+' m³</div></div>'
    +'<div class="result-item"><div class="result-label">货物总体积</div><div class="result-value">'+fmtNum(total,1)+' m³</div></div>'
    +'<div class="result-item"><div class="result-label">所需箱数</div><div class="result-value">'+need+' 个</div></div>'
    +'<div class="result-item"><div class="result-label">单柜平均载重</div><div class="result-value">'+fmtNum(perW/1000,1)+' t</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>体积法</h4><p>'+fmtNum(total,1)+' ÷ '+fmtNum(eff,1)+' = '+fmtNum(eff>0?total/eff:0,2)+'</p><p>取整 '+byVol+' 个</p></div>'
    +'<div class="dist-card"><h4>重量法</h4><p>'+fmtNum(totalW/1000,1)+' t ÷ '+fmtNum(maxW/1000,0)+' t</p><p>取整 '+byWt+' 个</p></div>'
    +'<div class="dist-card"><h4>装载率</h4><p>'+fmtNum(fill,1)+' %</p><p>'+(fill>=85?'装载充分':(fill>=70?'尚可，可优化堆码':'偏低，建议调整柜型'))+'</p></div>'
    +'<div class="dist-card"><h4>所选柜型</h4><p style="font-size:12px;">'+ctName+'</p><p>有效容积 '+fmtNum(eff,1)+' m³</p></div>'
    +'</div>';

  var rows='';
  var types=[['20 尺标准柜',33.2,22000],['40 尺标准柜',67.0,26000],['40 尺高柜',67.7,26000]];
  for(var i=0;i<types.length;i++){
    var t=types[i], e=t[1]*(1-Math.min(loss,50)/100);
    var bv=e>0?Math.ceil(total/e):0, bw=Math.ceil(totalW/t[2]);
    rows+='<tr><td style="padding:5px 8px;">'+t[0]+'</td>'
      +'<td style="padding:5px 8px;">'+bv+'</td>'
      +'<td style="padding:5px 8px;">'+bw+'</td>'
      +'<td style="padding:5px 8px;">'+Math.max(bv,bw)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(total/(Math.max(bv,bw)*e)*100,1)+' %</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">单件体积 = 长 × 宽 × 高；总体积 = 单件体积 × 件数</div>'
    +'<div class="formula-line">体积所需箱数 = ⌈总体积 ÷ (标称内积 × (1 − 亏舱率))⌉</div>'
    +'<div class="formula-line">重量所需箱数 = ⌈总重量 ÷ 单柜限重⌉</div>'
    +'<div class="formula-line">实际箱数 = 两者取大（双约束）；装载率 = 总体积 ÷ (箱数 × 有效容积)</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">柜型</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">按体积</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">按重量</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">取大</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">装载率</th></tr>'
    +rows+'</table>';

  var ad='';
  ad+='<div class="tip-info">📦 '+fmtNum(total,1)+' m³ 货物需约 '+need+' 个'+ctName.split('（')[0]+'，单柜平均载重约 '+fmtNum(perW/1000,1)+' t。</div>';
  if(overW) ad+='<div class="tip-bad">⛔ 单柜载重 '+fmtNum(perW/1000,1)+' t 超过限重 '+fmtNum(maxW/1000,0)+' t，必须增加箱数（重量主导）。</div>';
  if(fill<70) ad+='<div class="tip-warn">⚠️ 装载率仅 '+fmtNum(fill,1)+'%，空间浪费明显，可考虑改用较小的柜型或增加装载量。</div>';
  if(loss<10) ad+='<div class="tip-warn">⚠️ 未预留亏舱系数。形状不规则或需留通道的货物建议按 10%~20% 预留，避免「算得下装不下」。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================ countdown-engine-oil
CE_INPUTS = '''    <div class="input-row">
      <div><label>车辆名称</label><input type="text" id="car" value="我的爱车" oninput="calc()" placeholder="如 沪A·12345"></div>
      <div><label>上次换油日期</label><input type="date" id="odate" oninput="calc()"></div>
    </div>
    <div class="input-row">
      <div><label>上次换油里程 (km)</label><input type="number" id="last" value="50000" oninput="calc()" min="0" step="100"></div>
      <div><label>当前里程 (km)</label><input type="number" id="cur" value="54000" oninput="calc()" min="0" step="100"></div>
    </div>
    <div class="input-row">
      <div><label>机油类型</label>
        <select id="oil" onchange="calc()">
          <option value="5000|6|矿物油">矿物油（5000 km / 6 个月）</option>
          <option value="7500|8|半合成">半合成（7500 km / 8 个月）</option>
          <option value="10000|12|全合成">全合成（10000 km / 12 个月）</option>
        </select>
      </div>
      <div><label>驾驶习惯</label>
        <select id="habit" onchange="calc()">
          <option value="1.15">高速畅通（×1.15）</option>
          <option value="1.0">城市一般（×1.0）</option>
          <option value="0.7" selected>拥堵短途（×0.7）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>涡轮增压</label>
        <select id="turbo" onchange="calc()">
          <option value="1.0">自然吸气（×1.0）</option>
          <option value="0.85">涡轮增压（×0.85）</option>
        </select>
      </div>
      <div><label>年均行驶里程 (km)</label><input type="number" id="kmY" value="15000" oninput="calc()" min="0" step="1000"></div>
    </div>'''

CE_CARDS = '''  <div class="card" id="garageCard">
    <h3>🚗 我的车库（本地保存）</h3>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:10px;">点击「保存本车记录」后，记录只保存在本机浏览器，不会上传服务器；按剩余里程从少到多排序，便于安排进店。</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
      <button type="button" onclick="saveCar()" style="padding:8px 16px;border:none;border-radius:10px;background:var(--tool-accent,#FF6B35);color:#fff;cursor:pointer;font-size:14px;">保存本车记录</button>
      <button type="button" onclick="clearCars()" style="padding:8px 16px;border:1px solid var(--border,#e5e7eb);border-radius:10px;background:transparent;color:var(--text-muted);cursor:pointer;font-size:14px;">清空车库</button>
    </div>
    <div id="garageList" style="font-size:13px;"></div>
  </div>'''

CE_JS = H + '''
var KEY='toolbox_auto_oil_countdown';
function loadCars(){
  try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return []; }
}
function saveCars(list){
  try{ localStorage.setItem(KEY, JSON.stringify(list)); }catch(e){}
}
function saveCar(){
  var rec={
    car:str('car')||'未命名车辆',
    last:val('last'), cur:val('cur'),
    oil:str('oil'), habit:str('habit'), turbo:str('turbo'),
    kmY:val('kmY'), odate:str('odate'),
    ts:new Date().toISOString().slice(0,10)
  };
  var list=loadCars().filter(function(x){return x.car!==rec.car;});
  list.push(rec);
  saveCars(list);
  renderGarage();
}
function delCar(name){
  saveCars(loadCars().filter(function(x){return x.car!==name;}));
  renderGarage();
}
function clearCars(){
  if(!confirm('确定清空车库中所有记录？该操作仅影响本机浏览器。')) return;
  saveCars([]);
  renderGarage();
}
function kmLeftOf(r){
  var op=(r.oil||'').split('|');
  var base=parseFloat(op[0])||10000;
  var iv=base*(parseFloat(r.habit)||1)*(parseFloat(r.turbo)||1);
  return iv-(r.cur-r.last);
}
function renderGarage(){
  var box=document.getElementById('garageList');
  if(!box) return;
  var list=loadCars();
  if(!list.length){ box.innerHTML='<div style="color:var(--text-muted);">暂无保存记录。</div>'; return; }
  list.sort(function(a,b){ return kmLeftOf(a)-kmLeftOf(b); });
  var rows='';
  for(var i=0;i<list.length;i++){
    var r=list[i], left=kmLeftOf(r);
    var st = left<=0 ? '已超期' : (left<=1000 ? '即将到期' : '正常');
    rows+='<tr><td style="padding:5px 8px;">'+r.car+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(r.cur,0)+'</td>'
      +'<td style="padding:5px 8px;color:'+(left<=0?'#dc2626':(left<=1000?'#d97706':'#059669'))+';">'+(left>0?fmtNum(left,0):'0')+'</td>'
      +'<td style="padding:5px 8px;">'+st+'</td>'
      +'<td style="padding:5px 8px;"><button type="button" onclick="delCar(\\''+r.car.replace(/'/g,'')+'\\')" style="border:none;background:transparent;color:#dc2626;cursor:pointer;">删除</button></td></tr>';
  }
  box.innerHTML='<table style="width:100%;border-collapse:collapse;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">车辆</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">当前里程</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">操作</th></tr>'
    +rows+'</table>';
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var last=val('last'),cur=val('cur'),kmY=val('kmY');
  var mp=str('oil').split('|');
  var base=parseFloat(mp[0]), mon=parseFloat(mp[1]), oilName=mp[2];
  var habit=val('habit'), turbo=val('turbo');

  var iv=base*habit*turbo;
  var used=cur-last;
  var left=iv-used;
  var pct=iv>0?Math.min(100,Math.max(0,used/iv*100)):0;
  var months = kmY>0 ? left/(kmY/12) : Infinity;

  var st,cls;
  if(left<=0){ st='已超期，须立即更换'; cls='bad'; }
  else if(left<=iv*0.15){ st='即将到期，尽快安排'; cls='warn'; }
  else { st='正常'; cls='ok'; }

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">建议换油间隔</div><div class="result-value">'+fmtNum(iv,0)+' km</div></div>'
    +'<div class="result-item"><div class="result-label">已行驶</div><div class="result-value">'+fmtNum(used,0)+' km</div></div>'
    +'<div class="result-item"><div class="result-label">剩余里程</div><div class="result-value">'+ (left>0?fmtNum(left,0):'0') +' km</div></div>'
    +'<div class="result-item"><div class="result-label">状态</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>周期进度</h4><p>'+fmtNum(pct,1)+' %</p><p>已用 '+fmtNum(used,0)+' / '+fmtNum(iv,0)+' km</p></div>'
    +'<div class="dist-card"><h4>预计可用时长</h4><p>'+(isFinite(months)?fmtNum(months,1)+' 个月':'—')+'</p><p>按年行驶 '+fmtNum(kmY,0)+' km 折算</p></div>'
    +'<div class="dist-card"><h4>时间上限</h4><p>'+fmtNum(mon,0)+' 个月</p><p>与里程先到为准</p></div>'
    +'<div class="dist-card"><h4>基础与系数</h4><p>'+oilName+' '+fmtNum(base,0)+' km</p><p>习惯 ×'+fmtNum(habit,2)+' · 涡轮 ×'+fmtNum(turbo,2)+'</p></div>'
    +'</div>';

  var rows='';
  var oils=[['矿物油',5000],['半合成',7500],['全合成',10000]];
  for(var i=0;i<oils.length;i++){
    var v=oils[i][1]*habit*turbo, l=v-used;
    rows+='<tr><td style="padding:5px 8px;">'+oils[i][0]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(oils[i][1],0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(v,0)+'</td>'
      +'<td style="padding:5px 8px;">'+(l>0?fmtNum(l,0):'已超期')+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">建议换油间隔 = 机油基础周期 × 驾驶习惯系数 × 涡轮增压系数</div>'
    +'<div class="formula-line">剩余里程 = 建议间隔 − (当前里程 − 上次换油里程)</div>'
    +'<div class="formula-line">预计可用时长 = 剩余里程 ÷ (年均里程 ÷ 12)</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">机油类型</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">基础周期</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">按当前系数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余里程</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 距下次换油还有约 '+fmtNum(left,0)+' km'+(isFinite(months)?('（约 '+fmtNum(months,1)+' 个月）'):'')+'，按当前工况保持即可。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 剩余仅 '+fmtNum(left,0)+' km，建议提前预约进店；若已接近时间上限也应按时间更换。</div>';
  else ad+='<div class="tip-bad">⛔ 已超出建议间隔 '+fmtNum(Math.abs(left),0)+' km，机油清净分散能力下降，须立即更换。</div>';
  if(isFinite(months)&&months<mon&&months<2) ad+='<div class="tip-warn">⚠️ 按年均里程折算仅剩约 '+fmtNum(months,1)+' 个月，短途少开的车应更看重时间上限（'+fmtNum(mon,0)+' 个月）。</div>';
  A.innerHTML=ad;
  renderGarage();
}
calc();'''

# ============================================= detector-recorder-fuel
DR_INPUTS = '''    <div class="input-row" style="display:block;">
      <div><label>油耗记录（每行一条：填写百公里油耗 L/100km，或填「里程 加油量」自动折算）</label>
        <textarea id="data" rows="10" oninput="calc()" style="width:100%;padding:10px;border-radius:10px;border:1px solid var(--border,#e5e7eb);font-family:monospace;font-size:13px;">8.0
7.8
8.2
7.9
8.1
8.3
7.7
8.0
8.1
7.8
8.2
10.5</textarea>
      </div>
    </div>
    <div class="input-row">
      <div><label>异常判定倍数</label>
        <select id="k" onchange="calc()">
          <option value="2">2σ（常规筛查，约覆盖 95%）</option>
          <option value="1.5">1.5σ（更敏感，约覆盖 87%）</option>
          <option value="3">3σ（仅抓极端值，约覆盖 99.7%）</option>
        </select>
      </div>
      <div><label>趋势判断窗口（后 N 条）</label>
        <input type="number" id="win" value="4" oninput="calc()" min="2" step="1">
      </div>
    </div>
    <div class="input-row">
      <div><label>车辆名称</label><input type="text" id="car" value="我的车" oninput="calc()" placeholder="可选"></div>
      <div><label>统计口径</label>
        <select id="sd" onchange="calc()">
          <option value="sample">样本标准差（n−1，推荐）</option>
          <option value="pop">总体标准差（n）</option>
        </select>
      </div>
    </div>'''

DR_CARDS = '''  <div class="card">
    <h3>📝 怎么记录才准确</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">做法</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">加满至跳枪</td><td style="padding:6px 8px;">每次加满后记录里程与加油量，下次加满再计算，避免估价误差</td></tr>
      <tr><td style="padding:6px 8px;">固定油站与标号</td><td style="padding:6px 8px;">减少油品密度与标号变化带来的波动</td></tr>
      <tr><td style="padding:6px 8px;">记录工况备注</td><td style="padding:6px 8px;">如长途、空调、拥堵、胎压异常，便于区分真实工况波动与故障</td></tr>
      <tr><td style="padding:6px 8px;">至少 8~12 条</td><td style="padding:6px 8px;">样本过少时均值与标准差不可靠，容易误报异常</td></tr>
    </table>
    <div class="scene-card">
      <h4>📈 单点 vs 趋势</h4>
      <p>冬季、短途、满载空调、胎压偏低都会抬高油耗，单点偏高属正常。真正值得警惕的是「连续多期高于上限」的持续恶化，往往指向积碳、点火不良、氧传感器失准或制动拖滞。</p>
    </div>
    <div class="scene-card">
      <h4>🔧 排查顺序建议</h4>
      <p>先排除工况与胎压因素 → 检查空气滤芯与节气门积碳 → 读 OBD 看长期燃油修正与氧传感器 → 再查点火系统与制动拖滞。按此顺序可避免盲目换件。</p>
    </div>
    <div class="info-box">💡 表显油耗通常比实际偏低 3%~10%，长期对比请统一使用「加油量 ÷ 区间里程」的实测值。</div>
  </div>'''

DR_JS = H + '''
function sdOf(a,sample){
  if(a.length<2) return 0;
  var m=0,i; for(i=0;i<a.length;i++) m+=a[i]; m/=a.length;
  var s=0; for(i=0;i<a.length;i++) s+=(a[i]-m)*(a[i]-m);
  return Math.sqrt(s/(sample?a.length-1:a.length));
}
function meanOf(a){
  if(!a.length) return 0;
  var m=0,i; for(i=0;i<a.length;i++) m+=a[i];
  return m/a.length;
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var raw=str('data')||'';
  var k=val('k'), win=Math.max(2,Math.round(val('win')));
  var sample=str('sd')==='sample';

  var lines=raw.split(/\\r?\\n/), vals=[], notes=[], bad=0;
  for(var i=0;i<lines.length;i++){
    var s=(lines[i]||'').trim();
    if(!s) continue;
    var parts=s.split(/[\\s,，;；\\t]+/).filter(function(x){return x!=='';});
    if(parts.length>=2){
      var km=parseFloat(parts[0]), L=parseFloat(parts[1]);
      if(isFinite(km)&&isFinite(L)&&km>0){ vals.push(L/km*100); notes.push('第 '+(i+1)+' 行（按里程+加油量折算）'); continue; }
    }
    var v=parseFloat(s);
    if(isFinite(v)){ vals.push(v); notes.push('第 '+(i+1)+' 行'); }
    else bad++;
  }

  if(vals.length<2){
    R.innerHTML='<div class="result-grid"><div class="result-item"><div class="result-label">有效记录</div><div class="result-value">'+vals.length+' 条</div></div>'
      +'<div class="result-item"><div class="result-label">提示</div><div class="result-value">至少需要 2 条</div></div></div>';
    G.innerHTML=''; F.innerHTML='<div class="formula-line">请在文本框中输入至少 2 条有效记录。</div>';
    A.innerHTML='<div class="tip-warn">⚠️ 记录不足，无法计算均值与标准差。建议累计 8~12 条后再做异常筛查。</div>';
    return;
  }

  var mean=meanOf(vals), sd=sdOf(vals,sample);
  var up=mean+k*sd, lo=Math.max(0,mean-k*sd);
  var hi=[], rowId=0;
  for(var i=0;i<vals.length;i++){
    if(vals[i]>up||vals[i]<lo) hi.push({i:i+1, v:vals[i], tag:notes[i]});
  }
  var tail=vals.slice(Math.max(0,vals.length-win));
  var tMean=meanOf(tail);
  var trend = tMean>mean*1.05 ? '近 '+win+' 条均值高于总体 5% 以上，油耗呈上升趋势'
            : (tMean<mean*0.95 ? '近 '+win+' 条均值低于总体 5% 以上，油耗下降'
            : '近 '+win+' 条与总体基本持平');
  var tCls = tMean>mean*1.05 ? 'warn' : 'ok';

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">有效记录</div><div class="result-value">'+vals.length+' 条</div></div>'
    +'<div class="result-item"><div class="result-label">平均油耗</div><div class="result-value">'+fmtNum(mean,2)+' L/100km</div></div>'
    +'<div class="result-item"><div class="result-label">标准差 σ</div><div class="result-value">'+fmtNum(sd,2)+' L</div></div>'
    +'<div class="result-item"><div class="result-label">异常记录</div><div class="result-value">'+hi.length+' 条</div></div>'
    +'</div>';

  var rr=fmtNum(hi[0]?hi[0].v:0,2);
  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>正常区间</h4><p>'+fmtNum(lo,2)+' ~ '+fmtNum(up,2)+' L</p><p>均值 ± '+fmtNum(k,1)+'σ</p></div>'
    +'<div class="dist-card"><h4>最低 / 最高</h4><p>'+fmtNum(Math.min.apply(null,vals),2)+' / '+fmtNum(Math.max.apply(null,vals),2)+'</p><p>极差 '+fmtNum(Math.max.apply(null,vals)-Math.min.apply(null,vals),2)+' L</p></div>'
    +'<div class="dist-card"><h4>近期趋势</h4><p style="font-size:12px;">'+trend+'</p><p>近 '+win+' 条均值 '+fmtNum(tMean,2)+' L</p></div>'
    +'<div class="dist-card"><h4>波动离散度</h4><p>'+fmtNum(mean>0?sd/mean*100:0,1)+' %</p><p>'+(sd/mean>0.15?'波动较大':'波动平稳')+'</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<vals.length;i++){
    var isHi=(vals[i]>up||vals[i]<lo);
    rows+='<tr><td style="padding:5px 8px;">'+(i+1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(vals[i],2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(vals[i]-mean,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(sd>0?(vals[i]-mean)/sd:0,2)+'σ</td>'
      +'<td style="padding:5px 8px;color:'+(isHi?'#dc2626':'#059669')+';">'+(isHi?'异常':'正常')+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">均值 μ = Σx ÷ n；标准差 σ = √(Σ(x−μ)² ÷ '+(sample?'(n−1)':'n')+')</div>'
    +'<div class="formula-line">正常区间 = μ ± '+fmtNum(k,1)+'σ ；超出者标记为异常记录</div>'
    +'<div class="formula-line">里程折算：[加油量 L ÷ 区间里程 km × 100] = 百公里油耗</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">序</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">油耗 (L/100km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">与均值差</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">偏离 σ</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">判定</th></tr>'
    +rows+'</table>';

  var ad='';
  if(!hi.length) ad+='<div class="tip-info">✅ 共 '+vals.length+' 条记录，均值 '+fmtNum(mean,2)+' L/100km，未见超出 '+fmtNum(k,1)+'σ（'+fmtNum(lo,2)+'~'+fmtNum(up,2)+' L）的异常值，油耗表现稳定。</div>';
  else{
    var names=hi.map(function(x){return x.tag+'='+fmtNum(x.v,2)+'L';}).join('、');
    ad+='<div class="tip-warn">⚠️ 检出 '+hi.length+' 条异常记录：'+names+'。请结合当期工况（长途/空调/拥堵）判断，若排除工况后仍持续偏高，再排查车辆状态。</div>';
  }
  if(tCls==='warn') ad+='<div class="tip-warn">⚠️ '+trend+'，建议提前检查空气滤芯、节气门积碳、氧传感器与胎压。</div>';
  else ad+='<div class="tip-info">📈 '+trend+'。</div>';
  if(bad) ad+='<div class="tip-warn">⚠️ 有 '+bad+' 行无法解析已忽略（支持「油耗值」或「里程 加油量」两种格式）。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================ estimate-distance-1
ED_INPUTS = '''    <div class="input-row">
      <div><label>车速 (km/h)</label><input type="number" id="v" value="100" oninput="calc()" min="0" step="5"></div>
      <div><label>反应时间 (s)</label><input type="number" id="rt" value="1" oninput="calc()" min="0.1" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>路面峰值附着系数 μ</label><input type="number" id="mu" value="1.0" oninput="calc()" min="0.05" step="0.05"></div>
      <div><label>道路坡度 (%)（上坡为正）</label><input type="number" id="grade" value="0" oninput="calc()" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>对比路面 μ</label><input type="number" id="mu2" value="0.6" oninput="calc()" min="0.05" step="0.05"></div>
      <div><label>路面预设</label>
        <select id="road" onchange="applyRoad()">
          <option value="1.0|0.6">干燥沥青 / 雨天对比</option>
          <option value="0.8|0.5">干燥水泥 / 湿滑对比</option>
          <option value="0.5|0.2">湿沥青 / 积雪对比</option>
          <option value="0.2|0.1">积雪 / 结冰对比</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>跟车时距参考 (s)</label><input type="number" id="gap" value="2" oninput="calc()" min="0.5" step="0.5"></div>
      <div><label>制动协调时间 (s，通常 0.2，可填 0)</label><input type="number" id="bt" value="0" oninput="calc()" min="0" step="0.05"></div>
    </div>'''

ED_CARDS = '''  <div class="card">
    <h3>🛞 不同路面的附着系数参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">路面状态</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">峰值 μ</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">100km/h 制动距离</th>
      </tr>
      <tr><td style="padding:6px 8px;">干燥沥青</td><td style="padding:6px 8px;">0.8 ~ 1.0</td><td style="padding:6px 8px;">约 39 ~ 49 m</td></tr>
      <tr><td style="padding:6px 8px;">雨天湿沥青</td><td style="padding:6px 8px;">0.5 ~ 0.6</td><td style="padding:6px 8px;">约 66 ~ 79 m</td></tr>
      <tr><td style="padding:6px 8px;">积雪路面</td><td style="padding:6px 8px;">0.2 ~ 0.3</td><td style="padding:6px 8px;">约 131 ~ 197 m</td></tr>
      <tr><td style="padding:6px 8px;">结冰路面</td><td style="padding:6px 8px;">0.1 ~ 0.15</td><td style="padding:6px 8px;">约 262 ~ 393 m</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 平方关系</h4>
      <p>制动距离与初速的平方成正比：车速从 50 提到 100 km/h，制动距离约变为 4 倍；叠加基本不变的反应距离后，总停车距离增长更惊人。降速是最有效的安全手段。</p>
    </div>
    <div class="scene-card">
      <h4>🧠 反应时间的现实</h4>
      <p>普通驾驶者从发现到踩下刹车的反应时间约 0.75~1.5 s，含感知、判断与动作；分心、疲劳或夜间识别不良时更长。安全距离核算常取 1 s 基准，实际应留更大余量。</p>
    </div>
    <div class="info-box">💡 跟车时距建议：干燥路面 ≥ 2 s，雨天 ≥ 3 s，冰雪 ≥ 4~6 s。用「时距」而非「车距」更便于随速调整。</div>
  </div>'''

ED_JS = H + '''
function applyRoad(){
  var p=str('road').split('|');
  document.getElementById('mu').value=p[0];
  document.getElementById('mu2').value=p[1];
  calc();
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var v=val('v'),rt=val('rt'),mu=val('mu'),grade=val('grade');
  var mu2=val('mu2'),gap=val('gap'),bt=val('bt');

  var vms=v/3.6;
  var g=9.81;
  var reach=vms*rt;             // 反应距离
  var coord=vms*bt;             // 制动协调（建压）距离
  function brakeDist(muV, slopePct){
    var denom=muV + slopePct/100;   // 上坡增加有效减速度（近似 sinθ≈tanθ）
    if(denom<=0.01) denom=0.01;
    return vms*vms/(2*g*denom);
  }
  var bd1=brakeDist(mu,grade);
  var bd2=brakeDist(mu2,grade);
  var total1=reach+coord+bd1, total2=reach+coord+bd2;
  var gapDist=vms*gap;
  var muEq=mu+grade/100;

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">反应距离</div><div class="result-value">'+fmtNum(reach,1)+' m</div></div>'
    +'<div class="result-item"><div class="result-label">制动距离</div><div class="result-value">'+fmtNum(bd1,1)+' m</div></div>'
    +'<div class="result-item"><div class="result-label">总停车距离</div><div class="result-value">'+fmtNum(total1,1)+' m</div></div>'
    +'<div class="result-item"><div class="result-label">安全跟车距离</div><div class="result-value">'+fmtNum(gapDist,1)+' m</div></div>'
    +'</div>';

  var ratio=total1>0?gapDist/total1:0;
  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>对比路面（μ='+fmtNum(mu2,2)+'）</h4><p>制动 '+fmtNum(bd2,1)+' m</p><p>总停 '+fmtNum(total2,1)+' m</p></div>'
    +'<div class="dist-card"><h4>路面差异增幅</h4><p>'+fmtNum(bd1>0?(bd2-bd1)/bd1*100:0,1)+' %</p><p>多出 '+fmtNum(total2-total1,1)+' m</p></div>'
    +'<div class="dist-card"><h4>等效附着系数</h4><p>'+fmtNum(muEq,3)+'</p><p>坡度 '+fmtNum(grade,0)+' % 修正</p></div>'
    +'<div class="dist-card"><h4>时距评估</h4><p>'+fmtNum(gap,1)+' s</p><p>'+(gapDist>=total1?'可覆盖停车距离':'小于停车距离，需加大')+'</p></div>'
    +'</div>';

  var rows='';
  var speeds=[30,50,60,80,100,120];
  for(var i=0;i<speeds.length;i++){
    var sp=speeds[i], vm=sp/3.6;
    var r1=vm*rt;
    function bdAt(muV){
      var den=muV+grade/100; if(den<=0.01) den=0.01;
      return vm*vm/(2*g*den);
    }
    rows+='<tr><td style="padding:5px 8px;">'+sp+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(r1,1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(bdAt(mu),1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(r1+bdAt(mu),1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(r1+bdAt(mu2),1)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">反应距离 = v × t（v 单位 m/s，t 为反应时间）</div>'
    +'<div class="formula-line">制动距离 = v² ÷ [2g × (μ + 坡度)]（上坡增加有效减速度）</div>'
    +'<div class="formula-line">总停车距离 = 反应距离 + 制动协调距离 + 制动距离；安全跟车距离 = v × 时距</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">车速 (km/h)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">反应 (m)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">制动 (m)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">总停 μ='+fmtNum(mu,2)+' (m)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">总停 μ='+fmtNum(mu2,2)+' (m)</th></tr>'
    +rows+'</table>';

  var ad='';
  ad+='<div class="tip-info">🛑 '+fmtNum(v,0)+' km/h 时反应距离 '+fmtNum(reach,1)+' m、制动距离 '+fmtNum(bd1,1)+' m，总停车距离约 '+fmtNum(total1,1)+' m。</div>';
  if(mu2<mu) ad+='<div class="tip-warn">⚠️ 湿滑路面（μ='+fmtNum(mu2,2)+'）制动距离增至 '+fmtNum(bd2,1)+' m，总停车约 '+fmtNum(total2,1)+' m，比干燥路面多 '+fmtNum(total2-total1,1)+' m。跟车距离须同步加大。</div>';
  if(gapDist<total1) ad+='<div class="tip-bad">⛔ 当前 '+fmtNum(gap,1)+' s 时距对应 '+fmtNum(gapDist,1)+' m，小于总停车距离 '+fmtNum(total1,1)+' m，紧急情况下无法避免追尾，请加大跟车距离。</div>';
  if(grade<0) ad+='<div class="tip-warn">⚠️ 下坡时有效减速度下降，制动距离显著增加，长下坡应提前降挡利用发动机制动。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================ estimate-wear-tire
EW_INPUTS = '''    <div class="input-row">
      <div><label>新胎花纹深度 (mm)</label><input type="number" id="nw" value="8" oninput="calc()" min="1" step="0.1"></div>
      <div><label>当前花纹深度 (mm)</label><input type="number" id="cw" value="4" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>已行驶里程 (km)</label><input type="number" id="km" value="40000" oninput="calc()" min="0" step="500"></div>
      <div><label>法定更换下限 (mm)</label><input type="number" id="lim" value="1.6" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>建议预警值 (mm)</label><input type="number" id="warn" value="3" oninput="calc()" min="0" step="0.5"></div>
      <div><label>年均行驶里程 (km)</label><input type="number" id="kmY" value="15000" oninput="calc()" min="0" step="1000"></div>
    </div>
    <div class="input-row">
      <div><label>对侧轮胎花纹深度 (mm)</label><input type="number" id="other" value="4.6" oninput="calc()" min="0" step="0.1"></div>
      <div><label>轮胎数量</label>
        <select id="cnt" onchange="calc()">
          <option value="4">4 条</option>
          <option value="2">2 条（成对更换）</option>
        </select>
      </div>
    </div>'''

EW_CARDS = '''  <div class="card">
    <h3>📏 花纹深度与安全状态</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">花纹深度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议</th>
      </tr>
      <tr><td style="padding:6px 8px;">8 mm</td><td style="padding:6px 8px;">全新</td><td style="padding:6px 8px;">正常使用</td></tr>
      <tr><td style="padding:6px 8px;">4 ~ 7 mm</td><td style="padding:6px 8px;">良好</td><td style="padding:6px 8px;">定期换位与定位检查</td></tr>
      <tr><td style="padding:6px 8px;">3 mm</td><td style="padding:6px 8px;">预警线</td><td style="padding:6px 8px;">雨天排水能力下降，规划更换</td></tr>
      <tr><td style="padding:6px 8px;">1.6 mm</td><td style="padding:6px 8px;">法定极限</td><td style="padding:6px 8px;">必须立即更换</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 磨损速率怎么算</h4>
      <p>磨损率 =（新胎深度 − 当前深度）÷ 已行驶里程。用实测速率推算剩余里程，比按年限估算更贴近本车实际，但驾驶习惯或路况改变后速率也会变化。</p>
    </div>
    <div class="scene-card">
      <h4>🔍 同轴差异提示什么</h4>
      <p>同轴两侧花纹深度差超过 1 mm，通常指向胎压长期不一致、四轮定位失准（前束/外倾）或悬架衬套松旷。发现偏磨应做定位与动平衡，否则新胎也会很快磨偏。</p>
    </div>
    <div class="info-box">💡 除花纹外，胎侧鼓包、裂纹、扎修补次数过多（＞3 次）或胎龄超过 6 年，即使花纹尚可就应更换。</div>
  </div>'''

EW_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var nw=val('nw'),cw=val('cw'),km=val('km'),lim=val('lim');
  var warn=val('warn'),kmY=val('kmY'),other=val('other'),cnt=Math.round(val('cnt'));

  var used=nw-cw;
  var rate = km>0 ? used/(km/1000) : 0;          // mm/1000km
  var remainDepth=Math.max(0,cw-lim);
  var remainKm = rate>0 ? remainDepth/rate*1000 : Infinity;
  var toWarnDepth=Math.max(0,cw-warn);
  var toWarnKm = rate>0 ? toWarnDepth/rate*1000 : Infinity;
  var months = (isFinite(remainKm)&&kmY>0) ? remainKm/(kmY/12) : Infinity;
  var totalLife = rate>0 ? (nw-lim)/rate*1000 : Infinity;
  var usedPct = (nw-lim)>0 ? used/(nw-lim)*100 : 0;
  var diff = Math.abs(cw-other);

  var st,cls;
  if(cw<=lim){ st='已达法定极限，必须更换'; cls='bad'; }
  else if(cw<=warn){ st='进入预警区，建议尽快更换'; cls='warn'; }
  else { st='状态良好'; cls='ok'; }

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">磨损率</div><div class="result-value">'+fmtNum(rate,3)+' mm/千km</div></div>'
    +'<div class="result-item"><div class="result-label">剩余可用深度</div><div class="result-value">'+fmtNum(remainDepth,1)+' mm</div></div>'
    +'<div class="result-item"><div class="result-label">剩余里程</div><div class="result-value">'+ (isFinite(remainKm)?fmtNum(remainKm,0)+' km':'—') +'</div></div>'
    +'<div class="result-item"><div class="result-label">判断</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>已磨损</h4><p>'+fmtNum(used,1)+' mm</p><p>占可用量 '+fmtNum(usedPct,1)+' %</p></div>'
    +'<div class="dist-card"><h4>到预警线 (3mm)</h4><p>'+(isFinite(toWarnKm)?fmtNum(toWarnKm,0)+' km':'—')+'</p><p>剩余深度 '+(toWarnDepth>0?fmtNum(toWarnDepth,1)+' mm':'已达预警')+'</p></div>'
    +'<div class="dist-card"><h4>预计可用时长</h4><p>'+(isFinite(months)?fmtNum(months,1)+' 个月':'—')+'</p><p>按年行驶 '+fmtNum(kmY,0)+' km</p></div>'
    +'<div class="dist-card"><h4>同轴差异</h4><p>'+fmtNum(diff,1)+' mm</p><p>'+(diff>=1?'偏磨明显，建议查定位与胎压':'左右一致，正常')+'</p></div>'
    +'</div>';

  var rows='';
  var steps=[1,2,3,4,5,6];
  for(var i=0;i<steps.length;i++){
    var extra=steps[i]*10000;
    var depth=cw-rate*extra/1000;
    rows+='<tr><td style="padding:5px 8px;">'+fmtNum(extra/1000,0)+' 千km</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(Math.max(0,depth),2)+'</td>'
      +'<td style="padding:5px 8px;">'+(depth<=lim?'已达极限':(depth<=warn?'预警区':'正常'))+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(km+extra,0)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">磨损率 = (新胎深度 − 当前深度) ÷ 已行驶里程（换算为 mm/千km）</div>'
    +'<div class="formula-line">剩余里程 = (当前深度 − 法定下限) ÷ 磨损率</div>'
    +'<div class="formula-line">轮胎总寿命 ≈ (新胎深度 − 法定下限) ÷ 磨损率</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">再行驶</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">预计深度 (mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">累计里程 (km)</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 当前花纹 '+fmtNum(cw,1)+' mm，磨损率 '+fmtNum(rate,3)+' mm/千km，预计还可行驶约 '+(isFinite(remainKm)?fmtNum(remainKm,0):'—')+' km（约 '+(isFinite(months)?fmtNum(months,1):'—')+' 个月）。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 已进入预警区（'+fmtNum(cw,1)+' mm），雨天排水性能明显下降，建议尽快安排更换。</div>';
  else ad+='<div class="tip-bad">⛔ 花纹 '+fmtNum(cw,1)+' mm 已达法定下限 '+fmtNum(lim,1)+' mm，湿滑路面极易失控，必须立即更换。</div>';
  if(diff>=1) ad+='<div class="tip-warn">⚠️ 同轴两侧花纹差 '+fmtNum(diff,1)+' mm，存在偏磨，建议检查胎压一致性与四轮定位，避免新胎快速磨偏。</div>';
  if(isFinite(totalLife)) ad+='<div class="tip-info">📊 按当前磨损率，单条轮胎总寿命约 '+fmtNum(totalLife,0)+' km（'+cnt+' 条合计约 '+fmtNum(totalLife*cnt,0)+' km 里程）。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='container-loading', title='集装箱装箱数量估算（汽车）', icon='📦', accent='#0369a1',
         desc='集装箱装箱数量估算器，输入货物尺寸与数量估算所需集装箱数，辅助物流配载与运输规划。',
         inputs=CL_INPUTS, cards=CL_CARDS,
         notes='估算未含货物不可堆叠、限高与绑扎空间等约束，实际装载建议预留 10%~20% 亏舱',
         js=CL_JS),
    dict(slug='countdown-engine-oil', title='机油更换里程倒计时', icon='🛢️', accent='#b45309',
         desc='机油更换里程倒计时，按机油类型与驾驶习惯系数智能计算建议换油间隔与剩余里程，支持多车管理、数据本地保存。',
         inputs=CE_INPUTS, cards=CE_CARDS,
         notes='里程与时间先到为准；车库记录保存在本机浏览器，清除浏览器数据会一并丢失',
         js=CE_JS),
    dict(slug='detector-recorder-fuel', title='油耗异常波动检测器（输入记录）', icon='🚙', accent='#475569',
         desc='粘贴一段时期的油耗记录，自动计算平均值并标出偏离过大的异常区间，帮助发现车辆油耗突变与潜在故障。',
         inputs=DR_INPUTS, cards=DR_CARDS,
         notes='支持「单值」与「里程 加油量」两种格式；样本少于 8 条时统计结果参考性有限',
         js=DR_JS),
    dict(slug='estimate-distance-1', title='制动距离估算', icon='🚗', accent='#b91c1c',
         desc='输入车速、制动减速度、反应时间与道路坡度，计算反应距离、制动距离及总停车距离，用于安全驾驶评估与交通事故分析。',
         inputs=ED_INPUTS, cards=ED_CARDS,
         notes='制动距离按峰值附着系数理论值计算，实际还受轮胎、载荷与 ABS 介入影响',
         js=ED_JS),
    dict(slug='estimate-wear-tire', title='轮胎花纹磨损估算', icon='🚗', accent='#0f766e',
         desc='输入新胎与当前花纹深度及行驶里程，计算磨损率、剩余可用里程与更换建议。',
         inputs=EW_INPUTS, cards=EW_CARDS,
         notes='花纹深度须在主排水沟槽多点测量取最小值，胎侧损伤不受花纹深度限制',
         js=EW_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-26s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch9: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
