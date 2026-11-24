# CSS 压缩：标注字节的大小实际按字符串长度计算

受影响工具：`tools/it/css-minifier.html`

问题：大小卡片标注“字节”，但 `showStats` 接收 `input.length` 和 `css.length`，JavaScript 长度是 UTF-16 码元数，不是 UTF-8 文件字节数。含中文或 emoji 的 CSS 会显示错误大小，压缩率也可能与实际传输字节比例不同。

解决方案：以 `TextEncoder` 或兼容方式按明确编码计算处理前后字节数，并说明不含 gzip/brotli；核对展示结果与实际下载编码。验证 ASCII、中文、emoji 和空输入。

证据范围：静态代码分析，页面及下载文件字节数待核验。
