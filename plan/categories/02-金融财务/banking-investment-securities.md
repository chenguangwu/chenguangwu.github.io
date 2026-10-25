# 银行/投资/证券 · tools/{banking,investment,securities}（~110 页）

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
- 久期/凸性页缺「利率敏感度±100bp 结果表」。

## 优化点
- S3：投资类全部结果加「时间轴现金流图」（NPV 已有，推广到定投/复利）。
- S7 引据：公式页标「Hull 教材第 9 版 §13.8」式出处。

## 受影响范围
- tools/banking/（25）、tools/investment/（48）、tools/securities/（35）

## 进度
- 🔴 待开发（B2 部分完成）
