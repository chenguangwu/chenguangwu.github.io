#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 10。

lux-1 车灯光型照度；maintenance-schedule 保养周期排程；oil-change-countdown 换油日期倒计时；
qichekongtiaoxuanxing 空调冷负荷选型；recommender-6 胎压监测与充气推荐。
说明：recommender-6 的 deep-dive 原为「车型推荐匹配」，与页面 <title>/<desc>（胎压推荐）完全不符，
本批按页面口径重建 body，deep-dive 另由 fix 脚本同步。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ============================================================== lux-1
LX_INPUTS = '''    <div class="input-row">
      <div><label>光源总光通量 (lm)</label><input type="number" id="lm" value="1500" oninput="calc()" min="1" step="50"></div>
      <div><label>灯泡功率 (W)</label><input type="number" id="pw" value="55" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>照射距离 (m)</label><input type="number" id="d" value="10" oninput="calc()" min="0.5" step="0.5"></div>
      <div><label>光束半角 (°)</label><input type="number" id="ang" value="15" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>灯具光输出效率 (%)</label><input type="number" id="eff" value="85" oninput="calc()" min="10" max="100" step="1"></div>
      <div><label>灯型</label>
        <select id="type" onchange="calc()">
          <option value="20|近光灯">近光灯（参考中心照度 ≥ 20 lx @10m）</option>
          <option value="40|远光灯">远光灯（参考中心照度 ≥ 40 lx @10m）</option>
          <option value="10|前雾灯">前雾灯（参考中心照度 ≥ 10 lx @10m）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>光型分布</label>
        <select id="dist" onchange="calc()">
          <option value="1.0">对称光型（远光/雾灯）</option>
          <option value="0.75" selected>非对称光型（近光，明暗截止线以下）</option>
        </select>
      </div>
      <div><label>对比光通量 (lm)</label><input type="number" id="lm2" value="1000" oninput="calc()" min="1" step="50"></div>
    </div>'''

LX_CARDS = '''  <div class="card">
    <h3>💡 光源类型光效参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">光源</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">光效</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">色温</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">特点</th>
      </tr>
      <tr><td style="padding:6px 8px;">卤素灯</td><td style="padding:6px 8px;">18 ~ 30 lm/W</td><td style="padding:6px 8px;">2800 ~ 3200 K</td><td style="padding:6px 8px;">成本低、雨雾穿透好</td></tr>
      <tr><td style="padding:6px 8px;">氙气灯 HID</td><td style="padding:6px 8px;">70 ~ 100 lm/W</td><td style="padding:6px 8px;">4000 ~ 6000 K</td><td style="padding:6px 8px;">需配透镜，启动有延迟</td></tr>
      <tr><td style="padding:6px 8px;">LED</td><td style="padding:6px 8px;">80 ~ 150 lm/W</td><td style="padding:6px 8px;">5000 ~ 6500 K</td><td style="padding:6px 8px;">响应快、寿命长</td></tr>
      <tr><td style="padding:6px 8px;">激光大灯</td><td style="padding:6px 8px;">＞ 150 lm/W</td><td style="padding:6px 8px;">≥ 6000 K</td><td style="padding:6px 8px;">照射距离远、成本高</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 平方反比定律</h4>
      <p>点光源照度 E = I ÷ d²（I 为光强 cd，d 为距离 m）。距离加倍照度降为 1/4，因此远光照度天然偏低，需靠提高光强补偿；雾天还应避免高色温带来的散射眩光。</p>
    </div>
    <div class="scene-card">
      <h4>📋 法规判定参考</h4>
      <p>GB 4599《汽车用 LED 前照灯》与 GB 25991 等标准对近光明暗截止线及各测试点（如 75R、50R、50L、25L/R）规定了最小与最大照度。本工具按中心照度给出快速参考判定，正式结论须以标准原文测试点与检测机构报告为准。</p>
    </div>
    <div class="info-box">💡 改装大灯须同步校核光型与眩光：只换灯泡不调光心，往往近光变「远光」，既刺眼又年检不过。</div>
  </div>'''

LX_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var lm=val('lm'),pw=val('pw'),d=val('d'),ang=val('ang'),eff=val('eff');
  var lm2=val('lm2');
  var tp=str('type').split('|');
  var thr=parseFloat(tp[0]), tpName=tp[1];
  var distK=val('dist');

  // 光束立体角 Ω = 2π(1 − cosθ)
  var rad=ang*Math.PI/180;
  var omega=2*Math.PI*(1-Math.cos(rad));
  var I = omega>0 ? lm/omega*(eff/100)*distK : 0;   // 中心光强 cd
  var E = d>0 ? I/(d*d) : 0;                        // 中心照度 lx

  var lpw = pw>0 ? lm/pw : 0;                       // 光效 lm/W
  var omega2=omega;
  var I2 = omega2>0 ? lm2/omega2*(eff/100)*distK : 0;
  var E2 = d>0 ? I2/(d*d) : 0;

  // 法规参考值以 10 m 为基准，故把实测照度折算回 10 m 等效值再判定
  var E10 = I/100;
  var thrAt = d>0 ? thr*100/(d*d) : thr;      // 参考下限折算至当前照射距离

  var st,cls;
  if(E10>=thr*1.2){ st='高于参考下限，照明充足'; cls='ok'; }
  else if(E10>=thr){ st='达到参考下限'; cls='ok'; }
  else if(E10>=thr*0.7){ st='略低于参考下限'; cls='warn'; }
  else { st='明显不足'; cls='bad'; }

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">中心光强 I</div><div class="result-value">'+fmtNum(I,0)+' cd</div></div>'
    +'<div class="result-item"><div class="result-label">'+fmtNum(d,1)+' m 处中心照度</div><div class="result-value">'+fmtNum(E,1)+' lx</div></div>'
    +'<div class="result-item"><div class="result-label">光源光效</div><div class="result-value">'+fmtNum(lpw,1)+' lm/W</div></div>'
    +'<div class="result-item"><div class="result-label">参考判定</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>光束立体角</h4><p>'+fmtNum(omega,4)+' sr</p><p>半角 '+fmtNum(ang,0)+'°</p></div>'
    +'<div class="dist-card"><h4>参考下限</h4><p>'+fmtNum(thr,0)+' lx @10 m</p><p>折算至 '+fmtNum(d,1)+' m：'+fmtNum(thrAt,1)+' lx</p></div>'
    +'<div class="dist-card"><h4>对比光源</h4><p>'+fmtNum(E2,1)+' lx</p><p>与当前相差 '+fmtNum(E>0?(E2-E)/E*100:0,1)+' %</p></div>'
    +'<div class="dist-card"><h4>距离加倍效应</h4><p>照度 ÷ 4</p><p>'+fmtNum(d*2,0)+' m 处约 '+fmtNum(E/4,1)+' lx</p></div>'
    +'</div>';

  var rows='';
  var ds=[5,10,15,20,25,30];
  for(var i=0;i<ds.length;i++){
    rows+='<tr><td style="padding:5px 8px;">'+ds[i]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(I/(ds[i]*ds[i]),1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(I2/(ds[i]*ds[i]),1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(thr*100/(ds[i]*ds[i]),1)+'</td>'
      +'<td style="padding:5px 8px;">'+(I/(ds[i]*ds[i])>=thr*100/(ds[i]*ds[i])?'达标':'不足')+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">光束立体角 Ω = 2π × (1 − cos θ)，θ 为光束半角</div>'
    +'<div class="formula-line">中心光强 I = 光通量 Φ ÷ Ω × 灯具效率 × 光型系数</div>'
    +'<div class="formula-line">中心照度 E = I ÷ d²（平方反比定律）</div>'
    +'<div class="formula-line">判定：法规参考值以 10 m 为基准，把实测照度折算回 10 m 等效值后与参考下限比较</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">距离 (m)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">当前照度 (lx)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">对比光源 (lx)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">该距离折算下限 (lx)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">判定</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">💡 '+fmtNum(d,1)+' m 处中心照度 '+fmtNum(E,1)+' lx（折算 10 m 等效 '+fmtNum(E10,1)+' lx），达到'+tpName+'参考下限 '+fmtNum(thr,0)+' lx。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 折算 10 m 等效照度 '+fmtNum(E10,1)+' lx（'+fmtNum(d,1)+' m 处实测 '+fmtNum(E,1)+' lx）略低于参考下限 '+fmtNum(thr,0)+' lx，建议检查灯泡衰减、灯罩雾化或反光碗老化。</div>';
  else ad+='<div class="tip-bad">⛔ 折算 10 m 等效照度仅 '+fmtNum(E10,1)+' lx（'+fmtNum(d,1)+' m 处实测 '+fmtNum(E,1)+' lx），远低于参考下限，夜间行车存在安全隐患，须检修或更换灯具总成。</div>';
  if(lpw>0&&lpw<18) ad+='<div class="tip-warn">⚠️ 光效仅 '+fmtNum(lpw,1)+' lm/W，低于常见卤素灯水平，可能存在灯泡老化或参数不符。</div>';
  if(ang>25) ad+='<div class="tip-warn">⚠️ 光束半角 '+fmtNum(ang,0)+'° 偏大，光型发散会降低中心照度并增加对向眩光。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================== maintenance-schedule
MS_INPUTS = '''    <div class="input-row">
      <div><label>当前里程 (km)</label><input type="number" id="km" value="45000" oninput="calc()" min="0" step="500"></div>
      <div><label>月均行驶里程 (km)</label><input type="number" id="kmM" value="1200" oninput="calc()" min="1" step="100"></div>
    </div>
    <div class="input-row">
      <div><label>上次保养日期</label><input type="date" id="sdate" oninput="calc()"></div>
      <div><label>距上次保养已过 (月)</label><input type="number" id="mon" value="8" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>车辆类型</label>
        <select id="veh" onchange="calc()">
          <option value="1.0">汽油车</option>
          <option value="1.0">柴油车</option>
          <option value="0.9">新能源（纯电/插混）</option>
        </select>
      </div>
      <div><label>使用工况</label>
        <select id="cond" onchange="calc()">
          <option value="1.0">标准工况</option>
          <option value="0.8">严苛工况（短途拥堵/多尘/重载）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>机油类型</label>
        <select id="oil" onchange="calc()">
          <option value="5000|6">矿物油（5000 km / 6 月）</option>
          <option value="7500|8">半合成（7500 km / 8 月）</option>
          <option value="10000|12" selected>全合成（10000 km / 12 月）</option>
        </select>
      </div>
      <div><label>提醒提前量 (km)</label><input type="number" id="ahead" value="1000" oninput="calc()" min="0" step="100"></div>
    </div>'''

MS_CARDS = '''  <div class="card">
    <h3>🗓️ 常规保养项目周期参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">里程周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">时间周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">严苛工况</th>
      </tr>
      <tr><td style="padding:6px 8px;">机油 + 机油滤芯</td><td style="padding:6px 8px;">5000~10000 km</td><td style="padding:6px 8px;">6~12 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">空气滤芯</td><td style="padding:6px 8px;">15000~20000 km</td><td style="padding:6px 8px;">12 月</td><td style="padding:6px 8px;">×0.7</td></tr>
      <tr><td style="padding:6px 8px;">空调滤芯</td><td style="padding:6px 8px;">15000~20000 km</td><td style="padding:6px 8px;">12 月</td><td style="padding:6px 8px;">×0.7</td></tr>
      <tr><td style="padding:6px 8px;">汽油滤芯</td><td style="padding:6px 8px;">30000~40000 km</td><td style="padding:6px 8px;">24 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">刹车油</td><td style="padding:6px 8px;">40000 km</td><td style="padding:6px 8px;">24 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">防冻液</td><td style="padding:6px 8px;">60000 km</td><td style="padding:6px 8px;">48 月</td><td style="padding:6px 8px;">×0.9</td></tr>
      <tr><td style="padding:6px 8px;">火花塞</td><td style="padding:6px 8px;">30000~60000 km</td><td style="padding:6px 8px;">—</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">变速箱油</td><td style="padding:6px 8px;">60000~80000 km</td><td style="padding:6px 8px;">48 月</td><td style="padding:6px 8px;">×0.8</td></tr>
      <tr><td style="padding:6px 8px;">正时皮带</td><td style="padding:6px 8px;">60000~100000 km</td><td style="padding:6px 8px;">60 月</td><td style="padding:6px 8px;">按手册</td></tr>
    </table>
    <div class="scene-card">
      <h4>📏 里程与时间先到为准</h4>
      <p>手册规定机油 1 万 km 或 12 个月「先到为准」。年行驶 6000 km 的车满 12 个月也应换油；年跑 2 万 km 则约 5 个月即需首换。机油的氧化与时间相关，长期停放同样会老化。</p>
    </div>
    <div class="scene-card">
      <h4>⚠️ 严苛工况打折</h4>
      <p>频繁短途、长期拥堵、重载牵引、风沙或多尘环境，通常把周期打 7~8 折，例如 1 万 km 改为 7000~8000 km，三滤同步提前。</p>
    </div>
    <div class="info-box">💡 本排程按「周期整倍数滚动」估算下次到期里程，实际请以随车保养手册与 4S 店记录为准。</div>
  </div>'''

MS_JS = H + '''
function today0(){ var d=new Date(); return new Date(d.getFullYear(),d.getMonth(),d.getDate()); }
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var km=val('km'), kmM=val('kmM'), mon=val('mon');
  var veh=val('veh'), cond=val('cond'), ahead=val('ahead');
  var op=str('oil').split('|');
  var oilKm=parseFloat(op[0]), oilMon=parseFloat(op[1]);
  var sd=str('sdate');

  var ITEMS=[
    ['机油 + 机油滤芯', oilKm, oilMon, cond],
    ['空气滤芯', 15000, 12, cond*0.9],
    ['空调滤芯', 15000, 12, cond*0.9],
    ['汽油滤芯', 35000, 24, cond*0.8+0.2],
    ['刹车油', 40000, 24, cond*0.8+0.2],
    ['防冻液', 60000, 48, cond*0.9+0.1],
    ['火花塞', 45000, 0, cond*0.8+0.2],
    ['变速箱油', 70000, 48, cond*0.8+0.2],
    ['正时皮带', 80000, 60, 1.0]
  ];

  var rows='', soon=[], overdue=[], minLeft=Infinity, minName='';
  for(var i=0;i<ITEMS.length;i++){
    var name=ITEMS[i][0], base=ITEMS[i][1], monBase=ITEMS[i][2], k=ITEMS[i][3];
    var cyc=base*k*veh;
    if(cyc<1000) cyc=1000;
    var next=Math.ceil(km/cyc)*cyc;
    if(next<=km) next=km+cyc;
    var left=next-km;
    var leftMon=(kmM>0)?left/kmM:Infinity;   // 月均里程 kmM 为每月里程，剩余月数 = 剩余里程 ÷ 月均里程
    var st, cls;
    if(left<=0){ st='已逾期'; overdue.push(name); }
    else if(left<=ahead){ st='即将到期'; soon.push(name); }
    else { st='正常'; }
    if(left<minLeft){ minLeft=left; minName=name; }
    rows+='<tr><td style="padding:5px 8px;">'+name+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(cyc,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(next,0)+'</td>'
      +'<td style="padding:5px 8px;color:'+(left<=ahead?'#dc2626':'#059669')+';">'+fmtNum(left,0)+'</td>'
      +'<td style="padding:5px 8px;">'+(isFinite(leftMon)?fmtNum(leftMon,1):'—')+'</td>'
      +'<td style="padding:5px 8px;">'+st+'</td></tr>';
  }

  var dueCnt=overdue.length+soon.length;
  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">当前里程</div><div class="result-value">'+fmtNum(km,0)+' km</div></div>'
    +'<div class="result-item"><div class="result-label">最近到期项目</div><div class="result-value">'+minName+'</div></div>'
    +'<div class="result-item"><div class="result-label">距最近到期</div><div class="result-value">'+fmtNum(minLeft,0)+' km</div></div>'
    +'<div class="result-item"><div class="result-label">待办项目</div><div class="result-value">'+dueCnt+' 项</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>机油周期</h4><p>'+fmtNum(oilKm*cond*veh,0)+' km</p><p>时间上限 '+fmtNum(oilMon,0)+' 个月</p></div>'
    +'<div class="dist-card"><h4>已过时间</h4><p>'+fmtNum(mon,0)+' 个月</p><p>'+(mon>=oilMon?'已超时间上限':'距时间上限 '+(oilMon-mon)+' 个月')+'</p></div>'
    +'<div class="dist-card"><h4>即将到期</h4><p>'+(soon.length?soon.join('、'):'无')+'</p><p>提前量 '+fmtNum(ahead,0)+' km</p></div>'
    +'<div class="dist-card"><h4>已逾期</h4><p>'+(overdue.length?overdue.join('、'):'无')+'</p><p>'+(overdue.length?'尽快进店':'状态良好')+'</p></div>'
    +'</div>';

  F.innerHTML='<div class="formula-title">📐 排程口径</div>'
    +'<div class="formula-line">实际周期 = 手册基础周期 × 工况系数 × 车型系数</div>'
    +'<div class="formula-line">下次到期里程 = ⌈当前里程 ÷ 实际周期⌉ × 实际周期（按周期整倍数滚动）</div>'
    +'<div class="formula-line">剩余里程 = 下次到期里程 − 当前里程；剩余月数 = 剩余里程 ÷ (月均里程)</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">实际周期 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">下次到期 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (月)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>';

  var ad='';
  if(dueCnt===0) ad+='<div class="tip-info">✅ 当前里程 '+fmtNum(km,0)+' km 下暂无临近到期的保养项目，最近一项为「'+minName+'」，约 '+fmtNum(minLeft,0)+' km 后到期。</div>';
  else ad+='<div class="tip-warn">⚠️ 有 '+dueCnt+' 项需关注：'+(overdue.length?('已逾期 '+overdue.join('、')+'；'):'')+(soon.length?('即将到期 '+soon.join('、')):'')+'。建议按本次清单预约进店。</div>';
  if(mon>=oilMon) ad+='<div class="tip-bad">⛔ 距上次保养已 '+fmtNum(mon,0)+' 个月，超过机油时间上限 '+fmtNum(oilMon,0)+' 个月，即便里程未到也应更换机油。</div>';
  if(sd) ad+='<div class="tip-info">📅 上次保养日期 '+sd+'，已过 '+fmtNum(mon,0)+' 个月。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================= oil-change-countdown
OC_INPUTS = '''    <div class="input-row">
      <div><label>上次换油日期</label><input type="date" id="ldate" value="2026-01-15" oninput="calc()"></div>
      <div><label>上次换油里程 (km)</label><input type="number" id="last" value="80000" oninput="calc()" min="0" step="100"></div>
    </div>
    <div class="input-row">
      <div><label>当前里程 (km)</label><input type="number" id="cur" value="87000" oninput="calc()" min="0" step="100"></div>
      <div><label>当前日期</label><input type="date" id="today" oninput="calc()"></div>
    </div>
    <div class="input-row">
      <div><label>机油周期里程 (km)</label><input type="number" id="iv" value="10000" oninput="calc()" min="100" step="500"></div>
      <div><label>机油周期月数 (月)</label><input type="number" id="ivm" value="12" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>驾驶习惯系数</label>
        <select id="k" onchange="calc()">
          <option value="1.15">高速畅通（×1.15）</option>
          <option value="1.0" selected>城市一般（×1.0）</option>
          <option value="0.7">拥堵短途（×0.7）</option>
        </select>
      </div>
      <div><label>提醒阈值 (km)</label><input type="number" id="warn" value="500" oninput="calc()" min="0" step="100"></div>
    </div>'''

OC_CARDS = '''  <div class="card">
    <h3>⏱️ 里程与时间双阈值</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">触发条件</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">含义</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">常见场景</th>
      </tr>
      <tr><td style="padding:6px 8px;">里程先到</td><td style="padding:6px 8px;">行驶里程达到周期上限</td><td style="padding:6px 8px;">年跑 2 万 km 的通勤车</td></tr>
      <tr><td style="padding:6px 8px;">时间先到</td><td style="padding:6px 8px;">距上次换油超过月数上限</td><td style="padding:6px 8px;">年跑不足 6000 km 的代步车</td></tr>
    </table>
    <div class="scene-card">
      <h4>🛢️ 为什么时间也重要</h4>
      <p>机油在使用中会氧化、吸湿并消耗添加剂，这些变化与时间相关而非仅与里程相关。长期短途低速行驶还会因曲轴箱窜气导致水分与燃油稀释，形成乳化，因此按月倒计时同样必要。</p>
    </div>
    <div class="scene-card">
      <h4>🔄 以实际换油节点滚动计算</h4>
      <p>倒推周期应以「上次实际换油」为起点滚动计算。出厂日期或首保日期常与实际使用不符，若中途自行换过油，应及时更新上次换油里程与日期。</p>
    </div>
    <div class="info-box">💡 临近阈值时可结合近期行程预估：若接下来有长途高速，可适当提前换油，避免超里程行驶。</div>
  </div>'''

OC_JS = H + '''
function parseD(s){
  var p=(s||'').split('-');
  if(p.length!==3) return null;
  return new Date(parseInt(p[0],10),parseInt(p[1],10)-1,parseInt(p[2],10));
}
function fmtD(d){ return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); }
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var last=val('last'), cur=val('cur'), iv=val('iv'), ivm=val('ivm');
  var k=val('k'), warn=val('warn');

  var ld=parseD(str('ldate'));
  var td=parseD(str('today'));
  if(!td){ td=new Date(); td=new Date(td.getFullYear(),td.getMonth(),td.getDate()); }

  var effIv=iv*k;
  var usedKm=cur-last;
  var leftKm=effIv-usedKm;
  var kmPct=effIv>0?Math.min(100,Math.max(0,usedKm/effIv*100)):0;

  var dueD=null, leftDay=null, dayPct=0;
  if(ld){
    dueD=new Date(ld.getFullYear(), ld.getMonth()+ivm, ld.getDate());
    leftDay=Math.round((dueD-td)/86400000);
    dayPct=ivm>0?Math.min(100,Math.max(0,(1-leftDay/(ivm*30.44))*100)):0;
  }
  // 按近期日均里程折算
  var dayKm = ld && td && (td>ld) ? usedKm/Math.max(1,Math.round((td-ld)/86400000)) : 0;
  var kmDays = (dayKm>0 && leftKm>0) ? Math.round(leftKm/dayKm) : null;

  var kmTrig=leftKm<=warn;
  var dayTrig=leftDay!==null&&leftDay<=15;
  var which = (leftKm<=0&&leftDay<=0)?'里程与时间均已超期'
            : (leftKm<=0?'里程已超期'
            : (leftDay!==null&&leftDay<=0?'时间已超期'
            : (kmTrig||dayTrig?'即将到期':'未到期')));
  var cls = (leftKm<=0||(leftDay!==null&&leftDay<=0))?'bad':((kmTrig||dayTrig)?'warn':'ok');

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">剩余里程</div><div class="result-value">'+ (leftKm>0?fmtNum(leftKm,0)+' km':'已超期') +'</div></div>'
    +'<div class="result-item"><div class="result-label">时间到期日</div><div class="result-value">'+ (dueD?fmtD(dueD):'—') +'</div></div>'
    +'<div class="result-item"><div class="result-label">剩余天数</div><div class="result-value">'+ (leftDay!==null?(leftDay>0?leftDay+' 天':'已超期'):'—') +'</div></div>'
    +'<div class="result-item"><div class="result-label">倒计时状态</div><div class="result-value">'+which+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>里程进度</h4><p>'+fmtNum(kmPct,1)+' %</p><p>已行 '+fmtNum(usedKm,0)+' / '+fmtNum(effIv,0)+' km</p></div>'
    +'<div class="dist-card"><h4>时间进度</h4><p>'+fmtNum(dayPct,1)+' %</p><p>周期 '+fmtNum(ivm,0)+' 个月</p></div>'
    +'<div class="dist-card"><h4>日均里程</h4><p>'+fmtNum(dayKm,1)+' km/天</p><p>按里程约 '+(kmDays!==null?kmDays+' 天':'—')+' 后到期</p></div>'
    +'<div class="dist-card"><h4>先到者</h4><p>'+(leftKm<=0?'里程':'时间')+'</p><p>'+(leftKm<=0?'里程已超':'以剩余里程与天数中较小者为准')+'</p></div>'
    +'</div>';

  var rows='';
  var ks=[['高速畅通',1.15],['城市一般',1.0],['拥堵短途',0.7]];
  for(var i=0;i<ks.length;i++){
    var v=iv*ks[i][1], l=v-usedKm;
    rows+='<tr><td style="padding:5px 8px;">'+ks[i][0]+'</td>'
      +'<td style="padding:5px 8px;">×'+fmtNum(ks[i][1],2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(v,0)+'</td>'
      +'<td style="padding:5px 8px;">'+(l>0?fmtNum(l,0)+' km':(l===0?'刚好到期限':'已超 '+fmtNum(-l,0)+' km'))+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 倒计时口径</div>'
    +'<div class="formula-line">实际周期 = 设定周期里程 × 驾驶习惯系数</div>'
    +'<div class="formula-line">剩余里程 = 实际周期 − (当前里程 − 上次换油里程)</div>'
    +'<div class="formula-line">时间到期日 = 上次换油日期 + 周期月数；剩余天数 = 到期日 − 当前日期</div>'
    +'<div class="formula-line">按日均里程折算：剩余天数 ≈ 剩余里程 ÷ 日均里程</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">驾驶习惯</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">系数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">实际周期 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余里程</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 距下次换油还有约 '+fmtNum(leftKm,0)+' km'+(leftDay!==null?('，时间上还有约 '+leftDay+' 天'):'')+'，无需提前保养。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 已进入提醒区间（'+which+'）：剩余里程 '+fmtNum(leftKm,0)+' km'+(leftDay!==null?('、剩余 '+leftDay+' 天'):'')+'，建议近期预约。</div>';
  else ad+='<div class="tip-bad">⛔ '+which+'，应尽快更换机油，避免润滑性能下降与油泥沉积。</div>';
  if(kmDays!==null&&leftDay!==null&&kmDays<leftDay) ad+='<div class="tip-warn">⚠️ 按当前日均里程，里程将比时间更早到期（约 '+kmDays+' 天 vs '+leftDay+' 天），请以里程为准。</div>';
  if(dayKm>0&&dayKm<15) ad+='<div class="tip-warn">⚠️ 日均里程仅 '+fmtNum(dayKm,1)+' km，属短途低速工况，即使里程未到也应按时间周期更换。</div>';
  A.innerHTML=ad;
}
calc();'''

# =============================================== qichekongtiaoxuanxing
QC_INPUTS = '''    <div class="input-row">
      <div><label>车室容积 (m³)</label><input type="number" id="vol" value="5" oninput="calc()" min="0.5" step="0.5"></div>
      <div><label>乘员人数</label><input type="number" id="ppl" value="2" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>环境温度 (℃)</label><input type="number" id="amb" value="35" oninput="calc()" min="-20" step="1"></div>
      <div><label>日照强度</label>
        <select id="sun" onchange="calc()">
          <option value="0.8">强烈直射（正午露天）</option>
          <option value="0.5" selected>中等（有遮阴/多云）</option>
          <option value="0.3">较弱（阴天/夜间）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>车体隔热</label>
        <select id="ins" onchange="calc()">
          <option value="0.95">良好（隔热膜+双层玻璃）</option>
          <option value="1.0" selected>一般（原厂标准）</option>
          <option value="1.1">较差（无膜/老旧车型）</option>
        </select>
      </div>
      <div><label>制冷剂类型</label>
        <select id="ref" onchange="calc()">
          <option value="120">R134a（约 120 g/m³ 经验值）</option>
          <option value="110">R1234yf（约 110 g/m³ 经验值）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>目标温降 (℃)</label><input type="number" id="dt" value="15" oninput="calc()" min="1" step="1"></div>
      <div><label>系统能效比 COP</label><input type="number" id="cop" value="2.8" oninput="calc()" min="1" step="0.1"></div>
    </div>'''

QC_CARDS = '''  <div class="card">
    <h3>❄️ 车室容积与制冷量参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">车型</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">车室容积</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型制冷量</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">折合匹数</th>
      </tr>
      <tr><td style="padding:6px 8px;">微型车</td><td style="padding:6px 8px;">约 3 m³</td><td style="padding:6px 8px;">1.8 ~ 2.4 kW</td><td style="padding:6px 8px;">约 0.7 ~ 1.0 匹</td></tr>
      <tr><td style="padding:6px 8px;">轿车</td><td style="padding:6px 8px;">约 4 ~ 6 m³</td><td style="padding:6px 8px;">2.4 ~ 3.6 kW</td><td style="padding:6px 8px;">约 1.0 ~ 1.4 匹</td></tr>
      <tr><td style="padding:6px 8px;">SUV / MPV</td><td style="padding:6px 8px;">约 6 ~ 9 m³</td><td style="padding:6px 8px;">3.5 ~ 5.5 kW</td><td style="padding:6px 8px;">约 1.4 ~ 2.2 匹</td></tr>
      <tr><td style="padding:6px 8px;">轻客 / 房车</td><td style="padding:6px 8px;">9 ~ 20 m³</td><td style="padding:6px 8px;">5.5 ~ 12 kW</td><td style="padding:6px 8px;">约 2.2 ~ 4.8 匹</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 冷负荷构成</h4>
      <p>总冷负荷 = 车体传热（与容积、温差、隔热相关）＋ 乘员散热（每人约 0.1~0.15 kW）＋ 日照辐射＋ 新风负荷。容积只是基础项，正午暴晒与满载人员会显著抬高需求。</p>
    </div>
    <div class="scene-card">
      <h4>🔧 选型留余量</h4>
      <p>车载空调长期处于振动、高温与变转速工况，COP 低于家用机。选压缩机时建议按计算冷负荷留 15%~25% 余量，并同步核对冷凝器散热面积；「小马拉大车」会导致高温天长时间不停机却不降温。</p>
    </div>
    <div class="info-box">💡 制冷剂充注量须以车型铭牌与维修手册为准，本页按容积给出经验估算，仅用于选型阶段参考。</div>
  </div>'''

QC_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var vol=val('vol'), ppl=val('ppl'), amb=val('amb'), dt=val('dt'), cop=val('cop');
  var sun=val('sun'), ins=val('ins'), ref=val('ref');
  var refName=str('ref')==='120'?'R134a':'R1234yf';

  var base=vol*0.40;                       // 车体传热基础，kW/m³
  var body=vol*0.012*Math.max(0,dt);       // 温降附加项
  var person=ppl*0.13;
  var solar=sun;
  var heat=(base+body+person+solar)*ins;
  var pi=heat/2.5;                          // 1 匹 ≈ 2.5 kW
  // 环境温度修正 COP：车用空调 COP 以 35 ℃ 为额定工况，环境每偏离 1 ℃ 约变化 1.5%
  var copEff=cop*(1-0.015*(amb-35));
  if(copEff<1.0) copEff=1.0;
  var elec=copEff>0?heat/copEff:0;          // 压缩机轴/电功率
  var charge=vol*ref;
  var margin=heat*1.2;

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">总冷负荷</div><div class="result-value">'+fmtNum(heat,2)+' kW</div></div>'
    +'<div class="result-item"><div class="result-label">折合匹数</div><div class="result-value">'+fmtNum(pi,2)+' 匹</div></div>'
    +'<div class="result-item"><div class="result-label">压缩机功率</div><div class="result-value">'+fmtNum(elec,2)+' kW</div></div>'
    +'<div class="result-item"><div class="result-label">制冷剂充注量</div><div class="result-value">'+fmtNum(charge,0)+' g</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>车体传热</h4><p>'+fmtNum(base+body,2)+' kW</p><p>容积 '+fmtNum(vol,1)+' m³·温降 '+fmtNum(dt,0)+' ℃</p></div>'
    +'<div class="dist-card"><h4>人员散热</h4><p>'+fmtNum(person,2)+' kW</p><p>'+fmtNum(ppl,0)+' 人 × 0.13 kW</p></div>'
    +'<div class="dist-card"><h4>日照与隔热</h4><p>'+fmtNum(solar,2)+' kW × '+fmtNum(ins,2)+'</p><p>合计贡献 '+fmtNum((solar)*ins,2)+' kW</p></div>'
    +'<div class="dist-card"><h4>选型建议（含余量）</h4><p>'+fmtNum(margin,2)+' kW</p><p>约 '+fmtNum(margin/2.5,2)+' 匹</p></div>'
    +'</div>';

  var rows='';
  var vs=[3,5,7,9,12,16];
  for(var i=0;i<vs.length;i++){
    var h=(vs[i]*0.40+vs[i]*0.012*Math.max(0,dt)+person+solar)*ins;
    rows+='<tr><td style="padding:5px 8px;">'+vs[i]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(h,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(h/2.5,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(h*1.2/2.5,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(vs[i]*ref,0)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">总冷负荷 = [容积 × 0.40 + 容积 × 0.012 × 温降 + 人数 × 0.13 + 日照] × 隔热系数</div>'
    +'<div class="formula-line">折合匹数 = 冷负荷 ÷ 2.5（1 匹 ≈ 2.5 kW 制冷量）</div>'
    +'<div class="formula-line">压缩机功率 = 冷负荷 ÷ 修正 COP（额定工况 35 ℃，环境每偏离 1 ℃ COP 约变化 1.5%）</div>'
    +'<div class="formula-line">制冷剂充注量 ≈ 车室容积 × 单位容积经验值（'+refName+'）</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">容积 (m³)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">冷负荷 (kW)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">匹数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">含余量匹数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">充注量 (g)</th></tr>'
    +rows+'</table>';

  var ad='';
  ad+='<div class="tip-info">❄️ '+fmtNum(vol,1)+' m³ 车室、'+fmtNum(ppl,0)+' 人、环境 '+fmtNum(amb,0)+' ℃ 时，估算冷负荷 '+fmtNum(heat,2)+' kW（约 '+fmtNum(pi,2)+' 匹），修正 COP '+fmtNum(copEff,2)+' 下压缩机功率约 '+fmtNum(elec,2)+' kW。</div>';
  ad+='<div class="tip-info">🔧 选型建议按 '+fmtNum(margin,2)+' kW（约 '+fmtNum(margin/2.5,2)+' 匹）配置，预留约 20% 余量以应对高温工况与长期衰减。</div>';
  if(pi<1.0&&vol>5) ad+='<div class="tip-warn">⚠️ 该容积下制冷量与匹数偏低，高温天易出现「风机转但不凉」，建议提高压缩机排量或加强冷凝散热。</div>';
  if(ins>1.05) ad+='<div class="tip-warn">⚠️ 车体隔热较差，冷负荷被放大 '+fmtNum((ins-1)*100,0)+'%，建议加装隔热膜或检查车门密封条以降低能耗。</div>';
  if(amb<20) ad+='<div class="tip-warn">⚠️ 环境温度低于 20 ℃，制冷需求较小，但低温下压缩机可能因低压保护不启动，属正常现象。</div>';
  else if(amb>=35) ad+='<div class="tip-info">🌡️ 环境 '+fmtNum(amb,0)+' ℃ 达到或高于额定工况 35 ℃，修正 COP 为 '+fmtNum(copEff,2)+'，压缩机功耗较额定工况上升约 '+fmtNum(Math.max(0,(1-copEff/cop))*100,1)+'%。</div>';
  else ad+='<div class="tip-info">🌡️ 环境 '+fmtNum(amb,0)+' ℃ 低于额定工况 35 ℃，修正 COP 升至 '+fmtNum(copEff,2)+'，同等冷负荷下压缩机功率更省。</div>';
  A.innerHTML=ad;
}
calc();'''

# ======================================================= recommender-6
RC_INPUTS = '''    <div class="input-row">
      <div><label>车型类别</label>
        <select id="veh" onchange="calc()">
          <option value="2.3|2.3">轿车（前 2.3 / 后 2.3）</option>
          <option value="2.4|2.5">SUV（前 2.4 / 后 2.5）</option>
          <option value="2.5|2.7">MPV / 商务（前 2.5 / 后 2.7）</option>
          <option value="2.6|2.9">皮卡 / 越野（前 2.6 / 后 2.9）</option>
          <option value="2.5|2.6">新能源（前 2.5 / 后 2.6）</option>
        </select>
      </div>
      <div><label>载重状态</label>
        <select id="load" onchange="calc()">
          <option value="0|0">空载（1~2 人）</option>
          <option value="0.1|0.2">半载（3~4 人 / 少量行李）</option>
          <option value="0.2|0.3">满载（5 人 / 满载行李）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>季节</label>
        <select id="season" onchange="calc()">
          <option value="-0.1">夏季（常温以下 0.1）</option>
          <option value="0" selected>常温</option>
          <option value="0.1">冬季（常温以上 0.1）</option>
        </select>
      </div>
      <div><label>当前环境温度 (℃)</label><input type="number" id="amb" value="25" oninput="calc()" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>前轮实测胎压 (bar)</label><input type="number" id="p1" value="2.3" oninput="calc()" min="0" step="0.05"></div>
      <div><label>后轮实测胎压 (bar)</label><input type="number" id="p2" value="2.3" oninput="calc()" min="0" step="0.05"></div>
    </div>
    <div class="input-row">
      <div><label>参考温度 (℃)</label><input type="number" id="ref" value="20" oninput="calc()" step="1"></div>
      <div><label>TPMS 报警比例 (%)</label><input type="number" id="alm" value="25" oninput="calc()" min="1" step="1"></div>
    </div>'''

RC_CARDS = '''  <div class="card">
    <h3>🔧 充气与监测要点</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">步骤</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">做法</th>
      </tr>
      <tr><td style="padding:6px 8px;">1. 冷胎测量</td><td style="padding:6px 8px;">停车 3 小时以上或行驶不足 2 km 时读数才对应标准值</td></tr>
      <tr><td style="padding:6px 8px;">2. 四轮同测</td><td style="padding:6px 8px;">同轴左右差应 ≤ 0.1 bar，偏差大先查慢漏或胎压表误差</td></tr>
      <tr><td style="padding:6px 8px;">3. 按标贴值充气</td><td style="padding:6px 8px;">以驾驶员侧门框标贴或油箱盖内侧标注值为准</td></tr>
      <tr><td style="padding:6px 8px;">4. 复位 TPMS</td><td style="padding:6px 8px;">充气或换位后按车型说明完成系统复位/标定</td></tr>
    </table>
    <div class="scene-card">
      <h4>📈 冷胎与热胎差异</h4>
      <p>行驶后胎温上升会使胎压虚高，通常升 10 ℃ 约增 0.07~0.1 bar。热胎读数偏高属正常，切勿在热态放气，否则冷却后会亏气并触发报警。</p>
    </div>
    <div class="scene-card">
      <h4>🚨 TPMS 报警阈值</h4>
      <p>多数车型在胎压低于推荐值约 25% 时点亮报警，部分车型按 25% 或 0.5 bar 取较小者。报警后应尽快检查，别只做复位——低压行驶会导致胎侧屈曲过热、甚至爆胎。</p>
    </div>
    <div class="info-box">💡 备胎同样需要检查：多数备胎标准压力高于在用胎（常见 3.0~4.2 bar），长期不查会在需要时无法使用。</div>
  </div>'''

RC_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var vp=str('veh').split('|');
  var lp=str('load').split('|');
  var sea=val('season');
  var amb=val('amb'), p1=val('p1'), p2=val('p2'), refT=val('ref'), alm=val('alm');

  var baseF=parseFloat(vp[0]), baseR=parseFloat(vp[1]);
  var loadF=parseFloat(lp[0]), loadR=parseFloat(lp[1]);
  var recF=baseF+loadF+sea;
  var recR=baseR+loadR+sea;

  // 温度折算至参考温度（理想气体近似）
  function tempFix(p){
    if(!isFinite(amb)||!isFinite(refT)) return p;
    return p*(refT+273.15)/(amb+273.15);
  }
  var p1c=tempFix(p1), p2c=tempFix(p2);
  var d1=p1c-recF, d2=p2c-recR;
  var almF=recF*(1-alm/100), almR=recR*(1-alm/100);

  function stOf(d,rec,alarm){
    if(alarm>0&&rec<=alarm*1.02) return ['低压报警', 'bad'];
    if(d<-0.15) return ['偏低，需补气', 'warn'];
    if(d>0.15) return ['偏高，可放气', 'warn'];
    return ['正常', 'ok'];
  }
  var s1=stOf(d1,recF,almF), s2=stOf(d2,recR,almR);
  var cls=(s1[1]==='bad'||s2[1]==='bad')?'bad':((s1[1]==='warn'||s2[1]==='warn')?'warn':'ok');

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">推荐前胎压</div><div class="result-value">'+fmtNum(recF,2)+' bar</div></div>'
    +'<div class="result-item"><div class="result-label">推荐后胎压</div><div class="result-value">'+fmtNum(recR,2)+' bar</div></div>'
    +'<div class="result-item"><div class="result-label">前轮偏差</div><div class="result-value">'+(d1>0?'+':'')+fmtNum(d1,2)+' bar</div></div>'
    +'<div class="result-item"><div class="result-label">后轮偏差</div><div class="result-value">'+(d2>0?'+':'')+fmtNum(d2,2)+' bar</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>前轮状态</h4><p style="font-size:12px;">'+s1[0]+'</p><p>实测折算 '+fmtNum(p1c,2)+' bar</p></div>'
    +'<div class="dist-card"><h4>后轮状态</h4><p style="font-size:12px;">'+s2[0]+'</p><p>实测折算 '+fmtNum(p2c,2)+' bar</p></div>'
    +'<div class="dist-card"><h4>TPMS 报警下限</h4><p>前 '+fmtNum(almF,2)+' bar</p><p>后 '+fmtNum(almR,2)+' bar（−'+fmtNum(alm,0)+'%）</p></div>'
    +'<div class="dist-card"><h4>前后压差</h4><p>实测 '+fmtNum(p2-p1,2)+' bar</p><p>推荐 '+fmtNum(recR-recF,2)+' bar</p></div>'
    +'</div>';

  var rows='';
  var loads=[['空载',0,0],['半载',0.1,0.2],['满载',0.2,0.3]];
  for(var i=0;i<loads.length;i++){
    var f=baseF+loads[i][1]+sea, r=baseR+loads[i][2]+sea;
    rows+='<tr><td style="padding:5px 8px;">'+loads[i][0]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(f,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(f*(1-alm/100),2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(r,2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(r*(1-alm/100),2)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 推荐口径</div>'
    +'<div class="formula-line">推荐胎压 = 车型基准 + 载重修正 + 季节修正</div>'
    +'<div class="formula-line">实测折算 = 实测值 × (参考温度 + 273.15) ÷ (环境温度 + 273.15)</div>'
    +'<div class="formula-line">TPMS 报警下限 = 推荐值 × (1 − 报警比例)</div>'
    +'<div class="formula-line">判定：偏差在 ±0.15 bar 内视为正常</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">载重</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">前轮 (bar)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">前报警下限</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">后轮 (bar)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">后报警下限</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 前后轮胎压折算后均在推荐值 ±0.15 bar 内（前 '+fmtNum(p1c,2)+' / 后 '+fmtNum(p2c,2)+' bar），无需调整。</div>';
  else{
    if(s1[1]!=='ok') ad+='<div class="tip-warn">⚠️ 前轮：'+s1[0]+'，建议调整至 '+fmtNum(recF,2)+' bar（冷胎）。</div>';
    if(s2[1]!=='ok') ad+='<div class="tip-warn">⚠️ 后轮：'+s2[0]+'，建议调整至 '+fmtNum(recR,2)+' bar（冷胎）。</div>';
  }
  if(p1>0&&p2>0&&Math.abs((p2-p1)-(recR-recF))>0.15) ad+='<div class="tip-warn">⚠️ 实测前后压差 '+fmtNum(p2-p1,2)+' bar 与推荐前后差 '+fmtNum(recR-recF,2)+' bar 偏离较大，请按门框标贴核对前后轮标准值。</div>';
  if(amb>refT+15) ad+='<div class="tip-info">ℹ️ 当前环境温度 '+fmtNum(amb,0)+' ℃ 较高，实测读数会自然升高，已按理想气体折算到 '+fmtNum(refT,0)+' ℃ 再比较。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='lux-1', title='车灯光型照度法规计算', icon='🚗', accent='#b45309',
         desc='输入灯泡功率、光通量、照射距离与光束角度，计算中心照度并对照 GB 4599 法规判断符合性。',
         inputs=LX_INPUTS, cards=LX_CARDS,
         notes='按中心照度快速参考判定，正式结论须以 GB 4599 等标准测试点与检测机构报告为准',
         js=LX_JS),
    dict(slug='maintenance-schedule', title='车辆保养周期排程', icon='📅', accent='#0369a1',
         desc='车辆保养周期排程器，输入当前里程自动排程各保养项目并显示到期状态，避免漏保延误。',
         inputs=MS_INPUTS, cards=MS_CARDS,
         notes='按周期整倍数滚动估算下次到期里程，实际以随车保养手册与 4S 店记录为准',
         js=MS_JS),
    dict(slug='oil-change-countdown', title='机油更换倒计时', icon='🛢️', accent='#b45309',
         desc='输入已行驶里程、机油周期与驾驶习惯系数，估算下次机油更换的剩余里程或天数，避免过度保养或超期损伤。',
         inputs=OC_INPUTS, cards=OC_CARDS,
         notes='里程与日期双阈值取先到者；倒推周期应以上次实际换油节点滚动计算',
         js=OC_JS),
    dict(slug='qichekongtiaoxuanxing', title='汽车空调选型', icon='🚗', accent='#0369a1',
         desc='输入车室容积、日照强度与乘员人数，计算空调冷负荷、压缩机功率与制冷剂充注量。',
         inputs=QC_INPUTS, cards=QC_CARDS,
         notes='制冷剂充注量为选型阶段经验估算，实际以车型铭牌与维修手册标注值为准',
         js=QC_JS),
    dict(slug='recommender-6', title='胎压（监测/充气）推荐', icon='🚙', accent='#0f766e',
         desc='根据车型、载重与季节推荐前后轮标准胎压，提示冷胎与热胎读数差异及充气注意事项，帮助延长轮胎寿命并保障行车安全。',
         inputs=RC_INPUTS, cards=RC_CARDS,
         notes='胎压须在冷胎状态测量，TPMS 报警后应先查因再复位',
         js=RC_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-26s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch10: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
