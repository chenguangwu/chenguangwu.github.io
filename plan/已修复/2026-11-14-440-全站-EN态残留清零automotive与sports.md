# 第 440 批：EN 态残留清零 automotive / sports（2026-11-14）

## 缺陷
- 探针 `--check` 实测：`automotive 59 页中 7 页有残留`、`sports 75 页中 8 页有残留`，合计 **15 页 / 27 条 text 节点 + 1 条 aria-label 属性残留**。
- 类型分两类：
  - **长公式/算例/注意事项**：磨损率、剩余厚度、折旧、油耗标准差与异常阈值、λ 空燃比、轮胎花纹、发电机负载率、铁三计时、柔韧进步、二项模拟、VO2max 对照、1RM 推算、MAOD 模型等。
  - **半翻译节点**（`src_diff=True`）：`data-zh` 是纯中文原文，当前显示文本却是全局层半翻译后的中英混合串，如 `Residual value = 购车价 × 残值率%…`、`Standard error = √(p(1−p)/n)，衡量…`、`Total time = swim + … 1时0分0秒`。
- 另有 `sports/juzhongzongchengji-sinclair-xishu` 的 `aria-label="跨体重预测的目标体重"` —— `--extract` 不收录属性类，靠 `--check` 兜底发现。

## 修法（改源，不改 HTML）
1. 批量 `--extract` 15 页 → 筛 `kind=text` 的 27 条 → 逐条语义化翻译（长公式保留符号与数字口径、术语按功能直译），写入 **14 个 per-tool 字典**的 `map`。
2. 首轮 `--check` 仍报 6 页：5 页为半翻译节点、1 页为属性漏项。
   - **双 key 修复**：从 work 明细读 `zh_src`（data-zh 原文），`map[zh_src] = map[zh]`，补 5 条锚点 ⇒ 运行时按 data-zh 查表即可命中。
   - **属性映射**：`map['跨体重预测的目标体重'] = 'Target body weight for cross-weight prediction'`。
3. `--reindex` 重建两行业 `_index.json`；`python3 _build.py` 单步核验（只带出 `sw.js` 版本戳）。
4. 新坑已固化进 `plan/门禁提速与工作协议.md` 第四节「EN 态翻译规则」。

## 验证（提速协议：只跑相关轻量项）
- `--check`：`automotive 0/59`、`sports 0/75`（此前 7 / 8 页）。
- `--roundtrip`：两行业均「不一致 0 页」。
- `--smoke --en` 抽查 `automotive/fuel-anomaly`、`sports/tester-1`、`sports/convert-time`：异常 0 页。
- 回归抽查 `home / film / life / edu / medical`：全部残留 0 页。
- 译文自检：27 条全部不含汉字与探针 `RESIDUAL_RE` 全角中文标点；17 个改动 JSON 全部 `json.load` 合法。
- `_build.py` EXIT=0，A 级 100%（4684/4685）。
- 未跑 264 道全量门禁（协议：每 2–3 小时一次）。

## 变更范围
17 个文件：14 个 per-tool 字典（含 1 个属性映射补齐）、2 个 `_index.json`、`sw.js`、协议规则文档、本交接档。

## 遗留（下一批可继续）
- 真实残留剩余：`design 36 页`、`mechanical 13`、`finance 12`、`pet 9`（pet 的 40 条待译原文已在 `/tmp/en440_text.json` 中，需重新 extract）、合计约 70 页。
- `_en-i18n/pending/*.json` 仍为 11-04 滞后快照，建议专项 `--scan` 重建后再派工。
