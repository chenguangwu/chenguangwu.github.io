# JSONPath 查询：继承属性被当作 JSON 字段

## 问题描述

输入 `{}` 并查询 `$.constructor`，代码用 `property in current` 判断字段，因 JavaScript 对象继承了 `constructor` 而错误地产生一个匹配；该值是函数，序列化到结果数组时显示为 `null`。原 JSON 并无该字段，查询结果和匹配数量都不正确；`toString` 等继承属性也受影响。

## 解决方案

子字段查询只读取对象自身属性，保留 JSON 中显式存在的同名键；递归和通配符也按自身可枚举字段处理。验证空对象的 `constructor`、`toString` 无匹配，以及显式同名键能正确查询。

## 受影响工具路径

- `tools/it/json-path.html`：`jsonPath()` 的子字段查找。
