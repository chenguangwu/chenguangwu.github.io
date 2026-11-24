# 音乐练习计时：自定义阶段名称未转义

- 受影响工具路径：`tools/life/music-practice-timer.html`
- 问题：添加阶段时，`prompt` 返回的名称在 `render()` 中直接拼接到 `innerHTML`。输入含 HTML 标签的名称会被解析为页面元素，事件属性还可能执行脚本；从不可信来源复制名称时存在风险。
- 解决方案：用 `textContent` 创建阶段名称节点，或在拼接前统一进行 HTML 转义；保留普通字符和特殊符号原样展示。验证 `<img src=x onerror=...>` 等输入只显示为文本，阶段计时仍可正常运行。
