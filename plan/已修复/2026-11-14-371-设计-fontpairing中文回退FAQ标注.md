# 第371批（设计：D-N51 font-pairing 中文场景能力缺口标注）

## 缺陷（来源 plan/categories/04-设计创意/design.md「D-N51」）
- `tools/design/font-pairing.html` 的 FAQ「中文怎么配？」已作答，但 FONT_PAIRS（36 组搭配、35 种字体）**全部是 Google Fonts 拉丁字体**，预览文本默认英文，copy CSS 只输出 `font-family:'X', sans-serif`，无中文字体或 CJK 回退；中文标题会静默落到浏览器默认中文字体，与拉丁预览观感完全不同（低/确认能力缺口，D-N51 证据 `:322-370`/`:433-446`/`:416-417`）。原 FAQ answer 未诚实说明这一点。

## 裁断
- 按「低风险去误导」策略：只**增强 FAQ 文案**说明「内置均为拉丁字体、中文由系统回退、如需一致请补 CJK 字体」，**不实际加入 Noto Sans SC 等中文字体**（避免改 FONT_PAIRS 数据结构 + copy CSS 逻辑，属独立功能项，符合 D-N51 方案「FAQ 明确说明中文由系统回退」轻量落地）。

## 改动（2 源 + 1 构建产物）
- `i18n/tools/content_deepdive.json`（`design/font-pairing` faqs 中 q=「中文怎么配？」的 answer）：补「当前内置搭配均为拉丁字体，预览文本默认英文；若标题含中文，会由浏览器回退到系统默认中文字体，与拉丁预览观感不同。如需中文显示一致，请在字体栈中加入『Noto Sans SC』等中文字体」。
- `i18n/tools/en/design/font-pairing.json:25-26`：FAQ key（中文 answer 整段）与 value（英文 answer）同步（JSON 合法、`json.loads` 通过）。
- `_build.py` EXIT=0 重建：`tools/design/font-pairing.html` FAQ 注入新文案；`sw.js` 戳刷新；sitemap 两页（含繁中）lastmod 刷新（构建既有行为）。

## 验证与门禁
- `font-pairing.html` 新文案落地：`grep -c "当前内置搭配均为拉丁字体"` = 1。
- `verify_design_calc.js design/font-pairing`：EXIT=0、零 FAIL（2/2 用例）。
- `check_inline_js_syntax.js`：全量 **12141** 个 inline 脚本语法正确。
- 纯文案批未新增 verify 强锁（强锁总数不变）。

## 销账
- `plan/categories/04-设计创意/design.md`：删 D-N51 整段，待办 **28→27**。

## 不入库项
- `.workbuddy/memory/2026-11-14.md` 追加本批段落（不入库）。

## 攒批状态
- 367（`ad325769a8`）/368/369/370/371 共 5 个本地未推送提交，满 5 批 ⇒ 跑全量 `run_gates.py` 全绿后一次性 push + 单次确认 Actions `Deploy to GitHub Pages`。
