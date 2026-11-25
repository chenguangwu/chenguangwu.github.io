# URL 解析：合法文本被无效数字守卫拦截

## 问题

解析结果 HTML 生成后，对整段字符串匹配 `Infinity` 和独立的 `NaN` 并显示无效数字错误。输入合法 URL `https://example.com/?value=NaN` 或 `https://example.com/Infinity`，URL 本身解析成功，但其正常文本触发守卫，页面不显示解析结果。这些字符串可能是路径或查询参数，与数值计算无关。

## 解决方案

移除对 URL 结果文本的数值关键字扫描，仅针对真正的数值字段做有限性校验，保留既有 HTML 转义。验证路径、参数、片段含 `NaN`、`Infinity`，以及非法 URL 仍能显示正确错误。

## 受影响工具路径

- `tools/it/url-parser.html`（`parseUrl` 结果输出守卫）
