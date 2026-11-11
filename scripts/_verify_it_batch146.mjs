import fs from 'fs';
import { JSDOM } from 'jsdom';
const html = fs.readFileSync('tools/it/http-status.html','utf8');
let exportedRows=null;
const dom = new JSDOM(html, { runScripts:'dangerously', beforeParse(w){
  w.ToolBox={ showToast(){}, toggleToolTheme(){} };
  w.TBKit={
    util:{ isEn:()=>false, exportTable(host){
      const rows=[]; const box=w.document.querySelector(host);
      box.querySelectorAll('tr').forEach(tr=>{const l=[];tr.querySelectorAll('th,td').forEach(c=>l.push((c.textContent||'').trim()));if(l.length)rows.push(l);});
      exportedRows=rows; return true;
    }},
    chart:{ bar(){} }
  };
}});
const w=dom.window, d=w.document;
const checks=[];
function check(n,ok,extra){checks.push([n,ok]);console.log((ok?'PASS ':'FAIL ')+n+(extra?' | '+extra:''));}
const t=d.getElementById('httpTable');

// 导出全部：CSV 内容仍含合计行（防回归），且导出后表格恢复隐藏
w.__httpExport();
check('导出CSV含合计行', !!exportedRows && exportedRows.some(r=>r[0]==='合计'));
check('导出CSV含状态码数据', !!exportedRows && exportedRows.length>=30, 'rows='+(exportedRows?.length));
check('导出后表格恢复隐藏', t.style.display==='none', 'display='+t.style.display);

// 筛选无匹配：表格隐藏、无遗留行、无表头
d.getElementById('search').value='zzzznotfound';
w.filterStatus();
check('空筛选表格隐藏', t.style.display==='none', 'display='+t.style.display);
check('空筛选无遗留数据行', t.querySelectorAll('tbody tr').length===0);
check('空筛选表头清空', (t.querySelector('thead')?.innerHTML||'').trim()==='');

// 筛选有匹配：表格隐藏、无合计行（合计只属于导出）
d.getElementById('search').value='200';
w.filterStatus();
check('有匹配筛选表格仍隐藏', t.style.display==='none', 'display='+t.style.display);
check('筛选结果无遗留合计行', ![...t.querySelectorAll('tbody tr')].some(r=>r.textContent.includes('合计')));
check('筛选结果数据行正确', t.querySelectorAll('tbody tr').length>=1 && t.querySelectorAll('tbody tr').length<32);

// 再次导出当前筛选：仍能导出含合计的 CSV
exportedRows=null;
w.__httpExport();
check('再导出CSV仍含合计', !!exportedRows && exportedRows.some(r=>r[0]==='合计'));
check('再导出后仍隐藏', t.style.display==='none');

dom.window.close();
const failed=checks.filter(c=>!c[1]).length;
console.log('\nBATCH146 checks='+checks.length+' failed='+failed);
process.exit(failed?1:0);
