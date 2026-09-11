#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 4（calc-2 / calc-3 / calc-5 / calc-72 / drive）。

calc-2 发动机功率扭矩换算；calc-3 轮胎胎压单位换算；calc-5 制动减速度与制动距离；
calc-72 发动机排量与压缩比；drive 变速器齿比与车速。算例数字均按各页 deep-dive
示例口径实现，并经 node 实跑复核。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# -------------------------------------------------------------------- calc-2
C2_INPUTS = '''    <div class="input-row">
      <div><label>发动机扭矩 (N·m)</label><input type="number" id="tq" value="250" oninput="calc()" min="0" step="any"></div>
      <div><label>对应转速 (rpm)</label><input type="number" id="rpm" value="4000" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>已知功率 (kW，可留空)</label><input type="number" id="kw" value="" oninput="calc()" min="0" step="any"></div>
      <div><label>反推转速 (rpm，留空按上行)</label><input type="number" id="rpm2" value="" oninput="calc()" min="0" step="any"></div>
    </div>'''

C2_CARDS = '''  <div class="card">
    <h3>📖 功率单位与换算系数</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">单位</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">定义</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">使用地区</th>
      </tr>
      <tr><td style="padding:6px 8px;">kW 千瓦</td><td style="padding:6px 8px;">国际单位制功率</td><td style="padding:6px 8px;">中国大陆、欧洲参数表</td></tr>
      <tr><td style="padding:6px 8px;">PS 公制马力</td><td style="padding:6px 8px;">1PS = 735.5W</td><td style="padding:6px 8px;">德系、日系部分标注</td></tr>
      <tr><td style="padding:6px 8px;">hp 英制马力</td><td style="padding:6px 8px;">1hp = 745.7W</td><td style="padding:6px 8px;">美系、英制市场</td></tr>
    </table>
    <div class="scene-card">
      <h4>↔️ 换算关系</h4>
      <p>1kW ≈ 1.360PS ≈ 1.341hp；1PS ≈ 0.7355kW；1hp ≈ 0.7457kW。三者相差约 1%~2%，对比不同市场车型时务必统一单位。</p>
    </div>
    <div class="scene-card">
      <h4>📈 扭矩与功率的关系</h4>
      <p>功率 = 扭矩 × 角速度。同一扭矩下转速越高功率越大，因此最大功率点总出现在高转速区，而最大扭矩点多在中等转速。</p>
    </div>
    <div class="info-box">💡 厂家标注的峰值功率与峰值扭矩往往不在同一转速，比较动力时应同时看「数值 + 对应转速区间」。</div>
  </div>'''

C2_JS = H + '''
var K_PS=1.35962, K_HP=1.34102;
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var tq=val('tq'),rpm=val('rpm');
  var kwIn=parseFloat(document.getElementById('kw').value);
  var rpm2=parseFloat(document.getElementById('rpm2').value);
  var kw,ps,hp,usedRpm;
  if(!isNaN(kwIn)&&kwIn>0){
    kw=kwIn; usedRpm=(!isNaN(rpm2)&&rpm2>0)?rpm2:rpm;
    tq=(usedRpm>0)?kw*9550/usedRpm:NaN;
  } else {
    if(isNaN(tq)||isNaN(rpm)||rpm<=0){
      R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入扭矩与转速，或直接输入功率</div>';
      G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
    }
    usedRpm=rpm;
    kw=tq*2*Math.PI*rpm/60/1000;
  }
  ps=kw*K_PS; hp=kw*K_HP;
  R.innerHTML='<div class="safe-val">'+fmtNum(kw,1)+' kW</div>'+
    '<div class="safe-sub">'+fmtNum(ps,0)+' PS · '+fmtNum(hp,0)+' hp · 扭矩 '+fmtNum(tq,1)+' N·m @ '+fmtNum(usedRpm,0)+' rpm</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(kw,1)+'</div><div class="l">功率 (kW)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(ps,0)+'</div><div class="l">功率 (PS 公制)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(hp,0)+'</div><div class="l">功率 (hp 英制)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(tq,1)+'</div><div class="l">扭矩 (N·m)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(usedRpm,0)+'</div><div class="l">对应转速 (rpm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(tq*2*Math.PI*usedRpm/60/1000/(kw>0?kw:1)*100,0)+'%</div><div class="l">功率构成校验</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">功率 P(kW) = 扭矩 T(N·m) × 2π × 转速 n(rpm) ÷ 60 ÷ 1000</div>'+
    '<div class="fb-row">反推扭矩 T = 9550 × P(kW) ÷ n(rpm)</div>'+
    '<div class="fb-row">PS = kW × 1.35962；hp = kW × 1.34102</div>'+
    '<div class="fb-row">本次：'+fmtNum(tq,1)+' N·m @ '+fmtNum(usedRpm,0)+' rpm → '+fmtNum(kw,2)+' kW</div>';
  A.innerHTML='<div class="tip-info">ℹ️ 峰值功率出现在高转速区、峰值扭矩在中低转速区，两者不可互换表述。改装后实测轮上功率通常为标定功率的 85%~92%（传动损耗）。</div>';
}
calc();'''

# -------------------------------------------------------------------- calc-3
C3_UNITS = {'bar': 100.0, 'psi': 6.894757, 'kpa': 1.0, 'kgcm2': 98.0665}

C3_INPUTS = '''    <div class="input-row">
      <div><label>胎压数值</label><input type="number" id="pv" value="2.3" oninput="calc()" min="0" step="any"></div>
      <div><label>输入单位</label><select id="unit" onchange="calc()">
        <option value="bar" selected>bar（欧系常用）</option>
        <option value="psi">psi（美规常用）</option>
        <option value="kpa">kPa</option>
        <option value="kgcm2">kg/cm²</option>
      </select></div>
    </div>
    <div class="input-row">
      <div><label>换算目标（留空显示全部）</label><select id="target" onchange="calc()">
        <option value="all" selected>全部单位</option>
        <option value="bar">bar</option>
        <option value="psi">psi</option>
        <option value="kpa">kPa</option>
        <option value="kgcm2">kg/cm²</option>
      </select></div>
      <div><label>冷胎 / 热胎读数切换</label><select id="temp" onchange="calc()">
        <option value="cold" selected>冷胎（标准值）</option>
        <option value="hot">热胎（行驶后）</option>
      </select></div>
    </div>'''

C3_CARDS = '''  <div class="card">
    <h3>📖 四种胎压单位换算表</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">基准</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">psi</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">kPa</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">kg/cm²</th>
      </tr>
      <tr><td style="padding:6px 8px;">1 bar</td><td style="padding:6px 8px;">14.5038</td><td style="padding:6px 8px;">100</td><td style="padding:6px 8px;">1.0197</td></tr>
      <tr><td style="padding:6px 8px;">1 psi</td><td style="padding:6px 8px;">1</td><td style="padding:6px 8px;">6.8948</td><td style="padding:6px 8px;">0.0703</td></tr>
      <tr><td style="padding:6px 8px;">1 kPa</td><td style="padding:6px 8px;">0.1450</td><td style="padding:6px 8px;">1</td><td style="padding:6px 8px;">0.0102</td></tr>
      <tr><td style="padding:6px 8px;">1 kg/cm²</td><td style="padding:6px 8px;">14.2233</td><td style="padding:6px 8px;">98.0665</td><td style="padding:6px 8px;">1</td></tr>
    </table>
    <div class="scene-card">
      <h4>❄️ 冷胎才是标准</h4>
      <p>行驶后胎温升高，胎压可比冷态高 0.2~0.3 bar（3~4 psi）。所有标准值均指冷胎（停车 3 小时以上或行驶不足 2km）。</p>
    </div>
    <div class="scene-card">
      <h4>🔧 气泵单位陷阱</h4>
      <p>便携气泵多显示 psi 或 bar，加油站的数显充气机可能显示 kPa。换算后再充，避免把 2.3bar 当成 2.3psi 或 230psi。</p>
    </div>
    <div class="info-box">💡 单位换算只解决读数口径，具体该充多少仍须以本车车门框标贴或手册建议值为准。</div>
  </div>'''

C3_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var pv=val('pv'),u=str('unit'),target=str('target'),temp=str('temp');
  if(isNaN(pv)||pv<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的胎压数值</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var map={bar:100,psi:6.894757,kpa:1,kgcm2:98.0665};
  var kpaVal=pv*map[u];
  var bar=kpaVal/100, psi=kpaVal/6.894757, kpa=kpaVal, kgcm2=kpaVal/98.0665;
  var note=(temp==='hot')?'热胎读数':(temp==='cold'?'冷胎读数':('冷胎读数'));
  var main=(target==='all')?bar:(kpaVal/map[target]);
  R.innerHTML='<div class="safe-val">'+fmtNum(kpaVal/map[target==='all'?'bar':target],2)+' '+((target==='all')?'bar':target)+'</div>'+
    '<div class="safe-sub">'+note+' · 基准 '+fmtNum(kpaVal,1)+' kPa</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(bar,2)+'</div><div class="l">bar</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(psi,1)+'</div><div class="l">psi</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(kpa,1)+'</div><div class="l">kPa</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(kgcm2,2)+'</div><div class="l">kg/cm²</div></div>';
  F.innerHTML=
    '<div class="fb-title">换算关系</div>'+
    '<div class="fb-row">1 bar = 100 kPa = 14.5038 psi ≈ 1.0197 kg/cm²</div>'+
    '<div class="fb-row">1 psi = 6.8948 kPa；1 kg/cm² = 98.0665 kPa</div>'+
    '<div class="fb-row">统一换算路径：先归一到 kPa，再换算到目标单位</div>'+
    '<div class="fb-row">本次：'+fmtNum(pv,2)+' '+u+' = '+fmtNum(kpaVal,1)+' kPa</div>';
  var ad='<div class="tip-info">ℹ️ 标准胎压指冷胎值。热胎测得偏高 0.2~0.3 bar 属正常，不应按热胎读数放气至标准值。</div>';
  if(u==='psi'&&pv<15){ ad+='<div class="tip-warn">⚠️ 输入的 psi 数值偏小，家用车常见为 28~36 psi，请确认单位是否选错。</div>'; }
  if(u==='bar'&&pv>5){ ad+='<div class="tip-warn">⚠️ 输入的 bar 数值偏大，家用车常见为 2.1~2.5 bar，请确认是否把 psi 当成了 bar。</div>'; }
  A.innerHTML=ad;
}
calc();'''

# -------------------------------------------------------------------- calc-5
C5_INPUTS = '''    <div class="input-row">
      <div><label>碰撞前车速 (km/h)</label><input type="number" id="v" value="100" oninput="calc()" min="0" step="any"></div>
      <div><label>制动痕迹长度 (m)</label><input type="number" id="s" value="40" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>路面类型（决定附着系数 μ）</label><select id="road" onchange="calc()">
        <option value="1.0">干燥沥青 μ≈1.0</option>
        <option value="0.8">干燥水泥 μ≈0.8</option>
        <option value="0.6" selected>潮湿沥青 μ≈0.6</option>
        <option value="0.3">压实雪 μ≈0.3</option>
        <option value="0.1">结冰 μ≈0.1</option>
      </select></div>
      <div><label>重力加速度 g (m/s²)</label><input type="number" id="g" value="9.81" oninput="calc()" min="1" step="0.01"></div>
    </div>'''

C5_CARDS = '''  <div class="card">
    <h3>📖 附着系数与制动距离参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">路面</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">附着系数 μ</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">100km/h 制动距离</th>
      </tr>
      <tr><td style="padding:6px 8px;">干燥沥青</td><td style="padding:6px 8px;">0.9 ~ 1.1</td><td style="padding:6px 8px;">约 36 ~ 44 m</td></tr>
      <tr><td style="padding:6px 8px;">潮湿沥青</td><td style="padding:6px 8px;">0.5 ~ 0.7</td><td style="padding:6px 8px;">约 56 ~ 79 m</td></tr>
      <tr><td style="padding:6px 8px;">压实雪</td><td style="padding:6px 8px;">0.2 ~ 0.4</td><td style="padding:6px 8px;">约 98 ~ 197 m</td></tr>
      <tr><td style="padding:6px 8px;">结冰</td><td style="padding:6px 8px;">0.05 ~ 0.15</td><td style="padding:6px 8px;">约 262 ~ 787 m</td></tr>
    </table>
    <div class="scene-card">
      <h4>📐 制动距离与初速平方成正比</h4>
      <p>车速翻倍，制动距离约变 4 倍。因此高速行驶时必须按「车速平方」放大安全车距，而非线性加长。</p>
    </div>
    <div class="scene-card">
      <h4>🧮 事故还原怎么用</h4>
      <p>现场测得制动痕迹长度 s 与路面 μ，即可反推碰撞前车速 v=√(2μgs)。实际还原需扣减痕迹起止误差并考虑 ABS 拖痕特征。</p>
    </div>
    <div class="info-box">💡 本工具计算的是「物理极限减速度」，未含驾驶员反应时间。实际停车总距离还应加上反应距离（车速 × 反应时间）。</div>
  </div>'''

C5_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var v=val('v'),s=val('s'),mu=parseFloat(str('road')),g=val('g');
  if(isNaN(v)||v<=0||isNaN(g)||g<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效车速</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var vms=v/3.6;
  var limitA=mu*g;
  var limitS=vms*vms/(2*limitA);
  var a=(!isNaN(s)&&s>0)?(vms*vms/(2*s)):limitA;
  var usedS=(!isNaN(s)&&s>0)?s:limitS;
  var gVal=a/g;
  var util=(limitA>0)?(a/limitA*100):0;
  var reachV=Math.sqrt(2*mu*g*(usedS>0?usedS:0))*3.6;
  R.innerHTML='<div class="safe-val">减速度 '+fmtNum(a,2)+' m/s²</div>'+
    '<div class="safe-sub">等效 '+fmtNum(gVal,2)+' g · 附着利用率 '+fmtNum(util,0)+'%</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(a,2)+'</div><div class="l">减速度 (m/s²)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(gVal,2)+'</div><div class="l">等效 g 值</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(usedS,1)+'</div><div class="l">制动距离 (m)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(limitA,2)+'</div><div class="l">路面极限减速度 (m/s²)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(limitS,1)+'</div><div class="l">该路面理论最短距离 (m)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(reachV,0)+'</div><div class="l">痕迹长度对应车速 (km/h)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">由初速与距离求减速度：a = v² ÷ (2s)</div>'+
    '<div class="fb-row">由路面附着系数求减速度：a = μ × g</div>'+
    '<div class="fb-row">等效 g 值 = a ÷ g；附着利用率 = a ÷ (μ × g)</div>'+
    '<div class="fb-row">由痕迹反推车速：v = √(2 × μ × g × s)</div>'+
    '<div class="fb-row">本次：初速 '+fmtNum(v,0)+' km/h（'+fmtNum(vms,2)+' m/s）、痕迹 '+fmtNum(usedS,1)+' m</div>';
  var ad='';
  if(util>105){ ad='<div class="tip-warn">⚠️ 计算减速度超过该路面附着极限（利用率 '+fmtNum(util,0)+'%），说明痕迹长度或车速数据存在偏差，或现场并非单一路面。</div>'; }
  else if(util>=90){ ad='<div class="tip-success">✅ 制动接近附着极限（利用率 '+fmtNum(util,0)+'%），说明驾驶员已采取全力制动，路面附着力被充分利用。</div>'; }
  else{ ad='<div class="tip-info">ℹ️ 附着利用率 '+fmtNum(util,0)+'%，低于该路面极限，可能存在制动不及时、制动系统衰减或痕迹测量偏差。</div>'; }
  ad+='<div class="tip-info">ℹ️ 未计入反应时间：若按 1 秒反应计，'+fmtNum(v,0)+' km/h 下还需额外增加约 '+fmtNum(vms,1)+' m 的反应距离。</div>';
  A.innerHTML=ad;
}
calc();'''

# ------------------------------------------------------------------- calc-72
C72_INPUTS = '''    <div class="input-row">
      <div><label>缸径 B (mm)</label><input type="number" id="bore" value="86" oninput="calc()" min="0" step="0.1"></div>
      <div><label>行程 S (mm)</label><input type="number" id="stroke" value="86" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>气缸数</label><input type="number" id="cyl" value="4" oninput="calc()" min="1" step="1"></div>
      <div><label>燃烧室容积 Vc (cm³)</label><input type="number" id="vc" value="56" oninput="calc()" min="0.1" step="0.1"></div>
    </div>'''

C72_CARDS = '''  <div class="card">
    <h3>📖 压缩比与燃油标号对照</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">压缩比区间</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型机型</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议标号</th>
      </tr>
      <tr><td style="padding:6px 8px;">9.0 ~ 10.0</td><td style="padding:6px 8px;">早期自然吸气</td><td style="padding:6px 8px;">92 号</td></tr>
      <tr><td style="padding:6px 8px;">10.0 ~ 11.5</td><td style="padding:6px 8px;">主流自然吸气</td><td style="padding:6px 8px;">92 ~ 95 号</td></tr>
      <tr><td style="padding:6px 8px;">11.5 ~ 13.0</td><td style="padding:6px 8px;">高压缩比自吸 / 混动</td><td style="padding:6px 8px;">95 ~ 98 号</td></tr>
      <tr><td style="padding:6px 8px;">涡轮增压</td><td style="padding:6px 8px;">1.5T / 2.0T</td><td style="padding:6px 8px;">95 号及以上</td></tr>
    </table>
    <div class="scene-card">
      <h4>⚙️ 排量怎么算</h4>
      <p>单缸排量 = π/4 × 缸径² × 行程。缸径与行程相等称「方形缸」，缸径大于行程称「短行程」（利于高转速），反之称「长行程」（利于低扭）。</p>
    </div>
    <div class="scene-card">
      <h4>🔥 压缩比与爆震</h4>
      <p>压缩比越高，混合气受压升温越剧烈，越易发生爆震，需更高辛烷值抑制。涡轮增压还会进一步提高有效压缩比，故标号要求更严。</p>
    </div>
    <div class="info-box">💡 铣缸盖、换薄缸垫或换活塞都会改变燃烧室容积，从而改变压缩比，改装后务必复算并与燃油标号匹配。</div>
  </div>'''

C72_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var B=val('bore'),S=val('stroke'),cyl=Math.round(val('cyl')),vc=val('vc');
  if(isNaN(B)||isNaN(S)||isNaN(cyl)||B<=0||S<=0||cyl<1){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的缸径、行程与缸数</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var vOne=Math.PI/4*B*B*S;
  var vOneCm3=vOne/1000;
  var total=vOneCm3*cyl/1000;
  var cr=(!isNaN(vc)&&vc>0)?((vc+vOneCm3)/vc):0;
  var ratio=(S>0)?(B/S):0;
  var layout=(Math.abs(B-S)<2)?'方形缸（缸径≈行程）':(B>S?'短行程（偏高速）':'长行程（偏低扭）');
  R.innerHTML='<div class="safe-val">总排量 ≈ '+fmtNum(total,2)+' L</div>'+
    '<div class="safe-sub">单缸 '+fmtNum(vOneCm3,1)+' cm³ · 压缩比 '+(cr>0?fmtNum(cr,2)+':1':'--')+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(vOneCm3,1)+'</div><div class="l">单缸排量 (cm³)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(total*1000,0)+'</div><div class="l">总排量 (cm³)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(total,2)+'</div><div class="l">总排量 (L)</div></div>'+
    '<div class="dist-card"><div class="v">'+(cr>0?fmtNum(cr,2):'--')+'</div><div class="l">压缩比</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(Math.PI/4*B*B/100,1)+'</div><div class="l">活塞面积 (cm²)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(ratio,2)+'</div><div class="l">缸径行程比 B/S</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">单缸排量 Vs = π/4 × 缸径² × 行程</div>'+
    '<div class="fb-row">总排量 = 单缸排量 × 气缸数</div>'+
    '<div class="fb-row">压缩比 CR =（燃烧室容积 + 单缸排量）÷ 燃烧室容积</div>'+
    '<div class="fb-row">本次：缸径 '+fmtNum(B,1)+' × 行程 '+fmtNum(S,1)+' mm、'+cyl+' 缸 → 总排量 '+fmtNum(total,2)+' L</div>';
  var ad='<div class="tip-info">ℹ️ 结构类型：'+layout+'。</div>';
  if(cr>0){
    if(cr>11.5){ ad+='<div class="tip-warn">⚠️ 压缩比 '+fmtNum(cr,2)+':1 偏高，通常需 95~98 号汽油抑制爆震，勿随意降标。</div>'; }
    else if(cr>=10){ ad+='<div class="tip-info">ℹ️ 压缩比 '+fmtNum(cr,2)+':1 属主流自吸水平，一般 92~95 号汽油即可，以厂家标注为准。</div>'; }
    else{ ad+='<div class="tip-success">✅ 压缩比 '+fmtNum(cr,2)+':1 较低，92 号汽油即可满足要求。</div>'; }
  }
  ad+='<div class="tip-info">ℹ️ 排量只决定基础进气量，实际动力还受增压、进排气效率与调校影响，1.5T 常可超越 2.0L 自吸。</div>';
  A.innerHTML=ad;
}
calc();'''

# --------------------------------------------------------------------- drive
DRIVE_INPUTS = '''    <div class="input-row">
      <div><label>档位齿比</label><input type="number" id="gear" value="3.5" oninput="calc()" min="0.1" step="0.01"></div>
      <div><label>终传比（主减速比）</label><input type="number" id="final" value="4.1" oninput="calc()" min="0.1" step="0.01"></div>
    </div>
    <div class="input-row">
      <div><label>轮胎周长 (m)</label><input type="number" id="circ" value="2.0" oninput="calc()" min="0.1" step="0.01"></div>
      <div><label>发动机转速 (rpm)</label><input type="number" id="rpm" value="6000" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>发动机扭矩 (N·m，可留空)</label><input type="number" id="tq" value="200" oninput="calc()" min="0" step="any"></div>
      <div><label>传动效率 (%)</label><input type="number" id="eff" value="90" oninput="calc()" min="1" max="100" step="1"></div>
    </div>'''

DRIVE_CARDS = '''  <div class="card">
    <h3>📖 齿比与车速关系</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">参数</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">增大后影响</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型取向</th>
      </tr>
      <tr><td style="padding:6px 8px;">档位齿比</td><td style="padding:6px 8px;">轮端扭矩增大、同转速车速降低</td><td style="padding:6px 8px;">低档位大齿比，利于起步爬坡</td></tr>
      <tr><td style="padding:6px 8px;">终传比</td><td style="padding:6px 8px;">各档车速整体下降、加速变强</td><td style="padding:6px 8px;">越野/载重偏大，巡航偏小</td></tr>
      <tr><td style="padding:6px 8px;">轮胎周长</td><td style="padding:6px 8px;">周长变大则同转速车速变快</td><td style="padding:6px 8px;">换大尺寸轮胎需重算车速表</td></tr>
    </table>
    <div class="scene-card">
      <h4>↗️ 密齿比与疏齿比</h4>
      <p>密齿比档间跨度小，换挡平顺、发动机常处高效区，利于加速与节油；疏齿比结构简单、低速有劲但高速转速偏高。</p>
    </div>
    <div class="scene-card">
      <h4>🔁 换大轮胎的代价</h4>
      <p>轮胎周长增大后实际车速高于仪表读数，同时轮端扭矩下降、加速变弱，里程表与油耗计算也会偏差。</p>
    </div>
    <div class="info-box">💡 总减速比 = 档位齿比 × 终传比。车速由「发动机转速 × 轮胎周长 ÷ 总减速比」决定，与发动机功率无关。</div>
  </div>'''

DRIVE_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var gear=val('gear'),fin=val('final'),circ=val('circ'),rpm=val('rpm');
  var tq=parseFloat(document.getElementById('tq').value), eff=val('eff');
  if(isNaN(gear)||isNaN(fin)||isNaN(circ)||isNaN(rpm)||gear<=0||fin<=0||circ<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的齿比、周长与转速</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var total=gear*fin;
  var vms=rpm*circ/total/60;
  var kmh=vms*3.6;
  var wheelTq=(!isNaN(tq)&&tq>0)?tq*total*(eff>0?eff/100:1):0;
  var ratio100=total;
  R.innerHTML='<div class="safe-val">'+fmtNum(kmh,1)+' km/h</div>'+
    '<div class="safe-sub">总减速比 '+fmtNum(total,2)+' @ '+fmtNum(rpm,0)+' rpm'+(wheelTq>0?' · 轮端扭矩 '+fmtNum(wheelTq,0)+' N·m':'')+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(total,2)+'</div><div class="l">总减速比</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(kmh,1)+'</div><div class="l">车速 (km/h)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(vms,2)+'</div><div class="l">车速 (m/s)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(rpm*circ/total,0)+'</div><div class="l">轮胎转速 (rpm)</div></div>'+
    '<div class="dist-card"><div class="v">'+(wheelTq>0?fmtNum(wheelTq,0):'--')+'</div><div class="l">轮端扭矩 (N·m)</div></div>'+
    '<div class="dist-card"><div class="v">'+(wheelTq>0?fmtNum(wheelTq/(circ/2/Math.PI/1000),0):'--')+'</div><div class="l">轮端驱动力 (N)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">总减速比 = 档位齿比 × 终传比</div>'+
    '<div class="fb-row">车速 (m/s) = 发动机转速 × 轮胎周长 ÷ 总减速比 ÷ 60</div>'+
    '<div class="fb-row">车速 (km/h) = 车速 (m/s) × 3.6</div>'+
    '<div class="fb-row">轮端扭矩 = 发动机扭矩 × 总减速比 × 传动效率</div>'+
    '<div class="fb-row">本次：'+fmtNum(gear,2)+' × '+fmtNum(fin,2)+' = '+fmtNum(total,2)+'，'+fmtNum(rpm,0)+' rpm 对应 '+fmtNum(kmh,1)+' km/h</div>';
  var ad='<div class="tip-info">ℹ️ 车速只取决于「转速 × 周长 ÷ 总减速比」，与发动机功率无关；功率决定能维持该转速多久（加速能力与极速上限）。</div>';
  if(kmh>180){ ad+='<div class="tip-info">ℹ️ 该齿比组合下理论车速较高，需确认轮胎速度等级与车辆极速限制。</div>'; }
  if(total>5){ ad+='<div class="tip-info">ℹ️ 总减速比 '+fmtNum(total,2)+' 偏大（多为一档或加大终传），起步爬坡有力但同速转速偏高。</div>'; }
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='calc-2', title='发动机功率/扭矩换算', icon='⚙️', accent='#0f766e',
         desc='在 kW、PS、hp 之间换算功率，并由扭矩与转速计算功率或反推扭矩，校核厂家参数。',
         inputs=C2_INPUTS, cards=C2_CARDS,
         notes='换算系数为国际标准值，各厂商标注口径可能略有取整差异',
         js=C2_JS),
    dict(slug='calc-3', title='轮胎胎压换算', icon='🧮', accent='#7c3aed',
         desc='在 bar、psi、kPa、kg/cm² 之间换算胎压，适配不同气压计单位，支持冷胎与热胎读数提示。',
         inputs=C3_INPUTS, cards=C3_CARDS,
         notes='标准胎压指冷胎读数，热胎测量值偏高 0.2~0.3bar 属正常',
         js=C3_JS),
    dict(slug='calc-5', title='制动减速度计算', icon='🛑', accent='#b91c1c',
         desc='由初速与制动痕迹长度计算减速度与等效 g 值，或按路面附着系数推算理论制动距离。',
         inputs=C5_INPUTS, cards=C5_CARDS,
         notes='结果为物理极限值，未含驾驶员反应时间，事故还原须结合现场实测',
         js=C5_JS),
    dict(slug='calc-72', title='发动机排量压缩比计算', icon='🔧', accent='#1e40af',
         desc='由缸径、行程、缸数与燃烧室容积计算单缸排量、总排量与压缩比，并提示燃油标号匹配。',
         inputs=C72_INPUTS, cards=C72_CARDS,
         notes='压缩比计算需准确测量燃烧室容积，改装后应复算并与燃油标号匹配',
         js=C72_JS),
    dict(slug='drive', title='变速器齿比计算', icon='🔁', accent='#1565c0',
         desc='由档位齿比、终传比、轮胎周长与转速计算车速与轮端扭矩，理解齿比对加速与极速的影响。',
         inputs=DRIVE_INPUTS, cards=DRIVE_CARDS,
         notes='理论车速未计入轮胎滑移与变形，实际车速以 GPS 实测为准',
         js=DRIVE_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-16s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch4: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
