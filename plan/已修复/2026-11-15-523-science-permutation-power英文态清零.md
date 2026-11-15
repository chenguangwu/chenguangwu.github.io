# 523 批：science 英文态清零（三）permutation / power

- 日期：2026-11-15
- 范围：`permutation-calculator`（23 条）、`power-calculator`（26 条），共 49 条键。
- 手段：只改 `i18n/tools/en/science/*.json` 的 `map`；深览定义、算例、误用与 FAQ 整段英译。
- 备注：`permutation` 的「与组合数的关系」、`power` 的「0⁰ 的约定」被行内元素拆成多节点，按片段作键；
  `power` 中 `2^-10` 的显示精度说明保留原口径（12 位四舍五入 + locale 3 位）。
- 验收：两页 `--check` 残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
- 剩余：science 两页（quartile / root）。
