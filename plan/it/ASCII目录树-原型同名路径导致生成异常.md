# 原型同名路径导致目录树生成异常

- 受影响工具：`tools/it/ascii-tree-generator.html`
- 问题：节点用普通对象保存并以 `node[p]` 判断是否存在，`constructor`、`toString`、`__proto__` 等合法目录名会命中继承属性，导致节点缺失或访问 `_children` 时报错。源码分析，需在页面用 `constructor/file.js` 等路径复核。
- 解决方案：使用 `Map` 或无原型字典，并仅判断自有节点；覆盖特殊名字的根节点、子目录和同名合并，确保不污染原型。
