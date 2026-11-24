# GSTIN 验证：两个工具的州码规则不一致

- **受影响工具路径**：`tools/finance/gst-validator.html`、`tools/finance/gstin-validator.html`
- **问题**：两页都校验 GSTIN，但 `gst-validator` 将 25、28 标为停用并拒绝，`gstin-validator` 仍将其列为有效州码；相同号码可能得到相反结论，26 的名称也不一致。
- **解决方案**：以权威资料核实现行及历史号码的适用状态，统一离线规则、来源和版本；对历史代码区分历史格式与当前登记，避免未经查询就断定号码状态，覆盖两页面相同输入。
