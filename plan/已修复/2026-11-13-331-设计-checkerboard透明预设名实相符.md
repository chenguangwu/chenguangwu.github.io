# 第331批 · 设计创意 · checkerboard 透明底预设名实相符（销 D-N100）

## 背景
- D-N100 原报「checkerboard 透明底预设仍带 #ffffff、名不副实」。329 批已将「格数→可调格子大小」「导出图片→可复制 CSS 代码」文案改对，本批收口最后的预设标签残留。
- 预设「透明底导出棋盘（16px）」（checkerboard-generator.html:400）实际 `color1=#ffffff`（白底），且工具仅复制 CSS 不导出图片，标签同时虚假宣称「透明」「导出」。

## 改动
- checkerboard-generator.html:400 预设标签「透明底导出棋盘（16px）」/「Transparency checker 16px」→「白底棋盘（16px）」/「White checker 16px」。
- 依据：`<input type="color">` 无法表示 `transparent`，真透明需改 UI（超出低风险残留修复范围）；诚实改标签使「名实相符」。`color1=#ffffff` 即白底，标签与实现一致。
- 重建 `_build.py` 后 zh-tw 产物同步（gitignored，部署时由构建重生成）。

## 验证
- `_build.py` EXIT=0（A 级率 4713/100%）。
- 源 line400 / zh-tw line379 均现「白底棋盘（16px）」，全仓无「透明底导出棋盘」「Transparency checker」残留。
- 小门禁：design calc 335/335、inline JS 语法 12141/12141 全过（纯标签改动无逻辑变更）。

## 销账
- design.md 删 `### D-N100 checkerboard 透明底预设仍带 #ffffff、名不副实（残留）`（261–265 行）。
- checkerboard 相关 D-N85/D-N100 全部闭环；design 分类下 checkerboard 无遗留项。
