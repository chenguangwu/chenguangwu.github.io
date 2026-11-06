#!/usr/bin/env node
/**
 * IT-N550–N559 运行期 / 静态证据（第十二批）。
 *
 * 为什么不用 verify_it_calc.js：简化桩不加载 js/qrcode.js、无 canvas/Blob/URL、
 * navigator.clipboard 与 history.mount 都是 no-op，覆盖不到「真二维码矩阵 / SVG 导出 /
 * U+0022 复制按钮点击 / ≥256 字节解密往返」这些真实行为。这里用 jsdom 真机执行页面脚本。
 *
 * 用法：
 *   node scripts/_verify_batch_n550_n559.mjs
 *   SRC_DIR=/tmp/head_pages node scripts/_verify_batch_n550_n559.mjs   # 回退判别力
 * 退出码：0 全通过；1 有失败项。
 */
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = resolve(process.env.SRC_DIR || resolve(ROOT, 'tools/it'));
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  —  ' + detail : ''}`);
}
function page(slug) {
  return readFileSync(resolve(SRC, `${slug}.html`), 'utf8');
}
function load(slug) {
  const html = page(slug);
  const dom = new JSDOM(html, {
    url: `https://toolbox.local/tools/it/${slug}.html?lang=zh-CN`,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    beforeParse(w) {
      w.TextEncoder = TextEncoder;
      w.TextDecoder = TextDecoder;
      w.__toasts = [];
      w.__downloads = [];
      w.ToolBox = { showToast: (m, t) => w.__toasts.push({ m, t }), copyText: () => {}, util: { isEn: () => false } };
      w.i18nText = (k) => k || '';
      Object.defineProperty(w.navigator, 'clipboard', {
        configurable: true,
        value: { writeText: (t) => { w.__copied = t; return Promise.resolve(); } },
      });
      w.URL.createObjectURL = () => 'blob:test';
      w.URL.revokeObjectURL = () => {};
      w.Blob = function (parts, opts) {
        w.__blobParts = parts;
        w.__blobOpts = opts || {};
        return { size: parts.join('').length, type: (opts || {}).type || '' };
      };
      w.HTMLAnchorElement.prototype.click = function () {
        w.__downloads.push({ href: this.href, download: this.download });
      };
      w.HTMLCanvasElement.prototype.getContext = function () {
        return { fillStyle: '', fillRect() {} };
      };
    },
  });
  return dom.window;
}

// ---------------------------------------------------------------- IT-N550 / N551 text-qr
{
  const w = load('text-qr');
  w.eval(readFileSync(resolve(ROOT, 'js/qrcode.js'), 'utf8'));
  const text = w.document.getElementById('text');
  const matrixOf = (s) => {
    text.value = s;
    w.generate();
    const m = w.__qrMeta;
    return m ? { n: m.n, dark: m.dark.join('') } : null;
  };
  const a = matrixOf('TOOLBOX-QR-2026');
  const b = matrixOf('TOOLBOX-QR-2027');
  const a2 = matrixOf('TOOLBOX-QR-2026');
  const long = matrixOf('X'.repeat(120));
  check('N550 真 QR 编码：不同文本矩阵不同', !!a && !!b && a.dark !== b.dark);
  check('N550 真 QR 编码：同文本矩阵可复现', !!a && !!a2 && a.dark === a2.dark);
  check('N550 版本随内容增长（不写死 29）', !!a && !!long && long.n > a.n && a.n !== 29,
    a && long ? `${a.n} -> ${long.n}` : 'matrix missing');
  w.document.getElementById('fg').value = '#123456';
  w.document.getElementById('bg').value = '#fedcba';
  matrixOf('SVG-EXPORT-CHECK');
  // HEAD 版没有 downloadSVG，不要让它抛异常打断后续检查：显式记 FAIL 保留完整判别数据。
  const hasSvgExport = typeof w.downloadSVG === 'function';
  if (hasSvgExport) w.downloadSVG();
  const svg = w.__blobParts ? String(w.__blobParts[0]) : '';
  const dl = w.__downloads[w.__downloads.length - 1];
  check('N551 导出真实 SVG 矢量矩阵',
    hasSvgExport && svg.startsWith('<svg') && svg.includes('<rect') && svg.includes('#123456') && svg.includes('#fedcba'),
    `${svg.length} bytes`);
  check('N551 SVG 下载文件名与 MIME',
    hasSvgExport && !!dl && dl.download === 'qrcode.svg' && /svg/.test(w.__blobOpts.type || ''),
    dl ? dl.download : 'no downloadSVG in this build');
}

// ---------------------------------------------------------------- IT-N552 / N553 tmux（静态）
{
  const html = page('tmux-cheatsheet');
  check('N552 所有 example 无 shell 不识别的 -- 注解', !html.includes('  -- '));
  check('N552 配置示例改用 # 注释', html.includes('set -g mouse on  # '));
  check('N553 attach -d 语义修正', html.includes('-d 分离其它已连接客户端并由本客户端接管') && !html.includes('-d 不接管'));
  check('N553 kill-session -a 带 -t', html.includes('tmux kill-session -a -t work'));
}

// ---------------------------------------------------------------- IT-N554 / N555 / N556 unicode-lookup
{
  const w = load('unicode-lookup');
  const grid = w.document.getElementById('grid');
  const search = (q) => {
    w.document.getElementById('search').value = q;
    w.render();
    return grid;
  };
  const g1 = search('U+2603');
  check('N554 码点 U+2603 解析为单字符 ☃',
    g1.querySelectorAll('.unicode-card').length === 1 && g1.textContent.includes('U+2603') && g1.textContent.includes('☃'));
  const g2 = search('snowman');
  check('N554 名称 snowman 命中 U+2603',
    g2.textContent.includes('U+2603') && g2.textContent.includes('SNOWMAN'));
  check('N555 真实 Unicode 名称（非 Code Point N 占位）',
    w.lookupName(0x22) === 'QUOTATION MARK' &&
    w.lookupName(0x1F600) === 'GRINNING FACE' &&
    w.lookupName(0x4E00) === 'CJK UNIFIED IDEOGRAPH-4E00' &&
    !String(w.lookupName(0x41)).includes('Code Point'));
  const copyOf = (code) => {
    w.__copied = null;
    w.showDetail(code);
    const btn = w.document.querySelector('#detail [data-code]');
    if (btn) btn.click();
    return { btn, copied: w.__copied };
  };
  const q = copyOf(0x22);
  const bs = copyOf(0x5C);
  check('N556 U+0022 复制按钮可点击且传出双引号',
    !!q.btn && q.btn.getAttribute('data-code') === '34' && q.copied === '"', JSON.stringify(q.copied));
  check('N556 U+005C 复制按钮可点击且传出反斜杠',
    !!bs.btn && bs.btn.getAttribute('data-code') === '92' && bs.copied === '\\', JSON.stringify(bs.copied));
}

// ---------------------------------------------------------------- IT-N557 username-generator（静态）
{
  const html = page('username-generator');
  check('N557 四档风格词库与分支落地',
    html.includes('UG_STYLES') && html.includes("style==='short'") && html.includes("style==='fun'") &&
    html.includes('id="style"') && html.includes('ug-meta'));
}

// ---------------------------------------------------------------- IT-N558 / N559 xxtea
{
  const w = load('xxtea');
  const input = w.document.getElementById('input');
  const key = w.document.getElementById('key');
  const out = w.document.getElementById('output');
  const fmt = w.document.getElementById('outputFormat');
  fmt.value = 'base64';
  const roundtrip = (plain, k) => {
    input.value = plain; key.value = k; w.encrypt();
    const cipher = out.value;
    input.value = cipher; w.decrypt();
    return { cipher, plain: out.value };
  };
  const r300 = roundtrip('X'.repeat(300), 'myxxteakey');
  check('N558 300 字节明文解密不截断', r300.plain === 'X'.repeat(300), `len=${r300.plain.length}`);
  const r256 = roundtrip('Y'.repeat(256), 'myxxteakey');
  check('N558 256 字节临界值往返一致', r256.plain === 'Y'.repeat(256), `len=${r256.plain.length}`);
  const encWith = (k) => { input.value = 'SAME PLAINTEXT'; key.value = k; w.encrypt(); return out.value; };
  const a = encWith('abcdefghijklmnopQRST');
  const b = encWith('abcdefghijklmnopXXXX');
  check('N559 前 16 字节相同的两组 20 字节密钥产生不同密文', !!a && !!b && a !== b);
  input.value = 'ABC'; key.value = 'KY'; fmt.value = 'base64'; w.encrypt();
  check('N559 ≤16 字节密钥行为保持兼容', out.value === 'MaTt9vgiYH8=', out.value);
  const cipher = encWith('keyA');
  w.__toasts.length = 0;
  input.value = cipher; key.value = 'keyB'; w.decrypt();
  check('N558 错误密钥解密显式报错而非静默成功',
    w.__toasts.some((t) => t.t === 'error') && out.value === cipher,
    `toast=${JSON.stringify(w.__toasts.slice(-1))}`);
}

const failed = results.filter((r) => !r.ok);
console.log(`\n==== ${results.length - failed.length}/${results.length} 通过 ====`);
if (failed.length) {
  console.log('FAILED: ' + failed.map((r) => r.name).join(' | '));
  process.exitCode = 1;
}
