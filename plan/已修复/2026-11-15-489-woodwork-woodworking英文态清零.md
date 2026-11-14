# 489 · woodwork / woodworking 英文态清零（11 页 69 条）

## 问题
斜切角度与刃口行程、榫接合尺寸、线干缩率与量级换算、桌面人机尺寸、家具阈值判定、
板英尺换算、木材含水率与干缩、榫卯尺寸、螺丝选型共 9 页公式块与 20 余个 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 69 条。
`board-feet` 的「换算：」被 `_prefix` 半译为 `Conversion:`，按 zh 源文作键；
`convert-30` 的量级换算示例被 `<code>` 拆成两段，按运行时片段分别作键。

## 验证
- woodwork / woodworking 两行业 `--check` 全部 **残留 0**（11 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
