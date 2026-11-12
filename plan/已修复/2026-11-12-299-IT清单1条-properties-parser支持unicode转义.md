# 第299批 · IT 清单：properties-parser 不解码 \uXXXX

## 清单来源
`plan/categories/01-IT开发/it.md` → 2026-11-03 续查（并行批 G）：`properties-parser.html:298` 的 `unescapeVal` 不解码 `\uXXXX`（`greet=\u4f60\u597d` 原样保留），与页面 FAQ「为什么中文显示成 \uXXXX」的说明不一致。

## 修复
`unescapeKey` / `unescapeVal` 统一走 `__ppUni()`：
1. 私有区占位符 `\uE000` 保护字面双反斜杠 `\\`；
2. 正则 `/\\u([0-9a-fA-F]{4})/g` 解码为 `String.fromCharCode(parseInt(h,16))`；
3. 处理 `\n` / `\t` / `\=` / `\:` / `\ `；
4. 占位符还原为单个反斜杠。

⇒ `\u4f60\u597d` → `你好`；`\\u4f60`（字面转义）保留为 `\u4f60`，不误解码。

## 验证
- `verify_it_calc.js` +1 强锁（PPUNI）：新源码 5/5；旧源码 **4/5**（输出字面 `\u4f60\u597d`），恢复 5/5。
- **真机（Playwright）**：`greet=\u4f60\u597d` → JSON `"你好"`；`lit=\\u4f60` → JSON `"\\u4f60"`（字面保留）；零 pageerror。
