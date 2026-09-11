#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 重建 · 批次 7（内容与 SEO 元信息对齐修正）。

背景：批次 1~6 重建时 body 标题取自 deep-dive，与页面原有 <title>/<meta description>
口径不一致（如 wear-tire 的 head「轮胎磨损换位」vs body「轮胎磨损速率测算」）。重构后
需保证<title> 与 <h1> 一致、且正文主题与 desc 承诺相符。

本批处理（以页面原有 <title>/<desc> 为权威口径）：
  1. wear-tire        重做 body → 四轮磨损差异分析与换位方案（消除与 tire-wear 的重复）
  2. resistance-1     重做 body → 点火线圈初/次级电阻判定与匝数比估算
  3. temp-pressure-1  重做 body → 空调高低压侧压力诊断与检漏判断
  4. tire-pressure    标题对齐「汽车胎压参考计算器」（内容不变）
  5. oil-change       标题对齐「汽车保养周期计算器」并扩展为多项目保养周期
  6. wear-brake       body 保持「刹车盘磨损与更换」，校正 head title/desc（避免与
                      lifespan-brake「刹车片剩余寿命」重复）
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402
import rebuild_automotive_batch1 as B1  # 复用 tire-pressure / oil-change / wear-brake 既有定义

H = L.JS_HELPERS

# ======================================================== 1. wear-tire
WT_INPUTS = '''    <div class="input-row">
      <div><label>左前轮花纹深度 (mm)</label><input type="number" id="lf" value="5.2" oninput="calc()" min="0" step="0.1"></div>
      <div><label>右前轮花纹深度 (mm)</label><input type="number" id="rf" value="5.0" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>左后轮花纹深度 (mm)</label><input type="number" id="lr" value="6.8" oninput="calc()" min="0" step="0.1"></div>
      <div><label>右后轮花纹深度 (mm)</label><input type="number" id="rr" value="6.6" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>新胎花纹深度 (mm)</label><input type="number" id="newD" value="8" oninput="calc()" min="1" step="0.1"></div>
      <div><label>已行驶里程 (km)</label><input type="number" id="km" value="20000" oninput="calc()" min="0" step="500"></div>
    </div>
    <div class="input-row">
      <div><label>更换极限深度 (mm)</label><input type="number" id="minD" value="1.6" oninput="calc()" min="0" step="0.1"></div>
      <div><label>驱动形式</label>
        <select id="drive" onchange="calc()">
          <option value="ff">前驱（FF，前轮为主驱动）</option>
          <option value="fr">后驱（FR，后轮为主驱动）</option>
          <option value="awd">四驱（AWD/4WD）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>轮胎类型</label>
        <select id="single" onchange="calc()">
          <option value="no">对称/非对称花纹（可交叉换位）</option>
          <option value="yes">单向花纹（仅可前后换位）</option>
        </select>
      </div>
      <div><label>换位间隔参考 (km)</label><input type="number" id="interval" value="10000" oninput="calc()" min="1000" step="1000"></div>
    </div>'''

WT_CARDS = '''  <div class="card">
    <h3>🔄 常见换位方案</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">驱动形式</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">换位方式</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">前驱 FF</td><td style="padding:6px 8px;">前轮交叉、后轮直换</td><td style="padding:6px 8px;">左前→右后、右前→左后；后轮同侧上前</td></tr>
      <tr><td style="padding:6px 8px;">后驱 FR</td><td style="padding:6px 8px;">后轮交叉、前轮直换</td><td style="padding:6px 8px;">左后→右前、右后→左前；前轮同侧上后</td></tr>
      <tr><td style="padding:6px 8px;">四驱 AWD</td><td style="padding:6px 8px;">前后同侧互换</td><td style="padding:6px 8px;">或按厂家手册采用 X 型交叉</td></tr>
      <tr><td style="padding:6px 8px;">单向花纹</td><td style="padding:6px 8px;">仅前后互换</td><td style="padding:6px 8px;">交叉会反转滚动方向，影响排水与噪音</td></tr>
    </table>
    <div class="scene-card">
      <h4>📏 磨损差异判读</h4>
      <p>前后轴平均磨损差 ≥ 1.5 mm 建议换位；同轴左右差 ≥ 1.0 mm 多为胎压异常或四轮定位失准；四轮最大差异 ≥ 3 mm 说明磨损已不可逆，通常建议成对更换。</p>
    </div>
    <div class="scene-card">
      <h4>⏱️ 换位周期</h4>
      <p>常规建议每 8000~10000 km 或每两次保养换位一次；驱动轮磨损速率通常比从动轮高 20%~40%，定期换位可使四轮寿命趋于一致。</p>
    </div>
    <div class="info-box">💡 换位后需按车辆要求重新设定胎压监测（TPMS）位置并复紧螺栓，避免系统报错或安全隐患。</div>
  </div>'''

WT_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var lf=val('lf'),rf=val('rf'),lr=val('lr'),rr=val('rr');
  var nw=val('newD'),km=val('km'),mn=val('minD'),itv=val('interval');
  var drive=str('drive'),single=str('single');

  var names=['左前','右前','左后','右后'];
  var depth=[lf,rf,lr,rr];
  var wear=[nw-lf,nw-rf,nw-lr,nw-rr];
  var kmW=km>0?km/10000:0;
  var front=(wear[0]+wear[1])/2, rear=(wear[2]+wear[3])/2;
  var diffFR=Math.abs(wear[0]-wear[1]), diffLR=Math.abs(wear[2]-wear[3]);
  var frontD=(lf+rf)/2, rearD=(lr+rr)/2;
  var axisDiff=Math.abs(frontD-rearD);
  var maxW=Math.max(wear[0],wear[1],wear[2],wear[3]);
  var minW=Math.min(wear[0],wear[1],wear[2],wear[3]);
  var spread=maxW-minW;
  var maxAxisDiff=Math.max(diffFR,diffLR);

  // 各轮剩余里程
  var remain=[];
  for(var i=0;i<4;i++){
    var rate=kmW>0?wear[i]/kmW:0;
    remain.push(rate>0?Math.max(0,(depth[i]-mn))/rate*10000:Infinity);
  }
  var urgent=Math.min(remain[0],remain[1],remain[2],remain[3]);
  var urgentIdx=remain.indexOf(urgent);

  // 换位建议
  var needRot=axisDiff>=1.5||spread>=1.5;
  var plan='';
  if(single==='yes') plan='单向花纹：左前↔左后、右前↔右后（仅前后互换，不可交叉）';
  else if(drive==='ff') plan='前驱：左前→右后、右前→左后（交叉）；左后→左前、右后→右前（直换）';
  else if(drive==='fr') plan='后驱：左后→右前、右后→左前（交叉）；左前→左后、右前→右后（直换）';
  else plan='四驱：左前↔左后、右前↔右后（前后同侧互换，或按手册 X 型）';

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">后→前磨损差异</div><div class="result-value">'+fmtNum(Math.abs(front-rear),2)+' mm</div></div>'
    +'<div class="result-item"><div class="result-label">四轮最大差异</div><div class="result-value">'+fmtNum(spread,2)+' mm</div></div>'
    +'<div class="result-item"><div class="result-label">是否需要换位</div><div class="result-value">'+(needRot?'建议换位':'暂不需要')+'</div></div>'
    +'<div class="result-item"><div class="result-label">最先到限轮胎</div><div class="result-value">'+names[urgentIdx]+'（'+(isFinite(urgent)?fmtNum(urgent,0)+' km':'—')+'）</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>前后轴磨损</h4><p>前轴均 '+fmtNum(front,2)+' mm / 后轴均 '+fmtNum(rear,2)+' mm</p><p>差 '+fmtNum(Math.abs(front-rear),2)+' mm</p></div>'
    +'<div class="dist-card"><h4>同轴左右差</h4><p>前轴 '+fmtNum(diffFR,2)+' mm</p><p>后轴 '+fmtNum(diffLR,2)+' mm</p></div>'
    +'<div class="dist-card"><h4>推荐换位方案</h4><p style="font-size:12px;">'+plan+'</p></div>'
    +'<div class="dist-card"><h4>换位间隔</h4><p>'+fmtNum(itv,0)+' km</p><p>已行驶 '+fmtNum(km/itv,1)+' 个周期</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<4;i++){
    var rate=kmW>0?wear[i]/kmW:0;
    var st='';
    if(depth[i]<=mn) st='已达极限，必须更换';
    else if(depth[i]<=mn+1.5) st='注意，规划更换';
    else if(depth[i]<=4) st='一般';
    else st='良好';
    rows+='<tr><td style="padding:5px 8px;">'+names[i]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(depth[i],1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(wear[i],2)+'</td>'
      +'<td style="padding:5px 8px;">'+(rate>0?fmtNum(rate,2):'--')+'</td>'
      +'<td style="padding:5px 8px;">'+(isFinite(remain[i])?fmtNum(remain[i],0):'--')+'</td>'
      +'<td style="padding:5px 8px;">'+st+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">单轮磨损量 = 新胎深度 − 当前深度</div>'
    +'<div class="formula-line">轴平均磨损 = (左轮磨损 + 右轮磨损) ÷ 2</div>'
    +'<div class="formula-line">磨损速率 = 磨损量 ÷ 已行驶里程；剩余里程 = (当前深度 − 极限深度) ÷ 速率</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">轮胎</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">深度 (mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">磨损量 (mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">速率 (mm/万km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余里程 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>';

  var ad='';
  if(spread>=3) ad+='<div class="tip-bad">⛔ 四轮最大磨损差异 '+fmtNum(spread,2)+' mm（≥3 mm），磨损已不可逆，建议成对更换并做四轮定位。</div>';
  else if(needRot) ad+='<div class="tip-warn">⚠️ 前后磨损差 '+fmtNum(Math.abs(front-rear),2)+' mm，建议按上述方案换位，使四轮寿命趋于一致。</div>';
  else ad+='<div class="tip-info">✅ 四轮磨损较为均匀（最大差异 '+fmtNum(spread,2)+' mm），按每 '+fmtNum(itv,0)+' km 定期换位即可。</div>';
  if(maxAxisDiff>=1.0) ad+='<div class="tip-warn">⚠️ 同轴左右差达 '+fmtNum(maxAxisDiff,2)+' mm（≥1.0 mm），优先检查胎压一致性与四轮定位（前束/外倾）。</div>';
  if(depth[urgentIdx]<=mn) ad+='<div class="tip-bad">⛔ '+names[urgentIdx]+' 花纹深度 '+fmtNum(depth[urgentIdx],1)+' mm 已达更换极限，湿滑路面极易失控，须立即更换。</div>';
  A.innerHTML=ad;
}
calc();'''

# ==================================================== 2. resistance-1
RS_INPUTS = '''    <div class="input-row">
      <div><label>初级线圈电阻 (Ω)</label><input type="number" id="rp" value="0.8" oninput="calc()" min="0" step="0.1"></div>
      <div><label>次级线圈电阻 (kΩ)</label><input type="number" id="rs" value="8" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>测量温度 (℃)</label><input type="number" id="t" value="25" oninput="calc()" min="-30" step="1"></div>
      <div><label>点火线圈类型</label>
        <select id="type" onchange="calc()">
          <option value="0.3|1.5|5|15">独立点火 COP（初级 0.3~1.5 Ω / 次级 5~15 kΩ）</option>
          <option value="0.3|1.5|5|15">分组点火（废火花，同 COP 范围）</option>
          <option value="1.0|2.0|6|30">分电器式（初级 1.0~2.0 Ω / 次级 6~30 kΩ）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>实测次级是否导通</label>
        <select id="open" onchange="calc()">
          <option value="no">导通（有读数）</option>
          <option value="yes">开路（万用表 ∞）</option>
        </select>
      </div>
      <div><label>初级对地是否短路</label>
        <select id="sh" onchange="calc()">
          <option value="no">不短路</option>
          <option value="yes">对地导通（短路）</option>
        </select>
      </div>
    </div>'''

RS_CARDS = '''  <div class="card">
    <h3>📊 点火线圈电阻参考范围</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">类型</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">初级电阻</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">次级电阻</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型匝数比</th>
      </tr>
      <tr><td style="padding:6px 8px;">独立点火 COP</td><td style="padding:6px 8px;">0.3 ~ 1.5 Ω</td><td style="padding:6px 8px;">5 ~ 15 kΩ</td><td style="padding:6px 8px;">约 80:1 ~ 120:1</td></tr>
      <tr><td style="padding:6px 8px;">分组点火</td><td style="padding:6px 8px;">0.3 ~ 1.5 Ω</td><td style="padding:6px 8px;">5 ~ 15 kΩ</td><td style="padding:6px 8px;">约 80:1 ~ 120:1</td></tr>
      <tr><td style="padding:6px 8px;">分电器式</td><td style="padding:6px 8px;">1.0 ~ 2.0 Ω</td><td style="padding:6px 8px;">6 ~ 30 kΩ</td><td style="padding:6px 8px;">约 100:1</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔍 常见故障特征</h4>
      <p>次级电阻明显偏低（&lt; 4 kΩ）多为匝间短路，表现为高速失火、加速无力；次级开路或电阻骤高多为绕组烧断，对应缸直接不工作并报失火码（P030x）。</p>
    </div>
    <div class="scene-card">
      <h4>🌡️ 温度修正</h4>
      <p>铜绕组电阻随温度上升而增大，约 +0.393%/℃。热车测量值偏高属正常，比较时应统一折算到 20 ℃ 再对照标准范围。</p>
    </div>
    <div class="info-box">💡 电阻合格不代表点火能量正常：还需结合火花塞间隙、次级高压波形与失火计数综合判断。测量前先断电并拔下插头。</div>
  </div>'''

RS_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var rp=val('rp'),rs=val('rs'),t=val('t');
  var mp=str('type').split('|');
  var rpLo=parseFloat(mp[0]),rpHi=parseFloat(mp[1]),rsLo=parseFloat(mp[2]),rsHi=parseFloat(mp[3]);
  var open=str('open'), sh=str('sh');

  // 温度折算至 20℃（铜 +0.393%/℃）
  var k=1+0.00393*(t-20);
  var rp20=rp/k, rs20=rs/k;
  var ratio=Math.sqrt(rs20*1000/Math.max(rp20,0.001));   // 等效匝数比粗估

  var rpSt,rpCls;
  if(sh==='yes'||rp20<0.15){ rpSt='初级对地短路或阻值异常低'; rpCls='bad'; }
  else if(rp20<rpLo){ rpSt='初级电阻偏低（低于 '+fmtNum(rpLo,1)+' Ω）'; rpCls='warn'; }
  else if(rp20<=rpHi){ rpSt='初级正常'; rpCls='ok'; }
  else if(rp20<=rpHi*1.6){ rpSt='初级电阻偏高'; rpCls='warn'; }
  else { rpSt='初级断路或严重氧化'; rpCls='bad'; }

  var rsSt,rsCls;
  if(open==='yes'){ rsSt='次级开路（绕组烧断）'; rsCls='bad'; }
  else if(rs20<4){ rsSt='次级电阻偏低，疑似匝间短路'; rsCls='bad'; }
  else if(rs20<rsLo){ rsSt='次级略偏低'; rsCls='warn'; }
  else if(rs20<=rsHi){ rsSt='次级正常'; rsCls='ok'; }
  else if(rs20<=rsHi*1.5){ rsSt='次级偏高，绕组老化'; rsCls='warn'; }
  else { rsSt='次级电阻过高，接近断路'; rsCls='bad'; }

  var worst=(rpCls==='bad'||rsCls==='bad')?'存在明确故障':((rpCls==='warn'||rsCls==='warn')?'疑似异常':'判定正常');
  var cls=(rpCls==='bad'||rsCls==='bad')?'bad':((rpCls==='warn'||rsCls==='warn')?'warn':'ok');

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">初级电阻（20℃折算）</div><div class="result-value">'+fmtNum(rp20,2)+' Ω</div></div>'
    +'<div class="result-item"><div class="result-label">次级电阻（20℃折算）</div><div class="result-value">'+fmtNum(rs20,2)+' kΩ</div></div>'
    +'<div class="result-item"><div class="result-label">等效匝数比</div><div class="result-value">≈ '+fmtNum(ratio,0)+' : 1</div></div>'
    +'<div class="result-item"><div class="result-label">综合判定</div><div class="result-value">'+worst+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>初级状态</h4><p style="font-size:12px;">'+rpSt+'</p><p>标准 '+fmtNum(rpLo,1)+'~'+fmtNum(rpHi,1)+' Ω</p></div>'
    +'<div class="dist-card"><h4>次级状态</h4><p style="font-size:12px;">'+rsSt+'</p><p>标准 '+fmtNum(rsLo,0)+'~'+fmtNum(rsHi,0)+' kΩ</p></div>'
    +'<div class="dist-card"><h4>温度修正系数</h4><p>×'+fmtNum(k,3)+'（'+fmtNum(t,0)+'℃）</p><p>铜绕组 +0.393%/℃</p></div>'
    +'<div class="dist-card"><h4>次级输出电压估算</h4><p>≈ '+fmtNum(350*ratio/1000,0)+' kV</p><p>按初级断电反电动势 350 V 估算</p></div>'
    +'</div>';

  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">温度折算：R<sub>20</sub> = R<sub>t</sub> ÷ [1 + 0.00393 × (t − 20)]</div>'
    +'<div class="formula-line">等效匝数比：N ≈ √(R<sub>次级</sub> ÷ R<sub>初级</sub>)（按电阻开方粗估）</div>'
    +'<div class="formula-line">判定区间：初级 '+fmtNum(rpLo,1)+'~'+fmtNum(rpHi,1)+' Ω；次级 '+fmtNum(rsLo,0)+'~'+fmtNum(rsHi,0)+' kΩ</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">测量温度</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">折算系数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">初级折算 (Ω)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">次级折算 (kΩ)</th></tr>'
    +[0,20,40,60,80].map(function(tv){
        var kk=1+0.00393*(tv-20);
        return '<tr><td style="padding:5px 8px;">'+tv+' ℃</td><td style="padding:5px 8px;">'+fmtNum(kk,3)+'</td>'
          +'<td style="padding:5px 8px;">'+fmtNum(rp/kk,2)+'</td><td style="padding:5px 8px;">'+fmtNum(rs/kk,2)+'</td></tr>';
      }).join('')
    +'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 初/次级电阻均在标准范围内，线圈绕组本体正常。若仍失火，请检查火花塞、点火模块与线束插接件。</div>';
  if(cls==='warn') ad+='<div class="tip-warn">⚠️ 检测到阻值偏离标准范围，建议与同型正常线圈对比测量确认后再更换。</div>';
  if(cls==='bad') ad+='<div class="tip-bad">⛔ 存在短路或断路特征，点火线圈已失效，建议更换并同时检查火花塞间隙与点火模块，避免新线圈二次损坏。</div>';
  if(t<10||t>60) ad+='<div class="tip-warn">⚠️ 测量温度 '+fmtNum(t,0)+' ℃ 偏离常温，折算值误差增大，建议冷车（20~30 ℃）复测。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================== 3. temp-pressure-1
TP_INPUTS = '''    <div class="input-row">
      <div><label>低压侧压力 (MPa)</label><input type="number" id="lp" value="0.18" oninput="calc()" min="0" step="0.01"></div>
      <div><label>高压侧压力 (MPa)</label><input type="number" id="hp" value="1.35" oninput="calc()" min="0" step="0.01"></div>
    </div>
    <div class="input-row">
      <div><label>环境温度 (℃)</label><input type="number" id="amb" value="30" oninput="calc()" min="-10" step="1"></div>
      <div><label>出风口温度 (℃)</label><input type="number" id="vent" value="8" oninput="calc()" min="-30" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>压缩机状态</label>
        <select id="comp" onchange="calc()">
          <option value="on">已吸合运转</option>
          <option value="off">未吸合/不运转</option>
        </select>
      </div>
      <div><label>制冷剂类型</label>
        <select id="ref" onchange="calc()">
          <option value="r134a">R134a</option>
          <option value="r1234yf">R1234yf（压力近似 R134a）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>冷凝器散热</label>
        <select id="cond" onchange="calc()">
          <option value="ok">风扇运转、表面清洁</option>
          <option value="fan">冷凝风扇不转</option>
          <option value="dirty">冷凝器脏堵</option>
        </select>
      </div>
      <div><label>静态压力 (MPa，停机 30min 后)</label><input type="number" id="stat" value="0" oninput="calc()" min="0" step="0.01"></div>
    </div>'''

TP_CARDS = '''  <div class="card">
    <h3>📈 制冷系统标准压力区间（R134a）</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">环境温度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">低压侧</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">高压侧</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">出风口温度</th>
      </tr>
      <tr><td style="padding:6px 8px;">20 ℃</td><td style="padding:6px 8px;">0.12 ~ 0.22 MPa</td><td style="padding:6px 8px;">1.00 ~ 1.50 MPa</td><td style="padding:6px 8px;">4 ~ 10 ℃</td></tr>
      <tr><td style="padding:6px 8px;">25 ℃</td><td style="padding:6px 8px;">0.15 ~ 0.25 MPa</td><td style="padding:6px 8px;">1.20 ~ 1.70 MPa</td><td style="padding:6px 8px;">5 ~ 12 ℃</td></tr>
      <tr><td style="padding:6px 8px;">30 ℃</td><td style="padding:6px 8px;">0.18 ~ 0.28 MPa</td><td style="padding:6px 8px;">1.35 ~ 1.90 MPa</td><td style="padding:6px 8px;">7 ~ 14 ℃</td></tr>
      <tr><td style="padding:6px 8px;">35 ℃</td><td style="padding:6px 8px;">0.20 ~ 0.32 MPa</td><td style="padding:6px 8px;">1.50 ~ 2.10 MPa</td><td style="padding:6px 8px;">8 ~ 16 ℃</td></tr>
      <tr><td style="padding:6px 8px;">40 ℃</td><td style="padding:6px 8px;">0.23 ~ 0.35 MPa</td><td style="padding:6px 8px;">1.65 ~ 2.30 MPa</td><td style="padding:6px 8px;">10 ~ 18 ℃</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔎 高低压组合诊断</h4>
      <p>低压低 + 高压低 → 制冷剂不足或泄漏；低压低 + 高压高 → 膨胀阀或管路堵塞；低压高 + 高压高 → 制冷剂过量或散热不良；高低压接近平衡且偏低 → 压缩机不作功。</p>
    </div>
    <div class="scene-card">
      <h4>🫧 检漏方法</h4>
      <p>常用手段：电子检漏仪沿管路接头、冷凝器、蒸发器、压缩机轴封巡检；关阀保压观测压力衰减；冷媒加荧光剂后紫外灯照射。静态压力与环境温度对应关系可用来判断系统是否存在明显缺失。</p>
    </div>
    <div class="info-box">💡 压力须在发动机 1500~2000 rpm、鼓风机中高档、内循环、车门关闭的稳定工况下读取；出风口与环境温差达 8~12 ℃ 属正常。</div>
  </div>'''

TP_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var lp=val('lp'),hp=val('hp'),amb=val('amb'),vent=val('vent'),stat=val('stat');
  var comp=str('comp'),cond=str('cond');

  // 标准区间按环境温度线性插值
  var T=[20,25,30,35,40];
  var LPL=[0.12,0.15,0.18,0.20,0.23], LPH=[0.22,0.25,0.28,0.32,0.35];
  var HPL=[1.00,1.20,1.35,1.50,1.65], HPH=[1.50,1.70,1.90,2.10,2.30];
  function interp(arr,x){
    if(x<=T[0]) return arr[0];
    if(x>=T[4]) return arr[4];
    for(var i=0;i<4;i++){
      if(x>=T[i]&&x<=T[i+1]){
        var k=(x-T[i])/(T[i+1]-T[i]);
        return arr[i]+(arr[i+1]-arr[i])*k;
      }
    }
    return arr[4];
  }
  var lpLo=interp(LPL,amb), lpHi=interp(LPH,amb);
  var hpLo=interp(HPL,amb), hpHi=interp(HPH,amb);

  var lpMid=(lpLo+lpHi)/2, hpMid=(hpLo+hpHi)/2;
  var lpOK=(lp>=lpLo&&lp<=lpHi), hpOK=(hp>=hpLo&&hp<=hpHi);
  var lpH=lp>lpHi, lpL=lp<lpLo, hpH=hp>hpHi, hpL=hp<hpLo;
  var pr=lp>0.01?hp/lp:0;

  var diag,cls='ok';
  if(comp==='off'){ diag='压缩机未吸合，压力无法判定。请先检查离合继电器、压力开关与冷媒量。'; cls='warn'; }
  else if(lpL&&hpL){ diag='制冷剂不足或系统泄漏：高低压同时偏低，常见于冷媒缺失、管路渗漏。建议检漏并补充冷媒。'; cls='bad'; }
  else if(lpL&&hpH){ diag='膨胀阀堵塞或管路节流：低压偏低而高压偏高，需检查膨胀阀开度与管路是否冰堵、脏堵。'; cls='bad'; }
  else if(lpH&&hpH){ diag='制冷剂过量或冷凝散热不良：高低压同时偏高，先清洗冷凝器并确认风扇运转，再回收多余冷媒。'; cls='bad'; }
  else if(lpOK&&hpH){ diag='冷凝器散热不足：低压正常但高压偏高，多为冷凝风扇不转、冷凝器脏堵或水箱散热片堵塞。'; cls='warn'; }
  else if(lpH&&hpOK){ diag='压缩机效率下降或膨胀阀开度过大：低压偏高，建议结合吸排气压力与出风温度进一步判断。'; cls='warn'; }
  else if(lpOK&&hpOK){ diag='高低压均在标准区间，系统运行正常。'; cls='ok'; }
  else { diag='读数处于临界区间，建议在稳定工况下复测并与出风口温差交叉验证。'; cls='warn'; }

  var dT=amb-vent;
  var coolTxt = dT>=8 ? ('正常（温差 '+fmtNum(dT,1)+' ℃）') : (dT>=5 ? ('偏弱（温差 '+fmtNum(dT,1)+' ℃）') : ('明显不足（温差 '+fmtNum(dT,1)+' ℃）'));

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">低压侧判定</div><div class="result-value">'+(lpOK?'正常':(lpL?'偏低':'偏高'))+'</div></div>'
    +'<div class="result-item"><div class="result-label">高压侧判定</div><div class="result-value">'+(hpOK?'正常':(hpL?'偏低':'偏高'))+'</div></div>'
    +'<div class="result-item"><div class="result-label">压力比</div><div class="result-value">'+fmtNum(pr,1)+' : 1</div></div>'
    +'<div class="result-item"><div class="result-label">制冷效果</div><div class="result-value">'+coolTxt+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>低压标准区间</h4><p>'+fmtNum(lpLo,2)+' ~ '+fmtNum(lpHi,2)+' MPa</p><p>实测 '+fmtNum(lp,2)+' MPa</p></div>'
    +'<div class="dist-card"><h4>高压标准区间</h4><p>'+fmtNum(hpLo,2)+' ~ '+fmtNum(hpHi,2)+' MPa</p><p>实测 '+fmtNum(hp,2)+' MPa</p></div>'
    +'<div class="dist-card"><h4>与环境温度偏差</h4><p>低压 '+fmtNum(lp-lpMid,2)+' MPa</p><p>高压 '+fmtNum(hp-hpMid,2)+' MPa</p></div>'
    +'<div class="dist-card"><h4>静态压力</h4><p>'+(stat>0?fmtNum(stat,2)+' MPa':'未填')+'</p><p>参考 ≈ '+fmtNum(0.4+0.0135*Math.max(amb,0),2)+' MPa @ '+fmtNum(amb,0)+'℃</p></div>'
    +'</div>';

  var rows='';
  for(var i=0;i<5;i++){
    rows+='<tr><td style="padding:5px 8px;">'+T[i]+' ℃</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(LPL[i],2)+' ~ '+fmtNum(LPH[i],2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(HPL[i],2)+' ~ '+fmtNum(HPH[i],2)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(HPL[i]/LPH[i],1)+' ~ '+fmtNum(HPH[i]/LPL[i],1)+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 判定口径</div>'
    +'<div class="formula-line">标准区间按环境温度线性插值（依据 R134a 制冷系统经验区间）</div>'
    +'<div class="formula-line">压力比 = 高压侧 ÷ 低压侧，正常约 5:1 ~ 9:1</div>'
    +'<div class="formula-line">制冷效果温差 = 环境温度 − 出风口温度，正常 8~12 ℃</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">环境温度</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">低压 (MPa)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">高压 (MPa)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">压力比</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ '+diag+'</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ '+diag+'</div>';
  else ad+='<div class="tip-bad">⛔ '+diag+'</div>';
  if(cond==='fan') ad+='<div class="tip-warn">⚠️ 冷凝风扇不转会直接推高高压侧压力，须先修复风扇再判断冷媒量是否正常。</div>';
  if(cond==='dirty') ad+='<div class="tip-warn">⚠️ 冷凝器脏堵导致散热能力下降，清洗后高压可下降 0.2~0.4 MPa。</div>';
  if(pr>0 && (pr<4||pr>10)) ad+='<div class="tip-warn">⚠️ 压力比 '+fmtNum(pr,1)+' 偏离 5~9 的常规区间，压缩机效率或膨胀阀开度可能异常。</div>';
  if(dT<5) ad+='<div class="tip-warn">⚠️ 出风口与环境温差仅 '+fmtNum(dT,1)+' ℃，制冷效果不足，请结合压力与风量排查。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================== 4/5/6 标题与 head 校正
# oil-change 扩展：多项目保养周期参考表（对齐 head「汽车保养周期计算器」+ desc 承诺）
OIL_EXTRA_CARD = '''  <div class="card">
    <h3>🗓️ 整车保养项目周期参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">保养项目</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">里程周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">时间周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">备注</th>
      </tr>
      <tr><td style="padding:6px 8px;">机油 + 机油滤芯</td><td style="padding:6px 8px;">5000 ~ 10000 km</td><td style="padding:6px 8px;">6 ~ 12 个月</td><td style="padding:6px 8px;">按机油类型，本页主算</td></tr>
      <tr><td style="padding:6px 8px;">空气滤芯</td><td style="padding:6px 8px;">15000 ~ 20000 km</td><td style="padding:6px 8px;">12 个月</td><td style="padding:6px 8px;">多尘环境减半</td></tr>
      <tr><td style="padding:6px 8px;">空调滤芯</td><td style="padding:6px 8px;">15000 ~ 20000 km</td><td style="padding:6px 8px;">12 个月</td><td style="padding:6px 8px;">雾霾重地区 6 个月</td></tr>
      <tr><td style="padding:6px 8px;">汽油滤芯</td><td style="padding:6px 8px;">30000 ~ 40000 km</td><td style="padding:6px 8px;">24 个月</td><td style="padding:6px 8px;">外置式周期更短</td></tr>
      <tr><td style="padding:6px 8px;">刹车油</td><td style="padding:6px 8px;">40000 km</td><td style="padding:6px 8px;">24 个月</td><td style="padding:6px 8px;">含水量 &gt;3% 即换</td></tr>
      <tr><td style="padding:6px 8px;">防冻液</td><td style="padding:6px 8px;">60000 km</td><td style="padding:6px 8px;">48 个月</td><td style="padding:6px 8px;">长效型可 10 年</td></tr>
      <tr><td style="padding:6px 8px;">火花塞</td><td style="padding:6px 8px;">30000 ~ 60000 km</td><td style="padding:6px 8px;">—</td><td style="padding:6px 8px;">铱金可 80000 km</td></tr>
      <tr><td style="padding:6px 8px;">变速箱油</td><td style="padding:6px 8px;">60000 ~ 80000 km</td><td style="padding:6px 8px;">48 个月</td><td style="padding:6px 8px;">AT/CVT 差异大</td></tr>
      <tr><td style="padding:6px 8px;">正时皮带</td><td style="padding:6px 8px;">60000 ~ 100000 km</td><td style="padding:6px 8px;">60 个月</td><td style="padding:6px 8px;">断带损失大，宜提前</td></tr>
    </table>
    <div class="info-box">💡 上述为通用参考区间，涡轮增压、拥堵短途、多尘或高寒工况应整体缩短 20%~30%；以随车保养手册为准。</div>
  </div>'''

TOOLS = [
    dict(slug='wear-tire', title='轮胎磨损换位', icon='🔘', accent='#4b5563',
         desc='输入四个轮胎的花纹深度与行驶里程，分析磨损差异，推荐换位方案与更换时间。',
         inputs=WT_INPUTS, cards=WT_CARDS,
         notes='花纹深度须在胎面主沟槽多点测量取最小值，测量前清除沟槽内石子',
         js=WT_JS),
    dict(slug='resistance-1', title='点火线圈电阻判断', icon='⚡', accent='#b45309',
         desc='输入初级与次级线圈电阻值，对照标准范围判断点火线圈是否正常，并估算匝数比。',
         inputs=RS_INPUTS, cards=RS_CARDS,
         notes='须断电并拔下插头测量，热车读数应折算至 20 ℃ 再对照标准值',
         js=RS_JS),
    dict(slug='temp-pressure-1', title='空调压缩机检漏', icon='🌡️', accent='#7c3aed',
         desc='输入空调高低压侧压力读数与环境温度，判断汽车制冷系统运行状态、制冷剂是否泄漏或过量，适用于维修诊断与日常检漏。',
         inputs=TP_INPUTS, cards=TP_CARDS,
         notes='压力须在发动机 1500~2000 rpm、鼓风机中高档的稳定工况下读取',
         js=TP_JS),
    # 标题对齐（复用 batch1 既有实现，仅更换页面标题口径）
    dict(slug='tire-pressure', title='汽车胎压参考计算器', icon='⚙️', accent='#0f766e',
         desc='按车门标贴标准胎压，结合载重与季节核算目标胎压，并对比实测值给出补放气建议。',
         inputs=B1.TIRE_INPUTS, cards=B1.TIRE_CARDS,
         notes='胎压须在冷胎状态测量，热胎读数不能直接对照标贴标准',
         js=B1.TIRE_JS),
    dict(slug='oil-change', title='汽车保养周期计算器', icon='🔧', accent='#b45309',
         desc='汽车保养周期计算器，估算机油机滤空滤变速箱油等保养间隔与费用参考，辅助养车规划。',
         inputs=B1.OIL_CHANGE_INPUTS, cards=B1.OIL_CHANGE_CARDS + '\n' + OIL_EXTRA_CARD,
         notes='里程与时间先到为准，严苛工况即使里程未到也应按时间上限更换',
         js=B1.OIL_CHANGE_JS),
    # wear-brake：body 保持刹车盘口径，纠正 head title/desc（避免与 lifespan-brake 重复）
    dict(slug='wear-brake', title='刹车盘磨损与更换', icon='🛑', accent='#b91c1c',
         desc='按盘厚、MIN 极限与跳动量判断刹车盘能否继续使用，并估算剩余可磨寿命。',
         inputs=B1.BRAKE_INPUTS, cards=B1.BRAKE_CARDS,
         notes='厚度须多点实测取最小值，跳动量须用百分表测量，不可目视替代',
         js=B1.BRAKE_JS,
         strict_subs=False,
         head_subs=[
             ('刹车片磨损限度', '刹车盘磨损与更换'),
             ('刹车盘磨损限度', '刹车盘磨损与更换'),
             ('输入刹车片当前厚度、新品厚度、磨损极限与使用里程，评估安全状态与剩余使用寿命。',
              '输入刹车盘当前厚度、标准盘厚与 MIN 极限，结合跳动量判断能否继续使用并估算剩余可磨寿命。'),
         ]),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-18s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch7: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
