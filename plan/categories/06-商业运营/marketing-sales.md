# 营销/销售 · tools/{marketing,advertising,sales}（~70 页）

## 已知问题

## 功能缺陷
- ROI 页缺「多渠道对比表」（同预算分三渠道敏感性）。
- 广告缺「A/B 测试显著性判定」（样本量+转化率→p 值，纯前端可算）。

## 优化点
- S2 场景：「抖音千川 ROAS 测算」「私域 SOP 转化漏斗」。
- S3 分步：盈亏平衡点图解。

## 受影响范围
- tools/marketing/（46）、tools/advertising/、tools/sales/

## 进度
- 🔴 待开发

### Z2. sales/cost-price-margin「利润率」与「加价率」输出同值（批20）
- 描述：输入口径为成本加成（售价=成本×(1+margin)），输出把「利润率」与「加价率」显示为同一个 margin%。加价率=利润/成本 ✓，但利润率=利润/售价=margin/(1+margin)，两者不等（margin=30% 时利润率应 23.1% 非 30%）。
- 方案：利润率改为 `(p-cost)/p` 输出，或把该行标签改为「成本利润率」；公式框同步。
- 受影响：tools/sales/cost-price-margin.html
- 置信度：高（口径定义）
