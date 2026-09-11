#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 12（收尾批）。

tester-11                   电池 CCA 与内阻健康度测试
time-maintenance            保养计划计算（十项内容，时间维度）
traffic-fine-calculator     违章罚款与记分计算（数据源：公安部令第163号 + 道交法）
xuanguatanhuangzunitexing   悬挂弹簧阻尼特性（固有频率/阻尼比）
说明：tester-11 的 deep-dive 原为「尾气与 OBD 排放检测」，与页面（电池测试）不符，另由 fix 脚本同步。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# =============================================================== tester-11
TB_INPUTS = '''    <div class="input-row">
      <div><label>标称冷启动电流 CCA (A)</label><input type="number" id="cca0" value="600" oninput="calc()" min="100" max="1500" step="10"></div>
      <div><label>实测冷启动电流 CCA (A)</label><input type="number" id="cca" value="510" oninput="calc()" min="0" max="1500" step="10"></div>
    </div>
    <div class="input-row">
      <div><label>实测内阻 (mΩ)</label><input type="number" id="res" value="7.2" oninput="calc()" min="0.1" max="60" step="0.1"></div>
      <div><label>测试时电瓶温度 (℃)</label><input type="number" id="temp" value="25" oninput="calc()" min="-20" max="60" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>电瓶类型</label>
        <select id="type" onchange="calc()">
          <option value="1.0" selected>普通铅酸（富液）</option>
          <option value="1.08">EFB 启停电池</option>
          <option value="1.15">AGM 启停电池</option>
        </select>
      </div>
      <div><label>电瓶已使用 (月)</label><input type="number" id="age" value="42" oninput="calc()" min="0" max="120" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>车辆排量 (L)</label><input type="number" id="disp" value="2.0" oninput="calc()" min="0.6" max="6" step="0.1"></div>
      <div><label>发动机类型</label>
        <select id="eng" onchange="calc()">
          <option value="1.0" selected>汽油自然吸气</option>
          <option value="1.15">汽油涡轮增压</option>
          <option value="1.35">柴油</option>
        </select>
      </div>
    </div>'''

TB_CARDS = '''  <div class="card">
    <h3>🔋 电瓶检测要点</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">指标</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">含义</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">判定参考</th>
      </tr>
      <tr><td style="padding:6px 8px;">CCA 实测 / 标称</td><td style="padding:6px 8px;">冷启动能力健康度 SOH</td><td style="padding:6px 8px;">≥90% 良好；70%~90% 预警；&lt;70% 更换</td></tr>
      <tr><td style="padding:6px 8px;">内阻</td><td style="padding:6px 8px;">极板硫化与连接劣化程度</td><td style="padding:6px 8px;">高于参考值 30% 需关注</td></tr>
      <tr><td style="padding:6px 8px;">静态电压</td><td style="padding:6px 8px;">荷电状态 SOC</td><td style="padding:6px 8px;">12.6 V 以上满电；12.2 V 约 50%</td></tr>
    </table>
    <div class="scene-card">
      <h4>🌡️ 温度对内阻的影响</h4>
      <p>铅酸电池内阻随温度降低而升高，低温下内阻可增加三成以上，这是冬季冷启动困难的主因之一。本工具按约 1.2%/℃ 的温度系数把实测内阻折算到 25 ℃ 标准条件后，再与参考值比较，避免低温测量被误判为「内阻偏高」。</p>
    </div>
    <div class="scene-card">
      <h4>🧪 检测方式的选择</h4>
      <p>普通万用表无法准确测量电瓶内阻（毫欧级），需用电导式电池测试仪或在带载条件下测压降。CCA 实测值应理解为仪器按内阻反推的等效冷启动电流，不同品牌仪器的算法略有差异，横向比较建议使用同一台设备。</p>
    </div>
    <div class="info-box">💡 启停电池（EFB/AGM）的参考内阻天然低于普通铅酸，本工具已按类型给出系数修正；更换时必须装同类型电池，否则启停功能与充电策略会失配。</div>
  </div>'''

TB_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var cca0=val('cca0'), cca=val('cca'), res=val('res'), temp=val('temp');
  var tk=val('type'), age=val('age'), disp=val('disp'), eng=val('eng');

  // 内阻参考值：经验关系 R_ref(mΩ) ≈ 3500 ÷ CCA × 类型系数
  var rRef=cca0>0?(3500/cca0)/tk:0;
  // 温度修正：内阻随温度降低而升高，约 1.2%/℃，折算到 25 ℃
  var r25=res/(1+0.012*(25-temp));
  var soh=cca0>0?cca/cca0*100:0;
  var rDev=rRef>0?(r25-rRef)/rRef*100:0;
  // 需求 CCA：按排量与发动机类型经验估算
  var need=(disp*180+120)*eng;
  var margin=need>0?cca/need*100:0;

  var st,cls;
  if(soh>=90&&rDev<=30){ st='健康'; cls='ok'; }
  else if(soh>=70&&rDev<=50){ st='性能衰减，需关注'; cls='warn'; }
  else { st='建议更换'; cls='bad'; }

  // 剩余寿命粗估：按 SOH 年均衰减约 5% 线性外推至 70% 更换线
  var lifeLeft=soh>=70?(soh-70)/5:0;

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">健康度 SOH</div><div class="result-value">'+fmtNum(soh,1)+' %</div></div>'
    +'<div class="result-item"><div class="result-label">内阻（折算 25 ℃）</div><div class="result-value">'+fmtNum(r25,2)+' mΩ</div></div>'
    +'<div class="result-item"><div class="result-label">内阻参考值</div><div class="result-value">'+fmtNum(rRef,2)+' mΩ</div></div>'
    +'<div class="result-item"><div class="result-label">状态判定</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>内阻偏差</h4><p>'+(rDev>0?'+':'')+fmtNum(rDev,1)+' %</p><p>实测 '+fmtNum(res,2)+' mΩ @ '+fmtNum(temp,0)+' ℃</p></div>'
    +'<div class="dist-card"><h4>排量需求 CCA</h4><p>'+fmtNum(need,0)+' A</p><p>实测余量 '+fmtNum(margin,0)+' %</p></div>'
    +'<div class="dist-card"><h4>已使用</h4><p>'+fmtNum(age,0)+' 个月</p><p>约 '+fmtNum(age/12,1)+' 年</p></div>'
    +'<div class="dist-card"><h4>剩余可用期（粗估）</h4><p>'+(lifeLeft>0?fmtNum(lifeLeft,1)+' 年':'已达更换线')+'</p><p>按年均衰减 5% 外推至 70%</p></div>'
    +'</div>';

  var rows='';
  var ages=[0,12,24,36,48,60];
  for(var i=0;i<ages.length;i++){
    rows+='<tr><td style="padding:5px 8px;">'+ages[i]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(Math.max(0,100-ages[i]*5/12),1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(cca0*Math.max(0,100-ages[i]*5/12)/100,0)+'</td>'
      +'<td style="padding:5px 8px;">'+(age>=ages[i]?'已过':'待观察')+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 判定口径</div>'
    +'<div class="formula-line">健康度 SOH = 实测 CCA ÷ 标称 CCA × 100%</div>'
    +'<div class="formula-line">内阻折算 = 实测内阻 ÷ [1 + 0.012 × (25 − 测试温度)]</div>'
    +'<div class="formula-line">内阻参考值 = (3500 ÷ 标称 CCA) ÷ 类型系数</div>'
    +'<div class="formula-line">需求 CCA ≈ (排量 × 180 + 120) × 发动机类型系数</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">使用月数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">SOH 外推 (%)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">对应 CCA (A)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">阶段</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 健康度 '+fmtNum(soh,1)+'%、内阻折算 '+fmtNum(r25,2)+' mΩ，电池状态健康，冷启动余量充足。</div>';
  else if(cls==='warn') ad+='<div class="tip-warn">⚠️ 健康度 '+fmtNum(soh,1)+'%'+(rDev>30?'、内阻偏高 '+fmtNum(rDev,1)+'%':'')+'，已进入衰减期，建议关注冷启动表现并避免长时间熄火用电。</div>';
  else ad+='<div class="tip-bad">⛔ 健康度仅 '+fmtNum(soh,1)+'%'+(rDev>50?'、内阻高于参考 '+fmtNum(rDev,1)+'%':'')+'，冷启动能力不足，建议尽快更换同规格电池。</div>';
  if(margin<100&&soh>=70) ad+='<div class="tip-warn">⚠️ 实测 CCA '+fmtNum(cca,0)+' A 低于 '+fmtNum(disp,1)+' L 发动机的建议需求约 '+fmtNum(need,0)+' A，寒区冬季可能启动困难。</div>';
  if(temp<10) ad+='<div class="tip-info">🌡️ 测试温度 '+fmtNum(temp,0)+' ℃ 偏低，低温下内阻天然升高，已折算到 25 ℃ 再比较；寒区建议关注冷车启动电压。</div>';
  if(tk>1.05) ad+='<div class="tip-info">🔁 已按启停电池类型系数修正参考内阻，更换时须装同类型电池以匹配充电策略。</div>';
  A.innerHTML=ad;
}
calc();'''

# ========================================================== time-maintenance
TM_INPUTS = '''    <div class="input-row">
      <div><label>当前里程 (km)</label><input type="number" id="km" value="43000" oninput="calc()" min="0" step="500"></div>
      <div><label>车龄 (年)</label><input type="number" id="age" value="4" oninput="calc()" min="0" max="30" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>上次保养距今 (月)</label><input type="number" id="last" value="11" oninput="calc()" min="0" max="60" step="1"></div>
      <div><label>年均行驶里程 (km)</label><input type="number" id="perY" value="9000" oninput="calc()" min="500" step="500"></div>
    </div>
    <div class="input-row">
      <div><label>动力类型</label>
        <select id="pow" onchange="calc()">
          <option value="1.0" selected>汽油车</option>
          <option value="1.0">柴油车</option>
          <option value="0.9">新能源（纯电/插混）</option>
        </select>
      </div>
      <div><label>使用与停放</label>
        <select id="park" onchange="calc()">
          <option value="1.0" selected>日常使用</option>
          <option value="0.8">长期停放（每周不足一次）</option>
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
      <div><label>提醒提前量 (km)</label><input type="number" id="ahead" value="800" oninput="calc()" min="0" step="100"></div>
    </div>'''

TM_CARDS = '''  <div class="card">
    <h3>📅 十项保养内容与双阈值</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">里程周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">时间周期</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">低里程车关注</th>
      </tr>
      <tr><td style="padding:6px 8px;">机油 + 机滤</td><td style="padding:6px 8px;">按机油类型</td><td style="padding:6px 8px;">6~12 月</td><td style="padding:6px 8px;">★ 时间先到</td></tr>
      <tr><td style="padding:6px 8px;">空气滤清器</td><td style="padding:6px 8px;">20000 km</td><td style="padding:6px 8px;">12 月</td><td style="padding:6px 8px;">★</td></tr>
      <tr><td style="padding:6px 8px;">空调滤清器</td><td style="padding:6px 8px;">20000 km</td><td style="padding:6px 8px;">12 月</td><td style="padding:6px 8px;">★</td></tr>
      <tr><td style="padding:6px 8px;">汽油滤清器</td><td style="padding:6px 8px;">40000 km</td><td style="padding:6px 8px;">24 月</td><td style="padding:6px 8px;">—</td></tr>
      <tr><td style="padding:6px 8px;">火花塞</td><td style="padding:6px 8px;">45000 km</td><td style="padding:6px 8px;">36 月</td><td style="padding:6px 8px;">★</td></tr>
      <tr><td style="padding:6px 8px;">刹车油</td><td style="padding:6px 8px;">40000 km</td><td style="padding:6px 8px;">24 月</td><td style="padding:6px 8px;">★ 吸湿</td></tr>
      <tr><td style="padding:6px 8px;">防冻液</td><td style="padding:6px 8px;">60000 km</td><td style="padding:6px 8px;">48 月</td><td style="padding:6px 8px;">★</td></tr>
      <tr><td style="padding:6px 8px;">变速箱油</td><td style="padding:6px 8px;">70000 km</td><td style="padding:6px 8px;">48 月</td><td style="padding:6px 8px;">—</td></tr>
      <tr><td style="padding:6px 8px;">正时皮带 / 链条</td><td style="padding:6px 8px;">80000 km</td><td style="padding:6px 8px;">60 月</td><td style="padding:6px 8px;">—</td></tr>
      <tr><td style="padding:6px 8px;">蓄电池</td><td style="padding:6px 8px;">60000 km</td><td style="padding:6px 8px;">36 月</td><td style="padding:6px 8px;">★ 自放电</td></tr>
    </table>
    <div class="scene-card">
      <h4>🕐 低里程车为什么按时间保</h4>
      <p>即便一年只跑 3000 km，机油满 12 个月也应更换：机油在使用中会氧化、吸湿并消耗添加剂，这些变化与时间相关而非仅与里程相关。刹车油具有吸湿性，含水率上升会显著降低沸点，连续制动时可能气阻失效，因此时间周期比里程更关键。</p>
    </div>
    <div class="scene-card">
      <h4>🅿️ 长期停放养护要点</h4>
      <p>长期停放时建议每 2 周启动一次并运行至水温正常，为电瓶补电并驱除潮气；每月移动车辆避免轮胎形成平点；胎压可略高于标准值以减少变形；停放前加满油减少油箱内冷凝水。若停放超过 3 个月，可断开负极或接维护充电器。</p>
    </div>
    <div class="info-box">💡 双阈值取先到者：里程与时间任一到期即需施工。本表为通用参考，实际以随车保养手册为准。</div>
  </div>'''

TM_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var km=val('km'), age=val('age'), last=val('last'), perY=val('perY');
  var pow=val('pow'), park=val('park'), ahead=val('ahead');
  var op=str('oil').split('|');
  var oilKm=parseFloat(op[0]), oilMon=parseFloat(op[1]);

  var ITEMS=[
    ['机油 + 机滤', oilKm, oilMon, 1.0],
    ['空气滤清器', 20000, 12, 1.0],
    ['空调滤清器', 20000, 12, 1.0],
    ['汽油滤清器', 40000, 24, 1.0],
    ['火花塞', 45000, 36, 1.0],
    ['刹车油', 40000, 24, 1.0],
    ['防冻液', 60000, 48, 1.0],
    ['变速箱油', 70000, 48, 1.0],
    ['正时皮带 / 链条', 80000, 60, 1.0],
    ['蓄电池', 60000, 36, 1.0]
  ];

  var due=[], over=[], normal=[], minKm=Infinity, minName='';
  var rows='';
  for(var i=0;i<ITEMS.length;i++){
    var name=ITEMS[i][0], ivKm=ITEMS[i][1]*pow*park, ivMon=ITEMS[i][2]*park;
    if(ivKm<1000) ivKm=1000;
    if(ivMon<1) ivMon=1;
    var nextKm=Math.ceil(km/ivKm)*ivKm;
    if(nextKm<=km) nextKm=km+ivKm;
    var leftKm=nextKm-km;
    // 时间维度：按「距上次保养月数」对时间周期取余，得剩余月数
    var used=last%ivMon;
    var leftMon=(used===0&&last>0)?ivMon:(ivMon-used);
    var yearMon=perY/12;
    var lmLimit=yearMon>0?Math.round(leftKm/yearMon):999;  // 剩余里程折算的月数（展示用）
    var monthLimit=Math.min(lmLimit, leftMon);             // 双阈值取先到者
    var st,col;
    if(leftKm<=0||leftMon<=0){ st='已超期'; col='#dc2626'; over.push(name); }
    else if(leftKm<=ahead||leftMon<=1){ st='建议本次做'; col='#d97706'; due.push(name); }
    else { st='未到期'; col='#059669'; normal.push(name); }
    if(monthLimit<minKm){ minKm=monthLimit; minName=name; }
    rows+='<tr><td style="padding:5px 8px;">'+name+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(ivKm,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(nextKm,0)+'</td>'
      +'<td style="padding:5px 8px;color:'+col+';">'+fmtNum(leftKm,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(ivMon,0)+'</td>'
      +'<td style="padding:5px 8px;color:'+col+';">'+fmtNum(leftMon,0)+'</td>'
      +'<td style="padding:5px 8px;color:'+col+';">'+st+'</td></tr>';
  }

  var ageMon=age*12;
  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">本次建议施工</div><div class="result-value">'+(due.length+over.length)+' 项</div></div>'
    +'<div class="result-item"><div class="result-label">已超期</div><div class="result-value">'+over.length+' 项</div></div>'
    +'<div class="result-item"><div class="result-label">最近到期</div><div class="result-value">'+minName+'</div></div>'
    +'<div class="result-item"><div class="result-label">车辆使用</div><div class="result-value">约 '+fmtNum(ageMon,0)+' 个月</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>本次清单</h4><p style="font-size:12px;">'+(over.concat(due).length?over.concat(due).join('、'):'暂无需进店')+'</p><p>合并一次施工省工时</p></div>'
    +'<div class="dist-card"><h4>上次保养至今</h4><p>'+fmtNum(last,0)+' 个月</p><p>年均 '+fmtNum(perY,0)+' km</p></div>'
    +'<div class="dist-card"><h4>机油时间上限</h4><p>'+fmtNum(oilMon,0)+' 个月</p><p>'+(last>=oilMon?'已超上限':'还剩 '+(oilMon-last)+' 个月')+'</p></div>'
    +'<div class="dist-card"><h4>下一年里程预估</h4><p>'+fmtNum(perY,0)+' km</p><p>约 '+fmtNum(perY/12,0)+' km/月</p></div>'
    +'</div>';

  F.innerHTML='<div class="formula-title">📐 计划口径</div>'
    +'<div class="formula-line">实际里程周期 = 手册周期 × 动力类型系数 × 停放系数</div>'
    +'<div class="formula-line">实际时间周期 = 手册时间周期 × 停放系数</div>'
    +'<div class="formula-line">剩余里程 = 下次到期里程（周期整倍数）− 当前里程</div>'
    +'<div class="formula-line">剩余月数 = 时间周期 −（距上次保养月数 对 时间周期 取余）</div>'
    +'<div class="formula-line">取两者先到者：里程剩余 ≤ '+fmtNum(ahead,0)+' km 或时间剩余 ≤ 1 个月即列入本次建议</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">里程周期</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">下次到期</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (km)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">时间周期</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">剩余 (月)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>';

  var ad='';
  if(over.length) ad+='<div class="tip-bad">⛔ 已超期 '+over.length+' 项：'+over.join('、')+'。其中刹车油、机油等涉及安全与润滑，建议立即安排。</div>';
  if(due.length) ad+='<div class="tip-warn">⚠️ 本次建议施工 '+due.length+' 项：'+due.join('、')+'，可合并为一次进店完成。</div>';
  if(!over.length&&!due.length) ad+='<div class="tip-info">✅ 暂无临近到期项目，最近一项为「'+minName+'」，按里程与时间双阈值估算约 '+fmtNum(minKm,0)+' 个月后到期。</div>';
  if(last>=oilMon) ad+='<div class="tip-warn">🕐 距上次保养已 '+fmtNum(last,0)+' 个月，达到或超过机油时间上限 '+fmtNum(oilMon,0)+' 个月，低里程也应更换机油（氧化与吸湿与时间相关）。</div>';
  if(perY<10000) ad+='<div class="tip-info">📉 年均里程 '+fmtNum(perY,0)+' km 属低里程用车，时间维度将先于里程到期，请以「剩余月数」列为准安排保养。</div>';
  if(park<1.0) ad+='<div class="tip-warn">🅿️ 长期停放会加速油液氧化与电瓶自放电：建议每 2 周启动运行至水温正常，每月移动车辆防轮胎平点，必要时断开负极或接维护充电器。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================== traffic-fine-calculator
TF_INPUTS = '''    <div class="input-row">
      <div><label>违章类型</label>
        <select id="kind" onchange="calc()">
          <option value="0">饮酒后驾驶机动车（12 分）</option>
          <option value="1">高速/快速路超速 50% 以上（12 分）</option>
          <option value="2">高速/快速路倒车、逆行、穿越中央分隔带掉头（12 分）</option>
          <option value="3">高速公路/快速路违法停车（9 分）</option>
          <option value="4">未悬挂号牌或故意遮挡、污损号牌（9 分）</option>
          <option value="5">驾驶与准驾车型不符的机动车（9 分）</option>
          <option value="6">高速/快速路超速 20%~50%（6 分）</option>
          <option value="7">非高速道路超速 50% 以上（6 分）</option>
          <option value="8" selected>不按交通信号灯指示通行（闯红灯，6 分）</option>
          <option value="9">高速/快速路违法占用应急车道行驶（6 分）</option>
          <option value="10">驾驶证被暂扣/扣留期间驾驶（6 分）</option>
          <option value="11">非高速道路超速 20%~50%（3 分）</option>
          <option value="12">高速/快速路不按规定车道行驶（3 分）</option>
          <option value="13">不按规定超车、让行，或非高速道路逆行（3 分）</option>
          <option value="14">驾驶时拨打、接听手持电话（3 分）</option>
          <option value="15">行经人行横道不按规定减速、停车、避让行人（3 分）</option>
          <option value="16">在高速公路上行驶低于规定最低时速（3 分）</option>
          <option value="17">不按规定会车，或非高速道路不按规定倒车、掉头（1 分）</option>
          <option value="18">不按规定使用灯光（1 分）</option>
          <option value="19">违反禁令标志、禁止标线指示（1 分）</option>
          <option value="20">驾驶机动车时未按规定系安全带（1 分）</option>
          <option value="21">载货长度、宽度、高度超过规定（1 分）</option>
          <option value="22">驾驶摩托车不戴安全头盔（1 分）</option>
        </select>
      </div>
      <div><label>准驾车型</label>
        <select id="lic" onchange="calc()">
          <option value="7" selected>小型车（C 类，满分学习 7 天）</option>
          <option value="30">大型车（A/B 类，满分学习 30 天）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>本记分周期已记分 (分)</label><input type="number" id="had" value="6" oninput="calc()" min="0" max="60" step="1"></div>
      <div><label>已通过学法减分扣减 (分)</label><input type="number" id="cut" value="0" oninput="calc()" min="0" max="6" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>罚款缴纳情况</label>
        <select id="paid" onchange="calc()">
          <option value="1" selected>已缴清</option>
          <option value="0">尚未缴纳</option>
        </select>
      </div>
      <div><label>处罚方式</label>
        <select id="mode" onchange="calc()">
          <option value="1" selected>电子监控（非现场）</option>
          <option value="0">现场处罚决定书</option>
        </select>
      </div>
    </div>'''

TF_CARDS = '''  <div class="card">
    <h3>⚖️ 记分与满分处理规则</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">规则项</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">规定</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">依据</th>
      </tr>
      <tr><td style="padding:6px 8px;">记分周期</td><td style="padding:6px 8px;">12 个月，满分 12 分，自初次领证之日起连续计算</td><td style="padding:6px 8px;">第 163 号令第三条</td></tr>
      <tr><td style="padding:6px 8px;">分值档位</td><td style="padding:6px 8px;">12 / 9 / 6 / 3 / 1 分</td><td style="padding:6px 8px;">第 163 号令第七条</td></tr>
      <tr><td style="padding:6px 8px;">周期清零</td><td style="padding:6px 8px;">未满 12 分且罚款已缴，周期结束记分清除；有罚款逾期未缴，对应记分转入下一周期</td><td style="padding:6px 8px;">第 163 号令第十五条</td></tr>
      <tr><td style="padding:6px 8px;">满分学习</td><td style="padding:6px 8px;">满 12 分扣留驾驶证，参加 7 天学习（大型车 30 天），考试合格且缴清罚款后清除</td><td style="padding:6px 8px;">第 163 号令第十七至二十三条</td></tr>
      <tr><td style="padding:6px 8px;">学法减分</td><td style="padding:6px 8px;">网上学习 3 日累计满 30 分钟且合格减 1 分；现场学习满 1 小时减 2 分；公益活动满 1 小时减 1 分；每周期最高减 6 分</td><td style="padding:6px 8px;">第 163 号令第二十五、二十七条</td></tr>
      <tr><td style="padding:6px 8px;">罚款幅度</td><td style="padding:6px 8px;">一般通行违法警告或 20~200 元；超速 50% 以上等 200~2000 元；饮酒驾驶 1000~2000 元并暂扣 6 个月</td><td style="padding:6px 8px;">《道交法》第 90、91、99 条</td></tr>
    </table>
    <div class="scene-card">
      <h4>⏳ 滞纳金与处理时限</h4>
      <p>现场处罚决定书应自收到之日起 15 日内缴纳罚款；逾期不履行处罚决定的，每日按罚款数额的百分之三加处罚款，加处罚款总额不得超出罚款数额本身。电子监控记录应先接受处理、领取处罚决定书，再按期缴纳，未处理期间不产生滞纳金但会被锁定业务办理。</p>
    </div>
    <div class="scene-card">
      <h4>📍 关于金额的地区差异</h4>
      <p>《道路交通安全违法行为记分管理办法》第三十五条明确：省、自治区、直辖市公安厅、局可以在本办法规定的处罚幅度范围内制定具体执行标准。因此同一种违法在不同地区的实际罚款金额可能存在差异，本页给出的是法定幅度，具体金额以处罚决定书与当地交警部门公示为准。</p>
    </div>
    <div class="info-box">⚠️ 本工具为记分与幅度的通用速查，不构成法律意见。对处罚有异议时，可在法定期限内申请行政复议或提起行政诉讼。</div>
  </div>'''

TF_JS = H + '''
// 数据源：公安部令第 163 号《道路交通安全违法行为记分管理办法》（2022-04-01 施行）
//        《道路交通安全法》第 90 / 91 / 99 条（罚款幅度）
var TF_TYPES=[
  {n:'饮酒后驾驶机动车', p:12, f:'1000~2000 元', e:'并处暂扣驾驶证 6 个月'},
  {n:'高速/城市快速路超速 50% 以上（小型车）', p:12, f:'200~2000 元', e:'可并处吊销驾驶证'},
  {n:'高速/城市快速路倒车、逆行、穿越中央分隔带掉头', p:12, f:'200~2000 元', e:'可并处吊销驾驶证'},
  {n:'高速公路/城市快速路违法停车', p:9, f:'警告或 20~200 元', e:''},
  {n:'未悬挂号牌或故意遮挡、污损号牌', p:9, f:'警告或 20~200 元', e:''},
  {n:'驾驶与准驾车型不符的机动车', p:9, f:'200~2000 元', e:''},
  {n:'高速/城市快速路超速 20%~50%（小型车）', p:6, f:'警告或 20~200 元', e:''},
  {n:'非高速道路超速 50% 以上（小型车）', p:6, f:'200~2000 元', e:''},
  {n:'不按交通信号灯指示通行（闯红灯）', p:6, f:'警告或 20~200 元', e:''},
  {n:'高速/城市快速路违法占用应急车道行驶', p:6, f:'警告或 20~200 元', e:''},
  {n:'驾驶证被暂扣/扣留期间驾驶机动车', p:6, f:'200~2000 元', e:''},
  {n:'非高速道路超速 20%~50%（小型车）', p:3, f:'警告或 20~200 元', e:''},
  {n:'高速/城市快速路不按规定车道行驶', p:3, f:'警告或 20~200 元', e:''},
  {n:'不按规定超车、让行，或非高速道路逆行', p:3, f:'警告或 20~200 元', e:''},
  {n:'驾驶时拨打、接听手持电话', p:3, f:'警告或 20~200 元', e:''},
  {n:'行经人行横道不按规定减速、停车、避让行人', p:3, f:'警告或 20~200 元', e:''},
  {n:'在高速公路上行驶低于规定最低时速', p:3, f:'警告或 20~200 元', e:''},
  {n:'不按规定会车，或非高速道路不按规定倒车、掉头', p:1, f:'警告或 20~200 元', e:''},
  {n:'不按规定使用灯光', p:1, f:'警告或 20~200 元', e:''},
  {n:'违反禁令标志、禁止标线指示', p:1, f:'警告或 20~200 元', e:''},
  {n:'驾驶机动车时未按规定系安全带', p:1, f:'警告或 20~200 元', e:''},
  {n:'载货长度、宽度、高度超过规定', p:1, f:'警告或 20~200 元', e:''},
  {n:'驾驶摩托车不戴安全头盔', p:1, f:'警告或 20~200 元', e:''}
];
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var idx=parseInt(str('kind'),10)||0;
  var lic=val('lic'), had=val('had'), cut=val('cut');
  var paid=val('paid'), mode=val('mode');
  var t=TF_TYPES[idx]||TF_TYPES[0];

  var eff=Math.max(0, had-cut);        // 已减分后的现有记分
  var total=eff+t.p;                   // 加上本次后的累计
  var cutLeft=Math.max(0, 6-cut);      // 本周期剩余可减分额度
  var over=total>=12;
  var needCut=Math.max(0, total-11);   // 想压到 11 分需再减的分数

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">本次记分</div><div class="result-value">'+fmtNum(t.p,0)+' 分</div></div>'
    +'<div class="result-item"><div class="result-label">累计记分</div><div class="result-value">'+fmtNum(total,0)+' / 12 分</div></div>'
    +'<div class="result-item"><div class="result-label">罚款幅度</div><div class="result-value">'+t.f+'</div></div>'
    +'<div class="result-item"><div class="result-label">是否达满分</div><div class="result-value">'+(over?'已达 12 分':'未达 12 分')+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>违纪类型</h4><p style="font-size:12px;">'+t.n+'</p><p>'+(t.e?t.e:'无附加处罚')+'</p></div>'
    +'<div class="dist-card"><h4>学法减分额度</h4><p>剩余 '+fmtNum(cutLeft,0)+' 分</p><p>本周期上限 6 分</p></div>'
    +'<div class="dist-card"><h4>清零条件</h4><p>'+(paid?'罚款已缴清':'罚款未缴清')+'</p><p>'+(paid?'周期结束可清除':'逾期未缴记分转入下周期')+'</p></div>'
    +'<div class="dist-card"><h4>满分处理</h4><p>'+(over?'扣留驾驶证':'无需满分学习')+'</p><p>'+(over?'学习 '+fmtNum(lic,0)+' 天并考试':'继续保持')+'</p></div>'
    +'</div>';

  var rows='';
  var seq=[1,3,6,9,12];
  for(var i=0;i<seq.length;i++){
    var q=seq[i];
    var after=q*t.p;
    rows+='<tr><td style="padding:5px 8px;">'+q+' 次</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(after,0)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(Math.max(0,eff+after-cut),0)+'</td>'
      +'<td style="padding:5px 8px;color:'+((eff+after-cut)>=12?'#dc2626':'#059669')+';">'+((eff+after-cut)>=12?'需满分学习':'正常')+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">累计记分 = （本周期已记分 − 学法减分扣减）+ 本次记分（同类多次按倍数累加）</div>'
    +'<div class="formula-line">记分周期 12 个月、满分 12 分，自初次领证之日起连续计算</div>'
    +'<div class="formula-line">学法减分一个记分周期内累计最高扣减 6 分</div>'
    +'<div class="formula-line">累积满 12 分扣留驾驶证并参加满分学习；二次满 12 分或累计 24~36 分加考道路驾驶技能</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">同类次数</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">本次累计</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">总累计 (分)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'
    +rows+'</table>';

  var ad='';
  if(over) ad+='<div class="tip-bad">⛔ 累计记分 '+fmtNum(total,0)+' 分已达满分线，驾驶证将被扣留，须参加为期 '+fmtNum(lic,0)+' 天的满分学习并考试合格、缴清罚款后方可清除记分。'+(total>=24?'累计 '+fmtNum(total,0)+' 分，属二次以上满分，须加考道路驾驶技能。':'')+'</div>';
  else if(total>=9) ad+='<div class="tip-warn">⚠️ 累计记分 '+fmtNum(total,0)+' 分，距满分仅剩 '+fmtNum(12-total,0)+' 分，建议谨慎驾驶；符合条件的可通过学法减分最多再减 '+fmtNum(Math.min(cutLeft,needCut),0)+' 分。</div>';
  else ad+='<div class="tip-info">✅ 累计记分 '+fmtNum(total,0)+' 分，未接近满分线。'+(cutLeft>0?'本周期还有 '+fmtNum(cutLeft,0)+' 分学法减分额度可用。':'')+'</div>';
  if(!paid) ad+='<div class="tip-warn">💰 罚款尚未缴清。未缴罚款对应的记分将转入下一记分周期，不会随周期结束清除。</div>';
  else if(over) ad+='<div class="tip-info">💰 罚款已缴清，但本周期累计已达满分，须完成满分学习、考试合格后记分方可清除。</div>';
  else ad+='<div class="tip-info">💰 罚款已缴清且未满 12 分，本记分周期结束后该记分予以清除。</div>';
  if(mode<1) ad+='<div class="tip-info">🧾 现场处罚决定书：应自收到之日起 15 日内缴纳罚款，逾期按每日 3% 加处罚款（总额不超过罚款本金）。</div>';
  else ad+='<div class="tip-info">📷 电子监控记录：应先到窗口或线上接受处理、取得处罚决定书后再按期缴纳，未处理不产生滞纳金但会锁定相关业务。</div>';
  A.innerHTML=ad;
}
calc();'''

# ================================================= xuanguatanhuangzunitexing
XS_INPUTS = '''    <div class="input-row">
      <div><label>弹簧刚度 k (N/mm)</label><input type="number" id="k" value="28" oninput="calc()" min="5" max="300" step="1"></div>
      <div><label>阻尼系数 c (N·s/m)</label><input type="number" id="c" value="2000" oninput="calc()" min="100" max="20000" step="50"></div>
    </div>
    <div class="input-row">
      <div><label>簧上质量 m (kg)</label><input type="number" id="m" value="400" oninput="calc()" min="50" max="3000" step="10"></div>
      <div><label>簧下质量 (kg)</label><input type="number" id="mu" value="45" oninput="calc()" min="5" max="300" step="5"></div>
    </div>
    <div class="input-row">
      <div><label>轮胎径向刚度 (N/mm)</label><input type="number" id="kt" value="220" oninput="calc()" min="50" max="600" step="10"></div>
      <div><label>悬架取向</label>
        <select id="tune" onchange="calc()">
          <option value="0" selected>舒适取向（目标 1.0~1.4 Hz）</option>
          <option value="1">均衡取向（目标 1.4~1.7 Hz）</option>
          <option value="2">运动取向（目标 1.7~2.2 Hz）</option>
        </select>
      </div>
    </div>
    <div class="input-row">
      <div><label>单轮承载 (kg)</label><input type="number" id="load" value="380" oninput="calc()" min="50" max="3000" step="10"></div>
      <div><label>减振器行程 (mm)</label><input type="number" id="stroke" value="200" oninput="calc()" min="30" max="400" step="5"></div>
    </div>'''

XS_CARDS = '''  <div class="card">
    <h3>📊 固有频率与阻尼比参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">簧上固有频率</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">主观感受</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型车型</th>
      </tr>
      <tr><td style="padding:6px 8px;">0.8 ~ 1.0 Hz</td><td style="padding:6px 8px;">偏软，长途舒适但侧倾大</td><td style="padding:6px 8px;">中大型舒适轿车、MPV</td></tr>
      <tr><td style="padding:6px 8px;">1.0 ~ 1.4 Hz</td><td style="padding:6px 8px;">舒适区，滤震与支撑平衡</td><td style="padding:6px 8px;">家用轿车、SUV</td></tr>
      <tr><td style="padding:6px 8px;">1.4 ~ 1.7 Hz</td><td style="padding:6px 8px;">偏硬，路感清晰</td><td style="padding:6px 8px;">运动型轿车</td></tr>
      <tr><td style="padding:6px 8px;">1.7 ~ 2.2 Hz</td><td style="padding:6px 8px;">硬朗，细碎振动明显</td><td style="padding:6px 8px;">性能车、赛道取向</td></tr>
    </table>
    <div class="scene-card">
      <h4>🎯 阻尼比取值</h4>
      <p>乘用车常用阻尼比在 0.2~0.35 之间：偏低（&lt;0.2）车身起伏衰减慢、余振多，过连续起伏路面易「坐船」；偏高（&gt;0.45）路面冲击传递直接、舒适性下降且减振器发热加剧。0.25~0.35 通常是舒适与操控的平衡区间。</p>
    </div>
    <div class="scene-card">
      <h4>🌀 弹簧刚度与线径的关系</h4>
      <p>圆柱螺旋弹簧刚度 k = G·d⁴ ÷ (8·D³·n)，其中 G 为材料剪切模量、d 为线径、D 为中径、n 为有效圈数。线径 d 是 4 次方项，影响最显著：线径增加 10%，刚度约增 46%。改刚度时优先调线径与圈数，同时注意压并高度与并圈风险。</p>
    </div>
    <div class="info-box">💡 簧上固有频率应在 1.0~1.5 Hz 附近，且与簧下固有频率拉开 4 倍以上，避免路面激励同时激起车身与车轮共振。</div>
  </div>'''

XS_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var k=val('k'), c=val('c'), m=val('m'), mu=val('mu');
  var kt=val('kt'), tune=parseInt(str('tune'),10)||0;
  var load=val('load'), stroke=val('stroke');

  var kN=k*1000, ktN=kt*1000, g=9.81;
  var wn=Math.sqrt(kN/m);                 // 簧上固有圆频率 rad/s
  var f=wn/(2*Math.PI);                   // Hz
  var cc=2*Math.sqrt(kN*m);               // 临界阻尼 N·s/m
  var zeta=cc>0?c/cc:0;                   // 阻尼比
  var defl=load*g/kN*1000;                // 静挠度 mm
  var T=1/f;
  var logDec=zeta<1?(2*Math.PI*zeta/Math.sqrt(1-zeta*zeta)):0;
  // 簧下固有频率：轮胎刚度与弹簧刚度并联作用在簧下质量上
  var wn2=Math.sqrt((kN+ktN)/mu);
  var f2=wn2/(2*Math.PI);
  var ratio=f>0?f2/f:0;
  var travel=stroke-defl;                 // 压缩方向可用余量 = 总行程 − 静挠度

  var rng=[[1.0,1.4],[1.4,1.7],[1.7,2.2]][tune];
  var name=['舒适','均衡','运动'][tune];
  var fOk=f>=rng[0]&&f<=rng[1];
  var zOk=zeta>=0.2&&zeta<=0.35;

  var st,cls;
  if(fOk&&zOk){ st='匹配良好'; cls='ok'; }
  else if(!zOk&&(zeta<0.15||zeta>0.5)){ st='阻尼严重失配'; cls='bad'; }
  else { st='需调整'; cls='warn'; }

  R.innerHTML='<div class="result-grid">'
    +'<div class="result-item"><div class="result-label">簧上固有频率</div><div class="result-value">'+fmtNum(f,3)+' Hz</div></div>'
    +'<div class="result-item"><div class="result-label">阻尼比 ζ</div><div class="result-value">'+fmtNum(zeta,3)+'</div></div>'
    +'<div class="result-item"><div class="result-label">临界阻尼</div><div class="result-value">'+fmtNum(cc,0)+' N·s/m</div></div>'
    +'<div class="result-item"><div class="result-label">匹配判定</div><div class="result-value">'+st+'</div></div>'
    +'</div>';

  G.innerHTML='<div class="dist-grid">'
    +'<div class="dist-card"><h4>静挠度与余量</h4><p>'+fmtNum(defl,1)+' mm</p><p>压缩余量 '+fmtNum(travel,1)+' mm（行程 '+fmtNum(stroke,0)+'）</p></div>'
    +'<div class="dist-card"><h4>振动周期</h4><p>'+fmtNum(T,3)+' s</p><p>对数衰减率 '+fmtNum(logDec,2)+'</p></div>'
    +'<div class="dist-card"><h4>簧下固有频率</h4><p>'+fmtNum(f2,1)+' Hz</p><p>与簧上比 '+fmtNum(ratio,1)+' 倍</p></div>'
    +'<div class="dist-card"><h4>目标区间</h4><p>'+fmtNum(rng[0],1)+'~'+fmtNum(rng[1],1)+' Hz</p><p>'+name+'取向 · ζ 0.20~0.35</p></div>'
    +'</div>';

  // 按线径比例反推不同线径下的刚度（同中径与圈数，k ∝ d⁴）
  var rows='', base=12;
  var ds=[10,11,12,13,14];
  for(var i=0;i<ds.length;i++){
    var kk=k*Math.pow(ds[i]/base,4);
    var fk=Math.sqrt(kk*1000/m)/(2*Math.PI);
    var zk=2*Math.sqrt(kk*1000*m);
    rows+='<tr><td style="padding:5px 8px;">'+ds[i]+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(kk,1)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(fk,3)+'</td>'
      +'<td style="padding:5px 8px;">'+fmtNum(c/zk,3)+'</td>'
      +'<td style="padding:5px 8px;">'+(fk>=rng[0]&&fk<=rng[1]&&c/zk>=0.2&&c/zk<=0.35?'匹配':'偏离')+'</td></tr>';
  }
  F.innerHTML='<div class="formula-title">📐 计算口径</div>'
    +'<div class="formula-line">簧上固有频率 f = (1 ÷ 2π) × √(k ÷ m)，k 单位 N/m、m 为簧上质量</div>'
    +'<div class="formula-line">临界阻尼 Cc = 2√(k·m)；阻尼比 ζ = c ÷ Cc</div>'
    +'<div class="formula-line">静挠度 δ = 单轮承载 × g ÷ k；振动周期 T = 1 ÷ f</div>'
    +'<div class="formula-line">对数衰减率 Λ = 2πζ ÷ √(1 − ζ²)</div>'
    +'<div class="formula-line">簧下固有频率 f₂ = (1 ÷ 2π) × √[(k + kt) ÷ 簧下质量]</div>'
    +'<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:10px;">'
    +'<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">线径 (mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">刚度 (N/mm)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">频率 (Hz)</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">阻尼比</th>'
    +'<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">是否匹配</th></tr>'
    +rows+'</table>';

  var ad='';
  if(cls==='ok') ad+='<div class="tip-info">✅ 簧上固有频率 '+fmtNum(f,3)+' Hz、阻尼比 '+fmtNum(zeta,3)+'，处于'+name+'取向的目标区间，滤震与支撑较为平衡。</div>';
  else if(cls==='bad') ad+='<div class="tip-bad">⛔ 阻尼比 '+fmtNum(zeta,3)+' 严重偏离 0.20~0.35：'+(zeta<0.15?'阻尼过小，车身余振多、过起伏路面易「坐船」，建议提高阻尼系数。':'阻尼过大，路面冲击传递直接、舒适性差，建议降低阻尼或换用可调减振器。')+'</div>';
  else ad+='<div class="tip-warn">⚠️ 簧上固有频率 '+fmtNum(f,3)+' Hz'+(fOk?'在':'不在')+'目标区间（'+fmtNum(rng[0],1)+'~'+fmtNum(rng[1],1)+' Hz）'+(zOk?'但阻尼比正常':'，阻尼比 '+fmtNum(zeta,3)+' 也需调至 0.20~0.35')+'，建议按目标刚度成套更换弹簧与减振器。</div>';
  if(ratio>0&&ratio<4) ad+='<div class="tip-warn">⚙️ 簧下与簧上固有频率比仅 '+fmtNum(ratio,1)+' 倍（建议 4 倍以上），路面激励可能同时激起车身与车轮共振，操控与接地性会变差。</div>';
  if(travel<40) ad+='<div class="tip-warn">📏 静挠度 '+fmtNum(defl,1)+' mm 占减振器行程 '+fmtNum(stroke,0)+' mm 的 '+fmtNum(stroke>0?defl/stroke*100:0,0)+'%，压缩方向余量仅 '+fmtNum(travel,1)+' mm，满载或过坑易触底，建议提高刚度或加长行程。</div>';
  if(zeta>0&&zeta<1) ad+='<div class="tip-info">📈 对数衰减率 '+fmtNum(logDec,2)+'：车身受激励后约经 '+(logDec>0?fmtNum(Math.ceil(6.9/(zeta*wn)/T),0):'—')+' 个振动周期衰减至初始幅值的 10%。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='tester-11', title='电池（CCA/内阻）测试', icon='🚙', accent='#4b5563',
         desc='汽车电池在线测试工具，输入冷启动电流（CCA）与内阻评估电池健康状态，给出状态判定，辅助电瓶选型与更换，纯前端。',
         inputs=TB_INPUTS, cards=TB_CARDS,
         notes='内阻须用电导式电池测试仪测量（万用表无法测毫欧级），CCA 为仪器按内阻反推的等效值，横向比较建议用同一台设备',
         js=TB_JS),
    dict(slug='time-maintenance', title='保养计划计算', icon='🚗', accent='#b45309',
         desc='输入当前里程、车龄与上次保养信息，自动生成包含机油、滤清器、火花塞等十项内容的下次保养计划与建议项目，规划养车周期。',
         inputs=TM_INPUTS, cards=TM_CARDS,
         notes='里程与时间双阈值取先到者；低里程用车以时间维度为主，实际以随车保养手册为准',
         js=TM_JS),
    dict(slug='traffic-fine-calculator', title='违章罚款金额计算（汽车）', icon='⚠️', accent='#b91c1c',
         desc='选择违章类型和严重程度，查看罚款金额和扣分标准（基于2022年道交法）',
         inputs=TF_INPUTS, cards=TF_CARDS,
         notes='记分依据公安部令第 163 号（2022-04-01 施行），罚款为道交法法定幅度，具体金额以处罚决定书与当地交警公示为准',
         js=TF_JS),
    dict(slug='xuanguatanhuangzunitexing', title='悬挂弹簧阻尼特性', icon='🚗', accent='#0f766e',
         desc='输入弹簧刚度、阻尼系数与簧上质量，计算悬挂系统固有频率、阻尼比与振动特性。',
         inputs=XS_INPUTS, cards=XS_CARDS,
         notes='簧上固有频率宜在 1.0~1.5 Hz、阻尼比 0.20~0.35；改刚度须同步匹配减振器阻尼',
         js=XS_JS),
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
    print('---- batch12: %d/%d ----' % (ok, total))


if __name__ == '__main__':
    main()
