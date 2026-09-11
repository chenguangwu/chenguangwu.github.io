#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 1（engine-oil / tire-pressure / oil-change / wear-brake）。

每页按站点 A 级工具页同构骨架重建真实 body：输入区 + calc + 结果卡 + formula-box
（触发 classify_quality 的 rich 判定 → A 级）+ 参考/场景卡 + 注意事项。
deep-dive 由 _build.py 从 content_deepdive.json 在占位符处重建。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

ROOT = L.ROOT
H = L.JS_HELPERS

# ---------------------------------------------------------------- engine-oil
ENG_OIL_INPUTS = '''    <div class="input-row">
      <div><label>当地冬季最低气温 (℃)</label><input type="number" id="tmin" value="-10" oninput="calc()" step="any"></div>
      <div><label>当地夏季最高气温 (℃)</label><input type="number" id="tmax" value="35" oninput="calc()" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>发动机类型</label><select id="eng" onchange="calc()">
        <option value="na">自然吸气（歧管喷射）</option>
        <option value="turbo">涡轮增压（歧管喷射）</option>
        <option value="gdi" selected>涡轮增压直喷（带 GPF/DPF）</option>
      </select></div>
      <div><label>车龄 (年)</label><input type="number" id="age" value="5" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>是否高里程 / 需补机油</label><select id="burn" onchange="calc()">
        <option value="no" selected>否</option>
        <option value="yes">是（超 15 万 km 或需补机油）</option>
      </select></div>
      <div><label>用车强度</label><select id="sev" onchange="calc()">
        <option value="normal" selected>日常通勤</option>
        <option value="heavy">长途 / 拖挂 / 高负荷</option>
      </select></div>
    </div>'''

ENG_OIL_CARDS = '''  <div class="card">
    <h3>📖 SAE 低温等级与泵送温度对照</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">SAE 低温等级</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">CCS 泵送温度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">适用最低气温</th>
      </tr>
      <tr><td style="padding:6px 8px;">0W</td><td style="padding:6px 8px;">−35℃</td><td style="padding:6px 8px;">≤ −35℃，严寒地区</td></tr>
      <tr><td style="padding:6px 8px;">5W</td><td style="padding:6px 8px;">−30℃</td><td style="padding:6px 8px;">−35 ~ −30℃</td></tr>
      <tr><td style="padding:6px 8px;">10W</td><td style="padding:6px 8px;">−25℃</td><td style="padding:6px 8px;">−30 ~ −25℃</td></tr>
      <tr><td style="padding:6px 8px;">15W</td><td style="padding:6px 8px;">−20℃</td><td style="padding:6px 8px;">−25 ~ −20℃</td></tr>
      <tr><td style="padding:6px 8px;">20W</td><td style="padding:6px 8px;">−15℃</td><td style="padding:6px 8px;">≥ −15℃，华南常温</td></tr>
    </table>
    <div class="scene-card">
      <h4>🌡️ W 前后看什么</h4>
      <p>W 前数字管低温启动，越小越抗寒；W 后数字是 100℃ 运动黏度，越大油膜越厚、越高负荷工况保护越好，但油耗与冷启动阻力也上升。</p>
    </div>
    <div class="scene-card">
      <h4>🧯 低灰分为何重要</h4>
      <p>带 GPF/DPF 的涡轮直喷机烧掉的机油灰分无法再生，会堵塞捕集器、缩短再生周期，须用 ACEA C 系列或厂家认证的低灰分油。</p>
    </div>
    <div class="info-box">💡 本工具给出的是「按气候与车况的合理黏度区间」，最终须以随车保养手册标注为准，不可凭感觉随意降黏或加黏。</div>
  </div>'''

ENG_OIL_JS = H + '''
var VISC=[{w:'0W',ccs:-35},{w:'5W',ccs:-30},{w:'10W',ccs:-25},{w:'15W',ccs:-20},{w:'20W',ccs:-15}];
function pickW(t){
  for(var i=0;i<VISC.length;i++){ if(t<=VISC[i].ccs) return VISC[i]; }
  return {w:'20W',ccs:-15};
}
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var tmin=val('tmin'),tmax=val('tmax'),age=val('age');
  var eng=str('eng'),burn=str('burn'),sev=str('sev');
  if(isNaN(tmin)||isNaN(tmax)||isNaN(age)){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的气温与车龄</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var v=pickW(tmin);
  var hot=30;
  if(tmax<30 && age<6 && burn==='no' && sev==='normal'){ hot=20; }
  if(tmax>=35 || age>=8 || burn==='yes' || sev==='heavy'){ hot=40; }
  if(burn==='yes' && (age>=10 || sev==='heavy')){ hot=50; }
  var sae=v.w+'-'+hot;
  var lowAsh=(eng==='gdi');
  var api=lowAsh?'ACEA C2/C3/C5（低灰分）':(eng==='turbo'?'API SP / ILSAC GF-6 + 厂家认证':'API SP / ILSAC GF-6');
  R.innerHTML='<div class="safe-val">SAE '+sae+'</div><div class="safe-sub">'+api+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+v.w+'</div><div class="l">低温等级（CCS '+v.ccs+'℃）</div></div>'+
    '<div class="dist-card"><div class="v">'+hot+'</div><div class="l">100℃ 高温黏度</div></div>'+
    '<div class="dist-card"><div class="v">'+(lowAsh?'需要':'不需要')+'</div><div class="l">低灰分要求</div></div>'+
    '<div class="dist-card"><div class="v">'+sae+'</div><div class="l">推荐黏度等级</div></div>';
  F.innerHTML=
    '<div class="fb-title">选型规则</div>'+
    '<div class="fb-row">低温等级：当地最低气温 ≤ 该等级 CCS 温度（0W −35℃ / 5W −30℃ / 10W −25℃ / 15W −20℃ / 20W −15℃）</div>'+
    '<div class="fb-row">高温黏度：新车温和气候 20~30；高温、老车、高负荷或已见机油消耗 40~50</div>'+
    '<div class="fb-row">认证规格：自然吸气 API SP；涡轮增压加厂家认证；带 GPF/DPF 须 ACEA C 系列低灰分</div>'+
    '<div class="fb-row">本次判定：最低气温 '+fmtNum(tmin,0)+'℃ → '+v.w+'；最高气温 '+fmtNum(tmax,0)+'℃、车龄 '+fmtNum(age,0)+' 年 → '+hot+'</div>';
  var ad='';
  if(lowAsh){ ad='<div class="tip-warn">⚠️ 带 GPF/DPF 的直喷机必须用低灰分机油（ACEA C 系列或厂家认证），普通高灰分油会加速捕集器堵塞。</div>'; }
  else if(hot>=40){ ad='<div class="tip-info">ℹ️ 已按高温／老车／高负荷上探高温黏度，冷启动阻力会略增，注意冬季启动表现。</div>'; }
  else{ ad='<div class="tip-success">✅ 常规气候与车况，按手册推荐黏度即可，无需刻意加黏。</div>'; }
  if(burn==='yes'){ ad+='<div class="tip-warn">⚠️ 已见机油消耗：先排查渗漏与 PCV，选油时适当提高高温黏度，但不要用黏度掩盖机械故障。</div>'; }
  A.innerHTML=ad;
}
calc();'''

# ------------------------------------------------------------- tire-pressure
TIRE_INPUTS = '''    <div class="input-row">
      <div><label>标贴标准前胎压 (bar)</label><input type="number" id="f0" value="2.3" oninput="calc()" step="0.01" min="0"></div>
      <div><label>标贴标准后胎压 (bar)</label><input type="number" id="r0" value="2.1" oninput="calc()" step="0.01" min="0"></div>
    </div>
    <div class="input-row">
      <div><label>载重状态</label><select id="load" onchange="calc()">
        <option value="empty" selected>空载（1~2 人）</option>
        <option value="half">半载（3~4 人）</option>
        <option value="full">满载 / 拉货</option>
      </select></div>
      <div><label>季节</label><select id="season" onchange="calc()">
        <option value="normal" selected>常温</option>
        <option value="winter">冬季（气温常低于 0℃）</option>
        <option value="summer">夏季（高温长途）</option>
      </select></div>
    </div>
    <div class="input-row">
      <div><label>实测前胎压 (bar)</label><input type="number" id="fc" value="2.0" oninput="calc()" step="0.01" min="0"></div>
      <div><label>实测后胎压 (bar)</label><input type="number" id="rc" value="1.9" oninput="calc()" step="0.01" min="0"></div>
    </div>'''

TIRE_CARDS = '''  <div class="card">
    <h3>📖 胎压修正与单位换算</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">修正项</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">调整量</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">原因</th>
      </tr>
      <tr><td style="padding:6px 8px;">半载</td><td style="padding:6px 8px;">+0.1 bar</td><td style="padding:6px 8px;">轴荷增加，接地印痕变大</td></tr>
      <tr><td style="padding:6px 8px;">满载 / 拉货</td><td style="padding:6px 8px;">+0.2 bar</td><td style="padding:6px 8px;">抑制胎侧过度变形与发热</td></tr>
      <tr><td style="padding:6px 8px;">冬季</td><td style="padding:6px 8px;">+0.1 bar</td><td style="padding:6px 8px;">低温冷缩，抵消约 0.1 bar 降幅</td></tr>
      <tr><td style="padding:6px 8px;">夏季高速</td><td style="padding:6px 8px;">−0.05 bar</td><td style="padding:6px 8px;">行驶升温，避免热态超压</td></tr>
    </table>
    <div class="scene-card">
      <h4>🔁 单位换算</h4>
      <p>1 bar = 100 kPa = 14.5038 psi ≈ 1.0197 kgf/cm²。标贴常见 bar 与 psi 双标，气泵读数单位不同时先换算再充气。</p>
    </div>
    <div class="scene-card">
      <h4>🧊 冷态测量</h4>
      <p>胎压须在冷胎（停车 3 小时以上或行驶不足 2km）时测量；刚跑完高速的热态读数会偏高 0.2~0.3 bar，不能直接对照标贴。</p>
    </div>
    <div class="info-box">💡 前后轴通常不同（前驱车前轮略高）。四轮独立、胎压监测灯亮起时，请逐轮核对并复位。</div>
  </div>'''

TIRE_JS = H + '''
var PSI=14.5038;
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var f0=val('f0'),r0=val('r0'),fc=val('fc'),rc=val('rc');
  var load=str('load'),season=str('season');
  if(isNaN(f0)||isNaN(r0)||isNaN(fc)||isNaN(rc)){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的标贴与实测胎压</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var adj=(load==='full')?0.2:(load==='half'?0.1:0);
  var se=(season==='winter')?0.1:(season==='summer'?-0.05:0);
  var tf=f0+adj+se, tr=r0+adj+se;
  var df=tf-fc, dr=tr-rc;
  R.innerHTML='<div class="safe-val">前 '+fmtNum(tf,2)+' / 后 '+fmtNum(tr,2)+' bar</div><div class="safe-sub">折合 前 '+fmtNum(tf*PSI,1)+' / 后 '+fmtNum(tr*PSI,1)+' psi</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(tf,2)+'</div><div class="l">建议前胎压 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(tr,2)+'</div><div class="l">建议后胎压 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+(df>=0?'+':'')+fmtNum(df,2)+'</div><div class="l">前轮差额 (bar)</div></div>'+
    '<div class="dist-card"><div class="v">'+(dr>=0?'+':'')+fmtNum(dr,2)+'</div><div class="l">后轮差额 (bar)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核算公式</div>'+
    '<div class="fb-row">目标胎压 = 标贴标准 + 载重修正 + 季节修正</div>'+
    '<div class="fb-row">载重修正：空载 0 / 半载 +0.1 / 满载 +0.2 bar</div>'+
    '<div class="fb-row">季节修正：冬季 +0.1 / 常温 0 / 夏季 −0.05 bar</div>'+
    '<div class="fb-row">差额 = 目标 − 实测（正值需补气，负值需放气）</div>'+
    '<div class="fb-row">单位换算：psi = bar × 14.5038；kPa = bar × 100</div>';
  var ad='';
  var worst=Math.max(Math.abs(df),Math.abs(dr));
  if(worst<0.05){ ad='<div class="tip-success">✅ 四轮均接近目标值，无需调整，保持每月冷态复测一次。</div>'; }
  else if(worst<=0.2){ ad='<div class="tip-info">ℹ️ 存在小幅偏差（最大 '+fmtNum(worst,2)+' bar），建议按差额补齐或放气后复测。</div>'; }
  else{ ad='<div class="tip-warn">⚠️ 偏差较大（最大 '+fmtNum(worst,2)+' bar）：胎压过低会费油、胎肩偏磨甚至驻波爆胎；过高会中央偏磨、抓地下降。请尽快调整并排查慢漏气。</div>'; }
  if(df<0||dr<0){ ad+='<div class="tip-warn">⚠️ 实测低于目标，注意排查气门嘴、胎唇与扎钉导致的慢漏气。</div>'; }
  A.innerHTML=ad;
}
calc();'''

# ---------------------------------------------------------------- oil-change
OIL_CHANGE_INPUTS = '''    <div class="input-row">
      <div><label>机油类型</label><select id="oType" onchange="calc()">
        <option value="mineral">矿物油</option>
        <option value="semi" selected>半合成</option>
        <option value="full">全合成</option>
      </select></div>
      <div><label>年行驶里程 (km)</label><input type="number" id="yearKm" value="15000" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>用车工况</label><select id="cond" onchange="calc()">
        <option value="highway">高速畅通为主</option>
        <option value="city" selected>城市一般路况</option>
        <option value="jam">长期拥堵 / 短途</option>
      </select></div>
      <div><label>是否涡轮增压</label><select id="turbo" onchange="calc()">
        <option value="no" selected>否（自然吸气）</option>
        <option value="yes">是（涡轮增压）</option>
      </select></div>
    </div>
    <div class="input-row">
      <div><label>当前里程 (km)</label><input type="number" id="curKm" value="30000" oninput="calc()" min="0" step="any"></div>
      <div><label>距上次换油已行驶 (km)</label><input type="number" id="doneKm" value="3000" oninput="calc()" min="0" step="any"></div>
    </div>'''

OIL_CHANGE_CARDS = '''  <div class="card">
    <h3>📖 机油类型基础周期与修正系数</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">机油类型</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">基础里程</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">时间上限</th>
      </tr>
      <tr><td style="padding:6px 8px;">矿物油</td><td style="padding:6px 8px;">5000 km</td><td style="padding:6px 8px;">6 个月</td></tr>
      <tr><td style="padding:6px 8px;">半合成</td><td style="padding:6px 8px;">7500 km</td><td style="padding:6px 8px;">8 个月</td></tr>
      <tr><td style="padding:6px 8px;">全合成</td><td style="padding:6px 8px;">10000 km</td><td style="padding:6px 8px;">12 个月</td></tr>
    </table>
    <div class="scene-card">
      <h4>🚦 工况系数</h4>
      <p>高速畅通 ×1.15（机油工况好）；城市一般 ×1.0；长期拥堵短途 ×0.75（冷启动多、燃油稀释与油泥更快累积）。</p>
    </div>
    <div class="scene-card">
      <h4>🌀 涡轮增压</h4>
      <p>涡轮转速高、油温高，机油劣化更快，周期统一 ×0.85，并优先选用符合厂家认证的全合成油。</p>
    </div>
    <div class="info-box">💡 里程与时间「先到为准」：即便里程未到，超过时间上限也应更换，因为机油氧化与添加剂衰减不可逆。</div>
  </div>'''

OIL_CHANGE_JS = H + '''
var BASE={mineral:{km:5000,mon:6},semi:{km:7500,mon:8},full:{km:10000,mon:12}};
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var type=str('oType'),yearKm=val('yearKm'),cur=val('curKm'),done=val('doneKm');
  var cond=str('cond'),turbo=str('turbo');
  if(isNaN(yearKm)||isNaN(cur)||isNaN(done)||yearKm<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的里程数据</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var b=BASE[type];
  var cf=(cond==='highway')?1.15:(cond==='jam'?0.75:1.0);
  var tf=(turbo==='yes')?0.85:1.0;
  var km=Math.round(b.km*cf*tf/500)*500;
  if(km<1000){ km=1000; }
  var mon=b.mon;
  if(cf<1){ mon=Math.round(b.mon*0.85); }
  if(turbo==='yes'){ mon=Math.round(mon*0.9); }
  var perYear=Math.ceil(yearKm/km);
  var next=cur+km;
  var left=km-done;
  var months=km/(yearKm/12);
  var stat=(left<=0)?'已到期':'剩余 '+fmtNum(left,0)+' km';
  R.innerHTML='<div class="safe-val">建议 '+fmtNum(km,0)+' km / '+mon+' 个月</div><div class="safe-sub">'+stat+(left<=0?'，请尽快更换':'')+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(km,0)+'</div><div class="l">建议换油里程 (km)</div></div>'+
    '<div class="dist-card"><div class="v">'+mon+'</div><div class="l">时间上限 (月)</div></div>'+
    '<div class="dist-card"><div class="v">'+perYear+'</div><div class="l">年换油次数 (次)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(next,0)+'</div><div class="l">下次换油里程 (km)</div></div>';
  F.innerHTML=
    '<div class="fb-title">计算规则</div>'+
    '<div class="fb-row">建议里程 = 基础里程 × 工况系数 × 涡轮系数（四舍五入至 500km）</div>'+
    '<div class="fb-row">基础里程：矿物 5000 / 半合成 7500 / 全合成 10000 km</div>'+
    '<div class="fb-row">工况系数：高速 ×1.15 / 城市 ×1.0 / 拥堵短途 ×0.75；涡轮 ×0.85</div>'+
    '<div class="fb-row">年换油次数 = 年里程 ÷ 建议里程（向上取整）</div>'+
    '<div class="fb-row">本次：'+fmtNum(km,0)+' km 约合 '+fmtNum(months,1)+' 个月，下次约在 '+fmtNum(next,0)+' km 或更早（先到为准）</div>';
  var ad='';
  if(left<=0){ ad='<div class="tip-warn">⚠️ 距上次换油已行驶 '+fmtNum(done,0)+' km，已超过建议里程，请尽快更换机油与机滤。</div>'; }
  else if(left<=km*0.2){ ad='<div class="tip-info">ℹ️ 已接近换油里程（剩余 '+fmtNum(left,0)+' km），可安排近期保养。</div>'; }
  else{ ad='<div class="tip-success">✅ 距下次换油还有约 '+fmtNum(left,0)+' km，正常使用即可。</div>'; }
  if(cond==='jam'){ ad+='<div class="tip-warn">⚠️ 长期拥堵短途属于「严苛工况」，即便里程很低也建议按时间上限换油。</div>'; }
  A.innerHTML=ad;
}
calc();'''

# ---------------------------------------------------------------- wear-brake
BRAKE_INPUTS = '''    <div class="input-row">
      <div><label>新品盘厚 (mm)</label><input type="number" id="nw" value="25" oninput="calc()" step="0.1" min="0"></div>
      <div><label>当前盘厚 (mm)</label><input type="number" id="cu" value="23.5" oninput="calc()" step="0.1" min="0"></div>
    </div>
    <div class="input-row">
      <div><label>MIN 极限厚度 (mm)</label><input type="number" id="min" value="22" oninput="calc()" step="0.1" min="0"></div>
      <div><label>盘面跳动量 (mm)</label><input type="number" id="run" value="0.03" oninput="calc()" step="0.01" min="0"></div>
    </div>
    <div class="input-row">
      <div><label>本盘已行驶里程 (万 km)</label><input type="number" id="km" value="6" oninput="calc()" step="0.1" min="0"></div>
      <div><label>刹车片剩余厚度 (mm，可留空)</label><input type="number" id="pad" value="8" oninput="calc()" step="0.1" min="0"></div>
    </div>'''

BRAKE_CARDS = '''  <div class="card">
    <h3>📖 盘厚、跳动量与判定标准</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">检查项</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">正常</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">处置</th>
      </tr>
      <tr><td style="padding:6px 8px;">剩余厚度</td><td style="padding:6px 8px;">高于 MIN + 0.5mm</td><td style="padding:6px 8px;">继续使用，按里程复查</td></tr>
      <tr><td style="padding:6px 8px;">剩余厚度</td><td style="padding:6px 8px;">MIN ~ MIN+0.5mm</td><td style="padding:6px 8px;">临近极限，安排下次保养换盘</td></tr>
      <tr><td style="padding:6px 8px;">剩余厚度</td><td style="padding:6px 8px;">低于 MIN</td><td style="padding:6px 8px;">必须立即更换</td></tr>
      <tr><td style="padding:6px 8px;">盘面跳动</td><td style="padding:6px 8px;">0.03 ~ 0.05mm</td><td style="padding:6px 8px;">可光盘一次（光盘后须仍高于 MIN）</td></tr>
      <tr><td style="padding:6px 8px;">盘面跳动</td><td style="padding:6px 8px;">大于 0.05mm</td><td style="padding:6px 8px;">高速易抖，直接换盘</td></tr>
    </table>
    <div class="scene-card">
      <h4>🧰 盘与片要配对</h4>
      <p>新片配旧盘（盘面有沟槽）会降低贴合面积与散热，建议同轴成对更换，或至少对旧盘做一次光盘处理。</p>
    </div>
    <div class="scene-card">
      <h4>📉 磨损率怎么估</h4>
      <p>磨损率 = 已磨厚度 ÷ 已行驶里程。市区频繁制动、山路下坡、重载都会显著抬高磨损率，据此推算的剩余寿命仅作参考。</p>
    </div>
    <div class="info-box">💡 厚度须用千分尺或卡尺在盘面多点测量取最小值；跳动量须拆轮后用百分表测。目视或手摸不可替代实测。</div>
  </div>'''

BRAKE_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var nw=val('nw'),cu=val('cu'),mn=val('min'),run=parseFloat(document.getElementById('run').value);
  var km=val('km'),pad=parseFloat(document.getElementById('pad').value);
  if(isNaN(nw)||isNaN(cu)||isNaN(mn)||nw<=0||nw<=mn){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效厚度（新品盘厚须大于 MIN）</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var total=nw-mn;
  var worn=nw-cu;
  var left=cu-mn;
  var rate=(km>0)?worn/km:0;
  var remainKm=(rate>0&&left>0)?left/rate:null;
  var pct=(total>0)?worn/total*100:0;
  var st,cls;
  if(left<=0){ st='已达极限 · 必须换盘'; cls='tip-warn'; }
  else if(left<=0.5){ st='临近极限 · 尽快换盘'; cls='tip-warn'; }
  else if(!isNaN(run)&&run>0.05){ st='跳动超差 · 建议换盘'; cls='tip-warn'; }
  else if(!isNaN(run)&&run>=0.03){ st='跳动偏大 · 可光盘一次'; cls='tip-info'; }
  else{ st='状态正常 · 继续使用'; cls='tip-success'; }
  R.innerHTML='<div class="safe-val">'+st+'</div><div class="safe-sub">剩余可磨 '+fmtNum(left,1)+' mm · 已磨 '+fmtNum(pct,0)+'%</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(left,1)+'</div><div class="l">剩余可磨量 (mm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(worn,1)+'</div><div class="l">已磨厚度 (mm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(pct,0)+'%</div><div class="l">磨损占比</div></div>'+
    '<div class="dist-card"><div class="v">'+(remainKm!=null?fmtNum(remainKm,1):'--')+'</div><div class="l">预计剩余里程 (万 km)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">剩余可磨量 = 当前盘厚 − MIN 极限</div>'+
    '<div class="fb-row">磨损率 = (新品盘厚 − 当前盘厚) ÷ 已行驶里程</div>'+
    '<div class="fb-row">预计剩余里程 = 剩余可磨量 ÷ 磨损率</div>'+
    '<div class="fb-row">判定：剩余 ≤ 0 必须换；剩余 ≤ 0.5mm 临近；跳动 &gt; 0.05mm 直接换盘</div>';
  var ad='<div class="'+cls+'">'+((cls==='tip-warn')?'⚠️ ':(cls==='tip-success'?'✅ ':'ℹ️ '))+st+'</div>';
  if(!isNaN(run)&&run>0.05){ ad+='<div class="tip-warn">⚠️ 跳动量 '+fmtNum(run,2)+' mm 超出常规上限：高速制动方向盘抖动的典型来源，换盘前先确认轮毂结合面清洁无锈。'; }
  if(!isNaN(pad)&&pad>0&&pad<=3){ ad+='<div class="tip-warn">⚠️ 刹车片仅剩 '+fmtNum(pad,1)+' mm，已接近更换线（通常 3mm），建议与盘一并处理。</div>'; }
  if(left>0.5&&left<=1.5){ ad+='<div class="tip-info">ℹ️ 剩余量进入后半程，下次保养请复测厚度与跳动量。</div>'; }
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='engine-oil', title='机油黏度规格选择', icon='🛢️',
         desc='输入环境温度范围与发动机类型，推荐合适的 SAE 黏度等级与 API 规格标准。',
         inputs=ENG_OIL_INPUTS, cards=ENG_OIL_CARDS,
         notes='推荐结果为按气候与车况推算的合理区间，实际请以随车保养手册为准',
         js=ENG_OIL_JS),
    dict(slug='tire-pressure', title='标准胎压查询与核算', icon='⚙️',
         desc='按车门标贴标准胎压，结合载重与季节核算目标胎压，并对比实测值给出补放气建议。',
         inputs=TIRE_INPUTS, cards=TIRE_CARDS,
         notes='胎压须在冷胎状态测量，热胎读数不能直接对照标贴标准',
         js=TIRE_JS),
    dict(slug='oil-change', title='机油更换周期计算', icon='🔧',
         desc='按机油类型、用车工况与涡轮增压情况，计算建议换油里程、时间上限与年换油次数。',
         inputs=OIL_CHANGE_INPUTS, cards=OIL_CHANGE_CARDS,
         notes='里程与时间先到为准，严苛工况即使里程未到也应按时间上限更换',
         js=OIL_CHANGE_JS),
    dict(slug='wear-brake', title='刹车盘磨损与更换', icon='🛑',
         desc='按盘厚、MIN 极限与跳动量判断刹车盘能否继续使用，并估算剩余可磨寿命。',
         inputs=BRAKE_INPUTS, cards=BRAKE_CARDS,
         notes='厚度须多点实测取最小值，跳动量须用百分表测量，不可目视替代',
         js=BRAKE_JS),
]


def accent_of(slug):
    """从原文件 meta toolbox 提取 bg 作为 accent 色。"""
    p = os.path.join(ROOT, 'tools/automotive', slug + '.html')
    s = open(p, encoding='utf-8').read()
    m = re.search(r'industry=automotive(?:,icon=[^,]*)?,bg=([^"\s]+)', s)
    return m.group(1) if m else '#FF6B35'


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        t['accent'] = accent_of(slug)
        good, msg = L.rebuild(slug, **t)
        print('%-18s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch1: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
