# 电气/电子 · tools/{electrical,electronics,electromagnetism}（~80 页）

## 已知问题
## 功能缺陷
- 导线选型缺「敷设方式/环境温度修正」联动（标准表静态可做）。
- 电子页缺「色环电阻图像识别」替代方案（纯文本速查表升级为交互拨盘）。

## 优化点
- ✅ S2 场景（2026-10-26）：electrical/calc-1 加 3 预设「空调专线 4mm²」（wall/40℃）「厨房专线 6mm²」「380V 动力 25mm²」（XLPE/桥架/k₂=0.8），labelEn 双语；「4 平方能带多少瓦」由用户按 Iz×电压自行换算，页面已有公式说明。verify electrical 17→20、判别器 0 逃生、门禁 218/218。
- ✅ 敷设/环温修正联动表（2026-10-26）：calc-1 新增「敷设联动」tab，当前参数下 5 种敷设方式(自由/墙面/桥架/穿管/直埋)持续载流量联动表 + 环境温度修正系数 k₁ 参考表(25~50℃)；renderLinkage 在 calcCableCurrent 末渲染。verify electrical 20→21（Cu/PVC/4mm²/2芯/θₐ40℃ ⇒ 穿管行 20.5 A），判别器 0 逃生。
- ⚪ 色环电阻交互拨盘（2026-10-26 复核）：science/resistor-color-code.html 已为完整交互（4/5 环拨盘+反向查色环+E24+导出+历史+对照表），该项实质已满足，标记销案。
- S3 分步：电压降逐步计算展示（页面已有，统一到全类）。

## 受影响范围
- tools/electrical/（37）、tools/electronics/、tools/electromagnetism/

## 进度
- 🟡 续批中（S2 + 联动表已落地、电阻拨盘销案；剩余：电压降分步统一）
