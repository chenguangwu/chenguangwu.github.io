# XML 转换工具：合法非 ASCII 标签被拒绝

- 受影响工具：`tools/it/xml-to-json.html`、`tools/it/xml-to-toml.html`、`tools/it/xml-to-yaml.html`
- 问题：格式预检只允许 ASCII 字母和下划线作为标签开头，合法的 `<根><名字>张三</名字></根>` 会被判为 XML 错误。依据源码推导，待浏览器复核。
- 解决方案：采用浏览器 XML 解析器及可靠的解析错误检测，保留安全限制并覆盖中文、其他 Unicode 名称、命名空间及非法 XML；排查其他复用该预检的工具。
