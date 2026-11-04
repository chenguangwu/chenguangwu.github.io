#!/usr/bin/env node
/**
 * 共享层保真门禁（TB_STUB_FIDELITY=1）
 *
 * 背景：所有 calc verify 门禁默认用「简化桩」跑页面脚本，**不加载 js/common.js**。
 * 于是「页面顶层同名函数被 common.js 的全局赋值覆盖」这类生产独有故障，在桩里根本不会发生
 * —— 出现「桩里全绿、线上输出错」（已验证实例：science-pressure-converter 的 fmtNum、
 * color-picker/fancy-text/rich-text-editor/random-string 的 copyText）。
 *
 * 本脚本把同一批用例改在保真模式下重跑：harness 按线上顺序在页面内联脚本之后注入**真实的
 * js/common.js**，并把页面顶层同名绑定重指到全局实现（等价于浏览器的 defer 覆盖）。
 *
 * 用法：
 *   node scripts/verify_stub_fidelity.js              # 门禁：保真不得比默认多红（差异必须为空）
 *   node scripts/verify_stub_fidelity.js --report     # 同上，并打印默认/保真/差异三组明细
 *   node scripts/verify_stub_fidelity.js --strict     # 严格：保真模式必须全绿（不含默认基线豁免）
 *   node scripts/verify_stub_fidelity.js --only=science,it,design
 *   node scripts/verify_stub_fidelity.js --concurrency=8
 *
 * 判定口径（这是本门禁的核心）：
 *   · 默认门禁证明「逻辑对不对」；本门禁证明「线上是不是这样执行」。
 *   · 门禁模式（默认）判 **差异**：某用例在默认模式绿、在保真模式红 ⇒ 就是「桩骗了我们」，
 *     必须红。两模式都红的既有失败不归本门禁管（由各自的默认门禁/责任线收口），
 *     否则本门禁会被历史债务拖成永久红、失去信号。
 *   · --strict 额外要求保真全绿；用于债务清零后的收紧（CI 可先保持门禁模式）。
 *
 * 退出码：
 *   0  无差异（或 --strict 下全绿）/ 无可跑用例（SKIP 也返回 0，CI 友好）
 *   1  存在「保真红而默认绿」的用例（--strict 下：存在任何保真失败）
 *
 * 说明：本脚本不需要浏览器，只依赖 Node（与各 verify_*_calc.js 相同）。
 *       若发现任何 verify_*_calc.js 缺失或不可执行，该项标 SKIP 并继续。
 */
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const ROOT = path.join(__dirname, "..");
const SCRIPTS = path.join(ROOT, "scripts");
const SUITE_RE = /^verify_([a-z0-9][a-z0-9-]*)_calc\.js$/;
const SUITE_TIMEOUT_MS = 15 * 60 * 1000;

function listSuites(only) {
  const files = fs.readdirSync(SCRIPTS)
    .filter((f) => SUITE_RE.test(f))
    .sort();
  if (!only || !only.length) return files;
  return files.filter((f) => only.includes(f.match(SUITE_RE)[1]));
}

function parseSummary(out) {
  const hits = [...out.matchAll(/====\s*[^\n]*?(\d+)\/(\d+)[^\n]*/g)];
  if (!hits.length) return null;
  const last = hits[hits.length - 1];
  return { pass: Number(last[1]), total: Number(last[2]) };
}

function parseFailedSlugs(out) {
  const set = new Set();
  for (const line of out.split("\n")) {
    const m = line.match(/^❌\s+(\S+)/);
    if (m && m[1].includes("/")) set.add(m[1]);
  }
  return [...set];
}

function runSuite(file, fidelity) {
  return new Promise((resolve) => {
    const env = Object.assign({}, process.env);
    if (fidelity) env.TB_STUB_FIDELITY = "1";
    else delete env.TB_STUB_FIDELITY;
    const child = spawn(process.execPath, [path.join(SCRIPTS, file)], {
      cwd: ROOT,
      env,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let out = "", errOut = "", timedOut = false;
    const timer = setTimeout(() => { timedOut = true; child.kill("SIGKILL"); }, SUITE_TIMEOUT_MS);
    child.stdout.on("data", (d) => { out += d; });
    child.stderr.on("data", (d) => { errOut += d; });
    child.on("error", (e) => {
      clearTimeout(timer);
      resolve({ file, skipped: true, reason: "spawn 失败: " + e.message });
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      const sum = parseSummary(out + errOut);
      if (timedOut) return resolve({ file, skipped: false, error: "超时（>15min）" });
      if (!sum) {
        return resolve({ file, skipped: true, reason: "未识别到汇总行（exit " + code + "）" });
      }
      resolve({
        file,
        pass: sum.pass,
        total: sum.total,
        failed: parseFailedSlugs(out + errOut),
      });
    });
  });
}

async function runAll(suites, fidelity, concurrency) {
  const results = [];
  let idx = 0;
  const workers = Array.from({ length: Math.min(concurrency, suites.length) }, async () => {
    while (idx < suites.length) {
      const my = idx++;
      results[my] = await runSuite(suites[my], fidelity);
    }
  });
  await Promise.all(workers);
  return results;
}

function label(file) {
  return file.match(SUITE_RE)[1];
}

async function main() {
  const argv = process.argv.slice(2);
  const report = argv.includes("--report");
  const strict = argv.includes("--strict");
  // 兼容两种写法：`--only=cat1,cat2`（本脚本默认）与 `--only cat1,cat2`（沿用旧版调用习惯）。
  const onlyEq = argv.find((a) => a.startsWith("--only="));
  const onlySp = argv.indexOf("--only");
  const onlyArg = onlyEq ? onlyEq.slice("--only=".length) : (onlySp >= 0 ? argv[onlySp + 1] || "" : "");
  const only = onlyArg ? onlyArg.split(",").filter(Boolean) : null;
  const concEq = argv.find((a) => a.startsWith("--concurrency="));
  const concSp = argv.indexOf("--concurrency");
  const concVal = concEq ? concEq.split("=")[1] : (concSp >= 0 ? argv[concSp + 1] : null);
  const concurrency = concVal ? Math.max(1, Number(concVal) || 4) : 4;

  const suites = listSuites(only).filter((f) => fs.existsSync(path.join(SCRIPTS, f)));
  if (!suites.length) {
    console.log("SKIP: 未发现可运行的 verify_*_calc.js");
    process.exit(0);
  }

  const fid = await runAll(suites, true, concurrency);
  const def = strict ? null : await runAll(suites, false, concurrency);

  const skipped = fid.filter((r) => r.skipped);
  const ran = fid.filter((r) => !r.skipped);
  const failed = ran.filter((r) => r.error || r.pass !== r.total);

  const sumOf = (list) => list.reduce(
    (a, r) => ({ pass: a.pass + (r.pass || 0), total: a.total + (r.total || 0) }),
    { pass: 0, total: 0 }
  );
  const fSum = sumOf(ran);
  const dRan = def ? def.filter((r) => !r.skipped) : [];
  const dSum = sumOf(dRan);

  // 差异计算（用例级）：保真红而默认绿 = 桩骗了我们；保真绿而默认红 = 默认桩的漏检/已修复。
  const diffs = [];
  if (def) {
    const byLabel = new Map(def.map((r) => [label(r.file), r]));
    for (const r of ran) {
      const d = byLabel.get(label(r.file));
      if (!d || d.skipped) continue;
      const fBad = new Set(r.failed || []);
      const dBad = new Set(d.failed || []);
      const newly = [...fBad].filter((s) => !dBad.has(s));
      const fixed = [...dBad].filter((s) => !fBad.has(s));
      if (newly.length || fixed.length) diffs.push({ cat: label(r.file), newly, fixed });
    }
  }

  console.log("\n=== 保真模式（TB_STUB_FIDELITY=1，注入真实 js/common.js）===");
  for (const r of ran) {
    if (r.error || r.pass !== r.total) {
      console.log(`  ❌ ${label(r.file)}  ${r.error || r.pass + "/" + r.total}` + (r.failed.length ? "  → " + r.failed.join(", ") : ""));
    }
  }
  for (const r of skipped) console.log(`  SKIP ${label(r.file)}  ${r.reason}`);
  console.log(`  汇总：${ran.length - failed.length}/${ran.length} 分类全绿，用例 ${fSum.pass}/${fSum.total}`);

  if (def) {
    console.log("\n=== 默认模式（简化桩，不加载 common.js）===");
    for (const r of dRan) {
      if (r.error || r.pass !== r.total) {
        console.log(`  ❌ ${label(r.file)}  ${r.error || r.pass + "/" + r.total}` + (r.failed.length ? "  → " + r.failed.join(", ") : ""));
      }
    }
    console.log(`  汇总：${dRan.length - dRan.filter((r) => r.error || r.pass !== r.total).length}/${dRan.length} 分类全绿，用例 ${dSum.pass}/${dSum.total}`);
  }

  if (def) {
    console.log("\n=== 默认 vs 保真 差异页（桩骗过我们的完整清单）===");
    if (!diffs.length) console.log("  （无差异）");
    for (const d of diffs) {
      if (d.newly.length) console.log(`  ${d.cat}: 保真红而默认绿 → ${d.newly.join(", ")}`);
      if (d.fixed.length) console.log(`  ${d.cat}: 保真绿而默认红 → ${d.fixed.join(", ")}`);
    }
  }

  const diffNewly = diffs.reduce((a, d) => a + d.newly.length, 0);
  if (strict) {
    if (failed.length) {
      console.log("\n结论：FAIL（--strict：保真模式存在失败用例）");
      process.exit(1);
    }
    console.log("\n结论：PASS（--strict：保真模式全绿）");
    process.exit(0);
  }
  if (diffNewly) {
    console.log(`\n结论：FAIL（${diffNewly} 条用例「默认绿、保真红」——桩掩盖了生产缺陷）`);
    process.exit(1);
  }
  console.log("\n结论：PASS（无「默认绿、保真红」用例；两模式同红项由既有门禁收口）");
  process.exit(0);
}

main().catch((e) => {
  console.error("SKIP: 脚本异常 " + (e && e.message));
  process.exit(0);
});
