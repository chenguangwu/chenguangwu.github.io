# curl 解析器：引号内转义引号导致参数被拆散

## 问题

分词正则把双引号内的 `\"` 当作引号结束，虽然后续 `trimQuote()` 试图还原转义引号，但分词已提前截断。例如 shell 命令 `curl https://example.com -H "X: a\" b"` 的 `-H` 参数应为 `X: a" b`；当前被拆为 `"X: a\"` 和 `b"`，Header 结果缺失后半部分且没有明确报错。复杂 JSON 请求体也可能发生同类截断。

## 解决方案

用可识别单引号、双引号、转义与续行的状态机进行分词，再按对应 shell 引号规则还原参数；对于暂不支持的 shell 展开语法明确提示。覆盖含转义引号与空格的 Header、JSON、单引号字面反斜杠和未闭合引号。

## 受影响工具路径

- `tools/it/curl-parser.html`（`parse` 分词与 `trimQuote`）
