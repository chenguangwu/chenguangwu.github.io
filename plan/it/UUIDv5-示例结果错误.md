# UUID v5 示例结果错误

- 受影响工具：`tools/it/uuid-v5-generator.html`
- 问题：使用说明称 DNS 命名空间与 `example.com` 生成的 UUID 以 `aad6f...` 开头；用 Python 标准库 `uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")` 核对，结果为 `cfbff0d1-9375-5685-968c-48ce8b15ae17`。错误示例容易让用户误以为工具或其他实现不兼容。
- 解决方案：将示例改为准确完整的 UUID，并以标准库或独立实现核对命名空间与输入字节；同步检查中英文对应说明。
