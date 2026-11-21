# 第 150 批：Attention/K-Means 滑杆联动（AI）

- 日期：2026-11-21
- 页面：`tools/ai/attention-flops.html`、`tools/ai/k-means.html`

## 原问题

A2：Attention 与 K-Means 演示页只有数字输入，缺少滑杆式即时联动，交互偏静态。

## 修复

- `attention-flops` 新增序列长度滑杆（128–8192，步长 128），拖动同步数字输入并即时重算单层 FLOPs。
- `k-means` 新增聚类数滑杆（1–20）与簇内散布滑杆（0.1–10，步长 0.1），拖动即时更新 Inertia、每簇样本数、Davies-Bouldin 估算。
- 数字输入继续保持可键入，滑杆只作为快捷联动，不改变原有计算口径。

## 验证

- `node scripts/verify_ai_calc.js ai/attention-flops ai/k-means`：4/4 通过。
- 默认值未变，原有 FLOPs/Inertia/每簇样本/DBI 结果不受影响。
- 构建 4,426 页成功；内联脚本 0 错误；静态检查 4,705 通过 / 0 失败 / 0 警告。
