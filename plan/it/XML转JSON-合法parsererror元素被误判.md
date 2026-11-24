# XML 转 JSON 误判合法 parsererror 元素

- 受影响工具：`tools/it/xml-to-json.html`
- 问题：转换直接以文档中是否存在 `parsererror` 元素判断解析失败，因此合法的 `<root><parsererror>example</parsererror></root>` 也被拒绝。源码推断，待浏览器复核。
- 解决方案：按浏览器解析错误文档的根节点、命名空间及结构判断失败，并复用项目内 XML 校验器已有的跨浏览器判定；验证合法同名根节点、子节点以及真正格式错误。
