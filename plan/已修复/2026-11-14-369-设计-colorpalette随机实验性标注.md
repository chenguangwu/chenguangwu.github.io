# 第369批（设计：D-N3 color-palette-generator「随机」模式标注实验性）

## 缺陷（来源 plan/categories/04-设计创意/design.md「D-N3」）
- `tools/design/color-palette-generator.html:200` 的「随机」模式 tab 与单色/互补/三角等**协调规则**并列，但 `generateRandom()`（`:503-508`）仅生成 5 个彼此独立的随机 hex，无任何色彩协调逻辑；页面无任何「该模式不保证协调」提示。设计师误以为随机也是协调配色方案。

## 裁断
- 按「低风险去误导」策略：只**标注实验性**提示用户，不改动随机生成算法（不新增受约束随机/锁定再生成等功能，属独立功能项）。符合 D-N3 方案「明确标注『实验性随机』」。

## 改动（1 文件）
- `tools/design/color-palette-generator.html:200`
  旧：`<div class="mode-tab" data-mode="random" onclick="setMode('random')">随机</div>`
  新：`<div class="mode-tab" data-mode="random" onclick="setMode('random')">随机（实验性）</div>`
  （精确串 `>随机</div>` 文件内唯一；该 tab 文本未在 EN 字典中，EN 态本就显示中文，与「单色/互补色」等 tab 行为一致，无需 EN 同步）
- `tools/design/color-palette-generator.html:188` 的「随机颜色」按钮是 baseColor 单色随机，非协调模式，不在 D-N3 范围，未动。

## 验证与门禁
- `verify_design_calc.js design/color-palette-generator`：EXIT=0、零 FAIL（4/4 用例，锚定生成输出的确定性结构，不依赖 tab 文本）。
- `check_inline_js_syntax.js`：全量 **12141** 个 inline 脚本语法正确。
- 纯文案批，未新增 verify 强锁（强锁总数 378 条不变）。

## 销账
- `plan/categories/04-设计创意/design.md`：删 D-N3 整段，待办 **30→29**。

## 不入库项
- `.workbuddy/memory/2026-11-14.md` 追加本批段落（不入库）。
