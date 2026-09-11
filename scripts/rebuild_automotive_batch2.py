#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 2（transport-calculator / fuel-cost-calculator / parking-fee-calculator）。

transport-calculator 按原 desc 做成多模块综合计算器（油费/吨公里/行驶时间/刹车距离/
货物换算/轮胎尺寸）；fuel-cost-calculator 修正英文 title 与占位 desc；parking-fee-calculator
按分段计费 + 封顶规则计算。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

ROOT = L.ROOT
H = L.JS_HELPERS

# --------------------------------------------------------- transport-calculator
TRANSPORT_INPUTS = '''    <div class="input-row">
      <div><label>行驶里程 (km)</label><input type="number" id="km" value="300" oninput="calc()" min="0" step="any"></div>
      <div><label>百公里油耗 (L)</label><input type="number" id="fc" value="20" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>油价 (元/L)</label><input type="number" id="price" value="7.5" oninput="calc()" min="0" step="0.01"></div>
      <div><label>平均车速 (km/h)</label><input type="number" id="speed" value="60" oninput="calc()" min="1" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>额定载重 (吨)</label><input type="number" id="load" value="5" oninput="calc()" min="0" step="any"></div>
      <div><label>实际装载率 (%)</label><input type="number" id="rate" value="60" oninput="calc()" min="0" max="100" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>制动初速 (km/h)</label><input type="number" id="v0" value="60" oninput="calc()" min="0" step="any"></div>
      <div><label>驾驶员反应时间 (s)</label><input type="number" id="rt" value="1" oninput="calc()" min="0" step="0.1"></div>
    </div>
    <div class="input-row">
      <div><label>货物体积 (m³)</label><input type="number" id="vol" value="10" oninput="calc()" min="0" step="any"></div>
      <div><label>货物重量 (吨)</label><input type="number" id="wt" value="6" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>轮胎规格（如 205/55R16）</label><input type="text" id="tire" value="205/55R16" oninput="calc()"></div>
      <div><label>荷载系数（干沥青 6.5 / 湿滑 4.5）</label><input type="number" id="mu" value="6.5" oninput="calc()" min="1" step="0.1"></div>
    </div>'''

TRANSPORT_CARDS = '''  <div class="card">
    <h3>📖 物流成本与安全距离参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">运价档位</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">吨公里成本</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">整车满载长途</td><td style="padding:6px 8px;">0.25 ~ 0.40 元</td><td style="padding:6px 8px;">装载率高，固定成本摊薄</td></tr>
      <tr><td style="padding:6px 8px;">整车半载</td><td style="padding:6px 8px;">0.45 ~ 0.70 元</td><td style="padding:6px 8px;">空载率高，单位成本陡升</td></tr>
      <tr><td style="padding:6px 8px;">零担拼货</td><td style="padding:6px 8px;">0.80 ~ 1.50 元</td><td style="padding:6px 8px;">含分拣、装卸与中转</td></tr>
    </table>
    <div class="scene-card">
      <h4>🛑 刹车距离三要素</h4>
      <p>总停车距离 = 反应距离（车速 × 反应时间）+ 制动距离（v²/2a）。车速翻倍制动距离约变 4 倍，雨天附着系数下降还会进一步拉长。</p>
    </div>
    <div class="scene-card">
      <h4>📦 轻泡货与重货</h4>
      <p>密度低于约 0.3 t/m³ 属轻泡货，按体积计费更亏；高于 1 t/m³ 属重货，受载重限制。报价前先算密度再选计费方式。</p>
    </div>
    <div class="info-box">💡 吨公里成本只含燃油，实为「燃油吨公里成本」。报价还须加折旧、保险、司机工时、路桥费与装卸费，短途零散单这些固定成本占比更高。</div>
  </div>'''

TRANSPORT_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var km=val('km'),fc=val('fc'),price=val('price'),speed=val('speed');
  var load=val('load'),rate=val('rate'),v0=val('v0'),rt=val('rt');
  var vol=val('vol'),wt=val('wt'),mu=val('mu');
  var tire=document.getElementById('tire').value;
  if(isNaN(km)||isNaN(fc)||isNaN(price)||km<=0||fc<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的里程与油耗</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var oilCost=km/100*fc*price;
  var loaded=load*rate/100;
  var tkm=(loaded>0)?oilCost/(loaded*km):0;
  var tkmFull=(load>0)?oilCost/(load*km):0;
  var hours=(speed>0)?km/speed:0;
  var vms=v0/3.6;
  var react=vms*rt;
  var brake=(mu>0)?vms*vms/(2*mu):0;
  var stopDist=react+brake;
  var density=(vol>0)?wt/vol:0;
  var m=tire.match(/(\\d+)\\s*\\/\\s*(\\d+)\\s*R\\s*(\\d+)/i);
  var dia=0,circ=0,side=0;
  if(m){
    var w=parseFloat(m[1]),ar=parseFloat(m[2]),rim=parseFloat(m[3]);
    side=w*ar/100;
    dia=rim*25.4+2*side;
    circ=Math.PI*dia/1000;
  }
  R.innerHTML='<div class="safe-val">油费 '+fmtNum(oilCost,0)+' 元 · 吨公里 '+fmtNum(tkm,2)+' 元</div>'+
    '<div class="safe-sub">装载率 '+fmtNum(rate,0)+'% 下实载 '+fmtNum(loaded,2)+' 吨</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(oilCost,0)+'</div><div class="l">燃油费用 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(tkm,2)+'</div><div class="l">吨公里成本 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(tkmFull,2)+'</div><div class="l">满载吨公里 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(hours,1)+'</div><div class="l">行驶时间 (h)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(stopDist,1)+'</div><div class="l">停车总距离 (m)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(density,2)+'</div><div class="l">货物密度 (t/m³)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(dia,0)+'</div><div class="l">轮胎直径 (mm)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(circ,3)+'</div><div class="l">轮胎周长 (m)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">燃油费用 = 里程 ÷ 100 × 百公里油耗 × 油价</div>'+
    '<div class="fb-row">吨公里成本 = 燃油费用 ÷（实载吨数 × 里程）</div>'+
    '<div class="fb-row">行驶时间 = 里程 ÷ 平均车速</div>'+
    '<div class="fb-row">停车总距离 = 车速 × 反应时间 + 车速² ÷ (2 × 减速度)</div>'+
    '<div class="fb-row">货物密度 = 重量 ÷ 体积</div>'+
    '<div class="fb-row">轮胎直径 = 轮辋直径 × 25.4 + 2 × 断面宽 × 扁平比；周长 = π × 直径</div>';
  var ad='';
  if(tkm>0.8&&rate<80){ ad='<div class="tip-warn">⚠️ 吨公里成本 '+fmtNum(tkm,2)+' 元偏高，主因装载率仅 '+fmtNum(rate,0)+'%。提升装载率或安排回程带货可显著摊薄。</div>'; }
  else if(tkm>0&&tkm<=0.4){ ad='<div class="tip-success">✅ 吨公里成本 '+fmtNum(tkm,2)+' 元，处于整车满载合理区间，运力利用良好。</div>'; }
  else{ ad='<div class="tip-info">ℹ️ 吨公里成本 '+fmtNum(tkm,2)+' 元，属常规水平；注意上述仅含燃油，报价还需覆盖固定成本。</div>'; }
  if(v0>0){ ad+='<div class="tip-info">ℹ️ '+fmtNum(v0,0)+' km/h 时停车总距离约 '+fmtNum(stopDist,1)+' 米（含 '+fmtNum(rt,1)+' 秒反应），请据此保持跟车距离。</div>'; }
  A.innerHTML=ad;
}
calc();'''

# ------------------------------------------------------- fuel-cost-calculator
FUEL_TITLE = '出行油费计算器'
FUEL_DESC = '输入行驶里程、车辆油耗与油价，估算单程油费、每公里成本与人均分摊，并对比不同车型的燃油成本差异。'

FUEL_SUBS = [
    ('<title>Fuel Cost Calculator</title>', '<title>' + FUEL_TITLE + '</title>'),
    ('<meta property="og:title" content="Fuel Cost Calculator">',
     '<meta property="og:title" content="' + FUEL_TITLE + '">'),
    ('<meta name="twitter:title" content="Fuel Cost Calculator">',
     '<meta name="twitter:title" content="' + FUEL_TITLE + '">'),
    ('content="📚 深度解析：Fuel Cost Calculator"', 'content="' + FUEL_DESC + '"'),
    ('"name":"Fuel Cost Calculator"', '"name":"' + FUEL_TITLE + '"'),
]

FUEL_INPUTS = '''    <div class="input-row">
      <div><label>行驶里程 (km)</label><input type="number" id="km" value="300" oninput="calc()" min="0" step="any"></div>
      <div><label>车辆百公里油耗 (L)</label><input type="number" id="fc" value="7" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>油价 (元/L)</label><input type="number" id="price" value="8" oninput="calc()" min="0" step="0.01"></div>
      <div><label>同行人数（含驾驶员）</label><input type="number" id="ppl" value="4" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>对比车型百公里油耗 (L)</label><input type="number" id="fc2" value="9" oninput="calc()" min="0" step="any"></div>
      <div><label>出行预算 (元)</label><input type="number" id="budget" value="300" oninput="calc()" min="0" step="any"></div>
    </div>'''

FUEL_CARDS = '''  <div class="card">
    <h3>📖 油耗来源与费用参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">油耗口径</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">与真实差异</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">适用</th>
      </tr>
      <tr><td style="padding:6px 8px;">工信部/WLTC 工况</td><td style="padding:6px 8px;">普遍偏低 10%~25%</td><td style="padding:6px 8px;">车型横向对比</td></tr>
      <tr><td style="padding:6px 8px;">仪表长期平均</td><td style="padding:6px 8px;">较接近实际</td><td style="padding:6px 8px;">日常预估</td></tr>
      <tr><td style="padding:6px 8px;">两次加油实测</td><td style="padding:6px 8px;">最接近真实</td><td style="padding:6px 8px;">费用精算与报销</td></tr>
    </table>
    <div class="scene-card">
      <h4>🛣️ 高速与市区差异</h4>
      <p>同车高速匀速约 6~7L/100km，市区拥堵可到 9~11L/100km。长途预估建议按高速油耗，市区通勤按实测量。</p>
    </div>
    <div class="scene-card">
      <h4>⚡ 电车如何类比</h4>
      <p>把「油耗 × 油价」换成「百公里电耗 × 电价」，公共快充另加服务费。家充谷电单价低，能源成本优势明显。</p>
    </div>
    <div class="info-box">💡 想算得更准：用最近一次「加满到加满」的加油量与对应里程反推真实百公里油耗，再代入本工具。</div>
  </div>'''

FUEL_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var km=val('km'),fc=val('fc'),price=val('price'),ppl=val('ppl');
  var fc2=val('fc2'),budget=val('budget');
  if(isNaN(km)||isNaN(fc)||isNaN(price)||km<=0||fc<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的里程与油耗</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var cost=km/100*fc*price;
  var perKm=(km>0)?cost/km:0;
  var perP=(ppl>0)?cost/ppl:0;
  var cost2=(!isNaN(fc2)&&fc2>0)?km/100*fc2*price:0;
  var diff=cost2-cost;
  var range=(!isNaN(budget)&&budget>0&&perKm>0)?budget/perKm:0;
  R.innerHTML='<div class="safe-val">'+fmtNum(cost,1)+' 元</div><div class="safe-sub">每公里 '+fmtNum(perKm,2)+' 元 · 人均 '+fmtNum(perP,1)+' 元</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(cost,1)+'</div><div class="l">单程油费 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(perKm,2)+'</div><div class="l">每公里成本 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(perP,1)+'</div><div class="l">人均分摊 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+(diff>=0?'+':'')+fmtNum(diff,1)+'</div><div class="l">对比车型差额 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(cost2,1)+'</div><div class="l">对比车型油费 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(range,0)+'</div><div class="l">预算可行驶 (km)</div></div>';
  F.innerHTML=
    '<div class="fb-title">核心公式</div>'+
    '<div class="fb-row">油费 = 里程 ÷ 100 × 百公里油耗 × 油价</div>'+
    '<div class="fb-row">每公里成本 = 油费 ÷ 里程</div>'+
    '<div class="fb-row">人均分摊 = 油费 ÷ 同行人数</div>'+
    '<div class="fb-row">对比差额 = 对比车型油费 − 本车油费</div>'+
    '<div class="fb-row">预算可行驶里程 = 预算 ÷ 每公里成本</div>';
  var ad='';
  if(diff>0){ ad='<div class="tip-success">✅ 本车比对比车型省 '+fmtNum(diff,1)+' 元（'+fmtNum(km,0)+'km），长里程下车型油耗差会持续放大。</div>'; }
  else if(diff<0){ ad='<div class="tip-warn">⚠️ 本车油费比对比车型高 '+fmtNum(-diff,1)+' 元，若有换车或改走路线打算，可据此评估回收周期。</div>'; }
  else{ ad='<div class="tip-info">ℹ️ 两车油耗一致，费用无差异。</div>'; }
  ad+='<div class="tip-info">ℹ️ 实际油费通常高于估算：市区拥堵、空调、载重与胎压都会抬高油耗，建议用实测油耗代入。</div>';
  A.innerHTML=ad;
}
calc();'''

# ---------------------------------------------------- parking-fee-calculator
PARKING_INPUTS = '''    <div class="input-row">
      <div><label>首时段时长 (分钟)</label><input type="number" id="firstMin" value="60" oninput="calc()" min="1" step="1"></div>
      <div><label>首时段费用 (元)</label><input type="number" id="firstFee" value="10" oninput="calc()" min="0" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>后续计费单位 (分钟)</label><input type="number" id="unitMin" value="30" oninput="calc()" min="1" step="1"></div>
      <div><label>后续单位单价 (元)</label><input type="number" id="unitFee" value="5" oninput="calc()" min="0" step="0.5"></div>
    </div>
    <div class="input-row">
      <div><label>停放时长 (分钟)</label><input type="number" id="parkMin" value="180" oninput="calc()" min="0" step="1"></div>
      <div><label>单日封顶 (元，0 表示不封顶)</label><input type="number" id="cap" value="60" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>免费时长 (分钟，仅首段抵扣)</label><input type="number" id="freeMin" value="0" oninput="calc()" min="0" step="1"></div>
      <div><label>跨天数 (天)</label><input type="number" id="days" value="1" oninput="calc()" min="1" step="1"></div>
    </div>'''

PARKING_CARDS = '''  <div class="card">
    <h3>📖 常见计费规则对照</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">场景</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">典型规则</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">长停策略</th>
      </tr>
      <tr><td style="padding:6px 8px;">商场</td><td style="padding:6px 8px;">首 1 小时免费/半价，消费满额免 1~2 小时</td><td style="padding:6px 8px;">满额免时优先，超时按全时长计</td></tr>
      <tr><td style="padding:6px 8px;">医院</td><td style="padding:6px 8px;">分时段单价，探视时段优惠</td><td style="padding:6px 8px;">按天封顶通常更划算</td></tr>
      <tr><td style="padding:6px 8px;">机场</td><td style="padding:6px 8px;">首 15~30 分钟免费，长停按日封顶</td><td style="padding:6px 8px;">长停选远端车场或按日套餐</td></tr>
      <tr><td style="padding:6px 8px;">路侧泊位</td><td style="padding:6px 8px;">按 15/30 分钟累加，夜间免费</td><td style="padding:6px 8px;">夜间免费时段可省整段费用</td></tr>
    </table>
    <div class="scene-card">
      <h4>🧮 为什么长停反而便宜</h4>
      <p>封顶是按自然日或单次进场设上限。超过某时长后费用不再累加，因此「分段计费总额 &gt; 封顶」时，实际支付即为封顶价。</p>
    </div>
    <div class="scene-card">
      <h4>⏱️ 不足一单位怎么算</h4>
      <p>绝大多数车场对不足一个计费单位的部分按「进一法」收费，即停 61 分钟按 90 分钟计。本工具即按进一法计算。</p>
    </div>
    <div class="info-box">💡 需要跨天停放时，把「跨天数」设为实际天数，费用按每日重新计封顶累加。实际以车场公示牌为准。</div>
  </div>'''

PARKING_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var firstMin=val('firstMin'),firstFee=val('firstFee');
  var unitMin=val('unitMin'),unitFee=val('unitFee');
  var parkMin=val('parkMin'),cap=val('cap'),freeMin=val('freeMin'),days=val('days');
  if(isNaN(parkMin)||isNaN(firstMin)||isNaN(firstFee)||parkMin<0||firstMin<=0){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的时长与费率</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var pay=Math.max(0, parkMin-(freeMin>0?freeMin:0));
  var oneDay, units=0;
  if(pay<=firstMin){ oneDay=firstFee; }
  else{
    units=Math.ceil((pay-firstMin)/unitMin);
    oneDay=firstFee+units*unitFee;
  }
  var cappedDay=(cap>0&&oneDay>cap)?cap:oneDay;
  var d=(days>0)?Math.floor(days):1;
  var total=cappedDay*d;
  var cappedNow=(cap>0&&oneDay>cap);
  R.innerHTML='<div class="safe-val">应付 '+fmtNum(total,1)+' 元</div><div class="safe-sub">单日 '+fmtNum(cappedDay,1)+' 元'+(cappedNow?'（已触发封顶）':'')+(d>1?' × '+d+' 天':'')+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(total,1)+'</div><div class="l">应付总额 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(cappedDay,1)+'</div><div class="l">单日费用 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+units+'</div><div class="l">后续计费单位数</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(pay,0)+'</div><div class="l">计费时长 (分钟)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(firstFee,1)+'</div><div class="l">首段费用 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(units*unitFee,1)+'</div><div class="l">后续费用 (元)</div></div>';
  F.innerHTML=
    '<div class="fb-title">分段计费规则</div>'+
    '<div class="fb-row">计费时长 = 停放时长 − 免费时长</div>'+
    '<div class="fb-row">若计费时长 ≤ 首时段：费用 = 首时段费用</div>'+
    '<div class="fb-row">否则：费用 = 首时段费用 + 进一法（(计费时长 − 首时段) ÷ 单位时长）× 单位单价</div>'+
    '<div class="fb-row">单日费用 = min(分段费用, 单日封顶)</div>'+
    '<div class="fb-row">总额 = 单日费用 × 跨天数</div>';
  var ad='';
  if(cappedNow){ ad='<div class="tip-success">✅ 分段累计已达 '+fmtNum(oneDay,1)+' 元，超过封顶 '+fmtNum(cap,1)+' 元，按封顶计费更划算，本次长停反而摊低了小时均价。</div>'; }
  else if(cap>0&&firstFee+units*unitFee>cap*0.8){ ad='<div class="tip-info">ℹ️ 距离封顶仅差 '+fmtNum(cap-oneDay,1)+' 元，再停不久即触发封顶，可考虑延长停放时间。</div>'; }
  else{ ad='<div class="tip-info">ℹ️ 未触发封顶，按分段规则正常计费。</div>'; }
  if(parkMin>0){ ad+='<div class="tip-info">ℹ️ 折合小时均价约 '+fmtNum(total/(parkMin/60),1)+' 元/小时。</div>'; }
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='transport-calculator', title='交通物流计算器', icon='🚚', accent='#1565c0',
         desc='涵盖刹车距离、油耗成本、货物换算、燃油效率、行驶时间、轮胎尺寸等多种交通物流常用计算。',
         inputs=TRANSPORT_INPUTS, cards=TRANSPORT_CARDS,
         notes='吨公里成本仅含燃油费用，报价须另行覆盖折旧、保险、司机工时与路桥费',
         js=TRANSPORT_JS),
    dict(slug='fuel-cost-calculator', title=FUEL_TITLE, icon='⛽', accent='#0f766e',
         desc=FUEL_DESC, head_subs=FUEL_SUBS,
         inputs=FUEL_INPUTS, cards=FUEL_CARDS,
         notes='油耗建议采用实测值，工况油耗普遍低于真实油耗 10%~25%',
         js=FUEL_JS),
    dict(slug='parking-fee-calculator', title='停车费用计算器（汽车）', icon='🅿️', accent='#7c3aed',
         desc='按首时段、后续计费单位与单日封顶规则计算停车费，支持免费时长与跨天停放，辅助出行成本预算。',
         inputs=PARKING_INPUTS, cards=PARKING_CARDS,
         notes='实际计费以车场公示牌为准，进出场时间与免费规则判定可能存在差异',
         js=PARKING_JS),
]


def fix_deepdive_title():
    """fuel-cost-calculator 的 deep-dive 标题由英文改为中文（键数守恒）。"""
    p = os.path.join(ROOT, 'i18n/tools/content_deepdive.json')
    d = json.load(open(p, encoding='utf-8'))
    n = len(d)
    k = 'automotive/fuel-cost-calculator'
    if k in d and d[k].get('title') == 'Fuel Cost Calculator':
        d[k]['title'] = '出行油费计算'
    assert len(d) == n, '键数变化'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))
    return '%s title=%r 键数=%d' % (k, d[k].get('title'), n)


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-28s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch2: %d/%d ----' % (ok, len(TOOLS)))
    print('deepdive:', fix_deepdive_title())


if __name__ == '__main__':
    main()
