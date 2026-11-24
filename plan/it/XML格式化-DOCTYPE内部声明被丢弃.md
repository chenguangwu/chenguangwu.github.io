# XML 格式化：DOCTYPE 内部子集被丢弃

受影响工具：`tools/it/xml-formatter.html`

问题：序列化 DOCTYPE 仅输出名称及 PUBLIC/SYSTEM 标识，不保留内部子集。浏览器能够解析的带内部声明 XML，例如 `<!DOCTYPE root [<!ELEMENT root EMPTY>]><root/>`，处理后会丢掉元素声明，导致文档约束信息变化；页面没有提示该限制。

解决方案：在不引入外部资源访问的前提下保留完整 DOCTYPE 内部子集，或对不能安全保真的输入拒绝处理并提示，而非静默丢失。验证内部元素、属性和实体声明、外部标识及无 DOCTYPE 输入，并检查浏览器解析兼容性。

证据范围：静态代码分析，具体浏览器对 DTD 的解析能力及结果待验证。
