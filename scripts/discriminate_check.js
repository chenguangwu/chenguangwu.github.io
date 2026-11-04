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
 * 做法：
 *   对用例的 inputs 逐键换回页面 HTML 里的默认值（模拟注入失败），
 *   然后跑 runCase —— 用例必须 FAIL。仍 PASS 的即含逃生项，需收紧 expect。
 *
 * 产出完整性（2026-11-05 新增，堵「静默退出 = exit 0 = CI 通过」）：
 *   - 全站模式改为**逐文件子进程**跑：任何单个页面的用例把进程静默干掉，
 *     只影响它自己的子进程，父进程照常汇总并打印统计行；
 *   - 父进程注册 exit 钩子：只要没打印统计行就强制 exit 1（绝不静默退出）；
 *   - 统计行缺失、`已检 = 0`、`已检 < TB_DISCRIM_MIN`（默认 8000）一律 FAIL；
 *   - 子进程无统计行的文件单独列为「隔离跑」，可显式报告，不吞掉；
 *     设 `TB_DISCRIM_STRICT_CHILD=1` 可把「有隔离文件」也判 FAIL。
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
const stub = require(path.join(ROOT, "scripts", "lib_stub.js"));

const FILES_ONLY = ARGV.filter((a) => !a.startsWith("--"));
const SELFTEST = ARGV.includes("--selftest");
const MIN_CHECKED = Number(process.env.TB_DISCRIM_MIN || 8000);
const CHILD_TIMEOUT = Number(process.env.TB_DISCRIM_CHILD_TIMEOUT || 120000);
const REPORT = process.env.TB_DISCRIM_REPORT === "1";
const STRICT_CHILD = process.env.TB_DISCRIM_STRICT_CHILD === "1";

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

/** 从页面 HTML 提取 input/select 的 id → 默认值（截断 deep-dive，避免抓到示例） */
function pageDefaults(slug) {
  const fp = path.join(ROOT, "tools", slug + ".html");
  if (!fs.existsSync(fp)) return null;
  const raw = fs.readFileSync(fp, "utf8");
  const cut = raw.indexOf("<!-- TOOLBOX-DEEP-DIVE -->");
  let body = cut > 0 ? raw.slice(0, cut) : raw;
  // 回退（2026-09-24）：全站 72 个页面的表单控件位于 deep-dive 标记**之后**
  // （如 engineering/heat-transfer 的 input 在第 235 行、deep-dive 在第 178 行），
  // 截断后取不到任何控件 ⇒ 所有键都「无法换回默认」⇒ 整例静默判「跳过」而漏检，
  // 而这些用例其实是有真实注入的有效用例。此处：截断后无控件、全文有控件时改用全文。
  // 安全性：本函数只提取 input/select/textarea 的 id→value，deep-dive 区块内不含表单控件。
  const CTRL = /<(?:input|select|textarea)\b/i;
  if (cut > 0 && !CTRL.test(body) && CTRL.test(raw)) body = raw;
  const out = {};
  // 默认走 legacy（TB_STUB_FIDELITY=1 才启用保真解析；TB_STUB_LEGACY=1 永久逃生）。
  if (!stub.stubFidelity()) return stub.legacyPageDefaults(body);
  // 1) <input> 的 value 默认（共用 lib_stub：属性顺序/引号无关；跳过 checkbox/radio）
  Object.assign(out, stub.parseInputDefaults(body, { skipTypes: /^(checkbox|radio|button|submit|reset|file|image)$/ }));
  // 2) <textarea> 初始文本（首次出现优先，input 同名时不覆盖）
  for (const [id, v] of Object.entries(stub.parseTextareaDefaults(body))) {
    if (out[id] === undefined) out[id] = v;
  }
  // 3) <select> 默认选中项（共用 lib_stub：尊重 selected，两种写法皆可，无则回退首个）
  for (const [id, opts] of Object.entries(stub.parseSelects(body))) {
    if (out[id] === undefined) out[id] = stub.selectDefault(opts);
  }
  return out;
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

function reportRec(obj) {
  if (REPORT) REAL_PROCESS.stdout.write("REPORT " + JSON.stringify(obj) + "\n");
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

  for (const c of CASES) {
    // checkIds（复选框选中态）/ radios（单选组取值）/ clicks（click 驱动页的模拟点击序列）
    // 是 2026-09-24 起 harness 支持的注入字段，与 inputs 等价地构成「被测输入」。
    // 模拟注入失败 = 一并清空这三者。
    const hasInj =
      (Array.isArray(c.checkIds) && c.checkIds.length > 0) ||
      (c.radios && Object.keys(c.radios).length > 0) ||
      (Array.isArray(c.clicks) && c.clicks.length > 0);
    const clearInject = { checkIds: [], radios: {}, checks: [], clicks: [] };
    // checks（声明「已选中项」的 value）同样构成真实注入，但它可能只作 inputs 的修饰项，
    // 故仅在「无 inputs」分支并入适用性判定（与 selfcheck_false_pass.weakKind 口径一致）：
    // 否则纯 checks 驱动的量表页会被计入 skipped 而漏检。
    const hasChecks = Array.isArray(c.checks) && c.checks.length > 0;
    const base = { file: f, slug: c.slug, ref: c.ref || "", expect: c.expect || [] };

    if (!c.inputs || Object.keys(c.inputs).length === 0) {
      if (!hasInj && !hasChecks) {
        stats.skipped++;
        reportRec(Object.assign({}, base, { kind: "skip", why: "no-inject", inputs: {} }));
        continue;   // 真正无任何注入的用例不适用
      }
      // 清空复选框/单选注入 → 页面回到「全未勾选」态，expect 必须失配，否则即逃生项。
      stats.total++;
      let r0;
      try { r0 = await runCase(Object.assign({}, c, clearInject)); }
      catch (e) { stats.fail++; continue; }
      if (r0.ok) {
        stats.stillPass++;
        bad.push(`${c.slug} (via=${r0.via})`);
        reportRec(Object.assign({}, base, {
          kind: "escape", via: r0.via, why: "clear-inject-still-pass",
          inputs: c.inputs || {}, checkIds: c.checkIds || [], radios: c.radios || {}, clicks: c.clicks || [],
        }));
      } else stats.fail++;
      continue;
    }
    const defs = pageDefaults(c.slug);
    if (!defs) {
      stats.skipped++;
      reportRec(Object.assign({}, base, { kind: "skip", why: "no-page", inputs: c.inputs }));
      continue;
    }
    const injected = {};
    let usable = hasInj;   // 有复选框/单选注入时，即便 inputs 全为默认值也可模拟失败
    const sameAsDefault = [];
    const unresolved = [];
    for (const k of Object.keys(c.inputs)) {
      if (defs[k] !== undefined && String(defs[k]) !== String(c.inputs[k])) {
        injected[k] = String(defs[k]);   // 换回默认值 = 模拟注入失败
        usable = true;
      } else {
        injected[k] = String(c.inputs[k]);
        if (defs[k] !== undefined) sameAsDefault.push({ id: k, def: String(defs[k]), injected: String(c.inputs[k]) });
        else unresolved.push(k);
      }
    }
    if (!usable && !hasInj) {
      stats.skipped++;
      // 区分两类跳过（口径必须分开，否则工单会把「控件解析不到」误当成 all_default 弱用例）：
      //   all-default  —— 所有键都能解析到默认值，且注入值恰好等于默认值（真弱用例）
      //   unresolved   —— 至少一个键在页面 HTML 里找不到默认值（桩/页面解析缺口，需人工）
      reportRec(Object.assign({}, base, {
        kind: "skip",
        why: unresolved.length ? "unresolved" : "all-default",
        inputs: c.inputs, sameAsDefault, unresolved,
        defaults: defs,
      }));
      continue;  // 注入值本就等于默认值，无法模拟
    }
    stats.total++;
    let r;
    try { r = await runCase(Object.assign({}, c, { inputs: injected }, clearInject)); }
    catch (e) { stats.fail++; continue; }
    if (r.ok) {
      stats.stillPass++;
      bad.push(`${c.slug} (via=${r.via})`);
      reportRec(Object.assign({}, base, {
        kind: "escape", via: r.via, why: "revert-to-default-still-pass",
        inputs: c.inputs || {}, checkIds: c.checkIds || [], radios: c.radios || {}, clicks: c.clicks || [],
        reverted: injected,
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
  const truncated = runIsolated(fakePath);
  say(!truncated.ok, `假 harness（用例内 process.exit(0)）→ ${truncated.ok ? "被当成通过" : "识别为无统计行：" + truncated.why}`);

  // ③ 统计行存在但已检过低 → 下限守卫必须变红
  const problems = integrityProblems({ total: 3, fail: 3, stillPass: 0, skipped: 0 }, { enforceMin: true });
  say(problems.length > 0, `已检=3 < 下限 ${MIN_CHECKED} → ${problems.length ? "判 FAIL：" + problems[0] : "被放过"}`);

  // ④ 正常规模统计行 → 守卫不应误伤
  const okProblems = integrityProblems({ total: 9000, fail: 8998, stillPass: 2, skipped: 54 }, { enforceMin: true });
  say(okProblems.length === 0, `已检=9000 → ${okProblems.length ? "误判 FAIL：" + okProblems[0] : "正常放行"}`);

  REAL_LOG(failed ? `\n❌ 自检失败 ${failed} 项` : "\n✅ 自检通过：静默退出/截断跑/低总量均会变红");
  statsPrinted = true;   // 自检本身已完整输出，勿触发「产出不完整」钩子
  REAL_PROCESS.exitCode = failed ? 1 : 0;
}

// 模拟「跑到一半就 return」：不打印任何统计行直接退出（供 --selftest 的第 ① 项）
if (process.env.TB_DISCRIM_SELFTEST_SILENT === "1" && FILES_ONLY.length === 0) {
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
    REAL_LOG(`\n✅ 逃生项 ${agg.stillPass} = 基线 ${basey.escape}，无新增（存量见基线注释）`);
    REAL_PROCESS.exitCode = 0;
    return;
  }

  if (bad.length) { REAL_PROCESS.exitCode = 1; return; }
  if (agg.total) REAL_LOG("✅ 全部用例在注入失败时均会变红 —— 判别力真实有效");
  REAL_PROCESS.exitCode = 0;
})();
