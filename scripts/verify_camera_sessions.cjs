const {createRequire}=require('module'),req=createRequire(process.cwd()+'/package.json'),{JSDOM,VirtualConsole}=req('jsdom'),fs=require('fs');
const flush=()=>new Promise(r=>setImmediate(r));let failed=0;
function check(name,ok){console.log((ok?'PASS ':'FAIL ')+name);if(!ok)failed++;}
function setup(){
  let rs=[],downloads=[],urls=[],vc=new VirtualConsole();vc.on('jsdomError',()=>{});
  const dom=new JSDOM(fs.readFileSync('tools/it/camera-recorder.html','utf8'),{url:'https://example.test/',runScripts:'dangerously',virtualConsole:vc,beforeParse(w){w.i18nText=k=>String(k);w.ToolBox={showToast(){}};w.TBKit={util:{isEn:()=>false},history:{record(){}}};w.navigator.mediaDevices={getUserMedia:async()=>({getTracks:()=>[{stop(){}}]})};w.HTMLMediaElement.prototype.play=()=>Promise.resolve();w.MediaRecorder=class{constructor(){this.state='inactive';rs.push(this)}start(){this.state='recording'}stop(){this.state='inactive'}};w.URL.createObjectURL=b=>(urls.push(b),'blob:test');w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){downloads.push(this.download)}}});
  return {w:dom.window,rs,downloads,urls};
}
(async()=>{
  {const {w,rs,downloads,urls}=setup();w.startRec();await flush();rs[0].ondataavailable({data:new w.Blob(['old'])});w.stopStream();w.startRec();await flush();rs[1].ondataavailable({data:new w.Blob(['newer'])});rs[0].onstop();check('旧关闭回调不下载',downloads.length===0);check('旧关闭回调不覆盖新录像提示',w.document.getElementById('result').textContent.includes('正在录制'));w.stopRec(true);rs[1].onstop();check('新录像单次下载且内容独立',downloads.length===1&&urls[0].size===5);w.close();}
  {const {w,rs,downloads,urls}=setup();w.startRec();await flush();rs[0].ondataavailable({data:new w.Blob(['old'])});w.stopRec(true);w.startRec();await flush();rs[1].ondataavailable({data:new w.Blob(['newer'])});w.stopStream();rs[1].onstop();const latest=w.document.getElementById('result').textContent;rs[0].onstop();check('旧保存意图不受新关闭影响',downloads.length===1&&urls[0].size===3);check('旧保存回调不覆盖新关闭提示',w.document.getElementById('result').textContent===latest);w.close();}
  {const {w,rs,downloads,urls}=setup();w.startRec();await flush();rs[0].ondataavailable({data:new w.Blob(['old'])});w.stopStream();w.startRec();await flush();rs[1].ondataavailable({data:new w.Blob(['newer'])});w.stopRec(true);rs[0].onstop();check('旧关闭回调晚于新保存时不下载',downloads.length===0);rs[1].onstop();check('新保存回调下载正确数据',downloads.length===1&&urls[0].size===5);w.close();}
  process.exit(failed?1:0);
})();
