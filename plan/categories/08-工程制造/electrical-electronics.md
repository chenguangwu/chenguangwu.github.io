# 电气/电子 · tools/{electrical,electronics,electromagnetism}（~80 页）

## 功能缺陷
- 导线选型缺「敷设方式/环境温度修正」联动（标准表静态可做）。
- 电子页缺「色环电阻图像识别」替代方案（纯文本速查表升级为交互拨盘）。

## 优化点
- S3 分步：电压降逐步计算展示（页面已有，统一到全类）。

## 受影响范围
- tools/electrical/（37）、tools/electronics/、tools/electromagnetism/

## 进度
- 🟡 续批中（剩余：电压降分步统一）

## 留存优化
- `tools/electrical/wire-gauge-selector.html`：补 50/70/95/120mm² 档位与「实际余量倍数」，增加三相 380V 口径。
- `tools/electrical/breaker-sizing.html`：增加 B/C/D 脱扣曲线与 Icu 分断能力输入，输出「过载/短路」两项校验；避免只给额定电流。
- `tools/electrical/transformer-sizing.html`：结果区并列「按计算负荷 / 按设备功率×Kd」两种口径的容量，并把 β 与经济负荷区间画成标尺。
- `tools/electrical/battery-bank.html`：补电池类型与 Peukert 指数、放电倍率 C 的提示，区分「标称/可用」能量；续航按恒功率与恒流两种口径对照。
- `tools/electronics/crystal-divider.html`：反求模式给出「分频 N / 倍频 M」候选表（含误差排序），并标注 PLL 参考频率与 VCO 上限。
- `tools/electronics/pcb-power.html`：增加散热过孔/铝基板/散热片等效热阻的可选项，输出「自然对流 vs 强制风冷」对照。

## 续查覆盖
- 已覆盖 8 页：`tools/electrical/voltage-drop.html`、`tools/electrical/wire-gauge-selector.html`、`tools/electrical/breaker-sizing.html`、`tools/electrical/transformer-sizing.html`、`tools/electrical/battery-bank.html`、`tools/electronics/capacitor-calculator.html`、`tools/electronics/crystal-divider.html`、`tools/electronics/pcb-power.html`。
- 未覆盖：`tools/electrical/`（目录共 35 个工具页）除本批 5 页与第一轮的 `power-factor-compensation.html` 外，其余 29 页未覆盖；`tools/electronics/`（共 21 个工具页）其余 18 页未覆盖；`tools/electromagnetism/` 全部未覆盖。第一轮页面本批未重复。
- 验证声明：仅源码阅读 + node 内存复算，未做真实浏览器、英文态（`?lang=en-US`）、移动端、门禁或线上验证；标准取值与器件手册亦未逐条核对。
