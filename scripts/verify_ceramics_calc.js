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
  "expect": [
    "375.0"
  ],
  "ref": "auto-restore"
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
  "clicks": ["MATS.forEach(function(m){m.pct=0;});MATS[0].pct=90;calc();var h=String(document.getElementById('result').innerHTML);var w=document.getElementById('w_0');document.getElementById('__tbProbe').textContent='TB828G '+((h.indexOf('低于 100%')>=0&&h.indexOf('不再用输入总重估算加水')>=0&&h.indexOf('需加水量')<0&&w&&w.value==='—')?'OK':'BAD');"],
  "expect": ["TB828G OK"],
  "ref": "第828批：配方合计 90% 时旧实现仍按输入总重算加水与釉浆。现在 |sum−100|>0.5 即停算，列出补足/扣减百分点表并把称量输入置 —，不输出需加水量。"
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
}
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
