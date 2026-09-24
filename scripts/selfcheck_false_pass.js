#!/usr/bin node
"use strict";
/**
 * 门禁「假门禁 / 假通过」反回归扫描。
 *
 * 设计要点（相对旧版的关键修正）：
 *   旧版对所有用例做「默认态执行 → expect 命中即 RISK」，会**误伤真用例**：
 *   energy / sports / health 等分类的 expect（如 "24.00 W"、"50.00%"）在页面
 *   默认态也会输出，于是真用例被错判为 RISK，无法直接接进门禁。
 *   旧版全量执行还因逐文件累积 OOM（~4.4GB）。
 *
 *   本版改用**结构判定**（可靠、零误伤、零 OOM）：
 *     RISK 当且仅当用例满足以下任一：
 *       (a) c._selfcheck === true            —— 显式自校验假门禁标记；
 *       (b) 用例没有有效 inputs（inputs 缺失或为空）—— 未注入任何真实输入，
 *           等价于只对默认态/关键字做断言，无法验证计算正确性。
 *   真用例都带真实 inputs，永远不会被误判；假门禁（_selfcheck / 裸空输入）
 *   会被精准捕获。门禁接上后，任何残留或新引入的假门禁都会让门禁变红。
 *
 * 用法:
 *   node scripts/selfcheck_false_pass.js <file>          # 单文件（结构判定）
 *   node scripts/selfcheck_false_pass.js <dir>           # 扫目录下所有 verify_*_calc.js
 *   node scripts/selfcheck_false_pass.js <file> --exec   # 额外跑默认态执行自检（人工深挖用，慢）
 */
const fs = require("fs");
const path = require("path");
const { runCase } = require("./verify_it_calc.js");

const argv = process.argv.slice(2);
const target = argv.find((a) => !a.startsWith("--"));
const execMode = argv.includes("--exec");
if (!target) {
  console.error("用法: node scripts/selfcheck_false_pass.js <file|dir> [--exec]");
  process.exit(2);
}

// 字符串感知的 CASES 数组抽取：括号匹配时跳过字符串字面量（' " `）内的 [ ]，
// 否则 ref/expect 含 "(100,300]" 这类字符会让匹配错位 → eval 语法报错。
function extractCases(src) {
  const marker = "const CASES = [";
  const start = src.indexOf(marker);
  if (start === -1) return null;
  const i = src.indexOf("[", start);
  let depth = 0, inStr = null, escape = false, end = -1;
  for (let k = i; k < src.length; k++) {
    const ch = src[k];
    if (inStr) {
      if (escape) { escape = false; continue; }
      if (ch === "\\") { escape = true; continue; }
      if (ch === inStr) { inStr = null; continue; }
      continue;
    }
    if (ch === '"' || ch === "'" || ch === "`") { inStr = ch; continue; }
    // 注释必须先于引号判定：行注释 `// ── Cohen's d → U₃ ──` 里的撇号会被误当字符串起始，
    // 一路吞到下一个撇号 → 括号层级错位、end 永远找不到 → 整个用例文件「静默消失」
    // （checked=0，弱用例审计对该文件完全失效，且门禁仍全绿）。字符串内的 // 不受影响。
    if (ch === "/" && src[k + 1] === "/") { const nl = src.indexOf("\n", k); k = nl === -1 ? src.length : nl; continue; }
    if (ch === "/" && src[k + 1] === "*") { const ce = src.indexOf("*/", k + 2); k = ce === -1 ? src.length : ce + 1; continue; }
    if (ch === "[") { depth++; continue; }
    if (ch === "]") { depth--; if (depth === 0) { end = k; break; } }
  }
  if (end === -1) return null;
  const casesSrc = src.slice(start, end + 1).replace(marker, "[");
  // eslint-disable-next-line no-eval
  return eval(casesSrc);
}

function hasRealInputs(c) {
  return !!(c.inputs && Object.keys(c.inputs).length > 0);
}

// 占位 expect 判定（与 _restore_fake_gates.js 保持一致）：仅命中已知占位词才视为假，
// 这样「无输入但 expect 为真实输出片段（静态展示页）」不会被误伤。
const PLACEHOLDER = /^(ok|ok\.|结果|result|通过|pass|✓|√|占位|占位符|暂无|计算中|test|测试|-|—|·|\.|\s*)$/i;
function isPlaceholderExpect(c) {
  const toks = (c.expect || []).map((s) => String(s).trim());
  if (!toks.length) return true;
  return toks.every((t) => PLACEHOLDER.test(t));
}

// 结构判定：是否疑似假门禁
function isFakeStruct(c) {
  if (c._selfcheck === true) return "marker";
  if (isPlaceholderExpect(c)) return "placeholder";
  return null;
}

// ── 弱用例（无判别力）判定 —— 补旧版两个盲区 ──────────────────
// 盲区1：文件头注释第 15–16 行声明「用例没有有效 inputs」判 RISK，
//        但 isFakeStruct() 从未调用 hasRealInputs()，该判定实际从未生效。
// 盲区2：「用例注入值 == 页面默认值」——框架在编译期已跑过一次默认态 calc()，
//        注入失败时默认结果恰好命中期望 → 假通过（项目记忆中的头号假通过机制）。
// 存量弱用例登记在 scripts/falsepass_baseline.json：只允许下降，新增即让门禁红。
const BASELINE_PATH = path.join(__dirname, "falsepass_baseline.json");
const _htmlCache = new Map();
const _escRe = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const _norm = (v) => String(v == null ? "" : v).trim();

function _pageDefaults(html, ids) {
  const out = {};
  for (const id of ids) {
    let m = html.match(new RegExp('<input\\b[^>]*\\bid=["\']' + _escRe(id) + '["\'][^>]*>', "i"));
    if (m) {
      const vm = m[0].match(/\bvalue=["']([^"']*)["']/);
      out[id] = vm ? vm[1] : "";
      continue;
    }
    let ms = html.match(new RegExp('<select\\b[^>]*\\bid=["\']' + _escRe(id) + '["\'][^>]*>([\\s\\S]*?)</select>', "i"));
    if (ms) {
      const sel = ms[1].match(/<option[^>]*\\bselected\\b[^>]*value=["\']([^"\']*)["\']/i)
               || ms[1].match(/<option[^>]*value=["\']([^"\']*)["\']/i);
      out[id] = sel ? sel[1] : "";
      continue;
    }
    let mt = html.match(new RegExp('<textarea\\b[^>]*\\bid=["\']' + _escRe(id) + '["\'][^>]*>([\\s\\S]*?)</textarea>', "i"));
    if (mt) { out[id] = mt[1].trim(); continue; }
    out[id] = null;
  }
  return out;
}

function weakKind(c) {
  const keys = Object.keys(c.inputs || {});
  // checkIds / radios / clicks 是**真实输入注入**，与 inputs 等价 ——
  // checkIds：复选框选中态（getElementById(id).checked）；radios：单选组取值（getElementsByName）；
  // clicks：click 驱动型页面（选项为 span/div + onclick，无任何表单控件）的「模拟用户点击」序列。
  // 不认这三者，纯 checkbox 量表页（curb65 / stop-bang / has-bled / rater-33 等）与量表点选页
  // （psychiatry/gad7-anxiety 等）的新用例会被误判为 no_inputs 弱用例，与「已注入输入」的事实相悖。
  const hasInjection =
    (Array.isArray(c.checkIds) && c.checkIds.length > 0) ||
    (c.radios && Object.keys(c.radios).length > 0) ||
    (Array.isArray(c.clicks) && c.clicks.length > 0);
  // checks（声明「已选中项」的 value ⇒ querySelector(':checked') 桩）同样是真实注入：
  // berg-balance-scale / flacc-scale / mmse-scoring / mmt-grading 这类**控件运行期渲染**的
  // 量表页只有一个静态容器，没有任何可注入的 input id，但页面逻辑读的正是「哪一项被选中」。
  // 不过 checks 也可能与 inputs 并存（此时它是修饰项），故仅在「无 inputs」分支计入 no_inputs 判定，
  // 不参与 all_default 判定（保持既有口径逐字节不变）。
  const hasChecked = Array.isArray(c.checks) && c.checks.length > 0;
  if (!keys.length) return (hasInjection || hasChecked) ? null : "no_inputs";
  if (hasInjection) return null;
  const p = path.join(__dirname, "..", "tools", String(c.slug || "") + ".html");
  if (!fs.existsSync(p)) return null;
  if (!_htmlCache.has(p)) _htmlCache.set(p, fs.readFileSync(p, "utf8"));
  const defs = _pageDefaults(_htmlCache.get(p), keys);
  if (keys.some((k) => defs[k] === null)) return null; // id 不在页面：交由结构判定，不重复计数
  if (keys.every((k) => _norm(c.inputs[k]) === _norm(defs[k]))) return "all_default";
  return null;
}

async function scanFile(file, exec) {
  const src = fs.readFileSync(file, "utf8");
  let CASES;
  try {
    CASES = extractCases(src);
  } catch (e) {
    return { file: path.basename(file), checked: 0, risk: 0, skip: "eval:" + e.message.slice(0, 50) };
  }
  if (!CASES || !CASES.length) return { file: path.basename(file), checked: 0, risk: 0 };

  let risk = 0, checked = 0;
  const reasons = [];
  const weak = { no_inputs: 0, all_default: 0 };
  for (const c of CASES) {
    checked++;
    const why = isFakeStruct(c);
    if (why) {
      risk++;
      reasons.push(`${c.slug || "?"} (${why})`);
      continue;
    }
    // 弱用例（无判别力）统计：不影响硬失败判定，仅入基线防回归
    const wk = weakKind(c);
    if (wk) weak[wk]++;
    // 真用例：可选执行态自检（仅人工深挖时开启，门禁默认不跑，避免 OOM/误伤）
    if (exec) {
      try {
        const r = await runCase({ slug: c.slug, expect: c.expect });
        if (r.ok) {
          risk++;
          reasons.push(`${c.slug} (default-hit)`);
        }
      } catch (_) { /* 页面执行异常不计入结构判定 */ }
    }
  }
  return { file: path.basename(file), checked, risk, reasons, weak };
}

(async () => {
  const stat = fs.statSync(target);
  let files;
  if (stat.isDirectory()) {
    files = fs.readdirSync(target).filter((f) => /^verify_.*_calc\.js$/.test(f)).map((f) => path.join(target, f));
  } else {
    files = [target];
  }
  files.sort();

  let totalRisk = 0, totalChecked = 0, skipped = 0;
  const weak = { no_inputs: 0, all_default: 0 };
  const risky = [];
  for (const f of files) {
    const r = await scanFile(f, execMode);
    totalChecked += r.checked;
    if (r.skip) { skipped++; console.log(`SKIP ${r.file} :: ${r.skip}`); continue; }
    for (const k of Object.keys(weak)) weak[k] += (r.weak ? r.weak[k] : 0);
    if (r.risk) {
      totalRisk += r.risk;
      risky.push(`${r.file}: ${r.risk}/${r.checked}`);
      for (const re of r.reasons) console.log(`  RISK ${r.file} :: ${re}`);
    }
  }

  // 弱用例基线防回归（仅目录模式比对；单文件调试模式不比对）
  let base = null;
  const regressed = [];
  if (stat.isDirectory() && fs.existsSync(BASELINE_PATH)) {
    base = JSON.parse(fs.readFileSync(BASELINE_PATH, "utf8"));
    for (const k of Object.keys(weak)) {
      if (base[k] != null && weak[k] > base[k]) regressed.push(`${k} ${weak[k]} > 基线 ${base[k]}`);
    }
  }

  console.log(`\n==== false-pass selfcheck: checked=${totalChecked} risk=${totalRisk} skipped=${skipped} ====`);
  console.log("弱用例(无判别力): no_inputs=" + weak.no_inputs + " all_default=" + weak.all_default +
              (base ? (" | 基线: no_inputs=" + base.no_inputs + " all_default=" + base.all_default) : ""));
  if (totalRisk) {
    console.log("结论：存在 %d 个疑似假门禁（_selfcheck 标记或占位 expect），需还原为真实 expect。", totalRisk);
    process.exit(1);
  }
  if (regressed.length) {
    console.log("结论：弱用例数量突破基线（新增用例缺少判别力）—— " + regressed.join("; "));
    console.log("      修法：新用例必须提供真实 inputs，且注入值必须避开页面默认值。");
    process.exit(1);
  }
  console.log("结论：无假门禁（结构判定：所有用例均带真实 inputs 且无 _selfcheck 标记）。");
  process.exit(0);
})();
