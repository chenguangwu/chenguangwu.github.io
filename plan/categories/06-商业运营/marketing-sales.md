# 营销/销售 · tools/{marketing,advertising,sales}（~70 页）

## 已知问题

## 功能缺陷
- ROI 页缺「多渠道对比表」（同预算分三渠道敏感性）。
- 广告缺「A/B 测试显著性判定」（样本量+转化率→p 值，纯前端可算）。

## 优化点
- ✅ S2 场景（2026-10-26）：ad-roi 加「抖音千川」预设按钮（CPM 模式 预算1万/CPM45/CTR1.8%/CVR4%/客单260/毛利45% ⇒ ROAS 4.16 / ROI 26.5%）；funnel-calculator 加「私域 SOP」模板（进群2万→加微1200→首单180→复购45）。verify marketing 117→118、判别器 0 逃生、Playwright 真机 zh 正常 + EN 零 CJK、门禁 218/218。
- S3 分步：盈亏平衡点图解。

## 受影响范围
- tools/marketing/（46）、tools/advertising/、tools/sales/

## 进度
- 🟡 续批中（S2 已落地；剩余：多渠道对比表 / A-B 显著性缺口确认 / S3 盈亏平衡图解）

## 2026-11-03 第一轮抽样补充

### 零贬损者时比值被算成有限数（中，确认函数缺陷）
- 问题与证据：`tools/marketing/marketing-nps-calculator.html:199-210,470-471` 推荐者 10、贬损者 0 时，`p/(d||1)` 输出比值 10.00；原函数在内存 DOM 桩复现。NPS 主值仍为 100。
- 影响：`tools/marketing/marketing-nps-calculator.html`，无法表达无贬损者的比值被误写成普通数值。
- 方案：零分母显示不适用或无贬损者，人数按非负整数校验。

### 漏斗零基数仍输出转化率（中，确认函数缺陷）
- 问题与证据：`tools/sales/conversion-funnel.html:272-298` 前一阶段为 0、后一阶段为 100 时以 `||1` 作为分母，原函数显示环节转化率 10000%、整体转化率 0%。
- 影响：`tools/sales/conversion-funnel.html`，不可计算的比例被当有效结果。
- 方案：零基数显示不可计算，后一阶段人数超过前序时提示；可允许用户主动保存、清除各期具名阶段快照，比较环节变化。

### 覆盖
- 本次抽查上述 2 页，原函数内存 DOM 桩，未实测浏览器、线上和其余营销销售页面。

