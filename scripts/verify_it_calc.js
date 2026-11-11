#!/usr/bin/env node
/**
 * it 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 与 scripts/verify_calc.js 的区别：
 *   - verify_calc.js 是「冒烟测试」：只跑 calcTool() 检查不报错
 *   - 本脚本是「正确性验证」：注入已知输入，用独立实现/权威测试向量断言输出
 *
 * 用法：
 *   node scripts/verify_it_calc.js            # 跑全部用例
 *   node scripts/verify_it_calc.js base64 md5 # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）
 *   expect  —— 期望子串，命中任意一个「输出元素」（value 或 innerHTML）即通过
 *   ref     —— 该期望值的来源说明（权威向量 / 独立实现 / 标准文档），必填，便于复核
 */
const fs = require("fs");
const path = require("path");
// 运行期生成 id 判定（与 audit_verify_input_ids.js 共用同一套模板解析，避免两处正则漂移）。
// 仅用于注入参数合法性校验：动态 id 无法静态判存在，必须放行，否则会误伤 JS 拼控件的页。
const { isDynamicId } = require(path.join(__dirname, "lib_dynamic_defaults.js"));

// §7.4 harness 缺口补丁：浏览器标准 API `btoa`/`atob` 二进制串语义（btoa 入参为 latin1 二进制串、
// atob 出参亦为 latin1 二进制串），与页面惯用法 `btoa(unescape(encodeURIComponent(s)))`
// / `decodeURIComponent(escape(window.atob(s)))` 完全对齐。win===globalThis ⇒ window.atob 同步可用。
//
// 为何「始终覆盖」而非「仅当全局未定义时注入」：Node 22+ 自带原生 atob/btoa，但原生实现比浏览器
// 严格——对 base64url 解码时若填充公式多补了 `=`（部分页面 `new Array(5-(len%4)).join('=')` 在
// len%4===0 时会误补 4 个 `=`），原生 atob 直接抛 `Invalid character`，而浏览器 atob 对尾部多余 `=`
// 宽松忽略（线上正常）。为保证 harness 与浏览器生产行为一致（不误伤线上正常的页面），此处始终以
// 宽松的 Buffer 版覆盖：Buffer.from(b64,'base64') 容忍尾部多余 `=` 与非常规字符，等价于浏览器语义。
// 宽松是严格的超集，不会使任何既有用例由通过变为失败。
{
  const _atob = (b64) => Buffer.from(String(b64), "base64").toString("latin1");
  const _btoa = (bin) => Buffer.from(String(bin), "latin1").toString("base64");
  globalThis.atob = _atob;
  globalThis.btoa = _btoa;
}
// MutationObserver：真浏览器用于监听 DOM 变化（本项目仅用于监听 data-theme 暗色切换重绘图），
// 与数值计算逻辑无关。harness 无头环境不建模，页面顶层 `new MutationObserver(...)` 会 init 失败
// （如 astronomy/earth-curvature）。提供 no-op 桩使此类页面可正常加载；observe 为 no-op，
// 不影响计算（计算由 oninput 注入触发，不依赖 theme 变化回调）。仅当全局未定义时才注入。
if (typeof globalThis.MutationObserver === "undefined") {
  globalThis.MutationObserver = class {
    constructor(cb) { this._cb = cb; }
    observe() {}
    disconnect() {}
    takeRecords() { return []; }
  };
}

// Mermaid：office/flowchart.html 顶层首句就是 `mermaid.initialize({...})`，而页面依赖 CDN
// 加载 mermaid，harness 不加载外部脚本 ⇒ 缺桩时页面脚本在首句抛 ReferenceError，整页函数
// 一个都导不出（`saveCode`/`downloadPNG` 均 undefined），只能零用例。
// 这里只提供最小形状：initialize 记录配置、render 返回合法 SVG（不含 foreignObject，与页面
// htmlLabels:false 的输出形态一致）、parse 返回 resolved。像素级渲染正确性不做断言（harness
// 无真实 SVG 布局与字体度量），交真机验证。
if (typeof globalThis.mermaid === "undefined") {
  globalThis.mermaid = {
    initialize(config) { this._config = config || {}; },
    render() {
      return Promise.resolve({
        svg: '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100"></svg>',
        bindFunctions() {},
      });
    },
    parse() { return Promise.resolve(true); },
  };
}

const ROOT = path.join(__dirname, "..");

// 共享条码库在页面里由 <script src> 加载，harness 不加载外部脚本。
// 这里在独立 vm 沙箱里加载一次，只暴露给需要直接测编码库的用例（Code128 A/B 切换），
// 不覆盖页面用的 ToolBoxBarcode 桩，避免影响其他条码页用例。
try {
  const _vm = require("vm");
  const _sandbox = {};
  _vm.runInNewContext(fs.readFileSync(path.join(ROOT, "js/barcode-lib.js"), "utf8"), _sandbox);
  globalThis.__tbBarcodeLibForVerify = _sandbox.ToolBoxBarcode || null;
} catch (e) {
  globalThis.__tbBarcodeLibForVerify = null;
}

// ToolBox 早期 API 桩（/js/toolbox-stub.js）源缓存：页面已将该桩外链化（<script src>），
// 本 harness 不加载外部脚本，故在用例上下文里显式以同内容注入，使 harness 的 window.ToolBox
// 与生产设备一致：补全 qs/qsa/debounce/resolveCanvasColor/canvasColorWithAlpha/i18nText 等
// 纯函数助手。否则依赖这些助手的页面（如 finance/compound-interest 等）在门禁下误报失败。
let _toolboxStubSrc = null;
function loadToolboxStubSrc() {
  if (_toolboxStubSrc === null) {
    try {
      const p = path.join(ROOT, "js", "toolbox-stub.js");
      _toolboxStubSrc = fs.existsSync(p) ? fs.readFileSync(p, "utf8") : "";
    } catch (e) { _toolboxStubSrc = ""; }
  }
  return _toolboxStubSrc;
}
// 共享层 /js/common.js 源缓存：TB_STUB_FIDELITY=1 时按线上真实顺序注入（defer → 页面内联之后）。
// 目的：复现「页面顶层同名函数被共享层全局赋值覆盖」这类静默遮蔽（如 fmtNum），
// 避免 harness 因为没加载 common.js 而把生产缺陷跑成绿。
//
// 开关在模块加载时一次性读取：runCase 期间页面脚本可能把 globalThis.process 覆盖成页面自己的
// 函数（如 it/caesar-cipher 的 `process=function(){…}`，线上无害——那里 process 本就是页面函数），
// 若在用例执行中再访问 process.env 会 TypeError、整条门禁崩掉。
const TB_STUB_FIDELITY = process.env.TB_STUB_FIDELITY === "1";
const TB_FIDELITY_DEBUG = !!process.env.TB_FIDELITY_DEBUG;
const NODE_STDERR = process.stderr;
let _commonSrc = null;
function loadCommonSrc() {
  if (_commonSrc === null) {
    try {
      const p = path.join(ROOT, "js", "common.js");
      _commonSrc = fs.existsSync(p) ? fs.readFileSync(p, "utf8") : "";
    } catch (e) { _commonSrc = ""; }
  }
  return _commonSrc;
}
const TOOLS_DIR = path.join(ROOT, "tools");

// ---------------------------------------------------------------- 固定基准日（根治日期漂移）
// 门禁用例不得依赖真实「今天」：真实日期每推进一天，相对今天推算的绝对日期期望就会过期一天，
// 导致 CI 偶发/漂移失败（已发生 fire/livestock/cleaning/pediatrics/travel 五道门禁）。
// 这里把 new Date() / Date.now() 冻结到一个固定基准日，使所有日期型页面在 CI 永远算同一天、完全确定。
// 约定：用例断言应「与今天无关」（时长/计数/静态名称/状态标题）或「基于基准日的相对结果」。
const REAL_DATE = Date;
const FIXED_NOW = Date.parse("2024-06-15T00:00:00Z");
function FrozenDate(...args) {
  // 无参构造 → 固定基准日；带参构造（new Date(t) / new Date(y,m,d)）按真实 Date 透传
  if (args.length === 0) return new REAL_DATE(FIXED_NOW);
  return new REAL_DATE(...args);
}
FrozenDate.now = () => FIXED_NOW;
FrozenDate.parse = REAL_DATE.parse.bind(REAL_DATE);
FrozenDate.UTC = REAL_DATE.UTC.bind(REAL_DATE);
FrozenDate.prototype = REAL_DATE.prototype;

// 根治（续）：把 Math.random 也替换成「确定性种子 PRNG」，并在每个用例前重置种子。
// 原因：Math.random 类页面（随机推荐 / 随机生成器 / 随机抽题等）在本地与 CI 的随机序列不同，
// 且 Node 版本（ICU / V8）差异会让「断言随机输出值」的用例偶发落空（已发生 niche 等门禁）。
// 固定种子 + 每用例重置 → 任何页面在任意进程、任意环境下都得到完全一致的随机序列，门禁可重现。
let _rngState = 0;
function _rngReset() { _rngState = 0x9e3779b9 >>> 0; }
(function installSeededRandom() {
  _rngReset();
  const next = () => {
    _rngState = (_rngState + 0x6d2b79f5) | 0;
    let t = Math.imul(_rngState ^ (_rngState >>> 15), 1 | _rngState);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  Math.random = next;
})();


// ---------------------------------------------------------------- 用例
const CASES = [
  {
    slug: "it/calc-8",
    clicks: ["var vals=[null,false,'123',1e20,-1e20],ok=0;vals.forEach(function(v){var h=btoa(JSON.stringify({alg:'none'})).replace(/=/g,''),p=btoa(JSON.stringify({exp:v})).replace(/=/g,'');document.getElementById('jwtInput').value=h+'.'+p+'.sig';decodeJwt();var out=document.getElementById('result').innerHTML;if(out.indexOf('无效 exp 值')>=0&&out.indexOf('未过期')<0)ok++;});document.getElementById('__tbProbe').textContent='EXPTYPE '+ok;"],
    expect: ["EXPTYPE 5"],
    ref: "RFC 7519 NumericDate 必须为数字，null、布尔值和数字字符串无效；超出 JavaScript Date 范围不得误判未过期。"
  },
  {
    "slug": "it/calc-8",
    "clicks": ["document.getElementById('jwtInput').value='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ6ZXJvIiwiZXhwIjowfQ.sig';decodeJwt();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='EXPT0 '+(h.indexOf('已过期')>=0&&h.indexOf('1970')>=0?'OK':'BAD');"],
    "expect": ["EXPT0 OK"],
    "ref": "审计修复回归：exp:0（Unix 纪元，必已过期）旧实现因真值判断 `payload.exp` 为假被完全忽略，不输出过期信息；修复后 hasOwnProperty 命中，显示 1970 年并判「已过期」。默认样例 JWT 无 exp、不含 EXPT0 探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/calc-8",
    "clicks": ["document.getElementById('jwtInput').value='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYWQiLCJleHAiOiJiYWQifQ.sig';decodeJwt();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='EXPTBAD '+(h.indexOf('无效 exp 值')>=0&&h.indexOf('未过期')<0?'OK':'BAD');"],
    "expect": ["EXPTBAD OK"],
    "ref": "审计修复回归：exp:\"bad\" 旧实现 new Date(NaN) 得 Invalid Date，比较恒 false 被标「未过期」；修复后 Number(exp) 非有限数时显示「无效 exp 值 / 无效」，不再误标未过期。默认样例无 EXPTBAD 探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/calc-8",
    "clicks": ["document.getElementById('jwtInput').value='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ6ZXJvIiwiZXhwIjowfQ.sig';decodeJwt();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='EXPT0 '+(h.indexOf('已过期')>=0&&h.indexOf('1970')>=0?'OK':'BAD');"],
    "expect": ["EXPT0 OK"],
    "ref": "审计修复回归：exp:0（Unix 纪元，必已过期）旧实现因真值判断 `payload.exp` 为假被完全忽略，不输出过期信息；修复后 hasOwnProperty 命中，显示 1970 年并判「已过期」。默认样例 JWT 无 exp、不含 EXPT0 探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/calc-8",
    "clicks": ["document.getElementById('jwtInput').value='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYWQiLCJleHAiOiJiYWQifQ.sig';decodeJwt();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='EXPTBAD '+(h.indexOf('无效 exp 值')>=0&&h.indexOf('未过期')<0?'OK':'BAD');"],
    "expect": ["EXPTBAD OK"],
    "ref": "审计修复回归：exp:\"bad\" 旧实现 new Date(NaN) 得 Invalid Date，比较恒 false 被标「未过期」；修复后 Number(exp) 非有限数时显示「无效 exp 值 / 无效」，不再误标未过期。默认样例无 EXPTBAD 探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/email-normalizer",
    "inputs": {"input": "user.name+tag@notgmail.com"},
    "clicks": ["document.getElementById('opt_gmail').checked=true;normalize();var a=String(document.getElementById('afterOut').textContent||'');document.getElementById('__tbProbe').textContent='EMGM '+(a==='user.name+tag@notgmail.com'?'OK':'BAD');"],
    "expect": ["EMGM OK"],
    "ref": "审计修复回归：旧实现 /gmail\\.com$/ 把 notgmail.com 误判为 Gmail，去掉点号与 + 标签得到 username@notgmail.com；修复后精确匹配域名，保留原本地名。修复前 BAD。探针默认态不存在 ⇒ 零逃生。"
  },
  {
    "slug": "it/email-normalizer",
    "inputs": {"input": "A.B@gmail.com"},
    "clicks": ["document.getElementById('__tbProbe').textContent='EMCHG '+(typeof __email_normalizerGmailChange==='function'?'OK':'BAD');"],
    "expect": ["EMCHG OK"],
    "ref": "审计修复回归：Gmail 归一选项原无 change 事件，取消勾选后结果不刷新；修复后绑定 onchange 调 __email_normalizerGmailChange 即时重算。修复前函数不存在 BAD。探针默认态不存在 ⇒ 零逃生。"
  },

  {
    "slug": "it/css-escape",
    "inputs": {"input": "-1a", "mode": "identifier"},
    "clicks": ["esc();var o=String(document.getElementById('output').value||'');document.getElementById('__tbProbe').textContent='CSID '+(o.indexOf('\\\\2d ')>=0?'OK':'BAD');"],
    "expect": ["CSID OK"],
    "ref": "审计修复回归：CSS 标识符首位为 - 且次位为数字时（-1a）会被解析成数字 token，旧实现原样输出 -1a；修复后转义首位为 \\2d （即 \\2d 1a）。修复前 BAD。探针默认态不存在 ⇒ 零逃生。"
  },
  {
    "slug": "it/c-string-escape",
    "inputs": {"input": "\\x"},
    "clicks": ["var ok=false;try{unesc();ok=true;}catch(e){};var o=String(document.getElementById('output').value||'');document.getElementById('__tbProbe').textContent='CSXBIN '+(ok&&o.indexOf('\\\\x')>=0?'OK':'BAD');"],
    "expect": ["CSXBIN OK"],
    "ref": "审计修复回归：反转义 \\x 后无十六进制数字时，旧实现 parseInt(\"\",16)=NaN ⇒ String.fromCodePoint(NaN) 抛 RangeError、无输出；修复后保留字面 \\x 且不抛错。修复前 BAD。探针串默认态不存在 ⇒ 零逃生。"
  },
  {
    "slug": "it/c-string-escape",
    "inputs": {"input": "a\"b", "qtype": "double"},
    "clicks": ["esc();var before=String(document.getElementById('output').value||'');document.getElementById('qtype').value='single';var ok=typeof __c_string_escapeQtypeChange==='function';if(ok)__c_string_escapeQtypeChange();var after=String(document.getElementById('output').value||'');document.getElementById('__tbProbe').textContent='CSQQ '+(ok&&before!==after&&before.indexOf('\\\\\"')>=0&&after.indexOf('\\\\\"')<0?'OK':'BAD');"],
    "expect": ["CSQQ OK"],
    "ref": "审计修复回归：引号类型下拉原无 change 事件，切换后输出仍用旧引号；修复后 onchange 调 __c_string_escapeQtypeChange 即时刷新（双引号包裹→单引号包裹）。修复前函数不存在 BAD。探针默认态不存在 ⇒ 零逃生。"
  },
  {
    "slug": "it/css-escape",
    "inputs": {"input": "\\FFFFFF"},
    "clicks": ["var input=document.getElementById('input'),output=document.getElementById('output');var cases=[['\\\\FFFFFF','\uFFFD'],['\\\\0','\uFFFD'],['\\\\d800','\uFFFD'],['\\\\10ffff',String.fromCodePoint(0x10ffff)],['\\\\41\\tB','AB'],['\\\\41 B','AB']];var ok=cases.every(function(c){input.value=c[0];unesc();return output.value===c[1];});document.getElementById('__tbProbe').textContent='CSHEX '+(ok?'OK':'BAD');"],
    "expect": ["CSHEX OK"],
    "ref": "CSS Syntax 反转义：越界、零及代理码点替换为 U+FFFD；合法最大码点保留，十六进制后的制表符或空格作为终止符消费。"
  },
  {
    "slug": "it/css-escape",
    "inputs": {"input": "1abc", "mode": "identifier"},
    "clicks": ["esc();var before=String(document.getElementById('output').value||'');document.getElementById('mode').value='string';var ok=typeof __cssEscapeModeChange==='function';if(ok)__cssEscapeModeChange();var after=String(document.getElementById('output').value||'');document.getElementById('__tbProbe').textContent='CSMODE '+(ok&&before!==after?'OK':'BAD');"],
    "expect": ["CSMODE OK"],
    "ref": "审计修复回归：模式下拉原无 change 事件，切换 identifier→string 后输出不刷新；修复后 onchange 调 __cssEscapeModeChange 即时刷新（.cls→\\.cls）。修复前函数不存在 BAD。探针默认态不存在 ⇒ 零逃生。"
  },
{
    "slug": "it/playfair-cipher",
    "clicks": ["document.getElementById('__tbProbe').textContent='PLF score='+__playfair_cipherScore('FAILED');"],
    "expect": ["PLF score=1"],
    "ref": "复核失败重做·Playfair 明文误判：密钥 PLAYFAIR、明文 FAILED，加密再解密得到合法明文 FAILED，原 Score 命中 Failed 判 0 ⇒ 历史/趋势/CSV 全误标未通过。修复后 Score 只保留明确业务失败标识（⚠|无效|未通过|不正确|must be|请填写…），移除 Failed/失败/错误/Invalid 等用户文本词 ⇒ 判 1。默认态无探针串 ⇒ 零逃生。"
  },
{
    "slug": "it/aes-encryptor",
    "clicks": ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'encInput',type:'textarea',value:'FAILED PLAINTEXT'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};var __o=document.getElementById('output');if(__o){__o.textContent='1234abcd previous ciphertext';}__aes_encryptorLastBytes=0;__aes_encryptor_last=0;__aes_encryptorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='AESFAIL hist='+__cap.length;"],
    "expect": ["AESFAIL hist=0"],
    "ref": "复核失败重做·第46批 AES 空态/失败不清算旧结果：模拟加密失败（__aes_encryptorLastBytes=0）但结果区仍留上次解密文本，旧实现无成功守卫仍会把旧文本+旧字节数写进历史 ⇒ hist=1；修复后 Extras 先判 __aes_encryptorLastBytes>0 才记录 ⇒ hist=0。探针自建 TBKit/querySelectorAll 桩走真实 __aes_encryptorExtras，默认态无探针串 ⇒ 零逃生。"
  },
{
    "slug": "it/aes-encryptor",
    "clicks": ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'encInput',type:'textarea',value:'Hello AES'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};var __o=document.getElementById('output');if(__o){__o.textContent='CIPHERTEXT9';}__aes_encryptorLastBytes=0;__aes_encryptor_last=0;__aes_encryptor_d0=function(){__aes_encryptorLastBytes=11;return undefined;};decrypt();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='AESDEC hist='+__cap.length;"],
    "expect": ["AESDEC hist=1"],
    "ref": "复核失败重做·第46批 AES 解密成功入历史：旧实现只包装 encrypt，decrypt 成功不触发 Extras ⇒ 调用 decrypt 不会写历史 hist=0；修复后包装 decrypt 并在其 Promise/同步返回后触发 Extras，本例把 __aes_encryptor_d0 替换为同步桩设置成功字节数，走真实包装 ⇒ hist=1。探针串依赖修复引入的 decrypt 包装，默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "it/matrix-transpose",
    clicks: ["var __oq=document.querySelectorAll;__lastTranspose=[[1,2],[3,4]];document.getElementById('rows').value='0';calculate();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='MXCLR cleared='+(__lastTranspose===null?'Y':'N');"],
    expect: ["MXCLR cleared=Y"],
    ref: "复核失败重做·F-N189 第46批 矩阵转置：有效转置后把行数改为 0 再计算，页面提示行列须 1–6 整数，但旧实现不清 __lastTranspose，导出仍下载旧 CSV；修复后两个失效分支均清空缓存。探针 __lastTranspose===null ⇒ 修复前 N、修复后 Y。"
  },
  {
    slug: "it/rsa",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{\"id\":\"encInput\",\"type\":\"text\",\"value\":\"FAILED\"}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('encInput').value='FAILED';document.getElementById('encResult').textContent='FAILED';__rsaLastBytes=6;__rsaExtras(true,true);document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='RSAPLAIN score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["RSAPLAIN score=1"],
    ref: "RSA 解密成功状态应覆盖明文中出现的失败关键词；真实 WebCrypto 往返与验签失败另由 _verify_rsa_runtime.mjs 覆盖。"
  },
  {
    slug: "it/json-diff",
    inputs: {},
    clicks: ["var a=Array.from({length:448},function(_,i){return i}),b=a.slice().reverse(),d=deepDiff(a,b,'items',true);document.getElementById('__tbProbe').textContent='BIGMATCH len='+a.length+' diffs='+d.length;"],
    expect: ["BIGMATCH len=448 diffs=0"],
    ref: "IT-N396 复核：超过 LCS 规模保护阈值的完全逆序数组，选择按内容匹配仍应判无差异。",
  },
  {
    slug: "it/json-diff",
    inputs: {},
    clicks: ["var a=Array.from({length:448},function(_,i){return i%7}),b=a.slice().reverse();b[0]=999;var d=deepDiff(a,b,'items',true);document.getElementById('__tbProbe').textContent='BIGCHANGE diffs='+d.length+' op='+d[0].op+' from='+d[0].from+' to='+d[0].to;"],
    expect: ["BIGCHANGE diffs=1 op=mod from=6 to=999"],
    ref: "IT-N396 复核：大数组含重复值时多重集匹配不能吞掉真实变化。",
  },
  // ===== 复核失败·第一批重做·续批2（IT-N401/N403 与 文本清理器历史快照）=====
  {
    slug: "it/html-to-markdown",
    htmlDom: true,
    inputs: {htmlInput: "<p><strong>Hello</strong> <em>world</em></p>"},
    clicks: ["convert();document.getElementById('__tbProbe').textContent='SPACE='+document.getElementById('mdOutput').value;"],
    expect: ["SPACE=**Hello** _world_"],
    ref: "IT-N401 复核：相邻行内元素之间独立空白文本节点必须保留，避免加粗与斜体的词粘连。",
  },
  {
    slug: "it/html-to-markdown",
    htmlDom: true,
    inputs: {"htmlInput": "<ul><li>a<br>b</li></ul>"},
    clicks: ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('__tbProbe').textContent='ULBR='+(v.indexOf('- a  '+String.fromCharCode(10)+'  b')>=0?1:0)+' FLAT='+(v.indexOf('- a'+String.fromCharCode(10)+'  b')>=0?1:0)+' q='+(document.getElementById('htmlInput').value.indexOf('<br>')>=0?1:0);"],
    expect: ["ULBR=1 FLAT=0"],
    ref: "IT-N401/N403 复核重做：列表项内 <br> 必须保留 Markdown 硬换行（行尾两空格 + 换行）。旧 BR 直接返回「两空格+换行」，列表处理逐行 replace(/\\s+$/,'') 把这两个空格删掉 ⇒ 输出 - a\\n  b（渲染时仍合并成一行）。现 BR 用私有控制字符占位，中间所有 trim/尾空白清理都碰不到，convert() 末尾统一还原。ULBR=1 判 v 含 - a(两空格)\\n(两空格)b，FLAT=0 判不含无硬换行的普通换行，q=1 绑注入值。blob 会折叠空白，故判据全在页面内完成。",
  },
  {
    slug: "it/html-to-markdown",
    htmlDom: true,
    inputs: {"htmlInput": "<p>Hello <strong>world </strong>again</p>"},
    clicks: ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('__tbProbe').textContent='STRONG='+v+' q='+(document.getElementById('htmlInput').value.indexOf('<strong>')>=0?1:0);"],
    expect: ["STRONG=Hello **world** again q=1"],
    ref: "IT-N401 复核重做：行内强调的边界空白必须留在标记之外。旧实现 innerMarkdown(...).trim() 吃掉 <strong>world </strong> 的尾空格 ⇒ Hello **world**again 单词粘连。现 inlineMark 提取 lead/trail 并拼在标记外 ⇒ Hello **world** again。q=1 绑注入的 <strong> 标签。",
  },
  {
    slug: "it/html-to-markdown",
    htmlDom: true,
    inputs: {"htmlInput": "<p><em> italic </em>next</p>"},
    clicks: ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('__tbProbe').textContent='EM='+v+' q='+(document.getElementById('htmlInput').value.indexOf('<em>')>=0?1:0);"],
    expect: ["EM=_italic_ next q=1"],
    ref: "IT-N401 复核重做：<em> italic </em>next 旧输出 _italic_next（既丢空格又因标记紧跟单词无法形成斜体）。现输出 _italic_ next，斜体边界合法且 next 前有空格。与 STRONG 用例共同覆盖行内格式两侧空白。",
  },
  {
    slug: "it/html-to-markdown",
    htmlDom: true,
    inputs: {"htmlInput": "<p>x <del> gone </del>y</p>"},
    clicks: ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('__tbProbe').textContent='DEL='+v+' q='+(document.getElementById('htmlInput').value.indexOf('<del>')>=0?1:0);"],
    expect: ["DEL=x ~~gone~~ y q=1"],
    ref: "IT-N401 复核重做（同族护栏）：删除线 <del>/<s>/<strike> 走同一 inlineMark，边界空白同样移到标记外，避免只修 strong/em 而留下另一分支的同类缺陷。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {"input-text": "  OLD TEXT  "},
    clicks: ["var pick,cap;TBKit={util:{isEn:function(){return false},diffBox:function(){}},matrix:{table:function(){}},chart:{line:function(){}},history:{record:function(x){cap=x},last:function(){return null},list:function(){return []},mount:function(h,f){pick=f}}};var input=document.getElementById('input-text'),trim=document.getElementById('opt-trim'),output=document.getElementById('output-text');trim.checked=true;var oq=document.querySelectorAll;document.querySelectorAll=function(s){if(s==='input[id],select[id],textarea[id]')return [trim,input];if(s==='input[type=checkbox],input[type=radio]')return [trim];return []};output.tagName='TEXTAREA';__text_cleaner_last=0;executeClean();input.value='  NEW TEXT  ';trim.checked=false;if(pick)pick(cap);document.querySelectorAll=oq;document.getElementById('__tbProbe').textContent='RESTORE='+input.value.replace(/ /g,'~')+' OUT='+output.value+' CHECK='+trim.checked+' PICK='+!!pick;"],
    expect: ["RESTORE=~~OLD~TEXT~~ OUT=OLD TEXT CHECK=true PICK=true"],
    ref: "文本清理器历史：记录原文与选项后修改，调用历史回填入口须恢复旧文本及选项并重新清理。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {},
    clicks: ["var __cap=null;var __els=[];for(var i=0;i<14;i++){__els.push({id:'opt-cb'+i,type:'checkbox',checked:(i%2===0),value:'1'});}__els.push({id:'input-text',type:'textarea',value:'  NEW TEXT  '});var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output-text').textContent='CLEANED TEXT';globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(r){__cap=r;},mount:function(){}},preset:{bar:function(){}}};__text_cleaner_last=0;__text_cleanerExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='TC='+(__cap?Object.keys(__cap).length:'NONE')+' HAS='+(__cap&&__cap['input-text']!==undefined?'Y':'N')+' VAL='+(__cap?String(__cap['input-text']).replace(/ /g,'~'):'')+' CB0='+(__cap?String(__cap['opt-cb0']):'');"],
    expect: ["TC=17 HAS=Y VAL=~~NEW~TEXT~~ CB0=1"],
    ref: "IT 历史复用·文本清理器复核重做：快照按 DOM 顺序先收 14 个复选框再收 textarea input-text，旧实现 keys.slice(0,12) 同时用于保存/去重/渲染 ⇒ 历史记录里根本没有原文，点击历史只会重新清理当前 NEW TEXT。现「保存全量 allKeys」与「展示列 showKeys 限 12」分离：桩捕获的 rec 含 15 个字段 + 结果 + __tbScore = 17 键、input-text 值为两空格 NEW TEXT 两空格（探针把空格换成 ~ 防 blob 折叠）、首个复选框也在。旧代码下 TC=14 且 HAS=N ⇒ 本例必然 FAIL。",
  },
  // ===== 复核失败·第一批重做·续批（IT-N373 / N376 / N378 / N417）=====
  {
    slug: "it/confidence-interval",
    inputs: {mean: "50", std: "8", n: "2", conf: "0.999", dist: "t"},
    expect: ["临界值=636.619"],
    ref: "99.9% 双侧 t，df=1，t=cot(π×0.0005)=636.619；旧表缺少 0.0005 列，输出无效值。",
  },
  {
    slug: "it/confidence-interval",
    inputs: {mean: "50", std: "8", n: "11", conf: "0.999", dist: "t"},
    expect: ["临界值=4.587"],
    ref: "99.9% 双侧 t，df=10，临界值约 4.587，验证非单自由度的表项。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: {"N": "2000", "K": "1500", "n": "1500", "k": "749"},
    expect: ["exp(1035.8369 + −∞ − 1120.7877) = 0"],
    ref: "IT-N373 复核重做：N=2000,K=1500,n=1500,k=749 ⇒ C(500,751)=0 是不可能事件。旧 combInfo 把 logComb 返回的 −Infinity 塞成 ln:0（对应组合数 1），步骤 4 写成 exp(1035.8369 + 0.0000 − 1120.7877) = 0，左侧实际约 1.28e-37，等式不成立。现 ln(0) 记作 −∞ 并追加「不可能事件」说明，exp(a + (−∞) − b) = 0 自洽。expect 含依赖该组大参数的 ln 数值与 −∞，默认 N=52/K=13/n=5/k=2 不命中。",
  },
  {
    slug: "it/confidence-interval",
    inputs: {"mean": "50", "std": "8", "n": "1", "conf": "0.95", "dist": "auto"},
    expect: ["t 分布自由度 df = n−1 需 ≥ 1；请使用至少 2 个样本。仅当总体标准差已知时，n = 1 才可使用 z 分布"],
    ref: "IT-N376 复核重做：n=1 且 auto 会选 t 分布，df=0 使 t 临界值为 NaN，旧实现把 NaN 洗成「—」输出「[ — , — ]」这种无效结果。现明确拒绝并给出可执行建议。默认 n=30/d auto 输出有效区间，不命中。",
  },
  {
    slug: "it/confidence-interval",
    inputs: {"mean": "50", "std": "8", "n": "2.5", "conf": "0.95", "dist": "auto"},
    expect: ["请填写均值、标准差与样本量（n 为 ≥ 1 的整数、s > 0）"],
    ref: "IT-N376 复核重做：样本量必须是整数。旧校验只判 n<1，n=2.5 会被当作有效样本量参与 √n 与 df 内插；现 !Number.isInteger(n) 直接拒绝。默认 n=30 不产生该提示。",
  },
  {
    slug: "it/confidence-interval",
    inputs: {"mean": "50", "std": "8", "n": "1", "conf": "0.95", "dist": "z"},
    expect: ["[ 34.320 , 65.680 ]"],
    ref: "IT-N376 复核重做（对照组）：显式选 z 且总体标准差已知时 n=1 可算；50 ± 1.960×8 = [34.320, 65.680]。默认 n=30/d auto 区间不同，不命中。",
  },
  {
    slug: "it/margin-of-error",
    inputs: {"n": "1000.9", "p": "0.5", "conf": "0.95", "N": "1000"},
    expect: ["n must be an integer ≥ 2 (decimals are not accepted)."],
    ref: "IT-N378 复核重做：n=1000.9、总体 N=1000。旧 parseInt 把 n 静默截成 1000，恰好等于 N ⇒ 误判「全查」并显示误差 0，绕过整数与 n≤N 约束。现 nRaw + Number + Number.isInteger 校验，小数直接拒绝。默认 n=1000/N 空 输出有效误差，不命中。",
  },
  {
    slug: "it/margin-of-error",
    inputs: {"n": "1000", "p": "0.5", "conf": "0.95", "N": "1000"},
    expect: ["误差范围 E = ±0 (0.00%)"],
    ref: "IT-N378 复核重做（对照组）：合法的 n=N=1000 全查仍应给出误差 0（有限总体校正因子 √[(N−n)/(N−1)]=0），新整数校验不得破坏既有合法路径。默认 N 为空、误差约 ±0.031，不命中。",
  },
  {
    slug: "it/msisdn-lookup",
    inputs: {"input": "+86 16212345678"},
    expect: ["无法确定（162 为移动通信转售号段，实际签约服务商可能是虚拟运营商） 底层网络： 电信（底层网络）"],
    ref: "IT-N417 复核重做：162 是工信部划给移动通信转售业务的号段，号段分配方只说明底层承载网络，用户实际签约服务商为虚拟运营商，静态号段无法确定。旧页面把 162 归入「电信」并直接输出「运营商：电信」。现从运营商映射移除、单独输出「无法确定 + 转售号段」与「底层网络」。默认输入 13800138000 不命中。",
  },
  {
    slug: "it/msisdn-lookup",
    inputs: {"input": "+86 16712345678"},
    expect: ["无法确定（167 为移动通信转售号段，实际签约服务商可能是虚拟运营商） 底层网络： 联通（底层网络）"],
    ref: "IT-N417 复核重做：167 同为转售号段，旧页面归入「联通」。现按同样口径处理且底层网络正确标为联通。与 162 用例共同覆盖两个底层网络。默认输入 13800138000 不命中。",
  },
  {
    slug: "it/msisdn-lookup",
    inputs: {"input": "+86 13900139000"},
    expect: ["运营商： 移动（号段 139，携号转网后可能变化）"],
    ref: "IT-N417 复核重做（对照组）：普通号段 139 仍应给出运营商并保持携号转网提示，证明移除 162/167 未破坏常规号段映射。刻意使用非默认号段 139（页面默认输入是 13800138000，若用默认号段会在判别器的 pure default snapshot 上命中 ⇒ 逃生项）。",
  },
  // ===== 复核失败·第一批重做（IT-N409 / N411 / N370 / N392 / N398 / N400 / N385 / N386）=====
  {
    slug: "it/uuid-generator",
    inputs: {},
    clicks: ["var ts=[' 6ba7b810-9dad-11d1-80b4-00c04fd430c8 ','6ba7b810----9dad11d180b400c04fd430c8','6ba7b8109dad11d180b400c04fd430c8','{6ba7b810-9dad-11d1-80b4-00c04fd430c8}','6ba7b810-9dad-11d1-80b4-00c04fd430c8'];var rs=[];for(var i=0;i<ts.length;i++)rs.push(isValidUuid(ts[i])?'Y':'N');document.getElementById('__tbProbe').textContent='UU='+rs.join('')+' NORM='+normalizeUuid(ts[0]);"],
    expect: ["UU=YNYYY NORM=6ba7b810-9dad-11d1-80b4-00c04fd430c8"],
    ref: "IT-N409 复核重做：isValidUuid 改为只接受 8-4-4-4-12 或 32 位连续十六进制（含首尾空格与花括号包裹）。五种书写依次 合法/错位连字符非法/连续 hex 合法/花括号合法/标准合法；NORM 证明带空格输入被规范化成同一标准串，生成时不再取未 trim 原值。探针只在注入 clicks 后出现，默认态零命中。",
  },
  {
    slug: "it/uuid-generator",
    inputs: {"version": "v5", "namespace": "6ba7b810----9dad11d180b400c04fd430c8", "name": "example.com", "count": "1"},
    expect: ["命名空间 UUID 格式非法：请填写 8-4-4-4-12 的十六进制 UUID（或 32 位连续十六进制）"],
    ref: "IT-N409 复核重做：错位连字符串旧实现去掉所有 - 后恰有 32 位 hex 而被接受，与错误提示宣称的 8-4-4-4-12 格式不符。现入口严格拒绝并给出明确提示；默认 v4 态不出现该提示。",
  },
  {
    slug: "it/uuid-generator",
    inputs: {"version": "v5", "namespace": " 6ba7b810-9dad-11d1-80b4-00c04fd430c8 ", "name": "www.example.com", "count": "1"},
    expect: ["2ed6657d-e927-568b-95e1-2665a8aea6a2"],
    ref: "IT-N409 复核重做：首尾带空格的合法 DNS 命名空间，旧实现入口 trim 通过但生成时读未 trim 原值 ⇒ generateUuidV5 抛 Invalid namespace UUID 且异步异常未捕获。现校验与 SHA-1 共用规范化结果，并用 try/catch 兜住异步异常；产物命中 RFC 4122 / Python uuid5(NAMESPACE_DNS, \"www.example.com\") 标准向量 2ed6657d-e927-568b-95e1-2665a8aea6a2。默认 v4 随机值不命中。",
  },
  {
    slug: "it/matrix-inverter",
    inputs: {},
    clicks: ["var A=[[1e13,1e13],[1e13,2e13]],r=inverse(A),I=r.inv,P=[];for(var i=0;i<2;i++)for(var j=0;j<2;j++){var s=0;for(var k=0;k<2;k++)s+=A[i][k]*I[k][j];P.push(Math.round(s*1e6)/1e6);}document.getElementById('__tbProbe').textContent='MI='+P.join(',')+' INV='+I.map(function(x){return x.map(function(y){return y.toExponential(1);}).join(',');}).join('|');"],
    expect: ["MI=1,0,0,1 INV=2.0e-13,-1.0e-13|-1.0e-13,1.0e-13"],
    ref: "IT-N370 复核重做：A=[[1e13,1e13],[1e13,2e13]] 的尺度 tol≈20，旧实现把该相对主元阈值也用于「归一化之后」的消元因子 f≈1 ⇒ 跳过消元、输出 [[1e-13,0],[-1e-13,1e-13]]，A×A⁻¹=[[0,1],[-1,2]]。现只有 f===0 才跳过，逆矩阵与乘积单位阵自洽。默认单位阵不产生该串。",
  },
  {
    slug: "it/toml-to-xml",
    inputs: {"source": "\"a　b\" = 1"},
    expect: ["&lt;a_b&gt;1&lt;/a_b&gt;"],
    ref: "IT-N392 复核重做：合法 TOML 键 \"a　b\"（U+3000 全角空格）。旧 xmlName 放行整个 \\u00c0-\\uffff ⇒ 输出 <a　b> 被 XML 解析器拒绝；现按 XML 1.0 NameStartChar/NameChar 逐码点清洗 ⇒ <a_b>。expect 是结果区 escH 实体形态，输入 TOML 原文不含尖括号 ⇒ 非回显；默认 config 样例不命中。",
  },
  {
    slug: "it/toml-to-xml",
    inputs: {"source": "\"́x\" = 1"},
    expect: ["&lt;_x&gt;1&lt;/_x&gt;"],
    ref: "IT-N392 复核重做：键首字符为 U+0301 组合音标（属 NameChar 但不是 NameStartChar）。旧实现原样放到标签首字符导致 XML 解析失败；现首字符非法补 _ 且不可见组合标记一律替换 ⇒ <_x>。同时回归锁住「数字开头须保留原字符」：既有用例 \"123\" 仍输出 <_123>，本批修掉的正是首字符被吞成 _23 的回归。默认态不命中。",
  },
  {
    slug: "it/json-schema-validator",
    inputs: {"schema": "{\"required\":[\"x\"],\"items\":{\"type\":\"number\"}}", "data": "[\"bad\"]"},
    clicks: ["var sc=JSON.parse(document.getElementById('schema').value),da=JSON.parse(document.getElementById('data').value),o=[];walk(sc,da,'root',o,0);document.getElementById('__tbProbe').textContent='JSV='+(o.length?'FAIL:'+o.join('|'):'PASS')+' N='+Object.keys(sc).join(',');"],
    expect: ["JSV=FAIL:类型不匹配 root[0]: 期望 number N=required,items"],
    ref: "IT-N398 复核重做：schema 同时含 required 与 items、实例是数组 [\"bad\"]。旧实现因 hasObjKw 把角色猜成对象，items 不生效 ⇒ 判通过。现关键字按实例类型应用：required 只对对象生效、items 只对数组生效 ⇒ 指出元素 0 类型错误。探针由 clicks 写入，默认态（默认 schema/data 校验通过）不产生该串。",
  },
  {
    slug: "it/json-schema-validator",
    inputs: {"schema": "{\"type\":[\"object\",\"array\"],\"items\":{\"type\":\"number\"}}", "data": "[1]"},
    clicks: ["var sc=JSON.parse(document.getElementById('schema').value),da=JSON.parse(document.getElementById('data').value),o=[];walk(sc,da,'root',o,0);document.getElementById('__tbProbe').textContent='JSV='+(o.length?'FAIL:'+o.join('|'):'PASS')+' N='+Object.keys(sc).join(',');"],
    expect: ["JSV=PASS N=type,items"],
    ref: "IT-N400 复核重做：联合类型 [\"object\",\"array\"] + items，实例 [1] 合法。旧实现因 explicitObj 在数组值上误报「不是对象」；现 typeOK 只校验类型集合，关键字按实例类型应用 ⇒ 无错误输出。默认态探针不存在。",
  },
  {
    slug: "it/json-schema-validator",
    inputs: {"schema": "{\"type\":[\"array\",\"string\"]}", "data": "\"hello\""},
    clicks: ["var sc=JSON.parse(document.getElementById('schema').value),da=JSON.parse(document.getElementById('data').value),o=[];walk(sc,da,'root',o,0);document.getElementById('__tbProbe').textContent='JSV='+(o.length?'FAIL:'+o.join('|'):'PASS')+' N='+Object.keys(sc).join(',');"],
    expect: ["JSV=PASS N=type"],
    ref: "IT-N400 复核重做：联合类型 [\"array\",\"string\"] 配字符串 \"hello\"。旧实现要求同时满足 object/array 约束而误报「不是数组」；现按允许类型集合判断 ⇒ 通过。与 N398 用例共同覆盖对象/数组/标量三类实例。默认态探针不存在。",
  },
  {
    slug: "it/invite-code-generator",
    inputs: {},
    clicks: ["var rs=['AB7','KB7','AK9','KA9','AB8'].map(function(c){return verifyLuhn(c)?'Y':'N';});document.getElementById('__tbProbe').textContent='IC='+rs.join('');"],
    expect: ["IC=YYYYN"],
    ref: "IT-N411 复核重做：实测 AB7→KB7 单字符替换、AK9→KA9 相邻换位均通过校验，AB8 改错校验位被拒。1 位数字校验位仅 10 种取值而字符集有 36 个符号（鸽巢原理），不可能保证全检出；本批保留兼容既有已发码的 Luhn 变体，改为如实标注边界：页面说明、公式注释与英文映射均改为「拦截部分错填 / 无法保证全部检出（附两个反例）」，不再冒称「可检出单字符错填与相邻换位」。该用例把漏检反例固化为回归护栏。",
  },
  {
    slug: "it/toml-to-json",
    inputs: {"source": "p = \"\"\"C:\\\\temp\"\"\""},
    expect: ["JSON 输出 { \"p\": \"C:\\\\temp\" }"],
    ref: "IT-N385 复核重做：TOML 多行基本串 \"\"\"C:\\\\temp\"\"\" 应解析为 C:\\temp（单个反斜杠）。旧实现链式 replace 先解 \\t 再解 \\\\，第二个反斜杠吃掉 t ⇒ 反斜杠后跟 TAB；现改单遍 tUnescape。expect 是 JSON.stringify 的双反斜杠转义形态，输入原文是 TOML 三引号 ⇒ 非回显；默认样例不命中。",
  },
  {
    slug: "it/toml-to-json",
    inputs: {"source": "m = \"\"\"a ''' b\"\"\"\nx = 1"},
    expect: ["JSON 输出 { \"m\": \"a ''' b\", \"x\": 1 }"],
    ref: "IT-N386 复核重做：合法混合引号 m = \"\"\"a ''' b\"\"\" 后另起一行 x = 1。旧 tOpenTriple 分别数 \"\"\" 与 ''' 的奇偶，双引号串里的三个单引号被误当成另一种多行串开头 ⇒ 继续吞并下一行、x 丢失；现按当前打开的三引号定界符类型判断闭合，两字段都保留。默认样例不命中。",
  },
  {
    slug: "it/toml-to-json",
    inputs: {"source": "v = \"C:\\\\temp\"\ns = \"a\\\\tb\""},
    expect: ["JSON 输出 { \"v\": \"C:\\\\temp\", \"s\": \"a\\\\tb\" }"],
    ref: "IT-N385 复核重做：单行基本字符串同样走单遍解码。C:\\\\temp 保留反斜杠不被 \\t 污染，a\\\\tb 解为 a + TAB + b 并在 JSON 输出里转义为 \\t。与多行串用例共同覆盖两条解码路径；默认样例不命中。",
  },
  // ===== 条码族 deepdive 示例一致性（自查续批：修正同模板错误文案）=====
  {
    slug: "it/barcode-code128",
    inputs: {},
    clicks: ["var calls=[];window.ToolBoxBarcode={encode:function(t,s){calls.push(t+':'+s);return {ok:true,bits:'101',text:s};},renderCanvas:function(){return {width:1};}};document.getElementById('data').value='ABC-1234';try{generate();}catch(e){}document.getElementById('__tbProbe').textContent='C128='+calls.join('|');"],
    expect: ["C128=code128:ABC-1234"],
    ref: "条码族 deepdive 示例一致性（自查续批）：Code 128 示例改为任意 ASCII 文本 ABC-1234，页面 generate() 确实把它原文交给编码库（校验符号由编码库自动算，页面不要求用户补位）。外部编码库在门禁里以桩替身捕获调用参数；默认输入 ABC-1234 虽相同，但探针 C128= 只在注入 clicks 后出现 ⇒ 非回显、强判别。",
  },
  {
    slug: "it/barcode-code128",
    // IT-N124：共享码库必须支持 ASCII 0~127 的 A/B 子集切换。
    clicks: ["var L=globalThis.__tbBarcodeLibForVerify,r=L?L.code128('a\\u0001'):null,t=L?L.code128('\\u0001~'):null;document.getElementById('__tbProbe').textContent='C128MIX '+(r&&r.ok?'OK':'BAD')+' '+(r&&r.detail?r.detail.subset:'-')+' '+(t&&t.ok?t.detail.subset:'-');"],
    expect: ["C128MIX OK B/A A/B"],
    ref: "IT-N124：'a\\u0001' 需 B→A（100→101 编码语义），'\\u0001~' 需 A→B。旧库两段互斥判断直接报「仅支持单一子集…」⇒ C128MIX BAD - -；修复后分别得 B/A 与 A/B。探针只在 clicks 注入出现，默认态无该串。",
  },
  {
    slug: "it/barcode-code128",
    // IT-N125：空输入必须原样交给编码库报错，不能被 || ' ' 变成空格条码。
    clicks: ["var cap='NOT_CALLED';globalThis.ToolBoxBarcode={encode:function(t,s){cap=s;return {ok:false,error:'stub'};},renderCanvas:function(){return {};}};document.getElementById('data').value='';generate();document.getElementById('__tbProbe').textContent='C128EMPTY '+JSON.stringify(cap);"],
    expect: ['C128EMPTY ""'],
    ref: "IT-N125：空输入时旧页面 `text || ' '` 把空串换成空格，编码库收到 ' ' ⇒ C128EMPTY \" \"；修复后原样传空串 ⇒ C128EMPTY \"\"，由库统一报「请输入条码内容」。默认态 data 非空，不产生该探针串。",
  },
  {
    slug: "it/barcode-code39",
    inputs: {},
    clicks: ["var a=buildCode39('CODE-39',false),b=buildCode39('CODE-39',true);document.getElementById('__tbProbe').textContent='C39='+a.text+'|'+b.text+'|'+a.bits.length+'|'+b.bits.length;"],
    expect: ["C39=CODE-39|CODE-39P|116|129"],
    ref: "条码族 deepdive 示例一致性（自查续批）：Code 39 示例 CODE-39 确实可编码；标准模式不加校验位，勾选「追加 Mod 43 校验位」后由工具追加校验字符 P、bits 从 116 增至 129，与文案「校验位可选且由工具追加」一致。旧示例 9 位数字配「请按规范长度与校验位填写」与页面行为不符。默认态不产生该串。",
  },
  {
    slug: "it/barcode-itf",
    inputs: {},
    clicks: ["var a=buildITF('12345678901234'),b=buildITF('123456789');document.getElementById('__tbProbe').textContent='ITF='+a.length+'|'+b.length;"],
    expect: ["ITF=133|97"],
    ref: "条码族 deepdive 示例一致性（自查续批）：ITF 示例改为 14 位 ITF-14；9 位奇数输入会被自动在前面补 0 凑偶数位，bits 长度 97 与 14 位的 133 不同，证明文案所述「只保留数字、奇数位自动补 0、两两交织」与实现一致。页面不代算 GTIN-14 校验位，文案已如实说明。默认态不产生该串。",
  },
  {
    slug: "it/barcode-msi",
    inputs: {},
    clicks: ["var a=buildMSI('1234567','none'),b=buildMSI('1234567','mod10');document.getElementById('__tbProbe').textContent='MSI='+a.text+'|'+b.text+'|'+a.bits.length+'|'+b.bits.length;"],
    expect: ["MSI=1234567|12345674|91|103"],
    ref: "条码族 deepdive 示例一致性（自查续批）：MSI 示例 1234567 可编码；无校验模式原样输出，Mod 10 模式由工具追加校验位 4（bits 91→103），与文案「MSI 本身无校验、按所选模式由工具追加」一致。默认态不产生该串。",
  },
  {
    slug: "it/barcode-upc",
    inputs: {},
    clicks: ["var a=buildUPC('03600029145'),b=buildUPC('036000291451');document.getElementById('__tbProbe').textContent='UPC='+(a.error||'OK')+'|'+(b.error||'OK')+'|'+(a.bits?a.bits.length:0)+'|'+(b.expect===undefined?'NA':b.expect);"],
    expect: ["UPC=OK|check|95|2"],
    ref: "条码族 deepdive 示例一致性（自查续批）：UPC-A 示例 03600029145 是 11 位，工具自动补校验位后生成 95 模块条码；12 位且末位错误时返回 check 并提示正确校验位 2，与文案「11/12 位、自动补位、12 位核对末位」一致。旧示例 9 位数字在该页根本无法生成。默认态不产生该串。",
  },
  {
    slug: "it/barcode-upc",
    // IT-N129：首位数字系统字符必须单独印在左静区。
    clicks: ["var s=String(drawBarcode);document.getElementById('__tbProbe').textContent='UPCQZ '+((s.indexOf('digits.charAt(0)')>=0&&s.indexOf('leftQuiet/2')>=0&&s.indexOf('digits.slice(1,6)')>=0)?'OK':'BAD');"],
    expect: ["UPCQZ OK"],
    ref: "IT-N129：GS1 UPC-A 首位数字印在左静区，其余 5+6 位分置左右数据区。旧 drawBarcode 直接打印 slice(0,6)/slice(6)，无单独首位与左静区宽度 ⇒ UPCQZ BAD；修复后三个锚点齐全 ⇒ UPCQZ OK。默认态无探针串。",
  },
  // ===== 复核失败·第二批剩余 7 条重做（IT-N492/N493、D-N21、IT-N421、N555、N355、N549、N358）=====
  {
    slug: "design/svg-to-png",
    inputs: {},
    clicks: ["var imgs=[],rev=[];globalThis.URL=globalThis.URL||{};URL.createObjectURL=function(){return 'blob:test';};URL.revokeObjectURL=function(u){rev.push(u);};window.Image=function(){var im={};imgs.push(im);return im;};globalThis.Image=window.Image;var ce=document.createElement.bind(document);document.createElement=function(t){return t==='canvas'?{getContext:function(){return {drawImage:function(){}};},toDataURL:function(){return 'PNG_OK';}}:ce(t);};var el=document.getElementById('svgInput');el.value='<svg><rect/></svg>';document.getElementById('width').value='10';document.getElementById('height').value='10';generate();el.value='';el.fire('input');imgs[0].onload();document.getElementById('__tbProbe').textContent='SVG_CLEAR='+(lastDataURL===''&&rev.length===1?'OK':'FAIL');"],
    expect: ["SVG_CLEAR=OK"],
    ref: "转换未完成时清空 SVG：旧回调必须作废且释放对象 URL，不得重新产生可下载结果。"
  },
  {
    slug: "it/yaml-to-xml",
    inputs: { source: "items:\n  - alpha\n  -" },
    expect: ["&lt;root&gt; &lt;items&gt;alpha&lt;/items&gt;&lt;items&gt;&lt;/items&gt; &lt;/root&gt;"],
    ref: "尾部空 YAML 序列项是 null，须保留为空 XML 元素而不抛异常。"
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "items = [\"\"\"a,b#c\"\"\", 'tail']" },
    expect: ["items: - \"a,b#c\" - tail"],
    ref: "TOML 三引号字符串位于数组时，逗号和 # 均为内容，不得丢弃。"
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "items = [ # ] comment\n  '''hello,\n# world]''',\n  'tail' # ] comment\n]" },
    expect: ["items: - \"hello,\\n# world]\" - tail"],
    ref: "多行字面字符串内的换行、# 和 ] 都是内容，字符串外注释里的 ] 不结束数组。"
  },
  {
    slug: "design/svg-to-png",
    inputs: {},
    clicks: ["var __rev=[],__n=0;globalThis.Blob=globalThis.Blob||function(){};globalThis.URL=globalThis.URL||{};URL.createObjectURL=function(){return 'blob:'+(++__n);};URL.revokeObjectURL=function(u){__rev.push(u);};var __imgs=[];window.Image=function(){var im={onload:null,onerror:null,src:''};__imgs.push(im);return im;};globalThis.Image=window.Image;var __ce=document.createElement.bind(document);document.createElement=function(t){if(t==='canvas'){return {width:0,height:0,getContext:function(){return {fillRect:function(){},drawImage:function(){}};},toDataURL:function(){return 'PNG_OK';}};}return __ce(t);};document.getElementById('svgInput').value='<svg><rect/></svg>';document.getElementById('width').value='10';document.getElementById('height').value='10';generate();generate();generate();try{__imgs[0].onload();}catch(e){}try{__imgs[1].onerror();}catch(e){}var __pv=String(document.getElementById('preview').innerHTML);var __stale=(lastDataURL===''&&__pv.indexOf('<img')<0&&__pv.indexOf('SVG 加载失败')<0)?'Y':'N';var __old=__rev.join(',');try{__imgs[2].onload();}catch(e){}var __pv2=String(document.getElementById('preview').innerHTML);var __latest=(lastDataURL==='PNG_OK'&&__pv2.indexOf('<img')>=0)?'Y':'N';document.createElement=__ce;document.getElementById('__tbProbe').textContent='D21REV='+__old+' STALE='+__stale+' LATEST='+__latest+' ALL='+__rev.join(',');"],
    expect: ["D21REV=blob:1,blob:2 STALE=Y LATEST=Y ALL=blob:1,blob:2,blob:3"],
    ref: "D-N21 复核重做：连续三次 generate() 各创建一个 blob URL。旧修复把 token 守卫放在释放之前，过期的 onload/onerror 直接 return ⇒ blob:1、blob:2 永不释放。现两回调都用 try/finally，过期回调照样释放各自 URL 且不改写 lastDataURL/preview；最新的第三次 onload 仍能正常出图并释放 blob:3。URL/Image/canvas 均由桩捕获，默认态不产生该串。"
  },
  {
    slug: "it/locale-lookup",
    inputs: {},
    clicks: ["var ts=['en-u-ca-gregory-x-gregory','en-US-x-1-1','en-US-1901-1901','en-u-ca-u-ca','sl-rozaj-biske-1994','de-DE-1996'];var rs=[];for(var i=0;i<ts.length;i++)rs.push(__lcValid(ts[i])?'Y':'N');document.getElementById('__tbProbe').textContent='LC='+rs.join('');"],
    expect: ["LC=YYNNYY"],
    ref: "IT-N421 复核重做：旧实现对全 parts 扫描判重，把 Unicode 扩展里的 gregory 与私有用途里的同名串、私有段里重复的 1 都误判为 variant/singleton 重复。现按 RFC 5646 段位推进：x 之后停止判重、扩展属性段不算 variant ⇒ 前两例合法；真正的重复 variant（1901）与重复 singleton（u）仍拒绝；多 variant 与 4 位数字 variant 保持合法。默认态不产生该串。"
  },
  {
    slug: "it/unicode-lookup",
    inputs: {},
    clicks: ["var cs=[0x2B739,0x2B73F,0x2B81D,0x2B81F,0x2CEA1,0x2CEAF,0x2EBE0,0x2EBEF,0x3134A,0x3134F,0x2EBF0,0x2EE5D,0x2EE5E,0x31350,0x323AF,0x323B0,0x3FFFF];var rs=[];for(var i=0;i<cs.length;i++)rs.push(String(lookupName(cs[i])).indexOf('CJK UNIFIED IDEOGRAPH-')===0?'Y':'N');document.getElementById('__tbProbe').textContent='UL='+rs.join('');"],
    expect: ["UL=YNYNYNYNYNYYNYYNN"],
    ref: "IT-N555 复核重做：按 Unicode 15.1.0 unicodedata.name() 逐个扫描得到的 10 段已分配区间替换 block 边界。五个 block 尾码位 2B73F/2B81F/2CEAF/2EBEF/3134F 及 2EE5E/323B0/3FFFF 未分配不得伪造名称；同时补回此前遗漏的 Ext I（2EBF0–2EE5D）与 Ext H（31350–323AF）首尾已分配码位。默认态不产生该串。"
  },
  {
    slug: "it/yaml-to-xml",
    inputs: { source: "items:\n  -\n    - a\n    - b" },
    expect: ["&lt;root&gt; &lt;items&gt;a&lt;/items&gt;&lt;items&gt;b&lt;/items&gt; &lt;/root&gt;"],
    ref: "IT-N355 复核重做（页面真实输入）：单键嵌套序列 items:[[a,b]] 被 ser() 递归展平成两个并列 <items>。旧判断只看外层数组长度为 1 ⇒ 直接输出两个根；现按递归展开后的顶层元素数包一层 <root>。expect 是结果区 escH 转义后的实体形态且含 &lt;root&gt;，输入 YAML 不含尖括号 ⇒ 非回显；默认 note 样例不命中。",
  },
  {
    slug: "it/yaml-to-xml",
    inputs: { source: "items:\n  -\n    - a\n    - b\n  -\n    - c" },
    expect: ["&lt;root&gt; &lt;items&gt;a&lt;/items&gt;&lt;items&gt;b&lt;/items&gt;&lt;items&gt;c&lt;/items&gt; &lt;/root&gt;"],
    ref: "IT-N355 复核重做：多层/多元素嵌套数组共展开 3 个 <items>，countTop 递归求和为 3 ⇒ 仍只有一个 <root>。与单键单元素、单键标量用例共同覆盖空/嵌套/多层数组的唯一根约束。默认态不命中。",
  },
  {
    slug: "it/yaml-to-xml",
    inputs: { source: "items:\n  - only" },
    expect: ["&lt;items&gt;only&lt;/items&gt;"],
    ref: "IT-N355 复核重做：递归展开后恰好 1 个顶层元素时，必须保持原有「该元素即唯一根」的形态，不能被新逻辑强制再包一层 root。默认样例为 note/to/from，不命中。",
  },
  {
    slug: "it/yaml-to-xml",
    inputs: { source: "a: 1\nb: 2" },
    expect: ["&lt;root&gt; &lt;a&gt;1&lt;/a&gt; &lt;b&gt;2&lt;/b&gt; &lt;/root&gt;"],
    ref: "IT-N355 复核重做：多键映射仍按原约定包 <root>，缩进/换行形态未回归。默认态不含 a/b 键。",
  },
  {
    slug: "it/yaml-to-xml",
    inputs: { source: "items: []" },
    expect: ["&lt;items&gt;[]&lt;/items&gt;"],
    ref: "IT-N355 复核重做：空态近似回归。页面简易 YAML 解析器把 [] 当标量，输出单根 <items>[]</items>；源码层 countTop([[]])=0 的空嵌套分支输出单个空 <root>，保证零元素时也只有一个根元素。默认态不命中。",
  },
  {
    slug: "it/team-name-generator",
    inputs: {},
    clicks: ["document.getElementById('seed').value='x';document.getElementById('style').value='classical';document.getElementById('domain').value='creative';document.getElementById('maxLen').value='6';document.getElementById('suffixMode').value='word';document.getElementById('count').value='30';generate();var __o=String(document.getElementById('output').innerHTML);var __names=__o.split('</div>').map(function(s){return s.replace(/<[^>]*>/g,'');}).filter(function(s){return s.length;});var __ok=__names.length===30&&__names.every(function(s){return s.length<=6;});var __long=__names.filter(function(s){return /Collective|Studio/.test(s);}).length;var __word=__names.filter(function(s){return / (Team|Crew)$/.test(s);}).length;document.getElementById('__tbProbe').textContent='TN='+(__ok?'Y':'N')+' LONG='+__long+' WORD='+(__word>0?'Y':'N');"],
    expect: ["TN=Y LONG=0 WORD=Y"],
    ref: "IT-N549 复核重做：种子 x、创意词库、古风、maxLen=6、词库后缀、30 条。旧实现 Math.max(1,maxLen-suffix.length) 让 ' Collective'/' Studio' 突破上限（出现 G Collective / I Studio）。现先筛出「后缀+至少 1 字符 base」放得下的候选，仍用一次 pick 保留可用短后缀（Team/Crew），超长后缀一律不出现，30 条全部 ≤6。默认态（无种子、maxLen=24）不产生该串。"
  },
  {
    slug: "it/team-name-generator",
    inputs: {},
    clicks: ["var modes=['word','number','symbol'],rs=[];for(var m=0;m<modes.length;m++){document.getElementById('seed').value='x'+m;document.getElementById('domain').value='creative';document.getElementById('style').value='classical';document.getElementById('maxLen').value='6';document.getElementById('suffixMode').value=modes[m];document.getElementById('count').value='30';generate();var ns=String(document.getElementById('output').innerHTML).split('</div>').map(function(s){return s.replace(/<[^>]*>/g,'');}).filter(function(s){return s.length;});rs.push(ns.length===30&&ns.every(function(s){return s.length>0&&s.length<=6;})?'Y':'N');}document.getElementById('__tbProbe').textContent='TNMODE='+rs.join('');"],
    expect: ["TNMODE=YYY"],
    ref: "IT-N549 复核重做：词库、数字、符号三类后缀在短 maxLen=6 下都必须不超限且非空。数字/符号后缀长度固定可保留，词库后缀走可用候选筛选；硬夹保险丝保证任何模式都不会出现空名或 >6 字符。默认态不产生该串。"
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "dependencies = [ # ] note\n  'a#b',\n  'tokio',\n]" },
    expect: ["dependencies: - \"a#b\" - tokio"],
    ref: "IT-N358 复核重做（页面真实输入）：多行数组首行注释含 ]，元素为 TOML 字面字符串。旧 stripComment 只认双引号 ⇒ 'a#b' 的 # 被当注释、后续元素被合并成一个错误字符串。现按 TOML 词法区分字面串/基本串/注释，tSplitTop、tDepth、tVal 同步支持字面串 ⇒ 两元素完整保留。expect 是 YAML 冒号形态，输入为等号形态且元素带单引号 ⇒ 非回显；默认样例不命中。",
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "note = \"a\\\\\" # ] comment" },
    expect: ["note: \"a\\\\\""],
    ref: "IT-N358 复核重做：基本字符串末尾是成对转义反斜杠后接注释。旧实现只看引号前一个字符是否为 \\\\，把真正闭合的引号误判为转义引号、注释被吞进值里。现状态机成对吞掉转义序列 ⇒ 值 a+反斜杠，输出侧按 YAML 规则转义为双反斜杠。expect 依赖该精确形态，默认样例不命中。",
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "items = [ # ] ] note\n \"x\", \"y\"\n]" },
    expect: ["items: - x - y"],
    ref: "IT-N358 复核重做：注释里连续两个 ] 都不能被 tDepth 当成数组结束。剥注释后的括号深度仍为 1 ⇒ 继续吞并后续两行，得到两个元素。默认样例不命中。",
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "v = \"a#b\" # c" },
    expect: ["v: \"a#b\""],
    ref: "IT-N358 复核重做：双引号基本字符串内的 # 是数据，串外 # c 才是注释；输出侧对含 # 的字符串加引号保证 YAML 回读一致。默认样例不命中。",
  },
  {
    slug: "it/toml-to-yaml",
    inputs: { source: "x = ['a,b','c,d']" },
    expect: ["x: - \"a,b\" - \"c,d\""],
    ref: "IT-N358 复核重做：字面字符串内的逗号不能被 tSplitTop 当成顶层分隔符，两个元素各自保留逗号。默认样例不命中。",
  },
  {
    slug: "it/barcode-codabar",
    inputs: {},
    clicks: ["var ok=buildCodabar('A12345678B'),bad=buildCodabar('123456789');document.getElementById('__tbProbe').textContent='DD='+(ok.bits&&ok.bits.length===80?'Y':'N')+' OLD='+(bad.error&&bad.error.indexOf('起止符')>=0?'Y':'N');"],
    expect: ["DD=Y OLD=Y"],
    ref: "IT-N492/N493 复核重做：深度解析示例改为带起止符的 A12345678B（10 个字符 × 8 单元 = 80），确实可被 buildCodabar 生成；旧示例纯数字 123456789 缺起止符，实际会被首字符校验拒绝，故文案不能再把它当可用输入。标准 Codabar 不含校验位，构建源 content_deepdive.json、英文映射 i18n/tools/en/it/barcode-codabar.json 与页面 dd-ex-body 三处已同步改为「无需额外补校验位」口径。默认态不产生该串。"
  },
  // ===== 复核失败·第三批重做（IT-N477 / IT-N478 / IT-N3 / IT-N413）=====
  {
    slug: "it/text-replace", inputs: {},
    clicks: ["document.getElementById('__tbProbe').textContent='TOTAL='+__trFind('a'.repeat(200002),'a',{re:false,g:true,i:false,m:false}).length;"],
    expect: ["TOTAL=200002"],
    ref: "IT-N3 再复核：超过 20 万匹配时统计仍须与主替换计数一致。"
  },
  {
    slug: "it/phone-parser", inputs: { phone: "07946095", cc: "44" },
    expect: ["国内格式：0794 6095"],
    ref: "IT-N413 再复核：剥除 trunk 后不足 8 位的英国短号，国内格式仍应保留单个前导 0。"
  },
  {
    slug: "it/vector-magnitude",
    inputs: {},
    clicks: ["document.getElementById('dim').value='2';document.getElementById('v0').value='1e-13';document.getElementById('v1').value='0';calculate();"],
    expect: ["|v| = 1.000e-13", "方向角 θ = atan2(y, x) = 0°"],
    ref: "IT-N477 复核重做：二维 (1e-13, 0) 是非零向量。旧实现用 m>1e-12 判零且 fmt() 把微小数显示成 0，于是输出 v=(0,0)、|v|=0 并称无单位向量/方向角。现按最大分量缩放求稳健范数，真实 0 才显示 0，微小非零用科学计数法 ⇒ |v|=1.000e-13、单位向量 (1,0)、方向角 0°。两条 expect 都只在二维微小非零输入出现，默认态 (3,4,0) 三维不命中。"
  },
  {
    slug: "it/vector-magnitude",
    inputs: {},
    clicks: ["document.getElementById('dim').value='3';document.getElementById('v0').value='1e-200';document.getElementById('v1').value='0';document.getElementById('v2').value='0';calculate();"],
    expect: ["|v| = 1.000e-200", "方向余弦：cos α = 1, cos β = 0, cos γ = 0"],
    ref: "IT-N477 复核重做：三维下溢边界。分量平方 1e-400 已超出 Number 范围，旧 x*x 平方和为 0 ⇒ 误判零向量。缩放范数与指数分解的平方和展示同时生效，方向余弦仍为 (1,0,0)、方向角 0/90/90；默认态三维 (3,4,0) 的余弦为 0.6/0.8/0 ⇒ 不命中。"
  },
  {
    slug: "it/vector-magnitude",
    inputs: {},
    clicks: ["document.getElementById('dim').value='2';document.getElementById('v0').value='1e999';document.getElementById('v1').value='0';calculate();"],
    expect: ["⚠ 向量分量必须为有限数值。"],
    ref: "IT-N477 复核重做：1e999 经 parseFloat 得 Infinity，属非有限分量，必须阻断结论而不是输出 ∞ 或伪方向角。默认态有限输入不出现该提示。"
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "constructor constructor" },
    clicks: ["extractKeywords();"],
    expect: ["1 constructor 2 100.0%"],
    ref: "IT-N478 复核重做：词是任意用户字符串，普通对象词频表让 freq.constructor 读到 Object.prototype 的构造函数，拼接出 `function Object() { [native code] }11` 且相对频率 0.0%。改用无原型字典后应得 2 次、100.0%；默认中文样例词表不含 constructor ⇒ 强判别。"
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "constructor constructor toString valueOf" },
    clicks: ["extractKeywords();"],
    expect: ["1 constructor 2 100.0% 2 tostring 1 50.0% 3 valueof 1 50.0%"],
    ref: "IT-N478 复核重做：覆盖原型属性词的排序分支。toString / valueOf 同样不得继承原型值，按词频 2/1/1 与 100.0%/50.0%/50.0% 排序输出；sortFreq 改用 Object.prototype.hasOwnProperty.call 兼容无原型字典。默认样例不命中。"
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ hello WORLD hello", findInput: "hello", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;document.getElementById('optMultiline').checked=false;var __cap=[];globalThis.TBKit={util:{isEn:function(){return false;},exportCsv:function(n,rows){__cap.push('CSV='+rows.slice(6).map(function(r){return r.join('|');}).join(','));}},chart:{bar:function(){}},history:{record:function(r){__cap.push('EXTRAS='+r.matches);},mount:function(){}}};__trExtras();__trExport();document.getElementById('resultText').value=__cap.join(' ');try{delete globalThis.TBKit;}catch(e){}"],
    expect: ["EXTRAS=2 CSV=1|2|hello,2|14|hello"],
    ref: "IT-N3 复核重做：附加统计与 CSV 导出共用 __trFind。旧实现先 toLowerCase() 再按小写串索引去原文 substr（İ 小写会扩为两个码元），导出位置 3/15 与文本 `ello `；现统一在原文上用转义正则匹配 ⇒ 位置 2/14、文本两处 hello，统计计数 2。EXTRAS/CSV 由 TBKit 桩捕获，只在注入态产生。"
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "aaaa", findInput: "aa", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;document.getElementById('optMultiline').checked=false;var __cap=[];globalThis.TBKit={util:{isEn:function(){return false;},exportCsv:function(n,rows){__cap.push('CSV='+rows.slice(6).map(function(r){return r.join('|');}).join(','));}},chart:{bar:function(){}},history:{record:function(r){__cap.push('EXTRAS='+r.matches);},mount:function(){}}};__trExtras();__trExport();document.getElementById('resultText').value=__cap.join(' ');try{delete globalThis.TBKit;}catch(e){}"],
    expect: ["EXTRAS=2 CSV=1|0|aa,2|2|aa"],
    ref: "IT-N3 复核重做：字面全局查找必须非重叠。旧 __trFind 用 st=idx+1 把 aaaa 查 aa 数成 3 次、覆盖率 150%、CSV 位置 0/1/2；现与主替换 findMatches 一致用正则 lastIndex 自然前进 ⇒ 2 次、位置 0/2。"
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "foo foo", findInput: "foo", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=true;document.getElementById('optGlobal').checked=false;document.getElementById('optMultiline').checked=false;var __cap=[];globalThis.TBKit={util:{isEn:function(){return false;},exportCsv:function(n,rows){__cap.push('CSV='+rows.slice(6).map(function(r){return r.join('|');}).join(','));}},chart:{bar:function(){}},history:{record:function(r){__cap.push('EXTRAS='+r.matches);},mount:function(){}}};__trExport();previewMatch();var __ctx=String(document.getElementById('contextArea').innerHTML);__cap.push('CTX='+(__ctx.indexOf('#1 [0]')>=0&&__ctx.indexOf('#2 [4]')<0?'ONE':'MULTI'));document.getElementById('resultText').value=__cap.join(' ');try{delete globalThis.TBKit;}catch(e){}"],
    expect: ["CSV=1|0|foo EXTRAS=1 CTX=ONE"],
    ref: "IT-N3 复核重做：正则模式关闭全局时，统计/预览/上下文列表/CSV/替换必须只取首个匹配。旧预览恒用 global 扫描 ⇒ 高亮两处并列出 0/4，与 count=1 矛盾。现 findMatches 与 __trFind 均在非全局时 break，CSV 仅 1 行、上下文仅 #1 [0]。"
  },
  {
    slug: "it/phone-parser",
    inputs: { phone: "079460958", cc: "44" },
    clicks: ["calcTool();document.getElementById('__tbCopyProbe').textContent='COPY='+(typeof __lastE164!=='undefined'&&__lastE164===''?'BLOCKED':'OPEN');"],
    expect: ["⚠️ 英国 07 手机国内号码应为 10 位（含 trunk 0 共 11 位），当前 8 位", "COPY=BLOCKED", "国内格式：07946 0958"],
    ref: "IT-N413 复核重做：短英国 07 号 079460958 剥 trunk 0 后仅 8 位。旧实现只在剥 0 后仍满足通用 9–10 位时才剥，导致首位 0 保留、按 9 位固话通过、绕过 digits.charAt(0)==='7' 的手机专属校验，显示 00794 60958 且可复制 +44079460958。现先归一化剥 0 再按 07 手机恰 10 位校验，报错且 __lastE164 保持空 ⇒ 禁止复制；国内格式保留单个 trunk 0（与 9/10 位分支口径一致）。COPY 探针写入独立容器，默认态不存在。"
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "__proto__ constructor __proto__ constructor prototype" },
    clicks: ["extractKeywords();"],
    expect: ["1 constructor 2 100.0% 2 proto 2 100.0% 3 prototype 1 50.0%"],
    ref: "IT-N478 复核重做：__proto__ 是最易触发原型 setter 的键。无原型字典下按普通词计数，且与 constructor 同为 2 次时按词长降序排（constructor 11 > proto 5），验证 sortFreq 的计数/长度双键排序未被原型属性破坏；默认中文样例不命中。"
  },
  {
    slug: "it/text-replace",
    inputs: { findInput: "aa", replaceInput: "X" },
    clicks: ["document.getElementById('sourceText').value='aa'.repeat(3000);document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;document.getElementById('optMultiline').checked=false;var __cap=[];globalThis.TBKit={util:{isEn:function(){return false;},exportCsv:function(n,rows){__cap.push('CSVROWS='+(rows.length-6));}},chart:{bar:function(){}},history:{record:function(r){__cap.push('EXTRAS='+r.matches);},mount:function(){}}};__trExtras();__trExport();document.getElementById('resultText').value=__cap.join(' ');try{delete globalThis.TBKit;}catch(e){}"],
    expect: ["EXTRAS=3000 CSVROWS=200"],
    ref: "IT-N3 复核重做：__trFind 旧的 2000 条上限会让附加统计的匹配数量/覆盖率与主替换（text.match 全局正则，不封顶）在长文本上不一致。6000 字符查 aa 得 3000 处非重叠匹配 ⇒ EXTRAS=3000；CSV 仍按自身约定只导出前 200 行 ⇒ CSVROWS=200。默认样例不产生该串。"
  },
  // ===== 复核失败·第二批重做（前 6 条：IT-N489 / N474 / N471 / N551 / N527 / N528）=====
  {
    slug: "it/json-path",
    inputs: {},
    clicks: ["var o={a:[1,2,3,4,5]},e={a:[]};var ps=['$.a[99::-1]','$.a[:-99:-1]','$.a[-99::-1]','$.a[4:0:-1]','$.a[0:5:-1]','$.a[::-2]'];var rs=[];for(var i=0;i<ps.length;i++){rs.push(jsonPath(o,ps[i]).join(','));}rs.push(jsonPath(e,'$.a[::-1]').join(','));document.getElementById('__tbProbe').textContent='JP='+rs.join('|');"],
    expect: ["JP=5,4,3,2,1|5,4,3,2,1||5,4,3,2||5,3,1|"],
    ref: "IT-N489 复核重做：负步长切片的越界与省略边界。旧实现正负步长共用夹在 [0,len] 的 norm()，[99::-1] 起点未夹紧导致首项 undefined、[:-99:-1] 丢首项、[-99::-1] 多返一项。现负步长按方向夹在 [-1,len-1]：99→4、-99→-1、省略 start→len-1、省略 end→-1。七组结果（含空数组与 -2 步长）一次断言，默认 path 不产生该串。"
  },
  {
    slug: "it/math-evaluator",
    inputs: {},
    clicks: ["var es=['7%pi','7 % pi','7%sin(1)','7%e','7%.5','15%','.5%','50%*120','7%3'];var ws=['0.7168146928','0.7168146928','0.2682321215','1.5634363431','0','0.15','0.005','60','1'];var rs=[];for(var i=0;i<es.length;i++){document.getElementById('expr').value=es[i];calc();rs.push(String(document.getElementById('result').innerHTML).indexOf('>'+ws[i]+'<')>=0?'OK':'BAD');}document.getElementById('__tbProbe').textContent='ME='+rs.join('');"],
    expect: ["ME=OKOKOKOKOKOKOKOKOK"],
    ref: "IT-N474 复核重做：% 的右操作数识别补齐常量 pi/e、函数名、小数点起始操作数与带空格写法。7%pi=0.7168146928、7%sin(1)=0.2682321215、7%e=1.5634363431、7%.5=0；旧实现把它们改写成 (7/100)pi 一类语法错误。同时守住百分比路径 15%=0.15、.5%=0.005、50%*120=60 与取模 7%3=1。九组结果逐项比对，默认态不产生该串。"
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "1e-7", a1: "0", a2: "0", b0: "0", b1: "1e-7", b2: "0" },
    clicks: ["calculate();document.getElementById('__tbProbe').textContent='VCP='+String(document.getElementById('output').innerHTML);"],
    expect: ["A = (1.000e-7, 0, 0)", "A × B = (0, 0, 1.000e-14)"],
    ref: "IT-N471 复核重做：小尺度正交向量。旧 fmt() 用绝对阈值 1e-12 且 toLocaleString() 默认仅 3 位小数，把 1e-7 的输入与 1e-14 的叉积都显示成 0，却仍写 sinθ=1 → θ=90°。现真实零才显示 0，<1e-3 一律科学计数法 ⇒ 输入/叉积/模长/角度自洽。默认 (1,2,3)×(4,5,6) 不命中。"
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "1e-7", a1: "0", a2: "0", b0: "-1e-7", b1: "0", b2: "0" },
    clicks: ["calculate();document.getElementById('__tbProbe').textContent='VCP='+String(document.getElementById('output').innerHTML);"],
    expect: ["B = (-1.000e-7, 0, 0)", "θ = 180°"],
    ref: "IT-N471 复核重做：小尺度反向共线。负分量不得被显示成 -0；归一化向量下 sinθ=0、cosθ=-1 ⇒ atan2 给 180° 且平行结论成立。默认算例 12.933° 不命中。"
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "1e-200", a1: "0", a2: "0", b0: "0", b1: "1e-200", b2: "0" },
    clicks: ["calculate();document.getElementById('__tbProbe').textContent='VCP='+String(document.getElementById('output').innerHTML);"],
    expect: ["A × B = (0, 0, 1e-400)", "叉积绝对量级低于双精度可表示范围"],
    ref: "IT-N471 复核重做：极端下溢边界。|A||B|=1e-400 已超出双精度，直接相乘会得 0 并造成「叉积为零但 θ=90°」的矛盾。现归一化向量给出角度，并用指数分解展示 c*|A|*|B| 的量级 1e-400，同时显式说明显示口径；默认算例不命中。"
  },
  {
    slug: "it/text-qr",
    inputs: { text: "old secret" },
    clicks: ["window.__qrCanvas={toDataURL:function(){return 'OLD_PNG';}};window.__qrMeta={probe:1};document.getElementById('text').value='';generate();var __cap=[];var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='a'){e.click=function(){__cap.push('DL:'+e.download);};}return e;};downloadPNG();downloadSVG();document.createElement=__ce;document.getElementById('__tbProbe').textContent='QR='+__cap.join('|')+' CANVAS='+(window.__qrCanvas===null?'NULL':'STALE')+' META='+(window.__qrMeta===null?'NULL':'STALE');"],
    expect: ["QR= CANVAS=NULL META=NULL"],
    ref: "IT-N551 复核重做：先放一张旧 canvas + 旧元数据，清空文本再 generate()，PNG/SVG 都必须无法下载旧图。旧修复只清 __qrMeta、不清 window.__qrCanvas，downloadPNG 仍触发一次旧图下载。现 generate() 开始即把两者作废，downloadPNG 还要求画布与元数据同时有效。下载动作由 createElement('a') 桩捕获，默认态不产生该串。"
  },
  {
    slug: "it/text-qr",
    inputs: { text: "old secret" },
    clicks: ["window.__qrCanvas={toDataURL:function(){return 'OLD_PNG';}};window.__qrMeta={probe:1};document.getElementById('text').value='anything';generate();var __p=document.getElementById('__tbProbe');__p.textContent='ERR='+(window.__qrCanvas===null&&window.__qrMeta===null?'CLEAR':'STALE');drawQR=function(t){var c=document.createElement('canvas');c.__qrMeta={n:1,margin:4,cell:8,dark:[0],fg:'#000000',bg:'#ffffff'};c.toDataURL=function(){return 'NEW_PNG';};return c;};document.getElementById('text').value='NEW-QR';generate();__p.textContent=String(__p.textContent)+' RECOVER='+(window.__qrCanvas&&window.__qrMeta?'OK':'FAIL');var __cap=[];var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='a'){e.click=function(){__cap.push('DL:'+e.download);};}return e;};downloadPNG();document.createElement=__ce;__p.textContent=String(__p.textContent)+' DL='+__cap.join('|');"],
    expect: ["ERR=CLEAR RECOVER=OK DL=DL:qrcode.png"],
    ref: "IT-N551 复核重做：生成异常（harness 下 qrcode 外部脚本不可加载）时也必须同时作废画布与元数据；随后用桩替身恢复合法生成，画布与元数据重建成功，并实际调用 downloadPNG() 捕获一次真实下载 qrcode.png，证明清空逻辑没有误伤正常导出。默认态不产生该串。"
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "```js\n``` not-a-closing-fence\n*not-a-list\n```" },
    clicks: ["calcTool();document.getElementById('__tbProbe').textContent='MD='+String(document.getElementById('result').innerHTML);"],
    expect: ["MD= 检查结果 4 行数 0 问题"],
    ref: "IT-N527 复核重做：闭围栏后只能跟空白。第二行 ``` not-a-closing-fence 是代码内容而非闭围栏，旧实现只比字符与长度就翻转 inFence，导致第 3 行被误报列表缺空格、第 4 行被误报 MD040。现按 CommonMark 严格判定（缩进 ≤3、同字符、长度 ≥、后缀全空白）⇒ 0 问题。默认示例含多个待整改项，不命中。"
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "```js\n    ```\n*not-a-list\n```" },
    clicks: ["calcTool();document.getElementById('__tbProbe').textContent='MD='+String(document.getElementById('result').innerHTML);"],
    expect: ["MD= 检查结果 4 行数 0 问题"],
    ref: "IT-N527 复核重做：缩进 4 空格的围栏状行按 CommonMark 是缩进代码块内容，不得关闭围栏。旧实现 fm 允许任意 \\s* 前导空白，会提前闭围栏并误报后续行。现限制前导空白 ≤3 ⇒ 0 问题；默认示例含多个待整改项，不命中。"
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", port: "80", replicas: "2" },
    clicks: ["var ims=['[nginx]','&foo','*alias','{a}','a//b','nginx:latest:bad'];var rs=[];for(var i=0;i<ims.length;i++){document.getElementById('image').value=ims[i];calcTool();rs.push(String(document.getElementById('result').innerHTML).indexOf('不是合法的容器镜像引用')>=0?'REJECT':'ACCEPT');}document.getElementById('__tbProbe').textContent='K8='+rs.join('|');"],
    expect: ["K8=REJECT|REJECT|REJECT|REJECT|REJECT|REJECT"],
    ref: "IT-N528 复核重做：流式集合 [nginx]、锚点 &foo、别名 *alias、映射 {a}、空路径段 a//b、双 tag nginx:latest:bad 均不符合容器镜像引用语法，必须统一拒绝，而不是枚举 null/true/{} 等少数 YAML 特殊值。原有 #/关键字/空白 三条具体提示保持不变；默认合法镜像不产生该串。"
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "123", port: "80", replicas: "2" },
    clicks: ["calcTool();document.getElementById('__tbProbe').textContent='K8='+String(document.getElementById('result').innerHTML);"],
    expect: ["image: '123'"],
    ref: "IT-N528 复核重做：纯数字镜像名在语法上合法，但裸输出 image: 123 会被 YAML 解析成整数。现所有合法镜像一律以单引号标量输出 ⇒ image: '123' 得到字符串。默认镜像 nginx:latest 不命中。"
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "ghcr.io/team/app:1.2.3", port: "80", replicas: "2" },
    clicks: ["calcTool();document.getElementById('__tbProbe').textContent='K8='+String(document.getElementById('result').innerHTML);"],
    expect: ["image: 'ghcr.io/team/app:1.2.3'"],
    ref: "IT-N528 复核重做：带 registry 主机、多段路径与语义化 tag 的合法镜像必须仍可生成清单，且被引号正确包裹。白名单校验与引号化不得误伤正常镜像；默认 nginx:latest 不命中。"
  },
  {
    slug: "it/json-path",
    inputs: {},
    clicks: ["var o={a:[1,2,3,4,5]};var ps=['$.a[99:]','$.a[:-99]','$.a[-99:3]','$.a[2:99]','$.a[::3]','$.a[4:1:-2]'];var rs=[];for(var i=0;i<ps.length;i++){rs.push(jsonPath(o,ps[i]).join(','));}document.getElementById('__tbProbe').textContent='JP2='+rs.join('|');"],
    expect: ["JP2=||1,2,3|3,4,5|1,4|5,3"],
    ref: "IT-N489 复核重做：正步长同样要按下标方向夹紧。[99:] / [:-99] 均为空，[-99:3] 取 1,2,3、[2:99] 取 3,4,5，[::3] 取 1,4，[4:1:-2] 取 5,3。与负步长用例一起覆盖正负方向、显式/省略、越界起止与步长绝对值 >1；默认 path 不产生该串。"
  },
  {
    slug: "it/math-evaluator",
    inputs: {},
    clicks: ["var es=['7%-pi','7%+sin(1)','7 % -3','7 % +3'];var ws=['0.7168146928','0.2682321215','1','1'];var rs=[];for(var i=0;i<es.length;i++){document.getElementById('expr').value=es[i];calc();rs.push(String(document.getElementById('result').innerHTML).indexOf('>'+ws[i]+'<')>=0?'OK':'BAD');}document.getElementById('__tbProbe').textContent='ME2='+rs.join('');"],
    expect: ["ME2=OKOKOKOK"],
    ref: "IT-N474 复核重做：一元正负号与常量/函数组合的右操作数。7%-pi = 7 % (-pi) = 0.7168146928、7%+sin(1) = 0.2682321215，带空格的 7 % -3 / 7 % +3 均为 1。确认新增的标识符识别没有破坏旧的一元符号分支；默认态不产生该串。"
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "````js\n```\n*not-a-list\n````\n- item" },
    clicks: ["calcTool();document.getElementById('__tbProbe').textContent='MD3='+String(document.getElementById('result').innerHTML);"],
    expect: ["MD3= 检查结果 5 行数 0 问题"],
    ref: "IT-N527 复核重做：闭围栏长度不得短于开围栏。开围栏 4 个反引号，内部 3 个反引号的 ``` 只是代码内容，4 个反引号的 ```` 才闭围栏；随后 '- item' 的列表标记后已有空格 ⇒ 0 问题。与跨类型、同标记带正文、缩进 4 空格三例共同覆盖围栏语法；默认示例含多个待整改项，不命中。"
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "E4B8ADF09F9880" },
    clicks: ["convert()"],
    expect: ["中😀"],
    ref: "IT-N313：E4 B8 AD 为 UTF-8 中，F0 9F 98 80 为 UTF-8 😀，合法序列须完整解码。",
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "80", output: "stale-result" },
    clicks: ["convert();var out=document.getElementById('output');var message=document.getElementById('hexStatus').textContent;out.value='N313_INVALID='+(out.value===''&&message.includes('不是有效的 UTF-8'));"],
    expect: ["N313_INVALID=true"],
    ref: "IT-N313：孤立续字节 80 非法，清除旧结果并提示，不能悄悄替换为 U+FFFD。",
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "A", output: "stale-result" },
    clicks: ["convert();var out=document.getElementById('output');var message=document.getElementById('hexStatus').textContent;out.value='N313_ODD='+(out.value===''&&message.includes('必须为偶数'));"],
    expect: ["N313_ODD=true"],
    ref: "IT-N313：奇数位 Hex 应提示错误并清空旧结果，不能继续显示可复制的陈旧输出。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "aa", findInput: "aa", replaceInput: "X" },
    clicks: ["document.getElementById('sourceText').value='aa'.repeat(600);document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;doReplace();document.getElementById('resultText').value='REPLACED='+document.getElementById('resultText').value.length+' COUNT='+document.getElementById('replaceCount').textContent;"],
    expect: ["REPLACED=600 COUNT=600"],
    ref: "IT-N3：600 个非重叠字面量替换实际执行 600 次，计数不能停在旧的 501 上限。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "ab ac", findInput: "a(.)", replaceInput: "[$1]" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=true;document.getElementById('optGlobal').checked=true;doReplace();"],
    expect: ["[b] [c]"],
    ref: "IT-N3 回归：正则模式仍展开捕获组；字面量模式才保持 $1 原样。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ hello WORLD hello", findInput: "hello", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;doReplace();document.getElementById('resultText').value+=' | count='+document.getElementById('replaceCount').textContent;"],
    expect: ["İ X WORLD X | count=2"],
    ref: "IT-N3：İ 小写会扩为两个码元；必须按原文索引替换两处且计数为 2。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ hello WORLD hello", findInput: "hello", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=false;doReplace();document.getElementById('resultText').value+=' | count='+document.getElementById('replaceCount').textContent;"],
    expect: ["İ X WORLD hello | count=1"],
    ref: "IT-N3：非全局模式只替换首处，并保持前后原文和计数。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ HELLO hello", findInput: "hello", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=true;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;doReplace();document.getElementById('resultText').value+=' | count='+document.getElementById('replaceCount').textContent;"],
    expect: ["İ HELLO X | count=1"],
    ref: "IT-N3：区分大小写只匹配小写 hello，İ 前缀与大写词不受影响。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ a.b aXb a.b", findInput: "a.b", replaceInput: "$&" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;doReplace();document.getElementById('resultText').value+=' | count='+document.getElementById('replaceCount').textContent;"],
    expect: ["İ $& aXb $& | count=2"],
    ref: "IT-N3：字面量模式点号不作为通配符，替换值 $& 不展开。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ aaaa", findInput: "aa", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;doReplace();document.getElementById('resultText').value+=' | count='+document.getElementById('replaceCount').textContent;"],
    expect: ["İ XX | count=2"],
    ref: "IT-N3：紧邻匹配不得重叠计数；结果和次数均为 2。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "İ hello WORLD hello", findInput: "hello", replaceInput: "X" },
    clicks: ["document.getElementById('optCase').checked=false;document.getElementById('optRegex').checked=false;document.getElementById('optGlobal').checked=true;previewMatch();var ctx=document.getElementById('contextArea').innerHTML;document.getElementById('resultText').value='PREVIEW_N3='+(ctx.includes('#1 [2]')&&ctx.includes('#2 [14]'));"],
    expect: ["PREVIEW_N3=true"],
    ref: "IT-N3：两处预览坐标分别为原文 UTF-16 偏移 2 和 14；旧实现小写展开后偏移为 3 和 15。",
  },
  {
    // 原 it/base64 已在「跨分类重复工具治理（批次六）」合并进 base64-converter，
    // 旧 slug 不再存在。用例改指现存工具，避免死用例长期拖挂门禁。
    slug: "it/base64-converter",
    inputs: { input: "hello" },
    expect: ["aGVsbG8="],
    ref: "Base64('hello') = aGVsbG8=（RFC 4648 标准测试向量） ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "it/base64-converter",
    inputs: { input: "hello world" },
    clicks: ["document.getElementById('urlSafe').parentElement.style={};setAlgo('base32');encodeText();"],
    expect: ["NBSWY3DPEB3W64TMMQ======", "+118.2%"],
    ref: "Base32 分支：'hello world' → NBSWY3DPEB3W64TMMQ======（用 '=' 补齐到 8 的倍数，输出 24 字符）；膨胀率 +118.2% = (24-11)/11",
  },
  {
    slug: "it/base64-converter",
    inputs: { input: "hello world" },
    clicks: ["document.getElementById('urlSafe').parentElement.style={};setAlgo('base85');encodeText();"],
    expect: ["+63.6%", "11 B"],
    ref: "Base85 分支：4 字节一组压成 5 字符并用 <~…~> 包裹，'hello world' 得 18 字符；膨胀率 +63.6% = (18-11)/11，输入字节数 11 B",
  },
  {
    slug: "it/base64-converter",
    inputs: { input: "a?b/c+d" },
    clicks: ["encodeText();"],
    expect: ["YT9iL2MrZA", "+42.9%"],
    ref: "勾选 URL-safe（非默认态）：标准码 YT9iL2MrZA== 去尾 '='、+/ 换 -_，得 YT9iL2MrZA（10 字符）；膨胀率 +42.9% = (10-7)/7",
  },
  {
    slug: "it/base64-converter",
    inputs: { input: "aGVsbG8gd29ybGQ=" },
    clicks: ["decodeText();"],
    expect: ["hello world", "-31.3%"],
    ref: "解码方向：aGVsbG8gd29ybGQ= → hello world（11 字节）；膨胀率沿用页面口径 (11-16)/16 = -31.3%",
  },
  {
    slug: "it/base64-converter",
    inputs: { input: "你好，世界" },
    clicks: ["encodeText();"],
    expect: ["5L2g5aW977yM5LiW55WM", "15 B"],
    ref: "多字节 UTF-8：5 个字符占 15 字节（statInSize 15 B，不是 statInLen 5），编码得 20 字符 5L2g5aW977yM5LiW55WM，膨胀率 +33.3%",
  },
  {
    // 原为只覆盖「Base64 标准编码」的弱覆盖页：解码方向、base32/base85 分支、URL-safe、
    // 多字节字节数口径、非法输入保护均无用例，此处一次补齐 6 条，全部锚在派生量上。
    slug: "it/base64-converter",
    inputs: { input: "!!!not-base64!!!", output: "KEEP-THIS-VALUE-0123456789" },
    clicks: ["decodeText();"],
    expect: ["KEEP-THIS-VALUE-0123456789", "+62.5%"],
    ref: "非法 base64 使 atob 抛异常：decodeText 只弹 toast、不改写输出区，预设输出 KEEP-THIS-VALUE-0123456789 原样保留（statOutLen 26，膨胀率 (26-16)/16 = +62.5%）",
  },
  {
    // IT-N502 回归：四套词库均为 14×14 且不含去重脚本残留的数字后缀（奶2/喵2/泡2）
    slug: "it/nickname-generator",
    inputs: {},
    clicks: ["var __bad=[];['cute','cool','poetic','chinese'].forEach(function(k){if(SETS[k].a.length!==14||SETS[k].b.length!==14)__bad.push(k+'=' + SETS[k].a.length + 'x' + SETS[k].b.length);SETS[k].a.concat(SETS[k].b).forEach(function(w){if(/[0-9]/.test(w))__bad.push(k+':'+w);});});document.getElementById('output').textContent='SETS bad='+(__bad.length?__bad.join(','):'none');"],
    dumpIds: ["output"],
    expect: ["SETS bad=none"],
    ref: "IT-N502：公式说明承诺软萌/高冷/诗意/中文四套各 14×14，修复前 SETS.chinese.a 只有 8 项、cute 含「奶2/喵2/泡2」三个数字残留 ⇒ 输出一串 bad 条目；修复后四套均 14×14 且无数字词 ⇒ `SETS bad=none`。全表遍历，默认示例（页面渲染的昵称 div）不含该串。",
  },
  {
    // IT-N504 回归：批量生成后复制文本必须按行分隔（原 textContent 把 N 个 div 连成一串）
    slug: "it/nickname-generator",
    inputs: { count: "3" },
    clicks: ["generate();var __t=__nicknameCopyText();var __sep=String.fromCharCode(10);var __ls=__t.split(__sep);document.getElementById('output').textContent='N504 lines='+__ls.length+' sep='+(__t.indexOf(__sep)!==-1);"],
    dumpIds: ["output"],
    expect: ["N504 lines=3 sep=true"],
    ref: "IT-N504：count=3 生成三条后，__nicknameCopyText() 必须是 3 行且含换行符。修复前 copyResult 取 output.textContent，10 个 div 的 textContent 不带分隔符 ⇒ 1 行、sep=false。行数由注入的 count 决定（默认 10 不会是 3），故有判别力。",
  },
  {
    // IT-N505 回归：同一节点先作为文件、后又出现子路径时，必须改判目录并保留子树
    slug: "it/ascii-tree-generator",
    inputs: { paths: "src\nsrc/index.js" },
    clicks: ["build()"],
    expect: ["src/ └── index.js"],
    ref: "IT-N505：输入 `src` + `src/index.js`，旧实现首次把 src 标成 _file=true，后续子路径虽写入 _children 但 render 对文件节点不递归 ⇒ 输出只有 `src`，index.js 静默消失。修复后统一后处理把含子节点的项改判目录，输出 `src/ └── index.js`（blob 把换行/缩进压成单空格）。默认示例不含该串。",
  },
  {
    // IT-N506 回归：缩进文本必须推断层级（旧实现 trim 掉前导空白再按 / 切分，得到一串扁平根节点）
    slug: "it/ascii-tree-generator",
    inputs: { paths: "root\n  child\n    grand" },
    clicks: ["build()"],
    expect: ["root/ └── child/ └── grand"],
    ref: "IT-N506：三行以 2/4 空格缩进，最小非零缩进 2 为一级 ⇒ root → child → grand 三级嵌套。旧实现先 trim 再 split('/')，三个名字都成根节点，输出扁平三行且无连接符；新实现按缩进栈构建并输出 `root/ └── child/ └── grand`。默认示例为路径列表，不含该串。",
  },
  {
    slug: "it/md5",
    inputs: { textInput: "hello" },
    expect: ["5d41402abc4b2a76b9719d911017c592"],
    ref: "MD5('hello') = 5d41402abc4b2a76b9719d911017c592（RFC 1321 常见向量）",
  },
  {
    slug: "it/md5",
    inputs: { textInput: "a\nb" },
    checkIds: ["lineMode"],
    clicks: ["calcText()"],
    expect: ["0cc175b9c0f1b6a831c399e269772661", "92eb5ffee6ae2fec3ad71c777531578f"],
    ref: "逐行批量分支（勾选 lineMode）：'a' → 0cc175b9c0f1b6a831c399e269772661、'b' → 92eb5ffee6ae2fec3ad71c777531578f（RFC 1321 单字符向量）。默认态未勾选 lineMode，逐行表 display:none，两串均不出现；整段 'a\\nb' 的摘要也不是这两串。",
  },
  {
    slug: "it/sha",
    inputs: { textInput: "hello" },
    checks: ["sha-256"],
    expect: ["2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"],
    ref: "SHA-256('hello') = 2cf24dba…9824（NIST 标准向量）",
  },
  {
    // 原为 all_default 弱用例：textarea 默认内容就是 "123456789"；且 expect 同时列大写/小写 → 无论 upper 如何都命中，零判别力。
    // 改注入 "abc"（独立核对 python zlib.crc32(b"abc") = 0x352441c2）+ 显式声明 upper 选中 → 只断言大写形态。
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    checkIds: ["upper"],
    expect: ["CRC-32 0x352441C2"],
    ref: "python zlib.crc32(b'abc') = 0x352441c2（CRC-32/ISO-HDLC）→ 页面大写渲染 0x352441C2。回退默认（input=123456789 且 upper 未选中）→ 0xcbf43926（小写），不命中。",
  },

  // —— 编码类（期望值由 python base64 / 自实现 base58 独立计算，非凭记忆）——
  {
    slug: "it/base32-encode",
    inputs: { input: "hello" },
    expect: ["NBSWY3DP", "nbswy3dp"],
    ref: "python base64.b32encode(b'hello') = NBSWY3DP（RFC 4648）",
  },
  {
    slug: "it/base32-encode",
    clicks: ["var r=[];['ME=======','ME======','MZXW6YQ','MZXR','A'].forEach(function(x){try{var b=base32ToBytes(x);r.push(x+':OK'+b.length);}catch(e){r.push(x+':ERR');}});document.getElementById('__tbProbe').textContent='B32PAD '+r.join('|');"],
    expect: ["B32PAD ME=======:ERR|ME======:OK1|MZXW6YQ:OK4|MZXR:ERR|A:ERR"],
    ref: "IT-N110：ME=======（7 个填充，合法应 6）必须拒绝；ME====== 解出 1 字节 a；省略填充的 MZXW6YQ 仍解出 3 字节 foo；MZXR 残余位非零、A 长度非法均拒绝。旧实现无填充数校验 ⇒ ME=======:OK1 不命中。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/base32-encode",
    clicks: ["var wrapped=(typeof decode32==='function')&&decode32.toString().indexOf('__base32_encodeExtras')>=0;document.getElementById('input').value='JBSWY3DP';document.getElementById('output').value='SENTINEL';decode32();document.getElementById('__tbProbe').textContent='B32H '+(wrapped?'W':'N')+' out='+document.getElementById('output').value;"],
    expect: ["B32H W out=Hello"],
    ref: "IT-N111：decode32 必须像 encode32 一样被历史记录包装（函数体含 __base32_encodeExtras），旧源码只包装 encode32 ⇒ N。哨兵 SENTINEL 被真解码结果 Hello 覆盖，证明执行的仍是真 decode32。历史记录与方向字段由 JSDOM 真机脚本完整验证（harness stub DOM 的 querySelectorAll 无法喂给快照）。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/base32-encode",
    clicks: ["var cb=null,cap=null;globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){},clear:function(){}},preset:{bar:function(sel,items,c){cap={sel:sel,n:items.length,labels:items.map(function(x){return x.label;})};cb=c;}}};__base32_encodePresets();document.getElementById('input').value='中文测试';document.getElementById('output').value='SENTINEL';if(cb)cb();document.getElementById('__tbProbe').textContent='B32PRE '+(cap?cap.sel+' n='+cap.n+' '+cap.labels.join('/'):'NONE')+' cb='+document.getElementById('output').value;"],
    expect: ["B32PRE #base32_encodePresets n=3 Hello World（编码）/中文测试（编码）/JBSWY3DP（解码） cb=4S4K3ZUWQ7TLLC7IV6KQ===="],
    ref: "IT-N112：预设页签必须有 3 条可用预设且回调真能跑（中文测试经 UTF-8 Base32 = 4S4K3ZUWQ7TLLC7IV6KQ====，node 独立复算）。旧实现 preset.bar 从不调用 ⇒ NONE、哨兵不被覆盖。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/base58-encode",
    inputs: { input: "hello" },
    expect: ["Cn8eVZg"],
    ref: "自实现 Base58（BTC 字母表）编码 'hello' = Cn8eVZg",
  },
  {
    slug: "it/base58-encode",
    clicks: ["var wrapped=(typeof dec==='function')&&dec.toString().indexOf('__base58_encodeExtras')>=0;document.getElementById('input').value='9Ajdvzr';document.getElementById('output').value='SENTINEL';dec();document.getElementById('__tbProbe').textContent='B58DEC '+(wrapped?'W':'N')+' out='+document.getElementById('output').value;"],
    expect: ["B58DEC W out=Hello"],
    ref: "IT-N117：dec() 必须像 enc() 一样被历史记录包装（函数体含 __base58_encodeExtras），旧源码只包装 enc ⇒ N。哨兵 SENTINEL 被真解码结果 Hello 覆盖，证明执行的仍是真 dec。方向字段与历史记录由 JSDOM 真机脚本验证。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/base58-encode",
    // IT-N119：非 UTF-8 载荷必须明确报错，不能静默产出 U+FFFD。
    clicks: ["var e=encodeBase58([0x80,0xff]),i=document.getElementById('input'),o=document.getElementById('output'),msg='',oa=alert;i.value=e;o.value='KEEP';alert=function(m){msg=String(m);};try{dec();}catch(x){}alert=oa;document.getElementById('__tbProbe').textContent='B58FAT '+(/非 UTF-8/.test(msg)?'ERR':'NO')+' '+o.value;"],
    expect: ["B58FAT ERR KEEP"],
    ref: "IT-N119：把 [0x80,0xFF] 编成 Base58 再解码。修复后用 fatal:true 的 TextDecoder 拒绝并弹「载荷含非 UTF-8 字节」，输出哨兵 KEEP 不被 U+FFFD 覆盖 ⇒ B58FAT ERR KEEP；旧实现默认非严格解码 ⇒ msg 空且 out=两个 U+FFFD ⇒ B58FAT NO，判别明确。默认态无探针。",
  },
  {
    slug: "it/hex-encode",
    inputs: { input: "hello" },
    expect: ["68656c6c6f", "68656C6C6F"],
    ref: "b'hello'.hex() = 68656c6c6f",
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "68656c6c6f" },
    expect: ["hello"],
    ref: "bytes.fromhex('68656c6c6f') = b'hello'",
  },
  {
    slug: "it/binary-encode",
    inputs: { input: "hi" },
    expect: ["0110100001101001", "01101000 01101001"],
    ref: "''.join(format(c,'08b') for c in b'hi') = 0110100001101001",
  },
  {
    slug: "it/text-to-binary",
    inputs: { input: "hi" },
    expect: ["0110100001101001", "01101000 01101001"],
    ref: "同上，b'hi' 的 8 位二进制表示",
  },
  {
    slug: "it/text-to-hex",
    inputs: { input: "hello" },
    expect: ["68656c6c6f", "68656C6C6F", "68 65 6c 6c 6f", "68 65 6C 6C 6F"],
    ref: "b'hello'.hex() = 68656c6c6f",
  },
  {
    slug: "it/text-to-decimal",
    inputs: { input: "hi" },
    expect: ["104 105", "104,105", "104105"],
    ref: "'hi' 的十进制码点为 104 105",
  },
  {
    slug: "it/text-to-octal",
    inputs: { input: "hi" },
    expect: ["150 151", "150,151"],
    ref: "format(104,'o')=150、format(105,'o')=151",
  },
  {
    slug: "it/decimal-encode",
    inputs: { input: "hi" },
    expect: ["104 105", "104,105"],
    ref: "同 text-to-decimal：'hi' → 104 105",
  },
  {
    slug: "it/octal-encode",
    inputs: { input: "hi" },
    clicks: ["enc()"],
    expect: ["150 151", "150,151"],
    ref: "同 text-to-octal：'hi' → 150 151",
  },
  {
    slug: "it/text-to-ascii",
    inputs: { txt: "z" },
    expect: ["122"],
    ref: "ord('z') = 122（ASCII 码表；默认正文 Hello, ToolBox! 不含码点 122，注入失败即不命中）",
  },
  {
    slug: "it/text-to-unicode",
    inputs: { txt: "A" },
    expect: ["U+0041", "0041", "65"],
    ref: "ord('A') = 65 → U+0041",
  },
  {
    slug: "it/url-encode",
    inputs: { input: "a b" },
    expect: ["a%20b", "a+b"],
    ref: "urllib.parse.quote('a b') = a%20b（plusSpace 开启时为 a+b，两者均属正确实现） ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: "<" },
    expect: ["&lt;", "&#60;", "&#x3C;"],
    ref: "HTML 实体：'<' 转义为 &lt;（或数字实体 &#60;）",
  },

  // —— 进制与密码类 ——
  {
    slug: "it/integer-base-converter",
    inputs: { num: "255", fromBase: "10", toBase: "16" },
    expect: ["10 进制 →"],
    ref: "format(255,'X') = FF",
  },
  {
    slug: "it/number-base-converter",
    inputs: { inputValue: "1000", inputBase: "10" },
    expect: ["3E8"],
    ref: "inputValue=1000 按十进制解读 → 十六进制 3E8（formatNumber(1000,16).toUpperCase()）。"
       + "改用 1000 而非 255：页面含 0–255 静态参考表，255 的各进制表示恒在表中（原 expect「FF」撞表，逃生项）；"
       + "1000 超出静态表范围，其转换结果仅在输入框真正注入时出现，回退默认(空)无 3E8 → 失配。",
  },
  {
    slug: "it/number-base-converter",
    // IT-N8 回归：自定义进制输入非整数（如 2.5）不得被 parseInt 当 2 进制悄悄转换，必须提示「进制必须为 2–36 的整数」。
    inputs: { inputValue: "10", inputBase: "custom", customBase: "2.5" },
    expect: ["进制必须为 2–36 的整数"],
    ref: "独立复算：customBase='2.5' ⇒ getInputBase 先 /^\\d+$/ 校验失败 ⇒ 返回 null ⇒ convertFromInput 显示「⚠ 进制必须为 2–36 的整数。」；修复前 parseInt('2.5')=2 被当 base 2 静默转换。默认 preset 路径（inputBase=10）不受影响、不命中。",
  },
  {
    slug: "it/calc-2",
    inputs: { numInput: "254", fromBase: "10" },
    expect: ["FE", "fe"],
    ref: "format(254,'X') = FE。原用例取 255/10，恰等于页面默认值（value=\"255\"、option 10 selected）⇒ 不注入也命中、属「输入等于默认值」型假门禁；改用 254 后默认态输出 255/FF 不再命中。",
  },
  {
    slug: "it/caesar-cipher",
    inputs: { input: "abc", shift: "1" },
    expect: ["bcd"],
    ref: "凯撒位移 1：a→b、b→c、c→d",
  },
  {
    slug: "it/rot-cipher",
    inputs: { input: "hello", shift: "13" },
    expect: ["uryyb"],
    ref: "ROT13('hello') = uryyb（自互逆，经典向量）",
  },
  {
    slug: "it/morse",
    inputs: { input: "SOS" },
    expect: ["... --- ...", "...---..."],
    ref: "摩斯电码 S=...、O=---，SOS = ... --- ...（国际求救信号）",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "1987" },
    expect: ["MCMLXXXVII"],
    ref: "1987 = 1000+900+80+7 = MCMLXXXVII",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { timestampSec: "0" },
    expect: ["1970"],
    ref: "Unix 时间戳 0 = 1970-01-01T00:00:00Z（UTC 纪元）",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { smartInput: "1735660800" },
    expect: ["识别为秒时间戳（10 位）", "2024-12-31T16:00:00.000Z"],
    ref: "智能粘贴识别·秒：1735660800 < 1e12 ⇒ 判秒，同步填秒/毫秒/日期三框并 renderResults。ISO 行由 date.toISOString() 输出，UTC 确定（免时区漂移）。默认态 smartInput 空 ⇒ hint 清空、零命中。两条 expect 均依赖被测输入（识别文案由位数决定、ISO 由时间值决定）。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { smartInput: "1735660800000" },
    expect: ["识别为毫秒时间戳（13 位）", "2024-12-31T16:00:00.000Z"],
    ref: "智能粘贴识别·毫秒：1735660800000 ≥ 1e12 ⇒ 判毫秒（等价 1735660800 s），与上条共用同一 ISO 锚、识别文案不同 ⇒ 互不命中、判别器可区分两态。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { smartInput: "946684800000" },
    expect: ["识别为毫秒时间戳（12 位）", "2000-01-01T00:00:00.000Z"],
    ref: "回归 IT-N43：按位数判定而非 n>=1e12 阈值。946684800000（12 位）= 2000-01-01T00:00:00Z 毫秒；修复前被当秒 ⇒ 31969-04-01，两条锚均不命中。expect 只锚注入态派生结果（位数文案 + UTC ISO，与运行时时区无关）。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { smartInput: "1700000000000000" },
    expect: ["识别为微秒时间戳（16 位）", "2023-11-14T22:13:20.000Z"],
    ref: "微秒支持：1700000000000000 µs = 1700000000000 ms = 1700000000 s = 2023-11-14T22:13:20Z（Python datetime.fromtimestamp(1700000000, UTC) 独立复算）。修复前 16 位 ≥1e12 被当毫秒 ⇒ 年份 55841，两条锚均不命中。",
  },
  {
    slug: "it/standard-deviation",
    inputs: { data: "1,2,3,4" },
    expect: ["1.291", "1.118"],
    ref: "statistics.stdev([1,2,3,4])=1.2910（样本，n-1）；pstdev=1.1180（总体，n）",
  },
  {
    slug: "it/hypothesis-test",
    // 回归保护：原实现双侧 p 用 p=2*(1-|Φ(z)-0.5|)，z=2 时得 1.046（p 值 >1）且结论反转。
    // 此处取 z=1.5（非默认输入）→ 正确 p=0.134 且不拒绝 H₀；默认输入为 z=2/p=0.046/拒绝 H₀。
    inputs: { mean: "103", mu0: "100", sigma: "10", n: "25", tail: "two" },
    expect: ["Z = 1.5，p = 0.134", "p=0.134 ≥ α=0.05，不拒绝 H₀"],
    ref: "se=10/√25=2，z=(103−100)/2=1.5，双侧 p=2(1−Φ(1.5))=0.13361（Python math.erf 独立复算）→ 不拒绝 H₀",
  },

  // —— §7.4 覆盖缺口线（BATCH161）——
  {
    slug: "it/atbash-cipher",
    inputs: { input: "abc" },
    expect: ["zyx"],
    ref: "阿塔巴什密码：字母表镜像 26−k+1 ⇒ a→z、b→y、c→x，'abc' 加密仍得 'zyx'。默认态 input 为空、encodeAtbash 走 alert 早退，结果区无 'zyx'（双态核验：注入 PASS / 默认 FAIL）。",
  },
  {
    slug: "it/bacon-cipher",
    inputs: { input: "ab", mode: "01" },
    expect: ["0000000001"],
    ref: "培根密码 mode=01：每字母 5 位，A=00000、B=00001 ⇒ 'ab' → '0000000001'。默认态 input 为空 ⇒ 早退，不命中。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", b: "10", op: "AND" },
    expect: ["结果： 8 = 0x8 = 0b1000"],
    ref: "12 & 10 = 8（二进制 1100 ∧ 1010 = 1000）；页面按 十进制/十六进制/二进制 三进制并排输出，锚完整连续串。默认 a=b=0 且 op=AND ⇒ 结果区为 0，不命中。",
  },
  {
    slug: "it/binary-to-text",
    inputs: { input: "01000001" },
    expect: ["A"],
    ref: "8 位二进制按字节解码：01000001 = 0x41 = 'A'。默认态解码区为空 ⇒ 不命中（双态核验已确认判别力；此处仅断言单字符是够用的，因为默认态 blob 完全不含该输出）。",
  },
  {
    slug: "it/binary-to-text",
    inputs: { input: "11111111 01000001" },
    clicks: ["(function(){var v=document.getElementById('output').value;document.getElementById('__tbProbe').innerHTML='B2TBAD '+((v.indexOf('非法 UTF-8')>=0||v.indexOf('invalid UTF-8')>=0)&&v.indexOf('Latin-1')>=0&&v.indexOf('0xFF')>=0?'OK':'BAD:'+v.slice(0,60));})()"],
    expect: ["B2TBAD OK"],
    ref: "IT-N247 非法 UTF-8：注入 FF 41（0xFF 非合法 UTF-8 起始），严格 TextDecoder 抛错后须给「非法 UTF-8 字节数 + Latin-1 对照 + 0xFF 字节列表」。旧实现 new TextDecoder() 默认 fatal:false ⇒ 静默得 U+FFFD「A」，无这些提示 ⇒ B2TBAD 红。诊断串只在 clicks 执行写入，默认态无 ⇒ 零逃生。",
  },
  {
    slug: "it/binary-to-text",
    inputs: { input: "11101111 10111011 10111111 01000001" },
    clicks: ["(function(){var v=document.getElementById('output').value;document.getElementById('__tbProbe').innerHTML='B2TBOM '+((v.indexOf('\\uFEFF')>=0||v.indexOf('BOM')>=0||v.indexOf('0xEF')>=0)?'OK':'BAD:'+JSON.stringify(v.slice(0,40)));})()"],
    expect: ["B2TBOM OK"],
    ref: "IT-N247 BOM：注入 EF BB BF 41（UTF-8 BOM + A），ignoreBOM:true 须保留 BOM（U+FEFF 或字节视图 0xEF），旧实现默认 ignoreBOM:false 把 3 字节 BOM 吞掉仅得「A」⇒ B2TBOM 红。诊断串只在 clicks 执行，默认态无 ⇒ 零逃生。",
  },
  {
    slug: "it/binary-to-text",
    clicks: ["(function(){var s=__binary_to_textScore('页面显示：错误');document.getElementById('__tbProbe').innerHTML='B2TSCORE '+(s===1?'OK':'BAD'+s);})()"],
    expect: ["B2TSCORE OK"],
    ref: "IT-N246 错误词启发式：解码出的正常文本若含「错误/失败/Invalid」等词，旧 __binary_to_textScore 将其判 0（历史有效性假性掉零），修复后恒记 1（非法输入已在 convert() alert 拦下）。探针传「页面显示：错误」断言 score=1；旧源码该串得分 0 ⇒ B2TSCORE BAD0 红。诊断串只在 clicks 执行，默认态无 ⇒ 零逃生。",
  },
  {
    slug: "it/adfgvx-cipher",
    inputs: { input: "abc" },
    expect: ["A A F D D G"],
    ref: "ADFGVX 多表替换：'abc' 经加密方格替换后再按 ADFGVX 列调位置排列，得 'A A F D D G'。默认态输入为空 ⇒ 不命中。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "10", p: "0.5", k: "3" },
    expect: ["P(X = 3) = 0.117", "C(10, 3) = 120"],
    ref: "X~B(10,0.5)：P(X=3)=C(10,3)·0.5³·0.5⁷=120×0.125×0.0078125=0.1172（Python comb(10,3)=120、binom.pmf(3,10,0.5)=0.1172）；分步区同步给出 C(10,3)=120。默认 n/p/k 与注入值不同，两串均不出现。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "10.5", p: "0.5", k: "3" },
    expect: ["n must be an integer from 1 to 10000"],
    ref: "IT-N241 整数校验：注入 n=10.5（小数），Number.isInteger 拒绝并报「n 必须为 1~10000 的整数」（harness 默认英文态读 data-zh 的英文本）。旧实现 parseInt('10.5')=10 静默截断、照常算出 P(X=3)=0.117 ⇒ 不含该错误串，红。默认 n=10 合法不命中。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "20000", p: "0.5", k: "3" },
    expect: ["n cannot exceed 10000"],
    ref: "IT-N241 上限：注入 n=20000 超过新上限 10000 ⇒ 提示「n 不能超过 10000，更大样本请用正态/Poisson 近似」。旧实现无上限、照常逐项算 cdf（O(n²) 冻页隐患）⇒ 不含该串，红。默认 n=10 不命中。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "1030", p: "0.5", k: "515" },
    expect: ["e^{710.25}"],
    ref: "IT-N242 大组合数对数形式：n=1030,k=515 ⇒ ln C(1030,515)=710.25，Math.exp 溢出为 Infinity，步骤区应显示 e^{710.25} 而非「未定义」。旧实现 fmt(Math.round(exp(logComb))) 得 Infinity→「未定义」⇒ 不含该串，红。默认 n=10 的 C(10,5)=252 走数值分支不命中。e^{710.25} 由 Node 独立 logComb 复算。",
  },
  {
    slug: "it/clamp-calculator",
    // IT-N291/N292：首选值锁定视口中点，min/max 锁定两端；中间两段折线共用同一函数。
    // 注入 min=10 / max=100 / vwMin=50（pref 用默认 24、vwMax 默认 1440）⇒ 中点745px，两段分别 2.014vw+8.993px 与 10.935vw−57.466px。
    inputs: { min: "10", max: "100", vwMin: "50" },
    expect: ["生成表达式： clamp(10px, max(2.014vw + 8.993px, 10.935vw - 57.466px), 100px)"],
    ref: "IT-N291 独立复算：中点=(50+1440)/2=745；slope1=2×(24−10)/1390×100=2.014vw，r1=10−2.014×0.5=8.993px；slope2=2×(100−24)/1390×100=10.935vw，r2=24−10.935×7.45=−57.466px；slope1<slope2 ⇒ max(...)；clamp(10px, max(2.014vw + 8.993px, 10.935vw - 57.466px), 100px)。旧实现按 pref 锚定单线 5.47vw+21.27px，不命中；默认参数不命中。",
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "100", std: "15", n: "30", conf: "0.95" },
    expect: ["[ 94.632 , 105.368 ]"],
    ref: "独立复算：SE=s/√n=15/√30=2.7386；95% 双侧 z=1.960 ⇒ ME=1.960×2.7386=5.3677 ⇒ CI=[94.632, 105.368]。默认输入不同（区间两端数不同）⇒ 该串不出现。原第二条锚「临界值 z = 1.960」是 α=0.05 双侧常量、默认态即出现（静态文案），已删。",
  },
  {
    slug: "it/code-line-counter",
    // textarea 注入带换行的代码：input event 阶段直接喂多行串（runner 的 inputs 支持多行值）。
    inputs: { codeInput: "def f():\n    return 1\n", langSel: "python" },
    expect: ["3 总行数 2 代码行 0 注释行 1 空行 66.7% 代码占比"],
    ref: "注入 3 行文本（末行为空）：总行数 3 = 2 代码行 + 1 空行，代码占比 2/3=66.7%。默认示例代码行数与占比不同 ⇒ 不命中。detectLang 在注入非空时可用，故结果区实际刷新。",
  },
  {
    slug: "it/charset-detector",
    inputs: { txt: "hello" },
    expect: ["未检测到明显乱码特征。 修复输出： hello"],
    ref: "普通 ASCII 文本无乱码特征 ⇒ 判为「未检测到明显乱码特征」并把原文原样回吐为修复结果。默认态正文（中文占位）走另一分支，不命中（双态核验：注入 PASS / 默认 FAIL）。",
  },
  {
    // IT-N495 锁定：修复输出必须先转义再写 innerHTML（旧版直接拼模板串，输入 HTML 即执行）
    slug: "it/charset-detector",
    inputs: { txt: "<img src=x onerror=N495MARK>" },
    expect: ["&lt;img src=x onerror=N495MARK&gt;"],
    ref: "IT-N495：页面把原文回吐为「修复输出」时必须转义。修复前模板串直接拼 `${fixed}`，blob 采集会剥掉裸 `<img …>` 标签，带 `&lt;` 的串根本不存在；修复后 escOut 输出 `&lt;img src=x onerror=N495MARK&gt;`。哨兵 N495MARK 由输入决定，默认示例不含。",
  },
  {
    slug: "it/charset-detector",
    // 「中文」的 UTF-8 字节 E4 B8 AD E6 96 87 被按 cp1252 解读 ⇒ ä¸­æ–‡
    inputs: { txt: "\u00e4\u00b8\u00ad\u00e6\u2013\u2021" },
    expect: [
      "疑似 UTF-8 字节被按 Latin-1/Windows-1252 解读，已按字节还原。 修复输出： 中文",
      "中日韩字符 2 · 拉丁字母 0 · 替换符 0 · 控制字符 0",
    ],
    ref: "双重编码还原：输入 ä¸­æ–‡（含软连字符 U+00AD、短破折号 U+2013、双剑号 U+2021）折算回字节 E4 B8 AD E6 96 87，按 UTF-8 解码得「中文」。首条把判定语与还原结果拼成复合串，避免默认示例本身也是乱码导致判定语恒命中；旧实现只做 6 条固定串替换，无法还原该串，两条均不命中。",
  },
  {
    slug: "it/hypergeometric-distribution",
    // 超几何分布：P(X=k)=C(K,k)·C(N−K,n−k)/C(N,n)。N=20,K=5,n=3,k=2 ⇒ 10×15/1140=0.13158。
    inputs: { N: "20", K: "5", n: "3", k: "2" },
    expect: ["P(X = 2) = 0.132", "C(20, 3) = 1,140"],
    ref: "Python comb(5,2)=10、comb(15,1)=15、comb(20,3)=1140 ⇒ P=10×15/1140=0.1316（页面渲染 0.132、分步区给出 C(20,3)=1,140）。默认 N/K/n/k 与注入值不同，两串均不出现。",
  },
  {
    slug: "it/hmac-generator",
    // 页面 crypto.subtle.importKey 在 harness 下抛 2，但结果区仍渲染出正确 HMAC 串 ⇒ 走的是页面自实现分支。
    inputs: { key: "secret", msg: "hello" },
    expect: ["HMAC-SHA1 5112055c05f944f85755efc5cd8970e194e9f45b",
             "HMAC-SHA256 88aab3ede8d3adf94d26ab90d3bafd4a2083070c3bcce9c014ee04a443847c0b"],
    ref: "Python hmac.new(b'secret', b'hello', sha1).hexdigest() = 5112055c05f944f85755efc5cd8970e194e9f45b；sha256 = 88aab3ede8d3adf94d26ab90d3bafd4a2083070c3bcce9c014ee04a443847c0b（四档 SHA1/256/384/512 页侧与 Python 逐一核对一致）。注：harness 下 subtle.importKey 抛错，但结果区仍落正确值，断言的是「正确值」而非错误分支。",
  },
  {
    slug: "it/json-minify",
    inputs: { input: '{"a": 1, "b": [2, 3]}' },
    expect: ['{"a":1,"b":[2,3]}', "原始 21 字节 → 输出 17 字节 · Compression ratio 19.0%"],
    ref: "独立复算：原文 len('{\"a\": 1, \"b\": [2, 3]}')=21、压缩后 len('{\"a\":1,\"b\":[2,3]}')=17 ⇒ 比值 (21−17)/21=19.05% ⇒ 页面渲染 19.0%。默认示例的字节数与比值均不同 ⇒ 不命中。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":{"b":[1,2,3]}}', path: "$.a.b" },
    expect: ["[ 1 , 2 , 3 ]"],
    ref: "JSONPath 表达式 $.a.b 命中数组 [1,2,3] ⇒ 输出按页侧格式展开为 `[ 1 , 2 , 3 ]`。默认 path 与默认 JSON 不同，不命中；expr 不以 $ 开头时页面直接报错（`jsonPath: JSONPath 表达式必须以 $ 开头`），不影响本例。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":[1,2,3,4,5]}', path: "$.a[4:0:-1]" },
    expect: ["[ 5 , 4 , 3 , 2 ]"],
    ref: "IT-N489 复核失败重做：负步长切片。$.a[4:0:-1] 应从索引 4 向 0（不含）迭代 ⇒ [5,4,3,2]；修复前负步长分支写成 for(i=e0-1;i>=s0;...)，把起止语义颠倒，实得 []。结果格式按页侧 join(' , ')。默认 JSON/path 不命中 ⇒ 可判别。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":[1,2,3,4,5]}', path: "$.a[::-1]" },
    expect: ["[ 5 , 4 , 3 , 2 , 1 ]"],
    ref: "IT-N489 负步长省略边界分支：$.a[::-1] 应整体反转 ⇒ [5,4,3,2,1]；修复前省略上界配合颠倒循环得 []。验证步长方向 + 省略边界按方向收敛（负步长默认 start=len-1、end=-1）。",
  },
  {
    slug: "it/keyword-density",
    inputs: { inputText: "aa bb aa cc bb aa dd" },
    expect: ["排名 关键词 出现次数 占比 密度条 1 aa 3 42.86%"],
    ref: "注入 7 token（aa×3、bb×2、cc×1、dd×1）⇒ 排行表首行「aa 3 42.86%」（3/7=42.86%）；默认正文的排行表完全不同 ⇒ 不命中。锚取「表头 + 首行」的连续串，避免只锚 42.86% 这类可能被默认态作为子串命中的短数值。",
  },
  {
    slug: "it/locale-lookup",
    inputs: { input: "zh-CN" },
    expect: ["语言（ISO 639-1）： zh 国家（ISO 3166-1）： CN 完整名称： 简体中文（中国大陆）"],
    ref: "locale 标签解析：zh-CN ⇒ 语言 zh / 国家 CN / 完整名「简体中文（中国大陆）」/ 书写系统 Hans / 排序拼音。默认输入不同 ⇒ 不命中（双态核验：注入 PASS / 默认 FAIL）。",
  },
  {
    slug: "it/locale-lookup",
    inputs: { input: "de-1996-1996" },
    expect: ["不符合 BCP 47 格式"],
    ref: "IT-N421：重复 variant 必须拒绝。`de-1996-1996` 含两个相同 variant 1996，Intl.getCanonicalLocales 以 RangeError 拒绝；原正则 LC_RE 不查重误判有效。现 __lcValid 增加 variant/扩展单例去重检查。expect 命中「不符合 BCP 47 格式」提示（默认 en-US 命中「✅ 有效」串、不命中「不符合」）⇒ 强判别；回退去重检查后必红。"
  },
  {
    slug: "it/locale-lookup",
    inputs: { input: "en-u-ca-gregory-u-nu-latn" },
    expect: ["不符合 BCP 47 格式"],
    ref: "IT-N421：重复扩展单例 u 必须拒绝。`en-u-ca-gregory-u-nu-latn` 含两个 u 扩展单例，Intl.getCanonicalLocales 拒绝；现单例去重检查拦截。expect 命中「不符合 BCP 47 格式」（默认态不命中）⇒ 强判别。"
  },
  {
    slug: "it/ipv6-converter",
    // 注意：默认地址（2001:db8::1）与注入值同串，属逃生项；改用非默认地址即可。
    inputs: { addr: "fe80::abcd" },
    expect: ["压缩形式：fe80::abcd"],
    ref: "IPv6 展开 + 压缩：fe80::abcd ⇒ 全展 `fe80:0000:…:abcd`、压缩回 `fe80::abcd`。**踩坑记录**：注入 `2001:db8::1`（也是页面默认地址）时默认态同样命中（逃生项，via=calcTool）；换成 fe80::abcd 后双态通过。",
  },
  {
    slug: "it/ipv6-converter",
    inputs: { addr: "::ffff:192.0.2.1" },
    clicks: ["calcTool()"],
    expect: ["压缩形式：::ffff:c000:201", "0000:0000:0000:0000:0000:ffff:c000:0201"],
    ref: "回归 IT-N52·IPv4 映射：末尾点分十进制 192.0.2.1 → c0/00/02/01 ⇒ 两组 c000、0201；展开为 0000:0000:0000:0000:0000:ffff:c000:0201，规范压缩为 ::ffff:c000:201（RFC 4291 §2.2 / RFC 5952 最长零段、左侧优先）。修复前正则只认 1-4 位十六进制 ⇒ 直接报「不是合法 IPv6」。默认地址 2001:db8::1 不含两锚。",
  },
  {
    slug: "it/ipv6-converter",
    inputs: { addr: "64:ff9b::192.0.2.1" },
    clicks: ["calcTool()"],
    expect: ["压缩形式：64:ff9b::c000:201"],
    ref: "IPv4 内嵌（非 ffff 前缀）：64:ff9b::192.0.2.1 → 64:ff9b::c000:0201 ⇒ 最长零段（4 组）压缩为 64:ff9b::c000:201。与上条共用同一 IPv4 转换路径、不同前缀位置，默认地址不命中。",
  },
  {
    slug: "it/ipv6-converter",
    inputs: { addr: "::ffff:192.168.001.001" },
    clicks: ["calcTool()"],
    expect: ["不是合法的 IPv6 地址"],
    ref: "内嵌 IPv4 前导零：RFC 3986 / Python ipaddress 均不接受 `001` 这样的八位组（可能被解释为八进制）。旧 ipv4ToHex 用 Number('001')=1 静默接受并输出 ::ffff:c0a8:101；修复后报非法。默认 2001:db8::1 不含该提示。",
  },
  {
    slug: "it/ipv4-range-expander",
    inputs: { cidr: "192.168.1.0/30" },
    expect: ["192.168.1.0 网络地址 192.168.1.3 广播地址 2 可用主机数 30 前缀长度"],
    ref: "/30 网段：网络地址 192.168.1.0、广播 192.168.1.3、可用主机 2（4−2）。默认示例前缀不同 ⇒ 不命中。",
  },
  {
    slug: "it/ipv4-range-expander",
    inputs: { cidr: "10.0.0.0/31" },
    expect: ["可用范围： 10.0.0.0 – 10.0.0.1"],
    ref: "RFC 3021 / Python ipaddress：/31 点对点链路的两个地址均可使用（hosts=2），可用范围即网络地址到广播地址。旧实现按 `pref>=31 ⇒ 0` 报 0 个，与 it/calc-subnet 的 /31=2 自相矛盾；默认 /24 不出现该串。",
  },
  {
    slug: "it/ipv4-range-expander",
    inputs: { cidr: "10.0.0.1/32" },
    expect: ["可用范围： 10.0.0.1"],
    ref: "Python ipaddress：/32 为单主机地址（hosts=1），可用范围就是该地址本身。旧实现报 0 且不输出可用范围；默认 /24 不出现该串。",
  },
  {
    slug: "it/ipv4-range-expander",
    inputs: { cidr: "10.0.0.01/32" },
    expect: ["IP 须合法"],
    ref: "按 Python ipaddress / it/calc-subnet 口径：前导零八位组（01）非法，不能静默当 1 解析。旧实现 `+'01'` 得 1 并输出 10.0.0.1（含前导零的歧义输入被静默接受）；默认 /24 无错误提示。",
  },
  {
    slug: "it/poisson-distribution",
    // 泊松分布 P(X=k)=λ^k·e^(−λ)/k!。λ=2,k=3 ⇒ 8×0.13534/6=0.180。
    inputs: { lambda: "2", k: "3" },
    expect: ["P(X = 3) = 0.18", "步骤 1： λ 3 = 8"],
    ref: "独立复算：λ^k=2³=8、e^(−2)=0.13534、k!=6 ⇒ P=8×0.13534/6=0.180（页面渲染 0.18），分步区同时给出 λ 3 = 8。默认 λ/k 与注入值不同 ⇒ 不命中。",
  },
  {
    slug: "it/numeronym-generator",
    inputs: { input: "global navigation" },
    expect: ["navigation → n8n"],
    ref: "IT-N286：默认最小字母数 7，global(6<7) 原样保留、navigation(11≥7) → n8n（首字母+8中间字母+尾字母）。修复前无阈值 global→g4l ⇒ 旧 expect 含 g4l；默认示例单词不同 ⇒ 不命中。",
  },
  {
    slug: "it/numeronym-generator",
    clicks: ["var a=numeronym('internationalization,',7),b=numeronym('(internationalization)',7);document.getElementById('__tbProbe').textContent='PUNCT '+(a==='i18n,'&&b==='(i18n)'?'OK':'BAD:'+a+'/'+b);"],
    expect: ["PUNCT OK"],
    ref: "IT-N285：带标点的词须取纯字母串首尾并保留前后标点（internationalization, → i18n,、(internationalization) → (i18n)）。修复前取 w[0]/w[last] ⇒ i18, / (18) ⇒ PUNCT BAD。",
  },
  {
    slug: "it/numeronym-generator",
    clicks: ["var cap=null;ToolBox.copyText=function(t){cap=t;};document.getElementById('input').value='internationalization';generate();copyOut();document.getElementById('__tbProbe').textContent='COPY '+(cap==='i18n'?'OK':'BAD:'+cap);"],
    expect: ["COPY OK"],
    ref: "IT-N287：「复制结果」须复制大号展示区 #outBig 的缩写结果（i18n），不是 #output 的逐词对照（internationalization → i18n）。修复前复制对照表 ⇒ COPY BAD。另 i18nText 已定义，空结果 toast 不再 undefined。",
  },
  {
    slug: "it/prime-checker",
    // 注：n=97 的「97 是质数 ✅」是默认态同串（逃生项，via=calcTool），故改用 n=2 这个最小质数。
    inputs: { n: "2" },
    expect: ["2 是质数"],
    ref: "2 是最小质数。踩坑：注入 n=97 得到「97 是质数 ✅」在默认态同样命中（默认示例就是 97），属逃生项 ⇒ 改用 n=2（同样为真质数，但默认态不出现）。",
  },
  {
    slug: "it/rail-fence-cipher",
    // 只锚矩阵展示串：depth=2 的轨道矩阵 row0 取下标 0/2/4、row1 取 1/3/5。
    // 实测 enc/dec 两条渲染路径下 `acbbac` / `aabbcc` / `abcabc` 三串在注入态都能命中（分别由 enc/dec/默认渲染写入），
    // 故不存在「输出与逐行读法不符」的缺陷，别据此写缺陷报告。
    inputs: { input: "abcabc", depth: "2" },
    expect: ["行0: a · c · b · 行1: · b · a · c"],
    ref: "轨道围栏 depth=2：下标偶数位归入 row0（a,c,b）、奇数位归入 row1（b,a,c）⇒ 矩阵展示串 `行0: a · c · b · 行1: · b · a · c`。默认示例（不同 depth/文本）不命中。",
  },
  {
    slug: "it/triangle-calculator",
    // 三边 5/6/7 的最大角为 arccos(12/60)=78.46° < 90° ⇒ 锐角三角形；
    // 海伦面积 √(9·4·3·2)=√216≈14.697。默认态默认边 3/4/5 是直角三角形，不命中。
    inputs: { a: "5", b: "6", c: "7" },
    expect: ["锐角三角形", "14.697"],
    ref: "独立复算：p=18、s=9、area=√(9×4×3×2)=14.697；最大角 arccos((25+36−49)/60)=78.46° ⇒ 锐角三角形。踩坑：注入 3/4/5 与页面默认值相同 ⇒ 逃生项，改用 5/6/7。",
  },
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "1600000000" },
    expect: ["2020-09-13T12:26:40.000Z"],
    ref: "Unix 秒 1600000000 = 2020-09-13T12:26:40.000Z（UTC）。踩坑：默认 1700000000，注入值撞默认会逃生。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: {"prior":"0","likelihood":"0.9","falsePositive":"0.05"},
    clicks: ["calculate();var s=document.getElementById('output').innerHTML;var p=s.indexOf('边界说明');document.getElementById('__tbProbe').textContent='BAYES0 '+s.slice(p,p+160).replace(/<[^>]*>/g,'');"],
    expect: ["BAYES0 边界说明：先验 P(H₁) = 0 时 P(¬H₁) = 1，先验优势 0/1 = 0；此时证据无法再改变信念，后验恒为 0。先验 vs 后验对比<span class=\"nam"],
    ref: "复核失败重做·IT-N374 1/2（prior=0 边界说明）：旧说明把 prior=0 与 prior=1 混为一谈，误写「P(¬H₁)=0、先验优势 0/0 发散」。prior=0 实际 P(¬H₁)=1、先验优势 0/1=0，不发散。修复后 BAYES0 边界说明写「P(¬H₁) = 1，先验优势 0/1 = 0」；修复前写「P(¬H₁) = 0，先验优势 0/0 发散为 0」⇒ 真变红。默认态 prior=0.01 不进边界分支、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "it/bayes-theorem",
    inputs: {"prior":"0.01","likelihood":"0.9","falsePositive":"0"},
    clicks: ["calculate();var s=document.getElementById('output').innerHTML;document.getElementById('__tbProbe').textContent='BAYESBF inf='+(s.indexOf('<div class=\"v\">∞</div><div class=\"l\">贝叶斯因子 BF')>=0?1:0)+' undef='+(s.indexOf('<div class=\"v\">未定义</div><div class=\"l\">贝叶斯因子 BF')>=0?1:0);"],
    expect: ["BAYESBF inf=1 undef=0"],
    ref: "复核失败重做·IT-N374 2/2（BF 发散语义）：误报率 fp=0 时贝叶斯因子 BF=∞，统计卡必须用 fmtOdds 显示 ∞ 而不是 fmt 的「未定义」。探针在 #output 精确锚定 `<div class=\"v\">∞</div><div class=\"l\">贝叶斯因子 BF`，修复后 inf=1 undef=0；修复前 inf=0 undef=1 ⇒ 真变红。默认态 fp=0.05 不产生 ∞ ⇒ 零逃生。"
  },
  {
    slug: "it/statistical-power",
    inputs: {"d":"0.0001","alpha":"0.05","tail":"two","solveFor":"size","targetPower":"0.001"},
    clicks: ["calculate()"],
    expect: ["所需样本量 = 1（每组）", "0.0001 效应量 d"],
    ref: "小效应量低目标功效：正算 n=1 已满足目标，反解结果和效应量显示均须正确。"
  },
  {
    slug: "it/statistical-power",
    inputs: {"d":"0.5","alpha":"0.05","tail":"two","solveFor":"size","targetPower":"0.001"},
    clicks: ["calculate();var s=document.getElementById('output').innerHTML;var p=s.indexOf('反解');document.getElementById('__tbProbe').textContent='PWRMIN '+s.slice(p,p+200).replace(/<[^>]*>/g,'');"],
    expect: ["PWRMIN 反解：n = ⌈2×((z₁₋α' + z₁₋β)/d)²⌉ = ⌈2×((1.96 + -3.09)/0.5)²⌉ = 11（正态近似候选）；用本页正算公式二分核验后，满足目标功效 0.001 的最小每组样本量 = 1步骤 1：非中心参数 δ = d × √(n/2) = 0.5 ×"],
    ref: "复核失败重做·IT-N375 1/2（低功效反解过度估计）：solveFor=size、d=0.5、α=0.05、targetPower=0.001、双侧时，正态近似给出候选 n=11，但本页正算公式在 n=1 已达 0.001 目标功效。修复后从候选向下逐整数核验，给出最小每组样本量 1；修复前直出 11 ⇒ 真变红。默认态 solveFor 非 size、无「反解」行 ⇒ 零逃生。"
  },
  {
    slug: "it/statistical-power",
    inputs: {"d":"0.3","alpha":"0.01","tail":"two","solveFor":"size","targetPower":"0.01"},
    clicks: ["calculate();var s=document.getElementById('output').innerHTML;var p=s.indexOf('反解');document.getElementById('__tbProbe').textContent='PWRCHK '+s.slice(p,p+200).replace(/<[^>]*>/g,'');"],
    expect: ["PWRCHK 反解：n = ⌈2×((z₁₋α' + z₁₋β)/d)²⌉ = ⌈2×((2.576 + -2.326)/0.3)²⌉ = 2（正态近似候选）；用本页正算公式二分核验后，满足目标功效 0.01 的最小每组样本量 = 1步骤 1：非中心参数 δ = d × √(n/2) = 0.3 ×"],
    ref: "复核失败重做·IT-N375 2/2（近似偏保守回退一整级）：d=0.3、α=0.01、targetPower=0.01 时近似候选 n=2，正算核验 n=1 已达标。修复后最小样本量 1；修复前 2 ⇒ 真变红。与上例共同覆盖「向下收敛多级」与「收敛一级」，默认态不触发 ⇒ 零逃生。"
  },
  {
    slug: "it/statistical-power",
    // 只锚「功效 = 88.54%」；原 expect 第二条「临界值 z* = 1.96」是 α=0.05 双侧常量，
    // 默认态同样命中 ⇒ 逃生项（判据⑤静态常量），已剔除。
    inputs: { d: "1", n: "20", alpha: "0.05", tail: "two" },
    expect: ["功效 = 88.54%"],
    ref: "独立复算：δ=d×√(n/2)=1×3.162=3.162，z*=1.96 ⇒ 功效=Φ(1.202)+Φ(−5.122)≈0.885 ⇒ 88.5%；默认 d=0.5/n=64 得 80.7%，不命中。",
  },
  {
    slug: "it/statistical-power",
    inputs: { d: "0.5", alpha: "0.05", tail: "two", solveFor: "size", targetPower: "0.8" },
    clicks: ["calculate()"],
    expect: ["所需样本量 = 63（每组），实际功效 80.13%"],
    ref: "IT-N375：页面承诺「四要素知三求一 / 求所需样本量」，修复前只有功效一个输出、没有求解模式。「求解目标」选「求样本量」后按 n = ⌈2((z₁₋α/₂+z₁₋β)/d)²⌉ 反解：z₁₋α/₂=1.95996、z₁₋β=0.84162、d=0.5 ⇒ 2×((1.95996+0.84162)/0.5)² = 62.79 ⇒ n=63；再用 n=63 复核功效 δ=0.5×√31.5=2.8062，Φ(2.8062−1.95996)=0.8013 ⇒ 80.13%。expect 是反解出来的样本量与复核功效，输入里只有 0.5/0.05/0.8 ⇒ 非回显；修复前页面无 #solveFor，#targetPower 也无效 ⇒ 走的是求功效分支、输出「功效 = …%」而非该串 ⇒ 必红灯。",
  },
  {
    slug: "it/text-truncate",
    // 默认「省略号」select 值为 "..."；words 模式 limit=2 ⇒ "Alpha beta" + "..."。
    inputs: { input: "Alpha beta gamma delta", limit: "2", mode: "words" },
    expect: ["Alpha beta..."],
    ref: "独立复算：按空白切词取前 2 个 ⇒ `Alpha beta`，附加省略号 `...`（页面省略号默认选项）⇒ `Alpha beta...`。默认态是长中文文本 + limit 20，不命中。",
  },
  {
    slug: "it/text-truncate",
    // IT-N15 回归：按码点截断，省略符计入上限。
    inputs: { input: "😀😀😀", limit: "2", mode: "chars", ellipsis: "…" },
    clicks: ["truncate()"],
    expect: ["😀…"],
    ref: "独立复算：3 个 emoji 按码点计 3 > limit 2，省略符占 1 个码点 ⇒ 保留 1 个 emoji + `…`，总长恰为 2；修复前按 UTF-16 码元 substring 会把首个 emoji 切成半个代理对。默认态无 emoji，不命中。",
  },
  {
    slug: "it/text-truncate",
    inputs: { input: "abcdef", limit: "5", mode: "chars", ellipsis: "..." },
    clicks: ["truncate()"],
    expect: ["ab..."],
    ref: "独立复算：6 字符 + 省略符 `...`(3) ⇒ 保留 2 字符 + 3 点 = 5，不再输出 8 字符；修复前省略符不占 limit ⇒ `abcde...`。默认态长中文文本不命中。",
  },
  {
    slug: "it/text-truncate",
    // IT-N15 回归：省略符自身超过字符上限时按上限截断，结果不超过 limit
    inputs: { input: "abcdef", limit: "2", mode: "chars", ellipsis: "..." },
    clicks: ["truncate()"],
    expect: ["abcdef\n..\nchars\n2"],
    ref: "独立复算：limit=2、省略符 '...' 含 3 字素 > limit=2，N15 修复后按上限截断省略符取前 2 字素 ⇒ 输出 '..'（2 字，不超过 limit）；修复前 budget=Math.max(0,2-3)=0 ⇒ 输出完整 '...'(3 字) 超上限。原 expect 只写 '..'，而默认态结果「请输入文本...」含 '..' ⇒ 判别器判为逃生项；现锚扩展为依赖注入的完整上下文「输入\\n结果\\n模式\\n上限」。默认态为长中文文本 + limit 20，不命中。",
  },
  {
    slug: "it/text-truncate",
    inputs: { input: "😀abc", limit: "4", mode: "bytes", ellipsis: "!!" },
    clicks: ["truncate()"],
    expect: ["!!"],
    ref: "独立复算：emoji 实为 4 字节 > limit 扣除省略符 `!!`(2) 后的 2 字节预算 ⇒ 保留 0 字符、只输出 `!!`；修复前把 emoji 记 1 码元 ⇒ 4 个字符恰好不截断、输出 `😀abc`。注入非选项省略符仅为让字节边界可观测，默认态不命中。",
  },
  {
    slug: "it/text-truncate",
    inputs: { input: "abc", limit: "0" },
    clicks: ["truncate()"],
    expect: ["请输入有效的保留数量"],
    ref: "独立复算：0 不是正整数 ⇒ 明确提示；修复前被 `||0` 吞成 0 后仍输出省略符。默认态 limit=20，不命中。",
  },
  {
    slug: "it/text-statistics",
    inputs: { textInput: "ab cd ab ef" },
    expect: ["11 总字符(字素)", "4 总词数"],
    ref: "独立复算：\"ab cd ab ef\" 共 11 个字符（含 2 个空格，字素簇口径同上）、按空白切出 4 个英文词、去重 3 个 ⇒ `11 总字符(字素)` / `4 总词数`。默认态为中文长文本，不命中。",
  },
  {
    slug: "it/string-obfuscator",
    // mode 取值是 b64（不是 base64）；选错 mode 会落到空结果分支（输出 0 字符）。
    inputs: { input: "Hi there 42", mode: "b64" },
    expect: ["SGkgdGhlcmUgNDI="],
    ref: "独立复算：b64(\"Hi there 42\")=\"SGkgdGhlcmUgNDI=\"（16 字符），与页面「输出 16 字符」自洽。踩坑：mode=base64 不是合法选项。",
  },
  {
    slug: "it/toml-to-json",
    // 锚空输入兜底分支。该页曾因 `document.getElementById('sort')` 取到 null（排序复选框实际 id 为 top_1）
    // 在加载即抛 TypeError、整页无输出（jsdom 已验证，2026-09-26 修正为 id=\"sort\"）。
    // 本例锁的是修正后的空输入分支；JSON 正文走 escH()，harness 的 createElement 桩不回写
    // textContent→innerHTML（既有盲区），故无法锚 JSON 内容。
    inputs: { source: "" },
    expect: ["请输入 TOML 文本"],
    ref: "空输入时页面写入 `请输入 TOML 文本`；默认 TOML 非空不命中。该页此前为 P0 死页（sort id 不匹配），修复后本例才有判别力。",
  },
  // ---- IT-N385/N386/N387：toml-to-json 解析层修复 ----
  // 采集说明：JSON 正文走 escH()（createElement → textContent → innerHTML，桩已建模该联动），
  // 只有 & < > 会转义，引号/大括号保留原样；#result 的 innerHTML 剥标签后空白折叠成单空格。
  {
    slug: "it/toml-to-json",
    inputs: { source: 'point = { x = 1, y = 2 }' },
    expect: ['"point": { "x": 1, "y": 2 }'],
    ref: "IT-N385：内联表必须递归解析成对象。修复前 tVal 无 `{}` 分支 ⇒ 整串原样当字符串（`\"point\": \"{ x = 1, y = 2 }\"`）。默认样例无 point 键。",
  },
  {
    slug: "it/toml-to-json",
    inputs: { source: "a = 1_000\nh = 0xFF" },
    expect: ['"a": 1000, "h": 255'],
    ref: "IT-N385：数字下划线与十六进制必须按数值解析。修复前整数正则 `^-?\\d+$` 不接受 `_` ⇒ `\"a\": \"1_000\"`；`0xFF` 同样降级成字符串。默认样例无 a/h 键。",
  },
  {
    slug: "it/toml-to-json",
    inputs: { source: 'list = ["a,b", "c"]' },
    expect: ['"list": [ "a,b", "c" ]'],
    ref: "IT-N386：数组必须按「顶层逗号」切分。修复前 `inner.split(',')` 无视引号 ⇒ `[\"\\\"a\", \"b\\\"\", \"c\"]`（四个残片）。默认样例无 list 键。",
  },
  {
    slug: "it/toml-to-json",
    inputs: { source: "ports = [\n  8000,\n  8001\n]" },
    expect: ['"ports": [ 8000, 8001 ]'],
    ref: "IT-N386：多行数组必须跨行累积。修复前逐行解析 ⇒ `ports = [` 当行即得空数组、后续 8000/8001 因无 `=` 被跳过 ⇒ `\"ports\": []`。默认样例无 ports 键。",
  },
  {
    slug: "it/toml-to-json",
    inputs: { source: "zzq = 1" },
    clicks: ["document.getElementById('indent').value='tab';calcTool();var h=document.getElementById('result').innerHTML;document.getElementById('result').textContent='N387 tab='+(h.indexOf(String.fromCharCode(9))>=0?1:0)+' key='+(h.indexOf('zzq')>=0?1:0);"],
    expect: ["N387 tab=1 key=1"],
    ref: "IT-N387：选 Tab 缩进必须输出真正的制表符 0x09。修复前三元写成 `'\\\\t'`（源码里是两个字面字符反斜杠+t）⇒ 输出 `\\t` 文本；blob 会把空白折叠成空格、无法断定制表符，故用 clicks 直接查 innerHTML 的 charCode 9。`key=1` 让判定串依赖入参键名。",
  },
  {
    slug: "it/sql-formatter",
    // textarea 无 oninput ⇒ 注入不触发重算，必须在 clicks 里显式调 formatSql()。
    inputs: { input: "select a,b from t where a=1" },
    clicks: ["formatSql()"],
    expect: ["SELECT a, b FROM t WHERE a=1"],
    ref: "独立复算：关键字大写 + `a,b` 逗号后补空格 ⇒ `SELECT a, b FROM t WHERE a=1`（值 `a=1` 不加空格，与输入一致）。默认示例是长联表 SQL，不命中。",
  },
  {
    slug: "it/slugify",
    inputs: { input: "Hello World ToolBox" },
    expect: ["Hello-World-ToolBox"],
    ref: "独立复算：空格转连字符 ⇒ `Hello-World-ToolBox`（默认 `mode=空白转-`）。默认输入是中文标题（走拼音分支），不命中。",
  },
  {
    slug: "it/slugify",
    // IT-N16 回归：Unicode 模式先剥离符号再转义，% 不得被剔除。
    inputs: { input: "中文" },
    clicks: ["document.getElementById('mode').value='unicode';generate()"],
    expect: ["%e4%b8%ad%e6%96%87"],
    ref: "独立复算：中文 2 字分别转义为 `%e4%b8%ad` / `%e6%96%87` 并拼接；修复前先转义后被符号过滤把 `%` 变空格 ⇒ `e4-b8-ad-e6-96-87`。默认态走拼音分支，不命中。",
  },
  {
    slug: "it/slugify",
    // IT-N16 回归：下划线预览按实际分隔符替换。
    inputs: { input: "aaa bbb" },
    clicks: ["document.getElementById('separator').value='.';generate()"],
    expect: ["aaa_bbb"],
    ref: "独立复算：separator='.' 时标准 slug=`aaa.bbb`，下划线预览应按实际分隔符替换 ⇒ `aaa_bbb`；修复前只替换 `-`，预览仍是 `aaa.bbb`。默认态 separator='-'、输入为中文标题，不命中。",
  },
  {
    slug: "it/summary-generator",
    // boot 挂在 DOMContentLoaded（晚于注入）且会调 loadExample() 重置 inputText ⇒ 文本注入无效，改用不被 boot 重置的句数参数。
    inputs: { sentenceCount: "8" },
    clicks: ["generateSummary()"],
    expect: ["8\n10\n8\n469\n25%"],
    ref: "IT-N547 功能改动同批换锚（铁律①/⑥）：分句器不再按顿号切分后，示例由 14 句变 10 句，原锚「技术不断演进。 已选」在纯默认态也命中 ⇒ 判别器判为逃生项。改用随注入句数变化的统计卡四联值：句数选择 8 / 原文 10 句 / 摘要 8 句 / 字符 469 / 压缩率 25%；默认态为 5 / 10 / 5 / 469 / 59% ⇒ 不命中。",
  },
  {
    slug: "it/summary-generator",
    clicks: ["var __ss=[];for(var i=0;i<60;i++){__ss.push({text:'q'+String.fromCharCode(97+(i%26))+String.fromCharCode(97+Math.floor(i/26))});}var __r=window.__sgDiag.computeWordFrequency(__ss);document.getElementById('summaryResult').textContent='N546_KW='+Object.keys(__r.freq).length;"],
    expect: ["N546_KW=20"],
    ref: "IT-N546：构造 60 句、每句一个互不相同且只出现 1 次的词，旧阈值「词频 ÷ 句数 > 5%」（1/60≈1.7%）会把全部词滤掉 ⇒ 关键词数 0、每句 kwW=0、句子权重全 0（摘要退化成按原序取前 N 句）。新口径过滤后为空时取词频最高的前 20 词兜底 ⇒ 20。经 window.__sgDiag 只读探针做单元级断言；默认态不含该哨兵。",
  },
  {
    slug: "it/summary-generator",
    clicks: ["var __s=window.__sgDiag.splitSentences('价格 3.14 元，涨幅明显。第二段内容也足够长用于验证。');document.getElementById('summaryResult').textContent='N547_N='+__s.length+':'+__s[0].text;"],
    expect: ["N547_N=2:价格 3.14 元，涨幅明显。"],
    ref: "IT-N547：旧分句器只把「句点后跟字母」当缩写，小数点后跟数字照切，`价格 3.14 元…` 被劈成「价格 3.」等 3 句；现句点后跟字母或数字都不切分，且换行/顿号不再作分句点 ⇒ 2 句、首句完整保留 3.14。回退后哨兵变 N547_N=3:价格 3. ⇒ 转红。默认态不含该哨兵。",
  },
  {
    slug: "it/team-name-generator",
    clicks: ["document.getElementById('seed').value='TB549';document.getElementById('style').value='passionate';document.getElementById('maxLen').value='40';document.getElementById('suffixMode').value='number';document.getElementById('count').value='6';generate();var __a=document.getElementById('output').innerHTML;generate();var __b=document.getElementById('output').innerHTML;document.getElementById('style').value='classical';generate();var __c=document.getElementById('output').innerHTML;var __rows=(__a.match(/code-row/g)||[]).length;var __names=__a.split('</div>').map(function(s){return s.replace(/<[^>]*>/g,'');}).filter(function(s){return s.length;});var __lenOK=__names.every(function(s){return s.length<=40;});var __numOK=__names.every(function(s){return /[0-9][0-9]$/.test(s);});document.getElementById('output').textContent='TN549='+(__a===__b?1:0)+(__a!==__c?1:0)+(__lenOK?1:0)+(__numOK?1:0)+':rows='+__rows;"],
    expect: ["TN549=1111:rows=6"],
    ref: "IT-N549：种子、风格、后缀类型三控件必须真的生效。四位分别验 ① 同种子两次 generate() 输出逐字相同（mulberry32 复现）；② 换风格后输出不同（风格词库生效）；③ 所有候选长度 ≤ 40；④ 数字后缀模式下每条都以两位数字结尾；再验条数=6。修复前全页无这些控件，__tnState/STYLES 不存在 ⇒ 哨兵不出现。默认态不含 TN549= 串。",
  },
  {
    slug: "it/team-name-generator",
    clicks: ["document.getElementById('seed').value='TB549B';document.getElementById('maxLen').value='10';document.getElementById('suffixMode').value='none';document.getElementById('count').value='8';generate();var __o=document.getElementById('output').innerHTML;var __names=__o.split('</div>').map(function(s){return s.replace(/<[^>]*>/g,'');}).filter(function(s){return s.length;});document.getElementById('output').textContent='TN549_LEN='+__names.length+'/'+(__names.every(function(s){return s.length<=10;})?1:0);"],
    expect: ["TN549_LEN=8/1"],
    ref: "IT-N549 最大长度：maxLen=10、无后缀、8 条，重试 16 次仍超长按上限截断 ⇒ 8 条全部 ≤10 字符。修复前无 maxLen 控件，候选常有 20+ 字符 ⇒ 该哨兵不出现。默认态不含该串。",
  },
  {
    slug: "it/team-name-generator",
    clicks: ["document.getElementById('seed').value='x';document.getElementById('style').value='classical';document.getElementById('domain').value='creative';document.getElementById('maxLen').value='6';document.getElementById('suffixMode').value='number';document.getElementById('count').value='5';generate();var __o=document.getElementById('output').innerHTML;var __names=__o.split('</div>').map(function(s){return s.replace(/<[^>]*>/g,'');}).filter(function(s){return s.length;});var __all=__names.length>0&&__names.every(function(s){return / [0-9][0-9]$/.test(s);});document.getElementById('output').textContent='TN549_SUFFIX='+(__all?1:0);"],
    expect: ["TN549_SUFFIX=1"],
    ref: "IT-N549：短 maxLen 时后缀须保留可见。种子 x、古风、创意、maxLen=6、数字后缀、5 条，修复后每条以「 两位数字」结尾（复现得 Jad 25 / Neo 19 / Moo 72 / Neo 28 / Cry 42），因截断时为后缀预留长度；修复前整串被截到 6 字符、数字后缀丢失（如 Jade W）⇒ 该哨兵为 0。默认态（无种子、maxLen=24）不命中 TN549_SUFFIX=。"
  },
  {
    slug: "it/screen-size",
    inputs: { width: "1920", height: "1080", diagonal: "24" },
    clicks: ["calc()"],
    expect: ["屏幕面积： 246.12 平方英寸", "1587.90 cm²"],
    ref: "IT-N545：公式框承诺「屏幕面积 = 物理宽 × 物理高」但结果区原先从未输出该量。独立复算：√(1920²+1080²)=2202.91 px ÷ 24 in = 91.79 PPI；physW=20.918 in、physH=11.766 in ⇒ 面积 246.12 in²，×6.4516 = 1587.90 cm²。默认 1080×2400/6.7 的面积为 16.80 in² / 108.38 cm² ⇒ 不命中。",
  },
  {
    slug: "it/screen-size",
    inputs: { width: "2560", height: "1440", diagonal: "27" },
    clicks: ["calc()"],
    expect: ["屏幕面积： 311.50 平方英寸"],
    ref: "IT-N545 第二组独立复算：√(2560²+1440²)=2937.66 px ÷ 27 = 108.80 PPI；physW=23.53 in、physH=13.24 in ⇒ 311.50 in²（2009.68 cm²）。与上例不同，防止结果被写成常量；默认态亦不命中。",
  },
  {
    slug: "it/text-replace",
    // 页面把 `doReplace` 挂在 `window` 上（非顶层 function 声明）⇒ 必须 clicks 显式驱动。
    inputs: { sourceText: "ab cd ab", findInput: "ab", replaceInput: "XY" },
    clicks: ["doReplace()"],
    expect: ["XY cd ab"],
    ref: "独立复算：非全局替换 ⇒ `ab cd ab` 只换第一处 `ab` ⇒ `XY cd ab`（第二处保留）。默认态源文本为空、直接 return，不命中。",
  },
  {
    slug: "it/text-similarity",
    inputs: { textA: "alpha beta", textB: "alpha gamma" },
    expect: ["0.6364", "编辑距离: 4"],
    ref: "独立复算：莱文斯坦距离 4、`len(A)=11` ⇒ 归一化 1−4/11=0.6364，与页面「63.64%（距离: 4）」自洽。默认态是更长示例文本，不命中。",
  },
  {
    // IT-N367 回归：compareMode=full（LCS 对齐）下 "abc" vs "xabc" 只多 1 个字符。
    slug: "it/text-similarity",
    inputs: { textA: "abc", textB: "xabc", compareMode: "full", tokenMode: "char" },
    expect: ["完整文本 · 差异合计 1 字符"],
    ref: "IT-N367：full 走 LCS 对齐，x→abc 的匹配使差异只剩插入的 1 个字符（旧实现 compareMode 只读不用，两个选项输出逐字节相同，这行摘要也不存在）。默认示例文本更长，不命中。",
  },
  {
    // IT-N367 回归：同一对文本切 compareMode=char（等长逐位）⇒ 差异合计 7。
    slug: "it/text-similarity",
    inputs: { textA: "abc", textB: "xabc", compareMode: "char", tokenMode: "char" },
    expect: ["逐字符 · 差异合计 7 字符"],
    ref: "IT-N367：char 走等长逐位对比 —— 3 位全部错位（A 侧 3 差异）+ B 侧多出的首/尾字符，合计 7；与 full 的 1 构成强判别，证明「比较模式」真的改变了对齐口径。默认 compareMode=full，不命中。",
  },
  {
    slug: "it/text-dedupe-sort",
    // 页面函数都包在闭包里（`applyOp` 非顶层声明）⇒ 只能从 clicks 进，不能直接 input 事件驱动。
    inputs: { input: "fig\napple\nfig\npear" },
    clicks: ["applyOp('dedupe')"],
    expect: ["fig apple pear"],
    ref: "独立复算：按整行去重保留首次出现顺序 ⇒ fig / apple / pear 三行（原 4 行、删 1 行）。默认示例是 banana/file10 那套，不命中。",
  },
  {
    slug: "it/text-dedupe-sort",
    // IT-N19 回归：首次操作建立快照后，用户再改输入 ⇒ 必须重建快照、按新数据出结果。
    inputs: { input: "a\na\nb" },
    clicks: ["applyOp('dedupe')", "document.getElementById('input').value='y\\nx'; applyOp('sortAsc')"],
    expect: ["x y"],
    ref: "独立复算：首轮去重 a,a,b ⇒ a/b；随后把输入改为 `y\\nx` 再升序 ⇒ `x\\ny`（不再是旧快照的 a/b）。修复前 applyOp 只用首轮快照，第二次点击仍输出 `a\\nb`，本 expect 不命中；默认态输入为空，不命中。",
  },
  {
    slug: "it/text-dedupe-sort",
    // IT-N20 回归：集合键与 Object.prototype 同名（__proto__）时不得被判为「已出现」。
    inputs: { input: "__proto__\na\n__proto__\nb" },
    clicks: ["applyOp('dedupe')"],
    expect: ["__proto__ a b"],
    ref: "独立复算：4 行按整行去重保留首次出现 ⇒ `__proto__` / `a` / `b`；修复前用普通 {} 做集合，`seen['__proto__']` 从 Object.prototype 继承后恒为真，首行即被丢弃 ⇒ 输出只剩 `a b`，本锚不命中（输入回显为 `__proto__ a __proto__ b`，不含该邻接串）。默认示例无该行。",
  },
  {
    slug: "it/text-cleaner",
    inputs: { "input-text": "  a  b \n\n\n  c \n" },
    expect: ["a b c"],
    ref: "独立复算：去首尾空格 + 合并连续空格 + 删空行 ⇒ `a b c`（3 个 token）。默认态源文本为空、直接 return，不命中。",
  },
  {
    slug: "it/slug-generator-advanced",
    inputs: { text: "Foo Bar Baz!!! 中文标题", sep: "_", maxLen: "40" },
    clicks: ["generate()"],
    expect: ["Foo_Bar_Baz"],
    ref: "独立复算：分隔符 `-`→`_` + 转小写 + 去首尾符号 ⇒ `foo_bar_baz_再截断`（页面同时把原文回显在 `←` 右侧，锚只取左侧真产物 `Foo_Bar_Baz`）。生成走按钮 onclick，必须 clicks。",
  },
  {
    slug: "it/shell-script-formatter",
    inputs: { input: "echo a\necho b" },
    clicks: ["doMinify()"],
    expect: ["echo a", "echo b"],
    ref: "独立复算：压缩保留换行，逐行去除首尾空白 ⇒ 输出两行 `echo a` 与 `echo b`（不再用 `; ` 合并，以免破坏 `&&`/`|`/`else`/`case`/heredoc 语法）。",
  },
  {
    slug: "it/shell-script-formatter",
    inputs: { input: "if true; then\necho $(date)\necho hi\nfi\nf() {\necho x\n}", indent: "2" },
    clicks: ["formatShell();var L=document.getElementById('output').textContent.split('\\n');var d=L.map(function(x){return (x.match(/^ */)||[''])[0].length;});document.getElementById('output').textContent='SHFMT221A='+d.join(',');"],
    expect: ["SHFMT221A=0,2,2,0,0,2,0"],
    ref: "第221批 IT-N186/N188：独立复算缩进序列。`if true; then` 开层(d=0)，`echo $(date)` 因行尾 ) 不再是 case 分支故与 `echo hi` 同为 1 层(2 空格)，`fi` 回 0；`f() {` 开层(d=0)、`echo x` 1 层(2 空格)、`}` 本行先减级回 0 ⇒ 0,2,2,0,0,2,0。修前宽泛正则 `.+\\)` 把命令替换当 case 分支、且 } 不先减级 ⇒ 0,2,4,2,2,4,4，必红。锚是把 output 每行前导空格数编码回 output（blob 会折叠空白，无法直接断言缩进），默认态输入为空 ⇒ SHFMT221A=0，不命中。",
  },
  {
    slug: "it/shell-script-formatter",
    inputs: { input: 'if [ "$x" = 1 ]\nthen\necho hi\nfi\ncat <<EOF\nhello\nEOF\necho "a <<EOF"\necho done', indent: "4" },
    clicks: ["formatShell();var pre=document.getElementById('output').textContent;var L=pre.split('\\n');var d=L.map(function(x){return (x.match(/^ */)||[''])[0].length;});doValidate();var post=document.getElementById('output').textContent;document.getElementById('output').textContent='SHFMT221B='+d.join(',')+'|OUTSAME='+(pre===post?'Y':'N');"],
    expect: ["SHFMT221B=0,0,4,0,0,0,0,0,0|OUTSAME=Y"],
    ref: "第221批 IT-N187/N189/N190：4 空格档独立复算。`if [ \"$x\" = 1 ]` 开层(d=0)、单独成行 `then` 本行减级后与 if 同列(d=0)且不再多开一层、`echo hi` 1 层(4 空格)、`fi` 回 0；heredoc 起始行按当前缩进输出(d=0)、body `hello`/`EOF` 原样、`echo \"a <<EOF\"` 剥离引号后不误触发 heredoc ⇒ 后续两行仍 d=0 ⇒ 0,0,4,0,0,0,0,0,0。`OUTSAME=Y` 锁 doValidate 绝不覆盖输出结果（修前 setOut(stats) ⇒ N）。默认态输入空 ⇒ SHFMT221B=0|OUTSAME=Y，不命中。",
  },
  {
    slug: "it/shell-script-formatter",
    inputs: { input: '  echo "a <<EOF"\n    echo next  ' },
    clicks: ["minifyShell();var L=document.getElementById('output').textContent.split('\\n');document.getElementById('output').textContent='SHFMT221C='+(L[1]==='echo next'?'TRIM':'RAW');"],
    expect: ["SHFMT221C=TRIM"],
    ref: "第221批 IT-N185 加固：压缩的 heredoc 探测改在剥离引号/注释后的代码上做。注入第 1 行是字符串字面量 `\"a <<EOF\"`，不含真实定界符；第 2 行仍应被逐行 trim 成 `echo next` ⇒ TRIM。修前按原始文本匹配 `<<EOF` 会误进 heredoc 态、第 2 行原样保留缩进 ⇒ RAW。默认态输入空 ⇒ RAW，不命中。",
  },
  {
    slug: "it/sql-escape",
    inputs: { input: "O'Brien" },
    clicks: ["esc()"],
    expect: ["O\\'Brien"],
    ref: "独立复算：MySQL 方言把单引号转义为 `\\'` ⇒ `O\\'Brien`（反斜杠转义后长度 9）。默认态输入为空直接 return，不命中。",
  },
  {
    slug: "it/text-to-binary",
    inputs: { input: "AB", encoding: "ascii" },
    expect: ["01000001 01000010"],
    ref: "独立复算：ASCII 模式下 A=65/B=66 补 8 位 ⇒ 空格分隔的两字节码。默认态示例是 Hello 的 UTF-8，不命中。",
  },
  {
    slug: "it/text-to-ascii",
    inputs: { txt: "AZ" },
    clicks: ["calcTool()"],
    expect: ["0x41"],
    ref: "独立复算：A 的十进制 65 转十六进制 ⇒ `0x41`、二进制 `01000001`（结果表走 dataGrid，非纯 innerHTML）。默认示例 `Hello, ToolBox!` 不含 A 且码点从 72 起，不命中。",
  },
  {
    slug: "it/case-converter",
    inputs: { inputText: "foo bar BAZ" },
    expect: ["fooBarBaz"],
    ref: "独立复算：驼峰命名按「词边界合并」（3 词）⇒ `fooBarBaz`；同批产物 `FOO BAR BAZ` / `FOO_BAR_BAZ` 与输入仅大小写不同、易误判回显，故选形态差异最大的驼峰串。默认示例 `Hello World Test Case` 走另一分支，不命中。",
  },
  {
    slug: "it/case-converter",
    // IT-N17 回归：按空白分词，仅每词首字符大写、保留词内大小写与撇号。
    inputs: { inputText: "don't O'Reilly myVar iPhone" },
    expect: ["Don't O'Reilly MyVar IPhone"],
    ref: "独立复算：4 个空白分词分别首字符大写、其余字符保持不变 ⇒ `Don't O'Reilly MyVar IPhone`；修复前 `\\b\\w`/`\\B\\w` 会把撇号后的 t 大写（`Don'T`）并把词内大写压低（`Myvar` / `Iphone`）。默认示例不含这些词，不命中。",
  },
  {
    slug: "it/url-encoder-advanced",
    inputs: { input: "a b&c=d/e?f" },
    clicks: ["enc()"],
    expect: ["a%20b%26c%3Dd%2Fe%3Ff"],
    ref: "独立复算：默认 `encodeURIComponent` 对空格 `& = / ?` 全部百分号编码 ⇒ 空 `%20`、`&`→`%26`、`=`→`%3D`、`/`→`%2F`、`?`→`%3F`。textarea 与 select 均无 oninput/onchange ⇒ 必须 clicks `enc()`。",
  },
  {
    slug: "it/list-converter",
    inputs: { input: "alpha\nbeta\ngamma", mode: "quote" },
    expect: ['"alpha", "beta", "gamma"'],
    ref: "独立复算：3 行按带引号格式用 `, ` 连接 ⇒ 双引号包裹的逗号串（产物在 textarea#output，非 result）。默认示例是水果词表，不命中。",
  },
  {
    slug: "it/list-converter",
    inputs: { input: "alpha\nbeta\ngamma", mode: "sql" },
    expect: ["('alpha', 'beta', 'gamma')"],
    ref: "独立复算：SQL IN 子句形态 ⇒ 单引号包裹、以 `, ` 连接、整体套圆括号。与 quote 模式同页同输入，靠 select 档位区分（判据⑧）。",
  },
  {
    slug: "it/list-converter",
    // IT-N30 回归：裸 CR（旧 Mac 换行）必须被切分，不能当成一整项。
    inputs: { input: "a\rb\nc", mode: "comma" },
    expect: ["a, b, c"],
    ref: "独立复算：输入 a\\rb\\nc，旧实现 split(/\\r?\\n/) 只按 \\n 切、裸 \\r 不识别 ⇒ 'a\\rb' 成一项；修复后 /\\r\\n|\\r|\\n/ 把 \\r 也切分 ⇒ 三项 a/b/c 以 ', ' 连接。默认示例为多行 \\n，不命中。",
  },
  {
    slug: "it/char-encoder",
    inputs: { input: "Hi~" },
    expect: ["SGl+"],
    ref: "独立复算：`Hi~` 的 Base64 ⇒ `SGl+`（同批 ASCII 码 72,105,126 / Unicode U+0048… / 二进制 01001000…，任一都行）。默认态 input 为空 ⇒ 各编码块只渲染标题不渲染值，不命中。",
  },
  {
    slug: "it/char-encoder",
    inputs: { input: "AZ" },
    expect: ["ASCII 码 65 90"],
    ref: "IT-N205 第225批：纯 ASCII 文本 ASCII 行按码点输出 `65 90`（空格分隔十进制），不再错误标「多字节序列」也不带逗号。默认态 input 为空 ⇒ ASCII 行无值，不命中。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=b&c" },
    clicks: ["enc()"],
    expect: ["a=3d"],
    ref: "独立复算：QP 编码把 `=` 转义为 `=3d` ⇒ `a=3db&c`（`&` 保留）。默认态输入为空直接 return，不命中。",
  },
  {
    slug: "it/html-entities",
    inputs: { encoderInput: "<b>Tom & Jerry</b>" },
    clicks: ["encodeAll()"],
    dumpIds: ["encoderOutput"],
    expect: ["&#60;&#98;&#62;"],
    ref: "独立复算：全字符编码把 `<` `b` `>` 转成 `&#60;&#98;&#62;`（`encodeText()` 只转 `&`/`<`/`>` 命名实体，产物是 `&lt;b&gt;Tom &amp; Jerry&lt;/b&gt;`，两者形态不同故可区分）。结果容器 `encoderOutput` 不在 harness 默认回写清单，须在用例里带 `dumpIds`。",
  },
  {
    slug: "it/html-entities",
    // IT-N33 回归：按码点生成十进制实体，emoji 不得只剩 UTF-16 高位。
    inputs: { encoderInput: "😀" },
    clicks: ["encodeAll()"],
    dumpIds: ["encoderOutput"],
    expect: ["&#128512;"],
    ref: "独立复算：😀 = U+1F600 ⇒ 十进制 128512；修复前 `charCodeAt(0)` 只取高位代理 ⇒ `&#55357;&#56832;`。默认示例不含 emoji，不命中。",
  },
  {
    slug: "it/html-entities",
    // IT-N33 回归：扩展 B 区汉字同样按码点编码。
    inputs: { encoderInput: "𠮷" },
    clicks: ["encodeAll()"],
    dumpIds: ["encoderOutput"],
    expect: ["&#134071;"],
    ref: "独立复算：扩展 B 区汉字 𠮷 = U+20BB7 ⇒ 十进制 134071；修复前 `charCodeAt(0)` 只取高位代理 ⇒ `&#55362;&#57271;`。默认示例不含该字，不命中。",
  },
  {
    slug: "it/html-entities",
    // IT-N33 回归：解码只替换已知实体，裸 < 与标签文本原样保留。
    inputs: { encoderInput: "a<b &amp; c" },
    clicks: ["decodeText()"],
    dumpIds: ["encoderOutput"],
    expect: ["a<b & c"],
    ref: "独立复算：`&amp;` 还原为 `&`、裸 `<` 不被当作标签 ⇒ `a<b & c`；修复前用 `div.innerHTML` 解析，裸 `<b` 被吞成 `a`。默认态编码示例为空，不命中。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "30", f_hour: "2" },
    expect: ["30 2 * * *"],
    ref: "独立复算：分钟/小时注入 30 / 2、日月月星期保持 `*` ⇒ 五段表达式 `30 2 * * *`。默认态是 `0 9 * * *`，不命中。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "99", f_hour: "9" },
    expect: ["分钟 字段超出范围或格式无效（允许 0-59"],
    ref: "回归 IT-N50·范围校验：分钟 99 越界（0-59）⇒ build() 必须显示错误且清空 cronOut。修复前 valid 忽略 min/max ⇒ 输出 `99 9 * * *`，错误串不命中。注入值刻意避开默认合法组合 `0 9`。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "*/0", f_hour: "9" },
    expect: ["分钟 字段超出范围或格式无效（允许 0-59"],
    ref: "回归 IT-N50·步长校验：*/0 步长为 0 非法 ⇒ build() 必须显示错误且不生成表达式。修复前正则 `^[*]|^[*]/\\d+$` 会放行 ⇒ 输出 `*/0 9 * * *`，错误串不命中；与上条分别覆盖「数值越界」和「步长=0」两条分支。",
  },
  {
    slug: "it/crontab-generator",
    // IT-N51 回归：中文说明不得重复量词且应自然。
    inputs: { f_min: "0", f_hour: "18", f_dow: "1-5" },
    expect: ["周 1-5 18:00 执行"],
    ref: "独立复算：分钟0/小时18/星期1-5 ⇒ 中文说明「周 1-5 18:00 执行」。修复前 f[2]==='*'&&f[4]!=='*' 走「每 星期 1-5 小时 18 分钟 0」分支，且默认 0 9 * * * 更会输出「每月 每月 每天 小时 9 分钟 0」重复量词。默认态为 0 9 * * *（输出「每天 09:00 执行」），本锚「周 1-5 18:00 执行」不命中默认态 ⇒ 非逃生。",
  },
  {
    slug: "it/morse-decode-advanced",
    inputs: { input: ".. --- .." },
    clicks: ["dec()"],
    expect: ["IOI"],
    ref: "独立复算：`..` `---` `..` 三段解码 ⇒ `IOI`。**入口是 `dec()` 不是 `decode()`**（后者不存在，errs 会直接报 not defined）。默认示例是 `... --- ...` ⇒ SOS，不命中；常量参考表里有单字母电码但不含连续三字母串。",
  },
  {
    slug: "it/normal-distribution",
    inputs: { mu: "0", sigma: "1", x0: "1.96" },
    clicks: ["calculate()"],
    expect: ["P(X ≤ 1.96) = 0.975"],
    ref: "独立复算：标准正态 Φ(1.96)=0.975（Z 分数公式 (x−μ)/σ 一致 ⇒ 分步区显示 Z = 1.96、Φ = 0.975）。**只锚这一条**：同页还有 α=0.05 双侧临界值 `1.96` 与「0.025 / 0.975」等常量，默认态同命中（判据⑤），锚须带 `P(X ≤ …)` 前缀才唯一。",
  },
  {
    slug: "it/video-bitrate",
    inputs: { w: "1920", h: "1080", fps: "30", dur: "60", br: "5" },
    expect: ["3433.2 MB"],
    ref: "独立复算：页面口径 `大小 = 码率(Mbps) × 时长(s) ÷ 8 ÷ 1.048576` ⇒ 5 Mbps、60 s ⇒ 2145.8 MB；同公式下 1080p 推荐码率 8 Mbps ⇒ **3433.2 MB**（锚取推荐码率档的那一支，避开默认示例的当前码率值）。数字走 dataGrid，非 innerHTML。",
  },
  {
    slug: "it/uniform-distribution",
    inputs: { a: "2", b: "8", x: "5" },
    clicks: ["calculate()"],
    expect: ["F(5) = 0.5"],
    ref: "独立复算：U(a=2,b=8) 的 CDF F(5) = (5−2)/(8−2) = 0.5，PDF 1/6 = 0.167、均值 5、方差 3 均与之自洽（分步区写 (5−2)/6）。默认态是 a=0,b=1 那套，不命中。",
  },
  {
    slug: "it/color-converter",
    inputs: { colorInput: "#1E90FF" },
    clicks: ["fromInput('#1E90FF')"],
    expect: ["#1E90FF"],
    ref: "独立复算：`#1E90FF`(DodgerBlue) 转 HEX 大写 `#1E90FF`、RGB `rgb(30, 144, 255)`、HSL `hsl(210, 100%, 56%)`。抠 `#1E90FF` 这一支而非 `rgb(30, 144, 255)`：默认态示例 `#667eea` 走的是另一色，两条锚都不命中。入口是 `fromInput(v)`（带参），`convert()` 不存在。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "400", p: "0.5", conf: "0.95" },
    clicks: ["calculate()"],
    expect: ["±0.049"],
    ref: "独立复算：SE = √[0.5×0.5/400] = 0.025，E = 1.96 × 0.025 = ±0.049（相对 4.90%）⇒ 95% CI [0.451, 0.549]。**注入值避开默认 n=100** —— 默认态 SE=0.05、E=±0.098，与注入态不同 ⇒ 双态成立；但同页 `z* = 1.96` / `α = 0.05` 是 α=0.05 双侧常量（判据⑤），不能单独当锚。",
  },
  {
    slug: "it/password-strength",
    inputs: { pwd: "Abcdef1!" },
    expect: ["良好"],
    ref: "独立复算：8 位、含大小写+数字+特殊符号、非键盘序列、非弱密码 ⇒ 评分 4/5 档「良好」（页面另给熵 52 bit 与破解耗时）。默认示例是更长的弱串，落另一档，不命中。",
  },
  {
    slug: "it/password-strength",
    inputs: { pwd: "abc123测试" },
    clicks: ["check()"],
    expect: ["在线破解（10亿次/秒）： 3 天"],
    ref: "IT-N536：在线档按 10 亿次/秒计算，48 bit 口令约 3 天；修复前基准是 2×10¹⁰ 次/秒，仅 3 小时。标签与除数必须一致。默认 ToolBox@2026 的耗时不同，注入失败回退后不命中。",
  },
  {
    slug: "it/password-strength",
    inputs: { pwd: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
    clicks: ["check()"],
    expect: ["熵判读（150 bits）： 极强"],
    ref: "IT-N537：32 个 a 的熵为 150 bit，公式承诺的 ≥120 极强判读须在结果区单列；修复前只按 6 项清单给「一般」，无任何熵判读输出。默认态不含该串。",
  },
  {
    slug: "it/password-strength",
    inputs: { pwd: "xxqwe123" },
    clicks: ["check()"],
    expect: ["⚠️ 包含键盘连续序列（如123、abc、qwe）"],
    ref: "IT-N538：中段 qwe 序列也要命中风险提示；修复前正则以 ^ 锚定只查开头，xxqwe123 被漏判。默认 ToolBox@2026 开头不在序列表，不含该提示 ⇒ 强判别。",
  },
  {
    slug: "it/whitespace",
    inputs: { source: "  a   b \n\n c \n" },
    clicks: [
      "document.getElementById('top_trim').checked=true;document.getElementById('top_blank').checked=true;document.getElementById('top_collapse').checked=true;document.getElementById('top_trail').checked=true;calcTool()",
    ],
    expect: ["处理后字符数 6"],
    ref: "独立复算：4 行输入（含 1 个空行）⇒ 删空行后 2 行、合并连续空格 + 去首尾空白 ⇒ 14 字符降到 6（`a b c\\n`）。**四个开关在桩内恒未勾 ⇒ 必须在 clicks 里逐个置 `checked=true` 再调 `calcTool()`**，否则与默认态完全一致（零差异）。",
  },
  {
    slug: "it/chmod-calculator",
    inputs: {},
    clicks: [
      "document.getElementById('r0').checked=true;document.getElementById('w0').checked=true;document.getElementById('x0').checked=true;document.getElementById('r1').checked=true;document.getElementById('x1').checked=true;document.getElementById('r2').checked=true;document.getElementById('w2').checked=true;document.getElementById('x2').checked=true;calc()",
    ],
    expect: ["chmod 757"],
    ref: "独立复算：用户 rwx=7、组 r-x=5、其他 rwx=7 ⇒ `757` 且符号位 `rwxr-xrwx`。checkbox 在桩内恒未勾（`inputs` 写 `checked` 不生效）⇒ 必须走这段 clicks；默认态（全勾 7）显示的是随机预设的另一组值，不命中。",
  },
  {
    slug: "it/regex-escape",
    inputs: { input: "a.b*c" },
    clicks: ["esc()"],
    expect: ["a\\.b\\*c"],
    ref: "独立复算：默认「通用 (JS)」风味下 `.` `*` 被转义、`/` 不转（勾「转义 /」另算）⇒ `a\\.b\\*c`。默认态输入为空直接 return，不命中。",
  },
  {
    slug: "it/regex-escape",
    // IT-N59 回归：verbose 风味只转义真正则元字符，= , ; : < > @ # & ~ 非元字符须原样保留。
    inputs: { input: "a=b,c.d", flavor: "verbose" },
    clicks: ["esc()"],
    expect: ["a=b,c\\.d"],
    ref: "独立复算：verbose 风味下 `=` `,` 不是 ECMAScript 正则元字符须原样保留，仅 `.` 被转义 ⇒ `a=b,c\\.d`。修复前 VERBOSE_META 含 `=,;:<>@#&~=` ⇒ 输出 `a\\=b\\,c\\.d`，不命中；贴进带 u/v 标志的 RegExp 会 SyntaxError。默认态输入为 Hello 预设串，不命中。expect 含被转义的 `.`（非纯输入回显）。",
  },
  {
    slug: "it/markdown-editor",
    // IT-N289 回归：预设「任务清单」的 `- [x]` / `- [ ]` 必须渲染成复选框，不得原样输出字面量。
    inputs: { mdInput: "- [x] done-item\n- [ ] todo-item" },
    clicks: ["var h=String(document.getElementById('mdPreview').innerHTML);document.getElementById('__tbProbe').textContent='TASKCHECK '+(h.indexOf('checkbox')>=0&&h.indexOf(' checked')>=0&&h.indexOf('task-list-item')>=0&&h.indexOf('[x]')<0&&h.indexOf('done-item')>=0?'OK':'BAD');"],
    expect: ["TASKCHECK OK"],
    ref: "探针校验解析产物：注入任务清单后预览须含禁用复选框（checked 勾已完成项、task-list-item 类）且不再有字面 `[x]`，文本 done-item 保留。修复前 parseLists 把 `[x] done-item` 整段当文本塞进 li ⇒ 无 checkbox、含 `[x]` ⇒ TASKCHECK BAD。默认态是页面样例（非任务清单）⇒ 不命中。",
  },
  {
    slug: "it/regex-escape",
    // IT-N21 回归：非法 `\\x` 转义必须原样保留，不能抛 RangeError 中断。
    inputs: { input: "\\x41\\xzz" },
    clicks: ["unesc()"],
    expect: ["A\\xzz"],
    ref: "独立复算：`\\x41` ⇒ `A`，紧随的 `\\xzz` 不是合法两位十六进制 ⇒ 原样保留，结果 `A\\xzz`；修复前 parseInt 得 NaN，String.fromCodePoint(NaN) 抛 RangeError，按钮无输出（输入回显 `\\x41\\xzz` 不含 `A\\xzz`）。默认态输入为空，不命中。",
  },
  {
    slug: "it/regex-escape",
    inputs: { input: "\\u{1F600}" },
    clicks: ["unesc()"],
    expect: ["😀"],
    ref: "独立复算：ES2015 码点转义 `\\u{1F600}` ⇒ U+1F600；修复前只认 4 位 `\\uXXXX`，会残留 `u{1F600}`。默认态输入为空，不命中。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "### 标题" },
    clicks: ["calcTool()"],
    expect: ["未发现明显风格问题"],
    ref: "独立复算：`### 标题` 属合法 ATX 标题、无其他风格项 ⇒ 问题 0 并落该结论串。默认示例含多个待整改项，结论不同，不命中。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "*斜体*\n**加粗**\n_斜体_" },
    clicks: ["calcTool()"],
    expect: ["✅ 未发现明显风格问题。"],
    ref: "IT-N527：成对强调语法 *斜体* / **加粗** 不是列表符号缺空格；修复前 /^\\s*[-*]\\S/ 会把两行判成问题。默认示例含待整改项，注入失败回退后不命中该结论。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "```js\n### 三级\n# 一级\n###### 六级\n```" },
    clicks: ["calcTool()"],
    expect: ["✅ 未发现明显风格问题。"],
    ref: "IT-N527：围栏代码块内的 # 行不参与标题层级与列表检查；修复前 H3→H6 会报跳级，结论串不出现。默认示例含待整改项。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "*斜体* 后面是说明" },
    clicks: ["calcTool()"],
    expect: ["✅ 未发现明显风格问题。"],
    ref: "IT-N527 复核失败重做：行首成对强调后接正文（*斜体* 后面是说明）是合法强调，旧实现整行须为强调才豁免、此处因后续正文被误报「列表符号后缺空格」；改为「行首以成对强调开头即豁免」。默认示例含待整改项不命中。回退 N527 源码会令此用例转红。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "```python\n~~~\ncode\n```" },
    clicks: ["calcTool()"],
    expect: ["✅ 未发现明显风格问题。"],
    ref: "IT-N527 复核失败重做：以 ```python 开围栏、内部出现 ~~~ 不应被当作闭围栏；旧实现任意围栏行都翻转 inFence，导致 ~~~ 提前闭围栏、末尾 ``` 被当成无语言新围栏报 MD040。新增按定界符类型+长度匹配开闭，跨类型围栏内内容不参与检查。默认示例含待整改项不命中。回退 N527 源码会令此用例转红。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "# T\n正文  \n- item" },
    clicks: ["calcTool()"],
    expect: ["第 2 行：行尾多余空格（MD009）"],
    ref: "IT-N526：MD009 行尾空格检查已实现；该描述仅在第二行确有尾随空格时出现，默认示例无行尾空格 ⇒ 强判别。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "# T\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" },
    clicks: ["calcTool()"],
    expect: ["行宽 90 超过 80 列（MD013）"],
    ref: "IT-N526：MD013 行宽检查已实现；90 字符行才触发该描述，默认示例无超长行 ⇒ 强判别。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "```\ncode\n```" },
    clicks: ["calcTool()"],
    expect: ["第 1 行：围栏代码块未标注语言（MD040）"],
    ref: "IT-N526：MD040 代码块语言检查已实现；无语言围栏才触发，默认示例无围栏 ⇒ 强判别。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "a\"b\\c\nd" },
    clicks: ["esc()"],
    expect: ["a\\\"b\\\\c\\nd"],
    ref: "转义产物非输入回显：引号→\\\"、反斜杠→\\\\、换行→\\n 逐一对应。默认示例不含该转义串。",
  },
  {
    slug: "it/java-escape",
    inputs: { input: "a\"b\\c", unicode: "1" },
    clicks: ["esc()"],
    expect: ["a\\\"b\\\\c"],
    ref: "Java 串内转义产物；unicode 档仅作形态区分，锚取与档位无关的基础转义部分。默认态不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "a\"b\\c", qtype: "s" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\\\\c\""],
    ref: "Python 字符串转义：整串用双引号包裹，内部双引号被转义 ⇒ 手算结果形如「双引号 + a\"b + 双引号」（**逐字符可手算复算**）。默认输入不同 ⇒ 不命中。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: "a\"b\\c" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\\\\c\""],
    ref: "Rust 字符串转义：整串用双引号包裹，内部双引号被转义 ⇒ 与 Python 那例输入、产物均相同，但走的是不同语言的实现路径（**手算复算**）。",
  },
  {
    slug: "it/css-escape",
    inputs: { input: "foo(bar)" },
    clicks: ["esc()"],
    expect: ["foo\\(bar\\)"],
    ref: "CSS.escape 风格逐字符加反斜杠，产物非原文回显。harness 内 escapeChar 报 undefined.code 属桩盲区（真机 DOM 事件源缺失），不影响产物串。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: "a\"b\\c" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\\\\c\""],
    ref: "JS 字符串转义：整串用双引号包裹、单引号**不转义** ⇒ 产物形如「双引号 + a'b + 双引号」（**手算复算**——双引号包围时单引号无需转义这一规则点）。",
  },
  {
    slug: "it/polybius-cipher",
    inputs: { input: "AB" },
    clicks: ["enc()"],
    expect: ["11 12"],
    ref: "A→11、B→12 的方格坐标拼接，随输入变化；默认示例对应其它坐标，不命中。",
  },
  {
    // IT-N346 回归：5×5 网格外字符（数字/标点）不得静默丢弃，必须回显跳过数量。
    slug: "it/polybius-cipher",
    inputs: { input: "AB1" },
    clicks: ["enc()"],
    expect: ["已跳过 1 个无法编码的字符（5×5 网格外）：1"],
    ref: "IT-N346：`1` 在 5×5 网格外，修复前 `findInGrid` 返回 -1 直接 continue、字符静默消失（AB1→`11 12`，往返得到 AB）；修复后结果区追加提示「已跳过 1 个…：1」。默认示例纯字母 ⇒ 无该提示，强判别。",
  },
  {
    slug: "it/xor-cipher",
    inputs: { input: "AB", key: "XY" },
    clicks: ["process()"],
    expect: ["191b"],
    ref: "0x19 0x1b 两字节异或密文（A^X=19、B^Y=1b）十六进制小写拼接。默认输入/密钥组合产物不同。",
  },
  {
    slug: "it/xor-cipher",
    // IT-N345 回归：hex 输入含非法字符，修复后 parseInput 抛错、catch 把错误写入 output 而非静默产出错误字节。
    inputs: { input: "1g", inFmt: "hex", key: "XY" },
    clicks: ["process()"],
    expect: ["包含非十六进制字符"],
    ref: "hex 通道输入 '1g' 含非十六进制字符 g，修复后抛「包含非十六进制字符」，不再静默转成错误字节；合法文本用例/默认态不命中该提示。",
  },
  {
    slug: "it/xor-cipher",
    // IT-N345 回归：hex 输入奇数长度，修复后应报「长度必须为偶数」而非静默截掉末位字节。
    inputs: { input: "1a2", inFmt: "hex", key: "XY" },
    clicks: ["process()"],
    expect: ["十六进制长度必须为偶数"],
    ref: "hex 通道输入 '1a2' 长度为奇数，修复后抛「十六进制长度必须为偶数」；合法用例不命中。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl https://a.test/x?a=1" },
    expect: ["URL： https://a.test/x?a=1"],
    ref: "URL 由命令行解析得出（方法 GET、无 Header、无 Body），非原文回显；默认示例指向另一域名，不命中。",
  },
  {
    slug: "it/ini-parser",
    inputs: { input: "[s]\na=1\n[t]\nb=2" },
    clicks: ["iniToJson()"],
    expect: ['{ "s": { "a": "1" }, "t": { "b": "2" } }'],
    ref: "两个 section 各自成对象、键值保持字符串形态；默认示例 section 名不同，不命中。",
  },
  {
    slug: "it/ini-parser",
    // IT-N23 回归：同名 [a] 必须合并已有键（此前重建空对象，x 被静默丢弃）。
    inputs: { input: "[a]\nx=1\n[a]\ny=2" },
    clicks: ["iniToJson()"],
    expect: ['{ "a": { "x": "1", "y": "2" } }'],
    ref: "独立复算：第 1 个 [a] 收 x=1，第 2 个同名节合并且不丢键 ⇒ {\"a\":{\"x\":\"1\",\"y\":\"2\"}}（修复前输出 { \"a\": { \"y\": \"2\" } }，x 丢失）。默认示例节名为 server/database，不命中。",
  },
  {
    slug: "it/ini-parser",
    inputs: { input: "[__proto__]\nx=1" },
    clicks: ["iniToJson()"],
    expect: ['"__proto__": { "x": "1" }'],
    ref: "__proto__ 作为节名：修复前 `result['__proto__'] = {}` 走原型 setter、不产生自有键，JSON.stringify 输出 `{}`；改为 Object.create(null) 后是普通自有键，JSON 保留 `\"__proto__\": { \"x\": \"1\" }`。默认示例无该节名。",
  },
  {
    slug: "it/ini-parser",
    // IT-N25 回归：JSON 数组 [..] 必须被识别为 JSON（而非 INI 节），美化后产出索引键值。
    inputs: { input: '["a","b"]' },
    clicks: ["doBeautify()"],
    expect: ["0 = a"],
    ref: "独立复算：输入 JSON 数组，doBeautify 用 JSON.parse 判别（非 startsWith('{')）⇒ 走 toIni 数组分支产出 '0 = a'/'1 = b'；修复前 startsWith('[') 误入 INI 分支、parseIni 把整行当节名、输出形如 '[{\"a\",\"b\":'，不含 '0 = a'。默认示例非 JSON 数组，不命中。",
  },
  {
    slug: "it/ini-parser",
    // IT-D40：无值键（布尔标志）须保留为空串值，不得整行丢弃。
    inputs: { input: "[s]\nflag\nx=1" },
    clicks: ["iniToJson()"],
    expect: ['"flag": ""'],
    ref: "INI 节中裸行 flag 是常见无值键（布尔标志），应解析为 flag 值为空串并与 x=1 共存。修复前 eq<0 直接 continue ⇒ 该行被丢弃，JSON 无 flag 键。默认示例各键均为 key=value，不命中。",
  },
  {
    slug: "it/properties-parser",
    inputs: { input: "a=1\nb=two" },
    clicks: ["propsToJson()"],
    expect: ['{ "a": "1", "b": "two" }'],
    ref: "properties 键值转 JSON 对象，值原样保留（含非数字串 two）；默认示例键/值组合不同。",
  },
  {
    slug: "it/properties-parser",
    // IT-D33：CRLF / 裸 CR 换行的 \r 不得残留在值尾。
    inputs: { input: "a=b\r\nc=d\r\n" },
    clicks: ["propsToJson()"],
    expect: ['"a": "b"', '"c": "d"'],
    ref: "CRLF 文本 a=b\\r\\nc=d\\r\\n 按行解析后值应为 b / d，不带残留 \\r。修复前只按 \\n 切行，值含 \\r ⇒ JSON 为 {\"a\":\"b\\r\",...}，锚 \"a\": \"b\" 不命中。默认示例为 LF 且键为 app.*，不命中。",
  },
  {
    slug: "it/properties-parser",
    inputs: { input: "__proto__=x" },
    clicks: ["propsToJson()"],
    expect: ['"__proto__": "x"'],
    ref: "键名恰为 `__proto__`：普通 `{}` 上赋字符串会走原型 setter 且被忽略，JSON 输出 `{}`（丢键）；Object.create(null) 后成为自有键 ⇒ `\"__proto__\": \"x\"`。默认示例键名是 app.* / db.*。",
  },
  {
    slug: "it/properties-parser",
    // IT-N11 回归：删除重复定义后，loadSample 必须走 propsToJson（输出 JSON），
    // 而非被覆盖的 doBeautify（输出 properties 文本）；同时成功提示 class 应为 ok 而非 err。
    clicks: ["loadSample();var __o=document.getElementById('output').textContent;document.getElementById('output').textContent='N11='+(/^\\s*\\{/.test(__o)?'JSON':'PROPS')+':'+(document.getElementById('err').className.indexOf('ok')>=0?'ok':'err');"],
    expect: ["N11=JSON:ok"],
    ref: "IT-N11 回归：loadSample 必须调 propsToJson（输出 JSON 且成功提示 class=ok），修复前重复定义使 loadSample 改为 doBeautify（输出 properties 文本）。原 expect 只写 '\"app.name\"'：页面 boot 自身就会调 loadSample()，纯默认态快照与注入态逐字相同（A===B 真盲区），被判别器判为逃生项。现改为在 clicks 里把「输出形态 + 成功态类名」写成唯一哨兵 N11=…，默认态不含该哨兵 ⇒ 有判别力；loadSample 若退化成 doBeautify，哨兵变 N11=PROPS:ok ⇒ 用例转红。",
  },
  {
    slug: "it/json-schema-validator",
    inputs: { data: '{"a":1}', schema: '{"type":"object","required":["b"]}' },
    clicks: ["validateJSON()"],
    expect: ["未通过： 缺少必填字段: root.b"],
    ref: "schema 要求必填 b 而数据缺 b ⇒ 必报缺失字段并点名路径；默认示例通过校验，结论相反。",
  },
  {
    slug: "it/email-normalizer",
    inputs: { input: "A.B+tag@Google.com" },
    expect: ["a.b+tag@google.com"],
    ref: "小写化后输出（保留标签部分、未去点）；默认示例地址不同形，不命中。",
  },
  {
    slug: "it/protobuf-parser",
    inputs: { input: "message M { optional string a = 1; }" },
    clicks: ["parseProto()"],
    expect: ['"name": "M"'],
    ref: "message 名与字段（type/name/number/标记位）由语法树解析得出；默认示例 message 名不同，不命中。",
  },
  {
    slug: "it/protobuf-parser",
    inputs: { input: "syntax = \"proto3\"; message Outer { oneof pick { map<string, string> opts = 1; } }" },
    clicks: ["parseProto()"],
    expect: ['"map<string, string>"', '"opts"'],
    ref: "IT-N276：oneof 内的 map<> 字段须被解析（type 为 map<string, string>、字段名 opts）。修复前 parseOneof 把 map 当普通类型、把 < 当字段名，抛「期望 ;」⇒ 两锚不命中；默认示例的 oneof 无 map ⇒ 不命中。",
  },
  {
    slug: "it/protobuf-parser",
    inputs: { input: "not proto at all" },
    clicks: ["doValidate()"],
    expect: ["校验失败", "无法识别的顶层内容"],
    ref: "IT-N277：任意非 .proto 文本校验须报失败。修复前主循环 `else { next(); }` 把未知顶层 token 静默跳过 ⇒ 空结果报「✅ 校验通过」；现未知顶层 name 抛「无法识别的顶层内容」。默认示例为合法 proto ⇒ 不命中。",
  },
  {
    slug: "it/phone-qr",
    inputs: { phone: "tel:+86 138 0013 8000" },
    clicks: ["generate();document.getElementById('__tbProbe').textContent='TELNW '+String(document.getElementById('output').innerHTML);"],
    expect: ["tel:+8613800138000"],
    ref: "IT-N274：已带 tel: 前缀的输入也须剥离全部空白（RFC 3966 不允许裸空格）。修复前只在非 tel: 分支 replace ⇒ 载荷保留空格；现先 replace 再补前缀。harness 无 qrcode 库，generate 走库加载失败分支但仍把处理后的 phone 写进 qr-text，可据此判别。",
  },
  {
    slug: "it/phone-qr",
    clicks: ["var ok=typeof downloadPNG==='function'&&/toDataURL\\(['\"]image\\/png/.test(String(downloadPNG))&&!!document.getElementById('__tbProbe');document.getElementById('__tbProbe').textContent='PNGD '+(ok?'OK':'BAD');"],
    expect: ["PNGD OK"],
    ref: "IT-N275：须有 downloadPNG() 且内部以 image/png 调用 canvas.toDataURL。修复前只有 copyResult（复制文本），无任何 PNG 导出 ⇒ PNGD BAD；默认态同样成立（检测函数存在性，与输入无关）。",
  },
  {
    slug: "it/math-evaluator",
    inputs: { expr: "2*(3+4)" },
    clicks: ["calc()"],
    expect: ["结果： 14"],
    ref: "先乘括号后乘除：2×7=14，验证运算符优先级与括号处理正确；默认表达式结果不同。",
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "苹果 香蕉 苹果 橙子 香蕉 苹果" },
    clicks: ["extractKeywords()"],
    expect: ["1 苹果 3 100.0%"],
    ref: "词频统计 + 相对频率（3/3=100.0%、2/3=66.7%），默认语料词表与频次均不同。",
  },
  {
    slug: "it/csv-to-html-table",
    inputs: { csvInput: "a,b\n1,2", sepSel: "," },
    expect: ["预览（2 行）"],
    ref: "行数统计随注入行数变化（默认示例行数不同 ⇒ 双态已排除同值巧合）。",
  },
  {
    slug: "it/regex-visualizer",
    inputs: { pattern: "^a(z+)" },
    clicks: ["render()"],
    expect: ["3 --z--> 4"],
    ref: "默认 pattern 为 `^a[0-9]+b$`（含 a 转移、无 z 转移）⇒ 锚取注入态独有的 z 转移边；`1 --a--> 2` 在默认态同命中，不可用。",
  },
  {
    // IT-N348 回归：正则内容进 innerHTML 前必须 HTML 转义，不能原样拼出可执行标签。
    slug: "it/regex-visualizer",
    inputs: { pattern: "a<b" },
    clicks: ["render()"],
    expect: ["S2: &lt; S3: b"],
    ref: "IT-N348：注入含 `<` 的 pattern `a<b`，状态标签里的 `<` 必须经 escapeHtml 变成 `&lt;`（裸 `<` 会被当作标签起始、在结果区不可见且存在注入风险）；默认 pattern `^a[0-9]+b$` 无 `<` 字符 ⇒ 该串仅注入态可见，强判别。",
  },
  {
    slug: "it/regex-visualizer",
    // IT-D28：必须输出真实 AST 层级（分支 + 分组 + 量词），旧实现只有线性状态链，无树节点 class。
    inputs: { pattern: "a(b|c)*" },
    clicks: ["render()"],
    expect: ["ast-alt", "2 路择一", "ast-group"],
    ref: "注入 `a(b|c)*`：递归下降解析应产出分支节点（2 路择一）、捕获分组节点与 * 量词节点，AST 树用 ast-alt/ast-group class 渲染；默认 pattern `^a[0-9]+b$` 无分组与分支 ⇒ 这些串仅注入态可见。",
  },
  {
    slug: "it/regex-visualizer",
    // IT-D28-b：分组类型细分（非捕获组、命名组、前后行断言）须在树上体现。
    inputs: { pattern: "(?:ab)+" },
    clicks: ["render()"],
    expect: ["非捕获分组"],
    ref: "注入 `(?:ab)+` 应解析为非捕获分组节点并渲染其类型标签；默认 pattern 只有一般字符类与锚点，无该标签 ⇒ 强判别。",
  },
  {
    slug: "it/markdown-to-html",
    inputs: { md: "## Hello World" },
    expect: ["Hello World"],
    ref: "二级标题渲染出的文本节点（注入串去掉 `##` 前缀后作为标题文本落进结果区）；默认示例标题词表不含该串。",
  },
  {
    slug: "it/markdown-to-html",
    // IT-N18 回归：链接 URL 里的双引号必须被编码/转义，不能闭合 href 造出 onmouseover 属性。
    inputs: { md: '[x](https://a/" onmouseover="alert(1))', showcode: "1" },
    clicks: ["calcTool()"],
    expect: ["https://a/%22%20onmouseover=%22alert(1"],
    ref: "独立复算：URL 中 `\"` 与空格先百分号编码（%22/%20）再属性转义 ⇒ href 内不再出现可闭合属性的裸引号（修复前原样拼进 href，生成 `<a href=\"https://a/\" onmouseover=\"alert(1\"`）。注入 showcode=1 让 HTML 代码面板可见该串；默认示例无此 URL，不命中。",
  },
  {
    slug: "it/markdown-to-html",
    // IT-N18 白名单：非 http/https/mailto 的相对路径之外的协议一律退回 #。
    inputs: { md: "[go](javascript:alert(1))", showcode: "1" },
    clicks: ["calcTool()"],
    expect: ['&lt;a href=&quot;#&quot;'],
    ref: "独立复算：`javascript:` 不在 http/https/mailto 白名单内且匹配协议前缀正则 ⇒ href 置 `#`，代码面板转义后为 `&lt;a href=&quot;#&quot;`（修复前只对字符串形式的 javascript: 前缀做判断、URL 仍原样落入 href）。默认示例为 https 链接，不命中。",
  },
  {
    slug: "it/markdown-to-html",
    // IT-N27 回归：![alt](url) 必须渲染为 <img>（此前输出字面 `!` + 链接）。
    inputs: { md: "![cat](https://x/y.png)", showcode: "1" },
    expect: ['&lt;img src=&quot;https://x/y.png&quot; alt=&quot;cat&quot; loading=&quot;lazy&quot;&gt;'],
    ref: "独立复算：图片规则先于链接规则 ⇒ `<img src=\"https://x/y.png\" alt=\"cat\" loading=\"lazy\">`；代码面板再转义一次 ⇒ 期望串里的 &lt;/&quot; 形态。修复前输出 `!<a href=…>cat</a>`，不含 `<img`。默认示例无图片语法，不命中。",
  },
  {
    slug: "it/markdown-to-html",
    // IT-N26 回归：#showcode 补选项后代码面板可用；#compact 压缩模式让代码面板单行（美化模式带换行）。
    inputs: { md: "# HeadA\n\n# HeadB", showcode: "1", compact: "compact" },
    expect: ["&lt;h1&gt;HeadA&lt;/h1&gt;&lt;h1&gt;HeadB&lt;/h1&gt;"],
    ref: "独立复算：两个 h1 拼接为 `<h1>HeadA</h1><h1>HeadB</h1>`；压缩模式下代码面板不插换行（美化模式为 `</h1>\\n<h1>`，collectStrings 归一后带空格，本 expect 不含空格 ⇒ 精确区分两种模式）。默认 md 是 `# 标题` 示例，不命中。",
  },
  {
    slug: "it/emoji-picker",
    inputs: { q: "cat" },
    expect: ["共 1 个 emoji（点击复制） 🐱"],
    ref: "关键词 cat 命中的唯一 emoji 及其计数与复制提示组成连续串；默认关键词命中集合不同，不命中。",
  },
  {
    slug: "it/html-minifier",
    inputs: { input: "<p>a</p>\n\n   <!-- x -->\n<p>b</p>" },
    checkIds: ["safeMode", "removeComments", "collapseWhitespace"],
    clicks: ["minify()"],
    expect: ["<p>a</p><p>b</p>", "50.0%"],
    ref: "页面三个复选框在 HTML 里均带 checked（真机默认全勾选），而 harness 桩的 checked 恒 false ⇒ 必须用 checkIds 显式还原真机默认态，否则 minify() 三个开关全假、走「不改动」分支，输出恒等于输入。输入 32 字符：移除 <!-- x --> 后 `</p>` 与 `<p>` 之间的空白被 `>\\s+<`→`><` 折叠 ⇒ 产物 <p>a</p><p>b</p>（16 字符），压缩率 (1−16/32)×100 = 50.0%。两项期望都来自压缩计算、非输入回显（输入归一后为 `<p>a</p> <!-- x --> <p>b</p>`，与产物不同）。python 独立复算一致。",
  },
  {
    slug: "it/html-minifier",
    inputs: { input: "<span>a</span>\n\n<span>b</span>" },
    checkIds: ["safeMode", "removeComments", "collapseWhitespace"],
    clicks: ["minify()"],
    expect: ["<span>a</span> <span>b</span>", "3.3%"],
    ref: "N2-B 回归（行内元素边界）：输入 30 字符，压缩后应为 29 字符 —— 两个 <span> 之间的换行+空行折叠为单个空格并保留 ⇒ 可见文本仍是 `a b`；修复前 `>\\s+<`→`><` 会把空格一起删掉压成 28 字符 `<span>a</span><span>b</span>`（文本粘连成 `ab`），压缩率 6.7%、且不命中本 expect。默认示例输入不含 span，默认态不命中。",
  },
  {
    slug: "it/html-minifier",
    inputs: { input: "<pre>a  b</pre>\n\n<span>c</span>" },
    checkIds: ["safeMode", "removeComments", "collapseWhitespace"],
    clicks: ["minify()"],
    expect: ["<pre>a  b</pre> <span>c</span>", "3.2%"],
    ref: "N2-B 回归（pre 保护 + 行内边界）：输入 31 字符（15 字符 `<pre>a  b</pre>` + 2 个换行 + 14 字符 span），<pre> 内双空格必须原样保留；<pre> 与 <span> 之间只保留一个空格 ⇒ 输出 30 字符，压缩率 (1−30/31)×100 = 3.2%。修复前安全模式的正则连 span 前的空格一起删掉（29 字符 / 6.5%），且不命中带空格的 expect。",
  },
  {
    slug: "it/python-formatter",
    inputs: { input: "def f():\n    return 1" },
    clicks: ["doValidate()"],
    expect: ["总行数: 2 def 数量: 1"],
    ref: "校验路径输出结构统计：两行函数定义 ⇒ 总行数 2、def 数量 1。压缩路径已改为保留物理行，不再把语句用 `; ` 串成一行。默认示例含更多 def/行数，不命中。",
  },
  {
    slug: "it/python-formatter",
    // IT-N300：缩进栈按真实层级输出 8/4/0，避免自带样例与小例不可编译。
    clicks: ["var nl=String.fromCharCode(10);document.getElementById('indent').value='4';document.getElementById('input').value='def f():'+nl+'    if x:'+nl+'        y=1'+nl+'    z=2'+nl+'w=3';doBeautify();var L=document.getElementById('output').textContent.replace(/ /g,'.').split(nl);var ok=L[1].indexOf('....if.x:')===0&&L[2].indexOf('........y=1')===0&&L[3].indexOf('....z=2')===0&&L[4]==='w=3';document.getElementById('__tbProbe').textContent='FMT300 '+(ok?'OK':'BAD:'+L.join('|'));"],
    inputs: { input: "def f():\n    if x:\n        y=1\n    z=2\nw=3", indent: "4" },
    expect: ["FMT300 OK"],
    ref: "IT-N300 独立复算：if 体 8 空格、def 体 4 空格、顶层 0；旧栈算法会给 4/2/2，Python 编译报 IndentationError。默认 fibonacci 示例不命中。"
  },
  {
    slug: "it/python-formatter",
    // IT-N301：注释独占一行，不能把后续代码拼到注释尾部吞掉。
    clicks: ["var nl=String.fromCharCode(10);document.getElementById('input').value='# comment'+nl+'x = 1'+nl+'print(x)';doMinify();var o=document.getElementById('output').textContent;document.getElementById('__tbProbe').textContent='MIN301 '+(o.indexOf('# comment;')<0&&o.indexOf(nl+'x = 1'+nl+'print(x)')>0?'OK':'BAD:'+o);"],
    inputs: { input: "# comment\nx = 1\nprint(x)", indent: "4" },
    expect: ["MIN301 OK"],
    ref: "IT-N301 注入注释+两行代码：压缩保留三条物理行，注释不得吞进赋值。旧实现输出 `# comment; x = 1; print(x)`，赋值与打印都成注释，不命中。"
  },
  {
    slug: "it/python-formatter",
    // IT-N302：冒号行后未缩进必须报错。
    clicks: ["var nl=String.fromCharCode(10);document.getElementById('input').value='def f():'+nl+'print(1)';doValidate();var e=document.getElementById('err').textContent;document.getElementById('__tbProbe').textContent='VAL302 '+(e.indexOf('未缩进')>=0&&e.indexOf('❌')===0?'OK':'BAD:'+e);"],
    inputs: { input: "def f():\nprint(1)", indent: "4" },
    expect: ["VAL302 OK"],
    ref: "IT-N302 注入 `def f():\\nprint(1)`：括号与三引号均平衡，但第 2 行未缩进必须报错；旧实现只看三引号闭合会报校验通过，不命中。"
  },
  {
    slug: "it/graphql-formatter",
    inputs: { input: "{a{b}}" },
    clicks: ["doMinify()"],
    expect: ["{ a{ b}}"],
    ref: "压缩形态（保留花括号间单空格、去掉换行）；默认示例的 query 文本不同，不命中。",
  },
  {
    slug: "it/html-nesting-checker",
    inputs: { html: "<div><p>a</div>" },
    clicks: ["check()"],
    expect: ["发现 1 个问题"],
    ref: "`<p>` 未被显式闭合即被 `</div>` 关闭 ⇒ 报 1 个问题并定位行号；默认示例无嵌套错误，不命中。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "AB" },
    clicks: ["convert()"],
    expect: ["Alpha Bravo"],
    ref: "字母逐个翻译为 NATO  Phonetic 单词（A→Alpha、B→Bravo），非原文回显；默认示例字母不同。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "X-ray" },
    checks: ["from"],
    clicks: ["convert()"],
    expect: ["X-ray → X"],
    ref: "IT-N529：反向查表需兼容 X-ray（去连字符后为 xray）。修复前 REV 只有 x-ray 键，X-ray 得 ?；结果区新增「原词 → 字母」明细，该串只在反查成功时出现。默认态为正向 Hello World，不命中。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "Hi! 123" },
    clicks: ["convert()"],
    expect: ["✅ 已转换 2 个字母"],
    ref: "IT-N530：正向计数只算 A–Z 字母。Hi! 123 只有 H、i 两个字母，修复前按去空白字符数得 6；默认 Hello World 为 10 个字母，不命中 2 个字母。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "Alpha Zzz" },
    checks: ["from"],
    clicks: ["convert()"],
    expect: ["✅ 已还原 1 个音标词"],
    ref: "IT-N530：反向计数只算成功还原项。Alpha→A、Zzz→?，成功 1 个；修复前 letters.length=2 会把 ? 计入。默认态正向不显示「已还原」。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "S3" },
    clicks: ["convert()"],
    expect: ["S=Sierra 3=Tree"],
    ref: "IT-N531：公式承诺的「字母=音标词」明细已在结果区渲染，且 3 按北约读法作 Tree。修复前 parts/all 从未渲染；默认 Hello World 明细为 H=Hotel…，不含该串。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "S3" },
    clicks: ["convert()"],
    expect: ["Sierra Tree"],
    ref: "IT-N531：复制框的数字按专用读法转换（3→Tree），修复前数字原样保留为 Sierra 3。默认 Hello World 不含 Sierra Tree ⇒ 强判别。",
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "Bad_Name", image: "nginx:latest", port: "80", replicas: "2" },
    clicks: ["calcTool()"],
    expect: ["⚠ 名称须符合 DNS-1123"],
    ref: "IT-N528：名称含大写/下划线违反 DNS-1123，须拒绝生成清单；修复前原样拼进 metadata.name，kubectl apply 必拒。默认 web 合法不出现该提示。",
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "nginx", port: "70000", replicas: "2" },
    clicks: ["calcTool()"],
    expect: ["⚠ 端口须为 1 ~ 65535 的整数"],
    ref: "IT-N528：端口 70000 超范围须拒绝；修复前 Math.floor(num)||80 只兜底 0/NaN，70000 原样写入 containerPort。默认 80 合法不出现该提示。",
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "my image:1", port: "80", replicas: "2" },
    clicks: ["calcTool()"],
    expect: ["⚠ 镜像名不能包含空白"],
    ref: "IT-N528：镜像引用含空白会破坏 YAML，须拒绝；修复前原样拼接。默认 nginx:latest 不含空白，不出现该提示。",
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "nginx:latest", port: "80.9", replicas: "2" },
    clicks: ["calcTool()"],
    expect: ["⚠ 端口须为整数（1~65535，80.9 不被允许）"],
    ref: "IT-N528：端口 80.9 非整数须拒绝（修复前 Math.floor 静默取整为 80 写进 containerPort，违反整数约束）。默认 80 合法不出现该提示。",
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "#invalid", port: "80", replicas: "2" },
    clicks: ["calcTool()"],
    expect: ["⚠ 镜像名不能以 # 开头（YAML 会当作注释）"],
    ref: "IT-N528：镜像 #invalid 以 # 开头会被 YAML 当作注释、值变 null，须拒绝。修复前原样拼成 `image: #invalid`。默认 nginx:latest 不出现该提示。",
  },
  {
    slug: "it/kubernetes-yaml-generator",
    inputs: { name: "web", image: "{}", port: "80", replicas: "2" },
    clicks: ["calcTool()"],
    expect: ["⚠ 镜像名不能是 YAML 关键字或空结构"],
    ref: "IT-N528：镜像 {} 会被 YAML 解析成空映射而非字符串，须拒绝。修复前原样拼成 `image: {}`。默认 nginx:latest 不出现该提示。",
  },
  {
    slug: "it/emoji-cheatsheet",
    inputs: { search: "🍺" },
    expect: ["共 1 个 emoji"],
    ref: "IT-N532：EMOJIS 表原有 8 组重复条目，🍺 重复两次；删除重复后搜索 🍺 只命中 1 条。修复前显示「共 2 个 emoji」，默认（空搜索）为 543 个，均不命中「共 1 个」。",
  },
  {
    slug: "it/uuencode",
    inputs: { input: "ABC" },
    clicks: ["enc()"],
    expect: ["begin 644 file.txt #04)# ` end"],
    ref: "uuencode 头（begin 644 文件名）＋ 编码体 ＋ 结束行 end，随输入体变化；默认语料长度不同。",
  },
  {
    // IT-N344 回归：RFC 未强制 begin 头，纯数据段（从邮件/工具截取）必须能解出内容。
    slug: "it/uuencode",
    inputs: { input: "&6F%P<&5R\n`\nend" },
    clicks: ["dec()"],
    expect: ["Zapper"],
    ref: "IT-N344：`&6F%P<&5R` 是 Zapper 的 uuencode 体（长度字节 `&`=6，两组 6-bit：22/38/5/48 → `6F%P`，28/6/21/50 → `<&5R`，手算可复算）。无 begin 头时修复前整段被跳过、输出空串；修复后按数据行解析出 Zapper。默认样例是编码后的其它文本不是合法数据段 ⇒ 不命中。",
  },
  {
    slug: "it/css-minify",
    inputs: { src: "a{color:red}" },
    expect: ["压缩后 0% 节省"],
    ref: "输入本已是最简形态 ⇒ 压缩字节数与原始相同、节省 0%，验证压缩率统计不虚报；默认示例压缩前后不同，不命中。",
  },
  {
    slug: "it/js-minify",
    inputs: { src: "var a=1;" },
    expect: ["压缩后 0% 节省"],
    ref: "无空白可去的最短输入 ⇒ 节省 0%，校验「压缩后字节 ≤ 原始字节」的统计口径；默认示例不命中。",
  },
  {
    slug: "it/js-obfuscator",
    inputs: { inputCode: "var s=\"a\\\"b\";" },
    clicks: ["window.ToolBox=window.ToolBox||{showToast(){},copy(){}};document.getElementById('optStringEncrypt').checked=true;obfuscate()"],
    expect: ["\\x22"],
    ref: "字符串加密必须把内嵌双引号写成 \\x22。旧实现条件 `ch < 128 && unescaped[i] !== quote` 直接跳过引号字符，产出 var s=\"\\x61\"\\x62\"; 这类引号提前闭合的非法源码（vm 报 Invalid or unexpected token），\\x22 不出现。默认示例代码的引号是分隔符而非内容，不含 \\x22 ⇒ 强判别。",
  },
  {
    slug: "it/regex-common",
    inputs: { txt: "abc", cat: "email", limit: "10" },
    clicks: ["calcTool()"],
    expect: ["无匹配"],
    ref: "`abc` 不匹配邮箱正则 ⇒ 匹配数 0 且结果区落「无匹配」；默认示例文本可命中，结论相反。",
  },
  {
    slug: "it/regex-common",
    // IT-D27：类别下拉必须实装 8 个 option；旧源码 <select id=cat></select> 无选项，
    // 页面任何选择都回退 email。探针读注入后的 select.innerHTML，锚 3 个非默认类别值。
    inputs: { txt: "13812345678", cat: "phone", limit: "5" },
    clicks: ["var s=document.getElementById('cat');var n=s.options?s.options.length:0;document.getElementById('__tbProbe').textContent='CATOPT '+n;"],
    expect: ["CATOPT 8"],
    ref: "IT-D27 修复后 #cat 必须含 8 个真实 option（phone/chinese/username 等）⇒ 探针 CATOPT 8；修复前下拉框为空 ⇒ CATOPT 0。探针串不来自默认态，判别力强。",
  },
  {
    slug: "it/regex-common",
    inputs: { txt: "x a@b.com y c@d.org z", cat: "email", limit: "8" },
    clicks: ["calcTool()"],
    expect: ["命中位置（字符偏移）：#1 [2-9] a@b.com、#2 [12-19] c@d.org"],
    ref: "S6 原文高亮：matchAll 逐段 <mark> 包裹 + 命中偏移明细。偏移由输入文本决定（x=0 空格=1 ⇒ a@b.com=[2-9]；c@d.org=[12-19]），默认样例（abc@example.com 13812345678…）不含该偏移组合 ⇒ 不命中。条目（『、』分隔 + 顺序号）与偏移都在被测输出中，判别力强。注意默认态样例也产「原文高亮（2 处）」字样，故不能以该标题单独作锚（铁律⑥或关系）。"
  },
  {
    slug: "it/vector-magnitude",
    inputs: {},
    clicks: ["document.getElementById('v0').value=6;document.getElementById('v1').value=8;document.getElementById('v2').value=0;calculate()"],
    expect: ["|v| = 10"],
    ref: "√(6²+8²)=10；输入框由 `build()` 运行期渲染（HTML 无字面 id）⇒ 必须 clicks 内按 id 赋值。默认值为 (3,4) ⇒ 5，不命中。",
  },
  {
    slug: "it/vector-dot-product",
    inputs: {},
    clicks: ["document.getElementById('a0').value=1;document.getElementById('a1').value=2;document.getElementById('a2').value=3;document.getElementById('b0').value=4;document.getElementById('b1').value=5;document.getElementById('b2').value=6;calculate()"],
    expect: ["A · B = 32"],
    ref: "dim 生产默认 3D（<select> selected=3D；harness 旧桩误取首选项 2D 曾致假期望 14）：A=(1,2,3)、B=(4,5,6) ⇒ 1×4+2×5+3×6=32（**逐项可手算复算**）。默认 A=(0,0,0)、B=(0,0,0) ⇒ 0，不命中。",
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "1", a1: "0", a2: "0", b0: "0", b1: "0", b2: "1" },
    clicks: ["calculate()"],
    expect: ["A × B = (0, -1, 0)"],
    ref: "i×k = −j ⇒ (0,−1,0)。默认示例 (1,0,0)×(0,1,0)=(0,0,1) 结论不同，不可用其做锚。",
  },
  {
    slug: "it/vector-cross-product",
    // IT-E1 空态：六分量全空时不得输出 (0, 0, 0)。
    inputs: { a0: "", a1: "", a2: "", b0: "", b1: "", b2: "" },
    clicks: ["calculate()"],
    expect: ["请输入向量 A 与 B"],
    ref: "空态口径：六分量全空 ⇒ 提示并 return，不给出零向量结论；修复前 getV 把空值 parseFloat 成 0，输出 `A × B = (0, 0, 0)`。默认示例 (1,2,3)×(4,5,6) 不含该提示。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.01", likelihood: "0.9", falsePositive: "0.05" },
    clicks: ["calculate()"],
    expect: ["P(H₁ | E) = 0.154 (15.38%)"],
    ref: "后验 = 0.9×0.01 / (0.9×0.01 + 0.05×0.99) = 0.009/0.059 ≈ 0.1538；默认示例先验不同，不命中。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "1", likelihood: "0.9", falsePositive: "0.05" },
    clicks: ["calculate()"],
    expect: ["先验优势 = ∞；BF = P(E|H₁)/P(E|¬H₁) = 0.9/0.05 = 18；后验优势 = ∞×18 = ∞"],
    ref: "IT-N374：先验 P(H₁)=1 ⇒ P(¬H₁)=0 ⇒ 先验优势 1/0 发散为 ∞。修复前 `fmt` 把 Infinity 一律写成「未定义」，卡片显示「未定义 → 未定义」、步骤 5「先验优势 = 未定义」。现在发散与未定义分开：优势比走 fmtOdds（∞），并补「边界说明」解释先验为 0/1 时优势比发散。expect 只依赖 prior=1 这一注入值（默认示例 prior=0.01，优势比 0.01 → 有限值）⇒ 非回显、修复前必红灯。",
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "2", x: "1" },
    clicks: ["calculate()"],
    expect: ["P(X ≤ 1) = 0.865"],
    ref: "指数分布 CDF F(1)=1−e⁻²=0.8647 ⇒ 0.865；默认参数不同，不命中。",
  },
  {
    slug: "it/barcode-ean",
    inputs: { data: "590123412345" },
    clicks: ["generate()"],
    expect: ["5901234123457"],
    ref: "EAN-12 补一位校验位（590123412345→7）⇒ 完整 13 位码；默认示例码不同。",
  },
  {
    // IT-N68 复核失败点：SHA 未算完时 copyAll/copyItem 会把占位符「—」当摘要复制走
    slug: "it/hash-multi",
    inputs: {},
    clicks: ["['al_md5','al_crc32','al_sha1','al_sha256'].forEach(function(k){document.getElementById(k).checked=true;});document.getElementById('input').value='n68probe';var __cap=null;var __o=ToolBox.copyText;ToolBox.copyText=function(t){__cap=t};calc();copyAll();ToolBox.copyText=__o;var __lines=String(__cap==null?'':__cap).split('\\n');var __dash=__lines.filter(function(l){return l.indexOf('—')!==-1}).length;var __total=lastHashPairs.length;document.getElementById('result').textContent='CAP lines='+__lines.length+' dash='+__dash+' total='+__total;"],
    dumpIds: ["result"],
    expect: ["CAP lines=2 dash=0 total=4"],
    ref: "IT-N68：SHA-1/256/512 走 crypto.subtle 异步，calc() 先渲染占位符「—」。修复前 copyAll() 把占位符一并复制（4~5 行、含「—」）；修复后只复制已就绪的 MD5 与 CRC32（2 行、零「—」）。total 为 4（勾选 MD5/CRC32/SHA-1/SHA-256），其中 SHA 两条在无 crypto.subtle 的桩里恒为占位符 ⇒ 可复制 2 条、占位符 0 条；三数同时成立才命中，任一条被破坏都不匹配，默认示例（无注入时 lastHashPairs 为空，copyAll 直接 return）不产生该串。",
  },
  {
    slug: "it/hash-multi",
    inputs: {},
    clicks: ["document.getElementById('al_md5').checked=true;document.getElementById('input').value='abc';calc()"],
    expect: ["MD5 900150983cd24fb0d6963f7d28e17f72"],
    ref: "MD5(`abc`) = 900150983cd24fb0d6963f7d28e17f72（RFC 1321 标准值）。算法是 checkbox 驱动的 ⇒ 桩内恒未勾，必须 clicks 内显式置位再 `calc()`。",
  },
  {
    slug: "it/hash-multi",
    inputs: { input: "中" },
    clicks: ["document.getElementById('al_md5').checked=true;calc()"],
    expect: ["MD5 aed1dfbc31703955e64806b799b67645"],
    ref: "UTF-8 字节口径：MD5('中'.encode('utf-8')) = aed1dfbc31703955e64806b799b67645（hashlib 核对）。旧实现按 charCodeAt(0x4E2D) 取字节 ⇒ f2f4599f…，不命中。默认输入 Hello ToolBox 不产生该值。",
  },
  {
    slug: "it/hash-multi",
    inputs: { input: "中" },
    clicks: ["document.getElementById('al_crc32').checked=true;calc()"],
    expect: ["CRC32 d5d15a8b"],
    ref: "CRC-32/ISO-HDLC（UTF-8 字节）核对：zlib.crc32('中'.encode('utf-8')) = 0xd5d15a8b。旧实现按 charCodeAt 取字节 ⇒ 结果不同，可判别 UTF-8 口径修复。",
  },
  {
    slug: "it/hash-multi",
    inputs: {},
    clicks: [
      "document.getElementById('input').value='中';document.getElementById('al_md5').checked=true;document.getElementById('al_crc32').checked=true;document.getElementById('al_sha1').checked=false;document.getElementById('al_sha256').checked=false;document.getElementById('al_sha512').checked=false;calc();ToolBox.copyText=function(s){document.getElementById('result').value=s;};copyAll()",
    ],
    expect: ["MD5: aed1dfbc31703955e64806b799b67645 CRC32: d5d15a8b"],
    ref: "「复制全部」修复：输出「算法名 + 哈希值」逐行文本，而非仅算法名。旧实现 querySelectorAll('div > div') 只取标签层 ⇒ 每行均为 `MD5: MD5`，不含哈希值。此处把剪贴板写入 result.value 以便采集。",
  },
  {
    slug: "it/wifi-qr",
    inputs: { ssid: "Net", pass: "pw" },
    clicks: ["generate()"],
    expect: ["WIFI:T:WPA;S:Net;P:pw;H:false;;"],
    ref: "Wi-Fi QR 的 TYPE/S/P/H 字段拼接（WPA、隐藏网络 false、末尾双分号）；默认示例 SSID/密码不同。",
  },
  {
    slug: "it/caa-record-generator",
    inputs: {},
    clicks: ["document.getElementById('ca_lets').checked=true;document.getElementById('domain').value='a.test';gen()"],
    expect: ['a.test CAA 0 issue "letsencrypt.org"'],
    ref: "勾选 letsencrypt 授权者 + 注入域名 ⇒ 输出标准 CAA 记录行（flags 0、issue 指令）。算法 checkbox 需 clicks 置位。",
  },
  {
    slug: "it/api-sign-generator",
    inputs: { secret: "s", params: "a=1", algo: "md5" },
    clicks: ["runSign()"],
    expect: ["签名结果： 9b211a5b174da8c32c0c361b39155597"],
    ref: "IT-N461 真 MD5：按 `参数串 + &secret=` 拼接待签串 a=1&secret=s，RFC 1321 MD5（node crypto 权威向量）= 9b211a5b174da8c32c0c361b39155597。旧实现拿 SHA-256 前 32 位冒充 MD5（得 14c37dbb…），与真 MD5 不符；默认参数组合产出不同密文。",
  },
  {
    slug: "it/api-sign-generator",
    // IT-N460：待签名串里的 payload 必须转义为文本，不得生成可执行 <img onerror> 节点。
    inputs: { secret: "s", params: "<img src=x onerror=alert(1)>=1", algo: "sha256" },
    expect: ["待签名串： &lt;img src=x onerror=alert(1)&gt;=1&secret=s"],
    ref: "注入 payload 参数 `<img src=x onerror=alert(1)>=1`：修复后 escHtml 把 < > 转成 &lt; &gt;，out.innerHTML 必含整段转义串 `&lt;img src=x onerror=alert(1)&gt;=1&secret=s` ⇒ 匹配。缺陷态（5640fa93c6^）原样拼接 ⇒ 裸 `<img onerror>` 入 DOM、无该转义串 ⇒ 不匹配。默认态 params 为正常键值、不含 payload ⇒ 判别明确。"
  },
  {
    slug: "it/api-sign-generator",
    // IT-N462：parseParams 必须把 a=1&b=2&c=3 解析成 3 个参数（预设用 & 分隔）。
    inputs: { secret: "s", params: "a=1&b=2&c=3", algo: "sha256" },
    clicks: ["var p=parseParams(),k=Object.keys(p);document.getElementById('__tbProbe').textContent='PP '+k.length+' '+(p.a||'')+'/'+(p.b||'')+'/'+(p.c||'');"],
    expect: ["PP 3 1/2/3"],
    ref: "注入 `a=1&b=2&c=3`：IT-N462 修复后 parseParams 按 [\\n&] 切分 ⇒ 3 键 a=1/b=2/c=3 ⇒ 探针 PP 3 1/2/3。旧实现只按换行切 ⇒ 1 键 a='1&b=2&c=3' ⇒ PP 1 1&b=2&c=3//，判别明确。默认态 params 正常键值、不执行探针。"
  },
  {
    slug: "it/http-status",
    inputs: { search: "zzz" },
    expect: ["No matching status code."],
    ref: "反向锚：不存在的状态码 ⇒ 列表区落英文空态提示（默认示例列表非空，必不命中）。",
  },
  {
    slug: "it/http-status",
    // IT-N101：数据规模与常用标准码补齐（旧态仅 32 条、缺 203/451 等）。
    clicks: ["var need=[103,203,205,300,303,305,411,412,414,416,417,418,421,425,426,428,431,451,506,507,508,510],miss=need.filter(function(c){return !statusCodes.some(function(s){return s.code===c;});});document.getElementById('__tbProbe').textContent='N101C '+(statusCodes.length>=50?'GE50':'LT50')+' '+(miss.length?miss.join(','):'ALL');"],
    expect: ["N101C GE50 ALL"],
    ref: "IT-N101：注入探针统计 statusCodes 条数与 22 个遗漏常用码。修复后 ≥50 条且 22 码齐全 ⇒ N101C GE50 ALL；旧态 32 条且缺全部 22 码 ⇒ N101C LT50 103,203,...，判别明确。默认态无探针，不产生该串。"
  },
  {
    slug: "it/http-status",
    // IT-N102：401 统一为「未认证」，detail 明确与 403 的权限差异。
    clicks: ["var s=statusCodes.find(function(x){return x.code===401;});document.getElementById('__tbProbe').textContent='N102A '+(s&&s.desc==='未认证'&&/403/.test(s.detail)?'OK':'BAD');"],
    expect: ["N102A OK"],
    ref: "IT-N102：401 卡片描述必须与概览一致为「未认证」且 detail 含 403 区分说明。旧态 desc=「未授权」且无 403 说明 ⇒ N102A BAD；修复后 ⇒ N102A OK。默认态无探针，不产生该串。"
  },
  {
    slug: "it/xxtea",
    inputs: { input: "ABC", key: "KY" },
    clicks: ["encrypt()"],
    expect: ["MaTt9vgiYH8="],
    ref: "XXTEA 加密后按 Base64 输出（固定密钥下结果确定）；默认示例明文/密钥不同，不命中。",
  },
  {
    slug: "it/xxtea",
    clicks: ["var __v=toUint32Array('X'.repeat(256)),__k=keyToLongs('myxxteakey'),__e=xxteaEncrypt(__v,__k),__d=xxteaDecrypt(bytesToLong(longToBytes(__e,false),false),__k),__o=document.getElementById('output');__o.value='N558_LEN='+longToBytes(__d,true).length;"],
    expect: ["N558_LEN=256"],
    ref: "IT-N558：长度字按完整 32 位读回，256 字节明文加密→解密往返后长度仍为 256。HEAD 版 longToBytes 只取低 8 位（256&255=0）⇒ N558_LEN=0，用例必红。",
  },
  {
    slug: "it/xxtea",
    clicks: ["var __a=xxteaEncrypt(toUint32Array('SAME PLAINTEXT'),keyToLongs('abcdefghijklmnopQRST')),__b=xxteaEncrypt(toUint32Array('SAME PLAINTEXT'),keyToLongs('abcdefghijklmnopXXXX')),__o=document.getElementById('output');__o.value='N559_DIFF='+(bytesToHex(longToBytes(__a,false))!==bytesToHex(longToBytes(__b,false)));"],
    expect: ["N559_DIFF=true"],
    ref: "IT-N559：前 16 字节相同、后 4 字节不同的两组 20 字节密钥必须产生不同密文（超长部分折叠进 128 位密钥）。HEAD 版第 17 字节起被静默丢弃 ⇒ N559_DIFF=false，用例必红。",
  },
  {
    slug: "it/mac-lookup",
    inputs: { macInput: "00:1A:2B:3C:4D:5E" },
    expect: ["点分： 001A.2B3C.4D5E"],
    ref: "MAC 的三种规范书写（冒号/连字符/点分）＋ OUI 与 NIC 拆分随输入变化；默认示例地址不同。",
  },
  {
    slug: "it/phone-parser",
    inputs: { phone: "13900139000", cc: "86" },
    clicks: ["calcTool()"],
    expect: ["国内格式：139 0013 9000"],
    ref: "E.164 与国内按位分组格式随号码变化：注入 13900139000 + 国家码 86 ⇒ E.164 +8613900139000、国内格式 139 0013 9000。原注入 13800138000 恰为页面默认号码，默认态同样输出「138 0013 8000」，属逃生项。",
  },
  {
    slug: "it/phone-parser",
    inputs: { phone: "07946095842", cc: "44" },
    clicks: ["calcTool()"],
    expect: ["07946 095842"],
    ref: "IT-N413：英国手机 07 开头须按手机分组（5-6）。输入 07946095842（含前导 0 共 11 位）⇒ 剥 trunk 后 7946095842（10 位、手机），国内格式应为 07946 095842。修复前按固话 3-4-4 显示 079 4609 5842。expect 命中手机分组串（默认 zh-CN 态不出现）⇒ 强判别；回退移动/固话分支后必红。"
  },
  {
    slug: "it/phone-parser",
    inputs: { phone: "0794609584", cc: "44" },
    clicks: ["calcTool()"],
    expect: ["⚠️ 英国 07 手机国内号码应为 10 位（含 trunk 0 共 11 位），当前 9 位"],
    ref: "IT-N413 复核重做（用例同步）：英国 07 手机国内须恰为 10 位（含 trunk 0 共 11 位）。0794609584 仅 10 位（含 0），剥 0 后 9 位 ⇒ 手机长度不足 ⇒ 应提示长度错误。短号警告不再笼统写 9–10 位，而点名手机需 10 位；expect 随页面文案同步更新（默认态不命中）⇒ 强判别。"
  },
  {
    slug: "it/country-code-lookup",
    inputs: { input: "CN" },
    expect: ["ISO 3： CHN"],
    ref: "ISO 3166-1 alpha-2 → alpha-3/区号/首都/货币映射（CN→CHN→+86→北京→CNY）。默认示例代码不同。",
  },
  {
    slug: "it/language-code-lookup",
    inputs: { input: "zh" },
    expect: ["ISO 639-3： zho"],
    ref: "ISO 639-1 → 639-3/语言名/语系/书写系统映射（zh→zho→Chinese→汉藏语系→Hans/Hant）。默认示例语言不同。",
  },
  {
    slug: "it/sms-qr",
    inputs: { phone: "13800138000", msg: "hi" },
    clicks: ["generate()"],
    expect: ["sms:13800138000?body=hi"],
    ref: "SMS 二维码内容格式 `sms:号码?body=短信`；默认号码/短信不同。",
  },
  {
    slug: "it/email-qr",
    inputs: { to: "a@b.com", subject: "S", body: "B" },
    clicks: ["generate()"],
    expect: ["mailto:a%40b.com?subject=S&amp;body=B"],
    ref: "mailto URI + 百分号编码收件箱（@→%40）＋ subject/body 查询参数；默认示例不同。注意产物区为 HTML 上下文，锚须写 `&amp;`。",
  },
  {
    slug: "it/location-qr",
    inputs: { lat: "31.2", lng: "121.4", label: "P" },
    clicks: ["generate()"],
    expect: ["geo:31.2,121.4?q=P"],
    ref: "Geo URI（纬度,经度 + 标签查询参数）；默认坐标/标签不同。",
  },
  {
    slug: "it/location-qr",
    inputs: { lat: "999", lng: "999", label: "" },
    clicks: ["generate()"],
    expect: ["⚠ 纬度需在 -90 ~ 90 之间"],
    ref: "IT-N522 锁定：纬度 999 超出范围须直接拒绝，不再静默生成 geo:999,999；默认样例 39.9/116.4 不出现该提示。与既有 NaN 补强用例互补（范围检查 vs 非数值检查）。",
  },
  {
    slug: "it/location-qr",
    inputs: { lat: "1oops", lng: "2", label: "" },
    clicks: ["generate()"],
    expect: ["⚠ 纬度 须为合法数字（不支持非法后缀）"],
    ref: "IT-N522 复核失败重做：纬度 1oops 含非法后缀，parseCoord 严格正则 /^-?\\d+(\\.\\d+)?$/ 拒绝，不再 parseFloat 截断为 1 静默生成 geo:1,2。默认样例 39.9/116.4 不出现该提示 ⇒ 强判别、零逃生。",
  },
  {
    slug: "it/sitemap-generator",
    inputs: { urls: "https://a.test\nhttps://b.test" },
    clicks: ["calcTool()"],
    expect: ["sitemap.xml 2 URL 数"],
    ref: "URL 条数统计随注入条数变化（默认示例条数不同 ⇒ 已排除同值巧合）。",
  },
  {
    slug: "it/phone-screen-sizes",
    inputs: { diag: "5", resw: "1080", resh: "1920" },
    clicks: ["calcTool()"],
    expect: ["2203 px 对角线像素"],
    ref: "√(1080²+1920²)=2202.9 ⇒ 2203 px；默认机型分辨率/尺寸组合不命中。",
  },
  {
    slug: "it/http-methods",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：搜索不存在的方法 ⇒ 过滤结果计数归零。默认列表非空 ⇒ 默认态必不命中。",
  },
  {
    slug: "it/http-headers",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：搜索不存在的头名 ⇒ 计数为 0；默认列表非空。",
  },
  {
    slug: "it/http-headers",
    clicks: ["var n=COMMANDS.map(function(c){return c.cmd;});var c={};COMMANDS.forEach(function(x){c[x.cat]=1;});document.getElementById('__tbProbe').textContent='HDRBAD RU='+(n.indexOf('Range-Unit')>=0?1:0)+' total='+COMMANDS.length+' cats='+Object.keys(c).length;"],
    expect: ["HDRBAD RU=0 total=97 cats=20"],
    ref: "IT-N104/N105：删除 RFC 中不存在的 Range-Unit 并补 7 个缓存/安全头 ⇒ 91→97 条、21→20 分类（「范围」分类消失）。旧表 RU=1 total=91 cats=21。探针仅 clicks 注入出现，默认态零命中。",
  },
  {
    slug: "it/http-headers",
    clicks: ["var n=COMMANDS.map(function(c){return c.cmd;});var need=['Cache-Control','ETag','Last-Modified','Expires','Strict-Transport-Security','Content-Security-Policy','Permissions-Policy'];var miss=need.filter(function(x){return n.indexOf(x)<0;});document.getElementById('__tbProbe').textContent='HDRNEED '+(miss.length===0?'OK':'BAD')+' '+need.length+'|'+miss.join(',');"],
    expect: ["HDRNEED OK 7|"],
    ref: "IT-N105：7 个最常查阅的缓存/安全响应头必须有独立词条（旧表全部缺失，ETag 仅作为 If-Match 参数出现）。显式 OK/BAD 标记杜绝前缀逃生——旧态输出 HDRNEED BAD 7|缺… 不命中。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/http-headers",
    clicks: ["var cc=COMMANDS.filter(function(c){return c.cat==='缓存';}).length,sc=COMMANDS.filter(function(c){return c.cat==='安全';}).length;document.getElementById('__tbProbe').textContent='HDRCAT cache='+cc+' sec='+sc;"],
    expect: ["HDRCAT cache=5 sec=8"],
    ref: "IT-N105：原「缓存」分类仅 Vary 一条、安全 5 条；补 4 个缓存头 + 3 个安全头后为 5/8。旧表 cache=1 sec=5。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/http-headers",
    inputs: { searchInput: "Cache-Control" },
    expect: ["共 1 项"],
    ref: "IT-N105 用户可见行为：搜索 Cache-Control 必须命中独立词条；旧表 0 条。默认态全表 97 项不产生「共 1 项」。",
  },
  {
    slug: "it/http-headers",
    inputs: { searchInput: "Range-Unit" },
    expect: ["共 0 项"],
    ref: "IT-N104 用户可见行为：搜索 RFC 中不存在的 Range-Unit 应零命中；旧表返回该编造条目 1 条。默认态全表不产生「共 0 项」。",
  },
  {
    slug: "it/http-cache",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：缓存头速查过滤空结果计数归零；默认列表非空。",
  },
  {
    slug: "it/http-cookies",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Cookie 速查过滤空结果计数归零；默认列表非空。",
  },
  {
    slug: "it/http-response-headers",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：响应头速查过滤空结果计数归零；默认列表非空。",
  },
  {
    slug: "it/http-response-headers",
    clicks: ["var n=COMMANDS.map(function(c){return c.cmd;});var bad=['Range','Want-Digest','Access-Control-Request-Method','Access-Control-Request-Headers'].filter(function(x){return n.indexOf(x)>=0;});document.getElementById('__tbProbe').textContent='RHREQ N='+bad.length+'|'+bad.join(',');"],
    expect: ["RHREQ N=0|"],
    ref: "IT-N459：请求头不得混入响应头速查表。旧 COMMANDS 含 Range / Want-Digest / Access-Control-Request-Method / Access-Control-Request-Headers 四项 ⇒ N=4；删除后 N=0。探针仅注入 clicks 时出现，默认态零命中。",
  },
  {
    slug: "it/http-response-headers",
    clicks: ["var n=COMMANDS.map(function(c){return c.cmd;});var d=[];n.forEach(function(x,i){if(n.indexOf(x)!==i&&d.indexOf(x)<0)d.push(x);});document.getElementById('__tbProbe').textContent='RHDUP N='+d.length+'|'+d.join(',');"],
    expect: ["RHDUP N=0|"],
    ref: "IT-N459：ETag / Last-Modified 各重复两条已去重，保留语法/参数更完整的第一条。旧表 ⇒ N=2|ETag,Last-Modified；现 N=0。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/http-response-headers",
    clicks: ["var c={};COMMANDS.forEach(function(x){c[x.cat]=1;});document.getElementById('__tbProbe').textContent='RHSTAT total='+COMMANDS.length+' cats='+Object.keys(c).length;"],
    expect: ["RHSTAT total=59 cats=14"],
    ref: "IT-N459：删 4 个请求头 + 2 个重复条目后总数 65→59，分类仍 14（CORS/内容/校验/缓存各类均有其他条目）。旧表 total=65 ⇒ 红。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/http-response-headers",
    inputs: { searchInput: "Access-Control-Request" },
    expect: ["共 0 项"],
    ref: "IT-N459 用户可见行为：预检请求头已从表中删除，搜索 Access-Control-Request 应零命中；旧表含两条 ⇒ 共 2 项。默认态（空搜索，59 项）不产生「共 0 项」。",
  },
  {
    slug: "it/affine-cipher",
    inputs: { input: "ABCD", a: "3", b: "1" },
    clicks: ["dec()"],
    expect: ["RAJS"],
    ref: "解密分支 `dec()` 走逆变换 a⁻¹(c−b)=9(c−1) mod 26：A→R、B→A、C→J、D⇒S（独立复算得 RAJS）。默认 a=5/b=8（产物 OJEZ），注入值必须避开默认。",
  },
  {
    slug: "it/basic-auth-generator",
    inputs: { f_user: "alice", f_pass: "pw123" },
    expect: ["Authorization: Basic YWxpY2U6cHcxMjM="],
    ref: "Basic 认证头 = `Basic ` + Base64(`alice:pw123`) = YWxpY2U6cHcxMjM=；裸 input event 即渲染，无需 clicks。默认示例用户名/口令不同。",
  },
  {
    slug: "it/basic-auth-generator",
    inputs: { f_user: "a:b", f_pass: "c" },
    clicks: ["generate();var t=String(document.getElementById('result').innerHTML||'');var tok=document.getElementById('tokenOut').value||'';document.getElementById('__tbProbe').textContent='AUTHCOLON '+(t.indexOf('用户名不能包含冒号')>=0&&tok.indexOf('YTpiOmM=')<0?'OK':'BAD');"],
    expect: ["AUTHCOLON OK"],
    ref: "IT-N208 第226批：用户名含冒号（a:b）须阻止生成并提示 RFC 7617，不得产出 a:b:c 的令牌 YTpiOmM=；旧实现直接 Base64('a:b:c') 生成该令牌。探针绑输入串，默认态用户名无冒号 ⇒ 零逃生。",
  },
  {
    slug: "it/char-encoder",
    inputs: { input: " …—" },
    expect: ["常用 HTML 实体 &nbsp;&hellip;&mdash;"],
    ref: "IT-N207 第226批：常见命名实体  = &nbsp;、… = &hellip;、— = &mdash;，标签改「常用 HTML 实体」。默认态 input 为空 ⇒ 该行无值，不命中。",
  },
  {
    slug: "it/date-duration",
    inputs: { d1: "2024-01-01", d2: "2024-03-15", inc: "1" },
    clicks: ["calcTool()"],
    expect: ["相差 74 天"],
    ref: "2024 闰年 1 月 31 + 2 月 29 + 15 − 1 = 74 天（页面按「不含结束当天」口径）。默认起止日不命中。",
  },
  {
    slug: "it/country-flag",
    inputs: { search: "zzz" },
    expect: ["共 0 个国家/地区"],
    ref: "反向锚：灌入不存在的国家名 ⇒ 计数归零；默认列表含上百个国家，默认态必不命中。与 http-* 五页同族。",
  },
  {
    slug: "it/calc-1",
    inputs: { sizeInput: "512", unitSelect: "KB" },
    expect: ["512,000 B"],
    ref: "512 KB = 512,000 B（十进制口径）；`unitSelect` 显式注入 KB 后才落该行。默认 1024 B ⇒ 1024 B，不命中。",
  },
  {
    slug: "it/calc-3",
    inputs: { hexInput: "#1E90FF" },
    expect: ["rgb(30, 144, 255)"],
    ref: "#1E90FF → rgb(30,144,255) → hsl(210,100%,56%)；默认色值不同形。裸 input event 即渲染。",
  },
  {
    slug: "it/calc-4",
    inputs: { pxInput: "48" },
    expect: ["font-size: 48px;"],
    ref: "48px 换算推出 em/rem/pt/% 四行（3 / 3 / 36pt / 300%）；锚取注入值对应的 px 行写法。默认 16px 不命中。",
  },
  {
    slug: "it/calc-5",
    inputs: { textInput: "hello world foo" },
    expect: ["15 字符 / 15 字节"],
    ref: "11 字符文本 + 3 空格 + 2 词 ⇒ 总长 15；统计区随输入重算（默认示例文本不同）。",
  },
  {
    slug: "it/calc-5",
    inputs: { textInput: "abc\n中文" },
    expect: ["6 字符 / 10 字节", "中文字符：2"],
    ref: "UTF-8 字节数：abc=3、换行 LF=1、中文=6，共 10；码点 6（Array.from），行 2，词 2，中文字符 2。默认空文本走「请输入文本」提示路径，不出现本串 ⇒ 判别有效。",
  },
  {
    slug: "it/calc-7",
    inputs: { jsonInput: '{"a":{"b":[1,2,3]}}', pathInput: "a.b" },
    expect: ["路径： $.a.b"],
    ref: "JSONPath 求值：`$.a.b` 命中数组 ⇒ 输出 `[ 1, 2, 3 ]`。**不可写 clicks 里的 `loadSample()`** —— 那会渲染默认样例（$.toolbox.name），默认态同命中 ⇒ 逃生项。",
  },
  {
    slug: "it/convert-11",
    inputs: { val: "255", from: "dec", to: "bin" },
    clicks: ["calc()"],
    expect: ["00000000.00000000.00000000.11111111"],
    ref: "十进制 255 → 点分二进制补齐 8 位×4 ⇒ 11111111；默认入参是 IP 地址 192.168.1.1（dot→bin），不命中。",
  },
  {
    slug: "it/convert-11",
    // IT-N483-a：非数字段（NaN）不得放行成 0.0.0.0。
    inputs: { val: "1.2.3.x", from: "dot", to: "dot" },
    clicks: ["calc()"],
    expect: ["IPv4 格式无效"],
    ref: "点分段 'x' 非数字，旧判据 on +x<0 / +x>255 对 NaN 均 false ⇒ 放行并 reduce 得 NaN ⇒ 输出 0.0.0.0。修复后每段须 /^\\d{1,3}$/ ⇒ 明确报 IPv4 格式无效。默认 192.168.1.1 合法不命中。",
  },
  {
    slug: "it/convert-11",
    // IT-N483-b：十进制 parseInt 截断（1e3→1）不得放行。
    inputs: { val: "1e3", from: "dec", to: "dot" },
    clicks: ["calc()"],
    expect: ["整数超出 IPv4 范围"],
    ref: "十进制 '1e3' 非纯数字，旧 parseInt(v,10)=1 ⇒ 输出 0.0.0.1。修复后先 /^\\d+$/ 校验 ⇒ 报整数超出 IPv4 范围。默认 192.168.1.1 走 dot 分支不命中。",
  },
  {
    slug: "it/convert-11",
    // IT-N483-c：小数 parseInt 截断（12.9→12）不得放行。
    inputs: { val: "12.9", from: "dec", to: "dot" },
    clicks: ["calc()"],
    expect: ["整数超出 IPv4 范围"],
    ref: "十进制 '12.9' 非整数，旧 parseInt=12 ⇒ 输出 0.0.0.12。修复后 /^\\d+$/ 拒绝 ⇒ 报整数超出 IPv4 范围。与 1e3 用例同分支但不同非法形态，分别锁住科学计数/小数两类截断。",
  },
  {
    slug: "it/playfair-cipher",
    inputs: { input: "HELLO", key: "KEY" },
    expect: ["DBNVMI"],
    ref: "Playfair 加密：`HELLO` 成对切分为 HE/LL/OX 后在 5×5 矩阵（KEY 去重后填充）中按行/列规则替换 ⇒ DBNVMI。默认示例明文/密钥不同，产物不命中。",
  },
  {
    slug: "it/playfair-cipher",
    // IT-N158 回归：解密模式能正确还原明文，验证 setMode('decrypt') 显式调用不破坏解密路径
    inputs: { input: "DBNVMI", key: "KEY" },
    clicks: ["setMode('decrypt')"],
    expect: ["HELXLO"],
    ref: "独立复算：HELLO 经 KEY 方阵加密得 DBNVMI；切到解密模式后 process() 用密文 DBNVMI 还原为 HELXLO（HE LL OX 拼接，X 为填充）。验证 setMode 默认值改动后解密路径正常；默认态 input 为 ATTACKATDAWN 不命中。",
  },
  {
    slug: "it/vigenere-visualizer",
    inputs: { input: "ABC", key: "KEY" },
    expect: ["KFA"],
    ref: "维吉尼亚加密：A+K、B+E、C+Y ⇒ KFA（逐字符位移）。默认明文/密钥组合产物不同。",
  },
  {
    slug: "it/html-escape",
    inputs: { batchInput: "<b>x</b>" },
    clicks: ["convert()"],
    expect: ["&lt;b&gt;x&lt;/b&gt;"],
    ref: "批量区把 `<b>x</b>` 实体化为 `&lt;b&gt;x&lt;/b&gt;`（结果区读的是 batchResult，主 result 在桩内仍为默认示例文本，勿锚它）。",
  },
  {
    slug: "it/css-properties",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 个属性"],
    ref: "反向锚：CSS 属性速查灌入不存在的关键词 ⇒ 计数归零（默认态列表上百条，必不命中）。与 http-* / country-flag 同族。",
  },
  {
    slug: "it/cpp-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：C++ 速查过滤无结果计数归零；默认列表非空。",
  },
  {
    slug: "it/cpp-cheatsheet",
    // IT-N484：重载示例必须可编译（去掉与单参重载歧义的默认参数），注解用 C++ 注释符。
    inputs: { searchInput: "重载" },
    clicks: ["var h=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent='CPPOVL '+(h.indexOf('int add(int a, int b) { return a + b; }')>=0&&h.indexOf('// 重载')>=0?'OK':'BAD');"],
    expect: ["CPPOVL OK"],
    ref: "注入搜索「重载」后探针读示例区：必须含无默认参数的双参 add 定义与 `// 重载` 注解。旧示例 `int add(int a, int b = 0)` + `int add(int a)` 调用 add(1) 编译歧义，且用 `--` 注解 ⇒ CPPOVL BAD。默认态不执行探针 ⇒ 判别明确。",
  },
  {
    slug: "it/ruby-cheatsheet",
    // IT-N486：Ruby 示例注解必须用 #，复制后可直接运行。
    inputs: { searchInput: "常量大写" },
    clicks: ["var h=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent='RUBYCMT '+(h.indexOf('PI = 3.14  # 常量大写')>=0&&h.indexOf('-- 常量大写')<0?'OK':'BAD');"],
    expect: ["RUBYCMT OK"],
    ref: "搜索「常量大写」后探针读示例区：必须是 `PI = 3.14  # 常量大写`（Ruby 注释符 #）。旧示例用 `-- 常量大写`，Ruby 无此注释符、复制运行报 NameError ⇒ RUBYCMT BAD。",
  },
  {
    slug: "it/cpp-cheatsheet",
    // IT-N486：C++ 示例注解必须用 //。
    inputs: { searchInput: "必须释放" },
    clicks: ["var h=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent='CPPCOMMENT '+(h.indexOf('delete[] arr;  // 必须释放')>=0&&h.indexOf('-- 必须释放')<0?'OK':'BAD');"],
    expect: ["CPPCOMMENT OK"],
    ref: "搜索「必须释放」后探针读示例区：必须是 `delete[] arr;  // 必须释放`。旧示例用 `-- 必须释放`，C++ 无此注释符 ⇒ CPPCOMMENT BAD。",
  },
  {
    slug: "it/typescript-cheatsheet",
    // IT-N486 + IT-N485：TS 注解用 //，且非空断言示例须带泛型参数否则 Element 无 value。
    inputs: { searchInput: "断言非空" },
    clicks: ["var h=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent='TSCMT '+(h.indexOf('// 断言非空')>=0&&h.indexOf('&lt;HTMLInputElement&gt;')>=0&&h.indexOf('-- 断言非空')<0?'OK':'BAD');"],
    expect: ["TSCMT OK"],
    ref: "搜索「断言非空」后探针读示例区：注解须为 `// 断言非空`，且 querySelector 带 `<HTMLInputElement>` 泛型（旧写法 el 为 Element，TS2339 类型错误）。旧示例用 `--` 且无泛型 ⇒ TSCMT BAD。",
  },
  {
    slug: "it/docker-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Docker 速查过滤无结果计数归零；默认列表非空。",
  },
  {
    slug: "it/hill-cipher",
    inputs: { input: "HELLO", key: "3,1,1,2" },
    clicks: ["enc()"],
    expect: ["ZPSHNI"],
    ref: "独立复算：密钥矩阵 [[3,1],[1,2]]（det=5，与 26 互素）作用于补齐后的 HELLOX ⇒ 逐对 (7,4)(11,11)(14,23) → ZP / SH / NI。明文与密钥均无 oninput ⇒ 必须 clicks `enc()`。",
  },
  {
    slug: "it/matrix-transpose",
    inputs: { rows: "1", cols: "2", a0: "7", a1: "3" },
    clicks: ["calculate()"],
    expect: ["转置矩阵 Aᵀ （2×1）： 7 3"],
    ref: "独立复算：1×2 矩阵 [7 3] 转置为 2×1 [[7],[3]]。同样必须注入运行期格子 `a0/a1`（rows/cols 只决定格子数量）。",
  },
  {
    slug: "it/invite-code-generator",
    inputs: { count: "3", len: "8" },
    clicks: [
      "document.getElementById('upper').checked=true;document.getElementById('num').checked=true;document.getElementById('prefix').checked=true;document.getElementById('prefixVal').value='ZZ';generate()",
    ],
    expect: ["ZZ-"],
    ref: "随机码只锚前缀拼接：勾选大写+数字+前缀后每条形如 `ZZ-L1ERDGP5`。四个开关在桩内恒未勾（`inputs` 写 checked 不生效）⇒ 必须在 clicks 里逐个置 true，否则 chars 为空直接 alert 返回、与默认态零差异。默认态（无 clicks）不产生任何输出。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "5" },
    clicks: ["calcTool()"],
    expect: ["生成的 IPv6 ULA（5 个）"],
    ref: "随机地址只锚计数：注入 cnt=5 ⇒ 条数字符串必为（5 个），默认 cnt=3 不命中。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "99" },
    clicks: ["calcTool()"],
    expect: ["生成的 IPv6 ULA（50 个）"],
    ref: "IT-N113 上限 50：注入 cnt=99 必须被 clamp 到 50 ⇒ 计数行为（50 个）；旧实现上限 20 得（20 个）不命中。默认 cnt=3 亦不命中。地址本体随机不可锚，只锚随 cnt 变的确定性计数行。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "7" },
    clicks: ["(function(){calcTool();var h=document.getElementById('result').innerHTML;var ok=h.indexOf('生成的 IPv6 ULA（7 个）')>=0&&h.indexOf('fd = 二进制 1111 1101，共 8 位，其中 L 位为 1；后接 40 位全局 ID + 16 位子网')>=0;document.getElementById('result').innerHTML=ok?'ULADOC-OK-7':'ULADOC-BAD';})()"],
    expect: ["ULADOC-OK-7"],
    ref: "IT-N115 说明纠错：注入 cnt=7 触发 calcTool，探针要求结果区同时含（7 个）计数与修正后的 8 位/40 位全局 ID/16 位子网说明；旧说明写「1111 1101 0」9 位且「48 位全局 ID」，不含该串 ⇒ 红。诊断串 ULADOC-OK-7 依赖修复后文案，默认态无该探针执行 ⇒ 零逃生。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "6" },
    clicks: ["(function(){var s=String(h);var ok=s.indexOf('getRandomValues')>=0;calcTool();var t=document.getElementById('result').innerHTML;var bad=t.indexOf('非安全伪随机')>=0;document.getElementById('result').innerHTML=(ok&&!bad&&t.indexOf('生成的 IPv6 ULA（6 个）')>=0)?'ULASAFE-OK-6':'ULASAFE-BAD';})()"],
    expect: ["ULASAFE-OK-6"],
    ref: "IT-N114 安全随机：注入 cnt=6，探针校验 h() 源码含 crypto.getRandomValues 且结果区无「非安全伪随机」告警（harness 全局有 webcrypto ⇒ 走安全路径）。旧实现 h() 纯 Math.random、源码无 getRandomValues ⇒ ULASAFE-BAD 红；默认态不执行探针 ⇒ 零逃生。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "4" },
    clicks: ["(function(){calcTool();var cap='';var _nw=navigator.clipboard;navigator.clipboard={writeText:function(t){cap=t;return Promise.resolve();}};try{copyUlaPrefixes({target:{textContent:''}});}catch(e){}navigator.clipboard=_nw;var n=cap.split('::/48').length-1;var ok=n===4&&cap.indexOf('fd')===0;document.getElementById('result').innerHTML=ok?'ULACOPY-OK-4':'ULACOPY-BAD-'+n;})()"],
    expect: ["ULACOPY-OK-4"],
    ref: "IT-N116 复制按钮：注入 cnt=4，探针替换 navigator.clipboard 后调用页面 copyUlaPrefixes，断言写入含 4 个 ::/48 前缀且以 fd 开头；旧实现无 copyUlaPrefixes 函数 ⇒ 抛错、cap 空、n=0 ⇒ ULACOPY-BAD-0 红。诊断串依赖新增复制函数，默认态无探针执行 ⇒ 零逃生。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "4" },
    clicks: ["(function(){calcTool();var rows=null,name='';globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(_s,n){name=n;}},matrix:{table:function(_sel,cfg){rows=cfg.rows;}}};try{__ipv6_ulaExport();}catch(e){}var ok=name==='ipv6-ula.csv'&&rows&&rows.length===4&&rows[0][0].indexOf('::/48')>0&&rows[0][1].indexOf('::')>0;document.getElementById('result').innerHTML=ok?'ULAEXP-OK-4':'ULAEXP-BAD';})()"],
    expect: ["ULAEXP-OK-4"],
    ref: "IT-N116 导出当前产物：注入 cnt=4，探针以 TBKit 桩调用 __ipv6_ulaExport，断言导出文件名 ipv6-ula.csv 且 matrix.table 收到 4 行本次生成的前缀/示例地址（非历史表）；旧实现导出走 __ipv6_ulaRender 历史快照、不写 matrix 表且文件名不同 ⇒ 红。诊断串依赖新导出逻辑，默认态无探针执行 ⇒ 零逃生。",
  },
  {
    slug: "it/mime-type",
    inputs: { search: "zzz" },
    expect: ["共 0 条"],
    ref: "反向锚：MIME 表搜索无命中计数归零；默认列表非空。",
  },
  {
    slug: "it/mime-type",
    inputs: { search: "  json  " },
    expect: ["共 2 条"],
    ref: "IT-N108：搜索词前后带空格必须先 trim 再过滤，命中 .json 与 .gltf(model/gltf+json) 共 2 条；旧实现未 trim ⇒ 共 0 条。默认态 84 条不命中。",
  },
  {
    slug: "it/mime-type",
    clicks: ["globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}}};var cap=null;var old=TBKit.matrix.table;TBKit.matrix.table=function(sel,cfg){cap={sel:sel,head:cfg.head,rows:cfg.rows};};__mime_typeDataTable();TBKit.matrix.table=old;document.getElementById('__tbProbe').textContent='MTTAB '+(cap?cap.sel+' '+cap.head.join('|')+' n='+cap.rows.length+' r0='+cap.rows[0].join('|'):'NONE');"],
    expect: ["MTTAB #mime_typeTable 扩展名|MIME 类型|分类 n=84 r0=.html|text/html|文本"],
    ref: "IT-N107：数据表必须渲染完整 MIME 清单（扩展名/MIME/分类 三列、84 行），不是搜索历史。旧源码无 __mime_typeDataTable 函数 ⇒ 探针 NONE。默认态无该串。",
  },
  {
    slug: "it/mime-type",
    clicks: ["globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}}};var calls=[];var oldT=TBKit.matrix.table,oldE=TBKit.util.exportTable;TBKit.matrix.table=function(sel,cfg){calls.push('TAB:'+sel+':'+cfg.head.join('/'));};TBKit.util.exportTable=function(sel,name){calls.push('EXP:'+sel+':'+name);};__mime_typeExport();TBKit.matrix.table=oldT;TBKit.util.exportTable=oldE;document.getElementById('__tbProbe').textContent='MTEXP '+calls.join(' ');"],
    expect: ["MTEXP TAB:#mime_typeTable:扩展名/MIME 类型/分类 EXP:#mime_typeTable:mime-type.csv"],
    ref: "IT-N107：导出前必须先重建 MIME 数据表再导出该表，调用序列固定为 TAB→EXP；旧实现直接导出历史表（无 TAB 或 TAB 头为时间/search/结果）⇒ 不命中。默认态无该串。",
  },
  {
    slug: "it/mime-type",
    clicks: ["globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}}};var n=0;var old=TBKit.matrix.table;TBKit.matrix.table=function(){n++;};__mime_typeRender(['search'],'结果',false);TBKit.matrix.table=old;document.getElementById('__tbProbe').textContent='MTHIST n='+n+'|';"],
    expect: ["MTHIST n=0|"],
    ref: "IT-N107：历史渲染路径不得再写 #mime_typeTable（历史已有独立 #mime_typeHist 页签）。旧实现写一次 ⇒ n=1，不命中；显式 n=0| 标记杜绝前缀逃生。探针仅 clicks 注入出现。",
  },
  {
    slug: "it/json-to-csv",
    inputs: { input: '[{"name":"Tom","age":3},{"name":"Ann","age":5}]' },
    clicks: ["toCSV()"],
    expect: ["已转换 2 行 × 2 列"],
    ref: "独立复算：两条 JSON 对象 ⇒ 表头 name,age + 2 行 ⇒ 2 行 × 2 列。转换走按钮 ⇒ 必须 clicks。",
  },
  {
    slug: "it/json-to-csv",
    inputs: { input: '[{"v":"=cmd|\' /C calc\'!A0"}]' },
    clicks: ["toCSV()", "document.getElementById('output').value=__jsonToCsvExportSafe"],
    expect: ["'=cmd|"],
    ref: "CSV 公式注入回归：导出路径必须给以 = 开头的单元格加单引号；页面原始输出为 \"=cmd|…（无前导单引号），故 expect 的 '=cmd| 只能由安全导出串命中。",
  },
  {
    slug: "it/json-to-csv",
    // IT-E3 空态：清空输入后不得只留效率工具栏的空结果。
    inputs: { input: "" },
    clicks: ["toCSV()"],
    expect: ["请输入非空 JSON 数组"],
    ref: "空态口径：输入为空 ⇒ 结果区提示；修复前空分支 `out.innerHTML=''`，既不报错也无提示，结果区只剩效率工具栏的「0 个参数」。默认示例已预填 JSON，不命中。",
  },
  {
    slug: "it/json-to-csv",
    // IT-N6 回归：非空但长度为 0 的数组 [] 不得保留上一次的有效 CSV。
    inputs: { input: "[]" },
    clicks: ["toCSV()"],
    expect: ["请输入非空 JSON 数组"],
    ref: "独立复算：输入 []（非空字符串、但 parsed 数组 length=0）⇒ 走 !data.length 分支，结果区提示且 output.value/__jsonToCsvExportSafe 必须被清空（修复前此分支不清空，旧 CSV 残留在 output 与导出串，复制/下载会误读旧数据）。默认样例是有效 JSON，不命中。",
  },
  {
    slug: "it/json-to-csv",
    // IT-N6 强回归：先生成有效 CSV，再注入非法 JSON（解析错误消息含 NaN/Infinity 字样），
    // 必须清空旧 CSV（output.value/__jsonToCsvExportSafe）且结果区改写「解析失败」，不得残留上一次的有效 CSV。
    inputs: { input: '[{"a":1,"b":2}]' },
    clicks: ["toCSV()", "document.getElementById('input').value='[NaN]'; toCSV()"],
    expect: ["解析失败"],
    ref: "独立复算：① 有效 JSON ⇒ output.value 写入 CSV、__jsonToCsvExportSafe 同步；② 注入非法 `[NaN]` ⇒ JSON.parse 抛 SyntaxError，其 message 含 `[NaN]` 子串命中 NaN 防御分支，修复前该分支提前 return 且不清空 output.value/__jsonToCsvExportSafe ⇒ 旧 CSV 残留（复制/下载会误读旧数据）；修复后该分支在 return 前清空两处并改写结果区为「解析失败：…」。expect 取「解析失败」——仅在修复态出现（旧实现该分支显示通用告警、不含「解析失败」），属强判别。",
  },
  {
    slug: "it/json-to-yaml",
    inputs: { input: '{"a":1}' },
    clicks: ["doYaml()"],
    expect: ["--- a: 1"],
    ref: "独立复算：`---` 文档分隔 + 一级键 `a: 1`。**不能用 `loadSample()`** —— 那会渲染默认样例，默认态同命中 ⇒ 逃生项。",
  },
  {
    slug: "it/json-to-yaml",
    // IT-N22 回归：空串 / 结构指示符开头 / 含冒号 / .inf / 日期类字符串必须加引号；指数补 .0。
    inputs: { input: '{"a":"","b":"- item","c":"a: b","d":".inf","e":1e21,"f":"2020-01-01"}' },
    clicks: ["doYaml()"],
    expect: ['b: "- item"', "e: 1.0e+21", 'a: ""'],
    ref: "独立复算：空串裸写会被 YAML 解析成 null、`- item` 会变成序列项、`a: b` 会拆成嵌套映射、`.inf` 会变成浮点、日期会被 1.1 解析器解析成日期 ⇒ 这些字符串都必须双引号；数字 `1e+21` 补 `.0` 才能被 YAML 1.1/1.2 都识别为浮点。修复前分别输出 `a: `、`b: - item`、`e: 1e+21` 等。默认样例键值不同，不含这些邻接串。",
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "XYZ", sep: "-" },
    clicks: ["enc()"],
    expect: ["24-25-26"],
    ref: "独立复算：A=1/Z=26 ⇒ `24-25-26`。**注入必须避开默认文本 `HELLO WORLD`** —— 它的编码结果以 `23-15-18-12-4` 结尾，与本例锚成子串关系，默认态会命中 ⇒ 逃生项。",
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "XYZ", sep: "-" },
    clicks: ["enc()"],
    copyCheck: { fn: "copyResult", expect: "24-25-26" },
    ref: "复制路径：enc() 后 copyResult(event) 写入剪贴板的内容必须等于结果区 `24-25-26`，且 then 回调不抛异常；旧实现 .then 内读隐式 event.target 会抛 TypeError 被 Promise 吞掉。",
  },
  {
    slug: "it/baudot-code",
    inputs: { input: "AB1" },
    clicks: ["enc()"],
    expect: ["00011 11001 11011 10111"],
    ref: "独立复算：查码表 A=00011、B=11001、数字 1=10111 ⇒ 五个位组以空格连接。表体（32 行码表）恒在默认态出现，锚只取产物行。",
  },
  {
    slug: "it/ascii-table",
    inputs: { search: "zzz" },
    expect: ["No matching entries."],
    ref: "反向锚：ASCII 速查搜索无命中 ⇒ 空态提示；默认列表非空。",
  },
  {
    slug: "it/ascii-tree-generator",
    inputs: { paths: "src/\na.js\nb.js\nlib/util.js" },
    clicks: ["build()"],
    expect: ["已生成 5 行目录树（4 个路径）"],
    ref: "独立复算：4 条路径按**换行**切分（非逗号）⇒ 5 行树、4 个路径。textarea 无 oninput ⇒ 必须 clicks `build()`。",
  },
  {
    slug: "it/area-code-lookup",
    inputs: { input: "212" },
    expect: ["New York (Manhattan)"],
    ref: "独立复算：NANP 区号库查 212 ⇒ New York (Manhattan)。库只覆盖北美编号计划，`021` 等中国区号查无 ⇒ 默认态不命中。",
  },
  {
    slug: "it/csv-validator",
    inputs: { src: "name,age\nTom,3", sep: "," },
    clicks: ["calcTool()"],
    expect: ["2 标准列数"],
    ref: "独立复算：两行 CSV（`name,age` / `Tom,3`）⇒ 标准列数 2、问题数 0。默认示例是 6 行中文表，不命中本锚。",
  },
  {
    slug: "it/csv-validator",
    // IT-N13 回归：RFC4180 引号内换行不得误报「引号未闭合」。
    inputs: { src: "name,note\nAlice,\"line1\nline2\"", sep: "," },
    clicks: ["calcTool()"],
    expect: ["2 行数", "✅ 未发现列数/引号问题。"],
    ref: "独立复算：引号内的换行属于字段内容 ⇒ 2 条记录、每条 2 列、无问题；修复前按 \\n 切行会把第 2 条记录切成两半并误报「引号未闭合」。默认示例有列数问题、无 ✅，不命中。",
  },
  {
    slug: "it/csv-validator",
    // IT-N13 回归：CRLF + 双引号转义 + 引号内 CRLF。
    inputs: { src: "a,b\r\n\"say \"\"hi\"\"\r\nbye\",2", sep: "," },
    clicks: ["calcTool()"],
    expect: ["2 行数", "✅ 未发现列数/引号问题。"],
    ref: "独立复算：`\"\"` 转为单个 `\"`、引号内 CRLF 不切记录 ⇒ 2 条记录、2 列、无问题；修复前引号内的 CRLF 会被当成行分隔并误报未闭合。默认示例不命中。",
  },
  {
    slug: "it/csv-validator",
    inputs: { src: "a,b\n\"open,2", sep: "," },
    clicks: ["calcTool()"],
    expect: ["第 2 行：引号未闭合"],
    ref: "独立复算：未闭合引号的记录起始于第 2 行 ⇒ 报「第 2 行：引号未闭合」；行号取记录起始物理行，多行字段场景不会错位。默认示例无此文案。",
  },
  {
    slug: "it/csv-validator",
    // IT-N24 回归：末尾空行不是一条记录，不得误报「列数 1（应为 2）」。
    inputs: { src: "a,b\n1,2\n\n", sep: "," },
    clicks: ["calcTool()"],
    expect: ["2 行数", "✅ 未发现列数/引号问题。"],
    ref: "独立复算：末尾空行不是记录 ⇒ 2 行、2 列、无问题；修复前空行被当成单列记录并报「列数 1（应为 2）」，且无 ✅ 结论。默认示例有列数问题，不命中。",
  },
  {
    slug: "it/csv-to-html-table",
    // IT-N25 回归：字段中间的 `\"` 是普通字符，不得开启引用段吞掉后续分隔符。
    inputs: { csvInput: 'a,b\n1,x"y,2' },
    clicks: ["calcTool()"],
    expect: ['<td>x"y</td>'],
    ref: "独立复算：RFC 4180 只允许字段起始处的双引号开启引用段 ⇒ 第二行是 3 个单元格 `1` / `x\"y` / `2`；修复前把中间双引号当引用起点，输出 `xy,2` 一个单元格（`<td>xy,2</td>`），本锚不命中。默认示例无引号。",
  },
  {
    slug: "it/csv-to-html-table",
    // IT-N304：文本 NaN/Infinity 不得改成破折号；空输入不得回退虚构样例。
    clicks: ["var nl=String.fromCharCode(10);var el=document.getElementById('csvInput');el.value='v'+nl+'NaN'+nl+'Infinity Labs'+nl+'NaNValue';calcTool();var h=document.getElementById('htmlOut').value;var p=document.getElementById('previewBox').innerHTML;var t=(h.indexOf('NaN')>0&&h.indexOf('Infinity Labs')>0&&h.indexOf('NaNValue')>0&&h.indexOf('—')<0&&p.indexOf('NaNValue')>0?'OK':'BAD');el.value='';calcTool();var e=document.getElementById('htmlOut').value;var ep=document.getElementById('previewBox').innerHTML;document.getElementById('__tbProbe').textContent='N304 '+t+' EMPTY '+(e===''&&ep.indexOf('输入为空')>=0?'OK':'BAD');"],
    inputs: { csvInput: "v\nNaN\nInfinity Labs\nNaNValue", sepSel: ",", withHeader: true },
    expect: ["N304 OK EMPTY OK"],
    ref: "IT-N304 合法文本含 NaN/Infinity 必须原样进入 HTML 与预览；随后清空输入必须清掉输出与示例，提示输入为空。旧实现两态均红；默认 Alice/Bob 样例不命中。"
  },
  {
    slug: "it/csv-to-yaml",
    // IT-N26 回归：引号内换行不得切成两条记录；表头含空格须加引号。
    inputs: { csv: 'first name,note\nTom,"line1\nline2"' },
    clicks: ["calcTool()"],
    expect: ['"first name": "Tom"', 'note: "line1\\nline2"'],
    ref: "独立复算：引号内换行属于字段内容，转成 YAML 双引号后为转义的 `\\n`，表头 `first name` 含空格须加引号 ⇒ `- \"first name\": \"Tom\"` / `note: \"line1\\nline2\"`；修复前按行切分把多行字段拆成两条记录，表头也裸写。默认 CSV 为 name/age/city，不命中。",
  },
  {
    slug: "it/csv-to-yaml",
    // IT-N361 回归：勾选「无表头」(top_1) 必须输出数组形态——预设「无表头」正是点这个方向。
    inputs: { csv: "Alice,30\nBob,25" },
    clicks: ["document.getElementById('top_1').checked=true; calcTool()"],
    expect: ['- ["Alice", "30"]', '- ["Bob", "25"]'],
    ref: "IT-N361：勾选「无表头」时每行输出为短横线 + 方括号数组（`- [\"Alice\", \"30\"]`）；未勾时首行是键名、输出 `- Alice: \"Bob\"` 这类键值对。旧预设把「无表头」置为 top_1='' 而 setValue 用 !!val，方向与实际相反。默认 CSV 为 name/age/city 且未勾选，不命中数组形态。",
  },
  {
    slug: "it/csv-to-yaml",
    // IT-N362 护栏：含 `:` 的表头必须加引号，否则 YAML 会被解析成键 a、值 b: 1。
    inputs: { csv: "a:b,c\n1,2" },
    clicks: ["calcTool()"],
    expect: ['"a:b": "1"'],
    ref: "IT-N362：表头 `a:b` 不是合法 YAML 裸键（会被读成键 `a`、值 `b: 1`），yamlKey() 须 JSON.stringify 成 `\"a:b\"`。同一行的 `y`/`on` 这类 YAML 保留字同理需加引号。默认表头 name/age/city 无冒号，不命中。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: "name,age\nTom,3" },
    expect: ['[{"column1":"name","column2":"age"}'],
    ref: "走「无表头」分支（桩内 checkbox 恒未勾，与真实用户未勾表头一致）⇒ 表头占位列名 column1/column2，产物是整条 JSON 数组。用整条数组做锚避免撞默认样例。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { jsonInput: '{"v":"=cmd|\' /C calc\'!A0"}' },
    clicks: ["jsonToCsv()", "document.getElementById('csvOutput').value=csvExportSafe"],
    expect: ["'=cmd|"],
    ref: "CSV 公式注入回归：JSON→CSV 的导出串必须给以 = 开头的单元格加单引号；原始预览为 \"=cmd|…（无前导单引号），expect 只能由安全导出串命中。",
  },
  {
    slug: "it/bluetooth-version",
    inputs: { v: "4.0", v2: "5.0" },
    clicks: ["calcTool()"],
    expect: ["Bluetooth 4.0 vs 5.0 版本对比"],
    ref: "独立复算：注入两侧版本 4.0 / 5.0 ⇒ 标题必为「Bluetooth 4.0 vs 5.0 版本对比」。默认态两侧同版（5.0/5.2 等）不命中。",
  },
  {
    slug: "it/bluetooth-version",
    // IT-N131：所有可选项必须有独立数据，4.0 不再静默回退 5.3。
    clicks: ["var sel=document.getElementById('v'),opts=[].map.call(sel.options,function(o){return o.value;}),need=['1.0','2.0','3.0','4.0','4.1'],missOpt=need.filter(function(v){return opts.indexOf(v)<0;}),missData=opts.filter(function(v){return !BT_INFO[v];});document.getElementById('__tbProbe').textContent='BTOPT '+(missOpt.length?missOpt.join(','):'ALL')+' '+(missData.length?missData.join(','):'ALL');"],
    expect: ["BTOPT ALL ALL"],
    ref: "IT-N131：下拉选项必须覆盖 1.0/2.0/3.0/4.0/4.1 且每个选项在 BT_INFO 中有独立数据。旧页只有 4.2~5.4 六项且 4.0 静默回退 5.3 ⇒ BTOPT 1.0,2.0,3.0,4.0,4.1 ALL（或未覆盖串）不命中；修复后 BTOPT ALL ALL。默认态无探针。",
  },
  {
    slug: "it/bluetooth-version",
    inputs: { v: "4.0", v2: "5.0" },
    clicks: ["calcTool();var s=String(document.getElementById('result').innerHTML||'');document.getElementById('__tbProbe').textContent='BT40 '+(/Bluetooth 4.0 vs 5.0/.test(s)?'T':'N')+(/BLE 低功耗引入/.test(s)?'D':'N');"],
    expect: ["BT40 TD"],
    ref: "IT-N131：注入 4.0/5.0 后结果区既要显示正确标题，也要显示 4.0 自身的「BLE 低功耗引入」。旧实现 4.0 未命中数据表 ⇒ 回退 5.3 的「连接子评级」⇒ BT40 TN；修复后 BT40 TD。默认态为 5.3/5.0，不产生该探针串。",
  },
  {
    slug: "it/emoji-cheatsheet",
    inputs: { search: "zzz" },
    expect: ["共 0 个 emoji"],
    ref: "反向锚：表情速查搜索无命中 ⇒ 空态计数归零，页面同时给出「未找到匹配的 emoji」。默认列表非空。",
  },
  {
    slug: "it/env-generator",
    inputs: { keyInput: "FOO", importText: "BAR=baz" },
    clicks: ["addVariable()"],
    expect: ["FOO 字符串"],
    ref: "独立复算：手动新增键 `FOO` ⇒ 变量表出现一行 `# Key ↕ Value ↕ Type ↕ 操作 / 1 FOO 字符串`。表格走 clicks 驱动，默认态无此行。",
  },
  {
    slug: "it/line-ending-converter",
    inputs: { leInput: "x\r\n\r\ny\n" },
    clicks: ["calcTool()"],
    expect: ["总换行 3"],
    ref: "独立复算：2 个 CRLF + 1 个 LF ⇒ 统计行 `CRLF 2 / LF 1 / CR 0 / 总换行 3`。**注入值必须避开默认的两行 CRLF**（`第一行\\r\\n第二行\\r\\n第三行` 也总换行 2，注入同值即逃生项，本例已踩并改 3）；锚也不能写 `LF 1`（会被 `CRLF 1` 误伤）。",
  },
  {
    slug: "it/line-ending-converter",
    // IT-N21 回归：空输入不得回退示例文本，输出/统计必须清空并提示。
    inputs: { leInput: "" },
    clicks: ["calcTool()"],
    expect: ["输入为空，请粘贴文本或点击“示例”加载示例文本。"],
    ref: "独立复算：输入为空 ⇒ calcTool 走空分支，leOutput 置空、统计不显示，只给提示；示例仅由「示例」按钮注入。修复前把局部 raw 换成 line1/line2/line3，输出与统计显示示例文本，本 expect 不命中。默认态 textarea 有默认文本，不命中。",
  },
  {
    slug: "it/line-ending-converter",
    // IT-N21 附带：清空后可视化区必须回到等待态。
    clicks: ["clearLe();document.getElementById('leInput').value='sentinel-text'"],
    expect: ["（等待输入）"],
    ref: "独立复算：clearLe 清空 leViz 并置为等待态；随后回填非空输入，避免兜底 calcTool 用空输入重写 viz（该空分支也会写等待态、会掩盖缺陷）。修复前 leViz 仍显示旧可视化内容，兜底也因输入非空而无法写出等待态，故必红。默认态不含「（等待输入）」。",
  },
  {
    slug: "it/js-formatter",
    inputs: { input: "function f(){\nreturn 1\n}" },
    clicks: ["doBeautify()"],
    expect: ["function f(){ return 1 }"],
    ref: "美化按原换行保留结构：函数体缩进 2 空格（默认缩进选项），语句不再被拼成一行。默认示例为 fibonacci，不命中该函数名组合。",
  },
  {
    slug: "it/js-formatter",
    // IT-N297：块注释内联保留，格式化结果仍是能算出 3 的合法 JS。
    clicks: ["var nl=String.fromCharCode(10);document.getElementById('input').value='const x = 1/*c*/+2'+nl+'console.log(x)';formatJs();var o=document.getElementById('output').textContent;var ok=false;try{ok=(new Function(o+'return x;')())===3;}catch(e){}document.getElementById('__tbProbe').textContent='ASI297 '+(ok?'OK':'BAD');"],
    inputs: { input: "const x = 1/*c*/+2\nconsole.log(x)", indent: "4" },
    expect: ["ASI297 OK"],
    ref: "IT-N297 独立执行：原码 x=3；格式化必须保留块注释原位与语句换行，编译后返回 3。旧实现把注释与 +2 拆到新行导致 SyntaxError；默认示例不命中。"
  },
  {
    slug: "it/js-formatter",
    // IT-N298：压缩结果自检失败时不得把坏代码留在输出框。
    clicks: ["document.getElementById('input').value='let a = ;';doMinify();var o=document.getElementById('output').textContent;var e=document.getElementById('err').textContent;document.getElementById('__tbProbe').textContent='MINI298 '+(o===''&&e.indexOf('自检失败')>=0?'OK':'BAD:'+o+'/'+e);"],
    inputs: { input: "let a = ;", indent: "4" },
    expect: ["MINI298 OK"],
    ref: "IT-N298 失败注入：非法源码压缩后必须清空 output 并报自检失败；旧实现输出 `let a =;` 还报压缩成功。默认示例不命中。"
  },
  {
    slug: "it/js-formatter",
    // IT-N299：校验必须调用 JS 引擎编译，而不是只数括号。
    clicks: ["document.getElementById('input').value='const 1 = 2;';doValidate();var e=document.getElementById('err').textContent;document.getElementById('__tbProbe').textContent='VAL299 '+(e.indexOf('语法错误')>=0&&e.indexOf('静态检查')<0?'OK':'BAD:'+e);"],
    inputs: { input: "const 1 = 2;", indent: "4" },
    expect: ["VAL299 OK"],
    ref: "IT-N299 括号 0/0 但语法非法 `const 1 = 2;`；新校验明确报语法错误，旧实现输出「已通过静态检查」不命中。"
  },
  {
    slug: "it/mysql-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：MySQL 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/url-parser",
    inputs: { urlInput: "https://a.io/p?x=1&y=2" },
    clicks: ["buildUrl()"],
    expect: ["域名 复制 a.io"],
    ref: "独立复算：解析结果逐行给出「协议/源/域名/端口/主机/路径/查询字符串/哈希/查询参数」，锚取域名行（`a.io`）。默认示例 URL 不同，不命中。",
  },
  {
    slug: "it/url-parser",
    inputs: { urlInput: "https://e.com/?__proto__=x&constructor=y" },
    clicks: ["parseUrl()"],
    expect: ["__proto__"],
    ref: "特殊键名：URLSearchParams 保留 `__proto__` / `constructor` 两个键，参数表逐行显示；默认示例只有 q/lang/page。数据容器由 `{}` 改为 `Object.create(null)` 后，JSON 导出也不再因原型继承丢键。",
  },
  {
    slug: "it/redis-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Redis 速查搜索无命中 ⇒ 计数归零；默认列表非空。与 `mysql-cheatsheet` 同族。",
  },
  {
    slug: "it/rest-api-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：REST API 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/rest-api-cheatsheet",
    clicks: ["var e=(COMMANDS||[]).filter(function(c){return c.cmd==='错误格式';})[0];var ok=false;try{var j=JSON.parse(e.syntax);ok=!!(j.error&&j.error.code&&j.error.message&&j.error.details)&&/problem\\+json/.test(e.params||'');}catch(x){}document.getElementById('__tbProbe').textContent='RACERR '+(ok?'OK':'BAD');"],
    expect: ["RACERR OK"],
    ref: "IT-N236：错误格式 syntax 必须是合法 JSON 且含 code/message/details，params 引 RFC 9457 problem+json。旧 syntax 写 `{\"error\":{\"code\",\"message\",\"details\"}}` 缺冒号与值，JSON.parse 抛错且 params 为空 ⇒ RACERR BAD。",
  },
  {
    slug: "it/postgresql-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：PostgreSQL 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/unicode-lookup",
    inputs: { search: "★" },
    clicks: ["showDetail()"],
    expect: ["U+2605"],
    ref: "独立复算：U+2605 就是 `★`（BLACK STAR），查表页把字符与其码点并列渲染。`showDetail()` 在桩内会因「无选中项」抛 `Invalid code point NaN`，但网格（`grid`）已由搜索框的 input 事件更新 ⇒ 不依赖该异常路径。默认列表里没有该条目。",
  },
  {
    slug: "it/unicode-lookup",
    inputs: { search: "U+2603" },
    clicks: ["render()"],
    expect: ["U+2603 · SNOWMAN"],
    ref: "IT-N554/N555：码点输入 U+2603 解析为 ☃ 一格并给出标准名称 SNOWMAN。HEAD 版拆成 U/+/2/6/0/3 六格、名称是 Code Point N ⇒ 不命中。",
  },
  {
    slug: "it/unicode-lookup",
    inputs: { search: "snowman" },
    clicks: ["render()"],
    expect: ["U+2603 · SNOWMAN"],
    ref: "IT-N554：按字符名 snowman 检索命中 U+2603（内置标准名称表）。HEAD 版把 7 个字母拆成 7 格 ⇒ 不命中。",
  },
  {
    slug: "it/unicode-lookup",
    inputs: { search: "U+AC00" },
    clicks: ["render()"],
    expect: ["HANGUL SYLLABLE GA"],
    ref: "IT-N555：U+AC00 是 Hangul 音节 가，标准名 HANGUL SYLLABLE GA（按 L/V/T 组合规则推导）。修复前显示 HANGUL SYLLABLE-AC00（拼码点而非合成名）。默认列表不含该条目。",
  },
  {
    slug: "it/unicode-lookup",
    inputs: { search: "U+3FFFF" },
    clicks: ["render()"],
    expect: ["名称未收录"],
    ref: "IT-N555：U+3FFFF 落在已分配 CJK 子区间（0x30000–0x3134F）之外、属未分配码位，应标「名称未收录」而非伪造 CJK UNIFIED IDEOGRAPH-3FFFF。修复前在 0x20000–0x3FFFF 宽区间里直接套用 CJK 命名。默认列表不含该码位。",
  },
  {
    slug: "it/username-generator",
    inputs: { style: "fun", maxLen: "20" },
    clicks: ["generate()"],
    expect: ["风格：趣味｜词库：14 词｜上限：20 字符"],
    ref: "IT-N557：风格下拉真的影响生成配置（趣味档 14 词词库 + 上限 20）。HEAD 版无 style 控件、无配置摘要 ⇒ 不命中。",
  },
  {
    slug: "it/username-generator",
    inputs: { style: "short", maxLen: "20" },
    clicks: ["generate()"],
    expect: ["风格：简短｜词库：16 词｜上限：10 字符"],
    ref: "IT-N557：简短档把上限压到 min(20,10)=10 并切到 16 词短词库，证明风格不只是回显。默认态经典档不含该串。",
  },
  {
    slug: "it/tmux-cheatsheet",
    inputs: { searchInput: "kill-session" },
    clicks: ["calcTool()"],
    expect: ["共 1 项\ntmux kill-session 关闭会话 分类： 会话 语法： tmux kill-session -t name 参数： -a 关闭除 -t 指定会话外的全部会话"],
    ref: "IT-N553：搜索 kill-session 后只剩 1 项，明细里的参数必须是带 -t 的新口径。⚠ 铁律⑤：默认态渲染全表也含 example 原文，单锚命令串会成为逃生项 ⇒ 用「共 1 项 + 条目明细」的组合串做 A/B 强判别；HEAD 版参数仍是「-a 除指定外全关」且不命中。",
  },
  {
    slug: "it/vim-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Vim 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/robots-txt-generator",
    inputs: { sitemap: "https://a.io/sitemap.xml" },
    clicks: ["addRule()", "render()"],
    expect: ["Sitemap: https://a.io/sitemap.xml"],
    ref: "独立复算：填 Sitemap 后 `render()` 把该行并进预览（`addRule()` 先把默认规则行补进来，故预览里同时含默认 UA/Disallow 行）。锚取注入的 sitemap 行，默认态不含。",
  },
  {
    slug: "it/go-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Go 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/go-cheatsheet",
    clicks: ["(function(){var bad=0;COMMANDS.forEach(function(c){var ex=c.example||'';if(/--\\s/.test(ex))bad++;ex.split('\\n').forEach(function(ln){var t=ln.trim();if(/\\{\\s*\\.\\.\\.\\s*\\}/.test(t)||/:\\s*\\.\\.\\.\\s*$/.test(t)||/\\.\\.\\.\\s*;/.test(t))bad++;});if(/for\\s+\\w+\\s*,\\s*\\w+\\s*:=\\s*range[^{]*\\{\\s*\\}/.test(ex))bad++;});document.getElementById('__tbProbe').innerHTML='GOSYNTAX '+(bad===0?'OK':'BAD'+bad);})()"],
    expect: ["GOSYNTAX OK"],
    ref: "IT-N244/N245 静态 Go 规则守卫：遍历 30 条 COMMANDS.example，统计非法 `--` 注释、裸 `...` 占位（`{...}`/`case: ...`/`...;`）、未使用变量空循环体（for k,v := range {}），全清零 ⇒ GOSYNTAX OK。旧源码 5 处 `--` + 8 处裸 `...` + 2 处空体 ⇒ BAD15 红。合法 `...T`/`[...]T`/`./...` 不在规则内、保留。探针只在 clicks 执行，默认态无该串 ⇒ 零逃生。",
  },
  {
    slug: "it/go-cheatsheet",
    clicks: ["(function(){var g=function(cmd){var c=COMMANDS.find(function(x){return x.cmd===cmd;});return c?c.example:'';};var ok=g('defer').indexOf('// \\u5148\\u8f93\\u51fa 2')>=0&&g('switch').indexOf('// \\u65e0\\u8868\\u8fbe\\u5f0f')>=0&&g('map').indexOf('fmt.Println(k, v)')>=0&&g('select').indexOf('no case ready')>=0&&g('\\u5b57\\u7b26\\u4e32').indexOf('i \\u662f\\u5b57\\u8282\\u7d22\\u5f15')>=0&&g('\\u6307\\u9488').indexOf('fmt.Println(x) // 2')>=0;document.getElementById('__tbProbe').innerHTML='GOFIX '+(ok?'OK':'BAD');})()"],
    expect: ["GOFIX OK"],
    ref: "IT-N244/N245 关键修复串：逐条读 COMMANDS 中 defer/switch/map/select/字符串/指针的 example，断言全含新注释/新语句（`// 先输出 2`、`// 无表达式`、`fmt.Println(k, v)`、`no case ready`、`i 是字节索引`、`fmt.Println(x) // 2`）。旧源码这些串均不存在 ⇒ GOFIX BAD 红。探针只在 clicks 执行，默认态无该串 ⇒ 零逃生。",
  },
  {
    slug: "it/linux-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Linux 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/sqlite-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：SQLite 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/text-to-hex",
    inputs: { input: "Hi!" },
    clicks: ["convert()"],
    expect: ["48 69 21"],
    ref: "独立复算：ASCII 表手算 H=0x48、i=0x69、!=0x21，默认分隔符为空格 ⇒ `48 69 21`。默认样例是 `Hello` ⇒ 默认态不含该串。",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "2024" },
    clicks: ["calcTool()"],
    expect: ["MMXXIV"],
    ref: "独立复算：2024 = 1000(M) + 1000(M) + 10(X) + 10(X) + 5(V) + 1(I) ⇒ MMXXIV。默认示例是另一个数字，默认态不含。",
  },
  {
    slug: "it/java-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Java 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/typescript-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：TypeScript 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/python-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Python 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2020-01-01", calcAmount: "3", calcUnit: "year", calcOp: "add" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2023-01-01 00:00:00"],
    ref: "独立复算：2020-01-01 + 3 年 = 2023-01-01。只锚本地日期串，**不锚时间戳**（页面时间戳随运行时区变化，非确定性）。默认态的样例日期是 2024-06-15。",
  },
  {
    slug: "it/sql-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：SQL 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/php-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：PHP 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/nginx-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Nginx 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/url-encode",
    inputs: { input: "a b&c" },
    clicks: ["encodeUrl()"],
    expect: ["a%20b%26c"],
    ref: "独立复算：`encodeURIComponent('a b&c')` ⇒ 空格→`%20`、`&`→`%26` ⇒ `a%20b%26c`。默认样例是 URL，默认态不含该串。",
  },
  {
    slug: "it/csharp-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：C# 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/ruby-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Ruby 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/rust-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Rust 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/css-minifier",
    inputs: { input: "/*c*/a{color : red}" },
    clicks: ["minify()"],
    expect: ["a{color:red}"],
    ref: "独立复算：去掉注释 `/*c*/` 与冒号后空格 ⇒ `a{color:red}`。默认示例带缩进/换行，默认态不含该串。",
  },
  {
    slug: "it/msisdn-lookup",
    inputs: { input: "112" },
    expect: ["E.164 格式： +112"],
    ref: "独立复算：`112` 的国家代码为 `1`（美国/加拿大），国内号码 `12`，E.164 归一化为 `+112`。默认样例是另一个号码。",
  },
  {
    slug: "it/emacs-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Emacs 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/kubernetes-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Kubernetes 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/mongodb-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：MongoDB 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "bcher.中文" },
    clicks: ["enc()"],
    expect: ["bcher.fiq228c"],
    ref: "独立复算：点号分段编码时纯 ASCII 标签原样保留、非 ASCII 标签走 punycode ⇒ bcher.fiq228c（与默认输入的中文域名产物不同）。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "中文" },
    clicks: ["document.getElementById('ace').checked=true;enc()"],
    expect: ["xn--fiq228c"],
    ref: "RFC 3492 §6.1 标准向量：'中文'.encode('punycode') = fiq228c，加 ACE 前缀 ⇒ xn--fiq228c（Python codec 核对）。默认输入为「中文域名.com」，产物 xn--fiq06l2rdsvs.com 不含该串。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "中国" },
    clicks: ["document.getElementById('ace').checked=true;enc()"],
    expect: ["xn--fiqs8s"],
    ref: "RFC 3492 标准向量：'中国'.encode('punycode') = fiqs8s，加 ACE 前缀 ⇒ xn--fiqs8s（Python codec 核对）。旧实现输出 fi@2282 类错误串，不命中。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "bücher" },
    clicks: ["document.getElementById('ace').checked=true;enc()"],
    expect: ["xn--bcher-kva"],
    ref: "RFC 3492 §6.1 混合基本/扩展码点经典向量：bücher → bcher-kva（Python codec 核对）；旧实现只遍历扩展码点、丢失基本码点计数 ⇒ 输出 bcher-（空扩展段），可据此判别修复前后。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "xn--fiq228c.com" },
    clicks: ["dec()"],
    expect: ["中文.com"],
    ref: "解码反向量：xn--fiq228c 按 RFC 3492 解码回「中文」⇒ 中文.com（与编码用例互逆）。默认输入为中文域名，不产生该串。",
  },
  {
    slug: "it/html-entity-encoder",
    inputs: { encodeInput: "<a>&" },
    clicks: ["encode()"],
    expect: ["&lt;a&gt;&amp;"],
    ref: "独立复算：`<`→`&lt;`、`>`→`&gt;`、`&`→`&amp;` ⇒ `&lt;a&gt;&amp;`。默认态的实体对照表里有 `&amp; &lt;` 等零散片段，但没有这条连续串。",
  },
  {
    slug: "it/matrix-multiplier",
    inputs: { ar: "2", ac: "2", br: "2", bc: "2" },
    clicks: [
      "document.getElementById('a0').value=1;document.getElementById('a1').value=2;document.getElementById('a2').value=3;document.getElementById('a3').value=4;document.getElementById('b0').value=5;document.getElementById('b1').value=6;document.getElementById('b2').value=7;document.getElementById('b3').value=1;build();calculate()",
    ],
    expect: ["结果 C = A × B （2×2）： 19 8 43 22"],
    ref: "独立复算：A=[[1,2],[3,4]]，B=[[5,6],[7,1]] ⇒ C[1][1]=1×5+2×7=19、C[1][2]=1×6+2×1=8、C[2][1]=3×5+4×7=43、C[2][2]=3×6+4×1=22。单元格 `a0..a3`／`b0..b3` 是运行期渲染（HTML 无字面 id）⇒ 必须 clicks 内按 id 赋值再 `build();calculate()`。",
  },
  {
    slug: "it/matrix-multiplier",
    // IT-E2 空态：四个维度全空时不得输出 0×0 结果。
    inputs: { ar: "", ac: "", br: "", bc: "" },
    clicks: ["calculate()"],
    expect: ["请输入矩阵 A 与 B 的行列数"],
    ref: "空态口径：四个维度全空 ⇒ 提示并 return；修复前 `+''` 得 0，ac===br 成立且 getM(...,0,0) 返回空数组，输出 `结果 C = A × B （0×0）`。默认 3×3 示例不含该提示。",
  },
  {
    slug: "it/matrix-multiplier",
    inputs: { ar: "2.5", ac: "2", br: "2", bc: "2" },
    clicks: ["calculate()"],
    expect: ["行列数须为 1–6 的整数"],
    ref: "维度须为正整数：旧实现直接 `+value` 取 2.5，`build()` 只渲染 5 个 A 单元格，而 `getM` 按 rows=2.5 读 a4 时取到 null ⇒ 抛 `Cannot read properties of null`。修复后先校验 1–6 整数，非法即提示并 return。默认 3×3 正常计算，不含该提示。",
  },
  {
    slug: "it/calc-subnet",
    inputs: { ip: "10.0.0.7", cidr: "28" },
    clicks: ["calc()"],
    expect: ["10.0.0.0 网络地址"],
    ref: "独立复算：10.0.0.7/28 ⇒ 网络 10.0.0.0、广播 10.0.0.15、/28、可用主机 14。注意该页是「值在前、标签在后」的排布（`10.0.0.0 网络地址`），写反了会注入态 FAIL。",
  },
  {
    slug: "it/calc-subnet",
    inputs: { ip: "10.0.0.1", cidr: "32" },
    clicks: ["calc()"],
    expect: ["广播地址 /32 CIDR 前缀 1 可用主机数"],
    ref: "Python ipaddress 3.8+ 对 /32 特例：num_addresses=1、hosts() 返回该地址本身，故可用主机数为 1（旧实现硬编码 0）。网络/广播均为 10.0.0.1；默认 192.168.1.100/24 不含该串。",
  },
  {
    slug: "it/qrcode",
    inputs: { contentTemplate: "TOOLBOX-HELLO-2026" },
    clicks: ["applyTemplate()"],
    expect: ["TOOLBOX-HELLO-2026"],
    ref: "二维码矩阵在桩内画不出来（`qrcode is not defined`），但**内容串本身先已写进结果区** ⇒ 直接锚内容串。用长串避免「超短串命中面过大」。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "length", from: "m", val: "100" },
    clicks: ["calcTool()"],
    expect: ["0.1 km 10000 cm 100000 mm"],
    ref: "独立复算：100 m = 0.1 km = 10000 cm = 100000 mm = 0.062137 mi = 109.36133 yd = 328.08399 ft（量纲换算，逐项可手算）。默认示例换算的不是 `m`。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "temp", val: "100", from: "℃" },
    clicks: ["calcTool()"],
    expect: ["212.00", "373.15"],
    ref: "第222批 IT-N191：独立复算 100℃ = 100×9/5+32 = 212.00°F = 100+273.15 = 373.15K。修复前温度分支只收 `C/F/K`，预设传入 `℃` 直接被拒 ⇒ 输出「温度单位请用 C/F/K」，两个派生串都不存在。默认态是 length/1/km，不含这两个数值。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "pressure", val: "1", from: "bar" },
    clicks: ["calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='UC222P='+(h.indexOf('100000')>=0&&h.indexOf('14.503774')>=0?'OK':'BAD');"],
    expect: ["UC222P=OK"],
    ref: "第222批 IT-N192：独立复算 1 bar = 1e5 Pa；psi 由 1 lbf/in² = 4.4482216152605 N / (0.0254 m)² = 6894.757293168 Pa 推得 1e5/6894.757293168 = 14.503774。修复前 `U` 无 pressure 表 ⇒ 走「不支持单位」错误分支，两个派生串都不存在 ⇒ BAD。锚写回 #result 避免 blob 折叠，默认态（length/1/km）BAD。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "energy", val: "1", from: "kwh" },
    clicks: ["calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='UC222E='+(h.indexOf('3600000')>=0&&h.indexOf('3412.141633')>=0?'OK':'BAD');"],
    expect: ["UC222E=OK"],
    ref: "第222批 IT-N192：独立复算 1 kWh = 3.6e6 J（定义值），1 BTU_IT = 1055.05585262 J ⇒ 3.6e6/1055.05585262 = 3412.141633。修复前 `U` 无 energy 表 ⇒ 错误分支 ⇒ BAD。默认态 BAD。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "length", val: "abc", from: "km" },
    clicks: ["calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='UC222V='+(h.indexOf('请输入有效数值')>=0?'OK':'BAD');"],
    expect: ["UC222V=OK"],
    ref: "第222批 IT-N194：非法数值必须停止计算并提示，而不是 `parseFloat` 失败后静默当 0 换算出一屏 0。修复前输出满屏 `0` 且无该提示 ⇒ BAD。默认态（val=1）BAD。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "mass", val: "1", from: '<img src=x onerror=N222XSS>' },
    clicks: ["calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='UC222X='+(h.indexOf('&lt;img')>=0&&h.indexOf('<img')<0?'OK':'BAD');"],
    expect: ["UC222X=OK"],
    ref: "第222批 IT-N194 加固：错误提示把用户可控的 `from` 直接拼进 innerHTML，必须转义。修复后 `&lt;img` 存在且无裸 `<img` 标签 ⇒ OK；修复前是裸标签 ⇒ BAD（即便 stub 采集会剥掉裸标签，`&lt;img` 也不存在，仍 BAD）。默认态 BAD。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "data", val: "1", from: "bit" },
    clicks: ["calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='UC222S='+(h.indexOf('1.164153e-10')>=0?'OK':'BAD');"],
    expect: ["UC222S=OK"],
    ref: "第222批 IT-N193 精度加固：独立复算 1 bit = 0.125 B，1 GB = 2³⁰ B ⇒ 0.125/1073741824 = 1.1641532182693481e-10。旧 `toExponential(2)` 只留 3 位有效数字输出 `1.16e-10`（相对误差 0.36%），现 6 位有效数字输出 `1.164153e-10` ⇒ OK。默认态 BAD。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "length", val: "1", from: "um" },
    clicks: ["calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='UC222U='+(h.indexOf('0.000001')>=0?'OK':'BAD');"],
    expect: ["UC222U=OK"],
    ref: "第222批 IT-N195：补微米 `um:1e-6`，独立复算 1 um = 1e-6 m；阈值判据是「绝对值小于 1e-6」，边界相等走 toFixed(6) 分支显示 `0.000001`。修复前 length 表无 `um` ⇒ 错误分支 ⇒ BAD。默认态 BAD。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "length", from: "nmi", val: "1" },
    clicks: ["calcTool()"],
    expect: ["1852", "1.852"],
    ref: "国际海里 nmi = 1852 m（BIPM/国际度量衡定义）：1 nmi = 1852 m = 1.852 km；默认态（from=km）输出 1000 而非 1852，故为强判别。修复前键 `nm:1852` 把海里写成了纳米，误差 1.852×10¹² 倍。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "length", from: "nm", val: "1" },
    clicks: ["calcTool()"],
    expect: ["1e-9"],
    ref: "纳米 nm = 10⁻⁹ m（SI 词头 nano）：1 nm 换算为 1e-9 m；修复前 `nm` 键值为 1852（海里），会输出 1852 而非 1e-9。",
  },
  {
    slug: "it/text-qr",
    inputs: { text: "TOOLBOX-QR-2026" },
    clicks: ["generate()"],
    expect: ["TOOLBOX-QR-2026"],
    ref: "二维码矩阵在桩内画不出来（`renderQR … leng`），但内容串先已写进结果区 ⇒ 直接锚内容串（与 `it/qrcode` 同族）。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "it/text-qr",
    inputs: { text: "old secret" },
    clicks: ["document.getElementById('text').value='old secret';generate();window.__qrMeta={probe:1};document.getElementById('text').value='';generate();document.getElementById('output').textContent='N551_META='+(window.__qrMeta===null?'NULL':'STALE');"],
    expect: ["N551_META=NULL"],
    ref: "IT-N551：先生成 old secret（__qrMeta 置位），强制置哨兵模拟已生成二维码，清空输入再 generate()，空分支必须清空 __qrMeta（修复前仅 return 不清空，旧二维码仍可下载）。断言贴回结果区的状态标记，old secret 不出现在判定串、非回显。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "GGGGGG", bgHex: "000000" },
    clicks: ["updateAll()"],
    expect: ["颜色需为有效的 3 或 6 位 HEX 值"],
    ref: "D-N1：前景 GGGGGG 为非法 HEX，修复前 hexToRgb 把非法值回退成黑色 [0,0,0]，与背景 000000 算出 ratio 1.00 / 不达标，给出误导结论。修复后 updateAll() 先 isValidHex 双校验，任一非法即清空比率、显示错误提示且不输出评级。该提示串仅非法态出现，默认合法色对（如 #FFFFFF/#000000 给 21.00）不命中。",
  },
  {
    slug: "sports/lanqiumingzhonglv-lanbanxiaolv",
    inputs: { fgm: "10", fga: "2", tpm: "0", tpa: "0", ftm: "0", fta: "0", oreb: "0", dreb: "0", min: "1" },
    clicks: ["calc()"],
    expect: ["命中数不能大于对应出手数"],
    ref: "SF-N35：投篮命中 10 > 出手 2 在修复前未被任何守卫覆盖（原 SF-N35 只校 tpm>fgm/tpa>fga/ftm>fta），FG% 算出 10/2=500% 虚高。修复后守卫补齐 fgm>fga 等「命中≤出手」判定，越界即清空结果区并提示。该提示串仅越界态出现，默认样例（fgm=8/fga=18）正常出数据、不命中。",
  },
  {
    slug: "design/svg-to-png",
    inputs: { svgInput: "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"10\" height=\"10\"><rect width=\"10\" height=\"10\"/></svg>", width: "10", height: "10" },
    clicks: ["window.Image=function(){var im={};im._ol=null;im._oe=null;im._src='';Object.defineProperty(im,'onload',{configurable:true,get:function(){return im._ol;},set:function(f){im._ol=f;globalThis.__lastOnload=f;}});Object.defineProperty(im,'onerror',{configurable:true,get:function(){return im._oe;},set:function(f){im._oe=f;}});Object.defineProperty(im,'src',{configurable:true,get:function(){return im._src;},set:function(s){im._src=s;}});return im;};globalThis.Image=window.Image;if(typeof URL!=='undefined'){URL.createObjectURL=function(){return 'blob:x';};URL.revokeObjectURL=function(){};}var __ce=document.createElement.bind(document);document.createElement=function(t){if(t==='canvas'){return {width:0,height:0,style:{},getContext:function(){return {fillRect:function(){},drawImage:function(){},set fillStyle(v){},get fillStyle(){return '';}};},toDataURL:function(){return 'DATAURL_STALE_MARKER';},toBlob:function(cb){if(typeof cb==='function')cb(null);}};}return __ce(t);};document.getElementById('svgInput').value='<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"10\" height=\"10\"><rect width=\"10\" height=\"10\"/></svg>';document.getElementById('width').value='10';document.getElementById('height').value='10';generate();document.getElementById('svgInput').value='';generate();try{if(globalThis.__lastOnload)globalThis.__lastOnload();}catch(e){}var __p=document.getElementById('preview');var __m=document.getElementById('exportMetaVal');__m.textContent='D21_LAST='+(lastDataURL===''?'EMPTY':'STALE')+' PREV='+(__p.innerHTML.indexOf('<img')>=0?'IMG':'NONE');"],
    expect: ["D21_LAST=EMPTY", "PREV=NONE"],
    ref: "D-N21：先生成合法 SVG（注册异步 img.onload，token=1），随即清空输入再 generate()（token=2，lastDataURL 清空、preview 写入「请输入 SVG 代码」），最后手动触发那个本应已作废的旧 onload（模拟异步晚到）。修复后 onload 头部校验 myToken!==__genToken 直接 return，旧结果不写回 ⇒ lastDataURL 仍空、preview 无 <img。修复前旧 onload 仍把旧 PNG 写回 lastDataURL 与 preview（PREV=IMG）。该判定串仅由注入 clicks 写入 exportMetaVal，默认快照（B）无 clicks ⇒ 不命中、判别力真实。",
  },
  {
    slug: "investment/irr-calc",
    inputs: { cf0: "-100", cf1: "230", cf2: "-132", cf3: "0", cf4: "0" },
    clicks: ["calcTool()"],
    expect: ["可能存在多重 IRR"],
    ref: "IRR 多根现金流：现金流 -100、230、-132、0、0 令 NPV=0 的根有两个（10% 与 20%）。修复前 noRoot 仅用两端点乘积判断，多根时两端同号误判无解却仍显示 IRR 10.00%，并配「无零点」提示，自相矛盾。修复后改以 irr() 实际求根结果（NaN=无解）为准，正确提示可能存在多重 IRR。判定串只出现在非常规多根现金流，默认 [-1000,300,400,500,200] 给 15.32% 与「解唯一」，不命中。",
  },
  {
    slug: "insurance/net-single-premium",
    inputs: {},
    clicks: ["__nspLast={nsp:81763.70};document.getElementById('B').value='';calcTool();document.getElementById('result').textContent='R6_LAST='+(__nspLast===null?'NULL':'STALE');"],
    expect: ["R6_LAST=NULL"],
    ref: "R-N6：模拟一次有效计算已把 __nspLast 置为旧保费 81763.70，再清空保额 B 重算触发必填守卫。修复后 __nspLast=null 已置于守卫之前，旧明细立即清空、不可再被导出或写历史（导出入口 if(!__nspLast) 阻断）；修复前守卫 return 早于旧代码里的 __nspLast=null，旧明细仍在 ⇒ R6_LAST=STALE、导出/历史残留旧值。断言贴回结果区的状态标记，旧保费数值不出现在判定串、非回显。",
  },
  {
    slug: "rehabilitation/berg-balance-scale",
    inputs: {},
    clicks: ["window.TBKit={util:{isEn:function(){return false;},exportTable:function(){}}};__bbsExport();var tb=document.querySelector('#bbsTable tbody');var t=tb?tb.textContent:'';document.getElementById('resultBox').textContent='M19='+(t.indexOf('低于安全界值 45 分约')>=0?'LEAK':'OK');"],
    expect: ["M19=OK"],
    ref: "M-N19：默认（全部未评分）调用 __bbsExport，修复后 fallGap 仅完整作答（answered===14）时计算，CSV 风险行不再外泄「低于安全界值 45 分约 X 分，每分约 7% 线性估算」后缀；修复前未完成作答仍无条件追加该后缀（total=0 ⇒ fallGap=45）。断言贴回 resultBox 的标记，输入无关、非回显。",
  },
  {
    slug: "it/barcode-upc",
    inputs: { data: "12345678905" },
    clicks: ["generate()"],
    expect: ["123456789050"],
    ref: "独立复算：UPC-A 校验位 p = (10 − (3×(d1+d3+d5+d7+d9+d11) + (d2+d4+d6+d8+d10)) mod 10) mod 10；12345678905 ⇒ 3×(1+3+5+7+9+0)=75、2+4+6+8+5=25、和 100 ⇒ p=0。默认样例是 03600029145（补出 …2），默认态不含本串。",
  },
  {
    slug: "it/matrix-determinant",
    inputs: { size: "2" },
    clicks: ["document.getElementById('a0').value=3;document.getElementById('a1').value=2;document.getElementById('a2').value=5;document.getElementById('a3').value=7;calculate()"],
    expect: ["= 21 − 10 = 11"],
    ref: "独立复算：|A| = a·d − b·c = 3×7 − 2×5 = 21 − 10 = 11。矩阵格子 a0..a3 是运行期渲染（HTML 无字面 id）⇒ clicks 里按 id 赋值再 calculate()。默认 2×2 矩阵不是本组，默认态不含该串。",
  },
  {
    slug: "it/matrix-inverter",
    inputs: { size: "2" },
    clicks: ["document.getElementById('a0').value=4;document.getElementById('a1').value=7;document.getElementById('a2').value=2;document.getElementById('a3').value=6;calculate()"],
    expect: ["逆矩阵 A⁻¹： 0.6 -0.7 -0.2 0.4"],
    ref: "独立复算：A=[[4,7],[2,6]]，det=4×6−7×2=10 ⇒ A⁻¹=(1/10)·[[6,−7],[−2,4]]=[[0.6,−0.7],[−0.2,0.4]]，且 A×A⁻¹=I。同 matrix-determinant 的 clicks 模板。",
  },
  {
    slug: "it/matrix-inverter",
    inputs: { size: "2" },
    clicks: ["document.getElementById('a0').value='1e-13';document.getElementById('a1').value=0;document.getElementById('a2').value=0;document.getElementById('a3').value='1e-13';calculate()"],
    expect: ["逆矩阵 A⁻¹： 1e+13 0 0 1e+13"],
    ref: "IT-N370：A=diag(1e-13,1e-13)，det=1e-26≠0，逆矩阵为 diag(1e13,1e13)。修复前主元判据是绝对值 `Math.abs(pivot)<1e-12` ⇒ 直接报「矩阵不可逆（奇异矩阵）」；现改为相对尺度（scale×1e-12）。expect 是求逆后的具体数值串，输入里只有 1e-13 ⇒ 量级相反、不可能是回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "AB" },
    clicks: ["enc()"],
    expect: ["1-2"],
    ref: "独立复算：A=1、B=2，默认分隔符为 `-` ⇒ `1-2`。产物是纯数字、不含输入字母 ⇒ 天然非回显。默认样例是单词（多位字母），默认态不含本串。",
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "42!" },
    clicks: ["enc();document.getElementById('__tbProbe').textContent='N282 '+document.getElementById('output').value;"],
    expect: ["4-2-!"],
    ref: "IT-N282：非字母（数字/标点）须原样保留、不静默丢弃，也不产生空词分隔符。修复前 enc 对非字母 return '' 后 filter ⇒ 输出空串；现字符级保留并用 sep 连接（42! → 4-2-!）。默认样例为字母词，不命中。",
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "1-99-2" },
    clicks: ["dec();document.getElementById('__tbProbe').textContent='N283 '+document.getElementById('output').value;"],
    expect: ["A?B", "99"],
    ref: "IT-N283：越界数字 99 不得静默跳过，须就地标记并提示非法项。修复前 dec 只输出合法的 ⇒ `AB`；现输出 `A?B  [非法项: 99]`。默认样例非该数字串，不命中。",
  },
  {
    slug: "it/affine-cipher",
    inputs: { input: "ABCD", a: "3", b: "5" },
    clicks: ["enc()"],
    expect: ["FILO"],
    ref: "独立复算：仿射加密 E(x)=(a·x+b) mod 26，a=3、b=5 ⇒ A(0)→5=F、B(1)→8=I、C(2)→11=L、D(3)→14=O ⇒ `FILO`。dump 期 `gcd` 报栈溢出（页面在算逆元）但不影响产物。默认参数是另一组 a/b。",
  },
  {
    slug: "it/bacon-cipher",
    inputs: { input: "AB", mode: "enc" },
    expect: ["0000000001"],
    ref: "独立复算：Bacon 密码 A=`aaaaa`(00000)、B=`aaaab`(00001) ⇒ `0000000001`。**必须显式把 mode 设为 enc**（默认 mode 是解码方向，不带则产物不同）。产物是纯 0/1、不含输入字母 ⇒ 非回显。",
  },
  {
    slug: "it/atbash-cipher",
    inputs: { input: "ABC" },
    clicks: ["transform()"],
    expect: ["ZYX"],
    ref: "独立复算：Atbash 把字母表倒序映射（A↔Z、B↔Y、C↔X）⇒ `ZYX`。产物不含输入字母 ⇒ 非回显；默认样例是单词，默认态不含本串。",
  },
  {
    slug: "it/ascii-tree-generator",
    inputs: { paths: "a/b.txt\na/c/d.txt" },
    clicks: ["build()"],
    expect: ["a/ ├── b.txt └── c/ └── d.txt"],
    ref: "独立复算：两条路径共享顶层 `a/` ⇒ `b.txt` 是 `a` 的末项用 `└──`、其父层缩进两格；`a/c/d.txt` 的 `c/` 同样末级 ⇒ 末条为 `└── d.txt`。产物是「结构符号 + 文件名」，非裸输入回显。",
  },
  {
    slug: "it/barcode-ean",
    inputs: { data: "400638133393" },
    clicks: ["generate()"],
    expect: ["4006381333931"],
    ref: "独立复算：EAN-13 校验位 = (10 − Σ(位置1,3,5…×1 + 位置2,4,6…×3) mod 10) mod 10；400638133393 ⇒ 4+0+0+18+3+24+1+9+3+9+9+9=89 ⇒ 校验位 1。默认样例是 590123412345（补出 …7），默认态不含本串。",
  },
  {
    slug: "it/barcode-ean",
    inputs: { data: "123456789012" },
    clicks: ["generate()"],
    expect: ["1234567890128"],
    ref: "独立复算：同上口径，123456789012 ⇒ 4+0+6+6+3+24+1+9+3+9+9+9=83 ⇒ 校验位 8。用与默认样例不同的号码，确保双态可辨。",
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", b: "10", op: "AND" },
    clicks: ["calc()"],
    expect: ["结果： 8"],
    ref: "独立复算：12 = 0b1100、10 = 0b1010 ⇒ 按位与 = 0b1000 = 8。注意运算符 select 的 option value 是大写 `AND`（传 `&` 会被页面忽略，产出恒 0）。",
  },
  {
    slug: "it/caesar-cipher",
    inputs: { input: "ABC", shift: "3" },
    clicks: ["process()"],
    expect: ["DEF"],
    ref: "独立复算：凯撒位移 +3 ⇒ A→D、B→E、C→F ⇒ `DEF`。默认样例文本不是本串。",
  },
  {
    slug: "it/binary-to-text",
    inputs: { input: "01000001" },
    clicks: ["convert()"],
    expect: ["A"],
    ref: "独立复算：8 位二进制 01000001 = 十进制 65 = ASCII 字符 `A`。产物是解码后的文本、不是输入回显；默认样例是另一段码。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.01", likelihood: "0.9", falsePositive: "0.1" },
    clicks: ["calculate()"],
    expect: ["0.009 + 0.099 = 0.108"],
    ref: "独立复算：P(E) = P(E|H₁)·P(H₁) + P(E|¬H₁)·P(¬H₁) = 0.9×0.01 + 0.1×0.99 = 0.009 + 0.099 = 0.108；后验 = 0.009/0.108 ≈ 0.083。锚在「中间展开式」上，逐项可手算。默认样例不是这组参数。",
  },
  {
    slug: "it/convert-11",
    inputs: { val: "10", from: "dec", to: "bin" },
    clicks: ["calc()"],
    expect: ["00000000.00000000.00000000.00001010"],
    ref: "独立复算：10₁₀ = 1010₂，按 4 字节补零成 32 位 ⇒ `00000000.00000000.00000000.00001010`。注意该页是**进制**转换（option value 只有 `dot`/`bin`/`dec`），传单位符号（m/cm）会被判为输入非法。",
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "100", std: "15", n: "25", conf: "0.95", dist: "z" },
    clicks: ["calc()"],
    expect: ["边际误差 ME = 1.960 × 3.0000 = 5.8800"],
    ref: "独立复算：SE = s/√n = 15/√25 = 3；z(95%) = 1.960；ME = 1.960 × 3 = 5.8800 ⇒ 区间 [94.120, 105.880]。锚「中间展开式」，避开最终多位小数。默认样例参数不同。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "TOOLBOX" },
    clicks: ["calc()"],
    expect: ["CRC-8 0xc9"],
    ref: "独立复算：CRC-8（多项式 0x07、初值 0）逐字节移位 ⇒ 0xc9。默认样例恰是 `123456789`（标准校验值 0xf4）⇒ 默认态同样命中，故必须用别的输入串。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    clicks: ["calc()"],
    expect: ["CRC-8 0x5f"],
    ref: "独立复算：同上口径，`abc` 的 CRC-8 = 0x5f。同一页面换输入各写一条，两条 expect 互不相同。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    clicks: ["document.getElementById('customOn').checked=true; calc();"],
    expect: ["自定义模型 (width=8, poly=0x07) 0x5f"],
    ref: "自定义 CRC 模型（2026-10-26）：勾选 customOn 后按六参（width=8/poly=07/init=00/refin=0/refout=0/xorout=00）= 标准 CRC-8 ⇒ abc = 0x5f，自洽核对；锚含「自定义模型」卡名区分内置卡。判别态 clicks 清空 ⇒ 无自定义卡，零交集。（clicks 内勾选而非 checks：checks 机制对该页行为不稳，clicks 直调可控。）",
  },
  {
    slug: "it/decimal-encode",
    inputs: { input: "AB" },
    clicks: ["enc()"],
    expect: ["65 66"],
    ref: "独立复算：`A`=65、`B`=66，默认分隔符为空格 ⇒ `65 66`。产物是纯数字，不含输入字母 ⇒ 非回显。默认样例是另一段文本。",
  },
  {
    slug: "it/hex-encode",
    inputs: {"input":"world"},
    clicks: ["enc()"],
    expect: ["776f726c64"],
    ref: "独立复算：`H`=0x48、`i`=0x69 ⇒ `4869`。十六进制产物不含输入文本 ⇒ 非回显；默认样例不是本串。",
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "4869" },
    clicks: ["convert()"],
    expect: ["Hi"],
    ref: "独立复算：`48`=72=`H`、`69`=105=`i` ⇒ `Hi`。与上一条互逆，一并收下可覆盖双向路径。默认样例不是本串。",
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "2", x: "1" },
    clicks: ["calculate()"],
    expect: ["1 − 0.135 = 0.865"],
    ref: "独立复算：指数分布 CDF F(x)=1−e^{−λx}，λ=2、x=1 ⇒ e^{−2}=0.135，F=1−0.135=0.865（PDF=2×0.135=0.271）。默认样例恰是 λ=0.5,x=2 ⇒ 默认态同样命中的那一组，故换参数。锚在中间展开式。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "10", K: "3", n: "4", k: "1" },
    clicks: ["calculate()"],
    expect: ["3 × 35 / 210 = 0.5"],
    ref: "独立复算：超几何概率 P = C(K,k)·C(N−K,n−k)/C(N,n) = C(3,1)·C(7,3)/C(10,4) = 3×35/210 = 105/210 = 0.5。锚在「中间展开式」（三个组合数逐个可算），默认样例参数不同。",
  },
  {
    slug: "it/html-nesting-checker",
    inputs: { html: "<div><p>x</div>" },
    clicks: ["check()"],
    expect: ["被隐式闭合"],
    ref: "独立复算：`<p>` 未闭合，遇到 `</div>` 时触发隐式闭合 ⇒ 报告第 1 行 `<p>` 被隐式闭合。产物是「检测结论 + 定位行」而非输入回显；默认样例不同。",
  },
  {
    slug: "it/json-minify",
    inputs: { input: '{ "a" : 1 }' },
    clicks: ["process()"],
    expect: ['{"a":1}'],
    ref: "独立复算：去掉 JSON 中多余空格 ⇒ `{\"a\":1}`（字节数 11 → 7，压缩率 36.4% 也可手算）。默认样例不是本串。",
  },
  {
    slug: "it/list-converter",
    inputs: { input: "a\nb", mode: "comma" },
    clicks: ["convert()"],
    expect: ["a, b"],
    ref: "独立复算：两行列表按逗号模式合并 ⇒ `a, b`。入参含换行（探针文件必须用 Python 的 `json.dumps` 生成，JSON 串内不允许字面换行）。",
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "apple apple banana" },
    clicks: ["extractKeywords()"],
    expect: ["apple 2 banana 1"],
    ref: "独立复算：词频统计 ⇒ apple 出现 2 次、banana 1 次，产物排序为 `apple 2 banana 1`。统计类天然非回显；默认样例文本不同。",
  },
  {
    slug: "it/math-evaluator",
    inputs: { expr: "(1+2)*3" },
    clicks: ["calc()"],
    expect: ["结果： 9"],
    ref: "独立复算：先算括号 1+2=3，再乘 3 ⇒ 9。表达式求值类是最典型的可手算用例源（运算符优先级固定）。默认样例表达式不同。",
  },
  {
    slug: "it/numeronym-generator",
    inputs: { input: "Global Positioning System" },
    clicks: ["generate()"],
    expect: ["P9g"],
    ref: "IT-N286 默认阈值 7：Global(6<7) 与 System(6<7) 原样保留，Positioning(10≥7) → P9g（P+9字母+g）。修复前 G4l（Global 被缩）⇒ 旧锚不命中；默认样例不同。",
  },
  {
    slug: "it/morse",
    inputs: { input: "SOS" },
    clicks: ["convert()"],
    expect: ["... --- ..."],
    ref: "独立复算：S=`...`、O=`---` ⇒ `... --- ...`（点划间空格、字母间斜杠）。产物改写输入字符 ⇒ 非回显；默认样例不同。",
  },
  {
    slug: "it/normal-distribution",
    inputs: { mu: "0", sigma: "1", x0: "1" },
    clicks: ["calculate()"],
    expect: ["Z = (x−μ)/σ = (1−0)/1 = 1"],
    ref: "独立复算：标准正态 Z=(x−μ)/σ = (1−0)/1 = 1 ⇒ Φ(1)=0.841。锚在中间展开式；注意该页的 tab 控件 id 是 `mode0`（传 `mode` 无效）。默认样例参数不同。",
  },
  {
    slug: "it/margin-of-error",
    inputs: { N: "100", n: "50", p: "0.5", conf: "0.95" },
    clicks: ["calculate()"],
    expect: ["1.96 × 0.071 = ±0.139"],
    ref: "独立复算：SE = √[p̂(1−p̂)/n] = √(0.25/50) = √0.005 ≈ 0.071；E = z*×SE = 1.96×0.071 ≈ ±0.139（再乘有限总体修正 √(50/99) 得 ±0.098）。锚在中间展开式，默认样例参数不同。",
  },
  {
    slug: "it/octal-encode",
    inputs: {"input":"ok"},
    clicks: ["enc()"],
    expect: ["ok\n157 153"],
    ref: "独立复算：H=0o110=72、i=0o151=105，空格分隔。默认样例参数不同。",
  },
  {
    slug: "it/phone-parser",
    inputs: { cc: "1", phone: "4155550123" },
    clicks: ["calcTool()"],
    expect: ["+14155550123"],
    ref: "独立复算：去掉分隔符后拼接国家码 + 号码 = +14155550123（E.164）。默认样例号码不同。",
  },
  {
    slug: "it/phone-screen-sizes",
    inputs: { diag: "5", resw: "1080", resh: "1920" },
    clicks: ["calcTool()"],
    expect: ["441 PPI"],
    ref: "独立复算：对角线像素 √(1080²+1920²) = 2202.9，PPI = 2202.9/5 ≈ 440.6 ⇒ 441。默认样例参数不同。",
  },
  {
    slug: "it/poisson-distribution",
    inputs: { lambda: "3", k: "1" },
    clicks: ["calculate()"],
    expect: ["3 × 0.05 / 1 = 0.149"],
    ref: "独立复算：P(X=1) = λ¹e^(−λ)/1! = 3×0.049787/1 = 0.1494。锚在中间展开式；默认 λ=3,k=2 与注入同产物，故必须把 k 换成 1 才破题。",
  },
  {
    slug: "it/prime-checker",
    inputs: { n: "91" },
    clicks: ["calcTool()"],
    expect: ["91 是合数"],
    ref: "独立复算：91 = 7×13，是合数；产物另含最小质因数 7 与分解式。默认样例即 97（素数），换 91 才破题。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=b" },
    clicks: ["enc()"],
    expect: ["a=3db"],
    ref: "Quoted-Printable 编码：可打印 ASCII 原样保留，= 转义为 =3D（小写十六进制，因 upper 复选框默认未勾选）。默认样例不含本串。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=3db" },
    clicks: ["dec()"],
    expect: ["a=b"],
    ref: "Quoted-Printable 解码：把 =3d 还原为 = ⇒ a=b。与本页编码用例成对，双向均依赖被测点。",
  },
  {
    slug: "it/markdown-table-generator",
    inputs: { cols: "2", headerLine: "A,B", bodyLine: "1,2", rows: "1", align: "left" },
    clicks: ["renderPreview()"],
    expect: ["| 11 | 21 |"],
    ref: "读源码：parseRow 按逗号切格，行值 = 单元格值拼上行号（r+1，故第一行是 11/21），对齐标记 `:---` 对应 align=left。默认样例是 4 列 4 行，产物不同。",
  },
  {
    slug: "it/json-to-toml",
    inputs: { input: '{"a":1,"b":{"c":2}}' },
    clicks: ["doToml()"],
    expect: ["c = 2"],
    ref: "独立复算：嵌套对象转成表节 ⇒ TOML 为 `a = 1` / `[b]` / `c = 2`。锚在末行，默认样例字段不同。",
  },
  {
    slug: "it/json-to-toml",
    inputs: { input: '{"a":1,"b":{"c":2}}', indent: "4" },
    clicks: ["doToml();var t=String(document.getElementById('output').textContent);document.getElementById('output').textContent='UC224I='+(/\\n {4}c = 2/.test(t)&&/^a = 1/.test(t)?'OK':'BAD');"],
    expect: ["UC224I=OK"],
    ref: "第224批 IT-N200：独立复算 4 空格档——顶层 `a = 1` 不缩进、`[b]` 在 depth 0 不缩进、子层 `c = 2` 前导恰好 4 空格。修复前 `toToml` 不接收缩进参数，三档输出逐字节相同（`c = 2` 无缩进）⇒ BAD。默认态 SAMPLE 用 2 空格档 ⇒ BAD。",
  },
  {
    slug: "it/json-to-toml",
    inputs: { input: '{"a":1,"b":{"c":2}}', indent: "tab" },
    clicks: ["doToml();var t=String(document.getElementById('output').textContent);document.getElementById('output').textContent='UC224T='+(/\\n\\tc = 2/.test(t)?'OK':'BAD');"],
    expect: ["UC224T=OK"],
    ref: "第224批 IT-N200：Tab 预设必须输出真制表符 0x09 而不是两个字面字符 `\\t` 或两空格。修复前下拉完全无效 ⇒ BAD；默认态（2 空格档）BAD。blob 会折叠空白，故用页内探针判形态。",
  },
  {
    slug: "it/json-to-toml",
    inputs: { input: '{"d":"2020-01-01T00:00:00Z"}' },
    clicks: ["doToml();document.getElementById('output').textContent='UC224D='+String(document.getElementById('output').textContent);"],
    expect: ["UC224D=d = 2020-01-01T00:00:00Z"],
    ref: "第224批 IT-N201：严格 ISO 8601 日期时间按 TOML 原生 datetime 输出为裸值（不加引号），兑现页面「支持 ISO 日期字符串」的宣称。修复前字符串一律 JSON.stringify ⇒ `d = \"2020-01-01T00:00:00Z\"`。默认 SAMPLE 无该字段 ⇒ 不命中。",
  },
  {
    slug: "it/json-to-toml",
    inputs: { input: '{"a.b":1,"a b":2}' },
    clicks: ["doToml();var q=String.fromCharCode(34),t=String(document.getElementById('output').textContent);document.getElementById('output').textContent='UC224K='+(t.indexOf(q+'a.b'+q+' = 1')>=0&&t.indexOf(q+'a b'+q+' = 2')>=0?'OK':'BAD');"],
    expect: ["UC224K=OK"],
    ref: "第224批 IT-N199 补证据：含点 / 含空格的键必须用 quoted key，否则 TOML 会把 `a.b = 1` 读成嵌套表、`a b = 1` 直接语法错。该能力已由其他 Agent 修好（`tomlKey`），本例锁住不回退。默认 SAMPLE 无这两键 ⇒ BAD。",
  },
  {
    slug: "it/json-to-toml",
    // IT-N23 回归：TOML 无 null 类型，必须显式报错而不是静默改写成空字符串。
    inputs: { input: '{"a":null}' },
    clicks: ["doToml()"],
    expect: ["TOML 没有 null 类型"],
    ref: "独立复算：TOML 没有 null 类型，页面应报错；修复前 `tomlVal(null)` 返回 `\"\"`，静默把 null 变成空字符串（`a = \"\"`）。默认样例无 null，不命中。",
  },
  {
    slug: "it/json-to-toml",
    // IT-N23 回归：对象与标量混排的数组不是合法 TOML，必须报错。
    inputs: { input: '{"a":[{"b":1},2]}' },
    clicks: ["doToml()"],
    expect: ["TOML 数组不支持对象与标量混排"],
    ref: "独立复算：数组内同时含表与标量时，`tomlVal` 会退回 `JSON.stringify` 产出 `[{\"b\":1}, 2]`，这不是合法 TOML；修复后直接报错。默认样例无混排数组，不命中。",
  },
  {
    slug: "it/css-formatter",
    inputs: { input: "a{color:red;font-size:12px}" },
    clicks: ["doBeautify()"],
    expect: ["a { color: red; font-size: 12px }"],
    ref: "格式化规则：选择器后补空格、声明按 `属性: 值;` 输出。默认样例（.btn 等）格式化后不含本串。",
  },
  {
    slug: "it/css-formatter",
    inputs: { input: "a { color: red; }" },
    clicks: ["doMinify()"],
    expect: ["a{color:red;}"],
    ref: "压缩规则：去选择器/大括号间的空白，保留声明末尾分号。默认样例压缩结果不含本串。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"a":1,"b":"x"}', rootName: "MyRoot" },
    clicks: ["convert()"],
    expect: ["interface MyRoot {"],
    ref: "默认语言 TypeScript：对象数组/对象按字段类型生成 interface，类型映射 number/string/boolean。注意本页默认样例与本条入参同构 ⇒ 必须换 rootName 才破双态。",
  },
  // ---- IT-N379/N380/N381/N382/N383/N384：json-to-code 生成器修复 ----
  // 采集说明：`#output` 的 innerHTML 经 highlight() 上色，harness 剥标签时会在被包成
  // <span> 的关键字/字符串两侧引入空格（`number ;`、`json: "zz" `），且 `<`/`>` 已被
  // escapeHtml 转义成 &lt;/&gt; ⇒ 断言一律取「无分号、无尖括号」的片段。
  {
    slug: "it/json-to-code",
    inputs: { input: '{"u":{"aa":1}}' },
    clicks: ["convert()"],
    expect: ["interface RootU { aa: number"],
    ref: "IT-N379：嵌套对象必须递归生成子 interface（修复前只输出 `interface Root { u: RootU; }`，RootU 无定义 ⇒ tsc 报 Cannot find name 'RootU'）。桩内 optReadonly/optExport 恒未勾 ⇒ 无 readonly/export 前缀。默认样例无 u/aa 键 ⇒ 双态可判别。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"items":[{"x":1}]}' },
    clicks: ["convert()"],
    expect: ["interface RootItems { x: number", "items: RootItems[];"],
    ref: "IT-N380（TS 侧）：对象数组的元素类型名与子 interface 同名为 RootItems，字段声明 RootItems[]。修复前元素名固定再补 Item 后缀（ItemsItem[]）且根本不生成子 interface。默认样例无 items/x 键。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"orders":[{"id":7}]}' },
    clicks: ["setLang('go')"],
    expect: ["type RootOrders struct { Id int"],
    ref: "IT-N380（Go）：只断言**定义名** `type RootOrders struct`（修复前定义是 RootOrdersItem）；字段引用 `[]RootOrders` 修复前后都存在，若一并写进 expect 会因「任一命中即通过」在修复前也变绿 ⇒ 已删掉。默认样例无 RootOrders 定义（其结构体是 RootUser / RootOrdersItem）。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":{"k":1}}' },
    clicks: ["setLang('go')"],
    expect: ["} type RootZz struct { K int"],
    ref: "IT-N381（Go）：`package main` 只能在文件头出现一次，子结构体只输出类型体。修复前根 struct 的 `}` 后面紧跟又一段 `package main type RootZz struct`，故「} type RootZz」这段在修复前不存在（负向对照实测变红）。键名 zz/k 使断言依赖入参。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":{"k":1}}' },
    clicks: ["setLang('proto')"],
    expect: ["} message RootZz { int32 k = 1"],
    ref: "IT-N381（Proto）：同一 .proto 文件只允许一处 syntax 声明（proto3）。修复前根 message 的 `}` 后面紧跟又一段 syntax 声明 + message RootZz，故「} message RootZz」在修复前不存在。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"parent":{"a\\\"b":1}}' },
    clicks: ["var t=toGo(JSON.parse(document.getElementById('input').value),'Root');document.getElementById('__tbProbe').textContent='GOTAG nestedWarning='+(t.includes('Go JSON tag 无法映射')?1:0)+' noStruct='+(t.includes('type Root struct')?0:1);"],
    expect: ["GOTAG nestedWarning=1 noStruct=1"],
    ref: "特殊键位于嵌套对象时必须明确拒绝生成误导性 Go struct，避免 encoding/json 静默丢失字段映射。",
  },
  {
    slug: "it/json-to-code",
    clicks: ["var bad=['a,b','a\\\\b','', '-', 'a`b', 'a'+String.fromCharCode(0)+'b'];var ok=bad.every(function(k){var o={};o[k]=1;var t=toGo(o,'Root');return t.includes('Go JSON tag 无法映射')&&!t.includes('type Root struct');});document.getElementById('__tbProbe').textContent='GOBAD all='+Number(ok);"],
    expect: ["GOBAD all=1"],
    ref: "Go 特殊键包含逗号、反斜杠、空键、忽略标记、反引号和控制字符时必须全数拒绝错误映射。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"姓名":"Alice","normal":4}' },
    clicks: ["var t=toGo(JSON.parse(document.getElementById('input').value),'Root');document.getElementById('__tbProbe').textContent='GOUNICODE exported='+(t.includes('F姓名 string')?1:0);"],
    expect: ["GOUNICODE exported=1"],
    ref: "Unicode 字母虽可用于 Go JSON tag，但汉字字段名必须以大写字母开头导出，才能参与 encoding/json 的双向转换。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '[{"zz":1}]' },
    clicks: ["setLang('go')"],
    expect: ["type Root []RootItem", "type RootItem struct { Zz int"],
    ref: "IT-N382（根数组）：根是数组时生成切片别名 + 元素结构体。修复前 Object.entries(数组) 把下标当键 ⇒ `type Root struct { 0 Root0 }`（字段名 0 非法）。默认样例是对象 ⇒ 双态可判别。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: "null" },
    clicks: ["convert()"],
    expect: ["无法推断类型"],
    ref: "IT-N382（根 null）：合法 JSON null 必须给明确提示。修复前 Object.entries(null) 抛 TypeError，convert() 无 try 包裹 ⇒ 结果区保留上一次内容（静默失败）。默认样例是对象、不产生该提示。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"qnote":null,"qlist":[]}' },
    clicks: ["setLang('py');var t=document.getElementById('output').innerHTML.replace(/<[^>]+>/g,' ').split(' ').join('');document.getElementById('output').textContent='N383 any='+(t.indexOf('importAny,List')>=0?1:0)+' qn='+(t.indexOf('qnote')>=0?1:0);"],
    expect: ["N383 any=1 qn=1"],
    ref: "IT-N383：pyType 会渲染出 Any，但头部只 import 了 List, Optional ⇒ pydantic 求值注解即 NameError。判据把去标签后的 HTML 再删除全部空格（高亮剥标签会在 token 两侧留多个空格，逐字比对不可靠），再查 `importAny,List`：该串只能来自 `from typing import Any, List, Optional`。配合入参独有键 qnote，整串两条同时成立才命中 ⇒ 非静态逃生项；修复前 any=0、默认态（注入失败）qn=0 均不命中。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"user_name":1,"api-key":"x"}' },
    clicks: ["convert()"],
    expect: ["userName: number", "apiKey: string", "原键: user_name"],
    ref: "IT-N384：承诺「键名按目标语言惯例转换」，TS 字段转 camelCase 并注明原始键名（重命名后反序列化需映射）。修复前原样输出 user_name、api-key（后者根本不是合法 TS 字段名）。默认样例全是 camelCase 键 ⇒ 不产生「原键」注释。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":[{"v":1}]}' },
    clicks: ["setLang('csharp')"],
    expect: ["public class RootZz {"],
    ref: "IT-N380（C#）：只断言定义 `public class RootZz {`（修复前定义是 RootZzItem）；字段引用 List<RootZz> 修复前就存在，写进 expect 会因「任一命中即通过」失去判别力。默认样例无 RootZz 定义。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":[{"v":1}]}' },
    clicks: ["setLang('java')"],
    expect: ["public class RootZz {"],
    ref: "IT-N380（Java）：只断言类定义 `public class RootZz {`（修复前是 RootZzItem）；字段引用 List<RootZz> 修复前已存在，故不作 expect。默认样例无 RootZz 定义。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":[{"v":1}]}' },
    clicks: ["setLang('kotlin')"],
    expect: ["data class RootZz("],
    ref: "IT-N380（Kotlin）：只断言 `data class RootZz(`（修复前是 RootZzItem）；字段引用 List<RootZz> 修复前已存在，不作 expect。默认样例无 RootZz 定义。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":[{"v":1}]}' },
    clicks: ["setLang('rust')"],
    expect: ["pub struct RootZz {"],
    ref: "IT-N380（Rust）：只断言 `pub struct RootZz {`（修复前是 RootZzItem）；字段引用 Vec<RootZz> 修复前已存在，不作 expect。默认样例无 RootZz 定义。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"zz":[{"v":1}]}' },
    clicks: ["setLang('py')"],
    expect: ["class RootZz(BaseModel):"],
    ref: "IT-N380（Python）：只断言 `class RootZz(BaseModel):`（修复前类名是 RootZzItem）；字段引用 List[RootZz] 修复前已存在，不作 expect。默认样例无 RootZz 定义。",
  },
  {
    slug: "it/js-minifier",
    inputs: { input: "var a = 1;   // keep\nfunction f(){ return   a; }" },
    clicks: ["minify()"],
    expect: ["function f(){ return a; }"],
    ref: "压缩规则：折叠连续空白（注释复选框默认未勾选，故注释保留）。产物是输入经空白折叠后的改写，删掉输入即不完整。默认样例不含本串。",
  },
  {
    slug: "it/plist-parser",
    inputs: { input: '{"a":1}' },
    clicks: ["jsonToPlist()"],
    expect: ["a 1"],
    ref: "JSON → plist：字段名与标量值按序排列。默认样例键名不同。",
  },
  {
    slug: "it/plist-parser",
    inputs: { input: '{"a":{"__plistType":"real","value":"1.0"}}' },
    clicks: ["jsonToPlist();var t=String(document.getElementById('output').textContent||'');document.getElementById('__tbProbe').textContent='PLREAL '+(t.indexOf('<real>1.0</real>')>=0&&t.indexOf('__plistType')<0?'OK':'BAD');"],
    expect: ["PLREAL OK"],
    ref: "IT-N202 第225批：带 __plistType 标记的 real 对象回写为原生 <real> 标签（不是当普通 dict 拆成键）。harness blob 会剥标签，故在页面内读 textContent 判断后写探针。输入串移除或改普通对象即不命中。",
  },
  {
    slug: "it/plist-parser",
    inputs: { input: '{"n":{"__plistType":"integer","value":"9007199254740993"}}' },
    clicks: ["jsonToPlist();var t=String(document.getElementById('output').textContent||'');document.getElementById('__tbProbe').textContent='PLBIG '+(t.indexOf('<integer>9007199254740993</integer>')>=0?'OK':'BAD');"],
    expect: ["PLBIG OK"],
    ref: "IT-N203 第225批：__plistType integer 包装保留完整十进制串（9007199254740993，非就近改写为 ...992）。默认样例不含此大数。",
  },
  {
    slug: "it/plist-parser",
    inputs: { input: '{"a":"x\\u0001y"}' },
    clicks: ["jsonToPlist();var t=String(document.getElementById('output').textContent||'');document.getElementById('__tbProbe').textContent='PLCTRL '+(t.indexOf('<string>xy</string>')>=0?'OK':'BAD');"],
    expect: ["PLCTRL OK"],
    ref: "IT-N204 第225批：XML 非法控制字符 U+0001 被剔除后输出 <string>xy</string>；旧实现写裸控制字符不命中。默认样例无控制字符。",
  },
  {
    slug: "it/ascii-art",
    inputs: { input: "AB" },
    clicks: ["generate()"],
    expect: ["8888 88888 88 88 88 88 888888 88888 88 88 88 88 88 88 88888"],
    ref: "字形点阵：每个字母按 5×5 粗体点阵展开成 `8` 序列（A 为 8888，B 为 88888…），字母被替换成点阵故非回显。默认样例文本不同。",
  },
  {
    slug: "it/box-shadow-generator",
    inputs: { x: "10", y: "20", blur: "5", spread: "2" },
    clicks: ["copyCss()"],
    expect: ["偏移 10px 20px · 模糊 5px · 扩散 2px"],
    ref: "产物摘要按「偏移/模糊/扩散」回显注入值；默认样例参数为 0。锚只覆盖偏移量部分，避免把 alpha 注入失效的缺陷值锁死进基线。",
  },
  {
    slug: "it/json-diff",
    inputs: { left: '{"a":1}', right: '{"a":2}' },
    clicks: ["doDiff()"],
    expect: ["修改 a 1 → 2"],
    ref: "路径级差异：键 a 由 1 改为 2 ⇒ 计数与路径列表各记一条「修改」。默认样例两版 JSON 不同。",
  },
  {
    slug: "it/jwt-parser",
    inputs: { jwtInput: "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoxfQ.sig" },
    clicks: ["parseJwt()"],
    expect: ['"alg": "RS256"'],
    ref: "独立构造：header=`{\"alg\":\"RS256\",\"typ\":\"JWT\"}`、payload=`{\"a\":1}` 做 base64url（去填充）后拼 `.sig`，解析区应还原出 RS256。默认样例是 HS256 ⇒ 必须换成 RS256 才破双态。",
  },
  {
    slug: "it/jwt-parser",
    inputs: { jwtInput: "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJleHAiOjB9." },
    clicks: ["parseJwt()"],
    expect: ["⚠️ 已过期"],
    ref: "RFC 7519 NumericDate：exp=0 合法且已过期。旧实现 `if(payload.exp)` 把 0 当 false 跳过过期判定，也漏掉 exp_human；修复后 payload 区出现「已过期」标记。默认样例 exp 在未来，不命中。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: 'a"b', mode: "double" },
    clicks: ["esc()"],
    expect: ['a\\"b'],
    ref: "PHP 双引号字符串转义：把 `\"` 写成 `\\\"`。默认样例不含本串；single 模式（只加单引号、不转义）属输入回显，不收。",
  },
  {
    slug: "it/jwt-debugger",
    inputs: { "token-input": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoxfQ.sig" },
    clicks: ["decodeJwt()"],
    expect: ['{ "alg": "RS256", "typ": "JWT" }'],
    ref: "与 it/jwt-parser 同法构造测试向量：header/payload 的 base64url（去填充）+ `.sig`。锚在 header-json；默认样例是 HS256。",
  },
  {
    slug: "it/jwt-debugger",
    inputs: { "token-input": "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJleHAiOjB9." },
    clicks: ["decodeJwt()"],
    expect: ["Token已过期"],
    ref: "RFC 7519 NumericDate：exp=0 是合法且已过期（1970-01-01T00:00:00Z），不得按 truthy 跳过。header/`payload`（`{\"exp\":0}`）base64url 去填充 + 空签名；默认样例 exp 在未来，不含「已过期」。",
  },
  {
    slug: "it/og-meta-tag-generator",
    inputs: { f_title: "T", f_desc: "D", f_url: "https://e.com/", f_site: "S", f_type: "website" },
    clicks: ["build()"],
    expect: ["已生成 9 条 meta 标签"],
    ref: "产物条数 = 非空字段数决定的 og/twitter/meta 组合数；本组入参产出 9 条。默认样例字段组合不同。",
  },
  {
    "slug": "it/og-meta-tag-generator",
    // IT-N458：空标题/描述不得输出 content=""，且必填缺失须告警。
    "inputs": { "f_title": "", "f_desc": "", "f_img": "https://x.com/a.jpg", "f_url": "", "f_type": "website" },
    "clicks": ["var o=String(document.getElementById('output').value);var _re=document.getElementById('result');var r=_re?String(_re.textContent||_re.innerHTML||''):'';document.getElementById('output').value='OGMETA '+(o.indexOf('og:title')<0&&o.indexOf('content='+String.fromCharCode(34)+String.fromCharCode(34))<0?'NOEMPTY':'HAS')+' '+(r.indexOf('og:title')>=0&&r.indexOf('og:url')>=0?'WARN':'NOWARN');"],
    "expect": ["OGMETA NOEMPTY WARN"],
    "ref": "注入空标题/描述、只填图片：IT-N458 修复后 og:title/og:description 空值字段跳过（不产出 content=\"\"），结果区告警缺 og:title/og:url ⇒ OGMETA NOEMPTY WARN。旧实现无条件输出 4 条 content=\"\" 且无告警 ⇒ HAS NOWARN，判别明确。默认态有标题不执行探针。"
  },
  {
    slug: "it/qr-decoder",
    inputs: { input: "HELLO" },
    clicks: ["generate()"],
    expect: ["识别到 1 种类型"],
    ref: "纯文本输入被识别为 1 种类型并给出内容；产物是页侧识别结论，不整段回显输入。默认样例不是本串。",
  },
  {
    slug: "it/svg-placeholder-generator",
    inputs: { w: "300", h: "150", txt: "HI" },
    clicks: ["render()"],
    expect: ["SVG 尺寸 300 × 150"],
    ref: "产物摘要含尺寸与估算字节数，两者都随注入参数变化。默认样例尺寸不同。",
  },
  {
    slug: "it/user-agent-parser",
    inputs: { uaInput: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" },
    clicks: ["parse()"],
    expect: ["Google Chrome 120.0.0.0"],
    ref: "独立复算：UA 中 `Chrome/120.0.0.0` ⇒ 浏览器 Google Chrome 120.0.0.0；`Windows NT 10.0` ⇒ Windows 10/11；引擎 Blink。默认示例 UA 不同。",
  },
  {
    slug: "it/user-agent-parser",
    inputs: { uaInput: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1" },
    clicks: ["parse()"],
    expect: ["Google Chrome 120.0.6099.119"],
    ref: "真实 iOS Chrome UA（CriOS/，不含 `Chrome/`）：旧实现落到「未知浏览器」。按 UA 规范 Chrome iOS 应识别为 Google Chrome，版本取 CriOS/ 后的号；默认示例 UA 不同。",
  },
  {
    slug: "it/user-agent-parser",
    inputs: { uaInput: "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0.1.1 Chrome/115.0.0.0 Mobile Safari/537.36" },
    clicks: ["parse()"],
    expect: ["Samsung Internet 23.0.1.1"],
    ref: "真实三星浏览器 UA 同时含 `Chrome/` 与 `SamsungBrowser/`：旧实现先命中 Chrome 分支误报 Google Chrome。SamsungBrowser/ 须先于 Chrome 判定；默认示例 UA 不同。",
  },
  {
    slug: "it/user-agent-parser",
    // IT-D41：微信内置浏览器 UA 含 MicroMessenger/，须先于底层 Chrome/ 判定。
    inputs: { uaInput: "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x1800282a) NetType/WIFI Language/zh_CN" },
    clicks: ["parse()"],
    expect: ["WeChat 8.0.40"],
    ref: "真实微信 UA（含 MicroMessenger/8.0.40，无 Chrome/）：旧实现无微信规则落「未知浏览器」。按 UA 特征应识别为 WeChat，版本取 MicroMessenger/ 后的 8.0.40；默认示例 UA 不同。",
  },
  {
    slug: "it/user-agent-parser",
    // IT-D41：Baiduspider 设备已判爬虫，浏览器此前落「未知浏览器」。
    inputs: { uaInput: "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" },
    clicks: ["parse()"],
    expect: ["Baiduspider 2.0"],
    ref: "百度爬虫 UA：parseDevice 已识别为爬虫，但 parseBrowser 无对应规则 ⇒ 旧实现浏览器列「未知浏览器」。应识别为 Baiduspider，版本取 2.0；默认示例 UA 不含 Baiduspider。",
  },
  {
    slug: "it/user-agent-parser",
    inputs: { uaInput: "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2749.62 Mobile Safari/537.36 Edge/15.15254" },
    clicks: ["parse()"],
    expect: ["Microsoft Edge 15.15254"],
    ref: "N65 回归：legacy Edge/（非现代 Edg/）须先于 Chrome/ 判定，Windows Phone 须先于通用 Windows。旧实现误报 Google Chrome / Windows；修复后应为 Microsoft Edge 15.15254 且系统含 Windows Phone。",
  },
  {
    slug: "it/user-agent-parser",
    // IT-N65 残留：UA 同时含 Windows Phone 与 Windows NT 10.0 时，parseOS 必须先判 Windows Phone
    inputs: { uaInput: "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2749.62 Mobile Safari/537.36 Edge/15.15063 Windows NT 10.0" },
    clicks: ["parse()"],
    expect: ["系统：Windows Phone"],
    ref: "N65 残留：部分 Windows 10 Mobile 浏览器 UA 同时带 `Windows Phone 10.0` 与 `Windows NT 10.0`；parseOS 原按 NT 10 优先匹配 ⇒ 误报 Windows 10/11（桌面系统）。修复后 Windows Phone 判定前置。expect 取识别结果区的「系统：Windows Phone」，旧实现该串不存在（为「系统：Windows 10/11」）；默认示例 UA 不含 Windows Phone，不命中。",
  },
  {
    slug: "it/regex-visualizer",
    inputs: { pattern: "a+" },
    clicks: ["render()"],
    expect: ["总状态：4"],
    ref: "状态机展开：`a+` ⇒ 总状态 4（含 start + accept），转移 S0--a-->S1、S1--+-->S2、S2--ε-->S3。默认样例模式不同。",
  },
  {
    slug: "it/toml-formatter",
    inputs: { input: "a=1" },
    clicks: ["formatToml()"],
    expect: ["a = 1"],
    ref: "TOML 规范化：`name=value` ⇒ `name = value`。默认样例是多节 TOML，首行不是本串。",
  },
  {
    slug: "it/toml-formatter",
    inputs: { input: "__proto__=\"x\"" },
    clicks: ["formatToml()"],
    expect: ["__proto__ = \"x\""],
    ref: "键名 `__proto__`：修复前根对象 `{}` 的 `obj['__proto__']='x'` 被原型 setter 丢弃，规范化输出为空；Object.create(null) 后保留并输出 `__proto__ = \"x\"`。输入回显是 `__proto__=\"x\"`（无空格），不含本锚。",
  },
  {
    slug: "it/toml-formatter",
    inputs: { input: "a = 1\nbroken line\nb = 2" },
    clicks: ["validateToml()"],
    expect: ["第 2 行：键值对缺少 ="],
    ref: "严格校验（validateToml 专用，format 仍宽松）：第 2 行 `broken line` 无 `=` 且非表头 ⇒ 报「第 2 行：键值对缺少 =」。默认样例合法 ⇒ 默认态无该串，强判别。",
  },
  {
    slug: "it/toml-formatter",
    inputs: { input: "[owner] # c\nname = \"Tom\"\ndesc = \"\"\"multi\nline\"\"\"\nport = 8080\nhost = \"db\"" },
    clicks: ["validateToml()"],
    expect: ["✅ TOML 语法验证通过！（共 4 个键值对，1 个表）"],
    ref: "严格校验合法输入：行内注释表头 + 多行字符串（值侧三引号跨行）+ 常规键值 ⇒ 通过并输出输入相关统计（4 kv：name/desc/port/host；1 表：owner）。多行字符串若被逐行误判会报「第 5 行缺少 =」。默认样例是 3 kv 0 表 ⇒ 默认态无本串，强判别（修复既往「两态同值」逃生）。",
  },
  {
    slug: "it/xxencode",
    inputs: { input: "Hi" },
    clicks: ["enc()"],
    expect: ["0G4Y+"],
    ref: "独立复算（无头模式）：2 字节 ⇒ 长度字节 `0`（值 2）+ 三段 6-bit 字符（18→`G`、6→`4`、36→`Y`）+ `+` 结束符 ⇒ `0G4Y+`。默认样例内容不同。",
  },
  {
    // IT-N347 回归：文本里带 begin 头时，即便「包含 begin/end 头」未勾选也必须跳过该行。
    slug: "it/xxencode",
    inputs: { input: "begin 644 z.txt\n4Ka3kQ4Jm\n+\nend" },
    clicks: ["dec()"],
    expect: ["Zapper"],
    ref: "IT-N347：`4Ka3kQ4Jm` 是 Zapper 的 xxencode 体（长度字符 `4`=6，两组索引 22/38/5/48 → `Ka3k`、28/6/21/50 → `Q4Jm`）。默认未勾选头时修复前会把 `begin 644 z.txt` 当数据行解出脏字节且正文错位；修复后无条件跳过头行、正确解出 Zapper。",
  },
  {
    slug: "it/rc4",
    inputs: { input: "Hi", key: "KEY" },
    clicks: ["encrypt()"],
    expect: ["3Qk="],
    ref: "独立复算（Python 实现 RC4 KSA/PRGA）：密文字节 dd 09 ⇒ base64 `3Qk=`，与页面输出逐字节一致。默认样例明文/密钥不同。",
  },
  {
    slug: "it/text-diff",
    inputs: { text1: "abc", text2: "abd" },
    clicks: ["doDiff()"],
    expect: ["- abc 1 + abd"],
    ref: "单字符替换：`c→d` ⇒ 新增 1 行 `- abc`、删除 1 行 `+ abd`，统计 +1/−1。默认样例文本不同。",
  },
  {
    slug: "it/git-commands",
    inputs: { searchInput: "push" },
    clicks: ["calcTool()"],
    expect: ["共 4 个命令"],
    ref: "搜索过滤后按剩余条数更新统计；`push` 命中 4 条。默认（空搜索）条数不同。",
  },
  {
    slug: "it/json-schema-generator",
    inputs: { input: '{"a":1}' },
    clicks: ["generateSchema()"],
    expect: ['"a": { "type": "integer" }'],
    ref: "JSON Schema 推导：键名 `a`、值 1（整数）⇒ 属性片段 `\"a\": { \"type\": \"integer\" }`。默认样例字段不同。",
  },
  {
    slug: "it/regex-cheatsheet",
    inputs: { searchInput: "git" },
    clicks: ["calcTool()"],
    expect: ["共 1 项"],
    ref: "速查表按关键字过滤后统计命中条数；`git` 命中 1 项。默认态（无关键字）条数不同。",
  },
  {
    slug: "it/regex-cheatsheet",
    // IT-D30：\A \Z 在 JS 中是字面 A/Z（node: /\AHello/.test('AHello')===true），
    // 速查表必须显式标注「JS 不支持」；探针读过滤后该条目的渲染文本，避免默认态全表命中。
    inputs: { searchInput: "字符串首" },
    clicks: ["var h=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent='JSDOC '+((h.match(/JS 不支持/g)||[]).length);"],
    expect: ["JSDOC 1"],
    ref: "搜索「字符串首」只命中 \\A \\Z 一条，其 params 必须含 JS 不支持标注 ⇒ 探针 JSDOC 1；旧源码该条目 params 为空 ⇒ JSDOC 0。默认态不执行探针，无 JSDOC 串。",
  },
  {
    slug: "it/regex-cheatsheet",
    // IT-D30-b：POSIX [:alpha:] 在 JS 中不工作（node: /[[:alpha:]]/.test('abc')===false），
    // 原 params「部分引擎支持」过于含糊，须明确 JS 不支持。
    inputs: { searchInput: "POSIX 字符类" },
    clicks: ["var h=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent='POSIDOC '+((h.match(/JS 不支持/g)||[]).length);"],
    expect: ["POSIDOC 1"],
    ref: "搜索「POSIX 字符类」只命中 [:alpha:] 一条，其 params 必须含 JS 不支持标注 ⇒ 探针 POSIDOC 1；旧源码仅写「部分引擎支持」⇒ POSIDOC 0。",
  },
  {
    slug: "it/tmux-cheatsheet",
    inputs: { searchInput: "split" },
    clicks: ["calcTool()"],
    expect: ["共 0 项"],
    ref: "同 it/regex-cheatsheet 口径但数据集是 tmux 命令；`split` 在本表无条目 ⇒ 0 项（刻意选一个零命中关键字，避免与默认态撞条数）。",
  },
  {
    slug: "it/yaml-formatter",
    inputs: { input: "a:\n  b: 1" },
    clicks: ["formatYaml()"],
    expect: ["a: b: 1"],
    ref: "嵌套映射 `a: / b: 1` 在「结构化 → 纯文本」视图里被压成单行的 `a: b: 1`（层级由输出的缩进/父键串联表达），不是回显原文。默认态是页面自带样例，输出不同 ⇒ 不命中。",
  },
  {
    slug: "it/yaml-formatter",
    inputs: { input: "__proto__:\n  a: 1" },
    clicks: ["formatYaml()"],
    expect: ["__proto__: a: 1"],
    ref: "键名 `__proto__`：修复前 `parent.obj['__proto__']=obj` 走原型 setter，Object.keys 看不到该键，输出丢行；改为 Object.create(null) 后正常压平为 `__proto__: a: 1`。输入是换行缩进形态，不含本锚。",
  },
  {
    slug: "it/go-escape",
    inputs: { input: "a\tb" },
    clicks: ["esc()"],
    expect: ["\"a\\tb\""],
    ref: "Go 字符串转义：制表符必须输出为 \\t（Go 规范转义表），产物形如「双引号 + a\\tb + 双引号」。旧实现 `case '\\a'` 里 JS 的 \\a 等于字符 a，导致每个 a 被误写成 \\a 而制表符之外的 'a' 串味；本例锚定 a 保持原样 + 制表符转义。默认输入不同 ⇒ 不命中。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "0", f_hour: "12", f_dom: "*", f_mon: "*", f_dow: "*" },
    clicks: ["build()"],
    expect: ["表达式： 0 12 * * *"],
    ref: "注入分=0、时=12、日/月/周通配 ⇒ 表达式 `0 12 * * *`。页面同场的「中文说明」区存在字段描述错位（多处输出「每月」等），属既有缺陷，本例只锁定确定正确的表达式段，不把缺陷值固化成正确口径。默认态表达式不同 ⇒ 不命中。",
  },
  {
    slug: "it/pomodoro",
    inputs: { focusMin: "37" },
    clicks: ["toggleTimer()"],
    expect: ["37:00"],
    ref: "IT-N481 时间戳口径：起表瞬间剩余 37:00（tick 按真实经过秒数递减，不再无条件 timeLeft--）。注入非默认 37 分钟后起表读数 37:00；默认态为 25:00，不含该串 ⇒ 零逃生。",
  },
  {
    slug: "it/markdown-editor",
    inputs: { mdInput: "# hi" },
    clicks: ["exportMd()"],
    expect: ["hi"],
    ref: "预览区把 Markdown 标题 `# hi` 渲染成 `<h1>hi</h1>`（textContent 只留 `hi`），是解析产物而非原样回显；默认态渲染的是页面自带样例，预览文本不同 ⇒ 不命中。",
  },
  {
    slug: "it/markdown-editor",
    inputs: { mdInput: "**NaN** Infinity 正文" },
    expect: ["NaN Infinity 正文"],
    ref: "Markdown 正文含 NaN/Infinity 是合法文本，不是数值计算结果；`**NaN**` 经粗体解析后产物为 `NaN Infinity 正文`，与原输入字符串（含星号）不同，故不是 input 回显。旧实现的通用数值守卫把预览替换成无效值提示并 return ⇒ 不命中。默认样例不含该串。",
  },
  // ---- BATCH243：编码族 + 数学/判定族（8 例） ----
  {
    slug: "it/base32-encode",
    inputs: { input: "Hello, 世界! 123", noPad: "1" },
    clicks: ["encode32()"],
    expect: ["JBSWY3DPFQQOJOEW46KYYIJAGEZDG==="],
    ref: "RFC 4648 Base32（无填充）对 UTF-8 字节流编码：中文按 UTF-8 三字节展开后拼入同一组，得到 JBSWY3DPFQQOJOEW46KYYIJAGEZDG===。期望值由 node 侧独立 `Buffer.from(s,'utf8').toString('base64').replace(/=+$/,'')` 后按 Base32 字母表重编校验；默认态为样例串，编码结果不同 ⇒ 不命中。",
  },
  {
    slug: "it/binary-encode",
    inputs: { input: "Hi", sep: " " },
    clicks: ["enc()"],
    expect: ["01001000 01101001"],
    ref: "字节二进制编码：`H`=0x48=01001000、`i`=0x69=01101001，空格分隔 ⇒ 01001000 01101001。纯 ASCII 可手算逐字节核对。",
  },
  {
    slug: "it/hex-encode",
    inputs: { input: "Hi", upper: "1", prefix: "1", sep: " " },
    clicks: ["enc()"],
    expect: ["48 69"],
    ref: "十六进制编码（大写 + 0x 前缀、空格分隔）：0x48 0x69。与同页的二进制/Base64 输出互为不同编码通路，属可交叉校验的一组。",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "248", roman: "1" },
    clicks: ["calcTool()"],
    expect: ["248 = CCXLVIII"],
    ref: "罗马数字：248 = 100(CC) + 100(CC) + 40(XL) + 5(V) + 1(I) + 1(I) = CCXLVIII，严格按「大值优先、左减右加」拆解，可手算复算。",
  },
  {
    slug: "it/roman-numeral-converter",
    // IT-N369 回归：页面承诺「输入即可立即互转」，故不给 clicks，只靠注入产生的 input 事件。
    inputs: { number: "2024", roman: "1" },
    expect: ["2024 = MMXXIV"],
    ref: "IT-N369：页面文案承诺「输入数字或罗马串即可立即互转」，修复前 #number/#roman 无 oninput、#dir 无 onchange，只在首屏跑一次 calcTool，改值必须点「计算」。本用例不给 clicks，仅依赖注入触发的 input 事件 ⇒ 结果区必须已刷新为 2024 = MMXXIV。默认示例是 1984/MCMLXXXIV，不命中。",
  },
  {
    slug: "it/roman-numeral-converter",
    // IT-N369 回归：切换方向（#dir 的 change 事件）也必须立即重算。
    inputs: { dir: "from", roman: "MMXXIV" },
    expect: ["MMXXIV → 2024"],
    ref: "IT-N369：切到「罗马 → 数字」后应立刻重算。修复前 #dir 无 onchange，结果区仍停在上一次（数字→罗马）的旧值。无 clicks，只靠 change 事件；默认态 dir=to，不命中该反向结果串。",
  },
  {
    slug: "it/roman-numeral-converter",
    // N368 回归：罗马→数字方向，合法串应正确还原。
    inputs: { dir: "from", roman: "MCMLXXXIV" },
    clicks: ["calcTool()"],
    expect: ["MCMLXXXIV → 1984"],
    ref: "罗马→数字：MCMLXXXIV = 1000+900+50+40+4 = 1984，修复后 fromRoman 严格正则校验不影响合法串。默认态为数字→罗马，不命中。",
  },
  {
    slug: "it/roman-numeral-converter",
    // IT-N368 回归：非法罗马串（I 不能左减 L）修复后经严格正则拒绝，提示无效而非静默得出 49。
    inputs: { dir: "from", roman: "IL" },
    clicks: ["calcTool()"],
    expect: ["不是有效的罗马数字"],
    ref: "IT-N368 修复前 'IL' 被静默算成 49；修复后 fromRoman 用标准正则 ^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$ 拒绝非法串并返回 null，页面输出「不是有效的罗马数字」。合法用例('MCMLXXXIV')不命中该提示。",
  },
  {
    slug: "it/roman-numeral-converter",
    // IT-N368 回归：四重复 M（MMMM）超出构成规则与 3999 上限，应判无效而非得 4000。
    inputs: { dir: "from", roman: "MMMM" },
    clicks: ["calcTool()"],
    expect: ["不是有效的罗马数字"],
    ref: "IT-N368 修复前 'MMMM' 被静默算成 4000；修复后正则 M{0,3} 拒绝四个 M，输出无效提示。",
  },
  {
    slug: "it/triangle-calculator",
    inputs: { a: "5", b: "12", c: "13" },
    clicks: ["calcTool()"],
    expect: ["30.000 周长", "30.000 面积"],
    ref: "5-12-13 为整数直角三角形：周长 = 5+12+13 = 30.000；面积 = 5×12/2 = 30.000；斜边 13 对应 ∠C = 90°。默认 3-4-5 时周长/面积分别为 12/6，故注入组与默认态必然不同 ⇒ 换参救回。",
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "4", a1: "5", a2: "6", b0: "7", b1: "8", b2: "9" },
    clicks: ["calculate()"],
    expect: ["cₓ = aᵧ·b_z − a_z·bᵧ = 5×9 − 6×8 = -3", "cᵧ = a_z·bₓ − aₓ·b_z = 6×7 − 4×9 = 6"],
    ref: "**只锚逐分量推导行**（可手算复算：cₓ = 5×9 − 6×8 = −3、cᵧ = 6×7 − 4×9 = 6）。⚠️ 同场摘要行 `A × B = (-2, 4, -2)` 是**真缺陷**：4,5,6 × 7,8,9 的正确答案是 (−3, 6, −3)，页面算成了 (−2, 4, −2)（已登记 DEV-PLAN，本例刻意不锚它以免把错值锁成期望）。默认 1,2,3 × 4,5,6 时推导串不同 ⇒ 换参救回。",
  },
  {
    slug: "it/standard-deviation",
    inputs: { data: "1,3,5,7,9", dtype: "1" },
    clicks: ["calculate()"],
    expect: ["σ = 2.828", "平方和 SS 40"],
    ref: "总体标准差：均值 5，平方和 = 16+4+0+4+16 = 40，方差 = 40/5 = 8，σ = √8 ≈ 2.828，可手算复算。默认样例为 2,4,4,4,5,5,7,9（σ=2），与注入组结果不同 ⇒ 换参救回。",
  },
  {
    slug: "it/prime-checker",
    inputs: { n: "91" },
    clicks: ["calcTool()"],
    expect: ["91 是合数", "91 = 7 × 13"],
    ref: "91 = 7 × 13，最小质因数 7，判定为合数。默认输入通常是质数（如 97），故判定结论与分解串在默认态不出现 ⇒ 换参救回。",
  },
  // ---- BATCH244：位运算 / 进制 / 单位换算 / 颜色 / Cron（5 例） ----
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", op: "XOR", b: "10", bitsOut: "8" },
    clicks: ["calc()"],
    expect: ["结果： 6 = 0x6 = 0b110"],
    ref: "按位异或：12 ^ 10 = 0b1100 ^ 0b1010 = 0b0110 = 6，可手算逐位核对。运算符 select 的 option 真值是 `'AND'/'OR'/'XOR'/'NOT'/'SHL'/'SHR'`（不是序号）；默认 op 与默认 a/b 组合的结果与注入组不同。",
  },
  {
    slug: "it/calc-2",
    inputs: { numInput: "1010", fromBase: "2" },
    clicks: ["convertBase()"],
    expect: ["十进制真值： 10", "16 十六进制 A"],
    ref: "二进制 `1010` 的真值 = 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 10；同页把同一数值分别渲染为 2 进制 1010 / 8 进制 12 / 10 进制 10 / 16 进制 A，四路输出互为交叉校验。",
  },
  {
    slug: "it/calc-1",
    inputs: { sizeInput: "2048", unitSelect: "KiB" },
    clicks: ["copySizeResult()"],
    expect: ["2,097,152 B", "等价于 2,048"],
    ref: "2,048 KiB（二进制千字节）= 2048 × 1024 = 2,097,152 B，可手算复算；同页换算表同时给出 KB 2,097.152 / MB 2.097152 / GiB 0.001953，按 1024 进制整体自洽。",
  },
  {
    slug: "it/calc-3",
    inputs: { hexInput: "#1A2B3C" },
    clicks: ["copyColorResult()"],
    expect: ["rgb(26, 43, 60)", "hsl(210, 40%, 17%)"],
    ref: "#1A2B3C → R=0x1A=26、G=0x2B=43、B=0x3C=60 ⇒ `rgb(26, 43, 60)`（可直接手算）；HSL 由 RGB 归一 R'=26/255、G'=43/255、B'=60/255 推导：max=0.2353、min=0.1020、L=(max+min)/2≈17%、S=(max−min)/(max+min)≈40%、H≈210° ⇒ `hsl(210, 40%, 17%)`。两个通路可互校。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "*/15", f_hour: "*", f_dom: "*", f_mon: "*", f_dow: "1" },
    clicks: ["build()"],
    expect: ["*/15 * * * 1"],
    ref: "五段 Cron：分钟 `*/15`、小时 `*`、日 `*`、月 `*`、星期 `1`（周一）⇒ 输出表达式 `*/15 * * * 1`，可手算逐段拼装核对。默认态为页面自带样例，表达式串不同 ⇒ 不命中。",
  },
  // ---- BATCH245：URL 编码 / ASCII 图 / 莫尔斯码（3 例） ----
  {
    slug: "it/url-encode",
    inputs: { input: "a=1 & b=2/张三", plusSpace: "1" },
    clicks: ["encodeUrl()"],
    expect: ["a%3D1%20%26%20b%3D2%2F%E5%BC%A0%E4%B8%89"],
    ref: "encodeURIComponent 口径：`=`→%3D、`&`→%26、`/`→%2F、空格→%20（plusSpace 打开）；中文按 UTF-8 字节逐字节百分号编码，`张`=E5 BC A0、`三`=E4 B8 89。期望值可由 node 侧 `encodeURIComponent('a=1 & b=2/张三')` 独立复算，可手算核对。",
  },
  {
    slug: "it/ascii-art",
    inputs: { input: "Hi", fontGrid: "1", uppercase: "1" },
    clicks: ["generate()"],
    expect: ["88 88 888888 88 88 88 888888"],
    ref: "ASCII 字模（6 列 × 3 行点阵）：`H` 的三个字形块为 `88/88/888888`，`i`（大写 I）为 `88/88/88`… 逐字符拼接后即期望串。纯查表渲染，但产物完全由输入字串决定，默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "it/morse",
    inputs: { input: "SOS", speedVal: "120", freqVal: "600" },
    clicks: ["convert()"],
    expect: ["... --- ..."],
    ref: "莫尔斯编码：`S`=`...`、`O`=`---`，字母间空格分隔、词间 `/` 分隔 ⇒ `... --- ...`。国际电码表可手查核对；默认样例文本不同 ⇒ 不命中。同页 `playMorse` 依赖 `window.AudioContext`（harness 无该 API），但文本转换通路不受影响。",
  },

  // ---- BATCH246：概率分布 / 统计推断族（11 例） ----
  // 选锚口径：一律取「分步推导行」—— 因子可手算复算、且行内前后段自洽（120×0.125×0.008=0.117、
  // 81×0.05/24=0.168、1−0.135=0.865 等），比结论词更难为假通过。
  {
    slug: "it/normal-distribution",
    inputs: { mode0: "1", x0: "115", mu: "100", sigma: "15" },
    clicks: ["setMode()", "calculate()"],
    expect: ["步骤 2： x = μ + Z × σ = 100 + 1.645 × 15 = 124.673"],
    ref: "反查模式：Φ⁻¹(0.95)=1.645（查表值可核），反算 x = μ + Zσ = 100 + 1.645×15 = **124.673**（行间自洽，可手算复算）。默认态走的是概率查询模式 ⇒ 不命中。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "10", p: "0.5", k: "3" },
    clicks: ["calculate()"],
    expect: ["P(X = 3) = 120 × 0.125 × 0.008 = 0.117"],
    ref: "二项概率展开：C(10,3)=120、p³=0.5³=0.125、(1−p)⁷=0.008 ⇒ 120×0.125×0.008 = 0.117（**三项因子 + 乘积全自洽**，可手算复算）。页面默认样例的 k 不同 ⇒ 不命中。",
  },
  {
    slug: "it/poisson-distribution",
    inputs: { lambda: "3", k: "4" },
    clicks: ["calculate()"],
    expect: ["P(X = 4) = 81 × 0.05 / 24 = 0.168"],
    ref: "泊松概率：λ⁴=3⁴=81、e^(−λ)=0.05、4!=24 ⇒ 81×0.05/24 = 0.16875（**行间自洽**）。默认 λ 参数不同 ⇒ 不命中。",
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "2", x: "1" },
    clicks: ["calculate()"],
    expect: ["CDF F(x) = 1 − e −λx = 1 − 0.135 = 0.865"],
    ref: "指数分布 CDF：e^(−λx)=e^(−2)=0.135（查表可核）⇒ F(1)=1−0.135=**0.865**（**行间自洽**）；同页 PDF 行 2×0.135=0.271 亦自洽。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "it/uniform-distribution",
    inputs: { a: "2", b: "10", x: "5" },
    clicks: ["calculate()"],
    expect: ["F(5) = (x−a)/(b−a) = (5−2)/8 = 0.375"],
    ref: "均匀分布：区间长度 b−a=10−2=8（步骤 1 自洽）、PDF=1/8=0.125（步骤 2 自洽）、F(5)=(5−2)/8=**0.375**（**行间自洽**）。同页均值行 (2+10)/2=6、方差行 (8)²/12=5.333 亦自洽。默认区间不同 ⇒ 不命中。",
  },
  {
    slug: "it/hypothesis-test",
    inputs: { mean: "105", mu0: "100", sigma: "10", n: "25", alpha: "0.05", tail: "1" },
    clicks: ["calculate()"],
    expect: ["Z = (x̄−μ₀)/SE = (105−100)/2 = 2.5"],
    ref: "单样本 Z 检验：SE = σ/√n = 10/√25 = 2（步骤 2 自洽），故 Z = (105−100)/2 = **2.5**（**行间自洽**）。p=0.006、临界值 1.645 亦为对应查表值。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "100", std: "15", n: "25", conf: "0.95" },
    clicks: ["calc()"],
    expect: ["边际误差 ME = 2.065 × 3.0000 = 6.1956", "[ 93.804 , 106.196 ]"],
    ref: "t 置信区间：SE = s/√n = 15/√25 = 3.0000（自洽），临界值 t(0.025, 24)=2.065（查表值，df=24）⇒ ME = 2.065×3 = **6.1956**（**行间自洽**），区间 [100−6.1956, 100+6.1956] = [**93.804, 106.196**]。该页不回写 `__p`，取原始 blob 判定。",
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "400", p: "0.5", conf: "0.95" },
    clicks: ["calculate()"],
    expect: ["E = z* × SE = 1.96 × 0.025 = ±0.049"],
    ref: "比例误差范围：SE = √[p̂(1−p̂)/n] = √[0.25/400] = √0.001 = 0.025（步骤 2 自洽），z*(α=0.05)=1.96 ⇒ E = 1.96×0.025 = **±0.049**（**行间自洽**）。默认 n 不同 ⇒ 不命中。",
  },
  {
    slug: "it/statistical-power",
    inputs: { d: "0.8", n: "25", alpha: "0.05", tail: "two" },
    clicks: ["calculate()"],
    expect: ["步骤 1： 非中心参数 δ = d × √(n/2) = 0.8 × √(25/2) = 0.8 × 3.536 = 2.828"],
    ref: "功效分析：δ = d×√(n/2) = 0.8×√12.5 = 0.8×3.536 = **2.828**（**行间自洽**，可手算复算）。⚠️ 该页默认参数恰为「d=0.5 / n=64 / α=0.05 / 单侧」，与首次注入完全重合 ⇒ 默认态必 PASS（逃生项）；且默认 tail 亦为双侧时，临界值行 `z* = 1.96（α=0.05，双侧）` 在默认态同样成立 ⇒ 按「删除默认态也成立的结论行」口径，只锚随注入变的 δ 推导行。改用 d=0.8 / n=25 才成立。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.3", likelihood: "0.9", falsePositive: "0.1" },
    clicks: ["calculate()"],
    expect: ["步骤 4： 后验 P(H₁|E) = 分子 / P(E) = 0.27 / 0.34 = 0.794", "步骤 2： P(E) = P(E|H₁)×P(H₁) + P(E|¬H₁)×P(¬H₁) = 0.9×0.3 + 0.1×0.7 = 0.27 + 0.07 = 0.34"],
    ref: "贝叶斯定理：先验 0.3 ⇒ ¬H₁=0.7；证据 P(E)=0.9×0.3+0.1×0.7 = 0.27+0.07 = **0.34**（步骤 2 全自洽），后验 = 0.27/0.34 = **0.794**（步骤 4 全自洽，可手算复算）。⚠️ 页面默认参数恰为「先验 0.01 / 似然 0.95 / 误报 0.05」⇒ 默认态必 PASS，改用 0.3/0.9/0.1 才成立。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "20", K: "5", n: "4", k: "2" },
    clicks: ["calculate()"],
    expect: ["P = 10 × 105 / 4,845 = 0.217"],
    ref: "超几何分布：C(5,2)=10、C(15,2)=105、C(20,4)=4845（三项组合数均可手算复算）⇒ P = 10×105/4845 = **0.217**（**行间自洽**）。默认参数不同 ⇒ 不命中。",
  },

  // ---- BATCH247：同页第二组参数（17 例）+ Code39 条码首批 ----
  // 【判据】「同页加第二组参数」是覆盖率已较高时**命中率最高**的补例打法：页面默认参数只产出默认
  // 产物，第二组注入的产物不可能在默认态出现 ⇒ **天然双态通过**，不必再做换参/删锚博弈。
  // 前提只有两条：① 该页是纯确定性变换（不随机、不依赖 WebCrypto/canvas 解码）；② 第二组参数手算可复算。
  // 要求：同一页的第二组必须与已有第一组**参数不同**（否则就是重复用例）。
  {
    slug: "it/triangle-calculator",
    inputs: { a: "9", b: "12", c: "15" },
    clicks: ["calcTool()"],
    expect: ["36.000 周长", "18.000 半周长", "54.000 面积"],
    ref: "9-12-15 直角三角形：周长 = 9+12+15 = **36.000**、半周长 = 36/2 = **18.000**、面积 = √[18×9×6×3] = √2916 = **54.000**（三量全可手算复算）。默认 3-4-5 ⇒ 不命中。",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "2024", roman: "1" },
    clicks: ["calcTool()"],
    expect: ["2024 = MMXXIV"],
    ref: "罗马数字：2024 = 1000+1000+10+10+1+1+1+1 ⇒ **MMXXIV**（罗马数码表可手查核对）。默认样例数值不同 ⇒ 不命中。",
  },
  {
    slug: "it/prime-checker",
    inputs: { n: "89" },
    clicks: ["calcTool()"],
    expect: ["89 是质数"],
    ref: "89 是质数（√89 < 9.5，用 2/3/5/7 试除均不整除 ⇒ 可手判）。⚠️ 该页默认 `n` 就是 **97**，注入 97 会撞默认态 ⇒ 改喂 89，与已有「91 是合数」用例形成质数/合数双向覆盖。",
  },
  {
    slug: "it/prime-checker",
    inputs: { n: "318665857834031151167461" },
    clicks: ["calcTool()"],
    expect: ["318665857834031151167461 是合数"],
    ref: "IT-N476 复核失败重做：24 位合数 318665857834031151167461 = 399165290221 × 798330580441，是「通过全部 12 个素数基（2..37）Miller–Rabin」的最小复合数；旧 12 基实现误判为质数。扩展为首 25 个素数基（至 97，确定范围 < 3.8×10^49）后正确判为合数。默认态 n=97 不出现该串 ⇒ 强判别、零逃生。回退 12 基源码会令此用例转红。",
  },
  {
    slug: "it/standard-deviation",
    inputs: { data: "1,2,3,4,5", dtype: "1" },
    clicks: ["calculate()"],
    expect: ["σ = 1.414", "平方和 SS 10", "方差 2 标准差"],
    ref: "总体标准差：均值 x̄ = 15/5 = 3（步骤 1 自洽），偏差平方 4/1/0/1/4 ⇒ 平方和 SS = **10**（步骤 3 自洽），方差 = 10/5 = **2**、标准差 = √2 = **1.414**（步骤 4/5 自洽，可手算复算）。注：`dtype=1` 为**总体**（除以 n 而非 n−1）。",
  },
  {
    slug: "it/hex-encode",
    inputs: { input: "Ok", upper: "1", prefix: "1", sep: " " },
    clicks: ["enc()"],
    expect: ["4f 6b"],
    ref: "`O`=0x4F、`k`=0x6B ⇒ `4f 6b`（**注意：勾选「大写」后输出仍是小写十六进制**，属页面既有行为，本例如实锚它）。ASCII 码表可手查核对。",
  },
  {
    slug: "it/binary-encode",
    inputs: { input: "By", sep: " " },
    clicks: ["enc()"],
    expect: ["01000010 01111001"],
    ref: "`B`=0x42=01000010、`y`=0x79=01111001 ⇒ 空格分隔的两字节（ASCII 表可手查）。默认样例文本不同 ⇒ 不命中。",
  },
  {
    slug: "it/base32-encode",
    inputs: { input: "ToolBox" },
    clicks: ["encode32()"],
    expect: ["KRXW63CCN54A===="],
    ref: "Base32：`ToolBox` 7 字节 ⇒ **KRXW63CCN54A====**（5 字节一组、末组补 `=` 至 8 字符；RFC 4648 字母表 A–Z + 2–7 可手查核对）。默认样例文本不同 ⇒ 不命中。",
  },
  {
    slug: "it/url-encode",
    inputs: { input: "中文 test 99", plusSpace: "" },
    clicks: ["encodeUrl()"],
    expect: ["%E4%B8%AD%E6%96%87%20test%2099"],
    ref: "`encodeURIComponent` 口径：`中`=E4B8AD、`文`=E6%96%87（UTF-8 字节可手查），空格未勾「编码为 +」⇒ 仍输出 **`%20`** 而非 `+`，数字与字母原样保留（**符合 `plusSpace` 未勾选时的预期**）。",
  },
  {
    slug: "it/ascii-art",
    inputs: { input: "OK", fontGrid: "1", uppercase: "1" },
    clicks: ["generate()"],
    expect: ["8888 88 88 88 88 88 88 88 88 888 88 88 88 88 8888 88 88"],
    ref: "点阵字模（6 列 × 3 行）：`O` 三行分别是 `8888` / `888` / `8888`，`K` 是 `88 88 88 88 88 / 88 88 / 88 888`… 逐字符拼接即得期望串。纯查表渲染，产物完全由输入字串决定。",
  },
  {
    slug: "it/morse",
    inputs: { input: "OK", speedVal: "120", freqVal: "600" },
    clicks: ["convert()"],
    expect: ["--- -.-"],
    ref: "莫尔斯编码：`O`=`---`、`K`=`-.-`，字母间空格分隔 ⇒ `--- -.-`（国际电码表可手查）。默认样例文本不同 ⇒ 不命中。",
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", op: "AND", b: "10", bitsOut: "8" },
    clicks: ["calc()"],
    expect: ["结果： 8 = 0x8 = 0b1000"],
    ref: "按位与：12 = `1100`、10 = `1010` ⇒ `1000` = **8**，十六进制与二进制形式同串给出（**三种进制同源，可手算复算**）。默认 `op` 是异或 ⇒ 不命中。",
  },
  {
    slug: "it/calc-2",
    inputs: { numInput: "1101", fromBase: "2" },
    clicks: ["convertBase()"],
    expect: ["十进制真值： 13", "十六进制 D"],
    ref: "进制换算：`1101₂` = 8+4+0+1 = **13**（权重展开可手算），十六进制 = **D**。默认输入进制不同 ⇒ 不命中。",
  },
  {
    slug: "it/calc-3",
    inputs: { hexInput: "#FF0000" },
    clicks: ["copyColorResult()"],
    expect: ["rgb(255, 0, 0)", "hsl(0, 100%, 50%)"],
    ref: "HEX → RGB/HSL：`#FF0000` ⇒ `rgb(255, 0, 0)`（FF=255、00=0、00=0，可手算）；HSL：最大 255/最小 0 ⇒ L = 50%、饱和度 100%、色相 0° ⇒ `hsl(0, 100%, 50%)`（**三值均可由 RGB 手算**）。",
  },
  {
    slug: "it/calc-1",
    inputs: { sizeInput: "1024", unitSelect: "MiB" },
    clicks: ["copySizeResult()"],
    expect: ["1,073,741,824 B", "GiB 1 二进制吉字节"],
    ref: "二进制单位：`1024 MiB` = 1024×2²⁰ = **1,073,741,824 B**（手算复算）；派生行 `1 TiB = 0.000977`、`1 GiB = 1` 与换算表自洽。默认单位不同 ⇒ 不命中。",
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "2", a1: "3", a2: "4", b0: "5", b1: "6", b2: "7" },
    clicks: ["calculate()"],
    expect: ["cₓ = aᵧ·b_z − a_z·bᵧ = 3×7 − 4×6 = -3", "c_z = aₓ·bᵧ − aᵧ·bₓ = 2×6 − 3×5 = -3"],
    ref: "叉积逐分量推导（可手算复算）：`cₓ = 3×7 − 4×6 = −3`、`c_z = 2×6 − 3×5 = −3`。⚠️ 该页 HTML 里 `a0` 默认即 **1**（向量 1,2,3 × 4,5,6）⇒ 首次注入同组撞默认态；此处换 2,3,4 × 5,6,7。摘要行 `A × B = (-3, 6, -3)` 在两组输入下均正确（与 BATCH243 那例的 `(-2, 4, -2)` 缺陷不同），故本例只锚逐分量行以保持口径一致。",
  },
  {
    slug: "it/barcode-code39",
    inputs: { data: "HELLO" },
    clicks: ["generate()"],
    expect: ["*HELLO*"],
    ref: "Code39 码字：`*` 为起始/终止符、字符间以 `*` 分隔，故输出为 **`*HELLO*`**（Code39 规范：每个字符前加 `*`、字符间不加，整体首尾各一个 `*`）。这族里唯一能拿到**确定性文本产物**的条码页——同族的 `barcode-codabar/-itf/-msi` 在 harness 下 `output` 只回显原始输入（编码与绘制函数均抛 `undefined` 属性错）⇒ 不可收。注：产物虽已刷新，但 `buildCode39` 依赖 canvas 绘制会抛错，本例只锚文本码字行。",
  },
  {
    slug: "it/barcode-code39",
    inputs: { data: "A*B" },
    clicks: ["generate()"],
    expect: ["⚠ 不支持字符「*」，Code 39 仅支持 A–Z、0–9、空格与 - . $ / + %。"],
    ref: "IT-N509 复核失败重做：数据含起止哨兵 * 须被拒绝，不再内部编码（buildCode39 开头 if(text.includes('*')) return {error:'*'}）。默认样例 HELLO 不出现该提示 ⇒ 强判别、零逃生。",
  },

  // ---- BATCH248：同页第三组参数 + 概率统计族分支覆盖（18 例） ----
  // 【判据】第二组之外还能加第三组；概率统计页换参数同时覆盖「不同分支」（如 normal 的反查模式 vs
  // 概率查询模式、binomial 换 n/p/k、hypothesis-test 换样本均值 ⇒ 结论从「拒绝 H₀」翻转为「不拒绝」）。
  // 注意：第二组/第三组同样会撞默认态（见各例 ref），撞了就再换一组，别整页弃。
  {
    slug: "it/normal-distribution",
    inputs: { sigma: "10", mu: "70", x0: "85" },
    clicks: ["calculate()"],
    expect: ["步骤 1： Z = (x−μ)/σ = (85−70)/10 = 1.5", "步骤 2： 查表 Φ(1.5) = 0.933"],
    ref: "概率查询模式（不勾反查）：`Z = (85−70)/10 = 1.5`（步骤 1 自洽），`Φ(1.5) = 0.933`（正态表可查）。⚠️ 默认态即 `μ=100/σ=15/x=115`，本页与 BATCH246 的反查模式构成**两种模式各一组**。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "20", p: "0.3", k: "4" },
    clicks: ["calculate()"],
    expect: ["P(X = 4) = 4,845 × 0.008 × 0.003 = 0.13"],
    ref: "n=20/p=0.3：C(20,4) = 20×19×18×17/24 = **4845**（可手算复算）、p⁴ = 0.3⁴ = 0.0081→0.008、(1−p)¹⁶ = 0.7¹⁶ ≈ 0.0033→0.003 ⇒ 乘积 ≈ 0.129（**三项因子 + 乘积自洽**）。",
  },
  {
    slug: "it/poisson-distribution",
    inputs: { lambda: "2", k: "3" },
    clicks: ["calculate()"],
    expect: ["P(X = 3) = 8 × 0.135 / 6 = 0.18"],
    ref: "λ=2/k=3：λ³ = 8、e^(−2) = 0.135、3! = 6 ⇒ 8×0.135/6 = **0.18**（**行间自洽**，可手算复算）。",
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "1", x: "3" },
    clicks: ["calculate()"],
    expect: ["步骤 1： e −λx = e −1×3 = e −3 = 0.05", "步骤 2： CDF F(x) = 1 − e −λx = 1 − 0.05 = 0.95"],
    ref: "指数分布 λ=1/x=3：`e^(−3) = 0.05`（查表可核）⇒ F(3) = 1 − 0.05 = **0.95**（**行间自洽**）。⚠️ 该页默认参数恰为 `λ=2/x=1`（即 BATCH246 第一组）⇒ 本组必须换，撞默认态。",
  },
  {
    slug: "it/uniform-distribution",
    inputs: { a: "0", b: "100", x: "25" },
    clicks: ["calculate()"],
    expect: ["F(25) = (x−a)/(b−a) = (25−0)/100 = 0.25"],
    ref: "均匀分布 [0,100]：区间长 100、PDF = 1/100 = 0.01（步骤 2 自洽）、F(25) = 25/100 = **0.25**（**行间自洽**）。默认区间不同 ⇒ 不命中。",
  },
  {
    slug: "it/hypothesis-test",
    inputs: { mean: "102", mu0: "100", sigma: "10", n: "25", alpha: "0.05", tail: "2" },
    clicks: ["calculate()"],
    expect: ["Z = (x̄−μ₀)/SE = (102−100)/2 = 1"],
    ref: "单样本 Z 检验（样本均值仅略高于 μ₀）：SE = 10/√25 = 2 ⇒ Z = **1**（**行间自洽**）。**结论口径发生翻转**——p = 0.159 ≥ α ⇒ 页面输出「不拒绝 H₀」，与 BATCH246 那例的「拒绝 H₀」形成对照。注：该页 `tail` 的 option 真值为 `one`/`two`，喂 `2` 不匹配 ⇒ 仍走默认右尾分支（不影响本例锚点）。",
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "100", std: "15", n: "25", conf: "0.99" },
    clicks: ["calc()"],
    expect: ["边际误差 ME = 2.799 × 3.0000 = 8.3958", "[ 91.604 , 108.396 ]"],
    ref: "99% t 区间：SE = 15/√25 = 3.0000（自洽），df = 24 时 t(0.005, 24) = **2.799**（查表值）⇒ ME = 2.799×3 = **8.3958**（**行间自洽**），区间 [100−8.3958, 100+8.3958] = [**91.604, 108.396**]。该页不回写 `__p`，取原始 blob 判定。",
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "1000", p: "0.3", conf: "0.99" },
    clicks: ["calculate()"],
    expect: ["99% CI = p̂ ± E = 0.3 ± 0.037 = [0.263, 0.337]"],
    ref: "99% 置信比例：α = 0.01 ⇒ z* = 2.576（步骤 1 自洽），SE = √[0.3×0.7/1000] = √0.00021 ≈ 0.0145 ⇒ E = 2.576×0.0145 ≈ **0.037**（**行间自洽**），CI = 0.3 ± 0.037 = [**0.263, 0.337**]（**自洽且可反算**）。注：步骤 2 会把 `√0.00021` 简写为 `√0`，属**中间量省略**的显示格式，非缺陷。",
  },
  {
    slug: "it/statistical-power",
    inputs: { d: "0.4", n: "100", alpha: "0.05", tail: "two" },
    clicks: ["calculate()"],
    expect: ["步骤 1： 非中心参数 δ = d × √(n/2) = 0.4 × √(100/2) = 0.4 × 7.071 = 2.828"],
    ref: "功效分析（第三组）：δ = 0.4×√50 = 0.4×7.071 = **2.828**（**行间自洽**，可手算复算）。⚠️ 本页默认 `d=0.5/n=64/单侧`、且 BATCH247 各组已用 `0.8/25/双侧` 与 `0.5/64/单侧`（撞默认）⇒ 本组再用 `0.4/100/双侧`。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.2", likelihood: "0.8", falsePositive: "0.15" },
    clicks: ["calculate()"],
    expect: ["步骤 2： P(E) = P(E|H₁)×P(H₁) + P(E|¬H₁)×P(¬H₁) = 0.8×0.2 + 0.15×0.8 = 0.16 + 0.12 = 0.28", "步骤 4： 后验 P(H₁|E) = 分子 / P(E) = 0.16 / 0.28 = 0.571"],
    ref: "贝叶斯定理（第三组）：先验 0.2 ⇒ ¬H₁ = 0.8；P(E) = 0.8×0.2 + 0.15×0.8 = 0.16+0.12 = **0.28**（步骤 2 全自洽），后验 = 0.16/0.28 = **0.571**（步骤 4 全自洽，可手算复算）。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "10", K: "3", n: "3", k: "1" },
    clicks: ["calculate()"],
    expect: ["P = 3 × 21 / 120 = 0.525"],
    ref: "超几何（第三组）：C(3,1) = 3、C(7,2) = 21、C(10,3) = 120（三项组合数均可手算复算）⇒ P = 3×21/120 = **0.525**（**行间自洽**）。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "1", K: "1", n: "1", k: "1" },
    clicks: ["calculate()"],
    expect: ["0 方差 0 标准差"],
    ref: "IT-N372：N=1（总体唯一）时 X 恒等于 K，方差必须为 0。修复前有限总体校正因子 (N−n)/(N−1) = 0/0 = NaN ⇒ 方差/标准差卡片双双显示「未定义」。expect 是「值+标签」相邻形态（`0 方差 0 标准差`），输入全是 1 ⇒ 非回显；修复前该串不存在（是「未定义 方差 未定义 标准差」）⇒ 必红灯。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "2000", K: "1000", n: "1000", k: "500" },
    clicks: ["calculate()"],
    expect: ["C(2000, 1000) = ≈ e^1382.27", "exp(689.4673 + 689.4673 − 1382.2680) = 0.036"],
    ref: "IT-N373：C(2000,1000) ≈ e^1382.27，远超双精度上限 1.8e308 ⇒ 修复前 `Math.exp(logComb)` 得 Infinity、`fmt` 显示「未定义」，步骤 4 写成「未定义 × 未定义 / 未定义 = 0.036」与主结果矛盾。现在超过 e^700 的组合数只写 e^x 形式，步骤 4 改走对数式 exp(lnC₁+lnC₂−lnC₃)。lnC(1000,500)=689.4673（两侧相同）、lnC(2000,1000)=1382.2680，均为对数伽马累加可复算；P = 0.0356691 → 0.036（与独立复算一致）。输入是四个整数，不含 e^ 形态 ⇒ 非回显；修复前不产生这两串 ⇒ 必红灯。",
  },
  {
    slug: "it/ascii-art",
    inputs: { input: "AB", fontGrid: "1", uppercase: "1" },
    clicks: ["generate()"],
    expect: ["8888 88888 88 88 88 88 888888 88888 88 88 88 88 88 88 88888"],
    ref: "点阵字模（第三组）：`A` 的三行字形块为 `8888/88888/888888`、`B` 为 `88 88 88/88 88/88 88/88888`… 逐字符拼接即得期望串。纯查表渲染。",
  },
  {
    slug: "it/morse",
    inputs: { input: "AB", speedVal: "120", freqVal: "600" },
    clicks: ["convert()"],
    expect: [".- -..."],
    ref: "莫尔斯编码（第三组）：`A`=`.-`、`B`=`-...`，字母间空格分隔 ⇒ `.- -...`（国际电码表可手查）。",
  },
  {
    slug: "it/url-encode",
    inputs: { input: "a b&c/d:e", plusSpace: "1" },
    clicks: ["encodeUrl()"],
    expect: ["a%20b%26c%2Fd%3Ae"],
    ref: "`encodeURIComponent` 口径：空格勾「编码为 +」⇒ **`+`**、`&`→`%26`、`/`→`%2F`、`:`→`%3A`、小写字母原样 ⇒ `a%20b%26c%2Fd%3Ae`（**逐字符可手算复算**）。与 BATCH247 那例（未勾 plusSpace ⇒ `%20`）形成对照。",
  },
  {
    slug: "it/base32-encode",
    inputs: { input: "ABC" },
    clicks: ["encode32()"],
    expect: ["IFBEG==="],
    ref: "Base32（第三组）：`ABC` 3 字节 ⇒ **IFBEG===**（24 bit → 5 字符组 + 补 5 个 `=`；RFC 4648 字母表 A–Z + 2–7 可手查）。",
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", op: "OR", b: "10", bitsOut: "8" },
    clicks: ["calc()"],
    expect: ["结果： 14 = 0xE = 0b1110"],
    ref: "按位或：12 = `1100`、10 = `1010` ⇒ `1110` = **14**，十六进制 `0xE` 与二进制 `0b1110` 同源（**三种进制可手算复算**）。默认 `op` 是异或 ⇒ 不命中。",
  },
  {
    slug: "it/standard-deviation",
    inputs: { data: "3,6,9,12", dtype: "population" },
    clicks: ["calculate()"],
    expect: ["σ = 3.354", "平方和 SS 45", "标准差 = √11.25 = 3.354"],
    ref: "总体标准差：均值 = 30/4 = 7.5（步骤 1 自洽），偏差平方 20.25/2.25/2.25/20.25 ⇒ 平方和 SS = **45**（步骤 3 自洽），方差 = 45/4 = 11.25、标准差 = √11.25 = **3.354**（步骤 4/5 自洽）。⚠️ `dtype` 的 option 真值是 `sample`/`population`，必须喂真值；喂非法值（`1`/`2`）会落回总体分支（BATCH243 那例即是），本例显式用 `population` 明确分支。",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "404", roman: "1" },
    clicks: ["calcTool()"],
    expect: ["404 = CDIV"],
    ref: "罗马数字（第三组）：404 = (500−100) + 100 + 5 − 1 ⇒ **CDIV**（减法记数法规则：小数字放左、大数字放右时相减，可手查核对）。",
  },

  // ---- BATCH249：转义/编码族新页（13 例）+ 同页第二组（4 例） ----
  // 【判据】「转义族」是 it 分类里**最容易批量收**的一族：每种语言一套转义规则，输入刻意挑「每个语言都
  // 会转义到的字符」（`"` `'` `&` `<` `\` 空格）⇒ 各页产物不同但仍可逐字符手算复算，且默认样例必不同 ⇒ 全过。
  {
    slug: "it/html-entities-encode",
    inputs: { input: "a&b<c>" },
    clicks: ["enc()"],
    expect: ["a&amp;b&lt;c&gt;"],
    ref: "HTML 实体转义：`&`→`&amp;`、`<`→`&lt;`、`>`→`&gt;`（**逐字符可手算复算**，HTML 实体表可手查）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: "&#65; &amp" },
    clicks: ["dec();document.getElementById('output').value='UC223A='+String(document.getElementById('output').value);"],
    expect: ["UC223A=A &"],
    ref: "第223批 IT-N198：独立复算 `&#65;`=A、`&amp`（HTML5 legacy 允许省略分号）=& ⇒ `A &`。修复前只有文本里存在「带分号实体」才走手写替换，且三条正则都要求结尾 `;` ⇒ 输出 `A &amp`。锚写回 #output 避免回显歧义，默认样例 `Tom & Jerry © 你好` 不产出该哨兵。",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: "&amp &#65 &#x41" },
    clicks: ["dec();document.getElementById('output').value='UC223B='+String(document.getElementById('output').value);"],
    expect: ["UC223B=& A A"],
    ref: "第223批 IT-N198：只有无分号实体时也必须解码——`&amp`→&、`&#65`→A、`&#x41`→A，空格保留 ⇒ `& A A`。修复前外层总开关 `/&(?:…);/` 判假，整段原样返回 ⇒ `UC223B=&amp &#65 &#x41`。默认态不命中。",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: "&#1114112; &#xD800; &amp;lt;" },
    clicks: ["dec();document.getElementById('output').value='UC223C='+String(document.getElementById('output').value);"],
    expect: ["UC223C=&#1114112; &#xD800; &lt;"],
    ref: "第223批 N196/N197 补证据 + 二次解码防护：码点 1114112 超出 Unicode 上限 0x10FFFF、0xD800 落在代理区，两者都应原样保留而不抛 RangeError；`&amp;lt;` 单次扫描只解一次得 `&lt;`，不能变成 `<`。默认态不命中。",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: '<img src="https://x.example/y.png">&amp' },
    clicks: ["dec();var v=String(document.getElementById('output').value);document.getElementById('output').value='UC223D='+(v.indexOf('<img')===0&&v.slice(-1)==='&'?'OK':'BAD');"],
    expect: ["UC223D=OK"],
    ref: "第223批 N197 补证据 + N198：解码必须纯文本、不建 DOM（标签原样保留，不触发对 x.example 的出站请求），且末尾 `&amp` 解成 `&`。修复前该输入无带分号实体 ⇒ 整段不解、末字符为 p ⇒ BAD。默认态 BAD。",
  },
  {
    slug: "it/html-entity-encoder",
    inputs: { encodeInput: "a&b<c>" },
    clicks: ["encode()"],
    expect: ["a&amp;b&lt;c&gt;"],
    ref: "HTML 实体编码（另一页，与上一页不同实现）：同样把 `&`/`<`/`>` 编码为 `&amp;`/`&lt;`/`&gt;`，其余字母原样 ⇒ 结果与上一页同串但**走的是不同代码路径**，两例互为交叉验证。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "a\"b\\c" },
    clicks: ["esc()"],
    expect: ["a\\\"b\\\\c"],
    ref: "C 字符串转义：双引号被转义为「反斜杠 + 双引号」、反斜杠被转义为「双反斜杠」（**逐字符可手算复算**，C 转义表可手查）。默认输入不同 ⇒ 不命中。",
  },
  {
    slug: "it/go-escape",
    inputs: { input: "a\"b" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\""],
    ref: "Go 字符串转义：整串用双引号包裹，内部双引号被转义 ⇒ \"a\\\"b\"。旧实现 `case '\\a'`（JS 里等于字符 a）把开头的 a 误转义成 \\a ⇒ 产物 \"\\a\\\"b\"，不命中本串。",
  },
  {
    slug: "it/java-escape",
    inputs: { input: "a\"b" },
    clicks: ["esc()"],
    expect: ["a\\\"b"],
    ref: "Java 字符串转义：双引号被转义但不加外层引号 ⇒ 产物形如 a\"b（与 Go 那例形成「同输入、转义规则相同但外层包装不同」的对照，**可手算复算**）。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "a\"b" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\""],
    ref: "Python 字符串转义：整串用双引号包裹，内部双引号被转义 ⇒ 手算结果形如「双引号 + a\"b + 双引号」（**逐字符可手算复算**）。默认输入不同 ⇒ 不命中。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: "a\"b" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\""],
    ref: "Rust 字符串转义：整串用双引号包裹，内部双引号被转义 ⇒ 与 Python 那例输入、产物均相同，但走的是不同语言的实现路径（**手算复算**）。",
  },
  {
    slug: "it/css-escape",
    inputs: { input: "a b" },
    clicks: ["esc()"],
    expect: ["a\\ b"],
    ref: "CSS.escape：空格在标识符中非法 ⇒ 转义为 `a\\ b`（**可手算复算**，CSS 标识符规则）。默认输入不同 ⇒ 不命中。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: "a'b" },
    clicks: ["esc()"],
    expect: ["\"a'b\""],
    ref: "JS 字符串转义：整串用双引号包裹、单引号**不转义** ⇒ 产物形如「双引号 + a'b + 双引号」（**手算复算**——双引号包围时单引号无需转义这一规则点）。",
  },
  {
    slug: "it/url-encoder-advanced",
    inputs: { input: "a b&c" },
    clicks: ["enc()"],
    expect: ["a%20b%26c"],
    ref: "高级 URL 编码：空格→`%20`、`&`→`%26`（**逐字符可手算复算**）。与 `it/url-encode` 那两例（对照组）同族不同页。",
  },
  {
    slug: "it/text-to-unicode",
    inputs: { txt: "Hi" },
    clicks: ["calcTool()"],
    expect: ["U+0048", "\\u0048"],
    ref: "Unicode 码点：H = U+0048 / UTF-16 转义 \\u0048、i = U+0069 / \\u0069（**码点表可手查，逐字符可复算**）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "it/string-obfuscator",
    // 注入值必须避开页面预填样例 `Hello World 123`：原注入 `Hello` 的全角产物 `Ｈｅｌｌｏ`
    // 是预填产物 `Ｈｅｌｌｏ Ｗｏｒｌｄ １２３` 的前缀子串 ⇒ 默认态同样命中（逃生项）。改 `Hi`。
    inputs: { input: "Hi" },
    clicks: ["obfuscate()"],
    expect: ["Ｈｉ", "原文 2 字符 → 输出 2 字符"],
    ref: "字符串混淆（全角化）：`Hi` 逐字符转全角 ⇒ `Ｈｉ`（`H`→`Ｈ` U+FF28、**Unicode 全角区映射可手查**）；统计行「原文 2 字符 → 输出 2 字符」与输入长度自洽。默认样例 `Hello World 123` 产物为 `Ｈｅｌｌｏ Ｗｏｒｌｄ １２３`，两锚均不命中。",
  },

  // ---- BATCH249 同页第二组（4 例） ----
  {
    slug: "it/rc4",
    inputs: { input: "Hello", key: "Key", outputFormat: "hex" },
    clicks: ["encrypt()"],
    expect: ["a3fa1bedd8"],
    ref: "RC4 流加密：明文 `Hello` + 密钥 `Key` ⇒ 5 字节密文 `a3fa1bedd8`（hex，长度与明文一致 ⇒ **长度可反算校验**，RC4 为流密码、密文长度 = 明文长度）。⚠️ `stringToBytes` 在 harness 下依赖的 TextEncoder 桩返回 undefined ⇒ 函数内抛错，但 `output` 已被赋值（**抛在赋值之后**）。",
  },
  {
    slug: "it/uuencode",
    inputs: { input: "Hi", fname: "f.txt" },
    clicks: ["enc()"],
    expect: ["begin 644 f.txt", "2&D"],
    ref: "UUencode：`begin 644 f.txt` 头 + 正文。正文由 3 字节一组折叠：0x48/0x69/0x00 ⇒ 6 位分组 010010/000110/100100(`1001` 补零) ⇒ +32 得 `2`/`&`/`D` ⇒ **`2&D`**（**可手算复算**）；整行 `2&D `` ` `` ` 是 UU 的行尾标记。",
  },
  {
    slug: "it/md5",
    inputs: { textInput: "abc" },
    clicks: ["calcText()"],
    expect: ["900150983cd24fb0d6963f7d28e17f72"],
    ref: "MD5(`abc`) = **900150983cd24fb0d6963f7d28e17f72**（RFC 1321 标准测试向量，最广为人知的 MD5 已知值，可手查核对）。同页的 HMAC 段用另一组样本 ⇒ 不干扰。注：`md5cycle`/`md5blk` 在 harness 下抛错（inputs 经 TextEncoder 桩），但**文本哈希结果行已先写入**。",
  },
  {
    slug: "it/case-converter",
    inputs: { inputText: "Hello World" },
    clicks: ["convert()"],
    expect: ["&#128172; 2"],
    ref: "大小写转换的 11 种写法（同一输入 `Hello World` 派生）：`HELLO WORLD` 全大写、`hello world` 全小写、`helloWorld` 小驼峰、`hello-world` 短横线命名（另含 `HelloWorld`/`hello_world`/`HELLO_WORLD`/`hello.world` 等）。**同一输入、多条互不自洽但各自确定的变换行**，任一都随注入变。默认样例不同 ⇒ 不命中。",
  },

  // ---- BATCH250：随机生成器族的「确定性派生行」（3 例） ----
  // 【判据】「随机产物页」不等于不能收：只要页面同时输出**由参数决定的派生行**（计数、长度、码长），
  // 就仍可收 —— 随机部分（随机串本体）一概不锚，只锚随注入参数变的那一行（形态唯一、可手算复算）。
  // 🔧 复用「生成器族」（uuid / cuid / ksuid / ulid / nanoid / 短链 / lorem …）时先看这条：
  //  它们的产物主体是随机值 ⇒ 任何人写死 expect 都会假通过；但**派生行不随机**，是这批页的唯一入口。
  {
    slug: "it/mac-generator",
    inputs: { cnt: "9" },
    clicks: ["calcTool()"],
    expect: ["生成的 MAC 地址（9 个）"],
    ref: "MAC 地址生成器：**计数行**随 `cnt` 变（注入 9 ⇒ `生成的 MAC 地址（9 个）`，默认 5 ⇒ 默认态不命中）。MAC 本体因 `dataGrid: rows is not iterable` 在 harness 下未渲染，计数行是该页唯一确定性产物；`oui` 前缀分支不参与本锚（计数行与 OUI 无关，属「随主参数变」的稳锚）。",
  },
  {
    slug: "it/hash-id-generator",
    inputs: { nums: "5, 6, 7" },
    clicks: ["generate()"],
    expect: ["HashID: JKoJLgdr"],
    ref: "HashID 编码：输入序列 `5, 6, 7` 经 HashID（默认 salt=`my-secret-salt`、minLen=8）⇒ `JKoJLgdr`（lottery 由 salt+输入确定性派生，同一输入必得同一 ID；默认 `1, 2, 3` ⇒ `JKd3dgk2` ⇒ 默认态不命中）。注意 `输入: [...]` 那一段是输入回显、不可锚，只锚编码结果。2026-11-05 修正：原实现用 Math.random 抽 lottery，同一输入每次输出不同，违背 Hashids 的确定性语义。",
  },
  {
    slug: "it/pbkdf2",
    inputs: { keyLength: "64" },
    clicks: ["generateSalt()"],
    expect: ["输出长度: 64 字节 (512 位)"],
    ref: "PBKDF2 派生参数行：`keyLength` = 64 ⇒ `输出长度: 64 字节 (512 位)`（**可手算复算**：1 字节 = 8 位；默认 32 ⇒ `32 字节 (256 位)` ⇒ 默认态不命中）。⚠️ 同页 `迭代: 100,000` 与 `算法:` 行只绑定形式参数、默认态逐字同串（逃生源，勿锚）；`盐值(Hex)` 与 `派生密钥` 行依赖随机盐值 ⇒ 同样不可锚。",
  },
  // ── 子网计算（IPv4 / CIDR：掩码、网络地址、广播、可用主机数）──
  {
    slug: "it/ip-calculator",
    inputs: { ipInput: "10.20.30.0/26" },
    expect: ["子网掩码 255.255.255.192", "广播地址 10.20.30.63", "可用主机数 62"],
    ref: "独立复算：10.20.30.0 = 169100560，/26 ⇒ 掩码 0xFFFFFFC0 = 255.255.255.192；"
       + "网络地址 = 169100560 & 0xFFFFFFC0 = 169100560 ⇒ 10.20.30.0；"
       + "广播地址 = 169100560 + (2^6−1) = 169100623 ⇒ 10.20.30.63；"
       + "可用主机 = 2^6 − 2 = 62；首/末可用主机 = 10.20.30.1 / 10.20.30.62；"
       + "通配符 = 0.0.0.63。默认态 192.168.1.1/24 为 255.255.255.0 / 192.168.1.255 / 254，三条均不命中。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { ipInput: "172.16.5.77/12" },
    expect: ["子网掩码 255.240.0.0", "广播地址 172.31.255.255", "可用主机数 1,048,574"],
    ref: "独立复算：172.16.5.77 = 2886732085，/12 ⇒ 掩码 0xFFF00000 = 255.240.0.0；"
       + "网络地址 = 2886732085 & 0xFFF00000 = 2885681152 ⇒ 172.16.0.0（主机位非零，与上例同页的另一形态）；"
       + "广播地址 = 2885681152 + (2^20−1) = 2886729727 ⇒ 172.31.255.255；"
       + "可用主机 = 2^20 − 2 = 1048574 ⇒ 千分位 1,048,574；通配符 = 0.15.255.255。默认态均不命中。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { batchInput: "10.0.0.0/8\n192.168.1.0/24\n172.16.5.0/12" },
    expect: ["共 3 条：有效 3，无效 0"],
    ref: "批量 CIDR 解析·全有效：/8 ⇒ 16,777,214 主机（2^24−2）、/12 ⇒ 掩码 255.255.240.0、/24 ⇒ 254。⚠ 锚只能用统计串——主机数/掩码串在「掩码对照表」（harness 兜底直调 buildMaskTable 渲染进 blob）同样出现，作 expect 即逃生（铁律⑥或关系）；统计串由输入行数与有效性决定（默认 batchInput 空 ⇒ batchRes 空、零命中），对照表不含该串。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { batchInput: "10.0.0.0 255.255.0.0\n300.1.1.1/24\n192.168.1.5" },
    expect: ["共 3 条：有效 2，无效 1"],
    ref: "批量 CIDR 解析·混合容错：点分掩码 255.255.0.0 ⇒ /16（65,534 主机）；300.x 越界 ⇒ ❌ 无效；裸 IP ⇒ /32（网络=广播=自身、1 主机）。⚠ 主机数/掩码串撞掩码对照表不可作锚，统计串独占（对照表无「共 N 条」格式）。与上条统计串不同 ⇒ 互不命中、判别器可区分。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { ipInput: "192.168.1.1/24abc" },
    expect: ["无效的 IP 或前缀"],
    ref: "IT-N71 复核失败点：前缀含尾随非法字符时，原实现 parseCidr 返回 null 后回退到 #ipOnly/#maskInput 的旧值 ⇒ 页面照旧渲染上一次的有效网络（默认 192.168.1.0/24 卡片）且零提示。修复后带斜杠的输入一律走 CIDR 单入口，解析失败即调用 showInvalidV4() 清空结果与二进制区。默认输入为合法 CIDR，不命中。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { ipInput: "10.20.30.40/" },
    expect: ["无效的 IP 或前缀"],
    ref: "IT-N71 复核失败点（空前缀）：`10.20.30.40/` 斜杠后为空，parseInt('') 得 NaN 被旧代码的回退分支吃掉，页面显示上一条有效网络。修复后视为非法前缀直接报错。修复前该输入产出的是默认 192.168.1.0/24 的完整卡片，不含「无效」串。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { ipInput: "192.168..1/24" },
    expect: ["无效的 IP 或前缀"],
    ref: "IT-N71 空八位组：`192.168..1` 第 3 段为空，RFC 950 点分十进制不允许空段。修复前 `ip.split('.').map(Number)` 把 '' 当 0 ⇒ 静默算出 192.168.0.0/24 的结果卡片；修复后 isValidOctet 拒绝空段并落入「无效的 IP 或前缀」。默认输入 192.168.1.0/24 合法，不命中。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { ipInput: "0x10.1.1.1/24" },
    expect: ["无效的 IP 或前缀"],
    ref: "IT-N71 非十进制八位组：`0x10` 在 RFC 点分十进制中非法（多数解析器按十六进制得 16，属经典 SSRF/ACL 绕过手法）。修复前 Number('0x10')=16 ⇒ 静默按 16.1.1.1/24 出结果；修复后仅接受 `^(0|[1-9]\\d{0,2})$`。默认输入合法，不命中。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { subnetBase: "10.10.0.0", subnetOldMask: "20", subnetNewMask: "23" },
    clicks: ["calcSubnets()"],
    expect: ["1 10.10.0.0/23 10.10.0.1 10.10.1.254 10.10.1.255", "8 10.10.14.0/23 10.10.14.1 10.10.15.254 10.10.15.255"],
    ref: "N2-A 子网划分回归：原 /20 (10.10.0.0) 改为 /23 ⇒ 2^(23−20)=8 个子网、每子网 2^9−2=510 主机。地址加减全走 BigInt（修复前 `networkInt + BigInt(i)` 混算抛 TypeError，循环不执行 ⇒ 表格为空、两条均不命中）。逐行复算：第 1 个子网 10.10.0.0/23，首/末可用 10.10.0.1 / 10.10.1.254，广播 10.10.1.255；第 8 个（索引 7）网络 = 10.10.0.0 + 7×512 = 10.10.14.0，首/末 10.10.14.1 / 10.10.15.254，广播 10.10.15.255。输入避开页面默认值 192.168.1.0/24→/26。",
  },
  {
    slug: "it/ip-calculator",
    inputs: { subnetBase: "0.0.0.0", subnetOldMask: "16", subnetNewMask: "24" },
    clicks: ["calcSubnets()"],
    expect: ["256 0.0.255.0/24 0.0.255.1 0.0.255.254 0.0.255.255"],
    ref: "N2-A 合法零地址回归：0.0.0.0 的 ipToInt 返回 0，修复前 `!baseInt` 会误判非法、直接返回（表格永远为空）。/16→/24 ⇒ 256 个子网，第 N 行（从 1 计）网络 = (N−1)×256 ⇒ 第 256 行 = 255×256 = 65280 = 0x0000FF00 = 0.0.255.0，首/末可用 0.0.255.1 / 0.0.255.254、广播 0.0.255.255。",
  },
  // ── .gitignore 生成（勾选技术栈 → 拼接忽略规则）──
  {
    slug: "it/gitignore-generator",
    checks: ["py", "go"],
    clicks: ["escH=function(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');};calcTool();"],
    expect: ["*.py[cod]", "/vendor/"],
    ref: "独立复算：勾选 py + go ⇒ 按 T 表顺序拼接 —— "
       + "`# Generated by ToolBox .gitignore Generator` 后依次为（空行分隔）# Python 组（__pycache__/、*.py[cod]、*.egg-info/、.venv/、venv/、env/）与 # Go 组（*.exe、*.test、/vendor/）。"
       + "默认态（无勾选）落 `请至少选择一种技术栈。` 分支，两条均不命中。"
       + "⚠️ 页面 `escH()` 走 `createElement('div').textContent → innerHTML`，harness 未建模 createElement 的转义读回 ⇒ `#result` 的 `<pre>` 恒空；"
       + "故在 clicks 内临时替换 escH 为等价纯字符串转义（只影响本用例进程内的本次调用，判别器清空 clicks 后自动回落 ⇒ 正确变红）。",
  },
  {
    slug: "it/gitignore-generator",
    checks: ["rust", "ide"],
    clicks: ["escH=function(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');};calcTool();"],
    expect: ["**/*.rs.bk", "# IDE/编辑器"],
    ref: "独立复算：勾选 rust + ide ⇒ # Rust 组（target/、**/*.rs.bk）与 # IDE/编辑器 组（.idea/、.vscode/、*.swp）。"
       + "技术栈名取自重构后的 T 表 name 字段（与页面 label 文案逐字一致：Python / Node.js / Go / Rust / Java/Kotlin / .NET / C/C++ / IDE/编辑器）。默认态不命中。",
  },  // —— BATCH284：哈希计算器多算法 / 批量 / 校验分支 + JSON 与 TSV 双向转换 ——
  {
    slug: "it/hash",
    inputs: { textInput: "abc" },
    checks: ["adler32"],
    expect: ["Adler-32 024d0127", "024d0127"],
    ref: "python zlib.adler32(b'abc') = 0x024d0127（Adler-32 标准向量）→ 页面渲染 Adler-32 024d0127。默认态 textInput 为空，calculateTextHashes() 直接 return，不渲染任何结果行。",
  },
  {
    slug: "it/hash",
    inputs: { textInput: "abc" },
    checks: ["crc32"],
    expect: ["CRC32 352441c2", "352441c2"],
    ref: "python zlib.crc32(b'abc') = 0x352441c2（CRC-32/ISO-HDLC）→ 页面渲染 CRC32 352441c2。与 it/crc-calculator 同算法但走哈希计算器的结果区，避开默认勾选集合。",
  },
  {
    slug: "it/hash",
    inputs: { textInput: "abc" },
    checkIds: ["uppercase"],
    checks: ["sha1"],
    expect: ["A9993E364706816ABA3E25717850C26C9CD0D89D"],
    ref: "python hashlib.sha1(b'abc').hexdigest() = a9993e364706816aba3e25717850c26c9cd0d89d，勾选 uppercase 后整串转大写。默认态未勾 uppercase，渲染的是同一种子的小写形态 ⇒ 不命中。",
  },
  {
    slug: "it/hash",
    inputs: { batchInput: "line1\nline2\nline3", batchAlgoSelect: "md5" },
    checks: ["md5"],
    expect: ["e6251bcf1a7dc3ba5e7933e325bbe605", "0c63b2a7c2c4808fb709c745630f6e29"],
    ref: "python hashlib.md5(b'line2').hexdigest() = e6251bcf1a7dc3ba5e7933e325bbe605、b'line3' = 0c63b2a7c2c4808fb709c745630f6e29。默认 batchInput 仅单行 Hello, ToolBox!（md5=53023f…），不含这两行 ⇒ 默认态不命中。",
  },
  {
    slug: "it/hash",
    inputs: { batchInput: "line1\nline2", batchAlgoSelect: "sha1" },
    checks: ["sha1"],
    expect: ["3ea6cb333875e2c37caaeeb19b1f54f037df3171", "a5de119f08985c4fbdbb7c6d975f302ebf582065"],
    ref: "python hashlib.sha1(b'line1').hexdigest() = 3ea6cb333875e2c37caaeeb19b1f54f037df3171、b'line2' = a5de119f08985c4fbdbb7c6d975f302ebf582065。批量行内哈希取自 getSelectedAlgos()，harness 下必须显式 checks 该键才存在。",
  },
  {
    slug: "it/hash",
    inputs: { batchInput: "line1\nline2", batchAlgoSelect: "crc32" },
    checks: ["crc32"],
    expect: ["d7d3ac2a", "4edafd90"],
    ref: "python zlib.crc32(b'line1') = 0xd7d3ac2a、b'line2' = 0x4edafd90。纯 JS 分支不依赖 WebCrypto，与 sha1 例共同覆盖批量模式的算法切换。",
  },
  {
    slug: "it/hash",
    inputs: { verifyInput: "abc", verifyHash: "900150983cd24fb0d6963f7d28e17f72" },
    checks: ["md5"],
    expect: ["匹配成功", "算法：MD5"],
    ref: "python hashlib.md5(b'abc').hexdigest() = 900150983cd24fb0d6963f7d28e17f72（RFC 1321 常见向量）→ 校验区输出「匹配成功！算法：MD5」。默认态两框为空，不渲染校验结论。",
  },
  {
    slug: "it/json-to-tsv",
    inputs: { tsvInput: "a\tb\n1\t2", t2jFormat: "compact" },
    clicks: ["tsvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ["[{\"a\":\"1\",\"b\":\"2\"}]"],
    ref: "TSV 两列（表头 a/b，数据行 1/2）→ 紧凑输出 [{\"a\":\"1\",\"b\":\"2\"}]，存在表头行时字段值一律按字符串处理。默认态 tsvInput 为空，tsvToJson() 直接 Toast 返回，jsonOutput 不更新。",
  },
  {
    // IT-N343 回归：自动识别数字不得改写长 ID / 前导零（勾选状态在桩内默认未勾，需在 clicks 里显式置真）。
    slug: "it/json-to-tsv",
    inputs: { tsvInput: "id\tcode\tamount\n12345678901234567890\t00123\t30", t2jFormat: "compact" },
    clicks: ["document.getElementById('t2jNumber').checked=true; tsvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ["[{\"id\":\"12345678901234567890\",\"code\":\"00123\",\"amount\":30}]"],
    ref: "IT-N343：开启「自动识别数字」后，20 位订单号 `12345678901234567890` 与带前导零的 `00123` 必须保持字符串原值（旧逻辑 parseFloat 会输出 12345678901234567000 / 123），而普通 `30` 仍应转成数值。三者同时成立才命中；默认态 jsonOutput 是示例数据，不含该串。",
  },
  {
    slug: "it/json-to-tsv",
    inputs: { tsvInput: "a\tb\n1\t2", t2jFormat: "pretty", t2jIndent: "4" },
    clicks: ["tsvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ["[ { \"a\": \"1\", \"b\": \"2\" } ]"],
    ref: "同样数据切「格式化 + 4 空格缩进」⇒ 输出 [ { \"a\": \"1\", \"b\": \"2\" } ]。与紧凑例构成同输入下 format/indent 两选项的判别力。",
  },
  {
    slug: "it/json-to-tsv",
    inputs: { jsonInput: "[{\"n\":\"x\",\"v\":1},{\"n\":\"y\",\"v\":null,\"w\":9}]", j2tHeader: "false", j2tNull: "NULL" },
    clicks: ["jsonToTsv()"],
    dumpIds: ["j2tStats"],
    expect: ["行数： 2 列数： 3 字符数： 17"],
    ref: "第二项带 w 字段 ⇒ 键并集 n/v/w 共 3 列、2 行，缺失值按 j2tNull=NULL 渲染；结果串 x\t1\tNULL\ty\tNULL\t9 长 17 字符。默认态 jsonInput 为空，jsonToTsv() 走 !input 早退，统计区保持初始文案。",
  },
  {
    slug: "it/json-to-tsv",
    inputs: { jsonInput: "[{\"a\":\"l1\\nl2\"}]", j2tNewline: "br" },
    clicks: ["jsonToTsv()"],
    dumpIds: ["tsvOutput"],
    expect: ["a l1\\nl2"],
    ref: "值内嵌换行 + j2tNewline=br ⇒ 转义为字面两字符 \n（不换真行），输出 a l1\nl2。默认态不注入该 JSON，tsvOutput 仍是页面初始样本。",
  },
  {
    slug: "it/json-to-tsv",
    inputs: { jsonInput: "[{\"a\":\"l1\\nl2\"}]", j2tNewline: "remove" },
    clicks: ["jsonToTsv()"],
    dumpIds: ["tsvOutput", "j2tStats"],
    expect: ["a l1l2", "行数： 1 列数： 1 字符数： 6"],
    ref: "同数据切 j2tNewline=remove ⇒ 换行被直接删除，输出 a l1l2（6 字符，行数/列数均 1）。与 br 例共同覆盖换行处理的两条分支。",
  },
  {
    slug: "it/json-to-tsv",
    inputs: { jsonInput: "[{\"a\":1,\"b\":2},{\"a\":3,\"b\":4}]" },
    expect: ["a b\n1 2\n3 4", "行数： 2 列数： 2"],
    ref: "实时重算：旧实现只在页面加载时调用一次 jsonToTsv()，textarea 没有 input 监听，改 JSON 后输出区与统计保持首屏结果。修复后输入合法 JSON 数组即自动重算 ⇒ TSV 表头 a/b、两行 1 2 与 3 4，统计 2 行 2 列。默认样本为 3 列（name/age/city），不含该表头与 `列数： 2`。",
  },

  // —— it/uuid-generator：UUID 解析器的结构化派生输出（版本号 / 变体 / 分段），
  //    锚点均为「解析产物」而非输入回显；默认态 parseInput 为空 → parseUuid() 直接 return，无输出。——
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "550e8400-e29b-41d4-a716-446655440000" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["版本号 4 (随机数)", "变体 RFC 4122（标准）", "time_low (32位): 550e8400", "clock_seq_hi_and_res (8位): a7", "node (48位): 446655440000"],
    ref: "RFC 4122 示例 UUID v4 的解析产物：version nibble = 4（随机数），variant nibble = 8（RFC 4122），time_low = 550e8400、clock_seq_hi_and_res = a7、node = 446655440000。默认态 parseInput 为空 → parseUuid() 首行即 return，parseResult 无内容，不命中。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "{550E8400-E29B-41D4-A716-446655440000}" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["标准格式 550e8400-e29b-41d4-a716-446655440000", "无分隔符 550e8400e29b41d4a716446655440000", "大写格式 550E8400-E29B-41D4-A716-446655440000"],
    ref: "normalizeUuid() 先剥离花括号再剥横线并转小写 ⇒ 花括号 + 全大写输入被归一化为标准小写形态。三条同时断言，任一归一化环节失效即不命中。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "550e8400e29b41d4a716446655440000" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["标准格式 550e8400-e29b-41d4-a716-446655440000"],
    ref: "无分隔符纯 hex（32 位）输入亦应被接受并还原为标准五段格式 —— 与上一例构成「带横线 / 不带横线」两种合法输入的判别力。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "00000000-0000-0000-0000-000000000000" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["版本号 0 (未知)", "变体 NCS 兼容（v0.x）", "NIL UUID 是"],
    ref: "NIL UUID（全零）走非法分支的边缘情形：version = 0 ⇒ 未知；variant nibble = 0 < 8 ⇒ NCS 兼容（v0.x）；NIL UUID 判定为「是」。三条同现方可证明零值未被误判为无效输入。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "cfbff0d1-9375-5685-968c-48ce8b15ae17" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["版本号 5 (SHA-1 哈希)", "node (48位): 48ce8b15ae17"],
    ref: "v5（SHA-1）UUID 的版本号识别，取 time_hi_and_version 高 4 位 = 5。node 段 48ce8b15ae17 同时确认字节切分正确。该值由同页 uuid-v5-generator 独立生成、并经 python uuid.uuid5 交叉核对。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "9073926b-929f-31c2-abc9-fad77ae3e8eb" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["版本号 3 (MD5 哈希)", "变体 RFC 4122（标准）"],
    ref: "v3（MD5）UUID 版本识别：python uuid.uuid3(NAMESPACE_DNS, 'example.com') = 9073926b-929f-31c2-abc9-fad77ae3e8eb，version nibble = 3。与 v4/v5 例构成三档版本判别。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "invalid!!" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["无效的 UUID 格式"],
    ref: "isValidUuid 正则不命中非 hex 输入 ⇒ 走拒绝分支，不输出任何分段。锚点为唯一的错误态文案，默认态同样不出现。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { parseInput: "f47ac10b-58cc-4372-a567-0e02b2c3d479" },
    clicks: ["parseUuid()"],
    dumpIds: ["parseResult"],
    expect: ["time_hi_and_version (16位): 4372", "clock_seq_hi_and_res (8位): a5", "node (48位): 0e02b2c3d479"],
    ref: "常被当作 v1 示例的 UUID 实际 version nibble 为 4（4372 首字符），页面据实判为「4 (随机数)」；本例只锚分段切分（v1 取值号段），避免与版本名串重叠。",
  },

  // —— it/uuid-v5-generator：纯 JS SHA-1 派生，RFC 4122 v5 标准实现（顶层全局函数，clicks 可直接调用）——
  {
    slug: "it/uuid-v5-generator",
    inputs: { ns: "6ba7b810-9dad-11d1-80b4-00c04fd430c8", name: "test.example.org" },
    clicks: ["generate()"],
    expect: ["test.example.org → a18100f5-ca06-5ccd-99c2-c48a12b87629"],
    ref: "RFC 4122 标准 DNS 命名空间 + python uuid.uuid5 独立复算 = a18100f5-ca06-5ccd-99c2-c48a12b87629。默认态 name 文本框已预置 example.com（会算出 cfbff0d1…）⇒ 故本例改锚非默认名，避免与默认态同档。",
  },
  {
    slug: "it/uuid-v5-generator",
    inputs: { ns: "6ba7b811-9dad-11d1-80b4-00c04fc430c8", name: "example.com" },
    clicks: ["generate()"],
    expect: ["example.com → a9a1848f-0316-5e07-bf97-385c699e24fe"],
    ref: "页面的 URL 命名空间预设末段为 00c04fc430c8（源码原值，非 RFC 的 00c04fd430c8）⇒ 派生结果须按页面实际常量复算 = a9a1848f-0316-5e07-bf97-385c699e24fe（python uuid.uuid5 逐字核对）。若误用 RFC 标准常量复算会得到 a5cf6e8e…，与页面不符。",
  },
  {
    slug: "it/uuid-v5-generator",
    inputs: { ns: "6ba7b812-9dad-11d1-80b4-00c04fc430c8", name: "example.com" },
    clicks: ["generate()"],
    expect: ["example.com → ab688337-55e6-5e43-85ce-ea1c3581409c"],
    ref: "OID 命名空间预设（末段 00c04fc430c8）下 python uuid.uuid5 = ab688337-55e6-5e43-85ce-ea1c3581409c。三个非 DNS 预设构成命名空间维度的三档判别。",
  },
  {
    slug: "it/uuid-v5-generator",
    inputs: { ns: "6ba7b814-9dad-11d1-80b4-00c04fc430c8", name: "example.com" },
    clicks: ["generate()"],
    expect: ["example.com → 5c5ba4c5-c2d9-5adc-a758-da46719bd156"],
    ref: "X500 命名空间预设（末段 00c04fc430c8）下 python uuid.uuid5 = 5c5ba4c5-c2d9-5adc-a758-da46719bd156。",
  },
  {
    slug: "it/uuid-v5-generator",
    inputs: { ns: "6ba7b810-9dad-11d1-80b4-00c04fd430c8", name: "example.com" },
    clicks: ["document.getElementById('upper').checked=true;generate()"],
    expect: ["example.com → CFBFF0D1-9375-5685-968C-48CE8B15AE17"],
    ref: "upper 开关改在 clicks 里显式置位（harness 下 runner 的 checks 读不到 .checked）。默认态 upper 未勾选 ⇒ 输出小写 cfbff0d1…，大小写形态不同 ⇒ 双态可判别。",
  },
  {
    // 默认 name 已含 example.com（与默认态同档）⇒ 本例第一行换成 test.example.org，第二行用 abc，
    // 使「多行 → 逐行输出」这一行为只在注入态出现。
    slug: "it/uuid-v5-generator",
    inputs: { ns: "6ba7b810-9dad-11d1-80b4-00c04fd430c8", name: "test.example.org\nabc" },
    clicks: ["generate()"],
    expect: ["test.example.org → a18100f5-ca06-5ccd-99c2-c48a12b87629", "abc → 6cb8e707-0fc5-5f55-88d4-d4fed43e64a8"],
    ref: "generate() 对 name 按空行切分后逐行派生（空行被 filter 掉）。两行结果均经 python uuid.uuid5 核对；默认态仅一行 example.com，不出现 abc → … ⇒ 有判别力。",
  },
  // —— it/timestamp-converter：仅「日期加减 / 日期差」两条路径在 harness 下可注入
  //    （oninput="fromTimestamp('sec')" 的 input 事件路径在 harness 下抛错不生效，投注于 clicks 调 calculateDate/calculateDiff）。
  //    所有日期值均经 python datetime 独立核对。 ——
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2023-12-15", calcOp: "add", calcAmount: "30", calcUnit: "day" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2024-01-14 00:00:00"],
    ref: "python datetime 核对：date(2023,12,15) + timedelta(days=30) = 2024-01-14。页面输出「计算结果: 2024-01-14 00:00:00 + 时间戳」。默认态四个日期控件均空 ⇒ parseDate 返回假值，直接 toast 返回，calcResult1 无内容。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2024-02-28", calcOp: "add", calcAmount: "1", calcUnit: "day" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2024-02-29 00:00:00", "时间戳: 1709136000 秒"],
    ref: "闰年边界：2024-02-28 + 1 天必须落到 02-29（平年会错落到 03-01）。时间戳 1709136000 = 2024-02-29T00:00:00+08:00，与页面本地时区渲染一致。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2023-02-10", calcOp: "add", calcAmount: "1", calcUnit: "month" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2023-03-10 00:00:00"],
    ref: "跨月且跨年界（同一年内 02→03）的月份加减；python 核对 date(2023,2,10) + 1 个月（按 setMonth 语义）≈ 2023-03-10。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2023-06-15", calcOp: "subtract", calcAmount: "1", calcUnit: "week" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2023-06-08 00:00:00"],
    ref: "减法方向（sign = -1）与「周」单位换算（amount×7）；python 核对 date(2023,6,15) - timedelta(days=7) = 2023-06-08。可选值 add 同结构已由上一例覆盖，本例专测减号方向。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2023-12-31", calcOp: "add", calcAmount: "1", calcUnit: "day" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2024-01-01 00:00:00"],
    ref: "年界跨越：2023-12-31 + 1 天 = 2024-01-01。与「2024-02-29」例共同覆盖两条最容易出错的进位边界。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { diffStart: "2023-01-01", diffEnd: "2023-12-31" },
    clicks: ["calculateDiff()"],
    expect: ["相差天数: 364 天", "相差周数: 52 周"],
    ref: "2023 非闰年全年 = 365 天 ⇒ 首尾相差 364 天（含首不含尾）。页面同时渲染「相差小时/分钟/秒」做量纲自洽校验。默认态两框为空 ⇒ 不进入渲染。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { diffStart: "2024-01-01", diffEnd: "2024-12-31" },
    clicks: ["calculateDiff()"],
    expect: ["相差天数: 365 天", "相差小时: 8,760 小时"],
    ref: "闰年全年（2024-02-29 计入）⇒ 相差天数应为 365（闰多的一天已含在 366 天的日历长度里），8,760 小时 = 365×24 与天数自洽；与上一例构成闰年/平年的对照。",
  },
  {
    // 跨闰年边界：2020-02-28 → 2021-03-01。手算易得 366，正确答案 367（2020 闰年多出的一天落在区间内）。
    slug: "it/timestamp-converter",
    inputs: { diffStart: "2020-02-28", diffEnd: "2021-03-01" },
    clicks: ["calculateDiff()"],
    expect: ["相差天数: 367 天", "相差年数: 约 1 年"],
    ref: "python date(2021,3,1) - date(2020,2,28) = 367 天。本例是「闰日是否落在区间内」的判定点：区间含 2020-02-29 ⇒ +1；若页面按平年算会得 366 而暴露缺陷。",
  },

  // —— it/csv-to-json：CSV ↔ JSON 双向转换。三个开关（hasHeader/trimFields/prettyPrint）在 harness 下
  //    读不到 .checked ⇒ 一律在 clicks 里显式置位；产物在 readonly textarea 的 value ⇒ 必须 dumpIds 回写。 ——
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: "a,b\n1,2" },
    clicks: ["document.getElementById('hasHeader').checked=true;csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['[{"a":"1","b":"2"}'],
    ref: "首行作表头 ⇒ 键取用首行列名、不再保留为一条数据。默认态 harness 下 hasHeader 读到 false（HTML 虽写死 checked 但桩读不到）⇒ 输出退化为 column1/column2 两键 ⇒ 本例与下一条构成表头开/关的强对照。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: "a,b\n1,2" },
    clicks: ["csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['[{"column1":"a","column2":"b"},{"column1":"1","column2":"2"}'],
    ref: "无表头时按 32 位通用列名 column1/column2 展开，且首行也作为一条数据。与上一条同输入、仅表头开关不同 ⇒ 判别力完全落在 hasHeader 上。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: "a;b;c\n1;2;3", csvDelimiter: ";" },
    clicks: ["document.getElementById('hasHeader').checked=true;csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['[{"a":"1","b":"2","c":"3"}'],
    ref: "分隔符切到分号后三列全部正确成键。若分隔符注入未生效（仍按逗号）则只会切出 1 列 ⇒ 输出退化为 column1。与逗号同形态的输入构成分隔符维度的判别。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: " a , b \n 1 , 2 " },
    clicks: ["document.getElementById('trimFields').checked=false;document.getElementById('hasHeader').checked=true;csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['[{" a ":" 1 "," b ":" 2 "}'],
    ref: "关闭 trimFields ⇒ 字段首尾空格（含表头键名）全部保留。与下一条同输入、仅 trimFields 开关不同 ⇒ 判别力落在 trimming 上。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: " a , b \n 1 , 2 " },
    clicks: ["document.getElementById('trimFields').checked=true;document.getElementById('hasHeader').checked=true;csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['[{"a":"1","b":"2"}'],
    ref: "开启 trimFields ⇒ 键名与值两端空格被裁掉，键变为 a/b。这是「去空格」这一行为的正向断言，与上一条互补。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: "__proto__,v\nx,1" },
    clicks: ["document.getElementById('hasHeader').checked=true;csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['{"__proto__":"x"'],
    ref: "表头键名 `__proto__`：修复前每行对象 `obj[h]=v` 走原型 setter，JSON 丢键只剩 v；Object.create(null) 后保留自有键 ⇒ `{\"__proto__\":\"x\"`。输入是逗号分隔，不含 JSON 引号键形态。",
  },
  {
    // ⚠ 存疑项：字段被引号包裹且内含分隔符时，页面把引号当普通字符切开，且后半段「y」丢失。
    //   修页面后本条须同步更新。已留档上报，未擅改页面。
    slug: "it/csv-to-json",
    inputs: { csvInput: "a,b\n1,\"x,y\"" },
    clicks: ["document.getElementById('hasHeader').checked=true;csvToJson()"],
    dumpIds: ["jsonOutput"],
    expect: ['[{"a":"1","b":"\\"x"}'],
    ref: "默认 csvQuote 为双引号，含分隔符的字段本应整体保留为 b=\"x,y\"；页面实际切成 b='\"x' 且丢弃后半段。可能是 parseCSV 未实现引号解析，也可能是 harness 下 select.value 取空 —— 二者在 harness 内无法区分。已被 SEA 记为待查项，修复页面后此条须同步更新。",
  },
  {
    slug: "it/url-encode",
    inputs: { "input": "a?b/c=d" },
    clicks: ["setEncodeMode('uri');encodeUrl();"],
    dumpIds: ["output", "statRatio"],
    expect: ["a?b/c=d", "+0.0%"],
    ref: "既有 5 条全走 component 口径，本例切到 uri 模式（encodeURI）后 问号/斜杠/等号/冒号 属保留字符不再转义 ⇒ 输出与原串完全一致 a?b/c=d，膨胀率 (7−7)/7×100 = +0.0%。python 复算：以 safe 集合包含 /?#=: 做 quote('a?b/c=d') 得同一串，长度 7。",
  },
  {
    slug: "it/url-encode",
    inputs: { "input": "%E4%B8%AD%E6%96%87+x%3Fy" },
    clicks: ["decodeUrl();"],
    dumpIds: ["output"],
    expect: ["中文+x?y"],
    ref: "decodeUrl：%E4%B8%AD%E6%96%87 还原为「中文」、%3F 还原为 ?；仅在勾选「空格编码为 +」时才把 + 当空格，默认未勾选 ⇒ + 原样保留，输出 中文+x?y（python unquote 同口径）。",
  },
  {
    slug: "it/url-encode",
    inputs: { "parseInput": "https://user:pw@example.com:8443/api/v1?a=1&b=%E4%B8%AD#frag" },
    clicks: ["parseUrl();"],
    dumpIds: ["pHost", "pPort", "pPathname", "pOrigin"],
    expect: ["example.com:8443", "8443", "/api/v1", "https://example.com:8443"],
    ref: "既有用例未覆盖解析器。分段结论区渲染：host example.com:8443 / port 8443 / pathname /api/v1 / origin https://example.com:8443。user:pw 属 username/password 字段、不进 host，故锚这三段 —— 既非输入回显、也不在页面源码里静态存在。锚 pSearch 会撞输入里的 ?a=1&b=%E4%B8%AD，按「禁输入回显」应避开。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='env';document.getElementById('keyInput').value='APP_ENV';document.getElementById('valInput').value='production';document.getElementById('typeInput').value='string';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["78 B", "1 个变量"],
    ref: "env 分支：两行固定注释头（# .env configuration + # Generated by ToolBox Env Generator）后逐变量输出 KEY=VALUE，每个变量后补一个空行。产出 UTF-8 字节数 = 20+1 + 36+1 + 0+1 + 18+1 = 78 B（页面用 new Blob([output]).size 统计）。python 复算 len(('# .env configuration\n# Generated by ToolBox Env Generator\n\nAPP_ENV=production\n'.encode())) = 78。默认态无变量 ⇒ 0 B。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='env-local';document.getElementById('keyInput').value='MAX_RETRY';document.getElementById('valInput').value='5';document.getElementById('typeInput').value='number';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["77 B", "1 个变量"],
    ref: "env-local 与 env 走同一段代码，仅注释头换成 .env.local（首行多 6 字符 ⇒ 78−1=77 B）。取 number 型顺带验证 formatValue 对数字不加引号。python 同式复算 = 77。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='docker';document.getElementById('optBase64').checked=true;document.getElementById('optQuote').checked=true;document.getElementById('keyInput').value='DB_PASSWORD';document.getElementById('valInput').value='s3cr3t';document.getElementById('typeInput').value='secret';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["78 B", "1 个变量"],
    ref: "同时打开 Base64 与引号开关：secret 型经 b64Encode('s3cr3t')=czNjcjN0，再被 quote 开关包上双引号 ⇒ 输出行以「  - DB_PASSWORD=」开头、值为带双引号的 czNjcjN0。docker 分支每个变量后不补空行。产出 = 38+1 + 12+1 + 26 = 78 B。python 复算该串 .encode() 长度 = 78。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='json';document.getElementById('keyInput').value='MAX_CONN';document.getElementById('valInput').value='120';document.getElementById('typeInput').value='number';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["21 B", "1 个变量"],
    ref: "json 分支是唯一直接 return 的分支，用 JSON.stringify(obj,null,2)，number 型先做 Number(val)||0 ⇒ 值输出为裸数字不带引号。产出 = 左花括号 + 换行 + 两空格 + 「MAX_CONN」+ 冒号空格 + 120 + 换行 + 右花括号，共 21 B。python 复算 len(json.dumps({'MAX_CONN':120},indent=2).encode()) = 21。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='yaml';document.getElementById('keyInput').value='COUNT';document.getElementById('valInput').value='42';document.getElementById('typeInput').value='number';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["41 B", "1 个变量"],
    ref: "yaml 分支对 number 型且值可转数字者输出裸标量（COUNT: 42），与 string 型走加引号分支形成对照。产出 = 30+1 + 9+1 = 41 B。python 复算 len(('# Environment variables (YAML)\nCOUNT: 42\n'.encode())) = 41。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='shell';document.getElementById('optSort').checked=true;document.getElementById('keyInput').value='ZEBRA';document.getElementById('valInput').value='1';document.getElementById('typeInput').value='string';addVariable();document.getElementById('keyInput').value='ALPHA';document.getElementById('valInput').value='2';document.getElementById('typeInput').value='string';addVariable();document.getElementById('keyInput').value='MID';document.getElementById('valInput').value='3';document.getElementById('typeInput').value='string';addVariable();"],
    dumpIds: ["previewSize", "varCount", "tableWrap"],
    expect: ["80 B", "3 个变量", "1 ALPHA"],
    ref: "打开排序开关后 getSortedVars() 用 key.localeCompare 重排 ⇒ 表格首行与首条 export 均为 ALPHA（插入序为 ZEBRA/MID/ALPHA，不排序时首行必是 ZEBRA），故锚 tableWrap 里的「1 ALPHA」可证排序生效。产出 = 11+1+21+1+0+1+(9+1+7+1+8+1)+0+1+(7+1+5+1+6+1)+0+1+(5+1+7+1+8+1) = 80 B。python 复算 len(('#!/bin/bash\n# Shell export script\n\nexport ALPHA=2\n\nexport MID=3\n\nexport ZEBRA=1\n'.encode())) = 80。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='toml';document.getElementById('keyInput').value='MAX_CONN';document.getElementById('valInput').value='120';document.getElementById('typeInput').value='number';addVariable();document.getElementById('keyInput').value='DEBUG_ON';document.getElementById('valInput').value='true';document.getElementById('typeInput').value='boolean';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["60 B", "2 个变量"],
    ref: "toml 分支固定输出 [env] 段：number 型写 Number(v.value)、boolean 型写 v.value==='true'，两者都不带引号 ⇒ 「MAX_CONN = 120」/「DEBUG_ON = true」。python 复算 len(('# TOML configuration\n\n[env]\nMAX_CONN = 120\n\nDEBUG_ON = true\n'.encode())) = 60。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='properties';document.getElementById('keyInput').value='LOG_LEVEL';document.getElementById('valInput').value='debug';document.getElementById('typeInput').value='string';addVariable();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["48 B", "1 个变量"],
    ref: "properties 分支与 env 同构（逐变量 KEY=VALUE 后补空行），仅注释头换成 # Java Properties configuration。python 复算 len(('# Java Properties configuration\nLOG_LEVEL=debug\n'.encode())) = 48。",
  },
  {
    slug: "it/env-generator",
    inputs: {},
    clicks: ["document.getElementById('formatSelect').value='env';document.getElementById('importText').value='PORT=8080\\nSECRET_KEY=abc\\nFLAG=true\\n# comment line\\nBAD_LINE';parseImport();"],
    dumpIds: ["previewSize", "varCount"],
    expect: ["96 B", "3 个变量"],
    ref: "走导入路径：parseImport 逐行解析，跳过空行与 # 注释行、跳过不含等号的 BAD_LINE，并按值自动判型（8080→number；abc 且键名含 SECRET→secret；true→boolean）⇒ 共 3 个变量。python 复算 len(('# .env configuration\n# Generated by ToolBox Env Generator\n\nPORT=8080\n\nSECRET_KEY=abc\n\nFLAG=true\n'.encode())) = 96。",
  },
  {
    slug: "it/rsa",
    inputs: {"signPubKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA66qDvUJcGDjBbeWGu3KQ\n4v+yvXkWUWIGmSlFU3+YJLurC7QfQRSbWaXg8WFcd1vojcgS8Te325mS+X3yuFEs\nKR+hSG+plotiOY2fhdpgVgz2OH1BsZE1QQsn/Vw7OEoMYcP4K2ncm+2orP9gXMUN\n16PJW1Jicy+xe/F8sfB9XEKsXfQkLpTezn5MlP1Y2qCJpp9zXq9GCAzQj74XGiDx\nGtV0+sydNliJllr9yldRfpNxUYrT+HgKdD1CtHcJo76XLxMh6Z7VFRzZMmHV1FJq\nGlp/38EgPqoW9Mhi8VJxj8x7tO6iw5VoJgrX3SVgwytbBcXmVUdS4yivtRHAHWwo\nvQIDAQAB\n-----END PUBLIC KEY-----\n", "signInput": "hello", "signature": "k9eH/wYFhf1yr1cnfXSJTpuXi/wcNb/AK1Skb9JhxAQly8Qe+w2QT9meteSHFBLWyrraTDhiny3YVQ5yxZVChDhudF2tzq6APEPRluzVLuWgBJ2dZN6pWqGwqcVLznMO729WpDHWJJ0UnI8ekcazecRHesGaW3y2o4g4hRP9ry2qegi5Uc4d0fLQqR/LsfNStrqTIjXDz5JLUlIZZHlg9Ny2+sWIzZ3dDo4EEgQmaUEfWqZc8Q0cA7/o3/owCcDkVsSmROqIO9rcZrOHdcKabWdmsq1zoQiCuGCA2+EprrecTUW/GAv7wNOLNvTB5lNOLo2EvP1tu4/cxnix07X0og=="},
    clicks: ["document.getElementById('signAlgo').value='RSA-PSS';doVerify()"],
    dumpIds: ["signResult"],
    expect: ["❌ 签名验证失败"],
    ref: "签名算法对照：同一 PKCS#1 v1.5 签名改用 RSA-PSS 验签 ⇒ 填充方案不同，验签必失败，页面输出「❌ 签名验证失败！数据被篡改或密钥不匹配。」。判别点落在 signAlgo 选择上：把点击清空后走兜底 doVerify 会按默认 PKCS1 验签并通过（不命中失败串）⇒ 强判别。",
  },
  {
    slug: "it/rsa",
    inputs: {"signPubKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA66qDvUJcGDjBbeWGu3KQ\n4v+yvXkWUWIGmSlFU3+YJLurC7QfQRSbWaXg8WFcd1vojcgS8Te325mS+X3yuFEs\nKR+hSG+plotiOY2fhdpgVgz2OH1BsZE1QQsn/Vw7OEoMYcP4K2ncm+2orP9gXMUN\n16PJW1Jicy+xe/F8sfB9XEKsXfQkLpTezn5MlP1Y2qCJpp9zXq9GCAzQj74XGiDx\nGtV0+sydNliJllr9yldRfpNxUYrT+HgKdD1CtHcJo76XLxMh6Z7VFRzZMmHV1FJq\nGlp/38EgPqoW9Mhi8VJxj8x7tO6iw5VoJgrX3SVgwytbBcXmVUdS4yivtRHAHWwo\nvQIDAQAB\n-----END PUBLIC KEY-----\n", "signInput": "HELLO", "signature": "k9eH/wYFhf1yr1cnfXSJTpuXi/wcNb/AK1Skb9JhxAQly8Qe+w2QT9meteSHFBLWyrraTDhiny3YVQ5yxZVChDhudF2tzq6APEPRluzVLuWgBJ2dZN6pWqGwqcVLznMO729WpDHWJJ0UnI8ekcazecRHesGaW3y2o4g4hRP9ry2qegi5Uc4d0fLQqR/LsfNStrqTIjXDz5JLUlIZZHlg9Ny2+sWIzZ3dDo4EEgQmaUEfWqZc8Q0cA7/o3/owCcDkVsSmROqIO9rcZrOHdcKabWdmsq1zoQiCuGCA2+EprrecTUW/GAv7wNOLNvTB5lNOLo2EvP1tu4/cxnix07X0og=="},
    clicks: ["doVerify()"],
    dumpIds: ["signResult"],
    expect: ["❌ 签名验证失败"],
    ref: "同一签名、仅把待验数据从 hello 改成 HELLO（大小写变了）⇒ 验签失败，页面输出「❌ 签名验证失败！数据被篡改或密钥不匹配。」。与上一条构成「同密钥、仅数据不同」的强对照，判别力完全落在被验数据上。",
  },
  {
    slug: "it/rsa",
    inputs: {"encPrivKey": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDrqoO9QlwYOMFt\n5Ya7cpDi/7K9eRZRYgaZKUVTf5gku6sLtB9BFJtZpeDxYVx3W+iNyBLxN7fbmZL5\nffK4USwpH6FIb6mWi2I5jZ+F2mBWDPY4fUGxkTVBCyf9XDs4Sgxhw/gradyb7ais\n/2BcxQ3Xo8lbUmJzL7F78Xyx8H1cQqxd9CQulN7OfkyU/VjaoImmn3Ner0YIDNCP\nvhcaIPEa1XT6zJ02WImWWv3KV1F+k3FRitP4eAp0PUK0dwmjvpcvEyHpntUVHNky\nYdXUUmoaWn/fwSA+qhb0yGLxUnGPzHu07qLDlWgmCtfdJWDDK1sFxeZVR1LjKK+1\nEcAdbCi9AgMBAAECggEAPpggu6EnkutoPQdM3PbWEuT1lavWyLDvrbiviDkIsSED\nkm06K/AMPyh28cX5aF6KCzaMCXPSKsrEpe3VDS3KO/YBwZqfAbRt13mNWGEjW1fA\nAksKqt41tdv/uCTKOe45EbKadPV+OhBK0ABYmOth/NetAMuGCLAvRQtkImMM+Pbe\nFGK+qDBgmL0JmlkQW+1aj2i4jBuWoyYiCF0DEogfgukX3RZS5RxYDTaaivLO1Jaj\nHkd8sdwb5E8YhbJwHr3F6Aanj3J2Lczd5sDg4nmyd1SQXQQS8xTJTCf+2h0ox7uk\n5BQEomZwyjxNOD83n2+u7R2eT5H9spVTjh/6NlS4pQKBgQD2mEZ2WhzhVIIAV9CU\ndH4slwVCb7UDfEyKN7uUE8pcP/Jw76eThoNqMAVlmqxbHZFIDLvnHTsbJahyWv40\njuF8P8yWCB1JjiePpBXPC5wzu3XbMC05m5JB7z10d0O2f8DwXxr7YhY2XNTEL8rg\n70XJ20+wR2OBgaaPhyMUuJBt1wKBgQD0p4g/8ThIpBEeFWXoOYSruxBcP1GEyfL+\n4GJ3gFtnllRv+TqoMIcOlO4qaDXEi/W9A4fr6Pocb43Q4coLq5RuBBPMsSKiIKhR\nE5ocHkganmGy+OYn+g7PsttvoTElYRKq+ThID3YtLD63vMJ+FSzncEB7MBQgJETm\nSX/kuyEDiwKBgQDhZGHTP55yHwoMQje12ZySKR93kB8FppFXLIXZXRVzqEdzDro+\nz45Ces4UBoJPbgEit/Dv1/n0YEFM9PqxE3/qT24yHAyY9MQYOMRuUJBfgJLC25Aa\nvaW7em7Ti0drAe5aRrOk3gyrd8JJ590qJ8nELR7zYu0CrHyPZ9ea0u/AVQKBgHYP\n6rZAp9KWKhSEavsX1qgwy4JYo/QaqILKsXnNnU5twy2N7fqAAIzO3eflBh1lFR8z\ndwInGZtjUeJ9M01SbXxxx0Q+LuJiNBd8CCCNlGoUCD2f0yFzkHY2b6J8/QR2xdVw\nEvLjUzoVYea01n6VpWfCSbuoxe2E0yL2URuGGjZlAoGAbl45fbaj0nyHfJDDCA1+\nNV9n/9av1k3yluCmuh5blWjsXLEvJ9JhZSaQN3yvIc6CRGJ/wZKFD8QmYwhj4ky1\npxlF765JMf8/Mcz5zfJt11epZZDLhzfBfze4oe25P34eJLKEkgqjnUK4uN1nMA9G\nWwYVMfvZCtDt9vrCaoUZvqM=\n-----END PRIVATE KEY-----\n", "encInput": "ljAhYreFpOCJsmdRXLJmG29hLhynILSjvOP2YKtCbr2kOpG3kogBTYAmpxDE25j3OCb+gk3/c2tEKxN5HILr+LiyHsXEbKaUydGpgtVF9jdiY9uxK2ZQeCUEkA1spzBRnDNVYfGHvoTTaDyTE85vs+j5xoVKENUGwOEnIna2kKuUI7mxMBnlJAWNbPp3Z8R3hobs+04zukmGldhoRVoASU4Z0jJ7cQLXhAZNlOV1B7R3/TMPCTl1FW91/seI6FX795Rn/VrA/UIsuNCsGrgT9koqmkcGPR5F4yowzatEhwf2HcY1FKKTwQkoKgQ0vVN0z4YuoFx+MY00o+eumCdiyw=="},
    clicks: ["doDecrypt()"],
    dumpIds: ["encResult"],
    expect: ["secret message"],
    ref: "RSA-OAEP(SHA-256) 解密：私钥用 PKCS#8 PEM 注入，密文以 base64 注入（页面按「偶数长度且全为十六进制才当 hex、否则走 base64」分流），解密后 textContent 还原为明文 secret message。密文由 node crypto.publicEncrypt({padding: RSA_PKCS1_OAEP_PADDING, oaepHash:'sha256'}) 生成，长度 256 字节。",
  },
  {
    slug: "it/rsa",
    inputs: {"encInput": "SIGNMARK42"},
    clicks: ["switchTab('sign');document.getElementById('signResult').textContent=document.getElementById('encInput').value+' SIGNED';document.getElementById('encResult').textContent='WRONG-BOX';var __t=__rsaResText();document.getElementById('encResult').textContent='PROBE '+__t;"],
    dumpIds: ["encResult"],
    expect: ["PROBE SIGNMARK42 SIGNED"],
    ref: "N96 回归：签名页签激活时 __rsaResText() 必须读 #signResult。旧实现 querySelector('.result-box') 恒取 DOM 里第一个结果框 #encResult，签名结果永不入库。这里把两个容器写成不同值，命中即证明按页签取容器；expect 为输入 encInput 的派生串，页面默认输入下不成立 ⇒ 有判别力。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {"input-text": "the\tquick\tbrown\nfox\tjumps\n"},
    clicks: ["document.getElementById('opt-tab2space').checked=true;executeClean();"],
    dumpIds: ["stat-original", "stat-result", "stat-reduce", "stat-lines"],
    expect: ["35", "+9"],
    ref: "Tab 转空格（默认宽度 4）：3 个制表符各展开成 4 个空格 ⇒ 26 → 35 字符，减少量 26−35 = −9，页面显示为 +9；行数仍为 3。python 复算：输入 len = 26，输出 len = 26 + 3×3 = 35。统计区四个 span 是唯一不折叠空白的派生量，故锚这里。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {"input-text": "a    b    c    d    e    f"},
    clicks: ["document.getElementById('opt-space2tab').checked=true;document.getElementById('space2tab-count').value='4';executeClean();"],
    dumpIds: ["stat-original", "stat-result", "stat-reduce", "stat-lines"],
    expect: ["11", "-15"],
    ref: "空格转 Tab（每 4 个空格换 1 个制表符，宽度输入框显式置 4）：5 组 4 空格 ⇒ 26 → 11 字符，减少量 26−11 = 15，页面显示 −15；行数 1。与上一条是互逆运算的强对照（同长度输入，一个变长一个变短）。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {"input-text": "  alpha   beta \n\n\n  gamma    delta  \n"},
    clicks: ["document.getElementById('opt-trim').checked=true;document.getElementById('opt-merge-spaces').checked=true;document.getElementById('opt-empty-lines').checked=true;executeClean();"],
    dumpIds: ["stat-original", "stat-result", "stat-reduce", "stat-lines"],
    expect: ["22", "-15"],
    ref: "三开关叠加：逐行 trim（去掉每行首尾空格）+ 行内连续空格合并成 1 个 + 整行删除空行。输入 37 字符 / 4 行，输出 22 字符 / 2 行（alpha beta 与 gamma delta 两行），减少量 15。既有那条只测 trim+合并空格，本例额外叠加删空行与行首行尾空格。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {"input-text": "  hello  world  again  "},
    clicks: ["document.getElementById('opt-trim').checked=true;document.getElementById('opt-remove-inline-space').checked=true;executeClean();"],
    dumpIds: ["stat-original", "stat-result", "stat-reduce"],
    expect: ["15", "-8"],
    ref: "去行内所有空格 + 逐行 trim：首尾空格与中间双空格一并清除 ⇒ 23 → 15 字符，减少量 8。默认态三个统计值恒 0，注入后才出现。",
  },
  {
    slug: "it/text-cleaner",
    inputs: {"input-text": "one\ntwo\nthree\nfour\nfive\n"},
    clicks: ["document.getElementById('opt-remove-newlines').checked=true;executeClean();"],
    dumpIds: ["stat-original", "stat-result", "stat-reduce", "stat-lines"],
    expect: ["19", "-5", "1"],
    ref: "删除所有换行 ⇒ 24 → 19 字符、行数降到 1（apshot 统计行数为结果串 split(换行).length）。python 复算：len('onetwothreefourfive') = 19。",
  },
  {
    slug: "it/text-cleaner",
    // IT-N20 回归：点「执行清理」须记录历史并填充数据表（修复前 executeClean 不触发 extras，table 恒空）
    inputs: {"input-text": "  hello   world  \n\n\n  foo   bar  "},
    clicks: ["document.getElementById('opt-trim').checked=true;document.getElementById('opt-merge-spaces').checked=true;document.getElementById('opt-empty-lines').checked=true;executeClean();"],
    dumpIds: ["text_cleanerTable"],
    expect: ["hello world foo bar"],
    ref: "修复前 executeClean 不调用 __text_cleanerExtras，历史/数据表/图表三页签恒空（原仅 applyPreset 被包裹）。现包裹 executeClean：清理完成触发 extras → TBKit.history.record + matrix.table 渲染 → text_cleanerTable 含结果『hello world foo bar』（output 经 trim+合并空格+去空行得 hello world\\nfoo bar，__text_cleanerResText 折叠空白为 hello world foo bar）。默认样例不命中（不调 executeClean 即无记录）。",
  },
  {
    // 遮蔽回归：本页复制函数已改名 copyPlainText，避免被 js/common.js 的全局 copyText(text) 覆盖
    //（原内联 onclick="copyText()" 命中全局实现，实际复制的是 undefined）。
    slug: "it/rich-text-editor",
    inputs: { source: "<p>hello world</p>" },
    clicks: ["applySource();document.getElementById('editor').innerText='hello world';var __c=ToolBox.copyText;ToolBox.copyText=function(t){document.getElementById('source').value='COPIED:'+t;};copyPlainText();ToolBox.copyText=__c;"],
    expect: ["COPIED:hello world"],
    ref: "copyPlainText 取编辑区纯文本交给 ToolBox.copyText：注入 <p>hello world</p> 后应为 hello world（用例把 ToolBox.copyText 换成采集器，两种桩模式都成立）。被全局 copyText 覆盖时无参调用收到 undefined，采集到 COPIED:undefined 或直接抛错，均不命中。",
  },
  {
    slug: "it/rich-text-editor",
    inputs: {"source": "<p>hello world</p>"},
    clicks: ["applySource();"],
    dumpIds: ["stSize", "stParas"],
    expect: ["18 B"],
    ref: "HTML 体积 = new Blob([editor.innerHTML]).size，即编辑区 HTML 串的 UTF-8 字节数：页面把源码注入 #source 后 applySource() 写回编辑区并 updateStats()。python 复算 len('<p>hello world</p>'.encode()) = 18。段落计数 stParas 在 harness 下只统计 p 标签（querySelectorAll 传的是逗号串，桩按首个标签匹配），本例为 1。默认态编辑区是页面自带样例，体积是另一数值且不出现 18 B。",
  },
  {
    slug: "it/rich-text-editor",
    inputs: {"source": "<p>见 <a href=\"https://a.dev\">A</a></p><p>图 <img src=\"x.png\"></p>"},
    clicks: ["applySource();"],
    dumpIds: ["stSize", "stParas", "stLinks", "stImgs"],
    expect: ["68 B"],
    ref: "同一统计兼带链接/图片计数：注入 1 个 a、1 个 img、2 个 p ⇒ stLinks=1 / stImgs=1 / stParas=2；python 复算两行 UTF-8 共 68 字节（「见」「图」各 3 字节）。锚取 68 B，默认态样例里没有该数值。",
  },
  {
    slug: "it/rich-text-editor",
    inputs: {"source": "<p>hello world</p>"},
    clicks: ["applySource();copyHtml();"],
    dumpIds: ["result", "stSize"],
    expect: ["✅ 已复制 HTML 源码（18 B）"],
    ref: "copyHtml() 取编辑区 innerHTML 走 ToolBox.copyText，并把结论写进 #result：✅ 已复制 HTML 源码（fmtSize(v.length)），此处 v.length 是 UTF-16 码元数（本例与字节数同为 18）。默认态 #result 为空 ⇒ 不命中。",
  },
  {
    slug: "it/rich-text-editor",
    inputs: {"source": "<ul><li>甲</li><li>乙</li></ul>"},
    clicks: ["applySource();downloadHtml();"],
    dumpIds: ["result", "stSize"],
    expect: ["✅ 已下载 document.html（152 B）"],
    ref: "downloadHtml() 拼固定外壳（<!DOCTYPE html> … <body> 换行）再 new Blob：固定头尾 python 复算 119 字节 + 编辑区 33 字节 = 152 ⇒ 结论行 ✅ 已下载 document.html（152 B）。默认态结论行的字节数不同 ⇒ 判别力落在注入内容上。",
  },
  {
    slug: "it/rich-text-editor",
    inputs: {"source": "<p>甲</p><p>乙</p><p>丙</p>"},
    clicks: ["applySource();"],
    dumpIds: ["stSize", "stParas", "stLinks"],
    expect: ["30 B"],
    ref: "三段纯中文：stParas=3，stSize = 3×10 = 30 字节（每个汉字 3 字节、标签各 7 字节⇒每段 10 字节）。与上两条合起来覆盖「字节统计 × 块计数 × 链接/图片计数」三条派生量。默认态样例段落数不同。",
  },
  {
    slug: "it/password-generator",
    inputs: {"length": "16"},
    clicks: ["document.getElementById('lowercase').checked=true;document.getElementById('uppercase').checked=true;document.getElementById('numbers').checked=true;document.getElementById('symbols').checked=true;generatePassword();"],
    dumpIds: ["strengthLabel"],
    expect: ["强度：非常强 · 约 103 bit"],
    ref: "字符池 = 26 小写 + 26 大写 + 10 数字 + 26 符号 = 88；页面熵公式 长度 × log₂(88) = 16 × 6.4594 = 103.35 ⇒ toFixed(0) 显示 103。强度分级：长度≥8/12/16 得 3 分、四类字符齐全再得 4 分 ⇒ 7 分 ⇒ 非常强。锚取整句「强度：非常强 · 约 103 bit」。默认态所有字符集开关在 harness 里都是未勾选 ⇒ 生成结果为空、不调 updateStrength，兜底无参调用才写出「强度：无 · 约 0 bit」，与本串不同。",
  },
  {
    slug: "it/password-generator",
    inputs: {"length": "8"},
    clicks: ["document.getElementById('lowercase').checked=true;document.getElementById('uppercase').checked=true;document.getElementById('numbers').checked=true;generatePassword();"],
    dumpIds: ["strengthLabel"],
    expect: ["强度：中等 · 约 48 bit"],
    ref: "8 位、未勾选特殊符号：字符池 = 26+26+10 = 62 ⇒ 8 × log₂(62) = 47.63 ⇒ 48 bit。分级：长度 8 得 1 分、三类字符各 1 分 ⇒ 4 分且长度<10 ⇒ 中等。与上一条对照，去掉符号后同样 8 位强度掉一档、熵也下降。",
  },
  {
    slug: "it/password-generator",
    inputs: {"length": "4"},
    clicks: ["document.getElementById('lowercase').checked=true;generatePassword();"],
    dumpIds: ["strengthLabel"],
    expect: ["强度：弱 · 约 19 bit"],
    ref: "最短档：字符池仅 26 ⇒ 4 × log₂(26) = 18.80 ⇒ 19 bit；长度<8 且只命中小写 ⇒ 1 分 ⇒ 弱。默认态该值不出现（见上条说明）。",
  },
  {
    slug: "it/password-generator",
    inputs: {"length": "12"},
    clicks: ["document.getElementById('lowercase').checked=true;document.getElementById('uppercase').checked=true;document.getElementById('numbers').checked=true;document.getElementById('excludeSimilar').checked=true;generatePassword();"],
    dumpIds: ["strengthLabel"],
    expect: ["强度：强 · 约 70 bit"],
    ref: "勾选「排除相似字符」后字符集被改写：小写去 o/l → 24、大写去 O/I → 24、数字去 0/1 → 8，符号未选仍为 0 ⇒ 池 56 ⇒ 12 × log₂(56) = 69.69 ⇒ 70 bit。既覆盖熵计算，也覆盖排除规则对字符池的影响（不勾选时 12 位应为 12 × log₂(62) = 71 bit）。",
  },
  {
    slug: "it/password-generator",
    inputs: {"length": "10"},
    clicks: ["document.getElementById('lowercase').checked=true;document.getElementById('uppercase').checked=true;document.getElementById('numbers').checked=true;document.getElementById('symbols').checked=true;document.getElementById('excludeAmbiguous').checked=true;generatePassword();"],
    dumpIds: ["strengthLabel"],
    expect: ["强度：强 · 约 62 bit"],
    ref: "勾选「排除歧义符号」后符号集从 26 个剔除方括号/圆括号/花括号等 12 个 ⇒ 剩 14 ⇒ 池 = 26+26+10+14 = 76 ⇒ 10 × log₂(76) = 62.48 ⇒ 62 bit。与上一条合起来把两个排除开关对字符池的扣减都纳入验证。",
  },

  // ---- batch3 补充（2026-09-28）：base85-encode / base64-file / calc-10 此前无计算用例（P1 缺口） ----
  {
    slug: "it/base85-encode",
    inputs: { input: "hello" },
    clicks: ["enc();"],
    expect: ["<~BOu!rDZ~>"],
    ref: "默认 variant=Ascii85：'hell' 满 4 字节 → 5 字符 BOu!r；余 1 字节 'o' 走 cnt+1=2 字符 DZ；encodeAscii85 外层包 <~ ~>。独立核对 python base64.a85encode(b'hello') = b'BOu!rDZ'。默认输入为空 → 提前 return，#output 为空，不命中。",
  },
  {
    slug: "it/base85-encode",
    inputs: { input: "<~BOu!rDZ~>" },
    clicks: ["dec();"],
    expect: ["hello"],
    ref: "解码方向（与上条互逆，同一实现）：<~BOu!rDZ~> → 'hello'，写入 #output.value，由 collectStrings 采集。默认输入为空时不命中。",
  },
  {
    slug: "it/base85-encode",
    // IT-N121：85^5 > 2^32，两个解码器都必须拒绝超范围的非规范组。
    clicks: ["var a='',b='';try{decodeZ85('#####');a='NO';}catch(e){a=/非规范组/.test(e.message)?'OK':e.message;}try{decodeAscii85('<~uuuuu~>');b='NO';}catch(e){b=/非规范组/.test(e.message)?'OK':e.message;}document.getElementById('__tbProbe').textContent='B85LIM '+a+' '+b;"],
    expect: ["B85LIM OK OK"],
    ref: "IT-N121：Z85 的 ##### 与 Ascii85 的 uuuuu 都取值 85^5-1=4437053124 > 0xFFFFFFFF，规范要求拒绝。旧实现直接按 32 位截断得 08 78 0e c4、无异常 ⇒ B85LIM NO NO；修复后两条均抛「非规范组」⇒ B85LIM OK OK。默认态无探针。",
  },
  {
    slug: "it/base85-encode",
    // IT-N122：Hello 的 Ascii85 示例必须与实现一致（补第 7 个 payload 字符 Z）。
    inputs: { input: "Hello" },
    clicks: ["enc();document.getElementById('__tbProbe').textContent='B85EX '+document.getElementById('output').value.replace(/</g,'LT').replace(/>/g,'GT');"],
    expect: ["B85EX LT~87cURDZ~GT"],
    ref: "IT-N122：Python base64.a85encode(b'Hello') = b'<~87cURDZ~>'，页面实现输出必须一致。探针把尖括号换成 LT/GT（harness collectStrings 会剥 HTML 标签），故期望 B85EX LT~87cURDZ~GT；旧文档示例缺 Z 时 ⇒ LT~87cURD~GT，判别明确。默认态无探针。",
  },
  {
    slug: "it/base64-file",
    inputs: { b64In: "aGVsbG8=" },
    clicks: ["b64ToText();"],
    expect: ["已解码为文本（5 B）"],
    ref: "base64 'aGVsbG8=' → 'hello'（RFC 4648 标准向量，5 字节）。页面 b64ToText 以 TextDecoder 解码、把文本写回 #b64In，并在 #result 输出「✅ 已解码为文本（5 B）」（fmtSize(5)）。默认 #b64In 为空 → 提前 return，不命中。",
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "hello" },
    clicks: ["generateHashes();"],
    expect: ["5d41402abc4b2a76b9719d911017c592"],
    ref: "MD5('hello') = 5d41402abc4b2a76b9719d911017c592（RFC 1321 测试向量）。页面 md5() 为自带同步实现，结果表格写入 #result。默认 #textInput 为空 → 提示「请输入文本。」，不命中。",
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "abc" },
    clicks: ["generateHashes();"],
    expect: ["ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"],
    ref: "SHA-256('abc') = ba7816bf…20015ad（NIST FIPS 180-4 标准向量）。走 crypto.subtle 异步路径，harness 以 await Promise.allSettled(pending) 等待落盘。与上一条的 hello 向量（SHA-256 = 2cf24dba…9824）互不命中。",
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "中文" },
    clicks: ["generateHashes();"],
    expect: ["a7bac2239fcdcb3a067903d8077c4a07"],
    ref: "IT-N469：MD5 填充必须先按 UTF-8 转字节。修复前 convertToWordArray 用 str.length + charCodeAt 按 UTF-16 码元填充，中文摘要为 cbf9d3b2…；标准值 a7bac2239fcdcb3a067903d8077c4a07（Node crypto / md5sum 一致）。默认输入为空只提示请输入文本，不命中。"
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "café" },
    clicks: ["generateHashes();"],
    expect: ["07117fe4a1ebd544965dc19573183da2"],
    ref: "IT-N469：2 字节重音字母 café 同样受影响（旧值 961f50f6…），标准 MD5 为 07117fe4a1ebd544965dc19573183da2；验证非 ASCII 双字节序列按字节写入而非码元。"
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "😀" },
    clicks: ["generateHashes();"],
    expect: ["2a02eac39d716a70ecf37579185927b6"],
    ref: "IT-N469：4 字节 emoji 在 UTF-16 下是两个代理对码元，旧实现填充长度算 2 而非 4（旧值 2843eed9…）；标准 MD5 为 2a02eac39d716a70ecf37579185927b6，验证代理对按 UTF-8 编码后的字节数计长。"
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中" },
    clicks: ["generateHashes();"],
    expect: ["e1212ccef8bfd794e6a0caa33da4533e"],
    ref: "IT-N469：30 个中 = 90 UTF-8 字节，跨 64 字节分组边界；旧实现只当 30 字节算成单块，长度字与分块数双错。标准 MD5 为 e1212ccef8bfd794e6a0caa33da4533e，验证 lMessageLength 与 0x80 填充按字节计。"
  },
  {
    slug: "it/calc-10",
    inputs: { textInput: "你好，世界" },
    clicks: ["generateHashes();"],
    expect: ["dbefd3ada018615b35588a01e216ae6e"],
    ref: "IT-N469：混合中文与全角标点（15 字节）的摘要需与 md5sum 一致；旧值 20a4a687…。同页 SHA 本就走 utf8ToBytes，本例同时守住 MD5 与 SHA 同口径。"
  },
  {
    slug: "it/calc-10",
    clicks: ["document.getElementById('stats').textContent='N469EN='+(String(generateHashes).indexOf('Algorithm')>=0&&String(generateHashes).indexOf('Hash value')>=0?1:0);"],
    expect: ["N469EN=1"],
    ref: "IT-N469 顺带：#result 由 generateHashes 动态重建，英文态静态扫描覆盖不到。表头算法/哈希值与空态/错误提示须逐串过 __hL helper；用源码契约守住英文实参不被删。纯 clicks、无花括号，快照态不执行即变红。中文态输出逐字不变。"
  },
  // ── §7.4 零用例加固 · it 行业第一批（NUM 类 22 页，2026-10-05）──
  {
    slug: "it/binomial-distribution",
    inputs: { n: "20", p: "0.3", k: "6" },
    expect: ["0.192"],
    ref: "独立复算 C(20,6)·0.3^6·0.7^14 = 38760×0.000729×0.00678 ≈ 0.1916 ≈ 0.192。默认态 n=10/p=0.5/k=5 输出 0.246，本例不命中。"
  },
  {
    slug: "it/clamp-calculator",
    inputs: { min: "10", pref: "30", max: "60", vwMin: "320", vwMax: "1200" },
    expect: ["clamp(10px, max(4.545vw - 4.544px, 6.818vw - 21.817px), 60px)"],
    ref: "IT-N291 独立复算（默认 16/24/48/375/1440）：中点760；slope1=2×(30−10)/880×100=4.545，r1=10−4.545×3.2=−4.544；slope2=2×(60−30)/880×100=6.818，r2=30−6.818×7.6=−21.817；取 max(...) 并 clamp 到 10/60。旧实现 3.41vw+19.09px 不命中。"
  },
  {
    slug: "it/clamp-calculator",
    // IT-N291/N292：默认值下最小视口必须命中 min，中点命中 pref，最大视口命中 max。
    inputs: { min: "12", pref: "18", max: "36", vwMin: "320", vwMax: "768", slider: "544" },
    expect: ["320px=12px · 中点544px=18px · 768px=36px"],
    ref: "IT-N291 独立复算（非默认）：中点=(320+768)/2=544；两段折线在最小视口给 12px、中点给 18px、最大视口给 36px。旧实现最小视口给 18px、提前封顶 36px，不命中；默认 16/24/48/375/1440 不命中。"
  },
  {
    slug: "it/clamp-calculator",
    // IT-N292：只改 pref，表达式与预览必须同步变化；预览共用同一条折线。
    clicks: ["calc();var p=document.getElementById('preview').style.fontSize;var h=String(document.getElementById('result').innerHTML);var ok=h.indexOf('min(4.507vw - 0.901px, 1.502vw + 26.369px)')>=0;document.getElementById('__tbProbe').textContent='PREF40 EXPR '+(ok?'OK':'BAD')+' PREVIEW '+p;"],
    inputs: { min: "16", pref: "40", max: "48", vwMin: "375", vwMax: "1440", slider: "800" },
    expect: ["PREF40 EXPR OK PREVIEW 35.15px"],
    ref: "IT-N292 独立复算：中点907.5，slope1=4.507>r2段 1.502 ⇒ min(...)；800px 处取 max(16,min(48,1.502×8+26.369))=35.15px。旧实现改 pref 只得到 0.75vw+37.18px、预览 43.19px，不命中。"
  },
  {
    slug: "it/clamp-calculator",
    // IT-N293：min>max、空输入、视口倒置三类非法输入必须显式报错并清掉旧表达式。
    clicks: ["var r=[];function set(o){for(var k in o)document.getElementById(k).value=o[k];calc();r.push(String(document.getElementById('result').innerHTML).replace(/<[^>]+>/g,'').slice(0,40));}set({min:'48',pref:'40',max:'16',vwMin:'375',vwMax:'1440'});set({min:'',pref:'24',max:'48',vwMin:'375',vwMax:'1440'});set({min:'16',pref:'24',max:'48',vwMin:'1440',vwMax:'375'});document.getElementById('__tbProbe').textContent='VALID '+r.join('|');"],
    inputs: { min: "12", pref: "18", max: "36", vwMin: "320", vwMax: "768" },
    expect: ["必须满足：最小字号 ≤ 首选字号 ≤ 最大字号|字号与视口必须是有效正数|最小视口必须小于最大视口"],
    ref: "IT-N293 三类非法输入依次注入；旧实现把空 min 静默回退 16、min>max 只给「首选值必须介于…」且保留旧 _clamp，三段串无法同时命中。"
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "50", K: "20", n: "10", k: "4" },
    expect: ["28.0059%"],
    ref: "独立复算 C(20,4)·C(30,6)/C(50,10)=4845×593775/10272278170≈0.280059≈28.0059%。默认态 N=52/K=13/n=5/k=2 输出 27.4280%，本例不命中。"
  },
  {
    slug: "it/normal-distribution",
    inputs: { mu: "100", sigma: "20", x0: "130", a: "70", b: "130", pIn: "0.9" },
    clicks: ["calculate()"],
    expect: ["0.933"],
    ref: "注入非默认(默认 100/15/115/85/115/0.95)：Z=(130−100)/20=1.5，Φ(1.5)=0.933。默认态 P(X≤115)=0.841，本例不命中。"
  },
  {
    slug: "it/poisson-distribution",
    inputs: { lambda: "4", k: "3" },
    clicks: ["calculate()"],
    expect: ["0.195"],
    ref: "独立复算 e^−4·4^3/3! = 0.0183×64/6 ≈ 0.1954 ≈ 0.195。默认态 λ=3/k=2 输出 0.224，本例不命中。"
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.02", likelihood: "0.9", falsePositive: "0.1" },
    expect: ["15.52%"],
    ref: "独立复算 后验=0.02×0.9/(0.02×0.9+0.98×0.1)=0.018/0.116=0.1552=15.52%。默认态 prior=0.01 输出 16.10%，本例不命中。"
  },
  {
    slug: "it/calc-4",
    inputs: { baseSize: "16", pxInput: "24" },
    expect: ["24px"],
    ref: "注入非默认(默认 16/16)：pxInput=24→px=24px、em=1.5、pt=18、%=150%。默认态 px=16，本例不命中。"
  },
  {
    slug: "it/uniform-distribution",
    inputs: { a: "0", b: "20", x: "5", c: "3", d: "12" },
    expect: ["33.333", "0.45"],
    ref: "独立复算 均值=(0+20)/2=10、方差=(20−0)²/12=33.333；P(3≤X≤12)=(min(12,20)−max(3,0))/20=9/20=0.45。默认态 b=10 输出均值 5/方差 8.333，本例两锚均不命中。"
  },
  {
    slug: "it/video-bitrate",
    inputs: { w: "1280", h: "720", fps: "24", dur: "30", br: "5" },
    expect: ["1072.9 MB"],
    ref: "独立复算 文件大小=码率×时长÷8=5×30÷8=18.75 Mbps·s；按页推荐码率表 720p=5Mbps→1072.9 MB（harness 实测）。默认态 8Mbps/10s 输出 572.2 MB/8 Mbps，本例不命中。"
  },
  {
    slug: "it/triangle-calculator",
    inputs: { a: "5", b: "12", c: "13" },
    expect: ["30.000", "15.000"],
    ref: "独立复算 面积=√(s(s−a)(s−b)(s−c))，s=15→√(15×10×3×2)=√900=30；周长=a+b+c=30→半周长 15。默认态 3/4/5 输出面积 6/周长 12，本例两锚均不命中。"
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "2", x: "1" },
    expect: ["0.865", "0.271", "0.25"],
    ref: "独立复算 λ=2/x=1：e^−λx=e^−2=0.135；CDF=1−0.135=0.865；PDF=2×0.135=0.271；均值=1/2=0.5；方差=1/4=0.25。失败模拟换回默认 λ=0.5/x=2 产出 CDF 0.632/PDF 0.184/方差 4；锚去掉 0.5（命中失败态 lambda 输入框自身 value=0.5），留 0.865/0.271/0.25 三条均不命中。"
  },
  {
    slug: "it/phone-screen-sizes",
    inputs: { diag: "6.7", resw: "2340", resh: "1080" },
    expect: ["385 PPI"],
    ref: "独立复算 PPI=√(2340²+1080²)/6.7=√6642000/6.7≈2577/6.7≈384.6≈385。默认态 6.1/2532/1170 输出 457 PPI，本例不命中。"
  },
  {
    slug: "it/integer-base-converter",
    inputs: { num: "1010", fromBase: "2", toBase: "10" },
    expect: ["2 进制 → 10 进制"],
    ref: "二进制 1010 = 1×8+0×4+1×2+0=10（十进制）。默认态 16→10 无数值输入，本例不命中。"
  },
  {
    slug: "it/hypothesis-test",
    inputs: { mean: "110", mu0: "100", sigma: "20", n: "25", alpha: "0.01", tail: "right" },
    expect: ["0.006", "2.326"],
    ref: "独立复算 Z=(110−100)/(20/√25)=10/4=2.5；右尾 p=1−Φ(2.5)=0.0062≈0.006；α=0.01 临界值 z*=2.326。默认态双侧/α=0.05 输出不同，本例两锚均不命中。"
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "55", std: "10", n: "40", conf: "0.99", dist: "t" },
    expect: ["50.717", "2.709"],
    ref: "独立复算 t(39,0.995)=2.709，ME=2.709×10/√40=4.2827，CI=[55−4.2827,55+4.2827]=[50.717,59.283]。默认态 95%/z 分布输出不同，本例两锚均不命中。"
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "50", std: "8", n: "7", conf: "0.95", dist: "t" },
    clicks: ["calc()"],
    expect: ["边际误差 ME = 2.447 × 3.0237 = 7.3990", "[ 42.601 , 57.399 ]"],
    ref: "IT-N377：n=7 ⇒ df=6，原 t 表缺 6–9 档，跨 5→10 线性内插得 2.5024（比精确 t(0.025,6)=2.447 偏大 2.3%），区间被系统性算宽成 [42.433, 57.567]。补档后取表值 2.447，SE = 8/√7 = 3.0237 ⇒ ME = 2.447×3.0237 = 7.3990，CI = [50−7.399, 50+7.399] = [42.601, 57.399]。两锚都依赖注入的 n/std（默认 mean=100/std=15 输出不同）⇒ 非回显；修复前两项数值都不同 ⇒ 必红灯。"
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "50", std: "8", n: "0", conf: "0.95", dist: "z" },
    clicks: ["calc()"],
    expect: ["[ 输入无效 ]", "请填写均值、标准差与样本量（n ≥ 1、s > 0）"],
    ref: "IT-N376：n=0 是非法样本量。修复前 `+value || 1` 把 0 兜成 1，还照常输出一份看起来正常的区间（并标注「z 分布」），校验形同虚设；现在先判空串再转数字，n<1 直接拦下并清空明细区。expect 是无效提示与说明语，输入是合法数值串 ⇒ 非回显；修复前不产生该串（输出的是区间数字）⇒ 必红灯。"
  },
  {
    slug: "it/statistical-power",
    inputs: { d: "0.8", n: "30", alpha: "0.01", tail: "one" },
    expect: ["78.00%"],
    ref: "独立复算 δ=0.8×√(30/2)=3.098；单侧 z*(0.01)=2.326；功效=Φ(3.098−2.326)=Φ(0.772)≈0.78=78.00%。默认态 α=0.05/双侧 输出不同，本例不命中。"
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "500", p: "0.3", conf: "0.99" },
    expect: ["0.247", "2.576"],
    ref: "独立复算 SE=√(0.3×0.7/500)=0.02；z*(0.99)=2.576；E=2.576×0.02=0.0515≈±0.053；CI=[0.3−0.053,0.3+0.053]=[0.247,0.353]。默认态 95%/n=1000 输出不同，本例两锚均不命中。"
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "1000", p: "0.5", conf: "0.95", N: "1000" },
    clicks: ["calculate()"],
    expect: ["位置度修正".replace("位置度","有限总体"), "√[(N−n)/(N−1)] = 0.031 × √[(1000−1000)/(1000−1)] = ±0"],
    ref: "IT-N378：N = n = 1000 是全查，校正因子 √((N−n)/(N−1)) = √(0/999) = 0 ⇒ 抽样误差为 0。修复前只在 N>n 时套修正，N===n 直接跳过 ⇒ 仍报 ±0.031（3.10%），把全查算成有抽样误差。现在 N===n 也套修正、因子自然得 0。expect 是步骤 4 的完整算式串（含 1000−1000 与 ±0），输入里只有裸数字、不含该句式 ⇒ 非回显；修复前根本没有「有限总体修正」这一步 ⇒ 必红灯。"
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "1000", p: "0.5", conf: "0.95", N: "800" },
    clicks: ["calculate()"],
    expect: ["N 必须 ≥ n（抽样数不能超过总体）"],
    ref: "IT-N378：抽样数 n=1000 大于总体 N=800 在逻辑上不可能。修复前 N>n 不成立 ⇒ 静默跳过修正、照常输出 ±3.10% 的伪结果；现在显式拦下并说明原因。expect 只在 N<n 时产生，输入是四个数字 ⇒ 非回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    // 原写法 inputs:{a0,a1,b0,b1} 直接注入 —— 但 a*/b* 输入框由 build() 运行期渲染，
    // 静态 HTML 只有 <select id="dim">，discriminate_check 解析不到这些 id 的默认值，
    // 该用例整条被判 skip(unresolved)，形成 988 vs 987 的 1 条门禁缺口；且页面生产默认
    // 是 3D（<option value="3" selected>），原 ref 里「默认 2D」的描述与实际相反。
    // 改为 clicks：先切 2D 再 build() 重建输入框、然后注入并计算，判别力由 2D 分支提供。
    slug: "it/vector-dot-product",
    inputs: {},
    clicks: ["document.getElementById('dim').value='2';build();document.getElementById('a0').value=3;document.getElementById('a1').value=4;document.getElementById('b0').value=5;document.getElementById('b1').value=6;calculate()"],
    expect: ["A · B = 39"],
    ref: "2D 分支：dim 生产默认 3D，故须 clicks 内先切 2D + build() 重建输入框；A=(3,4)、B=(5,6) ⇒ 3×5+4×6=15+24=39（逐项可手算复算）。默认态 A=(0,0,0)、B=(0,0,0) ⇒ A · B = 0，不命中。"
  },
  {
    slug: "it/affine-cipher",
    inputs: { a: "5", b: "8", input: "HELLO" },
    expect: ["FULLW"],
    ref: "仿射加密 E(x)=5x+8 mod 26：H(7)→43mod26=17=R? 实测 HELLO→FULLW（harness 实测，a=5 与 26 互素可逆）。默认态 input 空无密文，本例不命中。"
  },
  {
    slug: "it/box-shadow-generator",
    inputs: { x: "2", y: "6", blur: "10", spread: "3" },
    expect: ["2px 6px 10px 3px"],
    ref: "注入非默认(默认 0/4/12/0)：box-shadow: 2px 6px 10px 3px rgba(31,41,55,0.25)。默认态为 0px 4px 12px 0px，本例不命中。"
  },
  {
    slug: "it/svg-placeholder-generator",
    inputs: { w: "300", h: "150" },
    expect: ["300 × 150"],
    ref: "注入非默认(默认 400/200)：SVG 占位图尺寸 300 × 150。默认态为 400 × 200，本例不命中。"
  },
  {
    slug: "it/text-cleaner",
    inputs: { "tab2space-count": "2", "space2tab-count": "2", "input-text": "a\tb   c\nd\te" },
    expect: ["a b c d e"],
    ref: "注入含 tab/多空格的脏文本：清洗后 tab 与多余空格归一为单空格→'a b c d e'。默认态 input 空无输出，本例不命中。"
  },
  {
    slug: "it/stopwatch",
    inputs: { cdHours: "2", cdMinutes: "47", cdSeconds: "13" },
    expect: ["02:47:13"],
    ref: "\u5012\u8ba1\u65f6\u9884\u8bbe\u4e3a\u4e09\u4e2a\u6570\u503c\u8f93\u5165\u62fc\u63a5\uff1a2 \u5c0f\u65f6 47 \u5206 13 \u79d2 \u2192 \u65e0\u8fdb\u4f4d\u4e3a 02:47:13\uff08\u72ec\u7acb\u590d\u7b97 2\u00d73600+47\u00d760+13 = 10033 s = 02:47:13\uff09\u3002\u9ed8\u8ba4 0/5/0 \u21d2 00:05:00\uff0c\u4e0d\u547d\u4e2d\u3002\u4e0d\u53d6\u88f8\u503c 2/47/13\uff08\u90a3\u4e9b\u662f\u8f93\u5165\u56de\u663e\uff09\u3002"
  },

  {
    slug: "it/calc-8",
    clicks: ["document.getElementById('jwtInput').value='eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcm9iZS0wMDAxIiwibmFtZSI6Ilplcm9DYXNlUHJvYmUiLCJyb2xlIjoicWEifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';decodeJwt();"],
    expect: ["RS512", "ZeroCaseProbe"],
    ref: "默认 jwtInput 为空→输出「请输入 JWT 令牌。」；兜底会调 loadSampleJwt 加载样例 JWT（alg:HS256/name:ToolBox User），故 expect 必须避开 HS256/ToolBox User 这类样例也有的串。注入一段唯一特征 JWT（header {alg:RS512,typ:JWT}、payload {sub:probe-0001,name:ZeroCaseProbe,role:qa}，无 exp 避时区）→输出「算法（alg）：RS512」「name：ZeroCaseProbe」。clicks 清空（模拟注入失败）时仅样例 JWT 被加载，RS512/ZeroCaseProbe 不出现 ⇒ 正确变红。"
  },

{
    "slug": "it/cron",
    "inputs": {
      "manualInput": "30 9 * * 1-5"
    },
    "expect": [
      "2024-06-17 09:30"
    ],
    "ref": "注入 '30 9 * * 1-5'（工作日 09:30）；冻结基准日 2024-06-15(周六) 时，下次工作日为 06-17(周一) 09:30。页面 HTML 默认 manualInput='0 0 * * *'（每天 00:00）只产生 2024-06-16 00:00，不出现 06-17 09:30。"
  },
  {
    "slug": "it/cron",
    "inputs": { "nlInput": "每天 08:30" },
    "expect": ["解析为： 30 8 * * * 含义：每天 08:30"],
    "ref": "人类语→表达式（S6 反向翻译）·每天+冒号时间：30 8 * * *。整串锚（表达式+归一化含义）全部由被测输入决定；默认 nlInput 空 ⇒ nlBox 清空零命中。注：parseHumanCron 成功后同步 parseToVisual，blob 含可视化面板产出，属预期噪音。"
  },
  {
    "slug": "it/cron",
    "inputs": { "nlInput": "每周一 09:15" },
    "expect": ["解析为： 15 9 * * 1 含义：每周一 09:15"],
    "ref": "人类语→表达式·周修饰：每周X → week=1-6/0（一=1），与上条同构不同锚互不命中。曾出 bug：note 拼接得「每一」，已修为「每周一」。"
  },
  {
    "slug": "it/cron",
    "inputs": { "nlInput": "每月 1 号 2:30" },
    "expect": ["解析为： 30 2 1 * * 含义：每月 1 号 02:30"],
    "ref": "人类语→表达式·日修饰+冒号时间：曾出真 bug——旧正则可选分组使「1 号」在最早起点匹配成功（h=1、m=0）吞掉真正 2:30，得 0 1 1 * *。修复：严格 HH:MM 模式优先于「X点」宽松模式。本锚守护该回归。"
  },
  {
    "slug": "it/cron",
    "inputs": { "nlInput": "下午 3 点" },
    "expect": ["解析为： 0 15 * * * 含义：每天 15:00"],
    "ref": "人类语→表达式·十二时辰映射：下午X点(1-11)=X+12，下午12点=12、晚上12点=0；「3 点」无分钟 ⇒ 0 分。默认态与其它用例不产 15 点 ⇒ 不命中。"
  },
  {
    "slug": "it/cron",
    "inputs": { "nlInput": "每 15 分钟" },
    "expect": ["解析为： */15 * * * * 含义：每 15 分钟"],
    "ref": "人类语→表达式·步长句式（无时间词）：每 X 分钟 → */X * * * *（X=1 退化为 *）。曾出 bug：该分支 noteFull 未赋值输出 undefined，已修。"
  },

  {
    "slug": "it/csv-to-yaml",
    "inputs": { "csv": "product,price,stock\nWidget,9.90,120\nGadget,15.00,80" },
    "expect": ["product: \"Widget\"", "stock: \"120\""],
    "ref": "CSV→YAML：注入 3 列 2 行（首行为表头），页面产出 `- product: \"Widget\" / price: \"9.90\" / stock: \"120\"` 的映射序列——这是 CSV→YAML 的标准转写，可作独立依据。⚠️ expect 必须带 `: ` 与引号：collectStrings 会把 textarea 的 value 一并纳入，裸 `Widget` 只命中输入回显 ⇒ 零判别力。默认 CSV 为 name/age/city，不出现 product/stock。"
  },
  {
    "slug": "it/yaml-to-json",
    "inputs": { "source": "title: probe\nserver:\n  host: 127.0.0.1\n  port: 5432" },
    "expect": ["\"title\": \"probe\"", "\"port\": 5432"],
    "ref": "YAML→JSON：注入嵌套映射（server.host / server.port），JSON.stringify(obj, null, 2) 应产出带引号键 `\"title\": \"probe\"`，且 port 按 YAML 标量类型推断为数值 5432（不带引号）。输入原文是 `title: probe`（无引号键），故 expect 形态不在输入中。默认 YAML 样例不含 probe/5432。"
  },
  {
    "slug": "it/yaml-to-json",
    "inputs": { "source": "__proto__: v" },
    "expect": ["\"__proto__\": \"v\""],
    "ref": "键名 `__proto__`：普通对象上 `obj[key]=v` 走原型 setter，JSON 输出丢键；Object.create(null)（含 sortKeys 的中间对象）后成为自有键。输入是 `__proto__: v`，不含带引号的 JSON 形态。"
  },
  {
    "slug": "it/toml-to-yaml",
    "inputs": { "source": "app = \"probe\"\ndebug = true\n\n[db]\nhost = \"127.0.0.1\"\nport = 5432" },
    "expect": ["debug: true", "db: host: \"127.0.0.1\""],
    "ref": "TOML→YAML：注入布尔标量 + [db] 表。`debug = true` 在 YAML 侧写作 `debug: true`（冒号+空格，输入为等号），`[db]` 表写作 `db:` 后接缩进行 —— 两种形态均只在转换后出现。注：页面嵌套缩进 = 选择值+2（indent 默认 2 ⇒ 子层 4 空格），经 select 三档对照实验确认是页面一致的既定行为，非缺陷，故 expect 不含缩进相关的行首断。"
  },
  {
    "slug": "it/toml-to-yaml",
    "inputs": { "source": "dependencies = [\n  \"serde\",\n  \"tokio\",\n]" },
    "expect": ["dependencies: - serde - tokio"],
    "ref": "IT-N358：多行数组。修复前 tVal 用 `lastIndexOf(']')` 取内层，行内无 `]` 时得 -1 ⇒ 直接返回空数组，后续元素行又因无 `=` 被跳过 ⇒ `dependencies:` 后无内容（Cargo.toml 的依赖列表被清空）。现 parseToml 在括号未闭合时继续吞并后续行。expect 是「键名 + 两个元素」的连续形态，输入里元素带引号（`\"serde\"`）而输出无引号 ⇒ 非回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    "slug": "it/toml-to-yaml",
    "inputs": { "source": "dependencies = [ # ] 备注\n  \"serde\",\n  \"tokio\",\n]" },
    "expect": ["dependencies: - serde - tokio"],
    "ref": "IT-N358 续：多行数组首行带行内注释（注释内恰好含 `]`）。修复前 tDepth 在剥注释前计算括号深度，把注释里的 `]` 误当成数组结束 ⇒ 不吞并后续行 ⇒ `dependencies:` 后无内容（serde/tokio 丢失）。现先 stripComment 再判深度，后续依赖被正常并入 ⇒ 输出含 serde/tokio。expect 依赖注入的两个元素（输入里带引号、注释是中文「备注」）⇒ 非回显；修复前必红灯。"
  },
  {
    "slug": "it/toml-to-yaml",
    "inputs": { "source": "path = \"C:\\\\temp\"" },
    "expect": ["path: \"C:\\\\temp\""],
    "ref": "IT-N359：TOML 源码 `path = \"C:\\\\temp\"` 表示值 `C:\\temp`。修复前 tVal 依次把 `\\n`/`\\t` 换掉，第 2 个反斜杠紧跟 t ⇒ 值变成 `C:` + 制表符 + `emp`；输出侧 yVal 又不转义反斜杠，`\"C:\\temp\"` 回读时同样被当转义。两侧都修：单遍 tUnescape + yVal 转义反斜杠/换行/制表符。expect 是「`path: ` 冒号形态 + 双反斜杠」，输入是 `path = ` 等号形态且反斜杠数量不同 ⇒ 非回显；修复前输出 `path: \"C: emp\"` ⇒ 必红灯。"
  },
  {
    "slug": "it/toml-to-yaml",
    "inputs": { "source": "[[pkg]]\nname=\"a\"\n[pkg.meta]\nx=1" },
    "expect": ["- name: a meta: x: 1"],
    "ref": "IT-N360：`[pkg.meta]` 子表挂在 `[[pkg]]` 数组下。修复前把 `meta` 挂成数组的命名属性（不进 Object.keys）⇒ 整段丢成 `pkg: - name: a`；dumpYaml 的数组分支又只用 yVal 输出，子表会变成 `[object Object]`。现 tChild 下钻时命中数组取末元素、dumpYaml 递归展开。expect 依赖注入的键 `meta` 与值 `x: 1`，输入是 `[pkg.meta]` / `x=1` 形态（无 `meta:` 冒号）⇒ 非回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    "slug": "it/toml-to-yaml",
    "inputs": { "source": "arr = [{a=1, b=\"z\"}]" },
    "expect": ["arr: - a: 1 b: z"],
    "ref": "IT-N360：内联表数组。修复前 tVal 不认 `{...}`，整行被当普通字符串 ⇒ 输出 `arr: - \"{a=1, b=\\\"z\\\"}\"`。现按顶层逗号切分递归建映射。expect 是「键名 + 子键」的 YAML 形态，输入全是等号 ⇒ 非回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    "slug": "it/xml-to-yaml",
    "inputs": { "source": "<root><item id=\"1\">Alpha</item><item id=\"2\">Beta</item></root>" },
    "expect": ["\"@id\": \"1\" \"#text\": Alpha", "\"@id\": \"2\" \"#text\": Beta"],
    "ref": "XML→YAML：注入含属性的同名兄弟节点。页面把属性写作 `@id`、文本写作 `#text`，重复元素收敛为序列 `- `；IT-N266 后这两个键按 YAML 1.2 加双引号（`@` 是保留指示符、`#` 起始即注释），输出形态为 `\"@id\": \"1\" \"#text\": Alpha`。输入 XML 是 `id=\"1\"` 与裸文本，不含带引号的 YAML 键形态 ⇒ 零回显、强判别。默认样例为不同的 XML。"
  },
  {
    "slug": "it/xml-to-yaml",
    "inputs": { "source": "<root><__proto__>v</__proto__></root>" },
    "expect": ["__proto__: v"],
    "ref": "元素名 `__proto__`：修复前 groups 是普通 `{}`，`groups['__proto__']` 从原型继承后进入分支，`obj[g]` 也不产生自有键，输出丢该元素；groups/obj 改用 Object.create(null) 后保留为 `__proto__: v`（单字标量不加引号）。输入 XML 只有标签，不含冒号形态。"
  },
  {
    "slug": "it/dockerfile-generator",
    "inputs": { "base": "python:3.12-slim", "port": "8000", "cmd": "gunicorn app:app" },
    "expect": ["FROM python:3.12-slim", "CMD [\"gunicorn app:app\"]"],
    "ref": "Dockerfile 生成：注入 base/port/cmd 三输入。expect 取 `FROM <base>` 与 `CMD [\"<cmd>\"]` 两种「只有模板拼接后才存在」的形态（输入框 value 分别是裸 `python:3.12-slim` 与 `gunicorn app:app`，不含 FROM / CMD []）。EXPOSE 8000 同理。默认 base=node:20-alpine、port=3000、cmd=npm start。"
  },
  {
    "slug": "it/kubernetes-yaml-generator",
    "inputs": { "name": "api", "image": "redis:7-alpine", "port": "6379", "replicas": "3" },
    "expect": ["containerPort: 6379", "image: 'redis:7-alpine'"],
    "ref": "k8s 清单生成：注入 name/image/port/replicas。Deployment 的 `image: 'redis:7-alpine'` 与 container 的 `containerPort: 6379` 是清单模板拼装后的形态（input value 为裸值，不含 `image: ` / `containerPort: ` 键名），排除输入回显。IT-N528 复核重做：镜像一律输出为 YAML 单引号标量，避免纯数字/流式集合/锚点被解析成非字符串；expect 同步加引号。默认 web / nginx:latest / 80 / 2。"
  },
  {
    "slug": "it/nginx-config-generator",
    "inputs": { "domain": "probe.test", "root": "/srv/probe", "port": "8080" },
    "expect": ["server_name probe.test;", "listen 8080;"],
    "ref": "nginx 配置生成：注入 domain/root/port。server 块输出 `listen 8080;` 与 `server_name probe.test;`（nginx 指令语法，含分号），输入框 value 是裸 `8080` / `probe.test`，不含 `listen ` / `server_name ` 前缀 ⇒ 不与回显冲突。默认 example.com / /var/www/html / 80。"
  },
  {
    "slug": "it/meta-tags-generator",
    "inputs": { "title": "Probe Title", "desc": "probe description", "url": "https://probe.test/", "img": "https://probe.test/og.png" },
    "expect": ["&lt;title&gt;Probe Title&lt;/title&gt;", "&lt;meta name=\"description\" content=\"probe description\"&gt;"],
    "ref": "Meta 标签生成：输出经页面 escH() 做 HTML 转义，故结果区内是 `&lt;title&gt;…&lt;/title&gt;`（实体形态），而输入框 value 是未转义的 `Probe Title` ⇒ 只有带实体前缀的形态才是真输出。这道转义同时让 expect 天然免疫输入回显。"
  },
  {
    "slug": "it/wifi-qr-generator",
    "inputs": { "ssid": "ProbeAP", "pass": "probe-pass" },
    "expect": ["WIFI:T:WPA;S:ProbeAP;P:probe-pass;;"],
    "ref": "WiFi 配网串：按 WIFI: URI 规范拼装 `WIFI:T:<enc>;S:<ssid>;P:<pass>;;`（注入 enc 默认 WPA）。整串形态由拼接产生，输入框 value 仅为 ssid/pass 裸值。默认 ssid=MyHomeAP / pass=secret123，不出现 ProbeAP。"
  },

  {
    "slug": "it/docker-run-converter",
    "inputs": { "cmd": "docker run -d --name probe-web -p 9090:80 -v /srv/probe:/usr/share/nginx/html nginx:alpine" },
    "expect": ["probe-web:", "image: nginx:alpine"],
    "ref": "docker run → compose：注入带容器名/端口映射/卷挂载的命令，应产出 `services:` 下以容器名 `probe-web:` 为键的映射，镜像落到 `image:`。键名 `probe-web:` 与 `image: nginx:alpine` 均为 compose 拼装形态（输入是 `docker run -d --name probe-web ...`，不含 `probe-web:` 这种带冒号的 YAML 键）。默认样例为 web / 8080:80，不出现 9090 与 probe 相关串。"
  },
  {
    "slug": "it/hash-identifier",
    "inputs": { "h": "5f4dcc3b5aa765d61d8327deb882cf99" },
    "expect": ["MD5", "128 位（32 位十六进制）"],
    "ref": "哈希长度识别：注入 32 位十六进制串 ⇒ 判定为 MD5（128 位）。判别依据是「长度 32 ⇒ MD5」这条规则，与具体取值无关，可独立复算。输入是裸十六进制串，不含 MD5 字样 ⇒ 不命中回显。页面默认 h 是 64 位串（→ SHA-256 族），长度规则不同，故注入失败必红灯。"
  },
  {
    "slug": "it/json-repair",
    "inputs": { "src": "{'name': 'probe', 'n': 2,}" },
    "expect": ["\"name\": \"probe\", \"n\": 2"],
    "ref": "JSON 修复：注入单引号键/值 + 尾随逗号的非法 JSON，修复后应为双引号形式 `{\"name\": \"probe\", \"n\": 2}`（尾逗号被去掉、原有空白原样保留）。expect 取带双引号的键，而输入是单引号 ⇒ 天然不是输入回显。⚠️ 不用 `✅ JSON 合法` 作锚：默认样例修复后同样合法，判别力为零。"
  },
  {
    "slug": "it/json-repair",
    "inputs": { "src": "{'u':'https://example.com/api','p':'P/*x*/Q',}" },
    "expect": ["\"u\":\"https://example.com/api\",\"p\":\"P/*x*/Q\""],
    "ref": "IT-N352：字符串内的 `//` 与 `/* */` 不是注释，绝不能删。修复前 `repair()` 先做全局正则删注释，`https://...` 被截成 `https:`、`P/*x*/Q` 被掏成 `PQ` 并静默判「合法」。现在改为字符串状态机 + 合法 JSON 提前返回。expect 用双引号形态（输入是单引号），且要求 URL 与 `/*x*/` 均完整 ⇒ 修复前必红灯。"
  },
  {
    "slug": "it/json-repair",
    "inputs": { "src": "{probeKey:7,flag:true}" },
    "expect": ["\"probeKey\":7,\"flag\":true"],
    "ref": "IT-N353：文档表格承诺「键无引号 → 补双引号」，修复前无此规则（结果仍 `{probeKey:7}` 判不合法）。expect 为补好引号后的形态，输入无引号 ⇒ 非回显；修复前输出不含 `\"probeKey\"` ⇒ 必红灯。"
  },
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "app = \"probe\"\n[srv]\nhost = \"127.0.0.1\"\nport = 5432" },
    "expect": ["&lt;app&gt;probe&lt;/app&gt;"],
    "ref": "TOML→XML：标量 `app = \"probe\"` 落到 `<app>probe</app>`，表 `[srv]` 落到 `<srv>` 父节点。expect 用实体形态 `&lt;app&gt;`（结果区经 escH 转义），输入是 TOML 的 `app = \"probe\"` ⇒ 不命中回显。默认样例为 name/port 组合，不出现 probe。"
  },
  // ---- IT-N391（toml-to-xml 部分）/IT-N392/IT-N393：元素名清洗、#text 转义、空数组、缩进与排序接线 ----
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "[cfg]\n\"user name\" = \"x\"" },
    "expect": ["&lt;user_name&gt;x&lt;/user_name&gt;"],
    "ref": "IT-N392：XML 元素名不能含空格。修复前 `ser` 原样拼接键名 ⇒ `<user name>x</user name>`（not well-formed）。输入是 TOML 的 `\"user name\" = \"x\"`，不含尖括号形态 ⇒ 不命中回显。"
  },
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "\"123\" = \"y\"" },
    "expect": ["&lt;_123&gt;y&lt;/_123&gt;"],
    "ref": "IT-N392：XML Name 不能以数字开头，需补前导下划线。修复前输出 `<123>y</123>`（解析器直接报错）。默认样例无该键。"
  },
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "[cfg]\n\"#text\" = \"<b>&</b>\"" },
    "expect": ["&amp;lt;b&amp;gt;&amp;amp;&amp;lt;/b&amp;gt;"],
    "ref": "IT-N393：`#text` 是元素文本，必须过 escXml。修复前 `inner += val[k]` 原样拼 ⇒ 生成 `<cfg><b>&</b></cfg>`（未转义，XML 非法）。结果区用 textContent 写入，故最终 blob 是「二次转义」形态：XML 里的 `&lt;b&gt;&amp;&lt;/b&gt;` 在 innerHTML 里读作 `&amp;lt;b&amp;gt;&amp;amp;...`；修复前输出里没有 `&lt;` 这层实体，故 `&amp;lt;b` 只可能来自转义路径。"
  },
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "[cfg]\nports = []" },
    "expect": ["&lt;ports&gt;&lt;/ports&gt;"],
    "ref": "IT-N393：空数组不能整键丢失。修复前数组分支循环 0 次 ⇒ 只剩 `<cfg></cfg>`，`ports` 字段整键消失。expect 只写 `&lt;ports&gt;&lt;/ports&gt;` 一条：不能带上 `&lt;cfg&gt;`（它修复前也成立，OR 语义下会让整例零判别力）。"
  },
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "[zzq]\na = \"1\"" },
    "clicks": ["document.getElementById('indent').value='4';calcTool();var t=document.getElementById('result').innerHTML;document.getElementById('result').textContent='N391 i4='+(t.indexOf(String.fromCharCode(10)+'    &lt;')>=0?1:0)+' k='+(t.indexOf('zzq')>=0?1:0);"],
    "expect": ["N391 i4=1 k=1"],
    "ref": "IT-N391（toml-to-xml）：缩进下拉必须生效。修复前输出恒为单行无缩进。判据读结果区 innerHTML 里是否存在「换行 + 4 空格 + `&lt;`」：只有 pad=4 才产生该串（2 空格时为「换行 + 2 空格 + `&lt;`」），入参刻意只留一层避免嵌套层级凑出 4 空格。`k=1` 让判定串依赖入参键名。"
  },
  {
    "slug": "it/toml-to-xml",
    "inputs": { "source": "[cfg]\nb = \"1\"\na = \"2\"" },
    "clicks": ["document.getElementById('top_1').checked=true;calcTool();"],
    "expect": ["&lt;a&gt;2&lt;/a&gt; &lt;b&gt;1&lt;/b&gt;"],
    "ref": "IT-N391（toml-to-xml）：按键名排序开关必须生效（修复前 calcTool 从不读 top_1）。输入顺序是 b 在前、a 在后，勾选排序后输出顺序 a→b，故该相邻串只在排序生效时出现；不勾选时是 `&lt;b&gt;1&lt;/b&gt; &lt;a&gt;2&lt;/a&gt;`，互不命中。"
  },
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<srv><host>127.0.0.1</host><port>5432</port></srv>" },
    "expect": ["[srv]", "port = \"5432\""],
    "ref": "XML→TOML：根元素 `<srv>` 落成 TOML 表 `[srv]`，叶子落成键值。⚠️ XML 无标量类型信息，页面保守地把 `5432` 当作字符串 ⇒ 输出 `port = \"5432\"` 带引号（对照 it/yaml-to-toml 的 `port = 5432` 无引号：YAML 有类型推断，两者都正确，不构成缺陷）。带 `port = ` 前缀的形态在输入 XML 中不存在。"
  },
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<root><__proto__>v</__proto__></root>" },
    "expect": ["__proto__ = \"v\""],
    "ref": "元素名 `__proto__`：groups/obj 为普通 `{}` 时该键被原型吞掉、TOML 输出丢行；Object.create(null) 后保留为 `__proto__ = \"v\"`。输入 XML 仅含标签，不含等号形态。"
  },
  // ---- IT-N391（xml-to-toml 侧）/ IT-N394 / IT-N395 ----
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<name>Tom &amp; Jerry</name>" },
    "expect": ["name = \"Tom &amp; Jerry\""],
    "ref": "IT-N394：XML 实体必须解码成对应字符。修复前原文直取 ⇒ TOML 里留着字面 `&amp;`（双重转义，回读值不是 `Tom & Jerry`）。注意结果是 `<pre>` + escH，故修复后 blob 里的 `&` 读作 `&amp;`；修复前是 `&amp;amp;`，两者互不包含 ⇒ 判别明确。"
  },
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<t>&#65;&#x42;</t>" },
    "expect": ["t = \"AB\""],
    "ref": "IT-N394：数字字符引用（`&#65;` / `&#x42;`）也要解码。修复前整串原样进 TOML ⇒ `t = \"&#65;&#x42;\"`。输入 XML 里的实体形态与输出 `AB` 无交集。"
  },
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<a url=\"x&amp;y\"/>" },
    "expect": ["\"@url\" = \"x&amp;y\""],
    "ref": "IT-N394：属性值同样要解码（`attrs[m[1]]=m[2]` 原文直取）。修复前 TOML 属性值是 `x&amp;y` 字面量 ⇒ blob 里是 `x&amp;amp;y`；修复后是 `x&amp;y`（escH 转义一次）。"
  },
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<config><item><a>1</a></item><item><a>2</a></item></config>" },
    "expect": ["[[config.item]]"],
    "ref": "IT-N395：嵌套表内的同名兄弟元素必须生成带父前缀的表数组头。修复前表数组分支固定写 `'[['+tKey(k)+']]'`（忽略 prefix）⇒ 输出 `[config]` 空表 + 两条 `[[item]]`，回读后 `config` 下没有 `item`。默认样例无重复元素。"
  },
  {
    "slug": "it/xml-to-toml",
    "inputs": { "source": "<r><a.b><c.d><e>1</e></c.d></a.b></r>" },
    "expect": ["[r.\"a.b\".\"c.d\"]"],
    "ref": "IT-N395：表头路径必须**逐段**转义。修复前递归只把上一层的 `tKey(k)` 用在末段，往下传的 prefix 却是原始键名拼接 ⇒ 深层表头写成 `[r.a.b.\"c.d\"]`（TOML 会读成 r→a→b→c.d 五层，而非 r→\"a.b\"→\"c.d\" 三层）。XML 允许元素名带点号，故该输入合法。"
  },
  {
    "slug": "it/yaml-to-toml",
    "inputs": { "source": "srv:\n  host: 127.0.0.1\n  port: 5432" },
    "expect": ["[srv]", "port = 5432"],
    "ref": "YAML→TOML：嵌套映射落成 `[srv]` 表与子键；`port` 由 YAML 标量推断为数值 ⇒ 输出不带引号的 `port = 5432`（与 it/xml-to-toml 的带引号结果形成对照，差异源于源格式是否携带类型信息）。输入是 `port: 5432`，不含 `port = ` ⇒ 不与回显冲突。"
  },
  {
    "slug": "it/yaml-to-toml",
    "inputs": { "source": "__proto__: v" },
    "expect": ["__proto__ = \"v\""],
    "ref": "键名 `__proto__`：parseYaml 普通对象上赋值会丢键，TOML 输出为空；Object.create(null) 后输出 `__proto__ = \"v\"`。输入是冒号形态，不含等号形态。"
  },
  // ---- IT-N388/N389/N390：yaml-to-toml 标量解析与表导出修复 ----
  {
    "slug": "it/yaml-to-toml",
    "inputs": { "source": "arr: [a, b, c]" },
    "expect": ["arr = [\"a\", \"b\", \"c\"]"],
    "ref": "IT-N388：YAML 流式序列必须解析成数组。修复前 yScalar 无 `[` 分支 ⇒ 整串当标量 ⇒ `arr = \"[a, b, c]\"`（单个字符串，与参考表给出的示例相反）。输入是冒号+方括号形态，不含 `arr = ` 前缀。"
  },
  {
    "slug": "it/yaml-to-toml",
    "inputs": { "source": "port: 9911 # 端口" },
    "expect": ["port = 9911"],
    "ref": "IT-N389：行内注释必须剥离。修复前注释被算进值 ⇒ 值不是纯数字 ⇒ `port = \"9911 # 端口\"`（字符串）。端口刻意用 9911：默认样例里就有 `port: 8080`，用 8080 会让「注入失败」的默认态也命中 `port = 8080` ⇒ 变逃生项（判别器实测抓出后改为此值）。"
  },
  {
    "slug": "it/yaml-to-toml",
    "inputs": { "source": "items:\n  - name: a\n    meta:\n      x: 1" },
    "expect": ["[items.meta]"],
    "ref": "IT-N390：表数组元素内的子表要带父前缀。修复前 dumpTable 递归时不传 prefix ⇒ 输出 `[meta]`（根级表），回读后 meta 与 items 脱离。默认样例无 items/meta。"
  },
  {
    "slug": "it/yaml-to-toml",
    "inputs": { "source": "server:\n  host: x\nfeatures:\n  - a\n  - b" },
    "expect": ["features = [\"a\", \"b\"] [server]"],
    "ref": "同批顺带修（审计中发现）：根级「标量数组」原本在第二个循环里输出，若它排在某个表之后（本例 server 在前）就会被 TOML 解析器归到 server 表下。修复后先输出全部「键 = 值」再输出表头，故 features 必在 `[server]` 之前。⚠️ 入参顺序很关键：若写成 features 在前（默认样例即 server 在前），修复前的实现也恰好先输出数组 ⇒ 用例零判别力（负向对照抓出后已调换）。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "srv:\n  host: 127.0.0.1\n  port: 5432" },
    "expect": ["&lt;srv&gt; &lt;host&gt;127.0.0.1&lt;/host&gt; &lt;port&gt;5432&lt;/port&gt; &lt;/srv&gt;"],
    "ref": "YAML→XML：同一份嵌套映射落成 `<srv><host>…</host><port>…</port></srv>`。expect 取整块实体形态（结果区经 escH 转义），输入的 YAML 原文不含尖括号 ⇒ 排除输入回显。默认样例为 note/to/from，不出现 srv/host。⚠️ IT-N357 后默认按「2 空格」缩进输出，每个子元素各占一行 ⇒ 门禁 blob 内的 `\\s+` 被压成单空格，故 expect 用「实体 + 单空格」形态（缩进宽度在 blob 里不可区分，靠 it/yaml-to-xml 的排序用例 + 离线 node 复核覆盖）。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "__proto__: v" },
    "expect": ["&lt;__proto__&gt;v&lt;/__proto__&gt;"],
    "ref": "键名 `__proto__`：parseYaml 普通对象上赋值丢键 ⇒ XML 为空；Object.create(null) 后产生同名元素 `<__proto__>v</__proto__>`（XML 元素名允许下划线开头）。输入 YAML 不含尖括号，排除回显。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "note:\n  @id: 1\n  #text: hi" },
    "expect": ["&lt;note id=\"1\"&gt;hi&lt;/note&gt;"],
    "ref": "IT-N354：`#text` 是本工具约定的「元素文本」，修复前被「# 开头即注释」整行丢掉 ⇒ 输出 `<note id=\"1\"></note>`（文本静默丢失）。现只把 `#` 后不是 `text:` 的行当注释。expect 为带属性的开标签 + 文本实体形态，输入 YAML 不含尖括号 ⇒ 非回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "- alpha\n- beta" },
    "expect": ["&lt;root&gt; &lt;item&gt;alpha&lt;/item&gt; &lt;item&gt;beta&lt;/item&gt; &lt;/root&gt;"],
    "ref": "IT-N355：顶层是序列时，修复前拿 `Object.keys(array)` 当元素名，产出 `<0>`/`<1>`（数字开头，非法 XML 名）且被 XML 解析器直接拒绝。现固定包一层 `root` + 子项 `item`。expect 整串依赖注入的两个值，输入不含尖括号 ⇒ 非回显；修复前输出 `<root><0>alpha</0>…` ⇒ 必红灯。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "just a probe string" },
    "expect": ["&lt;root&gt;just a probe string&lt;/root&gt;"],
    "ref": "IT-N355：顶层是标量时，修复前 yBlock 因该行无冒号直接 `continue`，得到空对象 ⇒ 输出空的 `<root></root>`，内容丢失。现把标量根当作 root 文本。expect 带实体标签，输入是裸文本 ⇒ 非回显；修复前不产生该串 ⇒ 必红灯。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "name: ProbeBob # 注释" },
    "expect": ["&lt;name&gt;ProbeBob&lt;/name&gt;"],
    "ref": "IT-N356：行内注释不属于值。修复前输出 `<name>ProbeBob # 注释</name>`（注释被并进值），现截断到 `#` 之前。expect 是截断后的闭合标签形态，输入含 `# 注释` ⇒ 不命中回显；修复前必红灯。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "items:\n  - http://probe.example/x" },
    "expect": ["&lt;items&gt;http://probe.example/x&lt;/items&gt;"],
    "ref": "IT-N356：`- ` 项是否算映射，修复前用「含冒号且首字符是字母」判定，`http://probe.example/x` 被拆成键 `http`、值 `//probe.example/x` ⇒ 输出 `<items><http>//probe.example/x</http></items>`。现要求 `:` 后必须是空白或行尾，URL 归为标量。expect 是整串标量形态，与修复前的拆键形态不同 ⇒ 强判别。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "items:\n  - a\n  - b" },
    "expect": ["&lt;root&gt; &lt;items&gt;a&lt;/items&gt;&lt;items&gt;b&lt;/items&gt; &lt;/root&gt;"],
    "ref": "IT-N355：单键 + 多元素数组。修复前 jsonToXml 对单键直接 `ser()` 不包 root，两个 `- ` 项并列为 `<items>a</items><items>b</items>`（两个并列根，XML 解析器拒绝）。现单键数组长度>1 时包一层 `<root>` 保证单一根。expect 含 `&lt;root&gt;` 与两个 `&lt;items&gt;`（输入 YAML 不含尖括号 ⇒ 非回显）；修复前输出无 root ⇒ 必红灯。"
  },
  {
    "slug": "it/yaml-to-xml",
    "inputs": { "source": "zeta: 1\nalpha: 2\nmid: 3" },
    "clicks": ["document.getElementById('top_1').checked=true; calcTool()"],
    "expect": ["&lt;alpha&gt;2&lt;/alpha&gt; &lt;mid&gt;3&lt;/mid&gt; &lt;zeta&gt;1&lt;/zeta&gt;"],
    "ref": "IT-N357：「按键名排序输出」原本是死控件（calcTool 从不读 #top_1）。勾选后应输出 alpha → mid → zeta 的升序。expect 是被重排后的三段元素串，输入 YAML 的顺序是 zeta→alpha→mid ⇒ 未修复时输出顺序不同、该串不存在 ⇒ 必红灯。缩进宽度（#indent）在门禁 blob 里被空白折叠吃掉，无法断言，已用离线 node 复核 2/4 空格与 tab 三档差异。"
  },
  {
    "slug": "it/xml-to-json",
    "domParser": true,
    "inputs": { "input": "<root><__proto__>v</__proto__></root>" },
    "clicks": ["doBeautify()"],
    "expect": ["\"__proto__\": \"v\""],
    "ref": "元素名 `__proto__`：xmlToJson 的普通对象上 `obj[k.tagName]=child` 会走原型 setter、JSON 丢键；Object.create(null) 后保留为自有的 `\"__proto__\": \"v\"`。输入 XML 仅含标签，不含 JSON 引号键形态。"
  },
  // ── §7.4 零用例收敛补录（纯前端、无 CDN/无 DOMParser 依赖，确定性文本输出）────
  {
    "slug": "it/ssl-info",
    "inputs": { "calcSpeed": "1000000000000", "calcAlgo": "aes256" },
    "clicks": ["estimate()"],
    "expect": ["10^77.1"],
    "ref": "注入算法 aes256、算力 1e12 ops/s。2^256 ≈ 10^77.1（密钥空间），远不可破解 ⇒ 『极度安全』。默认态算法 aes128 ⇒ 2^128 ≈ 10^38.6，不出现 10^77.1。注：页面按所选算法估算密钥空间，纯算术无随机。"
  },
  {
    slug: "it/ssl-info",
    inputs: { calcSpeed: "1000000000000", calcAlgo: "aes128" },
    clicks: ["document.getElementById('__tbProbe').textContent='N99FT '+[formatTime(59.7),formatTime(86399),formatTime(31535999)].join('|');"],
    expect: ["N99FT 1 分钟|1 天|1 年"],
    ref: "IT-N99：临界秒数取整后不得跨档——59.7 秒须进为「1 分钟」（旧 Math.round 得「60 秒」）、86399 秒须进为「1 天」（旧「24 小时」）、31535999 秒须进为「1 年」（旧「12 个月」）。探针直接调 formatTime，默认态无该串。",
  },
  {
    slug: "it/ssl-info",
    inputs: { calcSpeed: "-100", calcAlgo: "aes128" },
    clicks: ["estimate();document.getElementById('__tbProbe').textContent='N100SPD '+document.getElementById('crackTime').textContent;"],
    expect: ["N100SPD 算力须为正数"],
    ref: "IT-N100：算力为负数时旧实现 parseFloat||1 放行、sec=avg/speed 得负时间并显示「< 1 秒」却判不安全；现明确提示「算力须为正数」并停止。默认算力 1e12 合法、不出现该提示。",
  },
  {
    "slug": "it/emoji-meaning",
    "inputs": { "searchInput": "火箭" },
    "clicks": ["renderCategories()"],
    "expect": ["共 1 个 Emoji"],
    "ref": "注入搜索『火箭』。内置 emoji 字典精确匹配 1 条 ⇒ 统计行『共 1 个 Emoji』。默认态 searchInput 为空 ⇒ 渲染全部 444 个 ⇒ 『共 444 个 Emoji』，不出现『共 1 个』。注：U+1F642 等码点属静态参考表，默认全量渲染，故改用计数串作判别点（已查字典确认『火箭』唯一匹配 1 条）。纯前端无随机。"
  },
  {
    "slug": "it/latex",
    "inputs": { "q": "\\frac{1}{2}" },
    "clicks": ["calcTool()"],
    "expect": ["共 1 条"],
    "ref": "注入 LaTeX 命令 \\frac{1}{2}。结果精确匹配 1 条（动能命令 \\frac{1}{2}mv^2）⇒ 统计行『共 1 条』。默认态 q 为空 ⇒ 渲染全部命令表（137 条）⇒ 『共 137 条』，不出现『共 1 条』。注：½mv² 等示例属静态参考表默认全量渲染，故改用计数串作判别点。纯前端无随机。"
  },
  {
    "slug": "it/latex",
    // IT-N305/N307：输入即筛选，且显示符号可反查命令。
    "clicks": ["var q=document.getElementById('q');q.value='alpha';q.fire('input');var a=document.getElementById('result').innerHTML;q.value='∑';q.fire('input');var s=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='SYM305 '+(a.indexOf('共 1 条')>=0&&a.indexOf('\\\\alpha')>=0?'OK':'BAD')+' SYM307 '+(s.indexOf('共 1 条')>=0&&s.indexOf('\\\\sum')>=0?'OK':'BAD');"],
    "inputs": { "q": "alpha" },
    "expect": ["SYM305 OK SYM307 OK"],
    "ref": "IT-N305/N307 注入 alpha 后只触发 input 事件即应筛到 1 条；再注入显示符号 ∑ 应按 e[1] 反查到 \\sum 且为 1 条。旧实现无 oninput 且不查符号字段，两态均红。"
  },
  {
    "slug": "it/latex",
    // IT-N306：复制必须先尝试 Clipboard API，失败分支给出明确提示。
    "clicks": ["var s=String(copyLatex);var ok=s.indexOf('navigator.clipboard')>=0&&s.indexOf('复制失败')>=0&&s.indexOf('execCommand')>=0;document.getElementById('__tbProbe').textContent='COPY306 '+(ok?'OK':'BAD');"],
    "inputs": { "q": "beta" },
    "expect": ["COPY306 OK"],
    "ref": "IT-N306 函数源码特征探针：优先 Clipboard API、保留 execCommand 兜底并判断布尔返回值、失败写「复制失败」提示。旧实现无条件 toast「已复制」且忽略返回值，不命中。行为路径由 JSDOM 真机脚本覆盖。"
  },
  {
    "slug": "it/usb-version",
    "inputs": { "v": "4.0", "v2": "3.0", "conn": "usba" },
    "expect": ["40 Gbps / 5 Gbps 最大速率", "USB 4.0 vs 3.0 版本对比", "最高 240W（PD 3.1）"],
    "ref": "注入非默认（三个 select 的 option 由 JS 填充，harness 取不到 ⇒ 页面回落到 ||'3.2' / ||'2.0' / ||'usbc'，默认态即 3.2 vs 2.0 = 20 Gbps / 480 Mbps）。⚠ 版本键是 '2.0'/'3.0'/'3.1'/'3.2'/'4.0'，不是 'usb4' 之类 —— 键不匹配时页面 info[v] 为 undefined 而静默回落到 3.2，输出与默认态完全一致 ⇒ 必须用页面源码里的键。注入 4.0 ⇒ 40 Gbps、供电『最高 240W（PD 3.1）』；v2=3.0 ⇒ 5 Gbps。默认态三串均不出现。"
  },
  {
    "slug": "it/json-to-xml",
    "inputs": { "root": "zzroot999" },
    "expect": ["✅ 转换成功\nzzroot999"],
    "ref": "派生映射：根元素名 zzroot999 被写进生成的 XML（默认 root）。⚠ 原 expect zzroot999 为根名输入回显（零判别力）；此处与「✅ 转换成功」拼成同一条串，要求该名字确实出现在转换产物区而不只是输入框。默认态为 转换成功+root，不命中 ⇒ 无逃生（已双态实测）。"
  },
  {
    "slug": "it/url-params",
    "inputs": { "urlInput": "https://example.com/zzpath?zz=7" },
    "expect": ["https://example.com/zzpath"],
    "ref": "注入非默认 URL。默认态 urlInput 为 example.com/search?q=toolbox… ⇒ 基 URL 行 'https://example.com/search'；注入后基 URL 行变 'https://example.com/zzpath'，默认态完全不含该串 ⇒ 0 逃生。注：删除参数功能(delParam)在桩下报错，但 URL 拆分与基 URL 解析为纯字符串，结果可靠。纯前端无随机。"
  },
  {
    "slug": "it/url-params",
    "inputs": { "urlInput": "https://example.com/zz?q=%" },
    "expect": ["https://example.com/zz"],
    "ref": "畸形百分号：`%` 单独出现时 decodeURIComponent 抛 URIError，旧实现整段中断、结果区停在默认示例（`…/search?q=toolbox…`）；修复后按标准把非法转义按字面 `%` 保留，基 URL `…/zz` 正常回写。默认示例不含 `/zz` ⇒ 判别有效。"
  },
  {
    "slug": "it/url-params",
    // IT-N466：「值解码显示：开/关」必须真正改变参数框显示值。
    "inputs": { "urlInput": "https://x.com/?q=%74oolbox&lang=%E6%89%8B" },
    "clicks": ["var u=document.getElementById('urlInput').value.split('?')[1]||'';var on=parseQueryPairs(u,true),off=parseQueryPairs(u,false);document.getElementById('__tbProbe').textContent='DECMODE '+(on[0].v==='toolbox'&&off[0].v==='%74oolbox'&&off[1].v==='%E6%89%8B'?'RAW':'DEC');"],
    "expect": ["DECMODE RAW"],
    "ref": "IT-N466：值解码显示开关必须真正改变解析结果。注入含百分号编码的 URL，探针从注入值取查询串并调用顶层 parseQueryPairs：开态应得 toolbox/手，关态应原样保留 %74oolbox/%E6%89%8B。旧实现 _decMode 从未被 calcTool 读取、也没有该解析函数 ⇒ 探针 ReferenceError 不出串 ⇒ DECMODE DEC/无串。harness stub DOM 不建模 <script type=text/template> 的 paramRowTpl，参数行根本未渲染，故不能直接读 paramsBox.innerHTML；完整集成态由 JSDOM 真机脚本覆盖。默认态不执行探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/url-params",
    // IT-N465：属性上下文必须转义引号，禁止裸引号进入 value="…" 模板。
    "clicks": ["var q=String.fromCharCode(34);var s=esc('a'+q+'b<c'+q+'>');document.getElementById('__tbProbe').textContent='ATTR '+(s.indexOf('&quot;')>=0&&s.indexOf('&lt;')>=0&&s.indexOf('&gt;')>=0&&s.indexOf(q)<0?'SAFE':'RAW');"],
    "expect": ["ATTR SAFE"],
    "ref": "IT-N465：esc() 先走 div.textContent→innerHTML（只转义 &<>），必须再补双引号/单引号实体，否则解析结果拼进 `<input value=\"{v}\">` 会破出属性执行脚本。探针用 String.fromCharCode(34) 构造引号，避开 clicks 里复杂引号转义；断言返回值同时含 &quot;/&lt;/&gt; 且不含裸引号。旧实现无这两次 replace ⇒ ATTR RAW。默认态不执行探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/url-params",
    // IT-N467：非法百分号必须按字面保留且不中断其余参数。
    "clicks": ["var r=parseQueryPairs('q=100%&ok=fine',true);document.getElementById('__tbProbe').textContent='URIERR '+(r.length===2&&r[0].v==='100%'&&r[1].v==='fine'?'SAFE':'BAD');"],
    "expect": ["URIERR SAFE"],
    "ref": "IT-N467：decodeURIComponent 无 try/catch 时，畸形 `%` 抛 URIError 会让整块解析停止（其余参数也不再刷新）。探针走顶层 parseQueryPairs(qs,true)，坏值须按字面保留为 100%，其后的 ok=fine 必须仍被解析出来。缺陷态抛错 ⇒ 探针不出串 ⇒ URIERR BAD/无串。默认态不执行探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/short-link-generator",
    // IT-N468：短码必须与 URL 有函数关系——同链稳定、异链不同。
    "clicks": ["var u=document.getElementById('url'),o=document.getElementById('output');document.getElementById('len').value='6';document.getElementById('count').value='2';u.value='https://stable.example.org/p?q=1';generate();var a=String(o.innerHTML);generate();var b=String(o.innerHTML);u.value='https://other.example.org/p?q=1';generate();var c=String(o.innerHTML);document.getElementById('__tbProbe').textContent='STABLE '+(a===b&&a!==c&&a.indexOf('stable.example.org')<0?'HASH':'RAND');"],
    "expect": ["STABLE HASH"],
    "ref": "IT-N468：旧实现每次用 crypto.getRandomValues 抽字符，同一 URL 连点两次得到两组不同短码，短码与 URL 无任何函数关系。修复后 URL 内容参与 FNV-1a 哈希，同链同设置必得同一短码。探针显式设 len/count 避免 harness 里 range 默认值为空，连续生成两次比较 innerHTML，再换一条 URL 必须不同；a 不含原始 URL 排除回显。默认态不执行探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/a1z26-cipher",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "sep": " ",
      "wordSep": "  "
    },
    "expect": [
      "1 2 3\nA B C"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"sep\":\" \",\"wordSep\":\"  \"}，输出区含「1 2 3\nA B C」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/affine-cipher",
    "inputs": {
      "a": "42",
      "b": "42",
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "X Y Z 密文 Q G W M C S I Y O E U K A Q G W M C S I Y O E U K A ✗ a=42 与 26 不互素，无法解密\n1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"b\":\"42\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「X Y Z 密文 Q G W M C S I Y O E U K A Q G W…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/adfgvx-cipher",
    "inputs": {
      "key": "abc123测试",
      "transKey": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      " U V X Y\nabc123测试\n1 2 3\nG A V A F D X X"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"transKey\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「 U V X Y\nabc123测试\n1 2 3\nG A V A F D X X」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\nInput: abc123测试 区号： 123 地区： 未知/非 NANP 区号 ❌ 未知区号"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\nInput: abc123测试 区号： 123 地区： 未知/…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "9995550100"
    },
    "expect": [
      "格式化： (999) 555-0100 ❌ N99 是保留未分配区号"
    ],
    "ref": "IT-N418：修复前 10 位一律「✅ 标准 10 位 NANP 号码」；现按 NANP 规则拒 N99 保留区号。expect 绑定「格式化 + 具体错误」整段，默认态 021 不含格式化行 ⇒ 不逃生。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "0005550100"
    },
    "expect": [
      "格式化： (000) 555-0100 ❌ 区号 NPA 首位须为 2–9"
    ],
    "ref": "IT-N418：NPA 首位须 2–9。默认态 021 也含「区号 NPA 首位须为 2–9」但不含格式化行，故把 expect 扩到格式化串以避开默认态命中。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "1115550100"
    },
    "expect": [
      "格式化： (111) 555-0100 ❌ 区号 NPA 首位须为 2–9"
    ],
    "ref": "IT-N418：111 首位非法且属 N11，同样被拒。同上用格式化串绑定输入派生值。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "2125550100"
    },
    "expect": [
      "格式化： (212) 555-0100 ✅ 标准 10 位 NANP 号码"
    ],
    "ref": "回归护栏（修复前后同绿）：合法 212 号码在加入结构校验后仍须正常格式化并判标准有效，防止校验收紧误伤正常路径。默认态 021 为 3 位无格式化行 ⇒ 判别器仍判正确变红。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "+1 212-555-0100"
    },
    "expect": [
      "国家码： +1 （已剥离，按 10 位 NANP 号码解析） 区号： 212 地区： New York (Manhattan)"
    ],
    "ref": "IT-N419：修复前 digits=12125550100（11 位）⇒ 区号 121 + 「⚠️ 通常为 10 位」；现剥前导国家码 1 得 212 → New York。expect 绑定剥码提示与解析结果，默认态不命中。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "1 212 555 0100"
    },
    "expect": [
      "国家码： +1 （已剥离，按 10 位 NANP 号码解析） 区号： 212 地区： New York (Manhattan)"
    ],
    "ref": "IT-N419：不带 + 的 11 位国际写法同样剥离（判据是「11 位且首位 1」，NANP 本地号首位必为 2–9，不会误剥）。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "456"
    },
    "expect": [
      "❌ 未知区号（456 是保留 / 非地理区号，未分配为地理区号）"
    ],
    "ref": "IT-N420：表内 456 标 Reserved，修复前 3 位分支只查存在性 ⇒ 「✅ 区号有效」；现按 NPA_RESERVED + Reserved 值双重规则拒绝。默认态是 021 的结构错误说明，不含 456 ⇒ 强判别。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "911"
    },
    "expect": [
      "❌ 未知区号（N11 是保留服务码，不能作区号）"
    ],
    "ref": "IT-N418/N420：N11 服务码不可作区号。修复前只给「❌ 未知区号」无理由，本 expect 要求明确 N11 理由。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "202"
    },
    "expect": [
      "地区： Washington, DC ✅ 区号有效"
    ],
    "ref": "回归护栏（修复前后同绿）：已收录的合法地理区号 202 在收紧校验后仍判有效；默认态 021 不命中。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "3455550100"
    },
    "expect": [
      "⚠️ NANP 结构合法，但区号 345 未收录或为保留码，不判为标准有效号码"
    ],
    "ref": "IT-N418：区号不在表中但 NPA/NXX 结构合法时，只给「结构合法、归属地未收录」的谨慎结论，绝不输出「✅ 标准」。修复前无条件判标准有效 ⇒ 本串不存在。"
  },
  {
    "slug": "it/area-code-lookup",
    "inputs": {
      "input": "800"
    },
    "expect": [
      "❌ 未知区号（800 是保留 / 非地理区号，未分配为地理区号）"
    ],
    "ref": "IT-N420 扩展：800 免费电话属非地理 NPA，不是地理区号；与 FAQ「800/888 为非地理区号」口径对齐。"
  },
  {
    "slug": "it/ascii-art",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      " Slim 紧凑\nabc123测试\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「 Slim 紧凑\nabc123测试\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/api-sign-generator",
    "inputs": {
      "secret": "abc123测试",
      "params": "1\n2\n3",
      "algo": "sha256"
    },
    "expect": [
      "sha256\nabc123测试\n1 2 3\n待签名串： &secret=abc123测试 签名结果： b652f9dbc2b4dd477559b3f0635242da8094a23d1c5b3eb9b8993ddae28f18c5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"secret\":\"abc123测试\",\"params\":\"1\\n2\\n3\",\"algo\":\"sha256\"}，输出区含「abc123测试\n1 2 3\nsha256\n待签名串： &secret=abc1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ascii-table",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "abc123测试\nNo matching entries."
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「abc123测试\nNo matching entries.」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ascii-tree-generator",
    "inputs": {
      "paths": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n✅ 已生成 3 行目录树（3 个路径）\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"paths\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n✅ 已生成 3 行目录树（3 个路径）\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/bacon-cipher",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "01"
    },
    "expect": [
      "ab 11001\n1 2 3\n01"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"01\"}，输出区含「ab 11001\n1 2 3\n01」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ast-viewer",
    "inputs": {},
    "clicks": ["window.acorn={parse:function(){return {type:'Program',start:0,end:0,body:[{type:'ToolBoxProbeNode',start:0,end:0}]}}};document.getElementById('btnParse').fire('click')"],
    "expect": [
      "ToolBoxProbeNode"
    ],
    "ref": "renderJson 旧实现把守卫写成 `const __h4=esc(...).replace(cb)`，并在回调里读取 __h4 ⇒ TDZ 抛 `Cannot access '__h4' before initialization`，整个解析结果被 catch 替换成「解析失败」，AST 树与 JSON 全部丢失。修复后注入独立解析桩（window.acorn.parse 返回含唯一节点 ToolBoxProbeNode 的 AST），该串出现在结果区。默认态（无 acorn 外链）走「未能加载解析器」提示，不含该串。"
  },
  {
    "slug": "it/atbash-cipher",
    "inputs": {
      "input": "abc"
    },
    "expect": [
      "zyx"
    ],
    "ref": "Atbash 自校验：a↔z、b↔y、c↔x ⇒ 加密 'abc' 得 'zyx'。原用例注入 '1\\n2\\n3' 且把只读输出框 output 也一并注入，期望串恰等于「输入回显 + 注入的 output 值」（'1 2 3\\n1 2 3'），属逃生形态；改注入纯字母后锚点由输入派生。2026-11-05 同批修正：真实 localStorage 桩下 saveHistory 会写历史并重渲染，原 expect 里的「暂无历史记录」不再出现（旧空桩把 setItem 吞掉才侥幸保留）。默认态输入为空 ⇒ 不命中。"
  },
  {
    "slug": "it/barcode-codabar",
    "inputs": {
      "data": "abc123测试"
    },
    "expect": [
      "第 7 位含非法字符「测」（仅支持 0-9 - $ : / . + 与起止符 A/B/C/D）"
    ],
    "ref": "自动补强（B类零用例）·2026-11-06 随 IT-N492 同步更新：注入非默认输入{\"data\":\"abc123测试\"}，原实现静默丢弃表外字符并回显原文（旧杆「abc123测试\\nABC123测试」= 输入回显，零判别力）；现 buildCodabar 逐位校验并报「第 7 位含非法字符「测」」，位置与字符均由输入决定。默认 data=A12345B 合法，不命中。"
  },
  {
    "slug": "it/barcode-code128",
    "inputs": {
      "data": "abc123测试"
    },
    "expect": [
      "完成，请稍后重试。\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"abc123测试\"}，输出区含「完成，请稍后重试。\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/barcode-code39",
    "inputs": {
      "data": "abc123测试"
    },
    "expect": [
      "⚠ 不支持字符「测」，Code 39 仅支持 A–Z、0–9、空格与 - . $ / + %。"
    ],
    "ref": "标准 Code 39 重写后校验字符集：注入 data=abc123测试（含汉字「测」）⇒ 输出不支持字符提示。默认样例仅含合法字符，不出现该提示 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/barcode-ean",
    "inputs": {
      "data": "12345"
    },
    "expect": [
      "Too short: EAN-13 needs 12 or 13 digits"
    ],
    "ref": "位数校验：5 位输入不再补零，输出位数不足错误（英文态为 Too short）；默认样例 590123412345 合法，不出现该提示 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/barcode-msi",
    "inputs": {
      "data": "abc测试"
    },
    "expect": [
      "⚠ 输入含非数字字符：MSI 仅支持 0–9，请删除后重试，本工具不会静默丢弃字符。"
    ],
    "ref": "IT-N511 同批更新：注入 data=abc测试（非数字）⇒ buildMSI 返回 error='nondigit'，输出「输入含非数字字符…不会静默丢弃字符」。旧版先 replace(/\\D/g,'') 剥离为空再报「请输入至少一位数字」，本批改为「有非数字就直接报错、不静默剥离」，故断言同步改写。默认样例为纯数字，不命中。"
  },
  {
    "slug": "it/barcode-msi",
    "inputs": {
      "data": "12A3"
    },
    "expect": [
      "⚠ 输入含非数字字符：MSI 仅支持 0–9，请删除后重试，本工具不会静默丢弃字符。"
    ],
    "ref": "IT-N511 回归：混合输入 12A3 必须被拒绝。修复前 replace(/\\D/g,'') 静默剥离 A ⇒ 条码编码 123、页面文字显示 12A3（显示与编码不一致）且零提示；修复后统一报非数字错误。默认样例为纯数字不命中，注入的 A 是触发该分支的关键。"
  },
  {
    "slug": "it/barcode-msi",
    "inputs": {
      "data": "7228588281088160612916291613220210957569",
      "checkMode": "mod10"
    },
    "clicks": ["generate()"],
    "expect": [
      "72285882810881606129162916132202109575694"
    ],
    "ref": "IT-N510 复核失败重做：40 位长串 Mod 10 校验位，旧实现把加倍位拼成大整数再 ×2 超 2^53 精度 ⇒ 校验位算成 7；逐位加倍后 >9 减 9 得正确校验位 4（数据流 data+校验位 = 7228…5694）。默认样例 1234567 不出现该 40 位串 ⇒ 强判别、零逃生。回退 N510 源码会令此用例转红。"
  },
  {
    "slug": "it/barcode-itf",
    "inputs": {
      "data": "abc123测试"
    },
    "expect": [
      "abc123测试\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"abc123测试\"}，输出区含「abc123测试\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/barcode-upc",
    "inputs": {
      "data": "abc123测试"
    },
    "expect": [
      "⚠ 输入含非数字字符，请只填写数字"
    ],
    "ref": "UPC-A 重写后严格校验字符集：注入 data=abc123测试（含汉字）⇒ 输出「⚠ 输入含非数字字符，请只填写数字」。默认样例为 12 位数字，不出现该提示 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/base32-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\nGEFDECRT"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\nGEFDECRT」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/base58-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "variant": "ripple"
    },
    "expect": [
      "1 2 3\naXuwMCY\nripple"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"variant\":\"ripple\"}，输出区含「1 2 3\naXuwMCY\nripple」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  // 已移除：it/base64-converter 的「自动补强（B类零用例）」用例（原 3813-3825 行）。
  // 原因：其输入目标为 textarea#input，harness 对 textarea 的注入会被页面 init 默认样例
  // 「Hello, World! 你好，世界！」覆盖（harness 已知缺口）⇒ 注入恒失效、期望值实为默认态
  // 输出（got = SGVsbG8sIFdvcmxkIQ== / Hello, World!），零判别力且恒失败。
  // base64-converter 已有 7 个手写用例完整覆盖（Base64/Base32/Base85/URL-safe/解码方向/
  // 多字节 UTF-8/非法输入），故移除该无效补强，不留无判别力用例。
  {
    "slug": "it/base64-file",
    "inputs": {
      "b64Out": "1\n2\n3",
      "b64In": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n�m\n✅ 已解码为文本（2 B）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"b64Out\":\"1\\n2\\n3\",\"b64In\":\"1\\n2\\n3\"}，输出区含「1 2 3\n�m\n✅ 已解码为文本（2 B）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/base64-file",
    "clicks": ["document.getElementById('result').innerHTML='EXT '+['text/plain','image/svg+xml','image/jpeg','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/octet-stream','application/x-foo'].map(extFromMime).join('|');"],
    "expect": ["EXT txt|svg|jpg|docx|bin|foo"],
    "ref": "IT-N406：MIME → 标准扩展名的映射表必须存在且生效。六个取样分别覆盖「子类型≠扩展名」(text/plain→txt)、结构化语法后缀 (svg+xml→svg)、别名 (jpeg→jpg)、Office 长类型 (vnd.openxmlformats...→docx)、通用二进制 (octet-stream→bin)、未知类型清洗 (x-foo→foo)。修复前无 extFromMime 函数 ⇒ clicks 抛错、结果区恒空 ⇒ 必红。"
  },
  {
    "slug": "it/base64-file",
    "inputs": {"b64In": "data:text/plain;base64,SGVsbG8="},
    "clicks": ["document.body=document.body||{appendChild:function(){},removeChild:function(){}};b64ToFile();"],
    "expect": ["text/plain → decoded.txt"],
    "ref": "IT-N406：走真实还原下载路径，结果区必须回显实际文件名。修复前文件名取 mime.split('/')[1] ⇒ decoded.plain，且结果区不含文件名 ⇒ 双变红。document.body 桩只为让 harness 跑完下载分支（浏览器里 body 恒存在）。"
  },
  {
    "slug": "it/base64-file",
    "inputs": {"b64In": "data:image/svg+xml;base64,PHN2Zy8+"},
    "clicks": ["document.body=document.body||{appendChild:function(){},removeChild:function(){}};b64ToFile();"],
    "expect": ["image/svg+xml → decoded.svg"],
    "ref": "IT-N406：image/svg+xml 修复前会生成 decoded.svg+xml（扩展名里带 +，文件名非法且打不开）。输入是含 +xml 的 data URI，默认态不含 ⇒ 判别明确。"
  },
  {
    "slug": "it/base64-file",
    "inputs": {"b64In": "data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,UEs="},
    "clicks": ["document.body=document.body||{appendChild:function(){},removeChild:function(){}};b64ToFile();"],
    "expect": ["wordprocessingml.document → decoded.docx"],
    "ref": "IT-N406：OOXML 长 MIME 必须映射成 docx；修复前取子类型末段会得到 decoded.document。同时验证结果区回显的是原始 MIME + 实际文件名。"
  },
  {
    "slug": "it/base64-file",
    "inputs": {"b64In": "SGVsbG8="},
    "clicks": ["document.body=document.body||{appendChild:function(){},removeChild:function(){}};b64ToFile();"],
    "expect": ["application/octet-stream → decoded.bin"],
    "ref": "IT-N406：无 data URI 前缀时回落通用二进制流，文件名应为 decoded.bin；修复前是 decoded.octet-stream。注入纯 Base64（非默认空输入）⇒ 默认态不触发该分支。"
  },
  {
    "slug": "it/base64-file",
    "inputs": {"b64Out": "data:image/jpeg;base64,/9j/"},
    "clicks": ["document.body=document.body||{appendChild:function(){},removeChild:function(){}};var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='a'){e.click=function(){document.getElementById('result').innerHTML='DL:'+e.download;};}return e;};downloadB64();"],
    "expect": ["DL:file.jpg"],
    "ref": "IT-N406：第二个调用点（b64Out 的「还原为文件」）也必须走映射，文件名应是 file.jpg 而非 file.jpeg。用 createElement 桩在 a.click() 时捕获 a.download 写进结果区 ⇒ 真下载文件名契约。修复前 extFromMime 不存在 ⇒ 该分支抛错、结果区无 DL: 串。"
  },
  {
    "slug": "it/base85-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "variant": "z85"
    },
    "expect": [
      "1 2 3\n1 2 3\nz85"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"variant\":\"z85\"}，输出区含「1 2 3\n1 2 3\nz85」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/basic-auth-generator",
    "inputs": {
      "f_user": "abc123测试",
      "f_pass": "abc123测试",
      "headerOut": "abc123测试",
      "urlOut": "abc123测试",
      "tokenOut": "abc123测试"
    },
    "expect": [
      "abc123测试\nabc123测试\n✅ 已生成 Basic 认证信息（令牌 36 字符） 含非 ASCII 字符时凭据按 UTF-8 编码，服务端须按 UTF-8 解码（RFC 7617 charset 参数）。\nAuthorization: Basic YWJjMTIz5rWL6K+VOmFiYzEyM+a1i+ivlQ==\nhttps://abc123%E6"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f_user\":\"abc123测试\",\"f_pass\":\"abc123测试\",\"headerOut\":\"abc123测试\",\"urlOut\":\"abc123测试\",\"tokenOut\":\"abc123测试\"}，输出区含成功行 + IT-N209 charset 提示 + Authorization/URL；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。第226批 N209 新增 charset 提示后同批同步本 expect。"
  },
  {
    "slug": "it/bcrypt",
    "inputs": {
      "plain": "abc123测试",
      "hashOut": "1\n2\n3",
      "rounds": "10"
    },
    "expect": [
      "abc123测试\n10\n哈希格式无效：bcrypt is not defined\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plain\":\"abc123测试\",\"hashOut\":\"1\\n2\\n3\",\"rounds\":\"10\"}，输出区含「abc123测试\n1 2 3\n10\n哈希格式无效：bcrypt is not d…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/baudot-code",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "format": "decimal"
    },
    "expect": [
      "TRS LTRS\n1 2 3\ndecimal\nE A"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"format\":\"decimal\"}，输出区含「TRS LTRS\n1 2 3\ndecimal\nE A」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/bayes-theorem",
    "inputs": {
      "prior": "42",
      "likelihood": "42",
      "falsePositive": "42"
    },
    "expect": [
      "42\n42\n42\n所有概率必须在 0~1 之间",
      "所有概率必须在 0~1 之间\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"prior\":\"42\",\"likelihood\":\"42\",\"falsePositive\":\"42\"}，输出区含「42\n42\n42\n所有概率必须在 0~1 之间」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/binary-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "sep": " "
    },
    "expect": [
      "1 2 3\n00110001 00001010 00110010 00001010 00110011"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"sep\":\" \"}，输出区含「1 2 3\n00110001 00001010 00110010 0000101…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/bitwise-calculator",
    "inputs": {
      "a": "abc123测试",
      "b": "abc123测试",
      "op": "OR"
    },
    "expect": [
      "abc123测试\nOR\nabc123测试",
      "OR\nabc123测试\nabc123测试\n请输入有效的数值（支持 255 / 0xff / 0b1111）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"abc123测试\",\"b\":\"abc123测试\",\"op\":\"OR\"}，输出区含「abc123测试\nOR\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", b: "10", op: "AND" },
    clicks: ["calc()"],
    expect: ["A 00000000 | 00000000 | 00000000 | 00001100 B 00000000 | 00000000 | 00000000 | 00001010 R", "与 A 不同：1 位"],
    ref: "S3 位对齐可视化：A/B/R 三行 8 位分组（12=…00001100、10=…00001010）+ 与 A 差异统计（1100→1000 仅第 2 位清零 ⇒ 1 位）。默认 a=0 ⇒ A 行全 0 且「与 A 不同：0 位」，双锚均不命中。"
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", b: "0", op: "NOT" },
    clicks: ["calc()"],
    expect: ["按位取反：1→0 共 2 位，0→1 共 30 位"],
    ref: "S3 位对齐可视化·NOT：12=0b1100（2 个 1、30 个 0）逐位取反 ⇒ 1→0 共 2 位、0→1 共 30 位。曾出 bug：用「总差异数 32−flips」推导方向计数恒得 0/32，已改为逐位方向计数。默认 a=0 ⇒ 1→0 共 0 位，不命中。"
  },
  {
    "slug": "it/binary-to-text",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/binomial-distribution",
    "inputs": {
      "n": "42",
      "p": "42",
      "k": "42"
    },
    "expect": [
      "42\n42\n42\np 必须在 0~1 之间",
      "p 必须在 0~1 之间\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"p\":\"42\",\"k\":\"42\"}，输出区含「42\n42\n42\np 必须在 0~1 之间」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/box-shadow-generator",
    "inputs": {
      "x": "42",
      "y": "42",
      "blur": "42",
      "spread": "42",
      "color": "abc123测试",
      "alpha": "42"
    },
    "expect": [
      "-shadow: 42px 42px 42px 42px rgba(171,193,35,0.42);\n偏移 42px 42px · 模糊 42px · 扩散 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"y\":\"42\",\"blur\":\"42\",\"spread\":\"42\",\"color\":\"abc123测试\",\"alpha\":\"42\"}，输出区含「-shadow: 42px 42px 42px 42px rgba(171,19…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/c-string-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "qtype": "single"
    },
    "expect": [
      "1 2 3\n1 2 3\nsingle",
      "1 2 3\nsingle\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"qtype\":\"single\"}，输出区含「1 2 3\n1 2 3\nsingle」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/caa-record-generator",
    "inputs": {
      "domain": "abc123测试",
      "iodefEmail": "abc123测试",
      "output": "1\n2\n3",
      "flag": "128"
    },
    "expect": [
      "abc123测试\n128\n请至少选择一个 CA\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"domain\":\"abc123测试\",\"iodefEmail\":\"abc123测试\",\"output\":\"1\\n2\\n3\",\"flag\":\"128\"}，输出区含「abc123测试\n128\n请至少选择一个 CA\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/caesar-cipher",
    "inputs": {
      "input": "xyz"
    },
    "expect": [
      "{|}"
    ],
    "ref": "关闭「仅字母移位」时作用于可打印 ASCII 共 95 个字符：xyz 位移 +3 ⇒ x→{、y→|、z→}。修复前模数固定 26，会错误地回绕成字母；默认输入不是 xyz，注入失败即不命中。"
  },
  {
    slug: "it/calc-3",
    inputs: { hexInput: "#00FF7F" },
    clicks: ["fromHex();document.getElementById('__tbProbe').textContent=String(document.getElementById('result').textContent).replace(/\\s+/g,' ').trim();"],
    expect: ["HEX： #00FF7F RGB： rgb(0, 255, 127) HSL： hsl(150, 100%, 50%)"],
    ref: "G06 元素顺序变更后的过期断言修正：旧断言锚「3%, 39%)\\n#5b1bac\\nabc123测试」，其中 #5b1bac 是页面默认色值、且三元素连续串依赖创建序 ⇒ 首屏自跑改变元素顺序后即失配（门禁 it calc correctness 红）。改为注入合法非默认色 #00FF7F 并显式 fromHex()，探针取结果区归一文本，锚完整派生串「HEX： … RGB： … HSL： …」；默认 #5B1BAC 不含该串 ⇒ 强判别、零逃生。",
  },
  {
    "slug": "it/calc-10",
    "inputs": {
      "textInput": "1\n2\n3"
    },
    "expect": [
      "SHA-256 ad53e8806d17c82d38902738d1d47d96bddaade27513466322efa0f793149dd0 SHA-512 c343b77400fa58c2ee2a5b295a413aaadc88c6c"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"textInput\":\"1\\n2\\n3\"}，输出区含「SHA-256 ad53e8806d17c82d38902738d1d47d96…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/calc-2",
    "inputs": {
      "numInput": "abc123测试",
      "fromBase": "8"
    },
    "expect": [
      "abc123测试\n8\n请输入有效的 8 进制数值。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"numInput\":\"abc123测试\",\"fromBase\":\"8\"}，输出区含「abc123测试\n8\n请输入有效的 8 进制数值。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/calc-4",
    "inputs": {
      "baseSize": "42",
      "pxInput": "42"
    },
    "expect": [
      "nt-size: 2.625rem; pt 31.5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseSize\":\"42\",\"pxInput\":\"42\"}，输出区含「nt-size: 2.625rem; pt 31.5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/calc-1",
    "inputs": {
      "sizeInput": "42",
      "unitSelect": "KB"
    },
    "expect": [
      "42\nKB\n原始大小： 42 KB （千字节） 等价于 42,000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sizeInput\":\"42\",\"unitSelect\":\"KB\"}，输出区含「42\nKB\n原始大小： 42 KB （千字节） 等价于 42,000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/calc-7",
    "inputs": {
      "pathInput": "abc123测试",
      "jsonInput": "1\n2\n3",
      "formatSelect": "raw"
    },
    "expect": [
      "box.name 结果： ToolBox"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pathInput\":\"abc123测试\",\"jsonInput\":\"1\\n2\\n3\",\"formatSelect\":\"raw\"}，输出区含「box.name 结果： ToolBox」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/case-converter",
    "inputs": {
      "inputText": "1\n2\n3"
    },
    "expect": [
      "#128196; 3 行\n1 2 3\n1 2 3\n1 2 3\n1 2 3\n123\n123\n1_2_3\n1-2-3\n1_2_3\n1.2.3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputText\":\"1\\n2\\n3\"}，输出区含「#128196; 3 行\n1 2 3\n1 2 3\n1 2 3\n1 2 3\n123…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    // 2026-11-05 随机源改 crypto.getRandomValues 后，原「固定码 gGANM/77mCE」锚点
    // 依赖 harness 的种子 Math.random，必然失效。随机内容不可断言，改为「条数 × 长度 ×
    // 字符集」的结构断言：批量 8 条、每条 5 位 [0-9A-Za-z]，且 grid 恰好由 8 个
    // 「码 + 复制导出」片段拼成。默认 batchCount=6 且不自动批量 ⇒ 不命中。
    "slug": "it/captcha-generator",
    "inputs": {
      "batchCount": "8"
    },
    "clicks": [
      'batchGenerate();(function(){var g=document.getElementById("batchGrid").innerHTML;var ok=/^([0-9A-Za-z]{5}复制导出){8}$/.test(g);document.getElementById("verifyInput").value=ok?"CAPTCHA-BATCH-8x5-ALNUM-OK":"CAPTCHA-BATCH-FAIL:"+g.length;})()'
    ],
    "expect": [
      "CAPTCHA-BATCH-8x5-ALNUM-OK"
    ],
    "ref": "批量 8 条：batchGenerate 为每条渲染 canvas（空）+ 答案 5 位字母数字 + 复制/导出按钮；桩内 appendChild 把子串拼进父 innerHTML，故 #batchGrid.innerHTML 恰为 8 组「5 位 [0-9A-Za-z] + 复制导出」的重复。断言验证条数、长度、字符集三项，随机内容本身不断言。默认 6 条且需点击批量 ⇒ 默认态为空。"
  },
  {
    // 数字模式同口径复核：字符集收窄为 [0-9]，长度仍 5，条数 3。
    "slug": "it/captcha-generator",
    "inputs": {
      "batchCount": "3"
    },
    "clicks": [
      'setType("num");batchGenerate();(function(){var g=document.getElementById("batchGrid").innerHTML;var ok=/^([0-9]{5}复制导出){3}$/.test(g);document.getElementById("verifyInput").value=ok?"CAPTCHA-BATCH-3x5-DIGIT-OK":"CAPTCHA-BATCH-FAIL:"+g.length;})()'
    ],
    "expect": [
      "CAPTCHA-BATCH-3x5-DIGIT-OK"
    ],
    "ref": "setType('num') 把字符集切到 0-9，batch 3 条、长度仍 5 ⇒ #batchGrid.innerHTML 恰为 3 组「5 位数字 + 复制导出」。验证数字模式字符集不含字母，同时避免「批量条数固定为 8」的单点依赖。"
  },
  {
    "slug": "it/char-encoder",
    "inputs": {
      "input": "1\n2\n3"
    },
    "expect": [
      " Binary 00110001 00001010 00110010 00001010 001100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\"}，输出区含「 Binary 00110001 00001010 00110010 00001…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/char-encoder",
    "inputs": { "input": "Hi中" },
    "expect": [
      "U+4E2D e4 b8 ad 11100100 10111000 10101101"
    ],
    "ref": "E1 字节视图（2026-10-26）：#byteViewBox 逐字符对照表，「中」= U+4E2D → UTF-8 三字节 e4 b8 ad（11100100 10111000 10101101）。默认态 input 为空 ⇒ byteView 清空不渲染，零交集。"
  },
  {
    "slug": "it/calc-subnet",
    "inputs": {
      "ip": "abc123测试",
      "cidr": "abc123测试",
      "subN": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\nIP 地址格式无效，请输入合法 IPv4（如"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ip\":\"abc123测试\",\"cidr\":\"abc123测试\",\"subN\":\"42\"}，输出区含「abc123测试\nabc123测试\nIP 地址格式无效，请输入合法 IPv4（如」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/charset-detector",
    "inputs": {
      "txt": "1\n2\n3"
    },
    "expect": [
      "未检测到明显乱码特征。 修复输出： 1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"txt\":\"1\\n2\\n3\"}，输出区含「未检测到明显乱码特征。 修复输出： 1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。// 2026-11-04：harness 保真度修复后 textarea 默认文本会同时进 .textContent，快照字符串顺序改变，故去掉跨元素的换行拼接断言，只锚输出域自身内容（仍含注入值 1 2 3）。"
  },
  {
    // 2026-11-11 第199批：原自动补强例锚具体随机名字串（含旧双字词条缺陷产物「利建华」），
    // 修复 N249（拆双字词条 + 复姓避让 + 逐字拼接）后 PRNG 调用序列改变、名字全变 ⇒ 必然失效。
    // 随机内容不可断言，改为结构断言：注入 count=5 / 2字名，结果恰好 5 条且每条姓名恰 2 字。
    "slug": "it/chinese-name-generator",
    "inputs": {
      "optCount": "5",
      "optGender": "male",
      "optLength": "2",
      "optStyle": "modern"
    },
    "clicks": [
      '(function(){generate();var ok=generatedNames.length===5;for(var i=0;i<generatedNames.length;i++){if(String(generatedNames[i].name).length!==2)ok=false;}document.getElementById("__tbProbe").innerHTML="CNSTRUCT "+(ok?"OK":"BAD:"+generatedNames.length);})()'
    ],
    "expect": [
      "CNSTRUCT OK"
    ],
    "ref": "自动补强改造·结构断言：注入 count=5/2字名，调 generate() 后读顶层 generatedNames，断言恰 5 条且每条姓名恰 2 字；不锚随机姓名内容，避免 PRNG 序列变动导致脆断。harness stub DOM 不渲染本页 resultArea 且 getAnalysis 有噪声，故走 JS 变量探针而非 DOM。默认态 count 非 5 ⇒ 探针只在 clicks 执行、零逃生。"
  },
  {
    // IT-N249：2 字名/3 字名必须精确等于目标字数（拆双字词条 + 复姓避让 + 逐字拼接 + 兜底）
    "slug": "it/chinese-name-generator",
    "clicks": [
      '(function(){var bad=0;for(var L=2;L<=3;L++)for(var i=0;i<60;i++){var it=generateOneName("male",String(L),"modern");if(String(it.name).length!==L)bad++;}document.getElementById("__tbProbe").innerHTML="CNLEN "+(bad===0?"OK":"BAD"+bad);})()'
    ],
    "expect": [
      "CNLEN OK"
    ],
    "ref": "IT-N249 字数精确：反复调 generateOneName(male,2/3,modern) 120 次，断言 name.length===目标字数。旧实现 maleChars 含「建国/志强/建华」双字词条，2 字名抽到即得 3 字；复姓用于 2 字名亦超长 ⇒ CNLEN BAD>0 红。诊断串只在 clicks 写入，默认态无 ⇒ 零逃生。"
  },
  {
    // IT-N250：getCharPool 出口去重，薇/素/毅 不再被放大取样
    "slug": "it/chinese-name-generator",
    "clicks": [
      '(function(){var bad=[];var combos=[["male","modern"],["female","modern"],["random","classic"]];for(var c=0;c<combos.length;c++){var p=getCharPool(combos[c][0],combos[c][1]);var s={};for(var i=0;i<p.length;i++)s[p[i]]=(s[p[i]]||0)+1;for(var k in s)if(s[k]>1){bad.push(k);break;}}document.getElementById("__tbProbe").innerHTML="CNUNIQ "+(bad.length===0?"OK":"BAD"+bad.join(","));})()'
    ],
    "expect": [
      "CNUNIQ OK"
    ],
    "ref": "IT-N250 字池去重：检查 male/female/random 三池出口无重复字（Set 去重）。旧实现 femaleChars 薇×3/素×3 等 17 组、maleChars 毅×3 ⇒ CNUNIQ BAD 红。诊断串只在 clicks 写入 ⇒ 零逃生。"
  },
  {
    // IT-N251：取消收藏 toast 有明确文案而非空/undefined
    "slug": "it/chinese-name-generator",
    "clicks": [
      '(function(){var got="";var old=ToolBox.showToast;ToolBox.showToast=function(m){got=String(m);};favorites=[{name:"__CNFAV__",gender:"male",style:"modern",time:1}];try{toggleFav("__CNFAV__","male","modern");}catch(e){}ToolBox.showToast=old;document.getElementById("__tbProbe").innerHTML="CNFAV "+(got&&got!=="undefined"&&got.indexOf("undefined")<0?"OK":"BAD:"+got);})()'
    ],
    "expect": [
      "CNFAV OK"
    ],
    "ref": "IT-N251 收藏 toast：stub showToast 捕获后调 toggleFav 取消收藏，断言 toast 文案非空且不含 undefined。旧实现 i18nText() 空参 ⇒ showToast 收到空串 ⇒ 空提示 ⇒ CNFAV BAD 红。诊断串只在 clicks 写入，默认态无 ⇒ 零逃生。"
  },
  {
    "slug": "it/clamp-calculator",
    "inputs": {
      "min": "42",
      "pref": "42",
      "max": "42",
      "vwMin": "42",
      "vwMax": "42",
      "slider": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n最小视口必须小于最大视口\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"min\":\"42\",\"pref\":\"42\",\"max\":\"42\",\"vwMin\":\"42\",\"vwMax\":\"42\",\"slider\":\"42\"}，输出区含「42\n42\n42\n42\n42\n最小视口必须小于最大视口\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/code-line-counter",
    "inputs": {
      "codeInput": "1\n2\n3",
      "langSel": "js"
    },
    "expect": [
      "1 2 3\njs\n3 总行数 3 代码行 0 注释行 0 空行 100.0% 代码占比"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"codeInput\":\"1\\n2\\n3\",\"langSel\":\"js\"}，输出区含「1 2 3\njs\n3 总行数 3 代码行 0 注释行 0 空行 100.0% 代…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/code-highlighter",
    "inputs": {
      "codeInput": "1\n2\n3",
      "langSelect": "html",
      "editorTheme": "dark"
    },
    "expect": [
      "<!DOCTYPE html> <html lang=\"zh-CN\"> <head> <meta charset=\"UTF-8\"> <meta name=\"viewport\" content=\"width=device-width, ini"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"codeInput\":\"1\\n2\\n3\",\"langSelect\":\"html\",\"editorTheme\":\"dark\"}，输出区含「<!DOCTYPE html> <html lang=\"zh-CN\"> <hea…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/color-converter",
    "inputs": {
      "colorPicker": "abc123测试",
      "colorInput": "abc123测试",
      "palettePicker": "abc123测试",
      "fgColor": "abc123测试",
      "fgInput": "abc123测试",
      "bgColor": "abc123测试",
      "bgInput": "abc123测试"
    },
    "expect": [
      "pha 1 复制\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"colorPicker\":\"abc123测试\",\"colorInput\":\"abc123测试\",\"palettePicker\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"fgInput\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgInput\":\"abc123测试\"}，输出区含「pha 1 复制\nabc123测试\nabc123测试\nabc123测试\nabc1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/code-runner",
    "inputs": {
      "codeHtml": "1\n2\n3",
      "codeCss": "1\n2\n3",
      "codeJs": "1\n2\n3",
      "sampleSelect": "animation"
    },
    "expect": [
      "kground: #fff; animation: bounce 1.4s ease-in-out infinite; } @keyframes bounce { 0%, 100% { transform: translateY(0) sc"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"codeHtml\":\"1\\n2\\n3\",\"codeCss\":\"1\\n2\\n3\",\"codeJs\":\"1\\n2\\n3\",\"sampleSelect\":\"animation\"}，输出区含「kground: #fff; animation: bounce 1.4s ea…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/convert-11",
    "inputs": {
      "val": "abc123测试",
      "from": "bin",
      "to": "bin"
    },
    "expect": [
      "abc123测试\nbin\nbin\n二进制串应为32位0/1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"abc123测试\",\"from\":\"bin\",\"to\":\"bin\"}，输出区含「abc123测试\nbin\nbin\n二进制串应为32位0/1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/confidence-interval",
    "inputs": {
      "mean": "42",
      "std": "42",
      "n": "42",
      "conf": "0.90",
      "dist": "z"
    },
    "expect": [
      "差 ME = 1.645 × 6.4807 = 10.6608 置信区间 = [42 - 10.6608, 42 + 10.6608]"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mean\":\"42\",\"std\":\"42\",\"n\":\"42\",\"conf\":\"0.90\",\"dist\":\"z\"}，输出区含「差 ME = 1.645 × 6.4807 = 10.6608 置信区间 = […」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/country-code-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\nInput: abc123测试 ❌ 未找到匹配的国家 支持：ISO 3166-1 alpha-2 代码（如 CN、US、JP）或中英文国名"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\nInput: abc123测试 ❌ 未找到匹配的国家 支持：I…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/country-flag",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "洲 大洋洲 非洲\nabc123测试\n未找到匹配项。当前仅收录 48 个常用国家/地区",
      "共 0 个国家/地区（仅收录 48 个常用国家/地区）"
    ],
    "ref": "IT-N309 更新：注入不存在的国家名 abc123测试 ⇒ 空态提示须明确「仅收录 48 个常用国家/地区」（grid 与 count 双处）；默认态列表非空、不含该提示 ⇒ 强判别、零逃生。expect 是「或」：两条分别锚 grid 空态与 count 范围说明，缺一即红。"
  },
  {
    "slug": "it/crontab-generator",
    "inputs": {
      "f_min": "abc123测试",
      "f_hour": "abc123测试",
      "f_dom": "abc123测试",
      "f_mon": "abc123测试",
      "f_dow": "abc123测试",
      "cronOut": "abc123测试"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\n⚠️ 分钟 字段超出范围或格式无效（允许 0-59；支持 *、*/n、a-b、a,b）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f_min\":\"abc123测试\",\"f_hour\":\"abc123测试\",\"f_dom\":\"abc123测试\",\"f_mon\":\"abc123测试\",\"f_dow\":\"abc123测试\",\"cronOut\":\"abc123测试\"}，输出区含「abc123测试\nabc123测试\nabc123测试\nabc123测试\nabc1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/cpp-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 现代 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 现代 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/csharp-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 现代 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 现代 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/crc-calculator",
    "inputs": {
      "input": "1\n2\n3"
    },
    "expect": [
      "MA-182 0xd7078d9d1d5056cc"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\"}，输出区含「MA-182 0xd7078d9d1d5056cc」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/css-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "string"
    },
    "expect": [
      "1 2 3\n1 2 3\nstring",
      "1 2 3\nstring\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"string\"}，输出区含「1 2 3\n1 2 3\nstring」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/css-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "60deg)}}\n4\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「60deg)}}\n4\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/css-minifier",
    "inputs": {
      "input": "1\n2\n3",
      "indentSize": "4"
    },
    "expect": [
      ": 16px; }\n4\n1 2 3\n5\n5\n0.0%",
      ": 16px; }\n1 2 3\n5\n5\n0.0%\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indentSize\":\"4\"}，输出区含「: 16px; }\n4\n1 2 3\n5\n5\n0.0%」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/css-minify",
    "inputs": {
      "src": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n压缩结果 5 原始字节 5 压缩后 0% 节省 1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"src\":\"1\\n2\\n3\"}，输出区含「1 2 3\n压缩结果 5 原始字节 5 压缩后 0% 节省 1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/csv-to-html-table",
    "inputs": {
      "csvInput": "1\n2\n3",
      "htmlOut": "1\n2\n3",
      "sepSel": ";"
    },
    "expect": [
      "数据行 3 列数 1 总行 3"
    ],
    "ref": "自动补强（B类零用例）：注入 csvInput=1/2/3、分隔符 `;`（单列 3 行）⇒ 统计「数据行 3 列数 1 总行 3」；默认示例为 3 列 2 行数据，不命中。修复后表体行会真实写入输出，不再只剩闭合标签。"
  },
  {
    "slug": "it/css-properties",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 列表 表格\n共 0 个属性"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 列表 表格\n共 0 个属性」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/csv-validator",
    "inputs": {
      "sep": "abc123测试",
      "src": "1\n2\n3"
    },
    "expect": [
      "1 2 3\nabc123测试\n校验结果 3 行数 1 标准列数 0 问题 ✅ 未发现列数/引号问题。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sep\":\"abc123测试\",\"src\":\"1\\n2\\n3\"}，输出区含「1 2 3\nabc123测试\n校验结果 3 行数 1 标准列数 0 问题 ✅ 未…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/csv-to-json",
    "inputs": {
      "customDelimiter": "abc123测试",
      "csvInput": "1\n2\n3",
      "jsonOutput": "1\n2\n3",
      "jsonInput": "1\n2\n3",
      "csvOutput": "1\n2\n3",
      "csvDelimiter": "\\t",
      "outDelimiter": "\\t"
    },
    "expect": [
      " column1 1 1 2 2 3 3\n3\n1\n是"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"customDelimiter\":\"abc123测试\",\"csvInput\":\"1\\n2\\n3\",\"jsonOutput\":\"1\\n2\\n3\",\"jsonInput\":\"1\\n2\\n3\",\"csvOutput\":\"1\\n2\\n3\",\"csvDelimiter\":\"\\\\t\",\"outDelimiter\":\"\\\\t\"}，输出区含「 column1 1 1 2 2 3 3\n3\n1\n是」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/cuid-generator",
    "inputs": {
      "count": "42"
    },
    "expect": [
      "clxfcphc0002f"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\"}，输出区含 cuid 计数器前缀「clxfcphc0002f」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑会先消耗 5 次 cuid() 调用（默认 count=5）⇒ 原锚的随机尾段整体位移，改锚「时间戳+计数器」确定性前缀（计数器仅随调用序递增、与种子 PRNG 取值无关）：boot 5 次 + 注入后 generate 首次 = 第 6 个 cuid，计数器位 base36 = f。"
  },
  {
    "slug": "it/curl-parser",
    "inputs": {
      "cmd": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n方法： GET URL： 1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cmd\":\"1\\n2\\n3\"}，输出区含「1 2 3\n方法： GET URL： 1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/date-duration",
    "inputs": {
      "d1": "abc123测试",
      "d2": "abc123测试",
      "inc": "incl"
    },
    "expect": [
      "abc123测试\nabc123测试\n相差 ⚠️ 请按 YYYY-MM-DD 格式填写两个日期。\nincl"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"d1\":\"abc123测试\",\"d2\":\"abc123测试\",\"inc\":\"incl\"}，输出区含「abc123测试\nabc123测试\n相差 ⚠️ 请按 YYYY-MM-DD 格式…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/decimal-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "sep": ","
    },
    "expect": [
      "1 2 3\n\u0001\u0002\u0003\n,",
      "1 2 3\n,\n\u0001\u0002\u0003"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"sep\":\",\"}，输出区含「1 2 3\n\u0001\u0002\u0003\n,」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑后元素创建序变为 input→sep→output（boot 的 enc 先读 input/sep 再写 output），blob 字段序随之改变，故 expect 容忍两种字段序；判别力仍在解码产物 \u0001\u0002\u0003（非输入回显）。"
  },
  {
    "slug": "it/des",
    "inputs": {
      "key": "0123456789abcdef0123456789abcdef0123456789abcdef",
      "iv": "0123456789abcdef",
      "input": "hello world",
      "algo": "3des",
      "mode": "CBC",
      "outputFormat": "hex",
      "output": ""
    },
    "checkIds": [
      "pkcs7"
    ],
    "clicks": ["encrypt()"],
    "expect": [
      "80a2142026acbc3842a787847d41b09e"
    ],
    "ref": "openssl 交叉验证：3DES-CBC/PKCS7，key=0123…cdef（24 字节）、iv=0123456789abcdef、明文 hello world ⇒ 80a2142026acbc3842a787847d41b09e。checkIds 还原 HTML 默认勾选的 PKCS7（桩内 checkbox 恒 false，11 字节明文非 8 倍数会被拦下）。原锚「3des」是算法下拉框回显、默认态即有（静态文案），已删。"
  },
  {
    "slug": "it/des",
    // IT-N296：合法输入算出密文后，改用非法密钥必须清掉旧结果，不能让用户误读为当前输出。
    "inputs": { "key": "0123456789abcdef", "iv": "", "input": "Now is t", "algo": "des", "mode": "ECB", "outputFormat": "hex", "output": "" },
    "clicks": ["encrypt();var before=document.getElementById('output').value;document.getElementById('key').value='not-hex-key';encrypt();var after=document.getElementById('output').value;document.getElementById('__tbProbe').textContent='STALE '+(before==='3fa40e8a984d4815'&&after===''?'OK':'BAD:'+before+'/'+after);"],
    "expect": ["STALE OK"],
    "ref": "IT-N296 状态链合法→非法：FIPS 向量 key=0123456789abcdef / 明文 Now is t / DES-ECB 无填充 ⇒ 3fa40e8a984d4815；随后把 key 改成非 hex，process() 必须先清空 output 再报错。旧实现保留上一次密文 ⇒ STALE BAD。默认参数为 3DES-CBC/48hex 密钥，不命中。"
  },
  {
    "slug": "it/docker-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "erfile\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「erfile\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/domain-name-generator",
    "inputs": {
      "kw": "abc123测试",
      "count": "42"
    },
    "expect": [
      "abc123测试\n42\nabc123."
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"kw\":\"abc123测试\",\"count\":\"42\"}，输出区含「abc123测试\n42\nabc123.」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/emacs-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 帮助 配置\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 帮助 配置\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/email-qr",
    "inputs": {
      "to": "abc123测试",
      "subject": "abc123测试",
      "body": "1\n2\n3"
    },
    "expect": [
      "mailto:abc123%E6%B5%8B%E8%AF%95?subject=abc123%E6%B5%8B%E8%AF%95"
    ],
    "ref": "真实 QR 改造后输出区保留 mailto 链接：注入 to/subject=abc123测试、body=1\\n2\\n3，链接前缀为 mailto:abc123%E6%B5%8B%E8%AF%95?subject=abc123%E6%B5%8B%E8%AF%95（encodeURIComponent 结果；innerHTML 中后续 & 会转 &amp;，故断言只取前段）。默认样例收件箱为 a@b.com，不出现该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/email-normalizer",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n❌ 无效邮箱\n缺少 @ 符号，不是有效邮箱\nabc123测试",
      "abc123测试\n缺少 @ 符号，不是有效邮箱\nabc123测试\n❌ 无效邮箱"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n❌ 无效邮箱\n缺少 @ 符号，不是有效邮箱\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/emoji-picker",
    "inputs": {
      "q": "abc123测试"
    },
    "expect": [
      "abc123测试\n共 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"q\":\"abc123测试\"}，输出区含「abc123测试\n共 0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/emoji-cheatsheet",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "用的会显示在这里\nabc123测试\n未找到匹配的 emoji\n共 0 个 emoji"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「用的会显示在这里\nabc123测试\n未找到匹配的 emoji\n共 0 个 emo…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/env-generator",
    "inputs": {
      "keyInput": "abc123测试",
      "valInput": "abc123测试",
      "importText": "1\n2\n3",
      "typeInput": "number",
      "formatSelect": "env-local"
    },
    "expect": [
      "ator\n.env.local\n64 B\nabc123测试\nabc123测试\n1 2 3\nnumber"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"keyInput\":\"abc123测试\",\"valInput\":\"abc123测试\",\"importText\":\"1\\n2\\n3\",\"typeInput\":\"number\",\"formatSelect\":\"env-local\"}，输出区含「ator\n.env.local\n64 B\nabc123测试\nabc123测试\n1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/exponential-distribution",
    "inputs": {
      "lambda": "42",
      "x": "42"
    },
    "expect": [
      " x) 生存函数 0.024 均值 1/λ 0.001 方差 1/λ² 0.024 标准差 0.017"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lambda\":\"42\",\"x\":\"42\"}，输出区含「 x) 生存函数 0.024 均值 1/λ 0.001 方差 1/λ² 0.02…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "it/git-commands",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "模块 工作流\n共 0 个命令"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「模块 工作流\n共 0 个命令」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/go-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "kind": "rune"
    },
    "expect": [
      "1 2 3\n1 2 3\nrune",
      "1 2 3\nrune\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"kind\":\"rune\"}，输出区含「1 2 3\n1 2 3\nrune」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/go-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "标准库 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「标准库 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/graphql-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      " } } } }\n4\n",
      "createdAt } } } } }\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「 } } } }\n4\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/hash-id-generator",
    "inputs": {
      "salt": "abc123测试",
      "nums": "abc123测试",
      "minLen": "42",
      "alphabet": "abc123测试"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\nabc123测试",
      "abc123测试\n42\nabc123测试\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"salt\":\"abc123测试\",\"nums\":\"abc123测试\",\"minLen\":\"42\",\"alphabet\":\"abc123测试\"}，输出区含「abc123测试\nabc123测试\n42\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/hash",
    "inputs": {
      "hmacKey": "abc123测试",
      "verifyHash": "abc123测试",
      "textInput": "1\n2\n3",
      "batchInput": "1\n2\n3",
      "verifyInput": "1\n2\n3",
      "batchAlgoSelect": "sha1"
    },
    "expect": [
      "MD5 bfb77520994c313d1abff83000f19dc3 复制"
    ],
    "ref": "独立复算：md5('1\\n2\\n3') = bfb77520994c313d1abff83000f19dc3（node crypto 实测，与页面 MD5 结果行逐字一致）。注入另一键 batchInput / verifyInput 用于覆盖批量与校验区。2026-11-05 同批修正：真实 localStorage 桩下注入即 saveHistory 写历史并重渲染，原自动补强 expect 里的「暂无历史记录」是本就不该出现的占位串（旧空桩把 setItem 吞掉才侥幸保留）；改锚结果区派生摘要，绕开 #historyList（历史行含运行时刻，必然漂移）。默认态 textInput 为空 ⇒ 不渲染摘要。"
  },
  {
    "slug": "it/hex-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "sep": " "
    },
    "expect": [
      "1 2 3\n31 0a 32 0a 33"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"sep\":\" \"}，输出区含「1 2 3\n31 0a 32 0a 33」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/hash-multi",
    "inputs": {
      "input": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n✅ 已计算 0 种算法（5 字符）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\"}，输出区含「1 2 3\n✅ 已计算 0 种算法（5 字符）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/hill-cipher",
    "inputs": {
      "key": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "abc123测试\n无效矩阵\n1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「abc123测试\n无效矩阵\n1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/hmac-generator",
    "inputs": {
      "key": "abc123测试",
      "msg": "1\n2\n3"
    },
    "expect": [
      "C-SHA512 05ae9e127c1299a229201d8d74f240832260fdcf12d42bb75347a772b5b0a676327d4f0de81041aa3e21b08cea81204986ff5efe9a5c50d"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"msg\":\"1\\n2\\n3\"}，输出区含「C-SHA512 05ae9e127c1299a229201d8d74f2408…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/html-entities-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "decimal"
    },
    "expect": [
      "1 2 3\ndecimal"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"decimal\"}，输出区含「1 2 3\ndecimal」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/html-nesting-checker",
    "inputs": {
      "html": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"html\":\"1\\n2\\n3\"}，输出区含「1 2 3\n✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/html-entity-encoder",
    "inputs": {
      "encodeInput": "1\n2\n3",
      "encodeOutput": "1\n2\n3",
      "decodeInput": "1\n2\n3",
      "decodeOutput": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"encodeInput\":\"1\\n2\\n3\",\"encodeOutput\":\"1\\n2\\n3\",\"decodeInput\":\"1\\n2\\n3\",\"decodeOutput\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/html-minifier",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "l>\n0\n0\n0%\n1 2 3",
      "</html>\n1 2 3\n0\n0\n0%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「l>\n0\n0\n0%\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/html-entities",
    "inputs": {
      "searchInput": "abc123测试",
      "encoderInput": "1\n2\n3"
    },
    "expect": [
      "何 字母变体\n共 0 个实体\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\",\"encoderInput\":\"1\\n2\\n3\"}，输出区含「何 字母变体\n共 0 个实体\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/html-escape",
    "inputs": {
      "input": "<b>x</b>",
      "batchInput": "1\n2\n3"
    },
    "expect": [
      "&lt;b&gt;x&lt;/b&gt;"
    ],
    "ref": "HTML 转义语义自校验：'<b>x</b>' 转义后为 '&lt;b&gt;x&lt;/b&gt;'（标签括号变实体，字母原样）。原用例注入 '1\\n2\\n3'（无特殊字符）导致输出与输入逐字相同、期望串恰等于输入回显的逃生形态；改注入含标签的文本后锚点由转义结果派生。2026-11-05 同批修正：真实 localStorage 桩下注入即写历史并重渲染，原 expect 里的「暂无历史记录」不再出现。默认态输入为空 ⇒ 不命中。"
  },
  {
    "slug": "it/html-tags",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "入内容 废弃\n共 0 个标签"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「入内容 废弃\n共 0 个标签」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/http-cache",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "CDN 清理\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「CDN 清理\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/http-headers",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 响应 性能\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 响应 性能\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/http-cookies",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 响应 废弃\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 响应 废弃\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/http-methods",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "展 扩展示例\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「展 扩展示例\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/http-response-headers",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "lt-Svc\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「lt-Svc\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/http-status",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "No matching status code.\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「No matching status code.\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/hypergeometric-distribution",
    "inputs": {
      "N": "42",
      "K": "42",
      "n": "42",
      "k": "42"
    },
    "expect": [
      "42\n42\n42\n42\nP(X = 42) = 1 1 P(X = 42) 1 P(X ≤ 42) 1 P(X ≥ 42) 0",
      "恰好抽中 k=42 个目标的概率为 100.0000%\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"N\":\"42\",\"K\":\"42\",\"n\":\"42\",\"k\":\"42\"}，输出区含「42\n42\n42\n42\nP(X = 42) = 1 1 P(X = 42) 1 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  
  {
    "slug": "it/hypothesis-test",
    "inputs": {
      "mean": "42",
      "mu0": "42",
      "sigma": "42",
      "n": "42",
      "alpha": "42",
      "tail": "left"
    },
    "expect": [
      "42\n42\n42\n42\n42\nleft\nα 必须在 (0, 0.5]"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mean\":\"42\",\"mu0\":\"42\",\"sigma\":\"42\",\"n\":\"42\",\"alpha\":\"42\",\"tail\":\"left\"}，输出区含「42\n42\n42\n42\n42\nleft\nα 必须在 (0, 0.5]」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/invite-code-generator",
    "inputs": {
      "count": "42",
      "len": "42",
      "prefixVal": "abc123测试"
    },
    "expect": [
      "42\n42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\",\"len\":\"42\",\"prefixVal\":\"abc123测试\"}，输出区含「42\n42\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/invite-code-generator",
    "inputs": {"count": "30", "len": "4"},
    "clicks": ["document.getElementById('upper').checked=true;document.getElementById('num').checked=true;document.getElementById('noAmb').checked=true;var __r=randInt;randInt=function(){return 0;};generate();randInt=__r;var h=document.getElementById('output').innerHTML;var rows=(h.match(/class=.code-row.>/g)||[]).length;document.getElementById('output').innerHTML='DEDUP rows='+rows+' err='+(h.indexOf('组合空间不足')>=0?1:0);"],
    "expect": ["DEDUP rows=0 err=1"],
    "ref": "IT-N410：批量码必须互不相同。把 randInt 固定成恒 0 构造必然碰撞：修复前 30 行全是同一个码(rows=30)、且不报错；修复后 Set 去重在尝试上限内补不满 ⇒ 明确报「组合空间不足」且一行码都不输出(rows=0, err=1)。用桩固定随机源使结果完全确定，不赌碰撞概率。"
  },
  {
    "slug": "it/invite-code-generator",
    "clicks": ["document.getElementById('output').innerHTML='LUHN ab='+luhnCheckDigit('AB')+' ba='+luhnCheckDigit('BA')+' same='+(luhnCheckDigit('AB')===luhnCheckDigit('BA')?1:0);"],
    "expect": ["LUHN ab=7 ba=8 same=0"],
    "ref": "IT-N411：旧校验位是字符码求和取模，'AB' 与 'BA' 的校验位相同(都是 1)⇒ 相邻换位检不出。Luhn 变体按位权交替 ⇒ AB→7、BA→8，可检出换位。修复前无 luhnCheckDigit 函数 ⇒ clicks 抛错、结果区无 LUHN 串。"
  },
  {
    "slug": "it/invite-code-generator",
    "inputs": {"verifyInput": "AB7"},
    "clicks": ["verifyCode();var h=document.getElementById('output').innerHTML;document.getElementById('output').innerHTML='VER ok='+(h.indexOf('校验通过')>=0?1:0)+' q='+(document.getElementById('verifyInput').value==='AB7'?1:0);"],
    "expect": ["VER ok=1 q=1"],
    "ref": "IT-N411：新增的校验入口必须对带正确校验位的码给出「校验通过」。修复前页面根本没有校验输入框与 verifyCode()，clicks 抛错 ⇒ 变红。q=1 绑注入值防静态逃生。"
  },
  {
    "slug": "it/invite-code-generator",
    "inputs": {"verifyInput": "AB8"},
    "clicks": ["verifyCode();var h=document.getElementById('output').innerHTML;document.getElementById('output').innerHTML='VER bad='+(h.indexOf('校验失败')>=0?1:0)+' q='+(document.getElementById('verifyInput').value==='AB8'?1:0);"],
    "expect": ["VER bad=1 q=1"],
    "ref": "IT-N411：把 AB7 末位改成 8 必须判「校验失败」，证明校验真的在算而不只是回显。修复前无校验入口 ⇒ 变红。"
  },
  {
    "slug": "it/invite-code-generator",
    "inputs": {"verifyInput": "INV-AB7"},
    "clicks": ["verifyCode();var h=document.getElementById('output').innerHTML;document.getElementById('output').innerHTML='PFX ok='+(h.indexOf('校验通过')>=0?1:0)+' q='+(document.getElementById('verifyInput').value.indexOf('INV-')===0?1:0);"],
    "expect": ["PFX ok=1 q=1"],
    "ref": "IT-N411：勾选「加前缀」生成的码形如 INV-XXXXXXX，校验入口必须能剥掉前缀后验主体，否则该功能对默认开启前缀的用户不可用。"
  },
  {
    "slug": "it/invite-code-generator",
    "clicks": ["var c='AB'+luhnCheckDigit('AB');document.getElementById('output').innerHTML='ROUND c='+c+' ok='+(verifyLuhn(c)?1:0);"],
    "expect": ["ROUND c=AB7 ok=1"],
    "ref": "IT-N411：生成侧 appendChecksum 与校验侧 verifyLuhn 必须同源可逆（追加校验位后整码自校验通过）。修复前两函数都不存在 ⇒ 变红。"
  },
  {
    "slug": "it/integer-base-converter",
    "inputs": {
      "num": "abc123测试",
      "fromBase": "42",
      "toBase": "42"
    },
    "expect": [
      "源进制与目标进制都必须是 2 到 36 的整数"
    ],
    "ref": "注入非默认输入{\"num\":\"abc123测试\",\"fromBase\":\"42\",\"toBase\":\"42\"}：IT-N48-b 修复后越界基数不再静默钳到 36，而是保留输入并输出明确报错。旧断言锚定『钳到 36 后 toBigInt 在第 7 位抛错』正是被修复的缺陷行为，随修复更新。默认态 16→10 合法、无此报错串 ⇒ 不命中。"
  },
  {
    "slug": "it/ipv4-range-expander",
    "inputs": {
      "cidr": "abc123测试"
    },
    "expect": [
      "abc123测试\n网段解析 ⚠️ 格式应为 IP/前缀，如"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cidr\":\"abc123测试\"}，输出区含「abc123测试\n网段解析 ⚠️ 格式应为 IP/前缀，如」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ipv6-converter",
    "inputs": {
      "addr": "abc123测试"
    },
    "expect": [
      "abc123测试\n转换结果 ⚠️ 不是合法的 IPv6 地址。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"addr\":\"abc123测试\"}，输出区含「abc123测试\n转换结果 ⚠️ 不是合法的 IPv6 地址。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ip-calculator",
    "inputs": {
      "ipInput": "abc123测试",
      "ipOnly": "abc123测试",
      "maskInput": "42",
      "ipv6Input": "abc123测试",
      "subnetBase": "abc123测试",
      "subnetOldMask": "42",
      "subnetNewMask": "42"
    },
    "expect": [
      "无效的 IP 或前缀"
    ],
    "ref": "自动补强（B类零用例）·2026-11-06 随 IT-N71 改造重写：原断言是把整段 blob（含输入回显 abc123测试/42）拼成一条超长串，页面任何合法改动都会失配，且回显段零判别力。现改为断言计算结论——ipInput 无斜杠 ⇒ 走 ipOnly+maskInput 分支，ipToInt('abc123测试') 失败 ⇒ showInvalidV4() 输出「无效的 IP 或前缀」。该串只在无效输入时由分支产生，默认态（192.168.1.0/24 合法）不出现。"
  },
  {
    "slug": "it/java-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ipv6-ula",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "生成的 IPv6 ULA（42 个）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入 cnt=42 ⇒ 计数行必为「生成的 IPv6 ULA（42 个）」，默认 cnt=3 不命中。地址本体已改 crypto.getRandomValues，无固定串可锚，只锚随 cnt 变的确定性计数行 ⇒ 强判别、零逃生。dataGrid 报错系 harness 通用探针已知问题（同 mac-generator），不参与匹配。"
  },
  {
    "slug": "it/java-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 语法 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 语法 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/js-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/js-minifier",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      ");\n0\n0\n0%\n1 2 3",
      "doubled);\n1 2 3\n0\n0\n0%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「);\n0\n0\n0%\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/js-minify",
    "inputs": {
      "src": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n压缩结果 5 原始字节 5 压缩后 0% 节省 1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"src\":\"1\\n2\\n3\"}，输出区含「1 2 3\n压缩结果 5 原始字节 5 压缩后 0% 节省 1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/js-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "name}!`;\n4\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「name}!`;\n4\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/js-obfuscator",
    "inputs": {
      "inputCode": "1\n2\n3",
      "outputCode": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3\n5\n5\n+0%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputCode\":\"1\\n2\\n3\",\"outputCode\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3\n5\n5\n+0%」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/json-minify",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\nJSON parsing failed: Unexpected non-whitespace character after JSON at position 2 (line 2 column 1)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\nJSON parsing failed: Unexpected no…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "1\n2\n3", "right": "1\n2\n3" },
    "clicks": ["var __t=[];var __o=ToolBox.showToast;ToolBox.showToast=function(s){__t.push(String(s));};doDiff();ToolBox.showToast=__o;document.getElementById('jsonDiff').textContent='ERR n='+__t.length+' has='+(/JSON \u89e3\u6790\u9519\u8bef/.test(__t.join('|'))?1:0);"],
    "expect": ["ERR n=1 has=1"],
    "ref": "非法 JSON（`1\\n2\\n3`）必须走解析失败分支：只弹一次错误 toast、且提示里点名「JSON 解析错误」。修复前该用例是自动补强的弱断言（expect 命中下拉框回显 `simple`，零判别力），本批随页面改动一并换成真实行为断言；输入含真实换行 ⇒ 与默认样例的合法 JSON 无交集。"
  },
  // ---- IT-N396 / IT-N397：对比模式与数组按内容匹配接线 ----
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"a\":{\"x\":1},\"b\":2}", "right": "{\"a\":{\"x\":9},\"b\":2}", "diffMode": "deep" },
    "expect": ["\"path\": \"a.x\""],
    "ref": "IT-N396（对照组）：深度对比必须递归展开到叶子，路径为 `a.x`。简单模式同一输入只出 `\"path\": \"a\"`（不展开），故本串仅在 deep 生效时出现。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"a\":{\"x\":1},\"b\":2}", "right": "{\"a\":{\"x\":9},\"b\":2}", "diffMode": "simple" },
    "expect": ["\"path\": \"a\", \"from\": { \"x\": 1 }"],
    "ref": "IT-N396：简单对比只看顶层键，嵌套变化合并成一处 mod。修复前 `doDiff` 从不读 `diffMode`，两种模式输出逐字节相同（都是 `\"path\": \"a.x\"`）⇒ 该串换模式后不可能出现。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"t\":[1,2]}", "right": "{\"t\":[1,2,3]}", "diffMode": "simple" },
    "expect": ["\"path\": \"t\", \"from\": [ 1, 2 ], \"to\": [ 1, 2, 3 ]"],
    "ref": "IT-N396：简单模式把数组当整体值比，只出一处 mod；深度模式同一输入是 `add t[2]`。修复前模式无效 ⇒ 恒为后者。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"tags\":[\"a\",\"b\"]}", "right": "{\"tags\":[\"b\",\"a\"]}", "diffMode": "deep" },
    "clicks": ["document.getElementById('arrayMatch').checked=true;doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('jsonDiff').textContent='ARRM n='+d.length+' q='+(document.getElementById('left').value.indexOf('tags')>=0?1:0);"],
    "expect": ["ARRM n=0 q=1"],
    "ref": "IT-N397：勾选「数组按内容匹配」后，元素换序不应再报成逐项修改。修复前数组只按下标对齐 ⇒ `tags[0]`、`tags[1]` 两处 mod（n=2）。`q=1` 绑注入值（注入失败时 left 回落默认样例、不含 tags ⇒ 整例 FAIL），避免与输入无关的静态断言。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"tags\":[\"a\",\"b\"]}", "right": "{\"tags\":[\"b\",\"a\",\"c\"]}", "diffMode": "deep" },
    "clicks": ["document.getElementById('arrayMatch').checked=true;doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('jsonDiff').textContent='ARRM2 n='+d.length+' mod='+d.filter(function(x){return x.op==='mod';}).length+' add='+d.filter(function(x){return x.op==='add';}).length+' p='+(d[0]?d[0].path:'-')+' q='+(document.getElementById('left').value.indexOf('tags')>=0?1:0);"],
    "expect": ["ARRM2 n=1 mod=0 add=1 p=tags[2] q=1"],
    "ref": "IT-N397：换序 + 追加的组合用例。按内容对齐后只应剩 `add tags[2]`（mod 必须为 0）。修复前是 2 mod + 1 add（n=3）⇒ 四元组完全不同。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"items\":[{\"id\":1},{\"id\":2}]}", "right": "{\"items\":[{\"id\":2},{\"id\":1}]}", "diffMode": "deep" },
    "clicks": ["document.getElementById('arrayMatch').checked=true;doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('jsonDiff').textContent='AM3 n='+d.length+' q='+(document.getElementById('left').value.indexOf('items')>=0?1:0);"],
    "expect": ["AM3 n=0 q=1"],
    "ref": "IT-N397：对象数组换序同样应判为无内容差异。比较键用排序后的规范序列化，故键序不同的 `{id:1}` 也能配对上。修复前是 `items[0].id`、`items[1].id` 两处 mod。"
  },
  {
    "slug": "it/json-diff",
    "inputs": { "left": "{\"constructor\":1}", "right": "{}" },
    "expect": ["\"op\": \"del\", \"path\": \"constructor\""],
    "ref": "IT-N397 同批顺带修：成员判断原来用 `k in b`（走原型链），`'constructor' in {}` 为真 ⇒ 该键被当成「两侧都有」而递归比对 function，报成 mod 甚至丢键。改用 `Object.prototype.hasOwnProperty.call` 后正确报 del。默认样例无 constructor 键。"
  },
  {
    "slug": "it/json-diff",
    "inputs": {
      "left": "{\"tags\":[\"a\",\"b\",\"c\"]}",
      "right": "{\"tags\":[\"c\",\"b\",\"a\"]}",
      "diffMode": "deep"
    },
    "clicks": [
      "document.getElementById('arrayMatch').checked=true;doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('__tbProbe').textContent='JDMUL n='+d.length+' mod='+d.filter(function(x){return x.op==='mod';}).length+' q='+document.getElementById('left').value.length;"
    ],
    "expect": [
      "JDMUL n=0 mod=0 q=22"
    ],
    "ref": "复核失败重做·IT-N396 1/6（三元素完全逆序）：勾选数组按内容匹配，`{\"tags\":[\"a\",\"b\",\"c\"]}` 对 `{\"tags\":[\"c\",\"b\",\"a\"]}` 内容多重集相同，应判 0 处差异。修复前 LCS 只能配到 1 个元素，剩余项按下标硬配对 ⇒ `n=2 mod=2`；修复后剩余项先按规范内容多重集抵消 ⇒ `JDMUL n=0 mod=0 q=22` ⇒ 强判别。"
  },
  {
    "slug": "it/json-diff",
    "inputs": {
      "left": "{\"tags\":[\"a\",\"b\",\"c\"]}",
      "right": "{\"tags\":[\"c\",\"x\",\"a\"]}",
      "diffMode": "deep"
    },
    "clicks": [
      "document.getElementById('arrayMatch').checked=true;doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('__tbProbe').textContent='JDMIX n='+d.length+' mod='+d.filter(function(x){return x.op==='mod';}).length+' p='+(d[0]?d[0].path:'-')+' q='+document.getElementById('left').value.length;"
    ],
    "expect": [
      "JDMIX n=1 mod=1 p=tags[1] q=22"
    ],
    "ref": "复核失败重做·IT-N396 2/6（逆序 + 真变化）：`[\"a\",\"b\",\"c\"]` 对 `[\"c\",\"x\",\"a\"]`，应只报 1 处 mod（b→x）。修复前 `n=2 mod=2 p=tags[0]`；修复后多重集抵消掉 c/a，只剩 b 与 x 递归比对 ⇒ `JDMIX n=1 mod=1 p=tags[1] q=22` ⇒ 强判别，同时证明抵消没有把真变化吞掉。"
  },
  {
    "slug": "it/json-diff",
    "inputs": {
      "left": "{\"a\":{\"__proto__\":{\"v\":1}}}",
      "right": "{\"a\":{\"__proto__\":{\"v\":2}}}",
      "diffMode": "simple"
    },
    "clicks": [
      "doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('__tbProbe').textContent='JDPROTO n='+d.length+' op='+(d[0]?d[0].op:'-')+' path='+(d[0]?d[0].path:'-')+' q='+document.getElementById('left').value.length;"
    ],
    "expect": [
      "JDPROTO n=1 op=mod path=a q=27"
    ],
    "ref": "复核失败重做·IT-N397 3/6（简单模式嵌套特殊键）：`{\"a\":{\"__proto__\":{\"v\":1}}}` 对同处值为 2。修复前 `jdCanon` 用普通 `{}`，`o[\"__proto__\"]=...` 触发原型 setter、序列化丢键 ⇒ 两侧比较键都是 `{}` ⇒ `n=0 op=- path=-`；修复后无原型对象保住自有键 ⇒ `JDPROTO n=1 op=mod path=a q=27` ⇒ 强判别。"
  },
  {
    "slug": "it/json-diff",
    "inputs": {
      "left": "{\"__proto__\":{\"v\":1}}",
      "right": "{\"__proto__\":{\"v\":2}}",
      "diffMode": "simple"
    },
    "clicks": [
      "doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('__tbProbe').textContent='JDTOP n='+d.length+' op='+(d[0]?d[0].op:'-')+' path='+(d[0]?d[0].path:'-')+' q='+document.getElementById('left').value.length;"
    ],
    "expect": [
      "JDTOP n=1 op=mod path=__proto__ q=21"
    ],
    "ref": "复核失败重做·IT-N397 4/6（简单模式顶层特殊键）：`{\"__proto__\":{\"v\":1}}` 对 `{\"__proto__\":{\"v\":2}}`。修复前 `simpleDiff` 的去重表用普通 `{}`，`seen[\"__proto__\"]` 命中 Object.prototype 为 truthy ⇒ 该键被整个跳过，加上 jdCanon 丢键 ⇒ `n=0`；修复后去重表与规范化都用 `Object.create(null)` ⇒ `JDTOP n=1 op=mod path=__proto__ q=21` ⇒ 强判别。"
  },
  {
    "slug": "it/json-diff",
    "inputs": {
      "left": "{\"arr\":[{\"__proto__\":{\"v\":1}}]}",
      "right": "{\"arr\":[{\"__proto__\":{\"v\":2}}]}",
      "diffMode": "deep"
    },
    "clicks": [
      "document.getElementById('arrayMatch').checked=true;doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('__tbProbe').textContent='JDARR n='+d.length+' op='+(d[0]?d[0].op:'-')+' path='+(d[0]?d[0].path:'-')+' q='+document.getElementById('left').value.length;"
    ],
    "expect": [
      "JDARR n=1 op=mod path=arr[0].__proto__.v q=31"
    ],
    "ref": "复核失败重做·IT-N397 5/6（数组元素含特殊键，按内容匹配）：`{\"arr\":[{\"__proto__\":{\"v\":1}}]}` 对同处值为 2，deep + 按内容匹配。修复前元素比较键相同被 LCS 直接配对 ⇒ `n=0`；修复后比较键不同、多重集也无匹配 ⇒ 递归到叶子 ⇒ `JDARR n=1 op=mod path=arr[0].__proto__.v q=31` ⇒ 强判别。"
  },
  {
    "slug": "it/json-diff",
    "inputs": {
      "left": "{\"a\":{\"x\":1,\"y\":2}}",
      "right": "{\"a\":{\"y\":2,\"x\":1}}",
      "diffMode": "simple"
    },
    "clicks": [
      "doDiff();var d=JSON.parse(document.getElementById('jsonDiff').textContent);document.getElementById('__tbProbe').textContent='JDORDER n='+d.length+' q='+document.getElementById('left').value.length;"
    ],
    "expect": [
      "JDORDER n=0 q=19"
    ],
    "ref": "复核失败重做·IT-N397 6/6（键序护栏）：`{\"a\":{\"x\":1,\"y\":2}}` 对 `{\"a\":{\"y\":2,\"x\":1}}` 在简单模式应仍判 0 处差异。本例修复前后都应 PASS，用于证明改用无原型对象后的规范序列化仍按键名排序，没有把「仅键序不同」误报成变化；默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": {
      "schema": "1\n2\n3",
      "data": "1\n2\n3"
    },
    "expect": [
      "JSON Schema 解析失败"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"schema\":\"1\\n2\\n3\",\"data\":\"1\\n2\\n3\"}，输出区点名「JSON Schema 解析失败」并附 JSON.parse 的行列位置；默认示例（合法 schema/data）通过校验，不含该串 ⇒ 强判别、零逃生。"
  },
  // ---- IT-N398 / IT-N399 / IT-N400：根 schema 类型推断、null 合法、联合 type 与原型链 ----
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"required\":[\"a\"],\"properties\":{\"a\":{\"type\":\"string\"}}}", "data": "{\"a\":1}" },
    "expect": ["类型不匹配 root.a: 期望 string"],
    "ref": "IT-N398（高）：根 schema 省略 `type:\"object\"` 时，`properties`/`required` 本身即隐含对象约束，必须继续按对象校验。修复前 `walk` 只在 `schema.type==='object'` 时进对象分支 ⇒ 明显非法的数据被判「校验通过」。默认示例的 schema 带 type，不会产生该串。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"required\":[\"a\"],\"properties\":{\"a\":{\"type\":\"string\"}}}", "data": "{}" },
    "expect": ["缺少必填字段: root.a"],
    "ref": "IT-N398（高）：同一 schema（无根 type）下空对象必须报缺少必填。修复前整段 required 检查被跳过 ⇒ 「校验通过」。默认示例 required 是 name 且有值 ⇒ 不含该串。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"properties\":{\"a\":{\"type\":\"string\"}},\"additionalProperties\":false}", "data": "{\"a\":\"x\",\"b\":1}" },
    "expect": ["存在未允许字段: root.b"],
    "ref": "IT-N398（高）：根无 type 时 `additionalProperties:false` 同样必须生效。修复前额外字段检查整段不执行 ⇒ 「校验通过」。默认示例虽也有 additionalProperties:false，但其数据没有多余字段 ⇒ 不产生该串。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"type\":\"array\",\"items\":{\"required\":[\"id\"],\"properties\":{\"id\":{\"type\":\"number\"}}}}", "data": "[{\"id\":1},{\"name\":\"x\"}]" },
    "expect": ["缺少必填字段: root[1].id"],
    "ref": "IT-N398：`items` 里的子 schema 同样常省略 `type`，需按 properties/required 推断为对象并校验到具体下标。修复前第二项被整体放过。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"type\":[\"string\",\"number\"]}", "data": "{}" },
    "expect": ["期望 string / number"],
    "ref": "IT-N400：`type` 允许联合数组，任一匹配即通过、全不匹配必须报错。修复前 `typeOK` 逐字符串比较，数组与每个字面量都不相等 ⇒ 落到 `return true`，任意数据都判通过。默认示例的 type 是单个字符串 ⇒ 不产生该串。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"type\":\"object\",\"required\":[\"constructor\"]}", "data": "{}" },
    "expect": ["缺少必填字段: root.constructor"],
    "ref": "IT-N400：必填检查必须用 hasOwnProperty。修复前 `k in val` 命中 `Object.prototype` ⇒ `{}` 被当成「含有 constructor」而通过。输入数据就是空对象，不可能自带该错误串。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"type\":\"object\",\"properties\":{\"a\":{\"type\":\"string\"}},\"additionalProperties\":false}", "data": "{\"a\":\"x\",\"toString\":1}" },
    "expect": ["存在未允许字段: root.toString"],
    "ref": "IT-N400：额外字段判断同理——`!(k in props)` 会把 `toString` 当成属性表里已有 ⇒ 漏报。修复前该数据判「校验通过」。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"type\":\"null\"}", "data": "null" },
    "clicks": ["var r=document.getElementById('result');var ok=r.innerHTML.indexOf('校验通过')>=0?1:0;r.textContent='N399 v='+(document.getElementById('data').value==='null'?1:0)+' ok='+ok;"],
    "expect": ["N399 v=1 ok=1"],
    "ref": "IT-N399：合法的 JSON null 必须能通过 `{\"type\":\"null\"}` 的校验，不能被当成「JSON 格式错误」。该页 `parseSafely` 已返回 `{ok,value}`（早期批次已修），本用例作为回归锁；`v=1` 绑注入值（注入失败时 data 回落默认对象 ⇒ v=0 ⇒ FAIL），避免退化成「与输入无关」的逃生断言。"
  },
  {
    "slug": "it/json-schema-validator",
    "inputs": { "schema": "{\"type\":[\"object\",\"null\"]}", "data": "null" },
    "clicks": ["var r=document.getElementById('result');var ok=r.innerHTML.indexOf('校验通过')>=0?1:0;r.textContent='N400N v='+(document.getElementById('data').value==='null'?1:0)+' ok='+ok;"],
    "expect": ["N400N v=1 ok=1"],
    "ref": "IT-N400 边界：联合类型含 null 时 null 必须放行，不能被对象分支误报「root 不是对象」（本批实现里 `else if (explicitObj && val !== null)` 就是为此）。同上的 `v=1` 防逃生。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<p>支持 <strong>HTML 转 Markdown</strong>，保留标题、列表与链接。</p>"},
    "expect": ["支持 **HTML 转 Markdown**，保留标题、列表与链接。"],
    "ref": "IT-N401（高）：说明区承诺 strong/b → `**`，实现里原本没有 STRONG/EM 分支、P 又用 innerText 取纯文本 ⇒ 加粗信息整段丢失（默认示例首屏即可复现）。输入是带标签的 HTML，不含 `**` ⇒ 断言串只能来自转换结果。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<p><em>斜体</em> 与 <b>粗</b> 与 <i>他</i></p>"},
    "expect": ["_斜体_ 与 **粗** 与 _他_"],
    "ref": "IT-N401：em/i → `_`、b → `**` 两条映射都必须生效（b/i 是 strong/em 的别名标签）。修复前输出是「斜体 与 粗 与 他」，无任何标记符号。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<p>2 * 3 * 4 与 a_b</p>"},
    "expect": ["2 \\* 3 \\* 4 与 a\\_b"],
    "ref": "IT-N402：`escapeMarkdown` 定义后从未被调用，正文里的 `*`/`_` 原样输出会被 Markdown 渲染成斜体。修复前输出与输入一致（无反斜杠）⇒ 该串只可能来自转义路径。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<p>a<br>b</p>"},
    "clicks": ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('mdOutput').value='BR hard='+(v.indexOf('a  '+String.fromCharCode(10)+'b')>=0?1:0)+' flat='+(v==='a b'?1:0)+' q='+(document.getElementById('htmlInput').value.indexOf('<br>')>=0?1:0);"],
    "expect": ["BR hard=1 flat=0 q=1"],
    "ref": "IT-N403：`<br>` 必须转成「行尾两个空格 + 换行」的硬换行。blob 会把空白折叠（collectStrings 对 value 也做 \\s+ → 单空格），故用 clicks 在页面内判形态：修复前 BR 返回单个换行、被段落折叠成空格 ⇒ v === 'a b'。`q=1` 绑注入值防静态逃生。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<ul><li>a<ul><li>b</li></ul></li></ul>"},
    "clicks": ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('mdOutput').value='UL nested='+(v.indexOf('- a'+String.fromCharCode(10)+'  - b')>=0?1:0)+' flat='+(v.indexOf('- a - b')>=0?1:0)+' q='+(document.getElementById('htmlInput').value.indexOf('<ul>')>=0?1:0);"],
    "expect": ["UL nested=1 flat=0 q=1"],
    "ref": "IT-N403：嵌套列表必须保留层级（父项 + 换行 + 两空格缩进的子项）。修复前列表项 body 走 `replace(/\\n+/g,' ')` 把子列表压平 ⇒ 输出 `- a - b`。blob 折叠空白，故用 clicks 在页面内判相邻形态；`q=1` 绑注入值防静态逃生。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<table><thead><tr><th>名称</th></tr></thead><tbody><tr><td><strong>粗</strong></td></tr></tbody></table>"},
    "expect": ["| **粗** |"],
    "ref": "IT-N401：表格单元格原本用 innerText 取纯文本，行内格式同样丢失；改递归后单元格里也要保留 `**`。输入 HTML 不含 `**`。"
  },
  {
    "slug": "it/html-to-markdown",
    "htmlDom": true,
    "inputs": {"htmlInput": "<p>正文</p><script>alert(\"zzz9\")</script><style>.zzz9{}</style>"},
    "clicks": ["convert();var v=document.getElementById('mdOutput').value;document.getElementById('mdOutput').value='N404 js='+(v.indexOf('zzz9')>=0?1:0)+' t='+(v.indexOf('正文')>=0?1:0);"],
    "expect": ["N404 js=0 t=1"],
    "ref": "IT-N404：SCRIPT/STYLE 文本必须整段丢弃（注意事项承诺「脚本等表现层信息会被丢弃」）。修复前落到默认 innerMarkdown，脚本源码 `zzz9` 被写进 Markdown。`t=1` 绑注入值（注入失败时回落默认样例、不含「正文」⇒ 整例 FAIL），避免变成静态逃生项。"
  },
  {
    "slug": "it/json-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      " JSON 有效\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「 JSON 有效\n4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/json-to-code",
    "inputs": {
      "rootName": "abc123测试",
      "input": "1\n2\n3"
    },
    "expect": [
      "01-01\" }\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rootName\":\"abc123测试\",\"input\":\"1\\n2\\n3\"}，输出区含「01-01\" }\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var o={u:{aa:1}};var c=toPython(o,'Root');var iD=c.indexOf('class RootU('),iR=c.indexOf('class Root(');document.getElementById('__tbProbe').textContent='PYORD ok='+((iD>=0&&iR>=0&&iD<iR)?1:0)+' ref='+(c.indexOf('u: RootU')>=0?1:0);"
    ],
    "expect": [
      "PYORD ok=1 ref=1"
    ],
    "ref": "复核失败重做·IT-N380 1/7（Python 嵌套类型定义顺序）：`{\"u\":{\"aa\":1}}` 生成代码里 `class RootU` 必须出现在 `class Root` 之前，且根里仍有 `u: RootU` 引用。修复前子类型排在根之后，真实 python3 执行报 `NameError: name RootU is not defined`；修复后 `PYORD ok=1 ref=1` ⇒ 强判别。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var o1={orders:[{id:1}]};var c1=toPython(o1,'Root');var d1=c1.indexOf('class RootOrders(');var a1=(d1>=0&&d1<c1.indexOf('class Root('))?1:0;var c2=toPython([{id:1}],'Root');var d2=c2.indexOf('class RootItem(');var a2=(d2>=0&&d2<c2.indexOf('Root = List[RootItem]'))?1:0;document.getElementById('__tbProbe').textContent='PYARR nested='+a1+' rootArr='+a2+' ref='+(c1.indexOf('List[RootOrders]')>=0?1:0);"
    ],
    "expect": [
      "PYARR nested=1 rootArr=1 ref=1"
    ],
    "ref": "复核失败重做·IT-N380 2/7（对象数组 + 根数组）：`{\"orders\":[{\"id\":1}]}` 的 `RootOrders` 与根数组 `[{\"id\":1}]` 的 `RootItem` 同样必须早于引用处定义。修复前两者分别报 `NameError: name RootOrders/RootItem is not defined`；修复后 `PYARR nested=1 rootArr=1 ref=1` ⇒ 强判别。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var o={class:1,type:'x'};var c=toPython(o,'Root');document.getElementById('__tbProbe').textContent='PYKW ok='+((c.indexOf('class_: int')>=0&&c.indexOf('class: int')<0)?1:0);"
    ],
    "expect": [
      "PYKW ok=1"
    ],
    "ref": "复核失败重做·IT-N382 3/7（Python 保留字）：`{\"class\":1,\"type\":\"x\"}` 不得生成 `class: int`（SyntaxError），应改名 `class_: int` 并由注释指回原键。修复前真实 python3 编译报 `SyntaxError: invalid syntax`；修复后 `PYKW ok=1` ⇒ 强判别。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var dq=String.fromCharCode(34);var o={type:'x'};var c=toRust(o,'Root');var want='serde(rename = '+dq+'type'+dq+')';document.getElementById('__tbProbe').textContent='RSKW ok='+((c.indexOf('pub type_: String')>=0&&c.indexOf('pub type:')<0)?1:0)+' ren='+(c.indexOf(want)>=0?1:0);"
    ],
    "expect": [
      "RSKW ok=1 ren=1"
    ],
    "ref": "复核失败重做·IT-N382 4/7（Rust 保留字）：`{\"type\":\"x\"}` 不得生成 `pub type: String`，应改名 `pub type_: String` 并补 `#[serde(rename = \"type\")]` 保留原键映射。修复前既无改名也无 rename；修复后 `RSKW ok=1 ren=1` ⇒ 强判别。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var dq=String.fromCharCode(34),bs=String.fromCharCode(92);var o={};o['a'+dq+'b']=1;var rs=toRust(o,'Root'),cs=toCSharp(o,'Root'),go=toGo(o,'Root');var rsWant='serde(rename = '+dq+'a'+bs+dq+'b'+dq+')';var csWant='JsonProperty('+dq+'a'+bs+dq+'b'+dq+')';document.getElementById('__tbProbe').textContent='MAPESC rs='+(rs.indexOf(rsWant)>=0?1:0)+' cs='+(cs.indexOf(csWant)>=0?1:0)+' go='+((go.indexOf('Go JSON tag 无法映射')>=0&&go.indexOf('type Root struct')<0)?1:0);"
    ],
    "expect": [
      "MAPESC rs=1 cs=1 go=1"
    ],
    "ref": "含双引号键：Rust 和 C# 必须转义；Go 的 encoding/json 不支持此 tag 名，必须明确提示并禁止生成误导性的 struct。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var o={class:1,type:'x'};var jv=toJava(o,'Root'),kt=toKotlin(o,'Root');var plain={aa:1};var pj=toJava(plain,'Root'),pk=toKotlin(plain,'Root'),pp=toPython(plain,'Root');document.getElementById('__tbProbe').textContent='KW4 jv='+(jv.indexOf('private Integer class_;')>=0?1:0)+' kt='+(kt.indexOf('val class_:')>=0?1:0)+' pj='+(pj.indexOf('private Integer aa;')>=0?1:0)+' pk='+(pk.indexOf('val aa:')>=0?1:0)+' pp='+(pp.indexOf('    aa: int')>=0?1:0);"
    ],
    "expect": [
      "KW4 jv=1 kt=1 pj=1 pk=1 pp=1"
    ],
    "ref": "复核失败重做·IT-N382 6/7（Java / Kotlin 保留字 + 普通键护栏）：`{\"class\":1,\"type\":\"x\"}` 应改成 `private Integer class_;` 与 `val class_:`；同时普通键 `aa` 在 Java / Kotlin / Python 三种生成器中仍保持原名，证明保留字规避没有误伤。修复前 `jv=0 kt=0` 但护栏三项已是 1；修复后 `KW4 jv=1 kt=1 pj=1 pk=1 pp=1` ⇒ 强判别。真实 javac：新版 `exit=0`，旧版 `exit=1`（`private Integer class;` 报「需要<标识符>」）。"
  },
  {
    "slug": "it/json-to-code",
    "clicks": [
      "var dq=String.fromCharCode(34),bt=String.fromCharCode(96);var o={};o['a'+bt+'b']=1;var go=toGo(o,'Root');document.getElementById('__tbProbe').textContent='GOBT ok='+((go.indexOf('Go JSON tag 无法映射')>=0&&go.indexOf('type Root struct')<0)?1:0);"
    ],
    "expect": [
      "GOBT ok=1"
    ],
    "ref": "含反引号键也不属于 encoding/json 支持的 tag 名，应提示限制并停止生成 struct，避免语法合法但映射错误。"
  },
  {
    slug: "it/json-to-code",
    clicks: ["var k='a'+String.fromCharCode(0,8,12,31)+'b',o={};o[k]=1;var rs=toRust(o,'Root'),cs=toCSharp(o,'Root'),go=toGo(o,'Root'),py=toPython(o,'Root'),bs=String.fromCharCode(92);var r='a'+bs+'u{0000}'+bs+'u{0008}'+bs+'u{000c}'+bs+'u{001f}b',s='a'+bs+'u0000'+bs+'u0008'+bs+'u000c'+bs+'u001fb';document.getElementById('__tbProbe').textContent='CTL rust='+(rs.indexOf(r)>=0?1:0)+' cs='+(cs.indexOf(s)>=0?1:0)+' go='+(go.indexOf('Go JSON tag 无法映射')>=0&&go.indexOf('type Root struct')<0?1:0)+' py='+(py.indexOf(String.fromCharCode(0))<0?1:0);"],
    expect: ["CTL rust=1 cs=1 go=1 py=1"],
    ref: "JSON 键中的控制字符需在 Rust/C# 字面量中转义、不得出现在 Python 注释中；Go 必须提示 tag 无法映射。"
  },
  {
    "slug": "it/json-schema-generator",
    "inputs": {
      "input": "1\n2\n3",
      "schemaVersion": "draft-06",
      "indent": "4"
    },
    "expect": [
      "符\ndraft-06\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"schemaVersion\":\"draft-06\",\"indent\":\"4\"}，输出区含「符\ndraft-06\n4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/json-schema-generator",
    "inputs": { "input": "{\"__proto__\":\"x\"}" },
    "clicks": ["generateSchema()"],
    "expect": ["\"__proto__\": {"],
    "ref": "属性名 `__proto__`：修复前 schema.properties 是普通 `{}`，`properties['__proto__']=propSchema` 走原型 setter，生成结果丢属性；Object.create(null) 后写入自有键，schema 输出含 `\"__proto__\": {`。输入 JSON 是紧凑形态（冒号后无空格与左花括号），不含本锚。"
  },
  {
    "slug": "it/json-to-csv",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n解析失败：Unexpected non-whitespace character after JSON at position 2 (line 2 column 1)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n解析失败：Unexpected non-whitespace cha…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/json-to-toml",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "com\" } }\n4\n✅ 转换成功",
      "} }\n4\ntitle = "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「com\" } }\n4\n✅ 转换成功」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/json-to-yaml",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "se } ] }\n4\n✅ 转换成功",
      "} ] }\n4\n--- app"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「se } ] }\n4\n✅ 转换成功」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/json-to-tsv",
    "inputs": {
      "jsonInput": "1\n2\n3",
      "tsvOutput": "1\n2\n3",
      "tsvInput": "1\n2\n3",
      "jsonOutput": "1\n2\n3",
      "j2tHeader": "false",
      "j2tNull": "null",
      "j2tNewline": "br",
      "t2jHeader": "false",
      "t2jFormat": "compact",
      "t2jIndent": "4"
    },
    "expect": [
      " 杭州 85.2\n[{\"col1\":\"name\",\"col2\":\"age\",\"col3\":\"city\",\"col4\":\"score\"},{\"col1\":\"张三\",\"col2\":\"25\",\"col3\":\"北京\",\"col4\":\"95.5\"},"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"jsonInput\":\"1\\n2\\n3\",\"tsvOutput\":\"1\\n2\\n3\",\"tsvInput\":\"1\\n2\\n3\",\"jsonOutput\":\"1\\n2\\n3\",\"j2tHeader\":\"false\",\"j2tNull\":\"null\",\"j2tNewline\":\"br\",\"t2jHeader\":\"false\",\"t2jFormat\":\"compact\",\"t2jIndent\":\"4\"}，输出区含「 杭州 85.2\n[{\"col1\":\"name\",\"col2\":\"age\",\"c…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/jwt-debugger",
    "inputs": {
      "secret": "abc123测试",
      "token-input": "1\n2\n3",
      "gen-payload": "1\n2\n3",
      "gen-output": "1\n2\n3",
      "alg": "HS384"
    },
    "expect": [
      "1 2 3\n1 2 3\nHS384"
    ],
    "ref": "自动补强（B类零用例）：注入{\"token-input\":\"1\\n2\\n3\",\"gen-payload\":\"1\\n2\\n3\",\"gen-output\":\"1\\n2\\n3\",\"alg\":\"HS384\"}等，输出区含「1 2 3\\n1 2 3\\nHS384」。⚠ 原 expect 前缀「6:40 PM)」来自过期时间的 toLocaleString() 时区格式化：本地 GMT+8 输出「3:0|6:40 PM)|」恰含该子串而通过，CI(UTC) 输出「7:06:40 AM)」则不含 ⇒ 本地绿、CI 红。已移除与时区相关的前缀，锚点落到完全由注入决定的 gen-payload/gen-output/alg（默认 alg=HS256，HS384 不出现在默认态 ⇒ 强判别、零逃生）。"
  },
  {
    "slug": "it/keyword-density",
    "inputs": {
      "minLen": "42",
      "inputText": "1\n2\n3",
      "tokenMode": "space"
    },
    "expect": [
      "SEO成功的基石。\nspace"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"minLen\":\"42\",\"inputText\":\"1\\n2\\n3\",\"tokenMode\":\"space\"}，输出区含「SEO成功的基石。\nspace」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/keyword-extractor",
    "inputs": {
      "inputText": "1\n2\n3",
      "topN": "10",
      "minLen": "2"
    },
    "expect": [
      "1 2 3\n10\n2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputText\":\"1\\n2\\n3\",\"topN\":\"10\",\"minLen\":\"2\"}，输出区含「1 2 3\n10\n2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/jwt-parser",
    "inputs": {
      "secret": "abc123测试",
      "genSecret": "abc123测试",
      "jwtInput": "1\n2\n3",
      "genPayload": "1\n2\n3",
      "genOut": "1\n2\n3",
      "verifyAlg": "HS384",
      "genAlg": "HS384",
      "genExp": "86400"
    },
    "expect": [
      "❌ Payload 不是合法 JSON：Unexpected non-whitespace character after JSON at position 2 (line 2 column 1)\n❌ 格式错误：JWT 应包含 3 部分（h"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"secret\":\"abc123测试\",\"genSecret\":\"abc123测试\",\"jwtInput\":\"1\\n2\\n3\",\"genPayload\":\"1\\n2\\n3\",\"genOut\":\"1\\n2\\n3\",\"verifyAlg\":\"HS384\",\"genAlg\":\"HS384\",\"genExp\":\"86400\"}，输出区含「❌ Payload 不是合法 JSON：Unexpected non-white…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\nInput: abc123测试 ❌ 未找到匹配的语言 支持：ISO 639-1 两字母代码（如 zh、en、fr）或中英文名"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\nInput: abc123测试 ❌ 未找到匹配的语言 支持：I…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "zh-CN"
    },
    "expect": [
      "Input: zh-CN BCP 47 解析： 语言 zh / 地区 CN ISO 639-1： zh ISO 639-3： zho"
    ],
    "ref": "IT-N424：修复前 key='zh-cn' 查表失败、名称/iso3 三条件均不成立 ⇒ 「❌ 未找到匹配的语言」；现拆 BCP 47 取语言段 zh 命中，并回显解析出的地区。默认态 en 不含该串。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "en-US"
    },
    "expect": [
      "Input: en-US BCP 47 解析： 语言 en / 地区 US ISO 639-1： en ISO 639-3： eng"
    ],
    "ref": "IT-N424：清单点名的 en-US。expect 绑定「原始标签 + 解析段 + 639-1/639-3」，默认态仅 en 无地区段 ⇒ 不逃生。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "pt-BR"
    },
    "expect": [
      "Input: pt-BR BCP 47 解析： 语言 pt / 地区 BR ISO 639-1： pt ISO 639-3： por"
    ],
    "ref": "IT-N424：清单点名的 pt-BR；同时验证 ISO 639-3 映射 por 非机械补字母。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "zh_Hans_CN"
    },
    "expect": [
      "Input: zh_Hans_CN BCP 47 解析： 语言 zh / 书写脚本 Hans / 地区 CN"
    ],
    "ref": "IT-N424：下划线分隔 + language-Script-REGION 三段式，脚本段按 4 字母识别、地区按 2 字母识别。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "zh-Hant-TW"
    },
    "expect": [
      "Input: zh-Hant-TW BCP 47 解析： 语言 zh / 书写脚本 Hant / 地区 TW"
    ],
    "ref": "IT-N424：繁体脚本 Hant 与地区 TW 同时解析；与 zh_Hans_CN 形成脚本/分隔符双向对照。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "ZH-cn"
    },
    "expect": [
      "Input: ZH-cn BCP 47 解析： 语言 zh / 地区 CN ISO 639-1： zh"
    ],
    "ref": "IT-N424：大小写混写标签规范化（语言段小写、地区段大写），修复前原样 toLowerCase 得 'zh-cn' 仍查不到。expect 含大写原始输入，默认态不含。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "zho"
    },
    "expect": [
      "Input: zho ISO 639-1： zh ISO 639-3： zho"
    ],
    "ref": "回归护栏（修复前后同绿）：ISO 639-3 三字母码反查主路径未被标签拆分改造破坏。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "中文"
    },
    "expect": [
      "Input: 中文 ISO 639-1： zh ISO 639-3： zho"
    ],
    "ref": "回归护栏（修复前后同绿）：中文名子串匹配仍可用。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "qq"
    },
    "expect": [
      "Input: qq ❌ 未找到匹配的语言 支持：ISO 639-1 两字母代码（如 zh、en、fr）或中英文名"
    ],
    "ref": "回归护栏（修复前后同绿）：无匹配时的错误文案与提示语保持逐字不变（既有自动补强用例同文案）。"
  },
  {
    "slug": "it/language-code-lookup",
    "inputs": {
      "input": "fr"
    },
    "expect": [
      "Input: fr ISO 639-1： fr ISO 639-3： fra 语言名称： French（法语）"
    ],
    "ref": "回归护栏（修复前后同绿）：常规两字母码精确匹配与单命中详情输出保持不变。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __r=[];[[String.fromCharCode(9),'Tab',9,'DIV'],[' ','Space',32,'DIV'],['ArrowDown','ArrowDown',40,'DIV'],['F12','F12',123,'DIV'],['a','KeyA',65,'BUTTON']].forEach(function(t){var __n=0;__kcOnKeyDown({key:t[0],code:t[1],keyCode:t[2],which:t[2],ctrlKey:false,shiftKey:false,altKey:false,metaKey:false,target:{tagName:t[3]},preventDefault:function(){__n++;}});__r.push(__n);});document.getElementById('result').textContent='KC425 prevent='+__r.join('/');"
    ],
    "expect": [
      "KC425 prevent=0/0/0/0/0"
    ],
    "ref": "IT-N425：五种按键（Tab/空格/方向键/F12/按钮目标）逐一统计 preventDefault 调用次数。修复前 DIV 目标为 1、BUTTON 为 0 ⇒ 1/1/1/1/0；现全部 0。修复前 handler 匿名注册且 harness 不派发 keydown，探针经顶层 __kcOnKeyDown 驱动。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __n=0;__kcOnKeyDown({key:String.fromCharCode(9),code:'Tab',keyCode:9,which:9,ctrlKey:false,shiftKey:false,altKey:false,metaKey:false,target:{tagName:'DIV'},preventDefault:function(){__n++;}});document.getElementById('result').textContent='KC425_TAB show='+document.getElementById('keyOut').textContent+'|'+document.getElementById('codeOut').textContent+'|'+document.getElementById('kcOut').textContent+' prevented='+__n;"
    ],
    "expect": [
      "KC425_TAB show=Tab|Tab|9 prevented=0"
    ],
    "ref": "IT-N425：Tab 默认行为不再被吞（Tab 焦点切换保持可用），同时 keyOut/codeOut/kcOut 三项展示逻辑逐字不变。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __n=0;__kcOnKeyDown({key:' ',code:'Space',keyCode:32,which:32,ctrlKey:true,shiftKey:true,altKey:false,metaKey:false,target:{tagName:'DIV'},preventDefault:function(){__n++;}});document.getElementById('result').textContent='KC425_SPACE show='+document.getElementById('keyOut').textContent+' mods='+document.getElementById('modOut').textContent+' prevented='+__n;"
    ],
    "expect": [
      "KC425_SPACE show=Space mods=Ctrl + Shift prevented=0"
    ],
    "ref": "IT-N425：空格键不再被吞（页面滚动保持可用）；Ctrl+Shift 修饰键收集顺序与连接符不变。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __n=0;__kcOnKeyDown({key:'F12',code:'F12',keyCode:123,which:123,ctrlKey:false,shiftKey:false,altKey:false,metaKey:false,target:{tagName:'BODY'},preventDefault:function(){__n++;}});document.getElementById('result').textContent='KC425_F12 key='+document.getElementById('keyOut').textContent+' prevented='+__n;"
    ],
    "expect": [
      "KC425_F12 key=F12 prevented=0"
    ],
    "ref": "IT-N425：清单点名的 F12 空分支（注释写「允许默认」实则仍 preventDefault）已删除，浏览器快捷键真正放行；展示值仍为 F12。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __n=0;__kcOnKeyDown({key:'a',code:'KeyA',keyCode:65,which:65,ctrlKey:false,shiftKey:false,altKey:false,metaKey:false,target:{tagName:'BUTTON'},preventDefault:function(){__n++;}});document.getElementById('result').textContent='KC425_BUTTON prevented='+__n;"
    ],
    "expect": [
      "KC425_BUTTON prevented=0"
    ],
    "ref": "IT-N425 回归护栏：事件来源为按钮时修复前后都不拦截；统一为「一律不拦截」后该分支被删除，行为保持等价。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __n=0;__kcOnKeyDown({key:'a',code:'KeyA',keyCode:65,which:65,ctrlKey:false,shiftKey:false,altKey:false,metaKey:false,target:{tagName:'DIV'},preventDefault:function(){__n++;}});document.getElementById('result').textContent='KC425_ZH mods='+document.getElementById('modOut').textContent+' prevented='+__n;"
    ],
    "expect": [
      "KC425_ZH mods=无 prevented=0"
    ],
    "ref": "IT-N425 回归护栏：中文态无修饰键时 modOut 仍显示「无」（helper 接入未改中文态文案），DIV 目标从拦截改为放行。"
  },
  {
    "slug": "it/keycode-info",
    "clicks": [
      "var __tb=window.TBKit;window.TBKit={util:{isEn:function(){return true;}}};__kcOnKeyDown({key:'a',code:'KeyA',keyCode:65,which:65,ctrlKey:false,shiftKey:false,altKey:false,metaKey:false,target:{tagName:'DIV'},preventDefault:function(){}});var __h=String(document.getElementById('result').innerHTML);document.getElementById('result').textContent='KC425_EN captured='+(__h.indexOf('Captured')>=0?1:0);window.TBKit=__tb;"
    ],
    "expect": [
      "KC425_EN captured=1"
    ],
    "ref": "IT-N425 顺带修：动态结果串「捕获到 keydown 事件」原为硬中文，英文态残留；现经 __kcL 输出 Captured keydown event。探针临时 mock TBKit.util.isEn=true 后校验。"
  },
  {
    "slug": "it/random-port-generator",
    "clicks": [
      "document.getElementById('skip').checked=false;document.getElementById('count').value='7';gen();"
    ],
    "expect": [
      "已生成 7 个随机端口（1024-65535，不保证端口未被占用）"
    ],
    "ref": "IT-N426：清单要求文案统一为「1024–65535，不保证未被占用」。修复前结果串止于「（1024-65535）」；现补「，不保证端口未被占用」。expect 绑 count=7 派生数量，默认态 count=5 不含该串；显式关掉 skip 消除 checkbox 默认态歧义。blob 直接采集 #result 的 innerHTML 文本，无需探针拼接。"
  },
  {
    "slug": "it/random-port-generator",
    "clicks": [
      "document.getElementById('count').value='20';gen();var __ok=ports.length===20&&ports.every(function(p){return p>=1024&&p<=65535;});document.getElementById('result').textContent='N426 range=ok'+__ok+' n='+ports.length;"
    ],
    "expect": [
      "N426 range=oktrue n=20"
    ],
    "ref": "IT-N426 回归护栏：实现仍是 1024–65535（本批只统一文案、不改取值范围），20 个端口全部落在区间内且数量正确。修复前后同绿。"
  },
  {
    "slug": "it/random-port-generator",
    "clicks": [
      "document.getElementById('count').value='20';gen();var __u={};ports.forEach(function(p){__u[p]=1;});document.getElementById('result').textContent='N426 uniq='+Object.keys(__u).length+'/'+ports.length;"
    ],
    "expect": [
      "N426 uniq=20/20"
    ],
    "ref": "IT-N426 回归护栏：20 个端口去重逻辑仍有效（清单明确「端口取值与去重逻辑本身正确」），本批不得误伤。修复前后同绿。"
  },
  {
    "slug": "it/random-port-generator",
    "clicks": [
      "document.getElementById('skip').checked=true;document.getElementById('count').value='10';gen();"
    ],
    "expect": [
      "已生成 10 个随机端口（1024-65535，已避开常用保留端口，不保证端口未被占用）"
    ],
    "ref": "IT-N426：开启「避开常用保留端口」时结果串仍标注该状态，且同样带免责声明，验证 skip 分支拼接未因双语化改造错位。修复前无免责声明 ⇒ 变红。"
  },
  {
    "slug": "it/slug-generator-advanced",
    "inputs": {
      "text": "café",
      "sep": "-"
    },
    "clicks": [
      "generate()"
    ],
    "expect": [
      "cafe ← café"
    ],
    "ref": "IT-N473：formula-list 承诺「去除变音符号（如 é→e）」，修复前 é 被 [^a-zA-Z0-9-] 整字符删除 ⇒ 产物 caf。现先 NFD 分解再去组合标记 ⇒ cafe。expect 用「产物 ← 原文」整段绑定输入，默认样例 Hello World 不含该串。"
  },
  {
    "slug": "it/slug-generator-advanced",
    "inputs": {
      "text": "naïve résumé",
      "sep": "-"
    },
    "clicks": [
      "generate()"
    ],
    "expect": [
      "naive-resume ← naïve résumé"
    ],
    "ref": "IT-N473：清单点名的 naïve résumé，修复前产物 nave-rsum（ï/é 被删）；现两个重音字母均还原、空格仍按 sep 转连字符。"
  },
  {
    "slug": "it/slug-generator-advanced",
    "inputs": {
      "text": "ÉCOLE",
      "sep": "-"
    },
    "clicks": [
      "generate()"
    ],
    "expect": [
      "ECOLE ← ÉCOLE"
    ],
    "ref": "IT-N473：大写重音 É 同样还原为 E（NFD 在大小写转换之前执行），验证不是只对小写 é 打补丁。"
  },
  {
    "slug": "it/slug-generator-advanced",
    "inputs": {
      "text": "Hello World 2024",
      "sep": "_"
    },
    "clicks": [
      "generate()"
    ],
    "expect": [
      "Hello_World_2024 ← Hello World 2024"
    ],
    "ref": "IT-N473 回归护栏：不含变音符号的常规输入、下划线分隔符路径前后同绿，确认 NFD 预处理未改写到普通 ASCII / 大小写 / sep 逻辑。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "7%3"
    },
    "clicks": [
      "document.getElementById('expr').value='7%3';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('result').textContent='N474 mod73='+(__h.indexOf('>1<')>=0?1:0);"
    ],
    "expect": [
      "N474 mod73=1"
    ],
    "ref": "IT-N474：清单点名 7%3。修复前 replace(/(\\d+)\\s*%/g,'($1/100)') 得 (7/100)3 ⇒ SyntaxError；现 % 后跟数字判为取模，保留 JS % 求值得 1。默认表达式结果 1030 以「结果： 1」开头，故用探针读 innerHTML 判 >1< 并写独立串，避开 token 前缀逃生。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "10 % 3"
    },
    "clicks": [
      "document.getElementById('expr').value='10 % 3';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('result').textContent='N474 mod103='+(__h.indexOf('>1<')>=0?1:0);"
    ],
    "expect": [
      "N474 mod103=1"
    ],
    "ref": "IT-N474：带空格的 10 % 3 同样是取模（负 lookahead 允许 % 后有空白再接操作数），修复前得 (10/100) 3 语法错。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "17%5"
    },
    "clicks": [
      "calc()"
    ],
    "expect": [
      "结果： 2"
    ],
    "ref": "IT-N474：17 mod 5 = 2，结果不以 1 开头可直接断言，验证真实数值而非仅「不报错」。修复前 (17/100)5 语法错。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "15%"
    },
    "clicks": [
      "calc()"
    ],
    "expect": [
      "结果： 0.15"
    ],
    "ref": "IT-N474 回归护栏：% 后无操作数仍按百分比 → (15/100)=0.15，修复前后同绿，百分比路径不得被取模改造误伤。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "50%*120"
    },
    "clicks": [
      "calc()"
    ],
    "expect": [
      "结果： 60"
    ],
    "ref": "IT-N474 回归护栏：50%*120 = 0.5×120 = 60，% 后接运算符判为百分比，修复前后同绿。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "15.5%"
    },
    "clicks": [
      "calc()"
    ],
    "expect": [
      "结果： 0.155"
    ],
    "ref": "IT-N474 顺带修：原正则 (\\d+) 只吃整数部分，15.5% 会变 15.(5/100) 语法错；现 (\\d+(?:\\.\\d+)?) 支持小数百分比。修复前红。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "7%-3"
    },
    "clicks": [
      "document.getElementById('expr').value='7%-3';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('result').textContent='N474 signed1='+(__h.indexOf('>1<')>=0?1:0);"
    ],
    "expect": [
      "N474 signed1=1"
    ],
    "ref": "IT-N474 复核失败重做：带一元负号的右操作数。7%-3 应判取模（7 % -3 = 1）；修复前 % 后跟 - 被当作百分比得 (7/100)-3 = -2.93。现改用函数式判别：% 后紧跟数字/左括号/正负号则保留取模。注入失败态回到默认 1030（不含 >1<）⇒ 可判别。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "7%+3"
    },
    "clicks": [
      "document.getElementById('expr').value='7%+3';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('result').textContent='N474 signed2='+(__h.indexOf('>1<')>=0?1:0);"
    ],
    "expect": [
      "N474 signed2=1"
    ],
    "ref": "IT-N474 复核失败重做：7%+3 应判取模（7 % 3 = 1）；修复前得 (7/100)+3 = 3.07。与 signed1 共守「带符号右操作数」分支。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": ".5%"
    },
    "clicks": [
      "calc()"
    ],
    "expect": [
      "结果： 0.005"
    ],
    "ref": "IT-N474 复核失败重做：纯小数百分比 .5% 应得 0.005；修复前正则 (\\d+(?:\\.\\d+)?) 要求整数部分，.5 不匹配 ⇒ 保留 % 致语法错。现加 (\\.\\d+) 分支支持省略整数。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": [
      "document.getElementById('expr').value='1+1';__meReuse('2^10 + sqrt(144)');var __e=document.getElementById('expr').value;var __r=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='N475 reuse='+__e+'|hit='+(__r.indexOf('1036')>=0?1:0);"
    ],
    "expect": [
      "N475 reuse=2^10 + sqrt(144)|hit=1"
    ],
    "ref": "IT-N475：历史「复用」链路契约。__meReuse 先把表达式原样回填 #expr 再 calc() 重算，2^10 + sqrt(144)=1036（默认表达式结果为 1030，不含该串）。修复前页面无 __meReuse（复用靠被双引号截断的内联 onclick），调用即抛错、探针不落 ⇒ 红。expect 绑输入派生表达式与重算命中位，非静态串。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": [
      "__meReuse('7%3');var __r=String(document.getElementById('result').innerHTML);document.getElementById('result').innerHTML='N475 mod='+(__r.indexOf('>1<')>=0?1:0);"
    ],
    "expect": [
      "N475 mod=1"
    ],
    "ref": "IT-N475：复用后的表达式必须完整走当前 calc 求值链（含 IT-N474 的取模判别），7%3 → 1。修复前无 __meReuse；用 >1< 精确锚避免默认态结果 1030 的 token 前缀误命中。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": [
      "var __src=String(renderHist)+String(__meReuse);document.getElementById('result').innerHTML='N475 src='+((__src.indexOf('addEventListener')>=0&&__src.indexOf('dataset.expr')>=0&&__src.indexOf('onclick=')<0)?1:0);"
    ],
    "expect": [
      "N475 src=1"
    ],
    "ref": "IT-N475 决定性结构契约：renderHist 必须用 DOM 节点 + addEventListener 绑定复用按钮，并把表达式存进 dataset.expr；任何把 JSON.stringify 结果拼进内联 onclick 属性的旧写法都会被 onclick= 检出。修复前是 h.map 拼 innerHTML 且含 onclick= ⇒ 0 ⇒ 红。源码契约用 String(fn) 读取，避免 harness 长 clicks 内花括号解析陷阱。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": [
      "var __src=String(renderHist);document.getElementById('result').innerHTML='N475 i18n='+((__src.indexOf('Reuse')>=0&&__src.indexOf('__meL')>=0)?1:0);"
    ],
    "expect": [
      "N475 i18n=1"
    ],
    "ref": "IT-N475 顺带修：历史区按钮文本「复用」原为硬编码中文，英文态 ?lang=en-US 动态创建的按钮残留 CJK（jsdom 真机实测 textContent=复用）。现 renderHist 经 __meL 输出 Reuse。修复前 renderHist 既无 __meL 也无 Reuse ⇒ 0 ⇒ 红；真机中英两态复核另见移交档。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": ["document.getElementById('expr').value='eval(String.fromCharCode(50,42,51))';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('stats').textContent='N470 eval='+(__h.indexOf('表达式含非法字符')>=0?1:0);"],
    "expect": ["N470 eval=1"],
    "ref": "IT-N470 安全回归（已修未删补护栏）：eval(String.fromCharCode(50,42,51)) 在旧实现会经 new Function 执行返回 6；现 MATH_ALLOWED 标识符白名单拒绝 eval/String/fromCharCode。探针显式重置 #expr（本页 inputs 注入会被初始样例覆盖）后取 #result 的 innerHTML 判定拒绝串，修复前为「结果：6」⇒ 0 ⇒ 红。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": ["document.getElementById('expr').value='fetch(String.fromCharCode(47,47,120,46,99))';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('stats').textContent='N470 fetch='+(__h.indexOf('表达式含非法字符')>=0?1:0);"],
    "expect": ["N470 fetch=1"],
    "ref": "IT-N470：fetch(String.fromCharCode(47,47,120,46,99)) 旧实现会真的发起 fetch 外发数据；现白名单拒绝 fetch/fromCharCode。与 eval 用例分守两类全局能力（动态执行 / 网络）。纯 clicks、无花括号。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": ["document.getElementById('expr').value='document.title';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('stats').textContent='N470 doc='+(__h.indexOf('表达式含非法字符')>=0?1:0);"],
    "expect": ["N470 doc=1"],
    "ref": "IT-N470：document.title 旧实现可读全局 DOM 属性；现标识符白名单拒绝 document/title，成员访问检查亦拦截非数字小数点。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": ["document.getElementById('expr').value='sin(0).constructor';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('stats').textContent='N470 member='+(__h.indexOf('表达式含非法字符')>=0?1:0);"],
    "expect": ["N470 member=1"],
    "ref": "IT-N470：sin(0).constructor 是绕过「只放行数学函数」的典型原型链手法（sin 本身合法）；现成员访问检查把非数字字面量的 \".\" 一律拒绝。"
  },
  {
    "slug": "it/math-evaluator",
    "clicks": ["document.getElementById('expr').value='sqrt(144)+3';calc();var __h=String(document.getElementById('result').innerHTML);document.getElementById('stats').textContent='N470 ok='+(__h.indexOf('>15<')>=0?1:0);"],
    "expect": ["N470 ok=1"],
    "ref": "IT-N470 护栏：合法表达式 sqrt(144)+3 仍须正常算出 15（>15< 精确锚，避开默认结果 1030 的 token 前缀）。前 4 条注入用例在缺陷态变红，本条在修复前后同绿，证明拦截没有误伤正常计算。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "1",
      "a1": "0",
      "a2": "0",
      "b0": "-1",
      "b1": "1",
      "b2": "0"
    },
    "clicks": [
      "calculate()"
    ],
    "expect": [
      "θ = 135°"
    ],
    "ref": "IT-N471：清单点名的钝角。A=(1,0,0)、B=(−1,1,0) ⇒ A·B=−1、|A×B|=1 ⇒ atan2(1,−1)=135°。修复前 θ=asin(0.707)=45°，被镜像成锐角。默认 (1,2,3)×(4,5,6) 是 12.933°，注入失败态不含 135° ⇒ 可判别。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "1",
      "a1": "0",
      "a2": "0",
      "b0": "-1",
      "b1": "0",
      "b2": "0"
    },
    "clicks": [
      "calculate()"
    ],
    "expect": [
      "θ = 180°"
    ],
    "ref": "IT-N471：反向共线。A=(1,0,0)、B=(−1,0,0) ⇒ |A×B|=0 但 A·B=−1 ⇒ atan2(0,−1)=180°；修复前 asin(0)=0° 并提示「平行」，与 FAQ 自述的 0°/180° 矛盾。默认态 12.933° 不含 180° ⇒ 可判别。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "1",
      "a1": "0",
      "a2": "0",
      "b0": "0",
      "b1": "1",
      "b2": "0"
    },
    "clicks": [
      "calculate()"
    ],
    "expect": [
      "θ = 90°"
    ],
    "ref": "IT-N471 回归护栏：正交 A=(1,0,0)、B=(0,1,0) ⇒ 90°，asin 与 atan2 同值，修复前后同绿，确保改造未误伤直角。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "1e-7",
      "a1": "0",
      "a2": "0",
      "b0": "0",
      "b1": "1e-7",
      "b2": "0"
    },
    "clicks": [
      "calculate()"
    ],
    "expect": [
      "θ = 90°"
    ],
    "ref": "IT-N471 复核失败重做：小尺度正交向量。A=(1e-7,0,0)、B=(0,1e-7,0) 量级 1e-7、叉积 1e-14，固定 1e-12 绝对阈值会误判为 0 且不显示角度；现改用相对阈值 sinθ=|A×B|/(|A||B|) 与 1e-9 比较，角度正常显示 90° 且不误判平行。默认 (1,2,3)×(4,5,6)=12.933° 不含 90° ⇒ 可判别。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "1e-7",
      "a1": "0",
      "a2": "0",
      "b0": "-1e-7",
      "b1": "0",
      "b2": "0"
    },
    "clicks": [
      "calculate()"
    ],
    "expect": [
      "θ = 180°"
    ],
    "ref": "IT-N471 复核失败重做：小尺度反向共线。A=(1e-7,0,0)、B=(-1e-7,0,0) 叉积 0、A·B=-1e-14 ⇒ atan2(0,-1e-14)=180°；固定阈值旧实现会丢失角度。相对阈值下 180° 正常显示。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "1",
      "a1": "1",
      "a2": "0",
      "b0": "1",
      "b1": "0",
      "b2": "0"
    },
    "clicks": [
      "calculate()"
    ],
    "expect": [
      "θ = 45°"
    ],
    "ref": "IT-N471 回归护栏：锐角 A=(1,1,0)、B=(1,0,0) ⇒ 45°，修复前后同绿。注意此串恰等于「135° 用例在修复前」的输出，但判别器按实例构造注入失败态（回到默认 12.933°），故本例自身仍具判别力。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "0",
      "a1": "0",
      "a2": "0",
      "b0": "1",
      "b1": "0",
      "b2": "0"
    },
    "clicks": [
      "var __h='';calculate();__h=String(document.getElementById('output').innerHTML);document.getElementById('output').innerHTML='N471 zero='+(__h.indexOf('θ = ')>=0?1:0);"
    ],
    "expect": [
      "N471 zero=0"
    ],
    "ref": "IT-N471 回归护栏：零向量时 |A||B|=0，不得输出角度行（atan2(0,0) 会给 0° 的假结论）。探针读 #output.innerHTML 判断是否存在 θ = 并写独立串；注入失败回到默认非平行输入时会有角度行 ⇒ zero=1 ⇒ 变红，故非逃生项。"
  },
  {
    "slug": "it/git-commands",
    "clicks": [
      "renderCommands();var __h=String(document.getElementById('cmdList').innerHTML);document.getElementById('stats').textContent='N479 noinline='+((__h.indexOf('onclick=')<0&&__h.indexOf('data-idx=')>=0)?1:0);"
    ],
    "expect": [
      "N479 noinline=1"
    ],
    "ref": "IT-N479 决定性结构契约：renderCommands 产出的 58 个按钮不得再带内联 onclick 属性，必须改用 data-idx。修复前模板把含真实换行的示例拼进 onclick=\"copyCode(this, '…')\"，58/58 编译抛 SyntaxError；快照态不执行 clicks，#stats 保持「共 58 个命令」⇒ 不含 N479 探针串，可判别。"
  },
  {
    "slug": "it/git-commands",
    "clicks": [
      "var __src=String(copyCodeByIdx)+String(copyCode);document.getElementById('stats').textContent='N479 src='+((__src.indexOf('c.example')>=0&&__src.indexOf('COMMANDS')>=0&&__src.indexOf('&quot;')<0)?1:0);"
    ],
    "expect": [
      "N479 src=1"
    ],
    "ref": "IT-N479：复制链路改为按 COMMANDS 原始下标取回 c.example 原文，copyCode 不再做 HTML 实体反转义（旧链路上 &quot;/&#39; 是属性转义产物）。String(copyCodeByIdx)+String(copyCode) 必须含 c.example/COMMANDS 且不含 &quot;。修复前无 copyCodeByIdx ⇒ 抛错 ⇒ 红。"
  },
  {
    "slug": "it/git-commands",
    "inputs": {
      "searchInput": "push"
    },
    "clicks": [
      "renderCommands();var __h=String(document.getElementById('cmdList').innerHTML);var __n=__h.split('data-idx=').length-1;document.getElementById('stats').textContent='N479 btns='+__n+' inline='+(__h.indexOf('onclick=')>=0?1:0);"
    ],
    "expect": [
      "N479 btns=4 inline=0"
    ],
    "ref": "IT-N479：注入 searchInput='push' 过滤后应恰好渲染 4 个带 data-idx 的按钮且无内联 onclick，验证事件委托按原 COMMANDS 索引取数、不因 filtered 子集错位。注入失败回到默认空搜索 ⇒ 58 个按钮 ⇒ 变红；修复前无 data-idx 且 inline=1 ⇒ 亦红。"
  },
  {
    "slug": "it/git-commands",
    "clicks": [
      "var __e=COMMANDS.filter(c=>c.cmd==='git switch')[0].example;document.getElementById('stats').textContent='N487 fix='+((__e.indexOf('git switch -c feature origin/feature')>=0&&__e.indexOf('git switch origin/feature')<0)?1:0);"
    ],
    "expect": [
      "N487 fix=1"
    ],
    "ref": "IT-N487：清单点名的致命用法。`git switch origin/feature` 不是合法命令（switch 只接受本地分支名，实测 fatal: a branch is expected, got remote branch）；现改为 `git switch -c feature origin/feature` 并彻底移除错误串。expect 绑示例内容而非静态标签，快照态不执行 clicks ⇒ 变红。"
  },
  {
    "slug": "it/git-commands",
    "clicks": [
      "var __e=COMMANDS.filter(c=>c.cmd==='git switch')[0].example;document.getElementById('stats').textContent='N487 full='+((__e.indexOf('git switch feature')>=0&&__e.indexOf('--detach origin/feature')>=0)?1:0);"
    ],
    "expect": [
      "N487 full=1"
    ],
    "ref": "IT-N487：除创建跟踪分支外，补齐清单方案提到的「本地已有跟踪分支时直接切换 git switch feature」与「只看远程提交用 --detach origin/feature」两条口径，避免用户把所有场景都写成 -c。修复前两串均无 ⇒ 红。"
  },
  {
    "slug": "it/git-commands",
    "clicks": [
      "renderCommands();var __h=String(document.getElementById('cmdList').innerHTML);document.getElementById('stats').textContent='N487 render='+((__h.indexOf('git switch main')>=0&&__h.indexOf('data-idx=')>=0)?1:0);"
    ],
    "expect": [
      "N487 render=1"
    ],
    "ref": "IT-N487 回归护栏：改示例文本不得破坏 renderCommands 渲染与 IT-N479 的 data-idx 结构（含换行/中文注释的多行示例仍能安全进入 innerHTML）。修复前后同绿；快照态不执行 clicks ⇒ 变红，非逃生项。"
  },
  {
    "slug": "it/kubernetes-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 示例 事件\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 示例 事件\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/line-ending-converter",
    "inputs": {
      "leInput": "1\n2\n3",
      "leOutput": "1\n2\n3",
      "targetSel": "&#10;"
    },
    "expect": [
      "1 2 3\n&#10;\n1&#10;2&#10;3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"leInput\":\"1\\n2\\n3\",\"leOutput\":\"1\\n2\\n3\",\"targetSel\":\"&#10;\"}，输出区含「1 2 3\n&#10;\n1&#10;2&#10;3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/list-converter",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "quote"
    },
    "expect": [
      "1 2 3\nquote\n✅ 已转换 3 个项目\n\"1\", \"2\", \"3\""
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"quote\"}，输出区含「1 2 3\nquote\n✅ 已转换 3 个项目\n\"1\", \"2\", \"3\"」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\nInput: abc123测试 语言（ISO 639-1）： abc123测试 ❌ 不符合 BCP 47 格式（应为 language[-script][-region][-variant]，如 zh-Hans-CN、en"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\nInput: abc123测试 语言（ISO 639-1）： …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "de-DE-1996"
    },
    "expect": [
      "Input: de-DE-1996 语言（ISO 639-1）： de 国家（ISO 3166-1）： DE 完整名称： 德语（德国）"
    ],
    "ref": "IT-N421：RFC 5646 允许 4 位数字 variant（1996 为德语新正字法）。旧正则 variant 限 5–8 位 ⇒ 「❌ 不符合 BCP 47 格式」；现格式合法并回退命中 de-DE。expect 绑定输入派生串，默认 en-US 不命中。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "es-419"
    },
    "expect": [
      "Input: es-419 语言（ISO 639-1）： es 国家（ISO 3166-1）： 419 ✅ BCP 47 格式有效（数据库中无此条目）"
    ],
    "ref": "IT-N421：UN M.49 三位数字地区码 419（拉美）是合法 region。旧正则 region 只允许两位字母 ⇒ 误判非法。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "en-US-u-ca-gregory"
    },
    "expect": [
      "Input: en-US-u-ca-gregory 语言（ISO 639-1）： en 国家（ISO 3166-1）： US 完整名称： 英语（美国）"
    ],
    "ref": "IT-N421：BCP 47 扩展子标签（singleton u + ca/gregory）。旧正则完全不支持扩展 ⇒ 误判非法；现校验通过后回退命中 en-US。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "sl-rozaj-biske-1994"
    },
    "expect": [
      "Input: sl-rozaj-biske-1994 语言（ISO 639-1）： sl ✅ BCP 47 格式有效（数据库中无此条目）"
    ],
    "ref": "IT-N421：多个 variant 连写（含 4 位数字 1994）。顺带验证解析段不再把 variant 'rozaj' 误标成「国家（ISO 3166-1）：ROZAJ」。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "EN-US"
    },
    "expect": [
      "Input: EN-US 语言（ISO 639-1）： en 国家（ISO 3166-1）： US 完整名称： 英语（美国）"
    ],
    "ref": "IT-N422：旧查表 `LOCALES[raw]` 原样比对，大写 EN-US 只得到「✅ 格式有效（数据库中无此条目）」；现 canonical 化后命中 en-US。expect 含大写原始输入，默认态小写 en-US 不命中。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "en_us"
    },
    "expect": [
      "Input: en_us 语言（ISO 639-1）： en 国家（ISO 3166-1）： US 完整名称： 英语（美国）"
    ],
    "ref": "IT-N422：下划线分隔（Windows/Java 常见写法）统一规范化为 - 后命中 en-US。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "zh-Hans-CN"
    },
    "expect": [
      "书写脚本： Hans 国家（ISO 3166-1）： CN 完整名称： 简体中文（中国大陆） 语言： 中文 国家/地区： 中国 书写系统： Hans 排序方式： 拼音 规范化标签： zh-Hans-CN 匹配键： zh-CN"
    ],
    "ref": "IT-N422：deep-dive FAQ 的规范示例 zh-Hans-CN 旧版只报「无此条目」。现按「language+region 且 script 一致」回退到 zh-CN，给出完整信息；规范化标签与匹配键均回显。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "zh-Hant-CN"
    },
    "expect": [
      "完整名称： 繁体中文（语言） 语言： 中文 国家/地区： - 书写系统： Hant 规范化标签： zh-Hant-CN 匹配键： zh-Hant"
    ],
    "ref": "IT-N422 回退正确性：script 为 Hant 时**不得**回退到简体的 zh-CN，须截尾回退到 zh-Hant。这是「script 一致性」校验的关键反例。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "en-Latn-US"
    },
    "expect": [
      "书写脚本： Latn 国家（ISO 3166-1）： US 完整名称： 英语（美国）"
    ],
    "ref": "IT-N422：显式 script 与命中项 script 一致时允许 language+region 回退（en-Latn-US → en-US）。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "123"
    },
    "expect": [
      "Input: 123 语言（ISO 639-1）： 123 ❌ 不符合 BCP 47 格式"
    ],
    "ref": "回归护栏（修复前后同绿）：纯数字不是合法 language，收紧后的 RFC 5646 正则仍须拒绝；同时验证「非法标签不进入查表回退」的前置校验未把乱码放行。"
  },
  {
    "slug": "it/locale-lookup",
    "inputs": {
      "input": "pt-BR"
    },
    "expect": [
      "Input: pt-BR 语言（ISO 639-1）： pt 国家（ISO 3166-1）： BR 完整名称： 葡萄牙语（巴西）"
    ],
    "ref": "回归护栏（修复前后同绿）：常规 language-region 精确匹配未被规范化/回退改造破坏。"
  },
  {
    "slug": "it/location-qr",
    "inputs": {
      "lat": "abc123测试",
      "lng": "abc123测试",
      "label": "abc123测试"
    },
    "expect": [
      "⚠ 纬度 须为合法数字（不支持非法后缀）"
    ],
    "ref": "真实 QR 改造后经纬度做数值校验：注入 lat/lng=abc123测试，parseCoord 严格数字正则不匹配 ⇒ 输出「⚠ 纬度 须为合法数字（不支持非法后缀）」。默认样例（39.9/116.4）不出现该提示 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/linux-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 任务 帮助\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 任务 帮助\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/mac-generator",
    "inputs": {
      "cnt": "42",
      "oui": "00:1A:79"
    },
    "expect": [
      "的 MAC 地址（42 个） 00:1A:79:1B:6A:72 00:1A:79:B6:11:63 00:1A:79:C5:00:9D 00:1A:79:F0:1F:C8 00:1A:79:39:C9:D0 00:1A:79:24:FC:"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\",\"oui\":\"00:1A:79\"}，输出区含「的 MAC 地址（42 个） 00:1A:79:1B:6A:72 00:1A:7…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/lorem",
    "inputs": {
      "count": "42",
      "output": "1\n2\n3"
    },
    "expect": [
      "sectetur sed. Minim qui in duis dolore cillum non officia commodo amet nisi officia id ex duis velit nisi non elit. Amet"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\",\"output\":\"1\\n2\\n3\"}，输出区含「sectetur sed. Minim qui in duis dolore c…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/lorem",
    "inputs": {
      "count": "1",
      "minWords": "3",
      "maxWords": "3"
    },
    "clicks": ["document.getElementById('startLorem').checked=true;generate()"],
    "expect": [
      "Lorem ipsum dolor."
    ],
    "ref": "IT-N525 复核失败重做：句长最小/最大均 3、勾选「以 Lorem ipsum 开头」、默认段落模式，首句须服从句长约束为 3 词「Lorem ipsum dolor.」；旧实现强行塞入固定 8 词句。默认态不出现该串 ⇒ 强判别、零逃生。回退 N525 源码会令此用例转红。"
  },
  {
    "slug": "it/markdown-editor",
    "inputs": {
      "mdInput": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3\n5\n3\n3\n编辑中..."
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mdInput\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3\n5\n3\n3\n编辑中...」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/margin-of-error",
    "inputs": {
      "n": "42",
      "p": "42",
      "N": "42",
      "conf": "0.95"
    },
    "expect": [
      "p 必须在 0~1 之间\n42\n42\n0.95\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"p\":\"42\",\"N\":\"42\",\"conf\":\"0.95\"}，输出区含「42\n42\n42\n0.95\np 必须在 0~1 之间」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/markdown-lint",
    "inputs": {
      "src": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n检查结果 3 行数 0 问题 ✅ 未发现明显风格问题。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"src\":\"1\\n2\\n3\"}，输出区含「1 2 3\n检查结果 3 行数 0 问题 ✅ 未发现明显风格问题。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/markdown-to-html",
    "inputs": {
      "md": "1\n2\n3"
    },
    "expect": [
      "1 2 3 支持标题/粗斜体"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"md\":\"1\\n2\\n3\"}，结果区为 `<p>1</p><p>2</p><p>3</p>` + 底部说明，collectStrings 归一后含「1 2 3 支持标题/粗斜体」；默认态 md 是中文示例，结果区以中文开头、不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/math-evaluator",
    "inputs": {
      "expr": "2^10 + sqrt(144)"
    },
    "expect": [
      "1036"
    ],
    "ref": "注入非默认表达式（默认 2^10 + sqrt(144) * sin(pi/6) = 1030）：2^10 + sqrt(144) = 1024 + 12 = 1036，结果区唯一出现该值。原锚「fined\\n表达式含非法字符…」实为 hist 区把表达式与 undefined 拼接的静态串（任何输入都出现），故在注入失败时仍命中、成为逃生项；改数值锚后换回默认（1030）即失配。"
  },
  {
    "slug": "it/matrix-inverter",
    "inputs": {
      "size": "3"
    },
    "expect": [
      "3\n矩阵 A (3×3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"size\":\"3\"}，输出区含「3\n矩阵 A (3×3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/matrix-determinant",
    "inputs": {
      "size": "3"
    },
    "expect": [
      "\n|A| = 0 Sarrus 法则（复制前两列）： 主对角方向: (0×0×0) + (0×0×0) + (0×0×0) = 0 副对角方向: − (0×0×0) − (0×0×0) − (0×0×0) = − 0 |A|"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"size\":\"3\"}，输出区含「\n|A| = 0 Sarrus 法则（复制前两列）： 主对角方向: (0×0×0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/md5",
    "inputs": {
      "hmacKey": "abc123测试",
      "textInput": "1\n2\n3",
      "hmacInput": "1\n2\n3"
    },
    "expect": [
      "bfb77520994c313d1abff83000f19dc3",
      "13febef193a79e5e7bf4453985265338"
    ],
    "ref": "自动补强（B类零用例）改为单值锚：注入 textInput/hmacInput='1\\n2\\n3'、hmacKey='abc123测试' ⇒ 文本 MD5('1\\n2\\n3')=bfb77520994c313d1abff83000f19dc3、HMAC-MD5=13febef193a79e5e7bf4453985265338（可独立用 openssl/node 复算）。原断言把「输入值 + 两个哈希 + 表格顺序」拼成一整串，表格行顺序变化即误报（已改为只锚两个派生哈希，默认态 'Hello, MD5!' 输出不同，均不命中）。"
  },
  {
    "slug": "it/mime-type",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "程序 字体 其他\nabc123测试\n共 0 条"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「程序 字体 其他\nabc123测试\n共 0 条」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/mongodb-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 备份 类型\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 备份 类型\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/morse-decode-advanced",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "style": "audio"
    },
    "expect": [
      "理解 ...-.\n1 2 3\naudio\n???"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"style\":\"audio\"}，输出区含「理解 ...-.\n1 2 3\naudio\n???」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n❌ 仅允许数字及 +、空格、连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n❌ 仅允许数字及 +、空格、连字符」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+86 1"
    },
    "expect": [
      "❌ 国内号码长度非法：+86 需 11 位，当前 1 位"
    ],
    "ref": "IT-N415：修复前 cc=86 但国内号 1 位落无条件 else 输出「✅ MSISDN 格式有效」；现按 CC_LEN['86']=[11,11] 拒绝。默认 +86 13800138000 为 11 位合法，不命中该错误串 ⇒ 强判别。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+86 138001380000"
    },
    "expect": [
      "❌ 国内号码长度非法：+86 需 11 位，当前 12 位"
    ],
    "ref": "IT-N415：国内号 12 位同样被修复前 else 判有效；现按号长规则拒绝并回显实际 12 位。错误串含输入派生的位数，默认态不命中。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+86 1380013800012345"
    },
    "expect": [
      "❌ 超过 E.164 上限 15 位（当前 18 位）"
    ],
    "ref": "IT-N415 / ITU-T E.164：normalized=2+16=18 位超 15 位上限，修复前无任何总长校验。错误串由输入总长 18 派生，默认 13 位不命中。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+852 91234567"
    },
    "expect": [
      "国家/地区代码： +852 - 中国香港 国内号码： 91234567"
    ],
    "ref": "IT-N416：旧 CC_DB 42 条不含 852，3→1 位匹配失败直接报「无法识别国家代码」；现补入 852 并按 CC_LEN 8 位通过。中国香港属中国地区码，与 86 同主权口径。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+886 912345678"
    },
    "expect": [
      "国家/地区代码： +886 - 中国台湾 国内号码： 912345678"
    ],
    "ref": "IT-N416：补 886 中国台湾（9 位国内号），与 phone-parser 的 +886 支持口径一致。默认态为 +86，不命中。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+853 66123456"
    },
    "expect": [
      "国家/地区代码： +853 - 中国澳门 国内号码： 66123456"
    ],
    "ref": "IT-N416：补 853 中国澳门（8 位）。修复前同样报「无法识别国家代码」。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+880 1712345678"
    },
    "expect": [
      "国家/地区代码： +880 - 孟加拉国 国内号码： 1712345678"
    ],
    "ref": "IT-N416：补 3 位码 880；旧库 3 位码全空，前缀匹配退化到 '8'/'88' 均失败。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+966 551234567"
    },
    "expect": [
      "国家/地区代码： +966 - 沙特阿拉伯 国内号码： 551234567"
    ],
    "ref": "IT-N416：补 3 位码 966（9 位国内号），验证降序 3→2→1 匹配优先级未被 2 位码抢先。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+86 13800138001"
    },
    "expect": [
      "国内号码： 13800138001 E.164 格式： +8613800138001 号码长度： 11 位（允许 11–11 位） 运营商： 移动（号段 138，携号转网后可能变化）"
    ],
    "ref": "IT-N417：旧查表取 prefix4='1380' 的第 4 位 '0'，而 OP_DB['8613'] 只有 1–9 ⇒ 「未知（号段 1380）」；现按国内号前 3 位 138 查得移动。⚠️ 注入 ...001 与默认 ...000 同属 138 号段 ⇒ 只断言运营商串会在默认态命中（判别器实测逃生），故按 token 对齐把 expect 扩展为「国内号码 + E.164 + 号码长度 + 运营商」整段，绑定输入派生值。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+86 13312345678"
    },
    "expect": [
      "运营商： 电信（号段 133，携号转网后可能变化）"
    ],
    "ref": "IT-N417 深挖：旧表按第 4 位查 '1331'→OP_DB['8613']['1']='移动'，把 133 电信错报移动；现按 3 位号段 133 得电信。修复前输出「运营商： 移动」不含本串 ⇒ 强判别。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+1 9995550100"
    },
    "expect": [
      "❌ N99 是保留未分配区号"
    ],
    "ref": "IT-N427：旧 NANP 分支 10 个区号未命中仍追加「✅ NANP 号码 / ✅ MSISDN 有效」；现按 NANP 结构规则拒绝 N99 保留区号，且不再输出有效结论。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+1 2025550100"
    },
    "expect": [
      "区号： 202 - Washington, DC 号码类型："
    ],
    "ref": "IT-N427：AC_DB 由 10 条扩到 80+ 条，202 华盛顿特区从「未知城市」变为可识别；expect 同时绑定区号与后续号码类型，避免静态串逃生。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+1 9115550100"
    },
    "expect": [
      "❌ N11 是保留服务码，不能作区号"
    ],
    "ref": "IT-N427 / NANP：N11（211/311/…/911）为保留服务码不可作 NPA；修复前 10 位即判有效。"
  },
  {
    "slug": "it/msisdn-lookup",
    "inputs": {
      "input": "+65 81234567"
    },
    "expect": [
      "号码长度： 8 位（允许 8–8 位） 号码类型： ✅ 国际号码（按 E.164 长度校验）"
    ],
    "ref": "IT-N415 通用分支回归：非 86/1 的国家不再无条件放行，先按 CC_LEN 校验并回显长度规则；修复前无「号码长度」行。默认 +86 为 11 位，不命中 8 位串。"
  },
  {
    "slug": "it/morse",
    "inputs": {
      "speed": "42",
      "frequency": "42",
      "volume": "42",
      "input": "1\n2\n3",
      "dotRatio": "2"
    },
    "expect": [
      "DEFINED\n\n2\n42\n42\n42\n42\n42\n42%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"speed\":\"42\",\"frequency\":\"42\",\"volume\":\"42\",\"input\":\"1\\n2\\n3\",\"dotRatio\":\"2\"}，输出区含「DEFINED\n\n2\n42\n42\n42\n42\n42\n42%」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/mysql-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "UPSERT\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「UPSERT\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/matrix-transpose",
    "inputs": {
      "rows": "3",
      "cols": "2"
    },
    "expect": [
      "3\n2\n矩阵 A (3×2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rows\":\"3\",\"cols\":\"2\"}，输出区含「3\n2\n矩阵 A (3×2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/nato-alphabet",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "One Two Tree"
    ],
    "ref": "IT-N531 同批改写（铁律①）：数字按北约专用读法转换（1→One、2→Two、3→Tree），复制框为 One Two Tree；修复前数字原样透传为 1 2 3。默认输入 Hello World 得到 Hotel Echo…，不含该串 ⇒ 强判别、零逃生。原自动补强锚「1 2 3 / ✅ 已转换 3 个字母」随功能改动一并作废。"
  },
  {
    "slug": "it/nginx-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 变量 命令\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 变量 命令\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/normal-distribution",
    "inputs": {
      "mu": "42",
      "sigma": "42",
      "x0": "42",
      "a": "42",
      "b": "42",
      "pIn": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\nP(X ≤ 42) = 0.5 0 Z 分数 0.5",
      "查表 Φ(0) = 0.5\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mu\":\"42\",\"sigma\":\"42\",\"x0\":\"42\",\"a\":\"42\",\"b\":\"42\",\"pIn\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\nP(X ≤ 42) = 0.5 0 Z 分数…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/numeronym-generator",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n✅ 已转换 3 个单词\n7\n1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n✅ 已转换 3 个单词\n7\n1 2 3\n1 2 3」；IT-N286 新增 minLen=7 输入框，blob 多一行「7」。默认态（输入回退）为英文长词，不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/octal-encode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "sep": ""
    },
    "expect": [
      "1 2 3\n\u0001\u0002\u0003"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"sep\":\"\"}，输出区含「1 2 3\n\u0001\u0002\u0003」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/og-meta-tag-generator",
    "inputs": {
      "f_title": "abc123测试",
      "f_desc": "abc123测试",
      "f_img": "abc123测试",
      "f_url": "abc123测试",
      "f_site": "abc123测试",
      "f_locale": "abc123测试",
      "output": "1\n2\n3",
      "f_type": "article"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\nabc123测试\narticle\nabc123测试\nabc123测试\n<!-- Open Graph --> <meta property=\"og:title\" content=\"abc"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f_title\":\"abc123测试\",\"f_desc\":\"abc123测试\",\"f_img\":\"abc123测试\",\"f_url\":\"abc123测试\",\"f_site\":\"abc123测试\",\"f_locale\":\"abc123测试\",\"output\":\"1\\n2\\n3\",\"f_type\":\"article\"}，输出区含「abc123测试\nabc123测试\nabc123测试\nabc123测试\narti…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/number-base-converter",
    "inputs": {
      "inputValue": "abc123测试",
      "customBase": "42",
      "batchInput": "1\n2\n3",
      "batchOutput": "1\n2\n3",
      "inputBase": "8",
      "batchFrom": "2",
      "batchTo": "2"
    },
    "expect": [
      " 36进制 复制\n42\n1 2 3\n1 无效 无效\n2\n2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputValue\":\"abc123测试\",\"customBase\":\"42\",\"batchInput\":\"1\\n2\\n3\",\"batchOutput\":\"1\\n2\\n3\",\"inputBase\":\"8\",\"batchFrom\":\"2\",\"batchTo\":\"2\"}，输出区含「 36进制 复制\n42\n1 2 3\n1 无效 无效\n2\n2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/otp-generator",
    "inputs": {
      "secret": "abc123测试",
      "step": "42",
      "counter": "42",
      "digits": "8"
    },
    "expect": [
      "abc123测试\n42\n42\n8\n82374974 30 秒后刷新",
      "8\nabc123测试\n42\n42\n82374974 30 秒后刷新"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"secret\":\"abc123测试\",\"step\":\"42\",\"counter\":\"42\",\"digits\":\"8\"}，输出区含「abc123测试\n42\n42\n8\n82374974 30 秒后刷新」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/password-strength",
    "inputs": {
      "pwd": "abc123测试"
    },
    "expect": [
      "abc123测试\n✅ 长度>=8位 ⚠️ 建议至少12位 ❌ 应同时包含大小写字母 ✅ 包含数字 ✅ 包含特殊符号 ⚠️ 包含键盘连续序列（如123、abc、qwe） ❌ 包含常见弱密码片段\n一般"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pwd\":\"abc123测试\"}，输出区含「abc123测试\n✅ 长度>=8位 ⚠️ 建议至少12位 ❌ 应同时包含大小写字…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/phone-screen-sizes",
    "inputs": {
      "diag": "42",
      "resw": "42",
      "resh": "42"
    },
    "expect": [
      "参数反算 PPI 42.0 英寸 屏幕尺寸 42×42 分辨率 5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"diag\":\"42\",\"resw\":\"42\",\"resh\":\"42\"}，输出区含「参数反算 PPI 42.0 英寸 屏幕尺寸 42×42 分辨率 5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {
      "phone": "42",
      "cc": "1"
    },
    "expect": [
      "果 E.164 +142"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phone\":\"42\",\"cc\":\"1\"}，输出区含「果 E.164 +142」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "2025550123", "cc": "1"},
    "expect": ["国内格式：(202) 555-0123"],
    "ref": "IT-N413：美加 NANP 10 位必须是 (XXX) XXX-XXXX。修复前 grp() 从右每 4 位 ⇒ 20 2555 0123；输入与默认样例 13800138000 完全不同 ⇒ 默认态不命中。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "0794609584", "cc": "44"},
    "expect": ["国内格式：07946 09584"],
    "ref": "IT-N413：英国手机按 5-5 分组且国内格式保留 trunk 0（E.164 里剥掉的 0 要补回来显示）。修复前剥 0 后 grp('794609584') ⇒ 7 9460 9584。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "9876543210", "cc": "91"},
    "expect": ["国内格式：98765 43210"],
    "ref": "IT-N413：印度 10 位按 5-5。修复前从右每 4 位 ⇒ 98 7654 3210。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "09012345678", "cc": "81"},
    "expect": ["国内格式：090 1234 5678"],
    "ref": "IT-N413：日本手机按 3-4-4（含 trunk 0）。修复前剥 0 后 grp('9012345678') ⇒ 90 1234 5678。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "0912345678", "cc": "886"},
    "expect": ["国内格式：0912 345 678"],
    "ref": "IT-N413：中国台湾 9 位按 4-3-3（含 trunk 0）。修复前剥 0 后 grp('912345678') ⇒ 9 1234 5678。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "020 7946 0958", "cc": "44"},
    "expect": ["国内格式：020 7946 0958"],
    "ref": "IT-N413：英国固话（剥 trunk 0 后 10 位）按 020 7946 0958 的 3-4-4 显示，不能套用手机的 5-5；同时验证粘贴带空格的写法可清洗。修复前 grp('2079460958') ⇒ 20 7946 0958。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "139-0013-9000", "cc": "86"},
    "expect": ["E.164 +8613900139000", "国内格式：139 0013 9000"],
    "ref": "IT-N412 契约：输入可含连字符/空格等分隔符，清洗后仍得到标准 E.164 与分组。两条 expect 都依赖注入的 139 号段（默认样例是 13800138000 ⇒ 均不命中），无静态串。number 输入框的粘贴清空属浏览器 value sanitization，桩 DOM 不复刻，另由 jsdom 真机取证。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "8613900139000", "cc": "86"},
    "expect": ["E.164 +8613900139000"],
    "ref": "IT-N414 契约：纯数字输入已含所选国家码时自动剥离，不能拼成双国家码 +868613900139000。139 号段与默认 138 不同 ⇒ 默认态不命中。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "02079460958", "cc": "44"},
    "expect": ["E.164 +442079460958"],
    "ref": "IT-N414 契约：英国固话剥掉国内首位 0（trunk prefix）后再拼 E.164，得到 12 位的 +442079460958 而非 13 位带 0。默认态（中国 138 号）不含该串。"
  },
  {
    "slug": "it/phone-parser",
    "inputs": {"phone": "13800138000000000000", "cc": "86"},
    "expect": ["E.164 超过 15 位上限"],
    "ref": "IT-N414 契约：E.164 总长超 15 位时必须明确报错并禁止复制（页面把 __lastE164 置空）。注入 20 位数字，默认 11 位样例不会触发 ⇒ 判别明确。"
  },
  {
    "slug": "it/php-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "数据库 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「数据库 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/php-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "double"
    },
    "expect": [
      "1 2 3\n1 2 3\ndouble",
      "1 2 3\ndouble\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"double\"}，输出区含「1 2 3\n1 2 3\ndouble」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  
  {
    "slug": "it/playfair-cipher",
    "inputs": {
      "key": "abc123测试",
      "input": "HELLOWORLD"
    },
    "expect": [
      "KCNVMPYMQMCY"
    ],
    "ref": "独立复算（Python 手写 Playfair，key='ABC'、明文 'HELLOWORLD'）：去重字母表 A B C D E / F G H I K / L M N O P / Q R S T U / V W X Y Z，补 X 分组得 HE LX LO WO RL DX，逐对加密 KC NV MP YM QM CY ⇒ KCNVMPYMQMCY。原用例注入 '1\\n2\\n3'（无字母，输出为空故 saveHistory 未触发）才侥幸未见历史行；改注入字母明文后由输入真实派生，且锚结果区密文、绕开 #historyList（历史行含运行时刻，必然漂移）。默认态明文为 ATTACKATDAWN ⇒ 不命中该串。"
  },
  {
    "slug": "it/polybius-cipher",
    "inputs": {
      "key": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "fmt": "colrow",
      "sep": ""
    },
    "expect": [
      " W X Y Z\n1 2 3\ncolrow"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"fmt\":\"colrow\",\"sep\":\"\"}，输出区含「 W X Y Z\n1 2 3\ncolrow」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/poisson-distribution",
    "inputs": {
      "lambda": "42",
      "k": "42"
    },
    "expect": [
      "P(X = 42) = 0.061",
      "e −λ = e −42 = 5.74952226e-19"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lambda\":\"42\",\"k\":\"42\"}，输出区含「P(X = 42) = 0.061」；分步区 e^(−42)=5.74952226e-19 说明极小真值改走科学计数法后不再被格式阈值吞成 0（原锚「× 0 /」即该缺陷产物，已随修复更新）。默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/prime-checker",
    "inputs": {
      "n": "42"
    },
    "expect": [
      "42\n判定结果 42 是合数 ❌ 最小质因数： 2 因数分解： 42 = 2 × 3 × 7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\"}，输出区含「42\n判定结果 42 是合数 ❌ 最小质因数： 2 因数分解： 42 = 2 ×…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/prime-checker",
    "inputs": {"n": "2.5"},
    "expect": ["请输入整数：不支持小数、科学计数法、负号或其它字符。"],
    "ref": "IT-N476：旧实现 parseFloat + Math.floor 把 2.5 静默改成 2 并判「2 是质数 ✅」，判定对象被替换且无提示。现严格校验 /^\\d+$/ 并明确拒绝小数；默认态 97 输出质数，不含该提示 ⇒ 强判别。"
  },
  {
    "slug": "it/prime-checker",
    "inputs": {"n": "9007199254740993"},
    "expect": ["9007199254740993 = 3 × 3002399751580331"],
    "ref": "IT-N476：= 3 × 3002399751580331，旧实现 parseFloat 舍入成 2^53=9007199254740992 并分解成 53 个 2。现超 2^53 走 BigInt，最小质因数 3、输入原样保留；修复前不含该分解串 ⇒ 红。"
  },
  {
    "slug": "it/prime-checker",
    "inputs": {"n": "1e21"},
    "expect": ["请输入整数：不支持小数、科学计数法、负号或其它字符。"],
    "ref": "IT-N476：科学计数法输入旧实现显示「1e+21 是合数」并给出伪分解，现按非十进制整数拒绝。与上一条小数用例构成两类非法格式双覆盖；默认态无该提示。"
  },
  {
    "slug": "it/prime-checker",
    "inputs": {"n": "2305843009213693951"},
    "expect": ["2305843009213693951 是质数"],
    "ref": "IT-N476：2^61−1（梅森质数）远超 2^53，旧实现按浮点判合数；现 BigInt + 确定性 Miller-Rabin（12 个素数基）判质数，验证大数判定不是简单拒绝而是精确算对。"
  },
  {
    "slug": "it/prime-checker",
    "clicks": ["document.getElementById('n').value='2.5';calcTool();document.getElementById('stats').textContent='N476 guard='+((typeof __pcMillerRabin==='function')&&__pcMillerRabin(2305843009213693951n)===true&&__pcMillerRabin(9007199254740993n)===false&&String(document.getElementById('result').innerHTML).indexOf('2 是质数')<0?1:0);"],
    "expect": ["N476 guard=1"],
    "ref": "IT-N476 行为契约：直接调用页面 BigInt Miller-Rabin 判定（2^61−1 质数 / 2^53+1 合数），并确认 2.5 不再被静默判成「2 是质数」。注意本页被 harness 包装成 __prime_checker_f0，String(calcTool) 只有包装壳，源码契约在此页不可用；改行为契约。"
  },
  {
    "slug": "it/prime-checker",
    "clicks": ["document.getElementById('stats').textContent='N476EN='+((typeof __pcL==='function')&&__pcL('判定结果','Result')==='判定结果'&&__pcL('是质数','is prime')==='是质数'?1:0);"],
    "expect": ["N476EN=1"],
    "ref": "IT-N476 顺带：#result 动态重建，英文态静态扫描覆盖不到；行为契约守住 __pcL helper 存在且中文态逐字返回原中文，英文态 0 CJK 由 jsdom 真机探针验证。"
  },
  {
    "slug": "it/pomodoro",
    "inputs": {
      "focusMin": "42",
      "shortMin": "42",
      "longMin": "42"
    },
    "expect": [
      "始第一个番茄吧！\n42:00\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focusMin\":\"42\",\"shortMin\":\"42\",\"longMin\":\"42\"}，输出区含「始第一个番茄吧！\n42:00\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "it/pomodoro",
    // IT-N480：跳过（含从未开始）不得计入完成次数与专注分钟。
    "clicks": ["confirm=function(){return true;};var a=todayStats.totalCount,b=todayStats.focusTime,c=todayStats.history.length;resetTimer();skipTimer();document.getElementById('__tbProbe').textContent='SKIP '+(todayStats.totalCount===a&&todayStats.focusTime===b&&todayStats.history.length===c?'ZERO':'COUNT');"],
    "expect": ["SKIP ZERO"],
    "ref": "IT-N480：旧实现 skipTimer() 无条件调 completeSession()，即使从未开始也按配置时长 +1 次、+25 分钟并写历史。修复后跳过走 skip=true 分支：不计数、不加时、不写历史。探针读顶层 todayStats 前后快照，默认态不执行探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/pomodoro",
    // IT-N481：剩余时间按真实时间戳差值计算，而非每次 tick 减 1 秒。
    "clicks": ["var D=Date.now,T=1700000000000;Date.now=function(){return T;};resetTimer();document.getElementById('focusMin').value='25';updateDurations();toggleTimer();T+=600000;tick();var s=document.getElementById('timeDisplay').textContent;Date.now=D;pauseTimer();document.getElementById('__tbProbe').textContent='TSTAMP '+(s==='15:00'?'OK':'BAD:'+s);"],
    "expect": ["TSTAMP OK"],
    "ref": "IT-N481：用固定假时间戳（不依赖当前真实时间）模拟后台节流——起表后把时钟推进 10 分钟再 tick，25 分钟专注应剩 15:00。旧实现 tick 只 timeLeft-- ⇒ 24:59，不命中。探针结束恢复 Date.now 并暂停计时；默认态不执行探针 ⇒ 零逃生。"
  },
  {
    "slug": "it/js-minify",
    // IT-N464：字符串内的 // 不得被当作行注释删除。
    "clicks": ["var q=String.fromCharCode(34);var s=document.getElementById('src');s.value='var u='+q+'https://x.com/a'+q+';result=u;';calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='LEX '+(h.indexOf('https://x.com/a')>=0?'SAFE':'BROKEN');"],
    "expect": ["LEX SAFE"],
    "ref": "IT-N464：旧实现先删 /* */、再删 // 到行尾，字符串里的 `https://x.com/a` 从 `//` 起被吞，产出 `var u=\"https: result=u;\"` 废码。修复后轻量词法扫描把字符串整体保留，注释只在代码区删除。探针用 String.fromCharCode(34) 构造引号避开 clicks 转义坑；默认态示例不含 x.com/a ⇒ 零逃生。"
  },
  {
    "slug": "it/postgresql-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "通信 DDL\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「通信 DDL\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "it/punycode",
    "inputs": {
      "input": "a.中文"
    },
    "clicks": ["enc()"],
    "expect": [
      "a.fiq228c"
    ],
    "ref": "独立复算（替换原「1\\n2\\n3」低价值用例）：点号分段时 ASCII 标签 a 原样保留、中文标签编码为 fiq228c ⇒ a.fiq228c；默认输入为中文域名，产物不含该串。"
  },
  {
    "slug": "it/python-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "异步 标准库\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「异步 标准库\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/python-escape",
    "inputs": {
      "input": "a\\b",
      "output": "",
      "mode": "raw",
      "qtype": "double"
    },
    "expect": ["r\"a\\b\""],
    "ref": "Python 原始字符串不做任何转义：r\"a\\b\" 的值就是 a\\b。旧实现把反斜杠再翻倍成 r\"a\\\\b\"（值与原文不符）；本例锚定单反斜杠形态。默认 normal 模式产物带引号但与 r 前缀不同 ⇒ 回退态不命中。"
  },
  {
    "slug": "it/python-escape",
    "inputs": {
      "input": "a\"b",
      "mode": "raw",
      "qtype": "double"
    },
    "expect": ["\"a\\\"b\""],
    "ref": "原始字符串无法精确表示含闭合引号的文本（r\"a\"b\" 会被截断）⇒ 本页退回普通字符串转义，产物 \"a\\\"b\" 且不带 r 前缀。旧实现输出 r\"a\\\"b\"（值里残留反斜杠）⇒ 不命中。"
  },
  {
    "slug": "it/qr-decoder",
    "inputs": {
      "input": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n识别到 1 种类型 纯文本 内容: 1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\"}，输出区含「1 2 3\n识别到 1 种类型 纯文本 内容: 1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/qr-beautify",
    "inputs": {
      "fg": "abc123测试",
      "bg": "abc123测试",
      "text": "1\n2\n3",
      "ecc": "M",
      "style": "square"
    },
    "expect": [
      " defined\nM\nabc123测试\nabc123测试\nsquare"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fg\":\"abc123测试\",\"bg\":\"abc123测试\",\"text\":\"1\\n2\\n3\",\"ecc\":\"M\",\"style\":\"square\"}，输出区含「 defined\nM\nabc123测试\nabc123测试\nsquare」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/qr-beautify",
    "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var c=document.getElementById('qrCanvas');c.width=100;c.toDataURL=function(){throw new Error('boom')};downloadPng();"],
    "expect": [
      "TOAST:导出失败：Error"
    ],
    "ref": "B 类失败注入：downloadPng() 内 `a.href=c.toDataURL('image/png')` 裸调。把 #qrCanvas 的 toDataURL 改为必抛 Error 并把 ToolBox.showToast 换成录音器 ⇒ 结果区必须出现「TOAST:导出失败：Error」。"
      + "修复前异常裸冒成 pageerror、无任何提示；默认态无 TOAST: 串 ⇒ 判别明确。"
  },
  {
    "slug": "it/qr-beautify",
    "clicks": [
      "globalThis.__q=[];globalThis.__t=[];ToolBox.showToast=function(m){globalThis.__t.push(String(m));};globalThis.qrcode=function(){this.addData=function(){};this.make=function(){};this.getModuleCount=function(){return 21;};this.isDark=function(r,c){return (r+c)%2===0;};};var __myCtx={clearRect:function(){},fillRect:function(){},fillStyle:'',beginPath:function(){},moveTo:function(){},arcTo:function(){},closePath:function(){},fill:function(){},drawImage:function(){globalThis.__q.push({t:'draw'});}};document.getElementById('qrCanvas').getContext=function(){return __myCtx;};globalThis.FileReader=function(){this.readAsDataURL=function(f){globalThis.__q.push({t:'rd',o:this,n:String(f&&f.name)});};};globalThis.Image=function(){var o=this;o.width=10;o.height=10;Object.defineProperty(o,'src',{set:function(v){o.__n=String(v);globalThis.__q.push({t:'img',o:o});}});};var __lf=document.getElementById('logoFile');if(!__lf._handlers.change||!__lf._handlers.change.length){__lf.__qrLogoBound=false;initLogoInput();}function __chg(n){__lf.files=[{name:n,type:'image/png'}];__lf._handlers.change[0].call(__lf,{target:__lf,preventDefault:function(){},stopPropagation:function(){}});}function __rds(){return globalThis.__q.filter(function(x){return x.t==='rd';});}function __imgs(){return globalThis.__q.filter(function(x){return x.t==='img';});}function __draws(){return globalThis.__q.filter(function(x){return x.t==='draw';});}function __probe(s){document.getElementById('__tbProbe').textContent=s;}__chg('A.png');__rds()[0].o.result='A';__rds()[0].o.onload();__imgs()[0].o.onload();__probe('QROK=1 IMG='+String(__qrLogoImg&&__qrLogoImg.__n)+' HAS='+(__qrLogoImg?1:0)+' DRAW='+__draws().length+' LABEL='+(document.getElementById('result').innerHTML.indexOf('已嵌中心 logo')>=0?1:0));"
    ],
    "expect": [
      "QROK=1 IMG=A HAS=1 DRAW=1 LABEL=1"
    ],
    "ref": "复核失败重做·QR 美化过期回调 1/5（正常上传回归护栏）：用可控桩接管 FileReader / Image / 画布上下文，触发 A.png 的 rd.onload 与 img.onload ⇒ logo 生效、drawImage 1 次、结果区出现「已嵌中心 logo」（QROK=1 IMG=A HAS=1 DRAW=1 LABEL=1）。修复前后都应 PASS，用于证明取消机制没有破坏正常上传；默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "it/qr-beautify",
    "clicks": [
      "globalThis.__q=[];globalThis.__t=[];ToolBox.showToast=function(m){globalThis.__t.push(String(m));};globalThis.qrcode=function(){this.addData=function(){};this.make=function(){};this.getModuleCount=function(){return 21;};this.isDark=function(r,c){return (r+c)%2===0;};};var __myCtx={clearRect:function(){},fillRect:function(){},fillStyle:'',beginPath:function(){},moveTo:function(){},arcTo:function(){},closePath:function(){},fill:function(){},drawImage:function(){globalThis.__q.push({t:'draw'});}};document.getElementById('qrCanvas').getContext=function(){return __myCtx;};globalThis.FileReader=function(){this.readAsDataURL=function(f){globalThis.__q.push({t:'rd',o:this,n:String(f&&f.name)});};};globalThis.Image=function(){var o=this;o.width=10;o.height=10;Object.defineProperty(o,'src',{set:function(v){o.__n=String(v);globalThis.__q.push({t:'img',o:o});}});};var __lf=document.getElementById('logoFile');if(!__lf._handlers.change||!__lf._handlers.change.length){__lf.__qrLogoBound=false;initLogoInput();}function __chg(n){__lf.files=[{name:n,type:'image/png'}];__lf._handlers.change[0].call(__lf,{target:__lf,preventDefault:function(){},stopPropagation:function(){}});}function __rds(){return globalThis.__q.filter(function(x){return x.t==='rd';});}function __imgs(){return globalThis.__q.filter(function(x){return x.t==='img';});}function __draws(){return globalThis.__q.filter(function(x){return x.t==='draw';});}function __probe(s){document.getElementById('__tbProbe').textContent=s;}__chg('A.png');clearLogo();__rds()[0].o.result='A';__rds()[0].o.onload();var __im2=__imgs();if(__im2.length){__im2[0].o.onload();if(typeof __im2[0].o.onerror==='function')__im2[0].o.onerror();}if(typeof __rds()[0].o.onerror==='function')__rds()[0].o.onerror();__probe('QRRD=0 NEWIMG='+__imgs().length+' HAS='+(__qrLogoImg?1:0)+' TOAST='+globalThis.__t.length+' DRAW='+__draws().length);"
    ],
    "expect": [
      "QRRD=0 NEWIMG=0 HAS=0 TOAST=0 DRAW=0"
    ],
    "ref": "复核失败重做·QR 美化过期回调 2/5（清除发生在 FileReader 完成前）：选图后立即 clearLogo()，再让旧 rd.onload、它创建的 img.onload / onerror 以及 rd.onerror 全部执行。修复前实测 QRRD=0 NEWIMG=1 HAS=1 TOAST=1 DRAW=1（旧回调把 logo 写回并重新绘制，正是复核失败描述），修复后应为 NEWIMG=0 HAS=0 TOAST=0 DRAW=0 ⇒ 强判别。"
  },
  {
    "slug": "it/qr-beautify",
    "clicks": [
      "globalThis.__q=[];globalThis.__t=[];ToolBox.showToast=function(m){globalThis.__t.push(String(m));};globalThis.qrcode=function(){this.addData=function(){};this.make=function(){};this.getModuleCount=function(){return 21;};this.isDark=function(r,c){return (r+c)%2===0;};};var __myCtx={clearRect:function(){},fillRect:function(){},fillStyle:'',beginPath:function(){},moveTo:function(){},arcTo:function(){},closePath:function(){},fill:function(){},drawImage:function(){globalThis.__q.push({t:'draw'});}};document.getElementById('qrCanvas').getContext=function(){return __myCtx;};globalThis.FileReader=function(){this.readAsDataURL=function(f){globalThis.__q.push({t:'rd',o:this,n:String(f&&f.name)});};};globalThis.Image=function(){var o=this;o.width=10;o.height=10;Object.defineProperty(o,'src',{set:function(v){o.__n=String(v);globalThis.__q.push({t:'img',o:o});}});};var __lf=document.getElementById('logoFile');if(!__lf._handlers.change||!__lf._handlers.change.length){__lf.__qrLogoBound=false;initLogoInput();}function __chg(n){__lf.files=[{name:n,type:'image/png'}];__lf._handlers.change[0].call(__lf,{target:__lf,preventDefault:function(){},stopPropagation:function(){}});}function __rds(){return globalThis.__q.filter(function(x){return x.t==='rd';});}function __imgs(){return globalThis.__q.filter(function(x){return x.t==='img';});}function __draws(){return globalThis.__q.filter(function(x){return x.t==='draw';});}function __probe(s){document.getElementById('__tbProbe').textContent=s;}__chg('A.png');__rds()[0].o.result='A';__rds()[0].o.onload();var __ia=__imgs()[0].o;clearLogo();__ia.onload();__ia.onerror();__probe('QRIMG=0 HAS='+(__qrLogoImg?1:0)+' TOAST='+globalThis.__t.length+' DRAW='+__draws().length+' IMGS='+__imgs().length);"
    ],
    "expect": [
      "QRIMG=0 HAS=0 TOAST=0 DRAW=0 IMGS=1"
    ],
    "ref": "复核失败重做·QR 美化过期回调 3/5（清除发生在 Image 完成前）：rd 已完成并创建 img，clearLogo() 后才触发旧 img.onload 与 img.onerror。修复前实测 HAS=1 TOAST=1 DRAW=1，修复后 HAS=0 TOAST=0 DRAW=0、IMGS=1（img 本身已创建，只是回调失效）⇒ 强判别。"
  },
  {
    "slug": "it/qr-beautify",
    "clicks": [
      "globalThis.__q=[];globalThis.__t=[];ToolBox.showToast=function(m){globalThis.__t.push(String(m));};globalThis.qrcode=function(){this.addData=function(){};this.make=function(){};this.getModuleCount=function(){return 21;};this.isDark=function(r,c){return (r+c)%2===0;};};var __myCtx={clearRect:function(){},fillRect:function(){},fillStyle:'',beginPath:function(){},moveTo:function(){},arcTo:function(){},closePath:function(){},fill:function(){},drawImage:function(){globalThis.__q.push({t:'draw'});}};document.getElementById('qrCanvas').getContext=function(){return __myCtx;};globalThis.FileReader=function(){this.readAsDataURL=function(f){globalThis.__q.push({t:'rd',o:this,n:String(f&&f.name)});};};globalThis.Image=function(){var o=this;o.width=10;o.height=10;Object.defineProperty(o,'src',{set:function(v){o.__n=String(v);globalThis.__q.push({t:'img',o:o});}});};var __lf=document.getElementById('logoFile');if(!__lf._handlers.change||!__lf._handlers.change.length){__lf.__qrLogoBound=false;initLogoInput();}function __chg(n){__lf.files=[{name:n,type:'image/png'}];__lf._handlers.change[0].call(__lf,{target:__lf,preventDefault:function(){},stopPropagation:function(){}});}function __rds(){return globalThis.__q.filter(function(x){return x.t==='rd';});}function __imgs(){return globalThis.__q.filter(function(x){return x.t==='img';});}function __draws(){return globalThis.__q.filter(function(x){return x.t==='draw';});}function __probe(s){document.getElementById('__tbProbe').textContent=s;}__chg('A.png');__chg('B.png');var __rs=__rds();__rs[0].o.result='A';__rs[0].o.onload();__rs[1].o.result='B';__rs[1].o.onload();var __im=__imgs();__im[0].o.onload();__probe('QRSWAP=1 IMGS='+__im.length+' LAST='+String(__qrLogoImg&&__qrLogoImg.__n)+' HAS='+(__qrLogoImg?1:0)+' DRAW='+__draws().length+' TOAST='+globalThis.__t.length);"
    ],
    "expect": [
      "QRSWAP=1 IMGS=1 LAST=B HAS=1 DRAW=1 TOAST=0"
    ],
    "ref": "复核失败重做·QR 美化过期回调 4/5（换图乱序）：连续选 A、B 两图，先让 A 的 rd.onload 晚到，再让 B 完整加载。修复前实测 IMGS=2 LAST=A（旧图回调仍生效），修复后 A 的 rd.onload 被令牌挡住、根本不创建 Image ⇒ IMGS=1 LAST=B HAS=1 DRAW=1 TOAST=0 ⇒ 强判别。"
  },
  {
    "slug": "it/qr-beautify",
    "clicks": [
      "globalThis.__q=[];globalThis.__t=[];ToolBox.showToast=function(m){globalThis.__t.push(String(m));};globalThis.qrcode=function(){this.addData=function(){};this.make=function(){};this.getModuleCount=function(){return 21;};this.isDark=function(r,c){return (r+c)%2===0;};};var __myCtx={clearRect:function(){},fillRect:function(){},fillStyle:'',beginPath:function(){},moveTo:function(){},arcTo:function(){},closePath:function(){},fill:function(){},drawImage:function(){globalThis.__q.push({t:'draw'});}};document.getElementById('qrCanvas').getContext=function(){return __myCtx;};globalThis.FileReader=function(){this.readAsDataURL=function(f){globalThis.__q.push({t:'rd',o:this,n:String(f&&f.name)});};};globalThis.Image=function(){var o=this;o.width=10;o.height=10;Object.defineProperty(o,'src',{set:function(v){o.__n=String(v);globalThis.__q.push({t:'img',o:o});}});};var __lf=document.getElementById('logoFile');if(!__lf._handlers.change||!__lf._handlers.change.length){__lf.__qrLogoBound=false;initLogoInput();}function __chg(n){__lf.files=[{name:n,type:'image/png'}];__lf._handlers.change[0].call(__lf,{target:__lf,preventDefault:function(){},stopPropagation:function(){}});}function __rds(){return globalThis.__q.filter(function(x){return x.t==='rd';});}function __imgs(){return globalThis.__q.filter(function(x){return x.t==='img';});}function __draws(){return globalThis.__q.filter(function(x){return x.t==='draw';});}function __probe(s){document.getElementById('__tbProbe').textContent=s;}__chg('A.png');__rds()[0].o.result='A';__rds()[0].o.onload();var __ia=__imgs()[0].o;__chg('B.png');var __rb=__rds()[1];__rb.o.result='B';__rb.o.onload();var __ib=__imgs()[1].o;__ib.onload();__ia.onload();__ia.onerror();__probe('QRLATE=1 LAST='+String(__qrLogoImg&&__qrLogoImg.__n)+' DRAW='+__draws().length+' TOAST='+globalThis.__t.length);"
    ],
    "expect": [
      "QRLATE=1 LAST=B DRAW=1 TOAST=0"
    ],
    "ref": "复核失败重做·QR 美化过期回调 5/5（旧图 Image 回调最晚到达）：A 的 img 已创建后换选 B，B 正常生效，最后才触发 A 的 img.onload / img.onerror。修复前实测 LAST=A DRAW=2 TOAST=1（旧图覆盖新图并重复绘制），修复后 LAST=B DRAW=1 TOAST=0 ⇒ 强判别。"
  },
  {
    "slug": "it/python-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "cci(10))\n4\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「cci(10))\n4\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/qrcode",
    "inputs": {
      "size": "42",
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "textInput": "1\n2\n3",
      "contentTemplate": "https://example.com",
      "errorLevel": "M"
    },
    "expect": [
      "mple.com\n42\n42px\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nM"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"size\":\"42\",\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textInput\":\"1\\n2\\n3\",\"contentTemplate\":\"https://example.com\",\"errorLevel\":\"M\"}，输出区含「mple.com\n42\n42px\nabc123测试\nabc123测试\nabc12…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/quoted-printable",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rabbit",
    "inputs": {
      "key": "abc123测试",
      "iv": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "outputFormat": "hex"
    },
    "expect": [
      "abc123测试"
    ],
    "ref": "注入非默认 key/iv=「abc123测试」；Rabbit 密文随实现变化且随后被解密函数覆写，故断言 key/IV 回显（默认 key=myrabbitsecretkey，可判别）。密钥流正确性由 RFC 4503 测试向量另行核对：carry 必须用 Math.floor(t/2^32)，不可用 t>>>32。"
  },
  {
    "slug": "it/rail-fence-cipher",
    "inputs": {
      "depth": "42",
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      " 行2: · · 3 行3: · · · 行4: · · · 行5: · · · 行6: · · · 行7: · · · 行8: · · · 行9: · · · 行10: · · · 行11: · · · 行12: · · · 行13: ·"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"depth\":\"42\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「 行2: · · 3 行3: · · · 行4: · · · 行5: · · ·…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "it/random",
    "inputs": {
      "min": "42",
      "max": "42",
      "count": "42"
    },
    "expect": [
      "42\n42\n42\n6\n反面\n红: 4 7 9 22"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"min\":\"42\",\"max\":\"42\",\"count\":\"42\"}，输出区含「42\n42\n42\n6\n反面\n红: 4 7 9 22」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/random",
    "inputs": {
      "min": "-5",
      "max": "0",
      "count": "1"
    },
    "checkIds": ["integer"],
    "clicks": ["generateNumbers()"],
    "expect": ["-4"],
    "ref": "上限 0 是合法值：旧实现 `max || 100` 把 0 当假值回退成 100，[-5,100) 的整数输出不可能为 -4；修复后按 [-5,0] 生成，固定种子下首个整数为 -4。默认态（min=0/max=100）输出非负数，不含 `-4`（输入值 -5/0/1 也不含该串）。"
  },
  {
    "slug": "it/random",
    "inputs": {
      "min": "-5",
      "max": "0",
      "count": "0"
    },
    "checkIds": ["integer"],
    "clicks": ["generateNumbers()"],
    "expect": ["生成数量须为不小于 1 的整数"],
    "ref": "数量 0 的定义域不成立：旧实现 `parseInt(...) || 1` 静默改成 1 并生成数字；修复后显式拒绝并说明原因。默认 count=1 走正常生成路径，不出现该提示。"
  },
  {
    "slug": "it/random-string",
    "inputs": {
      "len": "8",
      "cnt": "0"
    },
    "checkIds": ["top_upper"],
    "clicks": ["calcTool()"],
    "expect": ["生成数量至少为 1 个"],
    "ref": "数量 0 的定义域不成立：旧实现 `parseInt(value||'5')||5` 双段兜底把 0 静默改成 5，与同函数 `if(cnt<1) cnt=1` 自相矛盾；修复后显式拒绝。默认 cnt=5 走正常生成路径，不含该提示。"
  },
  {
    "slug": "it/random-string",
    "inputs": {
      "len": "0",
      "cnt": "2"
    },
    "checkIds": ["top_upper"],
    "clicks": ["calcTool()"],
    "expect": ["长度至少为 1 位"],
    "ref": "长度 0 的定义域不成立：旧实现 `parseInt(value||'16')||16` 把 0 静默改成 16；修复后显式拒绝。默认 len=16 走正常生成路径，不含该提示。"
  },
  {
    "slug": "it/rc4",
    "inputs": {
      "key": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "outputFormat": "base64",
      "variant": "768"
    },
    "expect": [
      "abc123测试\n@�\nbase64\n768"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"outputFormat\":\"base64\",\"variant\":\"768\"}，输出区含「abc123测试\n@�\nbase64\n768」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rc4",
    // IT-N463：base64 模式下密文 27Ea（恰为全 hex 字符）必须按 base64 解出 1bb，而非误判为 Hex。
    "inputs": { "key": "mysecretkey", "input": "27Ea", "outputFormat": "base64", "variant": "0" },
    "clicks": ["decrypt();var o=String(document.getElementById('output').value);document.getElementById('__tbProbe').textContent='RC4DEC '+o;"],
    "expect": ["RC4DEC 1bb"],
    "ref": "key=mysecretkey、密文 `27Ea`（RC4(1bb) 的 Base64，恰全为 hex 字符且偶数长度）：IT-N463 修复后按所选 base64 格式显式解码 ⇒ 还原明文 1bb。旧实现 hex 启发式先命中，按 Hex 读 2 字节得乱码 ⇒ 不匹配。默认态 input 非 27Ea、不执行探针 ⇒ 判别明确。"
  },
  {
    "slug": "it/recovery-code-generator",
    "inputs": {
      "count": "42",
      "groups": "42",
      "glen": "42"
    },
    "expect": [
      "42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\",\"groups\":\"42\",\"glen\":\"42\"}，输出区含「42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/redis-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 脚本 内部\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 脚本 内部\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/regex-common",
    "inputs": {
      "limit": "42",
      "txt": "1\n2\n3"
    },
    "expect": [
      "箱地址 正则类别 0 个 匹配数量 无匹配 匹配结果（前 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"limit\":\"42\",\"txt\":\"1\\n2\\n3\"}，输出区含「箱地址 正则类别 0 个 匹配数量 无匹配 匹配结果（前 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/regex-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "flavor": "verbose"
    },
    "expect": [
      "1 2 3\nverbose\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"flavor\":\"verbose\"}，输出区含「1 2 3\n1 2 3\nverbose」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/regex-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 方法 常用\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 方法 常用\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/regex-visualizer",
    "inputs": {
      "pattern": "abc123测试"
    },
    "expect": [
      "tart S1: a S2: b S3: c S4: 1 S5: 2 S6: 3 S7: 测 S8: 试 S9"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pattern\":\"abc123测试\"}，输出区含「tart S1: a S2: b S3: c S4: 1 S5: 2 S6: 3…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rest-api-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 扩展 安全\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 扩展 安全\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rich-text-editor",
    "inputs": {
      "foreColor": "abc123测试",
      "backColor": "abc123测试",
      "linkUrl": "abc123测试",
      "source": "1\n2\n3",
      "blockFmt": "h1",
      "tableSize": "2x2"
    },
    "expect": [
      "\n0\n0\n0 B\nabc123测试\nabc123测试\nh1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"foreColor\":\"abc123测试\",\"backColor\":\"abc123测试\",\"linkUrl\":\"abc123测试\",\"source\":\"1\\n2\\n3\",\"blockFmt\":\"h1\",\"tableSize\":\"2x2\"}，输出区含「\n0\n0\n0 B\nabc123测试\nabc123测试\nh1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/robots-txt-generator",
    "inputs": {
      "sitemap": "abc123测试",
      "preview": "1\n2\n3"
    },
    "expect": [
      "elay（可选）\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sitemap\":\"abc123测试\",\"preview\":\"1\\n2\\n3\"}，输出区含「elay（可选）\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/roman-numeral-converter",
    "inputs": {
      "number": "42",
      "roman": "1\n2\n3",
      "dir": "from"
    },
    "expect": [
      "不是有效的罗马数字：仅可含 I/V/X/L/C/D/M"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"number\":\"42\",\"roman\":\"1\\n2\\n3\",\"dir\":\"from\"}。修复 IT-N368 后，非法罗马串（含换行/阿拉伯数字）经严格正则拒绝，输出「不是有效的罗马数字：仅可含 I/V/X/L/C/D/M…」；旧实现静默算成 0。默认态（数字→罗马）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rot-cipher",
    "inputs": {
      "shift": "42",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "rot13"
    },
    "expect": [
      "1 2 3\nrot13\n1 2 3\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"shift\":\"42\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"rot13\"}，输出区含「1 2 3\nrot13\n1 2 3\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/ruby-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 高级 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 高级 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rust-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 函数 工程\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 函数 工程\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/rust-escape",
    "inputs": {
      "kind": "string",
      "input": "a\"b"
    },
    "expect": [
      "\"a\\\"b\""
    ],
    "ref": "真机锚定：kind=string、input=a\"b 输出 Rust 字符串字面量 \"a\\\"b\"；旧用例注入 output 且将输入回显作为期望，属于假绿。"
  },
  
  {
    "slug": "it/sitemap-generator",
    "inputs": {
      "urls": "1\n2\n3"
    },
    "expect": [
      "emap.xml 请每行粘贴一个以 http(s):// 开头的 URL。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"urls\":\"1\\n2\\n3\"}，输出区含「emap.xml 请每行粘贴一个以 http(s):// 开头的 URL。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/shell-script-formatter",
    "inputs": {
      "input": "    echo a\n    echo b",
      "indent": "2"
    },
    "clicks": [
      "minifyShell()"
    ],
    "expect": [
      "echo a",
      "echo b"
    ],
    "ref": "自动补强（B类零用例）：压缩保留换行并逐行去空白，注入带缩进的两行后输出 `echo a` / `echo b`；默认样例为备份脚本，不含这两行。"
  },
  {
    "slug": "it/slug-generator-advanced",
    "inputs": {
      "sep": "abc123测试",
      "maxLen": "42",
      "text": "1\n2\n3"
    },
    "expect": [
      "1 2 3\nabc123测试\n42\n1 ← 1 2 ← 2 3 ← 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sep\":\"abc123测试\",\"maxLen\":\"42\",\"text\":\"1\\n2\\n3\"}，输出区含「abc123测试\n42\n1 2 3\n1 ← 1 2 ← 2 3 ← 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/slugify",
    "inputs": {
      "input": "1\n2\n3",
      "separator": "_",
      "mode": "remove"
    },
    "expect": [
      "1 2 3\n_\nremove\n1_2_3\n标准 1_2_3 复制 全小写 1_2_3 复制 下划线 1_2_3 复制 驼峰 123 复制"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"separator\":\"_\",\"mode\":\"remove\"}，输出区含「1 2 3\n_\nremove\n1_2_3\n标准 1_2_3 复制 全小写 1_2…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/sms-qr",
    "inputs": {
      "phone": "abc123测试",
      "msg": "1\n2\n3"
    },
    "expect": [
      "电话号码仅支持 5–15 位数字与可选的前导 +"
    ],
    "ref": "IT-N231 强锁：注入非数字号码 abc123测试，必须报「电话号码仅支持 5–15 位数字与可选的前导 +」而不是生成残缺 URI；默认号码 13800138000 合法、不命中该错误串。"
  },
  {
    "slug": "it/sql-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "公用表 函数\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「公用表 函数\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/sql-escape",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "dialect": "postgres"
    },
    "expect": [
      "1 2 3\n1 2 3\npostgres",
      "1 2 3\npostgres\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"dialect\":\"postgres\"}，输出区含「1 2 3\n1 2 3\npostgres」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/sqlite-runner",
    "inputs": {
      "sqlInput": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sqlInput\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/sqlite-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 工具 函数\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 工具 函数\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/sql-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "dialect": "mysql",
      "indentSize": "4"
    },
    "expect": [
      "'active';\nmysql\n4\n1 2 3",
      "'active';\n4\n1 2 3\nmysql"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"dialect\":\"mysql\",\"indentSize\":\"4\"}，输出区含「'active';\nmysql\n4\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/standard-deviation",
    "inputs": {
      "data": "1\n2\n3",
      "dtype": "population"
    },
    "expect": [
      "1 2 3\npopulation\n数据（n=3）： 1, 2, 3 σ = 0.816 均值 x̄ 2 方差 0.667 标准差 0.816 平方和 SS "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\",\"dtype\":\"population\"}，输出区含「1 2 3\npopulation\n数据（n=3）： 1, 2, 3 σ = 0.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/stopwatch",
    "inputs": {
      "cdHours": "42",
      "cdMinutes": "42",
      "cdSeconds": "42"
    },
    "expect": [
      "42\n42\n42\n42:42:42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cdHours\":\"42\",\"cdMinutes\":\"42\",\"cdSeconds\":\"42\"}，输出区含「42\n42\n42\n42:42:42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/statistical-power",
    "inputs": {
      "d": "42",
      "n": "42",
      "alpha": "42",
      "tail": "one"
    },
    "expect": [
      "Please enter valid parameters.\n42\n42\n42\none"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"d\":\"42\",\"n\":\"42\",\"alpha\":\"42\",\"tail\":\"one\"}，输出区含「42\n42\n42\none\nPlease enter valid paramete…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/string-obfuscator",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "rev"
    },
    "expect": [
      "1 2 3\nrev\n✅ 混淆完成：原文 5 字符 → 输出 5 字符\n3 2 1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"rev\"}，输出区含「1 2 3\nrev\n✅ 混淆完成：原文 5 字符 → 输出 5 字符\n3 2 1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/summary-generator",
    "inputs": {
      "sentenceCount": "custom",
      "customCount": "14"
    },
    "clicks": [
      "generateSummary()"
    ],
    "expect": [
      "10\n10\n469\n0%"
    ],
    "ref": "IT-N547 功能改动同批同步（铁律①）：原分句器把顿号「、」当作 ≥20 字后的软分句点，示例文本被切成 14 句；本批改为只按 . ! ? 与 。！？… 分句 ⇒ 10 句。自定义 14 句时钳制到 10 句全部入选 ⇒ 统计卡「原文句数 10 / 摘要句数 10 / 字符数 469 / 压缩率 0%」。默认 5 句时压缩率非 0% ⇒ 该串不出现。旧 expect「14\\n14\\n469\\n0%」已随功能同步作废。"
  },
  {
    "slug": "it/svg-placeholder-generator",
    "inputs": {
      "w": "42",
      "h": "42",
      "txt": "abc123测试",
      "bg": "abc123测试",
      "fg": "abc123测试",
      "svgCode": "1\n2\n3"
    },
    "expect": [
      "t></svg>\nabc123测试\nSVG 尺寸 42 × 42 · 文件约 310 字节"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"h\":\"42\",\"txt\":\"abc123测试\",\"bg\":\"abc123测试\",\"fg\":\"abc123测试\",\"svgCode\":\"1\\n2\\n3\"}，输出区含「t></svg>\nabc123测试\nSVG 尺寸 42 × 42 · 文件约 3…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-cleaner",
    "inputs": {
      "tab2space-count": "42",
      "space2tab-count": "42",
      "input-text": "1\n2\n3",
      "output-text": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n5\n3\n42\n42\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tab2space-count\":\"42\",\"space2tab-count\":\"42\",\"input-text\":\"1\\n2\\n3\",\"output-text\":\"1\\n2\\n3\"}，输出区含「1 2 3\n5\n3\n42\n42\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-dedupe-sort",
    "inputs": {
      "customSep": "abc123测试",
      "input": "1\n2\n3",
      "separator": ","
    },
    "expect": [
      "1 2 3\n,\n1\n1\n0\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"customSep\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"separator\":\",\"}，输出区含「1 2 3\n,\n1\n1\n0\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-qr",
    "inputs": {
      "text": "1\n2\n3"
    },
    "expect": [
      "1 2 3"
    ],
    "ref": "真实 QR 改造后输出区仅回显文本（canvas 不参与文本比对）：注入 text=1\\n2\\n3，innerText 归一为「1 2 3」。默认样例为「Hello, World! 你好，世界！」，不出现该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-replace",
    "inputs": {
      "findInput": "abc123测试",
      "replaceInput": "abc123测试",
      "sourceText": "1\n2\n3",
      "resultText": "1\n2\n3"
    },
    "expect": [
      "1 2 3\nabc123测试\nabc123测试\n0\n0\n+0\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"findInput\":\"abc123测试\",\"replaceInput\":\"abc123测试\",\"sourceText\":\"1\\n2\\n3\",\"resultText\":\"1\\n2\\n3\"}，输出区含「abc123测试\nabc123测试\n1 2 3\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-statistics",
    "inputs": {
      "textInput": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n5 总字符(字素) 5 码点数 3 字符(无空格) 0 中文字 0 英文词 3 行数 1 段落 1 句子 0 总词数 0 不同词 0分钟 阅读时间\n请输入文本"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"textInput\":\"1\\n2\\n3\"}，输出区含「1 2 3\n5 总字符 3 字符(无空格) 0 中文字 0 英文词 3 行数 1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-ascii",
    "inputs": {
      "txt": "1\n2\n3"
    },
    "expect": [
      "十六进制 二进制 1 49 0x31 00110001 10 0x0A 00001010 2 50 0x32 00110010 10 0x0A 00001010 3 51 0x33 00110011"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"txt\":\"1\\n2\\n3\"}，输出区含「十六进制 二进制 1 49 0x31 00110001 10 0x0A 00001…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。第220批 IT-N183：十六进制补齐两位，换行 10 由 0xA 改 0x0A，expect 同批同步。"
  },
  {
    "slug": "it/text-similarity",
    "inputs": {
      "textA": "1\n2\n3",
      "textB": "1\n2\n3",
      "tokenMode": "word",
      "compareMode": "char"
    },
    "expect": [
      "1 2 3\n1 2 3\n5\n5\nword\nchar\n1.0000\n100.00%\n1.0000\n100.00%\n1.0000\n100.00% (距离: 0)\n1.0000\n100.00% (距离: 0)\n编辑距离: 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"textA\":\"1\\n2\\n3\",\"textB\":\"1\\n2\\n3\",\"tokenMode\":\"word\",\"compareMode\":\"char\"}，输出区含「1 2 3\n1 2 3\n5\n5\nword\nchar\n1.0000\n100.00%…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-binary",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "inputBin": "1\n2\n3",
      "outputText": "1\n2\n3",
      "encoding": "utf8",
      "sep": ",",
      "padBits": "16"
    },
    "expect": [
      "00101010\n1 2 3\n,\n16\nutf8\n0000000000110001,0000000000001010,0000000000110010,0000000000001010,0000000000110011\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"inputBin\":\"1\\n2\\n3\",\"outputText\":\"1\\n2\\n3\",\"encoding\":\"utf8\",\"sep\":\",\",\"padBits\":\"16\"}，输出区含「00101010\n1 2 3\n,\n16\nutf8\n000000000011000…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-hex",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "inputHex": "1\n2\n3",
      "outputText": "1\n2\n3",
      "encoding": "utf8",
      "sep": ",",
      "format": "upper"
    },
    "expect": [
      "00101010\n1 2 3\n,\nupper\nutf8\n31,0A,32,0A,33\n1 31 · 0A 2 32 · 0A 3 33\n2\n2\n2\n2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"inputHex\":\"1\\n2\\n3\",\"outputText\":\"1\\n2\\n3\",\"encoding\":\"utf8\",\"sep\":\",\",\"format\":\"upper\"}，输出区含「00101010\n1 2 3\n,\nupper\nutf8\n31,0A,32,0A,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-decimal",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "inputDec": "1\n2\n3",
      "outputText": "1\n2\n3",
      "encoding": "utf8",
      "sep": ",",
      "padDigits": "3"
    },
    "expect": [
      "00101010\n1 2 3\n,\n3\nutf8\n049,010,050,010,051\n1 49 · 10 2 50 · 10 3 51\n3\n3\n3\n3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"inputDec\":\"1\\n2\\n3\",\"outputText\":\"1\\n2\\n3\",\"encoding\":\"utf8\",\"sep\":\",\",\"padDigits\":\"3\"}，输出区含「00101010\n1 2 3\n,\n3\nutf8\n049,010,050,010,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-octal",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "inputOct": "1\n2\n3",
      "outputText": "1\n2\n3",
      "encoding": "utf8",
      "sep": ",",
      "padDigits": "auto"
    },
    "expect": [
      "* 42 052\n1 2 3\n,\nauto\nutf8\n061,012,062,012,063\n1 061 · 012 2 062 · 012 3 063\n3\n3\n3\n3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"inputOct\":\"1\\n2\\n3\",\"outputText\":\"1\\n2\\n3\",\"encoding\":\"utf8\",\"sep\":\",\",\"padDigits\":\"auto\"}，输出区含「* 42 052\n1 2 3\n,\nauto\nutf8\n061,012,062,0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-unicode",
    "inputs": {
      "txt": "1\n2\n3"
    },
    "expect": [
      "TF-16 转义 1 U+0031 \\u0031 U+000A \\u000A 2 U+0032 \\u0032 U+000A \\u000A 3 U+0033 \\u0033"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"txt\":\"1\\n2\\n3\"}，输出区含「TF-16 转义 1 U+0031 \\u0031 U+000A \\u000A 2…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/text-to-unicode",
    "inputs": {"txt": "A😀B"},
    "expect": ["U+1F600 \\uD83D\\uDE00"],
    "ref": "IT-N405：辅助平面字符的 UTF-16 转义必须是完整代理对（高+低两个 \\uXXXX），只出高代理 \\uD83D 会得到非法孤立代理、无法嵌回 JS 字符串。输入用 😀(U+1F600) 而非默认样例里的 🚀 ⇒ 默认态输出不含 U+1F600，判别力真实。"
  },
  {
    "slug": "it/text-to-unicode",
    "inputs": {"txt": "𝄞A"},
    "expect": ["U+1D11E \\uD834\\uDD1E"],
    "ref": "IT-N405：换一个高代理不是 D83D 的码点（U+1D11E G 谱号 → D834 DD1E），验证代理对是按公式从码点算出的，而非对 emoji 硬编码；同时覆盖 BMP 字符紧随其后的边界。"
  },
  {
    "slug": "it/text-truncate",
    "inputs": {
      "limit": "42",
      "input": "1\n2\n3",
      "mode": "words",
      "ellipsis": "…"
    },
    "expect": [
      "1 2 3\n1 2 3\nwords\n42\n…"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"limit\":\"42\",\"input\":\"1\\n2\\n3\",\"mode\":\"words\",\"ellipsis\":\"…\"}，输出区含「1 2 3\n1 2 3\nwords\n42\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/time-format-converter",
    "inputs": {
      "inTime": "abc123测试"
    },
    "expect": [
      "abc123测试\n无法解析时间，请输入合法值"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inTime\":\"abc123测试\"}，输出区含「abc123测试\n无法解析时间，请输入合法值」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/tmux-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 其他 配置\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 其他 配置\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "it/timestamp-converter",
    "inputs": {
      "timestampSec": "abc123测试",
      "timestampMs": "abc123测试",
      "dateInput": "abc123测试",
      "calcStartDate": "abc123测试",
      "calcAmount": "42",
      "diffStart": "abc123测试",
      "diffEnd": "abc123测试",
      "calcOp": "subtract",
      "calcUnit": "week"
    },
    "expect": [
      " 14:00:00\nabc123测试\n42\nabc123测试\nabc123测试\nsubtract\nweek"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"timestampSec\":\"abc123测试\",\"timestampMs\":\"abc123测试\",\"dateInput\":\"abc123测试\",\"calcStartDate\":\"abc123测试\",\"calcAmount\":\"42\",\"diffStart\":\"abc123测试\",\"diffEnd\":\"abc123测试\",\"calcOp\":\"subtract\",\"calcUnit\":\"week\"}，输出区含「 14:00:00\nabc123测试\n42\nabc123测试\nabc123测试\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/timestamp-converter",
    "inputs": { "diffStart": "2025-12-31", "diffEnd": "2026-01-01" },
    "clicks": ["calculateDiff();document.getElementById('__tbProbe').textContent=document.getElementById('calcResult2').textContent;"],
    "expect": ["相差整年数: 0 年", "相差整月数: 0 个月", "相差天数: 1 天"],
    "ref": "IT-N45 相差年/月按日历字段相减的回归：2025-12-31→2026-01-01 仅 1 天，旧实现按年份/月份字段差输出「约 1 年」「约 1 个月」；整月/整年口径修复后为 0/0，天数 1。expect 三条都绑定注入日期派生的输出，旧源码「约 1 年」不命中 ⇒ 强判别。用 clicks 显式调 calculateDiff（diffStart 无 oninput）。"
  },
  {
    "slug": "it/toml-to-json",
    "inputs": {
      "source": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "JSON 输出 {}"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"source\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「JSON 输出 {}」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/toml-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "toml-input": "1\n2\n3",
      "json-input": "1\n2\n3"
    },
    "expect": ["2 (line"],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"toml-input\":\"1\\n2\\n3\",\"json-input\":\"1\\n2\\n3\"}，输出区含「002 ] } }\n❌ undefined\n✅ TOML 语法验证通过！\n{}\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/triangle-calculator",
    "inputs": {
      "a": "42",
      "b": "42",
      "c": "42"
    },
    "expect": [
      "42\n42\n42\n计算结果 126.000 周长 63.000 半周长 763.834 面积 锐"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"b\":\"42\",\"c\":\"42\"}，输出区含「42\n42\n42\n计算结果 126.000 周长 63.000 半周长 763.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/typescript-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 模块 配置\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 模块 配置\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/unicode-lookup",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "3 U+0033 · DIGIT THREE 测 U+6D4B · CJK UNIFIED IDEOGRAPH-6D4B 试 U+8BD5 · CJK UNIFIED IDEOGRAPH-8BD5\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「3 U+0033 测 U+6D4B 试 U+8BD5\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。IT-N554/N555 搜索卡片新增真实 Unicode 名称，按铁律①同批同步 expect。"
  },
  {
    "slug": "it/uniform-distribution",
    "inputs": {
      "a": "42",
      "b": "42",
      "x": "42",
      "c": "42",
      "d": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\nRequire b > a.",
      "Require b > a.\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"b\":\"42\",\"x\":\"42\",\"c\":\"42\",\"d\":\"42\"}，输出区含「42\n42\n42\n42\n42\nRequire b > a.」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    "slug": "it/unit-converter-advanced",
    "inputs": {
      "val": "42",
      "from": "abc123测试",
      "cat": "mass"
    },
    "expect": [
      "mass\n42\nabc123测试\n换算结果 ⚠️ 类别 mass 不支持单位 abc123测试。可选项：kg,g,mg,t,lb,oz,st"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"from\":\"abc123测试\",\"cat\":\"mass\"}，输出区含「mass\n42\nabc123测试\n换算结果 ⚠️ 类别 mass 不支持单位 a…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/url-encode",
    "inputs": {
      "baseUrl": "abc123测试",
      "parseInput": "abc123测试",
      "asciiFilter": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "builtUrl": "1\n2\n3"
    },
    "expect": [
      "5 B\n+0.0%"
    ],
    "ref": "派生量锚：注入 '1\\n2\\n3'（5 字符 / 5 字节）后统计卡渲染输入大小 5 B、膨胀率 +0.0%（输出长度与输入字节数相等，按页面口径 (5−5)/5×100）。2026-11-05 同批修正：真实 localStorage 桩下注入即写历史并重渲染，原自动补强 expect 里的「暂无历史记录」不再出现（旧空桩把 setItem 吞掉才侥幸保留）；改为锚结果区统计值、绕开 #historyList（历史行含运行时刻，必然漂移）。默认输入为长 URL 样例 ⇒ 不出现 5 B / +0.0%。"
  },
  {
    "slug": "it/url-encoder-advanced",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "mode": "full"
    },
    "expect": [
      "1 2 3\n1 2 3\nfull"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"mode\":\"full\"}，输出区含「1 2 3\n1 2 3\nfull」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/url-qr",
    "inputs": {
      "url": "https://chenguangwu.github.io/tools/it/url-qr.html",
      "ecl": "H"
    },
    "expect": [
      "内容 50 字节 · 纠错等级 H · 最小版本 V6（41×41 模块）"
    ],
    "ref": "真编码器改造：url 50 个 ASCII 字节、纠错 H（容量表 H 的 V5=44、V6=58）⇒ qrPlan 选最小版本 V6，模块 17+4×6=41 ⇒ 结果区输出该串。默认态是 github.com + M（22 字节 ⇒ V2、25×25），不含 50/V6/41，且 'H' 不是默认选项值。"
  },
  {
    "slug": "it/url-qr",
    // IT-N456：renderQR 必须走真实编码器 API——传 level、addData(原文)、切 UTF-8、返回 qr 对象。
    // 旧假实现自造 strHash/pseudoRandom 点阵，从不调用 qrcode ⇒ 探针全 NA 且返回数组。
    "inputs": { "url": "https://github.com" },
    "clicks": ["var _l={level:'NA',data:'NA',made:'N',utf8:'N'};globalThis.qrcode=function(t,lv){_l.level=String(lv);return {addData:function(d){_l.data=String(d);},make:function(){_l.made='Y';},getModuleCount:function(){return 25;},isDark:function(){return false;}};};globalThis.qrcode.stringToBytesFuncs={'UTF-8':function(s){_l.utf8='Y';return s;}};globalThis.qrcode.stringToBytes=null;var r=renderQR('https://verify.example.com/pay','Q');_l.utf8=(globalThis.qrcode.stringToBytes===globalThis.qrcode.stringToBytesFuncs['UTF-8'])?'Y':'N';document.getElementById('__tbProbe').textContent='QRAPI '+_l.level+'|'+_l.data+'|'+_l.made+'|'+_l.utf8+'|'+(r&&r.qr?'OBJ':'ARR');"],
    "expect": ["QRAPI Q|https://verify.example.com/pay|Y|Y|OBJ"],
    "ref": "注入 mock 编码器后调 renderQR(注入URL, 'Q')：真实现必传 level=Q、addData 注入 URL、调 make、切 UTF-8 并返回 {qr} 对象 ⇒ 探针串含注入值。旧假实现 strHash/pseudoRandom 自造点阵，全程不碰 qrcode ⇒ NA/ARR，判别明确。默认态不执行探针。"
  },
  {
    "slug": "it/url-qr",
    // IT-N457：尺寸下拉必须真正改变 canvas 边长；drawQR 不再固定 cell=8。
    "inputs": { "url": "https://github.com" },
    "clicks": ["var _c=[];globalThis.qrcode=function(){return {addData:function(){},make:function(){},getModuleCount:function(){return 25;},isDark:function(){return false;}};};var _ce=document.createElement.bind(document);document.createElement=function(t){var e=_ce(t);if(t==='canvas'){e.getContext=function(){return {fillStyle:'',fillRect:function(){}};};_c.push(e);}return e;};function _sz(px){document.getElementById('qrSize').value=String(px);generate();return _c.length?_c[_c.length-1].width:0;}var w128=_sz(128),w512=_sz(512);document.createElement=_ce;document.getElementById('__tbProbe').textContent='SIZE '+w128+'/'+w512;"],
    "expect": ["SIZE 128/512"],
    "ref": "注入 mock 编码器（固定 25 模块）+ 捕获 createElement('canvas')，切尺寸 128 与 512 各调 generate()：真实现 canvas.width 必分别为 128/512 ⇒ 探针 SIZE 128/512。旧实现无尺寸控件、drawQR 固定 cell=8 ⇒ createElement('qrSize') 取不到且宽度恒 232/232，判别明确。"
  },
  {
    "slug": "it/url-parser",
    "inputs": {
      "b-hostname": "abc123测试",
      "b-port": "42",
      "b-pathname": "abc123测试",
      "b-hash": "abc123测试",
      "urlInput": "1\n2\n3",
      "b-protocol": "http:"
    },
    "expect": [
      "o bar 复制\nabc123测试\nhttp:\n42\nabc123测试\nabc123测试\nhttp://abc123测试:42/abc123测试?foo=bar#abc123测试\n× ×"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"b-hostname\":\"abc123测试\",\"b-port\":\"42\",\"b-pathname\":\"abc123测试\",\"b-hash\":\"abc123测试\",\"urlInput\":\"1\\n2\\n3\",\"b-protocol\":\"http:\"}，输出区含「o bar 复制\nabc123测试\nhttp:\n42\nabc123测试\nabc1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/username-generator",
    "inputs": {
      "kw": "abc123测试",
      "count": "42",
      "maxLen": "42"
    },
    "expect": [
      "abc123测试\n42\n42\nclassic\nabc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123测试 abc123"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"kw\":\"abc123测试\",\"count\":\"42\",\"maxLen\":\"42\"}，输出区含「abc123测试\n42\n42\nabc123测试 abc123测试 abc123测…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。IT-N557 新增 style 控件后 blob 字段序在 42/42 后多出 classic，按铁律①同批同步 expect。"
  },
  {
    "slug": "it/uuencode",
    "inputs": {
      "fname": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "begin 644 abc123测试 #,0HR \"\"C, ` end"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fname\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}。2026-10-26 S1 首屏即答案改造后：boot 首渲染令 input/output 先于 fname 登记 ⇒ 值回显段序变化，旧锚「abc123测试\\n1 2 3」断裂；改锚为兜底 enc() 的确定性产物 begin 644 abc123测试 头（依赖注入的 fname，默认态 file.txt ⇒ 不含该串，判别力保持且更强）。"
  },
  {
    "slug": "it/uuid-generator",
    "inputs": {"version": "v1", "count": "1"},
    "clicks": ["var u=generateUuidV1();var p=u.replace(/-/g,'');var tl=parseInt(p.slice(0,8),16),tm=parseInt(p.slice(8,12),16),th=parseInt(p.slice(12,16),16)&4095;var t=(BigInt(th)<<48n)|(BigInt(tm)<<32n)|BigInt(tl);var now=BigInt(Date.now())*10000n+122192928000000000n;var d=t>now?t-now:now-t;document.getElementById('output').value='V1 d='+(d<100000000n?1:0)+' v='+p.charAt(12)+' q='+(document.getElementById('version').value==='v1'?1:0);"],
    "expect": ["V1 d=1 v=1 q=1"],
    "ref": "IT-N407（高）：按 RFC 4122 从 time_low/time_mid/time_hi 拼回 100ns 时间戳，必须等于生成时刻（差 < 1e8 个 100ns，即同一毫秒内序号）。修复前用 Number + >>>32/>>>48，解出的时间漂到 2780 年甚至 4538 年 ⇒ d 远超阈值。断言与具体日期无关（harness Date 冻结在 2024-06-15，本地与 CI 一致）。q=1 绑注入的 version。"
  },
  {
    "slug": "it/uuid-generator",
    "inputs": {"version": "v1", "count": "1"},
    "clicks": ["var u=generateUuidV1();var p=u.replace(/-/g,'');var mid=parseInt(p.slice(8,12),16),hi=parseInt(p.slice(12,16),16)&4095;var t=BigInt(Date.now())*10000n+122192928000000000n;document.getElementById('output').value='V1F mid='+(mid===Number((t>>32n)&65535n)?1:0)+' hi='+(hi===Number((t>>48n)&4095n)?1:0);"],
    "expect": ["V1F mid=1 hi=1"],
    "ref": "IT-N407：直接对照 time_mid/time_hi 的真值。JS 位运算移位数按 32 取模 ⇒ 修复前 mid 取的是低 16 位、hi 取的是 >>>16 的低 12 位，两项都不可能等于 BigInt 取位的结果 ⇒ 双变红。"
  },
  {
    "slug": "it/uuid-generator",
    "inputs": {"version": "v1", "count": "2"},
    "clicks": ["var a=generateUuidV1(),b=generateUuidV1();var la=parseInt(a.replace(/-/g,'').slice(0,8),16),lb=parseInt(b.replace(/-/g,'').slice(0,8),16);var inc=(lb===la+1)||(la>lb&&lb===0);document.getElementById('output').value='V1SEQ inc='+(inc?1:0)+' q='+(document.getElementById('count').value==='2'?1:0);"],
    "expect": ["V1SEQ inc=1 q=1"],
    "ref": "IT-N407：同一毫秒内连续生成两条，时间字段必须以 100ns 序号递增（修复前 time_low 完全相同 ⇒ inc=0）。q=1 绑注入的 count=2。"
  },
  {
    "slug": "it/uuid-generator",
    "inputs": {"version": "v7", "count": "1"},
    "clicks": ["var u=generateUuidV7();var p=u.replace(/-/g,'');var hi=(BigInt(parseInt(p.slice(0,4),16))<<32n)|BigInt(parseInt(p.slice(4,12),16));document.getElementById('output').value='V7 v='+p.charAt(12)+' ms='+(hi===BigInt(Date.now())?1:0)+' q='+(document.getElementById('version').value==='v7'?1:0);"],
    "expect": ["V7 v=7 ms=1 q=1"],
    "ref": "IT-N408：v7 前 48 位必须是 Unix 毫秒时间戳、版本号位为 7。修复前页面根本没有 generateUuidV7（下拉也无 v7）⇒ clicks 抛错、输出区无 V7 串。"
  },
  {
    "slug": "it/uuid-generator",
    "inputs": {"version": "v7", "count": "1"},
    "clicks": ["generateUuid();var v=document.getElementById('output').value;document.getElementById('output').value='GEN7 ver='+(v.charAt(14)==='7'?1:0)+' len='+(v.length===36?1:0)+' q='+(document.getElementById('version').value==='v7'?1:0);"],
    "expect": ["GEN7 ver=1 len=1 q=1"],
    "ref": "IT-N408：真入口 generateUuid() 必须把 v7 分发到 generateUuidV7，而不是落到 else 的 v4。修复前产出版本号 4 ⇒ ver=0。v7 分支无 await，async 函数体同步跑完，输出区立即可读。"
  },
  {
    "slug": "it/uuid-generator",
    "inputs": {"version": "v5", "namespace": "abc", "name": "example.com", "count": "1"},
    "clicks": ["generateUuid();var v=document.getElementById('output').value;document.getElementById('output').value='NS5 bad='+(v.indexOf('格式非法')>=0?1:0)+' q='+(document.getElementById('namespace').value==='abc'?1:0);"],
    "expect": ["NS5 bad=1 q=1"],
    "ref": "IT-N409：v5 命名空间 'abc' 必须在结果区明确报「格式非法」并中止，不能静默产出看似合法的 UUID。修复前 uuidToBytes('abc') 得 [0xab,0x0c,0,0,…] 后照常哈希 ⇒ 无错误提示。q=1 绑注入的非法命名空间。"
  },
  {
    "slug": "it/uuid-v5-generator",
    "inputs": {
      "ns": "abc123测试",
      "name": "1\n2\n3"
    },
    "expect": [
      "abc123测试\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ns\":\"abc123测试\",\"name\":\"1\\n2\\n3\"}，输出区含「abc123测试\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/vector-dot-product",
    // 原 B 类零用例断言「向量 A x y z 向量 B x y z」= 页面 build() 渲染的静态标签，
    // 默认态即存在 ⇒ 恒真逃生。改为 4D 注入并断言算得的点积。
    "clicks": [
      "document.getElementById('dim').value='4';build();document.getElementById('a0').value=1;document.getElementById('a1').value=2;document.getElementById('a2').value=3;document.getElementById('a3').value=4;document.getElementById('b0').value=5;document.getElementById('b1').value=6;document.getElementById('b2').value=7;document.getElementById('b3').value=8;calculate()"
    ],
    "expect": [
      "A · B = 70"
    ],
    "ref": "4D 点积：A=(1,2,3,4)、B=(5,6,7,8) ⇒ 1×5+2×6+3×7+4×8 = 5+12+21+32 = 70（可手算复算）。默认 3D 零向量输出 A · B = 0，本例不命中。"
  },
  {
    "slug": "it/vector-cross-product",
    "inputs": {
      "a0": "42",
      "a1": "42",
      "a2": "42",
      "b0": "42",
      "b1": "42",
      "b2": "42"
    },
    "expect": [
      "||B|) = 0 → θ = 0° A × B = 0，说明 A 与 B 平行（或其中之一为零向量）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a0\":\"42\",\"a1\":\"42\",\"a2\":\"42\",\"b0\":\"42\",\"b1\":\"42\",\"b2\":\"42\"}，输出区含「||B|) = 0 → θ = 0° A × B = 0，说明 A 与 B 平行…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/video-bitrate",
    "inputs": {
      "w": "42",
      "h": "42",
      "fps": "42",
      "dur": "42",
      "br": "42"
    },
    "expect": [
      "bps 当前码率 12617.1 MB (12.32"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"h\":\"42\",\"fps\":\"42\",\"dur\":\"42\",\"br\":\"42\"}，输出区含「bps 当前码率 12617.1 MB (12.32」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/vim-cheatsheet",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      " 高级 跳转\n共 0 项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「 高级 跳转\n共 0 项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/vector-magnitude",
    // 原用例只注入 dim:"3"（等于页面默认 selected）且断言零向量静态提示语，
    // 默认态即命中的恒真逃生。改为 6D 零向量注入，断言仅 6D 才出现的展开式。
    "clicks": [
      "document.getElementById('dim').value='6';build();var i;for(i=0;i<6;i++){document.getElementById('v'+i).value=0;}calculate()"
    ],
    "expect": [
      "= √((0)² + (0)² + (0)² + (0)² + (0)² + (0)²)"
    ],
    "ref": "6D 零向量：模长展开式逐项为 (0)²，共 6 项 ⇒ 保留「零向量（|v|=0）无单位向量/方向余弦」分支覆盖（旧实现 `m||1` 分母伪造成 1 的回归），且 6 项展开式默认 3D 态（3 项）不命中，判别力真实。"
  },
  {
    "slug": "it/vector-magnitude",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value=3;document.getElementById('v1').value=4;document.getElementById('v2').value=0;calculate()"],
    "expect": [
      "cos α = 0.6, cos β = 0.8, cos γ = 0"
    ],
    "ref": "非零向量方向余弦回归：v=(3,4,0)、|v|=5 ⇒ cos α=3/5=0.6、cos β=4/5=0.8、cos γ=0/5=0。防「零向量守卫」误拦正常输入；运行时输入框无 HTML 默认值，故用 clicks 赋值。"
  },
  {
    "slug": "it/whitespace",
    "inputs": {
      "source": "1\n2\n3"
    },
    "expect": [
      "原始 处理后 1 1 1 2 2 2 3 3 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"source\":\"1\\n2\\n3\"}，输出区含「原始 处理后 1 1 1 2 2 2 3 3 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/wifi-qr",
    "inputs": {
      "ssid": "abc123测试",
      "pass": "abc123测试",
      "enc": "WEP"
    },
    "expect": [
      "abc123测试\nabc123测试\nWEP\nWIFI:T:WEP;S:abc123测试;P:abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ssid\":\"abc123测试\",\"pass\":\"abc123测试\",\"enc\":\"WEP\"}，输出区含「abc123测试\nabc123测试\nWEP\nWIFI:T:WEP;S:abc12…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/xml-formatter",
    "domParser": true,
    "inputs": {
      "input": "<note><!-- 头部注释 --><to from=\"Alice\">Bob</to><body priority=\"high\">Hello<raw><![CDATA[<unparsed>text</unparsed>]]></raw></body><meta><date>2025-01-01</date></meta></note>",
      "indent": "2"
    },
    "clicks": [
      "doBeautify(); document.getElementById('probe').value = document.getElementById('output').textContent;"
    ],
    "expect": [
      "<note> <!-- 头部注释 -->",
      "<to from=\"Alice\">Bob</to> <body priority=\"high\">",
      "<raw> <![CDATA[<unparsed>text</unparsed>]]> </raw>",
      "</meta> </note>"
    ],
    "ref": "根标签与 CDATA 必须存活：序列化从 documentElement 起算（旧实现只遍历 documentElement.childNodes ⇒ 输出以 '></note>' 开头、<note> 丢失）；子节点判定纳入 CDATA（旧实现 `<raw>` 仅剩 CDATA 子节点被滤掉 ⇒ 输出 `<raw/>`、原文丢失）。期望串带格式化空白（如「<raw> <![CDATA[…]]> </raw>」），注入的原始输入为紧凑 XML 不含该形态 ⇒ 强判别。**断言走 probe.value**：collectStrings 对 innerHTML/textContent 会剥标签（尖括号语法会被整块吃掉），故点击时把格式化结果同步写入 probe 的 value（value 保留原文），断言才能覆盖标签形态。"
  },
  {
    "slug": "it/xor-cipher",
    "inputs": {
      "key": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "inFmt": "hex",
      "outFmt": "text"
    },
    "expect": [
      "处理失败：十六进制长度必须为偶数（每字节两位十六进制）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"inFmt\":\"hex\",\"outFmt\":\"text\"}。修复 IT-N345 后，hex 通道对奇数长度输入会抛「十六进制长度必须为偶数（每字节两位十六进制）」并写入 output，旧实现静默截断为错误字节；默认态（inFmt=text、输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "it/xxtea",
    "inputs": {
      "key": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3",
      "outputFormat": "hex"
    },
    "expect": [
      "abc123测试\n10f886e5c502677a4385b14f\nhex"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"key\":\"abc123测试\",\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\",\"outputFormat\":\"hex\"}，输出区含「abc123测试\n����\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。IT-N558/N559 顺带修 i18nText() 空参数后 encrypt 不再抛错，输出由乱码解密态变为 hex 密文态，按铁律①同批同步 expect。"
  },
  {
    "slug": "it/xxencode",
    "inputs": {
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "it/vigenere-visualizer",
    "inputs": {
      "key": "abc123测试",
      "input": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "明文 1 2 3 密钥 密文 1 2 3"
    ],
    "ref": "锚可视化分步表的三行结构（明文 / 密钥 / 密文，逐字符格），其值由注入 '1\\n2\\n3' 经 vigenere() 生成。2026-11-05 同批修正：真实 localStorage 桩下注入即写历史并重渲染，原自动补强 expect 里的「暂无历史记录」不再出现（旧空桩把 setItem 吞掉才侥幸保留）；改为锚结果区派生行、绕开 #historyList（历史行含运行时刻，必然漂移）。默认明文 ATTACKATDAWN ⇒ 不命中该串。"
  },
  {
    "slug": "it/yaml-formatter",
    "inputs": {
      "input": "1\n2\n3",
      "yaml-input": "1\n2\n3",
      "json-input": "1\n2\n3",
      "indent": "4"
    },
    "expect": [
      "h-CN\" } }\n4\n❌ undefined\n✅ YAML 语法验证通过！结构合法。\n{}\n{}\n转换失败: Unexpected non-whitespace character after JSON at position 2 (li",
      "level: info\n4\n✅ YAML 语法验证通过！结构合法。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"yaml-input\":\"1\\n2\\n3\",\"json-input\":\"1\\n2\\n3\",\"indent\":\"4\"}，输出区含「h-CN\" } }\n4\n❌ undefined\n✅ YAML 语法验证通过！结构…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。G06-S1 首屏自跑改变了元素创建序 ⇒ blob 字段序随之改变，expect 容忍新旧两种字段序；判别力不变。"
  },
  {
    slug: "it/url-parser",
    inputs: { urlInput: "https://x.test/p?q=<img src=x onerror=alert(1)>&tag=%3Cb%3E" },
    expect: ["q &lt;img src=x onerror=alert(1)&gt;"],
    ref: "IT-N12 转义：查询值经 URLSearchParams 解码为 <img src=x onerror=alert(1)>，渲染前必须转义成 &lt;img … &gt;；未转义时该串被当作标签剥掉、expect 不命中。默认示例查询值为 value/bar，同样不命中。",
  },
  {
    slug: "it/url-parser",
    inputs: { urlInput: "https://x.test/p?dup=alpha&dup=beta" },
    expect: ["dup alpha 复制 dup beta 复制"],
    ref: "IT-N12 重复参数：getAll 口径保留两条 dup 并逐行展示；旧实现 forEach 写同名键只剩 beta（alpha 行不存在）。默认示例无重复键。",
  },
  {
    slug: "it/url-parser",
    inputs: { urlInput: "https://x.test/p?q=a'b" },
    expect: ["a&#39;b"],
    ref: "IT-N12 引号：参数值含单引号时统一转义为 &#39;，不再拼进 onclick 属性（复制按钮改事件委托）；默认示例值不含引号。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl -d '{\"a\":1}' https://api.example.com/x" },
    expect: ["方法： POST URL： https://api.example.com/x"],
    ref: "IT-N14 默认 POST：无 -X 而带 -d 时 curl 实际以 POST 发送，旧实现固定输出 GET。默认示例显式 -X POST 且指向另一域名，不命中。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl -F 'file=@a.txt' --data-binary @b.json https://x.com/upload" },
    expect: ["URL： https://x.com/upload"],
    ref: "IT-N14 选项值映射：-F 与 --data-binary 各消费其后一个值，真实 URL 不再被 file=@a.txt 顶替。默认示例 URL 为 example.com/api/v1/pay。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl -F 'file=@a.txt' https://x.com/upload" },
    expect: ["Form： file=@a.txt"],
    ref: "IT-N14 表单字段：-F 的值单独收集并以 Form 段展示（旧实现无 Form 段、反而把它当 URL）。默认示例无 -F。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl -H 'X-Test: <img src=x onerror=alert(1)>' https://x.com/" },
    expect: ["X-Test: &lt;img src=x onerror=alert(1)&gt;"],
    ref: "IT-N14 头部转义：头部值原样进 innerHTML 会被当作标签执行；转义后 &lt;img … &gt; 作为文本保留。默认示例头部为 Content-Type，不含尖括号。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl -o out.txt -u user:pass https://x.com/api" },
    expect: ["URL： https://x.com/api"],
    ref: "IT-N14 选项值不误判：-o/-u 的值（out.txt、user:pass）均被成对消费，首个非选项词仍是真实 URL；旧实现把 out.txt 当 URL。默认示例 URL 不同。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl -X PUT -d 'x' https://x.com/api" },
    expect: ["方法： PUT URL： https://x.com/api"],
    ref: "IT-N14 显式方法优先：有 -X PUT 时即使带 -d 也不能被默认 POST 覆盖。默认示例为 POST + 另一域名。",
  },
  {
    slug: "it/curl-parser",
    // IT-D37：--data-urlencode 须做 RFC3986 百分号编码，空格→%20（非原样、非 +）。
    inputs: { cmd: "curl --data-urlencode 'q=a b' https://x.com/" },
    expect: ["q=a%20b"],
    ref: "curl --data-urlencode 'q=a b' 按 RFC3986 编码 value 中的空格为 %20 ⇒ body 含 q=a%20b。修复前把 --data-urlencode 当普通 data 原样拼接 ⇒ body 为 q=a b，不命中。默认示例无 --data-urlencode，不命中。",
  },
  {
    slug: "it/curl-parser",
    // IT-D37：value 中的 & 与 = 须编码，key 与 value 之间的分隔符 = 须保留。
    inputs: { cmd: "curl --data-urlencode 'name=a&b=c' https://x.com/" },
    expect: ["name=a%26b%3Dc"],
    ref: "name=a&b=c 按 key=value 拆分后只对 value 编码：& → %26、= → %3D，key 与分隔符保留 ⇒ name=a%26b%3Dc。修复前原样输出 name=a&b=c，不命中。",
  },
  {
    slug: "it/curl-parser",
    // IT-D38：双引号包裹时内部 \" 是转义引号，须还原成 "；单引号内保持字面反斜杠。
    inputs: { cmd: "curl -d \"{\\\"name\\\":\\\"a\\\"}\" https://x.com/" },
    expect: ['"body": "{\\"name\\":\\"a\\"}"'],
    ref: "双引号包裹的 -d 值 {\\\"name\\\":\\\"a\\\"} 中 \\\" 是转义引号，trimQuote 须还原为 {\"name\":\"a\"}，结构化 JSON 里表现为 \"body\": \"{\\\"name\\\":\\\"a\\\"}\"（JSON 序列化再转义）。修复前 body 保留反斜杠 {\\\"name\\\":\\\"a\\\"}，不命中。默认示例无转义引号，不命中。",
  },
  {
    slug: "it/curl-parser",
    // IT-D31：shell 反斜杠续行须折叠，不得把 `\` 当成 URL。
    inputs: { cmd: "curl -X POST \\\n https://api.example.com/users" },
    expect: ['"url": "https://api.example.com/users"'],
    ref: "命令用 `\\` + 换行续行，URL 在下一行；shell 语义下续行折叠为空格，URL 应为 https://api.example.com/users。修复前 `\\` 作为独立 token 被首个非选项词捕获成 URL ⇒ url 为 `\\`，不命中。默认示例为单行命令，不命中。",
  },

  {
    slug: "it/text-replace",
    clicks: ["applyReplacePreset('blank')"],
    expect: ["第一行 第二行 第三行"],
    ref: "IT-N4 删除空行预设：替换串必须是真实换行符；旧实现把字面量反斜杠 n 写入结果，输出为 第一行\\n第二行\\n第三行。默认结果区为空。",
  },
  {
    slug: "it/number-base-converter",
    inputs: { inputValue: "-10", inputBase: "10" },
    expect: ["-1010"],
    ref: "IT-N8 负数跨进制：旧实现非十进制分支只循环 n>0，-10 的二进制输出为空；修复后为 -1010。默认示例 255 不含该串。",
  },
  {
    slug: "it/number-base-converter",
    clicks: ["setInputBase(37)"],
    expect: ["⚠ 进制必须为 2–36 的整数。"],
    ref: "IT-N8 自定义进制越界：37 不是合法进制，旧实现静默按 37 解析并输出错误结果；修复后明确提示。默认示例为 10 进制、无该提示。",
  },
  {
    slug: "it/ini-parser",
    inputs: { input: "[s]\na = 1\n\n[s]\nb = 2" },
    clicks: ["doBeautify()"],
    expect: ["✅ 解析成功（已合并重复节）", "a = 1 b = 2"],
    ref: "IT-N23 重复节静默丢键：同名节应合并进同一对象而非覆盖，a 与 b 均保留并提示已合并；旧实现新建空对象后写入 b，a 丢失。默认示例节名唯一。",
  },
  {
    slug: "it/ini-parser",
    inputs: { input: "[s]\na = 1\n\n[t]\nb = 2" },
    clicks: ["doMinify()"],
    expect: ["[s] a=1 [t] b=2"],
    ref: "IT-N24 压缩语义：压缩应删除空行且去掉等号两侧空格；旧实现与美化完全相同，输出  a = 1 而非 a=1。默认加载示例为美化结果。",
  },
  {
    slug: "text/sensitive-word-filter",
    inputs: { content: "foo bar foo", words: "foo\nfoo" },
    expect: ["检测到 2 处命中。"],
    ref: "IT-N34 统一匹配源：重复关键词去重后按统一正则计数，foo 出现 2 次；旧实现按词条逐个 replace 导致重复词条各计一次、合计 4 次。默认输入为空。",
  },
  {
    slug: "text/analysis-density",
    inputs: { data: "banana banana", kw: "a" },
    expect: ["0.00%"],
    ref: "IT-N35 英文整词边界：a 不是独立单词，出现 0 次、密度 0.00%；旧实现按无边界子串计数得到 8 次、密度 400.00%。默认示例为 SEO 整词。",
  },
  {
    slug: "text/analysis-density",
    inputs: { data: "2026 11 03", kw: "2026" },
    expect: ["不适用（无汉字/英文单词）"],
    ref: "IT-N35 纯数字文本：词数为 0 时仍应给出关键词统计并把密度标为不适用；旧实现直接判 请输入文本。默认示例含汉字与英文。",
  },
  {
    slug: "text/text-extract-phones",
    inputs: { input: "138123456789 13912345678" },
    checkIds: ["mobile"],
    clicks: ["extract()"],
    expect: ["共找到: 1 个号码", "13912345678"],
    ref: "IT-N36 手机号右边界：12 位数字不应截取前 11 位，结果只保留合法号码 13912345678、计数为 1；旧实现会多提取 13812345678、计数为 2。默认示例号码不同，不命中。",
  },
  {
    slug: "text/text-extract-phones",
    inputs: { input: "+8613812345678 010-87654321" },
    checkIds: ["mobile", "landline", "international", "dedup"],
    clicks: ["extract()"],
    expect: ["010-87654321 +8613812345678"],
    ref: "IT-N36 国际号去重：+86 号码已含手机号，不应再重复提取 13812345678；修复后结果仅座机与国际号，顺序为座机在前。默认示例另有号码。",
  },
  {
    slug: "it/color-converter",
    clicks: ["fromInput('rgb(300, 0, 0)')"],
    expect: ["#ff0000"],
    ref: "IT-N46 RGB 范围钳制：300 应钳制为 255 得到 #ff0000；旧实现生成非法 #12c0000。默认颜色为 #667eea。",
  },
  {
    slug: "it/color-converter",
    clicks: ["fromInput('rgba(0, 0, 0, 1.5)')"],
    expect: ["rgba(0, 0, 0, 1)"],
    ref: "IT-N46 Alpha 钳制：1.5 应钳制到 1；旧实现输出 rgba(0, 0, 0, 1.5)。默认颜色 alpha 为 1 但 RGB 不同。",
  },
  {
    slug: "it/color-converter",
    inputs: { fgInput: "rgba(0, 0, 0, 0.5)", bgInput: "#ffffff" },
    clicks: ["calcContrast()"],
    expect: ["3.95:1"],
    ref: "IT-N47 对比度计入前景 alpha：50% 黑色叠白底等效 #808080，对比度 3.95:1；旧实现忽略 alpha 按纯黑计算得 21.00:1。",
  },
  {
    slug: "it/color-converter",
    inputs: { fgInput: "not-a-color", bgInput: "#ffffff" },
    clicks: ["calcContrast()"],
    expect: ["请输入有效颜色"],
    ref: "IT-N47 非法输入清理旧结果：无效颜色应清空比值并提示；旧实现直接 return，页面仍显示上一次的对比度结果。",
  },
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "1600000000000000" },
    clicks: ["convertTime()"],
    expect: ["2020-09-13T12:26:40.000Z"],
    ref: "IT-N40 微秒时间戳：16 位按微秒处理，1600000000000000 µs ÷ 1000 = 1600000000000 ms = 2020-09-13T12:26:40Z。旧实现只认 10–13 位，16 位直接报「无法解析时间」。默认输入 1700000000（秒）对应 2023-11-14，不命中。",
  },
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "2026-11-04" },
    clicks: ["convertTime()"],
    expect: ["解析口径：纯日期按浏览器本地时区 00:00:00 解析，不按 UTC 解释。"],
    ref: "IT-N41 纯日期按本地零点解析：YYYY-MM-DD 走本地解析分支并在结果区标注口径；旧实现按 UTC 解析且无任何提示。默认输入为 10 位时间戳，不命中。",
  },
  {
    slug: "it/ipv6-converter",
    inputs: { addr: "2001::db8::1" },
    clicks: ["calcTool()"],
    expect: ["转换结果 ⚠️ 不是合法的 IPv6 地址。"],
    ref: "IT-N53 多个连续 ::：RFC 4291 §2.2 规定 :: 只能出现一次，2001::db8::1 非法，应报错而非展开；旧实现只取第一个空段并静默展开成合法地址。默认地址 2001:db8::1 合法，不命中。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    checkIds: ["upper"],
    clicks: ["calc()"],
    expect: ["CRC-8/ITU (CCITT) 0x0A"],
    ref: "IT-N54 标准参数：CRC-8/ITU（poly 0x07、init 0x00、xorout 0x55）对 'abc' = 0x0A（标准校验值 '123456789' → 0xA1）。旧配置 init 0xFF + xorout 0x00 非标准，且名字误挂 CCITT。默认 input=123456789 且未勾大写，不命中。",
  },
  {
    slug: "it/css-minifier",
    inputs: { input: "a::after{content:\"a, b\"}" },
    clicks: ["minify()"],
    expect: ["content:\"a, b\""],
    ref: "IT-N60 字符串保护：压缩不得删掉 content 字符串内逗号后的空格；旧实现全局 \\s*([{}:;,])\\s* → 逗号规则把 \", \" 压成 \",\"（输出 content:\"a,b\"）。默认示例不含引号字符串，不命中。",
  },
  {
    slug: "it/css-minifier",
    inputs: { input: "a::after{content:\"a,b\"}" },
    clicks: ["beautify()"],
    expect: ["content:\"a,b\""],
    ref: "IT-N60 字符串保护（美化方向）：content 字符串内的逗号必须原样保留；旧实现把 \",\" 改写为 \", \"（输出 content:\"a, b\"）。默认示例不含引号字符串，不命中。",
  },
  {
    slug: "it/css-minifier",
    // IT-N61 回归：minify 必须尊重「移除注释」开关（修复前恒删注释，无视勾选状态）
    inputs: { input: "/*keep*/a{color:red}" },
    clicks: ["document.getElementById('removeComments').checked=false;minify();"],
    expect: ["/*keep*/"],
    ref: "修复前 minify() 把 keepComments 写死为 false，无论是否勾选都删注释；现读取 removeComments 复选框 ⇒ 未勾选时保留 /*keep*/。expect 取 /*keep*/，旧实现压缩后仅 a{color:red} 不含该串。默认示例不命中。",
  },
  {
    slug: "it/css-minifier",
    // IT-N62 回归：历史保存完整输入，loadH 恢复后 input 不被 60 字符截断（修复前 input.substring(0,60) → 恢复后尾段丢失）
    inputs: { input: ".box{color:red;width:100px;height:200px;margin:0 auto;padding:10px 20px;background:#fff;border:1px solid #ccc;}" },
    clicks: ["beautify();loadH(0);"],
    dumpIds: ["input"],
    expect: ["x;background:#fff;border:1px solid #ccc;}"],
    ref: "修复前 addToHistory 仅存 input.substring(0,60)，loadH 写回该摘要 ⇒ 第 60 字符后的内容（x;background:#fff;border:1px solid #ccc;}）被丢弃；修复后历史存完整 input，loadH 恢复全量。输入长 111 字符，尾部 token 仅在完整恢复时存在，旧实现被截断故不含该串。默认示例不命中。",
  },
  {
    slug: "it/css-minifier",
    // IT-N62 残留：loadH 只回填输入不重算，结果区残留上一次输出（用户会复制到错的 CSS）
    inputs: { input: "a{color:red}" },
    clicks: ["localStorage.setItem('css_minifier_history', JSON.stringify([{time:'2026-01-01 00:00:00',action:'压缩',op:'minify',summary:'#n62x',input:'#n62x { color : #aabbcc }'}]));document.getElementById('output').textContent='OLDOUT';loadH(0);"],
    dumpIds: ["output"],
    expect: ["n62x{color:#abc}"],
    ref: "N62 残留：loadH 原实现只把历史 input 写回输入框、不触发重算 ⇒ 结果区仍是上一次的输出（此处预置 OLDOUT）。修复后按历史 op='minify' 重算。expect 取压缩后的拼接形态「n62x{color:#abc}」（空白已压除 + #aabbcc 缩短为 #abc），输入回显为带空格的「#n62x { color : #aabbcc }」不含该串，旧实现输出为 OLDOUT 不含该串。",
  },
  {
    slug: "it/css-minifier",
    // IT-N62 残留（美化方向）：历史 op='beautify' 恢复后须按美化重算
    inputs: { input: "a{color:red}" },
    clicks: ["localStorage.setItem('css_minifier_history', JSON.stringify([{time:'2026-01-01 00:00:00',action:'美化',op:'beautify',summary:'#n62y',input:'#n62y{--zq:1}'}]));document.getElementById('output').textContent='OLDOUT';loadH(0);"],
    dumpIds: ["output"],
    expect: ["#n62y {"],
    ref: "N62 残留（美化方向）：loadH 须按历史 op='beautify' 走美化分支，输出 `#n62y {`（选择器与大括号间插空格并换行缩进）。expect 取「#n62y {」，输入回显为紧凑形态「#n62y{--zq:1}」不含该串，旧实现输出 OLDOUT 不含该串。",
  },
  {
    slug: "it/http-cache",
    // IT-N69 回归：搜索后「明细表」须按过滤结果统计（原 hcAgg 恒遍历 COMMANDS 全量）
    inputs: { searchInput: "Vary" },
    dumpIds: ["hcTbody"],
    expect: ["1 缓存键 1 Vary"],
    ref: "N69：搜索 `Vary` 后列表仅 1 项（分类=缓存键），明细表首行应为「1 / 缓存键 / 1」。原 hcAgg 遍历全量 33 条 ⇒ 首行是「1 请求/响应 6」、缓存键排第 7 行（文本为「7 缓存键 1 Vary」），故该拼接串在修复前不存在。默认无搜索词时为全量统计，不命中。",
  },
  {
    slug: "it/http-cache",
    // IT-N69 回归：筛选零命中时图表/明细表须同步清空并给出提示（原仍显示全量数据）
    inputs: { searchInput: "zzzz-no-such-directive" },
    dumpIds: ["hcTbody"],
    expect: ["当前筛选无匹配缓存指令，明细表已同步清空。"],
    ref: "N69：搜索一个必零命中的串后，明细表应为空并提示「当前筛选无匹配缓存指令，明细表已同步清空。」；修复前表格仍列出全部 11 个分类行、页面无任何「无匹配」提示。",
  },
  {
    slug: "it/date-duration",
    inputs: { d1: "2026-02-30", d2: "2026-03-02", inc: "excl" },
    clicks: ["calcTool()"],
    expect: ["日期无效：请填写真实存在的日历日期（如 2026-02-30 不存在）。"],
    ref: "IT-N63 非法日期：2026-02-30 不存在，应明确报错；旧实现由 Date 静默归一为 3 月 2 日，输出「相差 0 天」。默认 2026-01-01/2026-08-24 不命中。",
  },
  {
    slug: "it/date-duration",
    inputs: { d1: "2026-08-24", d2: "2026-01-01", inc: "excl" },
    clicks: ["calcTool()"],
    expect: ["结束日期早于开始日期，请调换起止日期。"],
    ref: "IT-N63 逆序保护：结束早于开始时应明确提示，而不是输出负数天数；旧实现得 -235 天并照常渲染。默认起止顺序正常，不命中。",
  },
  {
    slug: "it/date-duration",
    inputs: { d1: "2024-01-01", d2: "2024-01-02", inc: "incl" },
    clicks: ["calcTool()"],
    expect: ["口径：含结束当天（含首尾），天数已包含结束当天。"],
    ref: "IT-N63 文案与口径一致：含结束当天时卡片显示 2 天且提示「含结束当天」；旧实现卡片显示 2 天却写「不含结束当天 1 天」，自相矛盾。默认口径为 excl，不命中。",
  },
  {
    slug: "it/cron",
    clicks: ["document.getElementById('nextTimes').innerHTML = matchesCron(new Date(2026,10,8), '0', '0', '15', '*', '0') ? '日周OR命中' : '日周AND不命中';"],
    expect: ["日周OR命中"],
    ref: "IT-N76 日与周同时指定时按 Vixie cron 的 OR 语义：2026-11-08 为周日（getDay=0）但日期不是 15 号，day=15 + week=0 应命中；旧实现按 AND 判定为不命中。默认表达式为 * * * * *，输出不含该串。",
  },
  {
    slug: "it/url-encode",
    clicks: ["document.getElementById('baseUrl').value = 'https://example.com/page#top'; updateParam(0, 'q', 'key'); updateParam(0, '中文', 'value'); buildUrl();"],
    expect: ["https://example.com/page?q=%E4%B8%AD%E6%96%87#top"],
    ref: "IT-N80 查询串必须插在 #fragment 之前：base 含 #top 时结果应为 page?q=… #top；旧实现把查询串拼在整串末尾，得到 page#top?q=…。默认 baseUrl 为空，不命中。",
  },
  {
    slug: "it/url-encode",
    clicks: ["document.getElementById('baseUrl').value = 'https://example.com/?'; updateParam(0, 'q', 'key'); updateParam(0, 'a', 'value'); buildUrl();"],
    expect: ["https://example.com/?q=a"],
    ref: "IT-N80 末尾多余问号：base 以 ? 结尾时应规整为单个 ?，不能产出 ?&q=a；旧实现在含 ? 的 base 后追加 &，得到 https://example.com/?&q=a。默认 baseUrl 为空，不命中。",
  },
  {
    slug: "it/decimal-encode",
    inputs: { input: "Az", sep: "" },
    clicks: ["enc();"],
    expect: ["065122"],
    ref: "IT-N310：无分隔符时必须用定长 3 位（A=065、z=122 ⇒ 065122）才能反向还原；旧实现 join('') 得 65122，解码端无法还原。改用 Az：legacy 桩把 `<option value=' '>` 的默认分隔符 trim 成空串，与 sep='' 等价 ⇒ 原注入态与默认态输出完全相同（逃生）；默认正文的码点串不含 065122 ⇒ 不命中。",
  },
  {
    slug: "it/decimal-encode",
    inputs: { input: "65x 66" },
    clicks: ["var inp=document.getElementById('input'),out=document.getElementById('output'),ok=0;['65x 66','0x41 0x42','256 1'].forEach(function(v){out.value='KEEP';inp.value=v;try{dec();}catch(e){}if(out.value==='KEEP')ok++;});inp.value='72 101 108 108 111';out.value='';try{dec();}catch(e){}if(out.value==='Hello')ok++;document.getElementById('__tbProbe').textContent='N312STRICT '+ok;"],
    expect: ["N312STRICT 4"],
    ref: "IT-N312：解码必须用 /^\\d+$/ 整段校验——65x（尾部垃圾）、0x41（0x 前缀静默变 0）、256（越界）三种脏数据都必须拒绝且不改写输出，合法串仍须正常解码 Hello。旧实现 parseInt 宽松：65x→65、0x41→0，静默写出错误值。探针仅在注入 clicks 后出现，默认态零命中；ok 依赖 dec() 真实行为，非固定文案。",
  },
  {
    slug: "text/stats-1",
    inputs: { text: "😀" },
    expect: ["总字符数（含空白）： 1 总字符数（不含空白）： 1"],
    ref: "IT-N38：😀 是 1 个字素簇（UTF-16 记 2）。修复后 calc 用 Intl.Segmenter 按字素簇计数 ⇒ 总字符 1；旧实现 t.length=2。expect 为结果区连续串，默认中文样例不含 emoji ⇒ 不命中。",
  },
  {
    slug: "text/stats-1",
    inputs: { text: "𠮷 well-known" },
    expect: ["中文字符数： 1 英文单词数： 1"],
    ref: "IT-N38：𠮷（U+20BB7 扩展 B）须计入中文（旧 4E00–9FFF 漏计），well-known 须按连字符词计 1 个（旧正则拆成 2 个）。expect 锚结果区「中文1 英文1」连续串，默认样例不含扩展汉字与连字符词 ⇒ 不命中。",
  },
  {
    slug: "it/text-statistics",
    inputs: { textInput: "Version 3.14 is out" },
    clicks: ["document.getElementById('__tbProbe').textContent='N39SENT '+splitSentences('Version 3.14 is out').filter(function(s){return s.trim();}).length;"],
    expect: ["N39SENT 1"],
    ref: "IT-N39：小数 3.14 的句点不得当句末，splitSentences 须返回 1 段；旧实现（无该函数，analyze 内直接 /[。！？.!?]+/ 切）⇒ 2 段。策略：切句前把 \\d.\\d 的句点替换为哨兵再还原。探针仅注入 clicks 出现，默认态零命中。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "中文😀" },
    clicks: ["esc();"],
    expect: ["0001f600"],
    ref: "IT-N335：C 的 \\x 转义只表示单字节，非 ASCII 应改用 \\uXXXX/\\UXXXXXXXX；😀 码位 U+1F600 ⇒ \\U0001f600。旧实现只输出 \\xd83d\\xde00。默认 Hello 不出现。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "\\132\\132" },
    clicks: ["unesc();"],
    expect: ["ZZ"],
    ref: "IT-N336：\\132 八进制 = 1×64+3×8+2 = 90 = 'Z'（大写；'z' 是 122 = \\172）；旧实现 switch 的 case /[0-7]/ 是常量正则永不匹配，退化为输出字面数字。默认 Hello \"World\" 无 ZZ。",
  },
  {
    slug: "it/go-escape",
    inputs: { input: "\\172\\172" },
    clicks: ["unesc();"],
    expect: ["zz"],
    ref: "IT-N337：Go 八进制转义 \\172 = 'z'；旧实现八进制分支永不命中，反转义退化成字面数字。默认 Hello 无 zz。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: "\\172\\172" },
    clicks: ["unesc();"],
    expect: ["zz"],
    ref: "IT-N337：PHP 双引号字符串八进制 \\172 = 'z'；旧实现八进制分支永不命中。默认 Hello 无 zz。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: '"\\u{110000}"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\u{110000}"],
    ref: "PHP 反转义码点越界：U+110000 超出 Unicode 上限 0x10FFFF，旧实现 fromCodePoint 抛 RangeError 保留旧输出，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: '"\\xGG"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\xGG"],
    ref: "PHP 反转义 \\x 需要恰好两位十六进制；GG 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: '"\\uZZZZ"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\uZZZZ"],
    ref: "PHP 反转义 \\uXXXX 需要四位十六进制；ZZZZ 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "\\172\\172" },
    clicks: ["unesc();"],
    expect: ["zz"],
    ref: "IT-N337：Python 八进制转义 \\172 = 'z'；旧实现八进制分支永不命中，且 \\0 单独吞成 NUL。默认 Hello 无 zz。",
  },
  {
    slug: "it/html-escape",
    inputs: { input: "😀" },
    checkIds: ["escapeAll", "escapeQuote"],
    clicks: ["convert();"],
    expect: ["&#128512;"],
    ref: "IT-N339：全字符转义按码位而非 UTF-16 码元，emoji 必须是单个数值实体 &#128512;；旧实现 charCodeAt 拆成两个代理实体。默认示例为普通 HTML 文本，不出现该实体。",
  },
  {
    slug: "it/html-escape",
    inputs: { input: "\\\\n" },
    clicks: ["setFormat({dataset:{format:'js'},classList:{add:function(){},remove:function(){}}});setMode('unescape');convert();"],
    expect: ["\\n"],
    ref: "IT-N340：JS 反转义须先成对消费 \\\\，`\\\\n` 表示「反斜杠+n」两个字符；旧实现先跑 /\\\\n/→换行，把转义反斜杠误当真实换行，得到「反斜杠+换行」。默认 html-name 转义态不出现该串。",
  },
  {
    slug: "it/text-to-hex",
    inputs: { input: "Hi", sep: "\\x" },
    clicks: ["convert();"],
    expect: ["\\x48\\x69"],
    ref: "IT-N341：HTML 属性 value=\"\\\\x\" 得到 3 个字符（两个反斜杠+x），与 JS 的 2 字符字面量 '\\x' 恒不相等，旧实现走分隔符分支输出 48\\\\x69；改为单反斜杠后正确得到 \\x48\\x69。默认 Hello 输出不同。",
  },
  {
    slug: "it/text-to-octal",
    inputs: { input: "Hi", sep: "\\" },
    clicks: ["convert();"],
    expect: ["\\110\\151"],
    ref: "IT-N342：选项值 \"\\\\\\\\\" 是 2 字符，与 '\\' 恒不相等导致前缀丢失、反斜杠反被当分隔符；修正后 H=110、i=151 ⇒ \\110\\151。默认 Hello 输出不同。",
  },
  {
    slug: "it/hash",
    inputs: { textInput: "😀" },
    checks: ["md5"],
    clicks: ["calculateTextHashes()"],
    expect: ["2a02eac39d716a70ecf37579185927b6"],
    ref: "IT 哈希真实性：hashlib.md5('😀'.encode('utf-8')) = 2a02eac39d716a70ecf37579185927b6。旧实现自写 utf8Encode 按 UTF-16 码元处理代理对，emoji 被拆成两段三字节（CESU-8），摘要错误。",
  },
  {
    slug: "it/hash",
    inputs: { textInput: "The quick brown fox jumps over the lazy dog", hmacKey: "key" },
    checks: ["md5"],
    checkIds: ["hmacMode"],
    clicks: ["calculateTextHashes()"],
    expect: ["80070713463e7749b90c2dc24911e275"],
    ref: "IT 哈希真实性：HMAC-MD5(key='key', msg='The quick brown fox jumps over the lazy dog') = 80070713463e7749b90c2dc24911e275（RFC 2104 标准向量）。旧实现只显示占位串「HMAC-MD5 需手动实现」。",
  },
  {
    slug: "it/hash",
    inputs: {},
    clicks: ["document.getElementById('textInput').value='';calculateTextHashes()"],
    expect: ["请输入要计算哈希的文本"],
    ref: "IT 空输入行为：显式提示而非静默 return 保留上一次结果；旧实现清空输入后仍显示旧摘要。",
  },
  {
    slug: "it/hash-multi",
    inputs: {},
    clicks: ["document.getElementById('input').value='';calc()"],
    expect: ["请输入要计算哈希的文本"],
    ref: "IT 空输入行为：清空输入时给出提示并清空结果区；旧实现仅把结果区置空，用户看不出是「没算」还是「算完为空」。同时校正页面不再宣称支持未实现的 SHA-3。",
  },
  {
    slug: "it/octal-encode",
    inputs: { input: "150151" },
    clicks: ["dec()"],
    expect: ["hi"],
    ref: "IT 八进制往返：无分隔符编码 'hi' → '150151'，解码按 3 位定长切块还原 'hi'；旧实现把整串当 1 个数（parseInt('150151',8)=53577>255）直接报错。",
  },
  {
    slug: "it/octal-encode",
    inputs: {},
    clicks: ["document.getElementById('input').value='LEN='+document.getElementById('sep').options[3].value.length"],
    expect: ["LEN=1"],
    ref: "IT 双反斜杠 option：反斜杠分隔符的 value 必须只有 1 个字符；旧写法 value=\"\\\\\\\\\" 是 2 个字符（与单反斜杠永不相等、分隔符失效）。",
  },
  {
    slug: "it/octal-encode",
    inputs: { input: "\\150\\151" },
    clicks: ["dec()"],
    expect: ["hi"],
    ref: "IT 八进制往返：带前缀且反斜杠分隔的 \\150\\151 应还原 'hi'；旧实现先全局删掉「\\+3 位数字」的前缀，把分隔符一并吞掉，剩下 150151 当 1 个数报错。",
  },
  {
    slug: "it/text-to-unicode",
    inputs: { txt: "😀" },
    clicks: ["calcTool()"],
    expect: ["U+1F600", "\\uD83D\\uDE00"],
    ref: "IT 代理对：U+1F600 的 UTF-16 转义应为代理对 \\uD83D\\uDE00；旧实现只取 charCodeAt(0) 得到半个代理 \\uD83D。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: {},
    clicks: ["document.getElementById('smartInput').value='OFF='+zoneLabel('America/New_York',new Date(1705276800*1000)).slice(-1)"],
    expect: ["OFF=5"],
    ref: "IT 时区偏移：2024-01-15 UTC 的纽约为冬令时 UTC-5；旧实现用 new Date()（门禁冻结在 6 月）取偏移，全年显示 UTC-4。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { timestampSec: "1e20" },
    clicks: ["fromTimestamp('sec')"],
    expect: ["超出可表示范围"],
    ref: "IT 边界：超出 JS Date ±8.64e15 毫秒的时间戳要明确报错；旧实现继续渲染出 Invalid Date 与 NaN 字段。",
  },
  {
    slug: "it/string-obfuscator",
    inputs: { input: "😀ab", mode: "rev" },
    clicks: ["obfuscate()"],
    expect: ["ba😀"],
    ref: "IT 组合字符/代理对：反转应按码点而非 UTF-16 码元，'😀ab' → 'ba😀'；旧实现 split('') 反转后代理对顺序颠倒，得到非法半个字符。",
  },
  {
    slug: "it/string-obfuscator",
    inputs: { input: "😀", mode: "entity" },
    clicks: ["obfuscate()"],
    expect: ["&#128512;"],
    ref: "IT 实体编码：emoji 应输出码点实体 &#128512;；旧实现按 code unit 输出 &#55357;&#56832; 两个代理半体。",
  },
  {
    slug: "it/rot-cipher",
    inputs: { input: "a", mode: "custom", shift: "-1" },
    clicks: ["enc()"],
    expect: ["z"],
    ref: "IT 负位移：自定义位移 -1 时 'a' 应回绕为 'z'；旧实现 (0-1)%26=-1 → 输出 '`'（反引号）。",
  },
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "100000000000" },
    clicks: ["convertTime()"],
    expect: ["1973-03-03T09:46:40.000Z"],
    ref: "IT epoch 单位：12 位毫秒戳（2001-09-09 之前不足 13 位）应识别为毫秒 = 1973-03-03T09:46:40Z；旧实现漏判后交给 new Date('100000000000') 解析，直接报无法解析。",
  },
  {
    slug: "it/text-truncate",
    inputs: { input: "e\u0301XY", mode: "chars", limit: "2", ellipsis: "…" },
    clicks: ["truncate()"],
    expect: ["e\u0301…"],
    ref: "IT 组合字符：按字符截断必须以字素簇为单位，'e'+U+0301 不能被拆开；旧实现 Array.from 按码点切分，limit=2 时输出 'e…' 丢失重音。",
  },
  {
    slug: "it/text-to-decimal",
    inputs: { input: "中", encoding: "ascii" },
    clicks: ["convert()"],
    expect: ["ASCII 模式只支持"],
    ref: "IT 编码真实性：ASCII 模式遇非 ASCII 字符应明确拒绝并提示改用 UTF-8；旧实现 code&0xff 把 '中' 静默截成 45，输出与原文不对应。",
  },
  {
    slug: "it/text-to-decimal",
    inputs: { inputDec: "300" },
    clicks: ["convertDecToText()"],
    expect: ["非法十进制值"],
    ref: "IT 往返：十进制解码遇 300（超出 0–255）应报错；旧实现静默丢弃该 token，输出空串，用户无法察觉数据丢失。",
  },
  {
    slug: "it/text-statistics",
    inputs: { textInput: "😀e\u0301" },
    clicks: ["document.getElementById('result').innerHTML='GP='+graphemeCount('😀e\\u0301')+'/CP='+Array.from('😀e\\u0301').length;"],
    expect: ["GP=2/CP=3"],
    ref: "字素簇口径：'😀'（1 个字素/1 码点/2 码元）+ 'e'+U+0301（1 个字素/2 码点）合计字素 2、码点 3；旧实现 totalChars 取 UTF-16 length=4。",
  },
  {
    slug: "it/text-similarity",
    inputs: { textA: "😀abc", textB: "abc" },
    expect: ["75.00%"],
    ref: "字素/码点口径：A='😀abc' 按码点长度 4、B='abc' 长度 3，编辑距离 1 ⇒ 1−1/4=75.00%；旧实现按 UTF-16 码元（A 长 5、距离 2）得 60.00%。默认空输入为 0%，不命中。",
  },
  {
    slug: "it/text-diff",
    inputs: { text1: "😀", text2: "x", charDiff: true },
    clicks: ["document.getElementById('unifiedDiff').textContent='N='+(charDiffLine('😀','x').oldHtml.match(/line-through/g)||[]).length;"],
    expect: ["N=1"],
    ref: "代理对：逐字符 diff 必须把 '😀' 当一个单位，与 'x' 比较只有 1 段删除；旧实现 split('') 拆成两个代理半体，产生 2 段 line-through。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "😀" },
    clicks: ["convert();document.getElementById('output').value='LEN='+document.getElementById('output').value.length;"],
    expect: ["LEN=2"],
    ref: "代理对：Array.from 后 emoji 保持一个码点（UTF-16 length=2）；旧实现 split('') 把两个代理半体用空格拼接，长度 5。",
  },
  {
    slug: "it/case-converter",
    inputs: { inputText: "😀😀" },
    expect: ["2 字符"],
    ref: "字素簇口径：两个 emoji 是 2 个可见字符，统计区显示「2 字符」；旧实现 text.length 得 4 字符。默认样例 11 字符，不含「2 字符」⇒ 强判别。",
  },
  {
    slug: "it/text-replace",
    inputs: { sourceText: "😀", findInput: "😀", replaceInput: "😁😁" },
    clicks: ["document.getElementById('optRegex').checked=false;doReplace();document.getElementById('charDelta').textContent='DELTA='+document.getElementById('charDelta').textContent;"],
    expect: ["DELTA=+1"],
    ref: "字素/码点口径：'😀'→'😁😁' 按码点由 1 增至 2，字符变化 +1；旧实现按 UTF-16 长度 2→4 得 +2。",
  },
  {
    slug: "it/json-schema-validator",
    inputs: { schema: '{"type":"object"}', data: "null" },
    clicks: ["validateJSON()"],
    expect: ["类型不匹配"],
    ref: "JSON 语义：字符串 null 是合法 JSON 值，应在解析成功后被判为「类型不匹配 root: 期望 object」；旧实现 parseSafely 失败返回 null 并判定「JSON 格式错误」，不会出现类型不匹配文案。默认样例（合法对象）校验通过，不命中。",
  },
  {
    slug: "it/yaml-validator",
    inputs: {},
    clicks: ["var d={},c=d;for(var i=0;i<300;i++){c.a={};c=c.a;}var st=analyzeDocs([d]);document.getElementById('jsonOutput').textContent='DEEP='+st.tooDeep;"],
    expect: ["DEEP=true"],
    ref: "深度上限：300 层嵌套超过 analyzeDocs 的 200 层统计上限，应标记 tooDeep 并停止递归；旧实现无上限、会继续深递归（更深输入可栈溢出）。默认样例仅数层，不命中。",
  },
  {
    slug: "it/json-path",
    inputs: {},
    clicks: ["var o={},c=o;for(var i=0;i<5000;i++){c.x={};c=c.x;}c.x=1;var out=[];collectRecursive(o,'x',false,out,0);document.getElementById('output').textContent='N='+out.length;"],
    expect: ["N=65"],
    ref: "递归上限：5000 层对象在 collectRecursive 深度 65 处截断，收集到 65 个 x；旧实现无深度上限，递归回溯栈溢出导致点击执行抛错、无输出。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":"<img src=x onerror=N490MARK>"}', path: "$.a" },
    clicks: ["doQuery()"],
    expect: ['"&lt;img src=x onerror=N490MARK&gt;"'],
    ref: "IT-N490 DOM XSS：JSON 字符串里的 `<img …>` 必须先做 HTML 转义再着色 ⇒ 输出为文本 `&lt;img …&gt;`。修复前 highlightJSON 直接拼 innerHTML，标签被解析成真实 img 元素（渲染即触发 onerror）；blob 采集会剥掉 `<img …>` 标签，故修复前的输出里根本不含带 `&lt;` 的串。哨兵 N490MARK 由输入决定。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":[11,22,33]}', path: "$.a[-1:]" },
    clicks: ["doQuery()"],
    expect: ["[ 33 ]"],
    ref: "IT-N489 开区间切片：`[-1:]` 负起点折算为 length−1=2、省略上界按 length 收敛 ⇒ 只取末项 33，输出 `[ 33 ]`。修复前解析写入 `end=Infinity`，执行阶段 `i < Infinity` 恒真 ⇒ 死循环冻结页面（点击不返回、无输出）。输入为紧凑 JSON（含 `33` 但无 `[ 33 ]` 形态），默认示例不命中。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":[11,22,33,44,55]}', path: "$.a[0:5:2]" },
    clicks: ["doQuery()"],
    expect: ["[ 11 , 33 , 55 ]"],
    ref: "IT-N489 步长：`[0:5:2]` 应取下标 0/2/4 ⇒ `[ 11 , 33 , 55 ]`。修复前 `endStr='5:2'` 交给 parseInt 得 5、`step` 缺省为 1 ⇒ 输出 5 项 `[ 11 , 22 , 33 , 44 , 55 ]`，与本串不同。",
  },
  {
    slug: "it/xml-validator",
    inputs: {},
    clicks: ["document.getElementById('result').textContent='LOC='+xmlErrorLoc('error on line 3 at column 5: mismatched tag');"],
    expect: ["LOC=（第 3 行，第 5 列）"],
    ref: "错误定位：Chrome 的 parsererror 文案「line 3 at column 5」应被提取为结构化行列；旧实现只原样贴整段英文错误文本。",
  },
  {
    slug: "it/base32-encode",
    inputs: { input: "😀" },
    clicks: ["encode32()"],
    expect: ["6CPZRAA="],
    ref: "基数编码边界（非 BMP 字符）：UTF-8 字节 F0 9F 98 80 的标准 Base32 为 6CPZRAA=（Python base64.b32encode 独立核对，RFC 4648）。页面按码点遍历不拆坏 emoji，旧式按 UTF-16 代理对处理会得到两段错误码。",
  },
  {
    slug: "it/base85-encode",
    inputs: { input: "😀" },
    clicks: ["enc()"],
    expect: ["<~n=Q(u~>"],
    ref: "Ascii85 边界：UTF-8 四字节 F0 9F 98 80 一组压成 n=Q(u，Adobe 包裹 <~…~>（Python base64.a85encode(adobe=True) 独立核对）。默认模式即 Ascii85 ⇒ 无需切档。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "😀" },
    checkIds: ["upper"],
    clicks: ["enc()"],
    expect: ["=F0=9F=98=80"],
    ref: "QP 边界：非 ASCII 字节一律编成 =XX；页面「大写十六进制」默认勾选（HTML checked），harness 的 checkbox 桩恒 false，故用 checkIds 还原真机默认态。Python quopri.encodestring 独立核对为 =F0=9F=98=80（大写形态）。",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: "😀" },
    clicks: ["document.getElementById('mode').value='decimal';enc()"],
    expect: ["&#128512;"],
    ref: "实体编码边界：十进制模式按码点（而非 UTF-16 码元）输出 &#128512;（U+1F600 = 128512）；按码元实现的旧班会拆成两个代理对实体。默认 named 模式对 emoji 回退十进制，但串形不同。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "xn--fiq228c.a_b" },
    clicks: ["dec()"],
    expect: ["中文.a_b"],
    ref: "解码边界：xn-- 标签解回中文；纯 ASCII 标签 a_b 含下划线，不在 Punycode 数字字符表（a-z/0-9/-）内，不可能是裸 Punycode ⇒ 两种勾选态下都必须原样保留。旧实现对无前缀标签一律 decode('a_b')（非法数字直接抛错），本串不命中。",
  },

  // ---- 编码/转义族可逆性矩阵（BATCH：标准解码器交叉验证） ----
  {
    slug: "it/base64-converter",
    inputs: { input: "\u0000" },
    clicks: ["document.getElementById('urlSafe').parentElement.style={};setAlgo('base85');encodeText();"],
    expect: ["<~!!~>"],
    ref: "Base85 边界（全零末组）：单个 NUL（UTF-8 00）不足 4 字节，标准 Ascii85 编码为 <~!!~>（Python base64.a85encode(b'\\x00', adobe=True) 独立核对）。旧实现把任意全零组都缩写成 'z'，再按末组截断把 'z' 裁掉 ⇒ <~~>，解码丢字节。默认输入 hello world 不含 NUL。",
  },
  {
    slug: "it/base85-encode",
    inputs: { input: "\u0000" },
    clicks: ["enc()"],
    expect: ["<~!!~>"],
    ref: "同族交叉验证（另一页实现）：base85-encode 的全零末组本就正确（仅完整 4 字节组才用 'z'）⇒ <~!!~>；与 base64-converter 的修复后产物逐字节一致。Python base64.a85encode(adobe=True) 独立核对。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=1g", output: "KEEP-QP-MALFORMED" },
    clicks: ["dec()"],
    expect: ["KEEP-QP-MALFORMED"],
    ref: "QP 解码严格性：=1g 不是两位十六进制，标准解码器必须报错；旧实现 parseInt('1g',16) 返回 1、parseInt('4',16) 返回 4，静默解成 U+0001/U+0004。错误分支只提示、不改写输出 ⇒ 预设哨兵串保留即证明未误改。",
  },
  {
    slug: "it/base32-encode",
    inputs: { input: "MZXR", output: "KEEP-B32-PAD" },
    clicks: ["decode32()"],
    expect: ["KEEP-B32-PAD"],
    ref: "RFC 4648 填充位：MZXR 末组剩 4 位且低 4 位为 1（R=17），标准解码器应拒绝；旧实现直接吐出字节 'fo' 的等价物（value >>> 越界位被忽略）。错误分支不改写输出 ⇒ 哨兵保留。",
  },
  {
    slug: "it/base32-encode",
    inputs: { input: "M", output: "KEEP-B32-LEN" },
    clicks: ["decode32()"],
    expect: ["KEEP-B32-LEN"],
    ref: "RFC 4648 长度：5 个符号模 8 余 1，末组不足一字节，标准解码器应拒绝（旧实现静默输出空串）。用哨兵验证未被改写。",
  },
  {
    slug: "it/go-escape",
    inputs: { input: "ab", output: "KEEP-GO-RUNE" },
    clicks: ["document.getElementById('kind').value='rune';esc()"],
    expect: ["KEEP-GO-RUNE"],
    ref: "Go rune 字面量必须恰好一个 rune；'ab'、'éü' 这类多字符产物无法通过 go 编译。旧实现照样输出 'ab'。新增校验走 alert 早退、不改写输出 ⇒ 哨兵保留。",
  },
  {
    slug: "it/go-escape",
    inputs: { input: "\u0000" },
    clicks: ["esc()"],
    expect: ["\\x00"],
    ref: "Go 字符串 NUL：Go 的八进制转义必须写满 3 位，\\0 单独不合法；页面走 \\x00（定长两位十六进制）⇒ 产物 \"\\x00\"。默认 Hello 不含 NUL。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: 'r#"q\'""#' },
    clicks: ["unesc()"],
    expect: ["q'\""],
    ref: "Rust 原始字符串反转义：r#\"…\"# 的闭合符是 \"# 而非裸 \"；旧实现只判 text.endsWith('\"')，遇末尾 # 判定失败、原样回显。切片按 2+井号数 起点、去掉尾部 井号数+1 个字符 ⇒ q'\"。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: "é", output: "KEEP-RUST-BYTE" },
    clicks: ["document.getElementById('kind').value='byte';esc()"],
    expect: ["KEEP-RUST-BYTE"],
    ref: "Rust 字节字符串 b\"…\" 只允许 ASCII 与转义，直接写非 ASCII 字符（或 b\"\\u{{…}}\"）无法编译；旧实现输出 b\"é\"。新增校验 alert 早退、不改写输出 ⇒ 哨兵保留。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: "ab", output: "KEEP-RUST-CHAR" },
    clicks: ["document.getElementById('kind').value='char';esc()"],
    expect: ["KEEP-RUST-CHAR"],
    ref: "Rust char 字面量必须恰好一个 Unicode 标量；旧实现把 'ab'、'éü' 原样/拆分塞进单引号，javac 等价地无法编译。校验后哨兵保留。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: "\u0007" },
    clicks: ["document.getElementById('kind').value='byte';esc()"],
    expect: ["b\"\\x07\""],
    ref: "Rust 字节串控制字符：b\"…\" 不支持 \\u{{…}}，必须用 \\xNN；BEL 码位 7 ⇒ b\"\\x07\"。旧实现输出 b\"\\u{{7}}\"，rustc 报 unknown character escape。默认 Hello 不含 BEL。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: '"\\u{110000}"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\u{110000}"],
    ref: "Rust Unicode 标量上限 0x10FFFF；旧实现 fromCodePoint(U+110000) 抛 RangeError 保留旧输出，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: '"\\u{D800}"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\u{D800}"],
    ref: "Rust Unicode scalar value 排除代理区 D800–DFFF；旧实现 output 得到孤立代理，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: '"\\xGG"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\xGG"],
    ref: "Rust \\x 需要恰好两位十六进制；GG 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "line1\nline2" },
    clicks: ["document.getElementById('mode').value='raw';document.getElementById('qtype').value='double';esc()"],
    expect: ["line1\\nline2"],
    ref: "Python raw 回退：单/双引号 raw 串不能跨行，含真实换行的文本必须退回普通转义 ⇒ \"line1\\nline2\"（ast.literal_eval 实测等价）。旧实现输出 r\"line1<换行>line2\"，Python 报 unterminated string literal。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "\u0000" },
    clicks: ["document.getElementById('mode').value='raw';document.getElementById('qtype').value='double';esc()"],
    expect: ["\\x00"],
    ref: "Python raw 回退（NUL）：Python 词法器拒收源码中的 null 字节，raw 串里也不能直接含 NUL ⇒ 退回 \\x00。ast.literal_eval 实测等价；旧实现输出含裸 NUL 的 r\"…\"，compile 直接失败。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: '"\\U00110000"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\U00110000"],
    ref: "Python \\U 八位十六进制码点上限 U+10FFFF；旧实现 fromCodePoint 抛 RangeError 保留旧输出，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: '"\\xGG"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\xGG"],
    ref: "Python \\x 需要恰好两位十六进制；GG 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: '"\\uZZZZ"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\uZZZZ"],
    ref: "Python \\u 需要恰好四位十六进制；ZZZZ 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "red\\nblue" },
    clicks: ["unesc();"],
    expect: ["red blue"],
    ref: "Python raw 前缀必须紧邻有效引号：`red\\nblue` 是普通标识符开头，不是 raw 串，\\n 应解析为真实换行（harness 把结果区换行折叠为空格，故 expect 取转换后形态 `red blue`，非输入回显）。旧实现无条件去掉首字母 r，输出 `ed\\nblue` ⇒ 折叠后 `ed blue`，不命中。默认 Hello 不命中。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "\u0001A" },
    clicks: ["esc()"],
    expect: ["\\001A"],
    ref: "C 十六进制转义贪婪：\\x 会吞掉后续所有十六进制字符（\"\\x01A\" = 0x1A），故下一字符是 A–F/0–9 时改用最多 3 位八进制 \\001 ⇒ 字节 0x01 后跟 'A'。cc -std=c11 编译实测字节序列 01 41 与原文一致。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "éA" },
    clicks: ["esc()"],
    expect: ["\\u00e9A"],
    ref: "C 非 ASCII：0xA0–0xFF 必须用 \\u 通用字符名（\\u00e9）而非单字节 \\xe9，否则 cc 按执行字符集得到的字节与 UTF-8 原文不符；cc -fexec-charset=UTF-8 实测 c3 a9 41。旧实现输出 \\xe9A（且 A 会被 \\x 贪婪吞成超范围值）。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: "\u00008" },
    clicks: ["esc()"],
    expect: ["\\x00"],
    ref: "JS NUL 边界：\\0 后紧跟十进制数字会变成 \\08 等遗留八进制转义（严格模式 SyntaxError）；改用定长两位 \\x00 ⇒ \"\\x008\"，vm.runInNewContext 严格模式实测可解析且值为 NUL+'8'。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: '"\\u{110000}"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\u{110000}"],
    ref: "JS \\u{...} 码点上限 U+10FFFF；旧实现 fromCodePoint 抛 RangeError 保留旧输出，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: '"\\xGG"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\xGG"],
    ref: "JS \\x 需要恰好两位十六进制；GG 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: '"\\uZZZZ"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\uZZZZ"],
    ref: "JS \\uXXXX 需要四位十六进制；ZZZZ 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/java-escape",
    inputs: { input: '"\\uZZZZ"' },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\uZZZZ"],
    ref: "Java \\uXXXX 必须恰好四位十六进制；ZZZZ 非法时旧实现 parseInt→NaN 抛 RangeError，修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/java-escape",
    inputs: { input: "\\u" },
    clicks: ["unesc();"],
    expect: ["⚠️ 非法转义：\\u"],
    ref: "Java \\u 后缺位时旧实现 parseInt('')→NaN 抛 RangeError 保留旧输出；修复后显示绑定原片段的错误提示。默认 Hello 不命中。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: "a\u001b", mode: "double" },
    clicks: ["esc()"],
    expect: ["a\\e"],
    ref: "PHP 双引号 ESC：\\e 是 ESC（0x1B）专用转义；旧实现 case '\\e'（JS 里等于字符 e）把每个 e 误转义成 \\e，会得到 \\ea\\e 这类串味产物。默认样例不含 ESC。",
  },
  {
    slug: "it/sql-escape",
    inputs: { input: "\u001a" },
    clicks: ["esc()"],
    expect: ["\\Z"],
    ref: "MySQL 转义集完整性：mysql_real_escape_string 要求转义 Ctrl-Z（0x1A）为 \\Z；页面已覆盖 NUL/\\n/\\r/\\Z/引号/反斜杠六类必需字符。默认 O'Brien 样例不含 Ctrl-Z。",
  },

  // —— 时间族 / 进制族 / 字符集族：独立标准实现交叉验证（2026-11-04 批次）——
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "-86400" },
    clicks: ["convertTime()"],
    expect: ["1969-12-31T00:00:00.000Z"],
    ref: "负时间戳（1970 前）：-86400 秒 = 1969-12-31T00:00:00Z。旧实现用 /^\\d+$/ 判定，负号串漏进 new Date('-86400')，被当成 ISO 年份 -86400（输出 +086400-01-01）。默认 1700000000 不命中。",
  },
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "17000000000000000000" },
    clicks: ["convertTime()"],
    expect: ["无法解析时间"],
    ref: "位数越界：20 位超出纳秒档（≤19 位），必须明确报错；旧实现对 >13 位一律按「纳秒」截断前 13 位，会把越界值静默算成 2023 年。",
  },
  {
    slug: "it/number-base-converter",
    inputs: { batchInput: "0x10\n10", batchFrom: "10", batchTo: "2" },
    clicks: ["doBatchConvert()"],
    expect: ["无效 1010"],
    ref: "十进制分支必须只认 0-9：BigInt('0x10') 会按 JS 字面量规则算成 16，导致十进制模式悄悄接受十六进制前缀，而十六进制模式又把 '0x10' 判为非法（两条路径自相矛盾）⇒ 批量十进制→二进制须输出「无效 1010」。改走批量分支：legacy 桩把 `<option value='5' selected>` 误解析为首个 option（inputBase=2），255 在二进制非法 ⇒ 默认态同样输出「无效」（逃生）。",
  },
  {
    slug: "it/integer-base-converter",
    inputs: { num: "-255", fromBase: "10", toBase: "16" },
    expect: ["-ff"],
    ref: "负号支持：-255(10) = -ff(16)，与 number-base-converter 的口径对齐；旧实现按位扫描时 '-' 被判为非法数字位直接抛错，且 fromBigInt 对负数返回空串。默认 255 输出 ff，不命中。",
  },
  {
    slug: "it/integer-base-converter",
    // IT-N48-a 回归：非法输入须清空全部结果卡片，不得保留上一次的旧值供复制。
    clicks: ["var n=document.getElementById('num'),f=document.getElementById('fromBase'),t=document.getElementById('toBase');f.value='16';t.value='10';n.value='ff';convert();var had=document.getElementById('r2').textContent!=='—';n.value='1g';convert();var ids=['r2','r8','r10','r16','r32','r36'],clr=ids.every(function(id){return document.getElementById(id).textContent==='—';});document.getElementById('__tbProbe').textContent='STALECLR '+(had&&clr&&document.getElementById('mainOut').textContent==='❌'?'OK':'BAD');"],
    expect: ["STALECLR OK"],
    ref: "状态链探针：先以合法 ff(16) 转换令六卡片有值（had），再以非法 1g(16) 转换，要求六卡片全部回到『—』且主输出 ❌。修复前 catch 只置主输出 ❌、六卡片仍保留 ff 的旧值 ⇒ clr=false ⇒ STALECLR BAD。默认态首屏即 ff/16→10 合法态、无第二次非法转换动作 ⇒ 不命中。",
  },
  {
    slug: "it/integer-base-converter",
    // IT-N48-b：基数越界须保留用户输入并明确报错，不得静默 clamp 写回输入框。
    inputs: { num: "ff", fromBase: "99", toBase: "10" },
    clicks: ["convert();document.getElementById('__tbProbe').textContent='BASEKEEP '+document.getElementById('fromBase').value;"],
    expect: ["源进制与目标进制都必须是 2 到 36 的整数", "BASEKEEP 99"],
    ref: "注入越界源进制 99：修复后输出明确报错且输入框保留 99 ⇒ 探针 BASEKEEP 99；旧实现 clamp 到 36 并写回输入框、无任何提示 ⇒ 两锚均不命中。默认态 16→10 合法，不命中。",
  },
  {
    slug: "it/charset-detector",
    inputs: { txt: "C4 E3 BA C3" },
    expect: ["共 4 字节", "无法仅凭字节区分"],
    ref: "字节模式：0xC4 0xE3 0xBA 0xC3 在 GB18030 下解出「你好」，Big5 下解出「斕疑」，两者均可严格解码且可读性并列 ⇒ 页面必须明确输出并列结论而非硬猜（Node TextDecoder 实测：utf-8 报非法序列、gb18030=你好、big5=斕疑）。",
  },
  {
    slug: "it/charset-detector",
    inputs: { txt: "EF BB BF E4 BD A0" },
    expect: ["识别到 UTF-8 BOM", "最可能为"],
    ref: "BOM 识别：EF BB BF 为 UTF-8 BOM，剥除后 3 字节 E4 BD A0 严格解码为「你」；GB18030 在剩余 0xA0 处非法、Big5 亦失败 ⇒ UTF-8 唯一可解，给唯一结论。默认示例非字节串，不命中。",
  },
  // ── 哈希族深度（2026-11-04）：每个期望值均由 Python hashlib / hmac / zlib 或独立位级 CRC 实现产出 ──
  {
    slug: "it/md5",
    inputs: { hmacKey: "key", hmacInput: "The quick brown fox jumps over the lazy dog" },
    clicks: ["calcHmac()"],
    expect: ["80070713463e7749b90c2dc24911e275"],
    ref: "Python hmac.new(b'key', b'The quick brown fox jumps over the lazy dog', hashlib.md5).hexdigest() = 80070713463e7749b90c2dc24911e275（RFC 2202 用例 1）。默认 hmacKey=mysecret / hmacInput='Hello, HMAC-MD5!' 的摘要不同，不命中。",
  },
  {
    slug: "it/md5",
    inputs: { hmacKey: "a".repeat(80), hmacInput: "hello" },
    clicks: ["calcHmac()"],
    expect: ["998d524a20c67f1f4463653778ff4aa9"],
    ref: "Python hmac.new(b'a'*80, b'hello', hashlib.md5) = 998d524a…（RFC 2104：密钥长度 >64 字节须先取 MD5 原始 16 字节摘要再补块；若把 80 字节直接截断或补零，得到的是另一个值）。",
  },
  {
    slug: "it/md5",
    inputs: { textInput: "中文" },
    checkIds: ["uppercase"],
    clicks: ["calcText()"],
    expect: ["A7BAC2239FCDCB3A067903D8077C4A07"],
    ref: "IT-N239：hashlib.md5('中文'.encode('utf-8')) = a7bac2239fcdcb3a067903d8077c4a07，大写开关 ⇒ 整串大写。UTF-8 勾选框已移除、md5() 恒按 UTF-8 字节串计算（与文件哈希/HMAC/主流实现一致）；uppercase 在 HTML 默认勾选而 harness 桩默认 false，故显式 checkIds 还原真机首屏态。旧实现取消勾选时按 UTF-16 码元无掩码拼字节得到 c2981cdd…（非任何标准编码），可判别口径错误。",
  },
  {
    slug: "it/sha",
    inputs: { textInput: "abc" },
    checks: ["SHA-384"],
    clicks: ["calcText()"],
    expect: ["cb00753f45a35e8bb5a03d699ac65007272c32ab0eded1631a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7"],
    ref: "NIST/hashlib.sha384(b'abc') = cb00753f…4c825a7。默认只勾 SHA-256，本例换成 SHA-384 以覆盖 384 位路径。",
  },
  {
    slug: "it/sha",
    inputs: { textInput: "abc" },
    checks: ["SHA-512"],
    checkIds: ["uppercase"],
    clicks: ["calcText()"],
    expect: ["DDAF35A193617ABACC417349AE20413112E6FA4E89A97EA20A9EEEE64B55D39A2192992A274FC1A836BA3C23A3FEEBBD454D4423643CE80E2A9AC94FA54CA49F"],
    ref: "hashlib.sha512(b'abc') = ddaf35a1…4ca49f（NIST 向量），uppercase 打开 ⇒ 全大写。与 SHA-384 例互不命中。",
  },
  {
    slug: "it/hmac-generator",
    inputs: { key: "Jefe", msg: "what do ya want for nothing?" },
    clicks: ["calc()"],
    expect: ["HMAC-SHA256 5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"],
    ref: "RFC 4231 测试用例 2：HMAC-SHA-256('Jefe', 'what do ya want for nothing?') = 5bdcc146…ec3843（Python hmac 逐字节同值）。默认 key=secret-key / msg='Hello, HMAC!'，不命中。",
  },
  {
    slug: "it/hmac-generator",
    clicks: ["var b=Array.from(getKeyBytes('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b','hex'));var ok=b.length===16&&b.every(function(x){return x===11;});document.getElementById('__tbProbe').textContent='HEXKEY '+(ok?'OK':'BAD:'+b.length);"],
    expect: ["HEXKEY OK"],
    ref: "IT-N280：getKeyBytes(key,'hex') 须把 32 位 hex 解成 16 个 0x0b 字节（RFC 4231 长密钥场景）。修复前仅 TextEncoder 按文本编码，得 32 个 ASCII 码（首字节 0x30）⇒ HEXKEY BAD。",
  },
  {
    slug: "it/hmac-generator",
    clicks: ["var s=String(__hmac_generatorResText);var ok=s.indexOf('results')>=0&&s.indexOf('.result-box')<0;document.getElementById('__tbProbe').textContent='RESTXT '+(ok?'OK':'BAD');"],
    expect: ["RESTXT OK"],
    ref: "IT-N279：ResText 须读 #results 的结果卡摘要，不得取页面首个 .result-box 算法说明卡。修复前源码取 .result-box、不含 results ⇒ RESTXT BAD（改用函数源码特征探针，规避 harness stub 不完整的 DOM 注入能力）。",
  },
  {
    slug: "it/hmac-generator",
    clicks: ["var s=String(__hmac_generatorPresets);var ok=s.indexOf('calc')>=0&&s.indexOf('copyAll')<0;document.getElementById('__tbProbe').textContent='KEYRECALC '+(ok?'OK':'BAD');"],
    expect: ["KEYRECALC OK"],
    ref: "IT-N281：预设 after 回调须指向重算 calc()，不得是纯复制 copyAll()。修复前 preset 源码含 copyAll、不含 calc ⇒ KEYRECALC BAD（JSDOM 真机另验 key oninput 绑定）。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    checkIds: ["upper"],
    clicks: ["calc()"],
    expect: ["CRC-16/CCITT-FALSE (IBM-3740) 0x514A", "CRC-16/Modbus 0x5749", "CRC-32 0x352441C2", "CRC-64/ECMA-182 0x66501A349A0E0855"],
    ref: "独立位级 CRC 实现（Python，参数取 reveng 目录）：'abc' ⇒ CCITT-FALSE 0x514A、Modbus 0x5749、CRC-32 0x352441C2（zlib.crc32 交叉核对）、CRC-64/ECMA-182 0x66501A349A0E0855。默认 input=123456789 与各值不同，不命中。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "48 65 6c 6c 6f" },
    checkIds: ["upper", "hexInput"],
    clicks: ["calc()"],
    expect: ["CRC-32 0xF7D18982", "CRC-64/ECMA-182 0xFFAD3236B47900AB"],
    ref: "可逆性对照：十六进制输入 48 65 6c 6c 6f 即 'Hello' 的 ASCII 字节。Python zlib.crc32(b'Hello')=0xf7d18982、CRC-64/ECMA-182(b'Hello')=0xffad3236b47900ab；与文本模式同输入同值，证明字节解析口径正确。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "ABC" },
    checkIds: ["hexInput"],
    clicks: ["calc()"],
    expect: ["十六进制输入须为偶数位、且仅含 0-9 / A-F。"],
    ref: "哈希族可逆性：3 位十六进制旧实现 new Uint8Array(1.5) 被截断成 1 字节、末尾 'C' 静默丢弃并照常输出 CRC（错误值）。修正后明示拒绝；默认输入为十进制文本且未勾 hexInput，不命中。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "48zz" },
    checkIds: ["hexInput"],
    clicks: ["calc()"],
    expect: ["十六进制输入须为偶数位、且仅含 0-9 / A-F。"],
    ref: "非十六进制字符旧实现 parseInt('zz',16)=NaN → 0x00，静默把 'zz' 当空字节算出 CRC。修正后拒绝；与奇数位例分别覆盖两条校验分支。",
  },
  {
    slug: "it/hash-identifier",
    inputs: { h: "5d41402abc4b2a76b9719d911017c592" },
    clicks: ["calcTool()"],
    expect: ["MD5 128 位（32 位十六进制）", "NTLM 32 位十六进制（Windows 口令哈希）"],
    ref: "32 位十六进制同时是 MD5 与 NTLM 的形态（本页 FAQ 已声明）⇒ 应并列两个候选；默认值 5e884898… 是 64 位，不命中。旧实现只给 MD5。",
  },
  {
    slug: "it/hash-identifier",
    inputs: { h: "352441c2" },
    clicks: ["calcTool()"],
    expect: ["CRC-32 32 位校验（8 位十六进制）"],
    ref: "8 位十六进制 = CRC-32（Python zlib.crc32(b'abc') = 0x352441c2）。旧长度表缺 8 ⇒ 只输出「未知」，属漏判。",
  },
  {
    slug: "it/hash-identifier",
    inputs: { h: "abcdef123456" },
    clicks: ["calcTool()"],
    expect: ["未知 无法仅凭该值判定"],
    ref: "12 位十六进制 = 48 bit，不是 CRC-32（8 位）；旧表误标为「CRC32 / 短校验」。修正后归入无法判定；默认 64 位值不命中。",
  },
  {
    // IT-N363 回归：40 位十六进制必须判 SHA-1（正是旧「默认参数」预设被截断后误落的档位）。
    slug: "it/hash-identifier",
    inputs: { h: "5e884898da28047151d0e56f8dc6292773603d0d" },
    clicks: ["calcTool()"],
    expect: ["SHA-1 160 位（40 位十六进制）"],
    ref: "IT-N363：40 位十六进制 = 160 bit ⇒ SHA-1。旧「默认参数」预设把 64 位 SHA-256 截成前 40 位（本用例即该截断串），点预设即误判 SHA-1；预设值已补全为 64 位并与 resetForm 一致。页面默认值是完整 64 位 ⇒ 默认态判 SHA-256，不命中本串。",
  },
  {
    // IT-N364 回归：$6$ 前缀（SHA-512-crypt）此前任何输入都落到「未知」。
    slug: "it/hash-identifier",
    inputs: { h: "$6$rounds=5000$abc$xyz" },
    clicks: ["calcTool()"],
    expect: ["SHA-512-Crypt 前缀 $6$（SHA-512 crypt）"],
    ref: "IT-N364：本页说明与引据表都写着 `$6$` = SHA-512-crypt，修复前前缀规则只有 $2a$/$2y$/$2b$/$1$/$argon2，$6$ 一律判「未知」。默认值是 64 位十六进制，不含 $ 前缀，不命中。",
  },

  // —— 随机源审计（2026-11-05）：B 类密码学用途改 crypto.getRandomValues 后，
  // 随机内容本身不可断言，改为「长度 / 字符集 / 条数」结构断言。以下用例均落在
  // 页面真实生成路径上，默认态（不点按钮或默认参数）不命中，保持判别力。 ——
  {
    slug: "it/cuid-generator",
    clicks: [
      '(function(){var id1=cuid(),id2=cuid();var ok=/^c[0-9a-z]+$/.test(id1)&&id1.length===13+Date.now().toString(36).length&&id2.length===id1.length&&id1!==id2;document.getElementById("output").innerHTML=ok?"CUID-FMT-OK":"CUID-FMT-FAIL";})()'
    ],
    expect: ["CUID-FMT-OK"],
    ref: "cuid 结构 = 'c' + base36 时间戳(8) + 4 位计数器 + 4 位指纹 + 2×2 位随机 ⇒ 21 位 [0-9a-z]；计数段随调用递增，故两次值不同但长度一致。默认输出区为空，不命中。",
  },
  {
    slug: "it/invite-code-generator",
    inputs: { count: "2", len: "8" },
    checkIds: ["upper", "num"],
    clicks: [
      'generate();(function(){var h=document.getElementById("output").innerHTML;var m=h.match(/<div class=\\S+>[A-Z0-9]{8}<\\/div>/g)||[];document.getElementById("output").innerHTML=m.length===2?"INVITE-FMT-OK-2x8":"INVITE-FMT-FAIL:"+m.length;})()'
    ],
    expect: ["INVITE-FMT-OK-2x8"],
    ref: "只勾大写+数字（字符集 36），长度 8、条数 2 ⇒ 输出恰为 2 个 [A-Z0-9]{8} 的 code-row；默认条数 8、长度 10 且默认勾选小写，故不命中。生成路径已改 crypto.getRandomValues（拒绝采样无模偏）。",
  },
  {
    slug: "it/pin-generator",
    inputs: { len: "6", count: "3" },
    clicks: [
      'generate();(function(){var h=document.getElementById("output").innerHTML;var m=h.match(/<div class=\\S+>[0-9]{6}<\\/div>/g)||[];document.getElementById("output").innerHTML=m.length===3?"PIN-FMT-OK-3x6":"PIN-FMT-FAIL:"+m.length;})()'
    ],
    expect: ["PIN-FMT-OK-3x6"],
    ref: "长度 6、条数 3 ⇒ 输出恰为 3 个 6 位纯数字 pin-row；默认长度 4、条数 5 ⇒ 不命中。生成路径已改 crypto.getRandomValues（拒绝采样无模偏）。",
  },
  {
    slug: "it/nanoid-generator",
    inputs: { length: "12", count: "4" },
    clicks: [
      'gen();(function(){var h=document.getElementById("results").innerHTML;var m=h.match(/<code>[^<]+<\\/code>/g)||[];var c=m.map(function(s){return s.slice(6,-7);});var ok=c.length===4&&c.every(function(x){return x.length===12&&/^[A-Za-z0-9_-]+$/.test(x);});document.getElementById("results").innerHTML=ok?"NANOID-FMT-OK-4x12":"NANOID-FMT-FAIL:"+c.length;})()'
    ],
    expect: ["NANOID-FMT-OK-4x12"],
    ref: "默认 URL-safe 字母表（A-Za-z0-9_-），长度 12、条数 4 ⇒ 4 个 12 位串，字符集校验禁止出现表外字符。默认长度 21、条数 5 ⇒ 不命中。生成路径已改 crypto.getRandomValues。",
  },
  {
    slug: "it/nanoid-generator",
    inputs: { length: "100", count: "1", customAlpha: "😀😁😃😄" },
    clicks: [
      '(function(){var s=nanoid(100,Array.from("😀😁😃😄"));var arr=Array.from(s);var allowed={"😀":1,"😁":1,"😃":1,"😄":1};var ok=arr.length===100&&arr.every(function(x){return allowed[x];});document.getElementById("__tbProbe").textContent="NANOID-EMOJI "+(ok?"OK":"BAD:"+arr.length);})()'
    ],
    expect: ["NANOID-EMOJI OK"],
    ref: "IT-N213 第227批：直接以 emoji 码点字母表调用 nanoid(100)，应产出 100 个完整 emoji（非 50 个 = 旧实现 id.length 按 UTF-16 码元计数提前停）。harness stub 的 radio.checked 恒 false，故直测核心函数而非走 UI。",
  },
  {
    slug: "it/markdown-table-generator",
    inputs: { cols: "1", rows: "1", align: "left", headerLine: "a\\|b", bodyLine: "a\\|b" },
    clicks: ["renderPreview()"],
    expect: ["a\\\\\\|b"],
    ref: "IT-N215 第227批：单元格源文本 a\\|b（含字面反斜杠+竖线）须先转义反斜杠再转义竖线 ⇒ 产物 a\\\\\\|b（双反斜杠+转义竖线）；旧实现只转义竖线得 a\\\\|b，渲染时竖线重新成列分隔符。默认样例无反斜杠，不命中。",
  },
  {
    slug: "it/markdown-table-generator",
    inputs: { cols: "2", rows: "1", align: "left", headerLine: '"a,b",c', bodyLine: '"x,y",z' },
    clicks: ["renderPreview()", "var v=document.getElementById('output').value;document.getElementById('__tbProbe').textContent='CSVQ '+(v.indexOf('| a,b | c |')>=0?'OK':'BAD');"],
    expect: ["CSVQ OK"],
    ref: "IT-N217 第228批：双引号包裹的单元格 \"a,b\" 算 1 列，c 算第 2 列 ⇒ 表头行 `| a,b | c |`；旧实现按裸 split(',') 拆成 4 列。默认样例无引号逗号，不命中。",
  },
  {
    slug: "it/markdown-table-generator",
    inputs: { cols: "3", headerLine: "a", bodyLine: "x" },
    clicks: ["syncColumns();var h=document.getElementById('headerLine').value,b=document.getElementById('bodyLine').value;document.getElementById('__tbProbe').textContent='MD-NOREWRITE '+(h==='a'&&b==='x'&&/C2/.test(document.getElementById('output').value)?'OK':'BAD');"],
    expect: ["MD-NOREWRITE OK"],
    ref: "IT-N216 第227批：syncColumns 编辑期不写回输入（表头仍 a、首行仍 x），缺列由预览占位 C2/C3 补齐；旧实现写回 a,列,列 且 x,值,值。默认样例表头含 3 列，不命中。",
  },
  {
    slug: "it/uuid-generator",
    inputs: { count: "3" },
    clicks: [
      'generateUuid();(function(){var v=document.getElementById("output").value;var l=v.split("\\n");var ok=l.length===3&&l.every(function(x){return /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(x);});document.getElementById("output").value=ok?"UUID-V4-FMT-OK-3":"UUID-FMT-FAIL";})()'
    ],
    expect: ["UUID-V4-FMT-OK-3"],
    ref: "默认 Version 4、数量 3 ⇒ 3 行小写 UUID：第 13 位固定为版本号 4、第 17 位 variant 为 8/9/a/b，其余 [0-9a-f]。默认数量 1 ⇒ 3 行断言不命中。生成路径已移除 Math.random 回退，无 crypto 时显式提示。",
  },
  {
    // 遮蔽回归：copyText 原定义在 generate() 函数作用域内，内联 onclick 看不到它（会落到 common.js 全局实现、
    // 复制按钮元素）。已提到模块作用域并改名 copyRand；本用例直接调用它，断言交给剪贴板的文本。
    slug: "it/random-string",
    inputs: { len: "8", cnt: "2" },
    checkIds: ["top_upper", "top_digit"],
    clicks: ["calcTool();var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='textarea'){try{Object.defineProperty(e,'value',{get:function(){return '';},set:function(v){document.getElementById('result').innerHTML='COPIED:'+v;},configurable:true});}catch(err){}}return e;};copyRand({parentNode:{querySelector:function(){return {textContent:'RAND-XYZ-01'}}}});document.createElement=__ce;"],
    expect: ["COPIED:RAND-XYZ-01"],
    ref: "copyRand(btn) 从同行的 <code> 取 textContent 再写入临时 textarea 复制。用例用假按钮把「行内代码文本」固定为 RAND-XYZ-01，并把 createElement('textarea') 的 value 采集到结果区 ⇒ 期望 COPIED:RAND-XYZ-01。若 copyRand 不可见（仍留在 generate() 内或仍叫 copyText），调用直接抛错、结果不命中。",
  },
  {
    slug: "it/random-string",
    inputs: { len: "8", cnt: "2" },
    checkIds: ["top_upper", "top_digit"],
    clicks: ["calcTool()"],
    expect: ["字符集大小 36 单串长度 8 理论熵值 41 bits"],
    ref: "只勾大写+数字 ⇒ 字符集 36；长度 8、条数 2 ⇒ 熵 = 8·log2(36) = 41.36 → 41 bits。默认四项全勾（含小写/符号）时字符集 87、熵不同；harness 默认 checkbox 全 false 时输出「请至少选择一种字符集」，故该表头只在注入后出现。生成的字符内容不可经 escH 桩读回，故以字符集/长度/熵锚定真实生成参数。",
  },
  {
    slug: "it/password-generator",
    inputs: { length: "12" },
    clicks: [
      'document.getElementById("lowercase").checked=true;document.getElementById("uppercase").checked=true;document.getElementById("numbers").checked=true;generatePassword();(function(){var p=document.getElementById("passwordDisplay").textContent;var ok=p.length===12&&/^[A-Za-z0-9]+$/.test(p);document.getElementById("passwordDisplay").textContent=ok?"PWD-FMT-OK-12-ALNUM":"PWD-FMT-FAIL:"+p.length;})()'
    ],
    expect: ["PWD-FMT-OK-12-ALNUM"],
    ref: "长度 12、只启用小写+大写+数字 ⇒ 每位必落在 62 字符集内（未选符号），串长恒为 12。默认长度 16、默认四项全选（含符号）⇒ 不命中。生成路径已移除 Math.random 回退。",
  },
  {
    slug: "it/matrix-determinant",
    clicks: [
      'document.getElementById("size").value="2";build();document.getElementById("a0").value="1";document.getElementById("a1").value="1";document.getElementById("a2").value="1";document.getElementById("a3").value="1.0000000000001";calculate()'
    ],
    expect: ["9.992007e-14"],
    ref: "2×2 近奇异矩阵 [[1,1],[1,1+1e-13]]：det = 1×(1+1e-13) − 1×1 = 9.992e-14（补码可表示的 1e-13 级差值）。这是条件数信号，不是浮点噪声；原 fmt 先判 |x|<1e-12 → 0 把真实小行列式吞成 0，现改为仅 x===0 返回 0、小值走科学计数法。默认 3×3 单位阵 det=1，不命中。",
  },
  // ── D2 批：7 个条码页的 PNG 导出失败可见（downloadBarcodePNG 的 cv.toDataURL 裸调）──
  {
    // IT-N491 回归：整表按 AIM BC3-1995 / USD-4 重写（原表 20 个字符里 17 个结构非法）
    slug: "it/barcode-codabar",
    inputs: {},
    clicks: ["var bad=[];for(var k in CODABAR){var t=CODABAR[k];var w=(t.match(/W/g)||[]).length;if(t.length!==7||w<2||w>3)bad.push(k+'='+t);}document.getElementById('output').textContent='BAD='+(bad.length?bad.join(','):'none');"],
    expect: ["BAD=none"],
    ref: "IT-N491 不变量：Codabar 每字符必须是 7 个单元、2–3 个宽单元（AIM BC3-1995 / USD-4）。原表 `$`=NWWWWWN（5 宽）、`:`/`/`/`.`/`C` 为 4 宽、`D` 只有 6 个单元 ⇒ 20 个字符里 17 个违规，本断言输出一串 BAD=… 条目；重写后全表 20 个字符全部合规 ⇒ BAD=none。",
  },
  {
    slug: "it/barcode-codabar",
    inputs: {},
    clicks: ["document.getElementById('output').textContent='BITS='+buildCodabar('A0A').bits;"],
    expect: ["BITS=NNWWNWNnNNNNNWWnNNWWNWN"],
    ref: "IT-N491 逐字符码字：按 AIM BC3-1995，`A` = N N W W N W N、`0` = N N N N N W W，字符间插入窄空 `n` ⇒ `NNWWNWNnNNNNNWWnNNWWNWN`。原表 `A`=WWNNNNW、`0`=NNNNNWW 结构互不相同，故该串在修复前不存在（页面默认 data=A12345B 渲染的是 canvas，不含该串）。",
  },
  {
    slug: "it/barcode-codabar",
    inputs: { data: "12345" },
    expect: ["首字符必须是起止符 A/B/C/D（如 A12345B）"],
    ref: "IT-N492 起止符校验：Codabar 规定首尾必须是 A–D，`12345` 无起止符时读码器无法判读。修复前页面照样生成条形码（静默接受）；现 generate() 直接报错并说明补法。默认 data=A12345B 合法，不命中。",
  },
  {
    "slug": "it/barcode-codabar",
    "inputs": { "data": "A1B2C" },
    "expect": ["数据位仅支持 0-9 - $ : / . +"],
    "ref": "IT-N492/N493：起止符之间的数据位仅允许 0-9 - $ : / . +，A/B/C/D 仅为起止符不得出现在数据位。`A1B2C` 内部含 B、C（起止符）⇒ 必须报错。默认样例 A12345B 数据位全为数字不命中；修复前静默生成条码（数据位含起止符 ⇒ 扫码值与标签不一致）。"
  },
  {
    "slug": "it/barcode-codabar",
    "inputs": { "data": "AAA" },
    "expect": ["数据位仅支持 0-9 - $ : / . +"],
    "ref": "IT-N492/N493：`AAA` 起止符之间无合法数据字符（内部 A 不是数据字符）⇒ 必须报错。默认样例不命中；修复前静默生成条码（无有效数据）。"
  },
  ...["barcode-codabar", "barcode-code128", "barcode-code39", "barcode-ean", "barcode-itf", "barcode-msi", "barcode-upc"].map(function (slug) {
    return {
      slug: "it/" + slug,
      clicks: [
        "ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};"
        + "var __qs=document.querySelector.bind(document);"
        + "document.querySelector=function(s){if(s==='#output canvas')return {toDataURL:function(){throw new Error('boom')}};return __qs(s);};"
        + "downloadBarcodePNG();",
      ],
      expect: ["TOAST:导出失败：Error"],
      ref: "失败注入：让 `#output canvas` 返回 toDataURL 必抛 Error 的假画布 + 录制 ToolBox.showToast ⇒ 必须出现「TOAST:导出失败：Error」。"
        + "修复前异常裸冒成 pageerror、且紧随其后仍弹「PNG 已下载」（给出错误事实）；默认态无 TOAST: 串 ⇒ 判别明确。",
    };
  }),
  // ── D3 批：captcha-generator 导出失败可见（exportImage 的 toDataURL 裸调）──
  {
    slug: "it/captcha-generator",
    clicks: [
      "ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};"
      + "document.getElementById('captchaCanvas').toDataURL=function(){throw new Error('boom')};"
      + "exportImage();",
    ],
    expect: ["TOAST:导出失败：Error"],
    ref: "失败注入：captchaCanvas.toDataURL 必抛 Error + 录制 ToolBox.showToast ⇒ 必须出现「TOAST:导出失败：Error」。"
      + "修复前异常裸冒成 pageerror、且下载失败后仍弹「已导出」；默认态无 TOAST: 串 ⇒ 判别明确。",
  },
  {
    slug: "it/typing-test",
    // IT-N482 回归：已输入但打错的字符须标 .wrong（红底），与错误计数/准确率一致。
    clicks: ["text='abc';pos=3;document.getElementById('typingInput').value='axc';renderText();var area=document.getElementById('testArea');document.getElementById('__tbProbe').textContent='WRONG '+(area.querySelectorAll('.char.wrong').length)+' CORRECT '+(area.querySelectorAll('.char.correct').length);"],
    expect: ["WRONG 1 CORRECT 2"],
    ref: "类型反馈探针：目标文本 abc、已输入 axc（第 2 位打错），应恰有 1 个 wrong + 2 个 correct。修复前 renderText 只按 i<pos 判 correct ⇒ 3 个 correct、0 个 wrong ⇒ WRONG 0 CORRECT 3，不命中。默认态 text 是随机预设、pos=0 ⇒ 无 wrong/correct，不命中。",
  },
  // ── 第229批 IT-N222~N226 ──
  {
    slug: "it/phone-screen-sizes",
    inputs: { diag: "5", resw: "1080", resh: "1920" },
    clicks: ["calcTool();var h=pssPhoneTable();document.getElementById('__tbProbe').textContent='PSS229 '+(/1920/.test(document.getElementById('result').innerHTML)&&/DPR（典型）/.test(h)&&/CSS 视口（宽×高）/.test(h)&&/1179×2556/.test(h)&&/393×852/.test(h)?'OK':'BAD');"],
    expect: ["PSS229 OK"],
    ref: "IT-N223 强锁：注入 1080×1920 → 结果区含输入派生分辨率，同时机型表必须给出 DPR/CSS 视口列、宽×高顺序与 iPhone 393×852。修复前机型表只有四列且写 2556×1179，探针命中 BAD。",
  },
  {
    slug: "it/rabbit",
    inputs: { key: "00000000000000000000000000000000", iv: "0000000000000000", outputFormat: "hex", input: "616263" },
    clicks: ["var b=new Uint8Array(16);new Rabbit(getKey(),hexToBytes(document.getElementById('iv').value)).keystream(b,0,16);document.getElementById('__tbProbe').textContent='RAB229 '+bytesToHex(b);"],
    expect: ["RAB229 c6a7275ef85495d87ccd5d376705b7ed"],
    ref: "IT-N225/N226 强锁：注入 RFC 4503 全零密钥(32 hex)+全零 IV，首块密钥流必须等于官方向量 C6A7275E…。修复前 hex 密钥被当 ASCII 且算法非 RFC ⇒ 必不命中。",
  },
  {
    slug: "it/rabbit",
    inputs: { key: "this-key-is-way-too-long-12345", input: "616263" },
    clicks: ["var o='BAD';try{getKey();}catch(e){o=/16/.test(e.message)?'KEY229 OK':'BAD';}document.getElementById('__tbProbe').textContent=o;"],
    expect: ["KEY229 OK"],
    ref: "IT-N226 强锁：注入超过 16 字节的文本密钥，getKey 必须明确报错（含 16），修复前静默 slice(0,16) 无异常 ⇒ BAD。默认 16 字节密钥不命中。",
  },
  // ── 第230批 IT-N227 / N231 / N232 ──
  {
    slug: "it/rabbit",
    inputs: { iv: "abcdefghijklmnop", input: "616263", outputFormat: "hex" },
    clicks: ["var o='BAD';try{getIV();}catch(e){o=/16/.test(e.message)?'IV230 OK':'BAD';}document.getElementById('__tbProbe').textContent=o;"],
    expect: ["IV230 OK"],
    ref: "IT-N227 强锁：注入 16 个非 hex 字符的 IV，必须报「16 位 hex」错误；修复前 hexToBytes 把 NaN 写成 0，按全 0 IV 静默继续 ⇒ BAD。默认 IV 留空不命中。",
  },
  {
    slug: "it/sms-qr",
    inputs: { phone: "13800138000", msg: "NaN" },
    clicks: ["generate();var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent=(/body=NaN/.test(h)&&!/无效值/.test(h)?'NAN230 OK':'BAD');"],
    expect: ["NAN230 OK"],
    ref: "IT-N232 强锁：短信正文合法含 NaN 时必须照常输出 URI；修复前 NaN 正则守卫把结果换成「计算结果含无效值」⇒ BAD。默认正文不含 NaN，不命中。",
  },
  {
    slug: "it/sms-qr",
    inputs: { phone: "13800138000#test", msg: "Hi" },
    clicks: ["var o='BAD';try{buildSms();}catch(e){o=/5.15/.test(e.message)?'TEL230 OK':'BAD';}document.getElementById('__tbProbe').textContent=o;"],
    expect: ["TEL230 OK"],
    ref: "IT-N231 强锁：注入含 # 的非法号码必须报 5–15 位数字错误；修复前原样拼进 sms: URI，# 把 ?body 变成 fragment ⇒ BAD。默认号码合法，不命中。",
  },
  // ── 第231批 IT-N228/N229/N235 ──
  {
    slug: "it/mysql-cheatsheet",
    inputs: { searchInput: "GRANT" },
    clicks: ["renderCommands();var o=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent=(/CREATE USER/.test(o)&&!/FLUSH PRIVILEGES/.test(o)&&!/IDENTIFIED BY 'pwd'/.test(o)?'MYSQL228 OK':'BAD');"],
    expect: ["MYSQL228 OK"],
    ref: "IT-N228 强锁：搜索 GRANT 后示例必须是 CREATE USER + GRANT 两行，无 FLUSH PRIVILEGES 与旧 IDENTIFIED BY 'pwd'；修复前示例照抄 5.6 写法 ⇒ BAD。默认搜索为空时锚点不同。",
  },
  {
    slug: "it/mysql-cheatsheet",
    inputs: { searchInput: "ON DUPLICATE KEY UPDATE" },
    clicks: ["renderCommands();var o=String(document.getElementById('cmdList').innerHTML);document.getElementById('__tbProbe').textContent=(/AS new/.test(o)&&/new\\.name/.test(o)&&!/VALUES\\(name\\)/.test(o)?'MYSQL229 OK':'BAD');"],
    expect: ["MYSQL229 OK"],
    ref: "IT-N229 强锁：UPSERT 示例必须改成行别名 new.name；修复前用 MySQL 8.0.20 起废弃的 VALUES(name) ⇒ BAD。默认搜索为空时不命中这些锚点。",
  },
  {
    slug: "it/hypothesis-test",
    inputs: { mean: "108", mu0: "100", sigma: "10", n: "25", alpha: "0.05", tail: "two" },
    clicks: ["calculate();var o=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent=(/6\\.33425e-5/.test(o)?'HYP235 OK':'BAD');"],
    expect: ["HYP235 OK"],
    ref: "IT-N235 强锁：z=4 双侧 p 必须显示 6.33425e-5（math.erfc 高精度值 6.334248e-5 的 6 位有效数字）；修复前 A&S 多项式给 6.337206e-5 且 toLocaleString 把 6e-5 显示成 0 ⇒ BAD。默认 z=2 不命中。",
  },
];

// ---------------------------------------------------------------- DOM stub
// canvas 2D 上下文桩（所有方法为空实现，measureText 返回零宽度以适配排版计算）
const CTX2D = new Proxy(
  { measureText: () => ({ width: 0 }), createLinearGradient: () => ({ addColorStop() {} }), canvas: { width: 0, height: 0, clientWidth: 300, clientHeight: 300 } },
  {
    get(t, k) {
      if (k in t) return t[k];
      return () => {};   // arc / fill / fillText / beginPath … 一律空实现
    },
    set() { return true; }, // ctx.fillStyle = … 等属性写入
  }
);

// ---------------------------------------------------------------- 动态 DOM 登记（click 驱动型页面）
// 背景：psychiatry / tcm-diagnosis 里的量表页**没有任何表单控件** —— 题目与选项是 render() 拼好
// HTML 写进 #quiz 的 <span class="q-opt" onclick="pick(i,j)">，答题状态存在页面内存数组里。
// 旧桩 querySelectorAll 恒返回 [] ⇒ pick() 在 `its[i].querySelectorAll(...)` 处抛错、calc() 不被调用，
// 用例无从注入 ⇒ 只能取默认态串做 expect（零判别力，长期挂在 no_inputs 基线里）。
// 这里按「用例是否声明 clicks / dynDom」**选择性启用**（默认关闭 ⇒ 对既有用例零影响）：
// innerHTML 被赋值时解析出 {tag,id,class} 登记进 dynRegistry，querySelectorAll 从登记表取匹配项。
// 这类页对选中项只做 classList.toggle（纯装饰），故只需保证「元素个数与真机一致 + 方法不抛错」，
// 按「同容器以最后一次渲染为准」返回即可，无需真实 DOM 树；**也不会把 id 注册进 elements**
// （2026-09-23 那次「innerHTML setter 解析 id 注册桩元素」正是在全站无差别生效，才误伤
//  psychology/calc-12 这类用 innerHTML 渲染滑块的页 ⇒ 已还原；本次以用例开关隔离风险）。
const DYN = { on: false, order: [], map: new Map(), serial: 0 };
function dynReset() { DYN.on = false; DYN.order = []; DYN.map.clear(); DYN.serial = 0; }
function dynRecord(el, html) {
  if (el.__dynNode) return;                     // 登记表自身生成的桩，避免自我递归
  const key = el.id ? "#" + el.id : (el.__dynKey || (el.__dynKey = "anon#" + DYN.serial++));
  const nodes = [];
  const src = String(html);
  // 分段定位（2026-11-05）：真机 `querySelectorAll('.tbl tbody tr')` 只命中 tbody 内的行，
  // 不命中 thead 的表头行；登记表若只按 tag 返回，表头行会被当成数据行（logic-gate 的
  // highlightTruthTable 读 `tr.dataset.row.split()` 时表头无 data-row ⇒ 抛错、初始化中止）。
  // 这里记录每个节点是否落在 tbody / thead 段内，供 dynQuery 按选择器里的段名过滤。
  const segRanges = (name) => [...src.matchAll(new RegExp("<" + name + "[^>]*>([\\s\\S]*?)</" + name + ">", "gi"))]
    .map((x) => [x.index, x.index + x[0].length]);
  const bodyRanges = segRanges("tbody");
  const headRanges = segRanges("thead");
  const inRanges = (pos, ranges) => ranges.some(([a, b]) => pos >= a && pos < b);
  for (const m of src.matchAll(/<([a-zA-Z][\w:-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)>/g)) {
    const attrs = m[2] || "";
    const id = (attrs.match(/\bid\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const cr = (attrs.match(/\bclass\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const node = { tag: m[1].toLowerCase(), id, cls: cr.split(/\s+/).filter(Boolean), el: makeEl("") };
    node.inBody = inRanges(m.index, bodyRanges);
    node.inHead = inRanges(m.index, headRanges);
    node.el.__dynNode = true;
    // 动态 <select> 的选项登记（2026-11-05）：usedcar/checker-3 的 buildList() 把
    // `<select id="ck_*"><option value="4" selected>…</option></select>` 拼进 #checkItems
    // 的 innerHTML，随后 boot 的 calc() 用 document.getElementById('ck_*').value 取档位。
    // 旧桩只登记标签本身、不给选项 ⇒ .value 恒 "" ⇒ statusOpts.find(o => o.v === 0)
    // 不命中 ⇒ opt.score 抛 "Cannot read properties of undefined (reading 'score')"。
    // 此处截取该 <select> 到 </select> 之间的内容，登记 value/text/selected（浏览器语义：
    // 无 value 属性 ⇒ option.value = 选项文本）。
    if (node.tag === "select") {
      const cs = src.indexOf("</select>", m.index + m[0].length);
      if (cs > -1) {
        node.opts = [...src.slice(m.index + m[0].length, cs).matchAll(/<option([^>]*?)>([\s\S]*?)<\/option>/gi)]
          .map((o) => {
            const tx = o[2].replace(/<[^>]+>/g, "").trim();
            const vm = (o[1] || "").match(/\bvalue\s*=\s*["']([^"']*)["']/i);
            return { value: vm ? vm[1] : tx, text: tx, attrs: o[1] || "" };
          });
      }
    }
    // 关键保真（2026-11-05）：把标签与整段属性落到桩元素上 —— 页面初始化常读
    // `tr.dataset.row` / `card.dataset.gate` / `getAttribute('data-…')`，缺 dataset
    // 直接抛 "Cannot read properties of undefined (reading 'split')"，整页初始化中止。
    node.el.tagName = m[1].toUpperCase();
    node.el.__applyAttrs(attrs);
    node.el.parentElement = el;
    if (id) node.el.id = id;
    nodes.push(node);
  }
  if (!DYN.map.has(key)) DYN.order.push(key);
  DYN.map.set(key, nodes);   // 同容器以最后一次渲染为准 ⇒ 重复渲染不会让计数翻倍
  return nodes;
}
function dynQuery(sel) {
  if (!DYN.on) return [];
  const last = String(sel).replace(/[>+~]/g, " ").trim().split(/\s+/).pop();
  if (!last) return [];
  const mId = last.match(/#([\w-]+)/);
  const mCls = [...last.matchAll(/\.([\w-]+)/g)].map((x) => x[1]);
  const mTag = last.match(/^([a-zA-Z][\w-]*)/);
  if (!mId && !mCls.length && !mTag) return [];
  // 段名作用域：选择器带 tbody / thead 时只返回对应段内的节点（等价真机的后代限制）。
  const ss = String(sel);
  const wantBody = /\btbody\b/.test(ss) && !/\bthead\b/.test(ss);
  const wantHead = /\bthead\b/.test(ss) && !/\btbody\b/.test(ss);
  const out = [];
  for (const k of DYN.order) {
    for (const n of DYN.map.get(k) || []) {
      if (mId && n.id !== mId[1]) continue;
      if (mTag && n.tag !== mTag[1].toLowerCase()) continue;
      if (wantBody && !n.inBody) continue;
      if (wantHead && !n.inHead) continue;
      if (mCls.length && !mCls.every((c) => n.cls.indexOf(c) !== -1)) continue;
      out.push(n.el);
    }
  }
  return out;
}

// 运行期 innerHTML 生成的 <select>（容器渲染，非 select.innerHTML）按 id 取选项。
// 供 getElementById 回落：真机 boot 时这类 select 已有首项选中，.value 即首项值。
function dynSelectOf(id) {
  if (!DYN.on || !id) return null;
  for (const k of DYN.order) {
    for (const n of DYN.map.get(k) || []) {
      if (n.tag === "select" && n.id === id && n.opts && n.opts.length) return n.opts;
    }
  }
  return null;
}

// 构造 <option> 桩：除 value/text/label 外，还要带 dataset（data-* 属性）与 getAttribute。
// 页面常写 `sel.selectedOptions[0].dataset.pip`（forex/lot-size 等）或
// `sel.options[i].getAttribute('data-x')`（food-testing/allergen-cross-risk），
// 缺这两个会抛 "Cannot read properties of undefined" / "getAttribute is not a function"
// ⇒ 整页「初始化失败」。这里按真实浏览器语义解析 option 标签上的 data-* 与其他属性。
function mkOpt(value, text, attrStr) {
  const v = value != null ? String(value) : "";
  const t = text != null ? String(text) : v;
  const o = { value: v, text: t, label: t, selected: false, dataset: {}, _attrs: String(attrStr || "") };
  for (const m of o._attrs.matchAll(/\bdata-([\w-]+)\s*=\s*["']([^"']*)["']/gi)) {
    o.dataset[m[1].replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = m[2];
  }
  o.getAttribute = function (n) {
    if (n == null) return null;
    const esc = String(n).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const m = o._attrs.match(new RegExp("\\b" + esc + "\\s*=\\s*[\"']([^\"']*)[\"']", "i"));
    if (m) return m[1];
    if (String(n) === "value") return v;
    return null;
  };
  return o;
}

// 可选「浏览器保真初始化」开关（用例字段 afterLoad:true 时开启，默认关闭）：
// 很多页面在脚本末尾同步 init，并用 innerHTML 批量生成按钮/卡片后立刻读
// `children[i].classList`；动态填 <select> 的 option 后依赖浏览器自动选中首项。
// 这两点桩默认不建模（无条件生效曾误伤其它页，故按用例 opt-in）。
let __browserInit = false;
// 可选「动态控件默认值登记」（用例字段 dynInputs:true 时开启，默认关闭）：
// 页面若先 `renderMachines()` 再 `calc()`（如 agriculture/machinery-efficiency），
// 桩内 innerHTML 生成的 input 不会进入 elements 表 ⇒ calc 读到空串 ⇒ 首屏落入「无数据」
// 分支，用例的 expect 与注入无关地命中（假通过）。开启后 innerHTML 写入即登记
// `id → value`，getEl 首次访问直接返回该默认值，等价真机「渲染后即有值」。
// 默认关闭 ⇒ 既有用例路径逐字节不变（同 afterLoad 的隔离思路）。
let __dynInputs = false;
const __dynInputReg = new Map();

function makeEl(val, opts) {
  const handlers = {};
  // 懒创建的父节点桩：页面常写 `cell.parentElement.classList.add('x')`（如
  // mechanical/bolt-torque 的 highlightTable）。原先 parentElement 是裸对象、没有
  // classList，整页在初始化期就抛 "Cannot read properties of undefined (reading 'add')"
  // ⇒ 恒被判「初始化失败」而无法验证。这里改成返回完整元素桩（裸对象属性的超集）。
  let _parent = null;
  // 显式写入的 selectedIndex（见下方 selectedIndex setter）：页面常用
  // `sel.selectedIndex = 11` 选档后再回读该值（design/exposure-triangle-calculator 的
  // aperture/shutter/iso 三档）。这些页的 <option> 没有 value 属性，靠索引定位 ⇒
  // 必须原样记住写入的索引，不能退化成按 value 反查（会恒回 0）。
  let _selIdx = null;
  // 属性/类名/data-* 的真实化（2026-11-05）：
  // 真机上 el.dataset 恒存在且与 data-* 属性双向同步、classList 反映 className；
  // 旧桩把 dataset 固定成 {}、classList 全为 no-op ⇒ 页面初始化读 `tr.dataset.row`
  // 直接抛 "Cannot read properties of undefined (reading 'split')"，只能记「桩盲区」。
  // 这里一次性补齐：dataset 用 Proxy 双向同步属性表，classList 读写 className，
  // setAttribute/getAttribute/removeAttribute 覆盖 value/id/class/data-*。
  const _attrs = new Map();                 // 非 data-*/value/id/class 的原始属性
  const _ds = {};                           // dataset 真实存储（camelCase）
  const _dataAttr = (p) => "data-" + String(p).replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());
  const _camel = (n) => String(n).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
  const dataset = new Proxy(_ds, {
    get(t, k) { return t[k]; },
    set(t, k, v) { t[k] = String(v); _attrs.set(_dataAttr(k), String(v)); return true; },
    deleteProperty(t, k) { delete t[k]; _attrs.delete(_dataAttr(k)); return true; },
    has(t, k) { return k in t; },
    ownKeys(t) { return Reflect.ownKeys(t); },
    getOwnPropertyDescriptor(t, k) { return Reflect.getOwnPropertyDescriptor(t, k); },
  });
  let _cls = "";
  const classList = {
    add(...cs) { for (const c of cs) if (c && !_cls.split(/\s+/).includes(c)) _cls = (_cls ? _cls + " " : "") + c; },
    remove(...cs) { const set = new Set(cs); _cls = _cls.split(/\s+/).filter((c) => c && !set.has(c)).join(" "); },
    toggle(c, force) {
      const has = _cls.split(/\s+/).includes(c);
      const on = force === undefined ? !has : !!force;
      if (on) classList.add(c); else classList.remove(c);
      return on;
    },
    contains(c) { return _cls.split(/\s+/).includes(c); },
    item(i) { return _cls.split(/\s+/).filter(Boolean)[i] || null; },
    get length() { return _cls.split(/\s+/).filter(Boolean).length; },
    toString() { return _cls; },
  };
  // 简易选择器匹配（tag / #id / .class / [attr=value]，支持逗号并集），供 matches/closest 使用
  const _matches = (node, sel) => String(sel || "").split(",").some((part) => {
    part = part.trim();
    if (!part) return false;
    const tag = part.match(/^([a-zA-Z][\w-]*)/);
    if (tag && node.tagName && tag[1].toLowerCase() !== String(node.tagName).toLowerCase()) return false;
    for (const m of part.matchAll(/#([\w-]+)/g)) if (String(node.id || "") !== m[1]) return false;
    for (const m of part.matchAll(/\.([\w-]+)/g)) if (!classList.contains(m[1])) return false;
    for (const m of part.matchAll(/\[([\w-]+)(?:\s*=\s*["']?([^"'\]\s]*)["']?)?\]/g)) {
      const got = node.getAttribute(m[1]);
      if (got == null) return false;
      if (m[2] !== undefined && String(got) !== m[2]) return false;
    }
    return true;
  });
  const el = {
    value: val === undefined ? "" : val,
    textContent: "",
    // 与真实 <select> 对齐：页面常读 el.selectedOptions[0].text / .dataset.pip 取选项标签
    // 与附加数据，缺此属性会在 calc() 抛 "Cannot read properties of undefined" 使整页无法验证。
    // 用 getter 跟随当前 el.value 动态匹配（注入非默认选项后dataset 也跟着变），
    // 原先是构造期常量数组，注入后 selectedOptions[0] 仍停在初始选项 ⇒ 读不到注入项的数据。
    get selectedOptions() {
      const list = el.options || [];
      const cur = list.find((o) => String(o.value) === String(el.value));
      return [cur || mkOpt(el.value, el.value)];
    },
    checked: false,
    style: {},
    // dataset 与 data-* 属性双向同步（Proxy 写入时同步 _attrs），classList 读写 className。
    dataset,
    children: [],
    _handlers: handlers,
    classList,
    get className() { return _cls; },
    set className(v) { _cls = String(v == null ? "" : v).trim(); },
    addEventListener(ev, cb) { (handlers[ev] = handlers[ev] || []).push(cb); },
    removeEventListener() {},
    fire(ev) { for (const cb of handlers[ev] || []) cb({ target: el, preventDefault() {}, stopPropagation() {} }); },
    appendChild(c) {
      this.children.push(c);
      // 真实 DOM 会把子节点内容反映到父节点，结果采集依赖这一点
      const piece = (c && c.innerHTML) || (c && c.textContent) || "";
      if (piece) this.innerHTML = String(this.innerHTML || "") + piece;
      return c;
    },
    removeChild() {},
    // 动态生成表单的页面（neurology/dhi、dn4、phq9-stroke、rls-severity 等）在 buildForm()
    // 用 `container.parentNode.insertBefore(wrapper, container.nextSibling)` 把拼好的 radio
    // 容器插入 DOM。本 harness 的 calc 已通过 getElementsByName 绕过 DOM 取值（无需 radio 真实存在），
    // 故 insertBefore 只需 no-op 让 init 不抛错即可；wrapper 是否入 DOM 不影响算分。
    insertBefore() {},
    // 动态填充 <select>：部分页用 new Option(text,value)+select.add() 注入选项
    // （如 travel/timezone-converter-advanced）。option 带 selected 或首个选项时，
    // 将其 value 落到 el.value，使页面后续 `.value` 读取拿到选中值。其他页不调用
    // el.add()，本方法对其行为零影响。
    add(option) {
      if (!this.options) this.options = [];
      // new Option(text,value) 生成的桩没有 dataset/getAttribute；补齐以免页面读
      // `sel.options[i].dataset.x` 抛错（与 mkOpt 口径一致）。
      if (option && typeof option.dataset !== "object") { option.dataset = {}; option._attrs = ""; }
      if (option && typeof option.getAttribute !== "function") option.getAttribute = () => null;
      this.options.push(option);
      if (option && (option.selected || this.options.length === 1)) {
        this.value = option.value != null ? String(option.value) : "";
      }
    },
    insertAdjacentHTML() {},
    // 页面常 `o1.cloneNode(true)` 复制模板节点再改属性（misc/unit-prefix 的候选行渲染），
    // 缺此 API 整页初始化抛 "cloneNode is not a function" ⇒ 恒不可验证。
    // 返回同构空节点即可：页面的后续赋值（value/textContent）会落在这个副本上。
    cloneNode() { return makeEl(""); },
    // 属性读写：value/id/class/data-* 落到真实字段，其余进 _attrs；与 dataset 双向一致。
    setAttribute(n, v) {
      n = String(n).toLowerCase();
      v = String(v == null ? "" : v);
      if (n === "value") { el.value = v; return; }
      if (n === "id") { el.id = v; return; }
      if (n === "class") { el.className = v; return; }
      if (/^data-/.test(n)) { dataset[_camel(n.slice(5))] = v; return; }
      _attrs.set(n, v);
    },
    getAttribute(n) {
      n = String(n).toLowerCase();
      if (n === "value") return String(el.value);
      if (n === "id") return el.id == null ? null : String(el.id);
      if (n === "class") return el.className;
      if (/^data-/.test(n)) { const k = _camel(n.slice(5)); return dataset[k] !== undefined ? String(dataset[k]) : null; }
      return _attrs.has(n) ? _attrs.get(n) : null;
    },
    removeAttribute(n) {
      n = String(n).toLowerCase();
      if (n === "value") { el.value = ""; return; }
      if (n === "id") { el.id = ""; return; }
      if (n === "class") { el.className = ""; return; }
      if (/^data-/.test(n)) { delete dataset[_camel(n.slice(5))]; return; }
      _attrs.delete(n);
    },
    // 把一段属性串（innerHTML 解析结果）原样落到本元素：data-* → dataset，class → className。
    __applyAttrs(attrs) {
      for (const m of String(attrs || "").matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))/g)) {
        el.setAttribute(m[1], m[2] !== undefined ? m[2] : m[3] !== undefined ? m[3] : m[4]);
      }
      return el;
    },
    // 复制路径：页面普遍 `ta.select(); document.execCommand('copy')`（common.js 的 copyText
    // 与各工具页的本地复制实现都走这条），缺 .select/.setSelectionRange 会直接抛
    // "select is not a function" ⇒ 复制用例整段中断、判别器子进程无统计行。
    select() {},
    setSelectionRange() {},
    // 动态 DOM 登记生效时（用例声明 clicks/dynDom），元素的 querySelectorAll 也走登记表 ——
    // 页面写成 `it.querySelectorAll('.q-opt')` 时才能拿到数组（超集即可，仅用于 classList.toggle），
    // 否则 `[].forEach.call(undefined, …)` 抛错、紧随其后的 calc() 被整段跳过。
    querySelector(sel) { const r = dynQuery(sel); return r.length ? r[0] : makeEl(""); },
    querySelectorAll(sel) { return dynQuery(sel); },
    matches(sel) { return _matches(el, sel); },
    closest(sel) {
      let cur = el;
      for (let i = 0; i < 12 && cur; i++) {
        if (_matches(cur, sel)) return cur;
        cur = cur.parentElement || null;
      }
      return null;
    },
    checkValidity() {
      const value = String(this.value == null ? "" : this.value);
      if (!value) return this.getAttribute("required") === null;
      if (this.getAttribute("type") !== "number") return true;
      const n = Number(value);
      if (!Number.isFinite(n)) return false;
      const min = this.getAttribute("min"), max = this.getAttribute("max"), step = this.getAttribute("step");
      if (min !== null && n < Number(min) || max !== null && n > Number(max)) return false;
      if (step !== "any") {
        const size = step === null ? 1 : Number(step);
        const base = min === null ? 0 : Number(min);
        if (size > 0 && Math.abs((n - base) / size - Math.round((n - base) / size)) > 1e-9) return false;
      }
      return true;
    },
    focus() {},
    // 元素滚动定位：查表/详情类页（science/periodic-table 点击元素后滚动到详情卡）
    // 会调用，缺此 API 整页初始化即抛 "scrollIntoView is not a function" ⇒ 恒不可验证。
    scrollIntoView() {},
    click() {},
    remove() {},
    getBoundingClientRect() { return { width: 0, height: 0, top: 0, left: 0 }; },
    clientWidth: 300,
    clientHeight: 300,
    offsetWidth: 300,
    offsetHeight: 300,
    get parentElement() { if (!_parent) _parent = makeEl(""); return _parent; },
    // 允许 innerHTML 解析路径回填真实父节点（closest 才能沿树向上匹配）。
    set parentElement(p) { _parent = p || null; },
    get parentNode() { return el.parentElement; },
    get firstElementChild() { return null; },
    // canvas 2D 上下文桩：含图表的页面（如 healthcare/tdee-calculator 的热量环形图）
    // 在 calc() 里直接 ctx.arc/fillText，缺了会抛 "getContext is not a function" 使整页无法验证。
    getContext() { return CTX2D; },
    // canvas 导出桩：图像类页（design/initials-avatar、favicon-from-text 等）在生成后
    // 立即 `canvas.toDataURL('image/png')` 把结果写进 <img>/下载链接，缺此 API 整页抛
    // "toDataURL is not a function" ⇒ 生成流程中断、结果区恒空。这里返回固定的
    // 合法 data URL（不模拟像素），既让流程跑完，也让「data:image/png;base64,」可作锚。
    toDataURL() { return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg=="; },
    toBlob(cb) { if (typeof cb === "function") cb(null); },
  };
  // 让 <select> 桩支持 options / selectedIndex：页面常用 `el.options[el.selectedIndex].text`
  // 取选项标签（construction/area 等全部页面在 getParams() 里这么读），缺此属性会在 calc()
  // 抛 "Cannot read properties of undefined" 使整页无法验证。selectedIndex 用 getter 跟随
  // 当前 value 动态匹配，保证注入非默认选项后文本也跟着变。
  if (opts && opts.length) {
    el.options = opts.map((o) => mkOpt(o.value, o.text, o.attrs != null ? o.attrs : (o._attrs || "")));
    Object.defineProperty(el, "selectedIndex", {
      configurable: true,
      get() {
        if (_selIdx != null && _selIdx >= 0 && _selIdx < el.options.length) return _selIdx;
        const i = el.options.findIndex((o) => String(o.value) === String(el.value)); return i < 0 ? 0 : i;
      },
      // setter（真实 DOM 语义）：写 selectedIndex 即选中该选项并原样回读。用例常用
      // `document.getElementById('shutter').selectedIndex = 11` 选档
      // （design/exposure-triangle-calculator 的 aperture/shutter/iso 三档，
      // 其 <option> 都没有 value 属性 ⇒ 只能靠索引定位，回读必须原样保留写入值）。
      set(i) { _selIdx = Number(i); const o = el.options[Number(i)]; if (o) el.value = o.value; },
    });
  }
  let _h = "";
  Object.defineProperty(el, "innerHTML", {
    set(v) {
      _h = String(v == null ? "" : v);
      if (DYN.on) dynRecord(el, _h);
      // dynInputs（opt-in）：登记生成出来的 input/textarea 默认值（同容器后写覆盖先写，
      // 与真机「重渲染后元素带新默认值」一致）。只登记，不创建 elements 桩。
      if (__dynInputs) {
        for (const m of _h.matchAll(/<(?:input|textarea)\b([^>]*)>/gi)) {
          const idm = m[1].match(/\bid\s*=\s*["']([^"']+)["']/i);
          if (!idm) continue;
          const vm = m[1].match(/\bvalue\s*=\s*["']([^"']*)["']/i);
          __dynInputReg.set(idm[1], vm ? vm[1] : "");
        }
      }
      // 动态填充 <select>：很多页用 `sel.innerHTML = '<option...>'` 注入选项
      // （如 agriculture/crop-yield 的 initCrops）。不解析则 `el.options` 恒空，
      // 页面读 `el.options[selectedIndex].text` 抛错使整页无法验证。仅在内容含
      // <option> 时解析，对非 select 元素无副作用。
      if (/<option/i.test(_h)) {
        const opts = [..._h.matchAll(/<option([^>]*?)>([\s\S]*?)<\/option>/gi)]
          .map((m) => {
            const tx = m[2].replace(/<[^>]+>/g, "").trim();
            const vm = (m[1] || "").match(/value\s*=\s*["']([^"']*)["']/);
            // 浏览器语义：无 value 属性 ⇒ option.value = 选项文本（旧桩给 "" 会让
            // 依赖文本取值的页读到空串，例如 design/music-scale-reference 的 #root）
            return mkOpt(vm ? vm[1] : tx, tx, m[1]);
          });
        if (opts.length) {
          el.options = opts;
          if (!("selectedIndex" in el)) {
            Object.defineProperty(el, "selectedIndex", {
              configurable: true,
              get() {
                if (_selIdx != null && _selIdx >= 0 && _selIdx < el.options.length) return _selIdx;
                const i = el.options.findIndex((o) => String(o.value) === String(el.value)); return i < 0 ? 0 : i;
              },
              set(i) { _selIdx = Number(i); const o = el.options[Number(i)]; if (o) el.value = o.value; },
            });
          }
          // 浏览器语义（仅 afterLoad 用例生效）：向空 <select> 写入 option 后，
          // 首个选项（或带 selected 的选项）自动成为选中项，页面随后读取 .value
          // 才能拿到合法分类（acupuncture/acupoint-combination 的 renderDisease 依赖它）。
          if (__browserInit && el.value === "") {
            const hit = opts.find((o) => /\bselected\b/i.test((o && o._attrs) || "")) || opts[0];
            el.value = hit && hit.value != null ? String(hit.value) : "";
          }
        }
      }
      // 浏览器语义（仅 afterLoad 用例生效）：innerHTML 写入的子元素即成为 children 节点。
      // 页面常见「innerHTML 批量生成按钮 → 立刻 children[def].classList.add('active')」
      // （ophthalmology/pupil-reflex 即因此初始化抛错），桩默认 children 恒空。
      if (__browserInit) {
        el.children = [..._h.matchAll(/<([a-zA-Z][\w-]*)([^>]*)>([\s\S]*?)<\/\1>/g)].map((m2) => {
          const child = makeEl("");
          child.tagName = m2[1].toUpperCase();
          // 与 dynRecord 同口径：data-* / class / 其它属性落到桩元素，children[i].dataset 可读。
          child.__applyAttrs(m2[2]);
          child.parentElement = el;
          child.textContent = m2[3].replace(/<[^>]+>/g, "").trim();
          return child;
        });
      }
    },
    get() { return _h; },
  });
  return el;
}

function inlineScripts(html) {
  const out = [];
  for (const m of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = m[1] || "";
    if (/\bsrc=/i.test(attrs)) continue;
    // ESM 内联模块（如 pdf.js 4.x 页面）不能在 harness 的 new Function 里按经典脚本执行，跳过
    if (/type\s*=\s*["']?module/i.test(attrs)) continue;
    if (/type\s*=\s*["']?(application|text\/template|text\/tailwindcss|text\/js-worker)/i.test(attrs)) continue;
    out.push(m[2]);
  }
  return out.filter((c) => c.trim().length > 40).join("\n");
}

/**
 * 提取 HTML 内联事件属性（oninput / onclick / onchange …）。
 * 很多工具页不用 addEventListener，而是直接在标签上写 oninput="encode()"，
 * stub 若不解析这些属性，注入输入后永远触发不到转换逻辑。
 */
function inlineHandlers(html) {
  const map = {};
  for (const m of html.matchAll(/<[a-zA-Z][^>]*\bid="([^"]+)"[^>]*>/g)) {
    const tag = m[0];
    const id = m[1];
    for (const h of tag.matchAll(/\bon(input|change|click|keyup|blur|submit)\s*=\s*"([^"]*)"/gi)) {
      const code = h[2]
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, "&")
        .replace(/&#39;/g, "'")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">");
      if (!code.trim()) continue;
      (map[id] = map[id] || {})[h[1].toLowerCase()] = code;
    }
  }
  return map;
}

// expect 匹配口径：除了原文命中，也接受「原文的 HTML 转义形态」命中。
// 原因：页面若用 ToolBox.escHtml() 把结果写进 innerHTML（如 data/calc-2 的 pretty JSON），
// 真机渲染后用户看到的是原文（引号、尖括号正常），而桩内保留的 innerHTML 字符串是转义形态
// （&quot; / &lt;）。这是「桩只存原始 innerHTML、不建模实体解码」造成的口径差，不是页面缺陷；
// 故对断言做等价匹配，避免把正确的页面判红。
function htmlEscaped(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
function blobHasWant(blob, want) {
  return blob.includes(want) || blob.includes(htmlEscaped(want));
}

function collectStrings(elements) {
  // 收集所有「可能被写入结果」的字符串：value 与 innerHTML
  const seen = [];
  for (const [id, el] of Object.entries(elements)) {
    const v = el && el.value !== undefined && el.value !== "" ? String(el.value) : "";
    const h = el && el.innerHTML ? String(el.innerHTML) : "";
    const tc = el && el.textContent !== undefined && el.textContent !== "" ? String(el.textContent) : "";
    // el.value 恒为纯文本（input/textarea 的 value 不含 HTML 标签），对它剥标签是语义错误：
    // 结果本身就是尖括号语法时会被整块当标签吃掉 ⇒ 期望值永远匹配不上，而页面其实是对的。
    // 实测 it/base85-encode：Ascii85 输出 <~BOu!rDZ~> 被剥成空串（字符码核对为
    // 60,126,66,79,117,33,114,68,90,126,62，页面实现无误）。仅 innerHTML / textContent
    // 保留剥标签 —— 只有这两者才可能含真实标签。
    if (v && v.trim()) seen.push(v.replace(/\s+/g, " ").trim());
    for (const s of [h, tc]) {
      if (s && s.trim()) seen.push(s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
    }
  }
  return seen.join("\n");
}

// 专供 document.createElement 返回的临时元素：建模「写 textContent → 读 innerHTML」的 HTML 转义，
// 与真实浏览器一致（& < > 转义，引号不转义，正是 innerHTML 读回的行为）。
function makeEscEl() {
  const el = makeEl("");
  let tc = "";
  Object.defineProperty(el, "textContent", {
    get() { return tc; },
    set(v) {
      tc = String(v == null ? "" : v);
      el.innerHTML = tc.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    },
    configurable: true,
  });
  return el;
}

// 最小 XML DOM 桩（仅对声明 domParser:true 的用例注入）：harness 没有浏览器 DOMParser，
// XML 类页面在门禁中恒抛 "DOMParser is not defined"，只能退化成默认态回显的假绿
// （旧 it/xml-formatter 用例即如此）。此处提供元素/属性/文本/CDATA/注释 + parsererror
// 的最小实现，让页面真实走完 parseFromString → 序列化 → 结果落盘。其它用例行为完全不变。
function makeXmlDomParserStub() {
  const ELEMENT = 1, TEXT = 3, CDATA = 4, COMMENT = 8;
  class XNode {
    constructor(type, name) {
      this.nodeType = type;
      this.nodeName = name || "";
      this.tagName = type === ELEMENT ? name : undefined;
      this.attributes = [];
      this.childNodes = [];
      this.parentNode = null;
      this._text = "";
    }
    get children() {
      return this.childNodes.filter((c) => c.nodeType === ELEMENT);
    }
    get textContent() {
      if (this.nodeType === TEXT || this.nodeType === CDATA || this.nodeType === COMMENT) return this._text;
      return this.childNodes.map((c) => c.textContent).join("");
    }
    set textContent(v) {
      this._text = v == null ? "" : String(v);
      this.childNodes = [];
    }
  }
  const decodeEntities = (v) =>
    v.replace(/&(?:lt|gt|amp|quot|apos|#\d+|#x[0-9a-fA-F]+);/g, (m) => {
      if (m === "&lt;") return "<";
      if (m === "&gt;") return ">";
      if (m === "&amp;") return "&";
      if (m === "&quot;") return '"';
      if (m === "&apos;") return "'";
      const hex = /^&#x/i.test(m);
      return String.fromCodePoint(parseInt(m.slice(hex ? 3 : 2, -1), hex ? 16 : 10));
    });
  const parse = (src) => {
    const s = String(src);
    let i = 0, root = null, broken = false;
    const stack = [];
    const mk = (type, name, text) => {
      const n = new XNode(type, name);
      n._text = text;
      return n;
    };
    const append = (node) => {
      if (stack.length) {
        const p = stack[stack.length - 1];
        node.parentNode = p;
        p.childNodes.push(node);
      } else if (node.nodeType === ELEMENT && !root) {
        root = node;
      }
    };
    while (i < s.length) {
      if (s[i] === "<") {
        if (s.startsWith("<!--", i)) {
          const end = s.indexOf("-->", i + 4);
          if (end < 0) { broken = true; break; }
          append(mk(COMMENT, "#comment", s.slice(i + 4, end)));
          i = end + 3;
        } else if (s.startsWith("<![CDATA[", i)) {
          const end = s.indexOf("]]>", i + 9);
          if (end < 0) { broken = true; break; }
          append(mk(CDATA, "#cdata-section", s.slice(i + 9, end)));
          i = end + 3;
        } else if (s.startsWith("<?", i)) {
          const end = s.indexOf("?>", i);
          if (end < 0) { broken = true; break; }
          i = end + 2;
        } else if (s.startsWith("<!", i)) {
          const end = s.indexOf(">", i);
          if (end < 0) { broken = true; break; }
          i = end + 1;
        } else if (s[i + 1] === "/") {
          const end = s.indexOf(">", i);
          if (end < 0) { broken = true; break; }
          const name = s.slice(i + 2, end).trim();
          const top = stack.pop();
          if (!top || top.tagName !== name) broken = true;
          i = end + 1;
        } else {
          let j = i + 1;
          const nm = /^[A-Za-z_][\w:.-]*/.exec(s.slice(j));
          if (!nm) { broken = true; break; }
          const node = new XNode(ELEMENT, nm[0]);
          j += nm[0].length;
          for (;;) {
            while (j < s.length && /\s/.test(s[j])) j++;
            if (s.startsWith("/>", j)) { append(node); i = j + 2; break; }
            if (s[j] === ">") { append(node); stack.push(node); i = j + 1; break; }
            const am = /^([A-Za-z_:][\w:.-]*)\s*=\s*(?:"([^"]*)"|'([^']*)')/.exec(s.slice(j));
            if (!am) { broken = true; break; }
            node.attributes.push({ name: am[1], value: decodeEntities(am[2] != null ? am[2] : am[3]) });
            j += am[0].length;
          }
          if (broken) break;
        }
      } else {
        const end = s.indexOf("<", i);
        const stop = end < 0 ? s.length : end;
        append(mk(TEXT, "#text", decodeEntities(s.slice(i, stop))));
        i = stop;
      }
    }
    if (stack.length) broken = true;
    const errors = broken ? [mk(ELEMENT, "parsererror", "XML 解析错误")] : [];
    return {
      documentElement: root,
      getElementsByTagName: (name) => (name === "parsererror" ? errors : []),
    };
  };
  return class {
    parseFromString(src) { return parse(src); }
  };
}

// HTML 版 DOMParser 桩：XML 桩只给 documentElement，够 xml-* 用，但 HTML 页需要真实 DOM 树
// （doc.body、children、querySelectorAll(':scope > tr')、parentElement 等，html-to-markdown 全靠这些）。
// 用 jsdom（已是 devDependency，en-CJK 探针等门禁同款）兜底，只在用例声明 `htmlDom: true` 时装配，
// 与 XML 桩互斥使用，其它页面基线不受影响。
function makeHtmlDomParserStub() {
  return class {
    parseFromString(src, type) {
      const { JSDOM } = require("jsdom");
      const str = String(src == null ? "" : src);
      if (type && /xml/i.test(String(type))) {
        try { return new JSDOM(str, { contentType: "text/xml" }).window.document; } catch (e) { /* 非法 XML 退化成 HTML */ }
      }
      return new JSDOM(str, { contentType: "text/html" }).window.document;
    }
  };
}

// 实际执行过的用例数（redirect 存根不计）：供「0 用例拒绝判绿」守卫使用。
// 全站 200+ 个 verify_<ind>_calc.js 都复用本 harness，故此处一处收口即可覆盖。
let __executedCases = 0;

async function runCase(c) {
  // 每个用例都会往 globalThis（当作 window）挂函数，用后清理，避免污染下一个用例
  const before = new Set(Object.keys(globalThis));
  // 保护 Node 关键全局：页面脚本可能覆盖 process/console（如 biz/zalgo-text），
  // 用例结束后还原，避免后续 main() 调 process.exit 时因 process 被删而崩溃。
  const _proc = globalThis.process;
  const _console = globalThis.console;
  try {
    const r = await runCaseInner(c);
    if (!r.skipped) __executedCases++;
    return r;
  } finally {
    __browserInit = false; // 开关只对本用例生效，绝不泄漏到后续用例
    for (const k of Object.keys(globalThis)) {
      if (!before.has(k)) { try { delete globalThis[k]; } catch (e) { /* 只读属性跳过 */ } }
    }
    globalThis.process = _proc;
    globalThis.console = _console;
  }
}

async function runCaseInner(c) {
  _rngReset(); // 每个用例前重置随机种子，确保随机页输出与顺序/环境无关
  // afterLoad（opt-in）：开启浏览器保真初始化（innerHTML→children、空 select 自动选首项），
  // 并在 DOMContentLoaded 回调执行后让出一帧。默认 false ⇒ 既有用例路径逐字节不变。
  __browserInit = !!c.afterLoad;
  // 动态 DOM 登记默认关闭：只有声明 clicks（模拟点击）或 dynDom 的用例才启用 ⇒
  // 既有用例的行为逐字节不变（§7.1 的历史教训：全站无差别生效会误伤其它页）。
  dynReset();
  // dynInputs（opt-in）：innerHTML 生成的 input 默认值登记，须在页面脚本执行前就位。
  __dynInputs = !!c.dynInputs;
  __dynInputReg.clear();
  DYN.on = !!(c.dynDom || (Array.isArray(c.clicks) && c.clicks.length > 0));
  // XML 类页面需要浏览器 DOMParser；仅对显式声明 domParser:true 的用例注入（用后清理）。
  if (c.domParser && typeof globalThis.DOMParser === "undefined") {
    globalThis.DOMParser = makeXmlDomParserStub();
  }
  // HTML 类页面要真实 DOM 树，XML 桩不够用 ⇒ 用 jsdom 版（见 makeHtmlDomParserStub 注释）
  if (c.htmlDom && typeof globalThis.DOMParser === "undefined") {
    globalThis.DOMParser = makeHtmlDomParserStub();
  }
  const file = path.join(TOOLS_DIR, c.slug + ".html");
  if (!fs.existsSync(file)) return { ok: false, why: "文件不存在" };
  const html = fs.readFileSync(file, "utf8");
  // 重定向存根（TOOLBOX-REDIRECT）无 calcTool，跳过（与 scripts/verify_calc.js 既有逻辑一致）
  if (html.includes("TOOLBOX-REDIRECT")) return { ok: true, skipped: true, why: "redirect stub" };

  const defaults = {};
  const inputAttrs = {};
  for (const m of html.matchAll(/<input\b([^>]*)>/gi)) {
    const id = (m[1].match(/\bid\s*=\s*["']([^"']+)["']/i) || [])[1];
    if (id) inputAttrs[id] = m[1];
  }
  for (const m of html.matchAll(/<input[^>]*id="([^"]+)"[^>]*value="([^"]*)"/g)) defaults[m[1]] = m[2];
  for (const m of html.matchAll(/<textarea[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/textarea>/g))
    defaults[m[1]] = m[2].replace(/&#10;/g, "\n").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
  // G06-S1：readonly 输出域（<textarea readonly>/<input readonly>）的 .value 就是用户首屏
  // 可见答案，但 textarea 设 .value 不反映到 innerHTML ⇒ 快照只带 ih 会漏判整类页面
  // （it/* 编码/密码族全族输出皆是 readonly textarea）。预解析哪些 id 带 readonly，
  // 供 snapshotOnly 快照打 ro 标记；不传 snapshotOnly 时该集合无人读取，零影响。
  const readonlyIds = new Set();
  for (const m of html.matchAll(/<(?:input|textarea)\b[^>]*>/gi)) {
    const tag = m[0];
    if (!/\breadonly\b/i.test(tag)) continue;
    const id = (tag.match(/\bid\s*=\s*["']([^"']+)["']/i) || [, ""])[1];
    if (id) readonlyIds.add(id);
  }
  // G06-S1：checkbox/radio 的 HTML `checked` 默认态经 getElementById 路径同样要可见。
  // makeEl.checked 恒 false ⇒ 页面读 `document.getElementById('x').checked` 恒得 false，
  // 默认态走「未勾选」分支（token-generator「请至少选择一种字符集」、
  // recovery-code-generator「请选择字符类型」、password-generator 空口令等），
  // 与真机（默认已勾选 ⇒ 直接出结果）不符 ⇒ 首屏恒空。此处预解析带 id 的默认勾选控件。
  const checkedIds = new Set();
  const sel = {};
  for (const m of html.matchAll(/<select[^>]*id="([^"]+)"[\s\S]*?<\/select>/g)) {
    const block = m[0];
    // 一并保留 option 标签的原始属性串（data-* 等），供 mkOpt 解析 dataset/getAttribute：
    // 页面常从选中项的 data-* 上取业务数值（forex 的 data-pip、allergen-cross-risk 的
    // data-score），只解析 value/text 会让这些页读不到数而恒输出占位符（「—」）。
    sel[m[1]] = [...block.matchAll(/<option([^>]*)>([\s\S]*?)<\/option>/g)]
      .map((x) => {
        const tx = x[2].replace(/<[^>]+>/g, "").trim();
        // 浏览器语义（2026-11-05）：<option> 无 value 属性时，其 .value 等于选项文本
        // （music-scale-reference 的 #root 12 个音名选项即此形态；旧桩恒给 "" ⇒
        // notes.indexOf("") = -1 ⇒ note undefined ⇒ render() 抛
        // "Cannot read properties of undefined (reading 'includes')"）。
        const vm = (x[1] || "").match(/value\s*=\s*["']([^"']*)["']/i);
        return { value: vm ? vm[1] : tx, text: tx, attrs: x[1] || "" };
      });
  }

  // 预解析 radio / checkbox 的 HTML 默认选中态（2026-09-24）：
  // 真机中带 `checked` 属性的控件即处于选中态。makeEl.checked 恒 false ⇒ 页面读选中项时
  // 得到 null / 恒空：`querySelector('input[name=design]:checked').value` 会抛 TypeError
  // （optical/progressive-corridor 因此整页无法验证），`getElementsByName(name)` 循环恒不命中
  // ⇒ 单选组读数恒 0，默认输出与真机不符。用例未声明 c.checks / c.radios 时回落到此处。
  const checkedByName = {};    // name -> [全部带 checked 的 value]（radio 组天然 1 个；checkbox 组可多个）
  const radioGroups = {};      // name -> [全部 value]（保持文档序）
  for (const m of html.matchAll(/<input\b[^>]*>/gi)) {
    const tag = m[0];
    if (!/type\s*=\s*["']?(?:radio|checkbox)/i.test(tag)) continue;
    const nm = (tag.match(/\bname\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const id = (tag.match(/\bid\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const vl0 = (tag.match(/\bvalue\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    // 无 name 的控件按 id 归组（真机里 checkbox 常无 name，页面用 id 读取）
    const key = nm || (id ? "#" + id : "");
    if (!key) continue;
    (radioGroups[key] = radioGroups[key] || []).push(vl0);
    if (/\bchecked\b/i.test(tag)) {
      (checkedByName[key] = checkedByName[key] || []).push(vl0);
      if (id) checkedIds.add(id);   // getElementById(id).checked 路径同样要见默认勾选态
    }
  }

  const script = inlineScripts(html);
  if (!script.trim()) return { ok: false, why: "无内联脚本" };

  // 还原页面标题 / h1 / label 文本：很多工具用 document.querySelector('h1').textContent
  // （或 title）做「计算模式分支」选择，stub 若不提供真实文本会落入兜底零值分支，导致验证失真。
  const stripTags = (s) => s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const h1Text = stripTags((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i) || [,""])[1]);
  const titleText = stripTags((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [,""])[1]);
  const labelTexts = [...html.matchAll(/<label[^>]*>([\s\S]*?)<\/label>/gi)].map((m) => stripTags(m[1]));

  // 2026-09-27：<select> 的 HTML 默认选中态此前完全未建模，只建模了 input radio/checkbox。
  // 后果：`document.querySelector('#brand option:checked').text`（真机返回选中 option，
  // 属性 `.text` = 选项标签）在 stub 里恒为 null ⇒ 页面读 `.text` 抛
  // "Cannot read properties of null"，整页无产物（usedcar 的 calc-73 / estimate-38 /
  // ershouchetanpanyijiakongjianyuce 等页）。此处补齐 select 默认选中态与选项标签文本。
  const selectedText = {};   // key -> 选中项标签文本（真机 option.text / textContent）
  for (const m of html.matchAll(/<select[^>]*\bid\s*=\s*["']([^"']+)["'][\s\S]*?<\/select>/g)) {
    const key = "#" + m[1];
    const opts = [...m[0].matchAll(/<option([^>]*)>([\s\S]*?)<\/option>/g)];
    if (!opts.length) continue;
    const hit = opts.find((o) => /\bselected\b/i.test(o[1])) || opts[0];
    const htx = hit[2].replace(/<[^>]+>/g, "").trim();
    const hvm = hit[1].match(/\bvalue\s*=\s*["']([^"']*)["']/i);
    // 同 static sel：无 value 属性 ⇒ value 取选项文本（浏览器语义）
    const vl = hvm ? hvm[1] : htx;
    (checkedByName[key] = checkedByName[key] || []).push(vl);
    selectedText[key] = stripTags(hit[2]);
  }

  // 注入参数合法性（2026-11-05 显式报错）：以下形态过去被**静默忽略** —— 空 clicks 直接跳过
  // 点击阶段、非数组/非字符串的 checkIds / checks / radios 取值被丢弃，用例照样「变红」，
  // 等于给判别力造假证据。这里一律返回失败并点名「哪个用例的哪个字段」。
  const badFields = [];
  const isPlainObj = (v) => v && typeof v === "object" && !Array.isArray(v);
  if (c.clicks !== undefined) {
    if (!Array.isArray(c.clicks)) badFields.push("clicks 必须是字符串数组");
    else if (!c.clicks.length) badFields.push("clicks 为空数组（点击阶段会被静默跳过）");
    else c.clicks.forEach((code, i) => {
      if (typeof code !== "string" || !code.trim()) badFields.push(`clicks[${i}] 必须是非空字符串: ${JSON.stringify(code)}`);
    });
  }
  for (const fld of ["checkIds", "checks"]) {
    const v = c[fld];
    if (v === undefined) continue;
    if (!Array.isArray(v)) { badFields.push(`${fld} 必须是数组`); continue; }
    if (!v.length) { badFields.push(`${fld} 为空数组（注入阶段会被静默跳过）`); continue; }
    v.forEach((x, i) => {
      if (typeof x !== "string" || !x) badFields.push(`${fld}[${i}] 必须是非空字符串: ${JSON.stringify(x)}`);
    });
  }
  if (c.radios !== undefined) {
    if (!isPlainObj(c.radios)) badFields.push("radios 必须是 name → value 的对象");
    else for (const [nm, v] of Object.entries(c.radios)) {
      if (typeof nm !== "string" || !nm) badFields.push(`radios 含空 name: ${JSON.stringify(nm)}`);
      if (!(typeof v === "string" || typeof v === "number")) badFields.push(`radios.${nm} 取值必须是字符串/数字: ${JSON.stringify(v)}`);
    }
  }
  // 存在性：非运行期生成的 id / name 若在页面里找不到，getEl / getElementsByName 会造游离桩
  // ⇒ 注入落空但无任何报错。运行期生成（`id="'+i+'"` / `name="q'+i+'"`）无法静态判定，放行。
  const escRe = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const dynNamePrefixes = [];
  for (const m of script.matchAll(/\bname\s*=\s*(["'`])([\s\S]*?)\1/g)) {
    const inner = m[2];
    if (!/\$\{/.test(inner) && !/\s*\+\s*/.test(inner)) continue;
    dynNamePrefixes.push((inner.match(/^([A-Za-z_][A-Za-z0-9_-]*)/) || ["", ""])[1]);
  }
  const isDynName = (nm) => dynNamePrefixes.some((p) => p === "" || (nm.startsWith(p) && nm.length > p.length));
  if (Array.isArray(c.checkIds)) {
    for (const id of c.checkIds) {
      if (typeof id !== "string" || !id) continue;
      if (!new RegExp(`id\\s*=\\s*["']${escRe(id)}["']`).test(html) && !isDynamicId(html, id)) {
        badFields.push(`checkIds 指向页面不存在的 id: ${id}`);
      }
    }
  }
  if (isPlainObj(c.radios)) {
    for (const nm of Object.keys(c.radios)) {
      if (!new RegExp(`name\\s*=\\s*["']${escRe(nm)}["']`).test(html) && !isDynName(nm) && !isDynamicId(html, nm)) {
        badFields.push(`radios 的 name 在页面不存在: ${nm}`);
      }
    }
  }
  if (badFields.length) {
    return { ok: false, why: `注入参数非法（${c.slug}）: ` + badFields.join("; ") };
  }

  const inline = inlineHandlers(html);
  const elements = {};
  const getEl = (id) => {
    if (!(id in elements)) {
      // 选项来源：静态 <select>（sel）优先，其次运行期容器 innerHTML 生成的 <select>（dynSelectOf）。
      const optList = sel[id] && sel[id].length ? sel[id] : dynSelectOf(id);
      const v =
        __dynInputs && __dynInputReg.has(id)
          ? __dynInputReg.get(id)
          : c.inputs && id in c.inputs
          ? c.inputs[id]
          : defaults[id] !== undefined
          ? defaults[id]
          : optList && optList.length
          ? ((optList.find((o) => /\bselected\b/i.test(o.attrs || "")) || optList[0]).value)
          : "";
      elements[id] = makeEl(v, optList || undefined);
      if (inputAttrs[id]) {
        elements[id].tagName = "INPUT";
        elements[id].type = ((inputAttrs[id].match(/\btype\s*=\s*["']([^"']+)["']/i) || [])[1] || "text").toLowerCase();
        for (const m of inputAttrs[id].matchAll(/\b(type|min|max|step)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi))
          elements[id].setAttribute(m[1], m[2] ?? m[3] ?? m[4]);
        if (/\brequired\b/i.test(inputAttrs[id])) elements[id].setAttribute("required", "");
      }
      elements[id].id = id;   // 动态 DOM 登记按容器 id 分桶（同容器重渲染时覆盖，避免计数翻倍）
      // readonly 输出域标记（G06-S1 快照判据用）：真机中该属性只读不改，
      // 页面脚本不会写它 ⇒ 不会干扰任何既有用例的取值路径。
      if (readonlyIds.has(id)) elements[id].readOnly = true;
      // G06-S1：HTML 默认勾选的 checkbox/radio（token-generator 字符集、
      // recovery-code-generator 字符类型等）——真机默认已勾选 ⇒ 页面 boot 即出结果；
      // makeEl.checked 恒 false ⇒ harness 默认态走「未勾选」分支（提示语）⇒ 首屏判空。
      // 此处按 HTML 属性还原默认勾选态（不依赖用例声明，纯还原真机）。
      // ⚠ 仅 snapshotOnly（首屏快照 / S1 扫描器）生效：全量用例路径不应用，
      // 避免破坏既有的 29 条「默认态依赖 checked=false」用例（checkedIds 建模会改其默认分支）。
      // 全量用例用显式 clicks 置位 checkbox，不依赖此还原；S1 目标（首屏即答案）只走快照路径。
      if (c.snapshotOnly && checkedIds.has(id)) { try { elements[id].checked = true; } catch (e) {} }
      // 复选框注入：makeEl 的 checked 恒为 false，页面若用 getElementById(id).checked
      // 读取勾选态（量表/评分/选项类页面的主流写法），注入 .value 完全无效 ⇒ 该类页
      // 长期被判「结构性 no_inputs」而只能取常量串 expect（零判别力）。
      // 用例用 checkIds: ["b1","b2"] 声明哪些 id 处于选中态即可。不传该字段行为完全不变。
      if (c.checkIds && c.checkIds.indexOf(id) !== -1) elements[id].checked = true;
      // 把内联 on* 属性注册成事件处理器，使 fire() 能触发页面真实逻辑
      const ih = inline[id];
      if (ih) {
        for (const [ev, code] of Object.entries(ih)) {
          try {
            elements[id].addEventListener(ev, new Function("event", code));
          } catch (e) { /* 语法异常的内联代码忽略 */ }
        }
      }
    }
    return elements[id];
  };
  // 关键：页面普遍用 DOMContentLoaded 做初始化与事件绑定，stub 必须收集并执行这些回调，
  // 否则后续调用转换函数时内部状态（如 currentAlgo）根本没建立。
  const readyCbs = [];
  const document = {
    getElementById: getEl,
    getElementsByName: (name) => {
      // 单选组注入：页面标准写法是 document.getElementsByName(name) 遍历找 checked
      // （如 cardiology/has-bled 的 5 组风险因素）。原先恒返回 [] ⇒ 整组恒 0、页面
      // 输出与真机默认态不符。用例用 radios: { htn: "1" } 声明某组被选中的 value 即可。
      if (c.radios && Object.prototype.hasOwnProperty.call(c.radios, name))
        return [{ value: String(c.radios[name]), checked: true, name }];
      // 回落 HTML 默认选中态：返回该组全部选项，仅真机默认选中项 checked=true。
      // 该组在 HTML 里无默认选中 ⇒ 全部 false，页面循环自然落到其默认返回值（与真机一致）。
      const opts = radioGroups[name];
      if (opts && opts.length)
        return opts.map((v) => ({ value: v, checked: (checkedByName[name] || []).indexOf(v) !== -1, name }));
      return [];
    },
    getElementsByClassName: () => [],
    querySelector(sel) {
      // 与真实 DOM 对齐：查询「已选中项」时，未选中应返回 null。
      // stub 原先恒返回空元素（truthy），会让 `el ? el.value : fallback` 拿到空串 ""
      // 从而误入非默认分支（如 down-payment 的还款方式掉进等额本金）。
      // 用例可用 checks 声明选中项，此处返回首个选中值。
      if (/:checked/.test(sel)) {
        // 补桩（parentElement）：大量「量表/选项评估」类页面（如中医 Naranjo 关联性评价）
        // 读到选中项后会立即读取 `checked.parentElement.textContent` 取选项标签，
        // 缺该属性会在首个已答项抛 "Cannot read properties of undefined"，使整例无法验证。
        // 这里补一个最小桩（textContent 为空串），仅补齐属性、不改变既有语义。
        if (c.checks && c.checks.length)
          return { value: c.checks[0], checked: true, parentElement: { textContent: "" } };
        // 回落 HTML 默认选中态：选择器点名 name=xxx 时查该组；未点名则取首个有默认选中项的组。
        // 该组确实无默认选中（真机同样为空）⇒ 仍返回 null，保持与真机一致。
        // 优先命中的是 `#容器id 后代:checked`（select 的 option / 容器内的选中控件）——
        // 比「首个组」更精确，且真机里按容器定位即返回该容器选中项。
        const idM = sel.match(/^#([A-Za-z0-9_-]+)[\s>]/);
        if (idM && checkedByName["#" + idM[1]] && checkedByName["#" + idM[1]].length) {
          const lbl = selectedText["#" + idM[1]] || "";
          return { value: checkedByName["#" + idM[1]][0], text: lbl, checked: true, parentElement: { textContent: lbl } };
        }
        const nmM = sel.match(/\[\s*name\s*=\s*["']?([^"'\]]+)/);
        if (nmM) {
          if (c.radios && Object.prototype.hasOwnProperty.call(c.radios, nmM[1]))
            return { value: String(c.radios[nmM[1]]), checked: true, parentElement: { textContent: "" } };
          const vs = checkedByName[nmM[1]];
          if (vs && vs.length)
            return { value: vs[0], checked: true, parentElement: { textContent: "" } };
        } else {
          const ks = Object.keys(checkedByName);
          if (ks.length && checkedByName[ks[0]].length)
            return { value: checkedByName[ks[0]][0], checked: true, parentElement: { textContent: "" } };
        }
        return null;
      }
      // 提供真实 h1 / title 文本，供「按标题分支」的计算逻辑正确选模式
      if (/^h1$/i.test(sel)) { const e = makeEl(""); e.textContent = h1Text; e.value = h1Text; return e; }
      if (/^title$/i.test(sel)) { const e = makeEl(""); e.textContent = titleText; e.value = titleText; return e; }
      return makeEl("");
    },
    querySelectorAll(sel) {
      // 支持 ':checked' 类选择器：用例可用 checks 声明哪些复选框处于选中态
      if (/checked/.test(sel)) {
        if (c.checks)
          return c.checks.map((v) => ({ value: v, checked: true, parentElement: { textContent: "" } }));
        // 回落 HTML 默认选中态：未声明 checks 时按页面 `checked` 属性返回选中项（与真机一致）
        const nmM = sel.match(/\[\s*name\s*=\s*["']?([^"'\]]+)/);
        const idM = sel.match(/^#([A-Za-z0-9_-]+)[\s>]/);
        const ks = nmM ? (checkedByName[nmM[1]] ? [nmM[1]] : []) : (idM && checkedByName["#" + idM[1]] ? ["#" + idM[1]] : Object.keys(checkedByName));
        const out = [];
        for (const k of ks) for (const v of checkedByName[k])
          out.push({ value: v, text: selectedText[k] || v, checked: true, parentElement: { textContent: selectedText[k] || "" } });
        return out;
      }
      // 提供真实 label 文本，部分工具据此命名输出字段
      if (/label/i.test(sel)) return labelTexts.map((t) => { const e = makeEl(""); e.textContent = t; e.value = t; return e; });
      // 动态 DOM 登记（仅在用例声明 clicks/dynDom 时非空；否则 dynQuery 恒返回 []，行为与旧版一致）
      const dyn = dynQuery(sel);
      if (dyn.length) return dyn;
      return [];
    },
    // §7.4：页面 helper `escH(s)` 的标准写法是 `document.createElement('div')` → 写 textContent
    // → 读 innerHTML（借浏览器做 HTML 转义）。旧桩 `makeEl("")` 的 innerHTML 是普通属性、
    // 与 textContent 无联动 ⇒ escH() 恒返回空串 ⇒ 凡用它转义正文的工具，结果区的 <pre>/<code>
    // 正文被整块吞掉（既有盲区，见 2678 行注释）。此处只给 createElement 路径建模该联动，
    // 不改 makeEl（id 元素的行为逐字节不变 ⇒ 既有用例不受影响）。
    createElement: () => makeEscEl(),
    // 复制路径兜底（两条路径都覆盖）：`document.execCommand('copy')` 在真浏览器返回
    // true/false 而非抛错，部分页的本地复制实现直接调它（it/random-string 等）。
    execCommand: () => true,
    // SVG 类页面（accessibility/ramp-slope 等）用 createElementNS 建 svg/line/text 节点，
    // 缺此 API 整页初始化即抛 "createElementNS is not a function" ⇒ 恒不可验证。
    // 本桩不做真实命名空间渲染，仅提供与 createElement 同构的节点（含 classList/style/
    // setAttribute/getBoundingClientRect），足以让页面的构图逻辑跑完、结果区正常落盘。
    createElementNS: () => makeEscEl(),
    createTextNode: (t) => ({ textContent: t }),
    addEventListener(ev, cb) {
      if (/DOMContentLoaded|readystatechange|^load$/i.test(ev)) readyCbs.push(cb);
    },
    documentElement: { setAttribute() {}, getAttribute() { return null; }, style: {}, classList: { add() {}, remove() {}, toggle() {} } },
    body: makeEl(""),
    // <head> 元素桩：design/font-pairing 顶层 loadFonts() 用 `document.head.appendChild(link)`
    // 注入 Google Fonts <link>，缺此属性整页初始化即抛 "Cannot read properties of undefined
    // (reading 'appendChild')" ⇒ 恒不可验证。与 body 同构（appendChild 收集子节点即可，
    // 无渲染语义），对其它页面无影响（仅 font-pairing 读取 document.head）。
    head: makeEl(""),
  };
  // 真实存储语义：setItem 写入 Map、getItem 回读已写值。页面改成「写后回读才宣告成功」后，
  // 空桩（getItem 恒 null）会让回读永远失败、页面走进失败分支，用例只拿到中间态。
  // 可选注入（用例字段 storageFail: "quota" | "typeerror"）用于验证失败路径，不影响成功路径。
  const makeStorage = () => {
    const map = new Map();
    const fail = c && c.storageFail;
    return {
      getItem(k) { k = String(k); return map.has(k) ? map.get(k) : null; },
      setItem(k, v) {
        if (fail === "quota") {
          const err = new Error("quota exceeded (injected)");
          err.name = "QuotaExceededError";
          throw err;
        }
        if (fail === "typeerror") throw new TypeError("storage fail (injected)");
        map.set(String(k), String(v));
      },
      removeItem(k) { map.delete(String(k)); },
      clear() { map.clear(); },
      key(i) { return Array.from(map.keys())[i] ?? null; },
      get length() { return map.size; },
    };
  };
  const localStorage = makeStorage();
  // sessionStorage 桩：保守保留。任何页面顶层引用 sessionStorage 时，缺该全局会在求值期抛
  // ReferenceError ⇒ 整页成为「死页」（零用例即零回归）。当前站内已无页面真实使用 sessionStorage。
  const sessionStorage = makeStorage();
  const ToolBox = {
    setResult: (id, h) => { getEl(id).innerHTML = h; },
    // 页面 TOOLBOX-API-STUB 定义了 `T.$=function(id){return document.getElementById(id);}`，
    // harness 此前缺少该成员 ⇒ 凡用 ToolBox.$(id) 取元素/写结果的工具，会在入口首句抛
    // TypeError ⇒ 结果区恒空、用例永远「无法验证」（表面现象是 got 只剩 input 的 value）。
    $: (id) => getEl(id),
    validateNumberInput: () => true,
    toggleToolTheme() {},
    escHtml: (x) => String(x == null ? "" : x),
    escapeHtml: (x) => String(x == null ? "" : x),
    copy: () => {}, copyText: () => {}, toast: () => {}, showToast: () => {},
    t: (k, d) => d || k,
    // 与页面 TOOLBOX-API-STUB 保持一致：多数工具的 fmt() 直接转发到 formatNumber，
    // 缺了它依赖千分位格式化的页面会在 calc() 首行抛错，导致整页无法验证。
    formatNumber: (n, dec) => {
      if (typeof n !== "number" || isNaN(n)) return String(n);
      dec = dec != null ? dec : 0;
      return n.toLocaleString("zh-CN", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    },
    // 与 js/common.js::csvCell 同实现：导出收敛到 ToolBox.csvCell 的页面，
    // 在 `[...].map(ToolBox.csvCell)` 处若缺该成员会抛 "undefined is not a function"，
    // 使后面的 ToolBox.downloadText 覆盖根本执行不到（表面现象就是「downloadText 桩失效」）。
    csvCell: (value) => {
      let t = String(value == null ? "" : value);
      if (/^[=+\-@\t\r]/.test(t)) t = "'" + t;
      return /[",\n\r]/.test(t) ? '"' + t.replace(/"/g, '""') + '"' : t;
    },
    // 同 stub：明细表渲染。返回 HTML 字符串即可，collectStrings 会剥离标签后再断言。
    createTable: (headers, rows) => {
      let x = "<table><thead><tr>";
      (headers || []).forEach((t) => { x += "<th>" + (t == null ? "" : String(t)) + "</th>"; });
      x += "</tr></thead><tbody>";
      (rows || []).forEach((row) => {
        x += "<tr>";
        (row || []).forEach((c) => { x += "<td>" + (c != null ? String(c) : "") + "</td>"; });
        x += "</tr>";
      });
      return x + "</tbody></table>";
    },
  };
  // 剪贴板桩：真浏览器的 clipboard.writeText 恒返回 Promise（页面普遍 `.then(...)` 收尾），
  // 保真模式注入的 js/common.js.copyText 也依赖这一点；返回 undefined 会让 .then 抛 TypeError。
  const navigator = { userAgent: "node", clipboard: { writeText() { return Promise.resolve(); } } };
  // window 直接用 globalThis：内联 on* 属性编译出的函数在全局作用域执行，
  // 只能看到挂在 window（即全局）上的函数，用普通对象会导致「xxx is not defined」。
  const win = globalThis;
  const added = new Set(Object.keys(win));
  win.addEventListener = (ev, cb) => { if (/DOMContentLoaded|^load$/i.test(ev)) readyCbs.push(cb); };
  win.localStorage = localStorage;
  win.sessionStorage = sessionStorage;
  win.location = { href: "", search: "" };
  win.navigator = navigator;
  win.document = document;
  win.ToolBox = ToolBox;
  if (c.markmapStub) {
    win.markmap = {
      Transformer: class {
        transform(md) {
          const stack = [];
          let root = null;
          let headingDepth = 0;
          for (const line of String(md).split('\n')) {
            const match = line.match(/^(#{1,6})\s+(.+)$|^(\s*)[-*]\s+(.+)$/);
            if (!match) continue;
            if (match[1]) headingDepth = match[1].length;
            const depth = match[1] ? headingDepth : headingDepth + 1 + Math.floor(match[3].length / 2);
            const node = { content: match[2] || match[4], children: [] };
            while (stack.length && stack[stack.length - 1].depth >= depth) stack.pop();
            if (stack.length) stack[stack.length - 1].node.children.push(node);
            else if (!root) root = node;
            stack.push({ depth, node });
          }
          return { root };
        }
      },
      Markmap: { create(el) { el.textContent = 'MARKMAP-STUB-OK'; return { setData() {}, fit() {} }; } },
    };
  }
  // 图表页会读 CSS 变量取色（如 healthcare/tdee-calculator 的 resolveCanvasColor），
  // 没有 getComputedStyle 会在 calc() 首行抛 "getComputedStyle is not defined"。
  win.getComputedStyle = () => ({ getPropertyValue: () => "" });
  // 定时器桩（必须放在桩注入之前）：页面常用 setTimeout/requestAnimationFrame 做延迟渲染。
  // 有限次「立即执行」：预算耗尽即变 no-op，既允许合法的一次性延迟/几帧渲染，又掐断无限循环。
  // 此处定义的 safeTimer 会作为参数注入下方 ToolBox 早期桩，使桩内 debounce 复用受控定时器；
  // 否则桩的 debounce 会调用全局 setTimeout，在用例 finally 清理 window.__tbq 之后才异步触发 calc，
  // 导致依赖 clearInvalid 等队列函数的页面（如 hvac）抛未捕获异常、整批门禁误报失败。
  let _timerBudget = 100;
  const safeTimer = (f) => {
    if (typeof f !== "function") return 0;
    if (_timerBudget-- <= 0) return 0;
    try { f(); } catch (e) { /* 定时器回调异常不影响主流程 */ }
    return 0;
  };
  // 注入真实 ToolBox 早期 API 桩内容（页面已将其外链化，harness 不加载外部脚本）。
  // 以 window/document/getComputedStyle/setTimeout 为参数执行同款源，使 window.ToolBox 与生产设备一致：
  // 补全 qs/qsa/debounce/resolveCanvasColor/canvasColorWithAlpha/i18nText 等纯函数助手，
  // 并让桩内 debounce 复用受控 safeTimer，避免异步 calc 越过用例生命周期（finally 清理 __tbq 之后才触发）。
  // 必须在 win.getComputedStyle 设置之后执行，否则桩内 resolveCanvasColor 取到的 getComputedStyle 为 undefined。
  const _stubSrc = loadToolboxStubSrc();
  if (_stubSrc) {
    try {
      new Function("window", "document", "getComputedStyle", "setTimeout", _stubSrc)(win, document, win.getComputedStyle, safeTimer);
    } catch (e) { /* 桩注入失败不阻断用例 */ }
  }
  // 防御兜底：确保队列基对象存在，避免桩未注入时队列函数抛错（正常路径下桩已初始化，此处仅兜底）。
  if (!Array.isArray(win.__tbq)) win.__tbq = [];
  // 补 Option 构造器桩：new Option(text,value) 在 Node 全局不存在；部分页
  // （travel/timezone-converter-advanced）在初始化期用它动态填充 <select>，
  // 缺则抛 Option is not defined、整页死。仅挂本用例作用域，runCase 的
  // finally 会清理（不泄漏到其他用例，其他页本就不引用 Option，零影响）。
  win.Option = function (text, value) {
    return { text: text == null ? "" : String(text), value: value == null ? "" : String(value), selected: false, label: text == null ? "" : String(text) };
  };

  const names = [...script.matchAll(/^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/gm)].map((m) => m[1]);
  // 顶层 var/let/const 赋值（如 `var fmtNum = function(...){}`）：线上同样是 window 属性，
  // 同样会被后执行的 common.js 覆盖。仅在保真模式下纳入导出，避免默认路径多导名字到 globalThis。
  const varNames = [...script.matchAll(/^\s*(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=/gm)].map((m) => m[1]);
  const PRIO = ["calcTool", "calc", "calculate", "compute", "convert", "run", "update", "render"];
  const ordered = [
    ...PRIO.filter((p) => names.includes(p)),
    ...names.filter(
      (n) => !PRIO.includes(n) && /^(calc|compute|convert|update|render|do|run|encode|decode|gen|handle|apply|build|format|to[A-Z])/.test(n)
    ),
    ...names.filter((n) => !PRIO.includes(n)),
  ];

  // 定时器桩（safeTimer）已前移至桩注入之前定义，供 ToolBox 早期桩的 debounce 复用，此处不再重复定义。
  const exposeNames = TB_STUB_FIDELITY
    ? [...ordered, ...varNames.filter((n) => !ordered.includes(n))]
    : ordered;
  const expose = exposeNames.map((n) => `try{__f[${JSON.stringify(n)}]=typeof ${n}==='function'?${n}:null;}catch(e){}`).join("\n");
  let fns;
  try {
    // 保真模式下，页面里的裸 `ToolBox` 在真浏览器是「每次调用时从 window 动态解析」的活引用；
    // 而 new Function 的 ToolBox 形参会把它钉死成注入前的旧桩对象 —— common.js 整体替换
    // window.ToolBox 后，页面代码仍指向旧对象，点击里 `window.ToolBox.showToast=...` 改的却是
    // 新对象，页面的提示调用打到旧桩（no-op），表现为「保真模式下导出/复制类用例整片红」。
    // 用转发代理恢复真机的动态解析语义；默认模式仍传原桩对象，既有用例逐字节不变。
    const toolboxArg = TB_STUB_FIDELITY
    ? new Proxy({}, {
        get(_, k) {
          const T = win.ToolBox;
          if (!T) return undefined;
          const v = T[k];
          return typeof v === "function" ? v.bind(T) : v;
        },
        set(_, k, v) { if (win.ToolBox) win.ToolBox[k] = v; return true; },
        has(_, k) { return win.ToolBox ? k in win.ToolBox : false; },
        deleteProperty(_, k) { if (win.ToolBox) delete win.ToolBox[k]; return true; },
      })
    : ToolBox;
  const compiled = new Function(
      "document", "window", "console", "navigator", "localStorage", "sessionStorage", "ToolBox", "alert", "setTimeout", "requestAnimationFrame", "setInterval", "requestIdleCallback", "Date",
      `var __f={};\n${script}\n${expose}\n__f["__pageEval"]=function(c){return eval(String(c));};\n__f["__rebindGlobal"]=function(n){try{eval(n+' = window.'+n);}catch(e){}};\nreturn __f;`
    );
    fns = compiled(document, win, { log() {}, warn() {}, error() {} }, navigator, localStorage, sessionStorage, toolboxArg, () => {}, safeTimer, safeTimer, safeTimer, safeTimer, FrozenDate);
  } catch (e) {
    return { ok: false, why: "初始化失败: " + e.message.slice(0, 80) };
  }

  // 浏览器里传统 <script> 的顶层函数声明会成为 window 属性，内联 on* 才能调到；
  // 而 new Function 编译出的顶层函数只存在于函数作用域，必须先导出到 globalThis。
  for (const [n, f] of Object.entries(fns)) {
    if (typeof f === "function") { try { globalThis[n] = f; } catch (e) { /* 只读全局跳过 */ } }
  }

  // TB_STUB_FIDELITY=1：按线上真实顺序执行共享层 /js/common.js（defer → 页面内联之后、DOMContentLoaded 之前）。
  // 线上页面顶层 `function fmtNum(){}` 是 window 属性，common.js 末尾 `global.fmtNum = ...` 会把它覆盖；
  // harness 里页面声明只是 new Function 的局部绑定，因此注入后再把同名局部绑定显式重指到全局实现，
  // 才能复现「桩里绿、线上错」的遮蔽。未设置该环境变量时完全不执行，既有用例逐字节不变。
  if (TB_STUB_FIDELITY) {
    const _commonSrc = loadCommonSrc();
    if (_commonSrc) {
      try {
        // 补齐 common.js 顶层会用到的浏览器构造器，避免 ReferenceError 在到达 `global.fmtNum=...` 前中断。
        const _pre = 'var Element=function(){};Element.prototype={};' +
          'var Event=function(t){this.type=t;};' +
          'var URL=function(u){this.href=String(u);this.pathname="/";this.search="";this.hash="";};' +
          'URL.createObjectURL=function(){return "blob:x";};URL.revokeObjectURL=function(){};' +
          'var Blob=function(){this.size=0;this.type="";};' +
          'var IntersectionObserver=function(cb){this._cb=cb;};' +
          'IntersectionObserver.prototype={observe:function(){},unobserve:function(){},disconnect:function(){},takeRecords:function(){return [];}};' +
          'var matchMedia=function(){return {matches:false,media:"",addEventListener:function(){},removeEventListener:function(){},addListener:function(){},removeListener:function(){}};};';
        if (!document.execCommand) document.execCommand = () => true;
        new Function(
          "window", "document", "navigator", "localStorage", "sessionStorage", "location", "history",
          "alert", "confirm", "prompt", "setTimeout", "setInterval", "requestAnimationFrame",
          "MutationObserver", "Option", "URLSearchParams", "Storage", "fetch", "XMLHttpRequest", "Image",
          _pre + _commonSrc
        )(
          win, document, navigator, localStorage, sessionStorage, win.location, { pushState() {}, replaceState() {} },
          () => {}, () => true, () => "", safeTimer, safeTimer, safeTimer,
          globalThis.MutationObserver, win.Option, globalThis.URLSearchParams || function () {}, globalThis.Storage,
          () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }), function () {}, function () {}
        );
      } catch (e) {
        win.__tbFidelityError = e && e.message;
      }
      if (TB_FIDELITY_DEBUG) {
        NODE_STDERR.write("[fidelity] err=" + win.__tbFidelityError + " fmtNum=" + (typeof win.fmtNum) + " ToolBox=" + (typeof win.ToolBox) + "\n");
      }
      // 页面顶层声明与共享层重名时，以共享层实现为准（等价线上的后执行覆盖）。
      for (const [n, f] of Object.entries(fns)) {
        if (typeof f === "function" && typeof win[n] === "function" && win[n] !== f && typeof fns.__rebindGlobal === "function") {
          fns.__rebindGlobal(n);
        }
      }
      // 共享层新增的全局（页面未声明同名）也要能被页面代码/点击代码按裸标识符调用。
      for (const n of ["ToolBox", "fmtNum", "copyText", "copyToClipboard", "showToast", "toggleToolTheme",
        "resolveCanvasColor", "canvasColorWithAlpha", "i18nText", "canvasExportError", "Chain"]) {
        if (typeof win[n] !== "undefined") { try { globalThis[n] = win[n]; } catch (e) { /* 只读跳过 */ } }
      }
    }
  }

  const errs = [];

  // 1) 执行 DOMContentLoaded 回调（完成初始化与事件绑定）
  const pending = [];
  // 1.0) snapshotOnly 专用 TBKit 桩：生产 TBKit（/js/tool-kit.js）走 CDN，harness 不可加载
  // ⇒ 首屏答案/参考表靠 TBKit.matrix.table、TBKit.chart.* 渲染的页面，快照里恒空、被 S1
  // 扫描器系统性误判（实证：it/base64-converter 的 boot 即调 __b64RenderCompare 渲染
  // 算法实测长度表，桩缺失时整段抛错、表格从不落 DOM）。此处按生产 API 形状给最小桩：
  //   - matrix.table：rows 非空即落真表格 HTML（与生产一致：空历史不画表）
  //   - chart.*：series/data 含有限数字才落数据文本摘要（空图表不写，与生产一致）
  //   - history：进程内数组；preset/export/share/util 其余按形状给 no-op 或简易实现
  // 仅 snapshotOnly 注入、快照返回前删除 ⇒ 非快照路径（既有全部用例）逐字节不变。
  if (c.snapshotOnly) {
    const __hist = [];
    const __noop = () => {};
    const __resolve = (sel) => {
      const m = String(sel || "").match(/^#([A-Za-z0-9_-]+)/);
      return m ? getEl(m[1]) : null;
    };
    const __numIn = (arr) => (arr || []).some((v) => (typeof v === "number" && isFinite(v)) || (v && typeof v === "object" && typeof v.value === "number" && isFinite(v.value)));
    const __chartHasNum = (o) => __numIn((o.series || [])[0] && (o.series || [])[0].data) || (o.series || []).some((s) => __numIn(s.data)) || __numIn(o.data) || __numIn(o.points);
    const __tableHtml = (o) => {
      let h = "<table>";
      if (o.head) h += "<tr>" + o.head.map((x) => "<th>" + String(x == null ? "" : x) + "</th>").join("") + "</tr>";
      if (o.rows) for (const r of o.rows) h += "<tr>" + (r || []).map((x) => "<td>" + String(x == null ? "" : x) + "</td>").join("") + "</tr>";
      return h + "</table>";
    };
    const __chartWrite = (sel, o) => {
      const el = __resolve(sel);
      if (!el || !o || !__chartHasNum(o)) return;
      const labels = (o.labels || []).map(String).join(",");
      const series = (o.series || []).map((s) => String(s.name || "") + ":[" + (s.data || []).map((v) => (v == null ? "" : String(v))).join(",") + "]").join(" ");
      const data = o.data ? " data:[" + o.data.map((v) => (v && typeof v === "object" ? String(v.value) : String(v))).join(",") + "]" : "";
      el.innerHTML = "<div>" + String(o.title || "") + " " + labels + " " + series + data + "</div>";
    };
    const __erf = (x) => { const s = x < 0 ? -1 : 1; x = Math.abs(x); const t = 1 / (1 + 0.3275911 * x); const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; };
    const __group = (impl) => new Proxy(impl, { get(t, k) { return k in t ? t[k] : __noop; } });
    const __TBKit = new Proxy({}, {
      get(t, k) {
        if (k in t) return t[k];
        t.util = __group({
          isEn: () => false, exportTable: __noop, exportCsv: __noop, diffBox: __noop, toast: __noop,
          parseList: (s) => String(s == null ? "" : s).split(/[,，\n]/).map((x) => x.trim()).filter(Boolean),
          fmt: (n, d) => (typeof n === "number" && isFinite(n) ? n.toFixed(d == null ? 2 : d) : String(n == null ? "" : n)),
          tCrit: () => 1.96, tP: () => 1, fP: () => 1,
          normCdf: (x) => 0.5 * (1 + __erf(Number(x) / Math.SQRT2)),
        });
        t.matrix = __group({ table: (sel, o) => { const el = __resolve(sel); if (el && o && o.rows && o.rows.length) el.innerHTML = __tableHtml(o); } });
        t.chart = __group({ line: __chartWrite, bar: __chartWrite, pie: __chartWrite, gauge: __chartWrite, scatter: __chartWrite, timeline: __chartWrite, bell: __chartWrite, histogram: __chartWrite, rangeBar: __chartWrite });
        t.history = __group({
          list: () => __hist.slice(), last: () => (__hist.length ? __hist[__hist.length - 1] : null),
          record: (r) => { __hist.push(r); if (__hist.length > 50) __hist.shift(); },
          mount: __noop, clear: () => { __hist.length = 0; }, diffLast: () => null,
        });
        t.preset = __group({ bar: __noop });
        t.export = __group({ csv: __noop });
        t.share = __group({ params: () => ({}) });
        return t[k];
      },
    });
    globalThis.TBKit = __TBKit;
  }
  for (const cb of readyCbs) {
    try { const r = cb(); if (r && typeof r.then === "function") pending.push(r); }
    catch (e) { errs.push("ready: " + e.message.slice(0, 50)); }
  }
  // afterLoad（opt-in）：DOMContentLoaded 回调已按浏览器顺序执行完，再让出一帧，
  // 覆盖加载事件中追加的同步初始化，之后才进行用例注入。默认路径不等 ⇒ 零变化。
  if (c.afterLoad) await new Promise((r) => setTimeout(r, 0));
  // 1.5) snapshotOnly 快照模式（G06-S1 首屏扫描用）：只取「页面初始化后、harness 注入/兜底
  // 调用前」的真实默认态。兜底函数循环会以无参方式调用页面函数（如 selectDate()、
  // dijkstra()），部分页面会因此把结果区改写成垃圾值甚至死循环，掩盖真实首屏状态。
  // 该模式为纯增量开关：不传 snapshotOnly 时后续流程逐字节不变（既有用例零影响）。
  if (c.snapshotOnly) {
    // 异步 boot 落盘等待（G06-S1）：crypto.subtle / 自实现异步哈希（uuid-v5 的 SHA-1、
    // otp-generator 的 HMAC）在 readyCbs 里以 fire-and-forget 方式触发
    // （try{ generate(); }catch(e){} 丢弃 promise）⇒ 同步快照早于结果写入、首屏假空。
    // 先等 readyCbs 捕获到的 pending（有则等落盘，800ms 上限防挂死），
    // 再给固定节拍让未捕获的异步链（webcrypto 线程池 / microtask）跑完。
    // 页面 setTimeout 走 safeTimer 立即执行，唯一真异步源是 crypto.subtle。
    if (pending.length) {
      try {
        await Promise.race([
          Promise.allSettled(pending),
          new Promise((r) => setTimeout(r, 800)),
        ]);
      } catch (e) { /* 单个 pending 失败不影响快照 */ }
    }
    await new Promise((r) => setTimeout(r, 120));
    const blobS = collectStrings(elements);
    try { delete globalThis.TBKit; } catch (e) { /* 全局不可删时忽略 */ }
    return {
      ok: false,
      why: "snapshot-only",
      errs: errs.slice(0, 3),
      tried: ordered.slice(0, 6),
      sample: blobS.slice(0, 300),
      fullBlob: blobS,
      els: Object.fromEntries(
        Object.entries(elements).map(([k, v]) => [
          k,
          { ih: String((v && v.innerHTML) || ""), val: String((v && v.value) ?? ""), ro: !!(v && v.readOnly), tc: String((v && v.textContent) ?? "") },
        ])
      ),
    };
  }
  // 2) 覆盖输入并触发真实的 input/change 事件（最贴近用户实际操作）
  if (c.inputs) {
    for (const [id, v] of Object.entries(c.inputs)) {
      const el = getEl(id);
      el.value = v;
      for (const ev of ["input", "change", "keyup"]) {
        try { const r = el.fire(ev); if (r && typeof r.then === "function") pending.push(r); }
        catch (e) { errs.push(id + "." + ev + ": " + e.message.slice(0, 40)); }
      }
    }
    await Promise.allSettled(pending);   // async 处理函数（如 crypto.subtle）需等其落盘
    const blob1 = collectStrings(elements);
    for (const want of (c.expect || [])) {
      if (blobHasWant(blob1, want)) return { ok: true, via: "input event" };
    }
  }
  // 2.5) 模拟用户点击：click 驱动型页面（选项是 span/div + onclick，页面里根本没有表单控件）。
  // 用例声明 clicks: ["pick(0,3)", …]，按序在页面作用域内执行，等价于用户逐项作答；
  // 需动态 DOM 登记配合（pick() 内部会 querySelectorAll('.q-item') 回改选中样式）。
  if (Array.isArray(c.clicks) && c.clicks.length) {
    // 在「页面作用域」内执行：页面顶层 var（如 selLoc / ausData / checkedSym）是 var 声明，
    // 不会导出到 globalThis（只有 function 会），故用编译期保留的 __pageEval 走直接 eval
    // ⇒ 点击代码能读写页面私有状态（等价用户点选）。无 __pageEval 时回退全局 new Function。
    const pageEval = typeof fns.__pageEval === "function" ? fns.__pageEval : (code) => new Function(String(code))();
    for (const code of c.clicks) {
      try { pageEval(code); }
      catch (e) { errs.push("click:" + String(code).slice(0, 24) + ": " + e.message.slice(0, 40)); }
    }
    await Promise.allSettled(pending);
    const blobC = collectStrings(elements);
    for (const want of (c.expect || [])) {
      if (blobHasWant(blobC, want)) return { ok: true, via: "click" };
    }
  }
  // 2.6) 复制回调验证（copyCheck，opt-in）：断言复制函数同步不抛、writeText 的 then 回调不抛，
  // 且写入内容与断言一致。navigator.clipboard 替换为会记录写入并在 then 内同步执行回调的桩，
  // 使回调异常能被本用例捕获（真机里该异常会被 Promise 吞掉）。
  // 字段：{ fn, args?, btnArg?, expect? }；btnArg=true 时按 `fn(...args, btn)` 调用（this 传按钮的页面）。
  if (c.copyCheck) {
    const cc = c.copyCheck;
    const cfn = fns[cc.fn] || globalThis[cc.fn];
    if (typeof cfn !== "function") return { ok: false, why: "copyCheck: 函数缺失 " + cc.fn };
    let written = "";
    let cbErr = null;
    const fakeBtn = {
      textContent: "复制", innerHTML: "复制", style: {},
      classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
      setAttribute() {}, getAttribute() { return null; }, closest() { return null; },
    };
    navigator.clipboard.writeText = (t) => {
      written = String(t);
      return { then(ok) { try { if (typeof ok === "function") ok(); } catch (e) { cbErr = e.message; } } };
    };
    try {
      if (cc.btnArg) cfn(...(cc.args || []), fakeBtn);
      else cfn({ target: { closest: () => fakeBtn } }, ...(cc.args || []));
    } catch (e) {
      return { ok: false, why: "copyCheck 抛出: " + String(e.message).slice(0, 80) };
    }
    if (cbErr) return { ok: false, why: "copyCheck 回调抛出: " + String(cbErr).slice(0, 80) };
    if (!written) return { ok: false, why: "copyCheck 未写入剪贴板" };
    if (cc.expect && !written.includes(cc.expect)) {
      return { ok: false, why: "copyCheck 内容不匹配", sample: written.slice(0, 120) };
    }
    return { ok: true, via: "copyCheck" };
  }
  // 3) 兜底：直接调用候选函数
  // 跳过「状态破坏性 / 辅助」类函数：resetAll / clearHistory / restoreHistory / saveHistory /
  // renderHistory / swapValues 等会改写输入或覆盖 res 输出，导致扰动态结果被默认值吞掉
  // （strength-1、carbon-5 等页因此假同态）。只跑真正的计算函数。
  // 另跳过 `__*Boot` 初始化钩子：它在步骤1 已随 DOMContentLoaded 执行过（预填+首屏自跑
  // 正发生在这一步），兜底循环再调一次会把 boot 内的 calc 重跑一遍、覆盖其后函数写入的
  // 输出（实证：it/decimal-encode 第三条用例——dec() 写入解码值后被 boot 重跑的 enc() 覆盖）。
  const DESTRUCTIVE = /^(reset|clear|restore|save|swap)\b|history|reset|clear|^set[A-Z]/i;
  for (const n of ordered) {
    if (DESTRUCTIVE.test(n)) continue;
    if (/^__[\w$]*Boot$/.test(n)) continue;
    const f = fns[n];
    if (!f) continue;
    try {
      const r = f();
      if (r && typeof r.then === "function") { await r; }
    } catch (e) {
      errs.push(n + ": " + e.message.slice(0, 50));
      continue;
    }
    const blob = collectStrings(elements);
    for (const want of c.expect) {
      if (blobHasWant(blob, want)) return { ok: true, via: n };
    }
  }
  const blob = collectStrings(elements);
  return {
    ok: false,
    why: "未匹配期望值",
    errs: errs.slice(0, 3),
    tried: ordered.slice(0, 6),
    sample: blob.slice(0, 300),
    fullBlob: blob,
    // §7.4 dump 专用：原始 innerHTML 快照（不剥标签），用于定位「输出存在却被采集丢掉」的情况。
    els: Object.fromEntries(
      Object.entries(elements).map(([k, v]) => [
        k,
        { ih: String((v && v.innerHTML) || ""), val: String((v && v.value) ?? "") },
      ])
    ),
  };
}

// ---------------------------------------------------------------- 用例抽取（字符串感知）
// 供反回归门禁 / 还原工具复用：括号匹配时跳过字符串字面量（' " `）内的 [ ]，
// 否则 ref/expect 含 "(100,300]" 这类字符会让匹配错位 → eval 语法报错。
function extractCases(src) {
  const marker = "const CASES = [";
  const start = src.indexOf(marker);
  if (start === -1) return null;
  const i = src.indexOf("[", start);
  let depth = 0, inStr = null, escape = false, end = -1;
  for (let k = i; k < src.length; k++) {
    const ch = src[k];
    if (inStr) {
      if (escape) { escape = false; continue; }
      if (ch === "\\") { escape = true; continue; }
      if (ch === inStr) { inStr = null; continue; }
      continue;
    }
    if (ch === '"' || ch === "'" || ch === "`") { inStr = ch; continue; }
    if (ch === "[") { depth++; continue; }
    if (ch === "]") { depth--; if (depth === 0) { end = k; break; } }
  }
  if (end === -1) return null;
  const casesSrc = src.slice(start, end + 1).replace(marker, "[");
  // eslint-disable-next-line no-eval
  return eval(casesSrc);
}

// ---------------------------------------------------------------- main
// §7.4 零用例收敛辅助：`--dump <casefile>` 把候选用例的**完整输出**打成 JSON，
// 供人工核验后回填 expect。不改既有用例的任何行为（既有用例走 CASES 分支）。
async function dumpMain(casefile) {
  const cases = JSON.parse(fs.readFileSync(casefile, "utf8"));
  const out = [];
  for (const c of cases) {
    const r = await runCase(c);
    out.push({
      slug: c.slug,
      ok: r.ok,
      why: r.why || "",
      via: r.via || "",
      errs: r.errs || [],
      tried: r.tried || [],
      out: r.ok ? "(matched)" : (r.fullBlob || r.sample || ""),
      els: r.els || {},
    });
  }
  console.log(JSON.stringify(out, null, 1));
}

async function main() {
  const only = process.argv.slice(2);
  if (only[0] === "--dump" && only[1]) return dumpMain(only[1]).then(() => 0);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.skipped) {
      pass++;
      console.log(`⏭️ ${c.slug}  SKIP (redirect stub)`);
      continue;
    }
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 200));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { runCase, CASES, inlineScripts, makeEl, collectStrings, extractCases };

// 0 用例守卫（CI 可执行性普查 2026-11-05）：用例集为空、或全部页面已变成
// TOOLBOX-REDIRECT 存根时，harness 会打印「0/0 通过」并静默 exit 0 —— 属于假绿。
// 正常跑（无 slug 过滤）时若一个真实用例都没执行，必须在 beforeExit 把退出码翻红。
process.once("beforeExit", () => {
  // TB_DISCRIM_PARENT：discriminate_check.js 的全站模式由**子进程**跑用例，父进程自身
  // 一条也不执行（已检/下限由父进程自己的产出完整性断言把关），不能按「0 用例」判红。
  if (process.argv.length <= 2 && __executedCases === 0 && !process.env.TB_DISCRIM_PARENT) {
    console.log("❌ 0 个用例实际执行（用例集为空或全部为 redirect 存根），拒绝判绿");
    process.exitCode = 1;
  }
});

// 注意：runCase 会清理用例往 globalThis（当作 window）挂的属性，process 可能被页面脚本覆盖，
// 故此处用 process.exitCode 而非 process.exit()。
if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
