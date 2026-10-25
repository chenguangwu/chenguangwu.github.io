# 家居/装修 · tools/{home,decor}（~40 页）

## 已知问题
### H1. 已修：detector-18 判限 18883-2022、dilution-ratio 1:N 口径、area-hours 速率基准、supply-usage 频率与总消耗。
### H2. 遗留：insulin-adjustment deep-dive 示例文案错（代码对）——同属 health，备注于本文件与 G03（改 content_deepdive.json 源）。
- 受影响：tools/health/insulin-adjustment.html（deep-dive 示例漏 ÷18 且「0.14/约1.4U」自相矛盾）

## 功能缺陷
- 涂料/壁纸页缺「门窗扣减」输入（现在靠手算）。
- 窗帘页已修缝边口径；缺「遮光/纱帘双层」组合估算。

## 优化点
- S2 场景：「89㎡ 两房刷墙」「3.6m 横厅窗帘」。
- S1 首屏即答案本类覆盖好（默认即结果），优先做 S3 用量明细表。

## 受影响范围
- tools/home/、tools/decor/（~40 页）

## 进度
- 🔴 待开发（H2 小改可先行）
