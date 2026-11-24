# JWT 生成：非对象 JSON 未校验

受影响工具：`tools/it/jwt-parser.html`

## 问题描述
页面接受任意合法 JSON 后直接写 `payload.iat` 和 `payload.exp`。输入 `null` 会在属性赋值时抛错；数组或其他非对象值即使可继续执行，也不能可靠表达页面预期的声明对象。

## 解决方案
要求 Payload 是非空的 JSON 对象（允许空对象），对数组、null 和原始值显示字段错误；签名前校验声明类型并清理旧生成结果。覆盖所有 JSON 顶层类型。
