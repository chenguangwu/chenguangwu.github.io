# XML 格式化：合法 parsererror 元素被误报

- 受影响工具：`tools/it/xml-formatter.html`
- 问题：美化、压缩和校验使用 `getElementsByTagName('parsererror').length` 判错；合法文档 `<root><parsererror>example</parsererror></root>` 会被误判为 XML 错误。主分支同样存在。
- 解决方案：按浏览器实际解析错误文档的结构和命名空间判断，并在各支持浏览器测试合法同名元素、不同命名空间和真正语法错误。
