# 机械/金属加工 · tools/{machinery,metalwork,welding,manufacturing}（~160 页）

## 已知问题
### M1. 已修：banjin 折弯三式、sheet-bend 四式、calc-gear 系、forging、speed-itinerary、power-16/选型链、torque 系、pressure-4 花键几何、detector-55 评分。
### M2. 遗留：estimate-capacity 注释矛盾（G01-C2 小改）。

## 功能缺陷
- 切削页缺「材料-刀具匹配表」（45 号钢/不锈钢/铝 的 Vc/Ff 参考静态表）。
- 折弯页缺「回弹补偿」输入项。

## 优化点
- S7 引据：GB/ISO 标准号徽标（本类可信度关键）。
- S3 分步：齿轮/皮带选型链路图（已注入部分 chart，推广 S3 明细）。

## 受影响范围
- tools/machinery/（78）、tools/metalwork/（42）、tools/welding/、tools/manufacturing/

## 进度
- 🔴 待开发
