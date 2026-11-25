# Unicode 码点解析接受非法输入并可能抛错

## 问题
十六进制解析接受尾随非法字符，超过 Unicode 上限会抛 RangeError，代理区码点也可能当作有效 UTF-8 编码。

## 解决方案
严格校验完整格式和 Unicode 标量范围，捕获并提示非法输入。

## 受影响工具路径
- `tools/encode/convert-4.html`
