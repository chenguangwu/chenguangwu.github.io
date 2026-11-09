// Regression: the copied unit cost and displayed cost must agree; edits survive adding/removing rows.
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { JSDOM, VirtualConsole } from 'jsdom';
const head=process.argv.includes('--head');
const html=head?execFileSync('git',['show','HEAD:tools/agriculture/machinery-efficiency.html'],{encoding:'utf8'}):readFileSync('tools/agriculture/machinery-efficiency.html','utf8');
let copied='', message='';
const dom=new JSDOM(html,{url:'https://example.test/',runScripts:'dangerously',virtualConsole:new VirtualConsole(),beforeParse(w){
 w.i18nText=x=>x;
 w.ToolBox={setResult(id,h){w.document.getElementById(id).innerHTML=h;},showToast(s){message=s;},copyText(s){copied=s;},escHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}};
}});
const w=dom.window,d=w.document;
const set=(id,v)=>{d.getElementById(id).value=String(v)};
if (!process.argv.includes('--only-rows')) {
  w.calc(); w.copyResult();
  assert.match(d.getElementById('result').textContent,/7\.41/);
  assert.match(copied,/大型拖拉机: 效率22\.95亩\/h, 亩成本7\.41元/);
  set('laborCost',0);w.calc();w.copyResult();assert.match(copied,/亩成本5\.23元/);
  copied='';set('laborCost','');w.calc();w.copyResult();assert.equal(copied,'');assert.match(d.getElementById('result').textContent,/请输入人工费/);
}
if (!process.argv.includes('--only-copy')) {
  set('laborCost',50);set('name0','机器 "A" <img src=x onerror=alert(1)>');set('width0',4);set('speed0',7);set('eff0',88);set('fuel0',20);set('fp0',9);
  w.addMachine();assert.equal(d.getElementById('fuel0').value,'20');assert.equal(d.getElementById('width0').value,'4');
  assert.equal(d.getElementById('name0').value,'机器 "A" <img src=x onerror=alert(1)>');
  w.removeMachine();assert.equal(d.getElementById('fuel0').value,'20');assert.equal(d.getElementById('speed0').value,'7');assert.equal(d.getElementById('eff0').value,'88');assert.equal(d.getElementById('fp0').value,'9');
  assert.equal(d.querySelector('#result img'),null,'name must not become HTML');
}
dom.window.close();console.log('Machinery: copied cost, input preservation, safe name and invalid state passed');
