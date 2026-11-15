# 510 · dermatology / ent 英文态清零（20 页 68 条）

## 问题
- `dermatology` 10 页 34 条：GAGS 痤疮部位系数表、VASI 计算公式与分级、HDSS 家族史提示、烧伤 TBSA/Parkland 说明，以及 `请选择…` / `恢复为未评估状态`；
- `ent` 10 页 34 条：AHI/ODI 口径、气骨导分型、喉功能声学参数、鼻阻力并联公式、鼓膜穿孔面积与 Jerger 分型等。

## 处理
只改源 `i18n/tools/en/<industry>/<slug>.json` 的 `map`，共 68 条。
被 `<strong>` 拆开的片段（如「GAGS 满分」「6 个部位」）按运行时片段分别作键。

## 验证
- dermatology / ent `--check` 均 **残留 0**（各 23 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
