import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

let failed = false;
for (const [file, prefix, button, valid, invalid] of [
  ['tools/fun/chess-fen-viewer.html', 'chess_fen_viewer', 'start()', w => { w.document.getElementById('fen').value = '8/8/8/8/8/8/8/8 w - - 0 1'; }, w => { w.document.getElementById('fen').value = '8/8/8/8/8/8/8/8 x - - 0 1'; }],
  ['tools/chess/gomoku-forbidden.html', 'gomoku_forbidden', 'analyzeCoordinate()', w => { w.document.getElementById('goCol').value = 'H'; w.document.getElementById('goRow').value = '8'; }, w => { w.document.getElementById('goCol').value = ''; }],
]) {
  const records = [], charts = [], exports = [];
  let rows = [];
  const noop = () => {};
  const kit = {
    util: { isEn: () => false, diffBox: noop, exportTable: () => exports.push(rows.map(row => [...row])) },
    matrix: { table: (_, data) => { rows = data.rows; } },
    chart: { line: (_, data) => charts.push(data.series[0].data.slice()) },
    history: { record: d => records.unshift({ t: Date.now(), d }), last: () => records[0]?.d, list: () => records, mount: noop },
    preset: { bar: noop },
  };
  const dom = new JSDOM(readFileSync(file, 'utf8'), { url: 'https://x.test/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(), beforeParse(w) { w.TBKit = kit; w.alert = noop; } });
  const w = dom.window, doc = w.document;
  await new Promise(resolve => w.addEventListener('load', resolve));
  const check = (label, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${prefix} ${label}`); if (!ok) failed = true; };
  const act = button === 'start()' ? () => doc.querySelector(`[onclick="${button}"]`).click() : () => doc.getElementById('goCol').dispatchEvent(new w.Event('input', { bubbles: true }));
  valid(w); act();
  invalid(w); act();
  check('连续真实点击产生通过与未通过历史', records.length === 2 && records[0].d.__tbScore === 0 && records[1].d.__tbScore === 1);
  check('趋势包含通过与未通过', charts.some(data => data.join(',') === '1,0'));
  check('明细表包含失败及成功', rows.length === 2 && rows[0].includes('未通过') && rows[1].includes('通过'));
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  check('导出调用获得最新明细', exports.length === 1 && exports[0].length === 2 && exports[0][0].includes('未通过'));
  if (prefix === 'gomoku_forbidden') {
    valid(w); act();
    w.document.getElementById('goCol').value = 'I'; act();
    check('连续同类输入先节流', records.length === 3);
    doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
    check('导出立即刷新节流中的最终结果', records.length === 4 && records[0].d.goCol === 'I' && exports[1][0].includes('I'));
    w.document.getElementById('goCol').value = 'J'; act();
    await new Promise(resolve => setTimeout(resolve, 1100));
    check('节流结束保留最终输入', records.length === 5 && records[0].d.goCol === 'J');
  }
  dom.window.close();
}
// Real validator interactions must preserve the latest rapid input, including on export.
for (const [slug, valid] of [
  ['gstin-validator','09AABCU9603R1ZL'], ['meid-validator','A00000123456780'],
  ['tfn-validator','876543210'], ['pan-validator','ABCPS1234E'],
  ['curp-validator','BOXW310820HMNERN16'], ['dni-validator','12345678Z'],
  ['sort-code-validator-validator','200000'], ['tin-validator','123-45-6789'],
  ['credit-card-luhn','4111111111111111'], ['credit-card-type','4111111111111111'],
  ['aba-validator','021000021'], ['aadhaar-validator','345678901238'],
  ['abn-validator','53004085616'], ['bic-validator','CHASUS33'], ['cpf-validator','11144477735'],
]) {
  const downloads = [], trends = [];
  const dom = new JSDOM(readFileSync(`tools/finance/${slug}.html`, 'utf8'), {
    url:`https://x.test/tools/finance/${slug}.html`, runScripts:'dangerously', pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(), beforeParse(w) {
      w.ToolBox={showToast(){},escHtml:s=>String(s)}; w.i18nText=k=>k;
      w.Blob=class { constructor(parts){this.text=parts.join('');} };
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{}; w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window, doc=w.document, prefix=slug.replaceAll('-','_');
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear(); w.eval(`__${prefix}_last=0`);
  const input=doc.getElementById('input');
  const enter=value=>{input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} ${slug} ${label}`);if(!ok)failed=true;};
  const actualValid=slug==='meid-validator' ? 'A0000012345678'+w.eval('HEX_BASE[meidCheckHex("A0000012345678")]') : valid;
  enter(actualValid); enter('2'.repeat(100));
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  let records=w.TBKit.history.list();
  check('快速输入后导出包含最新失败', records.length===2 && records[0].d.__tbScore===0 && downloads[0]?.includes('未通过'));
  check('快速输入趋势保留真实状态', trends.some(t=>t.join(',')==='1,0'));
  w.TBKit.history.clear(); w.eval(`__${prefix}_last=0`);
  enter(actualValid); enter('3'.repeat(100));
  await new Promise(resolve=>setTimeout(resolve,1100));
  records=w.TBKit.history.list();
  check('节流结束后记录最新失败', records.length===2 && records[0].d.input==='3'.repeat(100) && records[0].d.__tbScore===0);
  w.TBKit.history.clear(); w.eval(`__${prefix}_last=0`);
  enter(actualValid); enter('4'.repeat(100));
  doc.querySelector(`#${prefix}Hist .tbk-history-item`)?.click();
  await new Promise(resolve=>setTimeout(resolve,1100));
  check('恢复历史时取消待处理输入', input.value===actualValid && w.TBKit.history.list().length===1);
  w.close();
}
// Invalid long inputs and malformed ABNs must not be recorded as valid.
for(const [slug,valid] of [['aadhaar-validator','345678901238'],['abn-validator','53004085616'],['bic-validator','CHASUS33'],['cpf-validator','11144477735']]) {
  const dom=new JSDOM(readFileSync(`tools/finance/${slug}.html`,'utf8'),{
    url:`https://x.test/tools/finance/${slug}.html`,runScripts:'dangerously',virtualConsole:new VirtualConsole(),beforeParse(w){
      let now=100000;w.Date.now=()=>now+=1100;w.ToolBox={showToast(){},escHtml:s=>String(s)};w.i18nText=k=>k;
      w.eval(readFileSync('js/tool-kit.js','utf8'));
    }
  });
  const w=dom.window,doc=w.document;
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear();
  const enter=value=>{const el=doc.getElementById('input');el.value=value;el.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} ${slug} ${label}`);if(!ok)failed=true;};
  enter(valid);enter('2'.repeat(100));
  let records=w.TBKit.history.list();
  check('有效值及长无效值结论一致',records.length===2 && records[1].d.__tbScore===1 && records[0].d.__tbScore===0);
  if(slug==='abn-validator') {
    enter('53004085616x'); records=w.TBKit.history.list();
    check('夹杂字母的 ABN 被拒绝',records[0]?.d.__tbScore===0 && /非法|只能/.test(doc.getElementById('output').textContent));
    enter('<img src=x onerror=alert(1)>53004085616');
    check('输入不注入 HTML',!doc.getElementById('output').querySelector('img'));
  }
  w.close();
}
// BIN lookups distinguish known records, incomplete input, and unrecognized prefixes.
{
  const downloads=[],trends=[];
  const dom=new JSDOM(readFileSync('tools/finance/credit-card-bin.html','utf8'),{
    url:'https://x.test/tools/finance/credit-card-bin.html',runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      let now=100000; w.Date.now=()=>now+=1100;
      w.ToolBox={showToast(){},escHtml:s=>String(s)}; w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window,doc=w.document;
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear();
  const enter=value=>{const input=doc.getElementById('input');input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} credit-card-bin ${label}`);if(!ok)failed=true;};
  enter('411111');enter('invalid');
  check('非法字符记为未通过',w.TBKit.history.list()[0]?.d.__tbScore===0);
  enter('400000');
  check('未收录不冒充通过或失败',w.TBKit.history.list()[0]?.d.__tbScore==null && doc.getElementById('credit_card_binTable').textContent.includes('未收录'));
  check('趋势不将未收录计入通过或失败',trends.at(-1)?.join(',')==='1,0');
  doc.querySelector('[onclick="__credit_card_binExport()"]')?.click();
  check('CSV 区分未收录与非法输入',downloads[0]?.includes('未收录') && downloads[0]?.includes('未通过'));
  w.close();
}
{
  const downloads=[];
  const dom=new JSDOM(readFileSync('tools/finance/credit-card-bin.html','utf8'),{
    url:'https://x.test/tools/finance/credit-card-bin.html',runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      w.ToolBox={showToast(){},escHtml:s=>String(s)};w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
    }
  });
  const w=dom.window,doc=w.document;
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear();w.eval('__credit_card_bin_last=0');
  const input=doc.getElementById('input');
  const enter=value=>{input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} credit-card-bin ${label}`);if(!ok)failed=true;};
  enter('411111');enter('invalid');
  doc.querySelector('[onclick="__credit_card_binExport()"]')?.click();
  check('快速输入后导出最新失败',w.TBKit.history.list().length===2 && w.TBKit.history.list()[0]?.d.__tbScore===0 && downloads[0]?.includes('未通过'));
  enter('400000');await new Promise(resolve=>setTimeout(resolve,1100));
  check('节流后保存最终未收录结果',w.TBKit.history.list()[0]?.d.input==='400000' && w.TBKit.history.list()[0]?.d.__tbScore==null);
  enter('invalid');doc.querySelector('#credit_card_binHist .tbk-history-item')?.click();
  await new Promise(resolve=>setTimeout(resolve,1100));
  check('恢复历史不保存被替换输入',input.value==='400000' && w.TBKit.history.list()[0]?.d.input==='400000');
  w.close();
}
// Inspect real validity across malformed inputs and summaries longer than 80 characters.
for (const slug of ['credit-card-luhn','credit-card-type']) {
  const downloads=[], trends=[];
  const dom=new JSDOM(readFileSync(`tools/finance/${slug}.html`,'utf8'),{
    url:`https://x.test/tools/finance/${slug}.html`,runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      let now=100000; w.Date.now=()=>now+=1100;
      w.ToolBox={showToast(){},escHtml:s=>String(s)}; w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{}; w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window,doc=w.document,prefix=slug.replaceAll('-','_');
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear();
  const input=doc.getElementById('input');
  const enter=value=>{input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} ${slug} ${label}`);if(!ok)failed=true;};
  enter('4111111111111111'); enter('invalid');
  check('非法字符记为未通过',w.TBKit.history.list()[0]?.d.__tbScore===0);
  enter('4'.repeat(100));
  check('超长卡号记为未通过',w.TBKit.history.list()[0]?.d.__tbScore===0);
  check('趋势包含真实通过与失败',trends.some(t=>t.includes(1)&&t.includes(0)));
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  check('CSV 导出真实失败结论',downloads[0]?.includes('未通过'));
  w.close();
}
// Exercise validation with real output, history, trend and CSV.
for (const [slug, valid] of [
  ['tfn-validator','876543210'], ['pan-validator','ABCPS1234E'],
  ['curp-validator','BOXW310820HMNERN16'], ['dni-validator','12345678Z'],
  ['sort-code-validator-validator','200000'],
]) {
  const downloads=[], trends=[];
  const dom=new JSDOM(readFileSync(`tools/finance/${slug}.html`,'utf8'),{
    url:`https://x.test/tools/finance/${slug}.html`,runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      let now=100000; w.Date.now=()=>now+=1100;
      w.ToolBox={showToast(){},escHtml:s=>String(s)}; w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{}; w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window,doc=w.document,pre=slug.replaceAll('-','_');
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear();
  const input=doc.getElementById('input');
  function enter(value){input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));}
  enter(valid);
  const validOutput=doc.getElementById('output').textContent;
  enter('2'.repeat(100));
  const records=w.TBKit.history.list();
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} ${slug} ${label}`);if(!ok)failed=true;};
  check('真实有效与长输入无效结论一致',validOutput.includes('✅') && records.length===2 && records[0].d.__tbScore===0 && records[1].d.__tbScore===1);
  check('趋势包含真实通过和未通过',trends.some(t=>t.join(',')==='1,0'));
  doc.querySelector(`[onclick="__${pre}Export()"]`)?.click();
  check('真实 CSV 包含未通过',downloads.length===1 && downloads[0].includes('未通过'));
  w.close();
}
{
  const downloads=[], trends=[];
  const dom=new JSDOM(readFileSync('tools/finance/tin-validator.html','utf8'),{
    url:'https://x.test/tools/finance/tin-validator.html',runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      let now=100000; w.Date.now=()=>now+=1100;
      w.ToolBox={showToast(){},escHtml:s=>String(s)}; w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{}; w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window,doc=w.document;
  await new Promise(resolve=>w.addEventListener('load',resolve));
  w.TBKit.history.clear();
  const input=doc.getElementById('input');
  function enter(value){input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));}
  enter('123-45-6789');
  enter('2'.repeat(100));
  const records=w.TBKit.history.list();
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} tin ${label}`);if(!ok)failed=true;};
  check('真实长输入失败结论不受摘要截断影响',records.length===2 && records[0].d.__tbScore===0 && records[1].d.__tbScore===1);
  check('趋势包含真实通过和未通过',trends.some(t=>t.join(',')==='1,0'));
  doc.querySelector('[onclick="__tin_validatorExport()"]')?.click();
  check('真实 CSV 包含未通过',downloads.length===1 && downloads[0].includes('未通过'));
  w.close();
}
// Exercise the real toolkit, including its CSV serialization and download path.
for (const [file, prefix] of [
  ['tools/agriculture/fertilizer-calculator.html', 'fertilizer_calculator'],
  ['tools/chess/gomoku-forbidden.html', 'gomoku_forbidden'],
  ['tools/edu2/exam-analysis.html', 'exam_analysis'],
]) {
  const downloads = [], trends = [];
  const dom = new JSDOM(readFileSync(file, 'utf8'), {
    url: `https://x.test/${file}`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = { showToast() {}, escHtml: s => String(s), setResult(id, html) { w.document.getElementById(id).innerHTML = html; } };
      w.i18nText = k => k;
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = blob => { downloads.push(blob.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.eval(readFileSync('js/tool-kit.js', 'utf8'));
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (host, config) => { trends.push(Array.from(config.series[0].data)); return line(host, config); };
    },
  });
  const w = dom.window, doc = w.document;
  await new Promise(resolve => w.addEventListener('load', resolve));
  w.TBKit.history.clear();
  w.eval(`__${prefix}_last=0`);
  const check = (label, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${prefix} ${label}`); if (!ok) failed = true; };
  if (prefix === 'fertilizer_calculator') {
    w.drawChart = () => {};
    w.calc();
    doc.getElementById('area').value = '';
    doc.getElementById('area').dispatchEvent(new w.Event('input', { bubbles: true }));
  } else if (prefix === 'gomoku_forbidden') {
    doc.getElementById('goCol').value = 'H';
    doc.getElementById('goRow').value = '8';
    doc.getElementById('goCol').dispatchEvent(new w.Event('input', { bubbles: true }));
    doc.getElementById('goCol').value = '';
    doc.getElementById('goCol').dispatchEvent(new w.Event('input', { bubbles: true }));
  } else {
    doc.getElementById('scoreInput').value = '甲,80\n乙,90';
    doc.querySelector('[onclick="calc()"].btn').click();
    doc.getElementById('fullScore').value = '';
    doc.querySelector('[onclick="calc()"].btn').click();
  }
  const records = w.TBKit.history.list();
  check('连续有效和无效操作分别记账', records.length === 2 && records[0].d.__tbScore === 0 && records[1].d.__tbScore === 1);
  const err = prefix === 'fertilizer_calculator' ? '请填写' : prefix === 'gomoku_forbidden' ? '坐标无效' : '满分必须大于 0';
  check('失败记录包含当前错误而非旧结果', !!records[0] && String(records[0].d['结果']).includes(err));
  if (prefix === 'exam_analysis') check('失败记录不携带旧平均分', !!records[0] && records[0].d.__mean == null);
  const table = doc.getElementById(`${prefix}Table`);
  check('真实表格显示失败及通过', table.textContent.includes('未通过') && table.textContent.includes('通过'));
  check('真实趋势图包含通过与失败', !!doc.querySelector(`#${prefix}Chart svg`) && trends.some(t => t.join(',') === '1,0'));
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  check('实际下载 CSV 包含当前失败结果', downloads.length === 1 && downloads[0].includes('未通过') && downloads[0].includes(err));
  if (prefix === 'exam_analysis') {
    doc.getElementById('fullScore').value = '100';
    doc.getElementById('scoreInput').value = '甲,20';
    doc.querySelector('[onclick="calc()"].btn').click();
    const current = w.TBKit.history.list()[0].d;
    check('低分为有效计算而非输入失败', current.__tbScore === 1 && current['结果'].includes('不及格'));
  }
  dom.window.close();
}
// Check other reported pages through their real input handlers and toolkit downloads.
for (const [file, prefix, input, error] of [
  ['tools/agriculture/canopy-coverage.html', 'canopy_coverage', 'rowSpacing', '行距株距必须大于0'],
  ['tools/clinical-lab/flow-cytometry-ratio.html', 'flow_cytometry_ratio', 'wbc', '请先填写有效'],
  ['tools/clinical-lab/blood-gas-analysis.html', 'blood_gas_analysis', 'ph', '请填写'],
  ['tools/marketing/utm-builder.html', 'utm_builder', 'url', ''],
  ['tools/fun/chess-fen-viewer.html', 'chess_fen_viewer', 'fen', '字段缺失或非法'],
]) {
  const downloads = [], trends = [];
  const dom = new JSDOM(readFileSync(file, 'utf8'), { url:`https://x.test/${file}`, runScripts:'dangerously', pretendToBeVisual:true, virtualConsole:new VirtualConsole(), beforeParse(w) {
    w.ToolBox = { showToast(){}, toast(){}, escHtml:s=>String(s), setResult(id, html){w.document.getElementById(id).innerHTML=html;} };
    w.i18nText = k => k;
    w.Blob = class { constructor(parts){this.text=parts.join('');} };
    w.URL.createObjectURL = blob => { downloads.push(blob.text); return 'blob:test'; };
    w.URL.revokeObjectURL = () => {};
    w.HTMLAnchorElement.prototype.click = function(){};
    w.eval(readFileSync('js/tool-kit.js', 'utf8'));
    const line=w.TBKit.chart.line;
    w.TBKit.chart.line=(host, config)=>{ trends.push(Array.from(config.series[0].data)); return line(host, config); };
  }});
  const w = dom.window, doc = w.document;
  await new Promise(resolve => w.addEventListener('load', resolve));
  w.TBKit.history.clear(); w.eval(`__${prefix}_last=0`);
  const check = (label, ok) => { console.log(`${ok?'PASS':'FAIL'} ${prefix} ${label}`); if(!ok) failed=true; };
  if(prefix==='utm_builder') {
    doc.getElementById(input).value='https://example.com/test';
    doc.getElementById(input).dispatchEvent(new w.Event('input',{bubbles:true}));
    const result=doc.getElementById('resultUrl').textContent;
    check('真实生成链接入历史', w.TBKit.history.list().some(r=>r.d['结果']===result));
    doc.getElementById('source').value=''; doc.getElementById('source').dispatchEvent(new w.Event('input',{bubbles:true}));
    check('缺少来源立即记为失败', w.TBKit.history.list()[0]?.d.__tbScore===0);
    doc.getElementById('source').value='failed'; doc.getElementById('source').dispatchEvent(new w.Event('input',{bubbles:true}));
    check('URL 中的错误关键词不误判', w.TBKit.history.list()[0]?.d.__tbScore===1);
    doc.getElementById(input).value='https://example.com/'+ 'x'.repeat(100); doc.getElementById(input).dispatchEvent(new w.Event('input',{bubbles:true}));
    doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
    check('导出保存完整最终链接', downloads.pop()?.includes(doc.getElementById('resultUrl').textContent));
    doc.getElementById(input).value='https://example.com/test'; doc.getElementById(input).dispatchEvent(new w.Event('input',{bubbles:true}));
  } else if(prefix==='chess_fen_viewer') {
    doc.getElementById(input).value='8/8/8/8/8/8/8/8 w - - 0 1'; doc.querySelector('[onclick="start()"]').click();
    doc.getElementById(input).value='8/8/8/8/8/8/8/8 x - - 0 1'; doc.querySelector('[onclick="start()"]').click();
    check('连续解析记入失败', w.TBKit.history.list()[0]?.d.__tbScore===0);
  } else {
    const el=doc.getElementById(input); el.dispatchEvent(new w.Event('input',{bubbles:true}));
    el.value=''; el.dispatchEvent(new w.Event('input',{bubbles:true}));
    if(prefix==='blood_gas_analysis') {
      doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
      check('非法输入禁止导出', downloads.length===0);
      el.value='7.4'; el.dispatchEvent(new w.Event('input',{bubbles:true}));
      check('无效结果不被写入历史', w.TBKit.history.list().every(r=>!String(r.d['结果']).includes(error)));
    } else check('连续清空记入未通过', w.TBKit.history.list()[0]?.d.__tbScore===0 && String(w.TBKit.history.list()[0].d['结果']).includes(error));
  }
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  if(prefix==='blood_gas_analysis') check('恢复有效后导出不含错误',downloads.length===1 && !downloads[0].includes(error));
  else check('真实下载包含当前结果',downloads.length===1 && downloads[0].includes(error || 'https://example.com/test'));
  if (prefix==='canopy_coverage' || prefix==='flow_cytometry_ratio' || prefix==='utm_builder') {
    if(prefix!=='flow_cytometry_ratio') check('真实趋势包含通过与失败', trends.some(t=>t.includes(0) && t.includes(1)));
    else check('失败输入不进入比值趋势', !trends.some(t=>t.length>1));
    const failedRecord=w.TBKit.history.list().find(r=>r.d.__tbScore===0);
    if(prefix==='utm_builder') { doc.getElementById('source').value='restored-value'; doc.getElementById('source').dispatchEvent(new w.Event('input',{bubbles:true})); }
    else { doc.getElementById(input).value=prefix==='canopy_coverage'?'75':'7'; doc.getElementById(input).dispatchEvent(new w.Event('input',{bubbles:true})); }
    const buttons=Array.from(doc.querySelectorAll(`#${prefix}Hist .tbk-history-item`));
    const idx=w.TBKit.history.list().slice(0,6).findIndex(r=>r.t===failedRecord.t && r.d['结果']===failedRecord.d['结果']);
    if(idx>=0) buttons[idx]?.click();
    check('恢复失败快照时清空对应输入', idx>=0 && doc.getElementById(prefix==='utm_builder'?'source':input).value==='');
    check('恢复失败快照后显示对应错误', prefix==='utm_builder' ? doc.getElementById('resultUrl').textContent.includes('必填') : doc.getElementById(prefix==='canopy_coverage'?'result0':'result').textContent.includes(error));
    if(prefix==='flow_cytometry_ratio') {
      doc.getElementById('wbc').value='6'; doc.getElementById('cd4').value='101'; doc.getElementById('cd4').dispatchEvent(new w.Event('input',{bubbles:true}));
      doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
      check('百分比超范围记为失败', w.TBKit.history.list()[0]?.d.__tbScore===0 && w.TBKit.history.list()[0]?.d['结果'].includes('须在 0–100%'));
    }
  }
  w.close();
}
{
  const dom=new JSDOM(readFileSync('tools/finance/npv-calculator.html','utf8'), {url:'https://x.test/',runScripts:'dangerously',virtualConsole:new VirtualConsole(),beforeParse(w){w.ToolBox={showToast(){}};w.HTMLCanvasElement.prototype.getContext=()=>null;}});
  const w=dom.window;
  await new Promise(resolve=>w.addEventListener('load',resolve));
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} npv ${label}`);if(!ok) failed=true;};
  const close=(a,b)=>Math.abs(a-b)<1e-7;
  let result=w.calcIRR(100,[221,-122.1]);
  check('同区间两根 10% 与 11%',result.status==='multiple' && result.rates.length===2 && close(result.rates[0],.1) && close(result.rates[1],.11));
  result=w.calcIRR(100,[220,-121]);
  check('10% 重根',result.status==='ok' && close(result.rate,.1));
  result=w.calcIRR(100,[230,-132]);
  check('原案例两根 10% 与 20%',result.status==='multiple' && result.rates.length===2 && close(result.rates[0],.1) && close(result.rates[1],.2));
  result=w.calcIRR(100,[220,-121.0001]);
  check('接近重根但无根不误报',result.status==='none');
  result=w.calcIRR(100,[30,30,30,30,30]);
  check('普通单根',result.status==='ok' && close(result.rate,.1523823712));
  result=w.calcIRR(100,[221,-122.1,0,0]);
  check('尾随零不会隐藏两根',result.status==='multiple' && result.rates.length===2);
  result=w.calcIRR(100,[330,-363,133.1]);
  check('高阶重复根不能误报无解',result.status!=='none');
  for(const flows of [[2,-1.0000000000000002],[2,-0.9999999999999999],[2,-0.9999999999999998],[4,-6,4,-1]]){
    result=w.calcIRR(1,flows);
    check('精度极限不作错误判定 '+flows.join(','),result.status==='uncertain');
  }
  result=w.calcIRR(1,[10,-25]);
  check('严格重根不产生伪根',result.status==='ok' && close(result.rate,4));
  result=w.calcIRR(1,[1002,-1000.9999999999]);
  check('上边界外的根不误报多根',result.status==='uncertain' || result.status==='ok');
  result=w.calcIRR(1,[1.0001,-.000099999999999999]);
  check('下边界外的根不误报多根',result.status==='uncertain' || result.status==='ok');
  result=w.calcIRR(100,[360,-431,171.6]);
  check('三根 10%、20%、30%',result.status==='multiple' && result.rates.length===3 && close(result.rates[0],.1) && close(result.rates[1],.2) && close(result.rates[2],.3));
  result=w.calcIRR(100,[200,-100*(1-1e-10)]);
  check('非常接近的两个根不合并', result.status==='multiple' && result.rates.length===2 && result.rates[1]-result.rates[0]>1e-5);
  result=w.calcIRR(100,[200,-100*(1+1e-10)]);
  check('近似重根但无解不误报', result.status==='none' || result.status==='uncertain');
  result=w.calcIRR(100,[100100]);
  check('100000% 上边界', result.status==='ok' && close(result.rate,1000));
  result=w.calcIRR(100,[.01]);
  check('−99.99% 下边界', result.status==='ok' && close(result.rate,-.9999));
  result=w.calcIRR(1e-300,Array(150).fill(0).concat([-1e308,1e308]));
  check('归一化下溢不能虚报正 IRR',result.status==='uncertain' || (result.status==='ok' && result.rate<0 && result.rate>-.5));
  result=w.calcIRR(1,[1001,1e-11]);
  check('搜索范围外近边界单根不误报边界解',result.status==='none' || result.status==='uncertain');
  const longFlows=[200,-100].concat(Array(23).fill(1));
  check('长现金流不虚报无解',w.calcIRR(100,longFlows).status==='uncertain');
  w.drawChart=()=>{}; w.document.getElementById('init').value='100';
  w.eval('cashFlows=[221,-122.1]'); w.calc();
  check('真实页面展示两根',w.document.getElementById('detail').textContent.includes('10.00%') && w.document.getElementById('detail').textContent.includes('11.00%'));
  w.eval('cashFlows=[200,-100].concat(Array(23).fill(1))'); w.calc();
  check('真实页面显示无法确定而不是无解',w.document.getElementById('stats').textContent.includes('无法确定') && w.document.getElementById('detail').textContent.includes('无法确定'));
  w.close();
}
// Exercise real amount conversion and history, including out-of-range and rapid edits.
{
  const downloads=[], trends=[];
  const dom=new JSDOM(readFileSync('tools/finance/amount-in-words.html','utf8'),{
    url:'https://x.test/tools/finance/amount-in-words.html',runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      w.ToolBox={showToast(){},escHtml:s=>String(s)};w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window,doc=w.document;
  await new Promise(resolve=>w.addEventListener('load',resolve));
  const input=doc.getElementById('money');
  const enter=value=>{input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} amount-in-words ${label}`);if(!ok)failed=true;};
  w.TBKit.history.clear();w.eval('__amount_in_words_last=0');
  enter('1234.56');enter('10000000000000000');
  doc.querySelector('[onclick="__amount_in_wordsExport()"]')?.click();
  let records=w.TBKit.history.list();
  check('快速导出保留超范围失败',records.length===2 && records[0].d.__tbScore===0 && downloads[0]?.includes('未通过'));
  check('趋势包含真实通过和失败',trends.some(t=>t.join(',')==='1,0'));
  w.TBKit.history.clear();w.eval('__amount_in_words_last=0');
  enter('0');enter('9999999999999999.995');
  await new Promise(resolve=>setTimeout(resolve,1100));
  records=w.TBKit.history.list();
  check('舍入溢出记为失败且零元有效',records.length===2 && records[1].d.__tbScore===1 && records[0].d.__tbScore===0);
  enter('123');doc.querySelector('#amount_in_wordsHist .tbk-history-item')?.click();
  await new Promise(resolve=>setTimeout(resolve,1100));
  check('恢复历史取消待保存输入',input.value==='9999999999999999.995' && w.TBKit.history.list().length===2);
  w.TBKit.history.clear();w.eval('__amount_in_words_last=0');
  enter('1');enter('2');enter('');
  await new Promise(resolve=>setTimeout(resolve,1100));
  check('清空输入不保存被替换的待处理记录',w.TBKit.history.list().length===1 && /请输入/.test(doc.getElementById('out').textContent));
  w.close();
}
// Credit assessment history must reflect actual validation and restore empty fields.
{
  const downloads=[],trends=[];
  const dom=new JSDOM(readFileSync('tools/finance/assessor-manager.html','utf8'),{
    url:'https://x.test/tools/finance/assessor-manager.html',runScripts:'dangerously',pretendToBeVisual:true,
    virtualConsole:new VirtualConsole(),beforeParse(w){
      w.ToolBox={showToast(){},escHtml:s=>String(s)};w.i18nText=k=>k;
      w.Blob=class{constructor(parts){this.text=parts.join('');}};
      w.URL.createObjectURL=blob=>{downloads.push(blob.text);return 'blob:test';};
      w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
      w.eval(readFileSync('js/tool-kit.js','utf8'));
      const line=w.TBKit.chart.line;
      w.TBKit.chart.line=(host,config)=>{trends.push(Array.from(config.series[0].data));return line(host,config);};
    }
  });
  const w=dom.window,doc=w.document,input=doc.getElementById('debtRatio');
  await new Promise(resolve=>w.addEventListener('load',resolve));
  const enter=value=>{input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));};
  const check=(label,ok)=>{console.log(`${ok?'PASS':'FAIL'} assessor-manager ${label}`);if(!ok)failed=true;};
  w.TBKit.history.clear();w.eval('__assessor_manager_last=0');
  enter('55');enter('101');doc.querySelector('[onclick="__assessor_managerExport()"]')?.click();
  let records=w.TBKit.history.list();
  check('超出范围与快速导出记为失败',records.length===2 && records[0].d.__tbScore===0 && downloads[0]?.includes('未通过'));
  check('趋势反映真实成功与失败',trends.some(t=>t.join(',')==='1,0'));
  enter('');await new Promise(resolve=>setTimeout(resolve,1100));
  records=w.TBKit.history.list();
  check('空字段作为失败快照保存',records.length===3 && records[0].d.debtRatio==='' && records[0].d.__tbScore===0);
  enter('50');doc.querySelector('#assessor_managerHist .tbk-history-item')?.click();
  await new Promise(resolve=>setTimeout(resolve,1100));
  check('恢复空字段且取消待保存输入',input.value==='' && w.TBKit.history.list().length===3 && /留空/.test(doc.getElementById('res').textContent));
  w.TBKit.history.clear();w.eval('__assessor_manager_last=0');
  enter('100');doc.getElementById('currentRatio').value='0';doc.getElementById('revenue').value='0';doc.getElementById('profitMargin').value='-1';doc.getElementById('overdue').value='5';doc.getElementById('creditHistory').value='0';w.calc();
  doc.querySelector('[onclick="__assessor_managerExport()"]')?.click();
  check('高信用风险不等同于无效输入',w.TBKit.history.list()[0]?.d.__tbScore===1 && /信用风险高/.test(doc.getElementById('res').textContent));
  doc.getElementById('overdue').value='0.5';w.calc();doc.querySelector('[onclick="__assessor_managerExport()"]')?.click();
  check('逾期次数非整数记为失败',w.TBKit.history.list()[0]?.d.__tbScore===0 && /非负整数/.test(doc.getElementById('res').textContent));
  w.close();
}
process.exit(failed ? 1 : 0);
