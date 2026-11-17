#!/usr/bin/env node
/**
 * 第 969 批专项：车损险万元当元、扭转常数立方错边、功率密度多拼k、calc-stats 数据0开头误拒。
 * OLD=git show HEAD 回放、NEW=工作区源码；独立 browser context + 外链 abort。
 */
import fs from 'node:fs'; import path from 'node:path'; import http from 'node:http';
import { execFileSync } from 'node:child_process'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url); const puppeteer = require('puppeteer-core');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pass=0, fail=0;
const ok=(n,c,e)=>{if(c){pass++;console.log('  ✅ '+n);}else{fail++;console.log('  ❌ '+n+(e?'  → '+e:''));}};
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8'};
const cache={}; // 969 基线固定为修复提交 060ecc5636 的父提交
const oldSrc=rel=>(rel in cache)?cache[rel]:(cache[rel]=execFileSync('git',['show','dac4032970:'+rel],{cwd:ROOT,encoding:'utf8',maxBuffer:64*1024*1024}));
const CASES=[
  { name:'车损险万元当元', rel:'tools/automotive/insurance-premium-estimator.html',
    code:"document.getElementById('price').value='20';document.getElementById('ncd').value='0.7';calc();return document.getElementById('result').textContent;",
    oldExpect:'车损 0 +', newExpect:'车损 1680 +' },
  { name:'扭转常数立方短边', rel:'tools/automotive/analysis-strength.html',
    code:"calc();return (document.getElementById('distGrid')||{}).textContent||'';",
    oldExpect:'32641 N·m/°', newExpect:'8160 N·m/°' },
  { name:'功率密度多拼k', rel:'tools/general/power-focal.html',
    code:"calc();return document.getElementById('res').textContent;",
    oldExpect:'127.3k', newExpect:'127.3功率密度（kW/mm²）' },
  { name:'calc-stats数据0开头', rel:'tools/science/calc-stats.html',
    code:"document.getElementById('data').value='0,1,2,3,4';if(typeof calc==='function')calc();return (document.getElementById('res')||{}).textContent||'';",
    oldExpect:'是本计算的分母，不能为 0', newExpect:'均值2.0000' },
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
          if(phase==='OLD') ok(c.name+' 旧版缺陷可复现',txt.indexOf(c.oldExpect)>=0,'缺旧缺陷串 '+c.oldExpect+'；实际='+txt.replace(/\s+/g,' ').slice(0,160));
          else{
            ok(c.name+' 新版正确值',txt.indexOf(c.newExpect)>=0,'缺正确串 '+c.newExpect+'；实际='+txt.replace(/\s+/g,' ').slice(0,200));
            ok(c.name+' 新版缺陷串消失',txt.indexOf(c.oldExpect)<0,'旧串仍在 '+c.oldExpect);
            ok(c.name+' 无脚本异常',errs.length===0,errs.join(' | '));
          }
        }catch(e){ok(c.name+' '+phase,false,String(e));}finally{await ctx.close();}
      }
    }
  }finally{await browser.close();server.close();}
  console.log('\n结果：'+pass+' PASS / '+fail+' FAIL'); process.exit(fail?1:0);
})().catch(e=>{console.error(e);process.exit(2);});
