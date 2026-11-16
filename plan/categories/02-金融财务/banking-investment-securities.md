# 银行/投资/证券 · tools/{banking,investment,securities}（~110 页）

## 2026-11-09 已修交接中未完成的余项

以下为原交接未完成或尚待核实的余项，不代表本次复核确认当前代码仍存在：
- `tools/banking/loan-remaining-balance.html` 与 `tools/banking/loan-tenure.html` 的数据表 / CSV 各自复算，失败态导出未禁用。
- `tools/investment/discounted-payback.html` 仍为固定 4 期，「允许增删期间」未实现。
- `tools/banking/loan-tenure.html` 的敏感性扫描图按连续期数绘制，属于趋势示意。
- 其他页面的同类历史对比模板尚待统一口径与全量门禁，本次未逐页复核。

## 已知问题
### B1. 复利/年金公式族重复且口径不一
- 描述：annuity 系多页（pv/fv/due/growing）间互链弱、参数名不统一（r 有百分数/小数混用——growing-annuity 已注明）。
- 受影响：tools/banking/annuity-*、growing-annuity-pv、tools/investment/*（~25 页）
- 方案：统一参数命名与「期初/期末」开关；互相内链成族。

### B3. Black-Scholes/希腊字母页无隐含波动率反解
- 受影响：tools/securities/black-scholes-*、option-greeks
- 方案：加「由市价反解 IV」二分（纯前端可行，竞品标配）。

## 功能缺陷
- 定投计算器缺「止盈目标反推年化」。

## 优化点
- S3：投资类全部结果加「时间轴现金流图」（NPV 已有，推广到定投/复利）。
- S7 引据：公式页标「Hull 教材第 9 版 §13.8」式出处。

## 受影响范围
- tools/banking/（25）、tools/investment/（48）、tools/securities/（35）

## 进度
- 🔴 待开发（B1 年金族口径统一互链待做；B3 IV 反解全落地；S7 引据 securities 6 + investment 10 + banking 25 已全量落地，余 valuation 待续）

## 2026-11-03 第一轮抽样补充

### 零利率被拒（中，部分仍开放）
- `tools/banking/emi-loan.html` 仍把零利率标为非法分母（主计算 `emi = P·r·(1+r)^N/((1+r)^N−1)` 在 r=0 时 0/0=NaN；`__tbInputGuard` 的零分母表亦拒绝 r=0）。`tools/banking/loan-tenure.html` 已落地零利率分支（n = P/PMT）。
- 方案：emi-loan 加 `r>0 ? 公式 : P/N` 分支；注意门禁 harness 的零分母守卫会拦截 r=0，验证口径需另寻或调整守卫，暂搁置。

### 久期明细的权重命名不准确（中，待核源码）
- `tools/securities/bond-duration.html:310-328` 将 `PV×期数/价格` 以百分数标为「久期权重」，实为按期数加权的久期贡献，而非现值占价格的权重；其值可大于 100%。
- 方案：分别展示 `PV/价格` 权重和 `期数×权重` 久期贡献，注明期与年的换算；保留已有利率情景表。

## 2026-11-03 续查：贷款、投资与仓位

### B-N6 仓位历史未保存计算模式（中，待核源码路径）
- 证据：`tools/securities/position-sizing.html:361-386,592-602,629-643,677-680` 历史未记录或恢复 `currentTab`；切换到凯利模式后恢复固定风险记录，按当前模式重算，浏览器回填待测。
- 影响：`tools/securities/position-sizing.html`；历史方案可能无法复现，影响复核。
- 方案：保存并先恢复计算模式，再恢复全部输入和重算；另让 `tools/securities/position-sizing.html` 与 `tools/investment/discounted-payback.html` 导出当前完整输入、结果及明细，而非仅截断的历史摘要（分别见 `:604-610,683-697`、`:262-268,341-355`）。

### 续查覆盖
- 新抽查 `tools/banking/loan-tenure.html`、`tools/banking/loan-remaining-balance.html`、`tools/investment/discounted-payback.html`、`tools/securities/position-sizing.html` 共 4 页；仅 B-N6 待核源码。

## 2026-11-03 续查（并行批 F）

本轮只读抽查 8 页（banking 3 / investment 3 / securities 2），全部以源码阅读 + node 内存复算取证，未做浏览器交互、英文态、移动端、门禁或线上验证。

### 留存优化
- 8 页共用同一套 `num()` / `__tbInputGuard` 模板，分母表由「置零探测」写死（`__D={...}`），建议改为显式规则（`{min,max,allowZero,unit}` 声明），把零值、负数、单位三类问题一次性收口，避免逐页打补丁。
- 单位口径：`tax-equivalent-yield`、`geometric-mean-return`、`sortino-ratio`、`profitability-index` 的公式框宜统一增加「输入单位」一行（% 还是小数），示例中同时给出两种写法。
- `geometric-mean-return.html:175,418` 的算例「0.1,0.2,−0.05 → 7.83%」与 node 实算 7.84% 差 0.01pp，建议改为 7.84%（保留两位）。
- 各页导出/历史只存输入与结果摘要，建议附公式口径与单位，便于跨页对比。

### 续查覆盖
- 新抽查 `tools/banking/credit-card-interest-monthly.html`、`tools/banking/debt-to-income.html`、`tools/banking/tax-equivalent-yield.html`、`tools/investment/sortino-ratio.html`、`tools/investment/geometric-mean-return.html`、`tools/investment/profitability-index.html`、`tools/securities/max-drawdown.html`、`tools/securities/margin-requirement.html` 共 8 页；仅 B-F1、B-F2 仍开放待处理。
