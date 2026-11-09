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
- 新抽查 `tools/banking/loan-tenure.html`、`tools/banking/loan-remaining-balance.html`、`tools/investment/discounted-payback.html`、`tools/securities/position-sizing.html` 共 4 页。B-N1（零止损距离/手续费）、B-N2（两贷款页零利率）、B-N3（已还超期负余额）、B-N4（折现回收期缺失/非法输入）、B-N5（理论期数≠实际结清）均已代码修复并移交 plan/已修复/，本清单不再保留；仅 B-N6 待核源码。

## 2026-11-03 续查（并行批 F）

本轮只读抽查 8 页（banking 3 / investment 3 / securities 2），全部以源码阅读 + node 内存复算取证，未做浏览器交互、英文态、移动端、门禁或线上验证。

### B-F1 信用卡月利息页把「零欠款」判成非法分母（中，确认仍开放）
- 描述：`__tbInputGuard` 的零值分母表把欠款余额 `bal` 登记为分母（`tools/banking/credit-card-interest-monthly.html:249-260`），bal=0 时直接报「「欠款余额 (元)」是本计算的分母，不能为 0」。但主公式 `I=bal×dr×days`（`:280-287`）中 bal 只是乘数，0 欠款是合法输入（利息应为 0）；只有联动指标「期间利率 = I/bal×100」在 bal=0 时无定义。
- 证据：`tools/banking/credit-card-interest-monthly.html:249-260,280-287`；复现输入 bal=0、dr=0.0005、days=30 → 主公式 I=0，`I/bal` 得 NaN，页面在 `:281` 提前中止并显示分母错误；同页默认 1000/0.0005/30 → 15.00 元、期间利率 1.5000%、年化 18.2500%。
- 影响：真正该输出「0 元利息」的场景被拒绝，提示文案与数学事实不符；反向地 dr、days 取负值（`:283`）未被拦截，会输出负利息。
- 方案：bal=0 走零余额分支（利息 0、期间利率显示「—」），分母表只保留真实分母；给 dr、days 加 `>0` 校验。

### B-F2 债务收入比页无债务时「收入债务倍数」等于月收入数值（中，确认仍开放）
- 描述：`收入债务倍数 = 月收入 ÷ max(月债务支出, 1)`（`tools/banking/debt-to-income.html:283`，公式框 `:120` 亦写「分母 0 按 1 兜底」）。月债务为 0 时该指标退化成收入本身，语义完全失真。
- 证据：`tools/banking/debt-to-income.html:276-286`；复现 debt=0、inc=10000 → DTI 0.0%、剩余可支配收入 10000.00 元，但「收入债务倍数」= 10000.000（按定义应为「无债务/不可定义」）。
- 影响：无负债用户会看到「1 万倍」的荒谬指标，误以为是杠杆倍数；负数债务或负数收入同样可写入并产出负 DTI。
- 方案：debt<=0 时该行显示「—（无债务）」而非数字，删除 `max(...,1)` 兜底；对 debt、inc 加非负校验（inc>0）。

### 留存优化
- 8 页共用同一套 `num()` / `__tbInputGuard` 模板，分母表由「置零探测」写死（`__D={...}`），建议改为显式规则（`{min,max,allowZero,unit}` 声明），把零值、负数、单位三类问题一次性收口，避免逐页打补丁。
- 单位口径：`tax-equivalent-yield`、`geometric-mean-return`、`sortino-ratio`、`profitability-index` 的公式框宜统一增加「输入单位」一行（% 还是小数），示例中同时给出两种写法。
- `geometric-mean-return.html:175,418` 的算例「0.1,0.2,−0.05 → 7.83%」与 node 实算 7.84% 差 0.01pp，建议改为 7.84%（保留两位）。
- 各页导出/历史只存输入与结果摘要，建议附公式口径与单位，便于跨页对比。

### 续查覆盖
- 新抽查 `tools/banking/credit-card-interest-monthly.html`、`tools/banking/debt-to-income.html`、`tools/banking/tax-equivalent-yield.html`、`tools/investment/sortino-ratio.html`、`tools/investment/geometric-mean-return.html`、`tools/investment/profitability-index.html`、`tools/securities/max-drawdown.html`、`tools/securities/margin-requirement.html` 共 8 页。B-F3（税后等效收益率单位）、B-F4（索提诺零超额收益倍数）、B-F5（几何平均百分数口径）、B-F6（盈利指数 CF₀ 符号）、B-F8（最大回撤谷值越界）、B-F9（保证金权益为零/超额）、B-F10（索提诺重复历史）均已代码修复并移交 plan/已修复/，本清单不再保留；仅 B-F1、B-F2 仍开放待处理。
