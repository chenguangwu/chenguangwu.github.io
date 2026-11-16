#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "service/complaint-analysis",
  "clicks": [
    "document.getElementById('complaintText').value='配送太慢了，等了三天才到\\n商品质量有问题，收到就坏了';calc();"
  ],
  "expect": [
    "2 投诉总数",
    "物流 1 (50.0%)"
  ],
  "ref": "两条投诉分别命中物流（配送/慢）与质量（质量/坏了）⇒ 总数 2、物流 1 条占 50.0%。"
     + "原用例 expect「保修_X」直接抄自 keywords 输入框自身文本（collectStrings 收录该输入框的 value），与计算无关 ⇒ 逃生项，已重写。"
     + "不用「100% 分类覆盖率」：页面 fallback 会调 loadDemo()，10 条示例同样 0 未分类 ⇒ 该锚在注入失败时仍命中（逃生）；「2 投诉总数」「物流 1 (50.0%)」在示例态（10 条 / 物流 3）均不出现。"
},
{
  "slug": "service/csat-score",
  "inputs": {
    "s5": "120",
    "s4": "60",
    "s3": "20",
    "s2": "10",
    "s1": "6"
  },
  "clicks": ["calc()"],
  "expect": [
    "83.3% CSAT",
    "4.29 平均星级",
    "216 总评价数"
  ],
  "ref": "总评价数=120+60+20+10+6=216；CSAT=(120+60)/216=83.33%；"
     + "平均星级=(600+240+60+20+6)/216=4.287→4.29；NPS=(120−16)/216=48.1→48。"
     + "原 45/30/12/8/5 为默认态。等级词「良好」两态同现，不入断言。"
},
{
  "slug": "service/csat-score",
  "inputs": {
    "s5": "0",
    "s4": "0",
    "s3": "0",
    "s2": "0",
    "s1": "0"
  },
  "clicks": ["calc()"],
  "expect": [
    "请至少输入一条评价"
  ],
  "ref": "修复前全部清零仍输出 0.0% CSAT、「需改善」及 NaN% 星级分布；现提示补录"
},
{
  "slug": "service/csat-score",
  "inputs": {"s5":"10","s4":"0","s3":"0","s2":"0","s1":"-1"},
  "clicks": ["var cap=null,ot=ToolBox.copyText,ts=ToolBox.showToast;ToolBox.copyText=function(t){cap=String(t);};ToolBox.showToast=function(){};try{copyReport();}finally{ToolBox.copyText=ot;ToolBox.showToast=ts;}document.getElementById('__tbProbe').textContent='CSATCPY '+((cap===null||cap==='')?'OK':'BAD '+cap);"],
  "expect": ["CSATCPY OK"],
  "ref": "590：copyReport 原用 parseInt(v)||0 绕过 calc 校验，5星10/1星-1 会把 -1 截成 0 仍导出 10 人报告。修复后共用 readCounts 校验，非法输入直接拒绝、不复制。合法态默认 45/30/12/8/5 不触发探针串。"
},
{
  "slug": "service/csat-score",
  "inputs": {"s5":"50","s4":"30","s3":"12","s2":"5","s1":"3"},
  "clicks": ["var cap=null,ot=ToolBox.copyText;ToolBox.copyText=function(t){cap=String(t);};try{copyReport();}finally{ToolBox.copyText=ot;}document.getElementById('__tbProbe').textContent='CSATAGENT '+((cap&&cap.indexOf('NPS（星级代理）')>=0&&cap.indexOf('总评价：100人')>=0)?'OK':'BAD '+String(cap).slice(0,60));"],
  "expect": ["CSATAGENT OK"],
  "ref": "590：复制报告里的 NPS 需标注「星级代理」，与统计卡/公式框口径一致，避免误认为标准推荐意愿问卷。100 条评价导出报告须含该标注；旧源码仅写「NPS：」⇒ BAD。"
},
{
  "slug": "service/csat-score",
  "inputs": {"s5":"50","s4":"30","s3":"12","s2":"5","s1":"3"},
  "clicks": ["var cap=null,ot=ToolBox.copyText;ToolBox.copyText=function(t){cap=String(t);};var prevTB=globalThis.TBKit;globalThis.TBKit={util:{isEn:function(){return true;}}};try{copyReport();}finally{ToolBox.copyText=ot;globalThis.TBKit=prevTB;}var ok=!!cap&&cap.indexOf('CSAT Satisfaction Report')>=0&&cap.indexOf('NPS (star-based proxy)')>=0&&cap.indexOf('Total ratings: 100')>=0&&!/[\\u4e00-\\u9fa5]/.test(cap);document.getElementById('__tbProbe').textContent='CSATEN '+(ok?'OK':'BAD '+String(cap).slice(0,50));"],
  "expect": ["CSATEN OK"],
  "ref": "881 复核失败重做：copyReport 原硬编码中文，英文态复制仍出中文报告（英文 DOM 探针覆盖不到剪贴板）。注入 isEn=true 捕获 copyText，断言英文报告串且零 CJK；旧实现输出中文 ⇒ BAD。合法态默认 45/30/12/8/5 不触发探针串。"
},
{
  "slug": "service/csat-score",
  "inputs": {
    "s5": "10",
    "s4": "0",
    "s3": "0",
    "s2": "0",
    "s1": "-3"
  },
  "clicks": ["calc()"],
  "expect": [
    "留空或负数无法统计"
  ],
  "ref": "修复前负人数直接参与合计，CSAT 失真；现拒绝负数"
},
{
  "slug": "service/response-time",
  "inputs": {
    "slaTarget": "45"
  },
  "expect": [
    "100.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "service/script-template",
  "clicks": ["showScript(SCRIPTS[5]);"],
  "expect": [
    "场景：致歉安抚"
  ],
  "ref": "独立复算：SCRIPTS[5] = {cat:'apology', catLabel:'致歉安抚', text:'实在不好意思让您久等了，感谢您的耐心，我们马上为您跟进处理。'}；showScript() 把「场景：致歉安抚」与该话术全文写进 #scriptDisplay（默认占位为「点击「随机抽取」按钮获取话术」+「支持按场景筛选…」）。锚取「场景：」+ 分类标签的复合串 —— 单锚话术正文会撞 #scriptList 里同条目的卡片预览，属默认态必命中串（即逃生项）。"
},
{
  "slug": "service/ticket-priority",
  "clicks": ["tickets=[{name:'支付页面报错',urgency:5,importance:4},{name:'发票开具咨询',urgency:2,importance:3},{name:'账号无法登录',urgency:4,importance:5}];render()"],
  "expect": [
    "1. 支付页面报错",
    "紧急度：5/5 · 重要度：4/5 · 最高优先 20",
    "发票开具咨询"
  ],
  "ref": "顶层数组 tickets 注入 3 条：score = urgency × importance ⇒ 支付页面报错 5×4 = 20（并列最高、排序取其先）、账号无法登录 4×5 = 20、发票开具咨询 2×3 = 6。默认态为源码内置 6 条工单（系统宕机 5/5、25 分），三串均不命中。"
},
{
  "slug": "service/response-time",
  "clicks": [
    "document.getElementById('slaTarget').value='0';calc();document.getElementById('__tbProbe').textContent='RTSLA='+((String(document.getElementById('stats').innerHTML).indexOf('SLA目标需为正数')>=0)?'Y':'N');"
  ],
  "expect": ["RTSLA=Y"],
  "ref": "修复前 SLA 目标清空或填 0 被静默按 30 分钟兜底；现判定目标无效，SLA 卡显示「--」并标注「SLA目标需为正数」，不再给出误导性的达标率。默认 30 不出现该文案。"
},
{
  "slug": "service/response-time",
  "clicks": [
    "tickets=[{id:'A',resp:5,solve:0,status:'resolved'},{id:'B',resp:10,solve:0,status:'pending'}];renderList();calc();document.getElementById('__tbProbe').textContent='RTRATE='+String(document.getElementById('stats').innerHTML).match(/([\\d.]+)%<\\/div><div class=\"lbl\">解决率/)[1];"
  ],
  "expect": ["RTRATE=50.0"],
  "ref": "修复前解决率分子只数 solve>0 的已解决工单，已解决但解决时间为 0 的被漏掉（本例得 0.0%）；现按状态统计已解决占比 1/2=50.0%。默认 8 条工单为 87.5%，不命中也无该探针串。"
},
{
  "slug": "service/response-time",
  "clicks": [
    "tickets=[{id:'A',resp:null,solve:60,status:'resolved'},{id:'B',resp:20,solve:60,status:'resolved'}];renderList();calc();document.getElementById('__tbProbe').textContent='RTEMPTY='+(String(document.getElementById('stats').innerHTML).indexOf('20.0分')>=0?'Y':'N');"
  ],
  "expect": ["RTEMPTY=Y"],
  "ref": "修复前空响应时间被当成 0 计入均值（两条得 10.0 分）；现未填写的响应时间不参与均值/分位数统计，仅 B 的 20.0 分入样。默认态无 RTEMPTY 探针串。"
},
{
  "slug": "service/response-time",
  "inputs": { "slaTarget": "45" },
  "clicks": [
    "tickets=[{id:'Z',resp:5,solve:0,status:'resolved'},{id:'Y',resp:15,solve:20,status:'resolved'}];renderList();calc();var s=String(document.getElementById('stats').innerHTML);var d=String(document.getElementById('detailBody').innerHTML);document.getElementById('__tbProbe').textContent='RTZERO10 '+(s.indexOf('10.0分')>=0&&d.indexOf('<td>0.0</td>')>=0?'OK':'BAD');"
  ],
  "expect": ["RTZERO10 OK"],
  "ref": "591 批复核失败回归：已解决且解决时间 0 分钟是合法采样，旧 `solve>0` 把 Z 排除在平均解决时间外只剩 20 分钟；现按 `solve>=0` 入样，两条 (0+20)/2=10.0 分，明细应显示 0.0 而非「-」。注入 SLA=45（默认 30）避免默认态。"
},
{
  "slug": "service/response-time",
  "inputs": { "slaTarget": "45" },
  "clicks": [
    "tickets=[{id:'N',resp:null,solve:5,status:'resolved'},{id:'M',resp:20,solve:null,status:'pending'}];renderList();calc();var d=String(document.getElementById('detailBody').innerHTML);var row=d.split('</tr>').filter(function(r){return r.indexOf('>N<')>=0;})[0]||'';document.getElementById('__tbProbe').textContent='RTNOSAMPLE '+(row.indexOf('<td>-</td><td>5.0</td>')>=0&&row.indexOf('超标')<0?'OK':'BAD');"
  ],
  "expect": ["RTNOSAMPLE OK"],
  "ref": "591 批复核失败回归：SLA 有效但响应时间未采样时，旧明细把 ok=false 直接显示「超标」，等于把「没数据」当成违规；现无采样显示「-」且不着红色。注入 N 行 resp=null 专锚该行，默认 8 单响应均非空。"
},
{
  "slug": "service/ticket-priority",
  "clicks": [
    "var esrc=/ToolBox\\.escHtml\\(r\\[0\\]\\)/.test(String(__tpTable));var csrc=/tb0\\.innerHTML=''/.test(String(__tpExtras));tickets=[{name:'A',urgency:5,importance:5}];render();tickets=[];render();var clr=document.getElementById('q1').innerHTML.indexOf('A')<0&&document.getElementById('prioList').innerHTML.indexOf('暂无工单')>=0;document.getElementById('__tbProbe').textContent='TPX '+(esrc&&csrc&&clr);"
  ],
  "expect": ["TPX true"],
  "ref": "修复前明细表把工单名直接拼进 innerHTML（注入路径），且空列表时 __tpExtras 提前 return 使明细表残留旧行；现明细表名经 ToolBox.escHtml 转义、空列表分支先清空 tbody 再返回。harness 的 escHtml 桩为恒等函数且 #tpChart 缺失导致 __tpTable 提前返回，故转义与清表用源码形态判定，空态 DOM 另行校验。默认 6 条工单不产生该探针串。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== service calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
