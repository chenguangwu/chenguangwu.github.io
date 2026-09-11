#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建 · 批次 3（depreciation / loan-calculator / insurance-premium-estimator）。

depreciation 支持直线法、双倍余额递减法、年数总和法，并输出逐年折旧明细表；
loan-calculator 按购车总成本口径（裸车+购置税+附加费+贷款利息）计算，支持等额本息/等额本金；
insurance-premium-estimator 按交强险基础保费 + NCD 系数 + 商业险粗估。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_shell_lib as L  # noqa: E402

H = L.JS_HELPERS

# ------------------------------------------------------------- depreciation
DEP_INPUTS = '''    <div class="input-row">
      <div><label>裸车价 (万元)</label><input type="number" id="price" value="20" oninput="calc()" min="0" step="any"></div>
      <div><label>预计残值率 (%)</label><input type="number" id="res" value="5" oninput="calc()" min="0" max="100" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>使用年限 (年)</label><input type="number" id="years" value="5" oninput="calc()" min="1" step="1"></div>
      <div><label>已使用 (年)</label><input type="number" id="used" value="3" oninput="calc()" min="0" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>折旧方法</label><select id="method" onchange="calc()">
        <option value="straight" selected>直线法（每年等额）</option>
        <option value="ddb">双倍余额递减法（前期快）</option>
        <option value="soy">年数总和法（加速）</option>
      </select></div>
      <div><label>每年行驶里程 (万 km)</label><input type="number" id="kmY" value="1.5" oninput="calc()" min="0" step="any"></div>
    </div>'''

DEP_CARDS = '''  <div class="card">
    <h3>📖 三种折旧方法对比</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">方法</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">年折旧规律</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">适用</th>
      </tr>
      <tr><td style="padding:6px 8px;">直线法</td><td style="padding:6px 8px;">每年等额，最易理解</td><td style="padding:6px 8px;">个人估残值、简单核算</td></tr>
      <tr><td style="padding:6px 8px;">双倍余额递减</td><td style="padding:6px 8px;">按净值 × (2÷年限)，最后两年改直线</td><td style="padding:6px 8px;">企业资产、体现早期消耗</td></tr>
      <tr><td style="padding:6px 8px;">年数总和</td><td style="padding:6px 8px;">按剩余年数占比递减</td><td style="padding:6px 8px;">加速折旧、税收筹划</td></tr>
    </table>
    <div class="scene-card">
      <h4>📉 新车第一年跌最多</h4>
      <p>新车落地即转二手，购置税、保险、上牌等附加成本不计入二手车价，首年折旧常达 15%~25%，之后逐年趋缓。</p>
    </div>
    <div class="scene-card">
      <h4>💱 公式法与行情法</h4>
      <p>公式法反映资产消耗节奏，但真实卖价更受品牌保值率、里程、车况与市场供需影响。定价时结合二手车平台同年份同款报价。</p>
    </div>
    <div class="info-box">💡 卖车估残值建议用「直线法 + 市场行情」双对照；企业做账与税务处理则须按财务制度选定方法并保持一致。</div>
  </div>'''

DEP_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var price=val('price'),res=val('res'),years=Math.round(val('years')),used=Math.round(val('used'));
  var method=str('method'),kmY=val('kmY');
  if(isNaN(price)||isNaN(res)||isNaN(years)||price<=0||years<1){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的车价与年限</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  if(used<0){ used=0; }
  var residual=price*res/100;
  var dep=[],net=[],cur=price,i,d;
  if(method==='straight'){
    d=(price-residual)/years;
    for(i=1;i<=years;i++){ dep.push(d); cur-=d; net.push(cur); }
  } else if(method==='ddb'){
    for(i=1;i<=years;i++){
      if(i>years-2){ d=(cur-residual)/(years-i+1); }
      else { d=cur*(2/years); }
      if(cur-d<residual){ d=cur-residual; }
      if(d<0){ d=0; }
      dep.push(d); cur-=d; net.push(cur);
    }
  } else {
    var sum=years*(years+1)/2;
    for(i=1;i<=years;i++){ d=(price-residual)*(years-i+1)/sum; dep.push(d); cur-=d; net.push(cur); }
  }
  var acc=0;
  for(i=0;i<used&&i<years;i++){ acc+=dep[i]; }
  var book=(used<=0)?price:((used>=years)?residual:net[used-1]);
  var first=dep[0];
  var perKm=(kmY>0)?(acc/(used>0?used:1))/(kmY):0;
  R.innerHTML='<div class="safe-val">当前残值约 '+fmtNum(book,2)+' 万元</div>'+
    '<div class="safe-sub">第 1 年折旧 '+fmtNum(first,2)+' 万元 · 累计折旧 '+fmtNum(acc,2)+' 万元</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(book,2)+'</div><div class="l">当前账面残值 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(first,2)+'</div><div class="l">第 1 年折旧 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(acc,2)+'</div><div class="l">累计折旧 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(residual,2)+'</div><div class="l">预计残值下限 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(acc/(used>0?used:1),2)+'</div><div class="l">年均折旧 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(perKm,2)+'</div><div class="l">每万 km 折旧 (万元)</div></div>';
  F.innerHTML=
    '<div class="fb-title">折旧公式</div>'+
    '<div class="fb-row">直线法：年折旧 =（车价 − 残值）÷ 使用年限</div>'+
    '<div class="fb-row">双倍余额递减：年折旧 = 期初净值 ×（2 ÷ 使用年限），最后两年改按剩余净值均摊</div>'+
    '<div class="fb-row">年数总和：第 k 年折旧 =（车价 − 残值）×（年限 − k + 1）÷ 年限×(年限+1)÷2</div>'+
    '<div class="fb-row">当前净值 = 车价 − 累计折旧</div>';
  var rows='';
  for(i=0;i<years;i++){
    rows+='<tr><td style="padding:5px 8px;">第 '+(i+1)+' 年</td>'+
      '<td style="padding:5px 8px;">'+fmtNum(dep[i],2)+'</td>'+
      '<td style="padding:5px 8px;">'+fmtNum(net[i],2)+'</td>'+
      '<td style="padding:5px 8px;">'+(i+1<=used?'已计提':'未计提')+'</td></tr>';
  }
  A.innerHTML='<div class="tip-info">ℹ️ 折旧明细（单位：万元）</div>'+
    '<table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:6px;">'+
    '<tr><th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">年度</th>'+
    '<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">本年折旧</th>'+
    '<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">期末净值</th>'+
    '<th style="text-align:left;padding:5px 8px;border-bottom:1px solid var(--border,#e5e7eb);">状态</th></tr>'+rows+'</table>'+
    '<div class="tip-info" style="margin-top:8px;">ℹ️ 残值率越低、年限越短，前期折旧越猛。真实卖价还受品牌保值率与车况影响，建议对照二手车行情。</div>';
}
calc();'''

# ------------------------------------------------------------ loan-calculator
LOAN_INPUTS = '''    <div class="input-row">
      <div><label>裸车价 (万元)</label><input type="number" id="price" value="15" oninput="calc()" min="0" step="any"></div>
      <div><label>购置税率 (%)</label><input type="number" id="tax" value="8.85" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>保险+上牌+装潢等附加 (万元)</label><input type="number" id="extra" value="0.8" oninput="calc()" min="0" step="any"></div>
      <div><label>首付比例 (%)</label><input type="number" id="dp" value="30" oninput="calc()" min="0" max="100" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>贷款年限 (年)</label><input type="number" id="years" value="3" oninput="calc()" min="1" step="1"></div>
      <div><label>年化利率 (%)</label><input type="number" id="rate" value="4.8" oninput="calc()" min="0" step="any"></div>
    </div>
    <div class="input-row">
      <div><label>还款方式</label><select id="mode" onchange="calc()">
        <option value="equal" selected>等额本息（每月固定）</option>
        <option value="principal">等额本金（前期多后期少）</option>
      </select></div>
      <div><label>额外手续费 (元)</label><input type="number" id="fee" value="0" oninput="calc()" min="0" step="1"></div>
    </div>'''

LOAN_CARDS = '''  <div class="card">
    <h3>📖 购车落地成本构成</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">项目</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">口径</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">裸车价</td><td style="padding:6px 8px;">经销商成交价</td><td style="padding:6px 8px;">非厂商指导价，可谈</td></tr>
      <tr><td style="padding:6px 8px;">购置税</td><td style="padding:6px 8px;">不含税价 × 10%</td><td style="padding:6px 8px;">约为裸车价的 8.85%</td></tr>
      <tr><td style="padding:6px 8px;">保险 / 上牌</td><td style="padding:6px 8px;">首年商业险 + 交强险 + 牌证</td><td style="padding:6px 8px;">新能源车常免购置税</td></tr>
      <tr><td style="padding:6px 8px;">贷款利息</td><td style="padding:6px 8px;">随贷款额与年限变化</td><td style="padding:6px 8px;">零息促销需核手续费</td></tr>
    </table>
    <div class="scene-card">
      <h4>⚖️ 等额本息 vs 等额本金</h4>
      <p>等额本金每月还的本金固定，利息随余额递减，总利息更少但首月压力大；等额本息每月固定，前期利息占比高，总利息略多。资金紧张选本息，宽裕选本金。</p>
    </div>
    <div class="scene-card">
      <h4>🧾 别被「月费率」误导</h4>
      <p>信用卡分期常用月费率，因本金在递减，月费率×12 不等于真实年化。用月供反推 IRR 才是真实资金成本。</p>
    </div>
    <div class="info-box">💡 本工具按「落地总成本 = 裸车 + 购置税 + 附加费 + 贷款利息 + 手续费」口径，便于与全款购车横向比较。</div>
  </div>'''

LOAN_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var price=val('price'),tax=val('tax'),extra=val('extra');
  var dp=val('dp'),years=Math.round(val('years')),rate=val('rate'),fee=val('fee'),mode=str('mode');
  if(isNaN(price)||isNaN(dp)||isNaN(years)||price<=0||years<1){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的车价与年限</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var priceY=price*10000;
  var taxAmtY=priceY*(tax>0?tax:0)/100;
  var downY=priceY*dp/100;
  var loanY=priceY-downY;
  var n=years*12;
  var r=(rate>0?rate:0)/100/12;
  var monthly=0,totalInterest=0,firstPay=0,lastPay=0;
  if(mode==='principal'){
    var prinY=loanY/n;
    totalInterest=loanY*r*(n+1)/2;
    firstPay=prinY+loanY*r;
    lastPay=prinY+(loanY-(n-1)*prinY)*r;
    monthly=firstPay;
  } else {
    if(r>0){ monthly=loanY*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1); }
    else { monthly=loanY/n; }
    totalInterest=monthly*n-loanY;
    firstPay=monthly; lastPay=monthly;
  }
  var feeY=(fee>0?fee:0);
  var landingY=priceY+taxAmtY+((extra>0?extra:0)*10000);
  var totalY=landingY+totalInterest+feeY;
  var down=downY/10000, loan=loanY/10000;
  var landing=landingY/10000, total=totalY/10000;
  R.innerHTML='<div class="safe-val">月供 '+fmtNum(mode==='principal'?firstPay:monthly,0)+' 元'+(mode==='principal'?'起':'')+'</div>'+
    '<div class="safe-sub">落地 '+fmtNum(landing,2)+' 万 · 含息总计 '+fmtNum(total,2)+' 万</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(loan,2)+'</div><div class="l">贷款本金 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(down,2)+'</div><div class="l">首付金额 (万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(monthly,0)+'</div><div class="l">'+(mode==='principal'?'首月月供':'每月月供')+' (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(totalInterest,0)+'</div><div class="l">贷款总利息 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(landing,2)+'</div><div class="l">落地价（不含息）(万元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(total,2)+'</div><div class="l">含息总支出 (万元)</div></div>';
  F.innerHTML=
    '<div class="fb-title">计算口径</div>'+
    '<div class="fb-row">购置税 = 裸车价 × 购置税率（默认 8.85%，即不含税价的 10%）</div>'+
    '<div class="fb-row">贷款本金 = 裸车价 − 首付；期数 = 贷款年限 × 12</div>'+
    '<div class="fb-row">等额本息月供 = P × r × (1+r)ⁿ ÷ [(1+r)ⁿ − 1]</div>'+
    '<div class="fb-row">等额本金总利息 = P × r × (n+1) ÷ 2，首月月供最高、逐月递减</div>'+
    '<div class="fb-row">落地价 = 裸车价 + 购置税 + 附加费；含息总支出 = 落地价 + 总利息 + 手续费</div>'+
    '<div class="fb-row">本次：本金 '+fmtNum(loan,2)+' 万元 / '+n+' 期，'+(mode==='principal'?'首月 '+fmtNum(firstPay,0)+' 元、末月 '+fmtNum(lastPay,0)+' 元':'每月 '+fmtNum(monthly,0)+' 元')+'</div>';
  var ad='';
  if(mode==='principal'){ ad='<div class="tip-info">ℹ️ 等额本金总利息 '+fmtNum(totalInterest,0)+' 元，较等额本息更省，但首月需 '+fmtNum(firstPay,0)+' 元，请确认现金流可承受。</div>'; }
  else{ ad='<div class="tip-info">ℹ️ 等额本息每月固定 '+fmtNum(monthly,0)+' 元，便于记账；若资金宽裕可考虑提前还款或改等额本金以降息。</div>'; }
  var ratio=(total>0)?(totalInterest/10000)/total*100:0;
  ad+='<div class="tip-info">ℹ️ 利息占含息总支出约 '+fmtNum(ratio,1)+'%，零息促销时请重点核对手续费与实际利率。</div>';
  A.innerHTML=ad;
}
calc();'''

# ----------------------------------------------- insurance-premium-estimator
INS_INPUTS = '''    <div class="input-row">
      <div><label>车辆价格 (万元)</label><input type="number" id="price" value="15" oninput="calc()" min="0" step="any"></div>
      <div><label>使用性质</label><select id="useType" onchange="calc()">
        <option value="p6" selected>家用 6 座以下</option>
        <option value="p6up">家用 6 座及以上</option>
        <option value="biz">营运 / 网约车</option>
      </select></div>
    </div>
    <div class="input-row">
      <div><label>三者险额度</label><select id="third" onchange="calc()">
        <option value="100">100 万</option>
        <option value="200" selected>200 万</option>
        <option value="300">300 万</option>
        <option value="500">500 万</option>
      </select></div>
      <div><label>是否投保车损险</label><select id="damage" onchange="calc()">
        <option value="yes" selected>是</option>
        <option value="no">否</option>
      </select></div>
    </div>
    <div class="input-row">
      <div><label>车上人员每座保额 (万)</label><input type="number" id="seatAmt" value="1" oninput="calc()" min="0" step="1"></div>
      <div><label>座位数</label><input type="number" id="seats" value="5" oninput="calc()" min="1" step="1"></div>
    </div>
    <div class="input-row">
      <div><label>投保地区</label><select id="area" onchange="calc()">
        <option value="1.1">一线城市</option>
        <option value="1.0" selected>二线城市</option>
        <option value="0.9">其他地区</option>
      </select></div>
      <div><label>连续未出险年数</label><select id="ncd" onchange="calc()">
        <option value="1.0">新保 / 上年出险</option>
        <option value="0.85">1 年未出险</option>
        <option value="0.7">2 年未出险</option>
        <option value="0.6" selected>3 年及以上未出险</option>
      </select></div>
    </div>'''

INS_CARDS = '''  <div class="card">
    <h3>📖 险种与额度参考</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px;">
      <tr>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">险种</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">建议额度</th>
        <th style="text-align:left;padding:6px 8px;border-bottom:1px solid var(--border,#e5e7eb);">说明</th>
      </tr>
      <tr><td style="padding:6px 8px;">交强险</td><td style="padding:6px 8px;">强制投保</td><td style="padding:6px 8px;">6 座以下家用基准 950 元</td></tr>
      <tr><td style="padding:6px 8px;">三者险</td><td style="padding:6px 8px;">200 万起，一线建议 300 万+</td><td style="padding:6px 8px;">人伤赔付标准逐年走高</td></tr>
      <tr><td style="padding:6px 8px;">车损险</td><td style="padding:6px 8px;">新车建议投保</td><td style="padding:6px 8px;">已并入盗抢、玻璃、涉水等责任</td></tr>
      <tr><td style="padding:6px 8px;">车上人员</td><td style="padding:6px 8px;">司机 10 万起</td><td style="padding:6px 8px;">保额低、边际成本低</td></tr>
    </table>
    <div class="scene-card">
      <h4>📉 无赔款优待（NCD）</h4>
      <p>连续未出险年数越长，商业险折扣越大，最高可达基准的 6 折。出险一次即回退甚至上浮，小刮擦自费修常比走保险划算。</p>
    </div>
    <div class="scene-card">
      <h4>🧭 地区与车型系数</h4>
      <p>一线城市赔付标准高、费率上浮；车型风险等级（零整比、被盗率）也影响车损险费率，豪华车零整比高，保费显著更高。</p>
    </div>
    <div class="info-box">⚠️ 本工具为粗估口径（基准费率 + NCD + 地区系数），实际保费以保险公司核保报价为准，不同公司差异可达 20% 以上。</div>
  </div>'''

INS_JS = H + '''
function calc(){
  var R=document.getElementById('result'),G=document.getElementById('distGrid'),
      F=document.getElementById('formulaBox'),A=document.getElementById('adviceBox');
  var price=val('price'),seatAmt=val('seatAmt'),seats=Math.round(val('seats'));
  var useType=str('useType'),third=str('third'),damage=str('damage');
  var area=parseFloat(str('area')),ncd=parseFloat(str('ncd'));
  if(isNaN(price)||price<=0||isNaN(seats)||seats<1){
    R.innerHTML='<div class="safe-val">--</div><div class="safe-sub">请输入有效的车价与座位数</div>';
    G.innerHTML='';F.innerHTML='';A.innerHTML='';return;
  }
  var baseCtp=(useType==='p6')?950:(useType==='p6up'?1100:1800);
  var ctp=baseCtp*ncd;
  var damageFee=(damage==='yes')?price*1.2/100*area*ncd:0;
  var thirdMap={100:900,200:1200,300:1500,500:2000};
  var thirdFee=(thirdMap[third]||1200)*area*ncd;
  var seatFee=(seatAmt>0?seatAmt:0)*15*seats*area*ncd;
  var total=ctp+damageFee+thirdFee+seatFee;
  R.innerHTML='<div class="safe-val">合计约 '+fmtNum(total,0)+' 元 / 年</div>'+
    '<div class="safe-sub">交强 '+fmtNum(ctp,0)+' + 车损 '+fmtNum(damageFee,0)+' + 三者 '+fmtNum(thirdFee,0)+' + 人员 '+fmtNum(seatFee,0)+'</div>';
  G.innerHTML=
    '<div class="dist-card"><div class="v">'+fmtNum(ctp,0)+'</div><div class="l">交强险 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(damageFee,0)+'</div><div class="l">车损险 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(thirdFee,0)+'</div><div class="l">三者险 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(seatFee,0)+'</div><div class="l">车上人员 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(total,0)+'</div><div class="l">年度保费合计 (元)</div></div>'+
    '<div class="dist-card"><div class="v">'+fmtNum(price>0?total/(price*10000)*100:0,2)+'%</div><div class="l">占车价比例</div></div>';
  F.innerHTML=
    '<div class="fb-title">估算口径</div>'+
    '<div class="fb-row">交强险 = 基准保费 × NCD 系数（6 座以下家用基准 950 元）</div>'+
    '<div class="fb-row">车损险 ≈ 车价 × 1.2% × 地区系数 × NCD</div>'+
    '<div class="fb-row">三者险：100 万 900 / 200 万 1200 / 300 万 1500 / 500 万 2000，再乘地区与 NCD 系数</div>'+
    '<div class="fb-row">车上人员 ≈ 每座保额(万) × 15 元 × 座位数 × 地区 × NCD</div>'+
    '<div class="fb-row">地区系数：一线 1.1 / 二线 1.0 / 其他 0.9；NCD：3 年未出险 0.6</div>';
  var ad='';
  var thirdW=parseInt(third,10);
  if(thirdW<200){ ad='<div class="tip-warn">⚠️ 三者险建议至少 200 万：人伤与物损赔付标准逐年走高，低额度省小钱可能赔大钱。</div>'; }
  else if(thirdW>=300){ ad='<div class="tip-success">✅ 三者险额度充足，一线城市或豪车密集区建议保持 300 万以上。</div>'; }
  else{ ad='<div class="tip-info">ℹ️ 三者险 200 万属常规配置，若常在一线城市行驶可提高到 300 万，边际成本不高。</div>'; }
  if(ncd>=1.0){ ad+='<div class="tip-info">ℹ️ 当前无 NCD 折扣，保持连续不出险后次年费率会明显下降，小刮擦可权衡自费处理。</div>'; }
  else{ ad+='<div class="tip-info">ℹ️ 已按 '+(ncd===0.6?'3 年及以上':(ncd===0.7?'2 年':'1 年'))+' 未出险计入折扣，维持安全驾驶可继续享受优惠。</div>'; }
  ad+='<div class="tip-warn">⚠️ 粗估结果仅供比价参考，实际保费以保险公司核保报价为准。</div>';
  A.innerHTML=ad;
}
calc();'''

TOOLS = [
    dict(slug='depreciation', title='汽车折旧计算器', icon='🚗', accent='#1e40af',
         desc='支持直线、双倍余额递减与年数总和三种方法估算车辆残值与逐年折旧，辅助卖车定价与资产核算。',
         inputs=DEP_INPUTS, cards=DEP_CARDS,
         notes='公式法结果反映资产消耗节奏，真实成交价还须对照二手车市场行情',
         js=DEP_JS),
    dict(slug='loan-calculator', title='购车总成本计算器', icon='💰', accent='#dc2626',
         desc='综合裸车价、购置税、保险上牌等附加费与贷款利息，计算落地价与含息总支出，支持等额本息与等额本金对比。',
         inputs=LOAN_INPUTS, cards=LOAN_CARDS,
         notes='购置税与保险口径各地各车型不同，请以经销商与保险公司实际报价为准',
         js=LOAN_JS),
    dict(slug='insurance-premium-estimator', title='车辆保险保费估算', icon='🛡️', accent='#0e7490',
         desc='按车辆价格、使用性质、险种组合与 NCD 系数粗估年度保费，辅助投保方案比价与预算。',
         inputs=INS_INPUTS, cards=INS_CARDS,
         notes='本工具为粗估口径，实际保费以保险公司核保报价为准，不同公司差异可达 20% 以上',
         js=INS_JS),
]


def main():
    ok = 0
    for t in TOOLS:
        t = dict(t)
        slug = t.pop('slug')
        good, msg = L.rebuild(slug, **t)
        print('%-30s %s | %s' % (slug, 'OK ' if good else 'FAIL', msg))
        ok += 1 if good else 0
    print('---- batch3: %d/%d ----' % (ok, len(TOOLS)))


if __name__ == '__main__':
    main()
