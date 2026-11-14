# 第368批（设计：D-N49 image-color-picker 删除「放大取样」不实表述）

## 缺陷（来源 plan/categories/04-设计创意/design.md「D-N49」）
- `tools/design/image-color-picker.html` 的 meta/OG/twitter/JSON-LD 与正文均宣称「支持放大取样 / magnified sampling」，但脚本（`:284-301`）仅 `getBoundingClientRect` + `getImageData` 取单像素，无缩放视图、放大镜或像素网格。该卖点不存在（低/能力缺口）。

## 裁断
- 按既往「低风险去误导」策略：**只删除不实表述、不实现放大镜功能**（零回归），符合 D-N49 方案 B。

## 改动（3 文件 + 2 个 _build 产物待重建）
- `tools/design/image-color-picker.html`：行 10/15/68/71（meta/OG/twitter/JSON-LD）+ 行 153（正文 `<p data-zh>`）中文串删「放大取样与」；英文 `with magnified sampling` → `and keep a history`。（5 处中文串唯一、1 处英文串唯一）
- `i18n/tools/design.json`：image-color-picker 的 zh-CN intro（行 1832）、en-US intro（行 1843）同步删除「放大取样 / magnified sampling」。（各唯一）
- `i18n/tools/en/design/image-color-picker.json`：行 7 key（中文）+ value（英文）同步删除，JSON 合法性 `json.loads` 通过；key 与 HTML 正文 `data-zh` 改后文本**字节一致**（EN 态运行时替换可命中）。
- `json/industry-design.json:209` 与 `json/tools.json:73544` 含旧串，属 `_build.py` 产物，改 design.json 源后将在攒满 5 批统一重建时自动同步，**本批不手动改**。

## 验证与门禁
- `verify_design_calc.js design/image-color-picker`：EXIT=0、零 FAIL（该页 0/0 用例，删除文案不影响强锁）。
- `check_inline_js_syntax.js`：全量 **12141** 个 inline 脚本语法正确。
- 纯文案批，未新增 verify 强锁（强锁总数 378 条不变）。

## 销账
- `plan/categories/04-设计创意/design.md`：删 D-N49 整段，待办 **31→30**。

## 不入库项
- `.workbuddy/memory/2026-11-14.md` 追加本批段落（不入库）。
