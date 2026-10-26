# 电气/电子 · tools/{electrical,electronics,electromagnetism}（~80 页）

## 已知问题
## 功能缺陷
- 导线选型缺「敷设方式/环境温度修正」联动（标准表静态可做）。
- 电子页缺「色环电阻图像识别」替代方案（纯文本速查表升级为交互拨盘）。

## 优化点
- ✅ S2 场景（2026-10-26）：electrical/calc-1 加 3 预设「空调专线 4mm²」（wall/40℃）「厨房专线 6mm²」「380V 动力 25mm²」（XLPE/桥架/k₂=0.8），labelEn 双语；「4 平方能带多少瓦」由用户按 Iz×电压自行换算，页面已有公式说明。verify electrical 17→20、判别器 0 逃生、门禁 218/218。
- S3 分步：电压降逐步计算展示（页面已有，统一到全类）。

## 受影响范围
- tools/electrical/（37）、tools/electronics/、tools/electromagnetism/

## 进度
- 🟡 续批中（S2 已落地；剩余：导线敷设/环温修正联动表 / 色环电阻交互拨盘 / 电压降分步统一）
