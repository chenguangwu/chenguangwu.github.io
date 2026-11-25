# MySQL 命令速查：介绍承诺的事务与 JOIN 条目缺失

## 问题

页面描述、SEO 文案和用途说明宣称可查 JOIN、索引、事务语句，但命令数据中没有独立的 JOIN、START TRANSACTION、COMMIT、ROLLBACK 或 CREATE INDEX 条目。搜索 `JOIN` 或 `COMMIT` 时无法获得相应速查结果；正文中虽有一个 JOIN 算例，也无法从命令筛选中找到。用户按搜索摘要进入后缺少预期内容。

## 解决方案

补充 JOIN 类型、索引创建查看及事务开始、提交、回滚的简短例子，并注明存储引擎、DDL 隐式提交等适用条件及版本差异；确保命令搜索可检索中英文关键词。同步核对 SEO、正文和实际收录范围，避免夸大覆盖。

## 受影响工具路径

- `tools/it/mysql-cheatsheet.html`（`COMMANDS`、介绍与 SEO 文案）
