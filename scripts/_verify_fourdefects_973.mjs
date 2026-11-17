#!/usr/bin/env node
/**
 * 第 973 批专项：飞行时间60分进位、无刷/轻量相等与零值、CV/涨跌幅除零假合规。
 * OLD=git show HEAD 回放、NEW=工作区源码；独立 browser context + 外链 abort。
 */
import fs from 'node:fs'; import path from 'node:path'; import http from 'node:http';
import { execFileSync } from 'node:child_process'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const require=createRequire(import.meta.url); const puppeteer=require('puppeteer-core');
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pass=0,fail=0;
const ok=(n,c,e)=>{if(c){pass++;console.log('  ✅ '+n);}else{fail++;console.log('  ❌ '+n+(e?'  → '+e:''));}};
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8'};
const cache={}; // 973 基线固定为修复提交 1e1f8fbb11 的父提交 c18e6ba792
const oldSrc=rel=>(rel in cache)?cache[rel]:(cache[rel]=execFileSync('git',['show','c18e6ba792:'+rel],{cwd:ROOT,encoding:'utf8',maxBuffer:64*1024*1024}));
const CASES=[
  { name:'飞行时间60分进位', rel:'tools/science/calc-distance.html',
    code:"document.getElementById('lat1').value='40';document.getElementById('lon1').value='116';document.getElementById('lon2').value='116';document.getElementById('lat2').value='31.907';calc();return document.getElementById('res').textContent;",
    oldExpect:'小时 60 分', newExpect:'1 小时 0 分' },
  { name:'无刷轻量相等判定', rel:'tools/metalwork/wushua-zhinengyuqingliangduibijisuanqi.html',
    code:"document.getElementById('v0').value='80';document.getElementById('v1').value='80';calc();return document.getElementById('res').textContent;",
    oldExpect:'轻量路线优先', newExpect:'两方案持平' },
  { name:'CV均值零除零', rel:'tools/metalwork/analysis-cost-price-5.html',
    // 973 复核：当前页已拒绝负价格，改用全 0 非负序列覆盖零均值（mean=0、sd=0），仍触发 CV 除零
    code:"document.getElementById('data').value='0\\n0';calc();return document.getElementById('res').textContent;",
    oldCheck:t=>/变异系数（波动率）：0\.00%/.test(t), newCheck:t=>/变异系数（波动率）：—\/无法计算/.test(t) },
  { name:'负价格拒绝', rel:'tools/metalwork/analysis-cost-price-5.html',
    code:"document.getElementById('data').value='10\\n-10';calc();return document.getElementById('res').textContent;",
    oldCheck:t=>/变异系数（波动率）/.test(t), newCheck:t=>/价格须为非负有限数值/.test(t) },
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
