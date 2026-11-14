# 2026-11-14-399 文娱 · tongue-twister 文案源同步

## 背景
397 批已为 `tools/fun/tongue-twister.html` 实现真实可选本地计时（performance 计时 + 每条最佳用时存本机），
但文案源仍写「不录音、不计时、不评分」。构建会从源重注入文案，页面会还原成与功能矛盾的描述。

## 修复内容（只改源，不直接改生成文案）
- `i18n/tools/fun.json`：zh-CN `intro` / `note` 与 en-US `intro` 改为「不录音、不评分，支持可选本地计时，最佳用时仅存本机」。
- `i18n/tools/en/fun/tongue-twister.json`：`map` 内「no timer」类译文改为「optional local timer」，并补齐新 intro、注意事项、FAQ 的英文键。
- `i18n/guides/tongue-twister-guide.json` + `guides/tongue-twister-guide.html`：指南 lead、使用步骤（新增计时步骤）、技巧、FAQ 与 meta/JSON-LD 同步为可选本地计时口径。
- `i18n/tools/_en_override.json`：`fun/tongue-twister` 的 `ed` 改为「no audio recording or scoring, with an optional local timer」。
- `tools/fun/tongue-twister.html` 的 `SoftwareApplication` JSON-LD 描述为页面静态块（非构建注入区），手工同步。

## 验证
- [x] `python3 _build.py` 重建通过
- [x] 重建后页面 meta / og / twitter / WebApplication JSON-LD / 注意事项 / tool-intro 均无「不计时」残留
- [x] `tools/fun/index.html` 卡片中文描述随构建更新
- [x] 中文/英文文案与实际功能一致：可选本地计时为真，无录音、无评分

## 销账
- 交接单第五节唯一待办已闭环；`plan/fake-tools` 无 tongue-twister 条目需删。
