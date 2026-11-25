# 文本打乱与填充拆散 Unicode 字符

## 问题
打乱按 UTF-16 码元切分，填充只取首个码元；emoji 等字符可能被拆散并显示乱码。

## 解决方案
按用户可见字符簇处理并提供兼容回退；字节模式说明无法恰好填满时的规则。

## 受影响工具路径
- `tools/biz/text-shuffle.html`
- `tools/biz/text-pad.html`
