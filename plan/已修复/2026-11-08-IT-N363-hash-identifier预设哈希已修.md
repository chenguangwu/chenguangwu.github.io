# IT-N363 hash-identifier「默认参数」预设哈希被截断 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/hash-identifier.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

「默认参数」预设的 `h` 只写了完整 SHA-256 的前 40 个十六进制字符：

```
5e884898da28047151d0e56f8dc6292773603d0d          ← 旧预设，40 位
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8   ← resetForm / 页面默认值，64 位
```

40 位恰好落进「SHA-1 160 位」档 ⇒ 首屏一点「默认参数」即给出错误的算法结论。同页 `resetForm()` 用的是完整 64 位，两处不一致。

## 修复

```js
values:{'h':'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'}
```

与 `resetForm()` 的常量逐字符一致（已用脚本比对：`len=64`、`identical=true`）。

## 判别力实测

新增回归用例（钉住 40 位 → SHA-1 这个档位，也就是旧预设误落的档）：

```
slug:   it/hash-identifier
inputs: { h: "5e884898da28047151d0e56f8dc6292773603d0d" }
clicks: ["calcTool()"]
expect: ["SHA-1 160 位（40 位十六进制）"]
```

页面默认值是完整 64 位 ⇒ 判 SHA-256，默认态不命中本串，非逃生项。

## 补充证据

- jsdom 加载页面实测默认态：`#h` 长度 64，结果区为「SHA-256 256 位（64 位十六进制）」。
- 预设芯片点击依赖 `js/tool-kit.js`（页面用绝对路径 `/js/...`，jsdom 的 file:// 场景加载不到），故预设值本身以「源码常量比对」取证：预设与 `resetForm` 均为 64 位且完全一致。

`node scripts/verify_it_calc.js` → **1078/1078 通过**；判别力检查 → **逃生 0**。
