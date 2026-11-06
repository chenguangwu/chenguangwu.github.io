#!/usr/bin/env node
/**
 * IT-N539 ～ N544 速查表「复制即执行」专项回归。
 *
 * 为什么不用 verify_it_calc.js：速查表的 example 是页内命令数据表，门禁用例只校验
 * 搜索计数（反向锚），无法断言某条示例是否含非法注释 / 是否是可编译可执行的片段。
 * 这里直接解析三页真实的命令表字段，与线上同一份源码。
 *
 * 用法：node scripts/_verify_cheatsheet_syntax.mjs
 *      CHEAT_SRC=/tmp/head_cheat node scripts/_verify_cheatsheet_syntax.mjs  # 回退源码判别力实测
 * 退出码：0 全通过；1 有失败项。
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok });
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  —  " + detail : ""}`);
}

function fields(slug) {
  const srcDir = process.env.CHEAT_SRC ? resolve(process.env.CHEAT_SRC) : resolve(ROOT, "tools/it");
  const html = readFileSync(resolve(srcDir, `${slug}.html`), "utf8");
  const out = [];
  const re = /"(example|syntax|params)"\s*:\s*"((?:[^"\\]|\\.)*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    try { out.push([m[1], JSON.parse('"' + m[2] + '"')]); } catch (e) { /* 跳过异常转义 */ }
  }
  return { html, out };
}
function allText(f) { return f.out.map((x) => x[1]).join("\n"); }

// ---- python-cheatsheet（N539 / N540）----
{
  const f = fields("python-cheatsheet");
  const t = allText(f);
  check("N539 python 无 `--` 行内注释，全部改为 `#`", !t.includes("  -- ") && t.includes("  # "), `-- 计数 ${(t.match(/  -- /g) || []).length}`);
  check("N539 裸 raise 补了 except 上下文", t.includes("except ValueError:") && t.includes("    raise  # 重抛"));
  check("N540 dataclass 装饰器独立成行", f.out.some((x) => x[0] === "syntax" && x[1] === "@dataclass\nclass C:"));
  check("N540 相对导入改为独立脚本可用的绝对导入", t.includes("import helper") && !t.includes("from . import helper"));
}
// ---- rust-cheatsheet（N541 / N542）----
{
  const f = fields("rust-cheatsheet");
  const t = allText(f);
  check("N541 rust 无 `--` 行内注释，全部改为 `//`", !t.includes("  -- ") && t.includes("  // "), `-- 计数 ${(t.match(/  -- /g) || []).length}`);
  const rustExamples = f.out.filter((x) => x[0] === "example").map((x) => x[1]).join("\n");
  check("N542 示例表达式位置无 `...` 占位", !rustExamples.includes("{ ... }") && rustExamples.includes("while cond { break; }"));
  check("N542 顶层 `?` 包进返回 Result 的函数且不再引用未定义 r", t.includes("fn demo() -> Result<(), ParseIntError>") && t.includes('parse("x").unwrap_or(0)') && !t.includes("let v = r.unwrap_or(0);"));
}
// ---- redis-cheatsheet（N543 / N544）----
{
  const f = fields("redis-cheatsheet");
  const t = allText(f);
  check("N543 redis-cli 无行内注释（注解整体移除）", !t.includes("  -- "), `-- 计数 ${(t.match(/  -- /g) || []).length}`);
  check("N543 PING 示例只剩纯命令", t.includes("PING\nPING hello"));
  check("N544 SINTER/SUNION/SDIFF 不再承诺 STORE，改用 *STORE 命令", f.out.some((x) => x[0] === "params" && x[1].includes("SINTERSTORE / SUNIONSTORE / SDIFFSTORE")) && t.includes("SINTERSTORE out set1 set2"));
}

const pass = results.filter((r) => r.ok).length;
console.log(`\n==== ${pass}/${results.length} 通过 ====`);
process.exit(pass === results.length ? 0 : 1);
