# RLC 输入无效仍写入附加结果和历史

## 问题

主计算拒绝电感、电容或电阻等不合法参数，但后续附加计算仍运行；例如电感或电阻为零时主结果提示错误，附加表仍出现 Infinity 并存入历史。

## 解决方案

让主计算返回有效状态，仅在成功时生成附加结果与历史；无效时清空或明确标记旧结果并禁止导出。

## 受影响工具路径

- `tools/electrical/rlc-resonance.html`
- `tools/electrical/rc-filter.html`
