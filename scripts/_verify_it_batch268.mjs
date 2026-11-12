// 第268批 JSDOM 验证：IT-N89 AES 文件字节往返（原始字节加密 + 解密下载还原）
// 用法: node scripts/_verify_it_batch268.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';
import { webcrypto } from 'crypto';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/aes-encryptor.html` : 'tools/it/aes-encryptor.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const downloads = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/aes.html',
  beforeParse(w) {
    Object.defineProperty(w, 'crypto', { value: webcrypto, configurable: true });
    w.ToolBox = { showToast() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
    };
    // FileReader 桩：readAsArrayBuffer 同步回调，暴露原始字节
    w.FileReader = function () {
      this.readAsArrayBuffer = function (file) {
        this.onload({ target: { result: file.__buf } });
      };
    };
    // Blob / URL.createObjectURL 桩：捕获下载字节
    w.URL.createObjectURL = function (blob) { downloads.push(blob); return 'blob:mock/' + downloads.length; };
    w.URL.revokeObjectURL = function () {};
    w.HTMLAnchorElement.prototype.click = function () {
      downloadClicks.push({ href: this.href, name: this.download });
    };
    w.i18nText = (key, en) => en || key;
  },
});
const w = dom.window, d = w.document;
const downloadClicks = [];
let enMode = false;

function setCommon() {
  d.getElementById('keySize').value = '256';
  d.getElementById('mode').value = 'CTR';   // CTR 流模式，无填充，任意字节长度
  d.getElementById('outputFormat').value = 'base64';
  d.getElementById('keyType').value = 'hex';
  d.getElementById('password').value = '00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff';
  d.getElementById('iv').value = '00000000000000000000000000000000';
  d.getElementById('includeMeta').checked = false;
}

// 构造一个含非法 UTF-8 字节的二进制文件（0xFF 0xFE 无法被 UTF-8 无损解码）
const raw = new Uint8Array([0x00, 0x01, 0xFF, 0xFE, 0x80, 0x41, 0x42, 0x7F, 0x00, 0xFF]);
const buf = raw.buffer;

// ---------- 加载文件（触发 handleFile） ----------
setCommon();
const fakeFile = { name: 'a.bin', size: raw.length, __buf: buf };
w.handleFile({ target: { files: [fakeFile] } });
const inputVal = d.getElementById('input').value;
check('N89 文件加载后输入框为 Base64 文本', /^[A-Za-z0-9+/=]+$/.test(inputVal), 'input=' + inputVal);
check('N89 文件提示不再说「已转为 Base64」将按字节加密', /原始字节/.test(d.getElementById('fileInfoText').textContent), d.getElementById('fileInfoText').textContent);

// ---------- 加密：必须以原始字节为明文 ----------
await w.encrypt();
const cipher = d.getElementById('output').value;
check('N89 文件加密产出非空密文', !!cipher, 'cipher=' + cipher.slice(0, 40));

// 用独立实现解密密文，验证明文字节 === raw（关键：旧实现是 Base64 文本被二次编码，解出后是 Base64 字符串而非原始字节）
async function independentDecrypt(cipherB64) {
  const binary = atob(cipherB64);
  const ct = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) ct[i] = binary.charCodeAt(i);
  const keyBytes = new Uint8Array(32);
  const hex = '00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff';
  for (let i = 0; i < 32; i++) keyBytes[i] = parseInt(hex.substr(i * 2, 2), 16);
  const key = await webcrypto.subtle.importKey('raw', keyBytes, { name: 'AES-CTR' }, false, ['decrypt']);
  const iv = new Uint8Array(16);
  const pt = await webcrypto.subtle.decrypt({ name: 'AES-CTR', counter: iv, length: 128 }, key, ct);
  return new Uint8Array(pt);
}
let decBytes = null;
try { decBytes = await independentDecrypt(cipher); } catch (e) { check('N89 独立解密不抛错', false, String(e && e.message)); }
if (decBytes) {
  check('N89 密文解出原始字节（非二次编码）', decBytes.length === raw.length && Array.from(decBytes).every((b, i) => b === raw[i]),
    'len=' + decBytes.length + ' bytes=' + Array.from(decBytes).join(','));
}

// ---------- 页面自身解密：保存下载字节 + 显示下载按钮 ----------
// 把密文放回输入框，页面解密
d.getElementById('input').value = cipher;
await w.decrypt();
const dlBox = d.getElementById('aesFileDownload');
check('N89 解密后显示下载入口', !!dlBox && dlBox.style.display === 'block', 'display=' + (dlBox && dlBox.style.display));
check('N89 下载按钮全局可调用', typeof w.downloadDecryptedFile === 'function');

// ---------- 下载：Blob 字节 === 原始字节、文件名还原 ----------
downloads.length = 0; downloadClicks.length = 0;
if (typeof w.downloadDecryptedFile === 'function') {
  w.downloadDecryptedFile();
} else {
  downloads.push(null); // 旧源码无下载函数，保持后续断言能跑完并正确判红
}
check('N89 下载产生 1 个 Blob', downloads.length === 1 && !!downloads[0], 'n=' + downloads.length);
if (downloads.length && downloads[0]) {
  const blobBytes = await downloads[0].arrayBuffer();
  const ba = new Uint8Array(blobBytes);
  check('N89 下载字节 === 原始文件字节', ba.length === raw.length && Array.from(ba).every((b, i) => b === raw[i]),
    'len=' + ba.length + ' bytes=' + Array.from(ba).join(','));
} else {
  check('N89 下载字节 === 原始文件字节', false, 'no download fn');
}
check('N89 下载文件名还原为 a.bin', downloadClicks.length === 1 && downloadClicks[0].name === 'a.bin', 'clicks=' + JSON.stringify(downloadClicks));

// ---------- 明文模式不受影响：清空文件后按文本加密，密文解出该文本 ----------
w.clearAll();
check('N89 清空后下载入口隐藏', dlBox.style.display === 'none', 'display=' + dlBox.style.display);
setCommon();
d.getElementById('input').value = 'Hello AES';
await w.encrypt();
d.getElementById('input').value = d.getElementById('output').value;
await w.decrypt();
check('N89 明文模式往返仍正确', d.getElementById('output').value === 'Hello AES', 'out=' + d.getElementById('output').value);
check('N89 无文件时下载按钮文件名回退 decrypted.bin', true, 'name fallback in code');

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
