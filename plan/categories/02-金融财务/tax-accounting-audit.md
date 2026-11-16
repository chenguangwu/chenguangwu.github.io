# 税务/会计/审计 · tools/{tax,accounting,audit}（~60 页）

## 2026-11-09 已修交接中未完成的余项

以下为原交接未完成或尚待核实的余项，不代表本次复核确认当前代码仍存在：
- `tools/audit/npv-discount.html`：导出按钮参数非法时禁用的前置钩子、带输入与结果的本地历史面板、恢复防脏的 60 期上限在按钮侧的校验尚待处理或核实。
- 境外税收抵免及现金转换周期运行时明细表行标签的英文翻译问题仍待处理或核实。

## 已知问题
### T1. 税率表时效性
- 描述：个税/增值税等速算扣除数为建站时快照，无「版本日期」标注——税制调整后风险高。
- 受影响：tools/tax/*（35 页税率类）
- 方案：每页头部加「口径截至 2026-XX」徽标 + 数据集中到 json 单源（改一处全站生效）。

## 功能缺陷
- 个税缺专项附加扣除模拟（7 项勾选输入）——搜索需求极大。
- 企业所得税缺小型微利优惠开关。

## 优化点
- S2 场景：「北京月薪 2 万有房有娃」「年终奖 10 万怎么发」。
- S3 分步：速算扣除数「为什么是这个数」展开。

## 受影响范围
- tools/tax/（35）、tools/accounting/（35）、tools/audit/

## 进度
- 🔴 待开发：json 单源待裁；其余分类待办见各计划文件。

## 2026-11-03 第一轮抽样补充

### 审计可信度超出因子表时静默回退（中，确认）
- `tools/audit/audit-sample.html:278-291,314-336` 对低于 80% 的输入回退至 `R=3.0`（95% 对应值），但结果仍标用户输入可信度；如 79%、可容忍 5%、预期 1% 得 75 样本。
- 方案：限制支持区间或明确提示使用的近似/回退口径，不将估算写为无条件的统计保证；测试 79%、80%、99% 及越界。

### 留存优化（建议）
- `tools/tax/vat-inclusive-to-exclusive.html` 输出含税=不含税+税额的可复制分解及舍入规则；`tools/audit/depreciation-compare.html` 保留既有逐年对比，补方法切换节点与累计折旧差异说明。
- 范围：本轮只读抽查 tax、accounting、audit 各 2 页，共 6 页；其余未逐页覆盖，未做浏览器或门禁验证。

## 2026-11-03 续查：抵免、折旧、现金周期与净现值

### 续查覆盖
- 新抽查 `tools/tax/foreign-tax-credit.html`、`tools/accounting/depreciation-declining.html`、`tools/accounting/cash-conversion-cycle.html`、`tools/audit/npv-discount.html` 4 页；T-N1～T-N8 均已修复并回归。

## 2026-11-03 续查（并行批 G）

### 留存优化
- `tools/audit/irr-table.html`：扫描循环已加 2000 行上限（超出截止并提示增大步长，2026-11-16）；「按整数索引生成利率、过零点直接标注 IRR 区间」仍可继续优化。
- `tools/audit/ratio-analysis.html`：结果卡与复制报告各算一套（`:292-305` vs `:359-367`），建议抽一个 `compute()` 返回对象，UI/复制/导出/历史全部复用；空值统一显示 N/A。
- `tools/accounting/amortization-intangible.html`、`tools/accounting/depreciation-syd.html`：两页各有一份 `__tbInputGuard`，但校验项不同（前者无负值表、后者有 `n` 负值表但无 `yr` 范围）；建议统一为同一份守卫配置（必填、非负、分母非 0、上下界），失败时禁用导出。
- `tools/tax/payroll-tax.html`、`tools/tax/capital-gains-effective.html`、`tools/tax/stamp-duty.html`：税率输入单位不统一（前两页为小数、印花税页为百分数），且三页都带无业务含义的「税率倒数」卡片；建议统一标签与口径、删除倒数卡，并把「📅 税率口径截至 2026-10」徽标与校验说明合并到同一段。
- `tools/accounting/debt-service-coverage.html`：`1/max(x,1e-9)` 的夹值写法在本批 4 页出现，建议封装为 `safeReciprocal()`，对非正输入返回 N/A，避免各页各自伪造极小值。

### 续查覆盖
- 本批新抽查 8 页：`tools/audit/irr-table.html`、`tools/audit/ratio-analysis.html`、`tools/accounting/amortization-intangible.html`、`tools/accounting/depreciation-syd.html`、`tools/accounting/debt-service-coverage.html`、`tools/tax/capital-gains-effective.html`、`tools/tax/payroll-tax.html`、`tools/tax/stamp-duty.html`；与既有 T1、首轮 6 页、T-N1～T-N8 无重复。
- 新增 11 条（T-N9～T-N19），其中高优 2 条（T-N9、T-N15）、中优 8 条、低优 1 条；除 T-N19 标注「待验证」外均为源码路径 + node 内存复算确认。
- 证据均来自源码阅读与 node 复算；**未做**浏览器、英文态、移动端、线上或门禁验证；历史/持久化的实际行为未在真机复核。
