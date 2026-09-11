#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 6（voltage-2 / analysis-strength）。

voltage-2 发电机电压调节（保留原 title/desc 口径：发电机输出电压、充电电流、调节器状态），
并补充线路压降模块，呼应 deep-dive「48V 轻混系统与电路压降」示例；
analysis-strength 车架（刚度/强度）分析，按 deep-dive 示例（b=60/h=120/L=1000/F=5000）
实现弯曲应力、挠度与扭转刚度校核。算例均经 node 实跑复核。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ------------------------------------------------------------- voltage-2
VO_INPUTS = '''    <div class="input-row">
      <div><label>系统标称电压 (V)</label><input type="number" id="volt" value="12" oninput="calc()" min="1" step="0.1"></div>
      <div><label>调节器目标电压 (V)</label><input type="number" id="vreg" value="14.4" oninput="calc()" min="1" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>发电机切入转速 (rpm，按发动机转速折算)</label><input type="number" id="cutin" value="700" oninput="calc()" min="100" step="50"></div>
      <div><label>当前发动机转速 (rpm)</label><input type="number" id="rpm" value="2500" oninput="calc()" min="0" step="50"></div>
    </div>
    <div class="input-row">
      <div><label>电池静态电压 (V)</label><input type="number" id="vbat" value="12.4" oninput="calc()" min="0" step="0.1"></div>
      <div><label>充电回路总电阻 (Ω)</label><input type="number" id="rloop" value="0.08" oninput="calc()" min="0.001" step="0.01"></div>
    </div>
    <div class="input-row">
      <div><label>负载电流 (A)</label><input type="number" id="load" value="10" oninput="calc()" min="0" step="1"></div>
      <div><label>供电线长度 (m，单程)</label><input type="number" id="len" value="5" oninput="calc()" min="0" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>供电线线径 (mm²)</label><input type="number" id="area" value="2.5" oninput="calc()" min="0.1" step="0.5"></div>
      <div><label>线材</label>
        <select id="mat" onchange="calc()">
          <option value="0.0175">铜（ρ=0.0175）</option>
          <option value="0.0282">铝（ρ=0.0282）</option>
        </select>
      </div>
    </div>'''

VO_CARDS = '''  <div class="card">
    <h3>🔋 12V 电池荷电状态对照</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">静态电压</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">荷电状态</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">≥ 12.66 V</td><td style="padding:6px 8px;">100%（满电）</td><td style="padding:6px 8px;">静置 2h 后测量</td></tr>
      <tr><td style="padding:6px 8px;">12.45 V</td><td style="padding:6px 8px;">约 75%</td><td style="padding:6px 8px;">正常使用区间</td></tr>
      <tr><td style="padding:6px 8px;">12.24 V</td><td style="padding:6px 8px;">约 50%</td><td style="padding:6px 8px;">建议补电</td></tr>
      <tr><td style="padding:6px 8px;">12.06 V</td><td style="padding:6px 8px;">约 25%</td><td style="padding:6px 8px;">已偏亏，尽快充电</td></tr>
      <tr><td style="padding:6px 8px;">≤ 11.90 V</td><td style="padding:6px 8px;">亏电</td><td style="padding:6px 8px;">冷启动困难，需充电或换电瓶</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔌 48V 轻混系统</h4>
      <p>轻混车型电池工作电压约 36~52 V，BSG/ISG 电机减速回收、加速助力，通过 DC-DC 转换器向 12V 电网供电。诊断时先确认 48V 侧电压区间正常，再排查 DC-DC 与 12V 回路。</p>
    </div>
    <div class="scene-card">
      <h4>📉 压降控制经验</h4>
      <p>12V 系统末端压降宜控制在 3% 以内（≤0.36 V）。例：10 A 负载流经 0.1 Ω 线阻压降即 1 V（8.3%），末端仅 11 V，大灯会明显变暗——应加粗线径、缩短走线并保证搭铁可靠。</p>
    </div>
    <div class="info-box">💡 充电电压在 13.8~14.8 V（冷车可更高）属正常；长期低于 13.5 V 或高于 15 V 需检查调节器与搭铁。</div>
  </div>'''

VO_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var volt=val('volt'),vreg=val('vreg'),cutin=val('cutin'),rpm=val('rpm');
  var vbat=val('vbat'),rloop=val('rloop');
  var load=val('load'),len=val('len'),area=val('area'),rho=val('mat');

  // ---- 发电电压：转速不足时按比例欠压，调节器封顶
  var ratio=cutin>0?rpm/cutin:1;
  var genV=vreg*Math.min(1,ratio);
  var limited=ratio>=1;

  // ---- 充电电流
  var chg=0, state='', stateCls='';
  if(genV>vbat){ chg=(genV-vbat)/Math.max(rloop,0.001); }
  if(chg>0){ state='充电中'; stateCls='ok'; }
  else if(Math.abs(genV-vbat)<0.05){ state='临界（不充不放）'; stateCls='warn'; }
  else { state='放电中（发电机欠压）'; stateCls='bad'; }

  // ---- 电池荷电状态
  var soc='';
  if(vbat>=12.66) soc='100%（满电）';
  else if(vbat>=12.45) soc='约 75%';
  else if(vbat>=12.24) soc='约 50%';
  else if(vbat>=12.06) soc='约 25%';
  else soc='亏电';

  // ---- 供电线路压降
  var Rs=rho*len/Math.max(area,0.01), Rd=Rs*2;
  var dU=load*Rd, pct=volt>0?dU/volt*100:0, endV=volt-dU;
  var lineJudge = pct<=3 ? '良好（≤3%）' : (pct<=5 ? '尚可（3%~5%）' : (pct<=8 ? '偏高（5%~8%）' : '过高（>8%）'));

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">发电机输出电压</div><div class="result-value">'+fmtNum(genV,1)+' V</div></div>'
    +'<div class="result-item"><div class="result-label">充电电流</div><div class="result-value">'+fmtNum(chg,1)+' A</div></div>'
    +'<div class="result-item"><div class="result-label">电池荷电状态</div><div class="result-value">'+soc+'</div></div>'
    +'<div class="result-item"><div class="result-label">末端电压</div><div class="result-value">'+fmtNum(endV,2)+' V</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>充电状态</h4><p>'+state+'（调节器'+(limited?'已达目标':'未达目标，转速不足')+'）</p></div>'
    +'<div class="dist-card"><h4>线路压降</h4><p>'+fmtNum(dU,2)+' V（'+fmtNum(pct,1)+'%）</p><p>'+lineJudge+'</p></div>'
    +'</div>';

  var rows='';
  var rl=[500,700,900,1200,1500,2000,2500,3000];
  for(var i=0;i<rl.length;i++){
    var r=rl[i], gv=vreg*Math.min(1,cutin>0?r/cutin:1);
    var ic=(gv>vbat)?(gv-vbat)/Math.max(rloop,0.001):0;
    rows+='<tr><td style="padding:5px 8px;">'+r+'</td><td style="padding:5px 8px;">'+fmtNum(gv,1)+'</td><td style="padding:5px 8px;">'+fmtNum(ic,1)+'</td><td style="padding:5px 8px;">'+(ic>1?'充电':(ic>0?'微弱充电':'不充电'))+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">发电电压 V<sub>gen</sub> = V<sub>reg</sub> × min(1, n / n<sub>cutin</sub>)</div>'
    +'<div class="formula-line">充电电流 I<sub>chg</sub> = (V<sub>gen</sub> − V<sub>bat</sub>) ÷ R<sub>loop</sub></div>'
    +'<div class="formula-line">线路压降 ΔU = I × ρ × 2L ÷ A（单程 L，双线计入 2L）</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">转速 (rpm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">发电电压 (V)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">充电电流 (A)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>';

  var ad='';
  if(!limited) ad+='<div class="tip-warn">⚠️ 当前转速低于切入转速，发电电压未达调节目标，怠速长时间使用大功率电器会消耗电池电量。</div>';
  if(chg>0 && chg<3) ad+='<div class="tip-warn">⚠️ 充电电流偏小，电池回充缓慢；若长期如此，检查皮带打滑、调节器与搭铁点。</div>';
  if(pct>5) ad+='<div class="tip-warn">⚠️ 线路压降 '+fmtNum(pct,1)+'%，末端仅 '+fmtNum(endV,2)+' V，建议加粗线径或缩短走线。</div>';
  if(genV>15.2) ad+='<div class="tip-warn">⚠️ 充电电压超过 15.2 V，可能过充，需检查调节器。</div>';
  if(vbat<12.06) ad+='<div class="tip-warn">⚠️ 电池电压 '+fmtNum(vbat,2)+' V 已属亏电，建议充电并做负载测试。</div>';
  if(!ad) ad='<div class="tip-info">✅ 当前转速下发电机输出正常，充电电流与线路压降均在合理范围。</div>';
  A.innerHTML=ad;
}
calc();'''

# -------------------------------------------------------- analysis-strength
AS_INPUTS = '''    <div class="input-row">
      <div><label>截面宽度 b (mm)</label><input type="number" id="b" value="60" oninput="calc()" min="1" step="1"></div>
      <div><label>截面高度 h (mm)</label><input type="number" id="h" value="120" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>跨度 L (mm)</label><input type="number" id="L" value="1000" oninput="calc()" min="1" step="10"></div>
      <div><label>集中载荷 F (N)</label><input type="number" id="F" value="5000" oninput="calc()" min="0" step="100"></div>
    </div>
    <div class="input-row">
      <div><label>材料</label>
        <select id="mat" onchange="calc()">
          <option value="235|206000|79000">Q235 钢（σs=235 MPa）</option>
          <option value="345|206000|79000">Q345 钢（σs=345 MPa）</option>
          <option value="355|206000|79000">45 钢（σs=355 MPa）</option>
          <option value="276|69000|26000">6061-T6 铝（σs=276 MPa）</option>
        </select>
      </div>
      <div><label>安全系数 n</label><input type="number" id="sf" value="1.5" oninput="calc()" min="1" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>施加扭矩 T (N·m，可填 0 跳过)</label><input type="number" id="T" value="2000" oninput="calc()" min="0" step="100"></div>
      <div><label>承载形式</label>
        <select id="beam" onchange="calc()">
          <option value="mid">简支梁·跨中集中载荷</option>
          <option value="uni">简支梁·均布载荷</option>
        </select>
      </div>
    </div>'''

AS_CARDS = '''  <div class="card">
    <h3>🧱 常用车架材料力学参数</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">材料</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">屈服强度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">弹性模量 E</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">切变模量 G</th>
      </tr>
      <tr><td style="padding:6px 8px;">Q235 钢</td><td style="padding:6px 8px;">235 MPa</td><td style="padding:6px 8px;">206 GPa</td><td style="padding:6px 8px;">79 GPa</td></tr>
      <tr><td style="padding:6px 8px;">Q345 钢</td><td style="padding:6px 8px;">345 MPa</td><td style="padding:6px 8px;">206 GPa</td><td style="padding:6px 8px;">79 GPa</td></tr>
      <tr><td style="padding:6px 8px;">45 钢</td><td style="padding:6px 8px;">355 MPa</td><td style="padding:6px 8px;">206 GPa</td><td style="padding:6px 8px;">79 GPa</td></tr>
      <tr><td style="padding:6px 8px;">6061-T6 铝</td><td style="padding:6px 8px;">276 MPa</td><td style="padding:6px 8px;">69 GPa</td><td style="padding:6px 8px;">26 GPa</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔩 弯曲与扭转的分工</h4>
      <p>乘用车更关注扭转刚度（影响操控与异响，单位 N·m/°），商用车与载货平台更关注弯曲刚度（抗垂向载荷）。两者共同决定车架在复杂受力下的变形量。</p>
    </div>
    <div class="scene-card">
      <h4>🧮 安全系数取值</h4>
      <p>许用应力 = 材料屈服强度 ÷ 安全系数，车架一般取 1.5~2.5。静态结构可按屈服控制；涉及疲劳的接头与焊点还需校核循环应力幅与 S-N 曲线。</p>
    </div>
    <div class="info-box">💡 本工具按等截面梁做快速估算，未计入焊缝削弱、开孔与应力集中；关键件建议用有限元复核并做台架试验。</div>
  </div>'''

AS_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var b=val('b'),hh=val('h'),L=val('L'),Fq=val('F');
  var mp=str('mat').split('|');
  var ys=parseFloat(mp[0]),E=parseFloat(mp[1]),Gm=parseFloat(mp[2]);
  var sf=val('sf'),T=val('T'),beam=str('beam');

  var I=b*Math.pow(hh,3)/12;          // mm^4
  var W=I/(hh/2);                     // mm^3
  var M, loadDesc;
  if(beam==='uni'){ M=Fq*L/8; loadDesc='均布载荷'; }
  else { M=Fq*L/4; loadDesc='跨中集中载荷'; }
  var sigma=M/W;                      // MPa
  var allow=ys/Math.max(sf,0.1);
  var realSF=sigma>0?ys/sigma:Infinity;
  var delta=(beam==='uni')?(5*Fq*Math.pow(L,3)/(384*E*I)):(Fq*Math.pow(L,3)/(48*E*I));

  var it=b*Math.pow(hh,3)/3*(1-0.63*Math.min(b,hh)/Math.max(b,hh));  // 扭转常数近似
  var Tmm=T*1000;
  var tau=(it>0)?Tmm*(Math.min(b,hh)/2)/it:0;
  var kJ=Gm*it/L;                     // N·mm/rad
  var kJdeg=kJ/1000*Math.PI/180;      // N·m/°（N·mm→N·m 除 1000）

  var st=sigma<=allow?'合格':(sigma<=ys?'裕度不足（超许用但未屈服）':'屈服风险'), cls=sigma<=allow?'ok':(sigma<=ys?'warn':'bad');

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">最大弯曲应力 σ</div><div class="result-value">'+fmtNum(sigma,2)+' MPa</div></div>'
    +'<div class="result-item"><div class="result-label">许用应力 [σ]</div><div class="result-value">'+fmtNum(allow,1)+' MPa</div></div>'
    +'<div class="result-item"><div class="result-label">实际安全系数</div><div class="result-value">'+ (isFinite(realSF)?fmtNum(realSF,2):'∞') +'</div></div>'
    +'<div class="result-item"><div class="result-label">校核结论</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>截面惯性矩 I</h4><p>'+fmtNum(I/1e6,3)+' ×10⁶ mm⁴</p><p>抗弯截面系数 W='+fmtNum(W/1e3,2)+' ×10³ mm³</p></div>'
    +'<div class="dist-card"><h4>最大弯矩 M</h4><p>'+fmtNum(M/1e6,3)+' kN·m</p><p>'+loadDesc+'</p></div>'
    +'<div class="dist-card"><h4>最大挠度 δ</h4><p>'+fmtNum(delta,3)+' mm</p><p>挠跨比 1/'+(delta>0?fmtNum(L/delta,0):'∞')+'</p></div>'
    +'<div class="dist-card"><h4>扭转刚度</h4><p>'+fmtNum(kJdeg,0)+' N·m/°</p><p>切应力 τ='+fmtNum(tau,1)+' MPa</p></div>'
    +'</div>';

  var rows='';
  var list=[0.5,0.75,1,1.25,1.5,2];
  for(var i=0;i<list.length;i++){
    var k=list[i], Mk=(beam==='uni')?Fq*k*L/8:Fq*k*L/4;
    var sk=Mk/W, sfk=sk>0?ys/sk:Infinity;
    rows+='<tr><td style="padding:5px 8px;">'+fmtNum(k*100,0)+'%</td><td style="padding:5px 8px;">'+fmtNum(k*Fq,0)+'</td><td style="padding:5px 8px;">'+fmtNum(sk,2)+'</td><td style="padding:5px 8px;">'+(isFinite(sfk)?fmtNum(sfk,2):'∞')+'</td><td style="padding:5px 8px;">'+(sk<=allow?'合格':(sk<=ys?'裕度不足':'屈服'))+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">惯性矩 I = b·h³ / 12；抗弯截面系数 W = I / (h/2)</div>'
    +'<div class="formula-line">最大弯矩 M = F·L / 4（跨中集中）或 q·L² / 8（均布）</div>'
    +'<div class="formula-line">弯曲应力 σ = M / W；许用应力 [σ] = σs / n</div>'
    +'<div class="formula-line">挠度 δ = F·L³ / (48EI)（跨中集中）或 5qL⁴ / (384EI)（均布）</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">载荷比例</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">载荷 (N)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">σ (MPa)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">安全系数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">结论</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 最大弯曲应力 '+fmtNum(sigma,2)+' MPa，安全系数 '+fmtNum(realSF,1)+'，高于设定值 '+fmtNum(sf,1)+'，弯曲强度满足要求。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 弯曲应力已超许用应力（安全系数仅 '+fmtNum(realSF,2)+'），建议加大截面高度 h 或改用高强材料。</div>';
  else ad+='<div class="tip-bad">⛔ 弯曲应力超过材料屈服强度，存在永久变形风险，必须重新设计截面。</div>';
  if(delta>L/300) ad+='<div class="tip-warn">⚠️ 挠跨比 1/'+fmtNum(L/delta,0)+' 超过 1/300，变形偏大，按刚度控制时应加大 I。</div>';
  if(T>0 && tau>ys*0.5) ad+='<div class="tip-warn">⚠️ 扭转切应力 '+fmtNum(tau,1)+' MPa 偏高，注意焊缝与接头处的应力集中。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='voltage-2', title='发电机电压调节', icon='🚗', accent='#0369a1',
         desc='输入发动机转速、发电机规格与电池状态，计算输出电压、充电电流与调节器工作状态。',
         inputs=VO_INPUTS, cards=VO_CARDS,
         notes='调节目标电压随温度补偿浮动，冷态与热态读数差异属正常',
         js=VO_JS),
    dict(slug='analysis-strength', title='车架（刚度/强度）分析', icon='🚙', accent='#475569',
         desc='输入车架几何与载荷参数估算关键部位的刚度与强度裕度，对比许用应力判断安全性，用于车架设计与改装的快速校核。',
         inputs=AS_INPUTS, cards=AS_CARDS,
         notes='等截面梁快速估算，未计入焊缝削弱与应力集中，关键件建议有限元复核',
         js=AS_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-18s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch6: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
