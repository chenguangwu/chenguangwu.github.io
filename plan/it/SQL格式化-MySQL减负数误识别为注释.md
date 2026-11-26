# SQL 格式化：MySQL 减负数误识别为注释

- 受影响工具路径：`tools/it/sql-formatter.html`

## 问题描述

MySQL 方言的分词器将所有 `--` 识别为行注释，而 MySQL 要求第二个横线后紧跟空白或控制字符。例如 `SELECT 1--1 FROM t` 中的 `--1 FROM t` 实际是减负数表达式及后续语句，却被当作注释整体跳过格式化和校验。依据源码分析，具体输出及其他语法影响还需运行验证。

## 解决方案

按方言识别行注释，MySQL 仅在符合其空白或控制字符规则时识别 `--`；分别验证减负数、真实注释及其他方言，并检查格式化与压缩后语义保持一致。参考 [MySQL 注释语法](https://dev.mysql.com/doc/refman/8.4/en/ansi-diff-comments.html)。
