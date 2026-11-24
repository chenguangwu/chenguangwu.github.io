# URL 编解码：解码未区分 URI 与组件模式

受影响工具：`tools/it/url-encode.html`（首页编辑精选）

页面提供 `encodeURI` 和 `encodeURIComponent` 模式，公式说明对应使用 `decodeURI` 和 `decodeURIComponent`；但 `decodeUrl()` 无论所选模式均使用 `decodeURIComponent`。例如 URI 模式处理 `https://example.com/a%2Fb%3Fc` 时输出 `https://example.com/a/b?c`，把路径内编码的斜杠和问号变成结构分隔符；`decodeURI` 会保留这些编码。

解决方案：按所选模式明确调用对应解码规则，并说明保留字符的行为；处理非法百分号序列时清空或标记旧结果。验证两种模式的保留字符、UTF-8、多层编码、完整 URL 与组件往返，核对中英文说明及复制结果。
