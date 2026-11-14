# 492 · maritime / process 英文态清零（16 页 50 条）

## 问题
- maritime：锚地容量与旋回水域 11 条、罗经差、航速-航程-时间 10 条。
- process：Cp/Cpk/Pp/Ppk、DPMO、FPY、RTY、西格玛水平、测量不确定度、最差/RSS 公差、X̄ 控制限等 13 页。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 50 条。
`maritime/speed-distance` 的「时间换算：」被 `_prefix` 半译为 `Time conversion:`，按 zh 源文作键。

## 验证
- maritime / process 两行业 `--check` 全部 **残留 0**（16 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
