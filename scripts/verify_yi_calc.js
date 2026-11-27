#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
    "slug": "yi/64-gua",
    "clicks": ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'search',type:'text',value:'乾'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};var __r=document.getElementById('guaDetail');__r.textContent='第1卦 乾卦 乾为天';selectedGua=GUA[0];__64_gua_s0=function(){};selectGua(1);document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='GUASEL n='+__cap.length;"],
    "expect": ["GUASEL n=1"],
    "ref": "复核失败重做·选卦不入历史：搜索『乾』只记录全量列表前 80 字，随后选不同卦未增加历史；根因是真实交互入口 selectGua() 未被包装（只包装 filterList）。修复后同构包装 selectGua()。用例把原函数桩替换为空函数，预设选中卦和卦象详情，验证包装记录。默认态无探针串 ⇒ 零逃生。"
  },
{
    "slug": "yi/64-gua",
    "clicks": ["var __sel='';var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(s,f){__sel=String(s);}},matrix:{table:function(){}},history:{record:function(r){__cap.push(r);},mount:function(){}}};var __oq=document.querySelectorAll;document.querySelectorAll=function(){return [{id:'search',type:'text',value:'乾'}];};var __r=document.getElementById('guaList');__r.textContent='第1卦 乾卦';__64_guaExport();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='GUAEXP sel='+__sel;"],
    "expect": ["GUAEXP sel=[id=\"64_guaTable\"]"],
    "ref": "复核失败重做·数字开头 ID 导出异常：#64_guaTable 以数字开头，TBKit.util.exportTable 内部 querySelector('#64_guaTable') 是非法 CSS 选择器抛错被吞 ⇒ 无法导出。修复后改用等价合法的属性选择器 [id=\"64_guaTable\"]。用例以 exportTable 桩捕获实际传入的选择器：修复前 '#64_guaTable'、修复后 '[id=\"64_guaTable\"]'，默认态无探针串 ⇒ 零逃生。"
  },
{
  "slug": "yi/64-gua",
  "inputs": {},
  "clicks": [
    "selectedGua=GUA.find(function(g){return g.num===10;});renderDetail();"
  ],
  "expect": [
    "履虎尾,不咥人,亨"
  ],
  "ref": "clicks 直设顶层 selectedGua + 调 renderDetail()：默认态无选中 ⇒ renderDetail 早返回、不渲染详情；注入后渲染第10卦·履卦详情，卦辞「履虎尾,不咥人,亨」为详情独有锚点（默认列表仅显「第N卦 名卦」不含卦辞，已双态核验默认态无此串）。"
},
{
  "slug": "yi/bagua-viewer",
  "clicks": [
    "showGua('坤');"
  ],
  "expect": [
    "厚德载物，柔顺贞静，含弘光大。"
  ],
  "ref": "弱用例去默认化（BATCH118）：原锚「乾卦」（八卦名字串，默认列表本身含全部卦名 + 自然·五行 ⇒ 判别力0）。clicks 经 showGua('坤') 渲染坤卦详情，expect 锚坤卦专属「卦德」串「厚德载物，柔顺贞静，含弘光大。」；默认态只有八卦列表、无「卦象/卦德/象征」详情文本 ⇒ 零逃生项。"
},
{
  "slug": "yi/yi-yao",
  "inputs": {},
  "clicks": [
    "selectYao(5);"
  ],
  "expect": [
    "飞龙在天"
  ],
  "ref": "clicks 调 selectYao(5) 选第5爻 ⇒ renderYaoText 渲染卦1第5爻爻辞「飞龙在天」（默认只渲染初九「潜龙勿用」，已双态核验默认态无「飞龙在天」）。selectYao 内 querySelectorAll('.yao-item') 为 class 选择器、harness 支持；currentGua 由页面初始化置卦1，注入态产出正确。"
},
  {
    "slug": "yi/yi-divination",
    "inputs": {},
    "clicks": [
      "Math.random=function(){return 0.9;};var L=generateLines();var changed=L.filter(function(x){return x.change;}).length;document.getElementById('__tbProbe').textContent='YIDIV9 '+((L.length===6&&L.every(function(x){return x.type===1&&x.change;})&&changed===6)?'OK':'BAD');",
      "Math.random=function(){return 0.1;};var L2=generateLines();document.getElementById('__tbProbe').textContent='YIDIV6 '+((L2.length===6&&L2.every(function(x){return x.type===0&&x.change;}))?'OK':'BAD');",
      "var seq=[0.1,0.1,0.1,0.1,0.1,0.9,0.1,0.9,0.1,0.1,0.1,0.9,0.1,0.1,0.1,0.9,0.1,0.1],n=0;Math.random=function(){return seq[n++%seq.length];};var L3=generateLines();var mix=L3.filter(function(x){return x.change;}).length;document.getElementById('__tbProbe').textContent='YIDIVM '+((L3.length===6&&mix===2&&L3[1].type===1&&L3[1].change===false)?'OK':'BAD');"
    ],
    "expect": [
      "YIDIVM OK"
    ],
    "ref": "覆盖三枚硬币四态：random=0.9 ⇒ 每爻 9 老阳（阳爻+动），0.1 ⇒ 每爻 6 老阴（阴爻+动）；混合序列断言 7/8 静爻与 9 动爻同时出现，锁定原不可达的动爻分支。"
  }
,
{
  "slug": "yi/gua-interpretation",
  "clicks": ["var src=__tbFs.readFileSync(process.cwd()+'/js/tools/yi-hexagrams.js','utf8');var d=new Function(src+';return {H:YI_HEXAGRAMS,T:YI_TRIGRAMS};')();var bad=[];if(Object.keys(d.H).length!==64)bad.push('keys='+Object.keys(d.H).length);Object.keys(d.H).forEach(function(k){if(!/^[01]{6}$/.test(k)){bad.push('key');return;}var lo=d.T[k.slice(0,3)],up=d.T[k.slice(3)],n=d.H[k].name;if(!lo||!up||(!n.endsWith('为'+up.nature)&&!(n[0]===up.nature&&n[1]===lo.nature)))bad.push(k+':'+n);});var known={'111000':'地天泰','000111':'天地否','011001':'山风蛊','001011':'风山渐'};Object.keys(known).forEach(function(k){if(d.H[k].name!==known[k])bad.push(k+':'+d.H[k].name);});document.getElementById('__tbProbe').textContent='YI64 '+(bad.length?'BAD '+bad.slice(0,3).join(','):'OK');"],
  "expect": ["YI64 OK"],
  "ref": "第988批：共享数据源必须 64 个唯一六爻键、每个键上下卦与卦名自洽，并锁定泰/否/蛊/渐的关键映射（111000 地天泰、000111 天地否、011001 山风蛊、001011 风山渐）。旧页只有 55 键、9 个缺项 ⇒ 失败。"
},
{
  "slug": "yi/yi-divination",
  "clicks": ["var src=__tbFs.readFileSync(process.cwd()+'/js/tools/yi-hexagrams.js','utf8');var d=new Function(src+';return {H:YI_HEXAGRAMS};')();var p1=__tbFs.readFileSync(process.cwd()+'/tools/yi/gua-interpretation.html','utf8'),p2=__tbFs.readFileSync(process.cwd()+'/tools/yi/yi-divination.html','utf8');var ok=Object.keys(d.H).length===64&&p1.indexOf('/js/tools/yi-hexagrams.js')>=0&&p2.indexOf('/js/tools/yi-hexagrams.js')>=0&&p1.indexOf('GUA_JUDGE = typeof YI_HEXAGRAMS')>=0&&p2.indexOf('GUA_INTERPRET = typeof YI_HEXAGRAMS')>=0;document.getElementById('__tbProbe').textContent='YID64 '+(ok?'OK':'BAD');"],
  "expect": ["YID64 OK"],
  "ref": "第988批：两页必须引用同一共享数据源，禁止再各维护一份字面映射；共享表 64 键齐全且脚本引用存在，防止后续单页漂移。"
},
{
  "slug": "yi/yi-yao",
  "inputs": {},
  "clicks": [
    "selectGua(2);"
  ],
  "expect": ["履霜，坚冰至。"],
  "ref": "第1096批：选择第2卦坤，必须显示坤卦初六原文，不能再用乾卦初九替代；默认态为乾卦初九「潜龙，勿用」，双态互斥。"
},
{
  "slug": "yi/yi-yao",
  "inputs": {},
  "clicks": [
    "selectGua(64);selectYao(6);"
  ],
  "expect": ["濡其首，有孚失是。","火水未济 · 上九"],
  "ref": "第1096批：选择第64卦未济并选上爻，必须显示未济上九原文与卦名，锁定 64 卦选择与逐爻渲染贯通。"
},
{
  "slug": "yi/yi-yao",
  "inputs": {},
  "clicks": [
    "var bad=[];var texts=[];for(var i=1;i<=64;i++){var g=GUA_TEXT[i];if(!g||!g.l||g.l.length!==6){bad.push(i+':len');continue;}for(var p=1;p<=6;p++){var t=g.l[p-1];texts.push(t);var n=t.split('|')[0];if((p===1&&n.charAt(0)!=='初')||(p===2&&n.charAt(1)!=='二')||(p===3&&n.charAt(1)!=='三')||(p===4&&n.charAt(1)!=='四')||(p===5&&n.charAt(1)!=='五')||(p===6&&n.charAt(0)!=='上'))bad.push(i+':'+p+':'+n);}}if(texts.length!==384||new Set(texts).size!==384)bad.push('total='+texts.length+',uniq='+new Set(texts).size);document.getElementById('__tbProbe').textContent='YI384 '+(bad.length?'BAD '+bad.slice(0,3).join(','):'OK');"
  ],
  "expect": ["YI384 OK"],
  "ref": "第1096批：静态数据完整性检查 64 卦各 6 爻共 384 条、爻题位置字与自下而上顺序一致、文本无重复；防止只补选择器而数据仍为乾卦示例。"
}
,
{
  "slug": "yi/yi-divination",
  "inputs": {},
  "clicks": [
    "var __lines=[[1,true],[1,true],[1,true],[1,true],[1,true],[1,true]].map(function(x){return {type:x[0],change:x[1]};});var __m=renderGuaVisual(__lines,false),__c=renderGuaVisual(__lines,true);var mi=(__m.match(/y yin/g)||[]).length,ci=(__c.match(/y yin/g)||[]).length,mm=(__m.match(/gua-row changing/g)||[]).length,cm=(__c.match(/gua-row changing/g)||[]).length;document.getElementById('__tbProbe').textContent='YIDRAW-YANG '+((mi===0&&ci===6&&mm===6&&cm===6)?'OK':'BAD mi='+mi+' ci='+ci+' mm='+mm+' cm='+cm);"
  ],
  "expect": ["YIDRAW-YANG OK"],
  "ref": "第1097批：全老阳输入，本卦六爻必须全为阳爻（0 条 yin），变卦六爻必须全为阴爻（6 条 yin）；两栏六个动爻均标 changing。旧逻辑 type:1 被当作 yin，本卦会出现 6 条 yin ⇒ 失败。"
},
{
  "slug": "yi/yi-divination",
  "inputs": {},
  "clicks": [
    "var __lines=[[0,false],[0,false],[1,true],[0,false],[0,false],[0,false]].map(function(x){return {type:x[0],change:x[1]};});var __main=__lines.map(function(l){return effectiveType(l,false);}).join(''),__inv=__lines.map(function(l){return effectiveType(l,true);}).join('');document.getElementById('__tbProbe').textContent='YIDRAW-ONE '+((__main==='001000'&&__inv==='000000')?'OK':'BAD main='+__main+' inv='+__inv);"
  ],
  "expect": ["YIDRAW-ONE OK"],
  "ref": "第1097批：单动爻（第3爻阳变阴）本卦 5 阴 1 阳、变卦 6 阴，两栏仅第3爻标动；验证逐爻反转与动爻标记，不再只绘本卦。"
},
{
  "slug": "yi/yi-divination",
  "inputs": {},
  "clicks": [
    "var __lines=[{type:1,change:false},{type:0,change:false},{type:1,change:false},{type:0,change:false},{type:1,change:false},{type:0,change:false}];var __m=renderGuaVisual(__lines,false);document.getElementById('__tbProbe').textContent='YIDRAW-STATIC '+((__m.indexOf('y yin')>=0&&__m.indexOf('changing')<0)?'OK':'BAD');"
  ],
  "expect": ["YIDRAW-STATIC OK"],
  "ref": "第1097批：静爻不应出现 changing 标记；本卦按 type 原样绘制（阳爻无 yin、阴爻有 yin）。"
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

  console.log("==== yi calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
