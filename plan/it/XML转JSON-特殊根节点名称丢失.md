# XML 转 JSON 丢失特殊根节点名称

- 受影响工具：`tools/it/xml-to-json.html`
- 问题：根结果使用普通对象并直接赋值 `result[root.tagName]`。合法 XML `<__proto__><x>1</x></__proto__>` 会触发对象原型 setter 而不是生成同名属性，序列化结果丢失整个根节点。源码推断，待浏览器复核。
- 解决方案：根对象使用无原型对象或安全定义自有属性；覆盖 `__proto__`、`constructor`、`toString` 作为根及子元素时的转换结果。
