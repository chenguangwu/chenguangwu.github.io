import fs from 'fs';
import { JSDOM } from 'jsdom';
const html = fs.readFileSync('tools/it/html-tags.html','utf8');
let exported = null;
const dom = new JSDOM(html, { runScripts:'dangerously', beforeParse(w){
  w.ToolBox = { showToast(){}, toggleToolTheme(){} };
  w.TBKit = { util:{
    isEn:()=>false,
    exportTable(host, name){
      const rows=[];
      const box=w.document.querySelector(host);
      box.querySelectorAll('tr').forEach(tr=>{
        const line=[]; tr.querySelectorAll('th,td').forEach(td=>line.push((td.textContent||'').trim()));
        if(line.length) rows.push(line);
      });
      exported={name,rows}; return true;
    }
  }};
}});
const w=dom.window;
const checks=[];
function check(n,ok,extra){checks.push([n,ok]);console.log((ok?'PASS ':'FAIL ')+n+(extra?' | '+extra:''));}

w.__htgExport();
const rows=exported?.rows||[];
check('导出表非空(121数据行+表头)', rows.length===122, 'rows='+rows.length);
const byTag={};
for(const r of rows) if(r.length>=7) byTag[r[0]]=r[6];

// 核心缺陷：<a> 标签示例导出必须保留标签字面，不能只剩可见文字「链接」
check('a标签示例保留href属性', (byTag['a']||'').includes('<a href='), 'a='+JSON.stringify(byTag['a']));
check('a标签示例保留闭合标签', (byTag['a']||'').includes('</a>'));
check('a标签示例不再只剩可见文字', (byTag['a']||'').trim()!=='链接');
// nav 含两个超链接，导出须保留两个 <a>
check('nav示例保留两个超链接', ((byTag['nav']||'').match(/<a /g)||[]).length===2, 'nav='+JSON.stringify(byTag['nav']));
check('aside示例保留h3标签', (byTag['aside']||'').includes('<h3>'));
// desc/attrs 普通字段仍正确导出
check('普通字段未受影响', (byTag['p']||'').includes('这是一段文字'));

dom.window.close();
const failed=checks.filter(c=>!c[1]).length;
console.log('\nBATCH144 checks='+checks.length+' failed='+failed);
process.exit(failed?1:0);
