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
function smart(v){
  d.getElementById('smartInput').value=v;
  w.smartConvert();
  return {
    hint:d.getElementById('smartHint').textContent,
    ms:d.getElementById('timestampMs').value,
    date:d.getElementById('dateInput').value
  };
}
// IT-N43 核心回归：12 位毫秒戳 2000-01-01
let r=smart('946684800000');
check('12位判为毫秒', r.hint.includes('毫秒时间戳（12 位）'), r.hint.slice(0,60));
check('不再输出31969年', !/31969/.test(r.hint+r.date));
check('日期正确2000-01-01', r.date.includes('2000-01-01'), 'date='+r.date);
check('毫秒值正确', r.ms==='946684800000', 'ms='+r.ms);
// 13 位毫秒戳仍正确（防回归）
r=smart('1700000000000');
check('13位毫秒仍正确', r.hint.includes('毫秒时间戳（13 位）') && (r.date.includes('2023-11-14')||r.date.includes('2023-11-15')), 'date='+r.date);
// 10 位秒戳仍判秒（防回归）
r=smart('1700000000');
check('10位秒戳仍判秒', r.hint.includes('秒时间戳（10 位）'), 'hint='+r.hint.slice(0,50));
dom.window.close();
const failed=checks.filter(c=>!c[1]).length;
console.log('\nBATCH147 checks='+checks.length+' failed='+failed);
process.exit(failed?1:0);
