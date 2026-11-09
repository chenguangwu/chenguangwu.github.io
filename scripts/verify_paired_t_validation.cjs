#!/usr/bin/env node
// Execute the page's own calculator and enhanced results against a browser-like DOM.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const html = fs.readFileSync(path.join(__dirname, '../tools/statistics/paired-t-test.html'), 'utf8');
function load(lang) {
  const dom = new JSDOM(html, { url:'https://toolbox.local/tools/statistics/paired-t-test.html?lang='+lang, runScripts:'outside-only' });
  const w = dom.window, doc = w.document;
  w.ToolBox = { setResult(id, value) { doc.getElementById(id).innerHTML=String(value); } };
  let exports=0, records=0;
  w.TBKit = {
    util: { isEn:()=>lang==='en-US', tP2:()=>0.006079, tCrit:()=>2.145, diffBox(sel){doc.querySelector(sel).textContent='Previous result comparison';}, exportTable(){exports++;} },
    matrix: { table(sel, data){doc.querySelector(sel).textContent=data.rows.map(row=>row.join(' ')).join(' | ');} },
    history: { record(){records++;}, mount(){} }, preset:{bar(){}}
  };
  const start=html.indexOf('function __tbInputGuard('), end=html.indexOf('</script>',start);
  assert(start>=0&&end>start,'calculator script not found');
  w.eval(html.slice(start,end));
  return {w,doc,dom,getExports:()=>exports,getRecords:()=>records};
}
const x=load('zh-CN'), {w,doc}=x;
w.calcTool();
assert(doc.getElementById('result').textContent.includes('3.2275'));
assert(doc.getElementById('result').textContent.includes('0.0061'));
assert(doc.getElementById('ptTable').textContent.includes('0.006079'));
for(const n of ['0','1','2.5','-1']) {
  w.calcTool(); // Make the previous valid detail visible before the transition.
  doc.getElementById('n').value=n;
  const beforeRecords=x.getRecords();
  w.calcTool();
  assert(!doc.getElementById('result').textContent.includes('p 值'),`invalid n=${n} produced a p value`);
  assert.strictEqual(doc.getElementById('ptTable').textContent,'',`stale table for n=${n}`);
  assert.strictEqual(doc.getElementById('ptDiff').textContent,'',`stale comparison for n=${n}`);
  assert.strictEqual(x.getRecords(),beforeRecords,`invalid n=${n} recorded history`);
  w.__ptExport();assert.strictEqual(x.getExports(),0,`invalid n=${n} exported data`);
  doc.getElementById('n').value='15';
}
doc.getElementById('sd').value='-3';w.calcTool();assert(doc.getElementById('result').textContent.includes('须大于 0'));
doc.getElementById('sd').value='3';doc.getElementById('dbar').value='0';doc.getElementById('n').value='2';w.calcTool();
assert(doc.getElementById('result').textContent.includes('1.0000'),'zero mean is a valid input');
assert(doc.getElementById('ptTable').textContent.includes('自由度 df 1'));
const en=load('en-US');en.w.calcTool();
assert(en.doc.getElementById('result').textContent.includes('t statistic'));
assert(en.doc.getElementById('result').textContent.includes('Two-sided p value'));
en.doc.getElementById('n').value='1';en.w.calcTool();
assert(en.doc.getElementById('result').textContent.includes('integer of at least 2'));
en.dom.window.close();x.dom.window.close();
console.log('paired t test: invalid counts, stale results/export, positive SD, valid zero and English checks passed');
