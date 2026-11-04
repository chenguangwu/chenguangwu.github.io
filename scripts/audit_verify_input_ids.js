#!/usr/bin/env node
/**
 * 只读普查：verify_*_calc.js 的用例注入键 ↔ 工具页 HTML 的 id 存在性。
 *
 * 背景：用例 inputs 的键若在页面里不存在（页面改过 id / 只在旧版有），
 * getEl 会造出游离桩元素 → 注入落空 → 断言值恰好等于默认态 → 用例绿但零判别力。
 * 静态门禁（selfcheck_false_pass / discriminate_check）都抓不到这种「僵尸 id」。
 *
 * 三档口径（保守判定，避免误报）：
 *   ③ 存在        页面静态 HTML 里能搜到 `id="x"` / `id='x'`
 *   ② 动态/存疑   静态没有该 id 属性，但全文出现带引号的字面量 "x" / 'x'
 *                 （可能由 JS innerHTML / setAttribute / createElement 生成）
 *   ① 确认不存在  静态无 id 属性，且全文也搜不到该字面量
 *
 * 仅判 inputs 的**键**与 checkIds 的元素，绝不把 inputs 的**值**当 id 查。
 *
 * 用法：
 *   node scripts/audit_verify_input_ids.js                 # 全量
 *   node scripts/audit_verify_input_ids.js verify_hydraulic_calc.js  # 校准单文件
 *   node scripts/audit_verify_input_ids.js --top 30
 */
const fs = require("fs");
const path = require("path");

// 本脚本 require verify_it_calc.js 只为复用 extractCases；harness 的 beforeExit 兜底会把
// 「0 个用例实际执行」判红并覆盖 process.exitCode=1 ⇒ 本门禁将永远无法转绿。
// 该环境变量是 harness 已有的父进程逃生口（见 verify_it_calc.js beforeExit），此处只抑制兜底。
process.env.TB_DISCRIM_PARENT = "1";

const ROOT = path.join(__dirname, "..");
const TOOLS = path.join(ROOT, "tools");
const { extractCases } = require(path.join(__dirname, "verify_it_calc.js"));

function argVal(flag, dflt) {
  const i = process.argv.indexOf(flag);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}

function classify(html, id) {
  const esc = id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  if (new RegExp(`id\\s*=\\s*"${esc}"`).test(html) || new RegExp(`id\\s*=\\s*'${esc}'`).test(html)) return 3;
  if (html.includes(`"${id}"`) || html.includes(`'${id}'`)) return 2;
  // 页面存在「id 模板」（id="${...}" / setAttribute("id", …)）⇒ 静态无法判定生成哪一批 id
  if (/id\s*=\s*"\$\{/.test(html) || /id\s*=\s*'\$\{/.test(html) || /setAttribute\(\s*["']id["']/.test(html)) return 2;
  // 动态生成：id 由「字面量前缀 + 变量」拼接（'q'+i、'sens_'+seg+'_'+type、`m${r}_${c}`）
  for (const m of html.matchAll(/(["'])([A-Za-z_][A-Za-z0-9_-]*)\1\s*\+/g)) {
    if (id.startsWith(m[2]) && id.length > m[2].length) return 2;
  }
  const pre = (id.match(/^[A-Za-z_]+/) || [""])[0];
  if (pre) {
    const p = pre.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const dyn = [
      new RegExp(`['"]${p}['"]\\s*\\+`),   // 'q' + i
      new RegExp("`" + p + "\\$\\{"),       // `q${i}`
      new RegExp(`id\\s*=\\s*"${p}\\$\\{`),  // id="q${i}"
      new RegExp(`id\\s*=\\s*'${p}'\\s*\\+`), // id='q' + i
    ];
    if (dyn.some((re) => re.test(html))) return 2;
  }
  return 1;
}

const files = process.argv.slice(2).filter((a) => !a.startsWith("--") && a.endsWith(".js"));
const targets = files.length
  ? files.map((f) => (path.isAbsolute(f) ? f : path.join(__dirname, f)))
  : fs.readdirSync(__dirname).filter((f) => /^verify_.+_calc\.js$/.test(f)).map((f) => path.join(__dirname, f));

const zombies = []; // ① 确认不存在
const suspicious = []; // ② 动态/存疑
let cases = 0, idTotal = 0, missingPage = 0;

for (const file of targets) {
  const src = fs.readFileSync(file, "utf8");
  const list = extractCases(src) || [];
  const fname = path.basename(file);
  for (const c of list) {
    cases++;
    const page = path.join(TOOLS, String(c.slug) + ".html");
    if (!fs.existsSync(page)) {
      missingPage++;
      continue;
    }
    const html = fs.readFileSync(page, "utf8");
    const ids = [];
    for (const k of Object.keys(c.inputs || {})) ids.push(["inputs", k]);
    for (const k of c.checkIds || []) ids.push(["checkIds", k]);
    const bad = [], dyn = [];
    for (const [srcKind, id] of ids) {
      idTotal++;
      const tier = classify(html, id);
      if (tier === 1) bad.push(id);
      else if (tier === 2) dyn.push(id);
    }
    if (bad.length) zombies.push({ fname, slug: c.slug, kind: "僵尸id", ids: bad.join(","), src: c.ref || "", caseObj: c });
    if (dyn.length) suspicious.push({ fname, slug: c.slug, ids: dyn.join(",") });
  }
}

console.log(`扫描文件 ${targets.length} 个 / 用例 ${cases} 条 / 注入键 ${idTotal} 个 / 缺页 ${missingPage}`);
console.log(`① 确认不存在（僵尸 id）：${zombies.length} 条用例涉及`);
console.log(`② 动态生成存疑：${suspicious.length} 条用例涉及`);
console.log(`③ 存在：${cases - zombies.length - suspicious.length - missingPage} 条用例全键命中`);

const byFile = {};
for (const z of zombies) byFile[z.fname] = (byFile[z.fname] || 0) + 1;
console.log("\n按分类（verify 文件）分布：");
for (const [f, n] of Object.entries(byFile).sort((a, b) => b[1] - a[1])) console.log(`  ${f}: ${n}`);

const top = Number(argVal("--top", 30));
console.log(`\n前 ${top} 条 ①（文件 / 用例 / 僵尸 id）：`);
for (const z of zombies.slice(0, top)) console.log(`  ${z.fname} | ${z.slug} | ${z.ids}`);

if (argVal("--suspicious", "") === "1") {
  console.log("\n② 动态/存疑明细：");
  for (const s of suspicious) console.log(`  ${s.fname} | ${s.slug} | ${s.ids}`);
}
if (argVal("--run", "") === "1") {
  const { runCase } = require(path.join(__dirname, "verify_it_calc.js"));
  (async () => {
    let green = 0;
    for (const z of zombies) {
      const r = await runCase(z.caseObj);
      z.state = r.ok ? "GREEN" : "RED";
      if (r.ok) green++;
    }
    console.log(`\n僵尸 id 用例中目前仍为 GREEN（绿着但注入落空）：${green} / ${zombies.length}`);
    for (const z of zombies.filter((x) => x.state === "GREEN")) console.log(`  GREEN ${z.fname} | ${z.slug} | ${z.ids}`);
  })().catch((e) => { console.error(e); process.exitCode = 1; });
}
if (argVal("--json", "") === "1") {
  console.log("\nJSON=" + JSON.stringify({ zombies: zombies.map(({ caseObj, ...r }) => r), suspicious }));
}
process.exitCode = zombies.length ? 1 : 0;
