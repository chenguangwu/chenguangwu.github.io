#!/usr/bin/env python3
"""
Generate batch tool files for ToolBox.
Each tool is a self-contained HTML file using common.css + inline JS.
"""
import os
import sys

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')

TOOL_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat={cat},industry={industry},icon={icon},bg={bg}">
<title>{title} - ToolBox</title>
<link rel="stylesheet" href="common.css">
<script src="common.js"></script>
</head>
<body>

<div class="nav">
  <a href="../index.html">← ToolBox</a>
  <span>/ {title}</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>

<div class="container">
  <div class="card">
    <h2>{icon} {title}</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">{desc}</p>
{body}
  </div>
{extra_card}
</div>

<script>
{script}
</script>
</body>
</html>
'''

def make_tool(filename, title, icon, bg, cat, industry, desc, body, script, extra_card=''):
    html = TOOL_TEMPLATE.format(
        title=title, icon=icon, bg=bg, cat=cat, industry=industry,
        desc=desc, body=body, script=script, extra_card=extra_card
    )
    path = os.path.join(TOOLS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path

# ========== FINANCE TOOLS (50) ==========

FINANCE_TOOLS = [
    # Stock/Investment
    ('stock-average-calculator.html', '股票成本计算器', '📈', '#fff8e1', 'finance', 'finance',
     '计算多次买入股票后的平均成本价',
     '''<div class="input-row"><div><label>已买入股数</label><input type="number" id="shares1" value="100" oninput="calc()"></div>
     <div><label>买入均价</label><input type="number" id="price1" value="10" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>加仓股数</label><input type="number" id="shares2" value="50" oninput="calc()"></div>
     <div><label>加仓价格</label><input type="number" id="price2" value="8" step="any" oninput="calc()"></div></div>
     <div class="toolbar"><button class="btn primary" onclick="calc()">计算</button></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const s1=+document.getElementById('shares1').value||0,p1=+document.getElementById('price1').value||0;
       const s2=+document.getElementById('shares2').value||0,p2=+document.getElementById('price2').value||0;
       const ts=s1+s2,tc=s1*p1+s2*p2,ap=ts?tc/ts:0;
       document.getElementById('res').innerHTML=`<p>总投入：<strong>${tc.toFixed(2)}</strong> 元</p><p>总持股：<strong>${ts}</strong> 股</p><p style="font-size:18px;color:var(--primary);">平均成本：<strong>${ap.toFixed(4)}</strong> 元/股</p>`;
     }calc();'''),

    ('position-size-calculator.html', '仓位计算器', '📊', '#fff8e1', 'finance', 'finance',
     '根据风险比例计算股票仓位大小',
     '''<div class="input-row"><div><label>账户资金(元)</label><input type="number" id="capital" value="100000" oninput="calc()"></div>
     <div><label>风险比例(%)</label><input type="number" id="riskPct" value="2" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>买入价(元)</label><input type="number" id="entry" value="50" step="any" oninput="calc()"></div>
     <div><label>止损价(元)</label><input type="number" id="stop" value="48" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const cap=+document.getElementById('capital').value||0;
       const rp=+document.getElementById('riskPct').value||0;
       const entry=+document.getElementById('entry').value||0;
       const stop=+document.getElementById('stop').value||0;
       const riskAmt=cap*rp/100; const riskPer=Math.abs(entry-stop);
       const shares=riskPer?Math.floor(riskAmt/riskPer):0;
       const posVal=shares*entry;
       document.getElementById('res').innerHTML=`<p>可承受亏损：<strong>${riskAmt.toFixed(2)}</strong> 元</p><p>每股风险：<strong>${riskPer.toFixed(2)}</strong> 元</p><p>建议买入：<strong style="font-size:18px;color:var(--primary);">${shares}</strong> 股</p><p>仓位市值：<strong>${posVal.toFixed(2)}</strong> 元</p><p>仓位占比：<strong>${(posVal/cap*100).toFixed(2)}%</strong></p>`;
     }calc();'''),

    ('futures-pnl-calculator.html', '期货盈亏计算器', '📉', '#fff8e1', 'finance', 'finance',
     '计算期货合约盈亏',
     '''<div class="input-row"><div><label>合约乘数</label><input type="number" id="mult" value="10" oninput="calc()"></div>
     <div><label>开仓价</label><input type="number" id="open" value="3000" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>平仓价</label><input type="number" id="close" value="3050" step="any" oninput="calc()"></div>
     <div><label>手数</label><input type="number" id="lots" value="1" oninput="calc()"></div></div>
     <label>方向</label><select id="dir" onchange="calc()"><option value="1">做多</option><option value="-1">做空</option></select>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const m=+document.getElementById('mult').value||0,o=+document.getElementById('open').value||0;
       const c=+document.getElementById('close').value||0,l=+document.getElementById('lots').value||0;
       const d=+document.getElementById('dir').value;
       const pnl=(c-o)*d*m*l;
       const color=pnl>=0?'var(--success)':'var(--danger)';
       document.getElementById('res').innerHTML=`<p style="font-size:20px;color:${color};">盈亏：<strong>${pnl.toFixed(2)}</strong> 元</p><p>波动点数：<strong>${(c-o)*d}</strong> 点</p>`;
     }calc();'''),

    ('profit-margin-calculator.html', '利润率计算器', '💰', '#fff8e1', 'finance', 'finance',
     '计算毛利率和净利润率',
     '''<div class="input-row"><div><label>收入(元)</label><input type="number" id="revenue" value="1000" step="any" oninput="calc()"></div>
     <div><label>成本(元)</label><input type="number" id="cost" value="600" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>运营费用(元)</label><input type="number" id="expenses" value="200" step="any" oninput="calc()"></div>
     <div><label>税率(%)</label><input type="number" id="tax" value="25" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const r=+document.getElementById('revenue').value||0,c=+document.getElementById('cost').value||0;
       const e=+document.getElementById('expenses').value||0,t=+document.getElementById('tax').value||0;
       const gp=r-c, npm=gp-e, taxAmt=npm>0?npm*t/100:0, np=npm-taxAmt;
       const gpm=r?gp/r*100:0, npmPct=r?np/r*100:0;
       document.getElementById('res').innerHTML=`<p>毛利润：<strong>${gp.toFixed(2)}</strong> 元（毛利率 <strong>${gpm.toFixed(2)}%</strong>）</p><p>运营利润：<strong>${npm.toFixed(2)}</strong> 元</p><p>税费：<strong>${taxAmt.toFixed(2)}</strong> 元</p><p style="font-size:18px;color:var(--primary);">净利润：<strong>${np.toFixed(2)}</strong> 元（净利率 <strong>${npmPct.toFixed(2)}%</strong>）</p>`;
     }calc();'''),

    ('currency-converter.html', '实时汇率换算', '💱', '#fff8e1', 'finance', 'finance',
     '常见货币汇率换算（参考汇率）',
     '''<div class="input-row"><div><label>金额</label><input type="number" id="amount" value="100" step="any" oninput="calc()"></div>
     <div><label>从</label><select id="from" onchange="calc()"><option value="CNY" selected>人民币 CNY</option><option value="USD">美元 USD</option><option value="EUR">欧元 EUR</option><option value="JPY">日元 JPY</option><option value="GBP">英镑 GBP</option><option value="HKD">港币 HKD</option><option value="KRW">韩元 KRW</option><option value="AUD">澳元 AUD</option><option value="CAD">加元 CAD</option><option value="SGD">新币 SGD</option></select></div></div>
     <div class="input-row"><div><label>到</label><select id="to" onchange="calc()"><option value="CNY">人民币 CNY</option><option value="USD" selected>美元 USD</option><option value="EUR">欧元 EUR</option><option value="JPY">日元 JPY</option><option value="GBP">英镑 GBP</option><option value="HKD">港币 HKD</option><option value="KRW">韩元 KRW</option><option value="AUD">澳元 AUD</option><option value="CAD">加元 CAD</option><option value="SGD">新币 SGD</option></select></div></div>
     <p style="font-size:11px;color:var(--text-muted);">*参考汇率，实际以银行为准</p>
     <div class="result-box" id="res"></div>''',
     '''const RATES={CNY:1,USD:0.138,EUR:0.127,JPY:21.7,GBP:0.109,HKD:1.08,KRW:190,AUD:0.21,CAD:0.19,SGD:0.185};
     function calc(){
       const amt=+document.getElementById('amount').value||0;
       const f=document.getElementById('from').value,t=document.getElementById('to').value;
       const cny=amt/RATES[f]; const result=cny*RATES[t];
       document.getElementById('res').innerHTML=`<p style="font-size:22px;color:var(--primary);"><strong>${amt} ${f}</strong> = <strong>${result.toFixed(2)} ${t}</strong></p>`;
     }calc();'''),

    ('vat-calculator.html', '增值税计算器', '🧾', '#fff8e1', 'finance', 'finance',
     '计算增值税额和不含税价格',
     '''<div class="input-row"><div><label>金额(元)</label><input type="number" id="amt" value="1000" step="any" oninput="calc()"></div>
     <div><label>税率(%)</label><select id="rate" onchange="calc()"><option value="13" selected>13% (货物)</option><option value="9">9% (建筑/交通)</option><option value="6">6% (服务)</option><option value="3">3% (小规模)</option><option value="1">1% (优惠)</option><option value="0">0% (免税)</option></select></div></div>
     <label>计算方向</label><select id="dir" onchange="calc()"><option value="inclusive" selected>含税价→不含税</option><option value="exclusive">不含税→含税</option></select>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const a=+document.getElementById('amt').value||0,r=+document.getElementById('rate').value||0;
       const dir=document.getElementById('dir').value;
       let ex,in,tax;
       if(dir==='inclusive'){in=a;ex=in/(1+r/100);tax=in-ex;}
       else{ex=a;tax=ex*r/100;in=ex+tax;}
       document.getElementById('res').innerHTML=`<p>不含税价：<strong>${ex.toFixed(2)}</strong> 元</p><p>增值税额：<strong>${tax.toFixed(2)}</strong> 元</p><p style="font-size:18px;color:var(--primary);">含税价：<strong>${in.toFixed(2)}</strong> 元</p>`;
     }calc();'''),

    ('rental-yield-calculator.html', '租金回报率计算器', '🏠', '#fff8e1', 'finance', 'finance',
     '计算房产租金年化回报率',
     '''<div class="input-row"><div><label>房产价值(万元)</label><input type="number" id="value" value="300" step="any" oninput="calc()"></div>
     <div><label>月租金(元)</label><input type="number" id="rent" value="5000" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>年物业费(元)</label><input type="number" id="fee" value="3000" step="any" oninput="calc()"></div>
     <div><label>年维修费(元)</label><input type="number" id="maint" value="1000" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const v=(+document.getElementById('value').value||0)*10000;
       const r=+document.getElementById('rent').value||0;
       const f=+document.getElementById('fee').value||0;
       const m=+document.getElementById('maint').value||0;
       const income=r*12, expenses=f+m, net=income-expenses;
       const yieldGross=v?income/v*100:0, yieldNet=v?net/v*100:0;
       document.getElementById('res').innerHTML=`<p>年租金收入：<strong>${income.toFixed(0)}</strong> 元</p><p>年支出：<strong>${expenses.toFixed(0)}</strong> 元</p><p>年净收入：<strong>${net.toFixed(0)}</strong> 元</p><hr style="border:none;border-top:1px solid var(--border);margin:8px 0;"><p>毛回报率：<strong>${yieldGross.toFixed(2)}%</strong></p><p style="font-size:18px;color:var(--primary);">净回报率：<strong>${yieldNet.toFixed(2)}%</strong></p><p>回本周期：<strong>${yieldNet?(v/net).toFixed(1):'--'}</strong> 年</p>`;
     }calc();'''),

    ('lease-payment-calculator.html', '租赁付款计算器', '🚗', '#fff8e1', 'finance', 'finance',
     '计算等额租金和总利息',
     '''<div class="input-row"><div><label>租赁物价值(元)</label><input type="number" id="pv" value="100000" step="any" oninput="calc()"></div>
     <div><label>年利率(%)</label><input type="number" id="rate" value="6" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>租期(月)</label><input type="number" id="months" value="36" oninput="calc()"></div>
     <div><label>残值(元)</label><input type="number" id="fv" value="0" step="any" oninput="calc()"></div></div>
     <label>还款方式</label><select id="type" onchange="calc()"><option value="equal" selected>等额本息</option><option value="principal">等额本金</option></select>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const P=+document.getElementById('pv').value||0;
       const annual=+document.getElementById('rate').value||0;
       const n=+document.getElementById('months').value||0;
       const fv=+document.getElementById('fv').value||0;
       const r=annual/100/12;
       let pmt,total,interest;
       const type=document.getElementById('type').value;
       if(type==='equal'){
         if(r===0){pmt=P/n;}
         else{pmt=(P-fv*Math.pow(1+r,-n))*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1)+fv*r;}
         total=pmt*n;interest=total-P;
         document.getElementById('res').innerHTML=`<p>月供：<strong style="font-size:20px;color:var(--primary);">${pmt.toFixed(2)}</strong> 元</p><p>总还款：<strong>${total.toFixed(2)}</strong> 元</p><p>总利息：<strong style="color:var(--danger);">${interest.toFixed(2)}</strong> 元</p>`;
       } else {
         const principalPer=P/n;
         let totalInt=0;let scheduleHtml='';
         for(let i=1;i<=Math.min(n,6);i++){
           const remain=P-principalPer*(i-1);
           const intPay=remain*r;
           totalInt+=intPay;
           if(i<=3)scheduleHtml+=`<p>第${i}期：本金${principalPer.toFixed(0)} + 利息${intPay.toFixed(0)} = ${(principalPer+intPay).toFixed(0)}元</p>`;
         }
         const totalPay=P+totalInt;
         document.getElementById('res').innerHTML=`<p>首月还款：<strong style="font-size:18px;color:var(--primary);">${(principalPer+P*r).toFixed(2)}</strong> 元</p><p>总还款：<strong>${totalPay.toFixed(2)}</strong> 元</p><p>总利息：<strong style="color:var(--danger);">${totalInt.toFixed(2)}</strong> 元</p>${scheduleHtml}<p style="font-size:11px;color:var(--text-muted);">...共${n}期</p>`;
       }
     }calc();'''),

    ('invoice-generator.html', '发票金额拆分', '📄', '#fff8e1', 'finance', 'finance',
     '多税率发票金额拆分计算',
     '''<div class="input-row"><div><label>总金额(元)</label><input type="number" id="total" value="10000" step="any" oninput="calc()"></div>
     <div><label>税率(%)</label><select id="rate" onchange="calc()"><option value="13" selected>13%</option><option value="9">9%</option><option value="6">6%</option><option value="3">3%</option><option value="1">1%</option></select></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const t=+document.getElementById('total').value||0;
       const r=+document.getElementById('rate').value||0;
       const ex=t/(1+r/100), tax=t-ex;
       document.getElementById('res').innerHTML=`<p>价税合计：<strong>${t.toFixed(2)}</strong> 元</p><p>不含税金额：<strong>${ex.toFixed(2)}</strong> 元</p><p>税额：<strong>${tax.toFixed(2)}</strong> 元</p><hr style="border:none;border-top:1px solid var(--border);margin:8px 0;"><p style="font-size:12px;color:var(--text-muted);">金额大写：${numToChinese(t)}</p>`;
     }
     function numToChinese(n){
       const digits=['零','壹','贰','叁','肆','伍','陆','柒','捌','玖'];
       const units=['','拾','佰','仟','万','拾','佰','仟','亿'];
       const yuan=Math.floor(n),jiao=Math.floor((n-yuan)*10),fen=Math.round((n-yuan-jiao/10)*100);
       let s=yuan.toString();let r='';
       for(let i=0;i<s.length;i++){const d=+s[s.length-1-i];r=(d?digits[d]+units[i]:'零')+r;}
       r=r.replace(/零+/g,'零').replace(/零$/,'');
       return r+'元'+(jiao?digits[jiao]+'角':'')+(fen?digits[fen]+'分':'整');
     }
     calc();'''),

    ('irr-calculator.html', 'IRR 内部收益率', '📊', '#fff8e1', 'finance', 'finance',
     '计算投资项目的内部收益率',
     '''<label>现金流（逗号分隔，首期为负投入）</label><textarea id="flows" rows="3" oninput="calc()">-10000,3000,3000,3000,3000</textarea>
     <div class="toolbar"><button class="btn primary" onclick="calc()">计算 IRR</button></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const flows=document.getElementById('flows').value.split(/[,\\s]+/).map(s=>parseFloat(s.trim())).filter(v=>!isNaN(v));
       if(flows.length<2){document.getElementById('res').innerHTML='<p>至少需要2个现金流</p>';return;}
       let low=-0.99,high=10;
       for(let i=0;i<100;i++){
         const mid=(low+high)/2;
         let npv=0;for(let t=0;t<flows.length;t++){npv+=flows[t]/Math.pow(1+mid,t);}
         if(npv>0)low=mid;else high=mid;
       }
       const irr=(low+high)/2*100;
       document.getElementById('res').innerHTML=`<p style="font-size:22px;color:var(--primary);">IRR = <strong>${irr.toFixed(2)}%</strong></p><p>期数：${flows.length-1}期</p>${irr>10?'<p style="color:var(--success);">收益率较高</p>':irr>0?'<p>正收益</p>':'<p style="color:var(--danger);">亏损项目</p>'}`;
     }calc();'''),

    ('npv-calculator.html', 'NPV 净现值计算器', '💹', '#fff8e1', 'finance', 'finance',
     '计算投资项目的净现值',
     '''<div class="input-row"><div><label>折现率(%)</label><input type="number" id="rate" value="8" step="any" oninput="calc()"></div>
     <div><label>初始投资(元)</label><input type="number" id="init" value="10000" step="any" oninput="calc()"></div></div>
     <label>各期现金流（逗号分隔）</label><textarea id="flows" rows="2" oninput="calc()">3000,3000,3000,3000</textarea>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const r=(+document.getElementById('rate').value||0)/100;
       const init=+document.getElementById('init').value||0;
       const flows=document.getElementById('flows').value.split(/[,\\s]+/).map(s=>parseFloat(s.trim())).filter(v=>!isNaN(v));
       let npv=-init;
       let detail='';
       flows.forEach((cf,t)=>{const pv=cf/Math.pow(1+r,t+1);npv+=pv;detail+=`<p>第${t+1}期：${cf.toFixed(0)} → 现值 ${pv.toFixed(0)}</p>`;});
       const color=npv>=0?'var(--success)':'var(--danger)';
       document.getElementById('res').innerHTML=`<p>初始投资：<strong>${init.toFixed(2)}</strong></p><p style="font-size:20px;color:${color};">NPV = <strong>${npv.toFixed(2)}</strong> 元</p>${detail}${npv>=0?'<p style="color:var(--success);">✓ 可行</p>':'<p style="color:var(--danger);">✗ 不可行</p>'}`;
     }calc();'''),

    ('bond-yield-calculator.html', '债券收益率计算器', '📜', '#fff8e1', 'finance', 'finance',
     '计算债券到期收益率(YTM)',
     '''<div class="input-row"><div><label>面值(元)</label><input type="number" id="face" value="100" step="any" oninput="calc()"></div>
     <div><label>买入价(元)</label><input type="number" id="price" value="95" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>票面利率(%)</label><input type="number" id="coupon" value="5" step="any" oninput="calc()"></div>
     <div><label>剩余年限</label><input type="number" id="years" value="3" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const F=+document.getElementById('face').value||0;
       const P=+document.getElementById('price').value||0;
       const c=+document.getElementById('coupon').value||0;
       const n=+document.getElementById('years').value||0;
       const C=F*c/100;
       let ytm=(C+(F-P)/n)/((F+P)/2)*100;
       let low=0,high=1;
       for(let i=0;i<200;i++){
         const mid=(low+high)/2;
         let pv=0;for(let t=1;t<=n;t++){pv+=C/Math.pow(1+mid,t);}pv+=F/Math.pow(1+mid,n);
         if(pv>P)low=mid;else high=mid;
       }
       ytm=(low+high)/2*100;
       document.getElementById('res').innerHTML=`<p>年利息：<strong>${C.toFixed(2)}</strong> 元</p><p>总利息收入：<strong>${(C*n).toFixed(2)}</strong> 元</p><p>资本损益：<strong>${(F-P).toFixed(2)}</strong> 元</p><p style="font-size:20px;color:var(--primary);">YTM ≈ <strong>${ytm.toFixed(2)}%</strong></p>`;
     }calc();'''),

    ('option-profit-calculator.html', '期权盈亏计算器', '🎯', '#fff8e1', 'finance', 'finance',
     '计算期权到期盈亏',
     '''<div class="input-row"><div><label>类型</label><select id="type" onchange="calc()"><option value="call" selected>看涨 Call</option><option value="put">看跌 Put</option></select></div>
     <div><label>方向</label><select id="side" onchange="calc()"><option value="buy" selected>买入</option><option value="sell">卖出</option></select></div></div>
     <div class="input-row"><div><label>行权价</label><input type="number" id="strike" value="100" step="any" oninput="calc()"></div>
     <div><label>权利金</label><input type="number" id="premium" value="5" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>到期标的价</label><input type="number" id="s0" value="110" step="any" oninput="calc()"></div>
     <div><label>合约单位</label><input type="number" id="mult" value="100" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const type=document.getElementById('type').value;
       const side=document.getElementById('side').value;
       const K=+document.getElementById('strike').value||0;
       const p=+document.getElementById('premium').value||0;
       const S=+document.getElementById('s0').value||0;
       const m=+document.getElementById('mult').value||1;
       let val;
       if(type==='call'){val=Math.max(S-K,0)-p;}else{val=Math.max(K-S,0)-p;}
       if(side==='sell')val=-val+p*2;
       const total=val*m;
       const bep=type==='call'?K+p:K-p;
       const color=total>=0?'var(--success)':'var(--danger)';
       document.getElementById('res').innerHTML=`<p>单张盈亏：<strong style="color:${color};">${val.toFixed(2)}</strong></p><p style="font-size:18px;color:${color};">总盈亏：<strong>${total.toFixed(2)}</strong> 元</p><p>盈亏平衡点：<strong>${bep.toFixed(2)}</strong></p>`;
     }calc();'''),

    ('mutual-fund-calculator.html', '基金定投计算器', '📊', '#fff8e1', 'finance', 'finance',
     '计算定期定额基金投资收益',
     '''<div class="input-row"><div><label>每月定投(元)</label><input type="number" id="monthly" value="1000" step="any" oninput="calc()"></div>
     <div><label>预期年化(%)</label><input type="number" id="rate" value="8" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>定投年限</label><input type="number" id="years" value="10" step="any" oninput="calc()"></div>
     <div><label>已有本金(元)</label><input type="number" id="initial" value="0" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const m=+document.getElementById('monthly').value||0;
       const ar=+document.getElementById('rate').value||0;
       const y=+document.getElementById('years').value||0;
       const init=+document.getElementById('initial').value||0;
       const mr=ar/100/12;const n=y*12;
       let fv=init*Math.pow(1+mr,n);
       if(mr>0){fv+=m*((Math.pow(1+mr,n)-1)/mr*(1+mr));}else{fv+=m*n;}
       const invested=init+m*n;const profit=fv-invested;
       document.getElementById('res').innerHTML=`<p>累计投入：<strong>${invested.toFixed(0)}</strong> 元</p><p style="font-size:22px;color:var(--primary);">期末总值：<strong>${fv.toFixed(0)}</strong> 元</p><p>总收益：<strong style="color:var(--success);">${profit.toFixed(0)}</strong> 元</p><p>收益率：<strong>${(profit/invested*100).toFixed(2)}%</strong></p>`;
     }calc();'''),

    ('loan-amortization.html', '贷款摊销表', '🏦', '#fff8e1', 'finance', 'finance',
     '生成贷款还款计划明细',
     '''<div class="input-row"><div><label>贷款金额(元)</label><input type="number" id="amt" value="500000" step="any" oninput="calc()"></div>
     <div><label>年利率(%)</label><input type="number" id="rate" value="4.9" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>贷款年限</label><input type="number" id="years" value="30" oninput="calc()"></div></div>
     <label>还款方式</label><select id="type" onchange="calc()"><option value="equal" selected>等额本息</option><option value="principal">等额本金</option></select>
     <div class="toolbar"><button class="btn primary" onclick="calc()">计算</button></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const P=+document.getElementById('amt').value||0,y=+document.getElementById('years').value||0;
       const ar=+document.getElementById('rate').value||0;const n=y*12;const mr=ar/100/12;
       const type=document.getElementById('type').value;
       if(type==='equal'){
         const pmt=P*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1);
         const total=pmt*n;const interest=total-P;
         let html=`<p>月供：<strong style="font-size:18px;color:var(--primary);">${pmt.toFixed(2)}</strong> 元</p><p>总还款：<strong>${total.toFixed(0)}</strong> 元</p><p>总利息：<strong style="color:var(--danger);">${interest.toFixed(0)}</strong> 元</p>`;
         let bal=P;html+='<div style="max-height:200px;overflow-y:auto;margin-top:8px;font-size:11px;"><table style="font-size:11px;"><thead><tr><th>期</th><th>月供</th><th>本金</th><th>利息</th><th>剩余</th></tr></thead><tbody>';
         for(let i=1;i<=Math.min(n,12);i++){const ip=bal*mr,pp=pmt-ip;bal-=pp;html+=`<tr><td>${i}</td><td>${pmt.toFixed(0)}</td><td>${pp.toFixed(0)}</td><td>${ip.toFixed(0)}</td><td>${bal.toFixed(0)}</td></tr>`;}
         html+='</tbody></table></div>';
         document.getElementById('res').innerHTML=html;
       } else {
         const pp=P/n;let totalInt=0,bal=P;let html='';
         for(let i=1;i<=Math.min(n,6);i++){const ip=bal*mr;totalInt+=ip;const pay=pp+ip;bal-=pp;html+=`<tr><td>${i}</td><td>${pay.toFixed(0)}</td><td>${pp.toFixed(0)}</td><td>${ip.toFixed(0)}</td><td>${bal.toFixed(0)}</td></tr>`;}
         let totalIntFull=0;bal=P;for(let i=1;i<=n;i++){const ip=bal*mr;totalIntFull+=ip;bal-=pp;}
         document.getElementById('res').innerHTML=`<p>首月：<strong style="font-size:18px;color:var(--primary);">${(pp+P*mr).toFixed(2)}</strong> 元</p><p>总利息：<strong style="color:var(--danger);">${totalIntFull.toFixed(0)}</strong> 元</p><div style="max-height:200px;overflow-y:auto;margin-top:8px;font-size:11px;"><table style="font-size:11px;"><thead><tr><th>期</th><th>月供</th><th>本金</th><th>利息</th><th>剩余</th></tr></thead><tbody>${html}</tbody></table></div>`;
       }
     }calc();'''),

    ('credit-card-interest.html', '信用卡利息计算器', '💳', '#fff8e1', 'finance', 'finance',
     '计算信用卡最低还款利息',
     '''<div class="input-row"><div><label>账单金额(元)</label><input type="number" id="bill" value="10000" step="any" oninput="calc()"></div>
     <div><label>日利率(%)</label><input type="number" id="rate" value="0.05" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>还款日距记账日(天)</label><input type="number" id="days" value="50" oninput="calc()"></div>
     <div><label>还款金额(元)</label><input type="number" id="paid" value="1000" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const b=+document.getElementById('bill').value||0;
       const r=+document.getElementById('rate').value||0;
       const d=+document.getElementById('days').value||0;
       const p=+document.getElementById('paid').value||0;
       const interest=b*r/100*d;const remain=b-p;const newBal=remain+interest;
       document.getElementById('res').innerHTML=`<p>利息：<strong style="color:var(--danger);">${interest.toFixed(2)}</strong> 元</p><p>未还本金：<strong>${remain.toFixed(2)}</strong> 元</p><p style="font-size:18px;color:var(--primary);">下期账单：<strong>${newBal.toFixed(2)}</strong> 元</p><p style="font-size:11px;color:var(--text-muted);">全额还款可享受免息期</p>`;
     }calc();'''),

    ('inflation-calculator.html', '通货膨胀计算器', '📉', '#fff8e1', 'finance', 'finance',
     '计算通胀对购买力的影响',
     '''<div class="input-row"><div><label>当前金额(元)</label><input type="number" id="amt" value="100000" step="any" oninput="calc()"></div>
     <div><label>年通胀率(%)</label><input type="number" id="rate" value="3" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>年数</label><input type="number" id="years" value="20" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const a=+document.getElementById('amt').value||0,r=+document.getElementById('rate').value||0,y=+document.getElementById('years').value||0;
       const future=a/Math.pow(1+r/100,y);
       const need=a*Math.pow(1+r/100,y);
       document.getElementById('res').innerHTML=`<p>${y}年后 <strong>${a.toFixed(0)}</strong> 元的购买力：</p><p style="font-size:22px;color:var(--primary);">= 现在的 <strong>${future.toFixed(0)}</strong> 元</p><hr style="border:none;border-top:1px solid var(--border);margin:8px 0;"><p>保持购买力需要：<strong>${need.toFixed(0)}</strong> 元</p><p>购买力缩水：<strong style="color:var(--danger);">${((1-future/a)*100).toFixed(1)}%</strong></p>`;
     }calc();'''),

    ('insurance-calculator.html', '保险需求计算器', '🛡️', '#fff8e1', 'finance', 'finance',
     '根据家庭情况估算保险需求',
     '''<div class="input-row"><div><label>年收入(万元)</label><input type="number" id="income" value="20" step="any" oninput="calc()"></div>
     <div><label>年支出(万元)</label><input type="number" id="expense" value="12" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>房贷余额(万元)</label><input type="number" id="debt" value="80" step="any" oninput="calc()"></div>
     <div><label>子女教育(万元)</label><input type="number" id="edu" value="50" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>现有存款/保险(万元)</label><input type="number" id="assets" value="10" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const inc=+document.getElementById('income').value||0;
       const exp=+document.getElementById('expense').value||0;
       const debt=+document.getElementById('debt').value||0;
       const edu=+document.getElementById('edu').value||0;
       const assets=+document.getElementById('assets').value||0;
       const lifeNeed=exp*10+debt+edu-assets;
       const health=50;
       document.getElementById('res').innerHTML=`<p>建议寿险保额：<strong style="font-size:18px;color:var(--primary);">${Math.max(lifeNeed,0).toFixed(0)}</strong> 万元</p><p>建议重疾保额：<strong>${health}</strong> 万元</p><p>意外险保额：<strong>${inc*10}</strong> 万元（年收入10倍）</p><p style="font-size:11px;color:var(--text-muted);">*仅供参考，请咨询专业保险顾问</p>`;
     }calc();'''),

    ('payroll-calculator.html', '工资税后计算器', '💼', '#fff8e1', 'finance', 'finance',
     '计算个人所得税和税后工资',
     '''<div class="input-row"><div><label>税前工资(元/月)</label><input type="number" id="salary" value="15000" step="any" oninput="calc()"></div>
     <div><label>五险一金(元)</label><input type="number" id="insurance" value="2500" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>专项附加扣除(元)</label><input type="number" id="deduction" value="2000" step="any" oninput="calc()"></div>
     <div><label>起征点(元)</label><input type="number" id="threshold" value="5000" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const s=+document.getElementById('salary').value||0;
       const ins=+document.getElementById('insurance').value||0;
       const ded=+document.getElementById('deduction').value||0;
       const th=+document.getElementById('threshold').value||0;
       const taxable=s-ins-ded-th;
       let tax=0;
       if(taxable>0){
         const brackets=[[3000,0.03],[12000,0.1],[25000,0.2],[35000,0.25],[55000,0.3],[80000,0.35],[Infinity,0.45]];
         let prev=0;
         for(const[limit,rate]of brackets){
           if(taxable>prev){const band=Math.min(taxable,limit)-prev;tax+=band*rate;prev=limit;}
           else break;
         }
       }
       const net=s-ins-Math.max(tax,0);
       document.getElementById('res').innerHTML=`<p>税前：<strong>${s.toFixed(2)}</strong> 元</p><p>五险一金：<strong>${ins.toFixed(2)}</strong> 元</p><p>应纳税所得额：<strong>${Math.max(taxable,0).toFixed(2)}</strong> 元</p><p>个人所得税：<strong style="color:var(--danger);">${Math.max(tax,0).toFixed(2)}</strong> 元</p><p style="font-size:20px;color:var(--primary);">税后工资：<strong>${net.toFixed(2)}</strong> 元</p>`;
     }calc();'''),

    ('dca-calculator.html', '定投成本计算器', '📈', '#fff8e1', 'finance', 'finance',
     '定期定额投资成本计算',
     '''<label>投资记录（价格,数量 每行一条）</label><textarea id="trades" rows="5" oninput="calc()">10,100&#10;8,100&#10;12,100</textarea>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const lines=document.getElementById('trades').value.trim().split('\\n');
       let totalCost=0,totalShares=0;
       lines.forEach(line=>{const[price,qty]=line.split(/[,\\s]+/).map(Number);if(price&&qty){totalCost+=price*qty;totalShares+=qty;}});
       const avg=totalShares?totalCost/totalShares:0;
       document.getElementById('res').innerHTML=`<p>总投入：<strong>${totalCost.toFixed(2)}</strong> 元</p><p>总份额：<strong>${totalShares.toFixed(2)}</strong></p><p style="font-size:20px;color:var(--primary);">平均成本：<strong>${avg.toFixed(4)}</strong></p>`;
     }calc();'''),

    ('crypto-converter.html', '加密货币换算', '₿', '#fff8e1', 'finance', 'finance',
     '主流加密货币汇率换算（参考）',
     '''<div class="input-row"><div><label>金额(USD)</label><input type="number" id="usd" value="1000" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''const PRICES={BTC:67000,ETH:3400,BNB:580,SOL:150,XRP:0.52,DOGE:0.12,ADA:0.45,AVAX:35};
     function calc(){
       const usd=+document.getElementById('usd').value||0;
       let html='';
       for(const[sym,price]of Object.entries(PRICES)){
         html+=`<p>${sym}：<strong>${(usd/price).toFixed(6)}</strong> (@ $${price})</p>`;
       }
       document.getElementById('res').innerHTML=html+'<p style="font-size:11px;color:var(--text-muted);">*价格仅供参考</p>';
     }calc();'''),

    ('financial-ratio.html', '财务比率分析', '📊', '#fff8e1', 'finance', 'finance',
     '流动比率、速动比率、资产负债率等',
     '''<div class="input-row"><div><label>流动资产(万)</label><input type="number" id="ca" value="500" step="any" oninput="calc()"></div>
     <div><label>流动负债(万)</label><input type="number" id="cl" value="300" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>存货(万)</label><input type="number" id="inv" value="150" step="any" oninput="calc()"></div>
     <div><label>总资产(万)</label><input type="number" id="ta" value="2000" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>总负债(万)</label><input type="number" id="tl" value="1000" step="any" oninput="calc()"></div>
     <div><label>净利润(万)</label><input type="number" id="ni" value="200" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const ca=+document.getElementById('ca').value||0,cl=+document.getElementById('cl').value||0;
       const inv=+document.getElementById('inv').value||0,ta=+document.getElementById('ta').value||0;
       const tl=+document.getElementById('tl').value||0,ni=+document.getElementById('ni').value||0;
       const cr=cl?ca/cl:0,qr=cl?(ca-inv)/cl:0,dr=ta?tl/ta*100:0,roe=ta?ni/ta*100:0;
       document.getElementById('res').innerHTML=`<div class="stat-grid"><div class="stat-card"><div class="val">${cr.toFixed(2)}</div><div class="lbl">流动比率${cr>=2?'✓':'⚠'}</div></div><div class="stat-card"><div class="val">${qr.toFixed(2)}</div><div class="lbl">速动比率${qr>=1?'✓':'⚠'}</div></div><div class="stat-card"><div class="val">${dr.toFixed(1)}%</div><div class="lbl">资产负债率${dr<60?'✓':'⚠'}</div></div><div class="stat-card"><div class="val">${roe.toFixed(1)}%</div><div class="lbl">ROA</div></div></div>`;
     }calc();'''),

    ('break-even-calculator.html', '盈亏平衡分析', '⚖️', '#fff8e1', 'finance', 'finance',
     '计算盈亏平衡点',
     '''<div class="input-row"><div><label>固定成本(元)</label><input type="number" id="fc" value="10000" step="any" oninput="calc()"></div>
     <div><label>单位售价(元)</label><input type="number" id="price" value="50" step="any" oninput="calc()"></div></div>
     <div class="input-row"><div><label>单位变动成本(元)</label><input type="number" id="vc" value="20" step="any" oninput="calc()"></div>
     <div><label>预计销量</label><input type="number" id="qty" value="500" step="any" oninput="calc()"></div></div>
     <div class="result-box" id="res"></div>''',
     '''function calc(){
       const fc=+document.getElementById('fc').value||0,p=+document.getElementById('price').value||0;
       const vc=+document.getElementById('vc').value||0,q=+document.getElementById('qty').value||0;
       const cm=p-vc;const beq=cm?fc/cm:0;
       const rev=q*p;const tc=fc+vc*q;const profit=rev-tc;
       document.getElementById('res').innerHTML=`<p>单位边际贡献：<strong>${cm.toFixed(2)}</strong> 元</p><p style="font-size:20px;color:var(--primary);">盈亏平衡销量：<strong>${Math.ceil(beq)}</strong> 件</p><p>盈亏平衡收入：<strong>${(beq*p).toFixed(0)}</strong> 元</p><hr style="border:none;border-top:1px solid var(--border);margin:8px 0;"><p>预计收入：${rev.toFixed(0)} 元</p><p>预计利润：<strong style="color:${profit>=0?'var(--success)':'var(--danger)'};">${profit.toFixed(0)}</strong> 元</p><p>安全边际：<strong>${q>beq?((q-beq)/q*100).toFixed(1):'--'}%</strong></p>`;
     }calc();'''),
]

# Generate finance tools
for f in FINANCE_TOOLS:
    make_tool(*f)

print(f'Generated {len(FINANCE_TOOLS)} finance tools')
