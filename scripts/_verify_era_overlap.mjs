// Compare the same historical intervals in both orders, including containment and boundary-only contact.
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { JSDOM, VirtualConsole } from 'jsdom';
const html = process.argv.includes('--head') ? execFileSync('git',['show','HEAD:tools/museum/era-comparator.html'],{encoding:'utf8'}) : readFileSync('tools/museum/era-comparator.html','utf8');
const dom = new JSDOM(html,{url:'https://example.test/',runScripts:'dangerously',virtualConsole:new VirtualConsole()});
const w=dom.window, d=w.document;
function compare(a,b){d.getElementById('era1').value=String(a);d.getElementById('era2').value=String(b);w.compare();return d.getElementById('result').textContent.replace(/\s+/g,' ');}
for(const [a,b] of [[5,6],[6,5]]) assert.match(compare(a,b),/14 年的并存期/);
assert.match(compare(5,6),/266 年\s*–\s*280 年/);
assert.match(compare(5,5),/60 年的并存期/);
w.eval('ERAS[0].s=-2000; ERAS[0].e=-1000; ERAS[1].s=-1800; ERAS[1].e=-1600');
for(const [a,b] of [[0,1],[1,0]]) assert.match(compare(a,b),/200 年的并存期/);
assert.doesNotMatch(compare(11,12),/并存期/); // Yuan ends as Ming starts.
assert.doesNotMatch(compare(2,3),/并存期/); // Zhou and Qin do not intersect.
assert.match(compare(9,10),/比值 0\.80/);
assert.match(compare(10,9),/比值 1\.25/);
dom.window.close();
console.log('Era comparisons: reversed overlap, identical intervals, contact and population units passed');
