# 盈亏平衡 ROAS 负值被静默忽略

## 问题
当前 ROAS 和目标利润率以逻辑或回退为零，负值没有得到充分验证，可能被忽略并输出正常结论。

## 解决方案
区分空值、合法零值及无效负数，逐项提示并清除旧结果。

## 受影响工具路径
- `tools/marketing/marketing-break-even-roas.html`
