# 血常规查询：RDW-CV 百分号单位被误判

- 受影响工具：`tools/clinical-lab/blood-routine-reference.html`
- 问题：批量识别中 `__brKindOf` 将 RDW-CV 识别为 `rdw-cv`，百分号处理却只接受 `rdw`；因此 `RDW-CV 13 %` 会被标记为单位不匹配，而无单位的同一数值可以判读。
- 方案：统一指标标识，按各指标支持的单位转换和校验；覆盖 RDW-CV 带百分号、不带单位及错误单位的输入，并核验其他指标别名。
