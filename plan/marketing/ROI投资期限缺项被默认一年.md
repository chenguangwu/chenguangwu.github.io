# ROI 投资期限缺项被默认一年

## 问题
投资期限用 parseFloat 后回退为 1，空值或零被静默替换，后续正数检查无法发现。

## 解决方案
区分缺失与数值，要求有效正期限并明确提示。

## 受影响工具路径
- `tools/marketing/marketing-roi.html`
