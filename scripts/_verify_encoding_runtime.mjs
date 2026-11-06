#!/usr/bin/env node
/**
 * 编码类工具（tools/it/base64-converter.html）的运行期回归验证。
 *
 * 为什么不用 verify_it_calc.js：该页的编解码函数都包在页内 IIFE 里，harness 的 __pageEval
 * 取不到（实测 `typeof base32Decode === 'undefined'`），jsdom 也不会把它们挂到 window。
 * 因此这里从源文件按行抽取真实函数体，在 Node 里以 __b64L 桩执行——与门禁判定同一份源码。
 *
 * 覆盖 IT-N83 复核失败点：Base32 尾部等号数量必须符合 RFC 4648 §6（按末组补足到 8 的倍数），
 * 原实现 `replace(/=+$/,'')` 无条件剥掉全部等号，MY= / MY===== / MY========= 三种输入都解出同一个字节。
 *
 * 用法：node scripts/_verify_encoding_runtime.mjs
 * 退出码：0 全通过；1 有失败项。
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import vm from "node:vm";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PAGE = resolve(ROOT, "tools/it/base64-converter.html");

const lines = readFileSync(PAGE, "utf8").split("\n");
// 369 行起是 BASE32_CHARS/BASE85_CHARS 与四个编解码函数，到 base85Decode 的闭合大括号为止
const startIdx = lines.findIndex((l) => l.includes("var BASE32_CHARS"));
const endIdx = lines.findIndex((l, i) => i > startIdx && l === "  function encode(str, urlSafe){");
if (startIdx < 0 || endIdx < 0) throw new Error("页面结构变化，抽取区间失效，请更新本脚本的行锚点");

const src =
  "function __b64L(en, zh){ return zh; }\n" +
  lines.slice(startIdx, endIdx).join("\n") +
  "\n;globalThis.__api = { base32Decode, base32Encode, base85Decode, base85Encode, base64Encode, base64Decode };";

const ctx = { console };
vm.createContext(ctx);
vm.runInContext(src, ctx);
const api = ctx.__api;

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  —  " + detail : ""}`);
}
function bytes(fn, arg) {
  return Array.from(fn(arg));
}
function throws(fn, arg) {
  try {
    fn(arg);
    return null;
  } catch (e) {
    return e.message;
  }
}

// ---------------------------------------------------------------- 合法路径不回归
check("base32Decode('MY======') 解出 'f'", JSON.stringify(bytes(api.base32Decode, "MY======")) === "[102]");
check("base32Decode('MZXW6YTBOI') 无填充同样可解（foobar）", Buffer.from(bytes(api.base32Decode, "MZXW6YTBOI")).toString() === "foobar");
const rt = api.base32Encode(Uint8Array.from(Buffer.from("hello world")));
check(
  "base32 编码→解码往返",
  Buffer.from(bytes(api.base32Decode, String(rt))).toString() === "hello world",
  `encode=${rt}`
);

// ---------------------------------------------------------------- N83 填充校验
const badShort = throws(api.base32Decode, "MY=");
check(
  "N83 base32Decode('MY=') 报填充数量无效（不足 6 个）",
  !!badShort && /填充数量无效（应为 6 个等号）/.test(badShort),
  badShort || "未抛错（仍静默解出 f）"
);
const badLong = throws(api.base32Decode, "MY=========");
check(
  "N83 base32Decode('MY=========') 报填充无效（超过 6 个）",
  !!badLong && /填充无效（最多 6 个等号）/.test(badLong),
  badLong || "未抛错（仍静默解出 f）"
);
const badMid = throws(api.base32Decode, "MY=A====");
check(
  "N83 等号出现在中间时报错",
  !!badMid && /等号只能出现在末尾/.test(badMid),
  badMid || "未抛错"
);
const badChar = throws(api.base32Decode, "MZXW6YTB0I");
check(
  "N83 表外字符仍报错并给位次（第 9 位「0」）",
  !!badChar && /第 9 位含非法字符「0」/.test(badChar),
  badChar || "未抛错"
);

// ---------------------------------------------------------------- Base85 冒烟（防本次改动波及）
check(
  "base85 解码 <~BOu!rDZ~> = 'hello'（Ascii85 标准样例）",
  Buffer.from(bytes(api.base85Decode, "<~BOu!rDZ~>")).toString() === "hello"
);
const b85enc = api.base85Encode(Uint8Array.from(Buffer.from("easy")));
check(
  "base85 编码→解码往返",
  Buffer.from(bytes(api.base85Decode, String(b85enc))).toString() === "easy",
  `encode=${b85enc}`
);

const failed = results.filter((r) => !r.ok);
console.log(`\n==== ${results.length - failed.length}/${results.length} 通过 ====`);
if (failed.length) {
  for (const f of failed) console.log(`  FAIL ${f.name}`);
  process.exit(1);
}
process.exit(0);
