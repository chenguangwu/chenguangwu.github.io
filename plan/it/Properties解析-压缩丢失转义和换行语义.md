# Properties 压缩丢失转义和换行语义

- 受影响工具：`tools/it/properties-parser.html`
- 问题：压缩先解析再直接拼接 `key=value`，没有对键和值重新转义。例如 `a\ b=value` 输出 `a b=value`，重新读取会把键变成 `a`；包含 `\n` 的值也会变成实际换行并破坏记录。源码分析，需在页面及 Java Properties 读取器对照复核。
- 解决方案：复用符合 Java Properties 语义的序列化器处理键和值，保留空格、分隔符、反斜杠及控制字符；通过解析→压缩→重新解析比较键值验证。
