# 代码运行器：JavaScript 包含结束脚本标签导致代码截断

## 问题描述

在 JavaScript 编辑框输入 `console.log("</script>")` 并运行，工具把源码直接拼入 iframe 的内联 `<script>`。HTML 解析器会将字符串中的 `</script>` 当作脚本元素结束标签，造成 JavaScript 截断及语法错误，无法执行原本合法的代码。CSS 中的 `</style>` 也可能提前结束样式元素。

## 解决方案

通过 DOM 或安全编码方式为预览文档注入源码，避免原始输入被 HTML 标签解析提前截断，同时保留隔离沙箱与控制台捕获。验证 JS 字符串和注释内的 `</script>`、CSS 字符串内的 `</style>`，以及正常 HTML/CSS/JS 组合运行。

## 受影响工具路径

- `tools/it/code-runner.html`：`executeInIframe()` 组装 `srcdoc`。
