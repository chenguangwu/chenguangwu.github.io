#!/usr/bin/env node
/**
 * 判别力验证器 —— 检查 verify 用例是否真的「会失败」。
 *
 * 背景（教训）：
 *   verify 框架的判定是「expect 任一命中即通过」（见 verify_it_calc.js）。
 *   因此只要 expect 里混入一个「不依赖被测输入」的项（例如只依赖页面默认值的
 *   df、权重和，或与默认输出数值巧合相等的项），即使输入注入完全失败，用例仍会
 *   PASS —— 这就是「逃生项」，是继「撞默认值」之后更隐蔽的假通过机制。
 *   注意：仅做「新 expect ∩ 默认输出 = ∅」的零交集断言**不足以**发现它
 *   （实测 68 例改造中，6 例通过了零交集断言却在注入失败时仍 PASS）。
 *
 * 做法（2026-11-05 第二次修正，第 ⑧ 种假绿形态）：
 *   模拟「注入失败」= **纯默认态快照**：只执行页面脚本与 DOMContentLoaded，不注入
 *   inputs / checkIds / radios / checks、不执行 clicks、不跑无参兜底，**不派发任何
 *   input/change/keyup 事件**，然后逐锚检查 expect 是否已命中；命中即含逃生项。
 *
 *   为什么不能用「把 inputs 换回默认值再跑 runCase」：那仍会派发 input/change 事件，
 *   页面 calc() 重渲染会把**加载期扫描表 / 枚举表**冲掉（acoustics/critical-distance
 *   的 Q 表、thermodynamics/heat-conduction 的扫描表、quantum 的能级表），于是
 *   「全锚默认即命中」的用例被误判成「正确变红」，报出虚假的 0 逃生。真实注入失败
 *   时页面从未收到事件、扫描表仍在，锚照样命中 ⇒ 该用例本就没有判别力。
 *
 * 产出完整性（2026-11-05 新增，堵「静默退出 = exit 0 = CI 通过」）：
 *   - 全站模式改为**逐文件子进程**跑：任何单个页面的用例把进程静默干掉，
 *     只影响它自己的子进程，父进程照常汇总并打印统计行；
 *   - 父进程注册 exit 钩子：只要没打印统计行就强制 exit 1（绝不静默退出）；
 *   - 统计行缺失、`已检 = 0`、`已检 < TB_DISCRIM_MIN`（默认 8000）一律 FAIL；
 *   - 子进程无统计行的文件单独列为「隔离跑」，可显式报告，不吞掉；
 *     「有隔离文件」默认判 FAIL（子进程无统计行 = 该文件用例从未被判别）；本地排障可
 *     设 `TB_DISCRIM_STRICT_CHILD=0` 临时放宽。
 *
 * 用法：
 *   node scripts/discriminate_check.js                        # 全站（逐文件隔离子进程）
 *   node scripts/discriminate_check.js verify_energy_calc.js  # 指定脚本（单进程严格模式）
 *   node scripts/discriminate_check.js --selftest             # 自检：证明上述防线真的会变红
 *
 * 环境变量：
 *   TB_STUB_FIDELITY=1     启用桩保真解析（默认 legacy）
 *   TB_STUB_LEGACY=1       强制回 legacy（逃生开关，优先级最高）
 *   TB_DISCRIM_MIN=N       已检下限（默认 8000）
 *   TB_DISCRIM_REPORT=1    额外输出 `REPORT <json>` 行（逐条用例明细，供工单/取证）
 *   TB_DISCRIM_CHILD_TIMEOUT=ms  单文件子进程超时（默认 120000）
 *
 * 退出码：0 = 全部用例判别力有效；1 = 发现逃生项 / 产出不完整 / 低于已检下限。
 */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

// 全站模式：用例全部在逐文件子进程里执行，父进程自身 __executedCases 恒 0。
// 告知 verify_it_calc 的「0 用例守卫」不要按父进程判红（子进程 argv 含文件名，不受影响）。
process.env.TB_DISCRIM_PARENT = "1";
const ARGV = process.argv.slice(2);        // 必须提前保存：verify_it_calc.js 运行期会替换 process
const REAL_PROCESS = process;             // 同上：运行期写 REAL_PROCESS.exitCode 无效，须用真实引用
// 同理保存真实 console.log：tools/it/code-runner.html 会在用例里改写 window.console，
// 直接用 console.log 的话，跑过该页之后所有输出（含最终汇总）都会被吞掉。
const REAL_LOG = console.log.bind(console);
const ROOT = path.resolve(__dirname, "..");
const { runCase } = require(path.join(ROOT, "scripts", "verify_it_calc.js"));

const FILES_ONLY = ARGV.filter((a) => !a.startsWith("--"));
const SELFTEST = ARGV.includes("--selftest");
const MIN_CHECKED = Number(process.env.TB_DISCRIM_MIN || 8000);
const CHILD_TIMEOUT = Number(process.env.TB_DISCRIM_CHILD_TIMEOUT || 120000);
// 单条用例超时：harness 兜底阶段会无参调用页面全部顶层函数，若某函数返回一个「永不
// settle 的 Promise」（如 office/pdf-split 的 pdfjsReady() 轮询在桩定时器预算耗尽后
// 再也不会 resolve/reject），await 就永远挂住 —— 子进程静默退出、整个文件被判隔离，
// 其用例从未真正判别。用 Promise.race 给每条用例兜底：超时按 FAIL 计（注入失败时该
// 用例没有 PASS，属负向证据成立），并单独打印 ⏱ 行便于追溯，不放宽任何判定。
const CASE_TIMEOUT = Number(process.env.TB_DISCRIM_CASE_TIMEOUT || 15000);
const REPORT = process.env.TB_DISCRIM_REPORT === "1";
// 默认严格：任何「无统计行的隔离文件」都必须判 FAIL（其用例全部逃过判别）。
const STRICT_CHILD = process.env.TB_DISCRIM_STRICT_CHILD !== "0";

// ---------------------------------------------------------------- 产出完整性断言
// 关键：任何「没跑到终点就退出」都必须变成 exit 1。Node 在事件循环为空时会静默
// exit 0（如 office/pdf-split 的 pdfjsReady 轮询 Promise 在 harness 内永不 settle，
// 定时器又不持有事件循环）—— 这种情况此前会被 CI 当成「全站 0 逃生」通过。
let statsPrinted = false;
REAL_PROCESS.on("exit", () => {
  if (statsPrinted) return;
  try {
    REAL_PROCESS.stdout.write("\n❌ 产出不完整：未打印统计行（疑似静默退出），强制 exit 1\n");
  } catch (e) { /* 忽略输出失败，仍要改退出码 */ }
  REAL_PROCESS.exitCode = 1;
});

/** 统一判断「这一轮统计是否可信」，返回问题清单（空 = 通过） */
function integrityProblems(agg, opts) {
  const p = [];
  if (agg.total === 0) p.push("已检 = 0（整轮没有真正执行任何用例）");
  else if (opts.enforceMin && agg.total < MIN_CHECKED) {
    p.push(`已检 ${agg.total} < 既定下限 ${MIN_CHECKED}（疑似跑到一半就退出）`);
  }
  if (opts.isolatedCount && STRICT_CHILD) {
    p.push(`有 ${opts.isolatedCount} 个 verify 文件无统计行（静默退出，未计入总量）`);
  }
  return p;
}

function listFiles() {
  return fs.readdirSync(path.join(ROOT, "scripts"))
    .filter((f) => /^verify_.*_calc\.js$/.test(f))
    .sort();
}

/** 文件解析：支持 scripts/ 下的裸文件名，也支持自检用的绝对路径（/tmp 假 harness） */
function resolveFile(f) {
  return path.isAbsolute(f) ? f : path.join(ROOT, "scripts", f);
}

/** expect 匹配口径：原文命中，或原文的 HTML 转义形态命中（与 verify_it_calc 的 blobHasWant 一致） */
function htmlEscaped(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function reportRec(obj) {
  if (REPORT) REAL_PROCESS.stdout.write("REPORT " + JSON.stringify(obj) + "\n");
}

/** 单条用例带超时执行：返回值与 runCase 相同；超时抛 message=CASE_TIMEOUT 的错误 */
async function runCaseGuarded(c) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error("CASE_TIMEOUT")), CASE_TIMEOUT);
  });
  try { return await Promise.race([runCase(c), timeout]); }
  finally { clearTimeout(timer); }
}

/** 单文件用例扫描（子进程与单进程严格模式共用）；返回统计与逃生清单 */
async function sweepFile(f) {
  const stats = { total: 0, fail: 0, stillPass: 0, skipped: 0 };
  const bad = [];
  const fp = resolveFile(f);
  if (!fs.existsSync(fp)) { REAL_LOG("SKIP(不存在)", f); return { stats, bad }; }
  const src = fs.readFileSync(fp, "utf8");
  const m = src.match(/const CASES = (\[[\s\S]*?\n\]);/);
  if (!m) { REAL_LOG("SKIP(无 CASES)", f); return { stats, bad }; }
  let CASES;
  try { CASES = eval(m[1]); } catch (e) { REAL_LOG("SKIP(解析失败)", f, e.message); return { stats, bad }; }

  // 纯默认态快照缓存：同一页面（slug + 浏览器保真开关）只跑一次，避免重复加载页面脚本。
  // afterLoad / dynDom / dynInputs 只影响桩的保真度，不构成注入，故按用例原样带上。
  const snapCache = new Map();
  const snapshotOf = async (c) => {
    const key = JSON.stringify([c.slug, !!c.afterLoad, !!c.dynDom, !!c.dynInputs]);
    if (snapCache.has(key)) return snapCache.get(key);
    let r;
    try {
      // 关键：只传 slug 与保真开关 + snapshotOnly。绝不传 inputs / checkIds / radios /
      // checks / clicks ⇒ harness 不注入控件值、不派发 input/change/keyup、不跑兜底。
      r = await runCaseGuarded({
        slug: c.slug,
        afterLoad: !!c.afterLoad,
        dynDom: !!c.dynDom,
        dynInputs: !!c.dynInputs,
        snapshotOnly: true,
      });
    } catch (e) {
      r = { ok: false, timeout: !!(e && e.message === "CASE_TIMEOUT"), why: "snapshot-error: " + ((e && e.message) || e) };
    }
    snapCache.set(key, r);
    return r;
  };

  for (const c of CASES) {
    // 锚的归一必须与 harness 完全一致：verify_it_calc 直接 `blob.includes(want)`，
    // 因此嵌套数组（expect: [["60.00"]]）会被 Array.toString 强转成 "60.00" 参与匹配。
    // 早期版本只收 typeof === "string"，把这类**有效用例**误判 no-expect 静默跳过
    // （实测 17 条：surveying 6 个 slug 12 条 + biz/data/it/life 5 条）。
    const expects = Array.isArray(c.expect) ? c.expect.map((x) => String(x)) : [];
    // 适用性：用例必须声明过某种注入（inputs / checkIds / radios / checks / clicks），
    // 否则「注入失败」无从谈起 —— 真·无注入用例不参与判别。
    const hasInputs = !!(c.inputs && Object.keys(c.inputs).length > 0);
    const hasInj = hasInputs
      || (Array.isArray(c.checkIds) && c.checkIds.length > 0)
      || (c.radios && Object.keys(c.radios).length > 0)
      || (Array.isArray(c.checks) && c.checks.length > 0)
      || (Array.isArray(c.clicks) && c.clicks.length > 0);
    const base = { file: f, slug: c.slug, ref: c.ref || "", expect: c.expect || [] };
    if (!hasInj) {
      stats.skipped++;
      reportRec(Object.assign({}, base, { kind: "skip", why: "no-inject", inputs: {} }));
      continue;
    }
    if (!expects.length) {
      stats.skipped++;
      reportRec(Object.assign({}, base, { kind: "skip", why: "no-expect", inputs: c.inputs || {} }));
      continue;
    }

    const snap = await snapshotOf(c);
    if (snap.skipped) {          // TOOLBOX-REDIRECT 存根：页面本身不参与验证
      stats.skipped++;
      REAL_LOG(`⏭ ${c.slug} 是 TOOLBOX-REDIRECT 存根（不参与判别）`);
      reportRec(Object.assign({}, base, { kind: "skip", why: "redirect-stub" }));
      continue;
    }
    if (snap.why === "文件不存在") {
      stats.skipped++;
      REAL_LOG(`⏭ ${c.slug} 页面文件不存在（不参与判别）`);
      reportRec(Object.assign({}, base, { kind: "skip", why: "no-page", inputs: c.inputs || {} }));
      continue;
    }
    if (snap.timeout) {
      // 快照取不到 ⇒ 默认态是否命中无从判定。既不能算「正确变红」（无证据），也不
      // 算逃生项；显式计跳过并打印，由基线棘轮拦住静默增长。
      stats.skipped++;
      REAL_LOG(`⏱ ${c.slug} 默认态快照超时 ${CASE_TIMEOUT}ms（页面无参函数返回永不 settle 的 Promise），未参与判别`);
      reportRec(Object.assign({}, base, { kind: "skip", why: "snapshot-timeout", inputs: c.inputs || {} }));
      continue;
    }
    if (snap.fullBlob == null) {
      stats.skipped++;
      REAL_LOG(`⏱ ${c.slug} 默认态快照缺失（${snap.why || "unknown"}），未参与判别`);
      reportRec(Object.assign({}, base, { kind: "skip", why: "no-snapshot", detail: snap.why || "" }));
      continue;
    }

    stats.total++;
    const hits = expects.filter((w) => snap.fullBlob.includes(w) || snap.fullBlob.includes(htmlEscaped(w)));
    if (hits.length) {
      stats.stillPass++;
      bad.push(`${c.slug} (默认态命中 ${hits.length}/${expects.length})`);
      reportRec(Object.assign({}, base, {
        kind: "escape", why: "default-snapshot-still-pass", hits,
        inputs: c.inputs || {}, checkIds: c.checkIds || [], radios: c.radios || {}, clicks: c.clicks || [],
      }));
    } else stats.fail++;
  }
  return { stats, bad };
}

/** 解析子进程输出里的统计行 */
const STATS_RE = /已检: (\d+) \| 正确变红: (\d+) \| 仍 PASS\(逃生项\): (\d+) \| 跳过: (\d+)/;

/** 单文件隔离跑：子进程 + 超时 kill；无统计行 = 该文件静默退出，单独报告 */
function runIsolated(f) {
  const r = spawnSync(REAL_PROCESS.execPath, [__filename, f], {
    cwd: ROOT, encoding: "utf8", timeout: CHILD_TIMEOUT, env: REAL_PROCESS.env,
  });
  const out = (r.stdout || "") + (r.stderr || "");
  const m = out.match(STATS_RE);
  if (!m) {
    const why = r.status === null
      ? `超时或被信号终止（${r.signal || "?"}）`
      : `无统计行就退出（exit ${r.status}）`;
    return { ok: false, why, out };
  }
  const totals = { total: +m[1], fail: +m[2], stillPass: +m[3], skipped: +m[4] };
  const bad = out.split("\n").map((l) => l.trim()).filter((l) => l.startsWith("- ")).map((l) => l.slice(2));
  return { ok: true, totals, bad };
}

// ---------------------------------------------------------------- 自检（证明防线有效）
function selftest() {
  let failed = 0;
  const say = (ok, msg) => { REAL_LOG((ok ? "  ✅ " : "  ❌ ") + msg); if (!ok) failed++; };

  // ① 静默退出（未打印统计行）必须变红：子进程模拟「跑到一半就 return」
  const silent = spawnSync(REAL_PROCESS.execPath, [__filename, "--selftest-silent-parent"], {
    cwd: ROOT, encoding: "utf8",
    env: Object.assign({}, REAL_PROCESS.env, { TB_DISCRIM_SELFTEST_SILENT: "1" }),
  });
  say(silent.status === 1, `未打印统计行就跑完 → exit ${silent.status}（期望 1）`);

  // ② 只跑 3 条的假 harness：低于已检下限必须判 FAIL
  const fakePath = path.join(require("os").tmpdir(), "_disc_selftest_fake_calc.js");
  fs.writeFileSync(fakePath, [
    "const CASES = [",
    '  { slug: "office/pdf-split", inputs: {}, clicks: ["process.exit(0)"], expect: ["x"], ref: "selftest" },',
    "];",
    "",
  ].join("\n"));
  const truncated = (() => {
    // 子进程静默退出是「无统计行」的唯一可靠模拟：页面作用域里 process 不可达
    // （clicks 里的 process.exit(0) 会被 sandbox 拦成普通异常），故用测试专用环境变量
    // 让子进程在扫描前直接退出（见文件末尾 TB_DISCRIM_SELFTEST_SILENT 分支）。
    REAL_PROCESS.env.TB_DISCRIM_SELFTEST_SILENT = "1";
    try { return runIsolated(fakePath); }
    finally { delete REAL_PROCESS.env.TB_DISCRIM_SELFTEST_SILENT; }
  })();
  say(!truncated.ok, `子进程静默退出（无统计行）→ ${truncated.ok ? "被当成通过" : "识别为隔离：" + truncated.why}`);

  // ③ 统计行存在但已检过低 → 下限守卫必须变红
  const problems = integrityProblems({ total: 3, fail: 3, stillPass: 0, skipped: 0 }, { enforceMin: true });
  say(problems.length > 0, `已检=3 < 下限 ${MIN_CHECKED} → ${problems.length ? "判 FAIL：" + problems[0] : "被放过"}`);

  // ④ 正常规模统计行 → 守卫不应误伤
  const okProblems = integrityProblems({ total: 9000, fail: 8998, stillPass: 2, skipped: 54 }, { enforceMin: true });
  say(okProblems.length === 0, `已检=9000 → ${okProblems.length ? "误判 FAIL：" + okProblems[0] : "正常放行"}`);

  // ⑤ 隔离文件（子进程无统计行）：默认严格必须判 FAIL（只有 TB_DISCRIM_STRICT_CHILD=0 才放宽）
  const isoProblems = integrityProblems(
    { total: 9000, fail: 8990, stillPass: 0, skipped: 55 },
    { enforceMin: true, isolatedCount: 1 }
  );
  say(
    isoProblems.some((x) => x.includes("无统计行")),
    `默认严格：1 个隔离文件 → ${isoProblems.length ? "判 FAIL：" + isoProblems[0] : "被放过"}`,
  );

  REAL_LOG(failed ? `\n❌ 自检失败 ${failed} 项` : "\n✅ 自检通过：静默退出/截断跑/低总量均会变红");
  statsPrinted = true;   // 自检本身已完整输出，勿触发「产出不完整」钩子
  REAL_PROCESS.exitCode = failed ? 1 : 0;
}

// 模拟「跑到一半就 return」：不打印任何统计行直接退出（供 --selftest 的第 ① 项）
if (process.env.TB_DISCRIM_SELFTEST_SILENT === "1") {
  REAL_PROCESS.exitCode = 0;
  return;
}

(async () => {
  if (SELFTEST) return selftest();

  // ---------- 单文件严格模式（argv 指定脚本）：行为与历史版本一致
  if (FILES_ONLY.length) {
    const agg = { total: 0, fail: 0, stillPass: 0, skipped: 0 };
    const bad = [];
    for (const f of FILES_ONLY) {
      const r = await sweepFile(f);
      agg.total += r.stats.total; agg.fail += r.stats.fail;
      agg.stillPass += r.stats.stillPass; agg.skipped += r.stats.skipped;
      bad.push(...r.bad);
    }
    REAL_LOG(`\n==== 判别力验证（模拟注入失败 → 用例应 FAIL）====`);
    REAL_LOG(`已检: ${agg.total} | 正确变红: ${agg.fail} | 仍 PASS(逃生项): ${agg.stillPass} | 跳过: ${agg.skipped}`);
    statsPrinted = true;
    if (bad.length) {
      REAL_LOG("\n仍 PASS（expect 含不依赖被测点的逃生项，需收紧）:");
      bad.forEach((b) => REAL_LOG("  -", b));
    }
    const problems = integrityProblems(agg, { enforceMin: false });
    if (problems.length) {
      REAL_LOG("\n❌ 产出完整性不合格：\n  - " + problems.join("\n  - "));
      REAL_PROCESS.exitCode = 1;
      return;
    }
    if (bad.length) { REAL_PROCESS.exitCode = 1; return; }
    if (agg.total) REAL_LOG("✅ 全部用例在注入失败时均会变红 —— 判别力真实有效");
    REAL_PROCESS.exitCode = 0;
    return;
  }

  // ---------- 全站模式：逐文件子进程（单页静默退出不拖垮整轮）
  const files = listFiles();
  const agg = { total: 0, fail: 0, stillPass: 0, skipped: 0 };
  const bad = [];
  const isolated = [];
  for (const f of files) {
    const r = runIsolated(f);
    if (!r.ok) { isolated.push({ file: f, why: r.why }); continue; }
    agg.total += r.totals.total; agg.fail += r.totals.fail;
    agg.stillPass += r.totals.stillPass; agg.skipped += r.totals.skipped;
    bad.push(...r.bad);
  }

  REAL_LOG(`\n==== 判别力验证（模拟注入失败 → 用例应 FAIL）====`);
  REAL_LOG(`已检: ${agg.total} | 正确变红: ${agg.fail} | 仍 PASS(逃生项): ${agg.stillPass} | 跳过: ${agg.skipped}`);
  statsPrinted = true;
  if (isolated.length) {
    REAL_LOG(`\n⚠️ 逐文件隔离：${isolated.length} 个 verify 文件无统计行（静默退出，贡献计 0；已单独列出，未当作通过）:`);
    isolated.forEach((x) => REAL_LOG("  -", x.file + " → " + x.why));
  }
  if (bad.length) {
    REAL_LOG("\n仍 PASS（expect 含不依赖被测点的逃生项，需收紧）:");
    bad.forEach((b) => REAL_LOG("  -", b));
  }

  const problems = integrityProblems(agg, { enforceMin: true, isolatedCount: isolated.length });
  if (problems.length) {
    REAL_LOG("\n❌ 产出完整性不合格：\n  - " + problems.join("\n  - "));
    REAL_PROCESS.exitCode = 1;
    return;
  }

  // 基线防回归：存量逃生项入基线，只准降不准增；新增逃生项立即变红。
  const BASE_FP = path.join(ROOT, "scripts", "discriminate_baseline.json");
  if (fs.existsSync(BASE_FP)) {
    const basey = JSON.parse(fs.readFileSync(BASE_FP, "utf8"));
    if (agg.stillPass > basey.escape) {
      REAL_LOG(`\n❌ 突破基线：逃生项 ${agg.stillPass} > 基线 ${basey.escape}（新增 ${agg.stillPass - basey.escape} 个）`);
      REAL_PROCESS.exitCode = 1;   // 注意：verify_it_calc.js 会覆盖 process.exit，只能用 exitCode
      return;
    }
    if (agg.stillPass < basey.escape) {
      REAL_LOG(`\n⚠️ 逃生项已下降（${basey.escape} → ${agg.stillPass}），请将基线同步下调后提交。`);
      REAL_PROCESS.exitCode = 1;   // 强制棘轮：下降时必须更新基线，防止悄悄回涨
      return;
    }
    // 跳过数棘轮：跳过 = 无任何可模拟注入的用例，其 expect 从未被判别。新增跳过必须
    // 显式改基线（逼提交者看一眼「这条用例为什么判别不了」），下降同样要求同步。
    if (typeof basey.skipped !== "number") {
      REAL_LOG(`\n❌ 基线缺少 skipped 字段（当前跳过 ${agg.skipped}）：请在 discriminate_baseline.json 显式登记。`);
      REAL_PROCESS.exitCode = 1;
      return;
    }
    if (agg.skipped > basey.skipped) {
      REAL_LOG(`\n❌ 跳过 ${agg.skipped} > 基线 ${basey.skipped}（新增 ${agg.skipped - basey.skipped} 条未参与判别，需补可解析默认值或显式改基线）`);
      REAL_PROCESS.exitCode = 1;
      return;
    }
    if (agg.skipped < basey.skipped) {
      REAL_LOG(`\n⚠️ 跳过已下降（${basey.skipped} → ${agg.skipped}），请将基线同步下调后提交。`);
      REAL_PROCESS.exitCode = 1;
      return;
    }
    REAL_LOG(`\n✅ 逃生项 ${agg.stillPass} = 基线 ${basey.escape}，跳过 ${agg.skipped} = 基线 ${basey.skipped}（无新增）`);
    REAL_PROCESS.exitCode = 0;
    return;
  }

  if (bad.length) { REAL_PROCESS.exitCode = 1; return; }
  if (agg.total) REAL_LOG("✅ 全部用例在注入失败时均会变红 —— 判别力真实有效");
  REAL_PROCESS.exitCode = 0;
})();
