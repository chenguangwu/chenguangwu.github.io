// A positive item without participants must not disappear; selection follows the original person on edits.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {JSDOM,VirtualConsole} from 'jsdom';
const head=process.argv.includes('--head');
const html=head?execFileSync('git',['show','HEAD:tools/life/bill-splitter.html'],{encoding:'utf8'}):readFileSync('tools/life/bill-splitter.html','utf8');
const dom=new JSDOM(html,{url:'https://example.test/',runScripts:'dangerously',virtualConsole:new VirtualConsole(),beforeParse(w){w.i18nText=x=>x;w.ToolBox={showToast(){},copyText(){}};}});
const w=dom.window,d=w.document;w.renderAdvPersons();
const checks=()=>Array.from(d.querySelectorAll('#items-list .item-row:first-child .item-persons input'));
const row=d.querySelector('#items-list .item-row'), amt=row.querySelector('input[type=number]');
if(!process.argv.includes('--only-selections')){
 amt.value='100';w.calcAdvanced();assert.match(d.getElementById('adv-result').textContent,/总消费.*100\.00/);
 const oldHistory=w.localStorage.getItem('bill_splitter_history');
 checks().forEach(c=>c.checked=false);w.calcAdvanced();
 assert.match(d.getElementById('adv-result').textContent,/第\s*1\s*行.*选择.*参与人/);
 assert.doesNotMatch(d.getElementById('adv-result').textContent,/总消费/);
 assert.equal(w.localStorage.getItem('bill_splitter_history'),oldHistory,'no new record on error');
 amt.value='0';w.calcAdvanced();assert.match(d.getElementById('adv-result').textContent,/总消费.*0\.00/);
 amt.value='100';w.TBKit={util:{isEn:()=>true}};w.calcAdvanced();assert.match(d.getElementById('adv-result').textContent,/Select at least one participant/);w.invalidateAdvanced();assert.match(d.getElementById('adv-result').textContent,/Please recalculate/);delete w.TBKit;
}
if(!process.argv.includes('--only-unassigned')){
 checks().forEach((c,i)=>c.checked=(i===0||i===2));
 const person=d.querySelector('#adv-persons-list input');person.value='甲';person.dispatchEvent(new w.Event('change',{bubbles:true}));
 assert.deepEqual(checks().map(c=>c.checked),[true,false,true,false]);
 w.addItem();assert.deepEqual(checks().map(c=>c.checked),[true,false,true,false]);
 w.removeAdvPerson(0);assert.deepEqual(checks().map(c=>c.checked),[false,true,false]);
 w.addAdvPerson();assert.deepEqual(checks().map(c=>c.checked),[false,true,false,true]);
 assert.match(d.getElementById('adv-result').textContent,/重新计算/);
}
dom.window.close();console.log('Bill splitting: no unassigned amounts and selections preserved');
