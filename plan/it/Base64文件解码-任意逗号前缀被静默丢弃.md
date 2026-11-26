# Base64 文件解码静默丢弃任意逗号前缀

- 受影响工具：`tools/it/base64-file.html`
- 问题：文件还原和文本解码按第一个逗号拆分输入，不检查前缀是否为合法的 Base64 data URI。例如 `wrong,SGVsbG8=` 会忽略 `wrong,` 并成功输出 `Hello`，将错误输入当作成功结果；非 Base64 的 data URI 也可能被误处理。源码已核实，待浏览器复核。
- 解决方案：只在完整识别合法的 `data:...;base64,` 头时去除前缀，普通 Base64 应整体校验；拒绝格式错误或非 Base64 data URI 并说明原因。覆盖带参数的合法头、纯 Base64、任意逗号及非 Base64 data URI 的文件与文本解码。
