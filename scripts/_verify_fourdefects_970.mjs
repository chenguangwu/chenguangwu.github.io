#!/usr/bin/env node
/**
 * 第 970 批专项：传感器覆盖面积多乘距离、DPMO=0 误拒、曝光偏差单元格括号错。
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
const cache={}; // 970 基线固定为修复提交 cfb947172c 的父提交
const oldSrc=rel=>(rel in cache)?cache[rel]:(cache[rel]=execFileSync('git',['show','060ecc5636:'+rel],{cwd:ROOT,encoding:'utf8',maxBuffer:64*1024*1024}));
const CASES=[
  { name:'传感器覆盖面积多乘距离', rel:'tools/general/detector-16.html',
    code:"calc();return document.getElementById('res').textContent;",
    oldExpect:'22.7 m²', newExpect:'6.5 m²' },
  { name:'DPMO=0误拒', rel:'tools/process/sigma-level.html',
    code:"document.getElementById('dpmo').value='0';calcTool();return document.getElementById('result').textContent;",
    oldExpect:'不能为 0', newExpect:'≥ 6σ' },
  { name:'曝光偏差单元格括号', rel:'tools/photo2/exposure-triangle.html',
    code:"calcEV();calcEquivalent();return document.getElementById('result').innerHTML;",
    // 旧版括号错：颜色字符串拼在比较后，恒取 var(--warning) 且偏差单元格丢失 color 前缀
    oldCheck:txt=>txt.indexOf('color:var(--success)')<0,
    newCheck:txt=>txt.indexOf('color:var(--success)')>=0 && /\+\d/.test(txt) },
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
            ok(c.name+' '+(phase==='OLD'?'旧版缺陷可复现':'新版正确值'),check(txt),'片段='+txt.replace(/\s+/g,' ').slice(0,200));
            if(phase==='NEW') ok(c.name+' 无脚本异常',errs.length===0,errs.join(' | '));
          }else{
            const expect=phase==='OLD'?c.oldExpect:c.newExpect;
            if(phase==='OLD') ok(c.name+' 旧版缺陷可复现',txt.indexOf(expect)>=0,'缺旧串 '+expect+'；实际='+txt.replace(/\s+/g,' ').slice(0,160));
            else{ ok(c.name+' 新版正确值',txt.indexOf(expect)>=0,'缺正确串 '+expect+'；实际='+txt.replace(/\s+/g,' ').slice(0,200));
                  ok(c.name+' 无脚本异常',errs.length===0,errs.join(' | ')); }
          }
        }catch(e){ok(c.name+' '+phase,false,String(e));}finally{await ctx.close();}
      }
    }
  }finally{await browser.close();server.close();}
  console.log('\n结果：'+pass+' PASS / '+fail+' FAIL'); process.exit(fail?1:0);
})().catch(e=>{console.error(e);process.exit(2);});
