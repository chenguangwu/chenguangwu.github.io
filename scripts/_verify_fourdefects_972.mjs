#!/usr/bin/env node
/**
 * 第 972 批专项：二次方程复根符号、双销并联量纲、单摆重力常量与引据矛盾。
 * OLD=固定修复前基线回放、NEW=工作区源码；独立 browser context + 外链 abort。
 */
import fs from 'node:fs'; import path from 'node:path'; import http from 'node:http';
import { execFileSync } from 'node:child_process'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const require=createRequire(import.meta.url); const puppeteer=require('puppeteer-core');
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pass=0,fail=0;
const ok=(n,c,e)=>{if(c){pass++;console.log('  ✅ '+n);}else{fail++;console.log('  ❌ '+n+(e?'  → '+e:''));}};
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8'};
const cache={}; // 972 基线固定为修复提交 c18e6ba792 的父提交 5a2659e7ac
const oldSrc=rel=>(rel in cache)?cache[rel]:(cache[rel]=execFileSync('git',['show','5a2659e7ac:'+rel],{cwd:ROOT,encoding:'utf8',maxBuffer:64*1024*1024}));
// 精确取输出：二次方程用 solve() 后 roots 渲染区，双销用结果卡，单摆用输入 value + 结果
const CASES=[
  { name:'二次方程复根符号', rel:'tools/science/quadratic-equation.html',
    code:"document.getElementById('a').value='-1';document.getElementById('b').value='0';document.getElementById('c').value='-1';solve();return (document.getElementById('solution')||document.getElementById('result')||document.body).textContent;",
    oldCheck:t=>/0 \+ -1i/.test(t)||/\+ -\d/.test(t), newCheck:t=>/1\.000i|1i/.test(t)&&!/\+ -/.test(t) },
  { name:'双销并联直径量纲', rel:'tools/machinery/xiao-dingwei-lianjie-chicun.html',
    code:"document.getElementById('v0').value='20';document.getElementById('v1').value='120';calc();return document.getElementById('res').textContent;",
    oldExpect:'29.135', newExpect:'10.301' },
  { name:'单摆重力常量', rel:'tools/science/pendulum-period.html',
    code:"return JSON.stringify({g:document.getElementById('g').value,res:(document.getElementById('result')||{}).textContent||''});",
    oldExpect:'9.81', newExpect:'9.80665' },
];
(async()=>{
  const server=http.createServer((req,res)=>{const p=decodeURIComponent(req.url.split('?')[0]);const f=path.join(ROOT,p);if(!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);res.end('nf');return;}res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(res);});
  await new Promise(r=>server.listen(0,'127.0.0.1',r)); const port=server.address().port;
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
  try{
    for(const c of CASES){
      const url='http://127.0.0.1:'+port+'/'+c.rel;
      for(const phase of ['OLD','NEW']){
        const ctx=await browser.createBrowserContext();
        try{
          const page=await ctx.newPage(); await page.setRequestInterception(true);
          page.on('request',r=>{const u=r.url();if(phase==='OLD'&&u.endsWith('/'+c.rel))r.respond({status:200,contentType:'text/html; charset=utf-8',body:oldSrc(c.rel)});else if(/^https?:\/\/(?!127\.0\.0\.1)/.test(u))r.abort();else r.continue();});
          const errs=[];page.on('pageerror',e=>errs.push(String(e)));
          await page.goto(url,{waitUntil:'domcontentloaded'}).catch(()=>{});
          const txt=String(await page.evaluate(new Function(c.code)));
          if(c.oldCheck||c.newCheck){
            const check=phase==='OLD'?c.oldCheck:c.newCheck;
            ok(c.name+' '+(phase==='OLD'?'旧版缺陷可复现':'新版正确值'),check(txt),'片段='+txt.replace(/\s+/g,' ').slice(0,180));
            if(phase==='NEW') ok(c.name+' 无脚本异常',errs.length===0,errs.join(' | '));
          }else{
            const expect=phase==='OLD'?c.oldExpect:c.newExpect;
            if(phase==='OLD') ok(c.name+' 旧版缺陷可复现',txt.indexOf(expect)>=0,'缺旧串 '+expect+'；实际='+txt.replace(/\s+/g,' ').slice(0,180));
            else{ ok(c.name+' 新版正确值',txt.indexOf(expect)>=0,'缺正确串 '+expect+'；实际='+txt.replace(/\s+/g,' ').slice(0,200));
                  ok(c.name+' 无脚本异常',errs.length===0,errs.join(' | ')); }
          }
        }catch(e){ok(c.name+' '+phase,false,String(e));}finally{await ctx.close();}
      }
    }
  }finally{await browser.close();server.close();}
  console.log('\n结果：'+pass+' PASS / '+fail+' FAIL'); process.exit(fail?1:0);
})().catch(e=>{console.error(e);process.exit(2);});
