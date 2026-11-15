# 第 164 批复核失败：curl URL 编码名称重复编码

- 来源：`plan/已修复/2026-11-11-164-IT清单1条-curl-parser-urlencode编码.md`。
- `tools/it/curl-parser.html` 的 `urlEncodeData()` 对 `name=value` 的名称再次调用 `encodeURIComponent`。例如 `--data-urlencode 'a%20b=c'` 被解析成 `a%2520b=c`；实际 curl 的名称应预先编码，执行 `curl -sS -G --data-urlencode 'a%20b=c' --connect-timeout 1 -o /dev/null -w '%{url_effective}\n' http://127.0.0.1:1/` 可见 URL 中为 `a%20b=c`。无需成功连接即可观察生成的 URL。
- 另，实测 curl 对值中的空格产生 `+`，现实现产生 `%20`；两者在表单解码下等价，但与工具声称模拟 curl 的原始请求不完全一致。
- 待处理：按 curl 的 `--data-urlencode` 语义处理已编码名称，并补充以实际 curl 为参照的回归；明确空格输出口径。既有测试仅覆盖简单名称，10/10 通过仍未覆盖此缺陷。
