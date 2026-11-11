// 第238批探测 · IT-N294~N296（des 3 条，复核其他 Agent 已修实现）
//  N294 DES 密钥编排按 8 字节逐位 PC1，不能用 32 位打包
//  N295 64 位分组按位数组 IP→16 轮→FP，加解密可逆且匹配 FIPS 向量
//  N296 key/IV/ciphertext 非法输入显式报错，不静默补零/截断
// 用法：node scripts/_verify_it_batch238.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const HTML = OLD_DIR ? OLD_DIR + '/des.html' : 'tools/it/des.html';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 200) : ''));
}

const html = fs.readFileSync(HTML, 'utf8');
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://example.com/tools/it/des.html',
  beforeParse(w) {
    w.alert = () => {};
    w.__toasts = [];
    w.ToolBox = {
      showToast(m, type) { w.__toasts.push(String(m) + '|' + String(type || '')); },
      copyText() {}, toggleToolTheme() {}
    };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
    };
    w.TextEncoder = TextEncoder;
    w.TextDecoder = TextDecoder;
    if (!w.crypto) w.crypto = {};
    if (!w.crypto.getRandomValues) w.crypto.getRandomValues = (a) => { for (let i = 0; i < a.length; i++) a[i] = i & 255; return a; };
  }
});
const w = dom.window, d = w.document;
try { d.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}

function set(o) {
  for (const k of Object.keys(o)) {
    const el = d.getElementById(k);
    if (!el) continue;
    if (k === 'keyAsText' || k === 'pkcs7') el.checked = !!o[k];
    else el.value = o[k];
  }
}
function run(isEncrypt) {
  w.__toasts = [];
  try { isEncrypt ? w.encrypt() : w.decrypt(); } catch (e) { w.__toasts.push('THROW:' + e.message); }
  return { out: d.getElementById('output').value, toast: w.__toasts.join(' / ') };
}
function directEncrypt(keyHex, plainHex) {
  return w.bytesToHex(w.desEcb(w.hexToBytes(plainHex), w.hexToBytes(keyHex), false));
}

// ══════════════ N294 密钥编排敏感性 + FIPS 向量 ══════════════
const VEC_KEY = '0123456789abcdef', VEC_PT = '4e6f772069732074', VEC_CT = '3fa40e8a984d4815';
check('N294 FIPS DES 已知向量', directEncrypt(VEC_KEY, VEC_PT) === VEC_CT, directEncrypt(VEC_KEY, VEC_PT));
let sensitive = true;
for (let i = 0; i < 8; i++) {
  const kb = w.hexToBytes(VEC_KEY);
  kb[i] ^= 0x11;
  const ct = w.bytesToHex(w.desEcb(w.hexToBytes(VEC_PT), kb, false));
  if (ct === VEC_CT) sensitive = false;
}
check('N294 密钥每个字节均影响密文', sensitive, sensitive ? '8/8 敏感' : '存在无效字节');

// ══════════════ N295 64 位分组可逆 + 页面主流程 ══════════════
const block = w.hexToBytes('0123456789abcdef');
const sub = w.desCreateSubkeys(w.hexToBytes(VEC_KEY));
const ctBlock = w.desBlock(block, sub, false);
const back = w.desBlock(ctBlock, sub, true);
check('N295 单分组加密解密往返', w.bytesToHex(back) === '0123456789abcdef', w.bytesToHex(back));
set({ algo: 'des', mode: 'ECB', outputFormat: 'hex', key: VEC_KEY, keyAsText: false, pkcs7: false, iv: '', input: 'Now is t' });
const vec = run(true);
check('N295 页面流程匹配 FIPS 向量', vec.out === VEC_CT && /加密成功/.test(vec.toast), 'out=' + vec.out + ' toast=' + vec.toast);
set({ algo: '3des', mode: 'CBC', outputFormat: 'hex', key: '0123456789abcdef0123456789abcdef0123456789abcdef', keyAsText: false, pkcs7: true, iv: '0001020304050607', input: 'Hello, DES/3DES encryption!' });
const enc3 = run(true);
set({ input: enc3.out });
const dec3 = run(false);
check('N295 3DES-CBC+PKCS7 往返', enc3.out.length >= 32 && dec3.out === 'Hello, DES/3DES encryption!' && /解密成功/.test(dec3.toast), 'ct=' + enc3.out.slice(0, 24) + ' pt=' + dec3.out);

// ══════════════ N296 非法输入显式报错 ══════════════
set({ algo: 'des', mode: 'ECB', outputFormat: 'hex', key: 'password', keyAsText: false, pkcs7: false, iv: '', input: 'Now is t' });
const badKey = run(true);
check('N296 非 hex 密钥报错', /密钥必须是十六进制|密钥长度必须为/.test(badKey.toast) && !badKey.out, badKey.toast);
set({ key: '0123456789ab' });
const shortKey = run(true);
check('N296 短密钥不静默补零', /密钥长度必须为/.test(shortKey.toast) && !shortKey.out, shortKey.toast);
set({ key: VEC_KEY, mode: 'CBC', iv: 'abc' });
const badIv = run(true);
check('N296 非法 IV 不静默全零', /IV 必须是 16 个十六进制字符/.test(badIv.toast) && !badIv.out, badIv.toast);
set({ iv: '', mode: 'ECB', key: VEC_KEY });
const oddHex = run(false);
d.getElementById('input').value = 'abc';
const oddCipher = run(false);
check('N296 奇数 hex 密文明确报错', /密文 hex 长度必须为偶数/.test(oddCipher.toast) && !oddCipher.out, 'default=' + oddHex.toast.slice(0, 30) + ' odd=' + oddCipher.toast);
set({ input: '00112233' });
const shortCipher = run(false);
check('N296 非 8 字节倍数密文报错', /密文长度必须是 8 字节的倍数/.test(shortCipher.toast) && !shortCipher.out, shortCipher.toast);

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
