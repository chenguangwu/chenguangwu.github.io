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
