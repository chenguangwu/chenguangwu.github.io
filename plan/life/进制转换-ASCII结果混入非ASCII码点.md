# 进制转换：ASCII 结果混入非 ASCII 码点

- 受影响工具：`tools/life/base-convert.html`

## 问题

文本转换把每个 Unicode 码点直接填入标为 ASCII 的结果；例如中文或表情会得到大于 127 的数字，但这些字符不属于 ASCII。用户可能误认为该数字是有效 ASCII 编码。

## 解决方案

对 ASCII 范围外字符标记“不支持”或单独显示对应 Unicode 码点；若提供 UTF-8 字节编码，应明确区分编码和码点。验证英文、中文和补充平面表情的输出与复制。
