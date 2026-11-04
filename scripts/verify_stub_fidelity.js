#!/usr/bin/env node
/**
 * 共享层保真模式门禁（TB_STUB_FIDELITY=1）
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
 *   node scripts/verify_stub_fidelity.js                 # 门禁：只跑保真模式，全绿 exit 0
 *   node scripts/verify_stub_fidelity.js --report        # 报告：默认 vs 保真 双跑 + 差异页清单
 *   node scripts/verify_stub_fidelity.js --only science,it,design,image
 *   node scripts/verify_stub_fidelity.js --concurrency 4
 *
 * 退出码：
 *   0  全部通过 / 无可跑用例（SKIP 也返回 0，CI 友好）
 *   1  存在保真模式下失败的用例
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
  const onlyArg = argv.find((a) => a.startsWith("--only=")) || "";
  const only = onlyArg ? onlyArg.slice("--only=".length).split(",").filter(Boolean) : null;
  const concArg = argv.find((a) => a.startsWith("--concurrency="));
  const concurrency = concArg ? Math.max(1, Number(concArg.split("=")[1]) || 4) : 4;

  const suites = listSuites(only).filter((f) => fs.existsSync(path.join(SCRIPTS, f)));
  if (!suites.length) {
    console.log("SKIP: 未发现可运行的 verify_*_calc.js");
    process.exit(0);
  }

  const fid = await runAll(suites, true, concurrency);
  let def = null;
  if (report) def = await runAll(suites, false, concurrency);

  const skipped = fid.filter((r) => r.skipped);
  const ran = fid.filter((r) => !r.skipped);
  const failed = ran.filter((r) => r.error || r.pass !== r.total);

  const sumOf = (list) => list.reduce(
    (a, r) => ({ pass: a.pass + (r.pass || 0), total: a.total + (r.total || 0) }),
    { pass: 0, total: 0 }
  );
  const fSum = sumOf(ran);

  console.log("\n=== 保真模式（TB_STUB_FIDELITY=1，注入真实 js/common.js）===");
  for (const r of ran) {
    if (r.error || r.pass !== r.total) {
      console.log(`  ❌ ${label(r.file)}  ${r.error || r.pass + "/" + r.total}` + (r.failed.length ? "  → " + r.failed.join(", ") : ""));
    }
  }
  for (const r of skipped) console.log(`  SKIP ${label(r.file)}  ${r.reason}`);
  console.log(`  汇总：${ran.length - failed.length}/${ran.length} 分类全绿，用例 ${fSum.pass}/${fSum.total}`);

  if (report && def) {
    const dSum = sumOf(def.filter((r) => !r.skipped));
    console.log("\n=== 默认模式（简化桩，不加载 common.js）===");
    console.log(`  汇总：${def.filter((r) => !r.skipped && !r.error && r.pass === r.total).length}/${def.filter((r) => !r.skipped).length} 分类全绿，用例 ${dSum.pass}/${dSum.total}`);

    const byLabel = new Map(def.map((r) => [label(r.file), r]));
    const diffs = [];
    for (const r of ran) {
      const d = byLabel.get(label(r.file));
      if (!d || d.skipped) continue;
      const fBad = new Set(r.failed || []);
      const dBad = new Set(d.failed || []);
      const newly = [...fBad].filter((s) => !dBad.has(s));
      const noLonger = [...dBad].filter((s) => !fBad.has(s));
      if (newly.length || noLonger.length) {
        diffs.push({ cat: label(r.file), newly, noLonger });
      }
    }
    console.log("\n=== 默认 vs 保真 差异页（桩骗过我们的完整清单）===");
    if (!diffs.length) console.log("  （无差异）");
    for (const d of diffs) {
      if (d.newly.length) console.log(`  ${d.cat}: 保真红而默认绿 → ${d.newly.join(", ")}`);
      if (d.noLonger.length) console.log(`  ${d.cat}: 保真绿而默认红 → ${d.noLonger.join(", ")}`);
    }
  }

  if (failed.length) {
    console.log("\n结论：FAIL（保真模式下存在失败用例）");
    process.exit(1);
  }
  console.log("\n结论：PASS（保真模式全绿）");
  process.exit(0);
}

main().catch((e) => {
  console.error("SKIP: 脚本异常 " + (e && e.message));
  process.exit(0);
});
