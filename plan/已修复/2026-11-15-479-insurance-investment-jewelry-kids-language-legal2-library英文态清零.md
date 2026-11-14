# 479 · insurance / investment / jewelry / kids / language / legal2 / library 英文态清零（16 页 41 条）

## 问题
- insurance：年金现值问答、寿险保额需求与退保现金价值的整段代码口径说明。
- investment：几何平均收益示例序列。
- jewelry：钻石克拉公式、金纯度/珍珠/戒指尺寸 placeholder、戒指尺码匹配说明。
- kids：专注计时器状态机说明、记忆宫殿编码分段说明。
- language：语法检查规则口径、空输入提示、文本润色 8 条功能与场景。
- legal2：经济补偿金 N/N+1/2N 计算说明与个税阶梯。
- library：归档标签与统计报表 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 41 条。
`legal2/compensation-n1` 的「个税：」被 `_prefix` 半译为 `Personal tax：`，按 zh 源文作键；
`language/grammar-checker` 的「的/地/得、在/再」改写为英文表述，避免英文值残留汉字。

## 验证
- 7 个行业 `--check` 全部 **残留 0**（16 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
