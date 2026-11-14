# 第370批（设计：D-N5 font-preview 跨平台预览能力缺口标注）

## 缺陷（来源 plan/categories/04-设计创意/design.md「D-N5」）
- `tools/design/font-preview.html` 用本机系统字体栈渲染、点击复制整条 `font-family`；原 FAQ「本地没有的字体？」只说"未加载会回退默认"，**未说明跨平台差异**——macOS 上效果好的字体栈在 Windows/Android/iOS 用户端会退化为不同字体，用户复制后线上效果与预览不符（低/确认能力缺口，D-N5 证据 `:550-557`）。

## 裁断
- 按「低风险去误导」策略：只**增强 FAQ 文案**补充跨平台提示，**不实现**平台标注 / 回退链可视化 / 可用性表（属独立功能项），符合 D-N5 方案里"标明当前预览平台"的轻量落地。

## 改动（2 源 + 1 构建产物）
- `i18n/tools/content_deepdive.json`（`design/font-preview` faqs[0] answer）：补「预览效果取决于本机系统字体，Windows / macOS / Android / iOS 的可用字体集不同，复制到其它设备或系统后实际显示可能与预览不一致」。
- `i18n/tools/en/design/font-preview.json:24-25`：FAQ key（中文 answer 整段）与 value（英文 answer）同步（JSON 合法、`json.loads` 通过）。
- `_build.py` EXIT=0 重建：`tools/design/font-preview.html` FAQ 注入新文案；`sw.js` 戳 `ea9d8b8419`；sitemap 两页（含繁中）lastmod 刷新（构建既有行为）。

## 验证与门禁
- `font-preview.html` 新文案落地：`grep -c "Windows / macOS / Android / iOS 的可用字体集不同"` = 1。
- `verify_design_calc.js design/font-preview`：EXIT=0、零 FAIL（4/4 用例，D-N4 锁 FPEN/FPLANG 仍绿）。
- `check_inline_js_syntax.js`：全量 **12141** 个 inline 脚本语法正确。
- 纯文案批未新增 verify 强锁（强锁总数不变）。

## 销账
- `plan/categories/04-设计创意/design.md`：删 D-N5 整段，待办 **29→28**。

## 不入库项
- `.workbuddy/memory/2026-11-14.md` 追加本批段落（不入库）。
