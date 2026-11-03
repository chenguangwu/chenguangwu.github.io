# 银行/投资/证券 · tools/{banking,investment,securities}（~110 页）

## 已知问题
### B1. 复利/年金公式族重复且口径不一
- 描述：annuity 系多页（pv/fv/due/growing）间互链弱、参数名不统一（r 有百分数/小数混用——growing-annuity 已注明）。
- 受影响：tools/banking/annuity-*、growing-annuity-pv、tools/investment/*（~25 页）
- 方案：统一参数命名与「期初/期末」开关；互相内链成族。

### B3. Black-Scholes/希腊字母页无隐含波动率反解
- 受影响：tools/securities/black-scholes-*、option-greeks
- 方案：加「由市价反解 IV」二分（纯前端可行，竞品标配）。
- ✅ 已落地（2026-10-26）：black-scholes-call / black-scholes-put 加「期权市价（选填）」→ C(σ)/P(σ) 在 σ∈(0,5] 单调，二分 80 次反解 IV + 无解状态行（低于内在价值下界/超 σ=500% 上界）；mkt 空 ⇒ IV 行不渲染零交集。verify 自洽强用例（mkt=正向价 → IV=0.2500）×2。verify securities 71/71、判别器 0 逃生、门禁 218/218。option-greeks 页亦于 2026-10-27 加同款「由市价反解隐含波动率 IV」（marketPrice 输入 + calcIV 二分复用页面 BS 定价，ivBox 输出），自洽用例（spot=100/strike=100/rate=3/vol=20/time=0.5/div=0/mkt=6.371 → IV=20.00%）落 verify_futures_calc.js；verify futures 6/6、判别器 0 逃生、门禁 218/218。

## 功能缺陷
- 定投计算器缺「止盈目标反推年化」。
- ~~久期/凸性页缺「利率敏感度±100bp 结果表」~~ ✅ 已落地（2026-10-26）：`securities/bond-duration` 加 ±25/50/100bp 重定价表（priceAt 完整重算非久期线性近似，跌少涨多即正凸性说明）；该页此前 verify 被跳过，本批补强用例（C6/y4.5/n8 → +100bp 103.17/-6.12%，默认态 92.64/-7.36% 零交集）。verify securities 72/72、判别器 0 逃生、门禁 218/218。

## 优化点
- S3：投资类全部结果加「时间轴现金流图」（NPV 已有，推广到定投/复利）。
- S7 引据：公式页标「Hull 教材第 9 版 §13.8」式出处。

## 受影响范围
- tools/banking/（25）、tools/investment/（48）、tools/securities/（35）

## 进度
- 🔴 待开发（B1 年金族口径统一互链待做；B3 IV 反解全落地；S7 引据 securities 6 + investment 10 + banking 25 已全量落地，余 valuation 待续）

## 2026-11-03 第一轮抽样补充

### IRR 固定二分方向及端点判定失效（高，确认）
- `tools/investment/irr-calc.html:238-250` 固定按 NPV 正时抬高下界；现金流 `1000,-1100,0,0,0` 实际根为 10%，按该函数输出 1000% 且称唯一；`-100,230,-132,0,0` 的 10%、20% 均为根，但端点同号被称区间无根。
- 方案：根据现金流构造并验证根区间、处理相反现金流方向、多根和残差；不能仅凭端点同号断言无根。输入与算例在内存中执行原函数，未做浏览器交互测试。

### 零利率被拒（中，确认）
- `tools/banking/emi-loan.html:249-258,280-287` 将零利率标为非法分母；本金 1200、期限 1 年、0% 的合法极限为月供 100。`tools/banking/loan-tenure.html` 也有相同候选，留待逐页独立核实。
- 方案：零利率用本金/期数分支，保留非零公式；补充本金、利息与末期分解导出，方便用户核对。

### 久期明细的权重命名不准确（中，确认）
- `tools/securities/bond-duration.html:310-328` 将 `PV×期数/价格` 以百分数标为「久期权重」，实为按期数加权的久期贡献，而非现值占价格的权重；其值可大于 100%。
- 方案：分别展示 `PV/价格` 权重和 `期数×权重` 久期贡献，注明期与年的换算；保留已有利率情景表。

### 具体留存优化（建议）
- `tools/investment/npv-calc.html`：允许增删现金流期并导出每期折现值和累计 NPV，以便核对方案；`tools/securities/black-scholes-call.html` 已有市价反解 IV，可增理论价与市价差及输入单位解释。
- 范围：本轮只读抽查 banking、investment、securities 各 2 页，共 6 页；其余未逐页覆盖，未重跑门禁。

## 2026-11-03 续查：贷款、投资与仓位

### B-N1 固定风险仓位未纳入手续费且允许零止损距离（高，确认源码缺陷）
- 证据：`tools/securities/position-sizing.html:454-479,487-504` 先用风险金额除以价差求股数，再把双向手续费加入亏损；资金 100000、风险 2%、买入 10、止损 9、手续费 0.1% 得 2000 股，标示最大亏损 2040，超过 2000 风险预算。止损价等于买价时仍显示「风险金额 ÷ 0 = 0 股」。源码计算和数值推导，未真机测试。
- 影响：`tools/securities/position-sizing.html`；风险预算可能被突破，零止损距离输出伪结果。
- 方案：按止损时买卖费用和价差共同求可买数量，按交易单位向下取整；校验价格、费率、风险比例和方向，区分买入与卖出费用，并提供风险预算与实际最大损失对照。

### B-N2 两贷款页拒绝零利率且附表仍生成无效值（高，确认源码路径）
- 证据：`tools/banking/loan-tenure.html:249-258,280-288,339-354` 和 `tools/banking/loan-remaining-balance.html:255-264,286-294,345-361` 把利率零当非法分母，附加计算却只检查输入是否有限，零利率仍可生成 NaN 表项。前页本金 10000、期供 200，零利率应为 50 期；后页本金 1200、一年、还 6 期时余额应为 600。
- 影响：上述两页；合法贷款被拒，附表/导出可能与错误提示矛盾；同类问题先前已在本文件作为候选登记，此处补证，不另计候选。
- 方案：实现零利率极限分支；主计算、表格、历史和 CSV 共用统一有效状态，失败时清除或禁用导出，测试有效→无效→有效。

### B-N3 贷款已还期数超范围产生负余额（高，确认源码缺陷）
- 证据：`tools/banking/loan-remaining-balance.html:189-194,286-294` 明示 k 不得超过总期数，计算却未校验；本金 1200、年利率 12%、1 年、已还 13 期，算得余额约 -106.62、已还本金约 1306.62。
- 影响：`tools/banking/loan-remaining-balance.html`；超期还款时产生看似有效的错误结果。
- 方案：验证期数为整数且 `0 ≤ k ≤ N`，避免输出负余额；提供逐期本金及结清状态核对。

### B-N4 折现回收期将缺失或非法输入变成投资结论（高，确认源码缺陷）
- 证据：`tools/investment/discounted-payback.html:131-152,230-239` 的 `num` 把空输入转为零，清空期初现金流且其余为 500、500、500 和 10% 时显示 0.00 年；期初 -1000、后续各 500、贴现率 -100% 时折现分母为零，却给出「未回收」。
- 影响：`tools/investment/discounted-payback.html`；用户可能将未完成输入或数学无效结果误判为可回收或不可回收。
- 方案：区分缺失和显式零，要求数值有限、贴现率大于 -100%；展示各期折现现金流与累计值，允许增删期间并导出。其增删及现金流建议与前文留存项合并，不重复计数。

### B-N5 理论期数乘期供不等于实际结清总额（中，确认源码缺陷）
- 证据：`tools/banking/loan-tenure.html:280-287,330-331,339-351` 输出 `PMT×n`，但 FAQ 称末期按剩余本金及利息结清。本金 10000、每期利率 0.005、期供 200 时约 57.6801 期，页面总额约 11536.03；按前 57 期固定期供与最后一期约 136.14 计算，合计约 11536.14（未考虑银行逐期舍入）。
- 影响：`tools/banking/loan-tenure.html`；结果是连续期数近似值，不能无说明地等同实际还款总额。
- 方案：明确理论期数与整数还款期数，按末期结清额计算并同步表格、CSV；说明舍入假设。

### B-N6 仓位历史未保存计算模式（中，确认源码路径）
- 证据：`tools/securities/position-sizing.html:361-386,592-602,629-643,677-680` 历史未记录或恢复 `currentTab`；切换到凯利模式后恢复固定风险记录，按当前模式重算，浏览器回填待测。
- 影响：`tools/securities/position-sizing.html`；历史方案可能无法复现，影响复核。
- 方案：保存并先恢复计算模式，再恢复全部输入和重算；另让 `tools/securities/position-sizing.html` 与 `tools/investment/discounted-payback.html` 导出当前完整输入、结果及明细，而非仅截断的历史摘要（分别见 `:604-610,683-697`、`:262-268,341-355`）。

### 续查覆盖
- 新抽查 `tools/banking/loan-tenure.html`、`tools/banking/loan-remaining-balance.html`、`tools/investment/discounted-payback.html`、`tools/securities/position-sizing.html` 共 4 页，新增 6 条，其中 4 条高优；未进行浏览器、线上或门禁验证。
