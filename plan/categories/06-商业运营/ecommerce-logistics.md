# 电商/物流 · tools/{ecommerce,logistics,logistics2,shipping,express}（~60 页）

## 已知问题
## 功能缺陷
- 快递页缺「多快递公司价格对比」（静态价目表数据源）。
- 体积重页缺「多包裹合计」。

## 优化点
- S2 场景：「女装 500g 发全国选快递」「大促库存天数」。
- S5 回访：库存/利润页历史曲线（已注入部分，推广）。

## 受影响范围
- tools/ecommerce/、tools/logistics/、tools/logistics2/、tools/shipping/、tools/express/

## 进度
- 🔴 待开发

### Z3. procurement/stats-on-time-1「未达标率（非准时且合格）」标签写反（批20）
- 描述：`failRate=(total−both)/total` 是「未同时达标率」（迟到或不良的并集占比），括注「非准时且合格」描述的只是其中一个子集，标签误导。
- 方案：标签改「未同时达标率（迟到或质量不良）」；深度解读同步。
- 受影响：tools/procurement/stats-on-time-1.html
- 置信度：高（集合口径）
