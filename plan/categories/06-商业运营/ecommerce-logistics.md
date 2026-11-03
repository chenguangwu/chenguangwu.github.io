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

## 2026-11-03 第一轮抽样补充

### 负成本被接受并虚增利润（中，确认函数缺陷）
- 问题与证据：`tools/ecommerce/stats-profit.html:125-133,214-229` 输入框成本 min=0，计算函数只校验销售额；销售额 1000、成本 −200、费用税费 0 时原函数显示净利 1200、净利率 120%。
- 影响：`tools/ecommerce/stats-profit.html`，不符合页面成本约束的数据生成可复制利润。
- 方案：计算时校验各项非负；退款或冲销如需支持，独立命名并明确语义。可提供费用拆分与本地方案对比。

### 抛比为零被替换成 1（高，确认函数缺陷）
- 问题与证据：`tools/logistics/package-volume-calc.html:123-137,242-254` 因 `parseFloat(...)||1`，40×30×20 cm、抛比 0 时原函数显示材积重 24000 kg，而非拒绝无效分母。
- 影响：`tools/logistics/package-volume-calc.html`，可能误导运费测算。
- 方案：尺寸和抛比要求有限正数；零或空时停止计算并提示。接续原多包裹合计建议，可比较用户输入的多个抛比，不假设在线报价。

### 覆盖
- 本次抽查上述 2 页，原函数内存 DOM 桩执行，未验证真实浏览器、线上及其余电商物流工具。

