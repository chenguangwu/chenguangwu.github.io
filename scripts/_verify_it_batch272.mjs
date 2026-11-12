// 第272批 JSDOM 验证：IT-N315 PDF 头字节 / IT-N316 ByteRange 覆盖长度 / 假验签承诺收口
// 用法: node scripts/_verify_it_batch272.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const pagePath = () => OLD ? `${OLD}/tools/it/pdf-signature-checker.html` : 'tools/it/pdf-signature-checker.html';
const html = fs.readFileSync(pagePath(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const pdfText = '%PDF-1.7\n1 0 obj\n/ByteRange [0 8000 9000 1200]\n/Contents <AABBCCDD>\nendobj\n%%EOF\n';
const pdfBytes = Buffer.from(pdfText, 'latin1');
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/pdf-signature-checker.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, copyText() {}, exportCsv() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
      preset: { bar() {} },
    };
    w.i18nText = (z) => z;
    w.FileReader = class {
      constructor() { this.onload = null; this.onerror = null; this.result = null; }
      readAsArrayBuffer() {
        const ab = pdfBytes.buffer.slice(pdfBytes.byteOffset, pdfBytes.byteOffset + pdfBytes.byteLength);
        this.result = ab;
        if (typeof this.onload === 'function') this.onload({ target: { result: ab } });
      }
    };
  },
});
const d = dom.window.document;
Object.defineProperty(d.getElementById('file'), 'files', {
  value: [{ size: pdfBytes.length }], configurable: true,
});
dom.window.check();

const text = (id) => String((d.getElementById(id) || {}).textContent || '');
const color = (id) => String(((d.getElementById(id) || {}).style || {}).color || '');
check('N315 PDF 头显示完整版本号 %PDF-1.7', text('d_head') === '%PDF-1.7', 'head=' + text('d_head'));
check('N315 合法 PDF 头判绿', color('d_head').indexOf('success') >= 0, 'color=' + color('d_head'));
check('N316 ByteRange 原样展示', text('d_br').indexOf('/ByteRange [0 8000 9000 1200]') >= 0, 'br=' + text('d_br'));
check('N316 覆盖字节数为两段长度之和 9200 bytes', text('d_bytes') === '9200 bytes', 'bytes=' + text('d_bytes'));
check('N316 大数场景不溢出（BigInt 求和）', /BigInt\(br\[2\]\)/.test(html) && /BigInt\(br\[4\]\)/.test(html));
check('检出签名结构（回归锚）', text('result').indexOf('检测到数字签名') >= 0);
check('N316 公式文案改为两段长度之和', html.indexOf('两段长度之和（第 2 参数 + 第 4 参数）') >= 0 && html.indexOf('第 4 参数 − 第 3 参数') < 0);
check('N316 不再宣称 PKCS#7/证书链验签（场景）', html.indexOf('校验 PDF 内嵌 PKCS#7 签名与证书链') < 0 && html.indexOf('不验证 PKCS#7 内容或证书链') >= 0);
check('N316 不再输出有效/无效密码学结论（示例）', html.indexOf('显示“有效/无效/未知”') < 0 && html.indexOf('不给出“有效/无效”的密码学结论') >= 0);
check('N316 FAQ 不再虚构证书不受信提示', html.indexOf('为什么提示证书不受信？') < 0 && html.indexOf('为什么“检测到签名”不等于验签通过？') >= 0);
check('N316 结果含义/用途口径收口', html.indexOf('PDF 数字签名校验：验证文档自签名后是否被篡改') < 0 && html.indexOf('PDF 签名结构检查') >= 0);

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
