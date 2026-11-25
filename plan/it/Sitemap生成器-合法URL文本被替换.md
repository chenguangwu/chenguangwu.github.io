# Sitemap 生成器：合法 URL 文本被改写

- 受影响工具：`tools/it/sitemap-generator.html`
- 问题：`escH()` 将任意文本中的 `Infinity` 和 `NaN` 替换为破折号。输入合法地址 `https://example.com/Infinity` 或 `https://example.com/NaN`，展示的 sitemap 地址随之改变，复制结果将指向不同路径。源码分析，待浏览器复核。
- 解决方案：HTML 展示只做必要转义，XML 中按原样保留 URL 并正确转义 XML 特殊字符；分别核对预览与复制结果，覆盖包含上述字符串、`&` 和非 ASCII 路径的 URL。
