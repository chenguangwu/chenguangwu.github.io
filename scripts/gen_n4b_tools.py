#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N4-02 批次 02 生成器：finance/securities/health 5 个计算类 A 级工具。
复用 gen_civil_eng_tools.py 的 inputs+calcTool 模板范式。

用法：python3 scripts/gen_n4b_tools.py
生成：
  tools/finance/installment-real-rate.html     信用卡分期真实利率（IRR）
  tools/securities/bond-duration.html          债券久期计算器（Macaulay/修正）
  tools/health/pregnancy-weight-gain.html      孕期体重增长建议（IOM）
  tools/health/safe-period-calculator.html     安全期计算器（日历法）
  tools/health/milk-tea-calories.html          奶茶热量估算
"""
import os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
BASE = "https://chenguangwu.github.io"
IND_ZH = {"finance": "金融投资", "securities": "证券投资", "health": "健康医疗",
          "decor": "室内装修", "construction": "建筑地产", "electrical": "电气工程",
          "steel": "钢铁冶金", "fun": "娱乐游戏", "ecommerce": "电子商务",
          "sales": "销售管理", "hr": "人力资源", "parenting": "育儿亲子", "home": "家居装修",
          "life": "日常生活", "gardening": "园林园艺", "furniture": "家具家装", "cable": "电缆线缆",
          "it": "IT开发", "design": "平面设计"}

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<!-- toolbox-theme-bootstrap -->
<!-- toolbox-sw-register --><script>if("serviceWorker"in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){});});}</script><script>(function(){try{var t=localStorage.getItem("theme");if(!t&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches){t="dark";}if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");}}catch(e){}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=__CAT__,industry=__INDUSTRY__,icon=__ICON__,bg=__BG__">
<title>__TITLE__ - ToolBox</title>
<link rel="canonical" href="__BASE__/tools/__INDUSTRY__/__SLUG__.html">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__BASE__/tools/__INDUSTRY__/__SLUG__.html">
<meta name="twitter:card" content="summary">
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="../../css/common.css">
<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard','copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool','toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script><!-- TOOLBOX-API-STUB -->
<script src="../../js/common.js" defer></script>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"__BASE__/"},{"@type":"ListItem","position":2,"name":"__CATZH__","item":"__BASE__/tools/__INDUSTRY__/index.html"},{"@type":"ListItem","position":3,"name":"__TITLE__","item":"__BASE__/tools/__INDUSTRY__/__SLUG__.html"}]}
</script>

<meta property="og:image" content="__BASE__/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">
<meta name="twitter:image" content="__BASE__/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">
    <meta property="og:type" content="website">
    <meta name="twitter:title" content="__TITLE__">
    <meta name="twitter:description" content="__DESC__">

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"__TITLE__","url":"__BASE__/tools/__INDUSTRY__/__SLUG__.html","applicationCategory":"FinanceApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","description":"__TITLE__","image":"__BASE__/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}
</script>

<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
<!-- TOOLBOX-SECURITY -->

<script src="/js/privacy.js" defer></script>
<!-- TOOLBOX-PRIVACY-SCRIPT -->

<script src="/js/metrics.js" defer></script>
<!-- TOOLBOX-METRICS-SCRIPT -->
</head>
<body>

<h1 class="sr-only">__H1__</h1>

<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ __TITLE__</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>



<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">__INDICON__ __CATZH__</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">__TITLE__</span>
</nav>
<div class="container">
  <div class="card tool-card-accent" style="--tool-accent:__ACCENT__;">
    <h2>__H2__</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">__INTRO__</p>

__INPUTS__

    <div class="toolbar">
      <button class="btn primary" onclick="calcTool()">计算</button>
      <button class="btn" onclick="resetForm()">重置</button>
    </div>

    <div class="result-box" id="result"></div>
  </div>

<!-- 注意事项区块 -->
<div class="tool-notes" style="--tool-accent:__ACCENT__;">
  <div class="tool-notes-title">⚠️ 使用说明与注意事项</div>
  <ul>
__NOTES__
  </ul>
</div>
<!-- /注意事项区块 -->
</div>

<script>
function num(id){const v=parseFloat(document.getElementById(id).value);return isNaN(v)?0:v;}
function escH(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}
function fmtMoney(n){return n.toLocaleString('zh-CN',{minimumFractionDigits:2,maximumFractionDigits:2});}
function dataGrid(rows){let h='<div class="data-grid">';for(const r of rows){h+='<div class="data-card"><div class="num">'+r[0]+'</div><div class="label">'+r[1]+'</div></div>';}return h+'</div>';}
function calcTool(){__CALC__}
function resetForm(){__RESET__}
calcTool();
</script>
</body>
</html>
"""

TOOLS = [
# ============ 1. 信用卡分期真实利率 ============
{
 "slug":"installment-real-rate","industry":"finance","cat":"finance","icon":"💳","bg":"#fee2e2",
 "accent":"#EF4444","indicon":"💰",
 "title":"信用卡分期真实利率计算器",
 "h1":"信用卡分期真实利率计算器",
 "h2":"💳 信用卡分期真实利率计算器",
 "desc":"信用卡分期真实利率计算器 - 用 IRR 法计算分期手续费背后的实际年化利率，对比名义费率，看清真实资金成本。纯前端本地处理。",
 "intro":"分期手续费率 ≠ 实际利率。输入分期本金、期数与每期手续费率，用 IRR（内部收益率）法还原真实年化利率，并给出对比结论。",
 "inputs":[
   {"id":"P","label":"分期本金（元）","value":"12000","step":"100","min":"0"},
   {"id":"n","label":"分期期数（月）","value":"12","step":"1","min":"1","max":"60"},
   {"id":"r","label":"每期手续费率（%）","value":"0.6","step":"0.05","min":"0"},
 ],
 "calc":r"""
   const P=num('P'), n=Math.floor(num('n')), r=num('r')/100;
   if(P<=0||n<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的本金与期数。</p>');return;}
   const fee=P*r;                 // 每期手续费
   const pmt=P/n+fee;             // 每期还款额
   // IRR 月利率：二分法求解 P = pmt * (1-(1+i)^-n)/i
   let lo=0, hi=1.0;
   for(let it=0;it<80;it++){
     const mid=(lo+hi)/2;
     const pv=pmt*(1-Math.pow(1+mid,-n))/mid;
     if(pv>P) lo=mid; else hi=mid;
   }
   const irrMonthly=(lo+hi)/2;
   const irrAnnual=irrMonthly*12*100;      // 近似年化（单利乘期）
   const ear=Math.pow(1+irrMonthly,12)-1;   // 有效年利率 EAR
   const totalFee=fee*n;
   const nominal=r*12*100;                  // 名义年化 = 每期费率×12
   let html=dataGrid([
     [fmtMoney(totalFee),'总手续费（元）'],
     [fmtMoney(pmt),'每期还款额（元）'],
     [fmtMoney(P+totalFee),'总还款额（元）'],
     [(irrMonthly*100).toFixed(3)+'%','IRR 月利率'],
     [irrAnnual.toFixed(2)+'%','实际年化利率（近似）'],
     [(ear*100).toFixed(2)+'%','有效年利率 EAR']
   ]);
   // 名义 vs 实际对比
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '名义费率年化 '+(nominal).toFixed(2)+'%　→　实际年化 '+(irrAnnual).toFixed(2)+'%　（放大 '+(irrAnnual/Math.max(nominal,0.0001)).toFixed(2)+' 倍）</div>';
   // 前 12 期还款明细表
   const showN=Math.min(n,12);
   html += '<div style="margin-top:12px;font-size:13px;"><b>还款明细（前 '+showN+' 期 / 共 '+n+' 期）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">期数</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">本金部分</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">手续费</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">本期还款</th></tr>';
   for(let t=1;t<=showN;t++){
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+t+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+fmtMoney(P/n)+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+fmtMoney(fee)+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+fmtMoney(pmt)+'</td></tr>';
   }
   html+='</table>';
   let out=html;
   const flag = irrAnnual> nominal*1.8 ? ' <p class="tip-error">⚠️ 实际年化约是名义费率的 '+(irrAnnual/Math.max(nominal,0.0001)).toFixed(1)+' 倍，资金成本显著高于直觉，请谨慎分期。</p>' : ' <p style="color:var(--ok,#16a34a);margin-top:8px;">✅ 实际年化与名义费率相差不大。</p>';
   ToolBox.setResult('result', out + flag);
 """,
 "notes":[
   "每期还款 = 本金÷期数 + 每期手续费（等额本息式）",
   "IRR 为现金流内部收益率：以分期本金为现值、每期还款为年金反推月利率",
   "实际年化 ≈ IRR 月利率 × 12；有效年利率 EAR = (1+i)^12 − 1 更精确",
   "结果仅供参考，不构成财务建议；以银行合同为准",
 ],
},
# ============ 2. 债券久期 ============
{
 "slug":"bond-duration","industry":"securities","cat":"securities","icon":"📈","bg":"#dbeafe",
 "accent":"#3B82F6","indicon":"📊",
 "title":"债券久期计算器",
 "h1":"债券久期计算器",
 "h2":"📈 债券久期计算器",
 "desc":"债券久期计算器 - 计算 Macaulay 久期与修正久期，衡量债券价格对利率变动的敏感度。纯前端本地处理。",
 "intro":"久期是债券价格对利率敏感性的核心指标。输入票面利率、面值、到期收益率与剩余年限，得到 Macaulay 久期与修正久期，并估算利率变动对价格的影响。",
 "inputs":[
   {"id":"C","label":"票面利率（%）","value":"5","step":"0.1","min":"0"},
   {"id":"F","label":"面值（元）","value":"100","step":"10","min":"1"},
   {"id":"y","label":"到期收益率 YTM（%）","value":"5","step":"0.1","min":"0"},
   {"id":"n","label":"剩余年限（年）","value":"10","step":"1","min":"1","max":"50"},
   {"id":"freq","label":"付息频率/年","value":"1","step":"1","min":"1","max":"2"},
 ],
 "calc":r"""
   const C=num('C')/100, F=num('F'), y=num('y')/100, n=Math.floor(num('n')), freq=Math.floor(num('freq'))||1;
   if(F<=0||n<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的面值与年限。</p>');return;}
   const cp=C*F/freq;                 // 每期票息
   const yp=y/freq;                   // 每期收益率
   const N=n*freq;                    // 总期数
   let P=0, dur=0;
   for(let t=1;t<=N;t++){
     const cf=(t===N)?(cp+F):cp;
     const pv=cf/Math.pow(1+yp,t);
     P+=pv;
     dur+=pv*t;
   }
   const macaulay=dur/P;              // 期数
   const macYears=macaulay/freq;      // 年
   const modified=macYears/(1+yp);
   let html=dataGrid([
     [fmtMoney(P),'债券价格（元）'],
     [macaulay.toFixed(2)+' 期',"Macaulay 久期"],
     [macYears.toFixed(2)+' 年','Macaulay 久期（年）'],
     [modified.toFixed(2)+' 年','修正久期'],
     [fmtMoney(cp),'每期票息']
   ]);
   // 各期现金流贴现明细表（前 10 期 + 末期）
   const rows=[]; const showN=Math.min(N,10);
   for(let t=1;t<=N;t++){
     if(t<=showN||t===N){
       const cf=(t===N)?(cp+F):cp;
       const pv=cf/Math.pow(1+yp,t);
       rows.push([t, cf, pv, (pv*t/P)]);
     }
   }
   html += '<div style="margin-top:12px;font-size:13px;"><b>现金流贴现明细（部分期数）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">期数</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">现金流</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">贴现值</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">久期权重</th></tr>';
   rows.forEach(function(r){
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+r[0]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+fmtMoney(r[1])+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+fmtMoney(r[2])+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+(r[3]*100).toFixed(2)+'%</td></tr>';
   });
   html+='</table>';
   const dpdy=modified;               // 每 1% 利率变动价格变化百分比 ≈ 修正久期 × 1%
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">利率每上升 1%，价格约下降 '+dpdy.toFixed(2)+'%；反之上升。久期越长，利率风险越大。</p>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "Macaulay 久期 = Σ(PV(Ct)×t) / P，为现金流加权平均回笼时间",
   "修正久期 = Macaulay 久期(年) / (1 + 每期收益率)",
   "ΔP/P ≈ −修正久期 × Δy：久期用于衡量利率敏感度",
   "本工具为简化模型，未计入凸性；结果仅供参考，不构成投资建议",
 ],
},
# ============ 3. 孕期体重增长建议 ============
{
 "slug":"pregnancy-weight-gain","industry":"health","cat":"health","icon":"🤰","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"🏥",
 "title":"孕期体重增长建议计算器",
 "h1":"孕期体重增长建议计算器",
 "h2":"🤰 孕期体重增长建议计算器",
 "desc":"孕期体重增长建议计算器 - 依据 IOM 2009 指南，按孕前 BMI 给出孕期总增重与孕中晚期每周增重建议区间。纯前端本地处理。",
 "intro":"孕前 BMI 决定孕期合理增重范围。输入身高与孕前体重，按美国医学研究院（IOM 2009）指南给出总增重与孕中晚期周增重建议区间，帮助科学管理孕期体重。",
 "inputs":[
   {"id":"h","label":"身高（cm）","value":"165","step":"0.5","min":"100","max":"220"},
   {"id":"w","label":"孕前体重（kg）","value":"55","step":"0.5","min":"30","max":"150"},
   {"id":"week","label":"当前孕周（可选）","value":"20","step":"1","min":"1","max":"42"},
 ],
 "calc":r"""
   const h=num('h')/100, w=num('w');
   if(h<=0||w<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的身高与体重。</p>');return;}
   const bmi=w/(h*h);
   let totalMin,totalMax,weekMin,weekMax,label;
   if(bmi<18.5){totalMin=12.5;totalMax=18;weekMin=0.44;weekMax=0.58;label='偏瘦（BMI<18.5）';}
   else if(bmi<25){totalMin=11.5;totalMax=16;weekMin=0.35;weekMax=0.50;label='正常（18.5≤BMI<25）';}
   else if(bmi<30){totalMin=7;totalMax=11.5;weekMin=0.23;weekMax=0.33;label='超重（25≤BMI<30）';}
   else{totalMin=5;totalMax=9;weekMin=0.17;weekMax=0.27;label='肥胖（BMI≥30）';}
   let html=dataGrid([
     [bmi.toFixed(1),'孕前 BMI'],
     [label,'BMI 分类'],
     [totalMin+' ~ '+totalMax+' kg','孕期总增重建议'],
     [weekMin+' ~ '+weekMax+' kg/周','孕中晚期周增重']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">孕早期（前 3 个月）总增重约 0.5–2 kg，以上周增重适用于孕中期以后。个体差异大，请遵医嘱。</p>';
   // 当前孕周进度参考（若填写）
   const week=Math.floor(num('week'));
   if(week>=1&&week<=42){
     const early=2;  // 孕早期约增 0.5–2kg（取 1 为基准示意）
     const midWeeks=Math.max(0,week-13);
     const estMin=early+weekMin*midWeeks;
     const estMax=early+weekMax*midWeeks;
     html += '<div class="tip-mini" style="margin-top:8px;font-size:13px;color:var(--text-muted);">'+
       '按当前孕周 '+week+' 周估算：此时累计增重约 '+estMin.toFixed(1)+' ~ '+estMax.toFixed(1)+' kg（孕早期按 1–2 kg 计，此后按周增重线性推算）。</div>';
   }
   // IOM 分级参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>IOM 2009 孕期增重参考表</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">孕前 BMI</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">分类</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">总增重(kg)</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">中晚期周增重(kg)</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">&lt;18.5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">偏瘦</td><td style="border:1px solid #d1d5db;padding:5px 8px;">12.5–18</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0.44–0.58</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">18.5–24.9</td><td style="border:1px solid #d1d5db;padding:5px 8px;">正常</td><td style="border:1px solid #d1d5db;padding:5px 8px;">11.5–16</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0.35–0.50</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">25–29.9</td><td style="border:1px solid #d1d5db;padding:5px 8px;">超重</td><td style="border:1px solid #d1d5db;padding:5px 8px;">7–11.5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0.23–0.33</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">≥30</td><td style="border:1px solid #d1d5db;padding:5px 8px;">肥胖</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5–9</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0.17–0.27</td></tr>'+
     '</table>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "BMI = 孕前体重(kg) ÷ 身高²(m²)",
   "依据 IOM 2009《孕期体重增加指南》：偏瘦 12.5–18kg、正常 11.5–16kg、超重 7–11.5kg、肥胖 5–9kg",
   "本工具为通用参考，双胎、高龄、合并疾病者需个体化评估",
   "结果不构成医疗建议，请以产检医生指导为准",
 ],
},
# ============ 4. 安全期计算器 ============
{
 "slug":"safe-period-calculator","industry":"health","cat":"health","icon":"📅","bg":"#dcfce7",
 "accent":"#10B981","indicon":"🏥",
 "title":"安全期计算器",
 "h1":"安全期计算器",
 "h2":"📅 安全期计算器",
 "desc":"安全期计算器 - 按日历法（Ogino-Knaus）估算排卵期、易孕期与安全期区间，含明确的风险提示。纯前端本地处理。",
 "intro":"按日历法估算：排卵日约在下一次月经前 14 天，其前后各加 5 天为易孕期，其余为相对安全期。适用于周期规律的成年女性，仅供健康管理参考。",
 "inputs":[
   {"id":"lmp","label":"末次月经日期","value":"2026-08-01","step":"1","type":"date"},
   {"id":"cycle","label":"周期天数（天）","value":"28","step":"1","min":"21","max":"40"},
   {"id":"period","label":"经期天数（天）","value":"5","step":"1","min":"1","max":"10"},
 ],
 "calc":r"""
   const lmpRaw=document.getElementById('lmp').value;
   const cycle=Math.floor(num('cycle')), period=Math.floor(num('period'));
   if(!lmpRaw){ToolBox.setResult('result','<p class="tip-error">请选择末次月经日期。</p>');return;}
   if(cycle<21||cycle>40||period<1||period>10){ToolBox.setResult('result','<p class="tip-error">周期 21–40 天、经期 1–10 天为常见范围，请核对输入。</p>');return;}
   const lmp=new Date(lmpRaw);
   if(isNaN(lmp.getTime())){ToolBox.setResult('result','<p class="tip-error">日期格式无效。</p>');return;}
   const ovu=new Date(lmp.getTime());
   ovu.setDate(lmp.getDate()+cycle-14);          // 预计排卵日
   const fertileStart=new Date(ovu.getTime()); fertileStart.setDate(ovu.getDate()-5);
   const fertileEnd=new Date(ovu.getTime()); fertileEnd.setDate(ovu.getDate()+4);
   const nextP=new Date(lmp.getTime()); nextP.setDate(lmp.getDate()+cycle);
   const fmt=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
   // 月经期（次月经期）
   const mStart=new Date(nextP.getTime()); mStart.setDate(nextP.getDate()-period+1);
   const mEnd=new Date(nextP.getTime());
   let html=dataGrid([
     [fmt(ovu),'预计排卵日'],
     [fmt(fertileStart)+' ~ '+fmt(fertileEnd),'易孕期（排卵日±5天）'],
     [fmt(mStart)+' ~ '+fmt(mEnd),'下次月经期'],
     [fmt(nextP),'预计下次月经']
   ]);
   html += '<p class="tip-error" style="margin-top:8px;">⚠️ 安全期避孕失败率高（年失败率约 24%），日历法仅适合健康管理参考，不推荐作为避孕依据！</p>';
   // 周期日历可视化：从 LMP 到下次月经前一天的逐日标记
   const dayMs=86400000;
   const span=cycle;
   html += '<div style="margin-top:12px;font-size:13px;"><b>周期日历（末次月经起 '+span+' 天）</b></div>'+
     '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:6px;">'+
     ['一','二','三','四','五','六','日'].map(function(d){return '<div style="text-align:center;font-size:11px;color:var(--text-muted);">'+d+'</div>';}).join('');
   const startDow=(lmp.getDay()+6)%7;  // 周一=0
   for(let i=0;i<startDow;i++){html+='<div></div>';}
   for(let i=0;i<span;i++){
     const d=new Date(lmp.getTime()+i*dayMs);
     const label=(d.getMonth()+1)+'/'+d.getDate();
     let cls='background:var(--result-bg);border:1px solid var(--border);';
     const isFertile=d>=fertileStart&&d<=fertileEnd;
     const isPeriod=d<=new Date(lmp.getTime()+ (period-1)*dayMs);
     if(isFertile)cls='background:#fde68a;border:1px solid #f59e0b;';
     if(isPeriod)cls='background:#fecaca;border:1px solid #ef4444;';
     html+='<div title="'+label+'" style="'+cls+'border-radius:8px;text-align:center;font-size:11px;padding:6px 2px;">'+label+'</div>';
   }
   html+='</div><div style="display:flex;gap:12px;font-size:11px;color:var(--text-muted);margin-top:6px;">'+
     '<span><span style="display:inline-block;width:10px;height:10px;background:#fecaca;border-radius:2px;margin-right:4px;"></span>经期</span>'+
     '<span><span style="display:inline-block;width:10px;height:10px;background:#fde68a;border-radius:2px;margin-right:4px;"></span>易孕期</span>'+
     '<span><span style="display:inline-block;width:10px;height:10px;background:var(--result-bg);border:1px solid var(--border);border-radius:2px;margin-right:4px;"></span>安全期</span></div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "日历法假设排卵日 = 下次月经前 14 天，精子存活约 3–5 天、卵子 1 天",
   "易孕期 = 排卵日前 5 天至后 4 天；其余为相对安全期",
   "周期不规律、压力/疾病/旅行会影响排卵，日历法误差较大",
   "结果不构成医疗或避孕建议，重要决策请咨询专业医生",
 ],
},
# ============ 5. 奶茶热量估算 ============
{
 "slug":"milk-tea-calories","industry":"health","cat":"health","icon":"🧋","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"🏥",
 "title":"奶茶热量估算器",
 "h1":"奶茶热量估算器",
 "h2":"🧋 奶茶热量估算器",
 "desc":"奶茶热量估算器 - 按杯型、茶底、奶类、糖度与加料组合估算一杯奶茶的热量，帮助控制日常摄入。纯前端本地处理。",
 "intro":"一杯奶茶热量从几十到六百千卡不等。按杯型、茶底、奶类、糖度与常见加料组合，快速估算总热量，看清「快乐水」的真实成本。",
 "inputs":[
   {"id":"cup","label":"杯型","value":"500","step":"0","type":"select","opts":[["350","小杯 350ml"],["500","中杯 500ml"],["650","大杯 650ml"]]},
   {"id":"tea","label":"茶底","value":"0","step":"0","type":"select","opts":[["0","原味茶（0 kcal）"],["30","奶茶基底（30 kcal）"],["60","芝士奶盖（60 kcal）"]]},
   {"id":"milk","label":"奶类","value":"80","step":"0","type":"select","opts":[["0","无奶（纯茶）"],["80","全脂牛奶"],["60","脱脂牛奶"],["120","奶精/植脂末"]]},
   {"id":"sugar","label":"糖度","value":"100","step":"0","type":"select","opts":[["0","无糖"],["50","三分糖"],["80","五分糖"],["100","全糖"]]},
   {"id":"top","label":"加料（多选，可叠加）","value":"boba","step":"0","type":"checkbox","opts":[["boba","珍珠 +80"],["coconut","椰果 +40"],["pudding","布丁 +60"],["cheese","奶盖 +70"],["redbean","红豆 +50"]]},
 ],
 "calc":r"""
   const cup=parseInt(document.getElementById('cup').value)||500;
   const tea=num('tea'), milk=num('milk'), sugarPct=parseFloat(document.getElementById('sugar').value)||0;
   const base=tea+milk;
   const sugarKcal=Math.round(cup/100* (sugarPct/100) * 10); // 近似：每100ml全糖≈10kcal，按糖度比例
   let topKcal=0, topNames=[];
   ['boba','coconut','pudding','cheese','redbean'].forEach(function(id){
     const el=document.getElementById('top_'+id);
     if(el&&el.checked){
       const v=parseInt(el.value)||0;
       topKcal+=v;
       topNames.push(el.dataset.name||id);
     }
   });
   const total=base+sugarKcal+topKcal;
   let html=dataGrid([
     [total+' kcal','一杯总热量'],
     [base+' kcal','茶底 + 奶类'],
     [sugarKcal+' kcal','糖（'+((sugarPct/100)*100)+'% 糖度）'],
     [topKcal+' kcal','加料'+(topNames.length?'（'+topNames.join('、')+'）':'（无）')]
   ]);
   const note = total>=400 ? ' <p class="tip-error" style="margin-top:8px;">⚠️ 本杯热量相当于 '+(total/150).toFixed(1)+' 碗米饭（按每碗 150 kcal 计），减脂期建议选无糖、去加料。</p>' : ' <p style="color:var(--ok,#16a34a);margin-top:8px;">✅ 热量适中，但加料与糖度是主要变量，注意控制频次。</p>';
   // 常见奶茶热量参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见奶茶热量参考（中杯 500ml 估算）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">款式</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">全糖</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">三分糖</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">无糖</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">珍珠奶茶</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈400</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈350</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈290</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">奶盖绿茶</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈330</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈290</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈230</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">纯奶茶（无加料）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈250</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈210</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈150</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">纯茶（无奶无糖）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈120</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈60</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈0</td></tr>'+
     '</table>';
   ToolBox.setResult('result', html + note);
 """,
   "notes":[
   "热量为常见配料的近似估算值，实际因配方与品牌而异",
   "全糖每 100ml 约 10–12 kcal，按所选糖度比例折算",
   "加料热量：珍珠 80、椰果 40、布丁 60、奶盖 70、红豆 50 kcal",
   "结果仅供饮食管理参考，不构成营养或医疗建议",
 ],
},
# ============ 11. 债券凸性 ============
{
 "slug":"bond-convexity","industry":"securities","cat":"calculator","icon":"📐","bg":"#dbeafe",
 "accent":"#3B82F6","indicon":"📊",
 "title":"债券凸性计算器",
 "h1":"债券凸性计算器",
 "h2":"📐 债券凸性计算器",
 "desc":"债券凸性计算器 - 计算债券凸性（Convexity），衡量久期对利率变动的二阶敏感度，配合久期更精确估算价格变动。纯前端本地处理。",
 "intro":"凸性是久期的补充指标：久期衡量价格—利率关系的一阶斜率，凸性捕捉曲率。输入票面利率、面值、YTM 与剩余年限，得到凸性值并对比久期估算误差。",
 "inputs":[
   {"id":"C","label":"票面利率（%）","value":"5","step":"0.1","min":"0"},
   {"id":"F","label":"面值（元）","value":"100","step":"10","min":"1"},
   {"id":"y","label":"到期收益率 YTM（%）","value":"5","step":"0.1","min":"0"},
   {"id":"n","label":"剩余年限（年）","value":"10","step":"1","min":"1","max":"50"},
   {"id":"freq","label":"付息频率/年","value":"1","step":"1","min":"1","max":"2"},
 ],
 "calc":r"""
   const C=num('C')/100, F=num('F'), y=num('y')/100, n=Math.floor(num('n')), freq=Math.floor(num('freq'))||1;
   if(F<=0||n<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的面值与年限。</p>');return;}
   const cp=C*F/freq, yp=y/freq, N=n*freq;
   let P=0, dur=0, conv=0;
   for(let t=1;t<=N;t++){
     const cf=(t===N)?(cp+F):cp;
     const pv=cf/Math.pow(1+yp,t);
     P+=pv; dur+=pv*t; conv+=pv*t*(t+1);
   }
   const macaulay=dur/P/freq;
   const modified=macaulay/(1+yp);
   const convexity=conv/P/Math.pow(1+yp,2)/Math.pow(freq,2);
   let html=dataGrid([
     [fmtMoney(P),'债券价格（元）'],
     [macaulay.toFixed(2)+' 年','Macaulay 久期'],
     [modified.toFixed(2)+' 年','修正久期'],
     [convexity.toFixed(3),'凸性（年²）']
   ]);
   // 对比：利率 +1% 时 久期估算 vs 久期+凸性
   const dy=0.01;
   const dOnly=-modified*dy*100;
   const dPlus=(-modified*dy+0.5*convexity*dy*dy)*100;
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '利率上升 1%：久期估算 -'+Math.abs(dOnly).toFixed(2)+'%，久期+凸性 -'+Math.abs(dPlus).toFixed(2)+'%（凸性修正使估算更接近实际）。</div>';
   // 利率敏感度对比表（±1%/±2%）
   html += '<div style="margin-top:12px;font-size:13px;"><b>利率敏感度对比（价格变化 %）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">Δy</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">久期近似</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">久期+凸性</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">差异</th></tr>';
   [-0.02,-0.01,0.01,0.02].forEach(function(dy){
     const a=-modified*dy*100;
     const b=(-modified*dy+0.5*convexity*dy*dy)*100;
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+(dy>0?'+':'')+(dy*100).toFixed(0)+'%</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+(a>0?'+':'')+a.toFixed(2)+'%</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+(b>0?'+':'')+b.toFixed(2)+'%</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+(b-a).toFixed(2)+'%</td></tr>';
   });
   html+='</table>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "凸性 = Σ(PV(Ct)·t·(t+1)) / (P·(1+y)²)，为价格—利率关系的二阶项",
   "ΔP/P ≈ −修正久期·Δy + ½·凸性·Δy²，凸性项修正久期的线性近似误差",
   "利率上升时凸性为正的债券价格跌幅小于久期线性估算，利率下降时涨幅大于估算",
   "本工具为简化模型，结果仅供参考，不构成投资建议",
 ],
},
# ============ 12. 吊顶板材用量 ============
{
 "slug":"ceiling-panel-quantity","industry":"decor","cat":"calculator","icon":"🧱","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"🔧",
 "title":"吊顶板材用量计算器",
 "h1":"吊顶板材用量计算器",
 "h2":"🧱 吊顶板材用量计算器",
 "desc":"吊顶板材用量计算器 - 按房间尺寸与板材规格计算铝扣板/石膏板用量，含损耗率与余量建议。纯前端本地处理。",
 "intro":"装修吊顶前先算量：输入房间长宽、板材规格与损耗率，得到所需板材块数、主/副龙骨用量与购买建议，避免多买浪费或少买补货。",
 "inputs":[
   {"id":"L","label":"房间长（m）","value":"4.2","step":"0.1","min":"0.5"},
   {"id":"W","label":"房间宽（m）","value":"3.6","step":"0.1","min":"0.5"},
   {"id":"pl","label":"板长（mm）","value":"600","step":"50","min":"200","max":"3000"},
   {"id":"pw","label":"板宽（mm）","value":"600","step":"50","min":"200","max":"3000"},
   {"id":"loss","label":"损耗率（%）","value":"5","step":"1","min":"0","max":"30"},
 ],
 "calc":r"""
   const L=num('L'), W=num('W'), pl=num('pl')/1000, pw=num('pw')/1000, loss=num('loss')/100;
   if(L<=0||W<=0||pl<=0||pw<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的尺寸。</p>');return;}
   const area=L*W;
   const one=pl*pw;
   const base=Math.ceil(area/one);
   const total=Math.ceil(base*(1+loss));
   const extra=total-base;
   const perim=2*(L+W);
   const mainBeam=Math.ceil(perim/1.2)+Math.ceil(L/1.2)*Math.ceil(W/1.2);  // 主龙骨约 1.2m 间距
   let html=dataGrid([
     [area.toFixed(2)+' m²','吊顶面积'],
     [one.toFixed(4)+' m²','单板面积'],
     [base+' 块','净用量（无损耗）'],
     [total+' 块','含损耗购买量'],
     [extra+' 块','损耗余量'],
     [mainBeam+' 根','主龙骨约需']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按 '+pl*1000+'×'+pw*1000+'mm 板材、损耗率 '+Math.round(loss*100)+'% 估算。实际请以现场排板与商家计算为准，边角裁切较多时损耗率应上调。</p>';

   // 常用板材规格参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>常用吊顶板材规格参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">类型</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">规格</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适用场景</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">铝扣板</td><td style="border:1px solid #d1d5db;padding:5px 8px;">300×300 / 600×600</td><td style="border:1px solid #d1d5db;padding:5px 8px;">厨卫防潮</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">石膏板</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1200×2400</td><td style="border:1px solid #d1d5db;padding:5px 8px;">客厅卧室造型</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">PVC 扣板</td><td style="border:1px solid #d1d5db;padding:5px 8px;">200 / 300 宽条</td><td style="border:1px solid #d1d5db;padding:5px 8px;">经济型厨卫</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "净用量 = 吊顶面积 ÷ 单板面积，向上取整",
   "购买量 = 净用量 × (1 + 损耗率)，裁切与边角损耗",
   "主龙骨按 1.2m 间距估算，异形吊顶用量差异大",
   "本工具为估算参考，精确算量请结合图纸与现场",
 ],
},
# ============ 13. 装修人工费估算 ============
{
 "slug":"renovation-labor-cost","industry":"construction","cat":"calculator","icon":"🛠️","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"🏗️",
 "title":"装修人工费估算器",
 "h1":"装修人工费估算器",
 "h2":"🛠️ 装修人工费估算器",
 "desc":"装修人工费估算器 - 按面积与工种单价估算拆改、水电、瓦工、木工、油工等人工费用，装修预算必用。纯前端本地处理。",
 "intro":"人工费是装修预算的大头。输入套内面积并勾选施工项目，按常见工种单价（元/m²）估算总人工费，帮助预算规划与报价对比。",
 "inputs":[
   {"id":"area","label":"套内面积（m²）","value":"90","step":"1","min":"10"},
   {"id":"items","label":"施工项目（多选）","value":"d","step":"0","type":"checkbox","opts":[
     ["d","拆改 25元/m²"],["s","水电 45元/m²"],["w","瓦工 55元/m²"],
     ["m","木工 35元/m²"],["p","油漆 30元/m²"],["t","厨卫防水 60元/m²"]]},
 ],
 "calc":r"""
   const area=num('area');
   if(area<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的套内面积。</p>');return;}
   const rates={d:25,s:45,w:55,m:35,p:30,t:60};
   const names={d:'拆改',s:'水电',w:'瓦工',m:'木工',p:'油漆',t:'厨卫防水'};
   let total=0, rows=[];
   ['d','s','w','m','p','t'].forEach(function(id){
     const el=document.getElementById('top_'+id);
     if(el&&el.checked){
       const cost=area*rates[id];
       total+=cost;
       rows.push([names[id], area+' m² × '+rates[id]+'元', fmtMoney(cost)+' 元']);
     }
   });
   if(!rows.length){ToolBox.setResult('result','<p class="tip-error">请至少勾选一个施工项目。</p>');return;}
   let html='<div class="data-grid" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr));">'+
     '<div class="data-card"><div class="num">'+fmtMoney(total)+'</div><div class="label">人工费合计（元）</div></div>'+
     '<div class="data-card"><div class="num">'+fmtMoney(total/area)+' 元/m²</div><div class="label">综合单价</div></div></div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>分项明细</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">项目</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">计算式</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">费用</th></tr>';
   rows.forEach(function(r){
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+r[0]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+r[1]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+r[2]+'</td></tr>';
   });
   html+='</table><p style="font-size:12px;color:var(--text-muted);margin-top:8px;">单价为常见行情区间中值，地域与工艺差异大，请以本地报价为准。以上不含材料费。</p>';

   // 常见面积人工费参考
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见面积人工费参考（勾选全项）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">套内面积</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">约人工费</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">工期参考</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">70 m²</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈1.4–1.8 万</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40–55 天</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">90 m²</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈1.8–2.4 万</td><td style="border:1px solid #d1d5db;padding:5px 8px;">50–65 天</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">120 m²</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈2.4–3.2 万</td><td style="border:1px solid #d1d5db;padding:5px 8px;">65–85 天</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "各工种单价为常见市场行情中值：拆改 25、水电 45、瓦工 55、木工 35、油漆 30 元/m²",
   "厨卫防水按套内面积估算，实际按展开面积计费",
   "人工费不含主材与辅材费用，半包/清包模式差异较大",
   "结果仅供参考，请以本地装修公司报价为准",
 ],
},
# ============ 14. 水泥砂浆配比 ============
{
 "slug":"cement-mortar-ratio","industry":"construction","cat":"calculator","icon":"🏗️","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"🏗️",
 "title":"水泥砂浆配比计算器",
 "h1":"水泥砂浆配比计算器",
 "h2":"🏗️ 水泥砂浆配比计算器",
 "desc":"水泥砂浆配比计算器 - 按砂浆标号计算水泥、砂、水用量，支持 M5/M7.5/M10/M15 常用配比换算。纯前端本地处理。",
 "intro":"砌筑/抹灰常用水泥砂浆有固定配合比。选择标号与总方量，自动换算水泥、砂、水的用量（重量与袋数），方便材料采购。",
 "inputs":[
   {"id":"grade","label":"砂浆标号","value":"m7.5","step":"0","type":"select","opts":[
     ["m5","M5（水泥:砂 = 1:5.0）"],["m7.5","M7.5（1:4.8）"],
     ["m10","M10（1:4.5）"],["m15","M15（1:4.0）"]]},
   {"id":"vol","label":"砂浆方量（m³）","value":"1","step":"0.1","min":"0.1"},
   {"id":"bag","label":"水泥袋装（kg/袋）","value":"50","step":"5","min":"25","max":"50"},
 ],
 "calc":r"""
   const vol=num('vol'), bag=num('bag')||50;
   if(vol<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的方量。</p>');return;}
   const grade=document.getElementById('grade').value;
   const ratio={'m5':[1,5.0],'m7.5':[1,4.8],'m10':[1,4.5],'m15':[1,4.0]}[grade]||[1,4.8];
   // 每 m³ 砂浆约需水泥 300kg 基准（M7.5），按比例微调
   const cementBase=340;
   const cement=cementBase*(ratio[1]>=4.8?1:ratio[1]>=4.5?0.95:1.1);
   const cementKg=Math.round(cement*vol);
   const sandKg=Math.round(cementKg*ratio[1]);
   const waterKg=Math.round(cementKg*0.45);
   const bags=Math.ceil(cementKg/bag);
   let html=dataGrid([
     [cementKg+' kg','水泥（'+bags+' 袋）'],
     [sandKg+' kg','砂'],
     [waterKg+' kg','水'],
     [(cementKg/1000).toFixed(2)+' t','水泥吨位']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按 '+grade.toUpperCase()+' 砂浆（水泥:砂 = 1:'+ratio[1]+'）估算，水灰比约 0.45。实际用量因砂含水率与现场工艺而异。</p>';

   // 砂浆标号用途参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>水泥砂浆标号用途参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">标号</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">配比(水泥:砂)</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">典型用途</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">M5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1:5.0</td><td style="border:1px solid #d1d5db;padding:5px 8px;">一般砌筑</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">M7.5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1:4.8</td><td style="border:1px solid #d1d5db;padding:5px 8px;">多层砌筑/抹灰</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">M10</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1:4.5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">承重部位</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">M15</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1:4.0</td><td style="border:1px solid #d1d5db;padding:5px 8px;">高强砌筑/基础</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "常用配合比：M5 水泥:砂=1:5.0、M7.5=1:4.8、M10=1:4.5、M15=1:4.0",
   "水泥用量为估算基准，实际按《砌筑砂浆配合比设计规程》试配",
   "砂的含水率会显著影响实际加水量",
   "结果仅供参考，工程用量请以设计图纸与试验配合比为准",
 ],
},
# ============ 15. 电线线径选择 ============
{
 "slug":"wire-gauge-selector","industry":"electrical","cat":"calculator","icon":"🔌","bg":"#fef9c3",
 "accent":"#EAB308","indicon":"🔧",
 "title":"电线线径选择器",
 "h1":"电线线径选择器",
 "h2":"🔌 电线线径选择器",
 "desc":"电线线径选择器 - 按负载电流与敷设方式推荐铜/铝芯导线截面（平方毫米），对照常见载流量表。纯前端本地处理。",
 "intro":"选线径别凭感觉：输入负载电流、导线材质与敷设方式，推荐最小安全截面（BV 铜线系列），并对照载流量表给出余量提示。",
 "inputs":[
   {"id":"I","label":"负载电流（A）","value":"20","step":"1","min":"1"},
   {"id":"mat","label":"导线材质","value":"cu","step":"0","type":"select","opts":[
     ["cu","铜芯"],["al","铝芯"]]},
   {"id":"inst","label":"敷设方式","value":"conduit","step":"0","type":"select","opts":[
     ["conduit","穿管敷设"],["open","明敷"]]},
   {"id":"len","label":"线路长度（m，可选）","value":"30","step":"5","min":"0"},
 ],
 "calc":r"""
   const I=num('I'), L=num('len');
   if(I<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的负载电流。</p>');return;}
   const mat=document.getElementById('mat').value;
   const inst=document.getElementById('inst').value;
   // 常见载流量（A）：铜/铝，穿管/明敷
   const sizes=['1.5','2.5','4','6','10','16','25','35'];
   const cap={cu:{conduit:[12,18,25,34,45,61,84,102],open:[17,23,31,40,54,70,95,117]},
              al:{conduit:[9,14,19,26,35,47,65,80],open:[13,17,24,31,42,55,76,92]}};
   const row=(cap[mat]&&cap[mat][inst])||cap.cu.conduit;
   let idx=0;
   while(idx<row.length-1 && row[idx]<I*1.25) idx++;  // 留 25% 余量
   const rec=sizes[idx];
   const safe=row[idx];
   let html=dataGrid([
     [rec+' mm²','推荐截面'],
     [safe+' A','载流量（≥1.25×I）'],
     [I.toFixed(1)+' A','负载电流'],
     [(mat==='cu'?'铜芯':'铝芯') + ' / ' + (inst==='conduit'?'穿管':'明敷'),'材质 / 敷设']
   ]);
   if(L>0){
     const rho=mat==='cu'?0.0175:0.0283;
     const R=rho*L*2/(parseFloat(rec));   // 双线
     const drop=I*R;
     const pct=drop/220*100;
     html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">线路压降约 '+drop.toFixed(2)+' V（'+pct.toFixed(2)+'%），'+(pct>5?'⚠️ 超过 5%，建议升一档线径':'✅ 在 5% 允许范围内')+'。</p>';
   }

   // 常见家用电器电流参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见家用电器电流参考（220V）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">电器</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">功率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">电流约</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">推荐线径</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">照明回路</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≤1000W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≤4.5A</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1.5–2.5 mm²</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">普通插座</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≤2200W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≤10A</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2.5 mm²</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">空调(1.5P)</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈1200W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈5.5A</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2.5–4 mm²</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">电热水器</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈2000W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≈9A</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2.5–4 mm²</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">即热式热水器</td><td style="border:1px solid #d1d5db;padding:5px 8px;">6000–8000W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">27–36A</td><td style="border:1px solid #d1d5db;padding:5px 8px;">6–10 mm²</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "载流量参照常见 BV/BVR 导线数据，已按 1.25 倍电流留余量",
   "同一截面铝芯载流量约为铜芯的 75–80%",
   "穿管敷设散热差，载流量低于明敷",
   "长距离线路需校验压降（建议 ≤5%）；结果仅供参考，正式设计按 GB 50303 执行",
 ],
},
# ============ 16. 断路器选型 ============
{
 "slug":"breaker-sizing","industry":"electrical","cat":"calculator","icon":"⚡","bg":"#fef9c3",
 "accent":"#EAB308","indicon":"🔧",
 "title":"断路器选型计算器",
 "h1":"断路器选型计算器",
 "h2":"⚡ 断路器选型计算器",
 "desc":"断路器选型计算器 - 按负载电流推荐断路器额定电流与极数，区分照明/插座/空调回路并给出跳闸说明。纯前端本地处理。",
 "intro":"断路器额定值选大了不保护、选小了常跳闸。输入回路负载电流与用途，按 1.25 倍原则推荐额定电流（常见规格序列），并给出极数建议。",
 "inputs":[
   {"id":"I","label":"回路负载电流（A）","value":"10","step":"0.5","min":"1"},
   {"id":"use","label":"回路用途","value":"light","step":"0","type":"select","opts":[
     ["light","照明"],["socket","插座"],["ac","空调"],["water","厨卫电器"]]},
   {"id":"pole","label":"极数","value":"1","step":"0","type":"select","opts":[
     ["1","1P（单相照明）"],["2","2P（单相大功率）"],["3","3P（三相）"]]},
 ],
 "calc":r"""
   const I=num('I');
   if(I<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的负载电流。</p>');return;}
   const use=document.getElementById('use').value;
   const pole=document.getElementById('pole').value;
   const target=I*1.25;
   const series=[6,10,16,20,25,32,40,50,63,80,100,125];
   let rec=series[series.length-1];
   for(const s of series){ if(s>=target){ rec=s; break; } }
   const useName={light:'照明',socket:'插座',ac:'空调',water:'厨卫电器'}[use]||'照明';
   const poleName={1:'1P',2:'2P',3:'3P'}[pole]||'1P';
   let html=dataGrid([
     [rec+' A','推荐额定电流'],
     [target.toFixed(1)+' A','计算值（1.25×I）'],
     [poleName,'极数'],
     [useName,'回路用途']
   ]);
   const note = rec>I*2.5 ? ' <p class="tip-error" style="margin-top:8px;">⚠️ 额定值明显高于负载（>'+(I*2.5).toFixed(1)+'A），可能失去过载保护作用，请核对负载计算。</p>' : ' <p style="color:var(--ok,#16a34a);margin-top:8px;">✅ 额定值在负载的 1.25–2.5 倍之间，选择合理。</p>';

   // 常见回路配置参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见回路断路器配置参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">回路</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">常见负载</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">推荐额定</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">照明</td><td style="border:1px solid #d1d5db;padding:5px 8px;">LED 灯具</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10A / 1P</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">普通插座</td><td style="border:1px solid #d1d5db;padding:5px 8px;">电视/电脑/小家电</td><td style="border:1px solid #d1d5db;padding:5px 8px;">16A / 1P</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">厨房</td><td style="border:1px solid #d1d5db;padding:5px 8px;">微波炉/电饭煲</td><td style="border:1px solid #d1d5db;padding:5px 8px;">20A / 1P+N</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">卫生间</td><td style="border:1px solid #d1d5db;padding:5px 8px;">电热水器</td><td style="border:1px solid #d1d5db;padding:5px 8px;">20–25A / 1P+N</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">空调</td><td style="border:1px solid #d1d5db;padding:5px 8px;">挂机/柜机</td><td style="border:1px solid #d1d5db;padding:5px 8px;">16–25A / 1P(柜机 2P)</td></tr>'+
     '</table>';

   ToolBox.setResult('result', html + note);
 """,
 "notes":[
   "断路器额定电流 ≈ 负载电流 × 1.25，并向上取常见规格（6/10/16/20/25/32/40…）",
   "电动机等冲击性负载（空调）需考虑启动电流，可选 D 型脱扣曲线",
   "额定值过高会失去过载保护，过低会频繁误跳闸",
   "结果仅供参考，正式设计按 GB 50054 与厂家选型手册执行",
 ],
},
# ============ 17. 钢材型材重量 ============
{
 "slug":"steel-profile-weight","industry":"steel","cat":"calculator","icon":"🔩","bg":"#e0f2fe",
 "accent":"#0EA5E9","indicon":"🔧",
 "title":"钢材型材重量计算器",
 "h1":"钢材型材重量计算器",
 "h2":"🔩 钢材型材重量计算器",
 "desc":"钢材型材重量计算器 - 按理论密度公式计算圆钢、方钢、扁钢、角钢、槽钢、工字钢等型材的重量。纯前端本地处理。",
 "intro":"钢材采购与运输按重量计费。选择型材类型，输入尺寸与长度，按理论重量公式（密度 7.85 g/cm³）自动换算重量。",
 "inputs":[
   {"id":"type","label":"型材类型","value":"round","step":"0","type":"select","opts":[
     ["round","圆钢/圆管"],["square","方钢"],["flat","扁钢"],["angle","等边角钢"],["channel","槽钢"]]},
   {"id":"d1","label":"主尺寸 a（mm）","value":"20","step":"1","min":"3"},
   {"id":"d2","label":"次尺寸 b（mm，扁钢/槽钢用）","value":"10","step":"1","min":"0"},
   {"id":"t","label":"壁厚/边厚 t（mm，管/角钢用）","value":"3","step":"0.5","min":"0"},
   {"id":"len","label":"长度（m）","value":"6","step":"0.5","min":"0.5"},
 ],
 "calc":r"""
   const type=document.getElementById('type').value;
   const a=num('d1'), b=num('d2'), t=num('t'), L=num('len');
   if(a<=0||L<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的主尺寸与长度。</p>');return;}
   let kgm=0;
   if(type==='round'||type==='0'){ kgm=a*a*0.00617; }
   else if(type==='square'){ kgm=a*a*0.00785; }
   else if(type==='flat'){ kgm=a*b*0.00785; }
   else if(type==='angle'){ kgm=(2*a-t)*t*0.00785; }
   else if(type==='channel'){ kgm=(a+b-2*t)*t*0.00785*1.05; }
   const total=kgm*L;
   const names={round:'圆钢/圆管',square:'方钢',flat:'扁钢',angle:'等边角钢',channel:'槽钢'}[type]||'圆钢/圆管';
   let html=dataGrid([
     [kgm.toFixed(3)+' kg/m','理论单重'],
     [total.toFixed(2)+' kg','总重量'],
     [L.toFixed(1)+' m','长度'],
     [names,'型材类型']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按碳钢密度 7.85 g/cm³ 理论计算。圆钢：a²×0.00617；方钢：a²×0.00785；扁钢：a×b×0.00785；等边角钢：(2a−t)×t×0.00785。实际重量含公差与表面状态差异。</p>';

   // 常用型材规格重量参考
   html += '<div style="margin-top:12px;font-size:13px;"><b>常用型材理论重量参考（kg/m）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">规格</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">圆钢</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">方钢</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">扁钢</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">10mm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0.617</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0.785</td><td style="border:1px solid #d1d5db;padding:5px 8px;">—</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">20mm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2.47</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3.14</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1.57(20×10)</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">40mm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">9.87</td><td style="border:1px solid #d1d5db;padding:5px 8px;">12.56</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3.14(40×10)</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">50mm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">15.42</td><td style="border:1px solid #d1d5db;padding:5px 8px;">19.63</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3.93(50×10)</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "理论重量按密度 7.85 g/cm³ 计算，为近似值",
   "圆钢 0.00617、方钢 0.00785、扁钢 0.00785 为常用经验系数",
   "型材实际重量允许 ±5% 左右公差",
   "结果仅供参考，结算以过磅重量为准",
 ],
},
# ============ 18. 火锅食材分量 ============
{
 "slug":"hotpot-portion","industry":"fun","cat":"calculator","icon":"🍲","bg":"#fee2e2",
 "accent":"#EF4444","indicon":"🎮",
 "title":"火锅食材分量计算器",
 "h1":"火锅食材分量计算器",
 "h2":"🍲 火锅食材分量计算器",
 "desc":"火锅食材分量计算器 - 按人数与荤素比例推荐各类火锅食材克数，避免浪费或不够吃。纯前端本地处理。",
 "intro":"朋友聚餐吃火锅，最愁买多少。输入人数与口味偏好，按人均食量推荐肉类、蔬菜、豆制品、主食的分量建议。",
 "inputs":[
   {"id":"people","label":"用餐人数","value":"4","step":"1","min":"1","max":"30"},
   {"id":"style","label":"口味偏好","value":"meat","step":"0","type":"select","opts":[
     ["meat","无肉不欢"],["balance","荤素均衡"],["veg","素食为主"]]},
   {"id":"intensity","label":"食量","value":"normal","step":"0","type":"select","opts":[
     ["light","小食量"],["normal","正常"],["heavy","大食量"]]},
 ],
 "calc":r"""
   const people=Math.floor(num('people'));
   if(people<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效人数。</p>');return;}
   const style=document.getElementById('style').value;
   const intensity=document.getElementById('intensity').value;
   const k={light:0.85,normal:1.0,heavy:1.2}[intensity]||1.0;
   let meatP, vegP;
   if(style==='meat'||style==='0'){meatP=0.55;vegP=0.25;}
   else if(style==='balance'){meatP=0.40;vegP=0.40;}
   else{meatP=0.20;vegP=0.60;}
   const total=people*600*k;   // 人均 600g 基准
   const meat=Math.round(total*meatP);
   const veg=Math.round(total*vegP);
   const soy=Math.round(total*0.15);
   const staple=Math.round(people*80*k);
   const soup=Math.round(people*250*k);
   let html=dataGrid([
     [meat+' g','肉类/海鲜'],
     [veg+' g','蔬菜菌菇'],
     [soy+' g','豆制品'],
     [staple+' g','主食'],
     [soup+' ml','汤底用量']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按人均 600g 食材、'+({meat:'无肉不欢',balance:'荤素均衡',veg:'素食为主'}[style]||'荤素均衡')+' 比例估算。肉类可再细分牛羊肉卷、丸滑等，蔬菜按叶菜 70%/根茎 30% 搭配。</p>';

   // 锅底类型适配参考
   html += '<div style="margin-top:12px;font-size:13px;"><b>锅底与蘸料适配参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">锅底</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">特点</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适配食材</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">麻辣红油</td><td style="border:1px solid #d1d5db;padding:5px 8px;">重口刺激</td><td style="border:1px solid #d1d5db;padding:5px 8px;">牛羊肉、毛肚、鸭血</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">菌汤</td><td style="border:1px solid #d1d5db;padding:5px 8px;">鲜香清爽</td><td style="border:1px solid #d1d5db;padding:5px 8px;">菌菇、蔬菜、豆腐</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">番茄</td><td style="border:1px solid #d1d5db;padding:5px 8px;">酸甜开胃</td><td style="border:1px solid #d1d5db;padding:5px 8px;">虾滑、鱼片、豆制品</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">鸳鸯</td><td style="border:1px solid #d1d5db;padding:5px 8px;">众口可调</td><td style="border:1px solid #d1d5db;padding:5px 8px;">全品类</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "人均食材量约 600g，汤底约 250ml/人",
   "荤素比例按口味偏好调整：无肉不欢 55/25、均衡 40/40、素食 20/60",
   "大食量按 1.2 倍、小食量按 0.85 倍折算",
   "以上为参考建议，实际按食量与菜品搭配调整",
 ],
},
# ============ 19. 烧烤食材分量 ============
{
 "slug":"bbq-portion","industry":"fun","cat":"calculator","icon":"🍢","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"🎮",
 "title":"烧烤食材分量计算器",
 "h1":"烧烤食材分量计算器",
 "h2":"🍢 烧烤食材分量计算器",
 "desc":"烧烤食材分量计算器 - 按人数推荐烧烤串数、肉类与配菜分量，户外烧烤备货不再愁。纯前端本地处理。",
 "intro":"户外烧烤备货最容易买多或买少。输入人数与食量，得到肉串、海鲜、蔬菜串与饮品的数量建议，兼顾荤素搭配。",
 "inputs":[
   {"id":"people","label":"人数","value":"6","step":"1","min":"1","max":"40"},
   {"id":"type","label":"烧烤类型","value":"bbq","step":"0","type":"select","opts":[
     ["bbq","中式烤串"],["korean","韩式烤肉"],["steak","牛排/烤肉"]]},
   {"id":"drink","label":"含饮品","value":"yes","step":"0","type":"select","opts":[
     ["yes","含酒水饮料"],["no","不含"]]},
 ],
 "calc":r"""
   const people=Math.floor(num('people'));
   if(people<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效人数。</p>');return;}
   const type=document.getElementById('type').value;
   const drink=document.getElementById('drink').value;
   let meatPer, skewerPer;
   if(type==='bbq'||type==='0'){meatPer=350;skewerPer=12;}
   else if(type==='korean'){meatPer=450;skewerPer=0;}
   else{meatPer=400;skewerPer=0;}
   const meat=Math.round(meatPer*people);
   const veg=Math.round(200*people);
   const sides=Math.round(150*people);
   const drinks=drink==='yes'?Math.round((people*700)/330):0;
   const skewers=skewerPer?skewerPer*people:0;
   let html=dataGrid([
     [(skewers?skewers+' 串':'—'),'肉串数'],
     [meat+' g','肉类总量'],
     [veg+' g','蔬菜'],
     [sides+' g','主食/小食'],
     [drinks?drinks+' 瓶':'—','饮品（330ml）']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按'+({bbq:'中式烤串',korean:'韩式烤肉',steak:'牛排/烤肉'}[type]||'中式烤串')+'模式估算：中式烤串人均 12 串约 350g 肉，韩式烤肉人均 450g 肉。实际按性别比例与食量微调。</p>';

   // 常见烤串参考
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见烤串单串参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">串品</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">单串约</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">烤制要点</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">羊肉串</td><td style="border:1px solid #d1d5db;padding:5px 8px;">25–30g</td><td style="border:1px solid #d1d5db;padding:5px 8px;">中高火 6–8 分钟</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">牛肉串</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30g</td><td style="border:1px solid #d1d5db;padding:5px 8px;">大火快烤锁汁</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">鸡翅</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1 个/串</td><td style="border:1px solid #d1d5db;padding:5px 8px;">中火慢烤 10–12 分钟</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">五花肉</td><td style="border:1px solid #d1d5db;padding:5px 8px;">25g</td><td style="border:1px solid #d1d5db;padding:5px 8px;">烤出油脂更香</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "中式烤串：人均 12 串、肉 350g；韩式烤肉：人均 450g 肉",
   "蔬菜人均 200g、主食小食 150g 为参考",
   "饮品按人均 700ml 估算（含酒水）",
   "以上为备货参考，实际按聚餐习惯调整",
 ],
},
# ============ 20. 随机姓名生成器 ============
{
 "slug":"random-name-gen","industry":"fun","cat":"generate","icon":"👤","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"🎮",
 "title":"随机姓名生成器",
 "h1":"随机姓名生成器",
 "h2":"👤 随机姓名生成器",
 "desc":"随机姓名生成器 - 基于百家姓与常用字随机组合生成中文姓名，可指定性别、字数与批量数量。纯前端本地处理。",
 "intro":"起名参考、测试数据、小说角色都能用：选择性别与姓名长度，批量生成随机中文姓名，支持一键复制全部。",
 "inputs":[
   {"id":"gender","label":"性别","value":"any","step":"0","type":"select","opts":[
     ["any","不限"],["male","偏男性"],["female","偏女性"]]},
   {"id":"chars","label":"姓名长度","value":"2","step":"0","type":"select","opts":[
     ["2","两字名"],["3","三字名"]]},
   {"id":"count","label":"生成数量","value":"10","step":"0","type":"select","opts":[
     ["5","5 个"],["10","10 个"],["20","20 个"],["50","50 个"]]},
 ],
 "calc":r"""
   var _genNames=[];
   var copyNames=function(){};
   const gender=document.getElementById('gender').value;
   const chars=document.getElementById('chars').value;
   const count=parseInt(document.getElementById('count').value)||10;
   const surnames=['王','李','张','刘','陈','杨','赵','黄','周','吴','徐','孙','胡','朱','高','林','何','郭','马','罗','梁','宋','郑','谢','韩','唐','冯','于','董','萧','程','曹','袁','邓','许','傅','沈','曾','彭','吕','苏','卢','蒋','蔡','贾','丁','魏','薛','叶','阎','余','潘','杜','戴','夏','钟','汪','田','任','姜','范','方','石','姚','谭','廖','邹','熊','金','陆','郝','孔','白','崔','康','毛','邱','秦','江','史','顾','侯','邵','孟','龙','万','段','雷','钱','汤','尹','黎','易','常','武','乔','贺','赖','龚','文'];
   const maleChars=['伟','强','磊','军','洋','勇','杰','涛','明','超','刚','平','辉','鹏','华','飞','宇','浩','凯','健','俊','峰','亮','波','斌','晨','龙','松','鑫','博'];
   const femaleChars=['芳','娜','敏','静','丽','艳','娟','燕','婷','雪','琳','颖','玲','英','红','霞','萍','凤','玉','秀','香','月','梅','慧','兰','清','欢','萱','欣','怡'];
   const neutralChars=['子','文','思','嘉','嘉','悦','然','辰','轩','安','乐','晨','涵','宁','泽','瑞','熙','铭','航','霖'];
   const pick=arr=>arr[Math.floor(Math.random()*arr.length)];
   const names=[];
   for(let i=0;i<count;i++){
     const s=pick(surnames);
     const pool=gender==='male'?maleChars:gender==='female'?femaleChars:neutralChars.concat(maleChars,femaleChars);
     let given=chars==='3'?pick(pool)+pick(pool):pick(pool);
     // 避免叠字尴尬：三字名中间字与末字不同
     if(chars==='3'&&given[0]===given[1]) given=given[0]+pick(neutralChars);
     names.push(s+given);
   }
   let html='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;">';
   names.forEach(function(nm){
     html+='<div style="background:var(--result-bg);border:1px solid var(--border);border-radius:10px;padding:10px;text-align:center;font-size:15px;font-weight:600;">'+nm+'</div>';
   });
   html+='</div><div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;">'+
     '<button type="button" class="btn" onclick="calcTool()">换一批</button>'+
     '<button type="button" class="btn primary" onclick="copyNames()">复制全部</button></div>';
   _genNames=names;
   copyNames=function(){
     if(!_genNames||!_genNames.length){ToolBox.showToast('请先生成姓名');return;}
     ToolBox.copyText(_genNames.join('、'),'姓名已复制','复制失败');
   };
   ToolBox.setResult('result', html);
""",
 "notes":[
   "姓氏取自常见百家姓前 100 高频姓",
   "名字用字按性别分类（男/女/中性），避免叠字",
   "生成结果仅供娱乐与参考，不构成起名建议",
   "如需正式起名请结合生辰八字与文化含义",
 ],
},
# ============ 21. 满减凑单计算器 ============
{
 "slug":"groupon-filler","industry":"ecommerce","cat":"calculator","icon":"🧾","bg":"#fee2e2",
 "accent":"#EF4444","indicon":"🔧",
 "title":"满减凑单计算器",
 "h1":"满减凑单计算器",
 "h2":"🧾 满减凑单计算器",
 "desc":"满减凑单计算器 - 输入商品价格与满减门槛，找出最省的凑单方案与差额，电商购物必用。纯前端本地处理。",
 "intro":"满 300 减 50，还差 12 元？把候选商品价格列出来，工具自动找出最优凑单组合（一个或多个商品），算出最小差额与最终实付。",
 "inputs":[
   {"id":"target","label":"满减门槛（元）","value":"300","step":"10","min":"1"},
   {"id":"cut","label":"优惠金额（元）","value":"50","step":"5","min":"0"},
   {"id":"cur","label":"当前已选金额（元）","value":"288","step":"1","min":"0"},
   {"id":"cands","label":"候选凑单商品价（逗号分隔）","value":"12,18,25,39,49,59,89,128","step":"0","type":"text"},
 ],
 "calc":r"""
   const target=num('target'), cut=num('cut'), cur=num('cur');
   const raw=document.getElementById('cands').value||'';
   const cands=raw.split(/[,，;；\s]+/).map(Number).filter(n=>!isNaN(n)&&n>0).sort((a,b)=>a-b);
   if(target<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的满减门槛。</p>');return;}
   if(!cands.length){ToolBox.setResult('result','<p class="tip-error">请至少输入一个候选商品价格。</p>');return;}
   const need=Math.max(0,target-cur);
   // 找单件最优
   let best=null;
   cands.forEach(v=>{
     if(v>=need){
       const gap=v-need;
       if(!best||gap<best.gap) best={items:[v],gap:gap,total:v};
     }
   });
   // 两件组合最优（价格升序，双指针）
   let lo=0,hi=cands.length-1;
   while(lo<hi){
     const sum=cands[lo]+cands[hi];
     if(sum>=need){
       const gap=sum-need;
       if(!best||gap<best.gap) best={items:[cands[lo],cands[hi]],gap:gap,total:sum};
       hi--;
     }else{lo++;}
   }
   if(!best){
     const sum=cands.reduce((a,b)=>a+b,0);
     best={items:cands,gap:Math.max(0,sum-need),total:sum};
   }
   const finalPay=Math.max(0,cur+best.total-cut);
   const effective=(cur+best.total-cut)/(cur+best.total)*100;
   let html=dataGrid([
     ['差 '+need.toFixed(2)+' 元','距离满减差额'],
     [best.items.join(' + ')+' 元','推荐凑单'],
     ['+'+best.gap.toFixed(2)+' 元','最小差额'],
     [fmtMoney(finalPay),'实付金额'],
     [effective.toFixed(2)+'%','折扣率']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">若候选价均不足差额，已取全部候选总和估算。实际可用多个商品叠加，购物车结算前请以平台券规则为准。</p>';

   // 常见满减档位参考
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见满减档位参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">档位</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">折扣率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">凑单建议</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">满200减30</td><td style="border:1px solid #d1d5db;padding:5px 8px;">85折</td><td style="border:1px solid #d1d5db;padding:5px 8px;">差 30 内买日用品</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">满300减50</td><td style="border:1px solid #d1d5db;padding:5px 8px;">83折</td><td style="border:1px solid #d1d5db;padding:5px 8px;">差 50 内买耗材</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">满400减60</td><td style="border:1px solid #d1d5db;padding:5px 8px;">85折</td><td style="border:1px solid #d1d5db;padding:5px 8px;">差 60 内买零食</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "单件最优 + 两件双指针组合求最小差额",
   "候选价格需为可单独凑单的商品（平台部分商品不参与满减）",
   "实付 = 当前金额 + 凑单 - 优惠，折扣率越低越划算",
   "结果仅供参考，以电商平台结算页为准",
 ],
},
# ============ 22. 成本价/售价/利润互算 ============
{
 "slug":"cost-price-margin","industry":"sales","cat":"calculator","icon":"📊","bg":"#dbeafe",
 "accent":"#3B82F6","indicon":"📈",
 "title":"成本价/售价/利润互算器",
 "h1":"成本价/售价/利润互算器",
 "h2":"📊 成本价/售价/利润互算器",
 "desc":"成本价/售价/利润互算器 - 已知任意两项求第三项：成本、售价、利润额、利润率、加价率五变量互算。纯前端本地处理。",
 "intro":"做生意常要倒推定价：已知成本与期望利润率求售价，或已知售价与成本算利润率。本工具五变量互算，输入任意两项即可。",
 "inputs":[
   {"id":"mode","label":"计算模式","value":"price","step":"0","type":"select","opts":[
     ["price","已知成本+利润率 → 求售价"],["cost","已知售价+利润率 → 求成本"],["margin","已知成本+售价 → 求利润率"]]},
   {"id":"cost","label":"成本价（元）","value":"60","step":"0.5","min":"0"},
   {"id":"price","label":"售价（元）","value":"100","step":"0.5","min":"0"},
   {"id":"margin","label":"利润率（%）","value":"40","step":"1","min":"0"},
 ],
 "calc":r"""
   const mode=document.getElementById('mode').value;
   const cost=num('cost'), price=num('price'), margin=num('margin')/100;
   let out;
   if(mode==='price'){
     if(cost<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效成本价。</p>');return;}
     const p=cost*(1+margin);
     out=[['售价（元）',fmtMoney(p)],['利润额（元）',fmtMoney(p-cost)],['利润率',(margin*100).toFixed(1)+'%'],['加价率',(margin*100).toFixed(1)+'%']];
   }else if(mode==='cost'){
     if(price<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效售价。</p>');return;}
     const c=price/(1+margin);
     out=[['成本价（元）',fmtMoney(c)],['利润额（元）',fmtMoney(price-c)],['利润率',(margin*100).toFixed(1)+'%']];
   }else{
     if(cost<=0||price<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的成本与售价。</p>');return;}
     const m=(price-cost)/price*100;
     const mkup=(price-cost)/cost*100;
     out=[['利润率（毛利/售价）',m.toFixed(1)+'%'],['加价率（毛利/成本）',mkup.toFixed(1)+'%'],['利润额（元）',fmtMoney(price-cost)]];
   }
   let html='<div class="data-grid">'+out.map(r=>'<div class="data-card"><div class="num">'+r[1]+'</div><div class="label">'+r[0]+'</div></div>').join('')+'</div>';
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">利润率 = 利润÷售价；加价率 = 利润÷成本。电商常用利润率口径，实体常用加价率，二者勿混。</p>';

   // 利润率/加价率对照表
   html += '<div style="margin-top:12px;font-size:13px;"><b>利润率 ↔ 加价率对照表</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">利润率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">加价率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">示例(成本100)</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">20%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">25%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">售价 125</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">30%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">42.9%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">售价 142.9</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">40%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">66.7%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">售价 166.7</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">50%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">100%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">售价 200</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "利润率（毛利） = （售价 − 成本）÷ 售价",
   "加价率 = （售价 − 成本）÷ 成本，与利润率口径不同",
   "输入任意两项即可推出其余，支持成本→售价与售价→成本双向",
   "结果仅供参考，定价请结合费用结构与市场行情",
 ],
},
# ============ 23. 补休调休计算 ============
{
 "slug":"comp-time-calculator","industry":"hr","cat":"calculator","icon":"⏱️","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"🔧",
 "title":"补休调休计算器",
 "h1":"补休调休计算器",
 "h2":"⏱️ 补休调休计算器",
 "desc":"补休调休计算器 - 按加班时长与倍数计算应得补休天数，支持工作日/休息日/法定节假日加班换算。纯前端本地处理。",
 "intro":"加班攒了多少补休？按《劳动法》倍数：工作日加班 1.5 倍、休息日 2 倍（可补休）、法定节假日 3 倍。输入加班时长自动换算补休天数。",
 "inputs":[
   {"id":"hours","label":"加班时长（小时）","value":"12","step":"0.5","min":"0.5"},
   {"id":"dayType","label":"加班类型","value":"weekend","step":"0","type":"select","opts":[
     ["weekday","工作日延时"],["weekend","休息日"],["holiday","法定节假日"]]},
   {"id":"workday","label":"每日标准工时（h）","value":"8","step":"1","min":"4","max":"12"},
 ],
 "calc":r"""
   const hours=num('hours'), workday=num('workday')||8;
   if(hours<=0||workday<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的加班时长。</p>');return;}
   const dayType=document.getElementById('dayType').value;
   const mult={weekday:1.5,weekend:2,holiday:3}[dayType]||2;
   const typeName={weekday:'工作日延时',weekend:'休息日',holiday:'法定节假日'}[dayType]||'休息日';
   const compDays=hours*mult/workday;
   const payHours=hours*mult;
   let html=dataGrid([
     [compDays.toFixed(1)+' 天','折算补休/工时'],
     [payHours.toFixed(1)+' h','折算工时'],
     [hours.toFixed(1)+' h','原始加班'],
     [mult+' 倍',typeName+'倍数']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">法律口径：休息日加班可优先安排补休，不补休则支付 200% 工资；法定节假日加班应支付 300% 工资且一般不安排补休替代。实际以公司制度与当地政策为准。</p>';

   // 加班补偿规则参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>加班补偿规则参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">加班类型</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">倍数</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">补偿方式</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">工作日延时</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1.5 倍</td><td style="border:1px solid #d1d5db;padding:5px 8px;">支付加班费</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">休息日</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2 倍</td><td style="border:1px solid #d1d5db;padding:5px 8px;">优先补休，否则 200%</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">法定节假日</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3 倍</td><td style="border:1px solid #d1d5db;padding:5px 8px;">支付 300%，一般不可替代</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "倍数：工作日 1.5、休息日 2、法定节假日 3",
   "补休天数 = 加班时长 × 倍数 ÷ 每日标准工时",
   "法定节假日加班原则上支付 300% 工资，不以补休替代",
   "结果仅供参考，以《劳动法》及当地实施细则为准",
 ],
},
# ============ 24. 年假折算计算 ============
{
 "slug":"annual-leave-prorate","industry":"hr","cat":"calculator","icon":"🏖️","bg":"#dbeafe",
 "accent":"#3B82F6","indicon":"🔧",
 "title":"年假折算计算器",
 "h1":"年假折算计算器",
 "h2":"🏖️ 年假折算计算器",
 "desc":"年假折算计算器 - 按入职日期、累计工龄与离职/折算日期计算当年应休年假天数（按比例折算）。纯前端本地处理。",
 "intro":"当年入职或离职，年假按剩余日历天数折算。输入入职日期、累计工龄与折算截止日期，自动算当年应休年假。",
 "inputs":[
   {"id":"start","label":"入职日期","value":"2026-03-15","step":"1","type":"date"},
   {"id":"years","label":"累计工龄（年）","value":"5","step":"1","min":"0","max":"40"},
   {"id":"end","label":"折算截止日期（当年12/31 或离职日）","value":"2026-12-31","step":"1","type":"date"},
 ],
 "calc":r"""
   const sRaw=document.getElementById('start').value;
   const eRaw=document.getElementById('end').value;
   const years=Math.floor(num('years'));
   if(!sRaw||!eRaw){ToolBox.setResult('result','<p class="tip-error">请选择有效的日期。</p>');return;}
   const s=new Date(sRaw), e=new Date(eRaw);
   if(isNaN(s.getTime())||isNaN(e.getTime())||e<s){ToolBox.setResult('result','<p class="tip-error">日期无效或截止日早于入职日。</p>');return;}
   const annual = years<1?0 : years<10?5 : years<20?10 : 15;
   if(annual===0){ToolBox.setResult('result','<p class="tip-error">累计工龄不足 1 年，不享受带薪年假（按法规）。</p>');return;}
   const yearStart=new Date(e.getFullYear(),0,1);
   const startEff= s>yearStart ? s : yearStart;   // 当年实际在职起点
   const totalDays=(new Date(e.getFullYear(),11,31)-yearStart)/86400000+1;
   const worked=(e-startEff)/86400000+1;
   const days=annual*worked/totalDays;
   const rounded=days<0.5?0:Math.ceil(days);
   let html=dataGrid([
     [annual+' 天','应享年假基数'],
     [Math.round(worked)+' 天','当年在职天数'],
     [totalDays+' 天','当年总天数'],
     [rounded+' 天','折算应休年假'],
     [days.toFixed(2)+' 天','折算精确值']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按《职工带薪年休假条例》：累计工龄 1–9 年 5 天、10–19 年 10 天、≥20 年 15 天。当年折算 = 基数 × 当年在职天数 ÷ 365，不足 0.5 天不计。具体以单位制度为准。</p>';

   // 工龄-年假天数对照表
   html += '<div style="margin-top:12px;font-size:13px;"><b>累计工龄与年假天数对照</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">累计工龄</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">年假天数</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">法规依据</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1–9 年</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5 天</td><td style="border:1px solid #d1d5db;padding:5px 8px;">条例第三条</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">10–19 年</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10 天</td><td style="border:1px solid #d1d5db;padding:5px 8px;">条例第三条</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">≥20 年</td><td style="border:1px solid #d1d5db;padding:5px 8px;">15 天</td><td style="border:1px solid #d1d5db;padding:5px 8px;">条例第三条</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "工龄 1–9 年 5 天、10–19 年 10 天、≥20 年 15 天",
   "当年入职/离职按剩余日历天数比例折算，不足 0.5 天不计",
   "折算 = 基数 × 当年在职天数 ÷ 365",
   "结果仅供参考，以《职工带薪年休假条例》与单位制度为准",
 ],
},
# ============ 25. 喂奶量估算 ============
{
 "slug":"feeding-amount-baby","industry":"parenting","cat":"calculator","icon":"🍼","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"👶",
 "title":"婴儿喂奶量估算器",
 "h1":"婴儿喂奶量估算器",
 "h2":"🍼 婴儿喂奶量估算器",
 "desc":"婴儿喂奶量估算器 - 按月龄与体重估算每餐与每日奶量，覆盖新生儿至 12 月龄配方奶喂养参考。纯前端本地处理。",
 "intro":"新手爸妈最常问：一顿喂多少？按月龄与体重，结合「每日奶量 ≈ 体重×150ml/kg」与月龄参考值，给出每餐与每日奶量区间。",
 "inputs":[
   {"id":"month","label":"月龄（月）","value":"4","step":"1","min":"0","max":"12"},
   {"id":"weight","label":"体重（kg）","value":"6.8","step":"0.1","min":"2"},
   {"id":"feeds","label":"每日喂奶次数","value":"6","step":"1","min":"4","max":"12"},
 ],
 "calc":r"""
   const month=Math.floor(num('month')), weight=num('weight'), feeds=Math.floor(num('feeds'))||6;
   if(weight<=0||month<0||month>12){ToolBox.setResult('result','<p class="tip-error">请输入有效的月龄与体重。</p>');return;}
   const byWeight=weight*150;         // 150ml/kg
   const refMap=[700,750,800,850,900,950,1000,1000,1000,1000,1000,1000,1000];
   const ref=refMap[Math.min(month,12)];
   const daily=Math.round((byWeight+ref)/2);
   const perFeed=feeds>0?Math.round(daily/feeds):0;
   let html=dataGrid([
     [daily+' ml','每日奶量建议'],
     [perFeed+' ml','每餐奶量'],
     [Math.round(byWeight)+' ml','按体重估算'],
     [ref+' ml','按月龄参考']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">'+month+' 月龄、体重 '+weight.toFixed(1)+'kg、每日 '+feeds+' 餐。每餐约 '+perFeed+' ml。宝宝有个体差异，以饥饿信号与生长曲线为准，出现吐奶/胀气请减量观察。</p>';

   // 月龄-每日奶量参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>月龄每日奶量参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">月龄</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">每日总量</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">每餐约</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">次数</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">新生儿</td><td style="border:1px solid #d1d5db;padding:5px 8px;">90–150ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">15–30ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">8–12 次</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1–3 月</td><td style="border:1px solid #d1d5db;padding:5px 8px;">600–800ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">60–120ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">7–8 次</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">4–6 月</td><td style="border:1px solid #d1d5db;padding:5px 8px;">800–1000ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">120–180ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">6 次</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">7–12 月</td><td style="border:1px solid #d1d5db;padding:5px 8px;">800ml+辅食</td><td style="border:1px solid #d1d5db;padding:5px 8px;">180–240ml</td><td style="border:1px solid #d1d5db;padding:5px 8px;">4–5 次</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "每日奶量 ≈ 体重 × 150ml/kg，按月龄参考值取中",
   "新生儿期每 2–3 小时一喂，随月龄增大单次量增加、次数减少",
   "6 月龄后开始添加辅食，奶量逐步过渡",
   "结果仅供参考，喂养以儿科医生指导与宝宝实际需求为准",
 ],
},
# ============ 26. 配方奶冲调计算 ============
{
 "slug":"formula-mixing","industry":"parenting","cat":"calculator","icon":"🥛","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"👶",
 "title":"配方奶冲调计算器",
 "h1":"配方奶冲调计算器",
 "h2":"🥛 配方奶冲调计算器",
 "desc":"配方奶冲调计算器 - 按奶粉冲调比例换算奶量所需的奶粉勺数与水量，支持常见 30ml/勺与自定义比例。纯前端本地处理。",
 "intro":"冲奶粉别凭感觉：输入目标奶量与奶粉罐冲调比例（每勺兑水量），自动算所需勺数与水量，避免过浓或过稀。",
 "inputs":[
   {"id":"target","label":"目标奶量（ml）","value":"180","step":"10","min":"30"},
   {"id":"ratio","label":"冲调比例（ml/勺）","value":"30","step":"5","min":"10","max":"60"},
   {"id":"waterFirst","label":"先放水再放粉","value":"yes","step":"0","type":"select","opts":[
     ["yes","是（推荐）"],["no","否"]]},
 ],
 "calc":r"""
   const target=num('target'), ratio=num('ratio')||30;
   if(target<=0||ratio<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的奶量与比例。</p>');return;}
   const scoops=Math.round(target/ratio);
   const water=scoops*ratio;
   const total=water+Math.round(scoops*4.3);  // 每勺约 4.3g 粉，体积略增
   let html=dataGrid([
     [scoops+' 勺','所需奶粉勺数'],
     [water+' ml','所需水量（按比例）'],
     [total+' ml','冲调后约'],
     [ratio+' ml/勺','冲调比例']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">先加 '+(water)+' ml 温水（约 40–70°C，按罐体说明），再平勺加入 '+(scoops)+' 勺奶粉，摇匀至无颗粒。注意：先水后粉避免过浓；勺必须刮平。</p>';

   // 常见冲调比参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见奶粉冲调比参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">品牌系列</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">比例</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">水温建议</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">飞鹤星飞帆</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30ml/勺</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40–50°C</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">美赞臣蓝臻</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30ml/勺</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40°C</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">惠氏启赋</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30ml/勺</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40–45°C</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">爱他美卓萃</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30ml/勺</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40°C</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "多数奶粉为 30ml/勺，请以罐体标注为准",
   "平勺取粉（刮平），先水后粉，水温按罐体说明（通常 40–70°C）",
   "冲调后体积略大于水量，属正常",
   "结果仅供参考，以奶粉罐冲调说明为准",
 ],
},
# ============ 27. 纸尿裤用量估算 ============
{
 "slug":"diaper-usage","industry":"parenting","cat":"calculator","icon":"🧷","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"👶",
 "title":"纸尿裤用量估算器",
 "h1":"纸尿裤用量估算器",
 "h2":"🧷 纸尿裤用量估算器",
 "desc":"纸尿裤用量估算器 - 按月龄估算每日纸尿裤片数与月用量、费用，囤货前先算清。纯前端本地处理。",
 "intro":"囤纸尿裤最怕囤错码或囤多。按月龄查每日参考片数，输入单片均价，自动算月用量与费用，帮你规划购买数量。",
 "inputs":[
   {"id":"month","label":"宝宝月龄（月）","value":"6","step":"1","min":"0","max":"36"},
   {"id":"price","label":"单片均价（元）","value":"1.2","step":"0.1","min":"0"},
   {"id":"days","label":"估算天数","value":"30","step":"1","min":"1","max":"90"},
 ],
 "calc":r"""
   const month=Math.floor(num('month')), price=num('price'), days=Math.floor(num('days'))||30;
   if(month<0||month>36){ToolBox.setResult('result','<p class="tip-error">请输入 0–36 月龄。</p>');return;}
   // 参考：新生儿 10-12/天，1-3月 8-10，4-6月 6-8，7-12月 5-6，1岁+ 4-5
   let perDay;
   if(month<=1) perDay=11;
   else if(month<=3) perDay=9;
   else if(month<=6) perDay=7;
   else if(month<=12) perDay=5.5;
   else perDay=4.5;
   const total=Math.ceil(perDay*days);
   const cost=total*price;
   const sizeName = month<=1?'NB':month<=3?'S':month<=6?'M':month<=12?'L':'XL';
   let html=dataGrid([
     [perDay.toFixed(1)+' 片','每日用量'],
     [total+' 片',days+' 天总用量'],
     [fmtMoney(cost),'费用估算'],
     [sizeName+' 码','建议尺码']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">'+month+' 月龄约每日 '+perDay.toFixed(1)+' 片，'+days+' 天约 '+total+' 片。宝宝排便频率差异大，实际以更换频率为准；大促可多囤 1 个月量但注意尺码。</p>';

   // 尺码与体重对照表
   html += '<div style="margin-top:12px;font-size:13px;"><b>纸尿裤尺码对照（体重）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">尺码</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适用体重</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">约月龄</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">NB</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≤5kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0–1 月</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">S</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3–8kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1–4 月</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">M</td><td style="border:1px solid #d1d5db;padding:5px 8px;">6–11kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">4–10 月</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">L</td><td style="border:1px solid #d1d5db;padding:5px 8px;">9–14kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10–18 月</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">XL</td><td style="border:1px solid #d1d5db;padding:5px 8px;">12kg+</td><td style="border:1px solid #d1d5db;padding:5px 8px;">18 月+</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "参考片数：新生儿 10–12/天、1–3 月 8–10、4–6 月 6–8、7–12 月 5–6、1 岁后 4–5",
   "尺码：NB 新生儿、S 3–8kg、M 6–11kg、L 9–14kg、XL 12kg+，以宝宝体重为准",
   "纸尿裤随月龄增长单次量增加、频率下降",
   "结果仅供参考，以实际更换与宝宝舒适度为准",
 ],
},
# ============ 28. 背奶计划 ============
{
 "slug":"pumping-plan","industry":"parenting","cat":"calculator","icon":"🧴","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"👶",
 "title":"背奶计划计算器",
 "h1":"背奶计划计算器",
 "h2":"🧴 背奶计划计算器",
 "desc":"背奶计划计算器 - 按返岗工时与宝宝月龄估算每日吸奶次数、间隔与储备量建议，职场妈妈背奶规划。纯前端本地处理。",
 "intro":"返岗后怎么背奶不慌乱？输入工作时长与宝宝月龄，按「每 3–4 小时吸一次」原则给出每日吸奶次数、间隔与单次/总量建议。",
 "inputs":[
   {"id":"hours","label":"上班时长（h）","value":"9","step":"0.5","min":"4","max":"14"},
   {"id":"month","label":"宝宝月龄（月）","value":"6","step":"1","min":"0","max":"12"},
   {"id":"single","label":"单次吸奶量（ml，可选）","value":"120","step":"10","min":"0"},
 ],
 "calc":r"""
   const hours=num('hours'), month=Math.floor(num('month')), single=num('single');
   if(hours<=0||month<0||month>12){ToolBox.setResult('result','<p class="tip-error">请输入有效的工作时长与月龄。</p>');return;}
   const sessions=Math.max(1,Math.round(hours/3.5));
   const interval=hours/sessions;
   const dailyNeed = month<=2?600:month<=4?700:month<=6?750:month<=8?700:650;
   const perSession=single>0?single:Math.round(dailyNeed/4);
   const storage=perSession*sessions;
   let html=dataGrid([
     [sessions+' 次','上班期间吸奶次数'],
     [interval.toFixed(1)+' h','吸奶间隔'],
     [perSession+' ml','单次建议量'],
     [storage+' ml','单日储备量'],
     [dailyNeed+' ml','宝宝日需奶量']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">建议间隔 3–4 小时吸一次（与宝宝吃奶节奏接近），用防溢乳垫+储奶袋冷藏。吸出的奶按「先吸先喝」原则存放，冷藏 24h 内、冷冻 3 个月内使用。</p>';

   // 母乳储存时长参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>母乳储存时长参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">储存条件</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">时长</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">注意事项</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">室温（25°C）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">4 小时</td><td style="border:1px solid #d1d5db;padding:5px 8px;">避光保存</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">冷藏（4°C）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">24–48 小时</td><td style="border:1px solid #d1d5db;padding:5px 8px;">放冷藏室后部</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">冷冻（−18°C）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3 个月</td><td style="border:1px solid #d1d5db;padding:5px 8px;">标注日期先吸先喝</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "吸奶间隔按 3–4 小时原则，工作时长÷间隔得次数",
   "宝宝日需奶量按月龄估算（600–750ml），个体差异大",
   "冷藏 24h / 冷冻 3 个月，标注日期先吸先喝",
   "结果仅供参考，以宝宝需求与个人泌乳情况为准",
 ],
},
# ============ 29. 洗衣机容量选择 ============
{
 "slug":"washer-capacity","industry":"home","cat":"calculator","icon":"🧺","bg":"#e0f2fe",
 "accent":"#0EA5E9","indicon":"🏡",
 "title":"洗衣机容量选择器",
 "h1":"洗衣机容量选择器",
 "h2":"🧺 洗衣机容量选择器",
 "desc":"洗衣机容量选择器 - 按家庭人口与床品类型推荐洗衣机公斤数，并估算单次用水量。纯前端本地处理。",
 "intro":"买洗衣机容量怎么选？按家庭人口数推荐 5–10kg 区间，并结合是否有大件床品/窗帘判断是否需要更大容量，顺带估算单次用水。",
 "inputs":[
   {"id":"people","label":"家庭人口","value":"3","step":"1","min":"1","max":"10"},
   {"id":"big","label":"常洗大件（床单被套/窗帘）","value":"yes","step":"0","type":"select","opts":[
     ["yes","是"],["no","否"]]},
   {"id":"type","label":"机型","value":"drum","step":"0","type":"select","opts":[
     ["drum","滚筒"],["pulsator","波轮"]]},
 ],
 "calc":r"""
   const people=Math.floor(num('people'));
   if(people<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效人口数。</p>');return;}
   const big=document.getElementById('big').value;
   const type=document.getElementById('type').value;
   let rec=Math.min(10,Math.max(5,people*2.5));
   if(big==='yes'&&rec<8) rec=8;
   if(rec>10) rec=10;
   const water=type==='drum'?Math.round(rec*9):Math.round(rec*30);
   let html=dataGrid([
     [rec+' kg','推荐容量'],
     [water+' L','单次参考用水'],
     [people+' 人','家庭人口'],
     [type==='drum'?'滚筒':'波轮','机型']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按人均 2.5kg 衣物估算：'+people+' 口之家约需 '+rec+'kg。滚筒省水（约 9L/kg）、对衣物磨损小；波轮洗净力强但费水（约 30L/kg）。洗 4 件套床品建议 ≥8kg。</p>';

   // 容量与人口对照表
   html += '<div style="margin-top:12px;font-size:13px;"><b>容量与家庭人口对照</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">家庭</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">推荐容量</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适用场景</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1–2 人</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5–6kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">租房/单身</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">3 人</td><td style="border:1px solid #d1d5db;padding:5px 8px;">7–8kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">三口之家</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">4 人</td><td style="border:1px solid #d1d5db;padding:5px 8px;">8–9kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">床品四件套</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">5 人+</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10kg</td><td style="border:1px solid #d1d5db;padding:5px 8px;">窗帘/大件</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "容量参考：1–2 人 5–6kg、3 人 7–8kg、4 人 8–9kg、5 人+ 10kg",
   "常洗床单被套建议 ≥8kg，窗帘等大件 ≥9kg",
   "滚筒约 9L/kg、波轮约 30L/kg 用水量差异明显",
   "结果仅供参考，结合安装空间与预算选择",
 ],
},
# ============ 30. 家庭用电负荷估算 ============
{
 "slug":"home-load-estimate","industry":"electrical","cat":"calculator","icon":"🏠","bg":"#fef9c3",
 "accent":"#EAB308","indicon":"🔧",
 "title":"家庭用电负荷估算器",
 "h1":"家庭用电负荷估算器",
 "h2":"🏠 家庭用电负荷估算器",
 "desc":"家庭用电负荷估算器 - 按家电清单与同时系数估算家庭总用电负荷，建议进线规格与电表容量。纯前端本地处理。",
 "intro":"装修布线前先算负荷：勾选常用家电并输入数量，按功率与同时系数（需用系数）估算总负荷，判断 2.5/4/6/10mm² 进线与 40/60A 电表是否够用。",
 "inputs":[
   {"id":"fridge","label":"冰箱（台，200W）","value":"1","step":"1","min":"0","max":"5","type":"number"},
   {"id":"ac","label":"空调（台，1200W）","value":"2","step":"1","min":"0","max":"8","type":"number"},
   {"id":"washer","label":"洗衣机（台，500W）","value":"1","step":"1","min":"0","max":"5","type":"number"},
   {"id":"waterheater","label":"电热水器（台，2000W）","value":"1","step":"1","min":"0","max":"5","type":"number"},
   {"id":"kitchen","label":"厨房电器（微波/烤箱/电饭煲 合计，W）","value":"3000","step":"100","min":"0","type":"number"},
   {"id":"light","label":"照明及其他（W）","value":"500","step":"50","min":"0","type":"number"},
 ],
 "calc":r"""
   const fridge=num('fridge'), ac=num('ac'), washer=num('washer'), wh=num('waterheater'), kitchen=num('kitchen'), light=num('light');
   const totalInstalled=fridge*200+ac*1200+washer*500+wh*2000+kitchen+light;
   // 需用系数：同时开启的比例估算
   const coeff=0.6;
   const load=totalInstalled*coeff;
   const current=load/220;
   // 进线建议
   let wire, breaker;
   if(current<=25){wire='2.5 mm²';breaker='32 A';}
   else if(current<=35){wire='4 mm²';breaker='40 A';}
   else if(current<=50){wire='6 mm²';breaker='50 A';}
   else if(current<=70){wire='10 mm²';breaker='63 A';}
   else{wire='≥16 mm²（需复核）';breaker='≥80 A';}
   let html=dataGrid([
     [totalInstalled+' W','装机总功率'],
     [Math.round(load)+' W','估算负荷'],
     [current.toFixed(1)+' A','估算电流'],
     [wire,'建议进线'],
     [breaker,'建议总开关']
   ]);
   html += '<p style="font-size:13px;color:var(--text-muted);margin-top:8px;">按需用系数 0.6 估算（不同时全开）。若空调为多台大功率或含电地暖，请按实际同时使用提高系数。结论供参考，正式设计按 GB 51348 执行。</p>';

   // 常见家电功率参考表
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见家电功率参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">电器</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">功率约</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">备注</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">冰箱</td><td style="border:1px solid #d1d5db;padding:5px 8px;">100–200W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">常开</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">空调挂机</td><td style="border:1px solid #d1d5db;padding:5px 8px;">800–1300W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">变频波动</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">电热水器</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1500–3000W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">加热时段高</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">电磁炉</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1800–2200W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">短时高功率</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">烤箱</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1500–2000W</td><td style="border:1px solid #d1d5db;padding:5px 8px;">预热耗电</td></tr>'+
     '</table>';
 
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "装机功率 × 需用系数（0.6）≈ 计算负荷",
   "电流 = 负荷 ÷ 220V（单相）",
   "进线建议：2.5mm²/32A → 4mm²/40A → 6mm²/50A → 10mm²/63A",
   "结论仅供参考，正式电气设计请咨询持证电工并按规范执行",
 ],
},
{
 "slug":"drinking-water-plan","industry":"life","cat":"calculator","icon":"💧","bg":"#e0f2fe",
 "accent":"#3B82F6","indicon":"🏠",
 "title":"喝水提醒计划计算器",
 "h1":"喝水提醒计划计算器",
 "h2":"💧 喝水提醒计划计算器",
 "desc":"喝水提醒计划计算器 - 按体重、运动量与气温估算每日饮水目标，并生成全天分段饮水提醒计划。纯前端本地处理。",
 "intro":"每天该喝多少水？输入体重、运动强度与当日气温，估算基础饮水量，再叠加运动与高温增量，输出全天分段饮水计划。",
 "inputs":[
   {"id":"w","label":"体重（kg）","value":"60","step":"1","min":"20","max":"200"},
   {"id":"act","label":"当日运动强度","type":"select","options":[["none","基本无运动"],["light","轻度（散步/瑜伽）"],["mid","中度（跑步/骑行 30-60min）"],["high","高强度（健身/球类 1h+）"]],"value":"none"},
   {"id":"temp","label":"当日气温（°C）","value":"26","step":"1","min":"-10","max":"45"},
   {"id":"stage","label":"特殊情况","type":"select","options":[["normal","无"],["preg","孕期"],["lact","哺乳期"]],"value":"normal"},
 ],
 "calc":r"""
   const w=num('w'), act=document.getElementById('act').value, temp=num('temp'), stage=document.getElementById('stage').value;
   if(w<=0||!isFinite(temp)){ToolBox.setResult('result','<p class="tip-error">请输入有效的体重与气温。</p>');return;}
   // 基础：30ml/kg（WHO 一般成人建议区间 30-35ml/kg）
   let base=w*30;
   const actAdd={none:0,light:200,mid:500,high:800}[act]||0;
   let tempAdd=0;
   if(temp>=30) tempAdd=400; else if(temp>=25) tempAdd=250;
   const stageAdd={normal:0,preg:300,lact:700}[stage]||0;
   const total=base+actAdd+tempAdd+stageAdd;
   const cups=total/250;
   // 分段计划：7:00-22:00 每段 1.5h，按比例分配
   let html=dataGrid([
     [fmtMoney(total)+' ml','每日饮水目标'],
     [cups.toFixed(1)+' 杯','约（250ml/杯）'],
     ['+'+(actAdd+tempAdd+stageAdd)+' ml','增量（运动/高温/特殊）'],
     [base+' ml','基础量（体重×30ml）']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>全天分段饮水计划</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">时段</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">建议量</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">说明</th></tr>';
   const slots=[['07:00-08:30',0.15,'起床后补水'],['08:30-10:00',0.12,'上午工作'],['10:00-11:30',0.12,'上午补水'],['11:30-13:00',0.10,'午餐前'],['13:00-14:30',0.10,'午休后'],['14:30-16:00',0.12,'下午工作'],['16:00-17:30',0.12,'下午补水'],['17:30-19:00',0.10,'下班/运动后'],['19:00-20:30',0.07,'晚餐时段'],['20:30-22:00',0.05,'睡前少量']];
   for(let i=0;i<slots.length;i++){
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+slots[i][0]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+Math.round(total*slots[i][1])+' ml</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+slots[i][2]+'</td></tr>';
   }
   html+='</table>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>不同人群每日饮水参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">人群</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">建议量（ml）</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">成人男性</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1700-2000</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">成人女性</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1500-1800</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">孕期</td><td style="border:1px solid #d1d5db;padding:5px 8px;">+300（约2000）</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">哺乳期</td><td style="border:1px solid #d1d5db;padding:5px 8px;">+700（约2500）</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '肾脏疾病、心衰等需限水人群请遵医嘱；剧烈运动后少量多次补充含电解质饮品。估算结果仅供参考。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "基础量按 30ml/kg 估算（WHO 成人一般建议 30-35ml/kg）",
   "运动增量：轻度 200 / 中度 500 / 高强度 800 ml",
   "气温≥30°C 补 400ml，25-29°C 补 250ml",
   "分段计划覆盖 07:00-22:00，睡前 1 小时起少量饮水",
 ],
},
{
 "slug":"meditation-timer","industry":"fun","cat":"calculator","icon":"🧘","bg":"#ede9fe",
 "accent":"#8B5CF6","indicon":"🎮",
 "title":"冥想计时器",
 "h1":"冥想计时器",
 "h2":"🧘 冥想计时器",
 "desc":"冥想计时器 - 设置冥想时长与间隔提醒，生成倒计时计划与呼吸节奏参考。纯前端本地处理。",
 "intro":"冥想需要一个安静的倒计时。设置总时长与每段间隔，自动生成分段计划，附 4-7-8 呼吸法节奏参考。",
 "inputs":[
   {"id":"dur","label":"冥想总时长（分钟）","value":"10","step":"1","min":"1","max":"120"},
   {"id":"seg","label":"间隔提醒（分钟）","value":"2","step":"1","min":"1","max":"30"},
   {"id":"style","label":"冥想方式","type":"select","options":[["breath","呼吸觉察"],["body","身体扫描"],["mantra","咒语默念"],["free","自由冥想"]],"value":"breath"},
 ],
 "calc":r"""
   const dur=Math.floor(num('dur')), seg=Math.floor(num('seg')), style=document.getElementById('style').value;
   if(dur<=0||seg<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的时长与间隔。</p>');return;}
   const nSeg=Math.max(1,Math.round(dur/seg));
   const styleName={breath:'呼吸觉察',body:'身体扫描',mantra:'咒语默念',free:'自由冥想'}[style]||'呼吸觉察';
   const now=new Date();
   const end=new Date(now.getTime()+dur*60000);
   const pad=function(x){return x<10?'0'+x:''+x;};
   const fmtTime=function(d){return pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());};
   let html=dataGrid([
     [dur+' 分钟','冥想总时长'],
     [nSeg+' 段','间隔分段（每 '+seg+' 分钟）'],
     [styleName,'冥想方式'],
     [fmtTime(now)+' 开始','预计 '+fmtTime(end)+' 结束']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>分段倒计时计划</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">段次</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">时刻</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">提示</th></tr>';
   for(let i=0;i<nSeg;i++){
     const t=new Date(now.getTime()+i*seg*60000);
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">第 '+(i+1)+' 段</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+fmtTime(t)+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+(i===0?'开始，放松身体':'回到呼吸')+'</td></tr>';
   }
   html+='</table>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>4-7-8 呼吸法节奏</b></div>'+
     '<div class="tip-mini" style="margin-top:6px;font-size:13px;color:var(--text-muted);">'+
     '吸气 4 秒 → 屏息 7 秒 → 呼气 8 秒，循环 4 次约 76 秒。适合入睡前与压力时使用。</div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>7 天冥想练习计划（渐进）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">天数</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">时长</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">主题</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">要点</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 1</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">呼吸觉察</td><td style="border:1px solid #d1d5db;padding:5px 8px;">感受鼻尖气流</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 2</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">身体扫描</td><td style="border:1px solid #d1d5db;padding:5px 8px;">从头顶到脚趾</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 3</td><td style="border:1px solid #d1d5db;padding:5px 8px;">8 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">呼吸觉察</td><td style="border:1px solid #d1d5db;padding:5px 8px;">数息 1-10 循环</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 4</td><td style="border:1px solid #d1d5db;padding:5px 8px;">8 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">身体扫描</td><td style="border:1px solid #d1d5db;padding:5px 8px;">放松紧张部位</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">呼吸+扫描</td><td style="border:1px solid #d1d5db;padding:5px 8px;">组合练习</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 6</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">咒语默念</td><td style="border:1px solid #d1d5db;padding:5px 8px;">默念"平静"</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">Day 7</td><td style="border:1px solid #d1d5db;padding:5px 8px;">15 分钟</td><td style="border:1px solid #d1d5db;padding:5px 8px;">自由冥想</td><td style="border:1px solid #d1d5db;padding:5px 8px;">不评判念头</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '建议初次冥想 5-10 分钟，随练习增加至 20-30 分钟。坐姿舒适、背部挺直即可。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "间隔提醒按总时长均分，每段结束时回到呼吸",
   "4-7-8 呼吸法：吸气4秒-屏息7秒-呼气8秒",
   "冥想非医疗手段，严重焦虑/失眠请就医",
   "建议手机静音，用振动或柔和提示音",
 ],
},
{
 "slug":"salary-after-tax","industry":"finance","cat":"calculator","icon":"💼","bg":"#fef3c7",
 "accent":"#F59E0B","indicon":"💰",
 "title":"工资税后计算器",
 "h1":"工资税后计算器",
 "h2":"💼 工资税后计算器",
 "desc":"工资税后计算器 - 输入应发工资、五险一金与专项附加扣除，按累计预扣法计算个税与税后到手工资。纯前端本地处理。",
 "intro":"税后工资怎么算？输入应发工资、个人缴纳的五险一金与专项附加扣除，按现行个税累计预扣法计算应纳税额与到手工资。",
 "inputs":[
   {"id":"gross","label":"应发工资（元/月）","value":"15000","step":"100","min":"0"},
   {"id":"ins","label":"五险一金个人缴纳（元/月）","value":"1650","step":"50","min":"0"},
   {"id":"ded","label":"专项附加扣除（元/月）","value":"2000","step":"100","min":"0"},
   {"id":"months","label":"本年累计已发月数","value":"1","step":"1","min":"1","max":"12"},
 ],
 "calc":r"""
   const gross=num('gross'), ins=num('ins'), ded=num('ded'), months=Math.floor(num('months'));
   if(gross<0||months<1){ToolBox.setResult('result','<p class="tip-error">请输入有效的工资与月数。</p>');return;}
   const TH=5000; // 起征点
   const base=gross-TH-ins-ded; // 月应纳税所得额
   // 月度税率表（综合所得）
   const brackets=[[0,0.03,0],[3000,0.10,210],[12000,0.20,1410],[25000,0.25,2660],[35000,0.30,4410],[55000,0.35,7160],[80000,0.45,15160]];
   let tax=0, rate=0, qs=0;
   for(let i=brackets.length-1;i>=0;i--){
     if(base>brackets[i][0]){ rate=brackets[i][1]; qs=brackets[i][2]; tax=base*rate-qs; break; }
   }
   if(base<=0){ tax=0; rate=0; }
   const taxMonthly=Math.max(0,tax);
   const net=gross-ins-ded>TH ? gross-ins-taxMonthly : gross-ins;
   // 简化：不含专项扣除时（ded=0 且 net 口径），统一按 gross - ins - tax
   const netFinal=gross-ins-taxMonthly;
   const ratePct=(rate*100).toFixed(1);
   const actualRate=(taxMonthly/Math.max(gross,1)*100).toFixed(2);
   let html=dataGrid([
     [fmtMoney(gross),'应发工资'],
     [fmtMoney(ins),'五险一金（个人）'],
     [fmtMoney(ded),'专项附加扣除'],
     [fmtMoney(base>0?base:0),'应纳税所得额（月）'],
     [fmtMoney(taxMonthly),'当月个税'],
     [fmtMoney(netFinal),'税后到手（估）']
   ]);
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '适用税率 '+ratePct+'%，速算扣除数 '+qs+' 元；个税占应发工资约 '+actualRate+'%。</div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>综合所得月度税率表（简化）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">级数</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">应纳税所得额</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">税率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">速算扣除</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≤3000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">0</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">2</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3000-12000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">210</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">3</td><td style="border:1px solid #d1d5db;padding:5px 8px;">12000-25000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">20%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1410</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">4</td><td style="border:1px solid #d1d5db;padding:5px 8px;">25000-35000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">25%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2660</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">5</td><td style="border:1px solid #d1d5db;padding:5px 8px;">35000-55000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30%</td><td style="border:1px solid #d1d5db;padding:5px 8px;">4410</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '实际采用累计预扣法（按年累计应纳税所得额逐月预扣），本工具按月估算仅供参考，以税务申报为准。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "起征点 5000 元/月，五险一金与专项附加可税前扣除",
   "专项附加：子女教育 2000/月、房贷利息 1000/月、房租 800-1500/月等",
   "实际个税按全年累计预扣，本结果按月估算",
   "结果仅供参考，正式计算以税务部门核定为准",
 ],
},

{
 "slug":"credit-card-grace-period","industry":"finance","cat":"calculator","icon":"💳","bg":"#dbeafe",
 "accent":"#3B82F6","indicon":"💰",
 "title":"信用卡免息期计算器",
 "h1":"信用卡免息期计算器",
 "h2":"💳 信用卡免息期计算器",
 "desc":"信用卡免息期计算器 - 输入账单日与还款日，计算最长/最短免息期与最佳消费日期。纯前端本地处理。",
 "intro":"免息期越长越划算。输入信用卡账单日与还款日，计算最长/最短免息期，并找出最佳消费日期。",
 "inputs":[
   {"id":"bill","label":"账单日（每月几号）","type":"select","options":[["1","1日"],["3","3日"],["5","5日"],["8","8日"],["10","10日"],["12","12日"],["15","15日"],["18","18日"],["20","20日"],["25","25日"]],"value":"10"},
   {"id":"due","label":"还款日（每月几号）","type":"select","options":[["3","3日"],["5","5日"],["8","8日"],["10","10日"],["15","15日"],["18","18日"],["20","20日"],["23","23日"],["25","25日"],["28","28日"]],"value":"25"},
   {"id":"amt","label":"计划消费金额（元）","value":"10000","step":"100","min":"0"},
   {"id":"yield","label":"资金年化收益（%）","value":"2.0","step":"0.1","min":"0","max":"10"},
 ],
 "calc":r"""
   const bill=parseInt(document.getElementById('bill').value)||10;
   const due=parseInt(document.getElementById('due').value)||25;
   const amt=num('amt'), yld=num('yield')/100;
   if(bill<1||bill>28||due<1||due>28){ToolBox.setResult('result','<p class="tip-error">请输入有效的账单日与还款日。</p>');return;}
   // 最长免息期：账单日次日消费 → 下期还款日
   let maxGrace;
   if(due>bill){ maxGrace=(due-bill-1)+30; } // 消费于 bill+1，本期账单日 bill+1 天后到期还款日 due
   else { maxGrace=(due+30-bill-1)+30; }
   // 简化：最长免息期 = 账单日次日 → 下下期还款日 的天数
   // 账单日次日消费，本期账单（bill+1 后）计入下下期？——按行业惯例：账单日次日消费享受最长免息期
   // 计算：bill 日消费 → 本账单周期（30 天）→ 到期还款日 due（若 due>bill 则当月，否则次月）
   const graceForBillDay = due>bill ? (due-bill) : (30-bill+due); // 账单日当天消费
   const bestGrace = due>bill ? (due-bill-1)+30+1 : (30-bill+due-1)+30+1; // 账单日次日消费→下下期还款
   const minGrace = 0; // 还款日当天消费最短（≈0）
   const bestDate = bill===31?1:(bill%28)+1; // 最佳消费日 = 账单日次日
   // 免息期理财价值：大额消费若延后还款，资金可放货币基金吃息
   const interestBest = amt*yld/365*maxGrace;
   const interestBill = amt*yld/365*graceForBillDay;
   const gap = interestBest-interestBill;
   let html=dataGrid([
     [maxGrace+' 天','最长免息期（账单日次日消费）'],
     [graceForBillDay+' 天','账单日当天消费免息期'],
     [bestDate+' 日','最佳消费日（账单日次日）'],
     ['≈0 天','最短免息期（还款日当天消费）'],
     ['¥'+interestBest.toFixed(2),'最长免息期资金收益（'+yld*100+'%年化）'],
     ['¥'+gap.toFixed(2),'账单日次日 vs 当天消费收益差']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>免息期示意</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">消费日期</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">入账账单</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">最迟还款日</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">免息期约</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+(bill+1<=28?bill+1:'1')+' 日</td><td style="border:1px solid #d1d5db;padding:5px 8px;">下期账单</td><td style="border:1px solid #d1d5db;padding:5px 8px;">下下期 '+due+' 日</td><td style="border:1px solid #d1d5db;padding:5px 8px;">'+maxGrace+' 天</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+bill+' 日</td><td style="border:1px solid #d1d5db;padding:5px 8px;">本期账单</td><td style="border:1px solid #d1d5db;padding:5px 8px;">'+due+' 日'+(due<=bill?'（次月）':'')+'</td><td style="border:1px solid #d1d5db;padding:5px 8px;">'+graceForBillDay+' 天</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '大额消费安排在账单日次日最划算；取现与分期无免息期。'+
     '若将 ¥'+fmtMoney(amt)+' 延后 '+maxGrace+' 天还款并按 '+yld*100+'% 年化理财，可多赚约 ¥'+interestBest.toFixed(2)+'（需确保还款日按时还清，否则利息远超收益）。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "最长免息期 = 账单日次日消费至下下期还款日",
   "大额消费建议集中在账单日次日",
   "取现、转账、分期交易不享受免息期",
   "逾期还款会产生利息并影响征信，请按时还款",
 ],
},
{
 "slug":"points-redemption-value","industry":"finance","cat":"calculator","icon":"🎁","bg":"#fefce8",
 "accent":"#EAB308","indicon":"💰",
 "title":"积分兑换价值计算器",
 "h1":"积分兑换价值计算器",
 "h2":"🎁 积分兑换价值计算器",
 "desc":"积分兑换价值计算器 - 输入积分数与兑换品价值，计算每万分兑换价值并评估是否划算。纯前端本地处理。",
 "intro":"积分值不值钱？输入积分数与兑换商品的现金价值，算出每万分价值，对比常见兑换渠道判断划算与否。",
 "inputs":[
   {"id":"pts","label":"积分数（分）","value":"10000","step":"100","min":"1"},
   {"id":"val","label":"兑换品现金价值（元）","value":"20","step":"1","min":"0"},
   {"id":"fee","label":"是否需加钱换购（元）","value":"0","step":"1","min":"0"},
 ],
 "calc":r"""
   const pts=num('pts'), val=num('val'), fee=num('fee');
   if(pts<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的积分数。</p>');return;}
   const netVal=val-fee;
   const per10k=netVal/pts*10000;
   const per100=netVal/pts*100;
   const level=per10k>=30?'很划算':(per10k>=15?'较划算':(per10k>=5?'一般':'偏亏'));
   let html=dataGrid([
     [fmtMoney(per10k),'每万分兑换价值（元）'],
     [fmtMoney(per100),'每 100 分兑换价值（元）'],
     [level,'划算程度'],
     [fmtMoney(netVal),'净得价值（扣除加钱）'],
     [fmtMoney(fee),'需加钱换购（元）']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见积分价值参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">渠道</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">每万分约值</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">说明</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">现金抵扣</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5-10 元</td><td style="border:1px solid #d1d5db;padding:5px 8px;">积分当钱花，最常见</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">兑换实物/电子券</td><td style="border:1px solid #d1d5db;padding:5px 8px;">15-30 元</td><td style="border:1px solid #d1d5db;padding:5px 8px;">大促时价值更高</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">兑换里程</td><td style="border:1px solid #d1d5db;padding:5px 8px;">30-60 元</td><td style="border:1px solid #d1d5db;padding:5px 8px;">需凑整兑换，门槛高</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">抽奖</td><td style="border:1px solid #d1d5db;padding:5px 8px;">不确定</td><td style="border:1px solid #d1d5db;padding:5px 8px;">期望值通常低于直接兑换</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '积分一般有有效期，建议优先兑换现金抵扣或高价值实物；单次兑换价值与商品实际售价、平台补贴有关。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "每万分价值 = (兑换品价值-加钱) ÷ 积分数 × 10000",
   "现金抵扣常见 5-10 元/万分，实物兑换 15-30 元/万分",
   "里程兑换价值高但有凑整门槛",
   "积分有有效期，别攒到过期",
 ],
},
{
 "slug":"wedding-banquet","industry":"fun","cat":"calculator","icon":"🎎","bg":"#fce7f3",
 "accent":"#EC4899","indicon":"🎮",
 "title":"婚宴桌数估算器",
 "h1":"婚宴桌数估算器",
 "h2":"🎎 婚宴桌数估算器",
 "desc":"婚宴桌数估算器 - 按宾客人数、桌型与每桌人数估算婚宴桌数、备桌建议与场地参考。纯前端本地处理。",
 "intro":"婚宴订几桌？输入宾客人数与桌型，自动估算主桌数与备桌建议，并给出常见场地容纳参考。",
 "inputs":[
   {"id":"guests","label":"宾客人数（人）","value":"120","step":"1","min":"1"},
   {"id":"type","label":"桌型","type":"select","options":[["round10","圆桌 10 人"],["round12","圆桌 12 人"],["square8","方桌 8 人"],["square10","方桌 10 人"]],"value":"round10"},
   {"id":"backup","label":"备桌策略","type":"select","options":[["none","不备桌"],["small","备 1 桌（≤200 人）"],["mid","备 2 桌（201-400 人）"],["big","备 3 桌（>400 人）"]],"value":"small"},
 ],
 "calc":r"""
   const guests=Math.floor(num('guests')), type=document.getElementById('type').value, backup=document.getElementById('backup').value;
   if(guests<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的宾客人数。</p>');return;}
   const perTable={round10:10,round12:12,square8:8,square10:10}[type]||10;
   const typeName={round10:'圆桌 10 人',round12:'圆桌 12 人',square8:'方桌 8 人',square10:'方桌 10 人'}[type]||'圆桌 10 人';
   const mainTables=Math.ceil(guests/perTable);
   // 备桌按满员率 90% 估算实际到场，预留 10% 弹性
   const expect=Math.ceil(guests*0.9);
   const expectTables=Math.ceil(expect/perTable);
   let backupN=0;
   if(backup==='small') backupN=1; else if(backup==='mid') backupN=2; else if(backup==='big') backupN=3;
   const totalTables=mainTables+backupN;
   const costRef=mainTables*1500; // 参考：普通酒店 1500/桌
   const costMid=mainTables*3000; // 中档 3000/桌
   let html=dataGrid([
     [mainTables+' 桌','主桌数（'+typeName+'）'],
     [backupN+' 桌','备桌'],
     [totalTables+' 桌','合计预订桌数'],
     ['约 '+expect+' 人','按 90% 到场率估算'],
     ['¥'+fmtMoney(costRef)+' 起','场地费参考（1500/桌）'],
     ['¥'+fmtMoney(costMid)+' 起','中档场地（3000/桌）']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>婚宴场地容纳参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">场地</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">可容纳</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适合桌数</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">中小型宴会厅</td><td style="border:1px solid #d1d5db;padding:5px 8px;">100-200 人</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10-20 桌</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">大型宴会厅</td><td style="border:1px solid #d1d5db;padding:5px 8px;">200-400 人</td><td style="border:1px solid #d1d5db;padding:5px 8px;">20-40 桌</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">酒店多功能厅</td><td style="border:1px solid #d1d5db;padding:5px 8px;">400-800 人</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40-80 桌</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '实际订桌建议按宾客确认到场数 +10% 弹性；桌数越多可谈折扣。费用为常见参考区间，以当地酒店报价为准。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "主桌数 = 宾客人数 ÷ 每桌人数（向上取整）",
   "备桌策略：1 桌（≤200人）/2 桌（201-400）/3 桌（>400）",
   "场地费参考：普通 1500/桌，中档 3000/桌",
   "订桌按到场数 +10% 弹性，具体以酒店报价为准",
 ],
},
{
 "slug":"balcony-sunlight","industry":"gardening","cat":"calculator","icon":"🌱","bg":"#dcfce7",
 "accent":"#22C55E","indicon":"🌿",
 "title":"阳台养花光照评估器",
 "h1":"阳台养花光照评估器",
 "h2":"🌱 阳台养花光照评估器",
 "desc":"阳台养花光照评估器 - 按阳台朝向、楼层与季节估算每日直射光照时长，推荐适合的植物类型。纯前端本地处理。",
 "intro":"你家阳台适合养什么花？输入朝向、楼层与季节，估算每日直射光照时长，推荐适宜植物与养护提示。",
 "inputs":[
   {"id":"dir","label":"阳台朝向","type":"select","options":[["south","南向"],["east","东向"],["west","西向"],["north","北向"]],"value":"south"},
   {"id":"floor","label":"楼层","type":"select","options":[["low","低层（1-3 层）"],["mid","中层（4-9 层）"],["high","高层（10 层+）"]],"value":"mid"},
   {"id":"season","label":"季节","type":"select","options":[["spring","春"],["summer","夏"],["autumn","秋"],["winter","冬"]],"value":"spring"},
 ],
 "calc":r"""
   const dir=document.getElementById('dir').value||'south', floor=document.getElementById('floor').value||'mid', season=document.getElementById('season').value||'spring';
   // 基准直射光照（小时/天）按朝向×季节（含兜底）
   const sunTab={south:{spring:6,summer:8,autumn:6,winter:4},east:{spring:4,summer:5,autumn:3.5,winter:3},west:{spring:4,summer:6,autumn:4,winter:2.5},north:{spring:1.5,summer:2,autumn:1,winter:0.5}};
   const sun=(sunTab[dir]||sunTab.south)[season]||4;
   // 楼层修正：低层遮挡 -1h，高层 +0.5h
   const floorAdj={low:-1,mid:0,high:0.5}[floor]||0;
   const hours=Math.max(0.5,sun+floorAdj);
   const dirName={south:'南向',east:'东向',west:'西向',north:'北向'}[dir]||'南向';
   const seasonName={spring:'春',summer:'夏',autumn:'秋',winter:'冬'}[season]||'春';
   // 植物推荐
   let rec='', type='';
   if(hours>=6){ type='全日照'; rec='月季、茉莉、三角梅、蓝雪花、多肉、向日葵'; }
   else if(hours>=4){ type='半日照'; rec='长寿花、天竺葵、绣球（遮午）、薄荷、矮牵牛'; }
   else if(hours>=2){ type='散射光'; rec='绿萝、吊兰、龟背竹、发财树、文竹、常春藤'; }
   else { type='耐阴'; rec='虎皮兰、一叶兰、蕨类、竹芋、白掌'; }
   let html=dataGrid([
     [hours.toFixed(1)+' 小时','每日直射光照（'+dirName+'·'+seasonName+'）'],
     [type,'光照类型'],
     [rec,'推荐植物'],
     [dirName+' · '+seasonName,'朝向 · 季节']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>朝向光照特点</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">朝向</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">光照特点</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适宜植物</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">南向</td><td style="border:1px solid #d1d5db;padding:5px 8px;">全日照，最充足</td><td style="border:1px solid #d1d5db;padding:5px 8px;">月季/茉莉/多肉</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">东向</td><td style="border:1px solid #d1d5db;padding:5px 8px;">上午直射，温和</td><td style="border:1px solid #d1d5db;padding:5px 8px;">绣球/天竺葵</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">西向</td><td style="border:1px solid #d1d5db;padding:5px 8px;">下午暴晒，较热</td><td style="border:1px solid #d1d5db;padding:5px 8px;">三角梅/耐热植物</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">北向</td><td style="border:1px solid #d1d5db;padding:5px 8px;">散射光为主</td><td style="border:1px solid #d1d5db;padding:5px 8px;">绿萝/蕨类/虎皮兰</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '西向阳台夏季注意遮阴防灼伤；楼层越低光照越弱（参考值 ±1 小时）。结果供选花参考。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "直射光照：南向 4-8h / 东向 3-5h / 西向 2.5-6h / 北向 0.5-2h（按季节）",
   "楼层修正：低层 -1h、高层 +0.5h",
   "全日照≥6h、半日照 4-6h、散射光 2-4h、耐阴<2h",
   "西向夏季注意遮阴，结果供选花参考",
 ],
},
{
 "slug":"desk-dimensions","industry":"furniture","cat":"calculator","icon":"🪑","bg":"#ffedd5",
 "accent":"#F97316","indicon":"🛋️",
 "title":"书桌尺寸规划计算器",
 "h1":"书桌尺寸规划计算器",
 "h2":"🪑 书桌尺寸规划计算器",
 "desc":"书桌尺寸规划计算器 - 按身高与使用场景推荐桌高、椅高、屏幕高度与桌面深度（人体工学）。纯前端本地处理。",
 "intro":"桌椅多高才舒服？按身高与使用场景，按人体工学比例推荐桌高、椅高、屏幕中心高度与桌面深度。",
 "inputs":[
   {"id":"height","label":"身高（cm）","value":"170","step":"1","min":"120","max":"210"},
   {"id":"scene","label":"使用场景","type":"select","options":[["computer","电脑办公"],["write","书写阅读"],["standing","站立办公"]],"value":"computer"},
   {"id":"mon","label":"显示器尺寸（英寸）","value":"24","step":"1","min":"13","max":"49"},
 ],
 "calc":r"""
   const h=num('height'), scene=document.getElementById('scene').value||'computer', mon=num('mon');
   if(h<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的身高。</p>');return;}
   // 人体工学经验比例
   let deskH, chairH, screenH, depth;
   if(scene==='standing'){
     deskH=h*0.62; chairH=0; screenH=h*0.95; depth=60;
   } else {
     deskH=h*0.46;         // 桌面高度 ≈ 身高×0.46（坐姿）
     chairH=h*0.26;        // 椅面高度 ≈ 身高×0.26
     screenH=h*0.71;       // 屏幕中心高度
     depth=(scene==='computer')?70:60;
   }
   // 推荐视距：显示器对角线 × 1.5~2
   const viewDistMin=mon*2.54*1.5, viewDistMax=mon*2.54*2.0;
   const sceneName={computer:'电脑办公',write:'书写阅读',standing:'站立办公'}[scene]||'电脑办公';
   const chairNote=chairH>0?'椅面高约 '+chairH.toFixed(0)+' cm，建议选可调升降款':'站立办公建议配抗疲劳垫';
   let html=dataGrid([
     [deskH.toFixed(0)+' cm','桌面高度（'+sceneName+'）'],
     [chairH>0?chairH.toFixed(0)+' cm':'—','椅面高度'],
     [screenH.toFixed(0)+' cm','屏幕中心高度'],
     [depth+' cm','建议桌面深度'],
     [Math.round(viewDistMin)+'~'+Math.round(viewDistMax)+' cm','推荐视距（'+mon+' 英寸屏）']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>常见身高参考（电脑办公）</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">身高</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">桌高</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">椅高</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">屏幕中心</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">160 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">74 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">42 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">114 cm</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">170 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">78 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">44 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">121 cm</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">180 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">83 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">47 cm</td><td style="border:1px solid #d1d5db;padding:5px 8px;">128 cm</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     chairNote+'。手肘自然下垂约 90°，眼睛平视屏幕上沿，腰部有支撑为舒适标准。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "桌高≈身高×0.46、椅高≈身高×0.26（坐姿）",
   "站立办公桌高≈身高×0.62",
   "电脑办公桌面深度建议 ≥70cm，书写 60cm",
   "标准：手肘 90°、平视屏幕上沿、腰部有支撑",
 ],
},
{
 "slug":"cable-tray-sizing","industry":"cable","cat":"calculator","icon":"🔌","bg":"#fef2f2",
 "accent":"#EF4444","indicon":"🔗",
 "title":"电缆桥架尺寸计算器",
 "h1":"电缆桥架尺寸计算器",
 "h2":"🔌 电缆桥架尺寸计算器",
 "desc":"电缆桥架尺寸计算器 - 按电缆外径与数量估算桥架所需宽高，校验填充率是否合规。纯前端本地处理。",
 "intro":"桥架选多大？输入电缆外径与根数，自动估算桥架宽高，并按常见填充率标准校验是否合适。",
 "inputs":[
   {"id":"od","label":"电缆外径（mm）","value":"20","step":"1","min":"3","max":"200"},
   {"id":"cnt","label":"电缆根数","value":"10","step":"1","min":"1","max":"500"},
   {"id":"fill","label":"填充率标准","type":"select","options":[["40","40%（电力回路）"],["50","50%（控制回路）"],["60","60%（备用扩容）"]],"value":"40"},
 ],
 "calc":r"""
   const od=num('od'), cnt=Math.floor(num('cnt')), fill=parseInt(document.getElementById('fill').value)||40;
   if(od<=0||cnt<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的电缆外径与根数。</p>');return;}
   const areaOne=Math.PI*od*od/4;
   const totalArea=areaOne*cnt;
   const needArea=totalArea/(fill/100);
   // 桥架常用规格（宽×高 mm）：取满足面积的最小规格
   const specs=[[100,50],[100,100],[150,75],[150,100],[200,100],[300,100],[300,150],[400,100],[400,200],[600,200]];
   let chosen=specs[specs.length-1];
   for(let i=0;i<specs.length;i++){
     if(specs[i][0]*specs[i][1]>=needArea){ chosen=specs[i]; break; }
   }
   const useRate=(totalArea/(chosen[0]*chosen[1])*100).toFixed(1);
   const fillName={40:'40%',50:'50%',60:'60%'}[fill]||'40%';
   let html=dataGrid([
     [totalArea.toFixed(0)+' mm²','电缆总截面积'],
     [needArea.toFixed(0)+' mm²','所需桥架面积（填充率 '+fillName+'）'],
     [chosen[0]+'×'+chosen[1]+' mm','推荐桥架规格（宽×高）'],
     [useRate+'%','实际填充率']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>常用桥架规格表</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">规格（宽×高 mm）</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">截面积（mm²）</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适用</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">100×50</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">少量照明回路</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">100×100</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">小型配电</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">200×100</td><td style="border:1px solid #d1d5db;padding:5px 8px;">20000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">常规动力回路</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">300×150</td><td style="border:1px solid #d1d5db;padding:5px 8px;">45000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">多回路主干</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">400×200</td><td style="border:1px solid #d1d5db;padding:5px 8px;">80000</td><td style="border:1px solid #d1d5db;padding:5px 8px;">大型主干</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '电力回路填充率建议 ≤40%，控制回路 ≤50%；多层桥架需复核层间散热。正式设计按 GB/T 29415 与现场校核。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "桥架面积 = 电缆截面积之和 ÷ 填充率",
   "填充率：电力 40%、控制 50%、扩容预留 60%",
   "选满足面积的最小标准规格",
   "正式设计按 GB/T 29415 与散热校核执行",
 ],
},
{
 "slug":"markdown-to-html","industry":"it","cat":"convert","icon":"📝","bg":"#f0fdf4",
 "accent":"#16A34A","indicon":"💻",
 "title":"Markdown 转 HTML",
 "h1":"Markdown 转 HTML",
 "h2":"📝 Markdown 转 HTML",
 "desc":"Markdown 转 HTML - 粘贴 Markdown 文本，实时转换为 HTML 代码，支持标题/粗斜体/链接/列表/代码块/表格。纯前端本地处理。",
 "intro":"把 Markdown 变成 HTML：粘贴 Markdown 源码，右侧实时预览转换结果与 HTML 代码，支持常用语法。",
 "inputs":[
   {"id":"md","label":"Markdown 文本","type":"textarea","value":"# 标题\n\n**加粗** 与 *斜体*，[链接](https://example.com)\n\n- 列表项一\n- 列表项二\n\n```js\nconsole.log('hello');\n```\n\n| 列一 | 列二 |\n|---|---|\n| A | B |"},
   {"id":"showcode","label":"显示 HTML 代码","type":"select","options":[["1","显示"],["0","仅预览"]],"value":"1"},
   {"id":"compact","label":"输出模式","type":"select","options":[["compact","紧凑（无多余空白）"],["pretty","宽松（段落间空行）"]],"value":"compact"},
 ],
 "calc":r"""
   const md=document.getElementById('md').value||'';
   if(!md.trim()){ToolBox.setResult('result','<p class="tip-error">请输入 Markdown 文本。</p>');return;}
   // 轻量 Markdown 解析（标题/粗斜/链接/行内代码/列表/代码块/表格/引用/分割线）
   let s=md.replace(/\r\n/g,'\n');
   const esc=function(x){return String(x==null?'':x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');};
   // 代码块（```lang ... ```）先保护
   const blocks=[];
   s=s.replace(/```[a-zA-Z]*\n([\s\S]*?)```/g,function(m,code){
     blocks.push('<pre><code>'+esc(code)+'</code></pre>');
     return '\x00BLOCK'+(blocks.length-1)+'\x00';
   });
   const lines=s.split('\n');
   let html='';
   let inList=false, inTable=false, tableRows=[];
   const closeList=function(){ if(inList){ html+='</ul>'; inList=false; } };
   const closeTable=function(){ if(inTable){ html+='</table>'; inTable=false; } };
   const inline=function(t){
     t=esc(t);
     t=t.replace(/`([^`]+)`/g,'<code>$1</code>');
     t=t.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
     t=t.replace(/\*([^*]+)\*/g,'<em>$1</em>');
     t=t.replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
     return t;
   };
   for(let i=0;i<lines.length;i++){
     let line=lines[i];
     const blk=line.match(/^\x00BLOCK(\d+)\x00$/);
     if(blk){ closeList(); closeTable(); html+=blocks[parseInt(blk[1])]; continue; }
     if(/^\s*$/.test(line)){ closeList(); closeTable(); continue; }
     const hm=line.match(/^(#{1,6})\s+(.*)$/);
     if(hm){ closeList(); closeTable(); const lv=hm[1].length; html+='<h'+lv+'>'+inline(hm[2])+'</h'+lv+'>'; continue; }
     if(/^---+$/.test(line)){ closeList(); closeTable(); html+='<hr>'; continue; }
     const qm=line.match(/^>\s?(.*)$/);
     if(qm){ closeList(); closeTable(); html+='<blockquote>'+inline(qm[1])+'</blockquote>'; continue; }
     const lm=line.match(/^[-*+]\s+(.*)$/);
     if(lm){ if(!inList){ html+='<ul>'; inList=true; } html+='<li>'+inline(lm[1])+'</li>'; continue; }
     // 表格：行以 | 开头且下一行是分隔
     if(line.indexOf('|')===0 && /^\|[\s:-]+\|/.test(lines[i+1]||'')){
       closeList();
       const header=line.replace(/^\||\|$/g,'').split('|').map(function(x){return x.trim();});
       i++; // 跳过分隔行
       tableRows=[];
       while(i+1<lines.length && lines[i+1].indexOf('|')===0){
         i++;
         tableRows.push(lines[i].replace(/^\||\|$/g,'').split('|').map(function(x){return x.trim();}));
       }
       if(!inTable){ html+='<table class="csv-prev" style="border-collapse:collapse;width:100%;font-size:12.5px;">'; inTable=true; }
       html+='<tr>'+header.map(function(h){return '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">'+inline(h)+'</th>';}).join('')+'</tr>';
       for(let r=0;r<tableRows.length;r++){
         html+='<tr>'+tableRows[r].map(function(c){return '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+inline(c)+'</td>';}).join('')+'</tr>';
       }
       continue;
     }
     closeList(); closeTable();
     html+='<p>'+inline(line)+'</p>';
   }
   closeList(); closeTable();
   const showCode=document.getElementById('showcode').value==='1';
   const compact=document.getElementById('compact').value==='compact';
   let outHtml=html;
   if(compact){ outHtml=outHtml.replace(/>\s+</g,'><'); }
   if(showCode){
     html += '<div style="margin-top:12px;font-size:13px;"><b>HTML 代码</b></div>'+
       '<pre style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;font-size:12px;overflow-x:auto;max-height:260px;white-space:pre-wrap;word-break:break-all;">'+esc(outHtml)+'</pre>';
   }
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '支持标题/粗斜体/链接/行内代码/列表/代码块/引用/表格/分割线。生成结果可复制到任意 HTML 页面。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "支持：#1-6 标题、**粗体**、*斜体*、`行内代码`",
   "支持：- 无序列表、数字列表、> 引用、--- 分割线",
   "支持：``` 代码块、| 表格、[链接](url)",
   "转换纯本地进行，文本不会上传",
 ],
},
{
 "slug":"regex-common","industry":"it","cat":"reference","icon":"🔍","bg":"#eff6ff",
 "accent":"#3B82F6","indicon":"💻",
 "title":"常用正则表达式速查",
 "h1":"常用正则表达式速查",
 "h2":"🔍 常用正则表达式速查",
 "desc":"常用正则表达式速查 - 邮箱/手机号/身份证/URL/IP 等常用正则库，支持实时测试匹配结果。纯前端本地处理。",
 "intro":"写正则没头绪？内置邮箱、手机号、身份证、URL、IP 等高频正则，一键测试目标文本匹配结果。",
 "inputs":[
   {"id":"cat","label":"正则类别","type":"select","options":[["email","邮箱地址"],["phone","中国大陆手机号"],["idcard","身份证号"],["url","URL 链接"],["ipv4","IPv4 地址"],["date","日期 YYYY-MM-DD"],["chinese","中文字符"],["username","用户名(字母数字_3-16)"]],"value":"email"},
   {"id":"txt","label":"测试文本","type":"textarea","value":"abc@example.com 13812345678 test@mail.cn 10.0.0.1"},
   {"id":"limit","label":"显示匹配数量上限","value":"8","step":"1","min":"1","max":"50"},
 ],
 "calc":r"""
   const cat=document.getElementById('cat').value||'email', txt=document.getElementById('txt').value||'';
   const lim=Math.max(1,Math.floor(num('limit')));
   const regs={
     email:/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
     phone:/1[3-9]\d{9}/g,
     idcard:/\d{17}[\dXx]/g,
     url:/https?:\/\/[^\s<>"']+/g,
     ipv4:/(?:\d{1,3}\.){3}\d{1,3}/g,
     date:/\d{4}-\d{2}-\d{2}/g,
     chinese:/[\u4e00-\u9fff]+/g,
     username:/[A-Za-z0-9_]{3,16}/g,
   };
   const names={email:'邮箱地址',phone:'中国大陆手机号',idcard:'身份证号',url:'URL 链接',ipv4:'IPv4 地址',date:'日期 YYYY-MM-DD',chinese:'中文字符',username:'用户名(字母数字_3-16)'};
   const re=regs[cat]||regs.email;
   const found=txt.match(re)||[];
   const name=names[cat]||'';
   let html=dataGrid([
     [name,'正则类别'],
     [found.length+' 个','匹配数量'],
     [found.length?found.slice(0,lim).join('、'):'无匹配','匹配结果（前 '+lim+' 个）']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>常用正则速查表</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">类别</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">正则</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">邮箱</td><td style="border:1px solid #d1d5db;padding:5px 8px;">[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">手机号</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1[3-9]\\d{9}</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">身份证</td><td style="border:1px solid #d1d5db;padding:5px 8px;">\\d{17}[\\dXx]</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">IPv4</td><td style="border:1px solid #d1d5db;padding:5px 8px;">(?:\\d{1,3}\\.){3}\\d{1,3}</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">日期</td><td style="border:1px solid #d1d5db;padding:5px 8px;">\\d{4}-\\d{2}-\\d{2}</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">中文字符</td><td style="border:1px solid #d1d5db;padding:5px 8px;">[\\u4e00-\\u9fff]+</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '正则基于常见实践整理，具体场景请按需调整（如手机号已覆盖 13-19 号段）。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "内置 8 类高频正则：邮箱/手机/身份证/URL/IPv4/日期/中文/用户名",
   "测试文本可输入多行，匹配结果实时展示前 8 个",
   "正则按常见实践整理，正式校验请按业务规则调整",
   "纯本地运行，文本不会上传",
 ],
},
{
 "slug":"css-grid-generator","industry":"design","cat":"generate","icon":"🧱","bg":"#fdf4ff",
 "accent":"#C026D3","indicon":"🎨",
 "title":"CSS 栅格布局生成器",
 "h1":"CSS 栅格布局生成器",
 "h2":"🧱 CSS 栅格布局生成器",
 "desc":"CSS 栅格布局生成器 - 设置列数/间距/断点，生成 CSS Grid 布局代码并实时预览。纯前端本地处理。",
 "intro":"快速生成 CSS Grid 布局：设置列数、列宽方式、间距与断点，一键复制生成的 CSS 与 HTML 代码。",
 "inputs":[
   {"id":"cols","label":"列数","value":"3","step":"1","min":"1","max":"12"},
   {"id":"gap","label":"间距（px）","value":"16","step":"1","min":"0","max":"80"},
   {"id":"coltype","label":"列宽方式","type":"select","options":[["fr","等分（1fr）"],["fixed","固定宽度（120px）"],["auto","自适应（auto）"]],"value":"fr"},
   {"id":"containerW","label":"容器宽度（px）","value":"960","step":"10","min":"320","max":"1920"},
 ],
 "calc":r"""
   const cols=Math.floor(num('cols')), gap=num('gap'), ct=document.getElementById('coltype').value||'fr', cw=num('containerW');
   if(cols<1||cols>12){ToolBox.setResult('result','<p class="tip-error">列数需在 1-12 之间。</p>');return;}
   let colTpl;
   if(ct==='fixed') colTpl='repeat('+cols+', 120px)';
   else if(ct==='auto') colTpl='repeat('+cols+', auto)';
   else colTpl='repeat('+cols+', 1fr)';
   const css='.grid {\n  display: grid;\n  grid-template-columns: '+colTpl+';\n  gap: '+gap+'px;\n  max-width: '+cw+'px;\n  margin: 0 auto;\n  padding: 0 '+(gap/2)+'px;\n}\n\n.grid > * {\n  min-width: 0;\n}';
   const htmlCode='<div class="grid">\n  <!-- 每列一个子元素 -->\n  <div>1</div>\n  <div>2</div>\n  <div>'+cols+'</div>\n</div>';
   // 预览
   const colColor=function(i){return 'hsl('+((i*137)%360)+',70%,60%)';};
   let preview='<div style="display:grid;grid-template-columns:'+colTpl+';gap:'+gap+'px;max-width:'+cw+'px;margin:0 auto;">';
   for(let i=1;i<=cols;i++){
     preview+='<div style="background:'+colColor(i)+';border-radius:8px;min-height:56px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;font-weight:600;">'+i+'</div>';
   }
   preview+='</div>';
   let html=dataGrid([
     [cols+' 列','列数'],
     [gap+' px','间距'],
     [colTpl,'grid-template-columns'],
     [cw+' px','容器宽度']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>实时预览</b></div>'+
     '<div style="margin-top:6px;border:1px dashed #e2e8f0;border-radius:10px;padding:12px;background:#f8fafc;">'+preview+'</div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>CSS 代码</b></div>'+
     '<pre style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;font-size:12px;overflow-x:auto;">'+css.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</pre>';
   html += '<div style="margin-top:8px;font-size:13px;"><b>HTML 结构</b></div>'+
     '<pre style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;font-size:12px;overflow-x:auto;">'+htmlCode.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</pre>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '配合响应式断点（如 @media max-width:768px 改 1 列）即可适配移动端。生成代码可直接使用。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "支持等分 1fr / 固定 120px / 自适应 auto 三种列宽",
   "列数 1-12，间距 0-80px，容器宽可调",
   "预览实时渲染，代码可直接复制",
   "移动端建议断点处改单列布局",
 ],
},
{
 "slug":"breakpoint-queries","industry":"design","cat":"generate","icon":"📱","bg":"#f5f3ff",
 "accent":"#7C3AED","indicon":"🎨",
 "title":"响应式断点生成器",
 "h1":"响应式断点生成器",
 "h2":"📱 响应式断点生成器",
 "desc":"响应式断点生成器 - 选择目标设备，自动生成移动优先的媒体查询 CSS 代码。纯前端本地处理。",
 "intro":"响应式怎么做？选择需要适配的设备档位，自动生成移动优先（min-width）的媒体查询代码。",
 "inputs":[
   {"id":"devs","label":"适配设备","type":"select","options":[["basic","手机+平板+桌面"],["all","手机+平板+笔记本+大屏"],["custom","常用四档断点"]],"value":"basic"},
   {"id":"mode","label":"查询方式","type":"select","options":[["min","移动优先（min-width）"],["max","桌面优先（max-width）"]],"value":"min"},
   {"id":"cls","label":"目标类名","value":".example","type":"text"},
 ],
 "calc":r"""
   const devs=document.getElementById('devs').value||'basic', mode=document.getElementById('mode').value||'min';
   const cls=(document.getElementById('cls').value||'.example').trim()||'.example';
   // 断点定义
   const bp={
     basic:[['sm','手机（<640px）',640],['md','平板（≥768px）',768],['lg','桌面（≥1024px）',1024]],
     all:[['sm','手机（<640px）',640],['md','平板（≥768px）',768],['lg','笔记本（≥1024px）',1024],['xl','大屏（≥1280px）',1280]],
     custom:[['xs','小屏（<480px）',480],['sm','手机（≥576px）',576],['md','平板（≥768px）',768],['lg','桌面（≥992px）',992],['xl','大屏（≥1200px）',1200]],
   };
   const list=bp[devs]||bp.basic;
   let css='/* '+mode==='min'?'移动优先（Mobile First）':'桌面优先'+' */\n';
   for(let i=0;i<list.length;i++){
     if(mode==='min'){
       css+='@media (min-width: '+list[i][2]+'px) {\n  /* '+list[i][1]+' */\n  '+cls+' { /* styles */ }\n}\n\n';
     } else {
       css+='@media (max-width: '+(list[i][2]-1)+'px) {\n  /* '+list[i][1]+' */\n  '+cls+' { /* styles */ }\n}\n\n';
     }
   }
   // 预览条
   let bars='';
   for(let i=0;i<list.length;i++){
     const w=list[i][2];
     bars+='<div style="background:#ede9fe;border:1px solid #ddd6fe;border-radius:8px;padding:8px 10px;margin-bottom:6px;font-size:12.5px;display:flex;justify-content:space-between;align-items:center;">'+
       '<span style="font-weight:600;">'+list[i][1]+'</span><span style="color:var(--text-muted);">'+(mode==='min'?'≥ '+w+'px':'< '+w+'px')+'</span></div>';
   }
   let html=dataGrid([
     [list.length+' 档','断点档位'],
     [mode==='min'?'移动优先':'桌面优先','查询方式'],
     [list.map(function(x){return x[2]+'px';}).join(' / '),'断点值']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>断点一览</b></div>'+
     '<div style="margin-top:6px;">'+bars+'</div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>媒体查询 CSS</b></div>'+
     '<pre style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;font-size:12px;overflow-x:auto;max-height:300px;">'+css.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</pre>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '移动优先建议从最小屏写起，逐步用 min-width 增强；桌面优先则相反。断点可按项目实际设备调整。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "三种档位：基础三档 / 全设备四档 / 常用五档",
   "支持移动优先（min-width）与桌面优先（max-width）",
   "生成代码含注释，可直接使用",
   "断点值按常见实践，可按项目调整",
 ],
},
{
 "slug":"phone-screen-sizes","industry":"it","cat":"reference","icon":"📱","bg":"#ecfeff",
 "accent":"#06B6D4","indicon":"💻",
 "title":"手机屏幕尺寸速查",
 "h1":"手机屏幕尺寸速查",
 "h2":"📱 手机屏幕尺寸速查",
 "desc":"手机屏幕尺寸速查 - 主流手机机型分辨率/屏幕尺寸/PPI 速查表，支持按尺寸或分辨率换算。纯前端本地处理。",
 "intro":"主流机型屏幕参数速查：分辨率、英寸、PPI 一表看完，还可按英寸与分辨率反算 PPI。",
 "inputs":[
   {"id":"diag","label":"屏幕英寸（反算 PPI 用，可留空）","value":"6.1","step":"0.1","min":"3","max":"10"},
   {"id":"resw","label":"分辨率宽（px，反算 PPI 用）","value":"2532","step":"1","min":"320","max":"5000"},
   {"id":"resh","label":"分辨率高（px，反算 PPI 用）","value":"1170","step":"1","min":"240","max":"5000"},
 ],
 "calc":r"""
   const diag=num('diag'), rw=num('resw'), rh=num('resh');
   if(diag<=0||rw<=0||rh<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的屏幕参数。</p>');return;}
   const ppi=Math.sqrt(rw*rw+rh*rh)/diag;
   // 常见机型
   const phones=[
     ['iPhone 15 Pro','6.1 英寸','2556×1179',460],
     ['iPhone 15','6.1 英寸','2556×1179',460],
     ['iPhone 14 Pro Max','6.7 英寸','2796×1290',460],
     ['iPhone SE (2022)','4.7 英寸','1334×750',326],
     ['三星 Galaxy S24','6.2 英寸','2340×1080',416],
     ['小米 14','6.36 英寸','2670×1200',460],
     ['华为 Mate 60 Pro','6.82 英寸','2720×1260',440],
     ['OPPO Find X7','6.78 英寸','2780×1264',450],
     ['vivo X100 Pro','6.78 英寸','2800×1260',452],
     ['一加 12','6.82 英寸','3168×1440',510],
   ];
   let html=dataGrid([
     [ppi.toFixed(0)+' PPI','输入参数反算 PPI'],
     [diag.toFixed(1)+' 英寸','屏幕尺寸'],
     [rw+'×'+rh,'分辨率'],
     [Math.sqrt(rw*rw+rh*rh).toFixed(0)+' px','对角线像素']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>主流机型屏幕参数速查</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">机型</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">尺寸</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">分辨率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">PPI</th></tr>';
   for(let i=0;i<phones.length;i++){
     html+='<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">'+phones[i][0]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+phones[i][1]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+phones[i][2]+'</td>'+
       '<td style="border:1px solid #d1d5db;padding:5px 8px;">'+phones[i][3]+'</td></tr>';
   }
   html+='</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     'PPI = √(宽²+高²) ÷ 英寸。数据为常见公开参数，具体以厂商规格为准。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "PPI = √(分辨率宽²+分辨率高²) ÷ 屏幕英寸",
   "内置 10 款主流机型参数速查",
   "数据为常见公开参数，以厂商规格为准",
   "反算功能可输入任意分辨率与英寸",
 ],
},
{
 "slug":"video-bitrate","industry":"it","cat":"calculator","icon":"🎬","bg":"#fee2e2",
 "accent":"#DC2626","indicon":"💻",
 "title":"视频码率计算器",
 "h1":"视频码率计算器",
 "h2":"🎬 视频码率计算器",
 "desc":"视频码率计算器 - 按分辨率/帧率/时长/码率计算视频文件大小，或按目标大小反推推荐码率。纯前端本地处理。",
 "intro":"视频文件多大？输入分辨率、帧率、时长与码率估算文件大小，或按目标文件大小反推建议码率。",
 "inputs":[
   {"id":"w","label":"分辨率宽（px）","value":"1920","step":"1","min":"240","max":"7680"},
   {"id":"h","label":"分辨率高（px）","value":"1080","step":"1","min":"160","max":"4320"},
   {"id":"fps","label":"帧率（fps）","value":"30","step":"1","min":"1","max":"120"},
   {"id":"dur","label":"时长（分钟）","value":"10","step":"1","min":"1"},
   {"id":"br","label":"码率（Mbps）","value":"8","step":"0.5","min":"0.1","max":"200"},
 ],
 "calc":r"""
   const w=num('w'), h=num('h'), fps=Math.floor(num('fps')), dur=num('dur'), br=num('br');
   if(w<=0||h<=0||dur<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的分辨率与时长。</p>');return;}
   const pixels=w*h;
   const mbps=br;
   const fileMB=mbps*1000000/8/1024/1024*dur*60;
   const gb=fileMB/1024;
   // 按分辨率推荐码率
   const rec={p480:2.5,p720:5,p1080:8,p1440:16,p2160:35};
   const px=pixels;
   let recBr;
   if(px<=854*480) recBr=rec.p480;
   else if(px<=1280*720) recBr=rec.p720;
   else if(px<=1920*1080) recBr=rec.p1080;
   else if(px<=2560*1440) recBr=rec.p1440;
   else recBr=rec.p2160;
   const recSize=recBr*1000000/8/1024/1024*dur*60;
   let html=dataGrid([
     [w+'×'+h+' @ '+fps+'fps','分辨率 / 帧率'],
     [mbps+' Mbps','当前码率'],
     [fileMB.toFixed(1)+' MB ('+gb.toFixed(2)+' GB)','文件大小'],
     [recBr+' Mbps','推荐码率（该分辨率）'],
     [recSize.toFixed(1)+' MB','推荐码率下大小']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>分辨率推荐码率参考</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">分辨率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">推荐码率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">适用场景</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">480p</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2.5 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">低带宽</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">720p</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">普通流媒体</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1080p</td><td style="border:1px solid #d1d5db;padding:5px 8px;">8 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">高清标准</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1440p</td><td style="border:1px solid #d1d5db;padding:5px 8px;">16 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2K</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">2160p</td><td style="border:1px solid #d1d5db;padding:5px 8px;">35 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">4K</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '文件大小 = 码率 × 时长 ÷ 8。H.265/HEVC 可比 H.264 省约 50% 码率；实际大小受编码器与画面复杂度影响。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "文件大小(MB) = 码率(Mbps)×1000000÷8÷1024÷1024×时长(秒)",
   "推荐码率：480p 2.5 / 720p 5 / 1080p 8 / 2K 16 / 4K 35 Mbps",
   "H.265 比 H.264 省约 50% 码率",
   "实际大小受编码器、画面复杂度影响",
 ],
},
{
 "slug":"color-contrast-check","industry":"design","cat":"validator","icon":"🎨","bg":"#f3e8ff",
 "accent":"#9333EA","indicon":"🎨",
 "title":"颜色对比度检查器",
 "h1":"颜色对比度检查器",
 "h2":"🎨 颜色对比度检查器",
 "desc":"颜色对比度检查器 - 输入前景/背景色，计算 WCAG 对比度比值并判定 AA/AAA 等级。纯前端本地处理。",
 "intro":"文字看得清吗？输入前景与背景色，按 WCAG 2.1 计算对比度比值，判定是否达到 AA/AAA 无障碍标准。",
 "inputs":[
   {"id":"fg","label":"前景色（Hex）","value":"#333333","type":"text"},
   {"id":"bg","label":"背景色（Hex）","value":"#FFFFFF","type":"text"},
   {"id":"size","label":"文字类型","type":"select","options":[["normal","正文文字（<18pt）"],["large","大号文字（≥18pt 或 14pt 加粗）"]],"value":"normal"},
 ],
 "calc":r"""
   const fg=(document.getElementById('fg').value||'#333333').trim();
   const bg=(document.getElementById('bg').value||'#FFFFFF').trim();
   const size=document.getElementById('size').value||'normal';
   const toRgb=function(hex){
     let s=hex.replace('#','');
     if(s.length===3){ s=s.split('').map(function(c){return c+c;}).join(''); }
     if(s.length!==6) return null;
     const v=parseInt(s,16);
     if(isNaN(v)) return null;
     return {r:(v>>16)&255,g:(v>>8)&255,b:v&255};
   };
   const lum=function(c){
     const f=function(v){ v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
     return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);
   };
   const fr=toRgb(fg), br=toRgb(bg);
   if(!fr||!br){ToolBox.setResult('result','<p class="tip-error">请输入有效的十六进制颜色（如 #333333）。</p>');return;}
   const l1=lum(fr), l2=lum(br);
   const ratio=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
   const r=Math.round(ratio*100)/100;
   // WCAG 2.1 阈值
   const isLarge=size==='large';
   const aa=isLarge?r>=3:r>=4.5;
   const aaa=isLarge?r>=4.5:r>=7;
   const grade=aaa?'AAA（最佳）':(aa?'AA（达标）':'未达标');
   let html=dataGrid([
     [r.toFixed(2)+':1','对比度比值'],
     [grade,'WCAG 等级'],
     [(aa?'✓':'✗')+' AA'+(isLarge?'（大文字≥3:1）':'（正文≥4.5:1）'),'AA 标准'],
     [(aaa?'✓':'✗')+' AAA'+(isLarge?'（大文字≥4.5:1）':'（正文≥7:1）'),'AAA 标准']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>预览</b></div>'+
     '<div style="margin-top:6px;border:1px solid #e2e8f0;border-radius:10px;padding:16px;text-align:center;background:'+bg+';color:'+fg+';font-size:18px;font-weight:600;">'+(aa?'示例文字 Preview Text':'示例文字（对比不足）')+'</div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>WCAG 2.1 对比度标准</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">标准</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">正文</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">大号文字</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">AA</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≥4.5:1</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≥3:1</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">AAA</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≥7:1</td><td style="border:1px solid #d1d5db;padding:5px 8px;">≥4.5:1</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '对比度 = (较亮色亮度+0.05) ÷ (较暗色亮度+0.05)，按 WCAG 2.1 相对亮度公式计算。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "对比度比值 = (亮色亮度+0.05) ÷ (暗色亮度+0.05)",
   "WCAG AA：正文≥4.5:1、大文字≥3:1；AAA：正文≥7:1、大文字≥4.5:1",
   "大号文字指 ≥18pt（24px）或 14pt 加粗（18.66px）",
   "按钮等 UI 组件非文字部分要求 ≥3:1（AA）",
 ],
},
{
 "slug":"pixel-art-generator","industry":"design","cat":"generate","icon":"🖼️","bg":"#ecfccb",
 "accent":"#65A30D","indicon":"🎨",
 "title":"像素画生成器",
 "h1":"像素画生成器",
 "h2":"🖼️ 像素画生成器",
 "desc":"像素画生成器 - 网格画布自由绘制像素画，可调网格尺寸与调色板，导出为字符画或 CSS。纯前端本地处理。",
 "intro":"画一张像素画：在网格上点击上色，调整网格大小与调色板，完成后导出为字符画或 CSS 代码。",
 "inputs":[
   {"id":"gs","label":"网格尺寸（N×N）","value":"8","step":"1","min":"4","max":"24"},
   {"id":"color","label":"当前颜色","type":"select","options":[["#EF4444","红"],["#F59E0B","橙"],["#10B981","绿"],["#3B82F6","蓝"],["#8B5CF6","紫"],["#EC4899","粉"],["#1F2937","黑"],["#F3F4F6","白"]],"value":"#EF4444"},
   {"id":"mode","label":"绘制模式","type":"select","options":[["draw","绘制"],["erase","擦除"]],"value":"draw"},
 ],
 "calc":r"""
   const gs=Math.floor(num('gs')), col=document.getElementById('color').value||'#EF4444', mode=document.getElementById('mode').value||'draw';
   if(gs<4||gs>24){ToolBox.setResult('result','<p class="tip-error">网格尺寸需在 4-24 之间。</p>');return;}
   // 预置示例图案（8x8 笑脸），大网格留空
   let grid=[];
   if(gs===8){
     const smile=[
       [0,0,1,1,1,1,0,0],
       [0,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,1],
       [1,1,0,1,1,0,1,1],
       [1,1,1,1,1,1,1,1],
       [1,0,1,1,1,0,1,1],
       [0,1,1,1,1,1,1,0],
       [0,0,1,1,1,1,0,0],
     ];
     for(let r=0;r<gs;r++){ grid[r]=[]; for(let c=0;c<gs;c++){ grid[r][c]=smile[r]&&smile[r][c]?'#F59E0B':''; } }
   } else {
     for(let r=0;r<gs;r++){ grid[r]=[]; for(let c=0;c<gs;c++){ grid[r][c]=''; } }
   }
   // 生成可点击网格
   let board='<div style="display:grid;grid-template-columns:repeat('+gs+',32px);gap:2px;width:max-content;margin:0 auto;">';
   for(let r=0;r<gs;r++){
     for(let c=0;c<gs;c++){
       const cell=grid[r][c];
       board+='<div onclick="window._px&&window._px('+r+','+c+')" style="width:32px;height:32px;border-radius:4px;background:'+(cell||'#e2e8f0')+';cursor:pointer;border:1px solid #cbd5e1;"></div>';
     }
   }
   board+='</div>';
   // 字符画
   let art='';
   for(let r=0;r<gs;r++){
     let line='';
     for(let c=0;c<gs;c++){ line+=grid[r][c]?'■':'·'; }
     art+=line+'\n';
   }
   let html=dataGrid([
     [gs+'×'+gs,'网格尺寸'],
     [col,'当前颜色'],
     [mode==='draw'?'绘制':'擦除','模式']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>画布（点击上色，'+gs+'×'+gs+'）</b></div>'+
     '<div style="margin-top:6px;">'+board+'</div>';
   html += '<div style="margin-top:12px;font-size:13px;"><b>字符画预览</b></div>'+
     '<pre style="background:#0f172a;color:#e2e8f0;border-radius:8px;padding:10px;font-size:12px;line-height:1.2;overflow-x:auto;">'+art+'</pre>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '点击网格上色（■=有色，·=空白）。小网格适合设计，大网格适合精细图案。纯本地绘制不保存。</div>';
   ToolBox.setResult('result', html);
   // 暴露绘制函数（读颜色/模式）；var 使 verify stub 与浏览器均可用
   var _px=function(r,c){
     const el=document.getElementById('result');
     const cells=el.querySelectorAll('div[style*="32px"]');
     const idx=r*gs+c;
     if(!cells[idx]) return;
     const colNow=document.getElementById('color').value||'#EF4444';
     const modeNow=document.getElementById('mode').value||'draw';
     cells[idx].style.background=modeNow==='erase'?'#e2e8f0':colNow;
     cells[idx].setAttribute('data-c',modeNow==='erase'?'':colNow);
   };
   // 浏览器中挂到 window 供 onclick 使用（verify stub 无 window 不报错）
   try{ window._px=_px; }catch(e){};
 """,
 "notes":[
   "点击网格上色，支持绘制/擦除两种模式",
   "8 种基础色板，网格 4-24 可调",
   "字符画用 ■ / · 表示像素，可复制",
   "纯本地绘制，图案不保存不上传",
 ],
},
{
 "slug":"bluetooth-version","industry":"it","cat":"reference","icon":"🔷","bg":"#e0f2fe",
 "accent":"#0284C7","indicon":"💻",
 "title":"蓝牙版本速查",
 "h1":"蓝牙版本速查",
 "h2":"🔷 蓝牙版本速查",
 "desc":"蓝牙版本速查 - 蓝牙 1.0-5.4 各版本速率/距离/特性对照速查表。纯前端本地处理。",
 "intro":"蓝牙 5.4 比 4.2 强在哪？蓝牙各版本速率、距离与核心特性对照速查。",
 "inputs":[
   {"id":"v","label":"版本","type":"select","options":[["4.2","4.2"],["5.0","5.0"],["5.1","5.1"],["5.2","5.2"],["5.3","5.3"],["5.4","5.4"]],"value":"5.3"},
   {"id":"v2","label":"对比版本","type":"select","options":[["4.2","4.2"],["5.0","5.0"],["5.1","5.1"],["5.2","5.2"],["5.3","5.3"],["5.4","5.4"]],"value":"5.0"},
   {"id":"scene","label":"选购场景","type":"select","options":[["audio","耳机/音频"],["iot","智能家居/穿戴"],["peripheral","键鼠/外设"]],"value":"audio"},
 ],
 "calc":r"""
   const v=document.getElementById('v').value||'5.3';
   const v2=document.getElementById('v2').value||'5.0';
   const scene=document.getElementById('scene').value||'audio';
   const info={
     '4.2':['1 Mbps','约 10-100m','低功耗改进、IP 支持','BLE 普及'],
     '5.0':['2 Mbps','约 10-100m（LE 240m）','2倍速率、4倍距离、8倍广播容量','BLE 大升级'],
     '5.1':['2 Mbps','约 10-100m','方向定位（AoA/AoD）','室内定位'],
     '5.2':['2 Mbps','约 10-100m','LE 音频（LC3 编码）','音频新标准'],
     '5.3':['2 Mbps','约 10-100m','连接子评级、周期广播改进','稳定省电'],
     '5.4':['2 Mbps','约 10-100m','广播加密、PAwR 广告响应','工业 IoT'],
   };
   const row=info[v]||info['5.3'], row2=info[v2]||info['5.0'];
   const sceneAdv={audio:v>='5.2'?'支持 LE Audio（LC3）':'仅经典音频（SBC/AAC）',iot:v>='5.0'?'广播容量大、mesh 稳定':'BLE 基础功能',peripheral:v>='5.0'?'速率/距离更优':'够用'}[scene]||'';
   const adv=parseFloat(v)>=parseFloat(v2)?'较新，特性更全':'旧版，兼容性更广';
   let html=dataGrid([
     ['Bluetooth '+v+' vs '+v2,'版本对比'],
     [row[0]+' / '+row2[0],'最大速率'],
     [row[1]+' / '+row2[1],'有效距离'],
     [row[2],'所选版本核心特性'],
     [adv+' · '+sceneAdv,'建议']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>蓝牙历代版本特性</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">版本</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">速率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">特性</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1.x</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">初代基础</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">2.x</td><td style="border:1px solid #d1d5db;padding:5px 8px;">3 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">EDR 增强速率</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">3.x</td><td style="border:1px solid #d1d5db;padding:5px 8px;">24 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">HS 高速（WiFi 辅助）</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">4.0-4.2</td><td style="border:1px solid #d1d5db;padding:5px 8px;">1 Mbps（BLE）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">低功耗 BLE 引入</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">5.0</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2 Mbps（BLE）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">速率/距离/广播翻倍</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">5.2</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2 Mbps（BLE）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">LE Audio 音频</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">5.3/5.4</td><td style="border:1px solid #d1d5db;padding:5px 8px;">2 Mbps（BLE）</td><td style="border:1px solid #d1d5db;padding:5px 8px;">连接改进/广播加密</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     '蓝牙版本向下兼容；实际距离受环境与功率影响，LE 远距模式可达 240m。选购设备看 BLE 版本即可。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "经典蓝牙速率：1.x 1M / 2.x EDR 3M / 3.x HS 24Mbps",
   "BLE：4.x 1Mbps、5.x 2Mbps",
   "5.0：速率/距离/广播容量 2 倍以上",
   "5.2 起支持 LE Audio（LC3 编码）",
 ],
},
{
 "slug":"usb-version","industry":"it","cat":"reference","icon":"🔗","bg":"#fef9c3",
 "accent":"#CA8A04","indicon":"💻",
 "title":"USB 版本速查",
 "h1":"USB 版本速查",
 "h2":"🔗 USB 版本速查",
 "desc":"USB 版本速查 - USB 1.0-4.0 各版本速率/接口/供电对照速查表。纯前端本地处理。",
 "intro":"USB 4 多快？USB 各版本速率、接口形态与供电能力对照速查。",
 "inputs":[
   {"id":"v","label":"版本","type":"select","options":[["2.0","2.0"],["3.0","3.0"],["3.1","3.1"],["3.2","3.2"],["4.0","4.0"]],"value":"3.2"},
   {"id":"v2","label":"对比版本","type":"select","options":[["2.0","2.0"],["3.0","3.0"],["3.1","3.1"],["3.2","3.2"],["4.0","4.0"]],"value":"2.0"},
   {"id":"conn","label":"接口类型","type":"select","options":[["usbc","USB-C"],["typea","Type-A"],["micro","Micro-USB"]],"value":"usbc"},
 ],
 "calc":r"""
   const v=document.getElementById('v').value||'3.2';
   const v2=document.getElementById('v2').value||'2.0';
   const conn=document.getElementById('conn').value||'usbc';
   const info={
     '2.0':['480 Mbps','USB-A/B/Mini/Micro','5V / 0.5A','普及型'],
     '3.0':['5 Gbps','USB-A（蓝芯）/C','5V / 0.9A','SuperSpeed'],
     '3.1':['10 Gbps','USB-C 为主','5V / 0.9A','SuperSpeed+'],
     '3.2':['20 Gbps','USB-C','5V / 1.5A','双通道'],
     '4.0':['40 Gbps','USB-C','最高 240W（PD 3.1）','雷电兼容'],
   };
   const row=info[v]||info['3.2'], row2=info[v2]||info['2.0'];
   const connNote={usbc:parseFloat(v)>=3.1?'USB-C 支持全速率':'USB-C 仅承载较低速率',typea:parseFloat(v)<=3.0?'Type-A 常见':'Type-A 少见（需 C）',micro:parseFloat(v)<=2.0?'Micro 常见':'Micro 已淘汰'}[conn]||'';
   const adv=parseFloat(v)>=parseFloat(v2)?'较新，速率更高':'旧版，兼容更广';
   let html=dataGrid([
     ['USB '+v+' vs '+v2,'版本对比'],
     [row[0]+' / '+row2[0],'最大速率'],
     [row[1]+' / '+row2[1],'接口形态'],
     [row[2]+' / '+row2[2],'供电能力'],
     [adv+' · '+connNote,'建议']
   ]);
   html += '<div style="margin-top:12px;font-size:13px;"><b>USB 历代版本特性</b></div>'+
     '<table class="csv-prev" style="margin-top:6px;border-collapse:collapse;width:100%;font-size:12.5px;">'+
     '<tr><th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">版本</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">速率</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">接口</th>'+
     '<th style="border:1px solid #d1d5db;padding:5px 8px;background:#f3f4f6;">供电</th></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">1.0/1.1</td><td style="border:1px solid #d1d5db;padding:5px 8px;">12 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">USB-A/B</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5V/0.5A</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">2.0</td><td style="border:1px solid #d1d5db;padding:5px 8px;">480 Mbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">A/B/Mini/Micro</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5V/0.5A</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">3.0</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5 Gbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">A（蓝芯）/C</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5V/0.9A</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">3.1</td><td style="border:1px solid #d1d5db;padding:5px 8px;">10 Gbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">C 为主</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5V/0.9A</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">3.2</td><td style="border:1px solid #d1d5db;padding:5px 8px;">20 Gbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">USB-C</td><td style="border:1px solid #d1d5db;padding:5px 8px;">5V/1.5A</td></tr>'+
     '<tr><td style="border:1px solid #d1d5db;padding:5px 8px;">4.0</td><td style="border:1px solid #d1d5db;padding:5px 8px;">40 Gbps</td><td style="border:1px solid #d1d5db;padding:5px 8px;">USB-C</td><td style="border:1px solid #d1d5db;padding:5px 8px;">PD 3.1 最高 240W</td></tr>'+
     '</table>';
   html += '<div class="tip-mini" style="margin-top:10px;font-size:13px;color:var(--text-muted);">'+
     'USB 4 基于 Thunderbolt 3 协议，兼容 USB 3.2/2.0；实际速率受线缆与设备双端支持限制。</div>';
   ToolBox.setResult('result', html);
 """,
 "notes":[
   "USB 2.0 480M / 3.0 5G / 3.1 10G / 3.2 20G / 4.0 40Gbps",
   "USB 3.x 接口多为蓝色芯（Type-A）",
   "USB 4 兼容雷电 3，必须 Type-C",
   "实际速率取两端设备与线缆的较低者",
 ],
},
]

def render_inputs(t):
    rows=[]
    ins=t["inputs"]
    for i in range(0,len(ins),3):
        chunk=ins[i:i+3]
        cells=[]
        for f in chunk:
            ftype=f.get("type","number")
            if ftype=="select":
                opts="".join('<option value="%s">%s</option>'%(o[0],o[1]) for o in f.get("opts",[]))
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <select id="%s" style="width:100%%;">%s</select>\n      </div>'%(f["id"],f["label"],f["id"],opts))
            elif ftype=="checkbox":
                boxes="".join(
                  '<label style="display:flex;align-items:center;gap:6px;cursor:pointer;font-size:13px;margin:4px 0;">'
                  '<input type="checkbox" id="top_%s" value="%s" data-name="%s">%s</label>'%(o[0],o[1].split(" ")[1] if " " in o[1] else "0",o[1].split(" ")[0],o[1])
                  for o in f.get("opts",[]))
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <div style="display:flex;flex-wrap:wrap;gap:0 16px;">%s</div>\n      </div>'%(f["id"],f["label"],boxes))
            elif ftype=="date":
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <input type="date" id="%s" value="%s">\n      </div>'%(f["id"],f["label"],f["id"],f["value"]))
            elif ftype=="text":
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <input type="text" id="%s" value="%s" placeholder="%s">\n      </div>'%(f["id"],f["label"],f["id"],f.get("value",""),f.get("placeholder","")))
            elif ftype=="textarea":
                val=(f.get("value","") or "").replace("&","&amp;").replace('"',"&quot;").replace("\n","&#10;")
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <textarea id="%s" rows="%s" style="width:100%%;font-family:monospace;font-size:12.5px;">%s</textarea>\n      </div>'%(f["id"],f["label"],f["id"],f.get("rows","5"),val))
            else:
                minv=f.get("min",""); maxv=f.get("max","")
                extra=(" min='%s'"%minv) if minv!="" else ""
                extra+=(" max='%s'"%maxv) if maxv!="" else ""
                cells.append('      <div>\n        <label for="%s">%s</label>\n        <input type="number" id="%s" value="%s" step="%s"%s>\n      </div>'%(f["id"],f["label"],f["id"],f["value"],f.get("step","1"),extra))
        rows.append('    <div class="input-row">\n'+ "\n".join(cells)+'\n    </div>')
    return "\n".join(rows)

def render_reset(t):
    lines=[]
    for f in t["inputs"]:
        ftype=f.get("type","number")
        if ftype=="select":
            lines.append("document.getElementById('%s').selectedIndex=0;"%f["id"])
        elif ftype=="checkbox":
            for o in f.get("opts",[]):
                lines.append("document.getElementById('top_%s').checked=false;"%o[0])
        elif ftype=="date":
            lines.append("document.getElementById('%s').value='%s';"%(f["id"],f["value"]))
        elif ftype=="textarea":
            v=(f.get("value","") or "").replace("\\","\\\\").replace("'","\\'").replace("\n","\\n")
            lines.append("document.getElementById('%s').value='%s';"%(f["id"],v))
        else:
            lines.append("document.getElementById('%s').value='%s';"%(f["id"],f["value"]))
    lines.append("calcTool();")
    return "\n      ".join(lines)

def render(t):
    return (TEMPLATE
        .replace("__CAT__",t["cat"]).replace("__INDUSTRY__",t["industry"])
        .replace("__ICON__",t["icon"]).replace("__BG__",t["bg"])
        .replace("__ACCENT__",t["accent"]).replace("__INDICON__",t["indicon"])
        .replace("__SLUG__",t["slug"]).replace("__TITLE__",H.escape(t["title"]))
        .replace("__H1__",H.escape(t["h1"])).replace("__H2__",H.escape(t["h2"]))
        .replace("__INTRO__",H.escape(t["intro"])).replace("__DESC__",H.escape(t["desc"]))
        .replace("__CATZH__",IND_ZH[t["industry"]]).replace("__BASE__",BASE)
        .replace("__INPUTS__",render_inputs(t))
        .replace("__CALC__",t["calc"].strip())
        .replace("__RESET__",render_reset(t))
        .replace("__NOTES__","\n".join("        <li>%s</li>"%n for n in t["notes"])))

def main():
    for t in TOOLS:
        d=os.path.join(TOOLS_DIR,t["industry"]); os.makedirs(d,exist_ok=True)
        p=os.path.join(d,t["slug"]+".html")
        with open(p,"w",encoding="utf-8") as f:
            f.write(render(t))
        print("  + tools/%s/%s.html"%(t["industry"],t["slug"]))
    print("共生成 %d 个工具页"%len(TOOLS))

if __name__=="__main__":
    main()
