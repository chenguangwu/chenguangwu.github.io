# 牧/林/生态 · tools/{livestock,forestry,eco,beekeeping}（~70 页）

## 已知问题

## 功能缺陷
- 蜂养殖缺「春繁饲喂量」场景页（品类稀缺，SEO 蓝海）。

## 受影响范围
- tools/livestock/、tools/forestry/、tools/eco/、tools/beekeeping/（~70 页）

## 已知问题（批18 新增）
### E1. eco-10 / eco-16 「万 kWh」量纲口径存疑
- 描述：`eco-10` 年发电量 = capacity×hours÷1000、`eco-16` = capacity×cf÷100×8760，输入容量为 kW 口径时乘积为 kWh，÷1000 得 MWh（千 kWh），页面却标注「万 kWh」，差 10 倍；除非输入按「万 kW」口径（非常规）。此前 formula-eq 批沿用页面标注未纠。
- 方案：核对输入单位口径——若容量 kW，改标注「MWh/千 kWh」或公式 ×10；页面公式框与 dd 同步。
- 受影响：tools/eco/eco-10.html、tools/eco/eco-16.html
- 置信度：中

## 进度
- 🔴 待开发
