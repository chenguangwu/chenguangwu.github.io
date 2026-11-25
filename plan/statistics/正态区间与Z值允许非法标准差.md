# 正态区间与 Z 值允许非法标准差

## 问题
区间概率未限制标准差大于零或下界不大于上界，可能输出负概率；Z 值工具也允许负标准差，反转结果。

## 解决方案
验证标准差及区间顺序，输入无效时清除旧结果并提示。

## 受影响工具路径
- `tools/statistics/statistics.html`
- `tools/statistics/z.html`
