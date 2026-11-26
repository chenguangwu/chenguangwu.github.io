# URL 高级编解码：表单编码字符集与标准不一致

- 受影响工具：`tools/it/url-encoder-advanced.html`
- 问题：表单与 Query 模式使用 `encodeURIComponent` 并只把空格替换为加号，保留 `!'()~`，与标准表单序列化的百分号编码集合不同，可能影响要求字节一致的接口或签名。依据源码及 `URLSearchParams` 对照，待浏览器复核。
- 解决方案：按标准表单规则编码键和值，并与 URI 模式明确区分；验证空格、加号、特殊字符和 Unicode，保留 Query 的分隔结构。
