# 阀门检测：PN 压力示例单位错误

- 受影响工具路径：`tools/machinery/detector-pressure-torque.html`
- 问题：FAQ 将 16 MPa 举例为 PN16；PN16 的公称压力数值对应 1.6 MPa，16 MPa 对应 PN160。页面还使用固定检测阈值，易被误解为通用标准。
- 解决方案：修正示例单位和等级，将固定值明确标为演示，按阀门设计标准、介质和试验条件配置实际限值。
