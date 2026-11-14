# 480 · logistics2 / marketing / martial / media / medical2 / metalwork 英文态清零（22 页 128 条）

## 问题
- logistics2：库存呆滞分析、缓冲包装厚度、S/U 型拣货路径对比三页公式块。
- marketing：广告预算分配算例、毛利率平衡线、折扣率与 UTM 命名问答（含被 `<code>` 拆开的片段）。
- martial：呼吸节奏/演练计时/桩步重心/抗击打 placeholder 与整段评级说明。
- media：评论情感分析、漏斗转化率、两页指标 placeholder。
- medical2：床位运营指标、药品效期分级、输液滴速、手术时长四页公式。
- metalwork：铜价序列统计说明、齿轮加工公式与 5 个 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 128 条。
`picking-route`（`推荐`→`Recommended`）、`routine-timer` / `stance-center`（`评级：`→`Rating:`）、
`inventory-aging`（`库存呆滞（ aging ）分析`）在 EN 态已被半译，均按 zh 源文作键。

## 验证
- 6 个行业 `--check` 全部 **残留 0**（22 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
