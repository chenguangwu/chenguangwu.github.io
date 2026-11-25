# UTM 转换：自动分带未处理挪威和斯瓦尔巴例外

## 问题

两处转换均只按普通 6° 经带计算带号，未处理挪威和斯瓦尔巴群岛的 UTM 特殊分带。例如 60°N、4°E 应落在特殊带 32V，页面却按普通分带选 31，导致坐标采用不同中央经线。

## 解决方案

实现适用区域的特殊分带规则并明确采用的基准；验证挪威、斯瓦尔巴边界及普通经带转换。

## 受影响工具路径

- `tools/science/latlon-utm-converter.html`
- `tools/science/astronomy-toolkit.html`
