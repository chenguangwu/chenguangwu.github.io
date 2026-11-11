import fs from 'fs';
import { JSDOM } from 'jsdom';
const html=fs.readFileSync('tools/it/timestamp-converter.html','utf8');
const dom=new JSDOM(html,{runScripts:'dangerously',beforeParse(w){
  w.i18nText=(k,f)=>f||k;
  w.ToolBox={showToast(){},copyText(){},toggleToolTheme(){},escHtml(x){return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}};
  w.TBKit={util:{isEn:()=>false},history:{add(){},list(){return[];}},chart:{},matrix:{}};
}});
const w=dom.window,d=w.document;
const checks=[];
function check(n,ok,x){checks.push([n,ok]);console.log((ok?'PASS ':'FAIL ')+n+(x?' | '+x:''));}
function diff(a,b){
  d.getElementById('diffStart').value=a;
  d.getElementById('diffEnd').value=b;
  w.calculateDiff();
  return d.getElementById('calcResult2').textContent.replace(/\s+/g,' ');
}
// IT-N45: 跨年仅1天，整年应为0而非1
let r=diff('2025-12-31','2026-01-01');
check('跨年1天-整年数为0', /相差整年数: 0 年/.test(r), r.match(/相差整年数[^相]*/)?.[0]);
check('跨年1天-整月数为0', /相差整月数: 0 个月/.test(r));
check('跨年1天-天数为1', /相差天数: 1 天/.test(r));
// 跨月仅1天
r=diff('2026-01-31','2026-02-01');
check('跨月1天-整月数为0', /相差整月数: 0 个月/.test(r), r.match(/相差整月数[^相]*/)?.[0]);
check('跨月1天-天数为1', /相差天数: 1 天/.test(r));
// 防回归: 真正跨1整年
r=diff('2025-01-01','2026-01-01');
check('整1年-整年数为1', /相差整年数: 1 年/.test(r));
// 防回归: 真正跨1整月
r=diff('2026-01-01','2026-02-01');
check('整1月-整月数为1', /相差整月数: 1 个月/.test(r));
dom.window.close();
const failed=checks.filter(c=>!c[1]).length;
console.log('\nBATCH148 checks='+checks.length+' failed='+failed);
process.exit(failed?1:0);
