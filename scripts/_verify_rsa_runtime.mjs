#!/usr/bin/env node
/**
 * RSA 加签/验签/加解密的运行期回归验证（jsdom 真机执行页面脚本）。
 *
 * verify_it_calc.js 无法覆盖：该 harness 不 await 点击返回的 Promise，而 doSign/doVerify/doEncrypt
 * 都是 async 且依赖 crypto.subtle（桩环境没有），因此这里用 jsdom + Node webcrypto 跑真实函数。
 *
 * 覆盖 IT-N96 复核失败点：
 *   1) doSign / doVerify / doEncrypt / doDecrypt 成功后必须写入历史（原来只有 downloadKeys 的包装会记录）
 *   2) 历史条目（= CSV 导出数据源）不得包含任何 PEM 密钥明文
 *   3) 趋势图数据源改为输出字节数，不再对签名/密文 parseFloat
 *
 * 用法：node scripts/_verify_rsa_runtime.mjs [--verbose]
 * 退出码：0 全通过；1 有失败项。
 */
import { JSDOM, VirtualConsole } from "jsdom";
import { webcrypto } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PAGE = resolve(ROOT, "tools/it/rsa.html");
const VERBOSE = process.argv.includes("--verbose");

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  —  " + detail : ""}`);
}

const recs = []; // 与 js/tool-kit.js 一致：条目形如 { t, d }，新记录 unshift 到最前
const charts = [];
const tables = [];
const exports = [];
const toasts = [];
const vc = new VirtualConsole();
vc.on("jsdomError", (e) => {
  if (VERBOSE) console.log("[jsdomError]", e.message);
});

const dom = new JSDOM(readFileSync(PAGE, "utf8"), {
  runScripts: "dangerously",
  url: "https://example.com/rsa.html",
  pretendToBeVisual: true,
  virtualConsole: vc,
  beforeParse(w) {
    w.TextEncoder = TextEncoder;
    w.TextDecoder = TextDecoder;
    const subtle = new Proxy(webcrypto.subtle, {
      get(target, name) {
        const fn = target[name];
        if (typeof fn !== "function") return fn;
        return (...args) => {
          const positions = { importKey: [1], encrypt: [2], decrypt: [2], sign: [2], verify: [2, 3] }[name] || [];
          for (const i of positions) {
            if (args[i] instanceof w.ArrayBuffer) args[i] = Buffer.from(new w.Uint8Array(args[i]));
          }
          return fn.apply(target, args);
        };
      },
    });
    Object.defineProperty(w, "crypto", { value: { subtle, getRandomValues: webcrypto.getRandomValues.bind(webcrypto) }, configurable: true });
    w.i18nText = (k) => `MSG:${k}`;
    w.ToolBox = { showToast: (m, t) => toasts.push(`${t || ""}|${m}`), copyText: () => {} };
    w.TBKit = {
      util: { isEn: () => false, diffBox: () => {}, exportTable: (...args) => exports.push(args) },
      matrix: { table: (_sel, data) => tables.push(data) },
      chart: { line: (_sel, cfg) => charts.push(cfg) },
      preset: { bar: () => {} },
      history: {
        list: () => recs.map((x) => x),
        last: () => (recs.length ? recs[0].d : null),
        record: (r) => {
          recs.unshift({ t: Date.now(), d: r });
        },
        mount: () => {},
      },
    };
  },
});

const w = dom.window;
const g = (id) => w.document.getElementById(id);

await w.generateKeys();
check("前置：生成密钥对", recs.length === 0 && /密钥对生成成功/.test(toasts.slice(-1)[0] || ""));

// ---------------------------------------------------------------- 签名入历史
g("tab-sign").classList.add("active");
g("signInput").value = "hello-sign";
await w.doSign();
const signRec = recs[0] ? recs[0].d : null;
check(
  "N96 签名成功后写入历史，结果列含签名内容",
  recs.length === 1 && signRec && /签名已生成/.test(String(signRec["结果"] || "")),
  `记录数=${recs.length} toast=${JSON.stringify(toasts.slice(-1))}`
);
check(
  "N96 历史条目不含 PEM 密钥明文",
  !!signRec && !/BEGIN (RSA )?(PRIVATE|PUBLIC) KEY/.test(JSON.stringify(signRec)),
  signRec ? `字段=${Object.keys(signRec).join(",")}` : "无记录"
);
check(
  "N96 签名记录的 __bytes 为签名字节数（2048 位 ⇒ 256 B）",
  !!signRec && signRec["__bytes"] === 256,
  signRec ? `__bytes=${signRec["__bytes"]}` : "无记录"
);

// ---------------------------------------------------------------- 验签入历史
g("signInput").value = "hello-sign";
await w.doVerify();
const verifyRec = recs[0]?.d;
check(
  "N96 验签完成后写入历史，结果列为验签结论",
  recs.length === 2 && /签名验证(通过|失败)/.test(String(verifyRec?.["结果"] || "")),
  `记录数=${recs.length} 结果=${JSON.stringify(String(verifyRec?.["结果"] || "").slice(0, 24))}`
);

// ---------------------------------------------------------------- 加密入历史
g("encInput").value = "hello-enc";
await w.doEncrypt();
check("N96 加密成功后写入历史", recs.length === 3 && recs[0]?.d?.["__bytes"] === 256, `记录数=${recs.length}`);

// ---------------------------------------------------------------- 趋势图口径
const lastChart = charts[charts.length - 1];
check(
  "N96 趋势图数据源为输出字节数（数值），不再对签名 parseFloat",
  !!lastChart && Array.isArray(lastChart.series[0].data) && lastChart.series[0].data.every((v) => typeof v === "number" && v > 0),
  lastChart ? `series=${JSON.stringify(lastChart.series[0])}` : "未绘制"
);

// 连续真实加解密：明文中的失败词不代表解密失败。
g("tab-sign").classList.remove("active");
g("encInput").value = "FAILED";
await w.doEncrypt();
g("encInput").value = g("encResult").textContent;
await w.doDecrypt();
check("二次复核 RSA 解密明文 FAILED 记录通过", g("encResult").textContent === "FAILED" && recs[0]?.d?.__tbScore === 1, `结果=${g("encResult").textContent} score=${recs[0]?.d?.__tbScore}`);
w.__rsaExport();
check("二次复核 RSA 导出表包含正确结论", tables.at(-1)?.rows[0]?.includes("通过") && tables.at(-1)?.rows[0]?.includes("FAILED") && exports.at(-1)?.[0] === "#rsaTable");
g("encInput").value = "请输入文本";
await w.doEncrypt();
g("encInput").value = g("encResult").textContent;
await w.doDecrypt();
check("二次复核 RSA 提示词明文仍入历史", recs[0]?.d?.["结果"] === "请输入文本" && recs[0]?.d?.__tbScore === 1);
g("tab-sign").classList.add("active");
g("signInput").value = "tampered";
await w.doVerify();
check("二次复核 RSA 验签失败仍记录未通过", recs[0]?.d?.__tbScore === 0, `score=${recs[0]?.d?.__tbScore}`);

// ---------------------------------------------------------------- 汇总
const failed = results.filter((r) => !r.ok);
console.log(`\n==== ${results.length - failed.length}/${results.length} 通过 ====`);
if (failed.length) {
  for (const f of failed) console.log(`  FAIL ${f.name}`);
  process.exit(1);
}
process.exit(0);
