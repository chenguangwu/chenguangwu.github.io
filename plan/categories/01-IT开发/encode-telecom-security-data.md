# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

## 已知问题
### E1. encode 系结果仅文本
- ✅ 已落地（2026-10-26 · 落点 it/char-encoder 多格式字符编码器）：加「🔬 字节视图」卡（#byteViewBox：字符 ↔ 码点 ↔ UTF-8 字节 hex/binary 逐字符对照表，空格␣/换行⏎/制表⇥符号化、截前 64 字符、TBKit EN 守卫双语；空输入清空零渲染）。verify 强用例（Hi中 → U+4E2D e4 b8 ad 11100100…）；EN probe 全英文（输入回显除外）。verify it 763/763、判别器 0 逃生、门禁 218/218。

### E2. telecom 换算页口径混杂
- ✅ 已落地（2026-10-26）：bandwidth-calculator KB 选项 0.001→1/1024（byte 系统一 1024，GB/TB 原本已 1024）+ 「bit 系 1000 / byte 系 1024」口径标注（data-zh 双语）；quick-calc-time-bandwidth formula-eq 80 秒（1000 进制）与案例 91 秒（1024 进制）矛盾消除标注。verify 强用例（2048 KB=2.00 MB，clicks 直调）；verify telecom 11/11、判别器 0、门禁 218/218。

### E3. security 模拟器类内容单薄
- 描述：data-erase/virtual-safe/smoke-alarm 偏玩具化，无专业依据展示。
- 受影响：tools/security/*（~20 页）
- 方案：接 S7 引据徽标（NIST 800-88 标准条目），提升可信度。

## 功能缺陷
- crc-calculator 已含 7 算法（已验证正确）——缺「自定义多项式」输入（工程师刚需）。

## 优化点
- S1 首屏即答案：编码类页默认给「Hello World」示例的完整编码链。

## 受影响范围
- tools/encode/、tools/telecom/、tools/security/、tools/data/（合计 ~100 页）

## 进度
- 🟢 批次 2026-10-26：E1 字节视图（char-encoder）+ E2 进制统一（bandwidth-calculator/quick-calc）均已落地。
- 🔴 待开发：E3 security 引据徽标（NIST 800-88）；crc-calculator 自定义多项式；S1 编码链默认示例。
