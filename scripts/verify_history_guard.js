/**
 * 历史区字段守卫回归：确保 null/undefined/NaN 不会以文本形式渲染进 TBKit.history 区域。
 *
 * 背景：`__sxExtras()` 曾把 `conf: null` 写入历史，`tool-kit.js` 原样拼接后显示 `conf null`。
 * 用例：① 公共组件跳过缺失/非有限值；② 合法的 0 仍保留。
 */
"use strict";
const fs = require("fs");
const path = require("path");

// jsdom 只在动态用例里用；CI 未装依赖时不能让整条门禁在 require 阶段直接崩（假红）。
// 缺依赖 → 动态用例显式 SKIP(no-browser)，静态用例照常判红/绿。
let JSDOM = null;
let JSDOM_ERR = "";
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  JSDOM_ERR = e.message;
}

const ROOT = path.resolve(__dirname, "..");
const CASES = [];

CASES.push({
  name: "工具库历史区跳过 null/undefined/NaN",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const dom = new JSDOM('<!doctype html><body><div id="hist"></div></body>', {
      url: "http://localhost/",
      runScripts: "outside-only",
    });
    const win = dom.window;
    win.localStorage.clear();
    win.eval(fs.readFileSync(path.join(ROOT, "js/tool-kit.js"), "utf8"));
    win.TBKit.history.record({ conf: null, score: undefined, prob: NaN, mean: Infinity, ok: 1 });
    const host = win.document.getElementById("hist");
    win.TBKit.history.mount("#hist");
    const text = host.textContent;
    const dirty = /\b(null|undefined|NaN|Infinity)\b/.test(text);
    return { ok: !dirty && text.includes("ok 1"), got: text.trim() };
  },
});

CASES.push({
  name: "工具库历史区保留合法 0",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const dom = new JSDOM('<!doctype html><body><div id="hist"></div></body>', {
      url: "http://localhost/",
      runScripts: "outside-only",
    });
    const win = dom.window;
    win.localStorage.clear();
    win.eval(fs.readFileSync(path.join(ROOT, "js/tool-kit.js"), "utf8"));
    win.TBKit.history.record({ conf: 0, score: 0 });
    const host = win.document.getElementById("hist");
    win.TBKit.history.mount("#hist");
    return { ok: host.textContent.includes("conf 0"), got: host.textContent.trim() };
  },
});

CASES.push({
  name: "景深空物距不写入历史结论",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, "tools/design/depth-of-field-calculator.html"), "utf8");
    const dom = new JSDOM(html, { url: "http://localhost/", runScripts: "outside-only" });
    const win = dom.window;
    win.TBKit = { util: { isEn: () => false }, history: { last: () => null, record: r => records.push(r) } };
    const records = [];
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("const coc=") || match[1].includes("var __depth_of_field_calculator_last")) win.eval(match[1]);
    }
    win.document.getElementById("distance").value = "";
    win.calc();
    return { ok: records.length === 0 && win.document.getElementById("dofTotal").textContent === "—", got: JSON.stringify(records) };
  },
});

CASES.push({
  name: "TDS 英文空值和越界状态无中文",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, "tools/energy/water-tds-evaluator.html"), "utf8");
    const dom = new JSDOM(html, { url: "http://localhost/?lang=en-US", runScripts: "outside-only" });
    const win = dom.window;
    win.TBKit = { util: { isEn: () => true } };
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("function evaluate()")) win.eval(match[1]);
    }
    const states = [];
    for (const value of ["5001", ""]) {
      win.document.getElementById("tdsInput").value = value;
      win.evaluate();
      states.push(win.document.getElementById("result").textContent + win.document.getElementById("vizGrade").textContent);
    }
    return { ok: states.every(s => !/[\u4e00-\u9fff]/.test(s)), got: JSON.stringify(states) };
  },
});

CASES.push({
  name: "向量清空分量不得当作零",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, "tools/it/vector-magnitude.html"), "utf8");
    const win = new JSDOM(html, { url: "http://localhost/", runScripts: "outside-only" }).window;
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("function fmtSumSq(")) win.eval(match[1]);
    }
    win.document.getElementById("v0").value = "";
    win.calculate();
    const text = win.document.getElementById("output").textContent;
    return { ok: text.includes("向量分量必须为有限数值") && !text.includes("|v| ="), got: text };
  },
});

CASES.push({
  name: "向量最小非零分量不死循环",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const { spawnSync } = require("child_process");
    const code = `const fs=require('fs'),{JSDOM}=require('jsdom');const html=fs.readFileSync('tools/it/vector-magnitude.html','utf8');const w=new JSDOM(html,{url:'http://localhost/',runScripts:'outside-only'}).window;for(const m of html.matchAll(/<script(?:\\s[^>]*)?>([\\s\\S]*?)<\\/script>/g)){if(m[1].includes('function fmtSumSq('))w.eval(m[1]);}w.document.getElementById('dim').value='2';w.document.getElementById('v0').value='5e-324';w.document.getElementById('v1').value='0';w.calculate();process.stdout.write(w.document.getElementById('output').textContent);`;
    const child = spawnSync(process.execPath, ["-e", code], { cwd: ROOT, encoding: "utf8", timeout: 5000 });
    return { ok: child.status === 0 && child.stdout.includes("4.941e-324") && child.stdout.includes("e-647"), got: child.error ? child.error.message : child.stderr || child.stdout };
  },
});

CASES.push({
  name: "免税收益率清空时清除图表，合法零值仍可绘图",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, "tools/banking/tax-equivalent-yield.html"), "utf8");
    const win = new JSDOM(html, { url: "http://localhost/", runScripts: "outside-only" }).window;
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("function num(")) win.eval(match[1].replace(/calcTool\(\);\s*$/, ""));
      if (match[1].includes("function __teySweep()")) win.eval(match[1]);
    }
    win.TBKit = { chart: { line: () => {} }, util: { isEn: () => false } };
    const input = win.document.getElementById("muni"), host = win.document.getElementById("teyChart");
    input.value = "0";
    const zero = win.__teySweep();
    host.innerHTML = "old chart";
    input.value = "";
    win.__teyChart();
    return { ok: zero && zero.rows.length === 9 && win.__teySweep() === null && !host.innerHTML, got: host.innerHTML };
  },
});

CASES.push({
  name: "颜色输入事件清除旧评级并拒绝双井号",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, "tools/design/contrast-checker.html"), "utf8");
    const win = new JSDOM(html, { url: "http://localhost/", runScripts: "outside-only" }).window;
    win.ToolBox = { showToast() {} };
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("function onFgHexInput(")) win.eval(match[1]);
    }
    const fg=win.document.getElementById('fgHex'), bg=win.document.getElementById('bgHex');
    const status=win.document.getElementById('wcagAAStatus'), bar=win.document.getElementById('scoreBarFill');
    fg.value='FFFFFF'; bg.value='000000'; win.updateAll();
    fg.value='GGGGGG'; win.onFgHexInput();
    const cleared=status.textContent==='待判定' && bar.style.width==='0%';
    fg.value='##FFF'; win.onFgHexInput();
    const doubleHash=win.document.getElementById('ratioNum').textContent==='—';
    fg.value='FFFFFF'; bg.value='000000'; win.updateAll();
    bg.value='GGGGGG'; win.onBgHexInput();
    return { ok: cleared && doubleHash && status.textContent==='待判定' && bar.style.width==='0%', got: 'status='+status.textContent+' bar='+bar.style.width+' ratio='+win.document.getElementById('ratioNum').textContent };
  },
});

CASES.push({
  name: "油漆空参数阻止两种导出且合法参数可导出",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, 'tools/home/paint-calculator.html'), 'utf8');
    const win = new JSDOM(html, { url: 'http://localhost/', runScripts: 'outside-only' }).window;
    let downloads=0, csv=0;
    win.ToolBox={downloadText(){downloads++;},showToast(){}};
    win.TBKit={util:{isEn:()=>false,exportTable(){csv++;}},chart:{bar(){}}};
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("const STORAGE_KEY = 'home_paint_surfaces'")) win.eval(match[1]);
    }
    const coverage=win.document.getElementById('coverage');
    coverage.value=''; win.exportResult(); win.__paintExport();
    const blocked=downloads===0 && csv===0 && win.document.getElementById('total-paint').textContent==='—';
    coverage.value='10'; win.exportResult(); win.__paintExport();
    return {ok:blocked && downloads===1 && csv===1,got:`blocked=${blocked} text=${downloads} csv=${csv}`};
  },
});

CASES.push({
  name: "逐项分账真实控件按分配平并保留未参与者零额",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const html = fs.readFileSync(path.join(ROOT, "tools/life/bill-splitter.html"), "utf8");
    const win = new JSDOM(html, { url: "http://localhost/", runScripts: "outside-only" }).window;
    win.ToolBox = { showToast() {} };
    for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
      if (match[1].includes("const HISTORY_KEY = 'bill_splitter_history'")) win.eval(match[1]);
    }
    win.switchTab('advanced');
    const row = win.document.querySelector('#items-list .item-row');
    row.querySelector('input[type=number]').value = '0.01';
    row.querySelectorAll('input[type=checkbox]').forEach((el, i) => { el.checked = i < 2; });
    win.document.getElementById('adv-tip').value = '50';
    win.calcAdvanced();
    const text = win.document.getElementById('adv-result').textContent;
    const amounts = Array.from(win.document.querySelectorAll('#adv-result .result-person strong'), el => el.textContent);
    win.addItem();
    const added = win.document.querySelectorAll('#items-list .item-row')[1];
    const placeholders = Array.from(added.querySelectorAll('input:not([type=checkbox])'), el => el.placeholder);
    return { ok: text.includes('¥0.02') && amounts.join('|') === '¥0.01|¥0.01|¥0.00|¥0.00' && placeholders.join('|') === '项目名称|金额', got: text + ' / ' + placeholders.join('|') };
  },
});

CASES.push({
  name: "逐项分账巨大金额不能冻结页面或输出不安全金额",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
    const { spawnSync } = require('child_process');
    const code = `const fs=require('fs'),{JSDOM}=require('jsdom');const html=fs.readFileSync('tools/life/bill-splitter.html','utf8');const w=new JSDOM(html,{url:'http://localhost/',runScripts:'outside-only'}).window;for(const m of html.matchAll(/<script(?:\\s[^>]*)?>([\\s\\S]*?)<\\/script>/g))if(m[1].includes("const HISTORY_KEY = 'bill_splitter_history'"))w.eval(m[1]);w.switchTab('advanced');w.document.querySelector('#items-list input[type=number]').value='1e100';w.calcAdvanced();process.stdout.write(w.document.getElementById('adv-result').textContent);`;
    const child = spawnSync(process.execPath, ['-e', code], { cwd: ROOT, encoding: 'utf8', timeout: 3000 });
    return { ok: child.status === 0 && /超出|无法|过大/.test(child.stdout) && !/Infinity|NaN/.test(child.stdout), got: child.error ? child.error.message : child.stderr || child.stdout };
  },
});

CASES.push({
  name: '重做 IT：镜像标签中的 NaN 不得被替换',
  run() {
    if (!JSDOM) return {skip:true,got:JSDOM_ERR};
    const html=fs.readFileSync(path.join(ROOT,'tools/it/kubernetes-yaml-generator.html'),'utf8');
    const w=new JSDOM(html,{url:'http://localhost/',runScripts:'outside-only'}).window;
    for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) if(m[1].includes('var KY_IMG_RE=')) w.eval(m[1]);
    w.document.getElementById('image').value='nginx:NaN'; w.calcTool();
    const text=w.document.getElementById('result').textContent;
    return {ok:text.includes("image: 'nginx:NaN'"),got:text};
  },
});
CASES.push({
  name: '重做 IT：短标记不是 Markdown 围栏',
  run() {
    if (!JSDOM) return {skip:true,got:JSDOM_ERR};
    const html=fs.readFileSync(path.join(ROOT,'tools/it/markdown-lint.html'),'utf8');
    const w=new JSDOM(html,{url:'http://localhost/',runScripts:'outside-only'}).window;
    for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) if(m[1].includes("var fenceChar=''") && m[1].includes('function calcTool()')) w.eval(m[1]);
    w.document.getElementById('src').value='`js\n*bad\n`'; w.calcTool();
    const text=w.document.getElementById('result').textContent;
    return {ok:text.includes('列表符号后缺空格'),got:text};
  },
});
CASES.push({
  name: '重做 IT：二维码输入变化失效及真实编码错误',
  run() {
    if (!JSDOM) return {skip:true,got:JSDOM_ERR};
    const html=fs.readFileSync(path.join(ROOT,'tools/it/text-qr.html'),'utf8');
    const w=new JSDOM(html,{url:'http://localhost/',runScripts:'outside-only'}).window;
    w.HTMLCanvasElement.prototype.getContext=()=>({fillRect(){}});
    w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/png;base64,AA';
    let downloads=0; w.HTMLAnchorElement.prototype.click=function(){downloads++;}; w.alert=()=>{};
    w.eval(fs.readFileSync(path.join(ROOT,'js/qrcode.js'),'utf8'));
    for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) if(m[1].includes('function drawQR(')) w.eval(m[1]);
    const input=w.document.getElementById('text'); input.value='old'; w.generate();
    input.value=''; input.dispatchEvent(new w.Event('input',{bubbles:true})); w.downloadPNG();
    const blocked=downloads===0;
    input.value='x'.repeat(4000); let error=''; try{w.generate();}catch(e){error=e.message;}
    const text=w.document.getElementById('output').textContent;
    return {ok:blocked&&!error&&text.includes('内容过长'),got:`blocked=${blocked} error=${error} output=${text.slice(0,100)}`};
  },
});
CASES.push({
  name: '重做 IT：叉积极端量级与角度',
  run() {
    if (!JSDOM) return {skip:true,got:JSDOM_ERR};
    const html=fs.readFileSync(path.join(ROOT,'tools/it/vector-cross-product.html'),'utf8');
    const w=new JSDOM(html,{url:'http://localhost/',runScripts:'outside-only'}).window;
    for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) if(m[1].includes('function fmtScaled(')) w.eval(m[1]);
    function calc(values){['a0','a1','a2','b0','b1','b2'].forEach((id,i)=>w.document.getElementById(id).value=values[i]);w.calculate();return w.document.getElementById('output').textContent;}
    const tiny=calc(['5e-324','0','0','0','5e-324','0']);
    const partial=calc(['1e-200','0','0','1e-120','1e-130','0']);
    const parallel=calc(['1','0','0','1','1e-10','0']);
    const large=calc(['1.7e308','1.7e308','0','0','1','0']);
    return {ok:tiny.includes('e-647')&&partial.includes('e-330')&&!parallel.includes('A × B = 0，说明')&&large.includes('θ = 45°'),got:[tiny,partial,parallel,large].map(x=>x.slice(0,450)).join('\n')};
  },
});

let pass = 0;
let fail = 0;
let skipped = 0;
for (const c of CASES) {
  let r;
  try {
    r = c.run();
  } catch (e) {
    r = { ok: false, got: "抛出异常: " + e.message };
  }
  if (r.skip) {
    if (process.env.TB_REQUIRE_DYNAMIC === "1") {
      fail++;
      console.log(`❌ ${c.name} — TB_REQUIRE_DYNAMIC=1 但动态段被跳过：${r.got}`);
    } else {
      skipped++;
      console.log(`⚠️ SKIP(no-browser): ${c.name} — ${r.got}`);
    }
  } else if (r.ok) {
    pass++;
  } else {
    fail++;
    console.log(`❌ ${c.name} — ${r.got}`);
  }
}
console.log(`\n==== history field guard ${pass} passed / ${fail} failed / ${skipped} skipped ====`);
if (fail > 0) process.exit(1);
// 防空跑假绿：没有任何用例真正执行（全部跳过且无失败）时不能判绿
if (pass === 0) {
  console.log("❌ 0 个用例实际执行（全部跳过），拒绝判绿");
  process.exit(1);
}
process.exit(0);
