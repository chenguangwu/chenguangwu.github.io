import fs from 'fs';
import { JSDOM } from 'jsdom';
const html = fs.readFileSync('tools/it/env-generator.html','utf8');
let copied=null;
const dom = new JSDOM(html, { runScripts:'dangerously', beforeParse(w){
  w.i18nText=(k,f)=>f||k;
  w.ToolBox={
    showToast(){}, copyText(t){copied=t;}, downloadText(){},
    escHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');},
    toggleToolTheme(){}
  };
}});
const w=dom.window, d=w.document;
const checks=[];
function check(n,ok,extra){checks.push([n,ok]);console.log((ok?'PASS ':'FAIL ')+n+(extra?' | '+extra:''));}
function add(key,val,type){
  d.getElementById('keyInput').value=key;
  d.getElementById('valInput').value=val;
  d.getElementById('typeInput').value=type||'string';
  w.addVariable();
}
const pv=d.getElementById('previewCode');

// ===== 缺陷1：无效值守卫须清空 dataset.raw，杜绝复制/下载旧配置 =====
add('GOOD','hello','string');
const raw1=pv.dataset.raw||'';
check('有效态dataset.raw写入配置', raw1.includes('GOOD=hello'));
add('BAD','NaN','string');  // env 输出含独立 NaN → 守卫触发
const prev2=pv.innerHTML;
check('无效态预览显示警告', prev2.includes('无效值'));
const raw2=pv.dataset.raw||'';
check('无效态dataset.raw已清空', raw2==='', 'raw2='+JSON.stringify(raw2.slice(-50)));
copied=null; w.copyResult();
check('无效态复制不含旧配置', !copied || (!copied.includes('GOOD') && !copied.includes('BAD')), 'copied='+JSON.stringify((copied||'').slice(-60)));

// ===== 缺陷2：JSON number 非法值不伪造为 0 =====
w.deleteVar(0); w.deleteVar(0);  // 清 GOOD/BAD
d.getElementById('formatSelect').value='json';

// 2a 非法字符串值 abc → 保留字符串，不变 0
add('BADNUM','abc','number');
w.generatePreview();
let raw=pv.dataset.raw||'';
check('JSON非法number不伪造为0', !/"BADNUM"\s*:\s*0/.test(raw), 'raw='+JSON.stringify(raw));
check('JSON非法number保留原值', /"BADNUM"\s*:\s*"abc"/.test(raw));

// 2b 空值 → 保留空字符串，不变 0
w.deleteVar(0); add('EMPTYNUM','','number'); w.generatePreview();
raw=pv.dataset.raw||'';
check('JSON空number不伪造为0', !/"EMPTYNUM"\s*:\s*0/.test(raw), 'raw='+JSON.stringify(raw));

// 2c 合法数字仍正常转 number（防回归）
w.deleteVar(0); add('OKNUM','42','number'); w.generatePreview();
raw=pv.dataset.raw||'';
check('JSON合法number仍转数字', /"OKNUM"\s*:\s*42(?:\D|$)/.test(raw), 'raw='+JSON.stringify(raw));

dom.window.close();
const failed=checks.filter(c=>!c[1]).length;
console.log('\nBATCH145 checks='+checks.length+' failed='+failed);
process.exit(failed?1:0);
