# Favicon 生成器：复制 Data URL 缺少失败处理

受影响工具：`tools/design/favicon-generator.html`

## 问题描述
`copyDataURL()` 直接调用 `navigator.clipboard.writeText()`，未检测接口是否存在，也未处理 Promise 拒绝。在不支持该接口或权限被拒绝时，复制会失败且用户未收到清晰提示。

## 解决方案
检测剪贴板能力，捕获同步和异步失败，并提供安全的备用复制或手动复制方式；验证成功、接口缺失及权限拒绝。
