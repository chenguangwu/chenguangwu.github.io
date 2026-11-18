#!/usr/bin/env node
/** 第 971 批专项：AI 摘要短句文本 0/0=NaN 假合规。OLD=固定修复前基线回放、NEW=工作区。 */
import fs from 'node:fs'; import path from 'node:path'; import http from 'node:http';
import { execFileSync } from 'node:child_process'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const require=createRequire(import.meta.url); const puppeteer=require('puppeteer-core');
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pass=0,fail=0;
const ok=(n,c,e)=>{if(c){pass++;console.log('  ✅ '+n);}else{fail++;console.log('  ❌ '+n+(e?'  → '+e:''));}};
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8'};
const rel='tools/ai/ai-text-summarizer.html';
const old=execFileSync('git',['show','cfb947172c:'+rel],{cwd:ROOT,encoding:'utf8',maxBuffer:64*1024*1024}); // 971 基线固定为修复提交 5a2659e7ac 的父提交
const code="document.getElementById('input').value='天很蓝。'.repeat(13);summarize();return {stat:document.getElementById('stat').textContent,result:document.getElementById('result').textContent};";
(async()=>{
  const server=http.createServer((req,res)=>{const p=decodeURIComponent(req.url.split('?')[0]);const f=path.join(ROOT,p);if(!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);res.end('nf');return;}res.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(res);});
  await new Promise(r=>server.listen(0,'127.0.0.1',r)); const port=server.address().port;
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
  const url='http://127.0.0.1:'+port+'/'+rel;
  for(const phase of ['OLD','NEW']){
    const ctx=await browser.createBrowserContext();
    try{
      const page=await ctx.newPage(); await page.setRequestInterception(true);
      page.on('request',r=>{const u=r.url();if(phase==='OLD'&&u.endsWith('/'+rel))r.respond({status:200,contentType:'text/html; charset=utf-8',body:old});else if(/^https?:\/\/(?!127\.0\.0\.1)/.test(u))r.abort();else r.continue();});
      const errs=[];page.on('pageerror',e=>errs.push(String(e)));
      await page.goto(url,{waitUntil:'domcontentloaded'}).catch(()=>{});
      const out=await page.evaluate(new Function(code));
      const txt=String(out.stat+' '+out.result);
      if(phase==='OLD') ok('旧版缺陷可复现（短句被判无效）',txt.indexOf('计算结果含无效值')>=0,'实际='+txt.replace(/\s+/g,' ').slice(0,160));
      else{
        ok('新版正常出句数',txt.indexOf('原句数： 13')>=0||txt.indexOf('原句数：13')>=0,'实际='+txt.replace(/\s+/g,' ').slice(0,160));
        ok('新版压缩比 23%',txt.indexOf('23%')>=0,'实际='+txt.replace(/\s+/g,' ').slice(0,160));
        ok('新版无 NaN 错误',txt.indexOf('计算结果含无效值')<0,txt.replace(/\s+/g,' ').slice(0,120));
        ok('无脚本异常',errs.length===0,errs.join(' | '));
      }
    }catch(e){ok(phase,false,String(e));}finally{await ctx.close();}
  }
  await browser.close(); server.close();
  console.log('\n结果：'+pass+' PASS / '+fail+' FAIL'); process.exit(fail?1:0);
})().catch(e=>{console.error(e);process.exit(2);});
