# XML 校验：合法同名节点被误判解析错误

## 问题
错误检测遍历所有 `parsererror` 节点，只要其命名空间命中 Firefox 的错误命名空间，就判定整个文档解析失败；XHTML 根节点下的同命名空间普通同名子节点也会被判错。例如合法 XML `<root><parsererror xmlns="http://www.mozilla.org/newlayout/xml/parsererror.xml">ok</parsererror></root>` 会触发该分支，与代码注释允许用户自定义同名子元素的意图不一致。

## 解决方案
结合各浏览器实际生成的错误文档结构识别解析失败，不因普通子节点的名称及命名空间单独判错；用 Chrome、Firefox、Safari 验证合法同名节点和真实语法错误。

## 受影响的工具路径
- `tools/it/xml-validator.html`
