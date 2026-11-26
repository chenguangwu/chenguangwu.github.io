# Markdown 检查：特殊标题重复检测失效

- 受影响工具：`tools/it/markdown-lint.html`
- 问题：重复标题使用普通对象计数，标题为 `constructor`、`toString` 等继承属性名时初始值不是数字，导致重复标题不被报告。例如连续两行 `# constructor`。依据源码推导，待浏览器复核。
- 解决方案：用 Map 或无原型对象保存计数，覆盖 `constructor`、`__proto__`、普通标题及不同层级的规则。
