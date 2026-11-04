# 导出与下载路径质量（export-download-quality）

> 本线批次记录（Batch 10–13）。只固化可复核的口径与基线数字，不重复各页源码细节。

## 1. 测有损压缩参数必须用高熵图（Batch 11 复盘）

**一句话：用 120×80 纯色图测 `quality` 会产生稳定假绿，验证有损压缩参数一律改用 1024×1024 随机噪点。**

同一批页面对照（1024×1024 随机噪点）：

| 页面 / 格式 | quality=1.0 | quality=0.1 | 落差 |
|---|---|---|---|
| `tools/image/image-compress.html`（WebP） | 3,146,476 B | 320,646 B | 9.8× |
| `tools/design/image-format-converter.html`（JPEG） | 3,062,090 B | 90,427 B | 33.9× |
| `tools/image/image-converter.html`（页内直测） | 3,061,280 B | 89,963 B | 34× |

对照：120×80 纯色图 q1.0=1018 B、q0.2=938 B（仅差 8%），据此曾误判「参数未生效」。结论：参数一直生效，是小图/纯色把量化差压没了。

## 2. `revokeObjectURL` 全站盘点（Batch 13 基线）

扫描口径：`tools/**/*.html` 文本级统计 `createObjectURL(` / `revokeObjectURL(` 出现次数，再按「是否有终态释放」逐页核对。

- 全站：79 页含 `createObjectURL`；create 合计 98，revoke 合计 114（修复后）。
- 修复后差值 > 0 的页面为 0；仍保留的 +1 差值均为「当前正在使用的媒体 / 原图 URL」，随下次换图或重置释放，非泄漏。

| 页面 | create | revoke（修复前 → 后） | 终态释放（修复方式） | 风险 |
|---|---|---|---|---|
| `tools/ai/ocr.html` | 3 | 0 → 3 | 换图 onload 释放旧预览；推理 `finally` 释放运行 URL；下载后 1s 释放 | 反复触发（高） |
| `tools/ai/image-classification.html` | 2 | 0 → 2 | 换图 onload 释放旧预览；推理 `finally` 释放 | 反复触发（高） |
| `tools/image/image-mosaic.html` | 2 | 0 → 2 | 新图 onload 释放旧原图 URL；重置释放 | 反复触发（高） |
| `tools/audio/audio-waveform.html` | 1 | 0 → 1 | 换文件时释放旧音频 URL（当前文件保留） | 反复触发（高） |
| `tools/video/video-trimmer.html` | 1 | 0 → 1 | 换文件时释放旧视频 URL（当前文件保留） | 反复触发（高） |
| `tools/ai/speech-to-text.html` | 1 | 0 → 1 | 下载后 1s 释放 | 一次性（中） |
| `tools/ai/text-summarization.html` | 1 | 0 → 1 | 下载后 1s 释放 | 一次性（中） |
| `tools/biz/markdown.html` | 1 | 0 → 1 | 导出点击后 1s 释放 | 一次性（中） |
| `tools/it/stopwatch.html` | 1 | 0 → 1 | CSV 导出后 1s 释放 | 一次性（中） |

统一修法：新图 `onload` 后释放旧 URL；下载 / 导出 `click()` 后 `setTimeout(..., 1000)` 释放（立即释放会被 Safari 取消下载）。

## 3. 大画布上限的可量化判据（Batch 13）

- 阈值：**单边 16384 px、总像素 268,435,456（2.68 亿）**（Chrome）；Safari 单边约 4096 更严，按同一判据提前拦截即可覆盖。
- 判据函数：`js/common.js` 的 `canvasExportError(w, h)`（非法尺寸 / 超限返回可读文案，否则返回空串）。
- 口径：**导出前**用目标 canvas 的 `width × height` 先判，超限直接提示「当前 W×H 超出浏览器画布上限…请降低尺寸」，不等 `toBlob` 返回 null。

已落前置拦截（10 页）：

| 页面 | 拦截点 | 尺寸来源 |
|---|---|---|
| `tools/image/image-resize.html` | `toBlob` 前 | 目标宽高 |
| `tools/image/image-mosaic.html` | 建导出画布前 | 原图宽高 |
| `tools/ophthalmology/eye-chart-toolkit.html` | `toBlob` 前 | PPI × 缩放 |
| `tools/design/image-resizer.html` | 建画布前 | 用户输入宽高 |
| `tools/design/image-format-converter.html` | 每张建画布前 | 自定义 / 百分比缩放 |
| `tools/design/image-rotator.html` | 建画布前 | 旋转外接框（≤√2 倍） |
| `tools/image/image-rotate.html` | `toBlob` 前 | 旋转外接框 |
| `tools/image/image-watermark.html` | `toBlob` 前 | 原图尺寸 |
| `tools/office/flowchart.html` | 建画布前 | 图宽高 ×2 |
| `tools/office/mindmap.html` | 建画布前 | 图宽高 ×2 |

尚未前置拦截（尺寸受源图约束、放大倍数 ≤1，列为第二档）：`image/image-crop`、`image/image-filter`、`image/image-compress`、`image/image-converter`、`image/id-photo-crop`、`image/nine-grid-cutter`、`image/gif-split`、`image/wechat-cover-maker`；其余 `toDataURL` 页为固定尺寸生成（二维码 / 条形码 / 头像 / 视标等），不涉及用户放大。
