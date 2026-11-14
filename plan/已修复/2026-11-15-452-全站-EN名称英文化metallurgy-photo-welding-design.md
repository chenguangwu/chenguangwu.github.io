# 452 · 全站 EN 名称英文化（metallurgy / photo / welding / design 39 页）

## 问题
`metallurgy` 10、`photo` 10、`welding` 10、`design` 9 页 `en` 仍为中文名，英文态 SEO 与卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 39 条。

- metallurgy：`Brinell Rockwell Vickers Hardness Converter`、`Tailing Grade & Recovery Analyzer`、
  `Electric Arc Furnace Smelting Calculator`、`Forging Temperature & Force Calculator`。
- photo：`Hyperfocal Distance Calculator`、`Star Trail Exposure Time Calculator`、
  `Equivalent Focal Length Calculator`、`Flash Guide Number Calculator`。
- welding：`Friction Stir Welding Parameter Calculator`、`Interpass Temperature Control Calculator`、
  `Laser Welding Spot Size Calculator`、`Weld NDT Method Selector`。
- design：`CSS Keyframe Animation Generator`、`Box Shadow Batch Generator`、
  `CSS Background Pattern Generator`、`WCAG Contrast Checker`、`Accessibility Compliance Checker`。

## 验证
- 四行业 `en` 含中文 **39 → 0**；全站 **467 → 428**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
advertising 9 → leather 9 → textile 9 → chemistry 9 → chemical 8 → food 8 → forestry 8 → dyeing 8。
按老板要求暂不推送、不跑全量门禁。
