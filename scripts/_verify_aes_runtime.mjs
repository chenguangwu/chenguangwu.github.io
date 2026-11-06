#!/usr/bin/env node
/**
 * AES 加解密器的运行期回归验证（jsdom 真机执行页面脚本，非桩 DOM）。
 *
 * 为什么不用 verify_it_calc.js：该 harness 是自研桩 DOM，存在两处硬限制——
 *   1) 点击表达式不 await 返回值 ⇒ async 的 encrypt()/decrypt() 结果采集不到；
 *   2) 桩 DOM 不支持 querySelectorAll('input[id],select[id],textarea[id]') ⇒ __aes_encryptorSnap() 恒返回 {}。
 * 因此本脚本用 jsdom + Node webcrypto 直接跑页面真实函数，覆盖以下四项复核失败点：
 *
 *   N87  ECB/CBC 解密前必须校验密文长度为 16 字节整数倍
 *   N88  ECB 元数据（salt:cipher）在盐框有值时仍须剥离；盐字段须同时接受 hex 与 Base64
 *   N90  历史快照（history / CSV 导出数据源）不得含口令明文
 *   N92  加密信息栏的「输入」字节数取填充前长度
 *
 * 用法：node scripts/_verify_aes_runtime.mjs [--verbose]
 * 退出码：0 全通过；1 有失败项。
 */
import { JSDOM, VirtualConsole } from "jsdom";
import { webcrypto } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PAGE = resolve(ROOT, "tools/it/aes-encryptor.html");
const VERBOSE = process.argv.includes("--verbose");

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  —  " + detail : ""}`);
}

const html = readFileSync(PAGE, "utf8");
const toasts = [];
const vc = new VirtualConsole();
vc.on("jsdomError", (e) => {
  if (VERBOSE) console.log("[jsdomError]", e.message);
});

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  url: "https://example.com/aes-encryptor.html",
  pretendToBeVisual: true,
  virtualConsole: vc,
  beforeParse(w) {
    w.ToolBox = { showToast: (m, t) => toasts.push(`${t || ""}|${m}`) };
    w.i18nText = (k) => `MSG:${k}`;
    try {
      Object.defineProperty(w, "crypto", { value: webcrypto, configurable: true, writable: true });
    } catch {
      w.crypto.subtle = webcrypto.subtle;
    }
  },
});

const w = dom.window;
const g = (id) => w.document.getElementById(id);
const set = (id, v) => {
  const e = g(id);
  if (!e) throw new Error(`页面上找不到 #${id}`);
  if (e.type === "checkbox") e.checked = !!v;
  else e.value = String(v);
};

// ---------------------------------------------------------------- N92
set("mode", "ECB");
set("keySize", "128");
set("keyType", "password");
set("password", "pw");
set("useSalt", true);
set("pkcs7Padding", true);
set("outputFormat", "hex");
set("includeMeta", false);
set("salt", "00112233445566778899aabbccddeeff");
set("input", "中文");
await w.encrypt();
const cipherHex = g("output").value;
check(
  "N92 加密输入字节数取填充前长度（中文 6 B，而非填充后 16 B）",
  g("infoInputLen").textContent === "6 B" && cipherHex.length === 32,
  `infoInputLen=${g("infoInputLen").textContent} / infoOutputLen=${g("infoOutputLen").textContent} / cipher=${cipherHex.length} hex`
);

// ---------------------------------------------------------------- N88 (ECB + 盐框有值)
set("includeMeta", true);
set("input", "中文");
await w.encrypt();
const metaHex = g("output").value;
const saltKept = g("salt").value;
set("input", metaHex);
await w.decrypt();
check(
  "N88 ECB 元数据 salt:cipher 在盐框已有值时仍正确剥离（同页往返）",
  g("output").value === "中文" && metaHex.split(":").length === 2,
  `meta=${metaHex} salt=${saltKept} → 解出 ${JSON.stringify(g("output").value)}`
);

// ---------------------------------------------------------------- N88 (Base64 盐)
set("outputFormat", "base64");
set("input", "hello");
await w.encrypt();
const metaB64 = g("output").value;
set("input", metaB64);
await w.decrypt();
check(
  "N88 Base64 输出时盐以 Base64 标记，解密侧按同一编码还原（往返）",
  g("output").value === "hello",
  `解出 ${JSON.stringify(g("output").value)}`
);

// ---------------------------------------------------------------- N88 (CBC 三段元数据)
set("mode", "CBC");
set("outputFormat", "hex");
set("input", "CBC往返测试");
await w.encrypt();
const metaCbc = g("output").value;
set("input", metaCbc);
await w.decrypt();
check(
  "N88 CBC 元数据 salt:iv:cipher 三段式在盐框有值时正确剥离",
  g("output").value === "CBC往返测试" && metaCbc.split(":").length === 3,
  `段数=${metaCbc.split(":").length} → 解出 ${JSON.stringify(g("output").value)}`
);

// ---------------------------------------------------------------- N87
toasts.length = 0;
set("mode", "ECB");
set("pkcs7Padding", false);
set("outputFormat", "hex");
set("input", "abcdef1234"); // 5 字节，非 16 整数倍
const outBefore = g("output").value;
await w.decrypt();
const rejected = toasts.some((t) => /密文长度无效|Invalid ciphertext/.test(t) && t.startsWith("error|"));
check(
  "N87 ECB 解密拒绝非 16 字节整数倍密文且不改写结果区",
  rejected && g("output").value === outBefore,
  `toast=${JSON.stringify(toasts)}`
);

// ---------------------------------------------------------------- N87 反向（合法密文不得被误拒）
toasts.length = 0;
set("pkcs7Padding", true);
set("input", "0123456789abcdef");
await w.encrypt();
const okCipher = g("output").value;
set("input", okCipher);
await w.decrypt();
check(
  "N87 反向：合法 16 字节密文仍可正常解出（未过度拦截）",
  g("output").value === "0123456789abcdef",
  `解出 ${JSON.stringify(g("output").value)}`
);

// ---------------------------------------------------------------- N90
set("password", "SUPERSECRETPW");
set("input", "x");
await w.encrypt();
const snap = w.__aes_encryptorSnap();
check(
  "N90 历史快照对口令打码，不含明文",
  snap.password === "••••" && !JSON.stringify(snap).includes("SUPERSECRETPW"),
  `snapshot.password=${JSON.stringify(snap.password)}`
);

// ---------------------------------------------------------------- 汇总
const failed = results.filter((r) => !r.ok);
console.log(`\n==== ${results.length - failed.length}/${results.length} 通过 ====`);
if (failed.length) {
  for (const f of failed) console.log(`  FAIL ${f.name}`);
  process.exit(1);
}
process.exit(0);
