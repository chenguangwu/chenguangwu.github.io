#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {
    "wet": "150",
    "dry": "135",
    "fired": "120",
    "targetFired": "200",
    "totalShrink": "18"
  },
  "clicks": [
    "calc();calcReverse()"
  ],
  "expect": [
    "20.00%",
    "10.00%",
    "11.11%",
    "243.90"
  ],
  "ref": "S干=(150−135)/150=10.00%、S烧=(135−120)/135=11.11%、S总=(150−120)/150=20.00%（独立复算）；反向 L₀=L₂/(1−S总)=200/(1−0.18)=243.90 mm。默认 120/112/100 ⇒ 6.67% / 10.71% / 16.67%、L₀=116.28 ⇒ 四个锚点全不命中。原 expect「公式」是 calcReverse 的 step-line 标签常量（默认态同样渲染）⇒ 已替换。"
},
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {"wet":"100","dry":"120","fired":"130"},
  "clicks": ["calc();"],
  "expect": ["尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成"],
  "ref": "注入 100/120/130（干坯大于湿坯、烧成大于干坯），calc() 报「尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成」且不产生 .big-result；默认 120/112/100 合法 ⇒ 不含该错误串。"
},
{
  "slug": "ceramics/glaze-ratio",
  "inputs": {
    "totalW": "1500"
  },
  "clicks": ["calc();"],
  "expect": [
    "375.0"
  ],
  "ref": "1500g × 石英 25% = 375.0g；strict 默认口径合计 100% 不触发归一化提示。"
},
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {"wet":"100","dry":"120","fired":"130"},
  "clicks": ["calc();"],
  "expect": ["尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成"],
  "ref": "注入 100/120/130（干坯大于湿坯、烧成大于干坯），calc() 报「尺寸需满足 湿坯 ≥ 干坯 ≥ 烧成」且不产生 .big-result；默认 120/112/100 合法 ⇒ 不含该错误串。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["MATS[4].pct='-5';calc();"],
  "expect": [
    "比例须为 0–100 的有限数"
  ],
  "ref": "第 5 项氧化锌比例注入 -5，calc() 逐行校验后列出「第 5 项「氧化锌」比例须为 0–100 的有限数（当前 -5）」并清空称量表；默认全 0–100 合法 ⇒ 不出现该文案。"
},
{
  "slug": "ceramics/glaze-temp",
  "inputs": {
    "coneTargetTemp": "1150"
  },
  "expect": [
    "最接近测温锥：4 · 1142°C · 中温"
  ],
  "ref": "改用页面真实计算输入：#coneTargetTemp（默认 1200，oninput=__coneLookup）。注入 1150 ⇒ 与 CONES 最近的锥 4（1142°C，中温），差值 +8°C（「高于锥号 4（1142°C）8°C」）、华氏 ≈2102.0 °F，判定在 ±30°C 容差内。原断言「1060°C」是默认全量表 CONES 的常量行（锥 01），与输入无关 ⇒ 零判别力，且该页本就有可注入的计算器，无需以 no_inputs 兜底。"
},
{
  "slug": "ceramics/kiln-firing",
  "clicks": ["switchTab('porcelain');"],
  "expect": [
    "峰值温度 1300°C；可计算段：升温 18.3 h + 保温 2.5–3.0 h + 慢冷 6.3 h = 约 27.0–27.5 小时（不含自然冷却段）。"
  ],
  "ref": "独立复算 porcelain：升温 (150−25)/50=2.5 +(600−150)/70=6.43 +(950−600)/100=3.5 +(1100−950)/50=3 +(1300−1100)/70=2.86 =18.29，保温 排湿1.5+氧化0.5+高保温0.5~1=2.5~3，慢冷 (1300−800)/80=6.25，合计 27.04~27.54 ⇒ 27.0–27.5 h；自然冷却未计入。switchTab() 切到 porcelain 后 render() 由 __kfEstimate 逐段按温度区间÷速率计保温，不再取静态 totalDesc。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {
    "diameter": "23"
  },
  "expect": [
    "0.230"
  ],
  "ref": "auto-restore"
}
,
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["MATS.forEach(function(m){m.pct=0;});MATS[0].pct=90;calc();var h=String(document.getElementById('result').innerHTML);var w=document.getElementById('w_0');document.getElementById('__tbProbe').textContent='TB828G '+((h.indexOf('严格口径要求配方合计')>=0&&h.indexOf('按比例归一化')>=0&&h.indexOf('需加水量')<0&&w&&w.value==='—')?'OK':'BAD');"],
  "expect": ["TB828G OK"],
  "ref": "strict 口径下合计 90%：停算并提示切「按比例归一化」，列出补足/扣减表，称量输入置 —，不输出需加水量。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["document.getElementById('sumMode').value='normalize';document.getElementById('totalW').value='1000';MATS.forEach(function(m){m.pct=0;});MATS[0].pct=99.6;renderMats();calc();var h=String(document.getElementById('result').innerHTML);var w=document.getElementById('w_0').value;document.getElementById('__tbProbe').textContent='GNORM '+((h.indexOf('原始配方合计 99.6%')>=0&&h.indexOf('最大单料调整 0.40')>=0&&w==='1000.0 g')?'OK':'BAD');"],
  "expect": ["GNORM OK"],
  "ref": "用户切到 normalize 并确认：99.6% 饱和配方按比例缩放到 100%，单料 1000g，显示原始合计与最大调整 0.40 个百分点。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {"diameter":"23","maxRpm":"60"},
  "expect": ["超过设备最高 60 rpm", "可用转速 ≈ 60 rpm（设备限幅后）"],
  "ref": "第828批：23cm 开孔标准偏好理论约 90 rpm，设备最高 60 rpm 时限幅到 60；旧实现硬编码 30–320 且仍称推荐。现在显示理论/可用/实际/偏差并明确限幅，探针断超限说明与可用转速文案。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["MATS[0].pct='';calc();var w=document.getElementById('w_0');document.getElementById('__tbProbe').textContent='GBLANK '+((document.getElementById('result').innerHTML.indexOf('比例为必填')>=0&&w&&w.value==='—')?'OK':'BAD');"],
  "expect": ["GBLANK OK"],
  "ref": "清空第 1 项比例后必须报“比例为必填”并把称量表置 —；旧实现把空串 Number 成 0 继续，可能显示合格。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["calc();var w=document.getElementById('w_0');var before=w.value;document.getElementById('totalW').value='0';calc();document.getElementById('__tbProbe').textContent='GTOTAL '+((before!=='—'&&before!=='')?'BEFORE_OK':'BEFORE_BAD')+' '+((w.value==='—')?'CLEAR_OK':'CLEAR_BAD');"],
  "expect": ["GTOTAL BEFORE_OK CLEAR_OK"],
  "ref": "先算有效配方，再把总重设为 0：原先提前 return 保留上一批克数，现同步把所有称量输入置 —。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["MATS[0].name='<img src=x onerror=window.__inj=1>';renderMats();calc();var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ceramics/glaze-ratio.html','utf8');var seg=h.slice(h.indexOf('function renderMats'),h.indexOf('function updateMat'));var b=document.querySelectorAll('#result img').length,t=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='GINJ '+((seg.indexOf('innerHTML=')>=0&&seg.indexOf('+m.name')<0&&seg.indexOf('name.value=m.name')>=0)?'DOM_OK':'DOM_BAD')+' '+b+' '+(t.indexOf('&lt;img')>=0?'ESC_OK':'ESC_BAD');"],
  "expect": ["GINJ DOM_OK 0 ESC_OK"],
  "ref": "原料名通过 DOM value/textContent 与结果表 escHtml 输出，引号/尖括号不会生成真实 img 节点。"
},
{
  "slug": "ceramics/glaze-ratio",
  "clicks": ["var cb=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){},exportTable:function(){}},matrix:{table:function(){}},chart:{line:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(sel,f){cb=f;}}};__glaze_ratioRender(['totalW'],'结果',false);cb({totalW:'500',method:'0.8',__mats:'[{\"name\":\"A料\",\"pct\":\"50\"},{\"name\":\"B料\",\"pct\":\"50\"}]'});document.getElementById('__tbProbe').textContent='GHIST '+MATS.length+' '+MATS[0].name+' '+MATS[0].pct;"],
  "expect": ["GHIST 2 A料 50"],
  "ref": "历史记录携带 __mats 完整清单；恢复时先重建列表再回填输入并计算，避免只恢复总重/方法。"
},
{
  "slug": "ceramics/clay-shrinkage",
  "clicks": ["var cb=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){},exportTable:function(){}},matrix:{table:function(){}},chart:{line:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(sel,f){cb=f;}}};__clay_shrinkageRender(['wet','dry','fired','targetFired','totalShrink'],'结果',false);cb({wet:'120',dry:'112',fired:'100',targetFired:'200',totalShrink:'20'});var r=document.getElementById('reverseResult').innerHTML;document.getElementById('__tbProbe').textContent='CHIST '+((r.indexOf('250.00')>=0)?'OK':'BAD');"],
  "expect": ["CHIST OK"],
  "ref": "恢复历史时同时重算正算与反算；旧实现只调 calc()，反算区仍留上一组结果。"
},
{
  "slug": "ceramics/ceramic-firing",
  "clicks": ["var cb=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){},exportTable:function(){}},matrix:{table:function(){}},chart:{line:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(sel,f){cb=f;}}};__ceramic_firingRender(['fireType'],'结果',false);cb({fireType:'bisque',__clay:'porcelain'});document.getElementById('__tbProbe').textContent='CFCLAY '+selectedClay;"],
  "expect": ["CFCLAY porcelain"],
  "ref": "历史记录保存 __clay；恢复时先还原泥料选择再 renderCurve，跨泥料回放不被当前选择覆盖。"
},
{
  "slug": "ceramics/wheel-speed",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ceramics/wheel-speed.html','utf8');var i=h.indexOf('function copyResult');var seg=h.slice(i,i+420);document.getElementById('__tbProbe').textContent='WCOPY '+((seg.indexOf('#result .big-result')>=0&&seg.indexOf('当前没有有效计算结果')>=0&&seg.indexOf('拉坯转速结果')<0)?'OK':'BAD');"],
  "expect": ["WCOPY OK"],
  "ref": "无效直径时结果区无 .big-result，copyResult 必须提示而不是复制占位“拉坯转速结果”并报成功。"
},
{
  "slug": "ceramics/kiln-firing",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ceramics/kiln-firing.html','utf8');var i=h.indexOf('function __kfExport');var seg=h.slice(i,i+1200);var zh=__kfTr('排湿',false),en=__kfTr('排湿',true),nm=__kfName('素烧（Bisque）',true);document.getElementById('__tbProbe').textContent='KEXP '+((zh==='排湿'&&en==='Drying'&&nm==='Bisque'&&seg.indexOf('Type')>=0&&seg.indexOf('Stage')>=0&&seg.indexOf('Temp Range')>=0&&seg.indexOf('类型')>=0&&seg.indexOf('温度区间')>=0&&seg.indexOf('__kfTr(st[4],en)')>=0)?'OK':'BAD');"],
  "expect": ["KEXP OK"],
  "ref": "导出表头与每行字段按当前语言生成：中文态全中文表头/名称，英文态全英文名称、阶段、速率与保温；不再只切文件名。"
},
{
  "slug": "ceramics/clay-shrinkage",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ceramics/clay-shrinkage.html','utf8');var i=h.indexOf('data-related-tools');var seg=h.slice(i,i+1500);var n=seg.split('related-tool-card').length-1;var biz=seg.indexOf('../biz')>=0;document.getElementById('__tbProbe').textContent='CREL '+((n>=4&&!biz)?'OK':'BAD');"],
  "expect": ["CREL OK"],
  "ref": "相关工具改为陶瓷工序同类工具（泥料/釉料/拉坯/窑炉/烧成），不再推荐演讲计时、Markdown、Zalgo 等无关工具。"
},
{
  "slug": "ceramics/ceramic-firing",
  "clicks": ["document.getElementById('fireType').value='glaze';renderCurve();var a=__cfStageLines();document.getElementById('fireType').value='bisque';renderCurve();var b=__cfStageLines();document.getElementById('__tbProbe').textContent='CF573 '+((a.indexOf('300→573°C')>=0&&a.indexOf('573→600°C')>=0&&b.indexOf('300→573°C')>=0&&b.indexOf('573→600°C')>=0)?'OK':'BAD');"],
  "expect": ["CF573 OK"],
  "ref": "素烧/釉烧都把原 300→600 拆成 300→573 与 573→600 两段，600→800 明确写在石英转变之后；此前 573 转变点被压在一段内、文字位置错。"
},
{
  "slug": "ceramics/ceramic-firing",
  "clicks": ["var cap='';ToolBox.copyText=function(t){cap=String(t);};i18nText=function(){return '';};renderCurve();copyResult();document.getElementById('__tbProbe').textContent='CFCOPY '+((cap.indexOf('各阶段参数')>=0&&cap.indexOf('300→573°C')>=0&&cap.indexOf('573→600°C')>=0&&cap.indexOf('速率')>=0&&cap.indexOf('时长')>=0)?'OK':'BAD');"],
  "expect": ["CFCOPY OK"],
  "ref": "复制方案必须逐段含起止温度、速率、时长与说明，不能只复制峰值与合计。"
},
{
  "slug": "ceramics/ceramic-firing",
  "clicks": ["var csv='';ToolBox.downloadText=function(n,c){csv=String(c);};__cfExportCsv();document.getElementById('__tbProbe').textContent='CFCSV '+((csv.indexOf('300→573°C')>=0&&csv.indexOf('573→600°C')>=0&&csv.indexOf('起止温度')>=0&&csv.indexOf('速率')>=0&&csv.indexOf('时长')>=0)?'OK':'BAD');"],
  "expect": ["CFCSV OK"],
  "ref": "CSV 导出当前泥料/烧制类型的结构化阶段，含起止温度/速率/时长/说明与工艺示例备注。"
},
{
  "slug": "ceramics/kiln-firing",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ceramics/kiln-firing.html','utf8');var i=h.indexOf('function __kfExport');var seg=h.slice(i,i+1400);document.getElementById('__tbProbe').textContent='KFSCOPE '+((seg.indexOf('[cur]')>=0&&seg.indexOf('Object.keys(SCHED)')>=0&&seg.indexOf('kiln-firing-all-types.csv')>=0&&seg.indexOf('窑炉烧成曲线-全部类型.csv')>=0&&seg.indexOf('窑炉烧成曲线-\\'+SCHED[cur].name')>=0&&seg.indexOf('__kfName(s.name,en)')>=0)?'OK':'BAD');"],
  "expect": ["KFSCOPE OK"],
  "ref": "导出范围与按钮标签一致：cur 只取 [cur] 且文件名含当前类型；all 取 Object.keys(SCHED)、文件名含全部类型、每行带类型列。"
},
{
  "slug": "ceramics/glaze-temp",
  "clicks": ["document.getElementById('search').value='低温';renderTable();var n1=__coneFilterList().length;var h1=document.getElementById('refTable').innerHTML;document.getElementById('search').value='low';renderTable();var n2=__coneFilterList().length;var src=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ceramics/glaze-temp.html','utf8');var seg=src.slice(src.indexOf('window.__coneExport'),src.indexOf('renderTable();'));document.getElementById('__tbProbe').textContent='GTSCOPE '+((n1===22&&n2===22&&h1.indexOf('低温')>=0&&seg.indexOf('var list=__coneFilterList()')>=0)?'OK':'BAD '+n1+' '+n2);"],
  "expect": ["GTSCOPE OK"],
  "ref": "搜索低温/英文 low 都命中 22 个低温锥；导出与表格共用 __coneFilterList()，不再只匹配锥号+温度。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {"diameter":"23","minRpm":"30","maxRpm":"60"},
  "clicks": ["calc();"],
  "expect": ["超过设备最高 60 rpm", "实际线速度比目标低 33%"],
  "ref": "23cm 理论约 90rpm 被最高 60rpm 压低，实际线速度应低于目标 33%；旧文案反写「比目标高」。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {"diameter":"40","minRpm":"120","maxRpm":"320"},
  "clicks": ["calc();"],
  "expect": ["低于设备最低 120 rpm", "实际线速度比目标高 132%"],
  "ref": "40cm 理论约 52rpm 被最低 120rpm 抬高，实际线速度应高于目标 132%；旧文案反写「比目标低」。"
},
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  let __idx=0;
  for (const c of cases) {
    __idx++;
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ #" + __idx + " " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== ceramics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
