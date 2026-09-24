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
  // 1) <input> 的 value 默认
  const re = /<input\b[^>]*>/g;
  let m;
  while ((m = re.exec(body))) {
    const tag = m[0];
    const id = (tag.match(/id=["']([^"']+)["']/) || [])[1];
    const val = (tag.match(/value=["']([^"']*)["']/) || [])[1];
    // 复选框/单选/按钮的 `value` 不是页面读取的「输入值」（页面读 .checked），
    // 把它们「回退空串」既无意义、又会把行为等同默认的用例误报成逃生项 ⇒ 跳过。
    const typ = ((tag.match(/type=["']([^"']*)["']/) || [])[1] || "text").toLowerCase();
    if (!id || /^(checkbox|radio|button|submit|reset|file|image)$/.test(typ)) continue;
    // 无 value 属性 ⇒ 真机默认空串（与 runCase 的 defaults/sel 口径一致）。
    // 旧版直接丢弃这类键 ⇒ 判别器无法把它们换回默认 ⇒ 整例被判「跳过」而漏检。
    // 「首次出现优先」（2026-09-24）：部分页面存在**重复 id**（多页签结构，如
    // engineering/heat-transfer 有两个 id="k"，value 分别 50 与 0.04）。浏览器
    // getElementById 返回**第一个**，旧版循环覆盖会取到最后一个 ⇒ 与真机默认不符，
    // 导致「注入值恰等于末个同名控件的默认值」时 usable=false，整例又被静默跳过。
    if (out[id] === undefined) out[id] = val !== undefined ? val : "";
  }
  // 2) <select> 的默认选中项（selected option 优先，否则取首个 option）
  //    关键修复：旧版只抓 input，导致 select 类输入（如 hirschberg 的 fixing/reflex）
  //    永远无法「换回默认」→ 判别力校验误报逃生项。真实测试其实有效（默认「正位」/
  //    非默认「明显眼位偏斜」经 probe 实测确认），是校验器盲区而非盲区用例。
  const selRe = /<select\b[^>]*\bid=["']([^"']+)["'][^>]*>([\s\S]*?)<\/select>/g;
  // 3) <textarea> 默认值（如各分析/统计页的 id="data" 多值输入）
  //    关键修复（2026-09-20）：旧版 pageDefaults 不解析 textarea，导致「注入失败」模拟
  //    永远无法把 textarea 类输入换回默认 → 这类用例被误报为「逃生项」（实为校验器盲区），
  //    同时真正依赖 textarea 默认值的弱用例也从未被本门禁覆盖（基线注释已记录此缺口）。
  //    补齐后与 runCase 的 defaults 提取口径一致：textarea 也能被回退、被真实校验。
  const taRe = /<textarea[^>]*id=["']([^"']+)["'][^>]*>([\s\S]*?)<\/textarea>/g;
  let ta;
  while ((ta = taRe.exec(body))) {
    if (out[ta[1]] === undefined) {
      out[ta[1]] = ta[2].replace(/&#10;/g, "\n").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
    }
  }
  let s;
  while ((s = selRe.exec(body))) {
    const id = s[1];
    const inner = s[2];
    const sel = inner.match(/<option[^>]*\bselected\b[^>]*value=["']([^"']*)["']/i)
             || inner.match(/<option[^>]*value=["']([^"']*)["']/i);
    if (out[id] === undefined) out[id] = sel ? sel[1] : "";
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
      // checkIds（复选框选中态）/ radios（单选组取值）/ clicks（click 驱动页的模拟点击序列）
      // 是 2026-09-24 起 harness 支持的注入字段，与 inputs 等价地构成「被测输入」。
      // 模拟注入失败 = 一并清空这三者。
      const hasInj =
        (Array.isArray(c.checkIds) && c.checkIds.length > 0) ||
        (c.radios && Object.keys(c.radios).length > 0) ||
        (Array.isArray(c.clicks) && c.clicks.length > 0);
      const clearInject = { checkIds: [], radios: {}, checks: [], clicks: [] };
      if (!c.inputs || Object.keys(c.inputs).length === 0) {
        if (!hasInj) { skipped++; continue; }   // 真正无任何注入的用例不适用
        // 清空复选框/单选注入 → 页面回到「全未勾选」态，expect 必须失配，否则即逃生项。
        total++;
        let r0;
        try { r0 = await runCase(Object.assign({}, c, clearInject)); }
        catch (e) { fail++; continue; }
        if (r0.ok) { stillPass++; bad.push(`${c.slug} (via=${r0.via})`); }
        else fail++;
        continue;
      }
      const defs = pageDefaults(c.slug);
      if (!defs) { skipped++; continue; }
      const injected = {};
      let usable = hasInj;   // 有复选框/单选注入时，即便 inputs 全为默认值也可模拟失败
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
      try { r = await runCase(Object.assign({}, c, { inputs: injected }, clearInject)); }
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
