# curl 解析忽略 GET 和 HEAD 选项

- 受影响工具：`tools/it/curl-parser.html`
- 问题：`-G/--get` 和 `-I/--head` 未被识别。`curl -G -d 'q=x' https://example.com` 被显示为 POST 并将数据当作请求体，而 curl 会将数据放入查询字符串；`curl -I https://example.com` 则被显示为 GET 而非 HEAD。源码分析，需在页面及本地 curl 对照复核。
- 解决方案：按 curl 实际行为处理 `-G`、`-I` 与数据、显式方法的组合，无法确定时提示而非输出确定结论；覆盖短长选项、已有查询参数和空数据。
