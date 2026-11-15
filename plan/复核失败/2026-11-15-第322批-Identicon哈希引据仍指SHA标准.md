# 第322批复核失败：Identicon 哈希引据仍指 SHA 标准

原记录：`2026-11-12-322-设计-玻璃拟态图案与Identicon文案画廊修复.md`。其余已核对的修复点从原记录移除。

- 原要求：哈希引据表与实际 Java String.hashCode 风格的 32 位乘 31 算法一致，避免误称 SHA-256。
- 证据：`tools/design/identicon-generator.html` 引据表第二列已改成 Java String.hashCode 变体，但同一行第三列仍是 `FIPS 180-4 (SHA-2)`（中英均如此）。FIPS SHA-2 不是页面 `hashString()` 的乘 31 算法的依据，仍会误导读者。
- 验证：逐列核对引据表与 `hashString()`；`node scripts/verify_design_calc.js glassmorphism-generator identicon-generator pattern-generator spinner-generator` 为 15/15，未检查静态引据。
- 待修：更换或移除不相关的 SHA-2 引据，中英内容保持一致并核对构建后页面。
