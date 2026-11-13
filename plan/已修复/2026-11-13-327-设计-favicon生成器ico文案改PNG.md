# 第327批 · 设计 · favicon-generator 页 .ico 虚假文案收口（D-N39）

## 批次目标
收口 `favicon-generator` 工具页「宣称一键下载 .ico / 打包 .ico / ICO 与 PNG 套装」但实际只导出 PNG 的文案名实不符缺陷（D-N39），与第326批 emoji/text 两页同族但工具不同，单独成批避免 JSON 源与 HTML 内联不同步。

## 改动清单（7 处文案，统一 .ico → PNG，保留真实「多尺寸」）
**`tools/design/favicon-generator.html`**（4 处）：
- 第10/15/90 行 meta description / OG / Twitter：`一键下载 .ico 适配各浏览器` → `一键下载多尺寸 PNG 适配各浏览器`
- 第252 行英文文本节点：`downloadable as .ico` → `downloadable as PNG`（中文 data-zh 保留诚实说明「需要 ICO 格式请使用在线转换工具（纯前端无法生成真 ICO）」）
- 第254 行 formula-desc：`打包为 .ico` → `导出 PNG`
- 第302 行 deep-dive 示例：`ICO 与 PNG 套装可下载` → `PNG 套装可下载`

**`i18n/tools/design.json`**（3 处）：
- 第1096 行 favicon-generator intro：`一键下载 .ico` → `一键下载多尺寸 PNG`
- 第1107 行 favicon-generator EN intro：`downloadable as .ico` → `downloadable as PNG`
- 第1717 行 emoji favicon intro（同族补刀，第326批已改但本批复核确认在位）：`multi-size ICO or PNG` → `a PNG icon`

**`json/industry-design.json`** 第82 行、**`json/tools.json`** 第71414 行：favicon-generator 行业/工具描述 `一键下载 .ico` → `一键下载多尺寸 PNG`（这两处 JSON 源只喂 favicon-generator 页，不喂 emoji/text 页，故未混入 326）。

## 验证
- JSON 源语法：3 个文件 `python3 -c json.load` 全 OK。
- design 门禁 `verify_design_calc.js`：335/335 全过（文案改动无语法回归）。
- `_build.py` 重建 EXIT=0；重建后 `favicon-generator.html` 的 meta/OG/Twitter/JSON-LD 均为「一键下载多尺寸 PNG」，**无 .ico 回退**。
- 保留的 `.ico` 命中均为教学引用（第326 行「ICO packs several bitmaps…」解释格式、第688 行 i18n「无需传统 .ico」、第252 行中文诚实提示），非虚假宣称，合理。

## 清单销账
- `plan/categories/04-设计创意/design.md` 删除 D-N39（第178-183 行整块）。

## 提交
- 本地提交（待推送）：第325批 `091eb4e41f` + 第326批 `cf192e8b5c` + 本批，未到「攒 5 批再 push」阈值，按节奏不推送。

## 下批备料（memory 记录）
- D-N19 PNG转SVG、D-N23 翻转异步、D-N97 残留（历史恢复序列化 `__pxGrid`）、D-N100 checkerboard 文案、D-N85 initials-avatar 文案（宣称 PNG/SVG 实际仅 PNG，与 favicon 同族「名实不符」类，可归为文案收口批）、其余 design.md 中「文案与实现不一致」类低频项。
