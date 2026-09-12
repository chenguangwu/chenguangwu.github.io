#!/usr/bin/env node
/**
 * finance 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）；
 * 与之区别仅在于用例集：finance 用校验位算法（Luhn / mod-11 / mod-97 / Verhoeff 等）
 * 与金融公式（单利、贷款月供、ROI、NPV、盈亏平衡、增值税）的独立复算。
 *
 * 用法：
 *   node scripts/verify_finance_calc.js                        # 跑全部用例
 *   node scripts/verify_finance_calc.js credit-card-luhn tax   # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化/运行日期
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（校验位算法 / 标准公式 / 独立复算），必填，便于复核
 *
 * 期望值一律由独立实现或 python 复算得出，不凭记忆。反例（无效号）同样纳入：
 * 验证「算法对无效输入给出正确判定」与验证正例同等重要。
 * 注意：依赖图表（canvas）或依赖「今天」的工具刻意不纳入，否则门禁会随环境失败。
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  // ── 校验位算法类（11 正例 + 2 反例）──────────────────────────────
  {
    slug: "finance/credit-card-luhn",
    inputs: { input: "4532015112830366" },
    expect: ["✅ 通过"],
    ref: "Luhn（模 10）：4532015112830366 为公开测试卡号，加权和 mod 10 == 0",
  },
  {
    slug: "finance/aba-validator",
    inputs: { input: "011000015" },
    expect: ["ABA 路由号码有效"],
    ref: "ABA 3-7-1 权重：Σ = 3×0+7×1+1×1+3×0+7×0+1×0+3×0+7×1+1×5 = 20，mod 10 == 0",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "GB82WEST12345698765432" },
    expect: ["mod-97 校验通过"],
    ref: "ISO 13616：后 4 位前移 → 字母 A=10…Z=35 → 大数 mod 97 == 1（GB82 为公开示例）",
  },
  {
    slug: "finance/cpf-validator",
    inputs: { input: "52998224725" },
    expect: ["CPF 号码有效"],
    ref: "巴西 CPF 模 11 双校验：前 9 位算 DV1，前 10 位算 DV2，余数 <2 记 0",
  },
  {
    slug: "finance/cnpj-validator",
    inputs: { input: "11222333000181" },
    expect: ["CNPJ 号码有效"],
    ref: "巴西 CNPJ 模 11 双校验：权重 [5,4,3,2,9,8,7,6,5,4,3,2]，余数 <2 记 0",
  },
  {
    slug: "finance/abn-validator",
    inputs: { input: "51824753556" },
    expect: ["ABN 号码有效"],
    ref: "澳洲 ABN：首位减 1 后加权 [10,1,3,5,7,9,11,13,15,17,19] 求和 mod 89 == 0",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "9780306406157" },
    expect: ["校验通过"],
    ref: "ISBN-13：Σ 前 12 位交替权重 1/3 → 校验位 = (10 - Σ mod 10) mod 10 == 第 13 位",
  },
  {
    slug: "finance/sin-validator",
    inputs: { input: "046454286" },
    expect: ["SIN 号码有效"],
    ref: "加拿大 SIN 使用 Luhn：046454286 加权和 mod 10 == 0",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    expect: ["DNI 有效"],
    ref: "西班牙 DNI：校验字母 = 'TRWAGMYFPDXBNJZSQVHLCKET'[数字 mod 23]，12345678 mod 23 = 5 → Z",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "1234567893" },
    expect: ["NPI 号码有效"],
    ref: "美国 NPI：前缀 80840 拼接后过 Luhn，80840 + 1234567893 加权和 mod 10 == 0",
  },
  {
    slug: "finance/aadhaar-validator",
    inputs: { input: "234123412346" },
    expect: ["Aadhaar 号码有效"],
    ref: "印度 Aadhaar 使用 Verhoeff（十进制非线性和校验），234123412346 校验位正确",
  },
  {
    slug: "finance/tfn-validator",
    inputs: { input: "123456782" },
    expect: ["校验和失败"],
    ref: "澳洲 TFN 反例：权重 [1,4,3,7,5,8,6,9,11]，Σ = 255，255 mod 11 = 2 ≠ 0 → 无效",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "123456789" },
    expect: ["校验和失败"],
    ref: "新西兰 IRD 反例：base = 23456789，权重 [3,2,7,6,5,4,3,2]，Σ = 170 → 期望校验位 6 ≠ 9 → 无效",
  },

  // ── 金融公式类（7 个，期望值由 python 独立复算）────────────────────
  {
    slug: "finance/simple-interest",
    inputs: { principal: "10000", rate: "5", years: "3" },
    expect: ["1,500"],
    ref: "单利：利息 = P×r×t = 10000×5%×3 = 1500（年息 500），终值 11500",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "30" },
    expect: ["4,890.17"],
    ref: "等额本息月供 = P×i×(1+i)^n/((1+i)^n-1)，i = 4.2%/12、n = 360 → 4890.17",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "100000", value: "150000", years: "5" },
    expect: ["8.45%", "50.00%"],
    ref: "ROI = (150000-100000)/100000 = 50%；年化 = (1.5)^(1/5)-1 = 8.45%",
  },
  {
    slug: "finance/calc-3",
    inputs: { initial: "-100000", rate: "8", flows: "30000,30000,30000,30000,30000" },
    expect: ["19,781.30"],
    ref: "NPV = -100000 + Σ 30000/1.08^k (k=1..5) = -100000 + 119781.30 = 19781.30；PI = 1.1978",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { fc: "100000", price: "50", vc: "30" },
    expect: ["20.00"],
    ref: "盈亏平衡：单位边际贡献 = 50-30 = 20；平衡销量 = 100000/20 = 5000 件",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "1000", customRate: "13" },
    expect: ["884.96", "115.04"],
    ref: "含税价倒推：不含税 = 1000/1.13 = 884.96，税额 = 115.04",
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "1234567.89" },
    expect: ["five hundred sixty-seven", "point eight nine"],
    ref: "数字转英文单词：1234567.89 → one million two hundred thirty-four thousand five hundred sixty-seven point eight nine",
  },
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 200));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
