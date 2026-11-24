# AST 查看器无法序列化 BigInt 节点

- 受影响工具：`tools/it/ast-viewer.html`
- 问题：Acorn 解析如 `const n = 1n` 的代码后，AST 包含 BigInt 值；JSON 视图与复制功能直接使用 `JSON.stringify`，失败时回退为 `[object Object]`，用户无法获取结构化结果。源码推断，待浏览器复核树视图及解析状态。
- 解决方案：为 BigInt 提供明确、无精度丢失的 JSON 表示并说明类型标记，视图和复制使用同一序列化逻辑；测试正负大整数、普通数字和嵌套节点。
