# JWT 解析：搜索摘要混入控件标签且截断

- 受影响工具：`tools/it/jwt-parser.html`
- 问题：页面当前 `description`、Open Graph 及 Twitter 摘要由“Payload Signature 签名”等控件文本拼接而成，并以省略号截断；WebApplication 结构化数据描述同样混入中英文界面文本，难以说明工具用途、支持的算法及本地处理特点。静态检查所得。
- 解决方案：围绕 JWT 解码、声明查看和 HS256/384/512 本地验签生成完整自然的中英文摘要，并明确解码不等于验签；检查构建来源以及构建后 meta、社交摘要、JSON-LD 和英文态一致性。
