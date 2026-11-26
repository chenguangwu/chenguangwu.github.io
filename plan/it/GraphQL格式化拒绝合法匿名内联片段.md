# GraphQL 格式化：拒绝合法匿名内联片段

- 受影响工具：`tools/it/graphql-formatter.html`
- 问题：校验要求 `...` 后必须是名称等特定词元，拒绝省略类型条件的合法内联片段，例如 `query { user { ... @include(if: true) { name } } }` 或 `query { user { ... { name } } }`，格式化和压缩均受影响。依据源码推导，待浏览器复核。
- 解决方案：使用符合 GraphQL 语法的解析器或完善内联片段语法，支持可选类型条件和指令，同时保留非法片段的校验。
