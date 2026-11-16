#!/usr/bin/env node
/**
 * 910 批复核专项：324 / 332 异步乱序后的【真实浏览器交互】证据。
 *
 * 与旧脚本 _verify_async_race_324_332.mjs 的区别：
 *  - 旧脚本 324 只核源码守卫正则、332 只用 node:vm 验 lastSVG，未验证真实下载文件内容 / 真实复制剪贴板内容；
 *  - 本脚本用 puppeteer 启动真实 Chrome、加载真实页面 DOM，通过 evaluateOnNewDocument 注入【受控异步桩】：
 *      FileReader / canvas.toBlob 真实产生数据，但 onload 回调由测试显式触发，可按任意乱序 fire；
 *    然后在真实浏览器里驱动：换图→新旧回调乱序到达→断言旧代被丢弃，
 *    并核对 332 的 navigator.clipboard.writeText 实际写入 = 最新 SVG、
 *    324 的下载 blob（downloadBlob 所用 URL）真实字节头/大小 = 最新转换结果。
 *
 * 用法：node scripts/_verify_async_race_browser_910.mjs
 * 退出码 0 = 全部通过；非 0 = 有断言失败。
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PNG = path.join(ROOT, 'logo-32.png');
let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? '  ' + extra : '')); }
}

// 在页面所有脚本执行前注入：受控异步 + 剪贴板/下载探针（函数会被序列化到浏览器执行，不能引用外部变量）
function harness() {
  window.alert = function () {}; // 防止 copyResult 成功 alert 阻塞 headless
  window.__readers = [];
  window.__images = [];
  window.__imageLoads = 0;
  window.__blobs = [];
  window.__urls = [];
  window.__downloads = [];
  window.__clipboardWrites = [];

  // FileReader：真实读到 __result，但 onload 由测试显式触发（制造乱序）
  const NativeFR = window.FileReader;
  function ControlledFR() {
    const fr = new NativeFR();
    window.__readers.push(fr);
    fr.readAsDataURL = function (file) {
      fr.__file = file;
      const native = new NativeFR();
      native.onload = function (e) { fr.__result = e.target.result; };
      native.readAsDataURL(file);
    };
    return fr;
  }
  ControlledFR.prototype = NativeFR.prototype;
  window.FileReader = ControlledFR;
  window.__fireReader = async function (i) {
    const fr = window.__readers[i];
    if (!fr) return false;
    for (let k = 0; k < 200 && fr.__result == null; k++) await new Promise(r => setTimeout(r, 10));
    if (typeof fr.onload === 'function') fr.onload({ target: { result: fr.__result } });
    return typeof fr.onload === 'function';
  };

  // Image：只计数构造次数、不改 onload（避免破坏浏览器真实加载）
  const NativeImg = window.Image;
  function ControlledImg() {
    const img = new NativeImg();
    window.__images.push(img);
    return img;
  }
  ControlledImg.prototype = NativeImg.prototype;
  window.Image = ControlledImg;

  // canvas.toBlob：真实生成 blob，但回调由测试显式触发（制造转换乱序）
  const nativeToBlob = HTMLCanvasElement.prototype.toBlob;
  HTMLCanvasElement.prototype.toBlob = function (cb, mime, q) {
    const item = { cb, ready: false, blob: null };
    window.__blobs.push(item);
    nativeToBlob.call(this, function (blob) { item.blob = blob; item.ready = true; }, mime, q);
  };
  window.__fireBlob = async function (i) {
    const it = window.__blobs[i];
    if (!it) return false;
    for (let k = 0; k < 200 && !it.ready; k++) await new Promise(r => setTimeout(r, 10));
    if (typeof it.cb === 'function') it.cb(it.blob);
    return typeof it.cb === 'function';
  };

  // URL.createObjectURL：记录 downloadBlob 实际使用的 blob
  const nativeCreate = URL.createObjectURL;
  URL.createObjectURL = function (blob) { window.__urls.push(blob); return nativeCreate.call(URL, blob); };

  // <a>.click：记录下载触发（不执行默认下载，避免污染文件系统；内容由 __urls 的 blob 核对）
  HTMLAnchorElement.prototype.click = function () {
    if (this.download) window.__downloads.push({ name: this.download });
  };

  // navigator.clipboard.writeText：记录真实复制操作写入的内容
  try {
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText: function (t) { window.__clipboardWrites.push(String(t)); return Promise.resolve(); } },
    });
  } catch (e) {}
}

async function openPage(browser, rel) {
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.log('    [页面错误] ' + (e && e.message || e)));
  await page.evaluateOnNewDocument(harness);
  await page.goto('file://' + path.join(ROOT, rel), { waitUntil: 'load' });
  return page;
}

// 在页面内生成指定颜色的 PNG，返回可构造 File 的字节数组
async function makeFileBytes(page, rgb, name) {
  return page.evaluate(({ rgb, name }) => {
    const c = document.createElement('canvas');
    c.width = 16; c.height = 16;
    const ctx = c.getContext('2d');
    ctx.fillStyle = rgb; ctx.fillRect(0, 0, 16, 16);
    const dataUrl = c.toDataURL('image/png');
    const bin = atob(dataUrl.split(',')[1]);
    const bytes = [];
    for (let i = 0; i < bin.length; i++) bytes.push(bin.charCodeAt(i));
    return { name, bytes };
  }, { rgb, name });
}

async function injectFile(page, file, inputId, dispatchChange) {
  await page.evaluate(({ file, inputId, dispatchChange }) => {
    const f = new File([Uint8Array.from(file.bytes)], file.name, { type: 'image/png' });
    const dt = new DataTransfer();
    dt.items.add(f);
    const input = document.getElementById(inputId);
    input.files = dt.files;
    if (dispatchChange) input.dispatchEvent(new Event('change', { bubbles: true }));
  }, { file, inputId, dispatchChange });
}

// ============ 332：换图乱序后，真实复制内容 = 最新 SVG ============
async function test332(browser) {
  console.log('\n[332] png-to-svg 真实浏览器换图乱序 + 剪贴板内容');
  const page = await openPage(browser, 'tools/design/png-to-svg.html');
  const fA = await makeFileBytes(page, 'rgb(200,50,80)', 'A.png');
  const fB = await makeFileBytes(page, 'rgb(20,180,90)', 'B.png');

  // 上传 A → 生成（reader 0）；换 B → 再生成（reader 1），代次递增使 A 在途作废
  await injectFile(page, fA, 'fileInput', false);
  await page.evaluate(() => generate());
  await injectFile(page, fB, 'fileInput', false);
  await page.evaluate(() => generate());

  // 乱序：新代 B 的 FileReader 回调先到 → 正常生成；旧代 A 回调后到 → 应被丢弃
  await page.evaluate(() => window.__fireReader(1));
  await page.waitForFunction(() => !!document.getElementById('svgCode').value, { timeout: 6000 });
  await page.evaluate(() => window.__fireReader(0));
  await new Promise(r => setTimeout(r, 120));

  const imgCount = await page.evaluate(() => window.__images.length);
  ok('332 乱序后仅新代创建 Image（旧代回调丢弃）', imgCount === 1, 'images=' + imgCount);

  const svg = await page.evaluate(() => document.getElementById('svgCode').value);
  const last = await page.evaluate(() => lastSVG);
  ok('332 输出 SVG 反映新代 B 的颜色', svg.includes('rgb(20,180,90)') && !svg.includes('rgb(200,50,80)'), 'svg=' + svg.slice(0, 90));
  ok('332 lastSVG 与输出一致', last === svg);

  // 真实点击复制 → 核对 navigator.clipboard.writeText 写入 = 最新 SVG
  await page.evaluate(() => copyResult());
  await new Promise(r => setTimeout(r, 120));
  const clips = await page.evaluate(() => window.__clipboardWrites);
  ok('332 真实复制内容 = 最新 SVG（非旧代）', clips.length === 1 && clips[0] === svg,
    'clip=' + String(clips[0] || '').slice(0, 90));

  await page.close();
}

// ============ 324：两次转换乱序后，真实下载 blob 内容 = 最新代 ============
async function test324(browser) {
  console.log('\n[324] image-format-converter 真机转换乱序 + 下载文件内容');
  const page = await openPage(browser, 'tools/design/image-format-converter.html');
  const bytes = Array.from(fs.readFileSync(PNG));

  // 真实上传项目 logo PNG → 走页面 handleFiles → 图片进入 state.files
  await page.evaluate((bytes) => {
    const f = new File([Uint8Array.from(bytes)], 'sample.png', { type: 'image/png' });
    const dt = new DataTransfer(); dt.items.add(f);
    const input = document.getElementById('fileInput');
    input.files = dt.files;
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }, bytes);
  await page.evaluate(() => window.__fireReader(0));
  await page.waitForFunction(() => document.querySelectorAll('#fileList .file-item').length >= 1, { timeout: 6000 });

  // 第一次转换（gen=1，toBlob 0）；再次转换触发 invalidate（gen=2，toBlob 1）
  await page.evaluate(() => convertAll());
  await page.evaluate(() => convertAll());
  const blobCount = await page.evaluate(() => window.__blobs.length);
  ok('324 两次转换各产生一个 toBlob 回调', blobCount === 2, 'blobs=' + blobCount);

  // 乱序：新代 toBlob(1) 先到 → 写结果并开放下载；旧代 toBlob(0) 后到 → 应被丢弃
  await page.evaluate(() => window.__fireBlob(1));
  await page.waitForFunction(() => !document.getElementById('downloadAllBtn').disabled, { timeout: 6000 });
  await page.evaluate(() => window.__fireBlob(0));
  await new Promise(r => setTimeout(r, 120));

  const urlCount = await page.evaluate(() => window.__urls.length);
  ok('324 乱序后仅新代产生下载 URL（旧代不开放下载）', urlCount === 1, 'urls=' + urlCount);

  // 真实点“下载当前” → downloadBlob 用结果 URL 触发 a.click，核对文件名与 blob 真实字节
  await page.evaluate(() => downloadCurrent());
  await new Promise(r => setTimeout(r, 80));
  const downloads = await page.evaluate(() => window.__downloads);
  ok('324 下载触发带正确文件名', downloads.length === 1 && /\.png$/.test(downloads[0].name), 'dl=' + JSON.stringify(downloads));

  const dl = await page.evaluate(async () => {
    const blob = window.__urls[0];
    if (!blob) return { ok: false };
    const buf = new Uint8Array(await blob.arrayBuffer());
    return {
      ok: true,
      size: blob.size,
      type: blob.type,
      isPNG: buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47,
    };
  });
  ok('324 下载 blob 是真实 PNG（字节头校验）', dl.ok && dl.isPNG, JSON.stringify(dl));
  ok('324 下载 blob 非空且 MIME 对齐', dl.ok && dl.size > 0 && /png/.test(dl.type), JSON.stringify(dl));

  await page.close();
}

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
  });
  await test332(browser);
  await test324(browser);
} catch (e) {
  fail++;
  console.log('  ❌ 真机脚本执行异常: ' + (e && e.stack || e));
} finally {
  if (browser) await browser.close();
}

console.log('\n==== 910 真机异步乱序证据 通过 ' + pass + ' / 失败 ' + fail + ' ====');
process.exit(fail ? 1 : 0);
