# 522 批：science 英文态清零（二）log / median / mode / nato

- 日期：2026-11-15
- 范围：`log-calculator`（25 条）、`median-calculator`（12 条）、`mode-calculator`（26 条）、`nato-phonetic`（11 条），共 74 条键。
- 手段：只改 `i18n/tools/en/science/*.json` 的 `map`；深览全文（定义、算例、误用、FAQ）英译。
- 坑：`log-calculator` 的「72 法则」与 `mode-calculator` 的「众数和平均数哪个更可靠」被行内元素拆成
  多个文本节点，按片段分别作键；`nato-phonetic` 的算例原文含「abc123测试」，
  英文值若照抄中文会继续触发残留判定，改为 `abc123!!!` 示例。
- 验收：四页 `--check` 残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
- 剩余：science 四页（permutation / power / quartile / root）。
