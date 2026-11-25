# JavaScript 压缩改变自动分号插入语义

## 问题

启用空白压缩时，工具将代码中的换行统一折叠为空格，没有保留 JavaScript 自动分号插入所需的换行。例如 `function f(){return\n1}` 原本返回 undefined，压缩后成为 `return 1`，返回值发生变化；其他依赖换行的语句也可能变成无效代码。

## 解决方案

使用能够解析 JavaScript 并保持语义的本地压缩器，或在不能安全判断时保留必要换行并提示；验证 return、break、continue、后置自增及注释附近换行的行为与原代码一致。

## 受影响工具路径

- `tools/it/js-minifier.html`
