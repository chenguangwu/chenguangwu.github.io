# User-Agent 解析遗漏安卓 Edge

## 问题

浏览器识别包含桌面 `Edg/` 和 iOS `EdgiOS/`，缺少 Android Edge 的 `EdgA/`。其 UA 通常同时包含 `Chrome/`，因此会被识别成 Chrome。

## 解决方案

在 Chrome 判断前识别 `EdgA/` 并提取版本；使用 Android、iOS、桌面 Edge 和普通 Chrome 样本验证浏览器名称与版本。

## 受影响工具路径

- `tools/it/user-agent-parser.html`
