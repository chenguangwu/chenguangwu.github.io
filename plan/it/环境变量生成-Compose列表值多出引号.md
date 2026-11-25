# 环境变量生成器：Docker Compose 列表值多出引号

## 问题

Docker Compose 输出复用 `.env` 的值编码，并把结果拼在 YAML 列表的 `KEY=` 后。例如变量 `MESSAGE` 的值是 `hello world` 时生成 `- MESSAGE="hello world"`。在 YAML 中整项是普通标量，双引号位于标量内部，会成为变量值的一部分，容器实际得到 `"hello world"` 而不是 `hello world`；换行和反斜杠等转义也无法按 `.env` 规则还原。值含 `#` 等字符还可能改变 YAML 解析结果。

## 解决方案

为 Compose 单独序列化：使用 YAML mapping 格式并安全引用字符串值，或正确引用整个列表项；同时处理 Compose 的 `$` 插值规则，使特殊字符按用户期望保留。用 YAML 解析和 Compose 配置展开验证空格、引号、反斜杠、`#`、`$` 及多行值。

## 受影响工具路径

- `tools/it/env-generator.html`（`envValue`、`generateOutput` 的 docker 分支）
