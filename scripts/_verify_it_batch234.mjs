// 第234批探测 · IT-N278~N281（protobuf 1 条 + hmac-generator 3 条）
//  N278 protobuf 宣称解析"二进制结构"但只做 .proto 文本→JSON（口径造假）
//  N279 hmac ResText 取静态算法说明卡，历史/图表恒空
//  N280 hmac 密钥只能 UTF-8 文本，无 hex/Base64
//  N281 hmac 预设 after=copyAll 且 key 无 oninput，复制旧结果
// 用法：node scripts/_verify_it_batch234.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 170) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, escHtml: s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} },
        preset: { bar(sel, presets, cb) { w.__presets = presets; w.__presetCb = cb; } },
        history: { list() { return w.__hist || []; }, last() { return (w.__hist || []).slice(-1)[0] || null; }, record(r) { (w.__hist = w.__hist || []).push(r); }, mount() {}, clear() { w.__hist = []; } }
      };
      let cap = '';
      Object.defineProperty(w.navigator, 'clipboard', { value: { writeText(t) { cap = t; return Promise.resolve(); } }, configurable: true });
      w.__getCap = () => cap;
      // crypto.subtle 桩（JSDOM 无 WebCrypto；返回全零签名让 boot 时的 calc() 不抛错）
      if (!w.crypto) w.crypto = {};
      Object.defineProperty(w.crypto, 'subtle', { value: {
        importKey() { return Promise.resolve({}); },
        sign() { return Promise.resolve(new Uint8Array(32).buffer); }
      }, configurable: true });
    }
  });
  const w = dom.window;
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, w, d: w.document, html };
}

const PB = makeDom(OLD_DIR ? OLD_DIR + '/protobuf-parser.html' : 'tools/it/protobuf-parser.html');
const HM = makeDom(OLD_DIR ? OLD_DIR + '/hmac-generator.html' : 'tools/it/hmac-generator.html');
const rawPB = fs.readFileSync(OLD_DIR ? OLD_DIR + '/protobuf-parser.html' : 'tools/it/protobuf-parser.html', 'utf8');
const rawHM = fs.readFileSync(OLD_DIR ? OLD_DIR + '/hmac-generator.html' : 'tools/it/hmac-generator.html', 'utf8');
const ddRaw = fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8');
let bw = PB.w, hw = HM.w, hd = HM.d;

// ══════════════ N278 protobuf 口径 ══════════════
check('N278 formula-desc 不再宣称解析二进制编码结构', !/解析 Protocol Buffers 的二进制编码结构/.test(rawPB), '');
check('N278 场景/deep-dive 不再宣解析二进制消息/抓包', !/解析二进制消息|抓包排查/.test(rawPB), '');
check('N278 页面统一为 .proto 文本→结构化 JSON 口径', /\.proto.*结构化 JSON|解析 \.proto 文件/.test(rawPB), '');
// deep-dive 权威源同步
const ddSeg = (ddRaw.match(/"it\/protobuf-parser":\s*\{[\s\S]*?\n \},/) || [''])[0];
check('N278 deep-dive 源不再宣称二进制/抓包', !/按 \.proto 解析二进制消息|抓包排查 gRPC|与字节流/.test(ddSeg) && /解析的是 \.proto 定义文本/.test(ddSeg), ddSeg.slice(0, 120));

// ══════════════ N279 hmac ResText ══════════════
check('N279 ResText 不再取首个 .result-box 静态卡', !/querySelector\(['"]\.result-box['"]\)/.test(rawHM), '');
check('N279 ResText 读取 #results 结果卡', /getElementById\(['"]results['"]\)/.test((rawHM.match(/function __hmac_generatorResText\(\)\{[\s\S]*?\n\}/) || [''])[0]), '');
// 真机：填入两个不同结果卡后，ResText 应反映结果而非算法说明文本
try {
  const results = hd.getElementById('results');
  results.innerHTML = '<div class="hmac-card"><div class="name">HMAC-SHA256</div><div class="val">aabbccdd</div></div>';
  const t = hw.__hmac_generatorResText();
  check('N279 ResText 真机返回摘要值而非算法说明', /aabbccdd/.test(t) && !/Hash-based Message/.test(t), 't=' + t);
} catch (e) { check('N279 ResText 真机返回摘要值而非算法说明', false, e.message); }

// ══════════════ N280 hmac 密钥编码 ══════════════
check('N280 有密钥编码选择器（hex/base64）', /hex|Hex|base64|Base64/.test((rawHM.match(/id="key"[\s\S]{0,400}/) || [''])[0]) || /getKeyBytes\([^)]*,\s*(mode|enc|encoding)/.test(rawHM), '');
check('N280 getKeyBytes 支持按编码解释密钥', /base64|fromCharCode|parseInt\([^)]*,\s*16\)|atob/.test((rawHM.match(/function getKeyBytes\([\s\S]*?\n\}/) || [''])[0]), '');
// 真机：getKeyBytes 传 hex 模式能解出字节
try {
  const b = hw.getKeyBytes('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b', 'hex');
  const arr = Array.from(b || []);
  check('N280 hex 密钥解出 16 个 0x0b 字节', arr.length === 16 && arr.every(x => x === 11), 'len=' + arr.length + ' first=' + arr[0]);
} catch (e) { check('N280 hex 密钥解出 16 个 0x0b 字节', false, e.message); }

// ══════════════ N281 hmac 预设重算 ══════════════
check('N281 key 输入有 oninput 触发 calc', /id="key"[^>]*oninput="calc\(\)"/.test(rawHM), '');
// 真机：预设 bar 的 after 回调应是计算函数而非纯复制；检查源码 after 段
const presetSeg = (rawHM.match(/TBKit\.preset\.bar\([\s\S]*?\}\);/) || [''])[0];
check('N281 预设 after 不再指向 copyAll', !/function\(\)\s*\{\s*copyAll\(\)\s*;?\s*\}/.test(presetSeg), presetSeg.slice(-120));

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
