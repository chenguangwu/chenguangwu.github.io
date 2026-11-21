# 银行/投资/证券 · tools/{banking,investment,securities}（~110 页）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 已知问题
### B1. 复利/年金公式族重复且口径不一
- 描述：annuity 系多页（pv/fv/due/growing）间互链弱、参数名不统一（r 有百分数/小数混用——growing-annuity 已注明）。
- 受影响：tools/banking/annuity-*、growing-annuity-pv、tools/investment/*（~25 页）
- 方案：统一参数命名与「期初/期末」开关；互相内链成族。

## 功能缺陷
- 定投计算器缺「止盈目标反推年化」。

## 优化点
- S3：投资类全部结果加「时间轴现金流图」（NPV 已有，推广到定投/复利）。
- S7 引据：公式页标「Hull 教材第 9 版 §13.8」式出处。

## 受影响范围
- tools/banking/（25）、tools/investment/（48）、tools/securities/（35）

## 进度
- 🟢 2026-11-21 复核：S7 引据已落地 41 页；年金族互链与 valuation 引据转长期增强，不属缺陷。

## 2026-11-03 续查：贷款、投资与仓位

### 续查覆盖
- 新抽查 `tools/banking/loan-tenure.html`、`tools/banking/loan-remaining-balance.html`、`tools/investment/discounted-payback.html`、`tools/securities/position-sizing.html` 共 4 页；仅 B-N6 待核源码。

## 2026-11-03 续查（并行批 F）

本轮只读抽查 8 页（banking 3 / investment 3 / securities 2），全部以源码阅读 + node 内存复算取证，未做浏览器交互、英文态、移动端、门禁或线上验证。

### 留存优化
- 8 页共用同一套 `num()` / `__tbInputGuard` 模板，分母表由「置零探测」写死（`__D={...}`），建议改为显式规则（`{min,max,allowZero,unit}` 声明），把零值、负数、单位三类问题一次性收口，避免逐页打补丁。
- 单位口径：`tax-equivalent-yield`、`geometric-mean-return`、`sortino-ratio`、`profitability-index` 的公式框宜统一增加「输入单位」一行（% 还是小数），示例中同时给出两种写法。
- 各页导出/历史只存输入与结果摘要，建议附公式口径与单位，便于跨页对比。

### 续查覆盖
- 新抽查 `tools/banking/credit-card-interest-monthly.html`、`tools/banking/debt-to-income.html`、`tools/banking/tax-equivalent-yield.html`、`tools/investment/sortino-ratio.html`、`tools/investment/geometric-mean-return.html`、`tools/investment/profitability-index.html`、`tools/securities/max-drawdown.html`、`tools/securities/margin-requirement.html` 共 8 页；8 页复核未发现新的计算缺陷；B-F1/B-F2 编号在现有台账中已失联（无对应条目），按陈旧引用关闭。


## 2026-11-21 剩余本金零利率

- `banking/loan-remaining-balance` 明细表补零利率分支；无效输入清空表；导出前校验有效行与 NaN/Infinity。
