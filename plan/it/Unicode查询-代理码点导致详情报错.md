# Unicode 查询：代理码点应明确标注

- 受影响工具：`tools/it/unicode-lookup.html`
- 问题：搜索允许 `U+D800` 等代理码点，点击详情时将孤立代理项传给 `encodeURIComponent`，会抛出 URIError，详情无法正常更新。源码分析，待浏览器复核。
- 解决方案：区分 Unicode 码点与可独立编码的 Unicode 标量值，对代理范围说明其用途并将 UTF-8、URL 编码标为不适用；校验超范围输入，覆盖 D7FF、D800、DFFF、E000 和非 BMP 字符。
