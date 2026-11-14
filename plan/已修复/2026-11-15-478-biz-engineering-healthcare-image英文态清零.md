# 478 · biz / engineering / healthcare / image 英文态清零（20 页 67 条）

## 问题
- biz：URL 提取正则说明、列表合并问答、字符横幅问答（含被 `<code>` 拆开的片段）。
- engineering：11 页力学/传热公式块与 placeholder（正应力、简支梁挠度、热膨胀、复合传热、截面特性）。
- healthcare：BMI 体重筛查、BMI 法体脂率 2 条简介。
- image：GIF 拆帧与马赛克两页长问答、微信封面渐变算例、九宫格 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 67 条。
- `biz/text-extract-urls` 的正则说明保留原转义与符号；`image/wechat-cover-maker` 保留色值、坐标与字号。
- 被 `<code>` 拆开的「、邮件与文档…」「…最多 256 色」等片段分别按运行时文本作键。

## 验证
- 4 个行业 `--check` 全部 **残留 0**（20 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
