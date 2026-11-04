#!/usr/bin/env node
/**
 * it 分类安全回归自检（静态 + 内联脚本语法）
 *
 * 覆盖三类近期线上问题：
 *   1. regex.html 的 Web Worker 源码不得再用字符串拼装，静态 worker 脚本必须能通过 node --check；
 *   2. rich-text-editor.html 的富文本导入 / 源码应用 / 粘贴必须走 sanitizeHtml 白名单；
 *   3. code-runner.html 的预览 iframe 沙箱不得同时开启 allow-scripts 与 allow-same-origin。
 * 另对全站所有含动态执行（new Worker / new Function / Blob 脚本 / eval）的页面做内联脚本语法检查，
 * 防止再次出现拼接残留分号导致的 `Unexpected token ';'`。
 *
 * 用法：node scripts/verify_it_security.js
 */
const fs = require("fs");
const path = require("path");
const os = require("os");
const { execFileSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const failures = [];
function fail(msg) { failures.push(msg); }
function read(rel) { return fs.readFileSync(path.join(ROOT, rel), "utf8"); }

function checkNodeSyntax(code, label) {
  const tmp = path.join(os.tmpdir(), "tb_sec_" + Math.random().toString(36).slice(2) + ".js");
  fs.writeFileSync(tmp, code, "utf8");
  try {
    execFileSync(process.execPath, ["--check", tmp], { stdio: "pipe" });
  } catch (e) {
    fail(label + " 内联脚本语法错误: " + String(e.stderr || e.message).split("\n")[0]);
  } finally {
    try { fs.unlinkSync(tmp); } catch {}
  }
}

// 抽取页面内联脚本（排除 JSON-LD；text/js-worker 也按 JS 校验）
function inlineScripts(html) {
  const out = [];
  const re = /<script([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    const attrs = m[1] || "";
    if (/application\/ld\+json/i.test(attrs)) continue;
    if (m[2].trim()) out.push({ attrs, code: m[2] });
  }
  return out;
}

// 1. regex.html
(function () {
  const html = read("tools/it/regex.html");
  if (/RX_WORKER_SRC|['"]self\.onmessage/.test(html)) {
    fail("regex.html 仍在用字符串拼装 Worker 源码");
  }
  const worker = html.match(/<script[^>]*type="text\/js-worker"[^>]*id="rx-worker-src"[^>]*>([\s\S]*?)<\/script>/i);
  if (!worker) fail("regex.html 缺少静态 <script type=\"text/js-worker\" id=\"rx-worker-src\">");
  else checkNodeSyntax(worker[1], "regex.html worker");
  if (!/worker\.terminate\(\)/.test(html)) fail("regex.html 超时路径缺少 worker.terminate()");
  if (!/worker\.onerror/.test(html)) fail("regex.html 缺少 Worker onerror 兜底提示");
})();

// 2. rich-text-editor.html
(function () {
  const html = read("tools/it/rich-text-editor.html");
  if (!/function sanitizeHtml\(/.test(html)) fail("rich-text-editor.html 缺少 sanitizeHtml 白名单净化");
  if (!/editorEl\(\)\.innerHTML\s*=\s*sanitizeHtml\(v\)/.test(html)) fail("rich-text-editor.html applySource 未净化");
  if (!/editorEl\(\)\.innerHTML\s*=\s*sanitizeHtml\(String\(fr\.result/.test(html)) fail("rich-text-editor.html 文件导入未净化");
  if (!/addEventListener\('paste'/.test(html)) fail("rich-text-editor.html 缺少粘贴净化");
  if (/showResult\('<p>✅ 已导入 <strong>' \+ f\.name/.test(html)) fail("rich-text-editor.html 文件名未转义");
})();

// 3. code-runner.html
(function () {
  const html = read("tools/it/code-runner.html");
  const frame = html.match(/<iframe[^>]*id="preview"[^>]*>/i);
  if (!frame) fail("code-runner.html 缺少预览 iframe");
  else if (/allow-same-origin/i.test(frame[0])) fail("code-runner.html 预览 iframe 仍开启 allow-same-origin");
  if (!/iframe\.srcdoc\s*=/.test(html)) fail("code-runner.html 未改用 srcdoc 注入预览");
  if (/iframe\.contentDocument|iframe\.contentWindow\.document/.test(html)) fail("code-runner.html 仍访问 contentDocument");
})();

// 4. 全站动态执行页面语法扫描
(function () {
  const toolsDir = path.join(ROOT, "tools");
  const hits = [];
  (function walk(dir) {
    for (const name of fs.readdirSync(dir)) {
      const p = path.join(dir, name);
      const st = fs.statSync(p);
      if (st.isDirectory()) walk(p);
      else if (name.endsWith(".html")) {
        const c = fs.readFileSync(p, "utf8");
        if (/new Worker\(|URL\.createObjectURL\(new Blob\(|new Function\(|(^|[^A-Za-z_$.])eval\(/.test(c)) {
          hits.push({ rel: path.relative(ROOT, p), code: c });
        }
      }
    }
  })(toolsDir);
  for (const h of hits) {
    for (const s of inlineScripts(h.code)) checkNodeSyntax(s.code, h.rel);
  }
  if (hits.length === 0) {
    // 判绿前提：扫描必须真的有命中。命中 0 页多半是正则失效 / 目录不对 / 扫描被跳过，
    // 此时「0 条语法错误」是空集假绿，必须判红。
    fail("动态执行页面扫描命中 0 页（正则失效或 tools 目录异常，拒绝判绿）");
  } else {
    console.log("动态执行页面扫描: " + hits.length + " 页");
  }
})();

if (failures.length) {
  console.error("❌ it 安全自检失败:");
  failures.forEach((f) => console.error(" - " + f));
  process.exit(1);
}
console.log("✅ it 安全自检通过");
