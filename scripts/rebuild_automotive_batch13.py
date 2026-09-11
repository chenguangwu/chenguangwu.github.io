#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 13（收尾：calc-1）。

calc-1 此前为残缺页（仅有 formula-box 与 deep-dive/opt 区块，无任何输入控件与结果区，不可用），
本批按「汽车百公里加速时间估算」口径完整重建。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

C1_INPUTS = '''    <div class="input-row">
      <div><label>整车质量 (kg)</label><input type="number" id="m" value="1500" oninput="calc()" min="300" max="4000" step="50"></div>
      <div><label>发动机最大功率 (kW)</label><input type="number" id="P" value="130" oninput="calc()" min="20" max="1200" step="5"></div>
    </div>
    <div class="input-row">
      <div><label>峰值扭矩 (N·m)</label><input type="number" id="T" value="250" oninput="calc()" min="50" max="1600" step="10"></div>
      <div><label>一档总传动比（含主减）</label><input type="number" id="i" value="12" oninput="calc()" min="3" max="25" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>轮胎滚动半径 (m)</label><input type="number" id="r" value="0.32" oninput="calc()" min="0.2" max="0.55" step="0.01"></div>
      <div><label>传动效率 (%)</label><input type="number" id="eff" value="88" oninput="calc()" min="60" max="100" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>风阻 CdA (m²)</label><input type="number" id="cda" value="0.65" oninput="calc()" min="0.2" max="2" step="0.05"></div>
      <div><label>驱动形式</label>
        <select id="drv" onchange="calc()">
          <option value="0.55" selected>前驱（加速时前轴载荷下降）</option>
          <option value="0.58">后驱（加速时后轴载荷增加）</option>
          <option value="0.95">四驱（四轮共同附着）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>轮胎附着系数 μ</label><input type="number" id="mu" value="0.9" oninput="calc()" min="0.3" max="1.4" step="0.05"></div>
      <div><label>换挡次数 / 单次换挡耗时 (s)</label>
        <input type="number" id="sh" value="2" oninput="calc()" min="0" max="6" step="1" style="width:46%;display:inline-block;">
        <input type="number" id="st" value="0.35" oninput="calc()" min="0" max="1.5" step="0.05" style="width:46%;display:inline-block;margin-left:6px;">
      </div>
    </div>'''

C1_CARDS = '''  <div class="card">
    <h3>📊 比功率与加速能力对照</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">比功率 (kW/t)</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">0–100 km/h 量级</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">对应车型</th>
      </tr>
      <tr><td style="padding:6px 8px;">≤ 60</td><td style="padding:6px 8px;">12 s 以上</td><td style="padding:6px 8px;">经济型小车、微面</td></tr>
      <tr><td style="padding:6px 8px;">60 ~ 80</td><td style="padding:6px 8px;">10 ~ 12 s</td><td style="padding:6px 8px;">家用紧凑型轿车</td></tr>
      <tr><td style="padding:6px 8px;">80 ~ 100</td><td style="padding:6px 8px;">8 ~ 10 s</td><td style="padding:6px 8px;">主流中型轿车</td></tr>
      <tr><td style="padding:6px 8px;">100 ~ 130</td><td style="padding:6px 8px;">6 ~ 8 s</td><td style="padding:6px 8px;">2.0T 中型车、性能取向 SUV</td></tr>
      <tr><td style="padding:6px 8px;">130 ~ 180</td><td style="padding:6px 8px;">5 ~ 6 s</td><td style="padding:6px 8px;">性能车、双电机电车</td></tr>
      <tr><td style="padding:6px 8px;">≥ 180</td><td style="padding:6px 8px;">4 s 以内</td><td style="padding:6px 8px;">高性能跑车、高性能电车</td></tr>
    </table>
    <p style="font-size:12px;color:var(--text-secondary,#6b7280);">上表为行业惯例量级（官方公布或实测口径），用于快速定位动力水平；本工具按两段模型计算，结果是同一组参数下的相对比较值，与官方成绩可能因测试条件不同而有差异。</p>
    <div class="scene-card">
      <h4>⚙️ 两段式加速模型</h4>
      <p>车速较低时受峰值扭矩与传动比限制（扭矩段），加速度基本恒定；车速升高后发动机进入功率限制区（功率段），加速度随车速上升而下降，因为 a = P ÷ (m·v)。本工具用两段模型分别积分，比单一的「平均加速度」估算更接近实测。</p>
    </div>
    <div class="scene-card">
      <h4>🛞 为什么大马力前驱车反而慢</h4>
      <p>驱动轮能传递的纵向力受附着条件限制：F ≤ μ·N，N 为驱动轮载荷。加速时载荷向后转移，前驱车前轴载荷下降，一档起步很容易打滑、甚至出现扭矩转向；后驱与四驱能把更多载荷压到驱动轮上，同样的动力能更充分地用于加速。</p>
    </div>
    <div class="scene-card">
      <h4>📉 功率提升的边际效应</h4>
      <p>本模型固定一档传动比与附着条件，因此功率大幅提升后瓶颈会转移到牵引力与附着力上——再加大马力，加速时间也难有明显改善。实际高性能车会相应加大一档传动比、加宽轮胎并优化驱动轮载荷分配，这也是「马力翻倍、成绩未必减半」的原因。</p>
    </div>
    <div class="info-box">💡 电动车在起步即输出最大扭矩，扭矩段更宽，因此同比功率下 0–100 km/h 通常比燃油车快；但高速段受电机功率与减速比限制，后段加速会明显减弱。</div>
  </div>'''

C1_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var m=val('m'), P=val('P'), T=val('T'), i=val('i'), r=val('r');
  var eff=val('eff'), cda=val('cda'), drv=val('drv'), mu=val('mu');
  var sh=val('sh'), st=val('st');

  var v=100/3.6;                       // 目标末速 m/s
  var g=9.81, rho=1.225, fr=0.012;
  var Pw=P*(eff/100)*1000;             // 轮端功率 W
  var Fmax=(r>0)?T*i*(eff/100)/r:0;    // 一档轮端最大驱动力 N
  var Froll=m*g*fr;                    // 滚动阻力 N

  // 扭矩段：净驱动力 = Fmax − 滚动阻力
  var a1=(Fmax-Froll)/m;
  var v1=(Fmax>0)?Math.min(v, Pw/Fmax):0;   // 扭矩段结束车速
  // 附着限制
  var aT=mu*g*drv;
  var slip=a1>aT;
  if(slip) a1=aT;
  var t1=(a1>0.01)?v1/a1:Infinity;

  // 功率段：数值积分 ∫dv/a(v)
  var t2=0, ok=true;
  if(v>v1){
    var n=240, dv=(v-v1)/n;
    for(var j=0;j<n;j++){
      var vm=v1+(j+0.5)*dv;
      var Fd=Pw/vm - Froll - 0.5*rho*cda*vm*vm;
      var a=Fd/m;
      if(a<=0.005){ ok=false; break; }
      t2+=dv/a;
    }
  }
  var tShift=sh*st;
  var total=ok?(t1+t2+tShift):Infinity;
  var aAvg=isFinite(total)&&total>0?v/total:0;
  var pwPer=m>0?P/(m/1000):0;          // 比功率 kW/t
  var Fnet=Fmax-Froll;

  var st_,cls;
  if(!ok){ st_='动力不足，无法达到 100 km/h'; cls='bad'; }
  else if(slip){ st_='起步受附着限制（打滑）'; cls='warn'; }
  else { st_='估算完成'; cls='ok'; }

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">0–100 km/h</div><div class="result-value">'+(isFinite(total)?fmtNum(total,2)+' s':'—')+'</div></div>'
    +'<div class="result-item"><div class="result-label">平均加速度</div><div class="result-value">'+fmtNum(aAvg,2)+' m/s²</div></div>'
    +'<div class="result-item"><div class="result-label">比功率</div><div class="result-value">'+fmtNum(pwPer,1)+' kW/t</div></div>'
    +'<div class="result-item"><div class="result-label">判定</div><div class="result-value">'+st_+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>扭矩段</h4><p>0 ~ '+fmtNum(v1*3.6,1)+' km/h</p><p>用时 '+fmtNum(t1,2)+' s，a='+fmtNum(a1,2)+' m/s²</p></div>'
    +'<div class="dist-card"><h4>功率段</h4><p>'+fmtNum(v1*3.6,1)+' ~ 100 km/h</p><p>用时 '+fmtNum(t2,2)+' s</p></div>'
    +'<div class="dist-card"><h4>换挡损失</h4><p>'+fmtNum(sh,0)+' 次 × '+fmtNum(st,2)+' s</p><p>合计 '+fmtNum(tShift,2)+' s</p></div>'
    +'<div class="dist-card"><h4>附着上限</h4><p>'+fmtNum(aT,2)+' m/s²</p><p>'+(slip?'实际受此限制':'未触发打滑')+'</p></div>'
    +'</div>';

  var rows='';
  var ps=[60,90,120,150,180,220,300];
  for(var k=0;k<ps.length;k++){
    var Pk=ps[k]*(eff/100)*1000;
    var ak=(Fmax-Froll)/m;
    var v1k=(Fmax>0)?Math.min(v,Pk/Fmax):0;
    if(ak>aT) ak=aT;
    var tk=(ak>0.01)?v1k/ak:Infinity;
    var t2k=0, okk=true;
    if(v>v1k){
      var nn=160, dvv=(v-v1k)/nn;
      for(var j2=0;j2<nn;j2++){
        var vmk=v1k+(j2+0.5)*dvv;
        var Fdk=Pk/vmk-Froll-0.5*rho*cda*vmk*vmk;
        var akk=Fdk/m;
        if(akk<=0.005){ okk=false; break; }
        t2k+=dvv/akk;
      }
    }
    var tk2=okk?(tk+t2k+tShift):Infinity;
    var pw=ps[k]/(m/1000);
    rows+='<tr><td style="padding:5px 8px;">'+ps[k]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(pw,1)+'</td>'
      +'<td style="padding:5px 8px;">'+(isFinite(tk2)?fmtNum(tk2,2):'达不到')+'</td>'
      +'<td style="padding:5px 8px;">'+(isFinite(tk2)?fmtNum(v/tk2,2):'—')+'</td>'
      +'<td style="padding:5px 8px;">'+(Pk/1000>P?'+':'')+fmtNum(Pk/1000-P,0)+' kW</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">轮端功率 Pw = 发动机功率 × 传动效率；轮端最大驱动力 Fmax = 峰值扭矩 × 一档传动比 × 效率 ÷ 滚动半径</div>'
    +'<div class="formula-line">扭矩段（v ≤ Pw/Fmax）：a₁ = (Fmax − F_roll) ÷ m，加速度近似恒定</div>'
    +'<div class="formula-line">功率段：a(v) = [Pw ÷ v − F_roll − 0.5·ρ·CdA·v²] ÷ m，按数值积分求时间</div>'
    +'<div class="formula-line">滚动阻力 F_roll = m·g·f_r（f_r ≈ 0.012）；附着上限 a ≤ μ·g·驱动轮载荷比</div>'
    +'<div class="formula-line">总时间 = 扭矩段 + 功率段 + 换挡次数 × 单次换挡耗时</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">功率 (kW)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">比功率</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">0–100 (s)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">平均 a</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">vs 当前</th></tr>'
    +rows+'</table>';

  var ad='';
  if(!ok) ad+='<div class="tip-bad">⛔ 在给定参数下，'+(Fmax/1000).toFixed(1)+' kN 的轮端驱动力与阻力在 100 km/h 前已平衡，加速无法完成，请核对功率、传动比与轮胎半径。</div>';
  else if(slip) ad+='<div class="tip-warn">⚠️ 一档驱动力产生的加速度 '+fmtNum((Fmax-Froll)/m,2)+' m/s² 超过附着上限 '+fmtNum(aT,2)+' m/s²，起步阶段轮胎会打滑，实际加速时间比理论值更长且难以稳定复现。建议改善驱动轮载荷分配或使用更高附着轮胎。</div>';
  else ad+='<div class="tip-info">✅ 估算 0–100 km/h 约 '+fmtNum(total,2)+' s（扭矩段 '+fmtNum(t1,2)+' s + 功率段 '+fmtNum(t2,2)+' s + 换挡 '+fmtNum(tShift,2)+' s），比功率 '+fmtNum(pwPer,1)+' kW/t。</div>';
  if(isFinite(total)&&total<7&&!slip) ad+='<div class="tip-info">🚀 该动力水平下加速能力较强，注意起步时的轮胎与传动系统负荷。</div>';
  if(isFinite(total)&&total>12) ad+='<div class="tip-warn">🐢 加速偏慢，超车并线时需预留更长距离，建议提前降挡拉高转速。</div>';
  ad+='<div class="tip-info">📌 官方公布的 0–100 km/h 多在理想路面、弹射起步并取最好成绩，本估算包含了滚动阻力、空气阻力与换挡中断，通常比官方值更接近日常实测。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='calc-1', title='汽车百公里加速时间估算', icon='🏁', accent='#0369a1',
         desc='输入整车质量、功率、传动比与轮胎参数，按扭矩段与功率段两段模型估算 0–100 km/h 加速时间，并给出打滑判定与不同功率对照。',
         inputs=C1_INPUTS, cards=C1_CARDS,
         notes='估算已计入滚动阻力、空气阻力与换挡中断；起步若超出附着上限会打滑，实际时间更长',
         js=C1_JS),
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
    print('---- batch13: %d/%d ----' % (ok, total))


if __name__ == '__main__':
    main()
