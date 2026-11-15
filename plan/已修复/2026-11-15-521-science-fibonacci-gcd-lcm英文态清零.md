# 521 批：science 英文态清零（一）fibonacci / gcd / lcm

- 日期：2026-11-15
- 范围：`science/fibonacci`（19 条）、`gcd-calculator`（22 条）、`lcm-calculator`（21 条），共 62 条键。
- 手段：只改 `i18n/tools/en/science/*.json` 的 `map`；深度解析的标题、算例、误用提示、FAQ 整段英译。
- 备注：`gcd-calculator` 有一处被 `<strong>` 拆在公式中间的片段 `")，反复取余…"`，
  作键时须与运行时原文逐字一致（首字符为半角 `)` + 全角 `，`），本轮已按实际行修正。
- 验收：三页 `--check` 残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
- 剩余：science 尚有 log / median / mode / nato / permutation / power / quartile / root 八页。
