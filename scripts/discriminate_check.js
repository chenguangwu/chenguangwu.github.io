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
 *   对用例的 inputs 逐键换回页面 HTML 里的 value 默认值（模拟注入失败），
 *   然后跑 runCase —— 用例必须 FAIL。仍 PASS 的即含逃生项，需收紧 expect。
 *
 * 用法：
 *   node scripts/discriminate_check.js                       # 全站（慢）
 *   node scripts/discriminate_check.js verify_energy_calc.js # 指定脚本
 *
 * 退出码：0 = 全部用例判别力有效；1 = 发现逃生项。
 */
const fs = require("fs");
const path = require("path");

const ARGV = process.argv.slice(2);        // 必须提前保存：verify_it_calc.js 运行期会替换 process
const REAL_PROCESS = process;             // 同上：运行期写 REAL_PROCESS.exitCode 无效，须用真实引用
const ROOT = path.resolve(__dirname, "..");
const { runCase } = require(path.join(ROOT, "scripts", "verify_it_calc.js"));

/** 从页面 HTML 提取所有 input 的 id → value 默认值（截断 deep-dive，避免抓到示例） */
function pageDefaults(slug) {
  const fp = path.join(ROOT, "tools", slug + ".html");
  if (!fs.existsSync(fp)) return null;
  const raw = fs.readFileSync(fp, "utf8");
  const cut = raw.indexOf("<!-- TOOLBOX-DEEP-DIVE -->");
  const body = cut > 0 ? raw.slice(0, cut) : raw;
  const out = {};
  const re = /<input\b[^>]*>/g;
  let m;
  while ((m = re.exec(body))) {
    const tag = m[0];
    const id = (tag.match(/id=["']([^"']+)["']/) || [])[1];
    const val = (tag.match(/value=["']([^"']*)["']/) || [])[1];
    if (id && val !== undefined) out[id] = val;
  }
  return out;
}

function listFiles() {
  return fs.readdirSync(path.join(ROOT, "scripts"))
    .filter((f) => /^verify_.*_calc\.js$/.test(f))
    .sort();
}

(async () => {
  const args = ARGV;
  const files = args.length ? args : listFiles();

  let total = 0, stillPass = 0, fail = 0, skipped = 0;
  const bad = [];

  for (const f of files) {
    const fp = path.join(ROOT, "scripts", f);
    if (!fs.existsSync(fp)) { console.log("SKIP(不存在)", f); continue; }
    const src = fs.readFileSync(fp, "utf8");
    const m = src.match(/const CASES = (\[[\s\S]*?\n\]);/);
    if (!m) { console.log("SKIP(无 CASES)", f); continue; }
    let CASES;
    try { CASES = eval(m[1]); } catch (e) { console.log("SKIP(解析失败)", f, e.message); continue; }

    for (const c of CASES) {
      if (!c.inputs || Object.keys(c.inputs).length === 0) { skipped++; continue; }  // 无输入用例不适用
      const defs = pageDefaults(c.slug);
      if (!defs) { skipped++; continue; }
      const injected = {};
      let usable = false;
      for (const k of Object.keys(c.inputs)) {
        if (defs[k] !== undefined && String(defs[k]) !== String(c.inputs[k])) {
          injected[k] = String(defs[k]);   // 换回默认值 = 模拟注入失败
          usable = true;
        } else {
          injected[k] = String(c.inputs[k]);
        }
      }
      if (!usable) { skipped++; continue; }  // 注入值本就等于默认值，无法模拟
      total++;
      let r;
      try { r = await runCase(Object.assign({}, c, { inputs: injected })); }
      catch (e) { fail++; continue; }
      if (r.ok) { stillPass++; bad.push(`${c.slug} (via=${r.via})`); }
      else fail++;
    }
  }

  console.log(`\n==== 判别力验证（模拟注入失败 → 用例应 FAIL）====`);
  console.log(`已检: ${total} | 正确变红: ${fail} | 仍 PASS(逃生项): ${stillPass} | 跳过: ${skipped}`);
  if (bad.length) {
    console.log("\n仍 PASS（expect 含不依赖被测点的逃生项，需收紧）:");
    bad.forEach((b) => console.log("  -", b));
  }

  // 基线防回归：存量逃生项入基线，只准降不准增；新增逃生项立即变红。
  // 仅在「全站模式」下比对基线（指定单个脚本时按严格模式：有任何逃生项即红）。
  const isFullSite = !ARGV.length;
  const BASE_FP = path.join(ROOT, "scripts", "discriminate_baseline.json");
  if (isFullSite && fs.existsSync(BASE_FP)) {
    const base = JSON.parse(fs.readFileSync(BASE_FP, "utf8"));
    if (stillPass > base.escape) {
      console.log(`\n❌ 突破基线：逃生项 ${stillPass} > 基线 ${base.escape}（新增 ${stillPass - base.escape} 个）`);
      REAL_PROCESS.exitCode = 1;   // 注意：verify_it_calc.js 会覆盖 process.exit，只能用 exitCode
      return;
    }
    if (stillPass < base.escape) {
      console.log(`\n⚠️ 逃生项已下降（${base.escape} → ${stillPass}），请将基线同步下调后提交。`);
      REAL_PROCESS.exitCode = 1;   // 强制棘轮：下降时必须更新基线，防止悄悄回涨
      return;
    }
    console.log(`\n✅ 逃生项 ${stillPass} = 基线 ${base.escape}，无新增（存量见基线注释）`);
    REAL_PROCESS.exitCode = 0;
    return;
  }

  if (bad.length) {
    REAL_PROCESS.exitCode = 1;
    return;
  }
  if (total) console.log("✅ 全部用例在注入失败时均会变红 —— 判别力真实有效");
  REAL_PROCESS.exitCode = 0;
})();
