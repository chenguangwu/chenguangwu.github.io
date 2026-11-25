# JWT 调试器：生成载荷未检查对象类型

## 问题
生成器只调用 JSON.parse，数组、null 或字符串也可作为载荷生成 token；这些值不符合 JWT Claims Set 应为 JSON 对象的要求。失败时旧输出也可能仍留在页面。

## 解决方案
生成前要求载荷为非 null、非数组的 JSON 对象，非法时提示并清除或禁用旧输出；验证对象、数组、null、字符串和非法 JSON。

## 受影响的工具路径
- `tools/it/jwt-debugger.html`
