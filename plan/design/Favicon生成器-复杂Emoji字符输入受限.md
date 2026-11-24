# Favicon 生成器：复杂 Emoji 输入受字符数限制

- 受影响工具：`tools/design/favicon-generator.html`
- 问题：页面支持 Emoji，但文本框 `maxlength="2"` 按 UTF-16 码元限制，许多带肤色、组合连接符的单个 Emoji 超过两个码元，无法完整输入；普通两个非 BMP Emoji 也超过限制。实际输入法表现需浏览器复核。
- 解决方案：按用户可见字符簇限制数量而不是码元，保证组合 Emoji 和中英文均可输入；检测超出画布的文字并提供尺寸调整或适配提示。
