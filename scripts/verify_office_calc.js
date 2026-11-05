#!/usr/bin node
"use strict";
const fs = require("fs");
const path = require("path");
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- PNG 导出的静态结构断言
// harness 里 canvas / SVG / Image 全是桩，做不到像素级断言：
//   - 真实 SVG 的排版与字体度量依赖浏览器布局引擎，桩只能返回固定字符串；
//   - canvas 的 toBlob 在 Node 无实现（makeEl 的桩固定回调 null，用来走失败分支）。
// 因此这里只断言「PNG 导出链路能跑通所需的结构前提」，像素一致性交真机验证。
// 用户要求的三条都落在下面：htmlLabels:false → foreignObject 为 0；toBlob 在 try/catch 内；
// 失败 toast 取 e.name || e.message。
const FLOWCHART_PATH = path.join(__dirname, "..", "tools", "office", "flowchart.html");
function flowchartStaticChecks() {
  const src = fs.readFileSync(FLOWCHART_PATH, "utf8");
  const initCalls = [...src.matchAll(/mermaid\.initialize\(\{[\s\S]*?\}\);/g)].map((m) => m[0]);
  return [
    {
      // Mermaid htmlLabels:true 会把节点文字渲染成 <foreignObject>，导出的 SVG/PNG 在
      // Safari 下丢字；页面必须同时关掉全局与 flowchart 子配置。
      name: "mermaid.initialize 全部 htmlLabels:false（含 flowchart 子配置）",
      ok: initCalls.length > 0 && initCalls.every(
        (s) => /htmlLabels:\s*false/.test(s) && /flowchart:\s*\{\s*htmlLabels:\s*false/.test(s)
      ),
    },
    {
      // htmlLabels:false 是「foreignObject 为 0」的充要前提：页面自身不得再构造该标签。
      name: "页面不生成 foreignObject（htmlLabels:false 的必然结果）",
      ok: !/foreignObject/.test(src),
    },
    {
      // toBlob 在部分浏览器会同步抛异常（画布超限/被安全策略拒绝），必须包 try/catch，
      // 且失败提示优先取 e.name（TypeError 的 message 跨浏览器不稳定）。
      name: "canvas.toBlob 处于 try/catch 内，失败 toast 取 e.name || e.message",
      ok: /try\s*\{\s*canvas\.toBlob\(/.test(src)
        && /catch\s*\(e\)\s*\{\s*ToolBox\.showToast\('导出失败：'\s*\+\s*\(e\.name \|\| e\.message \|\| e\)/.test(src),
    },
  ];
}

// ---------------------------------------------------------------- PNG 导出的前置桩（内联原因）
// 页面顶层直接引用 XMLSerializer / Image / URL.createObjectURL / canvasExportError，
// 这些在 harness 默认路径下不存在（common.js 仅在 TB_STUB_FIDELITY=1 时注入）。
// 仅在 flowchart 的 PNG 用例里补齐；runCase 结束会清理 globalThis 新增键。
// ⚠ 必须逐条内联进 clicks，不能用外部常量 + 展开：scripts/selfcheck_false_pass.js 会
// `eval(CASES 字面量)` 做静态体检，展开会引用到未定义标识符、整份用例集被跳过判红。
const CASES = [
{
  "slug": "office/excel-formula-reference",
  "inputs": {},
  "clicks": [
    "document.getElementById('keyword').value='数字';render();"
  ],
  "expect": [
    "求平均值。 TEXT 分类：文本",
    "分类：统计 =AVERAGE(数字1,数字2,...) 求平均值。 TEXT"
  ],
  "ref": "（推翻 auto-restore）关键词过滤型页：render() 读 #keyword 后对 DATA 做顺序保持型过滤，命中项依次 appendChild 进 #list，collectStrings 采集其 innerHTML（标签→空格）⇒ 过滤态的「相邻条目」串可被断言。注入关键词「数字」⇒ 只有 SUM / AVERAGE / TEXT 命中（三处 syntax 含「数字」），于是 AVERAGE 与 TEXT 在全表中间隔 IF、VLOOKUP、INDEX、MATCH、SUMIFS、COUNTIFS 六项，在过滤态却紧邻 ⇒ 锚跨边界串「求平均值。 TEXT 分类：文本」（默认全量渲染下 AVERAGE 之后是 IF，故默认态必失配）。另一条锚「分类：统计 =AVERAGE(...) 求平均值。 TEXT」同属该边界。已实测排除的逃生项候选：`=TEXT(数字,\"0.00\")` 与 `TEXT 分类：文本 =TEXT(数字,\"0.00\") 数字转文本与格式控制。` —— 二者整段是 TEXT 条目自身的渲染结果，默认全量渲染里同样 contiguous ⇒ 判别力 0（BATCH110①「锚不得成为默认态某串的子串」）。"
},
{
  // 降级渲染（CDN 被墙 / 离线）：库缺失分支不再只留一句报错，而是把 Markdown 渲染成
  // 嵌套 <ul>，并绑定 input 实时刷新 ⇒ 注入 editor 后可在桩内断言真实产出。
  "slug": "office/mindmap",
  "inputs": {
    "editor": "# 项目知识库\n## 双向链接\n- 笔记A\n- 笔记B\n## 层级结构\n### 子层级\n- 子项"
  },
  "expect": [
    "双向链接",
    "大纲节点：7"
  ],
  "ref": "降级大纲：7 个节点（一级标题 1 + 二级标题 2 + 三级标题 1 + 列表项 3）；"
     + "「双向链接」与「大纲节点：7」都只在注入本文后出现（默认 editor 为空 ⇒ 大纲节点：0），"
     + "因此 OR 语义下两条锚各自具备判别力（不再是「库加载失败」这种默认态文案）。"
},
{
  // 反向用例：仅在本条用例内提供 window.markmap 桩 ⇒ 页面必须走 markmap 分支，
  // 不得落入降级大纲（降级分支只有库缺失时才会执行）。
  "slug": "office/mindmap",
  "markmapStub": true,
  "inputs": {
    "editor": "# 根主题\n## 分支A\n- 子节点"
  },
  "expect": [
    "MARKMAP-STUB-OK"
  ],
  "ref": "反向：markmapStub 在用例开始前把伪造的 window.markmap（Markmap.create 往 #mindmap 写 "
     + "MARKMAP-STUB-OK）+ MutationObserver 挂到 globalThis，runCase 结束后立即删除，不泄漏到其它用例。"
     + "该串只可能来自 markmap 分支；若页面误入降级分支则断言必失配。"
},
{
  "slug": "office/pdf-split",
  "inputs": {},
  "clicks": [
    "totalPages=20;document.getElementById('rangeInput').value='1,3,5-7';updateRangePreview();"
  ],
  "expect": [
    "将提取 <strong>5</strong> 页",
    "1, 3, 5, 6, 7"
  ],
  "ref": "（2026-09-24 记为「默认空态，只能断言「已选」」）updateRangePreview() 读 #rangeInput 文本 → parseRanges(input,totalPages) 解析页码区间 → 写 #rangePreview。totalPages 初始为 0（必须等真实 PDF 上传），但它是顶层 `let`，直接赋值即可；parseRanges 的越界校验按该值做（1/3/5-7 在 1..20 内合法）。独立复算：去重排序后 = [1,3,5,6,7] ⇒ 5 页。旧锚「已选」来自 updateThumbStatus() 的空态（selectedPages 为空），默认态必命中，判别力 0，已弃。"
},
{
  "slug": "office/pdf-rotate",
  "inputs": {},
  "clicks": [
    "state.numPages=1;state.rotations=[90];state.pdfjsDoc=null;rotateOne(0,180);"
  ],
  "expect": [
    "270°"
  ],
  "ref": "旋转角度累加取模：state.rotations[0]=90，rotateOne(0,180) ⇒ (90+180)%360=270，setAngle(0) 写入 #angle-0 徽标。默认态未上传 PDF 不生成缩略图 ⇒ 页面无任何 angle 徽标，「270°」只可能来自该次运算；renderThumbCanvas 无真实 pdfjsDoc，在自身 try 内失败，不影响徽标断言。"
},
// ---- office/flowchart：今天被改过两次却零用例（存储守卫 + PNG 导出失败分支）----
// 像素级 PNG 断言为何不做：harness 的 SVG 由 mermaid 桩返回固定串（无排版/字体度量）、
// canvas 由 makeEl 桩实现（toBlob 固定回调 null），既没有真实光栅化也没有像素缓冲，
// 任何「导出图与预览图逐像素一致」的断言都只是断言桩常量。故只断言「失败分支存在且可见」，
// 并由文件顶部的 flowchartStaticChecks() 断言 htmlLabels:false / try-catch / e.name 结构前提。
{
  "slug": "office/flowchart",
  "inputs": {},
  "storageFail": "quota",
  "clicks": [
    "saveCode();document.getElementById('errorBox').textContent='SAVE='+saveState.textContent;"
  ],
  "expect": [
    "SAVE=未保存（本次计算不受影响）"
  ],
  "ref": "存储守卫：storageFail:'quota' 使 localStorage.setItem 抛 QuotaExceededError，saveCode() 进 catch 把 ok 置 false，saveState 必须是「未保存（本次计算不受影响）」而不是「已保存」。探针写成 'SAVE='+saveState.textContent，若回归成宣告已保存则前缀串不成立（'已保存' 不含于 '未保存' 且整串不等）。默认态 #saveState 为空（init 只 loadSaved+渲染，不调 saveCode），故该串只可能来自本次点击。"
},
{
  "slug": "office/flowchart",
  "inputs": {},
  "clicks": [
    "globalThis.XMLSerializer=function(){return {serializeToString:function(){return '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"100\"></svg>';}};};",
    "globalThis.URL.createObjectURL=function(){return 'blob:stub';};globalThis.URL.revokeObjectURL=function(){};",
    "globalThis.canvasExportError=function(){return null;};",
    "globalThis.Image=function(){var self=this;this.onload=null;this.onerror=null;Object.defineProperty(this,'src',{set:function(){setTimeout(function(){if(self.onload)self.onload();},0);}});};",
    "window.ToolBox.showToast=function(m){document.getElementById('errorBox').textContent='TOAST:'+String(m);};",
    "var __origCE=document.createElement;document.createElement=function(t){if(String(t)==='canvas'){return {width:0,height:0,getContext:function(){return {fillStyle:'#fff',fillRect:function(){},drawImage:function(){}};},toBlob:function(cb){cb(new Blob(['png'],{type:'image/png'}));}};}if(String(t)==='a'){return {href:'',download:'',click:function(){},remove:function(){}};}return __origCE(t);};",
    "downloadPNG();"
  ],
  "expect": [
    "TOAST:已导出 PNG"
  ],
  "ref": "PNG 成功路径能跑通（结构级）：XMLSerializer/Image/createObjectURL/canvasExportError 全部补齐，toBlob 回调一个真实 Blob ⇒ 走完 a.click()+remove() 收尾并提示「已导出 PNG」。不做像素断言（见本节首注释）。htmlLabels:false ⇒ mermaid 输出不含 foreignObject，由顶部静态断言守住。"
},
{
  "slug": "office/flowchart",
  "inputs": {},
  "clicks": [
    "globalThis.XMLSerializer=function(){return {serializeToString:function(){return '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"100\"></svg>';}};};",
    "globalThis.URL.createObjectURL=function(){return 'blob:stub';};globalThis.URL.revokeObjectURL=function(){};",
    "globalThis.canvasExportError=function(){return null;};",
    "globalThis.Image=function(){var self=this;this.onload=null;this.onerror=null;Object.defineProperty(this,'src',{set:function(){setTimeout(function(){if(self.onload)self.onload();},0);}});};",
    "window.ToolBox.showToast=function(m){document.getElementById('errorBox').textContent='TOAST:'+String(m);};",
    "downloadPNG();"
  ],
  "expect": [
    "TOAST:导出失败：画布可能超出浏览器上限，请缩小画布后重试。"
  ],
  "ref": "PNG 失败分支 ①（toBlob 回调 null）：makeEl 的 canvas 桩固定 cb(null)，页面据此判定画布超限并弹可见 toast。默认态不调 downloadPNG、且无该文案 ⇒ 判别力来自本次点击。"
},
{
  "slug": "office/flowchart",
  "inputs": {},
  "clicks": [
    "globalThis.XMLSerializer=function(){return {serializeToString:function(){return '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"100\"></svg>';}};};",
    "globalThis.URL.createObjectURL=function(){return 'blob:stub';};globalThis.URL.revokeObjectURL=function(){};",
    "globalThis.canvasExportError=function(){return null;};",
    "globalThis.Image=function(){var self=this;this.onload=null;this.onerror=null;Object.defineProperty(this,'src',{set:function(){setTimeout(function(){if(self.onload)self.onload();},0);}});};",
    "window.ToolBox.showToast=function(m){document.getElementById('errorBox').textContent='TOAST:'+String(m);};",
    "var __origCE2=document.createElement;document.createElement=function(t){if(String(t)==='canvas'){return {width:0,height:0,getContext:function(){return {fillStyle:'#fff',fillRect:function(){},drawImage:function(){}};},toBlob:null};}return __origCE2(t);};",
    "downloadPNG();"
  ],
  "expect": [
    "TOAST:导出失败：TypeError"
  ],
  "ref": "PNG 失败分支 ②（注入 canvas.toBlob=null，即浏览器未实现/被安全策略禁用）：try 内抛 TypeError，catch 必须用 e.name || e.message 拼提示 ⇒ 文案恰为「导出失败：TypeError」。若回归成只用 e.message，则出现「canvas.toBlob is not a function」而不匹配本串。"
},
{
  "slug": "office/mindmap",
  "inputs": {},
  "clicks": [
    "var s=window.__mmTreeStats(['# 主题','## 分支一','- 子节点A','- 子节点B','## 分支二','- 子节点C'].join('\\n'));document.getElementById('mmRefTitle').textContent=s?('N:'+s.n+'|E:'+s.e+'|D:'+s.d):'NULL';"
  ],
  "expect": ["N:7|E:6|D:3"],
  "ref": "深度解析算例复算：1 个 # + 2 个 ## + 3 个 - → 节点数 7、边数 6、层深 3。默认态 mmRefTitle 为静态标题、不含该串 ⇒ 判别力来自本次点击。"
}
];
// 单例超时：office 两个 PDF 页的「注入失败态」会等待 pdfjsReady 轮询，该 Promise 在
// harness 内永不 settle，Node 事件循环一空就静默 exit 0（判别器报「无统计行」）。
// 用 Promise.race 强制每个用例在有限时间内落地：超时计入 FAIL（不放宽判定），
// 并让底层计时器在用例结束后被清理，避免正常路径被拖慢。
const CASE_TIMEOUT = Number(process.env.TB_OFFICE_CASE_TIMEOUT || 5000);
function runCaseWithTimeout(c) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error("CASE_TIMEOUT " + CASE_TIMEOUT + "ms")), CASE_TIMEOUT);
  });
  return Promise.race([runCase(c), timeout]).finally(() => clearTimeout(timer));
}

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    // markmapStub：仅该条用例内提供「库存在」环境（反向验证不进入降级分支）。
    // 必须在 runCase 之前挂到 globalThis（runCase 把它当 window），并在用例结束后删除，
    // 否则会泄漏到后续用例（runCase 的 finally 只清理用例期间新增的键，清理不到预先存在的）。
    const withMarkmap = !!c.markmapStub;
    const prevMarkmap = globalThis.markmap;
    const prevMO = globalThis.MutationObserver;
    if (withMarkmap) {
      globalThis.markmap = {
        Transformer: function () {
          this.transform = function (md) { return { root: { content: String(md || "") } }; };
        },
        Markmap: {
          create: function (svg) {
            if (svg) svg.innerHTML = '<div class="mm-stub">MARKMAP-STUB-OK</div>';
            return { setData: function () {} };
          },
        },
      };
      globalThis.MutationObserver = function () { return { observe: function () {}, disconnect: function () {} }; };
    }
    try {
      const r = await runCaseWithTimeout(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    } finally {
      if (withMarkmap) {
        // 必须还原而非一律 delete：MutationObserver 是运行环境预置全局（jsdom 提供），
        // delete 会让后续 flowchart 用例整页初始化失败。
        if (prevMarkmap === undefined) { try { delete globalThis.markmap; } catch (e) {} }
        else { globalThis.markmap = prevMarkmap; }
        if (prevMO === undefined) { try { delete globalThis.MutationObserver; } catch (e) {} }
        else { globalThis.MutationObserver = prevMO; }
      }
    }
  }

  // 结构前提断言（PNG 导出的可测部分）：与用例一起计入退出码，缺一即红。
  const stat = flowchartStaticChecks();
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== office calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
