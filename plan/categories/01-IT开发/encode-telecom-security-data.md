# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

## 已知问题
### E1. encode 系结果仅文本
- 描述：base64/hex/url 系缺「字节级对照」（每个字符↔字节↔编码段高亮）。
- 受影响：tools/encode/*（~30 页）
- 方案：结果区加「字节视图」折叠面板（教学向差异化）。

### E2. telecom 换算页口径混杂
- 描述：convert-24 已修 SNR→Eb/N0；bandwidth-calculator 已修 MB/s 倍率。同类页（ber-snr、subnet、path-loss）口径自洽，但「带宽 KB=0.001 与 GB=1024 混用」的进制口径仍不统一（audit 备案）。
- 受影响：tools/telecom/bandwidth-calculator.html（进制）、estimate-9（已修守卫）
- 方案：全分类统一「bit 系 1000 / byte 系 1024」并页面标注。

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
- 🔴 待开发（E2 进制统一可先行）
