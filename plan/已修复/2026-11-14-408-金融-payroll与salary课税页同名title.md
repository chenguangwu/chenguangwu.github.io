# 2026-11-14-408 金融 · payroll 与 salary 税后页同名 title

## 发现
`tools/finance/salary-after-tax.html` 与 `tools/finance/payroll-calculator.html` 的 `<title>` 完全相同：
「工资税后计算器 - 免费在线金融财务工具」。两页内容不同（后者含年终奖、月度/年度双口径），
同名会导致搜索结果互相稀释、用户无法区分。

## 修复
将后者显示名改为「工资个税与年终奖计算器」（英文 `Payroll & Year-End Bonus Tax Calculator`），
覆盖中文名、英文名、面包屑、深度解析标题与英文 `map` 键：

- 页面 `tools/finance/payroll-calculator.html`：`<h1>`、面包屑 `/ …` 与 `bc-current`、`<h2 data-zh>`、
  「📚 深度解析：…」、「关于「…」」、intro 段落（顺手修掉「工资税后计算器。工资税后计算器。」重复）、
  keywords / JSON-LD `name`、英文预渲染 h2 与副标题。
- `i18n/tools/finance.json` → `payroll-calculator.zh-CN` 的 h1/title/intro/desc 与 `en-US` 三项。
- `i18n/tools/en/finance/payroll-calculator.json`：`name` 及 4 个含旧名的 `map` 键（标题、深度解析、关于、整段 intro）。
- `i18n/tools/finance-body.json`：英文 title/h1/intro。
- `i18n/tools/_en_override.json`、`i18n/tools/slug-en.json`、`i18n/tools/finance-phrases.json`、`scripts/enmap/finance.json`：同步英文名与新键。
- `i18n/tools/content_deepdive.json` → `finance/payroll-calculator.title`。
- `json/tools.json` / `json/industry-finance.json` 由构建从页面 h1 + 英文 h2 自动重算，无需手改。

## 验证
- [x] `python3 _build.py` 连跑 2 次，退出 0
- [x] 两页 title 不再相同：
      salary-after-tax =「工资税后计算器 - 免费在线金融财务工具」，
      payroll-calculator =「工资个税与年终奖计算器 - 五险一金基数与年终奖」
- [x] og:title / twitter:title / JSON-LD `name` / 面包屑 / h1 全部为新名
- [x] 英文态 `<h2 data-zh="🧾 工资个税与年终奖计算器">🧾 Payroll &amp; Year-End Bonus Tax Calculator</h2>`，无中文回退
- [x] `tools.json` 与 `industry-finance.json` 中该页 name / desc / en 三端一致
- [x] 页面内旧名残留 0（`json/tools.json` 仅剩 salary-after-tax 自身条目）
- [x] `_test_static.py`：4714 / 4714 通过，0 失败 0 告警
